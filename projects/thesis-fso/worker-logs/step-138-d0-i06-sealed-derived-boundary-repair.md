# Step 138 — D0 I06 sealed/derived boundary repair

> 2026-08-10 | T092 / D012 / CP012 | strict TDD receipt

## 1. Frozen preflight

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
contract.py=35b20e922b9ea55c497b01fcf2d9b7bf92cf6e2f3386815dcec92911b21c7c8e
channel.py=c90d6c4d2ae8d4a860a1f1c5167a92c2ded383f4cc3518da55659cd36ceda9f9
test_contract_before=ad07d742f49efc9e814da4c4d67f305f27c3e79a035d60b636de5b9215561f89
test_waveform_channel_before=11cba3e14ed83eb015418e4d59ae4cc080da923b92b11d7f1c7d6a8bc07725ff
step-136=f898536ff99cd48867134c9495be0db9c5bab6a00b6e098af1fa63a7b092c27a
step-137=29918182abc1a21bf76830bb318ee8d2b05d1829a01a347663ba4ea2ea9d9409
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
D012=bde22e6ca455fd5986d0de14777abe2f3b44adfb604bf610a527cc71b75f51fb
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
```

Protected P05 hashes matched step-137: `7843b048...`, `735e4650...`,
`c76887c...`, `95a1d184...`. No production file was modified before RED.

## 2. Strict TDD RED

Command (with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`):

```powershell
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider projects/simulation/tests/test_d0_contract_views.py::test_i06_generic_receipt_objects_fail_closed projects/simulation/tests/test_d0_waveform_channel.py::test_i06_receiver_noise_estimate_is_init_free_derived projects/simulation/tests/test_d0_waveform_channel.py::test_i06_truth_finalization_is_constructor_sealed
```

```text
result=3 failed in 5.69s
exit=1
output_sha256=df30561c2936eadad51f32c631cf3bd0c279641a4d8a0a26f12d9b4c8a54e37d
test_contract_red=44a8c9e8f73caebda93a5e9db4941c59adccf2183083586533b3d22e27af5d30
test_waveform_channel_red=04b5d38d9a4ee00a0668da632751149c8df7bb927045fd3b32700d9145999480
contract_at_red=35b20e922b9ea55c497b01fcf2d9b7bf92cf6e2f3386815dcec92911b21c7c8e
channel_at_red=c90d6c4d2ae8d4a860a1f1c5167a92c2ded383f4cc3518da55659cd36ceda9f9
```

Failures were causally exact: a safe generic slots object entered a Receiver
receipt by identity; `receiver_noise_estimate` remained `init=True`; and the
module still exposed `_TRUTH_FINALIZER_TOKEN`. Production edits begin only
after this receipt.

## 3. Finding disposition

| step-137 finding | Implemented boundary | Fresh evidence before final audit tightening |
|---|---|---|
| P1-1 forgeable module token | Removed token/`InitVar`; pending correctness is `init=False`; evaluator returns independent frozen/slotted `EvaluatedTruthView` whose correctness is computed in `__post_init__` | exact node GREEN; two historical token attacks REJECT |
| P1-2 caller-supplied/stale `C_pre` | Receiver field is `init=False`; LS + RSS/31 is recomputed from the object's frozen received/known prefix; channel no longer computes or passes it; receipt values are internally overwritten | exact node GREEN; five historical C_pre attacks REJECT; four physical realizations independently match |
| P1-3 retained generic objects | `_deep_freeze` rejects generic slots/dict/dataclass objects, detaches plain containers/arrays, and rejects cycles | exact node GREEN; two historical generic attacks REJECT |

Fresh verified selections (all used the fixed deterministic environment):

```text
three_exact=3 passed in 5.24s
three_exact_output_sha256=e7c544d84c097e5fa2f9a32224075b0c0573e334c3c4b42a98fe18879168b9b1
contract_plus_waveform_channel=22 passed in 6.09s
full_i06_output_sha256=1f432c4dc948caeef881577769df4614db3e88935d277106fceadcde92d84a75
codec=7 passed in 4.91s
codec_output_sha256=d9038b055e25d4ce2ac4b9cedce3790d03155d292e53bdbb5bb37d0c162f2295
schemas=10 passed in 7.28s
schemas_output_sha256=89d7d4cd3a1732434b9f135fdbf0fdbc3c2462ab7a1e17f462b08b571d027d2c
all_test_d0=39 passed in 13.51s (4 files)
aggregate_output_sha256=93400e4955ba1b3c6af3f70bc6a0d59393d09b7ce7d6aea205eeeca8f06280d7
step137_bad_accepts=9/9 REJECT
adversarial_output_sha256=1e9b7bf3a6a54bcf84ffb38865bedeec544ca4337b44c643dfca8f657dea7db2
fresh_mutations_verified=34
```

The four independent `C_pre` runs used `(seed, SNR dB, linewidth Hz)` =
`(1001,10,10000)`, `(1002,14,20000)`, `(1003,18,80000)`, and
`(1004,22,10000)`. Both polarizations matched the independent owner-formula
recomputation in every run; received-array hashes matched step-137 exactly.

## 4. Time-boundary stop and protection state

After the verified aggregate, a final static tightening changed only
`contract.py` and its waveform/channel test: allowlisted layout types became
exact-type only, NumPy scalars were normalized without retaining references,
and physical-noise receipt aliases were rejected. The 15-minute boundary was
then called before that last delta could receive a fresh test run. Therefore
the earlier GREEN evidence is real but is not evidence for the final bytes,
and this receipt cannot claim READY.

```text
final_contract.py=1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240
final_channel.py=ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd
final_test_contract=9ff8edd59fc0f76ad268b37eb3c0182eb9089e6516d0bd8538c8fe31a9358206
final_test_waveform_channel=02bab0fc430853ccdb1c565995763bbfc25d5133438535a010be0f41fb88c296
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
git_diff_check=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache (no delta)
```

Codec, waveform, owner, D012, P05, HEAD and staging remained protected. No
benchmark/science/MVE/web/install/commit/push/stage action occurred.

## Terminal

`terminal=INCOMPLETE`
