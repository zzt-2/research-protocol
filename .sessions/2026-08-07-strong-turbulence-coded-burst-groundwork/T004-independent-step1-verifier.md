# Task Brief: Step 1 fresh independent verifier

> 来源: S001 | 产出位置: `.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R005-independent-verifier-report.md`
> 日期: 2026-08-07
> 唯一文档: 执行方可读本专题全部文件、四个 search JSON、历史证据与 git 状态；不信任 executor 自述

## 0. TL;DR（执行方先读）

以 fresh context 独立验证本专题的治理闭合、query receipt、物理/竞品/BOM 承重事实、outage 语义门和 terminal。产出 R005，结论只能 `ACCEPT / REJECT / PARTIAL`。

最高纪律：

1. 不运行仿真、Python、测试或 import；只用 PowerShell/`rg`/`Get-Content`/`git` 做静态与确定性复算。
2. 不信任 R001–R004 的总结；至少验证 8 条承重声称到原始 JSON/全文/源码/worker-log。
3. 重新计算四个 JSON count+SHA256，检查 6/6 query、2019+ strict baseline 数、三搜索源门和 Step 2 是否实际未执行。
4. 审计 forbidden paths：`common/`、`params.py`、旧 raw/result、Skill、四个 `p05_run*.log` 不得被本轮改动；识别 `tools/litsearch/__pycache__` 是否为工具副作用。
5. 核验 terminal 是否应为 `STEP1_EVIDENCE_INSUFFICIENT`，尤其检查是否误判为 `OUTAGE_NOT_INTERLEAVING_PROBLEM`、`NO_2019_PLUS_TASK_MATCHED_BASELINE` 或 `TESTBED_SCOPE_EXCESSIVE`。
6. 只写 R005；不要自行修改 D/topic/master-state。

## 1. 验证清单

- 启动 HEAD 与初始 dirty scope；registry 单一 slug、depends_on、closed 状态；topic-index/S001/D001-D002 模板与进度一致。
- R001：至少核 3 个来源指针与数值/证据类型，确认 occurrence/AFD 未闭合。
- R002：四 JSON count/hash；至少核 3 个论文 action/年份/DOI；严格 task-matched baseline 是否确为 1；旧 4b#1/P08/AMC collision 是否合理。
- R003：沿源码至少核 lifecycle、interleaver controllability、schema、metric 四项；工期仅是估算，不冒充实测。
- R004：三预卡 11 字段齐全；六项 reopen gate 无全 PASS；outage 六问无逻辑越界。
- Step 2：没有新下载/CORE content、没有 SHA/≥50 行伪闭合、没有运行 coded-chain。
- 文件卫生：禁止路径和 p05 logs 未改；列出所有本轮 tracked/untracked 变化及需要清理项。

## 2. 产出格式

R005 必须包含：验证方法；逐项 PASS/FAIL 表（至少 12 项）；8 条以上原始证据重算；query/hash 原始输出；terminal alternatives 分析；治理/文件卫生；结论 `ACCEPT/REJECT/PARTIAL`；若非 ACCEPT 列 blocker 与精确修复。

## 3. 验收

- [ ] fresh context，不复述 executor 摘要。
- [ ] ≥8 条事实到原始指针。
- [ ] count/hash/terminal 独立重算。
- [ ] forbidden path 与 Step 2 未执行均有 git/文件证据。
- [ ] 只写 R005。

## 附：产出回传位置

`.sessions/2026-08-07-strong-turbulence-coded-burst-groundwork/R005-independent-verifier-report.md`
