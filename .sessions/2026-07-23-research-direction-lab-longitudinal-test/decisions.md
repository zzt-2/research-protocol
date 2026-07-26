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

> status: active
> date: 2026-07-26
> 取代：无（只修改运行与协作模式，不取代 D003/formal D015 的科学选择）
> 被取代：无
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

> status: active
> date: 2026-07-27
> 取代：D015
> 被取代：无
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
