# Task Brief: Ch5 structured covariance demapper GW Step 3.5 closure

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step3-5-supplement-report.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 4
  action_class: TARGETED_SUPPLEMENT_SEARCH
  mission_checkpoint: CP004
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

只对 T046 的 Q-C5-1 做 mandatory Step 3.5 exact-recipe closure。目标 recipe 固定为：已知 APSK ring/angle + 当前/过去 pilot residual → radial/tangential covariance parameterization → 跨同环点/跨偏振统计强度的 shrinkage pooling → positive-definite structured covariance → Mahalanobis/log-det bit LLR。主 comparator 是同 pilot/sample/update budget 的 isotropic scalar、per-ring scalar、Layton unstructured per-point full covariance。

## 查询与引用链

- 预注册 query matrix 最多 6 个：`APSK radial tangential covariance demapper`、`polar coordinate Gaussian APSK soft demapping`、`pilot aided structured covariance shrinkage demodulation`、`small sample covariance regularized soft demapper`、`ring aware covariance LLR APSK`、`dual polarization APSK covariance pooling`。
- 以 Layton 2018 DOI `10.1186/s13638-018-1136-z` 做双向 citation-chain；只筛与 estimator input/action/output 直接相关者。
- 最多三轮：Round 1 query，Round 2 citation/alias，Round 3 只闭合剩余 exact-action debt；某轮 new MUST/SHOULD=0 即收敛。
- 使用项目 `tools/search`、citations 和合规 download/convert；全文只获取可能 exact collision 的少量对象。不得原始 WebSearch、不得扩成新方向。

## 裁决标准

- `EXACT_RECIPE_COLLISION` 需要同 receiver-visible inputs、pilot-only causal sample budget、radial/tangential structured estimator、shrinkage/pooling action 与 APSK LLR output 的完整组合相同。
- 只覆盖 Mahalanobis、full covariance、generic shrinkage、polar noise 或别的场景，均标 `STRONG_NEIGHBOR/PRIMITIVE_COLLISION`，限制 claim ceiling，不自动关闭硕士级 target-scene extension。
- 不声称首次/SOTA；完整 recipe 非完全相同即可保留 Step 4a 入口，但必须诚实列出强邻居。

## 边界与验收

- 不做 Step 4a、实现、实验，不改仿真/Skill/controller/论文正文；不处理 C5-2 adapter。
- 只提交 query JSON/receipt、少量必要全文、read notes、唯一 supplement report 与项目索引的必要更新。
- 报告必须给三轮新增计数、exact-action ledger、fulltext/abstract 边界、最终 `Q-C5-1 SURVIVES` 或 `EXACT_RECIPE_COLLISION`。
- 最终回报 commit、query/record/fulltext 数、collision verdict、最强邻居和唯一 blocker。
