# Step 140 — D0 I06 closed-world authority repair

> 2026-08-10 | T094 / D012 / D013 / CP012 | strict TDD receipt

## Frozen preflight

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
contract.py=1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240
channel.py=ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd
test_contract_before=9ff8edd59fc0f76ad268b37eb3c0182eb9089e6516d0bd8538c8fe31a9358206
test_waveform_before=02bab0fc430853ccdb1c565995763bbfc25d5133438535a010be0f41fb88c296
step-138=d94965345384387dfee88ebd0be23f750ca9f8e3ef88d70763aab744e20b3104
step-139=959fe9bffaa795633fcd4e0f9a72d08025f5573d67d631158e6128baa6a937b0
D013=63242551efd01a8b53989952a949cd742f2728ff4cb348f3955431b73f77effc
codec.py=77a5bbdb87715fc0cb932c8ea1e43afeaf4fd9c2c86f0cc675eb7a58770b950b
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
```

P05 hashes matched `7843b048... / 735e4650... / c76887c... /
95a1d184...`. No production edit preceded RED.

## Strict TDD RED

The four exact T094 nodes ran with the fixed interpreter/environment.

```text
result=4 failed in 5.60s
exit=1
output_sha256=0c6b84f2e6c6fb3beb8de4c4d86100a807621f5a63e5b3c231ea9821dd2afa1a
test_contract_red=3c5c010be89f5eb7b42a92baeacb04e3022747d617c3d736bf6848f6638190b4
test_waveform_red=f5335fa89a577e9752c5059de05ede5763a5dcf1b09684f315b135e1711efdbb
contract_at_red=1817a36756c4bf8e752f12293202b312e66c7f37979b7430d3c139e7a0e3a240
channel_at_red=ed73520af1e82965e1a1508622781973d2be461b97bf3a7908b6cb00e2dc7abd
```

The failures were causally exact: opaque `bytearray` entered the tree; the
evaluated wrapper still declared a stored correctness field; `noise_samples`
passed the semantic gate; and NumPy integer root was accepted.

## Finding disposition

| step-139 finding | Disposition | Final-byte evidence |
|---|---|---|
| P1-1 stored evaluated correctness | Removed the dataclass field/slot/cache; the read-only property creates a fresh `(2,16)` bool result from frozen decoded and pending information bits on every read | object/normal setattr, constructor, replace and returned-array mutation all fail to alter subsequent answers |
| P1-2 open-world receipt tree | Exact closed-world inputs only; exact built-in containers are detached into tuple/frozenset/tuple-backed frozen mappings; opaque protocols/subclasses reject; NumPy arrays copy and scalars normalize through the same exact allowlist | bytearray/memoryview/range/object/custom container/generator/iterator/non-string-key cases reject; plain tree controls detach |
| P1-3 incomplete noise aliases | Camel/acronym/case/separator/digit normalization plus semantic-family rejection covers physical/noise/AWGN/N0/SNR/variance/sample; only the two exact internal C_pre keys bypass and are overwritten | 13 spellings reject independently in both receipts and B2; safe metadata and derived C_pre controls pass |
| P1-4 NumPy root | Shared entry validator requires `type(root_seed) is int` before range use; both `build_views` and `spawn_named_streams` call it | NumPy integer/bool, bool, float, string and bounds mutations reject; exact Python int passes |

## Final-byte GREEN

All pytest commands used `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`,
Python 3.11 with `-B -m pytest -p no:cacheprovider`.

```text
four_exact=4 passed in 5.77s
four_exact_output_sha256=dbd553cb9d3a7a8b4aa9b450ff99dc760b5b08341bac73653389a50ebec97ca9
contract_plus_waveform=26 passed in 6.64s
full_i06_output_sha256=8468b852a844ed4ae87504f82164068c6b69407ca7ed8283b0ff0ca6a229efa4
codec=7 passed in 5.23s
codec_output_sha256=7b0c9c15ad9f0630da09e313f72be3672c5d1174b24ba18c72f36b3b2c61be70
schemas=10 passed in 8.28s
schemas_output_sha256=09011977517a2cdef38ba25ae0a3e52db663ebea40fa0b51f45ef67f176ca2ba
aggregate=43 passed in 14.10s (4 files)
aggregate_output_sha256=37b02c1bbc54f76756eee2bc1739eb0aea067b978a2d14953e367cdfe252b13a
```

Every pytest selection had zero fail/error/skip/xfail/warning. The fresh
mutation matrix contains at least 85 exercised mutations/controls, with
correctness `13`, closed-world tree `23`, noise semantics `30`, and root/cell
scalar `19`; each category exceeds the required eight.

## Step-139 replay and physical receipts

The warning-free standalone replay rejected all ten prior bad accepts:

```text
step139_bad_accepts=10/10 REJECT
payload_chain=True
replay_output_sha256=87029f65ea5cf579405a081972090ed4ca2a562dfe2bc2837d3043dc36b53b5f
```

Independent canonical codec encode → coded bits → Gray-16QAM → supplied data
positions matched. Four independent two-polarization LS + RSS/31 C_pre
recomputations all matched. Their received hashes were unchanged from
step-139: `c26cd856...`, `4d025b63...`, `9830a66b...`, `b3a37a60...`.

## Final protection and audit

```text
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
channel.py=af32b357ad8f270cce0e8343f2437b23399f9ee6770907ad21ff1b23d2ea18b6
test_contract=30fe6b67b6b26c9fc962476fef8287159b10e95bb046a67b0ee25cdf76b47779
test_waveform=f14cac811b0c68458eb62bbd37578d5dcf592c97cbd4c2ae92765d2e897e01e1
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
git_diff_check=0
cache=202 *.pyc / 41 __pycache__ / 4 .pytest_cache
```

Fresh import left the source snapshot and NumPy legacy RNG unchanged
(`rng_sha256=19a493ce...`). Static audit found no legacy common import, source
`sys.path` mutation, global RNG use, token, or evaluated stored-correctness
field. Codec, waveform, owner, D013, P05, HEAD, staging and cache remained
protected. Only the five authorized files were written. No benchmark,
science, MVE, web, install, commit, push or stage action occurred.

## Terminal

`terminal=I06_READY_FOR_INDEPENDENT_REVERIFICATION`
