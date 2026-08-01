"""P10 RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER — orchestrator with pre-test freeze receipt.

执行顺序 (用户合同 §四 chronology 两-commit + §七 Phase A/B/C 门控):
  Phase A (dev): fresh crossover confirmation — 至少两工况 ML 显著优于 CMA + 至少两工况 CMA 显著优于 ML
                 fixed-label BER PRIMARY + PI-BER secondary 双口径; ranking 反转非 metric/swap artifact.
                 若不能复现 -> PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE, Phase B/C 不运行.
  Phase B (dev): 传统廉价规则 B0-B4 (always-CMA/always-ML/best-global/config-rule/threshold)
                 若 B3/B4 已将相对 oracle regret 降至 MDE 以内 -> PROBLEM_RESOLVED_BY_SIMPLE_ROUTING.
  Phase C (dev, 条件): 只在 crossover 存活 + B 未解决时运行候选 C1/C2/C3 (dev tune).
  Freeze receipt: contract SHA256 + source hash + test_started=false, 独立落盘 (Commit 1).
                  ★ 任何 held-out test seed 读取前必须 freeze receipt 已落盘 + hash 校验通过.
  Held-out test: runner 校验 freeze receipt hash 一致 -> test_started=true -> fresh test seeds.
  Bootstrap CI: trajectory-cluster paired ΔBER CI (paired Δ = cand_BER - conv_BER per realization).
  Terminal verdict (§八 allowed_terminals).

chronology 闭合 (V077 教训 + P09 复用):
  本 runner 不在单进程内顺序 dev->test; freeze receipt 独立落盘, test 前校验 hash.
  held-out test seeds fresh disjoint from campaign history.

single-path 执行门 (合同 §六 最高优先级):
  router 先产生 expert_id -> 之后只调被选专家 -> 未选专家 monkeypatch 为 raise ->
  verifier 随机抽 >=20 realization 验证未选专家零调用.

用法:
  python explore/p10-single-expert-router/p10_run.py freeze    # 落 freeze receipt (test_started=false)
  python explore/p10-single-expert-router/p10_run.py dev       # Phase A+B(+C) dev only
  python explore/p10-single-expert-router/p10_run.py test      # 校验 receipt + fresh held-out + verdict
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
for p in (str(_SIM), str(_THIS)):
    if p not in sys.path:
        sys.path.insert(0, p)

OUT = _SIM / "results" / "p10_single_expert_router"
OUT.mkdir(parents=True, exist_ok=True)

# =============================================================================
# 冻结合同 (用户合同 §四 + §五 + §七)
# =============================================================================
CONTRACT = {
    "package": "P10",
    "id": "RISK_BUDGETED_SINGLE_EXPERT_ML_CMA_ROUTER",
    "problem": {
        "M": "固定使用 ButterflyCNN ML 均衡器 或 固定使用 StandardCMA (二选一, payload 前冻结)",
        "C": "接收工况在 短/慢变 (小 SOP 漂移) 与 长/快变 (大 SOP 漂移/OOD) 之间变化, 只允许执行一个主专家",
        "A": "历史证据显示专家排名反转 (D015/S017/S020/D022); 用户指令描述与证据方向相反, fresh dev 独立复现真实方向",
        "goal": "仅根据 receiver-visible 前缀与合法配置, 在 payload 前选 ML 或 CMA, 只执行被选中的一个",
        "claim_ceiling": "跨工况风险约束单专家选择策略 (非新均衡器/非首创 ML-CMA 混合/非通用智能接收机)",
    },
    "shared_anchor": {
        "paired_realization": True,
        "modulation": "QPSK (双偏振 PolMUX, P05 identity)",
        "turbulence": "weak/moderate/strong (params.py provenance, 不制造新湍流)",
        "receiver_visible_info": "rx prefix + known pilot/training symbols 残差 + raw RX stats + 短 CMA diagnostic + 配置字段",
        "latency": "payload 前选 expert (no cross-payload state in router decide)",
        "ambiguity_resolution": "fixed-label BER PRIMARY (swap-visible 不变量 10); PI-BER secondary (swap-blind, 报告不判)",
    },
    "experts": {
        "ML": "ButterflyCNNEqualizer2x2 (common/_ml_equalizer.py:104, P05 frozen identity, n_tap=11, lr=5e-3, batch=1024, n_epochs=15, MSE supervised)",
        "CMA": "StandardCMA2x2 (prompt019_mu_compress_mve.py:96, Godard 1980 with-z, P05 corrected, n_tap=11, mu=1e-3, R2=1.0, block=64)",
    },
    "primary_metric": {
        "metric": "fixed-label BER (swap-visible, 不变量 10) PRIMARY + PI-BER secondary",
        "decision_rule": "router 只用 receiver-visible feature, payload TX truth 只用于最终计分",
        "forbidden_in_decide": ["payload TX symbols/bits", "true h/theta/SNR/gamma_bar/fG", "两专家 payload 输出", "post-hoc oracle 标签"],
    },
    "complexity_metric": {
        "metric": "total compute proxy = prefix feature 提取 + 短 CMA diagnostic + router decide + 被选专家 train+infer 全部 FLOP",
        "includes": "未选专家必须零调用 (single-path 门); oracle selector 独立 post-hoc 分支不共享状态",
        "reduction_check": "router 成本明显低于同时运行两专家 (合同 §八 METHOD_SIGNAL 条件 6)",
    },
    "baseline_ladder": {
        "B0_always_CMA": "固定选 CMA",
        "B1_always_ML": "固定选 ML",
        "B2_best_global_single_expert": "dev-tuned 全局最优单专家 pick (frozen at test)",
        "B3_configuration_only_rule": "N >= N_thresh -> CMA else ML (deployable config only)",
        "B4_dev_tuned_simple_prefix_threshold": "单 receiver-visible stat 阈值",
    },
    "candidates": {
        "C1_frozen_logistic_ridge_router": "冻结 logistic/ridge on receiver-visible prefix features (dev tune weights/bias/thresh)",
        "C2_risk_constrained_router_with_CMA_safe_fallback": "risk score > thresh -> CMA; else regret sign 决定",
        "C3_conservative_router_with_abstention": "不确定时选 CMA (abstain -> CMA)",
    },
    "mde": {
        "fixed_ber_MDE": 0.02,
        "MDE_rationale": "务实可毕业路线 (D005); fixed-label BER 在 operating region 的可检测差",
        "complexity_fold": 2.0,
        "complexity_rationale": "router 成本须明显低于同时跑两专家 (单路径执行价值); 非 4x (router 本身有成本)",
    },
    "non_inferiority_threshold": "候选 fixed-BER 不劣于 always-CMA safety margin (catastrophic event rate)",
    "method_signal_conditions": [
        "1. 候选相对最强 deployable 传统规则改善达预冻结 MDE 且 paired CI 支持",
        "2. 捕获预冻结比例的 oracle headroom",
        "3. catastrophic event rate 不劣于 always-CMA safety margin",
        "4. 每个主要工况无灾难性退化",
        "5. 真正只运行一个 payload 专家 (single-path 门)",
        "6. router 成本明显低于同时运行两专家",
        "7. 信号不完全由配置字段或 swap 标签解释",
    ],
    "seeds": {
        "dev_seeds_phaseA": list(range(13000, 13006)),     # 6 trajectories Phase A crossover (fresh disjoint)
        "dev_seeds_phaseBC": list(range(13010, 13020)),    # 10 trajectories Phase B/C dev tune
        "test_seeds": list(range(14000, 14040)),           # 40 trajectories held-out FRESH disjoint
        "history_disjoint_check": "P09 11000-11019/12000-12039, P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, P08 1000-1014/1100-1114, P05 1000-1011",
    },
    "crossover_cells": {
        "ML_favored_hypothesis": {"N": 2_000_000, "f_G": 30.0, "SNR_dB": 20.0, "SOP_RATE": 1e-7, "turb": "strong"},
        "CMA_favored_hypothesis": {"N": 5_000_000, "f_G": 1000.0, "SNR_dB": 20.0, "SOP_RATE": 4e-7, "turb": "strong"},
        "note": "基于 D015/S017/S020 证据方向 (短N小SOP->ML; 长N大SOP/OOD->CMA). fresh dev 独立验证两方向.",
    },
    "allowed_terminals": [
        "PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE",
        "PROBLEM_RESOLVED_BY_SIMPLE_ROUTING",
        "NO_DIAGNOSTIC_METHOD_SIGNAL",
        "RISK_BUDGETED_ROUTER_METHOD_SIGNAL",
        "EVIDENCE_INSUFFICIENT",
        "EXECUTION_INVALID",
        "STRATEGIC_GATE",
    ],
    "single_path_execution_gate": {
        "priority": "HIGHEST (合同 §六)",
        "checks": [
            "1. router 先产生 expert_id",
            "2. 之后只调用被选专家",
            "3. runner 记录 ML/CMA 调用次数和训练成本",
            "4. 未选专家 monkeypatch 为 调用即抛异常",
            "5. verifier 随机抽 >=20 realization 验证未选专家零调用",
            "6. 成本含 prefix feature + 短诊断 + router + 被选专家全部",
            "7. oracle selector 独立 post-hoc 分支运行两专家, 不与 deployable 共享状态/特征",
        ],
    },
}

SOURCE_FILES = [
    "explore/p10-single-expert-router/p10_methods.py",
    "explore/p10-single-expert-router/p10_run.py",
]
# 加上 frozen common 文件 hash
FROZEN_FILES = [
    "common/_ml_equalizer.py",
    "common/_cma.py",
    "common/_gg_time.py",
    "common/_config.py",
    "explore/cma-fade-divergence/prompt019_mu_compress_mve.py",
    "explore/cma-fade-divergence/ml_long_seq_failure.py",
    "explore/cma-fade-divergence/prompt012_longseq_audit.py",
]


def sha256_file(rel):
    p = _SIM / rel
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def source_hashes():
    return {rel: sha256_file(rel) for rel in (SOURCE_FILES + FROZEN_FILES)}


def contract_sha256():
    return hashlib.sha256(json.dumps(CONTRACT, sort_keys=True).encode()).hexdigest()


def write_freeze_receipt(dev_summary=None):
    receipt = {
        "package": CONTRACT["package"],
        "id": CONTRACT["id"],
        "contract_sha256": contract_sha256(),
        "contract": CONTRACT,
        "source_hashes": source_hashes(),
        "primary_metric": CONTRACT["primary_metric"]["metric"],
        "complexity_metric": CONTRACT["complexity_metric"]["metric"],
        "mde": CONTRACT["mde"],
        "non_inferiority_threshold": CONTRACT["non_inferiority_threshold"],
        "dev_seeds_phaseA": CONTRACT["seeds"]["dev_seeds_phaseA"],
        "dev_seeds_phaseBC": CONTRACT["seeds"]["dev_seeds_phaseBC"],
        "test_seeds": CONTRACT["seeds"]["test_seeds"],
        "crossover_cells": CONTRACT["crossover_cells"],
        "receipt_creation_time": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "test_started": False,
    }
    if dev_summary is not None:
        receipt["dev_summary"] = dev_summary
    (OUT / "p10_freeze_receipt.json").write_text(json.dumps(receipt, indent=2))
    # also write sha256 of receipt itself
    rcpt = (OUT / "p10_freeze_receipt.json").read_bytes()
    (OUT / "p10_freeze_receipt.sha256").write_text(hashlib.sha256(rcpt).hexdigest())
    return receipt


def verify_freeze_receipt():
    """Verify receipt on disk: source/contract hash match + test_started must be False pre-test."""
    rcpt = json.loads((OUT / "p10_freeze_receipt.json").read_text())
    # check source hashes
    cur_sh = source_hashes()
    mismatches = []
    for f, h in rcpt["source_hashes"].items():
        if h is None and cur_sh[f] is None:
            continue
        if cur_sh.get(f) != h:
            mismatches.append(f"{f}: receipt={h} current={cur_sh.get(f)}")
    if mismatches:
        return False, f"source hash mismatch: {mismatches}"
    # check contract sha
    if rcpt["contract_sha256"] != contract_sha256():
        return False, "contract SHA256 mismatch"
    # check test_started
    if rcpt.get("test_started", False):
        return False, "test_started already True (freeze violated)"
    return True, rcpt


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "freeze"
    if mode == "freeze":
        rcpt = write_freeze_receipt()
        print(f"freeze receipt written: {OUT/'p10_freeze_receipt.json'}")
        print(f"contract_sha256: {rcpt['contract_sha256']}")
        print(f"test_started: {rcpt['test_started']}")
        print(f"source files hashed: {len(rcpt['source_hashes'])}")
    elif mode == "verify":
        ok, msg = verify_freeze_receipt()
        print(f"verify: {ok} -- {msg if not ok else 'OK'}")
    else:
        print(f"unknown mode {mode}; use freeze|verify (dev/test 在子 agent 执行)")
