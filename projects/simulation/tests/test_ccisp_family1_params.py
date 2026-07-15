"""Formal CCISP Family-1 parameter truth-source contract."""

from params import AuditFlag, SimulationConfig, SourceType, TurbulenceParams


EXPECTED = {
    "weak": (11.6, 10.1, 0.2),
    "moderate": (4.0, 1.9, 1.6),
    "strong": (4.2, 1.4, 3.5),
}


def test_formal_family1_values_are_frozen_in_params_truth_source():
    config = SimulationConfig()
    actual = config.get_turb_dict()
    assert {name: actual[name] for name in EXPECTED} == {
        name: (alpha, beta) for name, (alpha, beta, _sigma_r2) in EXPECTED.items()
    }

    from common._config import TURB
    from simulator._b11_params import TURB_ALPHA_BETA

    assert {name: TURB[name] for name in EXPECTED} == {
        name: (alpha, beta) for name, (alpha, beta, _sigma_r2) in EXPECTED.items()
    }
    assert TURB_ALPHA_BETA == {
        name: (alpha, beta) for name, (alpha, beta, _sigma_r2) in EXPECTED.items()
    }


def test_formal_family1_metadata_records_direct_values_and_model_provenance():
    for name, (_alpha, _beta, sigma_r2) in EXPECTED.items():
        for suffix in ("alpha", "beta"):
            field = TurbulenceParams.model_fields[f"turb_{name}_{suffix}"]
            meta = field.json_schema_extra
            assert meta["source_type"] == SourceType.literature
            assert meta["audit_flag"] == AuditFlag.OK
            combined = " ".join(
                str(meta[key]) for key in ("source", "derivation", "note")
            )
            assert "10.3390/app12073331" in combined
            assert "10.1117/1.1386641" in combined
            assert str(sigma_r2) in combined
            assert "5%" in combined
