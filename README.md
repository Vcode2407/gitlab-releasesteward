# ReleaseSteward

A new Path A entry for **Life After Code**. ReleaseSteward checks whether old and new application clients can coexist during a database migration. The local workbench executes real SQLite checks, compares a breaking rename with an expand/backfill strategy, and exports reproducible evidence.

## Run and verify

Use Python 3.12. There are no external runtime dependencies.

```powershell
python release_steward.py serve
python -m unittest discover -s tests -v
python release_steward.py audit --scenario expand-contract --require-pass
```

Open http://127.0.0.1:4184. Start with **Rename status in one release**. The migration applies, but old clients fail. Choose **Try the compatible strategy**; both clients can read, write, and insert. Backfill, default-value, and rollback checks execute in a fresh in-memory database. Export the report, inspect the exact SQL and hashes, and retain it with the CI pipeline.

The harness contains three controlled strategies and a work-order application fixture. It does not accept arbitrary SQL or certify production migrations. The compatible fixture models an expand phase; removing the legacy column is a later release after old clients retire.

## GitLab Duo integration: prepared, not verified

GitLab Duo execution is mandatory for the event. The local harness alone is **not submission-ready**. `.gitlab/duo/release-steward.yaml` defines an inspector and independent evidence reviewer using the current custom-flow v1 schema. It has been prepared against documentation; GitLab's catalog and actual tools still need live validation. `.gitlab-ci.yml` runs tests and exports evidence with real `CI_COMMIT_SHA` and `CI_PIPELINE_URL` metadata when executed in GitLab. Local reports leave those fields empty.

1. Complete [hackathon contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/). Provisioning can take about 24 business hours.
2. Put this new project in the provided GitLab project, retain the MIT license and run the pipeline.
3. Register the flow in the AI Catalog, configure its runner, enable it for the project, and ask it to inspect the rename versus expand strategy.
4. Verify actual command output and exported hashes; record the Duo session and visible pipeline history. If catalog validation rejects a field, fix it using the live instance's docs rather than claiming an executed flow.

References: [custom flows](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), [custom-flow schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/), [flow registry v1](https://docs.gitlab.com/user/duo_agent_platform/flows/claude-edit-v1-flow-registry/).

## Submission checklist

Deadline: **October 27, 2026, 18:30 IST**. [Official rules](https://gitlab-transcend.devpost.com/rules).

- [ ] Live GitLab Duo session executes the workflow.
- [ ] Public MIT GitLab repository with run instructions and visible pipeline history.
- [ ] English description explaining migration compatibility, fixture limits and actual Duo behavior.
- [ ] Public YouTube demo under three minutes.
- [ ] Final Devpost fields and links verified.

Suggested 2:40 recording: introduce a mixed-client rollout (20s), execute the breaking rename (40s), show Duo investigating and rerunning the compatible strategy (60s), review hashes/CI evidence and the human release decision (40s).
