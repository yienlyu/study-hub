#!/usr/bin/env python3
"""微免：補上原本沒有圖的章節 → subjects/micro-immuno/figures/（slides 裁切 webp）＋ 合併進 figures.json

原本的 figures.json 是手動維護的；這支只新增／更新下面列出的 id，其他條目原樣保留，
最後依 subject.json 的章節順序排序（同章節內維持原順序）。
來源：slides/micro-immuno/ 的講義 PDF 與上課 pptx（ppt/media 原圖）。
需要 pymupdf 與 Pillow。執行：python3 tools/build_micro_figures_extra.py（在 repo 根目錄）
"""
import io, json, os, zipfile
import fitz
from PIL import Image

SRC = "slides/micro-immuno"
ROOT = "subjects/micro-immuno"
OUT = f"{ROOT}/figures/slides"
W = 1400
STER = "[講義] Sterilization_ Disinfection_ and Antisepsis.pdf"
IMDEF = "1151_免疫缺陷疾病.pdf"
HOST = "20261007 宿主對感染之防衛.pptx"
BACI = "Bacillus_ Listeria_ Corynebacterium.pptx"
ENTE = "腸桿菌及弧菌.pptx"
INNATE = "Innate immunity 講義2026.pdf"
DECK = {INNATE: "W2-2 Innate immunity", STER: "Sterilization, disinfection & antisepsis", IMDEF: "W18 免疫缺陷疾病", HOST: "1007 宿主對感染之防衛",
        BACI: "Bacillus, Listeria, Corynebacterium", ENTE: "腸桿菌科與弧菌"}


def save(im, name):
    im = im.convert("RGB")
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=80, method=6)
    return im.size


def pdf_crop(pdf, page, box):
    p = fitz.open(f"{SRC}/{pdf}")[page - 1]
    r = p.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    z = max(2.0, 2 * W / clip.width)
    return Image.open(io.BytesIO(p.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip).tobytes("png")))


def pptx_media(pptx, media):
    with zipfile.ZipFile(f"{SRC}/{pptx}") as z:
        im = Image.open(io.BytesIO(z.read(f"ppt/media/{media}")))
        if im.mode in ("RGBA", "LA", "P"):   # 透明背景 → 白底，深色模式才看得清楚
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, "white")
            bg.alpha_composite(im)
            im = bg
        return im


def svg(id, ch, title, topics, kw, cap):
    assert os.path.exists(f"{ROOT}/figures/{id}.svg"), id
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap)


def slide(id, ch, title, topics, kw, cap, src, page, box=(0, 0, 1, 1), media=None):
    name = id.removeprefix("slide-")
    w, h = save(pptx_media(src, media) if media else pdf_crop(src, page, box), name)
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap,
                type="slide", src=f"figures/slides/{name}.webp", deck=DECK[src], page=str(page), w=w, h=h)


NEW = [
 # ---------------- 滅菌消毒
 slide("slide-control-methods", "sterilization", "微生物控制方法總覽", ["物理方法", "化學方法"],
       "microbial control methods physical chemical mechanical heat radiation filtration",
       "物理（熱、輻射）、化學（氣體、液體）、機械（過濾）三大類；每一種方法標明是<strong>滅菌</strong>還是<strong>消毒</strong>。", STER, 5),
 slide("slide-autoclave", "sterilization", "高壓蒸氣滅菌鍋（autoclave）", ["物理方法"],
       "autoclave steam under pressure 121 15 psi sterilization",
       "<strong>121°C、15 psi、10–40 分鐘</strong>，濕熱讓蛋白質凝固，可以殺孢子。液體瓶要鬆蓋、等降到 80°C 再開，避免爆裂。", STER, 8),
 svg("resistance-ladder", "sterilization", "微生物對消毒劑的抵抗力階梯", ["消毒劑等級"],
     "resistance prions spores mycobacteria nonenveloped virus fungi vegetative bacteria enveloped virus high intermediate low level disinfectant",
     "由難到易：<strong>普利昂 &gt; 孢子 &gt; 結核菌 &gt; 無套膜病毒 &gt; 真菌 &gt; 細菌 &gt; 有套膜病毒</strong>。高等級殺得到孢子、中等級殺得到結核菌、低等級兩者都不行。"),
 slide("slide-disinfectant-levels", "sterilization", "消毒劑等級與使用時機", ["消毒劑等級"],
       "high intermediate low level disinfectant critical semicritical noncritical Spaulding",
       "<strong>Critical</strong>（進入無菌組織：手術器械）→ 滅菌；<strong>Semicritical</strong>（接觸黏膜：內視鏡）→ 高等級消毒；<strong>Noncritical</strong>（完整皮膚：血壓計）→ 低中等級。", STER, 15),
 # ---------------- 先天免疫：四種 opsonic receptors（p32 總覽 phagocytosis、p36 tlr4 已在 figures.json）
 slide("mannose-receptor", "innate", "Opsonic receptor (1)：Mannose receptor", ["調理作用／opsonic receptor"],
       "mannose receptor C-type lectin domain cysteine-rich mannosylated ligand opsonic receptor",
       "頭端 cysteine-rich lectin domain 認硫酸化醣類；下面 <strong>8 個 C-type lectin domains</strong> 才是認 <strong>mannose</strong>（mannosylated ligand）的部分。", INNATE, 33, (0.255, 0.17, 0.77, 0.94)),
 slide("fc-receptor", "innate", "Opsonic receptor (2)：Fcγ receptors", ["調理作用／opsonic receptor"],
       "Fc receptor FcγRI CD64 FcγRIIa CD32 FcγRIIIa FcγRIIIb CD16 GPI anchor IgG monocyte neutrophil",
       "抓被 <strong>IgG</strong> 包住的病原：FcγRI（<strong>CD64</strong>）→ monocyte；FcγRIIa（<strong>CD32</strong>）→ monocyte／neutrophil；FcγRIIIa（<strong>CD16</strong>）→ monocyte；FcγRIIIb（CD16，<strong>GPI anchor</strong>）→ neutrophil。", INNATE, 34, (0.27, 0.14, 1.0, 0.97)),
 slide("complement-receptor", "innate", "Opsonic receptor (3)：Complement receptors CR1–4", ["調理作用／opsonic receptor", "補體系統"],
       "complement receptor CR1 CD35 CR2 CD21 CR3 CD11b CD18 CR4 CD11c integrin CCP repeat FDC",
       "CR1（<strong>CD35</strong>）在吞噬細胞、紅血球；CR2（<strong>CD21</strong>）在 <strong>B 細胞、FDC</strong>（不在吞噬細胞上）；<strong>CR3（CD11b/CD18）、CR4（CD11c/CD18）是 integrin</strong>，在單核吞噬細胞與 NK。", INNATE, 35, (0.05, 0.20, 0.97, 0.91)),
 # ---------------- 對抗感染的免疫反應
 slide("slide-infection-sites", "infection-immunity", "感染部位決定防禦機制", ["胞外感染", "胞內感染"],
       "extracellular intracellular cytoplasmic vesicular complement macrophage antimicrobial peptides NK cells activated macrophages",
       "胞外（組織間隙、血液）→ 補體、巨噬細胞、嗜中性球、抗體；上皮表面 → 抗菌胜肽、IgA；胞內細胞質（病毒、Listeria）→ <strong>NK、CTL</strong>；囊泡內（結核菌）→ <strong>活化的巨噬細胞</strong>（Janeway Fig 2.2）。", HOST, 53, media="image90.png"),
 slide("slide-ros-killing", "infection-immunity", "吞噬細胞怎麼殺菌：ROS 與 RNI", ["胞外感染"],
       "reactive oxygen species NADPH oxidase superoxide myeloperoxidase hypochlorous acid iNOS nitric oxide respiratory burst CGD",
       "NADPH oxidase 產生 superoxide → SOD → H₂O₂ → <strong>MPO</strong> → 次氯酸；iNOS 產生 NO。缺 NADPH oxidase = <strong>CGD</strong>。", HOST, 24, media="image28.png"),
 slide("slide-nox", "infection-immunity", "吞噬體上的 NADPH oxidase（NOX2）", ["胞外感染"],
       "NADPH oxidase NOX2 gp91phox p22phox p47phox p67phox Rac phagosome",
       "膜上的 gp91phox＋p22phox（cytochrome b558）與細胞質的 p47、p67、p40、Rac 組合後啟動 → respiratory burst。最常見的 CGD 是 X-linked <strong>gp91phox</strong> 缺陷。", HOST, 25, media="image29.png"),
 slide("slide-prrs", "infection-immunity", "PRR 家族：TLR、RLR、NLR、DNA sensor", ["PRRs、PAMPs、DAMPs"],
       "pattern recognition receptors TLR RLR NLR RIG-I MDA5 NOD NALP DNA sensor endosome",
       "細胞膜上的 TLR 看<strong>胞外</strong>菌體成分；內體的 TLR3/7/8/9 看<strong>核酸</strong>；細胞質的 RLR（RIG-I、MDA5）看病毒 RNA，NLR（NOD、NALP）看細菌成分。", HOST, 38, media="image46.jpeg"),
 # ---------------- 免疫缺陷
 svg("immunodeficiency-map", "immunodeficiency", "免疫缺陷地圖：卡在哪一步、怕哪種感染", ["SCID", "抗體缺陷", "吞噬細胞缺陷", "補體缺陷"],
     "SCID ADA IL2RG common gamma chain RAG FOXN1 BTK XLA CD40L hyper IgM CVID LAD CGD complement IL-12 IFN-gamma IL-17 STAT3",
     "用 T／B／NK 剩下誰來推缺陷：<strong>γc → T−B+NK−</strong>、<strong>RAG → T−B−NK+</strong>、<strong>ADA → 全部沒有</strong>；再用感染型態對應：化膿菌 → 抗體／補體／吞噬細胞，Neisseria → MAC。"),
 slide("slide-scid-map", "immunodeficiency", "SCID 的缺陷位置（Janeway Fig 13.2）", ["SCID"],
       "SCID T cell B cell development defects thymus bone marrow ADA RAG IL-7R JAK3",
       "骨髓與胸腺裡淋巴球發育的每一步，紅框標出會造成 SCID 的基因（ADA、γc、JAK3、IL-7Rα、RAG、Artemis…）。", IMDEF, 8, box=(0.57, 0.19, 1.0, 0.99)),
 slide("slide-xla", "immunodeficiency", "XLA：B 細胞卡在 pre-B", ["抗體缺陷"],
       "X-linked agammaglobulinemia BTK pre-B cell carrier female X inactivation",
       "BTK 缺陷的男孩 B 細胞發育停在 pre-B；女性帶因者的 B 細胞全部是正常 X 那一條（不隨機的 X 去活化）（Janeway Fig 13.6）。", IMDEF, 14, box=(0.47, 0.18, 1.0, 0.99)),
 slide("slide-hyper-igm", "immunodeficiency", "Hyper-IgM：沒有 CD40L 就沒有生發中心", ["抗體缺陷"],
       "hyper IgM CD40L CD40 germinal center class switch macrophage activation",
       "CD40L 缺陷 → B 細胞不能 class switch（只有 IgM）、淋巴結沒有生發中心、巨噬細胞也活化不了（Janeway Fig 13.7、13.8）。", IMDEF, 15, box=(0.0, 0.535, 0.53, 0.99)),
 # ---------------- 過敏
 svg("hypersensitivity-types", "hypersensitivity", "四型過敏反應", ["過敏反應"],
     "hypersensitivity type I II III IV IgE mast cell cytotoxic immune complex delayed type Arthus serum sickness granuloma",
     "I 型 IgE＋mast cell（幾分鐘）、II 型抗體打細胞（輸血反應、新生兒溶血）、III 型免疫複合物沉積（Arthus、serum sickness）、IV 型 T 細胞（結核菌素試驗、肉芽腫）。"),
 # ---------------- 葡萄球菌、鏈球菌
 svg("gpc-id", "staph-strep", "G(+) 球菌鑑別流程", ["鑑別流程"],
     "catalase coagulase hemolysis alpha beta gamma Lancefield bacitracin CAMP optochin bile soluble Enterococcus",
     "<strong>Catalase</strong> 分葡萄球菌與鏈球菌 → <strong>coagulase</strong> 分出 S. aureus → 鏈球菌看<strong>溶血</strong>：β 用 Lancefield（A bacitracin、B CAMP）、α 用 optochin、γ 是腸球菌。"),
 # ---------------- 腸桿菌科
 slide("slide-entero-antigens", "enterobacteriaceae", "腸桿菌科的抗原：O、H、K", ["抗原與毒力"],
       "O antigen H antigen flagella K antigen capsule Vi LPS lipid A enterobacteriaceae serotyping",
       "<strong>O</strong>：LPS 的多醣側鏈；<strong>H</strong>：鞭毛；<strong>K</strong>：莢膜（Salmonella Typhi 的 Vi）。Lipid A 是內毒素的活性部分。", ENTE, 7, media="image10.jpeg"),
 slide("slide-lps-effects", "enterobacteriaceae", "LPS（內毒素）引起的全身反應", ["抗原與毒力"],
       "LPS endotoxin TNF IL-1 fever shock DIC complement hypotension",
       "Lipid A → 巨噬細胞釋放 <strong>TNF、IL-1</strong> → 發燒；補體、凝血活化 → <strong>低血壓、休克、DIC</strong>。", ENTE, 9, media="image15.jpeg"),
 slide("slide-epec-pedestal", "enterobacteriaceae", "EPEC／EHEC 的 attaching & effacing", ["致病性 E. coli"],
       "EPEC EHEC pedestal Tir intimin type III secretion attaching effacing lesion",
       "第三型分泌系統把 <strong>Tir</strong> 打進腸細胞，Tir 再當 <strong>intimin</strong> 的受體 → 肌動蛋白聚合成<strong>台座（pedestal）</strong>，微絨毛被抹平。", ENTE, 17, media="image22.png"),
 slide("slide-ecoli-virulence", "enterobacteriaceae", "各型致病性 E. coli 的黏附素與毒素", ["致病性 E. coli"],
       "ETEC EPEC EAEC STEC EIEC uropathogenic adhesins exotoxins LT ST Shiga toxin P pili",
       "ETEC：<strong>LT、ST</strong>（旅行者腹瀉）；EPEC：BFP、intimin；STEC：<strong>Shiga toxin</strong>；EIEC：侵入性質體；UPEC：<strong>P pili</strong>。", ENTE, 19, media="image25.jpg"),
 slide("slide-shiga-toxin", "enterobacteriaceae", "Shiga toxin 的作用：切 60S", ["Shigella", "致病性 E. coli"],
       "Shiga toxin Gb3 endosome Golgi ER retrograde 60S ribosome protein synthesis HUS",
       "B 次單元結合 <strong>Gb3</strong> → 逆向運輸經高基氏體到 ER → A 次單元切 <strong>60S rRNA</strong> → 蛋白質合成停止；腎臟內皮受損 → <strong>HUS</strong>。", ENTE, 28, media="image39.jpeg"),
 # ---------------- Bacillus 等
 svg("ab-toxins", "bacillus", "炭疽毒素與白喉毒素", ["Bacillus anthracis", "Corynebacterium diphtheriae"],
     "anthrax toxin protective antigen edema factor lethal factor MEK cAMP diphtheria toxin EF-2 ADP-ribosylation",
     "炭疽：<strong>PA＋EF</strong> = 水腫毒素（cAMP↑）、<strong>PA＋LF</strong> = 致死毒素（切 MEK）；白喉：A 次單元 <strong>ADP-ribosylate EF-2</strong> → 停止蛋白質合成。"),
 slide("slide-cereus-forms", "bacillus", "B. cereus：嘔吐型 vs 腹瀉型", ["Bacillus cereus"],
       "Bacillus cereus emetic diarrheal fried rice heat stable heat labile enterotoxin",
       "<strong>嘔吐型</strong>：炒飯、潛伏期 &lt;6 小時、<strong>耐熱</strong>毒素；<strong>腹瀉型</strong>：肉類蔬菜、&gt;6 小時、不耐熱毒素。", BACI, 15, media="image29.jpeg"),
 slide("slide-listeria-cycle", "bacillus", "Listeria 的胞內生活：ActA 肌動蛋白尾巴", ["Listeria monocytogenes"],
       "Listeria internalin E-cadherin listeriolysin O LLO ActA actin cell-to-cell spread",
       "Internalin 結合 E-cadherin 進入 → <strong>LLO</strong> 破開吞噬泡 → 在細胞質複製 → <strong>ActA</strong> 聚合肌動蛋白當推進器 → 直接鑽到鄰近細胞，不必出來面對抗體。", BACI, 19, media="image34.png"),
 slide("slide-ab-toxin-table", "bacillus", "細菌 A-B 毒素總表", ["Corynebacterium diphtheriae"],
       "A-B toxins anthrax pertussis botulinum cholera diphtheria heat-labile enterotoxin Pseudomonas exotoxin A Shiga tetanus target cell receptor",
       "炭疽、百日咳、肉毒、霍亂、白喉、LT、綠膿桿菌外毒素 A、Shiga、破傷風：基因位置（質體、噬菌體、染色體）、受體與作用。", BACI, 35, media="image70.png"),
 # ---------------- Neisseria、Vibrio…
 slide("slide-cholera-toxin", "neisseria", "霍亂毒素與 LT：cAMP↑ → 米湯樣腹瀉", ["Vibrio"],
       "cholera toxin LT GM1 ganglioside adenylate cyclase cAMP chloride secretion rice water diarrhea",
       "B 次單元結合 <strong>GM1</strong> → A1 ADP-ribosylate Gs → <strong>adenylate cyclase 持續活化 → cAMP↑</strong> → Cl⁻、水大量分泌 → 米湯樣腹瀉。ETEC 的 LT 機轉相同。", ENTE, 39, media="image60.jpeg"),
 # ---------------- 真菌
 svg("fungal-forms", "fungi", "真菌的基本型態與孢子", ["真菌定義與構造", "生活史與分類"],
     "yeast pseudohyphae septate hyphae coenocytic Zygomycota dimorphism 25 37 conidia arthrospore chlamydospore sporangiospore",
     "酵母（出芽）、假菌絲（Candida）、有隔菌絲（Aspergillus）、無隔菌絲（Mucor）；<strong>雙型性真菌 25°C 黴菌、37°C 酵母</strong>。"),
]

figs = json.load(open(f"{ROOT}/figures.json", encoding="utf-8"))
new_ids = {f["id"] for f in NEW}
figs = [f for f in figs if f["id"] not in new_ids] + NEW
order = {c["id"]: i for i, c in enumerate(json.load(open(f"{ROOT}/subject.json", encoding="utf-8"))["chapters"])}
figs = sorted(figs, key=lambda f: order.get(f["chapter"], 999))   # sorted 是穩定排序，同章節保留原順序
json.dump(figs, open(f"{ROOT}/figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"{ROOT}/figures.json", "a").write("\n")
print(len(figs), "figures total,", len(NEW), "added/updated")
