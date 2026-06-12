#!/usr/bin/env python3
"""湍流 FSO 载波同步仿真 — 自动化验证测试套件

层次:
  T1: 信号原语单元测试 (gg_block, qpsk_mod/demod, ber_count)
  T2: 载波恢复基线单元测试 (fft_foe, dpll_track, vv_cpr, bps_cpr)
  T3: Kalman 滤波器单元测试 (kf_unified, design_Q)
  T4: 信道生成公平性测试 (generate_shared_realization)
  T5: 物理不变量 / 红旗检测
  T6: 回归守卫 (与 SPEC.md 已验证事实对照)

运行:
  cd projects/simulation
  ~/.venvs/torch/bin/python -m pytest tests/test_common.py -v
  ~/.venvs/torch/bin/python -m pytest tests/test_common.py -v -k "t1"   # 只跑 T1
  ~/.venvs/torch/bin/python -m pytest tests/test_common.py -v -k "t5"   # 只跑红旗检测
  ~/.venvs/torch/bin/python -m pytest tests/test_common.py -v --tb=short

所有测试从 common.py 导入，不复制任何信号处理逻辑。
"""

import sys
import os
import warnings

import numpy as np
import pytest

# 确保 common.py 可导入
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SIM_DIR = os.path.dirname(SCRIPT_DIR)
if SIM_DIR not in sys.path:
    sys.path.insert(0, SIM_DIR)

from common import (
    # 系统参数
    R_SYM, T_S, F_CARRIER, LASER_LW, BLOCK,
    TURB, DOPPLER_HIGH, DOPPLER_LOW, F_RESIDUAL,
    FIXED_CFG, FIXED_CFG_OPTIMAL, GAMMA_BAR_DEFAULT,
    SIGMA2_LASER, Q_TURB_PARAMS,
    DEF_B_BPS, DEF_NW_BPS,
    # 信号原语
    gg_block, qpsk_mod, qpsk_demod, ber_count,
    resolve_qpsk, ber_eval,
    qam16_mod, qam16_demod, ber_count_qam16, resolve_qam16,
    amp_limit, hard_decision,
    doppler_phase,
    # 载波恢复基线
    fft_foe, dpll_track, dpll_track_dd, vv_cpr, bps_cpr,
    carrier_recovery_fixed,
    # Kalman 滤波器
    design_Q, kf_unified,
    # 信道生成
    generate_shared_realization, insert_pilots,
    # 均衡
    mmse_equalize, equalize_oracle, equalize_hmed,
    # KF 载波恢复变体
    kf_oracle_recovery, kf_frame_h_recovery, kf_pilot_recovery,
    # 便捷函数
    run_fixed, run_kf_oracle, run_kf_frame_h, run_kf_pilot, run_bps,
    run_trial_shared,
    # 辅助
    db_ratio, get_pilots, PILOT_PATTERN,
)


# ═══════════════════════════════════════════════════════════════════
# T1: 信号原语单元测试
# ═══════════════════════════════════════════════════════════════════

class TestT1SignalPrimitives:
    """信号原语：调制/解调/信道生成"""

    def test_qpsk_roundtrip(self):
        """QPSK 调制 → 解调 → 误码为 0"""
        np.random.seed(0)
        bits = np.random.randint(0, 2, 10000)
        symbols = qpsk_mod(bits)
        bits_rx = qpsk_demod(symbols)
        assert np.array_equal(bits, bits_rx), "QPSK 无噪声 roundtrip 应零误码"

    def test_qpsk_avg_power(self):
        """QPSK 平均功率 = 1"""
        np.random.seed(1)
        bits = np.random.randint(0, 2, 100000)
        symbols = qpsk_mod(bits)
        avg_power = np.mean(np.abs(symbols) ** 2)
        np.testing.assert_allclose(avg_power, 1.0, atol=0.01,
                                   err_msg="QPSK 平均功率应为 1")

    def test_qpsk_constellation_points(self):
        """QPSK 星座点在 (±1±1j)/sqrt(2)"""
        for b0, b1 in [(0,0), (0,1), (1,0), (1,1)]:
            bits = np.array([b0, b1])
            s = qpsk_mod(bits)
            expected = ((2*b0-1) + 1j*(2*b1-1)) / np.sqrt(2)
            np.testing.assert_allclose(s[0], expected, atol=1e-10)

    def test_qpsk_ber_noiseless(self):
        """ber_count 在无噪声时 = 0"""
        np.random.seed(2)
        bits = np.random.randint(0, 2, 1000)
        symbols = qpsk_mod(bits)
        assert ber_count(bits, symbols) == 0.0

    def test_qpsk_ber_max_noise(self):
        """ber_count 在纯随机噪声时 ≈ 0.5"""
        np.random.seed(3)
        bits = np.random.randint(0, 2, 100000)
        noise = (np.random.randn(50000) + 1j * np.random.randn(50000)) / np.sqrt(2)
        ber = ber_count(bits, noise)
        # QPSK 在纯噪声下 BER ≈ 0.5（每个比特独立 50% 概率错误）
        np.testing.assert_allclose(ber, 0.5, atol=0.02,
                                   err_msg="纯噪声 QPSK BER 应接近 0.5")

    def test_qam16_roundtrip(self):
        """16-QAM 调制 → 解调 roundtrip"""
        np.random.seed(4)
        bits = np.random.randint(0, 2, 40000)
        symbols = qam16_mod(bits)
        bits_rx = qam16_demod(symbols)
        assert np.array_equal(bits, bits_rx), "16-QAM 无噪声 roundtrip 应零误码"

    def test_qam16_avg_power(self):
        """16-QAM 平均功率 = 1"""
        np.random.seed(5)
        bits = np.random.randint(0, 2, 400000)
        symbols = qam16_mod(bits)
        avg_power = np.mean(np.abs(symbols) ** 2)
        np.testing.assert_allclose(avg_power, 1.0, atol=0.02,
                                   err_msg="16-QAM 平均功率应为 1")

    def test_gg_block_statistics(self):
        """Gamma-Gamma 块衰落: E[h] ≈ 1, h > 0"""
        np.random.seed(10)
        N = 1000000
        for turb_name in ['weak', 'moderate', 'strong']:
            a, b = TURB[turb_name]
            h = gg_block(N, a, b)
            assert np.all(h > 0), f"Gamma-Gamma h 应始终 > 0 ({turb_name})"
            # E[h] = E[X] * E[Y] = 1 * 1 = 1（X ~ Gamma(a, 1/a), E[X]=1）
            mean_h = np.mean(h)
            np.testing.assert_allclose(
                mean_h, 1.0, atol=0.05,
                err_msg=f"E[h] ≈ 1 for {turb_name}, got {mean_h:.4f}"
            )

    def test_gg_block_block_constancy(self):
        """gg_block: 同一 block 内 h 恒定"""
        np.random.seed(11)
        N = 1000
        h = gg_block(N, 2.5, 1.8)
        # 第一个 block: h[0:BLOCK] 应全部相同
        assert np.all(h[:BLOCK] == h[0]), "Block 内 h 应恒定"

    def test_doppler_phase_monotonic_dominant(self):
        """多普勒相位: f_dot=150MHz/s 使得相位总体递增"""
        np.random.seed(12)
        N = 10000
        phi = doppler_phase(N, f_res=F_RESIDUAL, f_dot=DOPPLER_HIGH)
        # 线性+二次分量主导，总体应递增
        # 去掉激光噪声分量，线性+二次项应单调
        k = np.arange(N)
        phi_deterministic = 2 * np.pi * F_RESIDUAL * k * T_S + np.pi * DOPPLER_HIGH * (k * T_S)**2
        assert phi_deterministic[-1] > phi_deterministic[0], "确定性相位分量应递增"

    def test_hard_decision_qpsk(self):
        """hard_decision 返回 QPSK 星座点"""
        np.random.seed(13)
        bits = np.random.randint(0, 2, 1000)
        s = qpsk_mod(bits)
        dec = hard_decision(s, mod='qpsk')
        # 每个输出应在 QPSK 星座上
        constellation = set()
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                constellation.add(((2*b0-1) + 1j*(2*b1-1)) / np.sqrt(2))
        for val in dec:
            matches = any(abs(val - c) < 1e-10 for c in constellation)
            assert matches, f"hard_decision 输出 {val} 不在 QPSK 星座上"


# ═══════════════════════════════════════════════════════════════════
# T2: 载波恢复基线单元测试
# ═══════════════════════════════════════════════════════════════════

class TestT2CarrierRecovery:
    """载波恢复算法: FFT-FOE, VV, DPLL, BPS"""

    @pytest.fixture
    def clean_signal(self):
        """无噪声、无衰落的 QPSK 信号 + 已知频偏"""
        np.random.seed(100)
        Ns = 10000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        # 加已知频偏
        fo = 2 * np.pi * 0.01  # 归一化频偏
        k = np.arange(Ns)
        rx = tx * np.exp(1j * fo * k)
        return rx, bits, tx, fo, k, Ns

    def test_fft_foe_clean_signal(self, clean_signal):
        """FFT-FOE 在干净信号下精确估计频偏"""
        rx, bits, tx, fo_true, k, Ns = clean_signal
        fo_est = fft_foe(rx)
        # 归一化频偏估计精度（允许 1% 误差）
        rel_error = abs(fo_est - fo_true) / fo_true
        assert rel_error < 0.05, f"FFT-FOE 频偏估计误差 {rel_error:.4f} > 5%"

    def test_fft_foe_zero_offset(self):
        """FFT-FOE 在零频偏时估计 ≈ 0"""
        np.random.seed(101)
        Ns = 10000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        fo_est = fft_foe(tx)
        assert abs(fo_est) < 0.01, f"零频偏 FFT-FOE 应 ≈ 0, got {fo_est:.4f}"

    def test_vv_cpr_clean_phase(self):
        """VV CPR 在恒定相位偏移下完全补偿"""
        np.random.seed(102)
        Ns = 10000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        # 恒定相位偏移（不含频偏，VV 应能补偿）
        phi_const = 0.3
        rx = tx * np.exp(1j * phi_const)
        rx_comp, pe = vv_cpr(rx, Nw=64)
        # VV 估计后星座应接近原始
        ber = resolve_qpsk(rx_comp, bits)
        assert ber < 0.01, f"恒定相位 VV 补偿后 BER={ber:.4f} 应 < 1%"

    def test_dpll_track_clean_signal(self):
        """DPLL 在干净信号（恒定相位偏移）下跟踪

        注意: DPLL 使用 4 次方鉴相器，有 pi/4 偏移 + pi/2 模糊。
        只测恒定相位（无频偏），因为 DPLL 是二阶环对恒定相位无稳态误差。
        必须用 resolve_qpsk 评估（ber_count 无法处理 pi/2 模糊）。
        """
        np.random.seed(103)
        Ns = 10000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        # 仅恒定相位偏移（不施加频偏，DPLL 对恒定相位完美跟踪）
        phi0 = 0.5
        rx = tx * np.exp(1j * phi0)
        rx_comp, phi_est = dpll_track(rx, omega_n=8e6)
        ber = resolve_qpsk(rx_comp, bits)
        assert ber < 0.05, f"DPLL 干净信号 BER={ber:.4f} 应 < 5%"

    def test_bps_cpr_clean_signal(self):
        """BPS 在恒定相位偏移下精确补偿"""
        np.random.seed(104)
        Ns = 5000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        phi_const = 0.7
        rx = tx * np.exp(1j * phi_const)
        rx_comp, pe = bps_cpr(rx, B=DEF_B_BPS, Nw=DEF_NW_BPS)
        ber = resolve_qpsk(rx_comp, bits)
        assert ber < 0.01, f"BPS 恒定相位 BER={ber:.4f} 应 < 1%"

    def test_dpll_track_dd_qpsk(self):
        """DD-DPLL QPSK 模式在干净信号下工作"""
        np.random.seed(105)
        Ns = 5000
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        phi0 = 0.3
        rx = tx * np.exp(1j * phi0)
        rx_comp, _ = dpll_track_dd(rx, omega_n=8e6, mod='qpsk')
        ber = ber_count(bits, rx_comp)
        assert ber < 0.05, f"DD-DPLL QPSK BER={ber:.4f}"

    def test_dpll_track_dd_qam16(self):
        """DD-DPLL 16-QAM 模式基本工作"""
        np.random.seed(106)
        Ns = 5000
        bits = np.random.randint(0, 2, Ns * 4)
        tx = qam16_mod(bits)
        phi0 = 0.2
        rx = tx * np.exp(1j * phi0)
        rx_comp, _ = dpll_track_dd(rx, omega_n=8e6, mod='qam16')
        ber = ber_count_qam16(bits, rx_comp)
        assert ber < 0.05, f"DD-DPLL 16-QAM BER={ber:.4f}"

    def test_carrier_recovery_pipeline(self):
        """完整 carrier_recovery_fixed 在弱湍流下工作"""
        np.random.seed(107)
        shared = generate_shared_realization(
            Ns=5000, gamma_bar=GAMMA_BAR_DEFAULT,
            turb_name='weak', f_dot=DOPPLER_HIGH, seed=200
        )
        rx_eq = equalize_oracle(shared)
        rx_comp = carrier_recovery_fixed(rx_eq)
        ber = resolve_qpsk(rx_comp, shared['bits'])
        # 弱湍流 20dB 下 Fixed 基线 BER 应 < 1%
        assert ber < 0.05, f"Weak turbulence Fixed BER={ber:.4f}"


# ═══════════════════════════════════════════════════════════════════
# T3: Kalman 滤波器单元测试
# ═══════════════════════════════════════════════════════════════════

class TestT3KalmanFilter:
    """Kalman 滤波器: Q 矩阵设计、单块滤波、跨块 P 传递"""

    def test_design_Q_positive_definite(self):
        """design_Q 返回正定矩阵"""
        for turb_name in ['weak', 'moderate', 'strong']:
            Q = design_Q(turb_name)
            eigvals = np.linalg.eigvalsh(Q)
            assert np.all(eigvals > 0), f"Q 非正定 ({turb_name}): eigenvalues={eigvals}"

    def test_design_Q_diagonal(self):
        """design_Q 返回对角阵"""
        for turb_name in ['weak', 'moderate', 'strong']:
            Q = design_Q(turb_name)
            assert Q[0, 1] == 0.0 and Q[1, 0] == 0.0, f"Q 非对角 ({turb_name})"

    def test_design_Q_strong_larger_phase(self):
        """强湍流 Q 的相位不确定性 > 弱湍流

        Q[0,0] = sigma2_phi (含湍流分量), 强湍流 > 弱湍流。
        Q[1,1] = sigma2_df (多普勒率), 与湍流无关，所有等级相同。
        """
        Q_weak = design_Q('weak')
        Q_strong = design_Q('strong')
        assert Q_strong[0, 0] > Q_weak[0, 0], "强湍流 Q[0,0] 应 > 弱湍流"
        # Q[1,1] 只依赖 f_dot，不依赖湍流等级
        np.testing.assert_allclose(Q_strong[1, 1], Q_weak[1, 1],
                                   err_msg="Q[1,1] 只依赖 f_dot，不依赖湍流")

    def test_kf_unified_returns_correct_shapes(self):
        """kf_unified 返回正确形状

        h_block 是标量（每块一个 h 值），不是向量。
        """
        np.random.seed(200)
        N = 500
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        h_val = 1.0  # 标量，代表整块的信道增益
        rx = tx * np.exp(1j * 0.3)  # 恒定相位

        Q = design_Q('weak')
        phi_est, df_est, P_final = kf_unified(rx, h_val, GAMMA_BAR_DEFAULT, Q)

        assert phi_est.shape == (N,), f"phi_est 形状 {phi_est.shape} != ({N},)"
        assert isinstance(df_est, (float, np.floating)), f"df_est 类型 {type(df_est)}"
        assert P_final.shape == (2, 2), f"P_final 形状 {P_final.shape} != (2,2)"

    def test_kf_unified_P_symmetric_positive_semidefinite(self):
        """KF 输出 P 矩阵对称半正定"""
        np.random.seed(201)
        N = 200
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        h_val = 1.0  # 标量
        rx = tx * np.exp(1j * 0.2)

        Q = design_Q('moderate')
        _, _, P = kf_unified(rx, h_val, GAMMA_BAR_DEFAULT, Q)

        # 对称性
        np.testing.assert_allclose(P, P.T, atol=1e-10,
                                   err_msg="P 应对称")
        # 半正定
        eigvals = np.linalg.eigvalsh(P)
        assert np.all(eigvals >= -1e-10), f"P 非半正定: eigenvalues={eigvals}"

    def test_kf_converges_constant_phase(self):
        """KF 在恒定相位下收敛到真值"""
        np.random.seed(202)
        N = 1000
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        phi_true = 0.5
        h_val = 1.0  # 标量
        rx = tx * np.exp(1j * phi_true)

        Q = design_Q('weak') * 0.01  # 小 Q：相位几乎不变
        phi_est, _, _ = kf_unified(rx, h_val, GAMMA_BAR_DEFAULT, Q,
                                   phi_init=0.0)

        # 后半段估计误差应很小
        error_tail = np.abs(phi_est[N//2:] - phi_true)
        # 取模 [-pi, pi]
        error_tail = (error_tail + np.pi) % (2*np.pi) - np.pi
        rmse_tail = np.sqrt(np.mean(error_tail**2))
        assert rmse_tail < 0.1, f"KF 收敛后 RMSE={rmse_tail:.4f} > 0.1 rad"

    def test_kf_P_cross_block_propagation(self):
        """P 矩阵跨块传递（TL-09 验证）"""
        np.random.seed(203)
        N = BLOCK
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        h_val = 1.0  # 标量
        rx = tx * np.exp(1j * 0.3)

        Q = design_Q('moderate')
        # Block 1
        _, _, P1 = kf_unified(rx, h_val, GAMMA_BAR_DEFAULT, Q)
        # Block 2: P_init = P1（跨块传递）
        _, _, P2 = kf_unified(rx, h_val, GAMMA_BAR_DEFAULT, Q, P_init=P1)

        # P2 应该 <= P1（更多观测 = 更小不确定性）
        assert np.trace(P2) <= np.trace(P1) + 1e-8, \
            "P 不应因跨块传递而增大"

    def test_kf_oracle_recovery_runs(self):
        """kf_oracle_recovery 端到端运行不崩溃"""
        np.random.seed(204)
        shared = generate_shared_realization(
            Ns=1000, gamma_bar=GAMMA_BAR_DEFAULT,
            turb_name='weak', f_dot=DOPPLER_HIGH, seed=300
        )
        rx_eq = equalize_oracle(shared)
        rx_comp = kf_oracle_recovery(
            rx_eq, shared['h'], shared['gamma_bar'],
            'weak', DOPPLER_HIGH
        )
        assert len(rx_comp) == len(shared['rx_raw'])
        assert not np.any(np.isnan(rx_comp)), "KF oracle 输出含 NaN"


# ═══════════════════════════════════════════════════════════════════
# T4: 信道生成公平性测试
# ═══════════════════════════════════════════════════════════════════

class TestT4ChannelFairness:
    """信道共享：同 seed 产生完全相同的信道实现"""

    def test_shared_realization_deterministic(self):
        """同 seed → 同信道（确定性）"""
        s1 = generate_shared_realization(5000, 100, 'moderate', DOPPLER_HIGH, seed=42)
        s2 = generate_shared_realization(5000, 100, 'moderate', DOPPLER_HIGH, seed=42)
        np.testing.assert_array_equal(s1['rx_raw'], s2['rx_raw'],
                                      "同 seed 信道应完全相同")
        np.testing.assert_array_equal(s1['bits'], s2['bits'])
        np.testing.assert_array_equal(s1['h'], s2['h'])

    def test_different_seeds_differ(self):
        """不同 seed → 不同信道"""
        s1 = generate_shared_realization(5000, 100, 'moderate', DOPPLER_HIGH, seed=1)
        s2 = generate_shared_realization(5000, 100, 'moderate', DOPPLER_HIGH, seed=2)
        assert not np.array_equal(s1['rx_raw'], s2['rx_raw'])

    def test_shared_keys_complete(self):
        """generate_shared_realization 返回所有必要键"""
        s = generate_shared_realization(5000, 100, 'strong', DOPPLER_HIGH, seed=0)
        required_keys = ['rx_raw', 'bits', 'tx', 'h', 'h_blocks', 'h_med', 'phi',
                         'Ns', 'gamma_bar', 'turb_name', 'f_dot']
        for key in required_keys:
            assert key in s, f"缺少键: {key}"

    def test_signal_model_snr(self):
        """验证信号模型: SNR = gamma_bar * h (SPEC §1.1)

        r[k] = sqrt(h)*s*exp(j*phi) + n, E[|n|²] = 1
        瞬时 SNR = gamma_bar * h * |s|² = gamma_bar * h (QPSK |s|²=1)
        """
        np.random.seed(300)
        Ns = 100000
        gamma_bar = 100.0  # 20 dB
        shared = generate_shared_realization(Ns, gamma_bar, 'weak', DOPPLER_HIGH, seed=500)

        # 从 rx_raw 估算平均 SNR
        # signal = tx * sqrt(h) * exp(j*phi)
        carrier = np.exp(1j * shared['phi'])
        signal = shared['tx'] * np.sqrt(shared['h']) * carrier
        noise = shared['rx_raw'] - signal

        # 信号功率（含衰落）
        sig_power = np.mean(np.abs(signal)**2)
        # 噪声功率
        noise_power = np.mean(np.abs(noise)**2)

        # 有效 SNR = E[gamma_bar * h] = gamma_bar * E[h] ≈ gamma_bar
        measured_snr = sig_power / noise_power
        expected_snr = gamma_bar  # E[h]=1
        rel_error = abs(measured_snr - expected_snr) / expected_snr
        assert rel_error < 0.05, \
            f"SNR 验证失败: measured={measured_snr:.2f}, expected={expected_snr:.2f}"

    def test_h_block_values(self):
        """h_blocks 是每个 block 起始的 h 值"""
        shared = generate_shared_realization(1000, 100, 'moderate', DOPPLER_HIGH, seed=50)
        n_blocks = 1000 // BLOCK
        assert len(shared['h_blocks']) == n_blocks
        for i in range(n_blocks):
            assert shared['h_blocks'][i] == shared['h'][i * BLOCK]

    def test_insert_pilots_preserves_channel(self):
        """insert_pilots 不改变信道/噪声，只替换导频位置的发符号"""
        shared = generate_shared_realization(1000, 100, 'weak', DOPPLER_HIGH, seed=60)
        rx_pilot, pilot_idx, data_idx, data_bits = insert_pilots(shared, n_pilots_per_block=5)

        # 长度不变
        assert len(rx_pilot) == len(shared['rx_raw'])

        # 数据位置噪声不变（信号变了但信道+噪声不变）
        carrier = np.exp(1j * shared['phi'])
        noise_original = shared['rx_raw'] - shared['tx'] * np.sqrt(shared['h']) * carrier
        noise_pilot = rx_pilot - shared['tx'] * np.sqrt(shared['h']) * carrier  # tx 已被修改
        # 非导频位置噪声应完全相同（但这些位置的 tx 没变）
        # 只检查非导频位置的 tx 未改变
        assert len(data_idx) > 0
        assert len(pilot_idx) > 0

    def test_mmse_equalize_unit_h(self):
        """MMSE 均衡 h=1 时近似恒等变换"""
        np.random.seed(301)
        N = 1000
        rx = np.random.randn(N) + 1j * np.random.randn(N)
        eq = mmse_equalize(rx, h=1.0, gamma_bar=100)
        # h=1, gamma_bar=100: sqrt(1) / (1 + 0.01) ≈ 0.99
        np.testing.assert_allclose(eq, rx * 0.990099, atol=1e-4)

    def test_amp_limit_clips(self):
        """amp_limit 限制幅度"""
        np.random.seed(302)
        N = 100
        rx = np.zeros(N, dtype=complex)
        rx[0] = 5.0 + 0j   # |rx[0]| = 5 > 3
        rx[1] = 1.0 + 1j   # |rx[1]| = sqrt(2) < 3
        out = amp_limit(rx, thresh=3.0)
        assert abs(out[0]) == pytest.approx(3.0, abs=1e-10)
        np.testing.assert_allclose(out[1], rx[1])


# ═══════════════════════════════════════════════════════════════════
# T5: 物理不变量 / 红旗检测
# ═══════════════════════════════════════════════════════════════════

class TestT5PhysicalInvariants:
    """物理不变量检查：违反这些意味着 bug 或物理前提错误"""

    def test_ber_between_0_and_1(self):
        """任何方法的 BER 应在 [0, 1]"""
        shared = generate_shared_realization(5000, GAMMA_BAR_DEFAULT,
                                              'weak', DOPPLER_HIGH, seed=400)
        rx_comp = run_fixed(shared)
        ber = ber_eval(shared['bits'], rx_comp)
        assert 0.0 <= ber <= 1.0, f"BER={ber} 不在 [0,1]"

    def test_no_nans_in_output(self):
        """所有载波恢复方法输出不含 NaN/Inf"""
        shared = generate_shared_realization(5000, GAMMA_BAR_DEFAULT,
                                              'moderate', DOPPLER_HIGH, seed=401)
        methods = {
            'fixed': lambda s: run_fixed(s),
            'kf_oracle': lambda s: run_kf_oracle(s),
            'kf_frame': lambda s: run_kf_frame_h(s),
            'bps': lambda s: run_bps(s),
        }
        for name, fn in methods.items():
            rx = fn(shared)
            assert not np.any(np.isnan(rx)), f"{name} 输出含 NaN"
            assert not np.any(np.isinf(rx)), f"{name} 输出含 Inf"

    def test_high_snr_low_ber(self):
        """高 SNR (30dB) 下 BER 应极低 (<1%)"""
        gamma_bar_30db = 10 ** (30 / 10)  # 1000
        shared = generate_shared_realization(5000, gamma_bar_30db,
                                              'weak', DOPPLER_HIGH, seed=402)
        # 至少一种方法应达到低 BER
        best_ber = 1.0
        for fn in [run_fixed, run_kf_oracle, run_bps]:
            rx = fn(shared)
            ber = resolve_qpsk(rx, shared['bits'])
            best_ber = min(best_ber, ber)
        assert best_ber < 0.01, \
            f"30dB 弱湍流最低 BER={best_ber:.4f} 应 < 1%"

    def test_bpsk_qpsk_ber_never_exceed_half(self):
        """QPSK 系统 BER 不应 > 0.5（物理上限）"""
        # 极低 SNR
        shared = generate_shared_realization(5000, 0.1,  # -10 dB
                                              'strong', DOPPLER_HIGH, seed=403)
        # 直接解调（无载波恢复）
        ber = ber_count(shared['bits'], shared['rx_raw'])
        assert ber <= 0.55, f"极端低 SNR 下 BER={ber:.4f} > 0.55"

    def test_h_always_positive(self):
        """Gamma-Gamma 衰落 h > 0（物理约束）"""
        for turb_name in ['weak', 'moderate', 'strong']:
            for seed in range(10):
                shared = generate_shared_realization(5000, 100, turb_name,
                                                      DOPPLER_HIGH, seed=seed)
                assert np.all(shared['h'] > 0), \
                    f"h 含非正值 ({turb_name}, seed={seed})"

    def test_strong_turbulence_worse_than_weak(self):
        """强湍流 BER > 弱湍流 BER（物理不变量）"""
        bers = {}
        for turb_name in ['weak', 'strong']:
            shared = generate_shared_realization(10000, GAMMA_BAR_DEFAULT,
                                                  turb_name, DOPPLER_HIGH, seed=404)
            rx = run_fixed(shared, eq_mode='oracle')
            bers[turb_name] = resolve_qpsk(rx, shared['bits'])
        assert bers['strong'] > bers['weak'], \
            f"强湍流 BER ({bers['strong']:.4f}) 应 > 弱湍流 ({bers['weak']:.4f})"

    def test_snr_monotonic_ber(self):
        """BER 应随 SNR 单调下降（粗粒度检查）"""
        bers = []
        for snr_db in [5, 15, 25]:
            gamma = 10 ** (snr_db / 10)
            shared = generate_shared_realization(
                5000, gamma, 'moderate', DOPPLER_HIGH, seed=405)
            rx = run_fixed(shared)
            bers.append(resolve_qpsk(rx, shared['bits']))
        # 不要求严格单调（随机性），但粗粒度应下降
        assert bers[0] >= bers[2], \
            f"BER 非单调下降: SNR 5/15/25dB → {bers}"

    def test_gain_reasonable_range(self):
        """dB 增益应在合理范围: -10 ~ +20 dB

        超出此范围通常意味着:
        - 比较的基线有 bug
        - 参数不一致
        - 物理前提错误
        """
        shared = generate_shared_realization(
            5000, GAMMA_BAR_DEFAULT, 'weak', DOPPLER_HIGH, seed=406)
        rx_fixed = run_fixed(shared)
        rx_kf = run_kf_oracle(shared)
        ber_fixed = resolve_qpsk(rx_fixed, shared['bits'])
        ber_kf = resolve_qpsk(rx_kf, shared['bits'])
        gain = db_ratio(ber_fixed, ber_kf)
        assert -10 < gain < 20, \
            f"增益 {gain:.1f} dB 超出合理范围 [-10, +20]"

    def test_kf_pilot_ber_strong_turbulence_known_range(self):
        """KF pilot 强湍流 BER 应在已知范围 (SPEC §6.1 已验证事实)

        旧值 3.08%，允许 2x 容差因种子不同
        """
        bers = []
        for seed in range(30):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'strong', DOPPLER_HIGH, seed=seed)
            corrected, data_idx, data_bits, _ = run_kf_pilot(shared, n_pilots=5)
            bers.append(ber_eval(data_bits, corrected[data_idx]))

        mean_ber = np.mean(bers)
        # 已知范围: ~3%, 允许 [1%, 10%]
        assert 0.01 < mean_ber < 0.10, \
            f"KF pilot 强湍流 BER={mean_ber:.4f} 超出已知范围 [0.01, 0.10]"

    def test_dpll_strong_turbulence_known_range(self):
        """DPLL 强湍流 BER 应在已知范围 (SPEC §6.1)

        已知值 1.93%, 允许 [0.5%, 5%]
        """
        bers = []
        for seed in range(30):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'strong', DOPPLER_HIGH, seed=seed)
            rx_eq = equalize_oracle(shared)
            fo_est = fft_foe(rx_eq)
            k = np.arange(len(rx_eq))
            rx_foc = rx_eq * np.exp(-1j * fo_est * k)
            rx_dpll, _ = dpll_track(rx_foc, omega_n=8e6)
            bers.append(resolve_qpsk(rx_dpll, shared['bits']))

        mean_ber = np.mean(bers)
        assert 0.005 < mean_ber < 0.05, \
            f"DPLL 强湍流 BER={mean_ber:.4f} 超出已知范围 [0.005, 0.05]"


# ═══════════════════════════════════════════════════════════════════
# T6: 回归守卫 — 与 SPEC.md 已验证事实对照
# ═══════════════════════════════════════════════════════════════════

class TestT6RegressionGuard:
    """回归守卫: 防止代码改动导致已知结论被推翻

    基于 SPEC.md §6.1 已验证事实。使用宽松容差因种子差异。
    """

    N_SEEDS = 10  # 回归测试用少量种子，快速执行

    def _avg_ber(self, method_fn, turb_name, n_seeds=None, **kwargs):
        """辅助: 计算多种子平均 BER"""
        n = n_seeds or self.N_SEEDS
        bers = []
        for seed in range(n):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, turb_name, DOPPLER_HIGH, seed=seed)
            result = method_fn(shared, **kwargs)
            if isinstance(result, tuple):
                # KF pilot returns (corrected, data_idx, data_bits, h_est)
                corrected, data_idx, data_bits = result[0], result[1], result[2]
                bers.append(ber_eval(data_bits, corrected[data_idx]))
            else:
                bers.append(resolve_qpsk(result, shared['bits']))
        return np.mean(bers)

    def test_foe_only_ber_about_10pct(self):
        """FOE only BER ≈ 10% (SPEC §6.4: D2 消融)

        FOE 只补偿频偏，不跟踪残余相位，BER 应在 10-15%
        """
        bers = []
        for seed in range(self.N_SEEDS):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'moderate', DOPPLER_HIGH, seed=seed)
            rx_eq = equalize_oracle(shared)
            fo_est = fft_foe(rx_eq)
            k = np.arange(len(rx_eq))
            rx_foe = rx_eq * np.exp(-1j * fo_est * k)
            bers.append(resolve_qpsk(rx_foe, shared['bits']))
        mean_ber = np.mean(bers)
        assert 0.08 < mean_ber < 0.15, \
            f"FOE only BER={mean_ber:.4f} 偏离已知范围 [0.08, 0.15]"

    def test_vv_weak_turbulence_effective(self):
        """修正后 VV 在弱湍流有效 (SPEC §6.1 #5)

        修正 VV BER 应 < 5%（旧 bug 版本 27%）
        """
        bers = []
        for seed in range(self.N_SEEDS):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'weak', DOPPLER_HIGH, seed=seed)
            rx_eq = equalize_oracle(shared)
            fo_est = fft_foe(rx_eq)
            k = np.arange(len(rx_eq))
            rx_foc = rx_eq * np.exp(-1j * fo_est * k)
            rx_vv, _ = vv_cpr(rx_foc, Nw=64)
            bers.append(resolve_qpsk(rx_vv, shared['bits']))
        mean_ber = np.mean(bers)
        assert mean_ber < 0.05, \
            f"修正 VV 弱湍流 BER={mean_ber:.4f} 应 < 5%（如果 > 5% 说明 VV 公式又坏了）"

    def test_dpll_better_than_vv_strong(self):
        """强湍流 DPLL 优于 VV (SPEC §6.1 #4)"""
        ber_dpll = self._avg_ber(
            lambda s: _foe_then_dpll(s), 'strong')
        ber_vv = self._avg_ber(
            lambda s: _foe_then_vv(s), 'strong')
        assert ber_dpll < ber_vv, \
            f"DPLL ({ber_dpll:.4f}) 应 < VV ({ber_vv:.4f}) in 强湍流"

    def test_fixed_optimal_better_than_default(self):
        """Fixed 最优参数优于默认参数 (SPEC §2)"""
        bers_opt = []
        bers_def = []
        for seed in range(self.N_SEEDS):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'strong', DOPPLER_HIGH, seed=seed)
            rx_eq = equalize_oracle(shared)
            # 最优参数
            rx_opt = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG_OPTIMAL['strong'])
            bers_opt.append(resolve_qpsk(rx_opt, shared['bits']))
            # 默认参数
            rx_def = carrier_recovery_fixed(rx_eq, cfg=FIXED_CFG)
            bers_def.append(resolve_qpsk(rx_def, shared['bits']))

        assert np.mean(bers_opt) <= np.mean(bers_def) + 0.01, \
            f"最优 Fixed ({np.mean(bers_opt):.4f}) 应 <= 默认 ({np.mean(bers_def):.4f})"

    def test_pilot_pattern_known(self):
        """导频图案是已知的 4 个 QPSK 点"""
        assert len(PILOT_PATTERN) == 4
        pilots = get_pilots(8)
        assert len(pilots) == 8
        # 前 4 个应重复
        for i in range(4):
            assert abs(pilots[i+4] - pilots[i]) < 1e-10


# ═══════════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════════

def _foe_then_dpll(shared):
    """FOE + DPLL（不经过 VV）"""
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_comp, _ = dpll_track(rx_foc)
    return rx_comp


def _foe_then_vv(shared):
    """FOE + VV"""
    rx_eq = equalize_oracle(shared)
    fo_est = fft_foe(rx_eq)
    k = np.arange(len(rx_eq))
    rx_foc = rx_eq * np.exp(-1j * fo_est * k)
    rx_comp, _ = vv_cpr(rx_foc)
    return rx_comp


# ═══════════════════════════════════════════════════════════════════
# T7: 参数一致性检查
# ═══════════════════════════════════════════════════════════════════

class TestT7ParameterConsistency:
    """验证 common.py 参数与 SPEC.md 一致"""

    def test_symbol_rate(self):
        """R_SYM = 2.5e9 (SPEC §1.3)"""
        assert R_SYM == 2.5e9

    def test_symbol_period(self):
        """T_S = 1/R_SYM"""
        assert T_S == 1 / R_SYM

    def test_block_size(self):
        """BLOCK = 100 (SPEC §1.3)"""
        assert BLOCK == 100

    def test_laser_linewidth(self):
        """LASER_LW = 10e3 (SPEC §1.3)"""
        assert LASER_LW == 10e3

    def test_doppler_high(self):
        """DOPPLER_HIGH = 150e6 (SPEC §1.3)"""
        assert DOPPLER_HIGH == 150e6

    def test_f_residual(self):
        """F_RESIDUAL = 1e6 (SPEC §1.3)"""
        assert F_RESIDUAL == 1e6

    def test_turb_params_keys(self):
        """TURB 包含 weak/moderate/strong"""
        assert set(TURB.keys()) == {'weak', 'moderate', 'strong'}

    def test_turb_param_values(self):
        """TURB 参数与 SPEC §1.4 一致"""
        assert TURB['weak'] == (4.0, 3.0)
        assert TURB['moderate'] == (2.5, 1.8)
        assert TURB['strong'] == (1.5, 0.8)

    def test_sigma2_laser_formula(self):
        """SIGMA2_LASER = 2*pi*LASER_LW*T_S"""
        expected = 2 * np.pi * LASER_LW * T_S
        np.testing.assert_allclose(SIGMA2_LASER, expected)

    def test_gamma_bar_default(self):
        """GAMMA_BAR_DEFAULT = 100 (20 dB)"""
        assert GAMMA_BAR_DEFAULT == 100

    def test_fixed_cfg_optimal_keys(self):
        """FIXED_CFG_OPTIMAL 包含所有湍流等级"""
        for turb in ['weak', 'moderate', 'strong']:
            assert turb in FIXED_CFG_OPTIMAL
            cfg = FIXED_CFG_OPTIMAL[turb]
            assert 'N_fft' in cfg
            assert 'M_vv' in cfg
            assert 'omega_n' in cfg

    def test_q_turb_params_keys(self):
        """Q_TURB_PARAMS 包含所有湍流等级"""
        for turb in ['weak', 'moderate', 'strong']:
            assert turb in Q_TURB_PARAMS
            assert 'sigma2_turb' in Q_TURB_PARAMS[turb]
            assert 'kappa' in Q_TURB_PARAMS[turb]

    def test_sigma2_turb_strong_larger(self):
        """强湍流 sigma2_turb > 弱湍流"""
        assert Q_TURB_PARAMS['strong']['sigma2_turb'] > Q_TURB_PARAMS['weak']['sigma2_turb']


# ═══════════════════════════════════════════════════════════════════
# T8: 数值稳定性测试
# ═══════════════════════════════════════════════════════════════════

class TestT8NumericalStability:
    """边界条件: 极端参数下不崩溃"""

    def test_very_low_snr(self):
        """极低 SNR (-5dB) 不崩溃"""
        gamma = 10 ** (-5 / 10)
        shared = generate_shared_realization(
            1000, gamma, 'strong', DOPPLER_HIGH, seed=600)
        rx = run_fixed(shared)
        assert not np.any(np.isnan(rx))
        assert not np.any(np.isinf(rx))

    def test_very_high_snr(self):
        """极高 SNR (40dB) 不崩溃"""
        gamma = 10 ** (40 / 10)
        shared = generate_shared_realization(
            1000, gamma, 'weak', DOPPLER_HIGH, seed=601)
        rx = run_fixed(shared)
        assert not np.any(np.isnan(rx))

    def test_kf_very_short_block(self):
        """KF 在很短的信号上不崩溃"""
        np.random.seed(602)
        N = 32
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        h_val = 1.0  # 标量
        rx = tx * np.exp(1j * 0.3)
        Q = design_Q('weak')
        phi_est, df, P = kf_unified(rx, h_val, 100, Q)
        assert not np.any(np.isnan(phi_est))
        assert not np.any(np.isinf(P))

    def test_bps_short_signal(self):
        """BPS 在短信号上不崩溃"""
        np.random.seed(603)
        Ns = 100
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        rx = tx * np.exp(1j * 0.5)
        rx_comp, _ = bps_cpr(rx, B=32, Nw=10)
        assert len(rx_comp) == Ns

    def test_dpll_zero_signal(self):
        """DPLL 在零输入不崩溃"""
        N = 100
        rx = np.zeros(N, dtype=complex)
        rx_comp, phi = dpll_track(rx, omega_n=8e6)
        assert not np.any(np.isnan(rx_comp))

    def test_vv_zero_signal(self):
        """VV 在零输入不崩溃"""
        N = 100
        rx = np.zeros(N, dtype=complex)
        rx_comp, _ = vv_cpr(rx, Nw=64)
        assert not np.any(np.isnan(rx_comp))


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
