from copy import deepcopy


PROFESSIONS = {
    "administrativo": {
        "name": "Empleado administrativo",
        "summary": "Estabilidad razonable, crecimiento lento y margen de ahorro limitado.",
        "risk_profile": "Conservador forzado",
        "career_stability": 82,
        "age": 26,
        "cash": 1800,
        "salary": 2200,
        "expenses": 1900,
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
        "stress": 28,
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
        "expenses": 2300,
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
        "cash": 8000,
        "salary": 7200,
        "expenses": 3500,
        "education": 2,
        "stress": 32,
        "credit_score": 700,
        "debts": [
            {"name": "Prestamo estudiantil", "type": "Student loan", "balance": 25000, "payment": 350, "rate": 0.08, "stress": 8},
            {"name": "Auto financiado", "type": "Auto loan", "balance": 12000, "payment": 300, "rate": 0.12, "stress": 6},
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
        "stress": 28,
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
        "expenses": 2200,
        "education": 1,
        "stress": 30,
        "credit_score": 620,
        "debts": [{"name": "Equipo financiado", "type": "Personal loan", "balance": 3600, "payment": 160, "rate": 0.18, "stress": 5}],
    },
}


WORLD_STATES = [
    {"name": "Expansion", "inflation": 0.003, "asset_price": 1.08, "income_risk": 0.02, "credit": 1.15, "description": "Credito accesible, empleos fuertes y activos caros."},
    {"name": "Estable", "inflation": 0.002, "asset_price": 1.0, "income_risk": 0.04, "credit": 1.0, "description": "Mercados equilibrados y oportunidades razonables."},
    {"name": "Recesion", "inflation": 0.0005, "asset_price": 0.86, "income_risk": 0.11, "credit": 0.72, "description": "Activos baratos, ingresos fragiles y credito exigente."},
    {"name": "Recuperacion", "inflation": 0.001, "asset_price": 0.94, "income_risk": 0.06, "credit": 0.92, "description": "El mercado mejora y aparecen oportunidades subvaloradas."},
]


LIQUIDITY_BY_TYPE = {
    "Paper assets": 0.85,
    "Real estate": 0.70,
    "Small business": 0.60,
}


def profession_choices():
    return [{"id": key, **value} for key, value in PROFESSIONS.items()]
