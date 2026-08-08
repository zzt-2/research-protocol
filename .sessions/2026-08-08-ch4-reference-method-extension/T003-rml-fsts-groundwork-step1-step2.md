# Task Brief: RML-FSTS Groundwork Step 1–2

> 来源: S001 | 产出位置: 新建独立专题 `.sessions/2026-08-08-rml-fsts-groundwork/`
> 日期: 2026-08-08
> 唯一文档: 执行方必须完整读取本文件；只可读取本文件列出的权威规范、项目文件、搜索缓存和论文库

---

## 0. TL;DR（执行方先读）

你在 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。上游 Ch4 控制专题已经选择唯一 research object：**RML-FSTS fixed-lag/`BL` condition-dependence**。当前只有 source-domain defect 与 FSO transfer hypothesis，目标星地 lag-ranking crossover 尚未成立，object/package failure 计数仍为 `0/0`。上游预注册的 0.5–1 天 defect smoke 只是未来 Step 4a 合同，本轮绝对不运行。

**你的任务**：先查 `.sessions/_registry.yaml` 防重复，然后创建独立 `2026-08-08-rml-fsts-groundwork` 专题；在同一对话严格依次完成正式 Groundwork **Step 1 检索+初筛** 与 **Step 2 全文获取+覆盖面缺口报告**，到用户覆盖面确认关口立即停止。

**产出**：独立专题的 topic-index/S001/R001/R002/D/V/H、RML-FSTS 专属 literature owner、Step 1 search artifacts、Step 2 CORE 全文与 coverage receipt，并同步 `projects/thesis-fso/master-state.md`。最终独立 verifier 通过后统一 commit，一律不 push。

**最高纪律（违反一条就废了）**：

1. 本轮只做 GW Step 1–2。严禁 Step 3/3.5/4a、Q# 裁决、预注册 smoke、方法设计、实现、仿真、MVE、Contract 或 Execute。
2. source defect 只允许写成：Wang 2023 FSTS 的 fixed lag/`BL` 取值依赖 modulation/training length/received power，低功率存在 timing/FOE 退化。星地 lag-ranking crossover 仍是待证伪假设，不能写成已观察事实。
3. future action `receiver-visible reliability-weighted multi-lag circular fusion` 只作为后续可能形态背景；不得在 Step 1–2 设计、实现、验证或宣称新颖。
4. 最强廉价替代必须保留为未来的 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup；不得只与论文 fixed `BL` 或 global lag 比较。
5. 不并行启动 BUM-CMA，不补新 research object，不复活 K01/B10/B3-Q2/C3/P09/P1/oversampled-Q1 等 exact historical object。
6. 主线程不得直接 WebSearch/WebReader。检索只用项目 `tools/search`/`tools/blit`；全文消化、批量 abstract/引用链筛查必须委托 fresh-context subagent，主线程只接收结构化摘要。
7. 下载严格按 `gw-acquire.md` 止损；不绕付费墙、不抓 ResearchGate/Semantic Scholar 页面、不自行写 PDF 转换脚本。
8. 不修改 Skill、科学代码、仿真参数、正式论文、旧 dormant topic 或 protected history；四个既有 `p05_run*.log` 不修改、不暂存。一次统一 commit，不 push。
9. Step 1 未过、Step 2 覆盖不足或下载受阻都只是 Groundwork 门控结果，不计 research-object failure、method-bearing package failure 或 defect-smoke failure；只有未来真正执行且 evidence-valid 的 smoke/package 才能改变计数。

---

## 1. 权威背景与恢复验证

### 1.1 开始前必须完整读取

1. `.sessions/2026-08-08-ch4-reference-method-extension/topic-index.md`
2. 同专题 `decisions.md` 的 D004、`R002-reference-source-expansion.md`、`H003-reference-source-expansion-result.md`
3. `stages/groundwork.md`、`stages/gw-search.md`、`stages/gw-acquire.md`
4. `domain-comms.md`、`tools-guide.md`
5. `.sessions/profile.md`；并调用 `session-governance` 与 `research-direction-lab` skill 做 session start / scope 报到
6. `projects/thesis-fso/master-state.md` 的 frontmatter、当前控制面桥接与 `GW Progress`
7. `papers/_read_notes/10.1109_jphot.2023.3265847.md` 与其指向的共享全文；已有共享论文库可只读复用

### 1.2 H003 接收验证

执行前逐条验证并写入新专题 S001：

- D004 terminal 是否为 `ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`；
- R002 是否明确 source defect 不等于目标 FSO defect 已成立；
- object/package failure 计数是否为 `0/0`，且当前没有 smoke 授权；
- registry 是否不存在同名或同 research object 的 active/dormant 独立 Groundwork 专题。

任一 FAIL 立即停止，不自行修历史。若 registry 已有同方向未 closed 专题，续用既有专题；不得创建重复专题，并在最终回报实际 slug。

### 1.3 新专题合同

确认无重复后创建：

`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/.sessions/2026-08-08-rml-fsts-groundwork/`

必须包含：

- `topic-index.md`：原始目标、当前范围、明确不含、范围变更记录、不变量、其他结论、进展、未决项、当前位置；
- `S001-step1-step2.md`：本轮目标、H003 验证、Step 1/2 过程、决策引用、范围确认、后续；
- `decisions.md`：D001 冻结独立专题范围；按结果追加 D002 记录 Step 1/2 terminal；
- `verifications.md`：V001 独立终验；
- `H001-step2-coverage-stop.md`：只交接覆盖面状态与用户确认动作，不写 Step 3 执行指令；
- `.sessions/_registry.yaml` 新条目，`depends_on` 指向 `2026-08-08-ch4-reference-method-extension`，`conflicts_with: []`。

独立专题创建后，上游 Ch4 控制专题转 `dormant`，只保留 D004/R002 作为来源，不在其中继续科学执行；在其 S001 追加“T003 完成与新专题路径”，并更新上游 topic-index/registry current view。不得改写上游历史 D/V/R/H。

---

## 2. GW Step 1 — 检索与初筛

### 2.1 冻结 research object

Step 1 只围绕一个对象：

- **M**：Wang 2023 双偏振 FSTS frame/FOE 链中的 fixed lag/`BL` two-stage FSTS FOE；
- **C（待精读后重判）**：星地相干 FSO 的低接收功率、湍流/空间分集、modulation 与 training-length 条件变化；
- **A（待证伪假设）**：单一 fixed lag 或只按 modulation/TS/power 条件化的 single-lag policy 可能无法覆盖同一可见条件内的 lag-ranking 变化。

这只是 Step 1 检索锚点，不是合法 Q#，不许在本轮判 PASS/FAIL 或设计方法。

### 2.2 一轮检索

先复用：

- `search-archive/2026-08-08/` 的 T002 四组缓存与 receipt；
- `search-archive/_index/all-papers.jsonl`；
- `papers/`、`papers/_read_notes/` 和现有 carrier-sync/oversampled-sync literature notes。

复用结果必须重新做数量、来源、年份、发表状态和覆盖度核查；不得把 T002 的 entry-screening 直接冒充正式 Step 1。

至少构造 3 组不同角度的 query，并从 worktree 根目录用 `bash tools/search ... --mode academic`（推荐 `--preset problem-driven` / `scenario-method`）检索，每源目标 ≥15 条：

1. FSTS / training-sequence fixed-lag、`BL/BN`、fine CFO estimation 的参数依赖与低功率边界；
2. multi-lag / stepwise / autocorrelation / correlation-distance CFO estimators 的范围—精度—方差权衡；
3. coherent FSO spatial diversity、turbulence、low received power 对 frame/FOE/correlation reliability 的影响。

所有 JSON 必须由工具写入 `search-archive/2026-08-08/{slug}.json`。记录 query、requested/actual source、raw/dedup、cache SHA256；实际 0 命中源不计覆盖源。

### 2.3 AI 初筛与二轮定向检索

对合并去重后的每条候选按 title+abstract+venue+year+citation+publication_status 做语义审查，写回 `priority` 与 `priority_reason`。不得使用脚本 relevance score 代替 AI 审查。

初筛必须覆盖至少两个技术路线：

- 路线 A：task-matched FSTS/training-aided two-stage FOE、fixed/variable correlation lag；
- 路线 B：multi-lag/stepwise/correlation-distance CFO estimation 与 strongest conditioned single-lag comparator；
- 路线 C 可作为物理迁移支撑：FSO low-power/turbulence/spatial-diversity synchronization reliability。

从初筛中选择至少 2 个路线，每路线再做 ≥2 组方向专属 query。为控制工作量，本轮总 query group 上限为 **7**（一轮 3 + 二轮 2×2）；达到上限后不得继续补搜。二轮只验证论文池、直接竞品与路线覆盖，不宣称 novelty 已关闭。

### 2.4 Step 1 质量门

全部满足才标 Step 1 PASS：

- 去重候选 ≥20；
- 实际贡献结果的独立搜索源 ≥3；
- 必读 ≥5；
- 至少 2 个技术路线均有独立定向检索支撑，无明显方向空洞；
- 至少 1 个路线的定向检索在 metadata/abstract 层支持“仍有待精读核验的具体 gap hypothesis”；必须写出 exact claim boundary，不得把它升级为 novelty closure；
- 正式发表文献占全部去重候选 ≥50%，`unknown` 不计 published；
- Wang 2023 source reference、2019+ task-matched baseline/competitor、multi-lag/stepwise prior art、FSO transfer physics 均进入候选池；缺一类须显式列 coverage gap。

若 Step 1 不通过：terminal=`STEP1_GATE_FAILED_STEP2_NOT_RUN`，不得进入 Step 2；完成 D002/V001/H001/current-view 后停止。

该 terminal 只表示正式检索门未闭合，不证明 fixed-lag defect 不存在，也不消耗对象/方法包失败计数。

### 2.5 Step 1 产出

- `search-archive/2026-08-08/` 下原始 JSON、合并/审查 receipt；
- 新专题 `R001-step1-search-and-screen.md`：检索口径、优先级统计、三路线覆盖、direct-competitor 预警、Step 2 shortlist；
- `projects/thesis-fso/literature_notes_rml_fsts.md`：只建立 owner、GW Progress 与 Step 1 候选表，不做全文方法结论；
- 同步 `projects/thesis-fso/master-state.md` frontmatter/current bridge/GW Progress：RML-FSTS Step 1 完成，Step 2 状态按实际；不得覆盖历史行。

---

## 3. GW Step 2 — 获取、转换与覆盖面门

仅在 Step 1 PASS 后执行。

### 3.1 shortlist 与 CORE 定义

从 Step 1 的“必读+建议读”筛选约 8–12 篇。CORE 必须直接支撑至少一类：

1. Wang 2023 FSTS source baseline/defect identity；
2. task-matched training-aided/FSTS/fixed-variable-lag FOE comparator；
3. multi-lag/stepwise correlation CFO estimator 或 strongest single-lag alternative；
4. coherent FSO low-power/turbulence/spatial-diversity 对同步相关量的影响。

纯一般 CFO、非 coherent/非相关估计且无可迁移机制、只做 CPE/PLL、只有标题碰词的论文不计 CORE。

### 3.2 获取与止损

先查共享论文库，存在合格 `content.md` 的跳过下载并记录 absolute path+SHA256。共享库 `D:/code/study/research-protocol/papers/` 可只读复用，不复制、不改写；新增获取仍从 worktree 根目录使用项目工具。

对缺失论文严格执行：

1. `tools/download ... --dry-run`；
2. 第一轮 `tools/download` 批量获取 OA/arXiv/Unpaywall；
3. 第二轮只对失败项查正式 arXiv/作者稿并重试；
4. IEEE/CNKI 缺口按 `gw-acquire.md` 使用一次 `tools/blit --download` 专用轮；
5. 仍失败即停止，进入 coverage gap，不用 WebReader/ResearchGate/Semantic Scholar 页面替代全文。

转换必须用 `tools/convert`；不得自写 pymupdf 脚本。每篇核验 identity、provenance、SHA256、PDF bytes 与 `content.md` 有效行数。`content.md <50` 行、反爬页、只有标题/目录或大面积乱码均不合格。

### 3.3 Step 2 覆盖门与终态

创建 `projects/thesis-fso/rml-fsts-groundwork/step2-coverage-report.md`，列出：

- 成功获取及各自 CORE 类别；
- 内容质量不合格项及原因；
- 三轮后失败项、DOI/来源、重要性与用户手动获取动作；
- 正式发表/预印本/unknown 统计；
- 四类 CORE 覆盖矩阵与系统性偏差；
- receipt：source/content SHA256、行数、identity、provenance。

终态只能取其一：

- `STEP2_READY_FOR_USER_CONFIRMATION`：≥5 篇合格 CORE，且 Wang 2023 source baseline + 至少 1 篇 2019+ task-matched comparator + 至少 1 篇 multi-lag/stepwise prior art + 至少 1 篇 coherent-FSO transfer paper 均有合格全文；仍须用户确认，不能自动进 Step 3。
- `STEP2_BLOCKED_BY_COVERAGE_GAP`：合格 CORE <5，或上述四类任一没有合格全文；列出最小人工补件集合。
- 若 Step 1 失败，则保持 `STEP1_GATE_FAILED_STEP2_NOT_RUN`，Step 2 产出写 `NOT_RUN`，不得伪造下载失败。

不论 READY 或 BLOCKED，本轮都在 Step 2 覆盖面报告后硬停止。`READY` 只表示可交用户确认，不是 Step 3 授权。
`BLOCKED` 同样不构成对象失败或方法失败，不允许借覆盖缺口关闭 RML-FSTS research object。

### 3.4 Step 2 产出

- 合格全文：`papers/{arxiv|doi|manual}/{id}/content.md` 或已验证共享绝对路径；
- 新专题 `R002-step2-acquisition-coverage.md`；
- `projects/thesis-fso/rml-fsts-groundwork/step2-coverage-report.md`；
- `search-archive/2026-08-08/rml-fsts-step2-acquisition-receipt.json`；
- literature owner 与 master-state 的 Step 2 状态同步；Step 3 必须保持 `⬜/NOT_STARTED`。

---

## 4. 治理、独立验证与提交

### 4.1 新专题 current view

新专题 topic-index 必须冻结：

- 原始目标：验证 RML-FSTS fixed-lag condition-dependence 是否能经完整 Groundwork 成为 Ch4 方法入口；
- 当前范围：仅 Step 1–2；
- 明确不含：Step 3/3.5/4a、smoke、future action 设计/实现、仿真、METHOD_SIGNAL/Go/Kill；
- 不变量：source/target defect 分离、strongest conditioned lookup、exact collision 边界、0/0 计数；
- 当前位置：与三种 terminal 之一完全一致。

### 4.2 独立 fresh-context verifier

executor 完成后必须另派未参与生成的 verifier，逐项读取实际文件并检查：

1. registry 查重与新专题结构；
2. H003 三条事实验证；
3. Step 1 query 数、raw/dedup、actual source、published ratio 与 priority 从 JSON/receipt 可复算；
4. 一轮+二轮、≥2 路线、≤7 query 与质量门；
5. Step 2 每篇 identity/provenance/SHA256/bytes/≥50 行；
6. CORE 四类与关键缺口裁决；
7. terminal 唯一且符合门控；
8. literature owner 与 master-state GW Progress 一致，Step 3 未启动；
9. 无 abstract 冒充全文结论，无 source defect→target fact 偷换；
10. 无 Step 3/3.5/4a/smoke/实现/仿真；
11. 上游专题只做 current-view 交接，历史 D/V/R/H 未改写；
12. git diff scope、YAML、`git diff --check`、p05 日志哈希/no-stage、no-push。

verifier 结论必须为 PASS/FAIL/PARTIAL，并给 P0/P1/P2。允许一次最小修复轮；修复后同一 verifier 重新检查。仍有 P0/P1 或 terminal 承重缺口则不得提交完成态。

### 4.3 单次提交纪律

- 本对话只允许一次统一 commit，包含 Step 1–2、治理同步与 verifier 结果；不 push。
- 不提交搜索 API key、cookie、浏览器会话、缓存临时文件或四个 `p05_run*.log`。
- 搜索 JSON、acquisition receipt 与必要 coverage 证据按项目既有规则处理；被 gitignore 但对后续承重的 receipt 必须按既有先例显式纳入或在 H001 给出可复现位置与 SHA。

---

## 5. 最终回复格式（只给五项）

1. 新专题路径、H003 接收验证与 Step 1 terminal；
2. Step 1 query/source/raw/dedup/priority/路线覆盖与 shortlist；
3. Step 2 合格 CORE 全文、失败项、四类覆盖与最终 terminal；
4. 是否进入 Step 3/3.5/4a、是否运行 smoke/实现/仿真、当前 object/package 计数；
5. R/D/V/H、literature owner、coverage report、search/acquisition receipts、verifier、commit SHA 与下一合法动作。

---

## 6. 验收清单

- [ ] registry 无重复后才创建独立专题；topic-index/S/D/V/H 齐全；
- [ ] H003 三条事实与依赖/conflict 已验证；
- [ ] Step 1 满足正式 gw-search 流程，一轮+二轮均完成或诚实 FAIL；
- [ ] query group ≤7、候选 ≥20、actual source ≥3、必读 ≥5、published ≥50%、路线 ≥2；
- [ ] Step 1 PASS 后才执行 Step 2；
- [ ] Step 2 shortlist 约 8–12，工具链/止损/内容质量/receipt 合规；
- [ ] READY 时 ≥5 CORE 且四类全文覆盖齐；否则 BLOCKED/NOT_RUN；
- [ ] coverage report 后停止，Step 3 始终未授权；
- [ ] source defect 未偷换为目标 FSO fact，future action 未被设计或验证；
- [ ] master-state 与 literature owner GW Progress 一致；
- [ ] 独立 verifier 通过，终态唯一；
- [ ] 一次 commit、未 push、p05 logs 未修改未暂存。

---

## 附：关键路径

- 上游控制专题：`.sessions/2026-08-08-ch4-reference-method-extension/`
- 新专题：`.sessions/2026-08-08-rml-fsts-groundwork/`
- 新专题主产出：`R001-step1-search-and-screen.md`、`R002-step2-acquisition-coverage.md`
- 文献 owner：`projects/thesis-fso/literature_notes_rml_fsts.md`
- 覆盖报告：`projects/thesis-fso/rml-fsts-groundwork/step2-coverage-report.md`
- 搜索/获取 receipt：`search-archive/2026-08-08/`
