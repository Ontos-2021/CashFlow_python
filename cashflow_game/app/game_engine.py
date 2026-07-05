from copy import deepcopy
from random import choice


PROFESSIONS = {
    "administrativo": {
        "name": "Empleado administrativo",
        "summary": "Estabilidad razonable, crecimiento lento y margen de ahorro limitado.",
        "age": 26,
        "cash": 1800,
        "salary": 2200,
        "expenses": 1550,
        "education": 1,
        "stress": 28,
        "credit_score": 660,
        "debts": [
            {"name": "Tarjeta de credito", "balance": 2400, "payment": 120, "rate": 0.32}
        ],
    },
    "programador": {
        "name": "Programador",
        "summary": "Buen ingreso, alta empleabilidad y riesgo de subir gastos demasiado rapido.",
        "age": 25,
        "cash": 4500,
        "salary": 4200,
        "expenses": 2600,
        "education": 2,
        "stress": 35,
        "credit_score": 710,
        "debts": [
            {"name": "Prestamo estudiantil", "balance": 12000, "payment": 260, "rate": 0.09}
        ],
    },
    "docente": {
        "name": "Docente",
        "summary": "Ingreso moderado, gastos controlados y buena estabilidad laboral.",
        "age": 28,
        "cash": 2600,
        "salary": 2500,
        "expenses": 1700,
        "education": 2,
        "stress": 24,
        "credit_score": 690,
        "debts": [],
    },
    "medico": {
        "name": "Medico joven",
        "summary": "Ingreso alto, deuda alta y estilo de vida costoso.",
        "age": 30,
        "cash": 6000,
        "salary": 7200,
        "expenses": 4700,
        "education": 2,
        "stress": 48,
        "credit_score": 700,
        "debts": [
            {"name": "Prestamo estudiantil", "balance": 85000, "payment": 980, "rate": 0.08},
            {"name": "Auto financiado", "balance": 18000, "payment": 420, "rate": 0.12},
        ],
    },
    "vendedor": {
        "name": "Vendedor",
        "summary": "Ingreso variable, alto potencial y necesidad de reservas.",
        "age": 27,
        "cash": 2200,
        "salary": 3300,
        "expenses": 2300,
        "education": 1,
        "stress": 40,
        "credit_score": 640,
        "debts": [
            {"name": "Tarjeta de credito", "balance": 5200, "payment": 210, "rate": 0.34}
        ],
    },
    "freelancer": {
        "name": "Freelancer creativo",
        "summary": "Flexibilidad alta, ingresos inestables y potencial de crear activos propios.",
        "age": 24,
        "cash": 1400,
        "salary": 2800,
        "expenses": 1850,
        "education": 1,
        "stress": 44,
        "credit_score": 620,
        "debts": [
            {"name": "Equipo financiado", "balance": 3600, "payment": 160, "rate": 0.18}
        ],
    },
}


WORLD_STATES = [
    {"name": "Expansion", "inflation": 0.004, "risk": "bajo", "description": "Credito accesible y activos caros."},
    {"name": "Estable", "inflation": 0.003, "risk": "medio", "description": "Mercados equilibrados y oportunidades razonables."},
    {"name": "Recesion", "inflation": 0.001, "risk": "alto", "description": "Activos baratos, ingresos mas fragiles y credito exigente."},
    {"name": "Recuperacion", "inflation": 0.002, "risk": "medio", "description": "El mercado mejora y aparecen oportunidades subvaloradas."},
]


EVENTS = [
    {
        "id": "index_fund",
        "category": "Inversion",
        "title": "Fondo indexado diversificado",
        "description": "Podrias invertir en un fondo amplio de mercado con alta liquidez y volatilidad moderada.",
        "actions": {
            "invest": {
                "label": "Invertir $1.500",
                "cash": -1500,
                "asset": {"name": "Fondo indexado", "type": "Activos financieros", "value": 1500, "income": 12},
                "lesson": "Los fondos diversificados suelen priorizar crecimiento gradual y liquidez sobre flujo inmediato.",
            },
            "skip": {"label": "Mantener efectivo", "lesson": "Conservar liquidez tambien es una decision valida cuando tu reserva es baja."},
        },
    },
    {
        "id": "small_apartment",
        "category": "Inmuebles",
        "title": "Departamento pequeno con renta",
        "description": "Un vendedor necesita liquidez. La propiedad requiere entrada, pero genera flujo positivo.",
        "actions": {
            "buy": {
                "label": "Comprar con $8.000 de entrada",
                "cash": -8000,
                "asset": {"name": "Departamento pequeno", "type": "Inmueble", "value": 78000, "income": 260},
                "debt": {"name": "Hipoteca departamento", "balance": 70000, "payment": 640, "rate": 0.07},
                "stress": 5,
                "lesson": "El apalancamiento puede acelerar tu flujo, pero reduce liquidez y aumenta obligaciones fijas.",
            },
            "analyze": {
                "label": "Analizar y negociar",
                "education": 1,
                "stress": -2,
                "lesson": "Analizar antes de comprar mejora tu criterio. No toda oportunidad requiere accion inmediata.",
            },
            "skip": {"label": "Pasar", "lesson": "Evitar una inversion que no podes sostener protege tu supervivencia financiera."},
        },
    },
    {
        "id": "side_business",
        "category": "Negocio",
        "title": "Pequeno negocio digital",
        "description": "Tenes la chance de lanzar un producto simple. Requiere capital, tiempo y tolerancia al riesgo.",
        "actions": {
            "launch": {
                "label": "Invertir $3.000 y lanzar",
                "cash": -3000,
                "asset": {"name": "Negocio digital", "type": "Negocio", "value": 5000, "income": 380},
                "stress": 8,
                "lesson": "Los negocios pueden crear flujo importante, pero suelen exigir energia y ejecucion constante.",
            },
            "learn": {
                "label": "Estudiar el mercado primero",
                "cash": -500,
                "education": 1,
                "lesson": "Invertir en conocimiento antes de emprender reduce errores caros.",
            },
            "skip": {"label": "No emprender ahora", "lesson": "Decir no permite conservar foco, efectivo y energia."},
        },
    },
    {
        "id": "credit_card_attack",
        "category": "Deuda",
        "title": "Plan para destruir deuda cara",
        "description": "Tu tarjeta consume flujo de caja. Podes hacer un pago agresivo o seguir pagando minimo.",
        "actions": {
            "paydown": {
                "label": "Pagar $1.000 extra",
                "cash": -1000,
                "pay_debt": 1000,
                "credit_score": 10,
                "lesson": "Reducir deuda de alto interes suele tener un retorno ajustado por riesgo excelente.",
            },
            "minimum": {
                "label": "Pagar solo minimo",
                "stress": 3,
                "lesson": "El pago minimo conserva efectivo hoy, pero puede extender deuda cara durante anos.",
            },
        },
    },
    {
        "id": "emergency",
        "category": "Emergencia",
        "title": "Gasto medico inesperado",
        "description": "Aparece un gasto no planificado. Tu fondo de emergencia define si esto es molestia o crisis.",
        "actions": {
            "pay": {
                "label": "Pagar $1.200",
                "cash": -1200,
                "stress": 6,
                "lesson": "La liquidez no parece rentable hasta que evita deuda cara en una emergencia.",
            },
            "finance": {
                "label": "Financiar con prestamo personal",
                "debt": {"name": "Prestamo emergencia", "balance": 1200, "payment": 95, "rate": 0.24},
                "stress": 10,
                "lesson": "Financiar emergencias protege caja inmediata, pero agrega pagos futuros y presion mental.",
            },
        },
    },
    {
        "id": "course",
        "category": "Educacion",
        "title": "Curso de analisis financiero",
        "description": "Un curso practico promete ayudarte a evaluar inversiones con mejores metricas.",
        "actions": {
            "buy": {
                "label": "Invertir $700",
                "cash": -700,
                "education": 1,
                "lesson": "La educacion financiera de calidad mejora la calidad de tus proximas decisiones.",
            },
            "skip": {"label": "No comprar", "lesson": "No todo curso es urgente. El costo de oportunidad tambien importa."},
        },
    },
    {
        "id": "lifestyle_car",
        "category": "Doodad",
        "title": "Auto nuevo financiado",
        "description": "La cuota entra en tu presupuesto, pero no genera ingresos y sube tus gastos fijos.",
        "actions": {
            "buy": {
                "label": "Financiar el auto",
                "debt": {"name": "Auto nuevo", "balance": 16000, "payment": 390, "rate": 0.14},
                "expenses": 120,
                "stress": 6,
                "lesson": "Una compra puede ser accesible por cuota y aun asi alejarte de la libertad financiera.",
            },
            "skip": {
                "label": "Conservar tu auto actual",
                "stress": -2,
                "lesson": "Evitar inflacion de estilo de vida mantiene tu flujo disponible para activos.",
            },
        },
    },
    {
        "id": "raise",
        "category": "Trabajo",
        "title": "Oferta de ascenso",
        "description": "Podrias ganar mas, aunque el cargo suma responsabilidad y estres.",
        "actions": {
            "accept": {
                "label": "Aceptar ascenso",
                "salary": 450,
                "stress": 7,
                "lesson": "Aumentar ingreso activo ayuda, pero no reemplaza la construccion de activos.",
            },
            "decline": {
                "label": "Rechazar y cuidar energia",
                "stress": -5,
                "lesson": "Optimizar vida financiera tambien implica proteger salud y capacidad de decidir.",
            },
        },
    },
    {
        "id": "market_drop",
        "category": "Mercado",
        "title": "Correccion del mercado",
        "description": "Los activos financieros caen. Puede doler si ya invertiste, o ser oportunidad si tenes caja.",
        "actions": {
            "buy": {
                "label": "Comprar barato por $1.000",
                "cash": -1000,
                "asset": {"name": "Compra en correccion", "type": "Activos financieros", "value": 1200, "income": 10},
                "lesson": "Las crisis favorecen a quien llega con liquidez y plan.",
            },
            "panic": {
                "label": "Vender por miedo",
                "sell_asset_percent": 0.2,
                "stress": 4,
                "lesson": "Vender por panico convierte volatilidad temporal en perdida permanente.",
            },
            "hold": {"label": "No tocar nada", "lesson": "A veces la mejor decision es no reaccionar al ruido del mercado."},
        },
    },
]


def profession_choices():
    return [{"id": key, **value} for key, value in PROFESSIONS.items()]


def new_game(profession_id):
    profession = deepcopy(PROFESSIONS[profession_id])
    state = {
        "profession_id": profession_id,
        "profession": profession["name"],
        "profession_summary": profession["summary"],
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
        "world": WORLD_STATES[1],
        "current_event": None,
        "last_feedback": "Bienvenido. Tu objetivo es que tus ingresos pasivos cubran tus gastos y tener 6 meses de reserva.",
        "best_decision": None,
        "worst_decision": None,
        "insolvent_months": 0,
    }
    start_month(state)
    return enrich_state(state)


def start_month(state):
    state["world"] = choice(WORLD_STATES)
    apply_monthly_cashflow(state)
    event = deepcopy(choice(EVENTS))
    state["current_event"] = event
    return state


def apply_monthly_cashflow(state):
    income = state["salary"] + passive_income(state)
    outflow = state["expenses"] + debt_payments(state)
    state["cash"] += income - outflow
    state["expenses"] = round(state["expenses"] * (1 + state["world"]["inflation"]), 2)
    accrue_debt_interest(state)
    if state["cash"] < 0:
        state["insolvent_months"] += 1
        state["stress"] += 8
    else:
        state["insolvent_months"] = 0


def apply_action(state, action_id):
    if state.get("status") != "playing" or not state.get("current_event"):
        return enrich_state(state)

    event = state["current_event"]
    action = event["actions"].get(action_id)
    if not action:
        state["last_feedback"] = "Esa accion no esta disponible."
        return enrich_state(state)

    before = metrics(state)
    state["cash"] += action.get("cash", 0)
    state["salary"] += action.get("salary", 0)
    state["expenses"] += action.get("expenses", 0)
    state["education"] += action.get("education", 0)
    state["stress"] += action.get("stress", 0)
    state["credit_score"] += action.get("credit_score", 0)

    if action.get("asset"):
        state["assets"].append(deepcopy(action["asset"]))
    if action.get("debt"):
        state["debts"].append(deepcopy(action["debt"]))
    if action.get("pay_debt"):
        pay_down_debt(state, action["pay_debt"])
    if action.get("sell_asset_percent"):
        sell_assets(state, action["sell_asset_percent"])

    normalize_state(state)
    after = metrics(state)
    impact = after["freedom_ratio"] - before["freedom_ratio"]
    feedback = build_feedback(event, action, before, after)
    state["last_feedback"] = feedback
    update_decision_records(state, event, action, impact)
    state["history"].insert(0, {
        "month": state["month"],
        "age": display_age(state),
        "title": event["title"],
        "action": action["label"],
        "feedback": feedback,
    })
    state["history"] = state["history"][:12]
    state["current_event"] = None
    advance_time(state)
    check_end_conditions(state)
    if state["status"] == "playing":
        start_month(state)
    return enrich_state(state)


def advance_time(state):
    state["month"] += 1
    if state["month"] % 12 == 1 and state["month"] > 1:
        state["age"] += 1
        state["salary"] = round(state["salary"] * 1.025, 2)


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


def metrics(state):
    obligations = monthly_obligations(state)
    passive = passive_income(state)
    net_worth = state["cash"] + asset_value(state) - debt_balance(state)
    cashflow = state["salary"] + passive - obligations
    return {
        "passive_income": passive,
        "debt_payments": debt_payments(state),
        "debt_balance": debt_balance(state),
        "asset_value": asset_value(state),
        "monthly_obligations": obligations,
        "cashflow": round(cashflow, 2),
        "net_worth": round(net_worth, 2),
        "freedom_ratio": round((passive / obligations) if obligations else 0, 3),
        "runway": round((state["cash"] / obligations) if obligations else 99, 1),
    }


def enrich_state(state):
    state = deepcopy(state)
    state["metrics"] = metrics(state)
    state["display_age"] = display_age(state)
    state["investor_profile"] = investor_profile(state)
    return state


def display_age(state):
    years = state["age"]
    months = (state["month"] - 1) % 12
    return f"{years} anos" if months == 0 else f"{years} anos y {months} meses"


def normalize_state(state):
    state["stress"] = max(0, min(100, round(state["stress"])))
    state["education"] = max(0, min(10, state["education"]))
    state["credit_score"] = max(300, min(850, state["credit_score"]))


def accrue_debt_interest(state):
    for debt in state["debts"]:
        monthly_rate = debt.get("rate", 0) / 12
        debt["balance"] = max(0, round(debt["balance"] * (1 + monthly_rate) - debt.get("payment", 0), 2))
    state["debts"] = [debt for debt in state["debts"] if debt["balance"] > 1]


def pay_down_debt(state, amount):
    remaining = amount
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


def build_feedback(event, action, before, after):
    freedom_delta = round((after["freedom_ratio"] - before["freedom_ratio"]) * 100, 1)
    cash_delta = round(after["cashflow"] - before["cashflow"], 2)
    return (
        f"{action['lesson']} Impacto: ratio de libertad {freedom_delta:+}% "
        f"y flujo mensual {cash_delta:+}."
    )


def update_decision_records(state, event, action, impact):
    record = f"{event['title']}: {action['label']}"
    if impact >= 0.05:
        state["best_decision"] = record
    if impact <= -0.05 or state["cash"] < 0:
        state["worst_decision"] = record


def check_end_conditions(state):
    data = metrics(state)
    if data["freedom_ratio"] >= 1 and data["runway"] >= 6:
        state["status"] = "won"
        state["last_feedback"] = "Lograste libertad financiera sostenible: ingresos pasivos cubren obligaciones y tenes reserva suficiente."
    elif state["insolvent_months"] >= 4:
        state["status"] = "lost"
        state["last_feedback"] = "Tu caja fue negativa demasiados meses seguidos. La partida termina en insolvencia."
    elif state["month"] > 360:
        state["status"] = "ended"
        state["last_feedback"] = "Llegaste al final de la simulacion de 30 anos. Revisa tu reporte financiero."


def investor_profile(state):
    data = metrics(state)
    if data["freedom_ratio"] >= 1 and data["runway"] >= 6:
        return "Arquitecto de libertad"
    if passive_income(state) > state["salary"] * 0.5:
        return "Constructor de activos"
    if debt_balance(state) > asset_value(state) and state["stress"] > 60:
        return "Sobreviviente financiero"
    if len([asset for asset in state["assets"] if asset["type"] == "Negocio"]) >= 2:
        return "Emprendedor agresivo"
    if data["runway"] >= 6:
        return "Inversor prudente"
    return "Aprendiz financiero"
