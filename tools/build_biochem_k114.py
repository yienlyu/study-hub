#!/usr/bin/env python3
"""生化（二）114-1 期中考古（學長姐記題）→ subjects/biochem/data/questions-k114.json

來源：slides/biochemistry/共筆考古/百十三資料/生化(二)/期中考古匯集/
- 第 22–50 題：「醫學系期中考題答案(原檔名亂碼，22-50題).docx」，附官方答案。
- 第 4–16、18 題：各題記題 docx，**沒有附答案**；答案由網站依課本判斷，詳解開頭會註明。
- 第 1–3、17、19–21 題沒有被記下來。
執行：python3 tools/build_biochem_k114.py（在 repo 根目錄）
"""
import json

OUT = "subjects/biochem/data/questions-k114.json"
SRC = "114 期中考古"
NOKEY = "（考古未附答案，網站依課本判斷）"
Q = []


def q(num, ch, stem, opts, ans, exp, topic, official=True, pattern=None):
    Q.append({"id": f"k114-{num:02d}", "source": SRC, "num": num, "chapter": ch, "type": "mcq", "stem": stem,
              "options": [{"k": k, "t": t} for k, t in zip("ABCD", opts)], "answer": [ans],
              "explain": (exp if official else NOKEY + exp), "topics": [topic],
              "pattern": pattern or ("選錯誤／否定題" if any(w in stem for w in ("NOT", "INCORRECT", "not ")) else "選正確／單一概念題")})


# ---- 黃彥華部分（記題，無官方答案）
q(4, "ch17", "In patients with vitamin B12 deficiency, which compound is broken down the least efficiently?（記題者註：題幹太長，只記下考點）",
  ["CH₃(CH₂)₁₀COOH", "CH₃(CH₂)₁₁COOH", "CH₃(CH₂)₁₂COOH", "CH₃(CH₂)₁₄COOH"], "B",
  "奇數碳脂肪酸 β-oxidation 最後產生 propionyl-CoA，要經 methylmalonyl-CoA mutase（需要 B₁₂）才能變成 succinyl-CoA。只有 B 是 13 碳的奇數碳脂肪酸。", "奇數碳脂肪酸", official=False)
q(5, "ch17", "If palmitate (16:0) is oxidized completely to CO₂ and H₂O via β-oxidation and the citric acid cycle, and all energy-conserving products drive ATP synthesis, the net yield of ATP per palmitate is?",
  ["25", "106", "108", "110"], "B",
  "7 輪 β-oxidation 產生 7 FADH₂、7 NADH、8 acetyl-CoA → 108 ATP；活化脂肪酸消耗 2 個高能磷酸鍵 → 淨 106。", "β-oxidation ATP", official=False)
q(6, "ch17", "Where are ketone bodies synthesized?", ["Cytosol", "Mitochondrial matrix", "Mitochondrial intermembrane space", "Endoplasmic reticulum"], "B",
  "肝細胞粒線體基質中由 acetyl-CoA 合成（HMG-CoA synthase 粒線體型）。", "酮體", official=False)
q(7, "ch17", "Free fatty acids in the bloodstream are:",
  ["bound to hemoglobin.", "carried by the protein serum albumin.", "freely soluble in the aqueous phase of the blood.", "present at levels that are independent of epinephrine."], "B",
  "游離脂肪酸在血中與 serum albumin 結合運送；其濃度受 epinephrine、glucagon 調控。", "脂肪酸運送", official=False)
q(8, "ch17", "Which pathway is likely to be affected by a deficiency in carnitine?",
  ["α oxidation", "β oxidation", "Uptake of fatty acids from the bloodstream", "All of the answers are correct"], "B",
  "Carnitine shuttle 把長鏈脂肪醯基送進粒線體做 β-oxidation。", "Carnitine shuttle", official=False)
q(9, "ch21", "Which list ranks the compounds in order from the fewest to the greatest number of carbon atoms?",
  ["Acetate, cholesterol, mevalonate, squalene", "Acetate, mevalonate, squalene, cholesterol",
   "Mevalonate, cholesterol, squalene, acetate", "Acetate, mevalonate, cholesterol, squalene"], "D",
  "Acetate C2 → mevalonate C6 → cholesterol C27 → squalene C30（squalene 環化後去掉 3 個碳變成膽固醇）。", "膽固醇合成", official=False)
q(10, "ch17", "Which hormones stimulate the mobilization/release of fatty acids from adipose tissue to meet energy demands?",
  ["Insulin and epinephrine", "Glucagon and epinephrine", "Insulin and glucagon", "Cortisol and insulin"], "B",
  "Glucagon、epinephrine → cAMP → PKA 磷酸化 perilipin 與 hormone-sensitive lipase → 脂肪分解；insulin 抑制。", "脂肪動員", official=False)
q(11, "ch21", "Which compound is NOT an intermediate in the transfer of acetyl groups from mitochondria to the cytosol?",
  ["Citrate", "Malate", "Oxaloacetate", "Fumarate"], "D",
  "Citrate shuttle：citrate 出粒線體 → citrate lyase 切成 acetyl-CoA＋OAA → OAA 還原成 malate → malic enzyme 變 pyruvate 回粒線體。Fumarate 不參與。", "Citrate shuttle", official=False, pattern="選錯誤／否定題")
q(12, "ch21", "The rate-limiting step in fatty acid synthesis is:",
  ["Condensation of acetyl-CoA and malonyl-CoA", "Formation of acetyl-CoA from acetate",
   "Formation of malonyl-CoA from malonate and coenzyme A", "The reaction catalyzed by acetyl-CoA carboxylase"], "D",
  "Acetyl-CoA carboxylase（需要 biotin）把 acetyl-CoA 變成 malonyl-CoA，是脂肪酸合成的速率限制步驟。", "脂肪酸合成調控", official=False)
q(13, "ch17", "Chylomicrons carry _____ in _____.",
  ["Triglycerides; cell", "Triglycerides; blood", "Cholesterols; blood", "Fatty acid; blood"], "B",
  "乳糜微粒把飲食中的三酸甘油酯經淋巴、血液運到肌肉與脂肪組織。", "脂蛋白", official=False)
q(14, "ch21", "Which one is the critical enzyme for cholesterol biosynthesis, and where can this enzyme be detected?",
  ["HMG-CoA synthase, mitochondria", "HMG-CoA reductase, mitochondria", "HMG-CoA synthase, cytoplasm", "HMG-CoA reductase, cytoplasm"], "D",
  "HMG-CoA reductase 是膽固醇合成的速率限制酵素（statin 標的），位在 ER 膜、活性端朝細胞質；粒線體的 HMG-CoA synthase 用於酮體合成。", "膽固醇合成", official=False)
q(15, "ch21", "Which of the following events occurs first in the process of transporting an LDL into a cell?",
  ["Formation of a coated pit with the aid of clathrin", "Receptor-mediated endocytosis",
   "Fusion of the clathrin-lined vesicles to produce an endosome", "Interaction of apo B-100 with LDL receptors"], "D",
  "LDL 的 apoB-100 先與 LDL receptor 結合，接著 clathrin coated pit → 胞吞 → endosome。", "LDL 受體", official=False)
q(16, "ch21", "Which amino acid is crucial for choline and PC synthesis?", ["Serine", "β-alanine", "Homocysteine", "Methionine"], "D",
  "PE 經三次甲基化（甲基供體是由 methionine 產生的 SAM）變成 PC；choline 也由此而來。（serine 是 PS→PE 的起點，若老師強調 PS 路徑可能另有答案。）", "磷脂合成", official=False)
q(18, "ch17", "What is the major regulation point for transporting fatty acids into mitochondria?",
  ["Long-chain FA specific acyl-CoA synthetase", "Medium-chain FA specific acyl-CoA synthetase",
   "Carnitine palmitoyltransferase I", "Carnitine palmitoyltransferase II"], "C",
  "CPT I 被 malonyl-CoA 抑制，是脂肪酸進入粒線體的主要調控點。", "Carnitine shuttle", official=False)

# ---- 陳顧中部分（附官方答案）
q(22, "ch23", "Which of the following statements about the Cori cycle is CORRECT?",
  ["Alanine is the intermediate molecule in Cori cycle.", "Lactate produced in liver is converted back to glucose in muscle.",
   "It connects anaerobic glycolysis in muscle with gluconeogenesis in liver.", "It produces 36 ATP per glucose molecule."], "C",
  "肌肉無氧糖解產生 lactate → 肝臟糖質新生回到 glucose。Alanine 是 glucose–alanine cycle；Cori cycle 淨消耗 ATP。", "Cori cycle")
q(23, "ch17", "Which of the following substances inhibits ketone body synthesis?", ["Low glucose", "High malonyl-CoA", "High NADH/NAD⁺ ratio", "AMPK activation"], "B",
  "Malonyl-CoA 抑制 CPT I → 脂肪酸無法進粒線體 → 酮體生成減少。", "酮體")
q(24, "ch17", "Which ketone body is exhaled rather than used for energy?", ["β-Hydroxybutyrate", "Acetoacetate", "Acetone", "Propionate"], "C",
  "Acetone 由 acetoacetate 自發去羧產生，經呼氣排出（酮酸中毒的水果味）。", "酮體")
q(25, "ch23", "Which channel closure triggers insulin secretion in pancreatic β-cells?", ["ATP-gated K⁺ channel", "Na⁺/K⁺ pump", "Voltage-gated Ca²⁺ channel", "GLUT4 channel"], "A",
  "血糖 ↑ → ATP ↑ → 關閉 ATP-gated K⁺ channel → 去極化 → 電位依賴性 Ca²⁺ 通道打開 → 胰島素分泌。", "胰島素分泌")
q(26, "ch12", "Which statement about insulin receptor activation is CORRECT?",
  ["Insulin receptor exists as a monomer before activation.", "Insulin receptor must dimerize to become active.",
   "Insulin receptor activates adenylate cyclase directly.", "Insulin receptor is pre-formed as a dimer before ligand binding."], "D",
  "胰島素受體本來就是 (αβ)₂ 二聚體，結合胰島素後自我磷酸化（和 EGF 受體需要配體誘導二聚化不同）。", "胰島素受體")
q(27, "ch12", "The downstream effect of Akt activation includes:",
  ["Activation of GSK3β", "Inhibition of GSK3β via Ser9 phosphorylation", "Activation of PKA", "Activation of adenylate cyclase"], "B",
  "Akt（PKB）磷酸化 GSK3β Ser9 使其失活 → glycogen synthase 不被抑制 → 肝醣合成。", "胰島素訊息")
q(28, "ch23", "Which GLUT isoform is insulin-dependent?", ["GLUT1", "GLUT2", "GLUT4", "GLUT5"], "C",
  "GLUT4 在肌肉與脂肪，受胰島素刺激移到細胞膜。", "GLUT")
q(29, "ch23", "Which of the following CORRECTLY pairs hormone and effect?",
  ["Glucagon – activates gluconeogenesis", "Insulin – activates glycogen phosphorylase", "Epinephrine – inhibits muscle glycolysis", "Leptin – stimulates appetite"], "A",
  "Glucagon 促進肝臟糖質新生；insulin 抑制 glycogen phosphorylase；epinephrine 促進肌肉糖解；leptin 抑制食慾。", "激素作用")
q(30, "ch23", "Which of the following statements about AMPK is INCORRECT?",
  ["Activated during energy deficiency or hypoxia.", "Stimulates fatty acid oxidation and glycolysis.", "Is activated by adiponectin and ghrelin.", "Activates mTOR to promote anabolism."], "D",
  "AMPK 在能量不足時活化、促進分解代謝，並**抑制** mTORC1。", "AMPK")
q(31, "ch23", "Which of the following is NOT a characteristic of GLP-1?",
  ["Increases insulin secretion", "Suppresses glucagon release", "Slows gastric emptying", "Stimulates appetite"], "D",
  "GLP-1 增加胰島素、抑制升糖素、延緩胃排空、**抑制**食慾。", "腸泌素")
q(32, "ch18", "Which molecule activates carbamoyl phosphate synthetase I?", ["N-acetylglutamate", "Aspartate", "Fumarate", "Glutamine"], "A",
  "N-acetylglutamate 是 CPS I 的必要活化劑（尿素循環調控）。", "尿素循環")
q(33, "ch18", "Which amino acid transports nitrogen waste from muscle to liver?", ["Alanine", "Glutamine", "Arginine", "Aspartate"], "A",
  "Glucose–alanine cycle：肌肉把胺基轉給 pyruvate 形成 alanine 送到肝。（Glutamine 是多數組織的氨載體。）", "氮的運送")
q(34, "ch18", "Which of the following amino acids is purely ketogenic?", ["Valine", "Alanine", "Leucine", "Serine"], "C",
  "純生酮胺基酸只有 leucine 與 lysine。", "生酮／生醣胺基酸")
q(35, "ch18", "Which cofactor is required for methylmalonyl-CoA mutase?", ["Biotin", "Vitamin B₁₂", "Tetrahydrofolate", "PLP"], "B",
  "Methylmalonyl-CoA mutase 需要 5'-deoxyadenosylcobalamin（B₁₂）。", "輔因子")
q(36, "ch22", "The coenzyme of ALA synthase is:", ["FAD", "Biotin", "TPP", "PLP"], "D",
  "ALA synthase（succinyl-CoA＋glycine）需要 PLP，是血基質合成的速率限制酵素。", "血基質合成")
q(37, "ch22", "Which vitamin deficiency leads to pellagra?", ["B₁", "B₂", "B₃", "B₆"], "C",
  "Pellagra 是 niacin（B₃）缺乏；tryptophan 可轉成 niacin。", "胺基酸衍生物")
q(38, "ch18", "Which cofactor is required by branched-chain α-keto acid dehydrogenase?", ["PLP", "TPP", "BH₄", "Biotin"], "B",
  "BCKDH 和 PDH 一樣需要 TPP、lipoate、FAD、NAD⁺、CoA；缺乏 → 楓糖尿症。", "輔因子")
q(39, "ch18", "BH₄ is NOT a cofactor required for which of the following enzymes?",
  ["Tyrosine hydroxylase", "Pyruvate carboxylase", "Nitric oxide synthase", "Phenylalanine hydroxylase"], "B",
  "Pyruvate carboxylase 需要 biotin；其他三個都需要 BH₄。", "輔因子")
q(40, "ch18", "Which pair of amino acids are both branched-chain?",
  ["Valine, Isoleucine", "Serine, Alanine", "Histidine, Arginine", "Glycine, Cysteine"], "A", "BCAA：valine、leucine、isoleucine。", "BCAA")
q(41, "ch12", "Sildenafil (Viagra) exerts its effect by inhibiting:", ["Adenylyl cyclase", "Guanylyl cyclase", "Phosphatase", "Phosphodiesterase"], "D",
  "抑制 cGMP phosphodiesterase（PDE5）→ cGMP 維持 → 平滑肌放鬆。", "cGMP 訊息")
q(42, "ch22", "Which amino acid derivative is mainly used for bile salt synthesis?", ["Creatine", "Taurine", "Spermidine", "Ornithine"], "B",
  "Taurine（由 cysteine 而來）和 glycine 與膽酸結合形成膽鹽。", "胺基酸衍生物")
q(43, "ch22", "In heme catabolism, which enzyme converts biliverdin to bilirubin?",
  ["Biliverdin reductase", "Heme oxygenase", "UDP-glucuronyltransferase", "Ferrochelatase"], "A",
  "Heme oxygenase：heme → biliverdin；biliverdin reductase：biliverdin → bilirubin。", "血基質分解")
q(44, "ch22", "Which of the following is the correct match between amino acid and its main derivative?",
  ["Arginine – Creatine", "Glycine – GABA", "Tyrosine – Niacin", "Methionine – Histamine"], "A",
  "Creatine 由 glycine＋arginine（＋SAM）合成；GABA 來自 glutamate；niacin 來自 tryptophan；histamine 來自 histidine。", "胺基酸衍生物")
q(45, "ch12", "When epinephrine binds to β-adrenergic receptors on hepatocytes, which of the following occurs first?",
  ["Activation of adenylate cyclase", "Activation of protein kinase A", "Gs protein binds GTP", "Phosphorylation of glycogen phosphorylase"], "C",
  "受體活化 → Gs 的 GDP 換成 GTP → 活化 adenylyl cyclase → cAMP → PKA → phosphorylase。", "GPCR 訊息")
q(46, "ch23", "Insulin resistance in type II diabetes often involves serine phosphorylation of the insulin receptor (substrate). This modification:",
  ["Activates receptor tyrosine kinase activity", "Stimulates glycogen synthase", "Enhances GLUT4 translocation", "Blocks downstream PI3K–Akt signaling"], "D",
  "絲胺酸磷酸化阻斷 IRS 的酪胺酸磷酸化 → PI3K–Akt 訊息被擋住 → 胰島素阻抗。", "胰島素阻抗")
q(47, "ch23", "A mutation causing constitutive activation of mTORC1 would most likely result in:",
  ["Enhanced lipolysis", "Decreased protein synthesis", "Persistent anabolic signaling", "Increased AMPK activation"], "C",
  "mTORC1 促進蛋白質合成等合成代謝。", "mTOR")
q(48, "ch23", "Which of the following tissues relies exclusively on anaerobic glycolysis for ATP production?",
  ["Brain", "Red blood cells", "Heart", "Kidney cortex"], "B", "紅血球沒有粒線體，只能靠無氧糖解。", "器官燃料")
q(49, "ch23", "A mutation in GLUT2 would most directly affect which process?",
  ["Hepatic glucose uptake and release", "Muscle glucose storage", "Adipose lipolysis", "Intestinal fructose absorption"], "A",
  "GLUT2 在肝臟（與胰臟 β 細胞、腸道基底側），負責肝臟雙向運送葡萄糖。", "GLUT")
q(50, "ch18", "Which of the following reactions requires biotin as a cofactor?",
  ["Phenylalanine → Tyrosine", "Methylmalonyl-CoA → Succinyl-CoA", "Homocysteine → Methionine", "Propionyl-CoA → Methylmalonyl-CoA"], "D",
  "Propionyl-CoA carboxylase 需要 biotin；PAH 需要 BH₄；mutase 需要 B₁₂；methionine synthase 需要 B₁₂ 與 THF。", "輔因子")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(OUT, len(Q), "questions;", sum(1 for x in Q if x["explain"].startswith(NOKEY)), "without official key")
