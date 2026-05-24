# Demo 試玩報告

本報告記錄 2026-05-24 的人工三日 demo 驗證。請只記錄實際觀察，不記錄未驗證的設計猜測。

## 測試版本

- Commit: `12f68de` + 未提交 UI 修正
- 匯出路徑: `exports/windows/CursedCurioShop.exe`
- 自動 smoke 測試指令: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`
- 測試者: 使用者人工檢驗 + Codex 自動驗證
- 日期: 2026-05-24

## 自動 Preflight

- [x] 單元測試通過。
- [x] Godot headless 專案載入通過。
- [x] 三日流程 smoke script 通過。
- [x] Windows 匯出檔存在。

## 啟動流程

- [x] 遊戲可從 Godot debug run 啟動並進入 demo 流程。
- [x] 主選單與檢視桌流程未回報阻斷錯誤。
- [x] Start / 進入商店流程未回報阻斷錯誤。

## 三日流程

- [x] Day 1 以 Cash 100 與 Reputation 50 開始。
- [x] 玩家可以從商店進入檢視桌。
- [x] 檢視桌會顯示目前異物的名稱與描述。
- [x] Magnifier、UV Lamp、Thermometer 都會產生可閱讀的線索文字。
- [x] Appraisal Notes 會保留已發現的工具線索。
- [x] Sell、Seal、Discard 按鈕可見且可使用。
- [x] 做出處置決策後，會開啟結果面板並顯示 cash / reputation 變化。
- [x] Back To Shop 可回到商店場景。
- [x] 最終日前，Next Day 會推進到下一個每日異物。
- [x] 最終日結果按鈕文字為 `Return to Menu`。
- [x] Day 3 結束後，Return To Menu 會回到主選單。

## 後果與結局

- [x] 正確處置會產生比至少一種錯誤處置更好的結果。
- [x] 錯誤處置路徑可以觸發異常事件。
- [x] Day 1 錯誤出售 Whispering Teacup 可以進入 bad ending 路徑。
- [x] Cash 與 reputation 的變化在結果面板保持可見。

## 可讀性紀錄

| ID | 嚴重度 | 日數 / 異物 | 問題 | 重現步驟 | 預期 | 實際 |
| --- | --- | --- | --- | --- | --- | --- |
| VIS-005 | 已修正 | Bad Ending / Whispering Teacup | 壞結局 overlay 先前會與一般結果 UI 重疊，且第一版背景仍有 ledger 裁切問題。 | Day 1 對 Whispering Teacup 選擇 Sell，進入 Frost Sale bad ending。 | 壞結局只顯示單一置中卡片、最終 Cash/Reputation 與 Return to Menu。 | 已改為暗色遮罩 + 固定尺寸 BadEndingCard，並停用後續決策操作。 |

## 通過結果

- [x] 通過：demo 可以在沒有阻斷問題的情況下完成。
- [ ] 條件式通過：demo 可以完成，但分享前應先修正列出的問題。
- [ ] 失敗：demo 目前無法完成。

## 下一步

- Demo Slice 可視為已通過人工三日驗證。
- 下一個產品里程碑應從 post-MVP 方向中選一個切入：更多每日物件、強化失敗條件、封印物保存、或顧客呈現流程。
