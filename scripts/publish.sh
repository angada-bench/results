#!/usr/bin/env bash
set -euo pipefail
RUN_ID="${1:?run id}"
: "${TOOL:?}"
: "${OUT:?}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
HARNESS="${HARNESS:-$HOME/martian-bench/code-review-benchmark/offline}"
python3 "$SCRIPT_DIR/summarize.py" "$OUT" "$TOOL" | tee "$OUT/scoreboard.txt"
cat > "$OUT/manifest.json" <<JSON
{
  "run_id": "$RUN_ID",
  "tool_slug": "$TOOL",
  "org": "https://github.com/${ORG:-angada-bench}",
  "harness": {"repo": "withmartian/code-review-benchmark", "commit": "$(git -C "$HARNESS/.." rev-parse HEAD)"},
  "judge": {"model": "${MARTIAN_MODEL}", "base_url": "${MARTIAN_BASE_URL}", "published_equivalent": "anthropic_claude-opus-4-5-20251101"},
  "profile": "core",
  "beta": 2.0,
  "bot": "angada-apps[bot]",
  "generated_at": "$(date -u +%FT%TZ)"
}
JSON
cp "$OUT/summary.json" "$REPO_DIR/latest.json"
python3 "$SCRIPT_DIR/readme.py" "$REPO_DIR" > "$REPO_DIR/README.md"
mkdir -p "$REPO_DIR/docs"
cp "$OUT/benchmark_dashboard.html" "$REPO_DIR/docs/index.html"
cd "$REPO_DIR"
git add -A
git commit -qm "run: $RUN_ID"
git push -q origin HEAD
tar -czf "/tmp/$RUN_ID.tgz" -C "$REPO_DIR/runs" "$RUN_ID"
gh release create "$RUN_ID" "/tmp/$RUN_ID.tgz" --repo "${ORG:-angada-bench}/results" --title "$RUN_ID" --notes-file "$OUT/scoreboard.txt"
