# Step 137 — D0 I06 independent reverification

> 2026-08-10 | T091 | fresh non-author reverification | `I06_VERIFICATION_FAIL`

## VERDICT

`FAIL` — `P0=0, P1=3, P2=0`.

All fresh test selections are GREEN (`36 passed` in the aggregate), but nine owner-required adversarial cases were accepted. The accepted cases collapse into three independent P1 boundary defects below. Per T091, a non-zero P1 count is terminal FAIL; test GREEN does not override the adversarial evidence.

## Findings

### P1-1 — The evaluator-only correctness finalizer is forgeable through its module token

`contract.py:32` exposes `_TRUTH_FINALIZER_TOKEN` as a module attribute. `TruthView.__post_init__` accepts a supplied correctness array whenever the caller supplies that same object (`contract.py:482-488`), while `finalize_truth_view` uses it through ordinary `dataclasses.replace` (`contract.py:492-508`). Python callers can therefore read `contract._TRUTH_FINALIZER_TOKEN` and bypass the intended unique transition.

Fresh accepted attacks:

- `direct_correctness_with_private_token`: a pending truth was changed directly to caller-selected `(2,16)` correctness.
- `rewrite_final_with_private_token`: an already-finalized truth was rewritten with caller-selected correctness, bypassing the public repeated-finalize guard.

The no-token direct injection, repeated public finalization, wrong shape/type/non-binary decoded input, and source-truth immutability checks all failed closed. The defect is specifically authorization: the purported private capability is publicly retrievable and accepted by the dataclass constructor.

### P1-2 — Receiver `C_pre` is shape-checked but not bound to the received/known prefix

The channel computes the required per-polarization LS residual RSS/31 at `channel.py:376-384` and places it into both the Receiver field and receipt (`channel.py:385-405`). However, `ReceiverView.__post_init__` only checks `receiver_noise_estimate` shape, dtype, finiteness, and non-negativity (`contract.py:423-438`). It neither recomputes the value from `received_samples[:, :32]` and `known_prefix` nor cross-checks the receipt copy.

Fresh accepted attacks:

- `cpre_swap`: swap the two per-polarization estimates.
- `cpre_physical_injection`: replace them with finite physical-noise-derived values.
- `cpre_stale_after_rx_mutation`: mutate the received prefix while retaining stale estimates.
- `cpre_receipt_swap`: swap only the receipt values.
- `cpre_receipt_physical`: inject physical-noise-derived values only into the receipt.

The scalar-collapse attack was rejected, but that proves only the `(2,)` shape guard. T091 requires the unique per-polarization LS+RSS/31 recomputation and no physical-value/derived-alias injection; this boundary is therefore open.

### P1-3 — Generic `__slots__`/`__dict__` receipt objects remain mutable after construction

The recursive truth guard now traverses mappings, dataclasses, containers, slots, and instance dictionaries (`contract.py:269-319`), so aliases present at construction are rejected. But `_deep_freeze` handles arrays, mappings, built-in containers, and frozen dataclasses only (`contract.py:115-138`); an otherwise-safe generic slots/dict object falls through by identity. After Receiver construction, an external reference can mutate that object to add a nested truth alias, and the Receiver receipt observes the mutation.

Fresh accepted attacks:

- `slots_post_mutation`: mutate a retained slots object's safe field to `{"event_label": "leak"}`.
- `dict_post_mutation`: mutate a retained dict-backed object's safe field to `{"true_phase": 1}`.

This violates the frozen/defensive-copy Receiver boundary even though the initial recursive inspection succeeds.

## Frozen-input and protection evidence

The T091 frozen inputs matched before testing:

| Input | Fresh SHA-256 |
|---|---|
| `contract.py` | `35b20e922b9ea55c497b01fcf2d9b7bf92cf6e2f3386815dcec92911b21c7c8e` |
| `channel.py` | `c90d6c4d2ae8d4a860a1f1c5167a92c2ded383f4cc3518da55659cd36ceda9f9` |
| `test_d0_contract_views.py` | `ad07d742f49efc9e814da4c4d67f305f27c3e79a035d60b636de5b9215561f89` |
| `test_d0_waveform_channel.py` | `11cba3e14ed83eb015418e4d59ae4cc080da923b92b11d7f1c7d6a8bc07725ff` |
| step-135 | `3815f424b3f33f64ebf374ff61ddf0a7b05178cc5adc8461da6fd8eeec9f284f` |
| step-136 | `f898536ff99cd48867134c9495be0db9c5bab6a00b6e098af1fa63a7b092c27a` |
| `codec.py` | `77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b` |
| `waveform.py` | `7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f` |
| owner | `c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d` |
| D012 decisions | `47acc58ac08fd7cbb970590923926761e45faaed0c5c15fdebc6862314da9d0a` |

- `HEAD=715a65884b988ee737f21982f3bbf372860a1da8`; staging count remained `0`.
- `git diff --check` exited `0` (only line-ending conversion warnings on pre-existing user files).
- Protected P05 hashes remained:
  - `p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`
  - `p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`
  - `p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`
  - `p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`
- Cache inventory stayed at `202 *.pyc / 41 __pycache__ / 4 .pytest_cache`; the prescribed `-B`, `PYTHONDONTWRITEBYTECODE=1`, and `-p no:cacheprovider` controls produced no delta.
- Production and tests were read-only. This report is the sole write by this verifier.

## Fresh tests

Windows Python was run with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `-B -m pytest -p no:cacheprovider`.

| Selection | Result | Wall time | Captured-output SHA-256 |
|---|---:|---:|---|
| Four exact T090 nodes | `4 passed in 4.74s` | `6.209s` | `1a0199400d330e929c8ab70765fe6764f5fe261c13cacad6827a80509c4e28ad` |
| Full contract + waveform/channel files | `19 passed in 6.01s` | `7.507s` | `075e7c1a9225a2a55f631ddfa4dcf344414796a60beec12dabf05ed82e195062` |
| Codec file | `7 passed in 5.24s` | `6.690s` | `b2db8804998541f7d79a5c85702f72a9c7950f8d817c8fd7296ee9eee4fc18f6` |
| Schemas/statistics file | `10 passed in 7.77s` | `8.301s` | `e1463535e3ff01f7ca4d845d001aa678a394defdca5358e2e559091cc625ba70` |
| All current `test_d0_*.py` | `36 passed in 14.61s` | `16.094s` | `471732eca2de4a74e1dc87cb664f93727a4a824df6c545f0f7264e24798faa3f` |

The aggregate contained exactly four files and 36 unique tests. Every selection had zero fail/error/skip/xfail/warning.

## Fresh adversarial matrix

One fresh deterministic harness exercised 64 cases in `6.112s`; captured-output SHA-256 was `e083e2e2701515bbabab02ed821a175f2265f744440956e8a3497d8e0dff31f4`. Fifty-five cases behaved as required (including positive controls); nine owner-required mutations were unexpectedly accepted.

| Boundary | Fresh outcome |
|---|---|
| Step-135 replay; root/cell/contract/code/population/layout exactness; array shape/finiteness | Required invalid variants rejected |
| Recursive mapping/dataclass/container/slots/dict aliases present at construction | Rejected |
| PayloadTruth subclass and direct `replace`; equal-shape information-bit, codec-output, and one-waveform-symbol mutations | Rejected |
| Different valid payload with its corresponding canonical waveform | Accepted positive control |
| Same valid physical setup across valid payloads | Named-stream equality `True` |
| Correctness initially pending; no-token injection; repeated public finalize; wrong shape/type/non-binary; source truth unchanged | Required behavior observed |
| Correctness with retrieved private token; finalized-truth rewrite with retrieved token | **2 unexpected accepts — P1-1** |
| `C_pre` scalar collapse | Rejected |
| `C_pre` swap, physical injection, stale-after-received mutation, receipt swap, receipt physical injection | **5 unexpected accepts — P1-2** |
| Post-construction mutation of retained slots/dict receipt objects | **2 unexpected accepts — P1-3** |

## Independent numerical recomputation

Four fresh physical realizations independently recomputed the WC equations/sharing and per-polarization prefix LS residual RSS/31. All comparisons were exact/within the harness tolerance:

| seed | SNR dB | linewidth Hz | received SHA-256 | WC/sharing | `C_pre` |
|---:|---:|---:|---|---|---|
| 1001 | 10 | 10000 | `c26cd85600fa55dbc2d233df53adc9eb48a98190702e49b98d08764e9dfee27d` | `True` | `True` |
| 1002 | 14 | 20000 | `4d025b63ed1da8cab2b2db8424bebed7118083b82e18f12e372ffd01a5d5c262` | `True` | `True` |
| 1003 | 18 | 80000 | `9830a66b330f53126398efc519990ef272f36860df49bb1f8632d73d6b6f5aed` | `True` | `True` |
| 1004 | 22 | 10000 | `b3a37a606c8f0a72dc39f904fc5e62a7c71fc32db8520175f0c1ae658b986eef` | `True` | `True` |

This confirms that the numerical channel implementation itself did not regress; P1-2 is the post-construction contract/binding failure.

## Static, import, and cache review

- No legacy simulation-common import, import-time filesystem I/O, source `sys.path` mutation, or global RNG seeding/use was found in the four D0 production modules.
- A fresh-process dynamic import left the source-tree filesystem snapshot unchanged and left NumPy's legacy RNG state unchanged. Before/after RNG digest: `80279091ef716f4427af09a1e89cd85e4ee10db6bd189e27add001e39c1da4cb`.
- The only channel cache is `@lru_cache(maxsize=1)` on `_canonical_codec`, returning a source-bound `D0Codec` (`channel.py:312-314`). Payload canonicalization occurs before named streams are spawned (`channel.py:351-355`). The codec explicitly calls decode with `message_state=None, warm_state=None`, trips on non-None state, and the live decoder is configured with `return_state=False`; no per-message or decoder warm state is cached.
- Valid-payload substitution did not change the named RNG streams; rejected payload mutations occur before physical RNG consumption.

## Terminal

`terminal=I06_VERIFICATION_FAIL`

Required follow-up is limited to repairing the three P1 boundaries and obtaining a new independent reverification. This verifier made no repair.
