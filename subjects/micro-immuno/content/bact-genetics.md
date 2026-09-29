=== summary ===
# 細菌遺傳與生物技術

## 1. 基因體
- **Genome** = 染色體 + 質體上所有基因。
- 染色體：**單一、環狀、雙股 DNA，附著於細胞膜，haploid**（例外：*Streptomyces* 線形、*V. cholerae* 多條）。
- **Nucleoid**：染色體 DNA + 類組蛋白的蛋白質 + 少量 RNA（無核膜、無 histone）。
- **Plasmid**：染色體外、雙股環狀、**可獨立複製（replicon）**；G+、G− 都有；功能：**抗藥性基因傳播**、致病因子（外毒素）、重金屬抗性（Hg、Ag 還原酶）、pili/fimbriae。

## 2. DNA 複製
- 起點 **oriC**（富含 A=T，DnaA 辨識）→ **雙向（bidirectional）**、**半保留**、兩個複製叉。
- Helicase + gyrase 解旋；DNA 只能 **5'→3'** 合成。
- Leading strand 連續；Lagging strand：primase 做 RNA primer → Pol III 做 Okazaki fragments → **Pol I 去除 primer 補 DNA** → ligase 接合。
- ⚠️ **DNA polymerase 兩個方向都參與**（考古「只參與一個方向」為錯）。
- 終止：Topo IV、**dif / XerCD** 分離子代染色體。

## 3. 基因表現與調控
- **細菌 transcription 與 translation 同時進行**（無核膜）、polyribosome；無 intron；mRNA **不需修飾**即可轉譯。
- **Operon**：promoter + operator + 多個 structural genes（cistrons）→ **polycistronic mRNA，一起轉錄**。
- **60–80% 基因為 constitutive（不受調控）**，如糖解酶。
- **Induction（預設 OFF）**：*lac* operon
  - 無乳糖：repressor 結合 operator → 關。
  - 有乳糖：allolactose 使 repressor 失活 → 開。
  - 葡萄糖低 → **cAMP↑ → cAMP-CAP 結合 promoter → 大量表現（positive regulation）**。乳糖是「開關」，葡萄糖決定「多寡」。
- **Repression（預設 ON）**：*trp* operon
  - Trp（**corepressor**）+ inactive repressor → active repressor 結合 operator → 關。
  - **Attenuation**：Trp 高 → 核糖體通過 → region 3–4 hairpin（terminator）；Trp 低 → 核糖體卡在 region 1 → 2–3 anti-terminator → 繼續轉錄。

## 4. 重組
- **Homologous（general）recombination**：最常見，需序列相似，RecA。
- **Non-homologous**：少見於原核。
- **Site-specific recombination**：需 **recombinase + 兩段特定序列** → λ phage 嵌入（attP × attB，lysogenic）、***Salmonella* flagellin phase variation**。

## 5. 突變
- 定義：穩定、可遺傳的 DNA 改變。自發率約 **10⁻⁹（E. coli）**；mutator genes 破壞修復而增加突變率。
- 外因：物理（UV → **pyrimidine dimer**、X-ray）、化學（DNA-reactive、**base analogues**、**intercalating agents → frameshift**）。
- DNA 層級：substitution（**transition**：嘌呤↔嘌呤 / 嘧啶↔嘧啶；**transversion**：嘌呤↔嘧啶）、insertion/deletion。
- 蛋白層級：**silent**（同 aa，密碼子簡併）、**missense**（aa 改變；conservative 如 Val→Ala）、**nonsense**（stop codon → 截短）、**frameshift**（之後全錯）→ 可造成 **null mutation**。
- 🧮 **計算題技巧**：第 n 個核苷酸屬於第 ⌈n/3⌉ 個密碼子。
  - 1 個 nt deletion at 76：76/3 = 25 餘 1 → 前 25 個 aa 不變，**之後全變**。
  - 3 個 nt deletion at 121–123：剛好是第 41 個密碼子 → **只少第 41 個 aa**，其餘不變（in-frame）。
- 修復：direct（**photolyase**，光修復）、excision、recombinational（SOS 後）、error-prone。

## 6. 水平基因轉移（HGT）

| 方式 | 媒介 | 是否需接觸 | 關鍵字 |
|---|---|---|---|
| **Transformation** | 環境中裸露 DNA | ❌ | **competence**、同源重組、對 nuclease 敏感 |
| **Conjugation** | 質體，**sex pilus**（G−） | ✅ 直接接觸 | **抗藥性質體傳遞最重要途徑**；G+ 靠黏性物質 |
| **Transduction** | **噬菌體（phage）** | ❌ | generalized（任何片段）vs specialized（插入點附近） |
| Transposition | Transposon（jumping gene） | — | 細胞內位置移動；transposase（site-specific） |

- **Transposable elements**（Barbara McClintock，1983 諾貝爾）：IS（只帶 transposase、兩端反向重複）與 composite Tn（兩端 IS 夾抗藥基因）；不能自我複製。
- 臨床：**MRSA + VRE 之 vanA → VRSA / MVRSA**。
- ⚠️ Translation 不是 HGT。

## 7. 生物技術
- **Recombinant DNA**：restriction enzyme 切 → ligase 接到 vector → 轉入 *E. coli*。
- **PCR**：denaturation（90–95°C）→ annealing → extension（~72°C，Mg²⁺）；需 primers、dNTPs、thermostable polymerase、template；指數放大。
- **Sanger**：**ddNTP（缺 3'-OH）終止延長**；dye-terminator + 毛細管電泳，讀長約 800 bp。
- **NGS（illumina）**：massive、parallel、sequencing-by-synthesis。
- **16S rRNA amplicon sequencing**：9 個變異區 V1–V9，常用 **V3–V4** → 分析菌相組成。
- **CRISPR-Cas9**：細菌的後天免疫（specific、memory）；spacer 記錄入侵 DNA；crRNA + tracrRNA（→ sgRNA）引導 Cas9 切 DSB；PAM 防止切到自己；修復：**NHEJ → gene disruption**、**HDR → gene editing**（2020 諾貝爾化學獎）。
- 應用：大腸桿菌生產 insulin、interferon；表面蛋白疫苗；基因治療。

=== slides ===
# W1-2 上課 slides 重點：Bacterial genetics & biotechnology（Ch.13）

- Bacterial genome & chromosome（p.2）：single dsDNA, closed circular, attached to membrane → **haploid**；nucleoid。
- Plasmid DNA（p.3）：replicons、G+ & G−、可共存；四大功能（抗藥、毒素、重金屬、pili）。
- DNA 組成 / 結構（p.4–5）：purines A/G、pyrimidines C/T；right-handed、anti-parallel。
- Replication（p.7–8）：oriC、bidirectional、semi-conservative、high fidelity；Topo IV、dif/XerCD；gyrase & helicase、Pol III / Pol I（5'→3' exonuclease）。
- Prokaryotic gene structure（p.10–11）：operon（polycistronic）、noncoding / rRNA / tRNA；**simultaneous transcription & translation**。
- Regulation（p.12–14）：60–80% constitutive；induction vs repression；**lac operon**（positive regulation depends on cAMP）；**trp operon**（co-repressor、attenuation-antitermination）。
- Recombination（p.16–17）：homologous / non-homologous；site-specific（phage integration、*Salmonella* flagellar phase variation）。
- Mutation（p.19–21）：~10⁻⁹、mutator genes、mutagens；transition / transversion；silent / missense（conservative）/ nonsense / frameshift / null。
- DNA repair（p.22）：direct（photolyase）、excision、recombinational（SOS）、error-prone。
- HGT（p.23–27）：transformation（competence、nuclease sensitive）、conjugation（pilus in G−、transconjugants）、transduction（generalized / specialized）、transposition。
- Transposable element（p.28–30）：McClintock、IS / Tn、**MRSA → MVRSA**。
- Biotechnology（p.31–42）：recombinant DNA、PCR、Sanger / dye-terminator、shotgun、NGS、16S rRNA、therapeutic applications、CRISPR-Cas。

=== exam ===
# 考點分析

## 🔥 高頻考點
1. **HGT 定義與構造配對**：Conjugation / sex pili（最常考）；Transduction = 噬菌體（題目問「需與 virus 接觸」）；Transformation = 環境 DNA、competence。
2. **Frameshift 計算題**：每年都有「coding region X nt，在 Y 位置刪除」→ 判斷影響哪些 aa。記住 in-frame（3 nt）只少一個 aa。
3. **細菌基因表現特色**：轉錄轉譯同時、operon 一起轉錄、多數基因為 constitutive。
4. **Repressible operon**：corepressor–repressor 複合體結合 operator。
5. **DNA 複製**：兩股同時、Pol 參與兩個方向、lagging strand 需 RNA primer。
6. **Plasmid**：可在細菌間傳遞抗藥基因（不與染色體同步複製、不是 RNA、G+ 也有）。

## ⚠️ 陷阱
- 「mRNA needs to modify and translocate」→ 真核才要。
- 「Operon 基因個別轉錄」→ 錯，一起轉錄。
- 「Most metabolic genes are regulated」→ 錯，60–80% constitutive。
- 增加一個核苷酸 → frameshift → 答案選 **null mutation**（111 考古）。

## 📝 出題模式
- 以單選定義題為主，搭配 1 題計算題；偶有「Genetic changes can be brought about by…（All of the above）」。
- 生物技術（PCR、CRISPR、16S）去年考古未直接出，但老師上課強調 **16S rRNA amplicon sequencing** → 今年可能出。
