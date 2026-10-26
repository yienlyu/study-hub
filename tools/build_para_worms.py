#!/usr/bin/env python3
"""寄蟲蟲卡圖片 → subjects/parasitology/figures/worms/，並把 src、w、h 寫回 data/worms.json

worms.json 每隻蟲的 imgs 寫 {kind, pdf, page, box?}：
- pdf：NEM（1線蟲圖檔）、TRE（2吸蟲圖檔）、LAB（吸蟲實驗）、D0907、D0914、D0922（上課 deck 另存的 PDF）
- box：頁面比例 (x0, y0, x1, y1)。圖譜預設切掉上方標題列與頁尾，蟲卡「看圖猜蟲」時才不會直接看到學名
需要 pymupdf 與 Pillow。執行：python3 tools/build_para_worms.py（在 repo 根目錄）
"""
import io, json, os
import fitz
from PIL import Image

SRC = "slides/parasitology"
ROOT = "subjects/parasitology"
OUT = f"{ROOT}/figures/worms"
DATA = f"{ROOT}/data/worms.json"
W = 1000

PDF = {
    "NEM": "1線蟲圖檔.pdf",
    "TRE": "2吸蟲圖檔.pdf",
    "LAB": "吸蟲實驗.pdf",
    "D0907": "20260907-北醫醫學系-M2-Introduction_  STHs_ Toxocara canis_ Enterobius vermicularis.pdf",
    "D0914": "20260914-北醫醫學系-M2-Capillaria_ Strongyloides stercoralis_ Foodborne Nematodes.pdf",
    "D0922": "20250922-M2-Trichinella_ Anisakis_ Angiostrongylus cantonensis_ Filaria.pdf",
}
DECK = {"NEM": "線蟲圖譜（1 線蟲圖檔）", "TRE": "吸蟲圖譜（2 吸蟲圖檔）", "LAB": "吸蟲實驗（實驗課 slides）",
        "D0907": "0907 Introduction、STHs、Toxocara、Enterobius",
        "D0914": "0914 Capillaria、Strongyloides、Foodborne nematodes", "D0922": "0922 Trichinella、Anisakis、A. cantonensis、Filaria"}
# 圖譜每頁上方 12% 是學名標題、下方 7% 是學科名稱
BOX = {"NEM": (0, 0.12, 1, 0.93), "TRE": (0, 0.12, 1, 0.93)}


def crop(pdf, page, box):
    p = fitz.open(f"{SRC}/{PDF[pdf]}")[page - 1]
    r = p.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    z = max(2.0, 2 * W / clip.width)
    return Image.open(io.BytesIO(p.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip).tobytes("png")))


def trim(im, pad=12):
    g = im.convert("L").point(lambda v: 255 if v < 245 else 0)
    bb = g.getbbox()
    return im.crop((max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))) if bb else im


def main():
    worms = json.load(open(DATA, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    keep = set()
    for w in worms:
        for i, m in enumerate(w["imgs"], 1):
            im = trim(crop(m["pdf"], m["page"], m.get("box") or BOX.get(m["pdf"], (0, 0, 1, 1)))).convert("RGB")
            if im.width > W:
                im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
            name = f"{w['id']}-{i}.webp"
            im.save(f"{OUT}/{name}", "WEBP", quality=78, method=6)
            keep.add(name)
            m.update(src=f"figures/worms/{name}", w=im.width, h=im.height, deck=DECK[m["pdf"]])
    for f in os.listdir(OUT):
        if f not in keep:
            os.remove(f"{OUT}/{f}")
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(worms, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{len(worms)} 隻蟲、{len(keep)} 張圖 → {OUT}")


if __name__ == "__main__":
    main()
