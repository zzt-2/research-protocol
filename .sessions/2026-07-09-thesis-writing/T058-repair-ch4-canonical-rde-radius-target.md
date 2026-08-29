# Task Brief: 修复 Ch4 canonical RDE 最近半径目标

> 来源: S028 / D045 / T053 / T056 | 产出位置: `projects/simulation/explore/ch4-apsk-ring-gated-rde/` 与 `projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 7
  action_class: GW_STEP4A_D_IMPLEMENTATION_SMOKE
  mission_checkpoint: CP007
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

按 T056 的 `FAIL_REPAIRABLE` 精确修复 Ch4 seam：把 candidate gate 使用的 nearest-symbol 所属环特征，与 canonical RDE update 使用的 nearest-radius 目标显式分离；补上能使旧实现失败的分叉回归测试，fresh 重跑 correctness-only pytest/smoke 并刷新 receipt。不得调参、跑性能或扩方法。

## 必读与启动

1. 根 `AGENTS.md`、topic-index、D045、本 brief，先运行 task-control validator。
2. 按任务触发并完整读取 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md` 与相关测试模板。
3. 完整读取 T056 verification report、T052 §4.1、现有 Ch4 seam 和测试。
4. 公式 authority 以 T056 已核实的 JLT 2021 Eq. (1)–(3)、Ready–Gooch nearest-radius criterion 与 row-convention 独立推导为准；不要再依赖损坏的 2009 假 PDF。

## 精确修复合同

1. 新增或等价实现 receiver-visible `canonical nearest radius` 选择：对固定 APSK 半径集合最小化 `abs(abs(z)**2-r_m**2)`。
2. 保留 candidate gate 的两个原特征：nearest-symbol decision distance，以及该 nearest symbol 所属环的 normalized residual。
3. plain、cheap、candidate、oracle 四个 arm 传给 `canonical_rde_step` 的 update radius 必须统一来自 canonical nearest-radius selector，不能来自 nearest-symbol label。
4. cheap gate 继续遵守 T052 的 `native RDE ring residual` 语义，应由 canonical nearest radius 计算；candidate 的 point-ring residual 不因此改名或混用。
5. deployable signatures 与 truth firewall 不变；oracle truth 仍只决定 gate，不决定 update radius。
6. 不实现 DD-LMS/DD-RLS、smooth weight、performance driver 或新损伤。

## 必须新增的失败先行测试

- 先写一个旧代码必失败的分叉点，例如 `z=0.9+0j`：nearest constellation point 属外环，而 canonical nearest radius 为内环。
- 固定两种 RDE error 的符号相反：canonical 为负、旧 point-ring 路径为正；证明测试确实能捕获缺陷。
- 分别覆盖 plain、cheap、candidate、oracle 的 update target；同时保留 all-one=plain、zero=W0、cheap 单特征退化、一步手算、LS/SU(2)、paired hash 与 truth firewall。

## 交付与退出

- 只改 Ch4 seam、唯一测试和 correctness receipt/README/contract 中直接受影响的字段；不改 `common/`、`params.py`、治理、论文正文或性能资产。
- fresh 运行目标 pytest、`run_smoke.py`、task-control validator 与 `git diff --check`；记录命令和关键数字。
- receipt 仍必须写 `CORRECTNESS_ONLY / NO_METHOD_SIGNAL`。
- 若修复后无法同时保持 canonical update、candidate gate 合同和退化关系，回报 `BLOCKED`，不得改合同绕过。
- 一次 commit、不 push；最终回报 commit、改动、测试/smoke 数字和残余 blocker。
