# 考前速記表
<!-- 每張卡片以「## 標題」開頭；「@ch 章節id」加章節連結、「@fig 圖id」加觀念圖按鈕。內容全部整理自各章重點，以公式與計算例為主。
     數學式：$$…$$ 獨立成段 = 置中公式（區塊內每一行一條公式，不要用 \qquad 並排）；行內 $…$；表格裡用 $$…$$ 得到分數樣式（表格裡的 TeX 不能有 |）。 -->

## 三段五級預防（不用算，但每年必考）
@ch intro,screening
@fig slide-prevention
| 三段 | 五級 | 例子 |
|---|---|---|
| 初段 | 第一級 健康促進 | 衛教、飲食、運動 |
| 初段 | 第二級 特殊保護 | **預防接種**、安全帽 |
| 次段 | **第三級 早期診斷、適當治療** | **篩檢** |
| 三段 | 第四級 限制殘障 | 防惡化、併發症 |
| 三段 | 第五級 復健 | 中風復健 |

- 題目寫「**級**」用五級、寫「**段**」用三段：**篩檢 = 次段 = 第三級**。陳老師說三段五級可能出兩到三題。

## 病原三特性
@ch transmission
@fig infectivity
| 特性 | 公式（×100%） |
|---|---|
| **感染力 Infectivity** | $$\dfrac{\text{感染人數}}{\text{易感受者}}$$ |
| **致病力 Pathogenicity** | $$\dfrac{\text{發病人數}}{\text{感染者}}$$ |
| **毒性 Virulence**（致死率） | $$\dfrac{\text{死亡人數}}{\text{發病者}}$$ |

- 分母一層一層往下：**易感受者 → 感染者 → 發病者**。受到感染不一定會發病。

## R0、群體免疫閾值、侵襲率
@ch transmission
@fig herd-threshold
$$\text{HIT} = 1 - \frac{1}{R_0}$$

- $R_0 = 2$ → 50%；麻疹 $R_0$ 12–18 → 92–94%；Delta 5.1 → 約 80%；流感 1.3 → 23%。
- **$R_0 < 1$ 消失；$= 1$ endemic；$> 1$ epidemic**。**$R_t$ 持續 $< 1$ = 受控制**。$R_0$ 是傳播速度，跟毒性無關。

$$\text{Attack rate} = \frac{\text{有風險且發病}}{\text{有風險的總人數}}$$

$$\text{Secondary AR} = \frac{\text{接觸者中發病} - \text{primary}}{\text{易感受接觸者} - \text{primary}}$$

- Attack rate 其實是**比例**，不寫時間區間。Secondary AR 的**分子、分母都扣掉 primary cases**。
- **Food-specific AR** = 吃某食物且生病 ÷ 吃該食物的人；比較**有吃 vs 沒吃**，**差距最大**的才是元兇。

## 發生率（累積發生率、發生密度）
@ch morbidity
@fig slide-person-years
$$\text{累積發生率} = \frac{\text{期間內新個案}}{\text{期初 at risk 人數}}$$

$$\text{發生密度} = \frac{\text{新個案}}{\text{總人時（person-time at risk）}}$$

- 分母要**扣掉已經有病的人**。發生率是**風險**的測量：「聽到罹病風險就想到發生率」。
- 人時：發病、失訪、死於他因之後就**不再累加**；失訪與死於他因**不算事件**。例：5 人追 5 年，第 1、2、4 年各有 1 人發病 → $\dfrac{3}{17}$ **人年**。
- 找新個案要**兩次篩檢**：第一次篩到的是盛行個案。

## 盛行率與 P = I × D
@ch morbidity
@fig slide-inc-prev-example
$$\text{盛行率} = \frac{\text{某時間點的新＋舊個案}}{\text{該時間族群人數}}$$

$$
\frac{P}{1-P} = I \times D
P \approx I \times D \quad (P \le 0.05)
$$

- 盛行率分母**不用人時**；$I$ 和 $D$ 時間單位要一致。
- 計算例（1,000 人，年初已有 3 人病、年內新發 2 人）：**發生率** $\dfrac{2}{997}$；**期盛行率** $\dfrac{5}{1000}$。
- Hitown：$P = 0.1$、$D = 25$ 年 → $I = 4/1000/\text{年}$；Lotown：$P = 0.06$、$D = 3$ 年 → $I = 20/1000/\text{年}$（盛行率低的 Lotown 風險反而高）。
- 糖尿病：低 I、高 P；感冒：高 I、低 P。

## 死亡率、致死率、比例死亡
@ch mortality
@fig rate-denominators
| 指標 | 公式 | 性質 |
|---|---|---|
| **死亡率** | $$\dfrac{\text{一年內死亡數}}{\text{年中人口}}$$ | 率 |
| **致死率 CFR** | $$\dfrac{\text{診斷後一段時間內死亡}}{\text{患該病的人}}$$ | 比例（%） |
| **比例死亡** | $$\dfrac{\text{死於某原因}}{\text{總死亡數}}$$ | 比例（%） |

$$\text{特定死因死亡率} = \text{全死因死亡率} \times \text{比例死亡}$$

- 例：10 萬人中 20 人患 X 病，18 人死 → **死亡率 0.18/1000**、**致死率 90%**。
- $30/1000 \times 10\% = 15/1000 \times 20\% = 3/1000$：比例不同、風險相同。
- 死亡率的分母每個人都要**有機會進入分子**；年齡別、死因別的分子分母用同樣的限制。
- 死亡率可替代發生率：**致死率高＋病程短**（胰臟癌）。

## YPLL 與 DALY
@ch mortality
@fig slide-ypll
$$\text{YPLL} = \sum_{\text{死亡年齡} < 75} (75 - \text{死亡年齡})$$

$$\text{DALY} = \text{YLL} + \text{YLD}$$

- 1 歲死 → 74；50 歲死 → 25。**超過 75 歲的死亡直接刪掉**，不算負數。
- 自殺：死亡率排第 7、**YPLL 排第 4**（年輕人多）；0–19 歲 YPLL 第一是機動車事故。
- YLL = 過早死亡損失的生命年、YLD = 失能生活年；1 DALY = 損失 1 年健康生命。

## 年齡校正：直接法 vs SMR
@ch mortality
@fig age-adjust
@fig slide-smr
$$\text{直接法校正率} = \frac{\sum_i (\text{年齡別率}_i \times \text{標準人口}_i)}{\text{標準人口總數}}$$

$$
\text{SMR} = \frac{\text{觀察死亡數}}{\text{預期死亡數}}
\text{預期死亡數} = \sum_i n_i \times r_i^{\text{標準}}
$$

- **直接法**：有各族群**年齡別死亡率**時用。例：早期 vs 晚期粗率 96 vs 126 → 校正後 **124.3 vs 101.7 /10 萬**（反轉）；墨西哥 vs 美國 → **639 vs 574 /10 萬**。
- $n_i$ = 研究族群各年齡層人數、$r_i^{\text{標準}}$ = 標準族群的年齡別死亡率。
- **SMR（間接法）**：**沒有**年齡別死亡數（職業族群、小族群）時用。例：礦工 $\dfrac{406}{138.8} = 2.92$，**×100 = 292，跟 100 比** → 高於一般族群。謝老師點名 SMR 最容易算錯。

## 預後：五種指標
@ch prognosis
| 指標 | 公式 |
|---|---|
| **CFR** | $$\dfrac{\text{死於該病}}{\text{罹病人數}}$$（短期急性；名為率、實為比例） |
| **五年存活率** | $$\dfrac{\text{5 年後仍存活}}{\text{治療或診斷人數}}$$（有 **lead time bias**） |
| **觀察存活率** | $$\textstyle\prod_k P_k$$（life table、K-M 累乘） |
| **存活中位數** | 存活曲線降到 **50%** 的時間 |
| **相對存活率** | $$\dfrac{\text{觀察存活率}}{\text{預期存活率}}$$（相同條件但沒病者） |

## 生命表與 Kaplan-Meier
@ch prognosis
@fig km-curve
$$
P_k = \frac{\text{第 } k \text{ 年存活}}{\text{第 } k{-}1 \text{ 年存活} - \text{沒追滿第 } k \text{ 年者}}
S_k = P_1 \times P_2 \times \cdots \times P_k
$$

- 例：$P_1 = \dfrac{197}{375} = 0.525$；$P_2 = \dfrac{71}{197 - 43} = 0.461$ → 兩年累積 **0.242**。

有 withdrawal 時：

$$
\text{有效人數} = \text{期初} - \tfrac{1}{2} \times \text{withdrawal}
P_k = 1 - \frac{\text{死亡數}}{\text{有效人數}}
$$

- 例：$1 - \dfrac{83}{175.5} = 0.527$ → 兩年累積 **0.277**、五年 **0.124**。

K-M：每個死亡時間點算一次，再累乘：

$$p = 1 - \frac{\text{死亡數}}{\text{當時仍在追蹤人數}}$$

- 考古例（110、114）：第 1 週 8 人死 1 → **0.875**；第 12 週 $\tfrac{7}{8} \times \tfrac{6}{7} \times \tfrac{5}{6} \times \tfrac{2}{3}$ = **0.417**。
- **有人死亡才算**一次；失訪者如果是因為病情惡化離開 → 存活率被**高估**。

## RCT 結果：efficacy、RR、ARR、NNT
@ch rct
$$
\text{Efficacy} = \frac{R_{\text{placebo}} - R_{\text{treat}}}{R_{\text{placebo}}}
\text{RR} = \frac{R_{\text{treat}}}{R_{\text{placebo}}}
$$

$$
\text{ARR} = \text{CER} - \text{EER}
\text{NNT} = \frac{1}{\text{ARR}}
$$

- Efficacy 例：CFR 新藥 5%、安慰劑 20% → $\dfrac{0.20 - 0.05}{0.20}$ = **0.75**（講義除以新藥組算出 3，以 Gordis 為準）。
- RR 例：第一年存活 55% vs 40% → $\dfrac{0.55}{0.40}$ = **1.375**。
- NNT 例：中風 5% vs 20% → $\dfrac{1}{0.15} \approx$ **6.67**（109）；惡化 60% vs 40% → **NNT = 5**（110、114）。
- RRR 一樣時，罕見事件的 NNT 可能很大：MS 干擾素 50% vs 39% → **NNT ≈ 9**；0.00050% vs 0.00039% → **NNT 909,090**。

## 篩檢效度：2×2 表
@ch screening
@fig two-by-two
| | 有病 | 沒病 |
|---|---|---|
| 篩檢 + | a（TP） | b（FP） |
| 篩檢 − | c（FN） | d（TN） |

**直的看**（分母是真實疾病狀態）：

$$
\text{Se} = \frac{a}{a+c}
\text{Sp} = \frac{d}{b+d}
\%\text{FN} = \frac{c}{a+c} = 1 - \text{Se}
\%\text{FP} = \frac{b}{b+d} = 1 - \text{Sp}
$$

**橫的看**（分母是篩檢結果）：

$$
\text{PPV} = \frac{a}{a+b}
\text{NPV} = \frac{d}{c+d}
$$

- 考試**不給公式**，要自己記。
- 切點**降低** → Se↑、Sp↓、PPV↓（捐血篩 HIV 要高敏感度）；切點**提高** → Sp↑、Se↓。

## 序列 vs 平行篩檢
@ch screening
@fig multi-testing
| | **序列**（兩次都陽性才算陽性） | **平行**（任一陽性就算陽性） |
|---|---|---|
| 淨 Se | $\text{Se}_1 \times \text{Se}_2$ ↓ | $\text{Se}_1 + \text{Se}_2 - \text{Se}_1\text{Se}_2$ ↑ |
| 淨 Sp | $1 - (1-\text{Sp}_1)(1-\text{Sp}_2)$ ↑ | $\text{Sp}_1 \times \text{Sp}_2$ ↓ |

- 序列例：血糖（0.7／0.8）→ OGTT（0.9／0.9）→ **淨 Se 0.63、淨 Sp 0.98**。
- 平行例：A（0.8／0.6）＋ B（0.9／0.9）→ **淨 Se 0.98、淨 Sp 0.54**。
- 序列的淨 Sp↑，所以 PPV↑。

## 預測值與盛行率
@ch screening
@fig ppv-prevalence
$$
\text{PPV} = \frac{\text{Se} \cdot P}{\text{Se} \cdot P + (1 - \text{Sp})(1 - P)}
\text{NPV} = \frac{\text{Sp}\,(1 - P)}{\text{Sp}\,(1 - P) + (1 - \text{Se})\,P}
$$

- $P$ = 盛行率。盛行率 ↑ → **PPV↑、NPV↓**；**Se、Sp 不受盛行率影響**。陳老師說 PPV 只考盛行率的影響。
- Se 0.99、Sp 0.95：盛行率 **1% → PPV 0.17**；**5% → PPV 0.51**。
- Hemoccult Se = Sp = 0.8、盛行率 1%：$\dfrac{0.8 \times 0.01}{0.8 \times 0.01 + 0.2 \times 0.99} \approx$ **3.9%**。
- 疾病少見時，**特異度**對 PPV 的影響最大。

## 信度：一致率與 Kappa
@ch screening
$$
\text{一致率} = \frac{a+d}{N}
\text{Chamberlain 陽性一致率} = \frac{a}{a+b+c}
$$

$$\kappa = \frac{P_o - P_c}{1 - P_c}$$

- $P_o$ 觀察一致率、$P_c$ 機率一致率。例：$\dfrac{0.919 - 0.514}{1 - 0.514}$ = **0.833**。一般一致率會被大量陰性 $d$ 灌水。
- 判讀：0.41–0.60 moderate、0.61–0.80 substantial、≥ 0.81 almost perfect。
- 陳老師說**不考算一致率和 Kappa**，但要知道它們的意義。一致率高但 κ 低 → 盛行率極低、$P_c$ 很高。

## 率 vs 比例速查
@ch morbidity,mortality,prognosis
- 白老師：流病裡稱得上「率」的只有**發生率、死亡率、盛行率**。
- **名為率、實為比例**：**attack rate**、**case-fatality rate**、**比例死亡**。
- 比例不能推論風險：要比風險，請換回**率**（發生率、特定死因死亡率），長期比較還要做**年齡校正**。
