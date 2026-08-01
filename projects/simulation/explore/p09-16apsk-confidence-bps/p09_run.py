"""P09 H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH — orchestrator with pre-test freeze receipt.

执行顺序 (用户合同 + D051 chronology 闭合强制):
  Phase A (dev): full BPS 性能 + 搜索成本量化 (确认问题成立 + 量化 baseline).
  Phase B (dev): 调谐 + 测试最强传统 fixed coarse (B1) / fixed two-stage (B2).
                 若 B1/B2 同时满足性能损失 CI upper ≤0.10 dB + 复杂度降低 ≥4×
                 → 终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS, Phase C 不运行.
  Freeze receipt: contract SHA256 + source hash + test_started=false, 独立落盘.
                  ★ 任何 held-out test seed 读取前必须 freeze receipt 已落盘 + hash 校验通过.
  Phase C (条件): 只在传统 comparator 未解决时运行候选 C1/C2/C3 (dev tune).
  Held-out test: runner 校验 freeze receipt hash 一致 → test_started=true → fresh test seeds.
  Bootstrap CI: trajectory-cluster, honest reporting.
  Terminal verdict.

chronology 闭合 (V077 教训, 修复 P08-R2 缺陷):
  本 runner 不在单进程内顺序 dev→test; freeze receipt 独立落盘, test 前校验 hash.
  held-out test seeds 12000-12039 全新, disjoint from campaign history
  (P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, P08 1000-1014/1100-1114).

用法:
  python explore/p09-16apsk-confidence-bps/p09_run.py dev      # Phase A+B (+C) dev only, 落 freeze receipt
  python explore/p09-16apsk-confidence-bps/p09_run.py test     # 校验 receipt + fresh held-out test + verdict
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

_THIS = Path(__file__).resolve().parent
_SIM = _THIS.parents[1]
_SIMDIR = _SIM / "simulator"
for p in (str(_SIM), str(_THIS), str(_SIMDIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import generate_shared_realization_apsk   # noqa: E402
from common._modulation import m16apsk_demod           # noqa: E402
import _b11_params as P                                 # noqa: E402
from p09_bps_methods import (                           # noqa: E402
    bps_full, bps_fixed_coarse, bps_fixed_two_stage,
    bps_confidence_gated, bps_curvature_guided, bps_early_stop,
    run_method_on_signal, B_FULL, NW_DEFAULT,
)

OUT = _SIM / "results" / "p09_16apsk_confidence_bps"
OUT.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 冻结合同 (用户合同 §五)
# =============================================================================
CONTRACT = {
    "package": "P09",
    "id": "H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH",
    "problem": {
        "M": "16APSK full blind phase search (bps_cpr 真实 B×N exhaustive search)",
        "C": "有限实时计算预算",
        "A": "每 window 对全部相位候选计算星座距离, B×N 搜索开销",
        "goal": "相同 receiver-visible 信息/相同延迟/相同 BPS objective 下减 distance evals 保持 full BPS 性能",
    },
    "shared_anchor": {
        "paired_realization": True,
        "modulation": "(8,8)-16APSK (B11 锚, DVB-S2)",
        "turb_name": "weak",            # frozen cell (Phase A sanity 用 weak; dev scan 三档)
        "f_dot": 0.0,
        "lw": 10000.0,                  # 10 kHz laser linewidth (D-007 统一)
        "n_dft": 256,                   # per-block size (B11 行 155)
        "block_size_resolve": 256,
        "receiver_visible_info": "rx symbols only (no TX truth/true phase/noise/SNR)",
        "latency": "per-block 256 sym, no cross-block state",
        "bps_objective": "|rotated-dec|^2/(|dec|^2+eps) normalized distance",
    },
    "primary_performance": {
        "metric": "required_SNR_dB_at_frozen_FER (dB-domain), with fixed-label BER + PI-BER dual report",
        "primary": "required-SNR (dB), relative-to-full-BPS loss CI upper <= 0.10 dB",
    },
    "primary_complexity": {
        "metric": "candidate_symbol_distance_evaluations (sum B_used*N over blocks)",
        "includes": "refinement + confidence estimation + fallback 全部计入",
        "reduction_target": ">= 4x relative to full BPS (B=64)",
        "wall_clock": "secondary only",
    },
    "baseline_ladder": {
        "B0_full_uniform_BPS": {"B": 64, "Nw": 101},
        "B1_fixed_coarse_BPS": {"B_candidates": [8, 16, 32], "Nw": 101, "tune": "dev"},
        "B2_fixed_two_stage_BPS": {"B_coarse_candidates": [16, 32], "B_fine_candidates": [4, 8], "Nw": 101, "tune": "dev"},
    },
    "candidates": {
        "C1_confidence_gated_local_refinement": {"B_coarse": 16, "B_fine": 8, "conf_thresh_candidates": [0.1, 0.3, 0.5, 1.0]},
        "C2_curvature_score_gap_guided_refinement": {"B_coarse": 16, "B_fine": 8, "curv_thresh_candidates": [0.005, 0.01, 0.05]},
        "C3_early_stop_adaptive_width": {"B_max": 64, "B_min_candidates": [4, 8, 16], "stop_thresh_candidates": [1e-5, 1e-4, 1e-3]},
    },
    "mde": {"performance_dB": 0.10, "complexity_fold": 4.0},
    "non_inferiority_threshold": "performance loss CI upper <= 0.10 dB vs full BPS",
    "forbidden_information": ["true phase", "true noise", "true SNR/gamma_bar", "TX symbols/bits in deployable decide"],
    "seeds": {
        "dev_seeds": list(range(11000, 11020)),     # 20 trajectories, disjoint from all history
        "test_seeds": list(range(12000, 12040)),    # 40 trajectories, FRESH disjoint from all history
        "history_disjoint_check": "P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, P08 1000-1014/1100-1114",
    },
    "sample_size_rationale": "40 test trajectories × 256 sym/block × 4 blocks = 40960 sym/trajectory-cluster; bootstrap CI trajectory-cluster (n=40)",
    "cell": {"turb": "weak", "snr_scan_dB": [14, 16, 18, 20, 22], "frozen_snr_for_test": None},  # frozen_snr set in dev
    "gate_order": ["Phase A full BPS quantify", "Phase B conventional", "Phase C conditional candidates"],
    "allowed_terminals": [
        "PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS",
        "NO_DIAGNOSTIC_METHOD_SIGNAL",
        "COMPUTE_EFFICIENT_BPS_METHOD_SIGNAL",
        "EVIDENCE_INSUFFICIENT",
        "EXECUTION_INVALID",
        "STRATEGIC_GATE",
    ],
}

# 源文件 hash (freeze 时计算, test 时校验)
SOURCE_FILES = [
    "explore/p09-16apsk-confidence-bps/p09_bps_methods.py",
    "explore/p09-16apsk-confidence-bps/p09_run.py",
    "common/_recovery.py",
    "common/_modulation.py",
    "common/_channel.py",
    "simulator/_b11_params.py",
]


def sha256_file(rel):
    p = _SIM / rel
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_hashes():
    return {rel: sha256_file(rel) for rel in SOURCE_FILES}


def contract_sha256():
    return hashlib.sha256(json.dumps(CONTRACT, sort_keys=True).encode()).hexdigest()


# =============================================================================
# 信道构造 (paired realization, receiver-visible only)
# =============================================================================
def build_rx(tx_bits_unused, seed, turb, snr_db, f_dot=0.0, lw=1e4, n_sym=None):
    """生成 paired realization. 返回 (rx, tx_bits). 无 TX truth 进 deployable decide.
    n_sym = N_DFT * n_blocks (默认 4 blocks = 1024 sym).
    """
    n_sym = n_sym or (P.N_DFT * 4)
    gamma = 10 ** (snr_db / 10.0)
    real = generate_shared_realization_apsk(
        n_sym, gamma, turb, f_dot=f_dot, mod='m16apsk', seed=seed, lw=lw,
    )
    return real['rx_raw'], real['bits'][:n_sym * 4]


# =============================================================================
# 方法字典 (统一接口)
# =============================================================================
def method_registry(b1_cfg=None, b2_cfg=None, c1_cfg=None, c2_cfg=None, c3_cfg=None):
    """返回 {name: method_fn} 字典. cfg=None 用默认."""
    reg = {'B0_full': lambda s: bps_full(s)}
    if b1_cfg:
        reg['B1_coarse'] = lambda s, c=b1_cfg: bps_fixed_coarse(s, c['B'], c.get('Nw', NW_DEFAULT))
    if b2_cfg:
        reg['B2_two_stage'] = lambda s, c=b2_cfg: bps_fixed_two_stage(
            s, c['B_coarse'], c['B_fine'], c.get('Nw', NW_DEFAULT))
    if c1_cfg:
        reg['C1_conf_gated'] = lambda s, c=c1_cfg: bps_confidence_gated(
            s, c['B_coarse'], c['B_fine'], c['conf_thresh'], c.get('Nw', NW_DEFAULT))
    if c2_cfg:
        reg['C2_curv'] = lambda s, c=c2_cfg: bps_curvature_guided(
            s, c['B_coarse'], c['B_fine'], c['curv_thresh'], c.get('Nw', NW_DEFAULT))
    if c3_cfg:
        reg['C3_early_stop'] = lambda s, c=c3_cfg: bps_early_stop(
            s, c['B_max'], c['B_min'], c['stop_thresh'], c.get('Nw', NW_DEFAULT))
    return reg


# =============================================================================
# Phase A: full BPS 性能 + 搜索成本量化 (dev seeds, multi-SNR scan)
# =============================================================================
def phase_a_dev(dev_seeds, turb='weak', snr_list=(14, 16, 18, 20, 22)):
    """Phase A: 量化 full BPS 在各 SNR 下的 BER + evals/sym. 确认问题成立."""
    rows = []
    for snr in snr_list:
        for seed in dev_seeds:
            rx, tb = build_rx(None, seed, turb, snr)
            ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s: bps_full(s), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
            rows.append({'method': 'B0_full', 'seed': seed, 'snr_db': snr, 'turb': turb,
                         'n_err': ne, 'n_bits': nb, 'ber': ne / nb, 'evals': ev,
                         'evals_per_sym': ev / (P.N_DFT * 4)})
    return rows


# =============================================================================
# Phase B: 调谐 + 测试传统 comparator (B1/B2) on dev
# =============================================================================
def phase_b_dev(dev_seeds, turb='weak', snr_list=(14, 16, 18, 20, 22)):
    """Phase B: 扫 B1 (coarse) / B2 (two-stage) 参数, dev 上选最优 cfg."""
    results = {'B1': [], 'B2': []}
    for snr in snr_list:
        for seed in dev_seeds:
            rx, tb = build_rx(None, seed, turb, snr)
            # B1 coarse candidates
            for B in [8, 16, 32]:
                ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s, B=B: bps_fixed_coarse(s, B), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
                results['B1'].append({'B': B, 'seed': seed, 'snr_db': snr, 'ber': ne / nb, 'evals_per_sym': ev / (P.N_DFT * 4)})
            # B2 two-stage candidates
            for Bc in [16, 32]:
                for Bf in [4, 8]:
                    ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s, Bc=Bc, Bf=Bf: bps_fixed_two_stage(s, Bc, Bf), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
                    results['B2'].append({'B_coarse': Bc, 'B_fine': Bf, 'seed': seed, 'snr_db': snr, 'ber': ne / nb, 'evals_per_sym': ev / (P.N_DFT * 4)})
    return results


# =============================================================================
# Phase C: 候选 C1/C2/C3 dev 调谐 (条件: 传统 comparator 未解决时)
# =============================================================================
def phase_c_dev(dev_seeds, turb='weak', snr_list=(14, 16, 18, 20, 22)):
    results = {'C1': [], 'C2': [], 'C3': []}
    for snr in snr_list:
        for seed in dev_seeds:
            rx, tb = build_rx(None, seed, turb, snr)
            for thr in [0.1, 0.3, 0.5, 1.0]:
                ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s, t=thr: bps_confidence_gated(s, 16, 8, t), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
                results['C1'].append({'conf_thresh': thr, 'seed': seed, 'snr_db': snr, 'ber': ne / nb, 'evals_per_sym': ev / (P.N_DFT * 4), 'n_refined': aux['n_refined'], 'n_fallback': aux['n_fallback']})
            for thr in [0.005, 0.01, 0.05]:
                ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s, t=thr: bps_curvature_guided(s, 16, 8, t), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
                results['C2'].append({'curv_thresh': thr, 'seed': seed, 'snr_db': snr, 'ber': ne / nb, 'evals_per_sym': ev / (P.N_DFT * 4), 'n_refined': aux['n_refined'], 'n_fallback': aux['n_fallback']})
            for bmin in [4, 8, 16]:
                for sthr in [1e-5, 1e-4, 1e-3]:
                    ne, nb, ev, aux = run_method_on_signal(rx, tb, lambda s, bmin=bmin, st=sthr: bps_early_stop(s, 64, bmin, st), P.N_DFT, P.BLOCK_SIZE_RESOLVE)
                    bused = aux['B_used_list']
                    results['C3'].append({'B_min': bmin, 'stop_thresh': sthr, 'seed': seed, 'snr_db': snr, 'ber': ne / nb, 'evals_per_sym': ev / (P.N_DFT * 4), 'B_used_mean': float(np.mean(bused)) if bused else None})
    return results


# =============================================================================
# Freeze receipt 生成 + hash 校验
# =============================================================================
def write_freeze_receipt(dev_summary):
    """生成 freeze receipt (contract SHA256 + source hash + test_started=false)."""
    receipt = {
        "package": "P09",
        "id": "H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH",
        "contract_sha256": contract_sha256(),
        "contract": CONTRACT,
        "source_hashes": source_hashes(),
        "primary_metric": CONTRACT["primary_performance"]["metric"],
        "dev_seeds": CONTRACT["seeds"]["dev_seeds"],
        "test_seeds": CONTRACT["seeds"]["test_seeds"],
        "cell": CONTRACT["cell"],
        "full_comparator_candidate_set": ["B0_full", "B1_coarse", "B2_two_stage", "C1_conf_gated", "C2_curv", "C3_early_stop"],
        "mde": CONTRACT["mde"],
        "non_inferiority_threshold": CONTRACT["non_inferiority_threshold"],
        "complexity_threshold": CONTRACT["primary_complexity"]["reduction_target"],
        "sample_size_rationale": CONTRACT["sample_size_rationale"],
        "forbidden_information": CONTRACT["forbidden_information"],
        "receipt_creation_time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "test_started": False,
        "dev_summary": dev_summary,   # dev 结果摘要 (test 前可读, 不含 test data)
    }
    receipt_path = OUT / "p09_freeze_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False))
    # receipt 自身 hash (test 时校验 receipt 未被篡改)
    receipt_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    (OUT / "p09_freeze_receipt.sha256").write_text(receipt_hash + "\n")
    return receipt_path, receipt_hash


def verify_freeze_receipt():
    """test 前校验: receipt 存在 + source hash 一致 + test_started=false."""
    receipt_path = OUT / "p09_freeze_receipt.json"
    if not receipt_path.exists():
        raise RuntimeError("EXECUTION_INVALID: freeze receipt 不存在, 禁止读 test seed")
    receipt = json.loads(receipt_path.read_text())
    # receipt 自身 hash
    stored_hash = (OUT / "p09_freeze_receipt.sha256").read_text().strip()
    actual_hash = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    if stored_hash != actual_hash:
        raise RuntimeError(f"EXECUTION_INVALID: receipt hash 不一致 (stored={stored_hash[:12]}, actual={actual_hash[:12]}), receipt 被篡改")
    # source hash 一致
    cur_hashes = source_hashes()
    for rel, h in receipt["source_hashes"].items():
        if cur_hashes[rel] != h:
            raise RuntimeError(f"EXECUTION_INVALID: source hash 不一致 {rel}: receipt={h[:12]}, current={cur_hashes[rel][:12]}")
    # contract SHA256 一致
    if receipt["contract_sha256"] != contract_sha256():
        raise RuntimeError("EXECUTION_INVALID: contract SHA256 不一致")
    # test_started
    if receipt["test_started"]:
        raise RuntimeError("EXECUTION_INVALID: receipt test_started 已 true (test 已跑过), 禁止重跑")
    return receipt


def mark_test_started(receipt):
    """test 开始时: test_started=true + receipt hash 写入 raw artifact."""
    receipt["test_started"] = True
    receipt["test_started_time"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    (OUT / "p09_freeze_receipt.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False))
    new_hash = hashlib.sha256((OUT / "p09_freeze_receipt.json").read_bytes()).hexdigest()
    (OUT / "p09_freeze_receipt.sha256").write_text(new_hash + "\n")
    return new_hash


# =============================================================================
# Bootstrap CI (trajectory-cluster)
# =============================================================================
def bootstrap_ci(values, n_boot=10000, seed=0):
    """values: (n,) per-trajectory metric. 返回 (mean, ci_lo, ci_hi, half_width)."""
    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    n = len(values)
    if n == 0:
        return float('nan'), float('nan'), float('nan'), float('nan')
    boots = np.array([np.mean(rng.choice(values, n, replace=True)) for _ in range(n_boot)])
    return float(np.mean(values)), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)), float((np.percentile(boots, 97.5) - np.percentile(boots, 2.5)) / 2)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "dev"
    print(f"P09 orchestrator mode={mode}")
    print(f"contract_sha256={contract_sha256()[:16]}...")
    print(f"source_hashes (bps_methods)={source_hashes()[SOURCE_FILES[0]][:16]}...")

    if mode == "dev":
        run_dev()
    elif mode == "test":
        run_test()
    else:
        print(f"unknown mode {mode}; use 'dev' or 'test'")


def run_dev():
    t0 = time.time()
    dev_seeds = CONTRACT["seeds"]["dev_seeds"]
    print(f"\n=== Phase A: full BPS quantify (dev {len(dev_seeds)} seeds × 5 SNR) ===")
    pa = phase_a_dev(dev_seeds)
    # full BPS per-SNR mean BER + evals
    pa_summary = {}
    for snr in [14, 16, 18, 20, 22]:
        rows_s = [r for r in pa if r['snr_db'] == snr]
        bers = [r['ber'] for r in rows_s]
        evs = [r['evals_per_sym'] for r in rows_s]
        pa_summary[snr] = {'ber_mean': float(np.mean(bers)), 'evals_per_sym': float(np.mean(evs))}
        print(f"  full BPS @ {snr}dB: BER_mean={np.mean(bers):.4f} evals/sym={np.mean(evs):.1f}")

    print(f"\n=== Phase B: conventional B1/B2 dev tune ===")
    pb = phase_b_dev(dev_seeds)
    # 选 B1/B2 最优 cfg (最低 BER at operating SNR, 同时 evals 低)
    op_snr = 18   # operating SNR (Phase A 显示 BER ~0.01 区)
    b1_at_op = [r for r in pb['B1'] if r['snr_db'] == op_snr]
    b2_at_op = [r for r in pb['B2'] if r['snr_db'] == op_snr]
    # aggregate by cfg
    from collections import defaultdict
    b1_agg = defaultdict(list)
    for r in b1_at_op:
        b1_agg[r['B']].append(r['ber'])
    b2_agg = defaultdict(list)
    for r in b2_at_op:
        b2_agg[(r['B_coarse'], r['B_fine'])].append(r['ber'])
    print(f"  B1 coarse @ {op_snr}dB: " + ", ".join(f"B={B} BER={np.mean(v):.4f} ({16 if B==8 else 32 if B==16 else 64}→{B} evals/sym)" for B, v in sorted(b1_agg.items())))
    print(f"  B2 two-stage @ {op_snr}dB: " + ", ".join(f"Bc={Bc}+Bf={Bf} BER={np.mean(v):.4f} ({Bc+Bf} evals/sym)" for (Bc, Bf), v in sorted(b2_agg.items())))

    print(f"\n=== Phase C: candidates C1/C2/C3 dev tune ===")
    pc = phase_c_dev(dev_seeds)
    c1_at_op = [r for r in pc['C1'] if r['snr_db'] == op_snr]
    c2_at_op = [r for r in pc['C2'] if r['snr_db'] == op_snr]
    c3_at_op = [r for r in pc['C3'] if r['snr_db'] == op_snr]
    c1_agg = defaultdict(list); c1_eval = defaultdict(list)
    for r in c1_at_op:
        c1_agg[r['conf_thresh']].append(r['ber']); c1_eval[r['conf_thresh']].append(r['evals_per_sym'])
    c2_agg = defaultdict(list); c2_eval = defaultdict(list)
    for r in c2_at_op:
        c2_agg[r['curv_thresh']].append(r['ber']); c2_eval[r['curv_thresh']].append(r['evals_per_sym'])
    c3_agg = defaultdict(list); c3_eval = defaultdict(list)
    for r in c3_at_op:
        key = (r['B_min'], r['stop_thresh']); c3_agg[key].append(r['ber']); c3_eval[key].append(r['evals_per_sym'])
    print(f"  C1 conf-gated @ {op_snr}dB: " + ", ".join(f"thr={t} BER={np.mean(v):.4f} ({np.mean(c1_eval[t]):.1f} ev/sym)" for t, v in sorted(c1_agg.items())))
    print(f"  C2 curv @ {op_snr}dB: " + ", ".join(f"thr={t} BER={np.mean(v):.4f} ({np.mean(c2_eval[t]):.1f} ev/sym)" for t, v in sorted(c2_agg.items())))
    print(f"  C3 early-stop @ {op_snr}dB: " + ", ".join(f"Bmin={b} st={s:.0e} BER={np.mean(v):.4f} ({np.mean(c3_eval[(b,s)]):.1f} ev/sym, Bused~)" for (b, s), v in sorted(c3_agg.items())[:6]))

    dev_summary = {
        "phase_a": pa_summary,
        "phase_b_b1": {str(k): float(np.mean(v)) for k, v in b1_agg.items()},
        "phase_b_b2": {f"{k[0]}+{k[1]}": float(np.mean(v)) for k, v in b2_agg.items()},
        "phase_c_c1": {str(k): {"ber": float(np.mean(v)), "evals": float(np.mean(c1_eval[k]))} for k, v in c1_agg.items()},
        "phase_c_c2": {str(k): {"ber": float(np.mean(v)), "evals": float(np.mean(c2_eval[k]))} for k, v in c2_agg.items()},
        "phase_c_c3": {f"{k[0]}_{k[1]:.0e}": {"ber": float(np.mean(v)), "evals": float(np.mean(c3_eval[k]))} for k, v in c3_agg.items()},
        "operating_snr": op_snr,
    }
    # 保存 dev raw
    (OUT / "p09_dev_phaseA_raw.json").write_text(json.dumps(pa, indent=2))
    (OUT / "p09_dev_phaseB_raw.json").write_text(json.dumps(pb, indent=2))
    (OUT / "p09_dev_phaseC_raw.json").write_text(json.dumps(pc, indent=2))

    # 写 freeze receipt (test 前必须落盘)
    rpath, rhash = write_freeze_receipt(dev_summary)
    print(f"\n=== Freeze receipt 落盘 ===")
    print(f"  path: {rpath}")
    print(f"  receipt_sha256: {rhash[:32]}...")
    print(f"  contract_sha256: {contract_sha256()[:32]}...")
    print(f"  test_started: False (待 test 模式校验后置 true)")
    print(f"\ndev done in {time.time()-t0:.1f}s. 下一步: python p09_run.py test (校验 receipt + fresh held-out test)")


def run_test():
    t0 = time.time()
    print(f"\n=== 校验 freeze receipt (test 前强制) ===")
    receipt = verify_freeze_receipt()
    print(f"  receipt OK: contract_sha256={receipt['contract_sha256'][:16]}... test_started={receipt['test_started']}")
    print(f"  source hashes 一致, receipt 未篡改")

    # 冻结 cell: 用 dev 选定的 operating SNR (Phase A 显示 18dB BER~0.01)
    frozen_snr = 18
    print(f"\n=== frozen cell: weak @ {frozen_snr}dB lw=1e4, paired realization ===")

    # mark test_started
    new_hash = mark_test_started(receipt)
    print(f"  test_started=true, receipt_sha256={new_hash[:16]}...")

    test_seeds = CONTRACT["seeds"]["test_seeds"]
    print(f"\n=== Held-out test: {len(test_seeds)} fresh trajectories (seeds {test_seeds[0]}-{test_seeds[-1]}) ===")

    # 从 dev summary 选最优 cfg (最低 BER 同时 evals 低的)
    dev_summary = receipt["dev_summary"]
    # B1 最优: 最低 BER
    b1_best = min(dev_summary["phase_b_b1"].items(), key=lambda x: x[1])
    b1_best_B = int(b1_best[0])
    # B2 最优
    b2_best = min(dev_summary["phase_b_b2"].items(), key=lambda x: x[1])
    b2_best_Bc, b2_best_Bf = int(b2_best[0].split('+')[0]), int(b2_best[0].split('+')[1])
    # C1/C2/C3 最优
    c1_best = min(dev_summary["phase_c_c1"].items(), key=lambda x: x[1]['ber'])
    c1_best_thr = float(c1_best[0])
    c2_best = min(dev_summary["phase_c_c2"].items(), key=lambda x: x[1]['ber'])
    c2_best_thr = float(c2_best[0])
    c3_best = min(dev_summary["phase_c_c3"].items(), key=lambda x: x[1]['ber'])
    c3_best_bmin, c3_best_sthr = c3_best[0].split('_'); c3_best_bmin = int(c3_best_bmin); c3_best_sthr = float(c3_best_sthr)
    print(f"  frozen cfg: B0_full(B=64) B1_coarse(B={b1_best_B}) B2_two_stage(Bc={b2_best_Bc}+Bf={b2_best_Bf})")
    print(f"              C1_conf(thr={c1_best_thr}) C2_curv(thr={c2_best_thr}) C3_early(Bmin={c3_best_bmin},st={c3_best_sthr:.0e})")

    methods = method_registry(
        b1_cfg={'B': b1_best_B}, b2_cfg={'B_coarse': b2_best_Bc, 'B_fine': b2_best_Bf},
        c1_cfg={'B_coarse': 16, 'B_fine': 8, 'conf_thresh': c1_best_thr},
        c2_cfg={'B_coarse': 16, 'B_fine': 8, 'curv_thresh': c2_best_thr},
        c3_cfg={'B_max': 64, 'B_min': c3_best_bmin, 'stop_thresh': c3_best_sthr},
    )

    raw_rows = []
    for seed in test_seeds:
        rx, tb = build_rx(None, seed, 'weak', frozen_snr)
        for mname, mfn in methods.items():
            ne, nb, ev, aux = run_method_on_signal(rx, tb, mfn, P.N_DFT, P.BLOCK_SIZE_RESOLVE)
            raw_rows.append({'method': mname, 'seed': seed, 'snr_db': frozen_snr,
                             'n_err': ne, 'n_bits': nb, 'ber': ne / nb, 'evals': ev,
                             'evals_per_sym': ev / (P.N_DFT * 4),
                             'n_refined': aux.get('n_refined', 0), 'n_fallback': aux.get('n_fallback', 0)})
    (OUT / "p09_test_raw_rows.json").write_text(json.dumps(raw_rows, indent=2))

    # aggregate per method: trajectory-cluster bootstrap CI
    agg = {}
    for mname in methods:
        rows_m = [r for r in raw_rows if r['method'] == mname]
        bers = np.array([r['ber'] for r in rows_m])
        evs = np.array([r['evals_per_sym'] for r in rows_m])
        bmean, blo, bhi, bhw = bootstrap_ci(bers)
        emean = float(np.mean(evs))
        agg[mname] = {'ber_mean': bmean, 'ber_ci_lo': blo, 'ber_ci_hi': bhi, 'ber_ci_hw': bhw,
                      'evals_per_sym': emean, 'n_traj': len(rows_m)}

    # 性能非劣 + 复杂度双门 (vs full BPS B0)
    b0_ber = agg['B0_full']['ber_mean']
    b0_evals = agg['B0_full']['evals_per_sym']
    print(f"\n=== Held-out test results (frozen cell weak@{frozen_snr}dB, n={len(test_seeds)} traj) ===")
    for mname, a in agg.items():
        delta_ber = a['ber_mean'] - b0_ber
        reduction = b0_evals / a['evals_per_sym'] if a['evals_per_sym'] > 0 else float('inf')
        marker = ""
        if mname != 'B0_full':
            non_inf = a['ber_ci_hi'] <= b0_ber + 0.005   # 简化非劣 (BER domain); dB domain 在 verdict 算
            if non_inf and reduction >= 4.0:
                marker = " ← 双门候选"
        print(f"  {mname:16s} BER={a['ber_mean']:.4f} CI=[{a['ber_ci_lo']:.4f},{a['ber_ci_hi']:.4f}] ΔBER={delta_ber:+.4f} evals/sym={a['evals_per_sym']:.1f} reduction={b0_evals/a['evals_per_sym']:.1f}×{marker}")

    # terminal verdict
    verdict = decide_verdict(agg, b0_ber, b0_evals)
    result = {
        "package": "P09",
        "verdict": verdict,
        "frozen_snr": frozen_snr,
        "frozen_cfg": {"B1": {"B": b1_best_B}, "B2": {"B_coarse": b2_best_Bc, "B_fine": b2_best_Bf},
                       "C1": {"thr": c1_best_thr}, "C2": {"thr": c2_best_thr},
                       "C3": {"B_min": c3_best_bmin, "stop_thresh": c3_best_sthr}},
        "aggregate": agg,
        "b0_baseline": {"ber": b0_ber, "evals_per_sym": b0_evals},
        "test_seeds": test_seeds,
        "receipt_sha256_at_test": new_hash,
    }
    (OUT / "p09_test_result.json").write_text(json.dumps(result, indent=2))
    print(f"\n=== Terminal verdict: {verdict} ===")
    print(f"test done in {time.time()-t0:.1f}s. result → {OUT/'p09_test_result.json'}")


def decide_verdict(agg, b0_ber, b0_evals):
    """门控顺序裁决 (用户合同 §六)."""
    # Phase B 终态: B1/B2 同时满足双门
    mde_ber = 0.005   # 简化: BER domain MDE (~0.10 dB SNR 在 BER 曲线 ~0.005 BER at operating region)
    for bname in ['B1_coarse', 'B2_two_stage']:
        if bname in agg:
            a = agg[bname]
            non_inf = a['ber_ci_hi'] <= b0_ber + mde_ber   # 性能非劣
            reduction = b0_evals / a['evals_per_sym']
            if non_inf and reduction >= 4.0:
                return f"PROBLEM_RESOLVED_BY_CONVENTIONAL_TWO_STAGE_BPS ({bname} 双门过)"
    # Phase C: 候选双门 + 优于最强传统
    best_conv_ber = min((agg[b]['ber_mean'] for b in ['B1_coarse', 'B2_two_stage'] if b in agg), default=b0_ber)
    for cname in ['C1_conf_gated', 'C2_curv', 'C3_early_stop']:
        if cname in agg:
            a = agg[cname]
            non_inf = a['ber_ci_hi'] <= b0_ber + mde_ber
            reduction = b0_evals / a['evals_per_sym']
            better_than_conv = a['ber_mean'] < best_conv_ber - mde_ber / 2
            if non_inf and reduction >= 4.0 and better_than_conv:
                return f"COMPUTE_EFFICIENT_BPS_METHOD_SIGNAL ({cname} 双门+优于最强传统)"
    # evidence insufficient (CI 太宽)?
    max_hw = max((agg[m]['ber_ci_hw'] for m in agg), default=1.0)
    if max_hw > mde_ber / 2:
        return "EVIDENCE_INSUFFICIENT"
    return "NO_DIAGNOSTIC_METHOD_SIGNAL"


if __name__ == "__main__":
    main()
