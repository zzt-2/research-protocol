# GREEN forward test — pragmatic baseline adjudication

> agent: fresh subagent `baseline_green_forward`
> skill state: after baseline-adjudication revision

## Blind prompt

请把自己当作接手正式研究推进的新智能体，必须先读取并使用 `.agents/skills/research-direction-lab/SKILL.md` 及它认为必要的 references。不要修改任何文件、不要运行实验，只根据以下原始事实给出当前证据级别、是否授权进入 ML、下一批怎么规划，以及为什么。事实：一个双偏振 16QAM 接收链使用实现正确的单模 Godard-with-z CMA；11 cells×10 paired seeds 中 10/11 对 nearest-decision 显示 oracle affine headroom≥MDE，最大 0.333；oracle affine 使用一段真实发送符号拟合，只作 scoring-only；blind affine 收益很小且有长窗变差；运行长度 N=512/8192，文献材料提示 CMA 可能需要约 1e5 symbols 收敛；多模 MMA/RDE 是 16QAM 常见传统方法但本轮未实现、未比较；用户明确偏好务实毕业，不要求追逐当前 SOTA，希望一次批量推进而不是每一步询问。请写一页式行动判断，不引用任何预期答案。

## Raw response

## 一页式行动判断

### 事实与证据级别

- 现有结果覆盖 **11 个 cells × 10 组 paired seeds**：其中 **10/11** 个 cell 的 nearest-decision 指标显示 oracle affine headroom ≥ MDE，最大值为 **0.333**。这已经是可重复的局部诊断信号，不是单次偶然结果。
- 但 oracle affine 用真实发送符号拟合，属于 privileged-information、scoring-only 上界。它只能说明“残差中存在可被监督仿射映射利用的结构”，不能说明该结构能够被盲接收机恢复，更不能作为 ML 的 Go comparator。
- blind affine 收益很小且长窗可能变差。目前最多支持“这个具体盲仿射估计器没有稳定利用 oracle 所见结构”，不能上升为“传统方法无效”或“必须使用 ML”。
- 单模 Godard-with-z CMA 虽然实现正确，但“代码正确”不等于“比较器充分”：
  - `N=512/8192` 可能远低于约 `1e5 symbols` 的典型收敛尺度；
  - 单模 CMA 对 16QAM 可能存在任务适配不足，而常见多模 MMA/RDE 尚未比较。

因此，当前证据应标为：

- **有效性**：作为诊断证据有效；
- **裁决状态**：`DIAGNOSTIC`；
- **claim ceiling**：`SLICE`，仅限当前双偏振 16QAM 接收链、11 个 cell、当前长度与评估合同；
- **尚不支持**：候选方法胜出、ML 必要性、方法族结论或领域结论。

### 是否授权进入 ML

**暂不授权进入 ML Scout。**

阻断原因不是需要追赶 SOTA，而是两个低成本、足以推翻当前问题定义的替代解释尚未排除：

1. CMA materially under-converged；
2. 单模 CMA 不是该 16QAM 问题的充分传统比较器。

只有在公平收敛条件下，问题仍然显著存在于任务适配的传统比较器之后，才能登记：

`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`

该状态才授权对 surviving slice 开展有限 ML Scout；它仍不等于授权完整训练工程或宣称 ML 优势。

### 下一批：Baseline Adjudication Shared Batch

一次性冻结并推进整个批次，不在每个实现步骤重新询问。

| 项目 | 批次设计 |
|---|---|
| 核心问题 | oracle 所见 headroom 是欠收敛/比较器不适配造成，还是充分传统基线之后仍存在？ |
| 诊断锚点 | 保留当前单模 CMA 与现有结果，不改写历史 |
| 收敛轴 | 使用 paired seeds，在同一 11-cell slice 上做对数间隔长度覆盖，至少延伸到约 `1e5` symbols；保存收敛曲线，而不只比较终点 |
| 比较器阶梯 | 当前 CMA → 公平收敛 CMA → 一个有文献闭环的 16QAM 常规主比较器（优先裁决 MMA）→ 一个直接处理多模结构的低成本扩展（候选 RDE） |
| 公平性 | 相同输入信息、训练/运行数据、调参预算、cell、seed、评估窗口和指标；真实符号只允许用于 scoring oracle |
| 主要判据 | nearest-decision 指标及 paired uncertainty；oracle affine 继续作为上界/Kill 工具；blind affine 仅作有界负对照 |
| 不纳入 | 当前 SOTA 大搜索、ML 实现、完整论文级 baseline 堆叠 |
| 并行准备 | 可同时整理若问题存活时的 ML 候选卡和统一接口，但门控通过前不运行 ML |

### 预注册退出判据

- **传统比较器或充分收敛消除 MDE 级差距**：把现象归为基线欠收敛或任务适配问题；不进入 ML。
- **差距仅在部分 cells 存活**：登记局部 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`，ML Scout 只覆盖 surviving slice，不外推整个 16QAM 域。
- **差距跨多数 cells 稳定存活，且 paired uncertainty 排除偶然性**：授权下一批 bounded ML Scout。
- **MMA/RDE 无法形成公平实现或来源闭环**：标记该轴 unresolved，不把基础设施阻塞误写成传统方法失败。

### 行动结论

当前最高信息价值的动作不是继续优化 blind affine，也不是直接训练 ML，而是用一个共享批次同时排除“欠收敛”和“比较器不适配”两项主要混杂因素。该路线符合务实毕业目标：不追逐非必要 SOTA，只补足能决定研究问题是否真实存在的最小传统基线阶梯；批次合同冻结后可自动连续推进，仅在需要改变核心场景、显著扩大算力投入或出现多条已证实论文路线时再升级给用户决策。

## Pre-registered scorer output

`PASS`：bounded claim、ML gate、oracle 边界、务实停止、公平传统 baseline 和 Portfolio 并行继续六项全部满足。
