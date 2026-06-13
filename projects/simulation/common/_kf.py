"""Kalman 滤波器：Q 矩阵设计 + 统一 KF + 各变体恢复"""
import numpy as np

from ._config import (
    Q_TURB_PARAMS, SIGMA2_LASER, DOPPLER_HIGH, T_S,
    BLOCK, PILOT_PATTERN,
)
from ._recovery import vv_cpr, fft_foe
from ._modulation import hard_decision


def design_Q(turb_name='strong', f_dot=DOPPLER_HIGH):
    sigma2_turb = Q_TURB_PARAMS[turb_name]['sigma2_turb']
    sigma2_df = (f_dot * T_S)**2 / 3
    sigma2_phi = SIGMA2_LASER + sigma2_turb
    Q = np.diag([sigma2_phi, sigma2_df])
    return Q


def kf_unified(rx_block, h_block, gamma_bar, Q, phi_init=None,
               df_init=0.0, P_init=None, mod='qpsk'):
    """2状态KF（单块），P 跨块传递（TL-09）"""
    N = len(rx_block)
    F = np.array([[1.0, T_S], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])

    if phi_init is None:
        if N >= 16:
            _, pe_vv = vv_cpr(rx_block, Nw=min(N, 16))
            phi_init = pe_vv[0]
        else:
            phi_init = np.angle(rx_block[0]**4) / 4

    x = np.array([phi_init, df_init])
    if P_init is not None:
        P = P_init.copy()
    else:
        P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    phi_est = np.zeros(N)

    for k in range(N):
        x_pred = F @ x
        P_pred = F @ P @ F.T + Q

        rx_rotated = rx_block[k] * np.exp(-1j * x_pred[0])
        s_hat = hard_decision(rx_rotated, mod=mod)
        y = rx_block[k] * np.conj(s_hat)
        z_obs = np.angle(y)

        innov = z_obs - x_pred[0]
        innov = (innov + np.pi) % (2*np.pi) - np.pi

        R = 1.0 / (2 * gamma_bar * h_block)

        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T / S

        x = x_pred + K.flatten() * innov
        x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi

        P = (np.eye(2) - K @ H) @ P_pred
        phi_est[k] = x[0]

    return phi_est, x[1], P


def get_pilots(n_pilots):
    return PILOT_PATTERN[np.arange(n_pilots) % len(PILOT_PATTERN)]


def kf_oracle_recovery(rx, h, gamma_bar, turb_name, f_dot=DOPPLER_HIGH,
                       Q_fine_df=(50e3)**2, mod='qpsk'):
    """KF oracle-h：逐块真实 h"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        h_val = h[s]
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(
            rx_foc[s:e], h_val, gamma_bar, Q_fine,
            phi_init=phi_init, df_init=prev_df, P_init=prev_P, mod=mod)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    return rx_foc * np.exp(-1j * phi_full)


def kf_frame_h_recovery(rx, h_med, gamma_bar, turb_name, f_dot=DOPPLER_HIGH,
                        Q_fine_df=(50e3)**2, mod='qpsk'):
    """KF frame-level h"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // BLOCK
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    h_val = max(h_med, 0.01)
    phi_full = np.zeros(N)
    prev_df = 0.0
    prev_P = None

    for i in range(n_blocks):
        s, e = i*BLOCK, (i+1)*BLOCK
        phi_init = phi_full[s-1] if i > 0 else None
        phi_est, df_est, P_final = kf_unified(
            rx_foc[s:e], h_val, gamma_bar, Q_fine,
            phi_init=phi_init, df_init=prev_df, P_init=prev_P, mod=mod)
        phi_full[s:e] = phi_est
        prev_df = df_est
        prev_P = P_final

    return rx_foc * np.exp(-1j * phi_full)


def kf_pilot_recovery(rx, gamma_bar, turb_name, n_pilots, h_med,
                      f_dot=DOPPLER_HIGH, block_size=BLOCK,
                      alpha_ema=0.5, Q_fine_df=(50e3)**2, mod='qpsk'):
    """导频辅助 KF 载波恢复"""
    N = len(rx)
    k = np.arange(N)
    fo_est = fft_foe(rx, N_fft=min(N, 4096), nfft_zp=8192)
    rx_foc = rx * np.exp(-1j * fo_est * k)

    n_blocks = N // block_size
    Q = design_Q(turb_name, f_dot)
    Q_fine = Q.copy()
    Q_fine[1, 1] = Q_fine_df * T_S**2

    F_mat = np.array([[1.0, T_S], [0.0, 1.0]])
    H_mat = np.array([[1.0, 0.0]])

    x = np.array([0.0, 0.0])
    P = np.diag([(np.pi/4)**2, (2*np.pi*100e3)**2])

    h_est = max(h_med, 0.01)
    h_est_prev = h_est
    h_est_per_block = np.zeros(n_blocks)

    corrected = np.zeros(N, dtype=complex)
    known_pilots = get_pilots(n_pilots)

    for b in range(n_blocks):
        start = b * block_size
        end = start + block_size
        pilot_end = start + n_pilots

        # 阶段1: 导频
        for k_idx in range(start, pilot_end):
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            s_p = known_pilots[k_idx - start]
            y = rx_foc[k_idx] * np.conj(s_p)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

        # 阶段2: 估计 h
        pilot_residuals = corrected[start:pilot_end]
        s_pilots = known_pilots[:n_pilots]
        h_est_raw = abs(np.mean(pilot_residuals * np.conj(s_pilots)))**2
        h_est = alpha_ema * h_est_raw + (1 - alpha_ema) * h_est_prev
        h_est = max(h_est, 0.01)
        h_est_prev = h_est
        h_est_per_block[b] = h_est

        # 阶段3: 数据（判决导引）
        for k_idx in range(pilot_end, end):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = hard_decision(rx_rotated, mod=mod)
            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    # 剩余符号
    rem_start = n_blocks * block_size
    if rem_start < N:
        for k_idx in range(rem_start, N):
            R_val = 1.0 / (2 * gamma_bar * max(h_est, 0.01))
            x_pred = F_mat @ x
            P_pred = F_mat @ P @ F_mat.T + Q_fine
            rx_rotated = rx_foc[k_idx] * np.exp(-1j * x_pred[0])
            s_hat = hard_decision(rx_rotated, mod=mod)
            y = rx_foc[k_idx] * np.conj(s_hat)
            z_obs = np.angle(y)
            innov = z_obs - x_pred[0]
            innov = (innov + np.pi) % (2*np.pi) - np.pi
            S = H_mat @ P_pred @ H_mat.T + R_val
            K_gain = P_pred @ H_mat.T / S
            x = x_pred + K_gain.flatten() * innov
            x[0] = (x[0] + np.pi) % (2*np.pi) - np.pi
            P = (np.eye(2) - K_gain @ H_mat) @ P_pred
            corrected[k_idx] = rx_foc[k_idx] * np.exp(-1j * x[0])

    return corrected, h_est_per_block
