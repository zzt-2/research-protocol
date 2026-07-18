"""参数域 swap 行为双控诊断扫描 (PROMPT-030).

> 方向: Q-CMA-FADE / 状态: WIP / 创建: 2026-07-15
> 来源: 主控诊断任务（摸清 swap 全貌：谁的病、什么条件下出现）

## 研究问题

S032 + 执行报告揭示的矛盾：
  - prompt012（旧域 alpha=1.5/beta=0.8, 10 seeds）: CMA 8/10 swap + 2/10 degraded
  - prompt029（新域 alpha=4.2/beta=1.4, 5 seeds）: CMA 0/5 swap 全 clean
  - 两处均: ML 100% swap（fixed_ber≈0.5）

核心矛盾：**CMA 的 swap 行为是否取决于 GG 参数域？**
  - 若是 → swap 不是 ML 独有的病，是信道（旧域更强湍流）的病，新域 CMA 恰好免疫
  - 若否 → 需查 prompt012/prompt029 的其他差异（seed 集/随机性）

## 扫描设计

双控变量：
  1. GG 参数域：{旧 1.5/0.8, 新 4.2/1.4} — 显式传入，不读 params.py
  2. 均衡器：{CMA, ML, oracle} 三者同 seed 同信道

控制变量（固定）：
  N=5M, f_G=30, SOP=4e-7, GAMMA_BAR=100 (20dB), QPSK
  late slice [4.375M, 5M)
  seeds = [1000..1009] (10 seeds，足够看 swap 分布)

扩展诊断（回答"边界在哪"）：
  - SOP_RATE 扫描 {0, 1e-8, 1e-7, 4e-7, 1e-6}（固定新域 4.2/1.4）
    → SOP 旋转速率对 CMA/ML swap 的影响
  - N 扫描 {2M, 5M, 8M}（固定新域 4.2/1.4）
    → 序列长度（SOP 累积旋转量）对 swap 的影响

## TL-20 假设（跑前写）

H_domain（主）：CMA swap 行为取决于 GG 参数域。
  预测：旧域 1.5/0.8 CMA swap_rate > 50%；新域 4.2/1.4 CMA swap_rate ≈ 0%。
  判据：两域 swap_rate 差 > 40%。
H_ml（次）：ML swap_rate 在两域均 ≈100%（SOP 泛化失败与 GG 域无关）。
H_sop（扩展）：CMA swap_rate 随 SOP_RATE 单调上升（新域）；存在临界 SOP_RATE。
  判据：CMA swap_rate 从 0% 升到 >50% 的 SOP_RATE 区间。

## 关键约束

1. 显式 alpha/beta：不从 params.py 读，两个域硬编码，避免漂移争议
2. 双口径 BER（守 D018）：fixed-label + PI 同时报，swap 分类基于 fixed
3. 同 seed 同信道：CMA/ML/oracle 共享 gen_channel 输出（公平对比）
4. swap 分类复用 prompt012 规则（main_correlation_threshold=0.5）

用法:
  cd projects/simulation && python explore/cma-fade-divergence/prompt030_domain_swap_audit.py
  (支持 checkpoint，每 seed 完成即存盘)
"""
import sys
import json
import time
import tempfile
import os
import numpy as np
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(SIM_DIR))

from params import SimulationConfig
from common._gg_time import gg_time_envelope
from common._cma import CMAEqualizer2x2
from common._ml_equalizer import MLChannelEqualizer
from common._equalizer import mmse_equalize
from common._config import BLOCK

# 复用 ml_long_seq_failure 的基建（文件夹名含连字符，用 importlib 加载）
import importlib.util as _ilu
_mlf_path = Path(__file__).resolve().parent / "ml_long_seq_failure.py"
_spec = _ilu.spec_from_file_location("ml_long_seq_failure", _mlf_path)
_mlf = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mlf)
gen_qpsk = _mlf.gen_qpsk
qpsk_demap = _mlf.qpsk_demap
compute_ber_phase_corrected = _mlf.compute_ber_phase_corrected
test_late_slice = _mlf.test_late_slice
run_ml_trial = _mlf.run_ml_trial
oracle_equalize = _mlf.oracle_equalize
ML_PARAMS = _mlf.ML_PARAMS

cfg = SimulationConfig()
GAMMA_BAR = cfg.experiment.GAMMA_BAR_DEFAULT  # 100
T_S = cfg.system.T_S

# ─── 实验参数 ──────────────────────────────────────────────
N_SYMBOLS = 5_000_000
F_G = 30.0
SOP_RATE = 4e-7
N_TAP = 11
MU_SAFE = 1e-3
R2_QPSK = 1.0
SEEDS = list(range(1000, 1010))  # 10 seeds

# 两个参数域（显式，不读 params.py）
DOMAINS = {
    "old_1p5_0p8": {"alpha": 1.5, "beta": 0.8, "label": "旧域 WARNING(无溯源)"},
    "new_4p2_1p4": {"alpha": 4.2, "beta": 1.4, "label": "新域 Gu2022(有溯源)"},
}

# 扩展扫描（固定新域）
SOP_SWEEP = [0.0, 1e-8, 1e-7, 4e-7, 1e-6]
N_SWEEP = [2_000_000, 5_000_000, 8_000_000]

RESULTS_DIR = SIM_DIR / 'results' / 'cma-fade-divergence'
OUT_PATH = RESULTS_DIR / 'prompt030_domain_swap_audit.json'
CKPT_PATH = RESULTS_DIR / 'prompt030_ckpts.json'


# ─── swap 分类（复用 prompt012 规则）──────────────────────

def classify_swap(zX, zY, sX, sY, threshold=0.5):
    """分类 swap。返回 clean/degraded/clean_swap/degraded_swap/normal。

    基于 main-correlation：zX 与 sX 相关 > threshold = 正常；与 sY 相关 > threshold = swap。
    """
    zX = np.asarray(zX).flatten()
    zY = np.asarray(zY).flatten()
    sX = np.asarray(sX).flatten()
    sY = np.asarray(sY).flatten()
    n = len(zX)
    # 归一化相关
    def corr(a, b):
        a = (a - np.mean(a))
        b = (b - np.mean(b))
        na = np.sqrt(np.sum(np.abs(a) ** 2))
        nb = np.sqrt(np.sum(np.abs(b) ** 2))
        if na < 1e-12 or nb < 1e-12:
            return 0.0
        return float(np.abs(np.vdot(a, b)) / (na * nb))
    r_XX = corr(zX, sX)  # 正常：zX 含 sX
    r_XY = corr(zX, sY)  # swap：zX 含 sY
    r_YX = corr(zY, sX)
    r_YY = corr(zY, sY)
    # 正常：XX 和 YY 高
    normal = max(r_XX, r_YY) > threshold and max(r_XX, r_YY) > max(r_XY, r_YX)
    swap = max(r_XY, r_YX) > threshold and max(r_XY, r_YX) > max(r_XX, r_YY)
    # BER 质量
    ber_normal = min(
        compute_ber_phase_corrected(zX, sX),
        compute_ber_phase_corrected(zX, sY),  # 若 swap 则取 sY
    )
    if swap and ber_normal < 0.1:
        return "clean_swap"
    elif swap:
        return "degraded_swap"
    elif normal and ber_normal < 0.1:
        return "normal"
    elif normal:
        return "degraded"
    else:
        return "mixed"


def gen_channel(N, alpha, beta, f_g, sop_rate, seed):
    """生成双偏振 GG 衰落 + SOP 旋转信道 (QPSK). 复用 ml_long_seq_failure 逻辑."""
    rng = np.random.default_rng(seed)
    tau_c = cfg.gg_time.tau_c_from_fg(f_g)
    h = gg_time_envelope(N, alpha, beta, tau_c, block=BLOCK, t_s=T_S,
                         method='gar', seed=seed)
    sX, _ = gen_qpsk(N, rng)
    sY, _ = gen_qpsk(N, rng)
    theta = sop_rate * np.arange(N)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    nv = 1.0 / (2 * GAMMA_BAR)
    rX = np.sqrt(h) * (cos_t * sX + sin_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    rY = np.sqrt(h) * (-sin_t * sX + cos_t * sY) \
        + np.sqrt(nv) * (rng.standard_normal(N) + 1j * rng.standard_normal(N))
    return rX, rY, sX, sY, h, theta


def cma_equalize(rX, rY, n_tap=N_TAP, mu=MU_SAFE, R2=R2_QPSK):
    """CMA 在线均衡（全段，模拟实际运行）. 返回 zX, zY, diverged."""
    eq = CMAEqualizer2x2(n_tap=n_tap, mu=mu, R2=R2)
    res = eq.equalize(rX, rY, block_size=64)
    return res['zX'], res['zY'], res['diverged']


def evaluate_all(rX, rY, sX, sY, h, theta, late_s, late_e):
    """CMA / ML / oracle 三者在同信道上评估，返回双口径 BER + swap 分类."""
    results = {}
    sX_l = sX[late_s:late_e]
    sY_l = sY[late_s:late_e]

    # CMA（在线，全段）
    zX_cma_full, zY_cma_full, cma_diverged = cma_equalize(rX, rY)
    if cma_diverged:
        results["cma"] = {"fixed_ber": 0.5, "pi_ber": 0.5, "classification": "diverged"}
    else:
        zX = zX_cma_full[late_s:late_e]
        zY = zY_cma_full[late_s:late_e]
        fixed = compute_ber_phase_corrected(zX, sX_l)
        swapped = compute_ber_phase_corrected(zX, sY_l)
        results["cma"] = {
            "fixed_ber": fixed,
            "pi_ber": min(fixed, swapped),
            "classification": classify_swap(zX, zY, sX_l, sY_l),
        }

    # ML（训练前 50%，推理全段）
    zX_ml_full, zY_ml_full, _n_train, _ml_res = run_ml_trial(rX, rY, sX, sY, ML_PARAMS)
    zX = zX_ml_full[late_s:late_e]
    zY = zY_ml_full[late_s:late_e]
    fixed = compute_ber_phase_corrected(zX, sX_l)
    swapped = compute_ber_phase_corrected(zX, sY_l)
    results["ml"] = {
        "fixed_ber": fixed,
        "pi_ber": min(fixed, swapped),
        "classification": classify_swap(zX, zY, sX_l, sY_l),
    }

    # oracle（完美 CSI）
    zX_or_full, zY_or_full = oracle_equalize(rX, rY, h, theta, GAMMA_BAR)
    zX = zX_or_full[late_s:late_e]
    zY = zY_or_full[late_s:late_e]
    fixed = compute_ber_phase_corrected(zX, sX_l)
    swapped = compute_ber_phase_corrected(zX, sY_l)
    results["oracle"] = {
        "fixed_ber": fixed,
        "pi_ber": min(fixed, swapped),
        "classification": classify_swap(zX, zY, sX_l, sY_l),
    }
    return results


def _save(payload):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".prompt030_", suffix=".json", dir=RESULTS_DIR)
    os.close(fd)
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=1, default=str)
        os.replace(tmp, OUT_PATH)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    payload = {
        "experiment": "PROMPT-030 参数域 swap 行为双控诊断扫描",
        "hypothesis": {
            "H_domain": "CMA swap 取决于 GG 参数域；旧域 >50% 新域 ≈0%",
            "H_ml": "ML swap 两域均 ≈100%（SOP 泛化失败与 GG 无关）",
            "H_sop": "新域 CMA swap 随 SOP_RATE 单调上升，存在临界点",
        },
        "design": {
            "domains": DOMAINS,
            "main_sweep": "域 × {CMA,ML,oracle} × 10 seeds, 固定 N=5M/SOP=4e-7",
            "sop_sweep": "新域 × SOP_RATE {0,1e-8,1e-7,4e-7,1e-6} × 10 seeds",
            "n_sweep": "新域 × N {2M,5M,8M} × 5 seeds",
            "fixed": f"N={N_SYMBOLS} f_G={F_G} SOP={SOP_RATE} GAMMA_BAR={GAMMA_BAR} late=[{int(N_SYMBOLS*0.875)},{N_SYMBOLS})",
            "seeds_main": SEEDS,
        },
        "main_audit": [],      # 域 × seed × method
        "sop_sweep_results": [],
        "n_sweep_results": [],
        "checkpoint": {"phase": "main", "completed": []},
    }
    _save(payload)

    late_s, late_e = test_late_slice(N_SYMBOLS)
    t_start = time.time()

    # ── Phase 1: 主扫描（域 × seed × method）──
    print("=" * 60)
    print("Phase 1: 域 × {CMA,ML,oracle} × 10 seeds")
    print("=" * 60)
    for dom_key, dom in DOMAINS.items():
        alpha, beta = dom["alpha"], dom["beta"]
        for seed in SEEDS:
            done = {r["seed"] for r in payload["main_audit"] if r["domain"] == dom_key}
            if seed in done:
                continue
            t0 = time.time()
            rX, rY, sX, sY, h, theta = gen_channel(N_SYMBOLS, alpha, beta, F_G, SOP_RATE, seed)
            res = evaluate_all(rX, rY, sX, sY, h, theta, late_s, late_e)
            payload["main_audit"].append({
                "domain": dom_key, "alpha": alpha, "beta": beta,
                "seed": seed, **{f"{m}_{k}": v for m, r in res.items() for k, v in r.items()},
                "elapsed_s": round(time.time() - t0, 1),
            })
            payload["checkpoint"]["completed"].append(f"{dom_key}_{seed}")
            _save(payload)
            sw_cma = res["cma"]["classification"]
            sw_ml = res["ml"]["classification"]
            print(f"  {dom_key} seed{seed}: CMA fixed={res['cma']['fixed_ber']:.2e} [{sw_cma}] | "
                  f"ML fixed={res['ml']['fixed_ber']:.2e} [{sw_ml}] | "
                  f"oracle={res['oracle']['fixed_ber']:.2e} ({time.time()-t0:.0f}s)", flush=True)

    # 主扫描汇总
    print("\nPhase 1 汇总:")
    for dom_key in DOMAINS:
        rows = [r for r in payload["main_audit"] if r["domain"] == dom_key]
        cma_swap = sum(1 for r in rows if "swap" in r["cma_classification"])
        ml_swap = sum(1 for r in rows if "swap" in r["ml_classification"])
        cma_fixed = np.mean([r["cma_fixed_ber"] for r in rows])
        ml_fixed = np.mean([r["ml_fixed_ber"] for r in rows])
        print(f"  {dom_key}: CMA swap {cma_swap}/{len(rows)} (fixed_ber={cma_fixed:.2e}) | "
              f"ML swap {ml_swap}/{len(rows)} (fixed_ber={ml_fixed:.2e})")

    # ── Phase 2: SOP_RATE 扫描（固定新域）──
    print("\n" + "=" * 60)
    print("Phase 2: 新域 × SOP_RATE 扫描")
    print("=" * 60)
    alpha, beta = DOMAINS["new_4p2_1p4"]["alpha"], DOMAINS["new_4p2_1p4"]["beta"]
    sop_seeds = SEEDS  # 10 seeds
    for sop in SOP_SWEEP:
        for seed in sop_seeds:
            rX, rY, sX, sY, h, theta = gen_channel(N_SYMBOLS, alpha, beta, F_G, sop, seed)
            res = evaluate_all(rX, rY, sX, sY, h, theta, late_s, late_e)
            payload["sop_sweep_results"].append({
                "sop_rate": sop, "seed": seed,
                **{f"{m}_{k}": v for m, r in res.items() for k, v in r.items()},
            })
        _save(payload)
        rows = [r for r in payload["sop_sweep_results"] if r["sop_rate"] == sop]
        cma_swap = sum(1 for r in rows if "swap" in r["cma_classification"])
        ml_swap = sum(1 for r in rows if "swap" in r["ml_classification"])
        print(f"  SOP={sop:.0e}: CMA swap {cma_swap}/{len(rows)} | ML swap {ml_swap}/{len(rows)}", flush=True)

    # ── Phase 3: N 扫描（固定新域）──
    print("\n" + "=" * 60)
    print("Phase 3: 新域 × N 扫描")
    print("=" * 60)
    n_seeds = list(range(1000, 1005))  # 5 seeds（N=8M 耗时长）
    for n_val in N_SWEEP:
        ls, le = test_late_slice(n_val)
        for seed in n_seeds:
            rX, rY, sX, sY, h, theta = gen_channel(n_val, alpha, beta, F_G, SOP_RATE, seed)
            res = evaluate_all(rX, rY, sX, sY, h, theta, ls, le)
            payload["n_sweep_results"].append({
                "N": n_val, "seed": seed,
                **{f"{m}_{k}": v for m, r in res.items() for k, v in r.items()},
            })
        _save(payload)
        rows = [r for r in payload["n_sweep_results"] if r["N"] == n_val]
        cma_swap = sum(1 for r in rows if "swap" in r["cma_classification"])
        ml_swap = sum(1 for r in rows if "swap" in r["ml_classification"])
        print(f"  N={n_val}: CMA swap {cma_swap}/{len(rows)} | ML swap {ml_swap}/{len(rows)}", flush=True)

    payload["total_runtime_s"] = round(time.time() - t_start, 1)
    payload["checkpoint"]["complete"] = True
    _save(payload)
    print(f"\n完成。总耗时 {payload['total_runtime_s']}s。结果: {OUT_PATH}")


if __name__ == "__main__":
    main()
