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

> **历史语义注记（D006）**：V004 保留为历史。它证明了 D005 本地解释、worker reports、状态投影与
> 文档之间的一致性，但未对照 AMC D005，也未逐字核对 canonical owner 是否要求“A 已被正文/MVE
> 证实”。因此其文件/身份/字段/保护边界验证仍有效；其 Q1 判据 1、Q2 判据 1 与 terminal 验证不能
> 作为 canonical 语义结论，已由 D006 取代。`PASS` 仅表示当时本地合同自洽，不表示 semantic gate 正确。

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

## V005: D006/D007 canonical 语义纠偏与 Step 3.5 fresh-context 复验

> 日期：2026-08-06
> 关联：S001 / D006 / D007
> 结论：PASS

### 验证项

- [x] fresh-context verifier 逐字对照 `stages/glossary.md` L22-31 与 AMC Groundwork D005，确认
  canonical 判据 1 只要求 M/C/A 明确、句子级、可解且 A 可证伪，不要求 Step 3 已由 MVE 证明 A。
- [x] Q1 四判据 `PASS/PASS/PASS/PASS`，Q2 为 `PASS/PASS/FAIL/PASS`；Q2 判据 3 独立失败，
  未用跨论文拼接伪造 task-matched baseline。
- [x] D005→D006、V004 历史注记与 H001 superseded 血缘一致；V004 只证明错误本地解释自洽，
  不再承担 canonical semantic verdict。
- [x] Step 3.5 数字复算：Round 1=`6 JSON/100 rows/80 unique`；Round 2=`3 JSON/27 rows/25 unique`，
  真正新增 must/should=`0/0`；Sun 引用链 forward/backward=`8/35`。
- [x] 新增 3 篇全文的 source/content/read-note/read-log 与 SHA/行数一致；它们分别是顺序模块链、
  joint integer frame+CFO、无 frame 的 joint τ+CFO+CPO，均非 exact 三参数 collision。
- [x] JOCN 2026 与 JLT 2025 IQ-skew 的全文缺口仍真实；composite cheap comparator 未冒充单篇方法，
  terminal 未越权写成 novelty closure、METHOD_SIGNAL、Go 或论文方法成立。
- [x] JSON/YAML、git diff、保护日志与越界路径检查通过；未进入 Step 4a、实现、testbed、MVE 或仿真。

### 复验过程与确定性证据

首次 fresh-context 复验发现 `literature_notes_oversampled_sync.md` 两处 stale-current 表述，判为 FAIL；
主控只修正这两处陈旧投影。同一 verifier 随后从 canonical owner、AMC D005 和原始 receipts 全量重跑，
最终 blocker=`0`、semantic=`PASS`、deterministic=`PASS`。

```text
HEAD=6874249530928616c13aa5a6107bc55d08fae939
ROUND1_JSON=6 ROWS=100 UNIQUE=80
ROUND2_JSON=3 ROWS=27 UNIQUE=25 NEW_MUST=0 NEW_SHOULD=0
Q2_ROWS=41/2/0
SUN_CITATIONS=8/35
RECENT_SEARCH_JSON_PARSE=37/37
METADATA_PARSE=9/9 SUCCESS=3 FAILED=6
NEW_FULLTEXT_LINES=555/156/712
READ_NOTE=3/3 READ_LOG=3/3
PROTECTED_LOG_SHA=4/4
OUT_OF_SCOPE_PYCACHE_COMMON_PARAMS_STEP4A_CODE_SKILL=0
STAGING=0
GIT_DIFF_CHECK_EXIT=0
BLOCKERS_AFTER_REPAIR=0
```

完整逐项报告：
`projects/thesis-fso/oversampled-sync-groundwork/step3-5-fresh-semantic-verifier-report.md`。

### 结论

PASS。D006/D007 的 canonical 语义、Step 3.5 证据链与保护边界均通过 fresh-context 复验；允许按
`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED` 关闭本专题，但不产生 Step 4a 入口。

## V006: JLT 用户全文与 coverage closeout fresh-context 复验

> 日期：2026-08-06
> 关联：S001 / D008 / T013 / T014
> 结论：PASS

### 验证项

- [x] 用户提供的 JLT 2025 PDF 已按 DOI 归档；identity、10 页、source/content SHA256、344 行、
  metadata、papers index、read note 与 read-log 均一致。
- [x] 全文只支持 shared-preamble sequential/extra-action：TS-A 复用给 frame detection、IQ-skew、
  SOP、timing recovery、FOE，TS-B 再做 frame synchronization/channel estimation；Eq. 16–23 只估
  IQ-skew，不存在 joint `(frame,fractional τ,CFO)` objective/search/output。
- [x] JLT 因而进入 strongest cheap comparator，但 verdict 为
  `NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`，不构成 Q1 exact collision。
- [x] JOCN 2026 仅按用户明确访问结果登记为 `USER_CONFIRMED_FULLTEXT_UNAVAILABLE`；未用摘要裁
  jointness，也未据此声称 no-collision、exact novelty、“首次”或 Go。
- [x] D008、formal current state、RDL D032/CP015/epoch28 与 H003 一致；未进入 Step 4a、实现、
  testbed、MVE 或仿真。
- [x] JSON `49/49`、YAML `2/2`、protected logs SHA `4/4`、`git diff --check` exit `0`；无越界改动。

### 结论

PASS，blocker=`0`。terminal=
`STEP3_5_COMPLETE_Q1_SURVIVOR_JOCN_FULLTEXT_UNAVAILABLE_NO_CONFIRMED_EXACT_COLLISION`；专题维持
closed，下一合法动作仅为新会话重读 `gw-feasibility.md` 后讨论 Step 4a。完整证据见
`projects/thesis-fso/oversampled-sync-groundwork/jlt-fulltext-closeout-verifier-report.md`。

## V007: Q1 Step 4a preflight 独立收口复验

> 日期：2026-08-07
> 关联：S002 / D009 / D010
> 结论：PASS

### 验证项

- [x] fresh-context verifier 对照 `stages/gw-feasibility.md`、`stages/glossary.md`、H003、D006–D010
  与项目证据，确认 A0 §0–§6、方法身份、离散模型、A′/A/B 和 semantic smoke 合同均已覆盖。
- [x] 初审提出的 5 个 blocker 已逐项修复并由同一 verifier 全量复验：A0 负面证据搜索状态、
  常相位参数去重、B1/C 公平性合同、`miss=N/A` 事件语义、D010 critic 证据指针均已闭合。
- [x] terminal 仅为 `STEP4A_PREFLIGHT_EVIDENCE_GAP`；没有写 Go/Conditional Go，没有把一般非可分性、
  “无人做过”或 JOCN 全文缺口冒充可用性能间隙。
- [x] 维度 D 未执行；没有脚本、MVE、testbed、方法实现或仿真。`common/`、`params.py`、Skill、旧实验
  与四个 `p05_run*.log` 均未改动。
- [x] verifier 的确定性检查通过：Markdown/YAML 合同可解析，`git diff --check` exit 0，保护路径 diff
  为空，当前 HEAD 不在任何 remote ref 中。

### 复验过程与确定性证据

初审为 PARTIAL、blocker=`5`；主控仅修复上述五项，不改变研究终态。fresh-context verifier 随后从框架
owner 与原始证据重新核验，最终报告：

```text
VERDICT=PASS
BLOCKERS=0
YAML_PARSE=4/4
GIT_DIFF_CHECK_EXIT=0
PROTECTED_PATH_DIFF=0
DIMENSION_D_EXECUTION=0
```

完整逐项报告：
`projects/thesis-fso/oversampled-sync-groundwork/step4a-preflight-independent-verifier-report.md`。

### 结论

PASS。该 PASS 只覆盖 Step 4a preflight discussion 与“可执行但未执行”的 semantic smoke 合同；不证明
joint estimator 有收益，不完成维度 D，也不产生 Go/Conditional Go。下一动作仍须由用户决定是否批准
D010 冻结的 ≤1 天 deterministic semantic smoke。

## V008: Q1 deterministic semantic smoke 独立复验

> 日期：2026-08-07
> 关联：S003 / D010–D012 / T015 / T016
> 结论：PASS

### 验证项

- [x] T015/T016 task-control 均 PASS；focused pytest `28/28` PASS；fresh identity-only PASS。
- [x] identity、paired-realization、truth-isolation、score-comparability 四项 semantic gate 全 PASS；estimator
  API 不接收 truth metadata。
- [x] artifacts 为 180 observations、180 truth、720 method rows、180 surfaces；residual noiseless 75、
  residual minus6db 75、stress 30 严格隔离，hash/reference 无孤儿或重复。
- [x] 独立重算得到 noiseless 四法 `0/75`；minus6db B0/B2=`58/75`、B1/C=`59/75`；
  `G_C=0/-0.0172413793`，coverage N/A，无 stable 2×2；B1/C 180/180 exact-equivalent。
- [x] B1/C 为不同 accessor/result 的独立完整 traversal，不是 alias 或相互调用；共同 helper 仅实现冻结的
  score/tie-break 合同。
- [x] 首轮 verifier 的 3 Important + 1 Minor 已经 RED→GREEN 修复并全量复验：traversal/cache-miss 分账、
  worst-margin plot 标记、stress/reducer 隔离、TDD evidence 降级标记与 fresh GREEN hash 均闭合。
- [x] `common/`、所有 `params.py`、Skill、旧实验与四个 protected logs 未变；`git diff --check` exit 0。

### 复验过程与确定性证据

首轮为 FAIL，blocker=`3`；执行 agent 只修复合同完整性，不改 waveform、grid、方法身份或阈值。full re-verification：

```text
SPEC_COMPLIANCE=PASS
CODE_SCIENCE_QUALITY=PASS
FOCUSED_TESTS=28/28
IDENTITY_GATES=4/4
OBSERVATIONS/TRUTH/METHOD_ROWS/SURFACES=180/180/720/180
B1_C_EQUIVALENCE=180/180
STABLE_B0_2X2=0
PROTECTED_LOG_SHA=4/4
BLOCKERS_AFTER_REPAIR=0
```

完整报告：
`projects/thesis-fso/oversampled-sync-groundwork/semantic-smoke-independent-verifier-report.md`。

### 结论

PASS。当前 artifacts 足以独立重算 `STEP4A_PREFLIGHT_KILL_OR_PIVOT`。该 PASS 仅覆盖受限 semantic smoke，
不构成正式 MVE、Go/Conditional Go、testbed、论文数字或连续 estimator 等价。
