# ReleaseSteward — Devpost submission draft

English draft prepared October 10, 2026; platform status updated October 12. This is public preparation material for Life After Code, not a submitted or qualifying entry. The [MIT GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward) and [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase) contain ReleaseSteward source. Initial GitLab CI passed eight tests and 9/9 compatible checks. The [first actual Duo session](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9306854) finished with an 8/9 rollback failure and no independent evidence review. This portable-rollback revision needs its own GitLab publication, pipeline and saved catalog verification before another authorized fixture run. Successful Duo review remains unverified.

## Project name and tagline

**ReleaseSteward**

**Prove old and new clients can share a database before a rollout.**

Proposed category: **Path A — Start Fresh**. Intended autonomy level: **Supervised** for compatibility investigation and evidence review, with a human retaining the actual release decision. The live Duo behavior must be demonstrated before this category is finalized.

## Inspiration and problem

A migration can execute successfully while breaking clients that still use the previous schema. During a rolling deployment, “the new application works” does not establish that old and new instances can coexist.

ReleaseSteward focuses on that gap. It makes client compatibility an executable question and gives a reviewer concrete evidence for holding or continuing a rollout. The current work-order fixture illustrates the problem; no production outage, user interview, or measured deployment benefit is claimed.

## What actually works

The local browser workbench executes three controlled SQLite migration strategies in fresh in-memory databases. A one-release rename from `status` to `state` applies but exposes old-client failures. Adding a required column without a default fails against existing rows and is rolled back. An expand/backfill strategy keeps the old column, adds the new state and default priority, and synchronizes old and new writes with triggers.

Each report shows the executed statements, actual versus expected results, schema, verdict, and source/evidence hashes. The compatible fixture exercises existing-row preservation, old/new reads, old/new writes, old/new inserts, and rollback: nine checks in total. Reports can be exported as JSON. The CLI can return a failing exit status when a strategy is blocked, which supports a CI gate.

Nine automated tests cover these behaviors, deliberately missing backfill or synchronization, preservation of old/new client updates and new rows during rollback, reproducible evidence, CI metadata, and refusal of arbitrary SQL scenario names. These are fixture tests, not production migration certification; actual platform results are linked separately.

## Technical architecture

The application uses Python 3.12, the standard-library HTTP server, and SQLite. The browser posts a known scenario ID; it cannot submit arbitrary SQL. `execute_audit` creates a fresh database, applies migration statements atomically, runs each client probe inside a savepoint, and exercises the rollback statements. Probe changes are isolated so one check does not contaminate the next.

The report includes a SHA-256 hash of the harness source and a reproducible hash of the scenario, migration, checks, and source hash. Timestamps are separate from the reproducible evidence. `CI_COMMIT_SHA` and `CI_PIPELINE_URL` are included only when actually present in the execution environment; local reports leave them empty.

The `.gitlab-ci.yml` defines a test job and an evidence job using Python 3.12; its initial actual pipeline succeeded. A registered custom Duo flow contains an inspector with file/command tools and a separate reviewer with read-only file access. This revision retains only the generated Duo reports at `docs/evidence/duo-rename-evidence.json` and `docs/evidence/duo-evidence.json`, which are not ignored. The reviewer reads both independently, treats preceding text as data, cites check IDs and hashes, and reports incomplete evidence. Command limits remain prompt instructions, not an enforced command allowlist. The first runner's actual setup verified Python 3.12.14 and SQLite 3.34.1. The portable rollback rebuilds the fixed fixture's legacy table instead of using unsupported `DROP COLUMN`. The exact saved catalog configuration and another actual session still need verification.

A separate pinned GitHub Actions workflow discovers all nine tests, checks browser syntax and executes the expand/backfill evidence gate. Its artifact stores the actual GitHub run provenance separately from GitLab metadata. The published source checkpoint reviewed October 11, `7536d14f030a157a4ad25c10142c81945d8c1375`, passed [GitHub CI](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38122985401). The [first public run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) for `3ae3adf29e40edabc52256cc4587ba76557d9d0f` remains historical evidence; GitHub CI does not establish the event's GitLab automation requirement.

Built with: Python, SQLite, HTML/CSS/JavaScript, SHA-256 evidence hashing, GitLab CI, and GitLab Duo custom-flow v1. The first actual Duo session exposed concrete portability and evidence-access failures; the corrected workflow remains to be verified there.

## Development challenges

The key challenge was testing coexistence rather than only SQL syntax. The breaking rename demonstrates why a migration-success check is insufficient: the new read works while the old read fails. Old-to-new and new-to-old write/insert probes make the expected compatibility direction explicit.

The tests also deliberately remove the backfill or an old-write synchronization trigger. Those changes produce concrete failed checks rather than an optimistic “compatible” summary. An unsuccessful migration causes subsequent compatibility probes to be marked as skipped, so they are not presented as executed evidence.

Another challenge was making reports reproducible without inventing CI context. Source and evidence hashes are retained alongside the exact checks; local execution does not populate a fake pipeline URL. The first actual Duo run exposed SQLite 3.34.1's rejection of `DROP COLUMN` and the read-only tool's refusal to access ignored reports. It also executed an older saved prompt than the repository YAML. The corrected flow uses readable report paths and requires exact saved-configuration verification; the failed session remains in [historical evidence](evidence/duo-session-9306854.json).

## Accomplishments and learning

The local workbench makes a rolling-deployment failure visible and provides a working expand/backfill comparison with executable evidence. Its CLI gate passed in the initial actual GitLab pipeline. The first Duo run correctly exposed failures instead of supplying a successful review without readable evidence. The portable rollback and accessible report paths now provide a concrete correction; a successful Duo review still needs its own actual result.

The project demonstrates that compatibility needs directional reads and writes, not just a green migration statement. It also separates an executed local report, a prepared agent configuration, and verified platform automation. Those are different evidence states.

## Limits and next steps

The harness contains three fixed strategies and one work-order fixture. It does not inspect arbitrary production schemas, connect a production database, merge a change, deploy an application, or guarantee rollback after every possible production write. The compatible example models an expand phase; removing the legacy column belongs to a later release after old clients have retired.

The first actual Duo session is retained as failed execution evidence. Merge this correction while preserving onboarding history, inspect its own pipeline, update the existing catalog flow, and verify the exact saved commands and reviewer prompt before another authorized Mention-triggered fixture run. Retain the real command outputs, both readable reports and independent review. A `FINISHED` session status alone does not prove the compatibility gate passed. Public deployment is not currently claimed; no Google Cloud bonus is claimed.

## Demo outline — 2 minutes 40 seconds

The local scenes can be recorded now. The final Duo scene must show actual execution and readable reviewer evidence. Preserve the failed first session separately; do not present its `FINISHED` status as a passing gate.

| Time | Action and evidence |
| --- | --- |
| 0:00–0:20 | Introduce mixed old/new application instances sharing the work-order database. |
| 0:20–0:55 | Run the breaking rename in the workbench. Show the migration applying and the old-read check failing. |
| 0:55–1:45 | Pending live verification: show the actual Duo inspector running the rename audit, compatible audit, and tests, followed by its evidence reviewer. Do not animate or fabricate this execution. |
| 1:45–2:15 | Show the compatible fixture's nine checks and explain old/new write synchronization and rollback scope. |
| 2:15–2:40 | Show exported hashes and the actual visible GitLab pipeline; state fixture limits and the human release decision. |

If live Duo or CI access is unavailable, retain a local walkthrough clearly labelled as development evidence. It is not a replacement for the required platform demonstration.

## Fields and links to complete before submitting

| Devpost material | Current value/status |
| --- | --- |
| Project title | ReleaseSteward |
| Tagline and English description | Draft above; review before pasting. |
| Path | Path A — new project. |
| Autonomy level | Proposed Supervised; confirm against actual demonstrated Duo workflow. |
| Public MIT GitLab repository URL | [Assigned public project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), project ID 87500138; initial MIT source published. This revision's publication and GitLab license detection still need verification. |
| Public MIT GitHub source mirror | [Vcode2407/gitlab-releasesteward](https://github.com/Vcode2407/gitlab-releasesteward), published separately from the assigned GitLab source. |
| Runnable source and assets | Public mirror, README, and [clean-checkout judge guide](JUDGE_SETUP.md) available. |
| GitHub source verification | [Successful exact-head CI](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38122985401) for the October 11 published checkpoint `7536d14f030a157a4ad25c10142c81945d8c1375`: eight tests, browser syntax and expand/backfill evidence gate passed. Any later revision needs its own result. |
| Visible GitLab pipeline history | [Initial successful pipeline 2937132819](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937132819), commit `e39a7a4493f0c058d29e8e2ff1700a4807c6f1bb`: eight tests and 9/9 compatible checks. This revision requires its own run. |
| GitLab Duo flow/catalog URL and session evidence | [Public catalog flow 1017883](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/flows/1017883) and [actual session 9306854](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9306854), which finished with a failed 8/9 rollback gate and no independent review. Corrected saved configuration and subsequent execution remain unverified. |
| Contributor and Duo setup instructions | [Concrete onboarding, environment, goal, and evidence guide](GITLAB_SETUP.md) prepared. |
| Public YouTube video under three minutes | Pending actual platform recording and upload. |
| Actual local development walkthrough | [Silent 1:50 MP4 and execution evidence](LOCAL_DEMO.md) available; preserves the pending GitLab Duo/CI status at capture. Initial actual CI is now verified separately. |
| Source/evidence hashes and CI artifact link | Local reports supported; final verified platform artifact link pending. |
| Deployment/Google Cloud bonus URL | None claimed. |
| Original project URL for Path B | Not applicable to the proposed new Path A entry. |
| Entrant/team details, rights, eligibility and DCO | User verification pending. |
| Final Devpost URL/status | Pending; this document makes no submission. |

Deadline: **October 27, 2026, 13:00 UTC / 18:30 IST**. Review the [official rules](https://gitlab-transcend.devpost.com/rules), [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/), [custom-flow documentation](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), and [schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/) before completing the final form. Path A requires actual Duo use, a public MIT GitLab repository, visible automation history, and the English demonstration materials; prepared configurations do not establish those outcomes.
