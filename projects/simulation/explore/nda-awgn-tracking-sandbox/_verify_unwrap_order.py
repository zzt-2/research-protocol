# -*- coding: utf-8 -*-
"""验证根因: unwrap 顺序对加权 seg 的影响.
正确顺序 (对齐主实验 nda_ml_recovery): seg_phi[k]=angle((w*yn).sum()) [不/M0, 升幂域]
                                       → unwrap → interp → 最后 /M0
错误顺序 (brief §2 给的): seg_phi[k]=angle((w*yn).sum())/M0 [先/M0, 还原域] → unwrap → interp
"""
import os, sys
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
sys.path.insert(0, _SIM_ROOT)
sys.path.insert(0, os.path.join(_SIM_ROOT, 'simulator'))
import _b11_params as P
import sc_nda_ml_sim as S
from common import m16apsk_mod, m16apsk_demod, resolve_m16apsk_blockwise

awgn_wiener_channel = S.awgn_wiener_channel

def rec_w_seg_WRONG(seg, M0):
    """错误顺序: 先/M0 再 unwrap (brief §2 给子agent的, 还原域 unwrap)."""
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    mag = np.abs(seg); mag[mag<1e-12]=1e-12
    yn = (seg/mag)**M0
    w = mag**2
    K = 8; seg_len = N//K
    seg_phi = np.empty(K); seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k*seg_len, (k+1)*seg_len
        seg_phi[k] = np.angle((w[lo:hi]*yn[lo:hi]).sum()) / M0   # 先/M0 (错)
        seg_center[k] = (lo+hi)/2.0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_est = np.interp(t, seg_center, seg_phi_unw)
    return seg * np.exp(-1j*phi_est)

def rec_w_seg_CORRECT(seg, M0):
    """正确顺序: 不/M0 升幂域 unwrap, 最后/M0 (对齐主实验 nda_ml_recovery)."""
    seg = np.asarray(seg, dtype=complex)
    N = len(seg)
    mag = np.abs(seg); mag[mag<1e-12]=1e-12
    yn = (seg/mag)**M0
    w = mag**2
    K = 8; seg_len = N//K
    seg_phi = np.empty(K); seg_center = np.empty(K)
    for k in range(K):
        lo, hi = k*seg_len, (k+1)*seg_len
        seg_phi[k] = np.angle((w[lo:hi]*yn[lo:hi]).sum())        # 不/M0 (升幂域, 对)
        seg_center[k] = (lo+hi)/2.0
    seg_phi_unw = np.unwrap(seg_phi)
    t = np.arange(N)
    phi_raised = np.interp(t, seg_center, seg_phi_unw)
    phi_est = phi_raised / M0                                    # 最后/M0
    return seg * np.exp(-1j*phi_est)

def ber_eval(rx, tx_bits, recovery_fn):
    N = len(rx); n_blk = N//P.N_DFT; L = n_blk*P.N_DFT
    rx_comp = np.zeros(L, dtype=complex)
    for b in range(n_blk):
        seg = rx[b*P.N_DFT:(b+1)*P.N_DFT]
        rx_comp[b*P.N_DFT:(b+1)*P.N_DFT] = recovery_fn(seg, P.M0)
    tb = tx_bits[:L*P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)

# 跑 AWGN 16/18/20
seed = P.SEED_AWGN
N_sym = P.N_BLOCKS * P.N_DFT
print(f"M0={P.M0}, LW={P.LASER_LW/1e3:.0f}kHz, SIGMA2_P={P.SIGMA2_P:.2e}, N_sym={N_sym}, seed={seed}")
print(f"{'SNR':>5} {'等权seg(主实验)':>16} {'加权seg(错unwrap)':>18} {'加权seg(对unwrap)':>18} {'VV':>12}")
import run_vv_ablation as VV
for snr in [16.0, 18.0, 20.0]:
    s = seed + int(snr*1000)
    rng = np.random.default_rng(s+7)
    bits = rng.integers(0,2,N_sym*P.BITS_PER_SYM)
    tx = m16apsk_mod(bits)
    rx, phi_true = awgn_wiener_channel(tx, snr, s)
    ne_eq, nb = ber_eval(rx, bits, lambda seg,M0: (lambda r: r*1)(*S.nda_ml_recovery(seg,M0,mod='m16apsk',assume_df_zero=True,intra_block_tracking='segmented')[:1]))
    ne_w_wrong, _ = ber_eval(rx, bits, rec_w_seg_WRONG)
    ne_w_correct, _ = ber_eval(rx, bits, rec_w_seg_CORRECT)
    ne_vv, _ = VV.ber_vv_awgn(rx, bits)
    print(f"{snr:>5.0f} {ne_eq/nb:>16.4e} {ne_w_wrong/nb:>18.4e} {ne_w_correct/nb:>18.4e} {ne_vv/nb:>12.4e}")
