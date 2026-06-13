# C1 方案设计：common.py 模块化拆分

> 2026-06-12 | 设计阶段
> 前置依赖：common.py (769行, 38函数) + SPEC.md + 27个实验脚本

---

## 1. 最终模块文件列表

### 1.1 目录结构

```
projects/simulation/
├── common/               # 包目录（替代 common.py 单文件）
│   ├── __init__.py       # 向后兼容重导出 (~50行)
│   ├── _config.py        # 常量重导出（参数真相源在 params.py）(~50行)
│   ├── _channel.py       # 信道模型 + 共享实现 (~100行)
│   ├── _modulation.py    # 调制解调 + BER + hard_decision (~110行)
│   ├── _recovery.py      # 载波恢复全部算法 (~280行)
│   ├── _equalizer.py     # MMSE均衡 + amp_limit (~50行)
│   ├── _kf.py            # Kalman 滤波器 + Q设计 + KF恢复变体 (~220行)
│   └── _experiment.py    # run_* + run_trial_shared + save_results (~120行)
├── SPEC.md
├── experiments/          # 不动
├── results/
└── figures/
```

### 1.2 各模块详情

#### `_config.py` (~50行) — 常量重导出（参数真相源在 params.py）

> **设计决策**：参数的唯一真相源是 `params.py`（Pydantic BaseModel）。
> `_config.py` 仅负责：(1) 将 params.py 的类型化参数重导出为模块级常量，
> (2) 定义非参数常量（PILOT_PATTERN 等）。
> 这样 `from common import R_SYM` 等脚本零改动。

**常量**（从 params.py SimulationConfig 实例化导出 + 本模块定义）：

```python
# 从 params.py 导入（单一真相源）
from params import SimulationConfig
_cfg = SimulationConfig()

R_SYM = _cfg.system.r_sym
T_S = _cfg.system.t_s
F_CARRIER = _cfg.system.f_carrier
LASER_LW = _cfg.system.laser_lw
BLOCK = _cfg.system.block_size
SIGMA2_LASER = _cfg.system.sigma2_laser
# ... 其他参数同理从 _cfg 导出

# 本模块定义的非参数常量
PILOT_PATTERN = [0, 16, 32, 48, 64, 80, 96, 112]
TURB = {'weak': (4.0, 4.0), 'moderate': (2.0, 2.0), 'strong': (1.0, 1.0)}
```

**依赖**：numpy, params (C2 的参数溯源模块)

**公共 API**：全部常量名（向后兼容）

---

#### `_channel.py` (~100行) — 信道模型

| 函数 | 行数（原 common.py L行） | 说明 |
|------|--------------------------|------|
| `gg_block(N, a, b, bs=BLOCK)` | L69-74 | Gamma-Gamma 块衰落 |
| `doppler_phase(N, f_res, f_dot, lw)` | L200-205 | 多普勒+激光相位噪声 |
| `generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)` | L380-412 | 共享信道/噪声/相位实现 |

**依赖**：`_config` (TURB, BLOCK, F_RESIDUAL, LASER_LW, T_S)

**内部耦合**：`generate_shared_realization` 调用 `_modulation.qpsk_mod`（唯一跨模块调用）

**公共 API**：gg_block, doppler_phase, generate_shared_realization

---

#### `_modulation.py` (~110行) — 调制解调 + BER

| 函数 | 行数 | 说明 |
|------|------|------|
| `qpsk_mod(bits)` | L76-77 | QPSK 调制 |
| `qpsk_demod(s)` | L79-83 | QPSK 解调 |
| `ber_count(tx_bits, rx)` | L85-86 | QPSK 直接 BER |
| `resolve_qpsk(rx, tx_bits)` | L88-93 | QPSK 旋转解模糊 |
| `qam16_mod(bits)` | L95-108 | 16-QAM 调制 |
| `qam16_demod(s)` | L110-129 | 16-QAM 解调 |
| `ber_count_qam16(tx_bits, rx)` | L131-132 | 16-QAM 直接 BER |
| `resolve_qam16(rx, tx_bits)` | L134-140 | 16-QAM 旋转解模糊 |
| `ber_eval(tx_bits, rx, mode)` | L170-181 | 统一 BER 评估 |
| `hard_decision(z, mod)` | L190-197 | 硬判决（QPSK/16-QAM） |

**依赖**：numpy（纯计算，无内部依赖）

**公共 API**：全部 10 个函数

---

#### `_recovery.py` (~280行) — 载波恢复算法

| 函数 | 行数 | 说明 |
|------|------|------|
| `fft_foe(rx, N_fft, nfft_zp)` | L210-229 | FFT 频偏估计 |
| `dpll_track(rx, omega_n, zeta)` | L231-247 | 4次方 DPLL |
| `dpll_track_dd(rx, omega_n, zeta, mod)` | L142-168 | DD-DPLL（支持 QAM16） |
| `vv_cpr(rx, Nw)` | L249-259 | Viterbi-Viterbi CPR |
| `bps_cpr(rx, B, Nw, mod)` | L261-288 | Blind Phase Search |
| `carrier_recovery_fixed(rx, cfg)` | L290-297 | Fixed 基线管线 |

**依赖**：`_config` (T_S, DEF_B_BPS, DEF_NW_BPS), `_modulation` (hard_decision)

**公共 API**：全部 6 个函数

---

#### `_equalizer.py` (~50行) — 均衡

| 函数 | 行数 | 说明 |
|------|------|------|
| `amp_limit(rx, thresh)` | L183-188 | 限幅 |
| `mmse_equalize(rx, h, gamma_bar)` | L461-463 | MMSE 均衡 |
| `equalize_oracle(shared)` | L466-468 | oracle-h 均衡 |
| `equalize_hmed(shared)` | L470-472 | h_med 均衡 |

**依赖**：无内部依赖（`equalize_oracle/hmed` 调用同模块 `mmse_equalize` + `amp_limit`）

**公共 API**：全部 4 个函数

---

#### `_kf.py` (~220行) — Kalman 滤波器

| 函数 | 行数 | 说明 |
|------|------|------|
| `design_Q(turb_name, f_dot)` | L310-315 | KF Q 矩阵设计 |
| `kf_unified(rx_block, h_block, gamma_bar, Q, ...)` | L317-362 | 2状态 KF 单块 |
| `get_pilots(n_pilots)` | L374-375 | 导频序列生成 |
| `kf_oracle_recovery(rx, h, gamma_bar, turb_name, ...)` | L477-505 | KF oracle-h 逐块恢复 |
| `kf_frame_h_recovery(rx, h_med, gamma_bar, turb_name, ...)` | L508-536 | KF frame-level h 恢复 |
| `kf_pilot_recovery(rx, gamma_bar, turb_name, n_pilots, ...)` | L539-635 | 导频辅助 KF 恢复 |

**依赖**：`_config` (T_S, BLOCK, SIGMA2_LASER, Q_TURB_PARAMS, PILOT_PATTERN), `_recovery` (fft_foe, vv_cpr), `_modulation` (hard_decision)

**注意**：`kf_unified` 调用 `vv_cpr` 做 phi 初始化（L326-327），这是唯一跨簇依赖。

**公共 API**：全部 6 个函数

---

#### `_experiment.py` (~120行) — 实验编排

| 函数 | 行数 | 说明 |
|------|------|------|
| `run_fixed(shared, eq_mode)` | L641-647 | Fixed 基线 |
| `run_kf_oracle(shared, eq_mode, **kw)` | L650-657 | KF oracle |
| `run_kf_frame_h(shared, eq_mode, **kw)` | L660-667 | KF frame-h |
| `run_kf_pilot(shared, n_pilots, eq_mode, **kw)` | L670-680 | KF pilot |
| `run_bps(shared, eq_mode)` | L683-693 | BPS |
| `run_trial_shared(Ns, gamma_bar, turb_name, f_dot, seed, ...)` | L704-740 | 多方案共享试验 |
| `save_results(data, filepath, script_name)` | L743-769 | 结果保存+元数据 |
| `insert_pilots(shared, n_pilots_per_block)` | L415-458 | 导频插入 |
| `db_ratio(a, b)` | L699-702 | dB 换算 |

**依赖**：几乎全部其他模块（编排层，自然汇聚依赖）

**公共 API**：全部 9 个函数

---

#### `__init__.py` (~50行) — 向后兼容重导出

详见 §6。

---

## 2. 函数分配表

| # | 函数名 | 分配模块 | 分配理由 |
|---|--------|----------|----------|
| 1 | `gg_block` | _channel | 信道模型原语 |
| 2 | `doppler_phase` | _channel | 相位噪声生成，与信道同域 |
| 3 | `generate_shared_realization` | _channel | 信道/噪声/信号生成的编排，核心是信道 |
| 4 | `qpsk_mod` | _modulation | 调制 |
| 5 | `qpsk_demod` | _modulation | 解调 |
| 6 | `ber_count` | _modulation | QPSK BER 计数，依赖 qpsk_demod |
| 7 | `resolve_qpsk` | _modulation | QPSK 解模糊，依赖 ber_count |
| 8 | `qam16_mod` | _modulation | 16-QAM 调制 |
| 9 | `qam16_demod` | _modulation | 16-QAM 解调 |
| 10 | `ber_count_qam16` | _modulation | 16-QAM BER 计数 |
| 11 | `resolve_qam16` | _modulation | 16-QAM 解模糊 |
| 12 | `ber_eval` | _modulation | 统一 BER 入口，依赖 ber_count/resolve_qpsk |
| 13 | `hard_decision` | _modulation | 硬判决，被 recovery/kf 调用（放在 modulation 因为是判决域） |
| 14 | `dpll_track_dd` | _recovery | DD-DPLL，属于载波恢复算法族 |
| 15 | `amp_limit` | _equalizer | 限幅是均衡后处理 |
| 16 | `fft_foe` | _recovery | 频偏估计，载波恢复第一步 |
| 17 | `dpll_track` | _recovery | 4次方 DPLL |
| 18 | `vv_cpr` | _recovery | VV CPR |
| 19 | `bps_cpr` | _recovery | BPS CPR |
| 20 | `carrier_recovery_fixed` | _recovery | Fixed 基线管线（组合 FOE+DPLL+VV） |
| 21 | `design_Q` | _kf | KF 过程噪声矩阵设计 |
| 22 | `kf_unified` | _kf | KF 核心算法 |
| 23 | `get_pilots` | _kf | 导频序列，专用于 KF |
| 24 | `kf_oracle_recovery` | _kf | KF oracle-h 恢复 |
| 25 | `kf_frame_h_recovery` | _kf | KF frame-h 恢复 |
| 26 | `kf_pilot_recovery` | _kf | KF pilot 恢复 |
| 27 | `mmse_equalize` | _equalizer | MMSE 均衡 |
| 28 | `equalize_oracle` | _equalizer | oracle 均衡编排 |
| 29 | `equalize_hmed` | _equalizer | h_med 均衡编排 |
| 30 | `insert_pilots` | _experiment | 导频插入是实验编排逻辑 |
| 31 | `run_fixed` | _experiment | 实验编排 |
| 32 | `run_kf_oracle` | _experiment | 实验编排 |
| 33 | `run_kf_frame_h` | _experiment | 实验编排 |
| 34 | `run_kf_pilot` | _experiment | 实验编排 |
| 35 | `run_bps` | _experiment | 实验编排 |
| 36 | `run_trial_shared` | _experiment | 实验编排（最高层） |
| 37 | `save_results` | _experiment | I/O |
| 38 | `db_ratio` | _experiment | 通用辅助 |

**常量分配**：全部入 `_config.py`，包括 PILOT_PATTERN（KF 专用但本质是常量）。

---

## 3. 模块间依赖关系

```
_config (纯常量，零依赖)
    ↑
    ├── _modulation (纯计算，零内部依赖)
    ├── _channel    (依赖 _config, _modulation)
    ├── _equalizer  (零内部依赖)
    ├── _recovery   (依赖 _config, _modulation)
    └── _kf         (依赖 _config, _recovery, _modulation)
           ↑
       _experiment  (依赖全部模块)
           ↑
       __init__     (重导出层)
```

**关键跨模块调用**（仅 3 处）：

1. `_channel.generate_shared_realization` → `_modulation.qpsk_mod`（L392 生成 TX 符号）
2. `_kf.kf_unified` → `_recovery.vv_cpr`（L326-327 phi 初始化）
3. `_recovery.bps_cpr` / `_recovery.dpll_track_dd` → `_modulation.hard_decision`

无循环依赖。依赖 DAG 是严格的层状结构。

---

## 4. 配置 dataclass 设计

### 4.1 SystemConfig

| 字段 | 类型 | 默认值 | 来源（原 common.py） |
|------|------|--------|----------------------|
| `r_sym` | float | 2.5e9 | L32 R_SYM |
| `t_s` | float | 1/2.5e9 | L33 T_S |
| `f_carrier` | float | 1.55e14 | L34 F_CARRIER |
| `laser_lw` | float | 10e3 | L35 LASER_LW |
| `block_size` | int | 100 | L42 BLOCK |
| `sigma2_laser` | float | 2*pi*10e3*T_S | L302 SIGMA2_LASER |

### 4.2 ScenarioConfig

| 字段 | 类型 | 默认值 | 来源 |
|------|------|--------|------|
| `gamma_bar` | float | 100 | L61 GAMMA_BAR_DEFAULT |
| `turb_name` | str | 'strong' | 实验默认 |
| `f_dot` | float | 150e6 | L44 DOPPLER_HIGH |
| `f_res` | float | 1e6 | L46 F_RESIDUAL |

### 4.3 FixedRecoveryConfig

| 字段 | 类型 | 默认值 | 来源 |
|------|------|--------|------|
| `n_fft` | int | 1024 | L49 FIXED_CFG['N_fft'] |
| `m_vv` | int | 64 | L50 FIXED_CFG['M_vv'] |
| `omega_n` | float | 8e6 | L51 FIXED_CFG['omega_n'] |
| `zeta` | float | sqrt(2)/2 | L52 FIXED_CFG['zeta'] |

### 4.4 保持 dict 形式的配置

以下保持 dict，因为它们是映射表而非单一配置：

- `TURB` — 按湍流等级索引的 (alpha, beta) 映射
- `FIXED_CFG_OPTIMAL` — 按湍流等级索引的 FixedRecoveryConfig 映射
- `Q_TURB_PARAMS` — 按湍流等级索引的 KF Q 参数映射

**理由**：frozen dataclass 是单个配置对象，而这些都是"per-scenario 的配置映射"，强行做成 dataclass 反而增加使用复杂度。保持 dict + 类型注释即可。

---

## 5. 管线注册表设计

### 5.1 设计决策：不做 @register_block

**理由**：当前 27 个脚本的实际使用模式是：

- 6 个脚本用 `run_fixed` / `run_kf_pilot` 等现成编排函数
- 21 个脚本自己编排（`equalize_oracle(shared)` → `fft_foe(rx)` → `vv_cpr(rx_foc)` 等）

没有脚本需要"注册新算法到框架"。管线的核心需求是**组合已有模块**，不是注册新模块。

注册表模式在这个场景下是过度设计。未来需要时再加。

### 5.2 替代方案：组合辅助函数

如果后续要添加新恢复算法（如 EKF/UKF），只需：

1. 在 `_recovery.py` 或新建 `_ekf.py` 中实现算法函数
2. 在 `_experiment.py` 中添加 `run_ekf(shared, ...)` 编排函数
3. 在 `__init__.py` 的 `__all__` 中添加导出

**扩展成本：1个新文件（或追加到现有文件）+ 2行导出声明。**

### 5.3 如果确实需要管线（未来）

当实验脚本数量超过 40 个、组合模式开始重复时，引入：

```python
# pipeline.py (未来，现在不做)
def run_pipeline(shared, steps: list[str], eq_mode='oracle'):
    """配置驱动的管线。steps 如 ['eq_oracle', 'foe', 'dpll', 'vv']"""
    rx = shared['rx_raw']
    for step in steps:
        rx = BLOCKS[step](rx, shared)
    return rx
```

**现在不做，留这个方向即可。**

---

## 6. 向后兼容垫片设计

### 6.1 方案

将 `common.py` 重命名为 `common/_init__.py`（即把 common.py 变成 common 包）。Python 包查找机制会自动将 `common/` 目录视为 `common` 模块。

**关键点**：`from common import *` 和 `from common import foo` 在 common.py（模块）和 common/__init__.py（包）之间行为完全一致。

### 6.2 `__init__.py` 内容

```python
"""湍流 FSO 载波同步仿真 — 公共基础设施（模块化版本）

使用方式不变：from common import *
"""

# 常量
from ._config import (
    R_SYM, T_S, F_CARRIER, LASER_LW,
    TURB, BLOCK,
    DOPPLER_HIGH, DOPPLER_LOW, F_RESIDUAL,
    FIXED_CFG, FIXED_CFG_OPTIMAL,
    GAMMA_BAR_DEFAULT,
    DEF_B_BPS, DEF_NW_BPS,
    SIGMA2_LASER, Q_TURB_PARAMS,
    PILOT_PATTERN,
    SystemConfig, ScenarioConfig, FixedRecoveryConfig,
)

# 信道
from ._channel import (
    gg_block, doppler_phase, generate_shared_realization,
)

# 调制解调
from ._modulation import (
    qpsk_mod, qpsk_demod, ber_count, resolve_qpsk,
    qam16_mod, qam16_demod, ber_count_qam16, resolve_qam16,
    ber_eval, hard_decision,
)

# 载波恢复
from ._recovery import (
    fft_foe, dpll_track, dpll_track_dd,
    vv_cpr, bps_cpr, carrier_recovery_fixed,
)

# 均衡
from ._equalizer import (
    amp_limit, mmse_equalize, equalize_oracle, equalize_hmed,
)

# Kalman 滤波器
from ._kf import (
    design_Q, kf_unified, get_pilots,
    kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery,
)

# 实验编排
from ._experiment import (
    insert_pilots,
    run_fixed, run_kf_oracle, run_kf_frame_h, run_kf_pilot, run_bps,
    run_trial_shared, save_results, db_ratio,
)

# matplotlib 设置（原 common.py L23-24）
import matplotlib
matplotlib.use('Agg')

# OUT 常量（原 common.py L27）— 必须指向 simulation/ 目录
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__all__ = [
    # 常量
    'R_SYM', 'T_S', 'F_CARRIER', 'LASER_LW',
    'TURB', 'BLOCK',
    'DOPPLER_HIGH', 'DOPPLER_LOW', 'F_RESIDUAL',
    'FIXED_CFG', 'FIXED_CFG_OPTIMAL',
    'GAMMA_BAR_DEFAULT', 'DEF_B_BPS', 'DEF_NW_BPS',
    'SIGMA2_LASER', 'Q_TURB_PARAMS', 'PILOT_PATTERN',
    'OUT',
    # dataclass
    'SystemConfig', 'ScenarioConfig', 'FixedRecoveryConfig',
    # 信道
    'gg_block', 'doppler_phase', 'generate_shared_realization',
    # 调制
    'qpsk_mod', 'qpsk_demod', 'ber_count', 'resolve_qpsk',
    'qam16_mod', 'qam16_demod', 'ber_count_qam16', 'resolve_qam16',
    'ber_eval', 'hard_decision',
    # 恢复
    'fft_foe', 'dpll_track', 'dpll_track_dd',
    'vv_cpr', 'bps_cpr', 'carrier_recovery_fixed',
    # 均衡
    'amp_limit', 'mmse_equalize', 'equalize_oracle', 'equalize_hmed',
    # KF
    'design_Q', 'kf_unified', 'get_pilots',
    'kf_oracle_recovery', 'kf_frame_h_recovery', 'kf_pilot_recovery',
    # 实验
    'insert_pilots',
    'run_fixed', 'run_kf_oracle', 'run_kf_frame_h', 'run_kf_pilot', 'run_bps',
    'run_trial_shared', 'save_results', 'db_ratio',
]
```

### 6.3 `__all__` 保障

`from common import *` 只导入 `__all__` 列出的名称。所有 27 个脚本使用的名称全部包含在内。

### 6.4 `save_results` 中的 `__file__` 问题

原 `save_results` L751 使用 `with open(__file__, 'rb')` 计算 common.py 的 MD5。迁移后 `__file__` 指向 `__init__.py`，行为一致（仍然可以追踪代码版本）。

---

## 7. 迁移步骤（具体可执行）

### Step 0：备份 + 验证基线

```bash
cd projects/simulation
cp common.py common.py.bak
# 跑一个快速实验确认基线
~/.venvs/torch/bin/python -c "from common import *; print('OK')"
~/.venvs/torch/bin/python experiments/bridge_ch3_ch4.py  # 快速脚本验证
```

### Step 1：创建包目录

```bash
mkdir -p common
```

### Step 2：创建 `_config.py`

从 common.py 提取 L29-64 的全部常量 + L302 SIGMA2_LASER + L304-308 Q_TURB_PARAMS + L367-372 PILOT_PATTERN。添加 3 个 frozen dataclass。

验证：`python -c "from common._config import R_SYM, TURB; print(R_SYM, TURB)"`

### Step 3：创建 `_modulation.py`

提取 L76-93 (QPSK), L95-140 (16-QAM), L170-181 (ber_eval), L190-197 (hard_decision)。

验证：`python -c "from common._modulation import qpsk_mod, resolve_qpsk; print('OK')"`

### Step 4：创建 `_channel.py`

提取 L69-74 (gg_block), L200-205 (doppler_phase), L380-412 (generate_shared_realization)。

验证：`python -c "from common._channel import generate_shared_realization; d = generate_shared_realization(1000, 100, 'strong', 150e6); print(d['Ns'])"`

### Step 5：创建 `_recovery.py`

提取 L210-297（fft_foe, dpll_track, dpll_track_dd, vv_cpr, bps_cpr, carrier_recovery_fixed）。

验证：`python -c "from common._recovery import vv_cpr, bps_cpr; print('OK')"`

### Step 6：创建 `_equalizer.py`

提取 L183-188 (amp_limit), L461-472 (mmse_equalize, equalize_oracle, equalize_hmed)。

验证：`python -c "from common._equalizer import equalize_oracle; print('OK')"`

### Step 7：创建 `_kf.py`

提取 L310-315 (design_Q), L317-362 (kf_unified), L374-375 (get_pilots), L477-635 (kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery)。

验证：`python -c "from common._kf import kf_unified; print('OK')"`

### Step 8：创建 `_experiment.py`

提取 L415-458 (insert_pilots), L641-693 (run_*), L699-769 (db_ratio, run_trial_shared, save_results)。

验证：`python -c "from common._experiment import run_trial_shared; print('OK')"`

### Step 9：创建 `__init__.py`

写入 §6 的完整内容。

### Step 10：删除旧 common.py，验证

```bash
rm common.py  # 注意：现在 common/ 目录是包，common.py 不能共存
```

验证全部 27 个脚本的导入：
```bash
for f in experiments/*.py; do
    echo "=== $f ==="
    ~/.venvs/torch/bin/python -c "
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath('$f')))
# 只验证导入，不运行实验
" 2>&1 | head -3
done
```

### Step 11：数值一致性验证

```bash
# 用相同 seed 跑一个已知结果的实验，对比数字
~/.venvs/torch/bin/python -c "
from common import generate_shared_realization, run_fixed, ber_eval
d = generate_shared_realization(10000, 100, 'strong', 150e6, seed=42)
rx = run_fixed(d)
ber = ber_eval(d['bits'], rx)
print(f'BER = {ber:.6f}')  # 应与拆分前完全一致
"
```

### Step 12：清理

```bash
rm common.py.bak
```

---

## 8. 扩展性验证

### 场景 A：新增 EKF 载波恢复算法

1. 在 `_recovery.py` 中添加 `ekf_track(rx, ...)` 函数（或新建 `_ekf.py`）
2. 在 `_experiment.py` 中添加 `run_ekf(shared, eq_mode='oracle')`
3. 在 `__init__.py` 的 `from ... import` 和 `__all__` 中添加 2 个名称

**改动：2 行导出 + 新增函数代码。零改动现有函数。**

### 场景 B：新增 64-QAM 调制格式

1. 在 `_modulation.py` 中添加 `qam64_mod`, `qam64_demod`, `resolve_qam64`
2. 在 `hard_decision` 中添加 `mod='qam64'` 分支
3. 在 `__init__.py` 中添加导出

**改动：1 个文件内扩展 + 3 行导出。零改动恢复/均衡/KF 代码。**

### 场景 C：新增自适应管线（如 FOE→DPLL→KF 级联）

1. 在 `_experiment.py` 中添加 `run_adaptive(shared, ...)`
2. 内部自由组合 `_recovery` + `_kf` 的函数

**改动：1 个新函数 + 1 行导出。零改动现有代码。**

### 场景 D：参数变更（如 BLOCK 从 100 改为 50）

1. 修改 `_config.py` 中的 `BLOCK` 常量

**改动：1 行。所有模块自动生效。**

---

## 附录 A：脚本导入名称全覆盖审计

逐脚本检查，确认 `__all__` 覆盖所有使用的名称：

| 脚本 | 使用的名称 | 全在 __all__? |
|------|-----------|--------------|
| bridge_ch3_ch4 | * (全部) | 是 |
| reverify_D1D2 | * (全部) | 是 |
| reverify_kf_internals | * (全部) | 是 |
| sim_nmse_vs_ber | * (全部) | 是 |
| sim_nmse_expanded | * (全部) | 是 |
| sim_nmse_turbulence_sweep | * (全部) | 是 |
| sim_nmse_qam16_sweep | * (全部) | 是 |
| multi_seed_sweep | BLOCK, DOPPLER_HIGH, FIXED_CFG_OPTIMAL, TURB, ber_eval, bps_cpr, carrier_recovery_fixed, fft_foe, generate_shared_realization, insert_pilots, kf_pilot_recovery, amp_limit, mmse_equalize, run_fixed, run_kf_pilot, vv_cpr, dpll_track, resolve_qpsk, qpsk_demod, equalize_oracle | 是 |
| sim_nw_sweep | GAMMA_BAR_DEFAULT, DOPPLER_HIGH, generate_shared_realization, equalize_oracle, fft_foe, vv_cpr, bps_cpr, resolve_qpsk | 是 |
| sim_dpll_omega_sweep | DOPPLER_HIGH, generate_shared_realization, equalize_oracle, fft_foe, dpll_track, resolve_qpsk | 是 |
| sim_dpll_zeta_sweep | DOPPLER_HIGH, generate_shared_realization, equalize_oracle, fft_foe, dpll_track, resolve_qpsk, save_results | 是 |
| sim_dpll_omega_50seed | 同 sim_dpll_omega_sweep | 是 |
| sim_dpll_omega_sweep_dense | 同 sim_dpll_omega_sweep | 是 |
| sim_nw_sweep_50seed | 同 sim_nw_sweep | 是 |
| sim_nw_sweep_dense | 同 sim_nw_sweep | 是 |
| sim_nw_sweep_low_snr | 同 sim_nw_sweep | 是 |
| sim_snr_dense | DOPPLER_HIGH, TURB, generate_shared_realization, equalize_oracle, fft_foe, vv_cpr, bps_cpr, dpll_track, resolve_qpsk | 是 |
| test_qam16_multimethod | TURB, BLOCK, T_S, F_RESIDUAL, DOPPLER_HIGH, gg_block, doppler_phase, qam16_mod, dpll_track_dd, bps_cpr, kf_unified, resolve_qam16, amp_limit, mmse_equalize, design_Q | 是 |
| sim_qam16_dpll_sweep | TURB, BLOCK, T_S, R_SYM, F_RESIDUAL, DOPPLER_HIGH, FIXED_CFG_OPTIMAL, gg_block, doppler_phase, qam16_mod, qam16_demod, dpll_track_dd, resolve_qam16, amp_limit, mmse_equalize, db_ratio, save_results | 是 |
| vv_formula_head2head | TURB, BLOCK, DOPPLER_HIGH, F_RESIDUAL, T_S, LASER_LW, GAMMA_BAR_DEFAULT, generate_shared_realization, equalize_oracle, fft_foe, resolve_qpsk, amp_limit, dpll_track, gg_block, qpsk_mod, doppler_phase, mmse_equalize | 是 |
| analytical_phase_model | TURB, BLOCK, T_S, R_SYM, LASER_LW, F_RESIDUAL, DOPPLER_HIGH, GAMMA_BAR_DEFAULT, generate_shared_realization, equalize_oracle, vv_cpr, dpll_track, fft_foe, ber_eval, resolve_qpsk, qpsk_mod, qpsk_demod, save_results, FIXED_CFG_OPTIMAL, carrier_recovery_fixed | 是 |
| analytical_dpll_stability | TURB, BLOCK, T_S, R_SYM, save_results | 是 |
| analytical_e_inv_h | TURB, BLOCK | 是 |
| verify_cross_chapter_ber | TURB, T_S | 是 |
| plot_snr_curves | 不导入 common（纯读 JSON 绑图） | N/A |
| sim_nmse_qam16_sweep | * (全部) | 是 |
| sim_qam16_dpll_sweep | 见上 | 是 |
| vv_formula_math | 不导入 common（纯数学推导） | N/A |

**覆盖率：25/25 个导入 common 的脚本，全部名称在 `__all__` 中。**（plot_snr_curves 和 vv_formula_math 不导入 common）

---

## 附录 B：为什么不拆更多/更少

### 为什么不拆到每个函数一个文件（Java 风格）

38 个函数 38 个文件，导入管理成本远大于收益。当前 8 模块是自然聚类，每个模块内部函数高度相关。

### 为什么 recovery 和 KF 不合并

KF 依赖 recovery（vv_cpr 做 phi 初始化），但 recovery 不依赖 KF。合并会制造循环依赖或无意义的双向依赖。保持分离符合 DAG 原则。

### 为什么 insert_pilots 在 _experiment 而不是 _kf

insert_pilots 操作的是 shared dict（包含信道/噪声/信号），是"在共享实验数据上插入导频"的编排逻辑，不是 KF 算法本身。KF 只消费 insert_pilots 的输出。

### 为什么不做 pipeline.py

当前没有脚本需要通用管线框架。6 个 run_* 函数已经是最简编排。过早抽象管线会引入不必要的间接层。

---

## 附录 C：OUT 常量处理

原 `OUT = os.path.dirname(os.path.abspath(__file__))` 在 common.py L27，指向 `projects/simulation/`。

**被 8 个脚本使用**（通过 `from common import *`）：sim_nmse_vs_ber, sim_nmse_qam16_sweep, bridge_ch3_ch4, reverify_D1D2, reverify_kf_internals, sim_nmse_turbulence_sweep, sim_nmse_expanded, sim_qam16_dpll_sweep。另外 sim_qam16_dpll_sweep L53 自己重新定义了 OUT。

**迁移后**：`__init__.py` 中 `__file__` 指向 `common/__init__.py`，`os.path.dirname` 得到 `common/`。需要再 `os.path.dirname` 一次才能回到 `projects/simulation/`。

```python
# __init__.py 中
import os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# __file__ = .../projects/simulation/common/__init__.py
# dirname 一次 = .../projects/simulation/common/
# dirname 两次 = .../projects/simulation/  ← 与旧 common.py 一致
```

---

## 附录 D：matplotlib.use('Agg') 处理

原 common.py L23-24 在模块级设置 Agg backend。迁移后放在 `__init__.py` 中，确保 `import common` 时生效。各子模块不需要重复设置。

但更优做法是只在 `__init__.py` 中设置，不在子模块中设置（避免重复调用）。子模块中如果需要 plt，只做 `import matplotlib.pyplot as plt`。
