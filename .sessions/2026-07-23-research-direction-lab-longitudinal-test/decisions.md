# Decisions — Research Direction Lab 长程真实运行测试

## D001: Phase 2 首包续接合法 B1 carrier，不跳转 C15

> status: superseded
> date: 2026-07-26
> 取代：无
> 扩展：formal D013 / system D018 / mission CP007
> 被取代：D002
> 依据：`projects/thesis-fso/master-state.md` 当前控制面与 FR-22 + T007 phase-1 critic
> 触发原话：无（技术纠偏；用户只要求交付下一提示词）

### 决策

Phase 2 第一包为 B1 adaptive phase-window 的 **identity-repaired method-production
package**。C15 虽有现成代码，但未完成当前 formal owner 要求的新候选 Step 1–3；
直接运行会违反 FR-22。它保留为后续 candidate，不以“portfolio 可运行”冒充
“formal 已授权”。

B1 已有 Step 1–3 与 formal D013，且 T007 的当前 oracle 诊断仍显示约 0.4–1.0 dB
局部空间；其 Kill 未被主控接收。T008 只关闭五个已知身份缺口，若合法空间仍在，
同一包必须完成三个 receiver-visible 方法及 fresh-seed paired comparison。

### 正向方法合同

- `positive_method_target`：receiver-visible、低复杂度 adaptive phase-window CPE。
- `minimal_construct`：physics-ratio rule、validation lookup+hysteresis、
  confidence-safe selector。
- `fair_comparator`：validation-frozen global fixed window；per-condition fixed 作强对照。
- `primary_packaging`：面向 GG block-SNR 与 Wiener phase-noise 联合变化的自适应窗。
- `fallback_packaging`：合法 fixed-window 选择与 receiver-observability 工作区边界。
- `next_positive_action`：执行 T008；identity 修复后同包跑方法，不再单独派纯修复包。

### 已知五个缺口

1. B* 疑似按 seed/test truth 重选，而非 validation 全局冻结；
2. required-SNR 使用硬编码 log-BER slope，而非真实 SNR 曲线；
3. oracle/B* 候选集合与选择身份未完全闭合；
4. observability 缺 held-out exact-window accuracy 与 majority-fixed 对照；
5. 仅凭当前特征 `|rho|<0.5` 把 0.4–1.0 dB diagnostic headroom 提前 Kill。

### 边界

- 只在 GW Step 4a；不进 Step 5/Contract/Execute。
- executor 不更新 formal/current/master/mission owner。
- 任一 identity 无法闭合则 `BLOCKED_IDENTITY`，不作科学裁决。
- headroom 存在但方法不胜则 `METHOD_FAIL_WITH_SPACE`，不 Kill 整个 family。
- 不修 Pilot-Jones、B10/B12、C15 或 dormant science-scout。

---

## D002: 拒收 T008 Kill，停止 B1 修复并转 Goal 级 campaign remap

> status: superseded
> date: 2026-07-26
> 取代：D001（仅取代当前 carrier 与下一动作；D001 对 T008 的历史授权仍有效）
> 被取代：D003
> 依据：验证 V002 + mission CP008 + T008 task/runner/raw artifact 独立重算
> 触发原话：`voice.md` 2026-07-26（用户准备在新 GPT 对话用 Goal 模式持续推进）

### 决策

1. T008 的 17 项工程测试通过，五类修复尝试与数据资产保留；但正式
   `KILL_NO_ADAPTIVE_WINDOW_SPACE` **不接收**，formal disposition 为
   `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`。
2. 不再给 B1 开 T009 修复包。连续两个 B1 包、全 mission 八包均未产生方法增量，
   已满足“正式进展但 method delta 持续为 NONE”的 mission stalled 条件。
3. 前台动作切换为 `GOAL_MODE_CAMPAIGN_REMAP`：新主控先恢复 CP001–CP008，
   比较仍合法的 carrier、方法包装潜力和最小补债成本；只有完成显式 remap 后才可
   准备下一科学 T。

### 理由

- 冻结任务规定：无真实 FEC crossing 时只能报 raw/log-BER 与
  `UNRESOLVED_NO_CROSSING`，不得用 proxy dB 触发 `<0.5 dB` Kill。T008 runner
  却用非 FEC 区 B* slope 生成 `dB-equiv` 并据此 Kill。
- gate 实际比较 B-cond 与 B*，没有按任务计算 per-block oracle；其 per-block
  代码还跳过 `N>BLOCK=100`，而实际 `B*=256`，故“oracle 候选包含 B*”声明为假。
- 去 pilot 标签重算后，20 dB 的 QPSK BER 仍约 0.174–0.178，16QAM 约
  0.272–0.280。逐窗 VV 的 π/2 分支跳变只做全局 resolve，基线本身不在可靠
  working region；两个坏基线近似不能证明自适应空间消失。
- results/raw/fresh-test 位于 gitignored `results/`，未进入提交，证据闭包也不完整。

### 排除的替代方案

- 不接收 scoped/family Kill：主 metric、oracle identity 和 evaluator working
  region 同时失效。
- 不再修 B1：这会成为同轴第三包，并继续把方法生产 mission 运行成 evaluator
  修复链。
- 不立即运行 C15 或任意新实验：formal Step 1–3 与 campaign remap 尚未完成，
  直接开跑会再次违反 FR-22。

### 影响范围

- live control 升至 epoch 13，checkpoint 为 CP008；禁止 T009/B1 repair。
- formal master 将 B1 标为 `BLOCKED_IDENTITY / RETURNED_TO_POOL`。
- 下一对话通过 H002 恢复，并显式建立“方法产出优先”的 Goal；本对话不创建 Goal。

### 来源

T008 worker 回执、V002 独立审查、用户 2026-07-26 Goal 模式安排。

---

## D003: Campaign remap 激活 A4 deployable adaptive CPR

> status: superseded
> date: 2026-07-26
> 取代：D002（只取代“无 active carrier / 仅 remap”的当前动作；T008 拒收事实保留）
> 被取代：D005
> 依据：R001 + formal D015 + CP001–CP008 + A4 bugfix/common-768/写作资产
> 触发原话：`voice.md` 2026-07-26（长期 Goal 的 carrier 比较、方法优先与独立验收要求）

### 决策

1. campaign remap 完成。首轮比较 A4、B10/B12、B1 三条具有 formal 证据链的
   carrier，并逐项证明 B2/B3/B7/C15/B9/Pilot-Jones/P03/Scout 当前不满足
   formal readiness。
2. 当前 carrier 激活为 `A4_DEPLOYABLE_ADAPTIVE_CPR`，状态
   `READY_WITH_BOUNDED_IDENTITY_ADJUDICATION`；仍在 GW Step 4a。
3. 下一包 T009 不是纯 audit：一次有界 identity preflight 通过后，必须同包冻结并
   比较 P1 frozen two-stage rule、P2 monotone selector、P3 confidence-safe
   selector。
4. T009 只在统一 transmitter waveform、common data mask、deployable input、
   causal ambiguity resolve 与包含 S011 DPLL 的 validation-frozen strongest
   conventional comparator 下接受科学结论。
5. 若只胜 fixed NDA 却被 always-DA、DPLL 或 global B* 支配，最高
   `PACKAGING_BOUNDARY`；测试 PASS、negative result 或 evaluator repair 均不算
   method delta。
6. T009 失败不结束 Goal，也不追加第二个 A4 repair 包。主控接收后更新 CP009
   的 method delta、same-axis/repair/no-method streak 与 drift，再自动比较
   B10 source-native 最小重建和新候选 Step 1–3。

### 为什么优于两个替代项

- **相对 B10/B12**：A4 已有可运行方法动作、两个不同输出分支、30-seed 数据和
  论文方法结构；B10/B12 的核心 estimator source identity 尚未成立，先要重建
  方法本体。
- **相对 B1**：A4 是本轮第一次 formal adjudication；B1 已连续 T007/T008 两包且
  evaluator 不在可靠 working region，再继续将成为第三个同轴 repair 包。

### 正向方法合同

- `positive_method_target`：receiver-visible、块级 DA/NDA adaptive CPR。
- `minimal_construct`：P1 frozen two-stage rule；P2 monotone validation selector；
  P3 confidence-safe selector。
- `fair_comparator`：fixed DA、fixed NDA、validation-frozen DPLL；
  global B*/B-cond 均从三者选定；per-block oracle 只作 ceiling。
- `primary_packaging`：Gamma–Gamma 湍流下的接收功率感知自适应 CPR。
- `fallback_packaging`：NDA safeguard、工作区边界或 complexity/robustness trade-off。
- `next_positive_action`：执行 T009；identity 过门后同包完成 fresh paired method
  comparison。

### 边界

- 不修改旧 A4、论文正文、common、params 或任何 owner；
- 不恢复 B1/T008、T006 repair、Pilot-Jones、P03 或 dormant Scout；
- 不进入 Step 5、Contract 或 Execute；
- mission checkpoint 仍为 CP008，只有主控接收 T009 后才能追加 CP009。

---

## D004: 本对话主控端到端执行，取消用户中转 GLM

> status: superseded
> date: 2026-07-26
> 取代：无（只修改运行与协作模式，不取代 D003/formal D015 的科学选择）
> 被取代：D026
> 依据：用户原话: voice.md 2026-07-26
> 触发原话：`voice.md` 2026-07-26

### 决策

1. 长期科学目标、A4 carrier、formal D015、CP008 与 T009 科学合同均不变。
2. 撤销“用户另开 GLM 对话并中转 T 路径/四行回执”的运行方式；本 Codex 对话
   继续担任长期主控，并端到端推进实现、实验、验收、owner/mission 更新和轮换。
3. 为遵守项目的执行/审查分离与 MVE 强制委托规则，主控可在同一线程内部调用
   executor/verifier 子 agent；这些不是用户需要管理的外部对话。
4. control 升至 epoch 15，T009 同步重绑定；用户无需阅读日志或判断科学正确性。

### 理由

用户明确表示不想继续分出 GLM 对话，希望本对话自行完成全部工作。保留内部
executor/verifier 分离既满足这一协作偏好，也不牺牲科学审查独立性。

### 排除的替代方案

- 不继续要求用户中转：该模式已被用户显式撤销。
- 不由主控单上下文自审自验：违反项目 MVE 委托和独立 verifier 规则。
- 不改变 A4 科学合同或改派 carrier：本次纠正只涉及执行模式，没有新的科学证据。

### 影响范围

- live control/T009 从 epoch 14 升至 epoch 15；
- topic 当前范围与不变量改为“主控端到端 + 内部执行/审查分离”；
- formal D015、master scientific carrier 与 mission checkpoint 保持不变；
- T009 完成后仍由主控追加 CP009，并继续长期 Goal。

### 来源

S001 续接；用户 2026-07-26 运行模式纠正。

---

## D005: 接受 T009 身份阻断，A4 返回候选池并重开 campaign remap

> status: superseded
> date: 2026-07-26
> 取代：D003（只取代 A4 active carrier 与下一动作；D003 的 T009 历史任务合同、身份门和“不再二修”约束保留）
> 被取代：D006
> 依据：验证 V006 + formal D016/V003 + T009 worker-log + executor commit `8ea886e4b5c1e3318fd9426dcc7e8aebcdf8a558`
> 触发原话：无（技术推导）

### 决策

1. 接受 T009 的 formal disposition：
   `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`；mission 的
   `mission_method_delta=NONE`。P1–P3 primary 未运行，没有方法信号、包装边界或
   promotion 结论。
2. 拒绝把“DA 在 9/9 validation conditions 获胜”解释成可靠工作区中的物理支配。
   该观察来自未闭合 pilot/TX-truth、DA/NDA 频率处理不对称、无来源工作区和未提交
   raw/result 的 evaluator，不能用于论文 claim、family Kill 或 carrier 排名。
3. A4 返回候选池，不作 family Kill，也不为当前 evaluator 开第二个 repair package。
   前台恢复 `GOAL_MODE_CAMPAIGN_REMAP`，formal 当前无 active carrier。
4. remap 先比较 B10 source-native 最小重建与新的 formal-ready candidates；比较完成并
   更新 formal owner 前，只允许恢复、portfolio mapping 和任务准备，不运行科学实验。

### 核心失败机制

- `generate_shared_realization_apsk` 生成全 256 符号随机 payload，runner 又直接把
  `shared["tx"][PILOT_IDX]` 交给 deployable arm；没有独立冻结且接收端可重建的 pilot
  manifest，common-payload/pilot 身份未闭合。
- shared channel 保留 `F_RESIDUAL=1 MHz`，DA 用 64 个所谓 pilot 回归频率，NDA 却
  以 `assume_df_zero=True` 运行；该不对称足以制造 DA/NDA 排序。
- contract 的 16/24/36 dB 条件无来源且越过 formal 湍流网格上限 26 dB；所有 arm
  的最佳聚合 BER 仍为 `0.005056 > 3.8e-3`，没有合法 FEC crossing，高 SNR 曲线还
  非单调，不能称为可靠工作区。
- `raw.json`、`result.json` 被 `results*/` 规则忽略且 metadata 仍指向执行前
  `220e477`；commit `8ea886e` 无法复现 headline。该 commit 另有 8 个 EOF
  whitespace errors。

### 否决了什么

- 否决“DA 9/9 因而物理上支配 NDA”、A4 family Kill 和任何 dB/论文结论。
- 否决把 5 项工程测试、DPLL smoke、negative result 或治理闭包记为方法增量。
- 否决在当前 A4 evaluator 上继续修；这既违反 D003 的 no-second-repair 契约，也比
  remap 到 B10 source-native 或新候选更不可能产生 `METHOD_SIGNAL`。

### 可复用部分

- T009 的 task-control、连续 VCO DPLL smoke、隔离实现、540 行本地 raw 和四类身份
  失败机制可作为 evaluator 防错资产。
- commit `8ea886e4…` 与 ignored raw/result 保留为带证据闭包限制的审计指针；不得
  作为正式性能证据。

### 影响范围

- live control 升至 epoch 16、checkpoint 升至 CP009，lane 改为
  `GOAL_MODE_CAMPAIGN_REMAP`，authority 指向 formal D016。
- D004 的“本对话主控端到端执行”协作模式保持 active；只更换科学 carrier 与下一
  动作。
- 仍停留在 GW Step 4a；不进入 Step 5、Contract 或 Execute。

### 来源

V006；formal D016/V003；T009 worker-log、raw/result 与 executor commit
`8ea886e4…`。

---

## D006: 激活 B10 source-native adaptive pilot-RLS carrier

> status: superseded
> date: 2026-07-26
> 取代：D005（只取代“无 active carrier / 仅 remap”的当前动作；T009 拒收、A4 回池与 no-second-repair 事实保留）
> 被取代：D007
> 依据：调研 R002 + formal D017 + B10 Springer 2024 全文/metadata + formal D012/V001 + 两条摘要级邻近方法先例（R002 §2.1）
> 触发原话：无（技术推导）

### 决策

1. post-T009 remap 选择 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR` 作为当前
   active carrier，仍处于 GW Step 4a 维度 D。
2. formal readiness 为 `FORMAL_READY_WITH_SOURCE_NATIVE_IDENTITY_GATE`：
   B10 L20/Q1/Q2 Step 1–3、formal D012 与可获取全文均存在；T006 verdict 已被
   V001 拒收、family 未 Kill，但 T006 estimator 不具 source identity，禁止复用为 P1。
3. T010 必须先闭合前 128 连续 pilot→DD 生命周期、TX 侧同通道 pilot 注入、
   receiver-reconstructable manifest、RLS 递推/初始化/单位与 positive-CFO source
   smoke；identity 过门后同包完成 P1–P3 和 cheap-rule/conventional comparison。
   `source-native` 只指 B10 estimator；2.5 GBd 星地 GG primary 必须引用
   `B5Params.R_SYM_B5` 并标 `SOURCE_TRANSFER`，不得把 B10 的 26 dB OSNR
   当 electrical SNR。
4. 不把 source smoke、测试 PASS、construct 创建或 evaluator 修复记为
   `METHOD_SIGNAL`。正信号必须来自 held-out paired test，同时胜
   source-native fixed B10、幅度门控 cheap rule 与 conventional B*；所有 required
   comparator 必须在共同真实 HD-FEC crossing/`BER<0.2` working region 内。
   no-crossing/collapse 只能支持 outage/boundary，不能触发 Q² Go。
5. T010 失败后不开第二个 B10 implementation repair，也不恢复 B12 组合、B1/T008
   或 A4/T009；优先转 C15 Step 1–3 formalization。

### 正向方法合同

- `positive_method_target`：在星地 GG 深衰落/低 SNR 使 DD residual 不可靠时，
  以 receiver-visible innovation 抑制错误 RLS 更新，并有界调整 forgetting factor。
- `minimal_construct`：P1 source-native fixed-`λ` B10；P2 innovation freeze；
  P3 lagged/EMA innovation variable forgetting。
- `fair_comparator`：P1、receiver-amplitude-only cheap gate，以及在同一 waveform、
  data mask、coarse-frequency responsibility 和 validation budget下冻结的
  4OPM+BPS / 4OPM+DD-DPLL；truth-assisted arm 仅作 bound。
- `primary_packaging`：面向星地高阶 QAM 深衰落决策错误的创新量门控
  adaptive pilot-RLS CPR。
- `fallback_packaging`：固定 B10 的 source-native 星地迁移边界、update-freeze
  低复杂度鲁棒规则或工作区/复杂度 trade-off。
- `next_positive_action`：独立审查 T010 后，由线程内 executor 执行；identity
  过门后不得停在纯 smoke。

### 为什么优于替代项

- 相对 C15：B10 已有 formal Step 1–3 和全文；C15 尚需完整 Step 1–3，当前不能跑。
- 相对 B1：B10 是新方法轴；B1 再继续是第三个 evaluator repair。
- 相对 B9：B10 只需隔离 source-native estimator/generator；B9 需新建自相干、
  oversampling、quantization 和检测链。

### 影响范围

- live control 升至 epoch 17，authority 指向 formal D017，mission checkpoint
  保持 CP009；
- 只授权 T010 的 `METHOD_CONSTRUCT`；不进入 Step 5/Contract/Execute，不改
  common/params/paper/owner，不运行 C15/B1/A4/B9；
- D004 的本 Goal 主控端到端 + 内部 executor/verifier 分离保持 active。

### 来源

R002；formal D017；B10 shared-paper metadata/content；formal D012/V001；
DOI `10.1109/ICAIT66450.2025.11353303` 与
`10.1016/J.CJA.2015.05.001` 的本地检索元数据（只作邻近先例）。

---

## D007: 驳回 T010 初次身份 verdict，并授权一次包内 Phase-B 合同纠错确认

> status: superseded
> date: 2026-07-26
> 取代：D006（只取代 T010 Phase-B 的 operational residual、source-smoke `λ` 与确认 seed 合同；B10 carrier、P1–P3 方法目标和 no-second-package 边界保留）
> 被取代：D008
> 依据：验证 V008 + T010 初次 `source-smoke.json` + B10 PDF p.165–170 Eq.(1)/(8) 与 Fig.1 + 独立科学 verifier 的不落盘反事实
> 触发原话：无（技术推导）

### 决策

1. T010 初次 `BLOCKED_IDENTITY` 不接收。其 1/10 GHz BER 为
   `0.250432213 / 0.418593197`，但独立 verifier 证明 verdict 同时受两个
   P0 污染：
   - 正相位 `r=s·exp(+jφ)+n`、`exp(-j predicted)` 去旋约定下，任务把论文
     Eq.(8) 的文字符号直接落成了相反的 operational residual；
   - source smoke 使用无来源硬编码 `λ=.999`，而论文要求优化 `λ`，且 verifier
     证明该值会制造 10 GHz failure。
   因此 formal disposition 仅为
   `SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID`，
   `mission_method_delta=NONE`；不能宣称 B10 身份失败或 family Kill。
2. CP009 尚未更新、T010 尚未最终提交或接受，本次不是第二个 B10 package。
   只授权同一 T010、同一 Phase B 的一次 bounded contract correction：
   - operational residual 固定为
     `angle(derotated_received * conj(hard_decision))`，desired phase 为
     `predicted_phase + residual`；
   - `λ=.99` 标为
     `IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN`，只用于 source identity
     confirmation，不是论文 source parameter、primary tuning 或方法信号；
   - seed `130001` 降为 invalid-development evidence；全新 confirm seed
     `130002` 在代码和任务审查通过前保持未观察；
   - 原 artifact 保留为 `source-smoke-invalid-v1.json`；新确认结果写
     `source-smoke.json`，不得覆盖失败来源链。
3. 修订后必须新增 residual-direction 与 1/10 GHz BER regression；先由独立 verifier
   审查 epoch 18 / formal D018 / T010 amendment，PASS 后才可只重跑 Phase B。
4. confirm 任一 gate 失败即接受 `BLOCKED_IDENTITY` 并轮换；confirm 通过才可由
   另一独立科学 verifier 授权 Phase C。不得再改 residual、`λ`、seed 或开第二个
   B10 repair/package。

### 理由

直接接受当前 `BLOCKED_IDENTITY` 会把任务合同的符号错误和任意参数造成的假失败
归因给 B10；直接进入 Phase C 又会绕过 source identity gate。一次包内、全新 seed
的确认既保留失败可追溯性，又以最小增量判断 source-native estimator 是否成立。

### 排除的替代方案

- 不接受当前 `BLOCKED_IDENTITY`：verdict 被两个 P0 污染。
- 不把 seed `130001` 的反事实当 confirm：该 seed 已被 verifier 用于开发诊断。
- 不做 `λ` grid/test 同池调参：会把 post-hoc tuning 冒充确认。
- 不立即转 C15：B10 仍是 formal-ready carrier，且一个全新 confirm seed 可以
  低成本关闭任务自身造成的 identity debt；若该确认失败再轮换。
- 不进入 Phase C：当前 source identity 尚未获得独立接受。

### 影响范围

- live control 升至 epoch 18，authority 指向 formal D018，checkpoint 保持 CP009；
- 只允许更新 T010、其隔离实现/tests/artifacts 与 owner current projections；
- 不改 common/params、旧包、论文或 protected history，不运行 primary/validation/
  held-out，不更新 mission-log。

### 来源

S001 续接；V008；T010 Phase-B artifact/report；B10 原 PDF p.165–170。

---

## D008: T010 confirm seed 与 Phase-B 暂停回执修订

> status: superseded
> date: 2026-07-26
> 取代：D007（仅更正 confirm seed 与 Phase-B→科学验收暂停协议；D007 的 operational residual、source-only `.99`、单次包内确认与 no-further-repair 边界全部保留）
> 被取代：D009
> 依据：独立 amendment review（P0=0/P1=3/P2=1）+ repository exact-token seed census + V008
> 触发原话：无（技术推导）

### 决策

1. `130002` 已在 Phase-B canonical/RNG test 中生成 realization，不能再称为
   “代码和任务审查前未观察”。confirm seed 改为仓库 exact-token 搜索零命中的
   `130003`；`130002` 仅保留为非性能 canonical-test seed。
2. T010 必须自包含新增：
   - synthetic residual-direction regression，明确旧符号沿错误方向更新、D007
     operational residual 沿真实相位方向更新；
   - seed `130003` 的 1/10 GHz BER gate；该 gate 的实际执行就是唯一 Phase-B
     confirm，派发前禁止预跑。
3. confirm PASS 后 executor 必须返回
   `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 并停止；只有主控接收独立科学 verifier
   后，新的递增 control 才能授权 Phase C。§8 final receipt 仍只用于整个 T010
   最终收口，不能覆盖中间科学门。
4. 本修订不新增科学 run、不改变 `.99` 或 method target。confirm 失败即轮换；
   confirm 通过也不自动产生 method delta。

### 理由

clean confirm 必须避免已执行 seed，并消除“Phase-B PASS 后可直接继续 Phase C”与
“只有最终 receipt 才验收”的操作冲突。该修订发生在 confirm 前，未消费新科学
数据。

### 排除的替代方案

- 不把 `130002` 辩解为“只看 RNG 所以仍 unseen”；硬合同要求更严格。
- 不在 epoch 18 静默换 seed；seed 属 decision gate，必须递增 owner/control。
- 不让 executor 在 confirm PASS 后自行进入 Phase C。
- 不新增另一组 `λ` 或 confirm seed。

### 影响范围

- live control 升至 epoch 19，authority 指向 formal D019，CP009 保持不变；
- 更新 T010、registry/current projections；confirm 前不改隔离实现或运行实验；
- mission-log 不更新，Phase C 仍禁止。

### 来源

S001 续接；独立 amendment reviewer；V008；现有 Phase-B test line 170。

---

## D009: 接收 T010 source identity，并授权分段 Phase C 方法构造与 validation

> status: superseded
> date: 2026-07-26
> 取代：D008（只取代“Phase C 未授权”的当前动作；D008 的 confirm 历史、operational residual、source-only `.99` 和 no-further-repair 事实保留）
> 被取代：D010
> 依据：验证 V012 + formal D020 + T010 clean-confirm artifact/source contract
> 触发原话：无（技术推导）

### 决策

1. 接收 T010 Phase B 为
   `SOURCE_IDENTITY_PASS / PHASE_B_CONFIRM_ACCEPTED`。1/10 GHz clean confirm
   均 `0/99488`，CFO relative errors 为
   `9.952903443384171e-5 / 4.499364865190506e-4`；独立 verifier 为
   `P0=0/P1=0/P2=3`。`mission_method_delta=NONE`，不是性能或方法信号。
2. live control 升至 epoch 20 / CP009，只授权同一 T010 的 Phase C：
   - **C1 implementation**：封死 source-smoke 二次运行入口、补 read-only
     artifact 重算/legacy P2，再实现 P2/P3、amplitude-only cheap rule、
     4OPM+BPS 与 4OPM+DD-DPLL，完成 direct information-increment 与 comparator
     sanity tests；不得消费 validation seeds；
   - C1 必须独立 code/science-contract review PASS；
   - **C2 validation freeze**：只用 `131001–131005` 完成预注册 validation grid，
     冻结 P1/P2/P3/cheap/B* 与每个 GG 档最多 3 个相邻 SNR 点；不得运行 held-out。
     若单 turn 超时，只能按预注册 Cartesian order 增量保存 raw，未完成全矩阵前
     不得选择参数或看 test seeds。
3. C2 完成后必须暂停并独立科学验收；新的递增 control 才能授权 Phase D。
4. Phase-B P2 债务：
   - runner 缺 source-smoke 防二次运行锁，C1 必须补；
   - source artifact 未保存 finite/switch/freeze 原值，不得事后伪造；read gate 只重算
     可重算字段，并标 legacy non-recomputable；
   - 默认 locale 的 T006 GBK 失败是旧包债，不修改旧包；T010 自身默认 locale 必须过。

### 理由

source identity 已由独立科学证据关闭，B10 是当前 formal-ready carrier；相对转 C15
仍少完整 Step 1–3 周期，相对 B1/A4 避免第三/第二 evaluator repair，相对 B9 不需
新接收架构。进入受控 Phase C 比在 identity 层继续停留更可能产生 METHOD_SIGNAL，
同时 C1/C2 分段避免把实现自洽、validation tuning 和 held-out 混在一起。

### 排除的替代方案

- 不把 Phase-B PASS 记为 method delta。
- 不再运行 source smoke，不改 sign/`.99`/seed。
- 不在 C1 消费 validation，不在 C2 消费 test。
- 不直接进入 Phase D，不修改 common/params/旧包。
- 不立即转 C15/B1/B9：B10 identity 已成立，当前方法动作比这些候选更接近可检验
  增量；若 C2 无方法空间或方法不增量，再按 D019 边界轮换。

### 影响范围

- authority 递增到 formal D020；T010 task-control 升到 epoch 20，CP009 不变；
- 只允许 T010 隔离路径/tests/artifacts 与 current projections；
- mission-log 暂不追加 CP010；no-method=9、same-axis/repair/drift 保持到整个
  T010 final receipt。

### 来源

S001 续接；V012；T010 Phase-B artifacts/source contract；formal D020。

---

## D010: 接收 T010 C1 并只授权 C2 validation freeze

> status: superseded
> date: 2026-07-26
> 取代：D009（只取代 C1 当前动作；D009 对 Phase-B identity、C1/C2 分段和
> no-second-package 的科学合同保留）
> 被取代：D011
> 依据：验证 V021 + formal D021 + T010 C1 source/experiment contract 与定向 tests
> 触发原话：无（技术推导）

### 决策

1. 接收 T010 Phase C1 为 `C1_IMPLEMENTATION_CONTRACT_PASS`。P2/P3、amplitude-only
   cheap rule、4OPM+BPS 与 4OPM+continuous-DD-DPLL 已形成可运行但尚未
   validation-frozen 的实现；direct information、no-truth、shared-realization、
   comparator responsibility 与 clean/noiseless tests 已闭合。
2. `mission_method_delta=NONE`。C1 PASS 只证明方法身份与比较接口可进入
   validation，不是 fair comparison、性能信号、方法信号或 CP010。
3. live control 升至 epoch 22 / CP009，只授权同一 T010 的 **C2 validation
   freeze**：
   - 只用 validation seeds `131001–131005`；
   - 严格按 T010 预注册 Cartesian order 逐行运行并保存 tracked raw；
   - 全矩阵完成前不得查看 test seeds、选择参数、选择 P2/P3 主臂或生成性能结论；
   - 全矩阵完成后才分别全局冻结 P1/P2/P3/cheap/B*，并为每个 GG 档选择最多
     3 个相邻 SNR 点；
   - 完成后返回 `PARTIAL_C2_AWAITING_SCIENCE_REVIEW` 并暂停。
4. held-out/Phase D、Step 5/Contract/Execute 仍未授权。C2 独立科学验收和新的
   递增 control 是进入 Phase D 的必要条件。
5. pre-C1 immutable snapshot 缺失保留为 legacy attribution P2；不得补造，也不得
   用它扩大或否定 C2 的科学结论。

### 理由

V021 已把 V019/V020 的全部 P1 关闭；B10 目前拥有合法 source identity、隔离方法
实现和 conventional comparator，C2 是第一个能回答“P2/P3 是否在完整 validation
矩阵中相对 P1、cheap 与 conventional B* 产生可冻结增量”的动作。相比立即转
C15，它无需重做 Step 1–3；相比 B1/A4，它不依赖第三/第二 evaluator repair；
相比继续 C1 微调，C2 直接产生 fair-comparison 所需信息。因此它比这些替代项更
接近 `METHOD_SIGNAL`，但仍不预判结果。

### 排除的替代方案

- 不把 C1 tests/contract PASS 记为方法增量。
- 不在 C2 使用 held-out/test seeds，不按 seed/cell 在 P2/P3 之间 best-of。
- 不重跑 source smoke，不再修改 sign、`.99` 或 Phase-B history。
- 不修 T006/B12、B1/T008、A4/T009，不恢复 Scout/P03。
- 不立即转 C15：当前 B10 已越过 source/C1 门，而 C15 仍需完整 Step 1–3；
  若 C2/后续科学验收没有可冻结方法空间，则按既定 no-second-package 边界转 C15。

### 影响范围

- foreground control 递增到 epoch 22；authority 递增到 formal D021；
- T010 task-control 与 C2 amendment 绑定 epoch 22 / CP009；
- 只允许 T010 隔离 package/tests/tracked validation artifacts 和 worker-log；
- mission-log 仍停在 CP009/no-method=9，直到整个 T010 final receipt。

### 来源

S001 续接；V021；T010 C1 executor report；formal D021。

## D011: 接收 T010 BLOCKED_IDENTITY 并轮换到 C15 formalization

> status: active
> date: 2026-07-26
> 取代：D010（只取代 C2 当前动作；D010/D009 的历史 source/C1 接收、held-out
> lock、no-second-package 与 method-claim 门保留）
> 被取代：无
> 依据：验证 V026 + T010 840-row raw checkpoint + worker-log deterministic diagnosis
> 触发原话：无（技术推导）

### 决策

1. 接收 T010 最终科学身份为 `BLOCKED_IDENTITY`，P0/P1/P2=`0/0/1`，
   `mission_method_delta=NONE`。840-row strict-prefix artifact 与 17-file frozen
   hash 是本包终局证据；不是 fair comparison、negative method、包装边界或方法信号。
2. 核心失败机制为 primary transfer 的 128-pilot phase unwrap 在
   moderate/14 dB/seed `131004` 选择错误 `-2π` branch，使进入 RLS 前的 LS slope
   已从真实正值变为负值；P1/P2/P3 共用该初始化，故失败属于 RLS lifecycle
   identity，不是 candidate DD gate 的局部实现 bug。
3. 立即停止 T010/B10：不补齐剩余 1410 rows，不生成 aggregate，不运行
   test/held-out/Phase D，不跳 cell、不伪造 collapse row、不改 positive-slope gate，
   也不开第二个 B10 repair package。
4. 按 R002 与 formal D021 的预注册轮换边界转
   `C15_REDUCED_CONSTELLATION_FORMALIZATION`。C15 当前不是 active scientific
   carrier；下一包只完成新候选 Step 1–3 formal readiness，独立审查通过前不得
   运行 MVE。

### 理由

继续 B10 必须改变 source identity 或异常 row schema，会污染预注册 setting score，
且违反 no-second-package。C15 虽需完整 Step 1–3，但机制与 B10 不同、旧 C15
unequal-step confound 已给出明确公平性问题，完成 formalization 能直接判断是否存在
可包装的复杂度/性能方法形态。相比 B1，它不需要第三次 evaluator 重建；相比 B9，
它不需要 oversampling/quantization/matched-filter/self-coherent 全链基础设施；
相比 A4/T009，它不重复第二个 identity repair。因此它是当前合法替代项中最可能
解锁后续 `METHOD_SIGNAL` 的下一动作，但本次轮换本身没有 method delta。

### 排除的替代方案

- 不把 45 tests、840 rows、identity diagnostic 或独立 PASS 记为方法产出。
- 不把异常编码成 nonfinite/BER=0.5 等未预注册 row。
- 不修 B10/T010、T006/B12、B1/T008、A4/T009，不恢复 Scout/P03。
- 不直接运行 C15 旧 sandbox 或 MVE；旧 C15 的共同 μ=`0.03` 与约 19× gradient
  scale 差是 confounded history，只作 Step 1–3 的失败证据。
- 不选 B9；其新接收架构成本和归因风险显著高于先 formalize C15。

### 影响范围

- mission 接收 CP010，no-method streak 增至 10，mission 继续
  `DRIFTED/STALLED`；
- formal D022 返回 B10，并只开放 C15 Step 1–3 formalization；
- foreground control 递增至 epoch 24 / CP010，action class 只允许
  recover/map/task preparation，不授权科学实验；
- T010 hashed execution contract/raw 保持不改，详细结论见 package synthesis。

### 来源

S001 续接；V026；T010 worker-log；R002；formal D021。

## D012: 授权 T011 只做 C15 Step 1–2 evidence formalization

> status: superseded
> date: 2026-07-26
> 取代：无（细化 D011 的 C15 Step 1–3 顺序）
> 被取代：D013
> 依据：调研 R002 + formal D022/D023 + 旧 C15 synthesis/contract 的
> equalizer-cost identity 与 unequal-step confound
> 触发原话：无（技术推导）

### 决策

1. 将 C15 的对象纠正为 **PM-16QAM/高阶 QAM blind equalization cost/update
   family**，不是 CPR。R002 旧包装句“高阶 QAM CPR 相位代价”作事实性纠正，
   不能进入 T011 的搜索或包装判断。
2. T011 只授权 Groundwork Step 1 search 与 Step 2 acquire：
   - 结构化检索 reduced-constellation/Sato、CMA/MMA、RDE/radius-directed、
     staged CMA→RDE/MMA 与 coherent-FSO task-fit；
   - 闭合至少五篇可读全文、canonical lineage、传统 comparator 和覆盖面缺口；
   - 完成后必须停在 `AWAITING_COVERAGE_CONFIRMATION`，不进入 Step 3。
3. T011 的 formal disposition 与 mission delta 分开：搜索/下载/覆盖门最多形成
   `FORMALIZATION_STEP1_STEP2_COMPLETE`，`mission_method_delta=NONE`。
4. foreground control 递增为 epoch 25 / CP010，action class
   `CANDIDATE_FORMALIZATION`；独立 dispatch review PASS 前不得执行。

### 理由

旧 C15 Scout 改的是均衡器 Godard cost，R002 的 CPR 表述会把方法形态、传统
comparator 和检索词全部带偏。旧结果又以共同 `mu=0.03` 比较约 19× 初始梯度
scale 差的 cost，不能证明方法族失败。当前最小合法动作不是修旧代码或直接重跑，
而是先用全文恢复 canonical cost 血缘与 task-fit。相对 B1 第三 evaluator repair、
A4 第二 identity repair 和 B9 新全链，这仍是最可能重新形成合法方法载体的路线；
但 Step 1–2 本身不是方法进展。

### 排除的替代方案

- 不运行旧 C15 sandbox、tests、seed 或 MVE。
- 不把 Sato/RCCMA/RDE/MMA 的旧代码注释当 canonical source。
- 不把 abstract、网页或 search metadata 当全文。
- 不越过 `gw-acquire.md` 的 coverage confirmation 硬门进入 Step 3。
- 不修 B10/T010、B1/T008、A4/T009、T006/B12，不恢复 Scout/P03。

### 影响范围

- 新建 T011，绑定 epoch 25 / CP010 / `CANDIDATE_FORMALIZATION`；
- formal owner 以 D023 细化 D022；
- master-state 将 C15 标为 Step 1–2 dispatch prepared，仍非 active carrier；
- mission-log 保持 CP010/no-method=10，直到 T011 被独立接收。

### 来源

S001 续接；R002；formal D022；旧 C15
`synthesis.v1.md` / `batch-contract.v1.yaml`；Groundwork Step 1/2 规范。

## D013: 接收 T011 source-coverage block 并授权一次 T012 恢复包

> status: superseded
> date: 2026-07-27
> 取代：D012
> 被取代：D014
> 依据：验证 V029 + T011 worker log/7 archives + 只读共享索引/论文库复核
> 触发原话：无（技术推导）

### 决策

1. 接收 T011 Step 1 的
   `BLOCKED_SEARCH_COVERAGE / P0=0/P1=0/P2=1 /
   mission_method_delta=NONE`。56 rows/53 unique/49 published 可信，但 actual
   source 只有 OpenAlex；未创建 acquisition pool、未进入 Step 2 的止损正确。
2. 该结果只阻断当次检索管道，不是 C15 negative/Kill。共享主仓索引已由
   Semantic Scholar、SerpAPI Scholar、OpenAlex、Exa 四个真实 source family
   召回直接相关候选；共享论文库已有 5 篇近期相关 content，其中 2 篇立即满足
   metadata/title gate，3 篇可作有界本地闭环。
3. 授权一次 T012，把以下工作合并为同一个可失败包：
   - 从共享索引恢复 candidate-specific ≥3-source view 和 8–12 篇 acquisition pool；
   - 核验/闭合现有近期全文 metadata/title；
   - 对 Sato 1975、Godard 1980、Yang–Werner–Dumont 2002 三篇 canonical 各执行
     一次 exact-title IEEE/blit 获取；
   - 任一 canonical 失败即 `BLOCKED_CANONICAL_FULLTEXT`；全部 3/3 且 recent≥2
     才停在 `AWAITING_COVERAGE_CONFIRMATION`。
4. T012 仍为 `CANDIDATE_FORMALIZATION`，不进入 Step 3 或 MVE，
   `mission_method_delta=NONE`。

### 理由

T011 已证明默认 fresh search 只有单源，但没有证明项目资产或 C15 文献只有单源。
共享索引存在四源直接证据，现有全文也已覆盖 JR-CMA pointing-jitter 和
modulus-rings VAE coherent-FSO 等 task-fit/collision；核心债务集中为三篇
canonical 全文。一次 T012 的可逆成本明显低于 B9 新建 oversampled
self-coherent/quantization 全链，也不重复 B1 第三 evaluator repair 或 A4 第二
identity repair，因此比至少这三个替代项更可能解锁后续方法判断。

这仍不是方法进展：JR-CMA 与 VAE collision 甚至可能在 Step 3 缩窄或推翻原包装。
但先闭合 canonical/source 是判断这种碰撞与合法方法空间的最小动作。

### 排除的替代方案

- 不降低三源门，不把 shared index 的合并来源字符串重复计数。
- 不把 53 篇数量、92.5% published 或本地 5 篇 content 写成 formal readiness。
- 不要求用户配置 API key、手工找论文或判断技术正确性。
- 不修 B1/T008、A4/T009、B10/T010、T006/B12；不建设 B9 全链。
- T012 失败后不再给 C15 第二个 source/canonical repair 包；返回候选池并轮换。

### 影响范围

- mission 追加 CP011/no-method=11，C15 same-axis=1，mission 继续
  `DRIFTED/STALLED`；
- formal D024 接收 T011 并授权 T012；
- foreground control 递增至 epoch 26 / CP011；
- 新建 T012；独立 dispatch review PASS 前不得执行。

### 来源

S001 续接；V029；T011 worker log/archives；共享
`all-papers.jsonl` 与 `papers/` 只读映射。

## D014: T012 因 task-interface contract 终止，C15 返回候选池并重开 remap

> status: superseded
> date: 2026-07-27
> 取代：D013
> 被取代：D015
> 依据：验证 V031/V032/V033 + T012 worker log + 独立 final-binding 审查
> 触发原话：无（技术推导）

### 决策

1. 接收 T012 为
   `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED /
   mission_method_delta=NONE`。两次 executor 均在 Phase A 组合 preflight
   停止，source view、acquisition pool、metadata closure 和 canonical acquire
   都未执行；这不是 C15 positive/negative science verdict。
2. 冻结命令的 final binding 又发现 CIM 查询失败时可能 fail-open。V032/T012
   已预注册“冻结命令缺陷也终止、不得第四次 amendment”，因此不再修补 T012。
3. C15 返回候选池，当前继续无 active scientific carrier。foreground 转
   `POST_T012_CARRIER_REMAP`，只允许 Recover/Portfolio Map/Task Preparation；
   新 carrier 正式激活前禁止实验。
4. 下一路线从未执行的新机制候选与已阻断路线中重新比较；不得借此次治理失败
   Kill C15 family，也不得把 preflight 审查写成方法材料。

### 核心失败机制

T012 没有冻结第一版组合命令，导致两个 executor 先后自拟 receipt 路径、
owner regex 与 process predicate；冻结第三版后，独立终验又发现 CIM
enumeration 没有 fail-closed。三个接口缺口属于 task contract 架构脆弱性，而非
source/canonical 获取或 C15 科学机制失败。

### 排除的替代方案

- 不做第四次 T012 amendment；这是 V032/T012 明示的退出条件，也符合连续修复后
  质疑架构而非继续补丁的纪律。
- 不把 `BLOCKED_PREFLIGHT` 改写为 `BLOCKED_CANONICAL_FULLTEXT`；canonical
  acquisition 从未启动。
- 不返回 B1 第三 evaluator repair、A4 第二 identity repair、B10 第二 identity
  repair；既有 no-second-package 边界继续有效。
- 不运行 B9 或其他候选实验；先完成 post-T012 formal-readiness remap。

### 可复用部分

T012 的三源 identity schema、五篇 existing-fulltext storage contract 与三篇
canonical exact binding 仍可作为未来 C15 formalization 资产；不得将本次失败
归因到这些尚未执行的科学/文献合同。

### 具体数据

- preflight attempt 1：唯一失败为错误 receipt 路径；
- attempt 2：owner old/new regex=`False/True`，broad/restricted process
  count=`79/0`；
- final binding：`P0/P1/P2=0/1/0`，唯一 P1 为 CIM query 未 fail-closed；
- source view/pool 不存在，main paper targets diff=`0`，科学命令执行=`false`。

### 影响范围

- mission 追加 CP012：same-axis=2、repair=1、no-method=12，
  `UNDERWEIGHT / mission DRIFTED/STALLED`；
- formal D025 与 live control epoch 30 接收终止；
- T012 历史保留，不再派发；下一 T 必须来自 remap 且继续禁止实验跳步。

### 来源

S001 续接；V031/V032/V033；T012 worker log；独立 final-binding 审查。

## D015: 选择 B9 evidence-adapter 作为下一 formalization workline

> status: superseded
> date: 2026-07-27
> 取代：D014
> 被取代：D016
> 依据：调研 R003 + formal D025/live V033/CP012 + B9 JLT 2023 主仓全文与旧
> Step-3-like 提取
> 触发原话：无（技术推导）

### 决策

1. post-T012 remap 选择 **B9 virtual-carrier self-coherent + DRE
   evidence-adapter** 作为下一 formalization workline；当前仍为
   `HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE`，不激活 scientific carrier。
2. T013 只授权 Groundwork Step 1：建立 candidate-specific ≥20 篇、≥3 个真实
   source families、≥2 mechanism routes、≥5 必读、正式发表 ≥50% 的文献视图，
   并完成 AI 语义审查、竞争碰撞和 acquisition debt 映射。
3. T013 不下载全文、不进入 Step 2/3/3.5/4a/MVE，不实现 DRE/DC-Value/
   virtual-carrier 链路，不运行仿真或 seed。Step 1 PASS 只允许
   `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE`，
   `mission_method_delta=NONE`。
4. candidate positive method contract 仅作待验证假设：
   - `positive_method_target`：低比特 virtual-carrier self-coherent 星地 FSO 中，
     使用因果可部署或预配置链路状态选择 DRE/CSPR 复杂度—稳健性设置，并保留
     source-native fixed-DRE/RO 安全回退；
   - `minimal_construct`：等待 Step 3/3.5/4a 后冻结，当前未授权；
   - `fair_comparator`：RO without DRE、source-native fixed DRE、以及经全文闭合
     的任务匹配传统 noise-shaping 方法；
   - `primary_packaging`：星地低比特 DAC 自相干 FSO 的数字分辨率增强与稳健适配；
   - `fallback_packaging`：固定 DRE 的星地迁移边界或复杂度/性能折中；
   - `next_positive_action`：T013 Step 1 coverage/collision adjudication。

### 理由

B9 的 JLT 2023 accepted fulltext、DOI/title metadata 与 42 m FSO 实验已落盘；
source-native DRE 相对同架构 RO 对照在 3/4/5 PNOB 报告约 3/1/0.5 dB SNR，
提供了真实正向锚和明确技术旋钮。它仍缺星地 M-C-A、canonical lineage、传统
comparator 与 formal Step 1–3，因此只能先 formalize，不能直接实验。

相对 C15，B9 是未消耗 repair 配额的新机制并已有正向锚；C15 已连续两个同轴包且
T012 科学内容仍未执行。相对 B1，B9 不需要被禁止的第三次 evaluator rebuild；
相对 A4，B9 不需要第二次修复四类 identity P0。一次 Step 1 能直接裁决 B9 是否有
足够证据池、独立机制路线和传统 comparator 支撑，比继续上述至少三个替代项更
可能恢复方法生产。

### 排除的替代方案

- 不把 JLT 内部 DRE-vs-RO 的 dB 增益写成相对传统 coherent CPR 的优势。
- 不把旧 S005/read-note 当当前 formal Step 1–3 完成证据。
- 不建设 B9 oversampled self-coherent 全链，不运行实验。
- 不做第四次 T012 amendment，不返回 B1 第三 evaluator repair、A4 第二
  identity repair或 B10 第二 identity repair。
- Step 1 若不足三源、无星地 task-fit 或竞争已饱和，B9 返回池；不降低门槛。

### 影响范围

- formal authority 转 D026；
- foreground control 递增为 epoch 31 / CP012，active lane 改为
  `B9_STEP1_FORMALIZATION`，允许 `CANDIDATE_FORMALIZATION`；
- 新建 T013；独立 verifier PASS 前不得执行；
- mission-log 暂不追加 CP013，streak 与 delta 保持 CP012，直到 T013 被主控
  独立接收。

### 来源

S001 续接；R003；B9 主仓 metadata/content；旧 S005 与
`_cut-b8b9-self-coherent.md`；Groundwork Step 1 规范。

## D016: 接收 T013 coverage blocker 并授权一次 B9 Step 1 覆盖修复

> status: superseded
> date: 2026-07-27
> 取代：D015
> 被取代：D017
> 依据：调研 R004 + 验证 V035 + T013 worker log/candidate view +
> independent science verifier
> 触发原话：无（技术推导）

### 决策

1. 正式接收 T013 为
   `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。该处置不是 B9
   science Go、Kill、方法信号或 promotion；当前继续
   `NO_ACTIVE_SCIENTIFIC_CARRIER`。
2. T013 的有效事实为：`61` raw → `58` unique，`21` nonexcluded、`8` 必读、
   正式发表 `21/21`；实际 search-run source 只有 OpenAlex，Route A deep
   nonexcluded=`0`，Route B 的两条 deep 只属一般 task-fit/adjacent FSO。
3. 授权一次且仅一次的 T014 B9 Step 1 coverage repair：只用 S2、arXiv、IEEE
   补真实来源与 mechanism-specific deep evidence，不下载、不精读、不实现或实验。
4. T014 后若实际 source families 仍 `<3`，或两条 route 都没有非 OpenAlex 的
   mechanism-specific deep 证据支撑 candidate-specific residual problem，则 B9
   返回候选池，不得再派第三个 B9 Step 1 包；随后必须轮换。
5. 若 T014 Step 1 PASS，也只允许
   `FORMALIZATION_STEP1_COMPLETE_AWAITING_ACQUIRE / method delta NONE`；主控独立
   接收并重新比较替代项后，才能另行授权 Step 2。

### 理由

T013 已经建立可复核候选池、直接 EFNS comparator 和 acquisition debt，失败集中在
真实来源与 deep mechanism coverage，属于一次检索包能直接裁决的有界缺口。所有
候选下一包立即产生 `METHOD_SIGNAL` 的可能性都为 0；按完成最小债务后进入方法比较
的主控判断，B9 修复约 `15%–25%`，最佳替代约 `5%–15%`，这是路线判断而非频率学
概率。

B9 比至少两个替代项更可能最终产生方法信号：相对 C15，它已有正向全文锚、
21 条非排除和真实 EFNS comparator，而 C15 连续两包仍未开始科学内容；相对 B1，
它不需要被禁止的第三次 evaluator rebuild；相对 A4，它不需要第二次四层 identity
重建。一次 T014 的成本小、可逆，且失败条件明确。

### 排除的替代方案

- 不立即重启 C15；T011/T012 已连续两包无方法增量，source/canonical 科学内容仍
  未执行。
- 不返回 B1 第三 evaluator repair、A4 第二 identity repair或 B10 第二 identity
  repair。
- 不因 T013 coverage block 降低 Step 1 门槛、外推星地空白或提前进入 acquire/read。
- 不把多源 PASS、检索量增加或 metadata gap 当方法产出。

### 影响范围

- formal authority 转 D027；
- mission 追加 CP013：same-axis=1、repair=0、no-method=13，
  `ADEQUATE / package ALIGNED`，mission 仍 `DRIFTED/STALLED`；
- control 转 epoch 33 / CP013 /
  `B9_STEP1_BOUNDED_COVERAGE_REPAIR`；
- 新建 T014；独立 dispatch review PASS 前不得执行。

### 来源

S001 续接；R004；V035；T013 worker log 与 ignored candidate view；独立 science
verifier 最终复核。

## D017: 接收 T014 coverage block，B9 返回候选池并强制轮换

> status: superseded
> date: 2026-07-27
> 取代：D016（只取代 B9 当前 workline 与下一动作；D016 对 T014 的历史授权和
> 唯一修复边界保留）
> 被取代：D018
> 依据：验证 V037 + T014 worker log/receipt/raw archives + executor commit
> `5ba5a54cce3705186d8a921d4e4f2ec3c34bb7c8`
> 触发原话：无（技术推导）

### 决策

1. 正式接收 T014 为
   `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。A1 两个
   S2/arXiv archive 各为 0 结果，IEEE Route A 为 1 条、Route B 为 0；连同
   T013 OpenAlex 后实际 source-family union 只有 `[openalex, ieee]`，
   `count=2<3`。
2. T014 按冻结合同正确停止在 A1；A2/A3/A4、两份 deep archive 与 candidate
   view v2 均未产生，未下载、精读、实现或实验。该处置只证明来源覆盖阻断，
   不是 B9 science Kill、空白证据、方法信号或 promotion。
3. B9 立即返回候选池；D016/formal D027 允许的唯一 coverage repair 已消费，
   不得第三个 B9 Step 1 包，也不得降低三源或 mechanism-deep 门槛。
4. 当前继续 `NO_ACTIVE_SCIENTIFIC_CARRIER`。foreground 转
   `POST_B9_CARRIER_REMAP`，只允许 Recover、Portfolio Map、Task Preparation
   与 candidate formalization；完成至少三 carrier 六维比较并更新 formal owner
   前禁止实验。

### 核心失败机制

公开检索能力没有形成足够的 candidate-specific 多源闭包：S2 实际无返回、
arXiv 两条 broad query 均为 0，IEEE 只在 Route A 返回 1 条。该失败属于
Groundwork Step 1 source capability/coverage，不支持对 B9 机制是否成立作正负
科学判断。

### 排除的替代方案

- 不重试第三个 B9 Step 1 包；唯一修复退出条件已经触发。
- 不把配置过 S2/arXiv、历史共享索引来源或零结果计入实际 source family。
- 不把 `BLOCKED_SEARCH_COVERAGE` 改写成“文献空白”或 B9 family Kill。
- 不直接进入 B9 Step 2/3/4a，也不在 remap 前运行 C15/B12/B1/A4 的代码或实验。

### 影响范围

- mission 追加 CP014：same-axis=2、repair=1、no-method=14，
  `ADEQUATE / package ALIGNED`，mission 继续 `DRIFTED/STALLED`；
- formal authority 转 D028；B9 标为
  `RETURNED_TO_POOL / STEP1_SEARCH_COVERAGE_BLOCKED`；
- foreground control 递增到 epoch 35 / CP014 /
  `POST_B9_CARRIER_REMAP`；
- 下一动作必须比较至少三个合法 carrier；不足三个时逐项证明 formal readiness
  不成立。

### 来源

S001 续接；V037；T014 worker log、ignored receipt/raw archives；executor commit
`5ba5a54c`；independent science/package verifier。

## D018: 激活 B12 standalone fade-reliability MAP 方法包

> status: superseded
> date: 2026-07-27
> 取代：D017（只取代“无 active carrier”与 post-B9 remap 下一动作；D017 对
> T014/B9 的处置和第三包禁令保留）
> 被取代：D019
> 依据：调研 R005 + formal D012/D013/D014/D022/D028 + B12 两篇本地全文与
> `literature_notes.md` B12-Q2
> 触发原话：无（技术推导）

### 决策

1. post-B9 remap 激活
   `B12_MAP_FADE_AOPN_STANDALONE`，formal 阶段仍是 GW Step 4a 维度 D。
   该 carrier 是 source-native B12-Q2 standalone，不是 T006 的 B10+B12
   combination repair。
2. 正向方法合同为：按 OECC 2025 Eq.4–7 与 TSP 2022 [5] 的 Σθ/Σε 定义
   重建 source-structured PA/PA-ML/MAP，以接收端可见幅度/innovation 构造
   异方差 AOPN 权重，并加入一个预注册的 observation-precision/
   standardized-residual clip；身份门通过后同包完成因果稳健构造与公平 paired
   comparison。
3. 主对照必须同时包含 source-native PA、PA-ML、exact MAP、obvious cheap
   fixed-variance/hard-skip 和同一 waveform/pilot/data population 上
   validation-frozen 的传统 BPS 或 DD-DPLL。只有同时胜过 exact MAP、
   cheap rule 与传统 B*，且 clean/source-like 退化门、共同 working region、
   seed/metric/statistics 门均闭合，才可记 `METHOD_SIGNAL`。
4. T015 是单包制：source-like 排序不能复现即
   `BLOCKED_IDENTITY`；共同 working region 不存在则只记 boundary；方法不胜
   三类主对照则最多记 `FAIR_COMPARISON_RUN`。OECC 未给 W、pilot sequence、
   sample count/seed 与 penalty 精确定义，这些必须标
   `PROJECT_VALIDATION_ASSUMPTION`；不得宣称 bit-exact 或完整数值复现。任一
   退出条件触发后 B12 回池，
   不开第二个 B12 repair 包。
5. dispatch 前必须由独立 verifier 审查 R005、D018/formal D029、control、
   T015 和 task-control binding。审查 PASS 前禁止 seed/MVE。

### 理由

- B12-Q2 已有 candidate-specific M-C-A/Q#、Step 1–3、OECC 2025 与其
  TSP 2022 [5] 本地全文；Eq.4–7、Σθ 与单正弦 AOPN Σε 可闭合，但数值复现
  仍有显式 project assumptions。T006 只使组合实现
  `UNRESOLVED_IMPLEMENTATION_INVALID`，未 Kill
  standalone family。当前缺口是一个隔离 source-native MAP/256QAM adapter，
  可在同一包的身份门后直接创建和比较方法。
- C15 的下一包仍只能补三源/canonical/Step 2，至少还需独立 Step 3 才能进入
  方法；B1/A4/B10 分别需要被禁止的第三或第二 identity/evaluator repair；
  B9 已消费唯一 Step 1 repair。B12 因而比至少这四类替代项更可能在下一包产生
  `CONSTRUCT_CREATED / FAIR_COMPARISON_RUN / METHOD_SIGNAL`。
- 选择 B12 不预支 Go：exact source ordering、物理参数、传统比较器和稳健增量
  均由可失败的预注册门约束。

### 排除的替代方案

- 不做 C15 的第三个无方法包：C15 保持
  `HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE`，等未来新 source capability
  或更高价值 workline 再议。
- 不返回 B1 第三 evaluator repair、A4 第二 identity repair、B10 第二
  lifecycle repair，也不做第三个 B9 Step 1 包。
- 不复用 T006 的 B12 公式代码，不接回 B10，不做 coarse→MAP cascade、
  CW+MAP 双导频或未经来源闭合的联合 CFO ML。
- 不把 source identity、测试 PASS、negative/boundary 或 metadata repair
  记作方法产出。

### 影响范围

- formal owner 新建 D029 并激活 B12 standalone carrier；
- foreground 升到 epoch 36，checkpoint 仍为 CP014；只有
  `B12_STANDALONE_METHOD_PACKAGE` task preparation/dispatch 被授权；
- 新建 T015；T015 被独立科学接收前不追加 CP015，no-method=14 保持；
- T015 后必须由不同 agent 独立裁决 formal disposition、method delta、三类
  streak、package weight 与 drift，并自动轮换或晋级。

### 来源

S001 续接；R005；formal D012/D013/D014/D022/D028；B12 OECC/TSP 本地全文、
`literature_notes.md` B12-Q2 与独立 readiness audits。

## D019: T015 因物理合同错误与 direct novelty collision 撤回，B12 返回池

> status: superseded
> date: 2026-07-27
> 取代：D018（取代 B12 active carrier 与 T015 派遣；D018 对 R005 历史比较、
> source identity 边界和 no-second-repair 约束保留）
> 被取代：D020
> 依据：验证 V038/V039/V040 + IEEE primary metadata
> 触发原话：无（独立科学审查）

### 决策

1. T015 在 dispatch 前撤回，状态为
   `BLOCKED_NOVELTY_COLLISION / PACKAGE_WITHDRAWN_BEFORE_EXECUTION`。没有运行
   seed、没有创建方法实现，不产生 science Kill，也不产生 method delta。
2. V038 的两个 P0 单独已足以禁止派遣：原任务把无来源的 100-symbol iid block
   与 128-symbol algorithm/pilot block 混为大气湍流生命周期；Huber
   `w=min(1,c/u)` 又错误使用 `precision=w²/sigma_eps`，而标准 IRLS 是
   `precision=w/sigma_eps`。
3. V039/V040 进一步确认 DOI `10.1109/JLT.2025.3600402` 已把 Huber
   M-estimator robust update、variational-Bayesian covariance adaptation、
   nonlinear Bayesian filtering 与 carrier phase recovery 直接组合，并相对
   BPS 报告最高 0.66 dB OSNR gain。合法全文恢复失败，无法证明 B12 的
   one-step batch adapter 形成未被覆盖的可包装 M-C-A；fail-closed 处理。
4. B12-Q2 standalone 返回候选池，不作 family Kill；但 D018/D029 的单包退出与
   “不得第二个 B12 repair”立即生效。不得把 Huber 公式修正后原样重派，也不得
   用摘要之外的猜测宣称 novelty。
5. formal carrier 恢复为 `NO_ACTIVE_SCIENTIFIC_CARRIER`。foreground 升到
   epoch 37 / CP015 / `POST_B12_NOVELTY_REMAP`；只允许比较 B4、B6、C15 与
   其他机制不同候选的 formal readiness，以及准备下一份独立审查任务。新
   formal owner 与 task clean binding 完成前禁止 seed/MVE。

### 理由

当前发现不是 negative experiment，而是方法合法性前置门失败。继续 T015 会同时
把非物理 iid fade lifecycle 和已被直接竞品占据的 generic Huber CPR 组合成
“方法信号”，违反 FR-22/FR-23、method-production 的 source/novelty gate 与
mission 对 negative/repair 不冒充方法的约束。立即轮换比再做一个 B12 adapter
更可能恢复方法产出。

### 排除的替代方案

- 不把 `sigma_eps/w²` 改成 `sigma_eps/w` 后直接执行：这只修公式，不闭合
  direct novelty collision。
- 不把 JLT 全文不可得解释成“没有碰撞”：官方题名、摘要和 IEEE identity 已证明
  direct method-family overlap；缺全文只会降低放行能力，不会提高 readiness。
- 不运行一个 exploratory B12 probe 来“看看是否有效”：有效性不能替代新颖性，
  且原 channel lifecycle 会制造假增益。
- 不恢复 B1/A4/B10/B9 被禁止的 repair，也不恢复 Scout/P03。

### 影响范围

- formal owner 新建 D030 并清空 active carrier；
- T015 标记 withdrawn，CP015 记录 `mission_method_delta=NONE`；
- current state/portfolio/harvest/master/projects-overview 与 registry 投影到
  epoch 37 / CP015 / post-B12 remap；
- 下一轮先完成候选六维比较和独立 readiness review，不进入 Step 5/Contract/Execute。

### 来源

S001 续接；V038/V039/V040；T015；DOI `10.1109/JLT.2025.3600402` 的
Semantic Scholar/IEEE primary metadata；formal D029。

## D020: 选择 C15 一次性 Step 1–2 formalization workline

> status: superseded
> date: 2026-07-27
> 取代：D019（只取代 post-B12 remap 下一动作；D019 对 T015/B12 的处置、
> no-second-repair 与 CP015 记账保留）
> 被取代：D021
> 依据：调研 R006 + B4/B6/C15 三项独立 formal-readiness audit +
> `stages/gw-search.md` / `stages/gw-acquire.md`
> 触发原话：无（技术推导）

### 决策

1. post-B12 remap 选择
   `C15_DISK_NATIVE_FORMALIZATION_ADAPTER` 作为下一 foreground workline，
   action class 为 `CANDIDATE_FORMALIZATION`。C15 仍是
   `HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE`，formal active scientific
   carrier 保持 `NONE`，不得运行 seed/MVE。
2. T016 是取代 T012 的全新一次性 Step 1–2 包，不是第四次 T012 amendment。
   它只可复用 T011 七份 archives、T011 worker receipt、项目 shared index 和
   明列的 shared papers；形成 actual-source ≥3、去重 ≥20、正式发表 ≥50%、
   必读 ≥5、覆盖 ≥2 技术子方向的 candidate view，以及 8–12 篇 acquisition
   pool。
3. T016 只读闭合五项 recent fulltext identity/content quality，并对 Sato 1975、
   Godard 1980、Yang–Werner–Dumont 2002 三篇 canonical 各执行一次 bounded
   exact-title worktree staging。T016 禁止写 shared main repo；3/3 staging
   PASS 时产出 preliminary coverage report 并停在
   `AWAITING_CANONICAL_PROMOTION`。promotion 必须另包独立审查；不精读、不写
   Q#、不实现、不实验。
4. T016 的预期 `mission_method_delta=NONE`。它若成功，只解除 C15 具体正向
   方法合同的上游 formal readiness 硬门；不得把 source、metadata、canonical、
   governance 或 coverage PASS 记成方法。
5. T016 是 C15 唯一 source/formalization package。actual source、pool、
   fulltext/canonical 或 coverage 任一硬门失败即
   `BLOCKED_FORMAL_READINESS`，C15 返回池，不再给第二个 source repair；
   若 Step 3 后无 task-specific residual M-C-A 或发生 direct collision，也不进
   MVE。
6. foreground 升至 epoch 38 / CP015 /
   `C15_FORMALIZATION_PREP`。R006、D020/formal D031、control、T016 与
   current projections 必须先经独立 dispatch verifier；clean binding 前不得
   执行。

### 理由

- R006 证明当前三候选均非 runnable carrier。B4-Q3 仍缺 carrier-specific M-C-A、
  合法 source 参数和 PADE/双环基础实现；B6 的 atan2/Z-domain/FPGA-delay/Doppler
  形态已被 2023/2025 direct sources 覆盖，且湍流相位环路会撞 D006。
- C15 虽仍缺 Step 1–3，却已有具体的 collapse-safe、scale-fair staged
  equalizer construct、合法 tuned comparator、cheap rule、退出点和可复用 2×2
  FIR runner。T016 本身不产方法，但它是三者中唯一会解除一条已定义正向方法链
  上游硬门的包，因而比 B4、B6 更可能最终产生 `METHOD_SIGNAL`。

### 排除的替代方案

- 不激活 B4：不以源论文双环 reproduction、PCS/Rs 旧轴或 timing-recovery
  时延证据冒充 carrier-specific 方法。
- 不激活 B6：不把 source-native atan2 或 Z 域分析工具包装成新方法，也不重开
  D006 环路旧轴。
- 不恢复 B1/A4/B10/B9/B12 的被禁止 repair，不恢复 B2/B3/B5/B7/B11 的
  formal Kill/伪增量路线。
- 不续改 T012，不把用户当 executor/verifier，也不要求用户阅读技术日志。

### 影响范围

- formal owner 新建 D031；active scientific carrier 仍为 `NONE`；
- 新建 T016；其独立接收前 mission 保持 CP015/no-method=15；
- current state/portfolio/harvest/master/projects-overview 与 registry 投影到
  epoch 38 / CP015 / C15 formalization prep；
- formal stage 保持 Groundwork Step 1–2 workline，不进入 Step 3、Step 4a
  experiment、Step 5、Contract 或 Execute。

### 来源

S001 续接；R006；formal D030；T011/T012 receipts；B4/B6/C15 独立
formal-readiness audits；`stages/gw-search.md`、`stages/gw-acquire.md`。

## D021: 接收 T016 Phase-A identity block 并返回 C15

> status: superseded
> date: 2026-07-27
> 取代：D020（只取代 C15 当前 workline 与下一动作；D020 的一次性合同、
> no-second-source 与 science ceiling 保留）
> 被取代：D022（只取代下一动作与 foreground workline；T016 接收结论、
> C15 no-second-source 边界继续有效）
> 依据：验证 V047 + T016 worker log + candidate-view raw artifact
> 触发原话：无（独立科学验收）

### 决策

1. 接收 T016 Phase A 的正式科学处置为
   `BLOCKED_FORMAL_READINESS / BLOCKED_IDENTITY_CONFLICT`；
   `mission_method_delta=NONE`。该结论不是 C15 science Kill，也不是 Step 1
   coverage PASS。
2. 五个数量门的落盘值为 unique=326、actual source families=8、
   published=`192/326=58.8957%`、必读=10、route coverage=5；但三组同
   normalized title 的不同非空 DOI 触发冻结 identity hard block，故 A2/A3、
   Phase B/C 均未执行。
3. V047 只以 PARTIAL 接收 candidate view 的证据完整性：persisted provenance
   只能回溯 375 个 locator，不支持 summary 的 `raw_rows_included=381`；
   singleton retrieval 口径有偏差，且全 index closure 发现至少另外三组未列
   conflict。上述缺陷不改变 hard block，但禁止把该 view 当作完整覆盖证明。
4. 按 D020/D031 的一次性退出边界，C15 返回候选池，不给第二个 source/
   formalization package，不派 Phase B，不修 alias/provenance/evaluator。
5. CP016 记为 same-axis=1、repair=0、no-method=16，
   `ADEQUATE / package ALIGNED`；mission 继续 `DRIFTED/STALLED`。
6. foreground 升至 epoch41 / CP016 /
   `POST_C15_FORMALIZATION_REMAP`。当前仍无 active scientific carrier；
   下一动作只允许机制级 carrier remap 与 formal-readiness 比较，remap 完成前
   不运行实验。

### 理由

冻结规则没有授权把 `.short`/`.v1` 后缀解释为 DOI alias；executor 正确
fail-closed。即使这些后缀将来可由官方元数据归并，D020 已明确 T016 是 C15
唯一 source package，且本包的 provenance view 还有独立可复现性缺陷。继续修
会把 no-method mission 再次运行成接口/元数据 repair 链；轮换更符合方法生产
目标。

### 排除的替代方案

- 不原地 canonicalize `.short`/`.v1` 后继续 A2/A3：这会修改冻结 identity
  predicate，并构成第二个 C15 source repair。
- 不派 Phase B：Phase A 终态不是
  `PHASE_A_COMPLETE_AWAITING_PHASE_B`。
- 不把 326/8/58.8957%/10/5 写成 coverage PASS：identity 与 provenance
  completeness 均未闭合。
- 不把 PARTIAL evidence quality 误写成 C15 方法或科学失败；旧 shared-mu
  family 仍是 unresolved。

### 影响范围

- formal owner 新建 D032；active scientific carrier 保持 `NONE`；
- mission-log 追加 CP016/no-method=16；
- control/current projections 转 epoch41 / CP016 / post-C15 remap；
- C15 标记 `BLOCKED_FORMAL_READINESS / RETURNED_TO_POOL /
  NO_SECOND_SOURCE_PACKAGE`，禁止 Phase B、Step 3、seed/MVE。

### 来源

S001 续接；T016；step-016 worker log；candidate-view artifact；V047；
formal D031。

## D022: 选择 C16-open 一次性 Step 1–2 formalization workline

> status: superseded
> date: 2026-07-27
> 取代：D021（只取代 post-C15 remap 的下一动作；D021 的 T016 正式处置、
> C15 返回池与 no-second-source 边界保留）
> 被取代：D023（只取代当前 workline 与下一动作；D022 的 T017 一次性合同、
> C16-open no-second-source 边界与 science ceiling 保留）
> 依据：调研 R007 + current portfolio/harvest + formal D044/D032
> 触发原话：无（机制级 remap 的技术推导；用户对长期 Goal 的端到端授权已由 D004 记录）

### 决策

1. 接收 R007 的有界 mechanism-level remap：当前为
   `READY=0 / NEEDS_SMALL_ADAPTER=0 / HYPOTHESIS_ONLY=5`，不存在可直接
   运行 seed 的 active scientific carrier。
2. 在 C16-open、Q14、B4、Q-ML4、C04/C09-open 五个机制不同候选中，选择
   **C16-open full-complex 2×2 FIR non-modulus blind equalizer** 获得一次性
   Groundwork Step 1–2 formalization workline。
3. 选择依据不是旧 C16 的 post-hoc complementarity，而是 current authority
   已确认旧 spatial 2×2 whitening+real-Givens expert 缺 FIR 能力，不能对抗
   11-tap 2×2 CMA；因此 equalizer-paradigm axis 仍开放，并存在明确可证伪的
   task-matched source/competitor 问题。
4. formal active scientific carrier 保持 `NONE`。T017 的
   `mission_method_delta` 预注册为 `NONE`；它只关闭 Step 1–2 formal
   readiness，不运行任何方法或实验。
5. T017 必须满足 actual source≥3、unique≥20、正式发表≥50%、必读≥5、
   至少两条技术 route，并取得≥5篇 title/identity/content-quality 合法全文；
   生成 coverage-gap report 后停止在 `AWAITING_COVERAGE_CONFIRMATION`。
6. 任一 source/identity/route/fulltext hard gate 失败即
   `BLOCKED_FORMAL_READINESS`，C16-open 返回池且不给第二个 source/
   formalization package。即使 PASS，未经用户极短 coverage 确认也不得 Step 3。
7. foreground 更新为 epoch42 / CP016 /
   `C16_FIR_HOS_FORMALIZATION_PREP`。D033、T017 与独立 dispatch review
   完成前不执行。

### 理由

- 相对 Q14，C16-open 已有一个由 current authority 确认的 comparator
  capability mismatch；Q14 在 5/5 全文后仍卡在问题四判据 2 UNKNOWN，并有
  receiver-visible residual headroom 的强负先验。
- 相对 B4，C16-open 与当前 coherent dual-pol FIR receiver 共用输入、输出、
  指标和 runner 接口；B4 的 source 已拥有双环本身，剩余 multi-rate 增量、
  carrier-specific latency M-C-A 与 PADE 状态机均未闭合。
- 相对 Q-ML4，C16-open 不承担从 30 m IM/DD 辐照度代理到星地 coherent
  complex-field 符号级 DSP 的四重迁移债。
- 该选择只承认“更值得关闭上游门”，不预支任何方法增量。Step 1/2 PASS、
  coverage confirmation、Step 3/3.5、Step 4a 与公平最小构造仍分别独立。

### 排除的替代方案

- 不激活 Q14：四判据 2 仍 UNKNOWN，不得先建 residual head。
- 不激活 B4：source-native dual loop 不是我方方法，载波专属 latency 问题与
  实现均缺。
- 不激活 Q-ML4：旧“全过”属于 IM/DD 原问题，不能直接迁移成 coherent/star-
  ground Q#。
- 不修 C15/T016 alias/provenance，也不恢复 B1/A4/B10/B9/B12 repair。
- 不直接把旧 C16 代码改成 FIR 后跑 seed；那会跳过 Step 1–3 与 Step 4a。

### 影响范围

- formal owner 新建 D033；active scientific carrier 继续为 NONE；
- live control 递增到 epoch42，新增允许 action
  `CANDIDATE_FORMALIZATION`；
- 新建 T017 与 Step 1–2 输出路径；
- master-state、projects-overview、state/current、portfolio/current、
  harvest/current 和 registry 投影到 C16 formalization prep；
- CP016 不变；只有 T017 经独立科学验收后才追加 CP017。

### 来源

S001 续接；R007；portfolio/current；harvest/current；Q14 S039/D044；
R006 的 B4 formal audit；formal D032。

## D023: 接收 T017 Phase-A formal-readiness block 并返回 C16-open

> status: superseded
> date: 2026-07-27
> 取代：D022（只取代 C16-open 当前 workline 与下一动作；D022 的一次性
> source/formalization 合同、science ceiling 与比较依据保留）
> 被取代：D024
> 依据：验证 V049 + T017 worker log + candidate-view/raw search artifacts
> 触发原话：无（独立科学验收）

### 决策

1. 接收 T017 Phase A 的正式科学处置为
   `BLOCKED_FORMAL_READINESS / BLOCKED_SEARCH_OR_IDENTITY`；
   `mission_method_delta=NONE`。这不是 C16 science Kill，也不是 Step 1
   coverage PASS。
2. 独立重算为 raw rows=53、unique=44、actual source family=1
   （OpenAlex）、必读=2、R1/R2 direct=`1/3`、pool=10、quarantine=0。
   TechRxiv 误标纠正后 published/preprint/unknown=`41/3/0`，
   published ratio=`41/44=0.9318181818`。
3. source `1<3` 与 must-read `2<5` 两项冻结硬门 FAIL；因此 Phase B、
   coverage confirmation、Step 3、实现与实验均未授权。
4. V049 为 `PARTIAL / P0=0/P1=2/P2=0`：一项是 TechRxiv published 误标，
   一项是 raw 未持久化 per-source error/status。两项都不改变双硬失败，也不
   授权 artifact/source repair。
5. 按 D022/D033 一次性退出边界，C16-open 返回候选池，不给第二个 source/
   formalization package，不追加第六查询，不修 label/receipt，不派 Phase B。
6. CP017 记为 same-axis=1、repair=0、no-method=17，
   `ADEQUATE / package ALIGNED`；mission 继续 `DRIFTED/STALLED`。
7. foreground 升至 epoch43 / CP017 / `POST_C16_FORMALIZATION_REMAP`。
   active scientific carrier 继续为 `NONE`；下一动作只允许机制级 remap 与
   formal-readiness/problem-evidence 比较，不运行新实验。

### 理由

44 个候选、两条 direct route 与高 published ratio 说明检索不完全空洞，但
冻结门要求的是可交叉核验的多源覆盖和足够密度的必读核心材料；单一 OpenAlex
与两篇必读不足以支撑 acquisition/Step 2。继续补 source receipt 或第六查询
既修改一次性合同，也会把 method-production mission 再次拖入元数据 repair。
因此接收 fail-closed、保留 family unresolved 并立即轮换。

### 排除的替代方案

- 不修 TechRxiv label 后重算包；纠正值已由 V049 记录且不改变 gate。
- 不补写 per-source status 或追加 S2/arXiv 查询；那是第二个 source repair。
- 不进入 Phase B；A6 明确 FAIL。
- 不把 44/93.18%/R1-R2 命中包装为 coverage、方法或 novelty 信号。
- 不运行旧 C16 spatial HOS、改写 FIR 后直接 seed，或复用 seeds 71–80。

### 影响范围

- formal owner 新建 D034；active scientific carrier 保持 `NONE`；
- mission-log 追加 CP017/no-method=17；
- control/current projections 转 epoch43 / CP017 / post-C16 remap；
- C16-open=`BLOCKED_FORMAL_READINESS / RETURNED_TO_POOL /
  NO_SECOND_SOURCE_PACKAGE`；
- candidate view 只作 partial defensive evidence，不作方法材料。

### 来源

S001 续接；T017；step-017 worker log；candidate-view/raw artifacts；V049；
formal D033。

---

## D024: 选择 Q14 mandatory Step 3.5 problem-evidence workline

> status: superseded
> date: 2026-07-27
> 取代：D023（只取代 post-C16 下一 workline 与 foreground；D023 对 T017、
> C16-open 返回池和 no-second-package 的处置继续有效）
> 被取代：D025
> 依据：调研 R008 + formal Q14 S037/S038/S039/D044 + current
> portfolio/master-state + framework gw-supplement/gw-feasibility
> 触发原话：无（技术推导；长期 Goal 自主推进授权已记录于 D004）

### 决策

1. 选择 Q14
   `standard-CMA always-online + strictly-causal receiver-visible additive
   residual corrector` 获得一次 T018 Groundwork Step 3.5 /
   problem-evidence workline；formal active scientific carrier 仍为 `NONE`。
2. T018 只闭合 mandatory Step 3.5 与四判据 2，固定
   `mission_method_delta=NONE`，禁止实现、simulation/Probe/MVE/seed 与
   Step 4a。
3. 冻结正向合同：
   - target：`z_out=z_CMA+gφ(z_CMA, causal CMA trace/context)`；
   - runtime 只允许 receiver-visible causal information；
   - fair comparator 以 tuned CMA+DD-LMS/RDE 为主，blind affine/simple
     residual DSP 为辅助；`fixed+PI` 只作评估口径；
   - primary packaging 为“保留盲跟踪的轻量因果 residual correction”；
   - fallback packaging 为受限工况的触发规则与 complexity/performance
     trade-off。
4. T018 必须满足 `gw-supplement.md`：≥6 系统关键词组合、actual Semantic
   Scholar + 至少一源、一个核心竞品双向引用链、最多 3 轮收敛、新高相关论文
   acquire/read、Q14-specific literature update。
5. 只有外部证据同时证明稳定 receiver-visible residual、decision/soft 或
   complexity 收益、且 tuned cheap DSP 未覆盖，才能建议
   `PROBLEM_EVIDENCE_READY_FOR_STEP4A_ZERO`；该状态仍不授权 A0。
6. source/identity/fulltext/convergence 任一门失败，或判据 2 仍
   UNKNOWN/FAIL，Q14 返回池且不给第二个 problem-evidence package；下一轮
   依次比较 Q-ML4、B4、C04/C09-open。
7. foreground 递增到 epoch44 / CP017 /
   `Q14_STEP35_PROBLEM_EVIDENCE_PREP`。T018 经独立 dispatch review PASS 前
   不执行。

### 理由

Q14 相对 Q-ML4、B4 与 C04/C09-open 的 debt 最集中：已有 Step 1–3、5 篇
全文、receiver 接口和传统 comparator，缺口只剩 mandatory Step 3.5 与判据 2。
Q-ML4 仍需五重场景/表示/输出迁移，B4 连 carrier-specific M-C-A 与 PADE
实现都缺，C04/C09 的 target 自身有常数零损解。T018 因而能用最小可逆成本
直接证伪一个方法入口，而不是再做元数据修复或提前跑实验。

### 排除的替代方案

- 不选择 Q-ML4 先建 coherent scene-transfer：迁移债多于一个问题证据门；
- 不选择 B4：source 已拥有双环主体，新增 latency M-C-A 与基础实现均未闭合；
- 不选择 C04/C09-open：先要发明非退化 target，conditional-information 证据
  又已撤回；
- 不把 P03、blind-affine harmful 或 hybrid-routing 0.003693 当作 Q14 family
  Kill；它们只作局部负先验；
- 不用实验、oracle/TX truth 或“没有直接论文”反向补四判据合法性。

### 影响范围

- formal owner 新建 D035；
- foreground=epoch44 / CP017 /
  `Q14_STEP35_PROBLEM_EVIDENCE_PREP`；
- formal active scientific carrier 保持 `NONE`；
- 新建 R008/T018；T018 最终验收前不追加 CP018；
- Q14 若失败即一次性退出，禁止第二个 problem-evidence package。

### 来源

S001 续接；R008；Q14 R009/S037/S038/S039/D044；R006；R007；
portfolio/current；master-state；gw-supplement；gw-feasibility。

---

## D025: 修复 T018 coverage gate 与可复现 receipt 合同

> status: superseded
> date: 2026-07-27
> 取代：D024（保留 Q14 选择、正向方法合同、一次性退出边界和
> `mission_method_delta=NONE`；只取代 T018 dispatch contract 与 foreground）
> 被取代：D026
> 依据：critic V050 + framework gw-acquire/gw-supplement + tools/search CLI/source
> 触发原话：`voice.md` 2026-07-26（D004 已记录 Goal 主控端到端授权；本次无新原话）

### 决策

1. Q14 仍只获得一次 mandatory Step 3.5/problem-evidence workline；formal
   active scientific carrier 仍为 `NONE`，不进入 Step 4a、实现或实验。
2. T018 若发现 1–5 篇新增必读/建议读，executor 只能完成合法 acquire 和
   `gw-acquire.md` coverage-gap report，随后以
   `AWAITING_DELEGATED_COVERAGE_GATE` 暂停；精读与 synthesis 尚未授权。
3. coverage report 必须由未参与 acquisition 的独立 verifier 审查，再由 Goal
   主控依据 D004 的用户端到端授权作 delegated coverage decision。executor
   不得自审放行；若缺口需要私有全文或用户独占材料，主控不得伪造批准。
4. 该 project-specific adapter 只替代本 mission 中“让用户阅读技术覆盖报告并
   判断”的接口，不修改 `gw-acquire.md` 通用规则，也不降低全文、identity、
   source、收敛或问题证据门。
5. T018 的七个 terminal 状态与两个 continuation 状态分离；timebox/coverage
   continuation 不追加 CP、不提 formal disposition 或 streak。
6. 六条 Round-1 检索和两条 citation 命令必须显式使用 `--format json -o
   <frozen-path>`；不得依赖 auto-save 猜测 receipt 路径。
7. Q14 五篇既有全文与新增 paper artifacts 的权威根是共享主仓库
   `D:\code\study\research-protocol\papers`，不是 worktree 的稀疏 `papers/`；
   T018 必须冻结绝对 content path/hash，并保护 shared repo 既有改动。
8. foreground 递增为 epoch45 / CP017 /
   `Q14_STEP35_TASK_AMENDMENT_REVIEW`。独立复审 PASS 前仍不执行 T018。

### 理由

V050 以 P0/P1/P2=`1/5/1` 拒收初版 T018：新论文路径绕过 coverage-gap
确认硬门，citation 固定路径不可由命令复现，timebox 的 terminal/continuation
schema 自相矛盾，且三处 current projection stale。用户已在 D004 明确要求 Goal
主控端到端工作且不让用户判断科学正确性；因此保留“获取后暂停 + 独立审查”的
实质门控，把最终技术确认交给主控，而不是删除该门或让 executor 自行确认。

### 排除的替代方案

- 不直接让 executor acquire→read：这会绕过 Step 2→3 强制门；
- 不要求用户阅读 coverage report：与 D004 和当前长期 Goal 的协作接口冲突；
- 不把 coverage gate 失败算方法或 package checkpoint；
- 不借合同修复激活 Q14 carrier、降低 source/fulltext 门或增加第二个 Q14 包。

### 影响范围

- formal owner 新建 D036；
- live control/T018 递增到 epoch45 / CP017，仍待独立 dispatch review；
- 修正 formal topic-index“当前位置”、registry 与 harvest/current stale 投影；
- mission-log 保持 CP017/no-method=17，未产生方法增量。

### 来源

S001 续接；V050；D004；R008；D024；formal D035；Q14 S037/S038；T018；
gw-acquire；gw-supplement；tools/search CLI。

---

## D026: 停止 T018/Goal 形式化链并建立 pre-formal 方法工厂

> status: active
> date: 2026-07-28
> 取代：D025 的 Q14/T018 当前执行授权；D004 的 Goal 端到端协作模式
> 被取代：无
> 依据：mission CP001–CP017；R007；R008；S002
> 触发原话：`voice.md` 2026-07-28

### 决策

1. 冻结 T018：不做 final-binding，不执行 Q14 Phase A，不追加 CP018。Q14
   保持 `UNRESOLVED`，本决策不是科学 Kill。
2. 停止当前长期 Goal 自动续跑，恢复“主控给短提示词—用户开普通 GLM—
   GLM 把细节写文件—主控只收关键索引”的协作接口。
3. 在 Research Direction Lab 中加入一个受限的
   `PREFORMAL_METHOD_FACTORY` lane。它只能产生诊断性方法信号，不是
   Groundwork Step 4a MVE，也不能产生 Go/Kill、论文结论或 formal seed。
4. 当 formal active scientific carrier 为空，且 portfolio 同时
   `READY=0`、`NEEDS_SMALL_ADAPTER=0` 时，禁止继续串行 formalize
   `HYPOTHESIS_ONLY` 候选；必须转入方法工厂或上交战略裁决。
5. 方法工厂复用已验证的 simulator/evaluator、传统 baseline、paired
   realization 与共享诊断 seeds；单包构造 3–5 个机制不同的候选，并在同包
   做公平 smoke compare。除共享测试床本身无法成立外，接收包的
   `mission_method_delta` 至少为 `CONSTRUCT_CREATED` 或
   `FAIR_COMPARISON_RUN`，不得再以固定 `NONE` 作为正常产出。
6. 方法工厂只输出 `DIAGNOSTIC_METHOD_SIGNAL`、
   `NO_DIAGNOSTIC_SIGNAL` 或 `BLOCKED_SHARED_TESTBED`。只有产生正信号的
   winner 才返回正式 Groundwork Step 1–3/3.5/4a，补齐问题、文献、碰撞与
   科学门控后再决定是否进入正式实验。
7. 本轮只做最小机制改造：更新 Research Direction Lab Skill、其
   `method-production` 参考和 FR-22 的窄例外；不新建 controller/scheduler，
   不做重型验证。

### 理由

CP001–CP017 的 `mission_method_delta` 全部为 `NONE`，当前
`METHOD_SIGNAL=0`、`PROMOTION_READY=0`、active scientific carrier 为空。
R007 又给出 `READY=0 / NEEDS_SMALL_ADAPTER=0 / HYPOTHESIS_ONLY=5`。继续
执行 T018 只会把同一批假设候选逐个加工成更完整的形式化档案，不能提高实际
产生方法的概率。当前缺口不是再加一道审查，而是缺少一个可快速构造、并排
比较和淘汰方法的生产环节。

### 排除的替代方案

- 不继续 T018：它的合同已通过静态审查，但仍不改变零方法信号状态；
- 不只缩短 timebox：包更短不会改变“每包 delta 固定 NONE”的目标函数；
- 不删除 baseline、公平性、因果性等科学护栏：方法工厂只降低 formal
  readiness 前置成本，不降低诊断比较质量；
- 不再新建长程 controller/scheduler：先由 Skill + 固定账本字段验证机制；
- 不把诊断 winner 直接包装成论文方法：正式结论仍需完整 Groundwork。

### 影响范围

- live foreground 更新为 epoch47 / CP017 /
  `PREFORMAL_METHOD_FACTORY_SKILL_UPDATE`；
- T018 与 Q14 workline 冻结，mission streak 暂停在 17；
- 更新 Research Direction Lab Skill、`method-production.md`、
  `stages/groundwork.md` FR-22 与 `AGENTS.md` 索引；
- Skill 更新后派普通 GLM 执行首个方法工厂 sprint。

### 来源

S002；R007；R008；mission-log CP001–CP017；用户 2026-07-28 原话。

---

## D027: 部分接收 T019 并只授权一次 corrected-baseline M5 family 扩展

> status: superseded
> date: 2026-07-28
> 取代：D026 的首个 sprint 当前执行状态；保留方法工厂总合同
> 被取代：D028
> 依据：T019 commit `e1c479e` / worker log / raw / V052
> 触发原话：无（技术推导）

### 决策

1. 接收 T019 的工程事实与 `mission_method_delta=FAIR_COMPARISON_RUN`；追加
   CP018。科学处置为
   `SCIENCE_VERDICT_REJECTED / DIAGNOSTIC_BATCH_PARTIAL`。
2. 只接受“这五个具体实现未过诊断门”。拒收“CB1 是结构性不可恢复
   attractor”“五族 receiver-visible gap≈0”及任何 family Kill。
3. M1/M2/M3/M4 不继续：其 baseline、因果性、去重或机制设计不足以支持二修。
   M5 保留为 `WEAK_DIAGNOSTIC_SEED`，依据是 15 help / 5 hurt / 40 tie 和
   trimmed mean `-0.00895`，但旧结果本身不能晋级。
4. 只授权一个 corrected-baseline 扩展包：以 B01-R current fixed-μ CMA
   `μ=0.03` 为系统 baseline，并加入合法 C11-causal 与 receiver-visible
   blind-affine；用 calibration prefix 与 eval window 严格分离、fresh dev/test
   seeds 和 B01-R 四分类。
5. 新包不是重跑旧 M5。它必须构造 3–4 个公开星座先验驱动、统计结构不同的
   因果 shell-distribution 方法，并在 fresh held-out test 上比较。只有 test
   信号算 `DIAGNOSTIC_METHOD_SIGNAL`。
6. 若 corrected-baseline 下没有 held-out 信号，CB1 z-only/post-processing
   轴退出方法工厂，不给第三包；下一轮必须换真实信息源或换测试床。

### 理由

T019 首次实现了方法工厂所需的实际构造与 paired compare，证明流程改造能提高
工作量；但它也暴露“历史 runnable baseline 被误当 current fair baseline”和
“whole-window statistics 被误当 causal”的新漏洞。直接接受总阴性会重复过去
的假 Kill；完全丢弃 M5 又会忽略唯一有方向性的 raw 弱迹象。一次 corrected
baseline + fresh held-out 扩展是最小且可证伪的折中。

### 排除的替代方案

- 不修 T019 文档/结果 JSON 后原样重跑：不会解决 baseline 与因果 P0；
- 不继续 M1–M4：没有比 best legal weak seed 更强的二修依据；
- 不直接把 M5 包装成方法：旧信号使用复用 seeds、under-tuned comparator 且
  非因果；
- 不立即开 pilot/history/decoder 三条接口：当前均有已知接口或物理动态债，
  更可能再次停在基础设施阻断；M5 有现成弱迹象，先消费一次有界机会。

### 影响范围

- mission 新增 CP018；no-method streak 结束，但 method-signal 仍为 0；
- live foreground 转 corrected-baseline M5 family sprint；
- Research Direction Lab Skill 增加 current baseline、prefix causality、
  去重和 smoke receipt 四条首轮实测约束；
- 普通 GLM 执行下一包；失败后不再留在 CB1 z-only 轴。

### 来源

T019；step-019 worker log；raw/result；V052；B01-R；C11 legality。

---

## D028: 接收 T020 工厂级方法信号并转入 Q15 正式 Groundwork

> status: superseded
> date: 2026-07-28
> 取代：D027 的 corrected-baseline 扩展执行状态；保留 D026 方法工厂总合同
> 被取代：D029
> 依据：验证 V053 + T020 commit `5cf76d5` / worker log / raw / result
> 触发原话：无（技术推导）

### 决策

1. 接收 T020 的 `mission_method_delta=METHOD_SIGNAL` 与 M4
   `DIAGNOSTIC_METHOD_SIGNAL`，追加 CP019；claim ceiling 固定为
   `DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE`。
2. M4 暂命名为 Q15 候选：
   `prefix-gated identity/quantile-shell transport after fixed-μ CMA`。它只用
   128-symbol receiver-visible prefix 的功率与幅度离散度选择 identity 或
   frozen quantile transport。
3. 不接受“普遍均衡增益”或“信道条件自适应已证实”。38/140 个触发样本集中
   在 7/20 seeds；当前证据更准确地表明 M4 能检测并部分修复固定
   `μ=0.03` CMA 的某类随机实现/初始化塌缩。
4. CB1 z-only 方法工厂到此结束，不给第三包。Q15 必须从 Groundwork Step 1
   返回，补齐 Step 1–3/3.5/4a 后才可能进入正式实验。
5. 下一包 T021 只做 Step 1 检索与 Step 2 公共全文获取/coverage-gap report。
   检索必须同时覆盖 direct collision、CMA/RDE/MMA 稳健化、restart/multistart/
   reinitialization、blind AGC/radius calibration/distribution matching 四条线。
6. Step 2 后暂停。未经过主控 coverage gate，不得精读、写 Q15 四判据 PASS、
   进入 Step 3.5/4a、补 gate artifact 或运行新 seed。

### 理由

V053 独立复算 1120 raw rows，M4 相对 `μ=0.03` CMA 的 seed-cluster
mean/CI/help-hurt-tie 为 `-0.082589 / [-0.138115,-0.031779] / 7-0-13`；
相对 blind-affine 与 C11 的 paired CI 也均低于 0。实现严格 prefix-only，
test 不使用 truth 选择动作，因此达到方法工厂的诊断门。

但这不是 formal Go：逐 pair gate receipt 未保存；offline 四分类只保留每 cell
首个 seed；方法只在 7 个 seed 上产生 seed-level gain，且当前未比较更稳健的
CMA tuning、restart 或 multistart。直接实验会再次把 baseline 脆弱性包装成
贡献；先做 formal collision/problem-survival 是最小合法动作。

### 排除的替代方案

- 不开第三个 CB1 z-only 工厂包：D027 已明确 one-last extension，且已有 winner；
- 不把 M4 直接写成论文方法：尚无 Step 1–3/3.5/4a、近期 direct competitor 或
  cheap-alternative closure；
- 不因 artifact 债务否决本轮信号：paired comparator 复算与只读重跑均支持
  诊断终态，债务可以在正式阶段闭合；
- 不恢复 Q14/T018：Q15 已有实际构造与 held-out 诊断信号，更接近方法产出。

### 影响范围

- foreground 更新到 epoch51 / CP019 / `Q15_GROUNDWORK_STEP1_2_READY`；
- formal owner 新建 D037，Q14/T018 继续冻结；
- current state/portfolio/harvest/master/projects-overview 投影到 Q15；
- 新建 T021；禁止第三个 factory、Q15 Step 3+ 与科学实验。

### 来源

T020；step-020 worker log；factory-contract.v2；raw/result；V053；D026/D027。

---

## D029: 部分接收 T021，并把收据修复与 Q15 Step 3 合并执行

> status: superseded
> date: 2026-07-28
> 取代：D028 的 Q15 Step 1–2 执行状态；保留其方法工厂终止与 claim ceiling
> 被取代：D030
> 依据：验证 V054 + T021 commit `287fb6a` / worker log / raw / paper receipts
> 触发原话：无（技术推导）

### 决策

1. 接收 T021 的 129 unique、121/129 published、11 必读、4 路线，以及
   6 篇独立核心工作 + 2 篇早期/长版全文获取事实；追加 CP020，
   `mission_method_delta=NONE`。
2. 不接受“Step 1 三源门全过”：merged raw 只含 Semantic Scholar 与
   OpenAlex；IEEE 只有文字 hits，无结构化 raw。T021 终态改记为
   `PARTIAL_WITH_INTEGRITY_REPAIR_REQUIRED`。
3. 不把这项收据债拆成纯修复包。T022 先补 IEEE raw、五篇 blit canonical/index
   receipt；前置门通过后在同一包内精读六篇独立核心和两篇补充全文。
4. D1/C1/C4 是会改变 direct-collision/cheap-alt 判断的 mandatory debt，
   但三轮下载已经耗尽。本轮不做第四轮获取；它们进入 Step 3.5 输入。
5. D1 未闭合前禁止 novelty、`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`、
   Step 4a 或实验。Step 3 只允许形成结构化文献证据和 Q# 候选。

### 理由

V054 重算确认 T021 的核心检索规模和八份全文真实，但 actual source union=2，
五篇 blit 未入 `papers/index.json`，且 ignored raw/papers 不由 commit 自包含。
这些缺陷推翻“全门 PASS”，不推翻已经存在且标题/哈希可核验的全文。

单开纯收据修复会重现本 mission 的“审计/修复机器”失败模式。把两个确定性收据
修复放进 Step 3 前置门，修通后立即精读，既不降证据标准，也确保下一包产生
direct-collision、cheap-alt 和 Q# 判断材料。

### 排除的替代方案

- 不直接无条件进入 Step 3：source receipt 与 paper index 确有缺口；
- 不单开纯 repair 包：决策价值过低，会再次把方法生产线变成流程修复线；
- 不要求用户现在手动找 D1/C1/C4：已有六篇独立核心全文足以开始精读，缺口可由
  mandatory Step 3.5 处理；
- 不因 D1 风险直接 Kill Q15：现有证据只证明思想同源，尚未证明 action、
  information boundary 与 problem 三者完全重合。

### 影响范围

- foreground 递增到 epoch52 / CP020 / `Q15_STEP3_WITH_RECEIPT_PREFLIGHT_READY`；
- formal owner 新建 D038；T022 只做两项收据修复 + Step 3；
- 第三个 factory、Step 3.5+、实验及论文声称继续禁止。

### 来源

T021；step-021 worker log；q15 annotated raw；paper artifacts；V054；D028/D037。

---

## D030: 部分接收 T022，并以正确归一化终局审判 Q15

> status: superseded
> date: 2026-07-28
> 取代：D029 的 Step 3 workline
> 被取代：D031
> 依据：验证 V056 + T022 commit `f3a47260f732e0987743f32bffc6d21d7f92e6aa` +
> critic `audit_t022_science`
> 触发原话：无（技术推导）

### 决策

1. 接收 T022 的保守终态：六篇独立核心满足 Step 3 内容门，Q15 仍为
   `PENDING_STEP35`，`mission_method_delta=NONE`；追加 CP021。
2. 不接受“8/8 全结构合同 PASS”：两篇补充 D3′/D4′ 已读但未各自完整展开
   15 字段和七个独立子表。该 P1 不推翻六篇独立核心门。
3. 不接受“四判据 1/3/4 已过、只差 D1/C1/C4”。判据 1/2 均降为
   `PARTIAL`，3/4 为 PASS。D1 官方全文公开可得；D3 的 \(R_n\) 是 decision
   error radius，不是星座 shell radius。
4. T020 的 M1 用功率比直接乘复振幅，正确因子应取平方根；evaluator 又不恢复
   尺度。这一 P0 使 M4 的收益可能只是补常规 gain normalization。
5. T023 是 Q15 唯一终局包：先完成真正 Step 3.5；仅在四判据全过后，同包进入
   Step 4a，用 correct sqrt normalization、gated scalar 等强简单先验复判。
6. 本包必须输出 Q15 `NO-GO` 或 `STEP4A_RECOMMENDATION_READY`。无论 blocked
   或 No-Go，均不再给第四个 Q15 repair/factory 包。

### 理由

继续只补 D1/C1/C4 会围绕错误 blocker 工作。源码显示
`scale=E|s|²/E|z|²` 被直接用于 `scale*z`；这会把功率归一化写成振幅过校正。
T020 没有合法的 conventional amplitude-normalization comparator，因而不能证明
非线性 shell map 有独立信息增量。

Q15 仍比轮换到 hypothesis-only 候选更接近方法：它已有实际构造和诊断 slice；
一次同时闭合 D1/定向文献与正确 baseline 的终局包，能直接给出方法包装边界或
No-Go。相比纯文献包、纯修公式包或重新方法工厂，其决策价值更高。

### 排除的替代方案

- 不原样派 D1/C1/C4 acquisition：D1 已公开，C1/C3 与目标相关性弱；
- 不直接轮换：尚有一个小而决定性的 conventional-normalization 解释可验证；
- 不只修 M1 后再留下一轮：T023 合并 Step 3.5 与条件式 Step 4a，失败即退出；
- 不把 corrected scalar 当“更严苛 SOTA”：它是接收链最基本、任务匹配的
  conventional comparator，符合 D005/FR-25 的务实 baseline 标准。

### 影响范围

- foreground 递增到 epoch53 / CP021 /
  `Q15_TERMINAL_STEP35_STEP4A_READY`；
- formal owner 新建 D039；T023 获得 Step 3.5 + 条件式 Step 4a 授权；
- Step 5、Contract、Execute、论文声称与后续 Q15 repair 继续禁止。

### 来源

T022；step-022 worker log；V056；T020 methods/evaluator 源码；D029/D038；
groundwork/gw-supplement/gw-feasibility；TL-20/TL-22/TL-30/TL-32。

---

## D031: 拒收 T023 的绑定式 Step 4a 终态，接收 gated normalization 诊断方法信号

> status: active
> date: 2026-07-28
> 取代：D030 的 T023 终局 workline
> 被取代：无
> 依据：验证 V058 + T023 commit `89d8174c56a7729c34a1268ef52394c58e889924`
> + 三路独立审查 `audit_t023_gate/audit_t023_science/audit_t023_literature`
> 触发原话：无（技术推导）

### 决策

1. T023 不作为合法 Step 4a 完成接收。Phase A 明确得到的四判据没有全部
   PASS，却越过 A4/B0 硬门运行 Phase B；合法 formal disposition 为
   `Q15_MAP_STEP35_NO_Q_NO_GO`。
2. Q15 primary（nonlinear monotone-radius map）退出，不给第四个 Q15 repair；
   T023 Phase B 只保留为 `NONBINDING_DIAGNOSTIC`。
3. 不接受 “全部被 conventional normalization 吸收 / delta=NONE”。独立重算
   显示低复杂度 `gated_scalar` 在 old/fresh slice 相对 tuned CMA 分别
   `−0.087444/−0.139286`，95% CI 均在 0 以下，help/hurt/tie 分别
   `7/0/13`、`13/0/7`，且 healthy-worst=`0`。
4. 因此本包的 mission method delta 记为 `METHOD_SIGNAL`，但 claim ceiling 仅为
   `NONBINDING_DIAGNOSTIC`。该信号对应 Q15-derived fallback / salvaged
   component `G1_SAFE_GATED_NORMALIZATION`，不是 nonlinear-map repair。
5. T024 只给 G1 一次终局 Groundwork 闭合：先做 candidate-delta 的 direct
   collision/四判据门；全部 PASS 才同包用全新 seeds 和完整 gate/raw receipt
   做正式 Step 4a confirm。失败即退出 G1，不留纯修复包。

### 理由

always-on pooled/per-pol/robust normalization 的 healthy-worst 为
`0.015625–0.027344`，均大于 MDE=`0.005`，执行报告把大小关系写反；因此
identity fallback 的安全价值没有被 always-on conventional normalization 吸收。
同门控的 correct-sqrt scalar 又在 old/fresh 两组都优于 M4 map，说明应淘汰的是
nonlinear map，而不是 gate+safety-layer 构造。

这一构造已经存在、可运行且有 fresh diagnostic signal。把它直接丢掉再轮换到
Q-ML4/B4/C04-C09 等 hypothesis-only 候选，会重新回到只做形式化、没有方法动作
的旧循环。T024 仍先守 Groundwork 碰撞门，不能把越门数字反向当 formal Go。

### 排除的替代方案

- 不接受 T023 的绑定式 `Q15_ABSORBED...`：A4/B0 越门、D1/read-log 与检索
  closure 不完整、relative comparator 统计和 raw receipt 均有缺口；
- 不修 Q15 nonlinear map：独立消融已显示 map 无 gate+scale 外增量；
- 不把 G1 直接标 `PACKAGING_BOUNDARY`：现有数字来自越门诊断，尚未完成
  candidate-specific collision 和 formal fresh confirm；
- 不立刻轮换到 hypothesis-only 候选：G1 是当前唯一已有 runnable construct、
  fair-comparator diagnostic 和正向安全-性能信号的 carrier。

### 影响范围

- foreground 递增到 epoch54 / CP022 /
  `G1_SAFE_GATED_NORMALIZATION_FORMAL_CONFIRM_READY`；
- formal owner 新建 D040；T024 获得 delta-specific Step 3/3.5 + 条件式
  Step 4a confirm 授权；
- Q15 map、T023 Phase B binding claim、Step 5/Contract/Execute 和旧轴 repair
  继续禁止。

### 来源

T023；step-023 worker log；raw/result；V058；D030/D039；method-production；
groundwork/gw-supplement/gw-feasibility。

---

## D032: 拒收 T024 的 Gate6 No-Go 与 formal confirm，G1 退出实验修复线并转有界包装待决

> status: active
> date: 2026-07-28
> 取代：D031 的 G1 terminal confirm workline
> 被取代：无
> 依据：验证 V060 + T024 commit `323c43bc8464e39b299ff405dbd884576d544bda`
> + 两路独立审查 `audit_t023_gate/audit_t023_science`
> 触发原话：无（技术推导；包装偏好见 `voice.md` 2026-07-24 原话）

### 决策

1. 不接受执行者自报的 `G1_FORMAL_CONFIRM_NO_GO`。任务书要求对 seed cluster
   重采样后重算 pooled confusion matrix；该口径的 balanced-accuracy 95% CI
   为约 `[0.885, 1.000]`，明确高于 Gate6 的 `0.5` 下限。执行器实际做的是
   `(cell,seed)` pair bootstrap；随后人工把单类 seed 的缺失 recall 记为 0，
   得到的 `0.50` 也不是冻结 estimand。
2. 同时不接受执行器原始 `G1_FORMAL_RECOMMENDATION_READY`。Phase A 的检索、
   引用链与 D1 read-note 收据未进入可提交证据闭包，`g1-step1-candidate-map.md`
   不存在；因此四判据与 `0 HIGH collision` 不能独立复核。
3. D4 recent comparator 不是任务要求的 likelihood-gated tap-update receiver。
   当前实现直接返回 post-CMA `z`，140/140 行与 CMA bit-identical；它是恒等
   占位符，不能支撑 target-comparator Gate4/Gate7。
4. T024 Phase B 只接收为 `NONBINDING_DIAGNOSTIC`。其余六门和 G1 的局部机制
   信号可回收：collapse stratum 相对 tuned CMA `−0.5598`，
   CI 约 `[-0.695,-0.406]`，help/hurt=`12/0`；healthy worst=`0`；
   G1−M4=`−0.03546`，CI 约 `[-0.0466,-0.0243]`。
5. binding disposition 改为
   `G1_GROUNDWORK_EVIDENCE_INCOMPLETE / PHASE_B_NONBINDING_DIAGNOSTIC`。
   按 D031/T024 的 one-shot 边界，不给第二个 G1 repair、补收据包或重实验。
6. 当前无 active scientific carrier。下一步不再 remap、修 evaluator 或开新
   候选；优先向用户提交一次最小设计确认：是否把 G1 现有证据整理为
   `NONBINDING_LOCAL_PACKAGING_BOUNDARY` 的毕业方法备选材料。

### 理由

T024 的失败不是“方法没有判别力”，而是 formal evidence closure 与 comparator
identity 失效。继续修会违反一次性退出边界；把它写成科学 No-Go 又会抹掉已经
重复出现的 receiver-visible 安全门控信号。最诚实且符合 mission 的处理，是停止
实验晋级，同时把算法动作、局部收益、适用边界和证据债分开包装，供毕业论文
择优使用，而不是再启动一轮零载体分析。

### 排除的替代方案

- 不按错误 `0.50` 维持 Gate6 No-Go；
- 不用 pair bootstrap 或事后改阈值“救活” formal Go；
- 不把恒等 D4 当直接竞品；
- 不补第二个 G1 Groundwork/实验包；
- 不在 0 READY 候选池上再做一轮纯 remap。

### 影响范围

- foreground 递增到 epoch55 / CP023；
- G1 formal workline 关闭，active scientific carrier 归零；
- G1 保留为 local diagnostic method signal，包装动作需用户确认；
- Step 5/Contract/Execute、论文正式声称与新实验继续禁止。

### 来源

T024；step-024 worker log；`prefix-receipt.csv`、`raw-rows.csv`、
`result.json`；T024 §A4/B1/B4；V060；D031/D040。

---

## D033: 接收 T025 为有边界内部方法材料，下一步直接产出论文小节与正式图

> status: active
> date: 2026-07-29
> 取代：D032 的“包装待决/待执行”状态
> 被取代：无
> 依据：T025 commit `5e355c6738ecefe831ddc0530a356f988cf7473b`
> + `g1-safe-gated-normalization-package.md`
> + `step-025-g1-bounded-thesis-packaging.md`
> 触发原话：无（T025 执行回执；包装偏好见 `voice.md` 2026-07-24、2026-07-29）

### 决策

1. 接收 T025 的 `PACKAGING_BOUNDARY`。G1 现已形成可追溯的内部方法包，包含
   算法、局部正向证据、论文叙事、图表计划、不可声称项与 provenance。
2. 科学上限不变：仍为
   `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`，不构成 formal Go、直接竞品胜利、
   新颖性闭合或 active scientific carrier。
3. 当前包是写作源材料，不直接标“论文可粘贴”。主控复核发现需在对外版本修正：
   “已知结构”不得暗示已知发送符号；“逐比特恒等”改为逐样本恒等；“零代价”
   限定为零后缀变换扰动；always-on 退化只写当前切片观测；`−0.5598`
   必须表述为 collapse 条件子集的 ΔPI-SER，而非“恢复后的错误率”。
4. 不把这些措辞修正再做成一个纯审计/纯润色包。下一包 T026 必须把现有方法包
   直接转成一个模块化论文小节、一个可编辑方法流程图和一张由 raw 重算的分层
   结果图；不修改现行 thesis framework，不暗示 G1 已成为论文主线。
5. T026 不新增科学证据，`mission_method_delta=NONE`；其价值是把已接收的
   `PACKAGING_BOUNDARY` 物化为可选的 `WRITING_MATERIAL`。

### 理由

T025 已完成“能不能包”的回答，继续打磨同一内部方法卡只会产生治理/文字循环；
直接制作论文小节与正式图，才把现有正向信号转成用户真正可用的毕业材料。由于
当前无 active carrier、第三个 CB1 z-only factory 被禁止，立刻再做同测试床方法
搜索的期望价值低于先把首个正向包装落实成可复用论文资产。

### 排除的替代方案

- 不把 T025 升为 formal method 或 active thesis spine；
- 不开第二个 G1 科学 repair、补实验、补文献闭包或实现直接竞品；
- 不只做措辞清单或再写一份包装评价；
- 不直接改 `thesis-framework.md`，避免未经用户确认改变论文结构；
- 不在本包后立即启动第三个 CB1 z-only factory。

### 影响范围

- foreground 递增到 epoch57 / CP024；
- T025 状态改为 accepted internal packaging source；
- T026 仅获 `THESIS_ARTIFACT_PRODUCTION` 授权；
- formal science disposition、D041 和无 active carrier 状态不变。

### 来源

T025 package/worker log；V060；D032/D041；research-direction-lab
`method-production.md`、`thesis-harvest.md`；external-output 出门审查。

## D034: 接收 T026 写作材料并暂停 T027 完成长程协议最小修订

> status: active
> date: 2026-07-29
> 取代：无
> 被取代：无
> 依据：调研: R009 + 验证: step-026 worker-log 双 reviewer + 用户原话: voice.md 2026-07-29

### 决策

接收 T026 为 `artifact_delta=WRITING_MATERIAL / mission_method_delta=NONE`，追加 CP025。G1 仍为 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`，不是 formal method 或 active carrier。

在派 T027 前，授权依 system D019 完成 RDL Skill 最小修订、live current snapshot 压缩和独立终验。终验后下一轮专门验证 `METHOD_SIGNAL → PROMOTION_READY/active carrier` 的端到端转化，不以包装或写作材料替代成功。

### 理由

T026 已把有边界 G1 包变成可复用小节和两张图，完成当前科学上限内的写作物化；R009 同时证明旧阶段 17/17 无方法增量、后段 signal→formal 转化仍为 0/2。继续直接派科学包会在未修复动作路由前重复旧问题。

### 排除的替代方案

- 不继续修 G1 科学线或把 T026 升成主方法；
- 不立即派 T027 新实验；
- 不新增完整 controller、固定批次门或每包恢复表；
- 不删除 mission-log、D/V、worker-log 或历史科学证据。

### 影响范围

foreground checkpoint 更新到 CP025；当前 allowed action 暂收敛为 Skill/current-view 修订与验证；R009 成为本阶段效果审计。既有 formal owners、thesis framework 和 protected history 不变。

### 来源

T026、step-026 worker-log、R009、system D019、用户 2026-07-29 授权。

---

## D035: 撤回频域/子带族 T027 入口，method-production 补入口四门，原位重写为逐符号/更新粒度族

> status: active
> date: 2026-07-29
> 取代：无（不取代任何科学决策；只取代 S003 选定的"T027=频域/子带族"入口授权，并把
> 入口改为唯一四门全过的替代项。T026/CP025、D019/D034 协议修订、所有 formal owner
> 与 protected history 不变）
> 被取代：无
> 依据：调研: 无 + 验证: V061 + 源码 file:line（见下）+ 用户原话: voice.md 2026-07-29

### 决策

1. 撤回 S003 选定的 **频域/子带均衡族** 作为 sprint-003 入口。该族 problem-bearing testbed
   preflight **门1 失败**：`projects/simulation/common/_dual_pol_channel.py:127-132` 的信道
   只有逐符号 GG 幅度 `h`、SOP 旋转 `theta`、AWGN，**无色散/多径/FIR/频率选择性**——频域/子带
   均衡对 memoryless、flat 信道退化为恒等/标量，**无可作用的物理自由度**。该族 comparator 也
   未冻结为真实、传统、同信息对象（原 T027 只留给 executor 冻结）。
2. method-production.md 补 **入口 problem-bearing testbed preflight 四门**（物理自由度存在 /
   基线失败与作用点一致 / 命名传统同信息可独立调谐 comparator / 每门 file:line），并明确禁
   "未测族 / REOPENED / testbed 曾产 signal"放行；另厘清 **shared anchor vs. identity parity**：
   后者只保护继承基线的比较连续性，**不禁止跑不同的传统算法**（把更细更新粒度选作传统
   comparator 是合法 re-adjudication，不是重开关闭轴、不是 identity 违例）。
3. T027 **原位重写**（不新建 T028，以保血缘）为唯一四门全过的替代入口 =
   **逐符号/更新粒度均衡族**：
   - 门1：`_cma.py:100-166` 的块末更新（block_size=64 内向量化滤波、块末平均梯度更新）是真旋钮；
   - 门2：sprint-001 `synthesis.v1.md` §4（L97-130）把 collapse 诊为"块末更新几何 + 信道时间
     变化"的结构性吸引子，§8（L176-179）把冻结块末协议列为"疑似瓶颈"、逐符号变体列为"最有
     信息的下一杠杆"——与基线失败点精确重合；
   - 门3：逐符号 stochastic-gradient CMA 是 Godard 1980 原始传统形式，同任务（同一 z-stream
     盲均衡）、同信息（receiver-visible）、可独立调谐；
   - 门4：每门均有 file:line。
4. task-control 同步修正：`control_epoch 59→60`、`action_class=METHOD_FACTORY_TASK_PREPARATION`
   与正文一致（正文显式声明"准备、待中转、本轮不跑"）；`validate_task_control.py` PASS。
5. 频域/子带族作 **rejected task brief** 保留在 T027 §3.1，不运行、不删除；仅在信道源码被升级
   到含色散/多径/频率选择性后才可能重审。`FREQUENCY_DOMAIN_SUBBAND_FAMILY` 加入
   `forbidden_actions`。
6. **无**科学实验、无方法构造、无 carrier 变更、无 protected history / formal owner 改动。
   CP026 记为入口纠偏治理包（`mission_method_delta=NONE`，不计 no-method streak，因非科学包）。

### 理由

继续按原 T027 派频域族 sprint，会在一个**物理自由度不存在的切片**上构造方法——频域处理对
当前 memoryless flat 信道退化为恒等/标量，任何"signal"都不可信。而逐符号/更新粒度族：物理
旋钮真实存在（代码即块末更新）、与已诊断的 collapse 机制（块末更新几何）精确重合、且有
Godard 1980 这一无可争议的传统同信息 comparator。S003 当初以"未测第六族 + portfolio REOPENED"
选频域族，正是新补的入口门要拦下的"未测族放行"。identity parity 的顾虑（S003 表 B）也需纠正：
它保护的是继承基线比较连续性，不是禁止跑不同传统算法。

### 排除的替代方案

- 不删原 T027、不建 T028：前者丢血缘、后者增噪音；原位重写 + §3.1 rejected 理由最干净。
- 不放宽门去"硬跑"频域族：物理自由度不存在是 P0，靠 executor 也无解。
- 不把逐符号族标为"已 Go"：仍只是诊断入口，是否产 signal 由 sprint 决定，claim ceiling
  `DIAGNOSTIC_*`。
- 不做广泛 portfolio remap：本轮边界是最小入口纠偏 + 入口门，不重排其它候选。
- 不改 controller/checklist 系统：method-production 只补入口门一段，不扩。

### 影响范围

- foreground `active_lane` → `SPRINT003_DISPATCH_READY_ENTRY_REDIRECTED`；authority → D035；
  `control_epoch` 保持 60；CP025 不变（CP026 为治理行，不进 mission science streak）。
- `method-production.md` 增入口四门 + shared-anchor/identity-parity 厘清（最小补丁）。
- T027 重写为逐符号/更新粒度族；task-control PASS。
- 无 formal owner / protected history / thesis framework 改动；无实验。

### 来源

S003、原 T027、`_dual_pol_channel.py:127-132`、`_cma.py:100-166`、sprint-001
`synthesis.v1.md` §4/§8、method-production.md、baseline-adjudication.md、V061、
用户 2026-07-29 中转指令（voice.md 2026-07-29）。

---

## D036: 最终纠偏 + 接收 sprint-003（NO_DIAGNOSTIC_SIGNAL）：纠正门2 证据等级、冻结 Godard-with-z comparator、action_class 改为 PREFORMAL_METHOD_FACTORY、新增 PROBLEM_RESOLVED 终态

> status: active
> date: 2026-07-29
> 取代：D035 的 T027 授权条款（门2 证据表述、comparator 身份未冻结、action_class=
> METHOD_FACTORY_TASK_PREPARATION 掩盖实验、三选一终态集）；不改 D035 的频域族撤回结论
> 与 protected history / formal owner
> 被取代：D035 的"门2 PASS 因 sprint-001 诊为结构性吸引子"与"comparator 留 executor 冻结"表述
> 依据：调研: 无 + 验证: V062 + 源码 file:line（见下）+ 用户原话: voice.md 2026-07-29

### 决策

本轮（用户中转指令）一次端到端完成"最终纠偏 → 科学执行 → 独立验证 → 主控接收"，
**无中间停顿**。四项确定性纠偏 + 接收 sprint-003 终态 `NO_DIAGNOSTIC_SIGNAL`。

#### A. 四项最终纠偏（修正 D035/T027/V061 的证据等级与授权语义）

1. **门2 证据等级纠正**：sprint-001 §4/§8 把"块末更新几何是结构性吸引子原因"写成已确认
   机制——该归因已在 CP018/D026/**V052 被拒收**（`REJECTED_SCIENCE=
   STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO`，理由：未做 basin/state-space 扫描、
   构造与既有候选高度重合）。正确表述：**块末更新是 source-backed、值得验证的疑似作用点**
   （`_cma.py:100-166` 块末更新是真旋钮；sprint-001 §4/§8 把它列为"疑似瓶颈"），**不是已确认
   因果机制**。T027 正是检验该疑似作用点因果性的诊断 sprint。已改正 T027 §0/§1/§1.1/§3，
   并在 method-production.md 补"Gate-2 evidence grade"段。
2. **冻结 comparator 身份**：传统 comparator = **tuned per-symbol standard CMA，canonical
   Godard-with-z 梯度 `Δw ∝ (R²−|z|²)·z·r*`**，provenance 指向 `cb1_cell_runner.py:124-129`
   （`(eX*zx_blk)[:,None]*conj(rX_blk)`，含 z 因子）。**禁用** `common/_cma.py` 的
   `CMAEqualizer2x2` 冒充 comparator——它是 **scalar-error** 梯度（`_cma.py:161-166`，缺 z，
   `cb1_cell_runner.py:20-30` docstring 已明示无法过 standard-CMA identity gate），只能证明
   block_size 是真旋钮。comparator 的 μ **在 dev 单独调谐**。已改正 T027 §0/§2.3。
3. **action_class 纠正**：D035/T027 的 `action_class=METHOD_FACTORY_TASK_PREPARATION` 把实际
   要跑的实验掩盖成"准备"。改为 `PREFORMAL_METHOD_FACTORY`（foreground 显式允许，control_epoch
   60→61），正文显式声明"授权仅覆盖本次 bounded 诊断 sprint，不授权 formal MVE/Step 5/论文
   claim/protected owner 修改"。`validate_task_control.py` PASS（epoch 61 / CP025）。已改正
   topic-index control 块与 T027 task-control 块。
4. **新增传统 comparator 裁决终态**：若 tuned per-symbol CMA 已消除 block-64 collapse 且新构造
   没稳定超过它，必须判 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`（**不是 METHOD_SIGNAL、
   不形成 active carrier**）。补 `EXECUTION_INVALID`（合同违反终态）。method-production.md 终态集
   从 3 个扩到 5 个（+ PROBLEM_RESOLVED + EXECUTION_INVALID）。已改正 T027 §2.4。

#### B. 接收 sprint-003 终态 `NO_DIAGNOSTIC_SIGNAL`（独立 verifier PASS）

executor 在 CB1 16QAM 共享 anchor 上构造 4 个更新粒度构造（block-64 μ=0.03 anchor、
tuned per-symbol Godard-with-z comparator μ=0.001、block-8 μ=0.003、block-16、
sliding-window recursive），dev 冻结后跑 fresh held-out（7 cells × 20 test seeds = 140 paired
realizations）。**结果**：
- inherited block-64 anchor（μ=0.03）seed-cluster mean PI-SER = **0.31431**；
- tuned per-symbol Godard-with-z comparator（μ=0.001）= **0.29685**（vs anchor Δ=−0.01747，
  CI [−0.0452,−0.0001]，11 help/9 hurt）；
- 最佳新候选 block-8（μ=0.003）= 0.29392，vs comparator Δ=**−0.00293**，CI [−0.0112,+0.0056]
  （跨 0），help/hurt/tie = 13/7/0 —— **未过 MDE=−0.005 且 CI 跨 0**，无 signal；
- comparator **未消除 collapse**：7 cells 中只 1 个（snr15-fg1000-long：0.158→0.090）降到
  PI-SER<0.1，其余 6 cells 仍 collapse。
- 消融：候选场在 64× 有效更新预算跨度（block64=0.0156 → per-symbol=1.0 updates/sym）上**平坦**，
  既非"更多更新次数"也非"更新粒度"产生可分离优势 → 无赢家，`NO_DIAGNOSTIC_SIGNAL` 正确。

**独立 verifier（V062）PASS**：Godard-with-z 公式逐方法核（`methods.py:141-148/228-234/313-322`
均含 z 因子，无 scalar-error 冒充）；block-64/per-symbol/candidate 信息公平（同 paired
realization、同 eval window、comparator μ dev-only 调谐）；dev/test 隔离 + fresh seeds（禁用
71–80 零命中）；raw→aggregate 独立重算全部吻合（<1e-4）；机制归因不越界（疑似作用点未被当
已确认机制）；terminal verdict `NO_DIAGNOSTIC_SIGNAL` 为五选一中唯一正确项。3 项微小非承重
wording/label 瑕疵（4-category label 用单 seed、§4 "2/3" 应为 "some"、§5 healthy cluster 空）
不改 verdict、不需修复。

### 理由

四项纠偏是科学诚实性要求：把被拒收的归因当已确认机制（门2）、用错误梯度身份冒充 canonical
comparator、用 preparation 掩盖实际实验，任一都会让 sprint 的 signal/NO_SIGNAL 判据不可信。
冻结 Godard-with-z comparator + 新增 PROBLEM_RESOLVED 终态后，sprint 才能真正裁决"块末更新是
否是 collapse 成因、传统 per-symbol 更新是否已解决"——裁决结果是：comparator 略优于 anchor
但未消除 collapse，且无新构造稳定超过它 → `NO_DIAGNOSTIC_SIGNAL`，疑似作用点（块末更新）的
因果性**未被本 sprint 确认**（既未确认是成因，也未确认不是；collapse 在所有更新粒度下都持续）。

### 排除的替代方案

- 不判 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`：comparator 只在 1/7 cell 消除 collapse，
  其余 6/7 仍 collapse，不满足"已消除问题"判据（V062 独立复核）。
- 不判 `DIAGNOSTIC_METHOD_SIGNAL`：最佳候选 Δ=−0.00293 未过 MDE 且 CI 跨 0，无赢家。
- 不做包内修复 verifier 发现的 3 项瑕疵：均非承重、不改 verdict/gate；verifier 明确"不需重跑"。
- 不升级战略 gate：sprint 在合法 anchor 下诚实产出诊断结果，问题未被传统 comparator 解决、
  也无新 signal，属合法 `NO_DIAGNOSTIC_SIGNAL` 终态，按 method-factory 纪律关闭本轴。

### 影响范围

- foreground `active_lane` → `SPRINT003_PREFORMAL_FACTORY_BOUND`；authority → D036；
  `control_epoch` 60→61；CP025 不变（CP027 为本 sprint 接收行）。
- method-production.md 终态集 3→5，补 Gate-2 evidence grade + comparator gradient identity 两段。
- T027 task-control epoch→61、action_class→PREFORMAL_METHOD_FACTORY；T027 正文改 §0/§1/§1.1/§2.2/
  §2.3/§2.4/§3/§4。
- **无 formal owner / protected history / thesis framework 改动**；无 active carrier 变更；
  `NO_DIAGNOSTIC_SIGNAL` 不形成 METHOD_SIGNAL、不晋级、不写论文。
- CB1 更新粒度均衡族轴关闭（method-factory 纪律：无 signal 即退出，不强行收尾）。

### 触发原话

voice.md 2026-07-29（用户中转纠偏 + 端到端执行指令）。

### 来源

用户 2026-07-29 中转指令（voice.md 2026-07-29）；sprint-003 产物（commit `689151c`，
`preformal-method-factory-sprint-003/`）；V062 独立验收；`cb1_cell_runner.py:20-30/124-129`、
`_cma.py:100-166/161-166`；V052（`REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO`）；
sprint-001 `synthesis.v1.md` §4/§8；method-production.md、baseline-adjudication.md、
evidence-and-claims.md。

---

## D037: CB1 轮换后下一入口六门评估——三候选全不过门，输出 STRATEGIC_GATE（不制造第四弱候选）

> status: active
> date: 2026-07-30
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-07-30 + 调研: 既有资产（portfolio/current.yaml、candidate-universe.yaml、candidate-map.v2.yaml、candidate-coverage-audit.v3.yaml）+ 源码 file:line（见下各门）+ 验证: V063

### 决策

接 CP027（CB1 更新粒度均衡族轴 `NO_DIAGNOSTIC_SIGNAL` 关闭）后，主控在 CB1 collapse 家族之外评估
**三个**候选入口（A: 传统 CPR VV 在 adversarial_sourced|snr14 切片；B: NDA-ML 跨问题扩展；
C: U24 high-SOP non-swap BER failure detection）。**三候选无一逐项过六门**。遵守用户"不得制造第四
个弱候选"的纪律，**输出 `STRATEGIC_GATE`**，不开 sprint、不派 executor/verifier、不建 T028。
`active_lane` 仍为 `SPRINT003_PREFORMAL_FACTORY_BOUND`，仍 0 active carrier。

#### 候选 A — 传统 CPR（VV Nw=128）在 adversarial_sourced|snr14 切片

- **门1（M-C-A）FAIL**：M=VV Nw=128（传统 comparator）、C=adversarial_sourced|snr14。synthesis 记
  两类事实：①VV 对 oracle O 留 ~0.6dB headroom（`high-order-cpr-combination/synthesis.md:56-68`，
  CI upper 1.7、lower <0，宽且点值小）——**TL-32/FR-25 明确 oracle 上界只做 Kill 工具不当 Go 判据**；
  ②P1/P2/P3 组合方法相对 VV 差 9–20dB、0/10 paired wins（`synthesis.md:75-92`），这是**已记录的
  机制失败**——但属**已被拒收的 B10/B12 组合实例**（DD 反馈跟踪 AWGN 判决误差、MAP 过平滑；
  master-state.md:149 `SCIENCE_VERDICT_REJECTED`），不是可合法轮换的开放轴。**关键**：synthesis
  `:104-128` 自述"在 10 kHz 线宽范围内……设计用于光纤的盲/导频相位估计器在数值上收敛于 VV，没有
  真正的机制优势"——即 VV（传统 comparator）本身**没有观察到可被不同传统 CPR 改善的具体机制失败**，
  只有 oracle-gap；且先验上"不同窗口 VV 也很可能在 10 kHz 退化成 VV"（与 sprint-003 更新粒度候选场
  在 comparator 周围平坦同构）。组合方法的失败不能重新洗成"VV 有待改善的失败"（用户门6）。
- **门2 PASS**：相位跟踪窗口/块结构 DOF 真实存在（`channel_helpers.py:97-108` 注入 CFO+Wiener；
  `baselines.py:31-45` arm_vv/arm_bps 有可调窗口）。
- **门3 PASS**：VV Nw=128 是 frozen 传统 comparator（`run_all.py:274-305` validation 选出）。
- **门4 PASS**：`high-order-cpr-combination/` runner+contract+source-closure 已 frozen，7 语义门 PASS。
- **门5 PASS**：CPR 是独立子问题，primary/fallback 可包装（block-adaptive CPR / 复杂度-性能折中）。
- **门6 FAIL-on-foundation-rejection**：master-state.md:149 记 B10/B12 combination verdict
  `SCIENCE_VERDICT_REJECTED / UNRESOLVED`（"source/channel/statistics 多重失效"）；candidate-coverage-
  audit.v3.yaml:164-165 明示 U10(CPR) "existing evidence is SOP/polarization/CMA BER failure, **not
  CPR cycle-slip or lock-loss**"。**rejected 证据不得重新洗成 PASS**（用户门6 硬约束）。
- **结论**：A 不开 sprint（属"只因未测/REOPENED/看起来新而放行"的禁止情形，且 verdict 被拒收）。

#### 候选 B — NDA-ML 跨问题扩展到 CPR 切片

- **门1 FAIL**：NDA-ML 在 AWGN +1.351dB / 弱湍 +1.53 / 中湍 +1.71（`single-carrier-nda-ml/_mve_results.json:67-130`）——它是**已完成的赢家**，不是失败的传统 M；DA-ML 是被它击败的 comparator。
  这是已封闭 Step 4a 工作（`SC-NDA-ML-MVE-SPEC.md` GW Step 4a 维度 D），不是新 problem-bearing 入口。
- **结论**：B 不构成新入口（已完成工作，非"传统方法失败"）。

#### 候选 C — U24 high-SOP non-swap BER failure detection

- **门1 部分**：U24 是 candidate-map.v2 唯一 `problem_truth:5` 候选（score 4.20，`BATCH_1_FAMILY`），
  rationale："foundation has authentic high-SOP non-swap BER failures while historical single-statistic
  threshold detector failed"（`candidate-universe.yaml:167`、`candidate-map.v2.yaml:41`）。但 D047
  明确"`1e-5` 的 fixed=PI，说明当前失败不是 X/Y 标签 swap；把它当 lock-swap 会混淆问题定义"——
  即**记录的失败是 BER tracking failure，不是 swap**（`decisions.md` D047）。
- **门4（runnable testbed）FAIL**：检测线已在 **D051 关闭**——"control `4e-6` 的新 seed47/48 已出现
  oracle events，control-only 阈值前提失效"（无干净 paired realization）；且"non-swap BER"标签需
  **TX-truth oracle assignment**（`prompt013_swap_quality_q1.py` 用 PI-BER oracle），属用户禁止的
  "oracle/genie 才能构造的动作"。evidence_gap = "event count and cross-domain validation"（候选未配
  备 testbed）。SOP-tracking 出路（sparse pilot）已在 portfolio 终止（`SPARSE_PILOT_SEMIBLID =
  RETURNED_WITH_PILOT_JONES_SCOPED_AXIS_KILLED`，`current.yaml:162-172`），model-based tracker F1
  RETRACTED（privileged CSI genie gap，`current.yaml:144-161`）。
- **结论**：C 的 detection 轴被 D051 阻塞且需 oracle 构造，禁止。

### 综合判定：`STRATEGIC_GATE`

三候选无一过门。**缺的是 problem-bearing 物理问题**（不是 testbed/comparator 基础设施）：portfolio
中 CB1 collapse 家族以外的开放候选，要么只有 oracle-gap 无传统方法失败（A），要么是已完成赢家非新
入口（B），要么标签本身需 oracle 构造且检测线已被 D051 关闭（C）。channel 源（`_dual_pol_channel.py`）
只有 GG 幅度 + 实 SOP 旋转 + AWGN，无多径/色散/FIR/频率选择性，物理自由度本身窄（FR-23 起点"找
baseline 指出其具体不足"在这条 channel 上，可作用的传统方法旋钮有限）。

#### 候选扫描完整性（problem_truth ≥ 4 的候选，V063 独立核实）

`candidate-map.v2.yaml` ranked_shortlist 中 problem_truth ≥ 4 的候选共四个：U24（pt5，=候选 C）、
U10（pt4，=候选 A 的 CPR 族）、**U05（pt4，`HOLD_FOR_COMPETITOR_CLOSURE`，score 3.65）**、
U23（pt4，`MERGE_WITH_U24_DIAGNOSTICS`，已并入 U24）。U05（GG/Jones/link-state 估计）是唯一未在
A/B/C 单列的 pt4 候选——它被 `candidate-map.v2.yaml:53` 标记 `HOLD_FOR_COMPETITOR_CLOSURE`、`:104,109`
标 observation-only（D047-D054）+ direct-competitor/crossref 未解（D056），**属 hold 状态不构成
Go-eligible 入口**，且其 SOP-tracking 实现出路已由 SPARSE_PILOT_SEMIBLIND（KILLED）和 F1 model-based
tracker（RETRACTED, privileged CSI）阻断。U05 不开为独立 sprint（hold + 出路已阻塞 = 无 runnable
problem-bearing 入口），但此处显式登记以补全候选扫描完整性。

### 综合判定：`STRATEGIC_GATE`

三候选（A/B/C）无一过门，U05 hold 且出路阻塞。**缺的是 problem-bearing 物理问题**（不是 testbed/
comparator 基础设施）：portfolio 中 CB1 collapse 家族以外的开放候选，要么只有 oracle-gap 无传统
方法失败（A），要么是已完成赢家非新入口（B），要么标签本身需 oracle 构造且检测线已被 D051 关闭
（C），要么 hold 状态出路已阻塞（U05）。channel 源（`_dual_pol_channel.py`）只有 GG 幅度 + 实 SOP
旋转 + AWGN，无多径/色散/FIR/频率选择性，物理自由度本身窄（FR-23 起点"找 baseline 指出其具体不足"
在这条 channel 上，可作用的传统方法旋钮有限）。

按 RDL 升级规则与用户"不得制造第四弱候选"指令，**不开 sprint、不建 T028、不修 protected history/
formal owner/Skill**。下一合法动作交用户：是 (1) 升级 channel 模型引入新物理自由度（complex
Jones/PMD/PDL/色散，需授权 ~1 天基础设施，会改变所有方法的竞争格局——FR-18），还是 (2) 论文范围
决策（把已有 G1 bounded package + 局部负面 harvest 作毕业材料，或开新子问题），还是 (3) 接受当前
RDL live-test 在 0 active carrier 下达成"协议稳定 + 可靠负面 + 1 bounded asset"的结论、收尾审计。

### 排除的替代方案

- 不制造第四个弱候选（用户硬约束）。
- 不把 CPR 0.6dB oracle-gap 重新包装成 Go（违反 TL-32/FR-25 + 用户"rejected/invalidated/privileged
  证据不得重新洗成 PASS"）。
- 不重开 D051 已关闭的 non-swap detection 线（control seeds 有 oracle events，无干净 paired
  realization；标签需 TX-truth oracle）。
- 不重开 CB1 collapse-recovery 任何变体（用户绑定结论 + D036 forbidden axis）。
- 不把 STRATEGIC_GATE 当成方法进度（mission_method_delta 仍 `NONE`；这是可靠"无合法 problem-bearing
  入口"的诚实判定，不是方法产出）。

### 范围确认

本轮在 scope boundary 内：无科学实验、无新 T、无 protected owner/formal 改动、无 push、无新
infrastructure；仅做入口六门评估 + STRATEGIC_GATE 判定 + 治理记录。无 scope change。

### 来源

用户 2026-07-30 中转指令（voice.md 2026-07-30）；portfolio/current.yaml:121-161（closed axes +
open candidates）；candidate-universe.yaml:163-167 + candidate-map.v2.yaml:41-65 + candidate-
coverage-audit.v3.yaml:163-165；`high-order-cpr-combination/synthesis.md:56-68,75-92,104-128` +
`baselines.py:31-45` + `channel_helpers.py:97-108` + `run_all.py:274-305`；`single-carrier-nda-ml/
_mve_results.json` + `SC-NDA-ML-MVE-SPEC.md:19`；foundation decisions D047/D048-D051
（`.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D047/D051；本 live topic 经 anchor
`foundation.decisions` 导入）；`_dual_pol_channel.py:104-132`；master-state.md:149；method-production.md
（入口四门）、baseline-adjudication.md、evidence-and-claims.md、TL-32/FR-25。V063 独立核实候选评估
与既有证据一致（claim 1 已据 V063 纠正表述、claim 6 已补 U05 扫描）。

---

## D038: 用户选定 CP028 三选项 (1)：授权一次端到端 channel 物理自由度扩展大包

> status: active
> date: 2026-07-30
> 取代：D037 的"等待用户决策 / 禁止 PREFORMAL_METHOD_FACTORY + GENERAL_INFRASTRUCTURE_BUILD"部分（D037 的 STRATEGIC_GATE 事实判定与 CB1 forbidden 轴保留）
> 被取代：无
> 依据：用户原话: voice.md 2026-07-30（方案1授权）；CP028 STRATEGIC_GATE（D037/V063）；method-production.md（入口四门+终态五选一）、baseline-adjudication.md、evidence-and-claims.md；`_dual_pol_channel.py:104-132`（当前物理自由度=GG幅度+实SOP旋转+AWGN）；FR-18（环境升级需分析对所有方法竞争格局的影响）；TL-26/27（参数溯源+物理量级核算）、TL-22（物理前提核查）、TL-32/FR-25（Go=赢传统baseline，oracle只做Kill）、FR-20（参数溯源）；code-quality.md（P4 只扩不改）+ SIM-ORG.md + sim-preflight（信道共享/参数溯源/元数据注入）；CB1 comparator provenance `cb1_cell_runner.py:124-129`（Godard-with-z，provenance 已核）
> 触发原话：`voice.md` 2026-07-30（用户授权方案1，端到端大包，不在选择入口或建设基础设施后停下来等待用户）

### 决策

1. 接收 CP028 `STRATEGIC_GATE` 已被用户以**选项 (1)** 解决：升级 channel 模型引入新物理自由度。
   - 解禁 `forbidden_actions` 中的 `PREFORMAL_METHOD_FACTORY` 与 `GENERAL_INFRASTRUCTURE_BUILD`，**仅限本 D038 端到端大包，一次性、有界**。
   - 其余 D037 forbidden 项全部保留：`CB1_COLLAPSE_RECOVERY_FAMILY`、`FREQUENCY_DOMAIN_SUBBAND_FAMILY`、`CLOSED_AXIS_REOPEN`、`POST_STEP4A_ADVANCE`、`PROTECTED_OWNER_MODIFY`、`PROTECTED_HISTORY_EDIT`、`PAPER_CLAIM`、`PRIVATE_FULLTEXT_ACQUISITION`、`ABSTRACT_AS_FULLTEXT` 仍禁止。
2. **本轮绝不开 CB1 collapse-recovery 任何变体**（block-size、μ、更新调度、频域/子带、z-only、初始化、cost 变体——用户绑定结论）。
3. 大包为严格的**串行四段链**，前一段不过则后一段禁止开跑；段间不在选择入口或建基础设施处停下等用户：
   - **段A 物理入口筛选**：由独立文献/物理 subagent，从以下候选最多比三个——(a) complex time-varying Jones / differential phase coupling；(b) physically justified PDL；(c) PMD、色散或其他有跨符号记忆的 coherent dual-pol FSO impairment。不得假定任何现象在 LEO/星地 FSO 成立（fiber 结果不可直接移植）。每个候选过**六门**：①与当前 coherent dual-pol 星地 FSO 范围直接相关（file:line）②≥2 篇可访问 primary/fulltext 支持其存在/模型/参数范围③真实参数量级核算（当前 symbol rate/frame length/处理窗口内可见，差≥3 数量级直接 Kill）④明确传统/同任务/同信息/可独立调谐 conventional comparator⑤能写成具体 M-C-A（不是"加复杂信道看看有没有增益"）⑥预计约一天内可隔离实现+验证+小批诊断。**每门须给全文或源码 file:line**。oracle gap 不能当 Go 依据（TL-32/FR-25）。三个均失败 → 终态 `PHYSICS_BACKED_TESTBED_UNAVAILABLE`，建议转论文范围/新子问题，**不制造第四个 impairment**（与 D037"不制造第四弱候选"一致）。
   - **段B 只扩一个 channel 自由度**：若且仅若一个候选六门全过——只实现排名第一的单一 impairment；新模块/显式 mode 隔离，**旧 channel 默认路径 byte-identical**（守 P4 只扩不改：新 `common/_*.py` 文件 + `params.py` 新 Pydantic 参数类 FR-20 全溯源，默认 identity/off 退化恢复旧输出）；不为让方法有用而扩大参数；参数全部绑定文献范围；建理论预期（TL-20）+ 单位测试 + 极限退化测试 + seed 可复现 + 旧模型 regression（TL-13 信道共享）。独立 verifier 先确认模型公式/单位/时间尺度/实现一致。testbed 未过物理/身份验证，不得进方法实验。
   - **段C conventional baseline adjudication**：在新 testbed 先跑——原有 shared anchor + 一个任务匹配/receiver-visible/充分调谐的传统 comparator + 一个明显廉价扩展（如适用）；paired realization、dev 冻结、fresh held-out、raw rows、CI。只有记 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 才允许进 method factory；若传统 comparator 已解决，终态 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`，不包装成新方法。
   - **段D 条件式 method factory**：若问题仍存，同一对话立即由独立 executor 构造并运行 3–5 个机制不同的最小方法。每方法只用 deployable receiver-visible 信息；单独 dev 调谐、fresh held-out；与 tuned conventional comparator 比；raw rows、paired CI、help/hurt/tie、语义 smoke、消融、复杂度齐全。只有新候选稳定超过 comparator 且排除额外信息/调参预算/实现伪影，才判 `DIAGNOSTIC_METHOD_SIGNAL`；signal 同时给 primary + fallback packaging。
4. **独立验证与接收**：至少分离——物理模型/source verifier（段A/B）、实现与数值 verifier（段B/C/D）、主控最终科学裁决。允许一次包内确定性修复，不开第二个修复对话。
5. 关闭时一次统一更新 topic-index/mission-log/D/V/必要 owner，一次 commit；不 push。
6. 仍 0 active carrier 直到段D 出现 METHOD_SIGNAL 且过 promotion preflight（method-production.md）。oracle 上界只做 Kill 工具（段A⑥ / Step 4a 收尾），绝不当 Go 判据。

### 理由

CP028 的核心结论是"缺的是 problem-bearing 物理问题，不是 testbed/comparator 基础设施"——channel 源（`_dual_pol_channel.py`）只有 GG 幅度+实 SOP 旋转+AWGN，物理自由度本身窄。用户选项 (1) 直接针对这个根因：引入一个**物理可信、文献支撑、量级可见、有传统对手**的新 channel 自由度，让"找 baseline 指出其具体不足"（FR-23）这条链有可作用的对象。

用户明确要求端到端大包、不在选择入口或建基础设施后停下等用户（voice.md 2026-07-30），故本 D038 不把四段拆成多个 T，而是单对话内串行执行，各段门控（六门/物理身份/PROBLEM_SURVIVES/METHOD_SIGNAL）仍独立硬性。段A 的六门是用户授权的更严上游物理 DOF 筛选屏（用于**选 impairment**），独立于 method-production.md 的入口四门（用于**选 method**）——两者都适用、不冲突。

风险控制：①不假定 fiber 的 PMD/PDL/CD 在星地成立（TL-22 物理前提）→ 六门②强制 primary 全文与量级核算；②参数不为方法服务拍（TL-26）→ 段B 参数绑定文献；③oracle 不当 Go（TL-32）→ 段A⑥/D 明确；④旧路径 byte-identical（P4/TL-13）→ 段B 退化测试；⑤不制造第四弱候选/impairment → 段A 三候选失败即终止。

### 排除的替代方案

- 不开 CB1 collapse-recovery 任何变体（用户绑定结论 + D036/D037 forbidden axis）。本轮不是继续挖 CB1。
- 不选 CP028 选项 (2)（论文范围决策）或 (3)（收尾审计）——用户已选定 (1)。
- 不预设 impairment：complex Jones / PDL / PMD/CD 须段A 六门实筛，不凭标题联想（TL-30 跳步信号）。注意 complex Jones 与已 scoped-Kill 的 Pilot-Jones complex rescue（D066，cond≈1 静态）部分重叠，但**时变**复 Jones/differential phase（跨符号记忆）是不同问题，须段A 独立过门判其是否在星地成立、是否已被 D066 关闭。
- 不用 oracle gap 当 Go（TL-32/FR-25）；不把 abstract 当 fulltext（AGENTS.md）；不获取私有全文。
- 段A 三候选全失败时不强凑第四 impairment（用户"不制造第四"硬约束），直接 `PHYSICS_BACKED_TESTBED_UNAVAILABLE`。

### 影响范围

- live control 升 epoch 62→63 / CP028→CP029（暂记；段A 终态后再定 CP029 是否追加 method delta）；active_lane → `CHANNEL_PHYSICS_EXTENSION_DISPATCH`；authority → D038。
- 解禁 `PREFORMAL_METHOD_FACTORY` + `GENERAL_INFRASTRUCTURE_BUILD`（仅本 D038 大包）。
- 其余 forbidden 全部保留；protected owner/formal/Skill/thesis framework 不改、无 push。
- mission_method_delta 在段D 出现 METHOD_SIGNAL 前保持 `NONE`。
- 文档：topic-index control block 升级、voice.md 补 2026-07-30 方案1原话、mission-log 待段链完成后追加 CP029 行；decisions.md 本条；如段A 出 sprint 则对应 V###。

### 范围确认

本轮（治理记录）在 scope boundary 内：仅做 STRATEGIC_GATE 解决 + 控制面解禁 + 用户 voice 记录，无科学实验、无 protected owner/formal 改动、无 push、无新 infrastructure（段B 才允许）。无 scope change（用户选项 (1) 本就是 CP028 预登记的三选项之一，未扩大原始目标）。

### 来源

用户 2026-07-30 voice.md（方案1授权，端到端大包）；CP028/D037/V063；method-production/baseline-adjudication/evidence-and-claims；code-quality.md/SIM-ORG.md/sim-preflight；TL-20/22/26/27/30/32 + FR-18/20/23/25；`_dual_pol_channel.py:104-132`；`cb1_cell_runner.py:124-129`。

## D039: 用户授权 10-有效包探索 campaign（不因 0 READY 要求 thesis pivot）

> status: active
> date: 2026-07-30
> 取代：D038 的 "active_lane=PHYSICS_EXTENSION_TERMINATED_AWAITING_USER_DECISION / 下一合法动作交用户"（D038 的段A 物理判定 PHYSICS_BACKED_TESTBED_UNAVAILABLE 与 forbidden axis 保留）
> 被取代：无
> 依据：用户原话: voice.md 2026-07-30（campaign 授权："至少跑10大包？"）；CP029/D038 段A 终止事实；method-production.md（DIAGNOSTIC_METHOD_SIGNAL/METHOD_SIGNAL 需 fresh held-out 稳定超过 tuned comparator + 语义 smoke + 消融 + 复杂度）；baseline-adjudication.md（pre-method gate 四门 + PROBLEM_SURVIVES_CONVENTIONAL_BASELINE 才进 method factory + minimal baseline ladder）；evidence-and-claims.md（claim ceiling 最小等级 + semantic smoke before scale）；D037/D038 已关闭轴清单（CB1 collapse family、频域/子带族、NDA-ML 本体、G1 science repair、Pilot-Jones 小轴、PMD/PDL/Jones/CD 星地移植）；TL-30（不得换名重开已关闭轴）/TL-32/FR-25（Go=赢传统 baseline，oracle 只做 Kill 工具）/FR-23（问题=M 在 C 下因 A 失效，非空白）
> 触发原话：`voice.md` 2026-07-30（用户授权至少 10 个有效科学大包；setup/治理/任务准备/接口修复不计包数）

### 决策

1. 接收 CP029/D038 段A 的 `PHYSICS_BACKED_TESTBED_UNAVAILABLE` 已被用户以 **campaign 授权** 解决：在完成 **10 个有效科学大包**前，主控不再因为当前 portfolio 0 READY 而要求 thesis pivot（推翻 D038 末尾"交用户 (2)/(3)"的等待）。`PREFORMAL_METHOD_FACTORY` 永久解禁为本 campaign 服务（不再单大包绑定）；`GENERAL_INFRASTRUCTURE_BUILD` 仍按需、有界、独立验证。
2. **建立最轻量 rolling queue**（不新建复杂 controller/scheduler，符合 profile"反对未收口设计散落成控制器补丁"）。rolling queue 保存在 `topic-index.md` 的 control block（轻量计数器 + 候选列表），**允许滚动更新，不要求现在证明数学完备**。计数器：
   - `exploration_budget_valid_packages`: 10
   - `accepted_valid_packages`: 0（每接收一个有效科学包 +1）
   - `current_package`: P01
3. **有效包定义**：一个端到端跑完且产出 **terminal verdict**（method-production 终态集五选一：`DIAGNOSTIC_METHOD_SIGNAL` / `NO_DIAGNOSTIC_SIGNAL` / `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`(含 adapter) / `PROBLEM_ABSENT_UNDER_TESTED_CONDITION`(负面但端到端完成) / `BLOCKED_SHARED_TESTBED` / `EXECUTION_INVALID`）的科学大包计 1 个有效包。**不计包数**：setup、治理、任务准备、接口修复、纯复现无新子问题、入口筛 preflight（出 STRATEGIC_GATE 的入口评估也不计）。
4. **机制族纪律**：至少跨 **5 个机制族**；**同族最多连续 2 包**（第 3 包必须换族，除非前 2 包其一产生 METHOD_SIGNAL 正走 promotion）；**第 5 包做一次内部校准（审计是否偏、族覆盖是否足），但不停线**；**第 10 包才做 campaign-level pivot/continue 裁决**。
5. **禁止换名重开已关闭轴**（TL-30）：NDA-ML 本体（已完成赢家 `_mve_results.json` 全正增益）、G1 science repair（CP024 bounded asset 已结）、CB1 collapse family（CP027 `NO_DIAGNOSTIC_SIGNAL` + 用户绑定结论）、Pilot-Jones 已关闭小轴、PMD/PDL/Jones/CD 星地移植（D038 段A PHYSICS_BACKED_TESTBED_UNAVAILABLE）。**新子问题 = 找已有方法的新的失效条件/鲁棒性问题，不是复现旧结果当新方法**（FR-23）。
6. 每个 package 遵守 **problem-bearing probe → conventional adapter → 条件式 method factory** 的三阶段门控结构（method-production + baseline-adjudication）：Phase A problem-first（先证明问题存在，dev 前冻结"实质失效"判据，判据相对原方法声称规模制定）；Phase B 仅当问题成立才跑 conventional adapter（receiver-visible plug-in），adapter 已解决则 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` 不产生 signal；Phase C 仅当 adapter 后仍残余才构造 3–5 个机制不同最小候选。oracle/true-truth 只作 bound 不作部署输入或 Go 判据（TL-32/FR-25）。
7. 执行分离：科学实现由独立 executor；数值/信息边界由独立 verifier；主控负责最终接收与 claim ceiling。允许一次包内确定性修复，不另开 repair 包。完成一个 package 后一次统一更新 topic-index/mission-log/D/V/必要 owner。
8. 仍 0 active carrier 直到某 package 产出 `DIAGNOSTIC_METHOD_SIGNAL` 且过 promotion preflight（method-production.md）。claim ceiling 默认 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC` 直到晋升。

### 候选队列（rolling，允许更新）

> 不要求数学完备；随每个 package 关闭滚动补。当前已知机制族（≥5）：
> A. **CPR 选择器鲁棒性族**（P01：SNR 失配；可延伸：CV 统计量分布漂移、pilot 稀疏度失配、噪声非平稳）
> B. **同步/估计器交互族**（FOE 残差对 CPR 的级联、定时偏移对 selector）
> C. **湍流场景边界族**（饱和/闪烁、上/下行差异、多普勒谱形变）
> D. **调制/编码层族**（HD/SD-FEC 边界、APSK 环比失配、16APSK 旋转模糊）
> E. **信息/复杂度边界族**（窗口长度 vs 估计方差、低复杂度降级、量化位宽）
> 同族连续≤2 包由队列自然轮换保证（每接收 2 包同族后强制换族）。

### 理由

D038 段A 证明 channel 源物理自由度窄、fiber impairment 无星地物理起源——这是**物理 DOF 路径的穷尽**，不是"该领域无问题可做"。用户的 campaign 授权正解此：把"找 baseline 指出其具体不足"（FR-23）的对象从"造新 channel 物理自由度"转向"对**已完成方法**（DA-NDA 选择器，method.tex 已成稿、`ccisp_family1_selector_a_30seed.json` 已冻结 0.8–1.5 dB 增益）的**新失效条件/鲁棒性**做子问题探索"。这类问题：①有冻结 anchor（原方法结果可复现）；②有明确传统 comparator（原选择器自身 = conventional，plug-in estimator = conventional adapter）；③receiver-visible、不需 oracle 部署；④claim 规模相对原 0.8–1.5 dB 可定量。

profile（"务实可毕业远胜理论最优"+"多挑候选保留余地"+"深耕已有基础、候选族批量排跑"+"不早收敛"）全部支持：不追 SOTA、扩大候选池、从已有代码抽基点展开机制族、局部失败只作组合内事件自动轮换。轻量 rolling queue 而非 controller 符合"反对未收口设计散落成控制器补丁"。

### 排除的替代方案

- 不因 0 READY 立即 thesis pivot（用户明确授权 10 包预算）。
- 不重开 D037/D038 已关闭轴（TL-30）：不挖 CB1 collapse-recovery 变体、不移植 fiber PMD/PDL/Jones/CD、不重开 NDA-ML 本体（已完成赢家）、不重开 G1 science repair、不重开 Pilot-Jones 小轴。
- 不把复现旧 selector 结果当新方法（FR-23）：P01 必须注入**新的 SNR 失配**这一新失效条件，复现 anchor 只是 Phase A 基线。
- 不用 oracle/true-truth 当部署输入或 Go 判据（TL-32/FR-25）：P01 中 true SNR 只用于生成信号和离线评价。
- 不预建复杂 controller/scheduler（profile）。

### 影响范围

- live control 升 epoch 64→65 / CP029→CP030（P01 关闭时追加）；active_lane → `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D039。
- `topic-index.md` control block 新增 campaign 计数器与候选队列段；`voice.md` 补 2026-07-30 campaign 原话；`mission-log.md` 待 P01 关闭追加 CP030 行。
- protected owner/formal/Skill/thesis framework 不改、无 push。`PREFORMAL_METHOD_FACTORY` 从 forbidden 解禁为本 campaign 服务。
- 仍 0 active carrier；mission_method_delta 在某 package 出 `DIAGNOSTIC_METHOD_SIGNAL` 前保持 `NONE`。

### 范围确认

本轮（治理记录 + campaign 授权）在 scope boundary 内：用户授权 10 包预算是新的授权范围扩展，已记录为 scope change（见 topic-index 范围变更记录）。无科学实验、无 protected owner/formal 改动、无 push、无新 infrastructure。

## D040: P02 cand_rank 工作区确认 → PROBLEM_RESOLVED_BY_REGION_RETUNING（A 族达同族上限）

> status: active
> date: 2026-07-30
> 取代：无（P01 的"条件式子群体信号作 future-work seed"被本包 fresh confirmation 消解）
> 被取代：无
> 依据：D039 campaign 授权；method-production.md（PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR 终态集 + cheap-alternative 门控）；baseline-adjudication.md（minimal baseline ladder 第 3 级 = 一个直接针对观察失效的廉价常规扩展）；evidence-and-claims.md（semantic smoke + claim ceiling）；worker-log step-029；V066 独立验收 PASS；TL-32/FR-25（Go 与 Kill 判据分离）/FR-23（问题驱动非空白）
> 触发原话：用户 campaign 授权（voice.md 2026-07-30 "至少跑10大包？"）+ 本轮 P02 执行指令

### 决策

1. 接收 P02（T029）端到端结果，terminal verdict = **`PROBLEM_RESOLVED_BY_REGION_RETUNING`**（method-production 终态集五选一）。P01 的条件式子群体信号（cand_rank@weak/低SNR +0.32~+0.43 vs adapter）经 fresh held-out confirmation（seeds {60..70}∪{81..89}∪{90..99}=30，全 disjoint 历史）确认为**真实但非可区分方法**：cand_rank 冻结 ref=9.0 dB 不是 load-bearing，dev 调谐同一 conventional lever（ref 9→11，独立 dev seeds 50–59 选出）即捕获并略超其增益（weakretune−adapter=+0.4539 > cand_rank−adapter=+0.3578；cand_rank−weakretune=−0.0961 |mean|≤MDE）。无可区分 deployable action → 不生成 bounded method card、不晋升、不写论文 claim。
2. **A 族（CPR 选择器鲁棒性）同族连续=2，达 D039 §4 同族上限**。P03 必须换机制族（B/C/D/E 任选）。cand_rank / weakretune / SNR-mismatch / region-retune 子轴关闭，不得换名重开（TL-30）。
3. campaign 计数：`accepted_valid_packages` 0→**2**（P01+P02 两个有效科学包）；`current_package` P02→P03；`same_family_consecutive` A 族=2 重置待 P03 换族；`families_started` 仍=[A_CPR_selector_robustness]（P03 起新族才追加）。P02 是有效包（产出 terminal verdict，非 setup/治理/纯复现）。
4. 一次包内确定性修复已用并记录：T029 §4 seed 集合算术（`{60..70}∪{81..89}`=20 而非 30）由主控授权补 seed 90–99 凑齐 30/cell；判据/dev-ref/方法身份/MDE/§5 顺序全不变；20-seed 与 30-seed verdict 同（PROBLEM_RESOLVED_BY_REGION_RETUNING），结果稳健。不另开 repair 包。
5. claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。仍 0 active carrier。P02 mission_method_delta = `NONE`（PROBLEM_RESOLVED 非方法进度；它消解而非创造方法信号）。
6. harvest：P02 产出一条**有界负面 + operating-regime 收敛证据**——"γ-magnitude-free stage-1 边界的 weak/低SNR 增益可被廉价区域门限重调替代"。作 thesis-harvest 的 robustness-boundary / conventional-comparator-resolves 类记录，不冒充 formal method。

### 理由

P01 留下的 open question 是"cand_rank 的子群体信号是真实可晋升方法，还是常规改进的假象"。P02 用 method-production + baseline-adjudication 的标准门控回答：构造最强廉价常规替代（同一 conventional adapter 结构，仅把 stage-1 ref 当 dev-可调旋钮），在独立 dev 上调谐后 fresh held-out 比较。结果 weakretune 反超 cand_rank 且差异在 MDE 内 → §5 Step 1 触发 PROBLEM_RESOLVED_BY_REGION_RETUNING。这是 minimal baseline ladder 第 3 级（"一个直接针对观察失效的廉价常规扩展"）已解决问题的标准情形，不允许再为同一问题 slice 开 method Scout（baseline-adjudication.md）。诚实有界负面比强行晋升一个非可区分方法更符合 FR-23/TL-32 的科学纪律。

profile（"务实可毕业"+"多挑候选保留余地"+"深耕已有基础"）支持：P02 深耕 P01 已有代码抽基点（cand_rank/adapter 全复用），局部结果自动收敛为常规 retune，自然轮换到 P03 新族，不早收敛、不造方法。

### 排除的替代方案

- 不把 cand_rank 晋升为 bounded method card（§5 Step 1 先于 Step 2 触发，cheap-alt 已达判据；强行取 Step 2 会违反冻结判决顺序）。
- 不在 A 族开 P03（同族连续=2 达上限；TL-30 禁换名重开 cand_rank/weakretune/SNR-mismatch/region-retune 子轴）。
- 不把 PROBLEM_RESOLVED 当方法进度（mission_method_delta=NONE；baseline-adjudication：常规替代已解决问题不允许 method Scout）。
- 不用 oracle/true-truth 当部署输入或 Go 判据（TL-32/FR-25；true γ 仅信号生成 + 离线 oracle bound，V066 确认绝不进 decide）。

### 影响范围

- live control 升 epoch 65→66 / CP030→CP031；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D040。
- `topic-index.md` control block 计数器更新（accepted_valid=2、current=P03、A 族连续=2、rolling_queue 追加 P02）；`mission-log.md` 追加 CP031 行；`verifications.md` 追加 V066。
- protected owner/formal/Skill/thesis framework 不改、无 push。无新 infrastructure。
- 仍 0 active carrier；某 package 出 `DIAGNOSTIC_METHOD_SIGNAL` 且过 promotion preflight 前不晋级。

### 范围确认

本轮（P02 执行 + 接收 + 治理更新）在 scope boundary 内：D039 campaign 授权范围内第 2 个有效包，遵守 problem-first 三阶段门控（Phase A problem 复用 P01 已立 → Phase B adapter 复用 P01 → Phase C 廉价替代裁决）。无 protected owner/formal/Skill/thesis framework 改动、无 push、无新 infrastructure。一次包内确定性修复已披露。

## D041: P03 定点/资源-性能协同设计 → PROBLEM_RESOLVED_BY_UNIFORM_PRECISION（B 族首包，无 METHOD_SIGNAL）

> status: active
> date: 2026-07-30
> 取代：无
> 被取代：无
> 依据：D039-D040 campaign 授权；method-production.md（PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR 终态集的工程族近邻 = PROBLEM_RESOLVED_BY_UNIFORM_PRECISION，uniform-precision 即"常规 comparator 已解决"的定点等价）；baseline-adjudication.md（minimal baseline ladder：uniform-precision 是定点域的常规 baseline）；evidence-and-claims.md（semantic smoke + claim ceiling + resource proxy 标注）；worker-log step-030；V067 独立验收 10/10 PASS；FR-23（问题驱动非空白——对已完成 DA/NDA 选择器注入"定点部署"新失效条件）；TL-32/FR-25（Go/Kill 判据分离）；绑定裁决（撤回 T030 FOE-residual 入口）
> 触发原话：用户本轮执行指令（绑定裁决：撤回无效 T030，新 P03 family = B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN，端到端运行不得停在入口修订）

### 决策

1. **撤回 T030**（FOE-residual→CPR cascade 入口）。T030 经独立历史审计 FAIL，五条独立依据：①1 MHz 是 FOE **前**的 warning 参数（`decisions.md:233`：shared channel 保留 `F_RESIDUAL=1 MHz`，是 FOE 步骤 `fft_foe_m0_omega` 要**移除**的 CFO，非移除后的残差）；②历史多普勒量级远低于 FOE 分辨率（A3 Kill D010 `decisions.md:614-638`：AO 相干时间 τ_c~1ms→Δν≈159Hz；MVE 时序 8.2µs；1MHz/s slew 仅移 8.2Hz；破 FFT-FOE 需 >7.4 GHz/s 非物理）；③未证明真实 post-FOE residual（FR-26）；④comparator/残差范围未冻结；⑤邻近已关闭的 B10/B12 高阶 CPR carrier（TL-30 不得换名重开）。T030 保留为 rejected brief（文件头加 REJECTED 段，正文保留供审计），该准备工作**不计有效 P03**。
2. 接收 P03（T031）端到端结果，terminal verdict = **`PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`**（method-production 终态集六选一）。问题"已完成 DA/NDA CPR 选择器定点部署时是否存在'统一位宽浪费资源或损害分支选择'的真实工程问题"被回答为**否**：可信 bit-true Q(W,F) 模型（float-bypass 0/132,000 逐 window 决策与浮点 `A.decide` 一致）下，uniform-precision 在 (8,6) 已到 regret 地板（gain-bearing 区 +0.027 dB），该地板是**branch-statistical 非 quantization**（(16,14) 处 Q-error≤2⁻⁴⁰ 仍持续 +0.685/+0.806 dB @高SNR cell，集中锚点增益本身 ~0 处）。mixed-precision 最佳候选 `two_exp(8,6)` Pareto-主导 uniform(14,12) 但优势 +0.0166 dB = 9×低于 MDE=0.15 → `mixed_strictly_better_by_mde=[]`。无可区分 deployable action → 不生成 bounded method card、不晋升、不写论文 claim。
3. **B 族（定点/资源-性能协同设计）同族连续=1**（B 族首包）。campaign `families_started` 追加 `B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN`。P04 可选同族第 2 包（B 族连续=2 达上限）或换 C/D/E 族。
4. campaign 计数：`accepted_valid_packages` 2→**3**；`current_package` P03→P04；`same_family_consecutive` B 族=1（P04 若换族重置）。P03 是有效包（产出 terminal verdict，非 setup/治理/纯复现）。
5. 一次包内确定性修复已用并记录：worker-log float-bypass 分母叙述从 "726,000 implying 2200 windows/cell" 更正为 "132,000 = 3 scenes×11 SNR×10 seeds×400 windows/cell"（V067 指出，独立 verifier 重跑 gate 确认 0 mismatch 实质不变；纯叙述算术错，不涉数据/代码/verdict）。Phase-BC 命名 bug（mixed-candidate held-out rows 首跑被键名误丢）已由 executor 修复并重跑，V067 确认最终 artifact 含全部 5 方法×660 rows。
6. claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。仍 0 active carrier。P03 mission_method_delta = `NONE`（PROBLEM_RESOLVED 非方法进度；它消解了"定点会损害分支选择"的假设而非创造方法信号）。
7. harvest：P03 产出两条**有界工程负面 + 定点可部署性证据**——(a) "DA/NDA CPR 选择器在 8-bit uniform Q(8,6) 定点下决策与浮点 byte-exact，定点非该选择器瓶颈"（Ch5 FPGA §5.4/§5.5 可引用的 resource-bitwidth 工程证据，**仅作 bit-cost/resource proxy，无真实综合**）；(b) "stage-2 噪声扣除 1/(2γ_lin) 在高 SNR 的下溢张力真实但量级 9×低于可检测阈值"（two_exp 的 mean-normalization 弱提示，作 future-work seed 不晋升）。作 thesis-harvest 的 engineering-robustness / deployment-feasibility 类记录，不冒充 formal method。

### 理由

P03 的科学问题是"定点部署是否给已完成的 DA/NDA 选择器引入新的失效条件（位宽损害分支选择）或资源浪费"。这是 FR-23 问题驱动（对已完成方法注入定点部署新条件），非空白驱动（"没人做过 X"）。回答需要可信的 bit-true 模型（非 decimal rounding 冒充）和公平的 uniform-vs-mixed 比较。结果：uniform-precision 已在 Pareto 地板，mixed 无可区分增益——这是 baseline-adjudication minimal ladder 在定点域的标准情形（uniform-precision 即定点域的常规 comparator），method-production 终态集判 `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`。诚实工程负面比强行晋升一个 sub-MDE 的 mixed 配置更符合科学纪律。bit-true 模型本身（Q-format 合同 + block-float + LUT-I/O 量化）是可复用的工程资产，支撑 Ch5 FPGA 章节的定点实现可行性论证。

profile（"务实可毕业"+"深耕已有基础"）支持：P03 深耕 P01/P02 已有 selector 代码抽基点（decide 控制路径复用冻结探针），局部结果自动收敛为 uniform-resolved，自然产出可复用 bit-true 资产。

### 排除的替代方案

- 不把 two_exp 晋升为 bounded method card（优势 +0.0166 dB = 0.11×MDE，Pareto-主导但 sub-MDE；强行取 METHOD_SIGNAL 会违反冻结 MDE 判据）。
- 不把 PROBLEM_RESOLVED 当方法进度（mission_method_delta=NONE；baseline-adjudication：常规 baseline 已解决问题不允许 method Scout）。
- 不用真实综合工具声称 LUT/DSP/功耗（brief 六 + V067 check 7：resource proxy 明确标 proxy，无综合工具时只声称 bit-cost/resource proxy 改善，不声称 FPGA LUT/DSP/功耗/吞吐）。
- 不在 B 族强行开第 2 包（B 族连续=1 未达上限 2，但 P03 已 RESOLVED，P04 应评估换族 vs B 族第 2 包哪个更可能产方法）。
- 不重开 NDA-ML 本体或把旧浮点增益重新计作新成果（TL-30 + 绑定裁决：P03 只评估定点对已完成选择器的影响，不重跑/不重计 NDA-ML 浮点增益）。

### 影响范围

- live control 升 epoch 66→67 / CP031→CP032；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D041。
- `topic-index.md` control block 计数器更新（accepted_valid=3、current=P04、B 族连续=1、families_started 追加 B、rolling_queue 追加 P03）；`mission-log.md` 追加 CP032 行；`verifications.md` 追加 V067。
- protected owner/formal/Skill/thesis framework 不改、无 push。无新 infrastructure（bit-true 模型是独立 _p03_*.py 新文件，非大型 FPGA 综合基础设施）。
- 仍 0 active carrier；某 package 出 `DIAGNOSTIC_METHOD_SIGNAL` 且过 promotion preflight 前不晋级。

### 范围确认

本轮（撤回 T030 + P03 执行 + 接收 + 治理更新）在 scope boundary 内：D039 campaign 授权范围内第 3 个有效包，遵守 problem-first 三阶段门控（Phase A uniform-precision baseline → Phase B 仅因 Phase A 显现弱张力而运行 → 公平比较裁决 sub-MDE）。撤回 T030 是绑定裁决要求，保留 rejected brief 供审计。无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施。两次包内确定性修复（叙述分母 + Phase-BC 键名）均已披露。

## D042: P04 连续 GG OOD 选择器鲁棒性 → PROBLEM_ABSENT_ON_CONTINUOUS_GG（C 族首包，有效负面）

> status: active
> date: 2026-07-30
> 取代：无
> 被取代：无
> 依据：D039-D041 campaign 授权；method-production.md（PROBLEM_ABSENT_ON_CONTINUOUS_GG 终态）；evidence-and-claims.md（semantic smoke + claim ceiling）；baseline-adjudication.md（problem-bearing probe 门控）；worker-log step-031；V068 独立验收 8/8 PASS；FR-23（问题驱动——对已完成 DA/NDA 选择器注入连续 GG 形状新失效条件）；FR-26（证据链）；绑定裁决（撤回无效 16APSK 环比入口 + 湍流标签入口，端到端执行 C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS）
> 触发原话：用户本轮执行指令（绑定裁决：撤回无效 16APSK 环比/湍流标签入口，新 P04 family = C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS，同对话端到端执行不得停在入口修订或 problem probe 后）

### 决策

1. **撤回无效 P04 入口**（16APSK 环比失配 + 湍流标签失配）。经绑定裁决独立审计四条 FAIL：①γ（环比）是调制格式配置非当前信道随机量；②冻结选择器 `decide(raw,γ_db,γ_lin)`（`_a4_switch_common768_30seed.py:97-107`）信息边界干净——不读取环比（环比只进 `per_block` 内 `m16apsk_demod` 即分支输出产生，selector 只读分支输出错误计数）也不读取 turbulence label（`main:312` 循环变量从不传入 decide；`method.tex:75`/`abstract.tex:2` 明确无湍流重调）；③matched/configured demod 是显然常规解；④两入口均无 selector 可作用面。保留 rejected brief（`P04-entry-selection-NOT-RUN.md` 加 REJECTED 段），**不计有效 P04**。
2. 接收 P04 端到端结果，terminal verdict = **`PROBLEM_ABSENT_ON_CONTINUOUS_GG`**（method-production 终态集六选一）。绑定裁决改写的合法问题"固定/AWGN 拟合的 CV decision boundary 在文献参数范围内、训练未见过的连续 GG 分布上是否产生 selector-specific regret"被回答为**否**：pooled held-out interior regret = **+0.1459 dB**（CI=[+0.0827,+0.2090]），统计上存在（CI_low>0）但**量级低于冻结 MDE=0.15 dB**；dev（seeds 0-9）+0.1393 与 held-out（seeds 30-49）+0.1459 一致（差 0.007 dB）。Phase A problem gate（pooled，§1.1 P2 冻结于读结果前）未过 → Phase B/C 不运行 → 无方法构造。
3. **诚实子区间结构**（已披露非掩埋）：9/30 interior cell 超 MDE 且 CI_low>0，集中在 weak-side interior（σ_R² 0.3/0.9/1.35 × γ 5-11 dB），最强 σ_R²=0.30 γ=9 +0.678 dB；但该 regret **非 OOD-specific**——同一 over-NDA-select 行为在 weak 训练锚点上更强（pooled anchor regret +0.2306 dB > interior +0.1393 dB；weak 锚点 σ_R²=0.2 γ{5,7,9,11} = +0.39/+0.78/+0.98/+0.56 dB 均 > interior σ_R²=0.45 同 cell）。regret 随 σ_R² 增大单调下降，强湍流侧（σ_R² 1.85/2.30/3.15）pooled <0.15、γ=13 dB 转负（selector 略有帮助）。**连续 GG 形状本身不让 AWGN 拟合边界退化**——regret 是跨 σ_R² 的平坦 selector 属性。
4. **C 族（连续 GG OOD 选择器鲁棒性）首包完成**（连续=1，未达上限）。campaign `families_started` 追加 `C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS`。P05 可选 C 族第 2 包（连续=2 达上限）或换 D/E 族。
5. campaign 计数：`accepted_valid_packages` 3→**4**；`current_package` P04→P05；`same_family_consecutive` C 族=1。P04 是有效包（产出 terminal verdict，非 setup/治理/纯复现/入口 preflight）。
6. 一次包内确定性修复已用并记录：`sigma2_to_ab` 在 3 个训练 σ_R² 用冻结四舍五入锚点对（11.6,10.1)/(4.0,1.9)/(4.2,1.4)（锚点训练于此非 Al-Habash 精确值）保证 byte-exact 回归，内部连续点用 Al-Habash 闭式（偏离锚点 ≤2.70%，受控外推非跳跃）。原因：Al-Habash 精确值 vs 冻结对偏离 ≤2.70%（验证：weak 0.44%/0.22%、moderate 0.66%/0.55%、strong 0.61%/2.70%），用精确值在 strong β（1.3622 vs 1.4）破坏 byte-exact 回归（85/108 mismatch）。V068 check 1/2 确认修复后 0 mismatch。
7. claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。仍 0 active carrier。P04 mission_method_delta = `NONE`（PROBLEM_ABSENT 非方法进度；它回答"否"而非创造方法信号）。
8. harvest：P04 产出**有界负面 + 连续 GG OOD 验证资产**——(a) "冻结 DA/NDA 选择器的 AWGN 拟合 CV 边界在连续 GG 形状（σ_R²∈[0.2,3.5] 内 off-anchor）上不产生 OOD-specific regret（pooled held-out +0.146 dB < MDE=0.15）"——对 Ch4 selector 鲁棒性论证可作受界工程证据；(b) weak-side-low-SNR 子区间（σ_R² 0.3-1.35 × γ 5-11，9/30 cell > MDE）的 over-NDA-select 倾向作 future-work seed，但**与已关闭 A 族（SNR-mismatch/region-retune）工作区重叠**，TL-30 禁换名重开，降级不晋升。

### 理由

P04 的科学问题是"AWGN 拟合的 CV 边界是否在连续 GG 形状 OOD 下退化"。回答需要：(a) 可信的 σ_R²→(α,β) 映射（Al-Habash 闭式 `system_model.tex:16-21`，文献溯源 Gu 2022/Al-Habash 2001，验证复现 3 锚点 ≤2.70%）；(b) 显式 (α,β) 注入（`generate_shared_realization_apsk(turb_params=...)`，复用 TL-13 共享信道）；(c) 锚点 byte-exact 回归门控（0 mismatch 证明注入路径忠实）；(d) dev/held-out seed 隔离。结果：pooled regret 真实但 sub-MDE，且 anchor > interior 证明非 OOD-specific——这是 evidence-and-claims 的标准 PROBLEM_ABSENT 情形（semantic smoke 通过但 problem gate 未过），method-production 终态集判 `PROBLEM_ABSENT_ON_CONTINUOUS_GG`。诚实的 sub-MDE 负面 + 子区间 future-work seed 比强行在 9/30 cell 上构造一个 region-specific 方法更符合科学纪律（且会违反 TL-30 换名重开 A 族禁令）。

profile（"务实可毕业"+"深耕已有基础"+"诚实负面可 harvest"）支持：P04 深耕 P01/P02 已有选择器代码抽基点（decide 控制路径 + per_block 分支输出全复用冻结探针），局部结果自动收敛为 PROBLEM_ABSENT，自然产出可复用连续 GG OOD 验证资产。

### 排除的替代方案

- 不把 9/30 cell > MDE 晋升为 DIAGNOSTIC_METHOD_SIGNAL（pooled 门控冻结为 pooled，0.1459<0.15；改门控违反 V067 check 9 / brief trap #9；且子区间 regret 在训练锚点上更强 → 非 OOD-specific）。
- 不构造 weak-side region-specific 方法（与已关闭 A 族 SNR-mismatch/region-retune 工作区重叠，TL-30 禁换名重开；且 problem gate 未过不允许 method Scout）。
- 不把连续 GG 负面外推成全部 turbulence robustness（绑定裁决明确禁止；saturation/新传播模型/拍定参数未用）。
- 不用 mcs `rytov_to_gg` 经验 piecewise-symmetric proxy（强制 α=β，非引用公式；用 Al-Habash 闭式）。
- 不重开已关闭轴（A 族 / NDA-ML 本体 / G1 / CB1 / Pilot-Jones / FOE-residual，TL-30）。

### 影响范围

- live control 升 epoch 67→68 / CP032→CP033；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D042。
- `topic-index.md` control block 计数器更新（accepted_valid=4、current=P05、C 族连续=1、families_started 追加 C、rolling_queue 追加 P04）；`mission-log.md` 追加 CP033 行；`verifications.md` 追加 V068。
- protected owner/formal/Skill/thesis framework 不改、无 push。无新 infrastructure（_p04_*.py 是独立新文件，复用 common 信道）。
- 仍 0 active carrier；某 package 出 `DIAGNOSTIC_METHOD_SIGNAL` 且过 promotion preflight 前不晋级。

### 范围确认

本轮（撤回无效 16APSK/湍流标签入口 + P04 端到端执行 + 接收 + 治理更新）在 scope boundary 内：D039 campaign 授权范围内第 4 个有效包，遵守 problem-first 三阶段门控（Phase A problem-bearing probe → gate 未过 → 不进 Phase B/C）。撤回两入口是绑定裁决要求，保留 rejected brief 供审计。无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施。一次包内确定性修复（sigma2_to_ab 锚点对）已披露。

---

## D043: P05 ML polarization equalizer OOD safe online adaptation — standard-CMA-continuation 恢复 swap regret → PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER

> status: active
> date: 2026-07-30
> 取代：无
> 被取代：无
> 依据: 验证: `projects/simulation/results/cma-fade-divergence/p05_phase0_identity.json`、`p05_ood_online_adaptation.json` + 脚本 `explore/cma-fade-divergence/p05_phase0_identity.py`、`p05_ood_online_adaptation.py` + 运行日志 `p05_run4.log` + V069 独立验收 + D022/D023/D032/不变量9/10/11 + binding decision

### 决策

**campaign 5/10，新机制族 D（D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION）首包。端到端一轮完成 Phase 0→A→B：frozen ButterflyCNN ML equalizer 在 (4.2,1.4) strong + N=5M SOP 累积旋转下产生稳定 +0.499 fixed-label BER swap regret（Phase A 问题成立），但 corrected standard-CMA-continuation（Godard 1980 with-z，在线）在两 cell 上 mean fixed-label BER 0.00018/0.00117 ≪ MDE=0.05 完全恢复 swap → `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`。Phase C 不运行（B 已解决）。不产方法卡/不晋升。**

对象 = `ButterflyCNNEqualizer2x2`（`common/_ml_equalizer.py:104`，双偏振蝶形 CNN MSE 监督，Q-CMA-FADE 方法层，contract H2/B4），**与 NDA-ML CPR selector（P01-P04 对象）不同方法身份**（不同类别/explore 目录/session）。

### Phase 0：身份门 CLOSED

无磁盘 checkpoint；frozen-ML identity = 冻结 seed+params 确定性复现。P0.1 ML 两次完整 train+equalize state_hash byte-identical（`03e91429dfed74c6`）；P0.2 StandardCMA2x2 byte-identical + z-factor 源 `prompt019:206-213`。channel provenance = 当前 params.py strong=(4.2,1.4) 真值（D036 记录的 1.5/0.8→4.2/1.4 drift；用当前真值保可复现）；F_G=30/SOP=4e-7/20dB/QPSK/N_TAP=11。in-dist anchor 复现 D022 修正后不变量 9：ML fixed-label≈0.5（swap）、standard-CMA fixed-label≈0（no-swap）。

### Phase A：问题成立（PRIMARY=fixed-label BER，swap-visible）

冻结（读结果前）：PRIMARY gate metric = fixed-label BER（dual-pol 不变量 10「PI-BER 对 swap 结构性失明」，PI 报告 secondary）；MDE_FIXED=0.05；两 cell（anchor N5M/fg30/20dB + provenance-OOD N5M/fg100/20dB，**不提高 SOP/f_G 制造问题**）。

| cell | fixed-label ML−CMA | CI | wins | cma_div_frac | gate |
|---|---|---|---|---|---|
| anchor | **+0.4990** | [+0.4983,+0.4997] | 3/3 | 0.0 | True |
| fg100 | **+0.4981** | [+0.4948,+0.5013] | 3/3 | 0.0 | True |

四混淆分离：(1) ML 自身 swap 真实；(2) CMA 共同退化否（cma_div_before_late 全 False，CMA fixed≈0）；(3) metric 伪差否（PI swap-blind 是结构性非无问题，fixed-label swap-visible diff≈0.5 稳定）；(4) 单 seed 否（6/6 swap）。

### Phase B：standard-CMA-continuation 恢复

comparators（同预算/prefix-only/receiver-visible/独立 dev/无 future 回灌）：standard-CMA-continuation、DD-LMS（block-grained）、periodic-pilot-finetune（D032 weak 化身，声明 overhead 0.2%）。recovered = comparator mean fixed-BER < MDE AND (ML−comp) ≥ MDE：

| cell | standard-CMA-cont | DD-LMS | periodic-pilot |
|---|---|---|---|
| anchor | 0.00018 **recovered** | 0.453 no | 0.499 no |
| fg100 | 0.00117 **recovered** | 0.449 no | 0.499 no |

standard-CMA-continuation 两 cell recovered → `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`。DD-LMS（slicer 在 swap 下喂错标签锁错盆地）与 periodic-pilot（与 D032 KILL 一致，weak Adam 1-step 不足以翻 swap）均未恢复。Phase C 不运行。

### 核心结论

- **swap 是 ML 固定权重 SOP 泛化失败**（D015/D040 回归），不是 CMA 在线更新的问题——corrected Godard-with-z CMA 在线跟踪 SOP 不 swap（D022 修正后不变量 9 再验证）。
- **standard-CMA 已是解决 swap 的常规在线 equalizer**——本包问题被常规 comparator 解决，无可区分 deployable ML-specific action，不产方法卡/不晋升。
- **D032 C1 KILL 独立佐证**：periodic-pilot（D032 同 weak 化身）作 comparator 同样未恢复，坐实 D032 结论非可重开信号。
- **强化 contract H2 适用边界（D023）**：ML 优于 standard-CMA 仅 PI-BER 窄域成立，fixed-label 口径 standard-CMA 远优于 ML；论文不得声称 ML 鲁棒优于 standard-CMA。

### 否决了什么

- 不构造 Phase C 在线适配方法（standard-CMA 已解决，门控顺序禁 B resolved 后跑 C）。
- 不把 fixed-label +0.499 swap regret 当 DIAGNOSTIC_METHOD_SIGNAL（swap 不是 ML-可优于-常规-在线-CMA 的 deployable action；常规在线 CMA 已解决）。
- 不重开 D032 C 类（本包 periodic-pilot 作 comparator 仅佐证 KILL，非复活；D032 明载"不否决更强化身但须重走 GW 门控"，本包未提更强化身方法）。
- 不把 PI-BER diff≈0 当 PROBLEM_ABSENT（不变量 10：PI 对 swap 结构性失明；fixed-label 才是真记分牌）。

### 可复用部分

- `p05_phase0_identity.py` + `p05_ood_online_adaptation.py`：ML identity freeze + 三阶段门控框架（Phase A fixed-label gate + Phase B 三 comparator + Phase C 候选工厂未触发），可复用于后续 ML-equalizer 子问题。
- corrected standard-CMA-continuation 作 swap 解决 baseline 的证据资产（Ch3/Ch4 双口径警示）。

### 影响范围

- live control 升 epoch 68→69 / CP033→CP034；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D043。
- `topic-index.md` control block：accepted_valid 4→5、current P05→P06、families_started 追加 D、rolling_queue 追加 P05；`mission-log.md` 追加 CP034；`verifications.md` 追加 V069；新增 S005。
- protected owner/formal/Skill/thesis framework 不改、无 push、无新 infrastructure（p05_*.py 独立新文件，复用 common/_ml_equalizer + prompt019 StandardCMA + ml_long_seq_failure 信道）。
- 仍 0 active carrier；claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。

### 触发原话

> 触发原话: 无（用户中转 binding decision 执行指令；P05 是 mid-calibration 包，结论来自数据验证非用户态度）

### 包内确定性修复（3 次，全披露，V069 复核）

1. metric-signature：Phase A PRIMARY gate 初版错用 PI-BER（swap-blind），改 fixed-label（D018 + 不变量 10 强制）。
2. dtype：`periodic_pilot_finetune` complex128→complex64（纯类型）。
3. recovered 判据方向：`(ML−comp)<MDE` → `comparator_mean<MDE AND (ML−comp)≥MDE`（对齐 binding decision「已恢复问题」）。

### 来源

worker-log `step-032-p05-ml-ood-online-adaptation.md` + V069

## D044: P06 绑定裁决（撤回旧 window/complexity 入口）+ E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION → NO_CAUSAL_HISTORY_INCREMENT

> status: active
> date: 2026-07-31
> 取代：无（撤回 P06-entry-selection-NOT-RUN.md 的旧"E 信息复杂度边界/window-length"入口为 rejected brief；不取代任何 active 决策）
> 被取代：无
> 依据: 验证: `projects/simulation/results/p06_causal_cross_frame_history/p06_phase0_physical_identity.json`、`p06_phaseA_result.json`、`p06_terminal_verdict.json`、`p06_verifier_result.json` + 脚本 `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/src/p06/{run_p06,build_datasets,build_all,phaseA_eval,verify_p06}.py` + `FROZEN_CONTRACT.md` + V070 独立验收 + 旧 F3-A 无效性 (`run_f3a_history.py:195-196` + `state/current.yaml:161-170` + `portfolio/current.yaml:173-181`) + binding decision（本轮用户执行指令）
> 触发原话: 用户本轮 P06 执行指令（绑定裁决：撤回旧 P06 window/complexity 入口，新 P06 = E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION 一次性修复型 PROBLEM_BEARING_PROBE，同对话端到端执行不得停在入口修订或 Phase 0/A 后）

### 决策

1. **撤回旧 P06 入口**（E 信息复杂度边界 / window-length vs Cramér-Rao）。经绑定裁决四条 FAIL：①与旧 B1 adaptive phase-window、P05-E window/complexity 作用点重复；②NDA 已有 whole-window/segmented time support（`_gg_time.py` 块级/块内窗口）；③当前无真实 latency/resource budget 驱动窗口长度部署 regret（P03 定点 proxy 无真实综合、P05-D 无真实 FEC）；④不能把旧机制改名为第五族（TL-30）。保留 rejected brief（`P06-entry-selection-NOT-RUN.md` 加 REJECTED 段），**不计有效 P06**。
2. 新 P06 = **`E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION`**（一次性修复型 `PROBLEM_BEARING_PROBE`）。修复旧 F3-A 科学无效性：`run_f3a_history.py:195-196` 把 `max(history_mi) - max(block0_mi)`（两个不同特征集上的边际 MI 最大值之差）当成 conditional MI（无 block-0 条件化）；`state/current.yaml:161-170` / `portfolio/current.yaml:173-181` 已标 `INVALIDATED_AS_CONDITIONAL_MI`。**不继承旧数值** +0.060 bits / +0.036 R²（仅历史保留）。
3. **Phase 0 物理与身份门 ALL PASS**（6 conditions）：frame-level GG state transition（`_gg_time.py` AR(1) 块级，frame=140k sym dt=56µs，不显式逐符号模拟）；GG 边缘 KS 0.056–0.144（<0.15）、块 ACF 与 ρ^lag 一致 relerr<0.2%、rho_frame 与 exp(-Δt/τ_c) 一致（fg30=0.99/fg100=0.97/fg1000=0.70）、冻结 CMA 身份重跑 relerr=0 byte-identical 0 divergence。
4. **Phase A 问题与严格因果信息门**：dev fail events 428/1140（frac=0.375，floor=30 MET）。test（180 trajectory 配对）：history-expanded ridge R²=0.320 > current-only ridge R²=0.040（MSE 减少per-traj macro mean=2.25e-02 CI=[4.72e-03,4.68e-02] CI_lo>0，**严格因果增量统计存在**）；**但 persistence R²=0.853（EWMA 0.853 / AR(1) 0.848）远优 history**。逐 condition（含动态 fg1000 rho=0.70）：persistence 0.68–0.95 全胜 history 0.04–0.88。**更便宜的常规 temporal baseline（last-value persistence）已远优解决**，无可区分 deployable 方法 → terminal verdict = **`NO_CAUSAL_HISTORY_INCREMENT`**。
5. Phase B/C **不运行**（Phase A 未过 signal 门）。只 harvest observability boundary。
6. verifier V070 **7/7 PASS / ACCEPT**（causality alignment、truth/future leakage、trajectory split、raw→aggregate、ACF、seed discipline、verdict 唯一性与逻辑全过；raw→aggregate dev_fail raw=428=reported，ACF relerr<0.2% 全 condition，test seed 与历史 11-150/30-99 零重叠）。

### 核心结论

- **修复了旧 F3-A 的科学无效性**：用严格因果 held-out 预测增量取代错误的 conditional-MI 声明。旧 +0.060 bits/+0.036 R² 不继承，`state/current.yaml`/`portfolio/current.yaml` 的 INVALIDATED 标记不动（旧 F3-A 仍 invalidated，新 P06 单独登记）。
- **物理诚实**：deployable frame rate（dt=56µs）≪ τ_c（0.16–5.3ms），只有 f_G=1000Hz（Greenwood 上界）有非平凡跨帧动力学（rho=0.70），f_G=30/100 准静态。即便 fg1000，下一帧失效/性能被 last-value persistence 以 R²=0.75 主导——**跨帧信息被帧间持续性主导，非新方法空间**。
- **history 增量真实但 sub-persistence**：history features 在 current-only 之外有统计显著预测增量（CI_lo>0），证明旧 F3-A 的"history 携带信息"直觉方向正确，但其量级被更便宜的常规 temporal baseline 完全吸收，无可区分 deployable action。

### 否决了什么

- 不把 history R²=0.32 > current-only R²=0.04 当 `CAUSAL_HISTORY_INFORMATION_SIGNAL`（persistence R²=0.85 远优，门控顺序：history 必须超最强传统 temporal comparator 才算 signal）。
- 不构造 Phase B/C 方法（Phase A 未过 signal 门；门控顺序禁 A 未过跑 B/C）。
- 不重开旧 F3-A 数值（+0.060/+0.036 invalidated 保留；新 P06 不继承）。
- 不调窗口、不做 DA/NDA selector、不做 Pilot-Jones、不微调 ButterflyCNN（绑定裁决禁止）。
- 本轮失败后关闭 E 族，**不允许再开第二个 evaluator-repair 包**（绑定裁决）。

### 可复用部分

- `run_p06.py`（Phase 0 物理身份门 + frame-level 数据集构建）、`phaseA_eval.py`（严格因果预测增量评估：current-only/history-expanded ridge + persistence/EWMA/AR(1) temporal baselines + per-traj bootstrap CI + logistic failure-target）、`verify_p06.py`（独立 verifier 7 项）：可复用于后续 cross-frame observability 子问题。
- frame-level GG state transition + rho 覆盖（fg30/100/1000）+ 冻结 CMA 身份 freeze 资产。
- harvest：(a) Ch3/Ch4 receiver-observability 边界证据（跨帧信息被帧间持续性主导）；(b) 方法论附录教训（marginal-MI max-difference ≠ conditional-MI）；(c) 物理诚实资产（deployable frame rate ≪ τ_c 下跨帧动力学边界）。

### 影响范围

- live control 升 epoch 69→70 / CP034→CP035；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D044。
- `topic-index.md` control block：accepted_valid 5→**6**、current P06→P07、families_started 追加 `E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION`（第 5 族，"≥5 族"达成）、same_family_consecutive E=1、rolling_queue 追加 P06；`mission-log.md` 追加 CP035；`verifications.md` 追加 V070；`P06-entry-selection-NOT-RUN.md` 加 REJECTED 段。
- protected owner/formal/Skill/thesis framework 不改、无 push、无新 infrastructure（p06_*.py 独立新文件，复用 common/_gg_time + common/_dual_pol_channel + atlas standard_cma_godard_with_z + cb1_evaluator）。
- 仍 0 active carrier；claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。旧 F3-A `state/current.yaml`/`portfolio/current.yaml` INVALIDATED 标记不动。

### 范围确认

本轮（撤回旧 P06 入口 + P06 端到端执行 Phase 0/A + 接收 + 治理更新）在 scope boundary 内：D039 campaign 授权范围内第 6 个有效包，遵守 problem-first 门控（Phase A problem-bearing probe → gate 未过 signal → 不进 B/C）。撤回旧入口是绑定裁决要求，保留 rejected brief 供审计。无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施。无包内确定性修复需要披露（一次跑通）。

### 来源

worker-log `step-033-p06-causal-cross-frame-history.md` + artifacts `projects/simulation/results/p06_causal_cross_frame_history/*` + V070 + 旧 F3-A `run_f3a_history.py` / `state/current.yaml` / `portfolio/current.yaml`

## D045: P07 绑定裁决（撤回旧 F/G/H 扫描）+ F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG → NO_DIAGNOSTIC_METHOD_SIGNAL

> status: partial_supersede_science_only  # 入口裁决部分仍 active；科学有效性部分被 D046 取代
> date: 2026-07-31
> 取代：无（撤回 P07-entry-selection-NOT-RUN.md 的旧 F/G/H 扫描为 rejected brief；不取代任何 active 决策）
> 被取代：科学有效性部分（Phase 0 可信因果 AGC/ADC adapter PASS + Phase A/B/C verdict + NO_DIAGNOSTIC_METHOD_SIGNAL）被 D046 取代；入口裁决部分（撤回旧 F/G/H、定义 P07=F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG、与 P03 区分）仍 active
> 依据: 验证: `projects/simulation/results/p07_agc_adc_dynamic_range/p07_phase0_smoke.json`、`p07_phaseA_dev.json`、`p07_phaseBC.json`、`p07_terminal_verdict.json`、`p07_verifier_result.json` + 脚本 `projects/simulation/explore/nda-awgn-tracking-sandbox/{_p07_adapters,_p07_runner,_p07_batch,_p07_smoke,_p07_phaseA,_p07_phaseBC,_p07_verify}.py` + `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/src/p07/FROZEN_CONTRACT.md` + V071 独立验收 10/10 ACCEPT + binding decision（本轮用户执行指令）
> 触发原话: 用户本轮 P07 执行指令（绑定裁决：撤回旧 P07-entry F/G/H 扫描，新 P07 = F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG，同对话端到端执行不得停在入口修订或 Phase 0/A/B 后）

### 决策

1. **撤回旧 P07 入口**（F symbol-timing offset / G 场景扩展 / H FEC/APSK）。经绑定裁决独立审计三条 FAIL：①F——`common/_channel.py:97-169` 与 `common/_dual_pol_channel.py` 信道只有逐符号 `signal = tx*sqrt(h)*carrier` + AWGN，**无过采样 / 脉冲成形 / 分数延迟**（grep `oversamp|pulse_shape|rrc|rcos|upsample|fractional_delay` 零命中）；1-sps 下 symbol-timing offset 没有可作用物理自由度；②G——未冻结 M-C-A；易重入已关闭 P04（连续 GG OOD）/ FOE-residual 轴（T030 撤回）；③H——coded chain blocked（P05-D 撤回：无真实 codec / threshold eval 非 FEC）；APSK 环比入口 P04 已撤回（γ 是调制配置非信道随机量，selector 不读环比）。保留 rejected brief（`P07-entry-selection-NOT-RUN.md` 加 REJECTED 段），**不计有效 P07**。
2. 新 P07 = **`F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`**（candidate-universe.yaml U07，ap=AP06）。**严格区别于 P03**：P03 = selector 内部定点 Q(W,F) 数字后处理（控制路径）；P07 = 模拟前端可变增益 + ADC 满量程/削顶/量化分辨率，作用于 **`rx_raw` 在整个冻结接收链之前**。
3. **Phase 0 可信因果 AGC/ADC adapter ALL 5 BLOCKER gates PASS**：signed I/Q quantizer（`code=clip(round_half_up(gain·value/step), ±(2^(W-1)-1))`，`step=2·FS/2^W`，饱和不 wrap）；G1 ADC math（round-half-up +0.5LSB→+1/-0.5LSB→0、饱和不 wrap W4 100·FS→7 非 -8、signed 对称 ±0.3→±38 @W8）；G2 float-bypass 重构 ≤2^-40（W=64+FS=1e6）；G3 **float-bypass 接收链 byte-identical `run_case_multidelta`**（FixedGainAGC(g=1,W=64) 与原 run_case_multidelta 逐 cell 0 mismatch，weak/mod/strong ×{5,9,15,21}×seeds{0,1,2}）；G4 因果性（window-0=nominal，gain 随过去 RMS 单调，确定性重放）；G5 信息边界 AST（AGC class 体 + `quantize_iq` 体零 forbidden 子串 h/alpha/beta/tx/phi/bits/oracle/future）。
4. **Phase A 问题成立**（dev grid 3 scenes×SNR{5,9,13,17,21}×dev seeds{0..4}=75 cell，FROZEN_CONTRACT §4 冻结代表性子集 5 SNR 跨低-高非单点；MDE=0.15；fixed-gain ladder {0.5,0.75,1.0,1.25,1.5,2.0,2.5,3.0,4.0} 预冻结非 cherry-pick）：dev-best fixed-gain g=0.75 pooled regret **+1.028/+0.924/+0.909 dB** W6/8/10（CI=[+0.886,+1.170]/[+0.799,+1.049]/[+0.788,+1.031]，CI_low 全>0），14-15/15 cell ≥MDE；clipping rate 随 gain 单调（g0.5→2.5%、g0.75→15%、g1.0→30%、g4.0→91%），低 gain 侧分辨率损失 + 高 gain 侧峰值 clipping —— **clipping–resolution 折中真实存在**。Phase A 门过 → 进入 Phase B。
5. **Phase B 传统 comparator 部分缓解但未解决**：最强传统 AGC=causal-RMS（dev-tuned，公平 3-config 预注册集，相同过去信息/更新预算/增益上下限/延迟），把 regret 从 +0.91~+1.03 dB 降到 **+0.896/+0.794/+0.767 dB**（缓解 0.12-0.20 dB，仍 5-6×MDE），`conv_resolves=False` → 进入 Phase C。
6. **Phase C 方法候选无一稳定超最强传统 AGC**（held-out 3 scenes×SNR{5,9,13,17,21}×seeds{30..34}=75 cell，paired delta=conv−cand 正=cand 更好）：最佳候选 dual_tc paired delta = **−0.016/−0.004/−0.017 dB**（CI 全跨 0，|Δ|≪MDE=0.15）；clipping_aware −0.21、robust_pct −0.12、hysteretic −0.47 全 ≤0（候选无一胜过 causal-RMS，多数更差）。无可区分 deployable action → terminal verdict = **`NO_DIAGNOSTIC_METHOD_SIGNAL`**。
7. verifier V071 **10/10 PASS / ACCEPT**（V1 ADC math / V2 float-bypass 身份独立重跑 / V3 信息边界 AST / V4 因果性 / V5 raw→aggregate relErr≤1e-9 + paired_regret identity / V6 seed 隔离 dev0-4·held-out30-34 无71-80 / V7 paired realization batched 等价 direct / V8 Phase-A terminal verdict re-derive / V9 frozen 文件未改 / V10 Phase-BC aggregate recompute + verdict re-derive）。

### 核心结论

- **clipping–resolution 折中真实存在**（Phase A 固定增益 +0.9-1.0 dB，机制由 clipping rate 单调随 gain 证实）。
- **标准 causal AGC 部分缓解但未解决**（Phase B +0.77-0.90 dB 仍远高于 MDE）。
- **4 个机制不同的 robust/clipping-aware AGC 无一稳定超 dev-tuned causal-RMS**（Phase C 最佳 dual_tc |Δ|≪MDE CI 跨0，clipping_aware/robust_pct/hysteretic 全更差）。
- **不是"问题不存在"也不是"常规已解决"**，是"问题真实存在、常规部分缓解、无方法增量"——迄今机制最完整的诚实负面。

### 否决了什么

- 不把 dual_tc 的 −0.016~−0.017 dB 当 `DIAGNOSTIC_METHOD_SIGNAL`（|Δ|≪MDE，CI 跨0；门控顺序：候选必须稳定超最强传统 AGC 达 MDE 才算 signal）。
- 不构造 Phase C 之外的新候选（4 机制已覆盖 attack/release/anti-windup/percentile/hysteretic 主要轴；cheap-alternative 已检）。
- 不重开已关闭轴（A/E 族 / NDA-ML 本体 / G1 / CB1 / Pilot-Jones / FOE-residual，TL-30）。
- 不把 P07 的 symbol-timing-offset（F）/场景扩展（G）/FEC-APSK（H）子轴换名重开（已撤回"无可作用物理自由度/重入已关闭轴"）。
- 不混淆 P07 与 P03（P03=selector 内部定点数字后处理；P07=模拟前端 AGC+ADC 在接收链之前——不同作用位置/不同对象）。

### 可复用部分

- `_p07_adapters.py`（signed I/Q quantizer + fixed/causal-RMS/peak-hold/log-domain AGC + 4 候选）、`_p07_runner.py`（float-bypass runner）、`_p07_batch.py`（批量评估，one channel-gen/cell）、`_p07_smoke.py`（Phase 0 五门）、`_p07_phaseA.py`、`_p07_phaseBC.py`、`_p07_verify.py`（独立 verifier 10 项）：可复用于后续 AGC/ADC 子问题。
- float-bypass 身份验证资产（AGC+ADC 在 float-bypass 下 byte-identical 冻结接收链）作 Phase 0 模板。
- harvest：(a) Ch5 接收机 8-10 bit uniform signed I/Q ADC + causal-RMS AGC 是该冻结接收链在源闭合 GG 下的合理模拟前端配置（fixed-gain 与 causal-RMS 的 clipping/量化边界曲线）；(b) Ch3/Ch4 鲁棒性边界（该 clipping–resolution 折中不是 ML/robust-AGC 可优于标准 causal-RMS 的 deployable 子问题）—— 与 P06 一致的 "receiver-visible 信号被常规 baseline 吸收" 趋势。

### 影响范围

- live control 升 epoch 70→71 / CP035→CP036；active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`；authority → D045。
- `topic-index.md` control block：accepted_valid 6→**7**、current P07→P08、families_started 追加 `F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`（第 6 族）、same_family_consecutive F=1、rolling_queue 追加 P07；`mission-log.md` 追加 CP036；`verifications.md` 追加 V071；`P07-entry-selection-NOT-RUN.md` 加 REJECTED 段。
- protected owner/formal/Skill/thesis framework 不改、无 push、无新 infrastructure（p07_*.py 独立新文件，复用 common/_channel + frozen receiver + _p01 probe）。
- 仍 0 active carrier；claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。

### 范围确认

本轮（撤回旧 P07 F/G/H 入口 + P07 端到端执行 Phase 0/A/B/C + 接收 + 治理更新）在 scope boundary 内：D039 campaign 授权范围内第 7 个有效包，遵守 problem-first 三阶段门控（Phase A problem-bearing probe 门过 → Phase B 传统 comparator 部分缓解未解决 → Phase C 方法候选无增量）。撤回旧入口是绑定裁决要求，保留 rejected brief 供审计。无 protected owner/formal/Skill/thesis framework 改动、无 push、无新大型基础设施。1 次包内确定性修复（Phase-BC JSON 序列化 numpy bool_ bug）已披露。

### 来源

worker-log `step-034-p07-agc-adc-dynamic-range.md` + artifacts `projects/simulation/results/p07_agc_adc_dynamic_range/*` + V071 + FROZEN_CONTRACT.md + binding decision

---

## D046: P07 科学完整性修复 — 冻结旧 P07 科学结论（三根因：H1 SCALE/H2 CONTROL/H3 LIFECYCLE），campaign 计数回退 7→6，重做 gain-aware ADC + stateful trajectory

> status: active
> date: 2026-07-31
> 取代：D045 的**科学有效性部分**（Phase 0 可信因果 AGC/ADC adapter PASS + Phase A/B/C 数字 + verdict `NO_DIAGNOSTIC_METHOD_SIGNAL` + V071 的科学层结论）；D045 的**入口裁决部分**（撤回旧 F/G/H、P07=F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG、与 P03 区分）继续 active
> 被取代：无
> 依据: 验证: `projects/simulation/results/p07r_agc_adc_repair/p07r_prefail_evidence.json`（三根因最小失败测试，修复前证据）+ 源码逐行核：`_p07_runner.py:111-118`（q 直接进 receiver 不 /g）、`_p07_adapters.py:158-183`（CausalRMSAGC.update g_next=target/rms(q) 漏 g_current）、`_channel.py:97-169`+`_p07_runner.py:101-103`（每 window 独立 seed 独立 gg_block）+ sc_nda_ml_sim.py:108/`_equalizer.py:5-15`/`_a4_switch_common768_30seed.py:97-107`（scale-dependent 函数清单：blind h 加性噪声底 1/(2γ)、amp_limit 固定 thresh 3.0、decide 含 1/(2·gamma_lin)）+ thesis-lessons TL-30~33 + sim-preflight rules/mve-validation.md（consistency≠correctness）
> 触发原话: 用户 P07-R 执行指令（"P07 当前科学结论不得继续使用...分别建立最小失败测试...必须保存修复前失败证据。不能一边改一边猜。"）

### 决策

冻结旧 P07 科学结论（`NO_DIAGNOSTIC_METHOD_SIGNAL` 及其 Phase A/B/C 数字、clipping–resolution 折中"真实存在"声称、harvest 全部作废），campaign `accepted_valid_packages` **7→6**，`current` = **P07-R**，P08 暂停；旧 artifacts 保留并标 **INVALIDATED**（不覆盖、不删除）。修复后若科学有效完成再恢复 7/10，若仍 EXECUTION_INVALID 则保持 6/10。

### 理由（三根因，已最小失败测试复现，证据存 `p07r_prefail_evidence.json`）

1. **H1 SCALE（致命）**：`_p07_adapters.quantize_iq` 返回 `q = code·step = Q(g·z)`，但 `_p07_runner._per_window_receiver_outputs`（`:118`）和 `_p07_batch._receiver_on_raw`（`:86`）把 `q` **直接**喂给冻结接收链，**未除以 g**。g 是接收机已知控制量（不是 oracle），正确链应喂 `q/g`。下游 `estimate_h_blind_perblock`（`sc_nda_ml_sim.py:108` `h_blk = p_rx − 1/(2γ)`，加性噪声底不随 g² 缩放）、`amp_limit`（`_equalizer.py:5` 固定 `thresh=3.0` 绝对幅度 clip）、`decide`（`_a4_switch_common768_30seed.py:106` `mean(|rx|²) − 1/(2·gamma_lin)`）是 **scale-DEPENDENT** 函数，g≠1 不可被事后 /g 恢复。复现：g=2.0@13dB OLD 链 selected_errors 偏差 +44/+62、selector choice 从 da 翻成 nda；**corrected 链 q/g 精确恢复 g=1 参考（mismatch=0/0，choice 不变）**。旧 Phase-0 G3 float-bypass identity 门**只在 g=1 测过**（`FixedGainAGC(g=1,W=64)`），从未测 g≠1 → 门本身漏审。
2. **H2 CONTROL**：`CausalRMSAGC.update`（`_p07_adapters.py:182`）用 `g_next = clamp(target_rms / rms(q_past))`，**漏乘 g_current**。正确增量形式 `g_next = clip(g_current · target_rms / rms(q_past), g_min, g_max)`（因 rms(q_past)=g_current·rms(z) → rms(z)=rms(q_past)/g_current）。两种形式常数输入定点不同：CURRENT √(target/r0)=1.0954 vs CORRECTED target/r0=1.2000；deployed lam=0.9 把 output RMS 驱动到 0.230（target 0.3），**target 错对象（output scale 非 input scale）**。
3. **H3 LIFECYCLE**：`_p07_runner.py:101-103` 每 window 用独立 seed（`ws=start+b`）调 `generate_shared_realization_apsk`，`_channel.py:150` `h=gg_block(...)` 块间独立 Gamma 抽样 → **无共享 stateful trajectory**。经验 lag-1/2/5/10 GG 幅度 ACF = −0.042/+0.003/−0.063/−0.082 ≈ 0，与合同声称的时间相关 ρ 矛盾。AGC"预测下一 window 尺度"实为预测独立抽样 → **不构成时间相关 GG 控制问题**。`_gg_time.py` 的 stateful AR(1) 生成器存在但未被 P07 使用。

### verifier 盲区（为什么 V071 10/10 ACCEPT 仍漏）

V071 全部 10 项查的是 **consistency**（float-bypass identity 在 g=1、raw→aggregate 复算、信息边界 AST、seed 隔离、冻结文件未改）——这些全过，但**没查算法物理正确性**。命中 sim-preflight `rules/mve-validation.md` 警告："consistency bit-exact PASS 但算法是错的"（NDA-ML D-008 同病）。G3 float-bypass 门只在 g=1 验证 = 测试用例覆盖不到 bug 触发条件（g≠1）。V072 必须沿调用链查 q=Q(gz)→q/g 数学、下游 scale-dependent 函数、causal AGC 递推、trajectory lifecycle、经验 ACF、clip/quant 分解，不能只查 frozen contract。

### 排除的替代方案

- **不直接改旧 p07_*.py 隐藏错误**：新建 `p07r_*` 版本化文件，旧 artifacts 标 INVALIDATED 保留审计。
- **不靠 verifier 链式标记判断正确性**（TL-21）：用确定性最小失败测试复现根因。
- **不在修复前宣布任何科学结论**（TL-23 冷静期）：先冻结旧结论、回退计数，修复重跑有效后再恢复。

### 影响范围

- `topic-index.md` control block：`accepted_valid_packages` 7→**6**、`current_package` P08→**P07-R**、P08 暂停；rolling_queue P07 标 INVALIDATED_PENDING_RERUN。
- `verifications.md`：追加 V072（取代 V071 科学层结论）；V071 保留标"合同一致性通过但物理正确性漏审"。
- 旧 artifacts `projects/simulation/results/p07_agc_adc_dynamic_range/*` 加 INVALIDATED 标记（不删不改）。
- 新 artifacts 路径 `projects/simulation/results/p07r_agc_adc_repair/`、新脚本 `p07r_*.py`。
- protected owner/formal/Skill/thesis framework/controller 不改、无 push。MDE=0.15 dB 维持（无预先登记理由不改）。

### 来源

用户 P07-R 执行指令 + `p07r_prefail_evidence.json`（三根因最小失败测试）+ 源码逐行核 + thesis-lessons TL-30~33 + sim-preflight rules/mve-validation.md

## D047: P08 coded-chain 场景扩展授权（scope-change）—— 建立 source-auditable 最小真实 coded baseline，运行 G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL

> status: active
> date: 2026-08-01
> 取代：无（新增 scope-change 授权；不取代 D046，D046 P07-R 终态维持）
> 被取代：无
> 依据: 用户原话"行"（voice.md 2026-08-01，授权 coded-chain 场景扩展）+ 源码事实核查（subagent 确认：仓库无 parity-check matrix/syndrome/BP/min-sum/encoder/decoder；`run_sdfec_eval.py` 只读旧 BER 与门限比、无 encode/decode；`soft_demap.py` 有 16QAM max-log LLR+identity；`gmi.py` 仅 evaluator 非 decoder；C12/F4 oracle 路径用 TX-truth 非 deployable；dual-pol generator 内部生成随机 uncoded bits 无 codeword 注入接口）+ D045 §撤回旧 P07-entry H（coded chain blocked，P05-D 撤回无真实 codec）+ FR-23（问题驱动非空白驱动）+ TL-13/TL-22/TL-23
> 触发原话: 用户"行"（voice.md 2026-08-01，授权 P08 coded-chain 执行指令的 scope-change）

### 决策

授权 P08 coded-chain 场景扩展。范围变更：

- **原范围**：pre-FEC / 无真实 codec 的 diagnostic method factory（P01-P07 全在此范围，coded chain 一直 blocked）。
- **新范围**：允许建立一个来源可审计（source-auditable）的最小真实 coded baseline（优先 DVB-S2 LDPC component rate 2/3 / 16QAM-BICM；若只实现 LDPC 而无 BCH/rate matching 必须称"DVB-S2 LDPC component"禁止称完整 DVB-S2 FEC），并运行 P08-P10 coded-layer package。
- **明确不含 / 禁止**：阈值模型冒充译码；随机玩具 LDPC 冒充标准码；TX-truth LLR 进 deployable decide；未验证 codec 结果写入论文；凭记忆手写 DVB-S2 parity matrix；用临时随机 H；用 pyldpc 随机生成码后称标准码；仅凭包名认定实现正确；为方便悄悄换码率或帧长。

P08 family = `G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL`（**新机制族 G，区别于已关闭 A/B/C/D/E/F**）。M=冻结 16QAM receiver 用标准 max-log LLR 配单一 receiver-visible 全局噪声尺度；C=GG/SOP/接收机残差使等化符号误差呈异方差/非高斯，有限码长 soft LDPC/min-sum 对 LLR 置信度敏感；A=单一 AWGN 尺度可能使 LLR 过/欠置信，增 FER、迭代数或所需 SNR。

runtime 合法信息：equalized symbol / 已知 pilot / AGC-receiver metadata / calibration prefix / 严格过去的 decision residual / decoder convergence-iteration（只在其自然时序内）。禁止 runtime 信息：TX bits / true h-theta / 全 scored window 事后 residual / oracle affine / test-label fitting / future frame / CRC 翻标签路线。TX truth 仅用于 BER/FER/NLL/GMI scoring。

baseline ladder（全方法同码/同 interleaver/同 decoder/同 iteration budget/同 LLR clipping/同 receiver/同 paired realization/同 net rate）：B0 uncalibrated receiver-visible max-log LLR；B1 dev-only global scalar temperature scaling（最强便宜传统 comparator，独立调谐）；B2 dev-only global LLR clipping + decoder normalization/offset tuning（防 decoder 常规调参包装成新方法）；Oracle TX-truth/per-symbol residual 仅作 scoring/headroom 上界，只 Kill 不 Go，不进 deployable decide。

### 理由

1. P05-D/P07-H 撤回 coded chain 的唯一障碍是"无真实 codec"，不是"coded 问题本身无科学价值"。用户授权建立 source-auditable 最小真实 coded baseline 即解锁该障碍（非空白驱动，是移除已知 blocker）。
2. source-code 事实核查（subagent）确认仓库零 coded 基础设施，必须从外部来源引入标准码——这正是 Phase 0A 标准码来源门的职责。
3. coded-LLR-calibration 是与 A-F 正交的新机制族（作用点是 LLR 置信度校准，非 selector/定点/OOD/在线适配/历史信息/AGC），满足 D039 §"至少 5 机制族"。
4. claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：METHOD_SIGNAL 只登记 pre-formal carrier，不直接宣称正式论文方法；后续需 promotion preflight + GW Step 1–3/3.5/4a。

### 影响范围

- `topic-index.md` control block：epoch 73→74，current_package=P08（执行中），families_started 追加 G，same_family_consecutive=0（新族），next_legal_action 更新；新增 allowed `CODED_CHAIN_BUILD`。
- campaign 计数：P08 有效科学完成才 accepted_valid 7→8；CODED_BASELINE_SOURCE_UNAVAILABLE / CODED_CHAIN_IDENTITY_UNAVAILABLE / EXECUTION_INVALID 不计 P08。
- P09 只准备不运行：若 P08 METHOD_SIGNAL → P09 做 promotion preflight/strong evidence；若 LLR 问题被传统方法解决 → P09 选 coded operating-boundary 或 receiver-ranking 但须重新过 problem gate；若 coded identity blocked → P09 不得启动。
- protected owner/formal/Skill/thesis framework 不改、无 push。MDE=0.15 dB 维持。
- D046 P07-R 终态（PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION，F 族关闭，7/10）维持不变。

### 排除的替代方案

- **不退回 BER threshold 冒充 FEC**（D045 撤回 P07-H 已裁决 threshold eval 非 FEC）。
- **不用随机 LDPC 冒充标准码**（用户指令明禁 + FR-20 关键参数溯源）。
- **不跳过标准码来源门直接用任意 codec**（Phase 0A 是硬门控）。
- **不把 P08 coded-chain 当论文正式方法**（METHOD_SIGNAL 只产 pre-formal carrier）。

### 来源

用户"行"（voice.md 2026-08-01）+ P08 coded-chain 执行指令 + 源码事实核查 subagent + D045/D046 + FR-23/TL-13/TL-22/TL-23
