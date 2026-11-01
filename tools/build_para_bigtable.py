#!/usr/bin/env python3
"""從「究極青眼白蟲」大表 PDF 裁出吸蟲頁（p2）的蟲體、蟲卵照片，給比較大表用。

表格文字（含紅筆手寫補充與 ⚠️ 共筆對照）是手打在 subjects/parasitology/data/bigtable.json，
這支只負責圖片，並把圖片尺寸寫回 bigtable.json 各欄的 imgs。來源 PDF：slides/parasitology/共筆考古/0 究極青眼白蟲.pdf

用法（repo 根目錄）：python3 tools/build_para_bigtable.py
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF = os.path.join(ROOT, "slides/parasitology/共筆考古/0 究極青眼白蟲.pdf")
OUT = os.path.join(ROOT, "subjects/parasitology/figures/bigtable")
DATA = os.path.join(ROOT, "subjects/parasitology/data/bigtable.json")
DPI = 432
K = DPI / 72

# p2 欄界線（pt，由表格線偵測）與對應的欄 id（和 bigtable.json 的 cols 一致）
XS = [23.5, 58.5, 95.8, 130.5, 162.2, 198, 235.5, 275.8, 308, 343, 380.5, 419.5, 451, 487.5, 526, 566, 608]
IDS = ["fbuski", "heterophyes", "metagonimus", "echinostoma", "gastrodiscoides", "eurytrema",
       "paragonimus", "clonorchis", "o-felineus", "opisthorchis", "dicrocoelium", "fasciola",
       "f-gigantica", "s-mansoni", "s-japonicum", "s-haematobium"]
ROWS = {"body": (371.5, 455), "egg": (490, 552.8)}


def trim(im):
    a = np.asarray(im.convert("L"))
    ink = a < 235
    ys, xs = np.where(ink)
    if len(xs) < 400:
        return None
    pad = 4
    return im.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                    min(xs.max() + pad, im.width), min(ys.max() + pad, im.height)))


def main():
    if not os.path.exists(PDF):
        sys.exit(f"找不到 {PDF}")
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", "2", "-l", "2", PDF, f"{tmp}/p"], check=True)
        page = Image.open(next(os.path.join(tmp, f) for f in os.listdir(tmp))).convert("RGB")
    made = []
    for kind, (y0, y1) in ROWS.items():
        for i, cid in enumerate(IDS):
            inset = 2  # 避開表格線
            box = ((XS[i] + inset) * K, (y0 + inset) * K, (XS[i + 1] - inset) * K, (y1 - inset) * K)
            im = trim(page.crop(tuple(round(v) for v in box)))
            if im is None:
                continue
            path = os.path.join(OUT, f"{cid}-{kind}.webp")
            im.save(path, "WEBP", quality=82)
            made.append((path, im.width, im.height))
    # 把圖片尺寸寫回 bigtable.json（放大檢視要用），其他內容不動
    sizes = {os.path.relpath(p, os.path.join(ROOT, "subjects/parasitology")): (w, h) for p, w, h in made}
    data = json.load(open(DATA, encoding="utf-8"))
    for t in data["tables"]:
        for c in t["cols"]:
            imgs = {}
            for kind in ROWS:
                src = f"figures/bigtable/{c['id']}-{kind}.webp"
                if src in sizes:
                    imgs[kind] = {"src": src, "w": sizes[src][0], "h": sizes[src][1]}
            if imgs:
                c["imgs"] = imgs
            else:
                c.pop("imgs", None)
    with open(DATA, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    for p, w, h in made:
        print(f"{os.path.relpath(p, ROOT)}\t{w}x{h}")


if __name__ == "__main__":
    main()
