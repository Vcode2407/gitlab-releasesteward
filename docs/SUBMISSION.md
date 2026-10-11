# ReleaseSteward — Devpost submission draft

English draft prepared October 10, 2026. This is public preparation material for Life After Code, not a submitted or qualifying entry. The [MIT GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward) is published and local SQLite execution works; live GitLab Duo and GitLab CI execution remain unverified.

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

Eight automated tests cover these behaviors, deliberately missing backfill or synchronization, reproducible evidence, CI metadata, and refusal of arbitrary SQL scenario names. These are local fixture tests, not a live GitLab session or production migration certification.

## Technical architecture

The application uses Python 3.12, the standard-library HTTP server, and SQLite. The browser posts a known scenario ID; it cannot submit arbitrary SQL. `execute_audit` creates a fresh database, applies migration statements atomically, runs each client probe inside a savepoint, and exercises the rollback statements. Probe changes are isolated so one check does not contaminate the next.

The report includes a SHA-256 hash of the harness source and a reproducible hash of the scenario, migration, checks, and source hash. Timestamps are separate from the reproducible evidence. `CI_COMMIT_SHA` and `CI_PIPELINE_URL` are included only when actually present in the execution environment; local reports leave them empty.

A prepared `.gitlab-ci.yml` defines a test job and an evidence job using Python 3.12. A prepared custom Duo flow contains an inspector with file/command tools and a separate evidence reviewer with read-only file access. The inspector is instructed to run the actual harness and tests; the reviewer must cite observed check IDs and hashes and reject unsupported success claims. The agent environment file checks Python 3.12 and SQLite in GitLab's default image. Catalog validation, runner setup, project enablement, and actual Duo execution are still pending.

A separate pinned GitHub Actions workflow runs the eight tests, browser syntax check, and expand/backfill evidence gate. Its artifact stores the actual GitHub run provenance separately from GitLab metadata. The [first public run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) passed for commit `3ae3adf29e40edabc52256cc4587ba76557d9d0f`; GitHub CI does not establish the event's GitLab automation requirement.

Built with: Python, SQLite, HTML/CSS/JavaScript, SHA-256 evidence hashing, prepared GitLab CI configuration, and a prepared GitLab Duo custom-flow v1 configuration.

## Development challenges

The key challenge was testing coexistence rather than only SQL syntax. The breaking rename demonstrates why a migration-success check is insufficient: the new read works while the old read fails. Old-to-new and new-to-old write/insert probes make the expected compatibility direction explicit.

The tests also deliberately remove the backfill or an old-write synchronization trigger. Those changes produce concrete failed checks rather than an optimistic “compatible” summary. An unsuccessful migration causes subsequent compatibility probes to be marked as skipped, so they are not presented as executed evidence.

Another challenge was making reports reproducible without inventing CI context. Source and evidence hashes are retained alongside the exact checks; local execution does not populate a fake pipeline URL. The prepared Duo flow uses the documented custom-flow fields and keeps live validation visibly pending instead of treating YAML preparation as successful agent execution.

## Accomplishments and learning

The local workbench makes a rolling-deployment failure visible and provides a working expand/backfill comparison with executable evidence. Its CLI and prepared pipeline offer a concrete path from investigation to a reviewable gate.

The project demonstrates that compatibility needs directional reads and writes, not just a green migration statement. It also separates an executed local report, a prepared agent configuration, and verified platform automation. Those are different evidence states.

## Limits and next steps

The harness contains three fixed strategies and one work-order fixture. It does not inspect arbitrary production schemas, connect a production database, merge a change, deploy an application, or guarantee rollback after every possible production write. The compatible example models an expand phase; removing the legacy column belongs to a later release after old clients have retired.

The local build alone does not satisfy the event's mandatory GitLab Duo use. Complete contributor onboarding, publish the project to the provided GitLab environment with its MIT license, run the visible pipeline, register and enable the custom flow, and retain an actual Duo session with command outputs and exported hashes. Live tool availability and catalog validation must be checked on that environment. Public deployment is not currently claimed; no Google Cloud bonus is claimed.

## Demo outline — 2 minutes 40 seconds

The local scenes can be recorded now. The Duo scene remains a recording gate and must show real execution before the final submission video is published.

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
| Public MIT GitLab repository URL | Pending publication to the provided project. |
| Public MIT GitHub source mirror | [Vcode2407/gitlab-releasesteward](https://github.com/Vcode2407/gitlab-releasesteward), published. The required GitLab URL remains pending. |
| Runnable source and assets | Public mirror, README, and [clean-checkout judge guide](JUDGE_SETUP.md) available. |
| GitHub source verification | [Successful public run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) for `3ae3adf`; later source revisions need their own current result. |
| Visible GitLab pipeline history | Configuration prepared; actual execution/link pending. |
| GitLab Duo flow/catalog URL and session evidence | Pending onboarding, registration, runner setup, enablement, and live execution. |
| Contributor and Duo setup instructions | [Concrete onboarding, environment, goal, and evidence guide](GITLAB_SETUP.md) prepared. |
| Public YouTube video under three minutes | Pending actual platform recording and upload. |
| Actual local development walkthrough | [Silent 1:50 MP4 and execution evidence](LOCAL_DEMO.md) available; clearly discloses pending GitLab Duo and CI. |
| Source/evidence hashes and CI artifact link | Local reports supported; final verified platform artifact link pending. |
| Deployment/Google Cloud bonus URL | None claimed. |
| Original project URL for Path B | Not applicable to the proposed new Path A entry. |
| Entrant/team details, rights, eligibility and DCO | User verification pending. |
| Final Devpost URL/status | Pending; this document makes no submission. |

Deadline: **October 27, 2026, 13:00 UTC / 18:30 IST**. Review the [official rules](https://gitlab-transcend.devpost.com/rules), [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/), [custom-flow documentation](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), and [schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/) before completing the final form. Path A requires actual Duo use, a public MIT GitLab repository, visible automation history, and the English demonstration materials; prepared configurations do not establish those outcomes.
