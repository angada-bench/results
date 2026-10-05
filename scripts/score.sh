#!/usr/bin/env bash
set -euo pipefail
: "${TOOL:?TOOL required}"
: "${ORG:=angada-bench}"
: "${HARNESS:=$HOME/martian-bench/code-review-benchmark/offline}"
: "${OUT:?OUT required (run artifact dir)}"
: "${MARTIAN_MODEL:?}"
: "${MARTIAN_API_KEY:?}"
PUBLISHED_MODEL_DIR="anthropic_claude-opus-4-5-20251101"
OURS_MODEL_DIR="$(echo "$MARTIAN_MODEL" | tr '/' '_')"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
uvr() { ~/.local/bin/uv run "$@"; }
cd "$HARNESS"
uvr python -m code_review_benchmark.step1_download_prs --org "$ORG" --tool "$TOOL" --output results/benchmark_data.json
uvr python -m code_review_benchmark.step2_extract_comments --tool "$TOOL"
uvr python -m code_review_benchmark.step2_5_dedup_candidates --tool "$TOOL"
uvr python -m code_review_benchmark.step3_judge_comments --tool "$TOOL" --dedup-groups "results/$OURS_MODEL_DIR/dedup_groups.json"
mkdir -p "$OUT"
uvr python "$SCRIPT_DIR/merge_into_published.py" results "$OURS_MODEL_DIR" "$PUBLISHED_MODEL_DIR" "$TOOL" "$OUT/merged-results"
uvr python analysis/benchmark_dashboard.py --results-dir "$OUT/merged-results" --output "$OUT/benchmark_dashboard.html" --json-output "$OUT/benchmark_dashboard.json"
cp -r "results/$OURS_MODEL_DIR" "$OUT/judge-$OURS_MODEL_DIR"
cp results/benchmark_data.json "$OUT/benchmark_data.json"
