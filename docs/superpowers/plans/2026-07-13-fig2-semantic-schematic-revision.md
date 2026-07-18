# Fig.2 Semantic Schematic Revision Implementation Plan

> **For agentic workers:** Implement this plan inline with an independent visual review checkpoint after rendering.

**Goal:** Replace the rejected motif-board/card grammar with one concise, semantically grounded Fig.2 adaptive-CPR schematic.

**Architecture:** Keep the R022 three-lane information structure: a continuous dark-blue raw-data spine, parallel DA/NDA phase-estimate branches, and a separate measurement/threshold/selector control lane. Use meaningful primitives only: layered processing plates, a threshold diamond, a selector hexagon, measurement branch, and a lateral estimate port into phase compensation.

**Tech Stack:** Hand-authored SVG 1.1 as the editable source, local SVG-to-PNG/PDF rendering for QA, and visual inspection at paper width.

## Global Constraints

- Use only the frozen R022 labels: `r_k`, `Per-block SNR measurement`, `γ_blk`, `Fixed SNR threshold γ_th`, `DA estimator`, `NDA estimator`, `Estimator selector`, `θ̂_DA`, `θ̂_NDA`, `Selected θ̂`, `Phase compensation`, `Common downstream DSP`, plus `Data path`, `Phase-estimate path`, `Control path` if needed.
- Preserve the semantic flow: `r_k` forks to DA/NDA and the measurement branch; raw data bypasses the selector; `Selected θ̂` enters `Phase compensation` laterally; compensated data continues to `Common downstream DSP`.
- Use dark-blue solid for raw data, green short-dashed for phase estimates, and orange dash-dot for measurement/control; shape and position must remain understandable in grayscale.
- Meaningful primitives only: layered plates for repeated estimator processing, a meter/branch for measurement, a diamond for fixed threshold, a hexagon/narrow trapezoid for selector, and a side port for estimate injection. No arbitrary inner bars, decorative icons, shadows, gradients, or performance annotations.
- Deliver editable SVG and paper-size PNG preview; do not modify Fig.1 or simulation code.

---

### Task 1: Build the semantic Fig.2 SVG

**Files:**
- Modify: `projects/simulation/figures/fig2_adaptive_cpr.svg`

**Interfaces:**
- Consumes: R022 §3.2–§3.5 and the four user-provided reference schematics.
- Produces: a 1100×560 SVG with one continuous raw spine, two parallel estimator branches, one control branch, and a lateral estimate injection.

- [ ] Replace the card-and-bars motif with semantically meaningful geometry while preserving the frozen label list.
- [ ] Keep arrowheads small and subordinate; ensure no connector crosses text or reverses direction.
- [ ] Use correct math typography for `r_k`, `γ_blk`, `γ_th`, `θ̂_DA`, `θ̂_NDA`, and `Selected θ̂`.
- [ ] Add a compact legend only if the three line encodings are not self-evident at paper size.

### Task 2: Render and review the prototype

**Files:**
- Create/modify: `projects/simulation/figures/fig2_adaptive_cpr.png`
- Create/modify: `projects/simulation/figures/fig2_adaptive_cpr.pdf`

- [ ] Render the SVG at paper-preview resolution.
- [ ] Inspect full-size and reduced-width previews for semantic traceability, label correctness, arrow crossings, and grayscale distinction.
- [ ] Report any remaining issue as PASS/PARTIAL/FAIL with file/region evidence before claiming completion.
