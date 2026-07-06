"""Genera benchmarks por profesion para comparar en el postmortem.

Corre N simulaciones con bot safe y guarda promedios en scripts/benchmarks.json.

Uso:
    python scripts/gen_benchmarks.py
    python scripts/gen_benchmarks.py --runs 30
"""

import argparse
import json
import os
import random as random_module
import sys
from collections import Counter
from statistics import median

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "cashflow_game"))

from app.game_engine import (  # noqa: E402
    PROFESSIONS,
    apply_action,
    enrich_state,
    metrics,
    monthly_obligations,
    new_game,
    pay_down_debt_action,
)

MAX_MONTHS = 300


def safe_choose(state, actions):
    from copy import deepcopy
    from app.game_engine import apply_action_effects, normalize_state
    before_fr = metrics(state)["freedom_ratio"]
    candidates = []
    for action_id, action in actions.items():
        tags = action.get("risk_tags", [])
        critical = any(tag in {"Caja negativa", "Supervivencia critica", "Riesgo de burnout"} for tag in tags)
        sim = deepcopy(state)
        apply_action_effects(sim, action)
        normalize_state(sim)
        after = metrics(sim)
        delta_fr = after["freedom_ratio"] - before_fr
        cash = sim["cash"]
        candidates.append((not critical, delta_fr, cash, action_id))
    candidates.sort(reverse=True)
    return candidates[0][3]


def run_one(profession_id, seed):
    random_module.seed(seed)
    state = new_game(profession_id)
    state = enrich_state(state)
    while state.get("status") == "playing" and state.get("month", 0) < MAX_MONTHS:
        if state.get("debts") and state.get("cash", 0) > monthly_obligations(state) * 2:
            if not state.get("action_used_this_month", {}).get("pay_debt"):
                if pay_down_debt_action(state):
                    state.setdefault("action_used_this_month", {})["pay_debt"] = True
        event = state.get("current_event")
        if not event:
            break
        if event["id"] == "quiet_month":
            action_id = "advance"
        else:
            actions = event.get("actions", {})
            if not actions:
                break
            action_id = safe_choose(state, actions)
        state = apply_action(state, action_id)
        state = enrich_state(state)
    return state


def collect(state):
    data = metrics(state)
    return {
        "outcome": state.get("outcome"),
        "status": state.get("status"),
        "month": state.get("month", 0),
        "net_worth": data["net_worth"],
        "freedom_ratio": data["freedom_ratio"],
        "runway": data["runway"],
        "stress_final": state.get("stress", 0),
        "max_stress": state.get("max_stress", 0),
        "assets_count": len(state.get("assets", [])),
        "debts_count": len(state.get("debts", [])),
        "cash_final": state.get("cash", 0),
    }


def aggregate_by_profession(runs, runs_per):
    benchmarks = {}
    for prof_id in PROFESSIONS.keys():
        cell = [r for r in runs if r["profession"] == prof_id]
        if not cell:
            continue
        outcomes = Counter(r["outcome"] for r in cell)
        win_rate = outcomes.get("Financially free", 0) / len(cell)
        benchmarks[prof_id] = {
            "win_rate": round(win_rate, 3),
            "runs": len(cell),
            "median_month": round(median(r["month"] for r in cell), 0),
            "median_cash_final": round(median(r["cash_final"] for r in cell), 0),
            "median_net_worth": round(median(r["net_worth"] for r in cell), 0),
            "median_freedom_ratio": round(median(r["freedom_ratio"] for r in cell), 3),
            "median_runway": round(median(r["runway"] for r in cell), 1),
            "median_assets": round(median(r["assets_count"] for r in cell), 1),
            "median_debts": round(median(r["debts_count"] for r in cell), 1),
            "median_max_stress": round(median(r["max_stress"] for r in cell), 0),
            "outcomes": dict(outcomes),
        }
    return benchmarks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=30, help="Runs per profession (default 30)")
    args = parser.parse_args()

    prof_ids = list(PROFESSIONS.keys())
    total = args.runs * len(prof_ids)
    print(f"Generating benchmarks: {args.runs} runs x {len(prof_ids)} professions = {total} simulations", file=sys.stderr)

    runs = []
    for prof_id in prof_ids:
        for i in range(args.runs):
            seed = hash(("benchmark", prof_id, i)) & 0xFFFFFFFF
            state = run_one(prof_id, seed)
            r = collect(state)
            r["profession"] = prof_id
            runs.append(r)
        print(f"  {prof_id}: done", file=sys.stderr)

    benchmarks = aggregate_by_profession(runs, args.runs)

    out_path = os.path.join(os.path.dirname(__file__), "benchmarks.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(benchmarks, f, indent=2, ensure_ascii=False)
    print(f"Saved to {out_path}", file=sys.stderr)
    print(json.dumps(benchmarks, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
