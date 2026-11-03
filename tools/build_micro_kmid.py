#!/usr/bin/env python3
"""微免整份期中考古（106／109／110）→ subjects/micro-immuno/data/questions-kmid.json

來源：slides/micro-immuno/共筆考古/考古/期中/（百十四組長上傳區，11/1–11/2 上傳）
- 106 免疫學期中考古（答案表＋詳解，甯泰翔組）
- 109 微免期中考古（答案表＋詳解，甯泰翔組）
- 110 微免期中考古（題目為百十二版本；答案與詳解為百十四版本，郭柏辰組）

只收「期中考範圍」且題庫還沒有的題目：
- 已在題庫（百十三每週考古、111 期中、114 記題、課堂題）的同題不重收，見各卷 SKIP。
- 過敏反應、自體免疫（期中考後）、臨床課（quinsy、gas gangrene）不收。
- 無解、題目不完整、看圖題不收。
執行：python3 tools/rebuild.py tools/build_micro_kmid.py（在 repo 根目錄）
"""
import json
import re
import subprocess

DIR = "slides/micro-immuno/共筆考古/考古/期中/"
OUT = "subjects/micro-immuno/data/questions-kmid.json"
BLANK = "（原考古此選項空白）"


def parse(pdf, stop=None):
    t = subprocess.run(["pdftotext", DIR + pdf, "-"], capture_output=True, text=True, check=True).stdout
    if stop and stop in t:
        t = t[:t.find(stop)]
    qs, cur, opt = {}, None, None
    for s in (l.strip() for l in t.split("\n")):
        if not s or re.search(r"（\d+%", s):  # 109 卷的單元標題，例：腸內菌、弧菌（8%; …）
            continue
        m = re.match(r"^(\d{1,3})\s*[\.．]\s*(\S.*)$", s)
        if m and (cur is None or int(m.group(1)) > cur["num"]) and int(m.group(1)) < 200:
            cur = {"num": int(m.group(1)), "stem": m.group(2), "opts": {}}
            qs[cur["num"]] = cur
            opt = None
            continue
        if cur is None:
            continue
        parts = re.split(r"[\(（]([A-E])[\)）]", s)
        if len(parts) > 1:
            pre = parts[0].strip()
            if pre:
                if opt:
                    cur["opts"][opt] += pre
                else:
                    cur["stem"] += pre
            for i in range(1, len(parts), 2):
                opt = parts[i]
                cur["opts"][opt] = parts[i + 1].strip()
        elif opt:
            cur["opts"][opt] += (" " if re.match(r"[A-Za-z(]", s) else "") + s
        else:
            cur["stem"] += ("" if re.search(r"[一-鿿，、]$", cur["stem"]) else " ") + s
    return qs


# 題號: (章節, 主題, 答案, 詳解[, {"stem":…, "opts":{…}}])
K106 = {
    1: ("immuno-basic", "先天 vs 後天免疫", "D", "體液免疫最後都要靠 B 細胞分化成漿細胞分泌抗體。T-independent 抗原（如 LPS、多醣）可直接活化 B 細胞，不需要 helper T，所以「所有」體液免疫都必需的只有 B 細胞。"),
    2: ("immuno-basic", "細胞毒殺（perforin/Fas）", "A", "CTL 辨識 MHC I＋病毒胜肽，以 perforin／granzyme 或 FasL–Fas 誘發受感染細胞凋亡。"),
    3: ("immuno-basic", "抗原處理與呈現（TAP）", "D", "T 細胞只認得 MHC 上呈現的胜肽，所以所有 T 細胞免疫反應的啟動都需要抗原呈現細胞（APC）。"),
    4: ("immuno-basic", "先天 vs 後天免疫", "A", "初級淋巴器官＝骨髓、胸腺（淋巴球生成、成熟、篩選）；Peyer's patches、淋巴結、脾臟是次級淋巴器官。"),
    5: ("immuno-basic", "先天 vs 後天免疫", "A", "嗜中性球是數量最多的顆粒球（也是最多的白血球）。"),
    6: ("innate", "白血球遷移（selectin→chemokine→integrin）", "D", "白血球貼附第一步（tethering／rolling）是 selectin 結合醣類配體；integrin 負責之後的牢固黏附（firm adhesion）。CR3（Mac-1）是 integrin。"),
    11: ("agab", "抗體結構", "A", "IgM、IgE 沒有 hinge region（多一個 CH4 domain 取代）；有 hinge、富含 proline 的是 IgG、IgD、IgA。"),
    12: ("agab", "抗體類別與功能", "D", "在黏膜表面以分泌型（secretory）形式作用的是 IgA，不是 IgG。（人類 IgG 四個亞型都能通過胎盤，但效率不同。）"),
    13: ("agab", "抗體類別與功能", "B", "五聚體（pentamer）是 IgM 不是 IgG；IgM 結合價高，適合結合重複 epitope（病毒顆粒、紅血球）。"),
    15: ("agab", "抗體多樣性（VDJ/SHM）", "D", "抗體多樣性來源：多個 germline V 基因、V(D)J 重組、輕重鏈配對、接合處多樣性（P／N 核苷酸）、體細胞超突變。基因互換（crossing over）是減數分裂的事，不參與。"),
    25: ("tcell-act", "超級抗原", "A", "超級抗原跨接 MHC II（胜肽溝外側）與 TCR Vβ，凡是用該 Vβ 的 T 細胞都被活化（可達 5–20%），不需辨識特定胜肽 → 大量細胞激素，造成毒性休克。"),
    26: ("tcell-act", "共刺激（CD28/B7/CTLA-4）", "B", "TNF receptor 家族共刺激分子（如 OX40、4-1BB）在 T 細胞活化後期給抗凋亡訊號，延長已活化 T 細胞的存活。"),
    27: ("tcell-act", "細胞毒殺（perforin/Fas）", "E", "Perforin 在標的細胞膜上聚合成孔洞；granzyme 經孔洞進入後活化 caspase 誘發凋亡。"),
    28: ("tcell-act", "TH 分化與細胞激素", "A", "TH1 分泌 IL-2、IFN-γ，幫助 CD8⁺ T 細胞增生分化為 CTL。TH1／TH2 互相抑制，不會互相「轉換」。"),
    29: ("tcell-act", "B 細胞活化／class switch／生發中心", "A", "IFN-γ（TH1）促進轉換成調理、活化補體能力強的 IgG 亞型（人 IgG1／IgG3，小鼠 IgG2a）；IL-4 → IgE；TGF-β → IgA。"),
    31: ("infection-immunity", "第一道防線", "D", "Defensins、cathelicidin、dermcidin 等抗菌胜肽除了直接殺菌，也有趨化、調節免疫的功能，所以「只有抗菌、沒有免疫調節」是錯的。"),
    32: ("infection-immunity", "NADPH oxidase／CGD", "D", "寫反了：膜結合次單位是 gp91phox、p22phox（cytochrome b558）；細胞質次單位是 p40phox、p47phox、p67phox（加 Rac）。呼吸爆發時組裝到膜上產生 superoxide；基因缺陷造成 CGD。"),
    33: ("infection-immunity", "TLR／PRR", "E", "PRR 活化產生發炎與抗病毒干擾素反應，基本上是保護性的（過度時才致病），題目說「致病性」是錯的。"),
    34: ("infection-immunity", "免疫逃脫", "E", "(A) 阻斷 PRR 訊號 → 抑制第一型干擾素；(B) 下調 MHC I；(C) 誘導抗發炎細胞激素（如病毒 IL-10）；(D) 潛伏在細胞內。四項都正確，所以沒有錯的選項。"),
    35: ("immunodeficiency", "免疫缺陷分類", "D", "結核、皮膚／食道念珠菌、CMV 都是細胞內病原或伺機性感染，靠 T 細胞（細胞性免疫）控制 → 最可能是 T 細胞缺陷（如 AIDS）。"),
    36: ("immunodeficiency", "NADPH oxidase／CGD", "B", "CGD：吞噬細胞缺 NADPH oxidase，無法產生 ROS 殺死吞入的 catalase 陽性細菌（S. aureus）與真菌（Aspergillus），反覆感染並形成肉芽腫。"),
    37: ("mhc", "MHC 構造與表現", "A", "HLA-B27（MHC I）與僵直性脊椎炎高度相關（相對風險約 100 倍以上）。"),
}
SKIP106 = "7–10、23、24、30 已在題庫；14 與 13 題重複且題目缺漏；16–21、38 過敏反應（期中考後）；22 無解"

K109 = {
    13: ("pathogenesis", "超級抗原", "AC", "超級抗原：(A) 金黃色葡萄球菌腸毒素、(C) 化膿性鏈球菌致熱外毒素（erythrogenic toxin A）。E. coli 腸毒素（LT／ST）與霍亂毒素是一般的 A-B 毒素，升高 cAMP／cGMP 造成分泌性腹瀉。", {"multi": True}),
    14: ("pathogenesis", "感染途徑", "B", "梅毒螺旋體（Treponema pallidum）經性行為（黏膜接觸）進入人體。"),
    15: ("pathogenesis", "細菌附著", "A", "尿道致病性 E. coli 用 P fimbriae（pyelonephritis-associated pili）附著於尿路上皮的醣脂。"),
    17: ("pathogenesis", "免疫逃脫", "E", "(A) coagulase 使 fibrin 包覆、形成膿瘍隔離；(B) GAS 玻尿酸莢膜模仿結締組織；(C) N. gonorrhoeae 分泌 IgA protease；(D) pilin／Opa 抗原變異。(E) 長 O 抗原可阻擋 MAC 插入細胞膜（抗補體），但不是「抑制趨化」，所以錯。"),
    20: ("staph-strep", "S. aureus", "B", "Protein A 結合 IgG 的 Fc 端，讓抗體方向顛倒，阻止調理吞噬。", {"opts": {"C": "脂多醣（lipopolysaccharides）"}}),
    22: ("staph-strep", "S. agalactiae (GBS)", "C", "B 群鏈球菌（S. agalactiae）是新生兒敗血症、腦膜炎的主因，孕婦於 35–37 週篩檢陰道／直腸帶菌。"),
    23: ("staph-strep", "S. pyogenes (GAS)", "A", "急性風濕熱：GAS M protein 與心肌、瓣膜、關節抗原的分子相似性（molecular mimicry）→ 自體免疫。"),
    24: ("staph-strep", "S. pyogenes (GAS)", "B", "Lancefield 血清分群依細胞壁的 C-carbohydrate（群特異多醣）；M protein 用來再細分 GAS 的型別。", {"opts": {"C": BLANK}}),
    25: ("staph-strep", "S. pneumoniae", "D", "肺炎鏈球菌疫苗是用莢膜多醣（PPSV23；PCV 則是多醣接合蛋白載體），不是黏附蛋白。(A)(B)(C) 正確：α 溶血、optochin 敏感、膽汁溶解、莢膜是主要毒力因子。"),
    26: ("staph-strep", "S. aureus", "A", "G(+) 球菌、溶血、coagulase 與 catalase 陽性 → S. aureus。它會產生腸毒素、hyaluronidase，但 IgA protease 是 S. pneumoniae（以及 Neisseria、H. influenzae）的毒力因子。", {"opts": {"C": BLANK}}),
    28: ("fungi", "皮膚／皮下／系統性黴菌", "B", "Penicillium（Talaromyces）marneffei 是溫度雙型性真菌（25 °C 菌絲、37 °C 酵母）。Epidermophyton、Trichophyton、Microsporum 是皮癬菌，只有菌絲型。", {"opts": {"B": "Penicillium marneffei", "C": "Trichophyton rubrum"}}),
    30: ("fungi", "Cryptococcus／Candida", "A", "念珠菌症是最常見、致死率最高的伺機性真菌感染（念珠菌血症死亡率可達 40–50%）；隱球菌也是伺機性（腦膜炎）但發生率較低；孢子絲菌症是皮下感染。", {"opts": {"B": "Cryptococcosis", "C": BLANK}}),
    32: ("bacillus", "孢子", "D", "Erysipelothrix rhusiopathiae 不產生內孢子；Clostridium、Bacillus 都會。"),
    33: ("bacillus", "Bacillus anthracis", "C", "腸胃型炭疽是吃進帶芽孢的未煮熟肉類所致，炭疽桿菌沒有「腸毒素」。致死毒素（PA＋LF）與水腫毒素（PA＋EF，adenylate cyclase → cAMP↑）都是 A-B 毒素；莢膜為 poly-D-glutamic acid。"),
    34: ("bacillus", "Bacillus cereus", "C", "Fried rice syndrome＝B. cereus 嘔吐型：耐熱的 cereulide 毒素在炒飯中仍有活性。"),
    35: ("bacillus", "C. diphtheriae", "B", "人類是白喉桿菌唯一宿主；B. anthracis、Erysipelothrix、Listeria 都有動物或環境宿主。", {"opts": {"C": "Erysipelothrix rhusiopathiae"}}),
    36: ("bacillus", "Listeria", "B", "Listeria 在室溫（< 30 °C）有鞭毛、呈翻滾式運動（tumbling motility），也能在細胞內用 actin rocket 移動，所以 non-motile 是錯的。可在 4 °C、高鹽生長；胞內寄生逃避抗體；可經胎盤造成流產、新生兒感染。"),
    37: ("bacillus", "C. diphtheriae", "A", "白喉毒素 A 片段把 EF-2 ADP-ribosylation，抑制蛋白質合成。結合 60S rRNA 的是 Shiga toxin。"),
    39: ("enterobacteriaceae", "Shigella", "C", "Shigella 沒有鞭毛（不會動）；E. coli、Salmonella、Proteus 都有周鞭毛（Proteus 會 swarming）。"),
    40: ("enterobacteriaceae", "Salmonella", "D", "傷寒需要較大的感染量（約 10³–10⁵），少於 100 隻就能感染的是 Shigella。傷寒只感染人，感染第一週血液培養陽性率最高。"),
    41: ("enterobacteriaceae", "Shigella", "D", "由 β 噬菌體 tox 基因編碼的是白喉毒素。Shiga toxin 是 A-B 毒素（A 切 60S 的 28S rRNA），可造成 HUS。"),
    42: ("enterobacteriaceae", "E. coli 致病型", "A", "ETEC 產生耐熱 ST（升高 cGMP）與不耐熱 LT（升高 cAMP），造成旅行者腹瀉。", {"opts": {"C": "Enteropathogenic E. coli（EPEC）"}}),
    43: ("enterobacteriaceae", "Yersinia／plague", "B", "鼠疫主要經跳蚤叮咬傳播（肺鼠疫可飛沫人傳人），不是被老鼠咬。Y. pestis 是人畜共通病原，有 F1 莢膜、Yops 等抗吞噬。"),
    46: ("immuno-basic", "先天 vs 後天免疫", "D", "B 細胞屬於後天免疫；巨噬細胞、嗜中性球、樹突細胞都是先天免疫細胞。"),
    47: ("immuno-basic", "NK 細胞與抑制性受體", "A", "NK 細胞沒有抗原特異性（靠活化／抑制受體平衡）；CTL 有。兩者都有 FasL、都與 MHC I 有關（CTL 辨識 MHC I＋胜肽；NK 遇到缺 MHC I 的細胞就殺）。"),
    48: ("immuno-basic", "先天 vs 後天免疫", "C", "M 細胞位在 Peyer's patches 上方，負責把腸腔抗原轉運（transcytosis）到下方的淋巴組織。"),
    57: ("agab", "B 細胞活化／class switch／生發中心", "C", "Immature B 細胞只表現 mIgM；成熟（naïve）B 細胞經 alternative splicing 同時表現 mIgM 與 mIgD。"),
    58: ("agab", "抗體結構", "C", "抗體的類別與亞型由重鏈（恆定區）決定，不是輕鏈。"),
    59: ("agab", "B 細胞活化／class switch／生發中心", "A", "生發中心三件事：親和力成熟（SHM＋篩選）、類別轉換、分化為漿細胞與記憶 B 細胞。V(D)J 重組在骨髓、mIgM 表現在骨髓中就已完成。"),
    67: ("tcell-dev", "胸腺選擇", "D", "Stem cell → pro-T → pre-T → double positive（CD4⁺CD8⁺）→ single positive → naïve mature T。"),
    68: ("mhc", "抗原處理與呈現（TAP）", "A", "β2-microglobulin 是 MHC I 的輕鏈，與 MHC II 路徑無關。MHC II 路徑：calnexin（ER 摺疊）、invariant chain、cathepsin（切 Ii 與抗原）、HLA-DM（換掉 CLIP）。"),
    72: ("tcell-act", "B 細胞活化／class switch／生發中心", "A", "Linked recognition 只要求 B、T 細胞辨識「同一個抗原（物理上相連）」，epitope 可以不同。B 細胞吞入整個病毒，把內部核心蛋白處理後以 MHC II 呈現，所以辨識核心蛋白的 TH 仍可以幫助辨識表面蛋白的 B 細胞，(A) 錯。"),
    76: ("tcell-act", "TH 分化與細胞激素", "D", "Tfh 位於生發中心 light zone，分化需要 Bcl-6，分泌 IL-21（促漿細胞分化）與 IL-4。小鼠 IgG1 的轉換需要 IL-4，所以只加 LPS、IL-2、IL-21 不能取代 Tfh 刺激 IgG1。"),
    77: ("infection-immunity", "第一道防線", "AE", "(A) 第一道防線包含物理、化學／生物活性因子（溶菌酶、胃酸、抗菌胜肽、共生菌）；(E) 補體最終形成 MAC 溶解病原。原考古答案為 E；A 也正確，兩個都算對。(B) 糞便移植是微生物相的應用；(C) 溶菌酶可直接殺菌；(D) defensin 等是胜肽不是脂質。"),
    78: ("infection-immunity", "NADPH oxidase／CGD", "B", "NADPH oxidase 是多次單位複合體，呼吸爆發時細胞質次單位（p40、p47、p67phox）移到膜上與 gp91／p22phox 組裝，產生 superoxide（氧化，不是抗氧化）。CGD 是次單位基因突變（缺失），不是過度表現。"),
    79: ("infection-immunity", "TLR／PRR", "D", "PRR 活化後誘發促發炎細胞激素與抗病毒干擾素。TLR、CLR 是膜上 PRR；NLR、RLR、cytosolic DNA sensor 在細胞質（B、C 寫反）；PRR 多數不是吞噬受體；過度活化也可能致病。"),
    80: ("infection-immunity", "免疫逃脫", "E", "病毒逃避免疫：阻斷 PRR／第一型干擾素訊號、下調 MHC I、誘導抗發炎細胞激素、潛伏在細胞內，四項都對。"),
    81: ("immunodeficiency", "補體缺乏", "D", "C3 缺乏：調理作用喪失 → 反覆化膿菌感染；免疫複合體無法經補體清除 → 沉積造成免疫複合體疾病。"),
    82: ("immunodeficiency", "NADPH oxidase／CGD", "E", "反覆細菌、真菌感染並出現肉芽腫 → 懷疑 CGD（吞噬細胞缺陷），應檢查嗜中性球數量與功能（如 DHR、NBT 試驗）。"),
}
SKIP109 = "1–12、16、18、19、21、31、38、49–56、69、70、73–75 已在題庫；60 與 106 第 15 題同；71 與 110 第 29 題同；27 選項缺漏；29 看圖題；44、45 臨床課；61–66、83、84 過敏與自體免疫（期中考後）"

K110 = {
    1: ("bact-structure", "微生物學史／柯霍假說", "B", "Koch 以炭疽桿菌證明特定微生物造成特定疾病（Koch's postulates）。"),
    2: ("bact-structure", "微生物學史／柯霍假說", "A", "在經濟動物飼料中添加抗生素正是 AMR 的成因之一。對策：抗生素使用指引、監測、研發新抗生素、噬菌體、疫苗、快速診斷。"),
    3: ("bact-structure", "人體微生物相", "D", "Human Microbiome Project：不同人同一部位的菌種組成差異很大（taxonomic diversity 大），但代謝功能相似（functional redundancy）。"),
    4: ("bact-structure", "細胞壁／革蘭氏染色", "A", "LPS（內毒素）位於 G(−) 菌外膜（outer membrane）的外層。"),
    5: ("bact-structure", "細菌分類鑑定", "A", "PCR 是依基因型（genotypic）鑑定；血清型、碳源利用、代謝產物都是表現型分類。"),
    6: ("bact-structure", "細菌構造與功能", "C", "趨化作用靠鞭毛運動（向營養、遠離毒物）；fimbriae 負責附著。"),
    8: ("bact-structure", "生長曲線與代謝", "C", "厭氧菌缺 superoxide dismutase、catalase，無法清除利用氧氣時產生的自由基（superoxide、H₂O₂），所以不能在有氧環境生長。", {"opts": {"C": "無法移除利用氧氣所生成的氧化自由基"}}),
    9: ("bact-genetics", "突變", "C", "Nonsense mutation：密碼子變成終止密碼子 → 蛋白提早終止。Missense 換成另一個胺基酸；silent 胺基酸不變；null 是功能完全喪失。"),
    10: ("bact-genetics", "DNA 複製與基因表現", "B", "Sanger 定序：DNA 合成時隨機摻入 ddNTP 使鏈終止，依片段長度與螢光讀出序列，所以是「DNA 合成」測「序列」。"),
    11: ("staph-strep", "S. aureus", "B", "兩者都是 catalase 陽性，無法區分。S. aureus：coagulase 陽性、發酵 mannitol、β 溶血；S. epidermidis 都是陰性或不溶血。"),
    12: ("pathogenesis", "免疫逃脫", "AC", "(A) GAS 玻尿酸莢膜模仿結締組織。(B) 分解 C5a 的是 S. pyogenes 的 C5a peptidase，不是 S. aureus。(C) 結核菌也有 catalase-peroxidase（KatG）可分解 H₂O₂。(D) 分泌 coagulase 的是 S. aureus。原考古答案為 A；C 敘述也成立，兩個都算對。"),
    13: ("pathogenesis", "細菌附著", "B", "黏附素（adhesin）常位於線毛末端，結合宿主細胞表面醣類受體。(A) Legionella 由環境吸入，不在肺內人傳人；(C) 生物膜靠多醣（glycocalyx）附著；(D) 題目原文缺字，不影響作答。", {"opts": {"D": "Salmonella 利用 docking system 抑制自己的……，以攻擊巨噬細胞（原考古缺字）"}}),
    14: ("sterilization", "滅菌與消毒", "A", "呼吸治療器材（塑膠、橡膠、有管腔）不耐熱，用 glutaraldehyde（高階消毒／化學滅菌）浸泡最合適。Hexachlorophene 是皮膚消毒劑；UV 穿透力差；γ 射線用於工業滅菌拋棄式用品。"),
    15: ("fungi", "皮膚／皮下／系統性黴菌", "B", "Paracoccidioides brasiliensis：酵母型多極出芽，像船舵（mariner's wheel）。Coccidioides 是 spherule；Histoplasma 小卵圓酵母在巨噬細胞內；Blastomyces 單一寬基底出芽。"),
    16: ("fungi", "Cryptococcus／Candida", "D", "白色念珠菌屬子囊菌門、為雙型性（酵母＋假菌絲／菌絲），可造成鵝口瘡；侵襲性念珠菌血症死亡率很高，所以「不會致死」錯。"),
    17: ("enterobacteriaceae", "E. coli 致病型", "C", "EHEC（O157:H7）的 Shiga toxin（verotoxin）是 A-B 毒素，切 28S rRNA 抑制蛋白合成，可引起 HUS；不是升高 cAMP。"),
    18: ("enterobacteriaceae", "毒素（內/外毒素、AB toxin）", "D", "ETEC LT、B. cereus 腹瀉型腸毒素、炭疽 edema toxin 都使 cAMP 上升；EHEC verocytotoxin（Shiga-like toxin）是抑制蛋白質合成。"),
    19: ("enterobacteriaceae", "E. coli 致病型", "C", "EHEC 的主要毒素是 Shiga toxin（抑制蛋白合成），造成出血性腹瀉與 HUS，並非一般「腸毒素」（升高 cAMP 那類）造成水瀉。"),
    20: ("bacillus", "Bacillus anthracis", "C", "人類炭疽最常見的是皮膚型（> 90%）；吸入型最致命。B. anthracis 是 G(+)，莢膜由多肽（poly-D-glutamic acid）組成，可作生物武器。"),
    21: ("bacillus", "Bacillus cereus", "C", "嘔吐型（耐熱毒素）的來源主要是米飯；腹瀉型（不耐熱腸毒素）才與肉類、蔬菜有關。"),
    22: ("bacillus", "Listeria", "B", "Listeria 不產生內孢子；它本身就能在 4 °C 生長，所以可用冷增菌（cold enrichment）分離。"),
    23: ("bacillus", "其他", "B", "Erysipelothrix rhusiopathiae 是人畜共通病原（豬、魚、禽類），人類不是唯一宿主；造成皮膚類丹毒（erysipeloid），生長慢，有莢膜。"),
    24: ("bacillus", "C. diphtheriae", "C", "白喉毒素是 EF-2 的 ADP-ribosylation 抑制蛋白合成，不是作用在 60S（那是 Shiga toxin）。A-B 毒素、需帶 tox 基因的 β 噬菌體溶原化、造成呼吸道感染（偽膜）都正確。"),
    28: ("innate", "干擾素", "B", "IFN-α（第一型干擾素）由受病毒感染的細胞（白血球）產生，讓周圍細胞進入抗病毒狀態、活化 NK；屬於先天免疫的細胞激素，不是 chemokine。"),
    29: ("tcell-act", "TH 分化與細胞激素", "B", "TH17 分泌 IL-17，招募嗜中性球，清除胞外細菌與真菌。"),
    33: ("agab", "B 細胞活化／class switch／生發中心", "A", "AID 在生發中心 B 細胞高量表現，造成體細胞超突變與類別轉換。(B) 轉換成 IgE 由 IL-4 決定；(C) AID 把 cytosine 變成 uracil（不是 uridine）；(D) RSS 是 RAG 辨識、主導 V(D)J 重組，類別轉換靠 switch region。"),
    34: ("tcell-act", "共刺激（CD28/B7/CTLA-4）", "A", "CTLA-4 與 CD28 競爭 B7（CD80／86），親和力更高，抑制 T 細胞活化；腫瘤利用此免疫檢查點逃脫，anti-CTLA-4 是免疫治療。"),
    35: ("innate", "白血球遷移（selectin→chemokine→integrin）", None, None),
    36: ("innate", "補體系統", "A", "C3b（以及 iC3b、C4b）是調理素；C3a、C5a 是過敏毒素與趨化因子。", {"opts": {"A": "C3b", "B": "C5a", "C": "C4a", "D": "C3a"}}),
    37: ("innate", "補體系統", "B", "補體功能：調理促進吞噬、趨化與發炎、MAC 溶解細胞膜。(A)(C)(D) 都講反了。"),
    40: ("innate", "TLR／PRR", "D", "TLR4（搭配 MD-2、CD14）辨識 LPS。TLR9 辨識 CpG DNA；TLR7／8 辨識 ssRNA。"),
    44: ("agab", "抗體類別與功能", "D", "IgD 主要以膜型存在於成熟 B 細胞上。血清與組織液中最多的是 IgG；黏膜分泌液中最多的是 IgA。"),
    46: ("agab", "抗體類別與功能", "B", "IgG 的功能是中和、調理、活化補體、ADCC、通過胎盤；抗體進不了細胞，無法清除細胞內病原菌（那要靠 CTL、活化巨噬細胞）。"),
    53: ("mhc", "抗原處理與呈現（TAP）", "A", "HLA-DM 催化 CLIP 離開 MHC II、換上抗原胜肽。缺 HLA-DM 時 MHC II 仍會運到細胞表面，但溝裡卡的是 CLIP（Janeway；HLA-DM 缺陷小鼠的 MHC II 大多帶 CLIP）。百十四詳解選 (B)「沒有 MHC II 被釋放到細胞外」，網站依課本改為 (A)。"),
}
del K110[35]
SKIP110 = "7、30–32、35、38、39、41–43、45、47、48 已在題庫；25–27 臨床課；49–51 過敏反應（期中考後）；52 題目不完整"

PAT_NEG = re.compile(r"錯誤|不正確|不是|不包括|不包含|不屬於|沒有|不會|最不可能|not|NOT|incorrect|wrong|false|except", re.I)


def build(src, pdf, stop, keys, prefix, overrides_stem=None):
    qs = parse(pdf, stop)
    out = []
    for n, v in keys.items():
        ch, topic, ans, exp = v[:4]
        extra = v[4] if len(v) > 4 else {}
        q = qs[n]
        opts = dict(q["opts"])
        opts.update(extra.get("opts", {}))
        stem = (overrides_stem or {}).get(n, q["stem"]).strip()
        item = {
            "id": f"{prefix}-{n:02d}", "source": src, "section": src.replace("期中考古", "微免期中考古"), "num": n,
            "chapter": ch, "type": "mcq", "stem": stem,
            "options": [{"k": k, "t": (opts[k].strip() or BLANK)} for k in sorted(opts)],
            "answer": list(ans), "explain": exp, "topics": [topic],
            "pattern": "選錯誤（否定）題" if PAT_NEG.search(stem) else ("臨床情境題" if re.search(r"year-old|病人|患者|孕婦|臨床", stem) else "選正確／單一概念題"),
        }
        if extra.get("multi"):
            item["multi"] = True
            item["pattern"] = "組合選擇題"
        out.append(item)
    return out


STEM106 = {5: "The most abundant granulocyte in the immune system is the ____.",
           15: "Antibody diversity is NOT generated by ____.",
           36: "A 3-year-old boy was found to have chronic granulomatous disease caused by NADPH oxidase deficiency. Which of the following is most likely?"}
STEM110 = {}

Q = (build("106 期中考古", "106微免期中考古.pdf", "106 免疫學期中考古\n\n組長：甯泰翔\n\n勘誤組員：全體組員", K106, "kmid106", STEM106)
     + build("109 期中考古", "109微免期中考古.pdf", "109 微免期中考古\n組長：甯泰翔\n\n勘誤組員：全體組員", K109, "kmid109")
     + build("110 期中考古", "110微免期中考古題目.pdf", None, K110, "kmid110", STEM110))

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(OUT, len(Q), "questions")
print("略過 106：", SKIP106)
print("略過 109：", SKIP109)
print("略過 110：", SKIP110)
