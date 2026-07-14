"""Typography contract for the five CCISP paper figures."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from xml.etree import ElementTree

import fitz
import pytest


SIM_ROOT = Path(__file__).resolve().parents[1]
FIGURES = SIM_ROOT / "figures"
PAPER_PDF = SIM_ROOT / "paper" / "ccisp2026" / "main.pdf"

PLOT_MODULES = {
    "ber": FIGURES / "plot_fig2_ber.py",
    "gain": FIGURES / "plot_fig3_gain.py",
    "crossover": FIGURES / "plot_fig4_crossover.py",
}

DATA_PDFS = {
    "ber": FIGURES / "ccisp_fig2_ber.pdf",
    "gain": FIGURES / "ccisp_fig3_gain.pdf",
    "crossover": FIGURES / "ccisp_fig4_crossover.pdf",
}

FIG1_MAJOR_TEXT = {
    "Transmitter",
    "Atmospheric FSO channel",
    "Coherent receiver DSP",
    "Composite FSO channel",
    "Adaptive carrier",
    "recovery",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(f"ccisp_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", PLOT_MODULES)
def test_matplotlib_sources_expose_final_size_typography_contract(name: str):
    module = _load_module(name, PLOT_MODULES[name])

    assert module.FIGSIZE_IN[0] == pytest.approx(3.5)
    assert module.FONT_SIZES["label"] == pytest.approx(10.0)
    assert module.FONT_SIZES["tick"] >= 8.5
    assert module.FONT_SIZES["legend"] >= 8.5
    assert module.MPL_RCPARAMS["font.family"] == "serif"
    assert module.MPL_RCPARAMS["font.serif"][0] == "Times New Roman"
    assert module.MPL_RCPARAMS["mathtext.fontset"] == "stix"
    assert module.MPL_RCPARAMS["text.usetex"] is False
    assert module.MPL_RCPARAMS["font.weight"] == "normal"
    assert module.MPL_RCPARAMS["axes.labelweight"] == "normal"
    assert module.MPL_RCPARAMS["pdf.fonttype"] == 42


@pytest.mark.parametrize("name", DATA_PDFS)
def test_data_plot_pdf_is_native_single_column_and_uses_allowed_fonts(name: str):
    document = fitz.open(DATA_PDFS[name])
    page = document[0]
    assert page.rect.width == pytest.approx(252.0, abs=1.0)

    disallowed = {"Helvetica", "DejaVuSans"}
    fonts = {entry[3] for entry in page.get_fonts(full=True)}
    assert not any(any(token in font for token in disallowed) for font in fonts)
    assert any("Times" in font for font in fonts)
    assert any("STIX" in font for font in fonts)


def test_ber_source_preserves_scientific_and_legend_contract():
    module = _load_module("ber", PLOT_MODULES["ber"])

    assert module.SCENES == [
        "awgn",
        "weak",
        "moderate",
        "strong",
        "uplink_moderate",
        "uplink_strong",
    ]
    assert module.HD_FEC == pytest.approx(3.8e-3)
    assert module.CURVE_SPECS == (
        {
            "ber_key": "da_ml_ber_mean",
            "label": "DA-ML (pilot-aided)",
            "color": "#0072B2",
            "linestyle": "-",
        },
        {
            "ber_key": "nda_ml_ber_mean",
            "label": "NDA-ML (blind)",
            "color": "#D55E00",
            "linestyle": "--",
        },
        {
            "ber_key": "oracle_ber_mean",
            "label": "Oracle",
            "color": "#009E73",
            "linestyle": ":",
        },
    )
    assert module.HD_FEC_LEGEND_LABEL == (
        r"HD-FEC threshold ($3.8\times10^{-3}$)"
    )


def test_ber_export_keeps_top_titles_inside_page_box():
    page = fitz.open(DATA_PDFS["ber"])[0]
    title_boxes = [
        box
        for title in ("(a) AWGN", "(b) Weak turbulence")
        for box in page.search_for(title)
    ]
    assert len(title_boxes) == 2
    assert min(box.y0 for box in title_boxes) >= 1.0


def test_fig1_effective_typography_matches_body_size_in_final_paper():
    document = fitz.open(PAPER_PDF)
    anchor = "Atmospheric FSO channel"
    page = next(page for page in document if page.search_for(anchor))

    title_boxes = [
        box
        for title in ("Transmitter", anchor, "Coherent receiver DSP")
        for box in page.search_for(title)
    ]
    caption_boxes = page.search_for("Fig. 1.")
    assert len(title_boxes) == 3
    assert caption_boxes
    figure_top = min(box.y0 for box in title_boxes) - 1.0
    figure_bottom = min(box.y0 for box in caption_boxes)

    spans = [
        span
        for block in page.get_text("dict")["blocks"]
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if figure_top <= span["bbox"][1] < figure_bottom
        and span["text"].strip()
        and "TimesNewRoman" in span["font"]
    ]
    assert spans

    for text in FIG1_MAJOR_TEXT:
        sizes = [span["size"] for span in spans if span["text"].strip() == text]
        assert sizes, text
        assert min(sizes) >= 9.8, (text, min(sizes))

    ordinary_sizes = [
        span["size"]
        for span in spans
        if span["text"].strip() not in FIG1_MAJOR_TEXT
    ]
    assert ordinary_sizes
    assert min(ordinary_sizes) >= 8.5

    information = page.search_for("Information")[0]
    input_bits = min(page.search_for("bits"), key=lambda box: box.x0)
    mapper_title = page.search_for("(8,8)-16APSK")[0]
    figure_rect = max(
        (
            drawing["rect"]
            for drawing in page.get_drawings()
            if drawing["rect"].y0 <= figure_top <= drawing["rect"].y1
        ),
        key=lambda box: box.width,
    )
    assert mapper_title.x0 - input_bits.x1 >= 3.0
    assert information.x0 - figure_rect.x0 >= 1.5


def test_fig1_block_fading_label_has_margin_inside_its_node():
    graph, cells = _drawio(FIGURES / "fig1_system_model_v5.drawio")
    page = fitz.open(FIGURES / "fig1_system_model_v5.pdf")[0]
    geometry = cells["fading"].find("mxGeometry")
    assert geometry is not None

    scale = page.rect.width / float(graph.attrib["pageWidth"])
    node_left = float(geometry.attrib["x"]) * scale
    node_right = (
        float(geometry.attrib["x"]) + float(geometry.attrib["width"])
    ) * scale
    label = page.search_for("Block fading")[0]

    assert label.x0 - node_left >= 3.0
    assert node_right - label.x1 >= 3.0


def _drawio(path: Path):
    tree = ElementTree.parse(path)
    graph = tree.find(".//mxGraphModel")
    assert graph is not None
    cells = {cell.attrib["id"]: cell for cell in tree.iter("mxCell")}
    return graph, cells


def _style_value(style: str, key: str) -> str | None:
    prefix = f"{key}="
    for item in style.split(";"):
        if item.startswith(prefix):
            return item[len(prefix) :]
    return None


@pytest.mark.parametrize(
    ("filename", "major_ids", "source_floor"),
    [
        (
            "fig1_system_model_v5.drawio",
            {"title_tx", "title_channel", "title_rx", "channel_label", "cpr_label"},
            28.0,
        ),
        (
            "fig2_adaptive_cpr.drawio",
            {"lane_est", "lane_data", "lane_ctrl", "da", "nda", "selector", "phase"},
            26.0,
        ),
    ],
)
def test_drawio_visible_labels_meet_source_floor_and_math_is_enabled(
    filename: str, major_ids: set[str], source_floor: float
):
    graph, cells = _drawio(FIGURES / filename)
    assert graph.attrib.get("math") == "1"

    for cell in cells.values():
        value = cell.attrib.get("value", "").strip()
        style = cell.attrib.get("style", "")
        if value and _style_value(style, "fontFamily") == "Times New Roman":
            size = _style_value(style, "fontSize")
            assert size is not None, cell.attrib["id"]
            assert float(size) >= source_floor, cell.attrib["id"]

    for cell_id in major_ids:
        size = _style_value(cells[cell_id].attrib.get("style", ""), "fontSize")
        assert size is not None
        major_floor = 31.0 if filename == "fig1_system_model_v5.drawio" else 29.0
        assert float(size) >= major_floor, cell_id


def test_drawio_variable_labels_use_math_typesetting_not_html_italics():
    _, fig1 = _drawio(FIGURES / "fig1_system_model_v5.drawio")
    _, fig2 = _drawio(FIGURES / "fig2_adaptive_cpr.drawio")

    for cells, ids in [
        (fig1, {"sk_label", "rk_label"}),
        (
            fig2,
            {
                "rk",
                "theta_da",
                "theta_nda",
                "selected_label",
                "cv_gate",
                "blind_effective_snr",
                "snr_gate",
            },
        ),
    ]:
        for cell_id in ids:
            value = cells[cell_id].attrib.get("value", "")
            assert "\\(" in value and "\\)" in value, cell_id
            assert "&lt;i&gt;" not in value, cell_id
