# Task Brief: Ch4 gated-RDE 预注册有界开发

> 来源: S028 / D041 / D046 / T052–T053 / T056 / T058 | 产出位置: `projects/simulation/explore/ch4-apsk-ring-gated-rde/` 与唯一对应测试
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 8
  action_class: GW_STEP4A_D_BOUNDED_DEVELOPMENT
  mission_checkpoint: CP008
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在已经独立通过 correctness 的 Ch4 seam 上，补齐一个独立 performance driver 与冻结 manifest，运行预注册 Round 1；只有满足本文门槛才运行 Round 2。输出 `PROVISIONAL A/B/C/D/F`，不得扩网格、临时换损伤或把 development 写成 final method signal。

## 启动与边界

1. 先完整读取本 brief、topic-index 当前控制、D046、T052 §4.1、T056 §7、现有 seam 全文件；运行 task-control validator。
2. 本任务触发 `sim-preflight`、`stages/gw-feasibility.md` 维度 D、`code-quality.md` 和 simulation test templates，按其纪律执行。不得改 `common/`、`params.py`、Skill/controller 或论文正文。
3. 先 fresh 跑现有 7 tests 与 correctness control；失败即 `F/INVALID`，不进入 development。
4. 物理切片只含 DP-(8,8)-16APSK、固定 memoryless unitary 2×2 Jones、equal circular AWGN、有限正交 pilots。关闭 GG、CFO/相噪、时变 SOP、IQ/滤波/FIR、PDL/PMD/CD、LDPC。

## 冻结矩阵

Correctness control：`J=I`、无噪声、`Np=16`、payload `512`、seed `53000`、`mu=1e-4`、thresholds `0.2`。PASS 要求 LS 与全部 arm BER=0，四个 gate arm 输出一致、全 gate 开、`W0≈I`、hash 一致、无 NaN/Inf。

Development payload 固定 `8192`：

| Round | cell | SNR/dB | pilots |
|---|---|---:|---:|
| 1 | D1 | 14 | 2 |
| 1 | D2 | 18 | 2 |
| 1 | D3 | 14 | 8 |
| 2 | D4 | 14 | 4 |
| 2 | D5 | 18 | 4 |
| 2 | D6 | 18 | 8 |

- Tune seeds `54101–54103`，只在 D1–D3 使用。
- Development-eval seeds `54201–54206`，全部进入所运行 cells。
- future confirmation seeds `54301+` 保留，严禁本任务读取。
- 所有 arm 共享同一 symbol/Jones/standardized-noise realization 与 realization hash。

## Arms、公平性与 truth firewall

1. `LS-only`：公共 pilot-LS `W0`，payload 不更新。
2. `plain RDE`：公共 `W0`，canonical update，每个机会都更新。
3. `cheap`：只以 canonical native-ring score 硬门控同一 update。
4. `candidate`：point-ring score 与 nearest-symbol decision score 双门控同一 update。
5. `oracle`：TX label 只决定 gate，永不决定 update radius、step、tuning 或 deployable 输出。
6. `update-count-matched plain`：按 gated arm 每 256 symbols、每偏振实际 accepted count，用独立确定性 RNG 在同 block 抽取相同数量的 plain updates，复用 gated arm 的 `mu`。

主传统对手 `B0*=min(LS-only,tuned plain RDE)`。若 cheap 与 candidate 同等级且 candidate 相对 cheap 增益 `<5%`，方法身份收缩为 cheap recipe，不为双门身份补网格。DD-LMS/RLS 不在本 development 实现；只有出现可确认信号时，后续 confirmation 才补一个等价经典强对手。

## 冻结调参与指标

每个 arm 最多 9 个配置，只看 tune split，并选一个跨 cells 的全局配置：

- plain/oracle：`mu=geomspace(1e-5,1e-3,9)`；
- cheap：`mu∈{3.16e-5,1e-4,3.16e-4}` × `tau_r∈{0.05,0.2,0.8}`；
- candidate：相同 3 个 `mu` × `(tau_r,tau_d)∈{(.05,.05),(.2,.2),(.8,.8)}`；
- objective：九个 tune realizations 上 Jeffreys-smoothed `mean(log10 BER)`；1% 内并列优先 accepted fraction 更高，再选更小 `mu`。

必须保存逐 seed raw BER/error counts、整帧与前/后半 BER、oracle headroom、gap recovery、ring/decision/combined AUROC、wrong-symbol update contamination、accepted fraction/count、count-matched 差、W norm/finite flags、所有配置与 hashes。每 cell 聚合错误数 `<100` 时标记 `UNDERPOWERED`，不得报百分比等级。

## 两轮停机与分级

Round 1 后任一成立即停：

- correctness、baseline、公平性或 truth firewall 失败：`F/INVALID`；
- 三格中 oracle 相对 `B0*` 均无 `>=10%` headroom；
- combined AUROC 三格均 `<=0.55`；
- gated arm 无任何一格回收 `>=20%` oracle gap 且不优于 count-matched；
- 所有 apparent gain 被 count-matched 吸收。

进入 Round 2 的最低条件：至少一个 gated arm 在一格相对 `B0*` BER 改善 `>=10%` 且 6 个 eval seeds 至少 5 个同向；或回收 `>=20%` oracle gap 且 AUROC `>=0.60`。cheap 有信号而 candidate 无增量时，以 cheap pivot 进入 Round 2。

- `A`：至少 3/6 cells 改善 `>=20%`，覆盖两 SNR、两 pilot budgets；paired bootstrap 95% 下界>0；无其他 cell >10% 退化；至少两格胜 count-matched `>=5%`；AUROC `>=.65` 且 contamination 降低 `>=20%`。
- `B`：至少两格改善 `>=10%`，一格 95% 下界>0；无系统性 >10% 伤害，count-matched/contamination 支持选择质量。
- `C`：仅局部 5–10%、单格或 CI 触零。
- `D/STOP_NO_METHOD_SIGNAL`：全部 `<5%`、方向不稳、只有代理改善或收益被 cheap/count-matched 完全吸收。
- `F` 只用于实现、truth、baseline、统计管线无效，不把无 headroom 写成 F。

## 交付

- 独立 driver、冻结 manifest、raw JSON、聚合报告、必要测试与 receipt；不覆盖 correctness receipt 的语义。
- 报告清楚回答：是否进入 Round 2；胜者是 candidate/cheap/none；相对 `B0*` 的 BER 提升；是否被 update-count 吸收；当前 provisional grade；唯一下一动作。
- 单线程总运行硬上限 15 分钟；超时只优化执行方式，不削 seed/判据、不扩网格。
- fresh 运行 validator、tests、driver 与 `git diff --check`。一次 commit、不 push，回报 commit、运行时间、关键数字和 residual blocker。
