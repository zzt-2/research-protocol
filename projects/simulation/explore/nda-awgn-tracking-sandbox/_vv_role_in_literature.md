# VV 算法在近年光通信载波相位恢复论文中的呈现方式（实证调研）

> 调研日期：2026-07-08
> 目的：确认领域惯例 —— 别人发 NDA-ML / M-APSK CPE / 星地 FSO 载波同步类论文时，VV（Viterbi-Viterbi 1983 升幂 mean-angle）通常扮演什么角色，以便决定"VV 当主 baseline 还是当同档对照一句带过"。
> 结论先行：**领域惯例强烈支持"VV 当同档对照 / 定性引用，而非主 baseline"**（中等偏强证据，N=13 篇精看 + web 补充 1 篇）。VV 作为"主对比对象逐一 SNR 点比"的情况存在，但集中在两类场景：①VV 是被改进对象本身（diff-4th/反馈环类），②VV 与 BPS 级联当"经典粗估计"被 Kalman/MAP 类新方法碾压。**NDA-ML / 升幂同族论文几乎不拿 VV 当 baseline，甚至不提**。

---

## 1. 检索覆盖

### 本地库（`study/research-protocol/papers/`）
- 总 content.md：**356 篇**
- 提到 "viterbi"（任何含义）：**19 篇** → 逐篇过 line context
- 提到 "carrier phase estimat / recover / phase noise compensat"（CPR 主题）：**26 篇**
- 提到 "M-th power / 升幂 / 4th power"：14 篇
- 提到 "NDA-ML / non-data-aided ML"：2 篇
- **精看（读 abstract+VV 上下文+baseline 段落）：13 篇**（19 篇 viterbi 命中去掉 6 篇无关——如纯 Viterbi 译码 / BH 资源调度里的 Viterbi 算法 / 仅参考文献条）

### Web 补充
- WebSearch：4 组查询（single-carrier NDA-ML M-APSK / blind CPE APSK 2024 / VV multi-ring APSK / Du NDA-ML PTL 2025）
- 关键补充命中：**Q. Wang, "Viterbi–Viterbi Carrier Phase Estimation for Multi-Ring M-APSK With Wiener Carrier Phase Noise," 2024**（IEEE 10561477）——这是**唯一**在 2024 仍直接以"改进 VV"为题的论文，对本调研极相关。

### 交叉验证（FR-26）
- ✅ Du et al. 2025 (10.1109/LPT.2024.3523478)：Semantic Scholar API 确认 title/year/venue/authors 与本地一致。
- ✅ 其余本地论文：均以本地 content.md 原文摘录（DOI 可定位），未臆造。
- ⚠️ Wang 2024 (IEEE 10561477)：Semantic Scholar 触发 429 限流，未能二次交叉验证；其标题/作者/IEEE id/描述来自 WebSearch 返回，**功能断言（"改进 VV for multi-ring M-APSK"）已标注为单源、待核**，不影响主结论。

### 筛选口径
- 计入分类的"CPR 论文"必须：①涉及载波相位估计/恢复/相位噪声补偿，且 ②VV（或其等价物 4th-power/升幂）以**算法对象**出现。
- 仅把 VV 当系统组件一笔带过、或只做 FOE（频偏估计）的论文，单列为"仅定性/系统组件"。

---

## 2. 分类统计：VV 的呈现方式

精看 13 篇 CPR 相关论文（去重后口径）+ web 1 篇 = **14 个样本**。分类如下：

| 呈现方式 | 计数 | 代表论文 |
|---|---|---|
| **主对比对象**（放对比表/曲线，逐 SNR 点比） | **4** | ①Hu 2025 Electronics ②oe.553709 (TS-KF) ③sat.1553 ④Wang 2024 (web) |
| **同档对照**（提一句"性能相当/经典方法"，不展开或仅定性比） | **3** | ⑤LCOMM 2026 ⑥osac.438524 ⑦optcom.2024.130981 |
| **仅定性引用**（引为经典 NDA 方法，列在方法清单里，不放数据） | **3** | ⑧10.1007_s11107-024-01019-2 ⑨electronics14020265(intro 表) ⑩mwp2022/photonics1312(OPLL 组件) |
| **完全不提**（CPR 论文但通篇无 VV/升幂） | **4** | ⑪Du 2025 (B11 NDA-ML) ⑫oecc-psc2025 MAP-256QAM ⑬jphot.2025.3534258 ⑭ACCESS.2025.3535789 |

### 主对比对象（4 篇）—— 都有"VV 被碾压或被改进"的共性

**① Hu et al., "A Noise-Tolerant Carrier Phase Recovery Method for Inter-Satellite Coherent Optical Communications," *Electronics* 14(2):265, 2025. DOI 10.3390/electronics14020265**
- VV 在此以 **"Diff-4th methods"**（差分级联四次方）之名出现，是**唯一主 baseline**，做 LRMSE 与 BER 逐 SNR 点对比 + 复杂度表。
- 呈现方式：把 VV 当"传统方法"全面碾压——"BER of the proposed method can be decreased to 6.7×10⁻³ at SNR 4.5 dB, in contrast to a BER of 0.25 for the traditional method"，资源消耗降 64%。
- 关键点：**作者改了 VV 的名字**（叫 Diff-4th），且 VV 是其方法的"被改进对象"（反馈环+前馈），不是平等同档对照。

**② "Robust two-stage Kalman filter scheme ... LEO-LEO laser inter-satellite links," *Opt. Express* (oe.553709), 2024.**
- 主 baseline = **"VV-BPS"级联算法**（VV 做粗、BPS 做精），与提出 TS-KF 做 BER 逐 OSNR/多普勒点对比（Fig.6）+ 复杂度/收敛（Fig.7）。
- 呈现：VV-BPS 在大多普勒下"fails to demodulate"，TS-KF 碾压。
- 关键点：VV 在这里是**与 BPS 绑定的经典粗估计**，被当作"传统级联方案"整体对比，而非单独 VV。

**③ "Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links," *Int. J. Satell. Commun. Netw.* 43(3), 2025. DOI 10.1002/sat.1553**
- 综述/分析文，VV 与 pilot-based、differential 三类做 **SNR penalty 逐场景对比**（Fig.9，4 个场景）。
- 呈现：客观——"nondifferential Viterbi–Viterbi algorithm outperforms the others as long as ΔwTs<3×10⁻⁵"，但 cycle-slip 风险大；pilot 在 fade 场景反超 VV 约 1 dB。
- 关键点：这是少数**公平地把 VV 当对等方法比**的，但它是 review，不是提出新方法的论文。

**④ Q. Wang, "Viterbi–Viterbi Carrier Phase Estimation for Multi-Ring M-APSK With Wiener Carrier Phase Noise," 2024 (IEEE 10561477).** ⚠️单源待核
- 唯一直接以"改进 VV"为题的近期论文；VV 既是主对比也是被改进对象（针对 multi-ring M-APSK refine VV 的线宽容限）。

### 同档对照（3 篇）—— 提一句，不展开

**⑤ Tang et al., "Polarization-fading-free CPE ... (LPT scheme)," *IEEE Commun. Lett.* 30, 2026. DOI 10.1109/LCOMM.2026.3651445**
- VV 仅在 intro 列为典型 CPE 之一："CPE algorithms based on blind phase search (BPS) [11] or Viterbi-Viterbi phase estimation [12]"。**全文不与 VV 比**，主 baseline 是自家上一代 PTJ 方案。
- 原句（DOI 10.1109/LCOMM.2026.3651445, intro 段）：> "carrier phase estimation (CPE) algorithms based on blind phase search (BPS) [11] or Viterbi-Viterbi phase estimation [12]."

**⑥ Martins et al., "Hardware optimization of dual-stage carrier-phase recovery," *OSA Continuum* 4(12), 2021. DOI 10.1364/OSAC.438524**
- VV 在 intro 作经典方法介绍 + 列出 BPS+VV 等组合，但**本文主 baseline 是 standalone BPS / pilot+BPS**，不单比 VV。
- 原句（DOI 10.1364/OSAC.438524, §1）：> "Carrier phase recovery (CPR) based on the Viterbi-Viterbi (VV) method is widely employed for M-PSK ... However, for high-order M-QAM signals, the VV algorithm becomes sub-optimal."

**⑦ "Coarse frequency offset estimation ... satellite-to-ground," *Opt. Commun.* 572:130981, 2024. DOI 10.1016/j.optcom.2024.130981**
- 这篇主菜是 FOE，VV 只作为**接收机系统组件**一句话："The system uses a V–V-based feedback phase recovery algorithm to compensate for residual phase noise [28]"。不参与对比。

### 仅定性引用（3 篇）

**⑧ Deka et al., "Low-complexity high linewidth-tolerant carrier synchronization for 16QAM using pilot-assisted RLS," *Photonic Netw. Commun.* 47:164, 2024. DOI 10.1007/s11107-024-01019-2**
- VV 列在 NDA 相位估计方法清单首位，纯定性，无数据。
- 原句（DOI 10.1007/s11107-024-01019-2, §I）：> "The most widely used techniques for NDA phase estimation include the Viterbi-Viterbi, barycenter algorithm, QPSK partitioning, and blind phase search (BPS)."

**⑨ Hu 2025 Electronics**（同①，但此处指其 intro 的 Table 1 方法对照）—— 把 VV-PE 与 BPS 并列为"blind estimation"两类，定性优劣，**正文才转为主对比**。

**⑩ "OPLL / DSP hybrid"类（mwp2022 9997784、photonics 10:1312）**：VV 作为"DSP 里常用相位估计"被引用，用于引出作者自己的 OPLL 改造，**不与 VV 比性能**。

### 完全不提（4 篇）—— 最关键的一类

**⑪ Du, Yu, Wang, Kam, "Non-Data-Aided ML Estimation of Timing Offset and Carrier Phase for M-APSK Modulated FSO Systems," *IEEE Photon. Technol. Lett.* 37(10), 2025. DOI 10.1109/LPT.2024.3523478（= 本地 B11）**
- 这是**与用户论文数学同族**（升幂 M₀-th power + ML）的最相关论文。**通篇不出现 "Viterbi"**。
- 用 M₀-th power 消调制相位（line 75: "raising R(k) to the M₀-th power"），与 VV 数学同族，但 baseline 选的是 **pilot-aided (PA) 与 DA-ML**。
- 主对比对象：DA ML 方法（"DA ML method exhibits a 2 dB SNR drop compared to our approach"）+ PA。VV 被沉默。
- ✅ Semantic Scholar 已交叉验证（title/year/venue/authors 一致）。

**⑫ Ma, Liu, Du, Wang, Kam, "Maximum A Posteriori Probability Phase Recovery for 256-QAM," OECC/PSC 2025, WP-B-26. DOI 10.23919/OECC-PSC62146.2025.11109607**
- 同一作者谱系（Du/Wang/Kam）。**通篇不提 VV**，引的是自家前作 ML/MAP [5]（Wang 的 joint ML+MAP），baseline 是 pilot-aided。

**⑬ "Performance of Coherent Optical MPSK in Underwater Turbulent Channels With Phase Errors," *J. Photon.* 2025. DOI 10.1109/JPHOT.2025.3534258**
- 理论 BER 分析（MPSK + 相位误差模型），无算法对比，自然不提 VV。

**⑭ Nasr et al., "Dual-Polarization Self-Coherent Transceivers for FSO ... Atmospheric Turbulence," *IEEE Access* 2025. DOI 10.1109/ACCESS.2025.3535789**
- 自相干 vs 相干方案对比，CPR 不是焦点，不提 VV。

---

## 3. 主 baseline 分布（别人主比什么）

按 14 篇统计主对比对象（含"不比"）：

| 主 baseline 类型 | 篇数 | 备注 |
|---|---|---|
| **DA-ML / pilot-aided (PA) / DA 方法** | 3 | Du 2025、oecc-psc2025、(Deka pilot-RLS 以 pilot 为主) |
| **BPS（blind phase search）及其低复杂度变种** | 3 | osac.438524、LCOMM2026(intro)、electronics(intro) |
| **VV-BPS 级联 / Diff-4th（含 VV）** | 3 | oe.553709(TS-KF)、Hu2025、sat.1553 |
| **自家上一代方法（PTJ/前作 MAP/ML）** | 2 | LCOMM2026(PTJ)、oecc-psc2025 |
| **理论界（CRLB/MCRLB）** | 1 | Hu2025（与 Diff-4th 并列） |
| **Kalman filter 类** | 1 | （oe.553709 本身即 KF 派，被别人引为 baseline） |
| **不设算法 baseline（理论分析/系统方案）** | 2 | jphot.2025.3534258、ACCESS.2025.3535789 |

**观察**：
- 在 **NDA-ML / 升幂同族**论文里，主 baseline 是 **DA-ML / pilot-aided**（Du 2025、oecc-psc2025），**不是 VV**。
- 在 **光纤 / 短距 QAM CPE** 论文里，主 baseline 是 **BPS 及其低复杂度变种**（osac.438524 系列），VV 只在 intro 作"PSK 经典、QAM 次优"的定性铺垫。
- 把 **VV 单独当主 baseline** 的，几乎都是"VV 是被改进对象"或"VV-BPS 当经典级联被新方法碾压"——即 VV 充当**靶子/下界**，而非平等同档对照。

---

## 4. 同族处理惯例（方法跟 VV 数学同族时怎么写）

当论文方法本身是升幂/M-th-power 类（与 VV 同族）时，**3 个直接同族样本（Du 2025、oecc-psc2025、Wang 2024）的处理高度一致：不正面写"与 VV 持平"，而是绕开 VV，改比 DA-ML/PA，或把 VV 仅当定性经典引用。**

### 典型措辞（原句摘录）

1. **Du 2025（升幂+ML，与用户最像）—— 完全沉默 VV，改比 DA-ML：**
   > "Simulation results verify the superior estimation accuracy and tolerance to laser linewidths of the proposed ML approach, compared to the pilot-aided (PA) method in [8] and DA ML method in [10]."
   （DOI 10.1109/LPT.2024.3523478, §I, line 29）—— 注意：方法用 M₀-th power（line 75），与 VV 同族，但 baseline 只字不提 VV。

2. **osac.438524 —— 把 VV 定性框定为"PSK 最优、QAM 次优"，为自己的 BPS 路线让路：**
   > "Carrier phase recovery (CPR) based on the Viterbi-Viterbi (VV) method is widely employed for M-phase-shift keying (PSK) modulation formats, since it provides an optimum solution for blind phase estimation of optical signals with constant amplitude [2]. However, for high-order M-quadrature amplitude modulation (QAM) signals, the VV algorithm becomes sub-optimal [2]."
   （DOI 10.1364/OSAC.438524, §1, line 21）—— 经典"先肯定 VV 在 PSK 的地位，再指出其在高阶 QAM 的不足"过渡句。

3. **electronics14020265（Hu 2025）—— 把 VV 重命名为"Diff-4th 传统方法"再碾压：**
   > "Compared to the traditional differential cascaded fourth-power (Diff-4th) methods [13–15], the proposed approach achieves improved noise [tolerance]... the LRMSE of the proposed method approaches the modified Cramér–Rao lower bound (MCRLB)."
   （DOI 10.3390/electronics14020265, §1 line 41 / 贡献点 line 51）—— 不说"持平 VV"，而是把 VV 等价物框成"差、被超越的传统方法"。

4. **LCOMM 2026 —— VV 与 BPS 并列作"CPE 常见法"一句带过，主比自家前作：**
   > "carrier phase estimation (CPE) algorithms based on blind phase search (BPS) [11] or Viterbi-Viterbi phase estimation [12]."
   （DOI 10.1109/LCOMM.2026.3651445, intro）

5. **Deka 2024 —— 把 VV 列为"NDA 经典方法清单"第一条，不展开：**
   > "The most widely used techniques for NDA phase estimation include the Viterbi-Viterbi, barycenter algorithm, QPSK partitioning, and blind phase search (BPS)."
   （DOI 10.1007/s11107-024-01019-2, §I）

**惯例小结**：领域里几乎没有"如实写与 VV 全场景持平"的范式。同族作者要么**沉默绕过 VV**（Du/Ma-Kam 系），要么把 VV **降格为"PSK 经典 / QAM 次优 / 传统方法"的定性铺垫**（osac/Hu），要么把它**与 BPS 绑定成级联靶子**（oe.553709）。直接宣称"我方与 VV 持平"是**反惯例**的写法。

---

## 5. 结论

**判断：领域惯例支持"VV 当同档对照 / 定性引用，不主比"。✅**

- **证据强度：中等偏强**（精看 N=13 本地 + web 1 篇 = 14 样本；其中与用户最同族的 3 篇升幂/ML 论文 100% 不把 VV 当主 baseline，2/3 直接不提 VV）。
- **适用条件**：当论文方法与 VV 数学同族（升幂类 NDA）时，惯例是**绕过 VV**——要么不提，要么仅在 intro 作"经典 NDA 法 / PSK 最优"的定性引用；主 baseline 应选 **DA-ML / pilot-aided**（同族论文的实际做法）或 **BPS / 复杂度维度**。
- **何时才把 VV 当主 baseline**：仅当 (a) VV 是被改进对象本身（反馈环/diff-4th 改造），或 (b) 用 VV-BPS 级联当"经典粗估计"被 Kalman/MAP 碾压时。这两种都要求**作者方法确实显著优于 VV**，与用户"全场景持平"的情况不符。
- **对用户论文的具体建议**：
  - 不要把"与 VV 全场景 BER 持平"当卖点（反惯例，且持平无卖点）。
  - 推荐 VV 当**同档对照一句带过**（仿 Du 2025 / LCOMM 2026 措辞：intro 列 VV 为经典 NDA/PSK 法，正文不展开逐点比），把对比资源投到 **DA-ML / pilot-aided**（你方法的真正差异点）或 **复杂度 / 免导频 / 能效 / 湍景鲁棒性** 等其他维度。
  - 若审稿人坚持要 VV 曲线，可放，但定位为"对等调参下与经典升幂 mean-angle 持平"的同档参照，而非主 baseline。

### 证据强度与局限
- **强项**：本地样本覆盖了与用户最同族的 Du 2025（升幂+ML+M-APSK+FSO，几乎同题）及其姊妹篇 oecc-psc2025，结论可直接类比。
- **弱项**：①Semantic Scholar 对 Wang 2024 (IEEE 10561477) 触发限流未二次核验（单源 WebSearch，已标注）；②2022-2026 单年 JLT/JPhoton 的 NDA-ML M-APSK 论文本就稀疏（WebSearch 也只返回 Du 一篇 + Wang 一篇），样本基数偏小，"完全不提 VV"类的 4 篇里有 2 篇（jphot UWOC、ACCESS 自相干）并非严格同子方向。建议若要更强证据，补查 Kam/Wang 课题组 2022-2024 的 JLT/JPhoton 旧作（它们是升幂+ML 同族的主力产出）。
