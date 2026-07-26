# Task Brief: B9 Step 1 多源与 mechanism-deep 覆盖修复

> 来源: S001 | 产出位置:
> `projects/thesis-fso/worker-logs/step-014-b9-step1-multisource-coverage-repair.md`
> 日期: 2026-07-27
> 唯一文档: 执行方只依赖本任务文件、T013 指定的本地 ignored archives/candidate
> view、项目检索工具和公开检索源

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 34
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP013
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：对 T013 暴露的唯一有界缺口做一次 B9 Groundwork Step 1 覆盖修复：
用 Semantic Scholar、arXiv 和 IEEE Xplore 的真实返回补充 OpenAlex，随后只在
来源门通过时做两条 mechanism route 的定向深搜、语义标注和 v2 综合。

**产出**：

1. `search-archive/2026-07-27/` 下最多四个 `tools/search` 自动 archive；
2. 同目录下最多四个 `t014-ieee-*.json`；
3. `tools/search` 标准副作用可增量更新本地 ignored
   `search-archive/_index/all-papers.jsonl`；
4. 始终生成
   `search-archive/2026-07-27/b9-step1-coverage-repair-receipt.json`；
5. 只有进入综合时生成
   `search-archive/2026-07-27/b9-step1-candidate-view-v2.json`；
6. worker log
   `projects/thesis-fso/worker-logs/step-014-b9-step1-multisource-coverage-repair.md`。

**允许的最终状态**：

- `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE`；
- `BLOCKED_SEARCH_COVERAGE`；
- `STEP1_NO_DISTINCT_PROBLEM_FOUND`。

三种状态的 `mission_method_delta` 都必须为 `NONE`。即使 Step 1 PASS，也不是
方法信号。

**最高纪律（违反一条即停止）**：

1. 只做 Groundwork Step 1。不得下载/转换/精读全文，不得进入 Step 2/3/3.5/4a/
   MVE，不得实现 DRE、EFNS、DC-Value、virtual-carrier 或运行仿真、seed。
2. 这是 B9 唯一一次 coverage repair。若 A1 后实际源仍不足 3，立即终止；
   不改门槛、不补第三个 B9 Step 1 包。
3. 实际 source family 只按本次 archive 中真实返回记录的 API/platform 计数。
   配置名、失败调用、共享索引的历史 `source_apis` 字符串都不能计数。
4. metadata/abstract 只能支持 Step 1 语义审查；不得冒充全文、formal Step 3、
   M-C-A、science Go/Kill、`METHOD_SIGNAL`。
5. EFNS 是 DRE 的直接廉价竞争者；混合 FSO/delta-sigma 只属 adjacent context；
   clipping paper 是 DRE optimization lineage，不能冒充 original DRE canonical。
6. executor 不修改 control、formal owner、mission-log、S/R/D/V/topic-index、
   master-state/current projections、共享论文库、工具、Skill 或旧研究资产；
   只允许 `tools/search` 更新 worktree 本地 ignored index。
7. 每个子 agent phase 最长 15 分钟；A1、A2、A3-n、A4 串行。A3-n 每次最多
   审查两个新 archive；每 phase 完成即停回主控。

## 1. 背景

### 1.1 当前权威状态

- formal owner:
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D027`
- live owner:
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D016`
- current control: epoch 34 / CP013 /
  `B9_STEP1_BOUNDED_COVERAGE_REPAIR`
- 当前无 active scientific carrier。
- T013 已独立接收为
  `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`：
  `61→58`、非排除 `21`、必读 `8`、正式发表 `21/21`，但实际来源只有
  OpenAlex；Route A deep=`0`，Route B 两条 deep 只是一般 task-fit/adjacent
  FSO。

### 1.2 只能继承的 T013 输入

- 七个 T013 annotated archives：
  `search-archive/2026-07-27/*.json`，排除本 T 新建的 `t014-*` 文件；
- `search-archive/2026-07-27/b9-step1-candidate-view.json`；
- `projects/thesis-fso/worker-logs/step-013-b9-step1-evidence-adapter.md`。

T013 view 是只读基线，不覆盖。v2 必须保留 T013 的 58 条去重记录、语义字段、
archive 指针和 acquisition debt 血缘。

### 1.3 两条 route

- **Route A**：low-resolution DAC、DRE、EFNS、clipping、quantization/noise
  shaping；要找任务匹配的传统 comparator 与尚未被 EFNS 覆盖的剩余机制问题。
- **Route B**：self-coherent/virtual-carrier FSO、KK/DC-Value、CSPR、
  phase reconstruction；要找星地/湍流下明确的 mechanism evidence，不能用一般
  FSO survey 或相干检测替代。

## 2. 执行方式

### 2.1 唯一起飞门

在 worktree 根运行：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T014-b9-step1-multisource-coverage-repair.md
git status --short
rg -n -A 7 "^## D027:|^## D016:|^> status: active" `
  .sessions/2026-07-06-step4a-mve-execution/decisions.md `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md
```

要求 validator `PASS`、worktree clean、D027/D016 active。若任何 T014 输出已存在，
停止且不删除/覆盖。任一失败写 worker log 为 `BLOCKED_PREFLIGHT`。

### 2.2 Phase A1（≤15 分钟）— source capability + broad route search

运行两条 S2/arXiv 检索。bash wrapper 为 CRLF，只读去除 `\r`，不得改工具：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'digital resolution enhancer error feedback noise shaping low resolution optical DAC' --sources s2 arxiv --max-per-source 20 --top 40"

wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'virtual carrier self coherent FSO Kramers Kronig DC value satellite ground' --sources s2 arxiv --max-per-source 20 --top 40"
```

再运行两条 IEEE 元数据检索；`tools/blit` 不自动 archive，所以只允许以下 exact
output：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' blit | bash -s -- 'digital resolution enhancer error feedback noise shaping low resolution optical DAC' --source ieee --max 20 --format json --output ../search-archive/2026-07-27/t014-ieee-route-a-broad.json"

wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' blit | bash -s -- 'virtual carrier self coherent free space optical Kramers Kronig DC value' --source ieee --max 20 --format json --output ../search-archive/2026-07-27/t014-ieee-route-b-broad.json"
```

记录每条命令的 exit、自动 `[存档]` 路径、每个真实返回源和结果数。建立
`b9-step1-coverage-repair-receipt.json`，至少包含：

```json
{
  "schema_version": "b9.step1.coverage-repair.receipt.v1",
  "phase": "A1",
  "queries": [],
  "actual_return_source_families": [],
  "actual_return_source_family_count": 0,
  "includes_t013_openalex": true,
  "gate_at_least_three_sources": false,
  "next_phase_authorized": false
}
```

实际 family union 必须把 T013 的 OpenAlex 与本阶段真实返回的 S2/arXiv/IEEE
去重合并。若 union `<3`，写 worker log：
`BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`，停止，不执行 A2。

### 2.3 Phase A2（≤15 分钟）— 两条 mechanism-deep 定向检索

仅当 A1 union `>=3` 时运行：

```powershell
wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'DRE EFNS clipping quantization noise feedback optical transmitter low bit DAC' --sources s2 arxiv --max-per-source 20 --top 40"

wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' search | bash -s -- 'satellite ground turbulence self coherent FSO virtual carrier CSPR phase reconstruction' --sources s2 arxiv --max-per-source 20 --top 40"

wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' blit | bash -s -- 'DRE EFNS clipping quantization noise feedback optical transmitter low bit DAC' --source ieee --max 20 --format json --output ../search-archive/2026-07-27/t014-ieee-route-a-deep.json"

wsl bash -lc "cd /mnt/d/code/study/research-protocol/.worktrees/rdl-method-production-v2/tools && sed 's/\r$//' blit | bash -s -- 'satellite ground turbulence self coherent FSO virtual carrier CSPR phase reconstruction' --source ieee --max 20 --format json --output ../search-archive/2026-07-27/t014-ieee-route-b-deep.json"
```

更新 receipt 到 `phase=A2_COMPLETE`，保留 A1 与 A2 全部 command/source/result
事实。若某命令失败或零结果，如实记录；不得用本地 index 补算真实来源。

### 2.4 Phase A3-n（每次≤15 分钟）— 新 archive 语义审查

每次最多两个 T014 archive；不重审或改写 T013 archives。对每个 result 只根据
已有 title/abstract/venue/year/citation/publication metadata 增加：

- `priority`: `必读|建议读|待确认|备选|排除`
- `priority_reason`
- `route`: `A_lowres_noise_shaping|B_selfcoherent_fso_taskfit|BOTH|NONE`
- `collision_role`
- `evidence_scope`: `METADATA_ONLY`
- `query_depth`: `BROAD|DEEP`

若 abstract 缺失，必须在 reason 中写 `ABSTRACT_MISSING`，不得脑补机制。每次写回
原 T014 archive并记录数量、字段完整性与 enum 检查。只有全部新 raw result
`100%` 标注后才能 A4。

### 2.5 Phase A4（≤15 分钟）— v2 synthesis 与唯一 Step 1 gate

合并 T013 七个 annotated archives 与全部 T014 annotated archives，用 DOI、
normalized title 去重，生成 `b9-step1-candidate-view-v2.json`。必须保留：

- 每条来源 archive 与 raw index；
- T013 已有语义字段，不覆盖成人为更有利的分类；
- actual search-run family 与 historical index provenance 分离；
- Route A/Route B 的 broad/deep/source 交叉表；
- direct competitor、residual problem hypothesis、claim ceiling；
- acquisition debt `8–12`，覆盖 DRE lineage、original DRE citation chase、
  traditional comparator、self-coherent/FSO task-fit 四类。

Step 1 PASS 必须同时满足：

1. 非排除 unique `>=20`；
2. 实际 source families `>=3`；
3. 必读 `>=5`；
4. 正式发表比例 `>=50%`；
5. 所有新 raw result 已人工语义标注；
6. 至少一条 route 同时有 broad 与非 OpenAlex 的 mechanism-specific deep
   非排除证据，并由具体 abstract 支持一个 candidate-specific residual problem；
7. acquisition debt 满足上述范围与四类角色。

处置：

- 全部通过：
  `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE`；
- 来源/route deep 仍不闭合：
  `BLOCKED_SEARCH_COVERAGE`；
- 来源闭合但没有 abstract 支持剩余问题，或竞争已完整覆盖：
  `STEP1_NO_DISTINCT_PROBLEM_FOUND`。

无论哪种，写
`formal_science_disposition`、`mission_method_delta=NONE`、
`simulation_or_seed_run=false`，停止在 Step 2 前。

## 3. 已知陷阱

1. S2 被限流不算返回；arXiv/IEEE 只在实际 `results` 非空时算 source family。
2. IEEE Xplore 是检索平台，不意味着每条都是 IEEE 正式发表；逐条看 venue/year。
3. 同一 DOI 被 OpenAlex、S2、IEEE 返回可增强交叉来源，但 unique paper 仍只算一篇。
4. “satellite-ground query 零结果”不是空白证据；只能写 coverage failure。
5. 不把 EFNS 的 DRE 对照改写成星地 FSO 结论，不把 42 m outdoor FSO 外推到深湍流。
6. 不覆盖 T013 candidate view，不删除零结果 archive，不修改 ignored 规则。

## 4. 验收

- [ ] task-control fresh PASS，起飞时 tracked worktree clean；
- [ ] A1 最多四条命令，真实 source family 计数可由 raw archive复核；
- [ ] A1 `<3` 时确实停止，没有 A2/A3/A4 产物；
- [ ] A1 `>=3` 时 A2 仅运行冻结四条 deep 查询；
- [ ] 所有新 raw results 的六个语义字段完整且 enum 合法；
- [ ] v2 的去重、source-family、route、priority、publication 与 debt 数可复算；
- [ ] disposition 只属于 Step 1，method delta 为 NONE；
- [ ] 未下载、精读、实现、实验或进入后续 Step；
- [ ] executor 只提交 worker log；ignored raw/view/receipt 不 force-add；
- [ ] `git diff --check` PASS，提交不含 owner/control/旧资产。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-014-b9-step1-multisource-coverage-repair.md`
