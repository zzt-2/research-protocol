# Task Brief: 闭合 C4-1 scaled-unitary pilot-LS 的 exact recipe

> 来源: S028 / D047 / T040 / T043 / T045 / T048 | 产出位置: `projects/thesis-fso/polarization-demux-groundwork/`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 9
  action_class: GW_STEP3_5_EXACT_RECIPE_CLOSURE
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

为 C4-1 完成候选专属 Groundwork Step 3.5。候选 recipe 固定为：receiver-known 双偏振短 pilots → unconstrained 2×2 pilot-LS → SVD → 两个奇异值取均值得到 scaled-unitary projection → 逆矩阵解复用 payload，并输出 receiver-visible singular-value ratio/applicability 标志。只回答完整 recipe 是否在目标 DP-(8,8)-16APSK 星地相干接收场景发生完全碰撞，以及 claim ceiling；不实现、不仿真、不进入 Step 4a。

## 启动门与必读

1. 先运行 task-control validator；完整读取 `stages/gw-supplement.md`（或 Step 3.5 当前 owner）、`stages/groundwork.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md`、`thesis-lessons.md` TL-31–33、T040/T043/T045/T048 产物与 D031/D032/D047。
2. 必须使用项目 `tools/search` / citation-chain 工具；全文精读与 web 信息消化按 AGENTS.md 委托子 agent。不得由主线程 WebSearch。
3. 三轮 bounded closure：exact-action queries → Roudas/Kikuchi/Procrustes 前后向引用链 → 用新术语做一次 reprise。Round 3 新增 MUST/SHOULD=`0/0` 即停止；最多新增 4 篇真正改变 exact-recipe ledger 的高价值全文。

## Exact-recipe ledger

逐篇冻结并核对九字段：

`known pilots | balanced Xp | unconstrained LS first | scaled polar | gain estimator | direct constrained objective | receiver-visible applicability/fallback | 2×2 demux output | DP-APSK/FSO target scene`

必须正面处理：

1. 在 `XpXpᴴ=cI` 时，LS 后 scaled-polar 与直接 constrained scaled-unitary LS 是否代数等价；给出推导或权威指针，不回避。
2. 历史 Pilot-Jones 资产的 B1 unconstrained LS+EMA、B2 Tikhonov、保留双奇异值的 full-SVD floor 均不是本候选 action；只作 comparator/negative prior，旧 verdict 不迁移。
3. polar/Procrustes、unitary Jones estimation 或 direct constrained estimator 属经典原子时，按 D031/D032 只降低 identity 为“经典结构估计向短 pilot DP-APSK FSO 的 bounded migration”，不自动 Kill。
4. 只有已发表方案在算法步骤、receiver-visible 输入输出、目标场景与关键配置上构成完整 recipe 碰撞，才给 `COMPLETE_RECIPE_COLLISION`。

## 裁决与交付

唯一允许的 terminal：

- `SURVIVES_AS_CLASSICAL_MIGRATION`：没有完整 target-scene recipe 碰撞；明确不得声称发明 polar/Procrustes、首次 unitary Jones estimation、SOTA 或适用于 PDL/PMD/FIR。
- `COMPLETE_RECIPE_COLLISION`：九字段完整碰撞；列出可核查证据。
- `EVIDENCE_BLOCKED`：三轮后关键全文不可得，不能诚实裁决；不得伪装成 collision。

报告必须含 query/coverage receipt、全文身份/来源、九字段 ledger、balanced-pilot 等价结论、最强邻居/廉价 comparator、可用 claim 句和下一步。若 survives，下一步仅为候选级 Step 4a A0/A′/A/B；禁止实现、仿真、任务外候选和正式论文正文。一次 commit、不 push。
