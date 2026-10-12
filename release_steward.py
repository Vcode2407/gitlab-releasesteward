"""ReleaseSteward: execute migration compatibility checks in isolated SQLite memory."""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SEED = [(1, "Install the display", "open"), (2, "Repair the scanner", "closed")]
SCENARIOS = {
    "rename-column": {
        "name": "Rename status in one release",
        "description": "The new client works, but a rolling deployment still has clients reading status.",
        "up": ["ALTER TABLE work_orders RENAME COLUMN status TO state"],
        "down": ["ALTER TABLE work_orders RENAME COLUMN state TO status"],
        "repair": "expand-contract",
    },
    "required-column": {
        "name": "Add a required column without a default",
        "description": "Existing rows cannot satisfy a new NOT NULL priority column.",
        "up": ["ALTER TABLE work_orders ADD COLUMN priority TEXT NOT NULL"],
        "down": [],
        "repair": "expand-contract",
    },
    "expand-contract": {
        "name": "Expand, backfill, keep both clients compatible",
        "description": "Keep status while introducing state. Synchronize old and new writes during the rollout.",
        "up": [
            "ALTER TABLE work_orders ADD COLUMN state TEXT",
            "ALTER TABLE work_orders ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal'",
            "UPDATE work_orders SET state = status",
            "CREATE TRIGGER sync_status AFTER UPDATE OF status ON work_orders WHEN NEW.state IS NOT NEW.status BEGIN UPDATE work_orders SET state = NEW.status WHERE id = NEW.id; END",
            "CREATE TRIGGER sync_state AFTER UPDATE OF state ON work_orders WHEN NEW.status IS NOT NEW.state BEGIN UPDATE work_orders SET status = NEW.state WHERE id = NEW.id; END",
            "CREATE TRIGGER sync_insert AFTER INSERT ON work_orders BEGIN UPDATE work_orders SET state = COALESCE(NEW.state, NEW.status), status = COALESCE(NEW.state, NEW.status) WHERE id = NEW.id; END",
        ],
        "down": [
            "DROP TRIGGER sync_status", "DROP TRIGGER sync_state", "DROP TRIGGER sync_insert",
            "CREATE TABLE work_orders_rollback (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open')",
            "INSERT INTO work_orders_rollback (id, title, status) SELECT id, title, status FROM work_orders",
            "DROP TABLE work_orders",
            "ALTER TABLE work_orders_rollback RENAME TO work_orders",
        ],
        "repair": None,
    },
}


def new_database():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE work_orders (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open')")
    db.executemany("INSERT INTO work_orders VALUES (?, ?, ?)", SEED)
    db.commit()
    return db


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def execute_audit(scenario_id):
    if scenario_id not in SCENARIOS:
        raise ValueError("Choose a known migration scenario.")
    scenario = SCENARIOS[scenario_id]
    db = new_database()
    operations = []
    checks = []
    migration_ok = True
    try:
        db.execute("BEGIN")
        for sql in scenario["up"]:
            try:
                db.execute(sql)
                operations.append({"sql": sql, "passed": True})
            except sqlite3.Error as error:
                operations.append({"sql": sql, "passed": False, "error": str(error)})
                migration_ok = False
                break
        if migration_ok:
            db.commit()
        else:
            db.rollback()
        checks.append({"id": "migration", "name": "Migration applies to existing rows", "passed": migration_ok,
                       "expected": "All statements succeed atomically", "actual": "Applied" if migration_ok else "Rolled back after a SQLite error"})

        def check(check_id, name, expected, probe):
            if not migration_ok:
                checks.append({"id": check_id, "name": name, "passed": False, "skipped": True, "expected": expected, "actual": "Not run: migration failed"})
                return
            db.execute("SAVEPOINT probe")
            try:
                actual = probe(db)
                checks.append({"id": check_id, "name": name, "passed": actual == expected, "expected": expected, "actual": actual})
            except sqlite3.Error as error:
                checks.append({"id": check_id, "name": name, "passed": False, "expected": expected, "actual": str(error)})
            finally:
                db.execute("ROLLBACK TO probe")
                db.execute("RELEASE probe")

        check("rows", "Original records retain the old-client shape", SEED,
              lambda connection: connection.execute("SELECT id, title, status FROM work_orders ORDER BY id").fetchall())
        check("old-read", "Old client can read open work", [1],
              lambda connection: [row[0] for row in connection.execute("SELECT id FROM work_orders WHERE status='open' ORDER BY id")])
        check("new-read", "New client can read open work", [1],
              lambda connection: [row[0] for row in connection.execute("SELECT id FROM work_orders WHERE state='open' ORDER BY id")])

        def old_write(connection):
            connection.execute("UPDATE work_orders SET status='closed' WHERE id=1")
            return connection.execute("SELECT state FROM work_orders WHERE id=1").fetchone()[0]

        def new_write(connection):
            connection.execute("UPDATE work_orders SET state='open' WHERE id=2")
            return connection.execute("SELECT status FROM work_orders WHERE id=2").fetchone()[0]

        def old_insert(connection):
            connection.execute("INSERT INTO work_orders (id,title,status) VALUES (3,'Set up a printer','open')")
            return connection.execute("SELECT state,priority FROM work_orders WHERE id=3").fetchone()

        def new_insert(connection):
            connection.execute("INSERT INTO work_orders (id,title,state) VALUES (3,'Set up a printer','closed')")
            return connection.execute("SELECT status,priority FROM work_orders WHERE id=3").fetchone()

        check("old-write", "Old writes are visible to new clients", "closed", old_write)
        check("new-write", "New writes are visible to old clients", "open", new_write)
        check("old-insert", "Old inserts have a new state and default priority", ("open", "normal"), old_insert)
        check("new-insert", "New inserts remain readable by old clients", ("closed", "normal"), new_insert)
        schema = [row[0] for row in db.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY name")]
        if migration_ok:
            try:
                db.execute("BEGIN")
                for sql in scenario["down"]:
                    db.execute(sql)
                actual = db.execute("SELECT id,title,status FROM work_orders ORDER BY id").fetchall()
                checks.append({"id": "rollback", "name": "Rollback preserves original data", "passed": actual == SEED, "expected": SEED, "actual": actual})
                db.rollback()
            except sqlite3.Error as error:
                db.rollback()
                checks.append({"id": "rollback", "name": "Rollback preserves original data", "passed": False, "expected": SEED, "actual": str(error)})
        else:
            checks.append({"id": "rollback", "name": "Rollback preserves original data", "passed": False, "skipped": True, "expected": SEED, "actual": "Not run: migration failed"})
    finally:
        db.close()

    passed = sum(item["passed"] for item in checks)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    evidence = {"scenario": scenario_id, "migration": scenario["up"], "checks": checks, "sourceHash": source_hash}
    return {
        "scenario": scenario_id, "name": scenario["name"], "description": scenario["description"],
        "verdict": "compatible" if passed == len(checks) else "blocked",
        "passed": passed, "total": len(checks), "checks": checks, "operations": operations,
        "schema": schema, "repairScenario": scenario["repair"],
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "evidenceHash": fingerprint(evidence), "sourceHash": source_hash,
        "commit": os.getenv("CI_COMMIT_SHA") or None, "pipeline": os.getenv("CI_PIPELINE_URL") or None,
        "runtime": {"python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version},
        "mode": "Actual controlled SQLite checks; platform execution requires separate evidence",
    }


class Handler(BaseHTTPRequestHandler):
    def response(self, status, data, mime="application/json; charset=utf-8"):
        body = json.dumps(data).encode() if not isinstance(data, bytes) else data
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def trusted_host(self):
        return self.headers.get("Host") in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}

    def do_GET(self):
        if not self.trusted_host():
            return self.response(403, {"error": "Untrusted host"})
        route = urlparse(self.path).path
        if route == "/api/scenarios":
            return self.response(200, {"scenarios": [{"id": key, "name": item["name"], "description": item["description"]} for key, item in SCENARIOS.items()], "duoVerified": False})
        files = {"/": ("index.html", "text/html; charset=utf-8"), "/app.js": ("app.js", "text/javascript; charset=utf-8"), "/style.css": ("style.css", "text/css; charset=utf-8")}
        if route in files:
            name, mime = files[route]
            return self.response(200, (ROOT / "public" / name).read_bytes(), mime)
        self.response(404, {"error": "Not found"})

    def do_POST(self):
        allowed = {f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}"}
        if not self.trusted_host() or self.headers.get("Origin") not in allowed | {None}:
            return self.response(403, {"error": "Untrusted origin"})
        if self.path != "/api/audit":
            return self.response(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 2048:
                return self.response(413, {"error": "Provide a small JSON scenario request"})
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or set(data) != {"scenario"}:
                raise ValueError("Provide only a scenario ID; arbitrary SQL is not accepted.")
            report = execute_audit(data["scenario"])
            self.response(200, report)
        except (ValueError, TypeError, KeyError):
            self.response(400, {"error": "Choose a known migration scenario. Arbitrary SQL is not accepted."})

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    serve = sub.add_parser("serve")
    serve.add_argument("--port", type=int, default=4184)
    audit = sub.add_parser("audit")
    audit.add_argument("--scenario", choices=SCENARIOS, default="expand-contract")
    audit.add_argument("--output")
    audit.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    if args.command == "serve":
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
        print(f"ReleaseSteward: http://127.0.0.1:{server.server_port}", flush=True)
        print("Local SQLite execution. Recorded GitLab Duo inspection: https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9307096", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
    else:
        result = execute_audit(args.scenario)
        output = json.dumps(result, indent=2)
        if args.output:
            destination = Path(args.output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(output + "\n", encoding="utf-8")
        print(output)
        if args.require_pass and result["verdict"] != "compatible":
            sys.exit(1)


if __name__ == "__main__":
    main()
