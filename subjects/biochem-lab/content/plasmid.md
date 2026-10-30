=== summary ===
# 質體 DNA 萃取與洋菜膠電泳 重點整理

> 2026/10/01 實驗課（周志銘）：少量質體 DNA 萃取（miniprep）＋洋菜膠膠體電泳。講義：plasmid mini-preparation_agarose gel electrophoresis 上課講義；影片：miniprep。

## 1. 鹼萃取法（alkaline lysis）為什麼能只抽到質體 ⭐⭐
- 質體是**共價閉合環狀（CCC）＝超螺旋**，而且比染色體 DNA 小很多；染色體 DNA 是長的線狀片段。
- 鹼／SDS 讓細胞裂解、內容物變性 → 中和後，**變性的蛋白質與高分子量染色體 DNA 一起沉澱**，上清液留下質體 DNA（與 RNA）。

## 2. S1／S2／S3 三種溶液 ⭐⭐⭐
| 溶液 | 功能 | 成分與作用 |
|---|---|---|
| **S1** | **Resuspension**（懸浮菌體） | Tris-HCl pH 8.0（緩衝）、**EDTA**（螯合金屬離子、抑制 DNase）、glucose（增加黏稠度）、**RNase A**（分解 RNA，kit 才有） |
| **S2** | **Lysis**（裂解） | **NaOH**（強鹼破壞細胞膜、DNA 變性）＋ **SDS**；**輕輕上下顛倒 6–8 次、不可劇烈搖晃、不超過 2 分鐘**（否則染色體 DNA 斷裂） |
| **S3** | **Neutralization**（中和） | **Potassium acetate**（與 SDS 形成不溶的 PDS，帶走變性蛋白與染色體 DNA）＋ acetic acid（中和 NaOH）；加完放冰上 |

- **RNA 用 RNase A 去除，加在 S1**。S1 出問題 → 膠底有一團「low molecular weight nucleic acid」（殘留 RNA）。
- 傳統鹼萃取法沒有 RNase A；kit 的 S1 才有。

## 3. 管柱純化（silica spin column） ⭐⭐
| 步驟 | 條件 | 目的 |
|---|---|---|
| 吸附 | **低 pH、高離子強度、chaotropic salt（離液鹽）** | 核酸結合到 silica 膜上，雜質流過 |
| 洗 | W1 → WS（含 ethanol） | 洗掉雜質；最後**空轉 3 分鐘**除去殘留酒精 |
| 沖提（elution） | **高 pH（8.0–8.5）、低離子強度** | 核酸離開膜 → 用 EB（5 mM Tris-HCl pH 8.5）或 ddH₂O |

- Elution buffer 選 **TE buffer pH 8.0**（DNA 在 pH 7.4–8.0 最穩定）；PBS 是細胞與蛋白質實驗用的。
- 抽好的質體存 **−20 °C**，下週限制酶實驗用。

## 4. Miniprep 流程（本實驗）
1. 1.5 mL 隔夜菌液離心（助教已處理）。
2. **200 µL S1** 懸浮 → **200 µL S2** 輕搖至澄清（≤ 2 分鐘）→ **300 µL S3** 輕搖、冰上。
3. 13,000 rpm 離心 10 分鐘 → 上清液到 spin column，10,000 rpm 1 分鐘。
4. 400 µL W1 → 600 µL WS 各離心 1 分鐘 → **空轉 8,000 rpm 3 分鐘**。
5. 換新管，加 **60 µL ddH₂O／EB**，8,000 rpm 3 分鐘收 DNA。
6. 取 3 µL DNA ＋ 3 µL 2× loading dye 跑膠。

## 5. 核酸定量（UV 260 nm）
- 核酸吸收峰 **~260 nm**：dsDNA ≈ A₂₆₀ × **50** µg/mL；ssDNA × 33；ssRNA × 40。

## 6. 洋菜膠電泳 ⭐⭐⭐
- DNA 帶**負電**（磷酸骨架）→ 往**正極**跑。
- **跑得遠 = 分子小**。**洋菜膠濃度越高、孔隙越小 → 適合分離小分子**；兩個小片段分不開 → **提高濃度**。
- 本學期設定：
  | 項目 | 本學期 |
  |---|---|
  | 介質 | **agarose（洋菜膠）**，微波加熱 1 分鐘溶解 |
  | 緩衝液 | **TAE buffer** |
  | 電泳槽 | **水平式平板電泳槽** |
  | DNA 染劑 | **Gel Green**（降到約 60 °C 才加，1:10000） |
  | 照膠 | **藍光 LED 燈箱**（Gel Green 不用 UV） |
  | 電壓 | 120 V、約 20 分鐘 |
- **Loading dye（樣品染料）≠ DNA 染劑**：loading dye 含 **bromophenol blue、xylene cyanol**（追蹤染料，看跑到哪）與 **glycerol**（增加密度讓樣品沉入 well）；DNA 染劑（Gel Green、EtBr）才是讓 DNA 在燈箱下顯色。
- 常見 DNA 染劑：**EtBr** 嵌入雙股之間、UV 下橙紅螢光、致癌；**acridine orange**（dsDNA 綠、ssDNA／RNA 紅）；**Gel Green** 較安全（Ames test 無致突變性）、更靈敏、可直接丟棄。

## 7. 質體型態與移動速度 ⭐⭐⭐
- 同樣大小：**超螺旋（SC）> 線狀（L）> 開環（OC, nicked）**（由快到慢）。
- 未切的質體常見兩條帶：下面是 SC、上面是少量受損的 OC。
- 鹼萃取法 vs kit：鹼萃取法較多 OC 與雜質，kit 幾乎都是 SC。

## 8. 儀器注意事項
- 離心機：**樣品平衡**、蓋安全蓋、轉速、時間。
- 電源供應器：**電極方向**（DNA 往正極）、定電壓或定電流、時間。

=== slides ===
# 講義重點（plasmid mini-preparation、agarose gel electrophoresis）

| 講義段落 | 重點 |
|---|---|
| 鹼萃取法 | 質體 CCC、小；鹼／SDS 變性後染色體 DNA 與蛋白一起沉澱 |
| S1 | Kit 版含 RNase A；傳統法沒有 |
| Silica 管柱 | 低 pH、高鹽、chaotropic salt 吸附；高 pH、低鹽沖提 |
| UV 定量 | 260 nm；dsDNA × 50 µg/mL |
| 電泳原理 Q1–Q3 | DNA 帶負電；膠越濃孔越小；本課程用 TAE |
| Q4 | loading dye vs DNA 染劑的差別 |
| Q5 | 介質 agarose、微波加熱、Gel Green |
| Q8–Q9 | 鹼萃取 vs kit 的差異；SC > L > OC |
| 1 kb DNA ladder | 250 bp、500、750 bp、1、1.5、2、2.5、3、4、5、6、8、10 kb |

=== exam ===
# 考點分析

## 🔥 高頻考點
- **S1 = resuspension、S2 = lysis、S3 = neutralize**（114 連考三題）。
- **RNase A 加在 S1**；elution 用 **TE pH 8.0**。
- 照膠用**藍光 LED**、染劑 **Gel Green**、緩衝液 **TAE**、介質 **agarose**、**水平式**電泳槽。
- 移動速度 **SC > L > OC**；跑得遠的分子小；小片段分不開要**提高**膠濃度。
- Loading dye 成分（複選）：bromophenol blue、xylene cyanol、glycerol（沒有 Orange G）。

## 📝 出題模式
- 單選以中文題幹為主，常強調「**本學期**」用的試劑。
- 手寫題：給 pTMU 電泳圖，問線狀或環狀、lane 2 的低分子量核酸是什麼（RNA）、哪個 buffer 出錯（S1）、解釋雙切結果。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| 照膠用 UV | **藍光 LED**（Gel Green）；EtBr 才要 UV |
| 染劑是 EtBr | 本學期 **Gel Green** |
| Elution buffer 用 PBS | **TE pH 8.0**（或 EB pH 8.5） |
| S2 要用力搖勻 | **輕輕顛倒**，否則染色體 DNA 斷裂污染 |
| OC 比線狀跑得快 | **SC > L > OC** |
| Loading dye 讓 DNA 顯色 | Loading dye 是追蹤與增加密度；顯色靠 DNA 染劑 |
