# Demo 試玩報告

本報告用於一次具體的 Windows demo 試玩。請記錄實際觀察，不要記錄未驗證的設計猜測。

## 測試版本

- Commit: `d5489be`
- 匯出路徑: `exports/windows/CursedCurioShop.exe`
- 自動 smoke 測試指令: `godot --headless --path godot --script res://tools/smoke_three_day_flow.gd`
- 測試者: Codex 自動 preflight + 截圖檢視紀錄
- 日期: 2026-05-22

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

| ID | 嚴重度 | 日期 / 異物 | 問題 | 重現步驟 | 預期 | 實際 |
| --- | --- | --- | --- | --- | --- | --- |
| VIS-001 | 已修正 | Day 1 / Whispering Teacup | 茶杯表面看起來過白，裂紋與污漬細節比較像幾何 marker，而不像表面細節。 | 檢視 Day 1，旋轉茶杯，並使用 Magnifier / UV Lamp。 | 瓷器仍保持淺色，但能看出暖色老化感、表面裂紋、污漬與 UV ring 細節。 | 茶杯目前使用較溫暖的材質反應，並以 decal 風格呈現裂紋 / 污漬細節與只在 UV 下顯示的 ring mark。 |
| VIS-002 | 已修正 | Day 2 / Mirror Coin | 硬幣起始角度偏側面或過亮，且 UV Lamp 會顯示固定的藍白圓圈，導致正面與鑑定刮痕不易閱讀。 | 推進到 Day 2，檢視 Mirror Coin，並使用 Magnifier / UV Lamp。 | 硬幣正面可讀，刮痕看起來像表面的鑑定痕跡；UV 模式不應顯示與物件無關的固定圓圈。 | Mirror Coin 目前以正面朝向開始，使用較大的 y 軸投射表面 decal，且固定 UVClueMarker 已保持隱藏。 |
| VIS-003 | 已修正 | Day 3 / Ashen Music Box | 音樂盒輪廓太像單純方塊，且小零件在檢視截圖中容易看成分離碎片。 | 推進到 Day 3 並檢視 Ashen Music Box。 | 物件在不依賴文字描述前，就應能被辨識為連成一體的音樂盒。 | Runtime GLB 目前保留底座、上蓋、圓筒與搖柄，放大主體並移除容易像散件的腳座 / 小把手。 |

## 通過結果

- [ ] 通過：demo 可以在沒有阻斷問題的情況下完成。
- [ ] 條件式通過：demo 可以完成，但分享前應先修正列出的問題。
- [ ] 失敗：demo 目前無法完成。
