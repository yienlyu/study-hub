#!/usr/bin/env python3
"""寄蟲考古：109 期中（一）（二）、109 期中補考、110 期中 → subjects/parasitology/data/questions-k109.json

來源：slides/parasitology/共筆考古/百十三資料/考古期中/寄蟲考古 109*.pdf、110*.pdf（每份 PDF 前半是題目，後半是「解答」：簡答表＋詳解）
需要 pymupdf（import fitz）。執行：python3 tools/build_para_k109.py（在 repo 根目錄；先跑 build_para_kaogu.py，這裡會跳過與 113 考古重複的題）
- 單選題 → mcq；多選題、配合題 → short（選項寫在題幹，參考答案顯示正確選項）
- 題目或選項需要原圖的 → imageOnly（不進練習）
- 與 113 考古或前面幾份完全相同（題幹＋選項）的題目略過
"""
import difflib, json, os, re
import fitz

SRC = "slides/parasitology/共筆考古/百十三資料/考古期中"
SETS = [  # (檔名, id 前綴, 來源標籤)
    ("寄蟲考古 109期中 (一).pdf", "k109a", "109 期中考古"),
    ("寄蟲考古 109期中 (二）.pdf", "k109b", "109 期中考古"),
    ("寄蟲考古 109期中補考.pdf", "k109m", "109 期中考古"),
    ("寄蟲考古 110期中 .pdf", "k110", "110 期中考古"),
]
OUT = "subjects/parasitology/data/questions-k109.json"
EXISTING = "subjects/parasitology/data/questions-kaogu.json"
TOPIC = {"intro": "總論：宿主與寄生型態", "sth": "土源性蠕蟲", "enterobius-toxocara": "蟯蟲與犬蛔蟲",
         "capillaria-strongyloides": "毛線蟲與糞小桿線蟲", "foodborne": "食源性線蟲", "filaria": "血絲蟲",
         "trematodes": "吸蟲"}
TRE = r"Schistosom|Paragonimus|Fasciol|Clonorchis|Metagonimus|Heterophyes|Echinostom|Dicrocoel|Opisthorch|Eurytrema|Gastrodisc|吸蟲|血吸蟲|miracidium|Miracidium|cercaria|Cercaria|redia|Redia|sporocyst|Sporocyst|metacercaria|Swimmer|尾動幼蟲|纖毛幼蟲|雷氏幼蟲|胞狀幼蟲|Biomphalaria|Oncomelania|Bulinus|螺"


def text(path):
    return "\n".join(p.get_text() for p in fitz.open(path))


def flat(s):
    return " ".join(s.split())


def split_numbered(body, n_max, pat=r"(?:^|\s){n}\.\s"):
    """依序切出 1.、2.、… 的段落（只接受下一個預期的題號）。"""
    starts, pos, n = [], 0, 1
    while n <= n_max:
        m = re.compile(pat.format(n=n)).search(body, pos)
        if not m:
            break
        starts.append((n, m.start()))
        pos, n = m.end(), n + 1
    out = {}
    for i, (num, s) in enumerate(starts):
        e = starts[i + 1][1] if i + 1 < len(starts) else len(body)
        out[num] = re.sub(rf"^\s*{num}\.\s*", "", body[s:e]).strip()
    return out


def options(seg):
    parts = re.split(r"\(([A-P])\)\s*", seg)
    stem = parts[0].strip()
    return stem, [{"k": parts[i], "t": parts[i + 1].strip()} for i in range(1, len(parts) - 1, 2)]


def parse_key(block):
    """簡答表：每列先 n 個題號再 n 個答案；整份依序配對即可。"""
    toks = re.sub(r"單選題?|多選題?", " ", block).split()
    nums = [int(t) for t in toks if t.isdigit()]
    vals = [t for t in toks if not t.isdigit()]
    return dict(zip(nums, vals))


def norm(q):
    """比對重複用：題幹＋選項內容（不管選項順序；多選題的選項寫在題幹裡）。"""
    k = lambda s: re.sub(r"[\s\W_]+", "", s).lower()
    return k(q["stem"]) + "|" + "|".join(sorted(k(o["t"]) for o in q.get("options", [])))


def needs_image(stem, opts):
    return bool(re.search(r"如附圖|如下圖|如圖|下圖|右圖|左圖|圖中", stem)) or (opts is not None and (not opts or any(not o["t"] for o in opts)))


def pattern(stem):
    return "選錯誤／否定題" if re.search(r"何者為非|何者錯誤|不正確|錯誤|不是|非|NOT|incorrect", stem) else "選正確／單一概念題"


def unwrap(e):
    """PDF 每行固定寬度斷行：長行接到下一行；短行（表格格子、標題）或下一行是 (A)、註、①… 開頭時保留換行。"""
    lines = [l.strip() for l in e.splitlines() if l.strip()]
    out = ""
    for i, l in enumerate(lines):
        if i and (len(lines[i - 1]) < 30 or re.match(r"\([A-P]\)|註|＊|[①-⑩]|→", l)):
            out += "\n"
        elif i:
            out += "" if re.search(r"[\u4e00-\u9fff，、）]$", lines[i - 1]) and re.match(r"[\u4e00-\u9fff（]", l) else " "
        out += l
    return out.strip()


def clean_exp(e):
    return unwrap(re.sub(r"^\s*\([A-E]\)(?:\s*or\s*\([A-E]\))*", "", e, count=1))


# 線蟲章節關鍵字規則與 113 考古共用：只執行 build_para_kaogu.py 的函式定義部分，不重新輸出
existing = json.load(open(EXISTING, encoding="utf-8"))
_rules_path = os.path.join(os.path.dirname(__file__), "build_para_kaogu.py")
rules_mod = {}
exec(compile(open(_rules_path, encoding="utf-8").read().split("\nQ = []")[0], _rules_path, "exec"), rules_mod)
RULES = rules_mod["CH_RULES"]


def chapter(s):
    # 題幹（選項 "(A)" 之前）只點名一類蟲時，就以題幹為準；否則看整題＋詳解
    stem = re.split(r"\(A\)", s, 1)[0]
    hits = {ch for ch, p in RULES if re.search(p, stem)} | ({"trematodes"} if re.search(TRE, stem) else set())
    if len(hits) == 1:
        return hits.pop()
    tre = len(re.findall(TRE, s))
    nem = sum(len(re.findall(p, s)) for _, p in RULES)
    if tre and tre >= nem:
        return "trematodes"
    return rules_mod["_chapter"](s) or "intro"


seen = {norm(q) for q in existing}
mismatch = []
Q, dup = [], 0
for fname, prefix, source in SETS:
    t = text(os.path.join(SRC, fname))
    head, ans = re.split(r"\n\s*\d+\s*寄蟲期中(?:補考)?解答.*\n", t, maxsplit=1)
    key_txt, exp_txt = ans.split("\n詳解", 1)
    key_txt = key_txt.split("簡答", 1)[1]

    # 題目區塊
    def sec(s, start, ends):
        if start not in s:
            return ""
        s = s.split(start, 1)[1]
        cut = min([s.find(e) for e in ends if e in s] or [len(s)])
        return s[:cut]

    q_s = sec(head, "單選題", ["多選題", "問答題", "配合題"])
    q_m = sec(head, "多選題", ["問答題", "配合題"])
    q_w = sec(head, "問答題", ["配合題"])
    q_x = sec(head, "配合題", [])
    k_s = parse_key(re.split(r"多選|問答題|配合題", key_txt)[0])
    k_m = parse_key(sec(key_txt, "多選", ["問答題", "配合題"])) if "多選" in key_txt else {}
    e_s = sec(exp_txt if "單選題" in exp_txt else "單選題" + exp_txt, "單選題", ["多選題", "問答題", "配合題"])
    e_m = sec(exp_txt, "多選題", ["問答題", "配合題"])
    e_w = sec(exp_txt, "問答題", ["配合題"])
    e_x = sec(exp_txt, "配合題", [])
    n_s, n_m = max(k_s or {0: 0}), max(k_m or {0: 0})
    qs, qm = split_numbered(q_s, n_s), split_numbered(q_m, n_m)
    es, em = split_numbered(e_s, n_s), split_numbered(e_m, n_m)

    def add(q, raw):
        global dup
        k = norm(q)
        stem, opts = k.split("|", 1)
        # 題幹相同、選項只差錯字（例：viverrini／viverrine）也算重複
        if k in seen or any(s.split("|", 1)[0] == stem and difflib.SequenceMatcher(None, sorted(s.split("|", 1)[1]), sorted(opts)).ratio() > 0.9 for s in seen):
            dup += 1
            return
        seen.add(k)
        Q.append(q)

    for n, seg in qs.items():
        raw_exp = es.get(n, "")
        # 答案以詳解開頭的 (X) 為準：簡答表抽成文字時偶爾會少格、整排錯位
        head_ans = re.match(r"\s*\([A-E]\)(?:\s*or\s*\([A-E]\))*", raw_exp)  # 例：(A)or(C) → 兩個都算對
        a = "".join(re.findall(r"[A-E]", head_ans.group())) if head_ans else "".join(re.findall(r"[A-E]", k_s.get(n, "")))
        if not a:
            continue
        if head_ans and k_s.get(n) and not set(k_s[n]) <= set(a):
            mismatch.append(f"{prefix}-{n:02d} 簡答表 {k_s[n]} / 詳解 {a}")
        stem, opts = options(flat(seg))
        answer = sorted(set(a))
        exp = clean_exp(raw_exp)
        q = {"id": f"{prefix}-{n:02d}", "source": source, "num": n, "chapter": chapter(flat(seg) + " " + exp[:300]),
             "type": "mcq", "stem": stem, "options": opts, "answer": answer,
             "explain": exp or "（考古未附詳解）", "topics": [], "pattern": pattern(stem)}
        if needs_image(stem, opts):
            q["imageOnly"] = True
        add(q, seg)

    for n, seg in qm.items():
        a = k_m.get(n, "")
        stem, opts = options(flat(seg))
        body = "（多選題）" + stem + "\n" + "\n".join(f"({o['k']}) {o['t']}" for o in opts)
        exp = re.sub(r"^\s*(\([A-E]\))+", "", em.get(n, "")).strip()
        q = {"id": f"{prefix}-m{n:02d}", "source": source, "num": n, "chapter": chapter(flat(seg) + " " + exp[:300]),
             "type": "short", "stem": body, "options": [], "answer": [],
             "answerText": "正確選項：" + "、".join(f"({c})" for c in a),
             "explain": clean_exp(exp) or "（考古未附詳解）", "topics": [], "pattern": "多選題"}
        if needs_image(stem, opts):
            q["imageOnly"] = True
        add(q, seg)

    # 問答題（110）：第 1 題答案是大表格，抽成文字讀不懂，略過
    k_w = split_numbered(sec(key_txt, "問答題", ["配合題"]), 10, r"(?:^|\n)\s*{n}\.")
    for n, seg in split_numbered(q_w, 10).items():
        a = (k_w.get(n) or split_numbered(e_w, 10).get(n, "")).strip()
        if n == 1 or not a:
            continue
        q = {"id": f"{prefix}-w{n:02d}", "source": source, "num": n, "chapter": chapter(flat(seg) + " " + a[:300]),
             "type": "short", "stem": "（問答題）" + re.sub(r"\s*\(([A-F])\)\s*", r"\n(\1) ", flat(seg)).strip(),
             "options": [], "answer": [], "answerText": unwrap(a), "explain": "", "topics": [], "pattern": "簡答題"}
        add(q, seg)

    # 配合題（110）：每組一張選項表，下面 1.、2.… 小題；答案在詳解 1-1. 這種編號
    groups = re.split(r"[①②③④]\.\s*根據下列選項，回答以下問題[^\n]*\n", q_x)[1:]
    for gi, g in enumerate(groups, 1):
        opts_part, _, subs = g.partition("\n1. ")
        subs = "1. " + subs
        _, opts = options(flat(opts_part))
        table = "\n".join(f"({o['k']}) {o['t']}" for o in opts)
        for n, sub in split_numbered(subs, 10).items():
            m = re.search(rf"{gi}-{n}\.\s*([A-P()]+)\s*(.*?)(?=\n\s*\d-\d\.|\n註：|$)", e_x, re.S)
            if not m:
                continue
            letters = re.sub(r"[()]", "", m.group(1))
            q = {"id": f"{prefix}-x{gi}{n}", "source": source, "num": n,
                 "chapter": "trematodes" if gi == 1 else "intro",
                 "type": "short", "stem": f"（配合題，可複選）{flat(sub)}\n{table}", "options": [], "answer": [],
                 "answerText": "正確選項：" + "、".join(f"({c})" for c in letters),
                 "explain": clean_exp(m.group(2)) + "\n（括號內的選項是 110 解答與傳承考古不同之處；解答者註明配合題答案僅供參考）",
                 "topics": [], "pattern": "配合題"}
            if gi == 2:
                q["topics"] = ["線蟲綜合比較"]
            add(q, sub)

for q in Q:
    if q["chapter"] == "compare":  # 跨三種以上線蟲的綜合比較題 → 總論
        q["chapter"], q["topics"] = "intro", ["線蟲綜合比較"]
    elif not q["topics"]:
        q["topics"] = [TOPIC[q["chapter"]]]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
# 簡答表與詳解不一致的題（多半是簡答表抽字時錯位）：python3 tools/build_para_k109.py -v 可列出
if "-v" in __import__("sys").argv:
    print("\n".join(mismatch))
print(OUT, len(Q), "questions;", sum(1 for q in Q if q.get("imageOnly")), "imageOnly;", dup, "duplicates skipped")
