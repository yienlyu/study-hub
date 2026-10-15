#!/usr/bin/env python3
"""生化（二）陳顧中《Ch18、22、23 練習題》→ subjects/biochem/data/questions-prac.json

來源：slides/biochemistry/Ch18、22、23 練習題.pdf（160 題，附答案與解析）
- 第一單元（1–54）器官能量代謝與激素調控 → ch23
- 第二、三單元（55–120）胺基酸氧化、尿素循環、胺基酸衍生物、血基質 → ch18
- 第四單元（121–160）進階難度，章節逐題指定；講義以深紅色標示的題目「僅供參考」
需要 poppler 的 pdftotext。執行：python3 tools/build_biochem_prac.py（在 repo 根目錄）
"""
import json
import re
import subprocess

PDF = "slides/biochemistry/Ch18、22、23 練習題.pdf"
OUT = "subjects/biochem/data/questions-prac.json"
SRC = "陳顧中練習題"
REF_ONLY = {137, 142, 147, 151, 156}  # 講義深紅色標示
REF_NOTE = "（講義以深紅色標示，僅供參考）"

CJK = r"　-〿㐀-鿿＀-￯"

# 題號 → (章節, 主題)；沒列章節的依單元決定
T23 = {
    "各器官燃料代謝": [1, 2, 3, 5, 6, 7, 8, 10, 23, 24, 25, 28, 40, 41, 42, 133, 141, 148, 149],
    "Cori／葡萄糖-丙胺酸循環": [4, 26, 140, 142],
    "胰島素與 GLUT": [11, 12, 13, 14, 15, 16, 29, 30, 31, 44, 45, 46, 123, 143, 144],
    "升糖素、腎上腺素與 cAMP": [17, 18, 34, 35, 52, 126],
    "AMPK": [19, 36, 50, 54, 145],
    "瘦素與脂肪激素": [20, 21, 32, 33, 47, 48, 49],
    "腸泌素": [22, 51, 130],
    "飢餓與糖尿病": [9, 27, 37, 38, 53, 139, 146],
    "酮體": [39, 43, 132, 147, 156],
}
T18 = {
    "尿素循環": [55, 60, 61, 62, 68, 69, 70, 81, 82, 83, 84, 122, 137, 150, 151, 152],
    "蛋白質消化與泛素": [56, 57, 75, 76],
    "轉胺與 PLP": [58, 59, 66, 67, 77, 80, 85, 131],
    "BCAA": [63],
    "一碳單位與輔酶（THF／BH4／B12）": [64, 72, 87, 88, 89, 90, 128, 136, 153, 154, 155],
    "胺基氮運輸（Gln／Ala）": [65, 78, 79, 125],
    "輔因子": [71, 86, 91, 92, 98, 121],
    "生酮／生醣胺基酸": [73, 74, 93, 94, 95, 96],
    "先天胺基酸代謝疾病": [97, 99, 100, 124, 129, 134, 135, 160],
    "胺基酸衍生物": list(range(101, 115)) + [138, 158, 159],
    "Heme 與膽紅素": list(range(115, 121)) + [127, 157],
}
TOPIC = {n: ("ch23", t) for t, ns in T23.items() for n in ns}
TOPIC.update({n: ("ch18", t) for t, ns in T18.items() for n in ns})

# PDF 斷行／排版造成的字串問題
FIXES = [
    ("(B) 人類尿素", "(B) 人類-尿素"),
    ("PFK-2/FBPase20 2", "PFK-2/FBPase-2"),
    ("propionylCoA", "propionyl-CoA"), ("methylmalonylCoA", "methylmalonyl-CoA"),
    ("Sadenosylmethionine", "S-adenosylmethionine"), ("UDPglucuronyl", "UDP-glucuronyl"),
    ("δaminolevulinate", "δ-aminolevulinate"), ("ATPgated", "ATP-gated"), ("αketo", "α-keto"),
    ("glucose 6phosphatase", "glucose 6-phosphatase"), ("脱", "脫"), ("羟", "羥"), ("醟", "醯"),
    ("檬檬酸", "檸檬酸"),
]


def join(lines):
    out = ""
    for ln in (x.strip() for x in lines):
        if not ln:
            continue
        if out and not (re.search(f"[{CJK}]$", out) or re.match(f"[{CJK}]", ln)) and not out.endswith("-"):
            out += " "
        out += ln
    out = re.sub(f"(?<=[{CJK}]) +(?=[{CJK}])", "", out)  # 去掉左右對齊撐開的空白
    out = re.sub(r"(?<=[（「]) +| +(?=[）」，、。；：])", "", out)
    out = re.sub(r"(?<=[A-Za-z0-9])(?=[㐀-鿿])|(?<=[㐀-鿿])(?=[A-Za-z0-9])", " ", out)  # 中英之間補空白
    return out


def pattern(stem):
    if re.search(r"患者|病人|病童|新生兒|嬰兒|早產兒|一名|兒童|受試者|酗酒|選手", stem):
        return "臨床情境題"
    if re.search(r"錯誤|不是|不參與|不以|不經|最不|不受影響", stem):
        return "選錯誤（否定）題"
    if "配對" in stem:
        return "配對題"
    return "選正確／單一概念題"


text = subprocess.run(["pdftotext", PDF, "-"], capture_output=True, text=True, check=True).stdout.replace("\f", "\n")
lines = [ln for ln in text.split("\n") if not re.fullmatch(r"\s*\d{1,2}\s*", ln)
         and not re.match(r"第[一二三四]單元|器官能量代謝與激素調控|進階難度|講義對照", ln.strip())]

# 依序切題（只接受下一個題號，避免把內文數字誤判成題號）
blocks, cur, nxt = {}, None, 1
for ln in lines:
    m = re.match(rf"{nxt}\.\s", ln)
    if m:
        cur, nxt = nxt, nxt + 1
        blocks[cur] = [ln[m.end():]]
    elif cur:
        blocks[cur].append(ln)
assert len(blocks) == 160, len(blocks)

Q = []
for num, bl in blocks.items():
    raw = "\n".join(bl)
    m = re.search(r"答\s*案\s*[：:]?\s*\(?\s*([A-D])\s*\)?", raw)
    assert m, num
    head, tail = raw[:m.start()], raw[m.end():].split("\n")
    # pdftotext 有時把解析最後一小段排到最前面（後面接空行）→ 移回句尾
    first = next((i for i, x in enumerate(tail) if x.strip()), None)
    if first is not None and len(tail[first].strip()) <= 6 and first + 1 < len(tail) and not tail[first + 1].strip():
        tail = tail[:first] + tail[first + 1:] + [tail[first]]
    head = join(head.split("\n"))
    exp = re.sub(r"^解析：", "", join(tail))
    for a, b in FIXES:
        head, exp = head.replace(a, b), exp.replace(a, b)
    parts = re.split(r"\s*\(([A-D])\)\s*", head)
    stem, opts = parts[0].strip(), dict(zip(parts[1::2], (p.strip() for p in parts[2::2])))
    assert list(opts) == list("ABCD"), (num, list(opts))
    ch, topic = TOPIC[num]
    Q.append({"id": f"prac-{num:03d}", "source": SRC, "num": num, "chapter": ch, "type": "mcq", "stem": stem,
              "options": [{"k": k, "t": t} for k, t in opts.items()], "answer": [m.group(1)],
              "explain": (REF_NOTE if num in REF_ONLY else "") + exp, "topics": [topic], "pattern": pattern(stem)})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(f"{len(Q)} 題 → {OUT}")
