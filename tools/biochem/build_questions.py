"""生化題庫：把 gongbi-raw.json 清理、校正、去重、標考點，輸出到 subjects/biochem/data/。
用法：python3 tools/biochem/parse_gongbi.py && python3 tools/biochem/build_questions.py
"""
import json, os, re, collections

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(ROOT, 'subjects', 'biochem', 'data')
SRC = '113 共筆考古'

raw = json.load(open(os.path.join(HERE, 'gongbi-raw.json'), encoding='utf-8'))

# ------------------------------------------------------------------ 章節重新歸類
MOVE = {
    ('17-2', 13): 'ch21', ('17-2', 14): 'ch21', ('17-2', 15): 'ch21', ('17-2', 19): 'ch21',
    ('17-2', 21): 'ch21', ('17-2', 26): 'ch21', ('17-2', 27): 'ch21',
    ('21', 14): 'ch12',
}

# ------------------------------------------------------------------ 人工校正
# key: (tag, num) → 要覆寫的欄位；explain 為 None 表示保留清理後的原詳解
F = {
    ('17-2', 4): {'explain_sub': [('即 PLP，又稱 Vitamin B6，是轉胺酶和肝糖磷酸水解酶的輔酶。', '')]},
    ('17-2', 13): {'explain_sub': [('或是直接下圖背起來，沒有 NADH！', '記法：脂肪酸合成只用 NADPH，沒有 NADH。'), ('或是直 接 下圖背起來，沒有 NADH！', '記法：脂肪酸合成只用 NADPH，沒有 NADH。')]},
    ('17-2', 15): {'explain_sub': [('（老師影片沒提到）', '')]},
    ('17-2', 16): {'explain_sub': [('詳見Ch17 PPT p.18。', ''), ('詳見 Ch17 PPT p.18。', '')]},
    ('17-2', 17): {'explain_sub': [('（詳見第 13 題的附圖，非常重要，背起來）', '（非常重要，背起來）')]},
    ('17-2', 20): {'explain_sub': [('，如右圖紅色方框標示處', '')]},
    ('17-2', 26): {'explain': '(A) 錯誤：trans-Δ²-enoyl 硫酯（crotonyl）在 β-oxidation（去氫後）和脂肪酸合成（脫水後）兩邊都會出現，兩者都是反式。\n'
                              '(B) 正確：合成路徑的中間物是 D-β-hydroxyacyl-ACP；β-oxidation 的中間物是 L-β-hydroxyacyl-CoA。\n'
                              '(C) 錯誤：β-oxidation 除了 NAD⁺ 還用 FAD。\n'
                              '(D) 錯誤：β-oxidation 在粒線體、脂肪酸合成在細胞質，正好相反。'},
    ('21', 6): {'explain_sub': [('（參見 ch19 PPT 第四頁）', '')]},
    ('21', 7): {'explain_sub': [('（可參考第四題詳解附圖）', ''), ('（可參考 第四題詳解附圖）', '')]},
    ('21', 9): {'explain': 'Tay-Sachs disease：溶體的 β-N-acetylhexosaminidase A（hexosaminidase A）缺乏 → GM2 ganglioside 堆積（神經退化、櫻桃紅斑）。\n'
                           '對照：Niemann-Pick＝sphingomyelinase → sphingomyelin；Fabry＝α-galactosidase A → globotriaosylceramide；Gaucher＝β-glucosidase → glucocerebroside。'},
    ('18', 18): {'answer': [], 'note': '共筆標「X」：四個選項（catecholamine 的 DOPA decarboxylase、polyamine 的 ornithine decarboxylase、轉硫作用、heme 合成的 ALA synthase）都需要 PLP，本題沒有正確答案。'},
    ('18', 34): {'explain': '五個反應都有脫羧（decarboxylation）：\n(1) Glutamate → GABA：glutamate decarboxylase\n(2) Histidine → histamine：histidine decarboxylase\n'
                            '(3) DOPA → dopamine：aromatic L-amino acid decarboxylase\n(4) Ornithine → putrescine（ornithine decarboxylase）→ spermidine\n(5) Cysteine → … → cysteine sulfinate → hypotaurine（cysteine sulfinate decarboxylase）→ taurine\n以上都需要 PLP。'},
    ('18', 36): {'explain': '九種必需胺基酸：His、Ile、Leu、Lys、Met、Phe、Thr、Trp、Val（兒童另需 Arg）；老師的口訣是「3T2LIP + HMV」。Proline 不在其中，是非必需胺基酸（由 glutamate 經 glutamate-γ-semialdehyde 合成）。'},
    ('18', 38): {'explain': 'Glycine 直接參與：purine 環（C4、C5、N7）、δ-aminolevulinic acid（ALA synthase：glycine + succinyl-CoA）、膽鹽（glycocholate＝bile acid + glycine）、creatine、glutathione。\n'
                            'Cysteine 的碳骨架來自 serine、硫來自 methionine（轉硫作用），不是由 glycine 直接生成。'},
    ('18', 39): {'explain_sub': [('，下圖為 phycocyanin 的結構，最左邊那個環沒有芳香環的共振結構', '；phycocyanin 的發色團（phycocyanobilin）是開鏈的 tetrapyrrole，沒有封閉的 porphyrin 環'), ('，下圖為 phycocyanin 的結 構，最左邊那個環沒有芳香環的共振結構', '；phycocyanin 的發色團（phycocyanobilin）是開鏈的 tetrapyrrole，沒有封閉的 porphyrin 環')]},
    ('18', 44): {'explain': '(A) Alanine 只靠轉胺（ALT，需 PLP）變成 pyruvate，不需要 THF。\n(B) N⁵,N¹⁰-methylene-THF：serine ⇌ glycine；glycine cleavage 也需要 THF。\n'
                            '(C) N⁵-methyl-THF（加 B₁₂）：homocysteine → methionine。\n(D) Histidine → FIGLU → glutamate，需要 THF 接走 formimino 基。'},
    ('18', 60): {'explain_sub': [('下圖為 glucose-alanine cycle。', 'Glucose-alanine cycle：')]},
    ('18', 80): {'options': [{'k': 'A', 't': 'Decarboxylation'}, {'k': 'B', 't': 'Transsulfuration'},
                             {'k': 'C', 't': 'Transamination'}, {'k': 'D', 't': 'Racemization'}]},
    ('18', 82): {'explain': '3-Phosphoglycerate →（3-phosphoglycerate dehydrogenase）→ 3-phosphohydroxypyruvate →（轉胺）→ 3-phosphoserine →（phosphatase）→ Serine。\n'
                            'Serine 再生成 glycine（serine hydroxymethyltransferase，需 THF）與 cysteine（轉硫作用，加 homocysteine 的硫）。'},
    ('18', 84): {'explain_sub': [('如圖，', '')]},
    ('22', 1): {'imageOnly': True, 'note': '原題四個選項都是化學結構圖，本站未收錄。PRPP＝5-phosphoribosyl-1-pyrophosphate：ribose-5-phosphate 的 C1 接上 pyrophosphate（α 構型）。'},
    ('22', 2): {'explain_sub': [('（圖引用百八共筆）', '')]},
    ('22', 8): {'stem': 'The following molecule, 5-fluorodeoxyuridylate (FdUMP), is an irreversible inhibitor of which enzyme of nucleotide metabolism?',
                'note': '原題附 FdUMP 結構圖，本站改以文字標出分子名稱。',
                'explain': 'FdUMP（5-FU 的活性代謝物）是 thymidylate synthase 的自殺性抑制劑：與酵素和 N⁵,N¹⁰-methylene-THF 形成共價複合物 → dTMP 無法合成 → 快速分裂細胞停止 DNA 合成。'},
    ('22', 28): {'explain': 'dUMP → dTMP 由 thymidylate synthase 催化，甲基來自 N⁵,N¹⁰-methylene-THF（之後變成 DHF），再由 dihydrofolate reductase 把 DHF 還原回 THF。\n'
                            'Thymidine kinase 是 salvage pathway（thymidine → dTMP）的酵素，不是 de novo 由 dUMP 合成 dTMP 所需。'},
    ('22', 36): {'explain_sub': [('參考右圖：', '')]},
    ('22', 38): {'answer': [], 'note': '共筆標「X」：四個選項都不正確。SCID（ADA 缺乏）→ dATP 堆積 → 抑制 ribonucleotide reductase（不是 DNA polymerase），與尿酸、xanthine dehydrogenase 無關。'},
    ('22', 40): {'explain': 'dUMP + N⁵,N¹⁰-methylene-THF →（thymidylate synthase）→ dTMP + DHF。\n(A) thymidine kinase 屬於 salvage pathway；(C) ribonucleotide reductase 負責 NDP → dNDP；(D) dTMP 是產物。'},
    ('22', 43): {'explain_sub': [('（如下左圖）', '')]},
    ('22', 45): {'explain': 'Dihydrofolate reductase（DHFR）抑制劑：aminopterin、methotrexate（抗癌）、trimethoprim（細菌 DHFR，抗菌）、pemetrexed。\n'
                            'AZT 抑制反轉錄酶；5-fluorouracil 抑制 thymidylate synthase；allopurinol 抑制 xanthine oxidase。'},
}

# ------------------------------------------------------------------ 考點
TOPICS = {
    'ch17': [
        ('脂蛋白與膽固醇恆定', r'lipoprotein|LDL|HDL|VLDL|chylomicron|apo|hypercholesterol|atheroscler|foam|cholesterol'),
        ('脂肪動員與運輸', r'albumin|lipase|glycerol|bloodstream|epinephrine|mobiliz|bile|dietary'),
        ('Carnitine shuttle', r'carrier to take|carnitine|mitochondri.* membrane|into the mitochondria|acyltransferase'),
        ('β-oxidation 與 ATP 計算', r'β-oxidation|beta-oxidation|ATP|palmit|lauric|FADH|water|thio'),
        ('奇數碳與 propionyl-CoA', r'propionyl|odd|B12|methylmalonyl|cobalamin|14C'),
        ('酮體', r'ketone|acetoacet|hydroxybutyr'),
    ],
    'ch21': [
        ('脂肪酸合成與 ACC', r'synthesis of fatty acids|palmitate biosynthesis|fatty acid synthesis|malonyl|acetyl-CoA carboxylase|rate-limiting|palmitate biosynthesis|carrier to the Acetyl-CoA|Acetyl-CoA from the mitochondrion'),
        ('合成 vs 分解比較', r'comparing|biosynthesis with β-oxidation'),
        ('必需脂肪酸', r'linoleate|plants but NOT'),
        ('Eicosanoids 與 NSAIDs', r'eicosanoid|prostaglandin|thromboxane|leukotriene|aspirin|ibuprofen|arachidon|COX'),
        ('磷脂質合成', r'phospholipid is produced|phosphatidyl|CDP|choline|methyl group donor|Phospholipids are synthesized'),
        ('鞘脂與溶體疾病', r'Tay-Sachs|ganglioside|sphingo|Niemann|Gaucher|Fabry'),
        ('膽固醇合成與 HMG-CoA reductase', r'HMG-CoA|cholesterol|statin|steroid|Prostacyclin|derivate'),
    ],
    'ch12': [
        ('IP3／DAG／Ca²⁺', r'InsP3|IP3|DAG|Ca2'),
    ],
    'ch23': [
        ('胰島素與 GLUT', r'insulin|Insulin|GLUT|IRS|GSK'),
        ('升糖素、腎上腺素與 cAMP', r'glucagon|Glucagon|epinephrine|Epinephrine|cAMP|phosphorylase'),
        ('瘦素與脂肪激素', r'leptin|Leptin|adiponectin|ADIPOQ|ghrelin|Grelin|Prader'),
        ('飢餓與糖尿病', r'starvation|diabetes|Diabetes|fasting|ketone'),
        ('Cori／葡萄糖-丙胺酸循環', r'Cori|lactate|Lactate|alanine'),
        ('各器官燃料代謝', r'organ|brain|Brain|muscle|liver|blood cells|fuel|creatine|Glycerol kinase|Glucose-6-phosphate'),
        ('AMPK／輔酶', r'AMPK|AMP-activated|pyridoxal'),
    ],
    'ch18': [
        ('尿素循環', r'urea|Urea|carbamoyl|ornithine|Ornithine|citrulline|argininosuccinate|N-acetylglutamate'),
        ('轉胺與 PLP', r'[Tt]ransamination|[Pp]yridoxal|aminotransferase|oxidative deamination'),
        ('胺基氮運輸（Gln／Ala）', r'[Gg]lutamine|glucose-alanine|amino group to be catabolized|Glutamate turns'),
        ('先天胺基酸代謝疾病', r'phenylketonuria|Phenylketo|PKU|maple syrup|Alkaptonuria|Albinism|Homocystinuria|methylmalonic'),
        ('一碳單位與輔酶（THF／BH4／B12）', r'[Tt]etrahydrofolate|THF|[Tt]etrahydrobiopterin|THB|B12|vitamin|Vitamin|pellagra|biotin|Biotin|S-adenosyl'),
        ('生酮／生醣胺基酸', r'ketogenic|glucogenic|Oxaloacetate|essential'),
        ('胺基酸衍生物', r'tyrosine metabolism|derivative|derivate|derived|hormone|catecholamine|Catecholamine|nitric oxide|glutathione|Decarboxylation|polyamine|creatine|shikimic|3-phosphoglycerate'),
        ('Heme 與膽紅素', r'heme|Heme|porphyrin|bilirubin|Bilirubin'),
        ('蛋白質消化與泛素', r'Trypsin|Chymotrypsin|ubiquitin|peptide'),
    ],
    'ch22': [
        ('核苷酸結構', r'structure is not involved|correct structure'),
        ('Purine 合成與調控', r'PRPP|IMP|purinosome|purine synthesis|purine ring|GMP synthesis|Glycine, Glutamate|amino acids is involved'),
        ('Pyrimidine 合成', r'pyrimidine|ATCase|carbamoyl'),
        ('Ribonucleotide reductase 與 dTMP', r'ribonucleotide reduc|Ribonucleotide reduc|dTMP|thymidylate|dUMP'),
        ('核苷酸分解與痛風', r'xanthine|Xanthine|uric|gout|Gout|allopurinol|metabolic product|β-Alanine|succinyl-CoA'),
        ('Salvage、Lesch-Nyhan 與 SCID', r'salvage|Lesch|SCID|HGPRT|deaminase|immune system'),
        ('抗代謝藥物', r'AZT|prodrug|drug|5-fluoro|methotrexate|Methotrexate|Aminopterin|Ganciclovir|FdUMP'),
    ],
}

def topics_for(ch, text):
    out = [t for t, rx in TOPICS.get(ch, []) if re.search(rx, text, re.I)]
    return out[:2] or ['其他']

NEG = re.compile(r'\b(NOT|not|incorrect|cannot|could not|does not|do not|dose not|except|EXCEPT|least)\b|錯誤|不適當|不是|不屬於|無關|不會|何者不|最不')

def pattern_for(q):
    s = q['stem']
    if re.search(r'pair|vs\.', s): return '配對題'
    if re.search(r'\(1\)|^\s*1\.|\n1\.|\b1\. ', s) or all(re.match(r'^[\d,() and]+(only)?$', o['t'].replace(' ', '')) for o in q['options'] if o['t']) and q['options']:
        return '組合選擇題'
    if re.search(r'how many|ATP yield|net yield|How many', s): return '計算題'
    if NEG.search(s): return '選錯誤（否定）題'
    if re.search(r'patient|Dr\.|individuals|disease|syndrome|diabetic|starvation', s): return '臨床情境題'
    return '選正確／單一概念題'

# ------------------------------------------------------------------ 清理詳解
def clean_explain(text, answer):
    lines = [l.strip() for l in text.split('\n')]
    # 第一行若只剩答案記號就去掉
    if lines and re.fullmatch(r'(\([A-EX]\))+', lines[0].replace(' ', '')):
        lines = lines[1:]
    out = []
    for l in lines:
        if not l: continue
        starts_new = re.match(r'^(\([A-E1-9]\)|〈|（以下|[1-9]\.|\(\d\)|[①-⑩]|Transamination|根據|題目|補充)', l)
        if out and not starts_new:
            prev = out[-1]
            sep = ' ' if re.search(r'[A-Za-z0-9,.)]$', prev) and re.match(r'^[A-Za-z0-9(]', l) else ''
            out[-1] = prev + sep + l
        else:
            out.append(l)
    s = '\n'.join(out)
    s = re.sub(r'\s*詳見老師\s*PPT（[^）]*）', '', s)
    s = re.sub(r'(?<=[一-鿿，。、）])\s+(?=[一-鿿，。、（])', '', s)
    s = s.replace('（以下保留之前的詳解：）', '').strip()
    return s

# ------------------------------------------------------------------ 主程式
def norm(q):
    return re.sub(r'[\s"“”]', '', (q['stem'] + '|' + '|'.join(o['t'] for o in q['options'])).lower())


# ── 第二輪校對（獨立審閱後的更正）：與 F 合併 ──
F2 = {
    # 答案更正
    ('18', 14): {'answer': ['A'], 'note': '共筆原標 D；MSUD 是 branched-chain α-keto acid dehydrogenase（氧化脫羧）缺陷，依課本更正為 A。',
                 'explain': 'Maple syrup urine disease：branched-chain α-keto acid dehydrogenase complex 缺陷 → Leu、Ile、Val 轉胺後的 α-keto acid 無法氧化脫羧 → 堆積在血液與尿液（楓糖漿味）。'},
    ('21', 11): {'stem': 'How is the activity of HMG-CoA reductase reduced?',
                 'answer': ['B'], 'note': '共筆原標 A；膽固醇不是 HMG-CoA reductase 的別構抑制劑，依課本（及第 21-15 題）更正為 B。題幹原文 retraced 應為 reduced。'},
    # 兩個選項都說得通
    ('22', 6): {'answer': ['B', 'D'], 'note': '共筆答案為 B；但 D 也不正確（ribonucleotide reductase 是自由基機制，不是單純的 hydride transfer），選 B 或 D 都算對。'},
    ('17-2', 22): {'answer': ['B', 'C'], 'note': '共筆答案為 C。活化時用掉 1 個 ATP（變成 AMP + PPi），相當於 2 個高能磷酸鍵；「1 ATP」或「2 ATP」兩種說法課本都有，選 B 或 C 都算對。'},
    ('17-2', 27): {'note': 'OAA 送回粒線體的經典路線還有 malate →（malic enzyme，產生 NADPH）→ pyruvate →（pyruvate carboxylase）→ OAA；共筆以最短的三個酵素為答案。'},
    ('18', 39): {'answer': ['A', 'B'], 'note': '共筆答案為 B；嚴格來說 cobalamin 是 corrin 環，也不是 porphyrin，選 A 或 B 都算對。',
                 'explain': '含 porphyrin 環：heme、chlorophyll。Cobalamin（B₁₂）是 corrin 環（少一個 methine 橋）；phycocyanin 的發色團（phycocyanobilin）是開鏈的 tetrapyrrole，沒有封閉的 porphyrin 環。'},
    ('22', 33): {'answer': ['A', 'C'], 'note': '共筆答案為 C；AZT 嚴格說是 nucleoside（不是 nucleotide）analog，所以 A 也不正確，選 A 或 C 都算對。',
                 'explain': 'AZT（3′-azido-3′-deoxythymidine）是 thymidine 的 nucleoside analog、prodrug：在細胞內被磷酸化成 AZT-triphosphate，對 HIV 反轉錄酶的親和力遠高於人類 DNA polymerase；3′-OH 被 azido 取代 → 鏈終止。'},
    ('22', 4): {'note': '共筆公布的答案為 C、D（複選或送分），選任一個都算對。細菌最受調控的是 aspartate transcarbamoylase；動物主要在 CPS II 調控。'},
    # 詳解更正
    ('17-2', 2): {'explain': '(A) Propionyl-CoA → methylmalonyl-CoA → succinyl-CoA 的 methylmalonyl-CoA mutase 需要 vitamin B₁₂（嚴格說是 5′-deoxyadenosylcobalamin；methylcobalamin 是 methionine synthase 的輔酶，選項以 B₁₂ 的別名代稱）。\n'
                                 '(B) PLP（vitamin B₆）是轉胺酶與 glycogen phosphorylase 的輔酶。\n(C) TPP 是 pyruvate dehydrogenase 的輔酶之一。\n(D) FAD 用在 β-oxidation、TCA、電子傳遞鏈，但不在這一步。'},
    ('17-2', 4): {'explain_sub': [('即 PLP，又稱Vitamin B6，是轉胺酶和肝糖磷酸水解酶的輔酶。', '')]},
    ('18', 11): {'explain_sub': [('（和 Phenylalanine dehydrogenase 同義）', '')]},
    ('18', 17): {'explain': 'Phycobilin（藻膽素）是藻類的開鏈 tetrapyrrole 色素，不是維生素；vitamin B₁₂ 的別名是 cobalamin（含 corrin 環）。其餘配對正確：PLP／B₆、folic acid／B₉、niacin／B₃。'},
    ('18', 70): {'explain_sub': [('（直線型的 porphyrin）', '（開鏈的 tetrapyrrole）')]},
    ('18', 37): {'explain': 'Alanine 在人體只和 pyruvate 互相轉換（ALT），不再用來合成其他胺基酸，是「死路」。\n'
                            'Serine → glycine、cysteine；aspartate → asparagine（也參與尿素循環、pyrimidine 合成）；glutamine 提供醯胺氮合成 asparagine 等。'},
    ('23-1', 22): {'explain_sub': [('紅血球糖解的最終產物是丙酮酸', '紅血球沒有粒線體，糖解的最終產物是乳酸（lactate）')]},
    ('23-1', 18): {'explain_sub': [('cAMP 在 Liver 會間接使 pyruvate kinase 失去活性，無法促進 glycolysis 使 glucose 送到血液中，血糖上升，但肝臟以外，像這題的 muscle，cAMP 會促進 pyruvate kinase 有活性，促進glycolysis。',
                                    'cAMP 在肝臟會讓 pyruvate kinase 被磷酸化而失活（糖解 ↓、葡萄糖送進血液）；在肌肉，cAMP（epinephrine）經 PKA 促進肝醣分解，提供更多 G6P 進入糖解（肌肉型 pyruvate kinase 不受 PKA 調控）。')]},
    ('23-1', 3): {'explain_sub': [('但長期飢餓時，酮體只會供給三個重要器官──大腦、心臟和骨骼肌，其餘器官會停擺，包括製造酮體的肝臟。因此不是題目所說的所有器官',
                                   '但肝臟缺乏活化酮體的 thiophorase（β-ketoacyl-CoA transferase），只製造、不使用酮體；紅血球沒有粒線體也不能用。因此不是所有器官')]},
    ('18', 20): {'explain_sub': [('(C)為肝糖合成', '(C) 是肝醣分解（glycogenolysis），不在這個循環中')]},
    ('23-1', 1): {'explain_sub': [('即腎上腺皮質素', '即腎上腺素')]},
    ('23-1', 24): {'explain_sub': [('人類的肥胖是源自於瘦素受體的缺陷造成瘦素抗性（Leptin resistance），而非瘦素的量。',
                                    '多數肥胖者的 leptin 濃度反而偏高，問題在下游訊號減弱（leptin resistance），而不是 leptin 不足；OB 基因缺陷造成 leptin 缺乏的人很少。')]},
    ('22', 10): {'explain_sub': [('Adenine deaminase（ADA）', 'adenosine deaminase（ADA；選項寫作 adenine deaminase）')]},
    ('22', 9): {'explain_sub': [('(A) 缺乏 xanthine dehydrogenase 會造成血漿聚集以及過多尿液的生成。', '(A) 缺乏 xanthine dehydrogenase 會造成 xanthinuria（尿中 xanthine 增加、可能結石），尿酸反而降低。'),
                                ('(B) 缺乏 Adenine deaminase 造成腺苷脫氨酶缺乏', '(B) Adenosine deaminase（ADA）缺乏造成 SCID。')]},
    ('22', 20): {'note': '題幹原文寫 urea cycle，應為 TCA cycle（succinyl-CoA 進入的是 TCA）。'},
    ('22', 21): {'explain_sub': [('(A)FdUMP 是藥物', '(B) FdUMP 是活性藥物'), ('(B)(D)都是直接抑制', '(C)(D) 都是直接抑制')]},
}
for k, v in F2.items():
    if k in F:
        merged = dict(F[k]); subs = merged.get('explain_sub', []) + v.get('explain_sub', [])
        merged.update(v)
        if subs: merged['explain_sub'] = subs
        F[k] = merged
    else:
        F[k] = v

out, seen = [], {}
for r in raw:
    key = (r['tag'], r['num'])
    # 23-2 與 23-1 是同一份題目（只有排版差異），只保留 23-2 第 7 題（題幹由 correct 改成 incorrect）
    if r['tag'] == '23-2' and r['num'] != 7:
        continue
    fx = F.get(key, {})
    q = {
        'id': f"g{r['tag'].replace('-', '_')}-{r['num']:02d}",
        'source': SRC,
        'section': 'Ch23' if r['tag'].startswith('23') else f"Ch{r['tag']}",
        'num': r['num'],
        'chapter': MOVE.get(key, r['chapter']),
        'type': 'mcq',
        'stem': re.sub(r'^\s*\.?\d*\.\s*', '', fx.get('stem', r['stem'])).strip(),
        'options': fx.get('options', r['options']),
    }
    a = r['answer']
    q['answer'] = fx['answer'] if 'answer' in fx else ([] if a == 'X' else list(a))
    if 'explain' in fx:
        q['explain'] = fx['explain']
    else:
        e = clean_explain(r['explain_raw'], a)
        for x, y in fx.get('explain_sub', []):
            e = e.replace(x, y)
        q['explain'] = e.strip()
    if len(q['answer']) > 1:
        q['note'] = f"共筆公布的答案為 {'、'.join(q['answer'])}（複選或送分），選任一個都算對。"
    if fx.get('note'): q['note'] = fx['note']
    if fx.get('imageOnly'): q['imageOnly'] = True
    k = norm(q)
    if k in seen:  # 同題重複出現：記在第一次出現的那題
        first = seen[k]
        # 23-1 與 23-2 是共筆把同一份題目印了兩次，不算「重複考」
        if not (first['section'] == 'Ch23' and q['section'] == 'Ch23'):
            first['repeat'] = first.get('repeat', 1) + 1
        continue
    seen[k] = q
    text = q['stem'] + ' ' + ' '.join(o['t'] for o in q['options'])
    q['topics'] = topics_for(q['chapter'], text)
    q['pattern'] = pattern_for(q)
    out.append(q)

for q in out:
    if q.get('repeat'):
        q['note'] = (q.get('note', '') + ' ' if q.get('note') else '') + f"這題在共筆中重複出現 {q['repeat']} 次（歷屆反覆考）。"

os.makedirs(OUT, exist_ok=True)
json.dump(out, open(os.path.join(OUT, 'questions-gongbi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
c = collections.Counter(q['chapter'] for q in out)
print('total', len(out), dict(c))
print('patterns', collections.Counter(q['pattern'] for q in out))
print('topics', collections.Counter(t for q in out for t in q['topics']).most_common())
