"""Structural regression tests for the Fig. 2 two-layer control path."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree


FIGURE = Path(__file__).resolve().parents[1] / "figures" / "fig2_adaptive_cpr.drawio"


def _tree_signature(element: ElementTree.Element):
    return (
        element.tag,
        tuple(sorted(element.attrib.items())),
        tuple(_tree_signature(child) for child in element),
    )


# Captured from the user-adjusted draw.io source before the control-path edit.
FROZEN_NON_CONTROL_EDGES = {
    "e_input": (
        "input_anchor",
        "fork",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=3;endArrow=block;endFill=1;entryX=0;entryY=0.5;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_raw": (
        "fork",
        "phase",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=3;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_phase_down": (
        "phase",
        "downstream",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=3;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_output": (
        "downstream",
        "output_terminal",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=3;endArrow=none;exitX=1;exitY=0.5;entryX=0;entryY=0.5;entryPerimeter=0;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_fork_da": (
        "fork",
        "da",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=2;endArrow=block;endFill=1;exitX=0.5;exitY=0;entryX=0;entryY=0.5;fontSize=18;",
        (
            "mxGeometry",
            (("as", "geometry"), ("relative", "1")),
            (("Array", (("as", "points"),), (("mxPoint", (("x", "262"), ("y", "125")), ()),)),),
        ),
    ),
    "e_fork_nda": (
        "fork",
        "nda",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#1c5c83;strokeWidth=2;endArrow=block;endFill=1;exitX=0.5;exitY=0;entryX=0;entryY=0.5;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_theta_da": (
        "da",
        "selector",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#277b58;strokeWidth=2.2;dashed=1;dashPattern=8 6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0.161;entryY=0.188;entryDx=0;entryDy=0;entryPerimeter=0;fontSize=18;",
        (
            "mxGeometry",
            (("as", "geometry"), ("relative", "1")),
            (("Array", (("as", "points"),), (("mxPoint", (("x", "815"), ("y", "125")), ()),)),),
        ),
    ),
    "e_theta_nda": (
        "nda",
        "selector",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#277b58;strokeWidth=2.2;dashed=1;dashPattern=8 6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0.218;entryY=0.938;entryDx=0;entryDy=0;entryPerimeter=0;fontSize=18;",
        ("mxGeometry", (("as", "geometry"), ("relative", "1")), ()),
    ),
    "e_selected": (
        "selector",
        "phase",
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#277b58;strokeWidth=2.2;dashed=1;dashPattern=8 6;endArrow=block;endFill=1;exitX=1;exitY=0.5;entryX=0.5;entryY=0;fontSize=18;",
        (
            "mxGeometry",
            (("as", "geometry"), ("relative", "1")),
            (("Array", (("as", "points"),), (("mxPoint", (("x", "1080"), ("y", "165")), ()),)),),
        ),
    ),
}


def _cells():
    return {cell.attrib["id"]: cell for cell in ElementTree.parse(FIGURE).iter("mxCell")}


def test_route_b_router_precedes_exactly_one_estimator_branch():
    cells = _cells()
    assert cells["selector"].attrib["value"] == "Branch<br>router"
    assert (cells["e_selected"].attrib["source"], cells["e_selected"].attrib["target"]) == (
        "fork",
        "selector",
    )
    assert (cells["e_fork_da"].attrib["source"], cells["e_fork_da"].attrib["target"]) == (
        "selector",
        "da",
    )
    assert (cells["e_fork_nda"].attrib["source"], cells["e_fork_nda"].attrib["target"]) == (
        "selector",
        "nda",
    )
    assert (cells["e_theta_da"].attrib["source"], cells["e_theta_da"].attrib["target"]) == (
        "da",
        "phase",
    )
    assert (cells["e_theta_nda"].attrib["source"], cells["e_theta_nda"].attrib["target"]) == (
        "nda",
        "phase",
    )


def test_old_single_layer_control_labels_are_removed():
    cells = _cells()
    values = " ".join(cell.attrib.get("value", "") for cell in cells.values())

    assert "Per-block SNR" not in values
    assert "Fixed SNR threshold" not in values
    assert "γ&lt;/i&gt;&lt;sub&gt;blk" not in values
    assert not {"measurement", "threshold", "threshold_caption", "gamma_label"} & set(cells)


def test_two_layer_control_nodes_and_exact_13_db_gate_exist():
    cells = _cells()
    expected_values = {
        "window_stats": "Window power<br>statistics",
        "cv_gate": r"CV &lt; \(\tau_{\mathrm{CV}}\)?",
        "blind_effective_snr": r"Blind \(\hat{h}_{\mathrm{dsp}}\)<br>Effective SNR \(\hat{\gamma}_{\mathrm{eff}}\)",
        "snr_gate": r"\(\hat{\gamma}_{\mathrm{eff}}\) &lt; 13 dB?",
        "branch_command": "Branch<br>command",
    }

    for cell_id, value in expected_values.items():
        assert cells[cell_id].attrib.get("value") == value


def test_two_layer_branches_merge_only_through_branch_command():
    cells = _cells()
    expected_edges = {
        "e_fork_stats": ("fork", "window_stats", ""),
        "e_stats_cv": ("window_stats", "cv_gate", ""),
        "e_cv_yes": ("cv_gate", "branch_command", "yes · NDA"),
        "e_cv_otherwise": ("cv_gate", "blind_effective_snr", "otherwise"),
        "e_blind_snr_gate": ("blind_effective_snr", "snr_gate", ""),
        "e_snr_yes": ("snr_gate", "branch_command", "yes · DA"),
        "e_snr_no": ("snr_gate", "branch_command", "no · NDA"),
        "e_branch_selector": ("branch_command", "selector", ""),
    }

    for edge_id, (source, target, value) in expected_edges.items():
        edge = cells[edge_id]
        assert (edge.attrib["source"], edge.attrib["target"], edge.attrib.get("value", "")) == (
            source,
            target,
            value,
        )
        assert "edgeStyle=orthogonalEdgeStyle" in edge.attrib["style"]

    control_edges = [
        cell for cell in cells.values() if cell.attrib.get("edge") == "1" and cell.attrib["id"] not in FROZEN_NON_CONTROL_EDGES
    ]
    assert {edge.attrib["id"] for edge in control_edges} == set(expected_edges)
    assert {edge.attrib["source"] for edge in control_edges if edge.attrib["target"] == "selector"} == {
        "branch_command"
    }


def test_every_semantic_edge_is_bound_to_existing_cells_and_orthogonal():
    cells = _cells()
    edges = [cell for cell in cells.values() if cell.attrib.get("edge") == "1"]

    assert len(edges) == 17
    for edge in edges:
        assert edge.attrib.get("source") in cells, edge.attrib["id"]
        assert edge.attrib.get("target") in cells, edge.attrib["id"]
        assert "edgeStyle=orthogonalEdgeStyle" in edge.attrib.get("style", ""), edge.attrib["id"]
