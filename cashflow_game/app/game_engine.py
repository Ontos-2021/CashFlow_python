from copy import deepcopy
from random import choice, random


PROFESSIONS = {
    "administrativo": {
        "name": "Empleado administrativo",
        "summary": "Estabilidad razonable, crecimiento lento y margen de ahorro limitado.",
        "risk_profile": "Conservador forzado",
        "career_stability": 82,
        "age": 26,
        "cash": 1800,
        "salary": 2200,
        "expenses": 1550,
        "education": 1,
        "stress": 28,
        "credit_score": 660,
        "debts": [{"name": "Tarjeta de credito", "type": "Credit card", "balance": 2400, "payment": 120, "rate": 0.32, "stress": 8}],
    },
    "programador": {
        "name": "Programador",
        "summary": "Buen ingreso, alta empleabilidad y riesgo de subir gastos demasiado rapido.",
        "risk_profile": "Optimizador tecnico",
        "career_stability": 74,
        "age": 25,
        "cash": 4500,
        "salary": 4200,
        "expenses": 2600,
        "education": 2,
        "stress": 35,
        "credit_score": 710,
        "debts": [{"name": "Prestamo estudiantil", "type": "Student loan", "balance": 12000, "payment": 260, "rate": 0.09, "stress": 4}],
    },
    "docente": {
        "name": "Docente",
        "summary": "Ingreso moderado, gastos controlados y buena estabilidad laboral.",
        "risk_profile": "Planificador paciente",
        "career_stability": 88,
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
        "risk_profile": "Alto ingreso diferido",
        "career_stability": 86,
        "age": 30,
        "cash": 6000,
        "salary": 7200,
        "expenses": 4700,
        "education": 2,
        "stress": 48,
        "credit_score": 700,
        "debts": [
            {"name": "Prestamo estudiantil", "type": "Student loan", "balance": 85000, "payment": 980, "rate": 0.08, "stress": 8},
            {"name": "Auto financiado", "type": "Auto loan", "balance": 18000, "payment": 420, "rate": 0.12, "stress": 6},
        ],
    },
    "vendedor": {
        "name": "Vendedor",
        "summary": "Ingreso variable, alto potencial y necesidad de reservas.",
        "risk_profile": "Cazador de upside",
        "career_stability": 48,
        "age": 27,
        "cash": 2200,
        "salary": 3300,
        "expenses": 2300,
        "education": 1,
        "stress": 40,
        "credit_score": 640,
        "debts": [{"name": "Tarjeta de credito", "type": "Credit card", "balance": 5200, "payment": 210, "rate": 0.34, "stress": 10}],
    },
    "freelancer": {
        "name": "Freelancer creativo",
        "summary": "Flexibilidad alta, ingresos inestables y potencial de crear activos propios.",
        "risk_profile": "Constructor independiente",
        "career_stability": 42,
        "age": 24,
        "cash": 1400,
        "salary": 2800,
        "expenses": 1850,
        "education": 1,
        "stress": 44,
        "credit_score": 620,
        "debts": [{"name": "Equipo financiado", "type": "Personal loan", "balance": 3600, "payment": 160, "rate": 0.18, "stress": 5}],
    },
}


WORLD_STATES = [
    {"name": "Expansion", "inflation": 0.005, "asset_price": 1.08, "income_risk": 0.02, "credit": 1.15, "description": "Credito accesible, empleos fuertes y activos caros."},
    {"name": "Estable", "inflation": 0.003, "asset_price": 1.0, "income_risk": 0.04, "credit": 1.0, "description": "Mercados equilibrados y oportunidades razonables."},
    {"name": "Recesion", "inflation": 0.001, "asset_price": 0.86, "income_risk": 0.11, "credit": 0.72, "description": "Activos baratos, ingresos fragiles y credito exigente."},
    {"name": "Recuperacion", "inflation": 0.002, "asset_price": 0.94, "income_risk": 0.06, "credit": 0.92, "description": "El mercado mejora y aparecen oportunidades subvaloradas."},
]


BASE_EVENTS = [
    {
        "id": "index_fund",
        "category": "Investment",
        "phase": "survival",
        "title": "Fondo indexado diversificado",
        "description": "El mercado ofrece una entrada razonable a un fondo amplio. Es liquido, aburrido y dificil de presumir.",
        "actions": {
            "invest": {"label": "Invertir $1.500", "cash": -1500, "asset": {"name": "Fondo indexado", "type": "Paper assets", "value": 1500, "income": 12, "risk": "market"}, "lesson": "Diversificacion", "interpretation": "Compraste tiempo y exposicion amplia, no emocion. El progreso lento suele ser el mas repetible."},
            "wait": {"label": "Esperar y proteger caja", "stress": -1, "lesson": "Liquidez", "interpretation": "No invertir tambien es una posicion. La liquidez compra calma y opciones."},
            "speculate": {"label": "Buscar una accion caliente", "cash": -900, "asset": {"name": "Accion especulativa", "type": "Paper assets", "value": 650, "income": 0, "risk": "high"}, "stress": 5, "lesson": "Riesgo concentrado", "interpretation": "La historia era emocionante. El margen de seguridad era pequeno."},
        },
    },
    {
        "id": "small_apartment",
        "category": "Investment",
        "phase": "growth",
        "title": "Departamento pequeno con renta",
        "description": "Un vendedor necesita liquidez. La propiedad tiene flujo positivo, pero la entrada usa gran parte de tu caja.",
        "actions": {
            "buy": {"label": "Comprar con $8.000 de entrada", "cash": -8000, "asset": {"name": "Departamento pequeno", "type": "Real estate", "value": 78000, "income": 260, "risk": "vacancy"}, "debt": {"name": "Hipoteca departamento", "type": "Mortgage", "balance": 70000, "payment": 640, "rate": 0.07, "stress": 8}, "stress": 6, "lesson": "Apalancamiento", "interpretation": "El flujo mejora, pero tus obligaciones fijas tambien. La deuda no perdona meses malos."},
            "negotiate": {"label": "Negociar y estudiar", "cash": -250, "education": 1, "stress": -2, "lesson": "Analisis", "interpretation": "Comprar mejor empieza antes de firmar. Aprender a analizar evita anos de pagos incomodos."},
            "skip": {"label": "Pasar por falta de reserva", "stress": -1, "lesson": "Margen de seguridad", "interpretation": "A veces una buena inversion es mala para tu momento financiero."},
        },
    },
    {
        "id": "side_business",
        "category": "Investment",
        "phase": "growth",
        "title": "Pequeno negocio digital",
        "description": "Puedes lanzar un producto simple. Requiere capital, energia y tolerancia a que nadie compre al principio.",
        "actions": {
            "launch": {"label": "Invertir $3.000 y lanzar", "cash": -3000, "asset": {"name": "Negocio digital", "type": "Small business", "value": 5000, "income": 380, "risk": "execution"}, "stress": 10, "lesson": "Activos construidos", "interpretation": "Los negocios pueden crear flujo, pero te cobran en incertidumbre y energia.", "delayed": [{"delay": 12, "label": "Negocio en bache (-40%)", "source": "Pequeno negocio digital", "effect": {"asset_drop": "Negocio digital", "percent": 0.4}}]},
            "validate": {"label": "Validar con $600", "cash": -600, "education": 1, "stress": 2, "lesson": "Validacion", "interpretation": "Pagar por informacion pequena antes de apostar fuerte puede salvar capital."},
            "ignore": {"label": "No emprender ahora", "stress": -3, "lesson": "Foco", "interpretation": "No toda oportunidad merece atencion. El foco tambien es un activo."},
        },
    },
    {
        "id": "credit_card_attack",
        "category": "Debt",
        "phase": "survival",
        "requires_debt": True,
        "title": "Plan para destruir deuda cara",
        "description": "La tarjeta consume flujo de caja. Podes atacar capital o seguir respirando con pago minimo.",
        "actions": {
            "paydown": {"label": "Pagar $1.000 extra", "cash": -1000, "pay_debt": 1000, "credit_score": 10, "stress": -4, "lesson": "Retorno garantizado", "interpretation": "Reducir deuda cara mejora tu futuro sin necesitar suerte de mercado."},
            "minimum": {"label": "Pagar solo minimo", "stress": 4, "lesson": "Costo invisible", "interpretation": "El pago minimo compra alivio hoy y vende meses futuros."},
            "new_card": {"label": "Aceptar nueva tarjeta", "cash": 700, "debt": {"name": "Nueva tarjeta", "type": "Credit card", "balance": 900, "payment": 60, "rate": 0.36, "stress": 7}, "credit_score": -12, "stress": 7, "lesson": "Credito facil", "interpretation": "La caja subio. Tu libertad bajo. Esa diferencia suele esconderse en cuotas."},
        },
    },
    {
        "id": "medical_bill",
        "category": "Crisis",
        "phase": "survival",
        "title": "Gasto medico inesperado",
        "description": "Un problema de salud genera un costo no planificado. Tu reserva define si es molestia o crisis.",
        "actions": {
            "pay": {"label": "Pagar $1.200", "cash": -1200, "stress": 6, "lesson": "Fondo de emergencia", "interpretation": "La liquidez parece improductiva hasta que evita deuda cara."},
            "finance": {"label": "Financiar con prestamo", "debt": {"name": "Prestamo emergencia", "type": "Personal loan", "balance": 1200, "payment": 95, "rate": 0.24, "stress": 6}, "stress": 10, "lesson": "Fragilidad", "interpretation": "Financiar emergencias protege caja inmediata, pero agrega presion futura."},
        },
    },
    {
        "id": "financial_course",
        "category": "Knowledge",
        "phase": "survival",
        "title": "Curso de analisis financiero",
        "description": "Un curso practico promete ayudarte a evaluar inversiones con mejores metricas.",
        "actions": {
            "buy": {"label": "Invertir $700", "cash": -700, "education": 1, "lesson": "Capital mental", "interpretation": "La educacion no paga renta hoy, pero cambia la calidad de tus proximas decisiones."},
            "cheap": {"label": "Aprender gratis durante meses", "education": 1, "stress": 2, "skip_months": 2, "lesson": "Costo de oportunidad", "interpretation": "Ahorraste dinero, pero pagaste con tiempo. El tiempo tambien compone."},
            "skip": {"label": "No estudiar ahora", "lesson": "Estancamiento", "interpretation": "Sin mejores herramientas, las oportunidades complejas siguen pareciendo ruido."},
        },
    },
    {
        "id": "lifestyle_car",
        "category": "Expense",
        "phase": "growth",
        "title": "Auto nuevo financiado",
        "description": "La cuota entra en tu presupuesto y el auto se siente como progreso. No genera ingresos.",
        "actions": {
            "buy": {"label": "Financiar el auto", "debt": {"name": "Auto nuevo", "type": "Auto loan", "balance": 16000, "payment": 390, "rate": 0.14, "stress": 8}, "expenses": 120, "stress": 7, "lifestyle": 1, "lesson": "Inflacion de estilo de vida", "interpretation": "El auto se disfruta hoy. El pago vota contra tus opciones durante anos."},
            "used": {"label": "Comprar usado en efectivo", "cash": -2500, "expenses": 35, "stress": -1, "lesson": "Utilidad sobre estatus", "interpretation": "Resolviste transporte sin encadenar tu flujo mensual."},
            "skip": {"label": "Conservar tu auto actual", "stress": -3, "lesson": "Disciplina", "interpretation": "No mejorar estilo de vida despues de ganar mas es una ventaja subestimada."},
        },
    },
    {
        "id": "raise",
        "category": "Income",
        "phase": "survival",
        "title": "Oferta de ascenso",
        "description": "Puedes ganar mas. El cargo suma responsabilidad y menos energia fuera del trabajo.",
        "actions": {
            "accept": {"label": "Aceptar ascenso", "salary": 450, "stress": 8, "lesson": "Ingreso activo", "interpretation": "Mas salario ayuda, pero si todo depende de tu energia, sigues en la carrera."},
            "negotiate": {"label": "Negociar salario y flexibilidad", "salary": 300, "stress": 2, "education": 1, "lesson": "Negociacion", "interpretation": "Mejorar condiciones puede valer mas que solo mejorar el sueldo."},
            "decline": {"label": "Rechazar y cuidar energia", "stress": -6, "lesson": "Sostenibilidad", "interpretation": "Optimizar vida financiera tambien implica proteger salud y capacidad de decidir."},
        },
    },
    {
        "id": "market_drop",
        "category": "Crisis",
        "phase": "growth",
        "title": "Correccion del mercado",
        "description": "Los precios caen. Si tenes liquidez puede ser oportunidad; si tenes miedo puede ser trampa.",
        "actions": {
            "buy": {"label": "Comprar barato por $1.000", "cash": -1000, "asset": {"name": "Compra en correccion", "type": "Paper assets", "value": 1200, "income": 10, "risk": "market"}, "lesson": "Crisis como oportunidad", "interpretation": "La misma caida que asusta a unos crea entrada para quien llega preparado."},
            "panic": {"label": "Vender por miedo", "sell_asset_percent": 0.2, "stress": 5, "lesson": "Panico", "interpretation": "Vender por miedo convierte volatilidad temporal en perdida permanente."},
            "hold": {"label": "No tocar nada", "stress": -1, "lesson": "Paciencia", "interpretation": "A veces la mejor decision es no reaccionar al ruido."},
        },
    },
    {
        "id": "rent_increase",
        "category": "Expense",
        "phase": "survival",
        "title": "Aumento de alquiler",
        "description": "Tu costo de vida sube. Puedes absorberlo, mudarte o compensar con mas trabajo.",
        "actions": {
            "absorb": {"label": "Absorber +$220/mes", "expenses": 220, "stress": 5, "lesson": "Gastos fijos", "interpretation": "Los gastos recurrentes son pequenos anclajes que frenan tu velocidad."},
            "move": {"label": "Mudarte y pagar $900", "cash": -900, "expenses": -160, "stress": 6, "lesson": "Costo inicial", "interpretation": "Algunas decisiones duelen una vez para mejorar todos los meses siguientes."},
            "side": {"label": "Tomar trabajo extra", "salary": 260, "stress": 12, "lesson": "Ingreso no sostenible", "interpretation": "Mas ingreso puede resolver caja y romper energia al mismo tiempo."},
        },
    },
    {
        "id": "refinance",
        "category": "Debt",
        "phase": "growth",
        "requires_debt": True,
        "title": "Oportunidad de refinanciar",
        "description": "El banco ofrece bajar cuotas extendiendo plazo. La caja mejora, el costo total puede subir.",
        "actions": {
            "refi": {"label": "Refinanciar y bajar pagos", "reduce_debt_payments": 0.18, "credit_score": 5, "stress": -4, "lesson": "Flexibilidad vs costo", "interpretation": "Liberaste flujo mensual, pero el alivio no es riqueza si solo estira la deuda.", "delayed": [{"delay": 8, "label": "Tasa variable sube 4%", "source": "Refinanciacion", "effect": {"debt_rate_hike": "Hipoteca departamento", "delta": 0.04}}]},
            "reject": {"label": "Mantener plan actual", "lesson": "Costo total", "interpretation": "A veces pagar mas por mes te libera antes."},
            "extra": {"label": "Pagar $1.500 y no refinanciar", "cash": -1500, "pay_debt": 1500, "stress": -3, "lesson": "Desapalancamiento", "interpretation": "Bajar deuda reduce riesgo aunque no se vea tan emocionante como invertir."},
        },
    },
    {
        "id": "job_loss",
        "category": "Crisis",
        "phase": "freedom",
        "requires_world": ["Recesion", "Recuperacion"],
        "title": "Riesgo de despido",
        "description": "Tu sector recorta personal. La estabilidad que parecia normal ahora tiene precio.",
        "actions": {
            "prepare": {"label": "Reducir gastos y preparar busqueda", "expenses": -250, "stress": 4, "career_stability": 5, "lesson": "Antifragilidad", "interpretation": "Prepararte antes del golpe convierte crisis en transicion."},
            "ignore": {"label": "Ignorar senales", "stress": 5, "salary_risk": 0.18, "lesson": "Riesgo ignorado", "interpretation": "La estabilidad se siente gratis hasta que desaparece.", "delayed": [{"delay": 3, "label": "Recorte llega (-20% salario)", "source": "Riesgo de despido", "effect": {"salary_snap_pct": 0.2}}]},
            "upskill": {"label": "Invertir $1.200 en habilidades", "cash": -1200, "education": 1, "career_stability": 8, "lesson": "Empleabilidad", "interpretation": "Mejorar habilidades es una forma de seguro contra el mercado laboral."},
        },
    },
    {
        "id": "family_support",
        "category": "Expense",
        "phase": "growth",
        "title": "Ayuda familiar urgente",
        "description": "Un familiar necesita apoyo. Es financieramente incomodo y emocionalmente dificil de ignorar.",
        "actions": {
            "help": {"label": "Ayudar con $1.800", "cash": -1800, "stress": 4, "lesson": "Vida real", "interpretation": "La planilla no captura todo. La libertad financiera tambien compra capacidad de ayudar."},
            "partial": {"label": "Ayuda parcial de $700", "cash": -700, "stress": 6, "lesson": "Limites", "interpretation": "Poner limites puede cuidar tu futuro sin abandonar tus valores."},
            "debt": {"label": "Endeudarte para ayudar", "debt": {"name": "Prestamo familiar", "type": "Personal loan", "balance": 1800, "payment": 135, "rate": 0.22, "stress": 7}, "stress": 8, "lesson": "Riesgo emocional", "interpretation": "La deuda tomada por presion emocional pesa doble: en caja y en cabeza."},
        },
    },
    {
        "id": "tenant_problem",
        "category": "Crisis",
        "phase": "freedom",
        "title": "Inquilino deja de pagar",
        "description": "Tu renta inmobiliaria falla durante varios meses. El flujo pasivo no siempre es pasivo ni estable.",
        "requires_asset_type": "Real estate",
        "actions": {
            "reserve": {"label": "Cubrir con reserva", "cash": -1600, "stress": 5, "lesson": "Renta no garantizada", "interpretation": "Los activos reales tienen friccion real. La reserva protege el activo."},
            "sell": {"label": "Vender parte del portafolio", "sell_asset_percent": 0.15, "stress": 7, "lesson": "Liquidez forzada", "interpretation": "Vender bajo presion suele ser mas caro que ahorrar antes."},
            "legal": {"label": "Proceso legal y gestion", "cash": -800, "stress": 11, "lesson": "Mantenimiento de activos", "interpretation": "El rendimiento inmobiliario incluye problemas que no aparecen en el anuncio."},
        },
    },
    {
        "id": "startup_friend",
        "category": "Investment",
        "phase": "growth",
        "title": "Startup de un amigo",
        "description": "La presentacion suena brillante. No hay flujo, solo promesa de multiplicar capital.",
        "actions": {
            "angel": {"label": "Invertir $2.500", "cash": -2500, "asset": {"name": "Equity startup", "type": "Small business", "value": 1200, "income": 0, "risk": "very high"}, "stress": 7, "lesson": "Especulacion privada", "interpretation": "El upside es real, pero la iliquidez tambien. No confundas cercania con diligencia.", "delayed": [{"delay": 18, "label": "Startup cierra (70%)", "source": "Startup de un amigo", "effect": {"asset_fail_chance": {"name": "Equity startup", "prob": 0.7}}}]},
            "small": {"label": "Invertir simbolico $500", "cash": -500, "asset": {"name": "Ticket startup", "type": "Small business", "value": 300, "income": 0, "risk": "very high"}, "lesson": "Tamano de posicion", "interpretation": "Puedes participar en riesgo alto sin apostar tu supervivencia.", "delayed": [{"delay": 18, "label": "Startup cierra (70%)", "source": "Startup de un amigo", "effect": {"asset_fail_chance": {"name": "Ticket startup", "prob": 0.7}}}]},
            "pass": {"label": "Pasar aunque incomode", "stress": 2, "lesson": "Independencia", "interpretation": "Decir no a una mala estructura puede costar socialmente y ahorrar financieramente."},
        },
    },
    {
        "id": "burnout",
        "category": "Income",
        "phase": "freedom",
        "title": "Advertencia de burnout",
        "description": "Tu ingreso activo crecio, pero el cuerpo empieza a cobrar factura.",
        "actions": {
            "rest": {"label": "Bajar ritmo y perder $400/mes", "salary": -400, "stress": -18, "lesson": "Sostenibilidad", "interpretation": "Una estrategia que destruye tu energia no es pasiva, es deuda biologica."},
            "push": {"label": "Seguir empujando", "salary": 250, "stress": 14, "lesson": "Riesgo humano", "interpretation": "El flujo subio. La capacidad de sostenerlo bajo."},
            "delegate": {"label": "Pagar ayuda por $600", "expenses": 600, "stress": -10, "lesson": "Comprar tiempo", "interpretation": "Gastar para recuperar energia puede ser inversion si protege decisiones futuras."},
        },
    },
    {
        "id": "debt_free_temptation",
        "category": "Debt",
        "phase": "growth",
        "requires_debt_free": True,
        "requires_world": ["Expansion", "Estable"],
        "title": "Tentacion de credito preaprobado",
        "description": "El banco te ofrece credito facil justo cuando no tenes deudas. Puede darte velocidad o volver a ponerte una cadena.",
        "actions": {
            "reject": {"label": "Rechazar y mantenerte libre", "stress": -2, "credit_score": 3, "lesson": "Libertad de obligacion", "interpretation": "No usar credito disponible tambien es poder. Tu flujo queda sin nuevos duenos."},
            "strategic": {"label": "Usar $1.200 para invertir", "cash": -1200, "asset": {"name": "Posicion financiada", "type": "Paper assets", "value": 1400, "income": 8, "risk": "market"}, "debt": {"name": "Linea de inversion", "type": "Investment loan", "balance": 1200, "payment": 85, "rate": 0.16, "stress": 5}, "stress": 4, "lesson": "Deuda estrategica", "interpretation": "La deuda no es mala por definicion. Es peligrosa cuando no sabes exactamente que compra."},
            "consume": {"label": "Usarlo para mejorar estilo de vida", "cash": 600, "debt": {"name": "Credito consumo", "type": "Credit card", "balance": 1400, "payment": 95, "rate": 0.34, "stress": 8}, "expenses": 80, "stress": 8, "lifestyle": 1, "lesson": "Regreso a la rueda", "interpretation": "La libertad de deuda puede perderse en una tarde. La cuota se queda anos."},
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
        "events_seen": [],
        "schedule": [],
        "asset_events": [],
    }
    start_month(state)
    return enrich_state(state)


def start_month(state):
    state["world"] = choice(WORLD_STATES)
    apply_monthly_cashflow(state)
    apply_market_drift(state)
    maybe_salary_shock(state)
    event = pick_event(state)
    state["current_event"] = event
    return state


def pick_event(state):
    phase = session_phase(state)
    available = []
    for event in BASE_EVENTS:
        if event.get("requires_debt") and not state["debts"]:
            continue
        if event.get("requires_debt_free") and state["debts"]:
            continue
        required_type = event.get("requires_asset_type")
        if required_type and not any(asset.get("type") == required_type for asset in state["assets"]):
            continue
        if event.get("requires_world") and state["world"]["name"] not in event["requires_world"]:
            continue
        if event["id"] == "burnout" and state["stress"] >= 78:
            available.append(event)
            continue
        if event.get("phase") in {phase, "survival"} or phase == "freedom":
            available.append(event)
    if len(available) >= 3:
        recent = set(state.get("events_seen", [])[-4:])
        fresh = [event for event in available if event["id"] not in recent]
        if fresh:
            available = fresh
    event = prepare_event_for_state(deepcopy(choice(available or BASE_EVENTS)), state)
    state.setdefault("events_seen", []).append(event["id"])
    state["events_seen"] = state["events_seen"][-12:]
    return event


def prepare_event_for_state(event, state):
    actions = {}
    for key, action in event["actions"].items():
        if action.get("pay_debt") and not state["debts"]:
            continue
        if action.get("reduce_debt_payments") and not state["debts"]:
            continue
        if action.get("sell_asset_percent") and not state["assets"]:
            continue
        actions[key] = action
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


def session_phase(state):
    ratio = metrics(state)["freedom_ratio"] if state.get("assets") or state.get("debts") else 0
    if state["month"] <= 48 or ratio < 0.25:
        return "survival"
    if ratio < 0.75:
        return "growth"
    return "freedom"


def apply_monthly_cashflow(state):
    income = state["salary"] + risky_passive_income(state)
    outflow = state["expenses"] + debt_payments(state)
    state["cash"] += income - outflow
    state["expenses"] = round(state["expenses"] * (1 + state["world"]["inflation"]), 2)
    accrue_debt_interest(state)
    if state["cash"] < 0:
        state["insolvent_months"] += 1
        state["stress"] += 8
        state["dangerous_moment"] = "Caja negativa durante varios meses"
    else:
        state["insolvent_months"] = 0


def risky_passive_income(state):
    total = 0
    education = state.get("education", 0)
    for asset in state.get("assets", []):
        a_income = asset.get("income", 0)
        risk = asset.get("risk", "")
        norm = max(0.0, 1 - education * 0.01)
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
        state["stress"] += 12
        state["dangerous_moment"] = "Recorte de ingresos durante " + state["world"]["name"]
        asset_events_append(state, "salary_shock", "Recorte de ingresos (-$" + str(int(loss)) + ")")


def apply_action(state, action_id):
    if state.get("status") != "playing" or not state.get("current_event"):
        return enrich_state(state)

    event = state["current_event"]
    action = event["actions"].get(action_id)
    if not action:
        state["last_feedback"] = feedback("Accion invalida", "Esa opcion no esta disponible.", "Revisa tus alternativas antes de decidir.")
        return enrich_state(state)

    before = metrics(state)
    before_snapshot = simple_snapshot(state)
    apply_action_effects(state, action)
    normalize_state(state)
    after = metrics(state)
    impact = after["freedom_ratio"] - before["freedom_ratio"]
    state["last_feedback"] = build_feedback(action, before_snapshot, simple_snapshot(state), before, after)
    update_decision_records(state, event, action, impact, before, after)
    state["history"].insert(0, {
        "month": state["month"],
        "age": display_age(state),
        "title": event["title"],
        "category": event["category"],
        "action": action["label"],
        "feedback": state["last_feedback"],
    })
    state["history"] = state["history"][:18]
    state["current_event"] = None
    advance_time(state, action.get("skip_months", 1))
    check_end_conditions(state)
    if state["status"] == "playing":
        start_month(state)
    return enrich_state(state)


def apply_action_effects(state, action):
    state["cash"] += action.get("cash", 0)
    state["salary"] += action.get("salary", 0)
    state["expenses"] += action.get("expenses", 0)
    state["education"] += action.get("education", 0)
    state["stress"] += action.get("stress", 0)
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
        pay_down_debt(state, action["pay_debt"])
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


def advance_time(state, months=1):
    months = max(1, int(months))
    for _ in range(months):
        state["month"] += 1
        process_schedule(state)
        if state["month"] % 12 == 1 and state["month"] > 1:
            state["age"] += 1
            state["salary"] = round(state["salary"] * (1.02 + state["education"] * 0.002), 2)


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
    score = 35 + min(35, max(0, runway) * 4) + state["education"] * 4 + max(0, state["credit_score"] - 600) / 12
    score -= debt_to_income * 55
    score -= max(0, state["stress"] - 55) * 0.5
    return round(max(0, min(100, score)))


def enrich_state(state):
    state = deepcopy(state)
    state["metrics"] = metrics(state)
    state["display_age"] = display_age(state)
    state["investor_profile"] = investor_profile(state)
    state["phase"] = session_phase(state)
    state["report"] = final_report(state)
    state["status_badges"] = status_badges(state)
    state["alerts"] = contextual_alerts(state)
    return state


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


def display_age(state):
    years = state["age"]
    months = (state["month"] - 1) % 12
    return f"{years} anos" if months == 0 else f"{years} anos y {months} meses"


def normalize_state(state):
    state["stress"] = max(0, min(100, round(state["stress"])))
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


def update_decision_records(state, event, action, impact, before, after):
    record = f"{event['title']}: {action['label']}"
    if impact >= 0.04 or after["cashflow"] - before["cashflow"] > 250:
        state["best_decision"] = record
    if impact <= -0.04 or state["cash"] < 0 or after["runway"] < 1:
        state["worst_decision"] = record
    if after["insolvency_risk"] >= 70:
        state["dangerous_moment"] = record


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
    elif state["stress"] >= 96:
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


def best_asset(state):
    if not state["assets"]:
        return "Sin activos productivos"
    asset = max(state["assets"], key=lambda item: item.get("income", 0) + item.get("value", 0) * 0.002)
    return f"{asset['name']} (+${asset.get('income', 0):,.0f}/mes)"


def worst_liability(state):
    if not state["debts"]:
        return "Sin deudas activas"
    debt = max(state["debts"], key=lambda item: item.get("payment", 0) + item.get("rate", 0) * 1000)
    return f"{debt['name']} (${debt.get('payment', 0):,.0f}/mes, {debt.get('rate', 0) * 100:.0f}% anual)"


def final_report(state):
    data = metrics(state)
    outcome = state.get("outcome") or partial_outcome(state)
    summary = (
        f"Termine como {state['profession']} a los {display_age(state)}. "
        f"Patrimonio neto: ${data['net_worth']:,.0f}. "
        f"Ingreso pasivo: ${data['passive_income']:,.0f}/mes. "
        f"Reserva: {data['runway']} meses. "
        f"Perfil: {investor_profile(state)}."
    )
    return {
        "outcome": outcome,
        "simulated_years": round((state["month"] - 1) / 12, 1),
        "biggest_win": state.get("best_decision") or "Aun no hubo una decision transformadora.",
        "biggest_mistake": state.get("worst_decision") or "No se detecto un error critico.",
        "dangerous_moment": state.get("dangerous_moment") or "No hubo un momento de peligro extremo.",
        "best_asset": best_asset(state),
        "worst_liability": worst_liability(state),
        "educational_summary": educational_summary(state, data, outcome),
        "shareable_summary": summary,
    }


def educational_summary(state, data, outcome):
    if outcome == "Financially free":
        return "Construiste libertad con dos defensas: flujo pasivo y reserva. El juego no premia solo ganar mas, premia depender menos."
    if outcome in {"Debt trapped", "Overleveraged collapse"}:
        return "El problema no fue una sola compra. Fueron obligaciones que siguieron llegando cuando la caja dejo de acompanar."
    if outcome == "High net worth, low liquidity":
        return "Tener activos no es igual a estar seguro. La liquidez decide si puedes sobrevivir sin vender en mal momento."
    if state["stress"] > 80:
        return "La estrategia produjo avance financiero, pero compro ese avance con estres. La energia tambien es capital."
    if data["runway"] >= 6:
        return "Tu seguridad vino de tener margen. La reserva no maximiza retorno, maximiza opciones."
    return "Tu resultado quedo en el medio: suficiente progreso para aprender, suficiente friccion para jugar otra vez mejor."
