# 繁體中文視覺檢查紀錄

日期：2026-05-25
測試者：Codex
版本：本機工作樹，Windows 匯出已於 2026-05-25 刷新

## 驗證指令

```powershell
python -m tools.project_status --root . --run-tests
godot --headless --path godot --script res://tools/smoke_three_day_flow.gd
godot --path godot --script res://tools/capture_traditional_chinese_review.gd
```

注意：截圖工具需要非 headless Godot，因為 headless 模式使用 dummy renderer，無法讀取 viewport texture。

## 截圖範圍

- `1152x648`：對應目前 Codex/Godot debug 視窗常見檢查尺寸。
- `1280x720`：標準 16:9 桌面尺寸。
- 狀態：商店顧客備註、商店鑑定結果詳情、一般日結結果、最終流程總結。

## 截圖證據

![shop_customer_brief-1152x648](screenshots/shop_customer_brief-1152x648.png)
![shop_result_detail-1152x648](screenshots/shop_result_detail-1152x648.png)
![day_result-1152x648](screenshots/day_result-1152x648.png)
![final_summary-1152x648](screenshots/final_summary-1152x648.png)
![shop_customer_brief-1280x720](screenshots/shop_customer_brief-1280x720.png)
![shop_result_detail-1280x720](screenshots/shop_result_detail-1280x720.png)
![day_result-1280x720](screenshots/day_result-1280x720.png)
![final_summary-1280x720](screenshots/final_summary-1280x720.png)

## 結論

- 通過：商店顧客備註與店鋪帳本沒有超出面板。
- 通過：鑑定結果詳情能顯示異物、決策、結果、現金、聲望與後果，兩個尺寸都沒有超出面板。
- 通過：一般日結文字位於半透明文字底板內，按鈕與文字分區清楚。
- 通過：最終流程總結在 `1152x648` 與 `1280x720` 都沒有文字超框或按鈕遮住文字。
- 保留觀察：結果面板按鈕目前接近 ledger 下緣，但沒有遮擋內容。若後續文案變長，優先縮短最後紀錄文字或增加結果面板高度。

## 下一步

下一個建議切片是把 `oddity_0004` 納入可玩日程，先擴充到四天流程並補齊繁中視覺檢查，再決定是否一次推進到 10 件異物。
