#!/usr/bin/env python3
"""寄蟲 113 期中考（第 20–41 題，115 第二組整理）→ subjects/parasitology/data/questions-k113mid.json

來源：slides/parasitology/共筆考古/考古/臨時繳交區/第二組.pdf（與 第二組工作台.docx 內容相同）
- 第 21、27、29、33、35 題原檔「缺失」，不收錄；第 23 題 (C) 選項缺失，保留其餘選項。
- 第 37–41 題是配合題（A–F 共用選項），拆成五題單選／複選。
- 詳解依原檔整理，選項標號錯位處已依題目重排。
執行：python3 tools/build_para_k113mid.py（在 repo 根目錄）
"""
import json

OUT = "subjects/parasitology/data/questions-k113mid.json"
SRC = "113 期中考古"
Q = []
NEG = "選錯誤（否定）題"
POS = "選正確／單一概念題"
CLIN = "臨床情境題"
PAIR = "配對題"


def q(num, ch, stem, opts, ans, exp, pattern=POS, note=None):
    item = {"id": f"k113mid-{num:02d}", "source": SRC, "num": num, "chapter": ch, "type": "mcq", "stem": stem,
            "options": [{"k": k, "t": t} for k, t in zip("ABCDEF", opts)], "answer": list(ans),
            "explain": exp, "topics": ["血絲蟲" if ch == "filaria" else "吸蟲"], "pattern": pattern}
    if note:
        item["note"] = note
    Q.append(item)


q(20, "filaria", "有關河盲症（river blindness）之敘述，下列何者正確？",
  ["受蚊子叮咬而受到 Wuchereria bancrofti microfilaria 感染所引起", "可見 Calabar swellings", "此病症常見於中西非與東南亞",
   "失明的原因是 Onchocerca volvulus microfilariae 侵犯眼部，引起發炎反應", "可藉由血液抹片檢測 microfilariae 輔助診斷"], "D",
  "(A) 河盲症是 Onchocerca volvulus，由黑蠅（Simulium）傳播；W. bancrofti 是淋巴絲蟲（蚊子），而且傳給人的感染期是 L3，不是 microfilaria。\n"
  "(B) Calabar swelling 是 Loa loa（斑虻 Chrysops）。\n(C) 主要流行於撒哈拉以南非洲，另有葉門與中南美少數疫區；東南亞不是主要流行區。\n"
  "(D) ✅ microfilariae 在皮膚移行並侵犯眼睛，死亡時引起強烈發炎，反覆發作造成角膜病變而失明。\n"
  "(E) 經典診斷是 skin snip（皮膚切片）找 microfilariae，不是血液抹片；Mazzotti test 是另一個考點。")
q(22, "trematodes", "吸蟲成長順序？",
  ["cercaria → metacercaria → redia", "egg → redia → adult", "miracidium → sporocyst → cercaria", "egg → cercaria → miracidium"], "C",
  "典型吸蟲：egg → miracidium（纖毛幼蟲）→ sporocyst（胞狀幼蟲）→ redia（雷氏幼蟲）→ cercaria（尾動幼蟲）→ metacercaria（囊狀幼蟲）→ adult。\n"
  "只有 (C) 的先後順序正確（中間省略 redia 但沒有顛倒）。血吸蟲例外：沒有 redia 與 metacercaria，cercaria 直接鑽皮。")
q(23, "trematodes", "毛蚴孵化法（miracidial hatching test）主要可用於檢測下列何種寄生蟲？",
  ["Ascaris", "Schistosoma", "（原題選項缺失）", "Paragonimus westermani"], "B",
  "血吸蟲卵沒有卵蓋，糞便處理後放入清水，卵內已成熟的 miracidium 會孵出，可在光下觀察 → 毛蚴孵化法用於 Schistosoma（尤其 S. japonicum）。",
  note="原題 (C) 選項缺失。")
q(24, "trematodes", "下列何種寄生蟲感染時，患者檢體中可能出現 Charcot-Leyden crystals？",
  ["Dicrocoelium dendriticum", "Fasciola hepatica", "Fasciolopsis buski", "Paragonimus westermani"], "D",
  "Paragonimus westermani（肺吸蟲）：咳嗽、胸痛、鐵鏽色血痰、嗜酸性球增多；痰液中可見蟲卵與 Charcot-Leyden crystals（嗜酸性球崩解產物）。易被誤診為肺結核。")
q(25, "trematodes", "下列何者與日本血吸蟲（Schistosoma japonicum）或其造成的疾病無關？",
  ["Swimmer’s itch", "Granuloma", "Metacercaria", "Katayama fever"], "C",
  "(C) ✅ 血吸蟲沒有 metacercaria（囊狀幼蟲）：螺類釋出的分叉尾 cercaria 直接經皮膚鑽入，尾巴脫落變成童蟲（schistosomulum）。\n"
  "(A) Swimmer’s itch：cercaria 鑽皮時引起的皮膚炎（禽類血吸蟲最典型）。\n(B) 致病主因是蟲卵沉積在肝臟、腸壁 → 遲發型過敏 → 肉芽腫與纖維化。\n"
  "(D) Katayama fever：初次感染數週後、開始大量產卵時的急性全身性過敏與高燒。", pattern=NEG)
q(26, "trematodes", "Fasciola hepatica 是草食性動物常見寄生蟲，下列何者錯誤？",
  ["Halzoun 是因生食感染 Fasciola hepatica 成蟲的動物肝臟而造成", "幼蟲經由膽管逆流而進入總膽管寄生，所以不會破壞肝組織",
   "Fasciola hepatica 無法以 praziquantel 治療", "人類係因食入遭囊狀幼蟲污染的水生植物而感染"], "B",
  "(B) ✅ 錯：吃下 metacercaria → 十二指腸脫囊 → 穿過腸壁 → 腹腔 → 穿過肝被膜 → 在肝實質移行 → 最後進入膽管，所以會破壞肝實質。\n"
  "(A) 生吃含成蟲的動物肝臟 → 成蟲附著咽部 → Halzoun（經典考法）。\n(C) Fasciola 對 praziquantel 效果差，首選 triclabendazole。\n"
  "(D) 吃到附著 metacercariae 的水生植物（如 watercress 水芹）。", pattern=NEG)
q(28, "trematodes", "可產生假性感染（spurious infection）的寄生蟲為：",
  ["Ascaris 和 Trichinella spiralis", "T. spiralis 和 Dicrocoelium dendriticum", "Capillaria philippinensis 和 Capillaria hepatica",
   "Dicrocoelium dendriticum 和 Capillaria hepatica"], "D",
  "假性感染：吃到受感染動物的肝臟，裡面的蟲卵只是「路過」腸道排出，人並沒有被感染。\n"
  "Dicrocoelium dendriticum（吃到羊肝）與 Capillaria hepatica（吃到含卵的動物肝臟；真正感染要吃到胚胎化的卵）都會造成 spurious infection。\n"
  "C. philippinensis 是真正的腸道感染（還會 autoinfection）；Ascaris 是一般腸道感染；T. spiralis 是組織型，糞便不會有卵。")
q(30, "trematodes", "下列何者可判別 Clonorchis sinensis 和 Opisthorchis felineus？",
  ["糞便中蟲卵大小", "嗜酸性白血球數量", "臨床症狀", "患者居住的地區"], "D",
  "兩者蟲卵都是小型、有卵蓋與「肩峰」的芝麻狀卵，大小、症狀（膽管炎、黃疸、膽管癌風險）與嗜酸性球反應都相似。\n"
  "最可靠的區分是地理分布／旅遊史：C. sinensis 在東亞、東南亞（台灣、中國、韓國、越南）；O. felineus 在歐洲與北亞（俄羅斯、西伯利亞、東歐）。")
q(31, "trematodes", "喝生水絕對不會感染下列哪個寄生蟲？",
  ["Fasciolopsis buski", "Schistosoma mansoni", "Fasciola hepatica", "Paragonimus westermani"], "D",
  "Paragonimus westermani 的 metacercaria 在淡水蟹、蝦（第二中間宿主）的組織內，不會游離在水中 → 感染要靠生食或半生食蟹蝦（或轉續宿主的肉），喝生水不會感染。\n"
  "Fasciolopsis、Fasciola 的 metacercaria 附著在水生植物上，也可能脫落浮在水裡；S. mansoni 的 cercaria 在水中游動，喝下時可經口腔黏膜鑽入。", pattern=NEG)
q(32, "trematodes", "關於吸蟲生活史特徵，何者為錯誤的描述？",
  ["有最終宿主及中間宿主", "幼蟲發育過程可在水中動物或水中植物進行", "幼蟲發育至成蟲需經過脫皮", "世代交替及宿主更換現象", "幼蟲有無性增殖現象"], "C",
  "脫皮（molting）是線蟲與節肢動物的特徵。吸蟲（扁形動物）靠變態與無性增殖（sporocyst、redia 在螺體內大量增殖）改變型態，不脫皮。\n"
  "吸蟲有世代交替（有性：成蟲；無性：螺體內幼蟲）與宿主更換（螺 → 第二中間宿主或水生植物 → 最終宿主）。", pattern=NEG)
q(34, "trematodes", "某人至中國旅遊，回台兩週後疑似感染 Schistosoma，可用的檢測方法為？",
  ["direct stool smear examination for eggs", "screening using immunological diagnostic methods", "miracidium hatching method",
   "intestinal mucosal biopsy"], "B",
  "感染兩週時蟲體還是童蟲、尚未產卵（S. japonicum 約 4–5 週後才產卵）→ 糞便抹片、毛蚴孵化法、腸黏膜切片都找不到卵。\n"
  "此時宿主已對尾動幼蟲／童蟲抗原產生抗體 → 只能用免疫學（血清學）方法篩檢。", pattern=CLIN)
q(36, "trematodes", "下列何者不會造成腦部病理傷害？",
  ["Heterophyes heterophyes", "Schistosoma japonicum", "Paragonimus westermani", "Dicrocoelium dendriticum"], "D",
  "Dicrocoelium dendriticum 的蟲體與蟲卵侷限在肝膽系統，不會異位到腦。\n"
  "(A) Heterophyes：蟲卵可穿過腸黏膜進入血流，異位到心臟、腦、脊髓。\n(B) S. japonicum：所有血吸蟲中最容易讓蟲卵進入中樞神經（腦肉芽腫、癲癇）。\n"
  "(C) Paragonimus：童蟲移行時最常見的異位部位就是腦（膿瘍、囊腫）。", pattern=NEG)

MATCH = ["Fasciolopsis buski", "Clonorchis sinensis", "Heterophyes heterophyes", "Fasciola hepatica", "Eurytrema spp.", "Opisthorchis felineus"]
MSTEM = "（配合題，選項 A–F 共用）"
q(37, "trematodes", MSTEM + "成蟲體型最小的是？", MATCH, "C",
  "Heterophyes heterophyes 體長僅約 1.0–1.7 mm，是人體寄生吸蟲中最小的（腸吸蟲）；最大的是 Fasciolopsis buski（薑片蟲）。", pattern=PAIR)
q(38, "trematodes", MSTEM + "吃水生植物可能感染？", MATCH, "AD",
  "附著在水生植物的 metacercaria：Fasciolopsis buski（荸薺、菱角、茭白筍）與 Fasciola hepatica（水芹 watercress）。",
  pattern=PAIR, note="原檔詳解只寫 (A)；Fasciola hepatica 也是吃水生植物感染（見第 26 題），本站 A、D 都算對。")
q(39, "trematodes", MSTEM + "哪些中間宿主是昆蟲？", MATCH, "E",
  "Eurytrema（胰吸蟲，如 E. pancreaticum）：第一中間宿主是陸生蝸牛，第二中間宿主是草螽（蝗蟲類昆蟲）。", pattern=PAIR)
q(40, "trematodes", MSTEM + "用 Praziquantel 治療效果差的是？", MATCH, "D",
  "Fasciola hepatica 對 praziquantel 反應差，首選 triclabendazole；其他吸蟲多以 praziquantel 治療。", pattern=PAIR)
q(41, "trematodes", MSTEM + "吃生魚片可能感染？（複選）", MATCH, "BCF",
  "第二中間宿主是魚的吸蟲：Clonorchis sinensis（淡水魚，草魚、鯉魚）、Heterophyes heterophyes（淡水／半鹹水魚，吳郭魚、烏魚）、Opisthorchis felineus（淡水魚）。", pattern=PAIR)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=1)
print(f"{len(Q)} 題 → {OUT}")
