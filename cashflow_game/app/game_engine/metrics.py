def passive_income(state):
    return round(sum(asset.get("income", 0) for asset in state["assets"]), 2)


def debt_payments(state):
    return round(sum(debt.get("payment", 0) for debt in state["debts"]), 2)


def debt_balance(state):
    return round(sum(debt.get("balance", 0) for debt in state["debts"]), 2)


def asset_value(state):
    return round(sum(asset.get("value", 0) for asset in state["assets"]), 2)


def monthly_obligations(state):
    return round(state["expenses"] + debt_payments(state), 2)


def display_age(state):
    years = state["age"]
    months = (state["month"] - 1) % 12
    return f"{years} anos" if months == 0 else f"{years} anos y {months} meses"


def session_phase(state):
    ratio = metrics(state)["freedom_ratio"] if state.get("assets") or state.get("debts") else 0
    if state["month"] <= 24 or ratio < 0.15:
        return "survival"
    if ratio < 0.75:
        return "growth"
    return "freedom"


def financial_state_label(state, runway, cashflow, debt_to_income):
    if state["stress"] >= 85:
        return "Burnout Risk"
    if state["cash"] < 0 or runway < 1:
        return "Critical"
    if debt_to_income > 0.42:
        return "Overleveraged"
    if runway < 3:
        return "Tense"
    if runway >= 6 and cashflow > 0 and not state["debts"]:
        return "Debt Free Builder"
    if runway >= 6 and cashflow > 0:
        return "Safe"
    return "Stable"


def calculate_insolvency_risk(state, runway, cashflow, debt_to_income):
    score = 0
    if runway < 1:
        score += 45
    elif runway < 3:
        score += 25
    elif runway < 6:
        score += 10
    if cashflow < 0:
        score += 30
    if debt_to_income > 0.35:
        score += 18
    if state["stress"] > 75:
        score += 12
    return min(100, score)


def calculate_opportunity_readiness(state, runway, debt_to_income):
    score = 35 + min(35, max(0, runway) * 4) + state["education"] * 6 + max(0, state["credit_score"] - 600) / 12
    score -= debt_to_income * 55
    score -= max(0, state["stress"] - 55) * 0.5
    return round(max(0, min(100, score)))


def metrics(state):
    obligations = monthly_obligations(state)
    passive = passive_income(state)
    debt_pay = debt_payments(state)
    debt_bal = debt_balance(state)
    assets = asset_value(state)
    total_income = state["salary"] + passive
    net_worth = state["cash"] + assets - debt_bal
    cashflow = total_income - obligations
    debt_to_income = debt_pay / total_income if total_income else 0
    asset_income_ratio = passive / total_income if total_income else 0
    lifestyle = max(0, (state["expenses"] - state.get("starting_expenses", state["expenses"])) / max(state.get("starting_expenses", 1), 1))
    runway = state["cash"] / obligations if obligations else 99
    insolvency_risk = calculate_insolvency_risk(state, runway, cashflow, debt_to_income)
    readiness = calculate_opportunity_readiness(state, runway, debt_to_income)
    return {
        "passive_income": passive,
        "debt_payments": debt_pay,
        "debt_balance": debt_bal,
        "asset_value": assets,
        "monthly_obligations": obligations,
        "total_income": round(total_income, 2),
        "cashflow": round(cashflow, 2),
        "net_worth": round(net_worth, 2),
        "freedom_ratio": round((passive / obligations) if obligations else 0, 3),
        "runway": round(runway, 1),
        "debt_to_income": round(debt_to_income, 3),
        "asset_income_ratio": round(asset_income_ratio, 3),
        "lifestyle_inflation": round(lifestyle, 3),
        "insolvency_risk": insolvency_risk,
        "opportunity_readiness": readiness,
        "financial_state": financial_state_label(state, runway, cashflow, debt_to_income),
    }


def simple_snapshot(state):
    data = metrics(state)
    return {
        "cash": round(state["cash"], 2),
        "passive_income": data["passive_income"],
        "runway": data["runway"],
        "stress": state["stress"],
        "cashflow": data["cashflow"],
        "freedom_ratio": data["freedom_ratio"],
        "debt_balance": data["debt_balance"],
    }
