# Angada on Martian's Code Review Bench

Eight runs of Angada on the offline set of [Martian's Code Review Bench](https://github.com/withmartian/code-review-benchmark): 50 pull requests, 158 known defects in the Core set.

These are our own runs, not Martian's, and not an official leaderboard entry. Martian scores every tool on its board itself.

## Results

| Run | Date | Verifier | Hits of 158 | Wrong | Precision | Recall | F1 | F2 |
|---|---|---|---|---|---|---|---|---|
| 1 | 20 Nov 2026 | on | 96 | 205 | .319 | .608 | .418 | .514 |
| 2 | 20 Nov 2026 | on | 87 | 193 | .311 | .551 | .397 | .477 |
| 3 | 20 Nov 2026 | on | 100 | 187 | .348 | .633 | .449 | .544 |
| 4 | 20 Nov 2026 | on | 89 | 195 | .313 | .563 | .403 | .486 |
| 5 | 20 Nov 2026 | off | 101 | 311 | .245 | .639 | .354 | .484 |
| 6 | 20 Nov 2026 | off | 93 | 284 | .247 | .589 | .348 | .461 |
| 7 | 20 Nov 2026 | off | 101 | 286 | .261 | .639 | .371 | .496 |
| 8 | 20 Nov 2026 | off | 102 | 281 | .266 | .646 | .377 | .502 |
| **Mean, verifier on** | | | **93.0** | **195.0** | **.323** | **.589** | **.417** | **.505** |
| **Mean, verifier off** | | | **99.3** | **290.5** | **.255** | **.628** | **.362** | **.486** |

The number we quote is the verifier-on mean: F2 .505 (sd .030, range .477 to .544). Two runs of the same configuration differed by .067, so we do not quote any single run. On Martian's board (Core set, same judge model) that mean would sit 12th of 21 rows. The board rows are single runs that Martian made itself.

Every full run of this configuration is reported, low ones included. Nothing was re-run to get a better number. One comparison run of an older configuration, made the same day, is not included.

Intervals, golden coverage and the board table are in [report/REPORT.md](report/REPORT.md).

## The verifier

The verifier is a step that checks each candidate finding before it is published. It can drop a finding or merge it into another one.

With the verifier on, each run had about 6 fewer hits and about 96 fewer wrong comments. Pooled over the four pairs of runs, F2 was .020 higher (paired 95% interval -.001 to +.039, which includes zero).

The verifier-off runs are derived, not reviewed again. For each verifier-on run, the same candidates pass through unverified and are judged again. Run 5 comes from run 1, run 6 from run 2, run 7 from run 3 and run 8 from run 4. So runs 5 to 8 are not independent of runs 1 to 4.

## How the runs were made

- Reviews: Angada's engine reviewed each pull request locally at one pinned configuration (pins in `runs.json`). Angada's production renderer produced the comment text.
- Delivery: the comments were not posted to GitHub in this campaign. They were written straight into Martian's `benchmark_data.json`. Martian's own flow posts each review on a GitHub fork and downloads the comments from there.
- Scoring: Martian's pipeline at commit `e616e84` (extract, dedup and judge steps), with Claude Opus 4.5 as the judge, reached through a gateway, on the Core set. Reviews that ended degraded or partial were left in as run (2, 5, 3 and 3 of 50 in runs 1 to 4). No pull request was dropped or re-rolled.
- Exceptions: in runs 6, 7 and 8, one review (sentry-greptile PR 5) could not be replayed and kept its verifier-on form; in run 6, one candidate on keycloak PR 37038 was placed by its published text. Three verifier-off judge attempts stopped before they finished (one on a gateway error, two stopped by the operator); each was derived and judged again from the start, and the stopped attempts are not published.

## Files

Each `run-N/` folder holds:

| File | What it is |
|---|---|
| `benchmark_data.json` | The 50 pull requests, their golden comments, and Angada's comments as the judge saw them. Other tools' reviews are left out. |
| `candidates.json` | The issues Martian's extraction step took from those comments. |
| `dedup_groups.json` | Which extracted issues Martian's dedup step treated as one. |
| `evaluations.json` | The judge's verdict for each pull request: hits, wrong comments and misses. |

Our tool key in these files is `angada`.

- `runs.json`: one entry per run: date, verifier, the run it was derived from, pins, benchmark, judge, profile, beta, the original harness tool key, reviews not completed, derivation exceptions and totals.
- `report/`: the detailed report (`REPORT.md`), the same numbers as `report.json`, and the board rows used for context (`leaderboard.json`).
- `scripts/aggregate.py`: recomputes every table here and in the report from the files.
- The other scripts in `scripts/` belong to an earlier single-run flow. They did not produce these runs.

## Checking the numbers

The raw totals in `evaluations.json` cover all 173 golden comments. Hits over all 173: 100, 89, 103, 93, 106, 95, 104 and 106 in runs 1 to 8. The board's default view is the Core set: it leaves out the 15 golden comments in the style and speculative categories and keeps 158. `aggregate.py` counts a hit or a miss only when the golden comment's category is bug, security, concurrency, data, api, perf, test_gap or doc_defect. It takes the category from the verdict, or else looks up the golden comment's text in `benchmark_data.json`. Wrong comments count in full. This mirrors `_compute_profile_metrics` in Martian's `offline/analysis/benchmark_dashboard.py`.

```
python3 scripts/aggregate.py
```

It uses only the Python standard library. It prints the table above first, then the tables in the report. With `--json report/report.json` it also writes the machine-readable report.

## Limitations

- The judge was reached through a gateway. We did not verify that it served the same snapshot as the board's judge.
- These 50 pull requests were used in earlier internal measurements, so they are not a held-out set.

Other limitations are listed in [report/REPORT.md](report/REPORT.md).
