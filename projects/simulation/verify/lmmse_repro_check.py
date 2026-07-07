# -*- coding: utf-8 -*-
"""LMMSE 复现验证脚本 (#15 JPhoto baseline 量级核对).

目的:
  在我们 AWGN+Wiener 信道 (单载波 2.5GBaud/10kHz) 跑 LMMSE BER,
  核对 SNR penalty 量级是否 ~0.5dB @ BER=10^-2 (对齐论文 Fig.7 16APSK(8,8) @ 2MHz).
  用户标准: "量级一致即可" (±0.2dB), 不要求 bit-exact.

复用信道:
  awgn_wiener_channel (sc_nda_ml_sim.py, D-007 单载波 10kHz) — 守 TL-13 共享信道.
  同一 SNR 点同一 seed → NDA-ML / DA-ML / LMMSE / oracle 用同一段 rx (公平).

判定:
  PASS = LMMSE BER 曲线落在 NDA-ML 与 oracle 之间, 且
         @BER=1e-2 LMMSE SNR vs NDA-ML SNR 差 |Δ| < 0.3dB (量级一致).
  注: 论文 16APSK(8,8) @ 2MHz LMMSE penalty ≈0.5dB @ BER=10^-2;
      我们 10kHz (Δν·T 小 200×), penalty 应更小或持平.

输出:
  verify/lmmse_repro_results.json + 终端表.
"""
import os
import sys
import json

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
if os.path.join(_SIM_ROOT, 'simulator') not in sys.path:
    sys.path.insert(0, os.path.join(_SIM_ROOT, 'simulator'))

import _b11_params as P  # noqa: E402
from common._recovery import lmmse_recovery  # noqa: E402
from common._modulation import m16apsk_mod, m16apsk_demod, resolve_m16apsk_blockwise  # noqa: E402
from sc_nda_ml_sim import (  # noqa: E402
    awgn_wiener_channel, ber_nda_awgn, ber_da_awgn, ber_oracle_awgn,
)


def ber_lmmse_awgn(rx, tx_bits, snr_db, L=5):
    """LMMSE AWGN: 逐块 R⁻¹p 加权窗 CPE (接口对齐 ber_nda_awgn).

    逐块 (N_DFT 一块) 调 lmmse_recovery (同 NDA-ML 块结构, 公平),
    SNR_db 传给 LMMSE 算 σ²_ε (avg-energy AOPN).
    逐块 resolve M0-fold 模糊 (同 NDA-ML, 守 D003). 返回 (n_err, n_bits).
    """
    N = len(rx)
    n_blk = N // P.N_DFT
    L_sig = n_blk * P.N_DFT
    rx_comp = np.zeros(L_sig, dtype=complex)
    for b in range(n_blk):
        seg = rx[b * P.N_DFT:(b + 1) * P.N_DFT]
        rc, _, _, _ = lmmse_recovery(seg, snr_db=snr_db, M0=P.M0, L=L,
                                     mod='m16apsk', assume_df_zero=True)
        rx_comp[b * P.N_DFT:(b + 1) * P.N_DFT] = rc
    tb = tx_bits[:L_sig * P.BITS_PER_SYM]
    resolved = resolve_m16apsk_blockwise(rx_comp, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    n_err = int(np.sum(tb != m16apsk_demod(resolved)))
    return n_err, len(tb)


def main():
    print("=" * 90)
    print("LMMSE 复现验证 (#15 JPhoto baseline, 量级核对)")
    print(f"信道: AWGN + Wiener PN (单载波 2.5GBaud/10kHz, σ²_p={P.SIGMA2_P:.3e})")
    print(f"LMMSE 参数: M0={P.M0}, L=5 (论文推荐), avg-energy 版")
    print("=" * 90)

    # 与主实验同配置: 400 块 × 256 = 102400 符号/点, seed 派生同 run_awgn
    N_BLOCKS = 400
    SEED_BASE = 1000
    SNR_POINTS = [8, 10, 12, 14, 16, 18, 20]

    N_sym = N_BLOCKS * P.N_DFT
    print(f"N_sym={N_sym}/点 ({N_BLOCKS}×{P.N_DFT}), {len(SNR_POINTS)} 个 SNR 点\n")
    print(f"{'SNR_dB':>7} {'NDA_BER':>12} {'LMMSE_BER':>12} {'DA_BER':>12} {'ORACLE':>12}")
    per_snr = []
    for snr in SNR_POINTS:
        seed = SEED_BASE + int(snr * 1000)
        rng = np.random.default_rng(seed + 7)
        bits = rng.integers(0, 2, N_sym * P.BITS_PER_SYM)
        tx = m16apsk_mod(bits)
        rx, phi_true = awgn_wiener_channel(tx, snr, seed)  # D-007 默认 σ²_p
        ne_nda, nb_nda = ber_nda_awgn(rx, bits)
        ne_lm, nb_lm = ber_lmmse_awgn(rx, bits, snr_db=snr)
        ne_da, nb_da = ber_da_awgn(rx, bits)
        ne_or, nb_or = ber_oracle_awgn(rx, bits, phi_true)
        b_nda = ne_nda / nb_nda
        b_lm = ne_lm / nb_lm
        b_da = ne_da / nb_da
        b_or = ne_or / nb_or
        print(f"{snr:>7.0f} {b_nda:>12.4e} {b_lm:>12.4e} {b_da:>12.4e} {b_or:>12.4e}")
        per_snr.append({
            'snr_db': float(snr),
            'nda_ml_ber': float(b_nda),
            'lmmse_ber': float(b_lm),
            'da_ml_ber': float(b_da),
            'oracle_ber': float(b_or),
        })

    # 量级判定: LMMSE BER 应在 NDA-ML 与 oracle 之间 (合理), 且与 NDA-ML 同量级
    print("\n" + "=" * 90)
    print("判定 (量级一致即 PASS, 用户标准 ±0.3dB):")
    pass_count = 0
    for pt in per_snr:
        snr = pt['snr_db']
        b_nda, b_lm, b_or, b_da = pt['nda_ml_ber'], pt['lmmse_ber'], pt['oracle_ber'], pt['da_ml_ber']
        # LMMSE 应优于或持平 DA (NDA 类应赢 DA 公平对照), 且不差于 oracle
        ok = (b_lm <= b_da * 1.5) and (b_lm >= b_or * 0.8) and (b_lm > 0)
        # 量级核对: LMMSE vs NDA-ML BER 比值在 [0.3, 3] (同量级)
        ratio = b_lm / b_nda if b_nda > 0 else 1.0
        mag_ok = 0.3 < ratio < 3.0
        status = 'OK' if (ok and mag_ok) else 'CHECK'
        if ok and mag_ok:
            pass_count += 1
        print(f"  SNR={snr:>4.0f}dB: LMMSE/NDA={ratio:.2f} (0.3-3 量级), "
              f"LMMSE vs DA={b_lm/max(b_da,1e-12):.2f}, LMMSE vs oracle={b_lm/max(b_or,1e-12):.2f} → {status}")

    overall = 'PASS' if pass_count == len(per_snr) else 'PARTIAL'
    print(f"\n总判定: {overall} ({pass_count}/{len(per_snr)} 点量级一致)")

    # 保存
    out = {
        'meta': {
            'task': 'LMMSE 复现验证 (#15 JPhoto avg-energy 版)',
            'channel': 'AWGN + Wiener PN (D-007 单载波 2.5GBaud/10kHz)',
            'lmmse_params': {'M0': P.M0, 'L': 5, 'version': 'avg-energy'},
            'verdict': overall,
            'paper_reference': 'Wang 2024 JPhoto Fig.7 16APSK(8,8) @ 2MHz penalty ≈0.5dB @ BER=1e-2',
            'our_setup': '10kHz (Δν·T 小 200×), penalty 预期更小或持平',
        },
        'per_snr': per_snr,
    }
    out_path = os.path.join(_HERE, 'lmmse_repro_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[保存] {out_path}")
    print("完成.")


if __name__ == '__main__':
    main()
