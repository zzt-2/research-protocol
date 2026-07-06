"""Bug 修复 sanity check — _recovery.py Bug1 + _modulation.py Bug2.

验证:
  1. brief 中的 sanity check (全帧单块恢复, BER old vs new)
  2. 诊断脚本复现: 逐块 256 恢复, NDA-fixed BER @ 18dB 应接近 2.07e-3
运行: cd projects/simulation && python explore/b11-nda-ml-sto-cpe/_bugfix_sanity_check.py
"""
import os
import sys

import numpy as np

_SIM_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)

from common import (
    nda_ml_recovery, resolve_m16apsk_blockwise,
    m16apsk_mod, m16apsk_demod, ber_count_m16apsk,
)

N_DFT = 256
M0 = 8
BITS_PER_SYM = 4


def channel_awgn_wiener(tx, snr_db, seed):
    """B11 行 33: r(k) = s(k)·exp(j·θ(k)) + n(k), θ=Wiener PN, 无 FOE/CFO."""
    rng = np.random.default_rng(seed)
    N = len(tx)
    sigma2_p = 2 * np.pi * 500e3 * (1 / 25e9)
    phi = np.cumsum(rng.normal(0.0, np.sqrt(sigma2_p), N))
    noise_var = 1.0 / (2.0 * 10.0 ** (snr_db / 10.0))
    noise = np.sqrt(noise_var) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return tx * np.exp(1j * phi) + noise, phi


# =============================================================================
# Check 1: brief 中的 sanity check (全帧, 简化)
# =============================================================================
def check1_brief_sanity():
    print("=" * 70)
    print("Check 1: brief sanity check (全帧单块恢复)")
    print("=" * 70)
    np.random.seed(0)
    N = 102400
    bits = np.random.randint(0, 2, N * 4)
    tx = m16apsk_mod(bits)
    sigma2_p = 2 * np.pi * 500e3 * (1 / 25e9)
    phi = np.cumsum(np.random.normal(0, np.sqrt(sigma2_p), N))
    rx = tx * np.exp(1j * phi) + np.sqrt(1 / (2 * 10 ** (15 / 10))) * (
        np.random.randn(N) + 1j * np.random.randn(N)
    )

    # 修前 (assume_df_zero=False)
    rx_comp_old, _, _, _ = nda_ml_recovery(rx, M0=M0, assume_df_zero=False)
    ber_old = ber_count_m16apsk(bits[:len(rx_comp_old) * 4], rx_comp_old)

    # 修后 (assume_df_zero=True + blockwise resolve)
    rx_comp_new, _, _, _ = nda_ml_recovery(rx, M0=M0, assume_df_zero=True)
    rx_comp_new = resolve_m16apsk_blockwise(rx_comp_new, bits, block_size=256)
    ber_new = ber_count_m16apsk(bits[:len(rx_comp_new) * 4], rx_comp_new)

    print(f"  BER old (bug, FFT-df + 全帧单旋转): {ber_old:.4e}")
    print(f"  BER new (assume_df_zero + blockwise): {ber_new:.4e}")
    print(f"  改善倍数: {ber_old / max(ber_new, 1e-12):.2f}x")
    return ber_old, ber_new


# =============================================================================
# Check 2: 诊断脚本复现 — 逐块 256 恢复 (Variant B 正确做法)
# =============================================================================
def check2_diagnostic_repro():
    print("\n" + "=" * 70)
    print("Check 2: 诊断脚本复现 (逐块 256, Variant B) — 应接近 2.07e-3 @ 18dB")
    print("=" * 70)
    SEED_BASE = 20240701
    for snr in [15.0, 18.0, 20.0]:
        seed = SEED_BASE + int(snr * 1000)
        rng_bits = np.random.default_rng(seed + 7)
        N_sym = 400 * N_DFT  # 102400
        bits = rng_bits.integers(0, 2, N_sym * BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = channel_awgn_wiener(tx, snr, seed)

        n_blk = len(rx) // N_DFT
        L = n_blk * N_DFT

        # 修前: 逐块 FFT-df + 全局 resolve_m16apsk
        rx_comp_old = np.zeros(L, dtype=complex)
        for b in range(n_blk):
            seg = rx[b * N_DFT:(b + 1) * N_DFT]
            rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=False)
            rx_comp_old[b * N_DFT:(b + 1) * N_DFT] = rc
        # 全局单旋转 BER (前两轮 bug 复现)
        from common import resolve_m16apsk
        tb = bits[:L * BITS_PER_SYM]
        ber_old_global = resolve_m16apsk(rx_comp_old, tb)

        # 修后: 逐块 assume_df_zero=True + blockwise resolve
        rx_comp_new = np.zeros(L, dtype=complex)
        for b in range(n_blk):
            seg = rx[b * N_DFT:(b + 1) * N_DFT]
            rc, _, _, _ = nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True)
            rx_comp_new[b * N_DFT:(b + 1) * N_DFT] = rc
        resolved = resolve_m16apsk_blockwise(rx_comp_new, tb, block_size=N_DFT)
        ber_new = np.mean(tb != m16apsk_demod(resolved))

        print(f"  SNR={snr:4.1f} dB | "
              f"NDA[old, glob-rotate]: {ber_old_global:.3e} (灾难)  |  "
              f"NDA[new, blk-resolve]: {ber_new:.3e}")
        if snr == 18.0:
            print(f"           ↑ 诊断 Variant B @ 18dB = 2.07e-3 → 差距: "
                  f"{ber_new/2.07e-3:.2f}x")
    return


if __name__ == '__main__':
    check1_brief_sanity()
    check2_diagnostic_repro()
