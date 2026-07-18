# Handoff: residual cascade Step 4a 前置门控后换路线

> 来源: S039 | 交接目标: 下一对话从新候选 GW Step 1 继续，不跳步
> 文件名: H014-residual-cascade-defer-next-route.md

## 已完成边界

residual cascade 已按 GW Step 1→2→3 完成：R009 检索、S037 获取（5 篇全文）、S038 精读（5/5）。Q14 已登记 `projects/thesis-fso/literature_notes.md`。Step 4a §0 按 S039/D044 判为 PIVOT/DEFER：四判据 1/3/4 PASS，第 2 条 UNKNOWN；未进入 A0 §1–§6，未跑 MVE，未改仿真代码。

## 不要做什么

- 不得把 L01/L04/L05 的邻近证据写成 additive cascade 直接先例。
- 不得跳过新候选的 Step 1→2→3→4a，亦不得先跑 MVE 再补问题合法性。
- 不回退到 D043 已否决的严格 e2cnn/SO(2) fixed-label 路线；F1 电控偏振跟踪和 G2 HARQ 仍不在范围。

## 必读

1. `projects/thesis-fso/master-state.md`（当前 Step 与 GW Progress）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/S039-residual-cascade-step4a-gate.md`
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md`（D042–D044）
5. `stages/groundwork.md`、`stages/gw-feasibility.md`、`stages/gw-acquire.md`、`stages/gw-read.md`

## 接口变更（如有代码改动）

无。

## 失败数据附录（如涉及路线失败）

- 5/5 精读文献均无 `standard-CMA always-online + additive NN residual` 直接先例。
- Q14 判据 2 UNKNOWN：当前 GG+SOP/线性模型内残差信息增量未证实；因此按 §0 阻断 A0/MVE。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| residual cascade 的方法增量未证 | 四判据第 2 条必须 PASS | DEFER，不删除证据 | 新证据证明稳定残差，或新问题重写后四判据全过 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| Step 2 | ≥5 篇可读、去重后全文 | `gw-acquire.md`/S037 | 1/1 |
| Step 3 | 5/5 按 14 字段+7 子表精读 | `gw-read.md`/S038 | 1/1 |
| Step 4a §0 | Q# 四判据全 PASS | `gw-feasibility.md` | 0/1（Q14） |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证至少 3 条关键事实声称（S037 5 篇门、S038 5/5 精读、S039 Q14 判据 2 UNKNOWN）
- [ ] 已检查 `_registry.yaml` 本专题依赖和冲突字段
- [ ] 已确认当前范围未违反“明确不含”（F1/G2）

## 下一轮

从已有资产中重新选择一个可形成完整 Q# 的软件 DSP 候选，优先检查 R007 已提示的“收敛后 SOP 驱动 lock-swap”问题，但必须重新执行 GW Step 1 检索，不能直接沿用 R007 的缺口结论作为 Go 依据。

## 用户关键指令（原话）

> “你直接自己做吧？按流程不跳步，切实地一直跑，自己想怎么能弄出东西？方向不行可以自己决定怎么换”
