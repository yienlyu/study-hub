#!/usr/bin/env python3
"""把 tools/explain_overrides.json 的詳解補到各科題庫（依題號覆寫 explain）。

題庫 JSON 由各 build_*.py 產生；重跑任何 builder 之後，要再跑一次這支，補寫的詳解才不會消失。
explain_overrides.json 的格式：{"科目資料夾": {"questions-xxx.json": {"題號 id": "詳解（純文字）"}}}
執行：python3 tools/apply_explain_overrides.py（在 repo 根目錄）
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OVR = os.path.join(ROOT, "tools", "explain_overrides.json")

overrides = json.load(open(OVR, encoding="utf-8"))
total = 0
for subj, files in overrides.items():
    for fname, items in files.items():
        path = os.path.join(ROOT, "subjects", subj, "data", fname)
        raw = open(path, encoding="utf-8").read()
        qs = json.loads(raw)
        ids = {q["id"] for q in qs}
        missing = set(items) - ids
        if missing:
            raise SystemExit(f"{subj}/{fname}: 找不到題號 {sorted(missing)}")
        n = 0
        for q in qs:
            if q["id"] in items and q.get("explain") != items[q["id"]]:
                q["explain"] = items[q["id"]]
                n += 1
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(qs, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else ""))
        total += n
        print(f"{subj}/{fname}: 更新 {n} 題")
print(f"共更新 {total} 題")
