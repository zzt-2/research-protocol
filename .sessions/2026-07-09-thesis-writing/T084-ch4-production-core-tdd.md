# Task Brief: Ch4 production core TDD

> 来源: S028 / D063 / V038 / T081–T083 | 产出位置: Ch4 scaled-unitary production seam 与 worker log
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 25
  action_class: CH4_PRODUCTION_CORE_BUILD
  mission_checkpoint: CP025
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

按 production-evidence plan Task 3，以 TDD 建立正式 Ch4 production kernel 的公共接口和科学不变量。该任务只验证 correctness，不运行任何 BER cell、A2 bridge、smoke、tuning 或 production。

## 开始前强制读取

1. active topic CP025、D063/V038、本 brief、T081 design/plan Task 3、T083 receipt/independent verification；
2. `sim-preflight`、`thesis-lessons.md` 速查表与最近三条、`code-quality.md`；
3. `development.py`、`scaled_unitary.py`、corrected common modulation、`projects/simulation/params.py` 的 `SimulationConfig().turbulence` authority；
4. fresh task-control validator；失败立即停止。

## 文件白名单

允许新建：

1. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/production_core.py`；
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_core.py`；
3. `projects/thesis-fso/worker-logs/step-084-ch4-production-core-tdd.md`。

仅在测试证明必要时允许最小修改 `scaled_unitary.py`；不得修改 common demapper、development/confirmation/demapper-replay artifacts、params、chapter package 或治理文件。

## 冻结公共接口

- `balanced_pilots(n_pilots) -> complex ndarray[2,n_pilots]`
- `make_latent_window(scenario, latent_id, payload_symbols, max_pilots) -> dict`
- `observe_latent(latent, snr_db, n_pilots) -> dict`
- `receiver_action(arm, x_pilots, y_pilots, y_payload, parameter) -> dict`
- `score_action(action, bits, h_true) -> dict`
- `structure_mismatch_matrix(left, right, delta) -> ndarray[2,2]`

不得增加结果驱动参数、truth fallback 或 grid override。

## TDD 不变量

1. `Np∈{2,4,8,16}` 时 `Xp Xp^H=Np I`，且前缀/重复规则冻结、可复现。
2. bits、U/V/Q、Gamma–Gamma gain、standardized pilot noise、standardized payload noise 使用独立可复现的 `SeedSequence` 子流；每个子流记录完整 `spawn_key` namespace，测试 exact replay，不能只测 hash 不同。
3. 只改 SNR 时全部 latent hashes 不变，observations 只按解析噪声比例变化；只改 Np 时 bits/Q/g/payload-noise hashes 不变，pilot noise 遵循冻结 prefix/block rule。
4. weak/moderate/strong 参数必须从 `SimulationConfig().turbulence` 解析为 `(11.6,10.1)/(4.0,1.9)/(4.2,1.4)`；`0.2/1.6/3.5` 只称 plane-wave Rytov variance，rounded-parameter GG scintillation index 分别约 `0.193752/0.907895/1.122449`。kernel 不重新硬编码第二份 authority。
5. B2 `tau=1` 与 C4 共享 `UV^H`，仅公共尺度不同；测试必须明确公式身份。
6. B3_PSC 只读 receiver-visible pilots：对 `Zp=W_B2Yp`，`a=max(0,Re<tr(Zp^H Xp)>/||Zp||_F^2)`，输出对 B2 action 施加该非负实标量；分母非正/非有限或输出非有限时 fail closed，不读 `H_true`、payload bits 或 payload decisions。
7. mismatch 固定为 `H_delta=g U diag(1+delta,1-delta)V^H/sqrt(1+delta^2)`；共享 U/V/g、保持平均 Frobenius power、true singular-value ratio 随 delta 单调；这里只验证构造，不运行 levels。
8. invalid matrices、unsupported scene/Np/arm、非有限输入全部 fail closed；deployable `receiver_action` 签名和源码不得出现 truth 参数。

## 测试与终态

先运行 focused test 得到真实 RED，再做最小实现；GREEN 命令至少包括：

`python -m pytest projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_production_core.py projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_m16apsk_ml_demod.py projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_scaled_unitary.py -q`

随后运行 py_compile、task-control、精确白名单与 `git diff --check`。未参与实现的 reviewer 必须自建至少一个 RNG namespace/latent replay oracle、一个 B3_PSC closed-form oracle、一个 mismatch power oracle，并审查 truth firewall。

- `PRODUCTION_CORE_CORRECTNESS_PASS`：全部接口、不变量、回归与独立 review PASS。
- `PRODUCTION_CORE_CORRECTNESS_INVALID`：任一不变量、authority、truth firewall 或复现合同失败；停止在 correctness repair。

一次任务不 commit、不 push。PASS 只允许主控另开 fixed A2 production-seam bridge；不得在本任务运行任何 BER grid。
