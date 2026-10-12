# Actual local development walkthrough

The [silent-video verification](media/silent-video-verification.json) records zero audio streams, the current file hash, a complete decode, and an unchanged encoded video stream.

[Watch the silent video](media/releasesteward-local-development.mp4) — **1 minute 50 seconds**, recorded October 10, 2026 from source commit `3ae3adf29e40edabc52256cc4587ba76557d9d0f`.

This is an actual isolated browser recording of ReleaseSteward executing its controlled SQLite fixtures. The audio track has been removed; the English application text and permanent banner remain unchanged. Its pending GitLab Duo/CI banner records the **October 10 capture state**. Later [verified CI and actual Duo session 9307096](GITLAB_SETUP.md) passed nine tests and 9/9 compatible checks. [The published final 2:44 demo](https://www.youtube.com/watch?v=WwfkawIuRuE) dates this historical footage and then shows labelled held captures of actual platform results. The table below describes the original local footage.

| Approximate time | Observed action |
| --- | --- |
| 0:00 | Introduce the working local workbench and its platform limits. |
| 0:16 | Run the one-release rename: migration applies, but only 3 of 9 checks pass. |
| 0:31 | Execute the authored expand/backfill strategy: 9 of 9 checks pass. |
| 0:47 | Inspect actual migration statements, schema and reproducible hashes. |
| 1:01 | Download the actual compatible JSON report. |
| 1:10 | Run the required-column strategy: migration fails, 0 of 9 pass and subsequent probes are skipped. |
| 1:23 | State fixture limits, pending platform work and the human release decision. |

The compatible strategy is supplied project code, not a model-generated repair. Every audit uses a fresh in-memory database. The recording does not show a production database, a deployment, or a live agent session.

[Recording evidence](media/releasesteward-recording-evidence.json) contains the actual HTTP responses, observed check totals and source revision. [The downloaded report](media/releasesteward-exported-expand-evidence.json) is the export captured during the recording; it was checked against the observed compatible response. GitLab metadata remains empty. No browser errors were observed.

The current screen recording contains no audio track. The permanent development-status banner and actual recorded actions are retained. No stock footage or simulated platform output is included. The video and fixture evidence are authored project assets covered by the repository's MIT license.

To reproduce the actions, follow [the judge setup guide](JUDGE_SETUP.md). Review the separate current platform evidence in [the GitLab setup guide](GITLAB_SETUP.md), the [final demo and provenance](FINAL_DEMO.md), and its timeline in [the submission draft](SUBMISSION.md).
