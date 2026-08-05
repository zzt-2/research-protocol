# Verifications — Shared M0-Power FOE–CPE Groundwork

> 本专题验证记录。V### 按编号排列，每条关联 S### 或 D###，结论必须是 PASS/FAIL/PARTIAL 三选一。

## V001: T008 Step 1–2 产物初审（acceptance repair 入口）

> status: PARTIAL
> date: 2026-08-05
> 关联：S001（acceptance repair 续接段）/ T008
> 验证者：本对话主线程（非独立上下文）
> 验证对象：S001 / H001 / topic-index / literature_notes_shared_m0_foe_cpe.md /
>   step2-coverage-report.md / _p1-competitor-shortlist.md / master-state.md（§2 P1 条目 + frontmatter）/
>   _registry.yaml / _step2_receipt.json / 12 篇 papers/doi/ 全文

### 结论

**PARTIAL** —— 初审发现 T008 Step 1–2 产物在统计口径与措辞上存在缺陷，需修复后再由独立
fresh-context verifier 做了 V002 复核。

### 发现的缺陷

1. **统计口径虚高（current-view 文档多处）**：
   - 原写"4 API 源（S2/OpenAlex/SerpAPI/Exa）+ 正式发表占比 ~97%"。实测
     `search-archive/2026-08-05/_r1_merged_shortlist.json`：`raw_total=100`、`dedup_total=97`。
     source_api 计数：semantic_scholar=51、serpapi_scholar=23、openalex=10（+ 合并源若干），**Exa 贡献 0**
     （不存在 exa 源记录）。4 查询通道均被调用，但实际贡献候选的 API 源只有 3 类。
   - publication_status 计数：published=59 / unknown=36 / preprint=2。**原"~97%"把 unknown 也按已发表
     计入，属虚高**。可直接证明的正式发表率下限 = 59/97 = **60.8%**（仍通过 ≥50% 门；unknown 不计入
     分母，不冒充已发表）。
2. **过度措辞（novelty 倾向）**：
   - S001 / `_p1-competitor-shortlist.md` 原写"领域内近乎空集 / 对 P1 新颖性有利 / 没有论文显式提出 …"。
     在 Step 1–2（metadata/abstract 级，Step 3 未授权）阶段写 novelty 倾向性结论，违反 topic-index
     "明确不含：不把'没人题名相同'写成 novelty"。须降级为中性表述。
3. **残留 stale 口径**：
   - S001 后续段、H001 多处仍写"当前 5 篇合格全文 / 仍需补两篇直接竞品 / 用户需手动获取直接竞品"，
     与 blit 第三轮已补取 7 篇 IEEE（含 2 篇 HIGH★ 直接竞品）、当前为 12 篇合格全文的事实矛盾。

### 修复动作（本对话完成）

- 统一统计口径为：raw=100 → dedup=97；4 查询通道均调用、实际贡献候选 API 源 3 类（Exa 贡献 0）；
  published 59 / unknown 36 / preprint 2；正式发表率下限 59/97 = 60.8%。
- novelty 倾向措辞统一降级为："当前 metadata/abstract 检索未发现明确覆盖；不得据此判断新颖性，
  须由 Step 3 全文精读验证"。
- 清除 stale "5 篇 / 补两篇 / 手动获取"口径，统一为 12 篇合格全文含 2 篇 HIGH★ 直接竞品。
- master-state.md frontmatter：`current_step` 指向 P1 Shared M0-Power GW Step 2 coverage accepted；
  `current_stage` = GROUNDWORK（不再写 DORMANT）；§2 把 P1 设为当前现行入口，dormant campaign 降为
  历史背景（不再称"唯一现行入口"）。

### 未越界声明

- repair 只动 current-view 文档措辞与统计口径；未进 Step 3、未新增检索、未下载论文、未实现、未仿真、
  未改 Skill/common/params、未动 4 个 `p05_run*.log`、未 amend 3495bb4。

### 下一步

修复后由独立 fresh-context verifier 执行 V002（复核 12/12 PDF SHA256/行数/identity/统计口径/
current-view 一致性/Step 3 未越界/禁区未污染）。V002 PASS → 终态升级为
`STEP2_ACCEPTED_READY_FOR_STEP3`。

> 注：V001 由本对话主线程做出，**非独立上下文**，故结论 PARTIAL，不单独作为终态依据；终态由
> V002 决定。

---

## V002: T008 acceptance repair 独立复核（fresh context）

> status: PASS
> date: 2026-08-05
> 关联：V001 / S001 acceptance repair 段
> 验证者：独立 fresh-context verifier agent
> 验证对象：`_step2_receipt.json`（12 条）+ 12 篇 `papers/doi/{dir}/source.pdf|content.md` +
>   `_r1_merged_shortlist.json` + 4 个 `r1-*.json` + S001 / H001 / topic-index /
>   `literature_notes_shared_m0_foe_cpe.md` / `step2-coverage-report.md` /
>   `_p1-competitor-shortlist.md` / `master-state.md`（frontmatter + §2）+ `_registry.yaml`

### 结论

**PASS**（8/8 项全过；终态升级为 `STEP2_ACCEPTED_READY_FOR_STEP3`）。所有数字均由本 verifier 从
primary source（`_step2_receipt.json`、`_r1_merged_shortlist.json`、12 篇 PDF/content.md、git status）
重算，未采信文档中的任何自述。

### 逐项复核（8 项）

| # | 项 | verdict | 证据（file:line + 数字） |
|---|---|---|---|
| 1 | 12/12 PDF SHA256 + 行数 + identity + qualified | **PASS** | `_step2_receipt.json` 12 条逐篇重算：12/12 SHA256 全等、12/12 `pdf_bytes` 全等、12/12 `content_lines` 全等、12/12 `qualified==true`、12/12 行数 ≥50（最小 137 行 `10.2991_icmmita-16.2016.71`，最大 984 行 `10.1109_jlt.2009.2024963`）。identity 逐篇读 content.md 首部核对：标题/作者/venue 与 receipt 一致（含 `10.1109_lcomm.2026.3653195` receipt 标题"Prefix-Sum and CT-MLE"对应 content.md "Prefix-Sum+CT-MLE"，同义）。 |
| 2 | Step 1 统计（从 JSON 重算） | **PASS** | `_r1_merged_shortlist.json`：`raw_total=100`、`dedup_total=97`、`candidates` 数组 len=97。`source_api` distinct 7 种，但**含 "exa" 的候选 = 0**；折叠复合源后实际贡献 API 家族 3 类：semantic_scholar=58、serpapi_scholar=35、openalex=17（注：含 openalex+openalex 等）。`publication_status`：published=59 / unknown=36 / preprint=2；下限 = 59/97 = **60.8%**（过 ≥50% 门，unknown 不计入分母）。4 个查询通道文件齐全：`r1-fso-sat-coherent-carrier.json` / `r1-hw-efficient-cpr-optical.json` / `r1-joint-cfo-cpe-lowcomplexity.json` / `r1-vv-mthpower-foe-cpe.json`。 |
| 3 | receipt ↔ paper-dir 一致性 | **PASS** | receipt 12 个 `dir` 全部存在于 `papers/doi/`，且各自 `source.pdf`+`content.md` 齐全。receipt `qualified=true` 恰 12 条；coverage-report §1 表与 `_p1-competitor-shortlist.md` 均只就这 12 篇下合格判定，无超额声明。其它 11 个含 pdf+md 的 paper 目录（如 `10.1038_s41377-023-01201-7`、`10.1109_ojcoms.2024.011100`）属历史专题资产，不在 P1 Step2 claim 范围。 |
| 4 | current-view 统计措辞一致性 | **PASS** | 6 个目标文件 grep：`4 API 源`/`4 个 API 源`/`S2/OpenAlex/SerpAPI/Exa`（作现源列表）/`~97%`（作现正式发表率）/`正式发表占比 ~97%`/`近乎空集`/`对 P1 新颖性有利`/`没有论文显式提出`（作现结论）—— 作为 **CURRENT 事实**的形式 0 命中。唯一命中均在内嵌引号上下文：`S001-step1-step2-execution.md:79` `原写"4 API 源（S2/OpenAlex/SerpAPI/Exa）+ 正式发表占比 ~97%"`、`:84` `原"领域内近乎空集 / 对 P1 新颖性有利 / 没有论文显式提出 …"`、`topic-index.md:97` `修正统计口径（… 而非 ~97%）`。live current claim 统一为"3 API 源（S2/OpenAlex/SerpAPI-scholar，Exa 贡献 0）+ published 59/97 = 60.8% 下限"（H001:14,52 / topic-index:62,73 / literature_notes:32 / _p1-competitor-shortlist:13,15 / master-state:36-37）。`_p1-competitor-shortlist.md:15` 的"正式发表占比"行写的是 **60.8%**（已修正），非旧值。 |
| 5 | stale "5 篇 / 补两篇 / 手动获取" 清除 | **PASS** | 6 文件 grep `当前 5 篇`/`当前5篇`/`仍需补两篇`/`先补 2 篇直接竞品`/`手动补 2`/`用户先手动`/`待用户确认覆盖面` 作为 current state —— **0 命中**。`topic-index.md:96` 的"合格全文 5→12 篇"是 repair 历史叙述（修订块内），非当前状态。`topic-index.md:65`、`S001:87` 当前事实写"12 篇合格全文含 2 篇 HIGH★ 直接竞品，无需再补"。`≥5 篇` 作 gw-acquire 门槛仍出现，属允许。 |
| 6 | master-state.md frontmatter + §2 | **PASS** | `master-state.md:8` `current_step: P1 Shared M0-Power GW Step 2 coverage accepted (STEP2_ACCEPTED_READY_FOR_STEP3；T008 acceptance repair V002 PASS；Step 3 未授权…)`；AMC 仅作"历史背景：…DORMANT"出现，非 primary current step。`:9` `current_stage: GROUNDWORK`（非 DORMANT）。§2（`:30-32`）P1 = "当前现行入口"；2026-08-02 dormant campaign 标注"历史背景"/"不再是'唯一现行入口'"。 |
| 7 | Step 3 未进入 / 禁区未污染 | **PASS** | 6 文件 grep Step3 式全文语义结论（`该论文实现了`/`该论文共享了`/`该论文提出了`/`实现了共享`/`全文证明` 等）= 0 命中。coverage-report 明写"本报告不填写 method/dataflow/competitor 的全文语义结论（属 Step 3）"；competitor-shortlist 全表标 `[META]`、"不当精读结论使用"、"不得据此判断新颖性"、"本轮不得据此宣称 P1 新颖/有效/能成章"。"P1 相关度"列仅复述 abstract 首行短语（允许）。`git status --short`：修改仅限 8 个文档文件（S001/H001/topic-index/literature_notes/master-state/step2-coverage-report/_p1-competitor-shortlist/_registry.yaml）+ verifications.md(新)；**0 改动**于 `.agents/skills/`、`projects/simulation/common/`、`params.py`；4 个 `p05_run*.log` 仅 `??` 未跟踪且 mtime=2026-07-30（早于本轮 repair），未被 T008 触碰；无新检索/下载代码执行。 |
| 8 | registry + topic-index terminal | **PASS** | `_registry.yaml:653-658` slug `2026-08-05-shared-m0-foe-cpe-groundwork`：`last_updated`/`description` 均写 `terminal=STEP2_ACCEPTED_READY_FOR_STEP3`、`Step 3 未授权`、`3 API 源（Exa 贡献 0）`、`12 篇合格全文含 2 HIGH★`（非 `STEP2_READY_FOR_USER_CONFIRMATION` 作 live terminal）。`topic-index.md:88-92` "当前位置" = `STEP2_ACCEPTED_READY_FOR_STEP3`，`Step 3 未授权`；`:53-55` 列出 `STEP2_READY_FOR_USER_CONFIRMATION` 是 schema 允许值清单（非当前值），`:99-100` 明写"终态由 STEP2_READY_FOR_USER_CONFIRMATION 升级为 STEP2_ACCEPTED_READY_FOR_STEP3"。 |

### 发现的缺陷（若有）

无。8 项全部 PASS，无阻塞项。

> 备注两条非缺陷观察（不影响终态）：
> 1. `_step2_receipt.json` 中 `10.1109_lcomm.2026.3653195` 的 receipt 标题"…Using Prefix-Sum and
>    CT-MLE"与 content.md 实际标题"…Using Prefix-Sum and CT-MLE"（content.md 首行作"Prefix-Sum+CT-MLE"）
>    仅连接词差异，语义一致，identity 核对 PASS。
> 2. 4 个 `p05_run*.log` 为 pre-existing 未跟踪文件（mtime 2026-07-30），与本轮 T008 repair 无关；
>    本 verifier 确认未被本轮触碰，不计入禁区污染。

### 终态判定

**PASS → 终态升级为 `STEP2_ACCEPTED_READY_FOR_STEP3`**（V002 独立 fresh-context 复核 8/8 全过）。
Step 3 仍未授权；下一合法动作 = 用户在新对话显式授权后开 Step 3 精读（启动前必读
`stages/gw-read.md`）。本轮不实现、不仿真、不改 Skill/common/params、不重开旧 campaign。

---

## V003: GW Step 3 初版独立结构与边界审查

> date: 2026-08-05
> 关联：S001 / D003
> 验证者：独立 fresh-context verifier agent `/root/step3_verifier`

### 验证项

- [x] title/身份与两篇 direct 原文：9/9 title exact；direct scientific adjudication PASS。
- [ ] gw-read 标准字段/七子表/实验完备性：FAIL；精确字段仅 6/14 全覆盖，七个要求标签与 VVUQ 均 0/9。
- [ ] terminal/治理闭合：FAIL；`STEP3_PARTIAL_NO_Q_CANDIDATE` 在框架定义中 0 命中，V003/H002 被前向引用但当时不存在。
- [x] comparator/Q#/边界/禁区：PASS；Q-P1-01 判据 3 FAIL 有依据，未进入 Step 3.5/4a/实现/仿真。

### 证据

```text
TITLE_EXACT=9/9
READ_LOG=9/9
LABEL[状态空间/动作空间/奖励函数/建模假设/网络架构/适配性分析/问题提取]=0/9
LABEL[VVUQ]=0/9
V003=0
H002=0
S001_IN_PROGRESS=1
TERMINAL_DEFINED=0
FORBIDDEN_DIFF=0
STAGED=0
DIFF_CHECK_EXIT=0
REGISTRY_YAML=PASS
```

原文门控：`stages/gw-read.md` L49–86、L146–160、L198；`stages/glossary.md` L65–70。

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

1. 九份 read note 按标准字段、七个独立子表、实验完备性与 VVUQ 重写；
2. 撤销自造 terminal，状态保持 Step 3 BLOCKED/IN PROGRESS；无合法 Q# 时按 glossary 回 search 扩检索，
   但该动作需用户另行授权，本轮不执行；
3. 去除 V003/H002 前向完成引用；修复后换新的 fresh-context verifier 记 V004，PASS 后方可写 H002。

---

## V004: GW Step 3 修复后独立终审

> date: 2026-08-05
> 关联：S001 / D004
> 验证者：独立 fresh-context verifier agent `/root/step3_verifier_final`

### 验证项

- [x] title/identity/read-log：9/9 PASS；L01–L09 唯一，路径 9/9 存在。
- [x] 结构与证据：标准字段 135/135、规范段落 72/72；五篇实验完备性均值可逐篇复算。
- [x] direct/Q#/状态：CSNDSP/JLT2018 裁决、Q-P1-01 判据 1/2/4 PASS 与 3 FAIL、Step 3
  BLOCKED/IN PROGRESS 及 search→Step 2→Step 3 恢复路径全部 PASS。
- [x] 治理/范围/git：D003→D004 血缘、registry YAML、禁区、未暂存、diff check 全 PASS。

### 证据

```text
NOTE_COUNT=9
UNIQUE_IDS=9
VENUE_UNKNOWN_REASON=9/9
TITLE_SELFCHECK_PASS=9/9
READLOG_PATHS=9/9
TOTAL_FIELDS=135/135
TOTAL_SECTIONS=72/72
FRAMEWORK_TERMINAL_COUNT=0
H002_EXISTS=False
STAGED_COUNT=0
DIFF_CHECK_LINES=0
FORBIDDEN_COUNT=0
YAML_REGISTRY_MATCHES=1
EXPERIMENT_MEANS: statistics=0.4/3 baseline=2.6/3 ablation=2.0/3 VVUQ=2.8/2.2/1.4 baseline_count=2.6
```

审查 HEAD：`65ff349867fa863bb8cd6e8351f164f3231af54b`；复审确认目标文件哈希在审查期间稳定。

### 结论

PASS

---

## V005: bounded evidence closure 独立复验

> date: 2026-08-05
> 关联：S001 / D005
> 验证者：独立 fresh-context verifier agent `/root/p1_closure_reverifier`

### 验证项

- [x] 六组 search artifact：逐个解析 JSON，`total == len(results)`，final=
  `19/30/14/5/1/13`；query/source 与 R002 一致；R002 已把 raw/dedup 标为 worker-reported、
  不可从现有 artifact 重算。
- [x] acquire/OFC 边界：OFC/PTL 两目录均只有 398 B `metadata.json`，状态 `failed/all_failed`、
  `content_file=""`；exact 裁决只能是 `UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`。
- [x] recent fulltext dataflow：JLT 2019 为 estimator/architecture change 且 conventional correlation
  重复已吸收；ISCAS 2022 与 LCOMM 2026 均为 CPE-only；三篇都不是合法 P1 task-matched M。
- [x] Q/terminal：Q-P1-01 为 1/2/4 PASS、3 FAIL；`RECENT_BASELINE_UNAVAILABLE`、
  `SUPPORTING_ONLY`、`mission_method_delta=NONE` 有证据，且未写成 Step 4a Kill/METHOD_SIGNAL。
- [x] 首轮 PARTIAL 四项修复：literature stale 终态 0；S001 时序正确；H003 十个强制锚点齐全；
  R002 evidence limitation 准确。
- [x] 治理/git：registry 56 个专题可解析；当前 topic closed、framework active、依赖存在、
  `conflicts_with=[]`；D004→D005；必须句逐字存在；`git diff --check=0`、staged=0、禁区 diff=0；
  四个 `p05_run*.log` 仅为 `??`。

### 证据

```text
SEARCH_TOTAL_RESULTS=19/30/14/5/1/13
SEARCH_JSON_TOP_KEYS=query,timestamp,sources,total,results
ACQUIRE_OFC=metadata_only,398B,failed,content_file_empty
ACQUIRE_PTL=metadata_only,398B,failed,content_file_empty
RECENT_QUALIFIED_TASK_MATCH=0
Q_P1_01=PASS/PASS/FAIL/PASS
TERMINAL=RECENT_BASELINE_UNAVAILABLE
P1_DISPOSITION=SUPPORTING_ONLY
H003_REQUIRED_ANCHORS=10/10
REGISTRY_TOPICS=56
CURRENT_TOPIC_STATUS=closed
FRAMEWORK_EVOLUTION_STATUS=active
DIFF_CHECK_EXIT=0
STAGED_COUNT=0
FORBIDDEN_DIFF_COUNT=0
P05_COUNT=4
P05_NON_UNTRACKED=0
```

全文行证据：JLT 2019 `content.md:23,43,76,80`；ISCAS 2022 `:35,59-63,79-81,97-101,182`；
LCOMM 2026 `:53,55-67,75-77,95-101,119-131`；JLT 2018 generic collision
`content.md:73-75,89`。完整 verifier 回执见本轮 agent `/root/p1_closure_reverifier`。

### 结论

PASS
