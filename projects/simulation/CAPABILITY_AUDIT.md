# FSO 湍流信道仿真平台 — 能力审计与实验扩展方案

> 生成时间: 2026-06-04
> 基于文件: SPEC.md, common.py (770行, 38函数, 18常量), CONCLUSIONS.md
> 实验脚本: 21个

---

## 一、common.py 能力全景

### 1.1 模块架构

```
common.py
├── 系统参数层（18个常量）
│   ├── 物理参数: R_SYM, T_S, F_CARRIER, LASER_LW
│   ├── 湍流参数: TURB{weak,moderate,strong}, Q_TURB_PARAMS
│   ├── 多普勒参数: DOPPLER_HIGH/LOW, F_RESIDUAL
│   └── 方法配置: FIXED_CFG, FIXED_CFG_OPTIMAL, BLOCK
│
├── 信号原语层（12个函数）
│   ├── 信道生成: gg_block (Gamma-Gamma 块衰落)
│   ├── 调制/解调: qpsk_mod/demod, qam16_mod/demod
│   ├── BER评估: ber_count, ber_count_qam16, resolve_qpsk, resolve_qam16, ber_eval
│   └── 辅助: amp_limit, hard_decision, doppler_phase
│
├── 载波恢复算法层（6个函数）
│   ├── FOE: fft_foe (4次方FFT频偏估计)
│   ├── DPLL: dpll_track (4次方鉴相), dpll_track_dd (DD鉴相)
│   ├── VV: vv_cpr (Viterbi-Viterbi 4次方)
│   ├── BPS: bps_cpr (盲相位搜索，支持QPSK/16-QAM)
│   └── Fixed: carrier_recovery_fixed (FOE+DPLL+VV组合)
│
├── Kalman滤波层（5个函数）
│   ├── 设计: design_Q
│   ├── 核心: kf_unified (2状态，支持QPSK/16-QAM)
│   └── 变体: kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery
│
├── 信道/均衡层（6个函数）
│   ├── 共享信道: generate_shared_realization (TL-13)
│   ├── 导频: insert_pilots, get_pilots
│   ├── 均衡: mmse_equalize, equalize_oracle, equalize_hmed
│
└── 实验框架层（9个函数）
    ├── 便捷运行: run_fixed, run_kf_oracle, run_kf_frame_h, run_kf_pilot, run_bps
    ├── 试验框架: run_trial_shared (多方法并行)
    └── 结果保存: save_results (自动注入元数据, TL-25)
```

### 1.2 已有实验覆盖矩阵（21个脚本）

| 维度 | 覆盖状态 | 脚本数 |
|------|---------|--------|
| QPSK 基础方法对比 | 已覆盖 | 10 |
| QPSK SNR扫描 | 已覆盖 | 1 (multi_seed_sweep) |
| QPSK NMSE灵敏度 | 已覆盖 | 4 |
| DPLL ω_n 扫参 | 已覆盖 | 1 |
| DPLL ζ 扫参 | 已覆盖 | 1 |
| VV/BPS Nw 扫参 | 已覆盖 | 2 |
| KF 内部参数 | 已覆盖 | 2 |
| 16-QAM DD-DPLL | 部分覆盖 | 3 |
| 解析模型验证 | 已覆盖 | 3 |
| **16-QAM SNR扫描** | **未覆盖** | 0 |
| **16-QAM 多方法对比** | **未覆盖** | 0 |
| **多普勒场景对比** | **未覆盖** | 0 |
| **非oracle均衡评估** | **未覆盖** | 0 |
| **resolve_qpsk oracle偏差量化** | **未覆盖** | 0 |
| **信道编码(FEC)影响** | **未覆盖** | 0 |
| **64-QAM 扩展** | **未覆盖** | 0 |

---

## 二、沉睡资产（已实现但未充分利用）

### 2.1 完全沉睡（0使用）

| 资产 | 功能 | 扩展潜力 |
|------|------|---------|
| `ber_count` | QPSK直接解调 | 量化oracle偏差 |
| `ber_count_qam16` | 16-QAM直接解调 | 量化oracle偏差 |
| `run_trial_shared` | 多方法并行框架 | 新实验的零成本骨架 |
| `kf_oracle_recovery` | KF性能上界 | KF系列方法的天花板参考 |
| `kf_frame_h_recovery` | 无导频KF | 低开销基线 |

### 2.2 低利用率（1-2个脚本）

| 资产 | 当前使用 | 扩展潜力 |
|------|---------|---------|
| `equalize_hmed` | 1脚本 | 非oracle均衡性能评估 |
| `dpll_track_dd` + QPSK | 0脚本(仅16-QAM) | DD vs 4th-power对比 |
| `DOPPLER_LOW` | 0脚本 | 场景对比 |
| `hard_decision` | 0脚本直接用 | 自适应方法基件 |

---

## 三、实验扩展方案

### 按开发成本分层

---

### A层: 零成本扩展（仅换参数/加对比组，不改代码）

---

#### A1: resolve_qpsk Oracle 偏差量化

- **目的**: 量化 resolve_qpsk（oracle旋转）对绝对BER值的乐观偏差，回答SPEC.md §7.4的未验证项
- **假设**: Oracle偏差在BER<1%时可忽略（<0.5dB），在BER>10%时显著（>2dB）
- **代码改动**: 零。直接复用 common.py 的 ber_count + resolve_qpsk
- **实验设计**: 对已有实验的每个种子，同时计算 ber_count 和 resolve_qpsk，对比差异
- **预计数据**: 3湍流 x 5 SNR x 5方法 x 10种子 = 750个数据点
- **价值**: 回答论文审稿人可能的质疑"oracle评估是否影响结论"

#### A2: KF Oracle-h 性能上界（QPSK）

- **目的**: 确定 KF 方法的理论上界（用真实h），判断 kf_pilot 与上界的差距
- **假设**: kf_oracle 在强湍流下也优于 DPLL（因为用真实h），但 kf_pilot 因 DD 失效差距大
- **代码改动**: 零。直接调用 run_kf_oracle + run_trial_shared
- **实验设计**: 在 multi_seed_sweep 框架中加入 'kf_oracle' 方案
- **预计数据**: 3湍流 x 16 SNR x 10种子 = 480点
- **价值**: 为 C4-07（KF强湍流不如DPLL）提供机制解释的完整证据链

#### A3: 低多普勒场景对比

- **目的**: DOPPLER_LOW (30 MHz/s) vs DOPPLER_HIGH (150 MHz/s) 对各方法的影响
- **假设**: 低多普勒下所有方法改善，VV改善最大（相位变化慢→unwrap更稳定）
- **代码改动**: 零。只需改 f_dot 参数
- **实验设计**: 用 run_trial_shared，f_dot 分别取 DOPPLER_LOW 和 DOPPLER_HIGH
- **预计数据**: 2场景 x 3湍流 x 5方法 x 10种子 = 300点
- **价值**: 展示方法在不同动态场景下的鲁棒性

#### A4: 非Oracle均衡性能评估

- **目的**: 评估 equalize_hmed（实际可用）vs equalize_oracle（理想）的性能差距
- **假设**: 20dB下差距<0.5dB（C3-02已暗示），但低SNR下差距增大
- **代码改动**: 零。run_fixed/run_kf_pilot 已有 eq_mode='hmed' 参数
- **实验设计**: 对 multi_seed_sweep 加 eq_mode 维度
- **预计数据**: 2均衡模式 x 3湍流 x 16 SNR x 5方法 = 480点
- **价值**: 回答"oracle h 均衡假设对结论有多大影响"

---

### B层: 小量开发（加一个函数或20行以内改动）

---

#### B1: 16-QAM 多方法 SNR 扫描

- **目的**: 在 16-QAM 下系统性对比 DD-DPLL/BPS/KF-oracle 的 BER vs SNR 曲线
- **假设**: DD-DPLL > KF-oracle > BPS（16-QAM下DD鉴相器最可靠），强湍流存在~1%平台
- **代码改动**: ~30行。复用 multi_seed_sweep.py 的框架，替换 method_vv 等为 16-QAM 版本
- **需要新增**: resolve_qam16 的统计框架（已有 resolve_qpsk 的 compute_stats 可直接复用）
- **预计数据**: 3湍流 x 16 SNR x 3方法 x 10种子 = 1440点
- **价值**: 首条 16-QAM 多方法 SNR 曲线，支撑 C4-13/C4-14

#### B2: DD-DPLL vs 4th-power DPLL 对比（QPSK）

- **目的**: 在 QPSK 场景下对比判决导引 DPLL 和传统 4 次方 DPLL 的性能
- **假设**: 两者性能持平（QPSK下DD等价于4th-power），但在深衰落块DD更稳定
- **代码改动**: ~15行。在已有实验中加入 dpll_track_dd(mod='qpsk') 作为新方法
- **预计数据**: 3湍流 x 5 SNR x 2 DPLL变体 x 10种子 = 300点
- **价值**: 方法论贡献——证明 DD 鉴相器是 QPSK/16-QAM 统一框架

#### B3: 桥接扩展 — 均衡误差→16-QAM BER

- **目的**: 将 bridge_ch3_ch4.py 的灵敏度分析扩展到 16-QAM
- **假设**: NMSE 对 16-QAM BER 的影响远大于 QPSK（C3-05已暗示，但缺NMSE-BER曲线）
- **代码改动**: ~40行。复用 bridge_ch3_ch4.py 框架，方法改为 dpll_track_dd + resolve_qam16
- **预计数据**: 3湍流 x 11 NMSE x 1方法 x 10种子 = 330点
- **价值**: Ch3→Ch4 桥接的完整版——QPSK免疫 + 16-QAM敏感的对比图

#### B4: KF pilot 16-QAM 实验

- **目的**: 验证 KF pilot + 16-QAM 的可行性（kf_pilot_recovery 已有 mod='qam16' 参数）
- **假设**: KF pilot 在 16-QAM 弱/中湍流有效，但 DD 在深衰落中不如 QPSK 可靠
- **代码改动**: ~20行。调用 run_kf_pilot 并在 insert_pilots 后用 qam16_mod 生成信号
- **注意**: 需要一个新的 generate_shared_realization_16qam() 函数（或给原函数加 mod 参数）
- **预计数据**: 3湍流 x 5 SNR x 10种子 = 150点
- **价值**: 首个 KF pilot + 16-QAM 结果

#### B5: 方法切换点分析（自适应框架验证）

- **目的**: 验证不同湍流/SNR区域的最优方法组合，为未来自适应切换提供数据支撑
- **假设**: 存在清晰的方法切换边界（如 SNR>15dB→DPLL，SNR<10dB→VV大窗口）
- **代码改动**: ~30行。后处理脚本，对已有 multi_seed_sweep 数据做等BER线分析
- **预计数据**: 不需要新实验，分析已有数据
- **价值**: 方法选择的工程指导

---

### C层: 大量开发（新信道模型/新算法/新框架）

---

#### C1: 信道编码 (FEC) 下的 BER 性能

- **目的**: 加入 LDPC/Turbo 码后的误码率表现，回答"实际系统BER"问题
- **假设**: 编码增益使 DPLL 在强湍流下 BER 从 ~2% 降至 ~1e-4（可纠错范围）
- **代码改动**: ~150行。需要实现: (a) FEC编码器/解码器接口, (b)交织器, (c)BER→FER映射
- **可行性考虑**: 可用 numpy 模拟简单 BCH/RS 码，或调用通信库
- **预计数据**: 3湍流 x 5 SNR x 5方法 x 2(编码/未编码) = 150点
- **价值**: 从"未编码BER"到"实际系统性能"的关键一步

#### C2: 自适应载波恢复策略

- **目的**: 根据实时信道状态（h估计值）动态切换 DPLL/KF/VV
- **假设**: 自适应策略在所有湍流下优于任何单一方法 >1dB
- **代码改动**: ~100行。需要: (a)信道状态检测器, (b)切换逻辑, (c)切换瞬态处理
- **风险**: 已有 TL-03/06/07 教训——自适应方案"物理上无效"的先例
- **预计数据**: 3湍流 x 10 SNR x 10种子 = 300点
- **价值**: 如果成功，是强创新点；如果失败，记录失败原因也有价值

#### C3: 64-QAM 扩展

- **目的**: 验证方法在更高阶调制下的表现
- **假设**: 64-QAM 对 NMSE 极度敏感，只有 DD-DPLL+KF 可行
- **代码改动**: ~200行。需要: (a)64-QAM mod/demod, (b)resolve_qam64, (c)hard_decision扩展
- **预计数据**: 3湍流 x 5 SNR x 3方法 x 10种子 = 450点
- **价值**: 方法的调制阶数可扩展性分析

#### C4: 时变信道模型（块间相关）

- **目的**: 当前块间衰落独立（gg_block），加入 Markov 相关性更接近真实
- **假设**: 块间相关使 VV/BPS 受益（平滑过渡），KF 影响不大（逐块独立估计）
- **代码改动**: ~80行。需要修改 gg_block 为 Markov-GG 或 AR(1)-GG
- **预计数据**: 3湍流 x 5相关系数 x 5方法 = 75点
- **价值**: 信道模型保真度提升

---

## 四、重点问题的深入分析

### 4.1 KF 能力利用情况

**现状**: KF 有 3 个变体（oracle/frame-h/pilot），但实验主要用 kf_pilot。kf_oracle 和 kf_frame 仅在 reverify_D1D2 中作为消融对照出现。

**未被利用的 KF 能力**:
1. `kf_unified` 支持 `mod='qam16'` 参数，但只有 test_qam16_multimethod.py（3种子快测）用了
2. `kf_pilot_recovery` 也支持 `mod='qam16'`，但完全没有 16-QAM KF pilot 实验
3. KF 的 `Q_fine_df` 参数（频偏精细调节）未被扫参
4. KF 的 `alpha_ema`（h估计平滑系数）只在 reverify_kf_internals 粗略验证

**建议优先级**: B1(16-QAM SNR扫描) > B4(KF pilot 16-QAM) > A2(KF oracle上界)

### 4.2 bridge_ch3_ch4 桥接思路的扩展

**现有模式**: 固定载波恢复方法 → 扫NMSE → 测BER退化

**可扩展方向**:
- **B3**: 桥接到 16-QAM（已列出）
- **桥接到 FEC**: 扫 NMSE → 测编码后 BER
- **桥接到同步误差**: 扫残余频偏误差 → 测 BER（与 NMSE 双变量正交扫描）
- **桥接到 Block Size**: 扫 BLOCK → 测各方法的 BER（C4-09 的反向视角）

### 4.3 sim_nmse_vs_ber 灵敏度分析的复用

**核心模式**: 对某个误差参数（NMSE）做精细化扫描，在多个 SNR/湍流/方法 条件下测 BER。

**可直接复用到**:
- 残余频偏灵敏度（把 NMSE 换成 Δf 误差）
- 导频数量灵敏度（已有 B4 粗略验证，但无精细曲线）
- KF Q 矩阵参数灵敏度（已有 reverify_kf_internals，但只测了极端值）

### 4.4 多种子蒙特卡洛框架

**run_trial_shared** 是一个未被使用的现成框架:
```python
results = run_trial_shared(Ns, gamma_bar, turb_name, f_dot, seed,
                           schemes=['fixed', 'kf_oracle', 'kf_frame', 'kf_pilot'],
                           eval_mode='oracle')
```

**直接支持**: 任何只需在 schemes 列表中加名字的新实验。对新方法（如 DD-DPLL），只需在 common.py 中加一个 `run_dd_dpll` 便捷函数。

**multi_seed_sweep.py** 的断点续跑机制也是可直接复用的。

---

## 五、推荐优先级排序

| 优先级 | 实验 | 成本 | 价值 | 风险 |
|--------|------|------|------|------|
| **P0** | A1: Oracle偏差量化 | 零 | 高（回应审稿人） | 无 |
| **P0** | A2: KF oracle上界 | 零 | 高（机制完整性） | 无 |
| **P1** | B1: 16-QAM SNR扫描 | 小 | 高（论文新数据） | 低 |
| **P1** | A4: 非oracle均衡评估 | 零 | 中（方法严谨性） | 无 |
| **P2** | B3: NMSE→16-QAM桥接 | 小 | 高（Ch3-Ch4连贯性） | 低 |
| **P2** | B2: DD vs 4th-power对比 | 小 | 中（方法论贡献） | 低 |
| **P2** | A3: 低多普勒场景 | 零 | 中（场景完整性） | 无 |
| **P3** | B4: KF pilot 16-QAM | 小 | 中（新组合验证） | 中 |
| **P3** | B5: 方法切换点分析 | 小 | 中（工程指导） | 无 |
| **P4** | C1: FEC编码 | 大 | 很高（实际系统） | 中 |
| **P4** | C3: 64-QAM | 大 | 中（扩展性） | 低 |
| **P5** | C2: 自适应策略 | 大 | 很高但... | 高(TL-03/06/07) |
| **P5** | C4: 时变信道 | 大 | 中 | 中 |

---

## 六、结论

### 代码复用率评估

- **A层实验（4个）**: 100% 复用 common.py，0行新代码
- **B层实验（5个）**: 80-90% 复用，每个只需 15-40 行新代码
- **C层实验（4个）**: 30-60% 复用，每个需要 80-200 行新代码

### 最大发现

1. **run_trial_shared 完全沉睡**——这是最高效的实验入口，支持 5 种方法并行对比，但 21 个实验脚本没有一个用它
2. **kf_oracle / kf_frame 完全沉睡**——KF 的两个重要变体未被系统性评估
3. **16-QAM 方向有大量空白**——common.py 已有完整的 16-QAM 支持（mod/demod/DD-DPLL/BPS/KF），但只做了 3 个初步实验
4. **bridge 模式可横向扩展**——NMSE→BER 的灵敏度分析框架可直接迁移到频偏误差、Block Size 等维度
