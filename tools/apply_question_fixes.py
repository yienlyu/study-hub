#!/usr/bin/env python3
"""題庫修正：把多選題轉成可點選的 multi 題，並套用 tools/question_fixes.json 的逐題修正。

題庫 JSON 由各 build_*.py 產生；重跑 builder 之後，依序再跑：
  python3 tools/apply_question_fixes.py
  python3 tools/apply_explain_overrides.py
（在 repo 根目錄）

1. 多選題轉換：type 為 short、題幹開頭是「（多選題）」或「（配合題，可複選）」、選項寫在題幹裡
   的題目 → type 改成 mcq、multi: true，選項從題幹拆出來，答案從 answerText 讀「(B)、(C)」或
   「全選（ABCDE）」。網站上要全部選對才算對。
2. 逐題修正：question_fixes.json 的格式是 {"科目資料夾": {"questions-xxx.json": {"題號": {欄位: 值}}}}，
   值是 null 代表刪掉這個欄位。常用欄位：
   answer（答案；一般題有多個表示任一個都算對）、options、multi、noAnswer（題目有誤、沒有正確選項）、
   img（題目附圖，相對於科目資料夾的路徑）、imageOnly。
"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXES = os.path.join(ROOT, "tools", "question_fixes.json")
MULTI_HEAD = re.compile(r"^（(多選題|配合題，可複選)）")
OPT = re.compile(r"(?:^|\s)\(([A-O])\)\s*")


def to_multi(q):
    """把選項寫在題幹裡的多選題拆成 options；拆不出來就維持原樣。"""
    stem = q["stem"]
    m = OPT.search(stem)
    if not m or m.group(1) != "A":
        return False
    head, body = stem[: m.start()].rstrip(), stem[m.start():]
    parts = OPT.split(body)[1:]  # [k, text, k, text, ...]
    keys, texts = parts[0::2], [t.strip() for t in parts[1::2]]
    if keys != [chr(65 + i) for i in range(len(keys))]:
        return False
    ans_txt = q.get("answerText", "")
    if "全選" in ans_txt:
        ans = keys[:]
    else:
        ans = sorted(set(re.findall(r"\(([A-O])\)", ans_txt)))
    if not ans or not set(ans) <= set(keys):
        return False
    q.update(type="mcq", multi=True, stem=head,
             options=[{"k": k, "t": t} for k, t in zip(keys, texts)], answer=ans)
    q.pop("answerText", None)
    return True


fixes = json.load(open(FIXES, encoding="utf-8"))
for subj in sorted(os.listdir(os.path.join(ROOT, "subjects"))):
    ddir = os.path.join(ROOT, "subjects", subj, "data")
    if subj.startswith("_") or not os.path.isdir(ddir):
        continue
    for fname in sorted(os.listdir(ddir)):
        if not fname.startswith("questions") or not fname.endswith(".json"):
            continue
        path = os.path.join(ddir, fname)
        raw = open(path, encoding="utf-8").read()
        qs = json.loads(raw)
        conv = 0
        for q in qs:
            if q.get("type") == "short" and MULTI_HEAD.match(q.get("stem", "")):
                conv += to_multi(q)
        items = fixes.get(subj, {}).get(fname, {})
        ids = {q["id"] for q in qs}
        missing = set(items) - ids
        if missing:
            raise SystemExit(f"{subj}/{fname}: 找不到題號 {sorted(missing)}")
        for q in qs:
            for k, v in items.get(q["id"], {}).items():
                if v is None:
                    q.pop(k, None)
                else:
                    q[k] = v
        out = json.dumps(qs, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else "")
        if (conv or items) and out != raw:
            open(path, "w", encoding="utf-8").write(out)
        if conv or items:
            print(f"{subj}/{fname}: 多選題轉換 {conv} 題、逐題修正 {len(items)} 題")
