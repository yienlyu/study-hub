=== summary ===

# 核苷酸代謝 內容整理（依百十四共筆整理、對照百十三共筆，鄭嘉雄）

> 📌 **期末範圍。**11/5 上課（鄭嘉雄）。依百十四共筆 W9（Chapter 22-4，115. Nov. 5）與今年 slides「Lehninger-pob8-ch22」（68 頁）整理，文末對照百十三共筆；slides 逐頁重點與錄影裡老師提點的考點在「上課重點」。

## 1. 核苷酸的組成與功能

- **Nucleotide = 含氮鹼基 + 五碳糖 + 磷酸**；**nucleoside = 鹼基 + 五碳糖**（沒有磷酸）。**沒有 glucose**。
  - 鹼基接在五碳糖 **C1′**；**C2′ 是 –OH → ribonucleotide（RNA）**，**–H → deoxyribonucleotide（DNA）**。
  - 聚合時新的 **NTP／dNTP 的 5′ 三磷酸**接到鏈末端的 **3′–OH**、脫掉 PPi → 鏈只能 **5′ → 3′** 延長，所以合成原料一定要是**三磷酸**。
  - **Purine（雙環）：A、G**；**pyrimidine（單環）：C、U、T**。一個 purine 配一個 pyrimidine，DNA 雙股寬度一致（A=T 兩個氫鍵、C≡G 三個）。
- 功能：① **DNA、RNA 的原料** ② **能量載體**（主要 ATP，部分 GTP）③ **輔因子成分**：NAD、FAD、SAM（AdoMet）、**coenzyme A**，以及活化的生合成中間物（**UDP-glucose → 肝醣**、**CDP-diacylglycerol → 磷脂**）④ **第二傳訊者**：cAMP、cGMP。

## 2. 兩條合成路徑與 PRPP ⭐⭐

|      | **De novo（從頭合成）**                  | **Salvage（回收）**                    |
| ---- | ---------------------------------------- | -------------------------------------- |
| 原料 | **胺基酸、ribose-5-phosphate、CO₂、NH₃** | 核酸分解釋出的**游離鹼基、nucleoside** |
| 成本 | 耗能、步驟多（purine 約 11 個酵素）      | 一個酵素一步完成、省能                 |
| 佔比 | 約 10%                                   | **約 90%**（細胞大部分走 salvage）     |

- 游離的 guanine、adenine、thymine、cytosine、uracil **都不是 de novo 的中間產物**。
- **Purine 環在 ribose 上一次接一兩個原子慢慢蓋出來**；**pyrimidine 先做成 orotate 環，再接到 ribose phosphate 上**。
- **PRPP（5-phospho-α-D-ribosyl-1-pyrophosphate）**：**ribose-5-phosphate（來自 PPP）+ ATP →（PRPP synthetase，又稱 ribose phosphate pyrophosphokinase）→ C1 接上焦磷酸**。**De novo（purine、pyrimidine）與 salvage 都要用 PRPP**；PRPP 的 ribose 結構會保留在最終的核苷酸裡。
- 環原子來源：
  - **Purine：glycine、aspartate、glutamine** + CO₂ + N¹⁰-formyl-THF（兩個碳）。
  - **Pyrimidine：aspartate + carbamoyl phosphate**（由 glutamine、CO₂ 來）。
  - 兩者都用 Gln、Asp；**purine 多一個 glycine**。**Asparagine、serine 都不參與**。

<div data-fig="ring-sources"></div>

## 3. Purine de novo 合成 ⭐⭐⭐

- 百十四共筆：老師說 PRPP → IMP 這段**主要記有哪些分子參與，酵素不用記**；**IMP → AMP／GMP 那張圖很常考，可以整張記下來**。
- 在 **PRPP 的 C1** 上一步步蓋環，第一個有完整 purine 環的產物是 **IMP（inosinate）**；酵素組成多功能複合體 **purinosome**（metabolon），中間產物在裡面傳遞、不外漏（例如不穩定的 5-phosphoribosylamine）。
- **第一個 committed step**：**glutamine-PRPP amidotransferase** 把 Gln 的胺基接到 PRPP 的 C1 → **5-phosphoribosylamine（PRA）**（feedback 的主要標的）。
- 接著依序加入 **glycine**（GAR synthetase，花 ATP）→ **N¹⁰-formyl-THF**（第一個碳）→ **glutamine** → 閉環成五元 imidazole 環 **AIR** → 加 CO₂（**真核一步 AIR carboxylase**；細菌、真菌兩步，且**不需要 biotin**，直接用 HCO₃⁻）→ **aspartate**（SAICAR，脫 fumarate）→ **N¹⁰-formyl-THF**（最後一個碳）→ 第二次閉環 → **IMP**。
- **IMP → AMP、GMP**（交叉使用能量，讓兩者平衡）：
  | 產物 | 第一步 | 第二步 | 能量 |
  |---|---|---|---|
  | **AMP** | IMP + **aspartate** →（**adenylosuccinate synthetase**）→ adenylosuccinate | adenylosuccinate lyase 脫 **fumarate** → AMP | **GTP** |
  | **GMP** | IMP →（**IMP dehydrogenase**，NAD⁺）→ **XMP（xanthylate）** | XMP-glutamine amidotransferase 接上 **glutamine** 的胺基 → GMP | **ATP** |

### Purine 合成的 feedback 調控（四個機制）

|     | 調控步驟                                       | 抑制劑            | 酵素                                |
| --- | ---------------------------------------------- | ----------------- | ----------------------------------- |
| ①   | PRPP → 5-phosphoribosylamine                   | **AMP、GMP、IMP** | **Glutamine-PRPP amidotransferase** |
| ②   | IMP → AMP                                      | **AMP**           | Adenylosuccinate synthetase         |
| ②   | IMP → GMP                                      | **GMP**           | **IMP dehydrogenase**               |
| ③   | IMP → AMP 需要 **GTP**；IMP → GMP 需要 **ATP** | 交叉供能          | 同上                                |
| ④   | Ribose-5-P → PRPP                              | **ADP**（及 GDP） | **PRPP synthetase**                 |

## 4. Pyrimidine de novo 合成 ⭐⭐

- **Carbamoyl phosphate**：
  - 動物做 pyrimidine 用的是**細胞質的 CPS II**（以 glutamine 為氮源）；尿素循環用的是**粒線體的 CPS I**。
  - 細菌只有一個 CPS，同時供應 arginine 與 pyrimidine；三個活性位點沿著約 100 Å 的通道排列（channeling）。
- 步驟：carbamoyl phosphate + **aspartate** →（**aspartate transcarbamoylase, ATCase**，第一個 committed step）→ N-carbamoylaspartate →（dihydroorotase，脫水閉環）→ dihydroorotate →（dihydroorotate dehydrogenase，NAD⁺）→ **orotate** →（**orotate phosphoribosyltransferase** 接上 **PRPP**）→ **orotidylate（OMP）** →（decarboxylase 脫 CO₂）→ **UMP** →（kinase）→ **UTP** →（**CTP synthetase**，Gln 提供胺基、耗一個 ATP）→ **CTP**。
- **真核**：前三個酵素（CPS II、ATCase、dihydroorotase）在同一條多功能蛋白 **CAD** 上。
- **調控（細菌）**：**ATCase 被終產物 CTP 抑制、ATP 解除抑制**。催化次單元結合受質、調節次單元結合 CTP；CTP 結合 → 構形改變傳到催化次單元 → 失活。

## 5. NMP → NDP → NTP

- **Adenylate kinase**：AMP + ATP → 2 ADP；ADP 再由糖解或氧化磷酸化變回 ATP。
- **NMP kinases**（各鹼基專一）：NMP + ATP → NDP + ADP。
- **NDP kinase**（不挑鹼基）：NDP + N′TP → NTP + N′DP；磷酸的供給者幾乎都是 **ATP**（有氧時濃度最高）。

## 6. Ribonucleotide reductase 與 dTMP ⭐⭐⭐

- **Deoxyribonucleotide 由 ribonucleotide 在 C2′ 直接還原而來**；受質是 **NDP（二磷酸）**：**ADP、GDP、CDP、UDP 四種由同一個酵素處理**，**沒有 TDP**。
- **結構（E. coli 與多數真核）**：**α₂β₂**；α₂ 是催化次單元，提供活性位點的**兩個 –SH**；β₂ 產生自由基，含**穩定的 tyrosyl radical（Tyr122）**與**雙核鐵（Fe³⁺）**輔因子。活性位點在 α、β 交界，兩邊可以同時工作。
- **電子來源**：NADPH → **thioredoxin reductase → thioredoxin**；或 **glutathione → glutaredoxin**。用來把反應後形成雙硫鍵的兩個 –SH 還原回來。
- 三種 RNR：**Class I（E. coli）需要 O₂** 再生 tyrosyl radical；Class II 用 **5′-deoxyadenosylcobalamin**（不是鐵）；Class III 在厭氧環境。
- **調控**：每個 α 次單元有兩種調節位點。
  | 位點 | 結合 | 效果 |
  |---|---|---|
  | **Activity（primary regulation）site** | **ATP → 活化**；**dATP → 抑制** | 整體開關；dATP 會讓酵素寡聚成環（E. coli αβ 交錯環、酵母 α₆β₆），自由基傳遞路徑被打斷 |
  | **Substrate specificity site** | ATP 或 dATP | 促進 **UDP、CDP** 還原 |
  | | **dTTP** | 促進 **GDP** 還原 |
  | | **dGTP** | 促進 **ADP** 還原 |
  - 百十四共筆另寫出抑制的一面：**dGTP** 促進 ADP、**抑制 CDP、UDP、GDP**；**dTTP** 促進 GDP、**抑制 CDP、UDP**；primary site 結合 **ATP 時 α、β 合併（開）**，結合 **dATP 時 α、β 分開或形成八聚體（關）**。反應機制（–SH 接電子形成 S–S，再由 glutaredoxin／thioredoxin 還原）老師說**看過即可、不太會考**。
  - 設計目的是讓四種 dNTP 平衡：pyrimidine dNTP 太多 → dTTP 高 → 轉向還原 GDP → dGTP 高 → 轉向 ADP → **dATP 高就把整個酵素關掉**。
- **dTMP（thymidylate）合成**：DNA 用 T 不用 U，T 的 de novo 路徑只走 deoxyribonucleotide。
  1. dCTP 去胺（deaminase）或 dUDP 磷酸化 → **dUTP** →（**dUTPase**）→ **dUMP**。
  2. **dUMP →（thymidylate synthase）→ dTMP**：甲基來自 **N⁵,N¹⁰-methylene-THF**，同時 THF 被氧化成 **DHF**（THF 反應中少見）。
  3. **DHF →（dihydrofolate reductase, DHFR，NADPH）→ THF** →（serine hydroxymethyltransferase）→ 回到 methylene-THF。
  - 植物與部分原生生物的 thymidylate synthase 和 DHFR 在同一條雙功能蛋白上。
  - **Thymidylate synthase 與 DHFR 是細胞合成 thymine 的唯一路徑** → 抗癌藥的重要標的。
  - 百十四共筆：老師強調 **thymidylate synthase 很重要**、**DHFR 要記住**；**dUMP 是 dTMP 的直接前驅物（immediate precursor）**，DNA 裡看得到 T 看不到 U，就是因為原料要先到 dUMP、去氧之後再甲基化成 dTMP。沒有 DHFR → DHF 無法回到 THF → 甲基來源斷絕 → dTMP 停擺。

<div data-fig="dtmp-cycle"></div>

## 7. 核苷酸分解 ⭐⭐

- **Purine → 尿酸**：
  - **AMP** →（**5′-nucleotidase** 去磷酸）→ adenosine →（**adenosine deaminase, ADA** 去胺）→ **inosine** →（水解）→ **hypoxanthine** + ribose →（**xanthine oxidase**）→ **xanthine** →（xanthine oxidase）→ **uric acid**。
  - **GMP** → guanosine → **guanine** →（**guanine deaminase**）→ **xanthine** → **uric acid**。
  - **人類終產物是尿酸**；多數哺乳類再由 **urate oxidase** 分解成 **allantoin**，其他生物再往下分解。
- **Pyrimidine → 尿素**：產生 **NH₄⁺**（進尿素循環）與 CO₂，水溶性好、不會堆積。百十四共筆：單環容易完全拆解、產物可溶，所以**沒有像痛風那樣的結晶性代謝疾病**。
  - **Cytosine** 去胺 → uracil → **β-alanine** → **acetyl-CoA**。
  - **Thymine** → **β-aminoisobutyrate** → **succinyl-CoA**（進 TCA）；尿中可測到 β-aminoisobutyrate。

## 8. Salvage pathway 與相關疾病 ⭐⭐⭐

- 游離鹼基 + **PRPP** → 核苷酸 + PPi（**phosphoribosyltransferase, PRT**）：
  - **Adenine →（APRT, adenine phosphoribosyltransferase）→ AMP**
  - **Guanine → GMP**、**hypoxanthine → IMP**：都由 **HGPRT（hypoxanthine-guanine phosphoribosyltransferase）**。
  - HGPRT **不參與 pyrimidine salvage**；**inosine（nucleoside）不是 PRT 的受質**。
- **Lesch-Nyhan syndrome**：**HGPRT 先天完全缺乏**、**X-linked**（幾乎都是男孩）、約 2 歲發病；協調差、智能障礙、極度易怒、**咬手指、腳趾、嘴唇的自殘行為**。機轉：hypoxanthine、guanine 無法回收 → **PRPP 堆積 → de novo 大量合成 purine → 尿酸過高**、類痛風組織傷害；腦特別依賴 salvage → 神經症狀。
- **ADA 缺乏 → 嚴重複合型免疫缺乏（SCID，俗稱泡泡男孩症）**：T、B 淋巴球無法正常發育。機轉：adenosine／deoxyadenosine 堆積 → 細胞內 **dATP 上升約 100 倍 → 結合 RNR 的 primary regulation site、全面關閉 RNR** → 無法生成 dCTP、dGTP、dTTP → 最需要頻繁複製 DNA 的淋巴球無法發育。（不是 dATP 不足、和 allopurinol 治療無關）百十四共筆：老師補充 **CRISPR-Cas9 基因編輯**修復缺陷基因是這類先天代謝缺陷的潛在治療方向。

<div data-fig="purine-degradation"></div>

## 9. 痛風與 allopurinol ⭐⭐⭐

- **痛風（gout）**：血液與組織**尿酸過高** → **尿酸鈉結晶**沉積在關節（發炎、疼痛）與**腎小管**。
- 造成尿酸過多的酵素異常（三個常考）：
  | 異常 | 機轉 |
  |---|---|
  | **PRPP synthetase 活性過高**（不受 ADP、GDP feedback 抑制） | PRPP 過多 → purine 合成過多 → 尿酸↑ |
  | **HGPRT 部分缺乏** | 無法回收 hypoxanthine、guanine → 只能分解成尿酸；PRPP 堆積再推動 de novo |
  | **Glucose-6-phosphatase 缺乏**（von Gierke） | G6P 無法變 glucose → 改走 **PPP** → ribose-5-P → **PRPP** ↑ |
  - **ADA 缺乏不會造成痛風**。
- 治療（飲食控制加藥物最有效）：避開富含核苷酸、核酸的食物（百十四共筆：**肝臟等內臟、部分海鮮、啤酒、大量紅肉**）+ 藥物 **allopurinol**。
- **Allopurinol**：**hypoxanthine 類似物**（環上 N、C 位置互換）、**xanthine oxidase 的受質** → 被轉成 **oxypurinol（alloxanthine）** → 緊密結合在**還原態**酵素的活性位點使其失活。排出的 purine 代謝物變成 **xanthine 與 hypoxanthine**，比尿酸好溶、不易結晶。
  - 由 Gertrude Elion 與 George Hitchings 開發（1988 諾貝爾獎），兩人也開發了 **acyclovir** 與化療用的 purine analog。
  - 非洲錐蟲沒有 de novo 核苷酸合成、只靠 salvage → allopurinol 等 purine analog 有治療潛力。

## 10. 抗代謝藥物 ⭐⭐⭐

- 癌細胞需要大量核苷酸，對核苷酸合成抑制劑比正常細胞敏感；所有**快速生長的細胞**（細菌、原生生物）都可以是標的。

| 藥物                                             | 標的                                   | 重點                                                                                                                                |
| ------------------------------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **5-Fluorouracil（5-FU）**、5-fluorodeoxyuridine | **thymidylate synthase**               | 本身不是抑制劑（**prodrug**）：經 salvage 轉成 **FdUMP**（C5 多一個 F）→ 與酵素卡死、**mechanism-based inactivation（自殺性抑制）** |
| **Methotrexate**                                 | **DHFR**（人）                         | folate 類似物、**競爭性抑制**；親和力約為 DHF 的 **100 倍**                                                                         |
| **Aminopterin**                                  | DHFR                                   | 作用同 methotrexate                                                                                                                 |
| **Trimethoprim**                                 | **細菌 DHFR**                          | 結合細菌酵素比哺乳類好約 **100,000 倍**；治療泌尿道、中耳炎（Hitchings、Elion 開發）                                                |
| Pemetrexed（Alimta）、Tomudex、Thymitaq          | thymidylate synthase（葉酸輔酶類似物） | 百十三共筆補充                                                                                                                      |
| **AZT（zidovudine）**、ddC、ddI、3TC、d4T        | **HIV 反轉錄酶**                       | **nucleoside analog、prodrug**（在 T 細胞內磷酸化成三磷酸）；**缺 3′-OH → 鏈終止**                                                  |
| **Acyclovir、ganciclovir**、araA（vidarabine）   | 病毒 DNA polymerase                    | 先被**病毒（HSV）thymidine kinase** 磷酸化 → 只在感染細胞活化                                                                       |
| araC（cytarabine）                               | 癌細胞 DNA polymerase                  |                                                                                                                                     |
| 6-Mercaptopurine、6-thioguanine、formycin B      | Salvage 的 PRT                         | purine analog                                                                                                                       |
| **Allopurinol**                                  | **xanthine oxidase**                   | 痛風                                                                                                                                |

## 百十三共筆對照

- **化療與抗病毒藥分類表**：百十三共筆（參考百十一共筆）列了 AZT 系列（ddC、ddI、3TC、d4T）、抗 HSV（acyclovir、ganciclovir、araA）、araC、葉酸類似物（pemetrexed、Tomudex、Thymitaq）、purine analog（6-MP、6-thioguanine、formycin B），並註明「老師上課未提及」；百十四共筆的藥物段只寫 **5-FU／5-FdUrd** 與 **methotrexate、aminopterin、trimethoprim** 兩類。上表其餘藥物來自 slides p41–45 與百十三共筆。
- **IMP 合成的記憶重點**、**AMP／GMP 圖常考**、**RNR 三種位點**（activity、primary regulation、substrate specificity）：兩屆共筆寫法相同。
- **PRPP synthetase 的 feedback**：兩屆共筆的調控表都只寫 **ADP**；痛風段落兩屆都寫 ADP、GDP 皆有負回饋。

=== slides ===

# 上課重點（鄭嘉雄，Lehninger-pob8-ch22）

> 講義「生物化學第22章-Nucleotide Metabolism講義」（檔名 Lehninger-pob8-ch22.pdf，68 頁）與錄影「Lehninger-pob8-ch22」（89 分）都在 **11/2** 上架，錄影沒有附逐字稿，本站用 whisper 自行轉錄。錄影檔的伺服器日期是 2025/12，是老師在課前放上的影片；今年 11/5 的錄影上架後再對照更新。

## 📑 slides 重點

| 頁     | 內容                                  | 重點                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------ | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| p2     | 核苷酸的功能                          | DNA／RNA 原料、能量（ATP、GTP）、輔因子（NAD、FAD、SAM、CoA）、UDP-glucose、CDP-diacylglycerol、cAMP／cGMP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| p3–5   | De novo vs salvage；環原子來源        | 游離鹼基不是 de novo 中間產物；**PRPP 兩條路都用**；pyrimidine：Asp、Gln；purine：**Gly**、Asp、Gln                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| p6–13  | Purine de novo（Fig. 22-35）          | 第一步 **Gln 的胺基接到 PRPP C1**；**AIR carboxylase 不需要 biotin**；步驟 6、7 只在細菌、真菌；第一個完整 purine 環 = **IMP**；多功能蛋白、metabolon                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| p14    | IMP → AMP、GMP                        | AMP 用 Asp + **GTP**；GMP 經 XMP、用 Gln + **ATP**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| p15–16 | Purine feedback 四機制                | ① **glutamine-PRPP amidotransferase** ② AMP 抑制 adenylosuccinate synthetase、GMP 抑制 IMP dehydrogenase ③ GTP／ATP 交叉需求 ④ **ribose phosphate pyrophosphokinase（PRPP synthetase）**                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| p17–20 | Pyrimidine de novo                    | **CPS II（細胞質）** vs CPS I（粒線體、尿素）；**ATCase** 是 committed step；真核 **CAD** 三功能蛋白；orotate + PRPP → OMP → UMP → UTP → CTP（cytidylate synthetase）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| p21    | ATCase 調控                           | **CTP 抑制、ATP 解除**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| p22    | NMP → NTP                             | adenylate kinase、NMP kinases、**NDP kinase**（供體幾乎都是 ATP）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| p23–29 | Ribonucleotide reductase              | α₂β₂、tyrosyl radical、Fe³⁺；thioredoxin、glutaredoxin；三種 class；**activity site（ATP 開、dATP 關）**、**specificity site（ATP／dATP → UDP、CDP；dTTP → GDP；dGTP → ADP）**；dATP 使酵素寡聚成環                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| p30–31 | dTMP                                  | dCTP 去胺／dUDP → dUTP →（dUTPase）→ dUMP → **thymidylate synthase**（methylene-THF）→ dTMP；**DHFR** 再生 THF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| p32–36 | 分解                                  | AMP → adenosine →（**ADA**）→ inosine → hypoxanthine → xanthine → **尿酸**（xanthine oxidase）；GMP → guanine →（guanine deaminase）→ xanthine；ADA 缺乏 → **dATP 增加 100 倍** → SCID；其他脊椎動物 urate oxidase → allantoin；pyrimidine → NH₄⁺、尿素；**T → succinyl-CoA**、C／U → acetyl-CoA                                                                                                                                                                                                                                                                                                                                                                 |
| p37–38 | Salvage、Lesch-Nyhan                  | **APRT**（adenine）、**HGPRT**（hypoxanthine、guanine）；Lesch-Nyhan：男孩、2 歲、自殘、PRPP 堆積 → 尿酸過多；腦依賴 salvage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| p39–40 | 痛風、allopurinol                     | 尿酸鈉結晶（關節、腎小管）；避開肝臟、腺體類食物；allopurinol → **oxypurinol** 抑制 xanthine oxidase；排出 xanthine、hypoxanthine（Elion、Hitchings，1988 諾貝爾獎）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| p41–45 | 化療藥                                | **5-FU → FdUMP**（mechanism-based inactivation）；**methotrexate** 競爭性抑制 DHFR（親和力 100 倍）、aminopterin；**trimethoprim** 對細菌 DHFR 好 10 萬倍；錐蟲只靠 salvage → allopurinol 類藥物                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| p46    | Summary                               | purine 逐步蓋環、pyrimidine 先成環；嚴格調控；分解產物不同；salvage 回收；代謝異常疾病；化療標的                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| p48–68 | **國考題**（91–112 年醫、牙、營、技） | 出現最多的是：de novo purine 胺基酸（Gly、Gln、Asp，**不含 Asn、Ser**）、**RNR 受質（UDP 等 NDP；TDP、GMP、ATP 都不是）**、HGPRT（不參與 pyrimidine salvage）、**inosine 不是 salvage 酵素受質**、痛風相關酵素（**PRPP synthetase**）、**PRPP 是 de novo 與 salvage 共用**、ADA 缺乏 → 嚴重免疫疾病、ATCase 被 **CTP** 抑制、**thymine → β-aminoisobutyrate → succinyl-CoA**、**dATP 抑制 RNR**、5-FU 要先變 **5-FdUMP**、methotrexate → **DHFR**、thymidylate synthase：**dUMP → dTMP**、**AZT 抑制反轉錄酶**（T 淋巴球 DNA 聚合酶對 AZT-TP 親和力**不高**）、**HSV thymidine kinase–ganciclovir**、IMP → AMP 的能量是 **GTP**、去氧位置是 **2′-OH**（不是 3′） |

## 🎙️ 上課錄影重點（鄭嘉雄，Lehninger-pob8-ch22，89 分）

- **核苷酸結構先搞懂**：看到 DNA、RNA 上的 ATCG，腦中要浮現「鹼基 + 五碳糖 + 磷酸」的 P–S–P–S 骨架。聚合原料一定要是**三磷酸**（NTP／dNTP），因為 5′ 三磷酸要和鏈末端的 3′–OH 連結並脫掉兩個 P；所以整章 de novo、salvage 的目的，都是做出三磷酸核苷酸。
- **細胞大部分走 salvage**：de novo 從胺基酸一個一個組，要十幾個酵素、很耗能；mRNA 用完拆開後鹼基都一樣，直接回收比較快。
- **PRPP 為什麼重要**：ribose-5-P 的 C1 是 –OH 無法反應，PRPP synthetase 從 ATP 接上兩個磷酸後，鹼基就能接到 C1 上。**De novo（purine 在 PRPP 上蓋環、pyrimidine 把 orotate 接上 PRPP）和 salvage 都要靠它**。
- **Purine 和 pyrimidine 環的胺基酸差一個 glycine**：pyrimidine 只有 Asp + Gln（藏在 carbamoyl phosphate 裡），purine 多一個 Gly。
- **IMP 之前那十幾個酵素都不用記**（「老師不會考」）；**IMP → AMP、GMP 那兩條要記**：AMP 用 **GTP**、GMP 用 **ATP**，「這考試有考過」，而且是 feedback 的標的。
- **Purine feedback 那張圖「考試也是常考，把它記起來」**：GMP 抑制 IMP → XMP、AMP 抑制 IMP → adenylosuccinate；再多就一起抑制 **glutamine-PRPP amidotransferase**；最後抑制 PRPP 的合成，一層一層控制。
- **Pyrimidine 中間的酵素不用記，只記 ATCase**：它是 feedback 標的，被終產物 **CTP** 抑制、**ATP** 可以逆轉（酵素那章講過）。
- **RNR 受質是二磷酸（NDP）**：「這考試很常考」，ADP、GDP、CDP、UDP 四種，三磷酸、單磷酸都不行；路徑裡沒有 T，所以不會有 TDP。反應機制（自由基、–SH 變雙硫鍵）「看一下就好，不用背」。
- **RNR 像一台電視**：ATP、dATP 是開關（**ATP 開、dATP 關**）；specificity site 選台（ATP、dATP、dGTP、dTTP 四種）。specificity 那張表「可能要硬背，找不到口訣」；至少一定要知道**開是 ATP、關是 dATP**，因為後面 ADA 缺乏的疾病會用到。
- **Thymidylate synthase 只做一件事：把甲基加到 dUMP 的 C5**，但它控制了 dTTP → DNA 複製 → 細胞分裂，所以和 **DHFR** 都是設計藥物的重點標的。
- **ADA 要「打勾框起來」**：adenosine 和 deoxyadenosine 都要靠 ADA 去胺才能往下分解；ADA 異常 → deoxyadenosine 堆積 → **dATP 大量產生 → 把 RNR 關掉** → 沒有 DNA 原料 → 免疫細胞無法複製 → 免疫缺乏。
- **痛風什麼時候發作**：體內尿酸本來就高，再吃大量 purine 食物就超過發病濃度，所以病人要控制飲食。人類 purine 只代謝到尿酸，不像其他生物分解成氨（氨有毒）。
- **造成尿酸過高的三個原因「考試常考」**：① **HGPRT 異常**（身體約 90% 走 salvage，回收不了就只能變尿酸；累積的 PRPP 又推動 de novo，更惡化）② **PRPP synthetase 異常**、不受 feedback 抑制 ③ **glucose-6-phosphatase 缺乏**（G6P 卡住 → 走 PPP → ribose-5-P → PRPP）。HGPRT 先天異常 = **Lesch-Nyhan**。
- **Allopurinol 的產物要選兩個**：hypoxanthine 的類似物（N、C 互換），被 xanthine oxidase 轉成 oxypurinol 後抑制酵素。A 的分解停在 **hypoxanthine**、G 的分解停在 **xanthine** → 題目問吃 allopurinol 後的產物，「不是只有 xanthine，也不是只有 hypoxanthine」，兩個都有。老師提醒：「老師講的可能都是會考的，老師喜歡考重點。」
- **Pyrimidine 分解**：C 去胺變 U → acetyl-CoA；T → succinyl-CoA；胺基走尿素循環，「就比較沒有問題」。
- **5-FU**：FdUMP 的 C5 多一個 F，甲基接上後切不開 → 酵素被卡死而失活。Methotrexate 等三個藥對 DHFR 親和力比正常受質高，所以酵素先抓藥物。

> ⚠️ 錄影的兩個口誤：講 salvage 時說「APRT 認 hypoxanthine 跟 guanine」，應該是 **HGPRT**（APRT 認 adenine）；講藥物親和力時說「Km 值比較高」，親和力高應該是 **Km 較低**。考試照 slides 與上面的整理。

=== exam ===

# 考點分析

## 🔥 高頻考點（百十三共筆 Ch22，47 題）

1. **Ribonucleotide reductase**（約 7 題）：一個酵素還原四種 NDP；**dATP 抑制**；TDP、dADP 不是受質。
2. **dTMP 合成**（約 6 題）：thymidylate synthase + **5,10-methylene-THF** + DHFR；thymidine kinase 不需要。
3. **藥物標的**（約 10 題）：5-FU → thymidylate synthase；methotrexate、aminopterin、trimethoprim → DHFR；AZT → 反轉錄酶、prodrug；ganciclovir → HSV thymidine kinase；allopurinol → xanthine oxidase。
4. **痛風、Lesch-Nyhan、SCID**（約 10 題）：哪個酵素缺乏、會不會造成痛風、SCID 是 dATP 抑制 RNR。
5. **Purine 環的原料**：glycine、glutamine、aspartate；**asparagine 不是**；IMP 是第一個 purine 核苷酸、purinosome。
6. **ATCase／CTP synthetase** 是 pyrimidine 最受調控的酵素。

## 📝 出題模式

- 「Which is incorrect」敘述題多，選項常把**藥物與標的**、**疾病與酵素**錯配。
- 有一題結構圖題（PRPP 結構，本站未收錄）、一題答案 X（SCID 敘述皆錯）。

## 🎙️ 老師課堂提示

- **一定要記**：IMP → AMP（**GTP**）、IMP → GMP（**ATP**）；purine 三層 feedback 圖；ATCase 被 **CTP** 抑制、ATP 逆轉；**RNR 受質是 NDP**；**RNR 開 = ATP、關 = dATP**；ADA 缺乏 → dATP → 關掉 RNR → 免疫缺乏；痛風三原因（HGPRT、PRPP synthetase、G6Pase）；allopurinol 後的產物是 **hypoxanthine + xanthine**。
- **可能要硬背**：RNR specificity site 表（ATP／dATP → UDP、CDP；dTTP → GDP；dGTP → ADP）。
- **不用背**：IMP 之前十幾個酵素、pyrimidine 路徑中除 ATCase 外的酵素、RNR 的自由基反應機制。
- 細節與原話見「上課重點」的 🎙️ 上課錄影重點。

## ⚠️ 陷阱整理

| 容易選錯                                                              | 正確                                                                                                 |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| ✗ Asparagine 是 purine 環的原料                                       | ✓ Purine 環原料：**glycine、glutamine、aspartate**、CO₂、N¹⁰-formyl-THF；**不是 asparagine**         |
| ✗ 第一個 purine 核苷酸是 AMP                                          | ✓ 第一個是 **IMP**（再分支成 AMP、GMP）                                                              |
| ✗ Purine 先做鹼基再接 ribose                                          | ✓ Purine **在 PRPP 上一步步長出環**；pyrimidine 才先做 orotate 環再接 PRPP                           |
| ✗ CPS I 做 pyrimidine                                                 | ✓ **CPS II（細胞質）** 做 pyrimidine；CPS I（粒線體）走尿素循環                                      |
| ✗ Ribonucleotide reductase 每種 NDP 各有一個酵素                      | ✓ **一個酵素還原四種 NDP**；**dATP** 是整體抑制劑                                                    |
| ✗ dTMP 的甲基來自 SAM                                                 | ✓ 來自 **N⁵,N¹⁰-methylene-THF**（thymidylate synthase）→ DHF 再由 **DHFR** 還原                      |
| ✗ Thymidine kinase 是 de novo dTMP 合成必需                           | ✓ Thymidine kinase 屬 **salvage**；de novo 是 dUMP → dTMP                                            |
| ✗ 5-FU 抑制 DHFR                                                      | ✓ **5-FU（FdUMP）→ thymidylate synthase**；methotrexate、aminopterin、**trimethoprim（細菌）→ DHFR** |
| ✗ Allopurinol 抑制 HGPRT                                              | ✓ Allopurinol 抑制 **xanthine oxidase**                                                              |
| ✗ 吃 allopurinol 後 purine 只會停在 hypoxanthine（或只停在 xanthine） | ✓ A 的分解停在 **hypoxanthine**、G 的分解停在 **xanthine**，兩者都會排出                             |
| ✗ IMP → AMP 用 ATP                                                    | ✓ IMP → AMP 用 **GTP**；IMP → GMP 用 **ATP**                                                         |
| ✗ RNR 的受質是 NTP 或 NMP                                             | ✓ 受質是 **NDP**（ADP、GDP、CDP、UDP）；**TDP 不是**                                                 |
| ✗ 去氧的位置是 3′-OH                                                  | ✓ 去氧的位置是 **2′**（3′-OH 是延長鏈用的）                                                          |
| ✗ Lesch-Nyhan 缺 APRT                                                 | ✓ Lesch-Nyhan = **HGPRT** 缺乏 → 尿酸↑、自殘行為                                                     |
| ✗ SCID（ADA 缺乏）是 dATP 抑制 DNA polymerase                         | ✓ **dATP 堆積 → 抑制 ribonucleotide reductase**                                                      |
| ✗ AZT 是核苷酸類似物、直接有活性                                      | ✓ AZT 是 **nucleoside analog、prodrug**（需磷酸化）→ 抑制**反轉錄酶**                                |
| ✗ Ganciclovir 被人類 thymidine kinase 活化                            | ✓ 被 **病毒（HSV／CMV）的 kinase** 活化，所以選擇性作用在感染細胞                                    |
