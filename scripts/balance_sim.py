"""Harness de balance para Cashflow Game.

Simula muchas partidas con bots y reporta metricas agregadas para detectar
desbalances por profesion y politica de juego.

Uso:
    python scripts/balance_sim.py --runs 50
    python scripts/balance_sim.py --runs 1 --json
"""

import argparse
import json
import os
import random as random_module
import sys
from collections import Counter
from copy import deepcopy
from statistics import median

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "cashflow_game"))

from app.game_engine import (  # noqa: E402
    PROFESSIONS,
    apply_action,
    apply_action_effects,
    enrich_state,
    metrics,
    new_game,
    normalize_state,
)

CRITICAL_TAGS = {"Caja negativa", "Supervivencia critica", "Riesgo de burnout"}
MAX_MONTHS = 300
PROFSSION_IDS = list(PROFESSIONS.keys())


def run_game(profession_id, policy, seed):
    random_module.seed(seed)
    state = new_game(profession_id)
    state = enrich_state(state)
    steps = 0
    while state.get("status") == "playing" and state.get("month", 0) < MAX_MONTHS:
        event = state.get("current_event")
        if not event:
            break
        action_id = choose_action(state, event, policy)
        state = apply_action(state, action_id)
        state = enrich_state(state)
        steps += 1
    return state, steps


def choose_action(state, event, policy):
    if event["id"] == "quiet_month":
        return "advance"
    actions = event.get("actions", {})
    if not actions:
        return "skip"
    if policy == "random":
        return random_module.choice(list(actions.keys()))
    return safe_choose(state, actions)


def safe_choose(state, actions):
    before_fr = metrics(state)["freedom_ratio"]
    candidates = []
    for action_id, action in actions.items():
        tags = action.get("risk_tags", [])
        critical = any(tag in CRITICAL_TAGS for tag in tags)
        sim = deepcopy(state)
        apply_action_effects(sim, action)
        normalize_state(sim)
        after = metrics(sim)
        delta_fr = after["freedom_ratio"] - before_fr
        cash = sim["cash"]
        candidates.append((not critical, delta_fr, cash, action_id))
    candidates.sort(reverse=True)
    return candidates[0][3]


def collect_run_result(state, profession_id, policy, run_idx, steps):
    data = metrics(state)
    events_seen = state.get("events_seen", [])
    return {
        "profession": profession_id,
        "policy": policy,
        "run": run_idx,
        "outcome": state.get("outcome"),
        "status": state.get("status"),
        "month": state.get("month", 0),
        "age": state.get("age", 0),
        "net_worth": data["net_worth"],
        "freedom_ratio": data["freedom_ratio"],
        "runway": data["runway"],
        "stress": state.get("stress", 0),
        "profile": state.get("investor_profile", ""),
        "quiet_months": state.get("quiet_months", 0),
        "insolvent_months": state.get("insolvent_months", 0),
        "events_seen": list(events_seen),
        "best_decision": state.get("best_decision"),
        "worst_decision": state.get("worst_decision"),
        "steps": steps,
    }


def run_matrix(runs_per_cell):
    results = []
    total = len(PROFSSION_IDS) * 2 * runs_per_cell
    done = 0
    for profession_id in PROFSSION_IDS:
        for policy in ("random", "safe"):
            for run_idx in range(runs_per_cell):
                seed = hash((profession_id, policy, run_idx)) & 0xFFFFFFFF
                state, steps = run_game(profession_id, policy, seed)
                result = collect_run_result(state, profession_id, policy, run_idx, steps)
                results.append(result)
                done += 1
                if done % 100 == 0:
                    print(f"  ...{done}/{total} runs", file=sys.stderr)
    return results


def aggregate(results):
    report = {"by_cell": {}, "global": {}}
    for profession_id in PROFSSION_IDS:
        for policy in ("random", "safe"):
            cell_results = [r for r in results if r["profession"] == profession_id and r["policy"] == policy]
            if not cell_results:
                continue
            outcomes = Counter(r["outcome"] for r in cell_results)
            statuses = Counter(r["status"] for r in cell_results)
            months = [r["month"] for r in cell_results]
            ages = [r["age"] for r in cell_results]
            freedom = [r["freedom_ratio"] for r in cell_results]
            net_worths = [r["net_worth"] for r in cell_results]
            runways = [r["runway"] for r in cell_results]
            stresses = [r["stress"] for r in cell_results]
            quiet = [r["quiet_months"] for r in cell_results]
            profiles = Counter(r["profile"] for r in cell_results)
            event_freq = Counter()
            for r in cell_results:
                event_freq.update(r["events_seen"])
            report["by_cell"][f"{profession_id}_{policy}"] = {
                "count": len(cell_results),
                "outcomes": dict(outcomes),
                "statuses": dict(statuses),
                "median_month": median(months),
                "min_month": min(months),
                "max_month": max(months),
                "median_age": median(ages),
                "median_freedom_ratio": round(median(freedom), 3),
                "median_net_worth": round(median(net_worths), 0),
                "median_runway": round(median(runways), 1),
                "median_stress": median(stresses),
                "median_quiet_months": median(quiet),
                "profiles": dict(profiles),
                "event_freq": dict(event_freq.most_common(10)),
            }
    all_events = set()
    from app.game_engine import BASE_EVENTS, PROFESSION_EVENTS
    for event in BASE_EVENTS + PROFESSION_EVENTS:
        all_events.add(event["id"])
    seen_events = set()
    for r in results:
        seen_events.update(r["events_seen"])
    never_seen = sorted(all_events - seen_events)
    all_outcomes = Counter(r["outcome"] for r in results)
    all_profiles = Counter(r["profile"] for r in results)
    all_quiet = [r["quiet_months"] for r in results]
    report["global"] = {
        "total_runs": len(results),
        "outcomes": dict(all_outcomes),
        "profiles": dict(all_profiles),
        "median_quiet_months": median(all_quiet) if all_quiet else 0,
        "never_seen_events": never_seen,
        "event_count": len(all_events),
        "seen_event_count": len(seen_events),
    }
    return report


def print_summary(report):
    print("=" * 72)
    print("BALANCE REPORT - Cashflow Game")
    print("=" * 72)
    g = report["global"]
    print(f"\nTotal runs: {g['total_runs']}")
    print(f"Events: {g['seen_event_count']}/{g['event_count']} seen, {len(g['never_seen_events'])} never seen")
    print(f"Median quiet months: {g['median_quiet_months']}")
    print(f"\nOutcomes:")
    for outcome, count in sorted(g["outcomes"].items(), key=lambda kv: kv[1], reverse=True):
        pct = count / g["total_runs"] * 100
        print(f"  {outcome:40s} {count:4d} ({pct:5.1f}%)")
    print(f"\nInvestor profiles:")
    for profile, count in sorted(g["profiles"].items(), key=lambda kv: kv[1], reverse=True):
        pct = count / g["total_runs"] * 100
        print(f"  {profile:40s} {count:4d} ({pct:5.1f}%)")
    if g["never_seen_events"]:
        print(f"\nEvents NEVER seen ({len(g['never_seen_events'])}):")
        for eid in g["never_seen_events"]:
            print(f"  - {eid}")
    print("\n" + "-" * 72)
    print(f"{'Cell':<30s} {'Won':>5s} {'Lost':>5s} {'Ended':>5s} {'Med.Mo':>7s} {'Med.FR':>7s} {'Med.QM':>7s}")
    print("-" * 72)
    for key, cell in sorted(report["by_cell"].items()):
        outcomes = cell["outcomes"]
        won = outcomes.get("Financially free", 0)
        lost = outcomes.get("Debt trapped", 0)
        ended = sum(v for k, v in outcomes.items() if k not in ("Financially free", "Debt trapped"))
        print(
            f"{key:<30s} {won:5d} {lost:5d} {ended:5d}"
            f" {cell['median_month']:7.0f} {cell['median_freedom_ratio']:7.2f} {cell['median_quiet_months']:7.0f}"
        )
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description="Balance simulation for Cashflow Game")
    parser.add_argument("--runs", type=int, default=50, help="Runs per cell (profession x policy)")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of summary")
    parser.add_argument("--save", type=str, default=None, help="Save JSON report to file")
    args = parser.parse_args()
    print(f"Running {args.runs} runs/cell x {len(PROFSSION_IDS)} professions x 2 policies = {args.runs * len(PROFSSION_IDS) * 2} total", file=sys.stderr)
    results = run_matrix(args.runs)
    report = aggregate(results)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Saved to {args.save}", file=sys.stderr)
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print_summary(report)


if __name__ == "__main__":
    main()
