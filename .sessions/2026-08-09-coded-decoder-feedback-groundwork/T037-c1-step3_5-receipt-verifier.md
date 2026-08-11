# Task Brief: C1 Step 3.5 fresh-context receipts / physical verifier

> 来源: S001 / D008 / step-067–081 | 产出位置: `projects/thesis-fso/worker-logs/step-083-c1-step3_5-receipt-verifier.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 9
  action_class: FULLTEXT_READ
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 0. 审查目标

从 fresh context 独立复核 Step 3.5 的检索充分性、三轮计数、physical/B2 参数锚、coverage limitation 和控制面冻结。不得使用主线程聊天结论；只认磁盘 receipts、worker logs 与本地全文。

## 1. 必验

1. 关键词矩阵是否 ≥8 queries、≥2 有效来源；最高引用核心竞品 forward/backward 是否均执行且筛 ≥10 abstracts。
2. Round 1/2/3 的 raw/unique/known/new/MUST/SHOULD 是否与 JSON/日志一致；重点离线复算 Round 3 `82→79→72, 0/1` 与唯一 OFC2017 身份，不把前 agent 超时聊天当证据。
3. 三轮上限与终态是否正确：不能写 `CONVERGED_ZERO_NEW`；OFC2017 全文 debt 是否确已关闭。
4. 抽核 OFC2014、PAPU、JLT2020 本地全文，验证 slip-rate/PCS、pilot overhead/filter、FSO turbulence/AO/CFO/penalty 数字及 transfer ceiling；不得把 JLT fading 写成 slip 因果。
5. CSSC/CS-DC/PAPU equation/U01/U02 debt、S2/OpenAlex 429/timeout、Crossref/arXiv recall ceiling 是否完整保留。
6. report 与 literature owner 是否一致；topic/control 是否仍禁止 Step4a/adapter/defect smoke，未提前晋级。

## 2. 终态与产出

写 `projects/thesis-fso/worker-logs/step-083-c1-step3_5-receipt-verifier.md`，含可复算公式/路径/行号、physical anchor spot-check、P0/P1/P2 数量、verdict=`PASS` / `FAIL`。FAIL 给最小修复，不得改中央文件。

只读；不得 web/新搜索/下载/改任何文件（除指定 verifier log）、不得实验/提交/push/触碰 p05。hard cap 15 分钟；fresh p05 4/4、staging、关键 JSON parse 后收口。
