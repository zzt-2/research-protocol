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
