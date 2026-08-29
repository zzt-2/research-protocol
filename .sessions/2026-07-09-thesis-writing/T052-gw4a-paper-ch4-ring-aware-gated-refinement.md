# Task Brief: Ch4 Q-C4-2 GW Step 4a paper feasibility

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-front-end-groundwork/step4a-paper-feasibility.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 6
  action_class: GROUNDWORK_FEASIBILITY_PAPER
  mission_checkpoint: CP006
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 `Q-C4-2` 只执行 `stages/gw-feasibility.md` Step 4a 的纸面部分：A0 §0–§6、A'、A、B。不得进入维度 D/MVE。研究对象固定为：有限 pilot 的 2×2 LS 初始化 + 已知 `(8,8)-16APSK` ring identity + payload receiver residual/decision distance → 对 RDE/均衡更新逐样本 reliability gate/weight → semi-blind refined 2×2 demultiplexer。

## 必读输入

1. `projects/thesis-fso/literature_notes_apsk_front_end.md` 的 Q-C4-2、comparator 与统计设计段。
2. `projects/thesis-fso/apsk-front-end-groundwork/step3-5-supplement-report.md`。
3. `projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md`。
4. `papers/_read_notes/10.1109_icassp.1990.115806.md`、`papers/_read_notes/10.1109_jlt.2009.2021961.md`、`papers/_read_notes/10.1186_1687-1499-2012-317.md`；只在需要核机制时读对应本地 fulltext。

## 必答判断

1. A0 §0：Q-C4-2 的 M/C/A 与四判据是否仍成立；不得把“没有 exact collision”当问题存在，也不得把 PS-QAM 场景差异本身当贡献。
2. A0 §1–§6：plain RDE 与 DD-LMS/RLS 在错环/错判样本下的可测更新污染、pilot-only LS 的残余、receiver-visible 信息、最强廉价替代与 failure modes。
3. A'：主竞争维度拆为 BER/FER、收敛/失锁或错误更新率、pilot/update budget 与复杂度；明确哪些指标能承重，哪些只能解释机制。
4. A：写出 reliability gate/weight 改变 2×2 update 的可证伪机制与最小 oracle/headroom 计划，但本轮不计算数字。
5. B：把外部 novelty 与科学 feasibility 分开；Di Rosa–Richter 2021、FEC-SoftRDE、MAPSK outer-ring CMA 只限制 claim，不自动 Kill。
6. 冻结 Step 4a-D 前的 candidate recipe v1、公平 comparator、receiver-visible firewall、最小消融、预期方向与 pre-MVE Kill/Pivot 条件。

## 务实约束

- candidate v1 应尽量简单。若 hard accept/reject gate 已足以形成完整方法动作链，不得为了“看起来复杂”强行叠加学习器或多层权重；smooth weight 只能是同族变体。
- 主 comparator 至少包含同 2×2 LS 初值的 tuned plain RDE，以及同 pilot/更新/调参预算的 tuned DD-LMS/RLS。CMA/MMA 只作 canonical reference，不得作唯一主 baseline。
- Di Rosa–Richter 2021 的全文缺口必须明确保留；不得用摘要脑补其 LS 初始化、公式或 butterfly 细节。
- 廉价替代若吸收增益，优先把方法身份收缩到更简单且诚实的 gate recipe，而不是把整章自动判死；只有 receiver-visible gate 对正确 baseline 没有可测 headroom，才 `KILL_BEFORE_MVE`。

## 证据与边界

- 只使用现有 T048/T050、本地 read notes/fulltext 与平台 authority；不检索、不下载。
- 不实现、不运行代码/仿真，不修改 Skill/controller/论文正文或正式 feasibility terminal。
- 不作 Go/Conditional Go；只给 `PAPER_DIMENSIONS_PASS / PIVOT / KILL_BEFORE_MVE` 与唯一 blocker。若纸面通过，主控后续另行授权维度 D。
- 只提交唯一 paper-feasibility report；最终回报 commit、A0/A'/A/B verdict、candidate v1、strongest cheap alternative、唯一 blocker。
