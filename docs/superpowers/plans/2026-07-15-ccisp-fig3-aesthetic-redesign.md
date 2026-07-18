# CCISP Fig.3 A2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use test-driven-development. Do not commit; the root agent performs the conversation's single final commit.

**Goal:** Reproduce the approved A2 preview in the authoritative Fig.3 plotting pipeline without changing scientific data or algorithms.

**Architecture:** Add regression assertions for the visual contract, then make a local presentation-only edit in `plot_fig2_ber.py`, regenerate the stable PDF/PNG, and verify the final IEEEtran embedding. Existing data loading and smoothing functions remain byte-for-byte equivalent.

**Tech Stack:** Python, Matplotlib, pytest, latexmk, PDF font/layout inspection.

## Global Constraints

- Modify only `plot_fig2_ber.py`, `ccisp_fig2_ber.pdf/png`, and the typography regression test.
- Keep all data sources, arrays, scene order, `HD_FEC=3.8e-3`, `merge_scene()`, `smooth_curve()`, and `set_yrange()` unchanged.
- Use three unmarked solid lines in the existing blue/orange/green colors.
- AWGN x major/minor ticks: 5/2.5 dB; other scenes: 10/5 dB.
- Use a thin solid gray HD-FEC line, direct-label it once in panel (a), and omit it from the global legend.
- Use a frameless three-column bottom legend with labels `DA-ML`, `NDA-ML`, `Oracle`.
- Preserve Times/STIX and final 10/9 pt typography.

---

### Task 1: Implement and verify A2

**Files:**
- Modify: `projects/simulation/tests/test_ccisp_figure_typography.py`
- Modify: `projects/simulation/figures/plot_fig2_ber.py`
- Regenerate: `projects/simulation/figures/ccisp_fig2_ber.pdf`
- Regenerate: `projects/simulation/figures/ccisp_fig2_ber.png`

**Interfaces:**
- Consumes: existing `SCENES`, `CURVE_SPECS`, `HD_FEC`, `merge_scene`, `smooth_curve`, `set_yrange`.
- Produces: stable Fig.3 PDF/PNG matching the approved A2 visual contract.

- [ ] Add failing tests asserting all method linestyles are solid, no method markers are drawn, tick spacings are frozen, HD-FEC is solid/direct-labeled, and the global legend is frameless with exactly three short labels.
- [ ] Run the focused tests and confirm RED failures arise from the current dashed/dotted/marker/boxed-legend implementation.
- [ ] Implement the minimal presentation-only changes in `plot_fig2_ber.py` using `MultipleLocator` and compact legend handles.
- [ ] Regenerate stable PDF/PNG from the authoritative script.
- [ ] Run typography and structural regression tests; confirm all pass.
- [ ] Fresh-build `main.pdf`, inspect Fig.3 at final single-column size, and verify embedded Times/STIX fonts and no clipping.
- [ ] Obtain independent verifier PASS for visual contract and scientific-semantic freeze.
