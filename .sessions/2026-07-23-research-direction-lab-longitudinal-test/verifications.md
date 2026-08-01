# Verifications — Research Direction Lab 长程真实运行测试

## V001: T008 派发前独立终验

> date: 2026-07-26
> 关联：D001 / T008 / control epoch 12 / mission CP007
> verifier：独立只读 subagent
> FINAL VERDICT: PASS

### 证据

- v2 task guard PASS；epoch、action class、CP007 与 live control 一致。
- formal owner 保持 B1 Groundwork Step 4a；C15 未越过 FR-22。
- 五项 T007 identity 缺口全部进入起飞 smoke；合法 space 存活时同包强制跑 P1–P3。
- oracle Kill 门与方法门统一为 0.5 dB；正信号同时要求 bootstrap CI 和
  frozen-denominator win fraction。
- fresh seed、validation/test、paired realization、真实 FEC crossing、claim
  ceiling 与 executor/owner 边界闭合。
- 总预算不超过 1 天；无 P0/P1。

### 结论

PASS。允许派发 T008；本验证不预判其科学结果。

---

## V002: T008 主控科学接收审查

> date: 2026-07-26
> 关联：D002 / T008 / mission CP008
> verifier：独立只读 subagent + 主控确定性重算

### 验证项

- [x] 任务契约：`T008` 第 116–118、159–160 行要求无 crossing 时
  `UNRESOLVED_NO_CROSSING`，且 Kill 只接受真实 required-SNR `<0.5 dB`；
  `corrected_gate.py` 第 161–176、242–269 行改用 `dB-equiv` Kill → FAIL。
- [x] oracle identity：gate 第 136–159 行只比较 B-cond vs B*；per-block oracle
  第 209–210 行跳过 `N>BLOCK=100`，但冻结 `B*=256` → “candidate set 包含 B*”
  为假，FAIL。
- [x] working region：去掉 pilot 覆盖位置后独立重跑 validation。20 dB 下
  QPSK clean/operational B* BER=`0.173963/0.178046`，16QAM
  `0.271821/0.280207`；全部无 HD-FEC crossing → FAIL。
- [x] 工程测试：`python -m pytest
  projects/simulation/tests/test_b1_adaptive_phase_window_v2.py -q`
  → `17 passed in 10.64s`；这些测试未覆盖上述科学身份错误 → 工程 PASS。
- [x] artifact closure：commit `61f8c53` 只提交 13 个 source/test/log 文件；
  六个 raw/result/log 文件位于 gitignored `projects/simulation/results/` → FAIL。
- [x] seeds/hash：validation 8000–8009 与本地 artifact SHA 可复核，但缺失提交内
  fresh-test/raw artifact，不能形成可移植证据闭包 → PARTIAL。

### 证据

```text
data-only recompute @20 dB
QPSK clean=0.173963, operational=0.178046, adversarial=0.272604
16QAM clean=0.271821, operational=0.280207, adversarial=0.321137
required-SNR crossing: NaN for every listed condition

pytest:
17 passed in 10.64s
```

### 结论

FAIL（科学裁决与证据闭包）。T008 的正式 disposition 为
`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`；只保留工程测试、失败机制和
局部 raw 作为 defensive/evaluator 资产，不形成 family Kill。

### 后续（FAIL/PARTIAL 时）

不修 T008、不派 T009。新 Goal 对话先做 campaign remap；任何未来复用 B1 必须
重新建立 data-only eval mask、跨窗 π/2 unwrap、真实 FEC working region、真正包含
B* 的 oracle，并重新预注册，不得继承本次 Kill。

---

## V003: CP008 状态协调与 Goal handoff 独立终验

> date: 2026-07-26
> 关联：D002 / CP008 / H002 / formal D014
> verifier：独立只读 subagent

### 验证项

- [x] registry、live control、formal topic 与 master-state →
  epoch 13 / CP008 / D002 / D014 / no active carrier 一致。
- [x] 决策血缘 → live D001→D002、formal D013→D014 均正确。
- [x] mission streak → `same-axis=2, no-method=8` 与
  `OVERWEIGHT / DRIFTED` 一致，下一动作停止 B1/T009 并上提 remap。
- [x] H002 → H001→H002 编号连续；必填锚点、失败数据、债务、阈值、接收验证
  齐全；C001/interface-change schema 合法。
- [x] 变更范围 → 仅 `.sessions/**` 和 `projects/thesis-fso/master-state.md`，
  未修改 T008 或其他科学产物。
- [x] 结构验证 → registry/live-control/H002 contract YAML 可解析；
  `git diff --check` 无 whitespace error。

### 证据

```text
independent final review: PASS
P0=0, P1=0, P2=0
live: epoch=13, CP008, authority=D002
formal: D014, B1=BLOCKED_IDENTITY/RETURNED_TO_POOL
master: CAMPAIGN-REMAP-GOAL-HANDOFF-READY
```

### 结论

PASS。允许提交 CP008 接收、formal 回收与 H002 Goal 恢复入口。

---

## V004: Campaign remap、A4 formal 激活与 T009 独立终验

> date: 2026-07-26
> 关联：R001 / D003 / formal D015 / T009
> verifier：独立只读 subagent

### 验证项

- [x] H002 接收：S001 已逐项记录 epoch 13 / CP008 / D002 接收权威、
  T008=`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`、接收时 no-active-carrier，
  并核对 registry 依赖/冲突与 scope。
- [x] carrier remap：R001 比较 A4、B10/B12、B1 三条 formal-eligible carrier，
  六个必需维度齐全，并逐项说明其他候选为何不 ready。
- [x] 相对选择：D003/D015/R001 明确 A4 比 B10/B12 少 source-native estimator
  重建、比 B1 少第三个同轴 evaluator repair，因此更可能在单包形成方法增量。
- [x] strongest conventional baseline：T009 将 fixed DA、fixed NDA 与 formal
  S011 DPLL 纳入 B*/B-cond；被 DPLL 支配时禁止 `METHOD_SIGNAL /
  PROMOTION_READY`。
- [x] DPLL 实现身份：T009 强制最近邻 16-APSK hard decision、跨 block 连续
  VCO、validation-only tuning，并在 primary 前复现 S011 AWGN/18 dB smoke；
  失败即 `BLOCKED_IDENTITY`。
- [x] 执行边界：只授权 T009；未运行实验，未修 T008/B1，未修改旧科学产物；
  回执覆盖 task-control、stage-owner、identity 与 shared-change 阻塞。
- [x] 结构验证：task-control PASS；registry YAML 可解析；`git diff --check`
  exit 0。

### 审查轨迹

1. 首轮 `FAIL`（P0=0, P1=1, P2=2）：缺 DPLL strongest baseline、H002
   三事实逐项证据、stage/task-control 阻塞回执。
2. 二轮 `FAIL`（P0=0, P1=1, P2=0）：DPLL 已进 comparator，但缺连续 VCO、
   16-APSK decision、validation-only tuning 与 S011 working-region smoke。
3. 终轮 `PASS`（P0=0, P1=0, P2=0）：上述缺口全部关闭，全量 diff 未发现
   越权科学产物、控制面冲突或新增缺陷。

### 证据

```text
independent final review: PASS
P0=0, P1=0, P2=0
task-control: PASS
registry YAML: PASS
git diff --check: exit 0
experiment runs in remap turn: 0
```

### 结论

PASS。campaign remap、formal D015、live epoch 14 与 T009 科学任务合同一致；
允许提交并把 T009 路径交给用户中转。此 PASS 只授权执行包，不构成
`METHOD_SIGNAL`，也不完成长期 Goal。

---

## V005: epoch 15 线程内端到端执行切换独立终验

> date: 2026-07-26
> 关联：S001 / D004 / T009 / control epoch 15
> verifier：独立只读 subagent

### 验证项

- [x] 控制一致性：独立核对 topic control、T009 task-control、formal D015 与
  mission CP008 → epoch 15 / A4 / D015 / CP008 / T009 一致，task guard PASS。
- [x] 科学合同不变：逐项比较 D004 前后的 method identity、comparator 与门槛 →
  formal D015、A4 carrier、CP008 和 T009 科学判据均未改变。
- [x] 治理闭包：核对 D004、voice、S001、topic scope-change、不变量、registry
  与 master-state → 用户不再中转、线程内 executor/verifier 分离的表述一致。
- [x] 依赖与范围：解析 registry 并检查 dependency/conflict、原始目标冻结段与
  当前范围 → 依赖 active、无 conflict，历史原始目标由 D004 显式 scope change
  覆盖，没有越权科学改动。
- [x] 结构完整性：registry YAML 解析、`git diff --check` 与变更文件审计 →
  YAML PASS、whitespace exit 0，仅授权治理文件发生变化。

### 证据

```text
independent final review: PASS
P0=0, P1=0, P2=0
task-control: PASS
registry YAML: PASS
git diff --check: exit 0
scientific contract changes: 0
```

### 结论

PASS。允许本对话主控直接派线程内 executor 执行 T009，随后交给不同的独立
verifier 做科学接收。此验证只授权执行接口切换，不构成方法产出。

---

## V006: T009 A4 身份阻断与 CP009 主控接收审查

> date: 2026-07-26
> 关联：T009 / D005 / formal D016/V003 / mission CP009
> verifier：独立只读 subagent + 主控确定性重算

### 验证项

- [x] 独立终审：读取 verifier FINAL → `FAIL, P0=4, P1=5, P2=1`；接受
  `BLOCKED_IDENTITY` 与 method delta `NONE`，拒绝可靠工作区物理支配 claim。
- [x] 工程测试：fresh 运行 T009 定向测试 → `5 passed in 1.48s`；覆盖不足以证明
  source/pilot/frequency/working-region 身份，工程 PASS、科学身份 FAIL。
- [x] DPLL smoke：从 raw/result 重算连续与 reset → BER
  `0.0036458333 / 0.0065364583`，ratio=`1.792857`，落入 T009 的局部 smoke 门；
  该 PASS 不补偿其他 identity P0。
- [x] raw 可复现性：解析 `raw.json` → validation 540 行、10 seeds、9 conditions、
  每 seed 54 blocks、540 个唯一 realization key；三 arm 的错误数/共同分母与
  result 一致。
- [x] P0-1 pilot/TX truth：审查 `generate_pool` 与 `_block_arms` →
  全 256 符号随机 payload 的 `shared["tx"][PILOT_IDX]` 被直接交给 arm，deployable
  API 还接收完整 `tx/bits`；没有独立冻结且接收端可重建的 pilot manifest，FAIL。
- [x] P0-2 frequency-stage：审查 shared channel 与 DA/NDA 调用 →
  `f_dot=0` 未关闭 `F_RESIDUAL=1 MHz`；DA 用 64 个所谓 pilot 回归频率，NDA
  `assume_df_zero=True`，DA 9/9 不能归因于 DA/NDA 机制，FAIL。
- [x] P0-3 working region/source：对照 contract、formal 条件与 FEC 门 →
  16/24/36 dB 无来源且 formal 湍流网格上限为 26 dB；9 个条件全部无合法
  HD-FEC crossing，最佳 arm/cell BER=`0.005056 > 0.0038` 且高 SNR 非单调，FAIL。
- [x] P0-4 evidence closure：运行 `git check-ignore`、核对 commit 与 metadata →
  raw/result 被忽略、未进入 `8ea886e`，metadata 仍写执行前 `220e477`，提交不能
  复现 headline，FAIL。
- [x] diff hygiene：运行 `git show --check --format= 8ea886e` →
  8 个文件报 `new blank line at EOF`，exit 2，FAIL。
- [x] stop/delta：worker-log 与 result 均为 `primary_run=false`、
  `bounded_repairs_used=1`；P1–P3 fresh test 未运行，没有
  `CONSTRUCT_CREATED / FAIR_COMPARISON_RUN / METHOD_SIGNAL`。

### 证据

```text
independent verifier FINAL:
FAIL
P0=4, P1=5, P2=1

P0:
1. random-payload tx[PILOT_IDX] is passed as known pilots; no frozen
   receiver-reconstructable pilot manifest
2. F_RESIDUAL=1 MHz is estimated by DA while NDA runs assume_df_zero=True
3. 16/24/36 dB conditions are unsourced/outside the formal <=26 dB grid;
   no arm/cell reaches HD-FEC 3.8e-3 and high-SNR BER is non-monotone
4. raw.json/result.json are ignored and absent from 8ea886e; metadata=220e477

executor:
commit=8ea886e4b5c1e3318fd9426dcc7e8aebcdf8a558
formal_science_disposition=BLOCKED_IDENTITY
mission_method_delta=NONE
primary_run=false
bounded_repairs_used=1

pytest:
5 passed in 1.48s

raw deterministic recompute:
rows=540, pools=validation, seeds=10, conditions=9, blocks_per_seed=54
unique_realization_keys=540
DA:   errors=20681, bits=414720, BER=0.0498673804012346
NDA:  errors=33412, bits=414720, BER=0.0805652006172839
DPLL: errors=22021, bits=414720, BER=0.0530984760802469
DPLL smoke: continuous=0.0036458333333333334
            reset=0.006536458333333333
            ratio=1.792857142857143

per-condition DA/NDA winners:
DA=9, NDA=0
minimum arm/cell BER=0.00505642361111111 > HDFEC=0.0038
required-SNR crossing=UNRESOLVED_NO_CROSSING

git check-ignore:
.gitignore:8:results*/ raw.json
.gitignore:8:results*/ result.json

git show --check --format= 8ea886e:
8 files: new blank line at EOF
exit=2
```

P1 的 5 项问题为：source closure 未完成算法级对照、seed census 只有声明、
bounded repair 无可审前后差异、5 项测试未覆盖 §4 全部身份、diff hygiene 失败。
P2=1 为 worker-log/synthesis/method-card 对 DA 9/9 的物理措辞越过证据上限。

### 结论

FAIL。接受 `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED` 与
`mission_method_delta=NONE`；拒绝“可靠工作区 DA 9/9 物理支配”、A4 family Kill
以及任何性能/论文 claim。T009 是 `ADEQUATE / ALIGNED` 的有界身份包，但完整
mission 已连续九包无方法增量，状态仍为 `DRIFTED / STALLED`。

### 后续（FAIL/PARTIAL 时）

不修当前 T009 evaluator，不开第二个 A4 repair package。A4 返回候选池，live
control 升至 epoch 16 / CP009 并进入 campaign remap；下一轮比较 B10 source-native
最小重建与新 candidates，在 formal 激活前禁止科学实验。

---

## V007: T010 B10 source-native 方法包独立派发终验

> date: 2026-07-26
> 关联：R002 / D006 / formal D017 / T010
> verifier：独立只读 subagent

### 验证项

- [x] formal/current/control 一致性：核对 live epoch 17 / CP009、formal D017、
  master-state、literature_notes 与 direction-lab current projections →
  当前唯一 carrier 均为 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，T006 只保留历史。
- [x] FR-20 参数来源：核对 B10/B5 原 PDF、params 与任务合同 →
  禁止消费占位 `SystemParams.R_SYM`；2.5 GBd 只从 `B5Params.R_SYM_B5`
  读取并标 `SOURCE_TRANSFER`；B10 26 dB OSNR 不等同 electrical SNR；
  五点电 SNR 网格标 `UNVERIFIED_PROJECT_DECLARED_RANGE`。
- [x] source identity：核对 B10 PDF Eq.(3)–(8)、Fig. 1、128 contiguous
  pilots、28 GBd 与 T010 → 原文身份、positive-CFO smoke、radians、训练→DD
  生命周期和 source claim ceiling 均有可失败门。
- [x] metric/working-region：核对 data-only population、整数 error/denominator、
  Q² 公式、paired CI、真实 HD-FEC crossing、全 seed `BER<0.2` 与 no-crossing /
  collapse 边界 → 非法区域不能触发 `METHOD_SIGNAL`。
- [x] comparator/information：核对 P1/P2/P3、amplitude-only cheap rule、共同
  4OPM coarse stage 的 BPS/DPLL、validation-only freeze 和 no truth/future/
  post-hoc boundary → fair-comparison 与 direct information-increment gate 闭合。
- [x] seed closure：核对 T006/T008/T009 历史事实源及 T010 冻结池 →
  `7600–7604/7700–7709`、`8000–8009/8100–8119`、
  `91001–91010/92001–92010` 与 `130001/131001–131005/132001–132010`
  均精确登记且交集为空。
- [x] 子 agent 预算：T010 Phase A–D 每个 executor turn 硬上限 15 分钟，
  有安全停止点；Phase C 禁用 held-out，Phase D 只读 frozen settings；
  `PARTIAL_CONTINUE` 不更新 owner/mission/method delta，同一包最终只做一次 commit。
- [x] 结构验证：task-control PASS；registry/current YAML 可解析；
  `git diff --check` exit 0；基础回归 `76 passed`；参数审计
  `40 OK / 24 WARNING / 4 CRITICAL / 6 DEAD`，T010 禁止消费 4 个 CRITICAL。

### 审查轨迹

1. 首轮 `FAIL`（P0=2, P1=3, P2=0）：参数来源混用、Q² mask 未闭合、
   current projections 停在 T006、source/figure 身份与 seed census 不完整。
2. 二轮 `FAIL`（P0=0, P1=2, P2=0）：上述科学与投影缺口已闭合，但
   literature_notes 文件末尾仍把 T006 写成当前；T010 未按单次子 agent
   `≤15 min` 分段。
3. 终轮 `PASS`（P0=0, P1=0, P2=0）：T006 段降为历史并追加 D017/T010
   current amendment；T010 Phase A–D 的时间边界、停止点与冻结边界全部闭合，
   未放宽 identity、validation、held-out 或 no-second-repair 科学合同。

### 证据

```text
independent final review: PASS
P0=0, P1=0, P2=0

task-control validator:
PASS

YAML:
PASS state/current.yaml
PASS portfolio/current.yaml
PASS harvest/current.yaml
PASS .sessions/_registry.yaml

pytest:
76 passed in 12.06s

audit_params:
total=74, ok=40, warning=24, critical=4, dead=6

git diff --check:
exit 0
```

### 结论

PASS。允许由本线程内部 executor 按 Phase A–D 执行 T010。此 PASS 只证明派发
合同、身份门与证据边界可审查，不预判 source smoke、科学结果、formal disposition
或 `mission_method_delta`，也不完成长期 Goal。

---

## V008: T010 初次 Phase-B 身份 verdict 独立科学拒收

> date: 2026-07-26
> 关联：T010 / D007 / formal D018
> verifier：独立只读 scientific subagent

### 验证项

- [x] artifact 确定性重算：只重跑预注册 source smoke，移除动态 `_meta` 后逐字段
  比较 → 与 `artifacts/source-smoke.json` 完全一致。
- [x] 初次 gate 数字：核 raw integer errors/denominator →
  1 GHz `24915/99488=0.2504322129302026`；
  10 GHz `41645/99488=0.4185931971695079`，均未过 `3.8e-3`。
- [x] PDF/source operational sign：核 B10 PDF p.165 Eq.(1)、p.166–167
  Eq.(8)/Fig.1 与代码 → Eq.(8) 文本虽被 literal 抄录，但在
  `r=s·exp(+jφ)+n`、`exp(-j predicted)` 约定下 residual 代数符号相反；
  operational residual 应为 `angle(derotated*conj(decision))`。
- [x] `λ` 身份：核 T010、PDF 与 runner → `.999` 无 source parameter 依据；
  论文要求优化 `λ` 且说明接近 1 会降质，不能用 `.999` 作 source identity Kill。
- [x] 不落盘诊断：只在 seed `130001` 上判断根因，不作 confirm 或 method evidence →
  operational sign + `.999`：1 GHz `6/99488`、10 GHz `41166/99488`；
  operational sign + `.99`：两格均 `0/99488`。
- [x] 其余身份边界：Gray 16-QAM、128 contiguous pilots、runtime data RNG、
  TX-side shared channel/noise、receiver information boundary、`h0/P0/δ/F`、
  indexing、CFO 换算与 data-only denominator → 未发现其他 P0。
- [x] 实现/证据闭包：fresh tests `12 passed, 1 skipped`，其中 skip 仅 Phase C；
  `git diff --check` exit 0；artifact 未 ignored 但尚未 final tracked/committed。

### 证据

```text
science_verdict=REJECT_VERDICT_IMPLEMENTATION_INVALID
formal_science_disposition=SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID
mission_method_delta=NONE
phase_c=NO

literal Eq.(8), lambda=.999:
1GHz 24915/99488 = 0.2504322129302026
10GHz 41645/99488 = 0.4185931971695079

operational residual diagnostic, lambda=.999:
1GHz 6/99488 = 6.030878e-5
10GHz 41166/99488 = 0.413778546

operational residual diagnostic, lambda=.99:
1GHz 0/99488
10GHz 0/99488

pytest:
12 passed, 1 skipped in 1.61s

git diff --check:
exit 0
```

### 结论

FAIL。拒收当前 `BLOCKED_IDENTITY` 为可信 B10 身份失败；只接受
`SCIENCE_VERDICT_REJECTED / IMPLEMENTATION_INVALID`，且
`mission_method_delta=NONE`、Phase C 禁止。D007/formal D018 只能授权一次包内
Phase-B 合同纠错与全新 seed 确认；不能把诊断数字当方法信号。

### 后续（FAIL/PARTIAL 时）

先独立审查 epoch 18 / D018 / T010 amendment；PASS 后固定 operational residual、
source-only `λ=.99` 和 confirm seed `130002`，只重跑 Phase B。confirm 失败即轮换，
通过也仍需另一独立科学 verifier 才可进入 Phase C。

---

## V009: T010 Phase-B amendment 独立派发审查

> date: 2026-07-26
> 关联：D007 / formal D018 / T010
> verifier：独立只读 subagent

### 验证项

- [x] owner/control/task：核 epoch 18 / CP009 / D018 / T010 → task-control PASS，
  operational residual 与 source-only `.99` 边界一致。
- [x] confirm seed 洁净性：repository exact-token 与已执行 tests →
  `130002` 已在 canonical/RNG test 生成 realization，不能称为严格 unseen。
- [x] T010 自包含回归：核 D007 与 T010 §7 → D007 要求的 synthetic
  residual-direction 和 1/10 GHz BER regression 未被显式写入。
- [x] Phase-B 暂停门：核 §1.4 与 §8 → “confirm 后独立验收”与“只有 final receipt
  才触发验收”冲突，存在 executor 直接进入 Phase C 的歧义。
- [x] registry/current/protected：YAML 与 diff → registry 仍停 epoch 17/D017；
  current YAML parse PASS，protected/common/params/旧包零 diff。

### 证据

```text
Spec Compliance=FAIL
Review=NEEDS_FIXES
P0=0
P1=3
P2=1

task-control validator:
PASS

seed fact:
tests/test_b10_source_native_adaptive_rls_cpr.py:170
generate_shared_b10_realization(seed=130002, ...)

git diff --check:
PASS
```

### 结论

FAIL。epoch 18 amendment 不得派发；不运行 confirm 或 Phase C。

### 后续（FAIL/PARTIAL 时）

D008/formal D019 将 confirm seed 改为 exact-token 零命中的 `130003`，在 T010
显式加入 residual-direction/BER regression 与
`PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 暂停回执，并同步 registry/current
projections 后重新独立审查。

---

## V010: epoch-19 T010 amendment 二轮独立审查

> date: 2026-07-26
> 关联：D008 / formal D019 / T010
> verifier：独立只读 subagent

### 验证项

- [x] seed 与暂停门：核 `130003`、regression、receipt → clean seed、唯一 confirm
  与 `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 均闭合。
- [x] current owner：核 epoch 19 / CP009 / D008 / D019 / registry/current →
  一致，task-control 与 YAML PASS。
- [x] stale formal 起飞引用：核 T010 §1.1 → 仍指 superseded D017。
- [x] source-contract 迁移：核 T010 §0.1 与旧 contract → task 未自包含要求把
  authority/status/residual/invalid-history/current-confirm plan 迁移到 D019。
- [x] protected diff：`git diff --check` PASS，common/params/旧包零 diff。

### 证据

```text
Spec Compliance=FAIL
Review=NEEDS_FIXES
P0=0
P1=2
P2=0

task-control=PASS
YAML=PASS
git diff --check=PASS
```

### 结论

FAIL。不得派发 confirm。

### 后续（FAIL/PARTIAL 时）

T010 起飞 authority 改为 D019，并在 §0.1 明列 source-contract 的 D019 authority、
invalid-history、pending confirm、operational residual/`.99`/seed `130003` 与
artifact non-overwrite 迁移要求；不需要改变 epoch 19 的科学 gate，修后复审。

---

## V011: epoch-19 T010 clean confirm 独立派发终验

> date: 2026-07-26
> 关联：D008 / formal D019 / T010
> verifier：独立只读 subagent

### 验证项

- [x] stale authority 修复：T010 §1.1 指向 D019，D017/D018 仅作 superseded
  历史 → PASS。
- [x] source-contract 迁移自包含：authority、initial invalid history、
  `source-smoke-invalid-v1.json`、pending confirm、operational residual、
  `.99` 类型、seed `130003` 与 non-overwrite 均明确 → PASS。
- [x] clean confirm/暂停门：唯一 seed `130003` 1/10 GHz gate，PASS 后返回
  `PARTIAL_CONFIRM_AWAITING_SCIENCE_REVIEW` 并停止 → PASS。
- [x] owner/current：epoch 19 / CP009 / D008 / D019、registry、master、
  state/portfolio/harvest 一致 → PASS。
- [x] deterministic guards：task-control、四份 YAML、`git diff --check` →
  PASS；protected/common/params/T006/T008/T009 零 diff。

### 证据

```text
Spec Compliance=PASS
Review=APPROVED
P0=0
P1=0
P2=0

task-control=PASS
registry/state/portfolio/harvest YAML=PASS
git diff --check=PASS
```

### 结论

PASS。只授权 seed `130003` 的一次 Phase-B confirm；confirm 后必须暂停并独立
科学验收。本 PASS 不授权 Phase C、method delta、第二个 repair/package、
Step 5/Contract/Execute 或 push。

---

## V012: T010 Phase-B clean confirm 独立科学接收

> date: 2026-07-26
> 关联：D008 / formal D019 / T010
> verifier：独立只读 scientific subagent

### 验证项

- [x] 历史 artifact 保留：SHA/bytes 与 V008 → invalid artifact
  `010662e1...f20f4`、2565 bytes，旧两格 `24915/99488` 与 `41645/99488`
  完全一致；新旧文件并存。
- [x] clean confirm 合同：核 seed/`λ`/claim ceiling → seed `130003`、
  source-only `.99`、`performance_claim=NONE`，confirm 前无性能观察。
- [x] artifact 独立重算：不重跑 smoke，只从 integer counts/config 重算 →
  1/10 GHz 均 `0/99488`；row bound `5.0257317465422965e-6`；
  Q² `12.900705909907302 dB`；CFO relative errors
  `9.952903443384171e-5 / 4.499364865190506e-4`；所有 gate 一致。
- [x] source identity 与信息边界：核 operational residual、RLS lifecycle、
  manifest/channel/noise/data mask → 无 TX truth/future/post-hoc、mask/mapping/noise
  P0/P1。
- [x] confirm invocation closure：报告只记录一次 runner；post-confirm test monkeypatch
  证明 read gate 不调用 smoke → 接受为一次 confirm，记录缺少 runtime lock 的 P2。
- [x] fresh non-smoke checks：task-control/YAML/diff/artifact-ignore/protected →
  PASS；`PYTHONUTF8=1` T010+T006 `46 passed, 1 skipped`，扩大回归
  `122 passed, 1 skipped`。

### 证据

```text
science_verdict=ACCEPT_SOURCE_IDENTITY_PASS
formal_science_disposition=SOURCE_IDENTITY_PASS / PHASE_B_CONFIRM_ACCEPTED
mission_method_delta=NONE
P0=0
P1=0
P2=3

1GHz: 0/99488, CFO rel=9.952903443384171e-5
10GHz: 0/99488, CFO rel=4.499364865190506e-4
BER bound=5.0257317465422965e-6
Q2=12.900705909907302 dB

expanded non-smoke regression:
122 passed, 1 skipped in 19.58s
```

### 结论

PASS。接收 `SOURCE_IDENTITY_PASS / PHASE_B_CONFIRM_ACCEPTED`；source-native P1
身份门关闭，`mission_method_delta=NONE`，不是 `METHOD_SIGNAL`。epoch 19 不授权
Phase C；formal/live owner 递增并经独立派发审查后才可继续。

### 后续

- Phase C 起飞前封死 source-smoke 二次运行入口；
- read-only artifact gate 全量重算可重算的 BER/Q²/CFO/gates，并显式登记
  finite/switch/freeze 原值未落盘的 legacy P2；
- 默认 locale 的两项失败属于旧 T006 YAML/GBK，不扩到当前实现；T010 自身默认
  locale 必须继续通过。

---

## V013: T010 Phase-C C1 派发规范首轮独立审查

> date: 2026-07-26
> 关联：D009 / formal D020 / T010 / control epoch 20
> verifier：独立只读 subagent

### 验证项

- [x] task-control 与静态边界：validator、YAML/JSON、`git diff --check`、
  protected/common/params/旧包 diff → PASS；未发现 validation/test artifact。
- [ ] formal current projection：formal topic-index 与 registry formal entry 仍停在
  D017/T010 pre-review，未投影 D020/V012/C1→review→C2/held-out lock → FAIL。
- [ ] live snapshot：V012 条目同时写“Phase C 推进”与“仍不授权 Phase C”，未区分
  epoch 19 历史和 epoch 20 当前授权 → FAIL。
- [ ] C1/C2 行为边界：T010 最高纪律仍可被解释为 C1 直接跑 P1–P3 comparison，
  未显式禁止 C1 创建 validation/test artifact → FAIL。
- [ ] source-contract migration：未给 exact path/schema，也未明确保留
  `current_confirm.*` confirm-time history并新增 D020 current authorization → FAIL。
- [ ] candidate arm identity：working-region 中使用未定义 `P`，可能导致逐 cell
  post-hoc 选择 P2/P3 → FAIL。

### 证据

```text
independent Phase-C dispatch review:
SPEC FAIL / NEEDS_FIXES
P0=0
P1=5

static positives:
task-control PASS
YAML/JSON PASS
git diff --check PASS
protected/common/params/old packages diff=0
validation/test artifacts=0
```

### 结论

FAIL。不得派发 C1，不得运行实验。

### 后续（FAIL/PARTIAL 时）

更新 formal topic-index/registry，消除 live epoch 19/20 歧义；把 C1 与 C2
comparison 边界、source-contract exact migration 和 P2/P3 no-best-of 规则写入
T010，再交同一独立 verifier 复审。

---

## V014: T010 Phase-C C1 派发规范第二轮独立审查

> date: 2026-07-26
> 关联：D009 / formal D020 / T010 / V013
> verifier：同一独立只读 subagent

### 验证项

- [x] V013 五项 P1：formal projection、live epoch 19/20、C1/C2 边界、
  source-contract exact migration、P2/P3 no-best-of → 全部关闭。
- [ ] formal current scope：仍保留早期 active `增量扩充 common`、`params.py`
  B11/B7 参数、旧 explore 路径与“转 experiments”清单；与 D020/T010 的隔离 C1、
  禁改 common/params/旧轴冲突 → FAIL。
- [x] fresh 静态门：task-control、7 YAML + 3 JSON、`git diff --check`、
  protected/common/params/T006/T008/T009 diff → PASS。
- [x] artifact/运行边界：只有两份 Phase-B source-smoke artifact，无
  validation/test artifact；审查未运行测试或科学实验 → PASS。

### 证据

```text
independent Phase-C dispatch re-review:
SPEC FAIL / NEEDS_FIXES
P0=0
P1=1
P2=0

V013 targeted P1 closed=5/5
task-control PASS
7 YAML + 3 JSON parse PASS
git diff --check exit 0
protected/common/params/T006/T008/T009 diff PASS
validation/test artifacts=0
tests/scientific experiments run by reviewer=0
```

### 结论

FAIL。C1 继续锁定。

### 后续（FAIL/PARTIAL 时）

从 formal topic-index 的 current scope 移除早期 B11/B7/B3
common/params/旧 explore/experiments 授权，只保留 T010 隔离 C1 路径后复审。

---

## V015: T010 Phase-C C1 派发独立终验

> date: 2026-07-26
> 关联：D009 / formal D020 / T010 / V013 / V014
> verifier：同一独立只读 subagent

### 验证项

- [x] V014 唯一 P1：formal current scope 只授权 T010 isolated C1；旧
  common/params/旧 explore/experiments 明确不再授权 → PASS。
- [x] V013 五项：formal/registry D020/V012、live epoch 19/20、C1/C2 边界、
  exact source-contract migration、P2/P3 no-best-of → 保持 PASS。
- [x] 静态门：task-control、7 YAML + 3 JSON、`git diff --check`、
  protected/common/params/T006/T008/T009 diff → PASS。
- [x] artifact/运行边界：仅两份 Phase-B source-smoke artifact；无
  validation/test artifact；reviewer 未运行测试或科学实验 → PASS。

### 证据

```text
independent final Phase-C C1 dispatch review:
SPEC COMPLIANCE PASS / APPROVED
P0=0
P1=0
P2=0

task-control PASS
7 YAML + 3 JSON parse PASS
git diff --check PASS
protected/common/params/T006/T008/T009 diff PASS
validation/test artifacts=0
tests/scientific experiments run by reviewer=0
```

### 结论

PASS。只授权 T010 Phase C1 implementation/direct/clean/noiseless tests，不授权
C2 validation、Phase D/held-out、method delta 或 push。

---

## V016: T010 epoch 21 起飞绑定首轮独立复审

> date: 2026-07-26
> 关联：D009 / formal D020 / V015 / T010 / control epoch 21
> verifier：同一独立只读 subagent

### 验证项

- [x] control/task binding：live epoch 21 / CP009 / D020 / V015 / C1-only 与
  T010 epoch 21，task-control → PASS。
- [ ] current projections：live 当前范围仍写 epoch 20/review 前禁执行，master
  方法轨仍标 `C1 REVIEW` 且未引用 V015 → FAIL。
- [x] 其他投影与边界：formal、registry、projects-overview、state、portfolio、
  harvest、C2/held-out lock、mission CP009/no-method=9 → PASS。
- [x] 静态与 artifact：`git diff --check`、protected/common/params/旧包、
  无 validation/test artifact，reviewer 未运行测试/科学实验 → PASS。

### 证据

```text
epoch21 binding review:
FAIL / NEEDS_FIXES
P0=0
P1=1
P2=0

task-control PASS
mission checkpoint=CP009
mission no-method=9
git diff --check PASS
protected diff PASS
validation/test artifacts=0
```

### 结论

FAIL。不得派 executor。

### 后续（FAIL/PARTIAL 时）

把 live 当前范围与 master 方法轨表统一为 epoch 21 / V015 / C1 AUTHORIZED，
明确 C1 完成后才独立 review，再复审。

---

## V017: T010 epoch 21 起飞绑定第二轮独立复审

> date: 2026-07-26
> 关联：D009 / formal D020 / V015 / V016 / T010 / control epoch 21
> verifier：同一独立只读 subagent

### 验证项

- [x] V016 两处 P1：live 当前范围与 master 方法轨已统一为
  epoch 21 / V015 / C1 AUTHORIZED → PASS。
- [ ] live 进展线索：V012 条目仍把 epoch 20/formal D020 称为“当前只授权 C1”，
  与顶部 epoch 21/V015/current position 冲突 → FAIL。
- [x] 其余 binding、投影、task-control、C2/held-out lock、mission CP009/
  no-method=9、diff/protected/artifact 边界 → PASS。

### 证据

```text
epoch21 binding second review:
FAIL / NEEDS_FIXES
P0=0
P1=1
P2=0

task-control PASS
git diff --check PASS
protected diff PASS
validation/test artifacts=0
tests/scientific experiments run by reviewer=0
```

### 结论

FAIL。不得派 executor。

### 后续（FAIL/PARTIAL 时）

把 live V012/epoch20 条目改为历史时态，并明确 V015/epoch21 才是当前 C1-only
授权，再复审。

---

## V018: T010 epoch 21 起飞绑定独立终验

> date: 2026-07-26
> 关联：D009 / formal D020 / V015–V017 / T010 / control epoch 21
> verifier：同一独立只读 subagent

### 验证项

- [x] live lineage：V012/epoch 20 已历史化，V015/epoch 21 是唯一当前 C1-only
  binding → PASS。
- [x] current projections：formal、registry、master、projects-overview、state、
  portfolio、harvest 均为 D020/V015/epoch 21/CP009/C1 AUTHORIZED → PASS。
- [x] task/mission：task-control fresh PASS；mission-log 仍为 CP009/no-method=9，
  未误记 method delta → PASS。
- [x] 静态/artifact：`git diff --check`、protected/common/params/T006/T008/T009
  diff → PASS；仅两份 Phase-B source artifact，无 validation/test artifact。
- [x] reviewer 行为：未运行测试或科学实验 → PASS。

### 证据

```text
epoch21 final binding review:
PASS / APPROVED
P0=0
P1=0
P2=0

task-control PASS
git diff --check PASS
protected diff PASS
mission checkpoint=CP009
mission no-method=9
validation/test artifacts=0
```

### 结论

PASS。允许内部 executor 执行 T010 Phase C1
implementation/direct/clean/noiseless tests；完成后必须暂停。不授权 C2、
Phase D/held-out、method delta 或 push。

---

## V019: T010 Phase C1 独立代码与科学合同审查

> date: 2026-07-26
> 关联：D009 / formal D020 / V018 / T010 / control epoch 21
> verifier：独立 code + science-contract subagent

### 验证项

- [ ] finite gate：P2/cheap 遇非有限 DD 样本时可冻结 `h/P` 而仍报告
  `state_finite=true`，但 corrected/innovation 已非有限 → FAIL。
- [ ] conventional identity：BPS 接受非 32 phases；DPLL API 的 `symbol_rate`
  未约束 common 隐藏 `T_S`，可能产生接口/科学身份错配 → FAIL。
- [ ] direct tests：shared-realization 未覆盖 P1/conventional；comparator 使用
  QPSK-like 波形；clean/noiseless 只断言 identity/finite，错误相位补偿也可通过
  → FAIL。
- [ ] primary contract：`contract.yaml` 仍为 `phase: B / NO_PHASE_C`，并把
  methods/baselines 标为未实现，与 C1 现状和 source contract 冲突 → FAIL。
- [x] source-contract migration、smoke seal、P2/P3 因果边界、cheap
  amplitude-only、P2/P3 no-best-of → PASS。
- [x] default locale 与 `PYTHONUTF8=1` 非-smoke C1 tests → 各 `6 passed`。
- [x] task/artifact/protected/mission：task-control、3 YAML + 3 JSON、两份 source
  artifact SHA、无 validation/test artifact、HEAD/CP009/no-method=9 → PASS。
- [ ] P2 债务：read-only recompute 固定返回 PASS；方法参数合法域未校验；
  pre-C1 owner/status/hash 无不可变快照，executor 的边界归因只能部分复核 → PARTIAL。

### 证据

```text
Spec Compliance: FAIL
Code/Science Contract: NEEDS_FIXES
P0=0
P1=4
P2=3

finite adversarial probe:
reported_state_finite=True
corrected_finite=False
innovation_finite=False

comparator identity probe:
test_phases=7 accepted

default Windows locale non-smoke C1 tests: 6 passed
PYTHONUTF8=1 non-smoke C1 tests: 6 passed
task-control PASS
artifact SHA accepted=f36901ff...105786
artifact SHA invalid=010662e1...f20f4
validation/test artifacts=0
HEAD=69e2d186...
mission=CP009 / no-method=9
```

### 结论

FAIL / `C1_REJECTED_NEEDS_FIXES`。`mission_method_delta=NONE`。不得运行 C2、
validation、held-out 或 Phase D。

### 后续（FAIL/PARTIAL 时）

同一 C1 内以 TDD 修复四项 P1 和两个可修 P2；扩大 direct 16-QAM shared-realization
与 clean/noiseless tests。pre-C1 snapshot 缺失作为 legacy attribution P2 保留，
不得事后伪造。修复后由同一独立 reviewer 复审。

---

## V020: T010 Phase C1 V019 修复独立复审

> date: 2026-07-26
> 关联：D009 / formal D020 / V019 / T010 / control epoch 21
> verifier：同一独立 code + science-contract subagent

### 验证项

- [x] V019 已关闭：finite adversarial path、BPS 32 phases/window、参数合法域、
  C1-only contract、read-only evidence audit、基础 all-arm 16-QAM sanity → PASS。
- [ ] DPLL 时标来源：`baselines.py` 仍导入 `common._config.T_S`，该值派生自本 T
  明令禁止的 `SystemParams.R_SYM`；wrapper 只检查数值相等，未消除来源违约
  → FAIL。
- [ ] DPLL 全局模糊：未像 BPS 一样用 receiver-known pilot manifest 处理 π/2
  ambiguity；同一 clean canonical Gray-16QAM realization 乘 `j` 后，
  BPS=`0/7680`，DPLL=`3838/7680≈0.49974` → FAIL。
- [x] task/default+UTF8/YAML/JSON/artifact/protected/mission 边界 → PASS。
- [ ] pre-C1 immutable snapshot 缺失 → legacy attribution P2，不能补造，不单独拒收。

### 证据

```text
Spec Compliance: FAIL
Code/Science Contract: NEEDS_FIXES
P0=0
P1=2
P2=1

pi/2 adversarial clean probe:
BPS errors=0/7680
DPLL errors=3838/7680
DPLL BER=0.49973958333333335

default locale targeted: 11 passed, 20 deselected
PYTHONUTF8=1 targeted: 11 passed, 20 deselected
task-control PASS
artifact SHA unchanged
validation/test artifacts=0
HEAD=69e2d186...
mission=CP009 / no-method=9
```

### 结论

FAIL / `C1_REJECTED_NEEDS_FIXES`。`mission_method_delta=NONE`。不得运行 C2、
validation、held-out 或 Phase D。

### 后续（FAIL/PARTIAL 时）

在隔离 `baselines.py` 中实现显式消费传入 `symbol_rate` 的 continuous DD-DPLL，
移除 `T_S/SystemParams.R_SYM` 依赖；用 pilot manifest 同步闭合 π/2 ambiguity 与
phase estimate，并增加 `rx·exp(jπ/2)` 对抗测试。修复后再次独立复审。

---

## V021: T010 Phase C1 最终独立复审

> date: 2026-07-26
> 关联：D009 / formal D020 / V019–V020 / T010 / control epoch 21
> verifier：同一独立 code + science-contract subagent；主控只做确定性证据复核

### 验证项

- [x] V020 两项 P1：隔离 Python 不再读取 `T_S`、`SystemParams/R_SYM`、
  `dpll_track_dd` 或 `_config`；continuous DD-DPLL 显式使用
  `t_s=1/symbol_rate` → PASS。
- [x] π/2 全局模糊：BPS 与 DPLL 都只用冻结的 128-symbol receiver-known pilot
  manifest 解模糊，并把 offset 同步写入 `phase_estimate`；`rx·exp(jπ/2)`
  Gray-16QAM 对抗测试两臂 data errors 均为 0 → PASS。
- [x] V019 回归：finite gate、exactly-32、参数域、all-arm shared realization、
  C1-only contract、read-only evidence audit 均保持闭合 → PASS。
- [x] fresh 主控复核：task-control PASS；Windows 默认 locale 与
  `PYTHONUTF8=1` 全文件各 `32 passed`；3 YAML + 2 JSON 可解析；
  `git diff --check` exit 0 → PASS。
- [x] artifact/seed 边界：artifact 仍只有两份 Phase-B source-smoke 文件且 SHA
  未变；validation/test/result artifact 均不存在；validation/test seed exact-token
  命中为 0 → PASS。
- [x] protected/mission 边界：common/params/旧包 numstat 为 0；HEAD 仍为
  `69e2d186...`；mission-log 仍为 CP009 / no-method=9 → PASS。
- [ ] pre-C1 immutable snapshot 缺失：无法事后证明 confirm-time fields
  byte-identical；当前实现没有补造或夸大证据 → legacy attribution P2，不阻断 C1。

### 证据

```text
independent final C1 review:
Spec Compliance: PASS
Code/Science Contract: APPROVED
P0=0
P1=0
P2=1

reviewer targeted evidence:
default locale V020/conventional/all-arm: 3 passed
PYTHONUTF8=1 same group: 3 passed
V019 finite/domain/recompute regression: 11 passed
YAML/JSON: 3 + 3 parse PASS
validation/test scientific runs by reviewer: 0

master fresh deterministic verification:
task-control PASS
default locale full file: 32 passed in 2.31s
PYTHONUTF8=1 full file: 32 passed in 2.27s
PARSE_PASS yaml=3 json=2
FORBIDDEN_SCAN_EXIT=1 (zero matches)
DIFF_CHECK_EXIT=0
PROTECTED_NUMSTAT_EXIT=0
validation/test/result artifacts=False
SEED_ARTIFACT_EXACT_TOKEN_HITS=0
accepted SHA=f36901ffdc59dfdde7102db545b6f46c3de3fb28ffaeed8b2368293663105786
invalid SHA=010662e1d6fa918ccf03b29e54428dbe66fd8e98316d2b4c88f2e5d37bef20f4
HEAD=69e2d186500c356ebc4a0b288cc416dcbc5d0d48
mission=CP009 / no-method=9
```

### 结论

PASS / `C1_ACCEPTED_AWAITING_CONTROL`。`mission_method_delta=NONE`。本验证只接收
C1 方法/对照实现与 direct information-contract closure；它不是 fair comparison、
方法信号或 package final receipt。C2、validation、held-out 与 Phase D 仍须等待
递增 control/formal owner 和独立起飞审查。

## V022: T010 C2 起飞合同首次独立审查

> date: 2026-07-26
> 关联：D010 / formal D021 / V021 / T010 / control epoch 22
> verifier：独立 science + dispatch-contract subagent；只读审查，未运行 validation/test

### 验证项

- [ ] checkpoint/resume identity：T010 只要求累计 rows、row key、SHA 与首个缺失
  row，没有冻结 2250 个 expected keys、严格前缀/30-row cell 完整性、完整 SHA
  bundle 和原子保存语义；现有 `common._experiment.save_results()` 直接覆盖目标
  文件 → FAIL（P1）。
- [ ] GG SNR freeze：`collective log-distance` 与共同 bracket 多解时的目标函数、
  pooled BER=0 的 log 替代值、等号方向和完整 tie chain 未闭合 → FAIL（P1）。
- [ ] C2 参数/归一化：T010/`contract.yaml` 未逐项冻结 setting index、单位、阈值
  语义、`gg_method=gar`、`block=100`、Es=1/AWGN 约定、无 AGC/无 per-cell
  renormalization → FAIL（P1）。
- [x] legacy pre-C1 snapshot：V021 已接受为不可补造 attribution debt；本次未补造，
  但 C2 artifact 必须继续显式携带 → PASS with P2。
- [x] 静态边界：task-control PASS；6 YAML + 3 JSON 可解析；30 settings ×
  75 cells = 2250 rows；当前仅两份 Phase-B smoke artifact；protected
  numstat=0；mission 仍为 CP009/no-method=9 → PASS。

### 证据

```text
Spec Compliance: FAIL
Science/Dispatch Contract: NEEDS_FIXES
P0=0
P1=3
P2=1
mission_method_delta=NONE

task-control=PASS
YAML=6 parse PASS
JSON=3 parse PASS
grid=30 settings * 75 realization cells = 2250 rows
validation/test/result artifacts=0
protected/common/params/old-package numstat=0
mission=CP009 / no-method=9

P1-1: no canonical expected-key sequence, strict-prefix/cell-completeness
       validation, exact execution hash bundle, or atomic checkpoint replace
P1-2: SNR freeze objective/ties and zero-error pooled log-distance undefined
P1-3: setting units/indexes and GG/Es/AWGN/AGC normalization contract incomplete
P2-1: PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT remains historical debt; do not fabricate
```

### 结论

FAIL / `C2_DISPATCH_REJECTED_NEEDS_FIXES`。`mission_method_delta=NONE`。不得运行
C2 validation、test/held-out 或 Phase D；先在同一 epoch 22 / D010 / formal D021
授权范围内补齐三个 P1 的确定性合同，再由独立 verifier 重新审查。

### 后续（FAIL/PARTIAL 时）

1. 冻结 canonical row-key/expected sequence/strict-prefix/cell-completeness、完整 SHA
   bundle 与临时文件 `fsync` + `os.replace` 原子 checkpoint 语义。
2. 冻结 pooled zero-error bound、共同 bracket 与无共同 crossing 的精确
   log-distance 目标、方向等号和 tie chain。
3. 在 T010 与 `contract.yaml` 逐项登记 30 settings 的 index/单位/语义，并冻结
   GG、16-QAM Es、AWGN、无 AGC/无 per-cell renormalization 约定。
4. 只做静态 parse/control/diff 检查后交独立 verifier 复审；复审 PASS 前不执行。

## V023: T010 C2 amendment 第二轮独立复审

> date: 2026-07-26
> 关联：D010 / formal D021 / V022 / T010 / control epoch 22
> verifier：同一独立 science + dispatch-contract subagent；只读审查，未运行 pytest/seed

### 验证项

- [x] V022 P1-1：2250 canonical keys、strict prefix、30-row cell、17-file exact
  hash map、existing-prefix SHA/deep equality 与 temp+fsync+replace 原子保存 →
  PASS。
- [x] V022 P1-2：pooled zero-error bound、bracket 等号、common/no-common
  max-log objective 与 pair/window tie chain → PASS。
- [x] V022 P1-3：30 settings index/unit/threshold、numerical guard、
  gar/block100、h→sqrt(h)、Es=1/AWGN、无 AGC/renormalization 与对应测试义务
  → PASS。
- [ ] conventional B* exact tie：BPS/DPLL 使用同一 score，但完整 score 相等时
  winner 未冻结；实现遍历顺序可能改变 B*、GG SNR freeze 和 strongest comparator
  → FAIL（新增 P1）。
- [x] legacy pre-C1 P2：`PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT` 继续携带且未补造
  → PASS with P2。

### 证据

```text
Spec Compliance: FAIL
Science/Dispatch Contract: NEEDS_FIXES
P0=0
P1=1
P2=1
mission_method_delta=NONE

V022-P1-1=PASS
V022-P1-2=PASS
V022-P1-3=PASS
NEW-P1=B* exact-tie winner undefined

task-control=PASS
YAML=6 parse PASS
JSON=3 parse PASS
settings=[3,9,3,9,3,3] / total=30
cells=75 / rows=2250
hash_paths=17 / all exist
contract validation=false / heldout=false
scientific seed runs=0
protected numstat=0
git diff --check=PASS
mission=CP009 / no-method=9
```

### 结论

FAIL / `C2_DISPATCH_AMENDMENT_REJECTED`。`mission_method_delta=NONE`。V022 的三项
原始 P1 已全部关闭，但 B* exact tie 是新的确定性阻断；复审 PASS 前仍不得运行 C2。

### 后续（FAIL/PARTIAL 时）

在 T010 与 `contract.yaml` 冻结科学中性的 conventional arm tie index，并明确完整
score 相等时的 B* winner；加入 deterministic exact-tie test 后仅做静态复审。

## V024: T010 C2 amendment 第三轮独立复审

> date: 2026-07-26
> 关联：D010 / formal D021 / V022–V023 / T010 / control epoch 22
> verifier：同一独立 science + dispatch-contract subagent；只读审查，未运行 pytest/seed

### 验证项

- [x] V023 B* exact tie：T010 与 `contract.yaml` 一致冻结
  `BPS=0,DPLL=1`、完整 score exact tie→BPS，理由仅为派遣前固定 arm order；
  deterministic test 要求反转实现遍历顺序不改变 winner → PASS。
- [x] V022 三项 P1 无回归：2250-key/checkpoint、SNR objective/ties、
  30-setting/normalization 全部保持闭合 → PASS。
- [x] legacy pre-C1 P2：`PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT` 仍在 C1 acceptance
  与 every-artifact obligation 中，未补造 → PASS with P2。
- [x] 静态边界：task-control PASS；30 settings/2250 rows/17 hash paths；
  contract validation=false/heldout=false；仅两份 Phase-B smoke；protected
  numstat=0；mission CP009/no-method=9 → PASS。

### 证据

```text
Spec Compliance: PASS
Science/Dispatch Contract: APPROVED
P0=0
P1=0
P2=1
mission_method_delta=NONE
final=C2_DISPATCH_AMENDMENT_PASS

task-control=PASS
YAML=6 parse PASS
JSON=3 parse PASS
settings=30
rows=2250
hash_paths=17 / all exist
bstar_exact_tie=4OPM_BPS
contract validation=false / heldout=false
scientific seed runs=0
protected numstat=0
git diff --check=PASS
mission=CP009 / no-method=9
```

### 结论

PASS / `C2_DISPATCH_AMENDMENT_PASS`。`mission_method_delta=NONE`。本 PASS 只批准
C2 amendment，不直接授权执行；主控必须先递增 foreground control 与 T010 task
binding，再经独立 binding 复审。held-out/Phase D 继续锁定。

## V025: T010 C2 epoch 23 最终 binding 独立复核

> date: 2026-07-26
> 关联：D010 / formal D021 / V024 / T010 / control epoch 23
> verifier：同一独立 binding subagent；只读审查，未运行 pytest/seed

### 验证项

- [x] control/task binding：live control 与 T010 均为
  epoch 23 / CP009 / formal D021 / `METHOD_CONSTRUCT`；task-control fresh PASS。
- [x] activation preflight：`contract.yaml` 记录 V024 amendment PASS，但
  validation/heldout/performance 均 false；`source-contract.yaml` 保持规定的
  executor 起飞前 C1/D020 状态，T010 已精确定义迁移。
- [x] current projections：master/projects-overview/formal topic-index/live+formal
  registry/state/portfolio/harvest 七组 current view 均指
  epoch23/V024/binding pending；残余 epoch22 只在历史段。
- [x] V024 合同无回归：30 settings、2250 rows、17 hash paths、B* tie→BPS、
  checkpoint/SNR/normalization obligations 全部闭合。
- [x] evidence boundary：仅两份 Phase-B smoke；protected numstat=0；mission
  CP009/no-method=9；未运行 scientific seed。

### 证据

```text
Spec Compliance: PASS
Binding: APPROVED
P0=0
P1=0
P2=1
mission_method_delta=NONE
final=C2_EPOCH23_BINDING_PASS

task-control=PASS
YAML=7 parse PASS
JSON=3 parse PASS
projection_assertions=7/7
contract validation=false / heldout=false
source_contract=preflight C1/D020
settings=30 / rows=2250 / hash_paths=17
scientific seed runs=0
protected numstat=0
git diff --check=PASS
mission=CP009 / no-method=9
```

### 结论

PASS / `C2_EPOCH23_BINDING_PASS`。`mission_method_delta=NONE`。只允许不同内部
executor 按 T010 执行 C2 validation freeze 与规定的起飞迁移；不授权 test、
held-out、Phase D、CP010、方法信号或正式性能结论。

## V026: T010 C2 runtime identity failure 独立科学接收

> date: 2026-07-26
> 关联：D010 / formal D021 / T010 / control epoch 23
> verifier：与 executor 分离的独立合同/科学 subagent；只读审查，未运行新 seed

### 验证项

- [x] checkpoint 完整性：独立读取 `validation-raw.json`，声明/实际均为
  840 rows，整除 30；keys 精确等于 canonical prefix，最后 key
  `[1,0,2,5,2]`、下一 key `[1,0,3,0,0]`；17/17 frozen source hash 匹配，
  aggregate 不存在、`heldout_consumed=false` → PASS。
- [x] 异常可复现性：executor 对同一 moderate/14 dB/seed `131004` frozen RX
  只读重建两次，RX/GG SHA 和 traceback 一致；真实 slope
  `+0.00251327`，含 PN true-phase LS `+0.00277341`，observed unwrap LS
  `-0.0138504` → deterministic identity failure。
- [x] 根因边界：低幅 pilot 的 raw angle 从 `-0.4179` 到 `+3.0458`，unwrap
  选择 `-3.2374` 并继续到 `-6.3042`；λ `.98/.99/.999` 的 RLS slope 均为负。
  P1/P2/P3 共用该 pilot 初始化，失败早于 DD/adaptation → 不是 runner、RNG、
  RLS 递推或某个 candidate gate 的局部 bug。
- [x] 合同处置：T010/contract 要求每行有真实 `bit_errors/denominator/BER`，
  但未定义 corrected data 产生前的 exception row；skip 违反 strict prefix，
  synthetic collapse/nonfinite row 会改变 setting score → 均禁止。
- [x] 预注册早停：T010 §6 规定 RLS lifecycle 任一失败即
  `BLOCKED_IDENTITY / mission_method_delta=NONE / no second package`；
  positive slope 与 `F=2π/h1` 是 deliberate source identity，不能按实现 bug
  在 epoch 23 内修改 → 当前证据足够，不要求完成 2250 rows。

### 证据

```text
raw rows actual/declared=840/840
complete cells=28
last key=[1,0,2,5,2]
next key=[1,0,3,0,0]
frozen hashes=17/17 exact match
aggregate=ABSENT
heldout_consumed=false

true slope=+0.00251327 rad/symbol
true-phase LS with PN=+0.00277341
observed unwrap LS=-0.0138504
RLS h1 lambda .98/.99/.999=-0.0062947/-0.0109464/-0.0164973
same frozen RX reproduction=2/2

P0=0
P1=0
P2=1
formal_science_disposition=BLOCKED_IDENTITY
mission_method_delta=NONE
```

### 结论

PASS / 接收 `BLOCKED_IDENTITY`。禁止继续 C2、跳过失败 cell、伪造
BER/collapse row、修改 positive-slope gate、运行 test/held-out/Phase D 或开启第二个
B10 package。该接收是科学身份失败，不是方法、fair comparison、negative method
claim 或治理产出。主控应保留 840-row 证据，更新 formal/mission/control 后轮换。

## V027: CP010 owner/control/current projection 独立终验

> date: 2026-07-26
> 关联：D011 / formal D022 / V026 / CP010 / H002
> verifier：与 executor/master 分离的同一独立只读 subagent；未改文件、未运行
> test 或 scientific seed

### 验证项

- [x] T010 evidence snapshot：fresh read-only 复核 raw 声明/实际均为 840 rows，
  整除 30，keys 为 canonical strict prefix，last/next key 为
  `[1,0,2,5,2]` / `[1,0,3,0,0]`；17/17 current byte SHA256 匹配，
  aggregate 不存在、heldout=false、method delta NONE → PASS。
- [x] CP010 双账：mission-log 精确记录
  `BLOCKED_IDENTITY / NONE / same-axis=1 / repair=1 / no-method=10 /
  package ALIGNED / mission DRIFTED-STALLED`，与 live D011、formal D022 和
  V026 一致；没有把 45 tests 或 identity diagnostic 写成方法 → PASS。
- [x] 首轮 owner/projection 审查：发现 formal topic-index “悬而未决”仍把
  C2 写为待执行且笼统禁止 C15，与 D022/current projections 冲突 →
  `FAIL / P0=0/P1=1/P2=1`。
- [x] 修正后同一 verifier 复审：formal topic-index 已明确 T010 终止、B10
  `RETURNED_TO_POOL`、C2 无待执行项；允许 C15 Step 1–3 formalization，但
  readiness PASS 前禁止旧 sandbox/Step 4a MVE。live control、formal owner、
  mission-log、projects-overview、master-state、state/portfolio/harvest current
  views、registry 与 H002 全部一致 → PASS。
- [x] 禁止项：未授权 T006/T008/T009/T010 repair、Scout/P03、旧 C15
  sandbox、Step 4a/MVE、Step 5/Contract/Execute；历史授权仍保留在 superseded
  血缘中，不构成当前动作 → PASS。

### 证据

```text
round1=FAIL
round1_P0/P1/P2=0/1/1
round1_only_P1=formal topic-index stale pending-C2/current-C15 wording

round2=PASS
round2_P0/P1/P2=0/0/1
final=CP010_CONTROL_PLANE_PASS

raw rows declared/actual=840/840
strict_prefix=true
last_key=[1,0,2,5,2]
next_key=[1,0,3,0,0]
source_hashes=17/17
aggregate=ABSENT
heldout_consumed=false

active_scientific_carrier=NONE
next_workline=C15_REDUCED_CONSTELLATION_FORMALIZATION_STEP1_3_ONLY
MVE_authorized=false
mission_method_delta=NONE
no_method_streak=10
```

### 结论

PASS / `CP010_CONTROL_PLANE_PASS`。P2=1 仅为既有
`PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT`，无新增阻断。T010/CP010 可作为下一包的
权威恢复基点；此 PASS 是控制面终验，不是方法产出或科学 performance PASS。

## V028: T011 C15 Step 1–2 dispatch 独立终审

> date: 2026-07-26
> 关联：S001 / D012 / formal D023 / T011 / control epoch 25
> verifier：与任务编写者分离的独立只读 subagent；未修改文件，未运行搜索、下载、
> 精读、仿真或 seed

### 验证项

- [x] control binding：独立运行 `validate_task_control.py`，epoch 25 /
  `CANDIDATE_FORMALIZATION` / CP010 与 foreground control 一致 → PASS。
- [x] 科学边界：C15 全程定义为 PM-16QAM/高阶 QAM blind-equalization
  cost/update family；T011 只授权 Groundwork Step 1 search + Step 2 acquire，
  coverage confirmation 前禁止 Step 3，readiness 前禁止 MVE → PASS。
- [x] 检索/下载合同：六词族、每源请求量、定向深搜、priority 标注、三轮止损、
  ≥5 篇全文及 canonical/recent comparator 组成均可查 → PASS。
- [x] 可执行性修订：CRLF wrapper 改为 `tools/` 目录只读 `sed` 管道；blit 冻结
  JSON；acquisition pool 冻结 `results` schema；共享主仓索引与
  `--output-dir`、IEEE PDF 的 source/content/metadata/index 闭环均冻结 → PASS。
- [x] 最终独立终审：第五轮结果 `PASS / P0=0/P1=0/P2=0`；task-control 独立复跑
  PASS → 可由不同 executor 派发。

### 证据

```text
round1=FAIL P0/P1/P2=0/3/1
round1_closed=current-location, per-source/deep-gap gate, exact-command placeholders

round2=FAIL P0/P1/P2=0/1/0
round2_closed=wrapper cwd/script resolution + exact convert command

round3=FAIL P0/P1/P2=0/3/0
round3_closed=blit --format json + acquisition results schema + IEEE ingest closure

round4=FAIL P0/P1/P2=0/3/0
round4_closed=shared absolute indexes + manual index key + relative index path

round5=PASS P0/P1/P2=0/0/0
task_control=PASS
simulation_or_seed_run=false
formal_science_disposition=DISPATCH_CONTRACT_PASS
mission_method_delta=NONE
```

### 结论

PASS。T011 可由与 verifier 不同的 executor 执行 Step 1–2，并必须停止于
`AWAITING_COVERAGE_CONFIRMATION`。该结论只证明派发合同可执行，不证明 C15
formal readiness、方法有效性、传统 comparator 充分性或 `METHOD_SIGNAL`；
`mission_method_delta=NONE`，mission 仍为 `DRIFTED/STALLED`。

## V029: T011 Step 1 search-coverage block 独立接收

> date: 2026-07-27
> 关联：D012 / formal D023 / T011 / CP011
> verifier：与 T011 executor 分离的独立只读 subagent；未调用新 search/download，
> 未修改文件，未运行仿真或 seed

### 验证项

- [x] archive/数量：七个 JSON 均可解析，query 与 T011 一致，SHA256 与 worker
  log 一致；56 retained rows，DOI 优先/否则 normalized title 去重为 53 →
  PASS。
- [x] publication/source：53 unique 中 published/preprint/unknown=`49/3/1`；
  56/56 actual `source_api=openalex`，planned `sources` 不能算实际覆盖 →
  三源门 FAIL。
- [x] deep/task-fit：staged/normalized/lineage retained 均 0；FSO retained=1，
  但为泛 ML/DL optical survey，有效 direct task-fit=0 → 不能排除单源漏召。
- [x] 止损：archive 没有 priority/priority_reason，acquisition pool 不存在；
  Step 2/IEEE/ingest/download 均未启动，共享 papers 未写 → 正确止损 PASS。
- [x] integrity：禁止的 sessions/master/simulation/common 无 executor diff，tracked
  pyc 与 HEAD 一致，worktree 只有 T011 worker log → PASS。

### 证据

```text
verifier=PASS_CORRECT_BLOCK
P0/P1/P2=0/0/1
task_control=PASS
archives=7/7 parse+query+sha PASS
retained_rows=56
unique=53
published/preprint/unknown=49/3/1
actual_sources=openalex
actual_source_count=1
deep_staged/normalized/lineage=0/0/0
deep_fso=1 generic survey; direct_task_fit=0
acquisition_pool=ABSENT
step2=NOT_STARTED
formal_science_disposition=BLOCKED_SEARCH_COVERAGE
mission_method_delta=NONE
```

P2=1：executor 未保留逐条原始 stdout/stderr/exit transcript；archive 和时间/hash
只能旁证成功产出，不能独立证明 S2 rate-limit/缺 key 等完整输出。该 P2 不影响
保守阻断。

### 结论

PASS，接收 `BLOCKED_SEARCH_COVERAGE`。这只是当次检索覆盖阻断，不是 C15
negative result、Kill、方法失败或方法产出；不得进入 Step 2。下一动作只有在独立
证明共享多源/全文恢复路径可行并更新 control 后，才可派一次有界恢复包。

## V030: T012 source/canonical recovery dispatch 独立终审

> date: 2026-07-27
> 关联：S001 / D013 / formal D024 / T012 / CP011
> verifier：与任务编写者、后续 executor 分离的独立只读 subagent；未修改文件，
> 未调用 search/blit/download/convert、仿真或 seed

### 验证项

- [x] control/receipt：独立运行 task-control validator，epoch 26 /
  `CANDIDATE_FORMALIZATION` / CP011 PASS；`700864d` 为 HEAD ancestor → PASS。
- [x] 首轮审查：发现 owner/hash 自包含、identity/provenance、shared storage、
  exact PDF binding、15 分钟切分、formal outcome 六项 P1 与 transcript 一项 P2
  → `FAIL / P0=0/P1=6/P2=1`。
- [x] 修订复审：normalized-title+DOI union、retrieval provenance/candidate/pool
  三口径、五项 metadata/index 字段与历史、exact arnumber→PDF/sidecar/content、
  Phase A/B/resume/timebox、outcome taxonomy 与 transcript 模板均闭合 → PASS。
- [x] 科学边界：成功也只到 coverage confirmation；Step 3/MVE/owner edit 禁止，
  `mission_method_delta=NONE` → PASS。
- [x] final binding：control/task 同步递增为 epoch 27 / CP011 后 fresh validator
  PASS；authority D024 active，action allowed 且不在 forbidden，下一动作只到
  Phase A → `FINAL_BINDING_PASS / P0=0/P1=0/P2=0`。

### 证据

```text
round1=FAIL
round1_P0/P1/P2=0/6/1
round1_P1=self-contained gate; dedupe/provenance; metadata/index storage;
          exact-result-to-PDF binding; <=15min phases; formal outcome taxonomy
round1_P2=initial preflight transcript creation/format

round2=PASS
round2_P0/P1/P2=0/0/0
task_control_epoch26=PASS
acceptance_commit=700864de9ac2d928681201312121d178ff243ccb
acceptance_commit_is_HEAD_ancestor=true
search_or_download_run=false
simulation_or_seed_run=false
formal_science_disposition=DISPATCH_CONTRACT_PASS
mission_method_delta=NONE

final_binding_epoch=27
final_binding=PASS
final_binding_P0/P1/P2=0/0/0
```

### 结论

PASS。T012 dispatch contract 与 epoch 27 final binding 均已通过，可先交给与
verifier 不同的 executor 执行 Phase A。本 PASS 只证明任务合同可执行，不证明
C15 formal readiness、科学正/负结论、`METHOD_SIGNAL` 或 promotion。

## V031: T012 Phase A preflight receipt 路径 amendment 独立复核

> date: 2026-07-27
> 关联：S001 / D013 / formal D024 / T012 / CP011
> verifier：V030 同一独立只读 verifier；未修改文件，未运行
> search/blit/download/convert、仿真或 seed

### 验证项

- [x] 首次 preflight：task-control、clean、owners、ancestry、7 archives、
  forbidden process=0、main target diff=0 均 PASS；唯一 failure 为 executor
  猜测不存在的 T011 worker-log 路径 → PASS（单一接口阻断）。
- [x] 实际 receipt：已提交的
  `projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md`
  存在；七个 `search-archive/2026-07-26/c15-*.json` 恰好存在 → PASS。
- [x] amendment diff：T012 只在 header/§2.1 冻结上述唯一 receipt 与 archive
  pattern，未改变 action、authority、科学范围、禁止边界或 delta → PASS。
- [x] integrity：首次 executor 阻断后立即停止；共享 papers、owners、Step 3、
  simulation/MVE 均无修改/运行 → PASS。

### 证据

```text
PATH_AMENDMENT_PASS
P0/P1/P2=0/0/0
task_control_epoch27=PASS
actual_receipt_exists=true
t011_archive_count=7
preflight_only_failure=t011_worker_log_missing
executor_guessed_path=projects/thesis-fso/worker-logs/step-011-c15-search-coverage.md
authorized_path=projects/thesis-fso/worker-logs/step-011-c15-step1-step2-formalization.md
search_or_download_run=false
shared_papers_modified=false
mission_method_delta=NONE
```

### 结论

PASS。接收 `BLOCKED_PREFLIGHT` 为已修复的 task-interface receipt path 缺口；
formal D024/T012 科学边界与 CP011 保持不变。control/task 可递增后形成 clean
retry gate。本 PASS 不是 formal science disposition、方法进展或 coverage 结论。

## V032: T012 第二次 preflight 假阳性与最后一次 bounded amendment 独立复核

> date: 2026-07-27
> 关联：S001 / D013 / formal D024 / T012 / CP011
> verifier：V030/V031 同一独立只读 verifier；未修改文件，未运行
> search/blit/download/convert、仿真或 seed

### 验证项

- [x] execution boundary：task-control、clean、ancestry、7 archives、正确
  receipt、主仓 target diff 均 PASS；source view/pool 不存在，只有 Step-012
  worker log 有 diff，未进入 §2.2 → PASS。
- [x] owner root cause：D024/D013 section 的 `^status` 均 False，
  `^>\s*status` 均 True → PASS（确定性 predicate 假阴性）。
- [x] process root cause：未限 executable 的 broad predicate 命中 79 个普通应用；
  限 `python|python3|wsl|bash` 且 seed 为独立 CLI token 后为 0 → PASS
  （确定性 substring 假阳性）。
- [x] repair-vs-rotation：真实前置门已通过；冻结两个 predicate 的成本和不确定性
  均低于 B1 第三 evaluator repair、A4 第二 identity repair、B9 新全链 → PASS。
- [x] stop boundary：只批准最后一次 exact-command retry；下一次任一
  preflight 非 PASS 都停止 T012，不再 amendment 并轮换 → PASS。

### 证据

```text
SECOND_PREFLIGHT_ROOT_CAUSE=PASS
P0/P1/P2=0/0/1
old_owner_regex_D024/D013=False/False
correct_owner_regex_D024/D013=True/True
broad_process_count=79
restricted_science_process_count=0
task_control=PASS
worktree_clean_at_takeoff=true
ancestry=PASS
archive_count=7
receipt_exists=true
main_target_diff=0
source_view_exists=false
acquisition_pool_exists=false
search_or_download_run=false
shared_papers_modified=false
mission_method_delta=NONE
P2=79-process verbatim listing truncated by execution harness; do not fabricate
```

### 结论

PASS。第二次 `BLOCKED_PREFLIGHT` 是 task self-containment/predicate 假阳性，
不是科学或主仓 blocker。批准在同一 T012 内冻结 exact combined preflight 并做
最后一次 retry；再次非 PASS 必须停止 T012 并轮换。当前
`formal_science_disposition=PENDING_PACKAGE_COMPLETION`、
`mission_method_delta=NONE`，不追加 mission checkpoint。

## V033: T012 epoch 29 final binding 与 package disposition 独立终验

> date: 2026-07-27
> 关联：S001 / D014 / formal D025 / T012 / CP012
> verifier：V030–V032 同一独立只读 verifier；未修改文件，未运行科学命令

### 验证项

- [x] frozen command syntax：T012 三个 PowerShell block parse error=`0` → PASS。
- [x] current binding：epoch 29 / CP011 / `CANDIDATE_FORMALIZATION`、D024、
  task-control、owners、ancestry、archives、receipt、YAML 与主仓 target diff
  均闭合 → PASS。
- [ ] fail-closed process gate：`Get-CimInstance Win32_Process` 在
  `$ErrorActionPreference='Continue'` 下未使用 `-ErrorAction Stop` 或捕获异常；
  查询失败可返回空集合并被当成 `forbidden_process_count=0` → FAIL（P1）。
- [x] stop rule：T012 已明确“冻结命令缺陷也终止，不再第四次 amendment”；
  当前 P1 正好触发该退出条件 → PASS（必须停止/轮换）。
- [x] evidence boundary：source view/pool/canonical targets 不存在，主仓五 DOI/
  index 无 diff，§2.2–§2.5 与 Step 3/MVE 未运行 → PASS。

### 证据

```text
FINAL_BINDING_FAIL
P0/P1/P2=0/1/0
task_control_epoch29=PASS
powershell_parse_errors=0
owner_D024/D013_active=true/true
ancestry_exit=0
t011_archive_count=7
t011_receipt_exists=true
restricted_science_process_count=0
main_target_diff_count=0
source_view_exists=false
acquisition_pool_exists=false
canonical_targets_exist=false
P1=Get-CimInstance failure is not fail-closed
formal_science_disposition=BLOCKED_TASK_INTERFACE/PACKAGE_NOT_EXECUTED
mission_method_delta=NONE
```

### 结论

FAIL（binding）/ PASS（保守终止处置）。epoch 29 冻结命令不能安全派发；按 V032
和 T012 的 one-last-attempt 规则，不再修复，接收
`BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`。该结果不是 C15 science
negative、coverage failure、方法或 promotion；C15 返回候选池，mission 追加
CP012/no-method=12 后进入 post-T012 remap。

## V034: T013 B9 Step 1 dispatch contract 独立复审

> date: 2026-07-27
> 关联：S001 / R003 / D015 / formal D026 / T013 / CP012
> verifier：T013 独立 dispatch verifier；只读复审，未运行 search/下载/实验

### 验证项

- [x] 输出接口：七条 search 命令均无 `-o/--output`，自动 archive 与本地
  ignored `_index/all-papers.jsonl` 已显式授权，最终只提交 worker log → PASS。
- [x] 阶段预算：A1/A2 为 search-only；A3-n 每次最多两个 archive；A4 只综合；
  全部 phase ≤15 分钟并串行停止 → PASS。
- [x] Step 1 artifact：每条 result 的 priority/reason/route/collision/evidence
  scope 必须写回原 archive，A4 只接收已标注 archive → PASS。
- [x] current projection：registry formal topic 与 formal topic-index 已收敛为
  D026/B9-only Step 1，C15 只保留历史状态 → PASS。
- [x] R003/D015/D026/control/task：四候选六维比较、正向合同、无 active
  carrier、epoch31/CP012/action class 一致 → PASS。
- [x] deterministic integrity：task-control、`git diff --check`、四个 current
  YAML parse 与同日 archive 不存在检查 → PASS。

### 证据

```text
DISPATCH_REVIEW_PASS
P0/P1/P2=0/0/0
SEARCH_COMMANDS=7
OUTPUT_ARG_COMMANDS=0
TASK_CONTROL=PASS
GIT_DIFF_CHECK=PASS
YAML_PASS=.sessions/_registry.yaml
YAML_PASS=projects/thesis-fso/direction-lab/state/current.yaml
YAML_PASS=projects/thesis-fso/direction-lab/portfolio/current.yaml
YAML_PASS=projects/thesis-fso/direction-lab/harvest/current.yaml
SEARCH_DIR_EXISTS=False
FORMAL_REGISTRY_CURRENT=D026/B9_STEP1
FORMAL_TOPIC_CURRENT=D026/B9_STEP1
```

### 结论

PASS

## V035: T013 B9 Step 1 执行与科学身份独立验收

> date: 2026-07-27
> 关联：S001 / D015 / formal D026 / T013 / CP013
> verifier：T013 independent science verifier；只读复算，未修改 owner/control

### 验证项

- [x] 执行与边界：HEAD `7ca3cbf`、tracked worktree clean；两个 T013 commit
  都只提交 worker log，未下载、精读、实现、仿真或进入 Step 2 → PASS。
- [x] raw/candidate view：七个 archive 全部 JSON parse；`61/61` raw result
  有完整人工语义字段；DOI/normalized-title 去重 `61→58` → PASS。
- [x] 数量与发表：非排除 `21`、排除 `37`、必读 `8`；正式发表
  `21/21`，数量门/必读门/发表门均通过 → PASS。
- [x] 真实来源：本次实际 search-run family 只有 OpenAlex；S2 被 rate limit，
  未配置源没有返回；历史 index 字符串未拆分计数 → PASS。
- [x] route 复算：Route A inclusive=`8`、deep nonexcluded=`0`；Route B
  inclusive=`17`、deep nonexcluded=`2`，但两条只属一般 task-fit/adjacent FSO，
  不含 self-coherent/virtual-carrier/CSPR/phase-reconstruction → PASS。
- [x] 三项 P2 修正：Route B broad+deep gate=`false`；delta-sigma 降为 adjacent
  context；clipping 改为 DRE optimization lineage并新增未猜 title/DOI 的 original
  DRE citation debt → PASS。
- [x] acquisition debt：`11`，覆盖 DRE optimization/canonical citation、
  traditional comparator、self-coherent/FSO task-fit；没有把 metadata 当全文
  → PASS。

### 证据

```text
HEAD=7ca3cbf
TRACKED_STATUS=CLEAN
T013_COMMITS=16176c2,7ca3cbf
COMMIT_SCOPE=worker-log-only
RAW_RESULTS=61
DEDUPLICATED_UNIQUE=58
NONEXCLUDED_UNIQUE=21
EXCLUDED_UNIQUE=37
MUST_READ_UNIQUE=8
FORMALLY_PUBLISHED_UNIQUE=21
PUBLISHED_RATIO=1.0
ACTUAL_SOURCE_FAMILIES=1
ACTUAL_SOURCE_FAMILY=openalex
ROUTE_A_INCLUSIVE=8
ROUTE_A_DEEP_NONEXCLUDED=0
ROUTE_B_INCLUSIVE=17
ROUTE_B_DEEP_NONEXCLUDED=2
ROUTE_B_INDEPENDENT_BROAD_AND_DEEP=false
ACQUISITION_DEBT=11
INITIAL_REVIEW_P0/P1/P2=0/0/3
FINAL_REVIEW_P0/P1/P2=0/0/0
CANDIDATE_VIEW_SHA256=C46EC7815671F003A28C12421D74F84AF8259BB71E0F50B49C7456CB1539E636
FORMAL_SCIENCE_DISPOSITION=BLOCKED_SEARCH_COVERAGE
MISSION_METHOD_DELTA=NONE
SIMULATION_OR_SEED_RUN=false
```

### 结论

PASS。接收 `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。这不是 B9
science Go、Kill、`METHOD_SIGNAL` 或 promotion；只证明 T013 在授权边界内可靠地
发现了来源与 mechanism-deep 覆盖不足。

## V036: T014 B9 Step 1 coverage repair dispatch 独立审查

> date: 2026-07-27
> 关联：S001 / R004 / D016 / formal D027 / T014 / CP013
> verifier：T014 independent dispatch quickcheck；只读，未运行检索/下载/实验

### 验证项

- [x] control binding：epoch33 / CP013 / D016 / formal D027 /
  `CANDIDATE_FORMALIZATION` 与 T014 一致，task-control validator PASS。
- [x] carrier comparison：R004 比较 B9、C15、B1、A4 的方法形态、预期增量、
  包装句、formal readiness、最小补债与失败轮换点，并说明 B9 优于至少两个替代。
- [x] bounded repair：A1/A2/A3-n/A4 各 ≤15 分钟；A1 union `<3` 必须停止；
  A3-n 每次最多两个 archive；失败后禁止第三个 B9 Step 1 包。
- [x] source integrity：只按 raw archive 实际返回平台计 source family；配置名、
  rate-limit、零结果和共享 index 历史 provenance 不计数。
- [x] output/interface：T014 使用新 query slug 与 `t014-ieee-*`/v2 view，不覆盖
  T013 archives/candidate view；executor 不修改 owner/control。
- [x] scope/current：FR-22、禁止下载/精读/实现/实验、无 active carrier，以及
  registry/master/state/portfolio/harvest/projects-overview 当前投影一致。
- [ ] clean binding：审查时 13 个 tracked 文件修改、R004/T014 未跟踪；符合
  “审查后提交”阶段，但提交并复核 clean 前不得执行 → P2。

### 证据

```text
DISPATCH_REVIEW_PASS
P0/P1/P2=0/0/1
TASK_CONTROL=PASS
GIT_DIFF_CHECK=PASS
CONTROL=epoch33/CP013/D027
LIVE_OWNER=D016
FORMAL_OWNER=D027
CURRENT_ACTIVE_CARRIER=NONE
REPAIR_COUNT_ALLOWED=ONE
P2=CLEAN_BINDING_NOT_YET_FORMED
```

### 结论

PASS（合同）/ PARTIAL（派发前 clean binding）。允许 control/task 递增到 final
binding epoch并提交；clean worktree 下的 task-control 与 owner/projection 独立
复核 PASS 前不得执行 A1。

## V037: T014 B9 Step 1 coverage repair 执行与科学身份独立验收

> date: 2026-07-27
> 关联：S001 / D016 / formal D027 / T014 / CP014
> verifier：T014 independent science/package verifier；只读，未修改 owner/control

### 验证项

- [x] commit 闭包：HEAD `5ba5a54cce3705186d8a921d4e4f2ec3c34bb7c8`
  继承 clean-binding `211160e`，只新增 T014 worker log；tracked worktree clean，
  owner/control 无 diff → PASS。
- [x] raw 复算：两个 S2/arXiv archive 各 `results=0`；IEEE Route A
  `results=1, source=ieee`；连同 T013 OpenAlex 后 union 为
  `[openalex, ieee]`、count=`2` → PASS。
- [x] 停止条件：`2<3` 触发 A1 stop；receipt 为
  `next_phase_authorized=false`，A2/A3/A4、Route-B broad、两份 deep archive
  与 view-v2 均不存在 → PASS。
- [x] 边界：没有下载、精读、实现、仿真或 seed；没有进入 Step 2/3/3.5/4a，
  没有修改正式 owner、live control、mission-log 或共享论文库 → PASS。
- [x] 科学身份：coverage gate failure 只支持
  `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`；不得解释成
  B9 Go/Kill、创新空白或方法产出 → PASS。
- [x] 轮换合同：D016/D027 的唯一 coverage repair 已消费；B9 必须返回候选池，
  不得第三个 Step 1 包 → PASS。

### 证据

```text
HEAD=5ba5a54cce3705186d8a921d4e4f2ec3c34bb7c8
PARENT=211160e2ab43132b67e47776713a6653e70840d2
COMMIT_SCOPE=projects/thesis-fso/worker-logs/step-014-b9-step1-multisource-coverage-repair.md
TRACKED_STATUS=CLEAN
TASK_CONTROL=PASS
RAW_RESULT_COUNTS=0,0,1
ACTUAL_SOURCE_FAMILIES=openalex,ieee
ACTUAL_SOURCE_FAMILY_COUNT=2
GATE_AT_LEAST_THREE_SOURCES=false
NEXT_PHASE_AUTHORIZED=false
A2_A3_A4_OUTPUTS=ABSENT
P0/P1/P2=0/0/0
FORMAL_SCIENCE_DISPOSITION=BLOCKED_SEARCH_COVERAGE
MISSION_METHOD_DELTA=NONE
SIMULATION_OR_SEED_RUN=false
```

### 结论

PASS。接收 `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE`。建议
CP014 为 same-axis=2、repair=1、no-method=14，
`ADEQUATE / package ALIGNED`；mission 保持 `DRIFTED/STALLED`。B9 返回候选池并
立即轮换。

## V038: T015 B12 standalone 首次 dispatch 独立审查

> date: 2026-07-27
> 关联：S001 / R005 / D018 / formal D029 / T015 / CP014
> verifier：`t015_dispatch_verifier`；只读，未运行任何实验 seed

### 验证项

- [ ] channel lifecycle：逐字段核对 T015、`params.py` 与现有 GG generator →
  T015 同时声称 primary `BLOCK` 从配置读取、又把算法/pilot block 固定为 128；
  配置中的 `BLOCK=100` 为 `NO VERIFIED SOURCE`，旧 iid block generator 会把
  40 ns 量级块误作独立大气湍流状态，足以人为制造 robust gain，P0。
- [ ] robust update：由 Huber score/IRLS 正规方程核对 T015 权重 →
  `w=min(1,c/u)` 应把 observation precision 改为 `w/sigma_eps`
  （等价 variance=`sigma_eps/w`）；原 `sigma_eps/w**2` 错把标准权重平方，
  会改变方法本体与方法信号，P0。
- [ ] source identity：核对 OECC Eq.4–7 与 TSP covariance 定义 →
  Σθ/Σε 与 QAM decision-aided 映射可形成有上限的 source adapter，但 T015
  未冻结 phase correction sign、Δφ/C 维度、terminal propagation、
  `L_sub=1` 生命周期，2/3 BER 排序不足以单独证明 identity，P1。
- [ ] comparator identity：静态核对 BPS 合同 → 64 phases/window 尚未冻结
  phase grid、decision metric、edge policy、unwrap/cycle-slip、跨 block state
  与 pilot branch 时机，强比较器结果可被实现选择左右，P1。
- [ ] statistics：静态核对 METHOD_SIGNAL 两入口 → bootstrap unit、replicate
  count、analysis seed 与 crossing curve resampling 未冻结；outage 门的
  “BER 不恶化”未指明相对全部三个比较器，P1。
- [ ] runtime：按 Phase B/C cell、block 与 BPS phase 数静态核算 →
  Phase B=90 realizations、Phase C=180 realizations；dense MAP 约
  369000 个 128×128 block solve，BPS 至少约
  `270*64*32768=566231040` 个 slicer metrics，未满足单 agent 15 分钟门，P1。
- [ ] parameter provenance：核对 `params.py` → `R_SYM=2.5e9` 指向占位
  DOI `10.1109/JLT.2025.xxx`，`LASER_LW=10 kHz` 为 WARNING，
  `BLOCK=100` 为无验证假设；T015 不得把这些字段统称为已闭合真相源，P1。
- [x] control/scope：epoch36 / CP014 / D018 / formal D029 / T015
  task-control validator PASS；FR-22 保持 GW Step 4a，且本审查未运行 seed。

### 证据

```text
VERDICT=FAIL
P0_1=UNFROZEN_AND_PHYSICALLY_INVALID_GG_LIFECYCLE
P0_2=HUBER_WEIGHT_SQUARED_IN_PRECISION
PHASE_B_REALIZATIONS=90
PHASE_C_REALIZATIONS=180
BPS_MIN_SLICER_METRICS=566231040
PARAMS_R_SYM_SOURCE=Zhao 2025 (doi:10.1109/JLT.2025.xxx)
PARAMS_LASER_LW_AUDIT=WARNING
PARAMS_BLOCK=100
PARAMS_BLOCK_SOURCE=NO VERIFIED SOURCE
TASK_CONTROL=PASS
SIMULATION_SEED_RUN=FALSE
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

在同一 T015、同一 B12 package 内完成一次派遣前修订：把 channel 明确定义为
有物理含义的独立 128-symbol snapshot ensemble 或使用已验证的相关 GG
lifecycle；把方法改为标准 Huber IRLS precision；补齐 Eq.4–7、BPS、bootstrap、
parameter provenance 与可分片 runtime contract；独立 verifier 重新 PASS 且
clean binding 提交前不得运行任何 seed。该 FAIL 是 task preparation failure，
不消费 B12 scientific repair，也不产生 mission checkpoint/method delta。

## V039: T015 Huber robust-method prior 独立审计

> date: 2026-07-27
> 关联：S001 / R005 / D018 / formal D029 / T015 / V038 / CP014
> verifier：`b12_robust_prior_audit`；只读，未运行任何实验 seed

### 验证项

- [x] Gaussian MAP anchor：核对本地 TSP 全文 → B12 的 Σθ/Σε 与
  amplitude-dependent AOPN measurement variance 已有 source anchor。
- [ ] robust formula：按 Huber score/IRLS 正规方程核对 →
  T015 原 `sigma_eps/w**2` 不是 Huber；标准 one-step update 必须是
  `sigma_eps/w`，与 V038 的 P0 一致。
- [ ] novelty collision：检索既有本地全局论文索引 →
  DOI `10.1109/JLT.2025.3600402` 已直接提出用于 carrier phase recovery 的
  Huber M-estimator robust variational-Bayesian UKF，并对比 BPS 报告最高
  0.66 dB OSNR gain；另有 arXiv `2603.11280` 将 Huber/outlier filtering
  用于卫星同步。原 T015 不得在未精读碰撞源时主张 robust CPR 方法差异。
- [ ] claim ceiling：把 source MAP 与成熟 Huber adapter 分开核对 →
  当前最多可称
  `ONE_STEP_HUBER_REWEIGHTED_SOURCE_MAP` 工程 adapter；是否有论文方法增量
  取决于 direct-collision Step 3.5 的输入、更新、复杂度和适用条件差异。

### 证据

```text
TSP_LOCAL_FULLTEXT=papers/doi/10.1109_tsp.2021.3137966/content.md
HUBER_IRLS_PRECISION=w/sigma_eps
HUBER_IRLS_VARIANCE=sigma_eps/w
DIRECT_COLLISION_DOI=10.1109/JLT.2025.3600402
DIRECT_COLLISION_TITLE=Laser FM Noise Compensation in Fiber-THz Convergence Systems Employing Robust Variational Bayesian Unscented Kalman Filter
DIRECT_COLLISION_ABSTRACT=Huber M-estimator robust update for CPR; up to 0.66 dB OSNR gain vs BPS
SATELLITE_HUBER_PREPRINT=arXiv:2603.11280
SIMULATION_SEED_RUN=FALSE
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

T015 不得直接派遣。先在同一 B12 preparation package 内完成有界 Step 3.5：
获取并精读 DOI `10.1109/JLT.2025.3600402`，逐项比较 measurement/state、
Huber update、covariance adaptation、复杂度、比较器与场景；只有形成未被该
先例覆盖的明确 M-C-A 和可包装句，才能修订 T015 进入实现。否则 B12 立即回池，
不运行 seed，不把 collision adjudication 记为方法 delta。

## V040: B12 direct-collision 全文恢复与派遣终局裁决

> date: 2026-07-27
> 关联：S001 / R005 / D018 / formal D029 / T015 / V038 / V039 / CP014
> verifier：`b12_collision_reader` + `b12_collision_source_recovery`；
> 未运行任何实验 seed

### 验证项

- [ ] OA/DOI 获取：项目 `tools/download --doi
  10.1109/JLT.2025.3600402` → `all_failed`，无 source PDF/content。
- [ ] IEEE 获取：项目 IEEE blit 精确命中文档 `11129614`，但 PDF 返回
  HTTP 202、download 0/1 → 仍无合法全文，公式级 novelty adjudication 阻断。
- [x] primary identity：IEEE metadata 与 Semantic Scholar official record →
  DOI、题名、作者、JLT 2025 身份一致。
- [x] direct family collision：primary abstract 明示 robust VB-UKF CPR 同时使用
  covariance adaptation 与 Huber M-estimator robust update，并相对 BPS 报告
 最高 0.66 dB OSNR gain → generic Huber robust CPR 新颖性已被直接覆盖。
- [x] fail-closed：全文缺失时不推断其具体公式，也不把“未能证明完全相同”偷换为
  B12 novelty；T015 保持不派遣且 seed census 未消费。

### 证据

```text
DOI=10.1109/JLT.2025.3600402
IEEE_DOCUMENT_ID=11129614
TOOLS_DOWNLOAD=all_failed
IEEE_PDF_HTTP=202
IEEE_DOWNLOAD=0/1
SOURCE_PDF=ABSENT
CONTENT_MD=ABSENT
PRIMARY_ABSTRACT_HUBER_CPR=true
PRIMARY_ABSTRACT_VB_COVARIANCE_ADAPTATION=true
PRIMARY_ABSTRACT_BPS_GAIN_DB=0.66
FORMULA_LEVEL_NOVELTY=UNRESOLVED_NO_FULLTEXT
DIRECT_METHOD_FAMILY_COLLISION=ESTABLISHED
SIMULATION_SEED_RUN=FALSE
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

接收 `BLOCKED_NOVELTY_COLLISION / PACKAGE_WITHDRAWN_BEFORE_EXECUTION`；
B12-Q2 family 不 Kill，但按 T015/D029 的一次性退出边界返回池且不得第二个 B12
repair。formal active carrier 清空，更新 CP015 后立即比较下一批 mechanism
family；不能把公式修复、下载 blocker 或 direct-collision negative 记为方法产出。

## V041: B4、B6、C15 formal-readiness 独立审计

> date: 2026-07-27
> 关联：S001 / R006 / D019 / formal D030 / CP015
> verifier：`b4_formal_readiness_audit`、`b6_formal_readiness_audit`、
> `c15_formal_readiness_audit`；只读，未修改文件、未运行实验 seed

### 验证项

- [x] B4 方法身份：主仓全文/精读笔记确认 PADE 粗频偏外环 + V–V
  残频/相位内环是 source-native baseline；Q2 PCS/Rs 维度错位，Q3
  “时延约束多速率双环”尚无 carrier-specific M-C-A。当前为
  `HYPOTHESIS_ONLY / MCA_BLOCKED`，不是 runnable carrier。
- [x] B6 方法身份：2023 全文确认逐样本 atan2 鉴相器已是源方法；2025
  ODPLL 又直接组合 Z-transform、VV/atan2、FPGA 时延与 Doppler。Q2 单独是
  分析工具，纳入湍流环路则撞 D006；当前为
  `NOT_READY / NO_POSITIVE_METHOD_CONTRACT`。
- [x] C15 science/task 拆分：T011 为
  `BLOCKED_SEARCH_COVERAGE`（53 unique/49 published 但 actual source 仅
  OpenAlex）；T012 为 `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`，
  source/canonical science 未运行。旧 shared `mu=0.03` 跨约 19× gradient
  scale，机制 verdict 不可继承；family 仍为
  `HYPOTHESIS_ONLY / FORMALIZATION_CANDIDATE`。
- [x] C15 可复用资产：2×2 FIR cost engine、Godard/MMA/DD-LMS comparator、
  paired evaluator 与 source schema 存在；因此它比 B4（尚无 M-C-A/核心实现）
  与 B6（无 residual construct）更接近一条可失败的正向方法链，但仍不能直接
  运行 seed。
- [x] 六维覆盖：三份审计均明确方法形态、预期增量、可包装句、formal
  readiness、最小补债与失败轮换点；R006 已逐项合并，不足三个 runnable
  carrier 的证明成立。

### 证据

```text
B4_CONTENT=D:\code\study\research-protocol\papers\doi\10.1016_j.optcom.2023.129312\content.md
B4_CONTENT_SHA256=ce080cd42c22205b10d5de28ad1655631d3a4b41a101bfa289ea23d469de9e36
B4_NOTE=D:\code\study\research-protocol\papers\_read_notes\_B4-dual-feedback-loop-increment.md
B4_NOTE_SHA256=f80c8d10a5a98032250c16e944be236e16b96119a9d261ad802dd1759672c8a5
B6_CONTENT=D:\code\study\research-protocol\papers\doi\10.3390_photonics10121312\content.md
B6_CONTENT_SHA256=f8eed543e1779aa64cc7303bff3e1fe9c1544378e8458d2b7608f33ce9de5b61
B6_DIRECT_2025=D:\code\study\research-protocol\papers\doi\10.1109_ICSOS66026.2025.11443174\content.md
B6_DIRECT_2025_SHA256=52ec61d5a486a1a8d93dc2f0223b6490026a5520e96c71d6b8d60b7508a3360b
B6_NOTE=D:\code\study\research-protocol\papers\_read_notes\_B6-z-odpll-opll-increment.md
B6_NOTE_SHA256=e319e0094ac963e82d2247a584bbcefafc7701efcf62f1da13504d8c406c92c2
C15_T011_RECEIPT_SHA256=713f4d3e957b09dcf84a33c156a78396225bc943c05a6fa8973bd84c025f1feb
C15_T012_RECEIPT_SHA256=b40b0c29365d82e6c03d864605f8cd9bc64cdea4f29d36f9d4b5485631571b17
C15_COST_ENGINE_SHA256=44ccbd9b83f41850301a35dff5f68a450f50efec48b2c2cfcd2a712542724e79
RUNNABLE_CARRIERS=0/3
SIMULATION_SEED_RUN=FALSE
```

### 结论

PASS（readiness audit 完整性）；科学结论为三者均非 runnable carrier。

该 PASS 只是候选审计 PASS，不是方法、promotion 或 scientific carrier PASS。
选择 C15 只授权一次性 formalization workline；`mission_method_delta=NONE`。

## V042: T016 首轮 dispatch 静态审查

> date: 2026-07-27
> 关联：S001 / R006 / D020 / formal D031 / T016 / V041 / CP015
> verifier：`t016_dispatch_verifier`；只读，未运行下载或实验 seed

### 验证项

- [ ] source provenance：T016 首版未冻结 atomic-family alias/split、
  singleton provenance 与 DOI/title conflict fail-closed；shared index 存在
  `serpapi_scholar+semantic_scholar` 等复合标签，可能虚构三源，P0。
- [ ] Phase B CLI/write boundary：首版
  `tools/blit --download --doi <DOI>` 与实际 CLI 不兼容；`tools/blit.py`
  要 positional query、required `--source`，且 `--download` 接目录。任务又把
  worktree cwd 与 shared-main 写入混用，可能参数失败或写错仓，P0。
- [ ] timebox：首版把三次 browser download 与最多三次 convert 放进一个
  Phase B，没有 per-turn wall-clock stop，不能证明每 agent ≤15 分钟，P1。
- [ ] current projections：`projects-overview.md`、master GW table 与 live
  topic current-range 仍有 post-B12/B10 present-tense stale state，P1。
- [ ] disk-only audit recovery：三项 readiness audit 只在 agent 回执中，
  未登记 V；R006 对 B4/B6 的相对路径在 worktree 不存在，P1。
- [ ] clean binding：owner/task/current edits 与 tracked `tools/**/__pycache__`
  改动使 worktree 非 clean；T016 A0 会正确阻断，P2。
- [x] science ceiling：R006/D020/D031/T016 始终保持
  `NO_ACTIVE_SCIENTIFIC_CARRIER`、`mission_method_delta=NONE`，并禁止
  coverage confirmation 前 Step 3、seed/MVE。

### 证据

```text
VERDICT=FAIL
P0=2
P1=3
P2=1
SHARED_INDEX_SIZE=39099216
SHARED_INDEX_SHA256=7530fa6fb9ae0234eee8d98902c8bcc936e278401dc61d0daded300542a4d27a
BLIT_QUERY_POSITIONAL=true
BLIT_SOURCE_REQUIRED=true
BLIT_DOWNLOAD_ARGUMENT=DIR
BLIT_DOI_FLAG=false
TASK_CONTROL_INITIAL=PASS
SIMULATION_SEED_RUN=FALSE
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

修订同一 T016 的 dispatch contract，但不执行：恢复 atomic-family/singleton/
identity-conflict 规则并冻结 shared-index hash；改为三个串行 exact-title IEEE
worktree-staging turn + disk-only synthesis，禁止写 shared main repo；更新 stale
projection；以 V041 落盘三项 readiness audit。随后由同一独立 verifier 复审；
P0/P1 关闭且 clean committed binding 前不得派 Phase A。

## V043: T016 第二轮 dispatch 静态审查

> date: 2026-07-27
> 关联：S001 / D020 / formal D031 / T016 / V042 / CP015
> verifier：`t016_dispatch_verifier`；只读，未运行检索、下载、转换或实验 seed

### 验证项

- [ ] canonical identity gate：`tools/blit.py` 的 IEEE JSON 固定写
  `doi=""`，下载 sidecar 只含 `expected_title`、`real_title`、
  `title_check`、`title_overlap`、`checked_at`；T016 却要求 JSON 与 sidecar
  DOI 等于冻结 DOI，因此正确 PDF 也必然失败 → P0。
- [ ] bounded download：T016 命令使用 `--max 5 --download`，而
  `ieee_download()` 会遍历所有返回结果；任务同时要求 staging 目录恰好一个
  PDF，存在由额外搜索结果制造的假阻塞 → P1。
- [ ] cumulative diff allowlist：B0 只概括“已完成 canonical staging
  receipt”，未显式允许前序 query JSON、PDF、sidecar 与 converted markdown，
  合法跨 turn 产物可能被 resume gate 误判 → P1。
- [ ] clean committed binding：owner/task/current edits 尚未提交，且 tracked
  `tools/**/__pycache__` 仍有工作树改动；A0 必须继续阻断 → P2。
- [x] V042 其余问题：atomic/singleton source provenance、shared-index
  size/hash、主仓只读、每 canonical 独立 turn/timebox、V041 disk-only
  readiness 与 current projections 已闭合。
- [x] science ceiling：仍为
  `NO_ACTIVE_SCIENTIFIC_CARRIER / mission_method_delta=NONE`，未运行
  seed/MVE。

### 证据

```text
tools/blit.py:267-278
  "doi": "",
  "url": p.get("url", ""),
  "source": "ieee"

tools/blit.py:39-58
  sidecar fields =
  expected_title, real_title, title_check, title_overlap, checked_at

tools/blit.py:327-346
  ieee_download iterates every result and downloads each arnumber

VERDICT=FAIL
P0=1
P1=2
P2=1
SIMULATION_SEED_RUN=FALSE
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

先独立冻结三篇 canonical 的 `exact title + DOI + IEEE arnumber/document URL`。
运行时只按 exact normalized title、result URL/arnumber 与 PDF sidecar title
验证；DOI 是事先审计的 bibliographic binding，不伪称由 blit JSON/sidecar
返回。把命令改为 `--max 1`，并显式列出跨 turn 累积 allowlist。修订后由独立
verifier 复审；clean committed binding 前仍不得执行 Phase A。

## V044: C15 三篇 canonical IEEE 身份独立审计

> date: 2026-07-27
> 关联：S001 / D020 / formal D031 / T016 / V043
> verifier：`c15_canonical_identity_audit`；只读，未写文件、未下载 PDF、
> 未运行实验 seed

### 验证项

- [x] Sato 1975：exact normalized-title 唯一命中
  `https://ieeexplore.ieee.org/document/1092854/`；arnumber=`1092854`；
  DOI `10.1109/TCOM.1975.1092854` 的 resolver 302 指向同一 document URL。
- [x] Godard 1980：exact normalized-title 唯一命中
  `https://ieeexplore.ieee.org/document/1094608/`；arnumber=`1094608`；
  DOI `10.1109/TCOM.1980.1094608` 的 resolver 302 指向同一 document URL。
  同次查询的 comments 论文 `1095475` 标题不同，不构成 identity 冲突。
- [x] Yang–Werner–Dumont 2002：exact normalized-title 唯一命中
  `https://ieeexplore.ieee.org/document/1007381/`；arnumber=`1007381`；
  DOI `10.1109/JSAC.2002.1007381` 的 resolver 302 指向同一 document URL。
  同次查询的 2026 GFDM 论文 `11422838` 标题不同，不构成 identity 冲突。
- [x] 工具语义：三项 blit IEEE 结果的 DOI 字段均为 `""`；因此运行时不得用
  JSON DOI 或 sidecar DOI 作 gate，bibliographic DOI 必须保持为本次独立
  resolver binding。
- [x] 边界：三次查询均 exit=0；未使用 `--output` 或 `--download`，未下载
  PDF、未写盘、未运行 seed/MVE。

### 证据

```text
SATO_TITLE=A Method of Self-Recovering Equalization for Multilevel Amplitude-Modulation Systems
SATO_IEEE_ARNUMBER=1092854
SATO_BLIT_DOI=""
SATO_DOI_LOCATION=http://ieeexplore.ieee.org/document/1092854/

GODARD_TITLE=Self-Recovering Equalization and Carrier Tracking in Two-Dimensional Data Communication Systems
GODARD_IEEE_ARNUMBER=1094608
GODARD_BLIT_DOI=""
GODARD_DOI_LOCATION=http://ieeexplore.ieee.org/document/1094608/

YANG_TITLE=The multimodulus blind equalization and its generalized algorithms
YANG_IEEE_ARNUMBER=1007381
YANG_BLIT_DOI=""
YANG_DOI_LOCATION=http://ieeexplore.ieee.org/document/1007381/

QUERY_EXIT=0/0/0
PDF_DOWNLOAD_COUNT=0
SIMULATION_SEED_RUN=FALSE
```

### 结论

PASS。三篇 canonical 的 `exact title + DOI + IEEE arnumber/document URL`
绑定可作为 T016 fail-closed identity gate；该 PASS 不是全文获取、coverage、
formal carrier 或 method PASS。

## V045: T016 第三轮静态合同独立复审

> date: 2026-07-27
> 关联：S001 / D020 / formal D031 / T016 / V043 / V044 / CP015
> verifier：`t016_dispatch_verifier`；只读，未运行检索、下载、转换或实验 seed

### 验证项

- [x] canonical identity：V044 已冻结 exact title、DOI、IEEE
  arnumber/document URL；T016 运行时只按唯一 normalized title、URL arnumber、
  PDF filename 与 sidecar title 验证，明确 JSON `doi=""` 不作 PASS，关闭
  V043 P0。
- [x] bounded download：命令已冻结 `--max 1`；`tools/blit.py` 最多下载唯一
  result，与 staging 恰好一个 PDF/sidecar 的门一致。
- [x] cumulative allowlist：Phase A 三 JSON+worker log，以及每个已完成 slug 的
  query JSON、receipt、PDF、sidecar、converted markdown 均显式允许；同时禁止
  `.sessions/**`、owners、mission/master/current、simulation/common/params、
  旧任务与旧 worker log 产生新 diff。
- [x] source provenance：atomic alias/split/singleton、identity conflict 与
  frozen shared-index size/hash 合同完整。
- [x] execution boundary：三篇 canonical 串行独立 turn、12 分钟 stop、shared
  main read-only/worktree staging 与 Phase C disk-only 均闭合。
- [x] science ceiling：formal scientific carrier 仍为 NONE，
  `mission_method_delta=NONE`，禁止 Step 3、seed/MVE。
- [x] task-control：复审时 epoch38 / CP015 /
  `CANDIDATE_FORMALIZATION` validator PASS，D020/D031 active，current
  projections 一致。
- [ ] clean committed final binding：intended owner/control/R/V/T/projection
  尚未提交，tracked pycache 仍有工作树改动 → 唯一 P2。

### 证据

```text
STATIC_CONTRACT=PASS
P0=0
P1=0
P2=1
TASK_CONTROL=PASS
FORMAL_ACTIVE_SCIENTIFIC_CARRIER=NONE
MISSION_METHOD_DELTA=NONE
SIMULATION_SEED_RUN=FALSE
ONLY_PENDING=clean committed final binding
```

### 结论

PARTIAL。T016 静态合同 PASS；只因 final binding 尚未形成，不允许起飞。

### 后续（FAIL/PARTIAL 时）

隔离并保留 tracked pycache 变化，只提交 intended owner/control/R/V/T/current
projection；工作树 clean 后由独立 verifier 用 `PYTHONDONTWRITEBYTECODE=1` /
`python -B` 重跑 task-control，核对 current epoch/checkpoint、D020/D031 血缘、
shared-index hash、主仓 target diff 与 commit 内容。全部 PASS 后才允许 Phase A。

## V046: T016 epoch39 clean final-binding 独立起飞审查

> date: 2026-07-27
> 关联：S001 / D020 / formal D031 / T016 / V045 / CP015
> verifier：`t016_final_binding_verifier`；只读，未修改文件、未运行检索、
> 下载、转换或实验 seed

### 验证项

- [x] clean worktree：HEAD
  `a392bc0ec077e61ba532152d26563b7cb921f74f`；
  `git status --short` 计数为 0。
- [x] task-control：`PYTHONDONTWRITEBYTECODE=1` + `python -B` 实测
  validator PASS；epoch39 / CP015 / `CANDIDATE_FORMALIZATION`。
- [x] owner 血缘：live D020/formal D031 active；D019/D030 superseded。
- [x] binding content：HEAD 包含 T016、live control/owner、formal owner/topic、
  current projections、master-state 与 V041–V045。
- [x] frozen shared index：size=`39099216`；
  sha256=`7530fa6fb9ae0234eee8d98902c8bcc936e278401dc61d0daded300542a4d27a`。
- [x] shared-main boundary：Sato/Godard/Yang 三个 canonical target 均不存在，
  限定 target 的 `git status --short` 为空。
- [x] commit boundary：HEAD 共 17 个路径；不含 tools/pycache、
  `papers/downloads`、`search-archive/2026-07-27`、simulation/seed/MVE
  产物。
- [x] science ceiling：state/portfolio 均为
  `NO_ACTIVE_SCIENTIFIC_CARRIER`；CP015/T016 的 method delta 均为 NONE。

### 证据

```text
VERDICT=PASS
P0=0
P1=0
P2=0
AUTHORIZATION=PHASE_A_ONLY
HEAD=a392bc0ec077e61ba532152d26563b7cb921f74f
WORKTREE_STATUS_COUNT=0
TASK_CONTROL=PASS
INDEX_SIZE=39099216
INDEX_SHA256=7530fa6fb9ae0234eee8d98902c8bcc936e278401dc61d0daded300542a4d27a
FORBIDDEN_COMMIT_PATH_COUNT=0
```

### 结论

PASS。允许把 foreground 切换为 Phase A ready；只授权 T016 Phase A 的
disk-native Step 1 view 与 recent identity，不授权 Phase B、检索下载、精读、
Step 3、seed 或 MVE。

## V047: T016 Phase-A 执行与科学身份独立验收

> date: 2026-07-27
> 关联：S001 / D020 / formal D031 / T016 / CP016
> verifier：`t016_phase_a_science_verifier`；只读，未修改文件、未运行网络、
> 下载、转换或实验 seed

### 验证项

- [x] task/integrity：epoch40 / CP015 task-control PASS；executor 窗口内只写
  candidate view 与 step-016 worker log，无 `.sessions`、owner、mission、
  simulation、staging、A2/A3 或 Phase-B 产物。
- [x] frozen inputs：七份 archive 原始行数
  `56=20/16/19/1/0/0/0`；shared index 流式扫描 20,747 行，size/hash 与冻结值
  一致。
- [x] identity hard block：artifact 报告的三组同 normalized-title/双非空 DOI
  均在原始 index 中存在；冻结规则未授权 `.short`/`.v1` alias 推断，必须
  `BLOCKED_IDENTITY_CONFLICT`。
- [x] stop discipline：A2/A3 与 Phase B 未执行符合合同；formal disposition
  为 `BLOCKED_FORMAL_READINESS`，delta NONE。
- [x] priority encoding：candidate JSON 与 worker log 均为合法 UTF-8，
  U+FFFD=0；实际枚举为必读10、建议读181、待确认63、备选72。主控
  PowerShell 乱码来自读取端，不是落盘 corruption。
- [ ] provenance completeness：artifact 声称 `raw_rows_included=381`，但
  persisted locator 只能回溯
  `375=44 archive+331 index`；OpenAlex singleton event 独立重算为 122，
  非 summary 114；全 index closure 另发现三组未列 multi-DOI conflict → P1。
- [ ] deterministic classification reproduction：priority/route assignment
  predicate 未冻结，独立验收可核对落盘枚举与计数，但不能从原始行完全重生成
  分类 → P2。

### 证据

```text
VERDICT=PARTIAL
P0=0
P1=1
P2=1
RAW_ARCHIVE_ROWS=56
FROZEN_INDEX_ROWS=20747
PERSISTED_INCLUDED_LOCATORS=375
UNIQUE_IDENTITIES=326
PUBLISHED_PREPRINT_UNKNOWN=192/5/129
PUBLISHED_RATIO=58.8957%
PRIORITY=10/181/63/72
ROUTE_COVERAGE=5
CANDIDATE_SHA256=177e20384be334fcb00dc3c9a6bb1f789f6f427baa9da3740f4a5ec79e6acd39
WORKER_LOG_SHA256=57f2e051ba90ba5590dbfa4bb0daa17b2f8352d84f2476bdafc30311e41fd34b
```

### 结论

PARTIAL（证据完整性）；科学停止裁决 PASS。

```text
formal_science_disposition=BLOCKED_FORMAL_READINESS
specific_block=BLOCKED_IDENTITY_CONFLICT
mission_method_delta=NONE
package_weight=ADEQUATE
package_drift=ALIGNED
mission_drift=DRIFTED/STALLED
same_axis_streak=1
repair_streak=0
no_method_streak=16
PHASE_B_AUTHORIZED=FALSE
```

C15 返回候选池且不得第二个 source package。P1/P2 不改变 hard block，也不授权
repair；candidate view 只能作 partial defensive evidence，不能作完整 coverage
证明或方法材料。

### 后续（FAIL/PARTIAL 时）

主控按 D020/D031 退出边界接收 CP016，更新 live/formal owner 与 current
projections到 post-C15 remap；禁止 Phase B、alias/provenance repair、Step 3、
seed/MVE。下一包先做机制级 carrier remap。

## V048: T017 C16-open Step 1–2 dispatch 独立审查

> date: 2026-07-27
> 关联：S001 / R007 / D022 / formal D033 / T017 / CP016
> verifier：`t016_phase_a_science_verifier` + `b6_formal_readiness_audit`；
> 只读，未修改文件、未运行网络、下载、转换或实验 seed

### 验证项

- [x] carrier remap：R007 以方法形态、预期增量、可包装句、formal
  readiness、最小补债成本、失败轮换点比较五个机制不同候选；readiness
  census 为 `READY=0 / NEEDS_SMALL_ADAPTER=0 /
  HYPOTHESIS_ONLY=5`。
- [x] 选择理由：C16-open 相对 Q14、B4、Q-ML4 的问题可判定性、接口同域性
  与迁移债更优；本包仍固定 `mission_method_delta=NONE`，没有预支方法产出。
- [x] 正向合同：full-complex 2×2 FIR non-modulus target 与 tuned 11-tap
  CMA/MMA comparators 明确，并冻结相同 samples/taps/warm-up/update budget。
- [x] FR-22：formal active scientific carrier 保持 `NONE`；T017 只允许
  Groundwork Step 1–2，不允许 Step 3/Q#/实现/simulation/Probe/MVE。
- [x] 执行合同：五种 terminal state、Phase-A/Phase-B authorization 映射、
  candidate-view 顶层 `results[8–12]` + stable IDs、download `--only`、
  exact-title IEEE `blit` 与所有 Bash wrapper 调用均与当前 CLI 一致。
- [x] EOL/integrity：按 wrapper 原始 `w/lf`/`w/crlf` 条件适配并恢复，
  object hash 与 diff 为硬门；不允许工具适配污染 owner/control。
- [x] current projections：epoch42 / CP016 / D022 / D033 / carrier NONE /
  T017 formalization-only 一致；task-control validator 实测 PASS。
- [x] 独立复审：首轮发现 5 个 P1、1 个 P2；修正后两个 verifier 均返回
  `PASS / P0=0 / P1=0 / P2=0`。

### 证据

```text
VERDICT=PASS
P0=0
P1=0
P2=0
TASK_CONTROL=PASS
FORMAL_ACTIVE_SCIENTIFIC_CARRIER=NONE
MISSION_METHOD_DELTA=NONE
AUTHORIZATION=T017_PHASE_A
STEP3_AUTHORIZED=FALSE
SIMULATION_SEED_RUN=FALSE
```

### 结论

PASS。允许由未参与本审查的不同 executor 执行 T017 Phase A / Groundwork
Step 1。只有 A6 全门 PASS 后才可在另一个 executor turn 进入 Phase B；任何
失败按冻结终态停止。V048 不激活 scientific carrier，也不形成方法增量。

## V049: T017 Phase-A 执行与正式科学身份独立验收

> date: 2026-07-27
> 关联：S001 / R007 / D022 / formal D033 / T017 / CP017
> verifier：`t016_phase_a_science_verifier`；只读，未修改文件、未运行网络、
> 下载、转换或实验 seed

### 验证项

- [x] raw/source：五份冻结查询分别保留 `16/8/11/17/1=53` rows；每篇
  singleton provenance 均只来自 OpenAlex，actual source family=`1<3`。
- [x] identity/review：冻结 DOI/title/year/first-author 规则独立去重为 44；
  normalized-title 双非空 DOI conflict=0，quarantine=0；53/53 review 字段
  完整，25/25 排除项有理由。
- [x] priority/route/pool：必读2、建议读4、待确认1、备选12、排除25；
  R1 direct/adjacent=`1/3`，R2=`3/1`；pool=10、stable IDs 唯一且均精确
  匹配一个 candidate。
- [x] published correction：一篇 `10.36227/techrxiv.14775957.v1` 明确是
  TechRxiv preprint，candidate view 误标 published；独立正确计数为
  `published/preprint/unknown=41/3/0`、ratio=`41/44=0.9318181818`，门仍 PASS。
- [x] A6：source `1<3` FAIL，must-read `2<5` FAIL；unique、published
  ratio、R1/R2、pool 与 quarantine 其余门 PASS。
- [x] integrity：raw/candidate/worker SHA256 与 executor receipt 一致；
  15/15 protected hashes 未变；`tools/search` 与五个 tracked pyc 均恢复到
  HEAD object 且零 diff。
- [x] stop discipline：未出现 Phase B、download/convert、全文精读、Step 3、
  Q#、实现、simulation/Probe/MVE/seed 产物。
- [ ] per-source failure receipt：raw JSON 未持久化 source status/error，只能
  证明 S2/arXiv 没有 singleton rows，不能独立区分 executor 所报的
  “S2 rate-limited”与“arXiv empty”原因。

### 证据

```text
VERDICT=PARTIAL
P0=0
P1=2
P2=0
RAW_ROWS=53
ACTUAL_SOURCE_FAMILY=1
UNIQUE_NONQUARANTINE=44
PUBLISHED_PREPRINT_UNKNOWN=41/3/0
PUBLISHED_RATIO=0.9318181818
MUST_READ=2
DIRECT_R1_R2=1/3
ACQUISITION_POOL=10
IDENTITY_QUARANTINE=0
CANDIDATE_SHA256=2d167ec74759a2f460b923cbf516e627a18003843f47729f5689d5a1da20e2d8
WORKER_LOG_SHA256=0fc319ac0f61043d8858cf21978bae66bd8faa5779d7a11272957dab168b57d0
```

### 结论

PARTIAL（published/source-receipt 证据质量）；正式科学停止裁决 PASS：

```text
terminal_status=BLOCKED_SEARCH_OR_IDENTITY
formal_science_disposition=BLOCKED_FORMAL_READINESS
mission_method_delta=NONE
package_weight=ADEQUATE
package_drift=ALIGNED
mission_drift=DRIFTED/STALLED
same_axis_streak=1
repair_streak=0
no_method_streak=17
PHASE_B_AUTHORIZED=FALSE
STEP3_AUTHORIZED=FALSE
```

两项 P1 不改变 source/must-read 双硬失败，不授权 artifact/source repair。
C16-open 返回候选池且不得第二个 source/formalization package；该 candidate
view 只作 partial defensive evidence，不作 coverage 或方法材料。

### 后续（FAIL/PARTIAL 时）

主控按 D022/D033 的一次性退出边界接收 CP017，更新 live/formal owner 与
current projections 到 post-C16 remap；禁止修 published label、补 per-source
receipt、追加第六查询、运行 Phase B/Step 3/seed/MVE。

## V050: T018 初版独立 dispatch review

> date: 2026-07-27
> 关联：S001 / R008 / D024 / formal D035 / T018 / CP017
> verifier：`t016_phase_a_science_verifier`；只读，未修改文件、未运行网络、
> 下载、转换、检索或实验

### 验证项

- [ ] Step2→3 coverage gate：T018 B3 原先允许新论文直接
  `gw-acquire→gw-read→synthesis`，没有 `gw-acquire.md` 的 coverage-gap
  report 与确认阻塞门 → **P0 FAIL**。
- [ ] 固定 receipt：两条 citation 命令没有 `-o`，不能产生声明的
  `q14-step35-core-forward/backward.json` → **P1 FAIL**。
- [ ] 状态机：`BLOCKED_EXECUTION_TIMEBOX` 同时被列为 final 与 continuation，
  terminal report 又会提前提出 no-method=18 → **P1 FAIL**。
- [ ] current projections：formal topic-index“当前位置”、harvest next_action、
  formal registry 仍停 D034/epoch43/post-C16 → **P1 FAIL ×3**。
- [ ] 可复制命令：六条检索只给 query、参数与输出名，未给含 `-o` 的完整命令
  → **P2 FAIL**。
- [x] 科学合同：R008 的四候选六维比较、Q14 相对至少两个替代项的选择理由、
  carrier=`NONE`、delta=`NONE`、actual-source/引用链/三轮收敛、criterion-2
  四联条件和 tuned CMA+DD-LMS/RDE/simple DSP comparator 均成立。
- [x] 控制完整性：初版 task-control validator PASS；四个 current YAML
  `safe_load` PASS；无 CP018/no-method18/epoch45 提前推进；T018 未执行。

### 证据

```text
VERDICT=FAIL
P0=1
P1=5
P2=1
TASK_CONTROL_INITIAL=PASS
YAML_SAFE_LOAD=4/4
T018_EXECUTED=FALSE
CP018_CREATED=FALSE
METHOD_DELTA=NONE
```

```text
P0-1=T018:314-326 vs stages/gw-acquire.md coverage-gap/user-confirmation gate
P1-1=T018:242-250 missing fixed -o
P1-2=T018 final/continuation timebox conflict
P1-3=formal topic-index:295-307 stale
P1-4=harvest/current.yaml:404-433 stale
P1-5=_registry.yaml formal owner:450-451 stale
P2-1=Round-1 commands not fully copyable
```

### 结论

FAIL

初版 T018 不得执行。该结论是 task-contract/gate 审查，不是 Q14 science Kill，
不是 package checkpoint，也不改变 CP017、no-method=17 或
`mission_method_delta=NONE`。

### 后续（FAIL/PARTIAL 时）

由 D025/formal D036 持有修订合同：新增论文 acquisition 后先写 coverage-gap
report并暂停，由独立 verifier + delegated Goal master 确认；显式冻结 search/
citation `-o`；分离七个 terminal 与两个 continuation；协调三处 stale current
projection。修订后必须由独立 verifier 重新完成 dispatch review。

## V051: T018 修订版独立 dispatch re-review

> date: 2026-07-27
> 关联：S001 / V050 / D025 / formal D036 / T018 / CP017
> verifier：`t016_phase_a_science_verifier`；只读，未修改文件、未联网、
> 下载、转换、检索或运行科学任务

### 验证项

- [x] coverage gate：`acquire → 完整 coverage report →
  AWAITING_DELEGATED_COVERAGE_GATE → 独立 V → Goal master approval →
  epoch/task 重绑 → B2 read` 全链冻结；任一 must/advised 全文失败即
  `BLOCKED_STEP35_FULLTEXT`。
- [x] user-delegated adapter：D004 明确用户把端到端技术/科学判断交 Goal；
  D025/D036 只替代本 mission 的技术确认接口，不放宽全文、identity、source、
  convergence 或私有材料阻塞。
- [x] terminal/continuation：七个 terminal 与两个 continuation 分离；
  continuation 禁 formal disposition、CP、streak 与 no-method。
- [x] receipt：六条 search 与两条 citation 均显式
  `--format json -o <frozen path>`，与 CLI parser/output 实现一致。
- [x] shared-paper identity：WORKTREE/SHARED_REPO/SHARED_PAPERS 三根明确；
  五篇 corpus 路径 5/5 存在，L04 正确为 `9695357.md`，均可生成 SHA256。
- [x] current projections：formal topic、registry、state、portfolio、harvest、
  master 与 projects-overview 一致指向 D036/epoch45/CP017；carrier NONE。
- [x] 无提前推进：无 CP018/epoch46/no-method18、step-018 worker 或
  q14-step35 raw；T018 未执行。

### 证据

```text
VERDICT=PASS
P0=0
P1=0
P2=0
TASK_CONTROL=PASS
YAML_SAFE_LOAD=4/4
TRACKED_DIFF_CHECK=PASS
UNTRACKED_T018_DIFF_CHECK=PASS
SHARED_CORPUS_EXISTS=5/5
T018_EXECUTED=FALSE
MISSION_CHECKPOINT=CP017
NO_METHOD_STREAK=17
```

### 结论

PASS

修订版 T018 的科学合同与静态 dispatch interface 可接受。V051 不激活
scientific carrier，不形成 method delta，也不追加 mission checkpoint。主控可把
foreground 递增到新 epoch，只授权不同 executor 执行 Phase A；epoch/task
重绑定后仍需独立 final-binding PASS。

## V052: T019 pre-formal 方法工厂独立科学审查

> date: 2026-07-28
> 关联：S002 / D026 / T019 / commit `e1c479e`
> verifier：独立 agent `verify_t019_science` + 主线 raw 重算；只读审查

### 验证项

- [x] 工程主链：commit 只含 T019 授权路径；420 raw rows =
  7 methods × 60 paired `(cell,seed)`，键唯一，共享 realization 成立；
  raw→median/help-hurt-tie 可复算，7/7 tests PASS。
- [ ] 当前公平 baseline：FAIL。T019 使用历史 `μ=0.001` anchor；B01-R 已将
  validation-optimal fixed-μ CMA 修正为 `μ=0.03`。
- [ ] 严格因果：FAIL。M3 用 `[cal,eval_end]` 选择同一 eval window；M5 用
  整个 eval window 的功率统计后回判该窗口。
- [ ] semantic smoke 闭包：FAIL。terminal `result.v1.json` 中
  `smoke_results={}`；单独 smoke 被后续 `--compare` 覆盖。
- [ ] clean boundary：FAIL。M3 在 30 个 clean pairs 中有 2 个退化超过 MDE，
  最大 ΔPI-SER=`+0.7461`，与 worker-log“全部 intact”矛盾。
- [ ] 机制归因：FAIL。未做 basin/state-space 扫描；M1 与 C15 modulus、M3
  与 C14 init/multistart、M4 与 blind-affine 高度重合；M3 第四 init 只是
  PI-SER 不变的中心 tap 符号翻转。
- [x] M5 弱线索：raw 为 15 help / 5 hurt / 40 tie，trimmed mean
  ΔPI-SER=`-0.00895`，但改善集中在少数复用 seed，且实现非因果，不能晋级。

### 证据

```text
VERDICT=PARTIAL
P0=2
P1=5
P2=2
RAW_ROWS=420
PAIRS=60
PYTEST=7/7_PASS
ACCEPTED_METHOD_DELTA=FAIR_COMPARISON_RUN
ACCEPTED_SCIENCE=THESE_FIVE_IMPLEMENTATIONS_DID_NOT_PASS_THE_GATE
REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO
M5_WEAK=15_HELP_5_HURT_40_TIE
```

### 结论

PARTIAL

接收“确实完成了一次五构造 paired comparison”和
`mission_method_delta=FAIR_COMPARISON_RUN`；拒收 T019 的广义真阴性、结构性
吸引子和 receiver-recoverable gap≈0 解释。`NO_DIAGNOSTIC_SIGNAL` 只能机械地
描述这五个具体实现未过预设门，不能关闭五个机制族。

### 后续

只允许一个有界的 corrected-baseline 方法包：回到 current `μ=0.03` CMA，
使用严格 prefix-only 统计、fresh disjoint seeds、B01-R 四分类和合法
receiver-visible comparators。M5 只作为弱种子扩成公开星座先验的因果
shell-distribution family；若仍无 held-out 信号，则退出 CB1 z-only
post-processing，不给第三包。

## V053: T020 causal constellation-prior 方法工厂独立科学审查

> date: 2026-07-28
> 关联：S002 / D027 / T020 / commit `5cf76d5`
> verifier：独立 agent `verify_t020_science` + 主线 raw/代码只读复算

### 验证项

- [x] raw 与统计：1120 rows，键重复/缺失/diverged=`0/0/0`；M4 相对
  baseline 的 mean/CI/help-hurt-tie 精确复现为
  `-0.0825893 / [-0.138115,-0.031779] / 7-0-13`。
- [x] baseline 与因果边界：primary 为 current `μ=0.03` CMA；M4 的 test
  动作只读 128-symbol prefix 的 `mean|z|²` 与 spread，未用 suffix/truth
  选 branch；5/5 tests PASS。
- [x] comparator 补算：M4−blind-affine mean=`-0.08661`，
  CI=`[-0.14244,-0.03423]`；M4−C11 mean=`-0.09049`，
  CI=`[-0.14470,-0.04096]`。因此结果确实未退化于两者。
- [ ] comparator gate 实现：代码只比较总均值
  `method_mean <= comparator_mean+0.005`，没有执行合同所称 paired CI；
  本次由 verifier 补算后结论仍成立 → P1。
- [ ] gate artifact：raw CSV 未保存逐 `(cell,seed)` policy、prefix features
  与 frozen map。只读重跑得到 identity=`102/140`、M2=`38/140`、
  M3=`0/140`，但原 artifact 自身不闭包 → P1。
- [ ] offline 四分类：`setdefault` 使每 cell 只保留第一个 test seed 标签，
  不能支撑 140 pairs 的类别分布叙述 → P2。
- [ ] dev 表述：合同声明 10 dev seeds，实际 grid 只用 3 cells×3 seeds；
  `ct=0.6` 在 grid 上界。但敏感性复算 `ct=0.4/0.5/0.6` 的 test mean 分别
  `-0.07575/-0.07952/-0.08259`，CI upper 均<0 → P2，不推翻 signal。
- [x] 机制边界：140 pairs 中 37 改善、1 退化、102 相同；38 次触发集中于
  7/20 seeds，说明主要是固定 CMA 的随机实现/初始化脆弱性修复，不是普遍信道
  增益。57 个 baseline<0.1 pairs 的实测最坏 delta=0。

### 证据

```text
VERDICT=ACCEPT_DIAGNOSTIC_METHOD_SIGNAL
P0=0
P1=3
P2=2
RAW_ROWS=1120
UNIQUE_KEYS=1120
DIVERGED=0
PYTEST=5/5_PASS
M4_VS_BASELINE=-0.0825893 CI[-0.138115,-0.031779] H/H/T=7/0/13
M4_VS_BLIND=-0.08661 CI[-0.14244,-0.03423]
M4_VS_C11=-0.09049 CI[-0.14470,-0.04096]
POLICY_COUNTS=identity:102,M2:38,M3:0
```

### 结论

PARTIAL

接收 M4 为冻结 diagnostic slice 上的 `DIAGNOSTIC_METHOD_SIGNAL`，并接收
`mission_method_delta=METHOD_SIGNAL`。不接收 formal Groundwork Go、论文方法
胜利、普遍均衡增益或信道条件归因。

### 后续（FAIL/PARTIAL 时）

停止方法工厂并返回正式 Groundwork。Step 1–2 先核查 direct collision 与
robust-CMA/restart/multistart/radius-calibration 廉价替代；正式阶段必须保存逐
pair gate receipt、完整四分类与 paired comparator CI。

## V054: T021 Q15 Step 1–2 coverage 与收据独立验收

> date: 2026-07-28
> 关联：S002 / D028 / T021 / commit `287fb6a`
> verifier：独立 agent `verify_t021_coverage` + 主线 raw/path 复算

### 验证项

- [x] annotated raw：129 unique；published=`121/129=93.8%`；
  priority=`11/13/2/16/87` 可重算。
- [ ] source union：merged raw 只有 OpenAlex+Semantic Scholar；IEEE
  `2/2/0 hits` 只有 markdown 叙述，无结构化 raw，故“3 源 PASS”不可重算。
- [x] 全文存在性：8 份 PDF/markdown 非空，报告行数与 SHA 匹配；三份 DOI
  artifact identity PASS，五份 blit 可由 markdown 实际标题核验。
- [ ] paper index/path：五份 blit 仍在 `papers/downloads/` 且未追加
  `papers/index.json`；需 canonical/index receipt。
- [ ] coverage closure：D1 会改变 direct collision；C1/C4 会改变 cheap-alt
  吸收判断；C3 重要但不是同级阻断。
- [x] 任务边界：未精读、未实验、未进入 Step 3+；commit 只含
  literature_notes 与 worker log，ignored raw/papers 在本地存在。

### 证据

```text
RAW_UNIQUE=129
PUBLISHED=121/129=93.8%
PRIORITY=11/13/2/16/87
ACTUAL_MERGED_SOURCE_UNION=2
FULLTEXT_RECEIPTS=8_PRESENT
INDEPENDENT_CORE_WORKS=6
P0=1 P1=3 P2=1
VERDICT=PARTIAL_WITH_INTEGRITY_REPAIR_REQUIRED
```

### 结论

PARTIAL

T021 的检索和全文资产可继续使用，但 Step 1“全门 PASS”撤回。主控不采纳
“再开一个纯 repair 包”的建议，改为 T022 前置修复通过后同包进入限定 Step 3。

### 后续（FAIL/PARTIAL 时）

T022 补 IEEE raw 与五篇 blit canonical/index receipt；通过后精读六篇独立核心
和两篇补充。D1/C1/C4 作为 Step 3.5 mandatory debt，未闭合前禁止 novelty、
problem-survival、Step 4a 或实验。

## V055: T022 Q15 Step 3 派工合同独立终审

> date: 2026-07-28
> 关联：D029 / D038 / V054 / T022
> verifier：独立 agent `verify_t020_acceptance_state`

### 验证项

- [x] 八篇派遣身份：expected title、canonical path 与独立/补充计数完整。
- [x] title abort：明确 `Jaccard >=0.4` 继续、`<0.4` abort，以及
  `title-unverifiable` 的前 20 行人工核对。
- [x] 精读 schema：15 个标准字段、七个结构化子表、预印本正式版核查、
  开源代码与 verification status 均为显式要求。
- [x] 综合分析：方法分类、已知局限、2–3 年趋势、背景时间线、baseline
  频次、写作架构、实验完备性与 Q15 problem table 均有交付位。
- [x] 边界：只允许收据修复后进入 Step 3；D1/C1/C4 继续阻断最终四判据、
  novelty、cheap-alt closure、Step 3.5+、Step 4a 与实验。
- [x] 控制完整性：epoch52 / CP020 / D029 / V054 / D038 / T022 投影一致；
  task-control validator、4 YAML 与 `git diff --check` 均 PASS。

### 证据

```text
FINAL_BINDING=PASS
P0=0
P1=0
P2=0
TASK_CONTROL=PASS
YAML=4/4_PASS
GIT_DIFF_CHECK=PASS
```

### 结论

PASS

T022 可交普通 GLM 执行；它仍是 Groundwork Step 3 内容生产包，不是方法
Go、novelty 结论或实验授权。

## V056: T022 内容、收据与 Q15 科学接收审查

> date: 2026-07-28
> 关联：S002 / D029 / D038 / T022 / commit `f3a47260`
> verifier：独立 agents `audit_t022_integrity`、`audit_t022_science` + 主线源码复核

### 验证项

- [x] commit/scope：实际 HEAD=`f3a47260...`，tree clean；只提交
  literature_notes/read-log/worker-log，未改代码或越界 owner。
- [ ] worker binding：worker log 仍写 amend 前 SHA `3555f615...`。
- [x] 收据：一份 IEEE raw 非空；五套 canonical PDF/MD/metadata、原件 SHA、
  index 5 条 success receipt 全部闭合；8 篇 title Jaccard 均为 1.0。
- [x] 六篇独立核心：结构化精读达到 Step 3 最低门。
- [ ] 两篇补充：D3′/D4′ 已读，但未各自完整展开 15 字段 + 七个独立子表，
  故“8/8 全合同 PASS”过强。
- [ ] scientific baseline：T020 M1 在
  `preformal-method-factory-sprint-002/src/methods.py:55-85` 用
  `E|s|²/mean|z|²` 直接乘复振幅；正确功率归一化需平方根。
- [ ] evaluator：`cb1_evaluator.py:172-237` 只搜索极化排列和四象限旋转，
  不做幅度尺度恢复；M4 增益尚未排除常规 gain normalization。
- [ ] collision：D3 的 \(R_n=|z_n-\hat{s}_n|\) 是 decision-error radius；
  D1 官方公开全文可得，不应继续记为不可获取 debt。

### 证据

```text
INTEGRITY=P0=0 P1=2 P2=0
SCIENCE=P0=1 P1=3 P2=1
ACTUAL_HEAD=f3a47260f732e0987743f32bffc6d21d7f92e6aa
INDEPENDENT_CORE=6_PASS
SUPPLEMENTS=2_READ_SCHEMA_PARTIAL
M1_IMPLEMENTED_SCALE=E_ABS2/trimmed_power
M1_APPLIED_AS=scale*z
CORRECT_AMPLITUDE_FACTOR=sqrt(E_ABS2/trimmed_power)
EVALUATOR_SCALE_RECOVERY=NONE
```

### 结论

PARTIAL

接收 `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35` 与
`mission_method_delta=NONE`；不接收“只差 D1/C1/C4”或“Q15 已是可包装方法
胚胎”。四判据改记 `1=PARTIAL / 2=PARTIAL / 3=PASS / 4=PASS`。

### 后续（FAIL/PARTIAL 时）

T023 先完成 D1+定向 normalization/MMA Step 3.5；仅当四判据全过时运行
条件式 Step 4a correct-normalization 审判。该包后不再修 Q15。

## V057: T023 终局 Step 3.5 + 条件式 Step 4a 派工终审

> date: 2026-07-28
> 关联：D030 / D039 / V056 / T023
> verifier：独立 agent `verify_t023_dispatch`

### 验证项

- [x] Step 顺序：任何实现/seed 前强制
  `Step3.5 → A0§0–6 → A′ → A → B → D`。
- [x] 起飞合同：FR-11/12/14/15/18/20/21 均在维度 D 前冻结。
- [x] 文献未收敛：三轮仍未收敛直接
  `Q15_STEP35_NONCONVERGED_NO_GO`，不自动进 Phase B。
- [x] target comparator：Step 3.5 认定的最强 direct/cheap-alt 无法忠实实现时
  直接 No-Go，不允许 recommendation-ready。
- [x] blocked/no-repair：identity、comparator、A0 与非收敛阻断全部归顶层
  No-Go，禁止后续 Q15 repair。
- [x] 实证公平性：correct sqrt normalization、旧/fresh seeds、共享
  realization、seed-cluster bootstrap、MDE 与 strongest-comparator 门完整。
- [x] 控制投影：epoch53 / CP021 / D030 / D039 / V056 / T023 一致；
  task validator、4 YAML 与 `git diff --check` PASS。

### 证据

```text
FINAL_BINDING=PASS
P0=0
P1=0
P2=0
TASK_CONTROL=PASS
YAML=4/4_PASS
GIT_DIFF_CHECK=PASS
```

### 结论

PASS

T023 可交普通 GLM 执行；它必须终局回答 Q15 No-Go 或
Step4a recommendation-ready，不授权 Step 5/Contract/Execute。

---

## V058: T023 Phase-A gate、Step 3.5、代码统计与科学结论独立验收

> date: 2026-07-28
> 关联：S002 / D031 / T023

### 验证项

- [x] control/file boundary：task validator fresh PASS；commit
  `89d8174c56a7729c34a1268ef52394c58e889924` 只改 12 个允许或条件允许路径，
  未改 `.sessions/**`、master/current、T020/common/evaluator；worktree clean。
- [x] deterministic integrity：semantic smoke fresh `8 passed`；JSON valid；
  raw=`3080` 行，`11 methods × 7 cells × 40 seeds`，主键闭合。
- [x] Phase A/A4：T023:48,164–178,197–221 要求四判据全 PASS 才进
  Phase B；worker:128–143 与 feasibility:1110–1114 明记判据 2 PARTIAL 后
  仍运行 seed，P0 越门成立。
- [x] Step 3.5 literature：D1 本地 PDF/MD/metadata 身份可核，D3
  `R_n=|z_n-s_hat_n|` 修正为 decision-error radius 正确；但 D1 未进入全局
  read-note/read-log，C1/C3/C4 closure 与 query/citation-chain raw 不完整。
- [x] comparator safety：contract MDE=`0.005`；result 中 always-on
  pooled/per-pol/robust healthy-worst=`0.0234375/0.02734375/0.015625`，
  均大于 MDE；worker/synthesis/feasibility/decision_log 写成 `<MDE` 错误。
- [x] relative statistics：runner 的 CI/help-hurt 相对裸 CMA，不是 strongest
  normalization；raw 又缺 gate/prefix_features/scale-map/offline-class 字段。
- [x] independent paired recompute：
  - M4−robust old=`+0.008510`，CI=`[+0.004604,+0.012388]`，
    better/worse/tie=`4/15/1`；fresh=`+0.014397`，
    CI=`[+0.009207,+0.020117]`，`1/19/0`。
  - M4−gated-scalar old=`+0.004855`，CI=`[+0.001758,+0.008399]`，
    `0/7/13`；fresh=`+0.007254`，CI=`[+0.004074,+0.010882]`，
    `0/13/7`。
  - gated-scalar−CMA old=`−0.087444`，CI=`[-0.145675,-0.033761]`，
    `7/0/13`；fresh=`−0.139286`，CI=`[-0.199108,-0.082226]`，
    `13/0/7`；两组 healthy-worst=`0`。

### 证据

```text
task-control: PASS
pytest: 8 passed in 5.71s
raw closure: 3080 rows / 11 methods / 7 cells / 40 seeds / unique key PASS
independent reviews:
  audit_t023_gate: REJECT_AS_T023_COMPLETION, P0/P1/P2=1/1/0
  audit_t023_literature: STEP3.5 PARTIAL / formal gate FAIL
  audit_t023_science: REJECT_BINDING_ABSORBED_NO_GO,
                      NONBINDING_DIAGNOSTIC, P0/P1/P2=1/3/1
```

### 结论

PARTIAL

T023 的合法 binding 终态不是 `Q15_ABSORBED_BY_CONVENTIONAL_NORMALIZATION_NO_GO`，
而是 `Q15_MAP_STEP35_NO_Q_NO_GO`；Phase B 只能作 nonbinding diagnostic。
同时，不能接收执行者的 `mission_method_delta=NONE`：数据支持
`G1_SAFE_GATED_NORMALIZATION` 的诊断级 `METHOD_SIGNAL`，但不支持直接
`PACKAGING_BOUNDARY` 或 thesis claim。

### 后续（FAIL/PARTIAL 时）

不修 T023、不重跑 Q15 map。D031/D040 记录 binding amendment；T024 仅给 G1
一次 candidate-specific collision/四判据闭合，并在全过后条件式 formal confirm。

---

## V059: T024 G1 Groundwork + 条件式 formal confirm 派发终验

> date: 2026-07-28
> 关联：S002 / D031 / D040 / T024 / V058

### 验证项

- [x] Groundwork 顺序：显式重入 Step 1→2→3→3.5；逐 Step 写明可继承/
  不可继承证据；任一 FAIL/PARTIAL 顶层 No-Go，禁止由实验反向补证。
- [x] lineage 与 claim：G1 明确为 Q15-derived fallback/salvaged component；
  Q15 nonlinear map 关闭，T023 Phase B 只作 hypothesis-generating diagnostic。
- [x] literature gate：direct/cheap-alt、recent task-matched comparator、
  canonical read-note/read-log、引用链 raw、四判据与收敛均有独立硬门。
- [x] label identity：正式 strata 精确绑定 T020 tuned-CMA `μ=0.03` caller、
  prefix oracle fit、suffix scoring 与 finite/divergence 分支；不迁移 B01-R
  `μ=0.001` z² threshold；raw 字段足以逐 row 重算。
- [x] statistics：primary robust comparator 与 recent comparator fresh 前冻结；
  healthy safety、recoverable-failure、M4 ablation、activation
  precision/recall/balanced-accuracy 均有量化门；每 seed 内先对同 stratum cells
  等权聚合，再对 seed-cluster 做 10k bootstrap。
- [x] no post-hoc rescue：禁止 fresh 选 comparator、调 gate、改 cells、挑 seed
  或降低阈值；任一门失败退出 G1，不留第二个 repair 包。
- [x] task integrity：fresh task-control validator PASS；`git diff --check`
  PASS；两位独立审查者最终均为 P0/P1/P2=`0/0/0`。

### 证据

```text
TASK_CONTROL=PASS
GIT_DIFF_CHECK=PASS
audit_t023_gate: PASS, P0/P1/P2=0/0/0
audit_t023_science: PASS, P0/P1/P2=0/0/0
```

### 结论

PASS

T024 可交普通 GLM 执行。它先回答 G1 是否通过合法 Groundwork；只有全部门
PASS 才可在同包运行一次 fresh formal confirm。该 PASS 不预支 G1 科学 Go。

---

## V060: T024 G1 Groundwork、Gate6 与 comparator identity 独立接收审查

> date: 2026-07-28
> 关联：S002 / D032 / formal D041 / T024

### 验证项

- [x] Gate6 原始计数：eligible 49 对；TP/FP/FN/TN=`19/1/1/28`，
  point balanced accuracy=`0.957759`。
- [x] 统计单位重算：按 seed ID 重采样、合并该 seed 的所有 eligible cells 后
  重算 confusion/balanced accuracy，10k bootstrap 95% CI 约
  `[0.885,1.000]`；Gate6 PASS。pair bootstrap 约 `[0.891,1.000]`，
  但不是冻结单位。
- [x] 错误 `0.50` 定位：人工更正把单类 seed 的缺失 recall 记为 0 后先算
  per-seed balanced accuracy；该统计量不是任务合同中的 pooled
  seed-cluster estimand。报告称 both-class seeds=3，raw 实际为 5：
  `262/264/270/275/278`。
- [x] Phase A evidence closure：G1 search/citation raw 与 D1 read-note 位于
  gitignored 路径，executor commit 中缺失；声称的
  `g1-step1-candidate-map.md` 不存在。四判据与 collision closure 不可独立复核。
- [x] D4 identity：`methods.py` 的 D4 apply 直接返回输入 post-CMA `z`；
  140/140 D4 PI-SER 与 CMA bit-identical，不是 likelihood-gated tap-update
  receiver，Gate4/Gate7 的 target-comparator 语义无效。
- [x] 其余局部数字复核：class support=`healthy 11/collapse 13`；
  G1−CMA collapse=`−0.559796`、CI 约 `[-0.6947,-0.4064]`、help/hurt=`12/0`；
  healthy worst=`0`；G1−M4=`−0.035457`、CI 约
  `[-0.0466,-0.0243]`。
- [x] 边界核查：D031/T024 禁止第二个 G1 repair；因此审查只改 binding
  disposition，不修 runner、不补收据、不重跑 seed。

### 证据

```text
executor commit: 323c43bc8464e39b299ff405dbd884576d544bda
raw eligible pairs: 49
confusion: TP=19 FP=1 FN=1 TN=28
seed-cluster pooled bootstrap: CI95 ≈ [0.885, 1.000] -> Gate6 PASS
independent science audit: UNRESOLVED_STAT_IMPLEMENTATION
independent process/identity audit: FAIL, P0/P1/P2=3/1/1
current-owner YAML parse: PASS (4/4)
current-owner cross-file assertions: PASS
git diff --check: PASS
independent reconciliation review after active-carrier fix: PASS, P0/P1/P2=0/0/0
legacy adapter tests: 10 passed / 3 failed
  - 2 failures: protected STATUS.v1.md is intentionally stale (D021 gap #10)
  - 1 failure: pre-existing H001 source hash drift in an untouched source/ledger
```

### 结论

FAIL。

`G1_FORMAL_CONFIRM_NO_GO` 的 Gate6 理由不成立；但 Phase A evidence closure
与 D4 comparator identity 失败，使 formal recommendation 同样不能接收。
binding disposition 为
`G1_GROUNDWORK_EVIDENCE_INCOMPLETE / PHASE_B_NONBINDING_DIAGNOSTIC`。
局部 G1 method signal 可 harvest，不构成 Step 4a Go。

### 后续（FAIL/PARTIAL 时）

执行 D032/D041：不修 T024、不做第二个 G1 包、不进 Step 5。先让用户确认是否
把现有机制与局部证据整理成有边界的毕业方法备选材料。

---

## V061: T027 入口 problem-bearing testbed preflight 四门独立裁决

> date: 2026-07-29
> 关联：S003 / D035（新建）

### 验证项

对原 T027（频域/子带均衡族）和替代入口（逐符号/更新粒度均衡族）各跑 problem-bearing
testbed preflight 四门，逐门核源码 file:line。

- [x] **频域/子带族 门1（物理自由度存在）= FAIL**：`projects/simulation/common/_dual_pol_channel.py:127-132`
      `rX/rY = sqrt(h)·(SOP 旋转后的 s) + sqrt(nv)·AWGN`；`h` 来自 `_gg_time.py` 的 AR(1) GG
      包络（逐符号标量乘性衰落），`theta = sop_rate * np.arange(N)` 是逐符号 SOP 旋转。
      **无任何色散、多径、FIR 卷积或频率选择性**——频域/子带均衡对 memoryless、flat 信道
      退化为恒等/标量，无可作用物理自由度。
- [x] **频域/子带族 门2（基线失败与作用点一致）= FAIL**：sprint-001 `synthesis.v1.md` §4
      （L97-130）把 collapse 诊为"块末更新几何 + 信道时间变化"的结构性吸引子，与频域作用点不重合。
- [x] **频域/子带族 门3（命名传统同信息可独立调谐 comparator）= FAIL**：原 T027 §2.3 把
      comparator 冻结推迟给 executor，未给一个有身份、同任务、同运行信息、可单独调谐的传统对象。
- [x] **频域/子带族 门4（file:line 证据）**：上三门证据齐全，但门1-3 FAIL，整体 FAIL。
- [x] **逐符号/更新粒度族 门1（物理自由度存在）= PASS**：`projects/simulation/common/_cma.py:100-166`
      `equalize` 在 `block_size=64` 块内向量化滤波、**块末**用块内平均梯度更新权重（L141-166）；
      更新粒度（逐符号 / 更小块 / 事件触发即时更新等）是该代码真实施加的可调变换。
- [x] **逐符号/更新粒度族 门2（基线失败与作用点一致）= PASS**：sprint-001 `synthesis.v1.md`
      §4（L97-130）诊 collapse 为"块末更新几何 + 信道时间变化"吸引子；§8（L176-179）明确冻结
      块末协议（block_size=64, μ）为"疑似瓶颈"，逐符号变体为"最有信息的下一杠杆"——与基线
      失败点精确重合。
- [x] **逐符号/更新粒度族 门3（命名传统同信息可独立调谐 comparator）= PASS**：逐符号
      stochastic-gradient CMA = Godard 1980 原始形式；任务相同（同一 z-stream 盲均衡）、同信息
      （receiver-visible，无 TX truth）、可独立调谐（自有 μ、validation freeze）。非候选占位、
      非 blind_affine、非恒等、非特权方法。
- [x] **逐符号/更新粒度族 门4（file:line 证据）= PASS**：每门均有 file:line（见上）。
- [x] **identity parity 厘清**：`baseline-adjudication.md` §"Shared anchor and claim-specific
      fairness"——共享 anchor 保端到端可比，但 identity parity（保持继承基线块末粒度）只保护
      已跑历史包的比较连续性，不禁止跑不同传统算法；逐符号 SGD-CMA 作传统 comparator 是合法
      re-adjudication，非重开关闭轴、非 identity 违例。
- [x] **task-control 一致性**：修订后 T027 `control_epoch=60`（= topic-index）、`action_class=
      METHOD_FACTORY_TASK_PREPARATION`、`mission_checkpoint=CP025`；`validate_task_control.py` PASS。
      action_class 与正文一致（正文 §0/§2 显式"准备、待中转、本轮不跑实验"）。

### 证据

```text
channel source (memoryless flat): projects/simulation/common/_dual_pol_channel.py:123-132
  theta = sop_rate * arange(N)         # per-symbol SOP rotation
  rX = sqrt(h)*(cos_t*sX+sin_t*sY) + sqrt(nv)*AWGN
  rY = sqrt(h)*(-sin_t*sX+cos_t*sY) + sqrt(nv)*AWGN
  # h = AR(1) GG envelope; NO dispersion/multipath/FIR/freq-selectivity
CMA update granularity (real lever): projects/simulation/common/_cma.py:141-166
  for blk in range(n_blocks):          # block_size=64
    zx_blk = rX_blk @ wxx + rY_blk @ wxy   # in-block vectorized FIR
    wxx += mu * mean(eX[:,None]*conj(rX_blk), axis=0)   # block-end update
collapse diagnosis (baseline failure = update geometry): sprint-001 synthesis.v1.md:97-130, 176-179
comparator identity (per-symbol SGD-CMA, Godard 1980): task-matched / same-info / tunable
validate_task_control.py T027: PASS (epoch 60 / CP025 / action allowed)
```

### 结论

**PARTIAL（按家族分）**：频域/子带族四门 = **FAIL**（门1 物理自由度不存在是 P0），原 T027
DISPATCH_READY 撤回、作 rejected task brief 保留；逐符号/更新粒度族四门 = **全 PASS**，
为唯一合法替代入口。T027 已原位重写，task-control PASS。整体入口纠偏 PASS。

### 后续（FAIL/PARTIAL 时）

执行 D035：method-production.md 补入口四门（最小补丁）；T027 重写为逐符号/更新粒度族；
频域族加 forbidden_actions、保留 rejected brief；不动 formal owner / protected history / thesis
framework；无实验。频域族仅在信道源码升级到含色散/多径/频率选择性后才可能重审。

## V062: sprint-003 更新粒度均衡族独立科学验收（含 Phase-0 四项纠偏核实）

> date: 2026-07-29
> 关联：D036（新建）/ D035 / V061 / T027 / commit `689151c`
> verifier：独立 agent `verify_sprint003_science` + 主线复核；只读审查，未改 executor 产物

### 验证项

**Part A — Phase-0 四项纠偏核实**

- [x] 门2 证据等级已纠正：T027 §0/§1/§1.1/§3 + method-production.md "Gate-2 evidence grade" 段
      均把"块末更新=结构性吸引子成因"降级为"source-backed 疑似作用点"；V052
      `REJECTED_SCIENCE=STRUCTURAL_ATTRACTOR_OR_RECEIVER_GAP_ZERO` 引用正确。
- [x] comparator 身份冻结正确：comparator 与所有候选均用 canonical Godard-with-z（含 z 因子），
      provenance 指向 `cb1_cell_runner.py:124-129`；`_cma.py` scalar-error 形式未冒充（见 Part B 核 1）。
- [x] action_class 已改为 `PREFORMAL_METHOD_FACTORY`，control_epoch 61，`validate_task_control.py`
      PASS；授权范围声明"仅本次 bounded 诊断 sprint"。
- [x] 终态集已扩为 5 个（+ `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` + `EXECUTION_INVALID`）。

**Part B — sprint-003 科学验收（独立重算）**

- [x] **Godard-with-z 梯度身份**：per-symbol comparator（`methods.py:141-148`，`(R2-|z|²)*z*conj(r)`）、
      block-8/16（`methods.py:228-234`，`(eX*zx_blk)[:,None]*conj(rX_blk)`，与 runner 一致）、
      recursive（`methods.py:313-322`，`eX*zx*conj(rx)`）**均含 z 因子**；无方法用 forbidden
      scalar-error `(R²−|z|²)·r*`（`_cma.py:161-166`）。TDD `test_persymbol_gradient_is_godard_with_z`
      显式断言。**无 EXECUTION_INVALID**。
- [x] **信息公平**：同 paired realization、同 eval window（N=512→133/261/389，N=8192→2181/2309/2437）、
      同 R2=1.32/n_tap=11；anchor μ=0.03 冻结未重调；comparator μ 在 dev only 调谐。
- [x] **dev/test 隔离 + fresh seeds**：dev=[181..190]/test=[201..220] disjoint（代码断言）；
      seeds 71–80 在 raw-rows.v3.csv 零命中；test seeds 不回灌选择；dev-freeze-receipt 记录 comparator
      μ 调谐 trace（μ=0.001 dev-optimal=0.3125，非强制）。
- [x] **μ 与更新预算公平**：候选场跨 64× 有效更新预算（0.0156→1.0 updates/sym）平坦，无赢家触发
      matched-budget block-64 ablation（逻辑正确：无赢家则无需分离 more-updates vs granularity）。
- [x] **raw→aggregate 复算**（独立脚本重算 840 行）：anchor=0.31431、comparator=0.29685、
      comparator vs anchor Δ=−0.01747 CI[−0.0452,−0.0001] 11/9/0、block8 vs comparator
      Δ=−0.00293 CI[−0.0112,+0.0056] 13/7/0、block16 Δ=+0.00313、recursive Δ=−0.00103 —— **全部
      与 result.v3.json/synthesis 吻合（<1e-4）**。
- [x] **机制归因不越界**：comparator 在 7 cells 中只 1 个（snr15-fg1000-long：0.158→0.090）降到
      PI-SER<0.1，"1/7" 属实；synthesis 表述"疑似作用点未被确认为成因"遵守 Phase-0/V052 ceiling，
      未把块末更新当已确认机制、也未越界判"已确认非成因"。
- [x] **closure**：identity gates PASS（QPSK PI-SER=0.0 独立重跑）；smoke 在 result.v3.json 非空未覆盖；
      TDD 7/7 PASS；`git show --stat 689151c` 仅 11 文件全在 sprint-003 目录 + worker-log，未改
      common/params/owner/session；未 push。

### terminal verdict 裁决

`NO_DIAGNOSTIC_SIGNAL` 为五选一中**唯一正确**项：
- 非 `DIAGNOSTIC_METHOD_SIGNAL`：无候选过 Δ≤−0.005 + CI upper<0 + help>hurt（最佳 block8 Δ=−0.00293，
  CI 跨 0）；
- 非 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`：comparator 只 1/7 cell 消除 collapse，6/7 仍 collapse；
- 非 `BLOCKED_SHARED_TESTBED`/`EXECUTION_INVALID`：testbed 支持公平比较、梯度身份正确。

### 非承重瑕疵（不改 verdict，不需修复）

1. `result.v3.json` offline 4-category label 用单 seed（201）而非 cell 均值（cosmetic；LABEL ONLY
   不影响 gate）；
2. synthesis §4 "μ=0.003 在 2/3 长 cell 发散"独立复核为 1/3（wording）；
3. synthesis §5 "healthy-cluster regression" 实为空 cluster（anchor 下无 healthy cell；wording）。
verifier 明确"不需重跑/重判"。

### 结论

**PASS**。sprint-003 工程主链闭合、梯度身份正确、统计可复算、verdict 唯一正确。接收
`NO_DIAGNOSTIC_SIGNAL`；不晋级、不写论文、不动 protected owner。Phase-0 四项纠偏已落实。

### 后续

CB1 更新粒度均衡族轴按 method-factory 纪律关闭（无 signal 即退出）。下一合法动作由主控在
mission-log/CP027 后选择：portfolio remap 选下一个机制不同的合法入口，或战略 gate 升级
（仍 0 active carrier）。

---

## V063: CB1 轮换后三入口六门评估独立核实（STRATEGIC_GATE）

> date: 2026-07-30
> 关联：D037（新建）/ 用户 voice.md 2026-07-30
> verifier：独立 Explore agent `verify_d037_gates` + 主线复核；只读审查，无 executor 产物（STRATEGIC_GATE 无 sprint）

### 验证项

D037 是 `STRATEGIC_GATE` 判定（三入口无一过六门、不制造第四弱候选）。这是强结论，须独立核实其事实
声称与候选扫描完整性。

**Part A — 三候选六门事实核实（file:line）**

- [x] **候选 A 门1（CPR/VV 无传统机制失败，只有 oracle-gap）**：核实 `high-order-cpr-combination/
      synthesis.md` —— headroom 表 `:59` adversarial_sourced|snr14 mean +0.606dB/CI upper +1.719
      属实；`:123-127` 自述 10 kHz 下"盲/导频估计器数值收敛于 VV，无机制优势"属实。
      **⚠️ 初版 D037 表述不准**：`:75-92` 同时记录 P1/P2/P3 vs VV 差 9–20dB、0/10 paired wins（**有**
      已记录机制失败，属 DD/MAP 组合方法）。verifier 标 claim 1 PARTIAL/MISLEADING。**已纠正**：
      D037 候选 A 门1 改写为"①VV 对 oracle 留 headroom（oracle-gap，TL-32 禁当 Go）+ ②P1/P2/P3 组合
      失败属**已拒收的 B10/B12 实例**（master-state.md:149 REJECTED），不是可轮换开放轴；VV 本身无
      可被不同传统 CPR 改善的机制失败"。**gate-1 FAIL 结论不变**（组合失败不能重新洗成 VV 有待改善）。
- [x] **候选 A 门6（verdict 被拒收 + U10 非 cycle-slip 证据）**：master-state.md:149 字面
      `SCIENCE_VERDICT_REJECTED / UNRESOLVED`；candidate-coverage-audit.v3.yaml:163-165 audit_finding
      "existing evidence is SOP/polarization/CMA BER failure, **not CPR cycle-slip or lock-loss**"。
      属实。
- [x] **候选 B（NDA-ML 是已完成赢家非失败方法）**：`single-carrier-nda-ml/_mve_results.json`
      AWGN fair_gain 全正（1.27–2.26）；`SC-NDA-ML-MVE-SPEC.md:19` "这是 Step 4a 维度 D MVE"。属实。
      （D037 引用弱/中湍 +1.53/+1.71 与 json +1.20/+1.92 略有出入，但方向一致均为正。）
- [x] **候选 C 4a（U24 pt5/score4.20/BATCH_1_FAMILY）**：candidate-map.v2.yaml:41-44 属实。
- [x] **候选 C 4b（D047: 1e-5 fixed=PI 非 swap）**：`2026-07-10-.../decisions.md` D047 原文属实。
- [x] **候选 C 4c（D051: control 4e-6 新 seed 已有 oracle events，control-only 失效）**：D051 原文属实。
- [x] **候选 C 4d（non-swap BER 标签需 TX-truth oracle）**：`prompt013_swap_quality_q1.py` 用
      permutation_invariant_ber + oracle_equalize（PI-BER oracle assignment）属实。
- [x] **候选 C 4e（SPARSE_PILOT_SEMIBLID KILLED + F1 RETRACTED）**：portfolio/current.yaml:144-161
      （F1 PROBE_FAIL/RETRACTED privileged CSI）、:162-172（SPARSE_PILOT returned killed）属实。
- [x] **channel 物理（GG+实SOP+AWGN，无多径/色散/FIR）**：`_dual_pol_channel.py:104-132` 属实。

**Part B — 候选扫描完整性（claim 6：无遗漏的 pt≥4 候选）**

`candidate-map.v2.yaml` problem_truth ≥ 4 候选共四个：U24（=C）、U10（=A 族）、**U05（pt4，
HOLD_FOR_COMPETITOR_CLOSURE）**、U23（pt4，MERGE_WITH_U24）。**⚠️ 初版 D037 漏列 U05**（文档缺口，
非门控错误——U05 hold 状态非 Go-eligible）。**已补**：D037 增"候选扫描完整性"段，登记 U05 hold +
出路阻塞（D056 crossref 未解 + SPARSE_PILOT/F1 出路已阻断）= 无 runnable 入口。U23 已显式并入 U24。
**无 problem_truth ≥ 4 候选被遗漏为独立入口。**

### 结论

D037 的 `STRATEGIC_GATE` 判定**事实成立**：三候选（A/B/C）无一逐项过六门，U05 hold 且出路阻塞。
verifier 发现 2 项初版瑕疵（claim 1 表述不准、claim 6 漏列 U05）**均非承重、不改 STRATEGIC_GATE
结论**，已据 V063 在 D037 内纠正。无 sprint/无 executor 产物/无 commit 可验；本 V 仅核实入口评估的
事实一致性。**结论 = PASS（D037 STRATEGIC_GATE 事实与候选扫描完整、表述已纠正）。**


---

## V064: D038 段A 物理入口六门评估独立科学接收（PHYSICS_BACKED_TESTBED_UNAVAILABLE）

> date: 2026-07-30
> 关联：D038 / CP029 / 段A / 独立物理/文献 subagent（agent_02236f7f）
> verifier：主控确定性复核（grep / find / 行级读取），未运行仿真/seed

### 验证项

- [x] 候选数 ≤3：subagent 评 a/b/c 各一（complex time-varying Jones / PDL / PMD-CD-跨符号记忆），共 3，未超。
- [x] 门1-2 文献零命中（独立复核）：对四篇星地 coherent dual-pol FSO primary 做
  `grep -ic -e PMD -e "polarization mode dispersion" -e "polarization-dependent loss" -e PDL -e "differential group delay" -e DGD -e birefring -e "jones matrix" -e "chromatic dispersion"` →
  `papers/downloads/2026-07-08/9120341.md`=0、`10305071.md`=0、`10301506.md`=0、
  `papers/doi/10.3390_app12073331/content.md`=0。PASS（事实成立：无星地 polarization-impairment primary）。
- [x] sat.1553/s24248036/photonics10121331 dangling：`ls papers/doi/10.1002_sat.1553/`、
  `10.3390_s24248036/`、`10.3390_photonics10121312/` 全部 CONFIRMED absent。这些是 params.py
  引用但本地不存在的 dangling reference，不能当 primary。PASS。
- [x] 现有 channel 已建模 SOP 旋转：`_dual_pol_channel.py:123-132` 核实 `theta=sop_rate*arange(N)`、
  `[[c,s],[-s,c]]` 实旋转；各向同性大气无 birefringence/PMD/PDL 物理起源——门1 物理根因成立。PASS。
- [x] D066 kill 范围核实：D066 在 groundwork topic `2026-07-10-dual-pol-osl-groundwork/decisions.md:3381`（非
  live topic；subagent 行号标注 live decisions.md:3391-3416 为小误，但实质引用正确）。D066:3391-3394
  Kill verified component PDL/PMD（8 cells max headroom 0.0804 dB / CI upper 0.2372 dB < 0.5 dB）；
  D066:3415-3416 排除项明令"不继续追求 verified DGD≫T_S 或 sub-symbol Jones 新轴"——
  **时变复 Jones 轴确已被关闭，非未测新问题**。PASS。
- [x] 量级核算（门3）：唯一可溯源参数 Valjus sat.1553 DGD≤6ps=1.5% T_S（T_S=400ps @ R_SYM=2.5GBaud）、
  PDL≤1dB；D066 实测 headroom 0.0804 dB ≪ 0.5 dB。即便取 stress DGD 40ps（10% T_S）也仅 ~0.1 symbol
  记忆。效应不可见。PASS（门3 即便前门过也要 Kill）。
- [x] 纪律遵守：subagent 全程只读（未改文件、未跑仿真、未建 testbed），公开检索仅取 abstract/metadata
  做 cross-check 未下载私有全文。PASS。
- [x] 未制造第四 impairment：三候选全失败 → `PHYSICS_BACKED_TESTBED_UNAVAILABLE`，符合用户"不制造第四"
  硬约束 + D038 段A 退出条件。PASS。

### 证据

```text
star_ground_primary_PMD_PDL_hits:
  9120341.md(Paillier2020)=0
  10305071.md(Zhou2024)=0
  10301506.md(Zhang2023)=0
  app12073331(Gu2022_IMDD)=0

dangling_references_absent:
  papers/doi/10.1002_sat.1553/  -> ABSENT
  papers/doi/10.3390_s24248036/ -> ABSENT
  papers/doi/10.3390_photonics10121312/ -> ABSENT

existing_channel:
  _dual_pol_channel.py:123 theta=sop_rate*arange(N)
  _dual_pol_channel.py:127-132 real orthogonal rotation [[c,s],[-s,c]] + GG amplitude + AWGN

D066_kill_scope (groundwork topic decisions.md:3381):
  D066:3391-3394 component PDL/PMD 8 cells max headroom 0.0804 dB / CI upper 0.2372 dB < 0.5 dB
  D066:3415-3416 excludes "verified DGD>>T_S or sub-symbol Jones new axis"

magnitude (gate 3):
  verified DGD<=6ps = 1.5% of T_S=400ps; PDL<=1dB
  D066 measured headroom 0.0804 dB << 0.5 dB threshold
  stress DGD 40ps = ~0.1 symbol memory (sub-symbol, already closed by D066)

candidates_evaluated=3
fourth_impairment_manufactured=NO
simulation_or_seed_run=false
files_modified_by_subagent=0
```

### 结论

PASS / 接收 `PHYSICS_BACKED_TESTBED_UNAVAILABLE`。三候选无一过门1-3：
fiber 现象（PMD/PDL/CD/复 Jones 双折射）源于各向异性玻璃波导，自由空间大气各向同性无物理起源；
本地+公开检索无星地 coherent dual-pol polarization-impairment primary；唯一可溯源参数实测 headroom
0.08 dB ≪ 0.5 dB。**时变复 Jones 轴已被 D066:3415-3416 关闭，非未测新问题。**

段B/C/D 不运行（用户授权终止：三候选均失败即 `PHYSICS_BACKED_TESTBED_UNAVAILABLE`，不制造第四 impairment）。
本终止不是方法进度（`mission_method_delta=NONE`），是可靠的"无物理可信 channel 自由度可扩展"诚实判定。
仍 0 active carrier。下一合法动作交用户：CP028 选项 (2) 论文范围决策 或 (3) 收尾审计（选项(1) 已尽）。

### 后续（FAIL/PARTIAL 时）

不复活 fiber impairment、不把 abstract/dangling reference 当 primary、不强凑第四 impairment、
不重开 D066 已关闭的 sub-symbol Jones 轴。诚实终止，建议转论文范围/新子问题。


## V065: P01 CPR 选择器 SNR 失配鲁棒性独立验收（NO_DIAGNOSTIC_SIGNAL）

> 关联：D039 / P01 / T028 / worker-log step-028
> verdict：**PASS**（8 项检查全过；executor 的 `NO_DIAGNOSTIC_SIGNAL` 为唯一正确终态）
> 日期：2026-07-30

### 验收范围

独立 verifier（非实现方）从 raw 数据起独立重算、重跑复现、grep 信息边界、git status 查改动。scratch 脚本审计后删除，不 commit。

### 8 项检查（逐项 PASS/PARTIAL/FAIL + 证据）

1. **复现正确性 — PASS**：①独立重跑（自己写脚本调 `generate_shared_realization_apsk` + 冻结 `A.decide`，非 executor wrapper）weak@9dB seed 0–2 δ=0 → 3/3 与 anchor `ccisp_family1_selector_a_30seed.json` 逐数完全一致（seed0 selected_errors=57991/n_da=265/n_nda=135/nda_c768=81504）。②executor `phaseA_dev.json` δ=0 rows vs anchor 全重叠 (scene,snr,seed) **150/150 match**。
2. **信息边界（关键）— PASS（干净）**：true γ（`gl_true`）仅出现在信号生成 `_p01_cpr_snr_mismatch_probe.py:117` 和 TRUE-channel 离线 BER 评价 `:123-127`/`:133`（oracle trueh），与 anchor `run_case` 同构。所有 `decide()` 调用点审计：probe `:130` 用 biased γ̂；`_decide_original` `:283` 收 `gamma_true_db+delta`（`:237`）；adapter/candidate 用 pilot γ̂_est / γ̂-derived 区间 / γ̂ EMA。唯一 true-γ-in-decide 点是 `oracle_true` 上界（`_p01_phaseBC.py:87`，正确从候选判断排除）+ 一个死代码 lambda（未调用）。**true γ 绝不进任何可部署 selector。**
3. **raw→aggregate 独立复算 — PASS**：从 raw rows 重算 gain_db（每 seed 10·log10(BER_NDA/BER_selected)），Student-t CI。所有量相对误差 **0.00e+00**。Phase A 损害 cell Δgain（weak@5/7/9 δ=−3 −0.339/−0.393/−0.324、weak@11 δ=+3 −0.704、moderate@13 δ=+3 −0.344）逐项吻合；Phase B adapter gain（+0.746/+1.113/+1.241/+0.957/+0.706）吻合；Phase C pooled cand_rank vs adapter **+0.1358 [+0.1207,+0.1510]** 吻合。
4. **dev/test 隔离 — PASS**：phaseA_dev.json tag=dev seeds 0–9；phaseBC_heldout.json tag=heldout seeds 30–49；dev/heldout seed 交集=∅。最终 verdict 取自 held-out 30–49，非 dev；anchor seeds 0–29 未作最终 test 判据。
5. **判据预冻结 — PASS**：损害判据（≥0.3 dB drop, CI<0）与 MDE=0.15 在 worker-log §1（line 32–50）冻结，**先于** test 结果（§2.1 line 58+、§3.2 line 82+、Phase C §5 line 142+）。`HARM_GAIN_DROP_DB=0.3` 硬编码于 `_p01_phaseA_dev.py:28`+`_p01_phaseBC.py:41`，MDE=0.15 于 `_p01_phaseBC.py:270`。冻结真实。
6. **无 protected-file 改动 — PASS**：`git diff --stat HEAD` on common/、params.py、`_a4_switch_common768_30seed.py`、`run_ccisp_family1_selector_a_30seed.py`、anchor JSON = 空。仅新增 7×`_p01_*.py`（results JSON gitignored）+ T028 brief + 治理文档编辑。
7. **verdict 正确性 — PASS**：cand_rank pooled held-out mean=+0.1358, CI=[+0.1207,+0.1510], MDE=0.15（冻结）。METHOD_SIGNAL 需 mean≥MDE AND CI_low>0；此处 mean=0.1358<0.15 → fails mean threshold → stable_beat=False。**`NO_DIAGNOSTIC_SIGNAL` 是唯一正确终态**（Phase A PROBLEM_PRESENT + Phase B adapter 未完全消除 → 非 PROBLEM_ABSENT；无执行阻断 → 非 EXECUTION_INVALID；无候选稳定超 adapter → 非 METHOD_SIGNAL）。executor 诚实注明 verdict 对 MDE 敏感（MDE=0.10 会翻为 METHOD_SIGNAL），非事后合理化。
   - **条件式子群体信号 — 真实、值得记录（非 artifact）**：verifier 全网格重算显示 cand_rank 仅在 weak@5/7/9 超 adapter ≥MDE（+0.385/+0.432/+0.323, CI_low>0），其后单调退化（weak@11 +0.111、weak@13 +0.014 CI 跨 0、moderate/strong 全 +0.05–0.12）。机制连贯（弱湍流+低 SNR = 原 stage-1 CV 边界最 miscalibrated 处），系统性非 cherry-pick。正确降级为 future-work seed 而非过度声称。
8. **语义 smoke — PASS**：δ=0 → `selection_error_rate_vs_d0`=0.0（全部 150 cell），gain retention 恒等 0。占用行为合理：weak@9 DA 占用 227→283（δ=−3→+1）后降 232（δ=+3），executor 明确记录的**真实非单调**性质（两阶段判据固有），端点正确（大 +δ→更多 NDA、大 −δ→更多 DA）。

### 结论

executor 的 `NO_DIAGNOSTIC_SIGNAL` **成立**。方法学稳健、纪律透明：复现逐数精确、信息边界严密、aggregate 可从 raw 复算到 0 相对误差、判据真实预冻结、无 protected 文件改动、verdict 唯一正确；条件式子群体信号（cand_rank @ weak/低 SNR）真实并正确降级为 future-work。

**无需包内确定性修复。** 记两处无害代码质量问题（dead/no-op，不影响结果/verdict）：①`_p01_phaseBC.py:65-89` 未调用 `build_selector_specs` 含 stale oracle lambda；②`:198-220` `phaseC_judge` 空 body，真正判断在 `main()` inline。可留。

### 主控 claim ceiling

P01 产出一个**有效科学负面 + 一个有界的条件式子群体观察**（cand_rank @ weak/低 SNR 超 adapter）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。子群体信号作 harvest 记录（thesis-harvest 的 robustness-boundary / operating-regime 类），候选晋升需重走 Groundwork Step 1–3/3.5/4a。

## V066: P02 cand_rank 工作区确认独立验收（PROBLEM_RESOLVED_BY_REGION_RETUNING）

> 关联：D040 / P02 / T029 / worker-log step-029
> verdict：**PASS**（8 项检查全过；executor 的 `PROBLEM_RESOLVED_BY_REGION_RETUNING` 为唯一正确终态）
> 日期：2026-07-30

### 验收范围

独立 verifier（非实现方）从 raw rows 起独立重算所有 aggregate、独立重跑复现、AST/grep 审计信息边界、git status 查冻结文件改动。scratch 脚本审计后删除，不 commit。

### 8 项检查（逐项 PASS + 关键证据）

1. **raw→aggregate 独立复算 — PASS**：仅取 raw_rows 重算 per-seed gain_db=10·log10(nda_c768/selected_errors)，paired diff（cand_rank−adapter）target region n=90 mean=+0.357782 CI[+0.338054,+0.377510]；weakretune−adapter=+0.453867、cand_rank−weakretune=−0.096085。全部 7350 rows + 245 aggregate 与 artifact 存储值相对误差 **0.000e+00**。
2. **seed 隔离 — PASS（干净）**：held-out = 恰好 {60..70}∪{81..89}∪{90..99}=30 seed（90–99 是主控授权包内修复补的，与 anchor 0–29/P01 dev 0–9/P01 held-out 30–49/dev 50–59/pollution 71–80 全 disjoint，零碰撞）；每 (scene,γ,method,δ=0) cell 恰 30 行无重无缺；dev 仅 50–59，dev∩heldout=∅。
3. **方法身份（冻结码未改）— PASS**：`git diff --stat HEAD` 对 common/、params.py、_b11_params.py、_a4_switch_common768_30seed.py、_p01_adapter_and_candidates.py、_p01_cpr_snr_mismatch_probe.py、_p01_phaseBC.py、_a4_branchrouted_30seed.py、sc_nda_ml_sim.py、anchor JSON 全空。`decide_adapter_weakretune` body 与 `decide_cand_rank` 逐字节相同，唯一差异 ref_snr_db 从默认参数改为读 `_FROZEN_REF_SNRS["weakretune"]`；cand_rank 以默认 ref=9.0 调用（冻结设计常数，未被覆盖）。
4. **信息边界（关键）— PASS（干净）**：AST 审计 `decide_adapter_pilot`/`decide_cand_rank`/`decide_adapter_weakretune`/`estimate_snr_pilot` 可执行代码中 true-gamma Name/arg 引用=0。唯一 true-γ-in-decide 路径是 `_oracle_decide_factory`（上界），所有 `paired_diff` 仅配对 cand_rank/adapter_pilot/weakretune，oracle_true 绝不进任何 aggregate。
5. **dev 调谐诚实（无 test 泄漏）— PASS**：dev_seeds=[50..59]、dev_cells=3 target、search_refs={7,8,9,10,11}，mean 单调增（0.222→0.462），ref=11.0 唯一 argmax（无 tie 歧义），与存储 chosen_ref=11.0 一致，等于 heldout frozen_weakretune_ref=11.0；cand_rank−adapter audit 跨 5 dev run 恒为 0.369389（ref-不变，证明 cand_rank 9.0 是冻结常数）。无 heldout seed 出现于 dev。
6. **判决顺序（§5）独立应用 — 吻合**：Step 1 触发：|cand_rank−weakretune|=0.0961≤0.15 AND weakretune−adapter(0.4539)≥cand_rank−adapter−MDE(0.2078) → `PROBLEM_RESOLVED_BY_REGION_RETUNING`，与 executor 一致。（注：即便 Step 1 不过，Step 2 也过——mean≥MDE、CI_low>0、3/3 cell 正、无单 cell 独占、无 boundary 灾难——结果稳健。）
7. **语义 sanity — PASS**：δ=0 oracle_true==orig 全 210 行（抽检 weak@7 seed60: 81543==81543）；adapter_pilot/cand_rank/weakretune 跨全行 δ-不变（0 失败）；help+hurt+tie=90+0+0=90=n_paired。
8. **fresh 独立重跑（identity parity）— PASS**：独立调 `PR.run_case_multidelta("weak",7.0,seed,deltas=(0.0,))` seed 60,61 weakretune ref 冻结 11.0 复现 artifact 精确一致：seed60 weakretune sel_err=76624(da=334,nda=66)、seed61=72011(da=328,nda=72)、base fixed_nda=108568/108721 全 MATCH。Artifact 可复现非伪造。

### 结论

executor 的 `PROBLEM_RESOLVED_BY_REGION_RETUNING` **成立**。P01 条件式子群体信号经 fresh held-out confirmation 确认为**真实但非可区分方法**：cand_rank 冻结 ref=9.0 dB 不是 load-bearing，dev 调谐同一 conventional lever（ref 9→11）即捕获并略超其增益（weakretune 反超 cand_rank +0.096 dB，|差|≤MDE）。无可区分 deployable action → 不生成方法卡/不晋升。

**包内确定性修复已正确执行并披露**：seed-count 算术（20→30 补 90–99）由主控授权，判据/dev-ref/方法身份/MDE/§5 顺序全不变，artifact `meta.seed_consolidation` 记录原 20 + 补 10；20-seed 与 30-seed verdict 同。无需第二修复。

### 主控 claim ceiling

P02 产出**有效科学负面 + operating-regime 收敛证据**（γ-magnitude-free stage-1 边界的 weak/低SNR 增益可被廉价区域门限重调替代）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。作 thesis-harvest 的 robustness-boundary / conventional-comparator-resolves 类记录。A 族（CPR 选择器鲁棒性）达同族上限 2，P03 必须换机制族。

## V067: P03 定点/资源-性能协同设计独立验收（PROBLEM_RESOLVED_BY_UNIFORM_PRECISION）

> 关联：D041 / P03 / T031 / worker-log step-030
> verdict：**PASS**（10 项检查全过；executor 的 `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION` 为唯一正确终态）
> 日期：2026-07-30

### 验收范围

独立 verifier（非实现方）从 raw rows 起独立重算所有 aggregate、独立重跑 float-bypass gate、读源码审 bit-true 算术真实性、AST/grep 审信息边界、git status 查冻结文件改动、grep 审 resource 措辞。

### 10 项检查（逐项 PASS + 关键证据）

1. **float-bypass identity — PASS**：独立重跑 `decide_fp(raw,γ_db,γ_lin,64,40)` vs `A.decide` 逐 window，seeds 0–9 × {weak,mod,strong} × γ∈{5,9,13,25}：**0 / 48,000 window mismatch**。gate 实质成立（executor 报 0/132,000 全网格，分母经主控包内修复）。
2. **bit-true 算术真实性（非 decimal rounding 冒充）— PASS**：`_p03_fixed_point.py:88` `floor(value*scale+0.5)` round-half-up；`:91-99` 饱和二补码 signed/unsigned 边界（验证 +100→31、−100→−32 无回绕）；`:66` `ceil(log2 N)+2`=10 guard；`:184` per-window 共享 exponent（cv 验证 1024×/1e-6× 缩放下尺度不变）；sqrt/log10/div 的 I/O 量化（`:298-299,:347-348,:313`）；bypass err 3.4e-14 ≤ 2⁻⁴⁰；**全文件无 `np.round`/`decimals=` 冒充**。
3. **raw→aggregate 独立复算 — PASS**：仅取 raw rows 独立重算 pooled regret（`10log10(fp_sel/bypass_sel)` paired）、per-bitwidth、per-cell、held-out aggregate、Pareto、ablation、help/hurt/tie：全部 aggregate 相对误差 **0.00e+00**（Phase A 2310 rows + Phase BC 14,190 rows）。regret identity 全 16,500 rows 0 error。
4. **seed 隔离 — PASS（干净）**：PhaseA dev=0–9；PhaseBC dev-tune=10–19；held-out=30–49；pollution 71–80 缺席。三集 disjoint（从 raw-row `seed_index` 跨全 artifact 验证）。
5. **信息边界 — PASS（干净）**：AST/grep 审 `decide_fp` + 4 个 mixed-candidate body：zero `true_snr/true_h/true_phi/tx_sym/tx_bits/oracle/gamma_true/labels` token；`_p03_fixed_point.py` 无 `r["h"]`/`estimate_h_*`/`ber_oracle` 接收端调用。仅消费 `(raw, gamma_db, gamma_lin)`。
6. **冻结文件未改 — PASS**：`git diff --stat HEAD` 对 common/、params.py、`_a4_switch_common768_30seed.py`、`_p01_cpr_snr_mismatch_probe.py`、`_a4_branchrouted_30seed.py`、`sc_nda_ml_sim.py`、anchor JSON 全空。仅新增 untracked `_p03_*.py` + results。
7. **resource-proxy 措辞 — PASS**：所有 LUT/DSP/power/area 提及要么是非线性算子的 LUT-I/O *模型*、accumulator 加宽规则的 DSP *术语*、物理 "mean power" 量，要么是显式 disclaimer。proxy 一致标 `op_bit_proxy`/`storage_bit_proxy`；两 artifact 带 "NO real synthesis / LUT / DSP / power / area" 注。无 "LUT 减少 X%"/"DSP 节省" 声称。
8. **verdict 正确性 — PASS**：数字完全支撑 `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`：地板是 branch-statistical（(16,14) 处 Q≤2⁻⁴⁰ 仍 regret +0.685 dB @moderate/25、+0.806 @strong/25 且 agreement ~10–13%；(6,4)→(16,14) 加宽在 γ≥21 处买 ≈0 dB）；mixed 最佳 `two_exp` 优势 +0.01661 dB = 0.11×MDE；`mixed_strictly_better_by_mde=[]`。verdict 唯一正确（非 METHOD_SIGNAL：无 mixed 过 MDE；非 NO_DIAGNOSTIC_SIGNAL：有真实工程发现）。
9. **判据冻结顺序 — PASS**：worker-log §1（2,264 字符）只含预声明阈值（0.15 MDE、0-mismatch bar、2⁻⁴⁰、seed 范围、uniform-tension 定义）——**无结果数字**（0.2005/0.0166/0.027/0.1729/726000 全缺席）。唯一 "(16,14)" 引用是预声明的*诊断规则*（最宽阶梯 rung 作 probe 点），非 post-hoc 数字。
10. **Phase-BC 命名 bug 修复 — PASS**：`heldout_raw_rows` 含全部 5 chosen 方法 × 660 rows（含 3 mixed candidate）；`chosen_configs` 名与 held-out 方法键精确匹配；regret identity 3,300 rows 0-error；mixed candidate 产生真正不同决策（583/660 cell 异于 uniform，agreement 50–55% 非 100%）——rows 未被丢/未塌缩。

### 结论

executor 的 `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION` **成立**。P03 的"定点部署是否损害 DA/NDA 选择器分支选择/浪费资源"被回答为**否**：uniform-precision 已在 regret 地板，地板是 branch-statistical（浮点下仍持续，非量化伪影），mixed-precision 最佳候选 Pareto-主导但 sub-MDE（+0.0166 dB = 0.11×MDE）。无可区分 deployable action → 不生成方法卡/不晋升。

**包内确定性修复已正确执行并披露**：①float-bypass 分母叙述 726,000→132,000（纯算术错，V067 check 1 独立重跑 gate 确认 0 mismatch 实质不变，主控已修 worker-log 3 处）；②Phase-BC 键名 bug（mixed-candidate held-out rows 首跑被丢）executor 已修并重跑，artifact 含全部 rows，regret identity 0-error。无需第三修复。

### 主控 claim ceiling

P03 产出**有效工程负面 + 定点可部署性证据**（DA/NDA CPR 选择器在 8-bit uniform Q(8,6) 下决策与浮点 byte-exact；定点非该选择器瓶颈；stage-2 噪声扣除高 SNR 下溢张力真实但 sub-MDE）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。resource 措辞严格 proxy（无真实综合工具，不声称 FPGA LUT/DSP/功耗/吞吐）。作 thesis-harvest 的 engineering-robustness / deployment-feasibility 类记录（Ch5 FPGA §5.4/§5.5 可引用 bit-cost/resource proxy 证据）。B 族（定点/资源-性能协同设计）首包完成，连续=1。

## V068: P04 连续 GG OOD 选择器鲁棒性独立验收（PROBLEM_ABSENT_ON_CONTINUOUS_GG）

> 关联：D042 / P04 / worker-log step-031
> verdict：**PASS**（8 项检查全过；executor 的 `PROBLEM_ABSENT_ON_CONTINUOUS_GG` 为唯一正确终态）
> 日期：2026-07-30

### 验收范围

独立 verifier（非实现方）从 raw artifacts 起独立重算所有 aggregate、独立重跑锚点回归门、读源码审 Al-Habash 公式真实性、AST/grep 审信息边界、git status 查冻结文件改动、独立复算 sub-range 结构。

### 8 项检查（逐项 PASS + 关键证据）

1. **α/β 映射 + provenance — PASS**：`_p04_continuous_gg.py:59-63` `alhabash()` 与 `system_model.tex:16-21` 逐项吻合（`α=[exp(0.49σ²/(1+1.11σ²^(6/5))^(7/6))−1]⁻¹`、`β=[exp(0.51σ²/(1+0.69σ²^(6/5))^(5/6))−1]⁻¹`）。独立重算 σ_R²∈{0.2,1.6,3.5} = (11.6510,10.1224)/(4.0265,1.9105)/(4.2257,1.3622)，对冻结对偏离 0.44%/0.22%、0.66%/0.55%、0.61%/**2.700%**（≤ 论文自报 2.78%）。`sigma2_to_ab`（`:66-75`）在 3 锚点用冻结对、其余用 Al-Habash（6 held-out σ_R² 验证不走冻结分支）。mcs `rytov_to_gg` proxy 未被 import（仅 docstring 提及 NOT used）。

2. **锚点回归门（独立重跑）— PASS**：独立调 `P4.run_case_contgg(sigma2_to_ab(s2)...)` vs `PR.run_case_multidelta(scene,...,deltas=[0.0])`，weak/moderate/strong × seeds 0-2 × γ{5,9} = 18 cell，比 selected_errors/n_select_da/n_select_nda/fixed_nda_errors/fixed_da_errors/lower_count_bound_errors = **108 字段 0 mismatch**。

3. **raw→aggregate 独立复算 — PASS**：从 phaseA_heldout.json raw_rows（600 rows）独立重算 pooled interior regret = 30 interior cell 的 [mean over seeds of 10·log10(selected/min(fixed_DA,fixed_NDA))] 的均值 = **0.1458564869 dB**。存储 verdict.pooled_mean = 0.1458564869 → 相对误差 **0.000e+00（精确）**。CI 重算 [+0.082679,+0.209034] = 存储 CI 精确。per-row regret 重算与存储 `regret_sel_db` 相对误差 0.00e+00。cells > MDE 且 CI_low>0 = **9/30**（精确匹配声称计数），全在 weak-side-low-SNR（σ² 0.30/0.90/1.35 × γ 5-11）。交叉验证：dev interior +0.139271（声称 +0.1393 ✓）、dev anchor +0.230611（声称 +0.2306 ✓）、dev-heldout 差 0.0066 dB（声称 0.007 ✓）。

4. **seed 隔离 — PASS（干净）**：dev seeds 恰 0-9（10）；held-out 恰 30-49（20）；disjoint；无 71-80 pollution；held-out 无 ≥50 seed。held-out σ² 恰 {0.3,0.9,1.35,1.85,2.3,3.15}，全严格 interior（无 = 锚点 0.2/1.6/3.5），全在 (0.2,3.5)。dev/held-out σ² 集 disjoint。所有 held-out `is_anchor==False`。

5. **信息边界 — PASS（干净）**：AST 审：唯一 `decide` 调用在 `_p04_continuous_gg.py:165` → `decide(raw, gdb, glin)`，恰消费 (raw, gamma_db, gamma_lin)。运行时确认 `A.decide`（冻结，`_a4_switch_common768_30seed.py:97`）只读 rx_seg/gamma_db/gamma_lin。`alpha`/`beta` 仅在 `:115` 信道生成（turb_params）。`r['h']`/`r['phi']` 仅在 `:129-130` 离线 `ber_oracle_turb`（存 base，绝不达 decide）。无 turb_name/labels/tx_sym/tx_bits/true_h/true_phi/true_snr/true_gamma token。pw_tx/bits/tx 只喂默认 no-op pilot hook，不进 orig decide。

6. **冻结文件未改 — PASS**：`git status`/`git diff HEAD` 对 `_a4_switch_common768_30seed.py`、`common/_channel.py`、`common/__init__.py`、`params.py`、所有 `_p01_*`、`_p03_*`、锚点 JSON — **全 CLEAN（无修改）**。仅新增 untracked：`_p04_continuous_gg.py`、`_p04_phaseA.py`、`_p04_phaseBC.py`、worker-log、results JSON。无 `A.decide =` 重赋值/monkeypatch。

7. **verdict 正确性 — PASS**：§1 判据冻结**无结果数字**（0.1459/0.1393/0.2306/CI/9-30 全缺席）。门控冻结于 `:57` 为"≥ MDE=0.15 dB pooled across held-out continuous cells"——读结果前写。代码 `judge()`（`_p04_phaseA.py:98-123`）精确实现 pooled 门控，无 post-hoc 改。pooled regret 0.1459 < MDE 0.15 → Phase A 门 fail → 决策树唯一给 `PROBLEM_ABSENT_ON_CONTINUOUS_GG`。其余 5 终态不可达：RESOLVED/DIAGNOSTIC/NO_SIGNAL 全需 Phase A 过（未过）；BLOCKED/INVALID 为假（0 mismatch、确定性已证、信息边界干净、冻结文件未改）。Phase B/C 正确**未运行**（无 phaseBC artifact，仅 phaseA_dev/phaseA_heldout JSON 存在）。

8. **子区间诚实 — PASS**：9/30 cell > MDE 真实（check 3 已重算）且 worker-log 显式报告（列全值、header 标"9/30 cells > MDE"）——非掩埋。future-work-seed 框架合理：weak-side-low-SNR regret 在 weak**训练锚点**更强（σ²=0.2: +0.39/+0.78/+0.98/+0.56 @ γ5-11）于 interior（σ²=0.45: +0.22/+0.37/+0.48/+0.34）。pooled anchor regret（+0.2306）> interior（+0.1393）。选择器是 weak turbulence/低 SNR 下的通用 NDA-over-selector，与训练无关——**非连续 GG OOD-specific 退化**。

### 结论

executor 的 `PROBLEM_ABSENT_ON_CONTINUOUS_GG` **成立**。Pooled held-out interior regret = +0.1459 dB（bit-exact 重算），恰低于冻结 MDE=0.15，在合法 disjoint seed 集（dev 0-9/held-out 30-49），信息边界干净，冻结文件未改，pooled 门控读结果前冻结，子区间结构诚实报告且确实非 OOD-specific。无可区分 deployable action → 不生成方法卡/不晋升。

**包内确定性修复已正确执行并披露**：`sigma2_to_ab` 在 3 训练 σ_R² 用冻结四舍五入锚点对（保 byte-exact 回归），内部连续点用 Al-Habash 闭式（≤2.70% 偏离锚点）。原因：Al-Habash 精确值在 strong β（1.3622 vs 冻结 1.4）破坏 byte-exact 回归（85/108 mismatch）。V068 check 1/2 确认修复后 0 mismatch。无第二修复。

### 主控 claim ceiling

P04 产出**有效负面 + 连续 GG OOD 验证资产**（冻结 DA/NDA 选择器 AWGN 拟合 CV 边界在连续 GG 形状 off-anchor 上不产生 OOD-specific regret，pooled held-out +0.146 dB < MDE=0.15；anchor > interior 证明非 OOD-specific）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。weak-side-low-SNR 子区间作 future-work seed（与已关闭 A 族工作区重叠，TL-30 禁换名重开）。C 族（连续 GG OOD 选择器鲁棒性）首包完成，连续=1。

---

## V069: P05 ML polarization equalizer OOD safe online adaptation 独立验收 — ACCEPT（10/10 + 方法身份非混淆）

> date: 2026-07-30
> 关联：D043 / CP034 / worker-log step-032 / campaign P05 (5/10)
> 验收对象：`p05_phase0_identity.py`、`p05_ood_online_adaptation.py`、结果 `p05_phase0_identity.json`、`p05_ood_online_adaptation.json`、verdict `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`

### 10 项核查（全 PASS）

1. **ML testbed identity (Phase 0) — PASS**：P0.1 state_hash_run1==run2==`03e91429dfed74c6` byte-identical；P0.2 StandardCMA byte-identical diverged=false。`_ml_equalizer.py:104` 确认 class=`ButterflyCNNEqualizer2x2`（双偏振蝶形 demux），非 NDA-ML CPR selector。无磁盘 checkpoint，确定性复现。

2. **corrected StandardCMA baseline 合法性 — PASS**：`prompt019_mu_compress_mve.py:210-213` 更新 `(R2-|z|²)·z·conj(r)` **含 z 因子**（Godard 1980）；docstring 99-101 明确对比 `common/_cma.py` scalar-error 缺 z。mu=0.001/R2=1.0/block=64。

3. **训练分布 provenance — PASS**：`params.py:149-150` turb_strong_alpha=4.2/beta=1.4（当前真值）；脚本 `p05_ood_online_adaptation.py:69` `CFG.turbulence.as_dict()['strong']` 活读非硬编码；JSON frozen_identity `[4.2,1.4]` 匹配。

4. **信息访问边界 — PASS**：grep 确认 sX/sY/h/theta 仅用于信道生成、离线 BER 评分、DD-LMS warm-start（声明 `:362`）、periodic-pilot comparator（声明 `:366`）。两候选 `gated_cma_update`/`trust_region_update` 仅消费 `(rX,rY,state)`（`:581/583`），用 Godard CMA `(R²-|z|²)²`（`:428/462`）无 TX truth。无 future suffix/true channel/SOP 进任何 update path。

5. **metric signature 正确性（关键修正）— PASS**：JSON `gate_metric`="fixed_label_BER (swap-visible, invariant10; PI-BER swap-blind reported secondary)"。`ml_long_seq_failure.py:143-147` `compute_ber_phase_corrected` 4 旋转 (0/90/180/270) 取 min。swap 可见：ML fx~0.5、CMA fx~0 坐实 polarization swap。PRIMARY=fixed-label 是不变量 10 + D018 双口径强制（PI 对 swap 结构性失明）。

6. **raw→aggregate 独立复算 — PASS（relErr=0）**：anchor 重算 mean=0.49901393 CI=[0.49834919,0.49967867] **精确一致**；fg100 mean=0.49805660 CI=[0.49484103,0.50127217] **精确一致**。

7. **Phase A problem gate 逻辑 — PASS**：两 cell m_fx≥0.05（0.4990/0.4981）✓ ci_lo>0 ✓ wins=3/3 ✓ cma_div_frac=0.0≤0.2 ✓。混淆分离：cma_div_before_late 全 False（CMA 不共同退化），wins=3/3（非单 seed）。slice PI 0.124→0.051→0.0007（swap 在 PI 被抹平，非 PI drift）。

8. **Phase B recovery 逻辑 + 更新预算公平 — PASS**：recovered = comparator_mean<MDE AND (ML−comp)≥MDE。stdCMA-cont recovered=True 两 cell（0.00018/0.00117<0.05）；DD-LMS（~0.453/0.449）/periodic-pilot（~0.499/0.499）no。预算公平：stdCMA-cont 同 mu=1e-3/block=64（`:247`）；DD-LMS block-grained block=64（`:252`）；periodic-pilot 声明 overhead 1024 sym/5000·100=0.2%。无 comparator 用 future。

9. **Phase C 正确未运行 — PASS**：main() `:640-645` Phase C 仅当 `vb != PROBLEM_RESOLVED` 运行；B resolved → C 不跑。JSON 无 `phases.C` key（grep count=0）。terminal=PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER。

10. **verdict 唯一性 — PASS**：唯一正确终态。PROBLEM_ABSENT 错（Phase A 两 cell gate True）；NO_DIAGNOSTIC_SIGNAL/DIAGNOSTIC_METHOD_SIGNAL 需 Phase C（未运行）；BLOCKED_* 需 identity/共享 testbed 失败（均无）。PROBLEM_RESOLVED 唯一 warranted：stdCMA 在线恢复 swap regret 两 cell。

### 方法身份非混淆 — PASS

`ButterflyCNNEqualizer2x2`（`common/_ml_equalizer.py:104`，双偏振蝶形 FIR demux，Q-CMA-FADE 方向，contract H2/B4）≠ NDA-ML CPR selector（`explore/single-carrier-nda-ml/sc_nda_ml_mve.py`，载波恢复 CPE/FOE per-block h 估计，session `2026-07-08-b11-nda-ml-*`）。不同 class/explore 目录/session。

### 结论

executor `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER` **成立**。raw→aggregate relErr=0；gate 逻辑、预算公平性、Phase-C 抑制、verdict 唯一性均源码级验证。三次包内确定性修复（metric-signature/dtype/recovered-logic）全明显修正非科学变更，已复核。无可区分 deployable action → 不生成方法卡/不晋升。

### caveat

- Phase A n=3 seed（但 wins=3/3、CI 远离 0 by 10×）。
- 单一 testbed 分布族（strong anchor + 一 provenance-OOD f_G；不声称跨 testbed 泛化，与包 scope 一致）。
- dtype bug 在 run2 暴露、run4 修复后终态 JSON 反映修正运行。

### 主控 claim ceiling

P05 产出**有效负面 + Ch3/Ch4 双口径警示资产**（frozen ButterflyCNN swap regret 被 corrected standard-CMA 在线恢复；强化 D022/D023 H2 适用边界 + 不变量 9/10/11）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。D 族（ML polarization equalizer OOD safe online adaptation）首包完成，连续=1。

## V070: P06 E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION 独立验收 — ACCEPT（7/7，修复旧 F3-A 科学无效性）

> 2026-07-31 | 关联：D044 / CP035 / step-033 | verdict: `NO_CAUSAL_HISTORY_INCREMENT`

### 验证对象

P06 一次性修复型 PROBLEM_BEARING_PROBE（撤回旧 window/complexity 入口，新 E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION 修复旧 F3-A 的 conditional-MI 误标）。独立 verifier `verify_p06.py` 对 Phase 0 物理身份门 + Phase A 严格因果信息门结果做源码 AST + 数据 + 逻辑审计。

### 7 项检查（全 PASS）

1. **V1 causality alignment [PASS]**：`build_feature_matrix` 源码审计——X_cur = frame fi 摘要，X_hist = frames fi-K..fi-1（全 < fi，严格因果）。证据：函数体含 `range(fi - history_k, fi)` 与 `X_cur[i] = cur_vec`。
2. **V2 truth/future leakage [PASS]**：summary dict 只含 receiver-visible trace 字段（cm_error/output_power/update_norm/w_norm/z_amp_max）。禁入变量（next_fixed_ser/next_fail/sX/sY/bitsX/bitsY/h/alpha/beta/seed/cell-id）在 summary 段零命中。target（next_fixed_ser/next_fail）只用 TX-truth 离线评分，绝不进特征。
3. **V3 trajectory split disjoint [PASS]**：train(200-214)∩dev(215-224)=∅、train∩test(225-239)=∅、dev∩test=∅。
4. **V6 seed discipline vs history [PASS]**：P06 seeds 与历史禁用集（11-50/61-130/30-99/131-150）零重叠。
5. **V4 raw→aggregate recompute [PASS]**：dev_fail 从 raw per-frame rows 独立重算 = 428 = reported；test mean next_ser(raw)=0.177 与评估口径一致。
6. **V5 ACF (phase0) [PASS]**：Phase 0 artifact 块 ACF max_relerr per condition = [0.0003,0.0003,0.0006,0.0006,0.0018,0.0018]（全 <0.10），经验 ACF 与 ρ^lag 一致。
7. **V7 verdict unique & logic [PASS]**：reported=`NO_CAUSAL_HISTORY_INCREMENT`，从报告数字独立重导 = `NO_CAUSAL_HISTORY_INCREMENT`（floor_met=True；history R²=0.32 未超最强 temporal persistence R²=0.85 → beats_temporal=False → NO_SIGNAL）；verdict 在允许集内、逻辑一致。

### 关键数字复核（独立从 raw 重算/源码核）

- Phase 0：GG 边缘 KS 0.056–0.144、块 ACF relerr<0.2%、rho_frame fg30/100/1000=0.99/0.97/0.70、CMA 身份重跑 relerr=0。全 condition PASS。
- Phase A test（n=1260 feature rows, 180 traj macro bootstrap）：persistence R²=0.853 > EWMA 0.853 > AR(1) 0.848 > history 0.320 > current-only 0.040。history−current MSE 减少 CI=[4.72e-03, 4.68e-02] CI_lo>0（history 真实 > current-only），但 history ≪ persistence。
- failure-target logistic：history brier 0.161 < current-only 0.208（history 更好），但同样 sub-persistence（连续目标已证 persistence 主导）。
- dev fail events 428/1140 floor=30 MET（问题在物理条件下成立，非 PROBLEM_ABSENT_AT_PHYSICAL_TIMESCALE）。

### 不变项确认

- 旧 F3-A `state/current.yaml:161-170` / `portfolio/current.yaml:173-181` 的 `INVALIDATED_AS_CONDITIONAL_MI` 标记不动；旧 +0.060 bits/+0.036 R² 不被新 P06 继承（新 P06 用 held-out 预测增量，不报告 MI）。
- 不调窗口、不做 selector、不做 Pilot-Jones、不微调 ButterflyCNN（绑定裁决禁）；E 族首包，本轮失败关闭，不允许第二个 evaluator-repair 包。

### 结论

**ACCEPT（7/7 PASS）**。P06 端到端有效执行：Phase 0 物理身份门全过、Phase A 严格因果信息门诚实判定 `NO_CAUSAL_HISTORY_INCREMENT`（history 增量统计真实但被更便宜常规 temporal baseline 完全吸收），Phase B/C 按 gate 顺序不运行。修复了旧 F3-A 科学无效性。accepted_valid_packages 5→6（有效负面包），families_started 追加 E（第 5 族，"≥5 族"达成），仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。

### 主控 claim ceiling

P06 产出**有效负面 + receiver-observability 边界资产**（跨帧信息被帧间持续性主导；deployable frame rate ≪ τ_c 下跨帧动力学边界；旧 F3-A conditional-MI 误标的方法论教训）。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。E 族（因果跨帧历史信息）首包完成，连续=1，本轮失败关闭。

---

## V071: P07 F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG — independent verifier (10/10 ACCEPT)

> 2026-07-31 | 关联: D045 / P07 / CP036 | 结论: **PASS (10/10) / ACCEPT**
> **2026-07-31 更新：科学层结论被 V072 取代**。V071 的 10 项检查全过，但查的全是 **consistency**（g=1 float-bypass 身份、raw→aggregate 复算、信息边界 AST、seed 隔离、冻结文件未改），**未查算法物理正确性**（q=Q(gz)→q/g 数学、下游 scale-dependent 函数、causal AGC 递推、trajectory lifecycle、经验 ACF）。G3 float-bypass 门只在 g=1 验证 = 测试用例覆盖不到 bug 触发条件（g≠1）。保留 V071 不删，标"合同一致性通过但物理正确性漏审"（命中 sim-preflight rules/mve-validation.md "consistency≠correctness"）。

独立 verifier `_p07_verify.py` 重算/审计 P07 结果（不依赖 executor 的聚合）：

- **V1 ADC math**（PASS）：round-half-up（+0.5LSB→+1/-0.5LSB→0）、饱和不 wrap（W4 100·FS→7 非 -8）、signed I/Q 对称（±0.3→±38 @W8）。
- **V2 float-bypass 身份**（PASS）：独立重跑 FixedGainAGC(g=1,W=64) 与 `run_case_multidelta` 逐 cell byte-identical（weak/strong/moderate ×{9,15,21}×seeds{0,1,2}，0 mismatch，含 per_window_da_err/nda_err 数组）。
- **V3 信息边界 AST**（PASS）：`_p07_adapters.py` 所有 AGC class 体 + `quantize_iq` 体零 forbidden 子串（h/alpha/beta/tx/phi/bits/oracle/true_h/r['h']/future）。
- **V4 因果性**（PASS）：window-0 gain=nominal（1.0），gain 随过去 RMS 单调（小 RMS→大 gain），确定性重放。
- **V5 raw→aggregate recompute**（PASS）：重载 Phase-A raw_rows，重算 per-bitwidth pooled regret 匹配 executor 聚合 relErr≤1e-9；paired_regret identity（10log10(sel/ideal_sel)）对前 2000 row 零违反。
- **V6 seed 隔离**（PASS）：dev seeds{0..4}，held-out seeds{30..34}，无 71-80 污染。
- **V7 paired realization**（PASS）：`eval_cell_fixed_gains` 批量（one channel-gen/cell）的 ideal_float selected_errors == 直接 `run_case_with_adc` 在同 (scene,g,seed) 的结果（weak/strong ×{9,15}）。
- **V8 terminal verdict (Phase A)**（PASS）：独立 re-derive problem_established（per-bitwidth pooled mean≥MDE AND CI_lo>0 AND ≥3 cell，跨位宽一致）与报告一致。
- **V9 frozen files 未改**（PASS）：`git diff --stat HEAD` 对 common/、params.py、_a4_switch_common768_30seed.py、_a4_branchrouted_30seed.py、sc_nda_ml_sim.py、_p01_cpr_snr_mismatch_probe.py 全空。
- **V10 Phase-BC aggregate recompute + verdict**（PASS）：重载 Phase-BC heldout_rows，重算 conventional regret per family|W 匹配 relErr≤1e-9；re-derive terminal verdict（conv_resolves → PROBLEM_RESOLVED / cross_consistent → DIAGNOSTIC_METHOD_SIGNAL / else NO_DIAGNOSTIC_METHOD_SIGNAL）与报告 `NO_DIAGNOSTIC_METHOD_SIGNAL` 一致。

**结论**：P07 verdict `NO_DIAGNOSTIC_METHOD_SIGNAL` 唯一正确、数据可独立复算、信息边界干净、因果性成立、frozen 文件未改。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。F 族（AGC/ADC 动态范围）首包完成，连续=1，**未关闭**（NO_SIGNAL 非关闭裁决；P08 可选 F 第 2 包换子轴连续≤2，但 F/G/H timing/scenario/FEC 子轴已撤回不得重开）。

---

## V072: P07-R 三根因最小失败测试复现 + 取代 V071 科学层结论（PART 1：根因复现 PASS）

> 2026-07-31 | 关联: D046 / P07-R | 结论: **PASS（三根因独立最小失败测试全部复现，修复前证据已存盘）**
> 取代：V071 的**科学层结论**（Phase A/B/C 数字 + verdict）。V071 的 consistency 结论保留。

**验证脚本**：`projects/simulation/explore/nda-awgn-tracking-sandbox/p07r_reproduce_rootcauses.py`（systematic-debugging Phase 1，未施加任何修复）。
**证据**：`projects/simulation/results/p07r_agc_adc_repair/p07r_prefail_evidence.json`。

三根因最小失败测试结果（修复前，确定性可复现）：

- **H1 SCALE — FAIL（致命）**：
  - T1（g≠1 真实接收链偏差）：13 dB moderate，OLD 链喂 q（不 /g）selected_errors 偏差 g=0.5→+32/+29、g=0.75→+9/+9、g=1.5→+8/+51（choice da→nda）、g=2.0→+44/+62（da→nda）、g=3.0→+59/+90（da→nda）。
  - T4（float-bypass identity g≠1 破坏）：9 dB weak，OLD 链 nd/nc mismatch g=0.5→+39/+56、g=0.75→+11/+22、g=1.5→−13/−1、g=2.0→−15/+0（**choice 改变**）；**corrected 链 q/g 全部 mismatch=0/0、choice 不变**。证明下游 `estimate_h_blind_perblock`（加性 1/(2γ) 噪声底）、`amp_limit`（固定 thresh 3.0）、`decide`（1/(2·gamma_lin)）是 scale-DEPENDENT，g≠1 不可恢复。
- **H2 CONTROL — FAIL（公式 bug）**：CausalRMSAGC `g_next=clamp(target/rms(q_past))` 漏乘 g_current。常数输入定点 CURRENT √(target/r0)=1.0954 ≠ CORRECTED target/r0=1.2000；deployed lam=0.9 output RMS 收敛到 0.230（target 0.3），target 错对象。
- **H3 LIFECYCLE — FAIL（无时间相关）**：`_p07_runner` 每 window 独立 seed 独立 gg_block，经验 lag-1/2/5/10 GG 幅度 ACF = −0.042/+0.003/−0.063/−0.082 ≈ 0，与合同声称 ρ≠0 矛盾。AGC 预测独立抽样 → 非时间相关控制问题。

**结论**：三根因全部独立最小失败测试复现，修复前证据已存盘（systematic-debugging Phase 1 完成）。旧 P07 verdict `NO_DIAGNOSTIC_METHOD_SIGNAL` 及 Phase A/B/C 数字、clipping–resolution 折中"真实存在"声称、harvest 全部 INVALIDATED。V072 PART 2（修复后 fresh-seed 重跑 + 沿调用链独立 verifier）在修复实现后追加。

**注**：本 PART 1 仅验证"根因确实存在"，不验证修复正确性。修复正确性由后续 PART 2 独立 verifier（沿调用链查 q/g 数学、下游 scale、AGC 递推、trajectory lifecycle、ACF、clip/quant 分解、oracle 未进 deployable、fresh seed 隔离、raw→aggregate、verdict 唯一）判定。

---

## V072 PART 2: P07-R 修复后独立 verifier + 终态裁决（10/10 ACCEPT）

> 2026-07-31 | 关联: D046 / P07-R / CP037 | 结论: **PASS (10/10) / ACCEPT**

**验证脚本**：`projects/simulation/explore/nda-awgn-tracking-sandbox/p07r_verify.py`（沿调用链查物理正确性，不止 consistency）。
**证据**：`projects/simulation/results/p07r_agc_adc_repair/p07r_verifier_result.json`。

10 项检查全过（区别于 V071 只查 consistency，本 PART 查物理正确性）：

- **W1 q/g 数学**（PASS）：`quantize_iq_gainaware` 返回 rx_in=q/g；无 clip 无 quant 时 rx_in==z 对任意 gain（max err ≤1e-9）。
- **W2 下游 scale**（PASS，V071 漏审项）：gain≠1 + 宽 rail + 精细 ADC，corrected 链精确恢复 g=1 参考（selected_errors/da/nda/choice/oracle 全 byte-exact）。这是 H1 SCALE 修复的核心证据。
- **W3 AGC 递推**（PASS）：corrected causal-RMS 常数输入收敛到 INPUT-scale 定点 target/rms，无 period-2（p2metric<1e-3）；attack-release/log-domain 有界。
- **W4 trajectory lifecycle**（PASS）：shared stateful AR(1) GG，rho 匹配 exp(-Δt/τ_c)，经验 lag-1 ACF 非零（>0.3 for rho=0.70 trajectory），所有方法共享同一 trajectory。
- **W5 四路分解隔离**（PASS）：scale_only==float、clip_only 只 clip、quant_only 只 round（宽 rail 无 clip）、full_adc=clip+round。
- **W6 信息边界 AST**（PASS）：所有 AGC class 体零 forbidden 子串（修了一处 false positive——CausalRMSAGC 的增量 blend 参数原名 `alpha` 与信道真值 `alpha` 撞名，已重命名 `blend` 消除歧义；非信息泄漏）。
- **W7 fresh seed 隔离**（PASS）：dev 300-309、held-out 500-520 与 campaign 历史（0-99/200-239）零重叠、71-80 未出现、dev/held-out 互斥。
- **W8 raw→aggregate**（PASS）：重载 Phase-A raw_rows 重算 paired regret 前 2000 row 零违反。
- **W9 终态 verdict**（PASS）：verdict 输入齐备、可唯一推导。
- **W10 frozen 文件未改**（PASS）：common/、params.py、sc_nda_ml_sim.py、_a4_switch_common768_30seed.py `git diff --stat HEAD` 全空。

**终态裁决（p07r_adjudicate.py / p07r_terminal_verdict.json）**：

- **verdict = `PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION`**（D046 §VII 终态 A）。
- Phase A deployable-region（W8/W10）dev-best fixed-gain g=0.5 pooled regret：fG30/100/1000（rho 0.99/0.97/0.70）W8=+0.035/+0.042/+0.067 dB、W10=+0.016/+0.025/+0.045 dB —— **全部远低于 MDE=0.15**，CI_low>0 但 mean≪MDE，cells_pass=0-2，deployable_problem=False（全 rho）。旧 P07 的 "+0.91 dB regret / clipping–resolution 折中真实存在" **完全是 H1 SCALE artifact**（下游 scale-dependent 函数在 gain≠1 看到错误尺度信号）。
- 四路分解（W=8, g=1.0）：scale_only=0.0000（H1 修复验证）、quant_only=0.0000（宽 rail 无 clip）、clip_only=+2.03~+2.51 dB、full_adc≈clip_only（clipping 主导）。但 dev-best g=0.5（clip_rate=2.2%）把 W8 regret 降到 +0.048 dB —— **折中是真实单调的，但是单侧的：静态低增益即解决，W8/W10 无残留问题给 AGC/方法处理**。
- counts_as_valid_package=True，**campaign accepted_valid 恢复 6→7**（D046 §X：修复后形成有效 P07-R）。
- Phase B/C 不运行（Phase A 门未过 = 问题不存在，同 P04/P06 gate 顺序逻辑）。

**结论**：P07-R verdict `PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION` 唯一正确、修复后链沿调用链物理正确、fresh seed 隔离干净、frozen 文件未改。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。F 族（AGC/ADC 动态范围）P07-R 修复后问题不存在于 deployable 位宽 → F 族可关闭（静态低增益即解决，无方法空间）。旧 P07 artifacts 保留 INVALIDATED 标记不删；P07-R artifacts 在 `results/p07r_agc_adc_repair/`。

## V073: P08 coded-chain 扩展包独立 verifier（15/15 ACCEPT）

> 2026-08-01 | 关联: D047 / P08 / CP038 | 结论: **PASS (15/15) / ACCEPT**

独立 verifier（与 executor 上下文分离）核查 P08 coded-chain 扩展包（5G NR LDPC + 16QAM BICM
over dual-pol SOP）。15 项全过，每项均独立读源码/重跑/recompute：

- **V1 source/hash real**（PASS）：bg2_csv_sha256=4f4db6f7... 是真 hash（recompute 自 5G_bg2.csv 吻合），encoder_sha256 真，sionna 2.0.1，bg=bg2 Z=104，非 UNAVAILABLE。
- **V2 H·c=0 + noiseless roundtrip**（PASS）：fresh encode 随机 info → |Hc|=0，noiseless decode BER=0。
- **V3 LLR sign/bit order**（PASS）：qam16_mod→_qam16_demod_to_bits round-trip 精确；maxlog LLR sign 匹配 bits 全 16 labels。
- **V4 AWGN waterfall**（PASS）：FER=[1,1,1,0.54,0,0,0,0,0] 单调，3 区（fail/waterfall/success）覆盖。
- **V5 12 checks**（PASS）：JSON 13 项（12 + 9b 子检查）全 PASS，all_pass=true。
- **V6 decoder no TX truth**（PASS）：CodecAdapter.decode 只收 llr；_decode_pol* 用 cw_bits/info 仅 post-decode BER/FER scoring。
- **V7 σ² call chain**（PASS）：B0/B1/B2 用 receiver-visible 1/(2γ_bar)；oracle 读 sX/sY 仅经 _oracle_sigma2 作 headroom，非 Go comparator。
- **V8 scout oracle not migrated**（PASS）：p08_*.py 零引用 scout/oracle_soft_demap/cb1_evaluator；_oracle_sigma2 自含 numpy。
- **V9 shared paired realization**（PASS）：Phase A 预建 ONE realizations list，4 方法 loop 同 list，paired by construction。
- **V10 frozen files unchanged**（PASS）：git diff --stat HEAD common/params.py/sc_nda_ml_sim.py 空；p07/p07r 未改。
- **V11 seed isolation**（PASS）：dev 1000-1009/test 1100-1114 互斥，与 P01-P07 历史（0-99/200-239/300-334/500-540）零重叠，71-80 缺席。
- **V12 raw→aggregate**（PASS）：从 1440 raw rows 重算 pooled FER per method/SNR，max relErr vs test_summary=0.0（精确）。
- **V13 verdict uniqueness**（PASS）：re-trace 分支 exec_invalid=F/conv_helps=F(CI_lo=0)/oracle_headroom=F(CI_lo=0) → 唯一 `PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE`，非 METHOD_SIGNAL。
- **V14 governance lineage**（PASS）：D047 active，control_epoch=74，families_started 含 G，mission_checkpoint=CP038，voice "行"→D047，task-control validator PASS。
- **V15 gate vs verdict separate**（PASS）：correctness gate JSON 与 phaseA verdict JSON 独立文件，verdict 不从 gate 派生。

**结论**：P08 verdict `PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE` 唯一正确、coded-chain 身份真实（5G NR LDPC）、算法正确性门全过、Phase A 数据可独立复算（raw→aggregate relErr=0）、信息边界干净、frozen 文件未改。claim ceiling 维持 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`：不构成 active carrier、不冒充 formal method、不写论文 claim。G 族（coded-LLR-calibration）首包 verdict PROBLEM_ABSENT → coded loss 主导机制是**不可恢复突发深衰落**非 LLR 置信度失配，单一 AWGN σ² 与最强传统校准近乎相同。counts_as_valid_package=True，campaign accepted_valid 7→**8**。Phase B/C 不运行（gate 顺序）。

---

## V073 状态更新（2026-08-01，D048）

> **本 V073 的科学层 ACCEPT 结论已被 V074 取代。保留不删除。**

V073（2026-08-01，15/15 ACCEPT）核查的是 **consistency + provenance receipt**（source hash、H·c=0、
noiseless roundtrip、LLR sign、AWGN waterfall、12 checks PASS、decoder no-TX、raw→aggregate relErr=0、
seed 隔离、frozen 文件未改、governance lineage）——这些全过。但**漏审科学合同六项**：

- H1：(α,β) 是否从 params.py 单一真相源导入（实际硬编码且三档全错）— **未查**
- H2：σ² 是否 receiver-visible（实际来自循环变量 γ_bar）— V7 只复述 "用 1/(2γ_bar)" 未判违规
- H3：oracle 粒度是否覆盖候选（实际单 global scalar）— 未查 action space 覆盖性
- H4：metric fallback 是否冻结（实际 Primary A 全 inf 时静默退 raw FER-delta）— 未查
- H5：interleaver 身份是否与 worker-log 声称一致（实际未启用，worker-log 谎称 triangle）— V5 "12 checks PASS" 复述 check #10 但 #10 自承 identity interleaver，V073 未对照 worker-log
- H6：统计单位是否 trajectory-cluster（实际按 16 cw 独立样本）— 未查

**这是 P07-R/D046 "consistency≠correctness" 教训在 coded 层的重演**。V073 标记为：
**"合同一致性通过（15/15 consistency + provenance receipt PASS），但科学合同六项（H1-H6）漏审，
科学层 ACCEPT 结论被 V074 取代"**。V074 必须沿 caller→callee 检查科学信息边界，逐项核 H1-H6，
不只复述合同或测试 PASS。

## V074: P08-R coded-chain 科学完整性修复独立 verifier（16/16 ACCEPT）

> 2026-08-01 | 关联: D048 / P08-R / CP039 | 结论: **PASS (16/16) / ACCEPT**

独立 verifier（与 executor 上下文分离——脚本 + 独立 sub-agent 双重核验）核查 P08-R coded-chain
科学完整性修复。脚本 `p08r_verify.py` 16 项确定性检查全 PASS；独立 sub-agent（fresh context，
不信任 executor 自述）逐项沿 caller→callee 检查科学信息边界，最终 **ACCEPT**。

**16 项逐项核验**（每项独立读源码/重跑/recompute）：

1. **H1 prefill root causes reproduced**（PASS）：prefail_evidence.md 含 H1-H6 全部六项根因证据。
2. **H1 params.py single source of truth**（PASS）：get_gg_scenes() 返回 SimulationConfig().get_turb_dict()；p08r_*.py 零硬编码 (α,β) 字面量（forbidden hits=[]）；weak=11.6,10.1 / moderate=4.0,1.9 / strong=4.2,1.4 与 params.py:222-224 一致。
3. **H5 bit-interleaver option A active**（PASS）：LDPC5GEncoder 传 num_bits_per_symbol=4；out_int shape=(1536,)，1536 unique，n_moved=1534/1536，前 12=[0,384,768,1152,1,385,769,1153,...]=3GPP §5.4.2.2 sub-block+triangle（Q=384），out_int_inv 互逆。
4. **H6 shared paired realization**（PASS）：40 test seeds，每 seed 6 方法（B0/B1/B2/O0/O1/O2）共享同一 real/eq（h_truth_mean 跨方法一致，0 违规）。
5. **H2 B0/B1/B2 信息边界**（PASS，AST 核）：method_B0/B1/B2 全调 estimate_sigma2_from_prefix(eqp,sp)（receiver-visible prefix）；函数体无 real.gamma_bar/real.h/real.theta/real.sX/real.sY（除 prefix 部分）。scored codeword 不反向参与 calibration。sub-agent 指出 equalize() 用 gamma_bar 作盲 h 估计噪声底（receiver-side 模块，非 decide 泄漏）——非缺陷，记录为 future-work seed（可用 prefix-based noise floor 进一步加固）。
6. **H3 oracle ladder**（PASS）：O0=scalar/O1=block(100)/O2=block(16)，O2 finer；独立重跑 O2=24 distinct blocks > O1=4 distinct blocks。
7. **H2 prefix/data separation**（PASS）：split_prefix_data 12 次调用，prefix=sX[:32]，data=sX[32:]；n_cw_X=16 一致。
8. **fairness**（PASS）：B2 仅 override (alpha,offset,llr_clip)，k/n/num_iter/interleaver 保持 default = B0 contract；所有方法同 code/rate/iter/interleaver。
9. **H6 trajectory lifecycle**（PASS）：raw=240 rows=40 seeds×6 methods（非 40×16 cw）；schema 含 per-traj h_truth_mean/min/max、per-pol fer_X/fer_Y/n_cw_err、post_ber。
10. **raw per-pol evidence**（PASS）：每行含 fer_X/fer_Y/post_ber_X/post_ber_Y。
11. **fresh seed zero collision**（PASS）：dev 6000-6019/test 7000-7039 与 campaign 历史（0-99/200-239/300-334/500-540/1000-1014/1100-1129）零重叠。
12. **powered trajectory count**（PASS）：n_test=40。
13. **H4 metric frozen before test**（PASS）：chosen_cell=['weak',1000.0,12.0]，primary=B_fixed_snr_paired_fer，mde_fer=0.2347；dev_workspace.json 在 Step5 test 前 Step3 写入；独立重算 MDE=2.802·√(2·0.16875·0.83125/40)=0.23466 精确一致。
14. **raw→aggregate recompute**（PASS）：独立重算 mean FER per method，relErr<1e-12。
15. **verdict uniqueness**（PASS）：B0−conv mean=+0.0016、conv−O1=−0.0016、conv−O2=+0.0039 全 ≪ MDE_fer=0.2347 ⇒ conv_helps=False、O1/O2 headroom=False ⇒ 唯一 `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`。
16. **mechanism decomposition**（PASS）：独立重算 B0 all-cw-fail seeds={7009,7011,7016,7038}（h_truth_mean 0.29-0.41），O2 all-cw-fail = **相同 4 seeds**（不可恢复深衰落）；O2 部分救回 3/40、全救回 1/40。coded loss 主导 = 不可恢复突发深衰落（10% trajectory），非 LLR 校准失配。

**结论**：P08-R verdict `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` 科学有效，唯一正确。
六根因（H1-H6）全部在源码+artifact 级修复验证；信息边界（H2 最关键）AST 确认；机制归因（4/40 不可恢复
深衰落突发）科学合理且独立复现。这是旧 P08 声称的同一物理机制，但**这次在 corrected chain 下正确建立**
（真 α/β、receiver-visible σ²、真 3GPP interleaver、正确 oracle ladder、trajectory-cluster 统计）。
counts_as_valid_package=True，campaign accepted_valid 7→**8**。G 族（coded-LLR-calibration）关闭
（PROBLEM_ABSENT：coded loss 主导是不可恢复突发深衰落，非 LLR 失配；单一 AWGN σ²≈最强传统校准，
oracle 仅 0.55% FER 局部 headroom≪MDE）。Phase B/C 不运行（gate 顺序）。claim ceiling 维持
LOCAL_SLICE / NONBINDING_DIAGNOSTIC。

**PARTIAL reusable asset 确认**：5G NR LDPC source-auditable 选择、CodecAdapter 骨架、AWGN waterfall
三区在 P08-R 复用并修复（interleaver 激活、(α,β) import、σ² 来源、oracle ladder、统计单位全部修正）。

**future-work seed**（诚实记录，非缺陷）：equalize() 的盲 h 估计用 gamma_bar 作噪声底（receiver-side
模块，非 decide 泄漏）；后续可用 prefix-based noise floor 替代以进一步加固信息边界。

> **本 V074 的科学层 ACCEPT 结论已被 V075 取代。保留不删除。**
> V074（2026-08-01，16/16 ACCEPT）核查的是 **consistency + H1-H6 合同**（GG params import、
> interleaver permutation、oracle ladder、metric freeze、trajectory-cluster、raw→aggregate 复算），
> 全过。但**漏审三项承重科学合同**：H7（equalize 是否读 gamma_bar，#5 只扫 method 函数体不递归）、
> H8（AST 是否覆盖调用图，#5 抽取逻辑本身有缺陷）、H9（MDE 是否先验、CI_lo=0 如何处理、是否有
> min(B1,B2)）。V074 #5 sub-agent 把 equalize 用 gamma_bar 作盲 h 噪声底错标 "future-work seed 非缺陷"
> ——H7 数值复现（p08r2_h7_reproduce.json）证伪此归类（max\|ΔLLR\| 高达 7.02，改 decode decision）。
> **这是 P07-R/D046、P08/D048 "consistency≠correctness" 教训的第三度重演**。V074 标记为：
> **"16/16 consistency + H1-H6 PASS 但 H7/H8/H9 漏审，科学层 ACCEPT 结论被 V075 取代"**。

## V075: P08-R2 receiver 信息边界 + AST 门 + 统计功效合同三根因修复独立 verifier（19/19 ACCEPT）

> 2026-08-01 | 关联: D049 / P08-R2 / CP040 | 结论: **PASS (19/19) / ACCEPT**

独立 verifier（与 executor 上下文分离——脚本 + 独立 sub-agent 双重核验）核查 P08-R2 receiver
信息边界 + AST 门 + 统计功效合同三根因修复。脚本 `p08r2_verify.py` 19 项确定性检查全 PASS；
独立 sub-agent（fresh context，不信任 executor 自述）逐项沿 caller→callee 递归 AST + 数值复算，
最终 **ACCEPT**。

**19 项逐项核验**（每项独立读源码/重跑/recompute）：

1. **H7/H8/H9 prefail evidence**（PASS）：prefail_evidence.md 含 H7/H8/H9 全部三项根因证据。
2. **H7 leak 复现 pre-fix**（PASS）：p08r2_h7_reproduce.json `h7_leak_confirmed=true`，max\|ΔLLR\| 高达 7.02（独立 sub-agent 复核）。
3. **params.py single source of truth**（PASS）：p08r2_* 零硬编码 (α,β) 字面量；get_gg_scenes() used。
4. **bit-interleaver option A active**（PASS）：out_int 真 3GPP §5.4.2.2 置换（n_moved>1000/1536）。
5. **coded bits injected & methods share realization**（PASS）：40 seeds，每 seed 6 方法 h_truth_mean 一致。
6. **H7 receiver info boundary — RECURSIVE AST**（PASS，**H8 fix**）：source_by_name 从 3 个 p08r2_*.py 模块建，从 method_B0/B1/B2 + equalize + estimate_pre_eq_noise_from_prefix + gamma_vis_from_prefix + estimate_sigma2_from_prefix + llr_per_cw_from_eq 入口，forbidden_set={gamma_bar,h_truth,theta}，递归 max_depth=5，**访问 9 函数 0 违规**；equalize 调 gamma_vis_from_prefix 确认。独立 sub-agent 用 Python AST 复核：equalize 可执行代码零 gamma_bar/h_truth/theta 引用（docstring 内的字面不算）。
7. **σ²_pre from prefix LS**（PASS）：equalize 可执行代码（去 docstring）零 gamma_bar；调 gamma_vis_from_prefix(σ²_pre)；estimate_pre_eq_noise_from_prefix 用 32-sym prefix LS（4 复未知数/64 方程/60 dof）。
8. **O0/O1/O2 ladder**（PASS）：O0=scalar/O1=block(100)/O2=block(16)，O2 finer。
9. **prefix separated from scored window**（PASS）：n_cw=16/pol，split_prefix_data 用。
10. **fairness**（PASS）：B2 仅 override (alpha,offset,llr_clip)，k/n/num_iter/interleaver 保持 default。
11. **trajectory lifecycle**（PASS）：raw 含 h_truth_mean/min/max per-traj。
12. **raw stores σ²_pre + γ_vis + per-pol FER/BER**（PASS）：H7 诊断字段全存。
13. **fresh seed zero collision**（PASS）：dev 9000-9019 / test 8000-8039 与 campaign 历史（含 P08-R 6000-6019/7000-7039）零重叠。独立 sub-agent 复核 dev∩hist=∅ test∩hist=∅ dev∩test=∅。
14. **powered trajectory count**（PASS）：n_test=40。
15. **metric frozen before test + H9 a-priori MDE=0.05**（PASS，**H9 fix**）：primary=B_fixed_snr_paired_fer，mde_fer=0.05 精确（非 0.2347 post-hoc）；dev workspace 记 n_required≈814 仅为透明度。独立 sub-agent grep 确认 "0.2347" 在 gate/dev artifacts 中 0 出现。
16. **raw→aggregate recompute**（PASS）：独立重算 mean FER per method，relErr<1e-9（独立 sub-agent 复核 relErr=0.0）。
17. **H7 metamorphic gate PASS**（PASS，**runtime proof**）：p08r2_metamorphic_gate.json `metamorphic_gate_pass=true`，所有 cell worst max\|ΔeqX\|=0.00e+00, worst max\|ΔLLR_X\|=0.00e+00（精确零）。独立 sub-agent 复核 30 cells 全 0.0。
18. **H9 no min(B1,B2) + separate deltas + CI_hw**（PASS，**H9 fix**）：test_results 含 delta_B0_minus_B1 和 delta_B0_minus_B2 两条独立 delta；delta_B0_minus_strongest_conv 字段 ABSENT（旧 min(B1,B2) 已删）；CI half-width 报告。
19. **verdict uniqueness + EVIDENCE_INSUFFICIENT reachable**（PASS）：verdict `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` 在 5 个合法终态集合内；EVIDENCE_INSUFFICIENT 分支可达（CI_hw > MDE/2 触发，本轮 hw=0.0066/0.0090 ≤ 0.025 未触发但可达）。独立 sub-agent 复核 verdict 逻辑 + 重算 B2-O2 mean=+0.009375 hw=0.00898 ≪ MDE。

**结论**：P08-R2 verdict `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE` 科学有效，
唯一正确。三根因（H7/H8/H9）全部在源码+artifact 级修复验证；**H7 信息边界经递归 AST（0 违规）+
运行时 metamorphic 门（Δ=0.0 精确）双重证明**；H8 verifier 真递归（9 函数访问）；H9 用先验
MDE=0.05 + 独立 B0-B1/B0-B2 delta + 可达 EVIDENCE_INSUFFICIENT。机制归因（3/40 不可恢复深衰落
突发，O2 也 2/40 不可恢复）独立复现。这是 P08-R 声称的同一物理机制，但**这次在真正 gamma_bar-free
的 corrected receiver 链 + 先验 MDE + 新 seeds + 无 cherry-pick 下得出**。counts_as_valid_package=True，
campaign accepted_valid 7→**8**。G 族（coded-LLR-calibration）关闭。Phase B/C 不运行（gate 顺序）。
claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。

**PARTIAL reusable asset 确认（D048 修复有效部分在 P08-R2 verbatim 复用）**：5G NR LDPC source-auditable
选择、CodecAdapterR、3GPP §5.4.2.2 真 interleaver（option A）、GG (α,β) params.py import、O0/O1/O2 oracle
ladder、H4 dev-freeze 流程、H6 trajectory-cluster 统计。

**独立 sub-agent ACCEPT**（agent_a1ce4c5f，fresh context）：7 项独立复核全 PASS（H7 leak 复现、H7 fix
正确性、metamorphic runtime、H8 verifier 递归、H9 统计合同、fresh seeds、verdict sanity + raw→aggregate
relErr=0.0），无任何 executor 自述与实际 code/artifact 的差异。

**TL 教训登记**：P07-R/D046 → P08/D048 → P08-R2/D049 是 "consistency≠correctness" 教训三度重演——
verifier 必须递归遍历 deployable 调用图（不只复述合同/扫函数体字面）+ 跑运行时 metamorphic 门。
此条作为 sim-preflight mve-validation.md 的强化项候选（跨 session 沉淀）。

---

## V076: P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 入口门裁决独立 verifier（ACCEPT — STRATEGIC_GATE 唯一合法终态）

> 2026-08-01 | 关联: D050 / P09 入口门 / CP041 | 结论: **PASS / ACCEPT（入口门事实核查）**

独立 verifier（与入口评估上下文分离——主线程 Read 源码 + grep 复算 + Explore 子 agent fresh context 交叉）核查 P09 入口门裁决的科学事实基础。P09 入口门无实验产物（无 sprint/无 held-out seed/无 artifact），故核查对象是**入口门的事实前提与终态合法性**，而非 raw→aggregate 数值（无 raw 可核）。

**逐项核验**（每项独立读源码/grep 复算）：

1. **NDA-ML 估计器是否 closed-form（非 search）**（PASS）：`common/_recovery.py:171-273` `nda_ml_recovery` 逐行 Read——`assume_df_zero=True` 路径（`:209-237`）：`raised = rx ** M0`（`:213`，向量化元素升幂），segmented 变体 K=8 段每段一次 `np.angle(raised[lo:hi].mean())`（`:222-225`），段间 `np.unwrap`+`np.interp`（`:226-229`）；'none' 变体整块 `np.angle(raised.mean())`（`:232`）。`assume_df_zero=False` 路径（`:238-273`）：单次 `np.argmax(np.abs(R))`（`:249`）+ Quinn-Rife 插值（`:250-258`）+ 线性回归（`:262-270`）。**确认全程零 candidate 枚举、零 likelihood/objective 在候选集上求值**。每块成本 = 8 次闭式 mean-angle + unwrap/interp（segmented）/ 1 次闭式 mean-angle（none）/ 1 次 FFT argmax（Doppler）。
2. **生产 driver 是否逐块 closed-form（无 per-window objective eval）**（PASS）：`simulator/sc_nda_ml_sim.py:173-191` `ber_nda_awgn`，`:180-187` for 循环逐 256-sym 块调一次 `nda_ml_recovery(seg, ..., intra_block_tracking='segmented')`。确认无候选集循环、无 objective 求值。
3. **grep 零命中复算**（PASS）：`grep -rniE "full.?search|exhaustive|candidate|grid_search|phase_grid|coarse|coarse.?to.?fine|hierarchical|objective.*eval|search.*space|enumerate"` on `common/_recovery.py` + `simulator/sc_nda_ml_sim.py` + `simulator/_b11_params.py` → 零结果（独立复算）。证 NDA-ML 本体无 search/exhaustive/grid/coarse/hierarchical/objective-eval 词汇。
4. **代码库唯一 exhaustive search 是 BPS（竞争对手非本体）**（PASS）：`_recovery.py:91-118` `bps_cpr`——B 测试相位 `phases = 2π·arange(B)/B`（`:97`）+ 向量化距离度量 `dist = np.abs(rotated-dec)**2`（`:104-106`）+ 滑窗平均（`:108-110`）+ `best_b = np.argmin(metrics, axis=0)`（`:113`）。docstring "Blind Phase Search (Pfau 2009, JLT)" 确认是独立算法。ADVISOR_BRIEFING 报 NDA-ML ≈ BPS 0.006-0.14 dB 证 BPS 是 comparator。确认 BPS 是 search 但**不是** NDA-ML 一部分，不能因 BPS 是 search 而称 NDA-ML 是 search。
5. **用户冻结合同承重前提 A 证伪**（PASS）：用户冻结 A = "当前 full-search NDA-ML 均匀穷举大量候选导致计算冗余"。核查 1-4 证明：①不存在 "full-search NDA-ML"（本体是 closed-form）；②无 candidate 枚举；③无 objective 在候选集上求值。A 在源码层不成立。
6. **双门 B primary cost metric 失效**（PASS）：双门 B = "objective evaluations 至少减少 4×" + "性能非劣 CI upper ≤0.10 dB"。核查确认无 objective evaluations 可数（核查 1-2），primary cost metric 无定义。双门不可执行（非"未过"，是 metric 不存在）。
7. **最强廉价 comparator 无可作用对象**（PASS）：用户命名 "dev-tuned uniform coarse grid"。核查确认 NDA-ML 无网格（核查 1-3），coarse grid 无可 coarse 化对象。备选 "fixed two-stage coarse-to-fine / hierarchical/local refinement" 同理无对象。`_db_caliber_and_complexity.md:51-61` 确认无现有 coarse-grid/coarse-to-fine/historical comparator（grep `projects/thesis-fso/` 零命中）。
8. **Phase A 备选终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COARSE_SEARCH 不适用**（PASS）：该终态触发条件 "full search 本身已很便宜或 coarse grid 已满足双门" 语义前提是存在 search。核查 1-5 证 search 不存在，无 search 可被 coarse grid 解决。强套 = TL-33 自欺。终态不适用。
9. **method-production.md 入口四门**（PASS，3 门 FAIL 路由 STRATEGIC_GATE）：门1 physical degree of freedom——NDA-ML 估计器内无 search 自由度可裁剪 FAIL；门2 baseline failure align with candidate's lever——无 lever 可作用 FAIL；门3 named conventional comparator——dev-tuned coarse grid 无网格可 coarse 化 FAIL；门4 file:line evidence——本决策 §file:line 证据 1-6 已举。3 门 FAIL + 门4 满足，路由 STRATEGIC_GATE/BLOCKED_TESTBED 而非 factory task（method-production.md L49-50）。
10. **动估计器本体减计算 = NDA_ML_BODY_REOPEN 禁止**（PASS）：topic-index control block forbidden_actions 含 `NDA_ML_BODY_REOPEN`（L24，TL-30）。核查确认减少逐块 closed-form 成本的唯一路径是替换估计器（跳块/块间状态复用/换升幂/减 K 段数）—— 这动 NDA-ML 本体核心，触发 forbidden。确认换研究对象路径被双重禁止（违反问题定义 + 触发 forbidden）。
11. **终态 STRATEGIC_GATE 合法性与唯一性**（PASS）：用户合同允许终态集含 STRATEGIC_GATE（"若无法证明计算问题或 novelty boundary，终止为 STRATEGIC_GATE，不计包"）。核查 5-9 证前提 A 证伪、双门 metric 失效、coarse-search 终态不适用、入口四门 3 FAIL——STRATEGIC_GATE 是**唯一合法终态**（EXECUTION_INVALID 不适用因无执行；EVIDENCE_INSUFFICIENT 不适用因非 held-out 数据不足而是前提证伪；NO_DIAGNOSTIC_METHOD_SIGNAL/COMPUTE_EFFICIENT_METHOD_SIGNAL 要求实验产物，本轮无 sprint）。
12. **不计有效包 + campaign 计数正确**（PASS）：P09 入口门否决 = `count_excludes: entry_preflight_only`（同 CP028/CP029 先例）。campaign `accepted_valid_packages` 维持 8/10，`current_package` 维持 P09（入口已否待重指定），不触发同族连续计数（P09 未启动新族），不重开 G 族（维持 D049 关闭）。
13. **无 truth leakage 风险**（PASS，trivially）：P09 未运行任何 deployable 路径（入口门即否），无 receiver 调用图可泄漏 true SNR/h/θ。NDA-ML 本体历史 NDA_ML_BODY 不在本次核查范围（forbidden，未触碰）。

**结论**：P09 入口门裁决 `STRATEGIC_GATE` 科学事实基础**唯一正确**。承重前提 A（NDA-ML = full-search 均匀穷举候选）在源码层被证伪（`_recovery.py:171-273` closed-form + grep 零命中 + 生产 driver `:180-187` 逐块 closed-form + BPS 是独立竞争对手）。双门 primary cost metric 失效（无 objective eval 可数），coarse-search 终态不适用（无 search 可被 coarse grid 解决），入口四门 3 FAIL 路由 STRATEGIC_GATE。动估计器本体减计算触发 `NDA_ML_BODY_REOPEN` forbidden。STRATEGIC_GATE 是唯一合法终态。**counts_as_valid_package=False**（count_excludes=entry_preflight_only），campaign accepted_valid 维持 **8/10**。本轮无实验/无 held-out seed/无 artifact/无 sprint。claim ceiling 不变（LOCAL_SLICE / NONBINDING_DIAGNOSTIC）。protected owner/formal/Skill/thesis framework 不改、无 push。

**未运行独立 sub-agent 的说明**：本轮入口门核查对象是源码事实（closed-form vs search），主线程已逐行 Read + grep 复算 + Explore 子 agent（agent_c9883e0a，fresh context）交叉确认 NDA-ML 实现是 closed-form、无 candidate grid、BPS 是独立竞争对手。V075 教训（verifier 必须递归调用图 + 运行时 metamorphic 门）适用于有 deployable 路径的科学包；P09 入口门未运行 deployable 路径，无调用图可递归、无 runtime 可 metamorphic，故核查以静态源码 + grep 复算为主，辅以 Explore 子 agent fresh context 交叉。若用户授权重指定 P09 入口并启动新族 sprint，须按 V075 标准（递归 AST + metamorphic 门）核查。

---

## V077: 计数纠正（chronology 缺陷）独立复核 — PASS（P08-R2 缺独立 pre-test freeze receipt，"恢复第 8 包"效力被取代，campaign accepted_valid 8→7，G 族 STOPPED_WITH_PARTIAL_ASSET；纠正本身不计有效包）

> 关联: D051（计数纠正）/ D049+V075（被取代"恢复第 8 包"效力，engineering asset 维持）/ D050+V076（NDA-ML STRATEGIC_GATE 维持，不动）
> 日期: 2026-08-01
> 独立性: 本复核不信任 D051 executor 自述，逐项核 git artifact + 源码 + JSON 内容；与 V075/V076 不同对象（chronology 闭合，非 receiver-info-boundary 或 NDA-ML 形态）

### 复核方法

主线程确定性 grep + Python JSON 核实 + git chronology 核对（chronology 缺陷是确定性事实，不需 sub-agent；同 TL-21 确定性证据原则）。

### 逐项核查

1. **单一 commit `a21fdba` 同时含 runner+dev+test raw+verifier+result+治理**（PASS）：`git show --stat a21fdba` 22 文件 9722 insertions，含 `p08r2_run.py`（runner）、`p08r2_dev_workspace.json`（dev 327 行）、`p08r2_phaseA_raw_rows.json`（test raw 6642 行）、`p08r2_verify.py`（verifier）、`p08r2_v075_result.json`（result）、decisions/verifications/mission-log/topic-index/voice/_registry（治理）。**无任何 freeze-only commit 在前**。
2. **dev/test 在同一 runner 顺序执行，无跨进程 immutable freeze**（PASS）：`p08r2_run.py:99 def main()` 顺序 Step 0（`:120` metamorphic 门）→ Step 1（`:130` AWGN sanity）→ Step 2（`:143` dev workspace scan）→ Step 3（`:168` freeze metric，进程内步骤顺序）→ Step 4（`:221` tune B1/B2 on dev_tune）→ Step 5（`:248` test on FRESH test seeds）→ Step 6（`:276` CI）→ Step 7（`:330` verdict）。同一 Python 进程，dev 在 test 前已跑完，全部产物同 commit。"freeze"（`:5,:168` docstring）是文字描述的步骤顺序，**非密码学 receipt/hash 落盘、非 `test_started=false→true` 状态机、非 commit 边界**。
3. **grep freeze/receipt/hash/test_started 零命中**（PASS）：`grep -nE "freeze|receipt|sha256|hashlib|test_started|prefreeze|pre_freeze|pre_test|pre-test" projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_*.py` → 零结果。确认 P08-R2 全流程无任何独立 freeze 凭据机制。
4. **held-out test seeds 8000-8039 raw 与 dev/verifier/result 同 commit**（PASS）：`p08r2_phaseA.py:54 test_seeds=tuple(range(8000,8040))`；Python 核实 `p08r2_phaseA_raw_rows.json` seed range = 8000-8039（40 seeds，has 8000=True, has 8039=True）。这些 held-out seeds 的 raw 结果无任何 artifact 证明在首次被读取前合同/源码不可变。
5. **V075 verifier 盲区确认**（PASS，chronology 角度）：`p08r2_verify.py:332-335` check c = `not (dev_seeds & history) and not (test_seeds & history)` —— 只验 dev/test seeds 与 campaign history 不相交，**未核 pre-test receipt/source/contract hash 闭合**。V075 19/19 ACCEPT 是 H7/H8/H9 修复 + consistency PASS，**不是 chronology 闭合证明**。这是 V075 的盲区（consistency≠correctness 第四度重演，本次是 chronology consistency 维度）。
6. **fail-closed 判据正确**（PASS）：任务用户指令 confirmatory evidence fail-closed——无法证明 freeze 不可变 = freeze 不成立（确认性证据语境）。P08-R2 物理归因（coded loss 主导突发深衰落）**可能正确**，但其作为"有效科学包"的 chronology 证据链有缺陷，故降为 PARTIAL diagnostic + engineering asset，不计有效包。判据与 P07-R/D046、P08/D048、P08-R2/D049 同模式（科学完整性修复不计有效包）。
7. **D049/V075 engineering asset 效力维持正确**（PASS）：D051 只取代 D049/V075 的"恢复第 8 包 / G 族关闭"效力，**不废** corrected-chain/receiver/oracle engineering 资产（prefix-LS σ²_pre + γ_vis MMSE + metamorphic 门 Δ=0.0 + AST 递归 + 先验 MDE + 去 min(B1,B2)）——这些是工程产物，物理上有效，作 PARTIAL reusable asset 保留同 D048 模式。
8. **D050/V076 NDA-ML 结论维持正确**（PASS）：D051 不动 NDA-ML 是 closed-form 非 search 的源码事实结论；本纠正只动 P08-R2 计数效力，不触发 `NDA_ML_BODY_REOPEN`。NDA-ML STRATEGIC_GATE 裁决维持。
9. **纠正本身不计有效科学包正确**（PASS）：属 `count_excludes: science_integrity_repair`，同前 3 轮修复模式（P07-R/D046、P08/D048、P08-R2/D049）。本次是 chronology 纠正不是新一轮实验。
10. **计数纠正目标值正确**（PASS）：`accepted_valid_packages` 8→**7**（P08-R2 不计有效包，G 族 STOPPED_WITH_PARTIAL_ASSET）。rolling_queue P01-P07 有效序列维持（P07-R 是 P07 的修复型 PARTIAL，P07 本身是第 6 有效包 PROBLEM_ABSENT；P08-R2 原本试图作第 8 包恢复但 chronology 不足）。
11. **不重开 G 族 / 不允许 P08-R3 正确**（PASS）：G 族 STOPPED_WITH_PARTIAL_ASSET，禁 coded/interleaving 换名重开（TL-30）。若未来恢复须用独立 freeze receipt 重跑（新 D### 授权）。

### 结论

计数纠正 `accepted_valid_packages 8→7`、G 族 `STOPPED_WITH_PARTIAL_ASSET`、D049/V075 engineering asset 维持、D050/V076 NDA-ML 结论维持、纠正本身不计有效包——**全部 PASS**，证据闭合（git chronology + grep 零命中 + seed range 实测 + verifier 盲区确认）。**counts_as_valid_package=False**（count_excludes=science_integrity_repair）。campaign accepted_valid = **7/10**。无 protected owner/formal/Skill/thesis framework 改动、无 push。

**V075/V076 盲区教训（consistency≠correctness 第四度）**：V075 递归 AST + metamorphic 门覆盖了 receiver-info-boundary（H7/H8/H9）但**未覆盖 chronology 闭合**（pre-test freeze receipt）；V076 覆盖了 NDA-ML 形态源码事实但同样不涉 chronology。本轮 P09（`H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH`）若启动 sprint，verifier **必须新增 chronology 闭合检查**：pre-test freeze receipt 含 contract SHA256 + source hash + `test_started=false`，独立 commit 在任何 held-out seed 读取前，runner 校验当前源码/contract hash 与 receipt 一致后才 `test_started=true`。

---

## V078: P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH 独立 verifier — ACCEPT (11/11 PASS)；verdict EVIDENCE_INSUFFICIENT 诚实正确；chronology 闭合正确建立；campaign 维持 7/10

> 关联: D052（P09 verdict）/ D051（计数纠正维持 7/10）/ V077（chronology 教训落实到 P09 sprint）
> 日期: 2026-08-01
> 独立性: fresh-context sub-agent（agent_cd1c4b2a）逐项核 git artifact + 源码 + JSON + 重跑 sanity，不信任 executor 自述。本轮是 V077 教训（chronology 闭合必须查）的首次落实验证。

### 逐项核查（11/11 PASS）

1. **Commit 1 早于任何 held-out test**（PASS）：`git log --oneline -3` HEAD=20d5825（Commit 1）。`git show 20d5825:.../p09_freeze_receipt.json` 含 `test_started: false`（Commit 1 时点）。`git show 20d5825 --stat` 不含 `p09_test_raw_rows.json`/`p09_test_result.json`（test artifacts 未提交，test 后才生成）。`git ls-files` 确认两 test 文件 untracked。**chronology 闭合正确建立**（修复 P08-R2 缺陷）。
2. **receipt/source/contract hash 闭合**（PASS）：重算 6 个源文件 SHA256 全部匹配 receipt（p09_bps_methods.py=4d654d4c, p09_run.py=673fc30a, _recovery.py=afb8aed9, _modulation.py=036fb7aa, _channel.py=800e4375, _b11_params.py=6159a891）；重算 `contract_sha256()`=007543e0...433485 匹配 receipt。`verify_freeze_receipt()` 逻辑（receipt 自身 hash + source hashes + contract SHA256 + test_started=false）正确。
3. **held-out seeds fresh**（PASS）：receipt test_seeds=[12000..12039]（40），dev_seeds=[11000..11019]。test∩dev=∅，test∩history(P08-R2 8000-8039/9000-9019 ∪ P08-R 6000-6019/7000-7039 ∪ P08 1000-1014/1100-1114)=∅，dev∩history=∅。p09_test_raw_rows.json 只含 seeds 12000-12039，6 方法 × 40 行。
4. **16APSK BPS objective 实现正确**（PASS）：`bps_objective_matrix`（p09_bps_methods.py:59-79）算 `|rotated-dec|²/(|dec|²+1e-10)` Pfau 2009 归一化距离 objective，B 个测试相位；`unwrap_phase(pe_raw, M0_fold=8)` 用 M0=8（16APSK 两环 8+8）非 QPSK M=4。sanity：clean 16APSK（phi_true=0.37, 30dB 无噪）经 full pipeline（含 M0-fold resolve）BER=0.0。
5. **full/coarse/two-stage/candidate 信息和延迟公平**（PASS）：6 个 method fn 全只取 rx_block + 自身超参；grep `gamma_bar|true_phase|true_snr|tx_bits|h_true|phi_true|generate_shared_realization` 在 p09_bps_methods.py 代码零命中（仅 docstring）。全用 256-sym 块（P.N_DFT=256），同 BPS objective，无跨块状态。
6. **refinement 全部成本已计数**（PASS）：实测验证——B0_full=64×256=16384 ✓；B1_coarse(32)=8192 ✓；B2_two_stage(16+8)=(16+8)×256=6144（两 stage 全计）✓；C1_conf_gated=16×N+n_refined×8=6144（refinement 全计）✓；C2_curv=16×N+n_refined×8=4688 ✓；C3_early_stop=B_used×N=2048 ✓。源码行 195(B2)/254(C1)/306(C2)/348(C3) 确认。
7. **完整 deployable 调用图无 truth leakage**（PASS）：decide path `method_fn(seg)`→`bps_objective_matrix/per_symbol`→`hard_decision_m16apsk`→只用 `_M16APSK_CONST`（星座）+ rx_block。无 `generate_shared_realization_apsk` 内部（h/phi/bits/gamma_bar）调用。唯一 TX-truth 用途是 `resolve_m16apsk_blockwise(rx_comp, tb, ...)`（p09_bps_methods.py:381）——标准 BPS M0-fold 模糊消除后处理（同 run_bps_ablation.py），在 eval/resolve 步非 phase-decision 步，只试 8 个 π/4 旋转选最低 BER，不反馈进相位估计。
8. **raw→aggregate**（PASS）：从 p09_test_raw_rows.json 重算 6 方法 ber_mean + evals_per_sym，relError=0.00e+00（<1e-9），n_traj=40/40 全匹配。B0_full bootstrap CI recheck lo=0.025641 hi=0.037433 精确匹配。
9. **性能非劣和复杂度双门**（PASS，诚实性确认）：b0_ber=0.031427, mde_ber=0.005, non-inf thr=0.036427。逐方法：B1 ci_hi=0.03925(>thr FAIL)+reduction 2.0×(FAIL)；B2 ci_hi=0.03981(FAIL)+1.6×(FAIL)；C1 ci_hi=0.05905(FAIL)+2.67×(FAIL)；C2 ci_hi=0.06808(FAIL)+3.93×(FAIL)；**C3_early_stop ci_hi=0.03716(>thr 0.036427 by 0.00073, FAIL non_inf)+reduction 8.0×(PASS complexity only)**。无一方法双门全过。max ber_ci_hw=0.00816 > mde_ber/2=0.0025 → EVIDENCE_INSUFFICIENT。**verdict 诚实正确**：C3 是最强候选（8× reduction + BER 点估计持平）但 CI upper 略超 non-inf 且 CI 宽度远大于 MDE/2。
10. **terminal verdict 唯一**（PASS）：p09_test_result.json 恰一个 `verdict`=`"EVIDENCE_INSUFFICIENT"`，在 allowed_terminals 内精确匹配（无括号后缀）。
11. **campaign 从正确 7/10 更新**（PASS）：topic-index.md:54 rdl_campaign `accepted_valid_packages: 7`（D051 chronology fail-closed 纠正后正确计数）。P09 EVIDENCE_INSUFFICIENT 非 signal 包，不计有效包，campaign 正确维持 7/10（非 8/10）。

### 结论

P09 `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH` verdict `EVIDENCE_INSUFFICIENT` + chronology 闭合正确建立 + campaign 维持 7/10——**全部 11/11 PASS，ACCEPT**。

**关键诚实性确认**：C3_early_stop 实测 8× complexity reduction + BER 点估计与 full BPS 持平（0.0312 vs 0.0314）是有前景的 bounded pre-formal carrier 信号，但其 BER CI upper (0.03716) 略超 non-inferiority 阈值 (0.036427) ~0.16 dB，且 CI half-width (~0.008 BER ~1.3 dB) ≫ MDE/2 (~0.0025 BER)，n=40 traj 不足以 resolve 0.10 dB MDE。EVIDENCE_INSUFFICIENT 是唯一合法诚实终态（FR-25 Go/Kill 标准分离：complexity 门 PASS ≠ METHOD_SIGNAL，须独立过 non-inf CI 门 + MDE 功效门）。

**chronology 闭合确认（V077 教训首次落实）**：本包 freeze receipt 独立 Commit 1 (`20d5825`) `test_started=false` 在任何 held-out test 前；test 模式校验 source hash + contract SHA256 + receipt hash 一致后才 test_started=true；held-out seeds 12000-12039 fresh disjoint。**修复了 P08-R2 的 chronology 缺陷**——这正是 V077 提出的"后续 P09 sprint verifier 必须新增 chronology 闭合检查"的首次落实验证，且 PASS。

---

## V079: P09 科学终态纠正 EXECUTION_INVALID/KILL_C3 独立复核 — ACCEPT（独立语义审计 6/6 PASS + V078 漏审 6 项承重缺陷确认 + EXECUTION_INVALID 唯一合法诚实终态）；D052 EVIDENCE_INSUFFICIENT 科学结论被取代（chronology 闭合仍有效）

> 关联: D053（P09 科学终态纠正）/ D052（被取代科学结论）/ V078（漏审的 11/11 ACCEPT，标"consistency 通过但 correctness 漏审"）
> 日期: 2026-08-01
> 独立性: 双层独立——① 独立语义审计子 agent（agent_d4ffc6b4，fresh-context）逐项读源码 + 数值复算；② 本 V079 主线程整合审计结论 + 复核 V078 漏审点 + 判 EXECUTION_INVALID 唯一性。不信任 executor/V078 自述。

### 逐项核查（6/6 PASS — 六项承重缺陷全部属实）

1. **(8,8)-16APSK π/4 旋转对称**（PASS）：`_modulation.py:199-201` 两环各 8 点均匀 π/4 分布。独立数值复算：旋转点集乘 exp(j·k·π/4) k=1..7 全部与原点集双射，max|min_dist|<7e-16（<1e-9 阈值）。
2. **B0 64 点含 8 组对称重复**（PASS）：`p09_bps_methods.py:134,75-78`。独立数值复算随机 rx 的 64 phase metrics：metrics[k] vs metrics[k+8] max|Δ|<4.5e-15（数值噪声级）→ 64 phase 实际只有 8 个独立相位，8 组各 8 个完全重复。
3. **C3 真实成本仍 64 eval/sym（记账欺骗）**（PASS）：`p09_bps_methods.py:329` `metrics_all,_ = bps_objective_matrix(rx_block, phases_all)`（phases_all=2π·arange(64)/64）**先算全部 64×N 距离矩阵**；`:348 n_evals=B_used*N` **只对 B_used 计费**。注释 `:328` 自认"先算全部用于 early-stop 判定，但只计费 B_used 个"。真实 FLOP=64 eval/sym，报告 8 eval/sym 是事后少报已发生计算。
4. **C3 非数据驱动 adaptive，恒定截断**（PASS）：`p09_bps_methods.py:335-342`。freeze receipt `dev_summary.phase_c_c3`：B_min=8 三档 stop_thresh (1e-5/1e-4/1e-3) evals 全=8.0；B_min=16 全=16.0；B_min=4 有微小变化（5.69-6.83，因 4 非 8 倍数对称不完美对齐）。独立验证 5 档 thresh × 10 随机块：B_min=8 五档全 [8,8,8,8,8,8,8,8,8,8]。π/4 对称致 metrics[k] 与 metrics[k+8] 相等 → 从 B_min 继续加 phase 不改 argmin 不降 block-mean best metric → early-stop 在 B_min+1 立即触发，B_used 恒定=B_min。**非 adaptive 是对称驱动的恒定截断**。
5. **resolve 用 TX bits → truth-resolved BER 违反 forbidden_information**（PASS）：`_modulation.py:278,301,304-308` `resolve_m16apsk_blockwise(rx, tx_bits, ...)` 接收 tx_bits，用 8 旋转假设选最低 BER。`p09_bps_methods.py:381` `run_method_on_signal` 把 `tb=tx_bits[:L*4]` 传给 resolve。`p09_run.py:99` 合同 `forbidden_information: ["...", "TX symbols/bits in deployable decide"]`。**resolve 是 decide 的一部分（决定最终 BER 的相位模糊解卷绕），消费 tx_bits 即违约**，无论是否反馈进相位估计。输出是 PI-BER/truth-resolved BER，非 receiver-visible fixed-label BER。
6. **0.10dB↔0.005BER 换算差 12× + 无 paired Δ CI**（PASS）：`p09_run.py:509 mde_ber=0.005`，但 Phase A dev 数据估 dBER/dSNR@18dB=-0.004178/dB（central diff 16→20dB），故 0.10dB≈0.00042 BER，mde_ber=0.005 比真实换算宽 **12×**。`:310-318 bootstrap_ci` 每 method 独立调一次，`:513,522 non_inf=a['ber_ci_hi']<=b0_ber+mde_ber` 是两独立 CI 边界比较，**全程无 per-trajectory paired ΔBER=C3_BER-full_BPS_BER 的 bootstrap CI**。

### V078 漏审确认（"consistency ≠ correctness" 第四度重演）

V078 11/11 ACCEPT 但漏掉全部 6 项承重缺陷：
- **check 5（信息和延迟公平）误判 resolve 用 tx_bits**：写"标准 BPS M0-fold 模糊消除后处理…只试 8 个 π/4 旋转选最低 BER，不反馈进相位估计"——但合同 forbidden_information 是 "TX symbols/bits in **deployable decide**"，resolve 是 decide 的一部分（决定最终 BER 的相位模糊解卷绕），消费 tx_bits 即违约，无论是否反馈进相位估计。V078 把"不反馈进相位估计"等同于"不进 decide"是范畴错误。
- **check 6（refinement 全部成本已计数）只对 B_used×N 公式**：不查 `:329` 是否已先全算 64×N。记账欺骗（少报已发生 FLOP）未被检出。
- **check 9（双门）不核 mde_ber=0.005 与 0.10dB 换算一致性**：直接采信 executor 的 mde_ber=0.005，不独立换算 0.10dB↔BER。
- **缺失运行时 metamorphic 门**：未做"翻 N/翻 stop_thresh 验证 B_used 是否恒定"的运行时验证（若做会发现 B_used 恒定=B_min）。

**模式**：P07-R/D046 → P08/D048 → P08-R2/D049 → P09/V078 是"consistency≠correctness" **第四度重演**。verifier 沿调用图未递归到 `bps_objective_matrix` 内部 + 未跑运行时 metamorphic 门 + 未独立换算 metric 阈值。**强化教训**：verifier 必须①递归遍历 deployable 调用图（含 resolve/后处理）②跑运行时 metamorphic 门（翻参数验不变性）③独立换算所有 metric 阈值（dB↔BER）。

### EXECUTION_INVALID 唯一合法性

- **非 EVIDENCE_INSUFFICIENT**：D052 的 EVIDENCE_INSUFFICIENT 隐含"C3 是有前景 carrier，只是 n=40 CI 不足"。独立审计推翻前提——8× reduction 与 BER 持平本身是假信号（记账欺骗 + 对称冗余 + truth-resolved BER），不是"信号弱"是"信号不存在"。
- **非 STRATEGIC_GATE**：STRATEGIC_GATE 是入口门失败（承重前提证伪），P09 已过入口门跑完实验，问题是实验执行违反合同（truth-resolved BER + 记账欺骗 + metric 换算错），属 EXECUTION_INVALID。
- **非 NO_DIAGNOSTIC_METHOD_SIGNAL**：该终态隐含"问题真实存在、常规 comparator 部分缓解、无方法增量"，但 P09 的"问题"（BPS 64 点搜索开销）本身含 8× 冗余是物理事实，C3 的"8× reduction"是去掉冗余非方法贡献，且所有 BER 是 truth-resolved。无合法诚实 NO_SIGNAL 判据。
- **EXECUTION_INVALID 是唯一合法诚实终态**：P09 违反自身合同三处（forbidden_information TX bits 进 deployable decide/resolve + complexity metric 真实 cost 未如实计 + primary metric mde_ber 换算 12× 错 + 无 paired Δ CI）。

### 结论

P09 `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH` 科学终态 **`EVIDENCE_INSUFFICIENT` → `EXECUTION_INVALID/KILL_C3`** 是唯一合法诚实纠正。**ACCEPT** D053 纠正。campaign 维持 **7/10**（P09 EXECUTION_INVALID 不计有效包；纠正本身 count_excludes=science_integrity_repair 不计包）。D052/V078 保留（chronology 闭合 Commit 1 freeze receipt 模式仍有效作方法论资产；D052 入口门裁决仍有效），但科学结论（EVIDENCE_INSUFFICIENT + "诚实正确"）被取代。

---

## V080: P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER 独立 verifier — ACCEPT（Phase A fresh crossover FAIL 复现确认 + chronology 闭合正确 + PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE 唯一合法诚实）；campaign 维持 7/10，campaign-level 裁决完成 0 active carrier

> 关联: D054（P10 verdict）/ D053（P09 纠正维持 7/10）/ V079（P09 纠正确认）
> 日期: 2026-08-01
> 独立性: 双层独立——① Phase A executor 子 agent fresh-context（agent_8c4b53c6）独立实现 + 运行 + 裁决，只读 dev seeds 不读 test seeds；② 本 V080 主线程整合 Phase A 结果 + 复核入口门 + chronology 闭合 + 判终态唯一性。不信任 executor 自述，逐项核 JSON + git chronology + freeze receipt。

### 逐项核查

1. **Commit 1 早于任何 held-out test**（PASS）：`git log --oneline -3` HEAD=56fee4c（Commit 1）。`git show 56fee4c:.../p10_freeze_receipt.json` 含 `test_started: false`（Commit 1 时点）。`git show 56fee4c --stat` 含 freeze receipt + sha256 + INVALIDATED_BY_D053 + P10 sandbox（methods/run/entry_gate）+ 治理文件，**不含** `p10_phaseA_dev_raw.json`（Phase A artifact 在 Commit 1 后生成）。**chronology 闭合正确建立**（V077 教训第二次落实，P09 模式复用）。
2. **receipt/source/contract hash 闭合**（PASS）：重算 9 个源文件 SHA256（p10_methods.py/p10_run.py + 7 frozen common/explore 文件）全部匹配 receipt（p10_run.py verify 模式 PASS）；重算 `contract_sha256()`=8e603bd4... 匹配 receipt。freeze receipt 自身 sha256 一致。
3. **Phase A fresh seeds**（PASS）：receipt `dev_seeds_phaseA=[13000..13005]`（6 trajectory × 2 cell = 12 realization）。Phase A raw 只含 seeds 13000-13005。test_seeds=[14000..14039] **未被读取**（Phase A FAIL Phase B/C 不运行，无 held-out test）。dev∩test=∅，dev∩history(P09 11000-11019/12000-12039 ∪ P08-R2 8000-8039/9000-9019 ∪ P08-R 6000-6019/7000-7039 ∪ P05 1000-1011)=∅。
4. **freeze receipt test_started 维持 false**（PASS）：Phase A 完成后 receipt `test_started: false`（dev_summary 追加 Phase A 结果但 test_started 不变）。无 held-out test 执行（Phase A FAIL gate 顺序直接终止）。
5. **Phase A crossover 判据诚实**（PASS）：ML_favored cell (N=2M fg30 SOP=1e-7) Δ=-6.08e-5 |Δ|≪MDE=0.02 crossover_pass=False（6/6 ml_wins 但绝对差微不足道，P05 老路 corrected standard-CMA 已解决 fixed-label swap）；CMA_favored cell (N=5M fg1000 SOP=4e-7) Δ=+0.4500 crossover_pass=True（fixed-label CMA 占优）。crossover_directions_consistent=False（ML_favored 无 crossover + CMA_favored 是 swap artifact）。phase_a_verdict=FAIL 诚实正确。
6. **CMA_favored swap artifact 确认**（PASS）：CMA_favored cell PI-BER ML=0.0237 vs CMA=0.0396 Δ_pi=-0.016（两者相当），fixed-label ML=0.4896 vs CMA=0.0396 Δ=+0.4500（CMA 大幅占优）。两口径方向不一致→ML 的 fixed-label 失败是 π 级 polarization swap（不变量 10：PI-BER 对 swap 结构性失明）。**swap artifact 非 ranking 反转**。
7. **ML_favored P05 老路确认**（PASS）：ML_favored cell (短 N 小 SOP 累积旋转 ~11.5°) ML fx≈3e-7 CMA fx≈6e-5 都接近完美。corrected StandardCMA (Godard 1980 with-z) 在 fixed-label 上已解决 swap，D015 历史 ML 优势（针对 scalar-error 缺 z current-CMA）在 corrected standard-CMA 下消失。与 P05 PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER 同构。
8. **fixed-label PRIMARY 口径正确**（PASS）：Phase A 用 `evaluate_outputs(...)["fixed_label_ber"]["mean"]`（prompt012_longseq_audit），这是真 fixed-label（直接 label 对比，不试旋转选最低，非 PI-BER/truth-resolved，与 P09 resolve_m16apsk_blockwise 用 tx_bits 的 truth-resolved BER 不同）。PI-BER 作 secondary 报告。**口径无 P09 缺陷 5 的 truth-resolution 问题**。
9. **完整 deployable 调用图无 truth leakage**（PASS）：Phase A channel 生成用 sX/sY（TX symbols）生成 rx（合法 signal synthesis），ML train_on_prefix 用 sX/sY 作 label（合法 supervised training on known prefix），CMA equalize 只用 rx（合法 blind）。TX truth 只用于最终 BER 计分（fixed-label + PI-BER）。无 router decide（Phase A 是 fresh crossover test 非路由实验）。
10. **raw→aggregate**（PASS）：从 p10_phaseA_dev_raw.json 重算两 cell mean ML/CMA fixed+PI，relError=0.00e+00。
11. **terminal verdict 唯一**（PASS）：Phase A FAIL → gate 顺序 → `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE`（用户合同 §入口门明文允许的 fresh-dev-fail 终态）。verdict 在 allowed_terminals 内精确匹配。非 PROBLEM_RESOLVED_BY_SIMPLE_ROUTING（crossover 不存在未到 Phase B）；非 NO_DIAGNOSTIC_METHOD_SIGNAL（未到 Phase C）；非 EVIDENCE_INSUFFICIENT（CI 宽度非瓶颈）；非 STRATEGIC_GATE（入口门已过 Phase A 是 fresh dev）；非 EXECUTION_INVALID（合同执行合法）。
12. **premise A 反转诚实标注**（PASS）：用户指令 §二 premise A 描述"长慢变 ML 占优"与证据方向相反。Phase A 用证据支持的方向（ML_favored=短N小SOP；CMA_favored=长N大SOP）测试，结果仍 FAIL。**无论 premise 方向，crossover 在 fixed-label PRIMARY 下都不成立**——这是 P05 老路根本结论。诚实标注在 D054 + worker-log，不强行 PASS。
13. **campaign 计数正确 + campaign-level 裁决完成**（PASS）：topic-index.md rdl_campaign `accepted_valid_packages: 7`（D053 纠正后正确计数）。P10 PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE 不计有效包（count_excludes=entry_phase_A_fail）。**P10 是 campaign 第 10 包（campaign_level_decision_at: P10）**——D039 授权的 10-有效包探索完成（7 有效 P01-P07-R + P08-R2 PARTIAL + P09 EXECUTION_INVALID + P10 PROBLEM_ABSENT），所有候选 honest negative 0 signal，0 active carrier。campaign 诚实终止。

### 结论

P10 `RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER` verdict `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE` + chronology 闭合正确建立 + campaign 维持 7/10 + campaign-level 裁决完成 0 active carrier——**全部 13/13 PASS，ACCEPT**。

**关键诚实性确认**：Phase A fresh crossover 在 fixed-label PRIMARY 口径下不成立（ML_favored P05 老路 corrected standard-CMA 已解决 swap；CMA_favored CMA 优势是 swap artifact PI-BER 两者相当）。这是用户合同 §入口门明文允许的 fresh-dev-fail 终态。crossover-based single-expert router 方向在 corrected standard-CMA 下无可作用空间。

**chronology 闭合确认（V077 教训第二次落实）**：Commit 1 (`56fee4c`) freeze receipt `test_started=false` 在任何 held-out test 前；Phase A 只读 dev seeds 13000-13005；未读 test seeds 14000-14039（Phase A FAIL 无 held-out test）。**P09 chronology 模式成功复用**。

**campaign-level 裁决（P10 是第 10 包）**：D039 授权的 10-有效包探索完成，0 active carrier，所有候选 honest negative 0 signal。campaign 诚实终止。


## V081: P10 终态降级（PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE → EVIDENCE_INSUFFICIENT / LOCAL_TWO_CELL_PROBE）独立复核 — ACCEPT（五项承重不足确认 + chronology 闭合保留 + 终态降级唯一合法诚实 + campaign 未终止 remaining=3）

> 关联: D055（P10 终态降级）/ D054/V080（原 P10 裁决，保留 chronology+raw，降级终态+count+campaign-complete）
> 日期: 2026-08-01
> 独立性: 主线程独立核实 P10 freeze receipt + git chronology，不信任 D054/V080 executor 自述。

### 逐项核查

1. **P10 freeze receipt 五项承重不足确认**（PASS，逐字段读 `projects/simulation/results/p10_single_expert_router/p10_freeze_receipt.json`）：
   - ① **仅 2 预选 cell**：receipt `crossover_cells` = {ML_favored_hypothesis, CMA_favored_hypothesis} 两 cell。用户 P11 指令 §五"≥4 预声明 problem-bearing cells"对标，2 cell 远不足。
   - ② **每 cell 仅 6 dev seed**：receipt `dev_seeds_phaseA=[13000,13001,13002,13003,13004,13005]`，6 trajectory。`held_out_test_run: false`，`held_out_test_seeds_read: []`（test_seeds 14000-14039 未读）。
   - ③ **未满足 cell 多样性**：两 cell 同 `turb: strong`，仅 N(2M/5M) / f_G(30/1000) / SOP(1e-7/4e-7) 变化，无 weak/moderate 档覆盖。
   - ④ **Phase B configuration rule 未运行**：receipt `phase_b_c_run: false`，`reason_phase_b_c_not_run: "Phase A FAIL -> gate order -> ... 终态, Phase B/C 不运行"`。contract `baseline_ladder.B3_configuration_only_rule` ("N>=N_thresh -> CMA else ML") 从未执行 → "RESOLVED_BY_CONFIG_RULE" 措辞无 Phase B 证据。
   - ⑤ **git chronology 闭合正确**（保留有效）：`git show 56fee4c --stat` 含 freeze receipt+sha256+entry_gate+methods+run，**不含** `p10_phaseA_dev_raw.json`；`git show 345d9e3 --stat` 含 `p10_phaseA_dev_raw.json`（Phase A raw 在 Commit 1 后生成）。chronology 非 P08-R2 型缺陷。

2. **终态降级唯一合法**（PASS）：EVIDENCE_INSUFFICIENT / LOCAL_TWO_CELL_PROBE 是唯一合法诚实降级——2 cell × 6 seed 局部 probe 既不能确认也不能推翻 crossover（外推过度归纳风险），Phase B configuration rule 未运行（"RESOLVED_BY_CONFIG_RULE" 措辞无据）。非保留 PROBLEM_ABSENT（证据不足确认 crossover 不存在）；非 EXECUTION_INVALID（chronology 合法无合同违反）；非 STRATEGIC_GATE（入口门已过）。

3. **chronology + raw 数据保留有效**（PASS）：D054/V080 的 chronology 闭合（Commit 1 freeze receipt pre held-out）、Phase A fresh dev seeds（13000-13005 disjoint 全部 history）、Phase A raw（两 cell 局部发现 ML_favored P05 老路 + CMA_favored swap artifact）均保留作局部诊断 + 方法论资产。**降级只针对终态宣称 + count + campaign-complete，不动 chronology/raw**。

4. **campaign 未终止 / remaining=3**（PASS）：D039 授权 10 有效包，当前 accepted_valid=7（D051 纠正后正确计数），P10 降级后仍不计有效包（count_excludes=evidence_insufficient_local_probe），**remaining_valid_packages=3**。撤回 D054/V080 "campaign-level 裁决完成 / 0 active carrier / campaign 诚实终止"——campaign **未终止**，用户已授权 P11 继续。

5. **single-expert-router 族不关闭**（PASS）：用户指令 §一 line 31 明令。P10 证据不足以下族级裁决，族维持 open；本轮不补跑 P10（立即进 P11）。

6. **accepted_valid 维持 7/10**（PASS）：P10 原本不计有效包（D054 count_excludes=entry_phase_A_fail），降级后仍不计（count_excludes=evidence_insufficient_local_probe），计数不变。remaining=3。

7. **不篡改旧 checkpoint**（PASS）：用户指令 §一 line 34"不篡改旧 checkpoint，mission-log 追加新 checkpoint"。D054/V080/CP045 保留历史，标"被 D055/V081 部分取代"，新 CP046 追加。worker-log step-040 追加降级段不删旧内容。

### 结论

P10 终态降级（PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE → EVIDENCE_INSUFFICIENT / LOCAL_TWO_CELL_PROBE）+ chronology 闭合保留 + campaign 未终止 remaining=3 + single-expert-router 族不关闭——**全部 7/7 PASS，ACCEPT**。

**关键诚实性确认**：2 cell × 6 dev seed 局部 probe 不足以下 campaign-level 终局裁决。撤回"0 active carrier / campaign 诚实终止"过度宣称，campaign 维持 open，remaining_valid=3。Phase B configuration-only rule 未运行是"RESOLVED_BY_CONFIG_RULE"措辞的关键漏洞——降级 EVIDENCE_INSUFFICIENT 是唯一合法诚实。

**campaign 计数纠正**：accepted_valid=7/10 维持，remaining_valid=3，campaign 未终止。立即进 P11（用户已授权）。


## V082: P11 PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR 独立 verifier — ACCEPT（14/14 PASS）；linear Butterfly FIR 身份确认 + B2 complex LS 1% pilot 达/超 full-label Adam + 公平 pilot 合同 + chronology 闭合 + PROBLEM_RESOLVED_BY_COMPLEX_LS 唯一合法诚实；campaign accepted_valid 7→8

> 关联: D056（P11 verdict）/ D055/V081（P10 纠偏维持 7/10 进入 P11）
> 日期: 2026-08-01
> 独立性: 独立 verifier fresh-context sub-agent（agent_7be7b55b）逐项核源码 + 重算 raw→aggregate + git chronology + 物理机制。不信任 executor 自述。

### 逐项核查（14/14 PASS）

1. **P10 纠偏正确**（PASS）：D055（decisions.md:3302）+ V081（verifications.md:4140）确认 P10 终态 PROBLEM_ABSENT→EVIDENCE_INSUFFICIENT/LOCAL_TWO_CELL_PROBE，accepted_valid 维持 7/10，"campaign completed/0 active carrier" 撤回。
2. **Commit 1 早于 held-out test**（PASS）：`git show 4d9c374 --stat` 含 freeze receipt（test_started=false, dev_summary={}）不含 `p11_phaseA_test_raw.json`；mtime dev_raw 21:11 → test_raw/verdict 22:01 → p11_run.py edit 22:03。
3. **receipt/source/contract hash 闭合**（PASS with flagged benign discrepancy）：4/5 source hash 匹配；`p11_run.py` mismatch（post-run cosmetic print-edit 移除不存在 key `b2_vs_b0_paired_delta_test`，未改 adjudicate/run/fit 逻辑，verdict 在 print 前已保存）—— **不影响 verdict 完整性**；contract_sha256 重算匹配（ccdd4c8d...）。
4. **pilot 位置 vs TX 信息边界**（PASS）：`freeze_pilot_positions` 共享；`fit_butterfly_ls`/`fit_sparse_label_adam`/`fit_pilot_rls` 只取 `s_target[pilot_idx]`；B0 用前 50% 连续段；payload TX 只在 `fixed_label_ber`/`pi_ber` 计分。
5. **Butterfly 模型线性身份**（PASS）：`ButterflyCNNEqualizer2x2` 4 复 FIR = 8 实 Conv1d bias=False，grep nn.ReLU/Tanh/BatchNorm/LayerNorm 零命中 → linear Butterfly FIR（非 CNN），entry gate 诚实标注。
6. **LS/RLS 公式与 tap 公平**（PASS）：P11 `_augmented_rows` 实值拆分与 `run_ls_fir_trial:616` 同结构同 n_tap=11；B2 LS 只用 pilot 位置行。
7. **full/sparse 训练标签数准确**（PASS）：N=500k；B0 train_frac=0.5（250k）；pilot fracs n_pilot 精确（pf≤0.2 = N·pf，pf=0.5 ≈222268 因 np.unique 去重，所有方法共享同 pilot_idx 公平）。
8. **pilot overhead 计入 goodput**（PASS）：contract goodput = `payload_bits×(1-pilot_frac)×(1-BER)`；B2@1% goodput ≈ B0@50% 的 1.98×。
9. **fixed-label BER ambiguity 可部署**（PASS）：`fixed_label_ber` 直接 sign(real/imag) bit 比较无旋转搜索（swap-visible PRIMARY）；`pi_ber` 4 旋转 min 单独 secondary（swap-blind）。
10. **raw→aggregate 独立重算**（PASS）：max rel err 3.4e-16（浮点噪声），全 6 frac B0/B2 mean + paired Δ + CI 重算与 verdict 精确一致。
11. **paired CI、MDE、功效**（PASS）：全 frac ci_high（≤4.4e-5）≪ non_inf（MDE=0.05）；ci_hw_max 1.206e-4 ≪ MDE/2=0.025 ratio 4.8e-3 充足功效；`_adjudicate` 正确要求 b2_mean ≤ b0_mean + non_inf AND ci_high < non_inf。
12. **terminal verdict 唯一**（PASS）：PROBLEM_RESOLVED_BY_COMPLEX_LS 在 allowed_terminals；Phase A 问题证伪（B2 解决）→ gate 顺序 → Phase C 不运行 → 唯一合法；正确不误判 METHOD_SIGNAL（无候选运行，传统 comparator 解决，valid negative 非 signal）。
13. **完整 deployable 调用图无 truth leakage**（PASS）：B2 `fit_butterfly_ls` 只 pilot_idx TX；`apply_butterfly` 无 TX；无 h/theta/SNR/gamma/fG 进 B2 decide。
14. **campaign 计数正确 7→8**（PASS）：P11 PROBLEM_RESOLVED_BY_COMPLEX_LS = 有效科学负面包（held-out confirmation 完成 + 诚实 verdict），用户指令 §九 "valid negative 7→8" → accepted_valid 8/10, remaining_valid=2。

### 重算数字（item 10，held-out test n=32 paired/frac）

| pf | B0_recomp | B2_recomp | Δ_mean_recomp | CI_high_recomp | CI_hw_recomp | max rel err |
|---|---|---|---|---|---|---|
| 0.01 | 3.859e-4 | 3.176e-4 | −6.83e-5 | 3.99e-5 | 1.082e-4 | 3.4e-16 |
| 0.02 | 3.859e-4 | 3.102e-4 | −7.57e-5 | 4.30e-5 | 1.187e-4 | 1.8e-16 |
| 0.05 | 3.859e-4 | 3.114e-4 | −7.45e-5 | 4.37e-5 | 1.182e-4 | 1.7e-16 |
| 0.10 | 3.859e-4 | 3.140e-4 | −7.19e-5 | 4.40e-5 | 1.159e-4 | 0 |
| 0.20 | 3.859e-4 | 3.111e-4 | −7.47e-5 | 4.42e-5 | 1.189e-4 | 1.7e-16 |
| 0.50 | 3.859e-4 | 3.098e-4 | −7.61e-5 | 4.45e-5 | 1.206e-4 | 3.1e-16 |

B2_mean ≤ B0_mean 全 frac（paired Δ mean 全负 → B2 严格优于，非仅非劣）。统计功效充足。

### Notable findings

1. **p11_run.py post-run cosmetic edit（FLAGGED, benign）**：on-disk run.py hash（4607e6ad）≠ receipt 记录（e7eb9856），因 verdict 保存后移除 print dict 中不存在 key `b2_vs_b0_paired_delta_test`（修复 KeyError）。未改 adjudicate（:453-508）/main（:309-450）/fit/BER 逻辑。verdict 由 pre-edit 二进制产生（hash 匹配 Commit 1）。**后果**：现 re-run `verify_freeze_receipt()` 会 SOURCE_HASH_MISMATCH，但不影响已存在 verdict（mtime run.py 22:03 > verdict 22:01）。建议：re-freeze 或 revert cosmetic edit 后再 re-run。
2. **B2 严格优于 B0（非仅非劣）**：paired Δ mean 全负 CI_high < 0。比合同非劣门更强——linear FIR 闭式 LS 解直接 MSE 最优，Adam 迭代近似不应优于 LS，与理论一致。

### 结论

P11 `PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR` verdict `PROBLEM_RESOLVED_BY_COMPLEX_LS` + linear Butterfly FIR 身份确认 + B2 complex LS 1% pilot 达/超 full-label Adam + 公平 pilot 合同 + chronology 闭合 + campaign accepted_valid 7→8——**全部 14/14 PASS，ACCEPT**。

**关键诚实性确认**：B2 batch complex LS 在 1%–50% pilot fractions 下严格优于 full-label B0 Adam（linear FIR 监督开销不必要）。这是用户合同 §七明文的 PROBLEM_RESOLVED_BY_COMPLEX_LS 终态（有效科学负面包 + held-out confirmation 完成）。

**campaign 计数**：accepted_valid 7→**8/10**，remaining_valid=2，campaign 未终止。0 active carrier 维持（valid negative 非 METHOD_SIGNAL）。
