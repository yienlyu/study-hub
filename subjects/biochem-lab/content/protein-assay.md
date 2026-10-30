=== summary ===
# Pipetman 操作與蛋白質定量 重點整理

> 2026/09/17 實驗課（陳顧中）：實驗室簡介、Pipetman 操作、Bradford 蛋白質定量。講義：protein quantification principle、實驗操作講義、Pipetman 操作。

## 1. Pipetman（微量吸管） ⭐⭐⭐
| 型號 | 可吸取範圍 | 刻度讀法（由上往下三格） |
|---|---|---|
| **P-20** | 2–20 µL | 0-6-8 → **6.8 µL**（最下一格是小數點後一位） |
| **P-200** | 20–200 µL | 0-6-3 → **63 µL** |
| **P-1000** | 100–1000 µL | 0-6-3 → **630 µL**（最上一格是千位） |
- **P-100 讀數 0-6-3 = 63 µL**（114 考古第 1 題）。同一個刻度在不同型號代表不同體積，先看型號再讀。
- 操作：**第一段（first stop）吸**、吸管尖放入液面下等液面到位才離開；**第二段（second stop）把殘液完全打出**；退 tip 鈕丟棄 tip。
- 實驗完把吸管**轉回最大值**收好。
- 練習：在 parafilm 上點 2、4、6、8、10 µL 染劑；另吸 50、150、450 µL 水到 1.5 mL 離心管給老師檢查。

## 2. 選擇蛋白質定量方法要考慮什麼 ⭐⭐
1. 蛋白質的量（amount available）
2. 蛋白質濃度（concentration）
3. 是否有干擾物（interfering chemicals）
4. 方法的專一性（specificity）
5. 方便與可信度（ease and reliability）

> **蛋白質大小不在考慮清單裡**（114 考古第 9 題）。

## 3. 五種定量法比較 ⭐⭐⭐
兩大類：**天然發色團**（UV 光譜，物理方法）vs **化學反應產生發色團**（Biuret、Lowry、BCA、Bradford）。

| 方法 | 原理 | 波長 | 優點 | 缺點 |
|---|---|---|---|---|
| **UV** | 芳香族胺基酸（**Trp、Tyr**、Phe）吸 **280 nm**；肽鍵 C=O 吸 190–210 nm | **280 nm** | **唯一不破壞樣品（non-destructive）**、可監測結合 | 靈敏度低（至少 20–50 µg）；芳香族胺基酸少就失準 |
| **Biuret** | 鹼性下 **Cu²⁺ 與肽鍵 N** 形成紫色錯合物 | 540 nm | **唯一不受胺基酸組成影響**，只看肽鍵數 | 最不靈敏；EDTA 等螯合劑干擾 |
| **Lowry** | Biuret ＋ **Folin reagent（phosphomolybdic + phosphotungstic acid）** 被 Tyr、Trp 還原成**鉬藍** | 750 nm | 比 Biuret 靈敏（0.01–1 mg/mL） | 受 Tyr／Trp 含量影響；還原劑（DTT、β-ME）、螯合劑、高鹽、酸干擾 |
| **BCA** | 蛋白質把 **Cu²⁺ 還原成 Cu⁺**，Cu⁺ 與 2 個 BCA 形成**紫色**錯合物 | 562 nm | 顏色穩定、較不受去垢劑影響 | 還原劑、銅螯合劑（EDTA、EGTA）干擾 |
| **Bradford** | **CBB G-250** 酸性下茶色，結合蛋白質（提供較中性環境）變**藍色** | **595 nm** | 干擾最少、靈敏、**單一步驟、快速呈色** | 偏好**疏水性與鹼性胺基酸**（Arg、Lys）；不同蛋白差到 50 倍 → 標準品要選相近的蛋白；鹼與界面活性劑干擾 |

- **Biuret、Lowry、BCA 都靠 Cu²⁺**；**Bradford 是唯一和離子無關的**（靠酸鹼變色）。
- 只用來定量特定蛋白的方法：gel filtration、HPLC、mass spectrometry。**Real-time PCR 不能測蛋白質**。

## 4. 本次實驗：Bradford assay ⭐⭐⭐
- 材料：BSA 標準品（1 µg/µL）、待測樣品、1× Bradford reagent、ddH₂O、**96 孔盤、ELISA reader**。
- 步驟：BSA 0、2、4、6、8、10、15、20 µL 加水到 50 µL；待測物 2 µL ＋ 48 µL 水 → 各加 **200 µL Bradford reagent** → 混勻、室溫 5 分鐘 → 取 150 µL 上 96 孔盤讀值。
- 讀值波長：分光光度計 **595 nm**；實驗用的 ELISA reader 濾片是 550／630 nm（講義兩種寫法都有）。
- 數據：**X 軸 = BSA 量（µg），Y 軸 = 吸光值**，作線性回歸得 y = ax + b 與 **R²（越接近 1 越好）**。
- 計算：x = (y − b) / a。待測物取 2 µL，所以**算出的 µg 要再 ÷ 2 才是 µg/µL**。
  - 講義範例：OD 0.14，回歸式 y = 0.0309x + 0.0028 → x = 4.45 µg → **2.225 µg/µL**。
- 加孔盤要依序加、不可空格；**96 孔盤底部不可用手摸**。
- 作業：上傳 Excel 原始檔，成績 = R² × 90 ＋ 待測物濃度（±0.2 得 10 分、±0.6 得 5 分）。

## 5. 實驗室規則（會影響成績）
- 總成績：**報告 30% ＋ 期末考 50% ＋ 平時 20%**（平時含組內互評、遲到早退）。
- 無故缺課一次總成績打八折、兩次打六折；遲到（鐘響後 10 分鐘）超過三次每次扣 5 分。
- 報告要**手寫**在 A4 紙上，附原始數據。

=== slides ===
# 講義重點（protein quantification principle、Pipetman 操作）

| 講義頁 | 重點 |
|---|---|
| 選擇方法 | 五個考量：量、濃度、干擾物、專一性、方便可信 |
| Beer's law | A = ε × l × c，吸光值和濃度成正比 |
| UV | 280 nm（芳香族）、190–210 nm（肽鍵）；不破壞樣品但靈敏度低 |
| Biuret | 鹼性硫酸銅 ＋ 肽鍵 N；540 nm；不受胺基酸組成影響 |
| Lowry | Biuret ＋ Folin（磷鉬酸、磷鎢酸）→ 鉬藍；750 nm |
| BCA | Cu²⁺ → Cu⁺ ＋ BCA → 紫色；562 nm |
| Bradford | CBG 茶色 → 藍色；595 nm；單一步驟 |
| Pipetman | P-20／P-200／P-1000 讀數；first stop 吸、second stop 打出 |

=== exam ===
# 考點分析

## 🔥 高頻考點
- **Pipetman 讀數**：P-100 讀 0-6-3 = 63 µL、P-1000 讀 0-6-3 = 630 µL。
- **Lowry 的 Folin reagent 含 phosphomolybdic acid**（114 連續兩題）。
- **Cu²⁺** 是 Biuret／Lowry／BCA 的關鍵離子；**Bradford 與離子無關**。
- **UV 是唯一 non-destructive**；280 nm；**Thr 不能**用 UV 測（非芳香族）。
- Bradford：**CBB（Coomassie）**、595 nm、單一步驟（「multiple-steps」是錯的）、偏好鹼性與芳香族胺基酸（**Asp 不行**）。
- **標準曲線計算**：Y = 0.25X + 0.1、Y = 0.6 → X = 2；最佳 R² 選最接近 1 的。
- 用 **ELISA reader** 讀 96 孔盤。

## 📝 出題模式
- 幾乎都是單選，英文題幹；常有「Continued.」題組（同一題情境問兩題）。
- 手寫題：寫出蛋白質定量會用到的東西（BSA、未知蛋白、Bradford reagent、eppendorf、ELISA reader、96 孔盤）。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| UV 測蛋白質靠 260 nm | **280 nm**（260 nm 是核酸）；選項只有 Phe 時選 Phe（257 nm） |
| 選擇定量法要考慮蛋白質大小 | 不需要；要考慮量、濃度、干擾物、專一性 |
| Bradford 是多步驟 | **單一步驟、快速呈色** |
| Bradford 用 methylene blue | **Coomassie brilliant blue G-250** |
| G-250 和 R-250 差一個甲基 | 差**兩個**甲基（G-250 多兩個） |
| 算出的濃度直接就是答案 | 取 2 µL 樣品，要 **÷ 2** |
