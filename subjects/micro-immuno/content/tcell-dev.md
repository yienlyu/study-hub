=== summary ===

# TCR、T 細胞發育與 TCR 訊息傳遞（陳玫潔）

> 這堂課分三段：① T cell receptor 基因重組與多樣性 ② T 細胞在胸腺的發育與篩選 ③ TCR 訊息傳遞與三訊號活化。

## 1. TCR–CD3 複合體

- T 細胞辨識的是：**蛋白抗原切成的 peptide，由 APC 呈現、結合在 self MHC 上，被抗原專一的 TCR 辨識**。
- **TCR complex = TCR + CD3**：(αβ)₂ 或 (γδ)，加上 CD3 的 **γ、δ、ε₂、ζ₂**。
  - CD3 有 6 條鏈、排成 3 對：**εδ、εγ、ζζ**。CD3 的 δ、ε、γ 和 Ig 的同名鏈無關。
  - **TCR 本身不能傳訊**，靠 CD3 與 ζ 鏈上的 **ITAM**（immunoreceptor tyrosine activation motif）。
- TCR 像一個**膜上的 Fab 片段**：α（40–50 kDa）、β（35–47 kDa），各有 V、C domain；V 上有 CDR1、2、3，**CDR3 位在抗原結合位中央、最多變**，負責接 MHC 槽裡的 peptide。
- **Co-receptor CD4 / CD8**：結合 MHC、增加 avidity，並帶 **Lck** 參與訊息傳遞。

<div data-fig="tcr-cd3"></div>

## 2. TCR 基因

|        | α 鏈      | β 鏈                          | γ 鏈      | δ 鏈                                   |
| ------ | --------- | ----------------------------- | --------- | -------------------------------------- |
| 類比   | ≈ Ig 輕鏈 | ≈ Ig 重鏈                     | ≈ 輕鏈    | ≈ 重鏈                                 |
| 片段   | V–J–C     | V–D–J–C–D–J–C（**兩組 DJC**） | V–J–C–J–C | V–D–J–C                                |
| 染色體 | 14        | 7                             | 7         | 14（**在 α 基因座內，Vα 與 Jα 之間**） |

- β 鏈和 Ig 重鏈相比：**D 片段較少、有 2 組 J 和 C**。
- 同樣遵守 **RSS 12/23 rule**、**allelic exclusion**。
- **Vα 接到 Jα 時，中間的 δ 基因座會被刪除** → 產生 αβ 的細胞不會再有 δ。
- **Rearrangement rescue**：α 鏈有很多 Vα、很多 Jα，第一次重組沒成功可以用外側的 V、內側的 J **再重組一次**，直到產生有功能的 α 鏈並通過 positive selection，否則細胞死亡。

## 3. TCR 多樣性 ⭐

| 機制                                          | Ig               | TCR                                                    |
| --------------------------------------------- | ---------------- | ------------------------------------------------------ |
| 多個 germline V / D / J                       | ✅               | ✅（Vα ~100、Jα ~50 → J 很多）                         |
| Junctional diversity（P、N nucleotides，TdT） | ✅               | ✅                                                     |
| **D 片段以三種讀框讀取**                      | 很少             | **β 鏈常見**                                           |
| **多個 D 串接（alternative joining of D）**   | ❌（只能 V–D–J） | **δ 鏈常見**（Vδ–Jδ、Vδ–Dδ–Jδ、Vδ–Dδ–Dδ–Jδ），β 鏈偶爾 |
| **Somatic hypermutation**                     | ✅               | **❌**                                                 |
| 重鏈輕鏈組合                                  | ✅               | ✅                                                     |
| 理論總多樣性                                  | ~5 × 10¹³        | **~10¹⁸**                                              |

- **CDR3 最多變**：α 鏈 CDR3 由 V 尾端 + J 開頭組成；β 鏈 CDR3 由 V、D、J 連接處加上隨機核苷酸組成。
- 所以 TCR 雖然**沒有 SHM**，但理論多樣性比 Ig 還高（J 多、D 可三框讀、多 D 串接）。

## 4. αβ vs γδ T 細胞

|              | αβ T                    | γδ T                              |
| ------------ | ----------------------- | --------------------------------- |
| 佔 CD3⁺ 細胞 | **90–99%**              | **1–10%**                         |
| V 基因庫     | 大                      | 小                                |
| CD4⁺         | ~60%                    | <1%                               |
| CD8⁺         | ~30%                    | ~30%                              |
| CD4⁻CD8⁻     | <1%                     | **~60%**                          |
| MHC 限制     | CD4⁺→MHC II、CD8⁺→MHC I | **無 MHC restriction**            |
| Ligand       | peptide + MHC           | **phospholipid 抗原**（整段分子） |
| 角色         | 專一性免疫主力          | 偏先天免疫、黏膜上皮              |

## 5. 胸腺中的 T 細胞發育 ⭐⭐

- T 前驅細胞在胸腺**大量增殖，但大多數死亡**；只有約 **2–5%** 成為 single positive 離開。
- 胸腺結構：**皮質**（未成熟 thymocyte、cTEC、macrophage）→ **皮髓交界** → **髓質**（成熟 thymocyte、mTEC、DC、macrophage）。
- 前驅細胞從**皮髓交界的小靜脈**進入，往**被膜下（subcapsular）**移動，再往髓質走。

<div data-fig="thymus-zones"></div>

### 發育階段（CD 標記）

| 階段           | 標記                    | 位置 / 事件                                                                                                              |
| -------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **DN1（ETP）** | c-kit⁺⁺ CD44⁺ CD25⁻     | **Notch1** 決定走 T 系（不走 NK、B、myeloid）                                                                            |
| **DN2**        | c-kit⁺⁺ CD44⁺ **CD25⁺** | **TCR γ、δ、β 基因座開始重組**（α 不重組）；決定 γδ 或 αβ                                                                |
| **DN3**        | c-kit⁺ CD44⁻ CD25⁺      | αβ 系（95%）；**β-selection checkpoint**：β 鏈 + **pre-Tα（surrogate α chain）** 形成 **pre-TCR** → β 重組停止、細胞增殖 |
| **DN4**        | c-kit⁻ CD44⁻ CD25⁻      | **TCR α 基因座開始重組**                                                                                                 |
| **DP**         | CD4⁺CD8⁺ αβTCR⁺         | 皮質：positive selection                                                                                                 |
| **SP**         | CD4⁺ 或 CD8⁺            | 髓質：negative selection → 離開胸腺                                                                                      |

- DN 階段**不依賴 TCR**（TCR-independent）；DP 之後的 positive / negative selection **主要依賴 TCR 交互作用**。
- γδ 系在 DN2–DN3 分出去，表型幾乎不再改變（CD4⁻CD8⁻）。

### Affinity model（Fig. 8.25）⭐

| TCR 對 self peptide:self MHC 的親和力 | 結果                                                                      | 負責細胞                 |
| ------------------------------------- | ------------------------------------------------------------------------- | ------------------------ |
| 無 / 太低                             | **Death by neglect**（沒有存活訊號）                                      | cTEC                     |
| 低～中等                              | **Positive selection**：得到 TCR-dependent 存活訊號 → **MHC restriction** | **cTEC**                 |
| 中高                                  | **Alternative selection** → **Treg**、NKT、IEL、MAIT                      | mTEC                     |
| 太高                                  | **Negative selection = clonal deletion** → **self-tolerance**             | **mTEC**、DC、macrophage |

- **Positive selection 決定 CD4 / CD8 命運**：TCR 辨識 cTEC 上的 **MHC II → CD4⁺ 成熟**；辨識 **MHC I → CD8⁺ 成熟**（co-receptor 與 TCR 辨識同一種 MHC，Lck 訊號才夠強）。

<div data-fig="thymus-selection"></div>

<div data-fig="positive-selection"></div>

## 6. TCR 訊息傳遞與 T 細胞活化 ⭐⭐

### Immunological synapse

- 中心：**TCR、co-receptor**；周圍：**黏附分子**。
- 初始黏附：**LFA-1（CD11a:CD18 integrin）↔ ICAM-1（CD54）、ICAM-2（CD102）**；**CD2 ↔ CD58**。TCR 辨識抗原後，LFA-1 構型改變、親和力增加。
- 不同的 selectin 與 integrin 讓淋巴球進入不同淋巴組織（naïve T 以 **L-selectin** 經 HEV 進淋巴結）。

<div data-fig="t-signal-summary"></div>

### 三種訊號

| 訊號                              | 分子                               | 作用                 |
| --------------------------------- | ---------------------------------- | -------------------- |
| （先）黏附                        | LFA-1–ICAM-1/3、CD2–CD58           | 讓 T 與 APC 接觸夠久 |
| **Signal ①** 抗原專一活化         | **TCR + CD4/CD8 ↔ pMHC**           | 決定專一性           |
| **Signal ②** 共刺激（**存活**）   | **CD28 ↔ B7（CD80/CD86）**         | 沒有 → **anergy**    |
| **Signal ③** 細胞激素（**分化**） | IL-1、IL-2 / **CD25（IL-2Rα）** 等 | 決定分化方向         |

<div data-fig="t-signals"></div>

### Signal ① 路徑

**CD4/CD8 帶 Lck → Lck 磷酸化 CD3 與 ζ 的 ITAM → ZAP-70 結合 ζ 上磷酸化的 ITAM 並被活化 → 下游（PLC-γ、Ca²⁺、Ras）→ 轉錄因子 NFAT、AP-1、NF-κB → IL-2 基因轉錄**。

<div data-fig="lck-zap70"></div>

### Signal ② 共刺激

- **CD28–B7**：誘導 **IL-2** 與**高親和力 IL-2 受體（CD25）** 表現 → 增殖存活。
- **ICOS**（inducible co-stimulator）：活化後才表現。
- **TNF receptor superfamily**：**CD40（B 細胞上的重要共刺激分子）–CD40L**、4-1BB、OX40 等 → 活化 **non-canonical NF-κB**，加強並延續 T 細胞反應。
- **抑制性受體**：
  - **CTLA-4（CD152）**：對 B7 的親和力比 CD28 **高 20 倍以上**，搶走 B7 → 關掉活化。
  - **PD-1**：與 PD-L1 結合抑制 T 細胞；腫瘤利用它躲避免疫。
  - **2018 諾貝爾**：James Allison（CTLA-4）、Tasuku Honjo（PD-1）→ immune checkpoint blockade。

<div data-fig="checkpoints"></div>

- **Effector T 細胞不再需要共刺激**：活化分化後只需 Signal ① 就能作用（所以 CTL 在周邊組織殺感染細胞不需要 B7）。

<div data-fig="effector-no-costim"></div>

## 🎙️ 上課錄影重點（陳玫潔，09/30）

- 上課前提：自學 MHC 課（大亨堡怎麼做）；peptide 放上 MHC **不具專一性但一定要穩定**。TCR 是**細胞免疫專一性的來源**、雙重辨識；不符合條件的 T 細胞在發育中大量死亡，「**完全靠親和力決定，過猶不及都不可以**」。
- TCR 和 BCR 的重組邏輯相同（RSS、RAG1/RAG2），老師「只講不一樣的地方」。**TCR 做完就不再改造** → 只能「先準備好、只篩選不改造」→ 多樣性必須比抗體更多；抗體則挑選後還會 somatic hypermutation 與 class switch。
- αβ（約 95%，教科書幾乎都在講）辨識 peptide；**γδ 辨識的不是 peptide**（常是脂質 / phosphorylated antigen，認一個長得像 MHC 但不是 MHC 的分子，老師記得像 CD1d）→ **沒有 MHC restriction**；與**黏膜免疫**有關，偏向 CD8 / 毒殺功能；「上我的課就再也不會看到這個細胞了」。
- **TCR complex = 白雪公主（TCR αβ，專一辨識但沒有胞內區、不能傳訊）+ 六個小矮人（CD3：εδ、εγ、ζζ，有時 ηη；負責傳訊）**；兩者以**正負電、非共價**結合（「你跟同學也很難共價鍵結」）。CD3 = T 細胞的定義 marker。
- **Coreceptor**：CD4 結合 MHC II 的 **β2**（老師補充：精確來說還有一點 α2）；CD8 結合 MHC I 的 **α3**；決定與哪種 MHC 結合，並增加整體 **avidity**；β2m 壞掉 MHC I 也做不出來 → 免疫缺失。
- TCR 有 CDR1、2、3；**CDR3 在正中間、變異最大（「C 位中的 C 位」）**，對應到基因上 **α 的 V–J 接合處、β 的 V–D–J 接合處**（junctional diversity 在這裡加花樣）。Tonegawa（1987 諾貝爾）發現抗體變異來源（gene segments）。
- CD3 的 **ITAM** 靠 tyrosine 磷酸化傳訊（ITIM 是抑制）。
- **Allelic exclusion**：TCR、BCR 都有，MHC 沒有（codominant）。重組失敗不會馬上放棄：還可以用**前面其他 V / 後面其他 J 再重組「敗部復活」**，試到不能試才換另一個 allele。
- Segment 的起源推測是 **transposon**（玉米的花色、McClintock）。
- **12/23 rule**：12 bp spacer 的 RSS 一定配 23 bp 的 → 確保 V–D–J 順序、不能跳過 D。TCR β / δ 的 D 兩側是 12 與 23（抗體 heavy chain 的 D 兩側都是 12）→ 老師說「**我不會很無良地考出來**」。
- 基因位置：TCRα 在 **14 號染色體**（V、J、C）；β 為 V…D-J-C、D-J-C（**D 分散**）；**δ 基因藏在 α 基因座內**（V 與 J 之間）且 **D 全部聚在一起**。→ ① **α 一重組，δ 就被切掉** → 這顆細胞不可能變 γδ；② δ 的 D 相鄰且 12/23 可互接 → **multiple D**（β 的 D 太遠接不起來）。
- **課堂投票：β 與 α 誰先重組？→ β 先**。β 做出來時以 **surrogate α（pTα）** 組成 pre-TCR 也能傳訊、讓細胞存活發育；α 重組完再取代 surrogate。「只要一個地方壞掉，細胞就會走向死亡」。
- TCR 獨有：**D segment 三個 reading frame 都能讀**（抗體重組 9 種 frame 中只留 in-frame 的 1/9）、**multiple D（δ 獨有）**、**N-addition 在 TCR 較常見**（TdT）。總 repertoire：**抗體約 10¹³、TCR 約 10¹⁸（差 10⁵）**。為什麼要那麼多？因為發育時要死掉約 99%（以量取勝，像海龜生很多蛋）。
- 抗體獨有的 somatic hypermutation 像「用砂紙精磨鑰匙」，與 FDC 搶抗原，搶得過拿到「免死金牌」→ 所以疫苗要打 **booster**（越來越強，像煉蠱）。**V(D)J 重組是亂數、不受調控；class switch 受 T 細胞 cytokine 控制**（cytokine 很短、易裂解、不會「遙指杏花村」→ 需要 T–B 直接接觸）。
- **胸腺發育**：胸腺新生兒時比例最高、老了退化。**重組與挑選都在胸腺**。Thymocyte 像「巡迴演唱會」：從 medulla 附近進入 → 往 capsule → 再往內走（cortex → medulla）。胸腺不碰外來抗原 → 「考官」帶 self MHC + self peptide。
- **AIRE** 基因讓全身基因都在胸腺表現（才能把會攻擊自己的殺掉）→ 壞掉 = 非常嚴重的免疫疾病；這屬於 **central tolerance**。考官有兩種：**cTEC**（主要做 positive selection）與 **mTEC**；兩者挑選的親和力不同。
- 階段：**DN1–DN4（重組中，不需要 CD4 / CD8）→ DP（準備給考官迎頭痛擊）→ SP**；看當初跟哪個考官的 MHC II 或 MHC I 接觸決定 CD4 或 CD8；出胸腺時是 **mature but naive**。若有人說要抽周邊血研究 DP / DN 細胞「聽起來就匪夷所思」。γδ 在重組時就分出、不參加「資格考」。
- **Affinity model（「重點就只有那張有兩個墓碑的圖」）**：完全不結合 = **no selection，死最多（90–99%）**（「漂浮的幽靈，留它幹嘛」）；中等親和力 = 存活（大部分對抗病原的細胞）；偏高 = 發育成 **Treg / NKT** 等（抑制型、數量少）；過高 = **negative selection、clonal deletion**。10¹⁸ 死 99% 還剩至少 10¹⁶。挑選沒做好 → autoimmunity 或 immunodeficiency。人的體質、荷爾蒙會變 → 需要 **peripheral tolerance**（Treg；老師提到近年有日本學者以此獲諾貝爾獎）。「概念一直在更新，掌握重點、不要拘泥細節」。
- **三種訊號**：signal 1 = TCR + coreceptor（白雪公主與小矮人合作體）；signal 2 = 共刺激（像**手槍的保險栓**）——保險卡死時 TCR 能辨識也沒用（腫瘤微環境）；signal 3 = APC 的 cytokine 影響 T 細胞分化（sensor cell 概念，下一堂細講，「可以講兩個小時以上」）。
- **免疫突觸**：先靠周邊**黏附分子（LFA-1–ICAM-1 等）**穩住兩個細胞（細胞膜像海中竹筏，蛋白會飄走；「你總要有機會接觸才能進一步了解」）→ TCR 才辨識專一性；TCR 活化會增加 integrin **親和力**（構形改變）。cytokine 是**彼此交換**的。
- **L-selectin = 「守宮砂」**：naive T 才表現 → 經 **HEV** 進入淋巴結；活化後不再表現 → effector T 不能再回淋巴結（「去周邊乖乖做事，不然就戰死」）。
- **只有 signal 1 沒有 signal 2 → anergy**：處於 G0、不增殖也不會死，「就是個殭屍」。
- Signal 1 傳遞：coreceptor 上的 **Lck** 磷酸化 ITAM → **ZAP-70** → PLC、AKT 等 → **NFAT** → **IL-2** 與 **IL-2 receptor**（自己餵自己）。老師說「**不會很無良地挖洞問訊息傳導中間哪個分子最重要**」。
- Signal 2：**CD28–B7 = 「簡配」（一定要有）**；ICOS、TNF 家族為「選配」——**CD40L（T）–CD40（B、macrophage）** 常見於 T–B 互相活化；CD8 常見 **4-1BB–4-1BBL**。
- 負向：**CTLA-4 與 CD28 搶 B7，親和力高 20 倍**（「程咬金」）→ 活化後期表現來關掉反應；**PD-1–PD-L1** 另一個抑制訊號；兩者癌細胞都會利用 → 抗體阻斷 → T 細胞 reactivate（**2018 諾貝爾：Allison 因母親卵巢癌研究 CTLA-4、在 MD Anderson 愛吹口琴；本庶佑 PD-1、很常來台灣**），臨床已在用、也有 combination therapy。
- **Effector T 到周邊只需 signal 1**（priming 在淋巴結才需要共刺激；周邊沒人給 signal 2）。

=== slides ===

# W4-2 上課 slides 重點：TCR、T development、TCR signaling（陳玫潔，2026/9/30）

> 共 60 頁，三份 slides 合併。

**Part 1 — T Cell Receptor（p.1–24）**

- Key subjects：TCR gene segments、generation of TCR diversity、**differences between Ig and TCR**。
- What do T lymphocytes recognize?（peptide / APC / self MHC / Ag-specific TCR）。
- **TCR complex = TCR + CD3**：(αβ)₂, γ, δ, ε₂, ζ₂；CD3 三對 εδ、εγ、ζζ；CD4、CD8 co-receptors 增加 avidity 並參與訊息傳遞；CDR1–3、**ITAM**。
- TCR families：αβ（專一性免疫最常見）vs γδ（先天免疫主要 T 細胞家族）。
- Fig 4.17 / 4.19a：TCR resembles a membrane-bound Fab。
- Review of TCR genes：α ~ L chain、β ~ H chain，**EXCEPT fewer D、2 sets of J and C**；allelic exclusion；RSS 12/23 rule（Fig 5.6）。
- Fig 5.14（α 在 chr14、β 在 chr7）、Fig 5.19（γ、δ loci）、Fig 5.20：**Vα→Jα 重組刪除 δ locus**。
- Fig 5.15 / 5.2：**CDR3 比 CDR1、2 多變**；α 的 CDR3 = V 尾 + J 頭；β 的 CDR3 = V、D、J + 隨機核苷酸。
- 多樣性四來源：junctional diversity、P & N additions（TdT）、**D 三框讀取**、**多 D 串接（δ 鏈）**。
- **Fig 5.17 表**：Ig 總多樣性 ~5×10¹³，αβ TCR ~10¹⁸（β 的 D 常三框讀、Jα ~50）。
- **Table 9-1**：αβ vs γδ 比例、CD4/CD8 表型、MHC restriction、ligands。
- **Table 9-3**：TCR **沒有 somatic mutation**；D 的 alternative joining：β（some）、δ（often）。

**Part 2 — Development of T lymphocytes（p.25–33）**

- Key subjects：前驅細胞在胸腺大量增殖但多數死亡；CD 標記代表發育階段；TCR 重組、表現與訊號調控發育；**affinity model**；positive selection 協調 CD4/CD8 與 TCR 專一性。
- Fig 8.16 胸腺構造、Fig 8.20 DN / DP / SP 位置。
- **Fig 8.23** αβ T 細胞基因重組階段：Dβ→Jβ → Vβ→DJβ → **β + surrogate α（pTα）表面表現、β 重組停止、增殖、誘導 CD4/CD8、α 開始轉錄** → Vα→Jα → αβ:CD3 表現、開始篩選。
- **Fig 8.24**：多次連續重組可救回失敗的 TCRα（跳山羊圖）。
- **Fig 8.25**：affinity model（cTEC / mTEC；death by neglect、positive、alternative → Treg / NKT / IEL / MAIT、negative → clonal deletion）。
- Fig 8.28：cTEC 上 MHC II → CD4⁺；MHC I → CD8⁺。
- **Fig 8.18**：DN1（ETP，Notch1）→ DN2（TCR γ、δ、β 重組）→ DN3（β-selection）→ DN4（TCR α 重組）→ DP → SP；DN 為 TCR-independent。

**Part 3 — TCR signaling and T cell activation（p.34–60）**

- Key subjects：immunological synapse、**Signal ①** TCR 訊息傳遞、**Signal ②** T 細胞存活、**Signal ③** T 細胞分化。
- Intracellular signals：adhesion（LFA-1–ICAM-1/3）→ ① CD2–CD58、TCR + CD8/4–MHC → ② CD28–B7 → ③ IL-1、IL-2 / CD25。
- **Fig 9.18**：LFA-1（CD11a:CD18）↔ ICAM-1（CD54）、ICAM-2（CD102）；CD2 ↔ CD58。Fig 9.5 / 9.19 / 9.6。
- Fig 9.20 / 9.21：三種訊號與 clonal expansion。
- Fig 7.9 ITAMs、Fig 4.30–4.31 CD4 / CD8 構造、**Fig 7.12 Lck → ITAM → ZAP-70**、Fig 7.16 / 7.19 / 7.30 NFAT。
- **CD28-dependent co-stimulation 誘導 IL-2 與高親和力 IL-2 受體**；ICOS；Fig 7.32 多條路徑匯集到 IL-2 promoter。
- Fig 7.33 CD40；Fig 9.32 TNF receptor family；Fig 9.28 non-canonical NF-κB。
- **Fig 7.34 / 9.27：CTLA-4 對 B7 親和力比 CD28 高 >20 倍**；PD-1；Fig 7.31；2018 Nobel。
- **Fig 9.29：effector T 細胞不需要共刺激**。

=== exam ===

# 考點分析

## 🔥 高頻考點（去年考古）

1. **Negative selection 機制**：辨識 self-antigen → **主動誘發凋亡**；T、B 細胞都有。Positive selection 才決定 MHC restriction。
2. **Positive selection 與 self-tolerance「最不相關」**（它和 MHC restriction 有關）。
3. **γδ T 細胞**：不受 MHC 限制、不是從 αβ T 衍生、源自骨髓、在胸腺成熟。
4. **TCR 敘述**：與 CD3 一起傳訊、在胸腺重組、CDR3 最多變；「**因為沒有 SHM，所以多樣性遠小於 BCR**」是錯的（TCR ~10¹⁸ > Ig ~5×10¹³）。
5. **δ 基因位於 α 基因座的 V 與 J 之間**。
6. **HIV 經 CD4 感染 helper T**。
7. **Naïve T 細胞的第二訊號是 CD28**；**CTLA-4 結合 B7**。
8. **不參與 TCR 胞內訊息傳遞的膜蛋白是 CD4**（考古答案；CD3γ、CD3ε、CD3ζ 都有 ITAM）。
9. MHC I / II 缺陷小鼠 → **卡在 DP 階段**；骨髓來源 APC 在 negative selection 最重要，因為能在 MHC I、II 上呈現 self peptide。

## 🆕 今年 slides 新強調、可能出題

- **DN1–DN4 的 CD44 / CD25 / c-kit 標記**，以及哪個階段重組哪條鏈（DN2：γ、δ、β；DN4：α）。
- **β-selection、pre-TCR（surrogate α chain / pTα）**。
- **Affinity model 四種結果**，alternative selection 產生 Treg、NKT、IEL、MAIT。
- **Ig vs TCR 多樣性表**：D 三框讀取（β 常見）、多 D 串接（δ 常見）、TCR 無 somatic mutation、總多樣性 10¹⁸。
- **αβ vs γδ 表**（比例、CD4/CD8 表型、ligand = phospholipid）。
- **黏附分子配對**：LFA-1（CD11a:CD18）–ICAM-1（CD54）、ICAM-2（CD102）；CD2–CD58。
- **Lck → ITAM → ZAP-70 → NFAT → IL-2** 順序題。
- **CTLA-4 > CD28 二十倍**、PD-1、2018 諾貝爾；effector T 不需共刺激。

## 📝 出題模式

- 陳玫潔老師的題目偏長、英文敘述（Abbas / Janeway 題庫風格），常見實驗情境題（TCR transgenic mice、缺陷小鼠）。
- 表格型比較（αβ vs γδ、Ig vs TCR）很適合出「何者錯誤」。

## 🎙️ 老師課堂提示

- 老師說**不會考**：12/23 rule 的細節（「不會也沒關係，我們不會考這個東西」）、β/δ 的 D 兩側 RSS 差異、多樣性的確切次方數字、訊息傳導路徑中「哪個分子最重要」的挖洞題。
- 老師強調的重點：**β 先於 α 重組（surrogate α）**、**α 重組會切掉 δ**、**CDR3 對應接合處**、**TCR 10¹⁸ > Ig 10¹³**、affinity model（「重點只有那張兩個墓碑的圖」）、AIRE 與 central tolerance、**anergy = 只有 signal 1**、CTLA-4 親和力 20 倍、effector T 不需 signal 2。

## 📒 百十四共筆對照（W04-1）

- 黏附分子：老師要大家掌握「**穩定接觸、調控歸巢、活化後提高 integrin 親和力**」的概念，**各種配對的細節不必逐一背**（L-selectin–GlyCAM-1／CD34 進 HEV、LFA-1–ICAM-1、α4β7–MAdCAM-1 黏膜歸巢）。
- 只有 signal 1、沒有 signal 2 → **anergy**：細胞仍能辨識抗原但無法正常活化，**不等於立即死亡**。負向訊號（如腫瘤微環境）讓能辨識腫瘤的 T 細胞無法反應 → 免疫檢查點阻斷就是解除這些抑制。
- 活化後的代謝轉換：由**氧化磷酸化**為主轉向**有氧糖解（aerobic glycolysis）**；細胞由 **G0** 進入細胞週期、clonal expansion。

## ⚠️ 陷阱整理

| 容易選錯                                    | 正確                                                                                                |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Positive selection 與 self-tolerance 最相關 | Positive selection 決定 **MHC restriction**；**negative selection** 才是 self-tolerance（主動凋亡） |
| TCR 沒有 SHM，所以多樣性比 BCR 小           | TCR 約 **10¹⁸ > Ig 約 5×10¹³**（junctional diversity 大）                                           |
| α 鏈先重組                                  | **β 先重組（DN2–3）**，與 **pTα（surrogate α）** 組成 pre-TCR → β-selection；α 在 DN4／DP           |
| δ 基因在 β 基因座                           | **δ 在 α 基因座的 V 與 J 之間** → α 重組會**切掉 δ**                                                |
| γδ T 由 αβ T 衍生、受 MHC 限制              | γδ **不受 MHC 限制**、不是 αβ 衍生；配體可為 phospholipid                                           |
| CD4 有 ITAM 參與 TCR 訊息                   | CD3γ、δ、ε、ζ 有 ITAM；**CD4 是考古答案「不參與胞內訊息」**                                         |
| MHC 缺陷小鼠卡在 DN                         | MHC I／II 缺陷 → **卡在 DP**（無法 positive selection）                                             |
| Naïve T 第二訊號是 CTLA-4                   | 第二訊號是 **CD28–B7**；CTLA-4 也結合 B7，但**親和力高約 20 倍**、傳抑制訊號                        |
| Anergy 是缺 signal 1                        | **Anergy = 只有 signal 1、沒有 signal 2**                                                           |
| ZAP-70 磷酸化 ITAM                          | **Lck** 磷酸化 ITAM → **ZAP-70** 結合 → … → NFAT → IL-2                                             |
| Effector T 仍需共刺激                       | **Effector T 不需共刺激**（CTL 在周邊只需 signal 1）                                                |
| LFA-1 結合 CD58                             | **LFA-1（CD11a:CD18）–ICAM-1／-2**；**CD2–CD58（LFA-3）**                                           |
