# GitLab onboarding and actual execution

**Current state:** Public [GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward) and working local SQLite harness. Contributor provisioning, a public GitLab project, GitLab CI, catalog validation, and Duo execution are pending. A mirror or a prepared YAML file is not evidence of Duo use.

## Obtain the hackathon project

Open [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/) and complete the account sign-in and requested registration yourself. The published event process provides a group/subgroup, project, and welcome issue after approval; its estimate is about 24 business hours. Keep the assigned project URL and follow that welcome issue. Participant identity, eligibility, and required declarations need the entrant's confirmation. No account has been created or onboarding submitted by this implementation. [Official event rules](https://gitlab-transcend.devpost.com/rules)

Import this new project's source into the assigned GitLab project. The GitHub mirror is public, so its clone URL can be used when the provided environment supports repository import. If the assigned project already contains onboarding commits, inspect those first and preserve them; do not force-push over its history. For an empty assigned repository, add its exact HTTPS URL as a separate remote and push the local `main` branch. Keep GitHub as the mirror remote. Enter credentials through GitLab's normal authentication flow, never in remote URLs or repository files.

Make the final source repository public and confirm that GitLab detects the MIT license. The event requires the GitLab URL and visible running pipeline history; the published GitHub URL is only the source mirror. [Submission rules](https://gitlab-transcend.devpost.com/rules)

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

No GitLab access, billable entitlement, actual agent model, or successful remote execution is assumed. Until these evidence links exist, retain the local recording as development evidence and keep the platform gates marked pending.
