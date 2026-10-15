=== summary ===
# 抗原、抗體與抗體多樣性（李岳倫）

## 1. 抗原
- 定義：能被 **B 細胞的 Ig receptor 或 T 細胞的 TCR** 辨識的物質。
- 類型：exogenous（多數，吸入 / 食入 / 注射 / 傷口）、endogenous（病毒顆粒）、autoantigen。
- 抗體可辨識 **linear（continuous）或 conformational（discontinuous）** epitope；TCR 只辨識 **linear peptide + MHC**。

| | B 細胞 | T 細胞 |
|---|---|---|
| 辨識 | 膜上 Ig 直接結合 Ag | TCR 辨識 MHC 上的 peptide |
| 與可溶性抗原結合 | ✅ | ❌ |
| 需 MHC | ❌ | ✅ |
| 抗原種類 | 蛋白、多醣、脂質 | 幾乎只有 peptide |
| Epitope | **親水**、連續或不連續 | 連續線性 |

<div data-fig="epitopes"></div>

## 2. 抗體基本結構
- **醣蛋白**；2 條 heavy + 2 條 light，**雙硫鍵**連接，排列為 **L–H–H–L**（不是 L-H-L-H）。
- Light chain：**κ 或 λ（一個抗體只有一種）**；由 **V、J、C** 片段編碼（**沒有 D**）。
- Heavy chain：**V、D、J、C**；重鏈種類 γ、α、μ、ε、δ **決定 class 與 subclass**。
- V domain（VL、VH）結合抗原；**CDR（hypervariable）** 形成結合位，**CDR3 變異最大**。
- **Hinge region**：CH1–CH2 間，富含 proline，提供彈性（IgG、IgA、IgD 有）；**IgM、IgE 無 hinge**（4 個 CH）。

<div data-fig="ig-domains"></div>

- 木瓜酶切：**Fab**（結合抗原）、**Fc**（結合 FcR、補體）。
- 功能：**Complement activation（IgM、IgG）**、**Opsonization（IgG–FcγR）**、**Neutralization（Fab）**。

<div data-fig="ab-functions"></div>

## 3. 五種抗體 ⭐⭐

| | IgG | IgM | IgA | IgD | IgE |
|---|---|---|---|---|---|
| 結構 | monomer | **pentamer + J chain**（膜上為 monomer） | 血中 monomer（80%）；分泌為 **dimer + J chain + secretory component** | monomer | monomer |
| 佔 Ig pool | **70–75%**（最多） | ~10% | 15–20% | <1% | 極少 |
| 特點 | **次級反應主力**；**唯一通過胎盤**（所有 subclass）；血管內外均勻 | **初級反應主力**；**最強補體活化**；侷限血管內；感染指標（current infection） | **黏液分泌物主力**（seromucous）：IgA1 鼻涕、淚、唾液、乳汁；IgA2 結腸 | **B 細胞膜上受體**（與 IgM 共表現），功能不明 | **寄生蟲、過敏**；經 **FcεRI** 結合 mast cell / basophil |
| 活化補體 | ✅（IgG1–3） | ✅✅ | ❌ | ❌ | ❌ |
| Hinge | ✅ | ❌ | ✅ | ✅ | ❌ |

<div data-fig="ig-classes"></div>

- IgG subclass 比例：IgG1 66%、IgG2 23%、IgG3 7%、IgG4 4%。
- **Secretory component 由上皮細胞合成**：dimeric IgA 結合 **poly-Ig receptor** → transcytosis → 受體切下殘留 = secretory component（保護不被 protease 分解、協助運送）。

<div data-fig="iga-transport"></div>

- 血清 IgA1:IgA2 ≈ 10:1；腸道 IgA2 比例顯著增加。
- **TGF-β 促進 IgA class switch**（不是 IL-12）。
- 新生兒保護：**IgG（胎盤）+ IgA（母乳）**。
- 疫苗第二劑後快速出現的是 **IgG**（memory B）；初次反應第 5 天還不會有大量 IgM。

## 4. B 細胞發育中的抗體表現
- 胚胎期在肝、出生後在**骨髓**（V(D)J 重組發生地）。
- Pro-B → Pre-B：**重鏈先重組（μ）**；Pre-B → immature B：輕鏈重組，**κ 先、失敗才 λ**（μ → κ → λ）；成功後抑制另一個 → **allelic exclusion**。
- Immature B：膜上 IgM；Mature B：**IgM + IgD** → 至周邊 → 抗原刺激 → plasma cell（分泌型）或 memory B；可 class switch。
- **Somatic hypermutation 發生在 mature B 被抗原活化之後**（germinal center），其他多樣性機制在骨髓發育時。

## 5. 抗體多樣性六大機制 ⭐⭐
1. **Multiple germline V genes**
2. **V-J（輕鏈）與 V-D-J（重鏈）recombination**：重鏈**先 D-J，再 V-DJ**
3. **Assorted heavy & light chain**（κ、λ 可能數要「相加」再乘重鏈）
4. **Gene conversion**（人類沒有；雞用 pseudogene 置換 V）
5. **Junctional diversity**
6. **Somatic point mutation（hypermutation）** → affinity maturation

> ❌ **Gene cross-over 不是**抗體多樣性機制。

<div data-fig="vdj"></div>

### Junctional diversity 的分子
| 分子 | 功能 |
|---|---|
| **RSS**（heptamer–12/23 spacer–nonamer） | 重組訊號，**12/23 rule** |
| **RAG-1 / RAG-2** | 辨識 RSS、切斷 DNA、形成 **hairpin** |
| **Artemis（DNA-PK）** | **打開 hairpin → P-nucleotides（回文）** |
| **TdT** | **不需模板**隨機加入 **N-nucleotides**（不是「辨識 / 標記 DNA 斷點」） |
| Exonuclease | 移除未配對鹼基 |
| **DNA ligase IV** | 接合 |

- 加入核苷酸數非 3 的倍數或產生 stop codon → B 細胞無功能而死亡。
- Somatic hypermutation：抗原刺激後約第 6 天開始點突變；第 8–16 天 affinity maturation，壞突變的 B 細胞凋亡、高親和力者擴增。**只有 B 細胞**有（T 細胞沒有）。

## 🎙️ 上課錄影重點（李岳倫，09/23）
- 老師定調：Part 1–2（抗原、五種抗體）「輕鬆上」；**Part 3 多樣性六大機制最複雜**，「國考一定會考」。
- **B vs T 認抗原**：B「大而化之、有容乃大」——直接以 BCR 結合、**可認水溶性抗原**、不需 MHC、可認蛋白 / 多醣 / 脂質、epitope **親水**、可連續或不連續（立體）；T「比較挑剔」——需 MHC 呈現、**不認水溶性抗原**、多為蛋白、只認**線性連續** peptide。
- **抗體三大功能**：**中和、調理、活化補體**。⚠️ 別和**補體三大功能（溶解、趨化、調理）**搞混。中和例：抗體結合外毒素 → 毒素無法結合細胞受體 → 再被吞噬細胞經 Fc receptor 清除。
- Light chain = κ 或 λ；hinge region 讓抗體可以「歪頭、彎身體」抓抗原（flexibility）。國考考過：**抗體認抗原的位置 = V domain**。
- **抗體命名（IgM、IgG3…）由 heavy chain 的 C 基因決定**：Cμ → μ chain → IgM；Cδ → IgD；Cγ3 → IgG3。⚠️ 基因上的 V（V、D、J 片段）和蛋白質上的 V domain 不要搞混。
- **B 細胞發育（國考考過，要熟圖）**：成人在 **bone marrow**、胎兒在 **liver**；pre-B 先重組 **heavy chain（μ）** → immature B 再重組 light chain → 表面 **mIgM** → mature B 經 **RNA splicing** 同時表現 **mIgM + mIgD** → 遇抗原活化，在次級淋巴器官（如脾）分化成分泌 IgM 的 plasma cell → **class switching** → IgG / IgA / IgE；plasma cell 壽命短，一部分變 memory B。課堂題：V region recombination 發生在 bone marrow。
- **IgM**：pentamer（J chain = Fc-linking polypeptide）；Cμ 有 4 個 → **沒有 hinge**；約占 **10%**；初次反應主角；太大不易出血管 → **80% 在血管內**；classical pathway activator。
- **IgD**：老師說「**我考試從來沒有考過 IgD**」；分泌型 < 1%，主要是膜型；有 hinge。
- **IgG（國考常考）**：Fab（含 V domain、結合抗原）vs Fc（吞噬細胞 FcR 抓的地方；**補體抓抗體也是抓 Fc**，考過）；占 **70–75%**，IgG1 最多；二次反應主角；血管內外**各半**；活化 classical pathway；**唯一能通過胎盤** → 新生兒帶有母親 IgG（被動免疫）。
- **IgA**：dimer 靠 J chain；**secretory component** 由上皮細胞製造：dimer IgA 被上皮的 **poly-Ig receptor** 抓住 → endocytosis → 運到對側時受體裂解，留下的片段黏在 IgA 上 → **保護 IgA 不被口腔、腸道蛋白酶分解**。占 15–20%；人類分泌型 IgA **80% 是 monomer**（多數哺乳類以 dimer 為主）；**IgA1** 在鼻液、淚液、唾液、母乳、血清；**IgA2** 在腸道。課堂題：促進 class switch 到 IgA 的 cytokine = **TGF-β**；IgA–Ag complex **不會**啟動 classical pathway（IgG、IgM 才會）。
- **IgE**：Cε 有 4 個 → **沒有 hinge**（與 IgM 同）；健康人血中幾乎測不到，只有**寄生蟲感染**或**過敏體質**才產生；結合 basophil / mast cell 上的 **FcεRI** → 再次接觸過敏原 **cross-link** 相鄰 IgE → **degranulation**（histamine、leukotrienes、prostaglandin）→ 過敏反應。
- 摘要：含量最高 IgG、最低 IgE；分子量最大 IgM、其次 dimer IgA。
- **多樣性的邏輯**：每株 B 細胞在遇到抗原**之前**就已做好各自不同的受體（「亂槍打鳥」），抗原進來再挑出能結合的那一株活化、增殖。
- κ chain 例：V 約 76 個、J 5 個 → 76 × 5 種組合；重組後轉錄、**RNA splicing** 剪掉多餘片段 → V2J4 + C。數字不用記（常更新）。
- **Heavy chain 重組有次序：先 D–J，再 V–DJ**（V 87、D 30、J 6）。課堂題：抗體基因重組的**最開始步驟 = heavy chain 的 D–J**。
- 表現順序 **μ → κ → λ**（κ 失敗才啟動 λ）；**allelic exclusion** 老師請共筆同學補充。小鼠計算例：heavy 134 × 13 × 4 = 6968；κ 85 × 4 = 340；λ 2 × 3 = 6 → 6968 × (340 + 6) ≈ **2.4 × 10⁶**。
- **Gene conversion 人類沒有**：雞、牛、豬、羊只有一個 V、一個 J → 用前方 **pseudogene** 片段插入置換。
- **Junctional diversity 酵素流程**：**RAG1/RAG2** 認 **RSS**（位於 intron）、切斷並形成 **DNA hairpin** → **Artemis + DNA-PK** 打開 hairpin → 產生對稱（palindromic）單股 = **P nucleotides** → **TdT** 不需模板隨機加入 **N nucleotides**（可多達 15–20 個）→ 配對 → **exonuclease** 切除未配對者 → DNA 合成 + **DNA ligase IV** 補起來。加入數非 3 的倍數 → frameshift → 失敗（一百顆可能只有一顆成功也沒關係）。老師：「你以為這麼複雜國考不會考？**國考考了**」。
- 機制 1–5 發生在 **B 細胞發育過程**；機制 6 **somatic point mutation** 在**成熟 B 遇到抗原後**才發生（約 6 天內陸續突變；第 8–16 天壞突變者死亡 = negative selection / **affinity maturation**）。課堂題：會進行 somatic hypermutation 的是 **B 細胞**；多樣性機制「不包括」**gene crossover**（是 conversion）。

=== slides ===
# W3-1 上課 slides 重點：Antigen and Antibody / Antibody diversity（Ch 4, 5, 8, 10，李岳倫）

- 學習目標：(1) 抗原抗體定義與特性 (2) 各種抗體構造與功能 (3) 抗體多樣性機制。
- Antigen 定義（Kuby）；continuous vs discontinuous epitope；TCR binds linear peptide + MHC。
- **課堂題 1**：可活化 B 細胞的抗原特性「不包括」→ **需要 MHC 參與**。
- Antibodies are glycoproteins：(1) 膜上受體 (2) 循環抗體三功能 (3) 五類（IgG1–4、IgA1–2）。
- Four-chain model、hinge region（flexibility）；**class & subclass determined by heavy chain**。
- B-cell development overview；**課堂題 2**：V 區重組在**骨髓**。
- IgM（pentamer、J chain added just before secretion、10%、primary response、intravascular、classical pathway activator）。
- IgD（<1%、membrane、function unclear）。
- IgG（70–75%、66/23/7/4%、2nd response、even distribution、classical pathway、**all subclasses cross placenta**）。
- IgA（dimer、secretory component by epithelial cells、15–20%、80% monomer in human、IgA1 vs IgA2）；**課堂題 3**：正確為 (C) 分泌片段由上皮細胞合成（A 比例不一致、B 應為 TGF-β、D 應為 IgG/IgM）。
- IgE（scarce、FcεRI on basophils / mast cells、parasites & allergy）。
- Physicochemical properties & functions table。
- 六大多樣性機制；κ chain（35 functional genes）、heavy chain（50 functional V、D-J → V-DJ）；**課堂題 4**：基因重組起始步驟 = **重鏈 D-J**。
- Assorted chains、gene conversion（chicken）、junctional diversity（RSS/RAG → DNA-PK/Artemis → P-nt → TdT N-nt）；**課堂題 5**：錯誤為 **TdT「可標記 DNA 斷裂點」**。
- Somatic hypermutation & affinity maturation；**課堂題 6**：B 細胞；**課堂題 7**：不包括 **gene cross-over**。

=== exam ===
# 考點分析

## 🔥 高頻考點
1. **IgA**：黏液 / 唾液 / 淚液、抑制流感入侵呼吸道、secretory component 由上皮製造、poly-Ig receptor（出 6+ 次）。
2. **IgE**：過敏、氣喘、寄生蟲、FcεRI（5+ 次）。
3. **IgM**：pentamer、J chain、初次反應、current infection、最佳補體活化者、IgM 不是 dimer。
4. **IgG**：唯一過胎盤、次級反應、血清最多、活化補體。
5. **多樣性機制**：「不包括」gene cross-over；CDR3 變異最大；somatic mutation 在成熟 B 被活化時。
6. **Allelic exclusion 順序 μ → κ → λ**；κ 成功則抑制 λ。
7. **Class / subclass 由 heavy chain 決定**（不是 light chain）。
8. **J chain：IgM 與 IgA**。

## ⚠️ 陷阱
- Light chain 由 V、J、C 組成（「V、D、J」是錯的）。
- 抗體排列是 L-H-H-L。
- IgM **沒有** hinge region（正確敘述）；IgD 有。
- 「在腸胃道黏膜含量最高是 IgE」→ 錯（IgA）；「IgM 可穿胎盤」→ 錯。
- 院內感染腸胃炎診斷看 **IgG 效價上升 4 倍**。

## 📝 出題模式
- 大量中文單選（國考風格）：「下列何種抗體…」。每年都會重複 IgA / IgE / IgG 的情境題。
- 李岳倫 slides 課堂題 7 題，需熟練。

## 🎙️ 老師課堂提示
- 老師說「**IgD 我考試從來沒有考過**」；「六大多樣性機制一定要記，國考一定會考」；V(D)J 酵素功能（RAG、Artemis/DNA-PK、TdT、ligase IV）國考考過。
- 國考考過：抗體認抗原的位置 = V domain；補體結合抗體的位置 = **Fc**；B 細胞發育中的抗體表現順序（μ 先、mIgM → mIgM + mIgD）。
- 錄影中的課堂題：B 細胞抗原特性「不包括」需 MHC；V region 重組在 bone marrow；IgA 敘述何者正確（secretory component 由上皮製造；**TGF-β** 促 IgA；IgA1 / IgA2 在血清與腸道比例不是 1:1）；最先的重組步驟 = heavy chain D–J；somatic hypermutation 只有 B 細胞。
- 易混：抗體三功能（中和、調理、活化補體）vs 補體三功能（溶解、趨化、調理）；沒有 hinge 的是 **IgM、IgE**。

## 📒 115 共筆對照（W03-1）
- **IgD：老師說不會考。**
- 老師強調：**secretory component 是上皮細胞做的**，不是 B cell／plasma cell。
- 促進 IgA class switching 的關鍵 cytokine 是 **TGF-β**。
- **IgG 是唯一能通過胎盤的抗體**（四個 subclass 都可以；國考常考）。
- 算抗體多樣性時：**κ 與 λ 的可能數要相加、不是相乘**；注意 V gene 與 V domain 是不同層級。
