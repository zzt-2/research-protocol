# [R004] 强湍流 FSO 的 BER 处理领域调研

> 2026-07-10 | 关联：专题 slug 2026-07-09-thesis-writing / D003（10⁻⁵ 矛盾待问导师）/ H002（BER 补点实测 strong/uplink 到不了 1e-5）/ S003（导师"10⁻⁵ 是底线"原话）
> 证据基线：本地论文精读（sat.1553 / Paillier JLT 2020 / Shoji JLT 2012 / Paillier ICSOS 2019 / Fan OptComm 2024）+ COMPARISON_REFS.md 17 篇档级标注 + Semantic Scholar API 4 查询 41 篇去重

## 调研问题

D003 待问导师的生死问题里，主线判断倾向解读 B（导师要"曲线画到 1e-5 量级 / 展示低 BER 区"，非"增益在 1e-5 为正"）。本调研为这个判断补领域证据，回答三个子问题：

1. 强湍流下 BER 降不到 1e-5（衰减率变缓），是 FSO 领域已知现象吗？别人强湍流 BER 能到多低？
2. 强湍流场景别人论文里怎么呈现性能（BER 瀑布 / outage / post-FEC / 别的）？
3. "10⁻⁵ 是底线"在 FSO 领域是 pre-FEC 还是 post-FEC？通行量化基准是多少？

## 发现

### A. 强湍流 BER 降不到 1e-5 是已知现象——但本地对照论文的"强湍流"强度普遍比我们低

**本地精读 5 篇无一在 σ²_R>1 区间给 BER 瀑布**，且它们自己的 BER 都没画到 1e-5：

| 论文 | 湍流强度（最强档） | BER 画到多低 | 到得了 1e-5？ | 备注 |
|------|------------------|------------|-------------|------|
| **Paillier JLT 2020**（本批最强湍流，σ²_I=0.684，AO 抑制后） | 波动光学 35 相屏，r₀=0.039m | **最低 1e-4** | 否 | 在 1e-4 处量化 2.3dB 功率惩罚，不到 1e-5 |
| **Valjus/sat.1553 综述**（σp²=0.029–0.25，弱-中） | 统计 PDF（对数正态/β）| **主动锚定在平均 BER=1e-3** | 否，主动停 | "比 1e-3 更低靠 soft-decision FEC" |
| **Shoji JLT 2012** | **不建模湍流**（只 Doppler）| "error-free" 或 2e-3 地板 | 否 | 低 OSNR 报 0.002，coding 交未来工作 |
| **Paillier ICSOS 2019** | **不建模湍流**（恒功率）| **无 BER 曲线** | N/A | 只报相位误差方差/锁定 SNR |
| **Fan OptComm 2024**（注意：**不是 Wang OE 2024**）| **不建模湍流**（只 CFO）| 单点 BER=1e-3@−48dBm | 否 | 只在灵敏度点报 1e-3 |

**外部证据**（Semantic Scholar API）：
- Optics Express 2026（DOI 10.1364/oe.596556）把"**BER floor limitation of OOK modulation in atmospheric turbulence channels**"当问题立项——error floor 是领域公认要解决的现象。
- IEEE TCOMM 2020（DOI 10.1109/TCOMM.2020.3008459）专门为"强湍流 BER + 中断容量统一公式"立项——承认平均 BER 在深衰落下饱和。

**对我们 64–81dB 的含义**：我们的"到 1e-5 需 64–81dB"比 Paillier（σ²_I=0.684，BER 到 1e-4）更极端。两种可能（都待核实）：(1) 我们的 σ²_R 比 0.684 更深（即确实是该报的"强湍流"，甚至更深）；(2) 我们的 BER 衰减率慢（~1.4×/2dB，H002 实测）就是强湍流的特征斜率，Paillier 没报全斜率。**无论哪种，"强湍流 BER 衰减率变缓降不到 1e-5"本身是领域已知现象，不是我们的 bug。**

### B. 强湍流场景别人怎么呈现性能（四种做法，关键证据）

| 处理方式 | 代表论文 | 具体做法 | 硬度 |
|---------|---------|---------|------|
| **(a) 照画 BER 不凑 1e-5** | **Paillier JLT 2020**（本批最强湍流，σ²_I=0.684）；Shoji JLT 2012 | BER 瀑布只画到实际可达（1e-4 或"error-free"），在目标 BER 处报 dB 惩罚，**不强凑 1e-5** | 🟢 最对齐我们 |
| **(b) BER + outage 联合**（非替换 BER）| IEEE TCOMM 2020（DOI 10.1109/TCOMM.2020.3008459）；IEEE TVT 2024（10.1109/TVT.2024.3399408）；MWIR-MIMO（10.1515/joc-2023-0182）；UAV-relay（10.1007/s11082-023-04772-2，79 cites）| 平均 BER 饱和时补充 outage probability。⚠️ **注意是"BER 和 outage 同时给"，不是替换** | 🟡 补充 |
| **(c) post-FEC BER / FEC 极限** | OECC 2025（10.23919/OECC/PSC62146.2025.11109630）；5G-NR LDPC（10.1109/RAEEUCCI63961.2025.11048345）；DWDM-LDPC（10.1515/joc-2026-0158）；turbo（10.2299/jsp.24.167）| 明确画"BER under FEC limit"或带/不带 LDPC 对比 | 🟢 与导师措辞呼应 |
| **(锚定单一 BER 工作点）** | **Valjus/sat.1553**；Fan OptComm 2024 | 选 1e-3 作锚，其余交 FEC | 🟢 直接对照基线 |

### C. 10⁻⁵ 底线在 FSO 领域 = post-FEC 工作门槛；pre-FEC 通行基准是 1e-3

**领域主流量化基准是 1e-3，不是 1e-5**：
- sat.1553 原文：基线 SNR 选在"**average BER of 10⁻³**"，"比 10⁻³ 更低要靠 soft-decision FEC"。
- Paillier 在 1e-4 报功率惩罚。
- **1e-5 几乎总是 post-FEC 的产物**——pre-FEC 瀑布到 1e-3/1e-4 就交给 FEC，这是 coherent sat-FSO 子领域的通行做法。

**导师原话关键限定词**（voice.md S003 段，原话）：**"在有编译码的情况下，10⁻⁵ 是底线"**——"在有编译码的情况下"这五个字直接指向 **post-FEC**，是 D003 解读 B（要曲线画到 1e-5 / 10⁻⁵ 是 FEC 后工作门槛）的有力证据，而非解读 A（要增益在 1e-5 仍成立）。"不能比 1e-5 再差"="译码后 BER 不能劣于 1e-5"，是通信工程常识（FEC 后工作门限），不是给 pre-FEC 增益设靶。

## 结论

**调研问题 1（普遍现象？）**：✅ 是。error floor / BER 衰减率变缓在强湍流下是领域公认现象（OE 2026 / IEEE TCOMM 2020 立项即为此）。但注意——本地对照论文的"强湍流"强度（最强 σ²_I=0.684）普遍比我们到 1e-5 需 64–81dB 的工况温和，我们的场景可能更深（待核对 σ²_R）。

**调研问题 2（别人怎么呈现？）**：四种做法并存，**与我们对齐度最高的是 (a) 照画 BER 不凑 1e-5（Paillier JLT 2020，本批最强湍流对照基线）+ (c) post-FEC/锚定工作点（sat.1553）**。(b) outage 是补充指标不是替换，平均 BER 饱和时加一段。

**调研问题 3（1e-5 是 pre 还是 post-FEC？）**：✅ **post-FEC**。领域 pre-FEC 通行基准是 1e-3（sat.1553）/ 1e-4（Paillier），1e-5 是 FEC 后工作门槛。导师原话"在有编译码的情况下"五个字直接锁定 post-FEC 解读。

## 对决策的影响

**直接支撑 D003 解读 B（主线倾向），削弱解读 A（致命）**：

1. **导师措辞"在有编译码的情况下"** = post-FEC，领域证据（1e-3 pre-FEC 锚 / 1e-5 post-FEC 门）一致。解读 A（"要增益在 1e-5 仍为正"）与领域惯例冲突——没人这么要求。
2. **问导师时可带的定心丸**：强湍流 BER 降不到 1e-5 是领域已知现象（不是我们菜），Paillier（JLT，档级顶刊）也只画到 1e-4。我们的做法（画到能到的最低 + 标 HD-FEC 不可达 + 工作区形态卖点）与 Paillier 一致。
3. **不新建 D###**（本调研是支撑 D003 的证据材料，不改方向/架构。D003 待问导师的状态不变，但主线判断 B 的信心从"倾向"升到"有领域证据支撑"）。

**建议（供主线/用户问导师时参考，不改任何决策）**：
1. **不硬凑 1e-5**：strong/uplink BER 瀑布画到实际可达（2e-4~1e-3，H002 数据），在固定 BER 处报 dB 增益——对齐 Paillier JLT 2020 + sat.1553（都是 COMPARISON_REFS 直接对照基线，审稿人会认）。
2. **加 outage probability 作强湍流补充指标**（IEEE TCOMM 2020 / TVT 2024 惯例）：一段话说明"平均 BER 在深衰下达不到 FEC 阈值，故补充中断概率"。⚠️ 这是补充不是替换。
3. **显式衔接导师措辞**：论文/简报里加一句"pre-FEC BER 基准取 1e-3/1e-4（与 sat.1553 一致），10⁻⁵ 为 post-FEC 工作门槛（导师要求）"，把导师的 1e-5 底线和领域惯例显式衔接。
4. **核对 σ²_R**：确认我们的湍流强度设定是否就是该报的"强湍流"，还是比 Paillier（σ²_I=0.684）更深，避免审稿人质疑工况设定。

## 调研局限（诚实标注）

- **Semantic Scholar 无 key 档限速**：搜索 2（卫星 FSO outage probability）和搜索 4（相干 FSO 相位噪声 BER）持续 HTTP 429，40+ 分钟冷却未恢复。卫星-FSO 子领域 outage 用法的"频率"和 coherent-detection 相位噪声贡献未直接验证（**AI 推断，未验证**）。
- **10⁻⁵ = pre-FEC 阈值这一具体数字**：未在任何 abstract 中原文出现（**AI 推断，未验证**）——与导师"在有编译码的情况下"措辞一致，但精确数值边界建议对照全文核实。
- **Wang OE 2024 未定位**：COMPARISON_REFS #16 标注的"Wang Opt. Express 2024"（相屏湍流 + 16QAM）在本轮未直接读到原文；`papers/doi/10.1016_j.optcom.2024.130981` 实为 Fan et al. OptComm 2024（只报 1e-3 灵敏度点，无湍流 BER）。Wang OE 2024 的强湍流 BER 处理方式（文件记录"四支路强湍 16QAM 改善 ~2.46dBm"）是 dBm 灵敏度增量非 BER 瀑布，**后续若要引用需补读原文**。
- **本地 5 篇无一覆盖真·强湍流（σ²_R>1）BER 瀑布**：Paillier σ²_I=0.684 是最接近的，仍未到饱和区。若需真·强湍流 BER/error-floor 数据，需补 wave-optics 或 Gamma-Gamma/Málaga 信道 BER 论文。

## 关键引文清单（带源 DOI，供后续引用溯源）

**本地精读**：
- Valjus, Wolf, Poliak (2025), "Review and Analysis of DSP Algorithms for Coherent Optical Satellite Links," *Int. J. Satell. Commun. Network.* 43(3):229–250. DOI 10.1002/sat.1553
- Paillier, Le Bidan, Conan, Artaud, Védrenne, Jaouën (2020), "Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop," *J. Lightwave Technol.* DOI 10.1109/JLT.2020.3003561
- Shoji, Fice, Takayama, Seeds (2012), "A Pilot-Carrier Coherent LEO-to-Ground Downlink System Using OIPLL," *J. Lightwave Technol.* 30(16):2696–2706. DOI 10.1109/JLT.2012.2204037
- Paillier et al. (2019), ICSOS. DOI 10.1109/ICSOS45490.2019.8978983
- Fan, Ju, Liu et al. (2024), *Optics Communications* 572:130981. DOI 10.1016/j.optcom.2024.130981（**注意：非 Wang OE 2024**）

**外部检索（Semantic Scholar API）**：
- IEEE TCOMM 2020，强湍流 BER + 中断容量统一公式，DOI 10.1109/TCOMM.2020.3008459（32 cites）
- IEEE TVT 2024，UAV-DF relaying，outage + BER 联合，DOI 10.1109/TVT.2024.3399408（14 cites）
- Opt. Quantum Electron. 2023，UAV-relay OWC，SER + outage + SNR，DOI 10.1007/s11082-023-04772-2（79 cites）
- J. Opt. Commun. 2023，MWIR-MIMO 强湍流 BER + outage，DOI 10.1515/joc-2023-0182（3 cites）
- Optics Express 2026，CNN-DMD 缓解 OOK BER floor，DOI 10.1364/oe.596556（0 cites）
- Sensors 2024 survey，76 cites，DOI 10.3390/s24248036
- OECC/PSC 2025，BER under FEC limit，DOI 10.23919/OECC/PSC62146.2025.11109630
- 5G-NR LDPC for FSO，DOI 10.1109/RAEEUCCI63961.2025.11048345
- DWDM-LDPC BPSK 强湍流，DOI 10.1515/joc-2026-0158
- Turbo code 强湍流，DOI 10.2299/jsp.24.167
