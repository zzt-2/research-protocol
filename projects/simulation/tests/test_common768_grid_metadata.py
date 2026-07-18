import importlib.util
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "explore"
    / "nda-awgn-tracking-sandbox"
    / "_a4_switch_common768_30seed.py"
)


def load_script_module():
    spec = importlib.util.spec_from_file_location("common768_30seed", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_grid_metadata_reflects_requested_scenes_and_snr_grid():
    module = load_script_module()
    snrs = list(range(5, 26, 2))

    metadata = module.build_grid_metadata(
        ["weak", "moderate", "strong"],
        snrs,
        mixed_oracle_violations=0,
        common_oracle_violations=0,
    )

    assert "33" in metadata["scope_note"]
    assert "5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25" in metadata["scope_note"]
    assert "9 点" not in " ".join(str(value) for value in metadata.values())
    assert "weak@10" not in metadata["sanity_check"]
    assert metadata["selfcheck_mixed_oracle_violations"] == 0
    assert metadata["selfcheck_common_oracle_violations"] == 0


def test_loaded_dependency_paths_handles_modules_on_another_windows_drive():
    module = load_script_module()

    paths = module.loaded_dependency_paths()

    assert paths
