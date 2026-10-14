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

## 🎙️ 上課錄影重點（陳玫潔，非同步遠距 W17；錄影無官方逐字稿，以 Whisper 轉錄整理）
- 本課 = 「**大亨堡怎麼做**」：Part 1 麵包（MHC）怎麼做、Part 2 熱狗（peptide）怎麼切、怎麼放上去。**專一性在 TCR**，MHC 與 peptide 的結合**不太需要專一性**（麵包不用切成熱狗形狀），但若 peptide 放不穩 → 無法被 TCR 辨識 → 喪失細胞免疫 → 「B 細胞免疫再好也無用」（T 細胞要幫 B）。
- 胸腺發育：DN（CD4⁻CD8⁻）→ **DP** → 依當初與胸腺細胞作用的是 MHC II 或 MHC I → **SP**（CD4 或 CD8）→ 出胸腺。TCR 認不得自己 MHC 的 T 細胞「死路一條」；認得自己 MHC **又認得自己 peptide** 的也不能放出去（之後會攻擊自己）。
- **Dual recognition（1996 諾貝爾）兩個例子**：① 兩位同學同時得 X 病毒，把一位的 T 細胞 transfer 給另一位 → peptide 相同但 MHC 不同 → **不能辨識**；② 同一人先得 X 再得 Y → 同 MHC 但 peptide 不同 → X 誘發的 T 細胞**不能**認 Y。所以「之前打過別的疫苗、這次流感就不用打」匪夷所思。
- TCR 的結合位：**認 peptide 的部分在正中間（變異最多處）**，認 MHC 的在周圍。
- 1980 諾貝爾：Benacerraf 找到 **Ir（immune response）gene**；Dausset 找到人類 **HLA**；Snell 在小鼠移植排斥實驗找到 **H-2**。人 = HLA、老鼠 = H-2。老師：「**恭喜各位，我不會考老鼠的**」。
- **結構（老師用手表演）**：MHC I = 一條 α 鏈（α1、α2、α3）+ **β2-microglobulin（不是 MHC 基因，但沒有它會免疫缺失）**；peptide 夾在 **α1 + α2** 之間，**CD8 接 α3**。MHC II = α + β 兩個基因產物（各兩個 domain）；peptide 夾在 **α1 + β1**，**CD4 接 β2**（課堂投票只有少數人答對）。結合槽：上方 **α-helix** 夾住熱狗、底部 **β-sheet**。
- MHC I peptide **8–9（8–10）aa、兩端 buried 在 pocket**；MHC II 可延伸、長度多變（13–18）。
- **Peptide 來源決定放到哪個 MHC**：endogenous（細胞自己 de novo 轉譯，如病毒利用宿主機器）→ MHC I；exogenous（吞噬、B 細胞 BCR 結合後 internalize、DC 攝入）→ 經胞器 protease → MHC II。
- **基因**：Class I = **HLA-A、-B、-C**（三個基因都會做 class I → **polygeny**）；Class II **不是 HLA-D**，而是 **DP、DQ、DR**（「不是我取的名字，你們也只能背」），其中 A 基因做 α 鏈、B 基因做 β 鏈；⚠️ **HLA-B 做的是 class I 的 α 鏈**（不是 β 鏈）。附近還有 TAP、DM、DO 等與 processing / 運送有關的基因。**Class III 不是 MHC**（TNF、補體）→「自動忽略」。基因圖譜「**絕對不會考**」。
- **Polymorphism**：multiple loci 全部表現、**沒有選擇性**；**allelic polymorphism** = 同一 locus 有個人差異；**haplotype（linkage）polymorphism** = A、B、C 的特定組合（命名號碼「萬萬不要去記」）。MHC 多樣性「**完全是拜祖上所賜，遺傳來的**」，不是像抗體那樣 rearrangement；最早從**多產婦**身上發現（胎兒帶父親的 MHC，對母親是「外星人」→ 懷孕時免疫被抑制）。
- **Co-dominant expression**：父母的 HLA 全部表現（手心手背都是肉）→ 準備越多越可能夾得住未來的抗原；但仍可能「沒有一個麵包夾得住」→ 有人分析家族 HLA 與疾病（如 COVID-19 重症）易感性的關係。
- **Gene conversion**（減數分裂時相似區域重組）→ 產生新種類 → 所以**兄弟姊妹 HLA 仍可能不同**，器官移植還是要配對。β 鏈的變異種類通常比 α 多。
- **組織分布（「這張圖小重要」）**：所有有核細胞（**RBC 除外**）表現 MHC I；只有 **B、macrophage、DC、胸腺上皮**多表現 MHC II → 只有它們能活化 CD4。
- **Allelic exclusion**：抗體與 TCR 一個 allele 重組成功就關掉另一個（確保**單一專一性**）；失敗會先嘗試修補，真的不行才換另一個 allele。**MHC 沒有 allelic exclusion、也不重組**，遺傳到什麼就表現什麼（百花齊放）。
- **MHC I 路徑**：cytosol 中蛋白經 **ubiquitin → proteasome**（免疫相關的 **immunoproteasome** 換掉部分 subunit；cytokine 使其 α-helix 開口打開）切碎 → **TAP1 / TAP2（需 ATP）** 送進 ER（TAP 基因就在 MHC 區）→ 進 ER 後還會再修剪 → MHC I 先在 **calnexin** 協助下與 β2m 組合，再換其他 chaperone；**tapasin** 把 MHC I 綁在 TAP 旁「就地結合」→ 結合不穩會被吐出、換別的 MHC 試 → 穩定者送到細胞表面 → **CD8**。
- 活化 CD8 的是**次級淋巴組織中的 APC**；effector CD8 才到周邊找被感染的細胞（「金正恩不會沒事出來巡視民間疾苦」）。
- **MHC II 路徑**：H⁺ pump 酸化 → 酶原變活化 protease → 切碎外來蛋白；MHC II 在 ER 被 **invariant chain（trimer，像章魚）** 塞住 → 運送途中被切到只剩 **CLIP**（紅酒塞）→ 與含 peptide 的囊泡融合成 **MIIC**（late endosome，電顯下像**洋蔥橫切面**；用不同大小金珠標定抗體觀察）→ **HLA-DM 改變構形讓 CLIP 離開**、peptide 補上；**HLA-DO 抑制 DM** → 缺 DM 則 CLIP 卡住 → 免疫缺失。
- **Neutrophil 吞完只把殘渣 exocytosis 丟出**；macrophage 會把殘渣放上 MHC II 帶回給「將軍」TH。
- **B 細胞**：BCR 抓下來的不一定是蛋白質 → 若是非蛋白抗原就**無法活化 T 細胞** → 沒有 T 幫忙就**不能 affinity maturation、不能 class switch**（V(D)J 重組不需 cytokine，但 class switch 需要 T 細胞的 cytokine）→ 永遠只有 **IgM**。IgM 是「**掃地機器人**」：pentamer 有 **10 個 binding site**，總結合力遠大於 10 倍 → 早期把病原困住、活化補體。
- **Cross-presentation（cross-priming）只有 DC 能做**：外來抗原也能放上 MHC I → **同時活化 CD4 與 CD8**；機制至今沒有定論（從囊泡吐到 cytosol？或空的 MHC I 送進囊泡？）。**Autophagy** 是例外：自己的蛋白包進 autophagosome → 走 **MHC II**。
- **Peptide 結合**：只有 T epitope 能寫胺基酸序列（「若有人說抗體認某段連續序列，要露出非常吃驚的表情」）。MHC I 的氫鍵在**兩端**、anchor residue 在兩端（常疏水）；MHC II 兩端開放、氫鍵**分布在中間整段**；**全部是非共價鍵**（所以有 Kd，會結合又解離）；只有少數 anchor 位置重要，其他都可以差很多。
- 預告下堂：TCR = **白雪公主**（負責專一辨識）、**CD3 = 六個小矮人**（負責傳訊息；TCR 與 CD3 以**正負電、非共價**結合；CD4 與 CD8 T 細胞的 CD3 一樣）；**免疫突觸**：先靠周邊黏附因子穩住兩個細胞，TCR 在正中間；**訊號 1 = TCR、訊號 2 = CD28–B7.1/B7.2（與 checkpoint blockade 有關）、訊號 3 = cytokine**。

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

## 🎙️ 老師課堂提示
- 老師明講**不考**：老鼠 H-2 的基因、MHC 基因圖譜距離、haplotype 號碼；Class III 自動忽略。
- 錄影中強調：**CD8 接 α3、CD4 接 β2**；class II 是 **DP、DQ、DR**（不是 HLA-D）；MHC 多樣性是**遺傳**來的、**沒有重組、沒有 allelic exclusion**；兄弟姊妹因 gene conversion 仍可能 HLA 不同。
- 「這張圖小重要」：MHC I 在所有有核細胞（RBC 除外）；MHC II 只在 B、macrophage、DC、胸腺上皮。
- **Cross-presentation 只有 DC**；autophagy 走 MHC II；非蛋白抗原無法活化 T → 只有 IgM、無 class switch。
