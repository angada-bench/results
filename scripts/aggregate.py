import argparse
import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

CORE = frozenset({"bug", "security", "concurrency", "data", "api", "perf", "test_gap", "doc_defect"})
BETA = 2.0


def load(path):
    return json.loads(Path(path).read_text())


def metrics(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    def fb(b):
        d = b * b * p + r
        return (1 + b * b) * p * r / d if d else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": fb(1.0), "f2": fb(BETA)}


def categories(bench):
    out = {}
    for entry in bench.values():
        for g in entry.get("golden_comments", []):
            if g.get("comment") and g.get("category"):
                out[g["comment"]] = g["category"]
    return out


def category(x, cats):
    return x.get("category") or cats.get(x.get("golden_comment", ""), "")


def per_pr_counts(evals, bench, tool):
    cats = categories(bench)
    out = {}
    for url, row in evals.items():
        t = row.get(tool)
        if t is None:
            continue
        if t.get("skipped"):
            out[url] = {"tp": 0, "fp": 0, "fn": 0}
            continue
        out[url] = {
            "tp": sum(category(x, cats) in CORE for x in t.get("true_positives", [])),
            "fp": t.get("fp", 0),
            "fn": sum(category(x, cats) in CORE for x in t.get("false_negatives", [])),
        }
    return out


def golden_hits(runs):
    hits = {}
    for i, run in enumerate(runs):
        cats = categories(run["bench"])
        for url, row in run["evals"].items():
            t = row.get(run["tool"]) or {}
            if t.get("skipped"):
                continue
            for hit, entries in ((True, t.get("true_positives", [])), (False, t.get("false_negatives", []))):
                for x in entries:
                    if category(x, cats) not in CORE:
                        continue
                    key = (url, x["golden_comment"])
                    hits.setdefault(key, set())
                    if hit:
                        hits[key].add(i)
    return hits


def load_run(d):
    man = load(d / "manifest.json")
    scores = load(d / "scores.json")
    evals = load(d / "evaluations.json")
    bench = load(d / "benchmark_data.json")
    tool = man["tool_key"]
    counts = per_pr_counts(evals, bench, tool)
    stored = {u: {k: v[k] for k in ("tp", "fp", "fn")} for u, v in scores["per_pr"].items()}
    if counts != stored:
        bad = sorted(u for u in set(counts) | set(stored) if counts.get(u) != stored.get(u))
        sys.exit(f"{d.name}: per-PR counts from evaluations.json differ from scores.json: {bad}")
    status = {u: v.get("status") for u, v in scores["per_pr"].items()}
    return {"name": d.name, "arm": man["arm"], "generation": man["generation"], "tool": tool,
            "manifest": man, "per_pr": counts, "status": status, "evals": evals, "bench": bench}


def pooled(runs, urls):
    tp = fp = fn = 0
    for run in runs:
        for u in urls:
            c = run["per_pr"].get(u)
            if c:
                tp += c["tp"]
                fp += c["fp"]
                fn += c["fn"]
    return metrics(tp, fp, fn)


def bootstrap(stat, urls, resamples, seed):
    rng = random.Random(seed)
    values = sorted(stat([rng.choice(urls) for _ in urls]) for _ in range(resamples))
    return {"mean": sum(values) / resamples,
            "ci95": [values[int(0.025 * resamples)], values[int(0.975 * resamples) - 1]],
            "share_le_0": sum(v <= 0 for v in values) / resamples,
            "resamples": resamples, "seed": seed}


def spread(values):
    return {"mean": statistics.mean(values), "sd": statistics.stdev(values) if len(values) > 1 else None,
            "min": min(values), "max": max(values), "n": len(values)}


def build(campaign, resamples, seed):
    runs = [load_run(d) for d in sorted((campaign / "runs").iterdir()) if (d / "manifest.json").is_file()]
    runs.sort(key=lambda r: (r["arm"] != "on", r["generation"]))
    rows = []
    for r in runs:
        m = metrics(*(sum(c[k] for c in r["per_pr"].values()) for k in ("tp", "fp", "fn")))
        rows.append({"run": r["name"], "arm": r["arm"], "generation": r["generation"], "prs": len(r["per_pr"]),
                     **m, "not_completed": sum(s != "completed" for s in r["status"].values()),
                     "derived_from": r["manifest"].get("derived_from")})
    by_arm = {}
    for r in runs:
        by_arm.setdefault(r["arm"], []).append(r)
    arms = {}
    for arm, rs in by_arm.items():
        ms = [x for x in rows if x["arm"] == arm]
        urls = sorted(set.intersection(*(set(r["per_pr"]) for r in rs)))
        arms[arm] = {"generations": [r["generation"] for r in rs], "prs": len(urls),
                     **{k: spread([x[k] for x in ms]) for k in ("f2", "precision", "recall")},
                     "tp_mean": statistics.mean(x["tp"] for x in ms),
                     "fp_mean": statistics.mean(x["fp"] for x in ms),
                     "fn_mean": statistics.mean(x["fn"] for x in ms),
                     "pooled": pooled(rs, urls),
                     "pooled_f2_bootstrap": bootstrap(lambda p, rs=rs: pooled(rs, p)["f2"], urls, resamples, seed)}
    delta = None
    if "on" in by_arm and "off" in by_arm:
        off_by = {r["generation"]: r for r in by_arm["off"]}
        pairs = [(a, off_by[a["generation"]]) for a in by_arm["on"] if a["generation"] in off_by]
        ons, offs = [a for a, _ in pairs], [b for _, b in pairs]
        urls = sorted(set.intersection(*(set(a["per_pr"]) & set(b["per_pr"]) for a, b in pairs)))
        d = lambda p: pooled(ons, p)["f2"] - pooled(offs, p)["f2"]
        delta = {"generations": [a["generation"] for a in ons], "prs": len(urls), "pooled_delta_f2": d(urls),
                 "bootstrap": bootstrap(d, urls, resamples, seed),
                 "per_generation": {a["generation"]: pooled([a], urls)["f2"] - pooled([b], urls)["f2"] for a, b in pairs}}
    coverage = {}
    for arm, rs in by_arm.items():
        hits = golden_hits(rs)
        hist = Counter(len(v) for v in hits.values())
        coverage[arm] = {"core_goldens": len(hits),
                         "hit_in_k_runs": {str(k): hist.get(k, 0) for k in range(len(rs) + 1)},
                         "hit_in_any_run": sum(bool(v) for v in hits.values())}
    board_doc = load(campaign / "leaderboard.json")
    on = arms.get("on")
    board = [dict(x, self_run=False) for x in board_doc["rows"]]
    if on:
        board.append({"tool": f"Angada, verifier on, mean of {on['f2']['n']} self-runs", "f2": 100 * on["f2"]["mean"],
                      "precision": 100 * on["precision"]["mean"], "recall": 100 * on["recall"]["mean"],
                      "tp": on["tp_mean"], "fp": on["fp_mean"], "fn": on["fn_mean"], "prs": on["prs"], "self_run": True})
    board.sort(key=lambda x: -x["f2"])
    rank = next((i for i, x in enumerate(board, 1) if x["self_run"]), None)
    return {"schema": "angada-bench.campaign/v1", "campaign": campaign.name, "profile": "core", "beta": BETA,
            "runs": rows, "arms": arms, "on_minus_off": delta, "coverage": coverage,
            "leaderboard": {"source": board_doc["source"], "judge": board_doc["judge"], "rows": board,
                            "rank_of_on_mean": rank, "rows_total": len(board)}}


def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}"


def markdown(doc):
    out = ["## Runs", "", "| Run | Verifier | PRs | TP | FP | FN | Precision | Recall | F1 | F2 | Reviews not completed |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in doc["runs"]:
        out.append(f"| {r['run']} | {r['arm']} | {r['prs']} | {r['tp']} | {r['fp']} | {r['fn']} | {pct(r['precision'])} | "
                   f"{pct(r['recall'])} | {pct(r['f1'])} | {pct(r['f2'])} | {r['not_completed']} |")
    out += ["", "## Arms", "", "| Verifier | Runs | F2 mean | F2 sd | F2 range | Precision mean | Recall mean | TP / FP / FN mean | Pooled F2 | Pooled F2 95% interval |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for arm, a in doc["arms"].items():
        ci = a["pooled_f2_bootstrap"]["ci95"]
        out.append(f"| {arm} | {a['f2']['n']} | {pct(a['f2']['mean'])} | {pct(a['f2']['sd'])} | {pct(a['f2']['min'])} to {pct(a['f2']['max'])} | "
                   f"{pct(a['precision']['mean'])} | {pct(a['recall']['mean'])} | {a['tp_mean']:g} / {a['fp_mean']:g} / {a['fn_mean']:g} | "
                   f"{pct(a['pooled']['f2'])} | {pct(ci[0])} to {pct(ci[1])} |")
    d = doc["on_minus_off"]
    if d:
        b = d["bootstrap"]
        out += ["", "## Verifier on minus verifier off", "",
                f"Pooled delta F2 {100 * d['pooled_delta_f2']:+.1f}, paired 95% interval {100 * b['ci95'][0]:+.1f} to {100 * b['ci95'][1]:+.1f}, "
                f"share of resamples at or below 0: {b['share_le_0']:.3f} ({b['resamples']} resamples, seed {b['seed']}, {d['prs']} PRs).", "",
                "| Generation | Delta F2 |", "|---|---|"]
        out += [f"| {g} | {100 * v:+.1f} |" for g, v in d["per_generation"].items()]
    out += ["", "## Golden coverage", ""]
    for arm, c in doc["coverage"].items():
        h = ", ".join(f"{k}: {v}" for k, v in c["hit_in_k_runs"].items())
        out.append(f"- verifier {arm}: {c['core_goldens']} core goldens; hit in k runs: {h}; hit in at least one run: {c['hit_in_any_run']}.")
    lb = doc["leaderboard"]
    out += ["", "## Leaderboard context", "", f"Rank of the verifier-on mean: {lb['rank_of_on_mean']} of {lb['rows_total']}.", "",
            "| # | Tool | F2 | Precision | Recall | TP | FP | FN |", "|---|---|---|---|---|---|---|---|"]
    for i, x in enumerate(lb["rows"], 1):
        name = f"**{x['tool']}**" if x["self_run"] else x["tool"]
        out.append(f"| {i} | {name} | {x['f2']:.1f} | {x['precision']:.1f} | {x['recall']:.1f} | {x['tp']:g} | {x['fp']:g} | {x['fn']:g} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Recompute the campaign tables from the published run files.")
    ap.add_argument("campaign", nargs="?", default=str(Path(__file__).resolve().parent.parent / "campaigns" / "2026-11-20-baseline"))
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=1237)
    ap.add_argument("--json", help="write the machine-readable report to this path")
    args = ap.parse_args()
    doc = build(Path(args.campaign), args.resamples, args.seed)
    if args.json:
        Path(args.json).write_text(json.dumps(doc, indent=2) + "\n")
    print(markdown(doc), end="")


if __name__ == "__main__":
    main()
