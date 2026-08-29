# Ch5 receiver-residual bridge 独立正确性验证

> 2026-08-30 | T061 | 独立 scientific verifier | fresh HEAD `174f36d`

## 结论

- **总裁决：PARTIAL**。
- **IMPLEMENTATION_CORRECTNESS：PARTIAL**。真实 observation 路径、Ch4→逐偏振 Ch3 DA CPR 顺序、8-fold 补偿符号、truth/future/polarization firewall 均成立；但 frozen Ch4 arm 的数值参数不进入 deployable bundle/hash，存在 T061 明定的 correctness blocker。
- **TARGET_RESIDUAL_OCCURRENCE：NOT RUN / NOT AUTHORIZED**。Ch4 acquisition pilots 绕过 shared scalar GG/CFO/Wiener；该缺口不推翻当前 bridge API 与 correctness 链，但当前 fixture 不能作为合法 occurrence generator。
- **SCIENTIFIC_METHOD_SIGNAL：NOT TESTED / NOT AUTHORIZED**。covariance identity 只证明 B1/B2/B3/C1 可消费 bundle；不得解释为 natural occurrence、headroom 或方法信号。
- **是否允许进入一次 occurrence smoke：否。**

## 按严重度排序的问题

### [P1] frozen-arm 数值配置不在 deployable bundle 与 bundle hash 中

`FrozenCh4Arm` 的承重字段为 `arm_id/mode/mu/ring_threshold/decision_threshold`（`post_ch4_ch3_bridge.py:71-77`），但 `ch4_summary` 只保存 `arm_id/mode/gate counts`（`:343-348`），deployable 输出没有 `mu` 或两个 threshold（`:148-174`）。`bundle_hash` 的 metadata 也只放入 `frozen_arm.arm_id`，其余输入仅是运行输出数组（`:359-375`）。合同虽把 `frozen_ch4_config` 列为允许的 receiver-visible 输入（`occurrence_contract.yaml:9-11`），`bundle_required` 却未冻结其数值字段（`:13-36`）。

Fresh probe 使用相同 `arm_id="same-id"`、`mode="candidate"`、`mu=0`，把两个 threshold 从 `0` 改为 `1e9`：两次 `ch4_gate_summary` 不同，但 `bundle_hash` 完全相同。即 hash 不能区分同名 arm 的不同数值配置，且甚至没有覆盖已导出的 gate summary。现有 hash 测试只改变 `rx`（`test_ch5_post_ch4_ch3_bridge.py:208-220`），因此没有发现该缺陷。

影响：receipt 不能唯一审计 occurrence 所用 frozen arm；保留 `arm_id` 重用或参数误配时会发生不可检测碰撞。按 T061 判定，这是 correctness blocker。

最小修复：把 canonical frozen-arm snapshot（`mode/mu/ring_threshold/decision_threshold`，含显式 `null`）放入 deployable bundle 和 `bundle_hash`；`realization_hash` 继续只表示接收实现、不随算法 arm 改变。新增 same-`arm_id` 数值变更测试，并覆盖 gate summary/hash 一致性。

### [P1] Ch4 acquisition pilots 绕过 shared scalar，仅可视为 correctness fixture

Observation samples 的真实生成链为 `sqrt(GG)*exp(j phase)`（`post_ch4_ch3_bridge.py:199-223`）→ Jones（`:224-225`）→ circular AWGN（`:226-230`）。但 acquisition pilots 单独生成为 `jones @ ch4_tx + ch4_noise`（`:232-236`），未经过 GG/CFO/Wiener scalar；随后该理想化 pilot block 直接进入 `pilot_ls_demux`（`:319-320`）。

Fresh sentinel probe 只打开 `f_residual_hz=8e5` 与 `linewidth_hz=2e4`：observation `rx` 最大变化 `0.6282046918`，post-Ch4 `z_pilot` 最大变化 `0.03577908047`，DA frequency 最大变化 `581164.7343 Hz`，但 `ch4_pilot_rx` 与 Ch4 `W` 的最大变化均精确为 `0.0`。这证明 shared scalar 真实流入 observation→Ch4→Ch3，却没有流入 acquisition pilots。

影响：当前 correctness bridge 的真实数据依赖成立，但 natural occurrence 中 acquisition/observation 的标量状态生命周期与相对相位/增益没有建模；不能用当前 generator 解释 occurrence。该问题是 occurrence 前置 blocker，不单独把 bridge API 判为 FAIL。

最小修复：把 acquisition pilot segment 纳入显式、可审计的 shared scalar realization/时序模型（或冻结并论证其独立 acquisition 状态），并把该状态/参数纳入 realization receipt；新增非零 GG/CFO/Wiener 下 acquisition `W` 受预期影响的测试。

### [P2] receipt 的“bundle fields complete”检查会对上述缺口给出假阳性

`run_occurrence_smoke.py:112-140` 的 required-set 与合同相同，只检查 `ch4_arm/ch4_W/ch4_gate_summary` 是否存在，不核查 frozen-arm 数值快照或其 hash 敏感性。因此 fresh smoke 报告 `bundle_fields_complete=true`，不能作为完整 frozen-config provenance 的证据。此项可与 P1 hash 修复一并关闭。

## 逐项正确性证据

### 1. shared scalar → Jones → AWGN → Ch4 → per-pol Ch3 的真实依赖

- scalar 由 `gg_block` 与 `doppler_phase` 生成并共同乘到两偏振（`post_ch4_ch3_bridge.py:199-225`）；AWGN 在 Jones 后注入（`:226-230`）。
- `run_bridge` 先调用真实 Ch4 runner（`:317-320`），再在 `for pol in range(2)` 内两次调用 `da_ml_recovery`（`:322-335`），无跨偏振 pooling。
- Fresh scalar sentinel probe 得到 `rx/z_pilot/phase/frequency/bundle_hash` 全部改变；因此不是只靠 mock call-order 成立。唯一语义缺口是 acquisition pilots 未消费 scalar，已列为 P1。

### 2. Ch3 DA CPR 输入/输出与逐偏振语义

`da_ml_recovery` 以 `angle(rx[pilot_idx]/pilot_sym)` 做 pilot-only phase regression，返回 `(rx_comp, phi_est, df_est)`（`common/_recovery.py:136-168`）。bridge 传入 post-Ch4 单偏振序列、共同 pilot indices、对应偏振 16APSK pilot symbols，并显式使用 `mod="m16apsk"`（`post_ch4_ch3_bridge.py:326-335`）。独立解析 probe 注入 `phi=0.37`、`df=2e6 Hz`，得到 phase error `3.33e-16`、frequency error `1.63e-9 Hz`、补偿最大误差 `5.03e-16`；符号与返回值顺序正确。

### 3. 8-fold 旋转索引与正负号

候选 `k` 使用 `exp(-j2πk/8)` 补偿，SSE 只在 known pilot indices 上计算（`post_ch4_ch3_bridge.py:293-306`）。Fresh pytest 对输入 `x*exp(+j2πk/8)` 的 8 个 `k` 全部唯一选择同一索引并恢复到 `x`（`test_ch5_post_ch4_ch3_bridge.py:62-75`）；31-test suite 全通过，无正负号/索引错误。

### 4. truth、future、receiver-visible 与 polarization firewall

- Offline truth 单列为独立对象（`post_ch4_ch3_bridge.py:111-118`），`run_bridge` 只接收 `ReceiverVisibleInput` 与 frozen arm（`:309-315`）。Fresh probe 同时突变 payload labels/bits、true Jones、true phase、true SNR 后 bundle hash 不变。
- Observation 在进入 Ch4 前截断到 `observation_stop`（`:317-318`）。Fresh probe 比较 `ResidualBridgeBundle` 的全部 dataclass 字段，future-window 突变后全部不变。
- Fresh polarization probe 同时核对 `z/e/labels/counts/phase/frequency/ambiguity`、`W' = PWP` 与 gate counts 交换，全部等变；不是只比较未受影响字段。
- Receiver-visible 已知 pilot sample 的微小变化会同时改变 realization/bundle hash（fresh 目标测试 `test_ch5_post_ch4_ch3_bridge.py:208-220`）。

### 5. B1/B2/B3/C1 消费 identity 的 claim ceiling

Fresh correctness smoke 中四类 covariance 均有限、对称、正定，最小特征值 `4.3790645132654896e-08`；circular B2/C1 scalar gap `6.683698138529319e-19`。这只关闭 bundle 可消费性 identity，不提供 natural R/T covariance、NLL/GMI/BER/FER 增益或方法信号。

## Fresh 验证记录

1. Task-control validator：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py .sessions/2026-07-09-thesis-writing/T061-verify-ch5-residual-bridge-correctness.md` → `PASS`。
2. `python -m pytest tests/test_ch5_apsk_structured_covariance.py tests/test_ch5_post_ch4_ch3_bridge.py -q` → `31 passed in 3.19s`。
3. `python run_occurrence_smoke.py --mode correctness` → exit 0；`truth_firewall/eight_rotation/polarization_swap/covariance_identity=PASS`，`realization_hash=b9553d20c1c9e815d1a2352c95db6d2811176d3b89ee3b391f8a9f44c149fedd`，`bundle_hash=f331ac5c444b12d6fdf4036e74590690a1841e1e85fe4474e41bd69c911973e2`。运行只刷新既有 receipt 元数据，验证后已恢复，不纳入提交。
4. `python run_occurrence_smoke.py --mode occurrence` → argparse 拒绝：`invalid choice: 'occurrence' (choose from 'correctness')`；未运行 occurrence。
5. 一次性 probe 未落盘；结果见上述 hash/scalar/DA/firewall/等变性证据。

## 唯一下一动作

回到一个严格限于 T060 bridge 的修复包：同时补齐 frozen-arm canonical snapshot/hash 契约与 acquisition-pilot shared-scalar 时序语义，并为两点各加直接回归测试；随后重新执行独立 T061 correctness verification。修复复验前不得运行 occurrence。
