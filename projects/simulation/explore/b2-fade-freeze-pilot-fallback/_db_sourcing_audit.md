# 阶段 0.2：dB 溯源核查（sat.1553 L440 +1dB 口径限定）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 0.2
> 日期: 2026-07-08
> 守: INVARIANT 12（dB 口径错位前置核查）+ INVARIANT 13（饱和池难出区警示）+ FR-26（读原文数值）+ V6（读原文数值）
> 输入: sat.1553 content.md L430-460 原文（主线 Read 核查）+ `_cut-b1b2b3-verify.md:144-145, 342`（二次引用对照）

## 0. 核查目标

**INVARIANT 12 要求**：把 sat.1553 L440 "+1dB pilot 在 fade" 限定到原始口径，B2-Q2 的 FOE freeze 双模切换增量是独立 MVE 的事。**不能引 sat.1553 +1dB 当 B2-Q2 的 dB**。

**核查动作**：读 sat.1553 content.md L430-460 原文（FR-26 读原文数值，不只引 _cut-b1b2b3-verify.md 的二次引用）。

## 1. sat.1553 L440 原文数值（主线 Read 核查）

### 1.1 原文精确引用（`papers/doi/10.1002_sat.1553/content.md:440`）

> "its [differential encoding] performance degrades fast at low SNR, such as during fades, which can be seen in scenario 4, where the penalty is almost **1.5 dB**. Pilot-based phase estimation has similar performance to differential encoding but performs much better during fades. In fact, **using pilots in scenario 4 could provide a 1 dB improvement over Viterbi–Viterbi with differential coding**."

### 1.2 原口径精确锁定

| 字段 | 原文数值 | 来源 |
|---|---|---|
| **+1dB 含义** | pilot-based 相位估计（PE）**vs** VV+差分编码 | content.md L440 |
| **对比方法** | pilot PE（pilot rate 7/8, 15/16, 31/32，线性插值）vs VV（window N=32）+ differential coding | content.md L433-437 |
| **场景** | scenario 4（上行强湍 σp²(Rytov)=0.25）| content.md L161 + L440 |
| **调制** | **QPSK**（不是 16-APSK）| content.md L432 "for QPSK" |
| **信道** | AWGN + 激光线宽 PN（Equation 17，Wiener）| content.md L432 |
| **测度** | SNR penalty @ BER=10⁻³（相对无 PN 参考系统）| content.md L433-434 |
| **符号数** | 10⁷ symbols per SNR value | content.md L432 |
| **VV+diff penalty** | ~1.5 dB（scenario 4）| content.md L440 |
| **pilot vs VV+diff** | +1 dB（pilot 比 VV+diff 好 1 dB）| content.md L440 |
| **→ pilot 自身 penalty** | ~0.5 dB（1.5 − 1 = 0.5，scenario 4）| 推算 |

### 1.3 sat.1553 自己的限定（content.md L437-440）

> "The implementation parameters have been chosen to show the strengths and weaknesses of the different algorithms, but it should be noted that **the number of symbols used to estimate the phase could be further optimized for specific scenarios**."

→ sat.1553 自己说 +1dB 是**特定参数下的对比**，不是普适量。

## 2. 口径错位分析（B2-Q2 为什么不能搬这个 +1dB）

### 2.1 五重口径差异

| 维度 | sat.1553 +1dB 口径 | B2-Q2 增量口径 | 差异 |
|---|---|---|---|
| **对比方法** | pilot PE vs VV+差分编码 | 双模切换 vs 纯 blind freeze | 完全不同（VV+diff 不是 blind freeze）|
| **估计对象** | 相位估计（PE，CPE）| FOE freeze + 模式切换 | PE vs FOE 不同对象 |
| **调制** | QPSK | 16-APSK M₀=8 | 不同调制（16-APSK 升幂阶数高）|
| **场景** | OFDM-ish（综述语境）+ AWGN PN | 单载波时域 + GG 块衰落 | 不同信道（频选 vs 时选）|
| **测度** | SNR penalty @ BER=10⁻³ | fair gain @ HD-FEC 3.8e-3 或动态恢复时间 | 不同测度 |

### 2.2 物理根因（为什么 sat.1553 +1dB 在单载波时域可能不成立）

**sat.1553 场景**（OFDM/QPSK + AWGN PN）：
- 差分编码在 low SNR（fade）时性能退化（需要信噪比门限）
- pilot PE 在 fade 期间仍能用 pilot 符号估相位（pilot 符号已知，不依赖判决）
- → pilot 比 VV+diff 好 1 dB（fade 期间 diff 退化，pilot 不退化）

**B2-Q2 场景**（单载波时域 + GG 块衰落）：
- step4a 实测：DA pilot（pilot-aided ML）在 fade 块 BER 崩溃（pilot 跟数据同信道，fade 同步影响两者）
- NDA-ML（盲）用全块平均 dilute 单点 fade → 鲁棒
- → **单载波时域下 pilot 反而比 blind 差**（step4a 实证，跟 sat.1553 OFDM 结论方向相反）

**根因**：sat.1553 的 +1dB 是 pilot PE 比 VV+diff（两种都依赖判决/差分，在 fade 都退化，pilot 稍好）；B2-Q2 比的是 pilot-aided vs blind ML（blind 用全帧积分，fade 鲁棒性不同机制）。**不是同一组对比**。

### 2.3 饱和池 dB 难出区警示（INVARIANT 13）

切法地图 `_cut-map-final-b1-b12.md:48` 把 sat.1553 pilot +1dB 归入"vs 传统 baseline（明确 SNR/BER dB）"第一梯队，但 `_cut-b1b2b3-verify.md:342` 自己警示：

> "sat.1553 的'pilot 场景 4 比 VV+diff 好 1 dB'是 B1 切入点最关键的 dB 锚——但 B1 草稿已正确指出'这是 pilot vs VV 的差，不是自适应 N vs 固定 N 的增量'，主线引用时必须保留这个条件性区分"

→ +1dB 是 **pilot vs VV+diff** 的差，**不是** B2-Q2 双模切换相对纯 blind freeze 的增量。B2-Q2 增量未量化，需独立 MVE。

## 3. B2-Q2 的 dB 来源（必须独立 MVE 产出）

### 3.1 B2-Q2 候选 dB 来源（都不是 sat.1553 +1dB）

| 来源 | 机制 | 可信度 | 备注 |
|---|---|---|---|
| **fade 恢复时间缩短** | pilot fallback 在 fade 期继续跟踪，恢复时无需 blind 重收敛 | 待 sandbox 验证 | B2-Q2 最可能的增量维度（阶段 0.1 维度 B）|
| **稳态 BER 改善** | 双模切换在非 fade 期用 blind（跟 NDA-ML 一样），fade 期用 pilot | 待 sandbox 验证 | 稳态 BER 维度 B2-Q2 不应比纯 blind 差，但也好不了多少 |
| **工作区扩展** | strong 湍流下纯 blind freeze HD-FEC 不可达，双模切换可能可达 | 待 sandbox 验证 | 饱和池 dB 难出区，可能靠范围维度够格（D005 会议门槛）|

### 3.2 不能引 sat.1553 +1dB 当 B2-Q2 的 dB（INVARIANT 12 红线）

**禁止引用**：
- ❌ "B2-Q2 增量 ~1dB（sat.1553 L440）"——口径错位
- ❌ "pilot 在 fade 比 blind 好 1dB"——sat.1553 没说这个（说的是比 VV+diff）
- ❌ "sat.1553 综述证明 pilot-aided 在 fade 更优"——sat.1553 只在 OFDM/QPSK 证，单载波时域反证（step4a）

**允许引用**：
- ✅ "sat.1553 L440 在 QPSK+AWGN PN scenario 4 下 pilot PE 比 VV+diff 好 1dB（**PE 方法对比，不是 FOE freeze 双模切换增量**）"
- ✅ "B2-Q2 增量待 MVE（阶段 0.1 张力验证设计已分解为 4 维度，sandbox 三方对照后定量）"

## 4. 意外发现：sat.1553 L440 的 B2-Q2 叙事锚点

### 4.1 原文发现（content.md L440）

> "In addition, pilot-based phase estimation **could be combined with a second blind phase estimator to further improve performance** [58]."

**这是 sat.1553 综述作者明确提出的方向**——"pilot + 盲相位估计器组合"，正好是 B2-Q2 双模切换的**叙事锚点**。

### 4.2 对 B2-Q2 A1 归属的价值

- **A1 归属**（创新点定位）：B2-Q2 双模切换是"pilot + blind 组合"的具体实现（fade 时切 pilot，非 fade 时用 blind）
- **sat.1553 [58] 引用**：综述作者提了这个组合方向，但没说具体怎么做——B2-Q2 是把这个 open direction 具体化
- **动机叙事**：可以用"sat.1553 L440 自报 open direction"作为 B2-Q2 的动机锚（切法地图 §A.4 "open problem 自报 → 填空白"~5% 证据链最强）

### 4.3 注意事项

- sat.1553 没给"组合"的具体 dB（只说"further improve"），B2-Q2 的增量仍需 MVE
- ref [58] 的具体论文待查（content.md reference list 未完整转换，需补查）——这是阶段 0.5 参数真相源的附带任务

## 5. 阶段 0.2 结论

### 5.1 sat.1553 +1dB 口径已限定

**原口径**：pilot PE vs VV+diff @ QPSK + AWGN PN scenario 4，SNR penalty @ BER=10⁻³，+1dB。

**限定使用**：
- 可作为"pilot 在 fade 期间比差分编码好"的**定性证据**（PE 方法对比）
- **不可作为 B2-Q2 双模切换的 dB 增量**（口径错位：PE vs FOE freeze / QPSK vs 16-APSK / OFDM vs 单载波 / penalty vs fair gain）

### 5.2 B2-Q2 真实增量来源

**必须独立 MVE 产出**，候选维度（阶段 0.1 已分解）：
1. fade 恢复时间（最可能）
2. 稳态 BER（不应差，也好不了多少）
3. 工作区扩展（strong 湍流，饱和池 dB 难出区可能靠范围维度）

### 5.3 债务更新

| 债务 | 阶段 0.2 后状态 |
|---|---|
| sat.1553 +1dB 口径限定 | ✅ 已限定（本文件）|
| B2-Q2 真实增量未量化 | pending MVE（阶段 3）|
| ref [58] 具体论文待查 | pending（阶段 0.5 附带）|

### 5.4 阶段 0.2 完成，进阶段 0.3

dB 溯源核查完成，sat.1553 +1dB 已限定到原始口径（PE vs VV+diff），B2-Q2 增量来源已明确（必须 MVE 产出）。进阶段 0.3 架构定性（下一对话）。

## 附：核查机制记录（FR-26 读原文数值）

| 声称 | 核查方式 | 结论 |
|---|---|---|
| sat.1553 L440 +1dB = pilot vs VV+diff | 主线 Read `content.md:440` 原文 | ✅ PASS（"1 dB improvement over Viterbi–Viterbi with differential coding"）|
| scenario 4 = 上行强湍 σp²=0.25 | 主线 Read `content.md:161` + L440 | ✅ PASS |
| 调制 = QPSK | 主线 Read `content.md:432` "for QPSK" | ✅ PASS |
| 测度 = SNR penalty @ BER=10⁻³ | 主线 Read `content.md:433-434` | ✅ PASS |
| VV+diff penalty ~1.5dB | 主线 Read `content.md:440` "penalty is almost 1.5 dB" | ✅ PASS |
| sat.1553 提"pilot+盲组合"open direction | 主线 Read `content.md:440` "combined with a second blind phase estimator [58]" | ✅ PASS（B2-Q2 叙事锚点新发现）|

**未交叉验证项**：ref [58] 具体论文（content.md reference list 未完整转换，pending 阶段 0.5）
