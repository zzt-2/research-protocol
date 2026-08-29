# Task Brief: APSK 均衡与软解调经典 baseline

> 来源: S028 | 产出位置: `projects/thesis-fso/direction-lab/harvest/apsk-front-end-baseline-authority.md`
> 日期: 2026-08-30
> 唯一文档: 本 T + 当前仓库既有证据；允许用项目 `tools/search` 做外部学术检索

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 1
  action_class: EXTERNAL_EVIDENCE
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

为 Ch4 的 APSK 环感知半盲/约束均衡和 Ch5 的径向—切向几何软解调完成 Groundwork Step 1 检索，冻结足够而不过度的经典 comparator 与适用前提。

最高纪律：只做 Step 1，不实现、不跑实验；主 Go comparator 是正确、常用、同任务经典方法，不要求追尽 SOTA。强邻居进入 comparator/claim ceiling，不靠想象自动 Kill 候选。

## 1. 背景

Ch4 暂定排序 C4-2 环感知半盲、C4-1 scaled-unitary、C4-0 时序正则。Ch5 暂定 C5-1 APSK 几何软解调、C5-2 syndrome rescue、C5-0 LLR 校准。本任务只覆盖前端均衡与 demapper 的经典 baseline，不讨论 LDPC 内部算法。

## 2. 任务详情

1. 至少三组查询：multi-ring APSK blind/semi-blind equalization；CMA/MMA/radius-directed equalization for APSK；APSK soft demapping under anisotropic/non-Gaussian residuals。
2. 审查不少于 20 条元数据，验证正式版本、经典来源与独立代表性使用。
3. 分别回答：
   - C4-2 最公平 baseline 是 tuned CMA、MMA、RDE 还是 pilot-aided LS+DD；各自使用信息和输出是否同任务？
   - C4-1 的 scaled-unitary 结构在哪种 Jones/PDL 条件成立？
   - C5-1 的 baseline 是 isotropic max-log、per-ring noise variance、还是完整 covariance demapper；径向—切向动作是否会改变 LLR 排序而非仅标量缩放？
4. 给出每个 claim 的最小 baseline ladder：当前链、一个经典主 comparator、一个确实直接解决问题的廉价扩展；不要追加无关 SOTA。
5. 输出 5–8 篇 Step 2 必读候选，标全文可得性和必须核对的公式/图表。

产出结构：一句话结论；Ch4 comparator 表；Ch5 demapper comparator 表；适用前提/碰撞风险；最小 baseline ladder；Step 2 候选；UNKNOWN。保存产出并只提交该 harvest 文件及本任务生成的唯一 search JSON；最终回报 commit、路径和一句结论。

## 3. 已知陷阱

- 不把 QPSK/16QAM 的 constant-modulus 设置直接搬给多环 APSK。
- 不把“有人做过同族”误判为完整 recipe 完全重复。
- 不用 oracle 或 receiver 不可见真值作 Go comparator。

## 4. 验收

- [ ] Ch4 与 Ch5 各有 claim-specific conventional comparator
- [ ] baseline ladder 在三层内停止且说明 stop reason
- [ ] 5–8 篇 Step 2 候选可核
- [ ] 无实验、代码或论文正文修改

