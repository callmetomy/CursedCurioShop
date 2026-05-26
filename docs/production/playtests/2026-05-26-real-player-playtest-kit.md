# 真人盲測測試包

日期：2026-05-26
目的：準備 1-3 位真實玩家的十日 demo 盲測，驗證 owner review build 在真人操作、理解、節奏與情緒反應上的可用性。

## Build

- Build zip: `exports/releases/CursedCurioShop-owner-review-2026-05-26-1051.zip`
- Executable: `CursedCurioShop.exe`
- SHA256: `A8EAF24C901E3B18CE518E745C67E8C2348444DF832A9C6B05BD38A0A42820B7`
- Owner playtest: OK, reported on 2026-05-26.
- Current automated baseline: 106 tests passing, 40/40 asset outputs ready, Godot ten-day smoke exit 0.

## 測試目標

這輪不追求新增內容，只驗證目前 demo 是否能被真人理解並完成。

必須回答：

1. 玩家是否能在沒有主持人提示的情況下完成十日流程？
2. 玩家是否理解 Sell / Seal / Discard 的差異？
3. 玩家是否能從顧客備註與三個工具線索推理正確處置？
4. 玩家是否理解 final summary 的兩個升級與 future-run persistence？
5. 哪些日數、文字、UI 或節奏造成誤解、猶豫或中止？

## 測試人選

建議 1-3 位。

- 玩家 A：常玩敘事 / 解謎 / 模擬遊戲。
- 玩家 B：較少玩 PC indie game 的普通玩家。
- 玩家 C：偏商業或效率導向，會快速略讀文字。

至少保留一位非專案熟人，避免只得到禮貌性回饋。

## 主持流程

1. 給玩家 build zip 或已解壓資料夾。
2. 告知玩家：「請像第一次買到這個 demo 一樣玩，不懂可以說出來，但我不會解釋正解。」
3. 請玩家邊玩邊說出推理，但不要要求他一定要表演。
4. 主持人用 `docs/production/demo_playtest_checklist.md` 記錄。
5. 若玩家卡住超過 2 分鐘，先記錄卡住點，再給最小提示。
6. 結束後問三個測試後問題。

## 不可提示內容

- 不要告訴玩家每天正解。
- 不要說 Day 9 曾由 Discard 改為 Seal。
- 不要先解釋 Ledger Desk 或 Containment Cabinet 的設計目的。
- 不要替玩家讀完整線索，除非他因畫面或字體問題看不清楚。

## 量化門檻

本輪可接受門檻：

- 1 位玩家：可完成十日流程，且能說出核心 loop。
- 2 位玩家：至少 1 位可無阻斷完成；兩位都能理解 Sell / Seal / Discard。
- 3 位玩家：至少 2 位可無阻斷完成；重大誤解集中在 1-2 個可修文字或 UI 的點。

Fail 條件：

- 任一玩家因 UI / 操作問題無法繼續。
- 多數玩家無法理解三個處置選項差異。
- 多數玩家看不懂 final summary 或升級效果。
- 同一日數被多數玩家誤判，且原因是文字或 UI 誤導。

## 回報格式

每位玩家測完後建立一份紀錄，建議命名：

`docs/production/playtests/2026-05-26-real-player-PLAYERID.md`

建議內容：

```markdown
# 真人盲測紀錄：PLAYERID

日期：
測試者背景：
測試方式：
是否完成十日流程：
中止點：

## 每日判斷

| Day | Oddity | 最終選擇 | 是否正確 | 主要推理 / 誤解 |
| --- | --- | --- | --- | --- |

## 觀察

- 操作：
- 文字理解：
- UI 可讀性：
- 節奏：
- 情緒反應：

## 測試後三問

1. 你覺得這個遊戲主要在玩什麼？
2. 哪一天或哪個古物最難判斷？為什麼？
3. 你會不會想再跑一次，看看升級後有什麼差異？為什麼？

## 結論

- 通過 / 條件式通過 / 失敗：
- 必修：
- 可延後：
```

## 下一步

完成第一位真人盲測後，先不要立即加內容。先根據紀錄判斷是：

- 只需要文字修正；
- 需要 UI 可讀性修正；
- 需要經濟或正解調整；
- 或可以進入 demo baseline commit / release note 整理。
