"""Write subjects/biochem/figures.json (hand-drawn SVGs + slide crops)."""
import json, os
from PIL import Image
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'subjects', 'biochem')

def svg(id, ch, title, topics, kw, cap):
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap)

def slide(id, ch, title, topics, kw, cap, deck, page):
    src = f"figures/slides/{id[6:]}.webp"
    w, h = Image.open(os.path.join(ROOT, src)).size
    return dict(id=id, chapter=ch, title=title, topics=topics, keywords=kw, caption=cap,
                type="slide", src=src, deck=deck, page=str(page), w=w, h=h)

D181, D182, D183 = ("Ch18-1 Amino acid oxidation（Ch23-2 後半）", "Ch18-2 Amino acid catabolism", "Ch18-3、Ch22 Nitrogenous compounds")
D17, D12, D21, D23 = ("W1 Ch17 Lipid metabolism", "W2 Ch12 Biochemical Signaling",
                     "W3 Ch21 Lipid Biosynthesis", "W4 Ch23-1 Hormonal regulation")
F = [
 # ch17
 slide("slide-ch17-overview","ch17","中間代謝總覽：脂肪酸與 TG 的位置",["β-oxidation 與 ATP 計算","脂肪動員與運輸"],
     "intermediary metabolism lipids glycerol fatty acids acetyl-CoA citric acid cycle FADH2 NADH oxidative phosphorylation Figure 17.1",
     "Figure 17.1：脂質分解成 <strong>glycerol</strong>（進糖解／糖質新生）與<strong>脂肪酸</strong>（β-oxidation → <strong>acetyl-CoA</strong> → TCA）；β-oxidation 本身也直接產生 <strong>FADH₂、NADH</strong> 送電子傳遞鏈。手寫：FADH₂、NADH、GTP。",D17,4),
 svg("fa-transport","ch17","脂質的消化、吸收與運輸",["脂肪動員與運輸","脂蛋白與膽固醇恆定"],
     "bile salt micelle chylomicron lipoprotein lipase apoC-II albumin 乳糜微粒",
     "膽鹽乳化 → 腸細胞重組 TG → <strong>乳糜微粒</strong>經淋巴入血 → 微血管的 <strong>lipoprotein lipase</strong>（apoC-II 活化）把 TG 切成脂肪酸給組織。"),
 slide("slide-ch17-lipoprotein","ch17","脂蛋白的運輸路線",["脂蛋白與膽固醇恆定"],
     "chylomicron VLDL IDL LDL HDL LDL receptor","外源（乳糜微粒）與內源（VLDL → IDL → LDL）兩條路線；LDL receptor 缺陷造成家族性高膽固醇血症。",D17,16),
 slide("slide-ch17-mobilization","ch17","激素動員脂肪組織的 TG",["脂肪動員與運輸"],
     "glucagon epinephrine PKA HSL perilipin ATGL MGL albumin",
     "Glucagon／epinephrine → cAMP → <strong>PKA 磷酸化 HSL 與 perilipin</strong> → ATGL、HSL、MGL 依序水解 TG；脂肪酸由 <strong>albumin</strong> 運到肌肉。",D17,22),
 svg("carnitine-shuttle","ch17","Carnitine shuttle",["Carnitine shuttle"],
     "carnitine CPT I CPT II translocase malonyl-CoA acyl-CoA synthetase",
     "脂肪醯-CoA 不能直接進粒線體：<strong>CPT I</strong> 換成 acyl-carnitine → translocase → CPT II 換回 acyl-CoA。CPT I 被 <strong>malonyl-CoA</strong> 抑制。"),
 svg("beta-oxidation","ch17","β-oxidation 四步驟與 ATP 帳本",["β-oxidation 與 ATP 計算"],
     "acyl-CoA dehydrogenase FAD hydratase NAD thiolase palmitate 106 ATP",
     "去氫（FAD）→ 水合 → 去氫（NAD⁺）→ 硫解，每輪切下一個 acetyl-CoA。Palmitate 淨產 <strong>106 ATP</strong>。"),
 svg("odd-chain","ch17","奇數碳脂肪酸與 propionyl-CoA",["奇數碳與 propionyl-CoA"],
     "propionyl-CoA carboxylase biotin methylmalonyl-CoA mutase B12 succinyl-CoA",
     "最後剩下 <strong>propionyl-CoA</strong> → 羧化（biotin）→ methylmalonyl-CoA → mutase（<strong>B₁₂</strong>）→ succinyl-CoA 進 TCA。"),
 svg("ketogenesis","ch17","酮體的生成與利用",["酮體"],
     "HMG-CoA synthase lyase acetoacetate beta-hydroxybutyrate acetone thiophorase",
     "肝粒線體合成（HMG-CoA synthase／lyase），肝外組織用 <strong>thiophorase</strong> 活化；<strong>肝臟自己不能用酮體</strong>。"),
 # ch12
 slide("slide-ch12-four-types","ch12","四大類訊號轉導器",["訊息傳遞特徵與受體類型"],
     "GPCR receptor tyrosine kinase gated ion channel nuclear receptor",
     "① GPCR ② 受體酵素（RTK）③ 門控離子通道 ④ 核受體。",D12,6),
 svg("gpcr-camp","ch12","β-adrenergic 受體與 cAMP 路徑",["GPCR 與 cAMP／PKA"],
     "epinephrine beta adrenergic Gs adenylyl cyclase cAMP PKA GTPase PDE betaARK arrestin",
     "Epinephrine → GPCR → <strong>G<sub>s</sub>α-GTP</strong> → adenylyl cyclase → cAMP → <strong>PKA（R₂C₂，4 cAMP）</strong> → 肝醣分解。右側是四種關閉機制。"),
 svg("second-messengers","ch12","IP₃／DAG／Ca²⁺ 與 cGMP",["IP3／DAG／Ca²⁺","cGMP／NO"],
     "Gq phospholipase C PIP2 IP3 DAG PKC calcium guanylyl cyclase NO ANF cGMP PKG PDE5 sildenafil",
     "PLC 把 PIP₂ 切成 <strong>IP₃（開 ER Ca²⁺ 通道）</strong>與 <strong>DAG（活化 PKC）</strong>；NO、ANF 經 guanylyl cyclase 產生 cGMP，sildenafil 抑制 PDE5。"),
 svg("insulin-signaling","ch12","Insulin 受體的訊號路徑",["RTK 與胰島素訊號"],
     "insulin receptor autophosphorylation IRS-1 Grb2 Sos Ras Raf MEK ERK PI3K PIP3 Akt GSK3 GLUT4",
     "受體 Tyr 自體磷酸化 → IRS-1 → ① <strong>Ras–MAPK</strong>（生長）② <strong>PI3K → Akt</strong> → GLUT4 移位、GSK3 失活 → 肝醣合成。"),
 slide("slide-ch12-insulin-rtk","ch12","Insulin 促進肝醣合成與 GLUT4 移位",["RTK 與胰島素訊號"],
     "IRS1 PI3K PKB GSK3 glycogen synthase GLUT4 Rab RAC1",
     "PKB（Akt）磷酸化 GSK3 使其失活 → glycogen synthase 保持活化；同時讓 GLUT4 囊泡移到細胞膜。",D12,31),
 # ch21
 svg("fa-synthesis","ch21","脂肪酸合成：citrate shuttle、ACC 與 FAS",["脂肪酸合成與 ACC","合成 vs 分解比較"],
     "citrate shuttle citrate lyase malic enzyme NADPH acetyl-CoA carboxylase malonyl-CoA fatty acid synthase palmitate",
     "Acetyl-CoA 以 <strong>citrate</strong> 運出粒線體；<strong>ACC</strong>（biotin，限速）做 malonyl-CoA；FAS 每輪用 2 NADPH，7 輪得 palmitate。"),
 svg("eicosanoids","ch21","Eicosanoids 的生成與 NSAIDs",["Eicosanoids 與 NSAIDs"],
     "phospholipase A2 arachidonate cyclooxygenase COX prostaglandin thromboxane lipoxygenase leukotriene aspirin",
     "PLA₂ 釋出 arachidonate → <strong>COX</strong>（prostaglandins、thromboxanes；NSAIDs 抑制）或 <strong>lipoxygenase</strong>（leukotrienes）。"),
 svg("phospholipid-synthesis","ch21","甘油磷脂合成的兩種策略",["磷脂質合成"],
     "phosphatidic acid CDP-diacylglycerol CDP-choline PI PS PE PC SAM methylation",
     "共同起點 PA：① 活化 DAG（CDP-DAG → PI、PS）② 活化頭基（CDP-choline → PC）。PE 經 <strong>3 個 SAM</strong> 甲基化成 PC。"),
 slide("slide-ch21-sphingolipid","ch21","鞘脂代謝的遺傳疾病",["鞘脂與溶體疾病"],
     "Tay-Sachs hexosaminidase Niemann-Pick sphingomyelinase Gaucher Fabry",
     "<strong>Tay-Sachs</strong>：hexosaminidase A → GM2；<strong>Niemann-Pick</strong>：sphingomyelinase → sphingomyelin。",D21,45),
 svg("cholesterol-synthesis","ch21","膽固醇合成與 HMG-CoA reductase 調控",["膽固醇合成與 HMG-CoA reductase"],
     "HMG-CoA reductase mevalonate isopentenyl pyrophosphate squalene lanosterol statin SREBP",
     "Acetyl-CoA → HMG-CoA →（<strong>HMG-CoA reductase，限速、statins 抑制</strong>）→ mevalonate → IPP（5C）→ squalene（30C）→ cholesterol（27C）。"),
 # ch23
 svg("organ-fuel","ch23","器官之間的燃料流動",["各器官燃料代謝","Cori／葡萄糖-丙胺酸循環","酮體"],
     "liver brain muscle adipose red blood cell glucose ketone lactate alanine",
     "肝臟輸出葡萄糖（飢餓時加酮體）；肌肉、紅血球把 <strong>lactate、alanine</strong> 送回肝；<strong>肌肉沒有 G6Pase</strong>，紅血球沒有粒線體。"),
 svg("rbc-glycolysis","ch23","紅血球糖解的支路",["各器官燃料代謝"],
     "red blood cell erythrocyte no mitochondria anaerobic glycolysis lactate pentose phosphate pathway PPP G6PD NADPH glutathione GSH GSSG 2,3-BPG Rapoport-Luebering shunt bisphosphoglycerate mutase methemoglobin reductase 紅血球 蠶豆症",
     "紅血球<strong>沒有粒線體</strong> → 只靠無氧糖解到 lactate（淨 2 ATP）；G6P 分出 <strong>PPP</strong> 產生 <strong>NADPH</strong> 維持 glutathione 還原態；1,3-BPG 分出 <strong>2,3-BPG</strong>（不產 ATP）降低 Hb 的 O₂ 親和力。"),
 svg("glycolysis","ch23","糖解作用總覽（複習）",["各器官燃料代謝","Cori／葡萄糖-丙胺酸循環"],
     "glycolysis 糖解 hexokinase glucokinase PFK-1 aldolase GAPDH PGK phosphoglycerate kinase enolase fluoride pyruvate kinase investment payoff phase net 2 ATP 2 NADH LDH lactate PDH",
     "葡萄糖 → 2 pyruvate：<strong>投資期</strong>（hexokinase、PFK-1）花 2 ATP，<strong>回收期</strong>（PGK、pyruvate kinase 各 ×2）產 4 ATP，GAPDH 產 2 NADH → <strong>淨 2 ATP + 2 NADH</strong>。紅線三步不可逆，是調控點，也是糖質新生要繞過的地方。"),
 svg("gluconeogenesis","ch23","糖質新生總覽（複習）",["各器官燃料代謝","Cori／葡萄糖-丙胺酸循環"],
     "gluconeogenesis 糖質新生 pyruvate carboxylase biotin acetyl-CoA PEPCK GTP malate shuttle FBPase-1 fructose-1,6-bisphosphatase F-2,6-BP G6Pase glucose-6-phosphatase ER von Gierke lactate alanine glycerol kinase glucogenic odd-chain propionyl-CoA 4 ATP 2 GTP 2 NADH",
     "2 pyruvate → glucose：用 <strong>pyruvate carboxylase + PEPCK、FBPase-1、G6Pase</strong> 繞過糖解三個不可逆步驟，其餘可逆步驟倒著走。每個葡萄糖花 <strong>4 ATP + 2 GTP + 2 NADH</strong>。原料是 lactate、alanine、生醣胺基酸、glycerol；<strong>偶數碳脂肪酸不能淨造糖</strong>。"),
 svg("tca-cycle","ch23","TCA 循環總覽（複習）",["各器官燃料代謝"],
     "TCA citric acid cycle Krebs 檸檬酸循環 citrate synthase aconitase isocitrate dehydrogenase rate-limiting α-ketoglutarate dehydrogenase TPP lipoate succinyl-CoA synthetase GTP substrate-level phosphorylation succinate dehydrogenase complex II FADH2 fumarase malate dehydrogenase oxaloacetate 3 NADH 1 FADH2 10 ATP anaplerotic propionyl-CoA SCOT aspartate glutamate citrate shuttle",
     "Acetyl-CoA + OAA → citrate → … → OAA：每圈產 <strong>3 NADH + 1 FADH₂ + 1 GTP ＝ 10 ATP</strong>，放出 2 CO₂。限速酵素是 <strong>isocitrate DH</strong>；FADH₂ 只來自 <strong>succinate DH（複合體 II）</strong>。紫字標出和各章的接點：citrate → FA 合成、α-KG ⇄ glutamate、奇數碳 → succinyl-CoA、尿素循環 → fumarate、OAA ⇄ aspartate／糖質新生。"),
 svg("ketone-switch","ch23","飢餓時肝臟的生酮開關",["酮體","飢餓與糖尿病","AMPK"],
     "malonyl-CoA ACC CPT I AMPK insulin glucagon oxaloacetate gluconeogenesis HMG-CoA synthase HMGCS2 SCOT thiophorase ketone bodies starvation diabetic ketoacidosis",
     "飢餓、T1DM：insulin ↓、AMPK ↑ → ACC 被抑制 → <strong>malonyl-CoA ↓ → CPT I 放行</strong> → β-oxidation ↑；<strong>OAA 被拉去糖質新生</strong> → acetyl-CoA 轉做酮體。肝外組織靠 <strong>SCOT</strong> 用酮體，<strong>肝臟沒有 SCOT</strong>。"),
 svg("nafld-ketogenesis","ch23","脂肪肝：生酮變少、氧化與糖質新生變多",["酮體","飢餓與糖尿病"],
     "NAFLD fatty liver ketogenesis beta-hydroxybutyrate acetoacetate TCA cycle anaplerosis oxygen consumption gluconeogenesis hyperglycemia insulin resistance glucagon insulin ratio fasting",
     "禁食 24 h：β-oxidation 量相近，但脂肪肝的 acetyl-CoA <strong>少做酮體、多進 TCA 燒掉</strong> → O₂ 耗用與 ATP ↑ → <strong>糖質新生 ↑ → 高血糖</strong>；血酮約少 30%（主要是 β-HB）。改繪自 Fletcher et al., <em>JCI Insight</em> 2019。"),
 svg("cori-cycle","ch23","Cori cycle",["Cori／葡萄糖-丙胺酸循環"],
     "Cori cycle lactate LDH anaerobic glycolysis gluconeogenesis liver muscle red blood cell 2 ATP 6 ATP 乳酸",
     "肌肉／紅血球無氧糖解得 <strong>2 ATP</strong> → lactate 經血液到肝 → 糖質新生花 <strong>6 ATP</strong> → 葡萄糖送回；整個循環淨耗 4 ATP。"),
 svg("glucose-alanine","ch23","Glucose-alanine cycle",["Cori／葡萄糖-丙胺酸循環"],
     "glucose-alanine cycle alanine aminotransferase ALT PLP B6 BCAA glutamate urea cycle gluconeogenesis 丙胺酸",
     "肌肉把胺基經 glutamate 交給 pyruvate → <strong>alanine</strong> 到肝 → ALT 轉胺回 pyruvate 做糖質新生、NH₂ 進<strong>尿素循環</strong>；同時運送 <strong>C 和 N</strong>。"),
 svg("insulin-secretion","ch23","β 細胞的胰島素分泌",["胰島素與 GLUT"],
     "beta cell GLUT2 ATP sensitive K channel depolarization calcium exocytosis incretin GLP-1 sulfonylurea",
     "血糖 ↑ → ATP/ADP ↑ → <strong>K-ATP 通道關閉 → 去極化 → Ca²⁺ 流入</strong> → insulin 胞吐。"),
 svg("membrane-potential","ch23","膜電位（複習）",["胰島素與 GLUT"],
     "membrane potential resting potential 膜電位 靜止膜電位 Na+/K+-ATPase K+ leak channel equilibrium potential Nernst depolarization hyperpolarization threshold voltage-gated calcium channel 去極化 過極化 閾值 K-ATP sulfonylurea diazoxide",
     "Na⁺/K⁺-ATPase 建立梯度，K⁺ 經 leak 通道外流 → 膜內為負（<strong>≈ −70 mV</strong>，接近 E<sub>K</sub>）。<strong>K⁺ 外流減少或陽離子流入 → 去極化</strong>，過閾值打開電壓門控 Ca²⁺ 通道；K⁺ 通道開更多 → 過極化。"),
 slide("slide-ch23-insulin-receptor","ch23","Insulin 受體的下游作用",["胰島素與 GLUT"],
     "insulin receptor IRS PI3K Akt mTORC1 GSK3 GLUT4 Ras MAPK PPAR gamma",
     "RTK → IRS → PI3K–Akt（GLUT4、mTORC1、GSK3）與 Ras–MAPK（生長）等多條路徑。",D23,43),
 slide("slide-ch23-cori","ch23","Cori cycle",["Cori／葡萄糖-丙胺酸循環"],
     "Cori cycle lactate gluconeogenesis 6 ATP 2 ATP",
     "肌肉糖解得 <strong>2 ATP</strong> → lactate → 肝臟糖質新生花 <strong>6 ATP</strong> → 葡萄糖回肌肉。",D23,14),
 slide("slide-ch23-leptin","ch23","Leptin：脂肪存量的訊號",["瘦素與脂肪激素"],
     "leptin adipocyte arcuate nucleus POMC NPY AgRP leptin resistance",
     "脂肪細胞分泌 leptin → 下視丘 arcuate nucleus（↑ POMC、↓ NPY/AgRP）→ 吃少、消耗多；多數肥胖者是 <strong>leptin resistance</strong>。",D23,56),
 # ch18
 svg("urea-cycle","ch18","尿素循環",["尿素循環"],
     "carbamoyl phosphate synthetase NAG ornithine citrulline argininosuccinate arginine fumarate arginase urea",
     "粒線體：CPS I（<strong>NAG</strong> 活化）→ citrulline；細胞質：+ <strong>aspartate</strong> → argininosuccinate → arginine + <strong>fumarate</strong> → urea。"),
 svg("urea-map","ch18","尿素循環觀念圖（氮從哪來、卡住會發生什麼事）",["尿素循環","氨的運輸"],
     "urea cycle concept map transamination PLP ALT AST glutaminase glutamate dehydrogenase GDH NH4 aspartate NAG CPS I OTC orotic acid citrullinemia argininosuccinate lyase arginase hyperammonemia hepatic encephalopathy HI/HA fumarate TCA 高血氨 肝性腦病變 觀念圖",
     "所有氮先集中到 <strong>glutamate</strong>：GDH 放出 <strong>NH₄⁺</strong>（第 1 個 N）、AST 做成 <strong>aspartate</strong>（第 2 個 N）；<strong>NAG</strong> 開 CPS I、<strong>fumarate</strong> 接 TCA；缺陷看上游堆積：<strong>OTC → orotic acid ↑</strong>、<strong>ASS → citrulline ↑</strong>。"),
 svg("krebs-bicycle","ch18","Krebs bicycle：尿素循環與 TCA 怎麼接",["尿素循環"],
     "Krebs bicycle urea cycle TCA citric acid cycle connection fumarate aspartate argininosuccinate shunt fumarase malate dehydrogenase NADH oxaloacetate AST glutamate GDH α-ketoglutarate CPS I NAG acetyl-CoA malate-aspartate shuttle hyperammonemia hepatic encephalopathy 尿素循環 TCA 連結 觀念圖",
     "尿素循環在 ASL 步驟<strong>吐出 fumarate</strong>，經 fumarase → malate → MDH（產 <strong>1 NADH</strong>）→ OAA → AST 轉胺成 <strong>aspartate</strong>，再於 ASS 步驟<strong>吃回去</strong>；malate 可進出粒線體與 TCA 共用碳骨架。<strong>Glutamate ⇄ α-KG</strong> 同時供應兩個 N（GDH → NH₄⁺、AST → Asp）。別和 malate-aspartate shuttle 搞混。"),
 svg("phe-tyr-diseases","ch18","Phe／Tyr 代謝與先天疾病",["先天胺基酸代謝疾病","胺基酸衍生物"],
     "phenylketonuria phenylalanine hydroxylase BH4 albinism tyrosinase alkaptonuria homogentisate catecholamine dopamine",
     "PAH（BH₄）缺 → <strong>PKU</strong>；tyrosinase 缺 → <strong>albinism</strong>；homogentisate dioxygenase 缺 → <strong>alkaptonuria</strong>。"),
 svg("homocysteine-hub","ch18","Homocysteine 的兩條出路：B₁₂、葉酸與 B₆",["一碳單位與輔酶（THF／BH4／B12）","先天胺基酸代謝疾病"],
     "homocysteine methionine synthase B12 folate MTHFR N5-methyl-THF methyl trap SAM SAH cystathionine beta-synthase PLP cysteine methylmalonic acid homocystinuria megaloblastic anemia",
     "再甲基化：<strong>methionine synthase（B₁₂）</strong>用 MTHFR 做的 <strong>N⁵-methyl-THF</strong>；轉硫：<strong>CBS（PLP）</strong>+ serine → cystathionine → cysteine。B₁₂ 另管 methylmalonyl-CoA mutase → <strong>MMA ↑ 區分 B₁₂ 缺與葉酸缺</strong>。"),
 svg("bh4-cycle","ch18","BH₄ 循環與兩型 PKU",["一碳單位與輔酶（THF／BH4／B12）","先天胺基酸代謝疾病","胺基酸衍生物"],
     "tetrahydrobiopterin BH4 dihydropteridine reductase DHPR phenylalanine hydroxylase tyrosine hydroxylase tryptophan hydroxylase nitric oxide synthase PKU dopamine serotonin",
     "BH₄ 是 <strong>PAH、Tyr hydroxylase、Trp hydroxylase、NOS</strong> 的共同輔因子，用過由 <strong>DHPR（NADH）</strong>再生。PAH 缺只卡 Phe → Tyr；<strong>BH₄ 缺連 dopamine、serotonin 都下降</strong>，要另補 BH₄ 與神經傳導物質前驅物。"),
 slide("slide-ch18-catabolism","ch18","胺基酸分解總覽",["蛋白質消化與泛素","胺基的去除"],
     "amino acid catabolism amino group carbon skeleton urea cycle citric acid cycle aspartate-argininosuccinate shunt",
     "胺基酸拆成兩半：<strong>胺基</strong> → NH₄⁺ → 尿素循環；<strong>碳骨架</strong> → α-酮酸 → TCA、糖質新生或酮體。",D181,46),
 slide("slide-ch18-transamination","ch18","轉胺作用：胺基交給 α-ketoglutarate",["胺基的去除"],
     "aminotransferase transaminase PLP alpha-ketoglutarate glutamate ALT AST GPT GOT",
     "所有 aminotransferase 都用 <strong>PLP</strong>、都把胺基交給 <strong>α-KG → glutamate</strong>。ALT（GPT）、AST（GOT）是肝、心受損的指標。",D181,48),
 slide("slide-ch18-gdh","ch18","Glutamate dehydrogenase：在肝臟放出 NH₄⁺",["胺基的去除"],
     "glutamate dehydrogenase oxidative deamination NAD NADP mitochondria transdeamination hyperinsulinism hyperammonemia",
     "肝粒線體的 <strong>GDH</strong> 把 glutamate 氧化脫胺成 α-KG + NH₄⁺（可用 NAD⁺ 或 NADP⁺）；轉胺＋GDH = <strong>transdeamination</strong>。GDH 持續活化 → 高胰島素高血氨症候群。",D181,63),
 slide("slide-ch18-glutamine","ch18","Glutamine 把氨運到肝",["氨的運輸"],
     "glutamine synthetase glutaminase ammonia transport liver kidney",
     "多數組織用 <strong>glutamine synthetase</strong>（耗 ATP）把有毒的 NH₄⁺ 裝進 glutamine；到了肝粒線體由 <strong>glutaminase</strong> 放出來進尿素循環。",D181,57),
 slide("slide-ch18-glucose-alanine","ch18","Glucose-alanine cycle：肌肉的氨用 alanine 運",["氨的運輸"],
     "glucose alanine cycle muscle pyruvate ALT liver gluconeogenesis",
     "肌肉把胺基轉給 <strong>pyruvate → alanine</strong> 送到肝；肝再轉回 pyruvate 做糖質新生，葡萄糖送回肌肉（和 Cori cycle 對照）。",D181,60),
 slide("slide-ch18-bicycle","ch18","尿素循環與 TCA 的「Krebs bicycle」",["尿素循環"],
     "aspartate argininosuccinate shunt fumarate malate oxaloacetate urea cycle citric acid cycle linked 3 ATP",
     "尿素循環放出的 <strong>fumarate</strong> → malate → OAA → 轉胺成 <strong>aspartate</strong> 再送回尿素循環。做一個尿素用 3 ATP（4 個高能鍵）。",D181,75),
 slide("slide-ch18-carbon-fates","ch18","碳骨架的七個去向：生醣 vs 生酮",["碳骨架的去向"],
     "glucogenic ketogenic amino acids pyruvate oxaloacetate alpha-ketoglutarate succinyl-CoA fumarate acetyl-CoA acetoacetyl-CoA",
     "進 pyruvate、α-KG、succinyl-CoA、fumarate、OAA → <strong>生醣</strong>；進 acetyl-CoA、acetoacetyl-CoA → <strong>生酮</strong>。⚠️ 圖中「Ketogenic (only)」框列了 Phe、Trp、Tyr，但<strong>純生酮只有 Leu、Lys</strong>，其餘是兩者皆是。",D182,30),
 slide("slide-ch18-thf","ch18","四氫葉酸攜帶的一碳單位",["一碳單位與輔酶"],
     "tetrahydrofolate THF one carbon methyl methylene formyl serine hydroxymethyltransferase",
     "THF 依氧化程度攜帶 –CH₃（最還原）、–CH₂–、–CHO（最氧化）等一碳單位；serine → glycine 是主要來源，用在 purine 與 thymidylate 合成。",D182,13),
 slide("slide-ch18-methyl-cycle","ch18","甲基循環：SAM 與 homocysteine",["一碳單位與輔酶"],
     "SAM S-adenosylmethionine SAH homocysteine methionine B12 betaine choline methylation",
     "Methionine → <strong>SAM</strong>（萬用甲基供體）→ SAH → <strong>homocysteine</strong> → 用 N⁵-methyl-THF 與 <strong>B₁₂</strong>（或 betaine）甲基化回 methionine。",D182,20),
 slide("slide-ch18-heme-synthesis","ch18","Heme 合成：粒線體 → 細胞質 → 粒線體",["Heme 代謝"],
     "heme synthesis delta-aminolevulinic acid synthase ALA PLP succinyl-CoA glycine porphobilinogen protoporphyrin ferrochelatase",
     "Succinyl-CoA + glycine →（<strong>ALA synthase，PLP，限速、被 heme 回饋抑制</strong>）→ ALA → 細胞質 PBG → … → 回粒線體，ferrochelatase 放進 Fe²⁺。",D183,69),
 slide("slide-ch18-porphyrias","ch18","各步驟酵素缺陷對應的紫質症",["Heme 代謝"],
     "porphyria acute intermittent porphyria porphyria cutanea tarda erythropoietic protoporphyria",
     "Heme 合成路徑每一步缺一個酵素就是一種紫質症；最常考 <strong>acute intermittent porphyria</strong>（PBG deaminase）與 <strong>porphyria cutanea tarda</strong>（uroporphyrinogen decarboxylase）。",D183,71),
 slide("slide-ch18-heme-degradation","ch18","Heme 分解：biliverdin → bilirubin",["Heme 代謝"],
     "heme oxygenase biliverdin reductase unconjugated bilirubin conjugated UDP glucuronyltransferase CO",
     "巨噬細胞：<strong>heme oxygenase</strong>（放出 CO、Fe²⁺）→ biliverdin（綠）→ biliverdin reductase → <strong>未結合 bilirubin</strong>（接 albumin）→ 肝臟 UDP-glucuronyltransferase → 結合型 bilirubin。",D183,73),

 # ch22
 svg("ring-sources","ch22","Purine 與 pyrimidine 環的原子來源",["Purine de novo 合成","Pyrimidine de novo 合成"],
     "purine ring glycine glutamine aspartate formyl THF CO2 pyrimidine carbamoyl phosphate CPS II IMP UMP PRPP",
     "Purine：<strong>glycine（C4、C5、N7）</strong>、glutamine（N3、N9）、aspartate（N1）、formyl-THF（C2、C8）、CO₂（C6），在 PRPP 上蓋出 <strong>IMP</strong>；pyrimidine 先做環（carbamoyl phosphate＋aspartate）再接 PRPP → <strong>UMP</strong>。"),
 svg("purine-degradation","ch22","Purine 分解、回收與相關疾病",["核苷酸分解與痛風","Salvage pathway 與相關疾病"],
     "xanthine oxidase allopurinol uric acid gout adenosine deaminase ADA SCID HGPRT Lesch-Nyhan salvage PRPP",
     "Hypoxanthine → xanthine → <strong>尿酸</strong>（xanthine oxidase，allopurinol 抑制）；<strong>HGPRT</strong> 回收 hypoxanthine、guanine（缺 → Lesch-Nyhan）；<strong>ADA</strong> 缺 → SCID。"),
 svg("dtmp-cycle","ch22","dTMP 合成與抗代謝藥",["Ribonucleotide reductase 與 dTMP","抗代謝藥物"],
     "ribonucleotide reductase dATP thymidylate synthase methylene THF DHFR methotrexate 5-FU trimethoprim",
     "RNR 還原 NDP（dATP 抑制）；<strong>thymidylate synthase</strong>（5-FU 抑制）把 dUMP 變 dTMP、產生 DHF；<strong>DHFR</strong>（methotrexate、trimethoprim 抑制）再生 THF。"),
]
# sanity: every svg exists
for f in F:
    if f.get('type') != 'slide':
        assert os.path.exists(os.path.join(ROOT, 'figures', f['id'] + '.svg')), f['id']
# Prettier-style formatting (matches the committed file): 2-space indent,
# lists on one line unless that line exceeds 80 columns (CJK counts as 2).
import unicodedata
dump = lambda v: json.dumps(v, ensure_ascii=False)
width = lambda s: sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)
def field(k, v):
    line = f'    {dump(k)}: {dump(v) if not isinstance(v, list) else "[" + ", ".join(map(dump, v)) + "]"}'
    if isinstance(v, list) and width(line) + 1 > 80:
        line = f'    {dump(k)}: [\n' + ',\n'.join(f'      {dump(x)}' for x in v) + '\n    ]'
    return line
out = '[\n' + ',\n'.join('  {\n' + ',\n'.join(field(k, v) for k, v in f.items()) + '\n  }' for f in F) + '\n]\n'
open(os.path.join(ROOT, 'figures.json'), 'w').write(out)
print(len(F), 'figures')
