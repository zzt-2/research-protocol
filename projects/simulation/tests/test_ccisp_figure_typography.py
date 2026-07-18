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
    assert module.FONT_SIZES["legend"] >= (6.5 if name == "ber" else 8.5)
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


def test_ber_source_preserves_single_axis_scientific_contract():
    module = _load_module("ber", PLOT_MODULES["ber"])

    assert module.SCENES == ["awgn", "weak", "moderate", "strong"]
    assert not hasattr(module, "HD_FEC")
    assert [spec["ber_key"] for spec in module.CURVE_SPECS] == [
        "da", "nda", "oracle"
    ]
    assert set(module.SCENE_COLORS) == set(module.SCENES)
    assert module.METHOD_STYLES == {"da": "-", "nda": "--", "oracle": ":"}
    assert module.X_TICK_INTERVALS == {
        "awgn": (5.0, 2.0),
        "weak": (5.0, 2.0),
        "moderate": (5.0, 2.0),
        "strong": (5.0, 2.0),
    }


def test_ber_single_axis_rendering_uses_in_axes_semantic_legend(
    monkeypatch: pytest.MonkeyPatch,
):
    module = _load_module("ber", PLOT_MODULES["ber"])
    saved_figures = []

    def capture_savefig(self, *_args, **_kwargs):
        saved_figures.append(self)

    monkeypatch.setattr(module.plt.Figure, "savefig", capture_savefig)
    monkeypatch.setattr(module.plt, "close", lambda _fig: None)
    module.main()

    figure = saved_figures[0]
    assert saved_figures == [figure, figure]
    figure.canvas.draw()

    assert len(figure.axes) == 1
    axis = figure.axes[0]
    assert axis.get_xlim() == pytest.approx((5.0, 35.0))
    assert axis.get_ylim()[0] <= 1e-6
    assert len(axis.lines) == 12
    assert {line.get_linestyle() for line in axis.lines} == {"-", "--", ":"}
    assert {line.get_color() for line in axis.lines} == set(module.SCENE_COLORS.values())
    assert all(line.get_marker() in (None, "None", "") for line in axis.lines)
    assert not axis.texts
    assert not figure.legends

    legend = axis.get_legend()
    assert [text.get_text() for text in legend.get_texts()] == [
        "AWGN", "Weak", "Moderate", "Strong", "DA", "NDA", "ORACLE"
    ]
    renderer = figure.canvas.get_renderer()
    legend_box = legend.get_window_extent(renderer)
    axes_box = axis.get_window_extent(renderer)
    assert axes_box.contains(*legend_box.get_points()[0])
    assert axes_box.contains(*legend_box.get_points()[1])


def test_ber_export_is_single_axis_without_fec_or_panel_titles():
    page = fitz.open(DATA_PDFS["ber"])[0]
    assert not page.search_for("HD-FEC")
    assert not page.search_for("(a) AWGN")
    for label in ("AWGN", "Weak", "Moderate", "Strong", "DA", "NDA", "ORACLE"):
        assert page.search_for(label), label


@pytest.mark.parametrize("name", ["ber", "gain", "crossover"])
def test_quantitative_snr_axes_use_explicit_data_symbol_esn0_label(
    name: str,
    monkeypatch: pytest.MonkeyPatch,
):
    module = _load_module(name, PLOT_MODULES[name])
    saved_figures = []

    def capture_savefig(self, *_args, **_kwargs):
        saved_figures.append(self)

    monkeypatch.setattr(module.plt.Figure, "savefig", capture_savefig)
    monkeypatch.setattr(module.plt, "close", lambda _fig: None)
    module.main()

    figure = saved_figures[0]
    expected = r"Data-symbol $E_s/N_0$ [dB]"
    assert figure.axes[0].get_xlabel() == expected


def test_gain_source_and_sampling_contract():
    module = _load_module("gain", PLOT_MODULES["gain"])

    assert Path(module.DATA_JSON).name == "ccisp_family1_formal_verification.json"
    assert module.EXPECTED_SNR_DB == set(range(5, 26, 2))
    assert module.X_MAJOR_TICKS == [5, 9, 13, 17, 21, 25]


def test_gain_rendering_shows_all_samples_ci_zero_and_negative_ci(
    monkeypatch: pytest.MonkeyPatch,
):
    module = _load_module("gain", PLOT_MODULES["gain"])
    snr_db = list(range(5, 26, 2))
    figure_data = {}
    for scene_index, scene in enumerate(module.SCENES):
        means = [0.9 - 0.03 * index - 0.35 * scene_index for index in range(11)]
        lows = [mean - 0.04 for mean in means]
        highs = [mean + 0.04 for mean in means]
        figure_data[scene] = {
            "snr_db": snr_db,
            "mean_gain_db": means,
            "ci95_low_db": lows,
            "ci95_high_db": highs,
        }
    figure_data["strong"]["mean_gain_db"][-1] = -0.02
    figure_data["strong"]["ci95_low_db"][-1] = -0.06
    figure_data["strong"]["ci95_high_db"][-1] = 0.02

    saved_figures = []

    def capture_savefig(self, *_args, **_kwargs):
        saved_figures.append(self)

    monkeypatch.setattr(module, "load_figure_data", lambda: figure_data)
    monkeypatch.setattr(module.plt.Figure, "savefig", capture_savefig)
    monkeypatch.setattr(module.plt, "close", lambda _fig: None)
    module.main()

    figure = saved_figures[0]
    assert saved_figures == [figure, figure]
    figure.canvas.draw()
    axis = figure.axes[0]
    assert axis.get_xlabel() == r"Data-symbol $E_s/N_0$ [dB]"
    assert axis.get_ylabel() == (
        "Common-payload BER-ratio\nreduction, $G_{\\mathcal{C}}$ [dB]"
    )
    assert list(axis.get_xticks()) == module.X_MAJOR_TICKS
    assert axis.get_ylim()[0] <= -0.06

    sample_lines = [
        container.lines[0]
        for container in axis.containers
        if container.get_label()
        in {module.STYLES[scene]["label"] for scene in module.SCENES}
    ]
    assert len(sample_lines) == 3
    assert all(list(line.get_xdata()) == snr_db for line in sample_lines)
    zero_lines = [
        line
        for line in axis.lines
        if len(line.get_ydata()) == 2 and set(line.get_ydata()) == {0.0}
    ]
    assert len(zero_lines) == 1
    assert zero_lines[0].get_linestyle() == "--"


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



@pytest.mark.xfail(
    reason="User-maintained Fig.1 preserves the accepted 0.32-pt mapper/input gap",
    strict=True,
)
def test_fig1_user_asset_geometry_debt_is_explicit():
    document = fitz.open(PAPER_PDF)
    page = next(page for page in document if page.search_for("Atmospheric FSO channel"))
    input_bits = min(page.search_for("bits"), key=lambda box: box.x0)
    mapper_title = page.search_for("(8,8)-16APSK")[0]
    assert mapper_title.x0 - input_bits.x1 >= 3.0


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
