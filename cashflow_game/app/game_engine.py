from copy import deepcopy
from random import choice, random, uniform


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
            "strategic": {"label": "Usar ${cash:,.0f} para invertir", "label_fmt": "Usar ${cash:,.0f} para invertir", "cash": {"factor": -0.2, "min": -8000, "max": -500}, "asset": {"name": "Posicion financiada", "type": "Paper assets", "value": {"factor": 0.25, "min": 600, "max": 10000}, "income": 8, "risk": "market"}, "debt": {"name": "Linea de inversion", "type": "Investment loan", "balance": {"factor": 0.2, "min": 500, "max": 8000}, "payment": 85, "rate": 0.16, "stress": 5}, "stress": 4, "lesson": "Deuda estrategica", "interpretation": "La deuda no es mala por definicion. Es peligrosa cuando no sabes exactamente que compra."},
            "consume": {"label": "Usarlo para mejorar estilo de vida", "cash": {"factor": 0.1, "min": 300, "max": 3000}, "debt": {"name": "Credito consumo", "type": "Credit card", "balance": {"factor": 0.2, "min": 500, "max": 4000}, "payment": 95, "rate": 0.34, "stress": 8}, "expenses": {"factor": 0.02, "min": 50, "max": 300}, "stress": 8, "lifestyle": 1, "lesson": "Regreso a la rueda", "interpretation": "La libertad de deuda puede perderse en una tarde. La cuota se queda anos."},
        },
    },
    {  # --- Crisis +10 ---
        "id": "robbery",
        "category": "Crisis",
        "phase": "survival",
        "title": "Robo en tu casa",
        "description": "Entran a tu domicilio. Lo material se repone, pero la sensacion de seguridad tarda mas.",
        "actions": {
            "absorb": {"label": "Reponer de caja ${cash:,.0f}", "label_fmt": "Reponer de caja ${cash:,.0f}", "cash": {"factor": -0.3, "min": -4000, "max": -300}, "stress": 8, "lesson": "Reserva improductiva", "interpretation": "El dinero parado parece ocioso hasta que un ladrigo te recuerda para que sirve."},
            "insurance": {"label": "Activar seguro con deducible", "cash": {"factor": -0.08, "min": -800, "max": -100}, "stress": 4, "credit_score": 3, "lesson": "Transferencia de riesgo", "interpretation": "El seguro no evita el daño, transfiere el costo."},
            "ignore": {"label": "No reponer y vivir con menos", "stress": 12, "lesson": "Costo emocional", "interpretation": "Ahorraste dinero. Pagaste con calma."},
        },
    },
    {
        "id": "divorce_settlement",
        "category": "Crisis",
        "phase": "growth",
        "title": "Separacion financiera",
        "description": "Una relacion larga termina. Los activos se dividen y los gastos se reestructuran.",
        "actions": {
            "fair": {"label": "Dividir activos equitativamente", "cash": {"factor": -0.3, "min": -8000, "max": -1000}, "sell_asset_percent": 0.3, "expenses": {"factor": -0.1, "min": -500, "max": -50}, "stress": 14, "lesson": "Costo de restructuracion", "interpretation": "La equidad duele ahora y protege despues."},
            "fight": {"label": "Pelear por mas en tribunales", "cash": {"factor": -0.15, "min": -3000, "max": -500}, "stress": 20, "career_stability": -8, "lesson": "Costo de oportunidad", "interpretation": "Ganaste principio. Perdiste tiempo, energia y foco."},
            "mediate": {"label": "Mediar y cerrar rapido", "cash": {"factor": -0.1, "min": -2000, "max": -300}, "sell_asset_percent": 0.2, "stress": 8, "education": 1, "lesson": "Cierre eficiente", "interpretation": "Cortar el costo emocional temprano puede ser la mejor inversion del momento."},
        },
    },
    {
        "id": "country_crisis",
        "category": "Crisis",
        "phase": "freedom",
        "requires_world": ["Recesion"],
        "title": "Crisis cambiaria en el pais",
        "description": "El gobierno impone restricciones. Tus activos locales se descalzan frente a la deuda en moneda extranjera.",
        "actions": {
            "hedge": {"label": "Comprar dolar / cobertura ${cash:,.0f}", "label_fmt": "Comprar dolar / cobertura ${cash:,.0f}", "cash": {"factor": -0.3, "min": -6000, "max": -800}, "asset": {"name": "Cobertura USD", "type": "Paper assets", "value": {"factor": 0.35, "min": 800, "max": 7000}, "income": 0, "risk": "market"}, "stress": 6, "lesson": "Cobertura", "interpretation": "Proteger patrimonio en crisis no es especular, es sobrevivir."},
            "freeze": {"label": "Congelar gastos y esperar", "expenses": {"factor": -0.1, "min": -400, "max": -50}, "stress": 10, "lesson": "Defensa total", "interpretation": "En crisis sistemica, reducir曝光 es la unidad de decision."},
            "panic_buy": {"label": "Comprar todo ahora", "cash": {"factor": -0.5, "min": -10000, "max": -2000}, "stress": 15, "lesson": "Panico sistematico", "interpretation": "El miedo convierte la incertidumbre en malas compras."},
        },
    },
    {
        "id": "tax_audit",
        "category": "Crisis",
        "phase": "growth",
        "title": "Auditoria fiscal",
        "description": "El fisco revisa tus ultimos años. Tu orden documental define si es molestia o multa.",
        "actions": {
            "pay": {"label": "Pagar lo que piden ${cash:,.0f}", "label_fmt": "Pagar lo que piden ${cash:,.0f}", "cash": {"factor": -0.25, "min": -5000, "max": -500}, "stress": 10, "lesson": "Cumplimiento", "interpretation": "Pagar rapido reduce interes y multa. No es justicia, es costo de cerrar."},
            "contest": {"label": "Contestar con contador", "cash": {"factor": -0.05, "min": -1500, "max": -200}, "stress": 6, "education": 1, "lesson": "Defensa informada", "interpretation": "Un buen contador devuelve mas de lo que cuesta cuando el fisco se equivoca."},
            "ignore": {"label": "Ignorar y rezar", "stress": 15, "credit_score": -20, "lesson": "Riesgo ignorado", "interpretation": "El fisco no olvida. El interestCompound no perdona."},
        },
    },
    {
        "id": "car_accident",
        "category": "Crisis",
        "phase": "survival",
        "title": "Accidente de transito",
        "description": "Un siniestro te genera gastos medicos y mecanicos imprevistos.",
        "actions": {
            "pay": {"label": "Pagar todo ${cash:,.0f}", "label_fmt": "Pagar todo ${cash:,.0f}", "cash": {"factor": -0.25, "min": -4000, "max": -400}, "stress": 8, "lesson": "Fondo de emergencia", "interpretation": "La reserva cumple su mision: convertir crisis en molestia."},
            "finance": {"label": "Financiar con prestamo", "debt": {"name": "Prestamo accidente", "type": "Personal loan", "balance": {"factor": 0.25, "min": 400, "max": 4000}, "payment": 90, "rate": 0.22, "stress": 6}, "stress": 8, "lesson": "Deuda por emergencia", "interpretation": "Sin caja, la emergencia se convierte en cuota."},
            "deductible": {"label": "Solo deducible del seguro", "cash": {"factor": -0.05, "min": -800, "max": -100}, "stress": 3, "lesson": "Seguro activo", "interpretation": "Pagaste una prima todo el año. Ahora cobraste el dividendo."},
        },
    },
    {
        "id": "bad_inheritance",
        "category": "Crisis",
        "phase": "growth",
        "title": "Heredas un activo con problema",
        "description": "Un familiar fallece y te deja una propiedad con deuda oculta o un negocio en rojo.",
        "actions": {
            "accept": {"label": "Aceptar y sanear", "cash": {"factor": -0.2, "min": -5000, "max": -800}, "asset": {"name": "Activo heredado", "type": "Real estate", "value": {"factor": 1.5, "min": 20000, "max": 120000}, "income": 180, "risk": "vacancy"}, "debt": {"name": "Deuda oculta heredada", "type": "Mortgage", "balance": {"factor": 0.8, "min": 10000, "max": 60000}, "payment": 520, "rate": 0.08, "stress": 7}, "stress": 8, "lesson": "Due diligence", "interpretation": "Heredar no es gratis. Asumir obligaciones sin revisar es una apuesta ciega."},
            "reject": {"label": "Renunciar a la herencia", "stress": 6, "lesson": "Saber decir no", "interpretation": "Rechazar un activo toxico puede ser la decision mas lucrativa del año."},
            "sell_fast": {"label": "Aceptar y vender rapido", "cash": {"factor": 0.3, "min": 2000, "max": 30000}, "sell_asset_percent": 0.0, "stress": 10, "lesson": "Liquidez sobre valor", "interpretation": "Vender con descuento libera caja y evita gestion de un activo que no elegiste."},
        },
    },
    {
        "id": "lawsuit",
        "category": "Crisis",
        "phase": "freedom",
        "title": "Demanda civil",
        "description": "Un cliente o socio te demanda. El costo legal come caja y energia.",
        "actions": {
            "settle": {"label": "Transar ${cash:,.0f}", "label_fmt": "Transar ${cash:,.0f}", "cash": {"factor": -0.3, "min": -8000, "max": -1000}, "stress": 6, "lesson": "Costo de cerrar", "interpretation": "Transar no es admitir culpa. Es comprar paz mental para seguir adelqnte."},
            "fight": {"label": "Pelear en tribunales", "cash": {"factor": -0.15, "min": -4000, "max": -500}, "stress": 16, "career_stability": -6, "lesson": "Principio vs costo", "interpretation": "Ganar puede costar mas que la propia demanda."},
            "insurance_cover": {"label": "Usar seguro de responsabilidad", "cash": {"factor": -0.03, "min": -500, "max": -50}, "stress": 4, "lesson": "Cobertura pasiva", "interpretation": "El seguro de responsabilidad es uno de los mejores gastos invisibles."},
        },
    },
    {
        "id": "natural_disaster",
        "category": "Crisis",
        "phase": "growth",
        "requires_asset_type": "Real estate",
        "title": "Danos por clima extremo",
        "description": "Una tormenta severa danas tu propiedad. El seguro puede no cubrir todo.",
        "actions": {
            "repair": {"label": "Reparar de caja ${cash:,.0f}", "label_fmt": "Reparar de caja ${cash:,.0f}", "cash": {"factor": -0.25, "min": -5000, "max": -800}, "stress": 8, "lesson": "Mantenimiento de activos", "interpretation": "Los activos reales exigen reservas para eventos que no aparecen en el brochure."},
            "insurance": {"label": "Activar seguro", "cash": {"factor": -0.05, "min": -1000, "max": -100}, "stress": 4, "lesson": "Proteccion activa", "interpretation": "El seguro convierte catastrofe en deducible."},
            "defer": {"label": "Postponer reparacion", "stress": 12, "credit_score": -5, "lesson": "Costo diferido", "interpretation": "El dano no reparado se agrava. El activo pierde valor y vos, calma."},
        },
    },
    {
        "id": "identity_theft",
        "category": "Crisis",
        "phase": "growth",
        "title": "Robo de identidad",
        "description": "Detectas movimientos sospechosos en tus cuentas. Tu credito puede estar comprometido.",
        "actions": {
            "freeze": {"label": "Congelar cuentas y reportar", "cash": {"factor": -0.05, "min": -1000, "max": -100}, "stress": 8, "credit_score": -10, "lesson": "Respuesta rapida", "interpretation": "Actuar en horas, no en dias, limita el dano."},
            "monitor": {"label": "Solo monitorear", "stress": 12, "credit_score": -25, "lesson": "Riesgo ignorado", "interpretation": "El fraude no se arregla solo. El silencio es consentimiento para el ladron."},
            "pro_service": {"label": "Pagar servicio de proteccion", "expenses": {"factor": 0.01, "min": 20, "max": 80}, "stress": -3, "credit_score": 5, "lesson": "Costo de tranquilidad", "interpretation": "Pagar por monitoreo es un seguro contra futuro dolor de cabeza."},
        },
    },
    {
        "id": "health_scare",
        "category": "Crisis",
        "phase": "freedom",
        "title": "Susto de salud serio",
        "description": "Un chequeo revela algo que requiere tratamiento. El costo depende de tu cobertura.",
        "actions": {
            "treat": {"label": "Tratar de inmediato ${cash:,.0f}", "label_fmt": "Tratar de inmediato ${cash:,.0f}", "cash": {"factor": -0.35, "min": -8000, "max": -1000}, "stress": -5, "lesson": "Salud primero", "interpretation": "La salud es el activo mas subestimado. Sin ella, el resto no funciona."},
            "delay": {"label": "Postponer tratamiento", "stress": 20, "lesson": "Costo de esperar", "interpretation": "Esperar puede convertir un problema manejable en uno critico."},
            "insurance": {"label": "Usar cobertura medica", "cash": {"factor": -0.08, "min": -1500, "max": -200}, "stress": 6, "lesson": "Seguro medico", "interpretation": "La cobertura no es lujo. Es la diferencia entre tratar y arruinarse."},
        },
    },
    {  # --- Income +8 ---
        "id": "competitor_offer",
        "category": "Income",
        "phase": "growth",
        "title": "Oferta de la competencia",
        "description": "Una empresa rival te ofrece mas salario. Cambiar implica riesgo y adaptacion.",
        "actions": {
            "accept": {"label": "Aceptar salto salarial", "salary": {"factor": 0.15, "min": 300, "max": 3000}, "stress": 8, "career_stability": -5, "lesson": "Ingreso vs estabilidad", "interpretation": "Mas salario sin red de estabilidad es un salto con piso frágil."},
            "leverage": {"label": "Usarla para renegociar", "salary": {"factor": 0.08, "min": 150, "max": 1500}, "education": 1, "lesson": "Palanca externa", "interpretation": "Una oferta no siempre se acepta. A veces se usa para crecer donde estas."},
            "decline": {"label": "Rechazar por lealtad o foco", "stress": -4, "career_stability": 5, "lesson": "Foco", "interpretation": "No todo aumento merece cambio. La estabilidad tambien compone."},
        },
    },
    {
        "id": "freelance_gig",
        "category": "Income",
        "phase": "survival",
        "title": "Trabajo freelance extraordinario",
        "description": "Un cliente te ofrece un proyecto extra. Duplica ingreso este mes, pero come fines de semana.",
        "actions": {
            "take": {"label": "Aceptar y cobrar ${cash:,.0f}", "label_fmt": "Aceptar y cobrar ${cash:,.0f}", "cash": {"factor": 0.3, "min": 500, "max": 6000}, "stress": 10, "lesson": "Ingreso activo", "interpretation": "El freelance acelera caja pero no construye sistema. Seguis cambiando tiempo por dinero."},
            "delegate": {"label": "Subcontratar parte", "cash": {"factor": 0.12, "min": 200, "max": 2500}, "stress": 5, "education": 1, "lesson": "Comprar tiempo", "interpretation": "Delegar convierte un trabajo en un mini-negocio. El margen baja, el sistema sube."},
            "pass": {"label": "Rechazar por energia", "stress": -5, "lesson": "Sostenibilidad", "interpretation": "Cuidar energia es cuidar capacidad productiva futura."},
        },
    },
    {
        "id": "semi_annual_bonus",
        "category": "Income",
        "phase": "growth",
        "title": "Bonus semestral",
        "description": "Tu empresa reparte utilidades. Puedes quemarlo, invertirlo o atacar deuda.",
        "actions": {
            "invest": {"label": "Invertir el bonus ${cash:,.0f}", "label_fmt": "Invertir el bonus ${cash:,.0f}", "cash": {"factor": -0.2, "min": -3000, "max": -300}, "asset": {"name": "Inversion bonus", "type": "Paper assets", "value": {"factor": 0.22, "min": 300, "max": 3500}, "income": 10, "risk": "market"}, "lesson": "Ingreso extraordinario", "interpretation": "El bonus no es salario. Es semilla. Invertirlo lo convierte en futuro."},
            "pay_debt": {"label": "Atacar deuda con el bonus", "cash": {"factor": -0.2, "min": -3000, "max": -300}, "pay_debt": {"factor": 0.2, "min": 300, "max": 3000}, "stress": -4, "lesson": "Desapalancamiento", "interpretation": "Usar ingreso extraordinario para bajar deuda es el doble retorno: liberas flujo y reduces riesgo."},
            "spend": {"label": "Gastarlo en algo deseado", "cash": {"factor": 0.2, "min": 300, "max": 3000}, "stress": -6, "lifestyle": 1, "lesson": "Inflacion de estilo", "interpretation": "El bonus se fue. La satisfaccion tambien. Lo que queda es el habito de esperar el proximo."},
        },
    },
    {
        "id": "big_commission",
        "category": "Income",
        "phase": "growth",
        "title": "Comision inesperadamente grande",
        "description": "Cerraste un deal grande. La comision supera lo normal. La tentacion de subir estilo de vida acecha.",
        "actions": {
            "save": {"label": "Guardar el 80% en reserva", "cash": {"factor": 0.05, "min": 100, "max": 1000}, "stress": -3, "lesson": "Reserva estrategica", "interpretation": "Las comisiones grandes son picos, no promedio. Tratarlas como promedio es peligroso."},
            "invest": {"label": "Invertir en activo", "cash": {"factor": -0.25, "min": -4000, "max": -500}, "asset": {"name": "Inversion comision", "type": "Paper assets", "value": {"factor": 0.28, "min": 500, "max": 5000}, "income": 12, "risk": "market"}, "lesson": "Pico a activo", "interpretation": "Convertir un pico en flujo recurrente es el movimiento del paciente."},
            "upgrade": {"label": "Subir estilo de vida", "expenses": {"factor": 0.05, "min": 100, "max": 600}, "stress": -8, "lifestyle": 1, "lesson": "Trampa del pico", "interpretation": "La comision se fue. El gasto nuevo se quedo anos. El timing es el peor posible."},
        },
    },
    {
        "id": "royalties",
        "category": "Income",
        "phase": "freedom",
        "title": "Oferta de royalties por tu trabajo",
        "description": "Alguien quiere licenciar tu contenido o producto. Es ingreso pasivo real, pero depends de terceros.",
        "actions": {
            "license": {"label": "Licenciar y cobrar royalties", "asset": {"name": "Royalties", "type": "Paper assets", "value": 0, "income": {"factor": 0.05, "min": 50, "max": 800}, "risk": "high"}, "stress": -3, "lesson": "Ingreso pasivo real", "interpretation": "Los royalties no garantizados son la forma mas pura de ingreso pasivo: sistema, no tiempo."},
            "sell_all": {"label": "Vender los derechos por lump sum", "cash": {"factor": 0.8, "min": 3000, "max": 40000}, "stress": 2, "lesson": "Liquidez cierta", "interpretation": "Cobrar hoy garantiza monto. Renuncias al upside futuro."},
            "pass": {"label": "No ceder tu obra", "stress": 3, "lesson": "Control", "interpretation": "Mantener control es mantener opcion. Tambien es mantener todo el riesgo."},
        },
    },
    {
        "id": "salary_renegotiation",
        "category": "Income",
        "phase": "survival",
        "title": "Revision salarial anual",
        "description": "Es momento de negociar. Tu argumento y tu alternativa definen el resultado.",
        "actions": {
            "data": {"label": "Negociar con datos", "salary": {"factor": 0.08, "min": 100, "max": 1200}, "education": 1, "stress": 2, "lesson": "Negociacion informada", "interpretation": "Negociar con datos es un salary hack repetible. No es suerte, es preparacion."},
            "soft": {"label": "Pedir sin argumento fuerte", "salary": {"factor": 0.03, "min": 50, "max": 500}, "stress": 4, "lesson": "Pedir sin palanca", "interpretation": "Sin alternativa ni datos, la negociacion es un deseo."},
            "wait": {"label": "No pedir y esperar reconocimiento", "stress": 5, "lesson": "Espera pasiva", "interpretation": "El reconocimiento rara vez llega solo. El salario estancado es el costo del silencio."},
        },
    },
    {
        "id": "second_job",
        "category": "Income",
        "phase": "survival",
        "title": "Oportunidad de segundo empleo",
        "description": "Puedes sumar un trabajo nocturno o de fin de semana. Duplicas ingreso, divides energia.",
        "actions": {
            "take": {"label": "Tomar segundo trabajo", "salary": {"factor": 0.2, "min": 300, "max": 2000}, "stress": 15, "lesson": "Ingreso vs salud", "interpretation": "El segundo trabajo resuelve caja y romte energia. No es sostenible mas de 6 meses."},
            "side": {"label": "Proyecto lateral chico", "salary": {"factor": 0.08, "min": 100, "max": 800}, "stress": 6, "lesson": "Margen", "interpretation": "Un proyecto lateral chico suma caja sin romper el ritmo principal."},
            "rest": {"label": "No sacrificar descanso", "stress": -6, "lesson": "Sostenibilidad", "interpretation": "Cuidar energia ahora puede significar mejor negociacion y foco despues."},
        },
    },
    {
        "id": "equity_grant",
        "category": "Income",
        "phase": "growth",
        "title": "Stock options de tu empresa",
        "description": "Tu empresa te ofrece equity. Es promesa, no caja. El vesting toma años.",
        "actions": {
            "accept": {"label": "Aceptar y esperar vesting", "asset": {"name": "Stock options", "type": "Paper assets", "value": {"factor": 0.5, "min": 5000, "max": 60000}, "income": 0, "risk": "very high"}, "salary": {"factor": -0.05, "min": -800, "max": -100}, "stress": 4, "lesson": "Ingreso diferido", "interpretation": "Aceptar equity es apostar por la empresa. No es salario, es loteria con informacion."},
            "cash_now": {"label": "Negociar mas salario sin equity", "salary": {"factor": 0.1, "min": 200, "max": 1500}, "lesson": "Caja cierta", "interpretation": "Preferir caja hoy es conservador. A veces aburrido es seguro."},
            "mix": {"label": "Mix de salario y equity", "salary": {"factor": 0.05, "min": 100, "max": 800}, "asset": {"name": "Stock options parcial", "type": "Paper assets", "value": {"factor": 0.2, "min": 2000, "max": 25000}, "income": 0, "risk": "very high"}, "stress": 2, "lesson": "Diversificacion", "interpretation": "El mix captura upside sin renunciar a todo el salario."},
        },
    },
    {  # --- Expense +8 ---
        "id": "moving_expense",
        "category": "Expense",
        "phase": "survival",
        "title": "Mudanza forzada",
        "description": "Tu contrato termina o el propietario vende. Mudarte tiene costo inicial, pero puede mejorar tu flujo.",
        "actions": {
            "cheap": {"label": "Mudanza economica ${cash:,.0f}", "label_fmt": "Mudanza economica ${cash:,.0f}", "cash": {"factor": -0.1, "min": -2000, "max": -300}, "expenses": {"factor": -0.03, "min": -150, "max": -20}, "stress": 6, "lesson": "Costo inicial vs flujo", "interpretation": "Mudarte duele una vez. El alquiler mas bajo te beneficia todos los meses."},
            "nice": {"label": "Mudarte a algo mejor", "cash": {"factor": -0.2, "min": -4000, "max": -600}, "expenses": {"factor": 0.05, "min": 100, "max": 500}, "stress": 4, "lifestyle": 1, "lesson": "Mejora temporal", "interpretation": "El nuevo lugar se siente bien. El gasto extra se queda anos."},
            "stay": {"label": "Renegociar y quedarte", "expenses": {"factor": 0.03, "min": 50, "max": 300}, "stress": 3, "lesson": "Costo de quedarse", "interpretation": "A veces pagar mas por quedarse es mas barato que mudarse."},
        },
    },
    {
        "id": "wedding",
        "category": "Expense",
        "phase": "growth",
        "title": "Boda o evento grande",
        "description": "Queres festejar un hito. El costo es real y la presion social empuja hacia arriba.",
        "actions": {
            "big": {"label": "Festejar grande ${cash:,.0f}", "label_fmt": "Festejar grande ${cash:,.0f}", "cash": {"factor": -0.4, "min": -8000, "max": -1500}, "stress": -4, "lifestyle": 1, "lesson": "Gasto emocional", "interpretation": "El recuerdo vale. La caja no vuelve. El habito de gastar por presion social se queda."},
            "modest": {"label": "Evento modesto", "cash": {"factor": -0.15, "min": -3000, "max": -500}, "stress": -2, "lesson": "Proporcionalidad", "interpretation": "Proporcionalidad no es mezquino. Es alinear felicidad con futuro."},
            "skip": {"label": "No festejar y ahorrar", "cash": {"factor": 0.05, "min": 100, "max": 1000}, "stress": 4, "lesson": "Prioridad", "interpretation": "Priorizar futuro sobre fiesta no es popular. A veces es sabio."},
        },
    },
    {
        "id": "baby_arrival",
        "category": "Expense",
        "phase": "growth",
        "title": "Llega un hijo/a",
        "description": "Tu familia crece. Los gastos suben y tu tiempo se reduce drasticamente.",
        "actions": {
            "prepare": {"label": "Adaptar presupuesto", "expenses": {"factor": 0.15, "min": 300, "max": 1500}, "stress": 6, "lesson": "Reestructura", "interpretation": "Un hijo cambia todo. El presupuesto que no se adapta se rompe solo."},
            "downsize": {"label": "Recortar otros gastos", "expenses": {"factor": 0.08, "min": 150, "max": 800}, "stress": 8, "education": 1, "lesson": "Tradeoff real", "interpretation": "Subir gastos por hijo y no recortar otros es inflacion de estilo sin control."},
            "keep_lifestyle": {"label": "Mantener estilo de vida", "expenses": {"factor": 0.2, "min": 400, "max": 2000}, "stress": 12, "lifestyle": 1, "lesson": "Negacion", "interpretation": "No adaptar el presupuesto no evita el gasto. Lo empuja a deuda."},
        },
    },
    {
        "id": "dream_trip",
        "category": "Expense",
        "phase": "growth",
        "title": "Viaje soñado",
        "description": "Siempre quisiste hacer este viaje. La oportunidad aparece ahora. ¿Es momento?",
        "actions": {
            "go": {"label": "Hacer el viaje ${cash:,.0f}", "label_fmt": "Hacer el viaje ${cash:,.0f}", "cash": {"factor": -0.25, "min": -5000, "max": -800}, "stress": -10, "lesson": "Experiencia vs activo", "interpretation": "El viaje nutre el alma. No construye patrimonio. Ambos son validos, no siempre simultaneos."},
            "plan": {"label": "Planificar para el proximo año", "stress": -2, "education": 1, "lesson": "Paciencia", "interpretation": "Postergar no es renunciar. Es llegar con mas caja y menos culpa."},
            "debt_travel": {"label": "Viajar a crédito", "debt": {"name": "Deuda viaje", "type": "Credit card", "balance": {"factor": 0.25, "min": 800, "max": 5000}, "payment": 120, "rate": 0.32, "stress": 8}, "stress": 5, "lifestyle": 1, "lesson": "Memoria con interes", "interpretation": "El viaje se acaba en dos semanas. La cuota dura dos años."},
        },
    },
    {
        "id": "pet_cost",
        "category": "Expense",
        "phase": "survival",
        "title": "Adoptar una mascota",
        "description": "Queres un animal. El cariño es gratis, el mantenimiento no.",
        "actions": {
            "adopt": {"label": "Adoptar", "expenses": {"factor": 0.03, "min": 50, "max": 250}, "cash": {"factor": -0.05, "min": -800, "max": -100}, "stress": -6, "lesson": "Gasto recurrente", "interpretation": "La mascota da compania. Tambien da gastos fixos por 10-15 años."},
            "foster": {"label": "Hogar temporal", "expenses": {"factor": 0.01, "min": 20, "max": 80}, "stress": -3, "lesson": "Compromiso acotado", "interpretation": "Hogar temporal prueba la opcion sin asumir 15 años de gasto."},
            "wait": {"label": "Noadoptar ahora", "stress": 2, "lesson": "Timing", "interpretation": "El amor por animales no cambia. Tu situacion financiera si. Esperar es valido."},
        },
    },
    {
        "id": "subscription_creep",
        "category": "Expense",
        "phase": "growth",
        "title": "Auditoria de suscripciones",
        "description": "Te das cuenta que acumulas servicios mensuales que no usas. El drip silencioso drena flujo.",
        "actions": {
            "cut": {"label": "Cancelar todo lo que no usas", "expenses": {"factor": -0.04, "min": -200, "max": -30}, "stress": -2, "lesson": "Drip control", "interpretation": "Los gastos invisibles son los mas caros. Auditarlos es retorno garantizado."},
            "keep": {"label": "Mantener por comodidad", "stress": 1, "lesson": "Inercia", "interpretation": "La inercia es el mayor costo recurrente. Pagar por no decidir es caro."},
            "negotiate": {"label": "Renegociar planes", "expenses": {"factor": -0.02, "min": -100, "max": -15}, "education": 1, "lesson": "Negociacion pasiva", "interpretation": "Llamar para renegociar es de los pocos retornos garantizados por hora."},
        },
    },
    {
        "id": "therapy",
        "category": "Expense",
        "phase": "growth",
        "title": "Consideras ir a terapia",
        "description": "El estres sube. Un profesional puede ayudar, pero es gasto mensual recurrente.",
        "actions": {
            "go": {"label": "Iniciar terapia", "expenses": {"factor": 0.04, "min": 80, "max": 400}, "stress": -15, "education": 1, "lesson": "Inversion mental", "interpretation": "La terapia es gasto que libera energia. La energia es el activo mas oculto."},
            "self": {"label": "Auto-gestion con libros", "cash": {"factor": -0.02, "min": -300, "max": -50}, "education": 1, "stress": -4, "lesson": "Autonomia", "interpretation": "La auto-gestion funciona para nivel medio. No reemplaza ayuda profesional en crisis."},
            "ignore": {"label": "No hacer nada", "stress": 10, "lesson": "Costo de ignorar", "interpretation": "El estres no atendido no desaparece. Se cobra en decisiones y salud."},
        },
    },
    {
        "id": "celebration",
        "category": "Expense",
        "phase": "survival",
        "title": "Fiesta por un logro",
        "description": "Algo bueno paso. Queres celebrar. La intensidad de la fiesta define el impacto financiero.",
        "actions": {
            "small": {"label": "Celebracion modesta", "cash": {"factor": -0.05, "min": -800, "max": -100}, "stress": -5, "lesson": "Proporcion", "interpretation": "Celebra el avance sin comprometer el proximo paso."},
            "big": {"label": "Fiesta grande", "cash": {"factor": -0.2, "min": -3000, "max": -500}, "stress": -8, "lifestyle": 1, "lesson": "Recompensa excesiva", "interpretation": "La recompensa excesiva por un logro chico genera expectativa de gasto futuro."},
            "invest_celebrate": {"label": "Invertir el monto de la fiesta", "cash": {"factor": -0.03, "min": -500, "max": -50}, "asset": {"name": "Inversion celebracion", "type": "Paper assets", "value": {"factor": 0.05, "min": 50, "max": 600}, "income": 3, "risk": "market"}, "stress": -3, "lesson": "Doble victoria", "interpretation": "Celebra construyendo futuro. No es la fiesta mas divertida, pero el yo del futuro agradece."},
        },
    },
    {  # --- Investment +12 ---
        "id": "bonds",
        "category": "Investment",
        "phase": "growth",
        "title": "Bonos corporativos con yield atractiva",
        "description": "Bonos de empresa solida pagan mas que el mercado. Es ingreso fijo, pero con riesgo de credito.",
        "actions": {
            "buy": {"label": "Comprar bonos ${cash:,.0f}", "label_fmt": "Comprar bonos ${cash:,.0f}", "cash": {"factor": -0.3, "min": -6000, "max": -800}, "asset": {"name": "Bonos corporativos", "type": "Paper assets", "value": {"factor": 0.32, "min": 800, "max": 6500}, "income": 25, "risk": "market"}, "lesson": "Ingreso fijo", "interpretation": "Los bonos dan flujo predecible. El riesgo de credito no es cero, es menos visible."},
            "mix": {"label": "Solo una porcion pequena", "cash": {"factor": -0.1, "min": -2000, "max": -300}, "asset": {"name": "Bonos parcial", "type": "Paper assets", "value": {"factor": 0.11, "min": 300, "max": 2200}, "income": 10, "risk": "market"}, "lesson": "Diversificacion", "interpretation": "No pongas todo en un emisor. El rendimiento extra no justifica riesgo concentrado."},
            "pass": {"label": "No comprar", "stress": -1, "lesson": "Simpleza", "interpretation": "No todo yield atractivo es oportunidad. A veces es trampa con buen marketing."},
        },
    },
    {
        "id": "sector_etf",
        "category": "Investment",
        "phase": "growth",
        "title": "ETF sectorial en tendencia",
        "description": "Un sectorpecifico esta en racha. El ETF promete exposure sin elegir acciones individuales.",
        "actions": {
            "buy": {"label": "Comprar ETF sectorial", "cash": {"factor": -0.2, "min": -4000, "max": -500}, "asset": {"name": "ETF sectorial", "type": "Paper assets", "value": {"factor": 0.22, "min": 500, "max": 4500}, "income": 8, "risk": "high"}, "stress": 3, "lesson": "Concentracion sectorial", "interpretation": "El ETF diversifica dentro del sector. Pero el sector mismo es una sola apuesta."},
            "broad": {"label": "Comprar ETF amplio en su lugar", "cash": {"factor": -0.2, "min": -4000, "max": -500}, "asset": {"name": "ETF amplio", "type": "Paper assets", "value": {"factor": 0.22, "min": 500, "max": 4500}, "income": 12, "risk": "market"}, "lesson": "Diversificacion real", "interpretation": "El ETF amplio captura el mercado. Menos emocion, mas solidez."},
            "wait": {"label": "Esperar", "stress": -1, "lesson": "Trend chasing", "interpretation": "Seguir tendencias es comprar despues de que subio. El FOMO no es estrategia."},
        },
    },
    {
        "id": "land_plot",
        "category": "Investment",
        "phase": "freedom",
        "title": "Terreno en zona de expansion",
        "description": "Un terreno barato en zona que se esta desarrollando. No genera income, apuesta a revalorizacion.",
        "actions": {
            "buy": {"label": "Comprar terreno ${cash:,.0f}", "label_fmt": "Comprar terreno ${cash:,.0f}", "cash": {"factor": -0.35, "min": -8000, "max": -1500}, "asset": {"name": "Terreno", "type": "Real estate", "value": {"factor": 0.4, "min": 1500, "max": 9000}, "income": 0, "risk": "vacancy"}, "stress": 4, "lesson": "Especulacion inmobiliaria", "interpretation": "El terreno no genera flujo. Su valor depende de que otros desarrollen alrededor."},
            "finance": {"label": "Comprar con credito", "cash": {"factor": -0.1, "min": -2500, "max": -400}, "asset": {"name": "Terreno financiado", "type": "Real estate", "value": {"factor": 0.4, "min": 1500, "max": 9000}, "income": 0, "risk": "vacancy"}, "debt": {"name": "Credito terreno", "type": "Mortgage", "balance": {"factor": 0.25, "min": 1000, "max": 6000}, "payment": 180, "rate": 0.1, "stress": 6}, "lesson": "Apalancar especulacion", "interpretation": "Financiar un activo sin flujo es doble riesgo. Si no se revaloriza, tenes deuda sin income."},
            "pass": {"label": "No comprar", "stress": -2, "lesson": "Oportunidad vs timing", "interpretation": "El terreno puede revalorizar. Tambien puede estancarse 10 años. Sin flujo, el costo de oportunidad es alto."},
        },
    },
    {
        "id": "franchise",
        "category": "Investment",
        "phase": "freedom",
        "title": "Franquicia con marca conocida",
        "description": "Puedes abrir una franquicia. La marca ayuda, pero el costo inicial y el royalty comen margen.",
        "actions": {
            "buy": {"label": "Comprar franquicia ${cash:,.0f}", "label_fmt": "Comprar franquicia ${cash:,.0f}", "cash": {"factor": -0.4, "min": -15000, "max": -3000}, "asset": {"name": "Franquicia", "type": "Small business", "value": {"factor": 0.5, "min": 4000, "max": 20000}, "income": 320, "risk": "execution"}, "expenses": {"factor": 0.02, "min": 50, "max": 300}, "stress": 8, "lesson": "Negocio con plantilla", "interpretation": "La franquicia reduce riesgo de ejecucion pero limita upside. Es un trabajo disfrazado de activo."},
            "partner": {"label": "Entrar con socio", "cash": {"factor": -0.15, "min": -6000, "max": -1000}, "asset": {"name": "Franquicia 50/50", "type": "Small business", "value": {"factor": 0.25, "min": 2000, "max": 10000}, "income": 160, "risk": "execution"}, "stress": 5, "education": 1, "lesson": "Socio", "interpretation": "Un socio divide costo y riesgo. Tambien divide control y ganancia."},
            "pass": {"label": "No comprar", "stress": -2, "lesson": "Independencia", "interpretation": "La franquicia no es libertad financiera. Es un trabajo con mas overhead."},
        },
    },
    {
        "id": "private_fund",
        "category": "Investment",
        "phase": "freedom",
        "requires_education": 5,
        "title": "Fondo privado con acceso restringido",
        "description": "Un fondo privado ofrece estrategias no disponibles al publico. Requiere ticket grande y conocimiento.",
        "actions": {
            "commit": {"label": "Comprometer capital ${cash:,.0f}", "label_fmt": "Comprometer capital ${cash:,.0f}", "cash": {"factor": -0.5, "min": -20000, "max": -5000}, "asset": {"name": "Fondo privado", "type": "Paper assets", "value": {"factor": 0.55, "min": 5000, "max": 22000}, "income": 45, "risk": "high"}, "stress": 5, "lesson": "Iliquidez premium", "interpretation": "El fondo privado cobra por iliquidez. El retorno extra es real, pero el capital no se toca por años."},
            "wait": {"label": "Esperar mejor momento", "stress": -1, "lesson": "Paciencia informada", "interpretation": "Con conocimiento, esperar tambien es una decision analitica, no miedo."},
            "small_ticket": {"label": "Entrar con ticket minimo", "cash": {"factor": -0.2, "min": -8000, "max": -2000}, "asset": {"name": "Fondo privado small", "type": "Paper assets", "value": {"factor": 0.22, "min": 2000, "max": 9000}, "income": 20, "risk": "high"}, "stress": 3, "lesson": "Tamano de posicion", "interpretation": "Entrar con ticket minimo captura exposure sin comprometer liquidez total."},
        },
    },
    {
        "id": "startup_diligence",
        "category": "Investment",
        "phase": "freedom",
        "requires_education": 5,
        "title": "Startup con acceso a datos internos",
        "description": "Tu educacion te da acceso a una startup con metricas reales. No es promesa, es dato.",
        "actions": {
            "invest": {"label": "Invertir con diligence ${cash:,.0f}", "label_fmt": "Invertir con diligence ${cash:,.0f}", "cash": {"factor": -0.3, "min": -10000, "max": -2000}, "asset": {"name": "Equity con diligence", "type": "Small business", "value": {"factor": 0.25, "min": 1500, "max": 8000}, "income": 0, "risk": "very high"}, "stress": 4, "lesson": "Inversion informada", "interpretation": "La education no elimina riesgo. Transforma apuesta ciega en apuesta calculada.", "delayed": [{"delay": 24, "label": "Startup cierra (60%)", "source": "Startup con diligence", "effect": {"asset_fail_chance": {"name": "Equity con diligence", "prob": 0.6}}}]},
            "advise": {"label": "Asesorar por equity", "cash": {"factor": -0.02, "min": -500, "max": -50}, "asset": {"name": "Equity asesor", "type": "Small business", "value": {"factor": 0.1, "min": 500, "max": 4000}, "income": 0, "risk": "very high"}, "stress": 6, "lesson": "Sweat equity", "interpretation": "Asesorar por equity es convertir conocimiento en posicion sin desembolsar capital.", "delayed": [{"delay": 24, "label": "Startup cierra (60%)", "source": "Startup con diligence", "effect": {"asset_fail_chance": {"name": "Equity asesor", "prob": 0.6}}}]},
            "pass": {"label": "No invertir", "stress": 0, "lesson": "Disciplina", "interpretation": "Tener data no obliga a invertir. La disciplina es saber decir no con informacion."},
        },
    },
    {
        "id": "art_collectible",
        "category": "Investment",
        "phase": "freedom",
        "title": "Obra de arte o coleccionable",
        "description": "Una pieza cotizada podria revalorizar. No genera income y su liquidez es impredecible.",
        "actions": {
            "buy": {"label": "Comprar pieza ${cash:,.0f}", "label_fmt": "Comprar pieza ${cash:,.0f}", "cash": {"factor": -0.2, "min": -5000, "max": -1000}, "asset": {"name": "Arte/coleccional", "type": "Paper assets", "value": {"factor": 0.22, "min": 1000, "max": 5500}, "income": 0, "risk": "high"}, "stress": 3, "lesson": "Inversion pasional", "interpretation": "El arte es inversion solo para quien entiende el mercado. Para el resto es decoracion cara."},
            "fund": {"label": "Fondo de arte fraccionado", "cash": {"factor": -0.05, "min": -1500, "max": -300}, "asset": {"name": "Fondo arte", "type": "Paper assets", "value": {"factor": 0.06, "min": 300, "max": 1600}, "income": 0, "risk": "high"}, "lesson": "Exposure sin illiquidez", "interpretation": "El fraccionamiento da exposure sin bloquear capital. Sigue siendo especulacion."},
            "pass": {"label": "No comprar", "stress": -1, "lesson": "Foco", "interpretation": "No toda clase de activo es para todos. El foco es un filtro, no una limitacion."},
        },
    },
    {
        "id": "green_investment",
        "category": "Investment",
        "phase": "growth",
        "title": "Fondo de inversion verde",
        "description": "Un fondo enfocado en transicion energetica promete impacto y retorno. El green premium puede ser real o marketing.",
        "actions": {
            "invest": {"label": "Invertir ${cash:,.0f}", "label_fmt": "Invertir ${cash:,.0f}", "cash": {"factor": -0.2, "min": -4000, "max": -500}, "asset": {"name": "Fondo verde", "type": "Paper assets", "value": {"factor": 0.22, "min": 500, "max": 4500}, "income": 9, "risk": "market"}, "stress": -2, "lesson": "Impacto + retorno", "interpretation": "El impacto real existe. El retorno depende de que el fondo sea solido, no solo verde."},
            "verify": {"label": "Verificar y decidir despues", "cash": {"factor": -0.02, "min": -300, "max": -50}, "education": 1, "stress": -1, "lesson": "Greenwashing", "interpretation": "No todo verde es verde. Verificar es proteccion, no escepticismo."},
            "pass": {"label": "No invertir", "stress": 0, "lesson": "Filtro personal", "interpretation": "Podes creer en la causa y no invertir. No son lo mismo."},
        },
    },
    {
        "id": "reit",
        "category": "Investment",
        "phase": "growth",
        "title": "REIT con yield mensual",
        "description": "Un REIT te da exposure inmobiliaria sin gestion directa. Es liquido, pero sensible a tasas.",
        "actions": {
            "buy": {"label": "Comprar REIT ${cash:,.0f}", "label_fmt": "Comprar REIT ${cash:,.0f}", "cash": {"factor": -0.25, "min": -5000, "max": -600}, "asset": {"name": "REIT", "type": "Paper assets", "value": {"factor": 0.27, "min": 600, "max": 5500}, "income": 22, "risk": "market"}, "lesson": "Inmobiliario sin friccion", "interpretation": "El REIT da lo bueno del inmobiliario (flujo) sin lo malo (inquilinos, mantenimientos)."},
            "direct": {"label": "Comprar propiedad directa en su lugar", "cash": {"factor": -0.4, "min": -8000, "max": -2000}, "asset": {"name": "Propiedad directa", "type": "Real estate", "value": {"factor": 1.0, "min": 20000, "max": 80000}, "income": 250, "risk": "vacancy"}, "debt": {"name": "Hipoteca REIT alt", "type": "Mortgage", "balance": {"factor": 0.6, "min": 12000, "max": 60000}, "payment": 580, "rate": 0.07, "stress": 7}, "stress": 6, "lesson": "Friccion vs control", "interpretation": "La propiedad directa da control y friccion. El REIT da simplicidad y menor upside."},
            "pass": {"label": "No invertir ahora", "stress": -1, "lesson": "Paciencia", "interpretation": "Esperar mejor entrada no es miedo. Es timing."},
        },
    },
    {
        "id": "peer_lending",
        "category": "Investment",
        "phase": "growth",
        "title": "Plataforma de peer lending",
        "description": "Prestas directamente a personas o pymes. Yield mas alto que bonos, riesgo de default mas alto.",
        "actions": {
            "lend": {"label": "Prestar ${cash:,.0f}", "label_fmt": "Prestar ${cash:,.0f}", "cash": {"factor": -0.2, "min": -4000, "max": -500}, "asset": {"name": "Peer lending", "type": "Paper assets", "value": {"factor": 0.22, "min": 500, "max": 4500}, "income": 28, "risk": "high"}, "lesson": "Riesgo de credito directo", "interpretation": "El yield extra es real. El default tambien. Diversificar entre prestatarios es clave."},
            "diversify": {"label": "Prestar en pequenas partes", "cash": {"factor": -0.1, "min": -2000, "max": -300}, "asset": {"name": "Peer lending diversificado", "type": "Paper assets", "value": {"factor": 0.11, "min": 300, "max": 2200}, "income": 14, "risk": "high"}, "lesson": "Diversificar default", "interpretation": "Repartir entre muchos prestatarios reduce el impacto de un solo default."},
            "pass": {"label": "No prestar", "stress": -1, "lesson": "Riesgo no transparente", "interpretation": "El riesgo de default en peer lending no es siempre visible. La opacidad es un costo."},
        },
    },
    {
        "id": "crypto",
        "category": "Investment",
        "phase": "growth",
        "title": "Cripto en tendencia",
        "description": "Una cripto prometedora aparece en tu radar. Volatilidad extrema, potencial alto, riesgo total.",
        "actions": {
            "small": {"label": "Posicion pequena ${cash:,.0f}", "label_fmt": "Posicion pequena ${cash:,.0f}", "cash": {"factor": -0.05, "min": -1500, "max": -200}, "asset": {"name": "Cripto small", "type": "Paper assets", "value": {"factor": 0.06, "min": 200, "max": 1500}, "income": 0, "risk": "very high"}, "stress": 4, "lesson": "Tamano de posicion", "interpretation": "Una posicion pequena en asset extremo puede sumar upside sin comprometer solvencia."},
            "big": {"label": "Posicion grande", "cash": {"factor": -0.3, "min": -8000, "max": -1500}, "asset": {"name": "Cripto big", "type": "Paper assets", "value": {"factor": 0.35, "min": 1500, "max": 9000}, "income": 0, "risk": "very high"}, "stress": 12, "lesson": "Concentracion extrema", "interpretation": "Una posicion grande en cripto no es inversion, es apuesta. La volatilidad te puede liquidar.", "delayed": [{"delay": 12, "label": "Crypto cae 70% (50%)", "source": "Cripto", "effect": {"asset_drop": "Cripto big", "percent": 0.7}}]},
            "pass": {"label": "No invertir", "stress": -1, "lesson": "Foco", "interpretation": "No entender un activo es razon valido para no invertir. El FOMO no es tesis."},
        },
    },
    {
        "id": "impact_fund",
        "category": "Investment",
        "phase": "freedom",
        "requires_education": 3,
        "title": "Fondo de impacto social",
        "description": "Un fondo mide retorno financiero y impacto social. Tu educacion te permite leer debajo del marketing.",
        "actions": {
            "invest": {"label": "Invertir ${cash:,.0f}", "label_fmt": "Invertir ${cash:,.0f}", "cash": {"factor": -0.25, "min": -6000, "max": -1000}, "asset": {"name": "Fondo impacto", "type": "Paper assets", "value": {"factor": 0.27, "min": 1000, "max": 6500}, "income": 16, "risk": "market"}, "stress": -3, "lesson": "Doble retorno", "interpretation": "El fondo de impacto real alinea interes financiero y social. El de marketing solo cobra fee."},
            "verify": {"label": "Verificar metricas de impacto", "cash": {"factor": -0.03, "min": -500, "max": -100}, "education": 1, "lesson": "Diligence", "interpretation": "Leer metricas reales separa fondo serio de greenwashing social."},
            "pass": {"label": "No invertir", "stress": 0, "lesson": "Foco", "interpretation": "El impacto es valido. No es obligatorio para toda tu cartera."},
        },
    },
    {  # --- Debt +5 ---
        "id": "consolidation",
        "category": "Debt",
        "phase": "survival",
        "requires_debt": True,
        "title": "Consolidacion de deudas",
        "description": "Un banco ofrece consolidar todas tus deudas en un solo pago, con tasa menor.",
        "actions": {
            "consolidate": {"label": "Consolidar todo", "reduce_debt_payments": 0.22, "credit_score": 8, "stress": -5, "lesson": "Flujo liberado", "interpretation": "Consolidar libera flujo. El costo total puede subir si extendes plazo demais."},
            "reject": {"label": "Mantener deudas separadas", "lesson": "Control granular", "interpretation": "Mantener deudas separadas te deja atacar la mas cara primero. Es mas trabajo, mas control."},
            "partial": {"label": "Solo consolidar tarjeta", "cash": {"factor": -0.02, "min": -500, "max": -50}, "reduce_debt_payments": 0.1, "credit_score": 3, "stress": -2, "lesson": "Consolidacion selectiva", "interpretation": "Consolidar solo la deuda cara es el mejor de ambos mundos."},
        },
    },
    {
        "id": "balance_transfer",
        "category": "Debt",
        "phase": "survival",
        "requires_debt": True,
        "requires_world": ["Expansion", "Estable"],
        "title": "Balance transfer a tasa 0%",
        "description": "Otra tarjeta ofrece 0% por 12 meses si transfieres tu saldo. Es trampa o puente?",
        "actions": {
            "transfer": {"label": "Transferir saldo", "credit_score": 5, "stress": -6, "lesson": "Puente temporal", "interpretation": "El 0% es real. La trampa es no pagar antes de que termine y la tasa suba al doble.", "delayed": [{"delay": 12, "label": "Tasa promocional expira (+18%)", "source": "Balance transfer", "effect": {"debt_rate_hike": "Nueva tarjeta", "delta": 0.18}}]},
            "pay_now": {"label": "No transferir y pagar agresivo", "cash": {"factor": -0.15, "min": -3000, "max": -300}, "pay_debt": {"factor": 0.15, "min": 300, "max": 3000}, "stress": -3, "lesson": "Ataque directo", "interpretation": "Atacar la deuda sin trucos es mas duro y mas limpio."},
            "ignore": {"label": "Ignorar oferta", "stress": 1, "lesson": "Costo de oportunidad", "interpretation": "El 0% es una herramienta. Ignorarla por desorganizacion es tan malo como abusar de ella."},
        },
    },
    {
        "id": "family_loan",
        "category": "Debt",
        "phase": "survival",
        "title": "Familiar te ofrece prestar",
        "description": "Un familiar con dinero te ofrece un prestamo sin interes. Es puente o cuerda?",
        "actions": {
            "accept": {"label": "Aceptar prestamo familiar", "cash": {"factor": 0.3, "min": 500, "max": 6000}, "debt": {"name": "Prestamo familiar", "type": "Personal loan", "balance": {"factor": 0.3, "min": 500, "max": 6000}, "payment": 0, "rate": 0.0, "stress": 6}, "stress": 4, "lesson": "Deuda emocional", "interpretation": "Sin interes es bueno financieramente. El costo emocional no aparece en la planilla."},
            "formalize": {"label": "Aceptar con contrato formal", "cash": {"factor": 0.3, "min": 500, "max": 6000}, "debt": {"name": "Prestamo familiar formal", "type": "Personal loan", "balance": {"factor": 0.3, "min": 500, "max": 6000}, "payment": {"factor": 0.02, "min": 30, "max": 300}, "rate": 0.03, "stress": 2}, "education": 1, "lesson": "Formalidad", "interpretation": "Formalizar protege la relacion y el dinero. Lo informal se vuelve conflicto."},
            "decline": {"label": "Rechazar por relacion", "stress": -2, "lesson": "Independencia", "interpretation": "Mezclar familia y dinero no siempre rompe. Pero cuando rompe, rompe doble."},
        },
    },
    {
        "id": "line_of_credit",
        "category": "Debt",
        "phase": "growth",
        "requires_debt_free": True,
        "title": "Linea de credito preaprobada",
        "description": "El banco te aprueba una linea flexible. No la pediste, pero esta ahi. Es seguridad o tentacion?",
        "actions": {
            "keep_unused": {"label": "Menerla sin usar", "credit_score": 10, "stress": -3, "lesson": "Opcion sin costo", "interpretation": "Una linea sin usar mejora tu credit score y tu paz mental. No usar credito es un superpoder."},
            "use_for_opportunity": {"label": "Usar para oportunidad", "cash": {"factor": -0.2, "min": -5000, "max": -500}, "asset": {"name": "Inversion con linea", "type": "Paper assets", "value": {"factor": 0.22, "min": 500, "max": 5500}, "income": 14, "risk": "market"}, "debt": {"name": "Linea usada", "type": "Investment loan", "balance": {"factor": 0.2, "min": 500, "max": 5000}, "payment": 80, "rate": 0.14, "stress": 5}, "lesson": "Deuda como palanca", "interpretation": "Usar linea para invertir es apalancamiento. Funciona hasta que no funciona."},
            "close": {"label": "Cerrar la linea", "stress": 2, "credit_score": -5, "lesson": "Foco", "interpretation": "Cerrar credito no usado baja score. Tambien baja tentacion. Es un tradeoff valido."},
        },
    },
    {
        "id": "mortgage_refi_opportunity",
        "category": "Debt",
        "phase": "freedom",
        "requires_asset_type": "Real estate",
        "requires_world": ["Recuperacion", "Expansion"],
        "title": "Refinanciar hipoteca con tasas bajas",
        "description": "Las tasas bajaron. Podes refinanciar tu hipoteca y ahorrar miles en intereses.",
        "actions": {
            "refi": {"label": "Refinanciar a tasa menor", "reduce_debt_payments": 0.15, "credit_score": 5, "stress": -4, "cash": {"factor": -0.03, "min": -800, "max": -100}, "lesson": "Timing de tasas", "interpretation": "Refinanciar cuando tasas bajan es retorno garantizado. No requiere suerte."},
            "shorten": {"label": "Acortar plazo", "reduce_debt_payments": 0.05, "cash": {"factor": -0.08, "min": -1500, "max": -200}, "pay_debt": {"factor": 0.1, "min": 200, "max": 2000}, "stress": 3, "lesson": "Plazo vs costo", "interpretation": "Acortar plazo sube pago mensual pero baja costo total. Es pagar mas hoy para liberar muchos años."},
            "skip": {"label": "No refinanciar", "stress": 1, "lesson": "Inercia", "interpretation": "No actuar ante tasas bajas es dejar dinero sobre la mesa por inercia."},
        },
    },
    {  # --- Knowledge +7 ---
        "id": "mentor",
        "category": "Knowledge",
        "phase": "growth",
        "requires_education": 3,
        "title": "Mentor con experiencia comprobable",
        "description": "Un inversor experimentado te ofrece mentoria. Su conocimiento puede ahorrarte años de errores.",
        "actions": {
            "hire": {"label": "Pagar mentoria ${cash:,.0f}", "label_fmt": "Pagar mentoria ${cash:,.0f}", "cash": {"factor": -0.1, "min": -2000, "max": -300}, "education": 2, "stress": -3, "career_stability": 5, "lesson": "Conocimiento transferido", "interpretation": "Un buen mentor no te da peces. Te ensena a evaluar el mar."},
            "exchange": {"label": "Mentoria por intercambio", "cash": {"factor": -0.02, "min": -300, "max": -50}, "education": 1, "stress": 3, "lesson": "Valor sin dinero", "interpretation": "Ofrecer tus skills a cambio de mentoria es creative deal. No siempre funciona, pero no cuesta probar."},
            "self": {"label": "Seguir aprendiendo solo", "education": 1, "stress": 1, "lesson": "Autonomia", "interpretation": "Aprender solo es posible. Es mas lento y no te protege de errores que un mentor hubiera visto."},
        },
    },
    {
        "id": "book_community",
        "category": "Knowledge",
        "phase": "survival",
        "title": "Libro + comunidad de inversores",
        "description": "Un libro recomendado mas acceso a una comunidad de inversores cuesta poco y abre network.",
        "actions": {
            "buy": {"label": "Comprar libro + acceso", "cash": {"factor": -0.03, "min": -400, "max": -50}, "education": 1, "stress": -2, "lesson": "Aprendizaje barato", "interpretation": "El libro mas recomendado de inversiones cuesta menos que una cena. La comunidad es bonus."},
            "library": {"label": "Pedir prestado en biblioteca", "education": 1, "stress": 1, "lesson": "Costo cero", "interpretation": "La biblioteca es el mejor ROI de la historia. Sin comunidad, pero con el mismo contenido."},
            "pass": {"label": "No leer ahora", "stress": 0, "lesson": "Estancamiento", "interpretation": "Sin ideas nuevas, las decisiones se repiten. El estancamiento es el costo invisible de no aprender."},
        },
    },
    {
        "id": "masterclass",
        "category": "Knowledge",
        "phase": "growth",
        "title": "Masterclass con inversor reconocido",
        "description": "Un inversor publico da una masterclass. El precio es alto, pero el acceso es unico.",
        "actions": {
            "attend": {"label": "Pagar y asistir ${cash:,.0f}", "label_fmt": "Pagar y asistir ${cash:,.0f}", "cash": {"factor": -0.08, "min": -1800, "max": -300}, "education": 2, "stress": -2, "career_stability": 3, "lesson": "Acceso a experiencia", "interpretation": "La masterclass no da secretos. Da frameworks que tomariamos años en construir solos."},
            "replay": {"label": "Comprar la grabacion", "cash": {"factor": -0.02, "min": -400, "max": -50}, "education": 1, "lesson": "Costo de oportunidad", "interpretation": "La grabacion tiene el contenido. No tiene el network ni las preguntas en vivo."},
            "pass": {"label": "No asistir", "stress": 0, "lesson": "Filtro", "interpretation": "No todo conocimiento vale su precio. Filtrar es tambien un skill."},
        },
    },
    {
        "id": "tax_analysis",
        "category": "Knowledge",
        "phase": "growth",
        "requires_education": 3,
        "title": "Revision fiscal profesional",
        "description": "Un contador te ofrece una revision fiscal completa. Tu educacion te permite entender y aplicar.",
        "actions": {
            "hire": {"label": "Pagar revision ${cash:,.0f}", "label_fmt": "Pagar revision ${cash:,.0f}", "cash": {"factor": -0.05, "min": -1200, "max": -200}, "education": 1, "salary": {"factor": 0.05, "min": 50, "max": 800}, "stress": -4, "lesson": "Optimizacion fiscal", "interpretation": "Una buena revision fiscal devuelve mas de lo que cuesta. Solo si aplicas lo que recomienda."},
            "diy": {"label": "Hacerlo solo con software", "cash": {"factor": -0.01, "min": -200, "max": -30}, "education": 1, "stress": 4, "lesson": "Autonomia con riesgo", "interpretation": "Hacerlo solo es mas barato. El riesgo de error es mas caro."},
            "skip": {"label": "No hacer revision", "stress": 2, "lesson": "Costo invisible", "interpretation": "No revisar impuestos es pagar mas de lo que debes. El costo es invisible pero real."},
        },
    },
    {
        "id": "research_paper",
        "category": "Knowledge",
        "phase": "freedom",
        "requires_education": 5,
        "title": "Reporte de investigacion exclusivo",
        "description": "Un reporte profundo sobre un sector especifico esta disponible. Tu educacion te permite aprovecharlo.",
        "actions": {
            "buy": {"label": "Comprar reporte ${cash:,.0f}", "label_fmt": "Comprar reporte ${cash:,.0f}", "cash": {"factor": -0.05, "min": -1500, "max": -200}, "education": 2, "stress": -1, "lesson": "Informacion asimetrica", "interpretation": "El reporte no te da certezas. Te da un borde sobre los que no lo tienen."},
            "summary": {"label": "Comprar solo el resumen", "cash": {"factor": -0.01, "min": -300, "max": -50}, "education": 1, "lesson": "Costo-beneficio", "interpretation": "El resumen tiene 80% del valor por 20% del precio. La ley de Pareto aplica a la informacion."},
            "pass": {"label": "No comprar", "stress": 0, "lesson": "Filtro", "interpretation": "No toda informacion exclusiva es valiosa. A veces es cara y obvia."},
        },
    },
    {
        "id": "online_community",
        "category": "Knowledge",
        "phase": "survival",
        "title": "Comunidad online de finanzas",
        "description": "Una comunidad online de inversores cuesta poco. Es ruido o signal?",
        "actions": {
            "join": {"label": "Unirte y participar", "cash": {"factor": -0.01, "min": -200, "max": -20}, "expenses": {"factor": 0.01, "min": 10, "max": 50}, "education": 1, "stress": -3, "lesson": "Network digital", "interpretation": "La comunidad buena acelera aprendizaje. La mala confirma sesgos y vende cursos."},
            "lurk": {"label": "Solo leer sin participar", "education": 1, "stress": 1, "lesson": "Aprendizaje pasivo", "interpretation": "Leer es mejor que nada. Participar es mejor que leer. Enseñar es mejor que participar."},
            "pass": {"label": "No unirte", "stress": 0, "lesson": "Foco", "interpretation": "Tu tiempo es escaso. Toda comunidad consume tiempo. Elegir es clave."},
        },
    },
    {
        "id": "certification",
        "category": "Knowledge",
        "phase": "growth",
        "title": "Certificacion profesional avanzada",
        "description": "Una certificacion reconocida puede abrir puertas y subir salario. Requiere tiempo y dinero.",
        "actions": {
            "full": {"label": "Hacer la certificacion", "cash": {"factor": -0.1, "min": -2500, "max": -500}, "education": 2, "salary": {"factor": 0.1, "min": 200, "max": 2000}, "career_stability": 10, "stress": 6, "lesson": "Inversion en credenciales", "interpretation": "La certificacion sube salario y credibilidad. El stress del proceso es temporal, el salario es permanente."},
            "partial": {"label": "Solo curso introductorio", "cash": {"factor": -0.03, "min": -800, "max": -100}, "education": 1, "career_stability": 3, "stress": 3, "lesson": "Costo medio", "interpretation": "El curso introductorio da 60% del conocimiento por 30% del costo. No da el papel."},
            "skip": {"label": "No certificar", "stress": -2, "lesson": "Experiencia vs papel", "interpretation": "La experiencia real puede valer mas que el papel. Sin el papel, algunas puertas no se abren."},
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
        "action_used_this_month": {"sell": False, "cut_expenses": False},
        "expense_creep_log": [],
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

    state.pop("last_discretionary_feedback", None)
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
            action["label"] = action["label_fmt"].format(**action)
        except (KeyError, ValueError):
            pass
    return action


def apply_action_effects(state, action):
    state["cash"] += amount(state, action.get("cash", 0))
    state["salary"] += amount(state, action.get("salary", 0))
    exp_delta = amount(state, action.get("expenses", 0))
    state["expenses"] += exp_delta
    if exp_delta > 0:
        state.setdefault("expense_creep_log", []).append({"kind": "creep", "amount": exp_delta, "month": state["month"]})
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


def advance_time(state, months=1):
    months = max(1, int(months))
    for _ in range(months):
        state["month"] += 1
        state["action_used_this_month"] = {"sell": False, "cut_expenses": False}
        process_schedule(state)
        if state["month"] % 12 == 1 and state["month"] > 1:
            state["age"] += 1
            state["salary"] = round(state["salary"] * (1.02 + state["education"] * 0.005), 2)


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
    score = 35 + min(35, max(0, runway) * 4) + state["education"] * 6 + max(0, state["credit_score"] - 600) / 12
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


LIQUIDITY_BY_TYPE = {
    "Paper assets": 0.85,
    "Real estate": 0.70,
    "Small business": 0.60,
}


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
