# Verifications — 过采样相干 FSO 联合同步前端 Groundwork

## V001: 首次独立验收

> 日期：2026-08-06
> 关联：S001 / D002
> 结论：FAIL

Phase 0、检索统计、BOM、六篇文件质量和阶段边界通过；但 Step 2 未取得其自身识别出的 JLT 2025 /
JOCN 2026 最近直接竞品全文，角色 5 缺失。另发现 RDL registry 不同步、参数证据类型未逐项标注、
S001 历史时点和 receipt 字段语义问题。证据：`independent-verifier-report.md`。

## V002: 修复后第二次独立复验

> 日期：2026-08-06
> 关联：S001 / D003
> 结论：PARTIAL

JLT 2025 官方 arXiv 全文补齐为第 7 篇 CORE；其 identity、SHA256、466 行与动作边界通过。物理数字
证据类型和两项 minor 已修复，八项门控通过；仅 RDL system registry 仍写“覆盖核查中”，与其他控制面
不一致。证据：`independent-reverification-report.md`。

## V003: 最终 fresh-context 验收

> 日期：2026-08-06
> 关联：S001 / D003
> 结论：PASS

registry 已同步到 CP009/D003/Step 2 ready。抽查 7 CORE 的数组数、content SHA256 与行数全部匹配；
JLT 2025 source/content hash 与 466 行匹配；JOCN 2026 三路径失败记录真实。9/9 JSON、2/2 YAML、
`git diff --check`、无暂存/代码/Step 3/仿真与四个 `p05_run*.log` 保护均通过。唯一非阻断遗留是用户
确认是否接受 JOCN 2026 全文缺口。证据：`final-fresh-verifier-report.md`。

## V004: Step 3 独立验收与修复后复验

> date: 2026-08-06
> 关联：S001 / D004 / D005

### 验证项

- [x] 7 篇 CORE identity/SHA/正文：独立复算 `7/7` PASS；行数
  `278/244/455/891/1582/873/466`，6 篇 title PASS，Paillier 为已披露的 title-unverifiable/主题一致。
- [x] read-note 合同：初审发现 4/7 缺显式字段，最小修复后复验为字段 `105/105`、七子表
  `49/49`、通信参数 `7/7`、实验完备性 `7/7`。
- [x] Q1/Q2 科学裁决：Q1 判据 1 FAIL、Q2 判据 1/3 FAIL 均有正文证据；survivor=0。
- [x] Step 3.5/JOCN gate：新增 search/receipt 命中 `0`；JOCN 仍三路径失败，abstract 未冒充全文。
- [x] current-state 一致性：初审 B2–B4 三处 stale-current 已修复；formal/RDL/master 均指向
  `STEP3_NO_VALID_PROBLEM` / CP010 / D029。
- [x] 确定性与保护边界：JSON `9/9`、search SHA `6/6`、YAML `1/1`、Markdown `13/13`、
  protected-path status `0`、四个日志 SHA `4/4`、`git diff --check` exit `0`。

### 证据

同一 fresh-context verifier 在最小修复后重新执行的原始命令：

```powershell
git rev-parse HEAD
git diff --cached --name-only
git status --short --untracked-files=all
git diff --check
Get-FileHash -Algorithm SHA256 <7 CORE content paths>
Get-FileHash -Algorithm SHA256 <4 p05_run*.log>
Get-Content -Raw <9 JSON files> | ConvertFrom-Json
python -c "import yaml; yaml.safe_load(open(r'.sessions/_registry.yaml',encoding='utf-8'))"
rg -n "receiver-visible|action|output|时序|failure|通信.*参数|实验完备性" <7 read notes>
rg -n "STEP3_NO_VALID_PROBLEM|CP010|当前入口|STRATEGIC_SHORTAGE_CONFIRMED" <formal/RDL/master state files>
```

原始计数输出：

```text
HEAD=50b4b474f822e253f02ad44fd47ba37afea6dddf
STAGED_COUNT=0
PROTECTED_LOG_SHA=4/4
CORE_CONTENT_SHA=7/7
CORE_LINE_COUNTS=278/244/455/891/1582/873/466
READ_NOTE_EXPLICIT_FIELDS=105/105
READ_NOTE_SUBTABLES=49/49
COMMUNICATION_PARAMETERS=7/7
EXPERIMENT_COMPLETENESS=7/7
JSON_PARSE=9/9
SEARCH_SHA=6/6
YAML_PARSE=1/1
MARKDOWN_BASIC=13/13
STEP3_5_NEW_SEARCH_OR_RECEIPT_STATUS_MATCHES=0
PROTECTED_PATH_STATUS_MATCHES=0
GIT_DIFF_CHECK_EXIT=0
BLOCKERS_AFTER_REPAIR=0
NONBLOCKERS_AFTER_REPAIR=2
```

逐篇正文抽查、初审 FAIL 证据及修复后完整复验见
`projects/thesis-fso/oversampled-sync-groundwork/step3-independent-verifier-report.md` §1–§8。

### 结论

PASS
