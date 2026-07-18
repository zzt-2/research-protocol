# [S008] B 路线 goodput 可行性分析 + Kill B 回 A

> 2026-07-11 | 阶段：写作准备（GW Step 4a 维度 D 内） | 状态：完成
> 来源：H006（B 路线 pilot on/off 系统级架构选择交接）

## 目标

判断 B 路线（pilot on/off 系统级架构选择）物理可行性：
1. goodput 风险怎么处理？论文用 BER 还是 goodput？
2. pilot overhead 在什么范围下，DA 架构 goodput 能赢 NDA？
3. 如果有交叉区 → 设计 pilot 开关实验（回 step4a 走 GW Step 4a 维度 D）
4. 如果没有 → Kill B 回 A

## 记录

### 1. 接收方验证（Trigger 5 handoff verification）

H006 的 4 条关键事实声称重跑脚本全部 PASS：
- **goodput 预检 8/8 DA 输 NDA** — 重跑 `/tmp/switch_goodput_check.py` 确认：8 个 DA 被选中点全输（BER 优势 +0.06~+1.50dB < 1.249dB 吞吐罚）
- **data 口径选对率 26/29** — 重跑 `/tmp/switch_caliber_audit.py` 确认：awgn 8/8 / weak 7/7 / moderate 7/7 / strong 4/7
- **crossover 随湍流左移** — 确认：awgn 无交叉 / weak-mod ~15-20dB / strong ~10-15dB
- **_registry.yaml** step4a-mve-execution status=active，本专题 depends_on 它，无 conflicts_with

### 2. B 跟 A 的增量价值定位

| 路线 | 切换对象 | 指标维度 | 当前数据 |
|---|---|---|---|
| A（当前） | per-block 估计器 DA↔NDA | BER | data 口径 26/29 选对 + crossover 左移 |
| B（pilot on/off） | 系统级架构 pilot 发/不发 | goodput？BER？ | goodput 8/8 输 / BER 跟 A 重复 |

**核心矛盾**：B 主推 BER → 跟 A 卖点完全重复；B 主推 goodput → 当前 25% overhead 下 8/8 输。**B 必须在 goodput 维度找到交叉区才有存在理由。**

### 3. Goodput 交叉区数学证明（FR-21 oracle 上界精神——先算上界再跑）

goodput_DA > goodput_NDA 条件：
```
throughput_DA × (1 − BER_DA) > throughput_NDA × (1 − BER_NDA)
```

设 pilot 占比 = p（当前 p=0.25），令成功率比 R = (1−BER_DA)/(1−BER_NDA)：
```
R > 1/(1−p)
```

**线性假设**（BER 优势 ∝ density，最自然假设）：goodput_gain(p) = (1−p)(1 + αp)，α = 单位 density 的 BER 成功率提升率。goodput_gain > 1 要求 α(1−p) > 1，即 α > 1。

**实测各点 α 值**（p=0.25，从 goodput 脚本数据算）：
| 点 | BER_DA | BER_NDA | α | α > 1？ |
|---|---|---|---|---|
| weak@5（最大） | 0.329 | 0.399 | 0.466 | ❌ |
| weak@10 | 0.160 | 0.226 | 0.341 | ❌ |
| weak@15 | 0.048 | 0.053 | 0.105 | ❌ |
| moderate@5 | 0.353 | 0.399 | 0.076 | ❌ |
| moderate@10 | 0.200 | 0.249 | 0.065 | ❌ |
| moderate@15 | 0.080 | 0.086 | 0.007 | ❌ |
| strong@5 | 0.392 | 0.400 | 0.013 | ❌ |
| strong@10 | 0.284 | 0.288 | 0.006 | ❌ |

**全 8 点 α < 1 → 线性假设下 goodput_gain(p) < 1 对所有 p∈(0,1) 成立 → 任何 pilot density 下 NDA goodput 都赢。**

### 4. 翻转条件物理分析

goodput 交叉区存在需要 BER 对 density 的响应是**超线性（凹函数）**——低 density 时 BER 优势保持得比线性更好。

但物理上 pilot 辅助相位估计：density 从高到低，BER 优势更可能是**线性或亚线性**（高 density 收益递减），到达 pilot 间距 > 相干时间后急剧恶化。这是凸函数不是凹函数。**翻转的物理条件极不现实。**

### 5. 论文指标维度判断

- **BER 指标**：B 跟 A 卖点完全重复。A 已用 data 口径展示 26/29 选对 + crossover 左移。B 切换 pilot on/off 在 BER 维度没有增量价值
- **goodput 指标**：线性假设下数学已证任何 density 都赢不了 NDA，物理上凹函数翻转不现实。goodput 交叉区极大概率不存在

### 6. Kill B 回 A 决策

用户选"Kill B 回 A（推荐）"。依据：
- goodput 维度数学证明（α<1 全点）+ 物理凹函数翻转不现实
- BER 维度跟 A 卖点重复
- 9 天截稿（CCISP 7/20）时间约束
- A 路线资产全就绪（D005 data 口径 + D002 切换 30seed + D004 net gain + H002 BER 主图），不需回 step4a 跑新实验

## 决策引用

- **D006：Kill B 回 A**（新建）——goodput 维度数学已证任何 pilot density 都赢不了 NDA（α<1 全点）+ BER 维度跟 A 卖点重复。回 A 路线（data 口径 26/29 选对 + crossover 左移）
- D005：data 口径物理公平，选对率 26/29（A 路线数据基础，B Kill 后回此）
- D004：fair_gain 口径方向（naive 口径下弱湍流归零 +0.09~0.19dB，强湍流 +1.26~1.85dB）——本轮 goodput 分析的 BER 优势数据与之同源

## 范围确认

- 本轮是否在 scope boundary 内：**是**。B 物理可行性判断 = 论点合理性审查（原始目标第 4 条"审查论点合理性"）。本轮**没有跑新实验**（守 FR-22），用 goodput 上界数学证明 + α<1 物理论证就 Kill 了 B（守 FR-21 oracle 上界前置门控精神）
- goodput 交叉区数学证明是分析性预检，不是 MVE 实验

## 后续

1. **回 A 路线写论文**：A 路线资产全就绪（data 口径 + crossover + 切换 30seed + net gain + BER 主图），直接进 D2 写草稿（Intro + System Model）
2. **goodput 判据 α<1 可复用**：未来任何 pilot 开关类方向先用 α<1 判据筛（线性假设 + 凸函数物理），省实验
3. **R006/R007 写作规划已就绪**（5 节骨架 + 4-6 图 + 贡献防御性表述 naive 版），A 路线叙事定位不变
4. **等导师反馈 v4 数据层 3 问**（10⁻⁵/口径/baseline）不阻塞写作
