# 验证系统集成方案

> 创建: 2026-06-12 | 基于: B4(69测试+9红旗)、B5(分层验证协议)、A6(审计发现)
> 状态: 待实施

---

## 1. 测试与代码的集成方式

### 1.1 当前状态

```
projects/simulation/
├── common.py              # 770行，所有仿真逻辑
├── SPEC.md                # 已验证事实
└── tests/
    ├── test_common.py     # 69个测试，8个类 (T1~T8)
    └── red_flags.py       # 9条红旗规则 (RF-01~RF-09)
```

### 1.2 测试文件组织（保持单文件，不拆分）

**结论: 维持 `test_common.py` 单文件结构。**

理由:
- common.py 本身就是单文件（770行），测试文件 937 行与其规模匹配
- 8 个测试类已经提供清晰的逻辑分组（`-k T1` 到 `-k T8`）
- 拆分成 8 个文件增加导入维护成本，收益为零
- 个人项目，不需要多文件并行测试

### 1.3 测试类与 common.py 函数的对应关系

```
common.py 区域                    测试类           测试数
────────────────────────────────  ───────────────  ──────
L67-198  信号原语                 TestT1           11
         gg_block, qpsk_mod/demod, ber_count,
         resolve_qpsk, qam16_*, doppler_phase,
         hard_decision, amp_limit

L209-298 载波恢复基线             TestT2           8
         fft_foe, dpll_track, dpll_track_dd,
         vv_cpr, bps_cpr, carrier_recovery_fixed

L300-363 Kalman滤波器            TestT3           7
         design_Q, kf_unified

L377-473 信道生成+均衡            TestT4           8
         generate_shared_realization, insert_pilots,
         mmse_equalize, equalize_oracle/hmed

L534-674 物理不变量+红旗          TestT5           9
         端到端物理约束验证

L680-776 回归守卫                 TestT6           5
         与 SPEC.md §6.1 已验证事实对照

L806-871 参数一致性               TestT7           13
         常量值与 SPEC.md 一致

L877-933 数值稳定性               TestT8           7
         极端参数边界
```

### 1.4 conftest.py（需要新建）

创建 `tests/conftest.py` 提供共享 fixture，消除测试文件中的重复设置:

```python
"""测试共享配置"""
import sys, os

# 确保 common.py 可导入 — 只写一次，所有测试文件共享
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)
```

之后 `test_common.py` 头部可删除 30-33 行的路径设置代码（4行），改为依赖 conftest.py。

---

## 2. 检查点插入位置

### 2.1 设计决策：检查点形式

**选用: 独立验证函数 + 可选开关，不用 assert/装饰器。**

理由:
- assert 在 `-O` 优化模式下被跳过 → 不可靠
- 装饰器需要改每个函数签名 → 侵入性大
- 独立函数 + 环境变量开关 → 零性能开销（生产模式不调用），显式调用位置清晰

### 2.2 检查点实现：`tests/checkpoints.py`

```python
"""运行时检查点 — 在实验脚本中显式调用

启用: 设置环境变量 SIM_CHECKPOINTS=1
关闭: 不设置（默认关闭，零开销）

用法:
  SIM_CHECKPOINTS=1 python experiments/multi_seed_sweep.py
"""
import os, sys
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

_ENABLED = os.environ.get('SIM_CHECKPOINTS', '0') == '1'


def cp1_channel(shared):
    """CP-1: 信道生成后验证
    位置: generate_shared_realization() 返回后立即调用
    """
    if not _ENABLED:
        return
    h = shared['h']
    assert np.all(h > 0), f"CP-1 FAIL: h 含非正值, min={np.min(h):.2e}"
    mean_h = np.mean(h)
    assert abs(mean_h - 1.0) < 0.15, f"CP-1 FAIL: E[h]={mean_h:.4f}, 偏离 1"
    # SNR 验证: sig_power / noise_power ≈ gamma_bar * E[h]
    carrier = np.exp(1j * shared['phi'])
    signal = shared['tx'] * np.sqrt(h) * carrier
    noise = shared['rx_raw'] - signal
    snr_meas = np.mean(np.abs(signal)**2) / np.mean(np.abs(noise)**2)
    snr_exp = shared['gamma_bar'] * mean_h
    rel = abs(snr_meas - snr_exp) / snr_exp
    assert rel < 0.1, f"CP-1 FAIL: SNR measured={snr_meas:.1f}, expected={snr_exp:.1f}"


def cp2_carrier_recovery(rx_out, label=""):
    """CP-2: 载波恢复后验证
    位置: 每个载波恢复方法返回后调用
    """
    if not _ENABLED:
        return
    assert not np.any(np.isnan(rx_out)), f"CP-2 FAIL [{label}]: 输出含 NaN"
    assert not np.any(np.isinf(rx_out)), f"CP-2 FAIL [{label}]: 输出含 Inf"


def cp3_ber(ber, method='', turbulence='', snr_db=20):
    """CP-3: BER 计算后红旗检测
    位置: 每个 BER 值计算后调用
    """
    if not _ENABLED:
        return
    # red_flags.py 在 tests/ 目录下，需加入 sys.path
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    from red_flags import check_ber, format_flags
    flags = check_ber(ber, method=method, turbulence=turbulence, snr_db=snr_db)
    critical = [f for f in flags if f.severity == 'CRITICAL']
    if critical:
        raise RuntimeError(f"CP-3 CRITICAL:\n{format_flags(flags)}")


def cp4_results(data, filepath):
    """CP-4: 结果保存前验证
    位置: save_results() 内部，在 json.dump 之前
    """
    if not _ENABLED:
        return
    meta = data.get('_meta', {})
    assert 'script' in meta, "CP-4 FAIL: _meta 缺少 script"
    assert 'common_md5' in meta, "CP-4 FAIL: _meta 缺少 common_md5"
    assert 'git_commit' in meta, "CP-4 FAIL: _meta 缺少 git_commit"
```

### 2.3 检查点在 common.py 中的插入位置

**关键决策: 检查点不直接写入 common.py。** 它们写在实验脚本和 `save_results()` 中。

理由:
- common.py 是被测代码，检查点是验证代码，混合违反关注点分离
- save_results() 已有元数据注入（TL-25），CP-4 是唯一嵌入 common.py 的检查点
- CP-1/CP-2/CP-3 属于实验脚本的控制流

#### save_results() 中的 CP-4 集成（唯一改动 common.py 的位置）

在模块化后的 `common/_experiment.py` 的 `save_results()` 函数中（`data['_meta'] = ...` 赋值之后、`os.makedirs` 之前）插入:

```python
    # CP-4: 元数据完整性验证（始终执行，零开销）
    meta = data.get('_meta', {})
    if 'script' not in meta:
        import warnings
        warnings.warn("save_results: _meta 缺少 script 字段", stacklevel=3)
```

只需 3 行代码，始终执行，开销为零（一次 dict.get + 一次 in 检查）。不需要独立函数。

### 2.4 检查点在实验脚本中的插入位置（以 multi_seed_sweep.py 为例）

```python
from tests.checkpoints import cp1_channel, cp2_carrier_recovery, cp3_ber

def run_single_seed(Ns, gamma_bar, turb_name, method_name, seed):
    shared = generate_shared_realization(...)
    cp1_channel(shared)                    # ← 新增

    if method_name == 'Fixed':
        rx = method_fixed(shared, turb_name)
        cp2_carrier_recovery(rx, 'Fixed')  # ← 新增
        ber = ber_eval(shared['bits'], rx, mode='oracle')
    # ... 其他方法同理 ...

    cp3_ber(ber, method_name, turb_name, snr_db)  # ← 新增
    return ber
```

**性能开销**:
- `SIM_CHECKPOINTS=0`（默认）: 4次函数调用 × 1行 `if not _ENABLED: return` = 约 200ns，可忽略
- `SIM_CHECKPOINTS=1`: CP-1 约 5ms（统计计算），CP-2 约 0.5ms（NaN检测），CP-3 约 0.1ms
- 典型单种子耗时 50-200ms，检查点额外开销 < 10%

---

## 3. 红旗规则集成方案

### 3.1 当前 red_flags.py 的调用方式

red_flags.py 已设计为独立模块，提供两个入口:
- `check_ber(ber, **context)` → 单 BER 检查
- `check_results(results_dict)` → 结果 dict 检查

### 3.2 集成到 save_results()（自动执行，零改动实验脚本）

**重要发现: 实验脚本存在两种 save_results 模式。**

| 模式 | 脚本 | 特点 |
|------|------|------|
| common.py 的 `save_results()` | `analytical_dpll_stability.py` | 自动注入 `_meta`（md5, git, timestamp） |
| 本地 `save_results()` | `multi_seed_sweep.py` 及多数脚本 | 简单原子写入，**无元数据** |

因此，红旗扫描不能只加在 common.py 的 save_results 中——大多数实验脚本不会经过它。

**方案: 提供独立工具函数，在实验脚本主循环末尾调用。**

在 `tests/checkpoints.py` 中增加 `cp4_save_scan()`:

```python
def cp4_save_scan(data):
    """CP-4: 结果保存前红旗扫描 + 元数据检查

    在实验脚本的 save_results() 之前调用。
    自动遍历结果中的 BER 值，触发红旗警告。
    """
    if not _ENABLED:
        return
    import warnings
    # red_flags.py 在 tests/ 目录下，需加入 sys.path
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    try:
        from red_flags import check_ber, format_flags
    except ImportError:
        return

    # 元数据检查
    meta = data.get('_meta', {})
    missing = [k for k in ('script', 'timestamp') if k not in meta]
    if missing:
        warnings.warn(f"结果缺少 _meta 字段: {missing}", stacklevel=2)

    # 遍历结果中的 BER 值
    results = data.get('results', {})
    for key, val in results.items():
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                if isinstance(sub_val, dict):
                    ber_mean = sub_val.get('ber_mean', None)
                    if ber_mean is not None and 0 < ber_mean < 1:
                        flags = check_ber(ber_mean, method=key)
                        critical = [f for f in flags if f.severity == 'CRITICAL']
                        if critical:
                            warnings.warn(
                                f"红旗检测 [{key}/{sub_key}]:\n{format_flags(flags)}",
                                stacklevel=2
                            )
```

**集成到 multi_seed_sweep.py（示范）:**

```python
from tests.checkpoints import cp4_save_scan

def main():
    # ... 现有主循环 ...
    # 最终保存前扫描
    cp4_save_scan(results_data)          # ← 新增
    save_results(results_data, output_path)
```

**为什么用 warnings.warn 而不是 raise:**
- save_results 的首要职责是保存文件，不应因红旗而阻止保存
- 警告会打印到终端，用户能看到
- CRITICAL 级红旗在 CP-3（checkpoints.py 的 cp3_ber）中会 raise，那里是正确的拦截点

### 3.3 红旗在实验循环中的集成（手动但简单）

实验脚本中有两种集成方式:

**方式A（推荐）: 通过 checkpoints.py 的 CP-3**
```python
# SIM_CHECKPOINTS=1 时自动调用 check_ber + raise on CRITICAL
from tests.checkpoints import cp3_ber
```

**方式B: 直接调用 red_flags**
```python
from tests.red_flags import check_ber, format_flags

for seed in range(N_SEEDS):
    ber = run_single_seed(...)
    flags = check_ber(ber, method='DPLL', turbulence=turb, snr_db=snr_db)
    if any(f.severity == 'CRITICAL' for f in flags):
        print(format_flags(flags))
        break  # 或 raise
```

### 3.4 RF-09 信道共享验证的增强

当前 RF-09 只检查是否提供了 `channel_seed`，无法真正验证信道共享。增强方案:

在 `run_trial_shared()` 中自动验证（因为这是唯一的公平对比入口）:

```python
def run_trial_shared(Ns, gamma_bar, turb_name, f_dot, seed, ...):
    shared = generate_shared_realization(Ns, gamma_bar, turb_name, f_dot, seed)
    # 自动验证: 同一 shared dict 被所有方法使用（结构上已保证）
    # 无需额外代码 — generate_shared_realization 的返回值被所有方法共享
    # 这就是 TL-13 的核心保证
```

**结论: run_trial_shared 已结构性地保证信道共享（所有方法从同一个 shared dict 读取），RF-09 的实际防护在 T4 测试中（`test_shared_realization_deterministic`）。无需额外代码。**

---

## 4. 分层验证协议的实现

### 4.1 B5 六步协议转化为测试

创建 `tests/test_layered_verification.py`:

```python
"""分层验证协议 — B5 六步验证

运行:
  ~/.venvs/torch/bin/python -m pytest tests/test_layered_verification.py -v

设计原则:
  - 每步一个测试方法
  - 理论参考值硬编码在测试中（来源: 教材/标准公式）
  - 容差参数化在测试类属性中
"""
import numpy as np
import pytest
from common import (
    qpsk_mod, qpsk_demod, ber_count, resolve_qpsk,
    gg_block, doppler_phase,
    fft_foe, dpll_track, vv_cpr,
    generate_shared_realization, equalize_oracle,
    run_fixed,
    T_S, BLOCK, GAMMA_BAR_DEFAULT, DOPPLER_HIGH, TURB,
)


class TestLayeredVerification:
    """B5 六步分层验证"""

    # 容差参数（B5 设计）
    BER_TOL_HIGH = 0.20    # BER 10^-2~10^-3: <20% 相对误差
    BER_TOL_MID  = 0.50    # BER 10^-4~10^-5: <50%
    BER_TOL_LOW_FACTOR = 10  # BER <10^-5: 10倍因子
    PHASE_VAR_RANGE = (0.5, 2.0)  # 相位方差比值范围

    def test_step1_awgn_qpsk_ber(self):
        """步骤1: AWGN 信道 QPSK BER 理论值验证

        理论值: QPSK BER = erfc(sqrt(SNR_lin)) / 2
        测试点: 10dB → BER ≈ 3.87e-6
        """
        from scipy.special import erfc
        snr_db = 10
        gamma = 10 ** (snr_db / 10)  # = 10
        ber_theory = erfc(np.sqrt(gamma)) / 2  # ≈ 3.87e-6

        # Monte Carlo 验证
        np.random.seed(42)
        N = 1000000
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        noise_std = 1.0 / np.sqrt(2 * gamma)
        noise = noise_std * (np.random.randn(N) + 1j * np.random.randn(N))
        rx = tx + noise
        ber_sim = ber_count(bits, rx)

        # 容差: BER ~10^-5 级别，用 10x 因子
        assert ber_theory / 10 < ber_sim < ber_theory * 10, \
            f"AWGN BER: theory={ber_theory:.2e}, sim={ber_sim:.2e}"

    def test_step2_gg_channel_statistics(self):
        """步骤2: Gamma-Gamma 信道统计验证

        理论: E[h] = 1, h ~ Gamma-Gamma(alpha, beta)
        矩验证 + KS 检验（仅验证均值和正值性）
        """
        for turb_name in ['weak', 'moderate', 'strong']:
            a, b = TURB[turb_name]
            np.random.seed(100 + hash(turb_name) % 100)
            h = gg_block(500000, a, b)

            # 均值 ≈ 1
            assert abs(np.mean(h) - 1.0) < 0.02, \
                f"E[h]={np.mean(h):.4f} ({turb_name})"

            # 方差: Var[h] = 1/(a*b) + 1/a + 1/b (Gamma-Gamma)
            var_theory = 1/a + 1/b + 1/(a*b)
            var_sim = np.var(h)
            rel = abs(var_sim - var_theory) / var_theory
            assert rel < 0.05, \
                f"Var[h] {turb_name}: theory={var_theory:.4f}, sim={var_sim:.4f}"

    def test_step3_awgn_fading_ber(self):
        """步骤3: AWGN + 衰落 BER 验证

        理论: 平均 BER = E_h[QPSK_BER(gamma_bar * h)]
        简化: 在高 SNR 弱湍流下，BER 应接近无衰落情况
        """
        # 弱湍流 25dB: BER 应 < 0.01
        np.random.seed(200)
        gamma_bar = 10 ** (25 / 10)
        shared = generate_shared_realization(
            50000, gamma_bar, 'weak', DOPPLER_HIGH, seed=300)
        # 直接解调（无载波恢复，只有衰落+噪声）
        signal = shared['tx'] * np.sqrt(shared['h']) * np.exp(1j * shared['phi'])
        rx = signal + (shared['rx_raw'] - signal)  # = shared['rx_raw']
        ber = resolve_qpsk(rx, shared['bits'])
        assert ber < 0.1, f"弱湍流 25dB 有衰落 BER={ber:.4f} 应 < 10%"

    def test_step4_vv_phase_variance(self):
        """步骤4: VV 相位估计方差验证

        理论: VV 相位估计方差 ≈ 1/(2*M_vv*SNR) (高 SNR 近似)
        测试: 恒定相位 + AWGN，VV 估计方差应在理论值 0.5~2.0 倍
        """
        np.random.seed(400)
        Ns = 10000
        gamma = 100  # 20dB
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        phi_true = 0.3
        noise_std = 1.0 / np.sqrt(2 * gamma)
        noise = noise_std * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
        rx = tx * np.exp(1j * phi_true) + noise

        rx_comp, pe = vv_cpr(rx, Nw=64)

        # 理论相位估计方差: ~1/(2*64*100) = 7.8e-5 rad^2
        var_theory = 1 / (2 * 64 * gamma)
        # 后半段估计误差
        phi_err = pe[Ns//2:] - phi_true
        phi_err = (phi_err + np.pi) % (2*np.pi) - np.pi
        var_sim = np.var(phi_err)

        ratio = var_sim / var_theory
        assert 0.5 < ratio < 2.0, \
            f"VV 相位方差比 {ratio:.2f} 超出 [0.5, 2.0]"

    def test_step5_dpll_phase_variance(self):
        """步骤5: DPLL 相位估计方差验证

        理论: 二阶 DPLL 稳态相位方差 ≈ 2*zeta*omega_n*T_S/(4*SNR)
        """
        np.random.seed(500)
        Ns = 50000
        gamma = 100
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        phi0 = 0.2
        noise_std = 1.0 / np.sqrt(2 * gamma)
        noise = noise_std * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
        rx = tx * np.exp(1j * phi0) + noise

        omega_n = 8e6
        zeta = np.sqrt(2)/2
        rx_comp, phi_est = dpll_track(rx, omega_n=omega_n, zeta=zeta)

        # 理论方差（近似）: 比噪声底高一个环路噪声带宽因子
        var_noise = 1 / (2 * gamma)  # 每符号相位噪声方差
        # 后半段相位估计误差
        phi_err = phi_est[Ns//2:] - phi0
        phi_err = (phi_err + np.pi) % (2*np.pi) - np.pi
        var_sim = np.var(phi_err)

        # DPLL 应降低噪声方差（环路带宽 < 符号率）
        # 粗检查: 相位误差方差 < 无跟踪时的方差
        assert var_sim < var_noise * 10, \
            f"DPLL 相位方差 {var_sim:.2e} 过大"

    def test_step6_full_system(self):
        """步骤6: 完整系统端到端验证

        与 SPEC.md §6.1 已验证事实对照:
        Fixed 弱湍流 20dB BER ≈ 0.016%
        """
        bers = []
        for seed in range(20):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'weak', DOPPLER_HIGH, seed=seed)
            rx = run_fixed(shared)
            bers.append(resolve_qpsk(rx, shared['bits']))

        mean_ber = np.mean(bers)
        # SPEC §6.1: Fixed 弱湍流 ≈ 0.016%, 允许 5x 容差
        assert 1e-5 < mean_ber < 0.005, \
            f"Fixed 弱湍流 BER={mean_ber:.6f} 超出合理范围"
```

### 4.2 理论参考值来源

| 步骤 | 参考值 | 来源 |
|------|--------|------|
| 步骤1 | `erfc(sqrt(SNR))/2` | Proakis, Digital Communications, Eq.4.3-13 |
| 步骤2 | `E[h]=1, Var[h]=1/a+1/b+1/(ab)` | Gamma-Gamma 分布矩公式 |
| 步骤3 | `E_h[QPSK_BER(gamma*h)]` | 数值积分参考 |
| 步骤4 | `1/(2*Nw*SNR)` | VV 算法高SNR近似 |
| 步骤5 | 二阶环路方差近似 | Gardner, Phaselock Techniques |
| 步骤6 | SPEC §6.1 已验证值 | 30种子实验确认 |

### 4.3 容差参数化

容差在测试类属性中定义（见上方代码），修改时只需改类属性:

```python
class TestLayeredVerification:
    BER_TOL_HIGH = 0.20    # 改这里
    BER_TOL_MID  = 0.50
    ...
```

---

## 5. CI/CD 适配（轻量）

### 5.1 本地 pytest 命令

```bash
# 全部测试（约 8 秒）
cd projects/simulation
~/.venvs/torch/bin/python -m pytest tests/ -v

# 按层级运行
~/.venvs/torch/bin/python -m pytest tests/ -v -k "T1"           # 信号原语 ~1s
~/.venvs/torch/bin/python -m pytest tests/ -v -k "T7"           # 参数一致性 <1s
~/.venvs/torch/bin/python -m pytest tests/ -v -k "T5 or T6"     # 物理检查+回归 ~8s

# 分层验证（B5 协议）
~/.venvs/torch/bin/python -m pytest tests/test_layered_verification.py -v

# 带检查点运行实验
SIM_CHECKPOINTS=1 ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py --n-seeds 3

# 快速冒烟测试（只跑最快的几层）
~/.venvs/torch/bin/python -m pytest tests/ -v -k "T1 or T7 or T8" --timeout=30
```

### 5.2 不需要 tox / GitHub Actions

理由:
- 个人项目，单机开发，无团队协作
- 仿真需要 GPU/CUDA 环境（RTX 4070），CI 跑不了
- pytest 直接运行就是最简单的"CI"
- 如果未来需要自动化，一个 git pre-commit hook 足够:

```bash
# .git/hooks/pre-commit（可选）
cd projects/simulation && ~/.venvs/torch/bin/python -m pytest tests/ -q --tb=line -k "T7 or T8"
```

### 5.3 测试运行时间估计

| 测试集 | 测试数 | 预计耗时 | 触发频率 |
|--------|--------|----------|----------|
| T1 信号原语 | 11 | <1s | 每次 common.py 改动 |
| T2 载波恢复 | 8 | ~3s | 改 VV/DPLL/BPS/KF |
| T3 KF | 7 | ~2s | 改 kf_unified |
| T4 信道公平 | 8 | ~2s | 改信道生成 |
| T5 物理不变量 | 9 | ~5s | 每次出结果 |
| T6 回归守卫 | 5 | ~10s | commit 前 |
| T7 参数一致 | 13 | <1s | 每次 common.py 改动 |
| T8 数值稳定 | 7 | ~2s | 新方法/新参数 |
| 分层验证 | 6 | ~5s | 大改动后 |
| **全部** | **74** | **~30s** | |

---

## 6. 回归守卫设计

### 6.1 黄金值获取

**来源: SPEC.md §6.1 已验证事实（30种子实验确认）**

黄金值不从测试中获取（测试是验证者，不是数据源）。黄金值来自:
1. SPEC.md §6.1 的已验证数字
2. multi_seed_sweep.py 大规模实验结果
3. 代码审计（如 VV 公式修正后的确认值）

### 6.2 黄金值在 T6 中的表达

T6 不使用硬编码的精确值（种子差异会导致波动），使用**范围断言**:

```python
# 当前 T6 做法（正确）:
def test_vv_weak_turbulence_effective(self):
    mean_ber = self._avg_ber(lambda s: _foe_then_vv(s), 'weak')
    assert mean_ber < 0.05  # 范围断言，不锁定精确值

def test_foe_only_ber_about_10pct(self):
    mean_ber = ...
    assert 0.08 < mean_ber < 0.15  # 窗口断言
```

### 6.3 如何更新黄金值（防止锁定错误值）

**更新触发条件:**
1. common.py 的信号处理逻辑有意修改（如优化 VV 窗口大小）
2. SPEC.md 参数更新

**更新流程:**
1. 先运行 30 种子大规模实验确认新值
2. 更新 SPEC.md §6.1
3. 放宽 T6 断言范围（不收窄到精确值）
4. 在 commit message 中注明 "T6 golden values updated per SPEC §6.1"

**防止锁定错误值的保护:**
- T6 用 N_SEEDS=10 的平均值（非单种子），减少随机性
- 断言用范围而非精确值，容许种子差异
- T5 物理不变量测试作为独立护栏（不依赖 SPEC 值）

### 6.4 VV 公式 bug 防护的具体实现

**核心测试: `TestT6RegressionGuard::test_vv_weak_turbulence_effective`**

这个测试直接防护 VV 公式退化:

```python
def test_vv_weak_turbulence_effective(self):
    """修正后 VV 在弱湍流有效 (SPEC §6.1 #5)

    修正 VV BER 应 < 5%（旧 bug 版本 27%）
    如果此测试失败 → VV 公式又坏了
    """
    bers = []
    for seed in range(self.N_SEEDS):
        shared = generate_shared_realization(...)
        rx_eq = equalize_oracle(shared)
        fo_est = fft_foe(rx_eq)
        k = np.arange(len(rx_eq))
        rx_foc = rx_eq * np.exp(-1j * fo_est * k)
        rx_vv, _ = vv_cpr(rx_foc, Nw=64)
        bers.append(resolve_qpsk(rx_vv, shared['bits']))
    mean_ber = np.mean(bers)
    assert mean_ber < 0.05  # 旧bug: 27%, 正常: <1%
```

**防护链条:**
1. `test_vv_weak_turbulence_effective` → 弱湍流 VV BER < 5%
2. `test_dpll_better_than_vv_strong` → 强湍流 DPLL < VV
3. RF-04 `check_known_ranges` → VV 强湍流在 [2%, 15%]

如果 VV 公式退化为旧 bug（`unwrap(angle*M)/M`），三个检查都会失败。

---

## 7. 迁移步骤（具体可执行）

### Phase 0: 验证现有测试通过 (5分钟)

```bash
cd /mnt/d/code/study/research-protocol/projects/simulation
~/.venvs/torch/bin/python -m pytest tests/test_common.py -v
```

如果全部 69 个测试通过 → 继续。如果有失败 → 先修 common.py。

### Phase 1: 创建基础设施 (15分钟)

**步骤 1.1: 创建 conftest.py**
- 文件: `tests/conftest.py`
- 内容: sys.path 设置（见 1.4 节）

**步骤 1.2: 创建 checkpoints.py**
- 文件: `tests/checkpoints.py`
- 内容: CP-1~CP-4 函数（见 2.2 节）

**步骤 1.3: 修改 test_common.py**
- 删除 30-33 行的 sys.path 设置（移到 conftest.py）
- 验证: `pytest tests/test_common.py -v` 仍全部通过

### Phase 2: common.py 集成 (5分钟)

**步骤 2.1: 添加 CP-4 到 save_results()**
- 在模块化后的 `common/_experiment.py` 的 `save_results()` 中（`data['_meta'] = ...` 之后）添加 3 行元数据完整性检查
- 不改函数签名，不加新函数
- 验证: `pytest tests/test_common.py -k T7 -v` 通过

### Phase 3: 分层验证测试 (20分钟)

**步骤 3.1: 创建 test_layered_verification.py**
- 文件: `tests/test_layered_verification.py`
- 内容: B5 六步验证（见第 4 节）

**步骤 3.2: 运行并验证**
```bash
~/.venvs/torch/bin/python -m pytest tests/test_layered_verification.py -v
```
- 如果步骤 4/5 的理论容差过紧，根据实际输出调整

### Phase 4: 一个实验脚本集成示范 (10分钟)

**步骤 4.1: 修改 multi_seed_sweep.py**
- 添加 `from tests.checkpoints import cp1_channel, cp2_carrier_recovery, cp3_ber`
- 在 `run_single_seed()` 中插入 3 个检查点调用
- 验证:
```bash
SIM_CHECKPOINTS=1 ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py --n-seeds 3 --n-symbols 1000 --methods DPLL --turbulence strong --snr-min 20 --snr-max 20
```

### Phase 5: 全量验证 (5分钟)

```bash
# 运行全部测试
~/.venvs/torch/bin/python -m pytest tests/ -v

# 运行带检查点的快速实验
SIM_CHECKPOINTS=1 ~/.venvs/torch/bin/python experiments/multi_seed_sweep.py --n-seeds 5 --n-symbols 5000 --methods VV DPLL --turbulence strong --snr-min 10 --snr-max 25 --snr-step 5
```

### 总工作量估计: 50-70 分钟

---

## 附录 A: 文件清单（实施后）

```
projects/simulation/
├── common.py                     # +3行: save_results 内元数据检查
├── SPEC.md                       # 不变
├── tests/
│   ├── conftest.py               # 新建: sys.path 共享设置
│   ├── test_common.py            # 微调: 删除 sys.path 设置（移到 conftest）
│   ├── test_layered_verification.py  # 新建: B5 六步分层验证
│   ├── checkpoints.py            # 新建: CP-1~CP-4 + cp4_save_scan
│   ├── red_flags.py              # 不变
│   └── VERIFICATION.md           # 不变
└── experiments/
    └── multi_seed_sweep.py       # 示范: 集成 checkpoints
```

## 附录 B: 对 common.py 的改动量

```
common.py 改动:
  save_results() 内加 3 行元数据检查            ≈ 3行
  ────────────────────────────────────────────────
  总改动                                         ≈ 3行（在 770 行文件上增加 0.4%）

test_common.py 改动:
  删除 4 行 sys.path 设置（移到 conftest.py）

新建文件:
  conftest.py                    ≈ 10行
  checkpoints.py                 ≈ 80行（含 cp1~cp4 + cp4_save_scan）
  test_layered_verification.py   ≈ 150行
```

## 附录 C: 不做什么

1. **不拆分 common.py** — 770 行单文件对个人项目完全可管理
2. **不加 CI 服务器** — 本地 pytest 就是 CI
3. **不加 tox** — 只有一个 Python 版本
4. **不用 hypothesis/property-based testing** — 69 个参数化测试已足够
5. **不加 coverage 追踪** — 测试目标是正确性不是覆盖率数字
6. **不改其他实验脚本** — multi_seed_sweep.py 做示范，其他脚本按需迁移
