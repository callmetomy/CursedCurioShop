# Demo 試玩報告

本報告用於一次具體的 Windows demo 試玩。請記錄實際觀察，不要記錄未驗證的設計猜測。

## 測試版本

- Commit: `2eb89e2`
- 匯出路徑: `exports/windows/CursedCurioShop.exe`
- 自動 smoke 測試指令: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`
- 測試者: Codex 自動 preflight
- 日期: 2026-05-21

## 自動 Preflight

- [x] 單元測試通過。
- [x] Godot headless 專案載入通過。
- [x] 三日流程 smoke script 通過。
- [x] Windows 匯出成功。

## 啟動流程

- [ ] 遊戲可從匯出的 Windows 執行檔啟動。
- [ ] 主選單顯示正常，沒有缺失貼圖、缺失字型或腳本錯誤。
- [ ] Start 按鈕可進入可遊玩的商店場景。

## 三日流程

- [ ] Day 1 以 Cash 100 與 Reputation 50 開始。
- [ ] 玩家可以從商店進入檢視桌。
- [ ] 檢視桌會顯示目前異物的名稱與描述。
- [ ] Magnifier、UV Lamp、Thermometer 都會產生可閱讀的線索文字。
- [ ] Appraisal Notes 會保留已發現的工具線索。
- [ ] Sell、Seal、Discard 按鈕可見且可使用。
- [ ] 做出處置決策後，會開啟結果面板並顯示 cash / reputation 變化。
- [ ] Back To Shop 可回到商店場景。
- [ ] 最終日前，Next Day 會推進到下一個每日異物。
- [ ] 最終日結果按鈕文字為 `Return to Menu`。
- [ ] Day 3 結束後，Return To Menu 會回到主選單。

## 後果與結局

- [ ] 正確處置會產生比至少一種錯誤處置更好的結果。
- [ ] 錯誤處置路徑可以觸發異常事件。
- [ ] 低 reputation 可以進入 bad ending 路徑。
- [ ] Cash 與 reputation 的變化在場景切換後仍保持可見。

## 可讀性紀錄

| ID | 嚴重度 | 日數 / 異物 | 問題 | 重現步驟 | 預期 | 實際 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## 通過結果

- [ ] 通過：demo 可以在沒有阻斷問題的情況下完成。
- [ ] 條件式通過：demo 可以完成，但分享前應先修正列出的問題。
- [ ] 失敗：demo 目前無法完成。
