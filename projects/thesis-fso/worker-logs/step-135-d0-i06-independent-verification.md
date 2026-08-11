# step-135 — D0 I06 independent channel/truth verification

> 2026-08-10 | T089 / D011 / V005 / CP012 | action: `D0_TESTBED_IMPLEMENTATION`
> Fresh independent verifier; production/tests were read-only.

## 1. Findings first / verdict

```text
VERDICT=FAIL
P0=0
P1=3
P2=1
TERMINAL=I06_VERIFICATION_FAIL
```

The frozen tests are green and the physical equations, named RNG isolation,
sharing matrix, supplied-waveform equation, array immutability, and import
purity independently reproduce.  They do not close the owner contract: fresh
mutations expose a receiver-side oracle value, incomplete TruthView payload,
and multiple fail-closed holes not exercised by WC04–WC07.

### [P1-1] ReceiverView receives exact physical-SNR-derived noise power

- Owner basis: `d0-defect-smoke-contract.yaml:31,37-49,161-178` permits a
  prefix/pilot receiver estimate and forbids true SNR/physical truth.
- Code path: `channel.py:323-329` supplies `physical_cell.snr_db` to the
  realization; `channel.py:250` converts that truth to exact complex noise
  power; `channel.py:349,358-362` copies the exact value into both
  `ReceiverView.receiver_noise_estimate` and its receipt.
- Fresh observation for the 14 dB cell:
  `receiver_noise_estimate == receipt value == awgn_variances(14)[1] ==
  0x1.46211ff90ea2ap-5`.
- This is value-provenance leakage even though the field names pass the alias
  denylist.  It is not the owner-required prefix/pilot estimate.
- Reproduction: Windows Python `-B` inline script loading the owner, building
  `N=20`, calling `build_views(..., physical_cell=14dB/20kHz)`, and comparing
  both receiver values with `awgn_variances(cell.snr_db)`; output SHA256
  `eb2cedb4009b616cf293384643b7339d8a9a6d23272c5284d7d94497eb4be775`.

### [P1-2] Receiver/truth boundary is not structurally fail closed

- `contract.py:259-289` recursively checks mappings, dataclasses, and standard
  containers but has no generic `__slots__` branch.  A slots object with field
  `event_label` nested in `ReceiverView.receipts` was accepted.  The corrected
  WC06 helper checks slots, but its fixture never injects one.
- `contract.py:320-354,357-381` freezes arrays without enforcing cross-field
  shapes or array finiteness.  Fresh `dataclasses.replace` mutations accepted a
  `(1,3)` receiver array, an all-NaN receiver array, a `(1,1)` truth phase, and
  an all-NaN truth phase.
- `contract.py:496-518` seals only CP012 control identity.  `channel.py:317-321`
  therefore accepted contracts with forged population symbol rate and forged
  `information_bits_per_cw=2048`; a positive but wrong Receiver
  `WaveformLayout(prefix_symbols=31,...)` was also accepted.
- Owner basis: `d0-defect-smoke-contract.yaml:31-55,60-67,83-88,203-212` and
  T089 require exact contract/layout identity, recursive truth freedom, shape,
  and nonfinite rejection.
- Reproduction: the 18-case primary mutation script plus five focused
  shape/nonfinite mutations, executed by piping a PowerShell here-string to
  Windows Python `-B -`; output SHA256s
  `fa026675fd3dffd4f8b63977c80f803f9ce19e92e13c32e4951e3d59e7a68c79`
  and `eb2cedb4009b616cf293384643b7339d8a9a6d23272c5284d7d94497eb4be775`.

### [P1-3] The sole split factory returns an incomplete TruthView

- Owner basis: `d0-defect-smoke-contract.yaml:50-55` requires transmitted bits
  and symbols plus final codeword correctness on the evaluator-only side;
  step-094 §3.1 likewise specifies `[2,16,1024]` information bits and
  `[2,16,1536]` coded bits.
- `channel.py:365-381` returns `information_bits.shape=(2,0,1024)`,
  `coded_bits.shape=(2,0,1536)`, and
  `final_codeword_correctness.shape=(2,0)`.  These fields are frozen and the
  `build_views` signature has no input from which to populate the missing
  payload truth.
- Fresh output also confirmed that transmitted symbols, phase, channel, and
  fade have the complete `(2,6501)` shape; the defect is specifically the
  required bit/correctness payload, not the physical arrays.
- Reproduction output SHA256:
  `eb2cedb4009b616cf293384643b7339d8a9a6d23272c5284d7d94497eb4be775`.

### [P2-1] Integer/cell guards do not enforce frozen scalar types

- `channel.py:83-109` rejects bool, float, and negative roots but accepts
  `2**63`, outside the owner's serialized `int64` seed type
  (`d0-defect-smoke-contract.yaml:545-565`).
- `PhysicalCell` has no type validation (`contract.py:384-389`), and tuple
  membership in `channel.py:320` accepted an independently constructed cell
  with `float(14)`/`float(20000)` because dataclass equality equates those with
  registered ints.
- Reproduction output SHA256s: primary mutation
  `fa026675fd3dffd4f8b63977c80f803f9ce19e92e13c32e4951e3d59e7a68c79`;
  focused cell check
  `eb2cedb4009b616cf293384643b7339d8a9a6d23272c5284d7d94497eb4be775`.

No source or test was changed to address these findings.

## 2. Frozen-input and protection preflight

All T089 frozen identities matched:

```text
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test_d0_waveform_channel.py=ce5b80b262612943ada9e5677ff27713bef8dafd9cf17c6f8e537d464da5c3b0
step-130=7d787b55f12b84a654bd87c453669b8bd317f2da6cb2b02a1f2a267e1de706b7
step-133=d0d8ca7b4b7c202289028ca52f2d43025b21ef75ad72a9766f68a89eb5a0bdc3
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
```

## 3. Fresh deterministic/unit receipts

Environment for every pytest invocation:

```text
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ... -q
```

| Gate | Fresh result | Wall | Output SHA256 |
|---|---:|---:|---|
| WC04–WC07 exact nodes | 4 passed | 1.410 s | `9dca0ae7311298b9c3c2e844f1155b908080c6f42c90fbbc60347537a0b201d5` |
| full waveform-channel | 9 passed | 1.349 s | `07b86e503e79ddcc7bdf76484a4cf1974fc4ba21003b0530307bc5421911dea4` |
| I02 contract regression | 6 passed | 0.827 s | `c463de96db76f8c370b043267e21df6bd8871df975e34b555e5b6a70ae59cc77` |

Unique tests=`15/15 GREEN`; failed/error/skip/xfail/warning=`0/0/0/0/0`.
The verdict is nevertheless FAIL because the independent mutations above are
owner-required gates not covered by those tests.

## 4. Independent mutation and numerical recomputation

Primary matrix: 18 cases; 13 produced the required outcome and five were
unexpected accepts.  Correctly rejected were bool/float/negative roots,
wrong/nonfinite/nonnumeric supplied waveform, unknown cell, bad schema,
direct receiver truth field, nested mapping/dataclass/container aliases.
`information_bits_per_cw` inside legal `CodeLayout` remained accepted as
required.  Unexpected accepts were oversize root, forged population, forged
code layout, forged receiver waveform layout, and nested slots truth alias.

Five additional focused structural mutations were all unexpectedly accepted:
receiver wrong shape, receiver nonfinite, truth wrong shape, truth nonfinite,
and float-typed registered cell.

Four independent `(seed,snr_db,linewidth_hz)` combinations recomputed
`tau=1/(2*pi*100)`, block-100 rho, `2*pi*linewidth*Ts`, AWGN per-real/complex
units, GG/Wiener sharing, independent AWGN, supplied-waveform equation,
read-only arrays, and defensive copying:

| seed | SNR | linewidth | result | received SHA256 |
|---:|---:|---:|---|---|
| 1001 | 10 | 10000 | PASS | `f94c7d2e1774a4889e859904179894b21e9a0b666d16f5e85f88d5411b72bfcd` |
| 1002 | 14 | 20000 | PASS | `6a3c61e73d30cf0729ec5e70ce550841364eede06224e3295c9228ced6cd30fc` |
| 1003 | 18 | 80000 | PASS | `39d83a5e4065712fa80e87105266ef10f7c952b239efa799fec7327cdc5b65bd` |
| 1004 | 22 | 10000 | PASS | `98701beee1704b5accf51607701fed61f8b330520b33596adecc2bbd3330714f` |

Global NumPy RNG state remained identical; named-stream access reversal and
extra `payload_x` consumption left GG/Wiener/AWGN-X/Y first draws unchanged.

## 5. Static/import audit

The fresh inline audit found:

```text
import_roots=[__future__, contract, dataclasses, math, numpy, scipy, typing, waveform]
project_legacy_runtime_imports=[]
forbidden_calls(open/mkdir/makedirs/BPS/equalizer/legacy)=[]
sys_path_changed_by_import=false
filesystem_changed_by_import=false
channel_equalizer_or_BPS_calls=[]
physical_arrays_readonly=true
receiver_truth_arrays_disjoint=true
```

Thus six-name `SeedSequence.spawn(6)` + local PCG64, fixed receipts/order,
source-bound GAR equations, single effective linewidth, theta[0] first
innovation, identity SOP, shared GG/Wiener, independent AWGN, and no I06
equalizer/BPS implementation all close independently.  They do not cure the
four findings in §1.

## 6. Final protection

At the final pre-write census, source/test/owner/step-130/step-133 hashes and
HEAD remained unchanged; staging remained zero. Existing cache census stayed
at `202 .pyc / 41 __pycache__ dirs / 4 .pytest_cache dirs`; controlled commands
used `-B` and `-p no:cacheprovider` and created no new cache.

Protected p05 SHA256s remained:

```text
7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

Only this step-135 log was created.  No benchmark/science/web/install was run;
no production/test repair, commit, push, stage, or governance edit occurred.

```text
TERMINAL=I06_VERIFICATION_FAIL
```
