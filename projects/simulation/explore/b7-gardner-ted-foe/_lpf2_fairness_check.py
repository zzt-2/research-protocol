"""LPF2 公平性验证（systematic-debugging Phase 3 最小化测试）。

假设：B7 vs baseline 的 +4dB BER gain 主因是 LPF2 只给 B7 加了（L851），
其他 baseline（PSA/4thpow/Kay）没有对等 LPF2 预处理。
验证：给所有 baseline 都加 LPF2，看 gain 是否大幅缩小。

只跑 f_D=5GHz（线性区内，所有baseline都该能估准）+ 3 OSNR 点，
精简配置快速验证假设（非正式 MVE）。
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import b7_gardner_ted_mve as M

N_SYM = 4096
N_SEED = 3
F_D_GHZ = 5.0
OSNR_LIST = [17.0, 14.0, 11.0]
SCAN_GRID = np.arange(0, 24, 1.0) * 1e9  # 单边 0-23GHz

def run_one(rx, fs_rx, alpha_psa, method, use_lpf2):
    """跑一个 baseline，可选 LPF2。返回 (f_est, ber)。"""
    t_v = np.arange(rx.size) / fs_rx
    if method == "B7":
        f_est, _, _ = M.b7_proposed_foe(rx, fs_rx, SCAN_GRID, lpf2_en=True)
        rx_c = rx * np.exp(-1j * 2 * np.pi * f_est * t_v)
        if use_lpf2:
            rx_c = M._lpf2(rx_c, fs_rx)
        rx_c, _ = M.residual_foe_mth_power(rx_c, fs_rx, M=4)
    elif method == "PSA":
        rx_c, f_est = M.psa_foe_two_stage(rx, fs_rx, alpha_psa)
        if use_lpf2:
            rx_c = M._lpf2(rx_c, fs_rx)
        rx_c, _ = M.residual_foe_mth_power(rx_c, fs_rx, M=4)
    elif method == "4thpow":
        rx_c, f_est = M.fourth_power_foe(rx, fs_rx)
        if use_lpf2:
            rx_c = M._lpf2(rx_c, fs_rx)
        rx_c, _ = M.residual_foe_mth_power(rx_c, fs_rx, M=4)
    elif method == "Kay":
        rx_c, f_est = M.kay_foe(rx, fs_rx)
        if use_lpf2:
            rx_c = M._lpf2(rx_c, fs_rx)
        rx_c, _ = M.residual_foe_mth_power(rx_c, fs_rx, M=4)
    out, _ = M.gardner_1986_tr(rx_c, fs_rx, return_timing_error=True)
    return f_est, out

def main():
    t0 = time.time()
    f_d = F_D_GHZ * 1e9
    fs_rx = M.SPS_RX * M.BAUD
    # 校准 PSA alpha（跟主脚本一致）
    tx_high_s_cal, _ = M.make_tx(N_SYM, M.SPS_GEN, M.ROLL_OFF,
                                  np.random.default_rng(20260707))
    tx_rx_cal, _ = M.decimate_to_rx(tx_high_s_cal)
    alpha_psa, _, _ = M.calibrate_psa_alpha_sequential(tx_rx_cal, fs_rx)
    print(f"[calib] alpha_psa = {alpha_psa/1e9:.3f} GHz")

    methods = ["B7", "PSA", "4thpow", "Kay"]
    results = {"no_lpf2": {}, "with_lpf2_all": {}}

    for osnr_db in OSNR_LIST:
        print(f"\n=== OSNR={osnr_db:.0f}dB, f_D={F_D_GHZ}GHz ===")
        for use_lpf2, tag in [(False, "no_lpf2"), (True, "with_lpf2_all")]:
            if use_lpf2 and tag == "no_lpf2":
                continue
            bers = {m: [] for m in methods}
            ests = {m: [] for m in methods}
            for seed_i in range(N_SEED):
                rng = np.random.default_rng(30000 + seed_i * 31 + int(round(osnr_db * 13)))
                tx_high_s, ref_syms = M.make_tx(N_SYM, M.SPS_GEN, M.ROLL_OFF,
                                                 np.random.default_rng(20260707))
                tx_rx, _ = M.decimate_to_rx(tx_high_s)
                rx = M.inject_foe(tx_rx, f_d, fs_rx)
                rx = M.add_awgn(rx, osnr_db, M.BAUD, rng)
                for m in methods:
                    # B7 永远用 LPF2（它是 B7 流程一部分），其他 baseline 按 use_lpf2
                    lpf2_for_this = True if m == "B7" else use_lpf2
                    f_est, out = run_one(rx, fs_rx, alpha_psa, m, lpf2_for_this)
                    ber = M.qpsk_hard_decision_ber(out, ref_syms)
                    bers[m].append(ber)
                    ests[m].append(f_est)
            key = f"osnr{int(osnr_db)}"
            results[tag].setdefault(key, {})
            line_parts = []
            for m in methods:
                bm = float(np.mean(bers[m]))
                em = abs(float(np.mean(ests[m])) - f_d) / 1e9
                results[tag][key][m] = {"ber": bm, "est_err_GHz": round(em, 3)}
                line_parts.append(f"{m}={bm:.4g}(err{em:.2f})")
            print(f"  [{tag}] " + " ".join(line_parts))

    # 计算 gain 变化
    print("\n" + "=" * 80)
    print("假设验证：LPF2 全加后 B7 vs baseline 的 gain 变化")
    print("=" * 80)
    for osnr_db in OSNR_LIST:
        key = f"osnr{int(osnr_db)}"
        b7_ber = results["no_lpf2"][key]["B7"]["ber"]  # B7 永远有LPF2
        print(f"\nOSNR={osnr_db:.0f}dB (B7 BER={b7_ber:.4g}, B7永有LPF2):")
        for m in ["PSA", "4thpow", "Kay"]:
            no = results["no_lpf2"][key][m]["ber"]
            wit = results["with_lpf2_all"][key][m]["ber"]
            gain_no = 10 * np.log10(no / b7_ber) if b7_ber > 0 and no > 0 else float('nan')
            gain_wit = 10 * np.log10(wit / b7_ber) if b7_ber > 0 and wit > 0 else float('nan')
            print(f"  {m:>7}: noLPF2 BER={no:.4g}(gain={gain_no:+.2f}dB) | "
                  f"withLPF2 BER={wit:.4g}(gain={gain_wit:+.2f}dB) | "
                  f"Δgain={gain_wit-gain_no:+.2f}dB")

    out = {"meta": {"n_sym": N_SYM, "n_seed": N_SEED, "f_D_GHz": F_D_GHZ,
                     "osnr_list": OSNR_LIST, "elapsed_s": round(time.time()-t0, 1)},
           "results": results}
    out_path = os.path.join(os.path.dirname(__file__), "_lpf2_fairness_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[wrote] {out_path} (elapsed {out['meta']['elapsed_s']}s)")

if __name__ == "__main__":
    main()
