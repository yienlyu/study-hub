=== summary ===
# MHC、抗原處理與呈現（陳玫潔）

## 1. T 細胞辨識什麼？
- 來自蛋白抗原的 **peptide**，由 **APC** 呈現，**結合在自身（self）MHC** 上，被**抗原專一 TCR** 辨識。
- **MHC restriction / dual recognition**（Zinkernagel & Doherty，**1996 諾貝爾**）：T 細胞同時辨識 MHC 與 peptide；peptide 同但 MHC 不同 → 不辨識；MHC 同但 peptide 不同 → 不辨識。
- 1980 諾貝爾：Benacerraf（Ir genes）、Dausset（HLA）、Snell（H-2）。
- 人類 MHC = **HLA（第 6 號染色體）**；小鼠 = **H-2（第 17 號）**。
- TCR 看 peptide 中間 + 周圍 MHC（大亨堡比喻）。

<div data-fig="mhc-restriction"></div>

<div data-fig="mhc-dual"></div>


## 2. MHC I vs MHC II ⭐⭐
| | **MHC class I** | **MHC class II** |
|---|---|---|
| 組成 | **α chain（α1、α2、α3）+ β2-microglobulin**（β2m 不是 MHC 基因編碼） | **α（α1、α2）+ β（β1、β2）**，皆 MHC 編碼 |
| Peptide 結合槽 | **α1 + α2**，**兩端封閉** | **α1 + β1**，**兩端開放** |
| Peptide 長度 | **8–10 aa**（ends buried；anchor 常為疏水 C 端；中間拱起） | **13–18（12 → >20）aa**（可伸出槽外；H-bond 分布全段） |
| 抗原來源 | **Endogenous**（細胞質：病毒、胞內菌） | **Exogenous**（endocytosis、phagocytosis、autophagy） |
| 辨識 T 細胞 | **CD8⁺ Tc**（CD8 結合 **α3**） | **CD4⁺ TH**（CD4 結合 **β2**） |
| 表現 | **所有有核細胞**（紅血球沒有） | **APC**（DC、macrophage、B）、胸腺上皮 |
| 基因 | **HLA-A、-B、-C** | **HLA-DP、-DQ、-DR**（A=α、B=β） |

<div data-fig="mhc-structure"></div>

> Class III 區域不是 MHC 分子，而是補體（factor B、C2、C4）與 **TNF、LT-α** 等。

## 3. MHC 多樣性
- **Polygeny**：每類有多個基因座（I：A/B/C；II：DR/DQ/DP）。
- **Allelic polymorphism**：每個基因座有極多 alleles（**class I 多形性 > class II**）。
- **Haplotype（linkage）polymorphism**：alleles 的組合不同。
- **Co-dominant expression**：父母雙方的 MHC 都表現。
- **Gene conversion**：減數分裂時由另一 MHC 基因複製序列 → 新 allele。
- ⭐ **MHC 多樣性是「個體間」差異（遺傳）**；BCR / TCR 多樣性是「個體內」差異（somatic DNA rearrangement）。MHC **不需重組、不需 RAG**；是移植排斥的原因。
- HLA-B27 與僵直性脊椎炎相關（但非確診依據）。

## 4. 各組織 MHC 表現
| 細胞 | MHC I | MHC II |
|---|---|---|
| T 細胞 | +++ | +（活化後） |
| B 細胞、DC | +++ | +++ |
| Macrophage | +++ | ++ |
| 胸腺上皮 | + | +++ |
| Neutrophil | +++ | − |
| 肝細胞、腎、腦 | + | −（microglia 例外） |
| **紅血球** | **−** | **−** |

## 5. 抗原處理與呈現 ⭐⭐

<div data-fig="pathogen-compartments"></div>

### MHC I 路徑（cytosolic / endogenous）
1. 細胞質蛋白（含 **DRiPs**）經 **ubiquitin–proteasome** 切成短 peptide（IFN-γ 誘導 immunoproteasome：**LMP2、LMP7**）。
2. **TAP-1 / TAP-2**（ER 膜上的 **ATP-dependent** 運輸蛋白；偏好 8–16 aa、C 端疏水或鹼性；基因在 MHC 區、受 IFN 誘導）送入 ER。
3. ER 內：**calnexin** 先結合 α 鏈 → β2m 結合後形成 **peptide-loading complex（calreticulin、tapasin、ERp57、TAP）** → **ERAAP** 修剪過長 peptide → 裝載上 MHC I。
4. 經 Golgi 運至細胞膜 → CD8 T 細胞辨識。

### MHC II 路徑（endocytic / exogenous）
1. 外源蛋白經 endocytosis / phagocytosis → endosome **酸化**、protease（cathepsins）切割。
2. MHC II 在 ER 與 **invariant chain（Ii）** 結合（防止在 ER 裝載內源 peptide、導向 endosome）。
3. 在 late endosome（**MIIC**）Ii 被切到剩 **CLIP** 佔住結合槽。
4. **HLA-DM** 催化 CLIP 離開、換上抗原 peptide；**HLA-DO** 抑制 HLA-DM。

<div data-fig="clip-hla-dm"></div>

5. 表現於細胞膜 → CD4 T 細胞辨識。

<div data-fig="mhc-pathways"></div>

### 例外路徑
- **Cross-presentation**：**DC** 把外源抗原放上 **MHC I**（活化 CD8）。
- **Autophagy**：細胞質抗原進入 MHC II 路徑。

## 6. 免疫突觸（下週詳述）
- Signal 1：TCR–pMHC（CD4/CD8 帶 **Lck**）；Signal 2：**CD28–B7（CD80/86）**；Signal 3：cytokines（IL-1、IL-6、IL-12）。
- 周邊：**LFA-1–ICAM-1** 黏附。

=== slides ===
# W4-1 上課 slides 重點：MHC and its function ＋ Antigen presentation（陳玫潔）

**Part 1 – MHC**（關鍵四主題：genes、generation & structure、peptides bound、MHC restriction）
- 1996 Nobel：Doherty & Zinkernagel、**dual recognition model**（LCMV 實驗）。
- What do T lymphocytes recognize?（peptides / APCs / self MHC / Ag-specific TCR）。
- 1980 Nobel：Ir genes、HLA、H-2。
- Primary structure（Fig 4.21b、4.22b）；Structural organization（**class I：α 45 kDa + β2m 12 kDa、8–9 residues、endogenous、CD8**；**class II：α/β、12 to >20 aa、exogenous、CD4**）。
- Genetic organization（Fig 6.16、6.17）：class III 含 factor B、LT-α。
- **MHC polymorphisms**：polygeny、co-dominant、allelic、haplotype（linkage）、**inherited differences**（vs TCR/BCR somatic）。
- Fig 6.19 polymorphism & polygeny；Fig 6.20 gene conversion；Fig 6.18 inherited differences；Fig 4.34 tissue expression。
- MHC restriction（Fig 6.23）；Ab / TCR 變異區為 somatic（not inherited）vs MHC 胜肽槽 inherited。

**Part 2 – Antigen presentation**（三主題）
1. Cytosol peptides → **TAP** → ER → MHC I（ubiquitin–proteasome；TAP-1/TAP-2；Fig 6.5、6.7、6.8）
2. Peptide:MHC II 在 **acidified endocytic vesicles** 產生（endocytosis、phagocytosis、autophagy；Fig 6.10）；**invariant chain、HLA-DM、HLA-DO、CLIP、MIIC**（Fig 6.11–6.13）
3. Peptide in groove：class I shorter / ends buried / H-bonds at ends；class II longer / extend / H-bonds throughout（Fig 4.21–4.23）
- Fig 6.1–6.4：兩大胞內區室、endogenous vs exogenous、**cross-presentation by DC**、**autophagy → MHC II**。
- Immunological synapse：adhesion molecules + TCRs。

=== exam ===
# 考點分析

## 🔥 高頻考點
1. **MHC I 表現**：所有有核細胞；**紅血球沒有**（出現 4 次）；「只在 DC 等 APC 表現」是錯的。
2. **MHC I 路徑**：peptide 經 **TAP（ATP-dependent）** 進 ER；在 **ER** 與 MHC I 結合；8–10 aa → CD8。
3. **DC 可同時用 MHC I 與 MHC II 呈現**（cross-presentation）。
4. **MHC polymorphism vs 抗體/TCR 多樣性**：「個體之間 vs 個體之內」（111 考古 75 題）。
5. **CD4 ↔ MHC II、CD8 ↔ MHC I**（4×2 = 8×1）。
6. **MHC II 基因產物位於 macrophage、DC、B 細胞**。

## ⚠️ 陷阱
- 「MHC class I deficiency 會難以對抗細菌」→ 主要影響病毒 / 胞內病原（考古答案為錯）。
- 「MHC I 比 MHC II 更多形性」→ 正確（別選錯）。
- β2-microglobulin 不是 MHC 基因編碼。
- HLA-DM 是「幫忙」換 peptide；HLA-DO 是抑制。

## 📝 出題模式
- 表格比較型（I vs II）最常見；今年 slides 大量引用 Janeway 圖（invariant chain、HLA-DM、cross-presentation）→ 可能出機制順序題。
