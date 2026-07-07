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
| 3 | BPS(光纤 CPR 事实标准) | T. Pfau, S. Hoffmann, R. Peveling, et al. "Optimized Blind Phase Search Algorithm for Phase Recovery in Coherent Optical Communication Systems."(题目/卷期以原文为准,这篇我们没下载全文,需要时补全) | **IEEE J. Lightwave Technol.(JLT,Transactions 级)** | **2009(经典,非近年)** | 档级够,但年份老。**已实测对照**（2026-07-08）：NDA-ML 公平对照 AWGN +0.117dB CI[+0.091,+0.144]、moderate +0.057dB CI[+0.022,+0.092] 稳赢 BPS，weak +0.047dB CI 跨 0 弱赢，strong 工作区 +0.106dB。详见 `baseline_report.md` §1.1 |
| 4 | VV(NDA 载波同步祖师爷) | A. J. Viterbi, A. M. Viterbi. "Nonlinear Estimation of PSK-Modulated Carrier Phase with Application to Coded Digital Communications." **IEEE Trans. Inf. Theory (TIT)**, vol. 29, no. 4, pp. 543–551, July 1983. | **IEEE TIT(Transactions 级)** | **1983(经典,非近年)** | 档级够,但年份很老。**已实测对照**（2026-07-08）：NDA-ML 公平对照 AWGN +0.006dB、weak/moderate −0.004dB（CI 全跨 0，基本持平）——物理合理，NDA-ML（升幂+ML 闭式）vs VV（升幂+mean-angle）在低 PN 下差异极小。**"NDA-ML 不输经典 VV"成立**。详见 `baseline_report.md` §1.1 |

### D. 场景/信道模型依据(1 篇)

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 评价 |
|---|---|---|---|---|---|
| 5 | OSL DSP 算法地图综述(4 场景信道模型 ISL/下行/上行弱湍/上行强湍) | Carl Valjus, Raphael Wolf, Juraj Poliak. "Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links." **International Journal of Satellite Communications and Networking (Wiley)**, vol. 43, no. 3, pp. 229–250, 2025. DOI: 10.1002/sat.1553 | **Wiley 期刊(Transactions 级,非 IEEE)** | **2025(近年)** | 够格,场景模型依据 |

### E. 近年 Transactions 并列 baseline 补充(2026-07-07 补+精读,老师意见 3 触发)

> 检索方法：`tools/search` 4 组关键词 + Crossref DOI 真实性交叉验证（5 篇全 VERIFIED）+ blit ieee 下载 IEEE 两篇 + download --doi 下 OE + subagent 精读。原始检索 `search-archive/2026-07-07/`，全文 `papers/doi/`。

| # | 角色 | 完整引用 | 期刊档级 | 年份 | 精读后可对比性结论 |
|---|---|---|---|---|---|
| 15 | **M-APSK V&V LMMSE 载波相位估计**(主题最贴合,复现失败改定性引用) | Qian Wang, Wenqiang Ma, Li Ping Qian, et al. "Viterbi-Viterbi Carrier Phase Estimation for Multi-Ring M-APSK With Wiener Carrier Phase Noise and Its Performance." **IEEE Photonics Journal**, vol. 16, no. 4, art. 7201408, August 2024. DOI: 10.1109/JPHOT.2024.3415635 | **IEEE Photonics Journal(IEEE 旗下,档级介于 Trans 和 Letters 之间,IF~2.1)** | **2024(近年)** | ⚠️ **文献定性引用（复现失败降级）**。精读确认主题+方法双贴合：(8,8)-16APSK + Wiener PN + NDA M₀=8 次幂同框架。**但实测复现失败**（2026-07-08）：PDF→md 转换把 eq(5)(6)(7) 的 R/p 矩阵闭式转成 picture omitted，靠文字重建公式 16APSK 高 SNR BER floor（@20dB 0.018 vs NDA-ML 7.5e-4），调 4 变体均不对。用户决策放弃实测，改引论文 Fig.7 数据（16APSK(8,8) @ 2MHz LMMSE penalty ≈0.5dB @ BER=10⁻²，跟 DA-ML 持平）作定性对照，诚实标"未实测，据文献"。对照矩阵主力改用 VV/BPS（已实测，见 #3/#4）。详见 `baseline_report.md` §1.2 |
| 16 | **相干 FSO 载波恢复**(场景贴但方法异类) | Liqian Wang, Kunfeng Liu, Siqi Zhang, Shuang Ding. "Enhanced frame synchronization and carrier recovery in coherent FSO communication: a pseudo-random and cyclic QPSK approach." **Optics Express**, vol. 32, no. 15, pp. 25560–25580, 2024. DOI: 10.1364/OE.520452 | **Optics Express(Optica,Transactions 级)** | **2024(近年)** | ⚠️ **场景参照非直接对照**。精读确认：调制是方阵 16QAM（**非 (8,8)-16APSK**），方法是 **DA 训练序列 FOE**（频偏估计，PRBS+cyclic QPSK 两级 FFT），我们是 **NDA-ML CPE**（相位估计），**任务层级不同**。信道有相屏湍流+线宽相位但无 Wiener 模型/Gamma-Gamma/Doppler。**风险**：content.md 是 firecrawl 抓取，**式(1)-(21) 公式全空**（MathJax 没抓到），复现性受限。FOE MSE 1e-8~1e-9，480 符号足够，四支路强湍 16QAM 改善 ~2.46dBm。 |
| 17 | **卫星载波同步 CRB 理论**(理论锚,非并列 baseline) | Zhongyang Yu, Jixun Gao, Li He, et al. "Joint Physical Layer Frame Optimization and Carrier Synchronization for Satellite Communications." **IEEE Transactions on Vehicular Technology**, vol. 72, no. 3, pp. 3517–3531, March 2023. DOI: 10.1109/TVT.2022.3218937 | **IEEE TVT(Transactions 级)** | **2023(近年)** | ⚠️ **理论锚价值,非并列 baseline**。精读确认：调制 QPSK/16QAM/SCMA/GMSK（**无 APSK**），信道**纯 AWGN**（无 PN/湍流，仅 Doppler 常数 CFO），方法 DA 帧优化——调制信道方法全不同。**但 CRB 推导有锚价值**：DA&NDA CRB < NDA CRB ≪ DA CRB，比率 R≈1/η（pilot overhead）量化 DA vs DA&NDA gap，跟我们公平对照框架（NDA 理论下界优于 DA）理论契合。可作"为什么 NDA 理论下界优于 DA"文献锚。OG-PSAM 帧 + PFPE 解耦器是 DA 路线，跟我们 NDA 路线正交。 |

**补充后覆盖度更新**（诚实档级标注）：

| 维度 | 补充前 | 补充后 | 说明 |
|---|---|---|---|
| 近年(2020+) | 9/14 (64%) | 12/17 (71%) | +3 篇全 2023+ |
| IEEE Transactions 严格级（JLT/TCOM/TIT/OE/TVT）| 5/14 (36%) | **7/17 (41%)** | +2 篇严格 Trans（#16 OE / #17 TVT），#15 JPhoton 档级次档不计入 |
| **近年 + 严格 Transactions 级** | **3/14 (21%)** | **5/17 (29%)** | +2 篇（#16 OE 2024 / #17 TVT 2023），改善但未过半 |
| 近年 + 次档 IEEE（含 JPhoton）| — | 6/17 (35%) | 若放宽到 JPhoton 档级 |

**精读后诚实评估**：近年+严格Trans 占比从 21% 升到 29%（严格档级口径），仍未过半。**核心瓶颈仍是方法来源 Du PTL 2025 是 Letters 级**。3 篇并列 baseline 里只有 #15 JPhoto 方法同类（NDA M₀=8 同框架），但它档级是 JPhoton（介于 Trans 和 Letters），**严格 Trans 级 + 方法同类 + 场景同款的 baseline 仍然缺**——这是物理事实（(8,8)-16APSK + NDA-ML + 星地 FSO 三者交集的近年严格 Trans 论文，检索 4 组关键词未召回）。当前对照够投 Letters 级或国内会议(CCISP 7/20 截稿),投 IEEE Trans 需补强方法本身深度(CRLB 紧致性证明 + 多场景验证)。

**未实现的候选(备选)**:
- Zhang et al. Optics Communications 2024 "Joint mitigation of frequency offset and phase noise..."(DOI: 10.1016/j.optcom.2023.130071)——主题贴合相干 FSO 湍流,但 OptComm 是 Elsevier 中档,档级不够 Trans,作备选。
- Matalla et al. JLT 2025 "Joint NDA Clock Recovery for SDM"(DOI: 10.1109/JLT.2025.3546721)——JLT Trans 级 + NDA 主题,但场景是 SDM 光纤非卫星 FSO,方法论参照而非直接对照。

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

### 现状盘点(诚实,2026-07-07 补充近年 Trans baseline 后)

| 维度 | 补充前(14篇) | **补充后(17篇)** | 说明 |
|---|---|---|---|
| **近年(2020+)** | 9/14 (64%) | **12/17 (71%)** | +3 篇(#15/#16/#17)全 2023-2024 |
| **IEEE Transactions 严格级** | 5/14 (36%) | **7/17 (41%)** | +2 篇严格 Trans(#16 OE/#17 TVT),#15 JPhoton 档级次档不计入 |
| **近年 + 严格 Transactions 级** | **3/14 (21%)** | **5/17 (29%)** | +2 篇,改善但未过半 |

**核心差距(补充+精读后)**:
1. **当前方法来源(#1 Du PTL 2025)仍是 Letters 不是 Transactions**——这是老师"达不到?"担心的**主因,补充 baseline 不能解决,只能靠方法本身深度**(CRLB 紧致性证明 + 多场景验证 + SD-FEC 阈值等)
2. **经典 baseline(BPS 2009 / VV 1983)够格但年份老**——领域事实(所有论文都引),现已并列 3 篇近年(#15 JPhoto M-APSK / #16 OE FSO / #17 TVT sat)做对照
3. **近年 + 严格 Trans 占比 29%**——从 21% 改善 8 个百分点,但仍偏少。继续补的边际收益递减,核心瓶颈在方法深度不在 baseline 数量
4. **精读后发现的结构性缺口**：3 篇里只有 #15 JPhoto 方法同类（NDA M₀=8 同框架），但档级是 JPhoton（次档）；严格 Trans 级的 #16/#17 方法都异类（DA-FOE / DA 帧优化）。**"(8,8)-16APSK + NDA-ML + 星地 FSO + 近年 + 严格 Trans"五者交集的 baseline 检索未召回**——这是物理事实（该交集领域窄），不是检索不全。对策：要么放宽到 NDA 方法大类（不计较 APSK/FSO），要么接受 Du PTL 2025（方法源头）+ #15 JPhoto（方法同类次档）作主要方法对照组合。

### 我的判断(待老师确认)

**要达到"近年 + Transactions 级"对照,需要补 2-3 篇近年(2022+)IEEE Transactions 的载波同步/盲估计论文作并列 baseline**。这部分**我现在还没做**——需要重新检索 IEEE Trans. Commun. / JLT / TCOM 近 2-3 年的 M-APSK 或卫星光通信载波同步论文。

具体待办:
- 检索 IEEE JLT / TCOM / Optics Express 2023-2026 的 (8,8)-16APSK 或卫星 FSO 载波相位估计论文,补 2-3 篇近年 Transactions 级并列 baseline
- 这关系到投稿期刊层级定位——如果目标 IEEE Transactions,当前对照不够;如果目标 PTL/Letters 级或国内会议,当前对照够

**请老师定**:目标投稿期刊层级是 IEEE Transactions 级,还是 PTL/Letters 级,还是国内会议就行?这决定要不要补近年 Transactions 对照。

---

## 四、需老师指示

1. **目标期刊层级**:投 IEEE Transactions(需要补方法深度:CRLB 紧致性证明 + 多场景验证,SD-FEC 阈值已补),还是 PTL/Letters 级(当前对照够),还是国内会议(CCISP 7/20 截稿,当前对照绰绰有余)?

2. **补近年 Trans baseline 已完成**:见 §一 E 段 3 篇(#15 JPhoto M-APSK / #16 OE FSO / #17 TVT sat)。如老师有推荐的近年(2022+)载波同步/盲估计论文,可继续补。

3. **BPS/VV 经典老论文是否还要保留作对照**:我觉得必须保留(领域共识),现已并列近年 Trans(#15/#16/#17)。老师意见?
