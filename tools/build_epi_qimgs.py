#!/usr/bin/env python3
"""流病題目附圖：從考古 PDF 裁切題目需要的原圖 → subjects/epidemiology/figures/questions/<id>.webp

題目在 build_epi_kaogu.py／build_epi_k1151.py 用 q["img"] 引用這些圖。
座標是 PDF point（左上原點），由 page.get_image_info() 的 bbox 外擴少許取得。
執行：python3 tools/rebuild.py tools/build_epi_qimgs.py（在 repo 根目錄）
"""
import io, os
import fitz
from PIL import Image

B = "slides/epidemiology/共筆考古/"
K113 = B + "3. 百十三資料/考古/期中/pdf/"
OUT = "subjects/epidemiology/figures/questions/"
SRC = {
    "114": K113 + "114 流病期中考古.pdf",
    "110": K113 + "110期中考古.pdf",
    "109": K113 + "109期中考古.pdf",
    "B1": B + "合併檔/流病考古Book1.pdf",
}
# id: (來源, 頁 index, clip rect)
CROPS = {
    "k114-06": ("114", 1, (65, 430, 508, 648)),       # Béjot CVE 人數長條圖
    "k114-43": ("114", 9, (196, 650, 423, 812)),      # 300 人追蹤 8 年存活曲線
    "k110-II-3": ("110", 2, (70, 169, 530, 396)),     # 四張流行曲線 Fig A–D
    "k110-II-16": ("110", 5, (40, 449, 363, 552)),    # 打靶圖 A–D
    "k110-III-8": ("110", 7, (40, 206, 308, 392)),    # 300 人追蹤 2 年存活曲線（原圖模糊）
    "k109-03": ("109", 0, (40, 285, 542, 524)),       # 四張流行曲線 A–D
    "k109-08": ("109", 1, (40, 335, 460, 578)),       # 打靶圖 A–D
    "k1151-04-c7": ("B1", 23, (160, 467, 431, 641)),  # 美國 2009 百日咳年齡分布
    "k1151-04-c8": ("B1", 25, (163, 222, 433, 405)),  # 2015 登革熱流行曲線
}
MAX_W = 1200

os.makedirs(OUT, exist_ok=True)
docs = {}
for qid, (src, page, rect) in CROPS.items():
    d = docs.setdefault(src, fitz.open(SRC[src]))
    pix = d[page].get_pixmap(dpi=220, clip=fitz.Rect(*rect))
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(OUT + qid + ".webp", "WEBP", quality=82, method=6)
    print(OUT + qid + ".webp", im.size)
