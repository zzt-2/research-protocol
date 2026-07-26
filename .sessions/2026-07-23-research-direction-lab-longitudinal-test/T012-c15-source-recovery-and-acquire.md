# Task Brief: C15 multi-source recovery and canonical acquisition

> 来源: S001 | 产出位置:
> `projects/thesis-fso/worker-logs/step-012-c15-source-recovery-and-acquire.md`
> 日期: 2026-07-27
> 唯一文档: 执行方只依赖本任务文件、下列明确列出的只读 owner/receipt、
> worktree 的 T011 archives/worker log，以及主仓共享 search index/papers library

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 28
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：在不降低 T011 三源门的前提下，用项目共享历史索引恢复 C15
candidate-specific 多源视图，闭合现有近期全文的 metadata/title，并且只对 Sato
1975、Godard 1980、Yang–Werner–Dumont 2002 三篇 canonical 论文各执行一次
IEEE/blit 获取。三篇 canonical 与至少两篇近期 comparator 都有效，才进入
`AWAITING_COVERAGE_CONFIRMATION`。

**产出**：

1. `search-archive/2026-07-27/c15-source-recovery-view.json`；
2. `search-archive/2026-07-27/c15-step1-acquisition-pool.json`；
3. 三个 canonical 的 blit JSON、裸 PDF/sidecar（若成功）和合法共享论文库条目；
4. worker log
   `projects/thesis-fso/worker-logs/step-012-c15-source-recovery-and-acquire.md`。

**最高纪律**：

1. 这是 T011 `BLOCKED_SEARCH_COVERAGE` 后的一次有界 source recovery，不是方法
   repair；`mission_method_delta=NONE`。
2. C15 是 blind-equalization cost/update family，不是 CPR。
3. 不运行 Step 3 精读、旧 sandbox、仿真、seed、MVE、Step 4a 或后续阶段。
4. 不猜 DOI，不把 reference list、abstract、搜索结果或临时 PDF 当 canonical
   fulltext closure。
5. 每篇 canonical 只允许一个 exact-title IEEE/blit 下载调用；任一失败即
   `BLOCKED_CANONICAL_FULLTEXT`，不得新增渠道或要求用户技术判断。
6. executor 不修改 `.sessions/**`、formal/current owner、mission-log、
   master-state、simulation/common/params 或旧任务。
7. 因单个子 agent 最长 15 分钟，本任务分成两个串行 executor phase：
   Phase A 只做 §2.1–2.3；Phase B 只做 §2.4–2.5。Phase A 写中间回执并停止，
   Phase B 只在 resume gate 通过后继续；二者之后仍须由第三个独立 verifier 验收。

---

## 1. 权威背景

允许的只读控制/receipt 输入：

- live control/topic：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
- live owner：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D013`
- formal owner：
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D024`
- T011 acceptance：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md#V029`
  与 commit `700864de9ac2d928681201312121d178ff243ccb`
- T011 worker receipt（唯一合法路径）：
  `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`
- T011 archives（恰好七个）：
  `search-archive/2026-07-26/c15-*.json`
- checkpoint：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md#CP011`
- validator 与工具：
  `research-direction-lab/scripts/validate_task_control.py`、worktree `tools/blit`、
  `tools/convert` 及其只读实现/`--help`

- formal owner:
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D024`
- live owner:
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D013`
- T011 Step 1 已由独立 verifier 接收为
  `BLOCKED_SEARCH_COVERAGE / P0=0/P1=0/P2=1 / mission_method_delta=NONE`：
  56 retained rows、53 unique、49 published，但 56/56 actual `source_api` 都是
  OpenAlex；三个关键 deep query 为 0，FSO deep 只有一篇泛 survey。
- 共享主仓索引
  `D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl`
  已存在直接相关的 Semantic Scholar、SerpAPI Scholar、OpenAlex 和 Exa 历史召回；
  T011 是当次管道覆盖失败，不是项目资产只有单源。
- 共享论文库为 `D:\code\study\research-protocol\papers\`。不得在 worktree
  创建孤立 `papers/index.json` 或共享索引副本。
- 当前无 active scientific carrier。B1/A4 禁止重复 repair，B9 未建全链；
  本包只是让 C15 恢复 formal readiness 输入。

现有直接相关全文：

| role | shared path | current debt |
|---|---|---|
| recent comparator | `papers/doi/10.1109_jlt.2025.3547459/` | title 已人工核验 |
| recent comparator | `papers/doi/10.1109_jphot.2021.3062727/` | `title_check=match` |
| coherent-FSO collision | `papers/doi/10.1109_tccn.2025.3631007/` | content 正确，metadata failed/空 title |
| FSO/JR-CMA collision | `papers/doi/10.1109_acp66871.2025.11350394/` | content 正确，metadata failed |
| coherent blind EQ | `papers/doi/10.1109_jsac.2022.3191346/` | source tar + content，metadata title 空 |

后两类 collision 只说明 Step 3 必须审创新碰撞，不在本包下方法结论。

---

## 2. 执行

### 2.1 起飞门

本任务严格串行。主控派 Phase A executor 时 worktree 必须 clean；Phase A
完成并停止后，主控才派 Phase B executor。两个 executor 都先从 worktree 根运行：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T012-c15-source-recovery-and-acquire.md
```

必须同时确认：

- task-control PASS；
- Phase A 起飞时 `git status --short` 为空；Phase B 使用下述 resume gate，
  不重复要求 clean；
- D024/D013 active；
- `git merge-base --is-ancestor
  700864de9ac2d928681201312121d178ff243ccb HEAD` exit 0；
- T011 七个 `search-archive/2026-07-26/c15-*.json` archive 与唯一合法 worker
  log `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`
  存在；不得按任务语义猜测或改写 receipt 文件名；
- 未运行 simulation/MVE/seed 进程。
- 主仓以下目标在 Phase A 起飞前无既有 diff：
  `papers/index.json`、上表五个 DOI 目录，以及
  `papers/downloads/2026-07-27/c15-*` / 本任务可能创建的 canonical target。

Phase A 的第一个动作是执行一个组合起飞门；门返回后、任何第二条命令之前，
立即用 `apply_patch` 创建 worker log 并原样记录该命令、stdout、stderr 和 exit。
非 PASS 立即停止。此后每个外部命令的 transcript 也必须立即用 `apply_patch`
追加，不得只写“exit 0”。统一分隔格式：

```text
### command N — <purpose>
command:
<exact command>
stdout:
<verbatim stdout or EMPTY>
stderr:
<verbatim stderr or EMPTY>
exit_code: <integer>
```

Phase A 最长 15 分钟，只执行 §2.1–2.3。完整结束时写：

```text
final_status=PHASE_A_COMPLETE_AWAITING_CANONICAL
formal_science_disposition=PENDING_PACKAGE_COMPLETION
mission_method_delta=NONE
```

然后停止，不执行 blit/convert。若时间耗尽但尚未闭合 §2.3，写
`BLOCKED_EXECUTION_TIMEBOX` 并停止，不把半成品冒充 Phase A complete。

Phase B 的 resume gate 必须同时满足：

- task-control 仍 PASS，D024/D013 仍 active，HEAD 仍含 `700864d`；
- worker log 精确为 `PHASE_A_COMPLETE_AWAITING_CANONICAL`；
- source view、acquisition pool 和五项 existing-fulltext closure 均已 JSON parse
  且满足 §2.2–2.3；
- worktree/main-repo diff 只包含 Phase A 预期 artifact、worker log 与五项精确
  metadata/index closure；`.sessions/**`、owners、master、simulation/common/params
  无 executor diff；
- 未调用任何 canonical blit。

Phase B 最长 15 分钟，只执行 §2.4–2.5；resume gate 的 transcript 同样立即追加。

### 2.2 Shared-index multi-source recovery

只读：

- `D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl`
- T011 七个 `search-archive/2026-07-26/c15-*.json`

用 title + abstract 严格筛选直接涉及以下对象的条目：

- CMA/MCMA/MMA/CMMA、RCA/reduced constellation、RDE/radius-directed；
- blind MIMO/dual-polarization equalization for QAM/coherent optical/FSO；
- staged/variable-step/normalized/confidence/ring-aware update。

用 `apply_patch` 创建
`search-archive/2026-07-27/c15-source-recovery-view.json`，schema：

```json
{
  "schema_version": "c15.source-recovery.v1",
  "fresh_t011_archives": [],
  "historical_index": "D:/code/study/research-protocol/search-archive/_index/all-papers.jsonl",
  "source_family_counts": {},
  "results": []
}
```

规则：

- 只复制原对象；必须保留 `source_apis`、`queries`、`key`、title、abstract、
  DOI/arXiv、venue/year/citations；
- 先为每个 retrieval record 生成 `normalized_title`：Unicode NFKC、lowercase，
  删除所有非字母数字字符；DOI 统一 lowercase；
- unique candidate identity 使用并集规则：同 DOI 必合并；同
  `normalized_title` 也必合并，即使一条有 DOI、一条无 DOI。若同一
  normalized title 出现两个不同非空 DOI，结束为 `BLOCKED_IDENTITY_CONFLICT`；
- 合并对象必须保留 `retrieval_records`（原 index line/key/source_apis/query）；
  合并后的 DOI 取唯一非空 DOI，`source_apis`/queries 只做 union；
- `source_family_counts` 统计的是 **retrieval provenance families**：拆分每条
  retrieval record 的 `source_apis`，同一 merged candidate 对同一 family 只计
  一次。`candidate_unique_count` 只统计 merged candidate，二者不得混用；
- acquisition pool 也按同一 merged identity 去重，不得把 line 19396 的 DOI
  JR-CMA 与 line 19822 的无 DOI 同题记录算成两篇；
- 至少有 20 个直接相关 unique candidates；
- 至少三个真实 source families，且必须包括
  `semantic_scholar`、`serpapi_scholar`、`openalex`；Exa 可作第四源；
- 每个 family 至少有一个 singleton provenance 直接相关条目，不能只靠合并字符串；
- 代表性复核锚：
  - shared index line 19396：JR-CMA，`semantic_scholar`；
  - line 19822：同题独立 `serpapi_scholar` 召回；
  - line 19857：likelihood-selected RDE，`openalex`；
  - line 10699：blind MIMO equalization，`exa`；
  - line 11383：multi-modulus blind equalization，`semantic_scholar`。

不足三源或 20 unique 即 `BLOCKED_SHARED_INDEX_COVERAGE`，停止，不写 acquisition
pool，不执行下载。

对 view 的每个 merged result 人工写 `priority` 与 `priority_reason`。随后用 `apply_patch`
创建 `c15-step1-acquisition-pool.json`，顶层必须为
`{"query":..., "sources":[...], "results":[...]}`，只放 8–12 个按上述 identity
规则去重后的必读/建议读 merged candidate。

### 2.3 Existing-fulltext metadata/title closure

只核验上表五个现有目录。逐篇：

1. JSON parse metadata；统计 content 有效行；核实际首个标题与 DOI。
2. 不覆盖正确 source/content。逐项合同如下：
   - JLT `10.1109_jlt.2025.3547459` 与 JPHOT
     `10.1109_jphot.2021.3062727`：metadata 已有效，不改 metadata；只把 index
     的精确 DOI key 协调为现有真实 title/status/title_check/path。
   - TCCN `10.1109_tccn.2025.3631007` 与 ACP
     `10.1109_acp66871.2025.11350394`：只有在 `source.pdf`、content title、目录
     DOI 三者一致时才协调 metadata。新增一条 `reconciliation_history`，保存
     prior `download_status=failed`、`download_method=all_failed` 与原时间；
     当前字段改为 `download_status=ok`、
     `download_method=existing-local-artifact-reconciled`、`content_type=pdf`、
     `content_file=content.md`、真实 title/real_title、`title_check=match`、
     `title_overlap=1.0`，并记录 source/content SHA256。不得删除历史字段/说明。
   - JSAC `10.1109_jsac.2022.3191346`：保留
     `download_status=success`、`download_method=arxiv_latex`、
     `content_type=latex` 和原时间，只补真实 title/real_title、
     `title_check=match`、`title_overlap=1.0`；其 index DOI key 当前不存在，
     允许在全部闭合后创建。
3. 共享 `papers/index.json` 的 exact storage contract：
   - DOI key 一律 `doi:<lowercase-doi>`；
   - path 一律为 repo-root-relative POSIX 路径
     `papers/doi/<lowercase-doi-with-slash-replaced-by-underscore>`；
   - JLT/JPHOT/TCCN/ACP 四个现有 key 只更新
     `path/doi/title/status/title_check` 并保留 `batches` 及额外历史字段；
   - JSAC 新建精确 DOI key，字段为
     `path/doi/title/status=success/batches=[]/title_check=match`；
   - 修改整个 index 前后均 JSON parse，且只允许上述五个 key 有 diff。
4. 修改前后 JSON parse。title mismatch 或 DOI 不明的条目不修、不计数。

本地近期全文只有至少两篇通过即可；不得把这一步称作方法或 canonical closure。

### 2.4 Three canonical exact-title acquisitions

每篇只执行以下一个调用。wrapper 为 CRLF，必须在 `tools/` 内用只读 `sed`：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p ../search-archive/2026-07-27 /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-sato-1975 && sed 's/\r$//' blit | bash -s -- 'A Method of Self-Recovering Equalization for Multilevel Amplitude-Modulation Systems' --source ieee --max 10 --format json -o ../search-archive/2026-07-27/c15-canonical-sato-1975.json --download /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-sato-1975"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-godard-1980 && sed 's/\r$//' blit | bash -s -- 'Self-Recovering Equalization and Carrier Tracking in Two-Dimensional Data Communication Systems' --source ieee --max 10 --format json -o ../search-archive/2026-07-27/c15-canonical-godard-1980.json --download /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-godard-1980"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-yang-2002 && sed 's/\r$//' blit | bash -s -- 'The Multimodulus Blind Equalization and Its Generalized Algorithms' --source ieee --max 10 --format json -o ../search-archive/2026-07-27/c15-canonical-yang-2002.json --download /mnt/d/code/study/research-protocol/papers/downloads/2026-07-27/c15-yang-2002"
```

对每篇：

- JSON 用 §2.2 同一 normalized-title 规则必须恰好命中一个 canonical exact-title
  record；0 个或多个 exact record 都算该 canonical 失败；
- 从该 exact record 的 IEEE URL `/document/<arnumber>/` 提取唯一 arnumber，只允许
  摄入下载目录内同名 `<arnumber>.pdf` 与 `<arnumber>.meta.json`。其他邻近命中
  即使被 `--max 10 --download` 下载也只能列为 ignored，不得摄入；
- sidecar 的 `expected_title` 规范化后必须等于 canonical exact title，PDF 必须
  有 `%PDF` 且 ≥1 KiB；转换后的 content 首标题还必须再次匹配。sidecar 自身
  `title_check` 不是充分条件；
- DOI 只有 JSON/PDF 明示才使用；否则入 `papers/manual/{title-slug}`；
- 先用 `apply_patch` 写
  `search-archive/2026-07-27/c15-canonical-ingest-plan.json`，包含实际 source PDF、
  sidecar、result pointer、title、DOI/无 DOI、target/index key/path；
- 把 PDF 精确复制为 target `source.pdf`，用 worktree `tools/convert` 转换并将
  `source.md` 精确重命名为 `content.md`；
- 用 `apply_patch` 写 metadata 并更新共享 index：
  - 有 DOI：key=`doi:<lowercase-doi>`，target=`papers/doi/<doi-slug>`，
    index path=`papers/doi/<doi-slug>`；
  - 无 DOI：本任务只允许
    `manual:c15-sato-1975`、`manual:c15-godard-1980`、
    `manual:c15-yang-2002` 三个 key，对应 target/index path
    `papers/manual/<same-slug>`；
  - metadata 必须记录 query、exact JSON record、arnumber、PDF/sidecar/result
    pointer、SHA256、title check、DOI/无 DOI 和 ingest date；
- content ≥50 有效行、title match、metadata/index parse 全部通过才计 canonical。

三篇中任一失败，立即结束为 `BLOCKED_CANONICAL_FULLTEXT`；成功的已入库条目保留，
不得再试第二渠道。

### 2.5 Final gate

允许的 `final_status` / `formal_science_disposition` 组合只有：

| 条件 | final_status | formal_science_disposition |
|---|---|---|
| shared index <20 unique 或 <3 provenance families | `BLOCKED_SHARED_INDEX_COVERAGE` | `BLOCKED_SHARED_INDEX_COVERAGE` |
| normalized-title cluster 出现不同非空 DOI | `BLOCKED_IDENTITY_CONFLICT` | `BLOCKED_IDENTITY_CONFLICT` |
| existing fulltext title/DOI/storage closure 失败 | `BLOCKED_EXISTING_FULLTEXT_IDENTITY` | 同 final_status |
| Phase A 完整、等待 Phase B | `PHASE_A_COMPLETE_AWAITING_CANONICAL` | `PENDING_PACKAGE_COMPLETION` |
| 任一 canonical exact binding/download/content closure 失败 | `BLOCKED_CANONICAL_FULLTEXT` | 同 final_status |
| 所有最终门均满足 | `AWAITING_COVERAGE_CONFIRMATION` | `FORMALIZATION_STEP1_STEP2_COMPLETE_AWAITING_COVERAGE_CONFIRMATION` |
| 任一 executor 超过 15 分钟未闭合其 phase | `BLOCKED_EXECUTION_TIMEBOX` | `PENDING_PACKAGE_COMPLETION` |

成功等待 coverage 仍不是 scientific PASS、negative/positive method verdict、
`METHOD_SIGNAL`、`PACKAGING_BOUNDARY` 或 `PROMOTION_READY`。

只有全部满足：

- candidate-specific unique ≥20；
- retrieval provenance families ≥3；
- acquisition pool 8–12 且 priority 完整；
- canonical effective fulltexts = 3/3；
- recent effective comparator/task-fit fulltexts ≥2；
- 所有计入全文 content ≥50 行、title/DOI/metadata/index 闭合；

才写：

`final_status=AWAITING_COVERAGE_CONFIRMATION`

否则写精确 blocker。无论哪种状态，均：

- `formal_science_disposition` 与 `mission_method_delta=NONE` 分开；
- 不进入 Step 3；
- 不要求用户阅读日志或判断科学正确性。

---

## 3. Worker log 格式

```markdown
# Step 012 — C15 source recovery and canonical acquisition

## Status
- task_control:
- final_status:
- formal_science_disposition:
- mission_method_delta: NONE
- simulation_or_seed_run: false

## Raw command transcripts and exits
## Multi-source recovery audit
## Candidate table and acquisition pool
## Existing-fulltext closure
## Canonical acquisition audit
## Coverage gap report
## Novelty collision flags
## Integrity boundaries
## Next gate
```

技术详情全部写入此日志；不得只在聊天回复。

---

## 4. 验收

- [ ] task-control PASS，起飞前 worktree clean。
- [ ] ≥20 unique、≥3 actual source families，provenance 没重复计数。
- [ ] acquisition pool 8–12，priority/priority_reason 完整。
- [ ] 现有全文只做可证 metadata/title closure，不覆盖 source/content。
- [ ] 三篇 canonical 各只调用一次 exact-title blit。
- [ ] canonical 3/3、recent ≥2 才到 coverage confirmation。
- [ ] 失败立即止损，不新增下载渠道。
- [ ] 未运行 Step 3/仿真/MVE/seed，未改 owners/sessions/master/mission-log。
- [ ] `mission_method_delta=NONE`，未把检索/下载/metadata repair 写成方法产出。
