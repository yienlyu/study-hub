=== summary ===
# 先天免疫（李岳倫）

> 老師標註 **\* IMPORTANT !** 的是補體三路徑。學習目標：① 細胞遷移與補體 ② 單核吞噬細胞 ③ NK 細胞毒殺。

## 1. 發炎
- 急性發炎：血流↑、微血管通透性↑、白血球聚集（**neutrophil 先到 → monocyte**）；mast cell 為組織常駐、早期活化。
- 慢性發炎：病原未清除 → macrophage、CTL、甚至 B 細胞浸潤。

## 2. 白血球遷移：Three-step model ⭐
| 步驟 | 名稱 | 分子 | 作用 |
|---|---|---|---|
| 1 | **Tethering**（滾動） | **Selectin**（內皮）↔ 白血球醣蛋白上的**醣類** | 減速 |
| 2 | **Triggering**（活化） | **Chemokine** ↔ chemokine receptor | 活化特定白血球 |
| 3 | **Latching**（緊密黏附） | **Integrin**（白血球，α+β 非共價）↔ **ICAM / VCAM**（Ig superfamily） | 停止、穿出血管 |

> 口訣：**S → C → I**（Selectin → Chemokine → Integrin）；考古「(c)(a)(b)」。

- Selectin：**P-selectin**（血小板、內皮）、**E-selectin**（內皮）、**L-selectin**（白血球，結合 HEV）；selectin 是單一鏈（**α、β 兩條是 integrin**）。
- Integrin 例：**LFA-1**（↔ ICAM-1）、**VLA-4**（↔ VCAM-1）、**CR3、CR4**（也是補體受體）。**CCR3 不是 integrin**（chemokine receptor，7 次跨膜 GPCR）。
- Chemokine receptor：**CCR3**（TH2、eosinophil ↔ **eotaxin**）；**CCR5**（TH1、macrophage ↔ MIP-1β）。
- MAdCAM：mucosal addressin。

<div data-fig="extravasation"></div>

## 3. 補體系統 ⭐⭐⭐
- 肝臟製造、30 多種可溶性蛋白、平時不活化、cascade 切割活化。

### 三大功能
| 功能 | 片段 |
|---|---|
| **Opsonization 調理** | **C3b**、C4b（iC3b）→ 被吞噬細胞 **CR** 辨識 |
| **Chemotaxis / 發炎** | **C3a、C5a**（小分子易擴散，C3aR / C5aR；anaphylatoxin） |
| **Lysis 溶解** | **MAC = C5b + C6 + C7 + C8 + 多個 C9** |

<div data-fig="complement-functions"></div>

> ⚠️ **Neutralization 是抗體的功能**，不是補體。C2a 是酵素片段、不是發炎介質。

### 三條路徑
| | Classical | Lectin | Alternative |
|---|---|---|---|
| 啟動 | **C1q** 結合 Ag 或 **Ag-Ab（IgM、IgG1–3）** | **MBL** 結合病原表面 **mannose/fucose**；ficolin 結合 acetylated sugars | C3b 結合病原表面（或 C3 自發水解 C3(H₂O)） |
| 酵素 | **C1qr₂s₂** | **MASP-1、MASP-2**（MASP-3） | **Factor B、Factor D** |
| 切割 | C4 → C4a + **C4b**；C2 → **C2a**（酵素）+ C2b | 同 classical | C3b + B → C3bB →（D 切）→ **C3bBb** |
| **C3 convertase** | **C4b2a** | **C4b2a** | **C3bBb**（C3(H₂O)Bb 短命） |
| C5 convertase | C4b2a3b | C4b2a3b | C3bBb3b |

- **三路徑第一會合點 = C3 convertase**（C3 是共同成分）；第二會合點 = C5 convertase。
- **MBL ≈ C1q**（功能相似）→ lectin 與 **classical** 機制較像（**不是** alternative）；MBL 是 **acute phase protein**、只接病原（不接宿主）。
- **Alternative pathway 是 positive feedback loop**（C3bBb 再切 C3）；第一個被活化的蛋白是 **C3**（C4 只出現在 classical/lectin）。
- 老師講法：alternative 的穩定啟動**依賴 classical/lectin 先產生 C3b**（所以考古選「alternative pathway is NOT linked to classical」為錯誤敘述）；但它本身**不需要抗體**。

<div data-fig="complement"></div>

## 4. 單核吞噬細胞與 Opsonic receptors ⭐
Macrophage：吞噬 → phagosome（酸化、H₂O₂、NO、TNF-α）→ 與 lysosome 融合 → phagolysosome → 部分 peptide 上 MHC II。

**四種 opsonic receptors**
1. **Mannose receptor**（C-type lectin domains，辨識 mannosylated ligand）
2. **Fc receptor**（FcγRI、II、III 抓 IgG；FcγR on monocyte/neutrophil）
3. **Complement receptor**（CR1–4；CR3、CR4 也是 integrin；CR2 不在吞噬細胞上）
4. **CD14 + TLR4**（LPS → **LPS-binding protein → CD14 → TLR4**）

> 不是 opsonic receptor：KIR（NK）、MHC II、CD94、selectin、TCR、CD15（正確是 CD14）。

<div data-fig="phagocytosis"></div>

**(1) Mannose receptor**：頭端 cysteine-rich domain；**8 個 C-type lectin domains** 才是認 mannose 的部分。

<div data-fig="mannose-receptor"></div>

**(2) Fc receptor**：抓 IgG 包住的病原。

| 受體 | CD | 細胞 |
|---|---|---|
| FcγRI | **CD64** | monocyte |
| FcγRIIa | **CD32** | monocyte / neutrophil |
| FcγRIIIa | **CD16** | monocyte |
| FcγRIIIb | **CD16**（**GPI anchor**） | neutrophil |

<div data-fig="fc-receptor"></div>

**(3) Complement receptor**

| 受體 | CD | 表現在 |
|---|---|---|
| CR1 | **CD35** | 吞噬細胞、紅血球、淋巴球 |
| CR2 | **CD21** | **B cell、FDC**（不在吞噬細胞上） |
| CR3 | **CD11b / CD18**（integrin） | 單核吞噬細胞、NK |
| CR4 | **CD11c / CD18**（integrin） | 單核吞噬細胞、NK |

<div data-fig="complement-receptor"></div>

**(4) CD14 + TLR4**：LPS → LPS-binding protein → CD14 → TLR4 → MyD88 → NF-κB。

<div data-fig="tlr4"></div>



### TLR 對照表
| TLR | 位置 | Ligand |
|---|---|---|
| TLR1:TLR2 | 細胞膜 | mycobacteria lipomannan、細菌 lipopeptides |
| TLR2:TLR6 | 細胞膜 | **G+ lipoteichoic acid**、真菌 β-glucan |
| **TLR3** | **endosome** | **病毒 dsRNA**、poly I:C |
| **TLR4** | 細胞膜 | **G− LPS（endotoxin）** |
| **TLR5** | 細胞膜 | **flagellin** |
| TLR7 / TLR8 | endosome | 病毒 **ssRNA** |
| **TLR9** | endosome | **unmethylated CpG DNA** |

## 5. 細胞性毒殺：Tc vs NK ⭐
| | Tc（CD8） | NK |
|---|---|---|
| 屬於 | adaptive | **innate**（源自 common lymphoid progenitor） |
| 辨識 | TCR 辨識 **MHC I + peptide**（抗原專一） | 無抗原專一；**抑制性受體辨識 MHC I** |
| 目標 | 呈現外來 peptide 的細胞 | **MHC I 表現下降**的細胞（病毒感染、腫瘤）＝ missing self |

- NK 活化受體：**CD2、CD16、CD69**。
- NK **抑制性受體**：
  - **CD94/NKG2A**（有 **ITIM**）↔ **HLA-E**（呈現其他 MHC I 的 leader peptide）；CD94/NKG2C 無 ITIM → 非抑制性。
  - **KIR-2D、KIR-3D（long tail，有 ITIM）** ↔ **HLA-C**；short tail 無 ITIM → 非抑制性。
  - ⚠️ HLA-E / HLA-C 是 **ligand**，不是 receptor。
- 紅血球**無 MHC I**（無核）。腫瘤逃避 CTL：**降低 MHC I**（但逃不過 NK）。

<div data-fig="tc-vs-nk"></div>

<div data-fig="nk-receptors"></div>

### 三種毒殺方式（Tc、NK 共通）
1. **Direct**：FasL ↔ **Fas（CD95）** → apoptosis
2. **Cytokines**：**TNF、lymphotoxin（LT）**
3. **Granules**：**perforin**（打洞）+ **granzymes**（誘發凋亡）

> ⚠️ **IFN-γ 與毒殺「沒有直接關聯」**（它是活化 macrophage）——考了兩次。

## 6. ILCs（先天性淋巴細胞）
| 類型 | 分泌 | 功能 |
|---|---|---|
| NK | perforin、IFN-γ | 胞內病原、腫瘤 |
| **ILC1** | **IFN-γ** | 病毒、**胞內**細菌（考古陷阱：寫成「胞外」即錯） |
| **ILC2** | **IL-4、IL-5、IL-13** | 寄生蟲、組織修復、**氣喘** |
| ILC3 | IL-17、IL-22 | 胞外細菌 |

- 無抗原專一性受體；轉錄因子 **Id2**。

## 🎙️ 上課錄影重點（李岳倫，09/18）
- 時間軸：innate 十幾個小時內就發生；adaptive（B 產抗體、T 分化成 effector）要 **5–7 天**。
- **白血球遷移三部曲**：白血球在大血管流很快，到**小靜脈**流速變慢 → ① **tethering**（selectin 抓住：E / P-selectin 在內皮，抓白血球上的醣類 ligand，如 neutrophil 的 **CD15**；L-selectin 在白血球、ligand 在內皮）→ ② **triggering**（內皮或受傷組織釋放 chemokine；**被抓住的細胞要有對應 chemokine receptor 才會反應**）→ ③ **latching**（integrin：**LFA-1、CR3** 結合 **ICAM-1** → 完全停下、從內皮縫隙鑽出）。順序 **selectin → chemokine → integrin**（課堂題答案 C）。
- Chemokine receptor 配對例：Th1 / macrophage 的 **CCR5 ↔ MIP-1β**；Th2 / eosinophil / basophil 的 **CCR3 ↔ eotaxin**；neutrophil 的 **CXCR1 / CXCR2 ↔ IL-8**、GRO。
- Integrin = α + β 鏈**非共價**結合；配體關係是**一對多**（LFA-1 認 ICAM-1/2/3；CR3 認 ICAM-1、**C3b、C4b**；ICAM-1 也被 LFA-1、CR3 認）→ 細胞交互作用不是一對一。
- **補體**：肝臟製造、**30 種以上**的血清蛋白。**三大功能「一定要知道」**：溶解（打洞）、趨化（像香水吸引吞噬細胞）、調理。
  - 調理素 = **C3b、C4b、iC3b**（吞噬細胞用 CR 抓住）；趨化 = **C3a、C5a**（片段很小、很快擴散）。
  - 「上面都是點心」，**重頭戲是第三個功能：三條路徑**。
- **Classical**：C1 = **C1q + 2 C1r + 2 C1s**；C1q 的頭（黃色球）認 antigen 或 **Ag–Ab complex（IgM、IgG1、G2、G3）** → C1r 互相活化 → 活化 C1s → 切 C4（得 C4b）→ C2 結合成 C4b2 → 切 C2 → **C4b2a = C3 convertase** → **C4b2a3b = C5 convertase** → C5b + C6–C9 = **MAC（C5b-9）**。
- **Lectin**：**MBL**（認 mannose / fucose）與 **ficolins**（認 oligosaccharide）+ **MASP-1/2/3**（protease）；結構像 C1q → 路徑**幾乎跟 classical 一樣**；差別只在活化者：lectin 只認 antigen、**antibody independent**。
- **Alternative** 兩種啟動：① 前兩路徑產生的 C4b2a 切出 C3b → factor B 結合 → **factor D 切 B** → **C3bBb**；② **C3 自發水解** → C3(H₂O) + Bb = **短命的 C3(H₂O)Bb**。所以 alternative 有**兩種 C3 convertase**；C5 convertase = **C3bBb3b**。
- 陷阱：問「**最初**匯合點」= C3 convertase；「第二個匯合點」= C5 convertase。老師建議把三路徑總整圖「印 A4 貼床頭」。
- **吞噬**：phagosome 酸化、釋放有毒物質與水解酶；碎片吐出或經 **MHC II** 呈現；同時產生 H₂O₂、NO、TNF-α。
- **Opsonic receptors**：mannose receptor（頭端 cysteine-rich、尾端 **8 個 C-type lectin domains** 才是認 mannose 的部分）；Fc receptor（FcγRI/II/III 認 IgG 的 Fc）；**CR1、CR3、CR4** 在吞噬細胞上，其中 **CR3、CR4 也是 integrin**（一個分子多功能）。
- **CD14 + TLR4「國考常常會考」**：LPS 先被 **LPS-binding protein** 抓住 → CD14 認 → 交給 TLR4。TLR 是家族（TLR8/9 認核酸、TLR5 認鞭毛）→ 老師建議自己用 Janeway 整理 TLR 表，國考不只考 TLR4。
- **NK 加總訊號**：activating receptor（ligand 如 CD2、CD16、CD69）vs inhibitory receptor（認 **MHC I**）；健康細胞 MHC I 滿滿 → 抑制 > 活化 → 不殺；感染細胞 MHC I↓ → 活化 > 抑制 → 殺。
- **正港的抑制性受體**：**CD94 + NKG2A**（有 **ITIM**，認 **HLA-E**）；CD94 + NKG2C 沒有 ITIM → 非抑制性。**長尾巴 KIR2D / KIR3D**（有 ITIM，認 **HLA-C**）才是抑制性；短尾巴不是。
- NK / Tc 毒殺三方式：**FasL–Fas（CD95）**（肉搏戰）、**TNF、lymphotoxin**（毒氣）、**perforin（需 Ca²⁺，先打洞）+ granzyme（再丟進去）**（子彈）→ apoptosis。
- **ILC**（老師給的 homework）：NK 與 ILC1 相似 → 病毒、**胞內**病原；ILC2 → 寄生蟲、**IL-4、IL-5、IL-13 參與過敏氣喘**；ILC3 → 胞外細菌。**ILC 沒有專一性受體**。老師說這題「**我曾經考過**」。

=== slides ===
# W2-2 上課 slides 重點：Innate Immunity（Ch 2, 3，李岳倫）

- 學習目標（p.2）：(1) Cell migration & complement (2) Mononuclear phagocytes (3) Cell-mediated cytotoxicity – NK。
- **Three-step model**（Roitt 6E）：Step 1 selectins ↔ carbohydrates；Step 2 chemokines trigger；Step 3 integrins ↔ CAMs（VLA / VCAM / LFA / ICAM / MAdCAM；Ig supergene family）。
- Complement functions：opsonization（C3b、C4b）、chemotaxis（**C3a、C5a，small & diffuse，C3aR / C5aR**）、lysis。
- **\* IMPORTANT !** Classical（Ag or Ag-Ab (IgM, IgG1-3) → C1qr₂s₂）、Lectin（MBL、ficolins；**MASP-1, -2, -3**）、Alternative（two ways：by lectin/classical → C3bBb；spontaneous → **C3(H₂O)Bb short-lived**）；MAC。
- Opsonic receptors：mannose receptor、Fc receptor（IgG-pathogen）、complement receptor、**CD14 & TLR4**（LPS）。
- Cell-mediated cytotoxicity：Tc、NK、myeloid cells；**inhibition vs activation signals（CD2, CD16, CD69）**。
- NK inhibitory receptors：(1) **CD94 ↔ HLA-E**（ITIM）(2) **KIR-2D、KIR-3D ↔ HLA-C**。
- Cytotoxicity mechanisms（Janeway Fig 3.36）：Fas/FasL、TNF/LT、perforin/granzymes。
- 課堂題 8 題（見「課堂題」練習）：遷移順序、C3b 調理、第一會合點 C3 convertase、MAC 組成、MBL、TLR4、CD94/NKG2A、ILC1 敘述。

=== exam ===
# 考點分析

## 🔥 高頻考點（本章是去年考古**題數最多的免疫章節**，63 題）
| 考點 | 出現次數（約） | 典型問法 |
|---|---|---|
| 補體 C3 convertase（C4b2a / C3bBb） | 10+ | 「Which is the C3 convertase of the alternative pathway?」 |
| 補體路徑敘述對錯 | 10+ | 「Not true about classical / alternative pathway」 |
| MAC 組成 C5b-9 | 5 | 常把 C5b 改成 C5a / C3b |
| NK 抑制性受體 CD94/NKG2A、KIR-long | 7 | 「Inhibitory receptor on NK」→ 小心 HLA-E 是 ligand |
| TLR4 ↔ LPS | 6 | 「LPS 的受器」、「TLR4 recognizes endotoxin」 |
| Opsonic receptors | 6 | 「Not an opsonic receptor」→ KIR / MHC II / CD15 |
| 三步驟遷移順序 | 4 | selectin → chemokine → integrin |
| Tc 毒殺機制 | 4 | IFN-γ 無直接關聯 |
| ILC | 3 | ILC1 對抗「胞內」 |

## ⚠️ 陷阱整理
- C2a 不引起發炎（C3a、C5a 才會）。
- Alternative pathway 由 **C3** 開始、不需要抗體；「activated by cleavage of C4」錯。
- Lectin pathway ≈ classical（MBL ≈ C1q），不是 ≈ alternative。
- KIR-3D (short) 不是抑制性（long 才是）。
- CR3 是 complement receptor + integrin，**不是 selectin**。
- CTL 與 NK 皆表現 FasL；只有 CTL 有抗原專一性。

## 📝 出題模式
- 李岳倫老師的課堂題**幾乎原封不動出現在考古**（111、113 都有），務必把 slides 上 8 題練熟。
- 同一概念換句話說重複出題（C3 convertase 出了 6 種問法）→ 用本站「隨機練習」反覆刷。

## 🎙️ 老師課堂提示
- 錄影中練習的課堂題：三部曲排序（selectin → chemokine → integrin）、三路徑的**最初匯合點 = C3 convertase**、MAC = C5b-9、MBL 敘述何者錯（lectin 像 classical 而非 alternative）、LPS 受體 = TLR4、NK 抑制性受體 = CD94/NKG2A、ILC 敘述何者錯（**老師說曾經考過**）。
- 老師明講：「**CD14 + TLR4 是國考常常會考的**」；補體三大功能「一定要知道」；alternative pathway 有**兩種** C3 convertase（C3bBb、C3(H₂O)Bb）。

## 📒 115 共筆對照（W02-2）
- 共筆標示：**補體系統活化路徑是本章重點**；**先天性免疫細胞的分類「老師之前考過」**。
- TLR 介紹（共筆參考 113 補充）：TLR4–LPS（CD14 為 co-receptor）、TLR3–dsRNA（TRIF）。
