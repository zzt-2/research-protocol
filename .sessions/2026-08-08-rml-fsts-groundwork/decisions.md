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

## D009: 授权并冻结 Q1 Groundwork Step 4a 连续执行合同

> status: active
> date: 2026-08-09
> 取代：无；延续 D008 的 provisional-survivor 边界
> 被取代：无
> 依据：用户原话: `voice.md` 2026-08-09 + D008/V005/H005 + `stages/gw-feasibility.md`
> 触发原话: `voice.md` 2026-08-09

### 决策

将专题范围只扩展到 Groundwork Step 4a feasibility，并连续执行到唯一合法 Step 4a terminal。顺序冻结为：A0 §0–§6与 testbed readiness → semantic smoke → 只有门控全过时才执行 bounded MVE → fresh-context 独立验证 → owner/治理同步。不得在 A0 后停为计划稿。

### 理由

D008/V005 已证明 Q1 具备带全文限制的 Step 4a 入口，但 target lag/`B_L` ranking crossover、conditioned lookup 吸收能力与 receiver-visible action 增量仍全部 UNKNOWN。用户已显式批准触及旧“明确不含”的 Step 4a/smoke/条件式 MVE，并冻结了最强廉价 comparator、MDE、paired CI 与 stop rules，满足 scope-change 的显式授权条件。

### 冻结合同

- Q1 身份：`M=Wang/Enhanced fixed-lag/fixed-B_L FSTS`；`C=PM-4/16QAM、320-symbol FSTS、receiver-power/SNR、弱/强湍流等有依据的条件变化`；`A=固定 lag/B_L 的最优值或排序可能随 receiver-visible condition 改变并产生 CFO-MSE/outage regret`。
- baseline ladder：`B0` 论文 fixed lag/`B_L`；`B1` dev 全局调优 fixed-lag；`B2` dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup；`O1` truth/oracle lag 仅作 headroom/Kill；`C1` 仅在 B2 后稳定残差、可观测、可行动时构造。
- defect-smoke 门：B2 后仍有 `>=20%` normalized CFO-MSE regret，或 `>=10 percentage-point` outage regret；残差须跨多个条件和 seeds 稳定，且不能由 baseline 未调谐、搜索不公平或单异常场景解释。
- hard exits：无 ranking crossover → 立即 Kill，不构造 controller；B2 吸收 → conventional conditioned lookup resolved；残差不稳定/不可观测/不可行动 → Kill；只有全部门控成立才进入 fresh-disjoint-seed paired bounded MVE。
- MVE：receiver-visible-only decide path；raw rows→aggregate；机制消融；合法传统 comparator；预冻结 MDE/paired CI；caller→callee 信息边界与 hidden-truth runtime metamorphic test。
- claim ceiling：SSRN 6293357 保持高风险全文债但不是 blanket blocker；不得声称首次、novelty closure；consistency PASS 不等于 scientific correctness。

### 唯一终态集

1. `STEP4A_KILL_NO_RANKING_CROSSOVER`
2. `STEP4A_RESOLVED_BY_CONDITIONED_LOOKUP`
3. `STEP4A_KILL_NO_STABLE_OBSERVABLE_ACTIONABLE_RESIDUAL`
4. `STEP4A_GO_BOUNDED_RECEIVER_VISIBLE_CONTROLLER_SIGNAL`
5. `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`

其中 1/3 为 Q1 Kill，2 为 Resolved，4 为 Go；5 仅限真实 shared-testbed/证据完整性硬 blocker，不能用来回避可修复的本地问题。`METHOD_SIGNAL` 与贡献层级必须依据 fresh held-out MVE 和独立 verifier 另判，不由 oracle headroom 或 semantic smoke 自动推出。

### 排除的替代方案

- 只比较 B0/B1：遗漏最强廉价 B2，会把普通查表包装成方法。
- 先造 C1 再找信号：违反 ranking-crossover/B2-residual 前置门。
- 用 truth SNR、true `h`、TX payload 或目标标签驱动动作：违反 deployable 信息边界。
- 无 smoke 直接搭正式 testbed、扩搜索量或进入 Contract/Execute：超出本轮和框架阶段。

### 影响范围

允许新增本专题 Step 4a preflight/contract、隔离的 experiment/test/artifact/worker-log 与 D/V/H；允许同步 `literature_notes_rml_fsts.md`、`master-state.md` 和 registry。继续禁止修改 `common/`、`params.py`、dormant campaign、正式论文正文、四个 `p05_run*.log` 与 push。

### 来源

S004；用户 2026-08-09 明确授权。

## D010: 冻结 Step 4a semantic-smoke 的 receiver-lag adapter 与统计合同

> status: rejected
> date: 2026-08-09
> 取代：无；落实 D009 的 bounded-adapter 要求
> 被取代：D011（仅取代待重构执行路线；本条 status 保持 rejected，作为 pre-run 失败合同证据）
> 依据：T011 公式/身份审计 + T012 testbed readiness + T013 A0 独立审计
> 触发原话：无（公式身份、可部署性与公平配对的技术推导）

### 决策

semantic smoke 固定每种 modulation 的发端 320-symbol FSTS：PM-4QAM 用论文 `(B_N,B_L^tx)=(16,20)`，PM-16QAM 用 `(8,40)`。动作不是事后改写发端 `B_L^tx`，而是在同一接收 FSTS 上选择 receiver-side fine-correlation lag `L_rx in {10,20,40,80}`；非默认 lag 使用 receiver-known FSTS 做 cross-polarization phase de-rotation。`L_rx=B_L^tx` 时去旋因子必须恒为 1，且输出必须逐项等价于 Wang Eq. (8)–(11)。因此 B0 保持论文身份，B1/B2/O1 是同一估计器的合法 single-lag receiver adapter；非默认 lag 不冒充论文原测点或 Enhanced 2024 精确公式。

### 理由

T011 证明 Wang 的 `B_L` 同时决定发端 block structure、`B_N=320/B_L`、fine divisor 与无模糊范围；直接为每个 action 重造 FSTS 会改变接收样值和协议配置，无法满足“同一 realization、receiver-visible-only decide path”的本轮合同。已知训练符号在接收机合法可得；用其只消除 off-default lag 的已知调制相位，既保持同一 320-symbol waveform、overhead、coarse stage 和样值 hash，又在论文默认点严格退化为原式。该 adapter 是最强廉价 comparator 的工程实现，不构成新方法声称。

### 冻结执行合同

- stage boundary：ideal frame start；输入为 source chain 中 MRC 与 polarization demultiplexing 后的双偏振 FSTS；不声称完整 FS/MRC/星地链路复现。
- waveform/physics：10 GBaud、1 sps、Tx/LO linewidth 各 50 kHz；CFO uniform `(-1.1,+1.1) GHz`；320-symbol PM-4/16QAM FSTS。weak/strong 用有文献溯源的 Gamma-Gamma `(alpha,beta)=(11.6,10.1)/(4.2,1.4)`，单 FSTS 内按 `tau_c >> 32 ns` 准静态；不把它冒充 Wang `C_n^2` 的一一映射。
- power axis：只称 dimensionless average electrical SNR，冻结 `10/20 dB` 诊断端点；不声称 dBm receiver optical power。该范围标 `UNVERIFIED_DIAGNOSTIC_RANGE`，不能单独承载星地 Go。
- split/pairing：每个 `2 modulation x 2 SNR x 2 turbulence` cell 为 `8 dev + 16 disjoint test` seeds；同一 cell/seed 的 FSTS、GG、CFO、phase-noise、AWGN 只生成一次，所有 lag 消费同一 immutable receiver samples。只有 sign/CI 边界按预注册规则允许一次扩为 `16 dev + 32 test`，不得同时调参。
- ladder：B0 按 modulation 用 `20/40`；B1 每个 modulation 在 dev 上冻结一个全局 lag；B2 用 `(modulation,320,dev-frozen measured-power bin)`，每 modulation 的两个 bin 由 dev power-proxy median 冻结，未覆盖走 B1；O1 主口径为 hidden-cell expected-best lag，per-realization hindsight 只作更松诊断上界；C1 门前不存在。
- metric：`q=((f_hat-f_true)/R_s)^2`；normalized CFO-MSE 为完整 population 的 `mean(q)`。evaluation-only onset outage 用 PM-4QAM `q>2.5e-7`、PM-16QAM `q>6.25e-8`；另报 severe outage `6.25e-6/2.25e-6` 与 fine-range false lock，不把这些改名成论文原生 outage。
- selection：B1/B2/O1 以 `(onset_outage_rate, NMSE, smaller_lag)` lexicographic 冻结；所有对象同 grid、同 dev budget、同 estimator、同 samples。
- regret gate：MSE regret 主口径为 `(MSE_B2-MSE_O1)/max(MSE_O1,epsilon_floor)`，其中 `epsilon_floor=max(1e-18,100 x noiseless_identity_NMSE)`；同时报告 bounded reducible fraction、absolute paired delta 与 95% CI。outage regret 为 `outage_B2-outage_O1` percentage points。
- terminal reducer：先 validity，再全条件 ranking crossover，再 B2 residual/stability，再 observability/actionability；无 crossover立即 D009 terminal 1，B2 吸收为 terminal 2，不稳定/不可观测/不可行动为 terminal 3，只有全过才派 fresh-seed bounded MVE。

### 排除的替代方案

- 每个 lag 重造不同发端 FSTS 后仍声称相同 receiver realization：改变了处理任务与样值，paired 语义不成立。
- 直接把旧 `frame_sync_fsts.py` 或 `fft_foe(...)/B_L` 当 Wang estimator：T011/T012 已证 `B_L/B_N` 为 no-op 且无 Eq. (7)–(11)。
- 把 `gamma_bar`、true `h`、true turbulence label或 action outcome直接作为 B2 key：属于 hidden-truth leakage。
- 用 Enhanced 缺失公式补 Wang adapter：本地 Enhanced Eq. (1)–(21) 不可恢复，只保留竞争边界与 power/length dependence。

### 影响范围

只允许新增隔离的 `projects/simulation/explore/rml-fsts-step4a/`、聚焦测试、artifact、worker-log 与本专题治理/owner；不修改 `common/`、`params.py`、旧 B3、正式论文或保护日志。

### 来源

`projects/thesis-fso/worker-logs/step-4a-rml-fsts-formula-identity.md`；`step-4a-rml-fsts-testbed-readiness.md`；`step-4a-rml-fsts-a0-independent.md`。

### 2026-08-09 pre-run 独立审查结论

fresh critic 在任何 RED/grid 前判 `BLOCKED, P0/P1/P2=2/5/2`。P0-1：固定发端 waveform 后扫描 `L_rx`，off-default 已改变原 Q1 的联合 `(B_N,B_L)` 方法对象，不能据 adapter 的 crossover/no-crossover 发原 Q1 terminal。P0-2：明确标为未验证的 `10/20 dB` 与 Gu scalar-GG transfer 没有 source calibration/B0 qualitative anchor，不能承载原 Q1 scientific terminal。故 D010 路线按分层试错 F1 立即 rejected；没有运行科学 grid、没有结果驱动调参。下一合同必须保留 structural `B_L`、改用 shared exogenous latent pairing，并先闭合 source condition/calibration。

## D011: Step 4a terminal 5——testbed validity/calibration 硬阻断

> status: active
> date: 2026-08-09
> 取代：D010 的待重构执行路线；D010 保持 rejected 历史证据
> 被取代：无
> 依据：验证: V006/V007 + 审计: T015–T019 worker logs + 决策: D009 terminal 5
> 触发原话: 无（技术推导；用户的 Step 4a terminal/stop 约束已登记于 `voice.md` 2026-08-09，本轮按 T018 不修改 voice）

### 决策

将当前唯一 Step 4a terminal 冻结为 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`。fresh-context V007 已独立重放并判 `PASS, P0/P1/P2=0/0/0`；Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`。

### 理由

performance grid 的 validity/calibration 起飞门在任何科学 raw row 之前被三类 hard blocker 阻断：

1. **structural action-before causality**：联合 `(B_N,B_L)` 已写入当前发端 FSTS；当前 FSTS 的 receiver-power estimate 在动作之后才可得。common probe 或 previous-frame feedback 会改变 protocol、overhead/state lifecycle，超出原 Q1。
2. **source channel non-equivalence**：Gu scalar Gamma-Gamma 只保留归一化 irradiance marginal，不等价于 Wang phase-screen、0.2 m aperture、SMF coupling、phase/branch joint statistics。
3. **dBm→离散噪声不可辨识**：Wang 未给 noise-equivalent bandwidth、BPD/TIA/thermal/background/ADC 与功率参考面，无法唯一得到 post-ADC complex-noise variance。

由此，B0 numeric calibration gate 也不可执行：当前材料不能同时冻结 source point、source equation 和 numeric tolerance。B0/B1/B2/O1/C1 的 performance 数字全部为 `N/A (NOT_RUN)`；没有 scientific raw rows、paired delta/CI、semantic-smoke performance grid 或 bounded MVE。

### 可恢复缺口与 hard blocker 的区别

Wang Fig. 8/10/11/12 direct figure 因 IEEE 403 未取得，坐标/ticks/逐点曲线属于可恢复缺口；恢复 PDF/原图可补图轴和部分 numeric target，却不能自动解决上述 causality、channel equivalence 与 noise-identifiability hard blockers。因此不得把“缺图可恢复”写成“testbed 可恢复后即可跑”。

### 排除的替代方案

- 不恢复或运行 T014 performance grid，不以 synthetic `10/20 dB` 或 Gu GG 诊断发 Q1 Kill/Resolved/Go。
- 不运行 structural diagnostic；即便未来另跑，也必须标 `DIAGNOSTIC_ONLY / TERMINAL_DISABLED`，无原 Q1 terminal authority。
- 不构造 C1、不进入 bounded MVE、Contract、Execute 或论文写作。
- 不增加 object/package failure 计数；当前仍为 `0/0`。

### 影响范围

同步 S004、topic-index、`literature_notes_rml_fsts.md`、`master-state.md`、rejected `contract.json`、terminal receipt、worker logs、V007、registry 与 H006。专题转 `dormant`；不修改 voice 或四个 `p05_run*.log`。

### 重开条件

下一合法科学动作只可在显式 scope-change 后发生：取得 authors/source receiver+channel configuration（至少闭合 phase-screen/SMF 与 `P_rx[dBm] -> E[|w[k]|^2]`），并定义 action-before protocol、feedback/state lifecycle 与 overhead。否则保持该 Inconclusive 边界，不进入下游。

### 来源

S004 / T015–T019 / V006–V007。
