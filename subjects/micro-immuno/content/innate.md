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
