# Actual local development walkthrough

[Watch the narrated video](media/releasesteward-local-development.mp4) — **1 minute 50 seconds**, recorded October 10, 2026 from source commit `3ae3adf29e40edabc52256cc4587ba76557d9d0f`.

This is an actual isolated browser recording of ReleaseSteward executing its controlled SQLite fixtures. A permanent banner and the narration disclose that **GitLab Duo and GitLab CI execution remain pending**. It is development evidence; the final event video still needs real platform execution and a public YouTube link.

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

[Recording evidence](media/releasesteward-recording-evidence.json) contains the actual HTTP responses, observed check totals, narration timing, source revision and SHA-256 of the final MP4. [The downloaded report](media/releasesteward-exported-expand-evidence.json) is the export captured during the recording; it was checked against the observed compatible response. GitLab metadata remains empty. No browser errors were observed.

The screen recording was encoded with a permanent status banner and Windows English speech timed to the observed actions. No external voice, music, stock footage or simulated platform output is included. The video and fixture evidence are authored project assets covered by the repository's MIT license.

To reproduce the actions, follow [the judge setup guide](JUDGE_SETUP.md). To complete the required platform demonstration, follow [the GitLab onboarding guide](GITLAB_SETUP.md) and the final outline in [the submission draft](SUBMISSION.md).
