"""F2: 发散概率可视化数据整理 — 从 cma_divergence_scan_results.json 提取 P_div 热图/曲线格式.

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 组织规范: ../../SIM-ORG.md (P1 结果进 results/; P5 标方向+状态)
> 来源: R004 批次1 F2 (主控做, 分析层核心产出的可视化数据)

做什么:
  从 Step B 的 cma_divergence_scan_results.json (128 trials, 4 turb × 4 f_G × 4 μ × 2 tap)
  提取 P_div, 整理成可直接画图的三种格式:
    1. heatmap: P_div 矩阵 (μ 行 × f_G 列), 按 tap/turb 分组或聚合
    2. curve: P_div vs μ 曲线 (每 f_G 一条), 用于线图
    3. by_turb: 按 4 个湍流档分组的 P_div 汇总

不重新跑实验, 只整理已有数据 (主控任务, 不需 GPU).

用法:
  cd projects/simulation && python explore/cma-fade-divergence/divergence_viz_data.py
"""
import sys
import json
from pathlib import Path
from collections import defaultdict

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
SRC = RESULTS_DIR / 'cma_divergence_scan_results.json'
OUT = RESULTS_DIR / 'divergence_viz_data.json'


def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        d = json.load(f)

    records = d['results']
    f_g_vals = sorted(set(r['f_g_hz'] for r in records))
    mu_vals = sorted(set(r['mu'] for r in records))
    turb_vals = sorted(set(r['turb_name'] for r in records))
    tap_vals = sorted(set(r['n_tap'] for r in records))

    print(f"源数据: {len(records)} trials")
    print(f"  f_G: {f_g_vals} Hz, μ: {mu_vals}, turb: {turb_vals}, tap: {tap_vals}")

    # ─── 1. heatmap: P_div 矩阵 (μ × f_G), 聚合所有 turb + tap ───
    # 每个 (mu, f_g) 把 4 turb × 2 tap = 8 个记录的 p_div 平均
    heatmap_agg = defaultdict(list)
    for r in records:
        heatmap_agg[(r['mu'], r['f_g_hz'])].append(r['p_div'])
    heatmap = {
        'mu_values': mu_vals,
        'f_g_values': f_g_vals,
        'matrix': [[round(float(sum(heatmap_agg[(mu, fg)]) / len(heatmap_agg[(mu, fg)])), 3)
                    for fg in f_g_vals] for mu in mu_vals],
        'description': 'P_div 聚合 (4 turb × 2 tap 平均), 行=μ, 列=f_G',
    }

    # ─── 2. curve: P_div vs μ, 每 f_G 一条 (聚合 turb+tap) ───
    curves = []
    for fg in f_g_vals:
        mu_pdiv = []
        for mu in mu_vals:
            vals = [r['p_div'] for r in records
                    if r['f_g_hz'] == fg and r['mu'] == mu]
            mu_pdiv.append(round(float(sum(vals) / len(vals)), 3) if vals else None)
        curves.append({'f_g_hz': fg, 'mu_values': mu_vals, 'p_div_values': mu_pdiv})

    # ─── 3. by_turb: 按湍流档分组, 每 turb 一个 (μ × f_G) 矩阵 (tap 平均) ───
    by_turb = {}
    for turb in turb_vals:
        sub = [r for r in records if r['turb_name'] == turb]
        mat = defaultdict(list)
        for r in sub:
            mat[(r['mu'], r['f_g_hz'])].append(r['p_div'])
        by_turb[turb] = {
            'mu_values': mu_vals,
            'f_g_values': f_g_vals,
            'matrix': [[round(float(sum(mat[(mu, fg)]) / len(mat[(mu, fg)])), 3)
                        for fg in f_g_vals] for mu in mu_vals],
            'n_records': len(sub),
        }

    # ─── 4. 安全/临界/危险区汇总 (来自 README 发散条件判据) ───
    zones = {
        'safe': {'criterion': 'μ ≤ 1e-3, 任意 turb/f_G/tap → P_div ≈ 0',
                 'examples': []},
        'critical': {'criterion': 'μ ≈ 5e-3, 取决于 f_G 和 tap',
                     'examples': []},
        'danger': {'criterion': 'μ ≥ 1e-2 且 f_G ≥ 100 Hz → P_div ≥ 0.67',
                   'examples': []},
    }
    for r in records:
        entry = {'turb': r['turb_name'], 'f_g': r['f_g_hz'], 'mu': r['mu'],
                 'tap': r['n_tap'], 'p_div': r['p_div']}
        if r['mu'] <= 1e-3 and r['p_div'] < 0.1:
            zones['safe']['examples'].append(entry)
        elif r['mu'] >= 1e-2 and r['f_g_hz'] >= 100 and r['p_div'] >= 0.67:
            zones['danger']['examples'].append(entry)
        elif 5e-4 < r['mu'] < 1e-2:
            zones['critical']['examples'].append(entry)
    zones['safe']['count'] = len(zones['safe']['examples'])
    zones['critical']['count'] = len(zones['critical']['examples'])
    zones['danger']['count'] = len(zones['danger']['examples'])

    out = {
        'meta': {
            'direction': 'Q-CMA-FADE',
            'step': 'F2 divergence viz data (R004 batch1, 主控任务)',
            'source_file': 'cma_divergence_scan_results.json',
            'n_trials': len(records),
            'sweep_dims': d.get('scan_dims', {}),
        },
        'heatmap': heatmap,
        'curves': curves,
        'by_turbulence': by_turb,
        'zones': zones,
    }

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n可视化数据已保存: {OUT}")

    # 打印预览
    print("\n=== Heatmap (P_div, μ × f_G, 聚合 turb+tap) ===")
    mu_fg_label = 'μ \\ f_G'
    print(f"{mu_fg_label:>10}", end='')
    for fg in f_g_vals:
        print(f"{int(fg):>8}", end='')
    print()
    for i, mu in enumerate(mu_vals):
        print(f"{mu:>10.0e}", end='')
        for j in range(len(f_g_vals)):
            print(f"{heatmap['matrix'][i][j]:>8.2f}", end='')
        print()

    print("\n=== 发散条件判据计数 ===")
    for z in ['safe', 'critical', 'danger']:
        print(f"  {z}: {zones[z]['count']} 组合 — {zones[z]['criterion']}")


if __name__ == '__main__':
    main()
