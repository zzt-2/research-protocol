# Decisions — RML-FSTS Groundwork

## D001: 冻结独立 Groundwork 专题范围与证据语义

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：调研: 上游 R002 + 决策: 上游 D004 + handoff: 上游 H003 + 任务合同: T003
> 触发原话: 无（技术推导）

### 决策

在独立专题 `2026-08-08-rml-fsts-groundwork` 中仅执行 Groundwork Step 1–2，并在 Step 2 覆盖面报告后停止等待用户确认。

### 理由

上游只把 RML-FSTS 选为 defect-reproduction Groundwork 入口，未证明目标星地 defect、未形成 Q# 或方法；正式 Step 1–2 是建立文献池和全文覆盖的最小合法动作。

### 排除的替代方案

- 不从上游 entry screening 直接运行 smoke、实现、仿真或进入 Step 3/3.5/4a。
- 不把 source-domain fixed-lag condition-dependence 偷换成目标 FSO lag-ranking crossover 已成立。
- 不削弱未来 comparator：保留 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。
- 不并行 BUM-CMA，不补新 research object，不复活 exact historical object。

### 影响范围

创建本专题 topic-index/S/R/D/V/H、RML-FSTS literature owner、Step 1/2 receipts 与 coverage report；同步 thesis-fso master-state；上游控制专题转 dormant current-view owner。科学代码、仿真参数、正式论文、旧 dormant topic 与 protected history不变。

### 来源

S001 / T003 / 上游 D004、R002、H003。

## D002: Step 1 PASS 与 Step 2 覆盖终态

> status: active
> date: 2026-08-08
> 取代：无
> 被取代：无
> 依据：R001 + R002 + Step 1 search receipt + Step 2 acquisition receipt + coverage report
> 触发原话: 无（技术推导）

### 决策

冻结 Step 1 terminal=`STEP1_PASS`，Step 2 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`。当前在覆盖面用户确认关口硬停止；Step 3 保持 `NOT_STARTED`。

### 理由

Step 1 的 7/7 query、121 unique、4 actual sources、58.68% 正式发表比例和路线门均通过；Step 2 有 5 篇合格 CORE，C1–C4 四类齐全。READY 仅是获取覆盖门，不是 target defect、Q#、方法或 novelty 判断。

### 排除的替代方案

- 不因 5 篇失败全文关闭 research object，也不把下载缺口计作 object/package failure。
- 不把 metadata/abstract 或 C3 无线场景结论外推为 coherent-FSO target fact。
- 不自动进入 Step 3/3.5/4a，不运行 smoke、实现或仿真。

### 影响范围

更新新专题 current view、RML-FSTS literature owner 与 thesis-fso master-state；上游专题只保留 current-view 交接。object/package failure 仍为 `0/0`。

### 来源

S001 / R001 / R002 / coverage report / T003。

## D003: 用户确认覆盖面后仅授权 Groundwork Step 3

> status: active
> date: 2026-08-09
> 取代：无（执行 D002 用户确认关口通过后的合法分支；不改写 Step 1/2 历史事实）
> 被取代：无
> 依据：调研: R002 + 决策: D002 + 用户确认: 2026-08-09 对当前 5 篇 CORE 覆盖面回复“行”（零信息应答，按 voice 规范不收录）
> 触发原话: 无（用户以零信息“行”确认覆盖面与进入 Step 3，按 voice 规范不收录）

### 决策

将本专题当前范围从正式 Groundwork Step 1–2 扩大到 **仅执行 Step 3**：以当前 5 篇合格 CORE 为冻结输入完成全文精读；到 Step 3 完成或阻塞状态停止，不进入 Step 3.5。

### 理由

D002 要求的 Step 2 用户覆盖面确认已经满足。当前五篇全文达到 Step 3 的最低数量门并覆盖 C1–C4；用户接受其已披露的谱系偏斜与缺失竞品债务，因此下一合法动作是按 `stages/gw-read.md` 完成事实提取和 canonical 问题清单，而不是补跑 smoke 或提前做 novelty/可行性裁决。

### 排除的替代方案

- 不把用户确认解释为 target lag-ranking crossover、conditioned single-lag failure、novelty、Q#、Go 或方法已成立。
- 不在同一任务进入 Step 3.5、Step 4a、smoke、future action 设计/实现、仿真、MVE、Contract 或 Execute。
- 不用 `problem_truth/actionability/novelty/thesis_fit` 取代 glossary canonical 四判据。
- 不从缺失论文的标题/摘要推导公式、失效机制或实现细节；Tang/WiSEE provenance 修复前不计 CORE。
- 不在无 canonical Q# 全过时自造 Step 3 terminal；保持 `BLOCKED/IN_PROGRESS` 并返回框架规定的搜索恢复路径。

### 影响范围

新建 S002/T001；更新本专题 topic-index、registry、`projects/thesis-fso/master-state.md` 与 `literature_notes_rml_fsts.md` 到 `STEP3_DISPATCH_READY`。不修改论文正文、科学代码、仿真参数、旧专题或四个 `p05_run*.log`。

### 来源

S002；用户在 Step 2 覆盖面确认关口的回复；R002/D002/coverage report。

## D004: Groundwork Step 3 completed 并在边界停止

> status: active
> date: 2026-08-09
> 取代：无
> 被取代：无
> 依据：调研: R003 + 验证: V002 + 全文证据: 五篇 fresh reader logs + receipt
> 触发原话: 无（技术推导；本轮用户消息为纯操作指令，按 voice 规范不收录）

### 决策

Groundwork Step 3 标为 `✅ completed`：五篇冻结 CORE 全文完成，canonical target-relevant Q# 共 1 条且四判据 4/4；本轮在 Step 3 边界停止。

### 理由

5/5 source preflight、标准字段、7 子表、通信参数、实验完备性、三篇写作架构和 owner/read-note/read-log/receipt 均闭合。Q1 的 M/C/A、方法产出形态、近期 baseline 与量化对标同时满足 glossary canonical 四判据；A 保持可证伪的 target inference，不要求 Step 3 已用 MVE 证明。

### 排除的替代方案

- 不增加 `problem_truth/novelty/actionability/thesis_fit` 语义门。
- 不把 Q1 通过写成 target defect、novelty、Go、METHOD_SIGNAL 或方法成立。
- 不以 Morelli/Yu/Paillier 证明 coherent-FSO target defect。
- 不进入 Step 3.5/4a，不运行 smoke、实现、仿真、MVE、Contract 或 Execute。

### 影响范围

更新 R003、literature owner、五篇全局 read-note、read-log、receipt、topic-index、registry、master-state、V002 与 H002。Step 3.5 保持 `NOT_STARTED`；object/package failure 保持 `0/0`。

### 来源

S002 / R003 / V002 / T001。

## D005: 修正 Q1 的 A 逻辑方向与近期 baseline 身份措辞

> status: active
> date: 2026-08-09
> 取代：无（amends D004 的 Q1 A 与判据 3 措辞；不取代 Step 3 completed）
> 被取代：无
> 依据：critic 审查: `/root/q1_semantic_critic` + 官方定义: `stages/glossary.md` 研究问题定义 + 全文证据: L01/L02/L04 cited lines
> 触发原话: 无（技术审查）

### 决策

保留 D004 的 Step 3=`✅ completed` 与 Q1 四判据 4/4，但把 Q1 的 A 明确为 **M 所依赖、可能在 C 下被违反的近似最优假设**。判据 3 分账为：Wang 2023 承担 exact recent M；Enhanced 2024（Optics Express）承担 2019+ task-matched 顶刊 comparator。项目既有 venue authority 已把 Optics Express 列为允许保留的光通信顶刊，因此不依赖 Wang venue 等级也能闭合项目参数。

### 理由

旧写法“ranking 保持稳定，因此 conditioned single-lag 足够”按字面是在说问题不存在，未显式连回“fixed-`B_L` 因该假设被违反而不足”。一手证据支持 `B_L` 的精度—范围折中及其 modulation/power/TS-length 依赖，但 target crossover、fixed 设计实际失效和 headroom 仍是 INFERENCE/UNKNOWN。该缺陷是任务示例与执行表述的语义歧义，不需要重读全文或运行实验。

### 排除的替代方案

- 不把 Step 3 退回 Step 2：五篇全文、结构化提取与 Q1 实质研究对象均保留。
- 不提前宣布 target defect、cheap comparator 失败、novelty 或 Go。
- 不因 Wang venue 标签证据不足而否定其作为 2023 exact M 的近期身份。

### 影响范围

修正 R003、literature owner、current view 与 handoff；V003 取代 V002 的 Q1 科学语义验收部分。判据 3 的项目级 venue 依据为 `.sessions/2026-06-20-problem-driven-redirection/decisions.md:983` 与 `.sessions/2026-06-04-advisor-review-revision/topic-index.md:94`。Step 3.5 仍未授权，object/package failure 保持 `0/0`。

### 来源

主控接收 T001 后的独立 scientific critic；R003/D004/V002。

## D006: 仅将当前范围扩展到 mandatory Groundwork Step 3.5

> status: active
> date: 2026-08-09
> 取代：无
> 被取代：无
> 依据：用户原话: `voice.md` 2026-08-09 + 框架: `stages/gw-supplement.md` + 验证: V003/H003

### 决策

在 D005/V003/H003 已验收 Step 3 的前提下，将当前范围只扩展到 mandatory Step 3.5 竞争闭包、独立验证与一次统一提交；在 Step 3.5 canonical terminal 处停止，不进入 Step 4a。

### 理由

用户已显式授权触及原“明确不含”的 Step 3.5，且 `stages/gw-supplement.md` 将其定义为 Step 3 精读后的必做步骤。Q1 当前只形成合法问题候选，Cheng 2020、两篇 Optica 直接竞品、Wang/Enhanced 引用链、Tang/WiSEE provenance 以及 conditioned single-lag cheap alternative 的竞争边界尚未闭合。

### 排除的替代方案

- 不把本次 scope change 扩大到 Step 4a、smoke、仿真、MVE、算法设计或实现。
- 不把 Q1=4/4 当作 novelty、Go、METHOD_SIGNAL 或方法成立。
- 不以“没有搜到”宣称首次或新颖；若关键一手全文不可得，允许终止为证据阻塞。
- 不省略 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup，也不复活历史已排除方向。

### 影响范围

允许更新本专题 R/S/D/V/H、`literature_notes_rml_fsts.md`、检索/引用链 receipt、必要 read-notes、topic-index、master-state 与 registry；禁止修改 `common/`、`params.py`、正式论文正文、dormant campaign 和四个既有 `p05_run*.log`，禁止 push。

### 来源

S003 / 用户 2026-08-09 明确授权。

## D007: Step 3.5 终止为证据阻塞且不开放 Step 4a

> status: superseded
> date: 2026-08-09
> 取代：无
> 被取代：D008
> 依据：调研: R004 + 检索/引用链 receipts: `search-archive/2026-08-09/rml-fsts-step3-5-*.json` + 全文证据: T004/T006 worker-logs + 独立验证: V004
> 触发原话: 无（技术推导；用户的终态约束已记录于 `voice.md` 2026-08-09）

### 决策

mandatory Step 3.5 的 canonical terminal 记为 **证据阻塞**：qualified fulltext 中未确认 exact-action collision 或 conditioned single-lag lookup 等价，但关键一手全文不可得且检索已达三轮上限，不能诚实闭合竞争边界；Step 4a 不开放。

### 理由

R1 完成 8-query matrix、三类真实来源与 Wang/Enhanced 双向引用链，新增 must/should=`3/3`；R2 新术语检索的三个完成 query 未新增 must/should，但第 4 query 超时；R3 源限定重试仍超时并达到轮次上限。新增/旧债务共 8 项缺 qualified fulltext，包含 Cheng、short-block、low-power joint FS/FOE 与 STFT 直接动作候选。缺全文不能被解释成无碰撞。

### 排除的替代方案

- 不把“qualified evidence 中 exact collision=0”写成首次、新颖或 Q1 存活闭包。
- 不把摘要级 architecture-adjacent 证据升级为全文排除。
- 不因 R3 超时而开启 R4 或无限漫灌；按框架三轮上限停止。
- 不把 conditioned single-lag cheap alternative 遗漏或包装成 adaptive method。
- 不进入 Step 4a、smoke、仿真、MVE、设计或实现。

### 影响范围

Step 3.5 状态改为 `EVIDENCE_BLOCKED`；Q1 仍为 Step 3 合法问题候选，但没有 Step 4a 入口。未来只有在获得关键一手全文并完成 action-level read/receipt 后，才可重开 Step 3.5 terminal 裁决。object/package failure 保持 `0/0`。

### 来源

S003 / R004 / T002-T010 / V004。

## D008: 撤回 blanket evidence block，Q1 作为带全文限制的 provisional survivor

> status: active
> date: 2026-08-09
> 取代：D007 的 terminal、8 项等强 blocker 分类与 Step 4a NO ENTRY；保留其检索/引用链/止损事实
> 被取代：无
> 依据：主控 scientific critic `/root/step35_science_critic` + blocker audit `/root/step35_blocker_feasibility` + `stages/gw-supplement.md` + 共享 canonical 130981 全文
> 触发原话: 无（主控技术验收）

### 决策

Step 3.5 修订为 `STEP3_5_COMPLETE_Q1_PROVISIONAL_SURVIVOR_WITH_FULLTEXT_LIMITATIONS`。Q1 获得后续 Step 4a 讨论入口，但本轮不授权 Step 4a、smoke、仿真、MVE、设计或实现。

### 理由

`gw-supplement.md` 在三轮仍未收敛时要求记录未覆盖方向并由用户决定是否继续，不要求所有标题相邻论文全文齐备，也未规定缺任一全文就禁止 Step 4a。R2 三个完成 query 新 must/should=`0/0`，Q4/R3 timeout 只能形成 coverage caveat。

D007 的 8 项等强 blocker 分类还包含一项确定性 stale false negative：Optics Communications 130981 全文与 read-note 早已存在于共享 canonical。正文证明其为固定 short-time-spectrum coarse FOE，received power 与 FFT points 不驱动运行时 lag/`B_L`/window 选择。其余缺件中，仅 SSRN 6293357 保持高风险 action-level UNKNOWN；ACP/IPOC 是次级 comparator 债，其他条目属于任务/条件邻接、动作不同或已有 generic prior-art 约束。

### Claim ceiling 与下游合同

- 不得宣称首次、exact novelty 已闭合、target fixed-lag failure 已证明或 METHOD_SIGNAL。
- Step 4a 必须比较 Wang fixed-`B_L`、dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup，以及任何拟议 receiver-visible controller。
- SSRN/ACP/Cheng/OE 缺件作为竞争边界债持续保留；获得全文后可回填或推翻 provisional survivor。
- object/package failure 保持 `0/0`。

### 来源

R004 主控接收审查；V005；共享 `papers/doi/10.1016_j.optcom.2024.130981/content.md:47,71-87,127-141`。
