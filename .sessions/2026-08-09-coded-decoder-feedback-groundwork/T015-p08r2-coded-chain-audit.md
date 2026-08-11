# Task Brief: P08-R2 corrected coded-chain 源码、身份与调用链复核

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-061-p08r2-coded-chain-fresh-audit.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书、仓库框架文件与列出的源码/receipt/worker-log

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 6
  action_class: CODED_CHAIN_AUDIT
  mission_checkpoint: CP006
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2` 做一次 fresh、只读的 P08-R2 corrected coded-chain 审计。回答可复用资产、缺失 carrier-action anchor、decoder callback/soft/state 能力、receiver-visible 边界与 C1 最小 adapter 的真实下界。不得继承旧科学 terminal，不得运行实验或改代码。

## 1. 必读与边界

1. 先运行 task-control validator；失败立即停止。
2. 完整读取：
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_chain.py`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_phaseA.py`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_run.py`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_verify.py`
   - `projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md`
   - `projects/thesis-fso/worker-logs/step-047-coded-decoder-lineage-recovery.md`
   - `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`
3. 旧 P08/P08-R/P08-R2 数字与 scientific terminal 只有 PARTIAL diagnostic ceiling；本任务只核 source/receipt 工程事实。
4. 不修改中央状态、`.sessions`、源码、artifact 或四个 `p05_run*.log`；不提交；总时限 15 分钟。

## 2. 必答问题

1. codec/BICM/interleaver/decoder 的精确身份与 source pointer。
2. 当前 `receiver input → equalize → demap → decode → score` 调用链；每处 truth/receiver-visible 字段。
3. 当前是否存在 phase-noise/CFO/slip 状态、phase hypothesis callee、局部 rollback/redecode、persistent controller。
4. Sionna 2.0.1 的 soft output、return_state、iteration override、v2c/c2v callback 能力；旧报告有无语义错误。
5. coded-bit↔symbol mapping 是否可逆、局部 segment/suffix 重译码需要哪些索引/边界。
6. C1 defect smoke 最少需新增哪些新文件/接口，哪些可复用；工作量下界及超过 7 天的明确触发条件。
7. no-feedback/noise-free/callback/mapping/metamorphic/truth-leakage/cost tests 的可执行断言。
8. 输出一份 fresh caller→callee allowlist/denylist 与 `READY / BOUNDED_ADAPTER / TESTBED_GAP / >7D_BLOCKER` 判定；不得把“当前无 anchor”自动升级为科学 Kill。

## 3. 产出与验收

worker-log 必含：validator 结果、读取文件+行号、identity receipt hash/字段、调用链图、能力矩阵、receiver-view schema、最小 adapter BOM、测试断言、工期判断、与 step-049 的一致/修正项、git status 保护检查。只写：

`projects/thesis-fso/worker-logs/step-061-p08r2-coded-chain-fresh-audit.md`

