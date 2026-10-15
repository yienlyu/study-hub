#!/usr/bin/env python3
"""流病圖片 → subjects/epidemiology/figures/（slides 裁切 webp）＋ figures.json

slides 來源：slides/epidemiology/ 的四份上課講義 PDF（整頁）。
手繪 SVG 放在 subjects/epidemiology/figures/<id>.svg，這裡只寫說明。
需要 pymupdf 與 Pillow。執行：python3 tools/build_epi_figures.py（在 repo 根目錄）
"""
import io, json, os
import fitz
from PIL import Image

SRC = "slides/epidemiology"
ROOT = "subjects/epidemiology"
OUT = f"{ROOT}/figures/slides"
W = 1400
INTRO = "20260911_Intro_OverviewDesEpi_Student.pdf"
TRANS = "The Dynamics of Disease Transmission 2026.pdf"
MORB = "Measuring the occurence of disease_Morbidityn_Print (1).pdf"
MORT = "4. Measuring the occurence of disease_Mortality_N.pdf"
DECK = {INTRO: "0911 Overview & Descriptive Epidemiology", TRANS: "Dynamics of Disease Transmission",
        MORB: "Measuring the Occurrence of Disease I：Morbidity", MORT: "Measuring the Occurrence of Disease II：Mortality"}


def crop(pdf, page, box=(0, 0, 1, 1)):
    p = fitz.open(f"{SRC}/{pdf}")[page - 1]
    r = p.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    z = max(2.0, 2 * W / clip.width)
    im = Image.open(io.BytesIO(p.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip).tobytes("png"))).convert("RGB")
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    return im


def svg(id, ch, title, topics, kw, cap):
    assert os.path.exists(f"{ROOT}/figures/{id}.svg"), id
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap)


def slide(id, ch, title, topics, kw, cap, src, page, box=(0, 0, 1, 1)):
    name = id.removeprefix("slide-")
    im = crop(src, page, box)
    os.makedirs(OUT, exist_ok=True)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=80, method=6)
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap,
                type="slide", src=f"figures/slides/{name}.webp", deck=DECK[src], page=str(page), w=im.width, h=im.height)


F = [
 # ---------------- 概論
 slide("slide-epi-transition", "intro", "流行病學轉變：美國十大死因 1900 → 2020", ["流行病學轉變"],
       "epidemiologic transition leading causes of death infectious chronic disease 1900 2010 2020",
       "1900 年前幾名是<strong>肺炎、結核、腸胃炎</strong>等傳染病；之後換成<strong>心臟病、癌症</strong>等慢性病（2020 年 COVID-19 又擠進前段）。", INTRO, 18),
 slide("slide-prevention", "intro", "疾病自然史與三段預防", ["三段預防"],
       "primary secondary tertiary prevention natural history screening detectable preclinical",
       "<strong>初段</strong>：生物學起點之前（健康的人，疫苗、減少危險因子）；<strong>次段</strong>：可偵測但無症狀時（篩檢、早期治療）；<strong>三段</strong>：發病後減少失能與併發症（復健）。", INTRO, 22),
 slide("slide-research-spectrum", "intro", "研究光譜：基礎研究、流行病學、臨床醫學", ["研究光譜"],
       "research spectrum basic research epidemiologic studies clinical medicine randomized observational",
       "流行病學研究的對象是<strong>人類族群</strong>，多為<strong>觀察性</strong>（自我選擇的暴露），推論<strong>因果</strong>但要處理多重因子；基礎研究在細胞動物上隨機操作。", INTRO, 26),
 slide("slide-snow-cholera", "intro", "John Snow 與 1854 倫敦霍亂", ["經典案例"],
       "John Snow cholera Broad Street pump spot map Soho water supply",
       "Snow 把死亡個案點在地圖上（spot map），發現集中在 <strong>Broad Street 水泵</strong>附近，並比較不同自來水公司住戶的死亡率 → 現代流行病學之父。", INTRO, 38),
 slide("slide-blackfoot", "intro", "台灣西南沿海烏腳病", ["經典案例"],
       "blackfoot disease arsenic artesian well southwest Taiwan endemic",
       "1950–60 年代嘉南沿海的地方病：飲用<strong>含砷深井水</strong>造成周邊血管病變、乾性壞疽。台灣描述性流行病學的經典例子。", INTRO, 39),
 # ---------------- 傳播動力學
 slide("slide-triad", "transmission", "流行病學三角", ["流行病學三角"],
       "epidemiologic triad host agent environment vector",
       "宿主（host）、病原（agent）、環境（environment）三者交互作用，<strong>病媒（vector）</strong>在中間連接。", TRANS, 7),
 svg("infectivity", "transmission", "感染力、致病力、毒性：分母一層一層往下", ["病原特性"],
     "infectivity pathogenicity virulence case fatality subclinical inapparent infection",
     "感染力 = 感染 ÷ 易感受者；致病力 = 發病 ÷ 感染；毒性（致死率）= 死亡 ÷ 發病。<strong>受到感染不一定會發病</strong>。"),
 slide("slide-iceberg", "transmission", "冰山概念：看得到的只是臨床病例", ["冰山概念"],
       "iceberg concept clinical subclinical infection cell response host response",
       "水面上是<strong>臨床疾病</strong>（典型、重症、死亡）；水面下是<strong>不顯性感染、帶原</strong>。只靠臨床通報會低估感染規模。", TRANS, 13),
 slide("slide-infection-classes", "transmission", "三種感染嚴重度分布", ["病原特性"],
       "class A tuberculosis inapparent class B measles class C rabies fatal",
       "<strong>A 結核</strong>：多為不顯性感染；<strong>B 麻疹</strong>：多為臨床病例、死亡少；<strong>C 狂犬病</strong>：感染幾乎都致死。", TRANS, 14),
 slide("slide-endemic-epidemic", "transmission", "Endemic vs Epidemic", ["流行型態"],
       "endemic epidemic pandemic normal expectancy epidemic curve",
       "<strong>Endemic</strong>：平常就存在的基準量；<strong>Epidemic</strong>：明顯超過<strong>正常預期</strong>；<strong>Pandemic</strong>：全球大流行。", TRANS, 17),
 slide("slide-point-source", "transmission", "點源爆發的流行曲線", ["流行曲線"],
       "point source outbreak epidemic curve single exposure incubation period",
       "共同來源、<strong>一次暴露</strong>：曲線<strong>陡升緩降</strong>，所有病例落在一個潛伏期之內。", TRANS, 27),
 slide("slide-propagated", "transmission", "連鎖傳播的流行曲線", ["流行曲線"],
       "propagated outbreak person to person multiple waves",
       "人傳人：<strong>一波接一波</strong>、間隔約一個潛伏期，持續時間比共同來源久，峰值越來越高。", TRANS, 29),
 slide("slide-cruise", "transmission", "郵輪腸胃炎爆發（諾羅病毒）", ["流行曲線"],
       "cruise ship norovirus acute gastroenteritis outbreak epidemic curve passengers crew",
       "2002 年 14 天郵輪：旅客與船員的急性腸胃炎病例依發病日期畫成流行曲線（Gordis Fig 2-8）。", TRANS, 30),
 svg("herd-threshold", "transmission", "群體免疫閾值與 R₀", ["集體免疫力"],
     "herd immunity threshold R0 basic reproduction number Rt measles influenza COVID",
     "<strong>HIT = 1 − 1/R₀</strong>：R₀ 越大，需要免疫的比例越高（麻疹 92–94%、流感 23%）。<strong>Rt 持續 &lt; 1</strong> 代表疫情受控。"),
 slide("slide-herd-polio", "transmission", "群體免疫：小兒麻痺的預期 vs 實際病例", ["集體免疫力"],
       "herd immunity paralytic poliomyelitis expected observed 1958 1961",
       "美國 1958–61 年小兒麻痺：實際病例比只依疫苗接種者推算的<strong>預期</strong>還少 → 沒打疫苗的人也受到保護。", TRANS, 36),
 slide("slide-sars-hk", "transmission", "2003 香港 SARS 流行曲線", ["流行曲線"],
       "SARS Hong Kong 2003 epidemic curve Amoy Gardens superspreading",
       "依感染場所分色：三月底<strong>淘大花園</strong>的群聚造成尖峰，其餘是社區與醫院內傳播。", TRANS, 38),
 slide("slide-incubation", "transmission", "潛伏期分布：沙門氏菌食物中毒", ["潛伏期"],
       "incubation period distribution Salmonella typhimurium right skewed log normal",
       "191 位與會者的潛伏期：<strong>右偏分布</strong>，大多數在一兩天內發病，少數拖很久（Gordis Fig 2-11）。", TRANS, 41),
 slide("slide-food-attack", "transmission", "食物別侵襲率表", ["侵襲率"],
       "food specific attack rate table outbreak investigation egg salad",
       "1974 年 Dade County 監獄鏈球菌爆發：<strong>蛋沙拉三明治</strong>吃的人 77.9%、沒吃的 37.0%，差距最大 → 最可疑（飲料 67.8% vs 44.0%）。", TRANS, 44),
 # ---------------- Morbidity
 slide("slide-natural-history-data", "morbidity", "疾病自然史與資料來源", ["疾病自然史與資料來源"],
       "natural history disease onset symptoms seek care diagnosis treatment sources of data interviews physician records hospital",
       "同一個病人從發病、出現症狀、就醫、診斷到治療，每一段能留下的資料不同：訪談、醫師紀錄、住院紀錄抓到的人越來越少。", MORB, 8),
 slide("slide-person-years", "morbidity", "人年（person-years）怎麼算", ["發生密度"],
       "person years person time incidence density follow up",
       "5 個人各追蹤 5 年 = <strong>25 人年</strong>；每個人觀察多久就貢獻多少人時，中途發病、失訪就停止計算。", MORB, 14),
 slide("slide-new-cases", "morbidity", "找出真正的新個案", ["發生率"],
       "incidence new cases baseline screening prevalent cases follow up one year",
       "先在基線篩掉<strong>已經有病的人（盛行個案）</strong>，只追蹤沒病的人，一年後新發生的才是<strong>新個案</strong>。", MORB, 18),
 slide("slide-inc-prev-example", "morbidity", "發生率與盛行率計算例", ["盛行率"],
       "incidence prevalence example period prevalence point prevalence died cured",
       "每條線是一個病人的病程：一年內新發生的算發生率；某時間點仍在病中的算點盛行率，一整年內曾經有病的算期間盛行率。", MORB, 25),
 slide("slide-flask-in", "morbidity", "盛行率燒瓶：發生率 ↑ → 盛行率 ↑", ["發生率與盛行率的關係"],
       "prevalence pool flask incidence inflow",
       "燒瓶裡的水是<strong>盛行個案</strong>，倒進來的是<strong>新發生</strong>；進來的速度變快，瓶裡就變多。", MORB, 28),
 slide("slide-flask-out", "morbidity", "盛行率燒瓶：死亡、治癒流出", ["發生率與盛行率的關係"],
       "prevalence flask deaths cures outflow duration",
       "死亡或治癒都會讓個案流出 → <strong>盛行率 ≈ 發生率 × 病程</strong>：慢性難治（糖尿病）盛行率高；短期可治（感冒）盛行率低。", MORB, 30),
 # ---------------- Mortality
 svg("rate-denominators", "mortality", "死亡率、致死率、比例死亡：差在分母", ["死亡率", "致死率", "比例死亡"],
     "mortality rate case fatality proportionate mortality denominator",
     "同樣 18 人死於 X 病：除以全體人口 → <strong>死亡率</strong>；除以 X 病人 → <strong>致死率</strong>；除以所有死亡 → <strong>比例死亡</strong>（比例，不是率）。"),
 slide("slide-ypll", "mortality", "YPLL 的算法", ["YPLL"],
       "years of potential life lost YPLL predetermined age 75",
       "預定年齡（例 75 歲）減去死亡年齡，再全部加總：嬰兒死亡貢獻 74 年、50 歲死亡貢獻 25 年 → <strong>強調早死</strong>。", MORT, 21),
 slide("slide-thyroid", "mortality", "甲狀腺癌：發生率上升，死亡率不變", ["甲狀腺癌"],
       "thyroid cancer incidence mortality overdiagnosis ultrasound papillary",
       "發生率一路上升、死亡率幾乎持平 → 多半是<strong>診斷技術進步</strong>抓到更多小的乳突癌（過度診斷），不是真的變多。", MORT, 33),
 slide("slide-icd-change", "mortality", "ICD 改版造成的死亡率斷層", ["死亡證明與 ICD"],
       "ICD 7 ICD 8 coding change diabetes death rate artifact",
       "糖尿病死亡率在 ICD-7 → ICD-8 時突然下降：<strong>編碼規則改了</strong>，不是疾病真的減少（人為的變化）。", MORT, 39),
 svg("age-adjust", "mortality", "直接法 vs 間接法（SMR）", ["年齡校正"],
     "direct age adjustment standard population indirect standardized mortality ratio SMR expected deaths",
     "<strong>直接法</strong>：自己的年齡別率 × 標準人口；<strong>間接法</strong>：標準族群的年齡別率 × 自己的人數 → 預期死亡數，<strong>SMR = 觀察 ÷ 預期</strong>。"),
 slide("slide-direct-adjust", "mortality", "直接法計算例", ["年齡校正"],
       "direct age adjustment hypothetical example standard population expected deaths",
       "把兩個時期各年齡層的死亡率套到同一個標準人口，加總預期死亡數後再比較（Gordis Table 4.8）。", MORT, 46),
 slide("slide-smr", "mortality", "SMR 計算例", ["年齡校正"],
       "standardized mortality ratio SMR white workers expected observed",
       "各年齡層人數 × 標準族群的年齡別死亡率 = 預期死亡數；觀察死亡數 ÷ 預期死亡數 = SMR（Gordis Table 4.10）。", MORT, 49),
 slide("slide-daly", "mortality", "DALY：早死＋失能", ["其他疾病衝擊指標"],
       "DALY disability adjusted life years YLL YLD",
       "<strong>DALY = 早死損失的年數＋失能狀態下的年數</strong>；1 DALY = 損失 1 年健康生活。", MORT, 55),
 # ---------------- 篩檢
 svg("two-by-two", "screening", "篩檢的二乘二表", ["效度", "預測值"],
     "sensitivity specificity PPV NPV true positive false positive false negative true negative 2x2 table",
     "<strong>直的看</strong>（Se = a/(a+c)、Sp = d/(b+d)）是檢驗本身的特性；<strong>橫的看</strong>（PPV = a/(a+b)、NPV = d/(c+d)）受盛行率影響。"),
 svg("cutoff", "screening", "切點怎麼選：敏感度與特異度的取捨", ["效度"],
     "cut point cutoff sensitivity specificity trade off overlapping distribution blood glucose",
     "降低切點 → <strong>敏感度 ↑、特異度 ↓</strong>；提高切點 → 相反。兩群人的分布重疊，不可能同時 100%。"),
 svg("multi-testing", "screening", "序列篩檢 vs 平行篩檢", ["多重測試"],
     "sequential two-stage simultaneous parallel testing net sensitivity net specificity",
     "<strong>序列</strong>：兩次都陽性才算 → 淨 Se ↓、淨 Sp ↑；<strong>平行</strong>：任一陽性就算 → 淨 Se ↑、淨 Sp ↓。"),
 svg("ppv-prevalence", "screening", "PPV 隨盛行率變化", ["預測值"],
     "positive predictive value prevalence Hemoccult specificity rare disease",
     "盛行率 1% 時，Se = Sp = 80% 的檢驗 PPV 只有 <strong>3.9%</strong>；疾病罕見時特異度最關鍵。"),
 svg("validity-reliability", "screening", "效度與信度：打靶圖", ["效度與信度的關係"],
     "validity reliability accuracy precision target",
     "<strong>效度</strong>是準不準（離靶心多遠），<strong>信度</strong>是穩不穩（點多集中）：集中但偏離靶心 = 信度高、效度低。"),
 # ---------------- 預後
 svg("km-curve", "prognosis", "Kaplan-Meier 存活曲線", ["Kaplan-Meier 法", "生命表法"],
     "Kaplan-Meier survival curve censored median survival cumulative survival life table",
     "有人死亡才重算，累積存活率 = 各時間點存活率連乘：7/8 × 6/7 × 5/6 × 2/3 = <strong>0.417</strong>。設限者不算死亡，但之後退出分母。"),
 svg("lead-time", "prognosis", "Lead time bias 與 Will Rogers 現象", ["影響預後分析的因素"],
     "lead time bias screening survival stage migration Will Rogers phenomenon",
     "篩檢讓診斷提早，<strong>存活看起來變長但死亡時間沒變</strong>；新診斷工具造成分期遷移，兩期存活率都上升。"),
 # ---------------- RCT
 svg("rct-flow", "rct", "隨機臨床試驗流程與 NNT", ["RCT 設計", "結果的呈現"],
     "randomized controlled trial randomization blinding concurrent control intention to treat ARR RRR NNT compliance",
     "隨機（防選擇偏差）＋盲性（防測量偏差）＋同期對照（防時間偏差）；依原分組分析，<strong>NNT = 1 ÷ ARR</strong>。"),
 svg("trial-designs", "rct", "交叉試驗、因子型設計與新藥分期", ["RCT 的變形", "新藥試驗分期"],
     "crossover washout carryover factorial design aspirin beta carotene phase 1 2 3 4",
     "交叉試驗要停藥並注意<strong>殘餘效應</strong>；因子型一次看兩個主效果與<strong>交互作用</strong>；Phase 3 完成可上市，Phase 4 是上市後監測。"),
]

json.dump(F, open(f"{ROOT}/figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"{ROOT}/figures.json", "a").write("\n")
print(len(F), "figures,", sum(1 for f in F if f.get("type") == "slide"), "slide crops")
