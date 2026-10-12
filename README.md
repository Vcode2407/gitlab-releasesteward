# ReleaseSteward

A new Path A entry for **Life After Code**. ReleaseSteward checks whether old and new application clients can coexist during a database migration. The local workbench executes real SQLite checks, compares a breaking rename with an expand/backfill strategy, and exports reproducible evidence.

Public MIT source mirror: [Vcode2407/gitlab-releasesteward](https://github.com/Vcode2407/gitlab-releasesteward). ReleaseSteward is also published in the [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase). Its [initial GitLab pipeline](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937132819) passed eight tests and the 9/9 compatible-fixture gate at commit `e39a7a4493f0c058d29e8e2ff1700a4807c6f1bb`. The [first actual Duo session](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9306854) finished with a failed rollback check and unreadable reviewer evidence. This portable-rollback revision needs its own GitLab publication, pipeline and saved catalog verification before another run. Successful Duo review remains unverified.

[Watch the actual silent local walkthrough](docs/LOCAL_DEMO.md) (1:50): real rename, expand/backfill and failed-migration results, with downloadable recording evidence. The recording preserves its status at capture; the later failed Duo session is retained separately.

## Run and verify

Use Python 3.12. There are no external runtime dependencies.

```powershell
python release_steward.py serve
python -m unittest discover -s tests -v
python release_steward.py audit --scenario expand-contract --require-pass
```

Open http://127.0.0.1:4184. Start with **Rename status in one release**. The migration applies, but old clients fail. Choose **Try the compatible strategy**; both clients can read, write, and insert. Backfill, default-value, and rollback checks execute in a fresh in-memory database. Export the report, inspect the exact SQL and hashes, and retain it with the CI pipeline.

The harness contains three controlled strategies and a work-order application fixture. It does not accept arbitrary SQL or certify production migrations. The compatible fixture models an expand phase; removing the legacy column is a later release after old clients retire. See [the reproducible judge walkthrough](docs/JUDGE_SETUP.md) for expected checks, exports, command-line failure gates, and troubleshooting.

## Public source verification

The [GitHub workflow](.github/workflows/verify.yml) pins its four actions to reviewed commit hashes. It runs the nine tests, checks browser JavaScript with Node 22, and executes the expand/backfill scenario with a required compatible verdict. Its artifact contains the executed report and a separate GitHub run record. The report's GitLab `commit` and `pipeline` fields remain empty on GitHub; the companion file records the actual GitHub commit and run URL.

The [first public verification run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) passed for commit `3ae3adf29e40edabc52256cc4587ba76557d9d0f`. Check [later Actions runs](https://github.com/Vcode2407/gitlab-releasesteward/actions/workflows/verify.yml) when reviewing another revision. GitHub execution is source-validation evidence and does not establish GitLab CI or Duo execution.

## GitLab Duo integration: first run failed, correction prepared

GitLab Duo execution is mandatory for the event. The project is **not submission-ready**. The [first-run record](docs/evidence/duo-session-9306854.json) retains the actual 8/9 failure on the runner's verified SQLite 3.34.1, the inaccessible ignored report paths, and the mismatch between source YAML and the old configuration actually executed. The rollback now rebuilds the fixed fixture's legacy table, preserving its synchronized data without `DROP COLUMN`.

`.gitlab/duo/release-steward.yaml` keeps the inspector and read-only reviewer. The inspector retains `docs/evidence/duo-rename-evidence.json` and `docs/evidence/duo-evidence.json`; these specific paths are not ignored. The reviewer reads both independently and reports incomplete evidence. Generated reports are not committed as execution proof. Command limits remain prompt instructions, not an enforced command allowlist. Verify the saved catalog's exact command and reviewer text before another run; source publication alone does not update the catalog. Local report labels and CI metadata do not establish successful Duo execution.

1. Follow the [assigned project's onboarding issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). Account registration and provisioning approval are complete; project access does not establish executed automation.
2. Merge this revision into the assigned project while preserving its onboarding and source history; run and inspect a new pipeline for that exact commit.
3. Update the existing catalog flow with the revised YAML and verify its saved configuration on a freshly loaded page. Confirm both exact output paths and the reviewer prompt before another authorized Mention-triggered fixture inspection.
4. Verify actual command output and exported hashes; record the Duo session and visible pipeline history. If catalog validation rejects a field, fix it using the live instance's docs rather than claiming an executed flow.

Follow [the concrete GitLab onboarding and execution guide](docs/GITLAB_SETUP.md), including the prepared goal text and evidence checklist. References: [custom flows](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), [custom-flow schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/), [flow registry v1](https://docs.gitlab.com/user/duo_agent_platform/flows/claude-edit-v1-flow-registry/).

## Submission checklist

Deadline: **October 27, 2026, 18:30 IST**. [Official rules](https://gitlab-transcend.devpost.com/rules).

- [ ] Actual GitLab Duo session completes the compatibility gate and independent report review successfully.
- [x] Public MIT GitLab repository with run instructions and initial visible pipeline history; this revision still needs its own publication and run.
- [x] Public MIT GitHub source mirror published.
- [ ] English description explaining migration compatibility, fixture limits and actual Duo behavior.
- [ ] Public YouTube demo under three minutes.
- [ ] Final Devpost fields and links verified.

Suggested 2:40 recording: introduce a mixed-client rollout (20s), execute the breaking rename (40s), show Duo investigating and rerunning the compatible strategy (60s), review hashes/CI evidence and the human release decision (40s).
