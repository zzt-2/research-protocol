"""PROMPT-011 standard-CMA regression tests."""
from pathlib import Path
import sys

import numpy as np


EXPLORE_DIR = Path(__file__).resolve().parents[1] / "explore" / "cma-fade-divergence"
sys.path.insert(0, str(EXPLORE_DIR))

from prompt011_cma_root_diagnostic import (
    StandardCMAEqualizer2x2,
    save_diagnostic_results,
)
from common._cma import CMAEqualizer2x2


def _standard_one_block_weights(r_x, r_y, mu, r2):
    z_x = r_x.copy()
    z_y = r_y.copy()
    e_x = r2 - np.abs(z_x) ** 2
    e_y = r2 - np.abs(z_y) ** 2
    return (
        np.array([1 + mu * np.mean(e_x * z_x * np.conj(r_x))]),
        np.array([mu * np.mean(e_x * z_x * np.conj(r_y))]),
        np.array([mu * np.mean(e_y * z_y * np.conj(r_x))]),
        np.array([1 + mu * np.mean(e_y * z_y * np.conj(r_y))]),
    )


def test_standard_cma_matches_single_block_complex_update():
    """w += mu*mean((R2-|z|^2)*z*conj(x)), for z=x@w."""
    r_x = np.array([0.5 + 0.2j, -0.3 + 0.7j])
    r_y = np.array([0.1 - 0.4j, 0.8 + 0.1j])
    mu, r2 = 0.03, 1.0
    expected = _standard_one_block_weights(r_x, r_y, mu, r2)

    eq = StandardCMAEqualizer2x2(n_tap=1, mu=mu, R2=r2)
    eq.equalize(r_x, r_y, block_size=2)

    for actual, target in zip((eq.wxx, eq.wxy, eq.wyx, eq.wyy), expected):
        np.testing.assert_allclose(actual, target, rtol=1e-13, atol=1e-13)


def test_current_scalar_error_update_is_not_standard_but_test_documents_it():
    """Existing CMA omits the output factor z; document mismatch without failing suite."""
    r_x = np.array([0.5 + 0.2j, -0.3 + 0.7j])
    r_y = np.array([0.1 - 0.4j, 0.8 + 0.1j])
    mu, r2 = 0.03, 1.0
    expected = _standard_one_block_weights(r_x, r_y, mu, r2)

    current = CMAEqualizer2x2(n_tap=1, mu=mu, R2=r2)
    current.equalize(r_x, r_y, block_size=2)

    assert any(
        not np.allclose(actual, target, rtol=1e-13, atol=1e-13)
        for actual, target in zip(
            (current.wxx, current.wxy, current.wyx, current.wyy), expected
        )
    )


def test_diagnostic_result_saver_injects_standard_metadata(tmp_path):
    output = tmp_path / "diagnostic.json"

    save_diagnostic_results({"trials": []}, output)

    import json
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["_meta"]["script"] == "prompt011_cma_root_diagnostic"
    assert saved["_meta"]["git_commit"]
    assert saved["_meta"]["timestamp"]
