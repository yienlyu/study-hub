=== summary ===
# T 細胞媒介免疫與免疫細胞合作（陳玫潔）

> 這堂課分兩大段：**① 活化後 T 細胞的反應**（CD8 CTL、CD4 TH 各亞群的功能）**② 免疫反應中的細胞合作**（TI / TD 抗原、T–B 交互作用、affinity maturation、isotype switch）。T 細胞活化的 Signal ①、② 與免疫突觸見上一章。

## 1. Signal ③：cytokine 決定 CD4 TH 分化 ⭐⭐⭐（老師標「IMPORTANT」）
| 亞群 | 誘導 cytokine（Fig 9.34） | 轉錄因子（共筆） | 分泌 | 對付 |
|---|---|---|---|---|
| **TH1** | IFN-γ、**IL-12**（老師圈起來） | T-bet | **IFN-γ** | 胞內病原、活化 macrophage |
| **TH2** | **IL-4** | GATA3 | **IL-4、IL-5、IL-13** | 寄生蟲（helminth） |
| **TH17** | **TGF-β + IL-6**、IL-23 | RORγt | **IL-17、IL-22** | **胞外細菌、真菌** |
| **TFH** | IL-6（?） | Bcl-6 | **IL-21** | 幫 B 細胞（幾乎所有微生物） |
| **pTreg** | **TGF-β + IL-2** | **FoxP3** | **TGF-β、IL-10** | **抑制**免疫反應 |

- APC 提供三種訊號給 naïve T：MHC II–TCR（①）、B7–CD28（②）、**cytokines IL-6、IL-12、IL-23、IL-4（③）** → activation、proliferation、survival、**differentiation**。
- **IL-2**：T 細胞生長因子（自分泌），也參與 pTreg 誘導。

<div data-fig="th-fate-cytokines"></div>

<div data-fig="th-subsets"></div>

### 黏膜組織：同一個 naïve T，看環境走 pTreg 或 TH17（Fig 9.37）
- 平常（**microbiota**）：iDC 分泌 **all-trans-retinoic acid（at-RA）** + TGF-β → **pTreg**（老師補充：腸腦軸）。
- 感染（**opportunistic pathogens**）：TLR 活化的 mDC 分泌 **IL-6** + TGF-β → **TH17**。

<div data-fig="mucosal-treg-th17"></div>

## 2. 各種 effector T 細胞的武器（Fig 9.42）
| 細胞 | 主要 effector 分子 | 其他 |
|---|---|---|
| **CD8 CTL**（peptide + MHC I） | **Perforin、granzymes、granulysin、Fas ligand** | IFN-γ、LT-α、TNF-α |
| **TH1**（macrophage 活化） | **IFN-γ**、GM-CSF、TNF-α、CD40L、FasL | IL-3、LT-α、CXCL2 |
| **TH2**（barrier immunity） | **IL-4、IL-5**、IL-13、CD40L | IL-3、GM-CSF、IL-10、TGF-β、CCL11（eotaxin）、CCL17 |
| **TH17**（barrier immunity、招 neutrophil） | **IL-17A、IL-17F、IL-22**、CD40L | IL-3、TNF-α、GM-CSF、CCL20 |
| **TFH**（B-cell help） | **IL-21**、IL-4、CD40L | TNF-α、LT-α、CXCL13 |

<div data-fig="effector-molecules"></div>

### T 細胞 cytokine 作用總表（Fig 9.43，紅底為老師標示）
| Cytokine | 來源 | 重點作用 | Knockout |
|---|---|---|---|
| **IL-2** | naïve、TH1、部分 CD8 | **T 細胞生長與分化**；B 細胞生長、J chain 合成 | ↓T 細胞反應、IBD |
| **IFN-γ** | TH1、TFH、CTL | **活化 macrophage、↑MHC I/II**；抑制 TH2、TH17 分化；活化 NK；B → IgG2a（小鼠） | 易感 **mycobacteria**、部分病毒 |
| LT-α（TNF-β） | TH1、部分 CTL | 活化 macrophage、產 NO；殺纖維母細胞、腫瘤 | **沒有淋巴結**、脾臟結構紊亂 |
| **IL-4** | TH2、TFH | **B 活化、IgG1、IgE**、↑MHC II；T 生長存活；↑mast cell | **沒有 TH2** |
| **IL-5** | TH2 | **eosinophil 生長分化**；小鼠 IgA | eosinophilia 減少 |
| **IL-13** | TH2 | IgG1、IgE switch；**↑mucus（goblet cell）** | 驅蟲受損 |
| **IL-17** | TH17、TFH | 刺激纖維母、上皮分泌 chemokine → **招募 neutrophil** | 抗菌防禦受損 |
| **IL-22** | TH17 | 黏膜上皮與皮膚產生**抗菌肽** | 抗菌防禦受損 |
| **IL-21** | **TFH**、部分 TH1、TH17、CTL | **B 細胞生長、germinal center 形成、IgG class switch**；CTL memory | 抗體反應缺陷 |
| **TGF-β** | Treg、TFH | 抑制生長；**IgA switch factor**；促 TH17 與 iTreg、抑制 TH1/TH2；活化 neutrophil | 約 10 週死亡 |
| **IL-10** | Treg、部分 TH1/2/17、CTL | **抑制 TH1**、抑制 macrophage 釋放 cytokine；↑B 的 MHC II | IBD |
| IL-3 | TH1、TH2、TH17 | 造血前驅細胞生長因子（multi-CSF） | — |
| TNF-α | TH1、TH17 | 活化 macrophage、產 NO；活化微血管內皮 | 易 G(+) sepsis |
| GM-CSF | TH1、TH17 | 骨髓造血（granulocyte、macrophage）、分化為 DC | — |

## 3. CD8 CTL ⭐⭐
### 兩種活化方式（Fig 11.21、9.29）
1. **DC 本身共刺激力很強**：感染後 DC 表現大量 **B7** → 直接活化 naïve CD8；DC 的 **IL-12、IL-18** 還能讓 bystander CD8 分泌 **IFN-γ** → 活化 macrophage。
2. **CD4 effector 幫忙**（在次級淋巴器官）：APC 刺激 CD4 表現 **CD40L、IL-2** → APC 經 CD40 被刺激後提高 **B7 與 4-1BBL** → 共同刺激 naïve CD8（4-1BB）。

<div data-fig="cd8-activation"></div>

### 殺手流程
- **Serial killing（Fig 9.44）**：辨識並結合感染細胞 → 啟動目標細胞死亡（DNA fragmentation）→ **移往下一個目標** → 目標細胞 apoptosis，**旁邊未感染的細胞不會被殺**。
- 在周邊組織只需要 Signal ①（effector 不需共刺激）。

<div data-fig="ctl-serial-killing"></div>

| 顆粒蛋白（Fig 9.47） | 作用 |
|---|---|
| **Perforin** | 幫忙把顆粒內容物送進目標細胞的 cytoplasm |
| **Granzymes** | serine protease，進入 cytoplasm 後**啟動 apoptosis** |
| **Granulysin** | 抗微生物、也能誘導 apoptosis |
| **Fas ligand** | 結合目標細胞的 Fas → apoptosis |

<div data-fig="ctl-granules"></div>

### Granzyme B 誘發凋亡（Fig 9.48）
**TCR 接到 pMHC → 定向釋放 perforin + granzymes（與 serglycin 結合）→ granzyme B 進入 cytosol，切 Bid 與 pro-caspase 3 → tBid 擠掉 Bcl-XL、結合 Bax → Bax 寡聚化在粒線體打孔 → cytochrome c 釋出 → apoptosome → caspase 3 切掉 I-CAD → CAD（caspase-activated DNase）切 DNA**。

<div data-fig="granzyme-apoptosis"></div>

- ⚠️ **TGF-β 不是 CD8 毒殺用的分子**（Treg 分泌）。

## 4. CD4 TH 各亞群的功能（Fig 9.33）⭐⭐⭐
| | **TH1** | **TH2** | **TH17** | **TFH** | **Treg** |
|---|---|---|---|---|---|
| 主要 cytokine | **IFN-γ** | **IL-4、IL-5**（骨髓）、**IL-13**（mucus、goblet cell） | **IL-17**（stromal cell → G-CSF、chemokines）、**IL-22**（上皮 → 抗菌肽） | **IL-21** | **TGF-β、IL-10** |
| 被增強的細胞 | **macrophage** → 殺胞內菌 | **eosinophil**、mast cell、basophil | **neutrophil** | B 細胞 → **isotype switching、affinity maturation**、plasma cell | 作用在 conventional DC → **CD4 T 無法活化**（抑制免疫） |
| 對付 | 能抵抗 macrophage 殺菌的微生物：**mycobacteria、Listeria、Leishmania、Pneumocystis**；胞外菌 | **Helminth（寄生蟲）** | **胞外細菌**（*Klebsiella pneumoniae*）、**真菌**（*Candida albicans*） | 幾乎所有微生物 | 自身、共生菌抗原 |

<div data-fig="th-functions"></div>

### 亞群互相抑制（Fig 9.38）
- **TH2 的 IL-4 抑制 TH1 分化**；**TH1 的 IFN-γ 抑制 TH2 增殖**。
- **IL-4 或 IFN-γ 都能抑制 TH17 發育**。
- **Treg 的 TGF-β 抑制 TH1、TH2** 的分化與增殖；IL-10 抑制 TH1。

<div data-fig="th-cross-regulation"></div>

### TH1 → classical activation（M1 macrophage）（Fig 11.10、11.11）
- TH1 用 **CD40L–CD40** + **IFN-γ** 活化受感染的 macrophage。
- **M1 macrophage**：↑MHC I、MHC II、B7、CD40、TNFR-I；產生 **NO、O₂⁻**、TNF-α、**IL-12**（再促 TH1，正回饋）、CXCL9/10/11。

<div data-fig="th1-m1-macrophage"></div>

### TH2 → type 2 response：驅蟲與組織修復（Fig 11.14）
| Cytokine | 作用 |
|---|---|
| **IL-13** | 上皮細胞更新、**mucus**（goblet cell）→ 寄生蟲脫落 |
| **IL-13** | 增加腸道**平滑肌收縮** → 排蟲 |
| **IL-4 + IL-13** | 招募並活化 **M2 macrophage**（arginase-1）→ 平滑肌收縮、**組織修復** |
| **IL-5** | 招募活化 **eosinophil** → MBP 殺蟲、ADCC |
| IL-3、IL-9 | 招募 **mast cell**；IgE 武裝的 mast cell 釋放 histamine、TNF-α、MMCP |

<div data-fig="th2-helminth"></div>

### TH17 → type 3 response：清除胞外菌與真菌（Fig 11.16）
- **IL-17、IL-22** → 上皮產生**抗菌肽**；IL-22 → 上皮更新、細菌難定殖。
- **IL-17** → stromal、myeloid cell 產 **G-CSF** → 骨髓**增產 neutrophil**；並產生 chemokines **招募 neutrophil**。
- **CCL20**（↔ CCR6）→ 招募更多 TH17。

<div data-fig="th17-bacteria"></div>

## 5. B 細胞活化：TD vs TI 抗原 ⭐⭐
- B 細胞發育：pro-B（重鏈重組）→ pre-B（μ + surrogate light chain）→ immature（mIgM）→ mature（**mIgM + mIgD**）→ **抗原刺激** → activated B → **class switching 與分化** → plasma cell / memory B。

| | **TD（thymus-dependent）** | **TI（thymus-independent）** |
|---|---|---|
| 抗原 | **蛋白質** | **TI-1：polyclonal B-cell activator（LPS）**；**TI-2：polymeric（重複）分子**，如莢膜多醣 |
| Signal ① | BCR（+ coreceptor **CD21–CD19** 接 C3d）→ PI3K → Ras/MAPK → AP-1、NFAT | 同樣 BCR → AP-1、NFAT |
| Signal ② | **TFH 的 CD40L ↔ B 的 CD40** → NF-κB（IKK p50/p65；NIK RelB/p100）→ Mcl1 | TI-1：**TLR**（MyD88）→ NF-κB；TI-2：BCR 大量交聯 |
| 結果 | class switch、affinity maturation、**memory**、IgG 為主 | **主要 IgM、記憶很差** |

- TD：B 細胞把抗原吞入、在 **MHC II** 呈現 peptide 給 TFH。
- 嬰兒對莢膜菌（肺炎鏈球菌）易感：TI-2 反應尚未成熟。

<div data-fig="ti-td-antigen"></div>

<div data-fig="ti-poor-memory"></div>

## 6. T–B 細胞交互作用
- **Fig 10.3**：TFH 辨識 B 細胞上的 pMHC II → **CD40L–CD40**、**IL-21 → STAT3**，加上 IL-6、TGF-β、IFN-γ、IL-4（**決定 isotype switch**）→ B 細胞增殖成 **plasmablast（primary focus）** → 再分化為 **germinal center B、plasma cell、memory B**。
- **Fig 10.5 遷移**：
  1. 活化前：B 細胞表現 **CXCR5** 待在 **follicle**（FDC 分泌 CXCL13）；T 細胞表現 **CCR7** 待在 **T-cell zone**（CCL21）。
  2. 活化後：**B 改表現 CCR7、EBI2**；**T 改表現 CXCR5** → 都移到 **B / T 區交界**與 interfollicular 區。
  3. 在 follicle 周邊聚集；部分 B 形成 primary focus 分化成 plasmablast，部分 T 表現 **Bcl-6 → TFH**。

<div data-fig="td-b-activation"></div>

<div data-fig="b-t-migration"></div>

## 7. Affinity maturation：Germinal center 與 SHM ⭐⭐
- **Germinal center B 細胞進行 V-region somatic hypermutation**，親和力變高的被選出（與 **FDC** 上的抗原競爭；Bcl-2 下降、需被救才能存活）。
- 產生 plasma cell 與 **memory B cell**（記憶的主要區域）。
- **AID（activation-induced cytidine deaminase）**：把 **cytidine 轉成 uridine**；由 **IL-4 與 CD40 ligation 誘導**。SHM 和 class switch 都靠它。

<div data-fig="shm-aid"></div>

### AID 之後的修復路徑（Fig 10.18、10.19）
| AID 造成 C → U 後 | 結果 |
|---|---|
| **Mismatch repair**（MSH2/6、Polη） | A-T 突變 → **SHM** |
| **UNG**（base-excision repair）把 U 移除 → abasic site → **REV1** | C-G 突變 → **SHM** |
| abasic → **APE1** → single-strand nicks | gene conversion |
| 兩股鄰近 nicks → **double-strand breaks** | **class switch recombination** |

<div data-fig="aid-mutation"></div>

## 8. Isotype (class) switch ⭐⭐⭐
- 同一個組好的 **VH exon** 接上不同的 **CH 基因** → 只換 constant region、**專一性不變**。
- C 基因順序：人 **μ–δ–γ3–γ1–α1–γ2–γ4–ε–α2**；小鼠 **μ–δ–γ3–γ1–γ2b–γ2a–ε–α**。除了 δ 以外，每個 C 前都有 **switch region**。

### DNA 層級的機制（Fig 10.21、10.22）
1. **Cytokine 活化上游 promoter**，轉錄穿過 switch region。
2. **AID、UNG、APE1** 在兩股 DNA 上打出成串的 nicks。
3. 交錯的 nicks 變成 **double-strand break**（機制未明）。
4. **DSBR machinery** 接合兩個 switch region，中間的 DNA 以**環狀切除** → 選中的 C 接到 VDJ 旁。
- **Switch region 轉出的 intron RNA** 被剪下後形成 **G-quadruplex**，結合 AID 並把它帶到被轉錄的 switch region。

<div data-fig="csr-mechanism"></div>

<div data-fig="class-switch"></div>

### RNA 層級
- **IgM 與 IgD**：同一條 primary transcript（V-D-J–μ–δ）用 **differential RNA splicing**（不同 poly A 位置）→ 成熟 B 細胞同時表現 mIgM + mIgD。
- **Membrane 與 secreted form**：同樣靠 RNA 層級的處理（poly A 位置）；secreted 用 S 尾端，membrane 包含 **M exons**（跨膜區）。

<div data-fig="igmd-splicing"></div>

<div data-fig="membrane-secreted"></div>

### Cytokine 決定換成哪一型（Fig 10.23，以小鼠為主）
| Cytokine | 誘導 isotype |
|---|---|
| **IL-4** | **IgG1、IgE** |
| **IFN-γ** | IgG3、IgG2a |
| **TGF-β** | IgG2b、**IgA** |
| **IL-21** | IgG3、IgG1、IgA |
| **IL-5** | IgG1、**IgA** |

- 機制：cytokine **促進特定 switch region 上游 promoter 的轉錄**。

<div data-fig="cytokine-isotype"></div>

### X-linked hyper-IgM syndrome
- **CD40L（CD154）缺陷**（T 細胞上）→ 無法 class switch → IgM 正常或升高、IgG/IgA/IgE 低；CD4 T 細胞數目**正常**；易反覆感染。

## 9. 抗體反應
- **Primary 四期**：lag → log → plateau → decline；先 IgM 後 IgG。
- **Secondary**：lag 短、抗體量高（約百倍）、**IgG 為主**、親和力更高。

<div data-fig="ab-response"></div>

## 10. 先天與後天整合：Immune effector modules（Fig 11.5、11.21）
| Module | ILC | T 細胞 | 效應細胞 | 主要結合的抗體 |
|---|---|---|---|---|
| **Cytotoxic** | NK（EOMES、T-bet；IL-15、IL-12、IL-18） | **CTL** | perforin / granzymes | NK：**IgG1、IgG3**（FcγRIII，ADCC） |
| **Type 1** | ILC1（T-bet） | **TH1**（IL-12） | **macrophage**（IFN-γ） | IgG1、IgG3、IgA |
| **Type 2** | ILC2（GATA3；IL-25、IL-33、TSLP） | **TH2**（IL-4） | **eosinophil、mast cell、basophil**（IL-5、IL-13） | eosinophil：IgE、IgG1、IgG3、IgA；**mast cell、basophil：IgE**（FcεRI） |
| **Type 3** | ILC3（RORγt、AHR；IL-23、IL-1） | **TH17**（TGF-β + IL-6） | **neutrophil**（IL-17、IL-22） | IgG1、IgG3、IgA |

<div data-fig="isotype-modules"></div>

## 🎙️ 上課錄影重點（陳玫潔，10/02）
- 開場：**T 細胞不會平白釋出 cytokine 幫別人**，與其他細胞作用通常有專一性辨識。T–B interaction 發生在次級淋巴組織 **T zone 與 B zone 的交界**（像隔著鐵窗），互相交換 chemokine / chemokine receptor、兩者皆活化。
- **TD vs TI 由抗原材質決定**：沒有蛋白質 → 沒有 peptide 可放上 MHC II → 無法活化 T → **不能 affinity maturation、不能 isotype switch**。V(D)J 重組是亂數、不受調控；**activation 後的優化受 T 細胞 cytokine 調控**。
- **今天重點 = signal 3**（sensor cell 概念的延續）：APC 初次接觸病原 → PAMP–PRR → 新的轉錄轉譯 → 帶著獨特的 cytokine 到次級淋巴組織，決定 T 細胞分化方向。
- **「這一張請大家背起來：決定命運的 cytokine」（黃色、紅色都要背）**：**IL-12 → TH1（IFN-γ）**；**IL-4 → TH2（IL-4、IL-5）**；**只有 IL-6 → TFH（IL-21，在 follicle 幫 B）**；**TGF-β + IL-2 → pTreg（TGF-β、IL-10，peripheral tolerance）**；**TGF-β + IL-6 + IL-23 → TH17（IL-17，胞外菌）**。TGF-β 是抑制型（癌細胞也會分泌）；IL-2「沒什麼了不起」——活化都需要、沒有選擇性。
- TH 亞群**沒有 surface marker 可以區分**（曾有人想找 marker 當博士論文，畢業了但沒找到），只能靠分泌的 cytokine。
- **分化是單行道**（「兩條路在森林裡只能挑一條」）：不能同時走兩條，但環境改變可以轉換；彼此抑制——TH2 的 IL-4 抑制走向 TH1、TH1 的 IFN-γ 抑制 TH2 增殖；Treg「所向披靡、全部抑制」；TH1、TH2 的 cytokine 都會阻止走向 TH17。
- **腸道例子**：共生菌存在時，周邊的 **immature DC 釋放 all-trans retinoic acid（ATRA）**、只有 TGF-β → **Treg** → 不攻擊共生菌（否則就是內耗；Crohn's disease 是失衡例子；**gut–brain axis** 與 autism spectrum、阿茲海默症有關）；病原來了（「營養午餐禍從口入」）→ TLR 活化 → **mature DC 釋放 IL-6** → TGF-β + IL-6 → **TH17** → 叫大量 neutrophil 吞病原。
- 功能速記：**TFH**（IL-21、CD40L 幫 B）；**TH17**（IL-17 → neutrophil）；**TH2**（IL-4、IL-5 → 寄生蟲、過敏）；**TH1**（看到 IFN-γ 就想 **macrophage** → 胞內菌如 mycobacteria、*Listeria*）；CD8 不再細分，跟**病毒**等胞內感染有關。
- **TNF 家族多功能**：淋巴組織 **organogenesis**（LT-α knockout → 淋巴結長不出來、脾臟怪怪的）、免疫細胞交互作用的共刺激（CD40L、4-1BB）、執行細胞凋亡（**FasL**）。早期免疫學大量用 knockout mice（「小時候把爸爸的新玩意弄壞看會喪失什麼功能」）。
- **CD8 / CTL**：naive CD8 在次級淋巴組織被 APC 活化 → 變 effector 後**一定要離開**到周邊（躲在淋巴組織沒用）；在淋巴組織叫 CD8、執行作用時叫 **CTL**。在周邊**只需 signal 1**（target cell 只會「揮舞著 peptide」，沒有 signal 2）。
- **CD8 活化兩條路**：① **DC**（可 cross-priming）直接活化，釋放 IL-12 等、高 B7（CD28–B7「簡配」）→ CD8 產生大量 **IFN-γ** 也能活化 macrophage（將軍出去打仗也要有小兵）；② **CD4 幫忙**：同一個 APC 用 MHC II 活化 CD4 → CD4 分泌 **IL-2「雨露均霑」**、APC 被活化後 ↑**B7、4-1BBL** → 活化 CD8。⚠️ 這件事**發生在次級淋巴組織、不在周邊**，而且需要很厲害的 APC。
- **CTL 殺手流程**：只認 signal 1 → 誘發 target **programmed cell death** → **不等它死、馬上找下一個苦主**（serial killing）；正常細胞沒有專一性辨識就不會死。凋亡一旦啟動就「死透了」。
- **兩種武器都誘發凋亡（cascade 略有不同）**：① granule 往接觸點聚集（螢光超亮）→ **perforin 打洞**、**granzyme（serine protease）**（+ serglycin）送進去 → 粒線體釋放 **cytochrome c** 放大 → **caspase**（到 caspase-3 必死無疑）→ DNase 切碎染色體 → 電泳 **DNA laddering**；② **FasL** 較快、不需 cytochrome c。
- **Bcl family**：名字聽起來像詛咒的 **Bax、Bid → 促凋亡**；聽起來和緩的 **Bcl-2、Bcl-xL → 抗凋亡**（「記不起來就算了」）。
- 「如果後面細節無法承受，**至少看一下那張 summary 圖**」：
  - **TH1 → M1 macrophage**：IFN-γ + **CD40L–CD40** → 吞噬更強（ROS、NO↑）、**MHC 與共刺激分子↑**（更好的 APC）、更多 cytokine → 回饋活化 TH1。M2 與組織修復有關（腫瘤中也有）。
  - **TH2**：IL-4、IL-13 → **M2 macrophage（arginase-1 定義）** → tissue remodeling / repair；**IL-5 → eosinophil**（殺寄生蟲、**ADCC**「借刀殺人」）；**IL-13** → 上皮修復、**goblet cell 產 mucus**、上皮 turnover 加快（寄生蟲勾不住）、**平滑肌收縮把蟲擠出去**（所以寄生蟲感染會肚子痛）；活化 **mast cell degranulation**（histamine）。cytokine 也作用在骨髓，像 Star Wars 的**複製人軍隊**大量產出特定顆粒球。
  - **TH17**：胞外菌、真菌（*Candida*）；IL-17 → 骨髓 stromal cell 產 **G-CSF** → neutrophil 變多（複製人軍團「戴白帽子」）；IL-17 讓上皮產 **chemokine** 把 neutrophil 叫到該去的地方；**IL-22** → 上皮 turnover、IL-17 / IL-22 → **antimicrobial peptides**；**CCL20**（對應 chemokine receptor）。
  - **Treg**：抑制性 cytokine 關掉所有免疫反應 → tolerance；老師「沒有打算講」。
- **IgM =「掃地機器人的刷子」**：抗體有 hinge 可轉，兩個結合位的總親和力不只 ×2（可達幾十到幾百倍），IgM 有 **10 個結合位** → 先把病原困在當地（實驗課的免疫凝集）、活化補體 classical pathway、調理；但親和力不完美（先找形狀差不多的鑰匙，之後才用砂紙磨）。
- B 細胞以 BCR 把抗原 **internalize** → 切碎 → MHC II vesicle → 呈現給 T（沒有 peptide 就是「空的麵包」）。親和力由考官 **FDC** 決定：搶得過 → 表現 **Bcl-2（免死金牌）** 存活；搶不過 → 凋亡；B 細胞在 follicle「巡迴演唱」反覆挑選。Class switch：腸道 → IgA、一般 → IgG（半衰期約 20 多天）→ 周邊血第一次感染 IgM 為主、之後 IgG 為主。暴露越多次親和力越高 → **booster**。
- **TI 抗原**兩種：① **polymeric（多價）**：同一 B epitope 重複多次（如多醣）→ 多個 BCR 同時結合 = 超強活化訊號；② 同時活化多個 clone（**LPS 經 TLR**）。都沒有 T 參與 → **永遠 IgM、每次感染都像第一次、記憶差**。**自然界 90% 以上的抗原是 TD**。
- **TFH** 在 T–B 交界與帶好大亨堡的 B 細胞專一結合 + **CD40–CD40L** → 分泌 **IL-21** 等 → isotype switch、memory B。兩個細胞要先靠近（cytokine 分子小、跑不遠，不能「牧童遙指杏花村」）。
- **AID（activation-induced cytidine deaminase）**：把 **C 變成 U** → 修復時換掉一個 nucleotide → codon 改變 → V region 點突變（SHM）；也誘發 **constant region** 的 class switch；由 **IL-4 + CD40 ligation**（T 細胞協助）誘導。
- **IgM → IgD 不是 DNA 重組**（μ 與 δ 之間沒有 switch region）→ 是 **differential RNA splicing**（不需活化，早期就能做）；**membrane form → secreted form 也是 RNA 層級**（保留 secreted leader / membrane exon）。其他 isotype 是 **DNA 層級的 class switch recombination**：不同 cytokine 讓不同 switch region 轉錄出特殊 RNA，形成 **G-quadruplex（四個 G 的小盒子）** 引導 AID 去切（細部機制還不清楚）。酵素細節「略懂即可」。
- **Cytokine → isotype 表「只能無奈地了解它、接受它」**：例如 **IL-4 → IgG1、IgE**；**IFN-γ → IgG3、IgG2a**（以小鼠為主，小鼠 IgG subtype 和人不同）。
- **抗體反應四期**：lag（病原要漂到最近的淋巴結或脾臟、被吞噬、活化 B）→ 指數上升（membrane form 立刻變 secretory form）→ plateau → decline（plasma cell 壽命有限、抗體有半衰期）；二次反應**沒有 lag phase**、以 IgG 為主。Memory cell 在廣島、長崎倖存者身上 **30–40 年**後仍找得到。疫苗讓你先經歷這段過程（小黃卡上的公費疫苗都是致死或嚴重傷殘的疾病，如**麻疹**可能造成 retardation）。
- **Immune effector module**：ILC / NK 在感染初期分泌的 cytokine（IFN-γ、IL-5 / IL-13、IL-17 / IL-22）和之後 TH1 / TH2 / TH17 的**一模一樣**（「同出一轍」）→ innate 非常重要，只是沒有抗體、活化強度較弱。Type 2 → eosinophil、IgE（黏膜 / 寄生蟲）；type 3 → neutrophil、IgG1、IgA；type 1 → macrophage、IgG1 / G3；cytotoxic → 類似 NK。

=== slides ===
# W4-2 上課 slides 重點：T cell–mediated immunity & Cell cooperation（陳玫潔）

> 共 49 頁，對應 Janeway **Ch 9** T Cell–Mediated Immunity、**Ch 10** The Humoral Immune Response、**Ch 11** Integrated Dynamics of Innate and Adaptive Immunity。

**Part 1 — Response of activated T cell（p.1–26）**
- Key subjects：① CD8⁺（CTL）的功能 ② CD4⁺（TH）的功能。
- p.3 APC 給 naïve T 三種訊號，**Signal ③ = cytokines（IL-6、IL-12、IL-23、IL-4）** → activation、proliferation、survival、differentiation。
- **p.4 Fig 9.34**（老師手寫「**IMPORTANT**」）：fate-specifying cytokines → TH1（IFN-γ、**IL-12** 圈起）、TH2（IL-4）、TH17（TGF-β、IL-6、IL-23）、TFH（IL-6?）、pTreg（TGF-β、IL-2，旁註「抑制」）；下方黃框為各亞群分泌物。
- p.5 Fig 9.37：黏膜組織 at-RA（**microbiota**，旁註「腸腦軸」）→ pTreg；TLR 活化 mDC + **IL-6** → TH17（**opportunistic pathogens**）。
- p.6 Fig 9.42 effector 分子總表（黃色螢光：IFN-γ、IL-4、IL-5、IL-17A、IL-17F、IL-22、IL-21）。
- p.7–9 Fig 9.43 三頁 cytokine 表（紅底格子：IL-2 對 T、IFN-γ／LT-α 對 macrophage、IL-4 對 B 與 T、IL-5 對 eosinophil、IL-13 對 goblet cell、IL-21 對 B、IL-3／GM-CSF 對造血）。
- **CTL（p.10–16）**
  - p.12 體液 vs 細胞免疫總覽圖（框 Tc → CTL 殺 altered self-cell）。
  - **p.13 CD8 活化兩種方式**：① DC 高共刺激（B7）、IL-12 / IL-18 → bystander CD8 分泌 IFN-γ ② **CD4 effector 幫忙**（CD40L、IL-2 → APC ↑B7、4-1BBL）；手寫「CD4 活化時會幫助 CD8 activate → 次級淋巴器官（vs 周邊）」。
  - p.14 Fig 9.44 serial killing；p.15 Fig 9.47 顆粒蛋白表（perforin、granzymes、granulysin、Fas ligand 紅框）+ Fig 9.49 time-lapse。
  - **p.16 Fig 9.48** perforin / granzyme B → Bid → tBid → Bax → cytochrome c；caspase 3 → I-CAD → CAD → DNA fragmentation。
- **CD4 TH（p.17–26）**
  - **p.20 Fig 9.33**（手寫「T help cell」）：五個亞群的 cytokine、目標細胞、對付的抗原；紅框 **eosinophil**、**neutrophils**、**extracellular bacteria**、**fungi**；Treg 旁註「抑制免疫反應」。
  - p.21 Fig 9.38 亞群互相抑制（IL-4 ⊣ TH1、IFN-γ ⊣ TH2、IL-4 / IFN-γ ⊣ TH17、Treg TGF-β ⊣ TH1 與 TH2）。
  - p.23 Fig 11.10 / 11.11：TH1 用 CD40L + **IFN-γ** 活化 **M1 macrophage**。
  - p.25 Fig 11.14：TH2 → type 2 response，驅蟲與修復（紅框 **M2 macrophages**）。
  - p.26 Fig 11.16：TH17 → type 3 response，對付**胞外菌與真菌**。

**Part 2 — Cell cooperation in the immune responses（p.27–49）**
- Key subjects：① T-independent & dependent antigens ② T–B cell interactions ③ Affinity maturation ④ Isotype switch。
- p.29 B 細胞發育表（紅框 **Antigen stimulation**、**Class switching and differentiation**）。
- **p.31 Fig 10.2** TD vs TI 抗原（coreceptor CD21/CD19；CD40 與 TLR 圈起）；**TI-1 = polyclonal B-cell activators、TI-2 = polymeric molecules**。
- p.32 **T-independent Ag induce poor memory**（TI 只有 IgM，TD 二次反應 IgG 大量上升）。
- p.33 Fig 10.3 T-dependent B cell activation（標註 **Isotype switch**）。
- p.35 Fig 10.5：B 細胞遇到抗原後移到**次級淋巴組織 B / T 區交界**（CXCR5、CCR7、EBI2、Bcl-6）。
- p.37 Fig 10.13 **Somatic hypermutation**；**AID 把 cytidine 轉成 uridine，由 IL-4 與 CD40 ligation 誘導**。
- p.39 人與小鼠的 constant region 基因排列。
- p.40 Fig 10.18 / 10.19：AID 引入突變 → SHM、gene conversion、class switch recombination。
- p.41 Fig 10.21：AID 啟動 class switch（μ → ε 為例；AID、UNG、APE1 打 nicks → DSB → DSBR）。
- p.42 Fig 10.22：switch region intron RNA 形成 **G-quadruplex** 引導 AID。
- p.43 **IgM、IgD 用 differential RNA splicing**；p.44 **membrane / secreted form** 靠 RNA 層級調控。
- **p.45 Fig 10.23**：cytokine → isotype 表（IL-4、IFN-γ、TGF-β、IL-21、IL-5）。
- p.46–47 primary 抗體反應四期、primary vs secondary。
- p.48 Fig 11.5 immune effector modules（Cytotoxic、Type 1、2、3）；p.49 Fig 11.21 各 module 的效應細胞由哪些 isotype 武裝。

=== exam ===
# 考點分析

## 🔥 高頻考點（去年考古）
1. **IL-12 → TH1**（考 4 次，還有複選組合版）。今年 slides 老師也特別圈 IL-12。
2. **TH1 分泌 IFN-γ**；**TH2 不分泌 IL-12**。
3. **CD40L 缺陷 → hyper-IgM**；hyper-IgM「CD4⁺ T 數目下降」為錯。
4. **Class switch 需要 CD4 T 細胞**（考 2 次）。
5. **IL-4 → IgE**；IL-5 → IgA；TGF-β + IL-6 → TH17。
6. **FasL 誘發 T 細胞凋亡**（考 2 次）；perforin 在靶細胞打洞。
7. **CTLA-4 結合 B7**；CD28 為 naïve T 的 second signal。
8. **Germinal center 是抗體記憶產生的主要區域**；「沒有 B 細胞凋亡」錯。
9. **TFH 主要分泌 IL-21**。
10. **TI 抗原產生 IgM**。

## 🆕 今年 slides 新強調、可能出題
- **Fig 9.34 fate-specifying cytokines**（老師寫 IMPORTANT）：注意 slides 的 **pTreg = TGF-β + IL-2**、TH17 多了 **IL-23**。
- **黏膜組織 at-RA → pTreg、IL-6 → TH17**（共生菌 vs 伺機性病原）。
- **Fig 9.33 各亞群對付的病原**：TH1 → mycobacteria、Listeria、Leishmania、Pneumocystis；TH2 → helminth；**TH17 → 胞外菌（Klebsiella）與真菌（Candida）**；Treg → 抑制。老師紅框 eosinophil、neutrophil。
- **CD8 活化兩條路**：DC 高 B7 直接活化、或 **CD4 幫忙（CD40L → APC ↑B7、4-1BBL）**。
- **Granzyme B 凋亡路徑順序**：Bid → tBid → Bax → cytochrome c；caspase 3 → I-CAD → CAD。
- **Serial killing**：殺完一個就換下一個、旁邊未感染細胞不受影響。
- **TH2 的 M2 macrophage（IL-4 + IL-13）** vs **TH1 的 M1（IFN-γ、CD40L）**。
- **TH17：IL-17 → G-CSF → neutrophil**；IL-22 → 抗菌肽；CCL20–CCR6。
- **TI-1（LPS、polyclonal、TLR）vs TI-2（polymeric）**；TI 記憶差。
- **B/T 遷移的趨化受體**：活化前 B = CXCR5、T = CCR7；活化後互換（B ↑CCR7、EBI2；T ↑CXCR5）；Bcl-6 → TFH。
- **AID：C → U，由 IL-4 + CD40 誘導**；UNG、APE1、mismatch repair 各自導致的結果。
- **IgM/IgD 是 RNA splicing、其他 isotype 是 DNA 重組**；switch region RNA 的 G-quadruplex 引導 AID。
- **Cytokine → isotype 表**，注意 slides 版本 **IL-21 → IgG3、IgG1、IgA**。
- **Immune effector modules** 與各 Fc receptor 結合的 isotype（mast cell / basophil = IgE）。

## 📝 出題模式
- 中英對照題（去年考古中英並列），常以「下列何者可誘使…」「下列何者為 TH1 所分泌」出現，**TH 分化表一定要背熟**。
- 陳玫潔老師的 slides 幾乎都是 Janeway 圖表，表格（Fig 9.33、9.42、9.43、10.23）很適合出「配對何者錯誤」。

## 🎙️ 老師課堂提示
- 老師明講要背：**fate-specifying cytokine 圖**（IL-12 → TH1、IL-4 → TH2、IL-6 → TFH、TGF-β + IL-2 → pTreg、TGF-β + IL-6 + IL-23 → TH17，與各自分泌的 cytokine）、**cytokine → isotype 表**（「只能接受它」）。
- 老師說可以放過：Fig 9.43 中 LT-α 等細節、凋亡 cascade 細節（Bcl family「記不起來就算了」）、AID 修復酵素細節（「略懂即可」）、Treg 功能（沒打算講）。
- 易考觀念：TH 分化是單行道且互相抑制；**CD4 幫 CD8 發生在次級淋巴組織**；CTL 在周邊只需 signal 1、serial killing；**IgM→IgD 與 membrane→secreted 是 RNA splicing**，其他 isotype 是 DNA 重組；**AID 把 C 變 U**、由 IL-4 + CD40 誘導；TI 抗原只有 IgM、記憶差；自然界 > 90% 為 TD 抗原。

## 📒 百十四共筆對照（W4-2）
- **Immune tolerance** 那部分老師放 PDF 補充、上課沒講（自己看）。
- **T–B cell interactions（次級淋巴組織中的相遇順序）**：共筆註記「**根本沒考過，老師也很隨便帶過**」，可放最後讀。重點只要記：B 細胞 **CXCR5**（CXCL13，留在濾泡）、T 細胞 **CCR7**（CCL19／21）；活化後 B ↑CCR7 往 T 區、T ↑CXCR5 往濾泡。
- AID 之後 staggered nicks 變 double-strand break 的詳細機制**不需深入**，知道最後造成 class-switch recombination 即可。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| IL-4 → TH1 | **IL-12 → TH1**（考 4 次）；IL-4 → TH2 |
| TH2 分泌 IL-12 | IL-12 由 **APC** 分泌；TH1 分泌 **IFN-γ**；TH2 分泌 IL-4、5、13 |
| TH17 由 TGF-β 單獨誘導 | **TGF-β + IL-6（+ IL-23）→ TH17**；**TGF-β + IL-2 → pTreg** |
| TFH 主要分泌 IL-4 | **TFH 主要分泌 IL-21**；Bcl-6 決定 TFH |
| Hyper-IgM 是 CD4 T 數目下降 | 是 **CD40L 缺陷**，CD4 數目正常 |
| Class switch 不需要 T 細胞 | Class switch **需要 CD4 T（CD40L + cytokine）** |
| IL-5 是 IgA class switch 的關鍵 | **TGF-β** 是 IgA switch 的關鍵（考古也出現 IL-5 → IgA，選項中要比較）；**IL-4 → IgE** |
| IgM 與 IgD 共表現靠 DNA 重組 | **RNA splicing**（membrane vs secreted 也是）；其他 isotype 才是 DNA switch recombination |
| AID 把 U 變成 C | **AID 把 C 去胺成 U**，由 IL-4 + CD40 誘導 |
| TI 抗原產生大量 IgG 與記憶 | TI 抗原以 **IgM** 為主、**記憶差** |
| Germinal center 沒有 B 細胞凋亡 | Germinal center **有大量凋亡**（篩選高親和力） |
| CD4 幫 CD8 發生在周邊組織 | 在**次級淋巴組織**（CD40L → APC ↑B7、4-1BBL） |
| TH17 主要對付病毒 | **TH17 → 胞外菌（Klebsiella）與真菌（Candida）**，經 IL-17 → G-CSF → neutrophil |
| M1 macrophage 由 IL-4 誘導 | **M1 = IFN-γ、CD40L（TH1）**；**M2 = IL-4 + IL-13（TH2）** |
| Perforin 誘發凋亡、FasL 打洞 | **Perforin 打洞**讓 granzyme 進入；**FasL** 結合 Fas 誘發凋亡 |
