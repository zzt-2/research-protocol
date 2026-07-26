# Mission Log — Research Direction Lab 长程真实运行测试

> original mission: 在用户只中转任务路径和极短回执的条件下，稳定推进真实研究并积累可用方法材料。
> phase 1: `4af6f9d..aab425d` | audit cutoff: 2026-07-27 | next checkpoint: `CP016`

| CP | 包 / intent / family | formal science disposition | mission method delta | streaks | weight / drift | 下一步为何优于替代项 |
|---|---|---|---|---|---|---|
| CP001 | T001 · log-001 · `4a0d4a4/d40b32e` / RECOVERY / current owners | 5 个 current view 已协调 | NONE | no-method=1 | UNDERWEIGHT / ALIGNED | 用户纠正吞吐过低；下一包必须关闭科学决策 |
| CP002 | T002 · log-002 · `0b642e9` / SCIENCE_GUARD / Pilot-Jones unitary | scoped local Kill；family 未关闭 | NONE | same-axis=1, no-method=2 | ADEQUATE / ALIGNED | complex Jones/PMD/PDL 是唯一未测物理救活轴 |
| CP003 | T003 · log-003 · `5445a2e/9fd5e32` / METHOD_CONSTRUCT / Pilot-Jones complex | verdict 因五项实验语义缺陷拒收 | NONE | same-axis=2, repair=1, no-method=3 | OVERWEIGHT / DRIFT_RISK | 只允许一次有界语义修复，避免固化假 verdict |
| CP004 | T004 · log-004 · `9a250e1/46866aa` / SCIENCE_GUARD / Pilot-Jones complex | 正面 gate 因时间语义与复现闭包拒收 | NONE | same-axis=3, repair=2, no-method=4 | OVERWEIGHT / DRIFTED | T005 只做终局 adjudication；之后不再同轴修复 |
| CP005 | T005 · log-005 · `8f7dd0d/bfc97d7` / SCIENCE_GUARD / Pilot-Jones complex | fixed-component rescue axis scoped Kill 已接收 | NONE | same-axis=4, no-method=5 | ADEQUATE / DRIFT_RISK | 合法 Kill 后转现有 READY carrier B10/B12 |
| CP006 | T006 · log-006 · `21bfbda/3a67c7a` / METHOD_CONSTRUCT / B10-B12 | source identity、channel、statistics 不闭合；verdict 拒收 | NONE | repair=0, no-method=6 | OVERWEIGHT / DRIFT_RISK | 多层缺陷不值得同轴修复；转已有 B1 载体 |
| CP007 | T007 · log-007 · `aab425d` / METHOD_CONSTRUCT / B1 phase window | 未接收；当前 Kill 未满足完整预注册门且 claim 越界 | NONE | no-method=7 | ADEQUATE / DRIFTED | 暂停 T008；先修订 method-production 与整链防偏协议 |
| CP008 | T008 · log-008 · `61f8c53` / METHOD_CONSTRUCT / B1 phase window | `KILL_NO_ADAPTIVE_WINDOW_SPACE` 拒收；`BLOCKED_IDENTITY`，仅保留 evaluator 负面资产 | NONE | same-axis=2, no-method=8 | OVERWEIGHT / DRIFTED | 停止 B1 修复和 T009；新 Goal 主控先做 campaign remap，再选能直接产方法的合法 carrier |
| CP009 | T009 · log-009 · `8ea886e` / METHOD_CONSTRUCT / A4 deployable CPR | `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`；拒绝“可靠工作区 DA 9/9 物理支配” | NONE | same-axis=1, repair=1, no-method=9 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | 不开第二个 A4 repair；campaign remap 比较 B10 source-native 与新候选，比修当前多层失效 evaluator 更可能产生方法信号 |
| CP010 | T010 · log-010 · `tag:rdl-t010-closure` / METHOD_CONSTRUCT / B10 source-native adaptive pilot-RLS | `BLOCKED_IDENTITY`；primary transfer 的 128-pilot unwrap 在 moderate/14 dB/seed 131004 选错 −2π branch，P1/P2/P3 共用初始化；840-row strict-prefix 终止 | NONE | same-axis=1, repair=1, no-method=10 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | 不改 identity/row schema、不补第二包；转 C15 Step 1–3 formalization，比 B1 第三次 evaluator repair 与 B9 新全链更可能解锁方法载体 |
| CP011 | T011 · log-011 · `700864d` / CANDIDATE_FORMALIZATION / C15 blind-equalization cost | `BLOCKED_SEARCH_COVERAGE`；56 rows/53 unique/49 published，但 actual source 仅 OpenAlex，关键 deep query 未闭合；Step 2 未启动 | NONE | same-axis=1, repair=0, no-method=11 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | 共享索引已有 Semantic Scholar/SerpAPI/OpenAlex/Exa 四源，论文库已有 5 篇近期 content；一次 T012 合并三源恢复、metadata closure 与 3 篇 canonical 获取，比 B1 第三 evaluator repair、A4 第二 identity repair、B9 新全链更可能解锁方法空间；失败即轮换 |
| CP012 | T012 · log-012 · `81ab4a0` / CANDIDATE_FORMALIZATION / C15 source recovery | `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`；两次 executor preflight 与 epoch29 final binding 共暴露 receipt、owner/process predicate、CIM fail-open 三项 task-contract 缺口；§2.2–2.5 均未执行 | NONE | same-axis=2, repair=1, no-method=12 | UNDERWEIGHT / package DRIFT_RISK；mission DRIFTED/STALLED | 遵守 one-last-attempt，不做第四次 T012 amendment；post-T012 remap 比继续接口修补、B1 第三 evaluator repair或 A4/B10 第二 identity repair更可能恢复方法载体，C15 仅返回池不作 science Kill |
| CP013 | T013 · log-013 · `16176c2/7ca3cbf` / CANDIDATE_FORMALIZATION / B9 Step 1 evidence adapter | `BLOCKED_SEARCH_COVERAGE`；61→58、21 nonexcluded、8 必读、21/21 正式发表，但实际来源仅 OpenAlex；Route A deep=0，Route B deep 仅一般 task-fit/adjacent FSO；非 B9 Go/Kill | NONE | same-axis=1, repair=0, no-method=13 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | 一次 bounded multi-source/mechanism-deep repair 有正向全文锚、真实 EFNS comparator 和集中缺口，完成最小债务后最终 METHOD_SIGNAL 主观判断 15%–25%，高于 C15/B1/A4 最佳 5%–15%；失败即 B9 返回池，不做第三个 Step 1 包 |
| CP014 | T014 · log-014 · `5ba5a54c` / CANDIDATE_FORMALIZATION / B9 Step 1 coverage repair | `BLOCKED_SEARCH_COVERAGE`；A1 raw=`0/0/1`，实际 source union=`openalex,ieee`、count=`2<3`；A2/A3/A4 未运行，非 B9 Go/Kill | NONE | same-axis=2, repair=1, no-method=14 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | 唯一 coverage repair 已用尽，B9 返回池且禁止第三包；post-B9 remap 比继续检索补丁更可能恢复方法载体，下一轮比较 B12 standalone、C15 与至少一个机制不同替代项的 formal readiness |
| CP015 | T015（dispatch review 后撤回，无 worker log/commit）/ METHOD_PREP / B12 standalone | `BLOCKED_NOVELTY_COLLISION / PACKAGE_WITHDRAWN_BEFORE_EXECUTION`；V038 发现非物理 GG lifecycle 与错误 Huber precision；V039/V040 确认 JLT 2025 Huber robust Bayesian CPR direct collision，全文不可得故 novelty fail-closed；未运行 seed，非 B12 science Kill | NONE | same-axis=1, repair=0, no-method=15 | ADEQUATE / package ALIGNED；mission DRIFTED/STALLED | D029 的单包退出已触发，B12 回池且禁止第二 repair；比较 B4、B6、C15 等机制不同候选，比修公式或用摘要猜 novelty 更可能恢复合法方法载体 |

## 使用规则

- master 接收包后、准备下一 T 前追加一行；详细数字只留在 worker-log/artifact。
- 每轮重读 original mission 和全表，分开记录 formal result 与 method delta。
- 连续同轴、repair、no-method 或 UNDERWEIGHT 只触发强制比较，不自动 Kill。
- executor 不修改本文件；master 接收后更新。
- `log-NNN` 对应 `projects/thesis-fso/worker-logs/step-NNN-*.md`；详细 artifact 路径从该日志下钻。
