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
