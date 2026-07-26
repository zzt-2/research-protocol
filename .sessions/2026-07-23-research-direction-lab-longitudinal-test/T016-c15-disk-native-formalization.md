# Task Brief: C15 disk-native Step 1–2 formalization

> 来源: S001 / R006 / D020 / formal D031
> 产出位置:
> `projects/thesis-fso/worker-logs/step-016-c15-disk-native-formalization.md`
> 日期: 2026-07-27
> 执行方式: 仅由本 Goal 内部 executor 执行；用户不转发、不读日志、不判断科学正确性

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 40
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP015
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
中，用已有 T011 七份搜索 archive、项目 shared index 和 shared papers library，
一次性闭合 C15 的 Groundwork Step 1–2 formal readiness：

1. 形成 actual-source ≥3、去重 ≥20、正式发表 ≥50%、必读 ≥5、覆盖 ≥2
   技术子方向的 candidate view；
2. 形成 8–12 篇“必读/建议读” acquisition pool；
3. 核对五项 recent fulltext identity/content quality；
4. 对 Sato 1975、Godard 1980、Yang–Werner–Dumont 2002 各进行一次 bounded
   exact-title canonical staging；
5. 生成 preliminary coverage-gap report 后停止；T016 不写 shared main repo，
   通过后另建受控 canonical-promotion package。

本包不是方法包，冻结：

```text
formal_active_scientific_carrier=NONE
mission_method_delta=NONE
no_seed=true
no_simulation=true
no_step3=true
```

任何硬门失败都按 `BLOCKED_FORMAL_READINESS` 收口；不得修 T012、降低门槛、
增加搜索/下载轮次或转入实验。

---

## 1. 权威输入与边界

### 1.1 控制面

- live control：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
- live owner：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D020`
- formal owner：
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D031`
- remap：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/R006-post-b12-carrier-remap.md`
- framework：
  `stages/gw-search.md`、`stages/gw-acquire.md`
- T011 receipt：
  `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`
- T012 只作失败事实：
  `projects/thesis-fso/worker-logs/step-012-c15-source-recovery-and-acquire.md`
  （不得复用其复杂 preflight 或继续 amendment）

### 1.2 T011 archives（必须恰好七份）

```text
search-archive/2026-07-26/c15-broad-cma-mma.json
search-archive/2026-07-26/c15-broad-rca-sato.json
search-archive/2026-07-26/c15-broad-rde-optical.json
search-archive/2026-07-26/c15-deep-fso-taskfit.json
search-archive/2026-07-26/c15-deep-lineage.json
search-archive/2026-07-26/c15-deep-normalized-cost.json
search-archive/2026-07-26/c15-deep-staged-optical.json
```

shared index（冻结输入）：

```text
D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl
size=39099216
sha256=7530fa6fb9ae0234eee8d98902c8bcc936e278401dc61d0daded300542a4d27a
```

shared index 只能按记录内真实 `source_apis`、`queries`、title、abstract、DOI、
venue、year、publication status 使用。不得从文件名、搜索渠道配置或历史叙述推断
来源；同一论文多源命中须 identity merge，不得重复计数。

### 1.3 五项 recent fulltext

只读 shared library 根：
`D:\code\study\research-protocol\papers\`

| role | exact target |
|---|---|
| recent comparator | `doi/10.1109_jlt.2025.3547459/` |
| recent comparator | `doi/10.1109_jphot.2021.3062727/` |
| coherent-FSO collision | `doi/10.1109_tccn.2025.3631007/` |
| FSO/JR-CMA collision | `doi/10.1109_acp66871.2025.11350394/` |
| coherent blind-EQ comparator | `doi/10.1109_jsac.2022.3191346/` |

对每项核对目录、`content.md`、title、DOI、metadata/index identity；逐篇记录
有效行数，`content.md < 50` 或只有标题/目录时视为 failure。可以在 Phase A
报告 metadata/index 债，但不得擅自改 shared recent 目录。

### 1.4 三篇 canonical

| id | exact title | DOI | IEEE arnumber / document URL |
|---|---|---|---|
| Sato 1975 | A method of self-recovering equalization for multilevel amplitude-modulation systems | `10.1109/TCOM.1975.1092854` | `1092854` / `https://ieeexplore.ieee.org/document/1092854/` |
| Godard 1980 | Self-recovering equalization and carrier tracking in two-dimensional data communication systems | `10.1109/TCOM.1980.1094608` | `1094608` / `https://ieeexplore.ieee.org/document/1094608/` |
| Yang–Werner–Dumont 2002 | The multimodulus blind equalization and its generalized algorithms | `10.1109/JSAC.2002.1007381` | `1007381` / `https://ieeexplore.ieee.org/document/1007381/` |

上述身份由独立 metadata audit 冻结：三次 exact-title IEEE 查询均得到唯一
normalized-title 命中，且每个 DOI 的 `doi.org` 302 `Location` 精确指向同一
IEEE document URL。`tools/blit.py` 的 IEEE JSON 设计上固定返回 `doi=""`，
PDF sidecar 也不含 DOI；因此 DOI 是事先审计的 bibliographic binding，运行时
不得要求 JSON/sidecar 返回 DOI，也不得把 DOI 回填进原始查询结果冒充工具字段。

canonical acquisition 只能在 Phase B 执行；每篇最多一个 exact-title IEEE
检索+下载调用。T016 只写 worktree 的合法 staging 路径
`papers/downloads/2026-07-27/c15-*/` 与
`search-archive/2026-07-27/`，**禁止修改**
`D:\code\study\research-protocol` 主仓 shared papers/index。若下载成功，必须用
项目 `tools/convert` 在 staging 目录转换；若失败，原样记录
exit/stdout/stderr/产物状态后停止该篇，不换渠道、不用
webReader/ResearchGate、不伪造 metadata。staging PASS 不等于 shared-library
canonical closure；只有独立验收后另建的 promotion package 才能入主仓。

---

## 2. 执行分相

单个子 agent 最长 15 分钟。本任务按严格串行 executor turn 执行：

1. Phase A：一个 executor turn；
2. Phase B-Sato、B-Godard、B-Yang：三个独立 executor turn，每 turn 只处理
   一篇 canonical；
3. Phase C：一个 disk-only synthesis turn；
4. 最后由未参加执行的独立 verifier 统一科学验收。

每个 executor turn 必须记录 wall-clock 起止；到 12 分钟仍未闭合当前原子任务，
立即写 `BLOCKED_EXECUTION_TIMEBOX` 并停止，禁止靠单次 turn 超过 15 分钟完成。

### Phase A — disk-native Step 1 view + recent identity

#### A0 起飞门

从 worktree 根执行并在 worker log 原样记录：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T016-c15-disk-native-formalization.md
git status --short
```

必须同时满足：

- task-control PASS；
- D020、D031 为 active，D019、D030 为 superseded；
- worktree clean；
- 七份 T011 archive、T011/T012 receipts、shared index、五个 recent target
  均存在；
- shared index size 与 SHA256 精确匹配 §1.2；
- 没有 simulation/MVE/seed 进程；
- current control 为 epoch 40 / CP015 /
  `C15_FORMALIZATION_PHASE_A_READY`。

任一失败：只写 worker log，状态
`BLOCKED_PREFLIGHT / mission_method_delta=NONE` 后停止。

#### A1 建立 candidate view

读取七份 T011 archive 与 shared index，按以下冻结规则做 provenance 与 identity
merge：

- `normalized_title`：Unicode NFKC、lowercase、删除所有非字母数字字符；
  DOI lowercase；
- 同 DOI 必合并；同 normalized title 也必合并，即使一条有 DOI、一条无 DOI；
  同一 normalized title 出现两个不同非空 DOI 时，立即
  `BLOCKED_IDENTITY_CONFLICT`；
- 合并对象必须保留每条 retrieval record 的 archive/index key、query 与原始
  `source_api/source_apis`；
- source family alias：`s2`、`semanticscholar` 统一为
  `semantic_scholar`；`serpapi`、`google_scholar` 统一为
  `serpapi_scholar`；`open_alex` 统一为 `openalex`；
- `a+b` 复合 provenance 必须按 `+` 拆成 atomic family，去空格、规范别名；
  同一 merged candidate 对同一 atomic family 只计一次；复合字符串本身绝不
  算一个新 family；
- 三源门必须至少包含 `semantic_scholar`、`serpapi_scholar`、`openalex`；
  Exa/IEEE 可作额外源；
- 每个被计数 family 必须至少有一条**直接相关 singleton retrieval**，即该原始
  retrieval record 规范化后恰好只有该一个 atomic family。只出现在复合 provenance
  中的 family 不计入三源门；
- `candidate_unique_count` 只统计 merged identity；`source_family_counts`
  统计 retrieval provenance，二者不得混用；
- 代表性锚必须复核：shared index 中 JR-CMA 的独立 semantic_scholar 与
  serpapi_scholar 召回、openalex likelihood-selected RDE，以及
  semantic_scholar MMA；按 key/title 查找，不凭可能漂移的行号猜对象。

只纳入与下列至少一个 route 直接相关的记录：

1. square-QAM CMA/MMA/RDE/reduced-constellation cost；
2. staged/dual-mode/switching blind equalization；
3. coherent optical/FSO dual-polarization blind equalization；
4. cost normalization、adaptive step 或 collapse recovery；
5. direct competing learned/VAE/JR-CMA equalizer。

每条输出至少包含：

```json
{
  "identity_key": "doi:... or title:...",
  "title": "...",
  "doi": "... or null",
  "year": 2025,
  "venue": "...",
  "publication_status": "published|preprint|unknown",
  "actual_source_families": ["openalex", "semantic_scholar"],
  "singleton_source_families": ["openalex"],
  "matched_routes": ["staged_switching"],
  "priority": "必读|建议读|待确认|备选|排除",
  "priority_reason": "...",
  "source_records": ["T011 archive path or shared-index line/key"]
}
```

输出：

`search-archive/2026-07-27/c15-formalization-candidate-view.json`

顶层 summary 必须计算并列出：

- raw rows、unique identities；
- actual source family 集合及 count；
- 每个 atomic family 的 singleton retrieval 数量与代表 key；
- published/preprint/unknown 数量和正式发表比例；
- 各 priority 数量；
- route coverage 数量；
- T011-only、shared-index-only、merged-multisource 数量；
- 每项质量门的 PASS/FAIL，不只给总 PASS。

门槛：unique ≥20、actual source family ≥3、published ratio ≥50%、
必读 ≥5、route coverage ≥2。任一失败立即写
`BLOCKED_SEARCH_COVERAGE`；不进入 A2/Phase B。

#### A2 形成 acquisition pool

从 candidate view 的“必读+建议读”中选 8–12 篇，必须包含：

- ≥2 篇 2023–2026 recent direct comparator；
- ≥1 篇 staged/switching comparator；
- ≥1 篇 coherent optical/FSO task-fit；
- ≥1 篇 learned/VAE/JR-CMA collision；
- 三篇 canonical 另列为 lineage anchors，不占 8–12 recent pool 配额。

输出：

`search-archive/2026-07-27/c15-step1-acquisition-pool.json`

每篇写选择理由、source identity、现有 fulltext 状态和 Step 3 预期角色。
不得因为本地已有全文而提高科学 priority。

#### A3 recent identity/content report

输出：

`search-archive/2026-07-27/c15-recent-fulltext-identity.json`

逐项记录五个 exact target 的：

- title、DOI、metadata/index identity；
- `content.md` 是否存在、有效行数、质量 PASS/FAIL；
- 是否进入 acquisition pool；
- 未闭合债务与其对 Step 3 的影响。

Phase A 结束时 worker log 必须写：

```text
phase_a_status=PHASE_A_COMPLETE_AWAITING_PHASE_B
formal_science_disposition=PENDING_PACKAGE_COMPLETION
mission_method_delta=NONE
```

若 A1 门失败，改为：

```text
phase_a_status=BLOCKED_SEARCH_COVERAGE
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
```

并停止，不派 Phase B。

### Phase B — three bounded canonical staging turns

#### B0 resume gate

每个 canonical turn 必须由 Phase A 之外的 executor 执行。起飞前核对：

- task-control 仍 PASS，D020/D031 仍 active；
- Phase A worker status 精确为
  `PHASE_A_COMPLETE_AWAITING_PHASE_B`；
- candidate view、pool、recent identity 三个 JSON 均 parse；
- A1 五项质量门全部 PASS；
- worktree 累积 diff 只允许下列 T016 产物：
  - Phase A 的
    `c15-formalization-candidate-view.json`、
    `c15-step1-acquisition-pool.json`、
    `c15-recent-fulltext-identity.json` 与 step-016 worker log；
  - 每个已完成 canonical slug 的
    `search-archive/2026-07-27/<SLUG>-ieee.json`、
    `search-archive/2026-07-27/<SLUG>-staging-receipt.json`、
    `papers/downloads/2026-07-27/<SLUG>/*.pdf`、
    `papers/downloads/2026-07-27/<SLUG>/*.meta.json` 和
    `papers/downloads/2026-07-27/<SLUG>/converted/*.md`；
  - 不允许 `.sessions/**`、control/formal owner、mission-log、master/current
    projections、simulation/common/params、旧任务或旧 worker log 产生新 diff；
- shared index size/hash 仍匹配冻结值；
- 主仓 `D:\code\study\research-protocol` 只读；三个 canonical target 起飞前
  无既有 diff，且本 phase 不允许产生任何主仓 diff。

任一失败：追加 `BLOCKED_RESUME_GATE` 并停止。

#### B1 每个 canonical turn 的冻结命令

每个 turn 只从下表取自己的一行：

| turn | exact title | slug |
|---|---|---|
| B-Sato | `A method of self-recovering equalization for multilevel amplitude-modulation systems` | `c15-sato-1975` |
| B-Godard | `Self-recovering equalization and carrier tracking in two-dimensional data communication systems` | `c15-godard-1980` |
| B-Yang | `The multimodulus blind equalization and its generalized algorithms` | `c15-yang-2002` |

tracked wrapper 为 CRLF，使用项目既有的 WSL 去 CRLF 入口；从 worktree
`tools/` 目录执行，禁止改写 CLI：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' blit | bash -s -- '<EXACT_TITLE>' --source ieee --max 1 --format json --output '../search-archive/2026-07-27/<SLUG>-ieee.json' --download '../papers/downloads/2026-07-27/<SLUG>'"
```

该 CLI 的冻结语义来自 `tools/blit.py`：query 是 positional 参数，
`--source ieee` 必填，`--download` 接目录；不存在 `--doi` flag。

调用后立即记录 command/stdout/stderr/exit、JSON/PDF/sidecar 精确路径、大小与
sha256。下载成功也必须先过 0/1 identity 门：

- JSON parse，且返回结果数恰好 1；
- 唯一结果的 normalized title 与本 turn exact title 精确一致；
- 唯一结果 URL 中 `/document/<arnumber>` 与 §1.4 冻结 arnumber 精确一致；
- JSON 的空 DOI 是工具已知语义，不作 PASS 证据；若意外返回非空 DOI，则必须
  与 §1.4 冻结 DOI 一致，否则 `BLOCKED_CANONICAL_IDENTITY`；
- PDF 文件名必须为 `<arnumber>.pdf`，且与唯一 result URL 和 §1.4 一致；
- PDF sidecar 的 `expected_title` 与 query title 规范化后一致，
  `real_title` 与 §1.4 exact title 规范化后一致，且 `title_check` 不得为
  `mismatch` 或空缺；
- staging 目录恰好一个非空 PDF 和一个对应 sidecar。

任一不满足即本 turn `BLOCKED_CANONICAL_IDENTITY`，不转换。全部满足后，才把
唯一 PDF 的精确路径代入：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' convert | bash -s -- '<EXACT_PDF_PATH_RELATIVE_TO_TOOLS>' -o '../papers/downloads/2026-07-27/<SLUG>/converted'"
```

转换后检查唯一 markdown 有效行数 ≥50，并用 `apply_patch` 创建：

`search-archive/2026-07-27/<SLUG>-staging-receipt.json`

receipt 必须包含 exact title/DOI、query JSON/PDF/sidecar/markdown 的路径、
IEEE arnumber/document URL、`doi_binding_source=V044_METADATA_AUDIT`、
size/sha256/line count、command exit、elapsed seconds、主仓 target diff
before/after（必须均为 0）和
`status=STAGED_CANONICAL_FULLTEXT_NOT_PROMOTED`。每篇只有一次 blit 调用；
失败后不得重试或换源。

每个 turn 结束时还必须在 worker log 写一个且仅一个终态：

```text
phase_b_<slug>_status=STAGED_CANONICAL_FULLTEXT_NOT_PROMOTED
# 或
phase_b_<slug>_status=BLOCKED_CANONICAL_IDENTITY
# 或
phase_b_<slug>_status=BLOCKED_EXECUTION_TIMEBOX
mission_method_delta=NONE
```

### Phase C — disk-only preliminary coverage synthesis

Phase C 不运行网络、下载或转换。它读取 Phase A 三个 JSON、三个 canonical
turn 的明确终态与 staging receipt（失败时可无 receipt）并输出：

`search-archive/2026-07-27/c15-step2-preliminary-coverage-gap-report.md`

必须按 `gw-acquire.md` 包含：

- 成功 staging 与内容质量 PASS 的标题列表；
- 内容质量不达标列表及原因；
- 下载失败标题、DOI、来源和科学重要性；
- 来源/技术路线覆盖偏差；
- 正式发表、预印本、unknown 统计；
- 五项 recent + 三篇 canonical 的 8 项矩阵，并区分
  `SHARED_RECENT_CLOSED`、`STAGED_NOT_PROMOTED`、`FAILED`；
- 明确写 `CANONICAL_PROMOTION_REQUIRED=true`；
- 明确写 `COVERAGE_CONFIRMATION_REQUIRED=true`，但 T016 不能请求该确认，
  因为 canonical promotion 尚未完成。

最终状态：

- 若 Step 1 所有门 PASS、recent core ≥5 且 canonical 3/3 staging
  content-quality PASS：

```text
final_status=AWAITING_CANONICAL_PROMOTION
formal_science_disposition=AWAITING_CANONICAL_PROMOTION
mission_method_delta=NONE
```

- 否则：

```text
final_status=BLOCKED_FORMAL_READINESS
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
```

无论哪种状态都立即停止；不得写 shared main repo、不得请求 coverage
confirmation、不得进入 Step 3。`AWAITING_CANONICAL_PROMOTION` 只能触发主控
另建受控 promotion package，不能由 executor 原地扩范围。

---

## 3. Worker log 最低字段

`projects/thesis-fso/worker-logs/step-016-c15-disk-native-formalization.md`
必须包含：

1. worktree、HEAD、phase executor 身份与起止时间；
2. control epoch/checkpoint、D020/D031 状态；
3. 每个命令的原样 command/stdout/stderr/exit；
4. 每个新/改文件的路径、sha256、用途；
5. Step 1 五项门的独立数值与 PASS/FAIL；
6. recent/canonical 8 项矩阵，明确 staged 与 promoted 的区别；
7. `formal_science_disposition`；
8. `mission_method_delta=NONE`；
9. 明确声明未运行 seed/MVE、未精读、未写 Q#、未进入 Step 3。

executor 不修改 `.sessions/**`、control/formal owner、mission-log、
master-state、direction-lab current views、simulation/common/params、旧任务或旧
worker log。只有主控和独立 verifier 可以接收并更新这些 owner。

---

## 4. 独立验收合同

Phase A/B/C executor 之外的 verifier 必须：

1. 从原始七 archive + shared index 重算 unique/source/priority/route/published
   统计；
2. 抽查所有 8–12 pool 条目的 title/DOI/source/priority；
3. 从 shared papers 重新检查五项 recent；从 worktree staging 重新检查三项
   canonical 的 identity、content 行数和 hash，并确认主仓未被修改；
4. 核对 blit/convert transcript 与实际产物；
5. 核对没有 seed、simulation、Step 3/Q# 或旧 C15 experiment diff；
6. 独立给出
   `formal_science_disposition`、`mission_method_delta=NONE`、
   package weight、no-method/repair/same-axis streak 与 drift；
7. 不把 Step 1/2 PASS、canonical staging 或 coverage confirmation 写成
   `METHOD_SIGNAL`。

验收前不得更新 CP016；验收后由主控决定：

- `AWAITING_CANONICAL_PROMOTION`：主控另建受控 promotion package；promotion
  独立验收并形成正式 coverage-gap report 后，才向用户请求极短覆盖面授权；
- `BLOCKED_FORMAL_READINESS`：C15 返回池且不得第二个 source package，自动
  remap 新 mechanism family。
