# Task Brief: C1 Step 4a A0 先验覆盖 / 负面证据 / B2 audit

> 来源: S001 / D009 / H002 | 产出位置: `projects/thesis-fso/worker-logs/step-087-c1-a0-prior-negative-evidence.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 10
  action_class: FEASIBILITY_A0
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

只用本地 corpus/fulltext/receipts 完成非 ML reference-method extension 的 A0 §2–§6：问题结构适配、相邻先例、MDP不适用说明、负面证据、简单先验/B2覆盖。不得新 web/search；不得把 Step3.5 非碰撞当可行性。

## 1. 必答

1. §2：这个 bounded change-point/local repair 问题是否需要复杂方法，还是小状态动态规划/pilot/global retry已足够；对 non-ML method-type 给适配判据，不套用“必须 ML”。
2. §3：至少列 2 个结构相似成功/失败先例及差异；可用 OFC2014、OFC2017、PAPU、HTDD、1704、2604 等，但必须回查本地全文。
3. §4：明确 `MDP=N/A（非DRL）` 的框架依据；同时审查有限候选/边界搜索是否平凡到不形成方法增量。
4. §5：从已有 Step1/3.5 receipts与全文主动提取 limitation/failure/negative evidence；至少包括 strongest simple alternative 与 decoder feedback 可能失败/无增量的机制。若本地证据不足，标覆盖限制，不得联网补。
5. §6：按 FER/post-BER/goodput/clean safety/decode calls/latency/overhead 列 B0/B1/global retry/PAPU-like/OFC2017-like/differential-FEC 等简单先验覆盖；判断哪些可能已达 O1 headroom 的90/95%。
6. 给 A0 致命信号、必须进入 defect smoke 的未知项、B2 absorption kill rule 与 C1-ext 相对 B2 的预冻结 practical-signal候选阈值；阈值须区分建议与文献事实。
7. 列 3 个空白结构性原因并逐一反驳（A0 B 零假设原料）；不作 novelty closure。

## 2. 产出

写 step-087：A0 §2–§6逐项表、先例/负面证据、prior coverage矩阵、B2/kill/unknown清单、evidence pointers。只读；不得 web/下载/改中央/代码/pyc/实验/提交/push/触碰p05。hard cap 15分钟，fresh p05/staging 后收口。
