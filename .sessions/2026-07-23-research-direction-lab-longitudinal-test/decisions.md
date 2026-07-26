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

> status: active
> date: 2026-07-26
> 取代：D005（只取代“无 active carrier / 仅 remap”的当前动作；T009 拒收、A4 回池与 no-second-repair 事实保留）
> 被取代：无
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
