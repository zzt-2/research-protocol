# Step 175 — D0 I09 scalar receiver / common BPS

> 2026-08-11 | executor `/root/i09_receiver` | status: DONE

## Scope

- Production: `projects/simulation/explore/coded-decoder-feedback/receiver.py`
- Tests: `projects/simulation/tests/test_d0_receiver_codec_methods.py`
- Test IDs: RM01–RM06; aggregate file also covers the existing RM07–RM10/negative codec cases.
- Frozen exclusions respected: no `common/` edit, no science/S1–S4, no physical SNR or truth input, no 2x2 LS, no eight-state/TX resolver, no `p05_run*.log` touch, no stage/commit/push.

## RED receipt

Environment:

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
flags=-B -p no:cacheprovider
```

Exact command:

```powershell
& $py -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm01_one_complex_gain_uses_rss_over_31 projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm02_scalar_equalizer_and_noiseless_branch projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm03_common_bps_six_cell_exact_and_receipt projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm04_common_bps_rejects_outside_frozen_six_cell_grid projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm05_global_resolution_uses_four_states_and_even_prefix_only projects/simulation/tests/test_d0_receiver_codec_methods.py::test_rm06_post_bps_residual_is_odd_only_and_never_equalizer_input -q
```

```text
exit=1
observed=6 failed in 0.38s
expected_root_cause=ModuleNotFoundError: No module named 'receiver'
RED_TEST_SHA256=af57218227107e7b54249450a9d9024e14aa0cb15111ba53ab55f18dd7717e8e
RED_PRODUCTION=ABSENT
RED_CANONICAL_RECEIPT_SHA256=a64e6c47c1b8fe122cb35664e24784a6e1b0c2b9d655a06c0c0df99c92a293a4
```

The initial invocation was not piped to a byte-capture sink, so the digest above is explicitly the canonical three-line receipt (`exit/count/root_cause`), not a falsely claimed full-console-byte digest. The complete traceback remains in the executor tool transcript.

## Implementation

- `estimate_prefix_calibration`: exactly one complex LS gain over 32 prefix symbols; `C_pre_cplx=RSS/31`; typed receipt.
- `scalar_visible_power_equalize`: absolute-time 100-symbol blocks, observed-only visible power `max(mean(|r|^2)-C_pre,0)`, frozen scalar MMSE expression, exact noiseless inverse-root branch, amplitude limit 3.0.
- `run_common_bps`: rejects values outside `{32,64} x {31,61,127}`, calls the read-only `common._recovery.bps_cpr(..., mod='qam16')` kernel and returns exact phase/output plus edge-rule receipt.
- `resolve_global_symmetry`: only states `{0,1,2,3}`, only even prefix indices `0..30`, negative pi/2 state rotation over the whole polarization, lower-state tie break.
- `estimate_post_bps_residual`: only odd prefix indices `1..31`; output-only API. The equalizer signature has no `C_post` input.

## GREEN receipts

Focused RM01–RM06, first GREEN:

```text
6 passed in 2.85s
process elapsed=3.582s
```

Whole file (RM01–RM10 plus existing negative/schema cases):

```text
15 passed in 5.71s
process elapsed=7.193s
```

Fresh final focused capture, same exact node command as RED:

```text
6 passed in 1.37s
process elapsed=2.083s
RAW_OUTPUT_SHA256=fb06be0765e83a121766a431badbf4b5e658484ef7d68ebf045206ac10377a05
```

Measured pytest process time total: `12.858s`; all implementation/read/edit/audit activity remained inside the 15-minute executor timebox.

## Final identities and guards

```text
test SHA256=af57218227107e7b54249450a9d9024e14aa0cb15111ba53ab55f18dd7717e8e
receiver SHA256=67c9d9818b7b8894d35d1a3457476f4ab9dcdb780adf9330c2b1173a13b1d545
owner SHA256=f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b
common BPS source SHA256=afb8aed9508cc83ee13d05bfd4346a2e6f0852af0e9d6a182a85a441ff5d60e2
source-bundle SHA256=0498348975da74105fcbf4aa5e051bbce0233a076af3f1741db31698d59046fa
git diff --check=PASS
forbidden-token scan=0 hits
p05_run*.log status=the same four untracked protected files; untouched
```

## Verdict

```text
STATUS=DONE
AUTHOR_GATE=GREEN
P0=0
P1=0
FAILURE_POINTS=none after the intended missing-module RED
NEXT_INTERFACE=I12 methods.py and I14 b2.py may consume the receiver primitives after the one-per-batch independent acceptance gate
SCIENCE_STATUS=NOT_RUN
METHOD_SIGNAL=NONE
```

`sim-preflight` usage-log writing was not performed because the executor's explicit file allowlist permits only receiver, its test, and this worker log; no parameter/formula/evaluation convention changed.
