# Step 122 — D0 I04 independent codec verification

> 2026-08-10 | T076 / D011 / V005 / CP012 / epoch 12 | fresh verifier
> Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
> Verdict: `FAIL / P0-P1-P2 = 0-3-0`

## 1. Findings first

### P1-1 — Full D0 contract identity is not enforced

**Owner oracle.** The codec is an I04 D0 component under
`coded_decoder_feedback.d0.v3 / epoch 12 / CP012 / D011 / V005`; T076 requires
wrong contract identity to fail closed.

**Fresh reproduction.** `D0Codec(...)` accepted both of these mutated contracts:

```text
wrong_schema_identity=coded_decoder_feedback.d0.v4 -> ACCEPTED
wrong_checkpoint_identity=CP013 -> ACCEPTED
```

It did reject `decoder_iterations=19`, showing the defect is specifically that
`__init__` checks only three code-layout integers and never checks the frozen D0
identity/control tuple. A non-D0 or unauthorized control object with matching
1024/1536/20 fields can therefore instantiate the codec.

**Minimum repair direction.** Before storing the contract or constructing any
backend, require the concrete frozen D0 contract identity and CP012 control
fields (or a single fail-closed owner identity validator), then add independent
schema/checkpoint/decision/verification/epoch mutation tests.

### P1-2 — Non-binary decoder backend output is accepted

**Owner oracle.** Fresh LDPC output is hard information bits; T076 explicitly
requires bad backend shape **and binary output** to be rejected.

**Fresh reproduction.** A backend returning shape `[1,1024]` filled with integer
`2` was accepted by `decode_fresh`. The implementation checks only shape, then
blindly applies `astype(np.uint8)`. The parallel wrong-shape backend was correctly
rejected, so this is a narrow missing value-domain guard rather than a fixture
or dependency problem.

**Minimum repair direction.** Validate plain numeric/bool dtype, finiteness where
applicable, and every decoded value in `{0,1}` before any cast; add backends that
return `2`, `0.5`, and `NaN` as negative tests.

### P1-3 — Boolean noise power is accepted as physical variance

**Owner oracle.** D0 variance inputs are explicit finite non-negative numeric
powers; owner-aligned validators distinguish `bool` from numeric scalars. T076
requires invalid noise power to fail closed.

**Fresh reproduction.** `demap(..., complex_noise_power=True)` was accepted
because `per_real_noise_power` immediately calls `float(True)` and obtains
`0.5` per-real variance. Negative, zero, NaN, and infinity were all correctly
rejected.

**Minimum repair direction.** Reject Python/NumPy boolean scalars before float
conversion and add a boolean noise-power negative test.

### Non-defect disposition

The raw matrix's fifth FAIL was an overly strict verifier equality check for
repeated NLL rows. The two results differed by one binary64 ULP:

```text
base=0x1.5677499331331p+0
repeated=0x1.5677499331332p+0
absolute_difference=2.2204460492503131e-16
within_1e-15=true
```

This is ordinary reduction rounding and passes the frozen `abs=1e-15` oracle;
it is not a production defect and is not counted as P2.

## 2. Frozen-input and protection baseline

All resolvable frozen identities matched. T076's logical names resolve to
`step-120-d0-i04-codec-green-continuation.md` and
`explore/nda-awgn-tracking-sandbox/p08r_chain.py`; their hashes match exactly.

```text
codec.py=1f03b278054cb380c73b98e5211c0c5a37b41d2c47d5966f50bc5803d4e74dcb
test=38a2b8ec0c2af6132d0425201c4231d2fa5074297b200d0384de051a385792ef
step-118=cccdfb0d149fbd925918d68957dd487b6d30921d126146e8b219f04d92df4fc3
step-120=1b79aad9be86027d6fef91ad9e9a3931bce0bf53aa7e6cbd86f8f9a1c13ab1b4
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
p08r_chain=174daad20f4fadbb0710cdee5faf7d49f360b6a8a6609b9a1ea46ccb41288404
branch=codex/rdl-method-production-v2
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
cache_file_count=222
cache_manifest_sha256=4d5a97f0b2acfb8dce37eadee3a567eff90e986af52a303d56fb19adda1bf456
pyc_count=202
__pycache___dirs=41
.pytest_cache_dirs=4
```

Protected p05 SHA256 values were the frozen 4/4 values:

```text
p05_run.log=7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11
p05_run2.log=735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b
p05_run3.log=c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d
p05_run4.log=95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de
```

## 3. Import-side-effect probe

A fresh `python -B` process imported only `codec` after adding the D0 root to
its local `sys.path`:

```text
sionna_before=False
sionna_after=False
legacy_new=[]
path_unchanged=True
filesystem_unchanged=True
exit_code=0
duration_seconds=0.221
output_sha256=fc3df0cd2147f1c873cb225240827e18b194da7e5fee22744a2fb839234cbe1d
filesystem_manifest_before=a029f5de4a4b7375f677fa6a37a57c66b0e6fbaa6a2e3f20020b6a5646f6925d
filesystem_manifest_after=a029f5de4a4b7375f677fa6a37a57c66b0e6fbaa6a2e3f20020b6a5646f6925d
```

Therefore lazy Sionna loading, no legacy runtime import, no global path
mutation, and no import I/O all pass.

## 4. Fresh frozen tests

Every command used Windows Python with
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `-B`, and
`-p no:cacheprovider` from the evidence worktree.

| Scope | Fresh result | Process duration | Output SHA256 |
|---|---:|---:|---|
| RM07 exact | 1 passed | 0.779 s | `c650684da631a53569764f5af8f60c3e0d0a19a4321a45fbbac8d3f55d3a7118` |
| RM08 exact | 1 passed | 6.673 s | `56e30a68f6e28e9767dd2b9a430843704bff4b415466669161f16dd5cda5fb47` |
| RM09 exact | 1 passed | 0.890 s | `e595c9dd5a9edc1722d0f72303c939afef026f4ec243dac3267b63461a9fa194` |
| RM10 exact | 1 passed | 0.932 s | `e595c9dd5a9edc1722d0f72303c939afef026f4ec243dac3267b63461a9fa194` |
| full I04 file | 4 passed | 6.743 s | `3abde6416fecdc9824e383ce716fd3ec0a834fd048ef9e3c7a02d261cfb0343a` |
| I02 regression | 6 passed | 0.864 s | `cc3748ddd64c25121333402d0cdb7c9733f3f0f33f6353f70f65bbf92942eb00` |

All six commands exited 0; total fresh test observations were `14/14` GREEN,
with no skip, xfail, warning, or hidden failure. These happy-path results do not
override the independent negative failures above.

## 5. Owner-driven negative and live audit

The valid one-shot matrix ran in a fresh Windows Python process without writing
a repository or temporary test file:

```text
raw_rows=48
raw_PASS=43
raw_FAIL=5
adjudicated_defect_trigger_rows=4
adjudicated_non_defect_rows=1
exit_code=0
duration_seconds=5.949
output_sha256=8057c84eb788f3502ca8bb21d886dea05546dae72b1dc21b33559a7f12f22b04
```

Positive/negative oracles that passed include all 16 labels, four rotations,
invalid states, shape mismatch, ambiguous zero reference, wrong code-layout
identity, info/LLR shape, nonbinary info and encoder output, nonfinite LLR,
duplicate/mismatched CW IDs, empty candidate, ordinary invalid noise powers,
bad backend shapes, repeated `(None,None)` decoder state, exact receipt ledger,
positive-for-bit1 demap, preclip 30, per-real conversion once, and live
1024→1536→1024.

Live source-bound checks passed:

```text
base_graph=bg2
lifting_size=104
interleaver_length=1536
out_int[out_int_inv]==arange(1536)=true
metadata_matches_live_encoder=true
metadata_validation_precedes_receipt=true
decoder_source_clamp20=true
```

Thus the metadata is not a purely unverified string: the live encoder's
`_bg`, `_z`, `_num_bits_per_symbol`, and permutation inverse are checked before
`LiveCodecMetadata` is exposed.

## 6. Static audit

AST/source inspection found only import roots
`__future__, dataclasses, numpy, sionna, torch, typing`; Sionna/Torch imports are
nested in the lazy backend constructor. Results:

```text
legacy_imports=[]
import_io_calls=[]
dynamic_import_calls=[]
forbidden sys.path mutation=0
skip/fallback/import-error bypass=0
truth correction path=0 (receipt constant false only)
message/warm cache reuse=0 (both explicitly None per decode)
```

## 7. Protection and terminal

This verifier did not modify production, tests, step-118, step-120, owner,
contract, legacy source, results, or governance. The only intended write is
this step-122 log. No benchmark, scientific seed/estimand, web/search/download,
dependency install, commit, or push occurred.

```text
VERDICT=FAIL
P0_P1_P2=0/3/0
FRESH_TESTS=14/14 GREEN
NEGATIVE_MATRIX_RAW=43/48 PASS
NEGATIVE_DEFECT_TRIGGERS=4 rows / 3 P1 findings
TERMINAL=I04_VERIFICATION_FAIL
```
