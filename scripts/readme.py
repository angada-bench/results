import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
s = json.loads((repo / "latest.json").read_text())
lines = [
    "# Angada on Martian Code Review Bench (offline), self-run",
    "",
    "Self-run of [withmartian/code-review-benchmark](https://github.com/withmartian/code-review-benchmark) offline mode against the production Angada GitHub App. Not an official Martian leaderboard entry. Competitor rows are Martian's published results, fetched at run time.",
    "",
    f"Latest run: `{s['run']}` | judge `{s['judge']}` | profile `{s['profile']}` | F-beta {s['beta']}",
    "",
    "| # | Tool | F2 | Precision | Recall | Source |",
    "|---|---|---|---|---|---|",
]
for i, r in enumerate(s["rows"], 1):
    name = f"**{r['tool']}**" if r["source"] == "self-run" else r["tool"]
    lines.append(f"| {i} | {name} | {r['f2']:.1f}% | {r['precision']:.1f}% | {r['recall']:.1f}% | {r['source']} |")
lines += [
    "",
    "## Layout",
    "",
    "- `runs/<run_id>/`: manifest, raw bot comments (`benchmark_data.json`), judge outputs, merged results, dashboard, review run costs, Martian snapshot.",
    "- `latest.json`: scoreboard of the latest run.",
    "- `docs/index.html`: dashboard for the latest run (GitHub Pages).",
    "- `scripts/`: replay, scoring, merge and publish scripts.",
    "",
    "Reviewed PRs are public in the [angada-bench](https://github.com/angada-bench) org.",
]
print("\n".join(lines))
