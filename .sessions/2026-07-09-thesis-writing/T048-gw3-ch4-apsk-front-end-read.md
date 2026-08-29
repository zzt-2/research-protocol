# Task Brief: Ch4 APSK front-end GW Step 3 结构化精读

> 来源: S028 | 产出位置: `projects/thesis-fso/literature_notes_apsk_front_end.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 4
  action_class: GROUNDWORK_READ
  mission_checkpoint: CP004
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行 GW Step 3，完整精读以下 7 篇已有全文，同时判定两个不同 research object：C4-2 ring-aware pilot-initialized semi-blind refinement 与 C4-1 scaled-unitary pilot-LS。

1. `papers/doi/10.1109_tcom.1980.1094608/content.md` — CMA canonical。
2. `papers/doi/10.1109_jsac.2002.1007381/content.md` — MMA canonical。
3. `papers/doi/10.1109_icassp.1990.115806/content.md` — RDE canonical。
4. `papers/doi/10.1109_jlt.2009.2021961/content.md` — coherent CMA/RLS-CMA/RDE comparator。
5. `papers/doi/10.1186_1687-1499-2012-317/content.md` — direct APSK DFE/LMS use。
6. `papers/doi/10.1587_elex.8.1642/content.md` — coherent Jones/DSP boundary。
7. `papers/doi/10.1109_jlt.2009.2035526/content.md` — unitary/PDL/ML boundary。

## gw-read 强制清单

- 每篇 title 自检；使用 14+ 独立字段、7 个结构化子表，传统 DSP 的 MDP/网络字段写 `N/A（原因）`。
- 每篇生成 `papers/_read_notes/{paper_id}.md` 并向 `projects/thesis-fso/read-log.md` 追加记录。
- 至少 4 篇做实验完备性提取，至少 2 篇做写作架构提取；综合分析必须形成 Q-C4-2、Q-C4-1 两行 M/C/A+四判据。
- 强经典方法只限制 claim ceiling，不因通用原子/更强邻居自动 Kill；只有完整 receiver-visible input-action-output recipe 完全相同，或目标条件下根本无问题，才关闭 Q#。

## 两个 Q# 必答

### Q-C4-2

- baseline M：同 pilot/初值/可靠度/更新预算的 LS-only + tuned DD-LMS/RLS，以及同 LS 初值 tuned RDE。
- target C：DP-(8,8)-16APSK、memoryless 2×2 Jones、有限 pilot、payload 期间只见 decision distance/ring identity/receiver residual。
- 检查经典 CMA/MMA/RDE、coherent blind→DD 与 direct APSK DFE 是否已完整覆盖“pilot-initialized + ring-aware reliability-gated refinement”；若未完整覆盖，准确写出差别和最强 comparator。

### Q-C4-1

- baseline M：unconstrained complex 2×2 pilot-LS、ridge/Tikhonov LS、singular-value floor。
- target C：scaled-unitary/near-equal singular values 的 memoryless Jones channel、短 pilot budget。
- 检查 unitary polar projection/Procrustes 是否只是已知原子；即使原子已知，也判断 DP-APSK FSO 场景迁移、pilot budget 与 bounded claim 是否形成完整 recipe 差别。必须列出 near-unitary 前提失效时的 claim ceiling。

## 边界与验收

- 不检索/下载，不做 Step 3.5/4a，不实现、不实验、不改仿真/Skill/controller/论文正文。
- 只提交 dedicated literature note、7 篇 read notes、read-log 追加。
- ≥5 篇合格精读且至少一条 Q# 四判据全过才 PASS；最终回报 commit、read count、两个 Q# verdict、优先进入 Step 3.5 的唯一对象和 blocker。
