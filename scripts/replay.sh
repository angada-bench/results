#!/usr/bin/env bash
set -euo pipefail
: "${TOOL:?TOOL required, e.g. angada-2026-10}"
: "${ORG:=angada-bench}"
: "${HARNESS:=$HOME/martian-bench/code-review-benchmark/offline}"
: "${LOGS:=$HOME/martian-bench/logs/$TOOL}"
mkdir -p "$LOGS"
cd "$HARNESS"
pids=()
for f in golden_comments/*.json; do
  name="$(basename "$f" .json)"
  ~/.local/bin/uv run python -m code_review_benchmark.step0_fork_prs \
    --file "$f" --org "$ORG" --name "$TOOL" > "$LOGS/step0-$name.log" 2>&1 &
  pids+=($!)
done
rc=0
for p in "${pids[@]}"; do wait "$p" || rc=1; done
grep -h "New PR:" "$LOGS"/step0-*.log | sort > "$LOGS/prs.txt"
echo "created $(wc -l < "$LOGS/prs.txt") PRs, rc=$rc"
exit $rc
