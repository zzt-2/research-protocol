"""Post-hoc behavior scorer for Probe cost, semantic smoke, and recovery cases."""

from pathlib import Path
import re


def _raw_response(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Raw response\s*$\n(?P<response>.*?)(?=^## Behavior scorer output\s*$)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"missing closed Raw response section: {path}")
    return match.group("response").strip().lower()


def _has(text: str, *terms: str) -> bool:
    return any(term.lower() in text for term in terms)


def _score_probe(text: str) -> dict[str, bool]:
    rejects_heavy_default = _has(text, "默认不创建", "does not require") and all(
        term in text for term in ("receipt", "verifier", "synthesis")
    )
    return {
        "probe_intensity": "probe" in text and _has(text, "paired-input", "paired input", "配对"),
        "bounded_budget": _has(text, "两分钟", "2 分钟", "two-minute", "two minutes")
        and _has(text, "最多一组", "at most one", "唯一配对"),
        "compact_record": "compact" in text or "紧凑" in text,
        "rejects_full_chain_by_default": rejects_heavy_default,
        "diagnostic_ceiling": "diagnostic" in text,
        "pass_not_method_signal": "pass" in text
        and _has(text, "method_signal", "方法信号", "method signal")
        and _has(text, "不是", "不能", "not"),
        "harvest_assessed_not_forced": _has(text, "no_durable_harvest_reason", "no durable harvest")
        and _has(text, "不制造", "不创建", "no ledger item"),
        "stops_at_probe_boundary": _has(text, "立即停止", "stop") and "scout" in text,
    }


def _score_semantic(text: str) -> dict[str, bool]:
    return {
        "integrity_not_semantics": _has(text, "只证明执行身份", "只证明", "integrity pass")
        and _has(text, "语义", "semantic"),
        "implementation_confounded": _has(text, "implementation-confounded", "implementation_confounded"),
        "candidate_unresolved": "unresolved" in text and _has(text, "不能判负", "not reject"),
        "bounded_ceiling": _has(text, "run/cell", "diagnostic")
        and _has(text, "不能提升", "cannot promote"),
        "alignment_check": all(term in text for term in ("objective", "label", "output")),
        "constant_check": _has(text, "常量", "constant", "平凡", "trivial"),
        "identity_check": _has(text, "no-op", "identity"),
        "support_check": _has(text, "输出方差", "output support", "支持集", "占用"),
        "overfit_check": _has(text, "overfit", "过拟合"),
        "blocks_scaling": all(term in text for term in ("seeds", "models", "hyperparameters"))
        and _has(text, "不应继续", "不扩算力", "before"),
        "bounded_next_probe": "probe" in text and _has(text, "修正 loss", "修正目标", "corrected objective"),
        "harvest_disposition": _has(text, "invalidated", "amended")
        and _has(text, "no_durable_harvest_reason", "failure_mechanism", "evaluation_insight"),
    }


def _score_recovery(text: str) -> dict[str, bool]:
    hot_path = ("status", "adapter", "state/current", "portfolio/current", "harvest/current")
    positions = [text.find(term) for term in hot_path]
    return {
        "hot_path_order": all(position >= 0 for position in positions)
        and positions == sorted(positions),
        "explicit_lineage_precedence": _has(text, "amends", "invalidates", "显式")
        and "mtime" in text
        and _has(text, "不能", "不", "never"),
        "raw_artifact_retained": _has(text, "raw artifact", "原始 artifact", "旧 artifact")
        and _has(text, "可复现", "reproducible", "保留"),
        "old_interpretation_invalid": _has(text, "旧结论", "old interpretation", "thesis-grade")
        and _has(text, "invalid", "撤回", "无效"),
        "candidate_unresolved": "unresolved" in text,
        "bounded_history": _has(text, "不", "no", "only")
        and _has(text, "全历史", "whole history", "archaeology", "冲突", "audit"),
        "legal_next_action": "probe" in text or _has(text, "portfolio", "下一动作", "next action"),
    }


def score_response(case_id: str, path: Path) -> dict:
    response = _raw_response(path)
    scorers = {
        "probe-cost-boundary": _score_probe,
        "semantic-integrity-separation": _score_semantic,
        "recovery-current-precedence": _score_recovery,
    }
    if case_id not in scorers:
        raise ValueError(f"unsupported case: {case_id}")
    checks = scorers[case_id](response)
    return {
        "case_id": case_id,
        "checks": checks,
        "verdict": "PASS" if all(checks.values()) else "FAIL",
    }
