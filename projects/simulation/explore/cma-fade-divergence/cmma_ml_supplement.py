"""G3 ML 补充: 为 cmma_ber_vs_fg_results.json 补 ML BER (单独跑, 避免重跑 CMA/CMMA).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-12
> 来源: R004 批次2 任务2 G3 补充 (CMMA/CMA/oracle 已在 cmma_ber_vs_fg.py 完成)

## 背景

cmma_ber_vs_fg.py 的 --no-ml 模式已跑完 CMMA/CMA/oracle (20 seeds, 双调制).
ML 训练慢 (每次 ~24s), 单独跑补充. 用相同确定性 seed (make_seed) 保证四
方同信道.

## 用法
  cd projects/simulation && python explore/cma-fade-divergence/cmma_ml_supplement.py
"""
import sys
import json
import time
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from params import SimulationConfig
from common._ml_equalizer import MLChannelEqualizer
from cmma_ber_vs_fg import (
    gen_channel, compute_ber, make_seed, ML_PARAMS, ML_TRAIN_FRAC,
    N_SYMBOLS, GAMMA_BAR, SOP_RATE, F_G_SWEEP, MOD_LIST, TURB,
    RESULTS_DIR,
)

cfg = SimulationConfig()
N_SEEDS_ML = 3  # ML 慢, 用 3 seeds

RESULTS_JSON = RESULTS_DIR / 'cmma_ber_vs_fg_results.json'
ML_CKPT = RESULTS_DIR / 'cmma_ml_supplement_checkpoint.json'


def _load_ckpt():
    if ML_CKPT.exists():
        try:
            with open(ML_CKPT, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {'results': {}}
    return {'results': {}}


def _save_ckpt(data):
    try:
        ML_CKPT.parent.mkdir(parents=True, exist_ok=True)
        with open(ML_CKPT, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, default=str)
    except Exception:
        pass


def run_ml_for_mod(mod, alpha, beta):
    """为指定调制跑 ML BER (N_SEEDS_ML × F_G_SWEEP)."""
    n_train = int(N_SYMBOLS * ML_TRAIN_FRAC)
    ckpt = _load_ckpt()
    results = ckpt.get('results', {}).get(mod, {})

    done = sum(1 for f_g in F_G_SWEEP
               if str(f_g) in results
               and len(results[str(f_g)]) >= N_SEEDS_ML)
    print(f"  [{mod}] ML 续跑: {done}/{len(F_G_SWEEP)} f_G 完成")
    print(f"  {'f_G(Hz)':>8} | {'ML_BER':>10} {'t(s)':>6}")

    t_mod0 = time.time()
    for f_g in F_G_SWEEP:
        key = str(f_g)
        if key in results and len(results[key]) >= N_SEEDS_ML:
            ml_m = np.mean(results[key][:N_SEEDS_ML])
            print(f"  {f_g:>8.0f} | {ml_m:>10.2e} {'-':>6} (cached)", flush=True)
            continue
        results[key] = results.get(key, [])
        t_fg = time.time()
        for seed_idx in range(len(results[key]), N_SEEDS_ML):
            seed_int = make_seed(mod, f_g, seed_idx)
            rX, rY, sX, sY, h, theta = gen_channel(
                mod, N_SYMBOLS, alpha, beta, f_g, SOP_RATE, GAMMA_BAR, seed_int)
            ml = MLChannelEqualizer(**ML_PARAMS)
            ml.train(rX[:n_train], rY[:n_train], sX[:n_train], sY[:n_train],
                     val_split=0.2, verbose=False)
            res_ml = ml.equalize(rX, rY)
            zX_ml = res_ml['zX'].flatten()
            ml_ber = compute_ber(mod, zX_ml[n_train:], sX[n_train:], 0.0)
            results[key].append(float(ml_ber))
        ml_m = np.mean(results[key][:N_SEEDS_ML])
        dt = time.time() - t_fg
        print(f"  {f_g:>8.0f} | {ml_m:>10.2e} {dt:>6.0f}", flush=True)
        # 写 ckpt
        full = _load_ckpt()
        full.setdefault('results', {})[mod] = results
        _save_ckpt(full)

    print(f"  [{mod}] ML 总耗时: {time.time()-t_mod0:.0f}s")
    return {k: v[:N_SEEDS_ML] for k, v in results.items()
            if len(v) >= N_SEEDS_ML}


def main():
    t0 = time.time()
    alpha, beta = cfg.turbulence.as_dict()[TURB]
    print("=" * 70)
    print(f"G3 ML 补充: N_SEEDS_ML={N_SEEDS_ML}, mods={MOD_LIST}")
    print("=" * 70)

    ml_results = {}
    for mod in MOD_LIST:
        print(f"\n--- {mod} ML ---")
        ml_results[mod] = run_ml_for_mod(mod, alpha, beta)

    # 合并进主 results JSON
    with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
        main_data = json.load(f)

    for mod in MOD_LIST:
        for fg_str, ml_list in ml_results[mod].items():
            if fg_str in main_data['results'].get(mod, {}):
                v = main_data['results'][mod][fg_str]
                v['ml_ber_mean'] = float(np.mean(ml_list))
                v['ml_ber_std'] = float(np.std(ml_list))
                v['ml_ber_list'] = [float(x) for x in ml_list]
                v['n_seeds_ml'] = len(ml_list)
    # 更新 meta
    main_data['meta']['params']['n_seeds_ml'] = N_SEEDS_ML
    main_data['meta']['ml_supplement_elapsed_s'] = time.time() - t0

    with open(RESULTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(main_data, f, indent=2, ensure_ascii=False)
    print(f"\n合并完成, 保存到: {RESULTS_JSON}")

    # 清 ckpt
    try:
        ML_CKPT.unlink()
    except Exception:
        pass

    print(f"ML 补充总耗时: {time.time()-t0:.0f}s")
    return main_data


if __name__ == '__main__':
    main()
