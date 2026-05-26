# Agent 盲測與線索修正紀錄

日期：2026-05-26
測試者：Codex 協調，3 位代理玩家
範圍：十日流程的 Sell / Seal / Discard 線索判讀

## 前提

本輪不是真人外部盲測。代理玩家只能檢查文字線索是否自洽、規則是否可推理，不能取代真人操作手感、情緒反應或畫面注意力測試。

## 代理玩家設定

- 玩家 A：保守型，傾向保護聲望，避免害到買家。
- 玩家 B：逐利型，危險不明確時偏向 Sell。
- 玩家 C：一般新手，第一次玩，以直覺理解 danger level、售價與工具線索。

## 原始盲測結果

標準答案：

| Day | Oddity | Correct |
| --- | --- | --- |
| 1 | Whispering Teacup | Seal |
| 2 | Mirror Coin | Seal |
| 3 | Ashen Music Box | Discard |
| 4 | Cold Brass Key | Seal |
| 5 | Glass Eye | Sell |
| 6 | Black Wax Candle | Discard |
| 7 | Moth-Eaten Doll | Seal |
| 8 | Silver Funeral Bell | Seal |
| 9 | Cracked Hand Mirror | Seal |
| 10 | Red Thread Spool | Sell |

| 玩家 | 命中 | 主要誤判 |
| --- | ---: | --- |
| A 保守型 | 9/10 | Day 3 誤判為 Seal |
| B 逐利型 | 5/10 | Day 2、3、4、6、9 |
| C 新手型 | 7/10 | Day 3、4、9 |

## 判斷

- Day 3 是最嚴重問題：3/3 代理玩家都沒有推到 Discard。原本「自奏機構」與「帶我回家」會讓玩家理解成 Seal 或保留，而不是破壞完整盒身。
- Day 9 是次要問題：原始設定為 Discard，但 2/3 代理玩家選 Seal。原本「遮蓋後才回溫」容易讓玩家以為只要隔離即可。
- Day 4 對逐利型與新手仍偏弱：遠端鎖具危害不夠明確，因此有人會 Sell。
- Day 5、7、8、10 判讀穩定，可暫時不動。

## 已修正

- Day 3 Ashen Music Box：強化「完整盒身會延長曲調」與「打斷曲調」線索，讓玩家理解問題在保持完整。
- Day 4 Cold Brass Key：強化「遠端鎖具連動」與看不見的鎖正在被拉動，降低誤 Sell。
- Day 9 Cracked Hand Mirror：先嘗試強化「完整反射面保留第二張臉」與「未完成的破裂」線索，但重測仍只有 1/3 代理玩家推到 Discard。
- Day 9 最終改為 Seal：這更符合玩家主流直覺。新的線索改成「遮蓋玻璃留住第二張臉」，封存成本從 20 調為 15，讓十日正確路徑仍維持 Final Cash 180。

## 修正後抽查

針對 Day 3 / Day 4 / Day 9 重測：

| Day | 原問題 | 修正後結果 |
| --- | --- | --- |
| Day 3 | 3/3 誤判，無人推到 Discard | 3/3 推到 Discard |
| Day 4 | 新手與逐利型可能 Sell | 3/3 推到 Seal |
| Day 9 | 原正解 Discard，但玩家直覺偏 Seal | 改正解為 Seal，避免設計師答案 |

## 驗證

```powershell
python -m tools.godot.sync_item_scenes --root .
python -m unittest tests.test_commercial_demo_design tests.test_godot_localization tests.test_godot_item_scene
python -m tools.project_status --root . --run-tests
```

結果：

- Targeted tests：14 passed。
- Full project status at this pass：101 tests passed。
- Latest release-audit status on 2026-05-26：106 tests passed, 40/40 assets ready.
- Asset outputs：40/40 ready across 10 item(s)。

## 下一步判斷

現在可進入下一個產品切片，但建議順序是：

1. 第二個店鋪 perk 已在 `2026-05-26-shop-perk-pass.md` 完成為 Containment Cabinet / 封存櫃。
2. 下一步不要同時新增奇物批次，避免混淆驗證來源。
3. 升級後二周目 smoke 與 progression panel agent 盲測已在 `2026-05-26-shop-perk-pass.md` 完成。
4. 下一次 build handoff 應優先整理 release 包裝與真人 playtest 限制，不要新增奇物或第三個 perk。
