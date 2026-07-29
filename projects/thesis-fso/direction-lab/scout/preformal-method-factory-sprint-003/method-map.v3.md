# Method Map — Sprint 003 (update-granularity CMA family)

> Schema: `direction-lab.preformal-method-factory-sprint-003.v3`
> Authority: T027 (PREFORMAL_METHOD_FACTORY, epoch 61 / CP025); D035 / V061.
> Common gradient identity for ALL constructs: **Godard-with-z** `dw ∝ (R²-|z|²)·z·r*`
> (provenance `cb1_cell_runner.py:124-129`). The scalar-error form
> `dw ∝ (R²-|z|²)·r*` (`common/_cma.py:161-166`, MISSING the z factor) is
> FORBIDDEN as the comparator.

## Family definition

Every construct acts **directly on raw `rX/rY`** and produces its **OWN**
equalized z-stream. The lever is the **update granularity** of the equalizer
weight (when/how often weights move), NOT a z-only post-processing of the
block-64 baseline's output. This is the fundamental difference from
sprint-001/002 (M1-M5), which were z-only post-processing variants.

Common inputs (receiver-visible only): raw `rX/rY`, public 16QAM alphabet
geometry, frozen public params (FROZEN_AXES). Forbidden: TX truth, true
channel/Jones, future suffix, oracle coefficients at runtime.

## Constructs

### (a) `block64_cma_mu0p03` — inherited shared-anchor (identity reference)

| field | value |
|---|---|
| deployable_action | block-end averaged Godard-with-z CMA, block_size=64, mu=0.03 FROZEN |
| update_granularity | block_end_averaged (1/64 updates per symbol) |
| raw_input | rX, rY (full signal; scored on [cal, ee)) |
| frozen_params | mu=0.03 (inherited from frozen-params-b01r-v1.yaml, NOT re-tuned), R2=1.32, n_tap=11, block_size=64 |
| role | inherited anchor + identity reference. NOT the Go comparator. |
| provenance | `cb1_cell_runner.standard_cma_godard_with_z`; gradient `cb1_cell_runner.py:124-129` |

### (b) `persymbol_cma_godard_with_z` — TRADITIONAL COMPARATOR

| field | value |
|---|---|
| deployable_action | per-symbol immediate Godard-with-z CMA: each symbol produces z=W·r, then weights update immediately with `dw = mu·(R²-|z|²)·z·conj(r)` |
| update_granularity | per_symbol_immediate (1 update per symbol) |
| raw_input | rX, rY (full signal; scored on [cal, ee)) |
| frozen_params | mu (dev-tuned, frozen), R2=1.32, n_tap=11, center-tap init |
| role | the tuned traditional comparator. Go comparator for the signal gate. |
| gradient_provenance | `cb1_cell_runner.py:124-129` (block-end averaged form `(eX*zx_blk)[:,None]*conj(rX_blk)` then `mean`; the per-symbol analogue drops the `mean`). Identity UNCHANGED (canonical Godard-with-z, contains the z factor). |

### (c) `block8_cma_godard_with_z` — smaller-block candidate

| field | value |
|---|---|
| deployable_action | block-end averaged Godard-with-z CMA, block_size=8 (8x more updates per symbol than block-64) |
| update_granularity | block_end_averaged (1/8 updates per symbol) |
| raw_input | rX, rY |
| frozen_params | mu (dev-tuned per block_size), R2=1.32, n_tap=11, block_size=8 |
| difference_from_comparator | SAME block-end averaged gradient identity, only block_size differs (8 vs per-symbol). Isolates "smaller block granularity" from the per-symbol immediate mechanism. |

### (c) `block16_cma_godard_with_z` — smaller-block candidate (intermediate)

| field | value |
|---|---|
| deployable_action | block-end averaged Godard-with-z CMA, block_size=16 (4x more updates per symbol than block-64) |
| update_granularity | block_end_averaged (1/16 updates per symbol) |
| raw_input | rX, rY |
| frozen_params | mu (dev-tuned per block_size), R2=1.32, n_tap=11, block_size=16 |
| difference_from_comparator | SAME block-end averaged gradient identity, intermediate block granularity. |

### (d) `sliding_window_recursive_cma` — recursive-memory candidate

| field | value |
|---|---|
| deployable_action | per-symbol update rate but accumulates the Godard-with-z gradient with a recursive (leaky) running mean: `g_acc <- lam·g_acc + (1-lam)·g_inst`, `W <- W + mu·g_acc`, where `g_inst = (R²-|z|²)·z·conj(r)` |
| update_granularity | per_symbol_recursive_running_mean (1 update per symbol, but smoothed by recursive memory) |
| raw_input | rX, rY |
| frozen_params | mu (dev-tuned), lam=0.9 (frozen forgetting factor), R2=1.32, n_tap=11 |
| difference_from_comparator | SAME per-symbol update RATE as the comparator, but the gradient is smoothed by a recursive window — "block memory on top of per-symbol rate". A distinct mechanism from both pure per-symbol (instantaneous) and block-end (averaged then idle). |

## Difference from rejected / prior axes (dedup)

| axis / construct | how sprint-003 differs |
|---|---|
| **sprint-001 M1-M5 / sprint-002 M1-M4** | Those were z-only post-processing / triggering / initialization families acting on the block-64 OUTPUT z. Sprint-003 constructs act on RAW rX/rY and produce their OWN z. Different receiver step. |
| **§3.1 rejected frequency-domain/subband family** | That family has NO physical DOF on this channel (`_dual_pol_channel.py:127-132` is memoryless, flat — no dispersion/multipath/FIR). Sprint-003 acts in the TIME domain on the update granularity, a real code-imposed knob. No frequency-domain/subband processing. |
| **C04 / C09 / C12 / C14 / C15 / C16** | Those are prior comparator / closure candidates (blind-affine, C11-DD-LMS, oracle). Sprint-003's comparator is a tuned per-symbol Godard-with-z CMA (a different traditional algorithm at a different update step), not a re-use of those. |
| **T019 M5 per-symbol nearest-shell remap** | M5 remapped the EVAL suffix |z| onto shells (z-only, suffix-dependent selection — V052 reject cause). Sprint-003 per-symbol updates the EQUALIZER WEIGHT each symbol from raw rX/rY; the suffix never selects anything. |
| **scalar-error `_cma.py` CMAEqualizer2x2 as comparator** | FORBIDDEN. That class implements `(R²-|z|²)·conj(r)` (missing z, `_cma.py:161-166`). The sprint-003 comparator uses the canonical Godard-with-z `(R²-|z|²)·z·conj(r)` (contains z). Gradient identity differs. |
| **block_size as a "knob demonstration" only** | Sprint-003 uses block-8/16 as DEPLOYABLE CANDIDATES with dev-tuned mu and a comparator-aware signal gate, not merely to demonstrate block_size is a knob. |

## Effective-update-budget fingerprint

| construct | updates per symbol | dev-frozen mu |
|---|---|---|
| block64_cma_mu0p03 (anchor) | 1/64 = 0.0156 | 0.03 (inherited) |
| block16_cma_godard_with_z | 1/16 = 0.0625 | 0.003 |
| block8_cma_godard_with_z | 1/8 = 0.125 | 0.003 |
| persymbol_cma_godard_with_z (comparator) | 1.0 | 0.001 |
| sliding_window_recursive_cma | 1.0 | 0.0003 |

The per-symbol/block-8/block-16 methods have far more updates per symbol than
block-64, which is exactly why the **ablation** is mandatory: a candidate win
must survive a matched effective-update-budget comparison or it is a
"more-updates" artifact, not a granularity signal.
