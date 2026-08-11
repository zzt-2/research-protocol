# Step 139 — D0 I06 final-bytes independent reverification

> 2026-08-10 | T093 / D012 / CP012 | non-author final-byte review | `I06_VERIFICATION_FAIL`

## VERDICT

`FAIL` — `P0=0, P1=4, P2=0`.

The final-byte test suite is GREEN (`39 passed`), and all nine step-137 bad accepts are closed. However, a fresh 73-case harness found ten new owner-required mutations accepted. They form four independent P1 boundaries. T093 requires `P0=P1=0`; therefore GREEN tests cannot produce PASS.

## Findings

### P1-1 — Evaluated correctness remains directly forgeable after construction

`EvaluatedTruthView` is frozen/slotted and declares correctness `init=False`, but stores the result in a writable object slot via `object.__setattr__` (`contract.py:533-554`). A caller can run:

```python
object.__setattr__(evaluated, "final_codeword_correctness", forged_bool_2x16)
```

The assignment succeeds and subsequent reads return the caller-selected array. There is no public validator or recomputing property on the evaluated wrapper to detect it. Direct constructor injection, `dataclasses.replace`, repeated finalization, bad decoded shapes/types/values, and tampered-pending re-finalization all reject; the remaining gap is the explicit T093 `object-setattr correctness` attack.

### P1-2 — The plain-tree freezer has an opaque-object fallthrough and retains mutable references

`_deep_freeze` rejects dataclass/slots/`__dict__` objects but returns every other unrecognized value unchanged at `contract.py:162`. Fresh attacks showed:

- `bytearray` and `memoryview` enter a Receiver receipt by identity; mutating the external backing bytes immediately changes the supposedly frozen receipt.
- `range` and a bare `object()` are accepted despite the required fail-closed exact allowlist.

Thus the slots/dict/dataclass repairs work, but the general “immutable plain tree / no mutable receipt reference” contract is still open.

### P1-3 — Physical-noise aliases can bypass the receiver truth taxonomy

The alias rule only treats token `noise` as forbidden when paired with one of `physical/true/actual/oracle/power/variance` (`contract.py:256-259`), and it does not recognize `awgn` or `n0`. Receiver receipts accepted arrays under all four fresh aliases:

- `noise_samples`
- `awgn_samples`
- `physical_awgn_samples`
- `n0`

A caller can therefore place exact physical-noise samples or noise power in the deployable Receiver receipt. The explicitly covered aliases (`physical_noise`, `physical_noise_power`, `complex_noise_power`, `noise_variance`, `true_snr`, `snr_db`, `actual_noise_samples`) do reject, but the owner requires value-level no-leak, not a finite spelling list.

### P1-4 — Root seed is not exact-type fail-closed

`spawn_named_streams` explicitly accepts `(int, np.integer)` and coerces to Python `int` (`channel.py:88-96`). The T093 exact-type mutation `root_seed=np.int64(999901)` was accepted and ran the full build. Bool, float, out-of-int64, seed-range `np.int64`, contract subclass, cell subclass, CodeLayout subclass, and WaveformLayout subclass all rejected. The remaining accepted NumPy root type violates the requested seed exact-type boundary.

## Frozen final-byte inputs and protection

All T093 inputs matched before execution:

| Input | SHA-256 |
|---|---|
| `contract.py` | `1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240` |
| `channel.py` | `ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd` |
| `test_d0_contract_views.py` | `9ff8edd59fc0f76ad268b37eb3c0182eb9089e6516d0bd8538c8fe31a9358206` |
| `test_d0_waveform_channel.py` | `02bab0fc430853ccdb1c565995763bbfc25d5133438535a010be0f41fb88c296` |
| step-137 | `29918182abc1a21bf76830bb318ee8d2b05d1829a01a347663ba4ea2ea9d9409` |
| step-138 | `d94965345384387dfee88ebd0be23f750ca9f8e3ef88d70763aab744e20b3104` |
| `codec.py` | `77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b` |
| `waveform.py` | `7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f` |
| owner YAML | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` |
| D012 decisions | `bde22e6ca455fd5986d0de14777abe2f3b44adfb604bf610a527cc71b75f51fb` |

`HEAD=715a65884b988ee737f21982f3bbf372860a1da8`; staging remained empty. Protected P05 hashes were unchanged:

- `p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
- `p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
- `p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
- `p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`

Cache inventory stayed `202 *.pyc / 41 __pycache__ / 4 .pytest_cache`. Production, tests, governance, and prior logs were read-only; this step-139 report is the verifier's sole write.

## Fresh final-byte tests

All commands used the fixed T093 interpreter and environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider`.

| Selection | Fresh result | Wall | Captured-output SHA-256 |
|---|---:|---:|---|
| Three T092 exact nodes | `3 passed in 5.71s` | `7.362s` | `4fc0df63195740f26d1a1d8ed635508e880c8fe0dee8f6735b62f1c446803891` |
| Full contract + waveform/channel | `22 passed in 6.46s` | `8.133s` | `0382c4b8df71a74361a3004a432c1e38e364a0ad75b52f75c4f6ed6f158bf2d2` |
| Codec file | `7 passed in 5.43s` | `7.065s` | `372807f80ea6ca80809a3622725f1c9616d53e710d396695213aa5d1aa5b2413` |
| Schemas/statistics file | `10 passed in 8.69s` | `9.396s` | `1517fde71871a3a6e5e89d841d43d3bdc51e4234f9ffaf801726bfaf5c987dbd` |
| All current `test_d0_*.py` | `39 passed in 14.74s` | `16.117s` | `b1049d71c4cd87fe8d1dca4aa8e4c7500527e59c69fcd1dffcdaeee08c4ceb75` |

The aggregate collected exactly four files and 39 unique nodes. All five selections had zero fail/error/skip/xfail/warning.

## Fresh independent mutation matrix

A standalone inline Python harness (no existing test helper) completed in `6.3s`, exit `0`, with `73` cases: `63` behaved as required and `10` were unexpected accepts.

| Boundary | Result |
|---|---|
| Replayed step-137 nine bad accepts | `9/9 CLOSED` |
| Token lookup/forgery; constructor/replace correctness; repeat finalization; decoded shape/type/binary; tampered pending through public finalizer | Required rejects/controls observed |
| Evaluated-wrapper `object.__setattr__` correctness | **1 unexpected accept — P1-1** |
| C_pre init-free direct/swap/scalar/physical injection; receipt overwrite; received/known replace recomputation | All required behavior observed |
| Single-string/inherited slots, dict object, generic dataclass, nested object, mapping/list cycles | All rejected |
| Plain mapping/list/set/array detachment; NumPy scalar normalization; exact Code/Waveform allowlist subclasses | All required behavior observed |
| `bytearray`, `memoryview`, `range`, bare `object()` | **4 unexpected accepts — P1-2** |
| Seven explicit physical truth aliases | Rejected |
| `noise_samples`, `awgn_samples`, `physical_awgn_samples`, `n0` | **4 unexpected accepts — P1-3** |
| Payload subclass; information/coded/Gray/waveform equal-shape mutations; malformed payloads | Rejected |
| Different canonical valid payload/waveform; same-seed truth-free physical RNG | Positive controls passed |
| Contract/cell/code/layout subclasses, bool/float/out-of-range root, NumPy seed-range endpoint | Rejected |
| NumPy `int64` root seed | **1 unexpected accept — P1-4** |

## Independent physical and C_pre recomputation

For each run, both polarizations matched the independent LS + RSS/31 calculation; the same received/known pair produced one result; the value was not equal to the physical complex-noise truth. The supplied-waveform equation, shared GG/Wiener processes, independent AWGN, and Receiver physical bytes also matched.

| seed | SNR | linewidth | received SHA-256 | equation/sharing/C_pre/unique/not-truth |
|---:|---:|---:|---|---|
| 1001 | 10 | 10000 | `c26cd85600fa55dbc2d233df53adc9eb48a98190702e49b98d08764e9dfee27d` | all `True` |
| 1002 | 14 | 20000 | `4d025b63ed1da8cab2b2db8424bebed7118083b82e18f12e372ffd01a5d5c262` | all `True` |
| 1003 | 18 | 80000 | `9830a66b330f53126398efc519990ef272f36860df49bb1f8632d73d6b6f5aed` | all `True` |
| 1004 | 22 | 10000 | `b3a37a606c8f0a72dc39f904fc5e62a7c71fc32db8520175f0c1ae658b986eef` | all `True` |

## Static/import audit

- No legacy simulation-common import, source `sys.path` mutation, global RNG seed/use, or import-time filesystem I/O was found. The sole file read remains inside the explicitly called `load_contract` function.
- A fresh-process import left the source-tree filesystem snapshot unchanged and NumPy legacy RNG unchanged; before/after digest was `207c90e033383bbc61ece0aa2c54d73089307f6ee928ecf9bfc907a773a7cfb9`.
- `git diff --check` exited `0` (only pre-existing CRLF conversion warnings).
- The truth/value-leak and mutable-receipt portions of the static audit fail for P1-2/P1-3 above. The finalizer tamper and exact root-type portions fail for P1-1/P1-4.

## Terminal

`terminal=I06_VERIFICATION_FAIL`

No repair was attempted. A further repair must close all four P1 boundaries and receive another fresh non-author verification before Batch 2 can open.
