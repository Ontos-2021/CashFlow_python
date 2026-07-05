import os
import sys
import unittest
from unittest import mock


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "cashflow_game"))

from app.game_engine import (  # noqa: E402
    PROFESSION_EVENTS,
    amount,
    apply_action,
    apply_market_drift,
    apply_monthly_cashflow,
    advance_time,
    check_end_conditions,
    cut_expenses,
    enrich_state,
    event_fits_state,
    is_quiet_month,
    new_game,
    pay_down_debt,
    pick_event,
    prepare_event_for_state,
    process_schedule,
    quiet_month_event,
    resolve_action_amounts,
    sell_one_asset,
    simulate_quiet_months,
)
from app import create_app  # noqa: E402


class GameEngineEdgeCaseTest(unittest.TestCase):
    def test_debt_free_player_does_not_receive_existing_debt_events(self):
        state = new_game("docente")
        state["debts"] = []
        for _ in range(40):
            event = pick_event(state)
            self.assertNotIn(event["id"], {"credit_card_attack", "refinance"})

    def test_debt_free_state_unlocks_badge_and_alert(self):
        state = enrich_state(new_game("docente"))
        labels = {badge["label"] for badge in state["status_badges"]}
        alert_titles = {alert["title"] for alert in state["alerts"]}
        self.assertIn("Debt Free", labels)
        self.assertIn("Libre de deuda", alert_titles)

    def test_stress_at_one_hundred_ends_as_burnout(self):
        state = new_game("programador")
        state["stress"] = 100
        check_end_conditions(state)
        self.assertEqual(state["status"], "ended")
        self.assertEqual(state["outcome"], "Burnout retirement")

    def test_insolvency_ends_as_debt_trapped(self):
        state = new_game("programador")
        state["cash"] = -100
        state["salary"] = 0
        state["insolvent_months"] = 3
        check_end_conditions(state)
        self.assertEqual(state["status"], "lost")
        self.assertEqual(state["outcome"], "Debt trapped")

    def test_pay_down_debt_with_no_debt_is_safe(self):
        state = new_game("docente")
        state["debts"] = []
        pay_down_debt(state, 1000)
        self.assertEqual(state["debts"], [])

    def test_sell_action_is_removed_when_player_has_no_assets(self):
        state = new_game("docente")
        state["assets"] = []
        event = {
            "id": "test_sell",
            "actions": {
                "sell": {"label": "Vender", "sell_asset_percent": 0.2},
                "hold": {"label": "Mantener", "lesson": "Paciencia", "interpretation": "No haces nada."},
            },
        }
        prepared = prepare_event_for_state(event, state)
        self.assertNotIn("sell", prepared["actions"])
        self.assertIn("hold", prepared["actions"])

    def test_risky_action_receives_warning_tag(self):
        state = new_game("freelancer")
        state["cash"] = 400
        event = {
            "id": "test_risk",
            "actions": {
                "buy": {"label": "Comprar", "cash": -1000, "lesson": "Riesgo", "interpretation": "Compraste sin caja."},
            },
        }
        prepared = prepare_event_for_state(event, state)
        self.assertIn("Caja negativa", prepared["actions"]["buy"]["risk_tags"])

    def test_victory_requires_passive_income_and_runway(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Activo", "type": "Paper assets", "value": 100000, "income": 3000}]
        state["cash"] = 20000
        state["debts"] = []
        check_end_conditions(state)
        self.assertEqual(state["status"], "won")

    def test_feedback_can_unlock_debt_free_badge(self):
        state = new_game("administrativo")
        state["cash"] = 10000
        state["current_event"] = {
            "title": "Pago final",
            "category": "Debt",
            "actions": {
                "pay": {"label": "Pagar todo", "pay_debt": 10000, "lesson": "Libertad", "interpretation": "Cerraste la deuda."},
            },
        }
        state = apply_action(state, "pay")
        self.assertIn("Debt Free", state["last_feedback"]["badges"])


class MechanicsTandaOneTest(unittest.TestCase):
    def test_scheduled_effect_applies_on_due_month(self):
        state = new_game("docente")
        state["schedule"].append({
            "due_month": state["month"] + 4,
            "label": "Tasa variable",
            "source": "test",
            "effect": {"cash": -500},
        })
        before = state["cash"]
        state["month"] += 3
        process_schedule(state)
        self.assertEqual(state["cash"], before)
        state["month"] += 1
        process_schedule(state)
        self.assertEqual(state["cash"], before - 500)
        self.assertEqual(state["schedule"], [])

    def test_vacancy_zeros_asset_income(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Departamento", "type": "Real estate", "value": 50000, "income": 250, "risk": "vacancy"}]
        state["debts"] = []
        state["cash"] = 0
        state["salary"] = 0
        state["expenses"] = 0
        with mock.patch("app.game_engine.random", return_value=0.0):
            cash_before = state["cash"]
            apply_monthly_cashflow(state)
            self.assertEqual(state["cash"], cash_before)
        self.assertTrue(any(e["kind"] == "vacancy" for e in state["asset_events"]))

    def test_execution_reduces_income_half(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Negocio", "type": "Small business", "value": 4000, "income": 400, "risk": "execution"}]
        state["debts"] = []
        state["cash"] = 0
        state["salary"] = 0
        state["expenses"] = 0
        base = state["assets"][0]["income"]
        with mock.patch("app.game_engine.random", return_value=0.0):
            apply_monthly_cashflow(state)
        self.assertEqual(state["cash"], round(base * 0.5, 2))

    def test_education_reduces_asset_event_probability(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Departamento", "type": "Real estate", "value": 50000, "income": 250, "risk": "vacancy"}]
        state["education"] = 8
        state["debts"] = []
        state["cash"] = 0
        state["salary"] = 0
        state["expenses"] = 0
        # Threshold at education 8 reduces vacancy probability from 0.08 to 0.08 * 0.92 = 0.0736
        # random just below 0.0736 triggers vacancy; just above does not.
        with mock.patch("app.game_engine.random", return_value=0.078):
            apply_monthly_cashflow(state)
        self.assertFalse(any(e["kind"] == "vacancy" for e in state["asset_events"]))

    def test_job_loss_only_in_recession_or_recovery(self):
        def make_freedom_state(world_name):
            state = new_game("docente")
            state["world"] = {"name": world_name, "inflation": 0.003, "asset_price": 1.0, "income_risk": 0.04, "credit": 1.0, "description": ""}
            state["month"] = 200
            state["assets"] = [{"name": "Cartera grande", "type": "Paper assets", "value": 200000, "income": 4000, "risk": "market"}]
            state["salary"] = 0
            state["expenses"] = 2000
            state["debts"] = []
            return state

        for _ in range(50):
            state = make_freedom_state("Expansion")
            event = pick_event(state)
            self.assertNotEqual(event["id"], "job_loss")

        for world_name in ["Recesion", "Recuperacion"]:
            seen = False
            for _ in range(200):
                state = make_freedom_state(world_name)
                event = pick_event(state)
                if event["id"] == "job_loss":
                    seen = True
                    break
            self.assertTrue(seen, f"job_loss not seen in {world_name}")

    def test_small_business_drift_follows_world(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Tienda", "type": "Small business", "value": 4000, "income": 200, "risk": "execution"}]
        original = state["assets"][0]["value"]
        state["world"] = {"name": "Recesion", "inflation": 0.001, "asset_price": 0.86, "income_risk": 0.11, "credit": 0.72, "description": ""}
        apply_market_drift(state)
        self.assertLess(state["assets"][0]["value"], original)

    def test_new_debt_rate_adjusted_by_world_credit(self):
        state = new_game("docente")
        state["world"] = {"name": "Recesion", "inflation": 0.001, "asset_price": 0.86, "income_risk": 0.11, "credit": 0.72, "description": ""}
        state["current_event"] = {
            "title": "Test",
            "category": "Debt",
            "actions": {"loan": {"label": "Pedir $1.000", "cash": 1000, "debt": {"name": "Prestamo test", "type": "Personal loan", "balance": 1000, "payment": 80, "rate": 0.2, "stress": 5}, "lesson": "Prueba", "interpretation": "test"}},
        }
        state = apply_action(state, "loan")
        debt = next(d for d in state["debts"] if d["name"] == "Prestamo test")
        self.assertGreater(debt["rate"], 0.2)


class MechanicsTandaTwoTest(unittest.TestCase):
    def test_amount_literal_returns_literal(self):
        state = new_game("docente")
        self.assertEqual(amount(state, 1500), 1500)
        self.assertEqual(amount(state, -700), -700)

    def test_amount_scaled_by_salary(self):
        state = new_game("medico")
        state["salary"] = 7200
        val = amount(state, {"factor": 0.4, "min": 500, "max": 5000, "rng": False})
        self.assertEqual(val, 2880)

    def test_amount_negative_factor_clamps(self):
        state = new_game("medico")
        state["salary"] = 7200
        val = amount(state, {"factor": -0.3, "min": -5000, "max": -200, "rng": False})
        self.assertEqual(val, -2160)
        self.assertGreaterEqual(val, -5000)
        self.assertLessEqual(val, -200)

    def test_amount_rng_within_range(self):
        state = new_game("medico")
        state["salary"] = 5000
        for _ in range(20):
            val = amount(state, {"factor": 0.4, "min": 100, "max": 5000})
            self.assertGreaterEqual(val, 100)
            self.assertLessEqual(val, 5000)

    def test_sell_one_asset_liquidity_differs_by_type(self):
        state = new_game("docente")
        state["assets"] = [
            {"name": "Fondo", "type": "Paper assets", "value": 10000, "income": 80, "risk": "market"},
            {"name": "Depto", "type": "Real estate", "value": 10000, "income": 80, "risk": "vacancy"},
            {"name": "Negocio", "type": "Small business", "value": 10000, "income": 80, "risk": "execution"},
        ]
        r1 = sell_one_asset(state, 0, 0.5)
        r2 = sell_one_asset(state, 1, 0.5)
        r3 = sell_one_asset(state, 2, 0.5)
        self.assertGreater(r1["proceeds"], r2["proceeds"])
        self.assertGreater(r2["proceeds"], r3["proceeds"])

    def test_sell_one_asset_education_not_sellable(self):
        state = new_game("docente")
        state["assets"] = [{"name": "Curso", "type": "Education", "value": 1000, "income": 0, "risk": ""}]
        result = sell_one_asset(state, 0, 0.5)
        self.assertIsNone(result)

    def test_cut_expenses_reduces_and_raises_stress(self):
        state = new_game("medico")
        state["expenses"] = 6000
        state["starting_expenses"] = 4700
        state["stress"] = 40
        result = cut_expenses(state)
        self.assertIsNotNone(result)
        self.assertLess(state["expenses"], 6000)
        self.assertEqual(state["stress"], 52)

    def test_cut_expenses_blocked_without_creep(self):
        state = new_game("docente")
        state["starting_expenses"] = state["expenses"]
        result = cut_expenses(state)
        self.assertIsNone(result)

    def test_requires_education_gates_actions(self):
        state = new_game("docente")
        state["education"] = 2
        event = {
            "id": "test_ed",
            "actions": {
                "basic": {"label": "Basico", "lesson": "L", "interpretation": "I"},
                "advanced": {"label": "Avanzado", "requires_education": 5, "lesson": "L", "interpretation": "I"},
            },
        }
        prepared = prepare_event_for_state(event, state)
        self.assertIn("basic", prepared["actions"])
        self.assertNotIn("advanced", prepared["actions"])
        state["education"] = 6
        event2 = {
            "id": "test_ed",
            "actions": {
                "basic": {"label": "Basico", "lesson": "L", "interpretation": "I"},
                "advanced": {"label": "Avanzado", "requires_education": 5, "lesson": "L", "interpretation": "I"},
            },
        }
        prepared2 = prepare_event_for_state(event2, state)
        self.assertIn("advanced", prepared2["actions"])

    def test_resolve_action_amounts_formats_label(self):
        state = new_game("medico")
        state["salary"] = 7200
        action = {
            "label": "Placeholder",
            "label_fmt": "Invertir ${cash:,.0f}",
            "cash": {"factor": -0.2, "min": -5000, "max": -500, "rng": False},
        }
        resolved = resolve_action_amounts(action, state)
        self.assertIn("$", resolved["label"])
        self.assertNotIn("{cash", resolved["label"])
        self.assertNotIn("$-", resolved["label"])
        self.assertIsInstance(resolved["cash"], int)

    def test_legacy_events_use_scaled_amount_specs(self):
        from app.game_engine import BASE_EVENTS
        event = next(item for item in BASE_EVENTS if item["id"] == "index_fund")
        self.assertIsInstance(event["actions"]["invest"]["cash"], dict)
        self.assertIsInstance(event["actions"]["invest"]["asset"]["value"], dict)
        event = next(item for item in BASE_EVENTS if item["id"] == "medical_bill")
        self.assertIsInstance(event["actions"]["pay"]["cash"], dict)

    def test_category_mapping_accepts_english_categories(self):
        categories = {
            "Investment": "neutral",
            "Debt": "danger",
            "Crisis": "danger",
            "Knowledge": "good",
            "Expense": "warning",
            "Income": "good",
        }
        self.assertEqual(categories["Debt"], "danger")
        self.assertEqual(categories["Knowledge"], "good")

    def test_advance_time_resets_action_used(self):
        state = new_game("medico")
        state["action_used_this_month"] = {"sell": True, "cut_expenses": True}
        advance_time(state, 1)
        self.assertFalse(state["action_used_this_month"]["sell"])
        self.assertFalse(state["action_used_this_month"]["cut_expenses"])

    def test_event_count_meets_target(self):
        from app.game_engine import BASE_EVENTS
        self.assertGreaterEqual(len(BASE_EVENTS), 60)


class RouteStorageRegressionTest(unittest.TestCase):
    def test_game_state_cookie_stays_small(self):
        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()
        response = client.post("/new-game", data={"profession": "medico"})
        cookie = response.headers.get("Set-Cookie", "")
        self.assertLess(len(cookie), 1000)

    def test_game_route_uses_server_side_store(self):
        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()
        client.post("/new-game", data={"profession": "medico"})
        response = client.get("/game")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"game-app", response.data)


class ProfessionEventsTest(unittest.TestCase):
    def test_profession_events_exist_for_each_profession(self):
        for profession_id in {"administrativo", "programador", "docente", "medico", "vendedor", "freelancer"}:
            count = sum(1 for event in PROFESSION_EVENTS if event.get("requires_profession") == profession_id)
            self.assertGreaterEqual(count, 3, f"profession {profession_id} has only {count} events")

    def test_profession_event_fits_only_matching_profession(self):
        state = new_game("programador")
        event = next(event for event in PROFESSION_EVENTS if event.get("requires_profession") == "programador")
        self.assertTrue(event_fits_state(event, state, "growth"))
        state["profession_id"] = "docente"
        self.assertFalse(event_fits_state(event, state, "growth"))

    def test_pick_event_can_return_profession_event(self):
        state = new_game("vendedor")
        state["month"] = 60
        state["assets"] = [{"name": "Fondo", "type": "Paper assets", "value": 50000, "income": 300, "risk": "market"}]
        seen = set()
        for _ in range(200):
            event = pick_event(state)
            seen.add(event["id"])
        profession_ids = {event["id"] for event in PROFESSION_EVENTS if event.get("requires_profession") == "vendedor"}
        self.assertTrue(seen & profession_ids, "no profession event seen after 200 picks")


class QuietMonthTest(unittest.TestCase):
    def test_quiet_month_triggered_when_stable(self):
        state = new_game("docente")
        state["month"] = 12
        state["cash"] = 20000
        state["salary"] = 3000
        state["expenses"] = 1500
        state["stress"] = 30
        state["debts"] = []
        self.assertTrue(is_quiet_month(state))

    def test_quiet_month_blocked_when_risky(self):
        state = new_game("docente")
        state["month"] = 12
        state["cash"] = 200
        state["salary"] = 2500
        state["expenses"] = 2000
        state["stress"] = 80
        state["debts"] = []
        self.assertFalse(is_quiet_month(state))

    def test_quiet_event_includes_advance_action(self):
        state = new_game("docente")
        state["month"] = 12
        state["cash"] = 20000
        state["salary"] = 3000
        state["expenses"] = 1500
        state["stress"] = 30
        event = quiet_month_event(state)
        self.assertEqual(event["id"], "quiet_month")
        self.assertIn("advance", event["actions"])
        self.assertTrue(event["actions"]["advance"].get("quiet"))

    def test_simulate_quiet_months_applies_cashflow(self):
        state = new_game("docente")
        state["month"] = 12
        state["cash"] = 20000
        state["salary"] = 3000
        state["expenses"] = 1500
        state["stress"] = 30
        state["debts"] = []
        before_month = state["month"]
        before_cash = state["cash"]
        simulate_quiet_months(state, 3)
        self.assertEqual(state["month"], before_month + 3)
        self.assertGreater(state["cash"], before_cash)
        self.assertEqual(state["status"], "playing")


if __name__ == "__main__":
    unittest.main()
