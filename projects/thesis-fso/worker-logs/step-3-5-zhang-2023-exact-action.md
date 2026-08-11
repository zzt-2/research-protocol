# Step 3.5 targeted fulltext read — Zhang 2023 exact action

> Task: T014 | date: 2026-08-11 | scope: Q001 collision evidence only

## Identity and source gate

- Dispatch title: *Flexible Phase Synchronization for Coherent Free-Space Optical Communications Based on Adaptive Fractionally-Spaced Blind Equalization Combined With Adaptive Kalman Filter*.
- Fulltext title: *Flexible Phase Synchronization for Wireless Optical Coherent Communication System With Adaptive Fractionally-Spaced Blind Equalization Combined With Adaptive Kalman Filter*.
- Stopword-normalized token Jaccard: `0.667 >= 0.4`; title gate **PASS**. The wording differs, but the unique method phrase and authors/DOI match.
- Authors: ShuPeng Zhang, LiYing Tan, Jing Ma.
- DOI: `10.1109/JPHOT.2023.3328423`.
- Source: `papers/downloads/2026-07-08/10301506.md`, 56,723 bytes, SHA256 `AFCE9FB293BC12F5638239D03F3B31A76068B31D48B528C8E82BCD091DAD45CF`.
- Evidence: source lines `5-19`.

## Exact action signature

| field | fulltext-supported extraction | evidence |
|---|---|---|
| input | Four coherent-receiver aperture I/Q baseband streams, already frequency-recovered and timing-synchronized per branch. | `10301506.md:57-85,115,145-149` |
| branch position/order | `ADC -> frequency recovery/timing synchronization per branch -> joint FSE-MCMA+DD -> MEKF/AKF -> symbol decision`. | `:115,145,185,223` |
| trigger | MCMA/DD switch: real-time MSE outside decision circle uses MCMA; inside uses DD (`d=0.4`, `λ=0.99`). AKF-CM/AR updates measurement-noise variance from innovations. | `:171-179,197-223` |
| weight/admission/abstention | Continuous joint fractionally-spaced equalizer-tap updates (`L_f=6`, `μ=10^-3`). Every aperture is represented in the joint tap vector; no textual or mathematical branch admission/drop/zero action is defined. | `:149-169` |
| no-valid flag | Absent. | full method chain `:115-223` |
| statefulness | Equalizer taps, MSE forgetting state, last `N=10` phase estimates, MEKF/AKF state/covariances, and innovation history. | `:157-179,185-223` |
| output | One jointly equalized sequence `y_k`, followed by complex-phase-compensated recovered symbols. No branch-validity output. | `:151-157,185-223` |

## Q001 adjudication

Classification: **neighbor**.

Reasoning by field:

1. Input differs: Zhang consumes post-frequency/timing branch samples, not receiver-visible FS/phase-validity features.
2. Position overlaps only broadly: it is pre-decision receiver processing, but replaces branch-local corrected MRC with a joint FSE/estimator chain.
3. Trigger differs: MSE switches equalizer update law; innovations adapt Kalman noise variance. Neither trigger decides whether a branch is valid.
4. Action differs: adaptive tap estimation/combining, with no bounded branch reliability, admission or abstention.
5. Output differs: one recovered sequence, with no `no-valid` flag.

Therefore Zhang 2023 is a task-relevant estimator-changing comparator/neighbor, not an exact Q001 input-trigger-action-output collision and not evidence that validity-based branch abstention is already implemented.

## Sun 2019 citation audit

At line 129, Zhang describes only this Sun [28] fragment: under a time-varying channel, the input signals are divided by their modulus in the cost function; derivative calculation becomes more complex. Reference identity is confirmed at line 405 as Sun et al., Optics Communications 444 (2019), DOI `10.1016/j.optcom.2019.03.069`.

Supported bounded fragment:

`input signals -> modulus normalization in adaptive cost -> adaptive-combining calculation`

Still unknown from this citation:

- whether normalization is per aperture or on an aggregate;
- ordering relative to per-branch FS/CE/CPE;
- explicit trigger, weight update and weight bounds;
- branch zero/drop/admission/abstention;
- statefulness and no-valid flag;
- complete output semantics.

Zhang's FSE-MCMA+DD/MEKF/AKF chain cannot be attributed to Sun. This later-primary related-work statement narrows Sun's cost-function mechanism but does not close Sun's exact action.

## Boundary

This report does not judge the Step 3.5 terminal, propose an algorithm, enter Step 4a, implement or simulate.
