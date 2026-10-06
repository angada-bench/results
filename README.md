# Angada on Martian Code Review Bench (offline), self-run

Self-run of [withmartian/code-review-benchmark](https://github.com/withmartian/code-review-benchmark) (commit `e616e84`) offline mode against the production Angada GitHub App. Not an official Martian leaderboard entry.

## Status: run in progress

Updated 2026-10-06T06:07Z. The 50 benchmark PRs are recreated as public PRs in [angada-bench](https://github.com/angada-bench) and reviewed by the production bot.

| Reviews published | Failed or partial (to retry) | In flight |
|---|---|---|
| 34 | 8 | 0 |

Scoring (Claude Opus 4.5 judge, core profile, F2) runs only after every PR has a final review. Results then land in `latest.json` and `runs/<run_id>/` with raw comments, judge outputs and the dashboard.

## Layout

- `latest.json`: scoreboard of the latest run (placeholder until scored).
- `runs/<run_id>/`: manifest, raw bot comments, judge outputs, merged results, dashboard, review costs, Martian snapshot.
- `scripts/`: replay, scoring, merge and publish scripts.
