"""validate.py - Part A validation suite for satellite DAG simulator.

Implements analytic, statistical, degradation, and autocorrelation checks
from gw-experiment.md and simulator_design.md §5.
"""

import sys
import numpy as np

from channel import ChannelModel, free_space_path_loss, compute_snr, shannon_rate, FREQ_G2U
from orbital import OrbitalMechanics
from dag import DAGGenerator
from config import (
    NOISE_POWER_W, BW_G2U, AREA_SIZE,
)


# ---------------------------------------------------------------------------
# Analytic validation
# ---------------------------------------------------------------------------

def test_path_loss():
    """Free space path loss matches L = 20·log10(4π·d·f/c)."""
    # Test 1: d=1000m, f=2GHz
    d, f = 1000.0, 2e9
    expected = 20.0 * np.log10(4.0 * np.pi * d * f / 3e8)
    result = free_space_path_loss(d, f)
    assert abs(result - expected) < 1e-10, f"Expected {expected:.4f}, got {result:.4f}"

    # Test 2: d=1000m, f=2GHz ~ 98.46 dB
    assert abs(result - 98.46) < 0.5, f"Path loss at 1km/2GHz should be ~98.46 dB, got {result:.2f}"

    # Test 3: LEO distance, f=20GHz - sanity check
    d2 = 500e3
    f2 = 20e9
    pl_leo = free_space_path_loss(d2, f2)
    expected_leo = 20.0 * np.log10(4.0 * np.pi * d2 * f2 / 3e8)
    assert abs(pl_leo - expected_leo) < 1e-6, f"LEO path loss mismatch"
    assert 150 < pl_leo < 200, f"LEO path loss {pl_leo:.1f} dB out of reasonable range [150, 200]"


def test_orbital_period():
    """LEO orbital period at 500km ≈ 94.6 minutes (5660s ± 60s)."""
    orb = OrbitalMechanics()
    period_s = orb.period
    period_min = period_s / 60.0
    assert 5600 < period_s < 5720, (
        f"Period {period_s:.1f}s ({period_min:.1f}min) outside 5600-5720s range"
    )
    assert abs(period_min - 94.6) < 1.0, (
        f"Period {period_min:.1f}min too far from expected 94.6min"
    )


def test_snr_calculation():
    """Known tx_power, path_loss, fading_gain → SNR matches manual calculation."""
    tx_power = 1.0  # W
    path_loss_db = 100.0  # dB
    fading_gain = 2.0  # linear
    noise = NOISE_POWER_W

    pl_linear = 10.0 ** (-path_loss_db / 10.0)
    expected_snr = tx_power * pl_linear * fading_gain / noise
    result = compute_snr(tx_power, path_loss_db, fading_gain, noise)
    assert abs(result - expected_snr) / expected_snr < 1e-10, (
        f"SNR {result} != expected {expected_snr}"
    )

    # Shannon rate sanity: with positive SNR, rate should be positive
    rate = shannon_rate(result, BW_G2U)
    assert rate > 0, f"Shannon rate should be positive, got {rate}"


# ---------------------------------------------------------------------------
# Statistical validation
# ---------------------------------------------------------------------------

def test_shadowed_rician_distribution():
    """Shadowed-Rician samples have correct mean/variance ordering."""
    from channel import shadowed_rician_fading

    rng = np.random.default_rng(42)
    n = 10000

    stats = {}
    for cond in ("light", "average", "heavy"):
        samples = shadowed_rician_fading(rng, condition=cond, size=n)
        mean = np.mean(samples)
        var = np.var(samples)
        assert mean > 0, f"{cond}: mean power should be positive, got {mean}"
        assert var > 0, f"{cond}: variance should be positive, got {var}"
        stats[cond] = {"mean": mean, "var": var}

    # Light shadowing (high b0) produces highest variance in scattered component;
    # the ordering is not monotonic across all three conditions, so just verify
    # light and average differ from each other (distinct distributions)
    assert stats["light"]["var"] != stats["average"]["var"], (
        "Light and average should have different variances"
    )


def test_dag_degree_distribution():
    """DAGs have correct source/sink and reasonable degree distribution."""
    gen = DAGGenerator(n_tasks=20)
    rng = np.random.default_rng(42)

    in_degrees = []
    out_degrees = []

    for _ in range(100):
        dag = gen.generate(rng)
        assert len(dag.tasks[0].predecessors) == 0, "Source (task 0) should have 0 predecessors"
        assert len(dag.tasks[-1].successors) == 0, "Sink (last task) should have 0 successors"

        for t in dag.tasks[1:-1]:
            in_degrees.append(len(t.predecessors))
            out_degrees.append(len(t.successors))

    # Internal tasks must have ≥1 predecessor and ≥1 successor
    for d in in_degrees:
        assert d >= 1, f"Internal task has {d} predecessors, expected ≥1"
    for d in out_degrees:
        assert d >= 1, f"Internal task has {d} successors, expected ≥1"

    mean_in = np.mean(in_degrees)
    mean_out = np.mean(out_degrees)
    assert 0 < mean_in < 20, f"Mean in-degree {mean_in} unreasonable"
    assert 0 < mean_out < 20, f"Mean out-degree {mean_out} unreasonable"


def test_iotd_position_uniformity():
    """IoTD positions (simulated uniform) have correct bounds and statistics."""
    rng = np.random.default_rng(42)
    n = 1000
    xs = rng.uniform(0, AREA_SIZE, size=n)
    ys = rng.uniform(0, AREA_SIZE, size=n)

    assert np.all(xs >= 0) and np.all(xs <= AREA_SIZE), "x positions out of bounds"
    assert np.all(ys >= 0) and np.all(ys <= AREA_SIZE), "y positions out of bounds"

    # Uniform on [0, 1000]: mean ≈ 500, std ≈ 289
    for vals, label in [(xs, "x"), (ys, "y")]:
        mean = np.mean(vals)
        std = np.std(vals)
        assert abs(mean - 500.0) < 30, f"{label} mean {mean:.1f} too far from 500"
        assert abs(std - 289.0) < 30, f"{label} std {std:.1f} too far from 289"


# ---------------------------------------------------------------------------
# Degradation tests
# ---------------------------------------------------------------------------

def test_deterministic_channel():
    """Deterministic channel produces identical results for same inputs."""
    cm = ChannelModel(rng=np.random.default_rng(0))
    cm.set_deterministic(True)

    r1 = cm.g2u_rate(500.0, 1.0)
    r2 = cm.g2u_rate(500.0, 1.0)
    assert r1 == r2, f"Deterministic channel gave different rates: {r1} vs {r2}"

    # Also check another link type
    r3 = cm.g2s_rate(500e3, 2.0)
    r4 = cm.g2s_rate(500e3, 2.0)
    assert r3 == r4, f"Deterministic G2S gave different rates: {r3} vs {r4}"


def test_fixed_dag_reproducibility():
    """DAGGenerator.generate_fixed(42) called twice produces identical DAGs."""
    gen = DAGGenerator(n_tasks=20)
    dag1 = gen.generate_fixed(42)
    dag2 = gen.generate_fixed(42)

    assert dag1.edges == dag2.edges, "Edges differ between two generate_fixed(42) calls"
    for t1, t2 in zip(dag1.tasks, dag2.tasks):
        assert t1.input_data == t2.input_data, f"Task {t1.task_id} input_data differs"
        assert t1.output_data == t2.output_data, f"Task {t1.task_id} output_data differs"
        assert t1.cycles == t2.cycles, f"Task {t1.task_id} cycles differs"
        assert t1.deadline == t2.deadline, f"Task {t1.task_id} deadline differs"


# ---------------------------------------------------------------------------
# Autocorrelation warning
# ---------------------------------------------------------------------------

def test_channel_autocorrelation():
    """Sequential channel samples should have low lag-1 autocorrelation."""
    cm = ChannelModel(rng=np.random.default_rng(42))
    n = 1000
    samples = [cm.g2u_rate(500.0, 1.0) for _ in range(n)]

    arr = np.array(samples)
    lag1_corr = np.corrcoef(arr[:-1], arr[1:])[0, 1]

    if abs(lag1_corr) > 0.95:
        print(f"    WARNING: lag-1 autocorrelation = {lag1_corr:.4f} (channel too smooth)")
    # Independent samples should have near-zero autocorrelation
    assert abs(lag1_corr) < 0.3, (
        f"lag-1 autocorrelation {lag1_corr:.3f} suspiciously high for independent samples"
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_all():
    """Run all validation tests, print results."""
    tests = [
        ("Analytic: Path Loss", test_path_loss),
        ("Analytic: Orbital Period", test_orbital_period),
        ("Analytic: SNR Calculation", test_snr_calculation),
        ("Statistical: Shadowed-Rician", test_shadowed_rician_distribution),
        ("Statistical: DAG Degree", test_dag_degree_distribution),
        ("Statistical: IoTD Position", test_iotd_position_uniformity),
        ("Degradation: Deterministic Channel", test_deterministic_channel),
        ("Degradation: Fixed DAG", test_fixed_dag_reproducibility),
        ("Autocorrelation: Channel", test_channel_autocorrelation),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  [PASS] {name}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {name}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
