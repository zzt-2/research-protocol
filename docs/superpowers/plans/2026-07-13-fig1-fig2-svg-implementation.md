# Fig.1/2 SVG Implementation Plan

> **For agentic workers:** Implement this plan inline with a review checkpoint after rendering and visual QA.

**Goal:** Produce editable, paper-ready SVG sources for the D011 Fig.1 system overview and Fig.2 adaptive CPR mechanism without changing the old SVG or any simulation code.

**Architecture:** Use two independent SVG files. Fig.1 contains one low-density Tx-to-downstream raw path and an expansion callout; Fig.2 contains the continuous raw path plus parallel DA/NDA estimates and the SNR-threshold selector control lane. Render PNG previews only for visual QA.

**Tech Stack:** Hand-authored SVG 1.1, CSS-in-SVG, Python CairoSVG for preview rasterization if available, local image inspection.

## Global Constraints

- Freeze all visible labels to R022; no result numbers, crossover values, training lanes, or decorative miniatures.
- Use dark-blue solid raw data, green short-dashed phase estimates, orange dash-dot measurement/control; color is never the only encoding.
- Keep Fig.1 single-column-first and Fig.2 double-column-first; target readable labels at approximately 3.5 in and 7.16 in respectively.
- Do not modify `projects/simulation/figures/fig1_system_block.svg`.
- Do not choose draw.io/TikZ/image as the primary source; SVG remains the editable source.

---

### Task 1: Create Fig.1 system-overview SVG

**Files:**
- Create: `projects/simulation/figures/fig1_system_overview.svg`

- [x] Define a compact SVG canvas with five aligned modules: `Tx`, `FSO channel`, `Coherent Rx`, `Adaptive CPR`, `Common downstream DSP`.
- [x] Draw one dark-blue solid raw path only, with `Expanded in Fig. 2` as the sole CPR callout.
- [x] Keep the figure title-free and omit pilot, BER, crossover, parameter, and training text.
- [x] Rely on the caption specification for the single raw path; no redundant Fig.1 legend was added.

### Task 2: Create Fig.2 adaptive-CPR SVG

**Files:**
- Create: `projects/simulation/figures/fig2_adaptive_cpr.svg`

- [x] Define a compact 1100×560 SVG canvas with the raw path centered, estimator lane above, and measurement/control lane below.
- [x] Fork the same `r_k` input to `DA estimator` and `NDA estimator`; route `θ̂_DA` and `θ̂_NDA` to `Estimator selector` using green short-dashed arrows.
- [x] Route `Per-block SNR measurement → γ_blk → Fixed SNR threshold γ_th → Estimator selector` using orange dash-dot control arrows and a diamond threshold node.
- [x] Feed `Selected θ̂` laterally into `Phase compensation`; keep the dark-blue raw path continuous through to `Common downstream DSP`.
- [x] Use only the frozen R022 labels and no performance/result annotations.

### Task 3: Render previews and perform visual QA

**Files:**
- Create: `projects/simulation/figures/fig1_system_overview.png`
- Create: `projects/simulation/figures/fig2_adaptive_cpr.png`

- [x] Rasterize each SVG at approximately 300 dpi with equivalent local renderers (CairoSVG for vector PDF; Edge 3.125× for publication-style PNG previews; final PNGs are 1050×419 and 2150×1094 px).
- [x] Inspect full-size and target-width previews for label truncation, arrow crossings, line-type distinction, and raw-path continuity.
- [x] Confirm black/white readability by desaturating previews and checking line/shape redundancy.
- [x] Record PASS/PARTIAL findings in `S013-fig1-fig2-svg-implementation.md`; independent verifier review remains the final checkpoint.
