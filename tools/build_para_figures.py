#!/usr/bin/env python3
"""寄蟲圖片 → subjects/parasitology/figures/（slides 裁切 webp）＋ figures.json

來源（都在 slides/parasitology/）：
- 1線蟲圖檔.pdf、2吸蟲圖檔.pdf：學科圖譜，整頁就是一張「蟲卵／蟲體＋大小形狀顏色」投影片
- 吸蟲實驗.pdf：實驗課「吸蟲實驗」ppt 另存的 PDF（整頁）
- Mixed ova 圖譜.pdf：原色等比蟲卵圖譜，裁成線蟲、吸蟲兩塊
- 上課 pptx：直接取出投影片裡的 CDC 生活史圖（ppt/media）
- 上課 deck 的 PDF（PowerPoint 另存）：生活史圖多是 EMF 向量圖，取不出來，改從 PDF 整頁裁切；
  for2h-1／for2h-2 是吸蟲的舊版 .ppt，也一樣另存 PDF
手繪生活史觀念圖由 tools/build_para_cycles.py 產生，要先跑那支。
手繪 SVG 放在 subjects/parasitology/figures/<id>.svg，這裡只寫說明。
需要 pymupdf 與 Pillow。執行：python3 tools/build_para_figures.py（在 repo 根目錄）
"""
import io, json, os, re, zipfile
import fitz
from PIL import Image

SRC = "slides/parasitology"
ROOT = "subjects/parasitology"
OUT = f"{ROOT}/figures/slides"
W = 1400

NEM, TRE, MIX = "1線蟲圖檔.pdf", "2吸蟲圖檔.pdf", "Mixed ova 圖譜.pdf"
LAB = "吸蟲實驗.pdf"  # 實驗課「吸蟲實驗」.ppt 用 PowerPoint 另存的 PDF
P0907 = "20260907-北醫醫學系-M2-Introduction_  STHs_ Toxocara canis_ Enterobius vermicularis.pptx"
P0914 = "20260914-北醫醫學系-M2-Capillaria_ Strongyloides stercoralis_ Foodborne Nematodes.pptx"
P0922 = "20250922-M2-Trichinella_ Anisakis_ Angiostrongylus cantonensis_ Filaria.pptx"
D0907, D0914, D0922 = (x.replace(".pptx", ".pdf") for x in (P0907, P0914, P0922))
F1, F2 = "for2h-1.pdf", "for2h-2.pdf"  # 鄭柏青吸蟲 slides（.ppt 另存 PDF）
DECK = {D0907: "0907 Introduction、STHs、Toxocara、Enterobius", D0914: "0914 Capillaria、Strongyloides、Foodborne nematodes",
        D0922: "0922 Trichinella、Anisakis、A. cantonensis、Filaria", F1: "吸蟲 for2h-1（鄭柏青）", F2: "吸蟲 for2h-2（鄭柏青）",
        LAB: "吸蟲實驗（實驗課 slides）", NEM: "線蟲圖譜（1 線蟲圖檔）", TRE: "吸蟲圖譜（2 吸蟲圖檔）", MIX: "人體常見寄生蟲蟲卵原色等比圖譜",
        P0914: "0914 Capillaria、Strongyloides、Foodborne nematodes", P0922: "0922 Trichinella、Anisakis、A. cantonensis、Filaria"}


def save(im, name):
    im = im.convert("RGB")
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=80, method=6)
    return im.size


def pdf_crop(pdf, page, box=(0, 0, 1, 0.93)):
    """box 是頁面比例 (x0, y0, x1, y1)；預設切掉頁尾學科名稱那一條。"""
    p = fitz.open(f"{SRC}/{pdf}")[page - 1]
    r = p.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height, r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    z = max(2.0, 2 * W / clip.width)
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip)
    return Image.open(io.BytesIO(pix.tobytes("png")))


def trim(im, pad=16):
    """切掉四周的白邊"""
    g = im.convert("L").point(lambda v: 255 if v < 245 else 0)
    bb = g.getbbox()
    if not bb:
        return im
    return im.crop((max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height)))


def pptx_media(pptx, media):
    with zipfile.ZipFile(f"{SRC}/{pptx}") as z:
        return Image.open(io.BytesIO(z.read(f"ppt/media/{media}")))


def svg(id, ch, title, topics, kw, cap):
    assert os.path.exists(f"{ROOT}/figures/{id}.svg"), id
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap)


def slide(id, ch, title, topics, kw, cap, src, page, box=None, media=None):
    name = id.removeprefix("slide-")
    im = pptx_media(src, media) if media else pdf_crop(src, page, box or (0, 0, 1, 0.93))
    if src in (D0907, D0914, D0922, F1, F2):
        im = trim(im)
    w, h = save(im, name)
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap,
                type="slide", src=f"figures/slides/{name}.webp", deck=DECK[src], page=str(page), w=w, h=h)


FULL = (0, 0, 1, 1)

F = [
 # ---------------- 總論
 svg("hosts", "intro", "宿主的種類：誰身上有成蟲、誰只有幼蟲", ["宿主分類"],
     "definitive host intermediate host reservoir host paratenic host 最終宿主 中間宿主 保蟲宿主 保幼宿主",
     "<strong>最終宿主</strong>：成蟲／有性生殖；<strong>中間宿主</strong>：幼蟲／無性生殖；<strong>保蟲宿主</strong>：人以外的最終宿主；<strong>保幼宿主</strong>：幼蟲不發育、只是等著被吃。"),
 svg("lung-migration", "intro", "會經過肺的線蟲：心肺移行路線", ["生活史"],
     "Loeffler syndrome lung migration Ascaris hookworm Strongyloides filariform larva trachea 心肺移行",
     "<strong>蛔蟲、鉤蟲、糞小桿線蟲</strong>的幼蟲都走「血流 → 右心 → 肺 → 氣管 → 吞下 → 小腸」，移行時可造成 <strong>Loeffler syndrome</strong>（嗜酸性肺炎）。蟯蟲、鞭蟲不經過肺。"),
 # ---------------- 土源性蠕蟲
 slide("slide-ascaris-egg", "sth", "蛔蟲受孕卵：厚殼＋蛋白質外套膜", ["蛔蟲"],
       "Ascaris fertilized egg decorticated protein coat mammillated", "受孕卵約 60 × 45 µm、圓形厚殼、外面有凹凸的<strong>蛋白質外套膜</strong>；外套膜脫落的叫 decorticated egg。", NEM, 3),
 slide("slide-ascaris-unfert", "sth", "蛔蟲未受孕卵：長橢圓、薄殼", ["蛔蟲"],
       "Ascaris unfertilized egg elongated", "未受孕卵約 90 × 40 µm、較長、殼薄、內部是雜亂的顆粒；浮游法會沉下去。", NEM, 4),
 slide("slide-trichuris-egg", "sth", "鞭蟲卵：兩端有塞的橄欖球", ["鞭蟲"],
       "Trichuris egg barrel polar plug", "約 54 × 22 µm，桶狀、<strong>兩端各一個無色的極塞（polar plug）</strong>、殼黃褐色。", NEM, 13),
 slide("slide-hookworm-egg", "sth", "鉤蟲卵：薄殼透明、內有分裂細胞", ["鉤蟲"],
       "hookworm egg thin shell cleavage rhabditiform larva", "約 60 × 40 µm、橢圓、<strong>殼很薄且無色透明</strong>，裡面是 2–8 個分裂中的細胞。跑台寫 hookworm 即可。", NEM, 14),
 slide("slide-necator-mouth", "sth", "美洲鉤蟲口囊：一對切板", ["鉤蟲"],
       "Necator americanus cutting plates buccal capsule", "<em>Necator americanus</em> 口囊是<strong>切板（cutting plates）</strong>；十二指腸鉤蟲則是兩對牙齒。", NEM, 16),
 slide("slide-duodenale-mouth", "sth", "十二指腸鉤蟲口囊：兩對牙齒", ["鉤蟲"],
       "Ancylostoma duodenale teeth buccal capsule", "<em>Ancylostoma duodenale</em>：<strong>兩對大小相近的牙齒</strong>；雌蟲尾端有尾刺。", NEM, 19),
 svg("ascaris-cycle", "sth", "蛔蟲生活史：吃卵 → 肝 → 肺 → 吞下 → 小腸", ["蛔蟲", "生活史"],
     "Ascaris lumbricoides life cycle embryonated egg soil lung migration Loeffler intestinal obstruction",
     "卵要在<strong>土壤</strong>胚胎化 2–3 週才有感染力；吃入後幼蟲走<strong>門脈 → 肝 → 右心 → 肺</strong>，穿入肺泡後經氣管被吞下，回小腸長成成蟲。肺移行 → Loeffler；成蟲 → 腸阻塞、異位移行。"),
 slide("slide-ascaris-cycle", "sth", "蛔蟲生活史（Lancet 2018）", ["蛔蟲", "生活史"],
       "Ascaris life cycle Lancet fertilised unfertilised egg Loeffler", "左邊是診斷期（受精卵／未受精卵），右邊是臨床：肺移行造成 Loeffler syndrome、成蟲造成腸阻塞；旁邊是成蟲照片與雄蟲交尾刺。", D0907, 34, box=FULL),
 svg("trichuris-cycle", "sth", "鞭蟲生活史：直接到盲腸、不經過肺", ["鞭蟲", "生活史"],
     "Trichuris trichiura life cycle cecum no lung migration rectal prolapse",
     "吃入胚胎化卵 → 小腸孵化 → 直接到<strong>盲腸、大腸</strong>，細長前端埋進黏膜。<strong>沒有心肺移行</strong>。重度感染幼童 → 直腸脫垂。"),
 slide("slide-trichuris-cycle", "sth", "鞭蟲生活史（Lancet 2018）", ["鞭蟲", "生活史"],
       "Trichuris life cycle Lancet embryonated egg rectal prolapse", "卵在土壤胚胎化後被吃入；重度感染：痢疾、杵狀指、直腸脫垂。", D0907, 42, box=FULL),
 svg("hookworm-cycle", "sth", "鉤蟲生活史：絲狀幼蟲鑽皮膚", ["鉤蟲", "生活史"],
     "hookworm life cycle filariform larva skin penetration ground itch lung iron deficiency anemia",
     "卵 → 土壤孵出<strong>桿狀幼蟲</strong> → <strong>絲狀幼蟲 L3（感染期）</strong>鑽皮膚 → 血流 → 肺 → 吞下 → 小腸咬腸壁吸血 → <strong>缺鐵性貧血</strong>。十二指腸鉤蟲也可經口。"),
 slide("slide-hookworm-cycle", "sth", "兩種鉤蟲生活史與形態", ["鉤蟲", "生活史"],
       "Ancylostoma duodenale Necator americanus life cycle buccal capsule bursa rhabditiform filariform", "左十二指腸鉤蟲（2 對牙）、右美洲鉤蟲（切板）；中間是 L3 鑽皮膚 → 肺 → 小腸的路線。", D0907, 49, box=FULL),
 # ---------------- 蟯蟲與犬蛔蟲
 slide("slide-enterobius-adult", "enterobius-toxocara", "蟯蟲雌蟲：食道球與尖尾", ["蟯蟲"],
       "Enterobius vermicularis female esophageal bulb cephalic alae pinworm", "8–13 mm，前端有<strong>頸翼（cephalic alae）</strong>與<strong>食道球</strong>、尾巴長而尖；夜間爬到肛門周圍產卵。", NEM, 6),
 slide("slide-enterobius-egg", "enterobius-toxocara", "蟯蟲卵：一邊扁平的 D 字形", ["蟯蟲"],
       "Enterobius egg asymmetrical flattened one side L3 larva", "約 55 × 26 µm、無色透明、<strong>一側扁平一側凸（左右不對稱）</strong>，卵內常已有幼蟲。", NEM, 7),
 slide("slide-scotch-tape", "enterobius-toxocara", "肛圍擦拭法（Scotch tape test）", ["蟯蟲"],
       "Scotch tape test adhesive tape perianal swab diagnosis", "蟯蟲卵產在肛門周圍、<strong>糞便很少找到</strong>，所以要在早上起床、排便洗澡前用透明膠帶黏肛圍。", NEM, 8),
 slide("slide-toxocara-egg", "enterobius-toxocara", "犬蛔蟲卵：球形厚殼、表面有凹洞", ["犬蛔蟲"],
       "Toxocara canis egg pitted shell", "80–85 µm、球形厚殼、蛋白膜表面像高爾夫球的<strong>凹洞（pitted）</strong>。人吃到卵 → VLM／OLM，<strong>人的糞便不會出現犬蛔蟲卵</strong>。", NEM, 30),
 svg("enterobius-cycle", "enterobius-toxocara", "蟯蟲生活史：夜間肛門產卵 → 手 → 口", ["蟯蟲", "生活史"],
     "Enterobius vermicularis life cycle perianal egg laying autoinfection retroinfection Scotch tape",
     "人是唯一宿主；雌蟲<strong>夜間爬到肛門外產卵</strong>，卵 6 小時就有感染力 → 抓癢 → 手 → 口<strong>自體再感染</strong>。所以診斷用<strong>肛圍擦拭法</strong>，治療要全家一起。"),
 slide("slide-enterobius-cycle", "enterobius-toxocara", "蟯蟲生活史", ["蟯蟲", "生活史"],
       "Enterobius life cycle autoinfection perianal contaminated hands", "成蟲在盲腸 → 雌蟲爬出肛門產卵 → 汙染手、食物、衣物 → 吃入；抓癢造成自體感染。", D0907, 61, box=FULL),
 svg("toxocara-cycle", "enterobius-toxocara", "犬蛔蟲生活史：人是保幼宿主", ["犬蛔蟲", "生活史"],
     "Toxocara canis life cycle dog paratenic host VLM OLM neurotoxocariasis sandpit",
     "成蟲在<strong>狗</strong>；卵在土壤 2–5 週胚胎化。人吃入胚胎化卵或生吃雞、羊、兔肝 → 幼蟲在體內亂鑽但<strong>不會長成成蟲</strong> → VLM、OLM、NT、隱蔽型。<strong>人的糞便找不到卵</strong>。"),
 slide("slide-toxocara-cycle", "enterobius-toxocara", "人體犬蛔蟲症：幼蟲跑到哪裡", ["犬蛔蟲", "生活史"],
       "Toxocara human toxocarosis larva migration liver eye CNS VLM OLM NT", "狗吃到卵 → 成蟲在狗小腸；人吃到卵 → 幼蟲經血流到肝（VLM）、眼（OLM）、腦（NT）。", D0907, 83, box=FULL),
 # ---------------- 毛線蟲與糞小桿線蟲
 svg("strongyloides-cycle", "capillaria-strongyloides", "糞小桿線蟲：自由生活、寄生與自體感染", ["糞小桿線蟲"],
     "Strongyloides stercoralis free-living cycle autoinfection hyperinfection disseminated rhabditiform filariform larva steroid HTLV-1",
     "土壤裡可以<strong>自由生活好幾代</strong>；在人體腸道孵化的桿狀幼蟲若直接變成絲狀幼蟲 → <strong>自體感染</strong>。用類固醇或 HTLV-1 → <strong>過度感染、播散</strong>。糞便看到的是<strong>幼蟲</strong>不是卵。"),
 slide("slide-strongyloides", "capillaria-strongyloides", "糞小桿線蟲：生活史與蟲卵", ["糞小桿線蟲"],
       "Strongyloides egg parthenogenesis free living autoinfection CDC", "卵約 54 × 32 µm、薄殼，在腸黏膜就孵化，所以糞便檢查找的是桿狀幼蟲。孤雌生殖、自由生活型 vs 寄生型。", NEM, 26),
 slide("slide-cphil-cycle", "capillaria-strongyloides", "菲律賓毛線蟲生活史（CDC）", ["菲律賓毛線蟲"],
       "Capillaria philippinensis life cycle fish autoinfection", "吃生的淡水魚 → 小腸黏膜成蟲 → 產兩種卵：有殼的隨糞便排出、<strong>無殼的在腸內孵化 → 自體感染</strong>，所以蟲數越來越多、嚴重腹瀉。", P0914, 3, media="image3.jpeg"),
 slide("slide-cphil-egg", "capillaria-strongyloides", "菲律賓毛線蟲卵：花生狀、兩端淺塞", ["菲律賓毛線蟲"],
       "Capillaria philippinensis egg peanut striated shell polar prominence", "35–45 µm、<strong>花生形</strong>、殼有放射紋、兩端的極塞很淺（和鞭蟲卵的明顯極塞不同）。", NEM, 39),
 slide("slide-chep-egg", "capillaria-strongyloides", "肝毛線蟲卵：在肝組織裡找到", ["肝毛線蟲"],
       "Capillaria hepatica egg liver rat spurious infection", "50–70 µm、殼厚有放射紋、兩端淺極塞。真正感染時卵留在<strong>肝臟</strong>；糞便看到卵多半是吃了鼠肝的<strong>假感染</strong>。", NEM, 38),
 svg("capillaria-cycles", "capillaria-strongyloides", "兩種毛線蟲：腸道型 vs 肝臟型", ["菲律賓毛線蟲", "肝毛線蟲", "生活史"],
     "Capillaria philippinensis hepatica life cycle fish autoinfection rat liver spurious infection",
     "<strong>菲律賓</strong>：吃生淡水魚、無殼卵在腸內孵化 → <strong>自體感染</strong>。<strong>肝</strong>：卵留在鼠肝，要被吃掉或死亡分解才進土壤；人吃入胚胎化卵才是真感染，<strong>吃鼠肝而糞便見卵＝假感染</strong>。"),
 slide("slide-chep-cycle", "capillaria-strongyloides", "肝毛線蟲生活史（CDC）", ["肝毛線蟲", "生活史"],
       "Capillaria hepatica life cycle rat liver predation decomposition embryonated egg soil", "成蟲與卵在鼠肝；卵靠<strong>捕食</strong>或<strong>屍體分解</strong>釋出，在土壤胚胎化後才有感染力。", D0914, 6, box=(0.21, 0.43, 0.92, 0.99)),
 slide("slide-strongyloides-cycle", "capillaria-strongyloides", "糞小桿線蟲生活史（CDC）：自由生活與寄生", ["糞小桿線蟲", "生活史"],
       "Strongyloides stercoralis life cycle CDC free-living parasitic internal external autoinfection", "左邊土壤裡的自由生活世代、右邊人體的寄生世代；紅框是<strong>內／外自體感染</strong>。", D0914, 11, box=FULL),
 # ---------------- 食源性線蟲
 slide("slide-trichinella-cycle", "foodborne", "旋毛蟲生活史（CDC）", ["旋毛蟲"],
       "Trichinella spiralis life cycle domestic sylvatic pig encysted larva", "人與豬<strong>同時是最終宿主也是中間宿主</strong>：吃到肌肉裡的被囊幼蟲 → 小腸成蟲 → 胎生幼蟲經血流到<strong>橫紋肌</strong>被囊。", P0914, 28, media="image34.gif"),
 slide("slide-trichinella-larva", "foodborne", "旋毛蟲被囊幼蟲（肌肉切片）", ["旋毛蟲"],
       "Trichinella encysted larva nurse cell striated muscle biopsy", "肌肉切片可見捲曲的幼蟲包在 <strong>nurse cell</strong> 裡；確診靠<strong>肌肉切片</strong>。", NEM, 28),
 slide("slide-gnathostoma-cycle", "foodborne", "顎口線蟲生活史（CDC）", ["顎口線蟲"],
       "Gnathostoma life cycle copepod fish frog paratenic host cat dog", "劍水蚤 → 魚、蛙（第二中間宿主）→ 貓狗是最終宿主；人吃生魚或蛙是<strong>非適合宿主</strong>，幼蟲在皮下移行（移動性腫塊）。", P0914, 39, media="image50.jpeg"),
 slide("slide-anisakis", "foodborne", "海獸胃線蟲第三期幼蟲", ["海獸胃線蟲"],
       "Anisakis L3 larva marine fish squid whale", "人吃生的海魚、魷魚吃到 <strong>L3</strong>，幼蟲鑽胃壁 → 劇烈胃痛；胃鏡直接夾出。", NEM, 37),
 slide("slide-acanton-cycle", "foodborne", "廣東住血線蟲生活史（CDC）", ["廣東住血線蟲"],
       "Angiostrongylus cantonensis life cycle rat snail slug eosinophilic meningitis", "成蟲在<strong>鼠的肺動脈</strong>；中間宿主是<strong>非洲大蝸牛</strong>、蛞蝓；人吃到 L3 → 幼蟲跑到腦 → <strong>嗜酸性腦膜炎</strong>。", P0914, 70, media="image103.jpeg"),
 slide("slide-acanton-snail", "foodborne", "廣東住血線蟲的中間宿主：非洲大蝸牛", ["廣東住血線蟲"],
       "Achatina fulica African giant snail intermediate host L3", "非洲大蝸牛（<em>Achatina fulica</em>）的肺囊裡有第三期幼蟲；台灣南部、移工、原住民生食蝸牛的病例。", NEM, 36),
 slide("slide-acanton-adult", "foodborne", "廣東住血線蟲雌蟲：Barber's pole", ["廣東住血線蟲"],
       "Angiostrongylus female barber's pole uterus intestine", "雌蟲白色子宮纏繞紅色腸道，看起來像<strong>理髮廳旋轉燈（barber's pole）</strong>。", NEM, 33),
 svg("trichinella-cycle", "foodborne", "旋毛蟲生活史：同一宿主是最終也是中間宿主", ["旋毛蟲", "生活史"],
     "Trichinella spiralis life cycle encysted larva nurse cell striated muscle larviparous",
     "吃入肌肉被囊幼蟲 → 小腸成蟲 → 雌蟲<strong>直接產幼蟲</strong> → 血流到<strong>橫紋肌</strong>被囊。同一隻宿主兩種角色都扮，要被下一隻動物吃掉才能繼續。"),
 svg("gnathostoma-cycle", "foodborne", "顎口線蟲生活史：人是非適合宿主", ["顎口線蟲", "生活史"],
     "Gnathostoma life cycle copepod fish loach frog cat dog migratory swelling",
     "貓狗胃壁成蟲 → 卵入水 → <strong>劍水蚤</strong> → 魚、泥鰍、蛙、蛇（進階 L3）。人生吃 → 幼蟲不成熟、到處移行 → <strong>遊走性皮下腫脹</strong>。"),
 svg("anisakis-cycle", "foodborne", "海獸胃線蟲生活史：人是意外宿主", ["海獸胃線蟲", "生活史"],
     "Anisakis life cycle whale dolphin krill marine fish squid accidental host gastroscopy",
     "鯨、海豚胃裡的成蟲 → 卵入海 → 磷蝦 → <strong>海魚、魷魚（L3）</strong>。人生吃 → L3 鑽胃壁，約 6 小時後劇烈胃痛；<strong>胃鏡夾出</strong>。"),
 slide("slide-anisakis-cycle", "foodborne", "海獸胃線蟲生活史", ["海獸胃線蟲", "生活史"],
       "Anisakis life cycle marine mammals crustacean fish squid accidental human", "① 未胚胎化卵 → ② 胚胎化 → ③ 自由游動 L2 → ④ 甲殼類 → ⑤ 人意外吃到 L3 → ⑥ 海洋哺乳類長成成蟲。", D0922, 8, box=(0, 0.05, 1, 0.95)),
 svg("acanton-cycle", "foodborne", "廣東住血線蟲生活史：鼠、螺、保幼宿主", ["廣東住血線蟲", "生活史"],
     "Angiostrongylus cantonensis life cycle rat pulmonary artery snail slug paratenic shrimp crab frog eosinophilic meningitis",
     "鼠肺動脈成蟲 → L1 隨鼠糞 → <strong>螺、蛞蝓</strong>（L3）→ 淡水蝦、陸蟹、青蛙（保幼宿主）。人生吃 → 幼蟲到<strong>腦</strong>死在那裡 → <strong>嗜酸性腦膜炎</strong>。"),
 slide("slide-acanton-hosts", "foodborne", "廣東住血線蟲：各種宿主與人的感染途徑", ["廣東住血線蟲", "生活史"],
       "Angiostrongylus cantonensis paratenic hosts frog crab shrimp vegetables human infection", "人會從<strong>螺、保幼宿主（蝦、蟹、蛙、蜥蜴）</strong>或被汙染的蔬果感染。", D0922, 22, box=FULL),
 # ---------------- 血絲蟲
 svg("microfilariae", "filaria", "四種微絲蚴怎麼分", ["微絲蚴鑑別"],
     "microfilaria sheath tail nuclei nocturnal periodicity Wuchereria Brugia Loa Onchocerca Mansonella",
     "看三件事：<strong>有沒有鞘</strong>、<strong>尾端有沒有核</strong>、<strong>在哪裡找</strong>（血液夜間／血液白天／皮膚）。班氏：有鞘、尾無核、夜間；馬來：有鞘、尾端兩顆核；羅阿：有鞘、尾核到底、白天；蟠尾：無鞘、在皮膚。"),
 slide("slide-wb-mf", "filaria", "班氏絲蟲微絲蚴：有鞘、尾端無核", ["淋巴絲蟲"],
       "Wuchereria bancrofti microfilaria sheathed no nuclei tail Culex", "有鞘、身體柔和彎曲、<strong>尾端沒有核</strong>；病媒以<strong>家蚊（Culex）</strong>為主，夜間週期性。", NEM, 40),
 slide("slide-bm-mf", "filaria", "馬來絲蟲微絲蚴：尾端兩顆核", ["淋巴絲蟲"],
       "Brugia malayi microfilaria sheathed two terminal nuclei Mansonia", "有鞘、彎曲較僵硬、<strong>尾端有兩顆分開的核</strong>；病媒是<strong>曼蚊（Mansonia）</strong>等。", NEM, 41),
 slide("slide-onchocerca-cycle", "filaria", "蟠尾絲蟲生活史（CDC）", ["蟠尾絲蟲"],
       "Onchocerca volvulus life cycle blackfly Simulium skin nodule river blindness", "<strong>黑蠅（Simulium）</strong>在河邊繁殖；成蟲在皮下結節，微絲蚴在<strong>皮膚</strong>（皮膚切片診斷），跑進眼睛 → 河盲症。", P0922, 66, media="image124.png"),
 svg("filaria-cycle", "filaria", "血絲蟲生活史與三類比較：病媒、成蟲、微絲蚴", ["淋巴絲蟲", "羅阿絲蟲", "蟠尾絲蟲", "生活史"],
     "filaria life cycle vector L3 microfilaria mosquito Chrysops Simulium lymphatic subcutaneous skin periodicity",
     "病媒吸血注入 <strong>L3</strong> → 成蟲 → 雌蟲產<strong>微絲蚴</strong> → 病媒吸走。橫著讀三條：<strong>蚊</strong>／淋巴管／血液夜間、<strong>斑虻</strong>／皮下移行／血液白天、<strong>黑蠅</strong>／皮下結節／皮膚。"),
 slide("slide-filaria-cycle", "filaria", "蟠尾絲蟲、羅阿絲蟲、馬來絲蟲生活史對照", ["淋巴絲蟲", "羅阿絲蟲", "蟠尾絲蟲", "生活史"],
       "Onchocerca Loa loa Brugia malayi life cycle adults microfilariae mosquito Chrysops Simulium", "上半是人體內（成蟲位置、微絲蚴在皮下組織或血液日／夜），下半是病媒（蚊、斑虻、黑蠅）。", D0922, 34, box=FULL),
 slide("slide-loa-cycle", "filaria", "羅阿絲蟲生活史（CDC）", ["羅阿絲蟲", "生活史"],
       "Loa loa life cycle Chrysops deerfly subcutaneous diurnal microfilariae", "斑虻（<em>Chrysops</em>）白天吸血；成蟲在皮下組織移行，有鞘微絲蚴白天出現在周邊血液。", D0922, 54, box=(0, 0.08, 1, 1)),
 # ---------------- 吸蟲
 svg("trematode-cycle", "trematodes", "吸蟲的一般生活史與血吸蟲的例外", ["吸蟲總論"],
     "trematode life cycle miracidium sporocyst redia cercaria metacercaria snail schistosome exception",
     "卵 → <strong>纖毛幼蟲</strong>（水中）→ 螺內 <strong>胞狀幼蟲 → 雷氏幼蟲 → 尾動幼蟲</strong> → 第二中間宿主或水生植物上的<strong>囊狀幼蟲</strong> → 人吃進去。<strong>血吸蟲</strong>例外：沒有雷氏幼蟲、沒有囊狀幼蟲，尾動幼蟲直接鑽皮膚。"),
 svg("schisto-eggs", "trematodes", "三種血吸蟲蟲卵：看刺的位置", ["血吸蟲"],
     "Schistosoma japonicum mansoni haematobium egg spine lateral terminal urine feces",
     "<strong>日本</strong>：小、圓、側邊小刺（常看不到）、糞便；<strong>曼氏</strong>：大側刺、糞便；<strong>埃及</strong>：尾端刺、<strong>尿液</strong>。三種都沒有卵蓋。"),
 slide("slide-trematode-ova", "trematodes", "吸蟲蟲卵原色等比圖譜", ["吸蟲總論"],
       "trematode eggs to scale Clonorchis Fasciola Paragonimus Schistosoma operculum",
       "同一比例尺比大小：最大的是<strong>牛羊肝吸蟲、薑片蟲</strong>（約 140 µm），最小的是<strong>中華肝吸蟲、橫川吸蟲</strong>（約 30 µm）。除了血吸蟲（10–12），都有卵蓋。", MIX, 1, box=(0.05, 0.255, 0.96, 0.62)),
 slide("slide-fbuski-egg", "trematodes", "布氏薑片蟲卵：大而薄殼、卵蓋不明顯", ["腸吸蟲"],
       "Fasciolopsis buski egg large operculum", "約 140 × 80 µm、淡黃色、卵蓋小而不明顯；和牛羊肝吸蟲卵幾乎分不出來。", TRE, 4),
 slide("slide-pw-egg", "trematodes", "衛氏肺吸蟲卵：卵蓋有肩、後端增厚", ["肺吸蟲"],
       "Paragonimus westermani egg operculum shoulder thickened abopercular sputum", "約 85 × 53 µm、金黃褐色、卵蓋扁平有肩、<strong>後端殼增厚</strong>、左右不太對稱；在<strong>痰</strong>或糞便找。", TRE, 16),
 slide("slide-pw-crab", "trematodes", "衛氏肺吸蟲第二中間宿主：澤蟹", ["肺吸蟲"],
       "Paragonimus second intermediate host crab Potamon metacercaria", "第一中間宿主川蜷、第二中間宿主<strong>淡水蟹（澤蟹）</strong>；吃醉蟹、生蟹感染。", TRE, 19),
 slide("slide-cs-egg", "trematodes", "中華肝吸蟲卵：小、卵蓋有肩、後端小突起", ["肝吸蟲"],
       "Clonorchis sinensis egg small operculum shoulder knob", "約 30 × 16 µm（吸蟲卵最小之一）、黃褐色、<strong>卵蓋坐在肩上</strong>、後端常有小突起，內含成熟纖毛幼蟲。", TRE, 23),
 slide("slide-schisto-pair", "trematodes", "血吸蟲雌雄異體：雌蟲住在雄蟲抱雌溝", ["血吸蟲"],
       "Schistosoma gynecophoral canal male female dioecious", "吸蟲裡唯一<strong>雌雄異體</strong>的；雌蟲細長，躺在雄蟲腹面的<strong>抱雌溝</strong>裡。", TRE, 47),
 slide("slide-sj-egg", "trematodes", "日本血吸蟲卵：圓、側邊小刺", ["血吸蟲"],
       "Schistosoma japonicum egg minute lateral spine", "約 90 × 70 µm、卵圓形、<strong>側邊小刺常被雜質蓋住看不到</strong>；糞便檢查。中間宿主釘螺（Oncomelania）。", TRE, 39),
 slide("slide-sh-egg", "trematodes", "埃及血吸蟲卵：尾端刺、在尿液", ["血吸蟲"],
       "Schistosoma haematobium egg terminal spine urine bladder Bulinus", "約 143 × 60 µm、<strong>尾端刺</strong>、在<strong>尿液</strong>找到（成蟲在膀胱靜脈叢）。中間宿主 Bulinus。", TRE, 43),
 slide("slide-sm-egg", "trematodes", "曼氏血吸蟲卵：大側刺", ["血吸蟲"],
       "Schistosoma mansoni egg large lateral spine Biomphalaria", "約 140 × 60 µm、<strong>靠近後端的大側刺</strong>；糞便檢查。中間宿主 Biomphalaria。", TRE, 48),
 slide("slide-trematode-stages", "trematodes", "吸蟲各期幼蟲：卵 → 纖毛 → 胞狀 → 雷氏 → 尾動 → 囊狀", ["吸蟲總論", "生活史"],
       "trematode stages egg miracidium sporocyst redia cercaria metacercaria adult", "順時針：卵、纖毛幼蟲、胞狀幼蟲、雷氏幼蟲、尾動幼蟲、（囊狀幼蟲）、成蟲。", F1, 12, box=FULL),
 svg("intestinal-flukes", "trematodes", "腸吸蟲：第一中間宿主 → 吃什麼得病 → 寄生部位", ["腸吸蟲", "生活史"],
     "intestinal flukes Fasciolopsis Metagonimus Heterophyes Echinostoma Gastrodiscoides Eurytrema snail water plant fish grasshopper",
     "<strong>薑片蟲</strong>、<strong>人雙口吸蟲</strong>：水生植物；<strong>異形、橫川</strong>：淡水魚；<strong>棘口</strong>：不挑；<strong>胰臟吸蟲</strong>：陸螺＋蝗蟲。只有人雙口吸蟲在大腸。"),
 slide("slide-fbuski-cycle", "trematodes", "布氏薑片蟲生活史（CDC）", ["腸吸蟲", "生活史"],
       "Fasciolopsis buski life cycle snail water plant metacercaria pig", "螺內 胞狀 → 雷氏 → 尾動；囊狀幼蟲附在<strong>水生植物</strong>上，人或<strong>豬</strong>吃入。", F1, 53, box=FULL),
 slide("slide-heterophyid-cycle", "trematodes", "異形吸蟲科生活史（CDC）", ["腸吸蟲", "生活史"],
       "Heterophyes Metagonimus life cycle snail freshwater fish metacercaria", "螺吃卵 → 尾動幼蟲鑽進<strong>淡水魚</strong>形成囊狀幼蟲；人、貓狗、食魚鳥類都可感染。", F1, 69, box=FULL),
 slide("slide-echinostoma-cycle", "trematodes", "棘口吸蟲生活史（CDC）", ["腸吸蟲", "生活史"],
       "Echinostoma life cycle snail second intermediate host aquatic birds", "第二中間宿主很多種（螺、蛙、魚）；終宿主多是水鳥。", F1, 94, box=FULL),
 slide("slide-gastrodiscoides-cycle", "trematodes", "人雙口吸蟲生活史", ["腸吸蟲", "生活史"],
       "Gastrodiscoides hominis life cycle pig deer water plants caecum", "保蟲宿主<strong>豬、鹿</strong>；吃水生植物上的囊狀幼蟲，成蟲附在<strong>盲腸、升結腸</strong>。", F1, 104, box=FULL),
 slide("slide-eurytrema-cycle", "trematodes", "胰臟吸蟲生活史", ["腸吸蟲", "生活史"],
       "Eurytrema pancreaticum life cycle snail grasshopper cattle sheep", "陸螺吃卵 → 尾動幼蟲附在草上 → <strong>蝗蟲</strong>吃進去 → 牛羊吃蝗蟲。", F1, 113, box=FULL),
 svg("paragonimus-cycle", "trematodes", "衛氏肺吸蟲生活史：腹腔 → 橫膈 → 肺", ["肺吸蟲", "生活史"],
     "Paragonimus westermani life cycle crab crayfish Semisulcospira peritoneal cavity diaphragm lung sputum brain",
     "吃生的<strong>淡水蟹、蝦</strong> → 小腸脫囊 → <strong>穿腸壁、腹腔、橫膈</strong>（不是經血流）→ 肺。卵隨<strong>痰</strong>或糞便 → 川蜷 → 蟹蝦。異位到<strong>腦</strong>最嚴重。"),
 slide("slide-pw-cycle", "trematodes", "衛氏肺吸蟲生活史（CDC）", ["肺吸蟲", "生活史"],
       "Paragonimus life cycle CDC crustacean metacercariae lung sputum", "成蟲在肺部囊腔，卵隨痰排出或吞下隨糞便；尾動幼蟲侵入甲殼類形成囊狀幼蟲。", F1, 141, box=FULL),
 svg("clonorchis-cycle", "trematodes", "中華肝吸蟲生活史：螺吃卵、魚帶囊蚴", ["肝吸蟲", "生活史"],
     "Clonorchis sinensis life cycle Parafossarulus snail cyprinid fish bile duct cholangiocarcinoma",
     "卵要被<strong>滿州泥螺</strong>吃進去才孵化；尾動幼蟲鑽進<strong>鯉科淡水魚</strong>。人吃生魚 → 十二指腸脫囊 → 沿總膽管上行到<strong>肝內膽管</strong> → 膽管癌。"),
 slide("slide-cs-cycle", "trematodes", "中華肝吸蟲生活史（CDC）", ["肝吸蟲", "生活史"],
       "Clonorchis sinensis life cycle CDC snail fish biliary duct", "螺吃卵 → 2a–2d 纖毛 → 胞狀 → 雷氏 → 尾動 → 魚 → 人；成蟲在膽管。", F2, 25, box=FULL),
 svg("fasciola-cycle", "trematodes", "牛羊肝吸蟲生活史：穿肝被膜進膽管", ["肝吸蟲", "生活史"],
     "Fasciola hepatica life cycle Lymnaea water plant watercress liver capsule bile duct Halzoun triclabendazole",
     "吃<strong>水生植物</strong>上的囊蚴（第二中間宿主非必要）→ 脫囊 → 穿腸壁 → 腹腔 → <strong>穿肝被膜、在肝實質移行</strong> → 膽管。PZQ 效果差 → Triclabendazole。"),
 slide("slide-fasciola-cycle", "trematodes", "牛羊肝吸蟲生活史（CDC）", ["肝吸蟲", "生活史"],
       "Fasciola hepatica life cycle CDC snail water plant sheep cattle hepatic biliary ducts", "椎實螺 → 尾動幼蟲在水生植物結囊 → 人、牛、羊吃入；成蟲在肝膽管。", F2, 85, box=FULL),
 svg("terrestrial-flukes", "trematodes", "陸生吸蟲：槍狀肝吸蟲吃螞蟻、胰臟吸蟲吃蝗蟲", ["肝吸蟲", "腸吸蟲", "生活史"],
     "Dicrocoelium dendriticum Eurytrema land snail ant grasshopper slime ball spurious infection",
     "兩個都是<strong>陸螺＋昆蟲</strong>。槍狀肝吸蟲：尾蚴包在黏液球裡排出 → <strong>螞蟻</strong>；吃到病肝而糞便見卵是<strong>假感染</strong>。胰臟吸蟲：<strong>蝗蟲</strong>，成蟲在胰管。"),
 slide("slide-dicrocoelium-cycle", "trematodes", "槍狀肝吸蟲生活史（CDC）", ["肝吸蟲", "生活史"],
       "Dicrocoelium dendriticum life cycle CDC land snail slime ball ant cattle", "陸螺吃卵 → 尾動幼蟲在黏液球中排出 → 螞蟻 → 牛羊吃到螞蟻。", F2, 74, box=FULL),
 svg("schisto-cycle", "trematodes", "血吸蟲生活史：例外最多的吸蟲", ["血吸蟲", "生活史"],
     "Schistosoma life cycle cercaria skin penetration schistosomulum portal vein venous plexus egg granuloma snail no redia no metacercaria",
     "只有<strong>一個中間宿主</strong>、沒有雷氏與囊狀幼蟲、尾動幼蟲<strong>直接鑽皮膚</strong>、雌雄異體、卵沒有卵蓋、<strong>卵造成肉芽腫</strong>。下排三種靠螺、卵刺、檢體分。"),
 slide("slide-schisto-cycle", "trematodes", "血吸蟲生活史（CDC）", ["血吸蟲", "生活史"],
       "Schistosoma life cycle CDC cercariae penetrate skin portal mesenteric venules bladder", "尾蚴鑽皮膚 → 童蟲 → 門脈成熟 → A 曼森、B 日本到腸繫膜靜脈，C 埃及到膀胱靜脈叢。", F2, 128, box=FULL),
 # ---------------- 吸蟲實驗（實驗課 slides，整頁）
 slide("slide-lab-fbuski-adult", "trematodes", "薑片蟲成蟲：樹枝狀睪丸前後排", ["腸吸蟲"],
       "Fasciolopsis buski adult acetabulum testes dendritic uterus vitellaria", "人體最大的吸蟲；腹吸盤（acetabulum）大、緊靠口吸盤；<strong>兩個樹枝狀睪丸前後排</strong>佔後半段，卵黃腺在兩側。", LAB, 3, box=FULL),
 slide("slide-lab-metagonimus", "trematodes", "橫川異形吸蟲：腹吸盤偏右、無生殖吸盤", ["腸吸蟲"],
       "Metagonimus yokogawai adult ventral sucker right no genital sucker testes 45 degree", "<strong>沒有生殖吸盤</strong>；腹吸盤在<strong>中線右側</strong>；兩個睪丸在蟲體後端呈 45° 弧線；卵黃腺在後 1/3 兩側。", LAB, 8, box=FULL),
 slide("slide-lab-heterophyes", "trematodes", "異形異形吸蟲：多一個生殖吸盤", ["腸吸蟲"],
       "Heterophyes heterophyes adult genital sucker gonotyl testes", "腹吸盤下側有一個<strong>大型生殖吸盤</strong>（共三個吸盤）；一對對稱並立的睪丸在蟲體後半。", LAB, 9, box=FULL),
 slide("slide-lab-heterophyid-eggs", "trematodes", "異形 vs 橫川蟲卵", ["腸吸蟲"],
       "Heterophyes Metagonimus egg comparison miracidium shoulder", "異形 23–30 × 14–17 µm、無肩峰、卵蓋對側殼厚有小棘、<strong>纖毛幼蟲明顯</strong>；橫川 28–32 × 14–18 µm、殼厚不光滑、纖毛幼蟲不明顯。", LAB, 10, box=FULL),
 slide("slide-lab-echinostoma", "trematodes", "伊羅棘口吸蟲成蟲", ["腸吸蟲"],
       "Echinostoma ilocanum adult testes tandem collar spines", "細長、頭端有棘；<strong>兩個圓形睪丸前後排</strong>在後半段，子宮充滿蟲卵。", LAB, 13, box=FULL),
 slide("slide-lab-echinostoma-egg", "trematodes", "棘口吸蟲卵：像薑片蟲卵、常未成熟", ["腸吸蟲"],
       "Echinostoma egg immature operculum", "81–154 × 53–95 µm、淡黃色、殼薄、卵蓋對側略增厚；排出時<strong>常未成熟</strong>（一個卵細胞＋許多卵黃細胞），形態接近薑片蟲卵。", LAB, 14, box=FULL),
 slide("slide-lab-gastrodiscoides", "trematodes", "人雙口吸蟲：角錐形、後端大吸盤", ["腸吸蟲"],
       "Gastrodiscoides hominis adult pyramidal acetabulum", "紅棕色、表皮光滑、<strong>角錐形</strong>，5–7 × 3–4 mm；後端寬大處有大型腹吸盤（acetabulum）；睪丸大、分葉、前後排；寄生<strong>大腸</strong>。", LAB, 16, box=FULL),
 slide("slide-lab-gh-fb-eggs", "trematodes", "人雙口吸蟲卵 vs 薑片蟲卵", ["腸吸蟲"],
       "Gastrodiscoides hominis egg Fasciolopsis buski egg comparison", "兩者都是淡黃、大型、薄殼有卵蓋；人雙口吸蟲卵較偏稜角、內容物較稀疏。", LAB, 17, box=FULL),
 slide("slide-lab-eurytrema", "trematodes", "胰臟吸蟲成蟲：睪丸在卵巢前", ["腸吸蟲"],
       "Eurytrema pancreaticum adult testes anterior to ovary pancreatic duct", "陸生吸蟲、寄生胰管；體中央兩個圓形睪丸、<strong>睪丸在卵巢之前</strong>，子宮佔滿後半。", LAB, 19, box=FULL),
 slide("slide-lab-eurytrema-egg", "trematodes", "胰臟吸蟲卵：殼厚色深", ["腸吸蟲"],
       "Eurytrema egg thick shell dark", "43–68 × 27–35 µm；陸生吸蟲卵<strong>殼厚、顏色深</strong>（抗乾燥）。", LAB, 20, box=FULL),
 slide("slide-lab-pw-adult", "trematodes", "衛氏肺吸蟲成蟲：咖啡豆、睪丸並列", ["肺吸蟲"],
       "Paragonimus westermani adult coffee bean ovary testes side by side", "卵圓、像<strong>咖啡豆</strong>；口吸盤與腹吸盤約等大；卵巢與子宮在腹吸盤後、<strong>兩個分葉睪丸左右並列在後 1/3</strong>。", LAB, 23, box=FULL),
 slide("slide-lab-opisthorchiid", "trematodes", "中華肝吸蟲、泰國肝吸蟲、貓肝吸蟲成蟲", ["肝吸蟲"],
       "Clonorchis sinensis Opisthorchis viverrini felineus adult testes", "三種後睪科肝吸蟲看<strong>睪丸</strong>：中華＝珊瑚狀（深分支）；泰國＝小花狀、深裂；貓＝大花狀、淺裂。", LAB, 29, box=FULL),
 slide("slide-lab-dicrocoelium", "trematodes", "槍狀肝吸蟲成蟲：睪丸在卵巢前", ["肝吸蟲"],
       "Dicrocoelium dendriticum adult lancet testes anterior ovary", "細長如<strong>槍頭（lancet）</strong>；兩個睪丸在腹吸盤後方、<strong>卵巢在睪丸之後</strong>；子宮佔滿後半。", LAB, 33, box=FULL),
 slide("slide-lab-dicrocoelium-egg", "trematodes", "槍狀肝吸蟲卵：不對稱、殼厚、含纖毛幼蟲", ["肝吸蟲"],
       "Dicrocoelium dendriticum egg asymmetric thick shell miracidium", "38–45 × 22–30 µm、黃褐至深黃褐色、<strong>不對稱</strong>、卵蓋傾斜、殼厚、<strong>內含纖毛幼蟲</strong>。", LAB, 34, box=FULL),
 slide("slide-lab-fasciola-adult", "trematodes", "牛羊肝吸蟲成蟲：頭錐、樹枝狀腸支", ["肝吸蟲"],
       "Fasciola hepatica adult cephalic cone branched ceca testes", "葉片狀、<strong>前端有頭錐（cephalic cone）</strong>；腸支與睪丸都是<strong>樹枝狀分支</strong>，佔滿蟲體。", LAB, 36, box=FULL),
 slide("slide-lab-fb-fh-eggs", "trematodes", "薑片蟲卵 vs 牛羊肝吸蟲卵", ["腸吸蟲", "肝吸蟲"],
       "Fasciolopsis buski egg Fasciola hepatica egg comparison", "兩者都約 130–150 µm、淡黃、卵蓋不明顯，<strong>幾乎無法區分</strong> → 要靠飲食史、旅遊史判斷。", LAB, 37, box=FULL),
 slide("slide-lab-cercaria", "trematodes", "血吸蟲尾動幼蟲：尾巴分叉", ["血吸蟲"],
       "Schistosoma cercaria forked tail", "尾巴末端<strong>分叉</strong> → 一定是血吸蟲尾蚴（直接鑽皮膚）；肺吸蟲尾蚴尾巴短小。", LAB, 41, box=FULL),
 slide("slide-lab-schisto-table", "trematodes", "三種血吸蟲成蟲型態比較表", ["血吸蟲"],
       "Schistosoma haematobium mansoni japonicum adult comparison tubercles testes ovary eggs per day lifespan", "紅箭頭是重點列：<strong>表皮結節、腸道聯合處、睪丸數目、卵巢位置、蟲卵形狀、每日產卵量</strong>。", LAB, 42, box=FULL),
 slide("slide-lab-schisto-testes", "trematodes", "血吸蟲雄蟲睪丸數目", ["血吸蟲"],
       "Schistosoma male testes number japonicum mansoni haematobium", "日本 6–7（平均 7，排成一列）、埃及 4–6、曼森 6–9（散佈）。", LAB, 43, box=FULL),
 slide("slide-lab-schisto-ovary", "trematodes", "血吸蟲雌蟲卵巢位置", ["血吸蟲"],
       "Schistosoma female ovary position", "日本＝<strong>體中部</strong>、埃及＝<strong>中線之後</strong>、曼森＝<strong>中線之前</strong>。", LAB, 44, box=FULL),
 slide("slide-lab-sm-tubercles", "trematodes", "曼森血吸蟲：體表結節明顯", ["血吸蟲"],
       "Schistosoma mansoni tegument tubercles prominent", "雄蟲體表<strong>結節明顯</strong>（電顯下更清楚）。", LAB, 45, box=FULL),
 slide("slide-lab-sh-tubercles", "trematodes", "埃及血吸蟲：體表結節細小", ["血吸蟲"],
       "Schistosoma haematobium tegument fine tubercles", "體表結節<strong>細小</strong>。", LAB, 46, box=FULL),
 slide("slide-lab-sj-smooth", "trematodes", "日本血吸蟲：體表平滑", ["血吸蟲"],
       "Schistosoma japonicum smooth tegument", "體表<strong>平滑、沒有結節</strong>。", LAB, 47, box=FULL),
 slide("slide-lab-schisto-snails", "trematodes", "三種血吸蟲的中間宿主螺", ["血吸蟲"],
       "Oncomelania hupensis Biomphalaria Bulinus snail intermediate host", "日本＝<strong>湖北釘螺 Oncomelania</strong>（尖塔形）、曼森＝<strong>雙臍扁螺 Biomphalaria</strong>（扁盤形）、埃及＝<strong>小泡螺 Bulinus</strong>。", LAB, 51, box=FULL),
 # ---------------- 實驗
 svg("egg-sizes", "nematode-lab", "常考蟲卵的相對大小（等比例示意）", ["蟲卵鑑別"],
     "egg size comparison Ascaris hookworm Trichuris Enterobius Capillaria Clonorchis Fasciola Paragonimus Schistosoma",
     "以<strong>受孕蛔蟲卵（60 µm）</strong>當比例尺：比它大兩倍以上的是牛羊肝吸蟲、薑片蟲、曼氏／埃及血吸蟲；只有一半的是中華肝吸蟲、橫川吸蟲。"),
 slide("slide-nematode-ova", "nematode-lab", "線蟲蟲卵原色等比圖譜", ["蟲卵鑑別"],
       "nematode eggs to scale Ascaris Trichuris Enterobius Toxocara hookworm Capillaria Strongyloides",
       "1 蛔蟲受孕卵、2 未受孕卵、3 蟯蟲、4 犬蛔蟲、5 鞭蟲、6 鉤蟲、7 肝毛線蟲、8 菲律賓毛線蟲、9 糞小桿線蟲。同一比例尺，比大小、顏色、殼的厚薄。", MIX, 1, box=(0.05, 0.043, 0.96, 0.258)),
]

json.dump(F, open(f"{ROOT}/figures.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(f"{ROOT}/figures.json", "a").write("\n")
print(len(F), "figures,", sum(1 for f in F if f.get("type") == "slide"), "slide crops")
