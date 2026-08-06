# Task Brief: Step 3 独立验收

> 来源: S001 | 产出位置: `projects/thesis-fso/oversampled-sync-groundwork/step3-independent-verifier-report.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取本任务书、Git diff、formal/RDL 状态文件、7 份 read notes 与三个 worker logs

## 0. TL;DR

在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2` 对 GW Step 3 做 fresh-context 独立验收。
只写 verifier report，不修改任何 owner、read note、worker log 或决策，不 commit，不联网。

## 1. 验证项

1. 核对当前起始基线 HEAD 为 `50b4b474f822e253f02ad44fd47ba37afea6dddf`，四个 `p05_run*.log` 未修改/暂存。
2. 核对 7 篇 CORE 的 identity/title 结果、canonical 源路径与全局 read notes；抽查每篇至少两条 method/experiment 行号证据。
3. 核对每份 read note 是否含标准字段、7 子表、通信参数、实验完备性；Tang 重读不应抹去旧用途。
4. 独立审查 Q1：GEO 2023 是否覆盖 2-sps timing/SCO→frame→CFO 顺序链；Sun 2025 是否仍为顺序动作；当前是否真有顺序链失效的正文证据；判据 3 是否确有 2019+ task-matched baseline。
5. 独立审查 Q2：是否真有 GG/dynamic fade+SCO 下双环共同失锁；shared freeze+fixed restart 是否已解决/被证伪；是否存在 2019+ integrated comparator。
6. 核对 `step3-deep-read-report.md` 与 literature notes 的 canonical 四判据、最强 comparator、terminal=`STEP3_NO_VALID_PROBLEM` 是否由证据支持；不得自造判据。
7. 核对 Step 3.5 gate：survivor=0 时应未新增 search JSON、引用链或 JOCN 抓取；既有三路径 receipt 保持，abstract 未冒充全文。
8. 核对 topic-index、decisions、S001、registry、master-state、RDL control/mission CP010 的状态一致性；检查 D/V/H 编号、scope change 与 voice。
9. 运行可用的确定性验证：`git diff --check`；JSON/YAML/Markdown 基础检查；`git status --short`；确认未修改 common/、params.py、旧实验结果或 Skill，未触碰四个 log。

## 2. 产出格式

报告必须列：逐项 PASS/FAIL/PARTIAL、原始命令/计数、关键证据路径、发现的问题（按阻断/非阻断）、最终结论三选一 `PASS/FAIL/PARTIAL`。任何 FAIL 必须给最小修复建议。不得代替主控写 V/H 或改变 terminal。

## 3. 验收

- 至少 3 条跨文件事实完成独立交叉验证；7 篇身份与字段覆盖有确定性计数。
- 科学裁决与执行完整性分开评估。
- 不以 agent/owner 自述作为唯一证据。
