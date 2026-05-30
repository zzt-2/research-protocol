# PROMPT-007: 方向 E 深入 — 湍流信道跟踪与预测

> 用途：新对话中深入探索方向 E（信道跟踪预测），评估是否可作为 Ch3 替代方案
> 前置：S001 已完成初筛（E 有 ~25-30 英文 + ~10-12 中文文献，评为 Go）
> 目标：产出 Go/No-Go 判断 + 如果 Go 则完成 MVE

## 论文背景

硕士论文《星地激光通信信号处理关键技术研究》。当前章节结构：

```
Ch2 星地激光通信系统与信道模型（含信道估计）
Ch3 ★★★ 候选方向之一 ★★★
Ch4 低轨星地载波同步算法（核心创新：三个湍流自适应公式）
Ch5 FPGA 实现
```

Ch3 必须与 Ch2 和 Ch4 相关，形成递进链。当前首选是方向 G（BER 闭合解），但新颖性偏弱。E 是最强备选。

## 方向 E 描述

**核心思路**：研究 Gamma-Gamma 湍流信道的时变跟踪与预测方法，为 Ch4 的自适应载波同步提供实时信道状态信息。

**与 Ch4 的衔接**：Ch4 的三个自适应公式（$N_\text{opt} \propto h^{-4}$、$M_\text{opt} \propto h^{-2/5}$、$B_\text{L,opt} \propto h$）都需要知道瞬时信道状态 $h$。如果 $h$ 的估计有延迟，自适应参数就是过时的。Ch3 解决"如何准确、低延迟地获取/预测 $h$"。

**叙事链**：Ch2 建模 → Ch3 跟踪预测 $h$ → Ch4 用预测的 $h$ 设计自适应参数

## S001 已有结论

### 精读论文（4 篇）

1. **Paillier 2019** — LEO 星地相干 BPSK DPLL 载波同步，湍流相位相干时间 ~1ms
2. **Song 2021** — GRU FSO 信道预测，APE<6.9%
3. **Nguyen 2024** — ESN 信道预测 + 自适应速率/功率控制
4. **Ying 2024** — CNN+LSTM LEO 卫星信道预测

### S001 风险标记

- **时间尺度不匹配**：ms 级湍流 vs 0.1ns 符号率，创新主要是应用迁移
- 创新空间：预测 CSI 驱动载波同步

### 文献空白

信道预测结果直接驱动载波同步参数的联合设计在文献中未见（S001 检索确认）。

## 本轮需要深入评估的问题

### 问题 1：时间尺度问题有多严重？

湍流相干时间 ~1ms，符号率 1 Gsps，意味着一个湍流状态持续 ~10^6 个符号。自适应参数（N_opt, M_opt, B_L）的计算频率远低于符号率，所以"延迟"可能根本不是问题——在 1ms 内 $h$ 基本不变。

**需要分析**：
1. $h$ 在 1ms 内的变化量有多大？（GG 过程的自相关函数）
2. Ch4 自适应参数的更新频率需要多高？
3. 如果更新频率远低于湍流相干时间，"预测"就退化为"估计"，E 的意义就变了

### 问题 2：与 Ch2 信道估计的区别是什么？

Ch2 已经合并了信道估计（LS/MMSE/Kalman/DL）。E 的"信道跟踪"与 Ch2 的"信道估计"有什么本质区别？

**可能答案**：
- Ch2 的估计是"当前的 h 是多少"（瞬时估计）
- E 的跟踪是"未来的 h 会是多少"（预测）+ "置信度是多少"（不确定性量化）
- E 的贡献可能是"预测性自适应"——用预测的 h 提前调整参数，而非用滞后的 h 反应式调整

**需要验证**：这个区别是否有工程价值？如果湍流相干时间 >> 参数更新周期，预测的价值就有限。

### 问题 3：创新点是否足够强？

如果 E 的核心贡献是"用 DL 预测 h → 驱动自适应参数"，这算创新吗？
- Nguyen 2024 已经做了 ESN 预测 + 自适应功率
- Song 2021 已经做了 GRU 预测
- 区别可能是：他们预测 h 用于功率控制，我们预测 h 用于载波同步参数

**需要评估**：从"功率控制"到"载波同步"的场景迁移是否构成足够的创新？

### 问题 4：仿真可行性

**需要评估**：
1. GG 时变过程如何生成？（需要 Lee 模型或 AR 模型生成时序）
2. 预测方法实现复杂度（AR/Kalman/LSTM/GRU 哪个最合适？）
3. MVE 需要多久？（目标：2-3 天原型）

## 执行方法

1. **精读补充**（3-5 篇新论文）：
   - GG 时变信道模型（Lee 模型、AR 模型生成时序）
   - FSO 信道预测方法对比（传统 vs DL）
   - 信道预测在自适应系统中的应用

2. **时间尺度分析**（关键判断）：
   - 计算湍流相干时间 vs 参数更新周期
   - 如果相干时间 >> 更新周期，E 的价值需要重新定位

3. **MVE 设计**（如果 Go）：
   - GG 时变信道生成（Lee 模型）
   - AR(1) 预测 vs Kalman 预测 vs LSTM 预测
   - 预测 h → 自适应参数 → BER 对比固定参数
   - 目标：证明预测性自适应 > 反应式自适应 > 固定参数

4. **Go/No-Go 判断标准**：
   - Go：时间尺度分析显示预测有工程价值 + MVE 显示 >1dB 增益 + 创新点清晰
   - No-Go：预测退化为估计（无额外价值）或创新点太弱（只是场景迁移）

## 搜索工具

```bash
cd /mnt/d/code/study/research-protocol && bash tools/search "keyword" --limit 20
cd /mnt/d/code/study/research-protocol && bash tools/blit --source cnki "关键词" --doc-type master
```

## 输出

写入 `.sessions/2026-05-30-ch3-direction-exploration/` 目录：
- `R002-direction-e-deep-analysis.md` — 深入评估报告
- 如果 Go：`sim_ch3_channel_tracking.py`（MVE 仿真）
- Go/No-Go 结论 + 与 G 的对比

## 必读文件

1. `.sessions/2026-05-30-ch3-direction-exploration/S001-candidate-search.md` — 6 方向初筛
2. `.sessions/2026-05-30-ch3-direction-exploration/topic-index.md` — 专题状态
3. `毕设/写作材料/formulas-ch3ch4-sync.md` — Ch4 自适应公式（了解 h 的使用方式）
4. `projects/thesis-figures/simulation/sim_ch3_precomp.py` — AR 预测已有代码（可复用）
5. `projects/thesis-figures/simulation/sim_cascade_robustness.py` — 级联数据
6. `papers/doi/10.1109_jlt.2023.3281082/content.md` — Fernandes 2023（Doppler 参考）

## 验证环境

```bash
~/.venvs/torch/bin/python
```
