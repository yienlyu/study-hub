=== summary ===
# SDS-PAGE 鑄膠、電泳與染色 重點整理

> 📌 **期末範圍。**今年尚未上課，先以百十三共筆彙編，上課後再依今年 slides、錄影與共筆更新。

## 1. 原理 ⭐⭐⭐
- **SDS**（sodium dodecyl sulfate，陰離子界面活性劑）讓蛋白質**變性**並包上**均勻的負電** → 電荷／質量比相同，只剩**分子量**決定移動速度。
- 蛋白質往**正極**跑；**分子量大跑得慢、小的跑得遠**。
- **膠濃度（T%）越高、孔越小、跑得越慢**，適合分離小蛋白。

## 2. 膠的成分 ⭐⭐⭐
| 成分 | 作用 |
|---|---|
| **Acrylamide** | 單體，聚合成直鏈的**主要結構**；**有神經毒性** |
| **Bis-acrylamide**（N,N′-methylene-bisacrylamide） | **交聯劑**，連接直鏈形成網狀孔洞（沒有它膠不會凝） |
| **APS**（ammonium persulfate） | **提供自由基**，啟動聚合 |
| **TEMED** | **催化劑**，傳遞電子、穩定自由基 |
| SDS | 讓蛋白質變性、帶負電 |
| Tris-HCl | 緩衝（上膠 pH 6.8、下膠 pH 8.8） |

- APS 和 TEMED **最後鑄膠時才加**；加越多聚合越快、鏈越短。
- **β-mercaptoethanol 不是膠的成分**（它在 sample buffer）；**PAGE 是縮寫不是成分**。

## 3. 上膠與下膠 ⭐⭐⭐
| | **上膠 stacking gel** | **下膠 running／resolving gel** |
|---|---|---|
| pH | **6.8** | **8.8** |
| 濃度 | 低（孔大） | 高（依蛋白大小調整） |
| 功能 | **濃縮（stack）**蛋白質，讓所有樣品在同一起跑線 | **分離**不同分子量的蛋白質 |
- Running buffer（Tris-glycine）**pH 8.3**；sample buffer pH 6.8。**pH 最低的是上膠（6.8）**。
- **Stacking 機制**：在 pH 6.8 的上膠中 **glycine 幾乎不帶電、跑最慢**，**Cl⁻ 跑最快**，蛋白質被夾在中間濃縮成一條線 → 順序（負極 → 正極）：**Glycine – Protein – Chloride**。進入 pH 8.8 下膠後 glycine 帶負電加速超過蛋白質，蛋白質開始依分子量分離。

## 4. Sample buffer ⭐⭐⭐
| 成分 | 作用 |
|---|---|
| Tris-HCl pH 6.8 | 緩衝 |
| **SDS** | 變性、給負電 |
| **β-mercaptoethanol／DTT** | **還原劑，打斷雙硫鍵** |
| **Glycerol** | 增加密度，讓樣品沉入 well |
| **Bromophenol blue** | 追蹤染料（dye front） |
- 混合後 **95 °C 煮 10 分鐘**變性，冷卻混勻再上樣。
- **nX buffer 的配法**：1 份 buffer ＋ (n − 1) 份樣品。
  - 3X、總量 150 µL → **SB 50 µL ＋ P 100 µL**。
  - 5X、well 最多 25 µL → 樣品最多 20 µL；要放 40 µg → 樣品濃度至少 **2 µg/µL**。

## 5. 鑄膠流程（W12）
1. 組裝：short plate 朝自己、spacer plate 在後，底部對齊夾進 casting frame，放上 casting stand；先注水測漏。
2. **下膠**：加 APS（50 µL 10%）與 TEMED（5 µL）→ 輕輕顛倒混勻（不可產生氣泡）→ 注到卡榫上緣。
3. **上面加水（或異丙醇）壓膠**：讓膠面平整、隔絕空氣、排出氣泡（異丙醇效果更好）。等約 20 分鐘凝固。
4. 倒掉水 → 上膠加 APS（25 µL）＋ TEMED → 注到 short plate 上緣 → **插齒梳**。
5. 凝固後取出，用擦手紙包好保存。
- 凝固不均：溫度太低或 APS／TEMED 沒混勻；有氣泡會讓色帶扭曲。

## 6. 電泳與染色（W14） ⭐⭐
- 樣品與 **protein marker（分子量標準）**一起上樣，蛋白質往正極跑。
- 跑完**拆膠時去掉上膠**，只染**下膠（running gel）**。
- 染色前要**用水洗膠，洗掉 SDS**：SDS 和 CBB 都帶負電會互斥，SDS 沒洗乾淨就染不上（或呈色變慢）。
- 染劑 **Coomassie brilliant blue（CBB）**：結合**帶正電的胺基酸（Lys、Arg、His）**與疏水區。
  - **G-250 比 R-250 多兩個甲基**；兩者溶解試劑、可偵測的濃度範圍、脫色液都不同。Bradford 定量用 G-250。

## 7. 估算分子量 ⭐⭐
- **Rf = 蛋白質移動距離 ÷ dye front 移動距離**。
- 以 **log（分子量）對 Rf（mobility）作圖** → 直線、**成反比**；用 marker 的標準曲線代入未知蛋白的 Rf 求分子量。

## 8. 其他電泳
| 類型 | 特點 |
|---|---|
| **Native PAGE** | 不變性，依電荷＋大小＋結構分離；**保留活性 → 可在膠上分析酵素活性** |
| SDS-PAGE | 變性，只依分子量 |
| Gradient PAGE | 膠濃度漸變，分得更開但製作麻煩 |
| Agarose | 主要跑 DNA |

## 9. 疑難排解
- Marker 和樣品都**沒有往下跑**：**電極接反**、**running buffer pH 錯誤**。
- 染色後呈色很慢或很淡：**樣品量太少**、**SDS 沒洗乾淨**。

=== slides ===
# 共筆重點（113 生化實驗 W7、W8：SDS-PAGE）

| 段落 | 重點 |
|---|---|
| 下膠配方（4 mL） | 30% acrylamide (37.5:1) 1333 µL、1 M Tris pH 8.8 1500 µL、10% SDS 40 µL、10% APS 20 µL、TEMED 2 µL、水 1105 µL |
| 上膠配方（2 mL） | 30% acrylamide 266 µL、1 M Tris pH 6.8 250 µL、10% SDS 20 µL、10% APS 10 µL、TEMED 2 µL、水 1452 µL |
| Sample buffer | Tris pH 6.8、4% SDS、5% 2-ME、0.15 M DTT、20% glycerol、0.01% bromophenol blue |
| T% | (acrylamide ＋ bis) ÷ 總體積 |
| Rf | 蛋白質距離 ÷ dye front 距離 |
| 器材 | casting stand、comb、spacer plate、short plate、casting frame、plastic seal |
| 毒性 | acrylamide 神經毒、SDS 傷眼、APS 傷黏膜、TEMED 神經毒 |

=== exam ===
# 考點分析

## 🔥 高頻考點（114 鄭嘉雄老師部分共 43 題，是生化實驗考古最大宗）
- **APS 提供自由基、TEMED 傳電子、acrylamide 是主結構、bis 交聯**。
- **β-ME 打斷雙硫鍵**；**SDS 變性並給負電**；**glycerol 讓樣品下沉**。
- **上膠 pH 6.8、下膠 pH 8.8、running buffer pH 8.3**；上膠濃縮、下膠分離。
- Stacking 順序 (−) **Glycine – Protein – Chloride** (+)。
- 染色前**水洗去 SDS**；只染 **running gel**；CBB 結合 **Lys**。
- **G-250 比 R-250 多兩個甲基**。
- **Rf = A／C（蛋白質距離 ÷ dye front）**；**log MW vs mobility**。
- 配 sample buffer 的計算題（3X、5X）。
- 要測酵素活性用 **native gel**。

## 📝 出題模式
- 單選英文＋中文各半，同一概念常換句話重考（APS 的作用出現三次）。
- 複選：呈色慢的原因（樣品少、SDS 未除）、蛋白質不動的原因（電極反、buffer pH）。
- 配合題（25 分）：Dr. Cheng 把蛋白 A、B 標籤弄混，用 SDS-PAGE 材料設計實驗並畫圖。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| SDS 是聚合必需的 | 聚合需要 acrylamide、bis、APS、TEMED；**SDS 不是** |
| APS 傳遞電子 | APS **產生自由基**；TEMED 傳遞電子 |
| 大蛋白跑得快 | **大蛋白跑得慢** |
| 高濃度膠跑得快 | 高濃度膠孔小、**跑得慢** |
| 上膠 pH 8.8 | 上膠 **6.8**、下膠 **8.8** |
| 染上膠和下膠 | 拆膠時去掉上膠，**只染下膠** |
| 洗膠是為了去鹽 | 洗膠是為了**去 SDS** |
| 3X buffer：SB 3 µL ＋ P 150 µL | 總量 150 µL：**SB 50 ＋ P 100** |
