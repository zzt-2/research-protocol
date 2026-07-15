"""Regression tests for side-effect-free Gamma-Gamma parameter injection."""

import numpy as np
import pytest

from common import generate_shared_realization, generate_shared_realization_apsk
from common._channel import gg_block
from common._config import DOPPLER_HIGH, TURB


ARRAY_KEYS = ("rx_raw", "bits", "tx", "h", "h_blocks", "phi")


def _assert_shared_bit_exact(left, right):
    for key in ARRAY_KEYS:
        assert np.array_equal(left[key], right[key]), key
    assert left["h_med"] == right["h_med"]


@pytest.mark.parametrize(
    "generator,extra",
    [
        (generate_shared_realization, {}),
        (generate_shared_realization_apsk, {"mod": "m16apsk"}),
    ],
)
def test_explicit_configured_turbulence_is_bit_exact_with_default(generator, extra):
    args = dict(
        Ns=200,
        gamma_bar=20.0,
        turb_name="moderate",
        f_dot=DOPPLER_HIGH,
        seed=1701,
        lw=0.0,
        **extra,
    )

    default = generator(**args)
    explicit = generator(**args, turb_params=TURB["moderate"])

    _assert_shared_bit_exact(default, explicit)


@pytest.mark.parametrize(
    "generator,bits_per_symbol,extra",
    [
        (generate_shared_realization, 2, {}),
        (generate_shared_realization_apsk, 4, {"mod": "m16apsk"}),
    ],
)
def test_explicit_family1_parameters_drive_gamma_gamma_realization(
    generator, bits_per_symbol, extra,
):
    family1 = (4.026521312058279, 1.9105223344570113)
    ns = 200
    seed = 1702

    actual = generator(
        ns,
        20.0,
        "moderate",
        DOPPLER_HIGH,
        seed=seed,
        lw=0.0,
        turb_params=family1,
        **extra,
    )

    np.random.seed(seed)
    np.random.randint(0, 2, ns * bits_per_symbol)
    expected_h = gg_block(ns, *family1)
    assert np.array_equal(actual["h"], expected_h)


@pytest.mark.parametrize(
    "generator,extra",
    [
        (generate_shared_realization, {}),
        (generate_shared_realization_apsk, {"mod": "m16apsk"}),
    ],
)
def test_explicit_turbulence_does_not_mutate_global_config(generator, extra):
    before = dict(TURB)
    generator(
        200,
        20.0,
        "moderate",
        DOPPLER_HIGH,
        seed=1704,
        lw=0.0,
        turb_params=(4.026521312058279, 1.9105223344570113),
        **extra,
    )
    assert TURB == before


@pytest.mark.parametrize(
    "invalid",
    [
        (),
        (1.0,),
        (1.0, 2.0, 3.0),
        "1,2",
        (0.0, 1.0),
        (-1.0, 1.0),
        (1.0, np.inf),
        (np.nan, 1.0),
    ],
)
@pytest.mark.parametrize(
    "generator,extra",
    [
        (generate_shared_realization, {}),
        (generate_shared_realization_apsk, {"mod": "m16apsk"}),
    ],
)
def test_invalid_explicit_turbulence_parameters_are_rejected(generator, extra, invalid):
    with pytest.raises((TypeError, ValueError)):
        generator(
            200,
            20.0,
            "weak",
            DOPPLER_HIGH,
            seed=1703,
            lw=0.0,
            turb_params=invalid,
            **extra,
        )
