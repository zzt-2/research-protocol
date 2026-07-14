"""Generate deterministic, text-free miniature assets for Fig. 1 v5.

These files illustrate the implemented signal model.  They are not experiment
results and deliberately do not use the results persistence pipeline.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw

SIMULATION_ROOT = Path(__file__).resolve().parents[2]
if str(SIMULATION_ROOT) not in sys.path:
    sys.path.insert(0, str(SIMULATION_ROOT))

from common import (
    generate_shared_realization_apsk,
    m16apsk_demod,
    m16apsk_mod,
)
from params import SimulationConfig


N = 256
SNR_DB = 15.0
SCENE = "moderate"
SEED = 2000
GRID_SIZE = 401

BLUE = "#729FCF"
ORANGE = "#E6A15C"
GRAY = "#68727D"


def _labels_from_bits(bits: np.ndarray) -> np.ndarray:
    return bits.reshape(-1, 4) @ np.array([8, 4, 2, 1], dtype=int)


def build_asset_data() -> dict[str, np.ndarray | float]:
    """Build all miniature inputs from one fixed formal channel realization."""
    config = SimulationConfig()
    f_dot = config.doppler.DOPPLER_HIGH
    realization = generate_shared_realization_apsk(
        N,
        gamma_bar=10.0 ** (SNR_DB / 10.0),
        turb_name=SCENE,
        f_dot=f_dot,
        mod="m16apsk",
        seed=SEED,
    )

    constellation_bits = (
        np.arange(16, dtype=np.uint8)[:, None]
        >> np.arange(3, -1, -1, dtype=np.uint8)
    ) & 1
    constellation = m16apsk_mod(constellation_bits.reshape(-1))

    extent = 1.55
    grid_x = np.linspace(-extent, extent, GRID_SIZE)
    grid_y = np.linspace(extent, -extent, GRID_SIZE)
    xx, yy = np.meshgrid(grid_x, grid_y)
    decision_bits = m16apsk_demod((xx + 1j * yy).reshape(-1))
    decision_labels = _labels_from_bits(decision_bits).reshape(GRID_SIZE, GRID_SIZE)

    tx = realization["tx"]
    h = realization["h"]
    phi = realization["phi"]
    rx_raw = realization["rx_raw"]
    noise = rx_raw - tx * np.sqrt(h) * np.exp(1j * phi)

    return {
        "constellation": constellation,
        "tx": tx,
        "h": h,
        "phi": phi,
        "rx_raw": rx_raw,
        "noise": noise,
        "decision_labels": decision_labels,
        "decision_extent": extent,
        "f_dot": float(f_dot),
    }


def _svg_root(width: int, height: int) -> ET.Element:
    return ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(height),
            "viewBox": f"0 0 {width} {height}",
        },
    )


def _write_svg(root: ET.Element, path: Path) -> None:
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def _map_xy(
    values: np.ndarray,
    width: int,
    height: int,
    pad: int,
    extent: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    if extent is None:
        extent = max(float(np.max(np.abs(values.real))), float(np.max(np.abs(values.imag))))
        extent = max(extent * 1.08, 1e-12)
    x = pad + (values.real + extent) * (width - 2 * pad) / (2 * extent)
    y = height - pad - (values.imag + extent) * (height - 2 * pad) / (2 * extent)
    return x, y


def render_constellation(output_dir: Path, data: dict) -> Path:
    """Render the formal two-ring 16APSK points as a transparent SVG."""
    width = height = 320
    root = _svg_root(width, height)
    x, y = _map_xy(data["constellation"], width, height, 18, extent=1.45)
    for index, (cx, cy) in enumerate(zip(x, y)):
        ET.SubElement(
            root,
            "circle",
            {
                "cx": f"{cx:.3f}",
                "cy": f"{cy:.3f}",
                "r": "7",
                "fill": BLUE if index < 8 else ORANGE,
                "stroke": GRAY,
                "stroke-width": "2",
            },
        )
    path = output_dir / "constellation.svg"
    _write_svg(root, path)
    return path


def _render_trace(
    output_dir: Path,
    filename: str,
    values: np.ndarray,
    color: str,
    boundaries: tuple[int, ...] = (),
) -> Path:
    width, height, pad = 480, 220, 12
    root = _svg_root(width, height)
    values = np.asarray(values, dtype=float)
    lower, upper = float(values.min()), float(values.max())
    margin = max((upper - lower) * 0.08, 1e-12)
    lower, upper = lower - margin, upper + margin
    x = pad + np.arange(len(values)) * (width - 2 * pad) / (len(values) - 1)
    y = height - pad - (values - lower) * (height - 2 * pad) / (upper - lower)
    for boundary in boundaries:
        bx = pad + boundary * (width - 2 * pad) / (len(values) - 1)
        ET.SubElement(
            root,
            "line",
            {
                "x1": f"{bx:.3f}",
                "x2": f"{bx:.3f}",
                "y1": str(pad),
                "y2": str(height - pad),
                "stroke": GRAY,
                "stroke-width": "2",
                "stroke-dasharray": "7 6",
                "opacity": "0.65",
            },
        )
    points = " ".join(f"{px:.3f},{py:.3f}" for px, py in zip(x, y))
    ET.SubElement(
        root,
        "polyline",
        {
            "points": points,
            "fill": "none",
            "stroke": color,
            "stroke-width": "4",
            "stroke-linejoin": "round",
            "stroke-linecap": "round",
        },
    )
    path = output_dir / filename
    _write_svg(root, path)
    return path


def render_block_fading(output_dir: Path, data: dict) -> Path:
    """Render the unsmoothed formal block-fading realization."""
    return _render_trace(
        output_dir,
        "block_fading.svg",
        data["h"],
        BLUE,
        boundaries=(100, 200),
    )


def render_carrier_phase(output_dir: Path, data: dict) -> Path:
    """Render the total formal carrier phase without component amplification."""
    return _render_trace(output_dir, "carrier_phase.svg", data["phi"], ORANGE)


def render_awgn_iq(output_dir: Path, data: dict) -> Path:
    """Render the reconstructed complex AWGN samples as a transparent SVG."""
    width = height = 320
    root = _svg_root(width, height)
    x, y = _map_xy(data["noise"], width, height, 14)
    for cx, cy in zip(x, y):
        ET.SubElement(
            root,
            "circle",
            {
                "cx": f"{cx:.3f}",
                "cy": f"{cy:.3f}",
                "r": "3.2",
                "fill": BLUE,
                "opacity": "0.72",
            },
        )
    path = output_dir / "awgn_iq.svg"
    _write_svg(root, path)
    return path


def render_received_signal(output_dir: Path, data: dict) -> Path:
    """Render the impaired received I/Q samples from the shared realization."""
    width = height = 320
    root = _svg_root(width, height)
    x, y = _map_xy(data["rx_raw"], width, height, 14)
    for cx, cy in zip(x, y):
        ET.SubElement(
            root,
            "circle",
            {
                "cx": f"{cx:.3f}",
                "cy": f"{cy:.3f}",
                "r": "3.2",
                "fill": ORANGE,
                "opacity": "0.72",
            },
        )
    path = output_dir / "received_signal.svg"
    _write_svg(root, path)
    return path


def render_decision_regions(output_dir: Path, data: dict) -> Path:
    """Render the actual demodulator labels on a 401 x 401 grid."""
    labels = data["decision_labels"]
    palette = np.array(
        [
            [204, 220, 238],
            [242, 215, 185],
            [218, 222, 226],
        ],
        dtype=np.uint8,
    )
    image = Image.fromarray(palette[labels % 3])
    draw = ImageDraw.Draw(image)
    extent = data["decision_extent"]
    for point in data["constellation"]:
        px = (point.real + extent) * (GRID_SIZE - 1) / (2 * extent)
        py = (extent - point.imag) * (GRID_SIZE - 1) / (2 * extent)
        radius = 4
        draw.ellipse(
            (px - radius, py - radius, px + radius, py + radius),
            fill=(104, 114, 125),
        )
    path = output_dir / "decision_regions.png"
    image.save(path, format="PNG", optimize=True)
    return path


def _write_manifest(output_dir: Path, data: dict) -> Path:
    manifest = {
        "provenance": {
            "purpose": "mechanism-only figure asset",
            "paper_result": False,
        },
        "fixed_inputs": {
            "N": N,
            "snr_db": SNR_DB,
            "scene": SCENE,
            "seed": SEED,
            "f_dot_source": "SimulationConfig().doppler.DOPPLER_HIGH",
        },
        "resolved_inputs": {"f_dot_hz_per_s": data["f_dot"]},
        "source_files": [
            "common/_modulation.py",
            "common/_channel.py",
            "params.py",
            "figures/fig1_v5_assets/generate_assets.py",
        ],
        "assets": {
            "constellation.svg": {"role": "formal (8,8)-16APSK constellation"},
            "block_fading.svg": {"role": "formal unsmoothed block-fading realization"},
            "carrier_phase.svg": {"role": "formal total carrier-phase realization"},
            "awgn_iq.svg": {"role": "reconstructed formal complex-AWGN I/Q samples"},
            "received_signal.svg": {
                "role": "impaired received-signal I/Q samples",
                "source_data": "rx_raw",
                "realization": "same fixed realization",
            },
            "decision_regions.png": {"role": "formal m16apsk_demod decision grid and points"},
        },
    }
    path = output_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def render_assets(output_dir: str | Path) -> tuple[Path, ...]:
    """Generate all five assets and their manifest in ``output_dir``."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = build_asset_data()
    paths = (
        render_constellation(output_dir, data),
        render_block_fading(output_dir, data),
        render_carrier_phase(output_dir, data),
        render_awgn_iq(output_dir, data),
        render_received_signal(output_dir, data),
        render_decision_regions(output_dir, data),
        _write_manifest(output_dir, data),
    )
    return paths


def main() -> None:
    render_assets(Path(__file__).resolve().parent)


if __name__ == "__main__":
    main()
