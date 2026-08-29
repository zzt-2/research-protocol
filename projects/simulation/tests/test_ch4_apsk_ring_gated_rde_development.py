from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "explore" / "ch4-apsk-ring-gated-rde"


def _load_driver():
    spec = importlib.util.spec_from_file_location("ch4_gated_rde_development", PKG / "run_development.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_manifest_freezes_exact_cells_and_seed_firewall():
    driver = _load_driver()
    manifest = driver.load_manifest(PKG / "development_manifest.yaml")
    assert manifest["payload_symbols"] == 8192
    assert [(c["id"], c["snr_db"], c["pilots"]) for c in manifest["round1_cells"]] == [
        ("D1", 14, 2), ("D2", 18, 2), ("D3", 14, 8)
    ]
    assert [(c["id"], c["snr_db"], c["pilots"]) for c in manifest["round2_cells"]] == [
        ("D4", 14, 4), ("D5", 18, 4), ("D6", 18, 8)
    ]
    assert manifest["tune_seeds"] == [54101, 54102, 54103]
    assert manifest["eval_seeds"] == [54201, 54202, 54203, 54204, 54205, 54206]
    assert min(manifest["confirmation_seeds_reserved"]) >= 54301
    driver.validate_manifest(manifest)


def test_jeffreys_ber_and_auc_are_deterministic():
    driver = _load_driver()
    assert driver.jeffreys_ber(0, 100) == (0.5 / 101.0)
    assert driver.jeffreys_ber(100, 100) == (100.5 / 101.0)
    assert driver.binary_auc(np.array([0.1, 0.2, 0.8, 0.9]), np.array([0, 0, 1, 1])) == 1.0
    assert driver.binary_auc(np.array([0.9, 0.8, 0.2, 0.1]), np.array([0, 0, 1, 1])) == 0.0


def test_count_matched_masks_preserve_each_pol_block_count_and_seed():
    driver = _load_driver()
    source = np.zeros((2, 600), dtype=bool)
    source[0, [0, 2, 258, 259, 599]] = True
    source[1, [1, 3, 4, 260, 511, 512, 513]] = True
    a = driver.count_matched_masks(source, seed=77, block_size=256)
    b = driver.count_matched_masks(source, seed=77, block_size=256)
    np.testing.assert_array_equal(a, b)
    for start in range(0, 600, 256):
        stop = min(start + 256, 600)
        np.testing.assert_array_equal(a[:, start:stop].sum(axis=1), source[:, start:stop].sum(axis=1))


def test_ring_auc_uses_wrong_ring_not_wrong_symbol_label():
    driver = _load_driver()
    constellation = driver.core.m16apsk_constellation_by_label()
    truth = np.array([[0, 1, 8, 9]], dtype=np.uint8)
    predicted = np.array([[1, 1, 9, 0]], dtype=np.uint8)
    result = {
        "z": constellation[predicted],
        "W": np.eye(2),
        "gates": np.ones((1, 4), dtype=bool),
        "ring_score": np.array([[0.9, 0.1, 0.8, 0.7]]),
        "native_ring_score": np.array([[0.9, 0.1, 0.8, 0.7]]),
        "decision_score": np.array([[0.9, 0.1, 0.8, 0.7]]),
    }
    measured = driver._measure(result, truth)
    assert measured["wrong_symbol_count"] == 3
    assert measured["wrong_ring_count"] == 1
    assert measured["ring_auc"] == pytest.approx(1 / 3)


def test_round1_gate_obeys_preregistered_or_conditions():
    driver = _load_driver()
    empty = {"cells": {"D1": {"arms": {"candidate": {"gain_vs_bstar": 0.0, "wins": 0, "gap_recovery": 0.0},
                                                   "cheap": {"gain_vs_bstar": 0.0, "wins": 0, "gap_recovery": 0.0}},
                                      "oracle_headroom": 0.0, "combined_auc": 0.5}}}
    decision = driver.round1_decision(empty)
    assert decision["enter_round2"] is False
    assert decision["winner"] == "none"

    signal = {"cells": {"D1": {"arms": {"candidate": {"gain_vs_bstar": 0.12, "wins": 5, "gap_recovery": 0.1},
                                                    "cheap": {"gain_vs_bstar": 0.02, "wins": 3, "gap_recovery": 0.0}},
                                       "oracle_headroom": 0.2, "combined_auc": 0.59}}}
    decision = driver.round1_decision(signal)
    assert decision["enter_round2"] is True
    assert decision["winner"] == "candidate"

    absorbed = {"cells": {"D1": {"arms": {
        "candidate": {"ber": 0.08, "gain_vs_bstar": 0.20, "wins": 6, "gap_recovery": 0.50},
        "cheap": {"ber": 0.09, "gain_vs_bstar": 0.10, "wins": 5, "gap_recovery": 0.25},
        "count_matched_candidate": {"ber": 0.07},
        "count_matched_cheap": {"ber": 0.08}},
        "oracle_headroom": 0.40, "combined_auc": 0.70}}}
    decision = driver.round1_decision(absorbed)
    assert decision["enter_round2"] is False
    assert "ALL_GAIN_COUNT_MATCHED_ABSORBED" in decision["stop_reasons"]
