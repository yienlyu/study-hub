#!/usr/bin/env python3
"""把 tools/manual_edits.json 記錄的手改套回產生出來的檔案。

各 build_*.py 會整個重寫 subjects/*/data/*.json、subjects/*/figures.json 與部分 SVG。
直接手改這些檔案沒關係，只要之後用 tools/rebuild.py 重建：它會在重建前拍快照，
把被蓋掉的手改自動記進 manual_edits.json，再由這支套回去。

manual_edits.json 的格式（路徑相對於 repo 根目錄）：
{
  "subjects/biochem/data/questions-new.json": {
    "fields":  {"題號": {"欄位": 值}},          # 值為 null 表示刪掉這個欄位
    "added":   [{"after": "前一題題號或 null", "item": {...整題...}}],
    "removed": ["題號"]
  },
  "subjects/parasitology/figures/xxx.svg": {"file": "tools/manual_files/subjects/parasitology/figures/xxx.svg"}
}

執行：python3 tools/apply_manual_edits.py（在 repo 根目錄；rebuild.py 會自動呼叫）
"""
import json
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EDITS = os.path.join(ROOT, "tools", "manual_edits.json")


def load_edits():
    if not os.path.exists(EDITS):
        return {}
    return json.load(open(EDITS, encoding="utf-8"))


def dump_list(path, items, raw):
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(items, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else ""))


def apply_list(path, spec):
    raw = open(path, encoding="utf-8").read()
    items = json.loads(raw)
    before = json.dumps(items, ensure_ascii=False)
    removed = set(spec.get("removed", []))
    items = [x for x in items if x["id"] not in removed]
    have = {x["id"] for x in items}
    for add in spec.get("added", []):
        it = add["item"]
        if it["id"] in have:
            items = [it if x["id"] == it["id"] else x for x in items]
            continue
        ids = [x["id"] for x in items]
        pos = ids.index(add["after"]) + 1 if add.get("after") in ids else (0 if add.get("after") is None else len(items))
        items.insert(pos, it)
        have.add(it["id"])
    for x in items:
        for k, v in spec.get("fields", {}).get(x["id"], {}).items():
            if v is None:
                x.pop(k, None)
            else:
                x[k] = v
    missing = set(spec.get("fields", {})) - {x["id"] for x in items}
    if json.dumps(items, ensure_ascii=False) != before:
        dump_list(path, items, raw)
        return True, missing
    return False, missing


def main():
    edits = load_edits()
    changed = 0
    for rel, spec in edits.items():
        path = os.path.join(ROOT, rel)
        if "file" in spec:
            src = os.path.join(ROOT, spec["file"])
            if not os.path.exists(path) or open(path, "rb").read() != open(src, "rb").read():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                shutil.copyfile(src, path)
                changed += 1
                print(f"還原手改檔案：{rel}")
            continue
        if not os.path.exists(path):
            print(f"⚠️ 找不到 {rel}，略過")
            continue
        did, missing = apply_list(path, spec)
        if missing:
            print(f"⚠️ {rel}：找不到題號 {sorted(missing)}（可能已被 builder 改名，請檢查 manual_edits.json）")
        if did:
            changed += 1
            print(f"套回手改：{rel}")
    print(f"共套回 {changed} 個檔案")


if __name__ == "__main__":
    main()
