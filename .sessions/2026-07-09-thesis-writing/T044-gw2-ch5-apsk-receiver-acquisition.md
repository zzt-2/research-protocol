# Task Brief: Ch5 APSK soft receiver 候选全文获取与覆盖门

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step2-coverage-report.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 2
  action_class: GROUNDWORK_ACQUIRE
  mission_checkpoint: CP002
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

严格执行 GW Step 2，为首选 C5-1 APSK structured-covariance demapper 和后备 C5-2 decoder rescue 获取全文。优先 Layton 2018 full-covariance demapper、Zhang/Kim 2013 APSK scaling、APSK BICM-ID/iterative demapping、syndrome bit-flipping、trapping-set post-processing、OSD、adaptive NOMS、Chen–Fossorier reduced-complexity decoding；从 T040/T041 JSON 选 8–12 篇，允许用同机制可获取替代，不扩成新方向。按项目工具三轮止损，核验全文质量并出覆盖报告。

## 边界

- 只做 Step 2；C5-1 是当前首选，C5-2 只保证后备文献覆盖，不因下载到论文就开放接口实现。
- 不精读、不写 Q#、不做 Step 3/3.5/4a，不实现、不实验。
- 不改仿真/Skill/controller/论文正文，不网页抓全文。
- 只提交本任务新增或规范更新的 `papers/**`、`papers/index.json`（若工具确有更新）和指定 coverage report；不要改 `.sessions/`。

## 验收

- ≥5 篇 qualified full text。
- C5-1 必须覆盖 isotropic/scalar 与 full covariance 或 data-dependent demapping；C5-2 后备至少覆盖 NOMS 和一种 rescue/OSD/BF。
- 单列 exact-recipe collision、decoder-interface debt 与付费墙缺口，不能把摘要当公式证据。
- 最终回报 commit、qualified/failed 数、coverage verdict 和阻塞 Step 3 的唯一缺口。
