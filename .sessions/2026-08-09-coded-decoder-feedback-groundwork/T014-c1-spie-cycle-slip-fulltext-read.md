# Task Brief: C1 SPIE 2026 cycle-slip comparator 全文获取与精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1117_12.3107192.md` + `projects/thesis-fso/worker-logs/step-060-c1-spie-cycle-slip-fulltext-read.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书、仓库框架文件、下载工具与论文全文

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 6
  action_class: FULLTEXT_READ
  mission_checkpoint: CP006
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR（执行方先读）

目标论文是 **Cycle Slip Mitigation Scheme Aided Blind Carrier Phase Recovery Algorithms**，DOI `10.1117/12.3107192`。

**任务**：获取并精读全文，判断它作为 coherent-optical strongest cheap comparator 是否处理局部 cycle slip、如何检测/定位/修复、使用何种 pilots/front-end 信息，以及是否已经消除 C1 的目标 defect。

**最高纪律**：

1. task-control 先 PASS；必须读全文，摘要不能裁 B2 是否“已解决”。
2. 只写独立 read-note/worker-log，不改中央 owner；不提交、不碰 p05。
3. 下载只走 `tools/download`/arXiv alias/`tools/blit` 三轮；禁止 webReader。CRLF workaround：`cd tools && tr -d '\r' < download | bash -s -- --doi 10.1117/12.3107192`。
4. phase-pilot/amplitude-label 方法的信息访问必须明确；不得把 receiver-visible pilot 误写成 decoder evidence，也不得把离线 truth 驱动当 deployable。
5. 总执行时间 ≤15 分钟；全文失败就保留 `UNRESOLVED_FULLTEXT`，不脑补。

## 1. 背景（了解即可）

B2 必须是实际 strongest cheap alternative，而非想象中的替代。该文在历史 Step 1 仅由 SPIE 摘要支持“pilot-aided cycle-slip mitigation”；其局部性、调用链和预算均未确认。

## 2. 任务详情

### 2.1 必答问题

1. cycle slip 的物理/信号模型、发生粒度和合法参数；2. detector 输入；3. 定位粒度/lead time；4. repair action；5. BPS/BCPR interaction；6. 是否需要 phase pilots/amplitude labels；7. clean/no-slip 行为与 false trigger；8. decode/CPR/候选调用数和复杂度；9. metric/实验条件与对手；10. 失效条件；11. 是否完整解决“局部 slip 污染全局 decoder evidence”的 defect；12. 能否作为 B2，信息与成本如何与 B1/C1-ext 配平。

### 2.2 执行方式

读 `gw-acquire/gw-read/glossary/domain-comms §1.1`；验证 control；dry-run→三轮止损；title-check；精读 algorithm/system/experiment；逐项记录公式、图、表、页码；写两份产出。

### 2.3 产出格式

read-note：标准条目、coherent optical signal/phase-noise/cycle-slip 参数表、非 ML N/A 字段、论文 M/C/A 与四判据原料、实验完备性、十二问、完整链八字段、`B2_identity ∈ {TASK_MATCHED, PARTIAL, NOT_MATCHED, UNRESOLVED_FULLTEXT}`、collision/claim ceiling。

worker-log：control、下载通道/失败、title/行数、源路径、关键事实、B2 身份限制、写入、耗时、git/p05 保护。

## 3. 已知陷阱

- “aided BCPR”可能只是 pilot 标记，不等于 decoder-aided 或局部 re-decode。
- 检出 slip 不等于定位 boundary，也不等于 segment/suffix repair。
- 若实验只给 uncoded BER/相位误差，不能宣称解决 coded FER/goodput defect。

## 4. 验收

- [ ] 全文或合规 unresolved receipt
- [ ] 十二问及八字段均有原文定位/NOT_STATED
- [ ] B2 信息访问、成本、clean behavior 明确
- [ ] 不越级声称 defect resolved
- [ ] 未改中央 owner/p05、未提交

## 附：产出回传位置

- `papers/_read_notes/10.1117_12.3107192.md`
- `projects/thesis-fso/worker-logs/step-060-c1-spie-cycle-slip-fulltext-read.md`
