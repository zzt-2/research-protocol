# 湍流 FSO 载波同步仿真项目

> 创建: 2026-06-02 | 本文件是 projects/simulation/ 的全局文档

## 核心原则（TL-24）

所有论文结论必须从 `common.py` 实验提取。独立脚本/旧代码的结论需用 common.py 重验。

## 项目结构

```
projects/simulation/
├── SPEC.md          # 仿真参数唯一真相源（信号模型、方法参数、湍流配置）
├── common.py        # 公共基础设施（信道生成、均衡、载波恢复、BER 评估）
├── README.md        # 本文件
├── experiments/     # 实验脚本（全部基于 common.py）
├── results/         # JSON 数据输出
├── figures/         # 图表输出
├── archive/         # 旧代码归档（不可用于论文结论）
└── .omc/            # 运行时状态
```

## common.py 状态

- 版本: 656 行, 23.3K
- VV 公式: `unwrap(angle(avg))/M`（公式 A，已修正）— L173
- 关键函数: `generate_shared_realization`, `mmse_equalize`, `dpll_track`, `vv_cpr`, `bps_cpr`, `kf_pilot_recovery`, `ber_eval`, `resolve_qpsk`
- 教训遵循: TL-01（信号模型）、TL-09（P 矩阵跨块传递）、TL-13（共享信道实现）

## 实验脚本清单

### 基于 common.py 的实验（结论可直接引用）

| 脚本 | 用途 | 导入方式 | 数据产出 | 状态 |
|------|------|---------|---------|------|
| `multi_seed_sweep.py` | 5 方法 × 3 湍流 × 3 SNR × 10 seeds 主扫描 | `from common import *` | sweep_*.json | 当前 |
| `sim_nmse_turbulence_sweep.py` | NMSE × 3 湍流 × 5 SNR × 10 seeds (PROMPT-008 Gap1) | `from common import *` | nmse_turbulence_sweep.json | 当前 |
| `sim_dpll_omega_sweep.py` | DPLL ω_n × 3 湍流 × 3 SNR × 10 seeds (PROMPT-008 Gap3) | `from common import *` | dpll_omega_sweep.json | 当前 |
| `sim_nmse_expanded.py` | NMSE 扩展验证（3 湍流 × 5 SNR × 4 NMSE） | `from common import *` | nmse_expanded.json | 当前 |
| `sim_nmse_vs_ber.py` | NMSE vs BER 灵敏度分析 | `from common import *` | nmse_vs_ber.json | 当前 |
| `sim_nw_sweep.py` | VV/BPS Nw 窗口扫描 | `from common import(...)` | nw_sweep.json | 当前 |
| `sim_nw_sweep_low_snr.py` | Nw 低 SNR 补种子 | `from common import(...)` | nw_sweep_low_snr.json | 当前 |
| `bridge_ch3_ch4.py` | Ch3→Ch4 衔接实验（NMSE 对载波同步影响） | `from common import *` | bridge_ch3_ch4_results.json | 当前 |
| `reverify_D1D2.py` | D1/D2 重验（VV 公式修正后） | `from common import *` | reverify_D1D2_new_common.json | 当前 |
| `reverify_kf_internals.py` | KF 内部机制+导频设计+公平性重验（C4-08/09, P-05~07） | `from common import *` | reverify_kf_internals.json | 当前 |
| `vv_formula_head2head.py` | VV 公式 A vs B 对比 | `from common import(...)` | — | 当前 |
| `plot_snr_curves.py` | SNR 曲线绑图 | `from common import(...)` | — | 辅助 |

### 独立脚本（不依赖 common.py，结论需重验）

| 脚本 | 用途 | 位置 | 状态 |
|------|------|------|------|
| `sim_ch3_ber_closed_form.py` | BER 闭合解验证 | projects/thesis-figures/simulation/ | 独立，纯数学+MC |
| `sim_ch3_ber_bounds.py` | BER 上下界 | projects/thesis-figures/simulation/ | 独立，1 seed |
| `sim_ch3_strengthening.py` | 设计准则表 | projects/thesis-figures/simulation/ | 独立，纯解析 |
| `sim_cascade_corrected.py` | 级联退化（修正 VV） | projects/thesis-figures/simulation/ | 用 common.py 的 vv_cpr |
| `sim_cascade_robustness.py` | AR 预补偿 | projects/thesis-figures/simulation/ | 旧代码，1 seed |
| `sim_ch4_kf_pilot_h.py` | KF h 估计诊断+公平性 | projects/thesis-figures/simulation/ | 独立，新代码 VV-A |
| `sim_ch4_systematic_analysis.py` | Ch4 系统性分析 | projects/thesis-figures/simulation/ | 独立，30 trials |
| `sim_kf_stress_*.py` (6 个) | D1/D2/C4/C5/D3-D5 压力测试 | projects/thesis-figures/simulation/ | 旧 stress_common |

## 旧代码归档

`archive/` 目录包含已废弃的旧文件（stress_common.py 等）。这些文件的结论不可直接引用，需用 common.py 重验。

## 数据文件索引

| JSON 文件 | 大小 | 来源脚本 | 覆盖范围 |
|-----------|------|---------|---------|
| sweep_20260601_181320.json | 100K | multi_seed_sweep.py | VV/DPLL/KF/Fixed, 10 seeds |
| sweep_bps_10seed.json | 24K | multi_seed_sweep.py | BPS, 10 seeds |
| nmse_turbulence_sweep.json | 100K | sim_nmse_turbulence_sweep.py | NMSE × 3 湍流 × 5 SNR |
| dpll_omega_sweep.json | 20K | sim_dpll_omega_sweep.py | ω_n × 3 湍流 × 3 SNR |
| nmse_expanded.json | 75K | sim_nmse_expanded.py | NMSE 扩展 |
| nmse_vs_ber.json | 50K | sim_nmse_vs_ber.py | NMSE vs BER 灵敏度 |
| nw_sweep.json | 16K | sim_nw_sweep.py | Nw 窗口扫描 |
| nw_sweep_low_snr.json | 35K | sim_nw_sweep_low_snr.py | Nw 低 SNR |
| bridge_ch3_ch4_results.json | 16K | bridge_ch3_ch4.py | Ch3→Ch4 衔接 |
| reverify_kf_internals.json | ~50K | reverify_kf_internals.py | KF R/Q/P + 导频开销/放置 + 公平性 + block size |

## 与 CONCLUSIONS.md 的映射

CONCLUSIONS.md 每条结论的 `代码来源` 字段指向本文件中的脚本。标记为 `[common.py]` 的结论可直接写入论文；标记为 `[旧代码]` 或独立脚本的需先重验。
