#!/usr/bin/env python3
"""微免 1141 期中考記題 → subjects/micro-immuno/data/questions-k114.json

來源：slides/micro-immuno/共筆考古/百十三/微免/1141微免期中記題.xlsx（學長姐考後記題，沒有答案欄）
- 答案與詳解由網站依課本判斷，詳解開頭會註明。
- 略過：沒記到的題、選項缺漏或有多個正確選項無法判斷的題（26、29、36、53、54、77、83–85），以及本學期章節沒有的病毒學（86–91）。
執行：python3 tools/build_micro_k114.py（在 repo 根目錄）
"""
import json, re, zipfile

XLSX = "slides/micro-immuno/共筆考古/百十三/微免/1141微免期中記題.xlsx"
OUT = "subjects/micro-immuno/data/questions-k114.json"
SRC = "114 期中考古"
NOKEY = "（記題沒有附答案，網站依課本判斷）"

# 題號: (章節, 答案, 詳解)
KEY = {
    3: ("bact-structure", "D", "Periplasmic space 位於 G(−) 菌的外膜與細胞膜之間。不是所有細菌都有鞭毛；細菌沒有粒線體；G(+) 的 peptidoglycan 更厚。"),
    4: ("bact-structure", "B", "Crystal violet–iodine 複合物被 G(+) 厚的 peptidoglycan 細胞壁留住，酒精脫色後仍呈紫色。"),
    5: ("bact-structure", "C", "Fimbriae（pili）負責黏附；負責移動的是鞭毛。"),
    6: ("enterobacteriaceae", "B", "O 抗原 = LPS 的 O 多醣；H 抗原 = 鞭毛（flagellin）；K 抗原 = 莢膜。"),
    11: ("sterilization", "B", "高壓蒸氣滅菌（121 °C、15 psi）靠飽和水蒸汽的高溫使蛋白質變性。"),
    12: ("sterilization", "D", "Ethylene oxide 是低溫氣體滅菌，適合怕熱的醫療器材。"),
    13: ("sterilization", "C", "Chlorhexidine（環己定）常用於手術前刷手與病人皮膚消毒。"),
    14: ("pathogenesis", "A", "逃避吞噬的方式：抑制 phagosome–lysosome 融合、抵抗溶酶體酵素、逃到細胞質複製（Listeria）。降解宿主核糖體不是常見機制。"),
    15: ("innate", "C", "Lysozyme 水解 peptidoglycan 的 β-1,4 鍵（NAM–NAG）。"),
    16: ("pathogenesis", "A", "Superantigen 跨接 MHC II 與 TCR Vβ，非專一活化大量 T 細胞 → cytokine storm（例：TSST-1）。"),
    19: ("staph-strep", "B", "Protein A 結合 IgG 的 Fc 端，使抗體方向倒置，阻止調理吞噬。"),
    20: ("staph-strep", "D", "A 群鏈球菌 M protein 與心肌抗原的分子相似性 → 自體免疫（急性風濕熱）。"),
    21: ("staph-strep", "A", "S. pneumoniae 可以是正常人咽喉的菌叢；莢膜是主要毒力因子，血液培養呈 α 溶血（半溶血）。"),
    22: ("staph-strep", "A", "Enterococcus 院內感染與多重抗藥性（例：VRE）有關。"),
    25: ("enterobacteriaceae", "A", "UPEC 產生 hemolysin；ETEC 產生 LT／ST；Shiga toxin 是 EHEC；EAEC 也會產生毒素。"),
    27: ("enterobacteriaceae", "B", "Shigella 只要 10–100 個菌就能致病，是三者中最低的。"),
    28: ("enterobacteriaceae", "A", "鼠疫桿菌 Yersinia pestis 經跳蚤叮咬傳播（肺鼠疫可飛沫人傳人），不是吸入老鼠糞便。"),
    30: ("neisseria", "A", "P. aeruginosa 的 alginate（多醣）構成生物膜基質，囊性纖維化病人特別重要。"),
    31: ("bacillus", "C", "Anthrax 的 edema toxin（PA＋EF）與 lethal toxin 都是 A-B toxin。B. anthracis 是 G(+)、莢膜是 poly-D-glutamic acid 胜肽，最常見的是皮膚型。"),
    32: ("bacillus", "D", "Elek test 是用抗毒素測**菌株是否產毒**；測中和抗體的是 Schick test（已不用）。"),
    33: ("bacillus", "C", "嘔吐型毒素耐熱、與米飯有關，潛伏期約 1–6 小時（平均約 2 小時），不是 9 小時。腹瀉型潛伏期 > 6 小時、病程約 20–36 小時。"),
    34: ("bacillus", "C", "Edema factor 是 adenylate cyclase；cholera toxin 使 Gs 持續活化，兩者都使 cAMP 上升。"),
    35: ("neisseria", "D", "H. pylori 微需氧、有端叢鞭毛、移動性高。吃未煮熟禽肉與 Guillain-Barré 症候群是 Campylobacter jejuni。"),
    37: ("fungi", "C", "Chromoblastomycosis：組織中可見厚壁、棕色、圓形的 sclerotic bodies（Medlar bodies），是暗色真菌。"),
    38: ("fungi", "A", "Polyenes（amphotericin B、nystatin）直接與 ergosterol 結合，在細胞膜形成孔洞。抑制 ergosterol 合成的是 azoles；抑制 β-glucan 的是 echinocandins。"),
    39: ("immuno-basic", "C", "樹突細胞是最主要的抗原呈現細胞，連結先天與後天免疫。"),
    40: ("tcell-dev", "A", "Positive selection：能辨識自我 MHC、訊號適中的胸腺細胞存活；不能辨識的死於 neglect。"),
    41: ("fungi", "C", "Germ tube test 用來鑑定 Candida albicans。Cryptococcus 屬擔子菌門，會造成腦膜炎，在 Niger seed agar 上因 phenoloxidase 呈棕黑色。"),
    42: ("immuno-basic", "C", "胚胎造血依序在卵黃囊、胎兒肝（脾）、骨髓；心臟不是造血器官。"),
    45: ("mhc", "A", "B 細胞、樹突細胞、巨噬細胞都表現 MHC II 與 B7（共刺激分子），是專業 APC。活化 naïve T 細胞最強的是樹突細胞。"),
    46: ("tcell-dev", "C", "CDR3 由 V(D)J 接合處形成（含 N、P 核苷酸），變異度最大。"),
    49: ("tcell-dev", "B", "Positive selection 是胸腺皮質上皮細胞的自我 MHC-peptide 給予適中訊號而存活。AIRE 相關的是 negative selection。"),
    50: ("immuno-basic", "D", "樹突細胞同時參與先天免疫並活化後天免疫。"),
    51: ("tcell-dev", "A", "TCR 多樣性來自多個 V 片段、V(D)J 重組（RAG1／2）、TdT 加 N 核苷酸。AIRE 與 negative selection 有關；class switch 只發生在 B 細胞。"),
    52: ("tcell-act", "A", "Tfh 分泌 IL-21（並表現 CD40L）幫助生發中心 B 細胞。"),
    57: ("mhc", "C", "MHC II 表現在專業 APC 與胸腺上皮細胞，不表現在嗜中性球；co-receptor 是 CD4。"),
    58: ("agab", "A", "體細胞超突變只發生在**可變區**，不發生在固定區。"),
    61: ("tcell-act", "B", "Th17 分泌 IL-17，招募嗜中性球對抗胞外細菌與真菌。"),
    62: ("innate", "C", "趨化反應由 chemokine receptor（GPCR）接收 chemokine 訊號。"),
    65: ("innate", "B", "三條補體路徑都匯集在 C3 convertase（C3 的切割）。"),
    66: ("innate", "C", "補體最終形成 MAC 溶解細胞膜；補體會促進吞噬（調理作用）與發炎。"),
    67: ("innate", "B", "MAC = C5b、C6、C7、C8、C9（多個 C9 聚合成孔洞）。"),
    69: ("innate", "D", "CD94/NKG2A 辨識 HLA-E，是 NK 細胞的抑制型受體。KIR 短尾（S）是活化型；HLA-E 是配體不是受體；CD14 是 LPS 共受體。"),
    70: ("agab", "B", "B 細胞直接辨識抗原的構形決定位（可為不連續序列，蛋白、多醣、脂質都可以），不需要 MHC。"),
    71: ("agab", "D", "分泌片段（secretory component）來自上皮細胞的 poly-Ig receptor。IgA 不活化經典補體路徑；TGF-β（不是 IL-12）促進 IgA class switch。"),
    72: ("agab", "A", "能通過胎盤的是 IgG，不是 IgM。"),
    73: ("agab", "C", "TdT 在接合處隨機加入 N 核苷酸，不是「標記」斷裂點。"),
    78: ("innate", "C", "PRRs 辨識 PAMPs 與 DAMPs；可在細胞膜、內體或細胞質；不只存在於吞噬細胞。"),
    79: ("innate", "A", "Inflammasome 可由 NLRP3、AIM2 等形成，活化 caspase-1 → 產生 IL-1β、IL-18。（樹突細胞中也有，但題目最佳答案為 A。）"),
}
TOPIC = {"bact-structure": "細菌構造", "sterilization": "滅菌消毒", "pathogenesis": "致病機轉", "innate": "先天免疫",
         "staph-strep": "葡萄球菌、鏈球菌", "enterobacteriaceae": "腸桿菌科", "neisseria": "其他 G(−) 菌", "bacillus": "Bacillus 等 G(+) 桿菌",
         "fungi": "真菌", "immuno-basic": "免疫學基本概念", "tcell-dev": "T 細胞發育", "tcell-act": "T 細胞活化",
         "mhc": "MHC 與抗原呈現", "agab": "抗原抗體"}


def rows():
    z = zipfile.ZipFile(XLSX)
    ss = [re.sub(r"<[^>]+>", "", m).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          for m in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)]
    sheet = z.read("xl/worksheets/sheet1.xml").decode()
    for r, body in re.findall(r'<row[^>]*r="(\d+)"[^>]*>(.*?)</row>', sheet, re.S):
        cells = {}
        for col, attr, v in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(?:<v>(.*?)</v>)?', body):
            if v:
                cells[col] = (ss[int(v)] if 't="s"' in attr else v).strip()
        yield cells


def clean(t):
    t = re.sub(r"^\(?[A-E1-4]\)\s*", "", t.replace("\n", "")).strip()
    if re.fullmatch(r"\d{5}\.0", t):  # 例：12357.0 → (1)(2)(3)(5)(7)
        t = "".join(f"({c})" for c in t[:5])
    return t


Q, seen = [], set()
for c in rows():
    try:
        n = int(float(c.get("A", "x")))
    except ValueError:
        continue
    if n not in KEY or not c.get("C"):
        continue
    opts = []
    for col in "DEFGH":
        if c.get(col):
            t = clean(c[col])
            if t not in [o["t"] for o in opts]:
                opts.append({"k": "ABCDE"[len(opts)], "t": t})
    ch, ans, exp = KEY[n]
    stem = c["C"].replace("\n", "")
    Q.append({"id": f"k114-{n:02d}", "source": SRC, "num": n, "chapter": ch, "type": "mcq", "stem": stem,
              "options": opts, "answer": [ans], "explain": NOKEY + exp, "topics": [TOPIC[ch]],
              "pattern": "選錯誤／否定題" if re.search(r"錯誤|不包含|不是|不會|不包括|incorrect", stem) else "選正確／單一概念題"})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(OUT, len(Q), "questions")
