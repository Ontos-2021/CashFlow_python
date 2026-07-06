from copy import deepcopy
from random import random, uniform

from .constants import LIQUIDITY_BY_TYPE
from .metrics import asset_value, debt_balance, monthly_obligations


def amount(state, spec):
    if isinstance(spec, (int, float)):
        return spec
    if isinstance(spec, dict):
        if "factor" in spec:
            base = state["salary"] * spec["factor"]
            if spec.get("rng", True):
                base *= uniform(0.5, 1.5)
            neg = spec["factor"] < 0
            lo = spec.get("min", -999999 if neg else 0)
            hi = spec.get("max", 0 if neg else 999999)
            return max(lo, min(hi, round(base)))
        if "min" in spec and "max" in spec:
            return round(uniform(spec["min"], spec["max"]))
    return 0


def resolve_action_amounts(action, state):
    for key in ("cash", "salary", "expenses", "pay_debt"):
        if key in action and isinstance(action[key], dict):
            action[key] = amount(state, action[key])
    if "asset" in action and isinstance(action["asset"], dict):
        for ak in ("value", "income"):
            if ak in action["asset"] and isinstance(action["asset"][ak], dict):
                action["asset"][ak] = amount(state, action["asset"][ak])
    if "debt" in action and isinstance(action["debt"], dict):
        for dk in ("balance", "payment"):
            if dk in action["debt"] and isinstance(action["debt"][dk], dict):
                action["debt"][dk] = amount(state, action["debt"][dk])
    if "label_fmt" in action:
        try:
            action["label"] = action["label_fmt"].format(**action).replace("$-", "$")
        except (KeyError, ValueError):
            pass
    return action


def apply_action_effects(state, action):
    net_worth = state["cash"] + asset_value(state) - debt_balance(state)
    crisis_scale = 1.5 if net_worth > 50000 else 1.0
    cash_delta = amount(state, action.get("cash", 0))
    if cash_delta < 0 and crisis_scale > 1:
        cash_delta = round(cash_delta * crisis_scale)
    state["cash"] += cash_delta
    state["salary"] += amount(state, action.get("salary", 0))
    exp_delta = amount(state, action.get("expenses", 0))
    state["expenses"] += exp_delta
    if exp_delta > 0:
        state.setdefault("expense_creep_log", []).append({"kind": "creep", "amount": exp_delta, "month": state["month"]})
    state["education"] += action.get("education", 0)
    stress_delta = action.get("stress", 0)
    if stress_delta > 0:
        stress_delta = round(stress_delta * 0.7)
        if crisis_scale > 1:
            stress_delta = round(stress_delta * crisis_scale)
    state["stress"] += stress_delta
    state["max_stress"] = max(state.get("max_stress", 0), state["stress"])
    state["credit_score"] += action.get("credit_score", 0)
    state["career_stability"] += action.get("career_stability", 0)
    state["lifestyle_inflation"] += action.get("lifestyle", 0)
    if action.get("salary_risk") and random() < action["salary_risk"]:
        state["salary"] = round(state["salary"] * 0.75, 2)
        state["dangerous_moment"] = "Ignorar riesgo laboral termino en recorte de ingresos"
    if action.get("asset"):
        asset = deepcopy(action["asset"])
        asset["value"] = round(asset["value"] * state["world"].get("asset_price", 1), 2)
        state["assets"].append(asset)
    if action.get("debt"):
        debt = deepcopy(action["debt"])
        debt["payment"] = round(debt["payment"] / state["world"].get("credit", 1), 2)
        rate_adj = {"Expansion": -0.02, "Estable": 0, "Recesion": 0.04, "Recuperacion": 0.01}.get(state["world"]["name"], 0)
        debt["rate"] = round(debt["rate"] + rate_adj, 4)
        state["debts"].append(debt)
    if action.get("pay_debt"):
        pay_down_debt(state, amount(state, action["pay_debt"]))
    if action.get("sell_asset_percent"):
        sell_assets(state, action["sell_asset_percent"])
    if action.get("reduce_debt_payments"):
        for debt in state["debts"]:
            debt["payment"] = round(debt["payment"] * (1 - action["reduce_debt_payments"]), 2)
            debt["rate"] = round(debt.get("rate", 0) + 0.01, 4)
    if action.get("delayed"):
        salary_snap = state["salary"]
        for entry in action["delayed"]:
            effect = dict(entry.get("effect", {}))
            if "salary_snap_pct" in effect:
                effect["salary"] = -round(salary_snap * effect.pop("salary_snap_pct"), 2)
            state.setdefault("schedule", []).append({
                "due_month": state["month"] + entry.get("delay", 1),
                "label": entry.get("label", "Consecuencia programada"),
                "source": entry.get("source", "Decision previa"),
                "effect": effect,
            })


def normalize_state(state):
    state["stress"] = max(10, min(100, round(state["stress"])))
    state["education"] = max(0, min(10, state["education"]))
    state["credit_score"] = max(300, min(850, round(state["credit_score"])))
    state["career_stability"] = max(0, min(100, round(state["career_stability"])))
    state["expenses"] = max(300, round(state["expenses"], 2))
    state["salary"] = max(0, round(state["salary"], 2))


def accrue_debt_interest(state):
    for debt in state["debts"]:
        monthly_rate = debt.get("rate", 0) / 12
        debt["balance"] = max(0, round(debt["balance"] * (1 + monthly_rate) - debt.get("payment", 0), 2))
    state["debts"] = [debt for debt in state["debts"] if debt["balance"] > 1]


def pay_down_debt(state, amt):
    remaining = amt
    state["debts"].sort(key=lambda debt: debt.get("rate", 0), reverse=True)
    for debt in state["debts"]:
        if remaining <= 0:
            break
        payment = min(remaining, debt["balance"])
        debt["balance"] -= payment
        remaining -= payment
        if debt["balance"] <= 1:
            debt["payment"] = 0
    state["debts"] = [debt for debt in state["debts"] if debt["balance"] > 1]


def sell_assets(state, percent):
    if not state["assets"]:
        return
    proceeds = 0
    for asset in state["assets"]:
        sold_value = asset["value"] * percent
        proceeds += sold_value * 0.85
        asset["value"] -= sold_value
        asset["income"] -= asset["income"] * percent
    state["cash"] += round(proceeds, 2)
    state["assets"] = [asset for asset in state["assets"] if asset["value"] > 100]


def sell_one_asset(state, asset_index, percent):
    if not state.get("assets") or asset_index < 0 or asset_index >= len(state["assets"]):
        return None
    asset = state["assets"][asset_index]
    if asset.get("type") == "Education":
        return None
    liquidity = LIQUIDITY_BY_TYPE.get(asset.get("type"), 0.75)
    sold_value = asset["value"] * percent
    proceeds = round(sold_value * liquidity, 2)
    asset["value"] = round(asset["value"] - sold_value, 2)
    asset["income"] = round(asset.get("income", 0) * (1 - percent), 2)
    state["cash"] += proceeds
    if asset["value"] <= 100:
        state["assets"].pop(asset_index)
    return {"name": asset["name"], "proceeds": proceeds, "percent": percent}


def cut_expenses(state):
    base = state.get("starting_expenses", state["expenses"])
    if state["expenses"] <= base * 1.05:
        return None
    reduction = round(state["expenses"] * 0.08, 2)
    state["expenses"] = round(state["expenses"] - reduction, 2)
    state["stress"] = min(100, state["stress"] + 12)
    state.setdefault("expense_creep_log", []).append({"kind": "cut", "amount": -reduction, "month": state["month"]})
    return {"reduction": reduction}


def pay_down_debt_action(state):
    if not state.get("debts"):
        return None
    obligations = monthly_obligations(state)
    if state["cash"] < obligations * 2:
        return None
    state["debts"].sort(key=lambda d: d.get("rate", 0), reverse=True)
    debt = state["debts"][0]
    payment = round(min(debt["balance"] * 0.2, state["cash"] * 0.25), 2)
    if payment < 50:
        return None
    debt["balance"] = round(debt["balance"] - payment, 2)
    state["cash"] = round(state["cash"] - payment, 2)
    if debt["balance"] <= 1:
        debt["payment"] = 0
    state["debts"] = [d for d in state["debts"] if d["balance"] > 1]
    state["credit_score"] = min(850, state["credit_score"] + 3)
    return {"name": debt["name"], "payment": payment}


def update_decision_records(state, event, action, impact, before, after):
    record = f"{event['title']}: {action['label']}"
    if impact >= 0.04 or after["cashflow"] - before["cashflow"] > 250:
        state["best_decision"] = record
    if impact <= -0.04 or state["cash"] < 0 or after["runway"] < 1:
        state["worst_decision"] = record
    if after["insolvency_risk"] >= 70:
        state["dangerous_moment"] = record
