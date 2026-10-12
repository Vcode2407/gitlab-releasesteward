# ReleaseSteward

A new Path A entry for **Life After Code**. ReleaseSteward checks whether old and new application clients can coexist during a database migration. The local workbench executes real SQLite checks, compares a breaking rename with an expand/backfill strategy, and exports reproducible evidence.

Public MIT source mirror: [Vcode2407/gitlab-releasesteward](https://github.com/Vcode2407/gitlab-releasesteward). ReleaseSteward is also published in the [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase). Its [initial GitLab pipeline](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937132819) passed eight tests and the 9/9 compatible-fixture gate at commit `e39a7a4493f0c058d29e8e2ff1700a4807c6f1bb`. The [public Duo catalog flow](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/flows/1017883) was accepted October 12, 2026. Those initial results precede this retained-evidence revision; its GitLab publication, pipeline and catalog validation remain pending. Project enablement and actual Duo execution remain pending.

[Watch the actual silent local walkthrough](docs/LOCAL_DEMO.md) (1:50): real rename, expand/backfill and failed-migration results, with downloadable recording evidence. Actual Duo execution remains pending; the recording preserves its status at capture.

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

The [GitHub workflow](.github/workflows/verify.yml) pins its four actions to reviewed commit hashes. It runs the existing eight tests, checks browser JavaScript with Node 22, and executes the expand/backfill scenario with a required compatible verdict. Its artifact contains the executed report and a separate GitHub run record. The report's GitLab `commit` and `pipeline` fields remain empty on GitHub; the companion file records the actual GitHub commit and run URL.

The [first public verification run](https://github.com/Vcode2407/gitlab-releasesteward/actions/runs/38074137450) passed for commit `3ae3adf29e40edabc52256cc4587ba76557d9d0f`. Check [later Actions runs](https://github.com/Vcode2407/gitlab-releasesteward/actions/workflows/verify.yml) when reviewing another revision. GitHub execution is source-validation evidence and does not establish GitLab CI or Duo execution.

## GitLab Duo integration: registered, execution pending

GitLab Duo execution is mandatory for the event. The local harness alone is **not submission-ready**. `.gitlab/duo/release-steward.yaml` defines an inspector and independent evidence reviewer using the current custom-flow v1 schema. The inspector retains `artifacts/duo-rename-evidence.json` and `artifacts/duo-evidence.json`; the reviewer reads both independently, compares check IDs and hashes, and reports missing evidence. These command limits are prompt instructions, not an enforced command allowlist. The revised configuration and actual tools need live validation before the first run. `.gitlab/duo/agent-config.yml` checks Python 3.12 and SQLite in the default flow image before the inspector starts. `.gitlab-ci.yml` runs tests and exports evidence with real `CI_COMMIT_SHA` and `CI_PIPELINE_URL` metadata when executed in GitLab. Local reports leave those fields empty; report labels alone do not establish platform execution.

1. Follow the [assigned project's onboarding issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). Account registration and provisioning approval are complete; project access does not establish executed automation.
2. Merge this revision into the assigned project while preserving its onboarding and source history; run and inspect a new pipeline for that exact commit.
3. Update the existing catalog flow with the revised YAML, validate it, enable its Mention trigger for the project, and ask it to inspect only the rename versus expand fixtures.
4. Verify actual command output and exported hashes; record the Duo session and visible pipeline history. If catalog validation rejects a field, fix it using the live instance's docs rather than claiming an executed flow.

Follow [the concrete GitLab onboarding and execution guide](docs/GITLAB_SETUP.md), including the prepared goal text and evidence checklist. References: [custom flows](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), [custom-flow schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/), [flow registry v1](https://docs.gitlab.com/user/duo_agent_platform/flows/claude-edit-v1-flow-registry/).

## Submission checklist

Deadline: **October 27, 2026, 18:30 IST**. [Official rules](https://gitlab-transcend.devpost.com/rules).

- [ ] Live GitLab Duo session executes the workflow.
- [x] Public MIT GitLab repository with run instructions and initial visible pipeline history; this revision still needs its own publication and run.
- [x] Public MIT GitHub source mirror published.
- [ ] English description explaining migration compatibility, fixture limits and actual Duo behavior.
- [ ] Public YouTube demo under three minutes.
- [ ] Final Devpost fields and links verified.

Suggested 2:40 recording: introduce a mixed-client rollout (20s), execute the breaking rename (40s), show Duo investigating and rerunning the compatible strategy (60s), review hashes/CI evidence and the human release decision (40s).
