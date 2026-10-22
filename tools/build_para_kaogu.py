#!/usr/bin/env python3
"""寄蟲考古：百十三「w1~4 Nematodes」與「w5~6 Trematodes」(題＋解) → subjects/parasitology/data/questions-kaogu.json

來源：slides/parasitology/共筆考古/百十三資料/考古期中/（題）與（解）PDF
需要 pymupdf（import fitz）。執行：python3 tools/build_para_kaogu.py（在 repo 根目錄）
- 吸蟲配合題 1–14 手動輸入（見檔案下方 match()，答案依 1151 寄蟲考古 Book1）；線蟲沒有配合題。單選題 → mcq；多選題 → short（選項寫在題幹，參考答案顯示正確選項，避免被當成「任一個對就算對」）
- 題目或選項需要原圖的 → imageOnly（不進練習）
"""
import json, os, re
import fitz

SRC = "slides/parasitology/共筆考古/百十三資料/考古期中"
SETS = [  # (題, 解, id 前綴, 固定章節或 None＝依關鍵字判斷)
    ("w1~4 寄蟲考古 Nematodes (題).pdf", "w1~4 寄蟲考古 Nematodes (解).pdf", "k113-nem", None),
    ("w5~6 寄蟲考古 Trematodes (題).pdf", "w5~6 寄蟲考古 Trematodes (解).pdf", "k113-tre", "trematodes"),
]
OUT = "subjects/parasitology/data/questions-kaogu.json"
SOURCE = "113 考古"


def text(path):
    return " ".join(" ".join(p.get_text().split()) for p in fitz.open(path))


def split_numbered(body, n_max):
    """依序切出 1.、2.、… 的段落（只接受下一個預期的題號，避免把題幹中的數字誤判）。"""
    out, pos, n = {}, 0, 1
    starts = []
    while n <= n_max:
        m = re.compile(rf"(?:^|\s){n}\.\s").search(body, pos)
        if not m:
            break
        starts.append((n, m.start()))
        pos = m.end()
        n += 1
    for i, (num, s) in enumerate(starts):
        e = starts[i + 1][1] if i + 1 < len(starts) else len(body)
        seg = body[s:e].strip()
        out[num] = re.sub(rf"^{num}\.\s*", "", seg)
    return out


def options(seg):
    parts = re.split(r"\(([A-E])\)\s*", seg)
    stem = parts[0].strip()
    opts = [{"k": parts[i], "t": parts[i + 1].strip()} for i in range(1, len(parts) - 1, 2)]
    return stem, opts


CH_RULES = [
    ("filaria", r"Wuchereria|Brugia|Loa|Onchocerc|filari|Filari|微絲|絲蟲|Mansonella|Dirofilaria|Mazzotti|elephant|象皮|河盲|W\. bancrofti|B\. malayi|O\. ?volvulus"),
    ("foodborne", r"Trichinella|旋毛|Anisakis|海獸胃|Angiostrongylus|cantonensis|廣東住血|Gnathostom|顎口|棘顎|Pseudoterranova|T\. spiralis|A\. ?cantonensis|C\.antonensis|G\. spinigerum"),
    ("capillaria-strongyloides", r"Capillaria|毛線蟲|毛細線蟲|Strongyloides|stercoralis|糞小桿|hyperinfection|autoinfection|S\. stercoralis|C\. philippinensis|C\. hepatica"),
    ("enterobius-toxocara", r"Enterobius|蟯蟲|pinworm|Toxocara|犬蛔|貓蛔|VLM|OLM|Scotch|肛圍|E\. vermicularis|T\. canis|T\. cati"),
    ("sth", r"Ascaris|蛔蟲|Trichuris|鞭蟲|hookworm|Hookworm|鉤蟲|Ancylostoma|Necator|STH|土源|A\. lumbricoides|T\. trichiura|N\. americanus|A\. duodenale"),
]


def chapter_of(s, fallback=""):
    for text_ in (s, fallback):
        ch = _chapter(text_)
        if ch:
            return ch
    return "intro"


def _chapter(s):
    hit = {ch: len(re.findall(pat, s)) for ch, pat in CH_RULES}
    if sum(1 for v in hit.values() if v) >= 3:
        return "compare"  # 跨多種蟲的綜合比較題
    best, hits = None, 0
    for ch, pat in CH_RULES:
        h = len(re.findall(pat, s))
        if h > hits:
            best, hits = ch, h
    return best


def needs_image(stem, opts):
    if re.search(r"如下|如圖|下圖|右圖|左圖|圖中", stem):
        return True
    return not opts or any(not o["t"] for o in opts)


def parse_key(block):
    """答案表：每列 10 個題號，接著 10 個答案。"""
    toks = block.split()
    ans, i = {}, 0
    while i < len(toks):
        nums = []
        while i < len(toks) and toks[i].isdigit() and len(nums) < 10:
            nums.append(int(toks[i])); i += 1
        vals = []
        while i < len(toks) and len(vals) < len(nums):
            vals.append(toks[i]); i += 1
        ans.update(zip(nums, vals))
        if not nums:
            i += 1
    return ans


def section(s, start, ends):
    """取出 start 之後、ends 中最早出現者之前的文字。"""
    if start not in s:
        return ""
    s = s.split(start, 1)[1]
    cut = min([s.find(e) for e in ends if e in s] or [len(s)])
    return s[:cut]


def strip_ans(exp):
    return re.sub(r"^\(([A-E,、 ]+)\)\s*", "", exp).strip()


Q = []
for qname, aname, prefix, fixed in SETS:
    qt, at = text(os.path.join(SRC, qname)), text(os.path.join(SRC, aname))
    q_single = section(qt, "單選題", ["多選題", "配合題", "手寫題"])
    q_multi = section(qt, "多選題", ["配合題", "手寫題"])
    q_written = section(qt, "手寫題", [])
    key_s = parse_key(section(at, "單選題 簡答", ["多選題 簡答", "配合題 簡答", "單選題 詳解"]))
    key_m = parse_key(section(at, "多選題 簡答", ["配合題 簡答", "單選題 詳解"]))
    exp_s = section(at, "單選題 詳解", ["多選題 詳解", "多選題", "配合題 詳解", "配合題", "手寫題 詳解"])
    exp_m = section(at, "多選題 詳解", ["配合題 詳解", "手寫題 詳解"]) or section(at.split("單選題 詳解", 1)[-1], "多選題", ["配合題", "手寫題 詳解"])
    exp_w = section(at, "手寫題 詳解", [])
    n_s, n_m = max(key_s or {0: 0}), max(key_m or {0: 0})
    qs, qm, qw = split_numbered(q_single, n_s), split_numbered(q_multi, n_m), split_numbered(q_written, 30)
    es, em, ew = split_numbered(exp_s, n_s), split_numbered(exp_m, n_m), split_numbered(exp_w, 30)
    ch = (lambda seg, exp: fixed) if fixed else chapter_of

    for n, seg in qs.items():
        stem, opts = options(seg)
        ans = key_s.get(n, "")
        if not re.fullmatch(r"[A-E]+", ans):
            continue  # 考古沒有給答案（例：線蟲第 73 題「無答案」）
        exp = strip_ans(es.get(n, ""))
        q = {"id": f"{prefix}-{n:02d}", "source": SOURCE, "num": n, "chapter": ch(seg, exp[:300]),
             "type": "mcq", "stem": stem, "options": opts, "answer": list(ans),  # 例：BD → 兩個都算對
             "explain": exp or "（考古未附詳解）", "topics": [],
             "pattern": "選錯誤／否定題" if re.search(r"何者為非|何者錯誤|不是|錯誤|非|NOT|incorrect", stem) else "選正確／單一概念題"}
        if needs_image(stem, opts):
            q["imageOnly"] = True
        Q.append(q)

    for n, seg in qm.items():
        stem, opts = options(seg)
        ans = key_m.get(n, "")
        full = "全選（ABCDE）" if ans == "全" else "、".join(f"({c})" for c in ans)
        body = "（多選題）" + stem + "\n" + "\n".join(f"({o['k']}) {o['t']}" for o in opts)
        exp = strip_ans(em.get(n, ""))
        q = {"id": f"{prefix}-m{n:02d}", "source": SOURCE, "num": n, "chapter": ch(seg, exp[:300]),
             "type": "short", "stem": body, "options": [], "answer": [], "answerText": f"正確選項：{full}",
             "explain": exp or "（考古未附詳解）", "topics": [], "pattern": "多選題"}
        if needs_image(stem, opts):
            q["imageOnly"] = True
        Q.append(q)

    for n, seg in qw.items():
        ans = ew.get(n, "").strip()
        if not ans:
            continue
        q = {"id": f"{prefix}-w{n:02d}", "source": SOURCE, "num": n, "chapter": ch(seg, ans[:300]),
             "type": "short", "stem": "（手寫題）" + re.sub(r"\s*\(([A-F])\)\s*", r"\n(\1) ", seg).strip(),
             "options": [], "answer": [], "answerText": ans, "explain": "", "topics": [], "pattern": "簡答題"}
        if re.search(r"下圖|如圖", seg):
            q["imageOnly"] = True
        Q.append(q)

# 吸蟲配合題（w5~6 Trematodes 配合題 1–14，答案與詳解依 1151 寄蟲考古 Book1）。
# 單一答案 → mcq，A–O 共用選項；多個答案 → short（選項寫在題幹，避免被當成「任一個對就算對」）
TRE = ["Fasciolopsis buski", "Metagonimus yokogawai", "Heterophyes heterophyes", "Gastrodiscoides hominis",
       "Eurytrema spp.", "Opisthorchis felineus", "Clonorchis sinensis", "Opisthorchis viverrini", "Echinostoma spp.",
       "Fasciola hepatica", "Dicrocoelium dendriticum", "Paragonimus westermani", "Schistosoma japonicum",
       "Schistosoma haematobium", "Schistosoma mansoni"]
HOST = ["Paragonimus westermani", "Eurytrema spp.", "Dicrocoelium dendriticum", "Clonorchis sinensis", "Fasciola hepatica"]
KEYS = "ABCDEFGHIJKLMNO"


def match(n, opts, stem, ans, exp, note=None):
    q = {"id": f"k113-tre-p{n:02d}", "source": SOURCE, "num": n, "chapter": "trematodes", "stem": stem,
         "explain": exp, "topics": [], "pattern": "配對題"}
    if len(ans) == 1:
        q.update(type="mcq", stem="（配合題）" + stem, options=[{"k": k, "t": t} for k, t in zip(KEYS, opts)],
                 answer=[ans])
    else:
        listing = "\n".join(f"({k}) {t}" for k, t in zip(KEYS, opts))
        q.update(type="short", stem=f"（配合題，可複選）{stem}\n{listing}", options=[], answer=[],
                 answerText="、".join(f"({k}) {opts[KEYS.index(k)]}" for k in ans))
    if note:
        q["note"] = note
    Q.append(q)


match(1, TRE, "下列吸蟲中，體型最大的是？", "A",
      "Fasciolopsis buski（薑片蟲）長 2–7.5 cm，是寄生在人體最大的吸蟲，蟲卵也是人體寄生蟲卵中最大的。")
match(2, TRE, "下列吸蟲中，會經由食用水生植物而感染的是？", "ADIJ",
      "以水生植物為感染來源（metacercaria 附著在植物表面）：F. buski（菱角、荸薺、茭白筍）、Gastrodiscoides hominis、"
      "Echinostoma spp.（宿主多樣，水生植物也是其一）、Fasciola hepatica（水芹 watercress）。")
match(3, TRE, "下列吸蟲中，寄生在大腸的是？", "D",
      "Gastrodiscoides hominis（人雙口吸蟲）是少數寄生在盲腸、升結腸的腸吸蟲。薑片蟲數量多時可擴散到胃與大腸，但主要寄生在小腸上段。")
match(4, TRE, "下列吸蟲中，中間宿主可以是昆蟲的是？", "EIK",
      "Eurytrema（胰吸蟲）：第二中間宿主是蝗蟲類（草螽）。Dicrocoelium dendriticum（槍狀肝吸蟲）：第二中間宿主是螞蟻。"
      "Echinostoma 的第二中間宿主種類很多，昆蟲幼蟲也算在內。")
match(5, TRE, "下列吸蟲中，用 praziquantel 治療無效的是？", "J",
      "Fasciola hepatica 對 praziquantel 反應差，首選 triclabendazole（舊用 bithionol）；其他吸蟲多以 praziquantel 治療。")
match(6, TRE, "下列吸蟲中，體型最小的是？", "C",
      "Heterophyes heterophyes（異形異形吸蟲）約 1–1.7 × 0.3–0.4 mm，是人體最小的吸蟲；Metagonimus yokogawai 稍大（1–2.5 mm）。")
match(7, TRE, "下列吸蟲中，會經由食用螃蟹感染的是？", "L",
      "Paragonimus westermani（衛氏肺吸蟲）：第一中間宿主是川蜷螺，第二中間宿主是淡水蟹、蝦；生吃或吃醉蟹會感染。")
match(8, TRE, "下列吸蟲中，第二中間宿主為魚的是？", "BCFGH",
      "以魚為第二中間宿主：Metagonimus yokogawai（淡水魚）、Heterophyes heterophyes（烏魚等鹹淡水魚）、"
      "Opisthorchis felineus、Clonorchis sinensis、O. viverrini（淡水魚，鯉科為主）。",
      note="原考古另註：Echinostoma spp. 少數以魚為第二中間宿主，選 (I) 也可接受。")
match(9, TRE, "下列吸蟲中，可能引發腦部病理損傷的是？", "BCJLMNO",
      "異形吸蟲（B、C）：蟲卵可穿過腸壁進入血流，異位到腦、脊髓、心肌。\nFasciola hepatica（J）：幼蟲移行時可異位到肺、皮下、眼睛或腦。\n"
      "Paragonimus westermani（L）：最常見的異位部位是腦（膿瘍、囊腫）。\n血吸蟲（M、N、O）：蟲卵可異位沉積在中樞神經，S. japonicum 最常見。")
for n, ans, host, exp in [
    (10, "C", "螞蟻（ant）", "Dicrocoelium dendriticum：第一中間宿主是陸生蝸牛，第二中間宿主是螞蟻；人是誤食螞蟻而感染。"),
    (11, "E", "水中植物（aquatic plants）", "Fasciola hepatica：cercaria 在水芹等水生植物上形成 metacercaria，不需要第二中間宿主動物。"),
    (12, "B", "蝗蟲（grasshoppers）", "Eurytrema spp.（胰吸蟲）：第一中間宿主是陸生蝸牛，第二中間宿主是蝗蟲類（草螽）。"),
    (13, "D", "淡水魚（fish）", "Clonorchis sinensis：第一中間宿主是螺（Parafossarulus），第二中間宿主是淡水魚（草魚、鯉魚等）。"),
    (14, "A", "毛蟹（crab）", "Paragonimus westermani：第二中間宿主是淡水蟹、蝦（毛蟹、澤蟹等）。"),
]:
    match(n, HOST, f"中間宿主「{host}」對應的是哪一種寄生蟲？", ans, exp)

# 考點標籤：用章節名稱當作粗分類；跨三章以上的歸到總論「線蟲綜合比較」
TOPIC = {"intro": "總論：宿主與寄生型態", "sth": "土源性蠕蟲", "enterobius-toxocara": "蟯蟲與犬蛔蟲",
         "capillaria-strongyloides": "毛線蟲與糞小桿線蟲", "foodborne": "食源性線蟲", "filaria": "血絲蟲",
         "trematodes": "吸蟲"}
# 關鍵字判斷錯的題目，手動指定（compare = 線蟲綜合比較）
OVERRIDE = {"k113-nem-08": "intro", "k113-nem-10": "compare", "k113-nem-13": "intro", "k113-nem-w04": "compare"}
for q in Q:
    q["chapter"] = OVERRIDE.get(q["id"], q["chapter"])
    if q["chapter"] == "compare":
        q["chapter"], q["topics"] = "intro", ["線蟲綜合比較"]
    else:
        q["topics"] = [TOPIC[q["chapter"]]]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(OUT, len(Q), "questions;", sum(1 for q in Q if q.get("imageOnly")), "imageOnly")
