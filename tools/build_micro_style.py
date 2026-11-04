#!/usr/bin/env python3
"""Build subjects/micro-immuno/data/questions-style.json: 依各老師期中出題習慣（含 AI 輔助出題風格）寫的模擬新題。"""
import json, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else 'subjects/micro-immuno/data/questions-style.json'
POS, NEG, CLIN, PAIR, COMB = '選正確／單一概念題', '選錯誤（否定）題', '臨床情境題', '配對題', '組合選擇題'

# (teacher, chapter, pattern, topics, stem, [A,B,C,D], answer, explain)
Q = [
# ───────── 黃姿雯：中文題幹＋英文術語，「何者最適當／錯誤」，選項長度整齊（AI 輔助風格），各論常比較兩菌
('黃姿雯', 'bact-structure', POS, ['細菌構造與功能'],
 '下列細菌構造與其功能的配對，何者最適當？',
 ['莢膜（capsule）：細菌運動的主要構造', '性纖毛（sex pilus）：接合作用（conjugation）時傳遞 DNA', '內孢子（endospore）：細菌主要的繁殖方式', '質體（plasmid）：攜帶細菌存活必需的基因'],
 'B', '**Sex pilus** 用於 conjugation。A 運動靠 flagella，capsule 抗吞噬；C 一個細胞只形成一個 endospore，是**休眠求生**不是繁殖；D plasmid **可丟棄仍存活**（老師的 plasmid 判斷法）。📍 細菌構造章 構造與功能表；遺傳章 plasmid。'),
('黃姿雯', 'bact-genetics', POS, ['水平基因轉移'],
 '將熱殺死的有莢膜 Streptococcus pneumoniae 與活的無莢膜菌株混合注入小鼠後，可分離出活的有莢膜菌。此現象屬於哪一種水平基因轉移（horizontal gene transfer）？',
 ['Transduction', 'Conjugation', 'Transformation', 'Transposition'],
 'C', 'Griffith 實驗：受體菌直接吸收環境中**裸露 DNA** = **transformation**。Transduction 靠 phage、conjugation 靠 sex pilus 接觸；transposition 不是 HGT 三機制之一。📍 細菌遺傳章 HGT 三機制。'),
('黃姿雯', 'sterilization', POS, ['滅菌與消毒'],
 '醫院供應中心以高壓蒸氣滅菌鍋（autoclave）處理手術器械，下列敘述何者最適當？',
 ['常用條件約為 121°C、15 psi、20 分鐘左右', '滅菌指示膠帶變色即可證明滅菌成功', '監測用的生物指示劑為 Bacillus pumilus 孢子', '適合用來滅菌油類與粉末'],
 'A', 'Autoclave **121°C、15 psi、10–40 min（最常見 20 min）**。B 膠帶只代表「有處理過」，**只有生物指示劑能證明滅菌**；C 濕熱用 ***B. stearothermophilus***，*B. pumilus* 是輻射；D 油、粉末水蒸氣進不去 → 乾熱。📍 滅菌章 濕熱／監測。'),
('黃姿雯', 'pathogenesis', NEG, ['毒素（內/外毒素、AB toxin）'],
 '關於 A-B toxin 的敘述，下列何者錯誤？',
 ['B subunit 負責與宿主細胞表面受體結合', 'A subunit 進入細胞後發揮酵素活性', 'Diphtheria toxin 與 Pseudomonas exotoxin A 都使 EF-2 ADP-ribosylation', 'Cholera toxin 的 A subunit 使 Gs 蛋白失活，導致細胞內 cAMP 下降'],
 'D', 'Cholera toxin 使 **Gsα 持續活化** → adenylate cyclase 一直開 → **cAMP 上升** → Cl⁻、水分泌（米湯樣腹瀉）。老師點名「A-B toxin 的構造與作用流程要特別記得」。📍 致病機轉章 A-B toxin。'),
('黃姿雯', 'staph-strep', CLIN, ['S. aureus'],
 '一名 20 歲籃球員小腿擦傷後出現紅腫化膿的癤（furuncle），培養出成簇排列的 G(+) 球菌，catalase(+)、coagulase(+)，對 oxacillin 具抗藥性。下列敘述何者最適當？',
 ['抗藥性來自 mecA 基因編碼的 PBP2a，對 β-lactam 親和力低', '抗藥性主要因產生 β-lactamase，合併 clavulanate 即可治療', 'Coagulase 試驗主要用來區分 S. epidermidis 與 S. saprophyticus', '首選治療藥物為 penicillin G'],
 'A', 'MRSA：**mecA → PBP2a**，所有 β-lactam 都受影響（加 β-lactamase 抑制劑沒用）。Coagulase 是區分 ***S. aureus* vs CoNS**；epidermidis vs saprophyticus 看 **novobiocin**。📍 葡萄球菌章 MRSA／鑑別流程。'),
('黃姿雯', 'neisseria', POS, ['Neisseria'],
 '關於 Neisseria meningitidis 與 Neisseria gonorrhoeae 的比較，下列何者正確？',
 ['N. meningitidis 可分解 glucose 與 maltose，N. gonorrhoeae 只分解 glucose', 'N. gonorrhoeae 具有多醣莢膜，是疫苗的主要成分', 'N. gonorrhoeae 感染後可產生持久免疫，因其 pili 抗原穩定', '兩者皆為 oxidase 陰性的 G(−) 雙球菌'],
 'A', '醣類分解：**meningitidis = glucose + maltose（M 對 M）**；gonorrhoeae 只有 glucose。B 莢膜是 **meningitidis** 才有；C gonococcus pili **antigenic variation** → 可重複感染；D Neisseria 是 **oxidase (+)**。📍 Neisseria 章 兩菌比較表。'),

# ───────── 鍾筱菁：中文出題、菌名用英文；國考題（黃字／紅字）為主；情境＋鑑別；上課明講「我會考」的點
('鍾筱菁', 'enterobacteriaceae', CLIN, ['E. coli 致病型'],
 '一名 22 歲女大學生反覆發生膀胱炎，尿液培養出發酵 lactose 的 G(−) 桿菌。醫師建議多喝水，也可以喝蔓越莓汁。蔓越莓汁的保護作用主要是抑制此菌的哪一項致病因子？',
 ['P pili（fimbriae）黏附尿路上皮', 'Shiga toxin 抑制蛋白質合成', 'LT／ST enterotoxin 使 cAMP／cGMP 上升', 'Intimin 造成 attaching-and-effacing lesion'],
 'A', 'UPEC 造成約 **90% UTI**，靠 **P pili／fimbriae 黏附**；蔓越莓汁的花青素抑制黏附（pH 不是重點）。B 是 EHEC、C 是 ETEC、D 是 EPEC／EHEC。老師上真菌課時提到蔓越莓汁說「我才剛出過考題…有沒有太洩題？」。📍 腸桿菌科章 E. coli 致病型表、UPEC。'),
('鍾筱菁', 'neisseria', NEG, ['Vibrio'],
 '下列關於弧菌（Vibrio）屬的敘述，何者錯誤？',
 ['為 oxidase(+)，可與 oxidase(−) 的腸桿菌科區分', 'V. cholerae 在 TCBS agar 上因發酵 sucrose 呈黃色菌落', 'V. parahaemolyticus 在 TCBS agar 上因發酵 sucrose 呈黃色菌落', 'V. vulnificus 可使肝硬化病人在生食海鮮後發生敗血症'],
 'C', 'TCBS 顏色：***V. cholerae* 黃**（發酵 sucrose）、***V. parahaemolyticus* 綠**、*V. vulnificus* 藍綠（不發酵 sucrose）。老師：「從弧菌開始之後的 G(−) 菌都是 oxidase (+)」。📍 Neisseria 章（弧菌段）／腸桿菌科章 Vibrio 表。'),
('鍾筱菁', 'bacillus', CLIN, ['Listeria'],
 '一名懷孕 30 週的孕婦吃了冷藏多日的生乳起司後發燒，血液培養出 G(+) 短桿菌，25°C 下呈翻滾運動（tumbling motility）。關於此菌，下列何者正確？',
 ['可在 4°C 生長，實驗室可用冷增菌法（cold enrichment）分離', '為絕對胞外菌，主要靠抗體清除', '會產生耐熱的內孢子（endospore）', '以 Elek test 偵測其毒素'],
 'A', '*Listeria monocytogenes*：**4°C 可生長 → cold enrichment**（老師點名國考題）、tumbling motility、**胞內菌**（ActA 推動 actin，靠細胞性免疫）；不產孢子（產孢子只有 *Bacillus*、*Clostridium*）；Elek test 是白喉毒素。📍 Bacillus／Listeria 章。'),
('鍾筱菁', 'neisseria', POS, ['H. pylori／Campylobacter'],
 '下列關於 Helicobacter pylori 的敘述，何者正確？',
 ['產生大量 urease，分解尿素產生氨以中和胃酸', '主要因生食未煮熟禽肉感染，並可併發 Guillain-Barré syndrome', '為 lactose 發酵菌，在 MacConkey agar 上呈粉紅色', '為 oxidase(−)、無鞭毛的直桿菌'],
 'A', '*H. pylori*：**urease（尿素呼氣試驗）**、螺旋形、**多端叢鞭毛**、oxidase(+)。B 是 ***Campylobacter jejuni***（禽肉、GBS）——114 期中就把這兩隻混在一起考。📍 Neisseria 章（H. pylori／Campylobacter 段）。'),
('鍾筱菁', 'fungi', POS, ['真菌構造與分類'],
 '子囊菌門（Ascomycota）真菌的無性孢子與有性孢子分別為何？',
 ['Sporangiospore／zygospore', 'Conidia／ascospore', 'Conidia／basidiospore', 'Blastospore／zygospore'],
 'B', '老師原話：「請問 ascomycetes 的無性世代孢子叫什麼？conidia；有性世代？ascospore。**我會考喔**」。接合菌（毛黴門）= sporangiospore／zygospore；擔子菌 = basidiospore（幾乎沒有無性孢子）。📍 真菌章 三大菌門表。'),
('鍾筱菁', 'fungi', NEG, ['皮膚／皮下／系統性黴菌'],
 '下列雙形性（dimorphic）真菌與其組織中典型型態的配對，何者錯誤？',
 ['Histoplasma capsulatum：巨噬細胞內充滿小型酵母（魚眼樣）', 'Coccidioides immitis：內含大量內孢子的大型 spherule', 'Blastomyces dermatitidis：寬基出芽、厚壁的大型酵母', 'Paracoccidioides brasiliensis：雪茄形（cigar-shaped）酵母'],
 'D', '*Paracoccidioides* 是**多芽「船舵型」（pilot\'s wheel）**；**雪茄形酵母是 *Sporothrix schenckii***（37°C）。老師：「這四個我會考一題，每一個系都一樣」。📍 真菌章 系統性黴菌（四隻雙形性菌）。'),

# ───────── 陳玫潔：題幹偏長、英文或中英夾雜、Janeway／Abbas 題庫風格、缺陷小鼠實驗情境、表格比較、組合題
('陳玫潔', 'immuno-basic', CLIN, ['先天 vs 後天免疫'],
 'A newborn mouse undergoes thymectomy. When it reaches adulthood, which response would be MOST severely impaired?',
 ['Antibody class switching to a protein antigen (T-dependent response)', 'Alternative pathway complement activation on bacterial surfaces', 'NK cell killing of MHC class I-deficient tumor cells', 'IgM production in response to LPS (a TI-1 antigen)'],
 'A', '新生期切除胸腺（≈ nude mouse）→ 沒有成熟 T 細胞 → **T-dependent** 抗體（class switch、affinity maturation）與細胞性免疫都垮。補體、NK 屬先天；TI-1（LPS）不需 T help。📍 免疫基本概念章 nude mouse；T 細胞活化章 TD vs TI。'),
('陳玫潔', 'mhc', CLIN, ['抗原處理與呈現（TAP）'],
 'TAP1-deficient mice are infected with influenza virus. Compared with wild-type mice, which finding is expected?',
 ['Reduced surface MHC class I and few peripheral CD8⁺ T cells', 'Absence of peripheral CD4⁺ T cells', 'Failure to remove CLIP from MHC class II', 'NK cells are unable to kill virus-infected cells'],
 'A', 'TAP 把 proteasome 切好的 peptide 送進 ER；缺 TAP → MHC I 載不到 peptide、表面 MHC I 低 → **CD8 positive selection 也受損**。CLIP 移除靠 HLA-DM（class II 路徑）；MHC I 低反而讓 NK 更容易殺（missing self）。📍 MHC 章 class I 路徑。'),
('陳玫潔', 'mhc', NEG, ['MHC 構造與表現'],
 'Which comparison between MHC class I and MHC class II is INCORRECT?',
 ['Class I: α chain + β2-microglobulin; class II: α and β chains, both encoded in the MHC', 'Class I binds peptides of 8–10 aa in a closed groove; class II binds longer peptides (13–25 aa) with open ends', 'CD8 binds the α3 domain of class I; CD4 binds the β2 domain of class II', 'MHC polymorphism is generated by somatic recombination of MHC genes in each lymphocyte'],
 'D', 'MHC 多樣性是**遺傳**來的（多基因 + 多對偶、codominant），**沒有重組、沒有 allelic exclusion**（老師錄影強調）。β2m 不在 MHC 上（chr 15）。📍 MHC 章 class I vs II 表、老師課堂提示。'),
('陳玫潔', 'tcell-dev', COMB, ['T 細胞發育'],
 '下列哪些分子的缺陷，會使胸腺細胞無法通過 β-selection，停留在 double-negative（DN）階段？（1）RAG1　（2）pre-Tα（pTα）　（3）Lck　（4）AIRE　（5）CD40L',
 ['(1)(2)(3)', '(1)(4)', '(2)(3)(5)', '(1)(2)(3)(4)'],
 'A', 'β-selection 需要 **TCRβ 成功重組（RAG）+ pTα 組成 pre-TCR + 訊號（Lck）** 才能進入 DP。AIRE 管 medulla 的 **negative selection**；CD40L 是 T 細胞幫 B 細胞／macrophage。組合題是 114 期中陳老師用過的格式。📍 TCR 與 T 細胞發育章 DN→DP。'),
('陳玫潔', 'tcell-act', POS, ['白血球遷移（selectin→chemokine→integrin）'],
 'After priming in a lymph node, effector T cells leave the node and home to inflamed tissues. Which change BEST explains this?',
 ['Downregulation of CCR7 and L-selectin (CD62L), with increased LFA-1/VLA-4 and E-/P-selectin ligands', 'Upregulation of CCR7 to follow CCL19/CCL21', 'Loss of TCR expression after differentiation', 'Increased CD62L expression to bind HEV addressins'],
 'A', 'Naïve T：**CCR7 + L-selectin** → 經 HEV 進淋巴結。Effector：關掉 CCR7、CD62L，改表現 **integrin（LFA-1、VLA-4）與 selectin ligand** → 走向發炎組織的內皮。📍 T 細胞媒介免疫章 白血球遷移。'),
('陳玫潔', 'tcell-act', POS, ['共刺激（CD28/B7/CTLA-4）'],
 'Which statement about CTLA-4 (CD152) is correct?',
 ['It binds B7 (CD80/CD86) with higher affinity than CD28 and delivers an inhibitory signal; anti-CTLA-4 (ipilimumab) is used in cancer immunotherapy', 'It is expressed at high levels on naïve T cells before activation', 'It binds MHC class II to stabilize the immunological synapse', 'CTLA-4-deficient mice are profoundly immunodeficient'],
 'A', 'CTLA-4 = **煞車**，活化**後**才上調，對 B7 親和力比 CD28 高（還會把 B7 胞吞掉）；Treg 也大量表現。CTLA-4 knockout → **淋巴增生、自體免疫**致死，不是免疫缺陷。📍 TCR 章 Signal ② 共刺激表（b7-competition 圖）。'),

# ───────── 李岳倫：中文國考風格、同一概念換句話重出、課堂題原題出現機率高
('李岳倫', 'innate', POS, ['補體系統'],
 '補體替代路徑（alternative pathway）中，C3 convertase 的組成為何？',
 ['C4b2a', 'C3bBb', 'C4b2a3b', 'C3bBb3b'],
 'B', '替代路徑 C3 convertase = **C3bBb**（起始為 C3(H₂O)Bb，老師說替代路徑有兩種）；classical／lectin = **C4b2a**；C4b2a3b、C3bBb3b 是 **C5 convertase**。📍 先天免疫章 補體三路徑。'),
('李岳倫', 'innate', NEG, ['ILC 先天性淋巴細胞'],
 '下列關於先天性淋巴細胞（innate lymphoid cells, ILCs）的敘述，何者錯誤？',
 ['不表現經基因重組的抗原專一性受體', 'ILC2 分泌 IL-5、IL-13，參與對抗寄生蟲與氣喘', 'ILC1 分泌 IFN-γ，對抗病毒與胞內病原', '發育過程需要 RAG 進行 V(D)J 重組'],
 'D', 'ILC **沒有 TCR／BCR、不需 RAG**；活化不靠辨識特定抗原。老師說 ILC「何者錯誤」**曾經考過**。📍 先天免疫章 §6 ILCs。'),
('李岳倫', 'innate', NEG, ['補體系統'],
 '下列補體片段與其主要功能的配對，何者錯誤？',
 ['C3b：調理作用（opsonization）', 'C5a：嗜中性球趨化', 'C3a：過敏毒素（anaphylatoxin）', 'C4a：組成膜攻擊複合體（MAC）'],
 'D', 'MAC = **C5b、C6、C7、C8、C9**。小片段（C3a、C4a、C5a）是過敏毒素，C5a 趨化最強；大片段 C3b 調理。補體在考古同一概念出 5–10 次。📍 先天免疫章 補體功能。'),
('李岳倫', 'agab', POS, ['抗體類別與功能'],
 '下列哪一種抗體活化補體古典路徑（classical pathway）的能力最強？',
 ['IgM', 'IgA', 'IgE', 'IgD'],
 'A', '**IgM 五聚體**，一個分子就能結合 C1q 啟動 classical pathway；IgG 需要兩個相鄰分子。IgA、IgE、IgD 不活化古典路徑（老師：「IgD 我考試從來沒有考過」）。📍 抗原抗體章 抗體類別表。'),
('李岳倫', 'agab', POS, ['抗體結構'],
 '下列有關抗體分子結構的敘述，何者正確？',
 ['抗原結合部位由重鏈與輕鏈的可變區（V domain）共同構成', '補體 C1q 結合在 Fab 區', 'IgG 是分子量最大的抗體', '輕鏈分為 κ、λ、μ 三種'],
 'A', '老師點名國考考過：認抗原 = **V domain**（VH + VL）；補體結合 = **Fc**。最大的是 IgM；輕鏈只有 **κ、λ**，μ 是 IgM 的重鏈。📍 抗原抗體章 抗體結構。'),
('李岳倫', 'agab', CLIN, ['抗體類別與功能'],
 '一名從東南亞返國的旅客糞便檢出蠕蟲卵，血液嗜酸性球明顯上升。下列哪一種抗體最可能升高，並與嗜酸性球、肥大細胞共同對抗此感染？',
 ['IgE', 'IgD', 'IgM', 'IgA'],
 'A', '寄生蟲（蠕蟲）→ TH2 → IL-4 促 class switch 到 **IgE**；IgE 經 FcεRI 讓 mast cell、eosinophil 脫顆粒（ADCC）。IgA／IgE 情境是每年必出。📍 抗原抗體章 IgE；T 細胞章 TH2。'),

# ───────── 林秋烽：英文題、否定題比例高、從宿主角度看免疫脫逃、配對題
('林秋烽', 'infection-immunity', NEG, ['NET／efferocytosis'],
 'Which statement about neutrophil extracellular traps (NETs) is INCORRECT?',
 ['NETs are composed of decondensed DNA decorated with granule enzymes', 'NETs can trap and kill microbes outside the cell', 'Group A Streptococcus can escape NETs by secreting DNase', 'NET formation is immunologically silent because it never exposes self antigens'],
 'D', 'NETosis 吐出 **DNA**（核內 self antigen）→ 與**自體免疫**、敗血性休克的 **DIC** 有關；「immunologically silent」是 apoptosis／efferocytosis 的特性。GAS 用 DNase 切 NET。📍 對抗感染的免疫反應章 錄影重點（NET／NETosis）。'),
('林秋烽', 'infection-immunity', PAIR, ['Inflammasome／pyroptosis'],
 'Which pairing of caspase and its role is CORRECT?',
 ['Caspase-1: activated by the NLRP3 inflammasome, processes IL-1β/IL-18 and drives pyroptosis', 'Caspase-3: initiator caspase of the death-receptor pathway', 'Caspase-8: initiator caspase of the mitochondrial (intrinsic) pathway', 'Caspase-9: processes pro-IL-18 into its mature form'],
 'A', '**Caspase-8** = death receptor initiator；**caspase-9** = 粒線體 initiator；兩者 → **caspase-3**（executioner）→ apoptosis。**Caspase-1** ← NLRP inflammasome → IL-1β、IL-18 → **pyroptosis**（老師：「請大家一定要對 NLRP 有點印象」）。📍 對抗感染章 §4 胞內感染。'),
('林秋烽', 'infection-immunity', POS, ['免疫逃脫'],
 'Some viruses (e.g., RSV, JEV) induce SOCS proteins in infected host cells. What is the MAIN immunological consequence?',
 ['Inhibition of JAK–STAT signaling, dampening interferon responses', 'Enhanced MHC class I expression and CD8⁺ T-cell recognition', 'Direct activation of the classical complement pathway', 'Increased TLR expression and NF-κB activation'],
 'A', 'SOCS（suppressor of cytokine signaling）是 PRR／cytokine 訊號的**內生性煞車**；病原操控它 → 擋 **JAK–STAT** → IFN 作用下降。SOCS3 可由 IL-10 誘導。📍 對抗感染章 免疫脫逃（「發炎像油門、旁邊要有煞車」）。'),
('林秋烽', 'infection-immunity', POS, ['TLR／PRR'],
 'Which of the following is a damage-associated molecular pattern (DAMP) rather than a PAMP?',
 ['HMGB1', 'Lipopolysaccharide (LPS)', 'Flagellin', 'Unmethylated CpG DNA'],
 'A', '**HMGB1** 是核蛋白，平常不暴露，細胞死亡才釋出 → **內生性 DAMP**（可被 TLR2、TLR4 辨識）。LPS → TLR4、flagellin → TLR5、CpG → TLR9 都是 PAMP。📍 對抗感染章 §3 PRRs、PAMPs、DAMPs。'),
('林秋烽', 'infection-immunity', NEG, ['免疫逃脫'],
 'Which pairing of Group A Streptococcus factor and immune-evasion mechanism is INCORRECT?',
 ['M protein: binds C4b-binding protein to limit C3b opsonization', 'SpeB (cysteine protease): cleaves IgG', 'DNase: degrades neutrophil extracellular traps', 'Streptolysin: acts as a superantigen that binds MHC class II outside the groove'],
 'D', 'Streptolysin（O、S）是**殺免疫細胞的 pore-forming toxin**；superantigen 是 **SpeA／SpeC（致熱外毒素）**。M protein 抓 C4bp、SpeB 切 IgG、DNase 切 NET 都是老師講的「GAS 全套脫逃」。📍 對抗感染章 §5 免疫脫逃。'),

# ───────── 吳珊瑩：中文題幹＋英文藥名；講義 ☆☆☆（核苷類似物、藥物↔步驟表）；新冠藥機制互換
('吳珊瑩', 'viruses', PAIR, ['病毒學總論'],
 '下列抗病毒藥物與其作用的配對，何者錯誤？',
 ['Enfuvirtide（T-20）：抑制 HIV gp41 媒介的膜融合', 'Amantadine：阻斷 A 型流感病毒 M2 離子通道，抑制脫殼', 'Oseltamivir：抑制 neuraminidase，阻止新病毒釋放', 'Foscarnet：需先經病毒 thymidine kinase 磷酸化才有活性'],
 'D', '**Foscarnet** 是 pyrophosphate 類似物，**不需磷酸化**，直接抑制 herpesvirus DNA polymerase／HIV RT；需要病毒 TK 的是 **acyclovir**。📍 病毒章 §8 抗病毒藥物表。'),
('吳珊瑩', 'viruses', POS, ['病毒學總論'],
 '下列關於動物病毒複製的敘述，何者正確？',
 ['RNA 病毒大多在細胞核內複製其基因體', '(+) 單股 RNA 病毒的基因體可直接當作 mRNA 進行轉譯', '有套膜的病毒以破壞細胞膜（lysis）的方式釋出', '反轉錄病毒的 provirus 可像 prophage 一樣從染色體切出'],
 'B', '(+)ssRNA（如 picornavirus）基因體 = mRNA。A RNA 病毒多在**細胞質**、DNA 病毒在核；C 有套膜 → **出芽**，無套膜才破膜；D **provirus 永遠不離開染色體**。📍 病毒章 §6 動物病毒複製。'),
('吳珊瑩', 'viruses', POS, ['病毒學總論'],
 '關於新冠肺炎（COVID-19）的治療藥物，下列何者正確？',
 ['Paxlovid 的 nirmatrelvir 抑制病毒 main protease（Mpro），ritonavir 用來提高其血中濃度', 'Molnupiravir 可用於 12 歲以上的青少年', 'Remdesivir 是病毒 protease 抑制劑', '取得緊急使用授權（EUA）即等同取得正式藥證'],
 'A', 'Paxlovid = **protease（Mpro）抑制劑**（症狀 5 天內）；**Remdesivir、Molnupiravir 是核苷類似物**；Molnupiravir **18 歲以下禁用**；**EUA ≠ 正式核准**。114 期中同一位老師就考了新冠藥物機制互換。📍 病毒章 新冠藥物表。'),
('吳珊瑩', 'viruses', NEG, ['病毒學總論'],
 '關於病毒的培養與定量，下列敘述何者錯誤？',
 ['細胞培養中 cytopathic effect（CPE）最早的徵兆通常是細胞變圓', 'Diploid cell line 來自人類胚胎，約可繼代 100 次', 'Continuous cell line 為轉形、可無限繼代的細胞', '以溶菌斑法（plaque method）定量噬菌體時，單位為 CFU'],
 'D', 'Plaque method 的單位是 **PFU（plaque-forming units）**；CFU 是細菌菌落。114 期中就考過「250 個 plaque → 250 PFU/mL」。📍 病毒章 §4 培養與鑑定。'),
('吳珊瑩', 'viruses', CLIN, ['病毒學總論'],
 '一名骨髓移植後的免疫低下病人長期服用 acyclovir 預防 HSV 復發，後來出現抗藥性皰疹病灶。最可能的抗藥機轉為何？',
 ['病毒 thymidine kinase 或 DNA polymerase 突變', '病毒 neuraminidase 突變', '病毒 M2 離子通道突變', '宿主 thymidine kinase 表現量下降'],
 'A', 'Acyclovir 需要**病毒 TK** 第一次磷酸化、再由宿主酵素變三磷酸、作用於**病毒 DNA polymerase**（缺 3\'-OH 終止鏈）→ 抗藥 = **TK 或 DNA polymerase 突變**。可當預防性治療，但清不掉潛伏感染。📍 病毒章 核苷類似物 ☆☆☆。'),

# ───────── 賴傳穎（遠距）：英文臨床情境 → 推缺陷（think mechanistically）、感染型態對照
('賴傳穎', 'immunodeficiency', CLIN, ['抗體缺陷'],
 'A 9-month-old boy has had recurrent otitis media and pneumonia caused by S. pneumoniae and H. influenzae since 6 months of age. CD3⁺ T cells are normal, CD19⁺ B cells are nearly absent, and all immunoglobulin isotypes are very low. Which defect is MOST likely?',
 ['BTK (Bruton\'s tyrosine kinase)', 'CD40 ligand', 'IL-2 receptor common γ chain', 'NADPH oxidase (gp91phox)'],
 'A', '**XLA**：BTK 缺陷 → pre-BCR 訊號異常、**卡在 pre-B** → 沒有 B 細胞、所有抗體都低；6 個月後母體 IgG 消退才發病，反覆**有莢膜化膿菌**感染。CD40L 缺陷有 B 細胞且 IgM 正常／高。📍 免疫缺陷章 §3 抗體缺陷。'),
('賴傳穎', 'immunodeficiency', CLIN, ['補體缺陷'],
 'A 19-year-old college student is hospitalized for a second episode of meningococcal meningitis. Deficiency of which component is MOST likely?',
 ['C5–C9 (terminal complement / MAC)', 'C1 inhibitor', 'BTK', 'Perforin'],
 'A', '反覆 ***Neisseria*** 感染 → **C5–C9（MAC）缺陷**（take-home framework）。C3 缺陷是反覆化膿菌；C1、C2、C4 缺陷是 immune complex 清除差。📍 免疫缺陷章 §4 補體缺陷、§9 框架表。'),
('賴傳穎', 'immunodeficiency', CLIN, ['Cytokine 路徑缺陷'],
 'A patient has recurrent mucocutaneous candidiasis, "cold" staphylococcal skin abscesses, eczema, and markedly elevated serum IgE. Which pathway is MOST likely defective?',
 ['STAT3 signaling, impairing TH17/IL-17 responses', 'IL-12/IFN-γ axis, impairing macrophage activation', 'BTK-dependent pre-BCR signaling', 'Terminal complement (C5–C9)'],
 'A', '**Type 3（IL-17）缺陷 → 黏膜皮膚念珠菌**；代表 **STAT3 deficiency（Job／高 IgE 症候群）**。IL-12/IFN-γ 缺陷是 **Mycobacteria**。📍 免疫缺陷章 §6 Cytokine 路徑缺陷。'),
('賴傳穎', 'immunodeficiency', CLIN, ['免疫失調'],
 'A 2-year-old develops persistent high fever, hepatosplenomegaly, and pancytopenia; bone marrow shows hemophagocytosis. NK cells are present in normal numbers but fail to kill target cells. Which defect is MOST likely?',
 ['Perforin (familial hemophagocytic lymphohistiocytosis)', 'ELANE (severe congenital neutropenia)', 'CD18 (leukocyte adhesion deficiency type 1)', 'FOXN1 (thymic epithelial defect)'],
 'A', 'Perforin 缺陷 → CTL／NK 殺不掉感染細胞 → 標的細胞持續放 cytokine → **hyperinflammation、噬血** = **FHL（perforin → FHL2）**。這題是「免疫缺陷不一定是感染多，也可能是發炎太多」。📍 免疫缺陷章 §7 免疫失調與毒殺缺陷。'),
('賴傳穎', 'immunodeficiency', PAIR, ['治療'],
 'Which pairing of treatment level and example is INCORRECT?',
 ['Replace: immunoglobulin replacement for X-linked agammaglobulinemia', 'Reconstitute: hematopoietic stem cell transplantation for SCID', 'Correct: gene therapy for a single-gene defect such as ADA-SCID', 'Reconstitute: a major risk is graft-versus-host disease caused by recipient T cells attacking donor stem cells'],
 'D', 'GVHD 是**移植來的（donor）T 細胞攻擊受者組織**；受者殘存 T 細胞殺掉 donor stem cell 叫 **graft rejection**。治療三層次：Replace（Ig）、Reconstitute（HSCT）、Correct（gene therapy／CRISPR）。📍 免疫缺陷章 §8 治療三層次。'),
]

out = []
for i, (t, ch, pat, topics, stem, opts, ans, ex) in enumerate(Q, 1):
    out.append({
        'id': f'style-{i:03d}', 'source': '老師風格新題', 'chapter': ch, 'type': 'mcq',
        'stem': stem, 'options': [{'k': k, 't': o} for k, o in zip('ABCD', opts)],
        'answer': [ans], 'explain': ex + f'\n\n🧑‍🏫 依**{t}**老師期中出題習慣編寫。',
        'topics': topics, 'pattern': pat, 'teacher': t,
    })
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(OUT, 'a').write('\n')
from collections import Counter
print(len(out), Counter(q['teacher'] for q in out), Counter(q['answer'][0] for q in out))

# ── 平衡答案位置：把正解與目標位置互換，詳解中的選項字母一併對調
import re, random
rng = random.Random(1104)
targets = list('ABCD' * 10)[:len(out)]
rng.shuffle(targets)
for q, tgt in zip(out, targets):
    a = q['answer'][0]
    if a == tgt: continue
    o = {x['k']: x['t'] for x in q['options']}
    o[a], o[tgt] = o[tgt], o[a]
    q['options'] = [{'k': k, 't': o[k]} for k in 'ABCD']
    q['answer'] = [tgt]
    sw = {a: tgt, tgt: a}
    q['explain'] = re.sub(r'(^|[。；、，\n])([ABCD])(?= )', lambda m: m.group(1) + sw.get(m.group(2), m.group(2)), q['explain'])
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(OUT, 'a').write('\n')
print(Counter(q['answer'][0] for q in out))
