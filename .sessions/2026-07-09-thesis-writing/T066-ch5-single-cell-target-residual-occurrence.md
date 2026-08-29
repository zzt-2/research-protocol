# Task Brief: Ch5 单格 target-residual occurrence smoke

> 来源: S028 / D047 / T060–T065 / V021 | 产出位置: `projects/simulation/explore/ch5-apsk-structured-covariance/` 与 `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-target-occurrence.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 9
  action_class: TARGET_RESIDUAL_BRIDGE_OCCURRENCE_SMOKE
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在 T065 已独立 PASS 的真实 `Ch4 demux → per-pol Ch3 DA CPR → known-pilot residual` bridge 上，只运行一个预注册 cell，判断共同星地相干平台中是否自然出现足以支持 C5-1 的非圆、点相关 residual covariance。不得调参、不得换 cell、不得加入新损伤、不得进入 C5-1 性能开发或 LDPC/FER grid。

## 启动门与执行纪律

1. 先运行 task-control validator；完整读取 T055、T060–T065、V021、D047、`occurrence_contract.yaml`、bridge/estimator/codec 实现与现有两份 Ch5 tests。
2. 触发并遵守 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md`、`test-driven-development` 与 `verification-before-completion`。先冻结 manifest 和失败判据，再写测试和实现，再只运行一次正式 cell。
3. 只允许修改 Ch5 独立 explore 目录、对应 Ch5 tests、指定 Groundwork 报告与必要 usage log；不得改 `common/`、`params.py`、Ch4 core、Ch3 算法、Skill/controller 或论文正文。
4. 可对 bridge 做的唯一泛化是把 correctness fixture 的“首 32 个 pilot”改为由显式 pilot indices/spacing 构造 balanced known pilots；不得借此改变物理链、arm、损伤或 CPR。

## 冻结的唯一 cell

| 字段 | 冻结值 |
|---|---|
| modulation / polarization | DP-(8,8)-16APSK |
| Jones | 每 window 一个静态、随机、memoryless 2×2 unitary Jones；无 PDL/PMD/FIR |
| scalar chain | shared moderate GG `alpha=4.0, beta=1.9` + `f_residual=1e6 Hz` + `f_dot=150e6 Hz/s` + Wiener `linewidth=10 kHz` |
| noise / SNR | Jones 后两偏振等方差 circular AWGN，`15 dB` |
| symbol rate | `2.5 GBd`，即 `Ts=4e-10 s` |
| observation | 每 window `N=256` symbols；GG block=`256` |
| Ch4 acquisition | `Np=4` orthogonal pilots；frozen arm=`plain canonical RDE, mu=1e-3, thresholds=null` |
| Ch3 pilots | spacing=`4`，每 window 每偏振 64 个 known pilots；16 labels 各 4 次，两个偏振都 balanced，可用固定循环移位避免逐样本相同 |
| windows / seeds | 64 windows；`seed=2000..2063`，每 window 独立；不得因结果重选 |
| split | calibration windows `0..31`；evaluation windows `32..63`；不得交叉使用 |
| covariance floor | 所有诊断统一 `1e-10`，不调 |
| bootstrap | evaluation window 为 cluster，PCG64 固定 seed `2026083001`，2000 resamples，95% CI |

这些数值来自已冻结共同平台与 D047 的经典 Ch4 anchor；本任务不得增设第二 SNR、第二湍流级别、更多 pilot budget 或 synthetic anisotropy。

## 必须先写成测试的语义

1. 64 个 pilot indices 必须精确为 `0,4,...,252`，每偏振 16 labels 各出现 4 次；known mask、symbols、labels 一致。
2. 64 windows 的 frozen config/arm 完全相同，seed/window/hash 不混淆；同一 window 的 acquisition 和 observation 保持 T065 验证过的连续 realization。
3. calibration/evaluation 严格分离；任一 evaluation residual 不得参与 covariance 拟合、阈值或分支选择。
4. bootstrap 只重采样 32 个 evaluation windows，不把 pilot 当独立 cluster；固定 seed 可逐字复现。
5. 用合成 unit fixture 验证 D1/D2/D3 的符号、CI 和 terminal 逻辑；fixture 只测 reducer，不得进入正式科学输出。

## 三个预注册诊断

对每个 known-pilot residual `e=z-x`，按对应 constellation point 角度旋转：`u=e*exp(-j angle(x))`，`r=Re(u)`、`t=Im(u)`。两个 polarization × 两个 ring 共 4 组。

1. **D1 radial/tangential log-variance ratio**：每组统计 `log(var(r)/var(t))`。对 4 组使用 Bonferroni simultaneous 95% window-cluster bootstrap CI（每侧 quantile `0.00625/0.99375`）。任一 CI 不含 0，D1 为 detectable。
2. **D2 rotated off-diagonal correlation**：每组统计 `rho=cov(r,t)/sqrt(var(r)var(t))`，使用同样 4 组 simultaneous CI。任一 CI 不含 0，D2 为 detectable。
3. **D3 held-out covariance NLL**：仅用 calibration windows，按 polarization 分别拟合零均值的 B1 per-ring scalar covariance 与 per-point full 2×2 covariance，统一 floor；在每个 evaluation window 上计算平均 Gaussian NLL improvement `NLL_B1-NLL_full`。对 32 个 window 值做普通 95% cluster-bootstrap CI；lower CI `>0` 才算 D3 detectable。

报告每个 group/window 的样本数、point counts、点估计、CI、bootstrap seed/resamples、config/realization/bundle hashes，不得只写 PASS/FAIL。

## 唯一裁决与停机

- 任一 D1/D2/D3 detectable：`DETECTABLE_OCCURRENCE`。只说明共同链存在非圆或点相关 covariance headroom；不得声称 C5-1 已改善 BER/GMI/FER。唯一下一步是由主控另派 C5-1 bounded development。
- D1/D2 四组 CI 全含 0，且 D3 lower CI `<=0`：`NO_DETECTABLE_OCCURRENCE`。立即关闭 C5-1 target-platform 路线；不运行第二 cell、不调参数、不加 IQ/PDL/PMD/FIR/synthetic anisotropy。唯一下一步是 C5-0 候选级 GW Step 2。
- correctness、firewall、split、hash 或数值有限性失败：`INVALID_TESTBED`。只返回最小 correctness 修复，不解释为方法失败。

正式 cell 只允许一次。若进程意外中断且没有完整 scientific artifact，可从 manifest 同配置重启；必须记录中断，不能更换 seed/config。

## 交付与回报

至少交付冻结 manifest、raw window records、aggregate/receipt、`step4a-target-occurrence.md`、必要测试与 usage log。fresh 跑 task validator、相关 Ch5 tests、correctness smoke、occurrence 一次和 `git diff --check`。最终一次 commit、不 push，回报：commit、RED/GREEN、64-window 完成数、D1/D2 四组 CI、D3 improvement CI、terminal、是否允许进入 bounded development、唯一下一步。
