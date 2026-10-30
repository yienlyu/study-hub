"""把 114 生化實驗考古裡「題目要看圖」的部分裁成 webp，給 build_k1141.py 的 img 欄位用。
需要 poppler 的 pdftoppm 與 Pillow。執行：python3 tools/biochem_lab/crop_questions.py（在 repo 根目錄）
"""
import os, subprocess, tempfile
from PIL import Image, ImageChops

K = "slides/biochemistry/共筆考古/百十三資料/生化(二)/考古/終審版/實驗/"
CHEN = K + "1141生化實考古 陳顧中老師.pdf"
CHENG = K + "114生化實考古 鄭嘉雄老師部分-1.pdf"
CHOU = K + "1141生化實考古 周志銘老師.pdf"
OUT = "subjects/biochem-lab/figures/questions"
DPI = 250
S = DPI / 60  # 裁切框用 60 dpi 預覽圖量的座標
# 題目 id: (pdf, 頁, 60 dpi 下的裁切框)
CROPS = {
    "chen-01": (CHEN, 1, (405, 140, 455, 235)),  # P-100 刻度 0-6-3
    "chen-03": (CHEN, 1, (300, 262, 448, 378)),  # gel filtration 層析圖
    "chen-04": (CHEN, 1, (128, 592, 452, 675)),  # Sepharose 2B/4B/6B 表
    "chen-05": (CHEN, 2, (168, 38, 432, 138)),  # ascorbic acid → dehydroascorbic acid
    "chen-31": (CHEN, 6, (238, 398, 448, 602)),  # CBB 結構
    "cheng-17": (CHENG, 3, (262, 512, 452, 692)),  # polyacrylamide matrix
    "cheng-19": (CHENG, 4, (243, 32, 448, 272)),  # Rf 示意
    "chou-16": (CHOU, 3, (148, 262, 338, 482)),  # pTMU 電泳結果
}


def trim(im, pad=20):
    bbox = ImageChops.invert(im.convert("L")).point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    return im.crop((max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height)))


os.makedirs(OUT, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for qid, (pdf, page, box) in CROPS.items():
        base = os.path.join(tmp, qid)
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile", "-f", str(page), "-l", str(page), pdf, base], check=True)
        pg = Image.open(base + ".png").convert("RGB")
        im = trim(pg.crop(tuple(round(v * S) for v in box)))
        im.save(os.path.join(OUT, f"{qid}.webp"), quality=88)
        print(qid, im.size)
