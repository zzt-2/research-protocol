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
