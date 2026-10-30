=== summary ===
# 膠體過濾（Gel filtration） 重點整理

> 📌 **期末範圍。**今年尚未上課，先以百十三共筆彙編，上課後再依今年 slides、錄影與共筆更新。

## 1. 原理 ⭐⭐⭐
- 又稱 **size exclusion chromatography（分子篩，molecular sieve）**：依**分子大小**分離。
- 膠珠有孔洞：**大分子進不去孔洞、走外面 → 先流出**；**小分子鑽進孔洞、路徑長 → 後流出**。
- 層析圖（X 軸時間、Y 軸吸光值）：**最早的峰 = 最大分子，最晚的峰 = 最小分子**。

## 2. 優點與應用 ⭐
- 不受溫度、pH、離子強度、緩衝液組成影響 → 任何條件都能做；吸附很少；**沖提體積和分子量相關**。
- 應用：**去鹽（desalting）**、蛋白質純化、**估算未知蛋白的分子量**。

## 3. 三種樹脂 ⭐⭐
| 樹脂 | 材質 | 特性 |
|---|---|---|
| **Sephadex** | **dextran** 以 epichlorohydrin 交聯 | 高解析、快、回收率高；不會熔化，可高壓滅菌；**本實驗用 Sephadex G-50（分離 1,500–30,000 Da）** |
| **Sepharose** | **agarose**（去掉帶電多醣的 agar） | 分離範圍很廣、適合很大的分子與病毒；**40 °C 以上會熔、冷凍會壞**；pH 4–9 |
| **Sephacryl HR** | allyl dextran ＋ N,N′-methylene bisacrylamide | 機械強度高、pH 2–11、可用 SDS、尿素；實驗室與工業規模都可 |

- **Sepharose 2B／4B／6B**：數字 = agarose 百分比；**數字越大、孔越小、適合越小的分子**。
  | | 2B | 4B | 6B |
  |---|---|---|---|
  | 分離範圍 | 70–40,000 kDa | 70–20,000 kDa | **10–4,000 kDa** |
  | % agarose | 2 | 4 | 6 |
- **選樹脂第一個要考慮：optimal MW separation range（最適分離範圍）**。

## 4. 影響分離的因素 ⭐⭐
- **Bed height（管柱高度）**：越高解析度越好，但太長流速太慢。
- **填充品質**：要均勻、無紋路、無氣泡。
- **流速**：要恆定、適當。
- 管柱體積與尺寸。
- **蛋白質來源不影響**分子量測定（114 考古）。

## 5. 本實驗（W10，11/12）
- 樣品：**BSA（約 67,000 Da）＋ methyl orange（約 400–600 Da，橘黃色染料）**，共 20 µL。
- 管柱：Sephadex G-50；沖提液：**1× PBS**。
- 步驟：
  1. 裝管柱：先加 PBS 到八分滿 → 加均勻的 G-50 懸浮液讓它自然沉降，到離上方管套約 0.5 cm（1–2 mL）→ 流乾後塞住。
  2. 上樣：20 µL 樣品**加在膠面正中央**，不能沿管壁加 → 打開讓樣品完全流入膠體 → 塞住。
  3. 收集：沿管壁慢慢加 PBS，維持 3–4 cm 液面；**每 10 滴收一管，共 10 管**。
  4. 分析：
     - **Methyl orange**：各取 100 µL 讀 **OD 450 nm**。
     - **BSA**：各取 50 µL ＋ 200 µL Bradford reagent，室溫 5 分鐘，讀 **OD 595 nm**。
- 預期：**BSA 的峰在前、methyl orange 的峰在後**，兩個峰分得越開越好（作業依此給分）。

=== slides ===
# 講義重點（gel filtration principle、protocol）

| 講義頁 | 重點 |
|---|---|
| 原理 | 分子篩，依大小分開球狀蛋白質；最常用 Sephadex（細菌 dextran 交聯） |
| Gel materials | Sepharose（agarose）、Sephadex（dextran）、Sephacryl（allyl dextran ＋ bis） |
| Advantages | 不受溫度、pH、離子強度影響；吸附少；沖提體積對應分子量 |
| Applications | Desalting、純化、估分子量 |
| 影響因素 | 流速、管柱體積與尺寸 |
| Protocol | Sephadex G-50、1× PBS、BSA ＋ methyl orange；OD450 ／ Bradford OD595 |
| 作業評分 | 兩峰分開一格 90 分；沒分開 88 分；與預期相反 85 分 |

=== exam ===
# 考點分析

## 🔥 高頻考點
- Gel filtration 又稱 **size exclusion chromatography**。
- 要收**最小**分子 → 選**最晚**的峰；最大分子 → 最早的峰。
- 第一個要考慮 **optimal MW separation range**；Sepharose **6B 孔最小**。
- 本學期樹脂 **Sephadex G-50**；**OD 450 nm 測 methyl orange**、BSA 用 Bradford。
- **不影響**分子量測定的是「蛋白質來源」（bed height、填充品質、流速都會影響）。

## 📝 出題模式
- 單選英文題幹，常附層析圖或 Sepharose 表格。
- 情境題：果汁中的 ascorbic acid（小分子）→ 選 6B。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| 小分子先流出 | **大分子先流出** |
| Gel filtration = affinity chromatography | **Size exclusion** |
| 2B 孔最小 | **6B** 孔最小（agarose 6%） |
| 本實驗用 Sepharose G50 | **Sephadex G-50**（Sepharose 沒有 G 系列） |
| 450 nm 測 BSA | 450 nm 測 **methyl orange** |
| 樣品沿管壁加 | 加在**膠面正中央**；沖提液才沿管壁加 |
