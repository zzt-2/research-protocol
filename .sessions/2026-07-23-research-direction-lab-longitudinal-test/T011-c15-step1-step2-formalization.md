# Task Brief: C15 blind-equalization cost Step 1–2 formalization

> 来源: S001 | 产出位置:
> `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`
> 日期: 2026-07-26
> 唯一文档: 执行方只依赖本任务文件、仓库内公开论文资产与指定工具

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 25
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：只完成 C15 的 Groundwork Step 1 search 与 Step 2 acquire，建立可审计的
盲均衡代价函数文献池、传统 comparator 来源和全文覆盖面报告。

**产出**：

1. `search-archive/2026-07-26/` 下由 `tools/search` 自动生成的结构化 JSON；
2. 合法下载到共享论文库
   `D:\code\study\research-protocol\papers\{arxiv|doi|manual}\{id}\` 的全文及
   metadata/index；
3. worker log
   `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`。

**结束状态**：`AWAITING_COVERAGE_CONFIRMATION`。即使全文达到五篇，也必须停下；
不得进入 Step 3 精读。

**最高纪律**：

1. C15 是 **16-QAM/高阶 QAM 的盲均衡 cost / update family**，不是 carrier phase
   recovery。不得沿用 R002 中“CPR 相位代价”的误称。
2. 不运行旧 C15 sandbox、任何仿真、MVE、seed、测试矩阵或参数修复。
3. 不把摘要、网页、搜索结果或旧 Scout synthesis 冒充全文或 scientific verdict。
4. 不获取私有全文；严格执行下载三轮止损，失败项进入覆盖面报告。
5. executor 不修改 control、formal owner、mission-log、S/R/D/V/topic-index、
   master-state 或 current projections。
6. Step 1/2、搜索 PASS、下载 PASS 与覆盖面 PASS 的
   `mission_method_delta` 均为 `NONE`。

---

## 1. 背景

### 1.1 当前科学状态

- formal owner: `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D023`
- live owner: `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D012`
- 当前无 active scientific carrier。
- T010/B10 已以 `BLOCKED_IDENTITY / mission_method_delta=NONE` 收口；不得修复。
- B1/T008、A4/T009、T006/B12、Pilot-Jones、P03/Scout 均不在本包范围。
- 本包止于 Groundwork Step 2；Step 3、3.5、4a/MVE、Step 5、Contract、Execute
  全部未授权。

### 1.2 旧 C15 资产的合法用法

旧资产：
`projects/thesis-fso/direction-lab/scout/cb1-modulation-generic-closure/c15-reduced-const-cost-scout/`

只允许提取以下历史事实：

- 它比较过 Godard、nearest-ring cost 与 outer-ring masked cost；
- 三种 cost 共用 `mu=0.03`，旧诊断显示 collapsed-state 初始梯度约有 19× scale 差；
- 因 unequal-step / unequal-convergence opportunity，旧性能数字和
  `LOCAL_NEGATIVE` 不得继承为 formal 结论；
- 旧文档将 Sato 1975、RCCMA、outer-ring-only、ring-aware/RDE/MMA 的关系写成
  若干未经全文闭合的断言。这些断言必须作为待核查问题，不能当来源。

了解即可，不对旧性能结果重新评价，不修改旧资产。

### 1.3 本包要闭合的 formalization 问题

搜索与获取必须回答：

1. “reduced constellation”在经典 Sato 1975 中究竟指什么 cost/update？
2. RCCMA、RDE/radius-directed equalization、MMA/generalized MMA 与
   nearest-ring/outer-ring-masked update 的准确血缘和差异是什么？
3. PM-16QAM 或 coherent-optical blind equalization 中，哪一种是当前仍广泛采用的
   传统 comparator：CMA、MMA、RDE、CMA→RDE/MMA staged chain，还是其他？
4. 在星地/自由空间 coherent optical 的湍流或动态偏振条件下，现有传统方法具体
   暴露了哪种 `M-C-A` 失效；若没有直接证据，必须明确记录。
5. 是否存在一个可毕业式包装的正向形态，例如“有界复杂度下降且保持均衡性能”或
   “动态条件下 staged/normalized cost 提升收敛与跟踪”，但本包不得预判。

---

## 2. 执行方式

### 2.1 起飞门

先从仓库根目录运行：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T011-c15-step1-step2-formalization.md
```

非 PASS 立即停止。再确认：

- `git status --short` 为空；
- formal D023 与 live D012 存在；
- worktree HEAD 至少包含标签 `rdl-t010-closure`；
- 未启动任何仿真进程。

### 2.2 Step 1 — structured search

先查项目主仓的共享索引
`D:\code\study\research-protocol\search-archive\_index\all-papers.jsonl` 与
`D:\code\study\research-protocol\papers\index.json`，但已有索引不满足 C15 的
候选专属 Step 1。两者是项目级共享资产；不得假定 worktree 内存在同名索引，也
不得在 worktree 内另建孤立 `search-archive/_index` 或 `papers/index.json`。

至少覆盖以下六个机制词族；不得用模型名变体凑数量：

1. `blind equalization square QAM constant modulus multimodulus`
2. `reduced constellation equalization Sato algorithm square QAM`
3. `radius directed equalization RDE coherent optical PM-16QAM`
4. `CMA RDE MMA staged blind equalization coherent optical 16QAM`
5. `free-space optical turbulence adaptive blind equalization CMA RDE`
6. `normalized variable step CMA confidence weighted staged blind equalization`

要求：

- 第一轮 ≥3 组不同角度检索；
- 从结果识别至少两个候选子方向，再各做 ≥2 组定向深搜；
- 每个启用的数据源请求 ≥15 条（统一使用 `--max-per-source 20`），并在 worker
  log 报告每源实际返回量；
- 至少一个候选子方向的定向检索必须在 metadata 层确认创新空白不是初始检索漏召；
  这只满足 Step 1 方向验证，不等于 M-C-A 或方法信号；
- 使用下方完整命令，结果同时由工具自动归档并写入确定路径
  `search-archive/2026-07-26/`；
- 去重后 ≥20 篇，覆盖 ≥3 个数据源、≥2 个技术路线；
- 对每条结果读取 title + abstract + venue + year + citations +
  publication_status，人工语义标注 `priority` 与 `priority_reason`；
- “必读”≥5，正式发表占比 ≥50%；
- 任何网页或 abstract 只能支撑候选筛选，不能支撑公式、方法血缘、M-C-A 或
  formal conclusion；
- 对 Sato 1975、Godard 1980、Yang/Werner/Dumont 2002 等经典条目记录精确
  title/venue/DOI/可获取状态，不凭旧代码注释填写。

若工具失败，保留命令、exit code 与已生成的合法 archive；不得改用主对话 web
search、ResearchGate 或网页抓全文。

#### 可直接执行的 Step 1 命令

仓库中的 bash wrapper 当前是 CRLF；不得改文件，统一以只读 `sed` 流去除行尾
`\r` 后执行。以下命令均在 PowerShell 中运行：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p ../search-archive/2026-07-26 && sed 's/\r$//' search | bash -s -- 'blind equalization square QAM constant modulus multimodulus' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-cma-mma.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'reduced constellation equalization Sato algorithm square QAM' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-rca-sato.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'radius directed equalization RDE coherent optical PM-16QAM' --mode academic --preset problem-driven --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-broad-rde-optical.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'CMA RDE MMA staged blind equalization coherent optical 16QAM' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-staged-optical.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'free space optical turbulence adaptive blind equalization CMA RDE' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-fso-taskfit.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'normalized variable step CMA confidence weighted blind equalization square QAM' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-normalized-cost.json"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'reduced constellation algorithm radius directed equalizer multimodulus canonical' --mode academic --preset comparison --max-per-source 20 --top 40 -o ../search-archive/2026-07-26/c15-deep-lineage.json"
```

完成语义审查后，executor 必须用 `apply_patch` 创建
`search-archive/2026-07-26/c15-step1-acquisition-pool.json`，只复制 8–12 个
“必读/建议读”结果对象，保留原 id/title/abstract/DOI/arXiv/source/priority 字段，
不得用 shell 重写或人工补造 metadata。顶层 schema 冻结为：

```json
{
  "query": "C15 Step 1 selected acquisition pool",
  "sources": ["从原 archive 原样复制实际来源"],
  "results": [
    {"id": "原对象字段；此处只是 schema 示意，不得原样落盘"}
  ]
}
```

实际文件的 `results` 必须是长度 8–12 的对象数组；不得写成裸列表或另一个键名。
创建后先以 Python JSON parse + `len(data["results"])` 验证，再运行 download。

### 2.3 Step 2 — acquire and quality gate

从“必读 + 建议读”中选择约 8–12 篇，优先级：

1. 定义 cost/update 血缘的 canonical 论文；
2. PM-16QAM/coherent optical 中的 conventional comparator 与 staged chain；
3. 直接涉及 FSO/湍流/动态偏振的 task-fit 论文；
4. 近年代表性正式论文。

五篇有效全文中至少包括：

- ≥3 篇 canonical cost/algorithm lineage 全文；
- ≥2 篇近期 coherent-optical/PM-16QAM conventional comparator 或 staged-chain
  全文。

严格按 `stages/gw-acquire.md`。第一轮使用确定路径的 acquisition pool：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' download | bash -s -- ../search-archive/2026-07-26/c15-step1-acquisition-pool.json --output-dir /mnt/d/code/study/research-protocol --dry-run"
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' download | bash -s -- ../search-archive/2026-07-26/c15-step1-acquisition-pool.json --output-dir /mnt/d/code/study/research-protocol"
```

第二轮只对第一轮失败标题做一次 arXiv/author-version 定向检索。executor 必须先在
worker log 写出每个失败标题对应的完整实际命令与确定输出路径，再执行；不得使用
`...`、`<title>` 或其他占位符。

第三轮只执行一次 IEEE 检索/下载：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && mkdir -p /mnt/d/code/study/research-protocol/papers/downloads/2026-07-26/c15-step2-ieee && sed 's/\r$//' blit | bash -s -- 'blind equalization PM-16QAM CMA MMA RDE' --source ieee --format json -o ../search-archive/2026-07-26/c15-step2-ieee.json --download /mnt/d/code/study/research-protocol/papers/downloads/2026-07-26/c15-step2-ieee"
```

blit 只产出裸 PDF、JSON 与 `{arnumber}.meta.json` sidecar，不自动入库。若有成功
PDF，必须先用 `apply_patch` 创建
`search-archive/2026-07-26/c15-step2-ieee-ingest-plan.json`。每篇记录以下确定字段：

- `source_pdf`：实际 `{arnumber}.pdf` 绝对路径；
- `source_sidecar`：实际 `{arnumber}.meta.json` 绝对路径；
- `result_pointer`：`c15-step2-ieee.json` 中对应对象的数组下标；
- `id`、`title`、`doi`、`arnumber`：只从 JSON/sidecar/PDF 首屏复制；
- `target_dir`：有 DOI 时固定为共享库
  `D:\code\study\research-protocol\papers\doi\{lowercase DOI 且 /→_}`；无 DOI
  时才用 `papers\manual\{title-slug}`；
- `index_key`：有 DOI 时固定为 `doi:{lowercase DOI}`；无 DOI 时固定为
  `manual:{title-slug}`。
- `index_path`：固定为相对共享 `papers/` 根的
  `doi/{lowercase DOI 且 /→_}` 或 `manual/{title-slug}`；不得写绝对路径，也
  不得加前缀 `papers/`。

不得猜 DOI；无法从结果/PDF 确认 DOI 的条目只允许进 `manual`。在实际搬运前，
executor 必须把每篇的**完整、无占位符** PowerShell/WSL 命令写入 worker log，
然后逐篇执行以下固定闭环：

1. 若 target 已有 `download_status=success`，只核验并复用，禁止覆盖；否则创建精确
   `target_dir`，把裸 PDF 复制为 `source.pdf`。
2. 对该 `source.pdf` 运行 worktree 的 `tools/convert`，`-o` 指向同一
   `target_dir`；工具会生成 `source.md`，随后将其精确重命名为 `content.md`。
3. 用 `apply_patch` 在 target 写 `metadata.json`，至少含
   `storage_version=2`、id/title/doi、`download_status=success`、
   `download_method=blit_ieee`、`content_type=pdf`、`content_quality`、
   `content_file=content.md`、`downloaded_at`、`download_source`、
   real_title/title_check/title_overlap。后三项必须来自 sidecar 或重新运行
   `litdownload.title_verify` 的实际输出，不得伪造。
4. 用 `apply_patch` 向共享 `papers/index.json` 的 `papers` 对象写入/更新精确
   `index_key`：`path` 必须等于 ingest plan 的相对 `index_path`，其余为 doi、
   title、status=`success`、method=`blit_ieee`、arnumber、
   batches=`["c15-step2-2026-07-26"]`。修改前后均 JSON parse；不得写绝对
   target_dir、不得加 `papers/` 前缀、不得覆盖其他条目的 batches/history。
5. 验证 `source.pdf`、`content.md`、`metadata.json` 齐全，正文 ≥50 有效行，
   metadata title/DOI 与 PDF 一致；只有全部通过才计入五篇门槛。

任一逐篇闭环失败，只把该篇记入覆盖缺口，不得把 downloads 临时目录中的 PDF
计为成功全文。第三轮后停止，不再增加下载通道。

不得超过三轮，不得抓 ResearchGate/Semantic Scholar 网页全文。

每篇成功全文必须：

- 位于 `papers/{arxiv|doi|manual}/{id}/content.md`；
- `content.md` 有 ≥50 行有效正文；
- metadata/title/DOI 与实际首个有效标题一致；
- 记录 `metadata.json` 的来源和 title_check；缺失时人工核对前 20 行；
- 公式/表格若大面积乱码则标内容质量不达标，不算入五篇门槛。

### 2.4 停止规则

出现任一情况立即停止并如实报告：

- task-control FAIL；
- 搜索无法达到 ≥20 或“必读”≥5；
- 可用全文 <5；
- canonical cost identity 仍只能由摘要/旧注释支撑；
- 下载需要私有凭据、用户手工全文或超出止损轮次；
- 发现 C15 本质与当前星地双偏振场景无 task-fit 证据。

停止不是 Kill，不得把缺全文当 scientific negative。

---

## 3. 产出格式

worker log 必须按以下结构：

```markdown
# Step 011 — C15 Step 1–2 formalization

## Status
- task_control: PASS/FAIL
- final_status: AWAITING_COVERAGE_CONFIRMATION | BLOCKED_...
- formal_science_disposition: FORMALIZATION_STEP1_STEP2_COMPLETE | BLOCKED_...
- mission_method_delta: NONE
- simulation_or_seed_run: false

## Exact commands and exits

## Step 1 search audit
### Query families and archive paths
### Deduplicated coverage statistics
### Candidate table
| id | title | year/venue | DOI/arXiv | source | route | priority | reason |
### Directional deep-search results
### Excluded false positives

## Terminology and lineage questions
| claim | evidence status | source pointer | unresolved debt |

## Step 2 acquisition audit
| title | id | download route | content path | effective lines | title/DOI check | status |

## Coverage gap report
### 成功获取
### 内容质量不达标
### 下载失败
### 覆盖面分析
### 引用质量分析
### 用户行动项

## Candidate-specific baseline map
| possible claim | shared anchor | task comparator | canonical source | representative uses | task-fit status |

## Integrity boundaries

## Next gate
只写：等待 coverage confirmation；未进入 Step 3。
```

搜索 JSON 中必须保留人工 priority 标注。worker log 只引用 archive/fulltext 路径，
不复制长摘要或全文。

---

## 4. 验收

- [ ] task-control 在执行前 PASS。
- [ ] 无仿真、seed、MVE 或旧 C15 资产修改。
- [ ] C15 全程按 blind equalization cost/update 处理，不误称 CPR。
- [ ] Step 1 ≥20 candidates、≥3 sources、≥2 routes、≥5 必读、正式发表≥50%。
- [ ] 每个启用源请求≥15条并报告实际返回量；至少一个子方向的定向检索确认
  metadata 层创新空白不是漏召。
- [ ] 两个候选子方向各有 ≥2 组定向深搜。
- [ ] 搜索结果 JSON 有人工 priority/priority_reason。
- [ ] Step 2 严格三轮止损，成功全文 ≥5 且每篇 ≥50 有效行。
- [ ] 五篇中 canonical lineage ≥3、近期 coherent-optical comparator/staged chain ≥2。
- [ ] canonical/traditional comparator 来源与 task-fit 分开记录。
- [ ] 覆盖面缺口报告完整，失败全文未被 abstract 替代。
- [ ] 最终状态停在 `AWAITING_COVERAGE_CONFIRMATION`。
- [ ] `formal_science_disposition` 与 `mission_method_delta=NONE` 分开记录。

## 5. 禁止修改

- `.sessions/**`（本 T 除外也不得回写）
- `projects/thesis-fso/master-state.md`
- `projects-overview.md`
- `projects/thesis-fso/direction-lab/{state,portfolio,harvest}/current.yaml`
- `projects/simulation/**`
- `common/**`、`params.py`
- 旧 T006/T008/T009/T010 与旧 C15 Scout
- RDL/session-governance Skills
