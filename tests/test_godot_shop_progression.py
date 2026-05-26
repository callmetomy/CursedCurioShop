from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GodotShopProgressionTests(unittest.TestCase):
    def test_game_state_tracks_ledger_desk_upgrade_across_new_runs(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("const LEDGER_DESK_UPGRADE_COST := 120", game_state)
        self.assertIn("var ledger_desk_upgraded := false", game_state)
        self.assertIn("func can_purchase_ledger_desk_upgrade() -> bool:", game_state)
        self.assertIn("func purchase_ledger_desk_upgrade() -> bool:", game_state)
        self.assertIn("cash -= LEDGER_DESK_UPGRADE_COST", game_state)
        self.assertIn("ledger_desk_upgraded = true", game_state)
        self.assertNotIn("ledger_desk_upgraded = false", game_state)

    def test_game_state_tracks_containment_cabinet_upgrade_across_new_runs(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("const CONTAINMENT_CABINET_UPGRADE_COST := 60", game_state)
        self.assertIn("const CONTAINMENT_CABINET_SEAL_DISCOUNT := 5", game_state)
        self.assertIn("var containment_cabinet_upgraded := false", game_state)
        self.assertIn("func can_purchase_containment_cabinet_upgrade() -> bool:", game_state)
        self.assertIn("func purchase_containment_cabinet_upgrade() -> bool:", game_state)
        self.assertIn("cash -= CONTAINMENT_CABINET_UPGRADE_COST", game_state)
        self.assertIn("containment_cabinet_upgraded = true", game_state)
        self.assertIn("func get_effective_seal_cost(base_cost: int) -> int:", game_state)
        self.assertIn("max(5, base_cost - CONTAINMENT_CABINET_SEAL_DISCOUNT)", game_state)
        self.assertNotIn("containment_cabinet_upgraded = false", game_state)

    def test_upgraded_ledger_adds_provenance_to_customer_briefs(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('Localization.text("upgrade.ledger_desk.provenance")', game_state)
        self.assertIn('"upgrade.ledger_desk.provenance"', localization)
        self.assertIn('"upgrade.ledger_desk.status_locked"', localization)
        self.assertIn('"upgrade.ledger_desk.status_unlocked"', localization)

    def test_containment_cabinet_localization_describes_discount(self):
        game_state = (ROOT / "godot" / "scripts" / "game_state.gd").read_text(
            encoding="utf-8"
        )
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('"upgrade.containment_cabinet.buy"', localization)
        self.assertIn('"upgrade.containment_cabinet.status_locked"', localization)
        self.assertIn('"upgrade.containment_cabinet.status_unlocked"', localization)
        self.assertIn('Localization.text("upgrade.containment_cabinet.status_unlocked")', game_state)
        self.assertIn('Localization.format_text("upgrade.containment_cabinet.status_locked"', game_state)
        self.assertIn("each future Seal", localization)
        self.assertIn("persists into future runs", localization)
        self.assertIn("每次封存成本降低", localization)
        self.assertIn("會保留到後續輪次", localization)

    def test_ledger_desk_localization_describes_customer_brief_value(self):
        localization = (ROOT / "godot" / "scripts" / "localization.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("adds source clues to future customer briefs", localization)
        self.assertIn("future runs", localization)
        self.assertIn("未來顧客備註會加入來源線索", localization)

    def test_final_day_result_panel_exposes_ledger_upgrade_purchase(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="ProgressionPanel" type="PanelContainer" parent="HUD/DayResultPanel"]', scene)
        self.assertIn('[node name="ProgressionStatusLabel" type="Label" parent="HUD/DayResultPanel/ProgressionPanel/ProgressionContent"]', scene)
        self.assertIn('[node name="BuyLedgerDeskButton" type="Button" parent="HUD/DayResultPanel/ProgressionPanel/ProgressionContent"]', scene)
        self.assertIn("progression_panel", script)
        self.assertIn("buy_ledger_desk_button", script)
        self.assertIn("GameState.purchase_ledger_desk_upgrade()", script)
        self.assertIn('Localization.text("upgrade.ledger_desk.buy")', script)

    def test_final_day_result_panel_exposes_containment_cabinet_purchase(self):
        scene = (ROOT / "godot" / "scenes" / "inspection_table.tscn").read_text(
            encoding="utf-8"
        )
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="BuyContainmentCabinetButton" type="Button" parent="HUD/DayResultPanel/ProgressionPanel/ProgressionContent"]', scene)
        self.assertIn("buy_containment_cabinet_button", script)
        self.assertIn("GameState.purchase_containment_cabinet_upgrade()", script)
        self.assertIn('Localization.text("upgrade.containment_cabinet.buy")', script)
        self.assertIn("GameState.can_purchase_containment_cabinet_upgrade()", script)

    def test_inspection_table_uses_discounted_seal_cost_after_containment_upgrade(self):
        script = (ROOT / "godot" / "scripts" / "inspection_table.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn("GameState.get_effective_seal_cost(_get_current_base_seal_cost())", script)
        self.assertIn("func _get_current_base_seal_cost() -> int:", script)

    def test_shop_hud_shows_progression_status(self):
        scene = (ROOT / "godot" / "scenes" / "shop_prototype.tscn").read_text(
            encoding="utf-8"
        )
        controller = (ROOT / "godot" / "scripts" / "first_person_controller.gd").read_text(
            encoding="utf-8"
        )

        self.assertIn('[node name="ProgressionStatus" type="Label" parent="HUD/ShopLedgerPanel/ShopLedgerContent"]', scene)
        self.assertIn("progression_status", controller)
        self.assertIn("GameState.get_progression_status_text()", controller)


if __name__ == "__main__":
    unittest.main()
