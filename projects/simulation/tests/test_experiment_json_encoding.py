import json

from common._experiment import save_results


def test_save_results_writes_non_ascii_json_as_utf8(tmp_path):
    output = tmp_path / "result.json"

    save_results({"scope_note": "三种湍流场景"}, str(output), "test_script.py")

    decoded = output.read_text(encoding="utf-8")
    assert json.loads(decoded)["scope_note"] == "三种湍流场景"

