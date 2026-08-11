# Task Brief: C1 TSP 2006 全文获取与完整链精读

> 来源: S001 | 产出位置: `papers/_read_notes/10.1109_tsp.2006.874844.md` + `projects/thesis-fso/worker-logs/step-059-c1-tsp2006-fulltext-read.md`
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

目标论文是 **Code-Aided Frame Synchronization and Phase Ambiguity Resolution**，DOI `10.1109/TSP.2006.874844`。

**任务**：按 Step 2→3 获取并精读全文，闭合其 hypothesis 粒度、decoder/code evidence、frame/segment 修复、复杂度与局部 slip 能力；不能用现有摘要的 strong-neighbor 标签代替全文。

**最高纪律**：

1. task-control 先验 PASS；只写独立 read-note/worker-log，不改中央 owner。
2. 必须读 `content.md`，每个必答字段给章节/公式/图表/页码或 `NOT_STATED`。
3. 下载走 `tools/download` 三轮止损；禁止 webReader/付费墙网页抓取。CRLF workaround 可用 `cd tools && tr -d '\r' < download | bash -s -- --doi 10.1109/TSP.2006.874844`。
4. 不把“code-aided hypothesis testing”自动升级为 same-information/same-granularity/same-budget 完整链碰撞。
5. 不提交、不碰 p05，总执行时间 ≤15 分钟。

## 1. 背景（了解即可）

D005 固定 C1 reference baseline 为全局一次性 finite phase-hypothesis decoder selection。拟议 extension 只有在全文未覆盖同信息、同 trigger、同 localization、同局部修复、同 decoder interaction/fallback/budget/output 时才可能继续；当前 defect 未成立。

## 2. 任务详情

### 2.1 必答十问

与 T012 相同：global/local、hypothesis 粒度、evidence 类型、iteration-wise、boundary localization、frame/segment/suffix、candidate/decode 次数、clean behavior、失效条件、完整链等价性。另额外回答 frame synchronization 与 phase ambiguity 两个子任务是否共用 code metric，以及 phase ambiguity 处理是否依赖码结构修改/已知 sync word/CRC/truth。

### 2.2 执行方式

读 `gw-acquire/gw-read/glossary/domain-comms §1.1`；验证任务控制；dry-run→download→必要 arXiv alias 定向检索→`tools/blit --download`→停止；title-check；精读 method/experiment；写两份产出。若全文不可得，worker-log 必须列三轮证据，read-note verdict=`UNRESOLVED_FULLTEXT`，不得凭摘要完成裁决。

### 2.3 产出格式

`papers/_read_notes/10.1109_tsp.2006.874844.md`：标准条目、通信参数、非 ML N/A 字段、M/C/A 原料与四判据、实验完备性、十问+额外问、完整链八字段矩阵、collision verdict 与 claim ceiling。

worker-log：control、获取/止损、title/行数、源路径、关键事实、未决、写入清单、耗时、git/p05 保护。

## 3. 已知陷阱

- 题名里的 frame synchronization 不能当作 slip boundary localization。
- phase hypotheses 在整个 frame 上测试，不等于 segment/suffix repair。
- 码约束 metric 与 decoder extrinsic/trajectory 的信息身份可能不同，必须原文区分。

## 4. 验收

- [ ] 全文或合规 `UNRESOLVED_FULLTEXT`
- [ ] 十问+额外问逐项有定位
- [ ] 八字段 collision matrix 不靠摘要推断
- [ ] 没有 Go/Kill/方法成立越级声称
- [ ] 未改中央 owner/p05、未提交

## 附：产出回传位置

- `papers/_read_notes/10.1109_tsp.2006.874844.md`
- `projects/thesis-fso/worker-logs/step-059-c1-tsp2006-fulltext-read.md`
