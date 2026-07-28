# Task Brief: Q14 Groundwork Step 3.5 与 problem-evidence closure

> 来源: S001 / R008 / D025 / formal D036
> 产出位置:
> `projects/thesis-fso/worker-logs/step-018-q14-step35-problem-evidence-closure.md`
> 日期: 2026-07-27
> 执行方式: 仅由本 Goal 内部 executor 分相执行；用户不转发、不读技术日志、
> 不判断科学正确性

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 46
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP017
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在 worktree
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

本任务有两个必须区分的根：

```text
WORKTREE_ROOT=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
SHARED_REPO_ROOT=D:\code\study\research-protocol
SHARED_PAPERS_ROOT=D:\code\study\research-protocol\papers
```

control、search raw、literature_notes 与 worker log 写 worktree；既有/新增全文和
全局 read note 写共享 `SHARED_PAPERS_ROOT`。不得因 worktree 下没有相同
`papers/doi/...` 目录而误报全文缺失或重复下载。

**任务**：只执行 Q14 的 Groundwork Step 3.5，系统性补检
`standard-CMA always-online + strictly-causal receiver-visible additive
residual corrector` 的直接/反面/cheap-alternative 证据，并把问题四判据 2
裁为 `PASS`、`FAIL` 或 `UNKNOWN`。

**产出**：冻结 search/citation/fulltext receipts、必要时更新
`projects/thesis-fso/literature_notes.md` 的 Q14 Step 3.5 条目，并写完整
step-018 worker log。

**最高纪律（违反任一条，本包废弃）**：

1. 本包不是方法或实验包：
   `formal_active_scientific_carrier=NONE`，
   `mission_method_delta=NONE`；禁止 simulation/Probe/MVE/seed、实现 residual
   head、修改 evaluator 或运行旧 Scout/P03。
2. 禁止用本地 experiment/oracle gap、标题空白、未发现直接先例或
   TX-truth-assisted result 反向证明问题合法性；判据 2 只能由本包的外部论文
   证据和既有 5 篇全文的明确内容裁决。
3. runtime 方法合同只允许 `z_CMA` 与严格因果 receiver-visible CMA
   trace/context；TX truth、future window、true h/theta/Jones、fixed-label BER、
   oracle branch 均只可用于离线训练/评分边界，不能伪装为部署输入。
4. strongest cheap comparator 是 tuned standard CMA +
   task-matched DD-LMS/RDE cascade；`fixed+PI` 是评估口径，不是方法 comparator；
   blind affine 只是辅助诊断。
5. executor 不更新 `.sessions`、control、formal owner、mission-log、current
   projections、registry、master-state 或 projects-overview；只写本任务授权的
   worktree search artifacts、共享 paper/read-note artifacts、必要的
   `literature_notes.md` Step 3.5 更新和 worker log。不得修改 shared repo 中
   与 papers/index 维护无关的 tracked file。
6. actual source 按结果行 provenance 计算；配置了 source、空返回、rate-limit
   或同一来源重复记录都不得凑源。Step 3.5 必须实际出现 Semantic Scholar
   以及至少一个其他 source family。
7. 每个 executor turn ≤15 分钟。接近 12 分钟仍未闭合当前 phase 时，只写
   continuation receipt，状态 `BLOCKED_EXECUTION_TIMEBOX`；主控可在同一 T018
   内续相，不能降门或新开第二个 Q14 problem-evidence package。

冻结 terminal 状态只有：

```text
BLOCKED_PREFLIGHT
BLOCKED_STEP35_SOURCE_COVERAGE
BLOCKED_STEP35_IDENTITY
BLOCKED_STEP35_FULLTEXT
BLOCKED_STEP35_NONCONVERGENCE
BLOCKED_PROBLEM_EVIDENCE_ROTATE
PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO
```

非 terminal continuation receipt 只有：

```text
BLOCKED_EXECUTION_TIMEBOX
AWAITING_DELEGATED_COVERAGE_GATE
```

continuation 不追加 mission checkpoint，不提出 formal disposition、streak 或
no-method 计数，也不能进入下一 phase。所有 terminal 状态均：

```text
mission_method_delta=NONE
STEP4A_AUTHORIZED=FALSE
METHOD_SIGNAL=FALSE
```

`PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO` 只表示建议主控另建 Step 4a A0
任务；本包无权激活 carrier 或进入 A0。

---

## 1. 背景与唯一权威

### 1.1 当前 owner

- live control：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
- live owner：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D025`
- formal owner：
  `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D036`
- remap：
  `.sessions/2026-07-23-research-direction-lab-longitudinal-test/R008-post-c16-q14-problem-evidence-remap.md`
- framework：
  `stages/groundwork.md`、`stages/gw-supplement.md`、
  `stages/gw-acquire.md`、`stages/gw-read.md`、`stages/glossary.md`
- 共享论文库：
  `D:\code\study\research-protocol\papers`（不等于 worktree 下的稀疏
  `papers/` 目录）

### 1.2 Q14 已有证据

- `R009-residual-cascade-step1-survey.md`：2019–2026 六组搜索；未发现
  “standard CMA 始终在线 + additive NN residual”的明确直接命中，但发现
  VAE replacement、CNN/Volterra、CMA+DD-LMS/RDE 等直接相邻方法。
- `S037-residual-cascade-acquire.md`：5 篇合法全文门 PASS。
- `S038-residual-cascade-read.md`：5/5 Step 3 精读 PASS。
- `S039-residual-cascade-step4a-gate.md` 与 formal D044：四判据 1/3/4
  PASS、2 UNKNOWN；未执行 Q14 专属 mandatory Step 3.5，不得进入 A0/MVE。
- `projects/thesis-fso/literature_notes.md:123` 是 Q14 当前正式问题表条目。

五篇当前 corpus：

```text
L01 10.1109/JSAC.2022.3191346
    D:\code\study\research-protocol\papers\doi\10.1109_jsac.2022.3191346\content.md
L02 10.1109/JLT.2021.3056869
    D:\code\study\research-protocol\papers\doi\10.1109_jlt.2021.3056869\content.md
L03 10.1109/JSTQE.2022.3174268
    D:\code\study\research-protocol\papers\arxiv\2109.14942\content.md
L04 10.1109/JLT.2022.3146839
    D:\code\study\research-protocol\papers\doi\10.1109_jlt.2022.3146839\9695357.md
L05 10.1109/JLT.2023.3276637
    D:\code\study\research-protocol\papers\doi\10.1109_jlt.2023.3276637\content.md
```

### 1.3 待裁决的唯一问题

Q14 的判据 2 不是“有没有 residual 这种网络结构”，而是：

> 在一个冻结的 dual-pol coherent receiver condition 下，tuned conventional
> CMA 后是否仍存在稳定、严格因果、receiver-visible、能产生 decision/soft
> information 收益且不被 tuned CMA+DD-LMS/RDE/simple residual DSP 吸收的
> residual；若存在，`z_out=z_CMA+gφ(...)` 才可能是可复用方法产出。

---

## 2. 分相与时间盒

T018 是一个 package，可在同一 executor 上下文内分多个 ≤15 分钟 turn：

1. **Phase A — evidence inventory + Round 1 matrix/citation search**；
2. **Phase B1 — 新高相关论文的合法 acquire + coverage-gap report**（只有
   Phase A 需要时）；
3. **Delegated coverage gate — 独立 verifier + Goal 主控确认**；
4. **Phase B2 — gate PASS 后才精读新全文**；
5. **Phase C — Round 2/3 convergence + problem-evidence synthesis**；
6. **Phase D — 仅在形成最终裁决时更新 literature_notes 与关闭 worker log**。

`BLOCKED_EXECUTION_TIMEBOX` 与 `AWAITING_DELEGATED_COVERAGE_GATE` 都是同一
package 的 continuation receipt，不计 mission checkpoint。只有上述七个
terminal 状态之一才关闭 T018。

---

## 3. Phase A — 起飞、证据库存与冻结 Round 1

### A0. 起飞门

从 worktree 根执行：

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  --repo-root . `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T018-q14-step35-problem-evidence-closure.md
git status --short
```

必须满足：

- task-control PASS：epoch46 / CP017 /
  `action_class=CANDIDATE_FORMALIZATION`；
- D025、D036 active，control lane 为
  `Q14_STEP35_PHASE_A_AUTHORIZED`；
- `formal_active_carrier=NONE`；
- 无 simulation/MVE/seed 进程；
- 起飞时记录完整 `git status --short` 和所有既有 dirty file SHA256。executor
  结束时必须证明除授权路径外未改变这些文件。
- 对上述五个 `SHARED_PAPERS_ROOT` corpus path 逐一做存在性、字节数与 SHA256
  receipt；同时记录 `git -C D:\code\study\research-protocol status --short`，
  不清理、不覆盖 shared repo 的既有用户改动。

任一失败：只写 worker log，终态 `BLOCKED_PREFLIGHT`。

### A1. 既有证据库存

先读取且只继承明确内容：

```text
.sessions/2026-07-10-dual-pol-osl-groundwork/R009-residual-cascade-step1-survey.md
.sessions/2026-07-10-dual-pol-osl-groundwork/S037-residual-cascade-acquire.md
.sessions/2026-07-10-dual-pol-osl-groundwork/S038-residual-cascade-read.md
.sessions/2026-07-10-dual-pol-osl-groundwork/S039-residual-cascade-step4a-gate.md
.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md#D044
projects/thesis-fso/literature_notes.md#Q14
```

建立 5 篇 corpus 的 title/DOI/content-path/citation-count table。citation count
只能来自本包 API receipt 或已有 raw metadata，缺失记 UNKNOWN，不猜。

### A2. 冻结关键词矩阵

方法变体固定三类：

```text
M1 neural additive residual after adaptive/CMA equalization
M2 post-equalizer error prediction/correction
M3 blind-to-decision-directed CMA+DD-LMS/RDE cascade
```

每类同时覆盖具体 dual-pol coherent scenario 与
online/causal/complexity/generalization 角度，共 6 个 Round-1 组合：

```text
Q1 "CMA neural residual equalizer dual polarization coherent optical PM-QAM"
Q2 "CMA neural residual equalizer online causal adaptation complexity"
Q3 "post equalizer error prediction coherent optical dual polarization QAM"
Q4 "post equalizer error correction online cross-channel generalization latency"
Q5 "CMA DD-LMS RDE cascade dual polarization coherent optical"
Q6 "blind decision directed hybrid equalizer online convergence complexity"
```

每个组合必须用同一实际源合同。以下六条是冻结、可复制的完整命令；不得省略
`--format json` 或 `-o`：

```powershell
bash tools/search "CMA neural residual equalizer dual polarization coherent optical PM-QAM" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q1.json
bash tools/search "CMA neural residual equalizer online causal adaptation complexity" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q2.json
bash tools/search "post equalizer error prediction coherent optical dual polarization QAM" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q3.json
bash tools/search "post equalizer error correction online cross-channel generalization latency" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q4.json
bash tools/search "CMA DD-LMS RDE cascade dual polarization coherent optical" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q5.json
bash tools/search "blind decision directed hybrid equalizer online convergence complexity" --sources s2 openalex --doc-types journal conference preprint --preset problem-driven --year-from 2019 --year-to 2026 --max-per-source 20 --top 40 --format json -o search-archive/2026-07-27/q14-step35-r1-q6.json
```

不得增加第七个 Round-1 组合。执行命令、exit code、wall time、configured
sources、actual sources、rows 与 SHA256 全部写 worker log。

### A3. 核心竞品与双向引用链

在 L01–L05 中按本包可核验 citation count 选择最高引用的 Q14 core
competitor；若 citation count 并列，按 DOI lexical order。对同一 DOI 执行：

```powershell
bash tools/search --citations <DOI> --citations-direction forward --citations-source both --format json -o search-archive/2026-07-27/q14-step35-core-forward.json
bash tools/search --citations <DOI> --citations-direction backward --citations-source both --format json -o search-archive/2026-07-27/q14-step35-core-backward.json
```

分别保存为：

```text
search-archive/2026-07-27/q14-step35-core-forward.json
search-archive/2026-07-27/q14-step35-core-backward.json
```

S2 citation 结果只作召回；凡声称某篇“引用/支持核心方法”的，必须用其
abstract/metadata 与可用 reference receipt 交叉验证。OpenAlex 与 S2 都无实际
rows、或只有单向链，终态 `BLOCKED_STEP35_SOURCE_COVERAGE`。

### A4. 实际 source hard gate

Round 1 六份 search 与两份 citation raw 必须满足：

```text
actual_semantic_scholar_present = TRUE
actual_other_source_family_count >= 1
forward_chain_nonempty = TRUE
backward_chain_nonempty = TRUE
```

actual source 从每条结果的 `source_api`/provenance 计算；`s2+openalex` 拆成
两个实际 family，但 configured-only/empty/error 不计。失败立即终止为
`BLOCKED_STEP35_SOURCE_COVERAGE`，不重试网络、不改 source owner、不降低门。

---

## 4. Review、identity、priority 与收敛轮

### B1. Identity

合并 Round 1、forward、backward 与旧 R009 候选：

- DOI lower-case、去 URL/prefix；
- 无 DOI 才用 Unicode NFKC normalized title + year±1 + first-author；
- 同 normalized title 出现多个非空 DOI 时进入 identity quarantine；
- quarantine 候选不能作 direct evidence 或 acquisition target。

出现影响核心证据的未解 identity conflict：
`BLOCKED_STEP35_IDENTITY`。

### B2. 证据 route

每篇必须分到一个主 route：

```text
R1_DIRECT_ADDITIVE_AFTER_CMA
R2_RECEIVER_VISIBLE_RESIDUAL_INFORMATION
R3_CHEAP_DSP_ABSORBER_OR_COMPARATOR
R4_PRIVILEGED_OR_NONTRANSFERABLE_GAIN
OUT_OF_SCOPE
```

并记录：

```text
priority = 必读 | 建议读 | 待确认 | 备选 | 排除
task_fit = direct | adjacent | none
evidence_scope = fulltext | abstract | metadata
runtime_information = receiver_visible | privileged | unclear
residual_benefit_metric = decision_or_soft | residual_mse_only | none | unclear
simple_dsp_disposition = beaten | matched | not_tested | unclear
exclusion_reason
```

不得把“残差 MSE 下降”自动等价为 BER/SER/Q²/GMI 增益。

### B3. 新论文处理

Round 1 新增 `必读/建议读` 为 0：Round 1 即满足收敛条件，进入 Phase C。

若新增 1–5 篇，严格分成 acquisition 与 read 两个阶段：

1. 按 DOI/title identity 走 `gw-acquire.md`，每篇最多 3 次合法通道；下载与
   转换从 `SHARED_REPO_ROOT` 调用项目工具，使产物进入共享 `papers/`，不得写成
   worktree 私有副本；
2. 私有全文、abstract-as-fulltext、手写 PDF converter 禁止；
3. 每篇 `content.md >=50` 有效行且 title/DOI identity PASS；
4. 获取结束后必须生成 `gw-acquire.md` 规定的完整 coverage-gap report，列出
   成功、质量失败、下载失败、来源偏置、正式发表/预印本比例与最关键缺口；此时
   **禁止精读和 synthesis**；
5. 任一新增必读/建议读全文无法合法获得，写完 coverage report 后 terminal 为
   `BLOCKED_STEP35_FULLTEXT`；不得用摘要补全文门；
6. 若新增必读/建议读均合法取得，则写
   `AWAITING_DELEGATED_COVERAGE_GATE` continuation receipt 并停止。由未参与
   acquisition 的独立 verifier 审查 coverage report 与 receipts，再由 Goal 主控
   依据 live D004 的用户端到端授权和 D025/formal D036 作 delegated coverage
   decision。executor 不得自行确认；
7. delegated gate 的磁盘 receipt 必须同时满足：
   - live `verifications.md` 新增独立 V###，明确
     `COVERAGE_GATE_VERIFIED=TRUE`；
   - Goal 主控在同一 V### 或后继 D### 明确
     `COVERAGE_GATE_APPROVED_BY_MASTER=TRUE`，并列出成功/失败/来源偏置/发表
     状态与未覆盖方向；
   - foreground control 递增 epoch，把 next legal action 改为 T018 Phase B2；
     T018 task-control 同步重绑定且 validator PASS。
   三项齐全后，executor 才可在后续 turn 按 `gw-read.md` 读取，提取与 Q14
   有关的 M-C-A、runtime information、output、comparator、指标、结论和适配
   边界。

该 delegated gate 只适配用户已明确要求 Goal 主控端到端完成、用户不判断技术
正确性的本 mission；不修改 `gw-acquire.md` 的通用人介入规则，也不把 executor
自审当确认。若 coverage report 暴露只有用户才能提供的私有全文，则主控按真实
外部资源阻塞处理，不伪造批准。

若新增 >5 篇高相关论文：本包范围失控，标
`BLOCKED_STEP35_NONCONVERGENCE`，不主观砍成 5 篇。

### B4. Round 2 与 Round 3

- 只从新 `必读/建议读` 全文中的术语/直接 competitor 构造最多 3 条 refinement
  query；每条仍使用 `s2 openalex` 与相同年份/文档类型合同。
- 每轮输出文件名为
  `q14-step35-r2-qN.json` / `q14-step35-r3-qN.json`。
- 每轮都重复 identity/route/priority；新高相关论文走 B3。
- 某轮新增 `必读/建议读=0` 即收敛并停止。
- Round 3 后仍新增高相关论文：
  `BLOCKED_STEP35_NONCONVERGENCE`。用户已将当前路线选择委托给 Goal
  主控，因此 executor 不请求用户判断，主控按 R008 轮换。

---

## 5. Phase C — 判据 2 裁决

### C1. PASS 的必要且联合条件

只有以下四项同时有明确全文/abstract 证据，才能建议
`PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO`：

1. 某个冻结的 dual-pol coherent condition 下，tuned conventional CMA
   存在稳定剩余失真，不是单纯未调参/短 warm-up/标签置换；
2. 该剩余信息在 runtime 可由严格因果 receiver-visible
   `z_CMA/trace/context` 获得，不依赖 TX truth、future、true channel 或 oracle；
3. 输出收益至少落到 decision/soft-information/收敛或 complexity 指标之一，
   不只是 residual MSE；
4. task-matched CMA+DD-LMS/RDE/simple residual DSP 未覆盖同一收益，或文献给出
   可证伪的结构性理由说明为何未覆盖。

### C2. 必须轮换的条件

以下任一成立：
`BLOCKED_PROBLEM_EVIDENCE_ROTATE`：

- 判据 2 仍 UNKNOWN；
- 证据中的 residual gain 只来自 Kerr/器件非线性，而当前冻结 C 不含该机制；
- runtime 增量依赖 TX truth/pilot/oracle/future，无法转成 receiver-visible；
- 只有 residual MSE，无 decision/soft/收敛/complexity 增益；
- tuned CMA+DD-LMS/RDE/simple rule 已吸收同一增量；
- 无法冻结单一 C，仍把 PCS、SOP、fading、PMD/Kerr 拼成一个宽泛条件。

“没有 direct precedent”本身既不是 PASS，也不是 FAIL。

### C3. 单一 C 与 comparator 建议

若 PASS，必须在 worker log 给出唯一建议的：

```yaml
M:
C:
A:
legal_runtime_information:
output:
primary_metric:
fair_comparator:
cheap_alternative:
claim_ceiling:
```

若 FAIL/UNKNOWN，也必须指出最小失败机制和下一轮换点。不得设计或运行 MVE。

---

## 6. Phase D — 文档与闭包

### D1. literature_notes 更新

只有形成七个 terminal 状态之一时，更新
`projects/thesis-fso/literature_notes.md`：

- 新增 `Q14 Step 3.5 定向补检（2026-07-27）` 小节；
- 记录关键词矩阵、actual sources、core DOI 双向引用链、轮次与收敛结果；
- 新论文仅写真实读取字段与路径；
- 更新 Q14 判据 2 为 `PASS`、`FAIL` 或 `UNKNOWN`；
- 不把全局 Step 3.5 行改成无条件 PASS；只标 Q14-specific 状态；
- 不更新 master-state、formal owner 或任何 `.sessions` 文件。

### D2. worker log 强制结构

`projects/thesis-fso/worker-logs/step-018-q14-step35-problem-evidence-closure.md`
必须包含：

```markdown
# step-018 Q14 Step 3.5 worker log
## Start receipt
## Existing evidence inventory
## Keyword matrix and raw receipts
## Core-paper selection and bidirectional citation receipts
## Actual-source and identity audit
## Round-by-round priority/convergence table
## New-paper acquisition/read receipts
## Coverage-gap report and delegated gate receipt
## Criterion-2 adjudication
## Single-C and comparator recommendation
## literature_notes diff receipt
## Protected-path and git closure
## Terminal report
```

### D3. terminal report

```text
terminal_status=<one of the seven frozen terminal statuses>
execution_phase=<A|B1|B2|C|D>
formal_science_disposition=<BLOCKED_FORMAL_READINESS|PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO>
mission_method_delta=NONE
criterion2=<PASS|FAIL|UNKNOWN|NOT_REACHED>
actual_source_families=<list>
semantic_scholar_present=<TRUE|FALSE>
other_source_family_count=<int>
forward_chain_count=<int>
backward_chain_count=<int>
rounds_completed=<1|2|3>
last_round_new_must_or_advised=<int>
new_fulltexts_acquired=<int>
new_fulltexts_read=<int>
identity_quarantine_count=<int>
coverage_gate=<NOT_REQUIRED|MASTER_APPROVED>
STEP4A_AUTHORIZED=FALSE
METHOD_SIGNAL=FALSE
same_axis_streak_proposed=1
repair_streak_proposed=0
no_method_streak_proposed=18
anomaly=<one line or NONE>
```

continuation receipt 使用下列最小 schema，严禁提前写
`formal_science_disposition`、streak 或 `no_method_streak_proposed`：

```text
continuation_status=<BLOCKED_EXECUTION_TIMEBOX|AWAITING_DELEGATED_COVERAGE_GATE>
execution_phase=<A|B1|B2|C|D>
coverage_gap_report=<path|NOT_APPLICABLE>
next_same_task_action=<one line>
anomaly=<one line or NONE>
```

---

## 7. 禁止路径

- 禁止运行 `projects/simulation/`、direction-lab Probe/Scout、任何 seed/MVE；
- 禁止修改 common/params/Skill/controller、现有 evaluator 或旧 search raw；
- 禁止修 T008/B1、T010/B10、T016/C15、T017/C16；
- 禁止恢复 P03/science-scout；
- 禁止进入 Step 4a A0/A′/A/B/D、Step 5、Contract 或 Execute；
- 禁止把 Step 3.5 PASS、problem-evidence PASS、negative result 或文献收敛写成
  `CONSTRUCT_CREATED`、`FAIR_COMPARISON_RUN`、`METHOD_SIGNAL` 或论文方法。

---

## 8. 主控验收清单

- [ ] task-control 在执行前 PASS，且执行未越过 epoch46/CP017；
- [ ] 六个冻结 Round-1 组合全部执行，未增第七条；
- [ ] actual source 含 Semantic Scholar + 至少一源；
- [ ] 同一 core DOI 的 forward/backward chain 均有 raw receipt；
- [ ] identity、route、priority 与 evidence scope 可从 raw 重算；
- [ ] 新必读/建议读全部按 acquire/read 处理，未用 abstract 冒充全文；
- [ ] acquisition 后先形成 coverage-gap report 并暂停；独立 verifier 与
  delegated master gate 的磁盘 receipt 在精读前存在；
- [ ] 最后一轮新增必读/建议读=0，或如实记录 Round-3 nonconvergence；
- [ ] criterion 2 的 PASS 满足 C1 四项联合条件；否则 fail-closed 轮换；
- [ ] 无实验、实现、Step 4a、Scout/P03 或旧路线修补；
- [ ] `mission_method_delta=NONE`，没有把 formal/negative/evaluator 工作冒充方法；
- [ ] executor 未修改 control/formal/current owner；authorized diff 与 protected
  hash 闭合；
- [ ] 独立 verifier 可从 raw、paper paths、literature diff 与 worker log 复算。

## 附：回传

执行方只回传：

```text
STATUS=<terminal or continuation>
WORKER_LOG=projects/thesis-fso/worker-logs/step-018-q14-step35-problem-evidence-closure.md
LITERATURE_DIFF=<none|path>
ANOMALY=<one line>
```
