"""③ MCS 排程增益上界 — 前置门控 MVE
目标: 仰角感知分段 MCS vs 全程最优固定 MCS, 算理论增益上界。

纯解析, 不仿真解码。用 Shannon 容量 outage 平均作上界 proxy。
复用 _channel.py:gg_block 的 GG 信道模型思想, 但这里直接用 scipy.stats 解析分布。

上界条件 (oracle): 完美 CSI + 零开销切换 + 精确仰角-统计映射。
判据: 上界 <0.5dB -> ③ 砍掉 (重演 N1 教训)。
"""
import json
import math
import os
import time
import hashlib
import subprocess
from scipy.stats import gamma as gamma_dist
import numpy as np

# ============================================================
# 1. GG 信道: 瞬时 SNR = gamma_bar * h, h ~ GG(a, b)
# ============================================================

def gg_pdf_inv_moment(a, b, k=1):
    """E[h^(-k)] for h ~ GG(a,b), 用于 outage 解析。
    GG pdf: f(h) = 2(ab)^(ab) / Gamma(a)Gamma(b) * h^((ab-1)/2) K_{a-b}(2 sqrt(ab h))
    E[h^(-1)] = ab / (a-1)(b-1) for a,b > 1 (标准结果)
    """
    if a <= 1 or b <= 1:
        return float('inf')
    return a * b / ((a - 1) * (b - 1))


def gg_sample(gamma_bar, a, b, N, bs=100, seed=42):
    """采样 N 个 GG 块衰落系数 h (块内相关 bs)。
    复用 _channel.py:gg_block 的思想。瞬时 SNR = gamma_bar * h。
    """
    np.random.seed(seed)
    nb = (N + bs - 1) // bs
    h = gamma_dist.rvs(a, scale=1/a, size=nb) * gamma_dist.rvs(b, scale=1/b, size=nb)
    return np.repeat(h, bs)[:N]


# ============================================================
# 2. Rytov -> GG 映射 (标准解析)
# ============================================================

def rytov_to_gg(sigma2_R):
    """Rytov 方差 sigma2_R -> GG 参数 (a, b)。
    平面波, 中-强起伏, 标准点对点近似 (Kaushal & Kaddoum 文献体系)。
    弱起伏 sigma2_R<0.3: a,b 大 (趋近无衰落)
    强起伏 sigma2_R>1: a,b 小 (~1-3)
    饱和 sigma2_R>5: a,b 极小 (<1, outage 主导)

    用经验拟合 (Trinh et al. / Khalighi 体系):
    a = exp(A1 + A2*log(sig2) + A3*log(sig2)^2) 的简化版
    这里用 Piecewise 近似:
      sig2 < 1: a,b = 10/sqrt(sig2), 给出温和参数
      1 <= sig2 < 5: a,b = 4/sqrt(sig2)
      sig2 >= 5: a,b = 2/sqrt(sig2) (饱和区, 最差)
    并 a >= 1.2, b >= 1.2 (避免 GG 力矩发散太远)
    """
    s = math.sqrt(sigma2_R)
    if sigma2_R < 1:
        a = b = max(10.0 / s, 1.2)
    elif sigma2_R < 5:
        a = b = max(4.0 / s, 1.2)
    else:
        a = b = max(2.0 / s, 1.05)
    return a, b


# ============================================================
# 3. 仰角 -> sigma2_R
# ============================================================

def elev_to_rytov(elev_deg, sigma2_R_zenith):
    """仰角(度) -> Rytov 方差。平面波 sec(zeta)^(11/6) 模型。"""
    zeta = math.radians(90 - elev_deg)
    sec = 1.0 / math.cos(zeta)
    return sigma2_R_zenith * sec ** (11.0 / 6.0)


# ============================================================
# 4. Shannon outage 容量 (上界 proxy)
# ============================================================

def avg_rate_at_mcs(gamma_bar, a, b, rate_bpsym, snr_threshold_db, N=200000, seed=42):
    """在给定 GG 信道下, 用 MCS(rate_bpsym, snr_threshold_db) 的过境平均可达速率。
    snr_threshold_db = 该 MCS 成功解码所需最低瞬时 SNR。
    可达速率 = rate_bpsym * P(instant SNR > threshold) ( outage 模型).

    用 Monte Carlo 采样 GG 信道算 P(SNR>thr), 避免 E[h^-1] 在 a<=1 时发散。
    """
    h = gg_sample(gamma_bar, a, b, N, seed=seed)
    inst_snr_db = 10 * np.log10(gamma_bar * h + 1e-12)
    p_success = np.mean(inst_snr_db >= snr_threshold_db)
    return rate_bpsym * p_success, p_success


# DVB-S2 标准 MCS 集 (rate_bpsym, snr_threshold_db at BER=1e-5)
# 简化集: 覆盖低阶到高阶, 反映实际链路 MCS 分级
MCS_SET = [
    # (name, rate_bpsym, snr_threshold_db)
    ('QPSK-1/4',   0.5,  -2.0),   # 最鲁棒
    ('QPSK-1/2',   1.0,   1.0),
    ('QPSK-3/4',   1.5,   3.5),
    ('8PSK-3/4',   2.25,  6.5),
    ('16APSK-3/4', 3.0,   9.0),
    ('16APSK-5/6', 3.33, 11.0),
    ('32APSK-3/4', 3.75, 13.0),
    ('32APSK-9/10',4.5,  15.5),
]


# ============================================================
# 5. 主分析
# ============================================================

def best_fixed_mcs_for_pass(elev_seq, sigma2_R_zenith, gamma_bar, N=200000):
    """方案 A: 全程最优固定 MCS。
    对每个 MCS, 算它在过境所有段的加权平均可达速率。
    baseline = max over MCS.
    """
    seg_weights = np.ones(len(elev_seq)) / len(elev_seq)  # 等权重段
    best_rate = -1
    best_mcs = None
    per_mcs = {}
    for name, rate, thr in MCS_SET:
        total_rate = 0.0
        for elev, w in zip(elev_seq, seg_weights):
            sig2 = elev_to_rytov(elev, sigma2_R_zenith)
            a, b = rytov_to_gg(sig2)
            r, _ = avg_rate_at_mcs(gamma_bar, a, b, rate, thr, N=N)
            total_rate += w * r
        per_mcs[name] = total_rate
        if total_rate > best_rate:
            best_rate = total_rate
            best_mcs = name
    return best_mcs, best_rate, per_mcs


def elevation_aware_mcs(elev_seq, sigma2_R_zenith, gamma_bar, N=200000):
    """方案 B: 仰角感知分段 MCS (oracle 上界)。
    每段独立选最优 MCS, 加权平均。
    """
    seg_weights = np.ones(len(elev_seq)) / len(elev_seq)
    total_rate = 0.0
    chosen = []
    for elev, w in zip(elev_seq, seg_weights):
        sig2 = elev_to_rytov(elev, sigma2_R_zenith)
        a, b = rytov_to_gg(sig2)
        best_r = -1
        best_name = None
        for name, rate, thr in MCS_SET:
            r, _ = avg_rate_at_mcs(gamma_bar, a, b, rate, thr, N=N)
            if r > best_r:
                best_r = r
                best_name = name
        total_rate += w * best_r
        chosen.append((elev, best_name, best_r))
    return total_rate, chosen


def main():
    t0 = time.time()
    # 过境仰角序列: 10 -> 90 -> 10, 19 个采样点 (对称)
    elev_seq = list(range(10, 91, 5)) + list(range(85, 9, -5))

    results = {'meta': {}, 'cases': []}

    for sigma2_R_zen in [0.1, 0.5, 1.0]:
        for gamma_bar_db in [5, 10, 15, 20]:
            gamma_bar = 10 ** (gamma_bar_db / 10)
            # 方案 A
            fix_name, fix_rate, per_mcs = best_fixed_mcs_for_pass(
                elev_seq, sigma2_R_zen, gamma_bar)
            # 方案 B
            ela_rate, chosen = elevation_aware_mcs(
                elev_seq, sigma2_R_zen, gamma_bar)

            # 增益
            gain_lin = ela_rate / fix_rate if fix_rate > 1e-9 else float('inf')
            gain_db = 10 * math.log10(gain_lin) if gain_lin > 0 else -float('inf')
            gain_rel = (ela_rate - fix_rate) / fix_rate if fix_rate > 1e-9 else float('inf')

            case = {
                'sigma2_R_zenith': sigma2_R_zen,
                'gamma_bar_db': gamma_bar_db,
                'fixed_best_mcs': fix_name,
                'fixed_rate': round(fix_rate, 4),
                'elevation_aware_rate': round(ela_rate, 4),
                'gain_db': round(gain_db, 3),
                'gain_rel_pct': round(100 * gain_rel, 2),
                'elevation_aware_choices': [(e, n) for e, n, _ in chosen],
            }
            results['cases'].append(case)

            print('sig2_zen=%.1f gamma=%2ddB | fixed=%s r=%.3f | elev-aware r=%.3f | gain=%.2fdB (%.1f%%)' % (
                sigma2_R_zen, gamma_bar_db, fix_name, fix_rate, ela_rate, gain_db, 100*gain_rel))

    # git hash
    try:
        git_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=os.getcwd()).decode().strip()[:7]
    except Exception:
        git_hash = 'unknown'

    results['meta'] = {
        'git_hash': git_hash,
        'seed': 42,
        'N_samples': 200000,
        'MCS_set': [m[0] for m in MCS_SET],
        'elev_seq': elev_seq,
        'runtime_s': round(time.time() - t0, 1),
        'method': 'shannon_outage_avg_rate_proxy',
        'oracle': True,
        'note': 'Upper bound: perfect CSI + zero switching cost + exact elev-stat mapping',
    }

    out_path = os.path.join(os.path.dirname(__file__), 'mcs_gain_upperbound_results.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('\nWrote', out_path)
    print('Runtime: %.1fs' % results['meta']['runtime_s'])

    # 判据汇总
    gains = [c['gain_db'] for c in results['cases']]
    print('\n=== JUDGE ===')
    print('Max gain across all cases: %.2f dB' % max(gains))
    print('Mean gain: %.2f dB' % (sum(gains)/len(gains)))
    print('Min gain: %.2f dB' % min(gains))
    n_above_1 = sum(1 for g in gains if g >= 1.0)
    n_05_1 = sum(1 for g in gains if 0.5 <= g < 1.0)
    n_below_05 = sum(1 for g in gains if g < 0.5)
    print('Cases >=1.0dB: %d/%d | 0.5-1.0dB: %d | <0.5dB: %d' % (
        n_above_1, len(gains), n_05_1, n_below_05))
    if max(gains) >= 1.0:
        print('VERDICT: ③ 进 GW (至少一个场景增益 >1dB)')
    elif max(gains) >= 0.5:
        print('VERDICT: ③ 边缘, 需更细 MVE')
    else:
        print('VERDICT: ③ 砍掉 (重演 N1, 上界 <0.5dB)')


if __name__ == '__main__':
    main()
