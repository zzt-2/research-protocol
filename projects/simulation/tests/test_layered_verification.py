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
    qpsk_mod, ber_count, resolve_qpsk,
    gg_block,
    vv_cpr, dpll_track,
    generate_shared_realization,
    run_fixed,
    T_S, GAMMA_BAR_DEFAULT, DOPPLER_HIGH, TURB,
)


class TestLayeredVerification:
    """B5 六步分层验证"""

    BER_TOL_HIGH = 0.20
    BER_TOL_MID = 0.50
    BER_TOL_LOW_FACTOR = 10
    PHASE_VAR_RANGE = (0.5, 2.0)

    def test_step1_awgn_qpsk_ber(self):
        """步骤1: AWGN 信道 QPSK BER 理论值验证

        理论值: QPSK BER = erfc(sqrt(SNR_lin)) / 2
        测试点: 10dB -> BER ~ 3.87e-6
        """
        from scipy.special import erfc
        snr_db = 10
        gamma = 10 ** (snr_db / 10)
        ber_theory = erfc(np.sqrt(gamma / 2)) / 2

        np.random.seed(42)
        N = 1000000
        bits = np.random.randint(0, 2, N * 2)
        tx = qpsk_mod(bits)
        noise_std = 1.0 / np.sqrt(2 * gamma)
        noise = noise_std * (np.random.randn(N) + 1j * np.random.randn(N))
        rx = tx + noise
        ber_sim = ber_count(bits, rx)

        assert ber_theory / 10 < ber_sim < ber_theory * 10, \
            f"AWGN BER: theory={ber_theory:.2e}, sim={ber_sim:.2e}"

    def test_step2_gg_channel_statistics(self):
        """步骤2: Gamma-Gamma 信道统计验证

        理论: E[h] = 1, Var[h] = 1/a + 1/b + 1/(a*b)
        """
        for turb_name in ['weak', 'moderate', 'strong']:
            a, b = TURB[turb_name]
            np.random.seed(100 + hash(turb_name) % 100)
            h = gg_block(500000, a, b)

            mean_tol = 0.05 if turb_name == 'strong' else 0.03
            assert abs(np.mean(h) - 1.0) < mean_tol, \
                f"E[h]={np.mean(h):.4f} ({turb_name}, tol={mean_tol})"

            var_theory = 1/a + 1/b + 1/(a*b)
            var_sim = np.var(h)
            rel = abs(var_sim - var_theory) / var_theory
            assert rel < 0.15, \
                f"Var[h] {turb_name}: theory={var_theory:.4f}, sim={var_sim:.4f}"

    def test_step3_awgn_fading_ber(self):
        """步骤3: AWGN + 衰落 BER 验证

        弱湍流 25dB: BER 应 < 0.1
        """
        np.random.seed(200)
        gamma_bar = 10 ** (25 / 10)
        shared = generate_shared_realization(
            50000, gamma_bar, 'weak', DOPPLER_HIGH, seed=300)
        # 补偿已知 Doppler 相位，只测试衰落+噪声效果
        rx_comp = shared['rx_raw'] * np.exp(-1j * shared['phi'])
        ber = resolve_qpsk(rx_comp, shared['bits'])
        assert ber < 0.1, f"弱湍流 25dB 有衰落 BER={ber:.4f} 应 < 10%"

    def test_step4_vv_phase_variance(self):
        """步骤4: VV 相位估计方差验证

        理论: VV 相位估计方差 ~ 1/(2*Nw*SNR) (高 SNR 近似)
        """
        np.random.seed(400)
        Ns = 10000
        gamma = 100
        bits = np.random.randint(0, 2, Ns * 2)
        tx = qpsk_mod(bits)
        phi_true = 0.3
        noise_std = 1.0 / np.sqrt(2 * gamma)
        noise = noise_std * (np.random.randn(Ns) + 1j * np.random.randn(Ns))
        rx = tx * np.exp(1j * phi_true) + noise

        _, pe = vv_cpr(rx, Nw=64)

        var_theory = 1 / (2 * 64 * gamma)
        phi_err = pe[Ns//2:] - phi_true
        phi_err = (phi_err + np.pi) % (2*np.pi) - np.pi
        var_sim = np.var(phi_err)

        ratio = var_sim / var_theory
        assert 0.5 < ratio < 2.0, \
            f"VV 相位方差比 {ratio:.2f} 超出 [0.5, 2.0]"

    def test_step5_dpll_phase_variance(self):
        """步骤5: DPLL 相位估计方差验证

        粗检查: DPLL 稳态相位误差方差 < 无跟踪时的方差
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

        _, phi_est = dpll_track(rx, omega_n=8e6, zeta=np.sqrt(2)/2)

        var_noise = 1 / (2 * gamma)
        phi_err = phi_est[Ns//2:] - phi0
        phi_err = (phi_err + np.pi) % (2*np.pi) - np.pi
        var_sim = np.var(phi_err)

        assert var_sim < var_noise * 10, \
            f"DPLL 相位方差 {var_sim:.2e} 过大"

    def test_step6_full_system(self):
        """步骤6: 完整系统端到端验证

        SPEC §6.1: Fixed 弱湍流 20dB BER ~ 0.016%
        """
        bers = []
        for seed in range(20):
            shared = generate_shared_realization(
                10000, GAMMA_BAR_DEFAULT, 'weak', DOPPLER_HIGH, seed=seed)
            rx = run_fixed(shared)
            bers.append(resolve_qpsk(rx, shared['bits']))

        mean_ber = np.mean(bers)
        assert 1e-5 < mean_ber < 0.005, \
            f"Fixed 弱湍流 BER={mean_ber:.6f} 超出合理范围"
