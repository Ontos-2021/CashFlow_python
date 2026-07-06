import json
import os

from .metrics import display_age, metrics
from .ui import investor_profile


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


def diagnose_patterns(state):
    patterns = []
    data = metrics(state)
    assets = state.get("assets", [])
    asset_types = set(a.get("type") for a in assets)
    cash = state.get("cash", 0)
    obligations = data["monthly_obligations"]
    fr = data["freedom_ratio"]
    education = state.get("education", 0)
    stress = state.get("stress", 0)
    max_stress = state.get("max_stress", stress)
    dti = data["debt_to_income"]
    debts = state.get("debts", [])

    if cash > obligations * 12 and len(assets) <= 2 and not debts:
        patterns.append({
            "id": "cash_hoarder",
            "icon": "💰",
            "title": "Acumulador de caja",
            "message": f"Tenes ${cash:,.0f} en caja pero solo {len(assets)} activos. La caja parada pierde contra la inflacion.",
        })

    if len(assets) >= 5 and dti > 0.3:
        patterns.append({
            "id": "compulsive_investor",
            "icon": "📈",
            "title": "Inversor apalancado",
            "message": f"Compraste {len(assets)} activos con deuda al {dti*100:.0f}%. El apalancamiento amplifica tanto las ganancias como el riesgo.",
        })

    if education >= 5:
        patterns.append({
            "id": "educator",
            "icon": "🎓",
            "title": "Estudiante permanente",
            "message": f"Tu nivel educativo ({education}/10) desbloqueo oportunidades premium. El conocimiento fue tu mejor inversion.",
        })

    if max_stress >= 85:
        patterns.append({
            "id": "burnout_chaser",
            "icon": "🔥",
            "title": "Cazador de burnout",
            "message": f"Llegaste a {max_stress}/100 de estres. La energia tambien es capital; un cuerpo agotado no sostiene un plan.",
        })

    if dti > 0.42:
        patterns.append({
            "id": "overleveraged",
            "icon": "⛓️",
            "title": "Sobreapalancado",
            "message": f"Tus pagos de deuda consumen {dti*100:.0f}% del ingreso. La flexibilidad murio antes que la oportunidad.",
        })

    if len(asset_types) >= 3:
        types_str = ", ".join(t for t in asset_types if t)
        patterns.append({
            "id": "diversifier",
            "icon": "🎨",
            "title": "Diversificador",
            "message": f"Mezclaste {len(asset_types)} tipos de activos ({types_str}). La diversificacion te protegio de la volatilidad.",
        })

    if len(assets) == 1 and fr > 0.5:
        patterns.append({
            "id": "concentrator",
            "icon": "🎯",
            "title": "Concentrador",
            "message": f"Todo tu ingreso pasivo viene de un solo activo. Concentracion extrema = un solo punto de falla.",
        })

    won = state.get("status") == "won"
    if won and state.get("month", 0) < 60:
        patterns.append({
            "id": "quick_win",
            "icon": "⚡",
            "title": "Victoria rapida",
            "message": f"Liberte en menos de {state['month']} meses. Disciplina temprana compuesta rapido.",
        })

    if won and state.get("month", 0) >= 120:
        patterns.append({
            "id": "late_bloomer",
            "icon": "🌱",
            "title": "Tardio pero constante",
            "message": f"Liberte en {state['month']} meses. La paciencia tambien es estrategia.",
        })

    if state.get("status") != "won" and fr >= 0.85:
        patterns.append({
            "id": "near_miss",
            "icon": "🎯",
            "title": "Casi llegas",
            "message": f"Llegaste a {fr*100:.0f}% de libertad. Estuviste a un activo de la victoria.",
        })

    return patterns


def actionable_advice(state, patterns):
    outcome = state.get("outcome", "")
    pattern_ids = {p["id"] for p in patterns}
    advice_pool = {
        "Burnout retirement": [
            "Proba reducir eventos de Income en tu proxima run. El segundo trabajo no vale el costo humano.",
            "Prioriza la accion 'Pagar deuda' antes de tomar nuevos riesgos. La deuda ancla el estres.",
        ],
        "Debt trapped": [
            "Ataca primero la deuda de mayor tasa. La tarjeta al 34% destruye flujo silenciosamente.",
            "En tu proxima run, usa la accion 'Pagar deuda' apenas tengas cash > 2x obligaciones.",
        ],
        "Financially free": [
            "Experimenta con mayor riesgo la proxima vez. Podrias haber llegado 2 anos antes con leverage.",
            "Proba una profesion mas dificil como Medico. Ya dominaste el flujo y la reserva.",
            "Tu siguiente meta podria ser: escalar a 1.5x de libertad. La holgura financia proyectos grandes.",
        ],
        "Slow conservative success": [
            "Tu paciencia fue tu fortaleza. Proba agregar un activo de mayor yield (Small business) para acelerar.",
        ],
        "Business success": [
            "Excelente uso de small business. La proxima: protege esos activos con diversificacion en paper assets.",
        ],
        "High net worth, low liquidity": [
            "Tenes activos pero poca caja. La proxima: vende 20% de un activo y guarda 6 meses de reserva.",
        ],
    }
    pool = advice_pool.get(outcome, [
        "Tu proximo paso: prioriza activos con income > 20/mes sobre ahorro en caja.",
        "Sube educacion a 5 antes de buscar oportunidades premium. El conocimiento paga sola.",
    ])
    if "near_miss" in pattern_ids:
        return "Estabas a un activo de ganar. La proxima run: invierte mas temprano, no mas grande."
    return pool[hash(state.get("profession", "")) % len(pool)]


def key_moments(state, n=5):
    history = state.get("history", [])
    if len(history) < 2:
        return history
    moments = []
    for i, entry in enumerate(history):
        next_entry = history[i - 1] if i > 0 else None
        if next_entry and "cash_after" in entry and "cash_after" in next_entry:
            cash_delta = next_entry.get("cash_after", 0) - entry.get("cash_after", 0)
        else:
            cash_delta = 0
        impact = abs(cash_delta)
        moments.append((impact, cash_delta, entry))
    moments.sort(key=lambda x: x[0], reverse=True)
    result = []
    for impact, delta, entry in moments[:n]:
        e = dict(entry)
        e["impact"] = delta
        result.append(e)
    return result


def get_benchmarks(profession_id):
    benchmarks_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts", "benchmarks.json")
    benchmarks_path = os.path.abspath(benchmarks_path)
    if not os.path.exists(benchmarks_path):
        return None
    try:
        with open(benchmarks_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(profession_id)
    except (json.JSONDecodeError, IOError):
        return None


def final_report(state):
    from .simulation import partial_outcome
    data = metrics(state)
    outcome = state.get("outcome") or partial_outcome(state)
    patterns = diagnose_patterns(state)
    advice = actionable_advice(state, patterns)
    moments = key_moments(state, n=5)
    benchmarks = get_benchmarks(state.get("profession_id", ""))
    assets = state.get("assets", [])
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
        "patterns": patterns,
        "advice": advice,
        "key_moments": moments,
        "benchmarks": benchmarks,
        "max_stress": state.get("max_stress", state.get("stress", 0)),
        "asset_allocation": {
            "Paper assets": sum(a.get("value", 0) for a in assets if a.get("type") == "Paper assets"),
            "Real estate": sum(a.get("value", 0) for a in assets if a.get("type") == "Real estate"),
            "Small business": sum(a.get("value", 0) for a in assets if a.get("type") == "Small business"),
            "Education": sum(a.get("value", 0) for a in assets if a.get("type") == "Education"),
        },
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
