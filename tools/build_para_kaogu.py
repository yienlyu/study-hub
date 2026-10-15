#!/usr/bin/env python3
"""寄蟲考古：百十三「w1~4 Nematodes」與「w5~6 Trematodes」(題＋解) → subjects/parasitology/data/questions-kaogu.json

來源：slides/parasitology/共筆考古/百十三資料/考古期中/（題）與（解）PDF
需要 pymupdf（import fitz）。執行：python3 tools/build_para_kaogu.py（在 repo 根目錄）
- 配合題略過（需要對照表）；單選題 → mcq；多選題 → short（選項寫在題幹，參考答案顯示正確選項，避免被當成「任一個對就算對」）
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
