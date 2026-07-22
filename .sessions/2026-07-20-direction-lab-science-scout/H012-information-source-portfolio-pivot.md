# Handoff: 从盲专家路由退到信息来源候选族批量 Probe

> 来源: S011 / D017 / D018 / D019 / V006 / V007 | 独立终验: V008 PASS | 交接目标: 恢复可信当前态，批量比较新增信息来源，再选择方法 Scout
> 日期: 2026-07-22

## 到哪了（状态）

e15ae60 的“五轴穷尽/信道本质属性”已由 D017 invalidated；S011 用合法、能力对齐的 CMA/MMA/DD-LMS 和 fresh seeds 121–130 重测混合路由。D018 裁决 C：per-realization oracle selector 的 macro PI-SER headroom 仅 **0.003693**，低于预注册实用阈值 **0.03**，所以未训练 router。本具体盲专家路由合同已关闭，但这只证明同类 blind experts 的失败相关，不证明新增模型、pilot、历史或 decoder 信息无价值。

H011 把 model-based tracker 写成近似唯一后续，仍然过早收窄。D019 改为先做开放的信息来源 headroom map：物理模型先验、稀疏/自适应 pilot、因果多 block 历史、decoder/CRC/soft feedback。先比较信息价值与可观测性，再决定实现哪种算法。

本交接前还修复了“报告称已同步、实际 current views 不一致”的问题：portfolio 的 C04/C09/C12/C14/C15 状态已按 D017 收窄；state 不再停留在已完成的 Macro A；harvest/current.yaml 从无法解析的伪 current view 改为合法 YAML，并加入 D018 当前负面结果。

## 下一步干什么

第一件事：按接收方验证清单核验 H012 与四个 current views。随后在同一 SCIENCE_SCOUT scope 内建立一个**信息来源候选族矩阵**，不是模型名表。对四类来源分别回答：合法信息是什么、最强 scoring-only/oracle headroom 多大、receiver 是否可观测、传统 comparator 是什么、物理可用门限是什么、共享基础设施与文献撞车风险如何。

先并行做最轻量的语义/headroom Probe；不得直接花一天实现 EKF/PF，也不得一次搭完 pilot、coded chain 和 tracker。Probe 结束后统一排序：只有满足“问题仍存在 + 合法信息有实用 headroom + receiver 可观测 + 基础设施可控”的信息族才进入 Scout。局部失败自动轮转到下一信息族，不逐个请求用户。

## 纪律（和下一步直接相关）

- 不复活 CMA/MMA/DD-LMS router；D018 的 oracle Kill 已经充分。
- 不把 model-based tracker 称为唯一剩余方向；portfolio 明确保持开放、不声称完备。
- 候选按“新增信息来源 × 作用点 × 输出动作”组织，不按 EKF/GRU/Transformer 等模型名拆假方向。
- oracle 只作 Kill/headroom bound；Go 必须赢正确、广泛使用、任务适配且公平的传统 comparator。
- 物理“可用”门限必须来自高质量文献/标准或明确系统合同；MDE 不是通信可用门限。
- 先共享 Probe，后建设施；完整实现前先过常数解、信息泄漏、因果前缀、身份和公平调参 smoke。
- 负面、blocked 和 invalid 分开；blocked 轴不得记成候选失败。

## Dead Ends / 失败数据附录

### 合法 FIR 盲专家路由

- 核心失败机制：CMA、MMA、cold-start DD-LMS 在当前 slice 上失败高度相关，没有可路由的专家多样性。
- 具体数据：110 realizations；CMA=0.3972、MMA=0.5031、DD-LMS=0.4319；all3 oracle selector=0.3935；headroom=0.003693；阈值=0.03。
- 已排除方向：继续换 router、增加 router 模型、增加相同合同 seeds、把 C16 task-mismatched HOS 当 fallback。
- 可复用部分：oracle complementarity 测试范式、DD-LMS identity tests、失败分类法、D017 task-mismatch 教训。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| C04/C09 目标无合法语义 | 目标不能有输入无关退化解 | UNRESOLVED | 仅在正确目标有独立 headroom 时重启 |
| C12 GMI/LLR 合同无真上界 | metric/oracle 必须回答同一任务 | UNRESOLVED | decoder/soft 信息族进入 Scout 前 |
| C15 不公平步长 | 相当调参机会而非相同 μ | UNRESOLVED | cost-family 再进入候选批前 |
| 当前无 FEC chain | 不得把 MDE 当通信可用门限 | INFRASTRUCTURE_BLOCKED | decoder/soft 族通过前置 headroom Probe 后 |
| 专题已有 11 个 S 文件 | ≥15 必须 scope review | inflation warning | 再新增 4 个 S 前必须拆阶段或变更范围 |

## 必读（不超过 8 个）

1. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`
2. 本文件 `H012-information-source-portfolio-pivot.md`
3. `projects/thesis-fso/direction-lab/STATUS.v1.md`
4. `projects/thesis-fso/direction-lab/state/current.yaml`
5. `projects/thesis-fso/direction-lab/portfolio/current.yaml`
6. `projects/thesis-fso/direction-lab/harvest/current.yaml`
7. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 D017–D019
8. `projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/hybrid-routing-scout-v1/synthesis.v1.md`

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落。
- [ ] 已验证至少 3 条关键事实：
  - headroom `0.003693` 与阈值 `0.03` → 从 hybrid result/synthesis 重算；
  - seeds 121–130 与旧 confirmatory sets 不重叠 → 查 contract/result；
  - `harvest/current.yaml`、`state/current.yaml`、`portfolio/current.yaml` 均可被 YAML parser 读取。
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with。
- [ ] 已确认 current portfolio 不再把 C04/C09/C12/C14/C15 写成 family closure。
- [ ] 已确认当前范围不含 formal promotion、push、protected history 改动。

## git 状态

- worktree: `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`
- branch: `codex/direction-lab-capability-atlas`
- 科学结果 commit: `782a55f`
- H012/current-view 收口位于 `782a55f` 的直接后继提交；接收时以 `git log -2` 核验实际 SHA。
- 未 push、未 merge。
