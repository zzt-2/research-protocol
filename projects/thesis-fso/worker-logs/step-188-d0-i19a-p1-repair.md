# Step 188 — D0 I19A P1 minimal repair

> 2026-08-11 | author repair | bounded code task | hard stop <15 min

## Status

```text
RESULT=AUTHOR_REPAIR_GREEN
P0=0
P1_CODE_REPAIRED=2
P1_INDEPENDENT_CLOSURE=PENDING_FRESH_I19A_REVIEW
P2=1
P2_DISPOSITION=DEFERRED_NONBLOCKING
SCIENCE=NOT_RUN
METHOD_SIGNAL=NONE
```

## P1-1 — real ReceiverView front end

- Root cause: `channel.build_views()` copied `physical.received` into
  `equalized_samples` and materialized an all-zero CPR trace, bypassing the
  already-implemented receiver primitives.
- RED: new WC regression exercised the real owner-loaded 14 dB / 20 kHz
  `build_views()` path and required the exact composition
  `prefix RSS/31 -> scalar visible-power equalizer -> common BPS(32,31) ->
  four-state global resolution -> odd-prefix C_post`.
- Production repair: `channel.py` now composes those truth-free primitives per
  polarization and stores the real resolved samples, real BPS phase traces,
  selected four-state receipts, and observation-only `C_post_cplx` receipts.
  No 2x2 LS, TX truth, physical SNR, or feedback of C_post enters the path.
- GREEN focused: `1 passed in 14.05s`.

## P1-2 — authenticated O1 boundary

- Root cause: public exact-type dataclass construction plus caller-controlled
  `is_frozen=True` allowed forged `FrozenDeployableOutputs` and
  `ControlledFixture` objects to enter O1 without the deployment seal.
- RED: new RM regression required a real `DeploymentBoundary.seal(...)`, an
  issued controlled fixture, and a fixture-bound output freeze; public ctor,
  invalid preseal, `copy.copy`, `object.__new__`, and tamper paths must reject.
- Production repair: both boundary objects now have controlled constructors,
  weak-reference issuance registries, structural fingerprints, and tamper
  checks. `freeze_deployable_outputs()` re-authenticates the real
  `DeploymentSeal`, authenticates and binds one issued fixture, then signs the
  exact B0/B1 object identities. `evaluate_o1_inverse()` re-authenticates the
  output bundle, deployment seal, and exact fixture identity before using the
  evaluator-only inverse.
- GREEN focused: RM12 plus the new forgery regression, `2 passed in 4.63s`.

## Fresh affected verification

Command (no cache/bytecode):

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:PYTHONHASHSEED='0'
python -B -m pytest -p no:cacheprovider \
  projects/simulation/tests/test_d0_waveform_channel.py \
  projects/simulation/tests/test_d0_receiver_codec_methods.py \
  projects/simulation/tests/test_d0_contract_views.py -q
```

Result: `57 passed in 69.29s`; measured process wall time `72.23s`; exit `0`.
This is the full affected WC/RM/CV set. The I05 five-file chain, science, and
real benchmark were not run.

## Final SHA-256

| File | SHA-256 |
|---|---|
| `channel.py` | `bd434893e474be163abf4d0c1519f5aa1bb400bb547cd6b768fd2da799e06e85` |
| `methods.py` | `3912601de2528c3c3155ee7e5c74ccf92233e7b95b3bab51b2a9af25aef3d977` |
| `test_d0_waveform_channel.py` | `c076f760107b113f9fca642164b507126966d140898b2299c7e6ae4340825dbc` |
| `test_d0_receiver_codec_methods.py` | `ff455e9e8a7740f20c2eb5d95db3130e12366ad53ef9020e1abbc7da43f136b` |

`git diff --check` exited `0`. No `common/` status entry appeared. The four
protected `p05_run*.log` files remain the same untracked files and were not
modified or staged.

## Deferred issue

I19A P2 (`channel.py` physical constructor silent defaults) is
`DEFERRED_NONBLOCKING` exactly as assigned. No production or test change was
made for it.

