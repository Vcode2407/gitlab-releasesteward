# GitLab onboarding and actual execution

**Current state, October 12, 2026:** Public [GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward) and working local SQLite harness. The free `vkslog69` GitLab account and contributor registration are complete. Provisioning approval provides the [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), project ID `87500138`, with Developer and AI access. ReleaseSteward source publication, GitLab CI, catalog validation, and Duo execution remain pending. Account access or a prepared YAML file is not evidence of Duo use.

## Obtain the hackathon project

The [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/) registration has been approved. Follow the [assigned welcome issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). The public repository's initial onboarding commit is `e7766f264a13957982bac67c0a12ef588cb1791d`, created October 12 at 02:11:17 IST. Its original README is preserved unchanged in [GITLAB_ONBOARDING_README.md](GITLAB_ONBOARDING_README.md). Participant identity, eligibility, original-work and required declarations still need the entrant's confirmation. [Official event rules](https://gitlab-transcend.devpost.com/rules)

Prepare publication from the assigned repository's `main` branch, then merge the published ReleaseSteward source history as an additional parent. Keep both histories and the onboarding README copy. Review the combined tree, run the eight tests, and push the reviewed candidate with a normal fast-forward update. Fetch and inspect any newer assigned-project commit before pushing; never force-push. The preserved generic onboarding template contains a force-push example; do not use that example for this nonempty project. Enter credentials through GitLab's normal authentication flow, never in remote URLs or repository files. Keep the GitHub source mirror separate.

The assigned project is public. After source publication, confirm signed-out source access and that GitLab detects the MIT license. The event requires the GitLab URL and visible running pipeline history; the published GitHub URL is only the source mirror. [Submission rules](https://gitlab-transcend.devpost.com/rules)

## Run the prepared GitLab pipeline

The existing `.gitlab-ci.yml` has two jobs: `compatibility-tests` runs all eight tests, and `release-evidence` runs the expand/backfill gate and retains `artifacts/release-evidence.json` for 60 days. Push the files to the assigned project, open its pipeline page, and inspect both actual job logs. Confirm a Python 3.12 runner is available and download the evidence artifact. The report should contain that GitLab job's real `CI_COMMIT_SHA` and `CI_PIPELINE_URL`.

If a job is queued or fails, follow the provided project's runner instructions and retain the actual error. A green GitHub Actions run cannot fill this gate. The harness is dependency-free and never needs production database credentials.

## Register and run the custom flow

With the assigned project's required permissions and Duo access, open **AI > Flows**, create **ReleaseSteward**, and paste `.gitlab/duo/release-steward.yaml` as its configuration. Enable it for the assigned project and select an available trigger. The instance supplies the actual service-account name; use that name when triggering the flow from an issue. Save the catalog and session URLs. [Flow creation, enablement, and triggers](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/)

The flow has an inspector that runs the harness and a separate reviewer that reads its evidence. `.gitlab/duo/agent-config.yml` checks `python3.12` and SQLite in GitLab's default flow image. Commit that environment file to the GitLab default branch before running the flow. GitLab documents Python 3.12 in its default image and hosted flow runners; verify the participant instance's actual startup log. [Execution configuration](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/), [default image](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/images/)

Prepared issue/goal text:

> Compare ReleaseSteward's rename-column and expand-contract fixtures. Run the documented compatibility harness and tests. Retain artifacts/duo-evidence.json, cite observed failed/passed check IDs and both hashes, and explain the remaining human release decision. Do not modify source or connect a production database.

The inspector should execute these commands and the reviewer should inspect their actual results:

```sh
python3.12 release_steward.py audit --scenario rename-column
python3.12 release_steward.py audit --scenario expand-contract --output artifacts/duo-evidence.json --require-pass
python3.12 -m unittest discover -s tests -v
```

Catalog validation remains a live gate. The prepared file uses `version: v1` and `environment: ambient`, without unsupported top-level metadata or a prompt model override. Resolve any rejection using that instance's supported schema and rerun; a local YAML parser cannot establish successful catalog registration. [Schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/)

## Retain qualifying evidence

Keep the public GitLab URL, visible pipeline/jobs, actual Duo session and reviewer output, downloaded evidence hashes, and final source commit. Record the real platform execution in a public YouTube video under three minutes. The proposed entry is **Path A / Supervised**: a new project with automated compatibility investigation and human review of the outcome. Finalize that label against the behavior actually demonstrated. Deadline: **October 27, 2026, 18:30 IST**. [Submission draft](SUBMISSION.md)

Provisioned project access is verified; no billable entitlement, actual agent model, GitLab pipeline or successful Duo execution is claimed. Until the actual execution evidence links exist, retain the local recording as development evidence and keep those platform gates marked pending.
