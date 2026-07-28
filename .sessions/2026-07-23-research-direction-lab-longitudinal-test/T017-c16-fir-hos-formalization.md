# Task Brief: C16-open full-complex FIR non-modulus Step 1–2 formalization

> 来源: S001 / R007 / D022 / formal D033
> 产出位置:
> `projects/thesis-fso/worker-logs/step-017-c16-fir-hos-formalization.md`
> 日期: 2026-07-27
> 执行方式: 仅由本 Goal 内部 executor 分相执行；用户不转发、不读技术日志、
> 不判断科学正确性

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 42
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP016
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：只用 Groundwork Step 1–2，把
“full-complex 2×2 FIR non-modulus blind equalizer”从旧 C16
task-mismatch 线索转成可审查的 source/fulltext/coverage 状态。

**最高纪律（违反任一条，本包废弃）**：

1. 本包不是方法或实验包：
   `formal_active_scientific_carrier=NONE`，
   `mission_method_delta=NONE`，禁止 simulation/Probe/MVE/seed。
2. 禁止运行或修改旧 C16 sandbox；禁止使用 seeds 71–80；禁止复用旧
   `MECHANISM_NEGATIVE` 或 complementarity 结论。
3. 禁止精读、写 Q#、修改 `literature_notes.md`、实现 FIR/HOS、修改
   common/params/Skill/controller。
4. executor 不更新 `.sessions`、control、formal owner、mission-log、current
   projections 或 registry；只写本任务授权的 search/papers artifacts 与
   step-017 worker log。
5. 搜索元数据/abstract 不能冒充全文。全文必须有 title identity 和
   `content.md >=50` 行有效内容。
6. 任一 hard gate 失败立即 stop；不得降低门槛、修工具/owner、增加第二个
   C16 source package或越过 coverage confirmation。

冻结终态只有五种：

```text
BLOCKED_PREFLIGHT
BLOCKED_EXECUTION_TIMEBOX
BLOCKED_SEARCH_OR_IDENTITY
BLOCKED_FULLTEXT_COVERAGE
AWAITING_COVERAGE_CONFIRMATION
```

逐状态映射：

```text
BLOCKED_PREFLIGHT
BLOCKED_SEARCH_OR_IDENTITY
  -> formal_science_disposition=BLOCKED_FORMAL_READINESS
  -> mission_method_delta=NONE
  -> PHASE_B_AUTHORIZED=FALSE
  -> STEP3_AUTHORIZED=FALSE

BLOCKED_EXECUTION_TIMEBOX
  -> formal_science_disposition=BLOCKED_FORMAL_READINESS
  -> mission_method_delta=NONE
  -> execution_phase=A 时 PHASE_B_AUTHORIZED=FALSE
  -> execution_phase=B 时 PHASE_B_AUTHORIZED=TRUE
  -> STEP3_AUTHORIZED=FALSE

BLOCKED_FULLTEXT_COVERAGE
  -> formal_science_disposition=BLOCKED_FORMAL_READINESS
  -> mission_method_delta=NONE
  -> PHASE_B_AUTHORIZED=TRUE
  -> STEP3_AUTHORIZED=FALSE

AWAITING_COVERAGE_CONFIRMATION
  -> formal_science_disposition=FORMAL_READINESS_STEP2_COMPLETE_AWAITING_USER_GATE
  -> mission_method_delta=NONE
  -> PHASE_B_AUTHORIZED=TRUE
  -> STEP3_AUTHORIZED=FALSE
```

---

## 1. 背景与权威边界

### 1.1 唯一权威

- live control：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
- live owner：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D022`
- formal owner：
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D033`
- remap：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/R007-post-c15-mechanism-carrier-remap.md`
- framework：
  `stages/groundwork.md`、`stages/gw-search.md`、
  `stages/gw-acquire.md`、`stages/glossary.md`

### 1.2 只继承的当前事实

- `portfolio/current.yaml` 中 C16 当前是
  `status=FORMALIZATION_WORKLINE_SELECTED_NOT_ACTIVE`、
  `readiness=HYPOTHESIS_ONLY`；其 note 中的 D017 amendment 记录：旧方法是
  spatial 2×2 whitening + real-Givens heuristic，**没有 FIR structure**，
  不能与 11-tap 2×2 butterfly CMA 作 capability-aligned comparison。
- equalizer-paradigm axis 因此 `REOPENED`。这不证明 HOS 有效，只证明旧
  negative 无权关闭该轴。
- 旧 C16 source code 只可用于确认“没有 FIR”的事实；旧 synthesis、result、
  seeds 和 post-hoc complementarity 均禁止作为 Go/coverage/method 证据。

### 1.3 候选正向合同（了解即可，不得据此实现）

```yaml
positive_method_target: source-backed full-complex 2x2 FIR non-modulus blind equalizer
legal_runtime_information: receiver samples and receiver-visible causal state only
minimal_construct_after_future_gates: task-matched 11-tap complex FIR HOS/joint-diagonalization or Step-3-confirmed equivalent
fair_comparators:
  - tuned 11-tap 2x2 butterfly CMA
  - tuned task-matched 11-tap 2x2 MMA
comparison_budget_alignment: same samples, 11 taps, warm-up and update budget
claim_ceiling_this_package: FORMAL_READINESS_ONLY
```

---

## 2. 分相与时间盒

T017 是一个 package，但必须拆为两个独立 executor turn：

1. **Phase A / Step 1**：多源检索、AI review、identity/coverage synthesis；
2. **Phase B / Step 2**：只在 Phase A 全门 PASS 后做 acquisition 和
   coverage-gap report。

每个 turn 最长 15 分钟；12 分钟仍未闭合当前原子任务时，写
`BLOCKED_EXECUTION_TIMEBOX` 并停止。Phase A 失败不得启动 Phase B。

最终由未参与执行的独立 verifier 读取 raw artifacts 与 worker log 统一验收。

---

## 3. Phase A — Groundwork Step 1

### A0. 起飞门

从 worktree 根执行：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T017-c16-fir-hos-formalization.md
git status --short
```

必须满足：

- task-control PASS：epoch42 / CP016 /
  `action_class=CANDIDATE_FORMALIZATION`；
- D022、D033 active；D021、D032 superseded，但其 T016/C15 退出边界保留；
- control 为 `C16_FIR_HOS_FORMALIZATION_PREP`；
- 无 simulation/MVE/seed 进程；
- 当前 worktree 的既有 dirty files 只属于主控尚未提交的 T017
  owner/control/remap/review 投影；executor 必须在 worker log 记录起飞时完整
  `git status --short`，并在结束时证明这些受保护文件 hash 未被自己改变。

任一失败：只写 worker log，终态 `BLOCKED_PREFLIGHT`。

### A1. 工具 EOL 纪律

Windows checkout 可能把 Bash wrapper 检出为 CRLF。起飞时先用
`git ls-files --eol tools/search` 记录原始 worktree EOL：

- 原始为 `w/lf`：不得调用 `dos2unix`/`unix2dos`，直接运行；
- 原始为 `w/crlf`：调用前执行 `dos2unix tools/search`，调用后立即
  `unix2dos tools/search` 恢复原始 CRLF；
- 其他/无法判定：`BLOCKED_PREFLIGHT`，不得猜测。

这是工作树 EOL 适配，不得修改脚本语义。每轮后必须记录：

```powershell
git hash-object tools/search
git rev-parse HEAD:tools/search
git status --short -- tools/search
```

两个 object hash 必须相同，且结束时 `tools/search` 不得留下 diff。
`PYTHONDONTWRITEBYTECODE=1` 必须保持，禁止产生 tracked pycache 污染。

### A2. 一轮多角度检索

每组均用 `s2 openalex arxiv` 三个 actual source、每源最多20条、输出最多60条：

```powershell
# 先按 A1 的原始 EOL 条件适配；w/lf 时不转换
bash tools/search `
  "blind equalization complex convolutive MIMO QAM higher order statistics" `
  --mode academic --sources s2 openalex arxiv --max-per-source 20 --top 60 `
  --year-from 1990 --sort composite --format json `
  -o search-archive/2026-07-27/c16-a1-convolutive-hos.json

bash tools/search `
  "polarization multiplexed coherent optical blind FIR equalizer higher order statistics ICA" `
  --mode academic --sources s2 openalex arxiv --max-per-source 20 --top 60 `
  --year-from 1990 --sort composite --format json `
  -o search-archive/2026-07-27/c16-a2-coherent-optical-fir.json

bash tools/search `
  "non constant modulus blind equalization PM-16QAM complex FIR" `
  --mode academic --sources s2 openalex arxiv --max-per-source 20 --top 60 `
  --year-from 1990 --sort composite --format json `
  -o search-archive/2026-07-27/c16-a3-nonmodulus-pmqam.json
# 若且仅若 A1 记录的原始状态为 w/crlf，此处恢复 CRLF
```

不得把“命令配置了某 source”当作 actual source。actual source 必须由每条
raw retrieval 的落盘 provenance 证明；空返回不计源。

### A3. AI candidate review

executor 必须读取三份 JSON 的每条 title+abstract+venue+year+citation+
publication status，逐条标注：

- `priority`：必读 / 建议读 / 待确认 / 备选 / 排除；
- `priority_reason`；
- `route`：
  - `R1_CONVOLUTIONAL_COMPLEX_BSS_HOS_FIR`
  - `R2_COHERENT_OPTICAL_PM_QAM_NONMODULUS_EQ`
  - `R3_CONVENTIONAL_COMPARATOR_OR_FOUNDATION`
  - `OUT_OF_SCOPE`
- `task_fit`：direct / adjacent / none；
- `exclusion_reason`（排除时必填）。

不能用工具的 relevance score 代替此审查。

### A4. 二轮 route-specific deep search

基于 A3 两条 direct route，分别执行：

```powershell
# 先按 A1 的原始 EOL 条件适配；w/lf 时不转换
bash tools/search `
  "convolutive independent component analysis complex QAM MIMO FIR blind equalization" `
  --mode academic --sources s2 openalex arxiv --max-per-source 20 --top 60 `
  --year-from 1990 --sort composite --format json `
  -o search-archive/2026-07-27/c16-d1-complex-convolutive-bss.json

bash tools/search `
  "coherent optical PM-QAM blind source separation cumulant joint diagonalization equalizer" `
  --mode academic --sources s2 openalex arxiv --max-per-source 20 --top 60 `
  --year-from 1990 --sort composite --format json `
  -o search-archive/2026-07-27/c16-d2-optical-cumulant-fir.json
# 若且仅若 A1 记录的原始状态为 w/crlf，此处恢复 CRLF
```

同样执行 A3 标注。若某 route 无 direct result，不能用 adjacent/general ICA
凑 route。

### A5. identity 与 candidate view

生成：

`search-archive/2026-07-27/c16-fir-hos-candidate-view.json`

冻结规则：

1. DOI 统一 lowercase/去 URL 前缀；title 用 Unicode NFKC、lowercase、
   去非字母数字得到 `normalized_title`。
2. 同 DOI 合并。无 DOI 条目只有在 normalized title、year（±1）与 first author
   一致时才并入有 DOI 条目；否则保留独立并标 `IDENTITY_UNCERTAIN`。
3. 同 normalized title 出现两个不同非空 DOI 时，不猜 alias：整组进入
   `identity_quarantine`，不计 unique/source/published/priority/route 门。
   若任一 acquisition-pool 候选落入 quarantine，则 Step 1 FAIL。
4. 每个 merged candidate 保留所有 retrieval locator、query、raw source、
   title、DOI、year、venue、publication status。
5. actual source family 按 raw singleton provenance 计数；同一 candidate
   同一 source 只计一次。空返回、query 配置和复合历史标签不得凑源。
6. published ratio 分母只用非 quarantine unique candidates；unknown 不计
   published 分子。

candidate view 必须包含：

```text
raw_rows_by_file
actual_source_families
unique_nonquarantine_count
identity_quarantine_groups
published/preprint/unknown counts and ratio
priority counts
route counts by direct/adjacent/none
8–12 paper acquisition_pool with identity and reason
all raw locator pointers
```

同时必须满足当前 `tools/download` 的批量输入契约：

```json
{
  "results": [
    {
      "id": "c16-p001",
      "title": "...",
      "authors": ["..."],
      "year": 2000,
      "venue": "...",
      "doi": "10....",
      "arxiv_id": null,
      "url": "...",
      "pdf_url": null,
      "source_api": "s2"
    }
  ],
  "candidates": [],
  "identity_quarantine": [],
  "gate_summary": {}
}
```

- 顶层 `results` **只能**放 acquisition pool 的 8–12 篇，每篇必须有稳定且
  唯一的 `id`；这是 Phase B 的 downloader view，不能把全部候选混入。
- `candidates` 保存全部非 quarantine 候选及 AI review；
  `identity_quarantine` 保存冲突组；`gate_summary` 保存 A6 所有计数。
- `results[*]` 必须保留下载器识别所需的 DOI/arXiv/URL 字段，并用
  `retrieval_provenance` 回指完整 raw locator。缺失字段显式写 `null`，不得猜测。

### A6. Step 1 hard gate

必须全部满足：

```text
actual_source_families >= 3
unique_nonquarantine_count >= 20
published_ratio >= 0.50
must_read_count >= 5
direct_route_R1 >= 1
direct_route_R2 >= 1
acquisition_pool_count in [8,12]
acquisition_pool_identity_quarantine_count == 0
```

任一失败：

```text
terminal_status=BLOCKED_SEARCH_OR_IDENTITY
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
PHASE_B_AUTHORIZED=FALSE
```

写完整 worker log 后停止，不做第六个查询、不改 gate。

---

## 4. Phase B — Groundwork Step 2

只在 A6 全 PASS 后执行。

### B0. 输入冻结

- candidate view 路径与 SHA256；
- acquisition pool 8–12 篇的 exact title、DOI/arXiv、priority、route；
- shared papers library（只读）：
  `D:\code\study\research-protocol\papers\`；
- worktree papers 路径（允许新写，gitignored）：
  `papers/{arxiv|doi|manual|downloads}/...`。

共享 main repo 只读，不得修改其 papers/index/search index。

### B1. 已有全文 census

对 acquisition pool 每篇依次查 worktree 与 shared library：

- metadata/title/DOI/arXiv identity；
- `content.md` 路径、SHA256、总行数与有效内容行；
- title 自检：metadata `title_check=mismatch` 直接 failure；缺字段时按
  `gw-read.md` 的 token-Jaccard `>=0.4` 规则核对；
- `content.md >=50` 行且不是纯标题/目录才计 valid fulltext。

已有合法全文直接计数，不重复下载。

### B2. acquisition 三轮止损

对仍缺失的 acquisition-pool 论文：

1. 第一轮：用
   `bash tools/download <candidate-view> --dry-run --only <missing-id-list>`
   核对计划；确认 dry-run 打印的条目数、ID 与缺失清单完全一致后，再执行
   `bash tools/download <candidate-view> --only <missing-id-list>`；
2. 第二轮：对失败项用 exact title 在 arXiv source 做一次检索，若得到唯一
   title/author/identity 一致版本，再用
   `bash tools/download --arxiv <id>`；
3. 第三轮：只有 IEEE DOI 且校园通道可用时，每篇最多一次用 **exact title**
   调用当前有效 CLI：
   `bash tools/blit "<exact-title>" --source ieee --max 3 --format json
   --output <receipt-json> --download
   papers/downloads/2026-07-27/c16-fir-hos/`。当前 `tools/blit` 不支持
   `--doi` 参数；DOI 只用于结果与下载 PDF 的 identity 核对。只允许把
   title/author/DOI 一致的 PDF 计入全文，其他命中保留在 receipt 中但不转换、
   不计 coverage。成功且 identity 合法的 PDF 必须用项目
   `bash tools/convert <pdf-path>` 转换，禁止自写 PDF parser。

`tools/download`、`tools/blit`、`tools/convert` 若为 CRLF，沿 A1 规则临时
LF 调用并恢复；不得修 wrapper。不得使用 webReader、ResearchGate、网页摘要
冒充全文。三轮后停止。

### B3. coverage-gap report

worker log 必须逐篇列出：

- 成功全文：title、identity、路径、SHA256、有效行数、route、发表状态；
- 内容质量 failure：路径与原因；
- 下载 failure：title、DOI/arXiv、三轮 receipt、为什么是 coverage gap；
- 正式发表/预印本/unknown 比例；
- 两条 direct route 的全文覆盖；
- 2–3 篇预期标杆写作架构候选（只列 title，不精读）；
- 是否存在 direct competitor 已占满候选包装句的 metadata-level signal；
  只能标 `REQUIRES_STEP3_ADJUDICATION`，不得在本包做 novelty verdict。

### B4. Step 2 hard gate 与停止

```text
valid_fulltext_count >= 5
valid_fulltext_direct_R1 >= 1
valid_fulltext_direct_R2 >= 1
all_counted_fulltexts_title_identity_pass == true
coverage_gap_report_complete == true
```

若失败：

```text
terminal_status=BLOCKED_FULLTEXT_COVERAGE
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
```

若通过：

```text
terminal_status=AWAITING_COVERAGE_CONFIRMATION
formal_science_disposition=FORMAL_READINESS_STEP2_COMPLETE_AWAITING_USER_GATE
mission_method_delta=NONE
STEP3_AUTHORIZED=FALSE
```

无论哪种终态，立即停止。不得精读或请求 executor 自行确认 coverage。

---

## 5. Worker log 强制格式

路径：

`projects/thesis-fso/worker-logs/step-017-c16-fir-hos-formalization.md`

必须包含：

1. `## Control validation`：命令与原始输出；
2. `## Protected-file baseline`：起飞 dirty set 与 owner/control/task SHA256；
3. `## Phase A receipts`：5 个搜索命令、exit code、wall clock、文件 size/hash、
   raw/source counts；
4. `## AI review and identity`：priority/route/identity quarantine 全计数；
5. `## Step 1 gate`：每项 PASS/FAIL；
6. `## Phase B receipts`（若授权）：existing/download/convert 每篇 receipt；
7. `## Coverage-gap report`；
8. `## Stop discipline`：证明未运行 Step3/Q#/implementation/simulation；
9. `## Git and artifact closure`：结束 git status、受保护文件 hash 对比、所有
   ignored raw artifact size/hash；
10. `## Terminal report`：

```text
terminal_status_allowed=BLOCKED_PREFLIGHT|BLOCKED_EXECUTION_TIMEBOX|BLOCKED_SEARCH_OR_IDENTITY|BLOCKED_FULLTEXT_COVERAGE|AWAITING_COVERAGE_CONFIRMATION
terminal_status=
execution_phase=A|B
formal_science_disposition=
mission_method_delta=NONE
actual_source_families=
unique_nonquarantine_count=
published_ratio=
must_read_count=
direct_route_R1=
direct_route_R2=
acquisition_pool_count=
valid_fulltext_count=
PHASE_B_AUTHORIZED=FALSE|TRUE
STEP3_AUTHORIZED=FALSE
same_axis_streak_proposed=1
repair_streak_proposed=0
no_method_streak_proposed=17
anomaly=
```

executor 只能提出 streak；最终值由独立 verifier 与主控裁决。

---

## 6. 主控验收 checklist

- [ ] task-control 与 action class PASS；
- [ ] 五次 search 都有 raw receipt，实际来源不由配置臆断；
- [ ] identity quarantine 不参与门槛，pool 无冲突身份；
- [ ] AI priority/route review 可从 raw locator 复核；
- [ ] Step 1 全门逐项可重算；
- [ ] Phase B 只在 Step 1 PASS 后启动；
- [ ] 每篇 counted fulltext 的 title/identity/content-quality 可复核；
- [ ] acquisition 严守三轮止损与 shared-main 只读；
- [ ] 没有 Step3/Q#/实现/实验；
- [ ] worker log 与 raw artifacts hash 闭合；
- [ ] executor 未修改 control/formal/current/mission/registry；
- [ ] independent verifier 分别裁决 execution integrity、
  formal science disposition、method delta、streak 与 drift。
