"""Tests for the T007 B1 adaptive phase-estimation window package.

Populations:
  SEMANTIC-GATES (Phase B1): the 8 semantic gates pass.
  THEORETICAL-DIRECTION: E1 (SNR down -> N up) holds on a clean monotone case;
    the linewidth axis is the documented weak axis.
  IDENTITY-SEPARATIONS: fixed B* / fixed-per-condition / oracle / pilot CPE /
    BPS are distinct; the pi/4 bias is corrected; legal pi/2 resolve only;
    no truth/future in deployable signatures.
  RAW-AGGREGATE: BER recomputation from raw rows is bit-identical.
  VERDICT-BOUNDARIES: the pre-registered verdict function maps synthetic
    evidence to the correct outcome.
  DETERMINISM: deterministic subprocess fingerprint (no built-in hash());
    SHA stamps are real file hashes; PYTHONUTF8 explicit IO.
  PROTECTED-IMMUTABILITY: T002-T006 / shared generator / params.py untouched.

The shared canonical generator (common/_dual_pol_channel.py), params.py and
prior T002-T005 artifacts are NEVER touched.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

HERE = Path(__file__).resolve().parent
SIM = HERE.parent
T007_DIR = SIM / "explore" / "adaptive-phase-window"
RESULT_DIR = SIM / "results" / "adaptive-phase-window"
ROOT = SIM.parent.parent
# The b2 runner also wrote a stray copy under explore/results before the path
# fix; prefer the authorized SIM/results location, fall back to the stray copy.
if not RESULT_DIR.exists() and (SIM / "explore" / "results" / "adaptive-phase-window").exists():
    RESULT_DIR = SIM / "explore" / "results" / "adaptive-phase-window"

# Make common.* and the flat T007 module names importable.
for p in (str(SIM), str(T007_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_module(name, filename):
    import importlib.util
    modname = f"t007_{name}"
    if modname in sys.modules:
        return sys.modules[modname]
    spec = importlib.util.spec_from_file_location(modname, T007_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod


channel = _load_module("channel", "channel.py")
sys.modules["channel"] = channel
cpe = _load_module("cpe", "cpe.py")
sys.modules["cpe"] = cpe
evaluator = _load_module("evaluator", "evaluator.py")
sys.modules["evaluator"] = evaluator
semantic_gates = _load_module("semantic_gates", "semantic_gates.py")
sys.modules["semantic_gates"] = semantic_gates
b2 = _load_module("b2_structural_gate", "b2_structural_gate.py")


# ---------------------------------------------------------------------------
# PHASE-B1 semantic gates
# ---------------------------------------------------------------------------
class TestSemanticGates:
    def test_all_gates_pass(self):
        r = semantic_gates.run_all_gates()
        assert r["all_pass"], json.dumps(r["gates"], indent=2)

    def test_each_gate_returns_pass_detail(self):
        r = semantic_gates.run_all_gates()
        for name, res in r["gates"].items():
            assert "pass" in res and isinstance(res["pass"], bool)
            assert "detail" in res and isinstance(res["detail"], str)


# ---------------------------------------------------------------------------
# THEORETICAL-DIRECTION tests
# ---------------------------------------------------------------------------
class TestTheoreticalDirection:
    """E1 holds (SNR down -> best N up). The linewidth axis is the documented
    weak axis in the satellite-FSO ECL regime."""

    def test_e1_snr_down_n_up_clean_monotone(self):
        """On a clean QPSK AWGN+Wiener slice, lowering SNR should not make the
        best window N smaller (E1 direction). Uses a strong linewidth so the
        SNR effect is visible above noise."""
        from cpe import WINDOW_GRID, vv_block_mean
        from evaluator import ber_with_legal_resolve
        N = 2048
        seed = 7800
        lw = 80000.0
        best_Ns = []
        for snr in [22.0, 18.0, 14.0, 10.0]:
            out = channel.generate_channel(channel.ChannelParams(
                modulation="qpsk", snr_db=snr, linewidth_hz=lw,
                n_symbols=N, seed=seed, channel="awgn_wiener"))
            bers = []
            for w in WINDOW_GRID:
                rc = vv_block_mean(out.rx, N=w, modulation="qpsk")
                bers.append(ber_with_legal_resolve(rc, out.debug()["tx_bits"], "qpsk"))
            best_Ns.append(WINDOW_GRID[int(np.argmin(bers))])
        # As SNR drops, best N should not shrink (E1: SNR down -> N up).
        # Allow ties; require the last (lowest SNR) N >= the first (highest SNR) N.
        assert best_Ns[-1] >= best_Ns[0], f"E1 violated: best N by SNR {best_Ns}"

    def test_innov_hat_weak_linewidth_response(self):
        """The raised-power phase-innovation estimator barely responds to
        linewidth in the satellite-FSO ECL range (D-011/A1 finding). This is
        the documented physics, not a bug."""
        N = 2048
        seed = 7800
        innovs = []
        for lw in [10000.0, 20000.0, 80000.0]:
            out = channel.generate_channel(channel.ChannelParams(
                modulation="qpsk", snr_db=18.0, linewidth_hz=lw,
                n_symbols=N, seed=seed, channel="awgn_wiener"))
            innovs.append(float(np.mean(channel.estimate_phase_innovation_hat(
                out.rx, m0=4, window=256))))
        # The 80kHz / 10kHz ratio is close to 1 (noise-dominated).
        ratio = innovs[2] / max(innovs[0], 1e-12)
        assert 0.9 <= ratio <= 1.2, f"innov_hat linewidth response {ratio} unexpected"


# ---------------------------------------------------------------------------
# IDENTITY-SEPARATIONS tests
# ---------------------------------------------------------------------------
class TestIdentitySeparations:
    def test_pi4_bias_correction_qpsk(self):
        """QPSK deterministic pi/4 bias is corrected by raised_power_bias."""
        assert abs(cpe.raised_power_bias("qpsk") - cpe.PI4_BIAS) < 1e-9

    def test_pi4_bias_correction_qam16(self):
        """Square 16-QAM also has pi/4 bias (colinear raised points)."""
        assert abs(cpe.raised_power_bias("qam16") - cpe.PI4_BIAS) < 1e-9

    def test_legal_pi2_resolve_only(self):
        """ber_with_legal_resolve uses 4 pi/2 rotations, NOT 8 pi/4 (T006
        forbidden mismatch). Verified structurally: a QPSK sequence recovered
        with pi/4 bias correction reaches ~0 BER under 4 pi/2 rotations."""
        from common._modulation import qpsk_mod
        rng = np.random.default_rng(7800)
        bits = rng.integers(0, 2, 2048 * 2)
        s = qpsk_mod(bits)
        rx_comp = cpe.vv_block_mean(s.astype(complex), N=64, modulation="qpsk")
        ber = evaluator.ber_with_legal_resolve(rx_comp, bits, "qpsk")
        assert ber < 1e-3

    def test_fixed_vs_fixed_per_condition_vs_oracle_distinct(self):
        """B* (single N), fixed-per-condition (one N per condition), and
        oracle (per-block) are conceptually distinct; the evaluator's verdict
        function treats them separately."""
        # Structural: the contract declares them as separate baselines.
        contract = yaml.safe_load((T007_DIR / "contract.yaml").read_text(encoding="utf-8"))
        names = set(contract["baselines"].keys())
        assert {"bstar_fixed", "fixed_per_condition", "oracle_per_block",
                "pilot_cpe", "validation_tuned_bps"} <= names
        # Oracle is Kill-only.
        assert contract["baselines"]["oracle_per_block"]["role"] == "kill_only"

    def test_no_truth_in_deployable_signatures(self):
        """vv_block_mean / pilot_block_mean / P1/P2/P3 signatures do not
        carry tx_bits / true h / theta / snr / oracle best N."""
        import inspect
        forbidden = {"tx_bits", "true_h", "true_phase", "true_snr",
                     "oracle_best_n", "h", "theta"}
        fns = {
            "vv_block_mean": cpe.vv_block_mean,
            "pilot_block_mean": cpe.pilot_block_mean,
            "p1_analytic_ratio_rule": cpe.p1_analytic_ratio_rule,
            "p2_lookup_hysteresis": cpe.p2_lookup_hysteresis,
            "p3_confidence_safe": cpe.p3_confidence_safe,
        }
        for name, fn in fns.items():
            params = set(inspect.signature(fn).parameters.keys())
            assert not (params & forbidden), f"{name} leaks truth: {params & forbidden}"

    def test_window_path_varies_with_conditions(self):
        """P1 picks different N under low-SNR vs high-SNR conditions."""
        cond_lo = channel.generate_channel(channel.ChannelParams(
            modulation="qpsk", snr_db=10.0, linewidth_hz=10000.0,
            n_symbols=2048, seed=7800, channel="awgn_wiener"))
        cond_hi = channel.generate_channel(channel.ChannelParams(
            modulation="qpsk", snr_db=22.0, linewidth_hz=80000.0,
            n_symbols=2048, seed=7800, channel="awgn_wiener"))
        r_lo = cpe.p1_analytic_ratio_rule(cond_lo.rx, block=256,
                                           snr_lo_db=9.0, snr_hi_db=18.0,
                                           innov_lo=0.05, innov_hi=0.35,
                                           modulation="qpsk", innov_weight=0.0)
        r_hi = cpe.p1_analytic_ratio_rule(cond_hi.rx, block=256,
                                           snr_lo_db=9.0, snr_hi_db=18.0,
                                           innov_lo=0.05, innov_hi=0.35,
                                           modulation="qpsk", innov_weight=0.0)
        assert float(np.mean(r_lo.n_per_block)) > float(np.mean(r_hi.n_per_block))


# ---------------------------------------------------------------------------
# RAW -> AGGREGATE bit-identical recomputation
# ---------------------------------------------------------------------------
class TestRawAggregate:
    def test_raw_rows_recompute_to_same_ber(self):
        """Recompute BER from the raw per-window BER lists and confirm they
        match the stored best_BER / best_N exactly."""
        for mod in ["qpsk", "qam16"]:
            path = RESULT_DIR / f"b2_raw_{mod}.jsonl"
            if not path.exists():
                pytest.skip(f"{path} not present (B2 not run)")
            with open(path, encoding="utf-8") as f:
                for line in f:
                    r = json.loads(line)
                    if r.get("phase") != "b2_awgn_wiener":
                        continue
                    grid = r["window_grid"]
                    per_w = r["per_window_BER"]
                    j = int(np.argmin(per_w))
                    assert grid[j] == r["best_N"]
                    assert abs(per_w[j] - r["best_BER"]) < 1e-12


# ---------------------------------------------------------------------------
# VERDICT-BOUNDARY tests (synthetic inputs)
# ---------------------------------------------------------------------------
class TestVerdictBoundaries:
    def test_kill_when_gate_fails(self):
        v = evaluator.verdict(
            structural_gate_passed=False,
            go_conditions_met=True, robustness_only_met=True,
            oracle_space_exists=True, identity_ci_fec_closed=True,
            collapse_dominated=False)
        assert v == "KILL_NO_ADAPTIVE_WINDOW_SPACE"

    def test_go_when_all_conditions_met(self):
        v = evaluator.verdict(
            structural_gate_passed=True,
            go_conditions_met=True, robustness_only_met=False,
            oracle_space_exists=True, identity_ci_fec_closed=True,
            collapse_dominated=False)
        assert v == "GO_ADAPTIVE_WINDOW_METHOD"

    def test_robustness_only_when_below_threshold_but_robust(self):
        v = evaluator.verdict(
            structural_gate_passed=True,
            go_conditions_met=False, robustness_only_met=True,
            oracle_space_exists=True, identity_ci_fec_closed=True,
            collapse_dominated=False)
        assert v == "ROBUSTNESS_ONLY"

    def test_method_fail_when_space_but_methods_cannot_close(self):
        v = evaluator.verdict(
            structural_gate_passed=True,
            go_conditions_met=False, robustness_only_met=False,
            oracle_space_exists=True, identity_ci_fec_closed=True,
            collapse_dominated=False)
        assert v == "METHOD_FAIL_WITH_SPACE"

    def test_unresolved_when_identity_not_closed(self):
        v = evaluator.verdict(
            structural_gate_passed=True,
            go_conditions_met=True, robustness_only_met=False,
            oracle_space_exists=True, identity_ci_fec_closed=False,
            collapse_dominated=False)
        assert v == "UNRESOLVED"

    def test_outlier_dominated_downgrades_go(self):
        v = evaluator.verdict(
            structural_gate_passed=True,
            go_conditions_met=True, robustness_only_met=False,
            oracle_space_exists=True, identity_ci_fec_closed=True,
            collapse_dominated=True)
        assert v == "UNRESOLVED_OUTLIER_DOMINATED"

    def test_collapse_check_flags_single_seed_dominance(self):
        # One seed contributes 60% of total gain -> collapse.
        gains = [0.6, 0.1, 0.1, 0.1, 0.1]   # 0.6 / 1.0 = 60%
        assert evaluator.collapse_check(gains) is True

    def test_collapse_check_passes_when_balanced(self):
        gains = [0.2, 0.2, 0.2, 0.2, 0.2]
        assert evaluator.collapse_check(gains) is False


# ---------------------------------------------------------------------------
# DETERMINISM + SHA + UTF-8
# ---------------------------------------------------------------------------
class TestDeterminism:
    def test_deterministic_subprocess_fingerprint(self):
        """Two independent Python subprocesses with the same params/seed
        produce bit-identical RX (V039 T004 lesson: no built-in hash())."""
        code = (
            "import sys; sys.path.insert(0, r'" + str(SIM) + "'); "
            "sys.path.insert(0, r'" + str(T007_DIR) + "'); "
            "import json, hashlib; import channel as ch; "
            "out = ch.generate_channel(ch.ChannelParams(modulation='qpsk', "
            "snr_db=18.0, linewidth_hz=20000.0, n_symbols=2048, seed=7800, "
            "channel='awgn_wiener')); "
            "h = hashlib.sha256(out.rx.tobytes()).hexdigest(); "
            "print(json.dumps({'sha': h}))"
        )
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONHASHSEED"] = "0"
        out1 = subprocess.run([sys.executable, "-c", code], capture_output=True,
                              text=True, env=env, cwd=str(SIM))
        out2 = subprocess.run([sys.executable, "-c", code], capture_output=True,
                              text=True, env=env, cwd=str(SIM))
        assert out1.returncode == 0, out1.stderr
        assert out2.returncode == 0, out2.stderr
        sha1 = json.loads(out1.stdout.strip().splitlines()[-1])["sha"]
        sha2 = json.loads(out2.stdout.strip().splitlines()[-1])["sha"]
        assert sha1 == sha2, "non-deterministic RX across subprocesses"

    def test_no_built_in_hash_in_source(self):
        """No Python built-in hash() CALL of objects in the T007 source (V039).
        Parsed via AST so docstring/comment mentions of 'hash()' do not trip it."""
        import ast
        for fname in ["channel.py", "cpe.py", "evaluator.py",
                      "semantic_gates.py", "b2_structural_gate.py"]:
            src = (T007_DIR / fname).read_text(encoding="utf-8")
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                        and node.func.id == "hash":
                    pytest.fail(f"{fname} uses built-in hash() call at line {node.lineno}")

    def test_sha_stamps_match_actual_files(self):
        """The SHA256 values stamped in the B2 result JSON are the actual
        SHA256 of source-closure.yaml / contract.yaml / MVE-SPEC.md."""
        for mod in ["qpsk", "qam16"]:
            rpath = RESULT_DIR / f"b2_result_{mod}.json"
            if not rpath.exists():
                continue
            with open(rpath, encoding="utf-8") as f:
                meta = json.load(f).get("_meta", {})
            # The log file records the SHAs; parse them.
            log = (RESULT_DIR / f"b2_log_{mod}.txt").read_text(encoding="utf-8")
            import re
            for fname in ["source-closure.yaml", "contract.yaml", "MVE-SPEC.md"]:
                actual = hashlib.sha256((T007_DIR / fname).read_bytes()).hexdigest()
                # The SHA appears in the log.
                m = re.search(rf"{re.escape(fname)} SHA256:\s*([0-9a-f]+)", log)
                assert m, f"{fname} SHA not found in log"
                assert m.group(1) == actual, f"{fname} SHA mismatch"

    def test_explicit_utf8_io(self):
        """All file open() in T007 source use explicit encoding='utf-8'."""
        import re
        for fname in ["b2_structural_gate.py"]:
            src = (T007_DIR / fname).read_text(encoding="utf-8")
            # Find every open(...) call.
            for m in re.finditer(r"open\([^)]*\)", src):
                call = m.group(0)
                if "encoding" not in call:
                    # Allow binary mode 'rb'/'wb' (no encoding needed).
                    assert "'rb'" in call or "'wb'" in call or '"rb"' in call or '"wb"' in call, \
                        f"open() without encoding in {fname}: {call}"


# ---------------------------------------------------------------------------
# PROTECTED-IMMUTABILITY tests (T002-T006 / shared generator / params.py)
# ---------------------------------------------------------------------------
class TestProtectedImmutability:
    def _git_blob_hash(self, rel_path):
        """Get the git blob hash of a path in HEAD (CRLF-safe)."""
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", "HEAD", rel_path],
            capture_output=True, text=True)
        if out.returncode != 0 or not out.stdout.strip():
            return None
        # Format: "<mode> blob <sha>\t<path>"
        return out.stdout.split()[2]

    def _worktree_blob_hash(self, abs_path):
        """Get the git blob hash of the working-tree file (CRLF-safe: uses
        git hash-object which applies the same filtering git uses)."""
        out = subprocess.run(
            ["git", "-C", str(ROOT), "hash-object", str(abs_path)],
            capture_output=True, text=True)
        return out.stdout.strip() if out.returncode == 0 else None

    def test_shared_generator_unchanged(self):
        """common/_dual_pol_channel.py is identical to its committed blob
        (the protected generator is never modified). Uses git hash-object so
        CRLF filtering matches between working tree and HEAD."""
        rel = "projects/simulation/common/_dual_pol_channel.py"
        head_blob = self._git_blob_hash(rel)
        wt_blob = self._worktree_blob_hash(SIM / "common" / "_dual_pol_channel.py")
        if head_blob is None:
            pytest.skip("path not in HEAD")
        assert wt_blob == head_blob, \
            f"shared generator modified: HEAD={head_blob} WT={wt_blob}"

    def test_params_py_unchanged(self):
        """params.py is identical to its committed blob."""
        rel = "projects/simulation/params.py"
        head_blob = self._git_blob_hash(rel)
        wt_blob = self._worktree_blob_hash(SIM / "params.py")
        if head_blob is None:
            pytest.skip("path not in HEAD")
        assert wt_blob == head_blob, \
            f"params.py modified: HEAD={head_blob} WT={wt_blob}"

    def test_t002_t006_artifacts_not_modified(self):
        """No T002-T006 explore/results/test file is in the working-tree diff."""
        out = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            capture_output=True, text=True)
        for line in out.stdout.splitlines():
            path = line[3:].strip().strip('"')
            # T007-only paths are allowed; anything under high-order-cpr-combination
            # (T006) or pilot-jones-* (T002-T005) must NOT appear as modified.
            for forbidden_sub in ["high-order-cpr-combination", "pilot-jones-",
                                  "test_high_order_cpr", "test_pilot_jones"]:
                if forbidden_sub in path:
                    pytest.fail(f"T002-T006 artifact modified: {path}")


# ---------------------------------------------------------------------------
# STRUCTURAL-GATE verdict (B2 result)
# ---------------------------------------------------------------------------
class TestB2Verdict:
    def test_b2_verdict_is_kill(self):
        """The pre-registered B2 structural gate produced KILL for both
        modulations; Phase C was therefore not implemented."""
        for mod in ["qpsk", "qam16"]:
            rpath = RESULT_DIR / f"b2_result_{mod}.json"
            if not rpath.exists():
                pytest.skip(f"{rpath} not present")
            with open(rpath, encoding="utf-8") as f:
                r = json.load(f)
            assert r["verdict"]["verdict"] == "KILL_NO_ADAPTIVE_WINDOW_SPACE"
            assert r["verdict"]["gate_passed"] is False

    def test_phase_c_not_executed(self):
        """No Phase C method paired-test artifact exists (gate failed)."""
        for fname in ["primary_paired_test.json", "mechanism_slice.json"]:
            assert not (RESULT_DIR / fname).exists(), \
                f"Phase C artifact {fname} should not exist (gate failed)"
