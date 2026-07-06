from copy import deepcopy

from .metrics import asset_value, debt_balance, display_age, metrics, session_phase


def enrich_state(state):
    state = deepcopy(state)
    state["metrics"] = metrics(state)
    state["display_age"] = display_age(state)
    state["investor_profile"] = investor_profile(state)
    state["phase"] = session_phase(state)
    state["status_badges"] = status_badges(state)
    state["alerts"] = contextual_alerts(state)
    return state


def feedback(title, interpretation, lesson, changes=None, alerts=None, badges=None):
    return {"title": title, "changes": changes or [], "interpretation": interpretation, "lesson": lesson, "alerts": alerts or [], "badges": badges or []}


def build_feedback(action, before_snapshot, after_snapshot, before, after):
    fields = [
        ("Cash", "cash", "$"),
        ("Passive income", "passive_income", "$"),
        ("Runway", "runway", " months"),
        ("Stress", "stress", ""),
        ("Monthly cash flow", "cashflow", "$"),
        ("Debt balance", "debt_balance", "$"),
    ]
    changes = []
    for label, key, suffix in fields:
        delta = round(after_snapshot[key] - before_snapshot[key], 2)
        if abs(delta) >= 0.1:
            if suffix == "$":
                changes.append(f"{label}: {delta:+,.0f}")
            elif suffix == " months":
                changes.append(f"{label}: {delta:+.1f} months")
            else:
                changes.append(f"{label}: {delta:+.0f}")
    ratio_delta = round((after["freedom_ratio"] - before["freedom_ratio"]) * 100, 1)
    if abs(ratio_delta) >= 0.1:
        changes.append(f"Freedom ratio: {ratio_delta:+.1f}%")
    alerts = next_risk_alerts(after_snapshot, after)
    badges = unlocked_badges(before, after)
    scheduled = action.get("delayed", [])
    for entry in scheduled:
        changes.append(f"Programado · {entry.get('label', 'Consecuencia')} · en {entry.get('delay', 1)} meses")
    return feedback("Decision aplicada", action.get("interpretation", "Tu estado financiero cambio."), action.get("lesson", "Consecuencia financiera"), changes, alerts, badges)


def next_risk_alerts(snapshot, data):
    alerts = []
    if snapshot["stress"] >= 85:
        alerts.append("Tu estres esta en zona roja. Una decision mas exigente puede terminar la partida por burnout.")
    if data["runway"] < 1:
        alerts.append("Tu reserva no cubre un mes completo. Cualquier shock puede forzar deuda o insolvencia.")
    if data["debt_to_income"] > 0.42:
        alerts.append("Tus pagos de deuda consumen demasiado ingreso. Perdiste flexibilidad.")
    if data["opportunity_readiness"] >= 80:
        alerts.append("Estas preparado para oportunidades grandes: buena caja, baja presion y margen de decision.")
    return alerts


def unlocked_badges(before, after):
    badges = []
    if before["debt_balance"] > 0 and after["debt_balance"] == 0:
        badges.append("Debt Free")
    if before["runway"] < 6 <= after["runway"]:
        badges.append("Emergency Fund")
    if before["freedom_ratio"] < 0.5 <= after["freedom_ratio"]:
        badges.append("Halfway to Freedom")
    if before["freedom_ratio"] < 1 <= after["freedom_ratio"]:
        badges.append("Financially Independent")
    return badges


def status_badges(state):
    data = metrics(state)
    badges = [{"label": data["financial_state"], "kind": state_badge_kind(data["financial_state"])}]
    if not state["debts"]:
        badges.append({"label": "Debt Free", "kind": "good"})
    if not state["assets"]:
        badges.append({"label": "100% Active Income", "kind": "warning"})
    if data["runway"] >= 6:
        badges.append({"label": "Emergency Fund", "kind": "good"})
    if data["opportunity_readiness"] >= 80:
        badges.append({"label": "Opportunity Ready", "kind": "good"})
    if data["debt_to_income"] > 0.42:
        badges.append({"label": "Overleveraged", "kind": "danger"})
    return badges


def state_badge_kind(label):
    if label in {"Safe", "Debt Free Builder"}:
        return "good"
    if label in {"Critical", "Burnout Risk", "Overleveraged"}:
        return "danger"
    if label == "Tense":
        return "warning"
    return "neutral"


def contextual_alerts(state):
    data = metrics(state)
    alerts = []
    if state["stress"] >= 85:
        alerts.append({"title": "Riesgo de burnout", "message": "Tu energia esta en zona roja. Descansar, delegar o bajar obligaciones puede ser una jugada ganadora.", "kind": "danger"})
    elif state["stress"] >= 70:
        alerts.append({"title": "Tension alta", "message": "Todavia podes avanzar, pero cada decision exigente reduce tu margen humano.", "kind": "warning"})
    if state["cash"] < 0:
        alerts.append({"title": "Caja negativa", "message": "Estas financiando la vida diaria. Si esto dura, la partida puede terminar en insolvencia.", "kind": "danger"})
    elif data["runway"] < 1:
        alerts.append({"title": "Supervivencia critica", "message": "Tu reserva no cubre un mes. Liquidez primero, crecimiento despues.", "kind": "danger"})
    elif data["runway"] < 3:
        alerts.append({"title": "Reserva baja", "message": "Podes jugar oportunidades, pero un shock te deja sin defensa.", "kind": "warning"})
    if not state["debts"]:
        alerts.append({"title": "Libre de deuda", "message": "Tu flujo no tiene acreedores. El nuevo desafio es construir activos sin perder esa libertad.", "kind": "good"})
    if not state["assets"]:
        alerts.append({"title": "Dependes del salario", "message": "Si tu ingreso activo falla, no hay activos trabajando por vos todavia.", "kind": "warning"})
    return alerts[:3]


def investor_profile(state):
    data = metrics(state)
    business_count = len([asset for asset in state["assets"] if asset.get("type") == "Small business"])
    real_estate_count = len([asset for asset in state["assets"] if asset.get("type") == "Real estate"])
    if data["freedom_ratio"] >= 1 and data["runway"] >= 6:
        return "Cash Flow Strategist"
    if data["debt_to_income"] > 0.45 and real_estate_count >= 1:
        return "Aggressive Leverager"
    if data["runway"] >= 9 and data["asset_income_ratio"] < 0.15:
        return "Conservative Builder"
    if data["asset_income_ratio"] >= 0.35:
        return "Patient Investor"
    if business_count >= 2:
        return "Opportunity Hunter"
    if state["salary"] > 5500 and data["freedom_ratio"] < 0.25 and data["lifestyle_inflation"] > 0.25:
        return "High-Income Spender"
    if data["insolvency_risk"] > 70:
        return "Overextended Optimist"
    if state["stress"] > 82 and data["cashflow"] > 0:
        return "Burnout Achiever"
    if debt_balance(state) > asset_value(state):
        return "Debt Survivor"
    return "Balanced Capitalist"
