# Task Brief: Ch4 direct APSK equalization 全文缺口闭合

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-front-end-groundwork/step2-direct-apsk-closure.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 3
  action_class: GROUNDWORK_ACQUIRE
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只闭合 T043 的唯一 blocker：从既有 `search-archive/2026-08-30/apsk-front-end-baseline-authority.json` 获取至少一篇“APSK 直接均衡”合格全文。固定顺序：T040-023 `Newton-like minimum entropy equalization algorithm for APSK systems`（OA，DOI `10.1016/j.sigpro.2014.02.003`）优先；若失败，再用 T040-010、T040-037，最后才尝试 T040-003/T040-008/T040-030。使用项目 download/blit/convert 链，逐篇做 title identity、`content.md >= 50` 行和正文质量门。成功一篇即停，不新增搜索 query。

## 边界

- 这是 T043 的 Step 2 bounded repair，不精读方法、不写 Q#、不进入 Step 3。
- 不实现、不实验、不修改 Skill/controller/仿真/论文正文，不修下载器。
- 最多三次候选获取；成功一篇立即收口，全部失败也立即报告，不继续找新方向。
- 只提交新增的 `papers/**`、必要索引更新和指定 closure report；不要改 `.sessions/`。

## 验收

- PASS：至少一篇正式身份、题名一致、有效正文不少于 50 行的 APSK 直接均衡全文。
- 报告必须说明该全文是否覆盖 multi-ring cost/update、APSK constellation assumptions 和 comparator；这里只做可读性定位，不做方法裁决。
- 最终回报 commit、paper identity/path、有效行数和 PASS/BLOCKED。
