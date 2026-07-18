# [S039] residual cascade Step 4a 前置门控结论

> 2026-07-16 | GW Step 4a 前置 §0 | 状态：PIVOT（不进入 A0/MVE）

## 目标

依据 S038 的 5 篇全文精读结果，检查 Q14 是否满足 gw-feasibility Step 4a §0 的合法问题与四判据门控。

## 记录

- Step 2 质量门：PASS（5/5 可读全文；其中 L02 的转换文本带 arXiv HTML 链接污染，但 DOI 标题/摘要与正文一致，作为同一篇 JLT 2021 论文，不重复计数）。
- Step 3：PASS（5/5 精读完成；没有发现 `standard-CMA always-online + additive NN residual` 的直接先例）。
- Q14 已登记到 `projects/thesis-fso/literature_notes.md`，但四判据第 2 条为 UNKNOWN：L01 只证明 online VAE 可替代 CMA，L04 只证明监督 residual target 的邻近形式，L05 只提供 CMA/FSO 压力条件；没有证据证明 additive residual 在当前 GG+SOP/线性模型中产生稳定信息增量。
- 按 `stages/gw-feasibility.md` §0：四判据任一非全过都**不得进入 A0 §1–§6**。因此本轮不做性能间隙、竞争维度、结构优势或 MVE 推算，不运行仿真。
- 这是 Pivot/DEFER，不是“方法已失败”：候选问题结构仍可修复，但必须先补一个能把 UNKNOWN 变成 PASS 的证据/问题重写（例如明确当前模型中 CMA 的具体失效 A，并证明简单 DSP 不能覆盖；或把残差路线改为有 pilot/CSI 锚定的在线校正问题）。

## 当前判定

**PIVOT（Step 4a §0 卡住）**。依据 D042，主控可自主选择下一条软件 DSP 路线；依据 D043，不回退到严格 e2cnn/等变固定标签路线。当前没有 MVE 授权。

## 后续

下一轮应从已有文献资产中选一个能通过四判据的候选，重新走 Step 1→2→3；优先检查“有明确传统 baseline 失效数字 + 方法产出形态属于 DSP 算法而非单纯替换网络”的候选。残差 cascade 保留为 DEFER，不删除已有证据。

## 决策引用

- D042：主控在软件 DSP/ML 范围内可自主排名、停止、切换。
- D043：严格 equivariance/e2cnn 不作为固定标签解。

## 范围确认

- 本轮是否在 scope boundary 内：是。
