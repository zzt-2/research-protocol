# 对比参考文献清单(发老师)

> 学生:张哲铜 | 日期:2026-07-07
> 老师 2026-07-07 反馈:"对比参考文献请单独发给我。要求:近年、transactions 水平(我担心达不到?)"
> 本清单诚实标注每篇的**年份 + 期刊/会议档级**,供老师判断对比对象够不够格。

---

## 一、当前论文用到的对比/来源文献(按角色)

### A. 当前方法的思想来源(1 篇)

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 评价 |
|---|---|---|---|---|---|
| 1 | 方法思想来源(NDA-ML 升幂 + ML 闭式) | Xinwei Du, Keying Yu, Qian Wang, Pooi-Yuen Kam. "Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems." **IEEE Photonics Technology Letters (PTL)**, vol. 37, no. 10, pp. 559–562, May 2025. DOI: 10.1109/LPT.2024.3523478 | **Letters(非 Transactions)** | **2025(近年)** | 思想源头,但是 OFDM 频域 + Letters 级,不是 Transactions |

### B. 主 baseline(直接对照,1 篇)

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 评价 |
|---|---|---|---|---|---|
| 2 | DA-ML baseline(贡献声称要超越的对手) | 同 #1(Du et al., PTL 2025)—— 该论文自选 DA-ML 作对照,我们沿用 | Letters | 2025 | 单篇自选对照,非领域共识级 |

### C. 经典盲估计 baseline(补的对比,2 篇)

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 评价 |
|---|---|---|---|---|---|
| 3 | BPS(光纤 CPR 事实标准) | T. Pfau, S. Hoffmann, R. Peveling, et al. "Optimized Blind Phase Search Algorithm for Phase Recovery in Coherent Optical Communication Systems."(题目/卷期以原文为准,这篇我们没下载全文,需要时补全) | **IEEE J. Lightwave Technol.(JLT,Transactions 级)** | **2009(经典,非近年)** | 档级够,但年份老 |
| 4 | VV(NDA 载波同步祖师爷) | A. J. Viterbi, A. M. Viterbi. "Nonlinear Estimation of PSK-Modulated Carrier Phase with Application to Coded Digital Communications." **IEEE Trans. Inf. Theory (TIT)**, vol. 29, no. 4, pp. 543–551, July 1983. | **IEEE TIT(Transactions 级)** | **1983(经典,非近年)** | 档级够,但年份很老 |

### D. 场景/信道模型依据(1 篇)

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 评价 |
|---|---|---|---|---|---|
| 5 | OSL DSP 算法地图综述(4 场景信道模型 ISL/下行/上行弱湍/上行强湍) | Carl Valjus, Raphael Wolf, Juraj Poliak. "Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links." **International Journal of Satellite Communications and Networking (Wiley)**, vol. 43, no. 3, pp. 229–250, 2025. DOI: 10.1002/sat.1553 | **Wiley 期刊(Transactions 级,非 IEEE)** | **2025(近年)** | 够格,场景模型依据 |

---

## 二、后续候选方向的来源文献(§七 候选,8 篇)

如果后续往这些方向扩,这些是要对比/参考的论文:

| # | 候选方向 | 完整引用 | 期刊档级 | 年份 |
|---|---|---|---|---|
| 6 | 跨子系统协同联合估计(§七 第二梯队) | "Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication." **IEEE J. Photonics (JPHOT)**, 2023. DOI: 10.1109/JPHOT.2023.3265847 + Optics Express(oe.520452,FSO 分集,标题待补全——原文 Optica 登录墙未拿到) | **IEEE JPHOT(Transactions 级)+ Optics Express(Optica 期刊)** | **2023(近年)** |
| 7 | TX 侧量化噪声整形 DRE(§七 第二梯队) | Patel et al. "Simplified Self-Coherent FSO Transmission Boosted by Digital Resolution Enhancer." **IEEE J. Lightwave Technol. (JLT)**, 2023. DOI: 10.1109/JLT.2023.3270673 | **JLT(Transactions 级)** | **2023(近年)** |
| 8 | Gardner TED 复用做 Doppler 频偏估计(§七 第三梯队) | Yan Ma, Zhenming Yu, Yongli Zhao, et al. "Doppler Estimation Reusing Gardner TED"(题目以原文为准). **OFC 2026**(Conference,W2A.62). DOI: 10.1364/OFC.2026.W2A.62 | **会议(非 Transactions)** | **2026(近年)** |
| 9 | 自适应相位估计窗口(§七 第三梯队) | 同 #5(Valjus sat.1553)+ Leven et al. "Mth-power phase estimator"(PTL 2007,DOI: 10.1109/LPT.2007.891893,理论锚) | PTL(经典) | 2007 |
| 10 | deep fade 冻结 + pilot 双模(§七 第三梯队) | Matsuda et al. SPIE 2020. DOI: 10.1117/12.2544050 | **SPIE 会议** | 2020 |
| 11 | atan2 鉴相器解耦(§七 第三梯队) | "Z-ODPLL…"(题目待补全). **Photonics (MDPI)**, vol. 10, no. 4, 2023. DOI: 10.3390/photonics10040389 | **MDPI 期刊(非 IEEE)** | **2023** |
| 12 | 短时谱粗频偏估计(§七 第三梯队) | **Optics Communications**, vol. 572, 130981, 2024. DOI: 10.1016/j.optcom.2024.130981 | **Elsevier 期刊** | **2024(近年)** |
| 13 | Pilot-RLS 联合频偏+相位(§七 第三梯队) | **Wireless Personal Communications (Springer)**, 2024. DOI: 10.1007/s11107-024-01019-2 | **Springer 期刊** | **2024(近年)** |
| 14 | MAP 联合相位估计(§七 第三梯队) | Kam et al. OECC/PSC 2025. DOI: 10.23919/OECC/PSC62146.2025.11109607 | **会议** | **2025** |

---

## 三、对老师"近年 + transactions 水平"担心的诚实回答

**老师担心的核心**:对比参考文献够不够"近年(2020+)+ IEEE Transactions 级"。

### 现状盘点(诚实)

| 维度 | 数量 | 占比 | 说明 |
|---|---|---|---|
| **近年(2020+)** | 9/14 | 64% | #1/#2/#5/#6/#7/#8/#11/#12/#13/#14 都是 2020+,够近年 |
| **IEEE Transactions 级** | 5/14 | 36% | #3(JLT)/#4(TIT)/#5(Wiley Trans 级)/#6(JPHOT)/#7(JLT) |
| **近年 + Transactions 级** | **3/14** | **21%** | #5(sat.1553,2025 Wiley)/#6(JPHOT 2023)/#7(JLT 2023) |

**核心差距**:
1. **当前方法来源(#1 Du PTL 2025)是 Letters 不是 Transactions**——这是老师"达不到?"担心的主因。如果要把方法本身提到 Transactions 级,需要更扎实的理论 + 实验工作(CRLB 紧致性证明、多场景验证、SD-FEC 阈值等)
2. **经典 baseline(BPS 2009 / VV 1983)够格但年份老**——这是领域事实(BPS 和 VV 就是这个领域最经典的两个,所有论文都引),但确实不是"近年"。**通常补 1-2 篇近年 NDA-ML/盲估计论文作并列对照更稳**
3. **近年 + Transactions 的只有 3 篇**——偏少

### 我的判断(待老师确认)

**要达到"近年 + Transactions 级"对照,需要补 2-3 篇近年(2022+)IEEE Transactions 的载波同步/盲估计论文作并列 baseline**。这部分**我现在还没做**——需要重新检索 IEEE Trans. Commun. / JLT / TCOM 近 2-3 年的 M-APSK 或卫星光通信载波同步论文。

具体待办:
- 检索 IEEE JLT / TCOM / Optics Express 2023-2026 的 (8,8)-16APSK 或卫星 FSO 载波相位估计论文,补 2-3 篇近年 Transactions 级并列 baseline
- 这关系到投稿期刊层级定位——如果目标 IEEE Transactions,当前对照不够;如果目标 PTL/Letters 级或国内会议,当前对照够

**请老师定**:目标投稿期刊层级是 IEEE Transactions 级,还是 PTL/Letters 级,还是国内会议就行?这决定要不要补近年 Transactions 对照。

---

## 四、需老师指示

1. **目标期刊层级**:投 IEEE Transactions(需要补近年 Trans 级对照),还是 PTL/Letters 级(当前对照够),还是国内会议(CCISP/ICECAI 级,当前对照绰绰有余)?

2. **如果补近年 Transactions 对照**:有没有老师推荐的近年(2022+)载波同步/盲估计论文?(我们自己也会检索,但老师有推荐更准)

3. **BPS/VV 经典老论文是否还要保留作对照**:我觉得必须保留(领域共识),但近年 Trans 论文要不要并列?老师意见?
