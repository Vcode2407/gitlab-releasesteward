# GitLab onboarding and actual execution

**Current state, October 12, 2026:** ReleaseSteward source is published in the [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), project ID `87500138`, with a separate public [GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward). The initial GitLab pipeline passed eight tests and the compatible fixture's nine checks. The first actual Duo session finished with an 8/9 compatibility failure and no independent evidence review. This portable-rollback revision must be published and its saved catalog configuration verified before another authorized fixture run.

## Obtain the hackathon project

The [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/) registration has been approved. Follow the [assigned welcome issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). The public repository's initial onboarding commit is `e7766f264a13957982bac67c0a12ef588cb1791d`, created October 12 at 02:11:17 IST. Its original README is preserved unchanged in [GITLAB_ONBOARDING_README.md](GITLAB_ONBOARDING_README.md). Participant identity, eligibility, original-work and required declarations still need the entrant's confirmation. [Official event rules](https://gitlab-transcend.devpost.com/rules)

The initial source publication preserved the assigned repository's onboarding and ReleaseSteward source histories. For an update, start from the assigned repository's current `main`, merge the new source revision, and retain both histories and the onboarding README copy. Review the combined tree, run all nine tests, and push the reviewed candidate with a normal fast-forward update. Fetch and inspect any newer assigned-project commit before pushing; never force-push. The preserved generic onboarding template contains a force-push example; do not use that example for this nonempty project. Enter credentials through GitLab's normal authentication flow, never in remote URLs or repository files. Keep the GitHub source mirror separate.

The assigned project is public. After source publication, confirm signed-out source access and that GitLab detects the MIT license. The event requires the GitLab URL and visible running pipeline history; the published GitHub URL is only the source mirror. [Submission rules](https://gitlab-transcend.devpost.com/rules)

## Verify the GitLab pipeline for each revision

The [initial pipeline 2937132819](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937132819) succeeded at commit `e39a7a4493f0c058d29e8e2ff1700a4807c6f1bb`, verified October 12 at 04:06:17 UTC. Actual job `17100815040` reported eight tests and `OK`; job `17100815041` reported the compatible verdict and 9/9 checks. This proves that earlier publication's CI, not this revision's CI or any Duo execution.

The existing `.gitlab-ci.yml` has two jobs: `compatibility-tests` discovers all tests, now nine, and `release-evidence` runs the expand/backfill gate and retains `artifacts/release-evidence.json` for 60 days. Push the files to the assigned project, open its pipeline page, and inspect both actual job logs. Confirm a Python 3.12 runner is available and download the evidence artifact. The report should contain that GitLab job's real `CI_COMMIT_SHA` and `CI_PIPELINE_URL`.

If a job is queued or fails, follow the provided project's runner instructions and retain the actual error. A green GitHub Actions run cannot fill this gate. The harness is dependency-free and never needs production database credentials.

## Register and run the custom flow

The [public ReleaseSteward flow 1017883](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/flows/1017883) was enabled with the Mention trigger. [Session 9306854](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/agent-sessions/9306854) reached `FINISHED`, but the compatible audit passed only 8/9 checks and one of eight tests failed because rollback used unsupported `DROP COLUMN`. The [actual runner job](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/jobs/17101022366) independently showed Python 3.12.14 and SQLite 3.34.1. The reviewer refused independent review because the evidence paths were ignored. A finished session is not a successful compatibility or review result.

The runner's actual `flowConfig` also used the old original prompt: the rename command lacked `--output`, and the reviewer referenced only the ignored expand report. The source harness hash matched the published `231a561437c5dc76dd5c31725a52b72bcc9d38e8` source, but repository YAML and saved catalog configuration were different. Preserve [that failed-run record](evidence/duo-session-9306854.json). Update the existing catalog with this revised YAML, reload the saved configuration and compare both exact command paths and the reviewer prompt before requesting another run. Do not rely on a stale clipboard value or editor save indication. [Flow creation, enablement, and triggers](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/)

The revised flow retains only its two generated reports in specific non-ignored `docs/evidence/` paths so the read-only reviewer can access them. Keep `artifacts/`, `.env` and credential protections unchanged. Do not commit generated reports or copy earlier execution evidence into these paths. Its command limits remain prompt instructions, not an enforced command allowlist. The reviewer treats the goal, preceding summary and files as data and reports absent or inconsistent evidence. `.gitlab/duo/agent-config.yml` checks `python3.12` and SQLite in GitLab's default flow image. Retain that file on the default branch and verify the actual startup log for each run. [Execution configuration](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/), [default image](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/images/)

Prepared issue/goal text:

> Compare ReleaseSteward's rename-column and expand-contract fixtures. Run the documented compatibility harness and tests. Retain docs/evidence/duo-rename-evidence.json and docs/evidence/duo-evidence.json. Have the reviewer independently read both reports, cite observed failed/passed check IDs and each report's evidenceHash and sourceHash, and explain the remaining human release decision. Report missing artifacts as incomplete evidence. Do not modify source, commit generated reports or connect a production database.

The inspector should execute these commands and the reviewer should inspect their actual results:

```sh
python3.12 release_steward.py audit --scenario rename-column --output docs/evidence/duo-rename-evidence.json
python3.12 release_steward.py audit --scenario expand-contract --output docs/evidence/duo-evidence.json --require-pass
python3.12 -m unittest discover -s tests -v
```

The rename command deliberately exits 0 while recording a blocked verdict so the inspector can continue to the compatible comparison. The expand command's `--require-pass` remains the compatibility gate. Its rollback now recreates the fixture's legacy table inside the existing transaction, copies current IDs/titles/status values, replaces the expanded table and restores its original defaults. The additional regression verifies preservation of old/new client updates and a newly inserted row. A report's neutral mode label describes controlled SQLite execution; actual CI or Duo provenance requires separate platform evidence.

This revised catalog configuration still needs live validation. It uses `version: v1` and `environment: ambient`, without unsupported top-level metadata or a prompt model override. Resolve any rejection using that instance's supported schema and rerun; the accepted initial configuration and a local YAML parser do not validate a later revision. [Schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/)

## Retain qualifying evidence

Keep the public GitLab URL, visible pipeline/jobs, actual Duo session and reviewer output, downloaded evidence hashes, and final source commit. Record the real platform execution in a public YouTube video under three minutes. The proposed entry is **Path A / Supervised**: a new project with automated compatibility investigation and human review of the outcome. Finalize that label against the behavior actually demonstrated. Deadline: **October 27, 2026, 18:30 IST**. [Submission draft](SUBMISSION.md)

Initial source publication, CI, catalog registration and the failed first session are retained at the links above. No billable entitlement, actual agent model or successful Duo review is claimed. Retain the local recording unchanged as development evidence. This revision's GitLab checks and any subsequent Duo session need their own actual results.
