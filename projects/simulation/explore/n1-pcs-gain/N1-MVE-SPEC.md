# N1 §4a 维度 D MVE 规格（子 agent 执行契约）

> 来源: S010 §B CONDITIONAL GO 留下的待闭合项 | 框架: gw-feasibility.md §D
> 日期: 2026-06-17 续 7 | 执行方式: 子 agent 写脚本 + 运行 + 返回数字

## 1. 核心假设

**在强湍流（Gamma-Gamma, α=1.5/β=0.8, 对应 σ²_R>1 strong）下，离线静态 PCS（单一 Maxwell-Boltzmann 分布，Elzanaty blind 范式）相比均匀 16-QAM，在固定 AIR 工作点的 SNR 增益 ≥ 0.5 dB。**

这是 S010 §B 判定的 AMBIGUOUS 项：§B 结构上无致命原因（0/5 致命），但强湍流幅度需实证闭合。

## 2. TL-20 理论预期（MVE 跑之前必须写明，偏离即查）

基于 Tian 2021 机制（content.md L560/L564）+ 信息论上限推导：

| 湍流 | 机制 | 预期 AIR gain (dB) | 预期排序 |
|------|------|--------------------|----------|
| weak (α4/β3) | 高 SNR 主导，PMF→uniform，gain 趋零 | **< 0.3**（趋零） | 3（最小）|
| moderate (α2.5/β1.8) | 中 SNR 甜区，分布整形空间大 | **0.3-0.8**（甜区） | 1（最大）|
| strong (α1.5/β0.8) | deep fade 底部 gain 归零 + 中低 SNR 块 gain 大，平均取决于 deep fade 占比 | **AMBIGUOUS 0.2-0.8** | 2（待量化）|

**物理依据**：
- Tian L564 直证："the gain between the two PS schemes and the uniform distribution **increases with the increase of the SER**"——高 SER（强湍流区）gain 更大
- 但 deep fade 底部（h→0）噪声主导，任何输入分布趋同，gain 归零
- MB 分布在 AWGN 下对 16-QAM 的 shaping gain 理论上限 ≈ 0.5-1.0 dB（Böcherer 2015）——**硬天花板**

**量化锚点（偏离即停查代码，TL-20）**：
- 强湍流 gain < 0.1 dB 或为负 → **可疑**（违背 Tian "gain↑ with SER"，除非 deep fade 占比压倒性）→ 查 MB 分布设计是否在代表性 SNR 上
- 任一湍流 gain > 2 dB → **可疑**（超 MB 理论上限）→ 查 AIR 计算 / 功率归一化
- 弱湍流高 SNR 区 AIR 不趋近 4 bit/sym → **bug**（16-QAM 上限是 4）
- uniform 在 AWGN（h=1 无湍流退化）下 AIR 应随 SNR 单调上升到 4

## 3. 最小实例（FR-04 保真度检查）

**保留的核心结构属性**（简化不得删除）：
- ✅ Gamma-Gamma 块衰落（deep fade，h 跨数量级波动）——复用 `projects/simulation/common/_channel.py:gg_block`
- ✅ 16-QAM 星座 + Gray 映射——复用 `projects/simulation/common/_modulation.py:qam16_*`
- ✅ 离线单一 MB 分布（不跨 RTT 自适应）——**N1 核心**，新实现
- ✅ 相干检测约定（h 实值辐照度，信号 √h，TL-01）——复用 `_channel.py` 的 `signal = tx * np.sqrt(h)`

**合理简化**（不删除核心结构）：
- 省略多普勒 + 相位噪声：PCS 是幅度/符号概率分布优化，与相位恢复正交（S010 §B 原因2 已证：A3 处理相位，N1 处理幅度分布，正交物理量）。MVE 隔离 PCS 增量，不加相位损伤
- 省略 FEC：用 AIR（BMD rate）替代 post-FEC BER（避免 LDPC 选择偏差，R007 限制 #2 量化点）
- 块内 h 恒定（BLOCK=100，现有约定）

**FR-04 结论**：简化保留了 PCS 增益所需的所有结构（GG 幅度分布 + 非均匀概率设计空间），结论可外推到含相位/FEC 的完整系统。若 gain 在此最小实例下不成立，完整系统下也不成立（简化对 PCS 更有利，非更不利）。

## 4. baseline 设计（FR-14 先验对照 + FR-15 目标 baseline）

| baseline | 角色 | 实现 |
|----------|------|------|
| **uniform 16-QAM** | FR-14 先验 + FR-15 目标 baseline（N1 贡献声称要超越的对手）| ν=0 的 MB 分布 = 均匀 |
| **offline MB（单一分布）** | **N1 候选方法** | Elzanaty blind：按 GG 长期 CDF 选代表性 SNR（中位数），在该 SNR 搜索 ν 最大化 AIR，整帧用此固定分布 |
| **per-block oracle MB** | CSI-aware 上界对照（非 baseline，验证"离线"离上界多远）| 每块用该块瞬时 SNR 的最优 ν |

**N1 vs Tian 的增量定位**：Tian 用 PSO 全搜索找 16 点任意 PMF；N1 限定 MB 分布族（单参数 ν）+ Elzanaty blind 离线设计。N1 gain 预期 ≤ Tian 1.3dB（参数化简化代价）。

## 5. pass/fail 标准（预定义）

主指标：**强湍流（strong）AIR gain (dB @ 固定 AIR 工作点)**

工作点选取：AIR = 3.0 bit/symbol（16-QAM 中段，4 的 75%，deep fade 影响显著区）。在该 AIR 下读 uniform 和 offline-MB 所需 SNR 差 = gain。

| 判定 | 条件 | 含义 |
|------|------|------|
| **Go (§D PASS)** | strong gain ≥ 0.5 dB @ AIR=3.0 | 假设成立，N1 可进 Step 5 |
| **Conditional Go** | 0.3 ≤ strong gain < 0.5 dB | 薄增益，记录风险，需论证或调整（TL-05：gain<1dB 叙事转分析）|
| **Kill/Fail** | strong gain < 0.3 dB 或为负 | 核心假设不成立，N1 降级/排除 |

**辅助判定（非一票否决）**：
- moderate gain 应 > strong gain（甜区预期）。若 strong > moderate 反常 → 查代码
- offline-MB vs per-block-oracle gap：gap 大说明"离线"损失大，记录但非致命（N1 本就是离线简化）

## 6. 扫描设计

- 湍流：weak / moderate / strong（params.py 现有值）
- γ̄（dB）：0, 4, 8, 12, 16, 20（覆盖 deep fade 到高 SNR）
- 每点：N_sym = 2×10⁵ 符号蒙特卡洛，seed 固定（可复现）
- 方案：uniform / offline-MB / per-block-oracle 三条曲线
- 输出：AIR vs γ̄ 曲线（每湍流一张）+ gain 表

## 7. AIR 计算（BMD rate）

对 16-QAM，4 bit Gray label (b0,b1,b2,b3)。BICM AIR：
```
R_BMD = Σ_{k=0}^{3} I(b_k; Y) = 4 - Σ_k H(b_k | Y)
```
每 bit 用 LLR 直方图法估 H(b_k|Y)（标准做法，参考 Böcherer 2015 / Tian Eq.12-14）：
- 给定 y，算每 bit 的后验 LLR：L_k(y) = log( Σ_{x: b_k=0} P(y|x)P(x) / Σ_{x: b_k=1} P(y|x)P(x) )
- P(y|x) = CN(y; √h·x, σ²)，σ² = 1/(2·γ_bar·h)（瞬时 SNR = γ_bar·h，相干约定）

校验：uniform + AWGN（h≡1）下 R_BMD 应随 SNR 单调上升到 4，趋势对照 Shannon 2·log2(1+γ)。

## 8. 执行约束

- **时间预算 ≤ 600s**（AGENTS.md 子 agent 上限 + R006 教训）
- 脚本放 `.sessions/2026-06-10-research-direction-exploration/mve/n1_pcs_gain_mve.py`
- 从 `projects/simulation/common/_channel.py` 导入 `gg_block`，从 `_modulation.py` 导入 QAM（TL-25 #3：不自建信道生成）
- 输出 JSON 含：每 (turb, γ_bar) 的 {uniform_AIR, offline_mb_AIR, oracle_AIR, offline_mb_nu}
- 结果图（可选）存同目录 PNG
- 环境探测：优先 WSL `~/.venvs/torch/bin/python`；探测失败用系统 python3（只需 numpy/scipy）

## 9. 子 agent 返回（≤500 词摘要）

返回必须含：
1. 三湍流等级的 uniform vs offline-MB vs oracle AIR 曲线关键点（@ AIR=3.0 的 gain dB）
2. offline-MB 选的 ν 值（每湍流）
3. 任何偏离 TL-20 预期的点（标注"DEVIATION"）
4. 一句话判定建议（Go/Conditional/Kill）+ 理由
5. 环境用哪个 python，运行耗时

不返回：完整曲线数据（存 JSON）、完整代码（存脚本文件）。主对话读 JSON 复核。
