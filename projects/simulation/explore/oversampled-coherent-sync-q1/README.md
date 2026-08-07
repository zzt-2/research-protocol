# Oversampled coherent sync Q1 semantic smoke

This directory contains the isolated deterministic Probe authorized by T015.
It is a Groundwork Step 4a dimension-D semantic smoke, not a formal MVE,
testbed, production receiver, or source of paper-ready numbers.

The executable contract is frozen in `semantic_smoke_core.py` and emitted in
`artifacts/manifest.json`.  The diagnostic waveform is 56-GBd QPSK at 2 sps
with unit-energy RRC filters (`beta=0.1`, span 10 symbols), full TX/RX
convolution, and a fixed-seed 64-symbol preamble (`20260807`).  The exact
literature preamble is unavailable, so the span and sequence are explicit
implementation sentinels.  The aggregate TX/RX group delay is 20 samples.
`d=0` means that the TX-shaped waveform starts at the 10-sample frame guard
before RX matched filtering; no post-filter crop changes the fixed 188-sample
observation window.  Positive `tau` delays `y[n]=x[n-tau]`; positive CFO uses
`exp(+j 2 pi f n/Fs)`.

All four methods consume only `ReceiverVisible`.  `TruthMetadata` is separate
and is used only for offline scoring.  B0 is the strengthened staged common-
score chain, B1 is the complete timing bank, B2 is non-decreasing coordinate
refinement from B0, and C is the receiver-visible complete 3-D grid argmax.
They share one normalized profiled-complex-gain GLRT and one lexicographic
tie-break.  B1/C equivalence is a scientific structural question, not a claim
that C must win.

The residual population is exactly 75 cells per layer: `d={-8,0,8}` samples,
`tau={-0.4,-0.2,0,0.2,0.4}` samples, and CFO
`={-100,-50,0,50,100}` MHz.  Noiseless and deterministic -6 dB AWGN layers
are reported separately.  The -6 dB layer is a numerical-stress sentinel, not
an occurrence distribution.  The separate stress population uses truth CFO
`={-5,+5}` GHz and is never pooled into the primary metric.

Run from the repository root:

```powershell
python -m pytest projects/simulation/tests/test_oversampled_coherent_sync_q1.py -q
python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --identity-only
python projects/simulation/explore/oversampled-coherent-sync-q1/run_semantic_smoke.py --run-grid --output-dir projects/simulation/explore/oversampled-coherent-sync-q1/artifacts
```
