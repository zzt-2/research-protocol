# PROMPT-005: Ch3 新章节方向探索（研究协议 Groundwork）

> 用途：新对话中用研究协议 Groundwork 流程探索新的第三章方向
> 前置：H008（了解论文全貌）+ `stages/groundwork.md`（研究协议流程）
> 目标：产出 2-3 个候选方向 + 可行性评估，供用户选择

## 论文背景

硕士论文《星地激光通信信号处理关键技术研究》，QPSK相干检测，Gamma-Gamma大气湍流信道，LEO星地链路。

**导师 2026-05-30 决定**：将原 Ch3（大气湍流信道估计技术）合并到 Ch2，新增一个 Ch3。Ch3 需要"和另外两章相关"，具体方向"开题答辩后再定"。

## 当前章节结构

```
Ch1 绪论
Ch2 星地激光通信系统与信道模型（含信道估计，已合并）
Ch3 ★★★ 新增章，TBD ★★★
Ch4 低轨星地载波同步算法（核心创新：三个湍流自适应公式）
Ch5 接收端信号处理链FPGA设计与实现
Ch6 总结与展望
```

## Ch3 的约束条件

### 硬约束（必须满足）

1. **与 Ch2 和 Ch4 相关**——导师原话："和另外两章相关"
2. **形成递进链**——Ch2 建模 → Ch3 [?] → Ch4 载波同步 → Ch5 FPGA，叙事要通
3. **有文献支撑**——不能是纯空白方向（找不到参考文献）
4. **硕士论文可完成**——不需要突破性创新，"方向对、水平够"即可
5. **与 QPSK 相干检测 + GG 湍流信道兼容**——不能换成 IM/DD 或其他调制

### 软约束（优先满足）

1. 能复用 Ch2 的仿真框架（Python + GG 模型 + 相干检测）
2. 与 Ch4 的载波同步有信息流依赖（Ch3 的输出是 Ch4 的输入，或 Ch3 解决 Ch4 前置问题）
3. 在 FPGA 上可实现（Ch5 能验证）
4. 有量化对比数据支撑创新点（仿真可产出）
5. 不依赖实验硬件（纯仿真可行）

### 排除方向

以下方向已被探索过并有明确结论，**不要重新考虑**：

| 方向 | 结论 | 来源 |
|------|------|------|
| 纯预补偿（$P_{tx} \propto 1/h^2$） | **FAIL**：估计噪声下完全崩溃 | S013 MVE |
| 信道均衡（CMA/DFE） | GG 是 flat fading，QPSK 下均衡无物理依据 | S002 分析 |
| DL 方法主线 | 降为对比实验，不作为主线（D005） | 导师确认 |
| 自适应 CPR 算法切换 | **No-Go**：湍流不是 CPR 切换的合理判据 | R012 |
| GNN/路由/网络层 | **废弃**：导师强制换方向 | S001 |

## 已有的技术积累（可复用）

### 仿真代码

| 代码 | 内容 | 可提取 |
|------|------|--------|
| `projects/thesis-figures/simulation/sim_prototype.py` | GG模型+LS估计+VV载波恢复端到端 | 完整仿真框架 |
| `projects/thesis-figures/simulation/sim_direction_a.py` | 载波同步 MVE，自适应参数 | 自适应算法框架 |
| `projects/thesis-figures/simulation/sim_ch3_precomp.py` | 预补偿 MVE | 预补偿失败数据 |
| `projects/thesis-figures/simulation/sim_cascade_robustness.py` | 级联鲁棒性 | NMSE→BER数据 |

### MVE 关键结论

- **载波同步对估计误差鲁棒**：NMSE≥-10dB 时 6/6 场景 PASS
- **功率预补偿对估计误差脆弱**：任意噪声下全 FAIL
- **三个自适应公式**已推导并验证：$N_\text{opt} \propto h^{-4}$, $M_\text{opt} \propto h^{-2/5}$, $B_\text{L,opt} \propto h^1$
- **DPLL 带宽自适应是最大增益来源**：88 Mrad/s vs 固定 8 Mrad/s

### 公式和参数

- `毕设/写作材料/formulas-ch2-system-model.md` — 36 条公式
- `毕设/写作材料/formulas-ch3ch4-sync.md` — 28 条公式
- `毕设/写作材料/symbol-conventions.md` — ~100 符号

## 可能的候选方向（需验证）

以下方向**仅为启发**，不是限定。Groundwork 的核心工作是验证这些方向（或发现更好的方向）的可行性和文献支撑。

### 候选 A：湍流信道估计精度需求与级联优化

**思路**：Ch2 已合并了信道估计方法对比，Ch3 可以深入"估计精度对下游的级联影响"。虽然预补偿失败了，但载波同步的鲁棒性分析本身就是贡献。

**与 Ch4 的衔接**：Ch3 给出"估计精度需要达到多少才够"的定量指导 → Ch4 按此设计自适应参数

**风险**：导师说 Ch3 估计已合并到 Ch2，再做估计可能重复

### 候选 B：大气湍流下的自适应调制与编码（AMC）

**思路**：根据湍流强度 $h$ 自适应选择调制阶数（QPSK→16QAM→BPSK）和编码率。与 Ch4 的载波同步共享湍流状态信息。

**与 Ch4 的衔接**：Ch3 的自适应调制需要载波同步质量反馈 → Ch4 提供载波同步

**风险**：系统复杂度高，FPGA 验证难度大

### 候选 C：星地链路 Doppler 预补偿与残余频偏处理

**思路**：LEO 卫星运动引入 ±8 GHz 多普勒频偏。Ch3 研究星历预补偿方案，将残余频偏降到 FFT-FOE 可处理范围。Ch4 在残余频偏基础上做精细载波同步。

**与 Ch4 的衔接**：Ch3 粗补偿 → Ch4 精同步，形成两级载波恢复链

**风险**：与 Ch4 可能有大量重叠（载波同步本身包含频偏处理）

### 候选 D：湍流信道下的信号检测与判决反馈

**思路**：研究湍流导致的幅度闪烁对信号检测的影响，设计自适应门限或判决辅助方案。

**与 Ch4 的衔接**：检测是同步之后、判决之前的环节

**风险**：QPSK 硬判决本身简单，创新空间有限

### 候选 E：其他你发现的方向

Groundwork 检索过程中如果发现更好的方向，直接提出。不局限于上面四个。

## 执行方法：研究协议 Groundwork

**必须先读** `stages/groundwork.md`，按流程执行。核心步骤：

1. **Step 1-2：问题定义 + 检索**
   - 对每个候选方向，用 `tools/search`（英文6源）+ `tools/blit --source cnki`（中文）检索
   - 每个方向 ≥5 组关键词，评估文献量和空白真实性
   - 特别注意：空白是"真空白"（没人做）还是"假空白"（不值得做）

2. **Step 3：精读**
   - 每个方向精读 3-5 篇核心论文
   - 提取：方法、结论、局限性、与我们的关系

3. **Step 4：可行性评估**
   - 按 `stages/gw-feasibility.md` 评估每个方向
   - 特别关注 FR-01~FR-08 可行性防坑规则

4. **Step 6：MVE（最小可行实验）**
   - 对最有前景的方向，快速仿真验证核心假设
   - Python 环境：`~/.venvs/torch/bin/python`
   - 可以复用 sim_prototype.py 的框架

5. **输出**：候选方向排序表 + 每个方向的 Go/No-Go 建议

## 搜索工具

从项目根目录调用：
```bash
cd /mnt/d/code/study/research-protocol && bash tools/search "keyword" --limit 20
cd /mnt/d/code/study/research-protocol && bash tools/blit --source cnki "关键词" --doc-type master
```

## 输出

写入 `projects/thesis-ch3-exploration/` 目录（如不存在则创建）：
- `master-state.md` — 探索状态
- `literature_notes.md` — 每个候选方向的文献笔记
- `feasibility_report.md` — 可行性评估报告

## 必读文件

1. **本文件** — Ch3 探索的完整上下文
2. `stages/groundwork.md` — 研究协议 Groundwork 流程
3. `stages/gw-feasibility.md` — 可行性评估流程和防坑规则
4. `.sessions/thesis-direction-pivot/H008-literature-deep-reading-handoff.md` — 论文全貌（可选，了解更深层上下文）
5. `projects/thesis-figures/simulation/sim_prototype.py` — 已有仿真框架（MVE 复用）

## 时间预期

这是多轮对话的任务：
- 第 1 轮：候选方向检索 + 初步筛选（Go/No-Go 初判）
- 第 2 轮：精读 + 可行性评估 + MVE
- 第 3 轮：确认方向 + 输出推荐

每轮结束时写 handoff，下轮续接。
