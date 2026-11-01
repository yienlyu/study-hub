#!/usr/bin/env python3
"""重建題庫／圖表時保留手改：以後一律用這支跑 builder，不要直接跑 build_*.py。

用法（在 repo 根目錄）：
  python3 tools/rebuild.py tools/build_para_kaogu.py
  python3 tools/rebuild.py tools/biochem/parse_gongbi.py tools/biochem/build_questions.py
  python3 tools/rebuild.py --accept-builder tools/build_para_kaogu.py   # 這次 builder 的改動優先

流程：
1. 拍快照：subjects/*/data/*.json、subjects/*/figures.json、subjects/*/figures/*.svg。
2. 依序執行指定的 builder。
3. 套用既有修正：apply_question_fixes.py → apply_explain_overrides.py → apply_manual_edits.py。
4. 跟快照比對。被 builder 改掉、又不在上述修正檔裡的差異，就是「手改」：
   - 預設：手改優先。自動記進 tools/manual_edits.json 並套回，最後列出記了哪些。
   - --accept-builder：builder 優先。不記錄，並把 manual_edits.json 裡跟這次改動衝突的條目刪掉。
   builder 新增的題目、圖一律保留。
5. JSON 一律以重建前的原檔為底寫回（tools/jsonfmt.py）：只改內容有變的題目，其餘保留原排版，不會整檔重排。
"""
import glob
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(ROOT, "tools")
EDITS = os.path.join(TOOLS, "manual_edits.json")
FILES_DIR = os.path.join(TOOLS, "manual_files")
sys.path.insert(0, TOOLS)
from jsonfmt import write_preserving  # noqa: E402

APPLIERS = ["apply_question_fixes.py", "apply_explain_overrides.py", "apply_manual_edits.py"]


def tracked():
    pats = ["subjects/*/data/*.json", "subjects/*/figures.json", "subjects/*/figures/*.svg"]
    return sorted({os.path.relpath(p, ROOT) for pat in pats for p in glob.glob(os.path.join(ROOT, pat))})


def snapshot():
    return {rel: open(os.path.join(ROOT, rel), "rb").read() for rel in tracked()}


def run(script):
    print(f"$ python3 {script}")
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def load_edits():
    return json.load(open(EDITS, encoding="utf-8")) if os.path.exists(EDITS) else {}


def save_edits(edits):
    with open(EDITS, "w", encoding="utf-8") as f:
        f.write(json.dumps(edits, ensure_ascii=False, indent=1, sort_keys=True) + "\n")


def diff_list(old, new):
    """回傳 (fields, added, removed)：要把 new 變回 old 需要的手改。"""
    o = {x["id"]: x for x in old}
    n = {x["id"]: x for x in new}
    fields = {}
    for i, ox in o.items():
        if i not in n:
            continue
        nx = n[i]
        d = {k: ox[k] for k in ox if nx.get(k, object()) != ox[k]}
        d.update({k: None for k in nx if k not in ox})
        if d:
            fields[i] = d
    added = []
    prev = None
    for x in old:
        if x["id"] not in n:
            added.append({"after": prev, "item": x})
        prev = x["id"]
    removed = [i for i in n if i not in o]
    return fields, added, removed


def main():
    args = sys.argv[1:]
    accept = "--accept-builder" in args
    builders = [a for a in args if a != "--accept-builder"]
    if not builders:
        sys.exit(__doc__)
    before = snapshot()
    for b in builders:
        run(b)
    for a in APPLIERS:
        run(os.path.join("tools", a))
    after = snapshot()

    edits = load_edits()
    report = []
    for rel, old in before.items():
        new = after.get(rel)
        if new == old:
            continue
        if accept:
            if rel in edits:
                del edits[rel]
                report.append(f"{rel}：依 builder 結果，刪掉原本記錄的手改")
            continue
        if rel.endswith(".svg"):
            keep = os.path.join(FILES_DIR, rel)
            os.makedirs(os.path.dirname(keep), exist_ok=True)
            open(keep, "wb").write(old)
            edits[rel] = {"file": os.path.relpath(keep, ROOT)}
            report.append(f"{rel}：保留手改版本（存到 {os.path.relpath(keep, ROOT)}）")
            continue
        old_j, new_j = json.loads(old), json.loads(new)
        if not (isinstance(old_j, list) and isinstance(new_j, list)):
            # 物件格式的檔案（例：bigtable.json）本身就是手寫來源，builder 只補欄位，直接採用
            report.append(f"{rel}：非清單格式，採用 builder 結果（不記手改）")
            continue
        fields, added, _ = diff_list(old_j, new_j)  # builder 新增的題目一律保留
        if not (fields or added):
            continue
        spec = edits.setdefault(rel, {})
        for i, d in fields.items():
            spec.setdefault("fields", {}).setdefault(i, {}).update(d)
        have = {a["item"]["id"] for a in spec.get("added", [])}
        for a in added:
            if a["item"]["id"] in have:
                spec["added"] = [a if x["item"]["id"] == a["item"]["id"] else x for x in spec["added"]]
            else:
                spec.setdefault("added", []).append(a)
        n_f = sum(len(d) for d in fields.values())
        report.append(f"{rel}：記錄 {len(fields)} 題共 {n_f} 個欄位的手改、{len(added)} 題手加的題目")
    for rel in after:
        if rel not in before:
            report.append(f"{rel}：builder 新產生的檔案")
    save_edits(edits)
    if not accept:
        run(os.path.join("tools", "apply_manual_edits.py"))
    # builder 會整個重寫檔案（排版可能跟原檔不同）：以原檔為底，只改內容有變的部分，
    # 內容沒變就還原原本的位元組，避免整檔重排的 git diff
    for rel, old in before.items():
        path = os.path.join(ROOT, rel)
        if rel.endswith(".json") and os.path.exists(path):
            cur = open(path, "rb").read()
            if cur == old:
                continue
            data = json.loads(cur)
            if data == json.loads(old):
                open(path, "wb").write(old)
            else:
                write_preserving(path, old.decode("utf-8"), data)
    print("\n== 重建結果 ==")
    print("\n".join(report) if report else "沒有任何手改被蓋掉。")


if __name__ == "__main__":
    main()
