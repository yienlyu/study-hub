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

D17, D12, D21, D23 = ("W1 Ch17 Lipid metabolism", "W2 Ch12 Biochemical Signaling",
                     "W3 Ch21 Lipid Biosynthesis", "W4 Ch23-1 Hormonal regulation")
F = [
 # ch17
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
 svg("insulin-secretion","ch23","β 細胞的胰島素分泌",["胰島素與 GLUT"],
     "beta cell GLUT2 ATP sensitive K channel depolarization calcium exocytosis incretin GLP-1 sulfonylurea",
     "血糖 ↑ → ATP/ADP ↑ → <strong>K-ATP 通道關閉 → 去極化 → Ca²⁺ 流入</strong> → insulin 胞吐。"),
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
 svg("phe-tyr-diseases","ch18","Phe／Tyr 代謝與先天疾病",["先天胺基酸代謝疾病","胺基酸衍生物"],
     "phenylketonuria phenylalanine hydroxylase BH4 albinism tyrosinase alkaptonuria homogentisate catecholamine dopamine",
     "PAH（BH₄）缺 → <strong>PKU</strong>；tyrosinase 缺 → <strong>albinism</strong>；homogentisate dioxygenase 缺 → <strong>alkaptonuria</strong>。"),
 # ch22
 svg("dtmp-cycle","ch22","dTMP 合成與抗代謝藥",["Ribonucleotide reductase 與 dTMP","抗代謝藥物"],
     "ribonucleotide reductase dATP thymidylate synthase methylene THF DHFR methotrexate 5-FU trimethoprim",
     "RNR 還原 NDP（dATP 抑制）；<strong>thymidylate synthase</strong>（5-FU 抑制）把 dUMP 變 dTMP、產生 DHF；<strong>DHFR</strong>（methotrexate、trimethoprim 抑制）再生 THF。"),
]
# sanity: every svg exists
for f in F:
    if f.get('type') != 'slide':
        assert os.path.exists(os.path.join(ROOT, 'figures', f['id'] + '.svg')), f['id']
json.dump(F, open(os.path.join(ROOT, 'figures.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'figures.json'), 'a').write('\n')
print(len(F), 'figures')
