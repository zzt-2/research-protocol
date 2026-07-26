# Mission Log — Research Direction Lab 长程真实运行测试

> original mission: 在用户只中转任务路径和极短回执的条件下，稳定推进真实研究并积累可用方法材料。
> phase 1: `4af6f9d..aab425d` | audit cutoff: 2026-07-26 | next checkpoint: `CP008`

| CP | 包 / intent / family | formal science disposition | mission method delta | streaks | weight / drift | 下一步为何优于替代项 |
|---|---|---|---|---|---|---|
| CP001 | T001 · log-001 · `4a0d4a4/d40b32e` / RECOVERY / current owners | 5 个 current view 已协调 | NONE | no-method=1 | UNDERWEIGHT / ALIGNED | 用户纠正吞吐过低；下一包必须关闭科学决策 |
| CP002 | T002 · log-002 · `0b642e9` / SCIENCE_GUARD / Pilot-Jones unitary | scoped local Kill；family 未关闭 | NONE | same-axis=1, no-method=2 | ADEQUATE / ALIGNED | complex Jones/PMD/PDL 是唯一未测物理救活轴 |
| CP003 | T003 · log-003 · `5445a2e/9fd5e32` / METHOD_CONSTRUCT / Pilot-Jones complex | verdict 因五项实验语义缺陷拒收 | NONE | same-axis=2, repair=1, no-method=3 | OVERWEIGHT / DRIFT_RISK | 只允许一次有界语义修复，避免固化假 verdict |
| CP004 | T004 · log-004 · `9a250e1/46866aa` / SCIENCE_GUARD / Pilot-Jones complex | 正面 gate 因时间语义与复现闭包拒收 | NONE | same-axis=3, repair=2, no-method=4 | OVERWEIGHT / DRIFTED | T005 只做终局 adjudication；之后不再同轴修复 |
| CP005 | T005 · log-005 · `8f7dd0d/bfc97d7` / SCIENCE_GUARD / Pilot-Jones complex | fixed-component rescue axis scoped Kill 已接收 | NONE | same-axis=4, no-method=5 | ADEQUATE / DRIFT_RISK | 合法 Kill 后转现有 READY carrier B10/B12 |
| CP006 | T006 · log-006 · `21bfbda/3a67c7a` / METHOD_CONSTRUCT / B10-B12 | source identity、channel、statistics 不闭合；verdict 拒收 | NONE | repair=0, no-method=6 | OVERWEIGHT / DRIFT_RISK | 多层缺陷不值得同轴修复；转已有 B1 载体 |
| CP007 | T007 · log-007 · `aab425d` / METHOD_CONSTRUCT / B1 phase window | 未接收；当前 Kill 未满足完整预注册门且 claim 越界 | NONE | no-method=7 | ADEQUATE / DRIFTED | 暂停 T008；先修订 method-production 与整链防偏协议 |

## 使用规则

- master 接收包后、准备下一 T 前追加一行；详细数字只留在 worker-log/artifact。
- 每轮重读 original mission 和全表，分开记录 formal result 与 method delta。
- 连续同轴、repair、no-method 或 UNDERWEIGHT 只触发强制比较，不自动 Kill。
- executor 不修改本文件；master 接收后更新。
- `log-NNN` 对应 `projects/thesis-fso/worker-logs/step-NNN-*.md`；详细 artifact 路径从该日志下钻。
