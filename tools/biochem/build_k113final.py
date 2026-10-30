"""113 生化（二）期末考古（共筆整理版）→ subjects/biochem/data/questions-k113f.json
原檔：slides/biochemistry/共筆考古/百十三資料/生化(二)/考古/終審版/正課/期末/*.pdf
文字檔由 pdftotext -layout 產生，放在 tools/biochem/k113final/。
用法：python3 tools/biochem/build_k113final.py
"""
import json, os, re, collections

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'subjects', 'biochem', 'data', 'questions-k113f.json')
SRC = '113 期末考古'

# (文字檔, 章節 id, section 標籤)
FILES = [
    ('ch12.txt', 'ch12', 'Ch12'),
    ('ch22a.txt', 'ch22n', 'Ch22 補充'),
    ('ch22b.txt', 'ch22n', 'Ch22 補充'),
    ('ch2425.txt', 'ch24', 'Ch24-25'),
    ('ch26.txt', 'ch26', 'Ch26'),
    ('ch28.txt', 'ch28', 'Ch28'),
]

NUMROW = re.compile(r'^\s*(\d+)(\s+\d+)+\s*$')
LETROW = re.compile(r'^\s*([A-EX]{1,4})(\s+[A-EX]{1,4})*\s*$')
QLINE = re.compile(r'^\s*(\d+)\s*[.．]\s*(.*)$')
GROUP = re.compile(r'^\s*(\d+)-(\d+)\s*為題組')
SKIP = {'選擇題', '簡答', '簡答選擇題', '詳解', '一、單選題'}


def parse(text):
    L = text.replace('\r', '').split('\n')
    # 答案表：第一個以 1 開頭的數字列
    t0 = next(i for i, l in enumerate(L) if NUMROW.match(l) and l.split()[0] == '1')
    answers, i, last = {}, t0, t0
    while i < len(L) and i < t0 + 40:
        if NUMROW.match(L[i]):
            nums = [int(x) for x in L[i].split()]
            j = i + 1
            while j < len(L) and not L[j].strip(): j += 1
            if j < len(L) and LETROW.match(L[j]) and len(L[j].split()) == len(nums):
                answers.update(zip(nums, L[j].split())); last = j
            i = j + 1
        else:
            i += 1
    # 題目（含題組：共用的說明與選項）
    qs, cur, expect, field, grp = {}, None, None, None, None
    for l in L[:t0]:
        s = l.strip()
        g = GROUP.match(l)
        if g:
            grp = {'lo': int(g.group(1)), 'hi': int(g.group(2)), 'intro': [], 'options': []}
            cur = None; field = 'grp'; continue
        m = QLINE.match(l)
        if m and (expect is None or int(m.group(1)) == expect):
            n = int(m.group(1))
            cur = {'num': n, 'stem': m.group(2).strip(), 'options': []}
            if grp and grp['lo'] <= n <= grp['hi']:
                cur['grp'] = grp
            qs[n] = cur; expect = n + 1; field = 'stem'; continue
        if not s or s in SKIP: continue
        mo = re.match(r'^\(([A-E])\)\s*(.*)$', s)
        if field == 'grp' and cur is None:
            if mo: grp['options'].append({'k': mo.group(1), 't': mo.group(2).strip()})
            else: grp['intro'].append(s)
            continue
        if cur is None: continue
        if mo:
            cur['options'].append({'k': mo.group(1), 't': mo.group(2).strip()}); field = 'opt'; continue
        if field == 'opt' and cur['options']:
            cur['options'][-1]['t'] += ' ' + s
        else:
            nl = re.match(r'^(\(?\d\)?[.)]|[①-⑩]|I{1,3}\.|IV\.)', s)
            cur['stem'] += ('\n' if nl else ' ') + s
    for q in qs.values():
        g = q.pop('grp', None)
        if g:
            q['stem'] = f"（題組 {g['lo']}–{g['hi']}）" + ' '.join(g['intro']) + '\n\n' + q['stem']
            q['options'] = g['options']
    # 詳解：「數字. (」開頭、題號遞增且是本檔的題目才換題
    ex, cur = {}, None
    for l in L[last + 1:]:
        m = re.match(r'^\s*(\d+)\s*\.\s*\(', l)
        if m and int(m.group(1)) in qs and (cur is None or int(m.group(1)) > cur):
            cur = int(m.group(1)); ex[cur] = [re.sub(r'^\s*\d+\s*\.\s*(\([A-EX]\))*', '', l).strip()]; continue
        if cur is not None:
            ex[cur].append(l.strip())
    return qs, answers, ex


def clean_explain(lines):
    out = []
    for l in lines:
        if not l: continue
        starts_new = re.match(r'^(\([A-E1-9a-e]\)|[1-9]\.|\(\d\)|[①-⑩]|註|＜|根據|補充)', l)
        if out and not starts_new:
            prev = out[-1]
            sep = ' ' if re.search(r'[A-Za-z0-9,.)]$', prev) and re.match(r'^[A-Za-z0-9(]', l) else ''
            out[-1] = prev + sep + l
        else:
            out.append(l)
    s = '\n'.join(out)
    s = re.sub(r'(?<=[一-鿿，。、）])\s+(?=[一-鿿，。、（])', '', s)
    return s.strip()


# ------------------------------------------------------------------ 人工校正
# key: (檔名, 題號)；explain 直接覆寫，explain_sub 只做字串替換
F = {
    # ---- Ch12（黃彥華）
    ('ch12.txt', 1): {'stem_sub': [('is block?', 'is blocked?')]},
    ('ch12.txt', 2): {'stem': 'Like G proteins, the Ras protein binds ______ when in its active state, which is hydrolyzed to ______ to convert the protein to its inactive state.',
                      'explain': 'Ras 和 G protein 一樣：結合 GTP 時為活化態，本身的 GTPase 把 GTP 水解成 GDP 後失活。\n'
                                 'SOS 是 GEF，讓 Ras 放掉 GDP、換上 GTP（活化）；GAP 加速 GTP 水解（失活）。'},
    ('ch12.txt', 3): {'stem': 'InsP₃ binds to ______ channels in the endoplasmic reticulum, while DAG activates ______.',
                      'explain': 'IP₃ 結合 ER 膜上的 IP₃-gated Ca²⁺ 通道 → Ca²⁺ 釋出到細胞質；DAG 與 Ca²⁺ 一起活化 protein kinase C（PKC）。\n'
                                 'PKA 是 cAMP 活化的，和 PLC 路徑無關。'},
    ('ch12.txt', 4): {'explain': 'Insulin receptor → IRS-1 → PI3K → PIP₃ → PDK1 磷酸化活化 PKB（Akt）→ PKB 磷酸化 GSK3 使其失活 → glycogen synthase 不再被 GSK3 磷酸化 → 保持活化，肝醣合成增加。\n'
                                 '(B) ERK 屬於 Ras-MAPK 路徑，調控細胞生長與增生，不直接作用在 glycogen synthase。\n'
                                 '(C) PIP₃ 是招募 PDK1、PKB 到膜上，不是 glycogen synthase 的別構活化劑。\n'
                                 '(D) 與 guanylate cyclase、cGMP 無關。'},
    ('ch12.txt', 9): {'explain': '(A) Thyroxine：核受體。\n(B) Epinephrine：GPCR（α、β-adrenergic receptor）。\n'
                                 '(C) EGF：receptor tyrosine kinase ✔（生長因子多半走 RTK）。\n(D) Glucagon：GPCR。\n(E) Cortisol：細胞質的 glucocorticoid receptor（核受體家族）。'},
    ('ch12.txt', 10): {'explain': 'Glucocorticoid 與細胞質受體結合後進入細胞核，經 zinc finger DNA-binding domain 結合 GRE，誘導 IκBα 合成。\n'
                                  'IκBα 把 NF-κB 留在細胞質，NF-κB 無法進核啟動發炎基因（TNF、IL-6 等）→ 抗發炎。\n'
                                  'TNF、NF-κB 都是發炎方向的分子。'},
    ('ch12.txt', 11): {'stem': 'Isoproterenol has the same catechol–ethanolamine structure as epinephrine, except that the amino nitrogen carries an isopropyl group instead of a methyl group. What is isoproterenol?',
                       'note': '原題附 isoproterenol 與 epinephrine 的結構圖，本站改用文字描述差異。',
                       'explain': 'Isoproterenol 是 epinephrine 的合成類似物（N 上是異丙基），能與 β-adrenergic receptor 結合並引起和 epinephrine 相同的反應 → agonist（β 選擇性 agonist）。\n'
                                  '對照：antagonist 結合受體但不活化（如 propranolol）；inverse agonist 會降低受體的基礎活性。'},
    ('ch12.txt', 13): {'explain': 'G protein 的 α 次單位結合 GDP 時為不活化態（與 βγ 組成三聚體）；受體活化後 α 放掉 GDP、換上 GTP，與 βγ 分開而活化下游（如 adenylate cyclase）。'},
    ('ch12.txt', 14): {'explain': '四者都能活化 phospholipase C → PIP₂ 切成 IP₃ + DAG：\n'
                                  'Acetylcholine（muscarinic M1、M3）、vasopressin（V1）、TRH 經 Gq 活化 PLCβ；PDGF 經 RTK 活化 PLCγ。'},
    # ---- Ch22 核苷酸補充（國考題）
    ('ch22a.txt', 2): {'explain': 'Purine 環的原料：glycine（C4、C5、N7）、glutamine（N3、N9）、aspartate（N1）、CO₂（C6）、N¹⁰-formyl-THF（C2、C8）。\n'
                                  'Asparagine、serine 不直接參與（serine 只經 THF 間接提供一碳單位），所以是 ②④⑤。'},
    ('ch22a.txt', 4): {'explain': 'IMP → adenylosuccinate → AMP 這一支被終產物 AMP 回饋抑制；IMP → GMP 則被 GMP 抑制。\n'
                                  'GTP 是 IMP → AMP 的能量來源（交叉需要），不是抑制劑。'},
    ('ch22a.txt', 13): {'explain': 'Lesch-Nyhan syndrome：HGPRT 缺乏 → hypoxanthine、guanine 無法經 salvage 回收 → PRPP 堆積、de novo 合成反而增加 → 尿酸大量產生（痛風、結石），加上神經症狀（自殘行為、智能障礙、肢體不協調）。\n'
                                   '(B) 錯：de novo 路徑本身正常，壞掉的是 salvage。'},
    ('ch22a.txt', 15): {'explain_sub': [('下圖紅框處 ', ''), ('此酵素可以將 NTP 轉為 dNTP', '此酵素負責 NDP → dNDP')]},
    ('ch22b.txt', 23): {'explain': 'Ribonucleotide reductase 的受質是 NDP（ADP、GDP、CDP、UDP），產物為 dNDP。\n'
                                   '② GMP 是 NMP、③ ATP 是 NTP，都不是受質；④ TDP 也不是（dTMP 由 dUMP 經 thymidylate synthase 而來）。所以只有 ①。'},
    ('ch22b.txt', 35): {'explain_sub': [('Thymine kinase', 'thymidine kinase')]},
    ('ch22b.txt', 36): {'explain': 'AZT（zidovudine）的 3′-OH 換成 azido，進細胞後磷酸化成 AZT-TP，被 HIV 反轉錄酶接上 DNA 後就無法再延長 → 鏈終止；HIV 反轉錄酶對 AZT-TP 的親和力遠高於人類 DNA polymerase。同類：ddC、ddI、3TC、d4T。\n'
                                   '對照：acyclovir、ganciclovir → 病毒 DNA polymerase；araC → 癌細胞 DNA polymerase；5-FU → thymidylate synthase；methotrexate、aminopterin、trimethoprim → DHFR；6-mercaptopurine、6-thioguanine → purine salvage（PRT）。'},
    ('ch22b.txt', 37): {'explain': '(D) 錯：人類 DNA polymerase 對 AZT-TP 的親和力低，AZT 的選擇性正是來自 HIV 反轉錄酶的高親和力。其餘敘述見第 36 題。'},
    ('ch22b.txt', 38): {'explain': 'HIV 反轉錄酶有三種活性：\n(1) RNA-dependent DNA polymerase：以病毒 RNA 為模板合成 DNA（RNA-DNA hybrid）。\n'
                                   '(2) RNase H：分解 hybrid 中的 RNA。\n(3) DNA-dependent DNA polymerase：再合成第二股 DNA。\n'
                                   'DNA-dependent RNA synthesis 是轉錄（RNA polymerase 的工作），不屬於反轉錄酶。'},
    ('ch22b.txt', 42): {'explain': 'Purine 是雙環（六角環接五角環），pyrimidine 是單環，所以 purine 比較大，(B) 錯。Thymine = 5-methyluracil，含甲基。'},
    # ---- Ch24-25（施純明）
    ('ch2425.txt', 2): {'explain': 'Hairpin 需要一段序列和後面的序列反向互補。(C) 5′-ACAGACAGA… 和 3′ 端的 …UCUGUCUGU 可以配成 9 bp 的 stem，中間的 CAG 當 loop，最容易形成 hairpin。'},
    ('ch2425.txt', 4): {'explain': 'Operator 是 DNA 上讓 repressor 結合的序列。Activator、repressor、transactivator 都是蛋白質（會結合 DNA，但本身不是 DNA 序列）。'},
    ('ch2425.txt', 7): {'explain': '互補股要從 5′ 寫到 3′：5′-CGCGAATTCGCG-3′ 是回文序列（palindrome，含 EcoRI 位置 GAATTC），互補股反過來讀仍然是 5′-CGCGAATTCGCG-3′。\n(A) 方向寫反；(C)(D) 含 U，是 RNA。'},
    ('ch2425.txt', 8): {'explain': '(C) 正確：DNA polymerase I 以 5′→3′ 外切酶活性移除 RNA primer（nick translation）。\n'
                                   '(A) Helicase 只解開雙股，不切 DNA。\n(B) Topoisomerase 是暫時切斷再接回（形成共價中間物）來改變超螺旋，不是核酸內切酶式的切割。\n'
                                   '(D) RNA primer 由 primase（DnaG）合成。'},
    ('ch2425.txt', 9): {'explain': '(C) 正確：β subunit（β clamp）形成環狀滑動夾，大幅提高 processivity。\n'
                                   '(A) Pol III 的校正是 3′→5′ 外切酶（ε subunit）。\n(B) 需要 RNA primer 提供 3′-OH。\n(D) 合成方向一律 5′→3′。\n'
                                   '(E) Pol III 同時合成 leading 與 lagging strand；Pol I 負責移除 primer 並補上 DNA。'},
    ('ch2425.txt', 11): {'explain': 'Topoisomerase I：切一股，每次改變 Lk 1。\nTopoisomerase II（如 DNA gyrase）：切兩股，每次改變 Lk 2（需 ATP）。'},
    ('ch2425.txt', 13): {'explain': '真核 pol α 帶 primase 活性（先合成 RNA primer，再接一小段 DNA），對應 E. coli 的 primase（DnaG）。\n'
                                    'pol β：DNA 修復；pol γ：粒線體 DNA 複製；pol δ／ε：主要延長（對應 Pol III）。'},
    ('ch2425.txt', 19): {'explain': '(D) 正確：RNA primer 由 primase（DnaG）合成。\n(A) Helicase 不切 DNA；(B) topoisomerase 是暫時切斷再接回；(C) primer 由 DNA polymerase I 移除，不是 primase；(E) primer 是 RNA。'},
    ('ch2425.txt', 21): {'explain': 'Klenow fragment 是 DNA polymerase I 被蛋白酶（trypsin、subtilisin）切開後的大片段：保留 5′→3′ polymerase 與 3′→5′ 外切酶（校正），去掉帶 5′→3′ 外切酶的小片段。'},
    ('ch2425.txt', 30): {'explain': 'Okazaki fragment 是 lagging strand 上不連續合成的短 DNA 片段。合成時 5′ 端帶一小段 RNA primer，但之後會被移除換成 DNA，教科書定義是 DNA 片段，所以選 (B) 不選 (D)。'},
    ('ch2425.txt', 32): {'explain': 'Helicase（DnaB）是 primosome 的一部分，在複製叉前方解開雙股。Topoisomerase 消除前方累積的超螺旋；primase 合成 RNA primer；clamp loader 把 β clamp 裝上 DNA。'},
    ('ch2425.txt', 33): {'explain': 'Primase（DnaG）依 DNA 模板合成短 RNA primer，提供 3′-OH 讓 Pol III 延長。\n'
                                    '(B) 填補 Okazaki 片段間的缺口是 Pol I + ligase；(C) 合成方向是 5′→3′；(D) 校正是 DNA polymerase 的 3′→5′ 外切酶。'},
    ('ch2425.txt', 35): {'explain': '粒線體 DNA 由 pol γ 複製，它也有 3′→5′ 外切酶校正與修復能力。\npol β：核內的 base excision repair；pol α：帶 primase；pol δ：主要延長。'},
    ('ch2425.txt', 36): {'explain_sub': [('，大家高中應該都有聽說過這件事', '')]},
    ('ch2425.txt', 37): {'explain': '雙向複製：從同一個 origin 向兩邊各形成一個 replication fork，同時往兩個方向進行。'},
    ('ch2425.txt', 39): {'explain': '(C) 正確：Pol III 是染色體複製的主要聚合酶。\n(A) 需要 primer；(B) nick translation 是 Pol I（5′→3′ 外切酶）；'
                                    '(D) 細胞內 90% 以上的 polymerase 活性來自 Pol I（Pol III 分子很少）；(E) primer 要提供的是 3′-OH。'},
    ('ch2425.txt', 40): {'explain': '校正：偵測錯配 → 3′→5′ 外切酶水解 phosphodiester bond，切掉錯的核苷酸 → 重新依鹼基配對接上正確的。\n'
                                    '這是水解反應，不是聚合反應的逆反應（pyrophosphorolysis），所以 (E) 不屬於校正。'},
    ('ch2425.txt', 41): {'explain': 'Nick translation：Pol I 從 nick 處用 5′→3′ 外切酶一邊切掉 RNA primer，一邊用 5′→3′ polymerase 補上 DNA；最後由 ligase 封口（(E) 是 ligase 的工作）。'},
    ('ch2425.txt', 43): {'explain': '真核基因體很大，DNA polymerase 速度又比細菌慢（約 50 nt/s，細菌約 1000 nt/s），只靠一個 origin 會複製太久，所以每條染色體有許多 origin。'},
    ('ch2425.txt', 44): {'stem_sub': [('similar to that of the subunit', 'similar to that of the β subunit')],
                         'explain': 'PCNA 是真核的 DNA sliding clamp（三聚體環），和 pol δ 結合，讓聚合酶一次能合成數千個核苷酸而不脫離（提高 processivity），功能等同 E. coli Pol III 的 β clamp。'},
    # ---- Ch26（周志銘）
    ('ch26.txt', 12): {'stem': 'Which of the following is true of the E. coli RNA polymerase?\n'
                               '1. Two copies of the α subunit are present, along with one each of β, β′, σ, and ω.\n'
                               '2. The largest subunit, β′, functions in DNA binding.\n'
                               '3. β binds the NTP substrates and interacts with σ; σ (70 kD) plays a role in transcription initiation.\n'
                               '4. The core polymerase (α₂ββ′ω) is catalytically competent and able to recognize promoters.',
                       'note': '原檔 β′、ω 符號轉檔後變成「*」，本站依課本補回。'},
    ('ch26.txt', 13): {'note': '依共筆公布答案為 C。第 3 項的判斷有爭議（poly(A) 一般認為能保護 mRNA 不被細胞質核酸酶分解）；第 5 項嚴格說是剪掉 intron、接合 exon。'},
    ('ch26.txt', 17): {'explain': '轉錄依鹼基配對：模板上的 A 對應 RNA 上的 U（RNA 沒有 T）。'},
    ('ch26.txt', 20): {'explain_sub': [('如右圖，', '')]},
    ('ch26.txt', 21): {'explain_sub': [('又稱為 TATA box', '又稱 Pribnow box（真核對應的是 TATA box）'), ('常出先', '常出現')]},
    # ---- Ch28（施純明）
    ('ch28.txt', 1): {'explain': 'Operator 是 repressor 結合的 DNA 序列（lac operon：LacI repressor 結合 operator，擋住 RNA polymerase）。\n'
                                 'Inducer（allolactose）是結合 repressor、讓它離開 operator，不是直接結合 operator。'},
    ('ch28.txt', 2): {'explain': '葡萄糖存在時 cAMP 低，CRP-cAMP 無法結合 → 即使有乳糖也只有低度表現（catabolite repression），所以 glucose 會降低 lactose 的誘導效果。\n'
                                 '(D) lac operon 主要在轉錄層次調控；(E) 有葡萄糖時就無法完全誘導。'},
    ('ch28.txt', 3): {'explain': '(A) 正確：CRP-cAMP 結合在 promoter 上游的 CRP site，幫助 RNA polymerase 結合 lac promoter。\n'
                                 '(B) 高 cAMP 促進結合；(C) 結合位置是 CRP site，不是 repressor（operator）區；(D) 葡萄糖少、cAMP 高時才結合；(E) 不影響 repressor 結合 operator。'},
    ('ch28.txt', 4): {'explain_sub': [('（下圖的 ACT）', '')]},
    ('ch28.txt', 5): {'explain': 'Trp operon 的 attenuation：leader peptide 含兩個連續 Trp codon。\n'
                                 'Trp 低：核糖體停在 Trp codon → leader 形成 2–3 anti-terminator → 繼續轉錄結構基因。\n'
                                 'Trp 高：核糖體快速通過 → 形成 3–4 terminator hairpin → 提早終止（sequence-dependent termination）。\n'
                                 '不論 Trp 高低，leader 區都會被轉錄，差別在後面的結構基因有沒有轉錄，所以 (C) 錯。'},
    ('ch28.txt', 6): {'explain': 'Enhancer 可以在基因上游、下游甚至 intron 裡，距離可達數千 bp，而且方向無關（orientation independent），這是 enhancer 最典型的特徵。'},
    ('ch28.txt', 7): {'explain': '乳糖低 → repressor 結合 operator；葡萄糖高 → cAMP 低、CRP 不結合。兩個條件都關掉，轉錄最少，所以是 III（葡萄糖高、乳糖低）。'},
    ('ch28.txt', 10): {'explain': 'σ⁷⁰（RpoD）是 E. coli 的 housekeeping σ factor，負責一般生長條件下大多數基因的轉錄。\n'
                                  '其他：σ³² 熱休克、σ³⁸（RpoS）靜止期與壓力、σ²⁸ 鞭毛、σ²⁴ 細胞外壓力。'},
}

# Ch28 第 11–15 題：配合題選項在原檔是圖片，原卷代號 (AB) 改成 (F)
MATCH28 = [
    {'k': 'A', 't': 'A class of small RNA molecules involved in gene silencing by inhibiting translation and/or promoting the degradation of particular mRNAs'},
    {'k': 'B', 't': 'A complex of RNAs and proteins involved in the splicing of mRNAs in eukaryotic cells'},
    {'k': 'C', 't': 'A DNA sequence that facilitates the expression of a given gene'},
    {'k': 'D', 't': 'Supramolecular assembly of enzymatic complexes that function in the degradation of damaged or unneeded cellular proteins'},
    {'k': 'E', 't': 'A ribozyme, part of the rRNA of the large ribosomal subunit'},
    {'k': 'F', 't': 'An RNA sequence involved in regulating the expression of certain genes, functions as a transcription terminator'},
]
for n, term in [(11, 'Spliceosome'), (12, 'Proteasome'), (13, 'Peptidyl transferase'), (14, 'Attenuator'), (15, 'miRNA')]:
    F[('ch28.txt', n)] = {**F.get(('ch28.txt', n), {}),
                          'stem': f'（題組 11–15）Match the term with the most directly related description.\n\n{term}',
                          'options': MATCH28}
F[('ch28.txt', 14)].update({'answer': ['F'], 'note': '原卷這個選項的代號是 (AB)，本站改成 (F)。',
                            'explain': 'Attenuator 是 operon leader 區的一段 RNA 序列，能形成終止子 hairpin 提早結束轉錄（如 trp operon）。'})
F[('ch28.txt', 13)]['explain'] = 'Peptidyl transferase 是 23S rRNA（大次單位）的活性，屬於 ribozyme，催化肽鍵形成。'
F[('ch28.txt', 15)]['explain'] = 'miRNA 是約 22 nt 的小 RNA，與目標 mRNA 結合後抑制轉譯或促使 mRNA 分解（gene silencing）。'

for n in (20, 21, 22, 23):
    F[('ch2425.txt', n)] = {**F.get(('ch2425.txt', n), {}), 'stem_sub': [('DNA polymerases Please', 'DNA polymerases. Please'), (' :', ':')]}
for n in (24, 25, 26):
    F[('ch2425.txt', n)] = {**F.get(('ch2425.txt', n), {}), 'stem_sub': [('the characteristics of the following statements is (A)or (B) :', 'is each statement a characteristic of (A) the leading strand or (B) the lagging strand?')]}
F[('ch2425.txt', 24)]['explain_sub'] = [('Olazaki', 'Okazaki')]

# Ch24-25 的「內切酶」其實都是指 exonuclease（外切酶）
EXO_FIX = {'ch2425.txt'}

# ------------------------------------------------------------------ 考點
TOPICS = {
    'ch12': [
        ('G protein 與 cAMP', r'G protein|GTP|GDP|adenylate|transducin|rhodopsin|Ras'),
        ('IP3／DAG／Ca²⁺', r'InsP|IP3|DAG|phosphoinositide|Ca2|nitric|cGMP'),
        ('Insulin 與 RTK', r'insulin|IRS|tyrosine kinase|growth factor'),
        ('核受體與類固醇激素', r'steroid|zinc|Glucocorticoid|thyroxine|cortisol'),
        ('激素與受體藥理', r'agonist|hypothalamus|releasing'),
    ],
    'ch22n': [
        ('Purine 合成與調控', r'purine|PRPP|IMP|胺基酸|嘌呤生合成'),
        ('Pyrimidine 合成', r'pyrimidine|嘧啶|transcarbamoylase'),
        ('Ribonucleotide reductase 與 dTMP', r'ribonucleotide reductase|dTMP|thymidylate|one-carbon|單碳'),
        ('核苷酸分解與痛風', r'uric|尿酸|gout|痛風|xanthine|aminoisobutyrate|thymine|尿素'),
        ('Salvage、Lesch-Nyhan 與 SCID', r'salvage|回收|Lesch|adenosine deaminase|免疫'),
        ('抗代謝藥物', r'5-FU|fluorouracil|methotrexate|AZT|prodrug|HIV|反轉錄'),
    ],
    'ch24': [
        ('DNA 結構與染色體', r'histone|hairpin|complementary|DNA and RNA|Operator|sequence'),
    ],
    'ch25': [
        ('DNA polymerase 種類與活性', r'polymerase I\b|polymerase III|Klenow|exonuclease|proofreading|pol [αβγδ]|polymerase.*Mitochondria|PCNA|three DNA polymerases'),
        ('Replication fork：primase、helicase、Okazaki', r'Okazaki|primase|helicase|lagging|leading|primosome|replication fork|unwinding'),
        ('複製起始與方向', r'origin|bidirection|Meselson|initiation|fashion'),
        ('Topoisomerase 與 telomerase', r'Topoisomerase|telomer|aging'),
    ],
    'ch26': [
        ('RNA polymerase 與 σ factor', r'RNA polymerase|sigma|σ|rifampicin|promoter|template|TATA|β subunit'),
        ('轉錄終止', r'termination|ρ'),
        ('mRNA 加工：cap、poly(A)、splicing', r'cap|poly\(A\)|poly A|AATAAA|splic|lariat|intron|spliceosome|Processing'),
        ('rRNA／tRNA 與 RNA 穩定性', r'rRNA|tRNA|stability|degradation'),
        ('DNA 結合蛋白與 hairpin', r'binding motif|binds to DNA|hairpin|Lys'),
    ],
    'ch28': [
        ('Lac operon 與 CRP', r'lac|CRP|glucose|operator'),
        ('Trp operon 與 attenuation', r'Attenuat|Trp|tryptophan'),
        ('真核調控：enhancer、甲基化、RNA', r'enhancer|methylation|antisense|miRNA|Coactivator|Spliceosome|Proteasome|Peptidyl'),
        ('σ factor', r'σ'),
    ],
}


def topics_for(ch, text):
    out = [t for t, rx in TOPICS.get(ch, []) if re.search(rx, text, re.I)]
    return out[:2] or ['其他']


NEG = re.compile(r'\b(NOT|not|incorrect|false|except|least)\b|錯誤|不會|不包括|最不可能|何者不|通常不')


def pattern_for(q):
    s = q['stem']
    if '題組' in s or 'Match' in s: return '配對題'
    if re.search(r'^\s*(1\.|①|I\.)|\n\s*(1\.|①|I\.)', s): return '組合選擇題'
    if NEG.search(s): return '選錯誤（否定）題'
    if re.search(r'patient|病人|病患|syndrome|癌症|愛滋|痛風', s): return '臨床情境題'
    return '選正確／單一概念題'


# Ch24-25 考古是兩章合在一起；今年課表 Ch24（W11）、Ch25（W12）分開上，依題目內容拆回去
CH24_NUMS = {1, 2, 3, 4, 7}  # DNA／RNA 結構、hairpin、histone、operator、互補股


def chapter_of(fname, n, ch):
    if fname == 'ch2425.txt':
        return 'ch24' if n in CH24_NUMS else 'ch25'
    return ch


def norm(q):
    return re.sub(r'[\s"“”]', '', (q['stem'] + '|' + '|'.join(o['t'] for o in q['options'])).lower())


out, seen = [], {}
for fname, ch, section in FILES:
    qs, ans, ex = parse(open(os.path.join(HERE, 'k113final', fname), encoding='utf-8').read())
    print(f'{fname}: {len(qs)} 題、答案 {len([n for n in qs if n in ans])}、詳解 {len([n for n in qs if n in ex])}')
    for n, r in sorted(qs.items()):
        fx = F.get((fname, n), {})
        stem = fx.get('stem', r['stem'])
        for x, y in fx.get('stem_sub', []): stem = stem.replace(x, y)
        q = {
            'id': f"k113f-{chapter_of(fname, n, ch)}-{n:02d}",
            'source': SRC,
            'section': section,
            'num': n,
            'chapter': chapter_of(fname, n, ch),
            'type': 'mcq',
            'stem': stem.strip(),
            'options': fx.get('options', r['options']),
            'answer': fx.get('answer', list(ans.get(n, ''))),
        }
        if 'explain' in fx:
            e = fx['explain']
        else:
            e = clean_explain(ex.get(n, []))
            if fname in EXO_FIX: e = e.replace('內切酶', '外切酶')
            for x, y in fx.get('explain_sub', []): e = e.replace(x, y)
            e = re.sub(r'(見|如)(下方|下|右|上)圖[。，]?', '', e).strip()
        q['explain'] = e
        if len(q['answer']) > 1:
            q['note'] = f"共筆公布的答案為 {'、'.join(q['answer'])}（複選或送分），選任一個都算對。"
        if fx.get('note'): q['note'] = fx['note']
        q['topics'] = topics_for(q['chapter'], q['stem'] + ' ' + ' '.join(o['t'] for o in q['options']))
        q['pattern'] = pattern_for(q)
        k = norm(q)
        if k in seen:  # 同一份考古重複出現：記在第一次出現的那題
            seen[k]['repeat'] = seen[k].get('repeat', 1) + 1
            continue
        seen[k] = q
        out.append(q)

bad = [q['id'] for q in out if not q['answer'] or len(q['options']) < 2 or not q['explain']]
print('總計', len(out), '題；', dict(collections.Counter(q['chapter'] for q in out)))
if bad: print('⚠️ 缺答案、選項或詳解：', bad)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
