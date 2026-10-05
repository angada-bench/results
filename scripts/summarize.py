import json
import sys
import urllib.request
from pathlib import Path

run_dir = Path(sys.argv[1])
tool = sys.argv[2]
model = "anthropic_claude-opus-4-5-20251101"
profile = "core"

ours = json.loads((run_dir / "benchmark_dashboard.json").read_text())
with urllib.request.urlopen("https://codereview.withmartian.com/benchmark_dashboard.json") as resp:
    live_raw = resp.read()
(run_dir / "martian_live_benchmark_dashboard.json").write_bytes(live_raw)
live = json.loads(live_raw)

names = live.get("tool_display_names", {})
rows = []
for name, metrics in live["models"][model]["overall_metrics"].items():
    m = metrics[profile]
    rows.append({"tool": names.get(name, name), "key": name, "source": "martian-published", **{k: m[k] for k in ("f2", "precision", "recall", "f1")}})
mine = ours["models"][model]["overall_metrics"][tool][profile]
rows.append({"tool": "Angada", "key": tool, "source": "self-run", **{k: mine[k] for k in ("f2", "precision", "recall", "f1")}, "tp": mine.get("tp"), "fp": mine.get("fp")})
rows.sort(key=lambda r: r["f2"], reverse=True)
summary = {"run": run_dir.name, "tool": tool, "judge": model, "profile": profile, "beta": 2.0, "rows": rows}
(run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
for i, r in enumerate(rows, 1):
    print(f"{i:>2} {r['tool']:<28} F2 {r['f2']:5.1f}  P {r['precision']:5.1f}  R {r['recall']:5.1f}  {r['source']}")
