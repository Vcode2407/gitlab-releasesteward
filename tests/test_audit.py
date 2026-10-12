import unittest
from unittest.mock import patch
from release_steward import execute_audit, new_database, SCENARIOS


class CompatibilityTests(unittest.TestCase):
    def test_rename_exposes_rolling_deployment_failure(self):
        report = execute_audit("rename-column")
        checks = {item["id"]: item for item in report["checks"]}
        self.assertTrue(checks["migration"]["passed"])
        self.assertTrue(checks["new-read"]["passed"])
        self.assertFalse(checks["old-read"]["passed"])
        self.assertIn("no such column", checks["old-read"]["actual"])
        self.assertEqual(report["verdict"], "blocked")

    def test_required_column_reports_atomic_failure(self):
        report = execute_audit("required-column")
        self.assertFalse(report["checks"][0]["passed"])
        self.assertIn("NOT NULL", report["operations"][0]["error"])
        self.assertEqual(report["passed"], 0)
        self.assertTrue(all(item.get("skipped") for item in report["checks"][1:]))

    def test_expand_contract_exercises_reads_writes_inserts_and_rollback(self):
        report = execute_audit("expand-contract")
        self.assertEqual(report["verdict"], "compatible")
        self.assertEqual(report["passed"], 9)
        self.assertTrue(all(item["passed"] for item in report["checks"]))
        self.assertEqual(len(report["evidenceHash"]), 64)

    def test_missing_backfill_is_caught_by_new_read(self):
        changed = dict(SCENARIOS["expand-contract"])
        changed["up"] = [sql for sql in changed["up"] if not sql.startswith("UPDATE work_orders SET state")]
        with patch.dict(SCENARIOS, {"missing-backfill": changed}):
            report = execute_audit("missing-backfill")
        checks = {item["id"]: item for item in report["checks"]}
        self.assertFalse(checks["new-read"]["passed"])

    def test_expand_rollback_preserves_old_and_new_client_changes(self):
        db = new_database()
        try:
            for sql in SCENARIOS["expand-contract"]["up"]:
                db.execute(sql)
            db.execute("UPDATE work_orders SET status='closed' WHERE id=1")
            db.execute("UPDATE work_orders SET state='open' WHERE id=2")
            db.execute("INSERT INTO work_orders (id,title,state) VALUES (3,'New-client work','closed')")
            db.commit()
            db.execute("BEGIN")
            for sql in SCENARIOS["expand-contract"]["down"]:
                db.execute(sql)
            db.commit()
            self.assertEqual(db.execute("SELECT id,title,status FROM work_orders ORDER BY id").fetchall(), [
                (1, "Install the display", "closed"),
                (2, "Repair the scanner", "open"),
                (3, "New-client work", "closed"),
            ])
            self.assertEqual([row[1] for row in db.execute("PRAGMA table_info(work_orders)")], ["id", "title", "status"])
            db.execute("INSERT INTO work_orders (id,title) VALUES (4,'Old-client default')")
            self.assertEqual(db.execute("SELECT status FROM work_orders WHERE id=4").fetchone(), ("open",))
        finally:
            db.close()

    def test_missing_sync_trigger_is_caught(self):
        changed = dict(SCENARIOS["expand-contract"])
        changed["up"] = [sql for sql in changed["up"] if not sql.startswith("CREATE TRIGGER sync_status")]
        with patch.dict(SCENARIOS, {"missing-sync": changed}):
            report = execute_audit("missing-sync")
        self.assertFalse(next(item for item in report["checks"] if item["id"] == "old-write")["passed"])

    def test_evidence_is_reproducible_and_different_for_different_migrations(self):
        one, two = execute_audit("expand-contract"), execute_audit("expand-contract")
        self.assertEqual(one["evidenceHash"], two["evidenceHash"])
        self.assertNotEqual(one["evidenceHash"], execute_audit("rename-column")["evidenceHash"])

    def test_ci_metadata_is_reported_only_from_actual_environment(self):
        with patch.dict("os.environ", {"CI_PIPELINE_URL": "https://gitlab.example.test/pipelines/123", "CI_COMMIT_SHA": "a" * 40}):
            report = execute_audit("expand-contract")
        self.assertEqual(report["pipeline"], "https://gitlab.example.test/pipelines/123")
        self.assertEqual(report["commit"], "a" * 40)

    def test_arbitrary_sql_cannot_be_selected_as_a_scenario(self):
        with self.assertRaises(ValueError):
            execute_audit("DROP TABLE work_orders")


if __name__ == "__main__":
    unittest.main()
