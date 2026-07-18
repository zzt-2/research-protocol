# [S042] Batch 0 基线与参数域审计

> 2026-07-16 | Batch 0 | 状态：PARTIAL（可探索，但存在 CRITICAL 参数债务）

## 目标

在不改动 `params.py`、`common/`、既有结果和算法的前提下，审计当前 CMA-fade/SOP lock-swap 基线、参数域和 fixed/PI/swap 指标口径，为后续 Batch 1 提供可复用的 paired baseline。

## 运行与输入

| 动作 | 命令/输入 | 结果 |
|---|---|---|
| 参数审计 | `cd projects/simulation && ~/.venvs/torch/bin/python -c "from params import SimulationConfig,audit_params; print(audit_params(SimulationConfig()))"` | 成功，约 1.6 s |
| MVE smoke | `~/.venvs/torch/bin/python explore/cma-fade-divergence/mve_cma_vs_ml.py --smoke --n-symbols 20000` | 成功，约 20 s；1 场景×2 trials |
| 统一基线复核 | 读取 `results/cma-fade-divergence/prompt015_unified_baseline.json` | 30 trials 完整；未重跑 5M 长实验 |
| 参数域/Swap 复核 | 读取 `results/cma-fade-divergence/prompt030_domain_swap_audit.json` | 20 主审计记录 + 50 SOP sweep + 15 N sweep |

未修改任何源代码、参数和旧结果；没有开始 Batch 1。

## 参数审计

`audit_params(SimulationConfig())` 的真实汇总为：`total=74, OK=40, WARNING=24, CRITICAL=4, DEAD=6`。

### CRITICAL（禁止据此写正式结论）

- `kf.Q_fine_df = 2.5e9`，来源 `NO VERIFIED SOURCE — SPEC 未记录此覆盖行为`。
- `kf.q_params_weak.sigma2_turb = 1e-6`，来源 `NO VERIFIED SOURCE`。
- `kf.q_params_moderate.sigma2_turb = 1e-4`，来源 `NO VERIFIED SOURCE`。
- `kf.q_params_strong.sigma2_turb = 1e-3`，来源 `NO VERIFIED SOURCE`。

### 关键 WARNING/DEAD

- 当前统一单载波线宽 `cfg.system.LASER_LW=10000 Hz`（WARNING，Valjus sat.1553 约束说明）；本批 CMA/ML 结果实际采用该值。
- GG 当前 strong 域为 `(alpha,beta)=(4.2,1.4)`，旧历史域为 `(1.5,0.8)`；旧域只在 `prompt030` 中显式作为对照输入。
- `experiment.BLOCK=100` 为 WARNING 且无 verified source。
- `kf.q_params_*.kappa` 为 DEAD；B11 的 `CLW=500 kHz`、`BAUD_RATE=25 GBaud`、`PN_VARIANCE` 也为 DEAD，不能混入当前单载波结论。

## Smoke 结果

原始结果：`projects/simulation/results/cma-fade-divergence/mve_cma_vs_ml_smoke.json`。

- 场景：`danger_1e-2_1000Hz`、strong；实际 1 场景×2 seeds，`N=20000`。
- CMA divergence：`0/2`；ML divergence：`0/2`。
- BER 均值（短切片、仅 smoke）：CMA `8.0e-4`，ML `0`，oracle `0`，raw `0`。
- 该 smoke 只验证调用链/结果写入，不足以支持性能或机制结论。

## 统一基线：PROMPT-015

原始结果：`projects/simulation/results/cma-fade-divergence/prompt015_unified_baseline.json`。

### 实验契约

- `N=5,000,000`，late slice `[4,375,000, 5,000,000)`；30 paired seeds `[1000..1029]`。
- strong GG `(4.2,1.4)`，`f_G=30 Hz`，`SOP_RATE=4e-7 rad/sym`，`gamma_bar=100`（20 dB），QPSK。
- CMA `mu=1e-3`、11 taps、block 64；ML 11 taps、lr `0.005`、batch `1024`、20 epochs；oracle 为后验完美 CSI 参照。
- 每个 trial 的各方法都记录同一个 `shared_realization_seed`；独立核查得到 30/30 trials 共享信道 seed 一致。

### 30-seed 聚合（从每条 trial 原始 JSON 重算）

| 方法 | fixed-label BER 均值 | PI-BER 均值 | classification | diverged |
|---|---:|---:|---|---:|
| current-CMA | 0.483859 | 0.0213144 | clean-swap 25 / degraded-swap 5 | 0/30 |
| standard-CMA | 0.0921174 | 0.0168877 | normal 24 / clean-swap 4 / degraded-swap 1 / mixed 1 | 0/30 |
| ML-original | 0.496682 | 0.00775071 | clean-swap 29 / degraded-swap 1 | 0/30 |
| ML-aligned | 0.496679 | 0.00775147 | clean-swap 29 / degraded-swap 1 | 0/30 |
| oracle | 0.00659673 | 0.00659673 | normal 30 | 0/30 |

fixed-label 与 PI-BER 不能混写：ML 的 PI-BER 接近 oracle，但 fixed-label BER 约 0.497，属于标签 swap 口径下不可部署；standard-CMA 的 fixed-label 与 PI 也有巨大差异。PROMPT-015 的 paired Wilcoxon 只证明其预注册的 excess-PI-BER 比较，不能把 PI 优势改写成 fixed-label 增益。

## 参数域/Swap 复核：PROMPT-030

原始结果：`projects/simulation/results/cma-fade-divergence/prompt030_domain_swap_audit.json`。

主审计各域各 10 seeds：

| 域 | CMA fixed / PI | CMA 分类 | ML fixed / PI | Oracle fixed / PI |
|---|---:|---|---:|---:|
| old `(1.5,0.8)` | 0.476902 / 0.0349110 | clean 9, degraded 1 | 0.497500 / 0.00518776 | 0.00422096 / 0.00422096 |
| current `(4.2,1.4)` | 0.487999 / 0.0129577 | clean 9, degraded 1 | 0.499596 / 0.00004584 | 0.000018 / 0.000018 |

该结果不支持“current domain CMA 0/5 swap”的旧概括；在 10-seed、5M 记录中 current 域仍为 clean-swap 9/10、degraded-swap 1/10。SOP 单轴 sweep（current 域）显示 CMA fixed BER 从 SOP=0 的 `1.028e-4`、1e-7 的 `0.012867`，上升至 4e-7 的 `0.4880`、1e-6 的 `0.4979`；PI-BER 同期约为 `1.30e-2` 和 `6.82e-3`。这表明 SOP 速率是主要控制轴之一，但这些结果仍属现有探索结果，并非新方法验证。

## standard-CMA 与 current-CMA 实现差异

- `common/_cma.py:CMAEqualizer2x2.equalize`（约 L159–168）实际更新为 `mu * mean((R²-|z|²) * conj(r))`，不含 `z` 因子；应称 current/repository CMA implementation，不能称标准 Godard CMA。
- `prompt013_swap_mechanism_q2.py:_cma_deltas`（约 L300–311）的 `standard` 分支更新为 `mu * mean((R²-|z|²) * z * conj(r))`，显式含 Godard `z` 因子；其 `current` 分支复制 common 当前实现。
- `common/_cma.py` 文档称误差为 `e=R²-|z|²`，但梯度实现缺少复值 CMA 的 `z` 乘积；故 current 与 standard 不是同一算法的命名差异，而是更新方程不同。

公式来源已在 `common/_cma.py` 注释标注 Godard 1980 与 sat.1553 §6 Eq.(48/50)；本批未修改该实现。

## 口径与可比性审计

- **可比**：同一 JSON trial 内 CMA/ML/oracle 使用同一 shared realization seed；同一 QPSK、SOP、GG 域和 late slice。
- **必须分列**：fixed-label BER、PI-BER、swap classification；PI 通过后验输出排列，属于第二口径，不等于可部署固定标签。
- **oracle**：完美 `h + theta` 的后验上界，不是可部署方法；只作上界参照。
- **fade 指标**：现有 PROMPT-015 记录 `classification`、`abs_corr`、`diverged`，但没有统一的“fade 后恢复延迟”字段；因此本批不能声称已完整复现 recovery-delay 指标。
- **发散**：PROMPT-015 30 trials 中各方法 `diverged=0`，不能由此推出没有长序列/深衰落发散，只能说明该固定契约下未触发代码中的发散阈值。

## Batch 0 结论

**PARTIAL：基线可用于候选族探索，但尚不能作为正式论文证据或直接授权 Batch 1。**

已确认的可复用事实是：paired 信道与 fixed/PI/swap 口径可重算，standard/current CMA 实现差异明确，当前 strong 域与旧域的 swap 行为不能沿用旧简报概括。阻断因素是 4 个 CRITICAL KF 参数与部分 WARNING 参数仍无来源；它们不直接进入 PROMPT-015 CMA/ML 主路径，但说明全局参数域尚未完全闭合；此外 recovery-delay 尚未有统一字段。

## Batch 1 开始条件（仅条件，不做新方法判断）

Batch 1 只有在以下条件满足后才能开始：

1. 固定并记录 Batch 0 的 shared realization、seed、N、SOP、GG 域和 fixed/PI/swap 口径；
2. 对 Batch 1 所用参数逐项确认是否进入 CMA/ML 路径；若触及 CRITICAL KF 参数，先完成来源推导并更新审计；
3. 增加或明确统一的 fade/recovery-delay 定义，避免只用 BER 或 PI-BER 代替；
4. 保留 current-CMA 作为实现审计项，standard-CMA 作为合法 Godard 对照，二者不得互换命名。

## 决策引用

- D045：候选族先地图、再批量排跑；Batch 0 是共同基线。
- 无新增方向决策。

## 范围确认

- 本轮是否在 scope boundary 内：是。
- 未修改 `params.py`、`common/`、旧结果；未运行 Batch 1。

## 后续

由主控根据本审计决定是否满足 Batch 1 前置条件；本文件中的所有数字在参数债务未解决前标为 provisional。
