from copy import deepcopy
from random import choice, random, uniform

from .constants import PROFESSIONS, WORLD_STATES
from .events import BASE_EVENTS, MINOR_EVENTS, PROFESSION_EVENTS
from .metrics import debt_payments, display_age, metrics, session_phase, simple_snapshot
from .actions import (
    accrue_debt_interest, apply_action_effects, normalize_state,
    resolve_action_amounts, update_decision_records,
)
from .ui import build_feedback, enrich_state, feedback


def new_game(profession_id):
    profession = deepcopy(PROFESSIONS[profession_id])
    state = {
        "profession_id": profession_id,
        "profession": profession["name"],
        "profession_summary": profession["summary"],
        "risk_profile": profession["risk_profile"],
        "career_stability": profession["career_stability"],
        "starting_expenses": profession["expenses"],
        "age": profession["age"],
        "month": 1,
        "cash": profession["cash"],
        "salary": profession["salary"],
        "expenses": profession["expenses"],
        "education": profession["education"],
        "stress": profession["stress"],
        "credit_score": profession["credit_score"],
        "assets": [],
        "debts": profession["debts"],
        "history": [],
        "status": "playing",
        "outcome": None,
        "world": WORLD_STATES[1],
        "current_event": None,
        "last_feedback": feedback("Bienvenido", "Tu meta es construir ingreso pasivo y reserva.", "La libertad financiera necesita flujo y liquidez."),
        "best_decision": None,
        "worst_decision": None,
        "dangerous_moment": None,
        "insolvent_months": 0,
        "lifestyle_inflation": 0,
        "quiet_months": 0,
        "consecutive_quiet": 0,
        "events_seen": [],
        "schedule": [],
        "asset_events": [],
        "action_used_this_month": {"sell": False, "cut_expenses": False, "pay_debt": False},
        "expense_creep_log": [],
    }
    start_month(state)
    return enrich_state(state)


def start_month(state):
    state["world"] = choice(WORLD_STATES)
    apply_monthly_cashflow(state)
    apply_market_drift(state)
    maybe_salary_shock(state)
    if is_quiet_month(state):
        if random() < 0.25:
            event = minor_event(state)
        else:
            event = quiet_month_event(state)
    else:
        state["consecutive_quiet"] = 0
        event = pick_event(state)
    state["current_event"] = event
    return state


def event_fits_state(event, state, phase):
    if event.get("requires_debt") and not state["debts"]:
        return False
    if event.get("requires_debt_free") and state["debts"]:
        return False
    required_type = event.get("requires_asset_type")
    if required_type and not any(asset.get("type") == required_type for asset in state["assets"]):
        return False
    if event.get("requires_world") and state["world"]["name"] not in event["requires_world"]:
        return False
    required_profession = event.get("requires_profession")
    if required_profession and required_profession != state.get("profession_id"):
        return False
    if event["id"] == "burnout" and state["stress"] >= 85:
        return True
    if event.get("phase") in {phase, "survival"} or phase == "freedom":
        return True
    return False


def pick_event(state):
    phase = session_phase(state)
    available = [event for event in BASE_EVENTS if event_fits_state(event, state, phase)]
    profession_events = [event for event in PROFESSION_EVENTS if event_fits_state(event, state, phase)]
    if profession_events:
        available.extend(profession_events)
    if len(available) >= 3:
        recent = set(state.get("events_seen", [])[-4:])
        fresh = [event for event in available if event["id"] not in recent]
        if fresh:
            available = fresh
    event = prepare_event_for_state(deepcopy(choice(available or BASE_EVENTS)), state)
    state.setdefault("events_seen", []).append(event["id"])
    state["events_seen"] = state["events_seen"][-12:]
    return event


def is_quiet_month(state):
    if state["month"] <= 6:
        return False
    if state.get("consecutive_quiet", 0) >= 2:
        return False
    data = metrics(state)
    if data["cashflow"] < 300 or data["runway"] < 6 or state["stress"] > 65 or data["insolvency_risk"] >= 30:
        return False
    current = state.get("current_event") or {}
    if current.get("id") == "quiet_month":
        return False
    for item in state.get("schedule", []):
        if item["due_month"] <= state["month"] + 1:
            return False
    return True


def quiet_month_event(state):
    data = metrics(state)
    months = 1
    if data["runway"] >= 8 and data["cashflow"] >= 600 and state["stress"] <= 45:
        months = 2
    return {
        "id": "quiet_month",
        "category": "Quiet",
        "phase": "survival",
        "title": "Mes tranquilo",
        "description": "Tu flujo es positivo, tenes reserva y no hay decisiones urgentes. Avanzar meses te acerca a la siguiente oportunidad.",
        "actions": {
            "advance": {
                "label": f"Avanzar {months} {'mes' if months == 1 else 'meses'}",
                "quiet": True,
                "skip_months": months,
                "lesson": "Tiempo compuesto",
                "interpretation": f"Avanzaste {months} {'mes' if months == 1 else 'meses'}. El tiempo tambien compone cuando tu estructura financiera esta sana.",
            },
        },
    }


def minor_event(state):
    template = deepcopy(choice(MINOR_EVENTS))
    event = {
        "id": template["id"],
        "category": "Quiet",
        "phase": "survival",
        "title": template["title"],
        "description": template["description"],
        "actions": {
            "continue": {
                "label": "Continuar",
                "quiet": True,
                "skip_months": 1,
                "lesson": template.get("lesson", "Contexto"),
                "interpretation": template.get("interpretation", "Un mes sin sobresaltos."),
            },
        },
    }
    for key in ("cash", "stress", "expenses", "education", "career_stability"):
        if key in template:
            event["actions"]["continue"][key] = template[key]
    return prepare_event_for_state(event, state)


def simulate_quiet_months(state, months):
    for _ in range(months):
        if state["status"] != "playing":
            break
        advance_time(state, 1)
        state["world"] = choice(WORLD_STATES)
        apply_monthly_cashflow(state)
        apply_market_drift(state)
        maybe_salary_shock(state)
        state["stress"] = max(10, state["stress"] - 2)
        state["max_stress"] = max(state.get("max_stress", 0), state["stress"])
        state["quiet_months"] = state.get("quiet_months", 0) + 1
        state["consecutive_quiet"] = state.get("consecutive_quiet", 0) + 1
        check_end_conditions(state)


def prepare_event_for_state(event, state):
    actions = {}
    for key, action in event["actions"].items():
        if action.get("pay_debt") and not state["debts"]:
            continue
        if action.get("reduce_debt_payments") and not state["debts"]:
            continue
        if action.get("sell_asset_percent") and not state["assets"]:
            continue
        req_ed = action.get("requires_education", 0)
        if req_ed and state.get("education", 0) < req_ed:
            continue
        actions[key] = resolve_action_amounts(deepcopy(action), state)
    event["actions"] = actions or {"skip": {"label": "Pasar", "lesson": "Contexto", "interpretation": "Esta oportunidad no encaja con tu situacion actual."}}
    for action in event["actions"].values():
        action["risk_tags"] = action_risk_tags(state, action)
    return event


def action_risk_tags(state, action):
    simulated = deepcopy(state)
    apply_action_effects(simulated, action)
    normalize_state(simulated)
    data = metrics(simulated)
    tags = []
    if data["runway"] < 1:
        tags.append("Supervivencia critica")
    elif data["runway"] < 3:
        tags.append("Reserva baja")
    if data["debt_to_income"] > 0.4:
        tags.append("Sobreapalancamiento")
    if simulated["stress"] >= 85:
        tags.append("Riesgo de burnout")
    if simulated["cash"] < 0:
        tags.append("Caja negativa")
    return tags


def apply_monthly_cashflow(state):
    income = state["salary"] + risky_passive_income(state)
    outflow = state["expenses"] + debt_payments(state)
    net = income - outflow
    state["cash"] += net
    state["expenses"] = round(state["expenses"] * (1 + state["world"]["inflation"]), 2)
    accrue_debt_interest(state)
    if state["cash"] < 0:
        state["insolvent_months"] += 1
        state["stress"] += 4
        state["dangerous_moment"] = "Caja negativa durante varios meses"
    else:
        state["insolvent_months"] = 0
        if net > 0 and state["cash"] > 0:
            state["stress"] -= 2
            if state["stress"] > 60:
                state["stress"] -= 1


def risky_passive_income(state):
    total = 0
    education = state.get("education", 0)
    for asset in state.get("assets", []):
        a_income = asset.get("income", 0)
        risk = asset.get("risk", "")
        norm = max(0.0, 1 - education * 0.015)
        if risk == "vacancy" and random() < 0.08 * norm:
            asset_events_append(state, "vacancy", asset["name"])
            a_income = 0
        elif risk == "execution" and random() < 0.06 * norm:
            asset_events_append(state, "bad_month", asset["name"])
            a_income = round(a_income * 0.5, 2)
        elif risk == "high" and random() < 0.04 * norm:
            asset_events_append(state, "soft_bad", asset["name"])
            a_income = round(a_income * 0.7, 2)
        total += a_income
    return round(total, 2)


def asset_events_append(state, kind, label):
    state.setdefault("asset_events", []).append({"kind": kind, "label": label, "month": state.get("month", 0)})
    state["asset_events"] = state["asset_events"][-10:]


def apply_market_drift(state):
    world = state["world"]
    for asset in state["assets"]:
        if asset.get("type") == "Paper assets":
            drift = {"Expansion": 1.025, "Estable": 1.006, "Recesion": 0.94, "Recuperacion": 1.018}[world["name"]]
            asset["value"] = round(asset["value"] * drift, 2)
        elif asset.get("type") == "Real estate":
            drift = {"Expansion": 1.012, "Estable": 1.003, "Recesion": 0.985, "Recuperacion": 1.008}[world["name"]]
            asset["value"] = round(asset["value"] * drift, 2)
        elif asset.get("type") == "Small business":
            drift = {"Expansion": 1.03, "Estable": 1.005, "Recesion": 0.88, "Recuperacion": 1.02}[world["name"]]
            asset["value"] = round(asset["value"] * drift, 2)


def maybe_salary_shock(state):
    risk = state["world"]["income_risk"] * (1 - state["career_stability"] / 140)
    if random() < risk:
        loss = round(state["salary"] * 0.18, 2)
        state["salary"] -= loss
        state["stress"] += 6
        state["dangerous_moment"] = "Recorte de ingresos durante " + state["world"]["name"]
        asset_events_append(state, "salary_shock", "Recorte de ingresos (-$" + str(int(loss)) + ")")


def apply_action(state, action_id):
    if state.get("status") != "playing":
        return enrich_state(state)
    if not state.get("current_event"):
        start_month(state)
        return enrich_state(state)

    event = state["current_event"]
    action = event["actions"].get(action_id)
    if not action:
        state["last_feedback"] = feedback("Accion invalida", "Esa opcion no esta disponible.", "Revisa tus alternativas antes de decidir.")
        return enrich_state(state)

    state.pop("last_discretionary_feedback", None)
    before = metrics(state)
    before_snapshot = simple_snapshot(state)
    apply_action_effects(state, action)
    normalize_state(state)
    if action.get("quiet"):
        simulate_quiet_months(state, action.get("skip_months", 1))
    after = metrics(state)
    after_snapshot = simple_snapshot(state)
    impact = after["freedom_ratio"] - before["freedom_ratio"]
    state["last_feedback"] = build_feedback(action, before_snapshot, after_snapshot, before, after)
    update_decision_records(state, event, action, impact, before, after)
    state["history"].insert(0, {
        "month": state["month"],
        "age": display_age(state),
        "title": event["title"],
        "category": event["category"],
        "action": action["label"],
        "feedback": state["last_feedback"],
        "stress_after": state["stress"],
        "cash_after": state["cash"],
        "freedom_ratio_after": after["freedom_ratio"],
    })
    state["history"] = state["history"][:18]
    state["current_event"] = None
    check_end_conditions(state)
    if state["status"] == "playing":
        if action.get("quiet"):
            state["consecutive_quiet"] = 0
            state["current_event"] = pick_event(state)
        else:
            advance_time(state, action.get("skip_months", 1))
            check_end_conditions(state)
            if state["status"] == "playing":
                start_month(state)
    if state["status"] == "playing" and not state.get("current_event"):
        start_month(state)
    return enrich_state(state)


def advance_time(state, months=1):
    months = max(1, int(months))
    for _ in range(months):
        state["month"] += 1
        state["action_used_this_month"] = {"sell": False, "cut_expenses": False, "pay_debt": False}
        process_schedule(state)
        if state["month"] % 12 == 1 and state["month"] > 1:
            state["age"] += 1
            state["salary"] = round(state["salary"] * (1.025 + state["education"] * 0.007), 2)
            data = metrics(state)
            if data["freedom_ratio"] > 0.5:
                for asset in state.get("assets", []):
                    if asset.get("type") == "Paper assets" and asset.get("income", 0) > 0:
                        asset["income"] = round(asset["income"] * 1.05, 2)
            state.setdefault("history", []).insert(0, {
                "month": state["month"] - 1,
                "age": display_age(state),
                "title": f"Resumen año {(state['month'] - 1) // 12}",
                "category": "Summary",
                "action": f"Patrimonio ${data['net_worth']:,.0f} · Libertad {data['freedom_ratio']*100:.0f}%",
                "feedback": None,
            })
            state["history"] = state["history"][:18]


def process_schedule(state):
    if not state.get("schedule"):
        return
    due = [item for item in state["schedule"] if item["due_month"] <= state["month"]]
    if not due:
        return
    state["schedule"] = [item for item in state["schedule"] if item["due_month"] > state["month"]]
    applied = []
    for item in due:
        note = apply_delayed_effect(state, item)
        if note:
            applied.append(note)
    if applied:
        asset_events_append(state, "schedule_hit", "; ".join(applied))


def apply_delayed_effect(state, item):
    effect = item.get("effect", {})
    label = item.get("label", "Consecuencia programada")
    if "asset_fail_chance" in effect:
        spec = effect["asset_fail_chance"]
        asset = find_asset_by_name(state, spec.get("name"))
        if asset and random() < spec.get("prob", 1):
            asset["value"] = 0
            asset["income"] = 0
            asset_events_append(state, "asset_fail", asset["name"])
            return label
        return None
    if "asset_fail" in effect:
        asset = find_asset_by_name(state, effect["asset_fail"])
        if asset:
            asset["value"] = 0
            asset["income"] = 0
            asset_events_append(state, "asset_fail", asset["name"])
            return label
        return None
    if "asset_drop" in effect:
        asset = find_asset_by_name(state, effect["asset_drop"])
        if asset:
            asset["value"] = round(asset["value"] * (1 - effect.get("percent", 0.5)), 2)
            asset_events_append(state, "asset_drop", asset["name"])
            return label
        return None
    if "debt_rate_hike" in effect:
        debt = find_debt_by_name(state, effect["debt_rate_hike"])
        if debt:
            debt["rate"] = round(debt.get("rate", 0) + effect.get("delta", 0.02), 4)
            debt["payment"] = round(debt.get("payment", 0) * 1.06, 2)
            return label
        return None
    apply_action_effects(state, effect)
    return label


def find_asset_by_name(state, name):
    if not name:
        return None
    for asset in state.get("assets", []):
        if asset.get("name") == name:
            return asset
    return None


def find_debt_by_name(state, name):
    if not name:
        return None
    for debt in state.get("debts", []):
        if debt.get("name") == name:
            return debt
    if state.get("debts"):
        return max(state["debts"], key=lambda d: d.get("balance", 0))
    return None


def check_end_conditions(state):
    data = metrics(state)
    if data["freedom_ratio"] >= 1 and data["runway"] >= 6:
        state["status"] = "won"
        state["outcome"] = "Financially free"
        state["last_feedback"] = feedback("Libertad financiera conseguida", "Tus ingresos pasivos cubren obligaciones y tu reserva aguanta meses malos.", "La libertad sostenible combina flujo y liquidez.")
    elif state["insolvent_months"] >= 3 and data["cashflow"] < 0:
        state["status"] = "lost"
        state["outcome"] = "Debt trapped"
        state["last_feedback"] = feedback("Insolvencia", "La caja negativa se mantuvo demasiado tiempo y tus pagos mensuales siguieron corriendo.", "La fragilidad mata antes que la falta de ambicion.")
    elif state["stress"] >= 99:
        state["status"] = "ended"
        state["outcome"] = "Burnout retirement"
        state["last_feedback"] = feedback("Burnout financiero", "El plan producia dinero, pero destruyo la capacidad de sostenerlo.", "Una estrategia que no cuida energia no es sostenible.")
    elif state["month"] > 240:
        state["status"] = "ended"
        state["outcome"] = partial_outcome(state)
        state["last_feedback"] = feedback("Fin de simulacion", "La vida financiera siguio su curso. El resultado muestra tu patron dominante.", "No todo final es victoria o colapso; muchos resultados son compromisos.")


def partial_outcome(state):
    data = metrics(state)
    if data["freedom_ratio"] >= 0.75 and data["runway"] < 3:
        return "High net worth, low liquidity"
    if data["cashflow"] > 1200 and state["stress"] > 75:
        return "High income, high stress"
    if data["debt_to_income"] > 0.42:
        return "Debt trapped"
    if data["freedom_ratio"] >= 0.65:
        return "Slow conservative success"
    if len([asset for asset in state["assets"] if asset.get("type") == "Small business"]) >= 2:
        return "Business success"
    if data["runway"] >= 6 and data["cashflow"] > 0:
        return "Stable but not free"
    return "Compromised middle path"
