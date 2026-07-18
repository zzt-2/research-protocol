# -*- coding: utf-8 -*-
"""A4 切换策略 30 seed（基准配置 geth13_cvmar1.1）— 简报主引数据.

5 seed 偏少（weak CI 太宽），补到 30 seed 让 CI 可信。
只跑基准配置（γ_eff_th=13, CV_margin=1.10），不做敏感性扫描。
"""
import os
import sys
import json
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIM_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..'))
if _SIM_ROOT not in sys.path:
    sys.path.insert(0, _SIM_ROOT)
_SIM_DIR = os.path.join(_SIM_ROOT, 'simulator')
if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)

import _b11_params as P
import sc_nda_ml_sim as S
from common import (
    m16apsk_mod, m16apsk_demod,
    resolve_m16apsk_blockwise,
    nda_ml_recovery, da_ml_recovery,
    mmse_equalize, amp_limit,
    generate_shared_realization_apsk,
)
from params import SimulationConfig
from scipy import stats

OUT_DIR = os.path.join(_SIM_ROOT, 'explore', 'nda-awgn-tracking-sandbox')
N_SEEDS = 30
GAMMA_EFF_TH = 13.0
CV_MARGIN = 1.10


def cv_awgn_theory(snr_db):
    return 0.74 + 0.12 * np.exp(-snr_db / 5.0)


def decide(rx_seg, gamma_db, gamma_lin):
    pwr = np.abs(rx_seg) ** 2
    cv = float(np.std(pwr) / max(np.mean(pwr), 1e-12))
    if cv < cv_awgn_theory(gamma_db) * CV_MARGIN:
        return 'nda'
    h = max(float(np.mean(pwr) - 1.0 / (2 * gamma_lin)), 1e-6)
    return 'da' if gamma_db + 10 * np.log10(h) < GAMMA_EFF_TH else 'nda'


def per_block(rx_blind, rx_pilot, bits, tx_sym):
    omega = S.fft_foe_m0_omega(rx_blind, P.M0)
    k = np.arange(P.N_DFT)
    rc_nda, _, _, _ = nda_ml_recovery(rx_blind * np.exp(-1j * omega * k),
                                      P.M0, mod='m16apsk', assume_df_zero=True)
    pidx = np.arange(0, P.N_DFT, P.DA_PILOT_SPACING)
    rc_da, _, _ = da_ml_recovery(rx_pilot, pilot_idx=pidx,
                                 pilot_sym=tx_sym[pidx], mod='m16apsk')
    tb = bits[:P.N_DFT * P.BITS_PER_SYM]
    res_nda = resolve_m16apsk_blockwise(rc_nda, tb, block_size=P.BLOCK_SIZE_RESOLVE)
    ne_nda = int(np.sum(tb != m16apsk_demod(res_nda)))
    dm = m16apsk_demod(rc_da)
    is_d = np.ones(P.N_DFT, dtype=bool); is_d[pidx] = False
    tba = tb.reshape(P.N_DFT, P.BITS_PER_SYM); dma = dm.reshape(P.N_DFT, P.BITS_PER_SYM)
    ne_da = int(np.sum(tba[is_d] != dma[is_d]))
    return ne_nda, P.N_DFT * P.BITS_PER_SYM, ne_da, int(np.sum(is_d) * P.BITS_PER_SYM)


def ci_t(data):
    a = np.asarray(data, dtype=float)
    n = len(a)
    mean = float(np.mean(a)); std = float(np.std(a, ddof=1)) if n > 1 else 0.0
    hw = float(stats.t.ppf(0.975, n - 1)) * std / np.sqrt(n) if n > 1 else 0.0
    return mean, std, hw, mean - hw, mean + hw


def main():
    cfg = SimulationConfig()
    NB = P.N_BLOCKS; Ns = P.N_DFT
    t0 = time.time()
    print(f"A4 切换 {N_SEEDS} seed (geth{GAMMA_EFF_TH}_cvmar{CV_MARGIN})")

    raw = {sc: [] for sc in ['awgn','weak','moderate','strong']}
    # AWGN
    for i in range(N_SEEDS):
        sb = P.SEED_AWGN + i
        per_snr = []
        for snr in P.SNR_AWGN_DB:
            gl = 10**(snr/10)
            seed = sb + int(snr*1000)
            rng = np.random.default_rng(seed+7)
            bits = rng.integers(0,2, NB*Ns*P.BITS_PER_SYM)
            tx = m16apsk_mod(bits)
            rx, _ = S.awgn_wiener_channel(tx, snr, seed)
            e_n=e_d=e_s=0; b_n=b_d=b_s=0
            for b in range(NB):
                seg = rx[b*Ns:(b+1)*Ns]
                tb = bits[b*Ns*P.BITS_PER_SYM:(b+1)*Ns*P.BITS_PER_SYM]
                rc_n,_,_,_ = nda_ml_recovery(seg, P.M0, mod='m16apsk', assume_df_zero=True, intra_block_tracking='segmented')
                res = resolve_m16apsk_blockwise(rc_n, tb, block_size=P.BLOCK_SIZE_RESOLVE)
                ne_n = int(np.sum(tb != m16apsk_demod(res)))
                pidx = np.arange(0,Ns,P.DA_PILOT_SPACING)
                rc_d,_,_ = da_ml_recovery(seg, pilot_idx=pidx, pilot_sym=tx[b*Ns+pidx], mod='m16apsk')
                dm = m16apsk_demod(rc_d)
                isd = np.ones(Ns,dtype=bool); isd[pidx]=False
                tba = tb.reshape(Ns,P.BITS_PER_SYM); dma = dm.reshape(Ns,P.BITS_PER_SYM)
                ne_d = int(np.sum(tba[isd]!=dma[isd]))
                e_n+=ne_n; b_n+=Ns*P.BITS_PER_SYM; e_d+=ne_d; b_d+=int(np.sum(isd)*P.BITS_PER_SYM)
                c = decide(seg, snr, gl)
                if c=='da': e_s+=ne_d; b_s+=int(np.sum(isd)*P.BITS_PER_SYM)
                else: e_s+=ne_n; b_s+=Ns*P.BITS_PER_SYM
            per_snr.append({'snr_db':float(snr),'nda':e_n/b_n,'da':e_d/b_d,'sw':e_s/b_s})
        raw['awgn'].append(per_snr)
        if (i+1)%5==0: print(f"  awgn seed {i+1}/{N_SEEDS} ({time.time()-t0:.0f}s)")

    # 湍流
    for turb in ['weak','moderate','strong']:
        for i in range(N_SEEDS):
            s0 = P.SEED_TURB0 + i*NB
            per_snr = []
            for gdb in P.SNR_TURB_DB:
                gl = 10**(gdb/10)
                e_n=e_d=e_s=0; b_n=b_d=b_s=0
                for b in range(NB):
                    r = generate_shared_realization_apsk(Ns, gl, turb, cfg.doppler.DOPPLER_HIGH, mod='m16apsk', seed=s0+b)
                    rx_raw=r['rx_raw']; bits=r['bits']; txs=r['tx']
                    hb = S.estimate_h_blind_perblock(rx_raw, gl)
                    rxb = amp_limit(mmse_equalize(rx_raw, hb, gl), 3.0)
                    hp = S.estimate_h_pilot_perblock(rx_raw, txs, gl)
                    rxp = amp_limit(mmse_equalize(rx_raw, hp, gl), 3.0)
                    ne_n,nb_n,ne_d,nb_d = per_block(rxb, rxp, bits, txs)
                    e_n+=ne_n; b_n+=nb_n; e_d+=ne_d; b_d+=nb_d
                    c = decide(rx_raw, gdb, gl)
                    if c=='da': e_s+=ne_d; b_s+=nb_d
                    else: e_s+=ne_n; b_s+=nb_n
                per_snr.append({'snr_db':float(gdb),'nda':e_n/b_n,'da':e_d/b_d,'sw':e_s/b_s})
            raw[turb].append(per_snr)
        print(f"  {turb} done ({time.time()-t0:.0f}s)")

    elapsed = time.time()-t0
    # 聚合
    summary = {}
    for sc in ['awgn','weak','moderate','strong']:
        snrs = [p['snr_db'] for p in raw[sc][0]]
        pts = []
        for j,snr in enumerate(snrs):
            nda=[raw[sc][i][j]['nda'] for i in range(N_SEEDS)]
            da=[raw[sc][i][j]['da'] for i in range(N_SEEDS)]
            sw=[raw[sc][i][j]['sw'] for i in range(N_SEEDS)]
            mx=[min(n,d) for n,d in zip(nda,da)]
            svm=[10*np.log10(m/s) if s>0 and m>0 else 0 for m,s in zip(mx,sw)]
            m_n,*_=ci_t(nda); m_d,*_=ci_t(da); m_sw,s_sw,hw_sw,lo_sw,hi_sw=ci_t(sw)
            m_mx,*_=ci_t(mx)
            m_svm,s_svm,hw_svm,lo_sv,hi_sv=ci_t(svm)
            pts.append({'snr_db':float(snr),
                'nda_ber_mean':m_n,'da_ber_mean':m_d,'switch_ber_mean':m_sw,
                'switch_ber_ci95':[lo_sw,hi_sw],'max_ber_mean':m_mx,
                'switch_vs_max_db_mean':m_svm,'switch_vs_max_db_ci95':[lo_sv,hi_sv],
                'per_seed_switch_vs_max_db':svm})
        summary[sc]={'snr_db':snrs,'points':pts}

    out={'meta':{'task':'A4 切换 30 seed','n_seeds':N_SEEDS,
                 'gamma_eff_th':GAMMA_EFF_TH,'cv_margin':CV_MARGIN,
                 'cv_model':'CV_awgn(snr)=0.74+0.12*exp(-snr/5)',
                 'ci_method':f't-dist 95% df={N_SEEDS-1}','elapsed_sec':float(elapsed)},
         'summary':summary}
    out_json=os.path.join(OUT_DIR,'_a4_switch_30seed.json')
    with open(out_json,'w',encoding='utf-8') as f:
        json.dump(out,f,indent=2,ensure_ascii=False,default=lambda x:float(x) if isinstance(x,(np.floating,)) else x)
    print(f"[保存] {out_json} ({elapsed:.0f}s)")
    print(f"\n{'场景':<9}{'γd':>5}{'NDA':>10}{'DA':>10}{'SW':>10}{'SW-max':>9}{'CI95':>16}")
    for sc in ['awgn','weak','moderate','strong']:
        for p in summary[sc]['points']:
            svm=p['switch_vs_max_db_mean']; lo,hi=p['switch_vs_max_db_ci95']
            print(f"{sc:<9}{p['snr_db']:>5.0f}{p['nda_ber_mean']:>10.2e}{p['da_ber_mean']:>10.2e}{p['switch_ber_mean']:>10.2e}{svm:>+8.2f}  [{lo:+.2f},{hi:+.2f}]")

if __name__=='__main__':
    main()
