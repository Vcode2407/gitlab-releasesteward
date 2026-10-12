# Reproduce ReleaseSteward

Public MIT source: [assigned GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), with a separate [GitHub mirror](https://github.com/Vcode2407/gitlab-releasesteward). This guide reproduces the controlled local database harness. Corrected [Duo session 9307096](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9307096) passed all nine tests and 9/9 compatible checks on SQLite 3.34.1 at code commit `6897bd93`. Its reviewer declared both reports read and cited consistent check IDs and hashes; separate file-read traces are not exposed. The [setup guide](GITLAB_SETUP.md) retains the verified CI, corrected run and historical first-run failure.

## Clean checkout

Install Python 3.12 and Git. Node.js 22 is needed only for the browser JavaScript syntax check. The application and Python tests use the standard library; no package installation, database account, API key, or external service is required.

```powershell
git clone https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase.git releasesteward
cd releasesteward
python --version
python -m unittest discover -s tests -v
node --check public/app.js
python release_steward.py serve
```

On Windows with multiple Python installations, use `py -3.12` in place of `python`. On Linux, `python3.12` is suitable. The `release_steward.py serve` subcommand serves both the workbench assets and its audit API. It prints its actual address and binds to loopback. Open [the local workbench](http://127.0.0.1:4184). If that port is occupied, start with `python release_steward.py serve --port 4194` and open that printed URL. Stop the server with Ctrl+C.

The local workbench links the completed October 12 Duo inspection. Running local checks executes SQLite fixtures; it does not start another Duo session. The dated October 10 footage retains its original pending banner.

## Browser walkthrough

1. Select **Rename status in one release**, then **Run compatibility checks**. The result is blocked with **3/9** checks passing. Inspect the successful migration and new-client read beside the failed old-client read. A successful SQL statement did not preserve rolling compatibility.
2. Select **Try the compatible strategy**. A new in-memory audit of the authored expand/backfill fixture returns **9/9**, with compatible reads, writes, inserts, default priority, and rollback. This selects the prepared strategy; no model wrote a repair.
3. Open **Migration, schema and provenance**. Review the SQL, schema, actual/expected probe output, source hash, and evidence hash. Select **Export evidence JSON** and retain that report.
4. Select **Add a required column without a default**, then run it. Existing rows cause a real SQLite constraint failure; dependent checks are skipped. No fabricated successful migration is shown.

Changing scenarios clears the previous report. Each audit uses a fresh in-memory database and isolated probe savepoints. Reloading clears the browser view; no production database or persistent client data is connected.

## Command-line evidence and release gate

Generate the same successful evidence without a browser:

```powershell
python release_steward.py audit --scenario expand-contract --output artifacts/release-evidence.json --require-pass
```

It writes the report and exits successfully only for the compatible verdict. Exercise the failing gate separately:

```powershell
python release_steward.py audit --scenario rename-column --output artifacts/rename-evidence.json --require-pass
```

The blocked rename exits with code **1**, while retaining the failed-check report. Inspect `$LASTEXITCODE` in PowerShell or `echo $?` in a POSIX shell immediately after that command. The nonzero result is expected development evidence.

The reproducible `evidenceHash` depends on the scenario, migration, checks, and `sourceHash`; run timestamps are separate. Reports do not invent CI URLs. Local runs have empty GitLab provenance. GitHub Actions keeps its real run URL and checked-out commit in the separate `github-run.json` artifact; GitLab jobs populate the report's GitLab fields from their actual environment.

## What this verifies

The current suite contains nine tests. They cover the known fixtures, missing backfill, missing synchronization, rollback preservation of old/new client updates and newly inserted rows, reproducible hashes, actual-environment metadata, and rejection of arbitrary SQL scenario names. Browser success, local CLI success, GitHub CI success, GitLab CI success, and Duo execution are distinct evidence states.

These checks cover one work-order fixture and three authored strategies. They do not certify arbitrary migrations, real workloads, or production rollback. A human makes the actual release decision. Review the linked public GitLab source, CI and actual Duo session alongside [the revised public silent 2:44 YouTube demo](https://www.youtube.com/watch?v=xGsDpR_3hEg). [Final demo downloads and provenance](FINAL_DEMO.md) include the video and English captions. Final Devpost submission remains pending.
