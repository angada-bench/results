# Angada on Martian Code Review Bench (offline), self-run

Self-run results for Angada on [withmartian/code-review-benchmark](https://github.com/withmartian/code-review-benchmark) (commit `e616e84`), offline mode. This is not an official Martian leaderboard entry: Martian runs the tools on its board itself.

## Latest: campaign 2026-11-20 baseline

Angada with the verifier on scored a mean F2 of **50.5** over 4 full runs of the 50 benchmark PRs (sd 3.0, range 47.7 to 54.4). The pooled 95% interval is 45.2 to 55.8 (bootstrap over PRs). Mean counts per run: 93 TP, 195 FP, 65 FN of 158 core goldens; precision 32.3, recall 58.9.

Placed into Martian's board (core profile, Claude Opus 4.5 judge), that mean sits **12th of 21 rows** (Martian's 20 rows plus ours). The board rows are single runs that Martian made itself. Our row is a mean of four runs we made ourselves. This is not an official Martian leaderboard entry.

Two runs of the identical configuration differed by 6.7 F2 (47.7 and 54.4). For that reason we report the mean of four and do not quote any single run as the score.

Every full run of the benchmarked configuration in this campaign is published, low ones included. A single comparison run of an older configuration, made the same day, is not included.

Full report: [campaigns/2026-11-20-baseline/REPORT.md](campaigns/2026-11-20-baseline/REPORT.md).

### Runs

| Run | Verifier | PRs | TP | FP | FN | Precision | Recall | F1 | F2 | Reviews not completed |
|---|---|---|---|---|---|---|---|---|---|---|
| on-g1 | on | 50 | 96 | 205 | 62 | 31.9 | 60.8 | 41.8 | 51.4 | 2 |
| on-g2 | on | 50 | 87 | 193 | 71 | 31.1 | 55.1 | 39.7 | 47.7 | 5 |
| on-g3 | on | 50 | 100 | 187 | 58 | 34.8 | 63.3 | 44.9 | 54.4 | 3 |
| on-g4 | on | 50 | 89 | 195 | 69 | 31.3 | 56.3 | 40.3 | 48.6 | 3 |
| off-g1 | off | 50 | 101 | 311 | 57 | 24.5 | 63.9 | 35.4 | 48.4 | 2 |
| off-g2 | off | 50 | 93 | 284 | 65 | 24.7 | 58.9 | 34.8 | 46.1 | 5 |
| off-g3 | off | 50 | 101 | 286 | 57 | 26.1 | 63.9 | 37.1 | 49.6 | 3 |
| off-g4 | off | 50 | 102 | 281 | 56 | 26.6 | 64.6 | 37.7 | 50.2 | 3 |

### Arms

| Verifier | Runs | F2 mean | F2 sd | F2 range | Precision mean | Recall mean | TP / FP / FN mean | Pooled F2 | Pooled F2 95% interval |
|---|---|---|---|---|---|---|---|---|---|
| on | 4 | 50.5 | 3.0 | 47.7 to 54.4 | 32.3 | 58.9 | 93 / 195 / 65 | 50.5 | 45.2 to 55.8 |
| off | 4 | 48.6 | 1.8 | 46.1 to 50.2 | 25.5 | 62.8 | 99.25 / 290.5 / 58.75 | 48.6 | 43.6 to 53.4 |

### Verifier on minus verifier off

Pooled delta F2 +2.0, paired 95% interval -0.1 to +3.9, share of resamples at or below 0: 0.027 (10000 resamples, seed 1237, 50 PRs).

| Generation | Delta F2 |
|---|---|
| g1 | +3.1 |
| g2 | +1.6 |
| g3 | +4.8 |
| g4 | -1.7 |

### Golden coverage

- verifier on: 158 core goldens; hit in k runs: 0: 39, 1: 18, 2: 13, 3: 24, 4: 64; hit in at least one run: 119.
- verifier off: 158 core goldens; hit in k runs: 0: 37, 1: 17, 2: 8, 3: 20, 4: 76; hit in at least one run: 121.

### Leaderboard context

Rank of the verifier-on mean: 12 of 21.

| # | Tool | F2 | Precision | Recall | TP | FP | FN |
|---|---|---|---|---|---|---|---|
| 1 | Qodo Extended | 65.1 | 67.1 | 64.6 | 102 | 50 | 56 |
| 2 | Cubic v2 | 64.9 | 61.5 | 65.8 | 104 | 65 | 54 |
| 3 | Augment | 64.0 | 59.5 | 65.2 | 103 | 70 | 55 |
| 4 | Qodo v2 | 60.6 | 55.4 | 62.0 | 98 | 79 | 60 |
| 5 | copilot-v2 | 58.0 | 38.5 | 66.5 | 105 | 168 | 53 |
| 6 | Gemini | 52.8 | 45.3 | 55.1 | 87 | 105 | 71 |
| 7 | GitLab Duo Code Review | 52.7 | 53.5 | 52.5 | 83 | 72 | 75 |
| 8 | Sourcery | 51.5 | 41.0 | 55.1 | 87 | 125 | 71 |
| 9 | Greptile v4 | 51.2 | 50.9 | 51.3 | 81 | 78 | 77 |
| 10 | CodeRabbit | 51.1 | 32.6 | 59.5 | 94 | 194 | 64 |
| 11 | Macroscope | 50.8 | 61.1 | 48.7 | 77 | 49 | 81 |
| 12 | **Angada, verifier on, mean of 4 self-runs** | 50.5 | 32.3 | 58.9 | 93 | 195 | 65 |
| 13 | Cursor Bugbot | 48.6 | 56.9 | 46.8 | 74 | 56 | 84 |
| 14 | Claude Code (CLI) | 47.7 | 46.3 | 48.1 | 76 | 88 | 82 |
| 15 | Devin | 44.8 | 69.1 | 41.1 | 65 | 29 | 93 |
| 16 | Kodus | 41.5 | 59.2 | 38.6 | 61 | 42 | 97 |
| 17 | CodeAnt | 40.9 | 40.1 | 41.1 | 65 | 97 | 93 |
| 18 | Baz | 40.5 | 61.5 | 37.3 | 59 | 37 | 99 |
| 19 | Claude Code | 38.9 | 43.2 | 38.0 | 60 | 79 | 98 |
| 20 | KG | 18.4 | 54.3 | 15.8 | 25 | 21 | 133 |
| 21 | Graphite | 9.3 | 100.0 | 7.6 | 12 | 0 | 146 |

Martian's rows come from its dashboard file at commit `e616e84` (core profile, judge `anthropic_claude-opus-4-5-20251101`). Our TP, FP and FN in that table are means over four runs.

### Methodology

- **Benchmark.** [withmartian/code-review-benchmark](https://github.com/withmartian/code-review-benchmark), offline set, commit `e616e84`: 50 PRs from cal.com, discourse, grafana, keycloak and sentry, with 173 golden comments, 158 of them in the core profile.
- **Reviews.** Angada's review engine, pinned to one commit and one configuration, reviewed each of the 50 PRs locally. Angada's production renderer turned the findings into the comment text a pull request would show: inline comments plus one summary comment. Those comments were written straight into Martian's `benchmark_data.json` as Angada's review.
- **Difference from Martian's flow.** Martian forks each PR on GitHub, lets the tool review it there, and downloads the tool's comments (steps 0 and 1). We skipped both steps. No comment was posted to GitHub in this campaign. The rendered text still names the public fork repositories of an earlier October run inside its "fix with AI" links; nothing was posted to those forks for this campaign.
- **Scoring.** Martian's own extraction (step 2), dedup (step 2.5) and judge (step 3) at commit `e616e84`, unmodified. Judge model `anthropic/claude-opus-4.5`, reached through an OpenAI-compatible gateway; Martian's board lists its judge as `anthropic_claude-opus-4-5-20251101`. Counts per PR use Martian's `score_tools` (core profile); F-beta uses beta 2.
- **Generations.** Four generations (g1 to g4) ran in parallel on 2026-11-20, starting 12:58 to 13:01 UTC, with the same pins: engine commit, reviewer version, route hash, renderer commit and render policy hash (see each `manifest.json`). The rules were fixed before the runs started: every run is reported, nothing is re-run, and degraded reviews stay in the score.
- **Verifier.** A step in Angada's pipeline that checks each candidate finding before it is published. It can drop a finding or merge it into another one.
- **Verifier off.** This arm is derived, not generated. For each generation, every candidate the verifier received in that generation passes through unverified, with the reviewer's own confidence. The same publication rules, renderer and policy then apply, and Martian's steps 2, 2.5 and 3 run again on the new comments. No new review was generated. So the two arms of one generation share the same reviews up to the verifier; they differ in the verifier and in the judge's own run-to-run variation.
- **Exceptions in the verifier-off arm.** In off-g2, off-g3 and off-g4, one review (sentry-greptile PR 5) could not be replayed and kept its verifier-on form. In off-g2, one candidate on keycloak PR 37038 was placed using its published text because the reviewer's original finding was not stored. Each `manifest.json` lists these.
- **Restarted judge attempts.** Three verifier-off judge attempts stopped before they finished (one on a gateway error, two stopped by the operator). Each was re-derived and re-judged from the start. The stopped attempts produced no score and are not published.
- **Statistics.** Per run, TP, FP and FN are summed over the 50 PRs. Arm mean and sample sd are taken over the four runs. The arm interval resamples the 50 PRs with replacement, sums each PR's counts over the four runs, and takes the 2.5 and 97.5 percentiles of pooled F2 over 10,000 resamples (seed 1237). The verifier on minus off interval uses the same PR resamples for both arms.

### Known limitations

- Self-run. Martian did not run or check these numbers. Board rows are single runs made by Martian through its own GitHub flow; ours is a mean of four runs through a different delivery path (no GitHub posting).
- The judge is reached through a gateway under the id `anthropic/claude-opus-4.5`. We did not verify that it served the same snapshot as the board's judge.
- The judge is a language model. Judging the same comments twice can give different counts. This campaign did not measure that variation separately from review variation.
- Four runs are few. The run sd is 3.0 F2 and the 95% interval is 10.6 F2 wide.
- The verifier-off arm is not independent of the verifier-on arm. The paired interval for the difference (-0.1 to +3.9) includes zero.
- Reviews that ended degraded or partial stay in the score as run: 2, 5, 3 and 3 of 50 in g1 to g4. In g2 one review (discourse-graphite PR 1) failed outright; it counts as zero findings and its 4 goldens as misses. keycloak PR 37038 ended partial in every run. No run and no PR was dropped or re-rolled.
- The board rows come from Martian's dashboard file at benchmark commit `e616e84` (committed 2026-08-30). Martian's live board may differ.
- These 50 PRs are public and were used in earlier internal measurements of Angada, so they are not a held-out set.
- The engine is not public. Its pins are opaque hashes. A reader can recompute every score from the published files but cannot regenerate the reviews.

### Recomputing the numbers

```
python3 scripts/aggregate.py campaigns/2026-11-20-baseline
```

The script uses only the Python standard library and the published files. It recomputes each PR's TP, FP and FN (core profile) from `evaluations.json` and the golden categories in `benchmark_data.json`, checks them against `scores.json`, and prints the tables in this report. With `--json PATH` it also writes the machine-readable report. The tables in this README and in `REPORT.md` are its output.

## Layout

- `latest.json`: headline of the latest campaign.
- `campaigns/2026-11-20-baseline/REPORT.md`: this campaign's report.
- `campaigns/2026-11-20-baseline/report.json`: the same numbers, machine-readable, written by `scripts/aggregate.py`.
- `campaigns/2026-11-20-baseline/leaderboard.json`: the board rows used for context, with their source.
- `campaigns/2026-11-20-baseline/runs/<run>/`, one per run (`on-g1` to `on-g4`, `off-g1` to `off-g4`):
    - `manifest.json`: benchmark repo and commit, judge model, profile, beta, arm, generation, start time, opaque pins, totals, reviews not completed; for verifier-off runs, the verifier-on run it was derived from.
    - `scores.json`: TP, FP and FN per PR and in total, with each review's status.
    - `benchmark_data.json`: the 50 PRs, their golden comments, and Angada's comments as the judge saw them. Other tools' reviews are left out.
    - `candidates.json`: the issues Martian's extraction step took from those comments.
    - `dedup_groups.json`: which extracted issues Martian's dedup step treated as one.
    - `evaluations.json`: the judge's verdict per PR: matched goldens, false positives and misses.
- `scripts/aggregate.py`: recomputes the campaign tables from the published files.
- `scripts/publish.sh`, `replay.sh`, `score.sh`, `merge_into_published.py`, `readme.py`, `summarize.py`: an earlier single-run flow that posted reviews to GitHub forks. They did not produce this campaign.
