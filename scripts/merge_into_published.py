import json
import shutil
import sys
from pathlib import Path

src_root = Path(sys.argv[1])
ours_dir = src_root / sys.argv[2]
published_dir = src_root / sys.argv[3]
tool = sys.argv[4]
out_root = Path(sys.argv[5])

out_root.mkdir(parents=True, exist_ok=True)
for extra in ("benchmark_data.json", "pr_labels.json"):
    if (src_root / extra).exists():
        shutil.copy(src_root / extra, out_root / extra)

merged_dir = out_root / published_dir.name
merged_dir.mkdir(parents=True, exist_ok=True)
for name in ("candidates.json", "dedup_groups.json", "evaluations.json"):
    published = json.loads((published_dir / name).read_text())
    ours_path = ours_dir / name
    ours = json.loads(ours_path.read_text()) if ours_path.exists() else {}
    added = 0
    for url, tools in ours.items():
        if tool in tools:
            published.setdefault(url, {})[tool] = tools[tool]
            added += 1
    (merged_dir / name).write_text(json.dumps(published, indent=2))
    print(f"{name}: merged {added} PRs for {tool}")
