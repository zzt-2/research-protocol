# Task Brief: Ch5 Q-C5-1 GW Step 4a paper feasibility

> 来源: S028 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-paper-feasibility.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 5
  action_class: GROUNDWORK_FEASIBILITY_PAPER
  mission_checkpoint: CP005
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 `Q-C5-1` 只执行 `stages/gw-feasibility.md` Step 4a 的纸面部分：A0 §0–§6、A'、A、B。不得进入维度 D/MVE。研究对象固定为：当前/过去 pilot residual + APSK ring/angle → radial/tangential covariance parameterization → 跨同环点/跨偏振统计强度的 shrinkage pooling → 正定 structured covariance → Mahalanobis/log-det bit LLR。

## 必答判断

1. A0 §0：Q-C5-1 四判据与 M/C/A 是否仍成立；不得把“没有 exact collision”当问题存在。
2. A0 §1–§6：scalar/per-ring/unstructured full covariance 在小 pilot 条件下的可测缺陷、结构方法是否需要复杂学习、廉价解析替代、receiver-visible 信息和 failure mode。
3. A'：竞争维度拆为 estimator variance/bias、positive-definiteness、GMI/BER/FER、pilot overhead、复杂度；明确主次指标和不可承重维度。
4. A：写出结构优势的数学自由度与偏差-方差机制；给出最小 oracle/headroom 计算计划，但本轮不计算实验数字。
5. B：把外部 novelty 与科学 feasibility 分开；Layton/full covariance/generic shrinkage 只压 claim ceiling，不替代机制可行性判断。
6. 冻结 Step 4a-D 前的候选 recipe v1、公平 comparator 合同、receiver-visible firewall、最小消融、预期方向与明确的 pre-MVE Kill/Pivot 条件。

## 证据与边界

- 只使用 T046/T049、Layton 2018 read note/fulltext、共同平台 parameter authority 与现有 Groundwork 证据；不再检索下载。
- 不实现、不运行代码/仿真，不修改 Skill/controller/论文正文或 feasibility_report 正式终态。
- 不作 Go/Conditional Go；只给 `PAPER_DIMENSIONS_PASS / PIVOT / KILL_BEFORE_MVE` 与唯一 blocker。若纸面通过，主控后续另行授权维度 D correctness/MVE。
- 只提交唯一 paper-feasibility report；最终回报 commit、A0/A'/A/B verdict、candidate v1、strongest cheap comparator、唯一 blocker。
