# Task Brief: C1 arXiv 2511.21340 全文获取与完整链精读

> 来源: S001 | 产出位置: `papers/_read_notes/2511.21340.md` + `projects/thesis-fso/worker-logs/step-058-c1-arxiv2511-fulltext-read.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书、仓库中的框架文件、论文下载工具与下载后的论文全文

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

你在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。目标论文是 **Phase-Aware Code-Aided EM Algorithm for Blind Channel Estimation in PSK-Modulated OFDM**（arXiv `2511.21340`）。

**你的任务**：按 Groundwork Step 2→3 的全文纪律获取、title-check 并精读该文，判断它只覆盖全局一次性 candidate selection，还是已经覆盖局部 slip 定位/segment 或 suffix repair 的完整链。

**最高纪律（违反一条就废了）**：

1. 必须读 `content.md`；摘要只能筛选，不能裁完整链 collision。
2. 先运行 task-control validator；失败立即停止。不得修改 topic/master/decision/mission/central literature owner。
3. 只陈述全文可定位事实；时间粒度、decoder evidence、decode 次数、局部修复若正文没写，标 `NOT_STATED`，不得由标题或直觉补齐。
4. 禁止 webReader/ResearchGate/Google Scholar 页面抓全文。使用仓库 `tools/download`；因 worktree 脚本 CRLF，允许等价无改写调用：`cd tools && tr -d '\r' < download | bash -s -- --arxiv 2511.21340`。
5. 不把拟议 C1-ext 当已成立方法，不给 Go/Kill；只输出事实、collision ceiling 与 Q# 原料。
6. 不提交 git，不碰四个 `p05_run*.log`，总执行时间不超过 15 分钟。

## 1. 背景（了解即可，不要对照评价）

历史 Step 1 已确认该文摘要覆盖 `decoder extrinsic evidence → PSK symmetry finite candidates → one selection`。D005 把这条核心动作降为 reference baseline M；新颖性只可能来自合法局部 slip/时变 ambiguity 缺陷与完整扩展链。完整签名是 `receiver-visible input → trigger → localization granularity → candidate action → decoder interaction → fallback → complexity/latency budget → output`。

## 2. 任务详情

### 2.1 必答问题

1. 方法处理 global ambiguity 还是 local/time-varying slip？
2. hypotheses 的时间/空间粒度？
3. decoder evidence 的精确定义、公式与因果时点？
4. 是否 iteration-wise？
5. 是否定位 slip boundary？
6. 修正整个 frame、OFDM model、segment 还是 suffix？
7. candidate 数与 decode/EM 次数？
8. clean-frame/no-ambiguity 行为？
9. 论文自述失效条件与场景边界？
10. 是否覆盖拟议完整局部 repair 链；若否，差异必须是全文事实而非命名差异。

### 2.2 执行方式

1. 读 `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`、`domain-comms.md §1.1`。
2. 运行 `python .agents/skills/research-direction-lab/scripts/validate_task_control.py <本任务书路径>`（若脚本 CLI 不同，先 `--help`）。
3. `tools/download --dry-run` 后正式下载；检查 `metadata.json` 与 `content.md` 行数，按 title overlap 规则决定继续或 ABORT。
4. 精读 method/algorithm/experiment/conclusion；公式、表、图、章节与关键数字给精确定位。
5. 写 read-note 与 worker-log。下载失败按 gw-acquire 三轮止损，保留失败通道与覆盖限制，不以失败替代全文结论。

### 2.3 产出格式（强制）

`papers/_read_notes/2511.21340.md` 必含：标准文献条目字段；通信信号/信道/编码参数表；非 ML 方向对状态/动作/奖励/网络架构字段写 `N/A（非 ML）`；M/C/A 与四判据逐项原料；实验完备性；上述十问；完整链八字段矩阵；`collision_verdict ∈ {EXACT_COMPLETE_CHAIN, PARTIAL_CORE_ONLY, STRONG_NEIGHBOR, NOT_COMPARABLE, UNRESOLVED_FULLTEXT}`；claim ceiling。

worker-log 必含：task-control 结果、获取命令与通道、title check、内容行数、源文件路径、关键结论（≤10 条）、未决/失败项、写入文件、耗时、git status 保护检查。

## 3. 已知陷阱

- 该文场景是 PSK-OFDM blind channel estimation，不得把 constant phase ambiguity 自动解释成 coherent-FSO local cycle slip。
- “invoked once”不能自动推出 clean-frame no-op、segment localization 或 bounded suffix rollback。
- `decoder selects candidate` 不等于 `decoder evidence locates boundary`。

## 4. 验收

- [ ] title self-check 通过或明确 ABORT
- [ ] 十问全部有正文定位或 `NOT_STATED`
- [ ] 完整链八字段齐全且 verdict 有证据
- [ ] M/C/A 只是原料，不把 defect 假设预写为成立
- [ ] read-note/worker-log 路径正确，未改中央 owner/p05，未提交

## 附：产出回传位置

- `papers/_read_notes/2511.21340.md`
- `projects/thesis-fso/worker-logs/step-058-c1-arxiv2511-fulltext-read.md`
