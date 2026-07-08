# 阶段 0.4 公平对照框架 + 0.5 参数真相源 + 0.6 文件组织接口

> 来源: B3-Q2 阶段 0.4-0.6（S003）| 日期: 2026-07-08
> 门控对象: INVARIANT 11（D002 增益归因）/ TL-26 参数溯源（FR-20）/ INVARIANT 14（代码基建新增）/ sim-preflight C7（三方对照）
> 依赖: 0.3 架构定性（前馈开环，已定）

---

## 阶段 0.4：公平对照框架（baseline 含 jphot FSTS，防增益归因）

### 0.4.1 核心问题：增益归因（D002/INVARIANT 11 首要风险）

B3-Q2 单链路 dB 优势（1.17dB）的物理来源 = **jphot 两段式 FOE 的 BL² 算法结构**（`_stage0_1b` L151 增益归因警示 + `_a1_attribution_audit` L28 坐实）。

→ 若 baseline = 传统分立 TS（jphot baseline），则 B3-Q2 ≈ 把 jphot 搬星地，**dB 是继承的不是新增的**。

→ **公平对照硬约束**：baseline 必须含 jphot FSTS（同算法结构），B3-Q2 必须靠 **CPE 联合 + Doppler 维度** 产生新增益。

### 0.4.2 三方对照矩阵（sim-preflight C7：消融 + 祖师爷）

| 方法 | FS | FOE | CPE | Doppler | MRC | 说明 |
|---|---|---|---|---|---|---|
| **M1 传统分立 TS 管线**（祖师爷/弱 baseline） | 独立相关峰 | 传统 TS（单段 4th-FFT/FFT）| 独立 VV/BPS | 不处理（缓变假设）| 独立 DSP 每支路 | jphot baseline；含偏差（故意弱） |
| **M2 jphot FSTS**（公平对照基准） | FSTS 相关峰 | 两段式 FOE BL²（jphot-L175/208）| 独立 CPE | 不处理（缓变假设）| 共享 LO 合并后联合补偿 | **核心对照**：同 FS+FOE 算法结构，B3-Q2 只差 CPE/Doppler 维度 |
| **M3 B3-Q2 联合**（本方法） | FSTS 相关峰 | 两段式 FOE BL² | **联合 CPE**（复用 FOE 共轭积先验）| **Doppler 斜率前馈** | 共享 LO 合并后联合补偿 | B3-Q2 增量 = M2 + CPE 联合 + Doppler 维度 |

**fair gain 定义**（防继承）：
- `gain_vs_M1 = M1.BER - M3.BER`（含 jphot 继承增益——**不作为 Go 判据**，仅参考）
- `gain_vs_M2 = M2.BER - M3.BER`（**B3-Q2 真实增量**——Go 判据用这个）
- **Go 标准**（D005/FR-25）：`gain_vs_M2 > 0`（B3-Q2 联合 vs jphot FSTS 有新增益），且 @ HD-FEC 3.8e-3 灵敏度改善 ≥ 几 dB 量级（D005 务实门槛）或 ≥0.5dB（FR-21 参考门槛，不卡 Kill）

**🔴 增益归因熔断**（sandbox 触发）：若 `gain_vs_M2 ≤ 0`（B3-Q2 打不过 jphot FSTS）→ **先不直接 Kill，进分层判据第二/三层（见 0.4.5）**。全条件持平不代表无信号——S013 教训：NDA-ML 全条件判据跑 9 对话全堵死，最后是 A4 条件切换才出信号。

### 0.4.3 场景配置（单链路强湍为主）

| 场景 | 支路数 | 湍流 | Doppler | 优先级 | 说明 |
|---|---|---|---|---|---|
| **S1 单链路强湍 + Doppler** | 1 | strong（Cn²=1e-14）| LEO f_dot（破缓变假设）| **主场景** | dB 最显著（单支路 1.17dB）+ B3-Q2 Doppler 切口对口 |
| S2 单链路强湍 无 Doppler | 1 | strong | 0 | 对照 | 验证 Doppler 维度的增量（S1 vs S2 差异 = Doppler 贡献）|
| S3 多支路（2/4）强湍 | 2/4 | strong | LEO f_dot | 加分项 | jphot 原场景，验证多支路是否压缩增益（0.1b 结论：4 支路反而 < 单支路）|

**评估指标**：
- BER vs 接收光功率（@ HD-FEC 3.8e-3 灵敏度 dB）——主指标
- FOE MSE（方差域）——诊断（对照 0.1b 的 26dB 方差域余量）
- CPE RMSE（度）——诊断 CPE 联合贡献
- fair gain @ HD-FEC（gain_vs_M1 / gain_vs_M2）——Go 判据

### 0.4.4 消融设计（归因 CPE 联合 vs Doppler 维度各自贡献）

为了区分"CPE 联合贡献"和"Doppler 维度贡献"（两者都是 B3-Q2 增量切口，需分别归因）：

| 消融变体 | CPE | Doppler | 测什么 |
|---|---|---|---|
| M3a = M2 + CPE 联合（无 Doppler） | 联合 | 无 | CPE 联合的独立贡献 |
| M3b = M2 + Doppler（独立 CPE） | 独立 | 前馈斜率 | Doppler 维度的独立贡献 |
| M3 = M2 + CPE 联合 + Doppler | 联合 | 前馈斜率 | 全量增量 |

**归因判据**：
- `CPE 贡献 = M3a - M2`；`Doppler 贡献 = M3b - M2`；`协同贡献 = M3 - M3a - M3b - M2`
- 若 CPE 贡献 <10% → CPE 联合无效（0.1b CRB 预警 ≈0dB 可能坐实）
- 若 Doppler 贡献 <10% → Doppler 维度无效（缓变假设下 Doppler 无害但也无益）
- 两者都 <10% → B3-Q2 无真实增量，转 Kill

### 0.4.5 分层 Go 判据（adaptation-scan A4/A6 降级保底，S013 教训）

> 来源：`_adaptation_scan_b3.md`（sandbox 前必扫 A1-A6）。S013 NDA-ML 教训：全条件 Go 判据过严，A4 条件切换才是出信号方向。B3-Q2 同理——全条件赢 jphot FSTS 先验不高（CPE CRB≈0dB + Doppler 无锚），应留 crossover/失效边界保底路。

**分层判据**（从严到宽，上一层 FAIL 进下一层，全 FAIL 才 Kill）：

| 层 | 判据 | Go 卖点 | Kill 触发 |
|---|---|---|---|
| **L1 全条件**（最强）| `gain_vs_M2 > 0`（全条件）+ CPE/Doppler 贡献各 ≥10% | "联合估计全条件优于分立管线" | gain_vs_M2 ≤ 0 或接近 0（进 L2）|
| **L2 Doppler crossover**（A4 降级）| 扫 f_dot 维度找 M2/M3 交叉点，高 Doppler 区 `gain_vs_M2 > 0` 且物理因果清晰（jphot-L208 缓变假设失效）| **"高动态条件下联合估计的特长场景"**（对齐导师特长标准）| 无 crossover（进 L3）|
| **L3 失效边界**（A6 降级）| jphot 在高 Doppler 直接失效（BER 爆/发散），B3-Q2 仍工作 | **"扩展 jphot FSTS 适用边界"**（鲁棒性叙事）| 失效边界相同 → **真 Kill** |

**L2/L3 的叙事要求**：
- L2（crossover）：必须用 Doppler 动态强度作 crossover 轴，**不能跟 NDA-ML A4 的 SNR 驱动 crossover 混淆**（物理量正交：确定性 Doppler vs 随机 SNR 衰落）。论文若同时发两篇条件切换，必须显式区分叙事
- L3（失效边界）：dB 可能很大（jphot 崩了），但需 framing 为"鲁棒性/适用范围"不是"增益"——审稿人可能质疑"从崩到工作"的价值

**与 0.4.2/0.4.4 的关系**：
- 0.4.2 的 `gain_vs_M2 > 0` 是 L1 全条件判据（最强 Go）
- 0.4.4 的消融（CPE/Doppler 各自 <10%）在 L1 层仍适用；L2/L3 层只看 Doppler 维度（CPE 联合若 L1 全 FAIL 则不作为主卖点）
- 增益归因熔断（防 jphot 继承）在所有层都守——L2/L3 的增益也必须 vs M2（jphot FSTS），不能只 vs M1（传统 TS）

---

## 阶段 0.5：参数真相源（TL-26/FR-20，全标 source + 读原文）

### 0.5.1 参数表（复用 `_stage0_1b` L9-36 已核 source + 补 Doppler 维度）

> **纪律**：所有数值读自原文（`papers/doi/10.1109_jphot.2023.3265847/content.md`），不靠笔记转录（D002 教训）。已 grep 核验。

| 参数 | 值 | source（jphot content.md 行号）| 备注 |
|---|---|---|---|
| 调制 / 符号率 | PM 4-QAM, 10 GBaud | jphot-L231 | 主调制；16-QAM 对照 |
| 强湍 Cn² | 1e-14 m⁻²/³ | jphot-L241（Fig.15-17 标注）/ L357（正文 strong turbulence Cn²=1e-14）| **已 grep L357 双源确认** |
| 弱湍 Cn² | 1e-16 m⁻²/³ | jphot-L355（Fig.16 标注 Cn²=1e-16）| 对照 |
| 链路距离 z | 10 km | jphot-L241（相位屏仿真）| |
| 强湍平均耦合效率 | 4.8395% | jphot-L243 | 极低 → 单链路低 SNR 区 |
| 激光线宽 Δν | 50 kHz | jphot-L231/L243 | 发射 + 各支路 LO 共享 |
| LO 输出功率 | 15 dBm | jphot-L243 | |
| 光电二极管响应度 | 0.8 A/W | jphot-L243 | |
| 接收望远镜口径 | 0.2 m | jphot-L243 | 单孔径 |
| TS 优化总长 | 320 符号（4-QAM: BN=16, BL=20）| jphot-L299 | |
| 块长 BL（4-QAM, 320）| 20 | jphot-L289/L299 | BL²=400 降噪因子 |
| FOE 估计范围 | [−Rs/2, +Rs/2] | jphot-L183 | ±5GHz @ 10GBaud |
| 频偏随机范围 | (−1.1, +1.1) GHz | jphot-L319/L339 | jphot 测试范围 |
| FEC 门限 | 3.8e-3 | jphot-L329/L357 | HD-FEC |
| FOE-MSE 陡崖 | 2.5e-7（恶化）/ 6.25e-6（严重）| jphot-L279 | 封顶可兑现增益 |
| **🔴 单支路 4-QAM 强湍实测** | **+1.03dB（960sym）/ +1.17dB（320sym）** | jphot-L375（Fig.18 "1.17 dB ... strong"）| **0.1b grep 核验 PASS** |
| 4 支路 4-QAM 强湍 | +0.7dB | jphot-L375 | < 单支路 |
| 2 支路 4-QAM 强湍 | +2.09dB | jphot-L375/L385 | D002 修正：2 支路才 +2~3dB |
| 2 支路 16-QAM 强湍 | +3.41dB | jphot-L375/L385 | |

### 0.5.2 B3-Q2 新增参数（Doppler 维度，需标 source）

| 参数 | 值（草案）| source | 备注 |
|---|---|---|---|
| LEO Doppler 斜率 f_dot | 待 sandbox 标定（量级 1e6~1e9 Hz/s）| common `_config.py` DOPPLER_HIGH | common 已建模 f_dot，B3-Q2 复用 |
| Doppler 全量程 | ±几 GHz（LEO 可见弧段）| B5 主题参考（Vieira α=17GHz）| 块内 FOE ±Rs/2 够，块间靠斜率外推 |
| Doppler 残余 f_res | ~1MHz 量级 | common F_RESIDUAL | 星历预测预补偿后残余 |
| 多支路数（S3 场景）| 2 / 4 | jphot Fig.18 | 加分项 |
| 多望远镜间距 | > 空间相干长度（jphot 未给具体值）| INVARIANT 7 | 待 sandbox 设 |

**⚠️ Doppler 参数溯源债务**：f_dot 精确值需读 B5 锚 optcom.2024.130981 / Vieira 2023 原文（本轮不深查，sandbox 前补）。标"未验证，范围 X-Y"（FR-20 诚实标注）。

### 0.5.3 B3Params 草稿（接口定义，sandbox 阶段实例化）

```python
# explore/b3-joint-estimation/_b3_params.py（阶段 0.6 接口，sandbox 前实例化）
from dataclasses import dataclass

@dataclass
class B3Params:
    # 信道（复用 common，TL-13）
    cn2: float = 1e-14          # 强湍 jphot-L357
    z_km: float = 10.0          # jphot-L241
    lw_hz: float = 50e3         # jphot-L231
    aperture_m: float = 0.2     # jphot-L243
    # TS（jphot FSTS）
    ts_total: int = 320         # jphot-L299
    bl: int = 20                # jphot-L289 BL²=400
    bn: int = 16                # jphot-L299
    # Doppler（B3-Q2 增量维度）
    f_dot: float = 1e6          # 待 sandbox 标定，溯源债务
    f_res: float = 1e6          # common F_RESIDUAL
    # 多支路（S3 加分项）
    n_branches: int = 1         # 主场景单链路
    # 评估
    fec_threshold: float = 3.8e-3  # jphot-L329 HD-FEC
    r_sym_baud: float = 10e9    # jphot-L231
```

---

## 阶段 0.6：文件组织规约 + 新建代码接口（INVARIANT 14）

### 0.6.1 目录结构

```
projects/simulation/explore/b3-joint-estimation/
├── _diversity_migration_validation.md       # 0.1 主线判定（已存）
├── _a1_attribution_audit.md                 # 0.2 A1 归属（已存）
├── _stage0_1a_aperture_diversity_scene_survey.md  # 0.1a 子 agent（已存）
├── _stage0_1b_single_link_crb_upper_bound.md      # 0.1b 子 agent（已存）
├── _architecture_decision.md                # 0.3 架构定性（本轮新建）
├── _fair_comparison_framework.md            # 0.4-0.6 本文件
├── _bupt_followup_audit.md                  # BUPT 续作核查（子 agent 产出）
├── _param_truth_source.md                   # 0.5 参数表（本文件 §0.5 即此）
├── _b3_params.py                            # B3Params（sandbox 前实例化）
├── _b3_mve_spec.md                          # sandbox 阶段 MVE 契约（待写）
├── mrc_combiner.py                          # 新建① MRC 合并器
├── frame_sync_fsts.py                       # 新建② 帧同步 FSTS 相关峰
├── multi_branch_phase_precorr.py            # 新建③ 多支路相位预校正
├── joint_estimation_pipeline.py             # 新建④ 联合估计管线（前馈开环）
├── multi_aperture_channel.py                # 新建⑤ 多望远镜信道扩展
├── b3_joint_mve.py                          # MVE 脚本（sandbox 阶段）
└── results/                                 # 结果输出
```

### 0.6.2 五个新建代码接口（INVARIANT 14，sandbox 阶段实现，本轮只定接口）

> **纪律**：单支路估计器（fft_foe/vv_cpr/bps_cpr/da_ml/nda_ml/gardner_ted/psa_foe/short_time_spectrum）从 `common/_recovery.py` 复用作子组件；多支路扩展在 explore 做，**不进 common**（TL-13/INVARIANT 8）。

#### ① MRC 合并器（`mrc_combiner.py`）

```python
def mrc_combine(branches: list[np.ndarray], h_branches: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """最大比合并（jphot-L101 共享 LO 合并后联合补偿）。

    Args:
        branches: 各支路复数信号 [r_1, r_2, ..., r_K]（已相位预校正）
        h_branches: 各支路信道增益 [h_1, h_2, ..., h_K]
    Returns:
        combined: MRC 合并后信号
        weights: 各支路合并权重（诊断用）
    数学: combined = sum_k conj(h_k) * r_k / |h_k|² （归一化 MRC）
    """
```

#### ② 帧同步 FSTS 相关峰（`frame_sync_fsts.py`）

```python
def fsts_frame_sync(branches: list[np.ndarray], ts_template: np.ndarray, bl: int) -> tuple[list[int], np.ndarray]:
    """FSTS 帧同步 + 支路时延对齐（jphot-L101 FS 相关峰搜索）。

    Args:
        branches: 各支路接收信号
        ts_template: FSTS 训练序列模板（X/Y 极化交织共轭对称，jphot-L107）
        bl: 块长（jphot-L289 BL=20）
    Returns:
        offsets: 各支路 TS 起点偏移（对齐支路时延）
        corr: 相关峰序列（诊断用）
    数学: 跨极化共轭相关 peak detection，jphot-L101 "TS is firstly used for FS"
    """
```

#### ③ 多支路相位预校正（`multi_branch_phase_precorr.py`）

```python
def multi_branch_phase_precorrect(
    branches: list[np.ndarray], offsets: list[int],
    df_est: float, f_dot_est: float, phi_est: np.ndarray,
) -> list[np.ndarray]:
    """各支路相位预校正（FOE + Doppler 斜率 + CPE 前馈补偿，合并前）。

    Args:
        branches: 各支路信号（FS 对齐后）
        offsets: 各支路时延偏移（来自 fsts_frame_sync）
        df_est: 块内频偏（两段式 FOE 输出，jphot-L175）
        f_dot_est: 块间 Doppler 斜率（B3-Q2 增量，前馈回归）
        phi_est: CPE 相位轨迹（VV/BPS 或联合 CPE 输出）
    Returns:
        precorrected: 各支路预校正后信号（待 MRC 合并）
    数学: r_k_precorr = r_k * exp(-j*(2π·df·(n-offset_k)·Ts + π·f_dot·(n·Ts)² + phi_est[n]))
    """
```

#### ④ 联合估计管线（`joint_estimation_pipeline.py`）—— 核心接口

```python
def b3_joint_pipeline(
    branches: list[np.ndarray], ts_template: np.ndarray,
    mode: str = 'full',  # 'full'=M3 / 'm2_fsts'=M2 / 'm1_traditional'=M1
    params: 'B3Params' = None,
) -> dict:
    """B3-Q2 前馈开环联合估计管线（0.3 架构决策实现）。

    流程（逐块前馈，不进环路，0.3 架构）:
        [1] FS: fsts_frame_sync → 支路时延对齐
        [2] FOE: 两段式（fft_foe 粗 + jphot-L208 细 BL²）→ df_est
        [3] Doppler: 块间 df_est 序列线性回归 → f_dot_est（B3-Q2 增量，仅 mode='full'）
        [4] CPE: VV/BPS 或联合 CPE（复用 FOE 共轭积先验，仅 mode='full' 联合）
        [5] 预校正: multi_branch_phase_precorrect（FOE+Doppler+CPE 前馈）
        [6] MRC: mrc_combine → 合并后信号
        [7] 解调 + BER

    Args:
        branches: 各支路接收信号
        ts_template: FSTS 模板
        mode: 'full'(M3)/'m2_fsts'(M2 jphot)/'m1_traditional'(M1)
        params: B3Params
    Returns:
        dict: {rx_combined, ber, df_est, f_dot_est, phi_est, offsets, ...}
    注: mode='m2_fsts' 跳过 [3] Doppler + [4] 用独立 CPE；mode='m1_traditional' 用传统单段 FOE
    """
```

#### ⑤ 多望远镜信道扩展（`multi_aperture_channel.py`）

```python
def generate_multi_aperture_realization(
    n_branches: int, Ns: int, gamma_bar: float, turb_name: str,
    f_dot: float, aperture_spacing_m: float, seed: int = 42,
) -> dict:
    """多望远镜信道实现（INVARIANT 14，从 common/_channel.py 单支路扩展，不进 common）。

    Args:
        n_branches: 支路数（望远镜数）
        Ns, gamma_bar, turb_name, f_dot: 同 common generate_shared_realization
        aperture_spacing_m: 望远镜间距（> 空间相干长度才独立分集）
        seed: 随机种子
    Returns:
        dict: {branches: list[np.ndarray], h_branches, phi_shared, ...}
    实现:
        - 各支路独立 Gamma-Gamma 块衰落（若间距 > 相干长度）或相关（若 < 相干长度）
        - 共享 LO → 共享频偏/Doppler/CPE 相位（jphot-L101 共享 LO 假设）
        - 各支路独立 AWGN
        - 守 TL-13: 单支路极限退化到 common generate_shared_realization
    """
```

### 0.6.3 复用清单（从 common/_recovery.py + _channel.py 导入，不重写）

| 组件 | 来源 | 用途 |
|---|---|---|
| `generate_shared_realization` / `generate_shared_realization_apsk` | common/_channel.py | 单支路信道（S1/S2 场景） |
| `gg_block` / `doppler_phase` | common/_channel.py | 信道组件（多支路扩展用） |
| `fft_foe` | common/_recovery.py | FOE 粗估（两段式第一段） |
| `vv_cpr` / `bps_cpr` | common/_recovery.py | CPE（独立 CPE baseline + 联合 CPE 子组件） |
| `dpll_track` | common/_recovery.py | 对照（传统 DPLL，非 B3-Q2 主用） |
| `T_S` / `LASER_LW` / `TURB` / `BLOCK` | common/_config.py | 参数 |

### 0.6.4 不进 common 的边界（TL-13/INVARIANT 8）

- MRC 合并器 / 帧同步 FSTS / 多支路相位预校正 / 联合估计管线 / 多望远镜信道——**全部在 explore/b3-joint-estimation/ 内**
- 仅当某组件被 ≥2 个候选（B3 + 其他）复用时才考虑进 common（当前只 B3 用，不进）

---

## 方法局限（诚实标注）

1. **CPE 联合增益预期偏薄**（0.1b CRB ≈0dB）：0.4 消融设计专门验证，可能 sandbox 发现 CPE 联合 <10% 贡献 → 该切口无效，B3-Q2 退化为"Doppler 维度 + 星地场景"两切口
2. **Doppler 参数 f_dot 溯源未完成**：本轮未深查 B5 锚 optcom.2024.130981 / Vieira 原文的 f_dot 精确值，sandbox 前需补（FR-20 债务）
3. **多望远镜间距参数无锚**：jphot 未给具体间距值，sandbox 需设（空间相干长度依赖 Cn² + 距离，需算）
4. **前馈 Doppler 外推误差未量化**：块间斜率外推的累积误差需 sandbox 验证（可能需多项式而非线性回归）
5. **BUPT 续作 SSRN 2025 + OECC 2026 abstract 未亲验**（子 agent 标注）：若 BUPT 已发"星地分集+CPE/Doppler 联合"汇合论文，B3-Q2 增量被吞——sandbox 前需补 CNKI 核查张思齐学位论文 + 亲验 SSRN/OECC abstract
