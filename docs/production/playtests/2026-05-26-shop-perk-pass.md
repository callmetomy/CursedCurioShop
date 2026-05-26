# 第二店鋪升級切片

日期：2026-05-26
範圍：十日 demo 完成後的第二個店鋪 perk

## 決策

新增 `Containment Cabinet` / `封存櫃` 作為第二個店鋪升級。

- 成本：60 cash。
- 效果：下一輪開始，所有 Seal 成本降低 5。
- 下限：Seal 成本最低不低於 5。
- 購買位置：十日最終結果的 progression panel，與 Ledger Desk 並列。

## 理由

- 這個 perk 直接回應核心玩法：玩家已經學會 Sell / Seal / Discard 後，下一輪會因 Seal 折扣改變經濟壓力。
- 它不新增奇物、不改主流程，風險小。
- 正確路徑 Final Cash 是 180，剛好能同時買 Ledger Desk 120 和 Containment Cabinet 60。

## 驗證

```powershell
python -m unittest tests.test_godot_shop_progression tests.test_godot_inspection_table tests.test_godot_game_state
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
```

結果：

- Targeted Python tests：43 passed。
- Full project tests：106 passed。
- Godot ten-day smoke：passed。
- Smoke flow 已實際購買兩個升級，並確認下一輪 Day 1 Seal cost 從 25 降到 20。
- 升級後第二輪已跑完整十日正確路徑：Final Cash 210、Final Reputation 100、最低現金緩衝 35。
- 繁中截圖已刷新；`1152x648` 與 `1280x720` 的 final summary 皆可完整顯示兩個升級按鈕與返回選單按鈕。

## Agent 盲測

因無法招募 3 位真實玩家，本輪改用 3 位 agent 玩家檢查最終結果面板的升級理解。

- 保守玩家：封存櫃清楚度 4/5；理解 Seal 折扣價值，但希望明確寫「每次 Seal」與是否永久。
- 收益玩家：封存櫃清楚度 2/5；知道 Seal 會變便宜，但缺少「省 5 的經濟參照」與生效範圍。
- 新手玩家：封存櫃清楚度 4/5；理解封存櫃比帳冊桌直覺，但仍不確定是每次封存或整輪總成本。

採取修正：

- 封存櫃文案改為「每次封存成本降低 5，會保留到後續輪次」。
- 帳冊桌文案改為「未來顧客備註會加入來源線索」，降低「來源紀錄」的抽象感。
- 文字變長後重新調整 final summary panel，在 `1152x648` 仍完整顯示兩個升級按鈕與返回選單。

## 下一步

升級後二周目 smoke、3 位 agent 玩家盲測與 demo release audit 已完成。下一個切片建議進入 owner review 或真人 playtest，不要新增第三個 perk 或新奇物批次。
