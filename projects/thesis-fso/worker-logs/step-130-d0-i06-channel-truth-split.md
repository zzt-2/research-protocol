# step-130 — D0 I06 named RNG, physical channel and truth split

> 2026-08-10 | T084 / D011 / V005 / CP012 | action: `D0_TESTBED_IMPLEMENTATION`
> Status: **IN PROGRESS / VALID RED CAPTURED / PRODUCTION ABSENT**

## 1. Scope and frozen preflight

Only WC04–WC07, `channel.py`, the existing waveform-channel test file, and this
receipt are in scope. I03 is independently verified by step-128. The current
topic authorizes implementation/unit tests only; no D0 scientific execution,
adapter, runner, artifact/result/cache, benchmark, web, install, commit, or push
is authorized here.

```text
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
test_before=f11fe29b3a83583514a2f10811645e78f9ff6af114f2910ba0bd00beef852157
step-125=092f535d64781f1ef9a0353ee70b85c55bb176cecd2b2327d2c0b79731b4974e
step-128=4b0b1257c7964724821fb94f6141e39cd3ef542133e567e2f73e10836a56959f
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
plan=52322d1374a5385f93d6df833aaca7dd2e7431912d2e751449f1c3de1cc9fd7b
step-106=67f699b06572d013eebd33a0e2ff4ca820404a0e3361b8338783f3501eb3b4a2
step-105=e104542c00127f1905d348f83a5108d0c3971d4f1ea9b9ea6b4639c20504ee6d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
channel.py=ABSENT
step-130=ABSENT
```

## 2. Test-first RED receipt

Only the four exact T084 tests were appended; the original five waveform tests
remain in the same file. The append changes the frozen test receipt and is the
new file-level RED authority.

```text
test_after_append_sha256=ba5ebbacdeab3904554772fec70f3a4d73f1809f0a0d7f35ea8074c4201bd13a
source_state_during_all_red_runs=ABSENT
cwd=D:\code\study\research-protocol\.worktrees\rdl-method-production-v2
python=C:\Users\zzt\scoop\apps\python311\current\python.exe
PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=0
pytest_flags=-B -m pytest -p no:cacheprovider -q
```

| exact node | exit | wall | output SHA256 | expected failure |
|---|---:|---:|---|---|
| `test_named_seedsequence_spawn_receipt` | 1 | 0.724s | `e4c0e1b46b32e38e66d25aacd6ee234733363cb89001015182b9a02557972174` | `ModuleNotFoundError: channel` |
| `test_stream_consumption_isolation` | 1 | 0.735s | `477cf0b9dc95c09c833ea23288016fec4575785c63fe550715e38efc0b3d89fc` | `ModuleNotFoundError: channel` |
| `test_shared_gg_wiener_independent_awgn` | 1 | 0.727s | `ddec946b5d91152f8851a735dbe6f924439ae5c9e22779a6b1d4248139ec05a2` | `ModuleNotFoundError: channel` |
| `test_gamma_gamma_wiener_formulas` | 1 | 0.758s | `b1a18169a46c2f01f68272732ae1bc2822f825bc0cffec95bc62be5fe695bbd0` | `ModuleNotFoundError: channel` |

All four failures occurred inside the selected test at `_channel_module()`;
there was no collection, fixture, dependency, or syntax error. `channel.py`
remained absent after the last RED invocation.

```text
RED=VALID 0/4 GREEN
RECEIPT_WRITTEN_BEFORE_PRODUCTION=YES
NEXT=minimum channel.py implementation, then exact-node GREEN
```

## 3. Bounded GREEN attempt and stop

The persisted RED receipt SHA256 was
`c711e7322eb50837e6cbd70f3c5ba88e62beaa46e56f66becc3558e9dbfd8198`;
`channel.py` was confirmed absent immediately before that receipt check. Only
then was the minimum production file created.

Production currently contains the six named local PCG64 streams and receipts,
source-bound GAR Gamma-Gamma helper, shared effective-linewidth Wiener phase,
independent per-pol AWGN, supplied-waveform identity-SOP realization, frozen
physical values, and the sole `build_views` split factory. Current source SHA256:

```text
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test=ba5ebbacdeab3904554772fec70f3a4d73f1809f0a0d7f35ea8074c4201bd13a
```

Fresh exact-node results before the time/test-ID stop:

| node | result | wall | output SHA256 |
|---|---:|---:|---|
| WC04 `test_named_seedsequence_spawn_receipt` | 1 passed | 3.443s | `49f3e29a212c09e239d566d800ad1a453c57eadb7df75ad1ac7db810d0140caa` |
| WC05 `test_stream_consumption_isolation` | 1 passed | 0.901s | `0dff5a7b4f7b627aa5d5ba9609862b0c83a9c34efeac8569b0ff66edb0c0e2d9` |
| WC06 `test_shared_gg_wiener_independent_awgn` | 1 failed | 1.185s | `4dbbfd7ace920f60c3561682fb20d1ccbb0de4bee47fa2b2c1e7ae05b0e13ceb` |

WC06 reaches and passes the physical sharing/determinism/equation checks plus
`build_views`; it fails only in the newly authored no-leakage assertion. That
assertion searches the complete `repr(receiver)` for `information_bits`, so it
incorrectly matches the owner-required, receiver-allowed frozen
`CodeLayout.information_bits_per_cw`. This is a test-oracle false positive, not
observed TruthView leakage. Hiding the allowed code-layout field in production
would be a test-specific workaround and was not attempted.

Per T084's “do not change tests after RED”, 15-minute cap, and test-ID boundary,
execution stopped at WC06. The test oracle was not edited after production;
WC07, full 9-test waveform-channel gate, I02 regression, independent negative
matrix, and final cache/p05 protection were not run. A continuation must first
adjudicate a narrowly corrected leakage oracle (inspect ReceiverView's direct
field/receipt graph while allowing CodeLayout), capture the superseding RED
required by any test edit, and only then resume GREEN.

```text
WC04_GREEN=1/1
WC05_GREEN=1/1
WC06_GREEN=0/1 (TEST_ORACLE_FALSE_POSITIVE)
WC07_GREEN=NOT_RUN
FULL_GATE=NOT_RUN
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
TERMINAL=INCOMPLETE_AT_WC06
```

No benchmark/science/web/search/download/install/commit/push/stage occurred;
waveform/contract/owner/legacy files were not modified.
