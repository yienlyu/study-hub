#!/usr/bin/env python3
"""Build questions-class.json (in-class questions from 2026 slides) and
questions-new.json (new questions modelled on past-exam patterns)."""
import json
from pathlib import Path

DATA = Path(__file__).parent.parent / 'subjects' / 'micro-immuno' / 'data'


def mk(prefix, i, source, ch, pattern, topics, stem, opts, ans, explain, based=None):
    q = {
        'id': f'{prefix}-{i:03d}', 'source': source, 'chapter': ch, 'type': 'mcq',
        'stem': stem, 'options': [{'k': 'ABCDE'[j], 't': t} for j, t in enumerate(opts)],
        'answer': list(ans), 'explain': explain, 'topics': topics, 'pattern': pattern,
    }
    if based: q['basedOn'] = based
    return q


NEG = '選錯誤（否定）題'
POS = '選正確／單一概念題'
CLIN = '臨床情境題'
PAIR = '配對題'
COMB = '組合選擇題'

# ------------------------------------------------------------------ in-class
CLASS = [
    ('innate', POS, ['白血球遷移（selectin→chemokine→integrin）'], '白血球黏附於血管內皮上的三步驟（three-step model of leukocyte adhesion）所使用到的包括有：(a) chemokine (b) integrin (c) selectin，請按照白血球表現使用順序排列。',
     ['c, b, a', 'b, c, a', 'c, a, b', 'a, c, b'], 'C', 'Tethering（selectin）→ Triggering（chemokine）→ Latching（integrin）。'),
    ('innate', POS, ['補體系統', '調理作用／opsonic receptor'], '下列何種產物具有調理作用（opsonization），可增強巨噬細胞、嗜中性球的吞噬作用？',
     ['C3b', 'C5a', 'C5b', 'C4a'], 'A', 'C3b（與 C4b）沉積在病原表面，被吞噬細胞的 complement receptor 辨識。C5a 為趨化；C5b 參與 MAC。'),
    ('innate', POS, ['補體系統'], '下列何者為補體（complement）的三種活化路徑之最初會合點？',
     ['C1qC1rC1s complex', 'C4b', 'C3 convertase', 'C5 convertase'], 'C', '三路徑第一會合點為 C3 convertase（C4b2a 或 C3bBb），第二會合點為 C5 convertase。'),
    ('innate', POS, ['補體系統'], '當補體系統啟動階梯式活化過程中會形成 membrane attack complex（MAC），請問 MAC 由哪些補體組成？',
     ['C3a, C6, C7, C8, C9', 'C3b, C6, C7, C8, C9', 'C5b, C6, C7, C8, C9', 'C5a, C6, C7, C8, C9'], 'C', 'MAC = C5b + C6 + C7 + C8 + 多個 C9。'),
    ('innate', NEG, ['補體系統'], '下列有關補體凝集路徑（lectin pathway）中的關鍵分子 mannan-binding lectin（MBL）的描述何者錯誤？',
     ['可和細菌表面醣蛋白上的 mannose 結合', '可與 MASP-1、MASP-2 以及 MASP-3 結合', '其功能在補體系統中和 C1q 分子相似', '其所參與的凝集路徑和替代路徑的作用機制較相似，與典型途徑較不同'], 'D', 'MBL ≈ C1q，lectin pathway 與 classical pathway 相似（都產生 C4b2a）。'),
    ('innate', POS, ['TLR／PRR'], '偵測細菌 LPS 的主要受器為下列何者？',
     ['Toll-like receptor 9', 'Toll-like receptor 8', 'Toll-like receptor 6', 'Toll-like receptor 4'], 'D', 'LPS → LBP → CD14 → TLR4。'),
    ('innate', POS, ['NK 細胞與抑制性受體'], '下列哪個是屬於 NK 細胞上的抑制性接受體（inhibitory receptor）？',
     ['CD14', 'KIR-3D (short)', 'CD94/NKG2A', 'HLA-E'], 'C', 'CD94/NKG2A（含 ITIM）辨識 HLA-E；KIR 需為 long tail 才有 ITIM；HLA-E 是 ligand。'),
    ('innate', NEG, ['ILC 先天性淋巴細胞'], '對於先天性淋巴細胞（innate lymphoid cell）特性的敘述，下列何者錯誤？',
     ['先天性淋巴細胞表面不表現專一性抗原接受器，其活化並非由辨識特定抗原誘發', '自然殺手細胞屬於先天性淋巴細胞的成員', 'ILC1 可分泌 IFN-γ 來對抗病毒或胞外細菌', 'ILC2 可分泌 IL-4、IL-5、IL-13，可參與氣喘疾病的產生'], 'C', 'ILC1 分泌 IFN-γ 對抗病毒與「胞內」病原；胞外細菌是 ILC3。'),
    ('agab', NEG, ['抗原／epitope'], '可作為活化 B 淋巴細胞的抗原，其特性不包括下列哪一項？',
     ['抗原上的 epitope 多為親水性', '需有 MHC 分子參與和抗原以及 B 細胞上的受體結合', '抗原上作為 B 細胞辨識的 peptides，其序列可為不連續的胺基酸序列', '抗原可以是 protein、polysaccharide 或 lipid'], 'B', 'BCR 直接辨識抗原，不需 MHC；TCR 才需要 MHC。'),
    ('agab', POS, ['抗體多樣性（VDJ/SHM）'], 'B 淋巴細胞的抗體基因進行可變區（variable region）重組，此過程發生於下列哪一器官？',
     ['胸腺', '骨髓', '脾臟', '腸道淋巴組織'], 'B', 'B 細胞在骨髓發育並完成 V(D)J 重組。'),
    ('agab', POS, ['抗體類別與功能', '抗體結構'], '腸胃道中含有大量 IgA，在黏膜免疫反應中可有效阻斷病原菌入侵，相關敘述何者最正確？',
     ['血清與腸胃道中 2 種 IgA 亞型的抗體比例一致', '細胞激素 IL-12 可以促進 B 細胞分泌 IgA', '分泌型 IgA 上的分泌片段（secretory component）是由上皮細胞合成的', '病原菌抗原結合 IgA，可以有效啟動補體古典活化路徑'], 'C', '(A) 血清 IgA1:IgA2 ≈ 10:1，腸道 IgA2 比例高；(B) TGF-β 促進 IgA class switch；(D) 古典路徑由 IgG、IgM 啟動。'),
    ('agab', POS, ['抗體多樣性（VDJ/SHM）'], '下列哪一項為免疫球蛋白基因重組（gene rearrangement）的起始步驟？',
     ['重鏈之 V、J 剪接', '重鏈之 V、D 剪接', '重鏈之 D、J 剪接', '輕鏈之 V、J 剪接'], 'C', '重鏈先 D-J joining，再 V-DJ joining；輕鏈之後才重組。'),
    ('agab', NEG, ['抗體多樣性（VDJ/SHM）'], 'V(D)J 重組過程有許多蛋白參與，下列有關這些蛋白和其功能的敘述何者錯誤？',
     ['RAG-1 和 RAG-2：辨識 recombination signal sequences（RSS）之後產生 DNA 斷裂', 'DNA ligase IV：連結 DNA 的斷裂點', 'Artemis：具有 nuclease activity，可以打開 DNA hairpin 結構，產生 P-nucleotide', 'TdT：可以標記 DNA 的斷裂點或異常的結構'], 'D', 'TdT 以不需模板的方式隨機加入 N-nucleotides，不是標記斷點。'),
    ('agab', POS, ['抗體多樣性（VDJ/SHM）'], '下列何種細胞的抗原接受器會進行體細胞高度突變（somatic hypermutation）？',
     ['T 細胞', 'B 細胞', '巨噬細胞', '自然殺手細胞'], 'B', '只有 B 細胞在 germinal center 進行 SHM → affinity maturation。'),
    ('agab', NEG, ['抗體多樣性（VDJ/SHM）'], '造成抗體多變性的機制（the mechanism of Ab diversity）不包括下列哪一項？',
     ['junctional diversity', 'assorted heavy and light chains', 'V(D)J recombination', 'gene cross-over'], 'D', '六大機制：multiple germline V genes、V(D)J recombination、assorted H/L chains、gene conversion、junctional diversity、somatic point mutation。'),
]

# ---------------------------------------------------------------------- new
NEW = [
    # ---------------- bact-structure
    ('bact-structure', NEG, ['細胞壁／革蘭氏染色'], 'Which of the following statements about the Gram-negative cell envelope is FALSE?',
     ['Lipid A is embedded in the outer membrane and is responsible for endotoxic activity', 'Porins are proteins located in the outer membrane', 'The periplasmic space may contain β-lactamase', 'Teichoic acids anchor the outer membrane to the peptidoglycan layer'], 'D', 'Teichoic acid 只存在於 G(+)。G(−) 外膜靠 lipoprotein（Braun lipoprotein）連接 PDG。', 'k113-bact-33'),
    ('bact-structure', PAIR, ['細菌構造與功能'], 'Which pair of bacterial structure and function is CORRECT?',
     ['Fimbriae – motility', 'Inclusion body – protein synthesis', 'Capsule – antiphagocytic', 'Axial filament – conjugation', 'Plasmid – required for survival'], 'C', 'Capsule 抗吞噬、抗原性差；fimbriae 黏附；inclusion 儲存；axial filament 是 spirochete 運動；plasmid 非生存必需。', 'k113-bact-44'),
    ('bact-structure', NEG, ['人體微生物相'], '關於人體微生物相（microbiota）的敘述，何者錯誤？',
     ['同一個體不同部位的菌種組成不同', '不同個體間菌種差異大，但整體功能相似（functional redundancy）', '共有菌種數：口腔 > 鼻腔 > 腸道 > 皮膚 > 陰道', 'Dysbiosis 只與腸道疾病有關，與代謝疾病無關'], 'D', 'Dysbiosis 與肥胖、糖尿病、憂鬱、癌症等有關。', 'k113-bact-39'),
    ('bact-structure', POS, ['生長曲線與代謝'], '細菌在哪一個生長期對 β-lactam 抗生素最敏感，且可用來計算 generation time？',
     ['Lag phase', 'Exponential (log) phase', 'Stationary phase', 'Death phase'], 'B', 'Log phase 細菌快速分裂、持續合成細胞壁，因此對抑制 PDG 合成的藥最敏感。', 'k113-bact-46'),
    ('bact-structure', POS, ['細菌分類鑑定'], '目前臨床微生物實驗室以蛋白質圖譜快速鑑定細菌，所使用的技術是？',
     ['16S rRNA sequencing', 'MALDI-TOF mass spectrometry', 'Serotyping', 'Phage typing'], 'B', 'Slides：「Current: protein profiling to identify bacteria – MALDI-TOF MS」。'),
    ('bact-structure', NEG, ['細胞壁／革蘭氏染色'], 'Which of the following bacteria is NOT properly classified by Gram staining because of its cell wall?',
     ['Staphylococcus aureus', 'Escherichia coli', 'Mycobacterium tuberculosis', 'Streptococcus pyogenes'], 'C', 'MTB 細胞壁含 mycolic acid → 需 acid-fast stain；Mycoplasma（無壁）、Chlamydia（無 PDG）也是例外。'),
    ('bact-structure', POS, ['生長曲線與代謝'], 'In bacteria, the electron transport chain that generates most ATP is located in the:',
     ['Mitochondrial inner membrane', 'Cytoplasmic (plasma) membrane', 'Outer membrane', 'Nucleoid'], 'B', '細菌無粒線體；ETC 與 oxidative phosphorylation 在細胞膜。', 'k113-bact-09'),
    ('bact-structure', PAIR, ['微生物學史／柯霍假說'], '下列科學家與貢獻的配對，何者正確？',
     ['Lister – 以洗手降低產褥熱', 'Ehrlich – Salvarsan 606 治療梅毒', 'Enders – 發現 penicillin', 'Semmelweis – 以 phenol 消毒手術器械'], 'B', 'Semmelweis 洗手、Lister phenol、Fleming penicillin、Enders 首次培養病毒。', 'k113-bact-40'),
    # ---------------- bact-genetics
    ('bact-genetics', POS, ['突變'], 'The coding region of a gene is 300 nucleotides long (including start and stop codons). A single-nucleotide insertion occurs after nucleotide 151. What is the most likely effect?',
     ['No change in the protein', 'Only amino acid 51 is changed', 'The first 50 amino acids are unchanged; downstream amino acids are altered', 'The first 51 amino acids are changed'], 'C', '151 = 第 51 個密碼子的第 1 個 nt，插入在其後 → 第 51 個密碼子起讀框改變；前 50 個 aa 不受影響。', 'k113-bact-10'),
    ('bact-genetics', POS, ['水平基因轉移'], 'Transfer of bacterial DNA from a donor to a recipient mediated by a bacteriophage is called:',
     ['Transformation', 'Conjugation', 'Transduction', 'Transposition'], 'C', 'Transduction = 噬菌體媒介；generalized 或 specialized。', 'k113-bact-20'),
    ('bact-genetics', NEG, ['DNA 複製與基因表現'], '關於大腸桿菌 lac operon 的敘述，何者錯誤？',
     ['屬於 inducible operon，預設狀態為關閉', 'Allolactose 使 repressor 失去活性', '葡萄糖濃度高時 cAMP-CAP 複合物增加，促進轉錄', '乳糖存在與否決定 operon 是否打開'], 'C', '葡萄糖低 → cAMP↑ → cAMP-CAP 結合 promoter（positive regulation）。'),
    ('bact-genetics', POS, ['DNA 複製與基因表現'], 'In the tryptophan operon, when tryptophan is abundant:',
     ['Tryptophan binds the operator directly', 'Tryptophan acts as a corepressor that activates the repressor to bind the operator', 'Region 2–3 forms an anti-terminator hairpin', 'The ribosome stalls at the Trp codons'], 'B', 'Trp 高：corepressor + repressor → operator；attenuation 時 region 3–4 形成 terminator。', 'k113-bact-48'),
    ('bact-genetics', POS, ['突變'], 'A mutation converting a purine to a pyrimidine is called:',
     ['Transition', 'Transversion', 'Frameshift', 'Silent mutation'], 'B', 'Transition：purine↔purine 或 pyrimidine↔pyrimidine；Transversion：purine↔pyrimidine。'),
    ('bact-genetics', NEG, ['DNA 複製與基因表現'], 'Which statement about bacterial DNA replication is INCORRECT?',
     ['Replication starts at oriC and proceeds bidirectionally', 'It is semi-conservative', 'DNA polymerase I removes RNA primers', 'The lagging strand is replicated from 3\' to 5\' by DNA polymerase III'], 'D', 'DNA 合成只能 5\'→3\'；lagging strand 以 Okazaki fragments 不連續合成。', 'k113-bact-47'),
    ('bact-genetics', POS, ['水平基因轉移'], '以 16S rRNA amplicon sequencing 分析腸道菌相時，最常選擇擴增的變異區為？',
     ['V1–V2', 'V3–V4', 'V6–V7', 'V8–V9'], 'B', '16S rRNA 有 V1–V9，糞便檢體常用 V3–V4。'),
    ('bact-genetics', POS, ['DNA 複製與基因表現'], 'In CRISPR-Cas9 genome editing, precise insertion of a donor DNA template depends on which repair pathway?',
     ['Non-homologous end joining (NHEJ)', 'Homology-directed repair (HDR)', 'Photolyase-mediated direct repair', 'Error-prone repair'], 'B', 'NHEJ → gene disruption；HDR + donor → gene editing。'),
    # ---------------- sterilization
    ('sterilization', POS, ['滅菌與消毒'], '下列哪一種滅菌監測方式「能證明」滅菌成功？',
     ['壓力與溫度計', '滅菌膠帶（chemical indicator）', '含 Bacillus stearothermophilus 孢子的生物指示劑', '操作紀錄表'], 'C', '只有 biological indicator 能證明滅菌；B. stearothermophilus 用於濕熱。'),
    ('sterilization', PAIR, ['滅菌與消毒'], '生物指示劑與滅菌法的配對，何者正確？',
     ['B. subtilis – 濕熱', 'B. pumilus – radiation', 'B. stearothermophilus – ETO', 'B. subtilis – radiation'], 'B', 'B. subtilis：乾熱、ETO；B. pumilus：radiation；B. stearothermophilus：濕熱。'),
    ('sterilization', NEG, ['滅菌與消毒'], 'Which statement about glutaraldehyde is INCORRECT?',
     ['It is a high-level, sporicidal agent', 'It is more active at acidic pH', 'It is inactivated by organic material, so items must be cleaned first', 'It is used for endoscopes'], 'B', 'Glutaraldehyde 在鹼性（2% + 0.3% NaHCO₃）才活化，活化後保存 14 天。'),
    ('sterilization', POS, ['滅菌與消毒'], '手術前刷手常用 0.4% 的哪一種防腐劑？',
     ['Povidone-iodine', 'Chlorhexidine', 'Phenol', 'Glutaraldehyde'], 'B', 'Chlorhexidine：0.2% 漱口、0.4% 刷手、2% 消毒；屬 biguanide。', 'k113-bact-51'),
    ('sterilization', CLIN, ['滅菌與消毒'], '某醫院欲處理對熱與濕氣都敏感的腹腔鏡金屬與塑膠器械，希望快速且不留毒性殘留，最適合的方法是？',
     ['Autoclave 121°C', 'Plasma gas sterilization', 'Boiling 100°C 30 min', 'UV 照射'], 'B', 'Plasma（離子化 H₂O₂ / peracetic acid）適用金屬、塑膠、關節鏡、腹腔鏡器械，但昂貴。', 'k113-mid111-15'),
    ('sterilization', NEG, ['滅菌與消毒'], '關於消毒劑等級的敘述，何者錯誤？',
     ['High-level 可殺死孢子與 M. tuberculosis', 'Intermediate-level 可殺死 M. tuberculosis', 'Low-level 可殺死 M. tuberculosis 但不能殺孢子', '70% alcohol 屬 intermediate-level'], 'C', 'Low-level 無法殺 MTB 與孢子。'),
    # ---------------- pathogenesis
    ('pathogenesis', NEG, ['超級抗原'], 'Which statement about superantigens is FALSE?',
     ['They bind MHC class II outside the peptide-binding groove', 'They activate a large fraction of T cells non-specifically', 'They must be processed by APCs before presentation', 'TSST-1 is an example'], 'C', '超級抗原不需 APC 處理，直接跨接 MHC II 與 TCR Vβ。', 'k113-mid111-76'),
    ('pathogenesis', POS, ['毒素（內/外毒素、AB toxin）'], '臨床上檢測注射液是否含有內毒素（endotoxin），常用的方法是？',
     ['ELISA', 'Limulus amebocyte lysate (LAL) assay', 'Elek test', 'Widal test'], 'B', 'LAL：鱟血 amebocyte 遇 endotoxin 凝集。'),
    ('pathogenesis', PAIR, ['免疫逃脫'], '細菌逃避宿主免疫的機制配對，何者錯誤？',
     ['S. aureus – Protein A 結合 IgG Fc', 'N. gonorrhoeae – IgA protease', 'S. pyogenes – C5a peptidase', 'M. tuberculosis – 產生 coagulase 形成血塊屏障'], 'D', 'Coagulase 是 S. aureus；MTB 阻止 phagolysosome 融合、形成 granuloma。', 'k113-mid111-19'),
    ('pathogenesis', POS, ['毒素（內/外毒素、AB toxin）'], 'Endotoxin (Lipid A) induces fever mainly by binding which receptor complex on macrophages?',
     ['CD14 / TLR4', 'TLR5', 'CD16', 'MHC class II'], 'A', 'LPS → CD14 + TLR4 → IL-1、TNF-α、IL-6 → fever。'),
    ('pathogenesis', POS, ['免疫逃脫'], 'Which bacterium uses a type III secretion system and actin polymerization to spread directly from cell to cell?',
     ['Staphylococcus aureus', 'Shigella', 'Streptococcus pneumoniae', 'Clostridium tetani'], 'B', 'Shigella、Listeria 利用 actin 在胞內移動並傳給鄰細胞。'),
    # ---------------- immuno-basic
    ('immuno-basic', PAIR, ['先天 vs 後天免疫'], '下列 CD 分子與細胞的配對，何者錯誤？',
     ['CD3 – 所有 T 細胞', 'CD19 – B 細胞', 'CD56 – NK 細胞', 'CD8 – helper T 細胞'], 'D', 'CD4 = helper T；CD8 = cytotoxic T。'),
    ('immuno-basic', NEG, ['先天 vs 後天免疫'], 'Which is NOT a feature of the adaptive immune response?',
     ['Specificity', 'Memory', 'Self-limitation', 'Response identical on first and tenth exposure'], 'D', '先天免疫才是每次反應都一樣（無記憶）。'),
    ('immuno-basic', POS, ['先天 vs 後天免疫'], 'A nude (nu/nu) mouse cannot mount a normal immune response mainly because it lacks:',
     ['Bone marrow', 'Thymus', 'Spleen', 'Lymph nodes'], 'B', 'Nude mouse：thymic dysgenesis（athymic）→ 缺 T 細胞。'),
    ('immuno-basic', POS, ['先天 vs 後天免疫'], '在脾臟中，T 細胞主要位於哪一個區域？',
     ['Red pulp', 'Periarteriolar lymphoid sheath (PALS)', 'Germinal center', 'Marginal zone'], 'B', '脾臟 PALS = T 區；follicle / germinal center = B 區。淋巴結 T 區為 paracortex。'),
    ('immuno-basic', NEG, ['先天 vs 後天免疫'], 'Which cell type is NOT considered a phagocyte?',
     ['Neutrophil', 'Macrophage', 'Basophil', 'Dendritic cell'], 'C', 'Phagocytes：neutrophil、eosinophil、monocyte/macrophage、DC；basophil 不屬於。'),
    ('immuno-basic', NEG, ['先天 vs 後天免疫'], 'Chimeric antigen receptor (CAR) T cells used for B-ALL typically contain all of the following EXCEPT:',
     ['anti-CD19 scFv', '4-1BB costimulatory domain', 'CD3ζ signaling domain', 'CTLA-4'], 'D', 'CTLA-4 是 immune checkpoint，不是 CAR 構造。', 'k113-mid111-46'),
    # ---------------- innate
    ('innate', POS, ['補體系統'], 'Which complement fragment forms the C3 convertase of the classical pathway together with C4b?',
     ['C2a', 'C2b', 'C3a', 'Bb'], 'A', 'Classical / lectin C3 convertase = C4b2a；alternative = C3bBb。', 'k113-innate-19'),
    ('innate', NEG, ['補體系統'], 'Which statement about the alternative pathway is NOT true?',
     ['Factor B and factor D are involved', 'C3bBb is its C3 convertase', 'Antigen–antibody complexes are required to initiate it', 'Spontaneous hydrolysis of C3 can form C3(H₂O)Bb'], 'C', '替代路徑不需要抗體。', 'k113-innate-43'),
    ('innate', POS, ['補體系統'], 'Which complement fragments are the main chemotactic / anaphylatoxin molecules?',
     ['C3b and C4b', 'C3a and C5a', 'C5b and C6', 'C1q and C1r'], 'B', 'C3a、C5a 小分子易擴散，結合 C3aR / C5aR。', 'k113-innate-12'),
    ('innate', NEG, ['調理作用／opsonic receptor'], 'Which of the following is NOT an opsonic receptor on phagocytes?',
     ['Mannose receptor', 'FcγRI', 'CR3', 'CD94/NKG2A'], 'D', 'CD94/NKG2A 是 NK 的抑制性受體。', 'k113-innate-10'),
    ('innate', PAIR, ['TLR／PRR'], 'Toll-like receptor 與 ligand 的配對，何者錯誤？',
     ['TLR3 – dsRNA', 'TLR4 – LPS', 'TLR5 – flagellin', 'TLR9 – lipoteichoic acid'], 'D', 'TLR9 辨識 unmethylated CpG DNA；lipoteichoic acid 是 TLR2:TLR6。'),
    ('innate', POS, ['NK 細胞與抑制性受體'], 'The inhibitory receptors KIR-2D and KIR-3D (long) on NK cells recognize:',
     ['HLA-E', 'HLA-C', 'HLA-DR', 'CD1d'], 'B', 'KIR → HLA-C；CD94/NKG2A → HLA-E。', 'k113-innate-48'),
    ('innate', NEG, ['細胞毒殺（perforin/Fas）'], 'Which is NOT directly used by CTLs or NK cells to kill target cells?',
     ['Perforin', 'Granzymes', 'Fas ligand', 'IL-4'], 'D', '毒殺三途徑：FasL–Fas、TNF/LT、perforin/granzymes。IL-4 是 TH2 cytokine。', 'k113-innate-46'),
    ('innate', NEG, ['白血球遷移（selectin→chemokine→integrin）'], 'Which statement about leukocyte migration is NOT true?',
     ['Selectins bind carbohydrates to slow circulating leukocytes', 'Chemokines activate integrins on leukocytes', 'LFA-1 binds ICAM-1', 'Integrins are single-chain molecules and mediate rolling'], 'D', 'Integrin 由 α、β 兩條鏈組成、負責 firm adhesion；rolling 是 selectin。', 'k113-innate-47'),
    ('innate', CLIN, ['NK 細胞與抑制性受體'], '某病毒會使受感染細胞的 MHC class I 表現量下降以躲避 CD8 T 細胞。此時最可能負責清除這些細胞的是？',
     ['CD4 T 細胞', 'B 細胞', 'NK 細胞', 'Mast cell'], 'C', 'NK 細胞偵測 MHC I 缺失（missing self）。', 'k113-innate-27'),
    # ---------------- agab
    ('agab', POS, ['抗體類別與功能'], 'Which immunoglobulin is found at the highest concentration in human serum?',
     ['IgA', 'IgG', 'IgM', 'IgE'], 'B', 'IgG 佔 70–75%。'),
    ('agab', POS, ['抗體類別與功能'], '新生兒出生後主要由哪兩種抗體獲得被動免疫保護？',
     ['IgA 與 IgD', 'IgG 與 IgA', 'IgM 與 IgE', 'IgG 與 IgM'], 'B', 'IgG 經胎盤、IgA 經母乳。', 'k113-agab-30'),
    ('agab', NEG, ['抗體結構'], 'Which statement about antibody structure is INCORRECT?',
     ['Light chains are encoded by V, J and C gene segments', 'IgM and IgE lack a hinge region', 'The class of an antibody is determined by its light chain', 'CDR3 is the most variable region'], 'C', 'Class / subclass 由 heavy chain 決定。', 'k113-agab-06'),
    ('agab', POS, ['抗體類別與功能'], 'A patient has an elevated titer of IgM against a pathogen but no IgG. This most likely indicates:',
     ['Previous vaccination', 'Current (primary) infection', 'Passive maternal immunity', 'Allergy'], 'B', 'IgM 為初次反應主力 → 目前感染指標。', 'k113-tact-22'),
    ('agab', POS, ['抗體多樣性（VDJ/SHM）'], '根據 allelic exclusion，若 B 細胞的 κ 輕鏈重組已成功，接下來會？',
     ['開始 λ 輕鏈重組', '抑制 λ 輕鏈重組', '重新進行 μ 重鏈重組', 'κ 與 λ 同時表現'], 'B', '順序 μ → κ → λ；κ 成功就抑制 λ。', 'k113-agab-21'),
    ('agab', POS, ['抗體結構'], 'The secretory component of secretory IgA is derived from:',
     ['The J chain produced by plasma cells', 'The poly-Ig receptor of epithelial cells', 'Complement C3', 'Fc receptor on mast cells'], 'B', 'poly-Ig receptor 在 transcytosis 後被切下，殘留部分即 secretory component。', 'k113-agab-24'),
    ('agab', NEG, ['抗體多樣性（VDJ/SHM）'], '關於 somatic hypermutation 的敘述，何者錯誤？',
     ['發生於成熟 B 細胞受抗原活化後', '發生在 germinal center', '會同時發生於 T 細胞受體', '與 affinity maturation 有關'], 'C', 'TCR 沒有 SHM。', 'k113-agab-18'),
    ('agab', POS, ['抗體類別與功能'], 'Which antibody binds FcεRI on mast cells and basophils?',
     ['IgA', 'IgD', 'IgE', 'IgG'], 'C', 'IgE 高親和力結合 FcεRI → 過敏反應。', 'k113-agab-28'),
    # ---------------- mhc
    ('mhc', NEG, ['MHC 構造與表現'], 'Which statement about MHC class I is FALSE?',
     ['It consists of an α chain and β2-microglobulin', 'Its peptide-binding groove is formed by α1 and α2', 'It presents peptides of 8–10 amino acids', 'It is expressed on red blood cells'], 'D', 'MHC I 表現於所有有核細胞；紅血球沒有。', 'k113-tdev-03'),
    ('mhc', POS, ['抗原處理與呈現（TAP）'], 'In the MHC class II pathway, which molecule catalyzes the removal of CLIP from the peptide-binding groove?',
     ['TAP', 'Tapasin', 'HLA-DM', 'HLA-DO'], 'C', 'HLA-DM 催化 CLIP 換成抗原 peptide；HLA-DO 抑制 HLA-DM。'),
    ('mhc', POS, ['抗原處理與呈現（TAP）'], 'The invariant chain (Ii) associated with newly synthesized MHC class II molecules functions to:',
     ['Transport peptides from cytosol to ER', 'Prevent binding of ER peptides and direct MHC II to endosomes', 'Degrade exogenous proteins', 'Bind CD4'], 'B', 'Ii 佔住槽、導向 endocytic pathway；在 MIIC 被切到只剩 CLIP。'),
    ('mhc', PAIR, ['MHC 構造與表現'], 'MHC 分子與 co-receptor 結合位置的配對，何者正確？',
     ['CD8 – MHC I α3', 'CD8 – MHC II β2', 'CD4 – MHC I α3', 'CD4 – MHC II α1'], 'A', 'CD8 → MHC I α3；CD4 → MHC II β2。'),
    ('mhc', POS, ['抗原處理與呈現（TAP）'], 'Dendritic cells can present extracellular antigens on MHC class I molecules to activate CD8⁺ T cells. This process is called:',
     ['Autophagy', 'Cross-presentation', 'Allelic exclusion', 'Class switching'], 'B', 'Cross-presentation 是 DC 的特殊能力。', 'k113-tdev-12'),
    ('mhc', NEG, ['MHC 構造與表現'], 'Which statement about MHC polymorphism is INCORRECT?',
     ['MHC genes are co-dominantly expressed', 'MHC diversity arises from somatic DNA rearrangement by RAG1/RAG2', 'MHC diversity mainly differs between individuals', 'MHC polymorphism contributes to transplant rejection'], 'B', 'MHC 多樣性是遺傳（inherited），不需 RAG 重組；BCR/TCR 才是 somatic rearrangement。', 'k113-mid111-75'),
    ('mhc', POS, ['抗原處理與呈現（TAP）'], 'Peptides generated by the proteasome are transported into the ER by:',
     ['Calnexin', 'TAP-1/TAP-2 (ATP-dependent)', 'Invariant chain', 'HLA-DM'], 'B', 'TAP 在 ER 膜，偏好 8–16 aa、C 端疏水 / 鹼性。', 'k113-tdev-04'),
    ('mhc', POS, ['MHC 構造與表現'], 'The human MHC (HLA) genes are located on chromosome:',
     ['6', '17', '14', '2'], 'A', '人類 HLA 在第 6 號；小鼠 H-2 在第 17 號。'),
    # ---------------- tcell-dev
    ('tcell-dev', POS, ['胸腺選擇'], 'Positive selection of thymocytes mainly ensures:',
     ['Self-tolerance', 'MHC restriction', 'Class switching', 'Somatic hypermutation'], 'B', 'Positive selection → MHC restriction；negative selection → self-tolerance。', 'k113-tdev-10'),
    ('tcell-dev', NEG, ['TCR 與 γδ T 細胞'], 'Which statement about γδ T cells is FALSE?',
     ['They are not MHC-restricted', 'Most are CD4⁻CD8⁻ or CD8⁺', 'They are enriched in mucosal epithelia', 'They are derived from mature αβ T cells'], 'D', 'γδ T 來自骨髓前驅細胞、在胸腺發育，不是 αβ 衍生。', 'k113-mid111-73'),
    ('tcell-dev', POS, ['胸腺選擇'], 'Negative selection in the thymus mainly occurs in which region and is mediated by which cells?',
     ['Cortex; cortical thymic epithelial cells', 'Medulla; mTECs and bone-marrow-derived dendritic cells', 'Subcapsular zone; B cells', 'Blood; neutrophils'], 'B', 'cTECs → positive；mTECs、DC、macrophage → negative。', 'k113-mid111-72'),
    ('tcell-dev', POS, ['共刺激（CD28/B7/CTLA-4）'], 'If a naïve T cell receives signal 1 (TCR–pMHC) without signal 2 (CD28–B7), it becomes:',
     ['Fully activated', 'Anergic', 'A memory cell', 'A plasma cell'], 'B', '缺乏共刺激 → T cell anergy。'),
    # ---------------- tcell-act
    ('tcell-act', PAIR, ['TH 分化與細胞激素'], 'TH 亞群與其主要分泌細胞激素的配對，何者錯誤？',
     ['TH1 – IFN-γ', 'TH2 – IL-4', 'TH17 – IL-17', 'Treg – IL-12'], 'D', 'Treg 分泌 TGF-β、IL-10；IL-12 由 APC 分泌、誘導 TH1。', 'k113-tact-07'),
    ('tcell-act', POS, ['TH 分化與細胞激素'], 'Which cytokine combination drives naïve CD4⁺ T cells toward TH17 differentiation?',
     ['IL-12 + IFN-γ', 'IL-4 alone', 'TGF-β + IL-6', 'IL-10 + TGF-β'], 'C', 'TGF-β + IL-6（IL-21、IL-23）→ TH17。', 'k113-tact-41'),
    ('tcell-act', CLIN, ['B 細胞活化／class switch／生發中心'], '一名男童反覆細菌感染，血清 IgM 升高但 IgG、IgA、IgE 很低，CD4 T 細胞數量正常。最可能的缺陷分子是？',
     ['CD28', 'CD40 ligand', 'CTLA-4', 'MHC class I'], 'B', 'X-linked hyper-IgM：CD40L 缺陷 → 無法 class switch。', 'k113-tact-14'),
    ('tcell-act', POS, ['B 細胞活化／class switch／生發中心'], 'Class switch recombination and somatic hypermutation both require which enzyme?',
     ['RAG1', 'TdT', 'AID (activation-induced cytidine deaminase)', 'Artemis'], 'C', 'AID 將 C 脫胺成 U。'),
    ('tcell-act', POS, ['B 細胞活化／class switch／生發中心'], 'Antibody responses to T-independent (TI-2) polysaccharide antigens are characterized by:',
     ['Strong memory and IgG dominance', 'Mainly IgM and little memory', 'Requirement for CD40–CD40L interaction', 'Presentation on MHC II to TFH cells'], 'B', 'TI 抗原無法 class switch、無記憶，主要 IgM。', 'k113-tact-12'),
    ('tcell-act', POS, ['TH 分化與細胞激素'], 'Which cytokine is mainly secreted by T follicular helper (TFH) cells?',
     ['IL-17', 'IL-21', 'IL-5', 'IFN-β'], 'B', 'TFH → IL-21（→ STAT3，促 B 細胞增殖與 germinal center）。', 'k113-mid111-48'),
    ('tcell-act', POS, ['細胞毒殺（perforin/Fas）'], 'Granzymes delivered by CTLs induce apoptosis mainly through:',
     ['Activating caspases (e.g. caspase-3) and cleaving BID', 'Binding TLR4', 'Activating complement C1q', 'Blocking MHC I expression'], 'A', 'Granzyme B → BID → tBID（粒線體）、pro-caspase 3 → caspase 3 → CAD 切 DNA。'),
    # ---------------- infection-immunity
    ('infection-immunity', POS, ['吞噬與 ROS／CGD'], 'Chronic granulomatous disease (CGD) is most commonly caused by a mutation in:',
     ['p47phox', 'gp91phox', 'Myeloperoxidase', 'TLR4'], 'B', 'X-linked gp91 約 65%；p47 約 25%。'),
    ('infection-immunity', POS, ['吞噬與 ROS／CGD'], 'Patients with CGD are especially susceptible to infection by:',
     ['Catalase-negative streptococci', 'Catalase-positive organisms such as S. aureus', 'Enveloped viruses', 'Helminths'], 'B', 'Catalase⁺ 菌會分解自身產生的 H₂O₂，病人吞噬細胞又不能產 ROS。'),
    ('infection-immunity', POS, ['Inflammasome／pyroptosis'], 'Activation of the NLRP3 inflammasome leads to processing of pro-IL-1β by:',
     ['Caspase-3', 'Caspase-1', 'Granzyme B', 'Furin'], 'B', 'Inflammasome → caspase-1 → IL-1β、IL-18；caspase-1 媒介 pyroptosis。'),
    ('infection-immunity', POS, ['TLR／PRR'], 'Which TLR signals independently of MyD88 (via TRIF) to induce type I interferon against RNA viruses?',
     ['TLR2', 'TLR3', 'TLR5', 'TLR9'], 'B', 'TLR3 不經 MyD88。'),
    ('infection-immunity', POS, ['抗微生物肽 AMPs'], 'Antimicrobial peptides such as defensins kill bacteria mainly because they are:',
     ['Negatively charged and bind host cells', 'Positively charged and disrupt negatively charged bacterial membranes', 'Enzymes that degrade peptidoglycan', 'Antibodies'], 'B', 'AMPs 富含 Arg、Lys → 帶正電。'),
    # ---------------- staph-strep
    ('staph-strep', CLIN, ['S. pneumoniae'], 'A 70-year-old man has lobar pneumonia. Sputum shows Gram-positive lancet-shaped diplococci, α-hemolytic, catalase-negative, optochin-sensitive and bile-soluble. The most important virulence factor is:',
     ['M protein', 'Polysaccharide capsule', 'Coagulase', 'TSST-1'], 'B', 'S. pneumoniae：capsule 抗吞噬、疫苗成分。', 'k113-staph2-18'),
    ('staph-strep', CLIN, ['S. agalactiae (GBS)'], '一名新生兒出生一週內發生敗血症與腦膜炎，培養出 catalase(−)、β 溶血、CAMP test(+) 的 G(+) 球菌，最可能是？',
     ['Streptococcus pyogenes', 'Streptococcus agalactiae', 'Enterococcus faecalis', 'Staphylococcus aureus'], 'B', 'GBS：新生兒腦膜炎、CAMP(+)。', 'k113-staph1-05'),
    ('staph-strep', NEG, ['S. aureus'], 'Which of the following is NOT produced by Staphylococcus aureus?',
     ['Protein A', 'Coagulase', 'Exfoliative toxin', 'Streptolysin O'], 'D', 'Streptolysin O 是 S. pyogenes。', 'k113-staph2-13'),
    ('staph-strep', POS, ['S. pyogenes (GAS)'], 'A child develops acute glomerulonephritis 2–3 weeks after a streptococcal skin infection. This complication is best described as:',
     ['Suppurative, caused by direct invasion', 'Non-suppurative, immune-complex mediated', 'Toxin-mediated superantigen disease', 'Caused by Streptococcus agalactiae'], 'B', 'PSGN 為非化膿性後遺症（免疫複合體）。', 'k113-staph2-11'),
    ('staph-strep', CLIN, ['Enterococcus／Viridans'], 'A catheterized elderly inpatient develops UTI. The isolate is catalase-negative, Gram-positive cocci that grow in 6.5% NaCl and bile-esculin, and is resistant to vancomycin. The organism is most likely:',
     ['Viridans streptococci', 'Enterococcus faecium', 'Streptococcus pyogenes', 'Staphylococcus epidermidis'], 'B', 'Enterococcus：耐鹽膽、院內 UTI、VRE。', 'k113-staph2-02'),
    ('staph-strep', POS, ['S. aureus'], 'Staphylococcal food poisoning with vomiting 2–6 hours after a meal is caused by:',
     ['Ingestion of a preformed heat-stable enterotoxin', 'Invasion of the intestinal mucosa', 'Endotoxin release', 'Colonization followed by TSST-1 production'], 'A', '吃到預先形成、耐熱的 enterotoxin（superantigen）。', 'k113-staph2-05'),
    ('staph-strep', PAIR, ['S. pyogenes (GAS)', 'S. aureus'], '疾病與病原的配對，何者正確？',
     ['Scalded skin syndrome – S. pyogenes', 'Scarlet fever – S. pyogenes', 'Rheumatic fever – S. aureus', 'Subacute endocarditis – S. agalactiae'], 'B', 'SSSS → S. aureus；Rheumatic fever → GAS；Subacute endocarditis → Viridans。', 'k113-staph2-14'),
    # ---------------- enterobacteriaceae
    ('enterobacteriaceae', PAIR, ['E. coli 致病型'], 'E. coli 致病型與特徵的配對，何者錯誤？',
     ['ETEC – 旅行者腹瀉、LT 與 ST', 'EHEC – Shiga toxin、HUS', 'EPEC – Shiga toxin、血便', 'UPEC – P pili、泌尿道感染'], 'C', 'EPEC 沒有 Shiga toxin（與 EHEC 差在這裡）。', 'k113-entero-03'),
    ('enterobacteriaceae', CLIN, ['Shigella'], '一群幼兒園學童出現發燒、腹痛、少量帶血黏液便與裡急後重。糞便培養出不發酵乳糖、無運動性、不產 H₂S 的 G(−) 桿菌，最可能是？',
     ['Salmonella enteritidis', 'Shigella sonnei', 'Escherichia coli (ETEC)', 'Proteus mirabilis'], 'B', 'Shigella：乳糖(−)、無運動、H₂S(−)、低感染劑量、人傳人。', 'k113-entero-13'),
    ('enterobacteriaceae', NEG, ['Salmonella'], 'Which statement about Salmonella is INCORRECT?',
     ['It has peritrichous flagella', 'S. Typhi carriers often harbor the organism in the gallbladder', 'Fewer than 100 organisms are usually sufficient to cause gastroenteritis', 'It can survive within macrophages and spread systemically'], 'C', 'Salmonella 需約 10⁵ CFU；<100 CFU 是 Shigella。', 'k113-entero-01'),
    ('enterobacteriaceae', POS, ['E. coli 致病型'], 'Shiga toxin inhibits protein synthesis by:',
     ['ADP-ribosylating EF-2', 'Cleaving an adenine in 28S rRNA of the 60S ribosomal subunit', 'Increasing cAMP', 'Increasing cGMP'], 'B', 'Shiga / Shiga-like toxin 作用在 60S；EF-2 是白喉毒素與 Pseudomonas exotoxin A。', 'k113-mid111-31'),
    ('enterobacteriaceae', POS, ['Yersinia／plague'], 'Which organism can grow at 4°C and is associated with pseudoappendicitis?',
     ['Yersinia enterocolitica', 'Yersinia pestis', 'Shigella dysenteriae', 'Klebsiella pneumoniae'], 'A', 'Y. enterocolitica：cold enrichment、假性闌尾炎、reactive arthritis。'),
    ('enterobacteriaceae', NEG, ['細胞壁／革蘭氏染色'], 'All members of Enterobacteriaceae share the following EXCEPT:',
     ['Glucose fermentation', 'Oxidase negative', 'Gram-negative rods', 'Lactose fermentation'], 'D', '乳糖發酵用來區分（E. coli、Klebsiella +；Salmonella、Shigella −）。', 'k113-entero-20'),
    # ---------------- bacillus
    ('bacillus', NEG, ['Bacillus anthracis'], 'Regarding Bacillus anthracis, which statement is FALSE?',
     ['Its capsule is composed of poly-D-glutamic acid', 'Edema toxin = protective antigen + edema factor', 'It is highly motile due to peritrichous flagella', 'Cutaneous anthrax is the most common form'], 'C', 'B. anthracis 不動（無鞭毛）；B. cereus 會動。', 'k113-bacillus-01'),
    ('bacillus', CLIN, ['Bacillus cereus'], '一家人在餐廳吃完炒飯約 2 小時後出現噁心、嘔吐。最可能的致病菌與毒素性質為？',
     ['B. cereus，heat-stable emetic toxin', 'B. cereus，heat-labile diarrheal toxin', 'S. aureus，TSST-1', 'Clostridium perfringens，α-toxin'], 'A', '米飯、<6 小時、嘔吐 → emetic form，耐熱、耐蛋白酶。', 'k113-bacillus-11'),
    ('bacillus', POS, ['Listeria'], 'Which Listeria virulence factor induces host actin polymerization for intracellular movement?',
     ['Internalin A', 'Listeriolysin O', 'ActA', 'Protein A'], 'C', 'InlA/B 入侵、LLO 溶解液泡、ActA 聚合 actin。', 'k113-bacillus-10'),
    ('bacillus', CLIN, ['C. diphtheriae'], 'A 6-year-old unvaccinated child has sore throat and a gray pseudomembrane over the tonsils. The toxin responsible acts by:',
     ['Cleaving 60S rRNA', 'ADP-ribosylating elongation factor-2', 'Increasing cAMP', 'Blocking acetylcholine release'], 'B', 'Diphtheria toxin → EF-2 ADP-ribosylation。', 'k113-bacillus-07'),
    ('bacillus', NEG, ['Listeria'], 'Which statement about Listeria monocytogenes is INCORRECT?',
     ['It shows tumbling motility at 20–25°C', 'It can cross the placenta', 'Humoral immunity is the main defense', 'It grows at refrigerator temperature'], 'C', '胞內菌 → 細胞免疫為主。', 'k113-bacillus-18'),
    ('bacillus', POS, ['C. diphtheriae'], 'The Elek test is used to detect:',
     ['Antibody against diphtheria toxin in the patient', 'Toxin production by an isolate (toxigenicity)', 'Listeria in food', 'Anthrax spores'], 'B', 'Elek test（immunodiffusion）判斷菌株是否產毒；Schick test 才測體內抗體。', 'k113-bacillus-12'),
    # ---------------- neisseria
    ('neisseria', NEG, ['H. pylori／Campylobacter'], 'Which statement about Helicobacter pylori is FALSE?',
     ['It is urease-positive', 'VacA and CagA are virulence factors', 'It is a zoonotic pathogen acquired from poultry', 'It is associated with gastric adenocarcinoma'], 'C', 'H. pylori 人為唯一宿主；家禽相關的是 Campylobacter jejuni。', 'k113-neis-17'),
    ('neisseria', POS, ['Neisseria'], 'The main component of the Neisseria meningitidis vaccine is:',
     ['Pili', 'Lipooligosaccharide', 'Polysaccharide capsule', 'Opa protein'], 'C', '莢膜多醣疫苗（conjugate）。', 'k113-neis-09'),
    ('neisseria', NEG, ['Pseudomonas'], 'Which statement about Pseudomonas aeruginosa is INCORRECT?',
     ['It produces pyocyanin', 'Exotoxin A inhibits EF-2', 'It commonly infects burn wounds and cystic fibrosis lungs', 'It forms endospores that resist disinfectants'], 'D', 'Pseudomonas 不產孢子；對消毒劑的抗性來自外膜與 biofilm。', 'k113-neis-12'),
    ('neisseria', CLIN, ['Vibrio'], '一名肝硬化病人生食生蠔後 24 小時內出現高燒、下肢出血性水泡與敗血性休克，最可能的病原是？',
     ['Vibrio parahaemolyticus', 'Vibrio vulnificus', 'Vibrio cholerae O1', 'Helicobacter pylori'], 'B', 'V. vulnificus：肝病高危、原發性敗血症。', 'k113-mid111-36'),
    ('neisseria', POS, ['H. pylori／Campylobacter'], 'Guillain-Barré syndrome is a well-known complication of infection with:',
     ['Campylobacter jejuni', 'Helicobacter pylori', 'Neisseria gonorrhoeae', 'Vibrio cholerae'], 'A', 'C. jejuni O:19 molecular mimicry。', 'k113-neis-17'),
    ('neisseria', NEG, ['Neisseria'], 'Which is NOT a virulence factor of Neisseria gonorrhoeae?',
     ['Pili', 'Opa (protein II)', 'IgA1 protease', 'Flagella'], 'D', 'Neisseria 無鞭毛。', 'k113-neis-10'),
    # ---------------- fungi
    ('fungi', POS, ['抗真菌藥物'], 'Which antifungal drug acts by inhibiting β-1,3-glucan synthesis in the fungal cell wall?',
     ['Amphotericin B', 'Fluconazole', 'Caspofungin', 'Terbinafine'], 'C', 'Echinocandins → glucan；azole → 14-α-demethylase；terbinafine → squalene epoxidase；amphotericin → ergosterol 打孔。', 'k113-mid111-43'),
    ('fungi', CLIN, ['皮膚／皮下／系統性黴菌'], '一名園丁被玫瑰刺傷手指數週後，沿前臂出現一連串結節與潰瘍。培養在 25°C 為有隔菌絲、分生孢子呈玫瑰花飾排列，37°C 為酵母菌。最可能為？',
     ['Cryptococcus neoformans', 'Sporothrix schenckii', 'Candida albicans', 'Aspergillus fumigatus'], 'B', 'Lymphocutaneous sporotrichosis，溫度雙型性。', 'k113-fungi-38'),
    ('fungi', NEG, ['Cryptococcus／Candida'], 'Which statement about Cryptococcus neoformans is FALSE?',
     ['It has a thick polysaccharide capsule', 'It is found in pigeon droppings', 'It usually enters via the gastrointestinal tract', 'India ink staining is used for CSF examination'], 'C', '經呼吸道吸入 → 肺 → 腦膜炎。', 'k113-fungi-45'),
    ('fungi', POS, ['真菌構造與分類'], 'A fungus with coenocytic (aseptate) hyphae that produces sporangiospores belongs to:',
     ['Ascomycota', 'Basidiomycota', 'Zygomycota', 'Deuteromycota'], 'C', 'Zygomycota：無隔菌絲、孢子囊孢子、接合孢子。', 'k113-fungi-35'),
    ('fungi', NEG, ['真菌構造與分類'], 'Which of the following is NOT a general characteristic of fungi?',
     ['Eukaryotic', 'Cell membrane contains ergosterol', 'Cell wall contains chitin and β-glucan', 'Optimal growth at pH 7.5–8'], 'D', '真菌偏好酸性 pH 4–6。', 'k113-fungi-46'),
    ('fungi', POS, ['Cryptococcus／Candida'], 'Candida albicans can be distinguished from other Candida species by producing germ tubes in:',
     ['Sabouraud agar', 'Serum', 'Tween-80 agar', 'Blood agar at 25°C'], 'B', 'Germ tube test 以血清培養。', 'k113-fungi-25'),
]


def main():
    cls = [mk('class', i + 1, '2026 課堂題', *t) for i, t in enumerate(CLASS)]
    new = [mk('new', i + 1, '模擬新題', *t) for i, t in enumerate(NEW)]
    (DATA / 'questions-class.json').write_text(json.dumps(cls, ensure_ascii=False, indent=1), encoding='utf-8')
    (DATA / 'questions-new.json').write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding='utf-8')
    from collections import Counter
    print('class', len(cls), 'new', len(new))
    print(Counter(q['chapter'] for q in new))
    for q in new + cls:
        ks = [o['k'] for o in q['options']]
        assert all(a in ks for a in q['answer']), q['id']


if __name__ == '__main__':
    main()
