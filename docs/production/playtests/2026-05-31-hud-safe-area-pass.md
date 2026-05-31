# 2026-05-31 HUD Safe-Area Visual Pass

Scope: Traditional Chinese HUD review at `1152x648` and `1280x720`, covering shop customer brief, shop result detail, day result, and final summary.

## Commands

```powershell
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
python -m unittest tests.test_godot_inspection_table
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
python -m tools.project_status --root . --run-tests
```

## Result

- Fixed: `final_summary-1152x648` previously clipped the bottom of the return-to-menu button.
- Change: final result panels now use a more compact vertical layout, and redundant top item/back UI is hidden once the day result panel is shown.
- Checked: `shop_customer_brief`, `shop_result_detail`, `day_result`, and `final_summary` at both target resolutions.
- Remaining note: continue Phase C in small wrong-outcome or ending branches before adding a new oddity batch.

## Evidence

![shop_customer_brief-1152x648](screenshots/shop_customer_brief-1152x648.png)
![shop_result_detail-1152x648](screenshots/shop_result_detail-1152x648.png)
![day_result-1152x648](screenshots/day_result-1152x648.png)
![final_summary-1152x648](screenshots/final_summary-1152x648.png)
![shop_customer_brief-1280x720](screenshots/shop_customer_brief-1280x720.png)
![shop_result_detail-1280x720](screenshots/shop_result_detail-1280x720.png)
![day_result-1280x720](screenshots/day_result-1280x720.png)
![final_summary-1280x720](screenshots/final_summary-1280x720.png)
