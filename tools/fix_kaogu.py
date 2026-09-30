#!/usr/bin/env python3
"""Apply manual fixes + chapter/topic/pattern tagging to parsed 考古 questions.

Input : kaogu-raw.json (from parse_kaogu.py)
Output: ../subjects/micro-immuno/data/questions-kaogu.json
"""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
qs = json.loads((HERE / 'kaogu-raw.json').read_text(encoding='utf-8'))
byid = {q['id']: q for q in qs}

# ---------------------------------------------------------------- manual fixes
def opt(*pairs):
    return [{'k': k, 't': t} for k, t in pairs]

F = {}
F['k113-bact-05'] = dict(type='short', stem='（簡答）細菌培養的生長曲線中，應選擇哪一個時期來計算世代時間（generation time）？',
                         answer_text='指數生長期（exponential / log phase）', options=[])
F['k113-bact-07'] = dict(stem='Which of the following structures is present in prokaryotic cells?  a. 70S Ribosomes  b. Nuclear membrane  c. Cell wall  d. Diploid chromosomes  e. Plasmids  f. Mitochondria',
                         options=opt(('A', 'a＋b＋d'), ('B', 'a＋c＋e'), ('C', 'a＋d＋f'), ('D', 'b＋d＋f')))
F['k113-bact-17'] = dict(note='原答案為 (B)(C)(D) 皆可：Propionibacterium、Listeria、Corynebacterium 都是不產孢子的 G(+) 桿菌。')
F['k113-bact-34'] = dict(note='原答案為 (C) 或 (D)：(D) 的敘述「taxonomic diversity 大、功能保守（functional redundancy）」也正確。')
F['k113-tact-19'] = dict(stem='The specificity of an antibody is due to ____.',
                         options=opt(('A', 'the constant portions of the H and L chains'), ('B', 'its valence'), ('C', 'the H chains'),
                                     ('D', 'the L chains'), ('E', 'the variable portions of the H and L chains')))
F['k113-tact-21'] = dict(stem='In addition to IgG, the antibody that can fix complement is ____.',
                         options=opt(('A', 'IgG'), ('B', 'IgM'), ('C', 'IgA'), ('D', 'IgD'), ('E', 'IgE')))
F['k113-staph2-03'] = dict(key='X', note='原考古標為「X」（無正確答案）：錯誤的配對應為 ①③（見同題幹的第 19 題），本題選項中沒有 ①③，所以任何選項都不算對。', disputed=True)
F['k113-staph2-20'] = dict(type='short', stem='Staphylococcus aureus is one of the most common pathogens causing a broad-spectrum disease. (A) What are the two key features to identify this pathogen? (B) Please write one toxin produced by this pathogen and its associated disease.',
                           answer_text='(A) Catalase(+)、Coagulase(+)\n(B) 任一：Cytotoxin／組織損傷；Exfoliative toxin／燙傷樣皮膚症候群（SSSS）；Enterotoxin／食物中毒；TSST-1／毒性休克症候群', options=[])
F['k113-neis-03'] = dict(note='原答案為 (B)(C) 皆錯：Salmonella 需約 10⁵ CFU 才致病（<100 CFU 是 Shigella）；HUS 是 EHEC 而非 UPEC。')
F['k113-fungi-53'] = dict(note='原答案 (A) 或 (B)：單細胞真菌（酵母）以出芽（budding）或分裂（fission）繁殖。')
F['k113-fungi-61'] = dict(type='short', answer_text='Fungi are eukaryotic organisms with a rigid cell wall composed of chitin and glucan, and a cell membrane in which ergosterol replaces cholesterol as the major sterol.', options=[])
F['k113-fungi-62'] = dict(type='short', answer_text='Candidiasis：Candida spp. 造成的各種感染（黏膜、皮膚、臟器）。\nCandidemia：Candida 進入血流造成的菌血症（blood stream infection）。', options=[])
F['k113-fungi-63'] = dict(type='short', answer_text='由 Sporothrix schenckii（溫度雙型性真菌）經刺傷引起的皮下感染，沿淋巴管擴散形成一連串結節與潰瘍。', options=[])
F['k113-mid111-04'] = dict(stem='下列有關細菌構造與功能的配對，何者錯誤？（原題幹誤植為「關於 Koch 的敘述」）')
F['k113-mid111-76'] = dict(explain='超級抗原不需要 APC 處理，直接跨接 MHC II 與 TCR Vβ，非專一性活化大量 T 細胞 → 細胞激素風暴。')
F['k113-tact-37'] = dict(explain='CD4 T 細胞（TFH）提供 CD40L 與細胞激素，B 細胞才能進行 class switch 與 affinity maturation。（同第 2 題）')

F['k113-tact-11'] = dict(key='C', note='原考古答案表為 (D)，但詳解與共筆 cytokine 表皆為 IL-5 → IgA（及小鼠 IgG1），故本站以 (C) 為答案。')
F['k113-entero-06'] = dict(note='原詳解開頭誤植為 (D)，依內容 Salmonella 有鞭毛，錯誤敘述為 (A)。')

# picture-dependent questions: keep out of practice pool
IMAGE_ONLY = {'k113-fungi-03', 'k113-fungi-06', 'k113-fungi-08', 'k113-fungi-09', 'k113-fungi-10',
              'k113-fungi-17', 'k113-fungi-18', 'k113-fungi-20', 'k113-fungi-28', 'k113-fungi-31'}

# --------------------------------------------------------------- chapter map
def chapter_for(q):
    s, n = q['section'], q['num']
    text = q['stem'] + ' ' + ' '.join(o['t'] for o in q['options'])
    if s == 'bact':
        if n in (12, 17, 18): return 'bacillus'
        if n in (37, 38, 51): return 'sterilization'
        if re.search(r'DNA|gene|mutation|operon|repress|conjugat|transduc|transform|transpos|nucleotide|Genetic changes|複製', text, re.I):
            return 'bact-genetics'
        return 'bact-structure'
    if s == 'innate':
        if n in (45, 52): return 'agab'
        return 'innate'
    if s == 'agab':
        if n == 10: return 'mhc'
        if n == 19: return 'tcell-dev'
        return 'agab'
    if s == 'tdev':
        return 'mhc' if n in (3, 4, 6, 12, 13) else 'tcell-dev'
    if s == 'tact':
        if n in (36, 39): return 'tcell-dev'  # CTLA-4 / CD28：9/30 上課內容
        if n in (18, 27): return 'mhc'
        if n in (24, 25, 28): return 'innate'
        if n == 16: return 'innate'
        if n in (19, 20, 21, 22, 23, 26, 29, 30, 31, 32, 34): return 'agab'
        return 'tcell-act'
    if s in ('staph1', 'staph2'): return 'staph-strep'
    if s == 'entero': return 'enterobacteriaceae'
    if s == 'bacillus': return 'bacillus'
    if s == 'neis':
        if n in (2, 3, 4, 5): return 'enterobacteriaceae'
        if n == 13: return 'bacillus'
        return 'neisseria'
    if s == 'fungi': return 'fungi'
    if s == 'mid111':
        if n in (8, 11, 12, 13): return 'bact-genetics'
        if n <= 13: return 'bact-structure'
        if n <= 17: return 'sterilization'
        if n <= 21 or n == 76: return 'pathogenesis'
        if n <= 29: return 'staph-strep'
        if n == 36: return 'neisseria'
        if n <= 35: return 'enterobacteriaceae'
        if n <= 38: return 'bacillus'
        if n <= 43: return 'fungi'
        if n in (44, 59, 60, 61, 62, 63): return 'agab'
        if n in (45, 54, 55, 56, 57, 58): return 'innate'
        if n in (46, 47): return 'immuno-basic'
        if n <= 53: return 'tcell-act'
        if n <= 70: return 'hypersensitivity'
        if n == 75: return 'mhc'
        return 'tcell-dev'
    raise ValueError(q['id'])

# ----------------------------------------------------------------- topic tags
TOPICS = [
    # bacteria basics
    ('微生物學史／柯霍假說', r'Koch|Pasteur|Fleming|Ehrlich|Jenner|Penicillin 的|柯霍|germ theory|spontaneous generation|Semmelweis|1928'),
    ('人體微生物相', r'microbiota|microbiome|dysbiosis|菌相'),
    ('細胞壁／革蘭氏染色', r'peptidoglycan|teichoic|cell wall|gram[- ]?(negative|positive)|革蘭|格蘭|葛蘭|lipid A|LPS|lipopolysaccharide|porin|periplasm|Lysozyme|Murein|cross-link|outer membrane|O-antigen|O antigen'),
    ('細菌構造與功能', r'fimbriae|pili|pilus|flagell|capsule|inclusion|nucleoid|plasmid|ribosome|organelle|structure'),
    ('孢子', r'spore|孢子'),
    ('生長曲線與代謝', r'growth|phase|ATP|phosphorylation|oxygen|需氧|生長|metabol'),
    ('細菌分類鑑定', r'identification|classif|typing|phenotype|表現型|size|diameter'),
    ('DNA 複製與基因表現', r'replicat|複製|operon|repress|expression|調控|translat'),
    ('突變', r'mutation|deletion|nucleotide|突變|核苷酸'),
    ('水平基因轉移', r'conjugat|transduc|transformation|transpos|水平|Genetic changes'),
    ('滅菌與消毒', r'steril|disinfect|滅菌|消毒|殺菌|UV|radiation|autoclave|glutaraldehyde|戊二醛|酒精|alcohol|biguanide|chlorhexidine|Supercritical|ETO|紗布|Pasteur'),
    ('毒素（內/外毒素、AB toxin）', r'toxin|毒素|endotoxin'),
    ('超級抗原', r'superantigen|超級抗原'),
    ('免疫逃脫', r'逃避|evade|evasion|escape'),
    # immunology
    ('先天 vs 後天免疫', r'innate immunity 的成員|先天性免疫系統不包括|adaptive|適應性免疫|innate immunity'),
    ('白血球遷移（selectin→chemokine→integrin）', r'selectin|integrin|chemokine|migration|趨化|黏附|CCR|VLA|LFA|CR3|CR4'),
    ('補體系統', r'complement|補體|C3|C4b|C5|MAC|MBL|convertase|lectin pathway|Factor [BD]'),
    ('TLR／PRR', r'TLR|Toll|CD14|PAMP'),
    ('調理作用／opsonic receptor', r'opson|調理'),
    ('NK 細胞與抑制性受體', r'NK|KIR|CD94|NKG2|HLA-E|HLA-C|natural killer|自然殺手'),
    ('細胞毒殺（perforin/Fas）', r'perforin|granzyme|FasL|Fas ligand|cytotoxic|毒殺'),
    ('ILC 先天性淋巴細胞', r'innate lymphoid|ILC'),
    ('抗體類別與功能', r'IgG|IgM|IgA|IgE|IgD|isotype|immunoglobulin class'),
    ('抗體結構', r'hinge|light chain|heavy chain|Fab|Fc |Fc$|Fc 部分|J chain|domain|disulfide|secretory component|分泌片段|poly Ig'),
    ('抗體多樣性（VDJ/SHM）', r'diversity|多變|多樣|somatic|junctional|VDJ|V-J|V-D-J|RAG|TdT|CDR|allelic|recombination|gene conversion|rearrangement|Junctional'),
    ('抗原／epitope', r'epitope|抗原上|antigen receptor|抗原受體|hapten'),
    ('MHC 構造與表現', r'MHC|HLA|β2|polymorphism'),
    ('抗原處理與呈現（TAP）', r'TAP|proteasome|內生性|endoplasmic|ER|抗原呈現|present'),
    ('胸腺選擇', r'selection|thymic|胸腺|self-tolerance|自我耐受'),
    ('TCR 與 γδ T 細胞', r'TCR|T cell receptor|γδ|CD3'),
    ('共刺激（CD28/B7/CTLA-4）', r'CD28|B7|CTLA-4|second message|第二'),
    ('TH 分化與細胞激素', r'TH1|TH2|Th1|Th2|TH17|IL-\d+|IL\d+|IFN|TGF|細胞激素|cytokine|interferon|TFH|Treg|調節型'),
    ('B 細胞活化／class switch／生發中心', r'class switch|isotype switch|germinal|affinity maturation|hyper-IgM|CD40|TD 抗原|TI 抗原|thymus-dependent'),
    ('過敏反應', r'過敏|hypersensitivity|allerg|Arthus|RhD|肉芽腫|Granuloma'),
    # bacteria species
    ('S. aureus', r'aureus|金黃|coagulase|Protein A|TSST|凝固酶'),
    ('S. pyogenes (GAS)', r'pyogenes|Group A|GAS|scarlet|猩紅|M protein|M-Protein|Streptolysin|rheumatic|glomerulonephritis|化膿性'),
    ('S. pneumoniae', r'pneumoniae|Pneumococc|optochin|肺炎鏈球菌'),
    ('S. agalactiae (GBS)', r'agalactiae|Group B|GBS|CAMP|無乳'),
    ('Enterococcus／Viridans', r'Enterococc|faecalis|faecium|Viridans|mitis|mutans|腸球菌'),
    ('E. coli 致病型', r'E\. ?coli|ETEC|EHEC|EPEC|EIEC|EAEC|UPEC|大腸桿菌|HUS'),
    ('Salmonella', r'Salmonella|沙門|Widal|typhi'),
    ('Shigella', r'Shigella|志賀'),
    ('Yersinia／plague', r'Yersinia|plague|鼠疫|耶'),
    ('Vibrio', r'Vibrio|弧菌|cholera'),
    ('Bacillus anthracis', r'anthracis|anthrax|炭疽|Protective antigen|Edema|Lethal'),
    ('Bacillus cereus', r'cereus|fried rice|炒飯|Rice'),
    ('Listeria', r'Listeria|李斯特'),
    ('C. diphtheriae', r'diphther|白喉|DPT|Elek'),
    ('Neisseria', r'Neisseria|gonorrh|mening|淋病'),
    ('H. pylori／Campylobacter', r'Helicobacter|pylori|Campylobacter|urease|Guillain'),
    ('Pseudomonas', r'Pseudomonas|pyocyanin|綠膿'),
    ('真菌構造與分類', r'hyphae|septate|coenocytic|Zygomy|Ascomy|Basidio|chitin|glucan|ergosterol|dimorph|兩型|雙型|anamorph|clamp|菌絲|真菌|yeast|酵母|Amastigo'),
    ('Cryptococcus／Candida', r'Cryptococcus|Candida|隱球菌|念珠菌|Germ-tube|India'),
    ('皮膚／皮下／系統性黴菌', r'Sporothrix|Trichophyton|Epidermophyton|Microsporum|Histoplasma|Penicillium|marneffei|孢絲菌|癬'),
    ('抗真菌藥物', r'azole|Amphotericin|Echinocandin|Terbinafine|Flucytosine|Polyene|butenafine'),
]
TOPIC_RE = [(name, re.compile(rx, re.I)) for name, rx in TOPICS]

# which topics are allowed in which chapter (keeps tags meaningful)
CH_TOPICS = {
    'bact-structure': ['微生物學史／柯霍假說', '人體微生物相', '細胞壁／革蘭氏染色', '細菌構造與功能', '孢子', '生長曲線與代謝', '細菌分類鑑定'],
    'bact-genetics': ['DNA 複製與基因表現', '突變', '水平基因轉移', '細菌構造與功能'],
    'sterilization': ['滅菌與消毒'],
    'pathogenesis': ['毒素（內/外毒素、AB toxin）', '超級抗原', '免疫逃脫', '細胞壁／革蘭氏染色'],
    'immuno-basic': ['先天 vs 後天免疫', 'TH 分化與細胞激素', '共刺激（CD28/B7/CTLA-4）'],
    'innate': ['補體系統', 'TLR／PRR', 'NK 細胞與抑制性受體', '白血球遷移（selectin→chemokine→integrin）', '調理作用／opsonic receptor', '細胞毒殺（perforin/Fas）', 'ILC 先天性淋巴細胞', '先天 vs 後天免疫', 'MHC 構造與表現'],
    'agab': ['抗體類別與功能', '抗體結構', '抗體多樣性（VDJ/SHM）', '抗原／epitope'],
    'mhc': ['MHC 構造與表現', '抗原處理與呈現（TAP）'],
    'tcell-dev': ['胸腺選擇', 'TCR 與 γδ T 細胞', '共刺激（CD28/B7/CTLA-4）', 'MHC 構造與表現'],
    'tcell-act': ['TH 分化與細胞激素', '共刺激（CD28/B7/CTLA-4）', 'B 細胞活化／class switch／生發中心', '細胞毒殺（perforin/Fas）', '白血球遷移（selectin→chemokine→integrin）'],
    'hypersensitivity': ['過敏反應'],
    'staph-strep': ['S. aureus', 'S. pyogenes (GAS)', 'S. pneumoniae', 'S. agalactiae (GBS)', 'Enterococcus／Viridans'],
    'enterobacteriaceae': ['E. coli 致病型', 'Salmonella', 'Shigella', 'Yersinia／plague', 'Vibrio', '毒素（內/外毒素、AB toxin）', '細胞壁／革蘭氏染色'],
    'bacillus': ['Bacillus anthracis', 'Bacillus cereus', 'Listeria', 'C. diphtheriae', '孢子'],
    'neisseria': ['Neisseria', 'H. pylori／Campylobacter', 'Pseudomonas', 'Vibrio'],
    'fungi': ['真菌構造與分類', 'Cryptococcus／Candida', '皮膚／皮下／系統性黴菌', '抗真菌藥物'],
}


def topics_for(q, ch):
    text = q['stem'] + ' ' + ' '.join(o['t'] for o in q['options'])
    allowed = CH_TOPICS.get(ch, [])
    hits = [name for name, rx in TOPIC_RE if name in allowed and rx.search(text)]
    return hits[:3] or ['其他']


TOPIC_OVERRIDE = {
    'k113-bact-05': ['生長曲線與代謝'], 'k113-bact-06': ['微生物學史／柯霍假說'], 'k113-bact-19': ['細菌分類鑑定'],
    'k113-bact-24': ['細菌分類鑑定'], 'k113-agab-28': ['抗體類別與功能'], 'k113-tdev-09': ['TCR 與 γδ T 細胞'],
    'k113-tdev-11': ['胸腺選擇'], 'k113-tact-12': ['B 細胞活化／class switch／生發中心'], 'k113-tact-19': ['抗體結構'],
    'k113-staph2-05': ['S. aureus'], 'k113-staph2-15': ['S. pyogenes (GAS)'], 'k113-entero-16': ['Salmonella'],
    'k113-entero-19': ['E. coli 致病型'], 'k113-neis-01': ['Neisseria'], 'k113-fungi-16': ['真菌構造與分類'],
    'k113-fungi-19': ['真菌構造與分類'], 'k113-fungi-61': ['真菌構造與分類'], 'k113-fungi-62': ['Cryptococcus／Candida'],
    'k113-fungi-63': ['皮膚／皮下／系統性黴菌'], 'k113-mid111-01': ['微生物學史／柯霍假說'], 'k113-mid111-41': ['真菌構造與分類'],
    'k113-mid111-47': ['先天 vs 後天免疫'],
}


def pattern_for(q):
    s = q['stem']
    if q.get('type') == 'short': return '簡答題'
    if re.search(r'year-old|歲|病人|患者|產婦|patient|男童|小姐|男士|學童|女孩|hospitali', s, re.I): return '臨床情境題'
    if re.search(r'①|\ba\.\s|\(1\)|\(a\)', s): return '組合選擇題'
    if re.search(r'pair|配對|－|−|—|link between|match', s, re.I): return '配對題'
    if re.search(r'not|false|incorrect|except|wrong|錯誤|不正確|不包括|不是|不屬於|無法|並非|最不|沒有直接|與其他不同|不符合|不可以', s, re.I): return '選錯誤（否定）題'
    return '選正確／單一概念題'


BULLET = re.compile(r'^\s*(\(?[A-Ea-e0-9]{1,2}[)）.]|[＊*⚫♦◆•\-]|註|[①②③④⑤]|[^：:。，,（(]{1,25}[：:]|Step|[IVX]+\.|【|〔|\d+\.|[a-z]\.|[A-Z]\.)')


def unwrap(text):
    lines = [l.rstrip() for l in text.split('\n')]
    out = []
    for l in lines:
        if not l.strip():
            continue
        if out and not BULLET.match(l):
            prev = out[-1]
            sep = ' ' if re.search(r'[A-Za-z0-9,.)]$', prev) and re.match(r'\s*[A-Za-z0-9(]', l) else ''
            out[-1] = prev + sep + l.strip()
        else:
            out.append(l.strip())
    return '\n'.join(out)


out = []
for q in qs:
    qid = q['id']
    fx = F.get(qid, {})
    q.update({k: v for k, v in fx.items()})
    if qid in IMAGE_ONLY:
        q['imageOnly'] = True
    key = q.get('key') or ''
    ans = re.findall(r'[A-E]', key) if key not in ('X', '見詳解') else []
    ex = q.get('explain', '') or ''
    first, _, rest = ex.strip().partition('\n')
    if re.fullmatch(r'\s*((\([A-E]\)|X)\s*((or|/)\s*)?)+\s*', first):
        ex = rest
    else:
        ex = ex.strip()
    ex = unwrap(ex)
    ch = chapter_for(q)
    rec = {
        'id': qid,
        'source': '113 考古' if q['section'] != 'mid111' else '111 期中考古',
        'section': q['sectionTitle'],
        'num': q['num'],
        'chapter': ch,
        'type': q.get('type', 'mcq'),
        'stem': q['stem'],
        'options': q['options'],
        'answer': ans,
        'explain': ex,
    }
    if q.get('answer_text'): rec['answerText'] = q['answer_text']
    if q.get('note'): rec['note'] = q['note']
    if q.get('disputed'): rec['disputed'] = True
    if q.get('imageOnly'): rec['imageOnly'] = True
    rec['topics'] = TOPIC_OVERRIDE.get(qid) or topics_for(q, ch)
    rec['pattern'] = pattern_for(q)
    out.append(rec)

dst = HERE.parent / 'subjects' / 'micro-immuno' / 'data' / 'questions-kaogu.json'
dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')

from collections import Counter
print('total', len(out), 'imageOnly', sum(1 for r in out if r.get('imageOnly')))
print(Counter(r['chapter'] for r in out))
print(Counter(r['pattern'] for r in out))
others = [r['id'] for r in out if r['topics'] == ['其他']]
print('untagged', len(others), others[:40])
