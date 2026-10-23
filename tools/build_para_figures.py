#!/usr/bin/env python3
"""寄蟲圖片 → subjects/parasitology/figures/（slides 裁切 webp）＋ figures.json

來源（都在 slides/parasitology/）：
- 1線蟲圖檔.pdf、2吸蟲圖檔.pdf：學科圖譜，整頁就是一張「蟲卵／蟲體＋大小形狀顏色」投影片
- 吸蟲實驗.pdf：實驗課「吸蟲實驗」ppt 另存的 PDF（整頁）
- Mixed ova 圖譜.pdf：原色等比蟲卵圖譜，裁成線蟲、吸蟲兩塊
- 上課 pptx：直接取出投影片裡的 CDC 生活史圖（ppt/media）
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
DECK = {LAB: "吸蟲實驗（實驗課 slides）", NEM: "線蟲圖譜（1 線蟲圖檔）", TRE: "吸蟲圖譜（2 吸蟲圖檔）", MIX: "人體常見寄生蟲蟲卵原色等比圖譜",
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


def pptx_media(pptx, media):
    with zipfile.ZipFile(f"{SRC}/{pptx}") as z:
        return Image.open(io.BytesIO(z.read(f"ppt/media/{media}")))


def svg(id, ch, title, topics, kw, cap):
    assert os.path.exists(f"{ROOT}/figures/{id}.svg"), id
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap)


def slide(id, ch, title, topics, kw, cap, src, page, box=None, media=None):
    name = id.removeprefix("slide-")
    im = pptx_media(src, media) if media else pdf_crop(src, page, box or (0, 0, 1, 0.93))
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
 # ---------------- 蟯蟲與犬蛔蟲
 slide("slide-enterobius-adult", "enterobius-toxocara", "蟯蟲雌蟲：食道球與尖尾", ["蟯蟲"],
       "Enterobius vermicularis female esophageal bulb cephalic alae pinworm", "8–13 mm，前端有<strong>頸翼（cephalic alae）</strong>與<strong>食道球</strong>、尾巴長而尖；夜間爬到肛門周圍產卵。", NEM, 6),
 slide("slide-enterobius-egg", "enterobius-toxocara", "蟯蟲卵：一邊扁平的 D 字形", ["蟯蟲"],
       "Enterobius egg asymmetrical flattened one side L3 larva", "約 55 × 26 µm、無色透明、<strong>一側扁平一側凸（左右不對稱）</strong>，卵內常已有幼蟲。", NEM, 7),
 slide("slide-scotch-tape", "enterobius-toxocara", "肛圍擦拭法（Scotch tape test）", ["蟯蟲"],
       "Scotch tape test adhesive tape perianal swab diagnosis", "蟯蟲卵產在肛門周圍、<strong>糞便很少找到</strong>，所以要在早上起床、排便洗澡前用透明膠帶黏肛圍。", NEM, 8),
 slide("slide-toxocara-egg", "enterobius-toxocara", "犬蛔蟲卵：球形厚殼、表面有凹洞", ["犬蛔蟲"],
       "Toxocara canis egg pitted shell", "80–85 µm、球形厚殼、蛋白膜表面像高爾夫球的<strong>凹洞（pitted）</strong>。人吃到卵 → VLM／OLM，<strong>人的糞便不會出現犬蛔蟲卵</strong>。", NEM, 30),
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
