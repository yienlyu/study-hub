=== summary ===
# 核苷酸代謝（期中考後才上）

> ⚠️ **不在 10/30 期中考範圍。** 陳顧中老師 10/22 錄影（Ch18-3 Ch22）：「核苷酸的部分就由下一個老師來幫你講」，CPS II 也「期中考後的老師會來跟你講」。這頁保留 113 共筆的核苷酸重點與 47 題考古，給期中考後用；練習區「已上課範圍」和模擬考都不會抽到。

## 1. 核苷酸的組成
- **Nucleotide = 含氮鹼基（nucleobase）+ 五碳糖（ribose／deoxyribose）+ 磷酸**；nucleoside = 鹼基 + 糖。**沒有 glucose**。
- **PRPP（5-phosphoribosyl-1-pyrophosphate）**：**ribose-5-phosphate**（來自 PPP）+ ATP →（**PRPP synthetase**）→ PRPP（C1 上的 pyrophosphate）。是 purine、pyrimidine 合成與 salvage 的共同原料。

## 2. Purine de novo 合成 ⭐⭐
- **在 PRPP 上一步步「蓋」出 purine 環**，第一個完整產物是 **IMP（inosinate）**；10 個酵素組成 **purinosome**。
- 環上原子來源：**glycine**（C4、C5、N7）、**glutamine**（N3、N9）、**aspartate**（N1）、**N¹⁰-formyl-THF**（C2、C8）、CO₂（C6）。（**asparagine 不參與**）
- IMP → **AMP**（需 **GTP**、aspartate）；IMP → **GMP**（需 **ATP**、glutamine）——交叉需要，讓兩者平衡。
- **回饋抑制**：AMP、GMP 抑制 PRPP amidotransferase（第一步）；**GMP 抑制 IMP → GMP**（IMP dehydrogenase），AMP 抑制 IMP → AMP。

<div data-fig="ring-sources"></div>

## 3. Pyrimidine de novo 合成 ⭐
- **先做環、再接上 PRPP**：carbamoyl phosphate（**CPS II，細胞質**，用 glutamine）+ **aspartate** →（**aspartate transcarbamoylase, ATCase**）→ … → orotate + PRPP → **UMP** → UTP →（**CTP synthetase**）→ CTP。
- **ATCase** 是細菌調控最嚴密的別構酵素：**CTP 抑制、ATP 活化**。動物主要在 CPS II 調控。
- Purine 需要但 pyrimidine 不需要：**glycine**（glutamine、aspartate 兩者都用）。

## 4. Ribonucleotide reductase 與 dTMP ⭐⭐⭐
- **Ribonucleotide reductase（RNR）**：**NDP → dNDP**（ADP、GDP、CDP、UDP 都是受質；**一個酵素處理四種**），以 **tyrosyl free radical** 機制、電子來自 thioredoxin／glutaredoxin（最終 NADPH）。
  - **dATP** 結合 activity site → **抑制整體活性**；ATP 活化。Specificity site 決定還原哪一種（dATP、dTTP、dGTP 調整受質）。
  - TDP 不是受質（dTMP 由 dUMP 來）。
- **dTMP 合成**：dUMP + **N⁵,N¹⁰-methylene-THF** →（**thymidylate synthase**）→ dTMP + **DHF** →（**dihydrofolate reductase, DHFR**，NADPH）→ THF →（serine hydroxymethyltransferase）→ 回到 methylene-THF。
  - **Thymidine kinase** 屬於 salvage pathway（thymidine → dTMP），不是 de novo 必需。

<div data-fig="dtmp-cycle"></div>

## 5. 核苷酸分解與痛風 ⭐⭐
- **Purine** → hypoxanthine、guanine → **xanthine** →（**xanthine oxidase／dehydrogenase**）→ **uric acid**（人類的終產物）。
  - AMP →（AMP deaminase）→ IMP；**adenosine →（adenosine deaminase, ADA）→ inosine** → hypoxanthine。
- **Pyrimidine** → **β-alanine**（C、U）、β-aminoisobutyrate（T）→ … → **succinyl-CoA**（從 T 來）；最後是 NH₄⁺、CO₂，可溶不會堆積。
- **痛風（gout）**：尿酸過多（產生過多或排泄不足）→ 關節沉積。原因包括 **PRPP synthetase 活性過高**、**HGPRT 部分缺乏**、**glucose-6-phosphatase 缺乏**（von Gierke）。**ADA 缺乏不會造成痛風**。
- **Allopurinol**：**hypoxanthine 類似物**，**抑制 xanthine oxidase** → 尿酸 ↓（不是 xanthine 類似物）。

<div data-fig="purine-degradation"></div>

## 6. Salvage pathway 與相關疾病 ⭐⭐
- **Salvage**：把游離的鹼基回收成核苷酸：鹼基 + **PRPP** → 核苷酸 + PPi（**HGPRT** 處理 hypoxanthine、guanine；**APRT** 處理 adenine）；不需要 purinosome。
- **Lesch-Nyhan syndrome**：**HGPRT 完全缺乏**、**X-linked recessive** → 尿酸大量堆積、自殘行為、神經症狀。（PRPP synthetase 缺乏不是它的原因）
- **SCID（ADA deficiency）**：ADA 缺乏 → **dATP 堆積 → 抑制 ribonucleotide reductase** → 淋巴球無法合成 DNA → 嚴重免疫缺陷；與尿酸、xanthine dehydrogenase 無關。

## 7. 抗代謝藥物 ⭐⭐⭐
| 藥物 | 標的 | 備註 |
|---|---|---|
| **5-Fluorouracil、5-fluorodeoxyuridine** | **thymidylate synthase**（轉成 **FdUMP**，自殺性抑制） | prodrug |
| **Methotrexate、aminopterin** | **DHFR**（人） | 抗癌 |
| **Trimethoprim** | **DHFR**（細菌） | 抗菌 |
| **Pemetrexed（Alimta）** | thymidylate synthase、DHFR 等多個葉酸依賴酵素 | 抗癌 |
| **AZT（zidovudine）** | HIV **反轉錄酶**（3′-OH 被 azido 取代 → 鏈終止） | **prodrug**、nucleoside analog |
| **Acyclovir、ganciclovir** | 病毒 DNA polymerase；先被 **HSV thymidine kinase** 磷酸化 | 只在受感染細胞活化 |
| **Allopurinol** | xanthine oxidase | 痛風 |
| Ara-A（vidarabine） | 病毒 DNA polymerase | |

=== slides ===
# 上課 slides

今年還沒上，期中考後由下一位老師講。

=== exam ===
# 考點分析

## 🔥 高頻考點（113 共筆 Ch22，47 題）
1. **Ribonucleotide reductase**（約 7 題）：一個酵素還原四種 NDP；**dATP 抑制**；TDP、dADP 不是受質。
2. **dTMP 合成**（約 6 題）：thymidylate synthase + **5,10-methylene-THF** + DHFR；thymidine kinase 不需要。
3. **藥物標的**（約 10 題）：5-FU → thymidylate synthase；methotrexate、aminopterin、trimethoprim → DHFR；AZT → 反轉錄酶、prodrug；ganciclovir → HSV thymidine kinase；allopurinol → xanthine oxidase。
4. **痛風、Lesch-Nyhan、SCID**（約 10 題）：哪個酵素缺乏、會不會造成痛風、SCID 是 dATP 抑制 RNR。
5. **Purine 環的原料**：glycine、glutamine、aspartate；**asparagine 不是**；IMP 是第一個 purine 核苷酸、purinosome。
6. **ATCase／CTP synthetase** 是 pyrimidine 最受調控的酵素。

## 📝 出題模式
- 「Which is incorrect」敘述題多，選項常把**藥物與標的**、**疾病與酵素**錯配。
- 有一題結構圖題（PRPP 結構，本站未收錄）、一題答案 X（SCID 敘述皆錯）。

## ⚠️ 陷阱整理
| 容易選錯 | 正確 |
|---|---|
| Asparagine 是 purine 環的原料 | Purine 環原料：**glycine、glutamine、aspartate**、CO₂、N¹⁰-formyl-THF；**不是 asparagine** |
| 第一個 purine 核苷酸是 AMP | 第一個是 **IMP**（再分支成 AMP、GMP） |
| Purine 先做鹼基再接 ribose | Purine **在 PRPP 上一步步長出環**；pyrimidine 才先做 orotate 環再接 PRPP |
| CPS I 做 pyrimidine | **CPS II（細胞質）** 做 pyrimidine；CPS I（粒線體）走尿素循環 |
| Ribonucleotide reductase 每種 NDP 各有一個酵素 | **一個酵素還原四種 NDP**；**dATP** 是整體抑制劑 |
| dTMP 的甲基來自 SAM | 來自 **N⁵,N¹⁰-methylene-THF**（thymidylate synthase）→ DHF 再由 **DHFR** 還原 |
| Thymidine kinase 是 de novo dTMP 合成必需 | Thymidine kinase 屬 **salvage**；de novo 是 dUMP → dTMP |
| 5-FU 抑制 DHFR | **5-FU（FdUMP）→ thymidylate synthase**；methotrexate、aminopterin、**trimethoprim（細菌）→ DHFR** |
| Allopurinol 抑制 HGPRT | Allopurinol 抑制 **xanthine oxidase** |
| Lesch-Nyhan 缺 APRT | Lesch-Nyhan = **HGPRT** 缺乏 → 尿酸↑、自殘行為 |
| SCID（ADA 缺乏）是 dATP 抑制 DNA polymerase | **dATP 堆積 → 抑制 ribonucleotide reductase** |
| AZT 是核苷酸類似物、直接有活性 | AZT 是 **nucleoside analog、prodrug**（需磷酸化）→ 抑制**反轉錄酶** |
| Ganciclovir 被人類 thymidine kinase 活化 | 被 **病毒（HSV／CMV）的 kinase** 活化，所以選擇性作用在感染細胞 |
