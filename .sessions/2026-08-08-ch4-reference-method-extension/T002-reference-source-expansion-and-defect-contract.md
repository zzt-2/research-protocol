# Task Brief: Ch4 reference-source expansion 与 defect-reproduction 入口合同

> 来源: S001 / D003 | 产出位置: `.sessions/2026-08-08-ch4-reference-method-extension/R002-reference-source-expansion.md`
> 日期: 2026-08-08
> 唯一文档: 执行方必须完整读取本文件；可读取本文件授权的仓库证据和使用项目检索工具，不得自行扩大任务

---

## 0. TL;DR（执行方先读）

你在 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。Ch3 已有 CCISP 主方法，Ch5 已有 select-before-execute 工程方法；Ch4 仍缺一个真实方法章。T001 只证明当前本地两项入口无直接 survivor：Paillier 是旧 K01 exact collision，LBS-RDE 的 FSO defect 未知。T001 没有执行 defect smoke，也不能算两个 research object 已失败。

**你的任务**：通过一次有界本地索引复用与定向检索，比较 2–4 个机制不同的外部 reference baseline，推荐至多 1 个进入下一轮正式 Groundwork Step 1 defect reproduction。

**产出**：`R002-reference-source-expansion.md`。无论有无入口均追加 D004、V003、H003，并更新 S001、topic-index 与 registry；本轮不得实现、仿真或进入 Groundwork。

**最高纪律（违反一条就废了）**：

1. 入口候选不要求目标 FSO defect 预先成立；允许以“外部已发表 defect + 向星地相干 FSO 迁移的物理机制 + 0.5–1 天可证伪 smoke 合同”通过准备门。
2. 本轮只选择 defect-reproduction 入口，不真正运行 smoke，不设计完整方法，不实现、不仿真、不进 GW。
3. 比较 2–4 个机制不同对象，推荐至多 1 个；不得为凑 survivor 降门，也不得制造第 5 个候选。
4. entry screening 不计“每对象 2 包 / 两对象失败”；只有后续已授权 smoke 或 method-bearing package 执行后才计数。
5. exact object/action collision 可拒绝；邻域 prior art 只限制未来 claim，不得泛化成整族禁令。
6. 禁止复活 P1 shared-M0、K01/Paillier FG-DRC、decoder-feedback coded chain、CCISP scalar calibration、C3、oversampled Q1、coded-burst 4b#1、AMC Q-A/Q-B、G1/P09 等 exact historical object。相邻机制可进入，但必须逐项证明不是改名复活。
7. 只使用 receiver-visible、可部署的未来动作设想；truth/genie 只能做未来诊断上界，不能作为动作或 Go 依据。
8. 一次统一 commit，不 push；不修改 Skill、旧 dormant topic、科学代码、正式论文、protected history 或四个既有 `p05_run*.log`。

---

## 1. 背景与权威纠偏（了解即可，不要写成长篇复盘）

D001 冻结 reference-method extension：从可复现 baseline、具体 defect、一个 deployable action 与 fair comparator 生产完整方法包。T001 的 G3 写成“有本地证据，或有低成本可证伪 defect reproduction”，却同时禁止实验；执行时又把未做 smoke 的 LBS-RDE 直接判成对象失败，并把两个入口审计候选计入“两对象停止”。D003 已纠正：entry screening 不是 method-bearing package，当前 terminal 为 `LOCAL_ENTRY_POOL_EXHAUSTED_DEFECT_REPRODUCTION_GATE_REQUIRED`。

以下 T001 事实仍有效：

- Paillier AGC+DPLL / FG-DRC 与旧 K01 方法动作 exact collision，保持 `REJECT`；
- LBS-RDE 的 fiber PMD/SOP defect 不能直接写成星地 FSO defect，当前为 `UNKNOWN`；
- Ch4 方法槽位仍开放，尚未消耗任何正式 object-failure 计数。

本任务不是 Groundwork Step 1。它只扩展候选源并冻结一个“以 defect reproduction 为目标的 Groundwork”入口。若选出胜者，下一对话必须重读 `stages/groundwork.md`，再从 GW Step 1 合法启动；0.5–1 天 smoke 只是未来 Step 4a 的预注册合同，禁止跳过 Step 1–3 直接运行。

---

## 2. 任务详情

### 2.1 启动恢复与防偏检查

开始前完整读取并核对：

1. 本专题 `topic-index.md` 的范围、不变量和当前位置；
2. `decisions.md` D001–D003，特别是 D002 被 D003 取代的边界；
3. `R001-entry-selection.md` 与 `H002-no-entry-strategic-decision.md` 的两项候选事实；
4. `.sessions/_registry.yaml`：本专题 active，旧 RDL system dormant；
5. `.agents/skills/research-direction-lab/references/method-production.md` 的 current method-production rules。

在 R002 开头回答：

- 当前工作是否直接选择一个可进入 defect reproduction 的方法对象？
- 本轮是否把检索/治理扩张到最小入口选择以外？
- 当前 object/package 失败计数是多少，为什么 T001 不计数？

任何权威状态不一致先停止并报告，不自行篡改历史。

### 2.2 候选源扩展预算

执行顺序必须是：本地索引/已有全文优先，缺口明确后才运行定向检索。

1. 复用 `search-archive/_index/all-papers.jsonl`、`papers/`、现有 literature notes、baseline inventory 与 local code/results；
2. 最多执行 **4 组定向 query**，每组围绕一个 baseline defect / action mechanism，不以“FSO new method”泛搜；
3. 使用项目 `tools/search`，至少让 3 个实际结果源有机会返回；如某源 0 命中，诚实记录 requested/actual source，不虚报；
4. 本轮不下载新全文。新命中的承重 defect 只能由结构化 abstract/metadata 支持；abstract 不足就标 `UNVERIFIED`, 不能晋级唯一入口；已有本地 `content.md` 可按需读取；
5. 原始 query、来源、raw/dedup 数字、筛选理由和缓存路径必须写入 R002。不得用主对话直接 WebSearch/WebReader。

允许最多 3 个 fresh-context subagent：baseline/defect、FSO transfer physics、collision/chapter closure 分工；主线程只整合和裁决。论文全文若需读取，必须委托子 agent 并返回结构化摘要。

### 2.3 候选构造边界

候选数必须为 2–4，且 action mechanism 不同。每个候选必须由具体外部 reference baseline 锚定，并填写：

- reference identity 与本地/公开证据状态；
- source-domain 已发表 defect；
- defect 向星地相干 FSO 迁移的物理机制与关键不确定项；
- 下一轮 0.5–1 天 smoke 要证伪什么；
- smoke 的传统 baseline、最强廉价替代与 primary metric；
- 若 defect 成立，恰好一个可部署 action 的占位身份；
- exact collision 检查与邻域 prior-art claim ceiling；
- 最小 testbed readiness 与预计总方法包预算。

不得从内部 supporting leftovers 先起方法名再倒找论文。不得把“不同场景”本身当 defect，也不得把“外部论文有效”当目标 FSO 必然失效。

### 2.4 defect-reproduction 准备门

每个候选逐门判定：

| 门 | PASS 标准 |
|---|---|
| E1 External reference | 有具体 2019+ 主流论文/权威 baseline；已有本地全文或 abstract 足以支持 source-domain defect |
| E2 Published defect | 外部证据明确描述 baseline 在某条件下的可测失败，不是“没人做过”或纯性能排名 |
| E3 FSO transfer mechanism | 有物理/信号链因果路径说明该 defect 为什么可能在目标 FSO 出现；只要求可证伪，不要求已成立 |
| E4 Smoke contract | 0.5–1 天内可完成，写清冻结 cell/输入、传统 baseline、廉价替代、primary metric、PASS/FAIL 与退出条件 |
| E5 One future action | defect 成立后有恰好一个 receiver/deployment-visible action；非 truth/genie、纯 scalar retune、纯审计或算账 |
| E6 Collision boundary | 无 exact historical object/action collision；邻域 prior art 已列为 claim ceiling 而非整族 Kill |
| E7 Chapter path | 若 smoke PASS 且后续方法有效，可形成方法名、算法/流程、主图、消融、复杂度与边界 |
| E8 Budget | smoke 0.5–1 天，之后最小方法包总预算 3–7 天；超出则 `INFRASTRUCTURE_DECISION_REQUIRED`，不是科学 Kill |

只有 E1–E8 全过才可标 `READY_FOR_GW_STEP1_DEFECT_REPRODUCTION`。若多个全过，按以下顺序选唯一入口：source defect 强度 > FSO transfer 可证伪性 > testbed readiness > action 区分度 > chapter closure > 工期。未选中的全过候选只留 `RESERVE`，本轮不并行启动。

若无候选全过，terminal=`NO_DEFECT_REPRODUCTION_ENTRY_AFTER_BOUNDED_SOURCE_EXPANSION`，只说明具体缺口；不得据此宣称整个 FSO/接收机范围耗尽，也不得把 entry screening 计入 object-failure。

### 2.5 本轮结束边界

- 有胜者：terminal=`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`；这不是 Q#、Go、METHOD_SIGNAL、defect 成立或方法成立。下一轮只从 GW Step 1 开始，不能直接跑 smoke。
- 无胜者：使用 §2.4 的 bounded-source terminal；交回用户决定下一 source/object 范围，不自动继续第 5 个候选。
- 不运行 smoke，不创建科学 runner/artifact，不修改仿真参数，不进入 GW、Contract 或 Execute。
- 不改 Skill、formal owner、旧 dormant topic 或论文正文。
- 由独立 fresh-context verifier 检查入口门、证据来源、exact-collision、范围纪律与计数语义。

---

## 3. 产出格式（强制）

### 3.1 R002

创建 `.sessions/2026-08-08-ch4-reference-method-extension/R002-reference-source-expansion.md`，结构必须为：

1. 恢复验证与防偏三问；
2. 检索 receipt：query、requested/actual source、raw/dedup、缓存路径；
3. 候选来源与为何只保留 2–4 个；
4. E1–E8 总表；
5. 逐候选 FACT / INFERENCE / UNKNOWN；
6. 唯一入口及其 0.5–1 天 smoke contract，或 bounded-source 无入口；
7. exact collision / prior-art claim ceiling；
8. object/package 计数（入口筛选不计数）；
9. 下一合法动作与禁止动作。

### 3.2 D/V/H 与 current views

- `decisions.md` 追加 **D004**：记录唯一入口或 bounded-source 无入口 terminal；不得改写 D003。
- `verifications.md` 追加 **V003**：独立 verifier 必须给 PASS/FAIL/PARTIAL 与 P0/P1/P2。
- 创建 **H003**：交接下一对话；有入口时只交接“重读 groundwork 并从 GW Step 1 启动该 defect-reproduction 研究对象”，明确 smoke 需等 Step 1–3 通过后进入 Step 4a；无入口时交回 source/object 范围决定。
- 在 S001 追加 T002 回传记录；更新 topic-index 与 `_registry.yaml` current view。
- 历史 R001/D002/V002/H002 保留，不删除、不回写结果。

### 3.3 最终回复只给五项

1. terminal 与当前 object/package 失败计数；
2. 2–4 个候选及 E1–E8 结果；
3. 唯一 defect-reproduction 入口与 smoke 合同，或无入口的具体缺口；
4. 是否形成方法、是否运行实现/仿真/GW；
5. R002/D004/V003/H003 路径、verifier、commit SHA。

---

## 4. 已知陷阱

- 不要把 T001 的两个 entry-screening FAIL 计成两个对象包失败。
- 不要要求目标 FSO defect 在 smoke 前已经成立；入口的职责是证明“值得且能低成本证伪”。
- 不要把 fiber/wireless source defect 直接宣称为 FSO fact；必须写迁移机制和 UNKNOWN。
- 不要因 generic/adjacent prior art 直接 Kill；只查 exact object/action collision，并收窄 future claim。
- 不要复活 K01：Paillier/FG-DRC 已是 exact collision，不因新 gate 放宽而改变。
- 不要从 “有代码 / 有论文 / 有 headroom” 直接跳到方法；本轮最多得到 GW Step 1 入口。
- 不要无限检索补 winner：4 query / 4 candidates 是硬上限。
- 不要让治理文件成为主要工作量；科学产出必须是候选证据和可执行 smoke contract。

---

## 5. 验收

- [ ] D001–D003、R001/H002 与 registry 已恢复，D002 supersession 语义正确；
- [ ] 使用本地索引优先，定向 query ≤4，requested/actual source 和 raw/dedup 有 receipt；
- [ ] 候选 2–4 个且机制不同，推荐 ≤1；
- [ ] 每个候选 E1–E8 齐全，FACT/INFERENCE/UNKNOWN 分开；
- [ ] 外部 defect、FSO 迁移机制、0.5–1 天 smoke 合同三者齐全才可晋级；
- [ ] exact collision 与邻域 prior art 已分开处理，K01 等 exact object 未复活；
- [ ] entry screening 不计 package/object failure；
- [ ] 未实现、未仿真、未进入 GW/Contract/Execute；
- [ ] R002/D004/V003/H003 与 current views 已同步；
- [ ] fresh-context verifier 完成，P0/P1/P2 明确；
- [ ] 一次统一 commit、未 push，四个 p05 日志未修改未暂存。

---

## 附：产出回传位置

- 主产出：`.sessions/2026-08-08-ch4-reference-method-extension/R002-reference-source-expansion.md`
- 决策：同专题 `decisions.md` 的 D004
- 验证：同专题 `verifications.md` 的 V003
- 交接：同专题 `H003-reference-source-expansion-result.md`
