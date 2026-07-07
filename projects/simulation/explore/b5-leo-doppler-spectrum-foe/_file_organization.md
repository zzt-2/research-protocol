# 阶段 0.6 文件组织规约 — explore 目录结构 + short_time_spectrum_foe 接口定义

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 来源: S003（工作对话对话 2）| 日期: 2026-07-08
> 纪律: INVARIANT 14（B5 特殊·代码基建新增需求）+ sim-preflight doc-discipline + D-007 教训 2（下游引用同步清单）+ NDA-ML E 类混乱防御
> 守: 阶段 0 不写代码，本文件只定文件组织规约 + 接口定义，实现留 sandbox

## 核心问题

NDA-ML 6 类混乱 E 类（文件混乱：MVE 薄包装 + 双套参数共存 + 两 results 目录，topic-index NDA-ML 6 类混乱表）就是文件组织没规约导致的。前置规约防此坑。

## explore 目录结构规约

### 目录位置

`projects/simulation/explore/b5-leo-doppler-spectrum-foe/`（不是根目录的 explore/）

### 命名规则

- **私有文件 `_` 前缀**：诊断/核查/草稿/探针脚本（不进 common，MVE 通过才转正）
- **正式文件无前缀**：SPEC / mve 脚本（MVE 通过后转 experiments/）
- **结果文件 `_results.json` / `_curve.png`**：跟探针脚本同名

### 当前文件清单（阶段 0 完成，6 文件）

| 文件 | 阶段 | 状态 | 说明 |
|---|---|---|---|
| `_qualification_path_validation.md` | 0.1 | ✅ 完成 | 够格路径验证（路径 C 成立）|
| `_db_range_sourcing_audit.md` | 0.2 | ✅ 完成 | dB/范围溯源（20 字段全溯源）|
| `_architecture_decision.md` | 0.3 | ✅ 完成 | 架构定性（前馈归一化 + 范围优势前提 PASS）|
| `_fair_comparison_framework.md` | 0.4 | ✅ 完成 | 公平对照框架（baseline + fair gain + 工作点 + 差异化）|
| `_b5_params_draft.md` | 0.5 | ✅ 完成 | B5Params 草稿（20 字段全溯源）|
| `_file_organization.md` | 0.6 | ✅ 完成 | 文件组织规约（本文件）|

### sandbox 阶段文件清单（对话 3 产出，规约预定）

| 文件 | 类型 | 说明 |
|---|---|---|
| `_short_time_spectrum_foe.py` | 探针脚本 | B5 核心算法实现（分块 FFT + 正负功率谱面积比 Rp-n + 星历预测调 LO + 前馈归一化）|
| `_leven_mthpower_foe.py` | 探针脚本 | [60] Leven Mth-power 祖师爷对照实现（时域 4 次方 + 500 样本相位增量）|
| `_sandbox_three_way.py` | sandbox 脚本 | 三方对照（B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power）|
| `_sandbox_results.json` | 结果 | 三方对照结果（fair gain 二维报告）|
| `_doppler_range_sweep.json` | 结果 | Doppler ±4.5GHz 全量程扫描（验证捕获范围）|
| `_turbulence_residual_sweep.json` | 结果 | 湍流下残频 σ 扫描（验证 0.3b 验证 2）|

### MVE 阶段文件清单（sandbox 通过后，对话 4 产出）

| 文件 | 类型 | 说明 |
|---|---|---|
| `B5-MVE-SPEC.md` | 正式 SPEC | MVE 契约（守 FR-11 架构摘要 + TL-20 理论预期表，仿 N1-MVE-SPEC.md §2）|
| `mve_b5_short_time_spectrum.py` | MVE 脚本 | 正式 MVE（MVE 通过后转 experiments/）|
| `results/` | 结果目录 | MVE 结果（单一目录，禁双 results——NDA-ML E 类教训）|

## short_time_spectrum_foe 接口定义

### 起点骨架（参考 fft_foe_m0_omega，sc_nda_ml_sim.py:137-166）

fft_foe_m0_omega 接口（已读，分块 FFT 部分可复用）：
```python
def fft_foe_m0_omega(rx, M0_power, N_fft=None):
    """M0 升幂 FOE: rx^M0 去调制 → FFT 找频峰 → /M0 还原 CFO (omega, rad/sample).
    返回 omega_est (rad/sample), 用于 exp(−j·omega·k) 补偿."""
    # 分块 FFT + Hanning 窗 + zero-pad + 抛物线插值找谱峰
```

**复用部分**：分块 FFT + Hanning 窗 + zero-pad + 抛物线插值（找谱峰的工程实现）
**不复用部分**：M0 升幂找谱峰 ≠ B5 正负功率谱面积比 Rp-n（机制不同，`_B5-...-increment.md:160` 确认）

### short_time_spectrum_foe 接口规约（sandbox 时实现）

```python
def short_time_spectrum_foe(
    rx: np.ndarray,
    n_fft: int = 16,           # B5 锚 L87 FFT 点数（B5Params.FFT_POINTS_B5）
    n_blocks: int = 1024,      # B5 锚 L87 均值滤波组数（B5Params.FFT_BLOCKS_B5）
    alpha: float = 6e8,        # B5 锚 L85 系数 α（B5Params.ALPHA_B5）
    fs: float = 2.5e9,         # 符号率（B5Params.R_SYM_B5）
    normalize_mode: str = 'block',  # 前馈归一化方案（0.3a 决策，sandbox 选最优）
    #   'block': 块内归一化（除以块总功率）
    #   'agc':   AGC 前置（归一化接收功率到固定电平）
    #   'ratio': 归一化功率比 Rp-n = (P_+ - P_-) / (P_+ + P_-)
    ephemeris_pred: float = 0.0,  # 星历预测频偏（Hz），B5 锚 L87 星历预测调 LO
) -> dict:
    """B5 短时谱 FOE: 分块 FFT → 正负功率谱面积比 Rp-n → 归一化频偏估计 Δfest → 星历预测调 LO.

    B5 锚 optcom.2024.130981 L71-87 算法（前馈开环，0.3a 确认）:
    1. 输入数据分块（n_fft 点/块，2 的幂次）
    2. 每块 FFT → 离散功率谱
    3. n_blocks 组 FFT 数据均值滤波（B5 锚 L87 1024 组）
    4. [前馈归一化] 消除湍流致慢包络幅度起伏（0.3a 方案 A/B/C，normalize_mode 选）
    5. 算正频率功率 P_+ vs 负频率功率 P_- 的比值 Rp-n（式 3）
    6. 归一化频偏估计 Δfest = α × Rp-n（式 2，α=6×10⁸，L85）
    7. + 星历预测频偏 → 调 LO 频率补偿

    返回 dict:
        'fest_hz': float,        # 估计频偏（Hz）
        'fest_omega': float,     # 估计频偏（rad/sample），用于 exp(−j·omega·k) 补偿
        'rp_n': float,           # 正负功率谱面积比（诊断用）
        'spectrum': np.ndarray,  # 均值滤波后功率谱（诊断用）

    纪律:
    - 前馈开环，无环路 TF（0.3a 决策，禁撞 D006）
    - normalize_mode 必须显式传参（禁默认不归一化）
    - 参数从 B5Params 导入（sim-preflight param-source.md，禁硬编码）
    """
```

### 公平对照接口规约（三方对照用）

```python
# 三方对照（sim-preflight V2/C7），都接受同一信道实现（TL-13）
def compare_three_way(rx_shared, tx_bits, params: B5Params, normalize_mode='block'):
    """三方对照: B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power.

    三方法都做前馈归一化（公平保证）+ 共用 rx_shared（TL-13）.
    返回 fair gain 二维报告 dict.
    """
    # 1. B5 短时谱 FOE（short_time_spectrum_foe）
    # 2. 传统 FFT FOE（common.fft_foe，主 baseline，0.4.1 决策）
    # 3. [60] Leven Mth-power（_leven_mthpower_foe.py，祖师爷对照，0.4.1 决策）
```

## 下游引用同步清单（D-007 教训 2 防御）

NDA-ML D-007 教训：参数改后没同步清理下游引用，致一致性检查假 PASS。B5-Q1 的下游引用同步清单：

| 参数变更触发 | 需同步的下游引用 | 检查方式 |
|---|---|---|
| B5Params 字段值变 | 所有 import B5Params 的脚本 | grep `from params import B5Params` / `B5Params.` |
| short_time_spectrum_foe 接口变 | sandbox 脚本 / MVE 脚本 / 三方对照 | grep `short_time_spectrum_foe` |
| normalize_mode 选定 | sandbox 脚本 default 参数 | grep `normalize_mode` |
| 信道参数变（湍流 Cn² / Doppler）| 从 common/_channel.py 导入处（TL-13，禁自建）| grep `from common._channel import` |

**纪律**（sim-preflight doc-discipline）：任何参数值/公式形式/信号模型/评估方法变更 → 必须在 handoff"约定变更"段记录 + 写使用日志。

## common 不污染原则（红线 6）

- **explore 阶段探针不直接进 common**（INVARIANT 14 + 红线 6）
- short_time_spectrum_foe 在 explore 验证通过（sandbox 三方对照 PASS + MVE consistency PASS）才转正进 `common/_recovery.py`
- [60] Leven Mth-power 同理，explore 验证通过才进 common
- 信道侧完全复用 `common/_channel.py`（TL-13，禁自建）

## 对 sandbox/MVE 的影响

- **sandbox 对话 3**：按本文件接口定义实现 `_short_time_spectrum_foe.py` + `_leven_mthpower_foe.py` + `_sandbox_three_way.py`，跑三方对照
- **MVE 对话 4**：sandbox 通过后写 `B5-MVE-SPEC.md`（含 TL-20 理论预期表）+ `mve_b5_short_time_spectrum.py`
- **转正**：MVE 通过后 short_time_spectrum_foe 进 `common/_recovery.py`，B5Params 进 `params.py`

## 来源

- S003（本轮工作对话）
- fft_foe_m0_omega（`sc_nda_ml_sim.py:137-166`）起点骨架参考
- fft_foe（`common/_recovery.py:37`）主 baseline
- B7/B2 explore 目录结构模式参照（`_` 前缀私有 + 正式文件无前缀）
- INVARIANT 14（topic-index，short_time_spectrum_foe 需新写 + common 不污染）
- D-007 教训 2（下游引用同步清单）+ NDA-ML E 类混乱防御
- sim-preflight doc-discipline（约定变更记录）+ param-source.md（参数单一字段读）
- TL-13（共用信道，从 common/_channel.py 导入）
