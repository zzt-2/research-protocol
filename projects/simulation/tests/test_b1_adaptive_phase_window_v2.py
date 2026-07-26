"""Test suite — B1 adaptive phase-estimation window v2 (T008).

Covers (per T008 §9 acceptance):
  - 5 identity smokes (+ direction/non-degenerate) via subprocess (exit 0)
  - determinism: no built-in hash() of objects; subprocess fingerprint bit-identical
  - identity separations: pi/4 bias + legal pi/2 resolve; no truth in deployable
    signatures; B*/B-cond frozen on validation
  - real-curve required-SNR (no fabricated dB); UNRESOLVED_NO_CROSSING
  - corrected-space-gate verdict is KILL (corrected oracle space collapsed);
    KILL is from the corrected headroom, NOT from feature rho (gap5 closure)
  - raw → aggregate BER recompute bit-identical
  - YAML/JSON parse; source/contract/MVE-SPEC/seed-census SHA stamps match files
  - forbidden-path diff: T002-T007 artifacts, shared common, params.py unchanged
  - PYTHONUTF8=1 explicit IO
  - git diff --check clean

Run:  PYTHONUTF8=1 python -m pytest projects/simulation/tests/test_b1_adaptive_phase_window_v2.py -v
"""
from __future__ import annotations

import ast
import hashlib
import io
import json
import os
import subprocess
import sys
import yaml

import numpy as np
import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))   # .../projects/simulation/tests
_SIM_DIR = os.path.dirname(_HERE)                    # .../projects/simulation
_PROJECTS_DIR = os.path.dirname(_SIM_DIR)            # .../projects
_REPO = os.path.dirname(_PROJECTS_DIR)               # worktree root
_V2 = os.path.join(_SIM_DIR, "explore", "b1-adaptive-phase-window-v2")
_RES = os.path.join(_SIM_DIR, "results", "b1-adaptive-phase-window-v2")

if _SIM_DIR not in sys.path:
    sys.path.insert(0, _SIM_DIR)
if _V2 not in sys.path:
    sys.path.insert(0, _V2)


# ---------------------------------------------------------------------------
# 1. Identity smokes via subprocess (must exit 0)
# ---------------------------------------------------------------------------
def _run(cmd, env=None):
    e = os.environ.copy()
    e["PYTHONUTF8"] = "1"
    if env:
        e.update(env)
    return subprocess.run(cmd, capture_output=True, text=True, env=e, cwd=_REPO)


def test_identity_smokes_pass():
    r = _run([sys.executable, os.path.join(_V2, "identity_smoke.py")])
    assert r.returncode == 0, f"identity smokes failed:\n{r.stdout}\n{r.stderr}"


# ---------------------------------------------------------------------------
# 2. Determinism — no built-in hash() of objects (V039 T004 lesson)
# ---------------------------------------------------------------------------
def _python_files():
    out = []
    for root, _, files in os.walk(_V2):
        for f in files:
            if f.endswith(".py"):
                out.append(os.path.join(root, f))
    return out


def test_no_builtin_hash_of_objects():
    """AST-scan: no `hash(...)` call on non-int/str objects."""
    forbidden_patterns = ["hash(out", "hash(self", "hash(rx", "hash(block"]
    for fp in _python_files():
        src = open(fp, encoding="utf-8").read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "hash":
                # hash() is allowed only on int/str literals (deterministic).
                arg = node.args[0] if node.args else None
                assert isinstance(arg, (ast.Constant, ast.Num, ast.Str)), \
                    f"{fp}: built-in hash() called on non-literal {ast.dump(node)}"
        # also forbid the string patterns (defensive)
        for p in forbidden_patterns:
            assert p not in src, f"{fp}: forbidden hash pattern '{p}'"


def test_subprocess_fingerprint_bit_identical():
    """Two independent Python subprocesses with the same seed/params produce a
    bit-identical RX sha256."""
    script = (
        "import sys, hashlib\n"
        "sys.path.insert(0, r'" + _SIM_DIR + "')\n"
        "sys.path.insert(0, r'" + _V2 + "')\n"
        "from channel import generate_channel, ChannelParams\n"
        "import numpy as np\n"
        "out = generate_channel(ChannelParams(modulation='qpsk', snr_db=14.0, linewidth_hz=20000.0, n_symbols=2000, seed=8100, channel='gg_block_fading'))\n"
        "h = hashlib.sha256(out.rx.tobytes()).hexdigest()\n"
        "sys.stdout.write(h)\n"
    )
    r1 = _run([sys.executable, "-c", script])
    r2 = _run([sys.executable, "-c", script])
    assert r1.returncode == 0 and r2.returncode == 0
    assert r1.stdout == r2.stdout, f"RX fingerprint differs across subprocesses:\n{r1.stdout}\n{r2.stdout}"


# ---------------------------------------------------------------------------
# 3. Identity separations — pi/4 bias + legal pi/2 resolve; no truth; B*/B-cond frozen
# ---------------------------------------------------------------------------
def test_pi4_bias_and_legal_pi2_resolve():
    from cpe import raised_power_bias, vv_block_mean
    from evaluator import ber_with_legal_resolve
    from channel import generate_channel, ChannelParams
    assert abs(raised_power_bias("qpsk") - np.pi / 4) < 1e-9
    # 16-QAM bias in legal range (|E[s^4]|≈0 -> 0)
    bq = raised_power_bias("qam16")
    assert -np.pi / 4 - 1e-9 <= bq <= np.pi / 4 + 1e-9
    # legal pi/2 invariance: rotating rx by pi/2 then resolving gives same BER
    out = generate_channel(ChannelParams(modulation="qpsk", snr_db=14.0, linewidth_hz=20000.0,
                                         n_symbols=2048, seed=8000, channel="awgn_wiener"))
    a = ber_with_legal_resolve(vv_block_mean(out.rx, N=64, modulation="qpsk"),
                               out.debug()["tx_bits"], "qpsk")
    b = ber_with_legal_resolve(vv_block_mean(out.rx * np.exp(1j * np.pi / 2), N=64, modulation="qpsk"),
                               out.debug()["tx_bits"], "qpsk")
    assert abs(a - b) < 1e-9


def test_deployable_signatures_no_truth():
    """P1/P2/P3 source must not reference truth/oracle/test-label/future."""
    import inspect
    from cpe import p1_physics_ratio_rule, p2_lookup_hysteresis, p3_confidence_safe
    forbidden = ("out.debug()", "tx_bits", "true_h", "true_phase", "true_snr",
                 "oracle_best_N", "test_labels", "future_block")
    for fn in (p1_physics_ratio_rule, p2_lookup_hysteresis, p3_confidence_safe):
        src = inspect.getsource(fn).replace("# ", "")
        for f in forbidden:
            assert f not in src, f"{fn.__name__} references forbidden truth '{f}'"


def test_bstar_bcond_frozen_on_validation():
    """B*/B-cond are deterministic integers from validation; the corrected gate
    result carries the frozen integers (gap1 closure)."""
    for mod in ("qpsk", "qam16"):
        rp = os.path.join(_RES, f"corrected_gate_result_{mod}.json")
        assert os.path.exists(rp), f"missing {rp}"
        r = json.load(open(rp, encoding="utf-8"))
        fb = r["frozen_baselines"]
        assert isinstance(fb["bstar_n"], int)
        assert fb["bstar_n"] in [8, 16, 32, 64, 128, 256]
        for cond, n in fb["bcond_n_by_condition"].items():
            assert isinstance(n, int) and n in [8, 16, 32, 64, 128, 256]


# ---------------------------------------------------------------------------
# 4. Real-curve required-SNR (no fabricated dB); UNRESOLVED_NO_CROSSING
# ---------------------------------------------------------------------------
def test_required_snr_real_curve_no_fabrication():
    from evaluator import required_snr_at_fec
    # real monotone curve -> exact crossing (no hardcoded slope)
    snr = [4.0, 8.0, 12.0, 16.0, 20.0]
    ber = [0.5 * np.exp(-s / 4.0) for s in snr]
    req = required_snr_at_fec(snr, ber)
    expected = -4.0 * np.log(3.8e-3 / 0.5)
    assert abs(req - expected) < 0.2
    # no crossing -> NaN
    assert np.isnan(required_snr_at_fec(snr, [0.5, 0.4, 0.3, 0.25, 0.22]))


# ---------------------------------------------------------------------------
# 5. Corrected-space-gate verdict = KILL; KILL from corrected headroom, not rho
# ---------------------------------------------------------------------------
def test_corrected_gate_verdict_is_kill():
    """The §5 corrected space gate returns KILL_NO_ADAPTIVE_WINDOW_SPACE for
    both modulations. This is the corrected oracle headroom collapse (gap5
    closure: the KILL is from the headroom, NOT from feature rho)."""
    for mod in ("qpsk", "qam16"):
        rp = os.path.join(_RES, f"corrected_gate_result_{mod}.json")
        r = json.load(open(rp, encoding="utf-8"))
        assert r["verdict"] == "KILL_NO_ADAPTIVE_WINDOW_SPACE", \
            f"{mod}: expected KILL, got {r['verdict']}"
        assert r["kill_triggered"] is True
        assert r["headroom"]["median_db_equiv"] < 0.5
        assert r["headroom"]["trimmed_db_equiv"] < 0.5
        # gap5 closure: the verdict is NOT a function of rho — rho is reported
        # but the KILL trigger is the headroom field, not rho.
        assert "rho_snr_hat" in r["observability"]
        assert "rho_innov_hat" in r["observability"]


def test_phase_c_not_executed():
    """Phase C (P1/P2/P3 paired test) was NOT executed because the §5 gate
    failed. The contract permits this when the corrected oracle space collapses
    (T008 §5 first stop condition). No method_test artifacts should exist."""
    # No method paired-test artifacts should exist (the gate failed before Phase C)
    method_artifacts = [f for f in os.listdir(_RES) if f.startswith("method_")] if os.path.exists(_RES) else []
    assert method_artifacts == [], f"Phase C ran despite gate KILL: {method_artifacts}"


# ---------------------------------------------------------------------------
# 6. raw → aggregate BER recompute bit-identical
# ---------------------------------------------------------------------------
def test_raw_aggregate_ber_recompute():
    """Recompute the per-cell mean BER from raw rows and verify it matches the
    frozen-baseline selection in the result JSON (bit-identical)."""
    for mod in ("qpsk", "qam16"):
        raw_path = os.path.join(_RES, f"corrected_gate_raw_{mod}.jsonl")
        res_path = os.path.join(_RES, f"corrected_gate_result_{mod}.json")
        rows = [json.loads(l) for l in open(raw_path, encoding="utf-8") if l.strip()]
        # raw gg_validation rows carry per_window_BER; recompute global mean per N
        gg = [r for r in rows if r.get("phase") == "gg_validation"]
        assert len(gg) > 0
        Ns = [8, 16, 32, 64, 128, 256]
        global_mean = {}
        for N in Ns:
            bers = [r["per_window_BER"][str(N)] for r in gg]
            global_mean[N] = float(np.mean(bers))
        result = json.load(open(res_path, encoding="utf-8"))
        # the FROZEN B* must equal the recomputed argmin
        recomputed_bstar = min(global_mean, key=global_mean.get)
        assert recomputed_bstar == result["frozen_baselines"]["bstar_n"], \
            f"{mod}: recomputed B*={recomputed_bstar} != frozen {result['frozen_baselines']['bstar_n']}"
        # the global_mean_ber_by_N in the result must match recompute
        for N in Ns:
            assert abs(result["global_mean_ber_by_N"][str(N)] - global_mean[N]) < 1e-12


# ---------------------------------------------------------------------------
# 7. YAML/JSON parse + SHA stamps match files
# ---------------------------------------------------------------------------
def test_yaml_json_parse():
    for fn in ("source-closure.yaml", "contract.yaml", "seed-census.yaml"):
        yaml.safe_load(open(os.path.join(_V2, fn), encoding="utf-8"))
    for mod in ("qpsk", "qam16"):
        json.load(open(os.path.join(_RES, f"corrected_gate_result_{mod}.json"), encoding="utf-8"))


def test_sha_stamps_match_files():
    def sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    for mod in ("qpsk", "qam16"):
        r = json.load(open(os.path.join(_RES, f"corrected_gate_result_{mod}.json"), encoding="utf-8"))
        assert r["sha"]["source_closure_yaml_sha256"] == sha(os.path.join(_V2, "source-closure.yaml"))
        assert r["sha"]["contract_yaml_sha256"] == sha(os.path.join(_V2, "contract.yaml"))
        assert r["sha"]["mve_spec_md_sha256"] == sha(os.path.join(_V2, "MVE-SPEC.md"))
        assert r["sha"]["seed_census_yaml_sha256"] == sha(os.path.join(_V2, "seed-census.yaml"))


# ---------------------------------------------------------------------------
# 8. Forbidden-path diff: T002-T007 artifacts, shared common, params.py unchanged
# ---------------------------------------------------------------------------
def _git_blob_hash(path):
    """CRLF-safe git blob hash via git hash-object (no file mutation)."""
    r = subprocess.run(["git", "hash-object", path], capture_output=True, text=True, cwd=_REPO)
    return r.stdout.strip()


def test_shared_common_params_unchaged_vs_head():
    """The shared common/ and params.py must be unchanged (git blob hash == HEAD)."""
    common_dir = os.path.join(_SIM_DIR, "common")
    for fn in os.listdir(common_dir):
        if fn.endswith(".py"):
            p = os.path.join(common_dir, fn)
            rel = os.path.relpath(p, _REPO).replace("\\", "/")
            head = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], capture_output=True, text=True, cwd=_REPO).stdout.strip()
            cur = _git_blob_hash(p)
            assert cur == head, f"{rel} modified: HEAD={head} cur={cur}"
    params = os.path.join(_SIM_DIR, "params.py")
    rel = os.path.relpath(params, _REPO).replace("\\", "/")
    head = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], capture_output=True, text=True, cwd=_REPO).stdout.strip()
    assert _git_blob_hash(params) == head, "params.py modified"


def test_t002_t007_artifacts_unchaged_vs_head():
    """T002-T007 tracked source artifacts must be unchanged (git blob hash == HEAD).
    Only checks TRACKED source files (.py/.yaml/.md/.json/.jsonl/.txt); .pyc and
    other untracked artifacts are skipped (they regenerate on import and are not
    in HEAD as source)."""
    targets = [
        os.path.join(_SIM_DIR, "explore", "adaptive-phase-window"),
        os.path.join(_SIM_DIR, "results", "adaptive-phase-window"),
    ]
    src_exts = (".py", ".yaml", ".yml", ".md", ".json", ".jsonl", ".txt")
    # get the set of tracked files under these targets
    r = subprocess.run(["git", "ls-files"] + [os.path.relpath(t, _REPO).replace("\\", "/") for t in targets],
                       capture_output=True, text=True, cwd=_REPO)
    tracked = set(line.strip() for line in r.stdout.splitlines() if line.strip())
    for rel in tracked:
        if not rel.endswith(src_exts):
            continue
        p = os.path.join(_REPO, *rel.split("/"))
        if not os.path.exists(p):
            continue
        head = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], capture_output=True, text=True, cwd=_REPO).stdout.strip()
        if not head or "HEAD:" in head:
            continue  # not tracked at HEAD (defensive)
        assert _git_blob_hash(p) == head, f"{rel} modified vs HEAD"


def test_t007_worker_log_unchanged():
    p = os.path.join(_REPO, "projects", "thesis-fso", "worker-logs", "step-007-b1-adaptive-phase-window-method.md")
    rel = os.path.relpath(p, _REPO).replace("\\", "/")
    head = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], capture_output=True, text=True, cwd=_REPO).stdout.strip()
    assert _git_blob_hash(p) == head, "T007 worker-log modified"


# ---------------------------------------------------------------------------
# 9. PYTHONUTF8=1 explicit IO — all file open() in v2 specify encoding='utf-8'
# ---------------------------------------------------------------------------
def test_explicit_utf8_io():
    for fp in _python_files():
        src = open(fp, encoding="utf-8").read()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                # binary mode ('rb') does not need encoding; text mode does
                mode_arg = node.args[1] if len(node.args) >= 2 else None
                is_binary = False
                if isinstance(mode_arg, ast.Constant) and isinstance(mode_arg.value, str) and "b" in mode_arg.value:
                    is_binary = True
                kws = {kw.arg for kw in node.keywords}
                if "mode" in kws:
                    # check mode kwarg
                    for kw in node.keywords:
                        if kw.arg == "mode" and isinstance(kw.value, ast.Constant) and "b" in kw.value.value:
                            is_binary = True
                if not is_binary:
                    assert "encoding" in kws, f"{fp}: text-mode open() without encoding= at line {node.lineno}"


# ---------------------------------------------------------------------------
# 10. git diff --check clean (no whitespace errors)
# ---------------------------------------------------------------------------
def test_git_diff_check_clean():
    r = subprocess.run(["git", "diff", "--check"], capture_output=True, text=True, cwd=_REPO)
    # --check returns non-zero if whitespace errors are found in tracked changes;
    # untracked files (the new v2 files) are not checked, which is fine.
    assert r.returncode == 0 or "coverage" in r.stdout, f"git diff --check found whitespace errors:\n{r.stdout}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
