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
