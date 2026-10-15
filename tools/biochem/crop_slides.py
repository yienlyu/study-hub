"""把 build_figures.py 用到、但還沒有 webp 的 Ch18 / Ch22 投影片裁出來（整頁）。
需要 pymupdf 與 Pillow。執行：python3 tools/biochem/crop_slides.py（在 repo 根目錄）
"""
import io, os
import fitz
from PIL import Image

SRC = "slides/biochemistry"
OUT = "subjects/biochem/figures/slides"
W = 1400
CROPS = {  # 檔名（= figure id 去掉 slide-）: (PDF, 頁)
    "ch18-catabolism": ("Ch23-2-18-1.pdf", 46),
    "ch18-transamination": ("Ch23-2-18-1.pdf", 48),
    "ch18-glutamine": ("Ch23-2-18-1.pdf", 57),
    "ch18-glucose-alanine": ("Ch23-2-18-1.pdf", 60),
    "ch18-gdh": ("Ch23-2-18-1.pdf", 63),
    "ch18-bicycle": ("Ch23-2-18-1.pdf", 75),
    "ch18-carbon-fates": ("Ch18-2.pdf", 30),
    "ch18-thf": ("Ch18-2.pdf", 13),
    "ch18-methyl-cycle": ("Ch18-2.pdf", 20),
    "ch18-heme-synthesis": ("Ch18-3 Ch22.pdf", 69),
    "ch18-porphyrias": ("Ch18-3 Ch22.pdf", 71),
    "ch18-heme-degradation": ("Ch18-3 Ch22.pdf", 73),
}
os.makedirs(OUT, exist_ok=True)
for name, (pdf, page) in CROPS.items():
    p = fitz.open(f"{SRC}/{pdf}")[page - 1]
    z = max(2.0, 2 * W / p.rect.width)
    im = Image.open(io.BytesIO(p.get_pixmap(matrix=fitz.Matrix(z, z)).tobytes("png"))).convert("RGB")
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=80, method=6)
print(len(CROPS), "slides")
