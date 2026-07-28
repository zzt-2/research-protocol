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

> status: active
> date: 2026-07-28
> 取代：D029 的 Step 3 workline
> 被取代：无
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
