# PROMPT-008: 方向 B/C 深入 + 继续找新方向

> 用途：新对话中深入探索方向 B（自适应调制编码）和 C（Doppler 预补偿），同时继续检索新候选
> 前置：S001 已完成初筛（B 和 C 均评为 Maybe，需深入评估）
> 目标：为 B 和 C 各产出 Go/No-Go 判断，同时发现 S001 未覆盖的新方向

## 论文背景

同 PROMPT-007。Ch3 需要介于 Ch2（系统模型+信道估计）和 Ch4（自适应载波同步）之间。

当前候选排序：G（BER 闭合解，首选但偏弱）> E（信道跟踪，备选）> B（AMC）/ C（Doppler）（待评估）。

## 方向 B：自适应调制与编码（AMC）

### S001 初筛结论

- 文献量：~80 英文 + ~35 中文（充足）
- 评为 Maybe：系统复杂度高，FPGA 验证难度大
- 未深入精读

### 核心思路

根据湍流强度 $h$ 自适应选择调制阶数（BPSK→QPSK→16QAM）和 FEC 编码率，在保证可靠性的前提下最大化吞吐量。

### 与 Ch4 的衔接

- AMC 需要 BER 估计来决定切换门限 → Ch4 的载波同步质量影响 BER → 反馈
- 或者：AMC 和载波同步共享湍流状态信息 $h$

### 本轮需要评估

1. **复杂度是否可控**：AMC + 载波同步 + FPGA，三章内容是否太多？
2. **与 Ch4 的独立性**：AMC 和 Ch4 的自适应载波同步是否高度耦合导致拆不开？
3. **创新空间**：湍流自适应 AMC 在 FSO 中是否已有成熟方案？我们做什么增量？
4. **MVE 可行性**：2-3 天能否完成最小验证？

### 搜索关键词

英文：
- "adaptive modulation coding FSO turbulence"
- "adaptive rate optical satellite communication"
- "QPSK 16QAM switching free space optical"
- "FEC adaptive coding FSO channel"

中文：
- "自适应调制 激光通信 湍流"
- "自适应编码 自由空间光通信"
- "调制格式切换 星地光通信"

## 方向 C：Doppler 预补偿

### S001 初筛结论

- 文献量：~30-40 英文 + ~1 中文（英文充足，中文极少）
- 评为 Maybe：与 Ch4 可能有大量重叠
- 核心风险：载波同步本身包含频偏处理，独立成章可能内容不够

### 核心思路

LEO 卫星运动引入 ±8 GHz 多普勒频偏。Ch3 研究星历预补偿方案（发射端预补偿），将残余频偏降到 FFT-FOE 可处理范围。Ch4 在残余频偏基础上做精细载波同步。

### 与 Ch4 的衔接

- Ch3 粗补偿（发射端预补偿，将 ±8GHz → ±几MHz）
- Ch4 精同步（接收端数字处理，FFT-FOE + DPLL + VV-CPR）
- 形成两级载波恢复链

### 本轮需要评估

1. **重叠风险**：Doppler 预补偿和 Ch4 载波同步的边界在哪？能否清晰拆分？
2. **独立性**：预补偿是否内容足够支撑完整一章？还是只能做几页？
3. **文献支撑**：中文文献极少是否影响答辩引用？
4. **已有基础**：Fernandes 2023（已精读）和 Zhao 2025（已精读）覆盖了多少？

### 搜索关键词

英文：
- "Doppler pre-compensation LEO satellite optical"
- "ephemeris Doppler compensation coherent FSO"
- "satellite optical link frequency offset correction"

中文：
- "多普勒预补偿 星地激光"
- "星历 频偏补偿 相干光通信"

## 继续找新方向

除 B/C 外，主动搜索是否还有 S001 未覆盖的方向。可能的启发：

1. **波前校正/自适应光学（数字域）**——数字信号处理替代 AO 硬件
2. **空间分集合并**——多接收孔径的信号合并策略
3. **编码协同**——FEC 编码与信道估计/同步的联合设计
4. **指向误差补偿**——卫星振动导致的波束偏移补偿
5. **任何你能发现的、与 Ch2+Ch4 相关的新方向**

对每个新发现的方向，快速评估（5 分钟级别）：
- 文献量是否 ≥20 篇
- 与 Ch2/Ch4 的相关性
- 硕士论文可行性
- 如果看起来有潜力，停下来做 3-5 篇精读

## 执行方法

1. **B 深入**：检索 → 精读 3-5 篇核心论文 → Go/No-Go 判断
2. **C 深入**：检索 → 精读 3-5 篇核心论文 → Go/No-Go 判断
3. **新方向搜索**：3-5 组额外关键词 → 如果发现高潜力方向，深入评估
4. **产出排序表**：G / E / B / C / 新方向的最终排序

## 搜索工具

```bash
cd /mnt/d/code/study/research-protocol && bash tools/search "keyword" --limit 20
cd /mnt/d/code/study/research-protocol && bash tools/blit --source cnki "关键词" --doc-type master
```

## 输出

写入 `.sessions/2026-05-30-ch3-direction-exploration/` 目录：
- `R003-direction-bc-deep-analysis.md` — B 和 C 的深入评估
- 如果发现新方向：追加到同一文件
- 最终排序推荐表

## 必读文件

1. `.sessions/2026-05-30-ch3-direction-exploration/S001-candidate-search.md` — 6 方向初筛
2. `.sessions/2026-05-30-ch3-direction-exploration/topic-index.md` — 专题状态
3. `毕设/写作材料/formulas-ch3ch4-sync.md` — Ch4 公式（了解衔接点）
4. `papers/doi/10.1109_jlt.2023.3281082/content.md` — Fernandes 2023（C 方向参考）
5. `毕设/写作材料/thesis-framework.md` — 论文框架（了解 Ch4 内容）

## 验证环境

```bash
~/.venvs/torch/bin/python
```
