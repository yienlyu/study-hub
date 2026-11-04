#!/usr/bin/env python3
"""微免 113 考古：把轉文字時掉的圖從原始 PDF 裁出來 → subjects/micro-immuno/figures/questions/

kaogu113.txt 是純文字，轉檔時圖都掉了；這支依 PDF 座標裁切（連紅框、箭頭標註一起）。
  *-ex.webp：詳解附圖 → 題目的 explainImg（只在詳解區顯示，不會在作答前洩漏答案）
  其他：題目附圖 → 題目的 img（看圖作答題，補圖後取消 imageOnly）
兩個欄位都寫在 tools/question_fixes.json。
需要 pymupdf 與 Pillow。執行：python3 tools/build_micro_explain_imgs.py（在 repo 根目錄）
"""
import io, os
import fitz
from PIL import Image

K = "slides/micro-immuno/共筆考古/考古/組長上傳區/微免考古"
W1, W2, W3, W4, W4B, W6, W8 = (f"{K}{w}.pdf" for w in ("W1", "W2", "W3解", "W4（上）", "W4（下）", "W6", "W8"))
OUT = "subjects/micro-immuno/figures/questions"
MAXW = 1400

# 檔名: (pdf, 頁碼, (x0, y0, x1, y1) PDF 座標)
CROPS = {
    # ---- 題目附圖（img）
    "k113-bact-05": (W1, 1, (440, 738, 548, 816)),     # 生長曲線 A–D
    "k113-fungi-03": (W8, 1, (394, 347, 559, 460)),
    "k113-fungi-06": (W8, 1, (336, 684, 543, 812)),
    "k113-fungi-08": (W8, 2, (374, 138, 554, 250)),
    "k113-fungi-09": (W8, 2, (370, 277, 555, 390)),
    "k113-fungi-10": (W8, 2, (449, 417, 553, 532)),
    "k113-fungi-18": (W8, 3, (240, 470, 364, 544)),    # 含紅色箭頭
    "k113-fungi-20": (W8, 3, (292, 653, 538, 766)),
    "k113-fungi-28": (W8, 4, (30, 640, 560, 816)),     # 選項 A–E 都是圖
    "k113-fungi-31": (W8, 5, (30, 233, 560, 396)),     # 選項 A–E 都是圖
    # ---- 詳解附圖（explainImg）
    "k113-innate-01-ex": (W2, 14, (136, 35, 495, 296)),   # 補體三條路徑 → MAC
    "k113-innate-03-ex": (W2, 14, (365, 384, 562, 583)),  # TLR-4 / CD14 / LPS-BP
    "k113-innate-04-ex": (W2, 15, (92, 35, 506, 190)),    # NK 抑制／活化受體（39 題也引用）
    "k113-innate-05-ex": (W2, 15, (113, 244, 458, 472)),  # cell migration 三步驟
    "k113-innate-06-ex": (W2, 15, (352, 594, 532, 788)),  # 補體三功能
    "k113-innate-08-ex": (W2, 16, (260, 101, 555, 268)),  # MBL / ficolin
    "k113-innate-22-ex": (W2, 18, (71, 424, 529, 720)),   # TLR 總表（38 題也引用）
    "k113-innate-34-ex": (W2, 21, (201, 154, 404, 290)),  # cell migration
    "k113-innate-40-ex": (W2, 22, (50, 84, 558, 222)),    # ILC 分類
    "k113-innate-54-ex": (W2, 24, (159, 35, 445, 221)),   # chemokine receptor
    "k113-innate-55-ex": (W2, 24, (98, 306, 502, 432)),   # opsonization → CR
    "k113-agab-01-ex": (W3, 1, (195, 435, 404, 618)),     # 抗體構造
    "k113-agab-06-ex": (W3, 2, (82, 579, 517, 647)),      # class / subclass 表
    "k113-tdev-01-ex": (W4, 4, (170, 322, 444, 486)),     # affinity model
    "k113-tdev-04-ex": (W4, 5, (36, 109, 559, 403)),   # MHC I 抗原處理路徑（13 題也引用）
    "k113-tdev-05-ex": (W4, 5, (166, 573, 429, 745)),  # 胸腺 positive / negative selection
    "k113-tdev-06-ex": (W4, 6, (64, 99, 558, 269)),    # 左：MHC 等位基因數；右：病原位置 → MHC 路徑
    "k113-tdev-07-ex": (W4, 6, (64, 358, 329, 528)),   # Ig vs TCR 多樣性
    "k113-tdev-12-ex": (W4, 7, (464, 322, 563, 518)),  # 各細胞 MHC I / II 表現量
    "k113-tdev-14-ex": (W4, 7, (49, 611, 535, 777)),   # TCR α/β/γ/δ 基因座
    "k113-tact-03-ex": (W4B, 7, (148, 530, 455, 672)),    # IL-12 → TH1
    "k113-tact-10-ex": (W4B, 8, (184, 415, 426, 572)),    # chemokine receptor 七次穿膜
    "k113-tact-40-ex": (W4B, 11, (206, 570, 397, 739)),   # cytokine → isotype
    "k113-tact-41-ex": (W4B, 12, (150, 80, 454, 298)),    # effector T 分化 cytokine
    "k113-tact-41-ex-b": (W4B, 12, (61, 392, 556, 562)),  # IL-17 作用（含左圖圖說）
    "k113-bacillus-07-ex": (W6, 14, (379, 33, 562, 192)), # Tox 噬菌體與白喉毒素
    "k113-fungi-06-ex": (W8, 11, (383, 241, 569, 326)),   # Trichophyton / Microsporum / Epidermophyton
    "k113-fungi-08-ex": (W8, 11, (394, 458, 550, 593)),   # 厚膜孢子（10、17 題也引用）
    "k113-fungi-08-ex-b": (W8, 11, (36, 604, 553, 739)),  # 其他四種孢子
    "k113-fungi-55-ex": (W8, 19, (442, 92, 557, 172)),    # Amphotericin B 與 ergosterol
}

os.makedirs(OUT, exist_ok=True)
docs = {}
for name, (pdf, page, box) in CROPS.items():
    d = docs.setdefault(pdf, fitz.open(pdf))
    clip = fitz.Rect(*box) + (-1, -1, 1, 1)
    z = min(4.0, max(2.0, MAXW / clip.width))
    im = Image.open(io.BytesIO(d[page - 1].get_pixmap(matrix=fitz.Matrix(z, z), clip=clip).tobytes("png"))).convert("RGB")
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=82, method=6)
    print(name, im.size)
