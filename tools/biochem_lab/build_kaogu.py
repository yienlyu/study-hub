"""生化實驗考古 → subjects/biochem-lab/data/questions-kaogu.json
原檔：
  114：slides/biochemistry/共筆考古/百十三資料/生化(二)/考古/終審版/實驗/*.pdf（陳顧中、周志銘、鄭嘉雄 -1／-2）
  108、109、歷屆：slides/biochem-lab/共筆考古/考古/*.pdf（共筆考古 Drive「生化實」資料夾）
文字檔由 pdftotext -layout 產生，放在 tools/biochem_lab/k1141/ 與 tools/biochem_lab/older/。
題目重複時只留最新的一份（114 > 歷屆 > 109 > 108）。題目要看圖的，圖由 crop_questions.py 裁好。
用法：python3 tools/biochem_lab/build_kaogu.py
"""
import json, os, re, difflib, collections

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'subjects', 'biochem-lab', 'data', 'questions-kaogu.json')

# (文字檔, id 前綴, 來源標籤, 只收這些題號)
FILES = [
    ('k1141/chen.txt', 'k114-chen', '114 實驗考古', None),
    ('k1141/chou.txt', 'k114-chou', '114 實驗考古', None),
    ('k1141/cheng1.txt', 'k114-cheng', '114 實驗考古', range(1, 21)),
    ('k1141/cheng2.txt', 'k114-cheng', '114 實驗考古', None),
    ('older/kall.txt', 'kall', '歷屆實驗考古', None),
    ('older/k109.txt', 'k109', '109 實驗考古', None),
    ('older/k108.txt', 'k108', '108 實驗考古', None),
]

NUMROW = re.compile(r'^\s*(\d+)(\s+\d+)*\s*$')
LETROW = re.compile(r'^\s*([A-EX]{1,5})(\s+[A-EX]{1,5})*\s*$')
QLINE = re.compile(r'^\s*(\d+)\s*[.．]\s*(.*)$')
QSTOP = re.compile(r'^\s*(二\s*[、.]\s*)?(手寫題|配合題|簡答)')
XSTOP = re.compile(r'^\s*(二\s*[、.]\s*)?(手寫題|配合題)')


def parse(text):
    L = text.replace('\r', '').replace('\f', '\n').split('\n')
    def table_at(i):
        if not NUMROW.match(L[i]) or len(L[i].split()) < 3: return False
        j = i + 1
        while j < len(L) and not L[j].strip(): j += 1
        return j < len(L) and LETROW.match(L[j]) and len(L[j].split()) == len(L[i].split())
    # 答案表：第一個「數字列＋字母列」
    t0 = next(i for i in range(len(L)) if table_at(i))
    answers, i, last = {}, t0, t0
    while i < len(L) and i < t0 + 30:
        if NUMROW.match(L[i]):
            nums = [int(x) for x in L[i].split()]
            j = i + 1
            while j < len(L) and not L[j].strip(): j += 1
            if j < len(L) and LETROW.match(L[j]) and len(L[j].split()) == len(nums):
                answers.update(zip(nums, L[j].split())); last = j
            i = j + 1
        else:
            i += 1
    qs, cur, field, stop = {}, None, None, False
    for l in L[:t0]:
        s = l.strip()
        if QSTOP.match(l): stop = True
        m = QLINE.match(l)
        if m and not stop and (cur is None or int(m.group(1)) == cur['num'] + 1 or not qs):
            n = int(m.group(1))
            cur = {'num': n, 'stem': m.group(2).strip(), 'options': []}
            qs[n] = cur; field = 'stem'; continue
        if stop or cur is None or not s: continue
        if re.match(r'^[＊*※].*老師', s) or re.search(r'老師部分', s): continue
        if re.match(r'^\([A-E]\)', s):
            # 一行可能並排好幾個選項（109 的排版）
            for k, t in re.findall(r'\(([A-E])\)\s*(.*?)(?=\s*\([A-E]\)|$)', s):
                cur['options'].append({'k': k, 't': t.strip()})
            cur['options'].sort(key=lambda o: o['k']); field = 'opt'; continue
        if field == 'opt' and cur['options']:
            if len(re.findall(r'\S {3,}\S', s)) >= 2: continue  # 選項後面的表格
            cur['options'][-1]['t'] += ' ' + s
        else:
            cur['stem'] += ' ' + s
    ex, cur = {}, None
    for l in L[last + 1:]:
        if XSTOP.match(l): break
        heads = re.findall(r'(\d+)\s*\.\s*((?:\([A-E]\))+)', l)
        if heads and re.match(r'^\s*\d+\s*\.\s*\(', l) and int(heads[0][0]) in qs:
            cur = [int(h[0]) for h in heads]
            rest = re.sub(r'^\s*(\d+\s*\.\s*(\([A-E]\))+\s*)+', '', l).strip()
            for n in cur: ex[n] = [rest] if rest else []
            continue
        if cur:
            for n in cur: ex[n].append(l.strip())
    return qs, answers, ex


def clean_explain(lines):
    out = []
    for l in lines:
        if not l: continue
        starts_new = re.match(r'^(\([A-E1-9a-e]\)|[1-9]\.|\(\d\)|[①-⑩]|＊|\*|註|根據|補充|【)', l)
        if out and not starts_new:
            prev = out[-1]
            sep = ' ' if re.search(r'[A-Za-z0-9,.)]$', prev) and re.match(r'^[A-Za-z0-9(]', l) else ''
            out[-1] = prev + sep + l
        else:
            out.append(l)
    s = '\n'.join(out)
    s = re.sub(r'(?<=[一-鿿，。、）])\s+(?=[一-鿿，。、（])', '', s)
    return s.strip()


# ------------------------------------------------------------------ 章節與考點
SKIP = r'P53|[Cc]holesterol|膽固醇|TBA|Fenton|peroxid|過氧化|[Aa]therosclerosis|抗氧化|sarkosyl|MDA|[Aa]rachidonic|monocyte|foam cell|hydroperoxide|bis-allylic|自由基.*亞鐵'
CHAPTERS = [
    ('sds-page', r'SDS|[Aa]crylamide|APS|TEMED|[Ss]tacking|[Rr]unning gel|mercaptoethanol|上膠|下膠|蛋白質電泳|Rf|R-?250|[Nn]ative|[Gg]lycine|[Ss]ample buffer|disulfide|雙硫鍵|bisulfate|pre-stain'),
    ('gel-filtration', r'[Gg]el filtration|Sephadex|Sepharose|Sephacryl|[Mm]ethyl orange|[Bb]ed height|填充|流速|分子量測定|[Ss]ize exclusion|chromatography|2B|juice'),
    ('restriction', r'[Rr]estriction|限制|EcoRI|BamHI|XhoI|HindIII|physical map|Type II|isoschizomer|palindrom|sticky|blunt'),
    ('plasmid', r'S1|S2|S3|RNase|[Ee]lution|TE buffer|DNA ?電泳|[Aa]garose|[Ll]oading dye|Gel ?[Gg]reen|EtBr|TAE|TBE|燈箱|[Ss]upercoil|plasmid|質體|miniprep|DNA 染劑|樣品染料|電泳槽|洋菜'),
    ('protein-assay', r'.'),
]
TOPICS = {
    'protein-assay': [
        ('Pipetman 操作', r'[Pp]ipet|micropipette|P-\d+'),
        ('化學呈色法：Biuret／Lowry／BCA', r'Biuret|Lowry|BCA|Folin|Cu2|phosphomolybd|\bion\b'),
        ('Bradford 與 CBB', r'Bradford|Coomassie|CBB|595'),
        ('UV 280 nm 定量', r'UV|280|260|Tryptophan|Tyrosine|Phenylalanine|aromatic'),
        ('標準曲線與吸光值', r'standard curve|R2|absorbance|ELISA|spectro|吸光'),
    ],
    'plasmid': [
        ('鹼裂解法：S1／S2／S3', r'S1|S2|S3|RNase|Resuspension|Lysis|Neutral'),
        ('Elution 與 TE buffer', r'[Ee]lution|TE buffer|EB'),
        ('Agarose 電泳條件', r'[Aa]garose|濃度|TAE|TBE|電泳槽|跑得|距離'),
        ('DNA 型態與移動速度', r'[Ss]upercoil|OC|[Ll]inear|circular'),
        ('染劑、loading dye 與照膠', r'Gel ?green|EtBr|燈箱|UV|[Ll]oading|染'),
    ],
    'restriction': [
        ('限制酶類型與辨識序列', r'Type|EcoRI|palindrom|辨識'),
        ('限制酶圖譜（physical map）', r'map|圖譜|BamHI|XhoI|HindIII'),
    ],
    'gel-filtration': [
        ('原理：大分子先出來', r'[Ss]ize|smallest|largest|分子|time point|min'),
        ('樹脂與條件選擇', r'Sephadex|Sepharose|Sephacryl|2B|4B|6B|range|bead|[Bb]ed height|流速|填充|pH'),
        ('Methyl orange 與 BSA 偵測', r'450|[Mm]ethyl orange|BSA|OD'),
    ],
    'sds-page': [
        ('鑄膠：acrylamide、bis、APS、TEMED', r'[Aa]crylamide|APS|TEMED|polymeriz|free radical|自由基|bis|水|壓'),
        ('Sample buffer 成分', r'[Ss]ample buffer|mercaptoethanol|雙硫鍵|disulfide|[Gg]lycerol|denature|negative charge'),
        ('Stacking 與 pH（6.8／8.8／8.3）', r'[Ss]tacking|pH|[Gg]lycine|[Cc]hloride|上膠|下膠|layer|[Ll]ower|[Uu]pper'),
        ('染色與分子量估算', r'CBB|[Cc]oomassie|stain|染|Rf|[Ll]og|marker|mobility|R-?250'),
        ('樣品配製計算', r'μ[lL]|µ[lL]|\dX|fold'),
    ],
}

# ------------------------------------------------------------------ 人工校正
# key: (id 前綴, 題號)
F = {
    ('k114-chen', 1): {'img': ['figures/questions/chen-01.webp'],
                       'stem': 'Johnny conducts the biochemistry experiments with a P-100 micropipette. As the figure shows (dial reads 0-6-3), what is the buffer quantity that Johnny wants to get?'},
    ('k114-chen', 3): {'img': ['figures/questions/chen-03.webp']},
    ('k114-chen', 4): {'img': ['figures/questions/chen-04.webp']},
    ('k114-chen', 5): {'img': ['figures/questions/chen-05.webp'],
                       'stem': 'The following is a reactant in juice (ascorbic acid → dehydroascorbic acid, see figure). What experiment would you design to measure the amount of reactants in the juice?',
                       'note': '原題選項只寫 2B／4B／6B（Sepharose 種類，見第 4 題的表）。'},
    ('k114-chen', 6): {'stem': 'Which of the following is the compound used in gel filtration that is detected at 450 nm in our experiment this semester?',
                       'explain': 'Gel filtration 實驗把 BSA（大分子，約 66 kDa）和 methyl orange（小分子染料，黃色）混合上管柱：BSA 先流出、methyl orange 後流出。Methyl orange 用 OD 450 nm 偵測；BSA 則用 Bradford（595 nm）測。'},
    ('k114-chen', 7): {'explain': '今年用 Sephadex G-50 當樹脂（詳見 gel filtration protocol 第 3 張）。Sepharose 是 agarose 系列（2B、4B、6B），Sephacryl 是 allyl dextran 與 bis-acrylamide 交聯。'},
    ('k114-chen', 11): {'stem_sub': [('260 nm', '≈260 nm')],
                        'explain': '選項中最接近的是 Phe（最大吸光約 257 nm）。Trp 約 280 nm、Tyr 約 275 nm，蛋白質 UV 定量通常用 280 nm（主要靠 Trp、Tyr）。'},
    ('k114-chen', 18): {'explain': 'R² 越接近 1，標準曲線的線性越好。選項中 0.99 最佳。'},
    ('k114-chen', 19): {'stem': 'In the biochemistry experiments this semester, which absorbance wavelength was used to detect methyl orange in the gel filtration experiment?',
                        'note': '原題問的是「蛋白質定量」用的波長，但選項沒有 595 nm；共筆解答選 450 nm（methyl orange），本站把題目改成問 methyl orange。',
                        'explain': '450 nm 測 methyl orange（gel filtration）；Bradford + 蛋白質用 595 nm。'},
    ('k114-chen', 29): {'explain': 'Bradford 試劑的 CBB G-250 結合蛋白質後由紅褐色（陽離子型，470 nm）轉為藍色（陰離子型），最大吸光移到 595 nm。'},
    ('k114-chen', 31): {'chapter': 'protein-assay', 'img': ['figures/questions/chen-31.webp'],
                        'explain': 'G-250 比 R-250 多兩個甲基（G = greenish，R = reddish）。圖中苯環上帶甲基的就是 G-250，Bradford 定量用的也是 G-250。'},
    ('k109', 1): {'stem': 'Teacher wants to evaluate how much volume this is in a 1000 μl micropipette (dial reads 0-6-3)?',
                  'img': ['figures/questions/chen-01.webp']},
    ('k109', 5): {'drop': True}, ('k109', 9): {'drop': True}, ('k109', 14): {'drop': True},
    ('k114-chen', 28): {'chapter': 'protein-assay'},
    ('k114-cheng', 11): {'chapter': 'sds-page'},
    ('k108', 26): {'drop': True},
    ('k109', 3): {'keep': True, 'img': ['figures/questions/chen-03.webp'],
                  'note': '同 114 第 3 題的層析圖，但這題問的是最大分子量。'},
    ('k114-chou', 4): {'options_sub': [('DNase A', 'DNase I')]},
    ('k114-chou', 11): {'stem': 'DNA 樣品染料（loading dye）中有哪幾種成分？（複選）'},
    ('k114-cheng', 3): {'options': [{'k': 'A', 't': 'bromophenol blue'}, {'k': 'B', 't': 'methylene blue'},
                                    {'k': 'C', 't': 'coomassie brilliant blue'}, {'k': 'D', 't': 'trypan blue'}],
                        'note': '原題 (A)(B) 重複，本站把 (B) 改成 methylene blue。'},
    ('k114-cheng', 7): {'explain': 'β-mercaptoethanol（或 DTT）是還原劑，打斷 disulfide bond；SDS 讓蛋白質變性並帶負電；glycerol 增加密度讓樣品沉入 well；bromophenol blue 是追蹤染料。'},
    ('k114-cheng', 9): {'explain': 'CBB G-250 比 R-250 多兩個甲基。G-250 用於 Bradford 定量與膠體染色（膠體染色也常用 R-250）。'},
    ('k114-cheng', 17): {'img': ['figures/questions/cheng-17.webp']},
    ('k114-cheng', 19): {'img': ['figures/questions/cheng-19.webp'],
                         'explain': 'Rf = 蛋白質跑的距離 ÷ 追蹤染料（dye front）跑的距離。圖中 A 是 B 帶跑的距離、C 是 dye front 的距離，所以 Rf = A/C。'},
    ('k114-cheng', 23): {'explain': '5X sample buffer：x µL buffer 配 4x µL 樣品，總量 5x ≤ 25 µL → 樣品最多 20 µL。\n要在 20 µL 內裝 40 µg → 濃度至少 2 µg/µL。只有 (B) 1.7 µg/µL 不夠。'},
    ('k114-cheng', 27): {'stem': '蛋白質電泳實驗中，有同學在加入染劑至膠體後，呈色時間明顯比其他組慢，可能的原因為何？（複選）',
                         'note': '共筆組長認為 (A)(D) 都合理，答案採複選。'},
    ('k114-cheng', 28): {'stem': '在蛋白質電泳實驗中，有同學在開始跑電泳一段時間後，蛋白質標準液（marker）和蛋白質樣本都沒有往下跑，可能的原因為何？（複選）',
                         'note': '共筆組長認為 (A)(C) 都合理，答案採複選。'},
    ('k114-cheng', 30): {'type': 'short', 'options': [], 'answerText': '蛋白質電泳的 Rf 值（相對遷移距離）',
                         'stem': 'SDS-PAGE 中，log（分子量）與下列何者成反比？'},
    ('k114-cheng', 33): {'explain': 'Native PAGE 不讓蛋白質變性，保留活性，所以能在膠上分析酵素活性。SDS-PAGE 會把蛋白質變性；agarose 主要跑 DNA；2-D gel 第二維也是 SDS。'},
    ('k114-cheng', 37): {'stem_sub': [('bisulfate', 'disulfide')]},
    ('k114-cheng', 41): {'explain': 'G-250 與 R-250 差兩個甲基，溶解性不同，所以溶解試劑、偵測的蛋白質濃度範圍、脫色液的配方都不一樣 → 以上皆是。'},
}

# 手寫題（看答案練習）
SHORT = [
    {'id': 'k114-chen-w1', 'source': '114 實驗考古', 'chapter': 'protein-assay', 'num': '手寫 1',
     'stem': '請寫出蛋白質定量實驗會用到的東西。',
     'answerText': 'BSA（標準品）、兩種未知蛋白 S1 和 S2、1× Bradford reagent、eppendorf、ELISA reader、96 well plate、pipetman 與 tips',
     'explain': 'BSA 做標準曲線（x 軸濃度、y 軸 OD595），未知蛋白讀值代入回歸式求濃度。'},
    {'id': 'k114-chou-w16', 'source': '114 實驗考古', 'chapter': 'plasmid', 'num': '手寫 16',
     'img': ['figures/questions/chou-16.webp'],
     'stem': 'The agarose gel electrophoresis results of mini-preparation of pTMU DNA are shown in the figure.\n'
             '(A) Is the pTMU DNA molecule linear or circular?\n(B) What is the "low molecular weight nucleic acid" in lane 2?\n'
             '(C) Which buffer in mini-preparation (S1, S2, S3, W1, W2, EB) may cause the result in (B) when it went wrong?\n(D) Please explain the lane 4 result.',
     'answerText': '(A) Circular\n(B) 殘留的 RNA（low MW nucleic acid）\n(C) S1（含 RNase A）\n(D) 最上面的 band 和 lane 3 相同：部分 DNA 只被 BamHI 切（不完全切割）；下面兩條是 BamHI + XhoI 都切到的片段',
     'explain': 'BamHI 單切只得一條 band → 環狀 DNA 被切成一條線狀。RNase A 加在 S1（resuspension buffer），S1 出問題時 RNA 沒被分解，就會在膠底跑出一團低分子量核酸。'},
    {'id': 'k114-chou-w17', 'source': '114 實驗考古', 'chapter': 'plasmid', 'num': '手寫 17',
     'stem': 'In agarose gel electrophoresis:\n(A) Which buffer system is used in this experiment?\n(B) Which DNA staining dye is used in this experiment?\n(C) What is the function of the DNA loading dye?',
     'answerText': '(A) TAE buffer\n(B) Gel Green\n(C) 讓透明的 DNA 樣品有顏色，確認有加進 well，並追蹤電泳進度；glycerol 增加密度讓樣品沉入 well',
     'explain': '今年用 TAE 與 Gel Green（藍光 LED 照膠，不用 UV）。Loading dye 含 bromophenol blue、xylene cyanol（追蹤染料）與 glycerol。'},
    {'id': 'k114-chou-w18', 'source': '114 實驗考古', 'chapter': 'restriction', 'num': '手寫 18',
     'stem': 'In the restriction enzyme experiment, we used BamHI, XhoI and EcoRI to digest pTMU DNA. EcoRI belongs to which type of restriction enzyme? (Type I, II, III)',
     'answerText': 'Type II',
     'explain': 'Type II 限制酶在辨識序列內（或固定位置）切割，不需 ATP，最常用於分子生物學。EcoRI 辨識 G↓AATTC（回文序列），切出 5′ 突出黏端。'},
    {'id': 'k114-cheng-w43', 'source': '114 實驗考古', 'chapter': 'sds-page', 'num': '手寫 43',
     'stem': 'Dr. Cheng 純化了兩個重組蛋白 A 與 B（A 比 B 大），但忘了標示試管。請用以下材料設計 SDS-PAGE 實驗分辨哪管是 A、哪管是 B，並畫圖說明：\n'
             'Tris-Glycine SDS-PAGE、Sample buffer、Electrophoresis system、Coomassie Blue G-250、Water bath、Water、Protein marker、Glycine buffer。',
     'answerText': '兩管各取樣品加 sample buffer，煮沸變性 → 和 protein marker 一起 loading 到 Tris-Glycine SDS-PAGE → 用含 glycine 的 running buffer 在電泳系統跑膠 → 水洗去 SDS → CBB G-250 染色。對照 marker：跑得慢（靠近 well）的那管是 A，跑得快的是 B。',
     'explain': '各材料的用途：\nSDS-PAGE：依分子量分離。\nSample buffer：SDS 變性並帶負電、β-ME 打斷雙硫鍵、glycerol 增加密度、bromophenol blue 追蹤。\nWater bath：加熱變性。\nGlycine buffer：維持 pH，在 stacking gel 形成離子邊界、濃縮蛋白質。\nWater：洗掉 SDS，避免和 CBB 互斥。\nCBB G-250：染蛋白質。\nProtein marker：分子量標準。\n畫圖：marker、A、B 三道，負極在上、正極在下，A 的 band 比 B 高。'},
]

# ------------------------------------------------------------------ 組裝
def norm(s):
    return re.sub(r'[^0-9a-z一-鿿]', '', s.lower())


def chapter_of(stem, whole):
    if re.search(SKIP, whole): return None
    # 先看題幹，題幹看不出來再看選項
    return next((c for c, rx in CHAPTERS[:-1] if re.search(rx, stem)), None) or next(c for c, rx in CHAPTERS if re.search(rx, whole))


def build():
    out, seen = [], []
    stats = collections.Counter()
    for fn, prefix, src, only in FILES:
        qs, answers, ex = parse(open(os.path.join(HERE, fn), encoding='utf-8').read())
        for n, q in sorted(qs.items()):
            if only and n not in only: continue
            fx = F.get((prefix, n), {})
            stem = fx.get('stem', q['stem'])
            for a, b in fx.get('stem_sub', []): stem = stem.replace(a, b)
            opts = fx.get('options', q['options'])
            for a, b in fx.get('options_sub', []):
                opts = [{**o, 't': o['t'].replace(a, b)} for o in opts]
            if fx.get('drop'): stats['skip-dup'] += 1; continue
            whole = stem + ' ' + ' '.join(o['t'] for o in opts)
            ch = fx.get('chapter') or chapter_of(stem, whole)
            if ch is None: stats['skip-scope'] += 1; continue
            key = norm(whole)
            # 只跟其他檔比（同一份考卷裡的 S1／S2／S3、上膠／下膠 長得很像但不是重複）
            if not fx.get('keep') and any(f != fn and difflib.SequenceMatcher(None, key, k).ratio() > 0.88 for f, k in seen):
                stats['skip-dup'] += 1; continue
            ans = fx.get('answer') or list(answers.get(n, '').replace('X', ''))
            qtype = fx.get('type', 'mcq')
            if qtype == 'mcq' and (len(opts) < 2 or not ans):
                stats['skip-bad'] += 1; continue
            seen.append((fn, key))
            explain = fx.get('explain') or clean_explain(ex.get(n, []))
            explain = re.sub(r'(詳見|參考)[^。\n]*(投影片|簡報|第 ?\d+ ?頁)[^。\n]*。?', lambda m: m.group(0), explain)
            item = {
                'id': f'{prefix}-{n:02d}', 'source': src, 'num': n, 'chapter': ch, 'type': qtype,
                'stem': stem, 'options': opts, 'answer': ans if qtype == 'mcq' else [],
                'explain': explain,
            }
            if qtype == 'short': item['answerText'] = fx['answerText']
            if fx.get('img'): item['img'] = fx['img']
            if fx.get('note'): item['note'] = fx['note']
            out.append(item); stats[src] += 1
    for s in SHORT:
        out.append({'type': 'short', 'options': [], 'answer': [], **s}); stats[s['source']] += 1
    for q in out:
        txt = q['stem'] + ' ' + ' '.join(o['t'] for o in q['options'])
        q['topics'] = [t for t, rx in TOPICS[q['chapter']] if re.search(rx, txt)][:2] or [TOPICS[q['chapter']][0][0]]
        q['pattern'] = '簡答題' if q['type'] == 'short' else ('計算題' if re.search(r'\d+\s*(µ|μ)', q['stem']) or 'curve formula' in q['stem'] else
                        '選錯誤／否定題' if re.search(r'not|NOT|incorrect|不會|非|錯誤', q['stem']) else '選正確／單一概念題')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), dict(stats))
    print(collections.Counter(q['chapter'] for q in out))


if __name__ == '__main__':
    build()
