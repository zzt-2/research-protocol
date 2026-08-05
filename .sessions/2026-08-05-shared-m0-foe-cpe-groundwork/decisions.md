# Decisions — Shared M0-Power FOE–CPE Groundwork

> 本专题决策记录。D### 按编号排列，旧决策标 superseded 不删。

## D001: 冻结研究对象与范围边界（GW Step 1–2 入口）

> status: active
> date: 2026-08-05
> 取代：无
> 扩展：承接 RDL system 专题 D024 / CP005 / T008（P1 计算图工程候选恢复与实际工具链吸收门）
> 被取代：无
> 依据：T008 任务书 §2（冻结研究对象）+ D024（P1 survivor 恢复）+ caller-path 证据复核

### 决策

本专题作为 P1 "Shared Raised-Power Compute Graph for NDA FOE+CPE" 的正式 Groundwork owner，
本轮只执行 GW Step 1 检索 + Step 2 全文获取/覆盖面门。冻结研究对象（M/C/A）见 topic-index
不变量段，仅用于检索与获取，不作为 Step 3/4a 结论。

确认关键已知事实（caller-path 已复核，证据指针见下）：

- `[FACT]` 升幂 `rx**M0` 在 NDA 路内被计算两次：FOE 在
  `projects/simulation/simulator/sc_nda_ml_sim.py:150`（`raised = rx ** M0_power`，FFT 找频峰）；
  CPE 在 `projects/simulation/common/_recovery.py:213`（`assume_df_zero` 分支 `raised = rx ** M0`，
  mean-angle）与 `:243`（FFT-df 分支 `raised = rx ** M0`）。
- `[FACT]` 两次跨独立 Python 函数调用（CPython/NumPy），无 JIT/graph optimizer/CSE 证据。
- `[FACT]` route-A caller `run_ccisp_family1_selector_a_30seed.py:24-31` 在 `per_block_nda_receiver_output`
  串行调 `fft_foe_m0_omega` → `nda_ml_recovery(assume_df_zero=True)`。
- `[FACT]` route-B caller `_a4_branchrouted_30seed.py:138-148` `per_block_nda` 同串行双调用。
- `[FACT]` 升幂域 CFO 去除可用 `raised * exp(-j*M0*omega*k)`，原信号域补 `omega*k + phi`。

未知项（必须由 Step 1–2 关闭或标 blocker，见 topic-index 未决项）。

### 理由

D024 已确认 P1 在实际 CPython/NumPy caller 中存在真实重复升幂，假想 compiler/CSE 不构成
廉价替代，恢复为 `THESIS_ENGINEERING_COMPONENT` 设计候选。但 survivor 不是 METHOD_SIGNAL，
必须回正式 GW Step 1–3/3.5/4a。本轮（T008）只推进 Step 1–2，停在用户覆盖面确认门。

### 排除的替代方案

- 不把 P1 升级为 METHOD_SIGNAL / active carrier / 论文结论；
- 不在 Step 1–2 阶段用 oracle/headroom 决定 Go；
- 不修改 NDA-ML 估计器统计（触发 `NDA_ML_BODY_REOPEN`）；
- 不跳过覆盖面用户确认门自动进 Step 3。

### 影响范围

新建本专题；新建项目 owner
`projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`（GW 进度 + Step 1–2 状态）与
`projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。不触动既有科学
verdict、common/params、Skill 与正式论文。

### 来源

T008 任务书；RDL system 专题 D024/CP005/S015。触发原话：无（技术推导；派生自 D024，用户仅
确认执行 T008）。

---

## D002: 显式授权仅执行 GW Step 3 精读

> status: active
> date: 2026-08-05
> 取代：无
> 扩展：D001 的执行边界（不改其冻结 M/C/A 与工程组件层级）
> 被取代：无
> 依据：验证: V002 + 用户原话: voice.md 2026-08-05

### 决策

在 `STEP2_ACCEPTED_READY_FOR_STEP3` 基础上，仅将本专题当前执行范围扩展到 GW Step 3：完成至少
6 篇 HIGH/MEDIUM 全文精读、直接竞品 collision、合法 comparator/action delta、Q# 四判据和独立
fresh-context verifier；终止于 Step 3 terminal。

### 理由

H001 要求 Step 3 必须由用户在新对话显式授权；用户已给出该授权，并明确保持 Step 3.5、Step 4a、
Contract、实现和仿真为禁区。V002 已独立验收 Step 2 的 12 篇全文与 receipt，满足 Step 3 入口门。

### 排除的替代方案

- 不停留在旧 Step 1–2 范围，因为用户已显式授权下一合法步骤；
- 不顺带进入 Step 3.5/4a/Contract，也不实现或仿真，因为这些均未获授权；
- 不用“当前检索未发现”代替 novelty 证据或直接给 Go/Kill。

### 影响范围

更新 topic-index 当前范围；续接 S001；写项目 literature notes、`papers/_read_notes/`、本专题 read-log、
研究/验证/交接记录。禁改 Skill/common/params，四个 `p05_run*.log` 不触碰。

### 来源

用户 2026-08-05 显式授权；H001 接收验证；V002。

---

## D003: generic shared-compute action 碰撞，Step 3 无合法 Q#

> status: superseded（terminal 部分由 D004 取代；collision/action-delta 科学裁决继续有效）
> date: 2026-08-05
> 取代：无
> 扩展：D001 的 P1 工程组件候选边界
> 被取代：D004（仅取代本决策第 3 条的自造 terminal；第 1/2/4 条继续有效）
> 依据：研究: R001；V003 后续审查为 FAIL

### 决策

1. 把“FOE/FE 与 CPE/PR 共享一次 m-th-power/correlation 中间量”裁定为 existing-action collision，
   不再作为 P1 的独立 action delta。
2. 仅保留窄候选：当前串行 NDA QAM 链中 raised-domain CFO removal 与跨级 lifetime/matched-output
   合同；其 exact novelty、工程价值和是否 trivial 均未闭合。
3. Q-P1-01 因 canonical 判据 3（2019+ task-matched recent baseline）失败，不形成合法 Q#；Step 3
   terminal 固定为 `STEP3_PARTIAL_NO_Q_CANDIDATE`。**此 terminal 后被 V003 证伪并由 D004 取代。**
4. P1 贡献层级仍最多为 `THESIS_ENGINEERING_COMPONENT`，本轮不给 Go/Kill 或论文 claim。

### 理由

JLT 2018 正文不仅给出 shared correlation graph，还明确记载 OFC 2016 已共享 differential m-th-power
FE 与 Viterbi PR 的 m-th power；这直接覆盖 generic 动作。CSNDSP 2014 则是不同输入/不同阶数的
joint algorithm，不是 shared sequence。近年论文提供硬件 refactor 与 cheap alternative，却没有
形成“2019+ baseline 在当前 C 下因重复 raised-domain 计算而失败”的证据链。

### 排除的替代方案

- 不以“当前九篇未发现 exact 公式”声称 novelty；论文池和一手 OFC 2016 证据均不完备。
- 不把 CSNDSP 2014 误报为 same-sequence shared compute。
- 不把窄 delta 直接判为 trivial/Go/Kill；这些属于后续证据或 Step 4a，而本轮没有授权。
- 不用 estimator-changing DA/ML 方法冒充 same-estimator conventional refactor。

### 影响范围

更新 literature notes、read notes、topic index、S001 与 verifier 记录；不改代码、仿真或论文 claim。

### 来源

`R001-step3-direct-competitor-synthesis.md`；JLT 2018 `content.md` L63–89、L237；CSNDSP 2014
`content.md` L47–55、L113–117、L151–161、L181–195。触发原话：见 `voice.md` 2026-08-05；D003
的 collision/terminal 为技术裁决，无新增用户态度原话。

---

## D004: 撤销自造 terminal，Step 3 保持阻塞

> status: superseded
> date: 2026-08-05
> 取代：D003 第 3 条的 terminal；不取代 D003 的 collision/action-delta 科学裁决
> 被取代：D005
> 依据：验证: V003 FAIL + `stages/gw-read.md` L198 + `stages/glossary.md` L65–70

### 决策

撤销 `STEP3_PARTIAL_NO_Q_CANDIDATE`。在没有 canonical 四判据全过 Q# 时，本专题保持 **GW Step 3
BLOCKED/IN PROGRESS**，不得宣称 Step 3 完成或离开 Step 3。框架规定的下一恢复路径是回
`gw-search.md` 扩检索，再 Step 2 获取、Step 3 精读；本轮没有该新增授权，因此只记录，不执行。

### 理由

V003 独立复核确认该 terminal 在框架文件中定义数为 0；`gw-read.md` 明确无 Q# 时禁止离开 Step 3，
`glossary.md` 指定回检索扩展。初版结构也未满足七子表/VVUQ 强制门，不能称“内容门完成”。

### 排除的替代方案

- 不以 Step 3.5 绕过 Q# 空集处置；
- 不保留自造 terminal；
- 不因 generic action collision 直接给 P1 Kill，scientific collision 与 stage completion 分开记录。

### 影响范围

修正 literature notes、topic-index、S001、registry、master-state；重写九份 read note；V004 复核前
不写 H002、不宣称 Step 3 完成。

### 来源

V003；`stages/gw-read.md` L198；`stages/glossary.md` L65–70。触发原话：无（框架合规纠错）。

---

## D005: bounded evidence closure 终止 P1

> status: active
> date: 2026-08-05
> 取代：D004 的 blocked-waiting 状态；不取代 D003/R001 的 generic collision 历史
> 被取代：无
> 依据：调研: R002 + 验证: V005 + 用户原话: voice.md 2026-08-05

### 决策

最后一次 bounded `gw-search→gw-acquire→gw-read` 用尽 6/6 query 后仍无 2019+ 合格 task-matched
baseline，触发 terminal=`RECENT_BASELINE_UNAVAILABLE`。Q-P1-01 判据 3 继续 FAIL，P1 降为
`SUPPORTING_ONLY`，本专题关闭；不得改名重开、进入 Step 3.5/4a、实现或仿真。

### 核心失败机制

P1 的宽泛 shared m-th-power/correlation 动作已由 OFC 2016（二手全文陈述）/JLT 2018 碰撞；窄
raised-domain lifetime 要形成合法 Q，还需 2019+、同输入序列、同估计器、同
FOE→CFO-removal→CPE 任务的 baseline。冻结预算内严格复筛为 0：三篇 recent 有效全文分别是
estimator-changing 或 CPE-only，不能从其公式/框图建立 P1 的重复 raised-domain 动作。

### 否决了什么

- 否决以 generic CSE、不同输入序列、不同估计器或 estimator-changing 方法冒充 task-matched M；
- 否决因作者未显式写“failure A”就忽略数据流证据，也否决在数据流不匹配时强行推断 failure A；
- 否决用 OFC 摘要、PTL 元数据或 JLT 2018 二手陈述冒充 OFC 一手 exact boundary；
- 否决继续扩检索、把 P1 改名后重开、或用 Step 3.5/4a/实现/仿真绕过 canonical Q 空集。

### 可复用部分

保留 generic action collision、matched-output protocol、复杂度/PPA 指标、三篇 near-miss 的数据流
排除证据，以及 OFC exact action=`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE` 的证据边界，作为后续
候选的防碰撞材料；不保留 P1 active carrier 身份。

### 具体数据

- query 预算 6/6；各组 final=19/30/14/5/1/13；严格 task-matched recent baseline=0；
- OFC 官方摘要 HTTP 200，但 PDF 端点返回 15,088 B Radware HTML；PTL download/arXiv/blit 均失败；
- Q-P1-01：1/2/4 PASS、3 FAIL；formal terminal=`RECENT_BASELINE_UNAVAILABLE`；
- P1：`SUPPORTING_ONLY`，`mission_method_delta=NONE`。

### 影响范围

更新 R002、项目 literature notes、topic-index、registry、S001、verification 与 closed-state handoff。
不修改 RDL 上游 formal/current owner，不产生实验、代码或论文 claim。

### 来源

S001 2026-08-05 bounded closure 续接；R002。触发原话见 `voice.md` 2026-08-05。

**P1 的 generic action 已碰撞，窄 delta 未形成合法 Q；停止该方向，下一轮轮换新候选，不再改名重开。**
