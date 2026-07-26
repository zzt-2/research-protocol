# Task Brief: B9 virtual-carrier self-coherent + DRE Step 1 evidence adapter

> 来源: S001 | 产出位置:
> `projects/thesis-fso/worker-logs/step-013-b9-step1-evidence-adapter.md`
> 日期: 2026-07-27
> 唯一文档: 执行方只依赖本任务文件、指定的仓库公开资产和项目工具

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 32
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：只完成 B9 virtual-carrier self-coherent + Digital Resolution Enhancer
候选的 Groundwork Step 1。用已有共享索引/全文锚和七组多源检索，建立可审计的
candidate-specific evidence view，裁决它是否值得进入 Step 2 acquire。

**产出**：

1. `search-archive/2026-07-27/` 下七个由 `tools/search` **自动存档**的原始 JSON；
2. `search-archive/_index/all-papers.jsonl`：从主仓共享索引复制后由七次搜索自动
   增量更新的 worktree 本地缓存；
3. `search-archive/2026-07-27/b9-step1-candidate-view.json`；
4. worker log
   `projects/thesis-fso/worker-logs/step-013-b9-step1-evidence-adapter.md`。

**允许的最终状态**：

- `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE`；
- `BLOCKED_SEARCH_COVERAGE`；
- `STEP1_NO_DISTINCT_PROBLEM_FOUND`。

三种状态的 `mission_method_delta` 都必须为 `NONE`。Step 1 PASS 不是方法信号。

**最高纪律（违反一条即停止）**：

1. 只做 Step 1。不得下载/转换全文，不得进入 Step 2/3/3.5/4a/MVE，不得实现
   DRE、DC-Value、virtual-carrier 或运行仿真、seed、测试矩阵。
2. B9 的现有约 3/1/0.5 dB 是同一 virtual-carrier 架构下 DRE vs. RO 的
   3/4/5-PNOB SNR 对照；不得写成相对传统 coherent CPR 的优势。
3. 42 m outdoor FSO 不等于星地深湍流；必须把场景迁移、因果/可部署输入和
   comparator debt 分开记录。
4. 不把旧 read-note、abstract、search metadata 或内部对照当 formal Step 3、
   M-C-A 结论、science Go/Kill 或 `METHOD_SIGNAL`。
5. executor 只写本 T 指定的七个自动 archives、本地 `_index/all-papers.jsonl`、
   candidate view 和 worker log；
   不修改 control、formal owner、mission-log、S/R/D/V/topic-index、
   master-state/current projections、共享论文库或旧研究资产。
6. 每个子 agent phase 最长 15 分钟；A1/A2/A3-n/A4 串行，不并发写。每 phase
   结束后必须停，由主控从磁盘确认再派下一 phase。A3-n 每次最多审查两个 archive。

---

## 1. 背景

### 1.1 当前权威状态

- formal owner:
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D026`
- live owner:
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D015`
- current control: epoch 32 / CP012 / `B9_STEP1_FORMALIZATION`
- 当前仍无 active scientific carrier。B9 只是
  `HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE`。
- T012/C15 是 `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`；不得把它写成
  C15 science negative。B1/A4/B10 的重复 repair 继续禁止。

### 1.2 已有锚，只能作为 Step 1 输入

主仓共享资产：

- `D:\code\study\research-protocol\papers\doi\10.1109_jlt.2023.3270673\metadata.json`
- `D:\code\study\research-protocol\papers\doi\10.1109_jlt.2023.3270673\content.md`
- `D:\code\study\research-protocol\papers\_read_notes\_B9-virtual-carrier-dre-increment.md`
- `D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl`
- `D:\code\study\research-protocol\papers\index.json`

worktree 旧提取：

- `.sessions/2026-07-02-carrier-sync-v2-deep-read/S005-conversation3-b8b9b10-eval.md`
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b8b9-self-coherent.md`
- `projects/thesis-fso/literature_notes.md`

已有锚只证明：

- JLT 2023 title/DOI/accepted fulltext 闭合；
- virtual carrier、low-resolution DAC、DRE、DC-Value 与 42 m FSO 实验存在；
- DRE-vs-RO 有正向 SNR 锚。

它们不证明：

- 当前 formal Step 1–3 已完成；
- 星地深湍流 M-C-A 成立；
- DRE canonical/DC-Value/virtual-carrier lineage 已闭合；
- EFNS/TQNS/其他传统 noise-shaping comparator 已公平覆盖；
- 任何具体自适应输入或算法可部署。

### 1.3 本 Step 1 要裁决的两条机制路线

**Route A — low-resolution DAC quantization/noise shaping**

- DRE canonical 与后续优化血缘；
- RO、DRE、error-feedback noise shaping、trellis/quantization-noise shaping 等
  传统/邻近 comparator；
- 低 PNOB coherent/self-coherent optical 中的复杂度—性能边界。

**Route B — self-coherent/virtual-carrier FSO task fit**

- virtual/optical carrier、KK/DC-Value/self-homodyne 等架构血缘；
- FSO/星地/湍流下 CSPR、minimum-phase、phase reconstruction 与硬件复杂度问题；
- 是否已有工作直接覆盖“星地低比特自相干 + DRE/量化整形”。

只有至少一条 route 的定向深搜同时证明：存在明确传统 comparator、候选问题不是
初始漏召、且尚未被直接竞争工作完整覆盖，才允许 Step 1 PASS。否则如实返回
`STEP1_NO_DISTINCT_PROBLEM_FOUND`，但不能作 family Kill。

---

## 2. 执行方式

### 2.1 唯一起飞门

在 worktree 根运行：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T013-b9-step1-evidence-adapter.md
git status --short
rg -n -A 6 "^## D026:|^## D015:|^> status: active" `
  .sessions/2026-07-06-step4a-mve-execution/decisions.md `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md
```

要求：

- validator 输出 `PASS`；
- `git status --short` 为空；
- D026 与 D015 均为 active；
- `search-archive/2026-07-27` 不存在；若已存在任何文件则停止，不删除、不覆盖；
- 不自行新增 process/CIM/receipt/ancestry preflight。当前任务不运行实验，禁止范围
  由输出路径和 diff 验收，不再复刻 T012 的自定义 task-interface。

任一项失败立即写 worker log 为 `BLOCKED_PREFLIGHT` 并停止。

### 2.2 Phase A1（≤15 分钟）— 本地索引种子 + 三组 broad search

先把主仓完整共享索引复制为 worktree 本地忽略缓存。`tools/search` 会无条件自动
存档，并自动更新这个本地索引；这是已授权的标准副作用：

```powershell
New-Item -ItemType Directory -Force 'search-archive\_index' | Out-Null
Copy-Item -LiteralPath `
  'D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl' `
  -Destination 'search-archive\_index\all-papers.jsonl'
```

随后只运行以下三条命令。bash wrapper 为 CRLF，只读去除 `\r`，不得改工具文件。
**禁止使用 `-o/--output`**：`tools/search` 已自动存档，额外 `-o` 会生成重复文件。

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'virtual carrier self coherent free space optical digital resolution enhancer' --mode academic --preset problem-driven --max-per-source 20 --top 30"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'low resolution DAC quantization noise shaping coherent optical DRE' --mode academic --preset problem-driven --max-per-source 20 --top 30"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'Kramers Kronig DC Value self coherent FSO virtual carrier' --mode academic --preset scenario-method --max-per-source 20 --top 30"
```

逐个记录完整命令、exit code、`[存档]` 输出的**实际唯一 archive 路径**、工具报告
的 source family 与返回量，以及 `_index` 更新行。A1 不做逐条语义审查。

A1 只更新 worker log 到：

```text
final_status: PARTIAL_A1_AWAITING_A2
mission_method_delta: NONE
```

不得创建最终 candidate view，不得运行 A2，不得 commit。向主控只回传 status、
worker-log path 和一行异常，然后停止。

### 2.3 Phase A2（≤15 分钟）— 四组 directional deep search

只有主控从磁盘确认 A1 三个 archive 可 parse、没有越界 diff 后，才由不同 executor
运行以下四条：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'error feedback noise shaping EFNS low resolution DAC coherent optical' --mode academic --preset comparison --max-per-source 20 --top 30"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'trellis quantization noise shaping low resolution optical DAC digital resolution enhancement' --mode academic --preset comparison --max-per-source 20 --top 30"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'satellite ground self coherent FSO turbulence virtual carrier CSPR' --mode academic --preset comparison --max-per-source 20 --top 30"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'free space optical turbulence self coherent detection low complexity phase reconstruction' --mode academic --preset comparison --max-per-source 20 --top 30"
```

只记录四条命令、exit、实际 `[存档]` 路径、source returns 与 `_index` 更新。
验证同日目录恰有七个本 T query 对应的自动 archives，没有 `-o` 重复文件；不做
逐条审查、不创建 view。更新 worker log 为
`PARTIAL_A2_AWAITING_SEMANTIC_REVIEW` 后停止。

### 2.4 Phase A3-n（每次 ≤15 分钟）— 原 archive AI 语义审查

由一个或多个不同 executor **串行**完成。每个 A3-n 最多处理两个尚未审查的
archive；七个 archive 至多四个 A3-n phase。对该 archive 的**每条结果**读取
title、abstract、venue、year、citation count、publication status，综合判断并用
`apply_patch` 把以下字段写回该自动 archive 的原 result 对象：

- `priority`：必读/建议读/待确认/备选/排除；
- `priority_reason`：一条可审计语义理由；
- `route`：A_lowres_noise_shaping / B_selfcoherent_fso_taskfit / BOTH / NONE；
- `collision_role`：canonical/comparator/direct-competitor/task-fit/adjacent/
  false-positive；
- `evidence_scope`：本阶段默认 METADATA_ONLY；只有 B9 锚的磁盘 fulltext
  title/DOI 精确匹配时可写 EXISTING_FULLTEXT。

不得用 relevance score 批量代替人工审查，不得补造原 metadata。每个 phase
完成后 JSON parse，worker log 记录已审 archive 与每类 priority 数量，状态写
`PARTIAL_A3_REVIEW_IN_PROGRESS`；七个 archive 全部逐条有
`priority/priority_reason` 后才允许 A4。

### 2.5 Phase A4（≤15 分钟）— 去重、candidate view 与 Step 1 判定

将七个**已标注原 archive**与 worktree 本地
`search-archive/_index/all-papers.jsonl` 合并审查。本地索引只补 provenance；
不能把 `semantic_scholar+openalex` 之类合并字符串重复计为两个独立 source。
对同一 DOI/title 去重，但保留真实 source family 和原 archive/line pointer。

使用 `apply_patch` 创建
`search-archive/2026-07-27/b9-step1-candidate-view.json`，schema：

```json
{
  "schema_version": "b9.step1-candidate-view.v1",
  "candidate": "B9 virtual-carrier self-coherent + DRE",
  "generated_at": "2026-07-27",
  "source_archives": [],
  "source_families": [],
  "route_summary": {
    "A_lowres_noise_shaping": {},
    "B_selfcoherent_fso_taskfit": {}
  },
  "results": [],
  "coverage": {},
  "acquisition_debt": [],
  "step1_disposition": ""
}
```

`results` 每项至少保留：

- id/key、title、abstract、year、venue、citation count、publication status；
- DOI/arXiv；
- `source_families` 与 `source_pointers`；
- `route`；
- `priority`：必读/建议读/待确认/备选/排除；
- `priority_reason`；
- `evidence_scope`：METADATA_ONLY 或 EXISTING_FULLTEXT；
- `collision_role`：canonical/comparator/direct-competitor/task-fit/adjacent/false-positive。

不得人工补造原 archive 没有的 metadata。已有 B9 fulltext 可标
`EXISTING_FULLTEXT`，其他候选只有磁盘 `content.md` 且 title/DOI 对上时才能如此
标记。

### 2.6 Step 1 判定

PASS 必须同时满足：

- 去重后非排除 candidates ≥20；
- 至少 3 个真实 source families；
- Route A 与 Route B 均有独立 broad + deep evidence；
- 必读 ≥5；
- 正式发表文献占非排除候选 ≥50%；
- 每条均有人工 `priority/priority_reason`；
- 至少一条 route 的 deep search 明确支持一个未被直接竞争完整覆盖的问题假设；
- acquisition debt 明确列出 8–12 篇 Step 2 目标，并区分：
  DRE canonical、DC-Value/virtual-carrier lineage、传统 noise-shaping comparator、
  self-coherent/FSO task-fit。

若数量/来源/路线门不达标：
`BLOCKED_SEARCH_COVERAGE`。

若门槛达标但两条 route 均已被直接竞争完整覆盖，或没有可陈述的星地 task-fit
问题：
`STEP1_NO_DISTINCT_PROBLEM_FOUND`。

两种非 PASS 都只返回 remap，不作 B9 family Kill。

### 2.7 禁止与停止

- 不调用 web search/web reader；只用项目 `tools/search` 和磁盘资产。
- 不使用 `tools/search -o/--output`；只接收工具自动 archive 与自动本地 index
  增量，不创建重复命名文件。
- 不下载、转换、修改
  `D:\code\study\research-protocol\papers\**` 或 `papers/index.json`。
- 不读取整篇新论文；只有 B9 既有 fulltext 可作锚，其他候选只看检索 metadata。
- 不运行任何 Python 仿真/测试/seed/MVE。
- 不修改 `.sessions/**`、master/current owners、common/params/Skill/旧任务。
- 任一命令需要私有凭据、非授权网络工具或超 15 分钟，保留 partial evidence 后停止。

---

## 3. worker log 格式

```markdown
# Step 013 — B9 Step 1 evidence adapter

## Status
- task_control: PASS/FAIL
- phase: A1 | A2 | A3-n | A4
- final_status: PARTIAL_A1_AWAITING_A2 | PARTIAL_A2_AWAITING_SEMANTIC_REVIEW | PARTIAL_A3_REVIEW_IN_PROGRESS | FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE | BLOCKED_SEARCH_COVERAGE | STEP1_NO_DISTINCT_PROBLEM_FOUND
- formal_science_disposition: ...
- mission_method_delta: NONE
- simulation_or_seed_run: false

## Exact commands and exits

## Input-anchor audit
| asset | identity/title/DOI check | allowed evidence scope |

## Search-source audit
| archive | query | actual source family | returned | parse |

## Deduplicated coverage
- nonexcluded_unique:
- actual_source_families:
- route_A_count:
- route_B_count:
- must_read:
- formally_published:
- published_ratio:

## Candidate table
| id | title | year/venue | source | route | priority | collision role | reason |

## Route A — low-resolution DAC/noise shaping

## Route B — self-coherent/FSO task fit

## Direct-competition and gap adjudication

## Acquisition debt
| role | exact title/id | why Step 2 needs it | current availability |

## Integrity boundaries

## Next gate
只写：等待主控独立验收；未进入 Step 2。
```

A4 完成后运行七个 archive + candidate view JSON parse、`git diff --check`、
禁止路径 diff 检查。`search-archive/` 是项目标准 ignore 路径，不 force-add；
只提交 worker log。commit message：

```text
execute T013 B9 Step 1 evidence adapter
```

---

## 4. 主控验收

- [ ] task-control 起飞前 PASS，D015/D026 active，起飞工作树 clean。
- [ ] A1/A2/A3-n/A4 串行执行，每 phase ≤15 分钟；A3-n 每次最多两个 archive。
- [ ] 只产生七个自动 search archives、本地 `_index/all-papers.jsonl`、
  candidate view 和 worker log；没有 `-o` 重复文件。
- [ ] 无下载、全文转换、Step 2/3/3.5/4a/MVE、仿真或 seed。
- [ ] ≥20 非排除 candidates、≥3 真实 source families、≥2 routes、≥5 必读、
  正式发表 ≥50%，或准确停止在对应 blocker。
- [ ] 七个原 archive 的每条 result 均写回人工 priority/reason；candidate view
  provenance 可回到 archive/index。
- [ ] DRE-vs-RO dB 与传统 coherent comparator 口径分离。
- [ ] 42 m FSO 与星地深湍流迁移债务分离。
- [ ] 8–12 篇 acquisition debt 覆盖 canonical/comparator/task-fit 四种角色。
- [ ] formal science disposition 与 `mission_method_delta=NONE` 分开。
- [ ] executor 未更新任何 formal/current owner。

## 5. 禁止修改

- `.sessions/**`
- `projects/thesis-fso/master-state.md`
- `projects-overview.md`
- `projects/thesis-fso/direction-lab/{state,portfolio,harvest}/current.yaml`
- `D:\code\study\research-protocol\papers\**` 与共享 `papers/index.json`
- `projects/simulation/**`
- `common/**`、`params.py`
- 旧 T006/T008/T009/T010/T011/T012 与旧 Scout
- RDL/session-governance Skills
