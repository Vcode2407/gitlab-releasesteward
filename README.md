# ReleaseSteward

A new Path A entry for **Life After Code**. ReleaseSteward checks whether old and new application clients can coexist during a database migration. The local workbench executes real SQLite checks, compares a breaking rename with an expand/backfill strategy, and exports reproducible evidence.

Public MIT source: [assigned GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), with a separate [GitHub mirror](https://github.com/Vcode2407/gitlab-releasesteward). The [GitLab pipeline](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937183718) and [corrected actual Duo session 9307096](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9307096) each passed nine tests and the 9/9 compatible-fixture gate at published code commit `6897bd93c17de4eea897c4cec6ce580a2985652c`. Duo used SQLite 3.34.1. Its reviewer completed a consistent review; separate reviewer file-read traces are not exposed. The [public execution record](docs/evidence/duo-session-9307096.json) retains that qualification. The final public platform video and Devpost submission remain pending.

[Watch the actual silent local walkthrough](docs/LOCAL_DEMO.md) (1:50): real rename, expand/backfill and failed-migration results, with downloadable recording evidence. The recording preserves its status at capture; both later actual Duo sessions are retained separately. It is not the final platform video.

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

## GitLab Duo integration: corrected run verified

The [first-run record](docs/evidence/duo-session-9306854.json) preserves the actual 8/9 rollback failure, ignored report paths and older saved prompt. The [corrected-run record](docs/evidence/duo-session-9307096.json) verifies the portable table-rebuild rollback and readable reports on the same SQLite 3.34.1 runtime. Actual runner checkout and both executed prompt blocks matched the published code and saved catalog v1.2.0.

`.gitlab/duo/release-steward.yaml` keeps the inspector and read-only reviewer. The inspector generated both non-ignored reports and separately read their actual disk hashes and check IDs. The reviewer declared reading both files independently and cited matching hashes/check IDs in its final note. Only reviewer final answers are logged, so its separate `read_file` traces are unavailable. The compatible JSON display was truncated at 4096 characters; the public record is a verified summary, not a fabricated full report. Generated reports remain uncommitted. Command limits are prompt instructions, not an enforced allowlist; a human retains the rollout decision.

1. Follow the [assigned project's onboarding issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). Account registration and provisioning approval are complete; project access does not establish executed automation.
2. Inspect the verified pipeline, source commit and actual session above. Preserve the assigned project's onboarding and source histories when publishing later changes.
3. For any later authorized run, verify the saved catalog's exact configuration; source publication alone does not update the flow.
4. Record the actual platform evidence in the final silent video, publish its YouTube link and review the remaining Devpost fields.

Follow [the concrete GitLab onboarding and execution guide](docs/GITLAB_SETUP.md), including the prepared goal text and evidence checklist. References: [custom flows](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/), [custom-flow schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/), [flow registry v1](https://docs.gitlab.com/user/duo_agent_platform/flows/claude-edit-v1-flow-registry/).

## Submission checklist

Deadline: **October 27, 2026, 18:30 IST**. [Official rules](https://gitlab-transcend.devpost.com/rules).

- [x] Actual GitLab Duo session passes the compatibility gate and completes a consistent reviewer note; separate reviewer file-read traces are not exposed.
- [x] Public MIT GitLab repository with run instructions and verified pipeline history for the executed code.
- [x] Public MIT GitHub source mirror published.
- [ ] English description explaining migration compatibility, fixture limits and actual Duo behavior.
- [ ] Public YouTube demo under three minutes.
- [ ] Final Devpost fields and links verified.

Suggested 2:40 recording: introduce a mixed-client rollout (20s), execute the breaking rename (40s), show Duo investigating and rerunning the compatible strategy (60s), review hashes/CI evidence and the human release decision (40s).

Development assistance: ChatGPT/Codex coding assistance was used during implementation and debugging. The compatible strategy was prepared in source before the Duo run. Duo executed it and reviewed evidence; it did not generate a repair or perform a production rollout.
