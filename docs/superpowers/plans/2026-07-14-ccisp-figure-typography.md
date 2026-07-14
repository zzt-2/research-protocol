# CCISP Figure Typography Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make CCISP Fig.1–Fig.5 use a Times/STIX typography hierarchy anchored to the final IEEEtran 10 pt body size without changing scientific semantics.

**Architecture:** Treat the final embedded PDF as the typography truth. Matplotlib scripts expose explicit physical sizes and font constants; draw.io sources retain their graph structure while visible labels are resized and mathematical labels move to the renderer's math mechanism. Contract tests inspect source settings and exported PDF geometry before the paper is rebuilt and visually reviewed.

**Tech Stack:** Python 3.11, Matplotlib, PyMuPDF, pytest, diagrams.net draw.io XML/CLI, IEEEtran/latexmk, Poppler.

## Global Constraints

- Do not change data, result JSON, curves, interpolation, crossover detection, thresholds, legends' meaning, line-style meaning, node structure, control logic, captions, or paper claims.
- Never run or restore a historical Fig.1 builder; the user-adjusted draw.io files are the only editable masters.
- Keep final asset names stable; do not retain v2/v3 candidates.
- Final effective sizes: major labels 10 pt, ordinary annotations 9 pt, ticks/legends/secondary annotations 8.5–9 pt, no readable text below 8 pt.
- Ordinary text uses Times New Roman or a reliable Times-compatible serif; mathematics uses STIX or the draw.io mathematical-typesetting mechanism.
- All PDF fonts must be embedded; Helvetica, DejaVu Sans, and Type 3 are forbidden.
- One commit only at the end of this conversation.

---

### Task 1: Typography contract tests

**Files:**
- Create: `projects/simulation/tests/test_ccisp_figure_typography.py`
- Test: `projects/simulation/tests/test_ccisp_figure_typography.py`

**Interfaces:**
- Consumes: the five authoritative figure sources and three current figure PDFs.
- Produces: deterministic assertions for physical size, font settings, draw.io math mode, visible source font floors, and stable PDF font families.

- [ ] **Step 1: Add source and exported-PDF contract assertions**

Implement tests that import `FIGSIZE_IN`, `FONT_SIZES`, and `MPL_RCPARAMS` from each plot module; assert native single-column width `3.5`, label/title `10`, ticks/legend `>=8.5`, `text.usetex=False`, STIX math, normal weight, and PDF Type 42. Parse draw.io XML, assert `math=1`, specific major IDs at `>=29`, all visible Times labels above the source floor, and math-label IDs use `\(...\)` rather than HTML italics. Use PyMuPDF to assert the three data PDFs have 252 pt page width and only embedded Times/STIX-compatible fonts.

- [ ] **Step 2: Run RED**

Run: `C:\Users\zzt\.venvs\torch\Scripts\python.exe -m pytest projects/simulation/tests/test_ccisp_figure_typography.py -q`

Expected: FAIL because the plot modules do not yet expose the contract constants, Fig.3/Fig.4 are wider than 252 pt, and both draw.io roots still have `math=0`.

### Task 2: Matplotlib figures

**Files:**
- Modify: `projects/simulation/figures/plot_fig2_ber.py`
- Modify: `projects/simulation/figures/plot_fig3_gain.py`
- Modify: `projects/simulation/figures/plot_fig4_crossover.py`
- Regenerate: `projects/simulation/figures/ccisp_fig2_ber.pdf`
- Regenerate: `projects/simulation/figures/ccisp_fig2_ber.png`
- Regenerate: `projects/simulation/figures/ccisp_fig3_gain.pdf`
- Regenerate: `projects/simulation/figures/ccisp_fig3_gain.png`
- Regenerate: `projects/simulation/figures/ccisp_fig4_crossover.pdf`
- Regenerate: `projects/simulation/figures/ccisp_fig4_crossover.png`

**Interfaces:**
- Consumes: unchanged JSON paths, fields, curve algorithms, constants, colors, line styles, and output filenames.
- Produces: `FIGSIZE_IN`, `FONT_SIZES`, `MPL_RCPARAMS` plus native single-column PDFs.

- [ ] **Step 1: Expose and apply the shared contract in each existing script**

Use the same fallback list `['Times New Roman', 'Times', 'Nimbus Roman No9 L', 'DejaVu Serif']`; set `text.usetex=False`, `mathtext.fontset='stix'`, `font.weight='normal'`, `axes.labelweight='normal'`, `pdf.fonttype=42`, and `ps.fonttype=42`. Use label/title 10 pt and ticks/legend/annotations 9 pt.

- [ ] **Step 2: Reflow only the BER overview layout**

Keep the same 3x2 scene order and curves, but set a native 3.5 in width, use a two-column legend, and tune height/margins so no label or legend overlaps. Do not change `merge_scene`, `smooth_curve`, `set_yrange`, the scene order, or any scientific constant.

- [ ] **Step 3: Retarget crossover and gain figures to native single-column size**

Use 3.5 in width, explicit subplot margins, no `bbox_inches='tight'` page-box drift, 300 dpi PNG output, 10 pt axis labels, and 9 pt tick/legend/annotation text. Do not change `find_crossover`, `log_linear_curve`, `load_scan`, plotted fields, line styles, or captions.

- [ ] **Step 4: Regenerate and run contract tests**

Run all three scripts from the repository root using `C:\Users\zzt\.venvs\torch\Scripts\python.exe`, then rerun the typography test. Expected: Matplotlib assertions PASS; draw.io assertions remain FAIL until Task 3.

### Task 3: Fig.1 and Fig.2 draw.io typography

**Files:**
- Modify: `projects/simulation/figures/fig1_system_model_v5.drawio`
- Modify: `projects/simulation/figures/fig2_adaptive_cpr.drawio`
- Regenerate: `projects/simulation/figures/fig1_system_model_v5.pdf`
- Regenerate: `projects/simulation/figures/fig1_system_model_v5.png`
- Regenerate: `projects/simulation/figures/fig2_adaptive_cpr.pdf`
- Regenerate: `projects/simulation/figures/fig2_adaptive_cpr.png`

**Interfaces:**
- Consumes: current user-adjusted cell IDs, geometry, edge bindings, colors, values, and embedded assets.
- Produces: the same graphs with `math=1`, resized visible labels, and math-rendered variables.

- [ ] **Step 1: Raise source font sizes to meet final effective sizes**

For Fig.1 use a visible-label source floor of 25 px and major labels around 30 px; for Fig.2 use a visible-label source floor of 24 px and major labels around 29 px. Resize or rewrap text boxes only where needed; do not add, delete, or reconnect cells.

- [ ] **Step 2: Convert only mathematical labels**

Enable `math=1`. Replace the existing HTML-italic/Unicode constructions for `s_k`, `r_k`, `\hat\theta_{DA}`, `\hat\theta_{NDA}`, `\tau_{CV}`, `\hat h_{dsp}`, and `\hat\gamma_{eff}` with draw.io inline mathematical typesetting. Keep surrounding prose and decision meanings unchanged.

- [ ] **Step 3: Run structural validation and existing Fig.2 regression tests**

Run the global draw.io validator on both files and `pytest projects/simulation/tests/test_fig2_two_layer_drawio.py -q`. If the exact-style regression rejects typography-only style changes, update only its expected font-size portions while retaining all endpoint, geometry, color, dash, and arrow assertions.

- [ ] **Step 4: Export from the authoritative draw.io files**

Use `D:\Software\drawio\draw.io\draw.io.exe --export` directly on each current draw.io source. Export to temporary staging, inspect page size/fonts, then replace the stable PDF/PNG names and delete staging files. Never run the historical builder or `fig1_v5_assets/generate_assets.py`.

### Task 4: Final paper verification

**Files:**
- Regenerate: `projects/simulation/paper/ccisp2026/main.pdf`
- Update: `.sessions/2026-07-14-ccisp-figure-typography/S001-five-figure-typography-contract.md`
- Create when evidence exists: `.sessions/2026-07-14-ccisp-figure-typography/verifications.md`

**Interfaces:**
- Consumes: all five stable figure PDFs and unchanged LaTeX sources.
- Produces: fresh seven-page paper evidence and independent PASS/PARTIAL/BLOCKED verdict.

- [ ] **Step 1: Fresh build and deterministic checks**

Run `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`. Record timestamp, bytes, pages, warnings, font table, figure placements, and effective font-size extraction from the final PDF.

- [ ] **Step 2: Render and inspect every page**

Render all pages at 150 dpi and inspect the complete paper. For Fig.1–Fig.5 check clipping, overlap, mathematical glyphs, legend density, tick readability, visual balance, and caption separation at final size.

- [ ] **Step 3: Independent verifier**

Give a fresh verifier the source diff, all contract outputs, final PDF, rendered pages, and semantic exclusions. Require a PASS/PARTIAL/BLOCKED verdict; do not claim completion on self-review alone.

- [ ] **Step 4: Record evidence and commit once**

Update S001 and verifications.md with exact evidence. Commit only the in-scope source, export, test, and governance files once at conversation close; preserve every unrelated dirty-worktree change.
