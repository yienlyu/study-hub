#!/usr/bin/env python3
"""寄蟲生活史觀念圖 → subjects/parasitology/figures/<id>.svg

每隻蟲一張「生活史流程」SVG，用格線排版：節點放在 (col, row)，箭頭自動走直線或 L 形。
樣式只用 assets/style.css 的 figure class（.bx .bw .bv .br .bp .ln .lr …），所以會跟著深淺色切換。
顏色慣例：黃框 = 感染期、紫框 = 成蟲寄生處、紅框 = 致病／臨床重點、灰框 = 補充。
說明文字（figures.json 的 title、caption）寫在 build_para_figures.py。
執行：python3 tools/build_para_cycles.py（在 repo 根目錄），再跑 build_para_figures.py。
"""
import html

OUT = "subjects/parasitology/figures"
X0, CH, GX, GY = 14, 54, 30, 44


class D:
    def __init__(self, id, cols, rows, cw=150, label="", top=False, legend=None):
        self.id, self.cols, self.rows, self.cw, self.label = id, cols, rows, cw, label
        self.legend = legend or (("bw", "感染期"), ("bv", "成蟲寄生處"), ("br", "致病／臨床"))
        self.y0 = 64 if top else 34  # top=True：第一列上方留一條回頭箭頭的路
        self.nodes, self.edges, self.zones, self.notes = {}, [], [], []

    # 格線座標
    def nx(self, c): return X0 + c * (self.cw + GX)
    def ny(self, r): return self.y0 + r * (CH + GY)

    def n(self, key, c, r, title, sub="", tip="", cls="bx", span=1, sub_cls=""):
        x, y = self.nx(c), self.ny(r)
        w = span * self.cw + (span - 1) * GX
        self.nodes[key] = dict(x=x, y=y, w=w, h=CH, cx=x + w / 2, cy=y + CH / 2,
                               title=title, sub=sub, tip=tip, cls=cls, sub_cls=sub_cls)
        for t, fs in ((title, 13), (sub, 11)):
            if t and twidth(t, fs) > w - 10:
                print(f"  ! {self.id}/{key}: 「{t}」太長（{twidth(t, fs):.0f} > {w - 10}）")

    def e(self, a, b, how="", label="", cls="ln", pts=None, lpos=None):
        self.edges.append(dict(a=a, b=b, how=how, label=label, cls=cls, pts=pts, lpos=lpos))

    def top_loop(self, a, b, label):
        """從 a 往上、沿第一列上方走回 b（例如：最後一站被最終宿主吃掉）"""
        A, B = self.nodes[a], self.nodes[b]
        y = self.ny(0) - 32
        self.e(a, b, label=label, pts=[(A["cx"], A["y"] - 2), (A["cx"], y), (B["cx"], y), (B["cx"], B["y"] - 2)],
               lpos=(B["cx"] + 12, y - 5))

    def zone(self, c0, c1, r0, r1, label):
        self.zones.append((c0, c1, r0, r1, label))

    def note(self, head, text):
        self.notes.append((head, text))


# 中文蟲名 → 英文學名：節點標題是蟲名時，滑過的說明第一行自動加上學名（考試只出英文學名）
SCI = {
    "蛔蟲": "Ascaris lumbricoides", "鞭蟲": "Trichuris trichiura", "蟯蟲": "Enterobius vermicularis",
    "犬蛔蟲": "Toxocara canis", "肝毛線蟲": "Capillaria hepatica", "菲律賓毛線蟲": "Capillaria philippinensis",
    "鉤蟲": "Ancylostoma duodenale、Necator americanus", "糞小桿線蟲": "Strongyloides stercoralis",
    "旋毛蟲": "Trichinella spiralis", "顎口線蟲": "Gnathostoma spinigerum", "海獸胃線蟲": "Anisakis simplex",
    "廣東住血線蟲": "Angiostrongylus cantonensis",
    "淋巴絲蟲": "Wuchereria bancrofti、Brugia malayi", "班氏絲蟲": "Wuchereria bancrofti", "馬來絲蟲": "Brugia malayi",
    "帝汶絲蟲": "Brugia timori", "羅阿絲蟲": "Loa loa", "蟠尾絲蟲": "Onchocerca volvulus",
    "血絲蟲": "Wuchereria、Brugia、Loa loa、Onchocerca",
    "中華肝吸蟲": "Clonorchis sinensis", "異形・橫川吸蟲": "Heterophyes heterophyes、Metagonimus yokogawai",
    "異形吸蟲": "Heterophyes heterophyes", "橫川吸蟲": "Metagonimus yokogawai",
    "異形異形吸蟲": "Heterophyes heterophyes", "橫川異形吸蟲": "Metagonimus yokogawai",
    "衛氏肺吸蟲": "Paragonimus westermani", "薑片蟲": "Fasciolopsis buski", "牛羊肝吸蟲": "Fasciola hepatica",
    "血吸蟲": "Schistosoma japonicum、S. mansoni、S. haematobium", "日本血吸蟲": "Schistosoma japonicum",
    "曼森血吸蟲": "Schistosoma mansoni", "埃及血吸蟲": "Schistosoma haematobium",
    "棘口吸蟲": "Echinostoma spp.", "人雙口吸蟲": "Gastrodiscoides hominis", "胰臟吸蟲": "Eurytrema pancreaticum",
    "槍狀肝吸蟲": "Dicrocoelium dendriticum", "貓肝吸蟲": "Opisthorchis felineus",
}


def sci_name(title):
    """標題整個是蟲名（或用「・」連接的幾個蟲名）才回傳學名"""
    if title in SCI:
        return SCI[title]
    parts = title.split("・")
    if len(parts) > 1 and all(p in SCI for p in parts):
        return "；".join(SCI[p] for p in parts)
    return ""


def twidth(s, fs):
    return sum(fs if ord(ch) > 0x2E80 else fs * 0.58 for ch in s)


def esc(s):
    return html.escape(s, quote=True)


def rpath(pts, r=10):
    """折線轉成圓角路徑"""
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        def toward(ax, ay, bx, by, k):
            L = max(abs(bx - ax), abs(by - ay)) or 1
            k = min(k, L / 2)
            return ax + (bx - ax) / L * k, ay + (by - ay) / L * k
        ax, ay = toward(x1, y1, x0, y0, r)
        bx, by = toward(x1, y1, x2, y2, r)
        d += f"L{ax:.0f} {ay:.0f}Q{x1:.0f} {y1:.0f} {bx:.0f} {by:.0f}"
    d += f"L{pts[-1][0]:.0f} {pts[-1][1]:.0f}"
    return d


def route(d, ed):
    A, B = d.nodes[ed["a"]], d.nodes[ed["b"]]
    if ed["pts"]:
        return ed["pts"]
    gap = 2
    if abs(A["cy"] - B["cy"]) < 1:  # 同一列
        if B["cx"] > A["cx"]:
            return [(A["x"] + A["w"] + gap, A["cy"]), (B["x"] - gap, B["cy"])]
        return [(A["x"] - gap, A["cy"]), (B["x"] + B["w"] + gap, B["cy"])]
    down = B["cy"] > A["cy"]
    if abs(A["cx"] - B["cx"]) < 1 or ed["how"] == "v":  # 同一欄
        x = A["cx"] if abs(A["cx"] - B["cx"]) < 1 else B["cx"]
        return [(x, A["y"] + A["h"] + gap if down else A["y"] - gap), (x, B["y"] - gap if down else B["y"] + B["h"] + gap)]
    if ed["how"] == "hv":  # 先橫再直
        right = B["cx"] > A["cx"]
        return [(A["x"] + A["w"] + gap if right else A["x"] - gap, A["cy"]), (B["cx"], A["cy"]),
                (B["cx"], B["y"] - gap if down else B["y"] + B["h"] + gap)]
    # 預設 vh：先直再橫
    right = B["cx"] > A["cx"]
    return [(A["cx"], A["y"] + A["h"] + gap if down else A["y"] - gap), (A["cx"], B["cy"]),
            (B["x"] - gap if right else B["x"] + B["w"] + gap, B["cy"])]


HALO = ' style="paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round"'  # 文字壓在線上時留白
MARK = {"lt": "fk", "ln": "fk", "lr": "fr", "lg": "fg", "lv": "fv"}


def render(d):
    p = d.id
    W = X0 * 2 + d.cols * d.cw + (d.cols - 1) * GX
    grid_bottom = d.ny(d.rows - 1) + CH
    H = grid_bottom + 30 + 20 * len(d.notes) + 22
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{esc(d.label)}">']
    out.append("<defs>" + "".join(
        f'<marker id="{p}-{m}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" class="{m}"/></marker>'
        for m in sorted(set(MARK.values()))) + "</defs>")
    for c0, c1, r0, r1, label in d.zones:
        x, y = d.nx(c0) - 8, d.ny(r0) - 10
        w = d.nx(c1) + d.cw - d.nx(c0) + 16
        h = d.ny(r1) + CH - d.ny(r0) + 20
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="fp"/>')
        out.append(f'<text x="{x + 6}" y="{y - 6}" class="th"{HALO}>{esc(label)}</text>')
    for ed in d.edges:
        pts = route(d, ed)
        cls = ed["cls"].split()
        mk = MARK[cls[0]]
        out.append(f'<path d="{rpath(pts)}" class="{" ".join(cls)}" marker-end="url(#{p}-{mk})"/>')
        if ed["label"]:
            (xa, ya), (xb, yb) = pts[0], pts[1]
            lx, ly = ed["lpos"] or ((xa + xb) / 2, (ya + yb) / 2)
            if ed["lpos"]:
                anchor = "start"
            elif abs(ya - yb) < 1:
                ly -= 6
                anchor = "middle"
            else:
                lx += 6
                anchor = "start"
            out.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" class="ts"{HALO}>{esc(ed["label"])}</text>')
    for k, nd in d.nodes.items():
        x, y, w, cx = nd["x"], nd["y"], nd["w"], nd["cx"]
        ty = y + (22 if nd["sub"] else 32)
        box = f'<rect x="{x}" y="{y}" width="{w}" height="{CH}" rx="10" class="{nd["cls"]}"/><text x="{cx:.0f}" y="{ty}" text-anchor="middle" class="tb">{esc(nd["title"])}</text>'
        sci = sci_name(nd["title"])
        if sci:
            nd["tip"] = f"<i>{sci}</i>" + (f"<br>{nd['tip']}" if nd["tip"] else "")
        if nd["tip"]:
            out.append(f'<g class="hot" data-tip="{esc(nd["tip"]).replace("&lt;", "<").replace("&gt;", ">")}" data-label="{esc(nd["title"])}">{box}</g>')
        else:
            out.append(box)
        if nd["sub"]:
            sc = f"ts {nd['sub_cls']}".strip()
            out.append(f'<text x="{cx:.0f}" y="{y + 41}" text-anchor="middle" class="{sc}">{esc(nd["sub"])}</text>')
    y = grid_bottom + 34
    for head, text in d.notes:
        out.append(f'<text x="{X0}" y="{y}" class="th">{esc(head)}</text><text x="{X0 + 64}" y="{y}" class="ts">{esc(text)}</text>')
        y += 20
    # 圖例
    lx = W - X0 - 330
    for i, (cls, t) in enumerate(d.legend):
        out.append(f'<rect x="{lx + i * 112}" y="{y - 9}" width="14" height="10" rx="3" class="{cls}"/><text x="{lx + i * 112 + 20}" y="{y}" class="ts">{t}</text>')
    out.append("</svg>")
    s = "\n".join(out) + "\n"
    open(f"{OUT}/{d.id}.svg", "w", encoding="utf-8").write(s)
    return W, H


DS = []

# ======================================================== 土源性蠕蟲
d = D("ascaris-cycle", 4, 3, label="蛔蟲生活史：吃入胚胎化蟲卵，小腸孵化後幼蟲穿腸壁經門脈到肝、右心、肺，穿入肺泡後經氣管被吞下，回到小腸長成成蟲；成蟲產的受精卵隨糞便排出，在土壤中胚胎化才有感染力。")
d.zone(0, 0, 0, 1, "土壤")
d.zone(1, 3, 0, 2, "人體")
d.n("emb", 0, 0, "胚胎化蟲卵", "感染期 · 吃入", cls="bw",
    tip="卵在<b>土壤</b>裡約 2–3 週才發育出幼蟲，這時才有感染力；剛排出的卵不會直接傳染（和蟯蟲不同）。來源：被糞便汙染的蔬菜、水、手。")
d.n("hatch", 1, 0, "小腸孵化", "幼蟲穿過腸壁",
    tip="幼蟲在小腸孵出後鑽進腸壁，進入門脈循環。")
d.n("liver", 2, 0, "門脈 → 肝 → 右心", "血流移行")
d.n("lung", 3, 0, "肺：穿入肺泡", "Ascaris pneumonia", cls="br",
    tip="感染後 4 天到 2 週，幼蟲從肺微血管穿進肺泡 → 發燒、咳嗽、<b>血痰</b>、<b>嗜酸性球增多</b>，即 <b>Loeffler syndrome</b>。蛔蟲、鉤蟲、糞小桿線蟲都會經過肺。")
d.n("swallow", 2, 1, "氣管 → 咽 → 吞下", "回到小腸")
d.n("adult", 1, 1, "小腸成蟲", "最大的腸道線蟲", cls="bv",
    tip="雌蟲 20–35 cm、雄蟲尾端捲曲。吃到卵後約 2–3 個月開始產卵，一天可產約 20 萬顆。")
d.n("egg", 0, 1, "卵隨糞便排出", "受精卵／未受精卵",
    tip="<b>受精卵</b>約 60 × 45 µm、厚殼、外有凹凸的<b>蛋白質外套膜</b>；<b>未受精卵</b>約 90 × 40 µm、較長、殼薄。<b>診斷：糞便找蟲卵</b>。")
d.n("ectopic", 1, 2, "腸阻塞、異位移行", "兒童腸阻塞；鑽膽管、胰管", cls="br",
    tip="大量感染 → <b>腸阻塞</b>（兒童常見）。成蟲<b>異位移行</b>到膽管、胰管、膽囊、肝，或往上爬到食道。")
d.e("egg", "emb", label="土壤 2–3 週")
d.e("emb", "hatch", label="吃入")
d.e("hatch", "liver")
d.e("liver", "lung")
d.e("lung", "swallow")
d.e("swallow", "adult")
d.e("adult", "egg")
d.e("adult", "ectopic", cls="lr dash")
d.note("診斷", "糞便找蟲卵（最常用）")
d.note("治療", "Albendazole（結合 β-tubulin）、Mebendazole 或 Ivermectin")
DS.append(d)

d = D("trichuris-cycle", 4, 2, label="鞭蟲生活史：感染途徑是攝入已受精、已胚胎化的蟲卵，在小腸孵化，幼蟲直接到盲腸、大腸長成成蟲，細長的前端埋進黏膜。不經過肺。卵隨糞便排出，在土壤中胚胎化。")
d.zone(0, 0, 0, 1, "土壤")
d.zone(1, 3, 0, 1, "人體")
d.n("emb", 0, 0, "胚胎化受精卵", "感染途徑：攝入", cls="bw",
    tip="感染途徑：<b>攝入已受精的蟲卵</b>（經口，污染的食物、水、手）。受精卵在土壤中約 2–4 週胚胎化才有感染力。")
d.n("hatch", 1, 0, "小腸孵化", "不經過肺",
    tip="和蛔蟲、鉤蟲不同，鞭蟲幼蟲<b>沒有心肺移行</b>，孵化後直接往下到大腸。")
d.n("adult", 2, 0, "盲腸、大腸成蟲", "細長前端埋進黏膜", cls="bv",
    tip="前細後粗，像鞭子；食道是一串 <b>stichocytes</b>（stichosome）。屬 Aphasmid nematode。")
d.n("clin", 3, 0, "直腸脫垂", "重度感染的幼童", cls="br",
    tip="多數無症狀；大量感染（尤其幼童）→ 腹痛、腹瀉、<b>直腸脫垂</b>、生長遲緩。")
d.n("egg", 2, 1, "卵隨糞便排出", "桶狀、兩端極塞",
    tip="50–54 × 22 µm、<b>桶狀</b>、兩端各一個透明的<b>極塞（polar plug）</b>、黃褐色；排出時<b>還沒胚胎化</b>。")
d.n("soil", 0, 1, "土壤中胚胎化", "約 2–4 週")
d.e("emb", "hatch", label="吃入")
d.e("hatch", "adult")
d.e("adult", "clin", cls="lr dash")
d.e("adult", "egg")
d.e("egg", "soil")
d.e("soil", "emb")
d.note("診斷", "糞便找蟲卵；輕度感染用濃縮法，Kato-Katz 定量")
d.note("治療", "Mebendazole 首選，Albendazole 替代")
DS.append(d)

d = D("hookworm-cycle", 4, 2, label="鉤蟲生活史：卵隨糞便排出，在土壤孵出桿狀幼蟲，再發育成有鞘的絲狀幼蟲（感染期），赤腳時鑽入皮膚，經血流到肺、氣管被吞下，在小腸長成成蟲咬住腸壁吸血，造成缺鐵性貧血。")
d.zone(0, 3, 0, 0, "人體")
d.zone(0, 3, 1, 1, "土壤")
d.n("skin", 0, 0, "鑽皮膚", "ground itch", cls="br",
    tip="L3 鑽入皮膚處搔癢起疹 → <b>ground itch</b>。動物鉤蟲（巴西鉤蟲）只會在皮下亂鑽 → <b>皮膚幼蟲移行症（CLM）</b>。")
d.n("lung", 1, 0, "血流 → 肺 → 吞下", "心肺移行",
    tip="和蛔蟲一樣經過肺，可有咳嗽、Loeffler 樣症狀。")
d.n("adult", 2, 0, "小腸成蟲", "咬住腸壁吸血", cls="bv",
    tip="十二指腸鉤蟲：<b>2 對牙齒</b>、雌蟲有尾刺；美洲鉤蟲：<b>一對切板</b>。可有<b>發育停滯（hypobiosis）</b>，潛伏期拉長。")
d.n("clin", 3, 0, "缺鐵性貧血", "異食癖（pica）", cls="br",
    tip="成蟲咬住腸壁造成慢性失血 → <b>缺鐵性貧血</b>（最常見）、異食癖，嚴重時心臟併發症。")
d.n("egg", 2, 1, "卵隨糞便排出", "薄殼、內有分裂細胞",
    tip="56–76 × 36–40 µm、<b>殼很薄、透明</b>；各種鉤蟲卵分不出來，跑台寫 hookworm 即可。")
d.n("l1", 1, 1, "桿狀幼蟲 L1", "土壤孵化")
d.n("l3", 0, 1, "絲狀幼蟲 L3", "有鞘 · 感染期", cls="bw",
    tip="<b>絲狀幼蟲（filariform）</b>是感染期，赤腳踩到潮濕土壤時鑽入皮膚。<b>十二指腸鉤蟲也可以經口感染</b>。")
d.e("skin", "lung")
d.e("lung", "adult")
d.e("adult", "clin", cls="lr dash")
d.e("adult", "egg")
d.e("egg", "l1")
d.e("l1", "l3")
d.e("l3", "skin", label="赤腳")
d.note("診斷", "糞便找蟲卵；洋菜平板的爬行痕跡要 3–5 天、不規則")
d.note("治療", "Albendazole；Mebendazole、pyrantel pamoate")
DS.append(d)

# ======================================================== 蟯蟲與犬蛔蟲
d = D("enterobius-cycle", 4, 2, label="蟯蟲生活史：吃入感染性蟲卵，小腸孵化，在盲腸附近長成成蟲；懷孕雌蟲夜間爬到肛門周圍產卵，卵約 6 小時就有感染力，抓癢後經手到口自體再感染。人是唯一宿主。")
d.zone(0, 2, 0, 0, "腸道")
d.zone(0, 2, 1, 1, "肛門周圍 · 手 · 寢具")
d.n("ingest", 0, 0, "吃入感染性卵", "手 → 口、灰塵", cls="bw",
    tip="卵沾在手指、指甲、寢具、衣物、灰塵上 → 吃進或吸入。人是<b>唯一宿主</b>，所以家人、同學之間很容易互相傳染。")
d.n("hatch", 1, 0, "小腸孵化", "往下移動")
d.n("adult", 2, 0, "盲腸附近成蟲", "♂ 交配後死亡", cls="bv",
    tip="♀ 8–13 mm、♂ 2–5 mm；有<b>頸翼</b>與<b>食道球</b>。不經過肺。")
d.n("female", 2, 1, "雌蟲夜間爬出產卵", "肛門周圍", cls="br",
    tip="懷孕的雌蟲<b>晚上爬到肛門外</b>產卵 → <b>夜間肛門搔癢</b>、抓破續發感染；偶爾跑進女性生殖道或闌尾。")
d.n("egg", 1, 1, "卵 6 小時有感染力", "D 字形、不對稱",
    tip="約 55 × 26 µm、<b>一側扁平一側凸</b>、透明，內有幼蟲。卵在肛門周圍孵出的幼蟲也可能<b>爬回肛門（retroinfection）</b>。")
d.n("auto", 0, 1, "抓癢 → 自體再感染", "手指、指甲", cls="br",
    tip="不需要土壤，直接手 → 口就能再感染，所以要<b>全家一起治療</b>、剪指甲、洗曬寢具。")
d.n("dx", 3, 1, "診斷：肛圍擦拭法", "早上、排便洗澡前", cls="bp",
    tip="<b>Scotch tape test</b>，準確率 > 90%。卵產在肛門外，<b>糞便找到卵的機會 < 5%</b> → 題目問糞便檢查不要選。")
d.n("tx", 3, 0, "Pyrantel pamoate", "治療 · 全家一起吃", cls="bp")
d.e("ingest", "hatch")
d.e("hatch", "adult")
d.e("adult", "female", label="夜間")
d.e("female", "egg")
d.e("egg", "auto")
d.e("auto", "ingest")
d.e("female", "dx", cls="ln dash")
DS.append(d)

d = D("toxocara-cycle", 4, 2, label="犬蛔蟲生活史：成蟲在狗的小腸，卵隨狗糞排出，在土壤中 2–5 週胚胎化。人吃入胚胎化卵，或吃生的雞、羊、兔等保幼宿主組織，幼蟲在體內移行但不會長成成蟲，造成內臟、眼、神經型犬蛔蟲症。")
d.zone(0, 1, 0, 0, "狗（最終宿主）")
d.zone(0, 1, 1, 1, "土壤")
d.zone(2, 3, 0, 1, "人（保幼宿主）")
d.n("adult", 0, 0, "狗小腸成蟲", "幼犬感染最重", cls="bv",
    tip="<i>T. canis</i> 在狗、<i>T. cati</i> 在貓。幼犬還可經<b>胎盤、乳汁</b>感染。")
d.n("pass", 1, 0, "狗吃入胚胎化卵", "或吃到保幼宿主")
d.n("egg", 0, 1, "卵隨狗糞排出", "球形厚殼、表面凹洞",
    tip="80–85 µm、蛋白膜表面像高爾夫球的<b>凹洞</b>。")
d.n("emb", 1, 1, "胚胎化卵", "2–5 週 · 可活 1 年", cls="bw",
    tip="公園土壤、<b>沙坑</b>常被汙染。蟲卵排出後約 2–5 週才有感染力，可存活至少 1 年。")
d.n("human", 2, 1, "人吃入", "沙坑、生菜、手",
    tip="誤食被汙染的土壤、食物、水中的胚胎化卵；小孩玩沙最常見。")
d.n("para", 3, 1, "生吃雞、羊、兔肝", "保幼宿主組織", cls="bw",
    tip="日本、韓國病例多半是吃生的雞肝、牛肝等保幼宿主組織裡的幼蟲。")
d.n("larva", 2, 0, "幼蟲在體內亂鑽", "不會長成成蟲", cls="br",
    tip="人是<b>保幼宿主</b>：幼蟲（350–445 µm）像<b>生物子彈</b>，多停在<b>肝</b>，也去肺、肌肉、眼、腦。<b>人的糞便找不到犬蛔蟲卵</b>。")
d.n("type", 3, 0, "VLM・OLM・NT", "＋隱蔽型 · 四大類型", cls="br",
    tip="<b>內臟幼蟲移行症（VLM）</b>、<b>眼部（OLM）</b>：可能失明，常被誤認為 retinoblastoma；<b>神經性（NT）</b>；<b>隱蔽性</b>。")
d.e("adult", "egg")
d.e("egg", "emb", label="土壤")
d.e("emb", "pass", how="v")
d.e("pass", "adult")
d.e("emb", "human")
d.e("para", "larva", how="hv")
d.e("human", "larva")
d.e("larva", "type", cls="lr dash")
d.note("診斷", "TES-ELISA（有交叉反應）→ TES-Western blot 24–35 kDa 確認；PCR")
d.note("治療", "Albendazole ＋ 類固醇（眼部）")
DS.append(d)

# ======================================================== 毛線蟲
d = D("capillaria-cycles", 4, 4, label="兩種毛線蟲生活史對照。菲律賓毛線蟲：生吃淡水魚吃到幼蟲，小腸黏膜成蟲產有殼卵與無殼卵，無殼卵在腸內孵化造成自體感染；有殼卵隨糞便到水中被魚吃。肝毛線蟲：成蟲與卵在鼠肝，卵要等宿主被吃掉或死亡分解才進入土壤胚胎化，人吃入胚胎化卵才是真感染；吃到鼠肝而在糞便看到卵是假感染。")
d.zone(0, 3, 0, 1, "菲律賓毛線蟲 · 腸道型")
d.zone(0, 3, 2, 3, "肝毛線蟲 · 肝臟型")
d.n("fish", 0, 0, "生吃淡水小魚", "魚體內幼蟲 · 感染期", cls="bw",
    tip="菲律賓、泰國流行；台灣東部阿美族病例多。吃生的或沒煮熟的魚。")
d.n("adult", 1, 0, "小腸黏膜成蟲", "", cls="bv")
d.n("eggs", 2, 0, "產兩種卵", "有殼卵／無殼卵",
    tip="雌蟲可產<b>有殼卵</b>（隨糞便排出）或<b>無殼卵</b>（在腸內直接孵化）。")
d.n("out", 3, 0, "有殼卵隨糞便", "花生形、淺極塞",
    tip="35–45 µm、<b>花生形</b>、殼有放射紋、兩端極塞很淺。")
d.n("auto", 1, 1, "腸內孵化 → 自體感染", "蟲數暴增、蛋白流失", cls="br",
    tip="<b>自體感染</b> → 蟲越來越多 → 嚴重腹瀉、<b>蛋白質流失性腸病</b>、惡病質甚至死亡。治療 Mebendazole。")
d.n("fishih", 3, 1, "水中胚胎化 → 魚吃", "魚是中間宿主")
d.e("fish", "adult")
d.e("adult", "eggs")
d.e("eggs", "out")
d.e("eggs", "auto", label="無殼卵")
d.e("auto", "adult", cls="lr", how="v")
d.e("out", "fishih")
f = d.nodes
d.e("fishih", "fish", pts=[(f["fishih"]["cx"], f["fishih"]["y"] + CH + 2), (f["fishih"]["cx"], f["fishih"]["y"] + CH + 16),
                            (f["fish"]["cx"], f["fishih"]["y"] + CH + 16), (f["fish"]["cx"], f["fish"]["y"] + CH + 2)])
d.n("rat", 0, 2, "鼠肝：成蟲與卵", "卵留在肝實質", cls="bv",
    tip="成蟲住在大鼠等動物的<b>肝臟</b>，卵<b>不會</b>隨糞便排出。")
d.n("release", 1, 2, "被吃掉或死亡分解", "卵才離開肝臟",
    tip="① 被另一隻動物吃掉 → 卵經消化釋出、隨牠的糞便排出；② 動物死亡分解 → 卵散到土壤。")
d.n("soil", 2, 2, "土壤中胚胎化", "")
d.n("ingest", 3, 2, "吃入胚胎化卵", "真正的感染", cls="bw")
d.n("liver", 3, 3, "孵化 → 門脈 → 肝", "肝炎 ＋ 嗜酸性球", cls="br",
    tip="急性或亞急性<b>肝炎合併嗜酸性球增多</b>，可能致命。<b>診斷靠肝臟切片或解剖</b>。")
d.n("spur", 0, 3, "吃到病鼠肝 → 糞便見卵", "過誤性寄生（假感染）", cls="br",
    tip="卵只是<b>路過</b>腸道（沒胚胎化、不會孵化），停止吃這些內臟後糞便就不再有卵。老師的例子：三杯鼠內臟。")
d.e("rat", "release")
d.e("release", "soil")
d.e("soil", "ingest")
d.e("ingest", "liver")
d.e("rat", "spur", cls="ln dash")
DS.append(d)

# ======================================================== 食源性線蟲
d = D("trichinella-cycle", 4, 2, label="旋毛蟲生活史：吃入肌肉中的被囊幼蟲，胃酸釋出幼蟲後在小腸長成成蟲；雌蟲約一週後直接產幼蟲，幼蟲經血流到橫紋肌形成包囊。同一隻宿主既是最終宿主也是中間宿主，要被下一隻動物吃掉才能繼續。")
d.zone(1, 3, 0, 1, "同一隻宿主 = 最終宿主 ＋ 中間宿主")
d.n("meat", 0, 0, "吃入肌肉被囊幼蟲", "感染期", cls="bw",
    tip="生的或沒煮熟的<b>豬肉、野味（熊、野豬）</b>。被囊幼蟲同時是<b>感染期也是診斷期</b>。")
d.n("adult", 1, 0, "小腸成蟲", "約活 4 週", cls="bv",
    tip="胃酸與 pepsin 釋出幼蟲 → 鑽進小腸黏膜長成成蟲（♀ 2.2 mm、♂ 1.2 mm）。腸道期：腹瀉、腹痛、嘔吐。")
d.n("nb", 2, 0, "雌蟲直接產幼蟲", "不是卵 · 約 1 週後",
    tip="胎生（larviparous）：產的是<b>新生幼蟲</b>，所以糞便找不到卵。")
d.n("blood", 3, 0, "血流 → 橫紋肌", "肌肉期症狀", cls="br",
    tip="<b>眼眶周圍與臉部水腫</b>、發燒、<b>肌肉痛</b>、<b>指甲下裂片狀出血</b>、嗜酸性球增多；嚴重時<b>心肌炎</b>、腦炎。")
d.n("cyst", 3, 1, "肌肉被囊幼蟲", "nurse cell · 活數年", cls="bw",
    tip="幼蟲捲在 nurse cell 裡，可存活好幾年。<i>T. pseudospiralis</i> 不形成包囊。<b>確診：肌肉切片</b>。")
d.n("next", 1, 1, "被下一隻動物吃掉", "人通常是終點",
    tip="<b>鼠</b>維持流行；豬、熊等雜食或肉食動物吃到被感染的鼠或肉。人是意外感染，吃人的動物很少，所以人是死路。")
d.e("meat", "adult")
d.e("adult", "nb")
d.e("nb", "blood")
d.e("blood", "cyst")
d.e("cyst", "next")
d.e("next", "meat", how="hv")
d.note("診斷", "臨床 ＋ 嗜酸性球增多 → 抗體、肌肉切片")
d.note("治療", "Albendazole／Mebendazole（早用）＋ 類固醇；預防：豬肉煮到 71 °C")
DS.append(d)

d = D("gnathostoma-cycle", 4, 2, top=True, label="顎口線蟲生活史：成蟲在貓狗胃壁，卵隨糞便入水孵出幼蟲，被劍水蚤吃，再被魚、蛙、蛇等第二中間宿主吃，發育成進階第三期幼蟲。貓狗吃入後長成成蟲；人吃入生魚、泥鰍、蛙是非適合宿主，幼蟲在體內到處移行。")
d.zone(0, 3, 0, 0, "動物間的循環")
d.zone(0, 3, 1, 1, "人（非適合宿主）")
d.n("adult", 0, 0, "貓狗胃壁成蟲", "最終宿主", cls="bv",
    tip="<i>G. spinigerum</i>：貓、狗（最常見）；<i>G. hispidum</i>：豬；<i>G. doloresi</i>：野豬；<i>G. nipponicum</i>：黃鼠狼。")
d.n("egg", 1, 0, "卵入水孵出 L1", "")
d.n("cope", 2, 0, "劍水蚤（1st IH）", "L1 → 早期 L3")
d.n("fish", 3, 0, "魚、泥鰍、蛙、蛇", "進階 L3 · 感染期", cls="bw",
    tip="第二中間宿主；雞、鴨、蛇等也可當<b>保幼宿主</b>。")
d.n("human", 3, 1, "人生吃", "生吞泥鰍、生魚片",
    tip="台灣病例：有錢人<b>生吞泥鰍</b>養生；泰國吃生魚的料理。")
d.n("migr", 2, 1, "幼蟲不成熟、到處移行", "非適合宿主", cls="br",
    tip="人體內多是<b>進階 L3</b>或很年輕的成蟲，頭球有 4 排小鉤。")
d.n("clin", 1, 1, "遊走性皮下腫脹", "CLM、VLM、OLM、NLM", cls="br",
    tip="<b>皮膚型最常見</b>：軀幹、上肢間歇性遊走性腫脹；神經型可造成致命的<b>嗜酸性腦膜炎、脊髓腦炎</b>；眼型可能失明。")
d.n("dx", 0, 1, "取出蟲體＝診斷＋治療", "", cls="bp")
d.e("adult", "egg")
d.e("egg", "cope")
d.e("cope", "fish")
d.e("fish", "human")
d.e("human", "migr")
d.e("migr", "clin")
d.e("clin", "dx", cls="ln dash")
d.top_loop("fish", "adult", "貓狗吃入")
DS.append(d)

d = D("anisakis-cycle", 4, 2, top=True, label="海獸胃線蟲生活史：成蟲在鯨、海豚胃裡，卵隨糞便入海孵出幼蟲，被磷蝦等甲殼類吃，再被海魚、魷魚吃，第三期幼蟲留在內臟與肌肉。人生吃海鮮是意外宿主，幼蟲鑽胃壁造成劇烈胃痛，但不會長成成蟲。")
d.zone(0, 3, 0, 0, "海洋")
d.zone(1, 3, 1, 1, "人（意外宿主）")
d.n("whale", 0, 0, "鯨、海豚胃：成蟲", "最終宿主", cls="bv")
d.n("egg", 1, 0, "卵入海孵出幼蟲", "")
d.n("krill", 2, 0, "磷蝦等甲殼類", "中間宿主 · 發育成 L3")
d.n("fish", 3, 0, "海魚、魷魚", "L3 · 感染期", cls="bw",
    tip="鯖魚、鮭魚、鱈魚、鯡魚、魷魚；L3 約 <b>2 cm</b>，尾端有<b>尾突（mucron）</b>，橫切面 <b>Y 字形側索</b>。魚是<b>保幼宿主</b>。")
d.n("human", 3, 1, "人生吃海鮮", "生魚片、醃鯡魚",
    tip="全球 > 90% 在<b>日本</b>；荷蘭首例吃生鯡魚。<b>Wasabi 殺不死幼蟲</b>。")
d.n("stomach", 2, 1, "L3 鑽胃壁", "約 6 小時後劇烈上腹痛", cls="br",
    tip="<b>胃型最常見</b>（胃體大彎），還有腸型、腸外型、<b>過敏型</b>。<i>Pseudoterranova</i> 常造成喉嚨刺痛。")
d.n("scope", 1, 1, "胃鏡夾出", "診斷＝治療", cls="bp")
d.e("whale", "egg")
d.e("egg", "krill")
d.e("krill", "fish")
d.e("fish", "human")
d.e("human", "stomach")
d.e("stomach", "scope", cls="ln dash")
d.top_loop("fish", "whale", "被鯨、海豚吃")
DS.append(d)

d = D("acanton-cycle", 4, 2, label="廣東住血線蟲生活史：成蟲在鼠的肺動脈，卵孵出第一期幼蟲經氣管吞下隨鼠糞排出，被螺、蛞蝓吃進去發育成第三期幼蟲。鼠吃螺後幼蟲先到腦發育再回肺動脈。人吃生螺、保幼宿主或被黏液汙染的生菜，幼蟲跑到腦造成嗜酸性腦膜炎，不會成熟。")
d.zone(0, 1, 0, 1, "鼠（最終宿主）")
d.zone(2, 3, 0, 0, "中間宿主與保幼宿主")
d.zone(2, 3, 1, 1, "人（非適合宿主）")
d.n("rat", 0, 0, "鼠肺動脈：成蟲", "rat lungworm", cls="bv",
    tip="卵卡在肺動脈末梢孵出 L1 → 穿進肺泡 → 氣管 → 吞下 → <b>L1 隨鼠糞排出</b>。")
d.n("l1", 1, 0, "L1 隨鼠糞排出", "")
d.n("snail", 2, 0, "螺、蛞蝓：L1 → L3", "非洲大蝸牛 · 感染期", cls="bw",
    tip="<b>非洲大蝸牛 <i>Achatina fulica</i></b>、福壽螺 <i>Pila</i>、蛞蝓。L3 也在螺的<b>黏液</b>裡，會汙染生菜。")
d.n("para", 3, 0, "保幼宿主", "淡水蝦、陸蟹、青蛙", cls="bw",
    tip="「吃淡水蝦會得哪些寄生蟲？」別漏掉廣東住血線蟲。")
d.n("human", 3, 1, "人生吃", "螺、蝦、蟹、生菜")
d.n("brain", 2, 1, "幼蟲到腦 → 死在腦", "嗜酸性腦膜炎", cls="br",
    tip="潛伏期 1–5 週；頭痛、頸僵硬、腦神經麻痺。<b>CSF 嗜酸性球增多</b>是診斷關鍵。多數自癒，<b>不建議用驅蟲藥</b>。")
d.n("ratcns", 0, 1, "鼠：幼蟲先到腦發育", "再經靜脈回肺動脈",
    tip="在鼠的 CNS 發育 2–3 週 → 蜘蛛膜下腔 → 靜脈 → 肺動脈成熟；感染 40–60 天後鼠糞出現 L1。")
d.e("rat", "l1")
d.e("l1", "snail")
d.e("snail", "para", label="被吃")
d.e("para", "human")
d.e("human", "brain")
sn, rc = d.nodes["snail"], d.nodes["ratcns"]
mid = sn["y"] + CH + 12
d.e("snail", "ratcns", label="鼠吃螺", pts=[(sn["cx"], sn["y"] + CH + 2), (sn["cx"], mid), (rc["cx"] + 30, mid), (rc["cx"] + 30, rc["y"] - 2)],
    lpos=(rc["cx"] + 120, mid + 13))
d.e("ratcns", "rat")
d.note("診斷", "CSF 嗜酸性球 > 10%（常 20–90%）、Charcot-Leyden 結晶；血清學")
d.note("預防", "不生吃螺、蝦、蟹；摸蝸牛後用肥皂洗手")
DS.append(d)

# ======================================================== 血絲蟲
d = D("filaria-cycle", 4, 4, top=True, cw=170, label="血絲蟲生活史與三類血絲蟲比較：病媒吸血時注入第三期幼蟲，在人體長成成蟲，雌蟲產微絲蚴，病媒再吸血時吸走微絲蚴，在病媒體內 1 到 2 週發育成第三期幼蟲。淋巴絲蟲由蚊傳播、成蟲在淋巴管、微絲蚴夜間在血液；羅阿絲蟲由斑虻傳播、成蟲在皮下移行、微絲蚴白天在血液；蟠尾絲蟲由黑蠅傳播、成蟲在皮下結節、微絲蚴在皮膚與眼睛。")
d.zone(0, 3, 0, 0, "共同的生活史")
d.zone(0, 3, 1, 1, "淋巴絲蟲 W. bancrofti、B. malayi")
d.zone(0, 3, 2, 2, "羅阿絲蟲 Loa loa（非洲眼蟲）")
d.zone(0, 3, 3, 3, "蟠尾絲蟲 Onchocerca volvulus")
d.n("bite", 0, 0, "病媒叮咬注入 L3", "感染期都是 L3", cls="bw",
    tip="所有血絲蟲都靠<b>節肢動物</b>傳播，感染期都是<b>第三期幼蟲</b>。")
d.n("adult", 1, 0, "人體組織內成蟲", "活好幾年", cls="bv")
d.n("mf", 2, 0, "雌蟲產微絲蚴", "是幼蟲、不是卵")
d.n("vec", 3, 0, "病媒吸血吸走微絲蚴", "1–2 週變成 L3",
    tip="黑蠅體內的 L3 要到<b>唾腺</b>成熟才有感染力。<i>Onchocerca</i> 在人體長成成蟲可能要 18 個月。")
d.e("bite", "adult")
d.e("adult", "mf")
d.e("mf", "vec")
d.top_loop("vec", "bite", "再去叮下一個人")
for r, (v, vt, a, at, m, mt, c, ct, tips) in enumerate([
    ("蚊", "家蚊、斑蚊、曼蚊、瘧蚊", "淋巴管、淋巴結", "台灣曾流行（金門）", "血液 · 夜間", "10 pm–4 am 採血", "象皮病、乳糜尿", "DEC 殺成蟲＋微絲蚴",
     ("班氏：家蚊 <i>Culex</i> 為主；馬來：曼蚊 <i>Mansonia</i>。",
      "成蟲死亡、鈣化 → 淋巴管阻塞 → 淋巴曲張。",
      "班氏：有鞘、尾端無核；馬來：有鞘、尾端兩顆核。厚血片 Giemsa、Knott 濃縮法。",
      "急性：淋巴管炎、絲蟲熱；慢性：<b>象皮病</b>、<b>乳糜尿</b>（班氏）。熱帶肺嗜酸性球症候群：血中沒有微絲蚴、IgE 很高。")),
    ("斑虻 Chrysops", "白天叮咬 · mango fly", "皮下組織，會移行", "爬過結膜＝眼蟲", "血液 · 白天", "有鞘、尾核到底", "Calabar swelling", "DEC 可能致命腦炎",
     ("<i>C. silicea</i>、<i>C. dimidiata</i>；只在西非、中非的森林沼澤。",
      "成蟲在皮下到處爬，爬過<b>結膜</b>時肉眼可見。",
      "<b>日間週期性</b>：白天採血。",
      "<b>Calabar swelling</b>（四肢暫時性腫脹）；重度微絲蚴血症時用 DEC 可能引起<b>致命腦炎</b>。")),
    ("黑蠅 Simulium", "白天叮咬 · 河邊繁殖", "皮下結節", "onchocercoma", "皮膚、眼睛", "無鞘 · skin snip", "河盲症、皮膚炎", "Ivermectin 只殺微絲蚴",
     ("黑蠅在湍急的河流繁殖 → 病患集中在<b>大河附近</b>。",
      "結節位置：非洲在下軀幹、下肢；中美洲在頭頸。",
      "<b>不在血液</b>：皮膚切片（skin snip）；Mazzotti test（50 mg DEC）可能有嚴重反應。",
      "失明主要是微絲蚴與共生菌 <i>Wolbachia</i> 引起的發炎。")),
], start=1):
    d.n(f"v{r}", 0, r, v, vt, tip=tips[0])
    d.n(f"a{r}", 1, r, a, at, cls="bv", tip=tips[1])
    d.n(f"m{r}", 2, r, m, mt, tip=tips[2])
    d.n(f"c{r}", 3, r, c, ct, cls="br", tip=tips[3])
    for x, y in ((f"v{r}", f"a{r}"), (f"a{r}", f"m{r}"), (f"m{r}", f"c{r}")):
        d.e(x, y, cls="lt")
DS.append(d)

# ======================================================== 吸蟲
d = D("intestinal-flukes", 4, 7, cw=160, label="腸吸蟲生活史比較：共同流程是卵隨糞便、纖毛幼蟲進入第一中間宿主螺、尾動幼蟲在第二中間宿主形成囊狀幼蟲、人吃入。薑片蟲：扁捲螺、水生植物、小腸。橫川異形吸蟲：淡水螺、淡水魚如香魚、小腸。異形異形吸蟲：海蜷燒酒螺等半鹹水螺、半鹹水魚如烏魚、小腸。棘口吸蟲：淡水螺、螺蛙魚與水生植物、小腸。人雙口吸蟲：淡水螺、水生植物、大腸。胰臟吸蟲：陸螺、蝗蟲、胰管。")
d.zone(0, 3, 0, 0, "共同流程")
d.n("g0", 0, 0, "卵隨糞便入水", "有卵蓋")
d.n("g1", 1, 0, "1st IH：螺", "胞狀 → 雷氏 → 尾動幼蟲")
d.n("g2", 2, 0, "2nd IH：囊狀幼蟲", "感染期", cls="bw")
d.n("g3", 3, 0, "人吃入 → 腸道成蟲", "", cls="bv")
d.e("g0", "g1")
d.e("g1", "g2")
d.e("g2", "g3")
d.zone(0, 3, 1, 6, "各蟲比較：第一中間宿主 → 吃什麼得病 → 寄生部位 → 重點")
for r, (name, ih1, ih2, site, key, tips) in enumerate([
    ("薑片蟲 F. buski", "扁捲螺", "水生植物", "小腸", "最大的吸蟲、最大的卵",
     ("<i>Fasciolopsis buski</i>；1st IH <b>扁捲螺</b>（<i>Segmentina</i>、<i>Hippeutis</i>）。",
      "<b>菱角、荸薺、筊白筍</b>：用牙齒剝皮時吃進表面的囊狀幼蟲；保蟲宿主<b>豬</b>（吃水生植物餵豬）。",
      "成蟲 3–7 cm，腹吸盤大；大量感染 → 腹痛、腸阻塞、<b>臉部水腫</b>。卵 130–140 µm，和牛羊肝吸蟲卵分不出來。")),
    ("橫川異形吸蟲", "川蜷等淡水螺", "淡水魚（香魚）", "小腸", "台灣首例；腹吸盤偏右",
     ("<i>Metagonimus yokogawai</i>；1st IH <b>淡水螺</b>（川蜷 <i>Semisulcospira</i>）。卵被螺吃進去才孵化。",
      "2nd IH <b>淡水魚</b>，主要是<b>香魚</b>，囊狀幼蟲在魚鱗下或肌肉裡。百十四共筆舉例寫烏魚，但烏魚是異形異形吸蟲的宿主；同學表寫的「蛙」查無文獻。",
      "1912 年橫川定在台灣發現；<b>腹吸盤偏中線右側</b>、<b>無生殖吸盤</b>、睪丸 45° 斜排。卵 28–32 µm、纖毛幼蟲不明顯。")),
    ("異形異形吸蟲", "海蜷、燒酒螺", "半鹹水魚（烏魚）", "小腸（空腸）", "最小；3 個吸盤；卵異位",
     ("<i>Heterophyes heterophyes</i>；1st IH <b>海蜷、燒酒螺、栓海螺</b>，都是河口、潮間帶的半鹹水螺（不是淡水螺）。",
      "2nd IH <b>烏魚</b>等河口半鹹水魚（也有吳郭魚、蝦虎）；小林晴次郎在埃及港口買魚解剖發現囊狀幼蟲。",
      "<b>人體最小的吸蟲</b>；<b>多一個生殖吸盤</b>、睪丸左右並列、體表魚鱗狀棘。主要在空腸，也見於十二指腸、迴腸、盲腸；卵經腸壁血管異位到<b>腦、脊髓、心肌</b>。")),
    ("棘口吸蟲", "淡水螺", "螺、蛙、魚、水生植物", "小腸", "2nd IH 不挑；頭冠有棘",
     ("<i>Echinostoma ilocanum</i>；螺內有<b>兩代雷氏幼蟲</b>。",
      "第二中間宿主要求不嚴格：尾蚴可以在雷氏幼蟲裡、原來的螺、其他螺、蛙、魚，甚至植物上結囊。",
      "頭端<b>馬蹄形頭冠＋兩列頭棘</b>；卵像薑片蟲卵，排出時常未成熟。")),
    ("人雙口吸蟲", "淡水螺", "水生植物", "大腸（盲腸）", "角錐形；保蟲宿主豬、鹿",
     ("<i>Gastrodiscoides hominis</i>；印度阿薩姆最早發現。",
      "生活史和薑片蟲相似：吃水生植物上的囊狀幼蟲。",
      "唯一寄生在<b>大腸</b>的；角錐形、後端大腹吸盤。治療 praziquantel。")),
    ("胰臟吸蟲", "陸螺", "蝗蟲", "胰管", "陸生吸蟲；卵殼厚色深",
     ("<i>Eurytrema pancreaticum</i>；1st IH 陸生蝸牛（<i>Bradybaena</i>）。",
      "2nd IH <b>蝗蟲</b>；牛羊吃草時吃到，人很少感染。",
      "成蟲在<b>胰管</b>；陸生吸蟲的卵殼厚、顏色深（抗乾燥）。")),
], start=1):
    d.n(f"n{r}", 0, r, name, "", cls="bp")
    d.n(f"i{r}", 1, r, ih1, "", tip=tips[0])
    d.n(f"j{r}", 2, r, ih2, "感染來源", cls="bw", tip=tips[1])
    d.n(f"s{r}", 3, r, site, key, cls="bv", tip=tips[2])
    for x, y in ((f"n{r}", f"i{r}"), (f"i{r}", f"j{r}"), (f"j{r}", f"s{r}")):
        d.e(x, y, cls="lt")
d.note("治療", "Praziquantel；診斷都是糞便找卵（棘口類的卵彼此很像）")
DS.append(d)

d = D("paragonimus-cycle", 5, 2, cw=140, label="衛氏肺吸蟲生活史：吃生的或醉的淡水蟹、蝦，囊狀幼蟲在小腸脫囊，穿過腸壁、腹腔、橫膈進入肺，成對住在肺部囊腔。卵隨痰咳出或吞下隨糞便排出，在水中孵出纖毛幼蟲，進入第一中間宿主川蜷，尾動幼蟲再進入淡水蟹蝦形成囊狀幼蟲。")
d.zone(0, 4, 0, 0, "人（貓、狗、豬也是保蟲宿主）")
d.zone(0, 3, 1, 1, "淡水環境")
d.n("crab", 0, 0, "生吃淡水蟹、蝦", "醉蟹、醉蝦", cls="bw",
    tip="2nd IH：<b>淡水蟹（澤蟹）</b>、蝦；囊狀幼蟲在鰓、肌肉、內臟。處理生蟹時汙染砧板、手也會感染。")
d.n("duo", 1, 0, "小腸脫囊", "")
d.n("mig", 2, 0, "穿腸壁、腹腔、橫膈", "不是經血流",
    tip="幼蟲<b>穿過腸壁</b>到腹腔，再<b>穿過橫膈</b>進入胸腔與肺（和蛔蟲經血流到肺不同）。")
d.n("lung", 3, 0, "肺囊腔：成對成蟲", "咳血痰，像結核", cls="bv",
    tip="咖啡豆形、兩個手掌狀睪丸<b>左右並列</b>在後 1/3。症狀：咳嗽、<b>鐵鏽色血痰</b>、胸痛；X 光常誤診為 <b>TB</b>。痰中有卵與 Charcot-Leyden 結晶。")
d.n("ecto", 4, 0, "異位：腦最嚴重", "癲癇；30 歲以下", cls="br",
    tip="蟲體移行到腦 → 佔位性病灶、癲癇。也可到皮下、腹腔。")
d.n("egg", 3, 1, "卵隨痰或糞便排出", "卵蓋有肩、後端增厚",
    tip="約 85 × 53 µm、金黃褐色、卵蓋扁平有肩、<b>後端殼增厚</b>。痰吞下去就出現在糞便或胃液。")
d.n("mira", 2, 1, "水中孵出纖毛幼蟲", "約 3 週")
d.n("snail", 1, 1, "1st IH：川蜷", "胞狀 → 雷氏 → 尾動",
    tip="<i>Semisulcospira libertina</i>。")
d.n("cerc", 0, 1, "尾動幼蟲進入蟹、蝦", "形成囊狀幼蟲")
d.e("crab", "duo")
d.e("duo", "mig")
d.e("mig", "lung")
d.e("lung", "ecto", cls="lr dash")
d.e("lung", "egg")
d.e("egg", "mira")
d.e("mira", "snail")
d.e("snail", "cerc")
d.e("cerc", "crab")
d.note("診斷", "痰、糞便、胃液找卵；ELISA；首二例在台灣發現")
d.note("治療", "Praziquantel（Bithionol 較差）")
DS.append(d)

d = D("clonorchis-cycle", 4, 2, label="中華肝吸蟲生活史：吃生的鯉科淡水魚，囊狀幼蟲在十二指腸脫囊，沿總膽管往上到肝內膽管長成成蟲。卵隨糞便排出，要被滿州泥螺吃進去才孵化，尾動幼蟲離開螺後鑽進淡水魚的魚鱗下或肌肉形成囊狀幼蟲。")
d.zone(0, 3, 0, 0, "人（貓、狗是保蟲宿主）")
d.zone(0, 2, 1, 1, "淡水環境")
d.n("fish", 0, 0, "生吃鯉科淡水魚", "魚肉內囊狀幼蟲", cls="bw",
    tip="2nd IH <b>鯉科淡水魚</b>（約 100 種）；生魚片、魚生粥。醃、燻、乾燥、冷凍不一定能殺死。")
d.n("duo", 1, 0, "十二指腸脫囊", "沿總膽管上行")
d.n("bile", 2, 0, "肝內膽管成蟲", "可活 15 年以上", cls="bv",
    tip="寄生在<b>膽管</b>（不是肝實質）；一天產 2400–4000 顆卵。三種後睪科肝吸蟲靠<b>睪丸</b>分：中華＝珊瑚狀。")
d.n("clin", 3, 0, "膽管炎、膽管癌", "兒童：侏儒症", cls="br",
    tip="膽管增生、阻塞、膽結石；長期感染 → <b>膽管癌</b>。兒童時期感染 → 營養不良、<b>侏儒症</b>。")
d.n("egg", 2, 1, "卵隨糞便排出", "小、卵蓋有肩、後端小突起",
    tip="約 30 × 16 µm，吸蟲卵最小之一；內有成熟纖毛幼蟲。和異形、橫川吸蟲卵很像 → 問飲食與旅遊史。")
d.n("snail", 1, 1, "1st IH：滿州泥螺", "螺吃卵後才孵化",
    tip="卵<b>不在水中孵化</b>，要被<b>滿州泥螺</b>（<i>Parafossarulus manchouricus</i>）吃進去才孵出纖毛幼蟲。")
d.n("cerc", 0, 1, "尾動幼蟲鑽入魚", "魚鱗下、肌肉")
d.n("rel", 3, 1, "同科：貓肝、泰國肝", "生活史相同", cls="bp",
    tip="<i>Opisthorchis felineus</i>（貓）、<i>O. viverrini</i>（泰國）：睪丸是花狀（大而淺裂／小而深裂）。泰國肝吸蟲也是膽管癌的致癌物。")
d.e("fish", "duo")
d.e("duo", "bile")
d.e("bile", "clin", cls="lr dash")
d.e("bile", "egg")
d.e("egg", "snail")
d.e("snail", "cerc")
d.e("cerc", "fish")
d.note("診斷", "糞便或十二指腸液找卵")
d.note("治療", "Praziquantel")
DS.append(d)

d = D("fasciola-cycle", 5, 2, cw=140, label="牛羊肝吸蟲生活史：吃到水生植物上（或水中）的囊狀幼蟲，在十二指腸脫囊後穿過腸壁、經腹腔、穿過肝被膜，在肝實質移行後進入膽管長成成蟲。卵隨糞便排出，在水中孵出纖毛幼蟲，進入椎實螺，尾動幼蟲游出後附著在水生植物上結囊。")
d.zone(0, 3, 0, 0, "人（牛、羊是保蟲宿主）")
d.zone(0, 3, 1, 1, "淡水環境")
d.n("plant", 0, 0, "吃水生植物上的囊蚴", "水芹 · 喝生水也會", cls="bw",
    tip="第二中間宿主<b>不是必要的</b>：囊狀幼蟲附在<b>水芹</b>等水生植物上，或漂浮在水中。")
d.n("duo", 1, 0, "十二指腸脫囊", "")
d.n("mig", 2, 0, "穿腸壁 → 腹腔 → 肝", "急性期：損傷性肝炎", cls="br",
    tip="幼蟲穿過腸壁到腹腔，再<b>穿過肝被膜</b>在<b>肝實質</b>移行（潛伏 2–4 個月）→ 發燒、右上腹痛、<b>traumatic hepatitis</b>、腹內出血。")
d.n("bile", 3, 0, "膽管成蟲", "慢性期：膽管阻塞", cls="bv",
    tip="葉片狀、有<b>頭錐</b>、腸支與睪丸都是樹枝狀。慢性期：膽管增生、纖維化、鈣化、阻塞。")
d.n("halz", 4, 0, "Halzoun", "生吃羊肝 → 咽喉黏蟲", cls="br",
    tip="吃生的動物肝臟，成蟲黏在<b>咽喉</b> → 咽部水腫、呼吸困難（中東）。也有肝外異位：皮下結節、肺膿瘍。")
d.n("egg", 3, 1, "卵隨糞便排出", "大、卵蓋不明顯",
    tip="130–150 × 63–90 µm、淡黃、殼薄；和<b>薑片蟲卵幾乎無法區分</b>。")
d.n("mira", 2, 1, "水中孵出纖毛幼蟲", "")
d.n("snail", 1, 1, "1st IH：椎實螺", "胞狀 → 雷氏 → 尾動",
    tip="<i>Lymnaea</i>（椎實螺）。")
d.n("cerc", 0, 1, "尾動幼蟲附著植物結囊", "")
d.n("tx", 4, 1, "Triclabendazole", "治療 · PZQ 效果差", cls="bp",
    tip="考古配合題：<b>praziquantel 無效</b>的吸蟲 → 牛羊肝吸蟲。也可用 Bithionol。")
d.e("plant", "duo")
d.e("duo", "mig")
d.e("mig", "bile")
d.e("bile", "egg")
d.e("egg", "mira")
d.e("mira", "snail")
d.e("snail", "cerc")
d.e("cerc", "plant")
d.note("診斷", "糞便或膽汁找卵（要排除吃動物肝的假感染）；影像、血清學")
DS.append(d)

d = D("terrestrial-flukes", 5, 3, cw=140, label="陸生吸蟲生活史：槍狀肝吸蟲的卵被陸螺吃進去，尾動幼蟲包在黏液球裡排出，被螞蟻吃下形成囊狀幼蟲，牛羊吃草時吃到螞蟻；人吃到螞蟻才是真感染，吃到病肝而在糞便見卵是假感染。胰臟吸蟲的第二中間宿主是蝗蟲，成蟲寄生在牛羊的胰管。")
d.zone(0, 4, 0, 1, "槍狀肝吸蟲 Dicrocoelium dendriticum")
d.zone(0, 4, 2, 2, "胰臟吸蟲 Eurytrema pancreaticum")
d.n("de", 0, 0, "卵隨糞便排出", "殼厚、含纖毛幼蟲",
    tip="38–45 × 22–30 µm、深黃褐色、<b>不對稱</b>、卵蓋傾斜、殼厚、內含纖毛幼蟲（陸生吸蟲的卵要抗乾燥）。")
d.n("ds", 1, 0, "1st IH：陸螺吃卵", "沒有雷氏幼蟲")
d.n("dm", 2, 0, "尾蚴包在黏液球排出", "黏在草上")
d.n("da", 3, 0, "2nd IH：螞蟻", "囊狀幼蟲 · 感染期", cls="bw",
    tip="被感染的螞蟻晚上會爬到草尖、咬住不放，等著被吃草的牛羊吃掉。")
d.n("db", 4, 0, "牛羊吃到螞蟻", "成蟲在膽管", cls="bv",
    tip="成蟲細長如<b>槍頭</b>、睪丸在卵巢前；寄生在膽管。")
d.n("dh", 4, 1, "人：吃到螞蟻＝真感染", "很少見")
d.n("dp", 3, 1, "吃到病肝 → 糞便見卵", "假感染", cls="br",
    tip="吃到被感染動物的肝，卵直接通過腸道 → <b>spurious infection</b>；要停吃肝臟幾天後重驗，或用膽汁找卵。")
d.e("de", "ds")
d.e("ds", "dm")
d.e("dm", "da")
d.e("da", "db")
d.e("db", "dh", cls="ln dash")
d.n("ee", 0, 2, "卵隨糞便排出", "殼厚、顏色深")
d.n("es", 1, 2, "1st IH：陸螺", "蝸牛 Bradybaena")
d.n("em", 2, 2, "尾蚴附著在草上", "")
d.n("eg", 3, 2, "2nd IH：蝗蟲", "感染期", cls="bw")
d.n("eb", 4, 2, "牛羊吃到蝗蟲", "成蟲在胰管", cls="bv",
    tip="睪丸在卵巢前、子宮佔滿後半；人很少感染。")
for x, y in (("ee", "es"), ("es", "em"), ("em", "eg"), ("eg", "eb")):
    d.e(x, y)
d.note("記法", "陸生吸蟲 = 陸螺 ＋ 昆蟲：槍狀肝吸蟲吃螞蟻、胰臟吸蟲吃蝗蟲")
d.note("治療", "Praziquantel")
DS.append(d)

d = D("schisto-cycle", 4, 3, cw=170, label="血吸蟲生活史：尾動幼蟲在水中直接鑽入皮膚，變成童蟲經血流、肺到肝門脈發育，雌雄成蟲合抱移到各自的靜脈叢產卵，卵穿過腸壁或膀胱壁隨糞便或尿液排出，卡在組織的卵造成肉芽腫。卵在水中孵出纖毛幼蟲進入螺，經兩代胞狀幼蟲產生尾動幼蟲。只有一個中間宿主，沒有雷氏幼蟲和囊狀幼蟲。")
d.zone(0, 3, 0, 0, "人")
d.zone(0, 2, 1, 1, "淡水環境（只有一個中間宿主）")
d.n("cerc", 0, 0, "尾動幼蟲鑽皮膚", "尾分叉 · 感染期", cls="bw",
    tip="下水、游泳、赤腳時，尾動幼蟲<b>直接鑽皮膚</b>（不是吃進去）→ 尾動幼蟲皮膚炎。水鳥血吸蟲 → <b>swimmer's itch</b>。")
d.n("schisto", 1, 0, "童蟲 → 血流 → 肝門脈", "片山熱（急性期）",
    tip="尾巴脫落變成<b>童蟲（schistosomulum）</b>，經血流、肺到肝門脈發育。感染 1–3 個月後<b>片山熱（Katayama fever）</b>：免疫複合體引起的發燒、過敏。")
d.n("pair", 2, 0, "雌雄合抱 → 靜脈叢產卵", "雌蟲躺在抱雌溝", cls="bv",
    tip="唯一<b>雌雄異體</b>的吸蟲。日本：<b>上</b>腸繫膜靜脈；曼森：<b>下</b>腸繫膜靜脈；埃及：<b>膀胱</b>靜脈叢。")
d.n("gran", 3, 0, "卵卡組織 → 肉芽腫", "主要致病原因", cls="br",
    tip="卵（不是成蟲）是致病主因：肝 → 門脈周圍纖維化、<b>門脈高壓</b>、肝脾腫大；埃及 → <b>血尿</b>、膀胱癌。日本血吸蟲卵可到腦。")
d.n("egg", 2, 1, "卵隨糞便或尿液", "沒有卵蓋",
    tip="三種都<b>沒有卵蓋</b>，看刺的位置分種。")
d.n("mira", 1, 1, "水中孵出纖毛幼蟲", "毛蚴孵化法")
d.n("snail", 0, 1, "螺：兩代胞狀幼蟲", "無雷氏、無囊狀幼蟲",
    tip="<b>例外</b>：只需要一個中間宿主；螺內是母胞蚴 → 子胞蚴 → 尾蚴，<b>沒有雷氏幼蟲</b>；尾蚴不結囊、直接鑽皮膚。")
d.e("cerc", "schisto")
d.e("schisto", "pair")
d.e("pair", "gran", cls="lr dash")
d.e("pair", "egg")
d.e("egg", "mira")
d.e("mira", "snail")
d.e("snail", "cerc")
d.n("sj", 0, 2, "日本 S. japonicum", "湖北釘螺 · 側小刺 · 糞便", cls="bp",
    tip="中間宿主<b>湖北釘螺 <i>Oncomelania</i></b>；卵圓、側邊小刺常看不到；產卵量最多。")
d.n("sm", 1, 2, "曼森 S. mansoni", "雙臍扁螺 · 大側刺 · 糞便", cls="bp",
    tip="中間宿主 <b><i>Biomphalaria</i></b>；卵後端旁有<b>大側刺</b>。Oxamniquine 只對曼森有效。")
d.n("sh", 2, 2, "埃及 S. haematobium", "小泡螺 · 尾端刺 · 尿液", cls="bp",
    tip="中間宿主 <b><i>Bulinus</i></b>；卵有<b>尾端刺</b>，在<b>尿液</b>找；中午前後採尿。")
d.n("tx", 3, 2, "治療：Praziquantel", "Artemether 殺童蟲", cls="bp")
DS.append(d)

# ======================================================== 跨章：移行路徑、感染來源
d = D("migration-routes", 5, 7, cw=150, label="寄生蟲在人體的四種移行路徑：門脈循環（腸道經門靜脈到肝），包括蛔蟲會再往肺走、肝毛線蟲與犬蛔蟲停在肝；鑽皮膚走靜脈到右心與肺，包括鉤蟲、糞小桿線蟲與血吸蟲童蟲，血吸蟲最後定居在門脈；穿過腸壁進腹腔不走血，肺吸蟲穿橫膈到肺、牛羊肝吸蟲穿肝被膜到膽管；膽管上行不穿腸壁，中華肝吸蟲從十二指腸經總膽管到肝內膽管。")
d.zone(0, 4, 0, 1, "① 門脈循環：腸 → 門靜脈 → 肝")
d.zone(0, 4, 2, 3, "② 鑽皮膚 → 靜脈 → 右心 → 肺")
d.zone(0, 4, 4, 5, "③ 穿腸壁 → 腹腔（不走血）")
d.zone(0, 4, 6, 6, "④ 膽管上行（不穿腸壁）")
for r, (who, wt, a, at, b, bt, c, ct, z, zt, z_cls, tips) in enumerate([
    ("蛔蟲", "Ascaris", "吃胚胎化蟲卵", "感染期", "小腸孵化", "幼蟲穿腸壁", "門脈 → 肝 → 右心", "血流移行", "肺 → 氣管 → 吞下", "Loeffler · 回小腸", "br",
     ("門脈到肝之後<b>沒有停</b>，繼續到右心、肺，再經氣管吞回小腸長成成蟲。",
      "穿過肺泡時造成 <b>Ascaris pneumonia／Loeffler syndrome</b>（咳嗽、血痰、嗜酸性球↑）。")),
    ("肝毛線蟲・犬蛔蟲", "Capillaria/Toxocara", "吃胚胎化蟲卵", "感染期", "小腸孵化", "幼蟲穿腸壁", "門脈 → 肝", "停在肝", "肝內病灶", "肝毛：成蟲＋卵在肝", "br",
     ("<i>C. hepatica</i>：在肝內長成成蟲、卵留在肝實質（人的糞便找不到卵，要肝切片）。<i>T. canis</i>：人是保幼宿主，幼蟲<b>多數停在肝</b>，部分到肺、眼、CNS。",
      "肝毛線蟲：肝炎、肝腫大；犬蛔蟲：<b>VLM</b>（內臟）、<b>OLM</b>（眼）。")),
    ("鉤蟲・糞小桿線蟲", "Necator/Strongyloides", "絲狀幼蟲鑽皮膚", "赤腳踩土", "靜脈 → 右心", "", "肺", "Loeffler", "氣管 → 吞下", "小腸成蟲", "bv",
     ("感染期是<b>絲狀幼蟲（filariform larva，L3）</b>，從腳底等皮膚鑽入。",
      "和蛔蟲一樣經過肺，但起點是<b>皮膚</b>不是腸道。糞小桿線蟲還能在體內自體感染。")),
    ("血吸蟲", "Schistosoma", "尾動幼蟲鑽皮膚", "碰疫水", "靜脈 → 右心", "童蟲", "肺 → 體循環", "童蟲移行", "定居門脈系統", "卵 → 肝 · 門脈高壓", "br",
     ("<b>進入走體循環、成蟲住門脈</b>：童蟲先走靜脈、心、肺，最後才在門脈系統定居。",
      "日本＝上腸繫膜靜脈、曼森＝下腸繫膜靜脈 → 卵順門脈到肝，肉芽腫 → 肝脾腫大、<b>門脈高壓</b>。埃及住<b>膀胱靜脈叢</b>，不在門脈 → 血尿。")),
    ("衛氏肺吸蟲", "Paragonimus", "吃螃蟹囊狀幼蟲", "醉蟹、生蟹", "小腸脫囊", "穿腸壁", "腹腔", "不走血", "穿橫膈 → 肺", "咳血 · 痰找卵", "bv",
     ("在十二指腸脫囊後<b>穿過腸壁</b>進腹腔，<b>不走血流</b>。",
      "腹腔 → 穿過<b>橫膈</b> → 胸腔 → 肺，形成蟲囊；異位可到腦。")),
    ("牛羊肝吸蟲", "Fasciola hepatica", "吃水生植物囊蚴", "水芹等", "小腸脫囊", "穿腸壁", "腹腔", "不走血", "穿肝被膜 → 膽管", "肝實質移行", "bv",
     ("同樣<b>穿腸壁進腹腔</b>，但目標是肝。",
      "穿過<b>肝被膜</b>、在肝實質移行（traumatic hepatitis）後進入膽管定居。")),
    ("中華肝吸蟲", "Clonorchis", "吃生淡水魚囊蚴", "魚肉裡", "十二指腸脫囊", "不穿腸壁", "總膽管上行", "Vater 壺腹", "肝內膽管", "膽管炎 · 膽管癌", "bv",
     ("<b>不穿腸壁、不走血</b>：脫囊後直接從 Vater 壺腹進總膽管。",
      "往上爬到肝內膽管定居；長期感染與<b>膽管癌（CCA）</b>有關。")),
]):
    d.n(f"w{r}", 0, r, who, wt, cls="bp")
    d.n(f"a{r}", 1, r, a, at, cls="bw")
    d.n(f"b{r}", 2, r, b, bt)
    d.n(f"c{r}", 3, r, c, ct, tip=tips[0])
    d.n(f"z{r}", 4, r, z, zt, cls=z_cls, tip=tips[1])
    for x, y in ((f"a{r}", f"b{r}"), (f"b{r}", f"c{r}"), (f"c{r}", f"z{r}")):
        d.e(x, y, cls="lr" if r in (4, 5) and y == f"c{r}" else "ln")  # 紅箭頭＝穿腸壁進腹腔
d.note("同樣到肝", "蛔蟲・肝毛線蟲・犬蛔蟲走門脈；牛羊肝吸蟲穿腹腔進肝被膜；中華肝吸蟲走膽管")
d.note("會經過肺", "蛔蟲、鉤蟲、糞小桿線蟲（Loeffler）＋血吸蟲童蟲；鞭蟲、蟯蟲不經過肺")
DS.append(d)

d = D("food-sources", 6, 10, cw=128, legend=(("bw", "暴露來源"), ("bx", "線蟲"), ("bg", "吸蟲")), label="吃什麼會得什麼：依暴露來源整理線蟲與吸蟲。吃到蟲卵：蛔蟲、鞭蟲、蟯蟲、犬蛔蟲、肝毛線蟲。生豬肉：旋毛蟲。生淡水魚：中華肝吸蟲、橫川異形吸蟲、菲律賓毛線蟲、顎口線蟲。生海魚與魷魚：海獸胃線蟲、異形異形吸蟲（烏魚，半鹹水魚）。生螃蟹與淡水蝦：肺吸蟲、廣東住血線蟲。生水生植物：薑片蟲、牛羊肝吸蟲。生蝸牛蛞蝓：廣東住血線蟲。赤腳踩土：鉤蟲、糞小桿線蟲。接觸疫水：血吸蟲。昆蟲叮咬：淋巴絲蟲、羅阿絲蟲、蟠尾絲蟲。")
NEM, TRE = "bx", "bg"
for r, (src, st, items) in enumerate([
    ("吃到蟲卵", "糞口：手、生菜、土", [
        ("蛔蟲", "小腸 · 經肺", NEM, "土壤中<b>胚胎化</b>的卵才有感染力。"),
        ("鞭蟲", "盲腸 · 不經肺", NEM, "胚胎化卵；孵化後直接到大腸。"),
        ("蟯蟲", "盲腸 · 肛門癢", NEM, "卵產出<b>數小時</b>就有感染力 → 手到口自體再感染、家庭群聚。"),
        ("犬蛔蟲", "VLM · OLM", NEM, "吃到<b>狗糞</b>汙染的土裡的胚胎化卵；也可吃生雞肝等保幼宿主。人是保幼宿主。"),
        ("肝毛線蟲", "肝 · 人是偶然宿主", NEM, "吃到土中<b>胚胎化卵</b>（鼠死後屍體分解釋出）。")]),
    ("生豬肉", "或野生動物肉", [
        ("旋毛蟲", "小腸 → 骨骼肌", NEM, "肉裡的<b>包囊幼蟲</b>；同一宿主既是最終宿主也是中間宿主。")]),
    ("生淡水魚", "生魚片、醃魚", [
        ("中華肝吸蟲", "膽管 · 膽管癌", TRE, "囊狀幼蟲在<b>淡水魚</b>（鯉科）肉裡。"),
        ("橫川異形吸蟲", "小腸 · 腹吸盤偏右", TRE, "囊狀幼蟲在<b>淡水魚</b>（主要是香魚）鱗下或肌肉；1st IH 川蜷。"),
        ("菲律賓毛線蟲", "小腸 · 自體感染", NEM, "生吃<b>小型淡水魚</b>；吸收不良、蛋白質流失。"),
        ("顎口線蟲", "皮下遊走腫塊", NEM, "淡水魚、<b>泥鰍</b>、雞、蛙等體內的 L3；人是非適合宿主。")]),
    ("生海魚、魷魚", "生魚片、壽司", [
        ("海獸胃線蟲", "胃壁 · 劇烈胃痛", NEM, "魚、魷魚肉裡的 <b>L3</b>；冷凍或煮熟可殺死。"),
        ("異形異形吸蟲", "小腸 · 卵可異位", TRE, "囊狀幼蟲在<b>烏魚</b>等河口半鹹水魚；1st IH 海蜷、燒酒螺等半鹹水螺。橫川是淡水螺→香魚，異形是半鹹水螺→<b>烏魚</b>。")]),
    ("生螃蟹、淡水蝦", "醉蟹、生蝦", [
        ("衛氏肺吸蟲", "肺 · 咳血", TRE, "<b>澤蟹</b>等淡水蟹的囊狀幼蟲。"),
        ("廣東住血線蟲", "蝦蟹是保幼宿主", NEM, "陷阱：吃淡水蝦不只肺吸蟲，<b>廣東住血線蟲</b>也會（蝦、蟹、蛙是保幼宿主）。")]),
    ("生水生植物", "菱角、荸薺、水芹", [
        ("薑片蟲", "小腸 · 最大吸蟲", TRE, "用牙齒剝<b>菱角、荸薺</b>皮時吃進表面的囊狀幼蟲。"),
        ("牛羊肝吸蟲", "肝 → 膽管", TRE, "<b>水芹</b>等水生植物；PZQ 效果差 → Triclabendazole。")]),
    ("生蝸牛、蛞蝓", "或沾黏液的生菜", [
        ("廣東住血線蟲", "嗜酸性腦膜炎", NEM, "中間宿主是<b>軟體動物</b>（非洲大蝸牛、蛞蝓）；生菜沾到螺黏液也會感染。")]),
    ("赤腳踩土", "絲狀幼蟲鑽皮膚", [
        ("鉤蟲", "小腸 · 缺鐵性貧血", NEM, "絲狀幼蟲鑽皮膚 → 經肺；<i>A. duodenale</i> 也可經口。"),
        ("糞小桿線蟲", "自體感染 · 超感染", NEM, "絲狀幼蟲鑽皮膚；免疫低下（類固醇、HTLV-1）→ 超感染。")]),
    ("碰到疫水", "游泳、下田", [
        ("血吸蟲", "門脈 · 膀胱靜脈", TRE, "<b>尾動幼蟲</b>直接鑽皮膚（不用吃）；游泳者癢。")]),
    ("昆蟲叮咬", "L3 從傷口進入", [
        ("淋巴絲蟲", "蚊 · 象皮病", NEM, "班氏、馬來絲蟲；夜間週期性。"),
        ("羅阿絲蟲", "斑虻 · 眼蟲", NEM, "<i>Chrysops</i>；日間週期性、Calabar swelling。"),
        ("蟠尾絲蟲", "黑蠅 · 河盲症", NEM, "<i>Simulium</i>；微絲蚴在皮膚、眼睛 → skin snip。")]),
]):
    d.n(f"s{r}", 0, r, src, st, cls="bw")
    for i, (name, sub, cls, tip) in enumerate(items, start=1):
        d.n(f"p{r}_{i}", i, r, name, sub, cls=cls, tip=tip)
    d.e(f"s{r}", f"p{r}_1")
d.note("讀法", "每一列：左邊黃框是暴露來源，右邊是會得的寄生蟲（同一列由左往右讀）")
d.note("陷阱", "蝦蟹 → 肺吸蟲＋廣東住血線蟲；橫川吃淡水魚（香魚）、異形吃烏魚（半鹹水魚）；不用吃的：鉤蟲、糞小桿線蟲、血吸蟲（鑽皮膚）、血絲蟲（叮咬）")
DS.append(d)

d = D("filaria-vectors", 5, 8, cw=150,
      legend=(("bw", "病媒"), ("bv", "成蟲位置"), ("br", "微絲蚴在皮膚")),
      label="八種人體血絲蟲的病媒配對：蚊傳班氏、馬來、帝汶絲蟲，成蟲在淋巴管、微絲蚴在血液；斑虻傳羅阿絲蟲，成蟲在皮下移行、微絲蚴白天在血液；黑蠅傳蟠尾絲蟲，成蟲在皮下結節、微絲蚴在皮膚與眼睛；蠓傳 Mansonella perstans（體腔、血液）、M. streptocerca（真皮、皮膚），M. ozzardi 由蠓與黑蠅傳播（皮下、血液）。")
d.zone(0, 4, 0, 2, "蚊 mosquito → 淋巴絲蟲")
d.zone(0, 4, 3, 3, "斑虻 deerfly、mango fly")
d.zone(0, 4, 4, 4, "黑蠅 blackfly")
d.zone(0, 4, 5, 7, "蠓 midges → Mansonella")
for r, (vec, vt, sp, spt, ad, adt, mf, mft, mf_cls, geo, geot, tips) in enumerate([
    ("蚊", "家蚊、斑蚊、曼蚊、瘧蚊", "班氏絲蟲", "W. bancrofti", "淋巴管、淋巴結", "", "血液 · 夜間", "10 pm–4 am", "bx", "熱帶", "台灣曾流行（金門）",
     ("主要是家蚊 <i>Culex</i>，也有斑蚊、曼蚊、瘧蚊。", "微絲蚴<b>有鞘、尾端無核</b>；象皮病、<b>乳糜尿</b>（班氏特有）。")),
    ("蚊", "曼蚊 · 斑蚊 · 瘧蚊", "馬來絲蟲", "B. malayi", "淋巴管", "", "血液 · 夜間", "", "bx", "亞洲", "",
     ("主要是曼蚊 <i>Mansonia</i>。", "微絲蚴<b>有鞘、尾端兩顆核</b>。")),
    ("蚊", "瘧蚊", "帝汶絲蟲", "B. timori", "淋巴管", "", "血液", "", "bx", "印尼", "",
     ("病媒是瘧蚊 <i>Anopheles</i>。", "也造成淋巴絲蟲症。")),
    ("斑虻", "Chrysops", "羅阿絲蟲", "Loa loa · 眼蟲", "皮下組織", "會主動移行", "血液 · 白天", "唯一日間週期", "bx", "西非、中非", "森林、沼澤",
     ("斑虻白天叮咬（deerfly、mango fly）。", "成蟲爬過<b>結膜</b>肉眼可見；<b>Calabar swelling</b>；微絲蚴有鞘、體核連續到尾尖。")),
    ("黑蠅", "Simulium", "蟠尾絲蟲", "O. volvulus · 河盲症", "皮下結節", "onchocercoma", "皮膚、眼睛", "無鞘 · skin snip", "br", "非洲、拉美", "葉門",
     ("黑蠅在湍急河流繁殖 → 病人集中在大河附近；L3 要到唾腺成熟才有感染力。", "<b>不在血液</b> → 皮膚切片（skin snip）、Mazzotti test；失明與 <i>Wolbachia</i> 引起的發炎有關。")),
    ("蠓", "midges", "M. perstans", "", "體腔", "", "血液", "", "bx", "非洲、南美", "",
     ("蠓（midges）。", "微絲蚴在血液。")),
    ("蠓", "midges", "M. streptocerca", "", "真皮、皮下", "", "皮膚", "", "br", "非洲", "",
     ("蠓（midges）。", "和蟠尾絲蟲一樣，微絲蚴在<b>皮膚</b>。")),
    ("蠓＋黑蠅", "兩種都可以", "M. ozzardi", "", "皮下", "", "血液", "", "bx", "美洲", "",
     ("唯一由<b>蠓與黑蠅</b>兩種病媒傳播。", "微絲蚴在血液。")),
]):
    d.n(f"v{r}", 0, r, vec, vt, cls="bw", tip=tips[0])
    d.n(f"s{r}", 1, r, sp, spt, cls="bp")
    d.n(f"a{r}", 2, r, ad, adt, cls="bv")
    d.n(f"m{r}", 3, r, mf, mft, cls=mf_cls, tip=tips[1])
    d.n(f"g{r}", 4, r, geo, geot)
    for x, y in ((f"v{r}", f"s{r}"), (f"s{r}", f"a{r}"), (f"a{r}", f"m{r}")):
        d.e(x, y, cls="lt")
d.note("口訣", "蚊 → 淋巴；斑虻 → 羅阿（白天）；黑蠅 → 河盲；蠓 → Mansonella（ozzardi 蠓＋黑蠅）")
d.note("皮膚", "微絲蚴在皮膚、不驗血：蟠尾絲蟲、M. streptocerca → skin snip")
DS.append(d)

d = D("parasite-exceptions", 5, 6, cw=150,
      legend=(("bw", "例外類別"), ("bx", "線蟲"), ("bg", "吸蟲")),
      label="線蟲與吸蟲的例外總整理：會自體感染的是糞小桿線蟲、菲律賓毛線蟲、蟯蟲；人是保幼或非適合宿主的是犬蛔蟲、顎口線蟲；人是意外宿主的是廣東住血線蟲與海獸胃線蟲；規則例外是旋毛蟲（同一宿主是最終也是中間宿主）、血吸蟲（雌雄異體、無雷氏與囊狀幼蟲、一個中間宿主）、牛羊肝吸蟲（PZQ 效果差）；不靠驗糞便診斷的是蟯蟲、犬蛔蟲、旋毛蟲、肝毛線蟲、肺吸蟲、埃及血吸蟲、血絲蟲、蟠尾絲蟲。")
N, T = "bx", "bg"
for r, (cat, ct, items) in enumerate([
    ("自體感染", "體內越變越多", [
        ("糞小桿線蟲", "內／外自體 → 超感染", N, "桿狀幼蟲在體內變成絲狀幼蟲，鑽<b>腸黏膜</b>（內）或<b>肛門周圍皮膚</b>（外）；免疫低下 → hyperinfection。"),
        ("菲律賓毛線蟲", "蛋白質流失性腸病", N, "自體感染 → 蟲數越來越多，吸收不良、惡病質。"),
        ("蟯蟲", "手 → 口再感染", N, "卵產出數小時就有感染力，搔癢後經手指再吃進去。")]),
    ("人是保幼宿主", "幼蟲不長大", [
        ("犬蛔蟲", "VLM · OLM", N, "L3 在人體不會長成成蟲 → <b>糞便找不到卵</b>。"),
        ("顎口線蟲", "人是非適合宿主", N, "幼蟲在皮下遊走（遊走性腫脹），可侵入 CNS。")]),
    ("人是意外宿主", "到不了成蟲", [
        ("廣東住血線蟲", "L3 → L5，例外", N, "最終宿主是<b>大鼠</b>；在人體可長到 L5 但不會成蟲 → 嗜酸性腦膜炎。"),
        ("海獸胃線蟲", "L3 鑽胃壁", N, "最終宿主是海洋哺乳類；人吃到魚裡的 L3 → 劇烈胃痛。")]),
    ("規則的例外", "考試最愛", [
        ("旋毛蟲", "同一宿主 FH＋IH", N, "同一隻動物既是最終宿主、也是中間宿主（幼蟲包囊在自己的肌肉）。"),
        ("血吸蟲", "雌雄異體 · 卵無蓋", T, "吸蟲中唯一<b>雌雄異體</b>；只要<b>一個中間宿主</b>；<b>沒有雷氏幼蟲、囊狀幼蟲</b>；尾蚴鑽皮膚。"),
        ("牛羊肝吸蟲", "PZQ 無效", T, "吸蟲共通藥 PZQ 效果差 → <b>Triclabendazole</b>（或 Bithionol）。")]),
    ("不靠驗糞便", "用其他檢體", [
        ("蟯蟲", "肛圍膠帶法", N, "早上、排便清洗前的 Scotch tape test。"),
        ("犬蛔蟲", "血清 TES-ELISA", N, "人是保幼宿主，沒有成蟲產卵。"),
        ("旋毛蟲", "IgG · 肌肉切片", N, "肌肉切片大海撈針；今年老師強調 IgG 抗體。"),
        ("肝毛線蟲", "肝切片", N, "卵留在肝實質；<b>糞便有卵＝spurious</b>（吃了感染動物的肝）。")]),
    ("不靠驗糞便（續）", "", [
        ("衛氏肺吸蟲", "痰（也可糞便）", T, "卵隨痰咳出，吞下則出現在糞便。"),
        ("埃及血吸蟲", "尿液", T, "成蟲住膀胱靜脈叢 → 血尿、卵在<b>尿液</b>。"),
        ("血絲蟲", "血片（看時間）", N, "淋巴絲蟲夜間、羅阿白天採血。"),
        ("蟠尾絲蟲", "skin snip", N, "微絲蚴在皮膚、眼睛，不在血液。")]),
]):
    d.n(f"c{r}", 0, r, cat, ct, cls="bw")
    for i, (name, sub, cls, tip) in enumerate(items, start=1):
        d.n(f"p{r}_{i}", i, r, name, sub, cls=cls, tip=tip)
    d.e(f"c{r}", f"p{r}_1")
d.note("自體感染", "蟯蟲、糞小桿線蟲、菲律賓毛線蟲三種都會（不是只有糞小桿線蟲）")
DS.append(d)

if __name__ == "__main__":
    for d in DS:
        W, H = render(d)
        print(f"{d.id}.svg  {W}×{H:.0f}")
