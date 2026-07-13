# CCISP Figures 2--4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Redraw Fig.2--4 from existing verified JSON using the approved paper-level visual specification, without changing Fig.1 or running simulations.

**Architecture:** Each plotting script owns one independent figure and writes a vector PDF plus a PNG preview. Shared semantics are coordinated through R018: identical SNR/BER labels, Times-compatible typography, scenario colors, line weights, and no in-plot headline.

**Tech Stack:** Python, NumPy, Matplotlib, SciPy, existing JSON results.

## Global Constraints

- Do not run simulations or change result JSON.
- Do not modify Fig.1.
- Final outputs are vector PDF; PNG previews are at least 300 dpi.
- No in-plot headline, selling-point arrow, large text box, CI, or unexplained dB metric.
- Use final-size fonts: axis labels 9 pt; ticks/legend 8.5--9 pt; main lines 1.1--1.5 pt; reference lines 0.7--0.9 pt.
- Use one conversation-level commit only after independent verification.

### Task 1: Fig.2 BER overview

**Files:** Modify `projects/simulation/figures/plot_fig2_ber.py`; regenerate `ccisp_fig2_ber.pdf/.png`.

- [x] Remove all point-value selling annotations and in-plot headline behavior.
- [x] Apply short panel labels, shared axis labels, professional HD-FEC formatting, final-size fonts and vector output.
- [x] Run the script and verify six panels, data source counts, dimensions and absence of annotation strings.

### Task 2: Fig.3 BER-reduction scan

**Files:** Modify `projects/simulation/figures/plot_fig3_gain.py`; regenerate `ccisp_fig3_gain.pdf/.png`.

- [x] Replace the old six-scenario fair/naive plot with three complete BER-reduction curves from `_a4_switch_30seed_fixed.json`.
- [x] Label the metric as BER reduction relative to fixed NDA and define the formula in code/caption metadata; never call it SNR gain.
- [x] Run the script and verify 21 points, positive-is-better orientation, zero reference line and no forbidden old labels.

### Task 3: Fig.4 crossover comparison

**Files:** Modify `projects/simulation/figures/plot_fig4_crossover.py`; regenerate `ccisp_fig4_crossover.pdf/.png`.

- [x] Remove the in-plot headline, HD-FEC line, large crosses/arrows and six-combination legend.
- [x] Use small crossover markers, approximate one-decimal labels and separate scenario-color/method-line legends.
- [x] Run the script and verify the reproducible log-BER-linear crossover labels 18.0/16.9/10.7 dB and consistent axes/style with Fig.2.

### Task 4: Independent verification and governance closeout

**Files:** Update `S011-figure-visual-spec-and-redraw.md`, `topic-index.md`, and `.sessions/_registry.yaml` after verification.

- [x] Independently compare plotted arrays against source JSON and inspect all PNGs at realistic final size.
- [x] Run deterministic grep/style checks and `git diff --check`.
- [x] Fix all Critical/Important findings and update the verification record in S011/V001.
