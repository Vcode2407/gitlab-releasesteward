# ReleaseSteward — Devpost submission draft

English draft prepared October 10, 2026; platform status updated October 12. This is preparation material, not a submitted entry. The [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase) detects MIT and retains verified code `6897bd93c17de4eea897c4cec6ce580a2985652c`. Its [pipeline](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937183718) passed nine tests and the compatible 9/9 gate. [Corrected actual Duo session 9307096](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9307096) also passed all nine tests and nine compatible checks on SQLite 3.34.1 and completed a consistent reviewer note. Separate reviewer file-read traces are unavailable. [The revised silent 2:44 demo is published on YouTube](https://www.youtube.com/watch?v=xGsDpR_3hEg), with English captions and [media/provenance](FINAL_DEMO.md). Final Devpost submission remains pending.

## Project name and tagline

**ReleaseSteward**

**Prove old and new clients can share a database before a rollout.**

Proposed category: **Path A — Start Fresh**. Intended autonomy level: **Supervised** for the demonstrated compatibility investigation and evidence review, with a human retaining the actual release decision. Review the category against the actual workflow before final submission.

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

The GitLab CI test and evidence jobs succeeded for the corrected code, and its downloaded report records 9/9 compatible checks. The public Duo catalog v1.2.0 and actual runner prompts matched the corrected source. Its inspector generated both non-ignored reports and verified their hashes/check IDs from disk. The separate read-only reviewer declared reading both independently and produced a consistent final note. Only that reviewer's final answer is logged, so separate `read_file` traces are unavailable. The compatible JSON display was truncated at 4096 characters; no complete report is fabricated. Both runtime setup and actual nine-test output were verified on Python 3.12.14/SQLite 3.34.1. Command limits remain prompt instructions, not an enforced allowlist.

A separate pinned GitHub Actions workflow discovers all nine tests, checks browser syntax and executes the expand/backfill evidence gate. Its artifact stores the actual GitHub run provenance separately from GitLab metadata. The docs-only publication `b5e66ed26cabbcedb4a39c77cf507fe222524707` passed [GitHub CI 38213648693](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38213648693); its matching GitLab tree at `744274d338addf069d0e06634789e9bcef22eb35` passed [pipeline 2937434867](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937434867). That is the running pipeline shown in the revised video. Any later revision needs its own CI result. The [first public run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) for `3ae3adf29e40edabc52256cc4587ba76557d9d0f` remains historical evidence; GitHub CI does not establish the event's GitLab automation requirement.

Built with: Python, SQLite, HTML/CSS/JavaScript, SHA-256 evidence hashing, GitLab CI, and actual GitLab Duo custom-flow v1 execution. ChatGPT/Codex coding assistance was used during implementation and debugging. The compatible strategy was prepared in source before the run; Duo executed it and reviewed evidence rather than generating a repair.

## Development challenges

The key challenge was testing coexistence rather than only SQL syntax. The breaking rename demonstrates why a migration-success check is insufficient: the new read works while the old read fails. Old-to-new and new-to-old write/insert probes make the expected compatibility direction explicit.

The tests also deliberately remove the backfill or an old-write synchronization trigger. Those changes produce concrete failed checks rather than an optimistic “compatible” summary. An unsuccessful migration causes subsequent compatibility probes to be marked as skipped, so they are not presented as executed evidence.

Another challenge was making reports reproducible without inventing CI context. The [first actual Duo run](evidence/duo-session-9306854.json) exposed SQLite 3.34.1's rejection of `DROP COLUMN`, inaccessible ignored reports and an older saved prompt. The correction rebuilt the legacy table, retained readable reports and verified the exact saved prompts. The [second actual run](evidence/duo-session-9307096.json) passed on that same older SQLite version. Both outcomes are retained, alongside the limits of the available reviewer traces and JSON display.

## Accomplishments and learning

The workbench makes a rolling-deployment failure visible, and actual GitLab CI and Duo execution now verify the authored compatible strategy. The first run exposed concrete failures; the corrected run passed nine checks and nine tests and produced a consistent review with retained source/evidence hashes. A passing controlled fixture remains evidence for a human decision, not production rollout approval.

The project demonstrates that compatibility needs directional reads and writes, not just a green migration statement. It also separates an executed local report, a prepared agent configuration, and verified platform automation. Those are different evidence states.

## Limits and next steps

The harness contains three fixed strategies and one work-order fixture. It does not inspect arbitrary production schemas, connect a production database, merge a change, deploy an application, or guarantee rollback after every possible production write. The compatible example models an expand phase; removing the legacy column belongs to a later release after old clients have retired.

Both actual Duo sessions, exact executed code, saved prompts and CI evidence are retained. The published final silent edit shows actual platform captures and the human release decision. Review the remaining Devpost fields and participant declarations before final submission. Public deployment is not currently claimed; no Google Cloud bonus is claimed.

## Published silent demo — 2 minutes 44 seconds

[Watch the revised public YouTube video](https://www.youtube.com/watch?v=xGsDpR_3hEg). The edit uses actual October 10 local footage and October 12 GitLab captures, with English captions and no audio. Timestamped observations show docs-only CI changing from Running to Passed; a later completed test job is an explicit hard cut. The completed Duo inspection is browsed as archived-session replay, not a new execution. Historical footage, the failed first run and other held captures retain their labels. Eleven unchanged segments are hash-identical to the earlier edit. All 14 scene midpoints and nine event frames were visually reviewed, and full decoding verified exactly 164 seconds and 4,100 frames at 25 fps with zero audio. These are sampled-frame checks plus full decoding, with no continuous normal-speed review claim. [Video, captions and provenance](FINAL_DEMO.md) are retained separately from the original local recording and earlier edit.

| Time | Action and evidence |
| --- | --- |
| 0:00–0:36 | Dated local footage: problem, breaking rename at 3/9, supplied compatible fixture at 9/9, executed SQL and evidence. |
| 0:36–0:52 | Actual assigned public source and historical first Duo failure at 8/9 on SQLite 3.34.1. |
| 0:52–1:04 | Timestamped observations of docs-only pipeline 2937434867 changing from Running to Passed at commit 744274d; migration harness unchanged. |
| 1:04–1:12 | Explicit hard cut to later completed test job 17102697264 showing nine tests and OK. |
| 1:12–1:36 | Saved public catalog v1.2.0 and actual second-run request; command restrictions remain prompt instructions. |
| 1:36–1:54 | Actual browsing opens completed session 9307096 audit/test output; nine compatible checks and nine tests, with no new Duo execution. |
| 1:54–2:12 | Held actual reviewer evidence with a consistent note; separate file-read traces are not exposed. |
| 2:12–2:28 | Actual Duo check IDs, common source hash and two evidence hashes; session report CI metadata is empty. |
| 2:28–2:44 | Controlled-fixture limits and the remaining human rollout decision; no production deployment. |

If live Duo or CI access is unavailable, retain a local walkthrough clearly labelled as development evidence. It is not a replacement for the required platform demonstration.

## Fields and links to complete before submitting

| Devpost material | Current value/status |
| --- | --- |
| Project title | ReleaseSteward |
| Tagline and English description | Saved and verified in the canonical Devpost draft, alongside the current public source, video and tags. |
| Path | Path A — new project. |
| Autonomy level | Supervised, saved in the draft; a human retains the rollout decision. |
| Public MIT GitLab repository URL | [Assigned public project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), project ID 87500138; public source and detected MIT verified at `6897bd93c17de4eea897c4cec6ce580a2985652c`. |
| Public MIT GitHub source mirror | [Vcode2407/gitlab-releasesteward](https://github.com/Vcode2407/gitlab-releasesteward), published separately from the assigned GitLab source. |
| Runnable source and assets | Public mirror, README, and [clean-checkout judge guide](JUDGE_SETUP.md) available. |
| GitHub source verification | [Successful CI 38213648693](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38213648693) for docs-only publication `b5e66ed26cabbcedb4a39c77cf507fe222524707`: nine tests, browser syntax and expand/backfill evidence gate passed. Any later revision needs its own result. |
| Visible GitLab pipeline history | [Corrected-code pipeline 2937183718](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937183718) and captured docs-only [pipeline 2937434867](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937434867) at `744274d338addf069d0e06634789e9bcef22eb35` succeeded; actual nine-test traces and compatible 9/9 artifacts verified. Any later revision needs its own result. |
| GitLab Duo flow/catalog URL and session evidence | [Public catalog flow 1017883](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/flows/1017883), verified v1.2.0; [actual session 9307096](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9307096) passed nine tests and 9/9 checks, with consistent review and unavailable separate reviewer read traces. First failed session retained separately. |
| Contributor and Duo setup instructions | [Concrete onboarding, environment, goal, and evidence guide](GITLAB_SETUP.md) prepared. |
| Public YouTube video under three minutes | [Revised public silent 2:44 video](https://www.youtube.com/watch?v=xGsDpR_3hEg), with Published English manual subtitles; 14 scene midpoints, nine event frames and full decoding checked, with zero audio. |
| Actual local development walkthrough | [Silent 1:50 MP4 and execution evidence](LOCAL_DEMO.md) available; retains the October 10 pending platform banner. Corrected actual CI and Duo are verified separately. |
| Source/evidence hashes and CI artifact link | [Actual CI artifact](https://gitlab.com/api/v4/projects/87500138/jobs/17101112724/artifacts/artifacts/release-evidence.json) and [qualified actual Duo record](evidence/duo-session-9307096.json) verified; complete generated Duo JSON was not retrieved. |
| Deployment/Google Cloud bonus URL | None claimed. |
| Original project URL for Path B | Not applicable to the proposed new Path A entry. |
| Entrant eligibility | User confirmed legal age of majority and India residence; no relevant GitLab/Devpost/promotion-entity employee, representative or agent affiliation; no immediate-family/household affiliation; and no judge or judge-employer affiliation. |
| Official Rules, rights and DCO | Final Official Rules and DCO acceptance remain pending; no acceptance is claimed by this document. |
| Final Devpost URL/status | Canonical draft saved at 4/5 steps; current story, source, video and tags verified. Final submission remains pending. |

Deadline: **October 27, 2026, 13:00 UTC / 18:30 IST**. Review the [official rules](https://gitlab-transcend.devpost.com/rules), [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/), [custom-flow documentation](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), and [schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/) before completing the final form. Path A requires actual Duo use, a public MIT GitLab repository, visible automation history, and the English demonstration materials; prepared configurations do not establish those outcomes.
