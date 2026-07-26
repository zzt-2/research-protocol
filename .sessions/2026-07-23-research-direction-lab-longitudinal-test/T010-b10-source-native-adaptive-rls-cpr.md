# Task Brief: B10 source-native adaptive pilot-RLS CPR

> 来源: S001（live D010 / R002 / formal D021）
> 产出位置: `projects/thesis-fso/worker-logs/step-010-b10-source-native-adaptive-rls-cpr.md`
> 日期: 2026-07-26
> 唯一文档: executor 只需本 T、其中明确列出的仓库源码与共享论文文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 23
  action_class: METHOD_CONSTRUCT
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

---

## 0. TL;DR

你在
`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，当前 formal
阶段是 **Groundwork Step 4a 维度 D**。

**任务**：从 B10 2024 原文重新实现 **estimator source-native** fixed
pilot-RLS；只有 identity smoke 全过才同包实现并比较 innovation-gated update 与
bounded adaptive forgetting，判断是否形成论文可包装的方法信号。`source-native`
只描述 B10 estimator 的 pilot/RLS/DD 身份；星地 2.5 GBd GG primary 是显式
`SOURCE_TRANSFER`，不得冒充 B10 原生光纤系统复现。

### 0.1 Phase-B amendment（2026-07-26，owner D008 / formal D019）

初次 Phase-B `BLOCKED_IDENTITY` 已被独立科学 verifier 以
`SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID` 拒收，不得作为 B10 身份失败：

- 旧合同在 `r=s·exp(+jφ)+n`、`exp(-j predicted)` 去旋约定下使用了相反的
  operational residual；
- runner 硬编码无 source 依据的 `λ=.999`，不能承担 identity Kill；
- seed `130001` 已用于失败定位和反事实诊断，只是 invalid-development evidence。

本 amendment 只授权一次同包 Phase-B confirmation：

1. residual 固定为
   `angle(derotated_received * conj(hard_decision))`，desired phase 为
   `predicted_phase + residual`；
2. source-only `λ=.99` 固定标为
   `IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN`；它不是论文参数、primary
   tuning 或方法信号；
3. 原 artifact 保留为 `source-smoke-invalid-v1.json`；seed `130002` 只作既有
   canonical/RNG test，不作性能证据；使用仓库 exact-token 零命中的 confirm seed
   `130003` 重跑完全相同的 1/10 GHz smoke，输出新 `source-smoke.json`；
4. control/formal/task amendment 必须先独立审查；confirm 通过仍需独立科学
   verifier 与新的递增 control 才能进入 Phase C。confirm 失败即轮换，不得再改
   sign、`λ`、seed 或补第二个 B10 repair/package；
5. 执行前新增 synthetic residual-direction regression；seed `130003` 的实际
   1/10 GHz BER gate 是唯一 confirm，派发前禁止预跑。confirm PASS 后必须返回
   `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 并停止；
6. confirm 前迁移 `source-contract.yaml`：
   - `authority.formal_decision` 改为 formal D019；
   - 旧 run 记为 `SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID` 历史，并指向
     原样保留的 `source-smoke-invalid-v1.json`；
   - current confirm 状态设为 pending，固定 operational residual、source-only
     `.99` 类型与 seed `130003`；
   - 新 `source-smoke.json` 只能由唯一 confirm 写入，禁止覆盖 invalid history。

### 0.2 Phase-C authorization（2026-07-26，owner D009 / formal D020）

V012 已独立接收
`SOURCE_IDENTITY_PASS / PHASE_B_CONFIRM_ACCEPTED`（P0=0/P1=0/P2=3）；
`mission_method_delta=NONE`。epoch 20 只授权分段 Phase C：

1. **C1 implementation/tests（≤15 min，不消费 validation）**：
   - 起飞时按以下精确 schema 迁移 `source-contract.yaml`：
     - `authority.formal_decision` =
       `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D020`；
     - `source_native_identity.phase_b_status` =
       `SOURCE_IDENTITY_PASS_ACCEPTED`；
     - `source_identity_smoke.initial_run.*` 和
       `source_identity_smoke.current_confirm.*` 全部作为 confirm-time immutable
       history 原样保留，包括 `current_confirm.status=PASS_AWAITING_SCIENCE_REVIEW`
       与 `current_confirm.phase_c_authorized=false`，不得覆写历史；
     - 新增根级 `current_authorization`：
       `formal_decision=.../decisions.md#D020`、
       `phase_c_status=C1_AUTHORIZED_NO_VALIDATION`、
       `validation_authorized=false`、`heldout_authorized=false`、
       `mission_method_delta=NONE`；
   - `run_source_smoke()` 在 current PASS artifact 已存在时必须立即拒绝，测试证明
     不生成 realization；
   - read-only gate 重算 artifact 中可重算的 BER/Q²/CFO/gates；finite/switch/freeze
     原值未落盘，必须标 `LEGACY_NON_RECOMPUTABLE_PHASE_B_P2`，禁止事后伪造；
   - 实现 P2/P3、amplitude-only cheap rule、4OPM+BPS 与 4OPM+DD-DPLL；
   - 完成 direct information-increment、no-truth、shared-realization、comparator
     frequency-responsibility 与 clean/noiseless sanity tests；
   - 不调用 validation/test seeds，不产生 validation artifact。
2. C1 完成后返回 `PARTIAL_C1_AWAITING_REVIEW` 并停止。独立 review PASS 后才允许
   **C2 validation freeze**。
3. **C2 validation freeze（每 turn ≤15 min）**：只用 `131001–131005` 按预注册
   Cartesian order生成 raw；若需续 turn，只追加未运行 rows，全矩阵完成前不得选
   参数。完成后冻结 P1/P2/P3/cheap/B* 与每个 GG 档最多 3 个相邻 SNR 点，返回
   `PARTIAL_C2_AWAITING_SCIENCE_REVIEW` 并停止。
4. Phase D/held-out/test seeds 始终未授权；C2 独立科学验收与新的递增 control
   是进入 Phase D 的必要条件。

### 0.3 C2 validation authorization（2026-07-26，owner D010 / formal D021）

V021 已独立接收 C1 为 `C1_IMPLEMENTATION_CONTRACT_PASS`
（P0/P1/P2=`0/0/1`）；唯一 P2 是不可事后补造的 pre-C1 immutable snapshot
债务。`mission_method_delta=NONE`。V022 首次起飞审查以 P0/P1/P2=`0/3/1`
拒绝派遣；以下 amendment 精确补齐 checkpoint、SNR freeze 与归一化合同。
V023 新增的 B* exact-tie P1 随后补齐；V024 第三轮以
P0/P1/P2=`0/0/1` 批准 amendment。epoch 23 只在最终 binding 独立复核 PASS 后
授权 C2：

1. 起飞时把 `source-contract.yaml` 迁移为：
   - `authority.formal_decision` =
     `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D021`；
   - `current_authorization.formal_decision` 同上；
   - `current_authorization.phase_c_status=C2_AUTHORIZED_VALIDATION_ONLY`；
   - `validation_authorized=true`、`heldout_authorized=false`、
     `mission_method_delta=NONE`；
   - 新增 `phase_c1_acceptance`，精确记录
     `verification=.../verifications.md#V021`、
     `status=C1_IMPLEMENTATION_CONTRACT_PASS`、`p0=0`、`p1=0`、`p2=1`、
     `legacy_debt=PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT` 和
     `mission_method_delta=NONE`；
   - `source_identity_smoke.initial_run.*`、
     `source_identity_smoke.current_confirm.*` 与
     `phase_c1_method_contract.*` 原样保留，禁止借迁移覆写 Phase-B/C1 历史。
2. 派遣复审前，`contract.yaml` 必须是 `phase=C2`、
   `execution_status=C2_DISPATCH_CONTRACT_AWAITING_REVIEW`；
   `authorization.validation=false`、`heldout=false`、
   `performance_conclusion=false`。独立派遣复审 PASS 并由主控更新递增 control
   后，executor 起飞时只把
   `execution_status` 改为 `C2_VALIDATION_AUTHORIZED`、
   `authorization.validation=true`，其余 C2 合同不得改变。C2 可生成 validation
   raw/aggregate 和冻结设置，但不能给正式性能或方法 verdict。
3. **精确 validation 参数网格、setting index 与单位**。所有扫描值均为
   `UNVERIFIED_PROJECT_DECLARED_RANGE / PREREGISTERED_C2_GRID`，不是文献最优：
   - `arm_family_index=0 / P1_FIXED`：setting `0,1,2` 分别为
     dimensionless forgetting factor `0.98,0.99,0.999`；
   - `arm_family_index=1 / P2_INNOVATION_FREEZE`：setting `0..8` 按
     forgetting factor major、threshold minor 排列
     `[0.98,0.99,0.999] × [0.05,0.11,0.20]`。threshold 是 dimensionless
     normalized innovation，逐 DD symbol 在更新前计算
     `abs(desired-h^T x)/sqrt(max(lambda_base+x^T P x,1e-15))`；`1e-15`
     只是固定 numerical finite guard，不是 validation tuning；P2 的
     `lambda_base=forgetting_factor`，只决定当前 update 是否冻结；
   - `arm_family_index=2 / P3_BOUNDED_ADAPTIVE_FORGETTING`：setting `0,1,2`
     按下列 tuple 原顺序，不做隐含 Cartesian 扩展：
     `(lambda_min,lambda_max,ema_alpha,innovation_scale)` =
     `(0.95,0.999,0.20,2.0)`、
     `(0.98,0.995,0.10,1.0)`、
     `(0.99,0.999,0.10,1.0)`。四项均 dimensionless；当前 innovation 的
     `lambda_base=lambda_max`，`lambda_k` 只依赖更新至 `k-1` 的 EMA；
   - `arm_family_index=3 / CHEAP_AMPLITUDE_FREEZE`：setting `0..8` 按
     forgetting factor major、threshold minor 排列
     `[0.98,0.99,0.999] × [0.10,0.20,0.40]`。threshold 是 Es=1
     Gray-16QAM 接收机链上的 dimensionless raw receiver amplitude
     `abs(derotated_received)`；无 AGC、无按 frame/cell/seed 归一化；
   - `arm_family_index=4 / 4OPM_BPS`：setting `0,1,2` 为 window
     `31,63,127 symbols`，每项 exactly 32 test phases；
   - `arm_family_index=5 / 4OPM_CONTINUOUS_DD_DPLL`：setting `0,1,2` 为
     `omega_n=4e6,8e6,20e6 Hz`；8e6/20e6 只作 project WARNING/既有 sweep
     anchor，不能冒充本场景文献值。
4. **精确运行顺序**：
   `GG=[weak,moderate,strong]` →
   `EsN0=[14,17,20,23,26] dB` →
   `seed=[131001,131002,131003,131004,131005]` →
   arm/settings 按第 3 条书写顺序。canonical row key 固定为五整数数组
   `[gg_index,snr_index,seed_index,arm_family_index,setting_index]`，每个 index
   都是上述冻结列表的零基索引。按 GG→SNR→seed→arm→setting 的 lexicographic
   顺序预先生成完整 `expected_row_keys`，长度必须精确为 2250；不得用字符串排序
   或运行结果决定顺序。每个 `(GG,EsN0,seed)` 只生成一次 shared realization，
   所有 30 个 arm/settings 消费同一对象。共 75 realization cells、2250 raw rows。
5. **shared realization 与归一化合同**：
   - `gg_method=gar`，`block=100 symbols`，GG intensity
     `h=X*Y` 的理论边缘均值为 1；有限 frame 的 sample mean 不重归一；
   - field amplitude 只取 `sqrt(h)`，不对 fade 后 waveform 做功率补偿；
   - Gray 16-QAM 使用 `qam16_mod`，未衰落发射星座平均
     `E_s=E[|s|^2]=1`；
   - electrical `gamma=10^(EsN0_dB/10)` 参照上述未衰落 `E_s=1`；
     complex circular AWGN 固定为
     `n=sqrt(1/(2*gamma))*(N(0,1)+j*N(0,1))`，故
     `E[|n|^2]=1/gamma`；
   - 禁止 AGC、按 realization/cell/seed 的 waveform/noise/h/sample-power
     renormalization，禁止按 realized `mean(h)` 调整 noise。
6. **checkpoint/resume identity 与原子保存**：
   - 只在一个 30-row realization cell 全部完成后 checkpoint；合法累计 row 数
     只能是 `0,30,...,2250`；
   - resume 时先重新生成完整 2250-key `expected_row_keys`。现有 rows 的 key
     必须唯一、无 gap，且逐项精确等于
     `expected_row_keys[:len(rows)]`；每个连续 30-row group 必须共享同一前三个
     cell index 并完整覆盖第 3 条的全部 arm/settings。任一不符返回
     `BLOCKED_STALE_OR_CORRUPT_CHECKPOINT`，不得修补、跳行或重跑覆盖；
   - 首次 checkpoint 前，以文件原始 bytes 的 SHA256 冻结 exact hash map：
     本 T、`source-contract.yaml`、`contract.yaml`、`pilot-manifest.json`、
     `seed-census.yaml`、`shared_realization.py`、`source_native_rls.py`、
     `methods.py`、`baselines.py`、`run_all.py`、`projects/simulation/params.py`、
     `common/_config.py`、`common/_modulation.py`、`common/_gg_time.py`、
     `common/_channel.py`、`common/_recovery.py`、`common/_experiment.py`。
     `validation-raw.json` 每次都保存完整 map；resume 必须 exact-match，否则
     `BLOCKED_STALE_OR_CORRUPT_CHECKPOINT`；
   - 每次 append 前保存既有 rows 的 canonical JSON SHA256，append 后证明既有
     prefix deep-equal 且 SHA 不变；禁止修改或覆盖任何 existing row key；
   - 原子保存只允许隔离 `run_all.py` wrapper：在目标同目录创建唯一临时文件，
     先调用 `save_results(payload,temp,...)` 注入元数据，再 flush + `os.fsync`
     临时文件，最后 `os.replace(temp,validation-raw.json)`；支持目录 fsync 的平台
     再 fsync parent directory，不支持时在 artifact 记录
     `directory_fsync=UNSUPPORTED_PLATFORM`。异常时删除临时文件并保留旧 target；
     禁止修改 shared `common/_experiment.py`；
   - 全 2250 rows 完成前不得生成 aggregate、查看局部排名、选择设置或改变网格。
7. **全局 setting freeze 规则**：
   - 对每个 arm family，以 75 个 validation cells 的同分母 rows 按以下固定
     lexicographic score 选一个全局设置：
     `(nonfinite_rows, BER>=0.2_rows, outage_rows_at_3.8e-3,
     total_bit_errors, preregistered_setting_index)`，全字段从小到大；
   - P2、P3 分别冻结；cheap、P1、BPS、DPLL 分别冻结；
   - conventional `B*` 在已全局冻结的 BPS/DPLL 两臂间用同一 score 选择；
     若完整 score exact tie，则按预注册 conventional arm index
     `BPS=0,DPLL=1` 选择 BPS。该 tie 只按派遣前固定顺序，不表示 BPS 有性能优势；
   - primary method arm 在已冻结的 P2/P3 两臂间用同一 score 选择，tie 固定选
     P2；另一个臂仍完整保留且 Phase D 不得按 cell/seed 替换主臂；
   - score 只用于 validation freeze，不构成 `METHOD_SIGNAL` 或 held-out claim。
8. **每个 GG 档的 SNR freeze**：
   - 使用已冻结的 primary method、P1、cheap 与 B* 的 validation pooled raw BER；
   - 每个 arm/SNR 的 pooled raw BER 固定为
     `sum(bit_errors)/sum(denominator)`；若 pooled errors=0，仅为 log-distance
     定义 `effective_BER=0.5/sum(denominator)`，否则
     `effective_BER=pooled_raw_BER`。不得加任意 epsilon；
   - 正常方向共同 bracket 的精确定义：同一相邻 pair `(i,i+1)` 上，四臂各自都
     满足低端 `pooled_raw_BER>3.8e-3`、高端
     `pooled_raw_BER<=3.8e-3`。等号只算高端；低端等号不成 bracket；
   - 对每个合法共同 pair，目标为四臂×pair 两端的
     `max(abs(log10(effective_BER/3.8e-3)))`；按
     `(objective,lower_snr_index)` 从小到大选唯一 pair；
   - 为已选 pair 枚举所有包含它的连续 3-point window；window 目标为四臂×三点
     的同一 max-log-distance，按 `(objective,window_start_index)` 选唯一 window；
   - 若不存在共同 bracket，对三个可能的连续 3-point window 全部计算同一
     max-log-distance，按 `(objective,window_start_index)` 选唯一 window，并标
     `NO_COMMON_VALIDATION_CROSSING`；该 GG 档以后不得触发 Q²
     `METHOD_SIGNAL`，只能作 raw BER/outage/boundary。
9. C2 artifact 必须继续显式携带
   `legacy_debt=PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT`，不得补造 pre-C1 snapshot，
   也不得用该债务扩大或否定 C2 结论。
10. C2 完成后只返回 `PARTIAL_C2_AWAITING_SCIENCE_REVIEW` 并停止。不得运行
   test seeds `132001–132010`、Phase D、held-out、Step 5/Contract/Execute，
   不得 commit/push 或更新 owner/mission-log。

**产出**：隔离实现、tracked raw/aggregate artifacts、定向 tests、synthesis 和
worker-log；一次 consolidated commit，不 push。

**最高纪律（违反任一条即废）**：

1. T006 只作失败 fixture；不得复制其稀疏 pilot、非星座 pilot、早退 DD、P reset、
   post-channel pilot 重构或 TX-truth resolve。
2. 前 128 个 symbol 必须是独立冻结、接收端可重建的连续 16-QAM pilot manifest；
   pilot 与 data 必须在 TX 侧进入同一物理 channel/noise realization。
3. deployable arm 不得读取 runtime TX payload、bits、true phase/CFO、future samples
   或 post-hoc ambiguity label；oracle 仅作 bound。
4. source smoke 已由 V012 接收，C1 已由 V021 接收；当前只按 §0.3 运行 C2
   preregistered validation comparison。禁止重跑 smoke、消费 test seed、运行
   held-out/Phase D 或把 smoke、测试 PASS、代码创建、evaluator 修复、局部
   validation 排名记为方法信号。
5. 只改本 T 授权的隔离路径；不改 `common/`、`params.py`、旧 T006/T008/T009、
   paper、formal/current/mission owner、Skill 或 protected history。

---

## 1. 起飞检查

### 1.1 control 与阶段

运行：

```powershell
python C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py `
  .sessions\2026-07-23-research-direction-lab-longitudinal-test\T010-b10-source-native-adaptive-rls-cpr.md
```

必须 PASS。随后核对：

- `projects/thesis-fso/master-state.md`：current step 为 GW Step 4a、carrier=B10；
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D021`；D017–D020 只作
  superseded 历史血缘，不能通过 stale-control check；
- 本包不进入 Step 5/Contract/Execute。

任一不一致：返回 `BLOCKED_STALE_CONTROL`，不写代码、不跑实验。

### 1.2 必读与来源

完整读取：

1. 本 T；
2. live `R002-post-t009-carrier-remap.md`、D010/V021 与 formal D021；D009/V012/
   D020 是 Phase-B→C1 历史血缘，D008/V008/D019 是 Phase-B repair 历史血缘；
3. `stages/groundwork.md`、`stages/gw-feasibility.md`；
4. `thesis-lessons.md` 速查及 TL-20/22/23/25–33；
5. `code-quality.md`；
6. `.agents/skills/sim-preflight/SKILL.md` 与
   `rules/constraints.md`、`rules/mve-validation.md`、`rules/param-source.md`、
   `rules/doc-discipline.md`、`rules/usage-log.md`、`rules/adaptation-scan.md`；
7. `projects/simulation/params.py`，运行 `audit_params(SimulationConfig())`；
8. `projects/thesis-fso/literature_notes.md` 的 L20、B10-Q1/Q2；
9. 主仓库共享论文：
   - `D:\code\study\research-protocol\papers\doi\10.1007_s11107-024-01019-2\metadata.json`
   - 同目录 `source.pdf`（核心公式与 Fig. 1 的最终权威）
   - 同目录 `content.md`
   - `D:\code\study\research-protocol\papers\_read_notes\_B10-16qam-pilot-rls-increment.md`
   - `D:\code\study\research-protocol\papers\doi\10.1016_j.optcom.2024.130981\source.pdf`
     与同目录 `content.md`（只支撑 2.5 GBd 星地下行 `SOURCE_TRANSFER`；
     原文调制为 PM-QPSK，不支撑 16-QAM source identity）
   - `D:\code\study\research-protocol\papers\_read_notes\_B5-short-time-spectrum-cfo-increment.md`
     L100–102（记录手工 PDF 落盘；该 DOI 的 `metadata.json` 仍为 stale failed，
     不得让 metadata 覆盖已存在的 PDF/content 事实）
10. 失败资产：
    - `projects/simulation/explore/high-order-cpr-combination/`
    - `projects/thesis-fso/worker-logs/step-006-high-order-cpr-combination-method.md`
    - formal V001。
11. 邻近方法先例元数据（只证明方法族先例，不是公式来源）：
    - `D:\code\study\research-protocol\search-archive\2026-06-22\satellite-optical-equalization-residual.json`
      中 DOI `10.1109/ICAIT66450.2025.11353303` 的 ASFRLS-CMA；
    - `D:\code\study\research-protocol\search-archive\2026-05-31\phase-locked-loop-adaptive-bandwidth-deep-fading-carrier-tra.json`
      中 DOI `10.1016/J.CJA.2015.05.001` 的 innovation-adaptive carrier tracking。

`audit_params` 当前允许存在与本包无关的 4 个 CRITICAL；本包不得消费
`kf.Q_fine_df` 或三个 `kf.q_params_*.sigma2_turb`。全局
`SystemParams.R_SYM` 的 `10.1109/JLT.2025.xxx` 是无效占位来源，本包也不得消费；
2.5 GBd 必须从 `B5Params.R_SYM_B5` 读取并标
`SOURCE_TRANSFER / PM-QPSK source, applied to 16-QAM transfer test`。实际用到的
每个物理参数必须在新 contract 中逐项写 `source/type/value/unit`；查不到文献的
扫描轴按 FR-20 写 `UNVERIFIED_PROJECT_DECLARED_RANGE`，不能伪装成 literature。

邻近先例均只在公开摘要级闭合：前者支持“卫星 RLS 自适应遗忘因子”，后者支持
“低 SNR 载波跟踪的 innovation adaptive control”。不得从摘要臆造精确映射，
不得声称 P2/P3 是上述论文的 source-native 实现，也不得声称首创 adaptive
forgetting 或 innovation control。

### 1.3 理论预期与否决条件（编码前写入 contract）

先写：

- **机制假设**：GG 深衰落/低 SNR 提高 DD decision error，使 fixed RLS 以错误
  residual 更新；receiver-visible normalized innovation 可识别这些更新，冻结或
  有界调整 `λ` 能减少发散。
- **预期方向**：P2/P3 的优势应集中在 moderate/strong GG 或低 SNR，不应在
  clean/high-SNR 无故大幅领先；若 clean 也巨幅领先，先查实现或 comparator。
- **物理时间尺度**：`f_G=100 Hz → τ_c≈1.59 ms`；2.5 GBd 下一个 25,000-symbol
  frame 约 10 μs，GG 在帧内近慢变。不能把结果解释为跟踪 ms 级湍流动态，只能
  解释为 fade-conditioned DD robustness。
- **否决条件**：
  1. 原文 1/10 GHz positive-CFO smoke 不能闭合；
  2. P1 不是 128 contiguous pilot→DD 或需 TX truth 才工作；
  3. primary 没有合法 BER working region或 conventional comparator 不可复现；
  4. P2/P3 只赢 P1 但输 amplitude-only cheap rule 或 conventional B*；
  5. 正信号只来自单 seed、post-hoc cell、无 crossing proxy dB 或 source-transfer
     stress-only 条件。

### 1.4 同一执行包的 ≤15 分钟分段

T010 是一个科学执行包，但不得把“一包”解释成一次超长子 agent 调用。主控使用
同一内部 executor 的连续 follow-up turn（必要时换 executor，但保持本 T 与共享
worktree），每个 turn **硬上限 15 分钟**；到时必须在安全点停止并回传阶段回执，
不得用阻塞等待跨过上限。各段共享未提交工作，只有整个 T010 收口时做一次
consolidated commit：

1. **Phase A — source/contract/TDD（≤15 min，不跑科学实验）**：核对 PDF 公式，
   写 source/experiment contract、pilot manifest、seed census 与先失败后通过的
   identity/metric 单元测试骨架。安全点：所有合同可解析，未运行 source smoke。
2. **Phase B — P1 identity（≤15 min）**：完成 shared realization 与 source-native
   fixed B10，只运行定向 tests 和 1/10 GHz source smoke。初次 run 已由 V008
   拒收；本轮只按 §0.1 固定合同在 confirm seed `130003` 重跑一次。任一 identity
   gate 失败即收口 `BLOCKED_IDENTITY`；通过返回
   `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 并停止，须独立科学验收与新 control
   才允许 Phase C。
3. **Phase C — methods + validation freeze**：严格按 §0.2 拆为 C1 与 C2；每个
   executor turn ≤15 min，C1 review PASS 前禁止 C2，C2 完成前禁止 held-out。
4. **Phase D — held-out + closure（≤15 min）**：只读取已冻结设置运行 test seeds，
   保存 raw/aggregate/result，完成重算、synthesis、worker-log、全套定向/回归检查
   与唯一 final commit。若预计本段超时，先停止在 raw 已完整落盘的安全点，下一
   ≤15 分钟 turn 只做 deterministic closure，不重选参数或重跑已完成 test。

阶段回执格式固定为：

```text
status: PARTIAL_CONTINUE|PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW|PARTIAL_C1_AWAITING_REVIEW|PARTIAL_C2_AWAITING_SCIENCE_REVIEW|BLOCKED|FAIL
phase: A|B|C|D
safe_point: <one line>
next_phase: <A|B|C|D|NONE>
anomaly: <NONE or one concise anomaly>
```

`PARTIAL_CONTINUE` 只表示同一 T010 尚未收口，不是新 package、method delta 或 formal
progress；主控不得据此更新 owner/mission-log。
`PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 只用于 Phase-B confirm PASS 后的强制暂停：
它触发中间独立科学验收，但仍不是 final receipt、CP010 或 method delta。§8 final
receipt 只触发整个 T010 的最终科学验收，不能替代 Phase-B→Phase-C 中间门。
`PARTIAL_C1_AWAITING_REVIEW` 与 `PARTIAL_C2_AWAITING_SCIENCE_REVIEW` 分别强制
阻断 validation 与 held-out；两者都不是 CP010、method delta 或 final receipt。

---

## 2. 授权文件边界

允许新增：

```text
projects/simulation/explore/b10-source-native-adaptive-rls-cpr/
  __init__.py
  source-contract.yaml
  contract.yaml
  pilot-manifest.json
  seed-census.yaml
  shared_realization.py
  source_native_rls.py
  baselines.py
  methods.py
  run_all.py
  synthesis.md
  artifacts/
    source-smoke-invalid-v1.json
    source-smoke.json
    validation-raw.json
    validation-aggregate.json
    test-raw.json
    test-aggregate.json
    result.json
projects/simulation/tests/test_b10_source_native_adaptive_rls_cpr.py
projects/thesis-fso/worker-logs/step-010-b10-source-native-adaptive-rls-cpr.md
```

允许按需要减少文件，不能把不同职责塞进一个巨型脚本。artifact 必须位于上述
tracked `explore/**/artifacts/`，并通过 `common._experiment.save_results()` 保存；
不得写到被 gitignore 排除的 `results*/`。

禁止修改：

- `projects/simulation/common/**`
- `projects/simulation/params.py`
- `projects/simulation/explore/high-order-cpr-combination/**`
- T008/T009 任意源码或 artifact
- `.sessions/**`（本 worker-log 路径除外，不在 `.sessions`）
- `projects/thesis-fso/master-state.md`、`projects-overview.md`
- `毕设/**`、`.agents/skills/**`、Direction Lab protected history

---

## 3. Source-native P1

### 3.1 冻结 pilot manifest

- 生成一次 512-bit、128-symbol 的合法 Gray 16-QAM pilot；写入
  `pilot-manifest.json` 的 bits、complex symbols、mapping、SHA256。
- manifest 必须独立于 runtime data RNG；receiver 只从该 manifest 取得 pilot，
  不能从 `shared["tx"]`、bits 或 true phase取。
- 每帧 symbol 0–127 全为该 manifest，128 之后才是 data；BER 分母只含 data。

### 3.2 Shared realization

新建隔离的 `generate_shared_b10_realization(...)`：

- 先构造 manifest pilots + independent random 16-QAM data，再一次性经过
  `r_k=sqrt(h_k)s_k exp(jφ_k)+n_k`；
- `φ_k=2πΔf kT_s + Wiener PN`；AWGN 在相位旋转后的信号上相加；
- 所有 arms 共用同一个返回对象、noise、GG envelope、phase、waveform 和 data mask；
- primary single-pol，不引入 SOP/Jones，避免把偏振问题混入 CPR；
- 复用 `qam16_mod/demod`、`gg_time_envelope` 与 params provenance；不复制到
  shared `common/`。

必须有 canonical-limit test：当 pilot manifest 关闭、SOP=0 且相同参数/seed 时，
局部生成器的 QAM mapping、GG envelope、noise variance 与 canonical
`generate_shared_realization_dp` 逐字段等价；若 RNG 排布使 byte-identical 不可得，
至少分解验证 bits/symbol mapping、GG、noise empirical variance 和 analytic
noiseless limit，且在 worker-log 说明差异。

### 3.3 RLS 生命周期

全链统一用 radians，索引约定写入 source contract：

- 训练 `k=1…128`：`x_k=[1,k]^T`，
  `y_k=unwrap(angle(r_k/s_k))`；
- `e_k=y_k-h_{k-1}^H x_k`；
- `κ_k=P_{k-1}x_k / (λ + x_k^H P_{k-1}x_k)`；
- `h_k=h_{k-1}+κ_k e_k`；
- `P_k=λ^{-1}(P_{k-1}-κ_k x_k^H P_{k-1})`；
- `h_0=[0,0]^T`、`P_0=0.5I`、`δ=2`；
- 训练结束一次冻结 `F=2π/h_{1,128}`；只跑 positive residual CFO，禁止擅自
  `abs(h1)`、P-norm reset 或首次非零 `h1` 即冻结；
- DD 期使用原文 periodic regressor，先预测/去旋/16-QAM hard decision，再以
  operational residual
  `angle(derotated_received * conj(hard_decision))` 更新 desired phase；无额外
  runtime pilot、无 truth reset。论文 Eq.(8) 的 literal 文本与 Eq.(1)/Fig.1 在
  当前正相位/负去旋约定下存在符号张力；D008/D019/V008 的 operational adjudication
  是本实现唯一合法约定，禁止恢复旧反号。

公式来源必须在 `source-contract.yaml` 和代码注释中逐项标注：Deka 等 2024
p.166 Eq.(3)–(6) 为 RLS 递推，p.166–167 Eq.(7)–(8) 与 Fig. 1 为
training→DD、周期 regressor 和 residual update；`F=2π/h_{1,128}` 是把原文
degree 表达全链一致地换成 radians 的实现约定。PDF/原页与提取笔记不一致时以
PDF 原页为准并 `BLOCKED_IDENTITY`，禁止靠文字描述补公式。

primary 的 `λ` 只在 validation 候选网格中选择并冻结。原文未给精确最优表，必须
标 `validation_tuned`，不能冒充 source parameter。source confirmation 例外固定
`λ=.99`，类型为 `IDENTITY_REPAIR_PREREGISTERED_AFTER_INVALID_RUN`；它只关闭
source identity，不进入 primary freeze，也不能触发方法或性能 claim。

### 3.4 Source identity smoke

source-only AWGN/control（非论文性能复现、非 thesis result）：

- 28 GBd、25,000 symbols、**electrical \(E_s/N_0=26\) dB**、
  linewidth 50 kHz；
- positive CFO 1 GHz 与 10 GHz；
- 同一 pilot manifest、P1 fixed B10、confirm seed `130003`、固定
  source-only `λ=.99`；
- 检查 CFO sign/relative error、finite state、training→DD 切换点、10 GHz
  phase-slope recovery、data BER/Q² 单调改善；
- 至少要求 P1 在两个 source cells 的 data BER 低于 HD-FEC `3.8e-3`，否则
  `BLOCKED_IDENTITY`，不进入 primary。

26 dB 只是预注册的高 SNR identity-smoke 数值，不是 B10 论文的 OSNR 性能点。
B10 原文报告的是 26 dB **OSNR**；由于缺少参考带宽、双偏振和噪声归一化换算，
禁止写 `OSNR/SNR` 或声称二者等价。由于未复现 SSMF/CD/PMD/SPM，禁止要求或
宣称逐图复现论文 Q-factor；smoke 只验证 RLS 身份和数量级。

---

## 4. P2/P3 与 cheap alternative

所有方法与 P1 byte-level 同构，只允许以下差异：

### P1 fixed

source-native B10，`λ` validation-frozen，作为方法同族主 baseline。

### P2 innovation freeze

- 只用当前/过去 receiver-visible normalized innovation；
- data symbol innovation 超过 validation-frozen threshold 时，输出预测相位但冻结
  当次 `h/P`；
- 不窥视 hard-decision 正误、true symbol、true phase、future residual；
- 用 pilot 时始终更新，但本 source-native lifecycle 只有最初 128 个训练 pilot。

### P3 bounded adaptive forgetting

- `λ_k∈[λ_min,λ_max]`；
- 只由 `k-1` 时刻或更早的 normalized innovation EMA 决定，防止同样本
  look-ahead；
- 映射单调、有界、validation-frozen；其余更新与 P1 相同；
- 不允许 P reset、truth clamp 或按 condition/test seed 单独选参数。

### Candidate-arm freeze rule

P2 与 P3 是两个分别预注册、分别评估的 candidate arms，不存在未定义的通用 `P`。
C2 必须先完成全部预注册 validation Cartesian matrix，再分别冻结 P2 与 P3 的
全局设置。禁止按 seed、GG/SNR cell 或观察到的结果在 P2/P3 之间取 best-of；若在
Phase D 前只选择一个主 method arm，必须依据完整 C2 矩阵和预注册的全局选择准则
一次冻结，另一个 arm 仍完整报告，不得逐 cell 切换。

### Cheap rule

只按 receiver amplitude（不看 innovation）冻结 DD update，threshold 同样只用
validation。它检验“创新量方法是否只是普通 fade gate”。

必须有两个不同输入产生不同 P2/P3 行为的 direct information-increment test；若
输出/更新 mask 与 P1 或 cheap rule 全同，方法 identity FAIL。

---

## 5. 公平比较与参数

### 5.1 Conventional comparator

至少包含：

- 4OPM coarse CFO + BPS（32 test phases，block/window validation-tuned）；
- 同一个 4OPM coarse CFO + continuous-state DD-DPLL；
- validation-frozen `B*` 为二者在 primary validation mix 上的全局最佳。

BPS/DPLL 不能单独承受 B10 才负责的大 CFO；所有 conventional arms 获得同等合法
coarse-frequency stage、waveform、evaluation mask 和 tuning opportunity。P1 自己
完成 joint CFO/PN，不额外获得 true/coarse CFO。

truth-assisted derotation 只作 upper bound，不作 Go comparator。

### 5.2 Primary star-ground transfer

从 `params.py` 读取并在 contract 记录：

- `B5Params.R_SYM_B5=2.5e9`：`SOURCE_TRANSFER`。来源
  `10.1016/j.optcom.2024.130981` 的 2.5-GBaud PM-QPSK 星地下行/B2B 硬件验证；
  只支撑符号率与星地迁移，不支撑 16-QAM 或 B10 原生身份；
- `LASER_LW=10 kHz`（WARNING，来源和限定原样保留）；
- positive `F_RESIDUAL=1 MHz`（WARNING，FOE-resolution derived assumption）；
- GG weak `(11.6,10.1)`、moderate `(4.0,1.9)`、strong `(4.2,1.4)`；
- `f_G=100 Hz`，对应 `τ_c≈1.59 ms`；
- 25,000 symbols/frame，前 128 pilot。

electrical \(E_s/N_0\) candidate grid 预注册为
`[14,17,20,23,26] dB`，类型固定为
`UNVERIFIED_PROJECT_DECLARED_RANGE / PREREGISTERED_EXPLORATORY_CANDIDATE_GRID`：
它是用于 validation 定位 HD-FEC 邻域的独立扫描轴，不是 B10 OSNR、不是文献性能
点，也不支撑星地链路预算。只用 validation 在每个 GG 档选择最多 3 个相邻点；
test 不重选。若 validation 在该有限网格内不能给 P1 与 conventional B* 找到共同的
真实 HD-FEC crossing 邻域，则该 GG 档不得触发 Q² `METHOD_SIGNAL`，只保留
raw BER/outage/boundary。

可另加 B10-supported transfer stress（10 MHz CFO、100 kHz linewidth），但必须标
`STRESS_ONLY / SOURCE_TRANSFER`，不能单独触发 `METHOD_SIGNAL`。

### 5.3 Seeds 与统计

- 在 primary 前生成并冻结 tracked `seed-census.yaml`，逐项列出事实源：
  - T006：`contract.yaml` / worker-log，validation `7600–7604`，test
    `7700–7709`；
  - T008：`b1-adaptive-phase-window-v2/seed-census.yaml`，validation
    `8000–8009`，test `8100–8119`；
  - T009：`a4-deployable-adaptive-cpr-v2/seed-census.yaml`，validation
    `91001–91010`，test `92001–92010`；
- T010 保留 invalid-development source-smoke seed `130001` 和非性能 canonical-test
  seed `130002`，冻结 clean confirm seed `130003`、validation seeds
  `131001–131005`、test seeds
  `132001–132010`。所有池两两不交，且与上述
  T006/T008/T009 全部观察池不交；
- runner、contract、seed census 和 tests 必须逐元素相等；确定性测试还要重新解析
  三份历史事实源并证明交集为空，不能只信 `disjoint: true` 文本；
- 每个 test row 保存 bit errors、denominator、BER、condition、SNR、seed、arm、
  update/freeze rate、innovation stats、state finite flag；
- paired bootstrap 95% CI，paired wins，mean/median/outage
  `P(BER>3.8e-3)`；所有聚合必须可从 raw bit-identical 重算。

### 5.4 BER、Q² 与合法 working region

指标合同在 `contract.yaml` 和实现中只能有一个定义：

- error population：仅 data symbols `k=128…N-1`，Gray 16-QAM 的 4 bits/symbol；
  所有 arm 使用同一个 data mask、bit population 和 denominator
  `4*(N-128)`，pilot 永不进入 BER；
- 每 seed/cell/arm 先保存整数 `bit_errors` 与 `denominator`，再算
  `BER=bit_errors/denominator`；cell aggregate 同时报告 pooled
  `sum(errors)/sum(denominator)` 和 per-seed 分布，禁止 mean-of-means 偷换；
- \(Q=\sqrt{2}\,\mathrm{erfcinv}(2\,BER)\)，
  \(Q^2_{\mathrm{dB}}=20\log_{10}(Q)\)。零误码只在该 row 用
  `BER_bound=0.5/denominator`；`BER>=0.5` 的 Q² 为 undefined；
- headline paired gain 按同 seed 的
  `Q²_method-Q²_comparator` 计算，再对 10 个冻结 test seeds bootstrap；pooled
  Q² 只作交叉检查，不能替代 paired CI/wins。

一个 GG/SNR cell 只有同时满足以下条件，才进入 Q² `METHOD_SIGNAL` mask：

1. 被裁决的 candidate arm（P2 或 P3）、P1、cheap rule、conventional B* 的全部
   冻结 test seed 均 finite 且
   `BER<0.2`；任一 seed `BER>=0.2` 即该 cell 为 collapse/out-of-region；
2. 该 GG 档冻结的相邻 SNR 点中，被裁决的 candidate arm、P1、cheap rule、
   conventional B* 各自都以
   **实际 pooled raw BER** 在 HD-FEC `3.8e-3` 两侧形成至少一个相邻 bracket：
   低 SNR 点 `BER>3.8e-3`，高 SNR 点 `BER<=3.8e-3`，且局部方向不反常；
3. 没有 no-crossing、non-monotone、state-nonfinite、denominator/mask mismatch、
   source-transfer-only 或单 seed/cell 支配 flag。

no-crossing、近随机 BER、collapse 或反常曲线仍必须完整报告 raw BER/outage，
但只能支持 `PACKAGING_BOUNDARY`/outage boundary 或 identity diagnostic，绝不能
通过非线性 BER→Q² 触发 `METHOD_SIGNAL`。raw→aggregate 重算必须逐行复现
bit errors、denominator、BER、Q²、mask reason、paired differences、CI 和 verdict。

---

## 6. 预注册裁决与 method delta

裁决先判 identity，再判 working region，再判 method：

### `BLOCKED_IDENTITY`

source smoke、pilot/channel、RLS lifecycle、information boundary、conventional
frequency responsibility、raw closure 任一失败。`mission_method_delta=NONE`；
不得补第二包。

### `METHOD_SIGNAL`

至少一个 P2/P3 在**非 stress-only、满足 §5.4 全部合法 working-region mask**
的 held-out primary cells：

- 相对 P1、cheap rule、conventional B* 三者的 validation-frozen strongest
  comparator，paired primary gain `>=0.3 dB Q²`；
- paired bootstrap 95% CI lower `>0`，paired wins `>=7/10`；
- outage 不劣于 strongest comparator；
- clean/weak high-SNR degradation `<=0.1 dB`；
- 至少两个 GG/SNR cells 方向一致，且都不含 collapse/no-crossing seed；
- 被裁决的 candidate arm（P2 或 P3）、P1、cheap rule 与 conventional B* 都有
  真实 FEC crossing 才允许该 GG 档的 Q² METHOD_SIGNAL 或 required-SNR/dB
  crossing claim；
- 机制诊断显示 gain 与 fewer erroneous/high-innovation updates 一致。

对应 `mission_method_delta=METHOD_SIGNAL`；若证据同时闭合正式推广所需边界，主控
另判 `PROMOTION_READY`，executor 不自行晋级。

### `PACKAGING_BOUNDARY`

P2/P3 未达到 mean-Q² signal，但在预注册 outage、failure boundary 或 complexity
维度形成稳定优势，且不被 cheap rule 支配。对应
`mission_method_delta=PACKAGING_BOUNDARY`。

### `METHOD_FAIL_WITH_SPACE`

source/native P1 与 conventional B* 均在合法 working region，oracle 或 P1 failure
diagnostic 说明仍有空间，但 P2/P3 未过方法门。若完整 fair comparison 已运行，
`mission_method_delta=FAIR_COMPARISON_RUN`；negative result 本身不是方法。

### `NO_PROBLEM_SURVIVAL`

source identity 成立，但 fixed P1/conventional B* 没有预注册问题空间，或 cheap
rule 完全解释/支配 P2/P3。formal 可作 scoped negative；mission delta 最高
`FAIR_COMPARISON_RUN`，不得写成方法。

---

## 7. Tests 与独立可审查证据

定向 tests 至少覆盖：

1. task-control 已由 executor 起飞时 PASS；
2. pilot manifest SHA、合法 16-QAM、128 contiguous、data RNG independence；
3. pilot/data 同一 TX-side channel/noise；
4. source RLS equations、`h0/P0/δ/F`、训练→DD 切换点；
5. synthetic residual-direction regression：同一正 residual 下旧反号沿错误方向、
   operational residual 沿真实相位方向更新；
6. radians only、positive CFO sign/units、seed `130003` 的 1/10 GHz BER confirm；
   该测试实际执行就是唯一 confirm，派发前不得预跑；
7. no TX truth/future/post-hoc resolve；
8. shared realization across every arm；
9. P2/P3 information increment 与 cheap-rule non-alias；
10. conventional arms 共享 coarse-frequency responsibility；
11. validation/test/excluded seed census；
12. BER/Q²/working-region mask 与 raw→aggregate bit-identical；no-crossing、
    `BER>=0.2`、non-monotone、denominator mismatch、pooled zero-error bound、
    bracket 等号、common/no-common SNR objective 与完整 tie chain；
13. 30-setting index mapping、gar/block100、h→sqrt(h)、Es=1/AWGN 方差、无
    AGC/无 per-cell renormalization；
14. exact 2250 expected keys、strict-prefix、30-row cell 完整性、duplicate/gap/
    stale-hash 拒绝、existing-prefix SHA 不变，以及模拟 write/replace failure 时旧
    target 保持 byte-identical 的 atomic checkpoint；
15. `save_results` metadata、source/contract/pilot/source-code exact SHA closure，
    每份 C2 artifact 携带 legacy pre-C1 debt；
16. BPS/DPLL 完整 score exact tie 时 B* 确定选择 BPS，且反转实现遍历顺序不改变
    winner；
17. verdict boundary tests；
18. Windows default locale 与 `PYTHONUTF8=1`。

还必须：

- `git diff --check` exit 0；
- YAML/JSON parse PASS；
- `git check-ignore` 证明 raw/aggregate 未被忽略；
- `git diff --stat` 证明 protected/common/params/旧包零改动；
- commit 中实际包含 source、tests、worker-log、pilot manifest 和全部 raw/aggregate；
- worker-log 记录真实命令、耗时、错误、修复、数据行数、tests 和 git status。

---

## 8. 收尾与回执

1. 使用日志追加一行到 `.sessions/sim-preflight-log/usage-2026-07.md` **由主控在
   接收后统一写**；executor 不改 `.sessions/**`。
2. executor 只做一次 consolidated commit，不 amend `8ea886e`，不 push。
3. 不更新 live/formal/master/mission owner；主控和独立 verifier 接收后更新 CP010。

最终只回传：

```text
status: PASS|PARTIAL|BLOCKED|FAIL
commit: <40-char SHA>
worker_log: projects/thesis-fso/worker-logs/step-010-b10-source-native-adaptive-rls-cpr.md
anomaly: <NONE or one concise anomaly>
```
