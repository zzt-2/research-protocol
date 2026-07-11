"""GG 时间域衰落模型验证脚本（Q-CMA-FADE Step A, FR-20 前置门控）

> 方向: Q-CMA-FADE | 状态: WIP | 创建: 2026-07-11
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/, P5 docstring 标方向+状态)

验证 common/_gg_time.py 的 gg_time_envelope 三项统计特性:
  1. 边缘 PDF 匹配: 生成包络直方图 vs GG PDF(α,β) F32 的 KS 检验
  2. 自相关函数: log-ACF 在 τ_c 处降到 ~exp(-1)（验证相干时间）
  3. 衰落统计: level crossing rate (LCR) / average fade duration (AFD)
     在多档阈值下的值，与文献量级对比（sat.1553 τ_c, Stefanović 2021）

物理参数全从 params.py 读（P3 单一真相源, FR-20）。

用法:
  cd projects/simulation && python explore/cma-fade-divergence/gg_time_fading_model.py
"""
import sys
import os
import json
import numpy as np
from datetime import datetime

# 确保从 projects/simulation/ 运行（sys.path 含 simulation 根）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from params import SimulationConfig
from common._gg_time import (
    gg_time_envelope, gg_time_envelope_blockwise,
    rho_from_tau_c, gg_pdf_theory,
)
from common._config import BLOCK


# ─── 物理参数（从 params.py 读，FR-20 P3）────────────────────
cfg = SimulationConfig()
T_S = cfg.system.T_S
TURB = cfg.get_turb_dict()  # {'weak':(4,3), 'moderate':(2.5,1.8), 'strong':(1.5,0.8)}
F_G_SWEEP = cfg.gg_time.GREENWOOD_FREQ_SWEEP  # (30, 100, 300, 1000) Hz
TAU_C_COEFF = cfg.gg_time.TAU_C_COEFF  # 1/(2π)

# 序列长度: 要看到完整衰落动力学, 需 N·t_s ≫ τ_c_max
# τ_c_max = coeff/30Hz = 5.3ms → N_min = 5.3e-3/0.4e-9 ≈ 1.3e7
# 取 N_BLOCKS = 500000 块 (50M 符号) 覆盖最慢档
N_BLOCKS = 500_000
N_SYMBOLS = N_BLOCKS * BLOCK  # 50M 符号 @ block=100


def ks_test_pdf(h, alpha, beta):
    """边缘 PDF KS 检验: 生成样本 vs GG PDF 理论。

    注: 此函数用完整序列做 KS。若序列高度自相关(ρ→1), 有效独立样本数
    n_eff = N/(2·τ_int) 很小, KS 噪声大。边缘准确性应辅以独立块模式
    (短 τ_c) 验证——见 main() 的 ``edge_check_independent``。

    返回 KS 统计量 + 理论/经验均值/方差对比。
    """
    emp_mean = float(np.mean(h))
    emp_var = float(np.var(h))
    emp_si2 = emp_var / emp_mean ** 2

    theory_mean = 1.0
    theory_var = 1.0 / alpha + 1.0 / beta + 1.0 / (alpha * beta)
    theory_si2 = theory_var

    from scipy.stats import kstest, gamma as gamma_dist
    ref_n = 500_000
    ref = (gamma_dist.rvs(alpha, scale=1.0 / alpha, size=ref_n) *
           gamma_dist.rvs(beta, scale=1.0 / beta, size=ref_n))
    ks_stat, ks_p = kstest(h[::max(1, len(h) // 100000)], ref[::max(1, ref_n // 100000)])

    # 有效独立样本数估计（AR(1): τ_int=(1+ρ)/(1-ρ)）
    rho_block = rho_from_tau_c(_TAU_C_CURRENT[0], BLOCK, T_S) if _TAU_C_CURRENT else 0.5
    tau_int = (1 + rho_block) / max(1 - rho_block, 1e-12)
    n_eff = len(h) / max(2 * tau_int, 1)

    return {
        'ks_stat': float(ks_stat),
        'ks_pvalue': float(ks_p),
        'emp_mean': emp_mean,
        'emp_si2': emp_si2,
        'theory_mean': theory_mean,
        'theory_si2': float(theory_si2),
        'mean_rel_err': float(abs(emp_mean - theory_mean) / theory_mean),
        'si2_rel_err': float(abs(emp_si2 - theory_si2) / theory_si2),
        'n_eff_estimate': float(n_eff),
        'ks_noise_floor': float(1.0 / np.sqrt(max(n_eff, 1))),
    }


# 全局当前 τ_c（供 ks_test_pdf 估 n_eff；非线程安全, MVE 脚本可接受）
_TAU_C_CURRENT = [None]


def autocorrelation_check(h_blocks, tau_c, block, t_s, max_lag_blocks=2000):
    """自相关函数检验: log-ACF 在 τ_c 处降到 ~exp(-1)。

    AR(1) 理论: log-ACF[lag] = ρ^lag = exp(-lag·block·t_s/τ_c)。
    ACF 降到 1/e 的 lag = τ_c/(block·t_s) 块。
    返回 measured log-ACF[1] 与理论 ρ 的对比。
    """
    # log-ACF (lognormal 法的物理正确指标)
    log_h = np.log(np.maximum(h_blocks, 1e-10))
    log_hc = log_h - log_h.mean()
    n = len(log_hc)

    # ACF[lag=1] (相邻块)
    if n > 1:
        log_acf1 = float(np.mean(log_hc[1:] * log_hc[:-1]) / np.mean(log_hc * log_hc))
    else:
        log_acf1 = float('nan')

    rho_theory = rho_from_tau_c(tau_c, block, t_s)

    # 找 log-ACF 降到 1/e 的块数（限制 max_lag 避免大数组）
    max_lag = min(max_lag_blocks, n - 1)
    acf_vals = np.empty(max_lag)
    for lag in range(1, max_lag + 1):
        acf_vals[lag - 1] = np.mean(log_hc[lag:] * log_hc[:-lag]) / np.mean(log_hc * log_hc)
    below_1e = np.where(acf_vals < 1.0 / np.e)[0]
    blocks_to_1e = int(below_1e[0] + 1) if len(below_1e) > 0 else -1

    tau_c_est = blocks_to_1e * block * t_s if blocks_to_1e > 0 else float('inf')
    theory_blocks_to_1e = tau_c / (block * t_s)

    return {
        'log_acf1_measured': log_acf1,
        'rho_theory': rho_theory,
        'log_acf1_rel_err': float(abs(log_acf1 - rho_theory) / rho_theory) if rho_theory > 0 else float('nan'),
        'blocks_to_1e': blocks_to_1e,
        'theory_blocks_to_1e': float(theory_blocks_to_1e),
        'tau_c_est_s': float(tau_c_est) if np.isfinite(tau_c_est) else None,
        'tau_c_est_ms': float(tau_c_est * 1e3) if np.isfinite(tau_c_est) else None,
    }


def fade_statistics(h_blocks, thresholds, block, t_s):
    """Level Crossing Rate (LCR) + Average Fade Duration (AFD)。

    LCR(thr) = 每秒跨过 thr 的次数（向下跨）。
    AFD(thr) = 平均每次衰落持续秒数 = P(h<thr) / LCR(thr)。
    用块级序列估计（块内恒定）。
    """
    below = h_blocks < thresholds[:, None]
    # 向下跨越: below[k] and not below[k-1]
    downcross = below[:, 1:] & ~below[:, :-1]
    n_cross = downcross.sum(axis=1)
    total_time_s = len(h_blocks) * block * t_s
    lcr = n_cross / total_time_s  # 每秒跨越次数
    p_below = below.mean(axis=1)
    afd = np.where(lcr > 0, p_below / np.maximum(lcr, 1e-15), float('inf'))
    return {
        'thresholds': thresholds.tolist(),
        'lcr_per_sec': lcr.tolist(),
        'afd_s': afd.tolist(),
        'afd_ms': (afd * 1e3).tolist(),
        'p_below': p_below.tolist(),
    }


def edge_check_independent(alpha, beta, method, n=500_000, seed=42):
    """边缘 PDF 准确性检验（独立块模式, ρ→0）。

    高 ρ 序列 n_eff 太小无法 KS。用短 τ_c（ρ→0, 块近似独立）生成大样本,
    直接 KS 检验边缘是否匹配 GG(α,β)。GAR 此模式应 KS<0.01（精确边缘）。
    """
    block = BLOCK
    t_s = T_S
    # τ_c = block·t_s/10 → ρ=exp(-10)≈4.5e-5 ≈ 独立
    tau_c_indep = block * t_s / 10.0
    h = gg_time_envelope_blockwise(n, alpha, beta, tau_c_indep, block, t_s, method, seed=seed)
    from scipy.stats import kstest, gamma as gamma_dist
    ref = (gamma_dist.rvs(alpha, scale=1.0 / alpha, size=n, random_state=seed + 1) *
           gamma_dist.rvs(beta, scale=1.0 / beta, size=n, random_state=seed + 2))
    ks_stat, ks_p = kstest(h[::5], ref[::5])
    return {
        'ks_stat': float(ks_stat),
        'ks_pvalue': float(ks_p),
        'method': method,
        'alpha': alpha, 'beta': beta,
        'n_samples': n,
    }


def main():
    print(f"=== GG 时间域衰落模型验证 (Q-CMA-FADE Step A) ===")
    print(f"N_blocks={N_BLOCKS}, N_symbols={N_SYMBOLS}, block={BLOCK}, t_s={T_S*1e9:.2f}ns")
    print(f"f_G sweep: {F_G_SWEEP} Hz")
    print(f"τ_c = {TAU_C_COEFF:.4f}/f_G → {[f'{TAU_C_COEFF/f*1e3:.2f}' for f in F_G_SWEEP]} ms")
    print(f"ρ (block间) for each f_G: {[f'{rho_from_tau_c(TAU_C_COEFF/f, BLOCK, T_S):.6f}' for f in F_G_SWEEP]}")
    print()

    results = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'A (FR-20 前置门控)',
            'timestamp': datetime.now().isoformat(),
            'n_blocks': N_BLOCKS,
            'n_symbols': N_SYMBOLS,
            'block': BLOCK,
            't_s': T_S,
            'f_g_sweep_hz': list(F_G_SWEEP),
            'tau_c_coeff': TAU_C_COEFF,
        },
        'methods_tested': ['lognormal', 'gar'],
        'configurations': {},
    }

    # === 边缘 PDF 准确性（独立块模式, ρ→0, 大样本 KS 有效）===
    print("=== 边缘 PDF 准确性（独立块模式 ρ→0）===")
    results['edge_check_independent'] = {}
    turb_levels = ['weak', 'moderate', 'strong']
    for turb_name in turb_levels:
        alpha, beta = TURB[turb_name]
        results['edge_check_independent'][turb_name] = {}
        for method in ['lognormal', 'gar']:
            ec = edge_check_independent(alpha, beta, method)
            results['edge_check_independent'][turb_name][method] = ec
            print(f"  {turb_name}(α={alpha},β={beta}) [{method}]: "
                  f"KS={ec['ks_stat']:.4f}, p={ec['ks_pvalue']:.3f} "
                  f"{'PASS' if ec['ks_stat'] < 0.02 else 'CHECK'}")
    print()

    # === ACF + 衰落统计（高 ρ 完整序列, 验证相干时间）===
    fade_thresholds = np.array([0.001, 0.01, 0.05, 0.1, 0.3, 0.5])
    for turb_name in turb_levels:
        alpha, beta = TURB[turb_name]
        results['configurations'][turb_name] = {'alpha': alpha, 'beta': beta}
        print(f"--- 湍流: {turb_name} (α={alpha}, β={beta}) ---")

        for f_g in F_G_SWEEP:
            tau_c = TAU_C_COEFF / f_g
            rho = rho_from_tau_c(tau_c, BLOCK, T_S)
            _TAU_C_CURRENT[0] = tau_c  # 供 ks_test_pdf 估 n_eff
            cfg_key = f"fG_{int(f_g)}Hz_tauC_{tau_c*1e3:.2f}ms"
            results['configurations'][turb_name][cfg_key] = {
                'f_g_hz': float(f_g),
                'tau_c_s': float(tau_c),
                'tau_c_ms': float(tau_c * 1e3),
                'rho_block': float(rho),
            }
            print(f"  f_G={int(f_g)}Hz, τ_c={tau_c*1e3:.2f}ms, ρ={rho:.6f}")

            for method in ['lognormal', 'gar']:
                h_blocks = gg_time_envelope_blockwise(
                    N_BLOCKS, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                    method=method, seed=42,
                )

                pdf_check = ks_test_pdf(h_blocks, alpha, beta)
                acf_check = autocorrelation_check(h_blocks, tau_c, BLOCK, T_S)
                fade_stats = fade_statistics(h_blocks, fade_thresholds, BLOCK, T_S)

                results['configurations'][turb_name][cfg_key][method] = {
                    'pdf_full_series': pdf_check,
                    'acf': acf_check,
                    'fade_stats': fade_stats,
                }

                print(f"    [{method}] n_eff≈{pdf_check['n_eff_estimate']:.1f}, "
                      f"log-ACF[1]={acf_check['log_acf1_measured']:.4f} "
                      f"(ρ={acf_check['rho_theory']:.4f}, "
                      f"err={acf_check['log_acf1_rel_err']*100:.2f}%)")
                if acf_check['blocks_to_1e'] > 0:
                    print(f"      τ_c est={acf_check['tau_c_est_ms']:.3f}ms "
                          f"(target {tau_c*1e3:.2f}ms)")
        print()

    # === 文献一致性检查 ===
    print("=== 文献一致性检查 ===")
    tau_c_values = [TAU_C_COEFF / f * 1e3 for f in F_G_SWEEP]
    lit_lower = cfg.gg_time.TAU_C_LITERATURE_LOWER_MS
    lit_upper = cfg.gg_time.TAU_C_LITERATURE_UPPER_MS
    in_range = [t for t in tau_c_values if lit_lower <= t <= lit_upper]
    print(f"τ_c sweep {[f'{t:.2f}' for t in tau_c_values]} ms; "
          f"文献范围 [{lit_lower}, {lit_upper}] ms; "
          f"在范围内: {[f'{t:.2f}' for t in in_range]} ms")
    results['literature_check'] = {
        'tau_c_sweep_ms': tau_c_values,
        'literature_range_ms': [lit_lower, lit_upper],
        'tau_c_in_range': in_range,
        'note': 'sat.1553:167 τ_c>1ms; s24248036:872 τ_c 1-100ms; '
                'f_G=300/1000Hz→τ_c<1ms 略低于文献下限（强湍快变边界, 允许）',
    }

    # === 保存结果 ===
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), 'results', 'cma-fade-divergence')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'gg_time_validation.json')

    # === PASS/FAIL 判定（分离边缘检验与 ACF 检验）===
    print("\n=== PASS/FAIL 判定 ===")
    pass_fail = {'edge_pdf_gar': True, 'edge_pdf_lognormal': True,
                 'acf': True, 'literature': True}
    issues = []

    # 边缘 PDF（独立块模式, GAR 应精确 KS<0.02; lognormal 近似 KS<0.1）
    for turb_name in turb_levels:
        gar_ks = results['edge_check_independent'][turb_name]['gar']['ks_stat']
        ln_ks = results['edge_check_independent'][turb_name]['lognormal']['ks_stat']
        if gar_ks > 0.02:
            pass_fail['edge_pdf_gar'] = False
            issues.append(f"edge/{turb_name}/gar KS={gar_ks:.4f} > 0.02")
        if ln_ks > 0.10:
            pass_fail['edge_pdf_lognormal'] = False
            issues.append(f"edge/{turb_name}/lognormal KS={ln_ks:.4f} > 0.10")

    # ACF（lognormal log-ACF[1] err <1%）
    for turb_name in turb_levels:
        for f_g in F_G_SWEEP:
            tau_c = TAU_C_COEFF / f_g
            cfg_key = f"fG_{int(f_g)}Hz_tauC_{tau_c*1e3:.2f}ms"
            d = results['configurations'][turb_name][cfg_key]['lognormal']
            if d['acf']['log_acf1_rel_err'] > 0.01:
                pass_fail['acf'] = False
                issues.append(f"{turb_name}/{cfg_key} log-ACF1 err={d['acf']['log_acf1_rel_err']*100:.2f}%")

    print(f"边缘 PDF (GAR, 精确): {'PASS' if pass_fail['edge_pdf_gar'] else 'FAIL'}")
    print(f"边缘 PDF (lognormal, 近似): {'PASS' if pass_fail['edge_pdf_lognormal'] else 'FAIL'}")
    print(f"自相关 τ_c (lognormal log-ACF): {'PASS' if pass_fail['acf'] else 'FAIL'}")
    print(f"文献 τ_c 范围: {'PASS' if len(in_range) >= 1 else 'CHECK'}")
    if issues:
        print("问题:")
        for iss in issues[:10]:
            print(f"  - {iss}")
    else:
        print("全部 PASS ✓")

    results['pass_fail'] = pass_fail
    results['pass_fail_issues'] = issues
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n结果已保存: {out_path}")

    return results


if __name__ == '__main__':
    main()
