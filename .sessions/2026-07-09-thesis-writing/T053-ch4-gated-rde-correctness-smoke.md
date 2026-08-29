# Task Brief: Ch4 gated-RDE implementation and correctness smoke

> 来源: S028 / D045 | 产出位置: `projects/simulation/explore/ch4-apsk-ring-gated-rde/` 与 `projects/simulation/tests/test_ch4_apsk_ring_gated_rde.py`
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

在独立 explore seam 实现 Q-C4-2 的最小可验证算法族并运行 correctness-only smoke：相同 2×2 pilot-LS 初值后的 plain RDE、native-ring-residual hard gate、双证据 hard-gated RDE candidate v1，以及只用于测试上界的 oracle gate。目标是证明公式、信息边界、退化行为和 paired realization 正确；本包不寻找性能增益、不形成 Go/Kill。

## 必读与启动

1. 根 `AGENTS.md`、topic-index、D045、本 brief，先运行 task-control validator。
2. `sim-preflight` 全部规则、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、`reference/sim-template/{config.py,experiment.py,evaluate.py,verify.py}`。
3. `projects/thesis-fso/apsk-front-end-groundwork/step4a-paper-feasibility.md`。
4. 本地 canonical RDE/RLS-CMA/RDE fulltext/read notes，尤其 `papers/doi/10.1109_jlt.2009.2021961/content.md` 与相应 read note；必须在 contract 中记录实际采用更新式的论文、页码/式号及本实现转写。
5. 只读借鉴：`pilot-jones-complex-repair/pilot_and_baselines.py`、`pilot-jones-temporal-adjudication/temporal_channel.py`、`common/_modulation.py` 的 APSK 点集、P09 nearest-point residual。不得复用公共 `_cma.py` 的已知错误更新式。

## 冻结对象

- 平台：DP-(8,8)-16APSK；固定 memoryless single-tap `J∈SU(2)`；两支路等方差 circular AWGN；有限正交 pilot prefix；payload symbol-rate samples。
- 关闭：GG fading、时变 SOP、CFO/CPE/linewidth、filter/IQ skew、PDL/PMD/FIR、LDPC、量化。
- Candidate v1：每个输出支路以 nearest-symbol normalized distance 与所属 ring normalized residual 同时过阈值，才允许该支路 canonical RDE row update。
- Cheap gate：只用 native ring residual 的单阈值 hard gate。
- Smooth weight、DD-LMS/DD-RLS 只保留接口/后续 comparator 说明；除非不扩包即可正确实现，否则本 correctness 包不必实现。
- truth 只允许在 oracle arm 和离线诊断；candidate/cheap/plain 运行接口不得接收 TX symbols、true Jones、true SNR 或 evaluation BER。

## 最小文件与测试合同

建议新增 `mve_contract.yaml`、`core.py`、`run_smoke.py`、`README.md` 和唯一 pytest 文件；不得修改 `common/`、`params.py` 或既有实验。

必须测试：

1. `(8,8)-16APSK` mapping、ring identity 与最近点一致。
2. 随机矩阵满足 unitary 且 `det(J)=1`；identity/noiseless 与 random-J/noiseless 的 LS 恢复误差达数值精度。
3. canonical RDE 一步更新与手算复数结果一致；维度、共轭和更新符号由测试固定。
4. all-one candidate gate 与 plain RDE bitwise/数值一致；zero gate 保持 `W0`；cheap gate 是 candidate 的严格单特征退化。
5. hard gate 边界确定、两项 score 非负有限；oracle truth 不进入 deployable signatures。
6. 所有 arms 共用完全相同的 symbols/J/noise/LS W0，seed 与 realization hash 写入 smoke receipt。
7. 输出 `z/G_eff/Sigma_n/flags/constellation_id/labeling_id` seam 至少形状、dtype、有限性正确。

Smoke 仅允许 identity/noiseless、random-J/noiseless、一个预注册 high-SNR correctness cell；不得循环搜索 SNR/pilot/阈值，不得以 BER 差异作结论。阈值可用显式固定测试值，只证明 gate 能开/关。

## 交付与退出

- 输出机器可读 receipt（参数、seed、git state、测试结果、realization hash）与简短 README，明确 `CORRECTNESS_ONLY / NO_METHOD_SIGNAL`。
- 运行目标 pytest 与最小 smoke；记录实际命令和结果。
- `git diff --check`，只提交一次。
- 若 canonical 式号无法从本地证据冻结、LS correctness 失败、truth firewall 无法隔离或公共资产必须被修改，立即 `BLOCKED`，不要调参绕过。
- 最终只回报 commit、文件、测试/smoke 数字、公式 authority、遗留 blocker；不声称性能改善。
