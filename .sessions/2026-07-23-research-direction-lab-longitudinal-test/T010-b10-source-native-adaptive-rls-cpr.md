# Task Brief: B10 source-native adaptive pilot-RLS CPR

> 来源: S001（live D006 / R002 / formal D017）
> 产出位置: `projects/thesis-fso/worker-logs/step-010-b10-source-native-adaptive-rls-cpr.md`
> 日期: 2026-07-26
> 唯一文档: executor 只需本 T、其中明确列出的仓库源码与共享论文文件

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 17
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

**产出**：隔离实现、tracked raw/aggregate artifacts、定向 tests、synthesis 和
worker-log；一次 consolidated commit，不 push。

**最高纪律（违反任一条即废）**：

1. T006 只作失败 fixture；不得复制其稀疏 pilot、非星座 pilot、早退 DD、P reset、
   post-channel pilot 重构或 TX-truth resolve。
2. 前 128 个 symbol 必须是独立冻结、接收端可重建的连续 16-QAM pilot manifest；
   pilot 与 data 必须在 TX 侧进入同一物理 channel/noise realization。
3. deployable arm 不得读取 runtime TX payload、bits、true phase/CFO、future samples
   或 post-hoc ambiguity label；oracle 仅作 bound。
4. source smoke 通过后必须同包跑 P1–P3 和 cheap/conventional comparison；不得把
   smoke、测试 PASS、代码创建或 evaluator 修复记为方法信号。
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
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md#D017`；
- 本包不进入 Step 5/Contract/Execute。

任一不一致：返回 `BLOCKED_STALE_CONTROL`，不写代码、不跑实验。

### 1.2 必读与来源

完整读取：

1. 本 T；
2. live `R002-post-t009-carrier-remap.md` 与 formal D017；
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
   fixed B10，只运行定向 tests 和 1/10 GHz source smoke。任一 identity gate 失败
   即收口 `BLOCKED_IDENTITY`；通过才允许 Phase C。
3. **Phase C — methods + validation freeze（≤15 min）**：实现 P2/P3、cheap rule、
   BPS/DPLL，完成 direct information-increment tests；只用 validation seeds 冻结
   P1/P2/P3/cheap/B* 参数与每个 GG 档最多 3 个相邻 SNR 点。不得运行 held-out test。
4. **Phase D — held-out + closure（≤15 min）**：只读取已冻结设置运行 test seeds，
   保存 raw/aggregate/result，完成重算、synthesis、worker-log、全套定向/回归检查
   与唯一 final commit。若预计本段超时，先停止在 raw 已完整落盘的安全点，下一
   ≤15 分钟 turn 只做 deterministic closure，不重选参数或重跑已完成 test。

阶段回执格式固定为：

```text
status: PARTIAL_CONTINUE|BLOCKED|FAIL
phase: A|B|C|D
safe_point: <one line>
next_phase: <A|B|C|D|NONE>
anomaly: <NONE or one concise anomaly>
```

`PARTIAL_CONTINUE` 只表示同一 T010 尚未收口，不是新 package、method delta 或 formal
progress；主控不得据此更新 owner/mission-log。只有 §8 final receipt 才触发独立
科学验收。

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
  residual phase 更新；无额外 runtime pilot、无 truth reset。

公式来源必须在 `source-contract.yaml` 和代码注释中逐项标注：Deka 等 2024
p.166 Eq.(3)–(6) 为 RLS 递推，p.166–167 Eq.(7)–(8) 与 Fig. 1 为
training→DD、周期 regressor 和 residual update；`F=2π/h_{1,128}` 是把原文
degree 表达全链一致地换成 radians 的实现约定。PDF/原页与提取笔记不一致时以
PDF 原页为准并 `BLOCKED_IDENTITY`，禁止靠文字描述补公式。

`λ` 只在 validation 候选网格中选择并冻结。原文未给精确最优表，必须标
`validation_tuned`，不能冒充 source parameter。

### 3.4 Source identity smoke

source-only AWGN/control（非论文性能复现、非 thesis result）：

- 28 GBd、25,000 symbols、**electrical \(E_s/N_0=26\) dB**、
  linewidth 50 kHz；
- positive CFO 1 GHz 与 10 GHz；
- 同一 pilot manifest、P1 fixed B10；
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
- T010 冻结 source-smoke seed `130001`、validation seeds
  `131001–131005`、test seeds `132001–132010`。三池两两不交，且与上述
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

1. P、P1、cheap rule、conventional B* 的全部冻结 test seed 均 finite 且
   `BER<0.2`；任一 seed `BER>=0.2` 即该 cell 为 collapse/out-of-region；
2. 该 GG 档冻结的相邻 SNR 点中，P、P1、cheap rule、conventional B* 各自都以
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
- P、P1、cheap rule 与 conventional B* 都有真实 FEC crossing 才允许该 GG
  档的 Q² METHOD_SIGNAL 或 required-SNR/dB crossing claim；
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
5. radians only、positive CFO sign/units、1/10 GHz smoke；
6. no TX truth/future/post-hoc resolve；
7. shared realization across every arm；
8. P2/P3 information increment 与 cheap-rule non-alias；
9. conventional arms 共享 coarse-frequency responsibility；
10. validation/test/excluded seed census；
11. BER/Q²/working-region mask 与 raw→aggregate bit-identical；no-crossing、
    `BER>=0.2`、non-monotone 和 denominator mismatch 的 verdict boundary；
12. `save_results` metadata、source/contract/pilot/source-code SHA closure；
13. verdict boundary tests；
14. Windows default locale 与 `PYTHONUTF8=1`。

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
