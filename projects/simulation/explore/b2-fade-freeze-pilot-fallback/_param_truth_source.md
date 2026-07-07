# 阶段 0.5：参数真相源前置（σp² vs GG α/β 严格区分 + ref [58] 查证 + B2Params 草稿）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 0.5
> 日期: 2026-07-08
> 守: TL-26 参数溯源 + FR-26 读原文数值 + V4 参数变更触发算法重审 + NDA-ML D-007 教训（线宽 500kHz→10kHz 全量重跑 3 轮）
> 输入: 阶段 0.1 `_step4a_detail_extract.md`（σp²/GG α/β/OSNR/线宽/pilot 配置）+ 阶段 0.2 `_db_sourcing_audit.md`（ref [58] 待查）+ 阶段 0.4 `_fair_comparison_framework.md`（γ_th / ρ_fade）

## 0. 目标

把 B2-Q2 所有关键参数**前置标文献来源 + 读原文数值**，草拟 B2Params 类（不直接写 params.py），防重蹈 NDA-ML D-007 参数反复混乱。

**阶段 0.1 子 agent 发现的命名混淆必须消除**：σp²（Wiener PN 单值）vs GG α/β（fade 三档）是两个正交物理量，禁用 σp² 名义塞 fade 三档。

## 1. 参数真相源（逐项标 source + 读原文数值）

### 1.1 激光线宽 LASER_LW（继承 D-007，单一真相源）

| 字段 | 值 | source | audit |
|---|---|---|---|
| LASER_LW | 10e3 Hz（10 kHz）| `params.py:81` SystemParams.LASER_LW | WARNING |
| 符号率 R_SYM | 2.5e9 sym/s（2.5 GBaud）| `params.py:46` SystemParams.R_SYM | OK |
| 来源文献 | Valjus sat.1553 §4.2 L438：星地 FSO ECL 典型 0.1-1MHz@28GBaud，单载波 2.5GBaud 配 ECL (1-100kHz)，10kHz@2.5GBaud → ΔνTs=2.51e-5 落在该区间低端 | `params.py:85` | WARNING |

**真相源统一**（D-007 已完成）：全场景 10kHz@2.5GBaud，σ²_pN = 2π·LASER_LW·T_S = 2.51e-5。**B2-Q2 继承，不改**。

### 1.2 ⚠️ σp²（Wiener PN 单值）vs GG α/β（fade 三档）严格区分

**阶段 0.1 子 agent 发现的命名混淆必须消除**：

| 物理量 | 符号 | 含义 | 数值 | B2-Q2 用途 |
|---|---|---|---|---|
| **Wiener PN 每符号方差** | σ²_pN | 激光线宽引起的离散相位噪声方差 | 2.51e-5（单值，全场景统一）| AWGN 场景 PN（继承 step4a）|
| **Gamma-Gamma 块衰落参数** | α, β | 大气闪烁引起的幅度 fade 统计参数 | weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8 | fade 场景（B2-Q2 核心）|
| **sat.1553 Rytov 方差** | σ²_R（sat.1553 记 σp²）| 弱起伏平面波闪烁方差 | scenario 4 σ²_R=0.25 | sat.1553 场景定义（不是 B2-Q2 直接用）|

**禁止混用**：
- ❌ "σp² 三档（weak/moderate/strong）"——σ²_pN 是单值，fade 三档是 GG α/β
- ❌ "σp²=0.25"——sat.1553 的 σp²=0.25 是 Rytov 方差 σ²_R，跟 Wiener PN σ²_pN=2.51e-5 不同物理量
- ✅ "σ²_pN = 2.51e-5（Wiener PN）+ GG α/β 三档（fade）"

**GG α/β 真相源**（`params.py:98-148`）：
- weak: α=4.0, β=3.0（`params.py:98, 108`）
- moderate: α=2.5, β=1.8（`params.py:118, 128`）
- strong: α=1.5, β=0.8（`params.py:138, 148`）
- 来源：step4a 继承，原始来源待 params.py 字段 audit 核查（阶段 0.5 附带：B2 sandbox 前确认 GG α/β 文献来源）

**待查**：GG α/β 三档的文献来源（是 sat.1553 scenario 定义还是别的）—— sandbox 前补标 source

### 1.3 OSNR 工作点（继承 step4a）

| 场景 | SNR 扫描点（γ_d dB）| source |
|---|---|---|
| AWGN | SNR_AWGN（step4a `_time_domain_crlb.py:548`，待 grep 具体值）| step4a 继承 |
| 湍流（weak/mod/strong）| [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0] | `_time_domain_crlb.py:555` |

**B2-Q2 OSNR 工作点**：继承 step4a 湍流扫描点。**B2-Q2 特有**：fade 占空比 ρ_fade 在不同 OSNR 点不同（低 OSNR → ρ_fade 大），sandbox 要逐点测 ρ_fade。

### 1.4 pilot 配置（step4a 继承 + B2-Q2 摊薄）

| 字段 | step4a 值 | B2-Q2 值 | source |
|---|---|---|---|
| pilot spacing | 4（`_time_domain_crlb.py:122`）| 4（fade 期）| step4a 继承 |
| pilot 类型 | 真符号 pilot（已知 tx 符号）| 同 | step4a 继承 |
| pilot 密度 | 25% overhead（全帧）| ρ_fade × 25%（摊薄）| 阶段 0.4 §3 |
| pilot overhead dB | 1.249 dB（全帧）| ρ_fade × 1.249 dB | 阶段 0.4 §3.2 |

### 1.5 B2-Q2 特有参数（fade 检测门控）

| 字段 | 含义 | 初始值 | source |
|---|---|---|---|
| γ_th | fade 检测功率阈值 | 待 sandbox 扫 [γ̄−3σ, γ̄−1σ] | 阶段 0.4 §3.3 |
| ρ_fade | fade 占空比 = P(P < γ_th) | 待 sandbox 实测 | 阶段 0.4 §3.2 |
| N_DFT | 逐块恢复块大小 | 256（继承 step4a）| step4a |
| CH_BLOCK | 信道 h 恒定块 | 100（继承 step4a）| step4a `params.py:476` |
| N_BLOCKS | 每点块数 | 400（继承 step4a）| step4a |

**γ_th 物理依据待补**：γ_th 不能拍脑袋（FR-20/TL-26）。sandbox 阶段 1 要先实测 rx 功率分布 P(|rx|²)，再定 γ_th ∈ [γ̄−3σ, γ̄−1σ] 的扫参范围。**这是 sandbox 第一步**（不是参数真相源阶段能定的）。

## 2. ref [58] 查证（阶段 0.2 附带任务）

### 2.1 ref [58] 身份（主线 grep sat.1553 reference list + B1 笔记交叉确认）

**ref [58] = Martins, Guiomar, Pinto (2021) "Hardware Optimization of Dual-Stage Carrier-Phase Recovery for Coherent Optical Receivers," OSA Continuum 4(12):3157-3175**

- sat.1553 reference list L1261：`58C. S. Martins, F. P. Guiomar, and A. N. Pinto, "Hardware Optimization of Dual-Stage Carrier-Phase Recovery..."`
- 已在 B1 笔记精读：`papers/_read_notes/_B1-pilot-window-increment.md:4, 18, 22, 31`

### 2.2 ref [58] 机制（B1 笔记交叉确认）

**[58] Martins dual-stage CPR**：
- 第一级：pilot-CPE（moving-average filter + 线性插值）
- 第二级：BPS（blind phase search，test-phase 搜索）
- **两阶段并行处理每个符号**（dual-stage parallel）
- 关键贡献：pilot-rate × modulation × linewidth 三维 trade-off，最优 pilot-rate 随 linewidth 变化
- [58] 的优化是**静态**（固定 linewidth 找最优 pilot-rate）

### 2.3 ⚠️ 对阶段 0.2 叙事锚点的修正

**阶段 0.2 原解读**（`_db_sourcing_audit.md` §4）：
> "sat.1553 L440 [58] 'pilot + 盲组合 open direction' 是 B2-Q2 叙事锚点"

**修正后解读**（ref [58] 查证后）：
- sat.1553 [58] 说的"pilot combined with second blind phase estimator"指的是 **dual-stage pilot-BPS CPR**（[58] Martins 的具体实现）
- **机制**：pilot-CPE 粗估 + BPS 精修（dual-stage 并行，每符号都过两级）
- **不是** B2-Q2 的"pilot fallback + blind freeze"（双模切换，按 fade 状态选估计器）

**对 B2-Q2 叙事的影响**：
- ❌ 不能说"B2-Q2 是 sat.1553 [58] open direction 的直接具体化"——[58] 已经具体化了（dual-stage），且机制不同
- ✅ 可以说"sat.1553 L440 提到 pilot+盲组合方向（引 [58] dual-stage），B2-Q2 探索的是这个大方向的**另一种机制**（fade 门控双模切换 vs dual-stage 并行）"
- ✅ B2-Q2 的动机叙事改为：sat.1553 自报"pilot+盲组合"是有效方向（[58] dual-stage 证 + sat.1553 综述背书），B2-Q2 探索 fade 门控切换这个**未被 [58] 覆盖的机制**

**修正后的叙事定位**（替代阶段 0.4 §4.3）：
1. sat.1553 L440 综述明确"pilot+盲组合能 further improve"（引 [58]）
2. [58] Martins dual-stage 是这个方向的具体化（pilot-CPE + BPS 并行）
3. 但 [58] 是**静态**优化（固定 linewidth 找最优 pilot-rate），没考虑 fade 动态
4. B2-Q2 探索的是"fade 门控双模切换"——[58] 未覆盖的机制（fade 期切 pilot，非 fade 期用 blind）
5. **B2-Q2 增量 = 把 [58] 静态 dual-stage 扩展到 fade 动态场景（双模切换）**

**这个修正实际上强化了 B2-Q2 的 A1 归属**：B2-Q2 不是简单"实现 sat.1553 open direction"（[58] 已实现），是"在 [58] 基础上扩展到 fade 动态"——更扎实的增量叙事。

### 2.4 ref [58] 落盘状态

- sat.1553 content.md L1261 有 reference 条目
- B1 笔记 `papers/_read_notes/_B1-pilot-window-increment.md` 已精读
- **待查**：[58] 全文 PDF 是否在 papers/ 下（B1 可能只读了摘要/部分）—— grep `find papers -iname "*osac*438524*" -o -iname "*martins*2021*"` 待执行
- **不阻塞 B2-Q2**：B1 笔记已有关键信息（dual-stage 机制 + 三维 trade-off），B2-Q2 sandbox 前不必重读 [58] 全文

## 3. B2Params 类草稿（不直接写 params.py，先在 explore 草拟）

```python
# explore/b2-fade-freeze-pilot-fallback/_b2_params_draft.py（草稿，不进 params.py）
"""B2-Q2 双模切换参数（草稿）.

真相源:
- 激光线宽/符号率: 继承 D-007 SystemParams.LASER_LW=10kHz / R_SYM=2.5GBaud（全场景统一）
- Wiener PN σ²_pN: 2π·LASER_LW·T_S = 2.51e-5（派生量，不是独立参数）
- GG α/β: 继承 step4a params.py GammaGammaParams（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8）
- pilot 配置: 继承 step4a DA_PILOT_SPACING=4 / 真符号 pilot / 25% overhead
- fade 阈值 γ_th: sandbox 扫 [γ̄−3σ, γ̄−1σ]（不拍脑袋，待实测功率分布）

⚠️ 命名澄清（阶段 0.1 子 agent 发现）:
- σ²_pN（Wiener PN）是单值，不是 fade 三档
- GG α/β 是 fade 统计参数，不是相位噪声
- 禁用 "σp² 三档" 表述（混淆两个物理量）
"""
from params import SystemParams, GammaGammaParams  # 继承，不自建

class B2Params:
    """B2-Q2 双模切换参数（sandbox 阶段 1 用）."""

    # === 继承（不自建，从 params.py 导入）===
    LASER_LW = SystemParams.LASER_LW          # 10e3 Hz, D-007 统一
    R_SYM = SystemParams.R_SYM                # 2.5e9 sym/s
    T_S = 1.0 / R_SYM                         # 4e-10 s（派生）
    SIGMA2_PN = 2 * 3.14159 * LASER_LW * T_S  # 2.51e-5（派生，Wiener PN 单值）

    # GG α/β（fade 三档，从 GammaGammaParams 导入）
    TURB_LEVELS = ['weak', 'moderate', 'strong']
    GG_ALPHA_BETA = {
        'weak':     (GammaGammaParams.alpha_weak,     GammaGammaParams.beta_weak),      # (4.0, 3.0)
        'moderate': (GammaGammaParams.alpha_moderate, GammaGammaParams.beta_moderate),  # (2.5, 1.8)
        'strong':   (GammaGammaParams.alpha_strong,   GammaGammaParams.beta_strong),    # (1.5, 0.8)
    }

    # === step4a 继承（pilot 配置）===
    DA_PILOT_SPACING = 4                      # 继承 step4a
    PILOT_OVERHEAD_DB_FULL = 10.0 * np.log10(4/3)  # 1.249 dB（全帧，step4a 口径）

    # === B2-Q2 特有（fade 门控）===
    # γ_th: fade 检测功率阈值，sandbox 扫 [γ̄−3σ, γ̄−1σ]
    # ρ_fade: fade 占空比，sandbox 实测（不预设）
    GAMMA_TH_SWEEP = None  # 待 sandbox 第一步实测 rx 功率分布后定
    # fade 块判据: mean(|rx_block|²) < γ_th

    # === B2-Q2 pilot overhead 摊薄（阶段 0.4 §3.2）===
    # B2-Q2 overhead = ρ_fade × PILOT_OVERHEAD_DB_FULL（不是全帧 1.249）
    # sandbox 每点实测 ρ_fade 后算实际 overhead

    # === 块结构（继承 step4a）===
    N_DFT = 256                               # 逐块恢复块大小
    CH_BLOCK = 100                            # 信道 h 恒定块（params.py ExperimentParams.BLOCK）
    N_BLOCKS = 400                            # 每点块数（400×256=102400 ≥ 1e5）
    HDFEC = 3.8e-3                            # 7% HD-FEC 阈值

    # === OSNR 扫描（继承 step4a）===
    SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]

    # === 估计器选择（阶段 0.3 前馈化）===
    BLIND_ESTIMATOR = 'fft_foe'  # 非 fade 期（或 nda_ml_recovery 备选）
    PILOT_ESTIMATOR = 'da_ml'    # fade 期（或 psa_foe_recovery 备选）
    # 所有估计器前馈闭式，无环路反馈（阶段 0.3 INVARIANT）
```

**注意**：
- 这是草稿，sandbox 阶段 1 实现时再落 params.py（MVE 通过才转正，INVARIANT 不污染 common）
- GG_ALPHA_BETA 从 GammaGammaParams 导入（需确认 params.py 有这个类，待 sandbox 前核查）
- γ_th / ρ_fade 不预设（sandbox 实测，FR-20/TL-26 不拍参数）

## 4. 阶段 0.5 结论

**参数真相源前置完成**：
- σ²_pN（Wiener PN 单值 2.51e-5）vs GG α/β（fade 三档）严格区分，消除阶段 0.1 子 agent 发现的命名混淆
- 所有关键参数标 source（继承 D-007 + step4a），B2Params 草稿落盘
- ref [58] 查证完成 = Martins 2021 dual-stage CPR，修正阶段 0.2 叙事锚点解读（[58] 是 dual-stage 并行，B2-Q2 是 fade 门控切换，机制不同但同属"pilot+盲组合"大方向）

**留给 sandbox 阶段 1 的参数任务**：
1. 实测 rx 功率分布，定 γ_th 扫参范围 [γ̄−3σ, γ̄−1σ]
2. 逐点（OSNR × 湍流档）实测 ρ_fade
3. 确认 GG α/β 三档文献来源（params.py audit）
4. 确认 GammaGammaParams 类存在（B2Params 导入依赖）

**进阶段 0.6**：文件组织规约。
