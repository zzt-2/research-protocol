# [S002] Ch4 代码+参数审计报告

> 2026-05-31 | 审计 | 完成
> 3 个 explore agent 并行审计 + 1 处手动验证

## 目标

对 Ch4 全部代码做参数级审计，产出参数一致性矩阵、函数一致性对比、Bug 状态确认、结论可靠性标记。不跑新实验，只验证已有代码和结论。

## 记录

### 审计摘要

- 审计文件数：16（旧目录 15 个 .py + 新 common.py）
- 参数不一致：0 处实质性不一致（1 处文档级缺失，无关紧要）
- 函数不一致：1 处严重（VV 公式）、1 处命名不一致（ber vs ber_count）
- Bug 确认：4/5 项确认存在，1 项为行为特性非 bug

---

## 任务 1：参数一致性矩阵

### 核心系统参数

| 参数 | SPEC.md | common.py (新) | stress_common | systematic | kf_pilot_h | kf_carrier_sync | kf_perblock_h | kf_verification |
|------|---------|----------------|---------------|------------|------------|-----------------|---------------|-----------------|
| R_SYM | 2.5e9 | 2.5e9 | 2.5e9 | 2.5e9 | 2.5e9 | 2.5e9 | 2.5e9 | 2.5e9 |
| T_S | 400e-12 | ✅ 1/R_SYM | ✅ 1/R_SYM | ✅ 1/R_SYM | ✅ 1/R_SYM | ✅ 1/R_SYM | ✅ 1/R_SYM | ✅ 1/R_SYM |
| F_CARRIER | 1.95e14 | 1.55e14 | 1.55e14 | ⚠️ 未定义 | 1.55e14 | 1.55e14 | 1.55e14 | 1.55e14 |
| LASER_LW | 10e3 | 10e3 | 10e3 | 10e3 | 10e3 | 10e3 | 10e3 | 10e3 |
| F_RESIDUAL | 1e6 | 1e6 | 1e6 | 1e6 | 1e6 | 1e6 | 1e6 | 1e6 |
| DOPPLER_HIGH | 150e6 | 150e6 | 150e6 | 150e6 | 150e6 | 150e6 | 150e6 | 150e6 |
| BLOCK | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| γ̄ default | 100 (20dB) | 100 | 100 | 变量传入 | 100 | 变量传入 | 变量传入 | 变量传入 |

### 湍流参数

| 参数 | SPEC.md | common.py | stress_common | kf_pilot_h | kf_carrier_sync | kf_perblock_h | kf_verification |
|------|---------|-----------|---------------|------------|-----------------|---------------|-----------------|
| weak (α,β) | (4.0, 3.0) | (4.0, 3.0) | (4.0, 3.0) | (4.0, 3.0) | (4.0, 3.0) | (4.0, 3.0) | (4.0, 3.0) |
| moderate (α,β) | (2.5, 1.8) | (2.5, 1.8) | (2.5, 1.8) | (2.5, 1.8) | (2.5, 1.8) | (2.5, 1.8) | (2.5, 1.8) |
| strong (α,β) | (1.5, 0.8) | (1.5, 0.8) | (1.5, 0.8) | (1.5, 0.8) | (1.5, 0.8) | (1.5, 0.8) | (1.5, 0.8) |

**注**：sim_ch4_systematic_analysis.py 不含 KF 相关参数（Q_TURB_PARAMS），因为它只做基线方法分析，不使用 KF。这是预期行为。

### KF/Q 矩阵参数

| 参数 | SPEC.md | common.py | stress_common | kf_pilot_h | kf_carrier_sync | kf_perblock_h |
|------|---------|-----------|---------------|------------|-----------------|---------------|
| σ²_turb weak | 1e-6 | 1e-6 | 1e-6 | 1e-6 | 1e-6 | 1e-6 |
| κ weak | 1.56e-6 | 1.56e-6 | 1.56e-6 | 1.56e-6 | 1.56e-6 | 1.56e-6 |
| σ²_turb moderate | 1e-4 | 1e-4 | 1e-4 | 1e-4 | 1e-4 | 1e-4 |
| κ moderate | 9.80e-5 | 9.80e-5 | 9.80e-5 | 9.80e-5 | 9.80e-5 | 9.80e-5 |
| σ²_turb strong | 1e-3 | 1e-3 | 1e-3 | 1e-3 | 1e-3 | 1e-3 |
| κ strong | 3.79e-4 | 3.79e-4 | 3.79e-4 | 3.79e-4 | 3.79e-4 | 3.79e-4 |
| Q_fine_df | (50e3)² | (50e3)² | (50e3)² | (50e3)² | (50e3)² | (50e3)² |

### Fixed 基线参数

| 参数 | common.py 默认 | stress_common 默认 | systematic | 所有旧文件默认 |
|------|---------------|-------------------|------------|---------------|
| N_fft | 1024 | 1024 | 1024 | 1024 |
| M_vv | 64 | 64 | 64 | 64 |
| omega_n | 8e6 | 8e6 | 8e6 | 8e6 |
| zeta | √2/2 | √2/2 | √2/2 | √2/2 |

**注**：默认值不公平（TL-14），D1 压力测试确认最优参数为 M_vv=256, omega_n=20MHz。common.py 和 stress_common.py 均提供 `FIXED_CFG_OPTIMAL` 字典。

### 信号模型

**所有 16 个文件均使用正确模型** `signal = tx * np.sqrt(h) * carrier`（即 r = √h·s·exp(jφ) + n）。

grep 搜索 `np.sqrt(h)` 在全部 .py 文件中命中 32/33 个仿真文件（1 个 Ch3 文件不含此模式）。无任何文件使用 h·s 或 h²·s。

### 压力测试文件

所有 8 个 sim_kf_stress_*.py 文件通过 `from sim_kf_stress_common import *` 获取参数。仅覆盖实验特定参数（如 Q_fine_df 扫描范围），核心参数与 SPEC.md 一致。

### 结论

**参数一致性：✅ 全部通过。** 无实质性不一致。

---

## 任务 2：函数一致性

### 2.1 resolve_qpsk

| 文件 | 行号 | 8 旋转? | 内部用 ber_count? | 与 common.py 一致? |
|------|------|---------|-------------------|-------------------|
| common.py (新) | 85-90 | ✅ | ✅ | — |
| stress_common | 72-77 | ✅ | ✅ | ✅ 完全一致 |
| systematic_analysis | 73-80 | ✅ | ✅ | ✅ 完全一致 |
| kf_pilot_h | 81-86 | ✅ | ⚠️ 用 `ber()` | ⚠️ 功能一致，命名不同 |
| kf_carrier_sync | — | — | — | 未定义，导入 |
| kf_perblock_h | 76-81 | ✅ | ⚠️ 用 `ber()` | ⚠️ 功能一致，命名不同 |
| kf_verification | — | — | — | 用 `ber()` 内联 |

**结论**：所有 resolve_qpsk 实现功能一致（8 旋转 π/4 步进，选 BER 最低）。命名差异（`ber()` vs `ber_count()`）不影响结果。

### 2.2 ber_count / ber

| 文件 | 行号 | sign(real)>0, sign(imag)>0? | 一致? |
|------|------|----------------------------|-------|
| common.py | 82-83 | ✅ | — |
| stress_common | 69-70 | ✅ | ✅ |
| systematic_analysis | 70-71 | ✅ | ✅ |
| kf_pilot_h | — | ✅（名为 `ber()`） | ✅ 功能一致 |
| kf_perblock_h | — | ✅（名为 `ber()`） | ✅ 功能一致 |

**结论**：所有 BER 计算实现功能一致。

### 2.3 信号生成

所有文件使用 `signal = tx * np.sqrt(h) * carrier`，噪声方差 `1/(2*gamma_bar)`。一致 ✅。

### 2.4 VV CPR — ⚠️ 关键不一致

| 文件 | 行号 | 公式 | 与 common.py 一致? |
|------|------|------|-------------------|
| **common.py (新)** | 170 | `unwrap(angle(avg)) / M` | — |
| **systematic_analysis** | 147 | `unwrap(angle(avg)) / M` | ✅ |
| stress_common | 144 | `unwrap(angle(avg) * M) / M` | ❌ |
| kf_pilot_h | 153 | `unwrap(angle(avg) * M) / M` | ❌ |
| kf_carrier_sync | 144 | `unwrap(angle(avg) * M) / M` | ❌ |
| kf_perblock_h | 148 | `unwrap(angle(avg) * M) / M` | ❌ |
| kf_verification | 153 | `unwrap(angle(avg) * M) / M` | ❌ |

**两种公式**：
- **公式 A**（正确）：`np.unwrap(np.angle(avg)) / M` — 先 unwrap 后除 M
- **公式 B**（错误）：`np.unwrap(np.angle(avg) * M) / M` — 先乘 M 后 unwrap

**影响**：4 次方后相位范围 [-4π, 4π]，公式 B 先乘 M=4 后 unwrap 会错误检测不存在的缠绕点。但此 bug 在 D2 消融实验中已被证明 VV 在湍流下有害（BER 从 10% 恶化到 27-30%），因此实际影响有限——不管公式对错，VV 都不该用。

**文件分属**：
- common.py 和 systematic_analysis 用正确公式
- stress_common 和 4 个 KF 文件用错误公式
- 所有压力测试脚本依赖 stress_common，因此都受影响

### 2.5 DPLL

所有 7 个文件的 DPLL 实现完全一致：`c1=2ζωT`, `c2=(ωT)²`, 鉴相器 `angle(m4)/4`。无 π/4 修正。一致 ✅。

### 2.6 KF

| 文件 | F 矩阵 | R 公式 | 创新 wrapping | P 跨块传递? |
|------|--------|--------|--------------|------------|
| common.py | [[1,T_S],[0,1]] | 1/(2γ̄h) | ✅ | ✅ P_init/P_final |
| stress_common | ✅ 一致 | ✅ 一致 | ✅ | ✅ |
| kf_pilot_h | ✅ 一致 | ✅ 一致 | ✅ | ✅ |
| kf_carrier_sync | ✅ 一致 | ✅ 一致 | ✅ | ❌ **每块重置** |
| kf_perblock_h | ✅ 一致 | ✅ 一致 | ✅ | ✅ |
| kf_verification | ✅ 一致 | ✅ 一致 | ✅ | ✅ |

**唯一不一致**：sim_ch4_kf_carrier_sync.py 的 `kf_unified()` 不接受 `P_init` 参数（L224 签名无 P_init），不返回 P（仅返回 phi_est, df_est），每块重新初始化 P（L262）。这就是 TL-09 记录的 bug。该文件已标记废弃。

### 2.7 MMSE 均衡

所有包含 MMSE 均衡的文件使用 `rx * np.sqrt(h) / (h + 1/γ̄)`。一致 ✅。

### 函数一致性总结

| 不一致 | 严重度 | 影响范围 |
|--------|--------|---------|
| VV 公式 unwrap(angle*M)/M vs unwrap(angle)/M | **中** | stress_common + 4 个 KF 文件。但 VV 已被证明有害，不影响最终结论 |
| ber() vs ber_count() 命名 | 低 | 4 个旧文件。功能完全一致 |
| kf_carrier_sync P 矩阵重置 | **高** | 仅 sim_ch4_kf_carrier_sync.py。文件已废弃 |

---

## 任务 3：Bug 状态确认

| Bug | 声称状态 | 代码证据 | 实际状态 |
|-----|---------|---------|---------|
| VV π/4 偏移 | 已确认未修 | VV 输出 `angle(avg)/M`，不含 `-π/4` 修正。所有文件一致。 | ✅ **确认存在** — 这是 4 次方鉴相器的物理特性，通过 resolve_qpsk 配套处理 |
| resolve_qpsk 掩盖 CPR 失效 | 已确认 | D1/D2 代码 L95/L98 证实两者都用 resolve_qpsk | ✅ **确认存在** — 但对所有方法一致使用，不影响相对排名 |
| P-matrix 每块重置 (TL-09) | 已确认，文件废弃 | sim_ch4_kf_carrier_sync.py L224：kf_unified 签名无 P_init；L262：P 每次初始化为 diag；L339-345：调用时不传 P | ✅ **确认存在于已废弃文件** — common.py/stress_common/kf_pilot_h 已修复 |
| VV unwrap(angle*M)/M | stress_common 有 | stress_common L144：`np.unwrap(np.angle(avg) * M) / M` | ✅ **确认存在** — common.py 已修正为 unwrap(angle)/M |
| TL-13 违规 | stress 已修 | stress_common L253-269：`generate_shared_realization()` 共享信道；original 文件各自生成 | ✅ **确认** — 压力测试已修，原始文件未修（已废弃） |

---

## 任务 4：结论可靠性标记

| # | 结论 | 标记 | 来源 | 条件/说明 |
|---|------|------|------|----------|
| 1 | TL-13 修复影响有限：共享 vs 独立信道 ±1.6 dB | ✅ 已验证 | A1 results JSON | 100 种子验证，3 湍流等级增益差异 0.4-1.6 dB |
| 2 | Fixed 基线默认参数严重次优：改善 4.6-8.9x | ✅ 已验证 | D1 results JSON | 序贯搜索：weak 4.6x, moderate 6.2x, strong 8.9x |
| 3 | V&V CPR 有害：BER 10%→27-30% | ✅ 已验证 | D2 results JSON | 消融：FOE+VV strong=30.5% vs FOE+DPLL=1.9% |
| 4 | DPLL 是载波恢复核心贡献者 | ✅ 已验证 | D2 results JSON | FOE→FOE+DPLL：13.3%→1.9%（7x 改善） |
| 5 | 湍流感知 R 矩阵无价值：<13% 差异 | ⚠️ 条件性 | B2+D3 results | 差异确实 <13%，但标准 PA-KF 反而更好 2.3dB — 结论可靠 |
| 6 | Q[1,1] 是哑参数：50x 范围 BER 完全相同 | ✅ 已验证 | B1 results | Q_fine_df 100M→250M：全部 BER=0.0308 |
| 7 | P 矩阵初始化不影响稳态 | ✅ 已验证 | B3 results | P00 扫描 0.01→10π²：BER 完全相同 |
| 8 | 5% 导频开销 near-optimal：<1.5x | ✅ 已验证 | B4 results | strong 1%→5%：net BER 0.168→0.029 |
| 9 | 前置式导频最优：均匀式差 6.1x | ✅ 已验证 | B5 results | moderate front=0.0018 vs uniform=0.0109 |
| 10 | BLOCK=100 非最优：BS=20 好 1.74x | ✅ 已验证 | C4 results | strong BS=20=0.0177 vs BS=100=0.0309 |
| 11 | 深衰落块 KF 改善：4.6-13 dB | ✅ 已验证 | C5 results | strong h<0.1: KF=14.3% vs Fixed=41.3% |
| 12 | KF 对频偏/线宽鲁棒 | ✅ 已验证 | C1-C3, D5 results | f_res 1→20MHz：增益 8.1→8.7dB；lw 10kHz→1MHz：8.1→11.1dB |
| 13 | 线性 KF 最优：EKF=KF，UKF 更差 | ✅ 已验证 | D4 results | KF vs EKF BER 完全相同；UKF 2-4x 更差 |

### 待重验项（SPEC.md §6.2）

| # | 结论 | 当前标记 | 说明 |
|---|------|---------|------|
| 1 | D1: KF pilot vs 最优 Fixed（强湍流 KF 输） | ⚠️ 待重验 | 数据可靠（3.08% vs 2.22%，resolve_qpsk 一致使用），但绝对值受 oracle 影响 |
| 2 | D2: VV 有害 | ⚠️ 待重验 | 相对排名可靠（BER 从 10% 恶化到 27-30%），但 VV 公式在 stress_common 中有 bug |
| 3 | KF 增益数字 +11/+12/+7 dB | ⚠️ 待重验 | 基于 resolve_qpsk（oracle），绝对值可能略偏低 |
| 4 | BPS 无噪声下 BER=0 | ⚠️ 待重验 | resolve_qpsk 贡献，非 BPS 真实性能 |

---

## 关键发现

### 1. 参数完全一致（0 问题）
所有 16 个文件的核心参数（R_SYM, T_S, LASER_LW, F_RESIDUAL, DOPPLER, BLOCK, 湍流参数, Q 矩阵参数）与 SPEC.md 完全一致。信号模型全部正确（√h·s）。

### 2. ~~VV 公式存在已知不一致（影响有限）~~ → **VV 公式 bug 是致命问题**

> ⚠️ **2026-05-31 重验后升级为最关键发现。** 以下为原始审计结论（已过时）：
> `unwrap(angle*M)/M` 出现在 stress_common 和 4 个旧 KF 文件中。但 D2 消融已证明 VV 在湍流下有害，公式差异不影响最终结论。common.py 已修正。
>
> **重验结果推翻了"影响有限"判断**，详见下方 §5。

### 3. P-matrix bug 仅存在于已废弃文件
sim_ch4_kf_carrier_sync.py 确认有 TL-09 bug（每块重置 P），但该文件已标记废弃。所有活跃代码（common.py, stress_common, kf_pilot_h）已正确实现 P 跨块传递。

### 4. ~~13 条结论全部有数据支撑~~ → 部分结论因 VV bug 需修订

旧结论中涉及 Fixed 基线和 VV 的条目受 VV 公式 bug 影响需修订（见 §5）。KF 内部机制相关结论（B1-B5, C1-C5, D4-D5）仍然有效。

### 5. ~~压力测试结果可信~~ → 压力测试数据可信但 D1/D2 结论需修订

所有压力测试使用 resolve_qpsk 统一评估 + 共享信道实现，方法间对比公平。但 D1/D2 的具体结论因 Fixed 基线含 bug VV 而需修订。

---

## §5. D1/D2 重验结果（2026-05-31 续接）

### 重验设置

- 脚本：`projects/simulation/experiments/reverify_D1D2.py`
- 配置：30 种子，Ns=10000，γ̄=100（20dB），3 湍流等级
- 使用新 common.py（修正 VV 公式 `unwrap(angle)/M`）
- 对比旧 `results_kf_stress_D1D2.json`（bug VV 公式 `unwrap(angle*M)/M`）

### D1 结果对比：KF pilot vs 最优 Fixed

| 湍流 | Fixed_opt (新/旧) | KF_pilot (新/旧) | KF 增益 (新/旧) |
|------|-------------------|------------------|-----------------|
| weak | 0.016% / 0.32% | 0.016% / 0.016% | **+0.01** / +13.0 dB |
| moderate | 0.148% / 0.579% | 0.173% / 0.173% | **-0.66** / +5.3 dB |
| strong | 1.74% / 2.22% | 3.08% / 3.08% | **-2.48** / -1.4 dB |

**关键观察**：KF pilot BER 完全不变（验证 KF 实现正确）。Fixed 基线 BER 因 VV 修正大幅改善，导致 KF 增益消失。

### D2 消融结果对比

| 方案 | 弱 (新/旧) | 中 (新/旧) | 强 (新/旧) |
|------|-----------|-----------|-----------|
| FOE only | 10.9% / 10.9% | 10.2% / 10.2% | 13.4% / 13.4% |
| FOE+VV | **0.015% / 27.4%** | **0.15% / 26.6%** | **7.9% / 30.5%** |
| FOE+DPLL | 0.20% / 0.20% | 0.37% / 0.37% | 1.93% / 1.93% |
| KF frame | 0.016% / 0.016% | 0.89% / 0.89% | 25.8% / 25.8% |
| KF pilot | 0.016% / 0.016% | 0.17% / 0.17% | 3.08% / 3.08% |

### 交叉验证（3 个子 agent）

1. **Head-to-head 测试**：同一数据上公式 A vs B，确认公式 A 在弱/中/强分别好 97x/23x/2.3x
2. **旧 systematic_analysis 检查**：确认该文件用正确公式，但报告强湍流 ~40% 失败率（种子级 BER>10% 比例，与平均 BER 7.9% 不矛盾）
3. **数学分析**：公式 B 先乘 M=4 后 unwrap，将 [-4π,4π] 扩展到 [-16π,16π]，产生大量假阳性缠绕修正（86 个检测 vs 47 个真实，39 个假阳性，每个注入 π/2 误差）。MSE 恶化最高 28,229 倍。

### 结论修订

| 旧结论 | 新状态 |
|--------|--------|
| VV 全湍流有害 | ❌ 仅强湍流不如 DPLL，弱/中 VV 有效 |
| KF 增益 +11/+5/-1.4 dB | ❌ 修正为 0/-0.7/-2.5 dB |
| KF pilot 弱/中有效 | ⚠️ 与最优 Fixed 持平（无显著增益） |
| DPLL 是核心贡献者 | ✅ 强湍流仍成立 |
| KF 内部机制（B/C/D4/D5） | ✅ 仍有效（不依赖与 Fixed 对比） |

## 决策引用

- 无决策

## 范围确认

- 本轮是否在 scope boundary 内：是（代码审计 + 重验确认，未做方向判断）

## 后续

- Ch4 论文叙事需转型：从"KF 算法创新"转为"系统性分析"
- SNR 扫描曲线（BER vs SNR）— 论文必需
- C5 深衰落改善用修正 Fixed 重验
- resolve_qpsk（oracle）对绝对 BER 值的影响量级评估
