import os
import sys
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "cashflow_game"))

from app.game_engine import (  # noqa: E402
    apply_action,
    check_end_conditions,
    enrich_state,
    new_game,
    pay_down_debt,
    pick_event,
    prepare_event_for_state,
)


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


if __name__ == "__main__":
    unittest.main()
