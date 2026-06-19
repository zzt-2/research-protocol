# [S001] Groundwork §A0/FR-20/FR-21 — 4b#1 方向 Kill

> 2026-06-19 | Groundwork §A0/A'/A 可行性预判 + FR-20 参数溯源 + FR-21 oracle 上界门控 | 状态: 完成（方向 Kill）

## 目标

接续上游定方向专题（2026-06-17-thesis-method-redirection 已 closed，D006 裁定 4b#1），进 Groundwork 阶段做 §A0/A'/A 可行性预判 + FR-20 参数溯源 + FR-21 oracle 上界门控 + §D MVE 验证 GG-LCR/AFD→B/D 解析可行性 + 仿真链路搭建。

实际本轮完成：§A0 前置（FR-20 + FR-21）即触发 Kill，未进 §D MVE / 仿真链路（FR-21 门控设计意图即如此）。

## 记录

### 1. Session Start + H004 接收方验证

报到完成（topic-index/registry/profile/voice 全检）。H004 接收方验证 3/3 PASS：
- 唐承茂 L2053"交织器开关"展望原话 ✓（Grep 验证逐字）
- Le 2021 = 卫星-UAV FSO LCR/AFD 闭式 ✓（R001 §F17 三处引用）
- D006 开环形态不撞坑3 ✓（坑3 = CSI 反馈延迟 ρ(RTT)<0.03，开环绕开）

**1 个缺口**：Le 2021 content.md 未下载到本地 papers/doi/，§F17 子 agent 仅核查 abstract。

### 2. 方法形态确认

用户选 **C（先 B 解析/数值优化保底，推不出退 RL）**，第一步先做 FR-21 oracle 上界 + §A0。

### 3. FR-20 参数溯源（本地 + web）

**本地（唐承茂 content.md，一手）**：
- 表 4-1：Cn²=1e-15 m^-2/3（中弱湍流）/ L=200km / H=10km / λ=1.55µm / 接收孔径 100mm / 接收灵敏度 -40dBm / SNR=10-20dB
- 表 4-3：Polar N=1024 R=0.5 + CA-SCL(L=8,CRC24-C) + 卷积交织 **B=27/D=38 静态** + OOK + 仿真次数 1e7
- 表 4-4：SNR=20dB 实测 BER（Cn²=1e-16→2.1e-6 / 1e-15→6.5e-6 / 1e-14→7.3e-5 经交织编码）
- L1081-1088：Lburst≈800 反推 B=27（thandle≈30bit，3GPP TS 38.212 估算）
- L440-468：LCR/AFD/Markov 双状态框架（Gilbert 1960 + Rappaport）

**web（子 agent 2026-06-19 核查 Le 2021）**：
- ⚠️ **DOI 疑点**：用户给的 10.1109/JPHOT.2021.3097363 三库查无，正确可能 10.1109/JPHOT.2021.3057198
- ⚠️ **湍流模型存疑**：abstract 未出现 "Gamma-Gamma"，仅称 "atmospheric turbulence conditions"——上游 D006"GG+指向 LCR/AFD 闭式"声称需全文确认
- 指向误差：Beckmann 四参数分布（非标准高斯 σ_x）
- 已确认：LEO satellite-to-UAV，LCR/AFD 闭式（核函数形式需全文）

**风险标记**：Le 2021 湍流模型存疑不影响 FR-21（FR-21 是下游交织增益，不依赖上游统计具体形式），但影响 §F17"GG-LCR/AFD 解析链"创新核描述。方向 Kill 后此风险 moot。

### 4. FR-21 oracle 上界门控（三版，详见 V001）

**版本 1 主脚本 MC 上界**：自适应 vs 全程最优静态 = -0.5~-0.8 dB（Kill 信号）
**版本 2 敏感性瀑布**：+0.6~+3.3 dB——**判定伪信号**（瀑布用 Lb 均值忽略 Exp 尾部）
**版本 3 唐承茂校准**：BER 维度增益 = 0 dB（B=27 全程够用，0/15 仰角超容）——**决定性**

### 5. 时延先例调研（子 agent 2026-06-19）

8 组 CNKI/WebSearch 关键词全空：**交织层时延作主指标中文硕论先例 0 篇**。Pivot 到"时延-BER 联合优化"无对标，毕业风险高。

### 6. Kill 决策与用户确认

三段呈现后用户确认："kill吧。"（voice.md 2026-06-19）。触发 D001。

## 决策引用

- **D001**（新建）：4b#1 BER 维度 + 时延维度双 Kill。回定方向专题重选
- 上游 D006（被本专题 D001 推翻执行，但 D006 本身在上游专题不动）：方向裁定 4b#1
- 上游 D005（仍有效）：增量改进定位

## 范围确认

- 本轮是否在 scope boundary 内：**是**。FR-21 oracle 上界门控是 Groundwork §A0/A' 的前置检查（gw-feasibility.md §A0 第 6 项"先验覆盖检查" + FR-21），在本专题"§A0/A'/A 可行性预判 + FR-20 + FR-21"范围内
- Kill 是 FR-21 门控的设计意图（TL-27 / FR-21："上界 <0.5dB → 直接 Kill 不跑 MVE，省时间"），不算范围越界

## 后续

### 本专题收尾（本轮剩余工作）

1. ✅ D001（decisions.md）
2. ✅ V001（verifications.md）
3. ✅ voice.md（已建）
4. ⬜ 更新 topic-index（状态 Kill + 结论 + 进展线索）
5. ⬜ 更新 _registry.yaml（status active → closed）
6. ⬜ 写 H001 handoff（给"重新定方向"的下一专题）

### 下一专题（重定方向）需关注的

1. **4b#1 死因 + 4 条殊途同归**：N1/③/A3/4b#1 全死在"当前信道设定（星地 GG 湍流 + Polar + LEO）信号处理增量窄"。**重定方向时应显式分析这个共同根因**——可能这个信道设定本身就不该做信号处理增量，需换信道设定（如非相干 IM/DD？不同编码？不同频段？）或换层（MAC/网络？）
2. **D006 排除列重新审视**：4b#3/4b#4/I/Q/A3/C3/盲均衡/C6/码型切换都被排除了，需看哪些排除理由在"4b#1 已死"前提下是否仍成立
3. **可复用资产**：FR-21 门控方法学（三版范式）、唐承茂参数溯源、HV slant-path 模型、4b#1 物理天花板量化结论
4. **未验证项**：Le 2021 DOI/湍流模型（moot，但若重定方向涉及 LCR/AFD 上游需补全文精读）
