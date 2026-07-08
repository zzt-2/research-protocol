"""B7 范围优势公平对照测试（类比 B5 D003 实验 B）。

B5 教训：范围优势可能是特权假象（给 baseline 配同等条件后归零）。
B7 的 2.1× 范围优势（全 baud 周期覆盖 vs 4thpow/PSA 半 baud 限制）
必须做公平范围对照：给所有 baseline 加 LPF2 + 同等条件，看范围优势是否残留。

判据（类比 B5 D003 实验 B）：
- 若 4thpow+LPF2 在 12-23GHz 也能收敛 → B7 范围优势归零（特权假象）
- 若 4thpow+LPF2 在 12-23GHz 仍全爆 → B7 范围优势真实（机制本质）

跑 f_D=0/5/12/15/23 GHz × OSNR 17dB，B7 vs 4thpow ± LPF2。
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import b7_gardner_ted_mve as M

N_SYM = 4096
N_SEED = 3
F_D_GRID_GHZ = [0.0, 5.0, 12.0, 15.0, 23.0]
OSNR_DB = 17.0
SCAN_GRID = np.arange(0, 24, 1.0) * 1e9

def run_one(rx, fs_rx, alpha_psa, method, use_lpf2):
    t_v = np.arange(rx.size) / fs_rx
    if method == "B7":
        f_est, _, _ = M.b7_proposed_foe(rx, fs_rx, SCAN_GRID, lpf2_en=True)
        rx_c = rx * np.exp(-1j * 2 * np.pi * f_est * t_v)
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
    elif method == "PSA":
        rx_c, f_est = M.psa_foe_two_stage(rx, fs_rx, alpha_psa)
        if use_lpf2:
            rx_c = M._lpf2(rx_c, fs_rx)
        rx_c, _ = M.residual_foe_mth_power(rx_c, fs_rx, M=4)
    out, _ = M.gardner_1986_tr(rx_c, fs_rx, return_timing_error=True)
    return f_est

def main():
    t0 = time.time()
    fs_rx = M.SPS_RX * M.BAUD
    tx_high_s_cal, _ = M.make_tx(N_SYM, M.SPS_GEN, M.ROLL_OFF,
                                  np.random.default_rng(20260707))
    tx_rx_cal, _ = M.decimate_to_rx(tx_high_s_cal)
    alpha_psa, _, _ = M.calibrate_psa_alpha_sequential(tx_rx_cal, fs_rx)

    methods = ["B7", "4thpow", "Kay", "PSA"]
    results = {"no_lpf2": {}, "with_lpf2_all": {}}

    for fd_ghz in F_D_GRID_GHZ:
        f_d = fd_ghz * 1e9
        print(f"\n=== f_D={fd_ghz}GHz, OSNR={OSNR_DB}dB ===")
        for tag, give_lpf2_to_baseline in [("no_lpf2", False), ("with_lpf2_all", True)]:
            bers = {m: [] for m in methods}
            ests = {m: [] for m in methods}
            for seed_i in range(N_SEED):
                rng = np.random.default_rng(40000 + seed_i * 31 + int(fd_ghz * 7))
                tx_high_s, ref_syms = M.make_tx(N_SYM, M.SPS_GEN, M.ROLL_OFF,
                                                 np.random.default_rng(20260707))
                tx_rx, _ = M.decimate_to_rx(tx_high_s)
                rx = M.inject_foe(tx_rx, f_d, fs_rx)
                rx = M.add_awgn(rx, OSNR_DB, M.BAUD, rng)
                for m in methods:
                    lpf2 = True if m == "B7" else give_lpf2_to_baseline
                    f_est = run_one(rx, fs_rx, alpha_psa, m, lpf2)
                    # 重算 ber
                    t_v = np.arange(rx.size) / fs_rx
                    rx_c = rx * np.exp(-1j * 2 * np.pi * f_est * t_v) if m in ("4thpow","Kay","PSA") else rx
                    # 简化：直接复用 run_one 内部已补偿，这里 run_one 返回 f_est 但 rx_c 已丢
                    # 重做一次拿 ber
                    bers[m].append(None)  # placeholder, recompute below
                    ests[m].append(f_est)
            # 重算 ber（run_one 内部已补偿+TR，但没返回 out；这里重跑拿 ber）
            bers2 = {m: [] for m in methods}
            for seed_i in range(N_SEED):
                rng = np.random.default_rng(40000 + seed_i * 31 + int(fd_ghz * 7))
                tx_high_s, ref_syms = M.make_tx(N_SYM, M.SPS_GEN, M.ROLL_OFF,
                                                 np.random.default_rng(20260707))
                tx_rx, _ = M.decimate_to_rx(tx_high_s)
                rx = M.inject_foe(tx_rx, f_d, fs_rx)
                rx = M.add_awgn(rx, OSNR_DB, M.BAUD, rng)
                for m in methods:
                    lpf2 = True if m == "B7" else give_lpf2_to_baseline
                    # inline 重建（跟 run_one 同逻辑）拿 out 算 ber
                    t_v = np.arange(rx.size) / fs_rx
                    if m == "B7":
                        fe, _, _ = M.b7_proposed_foe(rx, fs_rx, SCAN_GRID, lpf2_en=True)
                        rc = rx * np.exp(-1j*2*np.pi*fe*t_v)
                        if lpf2: rc = M._lpf2(rc, fs_rx)
                    elif m == "4thpow":
                        rc, fe = M.fourth_power_foe(rx, fs_rx)
                        if lpf2: rc = M._lpf2(rc, fs_rx)
                    elif m == "Kay":
                        rc, fe = M.kay_foe(rx, fs_rx)
                        if lpf2: rc = M._lpf2(rc, fs_rx)
                    elif m == "PSA":
                        rc, fe = M.psa_foe_two_stage(rx, fs_rx, alpha_psa)
                        if lpf2: rc = M._lpf2(rc, fs_rx)
                    rc, _ = M.residual_foe_mth_power(rc, fs_rx, M=4)
                    out, _ = M.gardner_1986_tr(rc, fs_rx, return_timing_error=True)
                    bers2[m].append(M.qpsk_hard_decision_ber(out, ref_syms))
            key = f"f_D{int(fd_ghz)}GHz"
            results[tag].setdefault(key, {})
            line = [f"[{tag}]"]
            for m in methods:
                bm = float(np.mean(bers2[m]))
                em = abs(float(np.mean(ests[m])) - f_d) / 1e9
                results[tag][key][m] = {"ber": bm, "est_err_GHz": round(em, 3)}
                line.append(f"{m}={bm:.3g}(e{em:.1f})")
            print("  " + " ".join(line))

    # 范围优势公平性总结
    print("\n" + "=" * 85)
    print("范围优势公平性总结（B7 可解调 vs baseline 可解调，BER<0.05 判可解调）")
    print("=" * 85)
    for tag in ["no_lpf2", "with_lpf2_all"]:
        ok = {m: 0 for m in methods}
        for fd_ghz in F_D_GRID_GHZ:
            key = f"f_D{int(fd_ghz)}GHz"
            for m in methods:
                if results[tag][key][m]["ber"] < 0.05:
                    ok[m] += 1
        print(f"\n[{tag}] 可解调点数（共{len(F_D_GRID_GHZ)}点，BER<0.05）:")
        for m in methods:
            print(f"  {m:>7}: {ok[m]}/{len(F_D_GRID_GHZ)}")
        b7_ok = ok["B7"]
        for m in ["4thpow", "Kay", "PSA"]:
            ratio = b7_ok / ok[m] if ok[m] > 0 else float('inf')
            print(f"  B7/{m} 范围比 = {ratio:.2f}x")

    out = {"meta": {"n_sym": N_SYM, "n_seed": N_SEED, "f_d_grid_GHz": F_D_GRID_GHZ,
                     "osnr_dB": OSNR_DB, "elapsed_s": round(time.time()-t0, 1)},
           "results": results}
    out_path = os.path.join(os.path.dirname(__file__), "_scope_fairness_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[wrote] {out_path} (elapsed {out['meta']['elapsed_s']}s)")

if __name__ == "__main__":
    main()
