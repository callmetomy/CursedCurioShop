# 十日平衡與可讀性 Playtest Pass

日期：2026-05-25
測試者：Codex 內部平衡檢查
版本：本機 `main`，含第一輪 commercial-demo readability tuning

## 範圍

- 十日正確處置路徑的現金與聲望節奏。
- 十個奇物是否仍有模板化線索或直接給答案的風險提示。
- Sell / Seal / Discard 是否形成實際取捨。
- 本次不是外部盲測；未知玩家是否真的理解線索仍需人工驗證。

## 驗證指令

```powershell
python -m unittest tests.test_commercial_demo_design
python -m unittest discover -s tests
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
python -m tools.project_status --root . --run-tests
```

## 正確路徑節奏

起始狀態：Cash 100 / Reputation 50。

| Day | Oddity | Correct | Cash Delta | Cash After | Reputation After | Sell Value | Seal Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Whispering Teacup | Seal | -25 | 75 | 55 | 85 | 25 |
| 2 | Mirror Coin | Seal | -30 | 45 | 60 | 110 | 30 |
| 3 | Ashen Music Box | Discard | 0 | 45 | 65 | 55 | 25 |
| 4 | Cold Brass Key | Seal | -25 | 20 | 70 | 80 | 25 |
| 5 | Glass Eye | Sell | +140 | 160 | 75 | 140 | 50 |
| 6 | Black Wax Candle | Discard | 0 | 160 | 80 | 45 | 15 |
| 7 | Moth-Eaten Doll | Seal | -35 | 125 | 85 | 65 | 35 |
| 8 | Silver Funeral Bell | Seal | -55 | 70 | 90 | 100 | 55 |
| 9 | Cracked Hand Mirror | Discard | 0 | 70 | 95 | 60 | 20 |
| 10 | Red Thread Spool | Sell | +125 | 195 | 100 | 125 | 45 |

## 判斷

- Cash 最低點是 Day 4 的 20，能形成前半段壓力，但正確玩家不會掉入負現金。
- Final Cash 195，代表正確路徑有明確回報，但不會富到讓 Seal 成本失去意義。
- Reputation 正確路徑從 50 到 100，節奏清楚；下一輪需要測錯誤路徑是否太快進入壞結局。
- Sell 正解集中在 Day 5 和 Day 10，能形成「不是所有奇物都該封存」的教學，但外部盲測需確認玩家是否看得懂 Glass Eye 與 Red Thread Spool 的安全訊號。

## 已修正問題

- 原先第一輪數值會讓正確路徑在 Day 4 掉到 Cash -15，這對玩家是不公平壓力。
- 本輪將 Day 1 / Day 2 / Day 4 的 Seal 成本降到 25 / 30 / 25，讓最低現金停在 20。
- 新增 `tests/test_commercial_demo_design.py` 的十日正解現金門檻，避免後續調數值時再次破壞正確路徑。

## 可讀性風險

- 風險提示已不直接寫出處置答案，但仍有可能太明顯，例如「醫療來源清楚」可能暗示 Glass Eye 應該出售。
- Discard 類奇物目前沒有金錢收益，玩家可能把它理解為「沒懲罰的安全選項」；需要盲測確認。
- 後段線索文字比上一版長；本輪已重新擷取繁中 `1152x648` / `1280x720` 截圖，抽查顧客提示、結果面板、最終總結與結果詳情後未見主要文字重疊。

## 下一步

- 找 3 位不知道答案的玩家做完整十日盲測。
- 盲測記錄每一天三個問題：
  - 玩家是否知道該用哪些工具查證？
  - 玩家是否能說出選擇 Sell / Seal / Discard 的理由？
  - 玩家看完結果後是否覺得答案公平？

## 驗收標準

- 至少 7/10 天，玩家在看結果後能說出正確答案合理的原因。
- 正確路徑最低 Cash 不低於 20。
- 正確路徑 Final Cash 落在 180 到 260 之間。
- 繁中畫面無主要文字重疊或遮擋。
