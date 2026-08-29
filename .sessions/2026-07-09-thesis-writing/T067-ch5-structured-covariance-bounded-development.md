# Task Brief: Ch5 structured-covariance 有界 BER/GMI 开发

> 来源: S028 / D048 / T051–T057 / T060–T066 / V022 | 产出位置: `projects/simulation/explore/ch5-apsk-structured-covariance/` 与 `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-bounded-development.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 10
  action_class: CH5_STRUCTURED_COVARIANCE_BOUNDED_DEVELOPMENT
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在 V022 已确认自然 residual covariance 的共同 DP-(8,8)-16APSK 星地相干链上，完成一次最多两轮、预注册的 B1/B2/B3/C1 同预算 BER/GMI 开发，自动选择最简真实胜者并给出 `PROVISIONAL` 等级。不得把 occurrence 当性能，不得增加新损伤、第三轮或完整 LDPC 网格。

## 启动门

1. 先运行 task-control validator；完整读取 D041、D048、T051/T054/T057/T060/T063/T065/T066、V022、`step4a-paper-feasibility.md`、occurrence manifest/raw/aggregate/receipt、bridge、methods、codec_metrics 与三份 Ch5 tests。
2. 遵守 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、TDD 与 verification-before-completion。先写 `development_manifest.yaml` 和失败判据，再写测试/runner。
3. 只修改 Ch5 独立 explore、对应 tests、指定 Groundwork 报告与必要 usage log；不改 `common/`、`params.py`、Ch3/Ch4 core、Skill/controller 或论文正文。

## 共同链与公平性

- 固定 T066 物理链和参数：DP-(8,8)-16APSK、memoryless random unitary Jones、moderate GG `4.0/1.9`、2.5 GBd、1 MHz residual CFO、150 MHz/s slope、10 kHz linewidth、plain RDE `mu=1e-3/Np=4`、Ch3 DA pilots spacing 4、无 PDL/PMD/FIR。
- 每个 window 仍为 256 observation symbols；64 个 pilots 各点每偏振 4 次，剩余 192 symbols 为 payload。模型只由本 window known pilots 拟合；payload truth 只进入离线 BER/GMI 评估。
- 所有臂共享相同 pilots、pilot-estimated means、floor=`1e-10`、LLR clip=`30`、payload、随机 realization 和 bootstrap clusters；cross-polarization sample pooling 关闭。
- arms：B1 per-ring scalar；B2 per-ring R/T hard pooling；B3 per-point full 2x2 + generic isotropic shrinkage；C1 per-point R/T + `lambda=kappa/(n_k+kappa)`。

## Round 1：单 cell 超参数与方法信号

- cell：与 T066 相同的 moderate/15 dB；64 windows，seeds `3000..3063`。
- development split：tune windows `0..31`，held-out evaluation `32..63`。只允许 tune 集的 payload GMI 选择超参数；evaluation 不得参与选择。
- C1 `kappa` grid=`[0,1,4,16,64]`；B3 shrinkage grid=`[0,0.25,0.5,0.75,1]`。B1/B2 无调参。并列时选择更强 shrinkage/更简单 recipe，不按 evaluation 挑值。
- primary：每个 evaluation window 的 GMI 与 hard-decision BER；以 window-cluster paired bootstrap（PCG64 seed=`2026083002`、2000 resamples）给 C1/B2/B3 相对 B1、C1 相对 strongest(B2,B3) 的均值差和 95% CI。
- secondary：held-out NLL、covariance condition/floor rate、per-point counts、runtime，只解释机制，不代替 BER/GMI。

Round 1 terminal：

1. `C1_SIGNAL`：C1 相对 strongest B2/B3 的 GMI 差 CI lower `>0`，且 BER 差 CI upper `<=0`；进入 Round 2，C1 为 provisional winner。
2. `SIMPLE_MIGRATION_SIGNAL`：C1 不满足上项，但 B2 或 B3 相对 B1 的 GMI CI lower `>0` 且 BER CI upper `<=0`；选 B2/B3 中更简且指标不劣者进入 Round 2。不得因它是廉价替代而 Kill。
3. `GMI_ONLY_SIGNAL`：任一结构臂 GMI CI lower `>0`，但 BER 没有非劣证据；停止本任务于 supporting/coded-gate 建议，不运行 Round 2 SNR curve。
4. `NO_METHOD_SIGNAL`：没有结构臂相对 B1 的 GMI 或 BER 正向信号；关闭 C5-1，唯一下一步 C5-0 Step 2。
5. correctness/firewall/hash/split/finiteness 失败：`INVALID_TESTBED`，只做最小修复，不解释为方法失败。

## Round 2：固定胜者三点 BER/GMI 曲线

只在 `C1_SIGNAL` 或 `SIMPLE_MIGRATION_SIGNAL` 后运行。冻结 Round 1 的唯一 arm/超参数，不再调参：

- SNR=`[14,15,16] dB`；每点 32 windows；seeds 分别 `4000..4031`、`4100..4131`、`4200..4231`。
- 只比较 B1、B2、tuned B3、冻结胜者；若胜者即 B2/B3 不重复 arm。
- 报告每点 paired BER/GMI、95% window-cluster CI、wins、payload bits/errors 和 required-SNR 仅在三点可合法插值时给出。
- `PROVISIONAL_A/B`：胜者在至少 2/3 SNR 点 BER 差 CI upper `<0`，且 GMI 不劣；`PROVISIONAL_C`：只有局部 BER 或仅 GMI；`D`：Round 2 不稳定或无信号。

## 禁止与交付

- 禁止第二湍流级、第二 pilot budget、IQ/PDL/PMD/FIR、LDPC/FER grid、第三轮、临场扩 κ/shrinkage/SNR/seeds、删除强 comparator、把 development 写成 FINAL。
- 交付 manifest、raw/aggregate/receipt、runner/tests、`step4a-bounded-development.md` 和 usage log。fresh 跑 validator、全部 Ch5 tests、correctness smoke、实际被授权轮次、raw-only reducer/invariant probe、`git diff --check`。
- 最终一次 commit、不 push；回报 RED/GREEN、Round 1 全 arms 数字/CI、是否进入 Round 2、三点曲线、terminal、provisional winner/grade、唯一下一步。
