#!/usr/bin/env python3
"""流病考古題：114、110、109 期中考古（百十三資料）→ subjects/epidemiology/data/questions-kaogu.json

來源：slides/epidemiology/共筆考古/3. 百十三資料/考古/期中/pdf/
答案依各份考古的簡答表；詳解為重新整理。題目需要原圖的標為 imageOnly（不進練習）。
執行：python3 tools/build_epi_kaogu.py（在 repo 根目錄）
"""
import json, os

OUT = "subjects/epidemiology/data/questions-kaogu.json"
S114, S110, S109 = "114 期中考古", "110 期中考古", "109 期中考古"
PAT_OK, PAT_NG, PAT_CALC, PAT_READ, PAT_FILL = (
    "選正確／單一概念題", "選錯誤／否定題", "計算題", "判讀題", "填充題")
Q = []


def mcq(qid, src, num, ch, stem, opts, ans, exp, topics, pattern=PAT_OK, image=False):
    q = {"id": qid, "source": src, "num": num, "chapter": ch, "type": "mcq", "stem": stem,
         "options": [{"k": k, "t": t} for k, t in zip("ABCDE", opts)], "answer": [ans],
         "explain": exp, "topics": topics, "pattern": pattern}
    if image:
        q["imageOnly"] = True
    Q.append(q)


def short(qid, src, num, ch, stem, ans, exp, topics, pattern=PAT_FILL):
    Q.append({"id": qid, "source": src, "num": num, "chapter": ch, "type": "short", "stem": stem,
              "options": [], "answer": [ans], "answerText": ans, "explain": exp,
              "topics": topics, "pattern": pattern})


# ---------------------------------------------------------------- 114 期中（陳偉仁等）
k = "k114-"
mcq(k + "01", S114, 1, "intro", "In the definition of epidemiology, the terms “distribution” and “determinants” together refer to:",
    ["Knowledge, attitudes, and practices related to health", "Frequency, patterns, and causes of health events",
     "The natural history of disease and its prevention", "Dissemination of information to those who need to know",
     "Public health services"], "B",
    "Distribution 是健康事件的頻率與模式（person／time／place），determinants 是造成這些事件的原因。",
    ["流行病學定義"])
mcq(k + "02", S114, 2, "intro", "Which of the following statements regarding the three levels and five stages of preventive medicine in the COVID-19 pandemic is CORRECT?",
    ["Wearing masks in the general population belongs to the first level of primary prevention, health promotion.",
     "Vaccination in the general population belongs to the first level of primary prevention, health promotion.",
     "Screening high-risk communities using throat swabs among asymptomatic individuals belongs to secondary prevention.",
     "Prescribing Remdesivir for patients who have been diagnosed with COVID-19 belongs to secondary prevention.",
     "Screening and treatment for people who have obvious COVID-19 symptoms belong to secondary prevention."], "C",
    "對無症狀者篩檢屬於次段預防（早期發現）。戴口罩、接種疫苗是初段預防的「特殊保護」，不是健康促進；已確診者給藥是治療，有明顯症狀者已不是篩檢對象。",
    ["三段預防"])
mcq(k + "03", S114, 3, "intro", "Which of the following is the primary difference between a clinical approach and an epidemiologic approach?",
    ["Clinical research quantifies the magnitude of the biological basis of disease, which has little relevance to the epidemiologic approach.",
     "The epidemiologic approach examines disease occurrence among populations, whereas the clinical approach examines disease occurrence among individuals.",
     "The epidemiologic approach describes specific signs and symptoms and prescribes individual treatment, whereas clinical observations assess the causality between symptoms and disease.",
     "A randomized controlled trial belongs to clinical medicine but not to the epidemiologic approach, as the intervention is conducted."], "B",
    "流行病學以族群為對象，臨床醫學以個人為對象。RCT 也是流行病學的研究設計。", ["研究光譜"])
mcq(k + "04", S114, 4, "intro", "Which of the following statements is CORRECT regarding basic and epidemiologic research?",
    ["Multiple factors need to be considered in an epidemiologic study.",
     "Both basic and epidemiologic research require random assignment.",
     "While epidemiologic studies primarily focus on human populations, animals can be used as alternatives in epidemiologic research.",
     "Both basic and epidemiologic research provide strong evidence for causal relationships.",
     "People can intentionally be exposed to toxic substances in epidemiologic research, as in basic animal research."], "A",
    "流病研究要用多變項模型同時考慮多個因子；基礎研究才是隨機分派、一兩個因子、證明因果。流病研究不能用動物替代，也不能故意讓人暴露毒物。",
    ["研究光譜"])
mcq(k + "05", S114, 5, "intro", "Which of the following studies does NOT fall within the scope of descriptive epidemiology?",
    ["Investigation of dengue infection in southern Taiwan", "Analysis of seasonal variation of enterovirus infections in children",
     "Assessment of the geographical distribution of COVID-19 cases", "Comparison of cancer incidence across countries",
     "Examination of the association between air pollution and COVID-19 in low-income areas"], "E",
    "探討暴露（空汙）與疾病的「相關」屬於分析性流行病學；其他選項是描述 person／time／place。",
    ["描述性流病"], PAT_NG)
mcq(k + "06", S114, 6, "intro", "Béjot 等人估計法國缺血性腦血管事件（CVEs）的人數，依研究期間、性別與年齡呈現（需原圖）。下列依圖的敘述何者 INCORRECT？",
    ["The number of CVE cases among men appeared stable across study periods.",
     "The number of CVE cases among women was relatively higher during 2017-2018 than in other study periods.",
     "The number of CVE cases among women was mainly driven by those aged ≥80 years, regardless of study periods.",
     "The incidence of CVEs was higher among women than among men during 2017-2018.",
     "The number of CVE cases among women was higher than among men during 2017-2018."], "D",
    "圖只呈現「人數」，沒有分母，不能推論「發生率」比較高。", ["人數 vs 率"], PAT_READ, image=True)
mcq(k + "07", S114, 7, "intro", "The figure shows the monthly time series of influenza cases and samples tested from hospital-based sentinel surveillance in Bangladesh, 2010–2019. What kinds of trends are observed by visualizing?",
    ["Trends for secular and place", "Trends for age and seasonal", "Trends for secular and seasonal",
     "Trends for secular and place", "Trends for secular and age"], "C",
    "10 年的逐月資料：可以看長期趨勢（secular）與季節性（seasonal），沒有地點或年齡的資訊。", ["描述性流病：Time"], PAT_READ)
mcq(k + "08", S114, 8, "intro", "Blackfoot disease is a peripheral vascular disorder that primarily affects the feet. It occurred during 1950–1960 in the coastal area of Taiwan and was limited to certain specific communities. What type of disease best describes Blackfoot disease?",
    ["Pandemic disease", "Endemic disease", "Vector-borne disease", "Infectious disease", "Blood-borne infectious disease"], "B",
    "烏腳病侷限在北門、學甲、布袋、義竹等地，是慢性砷中毒造成的地方性（endemic）疾病，不是傳染病。（原題寫「southeastern」，實際是西南沿海。）",
    ["經典案例"])
mcq(k + "09", S114, 9, "mortality", "在一家安養中心發生新冠肺炎群聚事件，已知該安養中心目前居住 40 名老人，這波疫情共 20 人被感染，隨後出現 4 人死亡。請問 0.1 最有可能為下列何種指標？",
    ["致死率（fatality rate）", "死亡率（mortality rate）", "發生率（incidence rate）", "侵襲率（attack rate）"], "B",
    "4 ÷ 40 = 0.1 是以全部住民為分母的死亡率。致死率 = 4/20 = 0.2；侵襲率 = 20/40 = 0.5。", ["死亡率 vs 致死率"], PAT_CALC)
mcq(k + "10", S114, 10, "morbidity", "族群中的疾病盛行率會隨著時間起伏。盛行率的起伏「不會」受到下列何項因素影響？",
    ["疾病發生率", "疾病的治癒率", "病人的存活率", "疾病篩檢工具的陽性預測值"], "D",
    "盛行率由新個案流入（發生率）與死亡、痊癒流出決定；PPV 是篩檢工具的特性，反而是受盛行率影響。", ["盛行率"], PAT_NG)
mcq(k + "11", S114, 11, "morbidity", "以下何者為計算某城市疾病發生率（incidence rate）的分母？",
    ["該城市的總人時（person-time）數", "該城市的年中人口數", "該城市風險族群之總觀察人時（person-time）數", "該城市的總人數"], "C",
    "發生密度的分母是 at risk 族群的總觀察人時；已經有病的人不能放進分母。", ["發生率"])
mcq(k + "12", S114, 12, "mortality", "下列有關年齡直接標準化死亡率（age adjusted mortality rate）的敘述，何者錯誤？",
    ["可比較不同國家的死亡風險", "可校正人口年齡結構不同所造成的干擾",
     "經過標準化後所算出來的死亡率可視為該族群真正的死亡率", "年齡直接標準化的作法可套用在發生率"], "C",
    "標準化率是套用標準人口算出的假想值，只能用來比較，不是族群真正的死亡率。", ["年齡校正"], PAT_NG)
mcq(k + "13", S114, 13, "morbidity", "有關發生率（incidence rate）與盛行率（prevalence）之敘述，下列何者正確？",
    ["發生率可透過單次調查來測量，只要確定該次測量是否為初次發現",
     "醫療技術的進步可以提升治癒率，在疾病發生率不改變的情形下，反而會使得疾病盛行率上升",
     "在疾病的病程長短固定的前提下，發生率跟盛行率之間會呈負相關",
     "發生率的計算，是由發病人數除以總人數"], "B",
    "題目的意思是醫療進步讓病人活得更久（病程延長），依 P = I × D，盛行率上升。發生率要兩次調查；病程固定時兩者正相關；分母是 at risk 的人。",
    ["P = I × D"])
mcq(k + "14", S114, 14, "mortality", "想要計算 2021 年臺灣肺腺癌死亡分率（proportionate mortality），分子是 2021 年臺灣肺腺癌死亡個案數，則其分母為下列何者？",
    ["2021 年臺灣全人口數", "2021 年臺灣死亡人口數", "2021 年臺灣有機會得到肺腺癌，但尚未罹患的人口數", "2021 年臺灣罹患肺腺癌的個案數"], "B",
    "比例死亡的分母是同期所有死亡人數。", ["比例死亡"])
mcq(k + "15", S114, 15, "morbidity", "以下關於疾病發生率（incidence）的描述，何者有誤？",
    ["計算子宮頸癌發生率時若研究一開始未將子宮切除術的個案排除會導致子宮頸癌發生率被低估",
     "發生密度（incidence density）適合使用在研究族群有失去追蹤或是死亡",
     "篩檢的推動可以使發生率下降", "發生率維持大於零，盛行率（prevalence）就會逐漸上升"], "C",
    "篩檢會找出更多病例，短期內發生率反而上升（考古答案為 C）。", ["發生率"], PAT_NG)
mcq(k + "16", S114, 16, "mortality", "有關死亡率採用年齡標準化的計算，以及比較人口老化程度差異大之不同國家年齡標準化死亡率之敘述，何者錯誤？",
    ["對於同一個國家而言，年齡標準化死亡率採用 direct age adjustment method 會隨著標準人口選擇之不同而有不同",
     "兩個國家的粗死亡率（crude mortality rate）即使相同，也無法判定其死亡風險是否相同",
     "兩國死亡率比較時，礙於人口小之國家其年齡別死亡率可能較不穩定，因此傾向採用人口多之國家的年齡別死亡率來計算標準化死亡比（SMR）",
     "兩國的粗死亡率不同，但各年齡別死亡率相同，比較時採標準族群選自第三地區之人口，兩國之直接年齡標準化死亡率不一定相同"], "D",
    "各年齡別死亡率相同時，不論標準人口選誰，直接標準化後的率一定相同。", ["年齡校正"], PAT_NG)
mcq(k + "17", S114, 17, "morbidity", "某研究者在某鄉鎮進行 50 歲以上之子宮頸癌初步調查，該鄉鎮 50 歲以上婦女有 2,600 位，其中 245 位自我報告曾罹患子宮頸癌，另有 355 位子宮已切除。追蹤此群婦女 10 年後，共有 20 名罹患子宮頸癌。追蹤期間的子宮頸癌累積發生率為何？",
    ["每千人有 7.69 人", "每千人有 8.49 人", "每千人有 10.00 人", "每千人有 118.04 人"], "C",
    "at risk = 2,600 − 245（已罹病）− 355（子宮切除）= 2,000；20 ÷ 2,000 = 每千人 10 人。", ["發生率計算"], PAT_CALC)
mcq(k + "18", S114, 18, "morbidity", "假設糖尿病的危險因子不變，但醫療治療水準提升，當糖尿病的篩檢計畫積極推動且成效斐然，該疾病之發生率與死亡率有何改變？",
    ["發生率不變，死亡率下降", "發生率上升，死亡率下降", "發生率下降，死亡率下降", "以上皆非"], "B",
    "篩檢找出更多病例 → 發生率上升；治療進步 → 死亡率下降。", ["發生率"])
mcq(k + "19", S114, 19, "morbidity", "在一項流行病學調查中，研究者觀察 100 名血清抗體為陰性的個案，一年之後其中有 30% 的人血清抗體轉成陽性。此「30%」所代表的流行病學意義為？",
    ["發生率", "盛行率", "致死率", "二次侵襲率"], "A",
    "原本都是陰性（at risk），一年後新轉陽 = 新個案 → 累積發生率。", ["發生率"])
mcq(k + "20", S114, 20, "mortality", "下列敘述何者有誤？",
    ["若死亡率排名心血管疾病在癌症之前，但以 YPLL 排名時癌症在心血管疾病之前，可推測癌症死亡族群的年齡層較輕",
     "在進行一次性的全國調查時僅可獲得疾病盛行率，但無法獲得疾病發生率",
     "若兩社區之心血管疾病死亡分率（proportionate mortality）相同，可推測此兩社區的死亡風險亦相同",
     "被動偵測（passive surveillance）具有較容易啟動調查的優勢，但缺點為資料可能較不完整，易有遺漏值"], "C",
    "比例死亡相同，總死亡率可能不同，所以死亡風險不一定相同。", ["比例死亡"], PAT_NG)
mcq(k + "21", S114, 21, "mortality", "當衛生政策規劃者想同時考量失能與早死所造成的疾病負擔，以作為後續疾病研究經費的分配，下列何者為最適合的量測指標？",
    ["YPLL（years of potential life lost）", "DALY（disability-adjusted life year）", "Mortality rate", "Case fatality rate"], "B",
    "DALY = YLL（早死）＋ YLD（失能）。YPLL 只看早死。", ["疾病負擔"])
mcq(k + "22", S114, 22, "transmission", "關於傳染病流行病學（Infectious Disease Epidemiology），下列何者正確？",
    ["研究對象僅限人類（humans only）", "病例本身不會影響他人暴露風險", "傳染病的致病原因通常未知",
     "一個病例（case）可能成為他人的暴露風險", "不涉及傳染媒介（vector or vehicles）"], "D",
    "傳染病流病的特色：一個 case 本身就是危險因子；病因通常已知；涉及人、病原與媒介。", ["傳染病流病特色"])
mcq(k + "23", S114, 23, "transmission", "下列何者為「毒性（Virulence）」的正確定義？",
    ["number infected / number susceptible", "number with clinical disease / number infected",
     "number of deaths / number with disease", "proportion immune in a population", "number exposed / total number in population"], "C",
    "Virulence（致死率）= 死亡數 ÷ 發病數。A 是 infectivity，B 是 pathogenicity。", ["病原三特性"])
mcq(k + "24", S114, 24, "transmission", "下列何者情境「無法」形成群體免疫（herd immunity）？",
    ["病原僅能在人與人間直接傳播", "病原只感染一種宿主物種", "病原具有重要的傳染窩（reservoir）",
     "感染後可產生持久免疫", "族群中免疫覆蓋率達到群體免疫閾值（threshold）"], "C",
    "有 reservoir 時病原可以躲在傳染窩伺機傳播，herd immunity 無法成立。", ["Herd immunity"], PAT_NG)
mcq(k + "25", S114, 25, "transmission", "一次餐會造成急性腸胃炎，病例在一個潛伏期內集中發生，流行曲線呈尖峰後漸降，最可能為何種疫情型態？",
    ["Propagated outbreak（連鎖感染）", "Continuous common source（持續共同來源）", "Intermittent exposure（間斷共同來源）",
     "Endemic pattern（地方性流行）", "Point source outbreak（點源共同來源）"], "E",
    "單次短暫暴露、所有病例在一個潛伏期內、快升慢降 → point source。", ["流行曲線"])
mcq(k + "26", S114, 26, "transmission", "若基本再生數（R0）= 4，則群體免疫閾值（HIT）= ？",
    ["25%", "50%", "60%", "75%", "90%"], "D", "HIT = 1 − 1/R0 = 1 − 1/4 = 75%。", ["Herd immunity"], PAT_CALC)
mcq(k + "27", S114, 27, "transmission", "關於潛伏期（incubation period）的敘述，下列何者正確？",
    ["指感染後立刻出現臨床症狀的時間", "感染後出現臨床症狀前的無症狀期間", "僅受宿主年齡影響", "與感染劑量無關", "僅見於病毒不見於細菌"], "B",
    "潛伏期是從感染到出現臨床症狀的時間，受病原複製時間、複製部位與劑量影響。", ["潛伏期"])
mcq(k + "28", S114, 28, "transmission", "「二次侵襲率（secondary attack rate）」的正確解釋為何？",
    ["所有人中發病者佔比", "初次暴露後立刻感染者比例", "暴露於 primary case 的易感者中發病比例",
     "所有進食某食物者中發病比例", "在一地持續存在疾病的程度"], "C",
    "二次侵襲率是易感受者接觸 primary case 後的發病比例（分子分母都扣掉 primary cases）。D 是 food-specific attack rate。", ["Attack rate"])
mcq(k + "30", S114, 30, "screening", "某醫院為提升糖尿病篩檢效率，將血糖陽性界值（cut-point）由 200 mg/dL 降為 100 mg/dL。若此醫院人群糖尿病盛行率高，下列最可能的結果為：",
    ["敏感度降低，特異度提高", "敏感度提高，但陽性預測值（PPV）下降", "敏感度與 PPV 皆提高",
     "特異度與 PPV 皆提高", "陰性預測值（NPV）下降"], "B",
    "切點降低 → 抓到更多病人（敏感度 ↑），但偽陽性也變多（特異度 ↓、PPV ↓）。", ["切點"])
mcq(k + "31", S114, 31, "screening", "若同一人先以低成本的 Test A 篩出陽性，再用精密的 Test B 確認。此篩檢策略最可能造成：",
    ["淨敏感度（net sensitivity）下降、淨特異度（net specificity）上升", "淨敏感度上升、淨特異度下降",
     "兩者同時上升", "兩者同時下降", "兩者不變"], "A",
    "序列篩檢：兩次都陽性才算陽性 → 淨敏感度下降、淨特異度上升。", ["序列 vs 平行"])
mcq(k + "32", S114, 32, "screening", "若對同一名患者同時使用兩種篩檢法（Test A 敏感度 80%、特異度 60%；Test B 敏感度 90%、特異度 90%），下列推論何者正確？",
    ["兩者同時使用會使淨敏感度高於 90%", "兩者同時使用可消除假陽性", "兩者同時使用將提升淨特異度至 > 90%",
     "兩者同時使用會減少淨敏感度", "兩者同時使用結果與任一單獨測試相同"], "A",
    "平行篩檢：淨敏感度 = 0.8 + 0.9 − 0.8 × 0.9 = 98%；淨特異度 = 0.6 × 0.9 = 54%。", ["序列 vs 平行"], PAT_CALC)
mcq(k + "33", S114, 33, "screening", "若一篩檢試驗的敏感度與特異度固定，當疾病盛行率由 1% 上升至 10% 時，陽性預測值（PPV）與陰性預測值（NPV）分別如何變化？",
    ["PPV 不變、NPV 上升", "PPV 上升、NPV 不變", "PPV 下降、NPV 上升", "PPV 上升、NPV 下降", "兩者皆不變"], "D",
    "盛行率上升 → PPV 上升、NPV 下降。", ["預測值"])
mcq(k + "34", S114, 34, "screening", "兩位放射科醫師各自判讀 100 張胸部 X 光片，結果一致率為 90%，但 Kappa 值僅 0.45。最合理的解釋為：",
    ["觀察者之間幾乎完全一致", "由於疾病盛行率極低，機率一致（chance agreement）較高", "Kappa 被高盛行率高估",
     "其中一位觀察者習慣性給出不同判讀，造成一致性下降", "該測試信度極佳"], "B",
    "大部分片子都是陰性時，靠機率就會很一致（Pc 很高），所以 κ = (P₀ − Pc)/(1 − Pc) 被拉低。", ["Kappa"], PAT_READ)
mcq(k + "35", S114, 35, "screening", "某新型快篩試驗在低盛行社區中敏感度 95%、特異度 95%。若陽性結果送至醫院確診時，只有 40% 被證實為真陽性。依據此現象，下列推論何者正確？",
    ["該快篩測試之敏感度實際遠低於 95%", "在低盛行族群中，PPV 會顯著下降", "提高特異度將導致 PPV 下降",
     "測試之信度（reliability）不佳", "該測試不具任何公共衛生價值"], "B",
    "40% 就是 PPV；盛行率低時，即使敏感度、特異度都高，PPV 仍會很低。提高特異度反而會提高 PPV。", ["預測值"])
mcq(k + "36", S114, 36, "rct", "研究者在規劃臨床試驗時，下面哪種技巧「不適當」？",
    ["按照事先擬定的納入排除標準來收取研究個案", "將各案隨機分派到對照組和標準治療組",
     "為了讓執行試驗者不知道個案的組別，執行時使用 single blind", "為了確認受試者是否每日使用藥物，因此要求個案作用藥紀錄"], "C",
    "single blind 只讓受試者不知道組別；要讓執行試驗者也不知道，必須用 double blind。", ["盲性"], PAT_NG)
mcq(k + "37", S114, 37, "rct", "關於隨機分派的敘述，下面何者錯誤？",
    ["可以降低指派治療組別時的選擇性誤差（selection bias）", "隨機分派只能採用 1:1 的機率進行分派",
     "無法進行隨機分派，還是能夠執行臨床試驗", "搭配盲性能讓試驗品質更佳"], "B",
    "隨機分派的機率不一定要 1:1（也有非固定機率分派）。", ["隨機分派"], PAT_NG)
mcq(k + "38", S114, 38, "rct", "使用三盲（triple-blind）設計時，下面哪種研究人員組合符合定義？",
    ["照顧醫師、藥師及護理師", "病例、對照及計畫主持醫師", "收集資料的研究護理師、測量超音波的檢查技師及判讀報告醫師",
     "病人、照顧醫師及統計分析師"], "D", "三盲 = 受試者＋施測者＋資料處理（統計分析）者。", ["盲性"])
mcq(k + "39", S114, 39, "rct", "某研究者使用交叉試驗（crossover design）研究 A 藥與 B 營養素對於保持骨質密度的效果，以下描述何者錯誤？",
    ["可以去除介入方式順序的影響", "必須考慮先進行 A 藥介入後，對於下一階段（攝取 B 營養素）的殘餘影響（residual effects）",
     "需觀察個案是否遵守藥品或營養素的遵從性（compliance）", "可以依據運動量做分層隨機分派（stratified randomization）"], "A",
    "交叉試驗反而要擔心順序與殘餘效應（carryover），所以中間要停藥；它本身不能去除順序影響。", ["交叉試驗"], PAT_NG)
mcq(k + "40", S114, 40, "rct", "下面敘述何者錯誤？",
    ["Phase 1 試驗用來測試新成分的藥理毒理", "Phase 2 試驗通常是小型試驗，用來測試藥品有效劑量",
     "Phase 3 試驗是大型試驗，用來測試藥品中長期成效及副作用", "Phase 4 試驗需要比 Phase 3 更大的樣本，完成後藥品才能上市"], "D",
    "Phase 3 完成就能上市；Phase 4 是上市後監測。", ["新藥試驗分期"], PAT_NG)
mcq(k + "41", S114, 41, "rct", "某藥學系老師想了解 Aspirin 與紅麴單獨使用或合併使用時，兩成分在凝血功能的主效果及可能的交互作用，你會建議下面哪個設計？",
    ["將個案隨機分派至 Aspirin 和紅麴兩組，獲得結果後再將兩組互換", "將個案隨機分派至 Aspirin、紅麴兩組，並進行 double blind",
     "先進行未用藥前凝血功能測量，提供 Aspirin 和紅麴給個案，並進行用藥後測量", "建立 Aspirin 和紅麴的 factorial design，並以隨機分派方式分組"], "D",
    "要同時看兩者的主效果與交互作用 → 因子型設計（factorial design）。A 是交叉試驗。", ["因子型設計"])
mcq(k + "42", S114, 42, "rct", "以下何者「不是」第三期臨床試驗的優點？",
    ["結果適合外推，因此常用於藥理研究", "隨機分派雙盲同期對照臨床試驗是最具證據力的研究設計，兼具時序性",
     "試驗設計可以同時觀察多種健康結果", "可以根據研究問題採用兩種以上介入，也可觀察特殊劑量的成效"], "A",
    "臨床試驗的限制之一就是外推性有限（考古答案 A）。", ["臨床試驗優勢與限制"], PAT_NG)
mcq(k + "43", S114, 43, "prognosis", "圖為 300 名病人手術後觀察 8 年的存活狀況（需原圖），存活中點（median survival time）會落在哪段時間內？",
    ["1–1.7 年", "2–2.4 年", "3–3.9 年", "6–6.4 年"], "C", "看存活曲線降到 50% 時對應的時間。", ["存活中位數"], PAT_READ, image=True)
T44 = ("某外科醫師收集 2015–2019 年間 461 名進行肝癌手術合併標靶治療的病人，假設所有病人都有完成追蹤：\n"
       "治療年  人數  第1年  第2年  第3年  第4年  第5年（各週年仍存活人數）\n"
       "2015    95    78    64    51    42    34\n"
       "2016    87    70    56    48    38\n"
       "2017    92    76    65    52\n"
       "2018    89    72    68\n"
       "2019    98    80\n"
       "Total  461   376   253   151    80    34\n")
short(k + "44-1", S114, 44, "prognosis", "（填充，四捨五入到小數第三位）" + T44 + "(1) 重點手術的 5 年存活率（比例，不需 life table 精準估計）？", "0.358",
      "只有 2015 年的 95 人有完整 5 年追蹤，其中 34 人存活：34 ÷ 95 = 0.358。", ["五年存活率"])
short(k + "44-2", S114, 44, "prognosis", "（填充，四捨五入到小數第三位）" + T44 + "(2) 以 life table method 計算病人第 3 年的存活機率（the probability for the 3rd year）？", "0.816",
      "第 3 年存活人數 151 ÷（第 2 年存活 253 − 沒有第 3 年紀錄的 2018 年 68 人）= 151 ÷ 185 = 0.816。", ["生命表"], PAT_CALC)
short(k + "44-3", S114, 44, "prognosis", "（填充，四捨五入到小數第三位）" + T44 + "(3) 病人存活累積滿 3 年的機率（the probability of surviving for 3 years）？", "0.569",
      "P₁ = 376/461、P₂ = 253/(376 − 80)、P₃ = 151/(253 − 68)；累乘 ≈ 0.569。", ["生命表"], PAT_CALC)
T45 = ("肝臟移植病人：\n週數  當時存活人數  當時死亡人數\n1     8     1\n2     7     1\n4     6     1\n12    3     1\n24    1     1\n")
short(k + "44-4", S114, 44, "prognosis", "（填充）" + T45 + "(4) 以 Kaplan-Meier method 算出第 1 週的病人存活率？", "0.875",
      "第 1 週 8 人中死 1 人：7/8 = 0.875。", ["Kaplan-Meier"], PAT_CALC)
short(k + "44-5", S114, 44, "prognosis", "（填充）" + T45 + "(5) 以 Kaplan-Meier method 算出病人累計到第 12 週的存活率？", "0.417",
      "7/8 × 6/7 × 5/6 × 2/3 = 0.417。", ["Kaplan-Meier"], PAT_CALC)
short(k + "44-6", S114, 44, "rct", "（填充）和只有手術的病人相比，以標靶治療輔助肝癌病人時，3 個月的惡化率由 60% 降為 40%。使用標靶治療時每減少一個惡化所需治療的病人數（NNT）為多少人？", "5",
      "NNT = 1 ÷ (0.6 − 0.4) = 5。", ["NNT"], PAT_CALC)

# ---------------------------------------------------------------- 110 期中
k = "k110-"
T110 = ("A 城市與 B 鄉鎮的年齡別人口與死亡數：\n"
        "年齡     A 人口   A 死亡   B 人口\n"
        "<40     15,000     75     1,000\n"
        "40–60   55,000  1,100     3,500\n"
        "≥60     30,000  1,500     6,000\n"
        "Total  100,000  2,675    10,500（B 鄉鎮總死亡 750 人）\n")
mcq(k + "I-1a", S110, 1, "mortality", T110 + "(1) A 城市 ≥60 歲的年齡別死亡率為？（%）", ["0.05", "5", "1.5", "0.015"], "B",
    "1,500 ÷ 30,000 = 5%。", ["年齡別死亡率"], PAT_CALC)
mcq(k + "I-1b", S110, 1, "mortality", T110 + "(2) A 城市的粗死亡率為？（%）", ["0.01", "0.03", "1.34", "2.68"], "D",
    "2,675 ÷ 100,000 ≈ 2.68%。", ["粗死亡率"], PAT_CALC)
mcq(k + "I-1c", S110, 1, "mortality", T110 + "(3) 假設 A 城市死於心臟病的人數為 535 人，該城市的心臟病死亡分率為？（%）", ["0.20", "0.63", "20.00", "63.00"], "C",
    "比例死亡 = 535 ÷ 2,675 = 20%。", ["比例死亡"], PAT_CALC)
mcq(k + "I-1d", S110, 1, "mortality", T110 + "(4) 若使用間接標準化（SMR）比較兩地區的死亡風險，SMR 的值與判斷為何？",
    ["SMR = 200，A 城市的死亡風險 < B 鄉鎮", "SMR = 200，A 城市的死亡風險 > B 鄉鎮",
     "SMR = 238，A 城市的死亡風險 < B 鄉鎮", "SMR = 50，A 城市的死亡風險 < B 鄉鎮"], "A",
    "用 A 城市的年齡別死亡率算 B 的預期死亡：1,000 × 0.5% + 3,500 × 2% + 6,000 × 5% = 5 + 70 + 300 = 375；SMR = 750 ÷ 375 = 200% → B 鄉鎮風險較高。",
    ["SMR"], PAT_CALC)
mcq(k + "I-2", S110, 2, "morbidity", "欲了解某社區老人罹患退化性關節炎的情況，以作為規劃復健中心的依據，何種測量可提供最有用的參考資料？",
    ["發生率（incidence rate）", "盛行率（prevalence rate）", "死亡率（mortality rate）", "致死率（case-fatality rate）"], "B",
    "規劃醫療資源要知道目前有多少病人 → 盛行率（疾病負擔）。", ["盛行率"])
mcq(k + "I-3", S110, 3, "mortality", "下列何者為沒有「分母」的指標？", ["潛在生命損失年數", "標準化死亡率", "累積發生率", "A 與 B"], "A",
    "YPLL 是把每個死者的（標準年齡 − 死亡年齡）加總，沒有分母。", ["YPLL"])
mcq(k + "I-4", S110, 4, "morbidity", "某藥廠研發出更有效治療高血壓的新藥，並已列為健保給付用藥。在其他與血壓相關的因素不變下，未來台灣地區高血壓的「發生率」會有什麼變化？",
    ["持續下降", "先下降，而後會再轉為上升", "先上升，而後會再轉為下降", "沒有變化"], "D",
    "發生率的分子是新個案；治療已罹病者不會改變新發病的人數。", ["發生率"])
mcq(k + "II-1", S110, 5, "transmission", "根據老師的講義內容，何者不是影響疾病傳播的要素？", ["宿主", "病原", "環境", "病媒", "以上皆有可能是"], "E",
    "宿主、病原、環境是三角，病媒有時也會加入，四者都是影響傳播的要素。", ["流行病學三角"])
mcq(k + "II-2", S110, 6, "transmission", "在傳染病爆發的調查中，繪製流行曲線（epidemic curve）會很有幫助，因為：",
    ["它有助於確定發生了什麼類型的爆發（例如單一來源、人與人之間）", "它顯示是否發生了群體免疫", "它有助於確定潛伏期中位數", "A 和 C", "A、B 和 C"], "D",
    "流行曲線可判斷爆發型態、估計潛伏期；無法直接顯示群體免疫。", ["流行曲線"])
mcq(k + "II-3", S110, 7, "transmission", "以下哪條流行曲線代表連鎖感染爆發（propagated outbreak）？（需原圖）", ["Fig A", "Fig B", "Fig C", "Fig D", "以上都不是"], "B",
    "Propagated：多波、峰值逐漸升高、間隔一個潛伏期。", ["流行曲線"], PAT_READ, image=True)
mcq(k + "II-4", S110, 8, "transmission", "Epidemic 意味著一種疾病：",
    ["發生明顯超出正常期望值", "經常性地存在於人群中", "同時影響許多國家", "表現出季節性模式", "在動物中普遍存在"], "A",
    "Epidemic = 超過正常預期；B 是 endemic；C 是 pandemic。", ["Endemic／Epidemic／Pandemic"])
mcq(k + "II-5", S110, 9, "transmission", "在女性人口佔一半的 10,000 人社區中進行子宮頸篩檢，發現有 200 名居民 HPV 陽性。HPV 的侵襲率（attack rate）是多少？",
    ["1%", "2%", "4%", "8%"], "C", "有風險的是女性 5,000 人：200 ÷ 5,000 = 4%。", ["Attack rate"], PAT_CALC)
mcq(k + "II-6", S110, 10, "transmission", "何者不是群體免疫（herd immunity）成立的條件？",
    ["疾病病原必須限制在單一宿主物種中", "具有快篩試劑和疫苗", "不能具有傳染窩", "感染必須能誘導足夠的免疫力", "傳播必須從宿主物種的一個成員直接傳播到另一個成員"], "B",
    "四個條件是 A、C、D、E；有沒有快篩試劑與群體免疫的成立無關。", ["Herd immunity"], PAT_NG)
mcq(k + "II-7", S110, 11, "transmission", "何者不是影響潛伏期的因素？",
    ["可能反映了病原充分複製所需的時間", "可能涉及病原需要在特定身體部位複製", "感染時接受的病原劑量也可能影響時間長度",
     "宿主的健康狀況", "這段期間宿主身體會有臨床症狀"], "E", "潛伏期的定義就是還沒有臨床症狀。", ["潛伏期"], PAT_NG)
T9 = ("食用兩種食物的人數與病人數（病人數／總人數）：\n"
      "             吃鮪魚     沒吃鮪魚\n"
      "吃蛋沙拉     60/75      75/100\n"
      "沒吃蛋沙拉   68/200     15/50\n")
mcq(k + "II-9", S110, 13, "transmission", T9 + "根據上表，以下哪種食物（或組合）最有可能具有傳染性？",
    ["僅蛋沙拉", "僅鮪魚", "既不是鮪魚也不是蛋沙拉", "同時吃鮪魚和蛋沙拉", "根據給定的數據無法計算"], "A",
    "吃蛋沙拉 (60+75)/(75+100) = 77%，沒吃 (68+15)/(200+50) = 33%；吃鮪魚 47%、沒吃 60%。差距大的是蛋沙拉。", ["Food-specific attack rate"], PAT_CALC)
TB = "3,000 名經切片證實為乳腺癌的女性與 6,000 名年齡和種族匹配的對照女性接受體格檢查篩檢，其中 2,460 名病例與 1,200 名對照的檢查結果呈陽性。"
mcq(k + "II-10", S110, 14, "screening", TB + "（考古詳解以 2,400 名病例陽性計算）體格檢查的敏感度為：", ["85%", "80%", "15%", "20%"], "B",
    "敏感度 = 2,400 ÷ 3,000 = 80%（若用題幹的 2,460 則為 82%，考古答案為 80%）。", ["敏感度"], PAT_CALC)
mcq(k + "II-11", S110, 15, "screening", TB + "體格檢查的特異度為：", ["85%", "80%", "15%", "20%"], "B",
    "特異度 = (6,000 − 1,200) ÷ 6,000 = 80%。", ["特異度"], PAT_CALC)
TH = ("500 名疑似聽力問題的人接受體格檢查與聽力測試，其中 300 人確實有聽力問題：\n"
      "體格檢查：有病者陽性 240、陰性 60；沒病者陽性 40、陰性 160\n"
      "聽力測試：有病者陽性 280、陰性 20；沒病者陽性 60、陰性 140\n")
mcq(k + "II-12", S110, 16, "screening", TH + "與體格檢查相比，聽力測試為：",
    ["同樣敏感性和特異性", "敏感性較好、特異性較好", "敏感性較好，特異性較差", "敏感性較差，特異性較好", "敏感性和特異性皆較差"], "C",
    "敏感度：體檢 240/300 = 80%、聽力 280/300 = 93%；特異度：體檢 160/200 = 80%、聽力 140/200 = 70%。", ["敏感度、特異度"], PAT_CALC)
mcq(k + "II-13", S110, 17, "screening", TH + "兩項測試同時進行時的淨敏感度（net sensitivity）為：", ["98.9%", "86.5%", "72%", "56%"], "A",
    "平行篩檢：0.8 + 0.933 − 0.8 × 0.933 = 98.9%。", ["序列 vs 平行"], PAT_CALC)
mcq(k + "II-14", S110, 18, "screening", "Hemoccult 試驗的敏感度和特異度皆為 80%。如果台北市結腸癌盛行率為 10/1,000，該檢測的陽性預測值是多少？",
    ["3.889%", "96.12%", "0.25%", "99.75%"], "A", "PPV = 0.8 × 0.01 ÷ (0.8 × 0.01 + 0.2 × 0.99) = 3.889%。", ["預測值"], PAT_CALC)
mcq(k + "II-15", S110, 19, "screening", "Hemoccult 陰性者不再檢查；陽性者再用 Hemoccult II 測第二個糞便樣本，兩次都陽性才轉介深入評估。這種篩選方法對淨敏感度和淨特異度有何影響？",
    ["淨敏感度和淨特異度均增加", "淨敏感度增加，淨特異度降低", "淨敏感度降低，淨特異度增加", "淨敏感度不變，淨特異度增加", "無法從數據中確定"], "C",
    "序列篩檢 → 淨敏感度下降、淨特異度上升。", ["序列 vs 平行"])
mcq(k + "II-16", S110, 20, "screening", "下列打靶圖何者代表信度差、但效度好（bad reliability but good validity）？（需原圖）", ["圖 A", "圖 B", "圖 C", "圖 D"], "B",
    "信度好 = 點集中；效度好 = 平均落在靶心。", ["效度與信度"], PAT_READ, image=True)
mcq(k + "III-1", S110, 21, "rct", "研究者在規劃臨床試驗時，下面哪種技巧「不適當」？",
    ["按照事先擬定的納入排除標準來收取研究個案", "將各案隨機分派到對照組和標準治療組",
     "為了避免執行試驗者可能產生執行上的不同，使用 single blind 讓病人不知道自己的組別", "為了確認受試者是否每日使用藥物，要求個案作用藥紀錄"], "C",
    "要避免執行者的差異，應該用 double blind。", ["盲性"], PAT_NG)
mcq(k + "III-2", S110, 22, "rct", "關於隨機分派的敘述，下面何者錯誤？",
    ["可以降低指派治療組別時的選擇性誤差", "隨機分派只能採用 1:1 的機率進行分派", "無法進行隨機分派，還是能夠執行臨床試驗", "搭配盲性讓試驗品質更佳"], "B",
    "隨機分派的機率不一定要 1:1。", ["隨機分派"], PAT_NG)
mcq(k + "III-3", S110, 23, "rct", "使用雙盲（double-blind）設計時，下面哪種組合符合定義？", ["照顧醫師及護理師", "病例及對照", "資料收集者及資料測量者", "病人及照顧醫師"], "D",
    "雙盲 = 受試者＋施測者。", ["盲性"])
mcq(k + "III-4", S110, 24, "rct", "某研究者使用交叉試驗（crossover design）研究手噴酒精與用手開門後門把上 COVID-19 病毒量，下列描述何者錯誤？",
    ["可以去除介入手段順序的影響", "須考慮先進行酒精噴灑後，對下一階段（不噴酒精）的殘餘影響", "需要依據門把材質做分層隨機分派",
     "不需觀察個案是否遵守酒精噴灑的遵從性"], "D", "交叉試驗仍然要觀察遵從性。（考古答案 D。）", ["交叉試驗"], PAT_NG)
mcq(k + "III-5", S110, 25, "rct", "某藥學系老師想了解 aspirin 與紅麴單獨或合併使用時，兩成分在凝血功能的主效果及可能的交互作用，你會建議哪個設計？",
    ["Aspirin 和紅麴的 factorial design，並以隨機分派方式分組", "將個案隨機分派至 aspirin、紅麴兩組，並進行 double blind",
     "先測未用藥前凝血功能，提供 aspirin 和紅麴後再測", "隨機分派至兩組，結果出來後再互換"], "A",
    "主效果＋交互作用 → 因子型設計。D 是預期性交叉試驗。", ["因子型設計"])
mcq(k + "III-6", S110, 26, "rct", "以下何者「不是」臨床試驗的優點？",
    ["臨床試驗結果適合外推，因此常用於藥理研究", "隨機分派雙盲同期對照試驗是最具證據力的研究設計，兼具時序性",
     "試驗設計可以同時觀察多種健康結果", "可以根據研究問題採用兩種以上介入，也可觀察特殊劑量的成效"], "D",
    "考古答案 D：臨床試驗通常只能處理一種介入。（A 的外推性也是限制，114 年同題答案為 A。）", ["臨床試驗優勢與限制"], PAT_NG)
mcq(k + "III-7", S110, 27, "rct", "下面敘述何者錯誤？",
    ["Phase 1 試驗用來測試新成分的藥理毒性", "Phase 2 試驗通常是小型試驗，用來測試藥品有效劑量",
     "Phase 3 試驗是大型試驗，用來測試藥品中長期成效及副作用", "Phase 4 試驗需要比 Phase 3 更大的樣本，完成後藥品才能上市"], "D",
    "Phase 3 完成就能上市。", ["新藥試驗分期"], PAT_NG)
mcq(k + "III-8", S110, 28, "prognosis", "圖為 300 名病人手術後觀察 2 年的存活狀況（需原圖），存活中點會落在哪個時段？",
    ["2–4.9 個月", "5–7.9 個月", "8–10.9 個月", "14–15 個月"], "C", "看存活率剩 50% 時的時間。", ["存活中位數"], PAT_READ, image=True)
TKM = "週數  存活人數  死亡人數\n1     8     1\n2     7     1\n4     6     1\n12    3     1\n24    1     1\n"
mcq(k + "III-12", S110, 29, "prognosis", TKM + "以 K-M 法算出第一週病人的存活率：", ["0.875", "0.857", "0.75", "0.667"], "A",
    "7/8 = 0.875。", ["Kaplan-Meier"], PAT_CALC)
mcq(k + "III-13", S110, 30, "prognosis", TKM + "以 K-M 法算出病人累積到第 12 週的存活率：", ["0.857", "0.75", "0.667", "0.417"], "D",
    "7/8 × 6/7 × 5/6 × 2/3 = 0.417。", ["Kaplan-Meier"], PAT_CALC)
mcq(k + "III-14", S110, 31, "rct", "和只有手術的病人相比，以標靶治療輔助肝癌病人時，3 個月的惡化率由 60% 降為 40%。每減少一個惡化所需治療的病人數為：",
    ["5", "6", "7", "8"], "A", "NNT = 1 ÷ (0.6 − 0.4) = 5。", ["NNT"], PAT_CALC)

# ---------------------------------------------------------------- 109 期中（僅存 17 題）
k = "k109-"
short(k + "01", S109, 1, "morbidity", "（計算）甲工廠 1,000 位員工，2000/1/1 C 肝篩檢有 50 位抗體陽性；2001/1/1 再次篩檢（含上次陽性者）共 60 位陽性，期間無人死亡或失去追蹤。\n(1) 2000 與 2001 年的盛行率？\n(2) 甲工廠 C 肝的發生率？",
      "(1) 5%、6%；(2) 10.53‰",
      "盛行率：50/1,000 = 5%、60/1,000 = 6%。發生率：新個案 10 人 ÷ at risk（1,000 − 50）= 10.53‰。", ["發生率計算"], PAT_CALC)
short(k + "02", S109, 2, "mortality", "（簡答）YPLL 與 DALY 的全名為？", "Years of potential life lost；Disability-adjusted life year",
      "YPLL 衡量過早死亡；DALY = YLL + YLD。", ["YPLL", "疾病負擔"], "簡答題")
mcq(k + "03", S109, 3, "transmission", "下列哪個圖形是 propagated 型疾病的流行曲線？（需原圖）", ["圖 A", "圖 B", "圖 C", "圖 D"], "C",
    "一波未平一波又起、峰值逐漸升高。", ["流行曲線"], PAT_READ, image=True)
mcq(k + "04", S109, 4, "transmission", "Endemic means that a disease…",
    ["occurs clearly in excess of normal expectancy", "is habitually present in human population",
     "affects a large number of countries simultaneously and exhibits a seasonal pattern", "is prevalent among animals"], "B",
    "Endemic = 在特定地區常態性存在（南部登革熱）。", ["Endemic／Epidemic／Pandemic"])
mcq(k + "05", S109, 5, "transmission", "Which of the following is characteristic of a single exposure, common vehicle outbreak?",
    ["Frequent secondary cases", "Increasing severity with increasing age", "Explosive",
     "Cases include both people who have been exposed and those who were not exposed", "All of the above"], "C",
    "單次共同暴露（例如食物中毒）會出現一個爆炸性的峰值，之後不再延伸。", ["流行曲線"])
short(k + "06", S109, 6, "screening", "（計算）以觸診篩檢乳癌：2,500 名切片證實的乳癌病人與 5,000 名年齡與種族配對的對照女性。觸診陽性者：病例 1,200 名、對照 1,000 名。\n(1) 敏感度？(2) 特異度？",
      "(1) 48%；(2) 80%", "敏感度 = 1,200 ÷ 2,500 = 48%；特異度 = (5,000 − 1,000) ÷ 5,000 = 80%。", ["敏感度、特異度"], PAT_CALC)
mcq(k + "07", S109, 7, "transmission", "Which of the following situation does NOT exist for herd immunity?",
    ["Disease agents must be restricted to a single host species", "Transmission must be relatively direct from one member of the host species to another",
     "Can operate on disease having a reservoir", "Must induce solid immunity", "All of above do"], "C",
    "有 reservoir 時 herd immunity 無法運作。", ["Herd immunity"], PAT_NG)
mcq(k + "08", S109, 8, "screening", "下列打靶圖何者是低效度、高信度？（需原圖）", ["圖 A", "圖 B", "圖 C", "圖 D"], "A",
    "點很集中但偏離靶心 = 信度高、效度低。", ["效度與信度"], PAT_READ, image=True)
TS = ("精神病院病人出院後的存活情況（無失去追蹤；表格依考古原樣）：\n"
      "出院年  人數  第一年  第二年  第三年\n"
      "2018    180    160    120     88\n"
      "2019    120     88     62\n"
      "2020    300    325\n"
      "total   650    573    182     88\n")
mcq(k + "09", S109, 9, "prognosis", TS + "第二年的存活率為？", ["0.88", "0.73", "0.47", "0.55"], "B",
    "第二年存活 182 ÷（第一年存活 573 − 沒有第二年紀錄的 325）= 0.73。", ["生命表"], PAT_CALC)
mcq(k + "10", S109, 10, "prognosis", TS + "第二年存活率跟第三年存活率之間的比較，以及代表的意義？",
    ["第二年存活率大於第三年存活率", "第二年存活率跟第三年存活率相等，代表出院後受到的治療沒有改變", "第二年存活率小於第三年存活率", "從題目中無法看出"], "A",
    "第二年 = 182 ÷ 248 = 0.734；第三年 = 88 ÷ (182 − 62) = 0.733。兩者幾乎相同，考古答案為 A（第二年略大）。", ["生命表"], PAT_CALC)
mcq(k + "11", S109, 11, "prognosis", TS + "活滿三年的存活率為多少？", ["0.88", "0.73", "0.47", "0.55"], "C",
    "(573/650) × [182/(573 − 325)] × [88/(182 − 62)] ≈ 0.47。", ["生命表"], PAT_CALC)
mcq(k + "12", S109, 12, "rct", "150 mg 阿司匹靈預防 3 個月腦中風的試驗中，服藥組 3 個月內中風比例 5%，未服藥組 20%。NNT 為多少？", ["5", "3", "7", "20"], "C",
    "NNT = 1 ÷ (0.20 − 0.05) = 6.67 ≈ 7。", ["NNT"], PAT_CALC)
mcq(k + "13", S109, 13, "rct", "關於隨機分派臨床試驗的優點，下面何者為非？",
    ["介入組與對照組可比性增加", "外在效度增加", "減少受試者自我選擇的機會", "無法預測下一個受試者所屬組別", "受試者的療效評估不受醫師主觀判斷的影響"], "B",
    "隨機分派提升的是內在效度，不是外在效度（外推性）。", ["隨機分派"], PAT_NG)
mcq(k + "14", S109, 14, "prognosis", "關於相對存活率（relative survival），下列何者正確？",
    ["適用於一等親", "適用於年老族群", "適用於男性", "通常是指某人群的觀察存活率與預期存活率相除的結果"], "D",
    "相對存活率 = 觀察存活率 ÷ 預期存活率。", ["相對存活率"])
mcq(k + "15", S109, 15, "screening", "下列何者會影響 PPV？", ["Sensitivity", "Specificity", "Prevalence", "All of the above"], "D",
    "PPV 同時受敏感度、特異度與盛行率影響。", ["預測值"])
mcq(k + "16", S109, 16, "rct", "下列何者「不是」臨床試驗的優點？",
    ["臨床試驗結果具外推性，常用於藥物試驗", "為最具證據力的研究設計，兼具時序及因果", "可以同時觀察多種健康結果",
     "可以根據研究設計同時有兩種以上介入，適合觀察特殊劑量"], "D", "臨床試驗通常只能處理一種介入（考古答案 D）。", ["臨床試驗優勢與限制"], PAT_NG)
mcq(k + "17", S109, 17, "prognosis", "若使用診斷時間作為預後測量的時間起點、治癒時間作為終點，下列何者錯誤？",
    ["受診斷工具影響", "受診治者影響", "受病人影響", "不適用長期觀察"], "D",
    "以診斷為起點受病人就醫時間與診斷工具影響；以治癒為終點受病人與診治者主觀影響。「不適用長期觀察」是以死亡為終點的限制。",
    ["預後起點與終點"], PAT_NG)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(OUT, len(Q), "questions;", sum(1 for q in Q if q.get("imageOnly")), "imageOnly")
