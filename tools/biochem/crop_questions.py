"""把 113 共筆考古裡「題目本身是圖」的部分裁成 webp，給 build_questions.py 的 img 欄位用。
需要 poppler 的 pdftoppm 與 Pillow。執行：python3 tools/biochem/crop_questions.py（在 repo 根目錄）
"""
import os, subprocess, tempfile
from PIL import Image, ImageChops

SRC = "slides/biochemistry/共筆考古/百十三資料/生化(二)/考古/終審版/正課/期末/Chapter 22 Biosynthesis of Amino Acids, and Related Molecules.pdf"
OUT = "subjects/biochem/figures/questions"
DPI = 250
# 題目 id: (頁, [250 dpi 下的裁切框…])；多個框（選項）排成 2 欄
CROPS = {
    "g22-01": (1, [(60, 497, 1080, 1010), (60, 1060, 1080, 1580), (60, 1625, 1080, 2140), (60, 2190, 1080, 2640)]),  # PRPP 四個結構選項
    "g22-08": (2, [(1360, 2495, 1990, 2880)]),  # FdUMP 結構
}


def trim(im, pad=24):
    bbox = ImageChops.invert(im.convert("L")).point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    return im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))


os.makedirs(OUT, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for qid, (page, boxes) in CROPS.items():
        base = os.path.join(tmp, qid)
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", "-f", str(page), "-l", str(page), SRC, base], check=True)
        pg = Image.open(base + ".png").convert("RGB")
        parts = [trim(pg.crop(b)) for b in boxes]
        if len(parts) == 1:
            im = parts[0]
        else:
            cols = 2
            cw, ch = max(p.width for p in parts), max(p.height for p in parts)
            im = Image.new("RGB", (cw * cols, ch * ((len(parts) + cols - 1) // cols)), "white")
            for i, p in enumerate(parts):
                im.paste(p, ((i % cols) * cw, (i // cols) * ch))
        im.save(os.path.join(OUT, f"{qid}.webp"), quality=88)
        print(qid, im.size)
