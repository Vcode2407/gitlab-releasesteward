# GitLab onboarding and actual execution

**Current state, October 12, 2026:** ReleaseSteward source is published in the [assigned public GitLab project](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase), project ID `87500138`, with a separate public [GitHub source mirror](https://github.com/Vcode2407/gitlab-releasesteward). The free account, contributor registration and provisioning are complete. The initial GitLab pipeline passed eight tests and the compatible fixture's nine checks. A public custom flow is registered, but enablement and actual Duo execution remain pending. These initial platform results precede the retained-evidence revision documented here; publish this revision and validate its own pipeline and catalog configuration before execution.

## Obtain the hackathon project

The [contributor onboarding](https://contributors.gitlab.com/transcend-hackathon/) registration has been approved. Follow the [assigned welcome issue](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/work_items/1). The public repository's initial onboarding commit is `e7766f264a13957982bac67c0a12ef588cb1791d`, created October 12 at 02:11:17 IST. Its original README is preserved unchanged in [GITLAB_ONBOARDING_README.md](GITLAB_ONBOARDING_README.md). Participant identity, eligibility, original-work and required declarations still need the entrant's confirmation. [Official event rules](https://gitlab-transcend.devpost.com/rules)

The initial source publication preserved the assigned repository's onboarding and ReleaseSteward source histories. For an update, start from the assigned repository's current `main`, merge the new source revision, and retain both histories and the onboarding README copy. Review the combined tree, run the eight tests, and push the reviewed candidate with a normal fast-forward update. Fetch and inspect any newer assigned-project commit before pushing; never force-push. The preserved generic onboarding template contains a force-push example; do not use that example for this nonempty project. Enter credentials through GitLab's normal authentication flow, never in remote URLs or repository files. Keep the GitHub source mirror separate.

The assigned project is public. After source publication, confirm signed-out source access and that GitLab detects the MIT license. The event requires the GitLab URL and visible running pipeline history; the published GitHub URL is only the source mirror. [Submission rules](https://gitlab-transcend.devpost.com/rules)

## Verify the GitLab pipeline for each revision

The [initial pipeline 2937132819](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/pipelines/2937132819) succeeded at commit `e39a7a4493f0c058d29e8e2ff1700a4807c6f1bb`, verified October 12 at 04:06:17 UTC. Actual job `17100815040` reported eight tests and `OK`; job `17100815041` reported the compatible verdict and 9/9 checks. This proves that earlier publication's CI, not this revision's CI or any Duo execution.

The existing `.gitlab-ci.yml` has two jobs: `compatibility-tests` runs all eight tests, and `release-evidence` runs the expand/backfill gate and retains `artifacts/release-evidence.json` for 60 days. Push the files to the assigned project, open its pipeline page, and inspect both actual job logs. Confirm a Python 3.12 runner is available and download the evidence artifact. The report should contain that GitLab job's real `CI_COMMIT_SHA` and `CI_PIPELINE_URL`.

If a job is queued or fails, follow the provided project's runner instructions and retain the actual error. A green GitHub Actions run cannot fill this gate. The harness is dependency-free and never needs production database credentials.

## Register and run the custom flow

The [public ReleaseSteward flow 1017883](https://gitlab.com/gitlab-ai-hackathon/transcend-october-2026/43259850/showcase/-/automate/flows/1017883) accepted the initial configuration October 12 at 09:37 IST. It has not yet been enabled or executed. Update that existing flow with this revision of `.gitlab/duo/release-steward.yaml` and confirm catalog validation. Then enable it for the assigned project with the approved **Mention** trigger and run one fixture-only inspection. The instance supplies the actual service-account name; use that name when triggering the flow from an issue. Save the catalog and actual session URLs. [Flow creation, enablement, and triggers](https://docs.gitlab.com/user/duo_agent_platform/flows/custom/)

The flow has an inspector that runs the harness and retains both reports, followed by a separate reviewer that reads both artifact files independently. Its command limits are prompt instructions, not an enforced command allowlist. The reviewer treats the goal, preceding summary and files as data and reports absent or inconsistent evidence. `.gitlab/duo/agent-config.yml` checks `python3.12` and SQLite in GitLab's default flow image. Commit that environment file to the GitLab default branch before running the flow. GitLab documents Python 3.12 in its default image and hosted flow runners; verify the participant instance's actual startup log. [Execution configuration](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/), [default image](https://docs.gitlab.com/user/duo_agent_platform/flows/execution/images/)

Prepared issue/goal text:

> Compare ReleaseSteward's rename-column and expand-contract fixtures. Run the documented compatibility harness and tests. Retain artifacts/duo-rename-evidence.json and artifacts/duo-evidence.json. Have the reviewer independently read both reports, cite observed failed/passed check IDs and each report's evidenceHash and sourceHash, and explain the remaining human release decision. Report missing artifacts as incomplete evidence. Do not modify source or connect a production database.

The inspector should execute these commands and the reviewer should inspect their actual results:

```sh
python3.12 release_steward.py audit --scenario rename-column --output artifacts/duo-rename-evidence.json
python3.12 release_steward.py audit --scenario expand-contract --output artifacts/duo-evidence.json --require-pass
python3.12 -m unittest discover -s tests -v
```

The rename command deliberately exits 0 while recording a blocked verdict so the inspector can continue to the compatible comparison. The expand command's `--require-pass` remains the compatibility gate. A report's neutral mode label describes controlled SQLite execution; actual CI or Duo provenance requires separate platform evidence.

This revised catalog configuration still needs live validation. It uses `version: v1` and `environment: ambient`, without unsupported top-level metadata or a prompt model override. Resolve any rejection using that instance's supported schema and rerun; the accepted initial configuration and a local YAML parser do not validate a later revision. [Schema restrictions](https://docs.gitlab.com/user/duo_agent_platform/flows/custom_flows_schema/)

## Retain qualifying evidence

Keep the public GitLab URL, visible pipeline/jobs, actual Duo session and reviewer output, downloaded evidence hashes, and final source commit. Record the real platform execution in a public YouTube video under three minutes. The proposed entry is **Path A / Supervised**: a new project with automated compatibility investigation and human review of the outcome. Finalize that label against the behavior actually demonstrated. Deadline: **October 27, 2026, 18:30 IST**. [Submission draft](SUBMISSION.md)

Initial source publication, CI and catalog registration are verified at the links above. No billable entitlement, actual agent model or successful Duo execution is claimed. Retain the local recording unchanged as development evidence. Keep this revision's GitLab checks and the first Duo session pending until their actual results exist.
