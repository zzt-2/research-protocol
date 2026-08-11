# step-136 — D0 I06 truth-boundary repair

> 2026-08-10 | T090 / D012 / CP012 | status: INCOMPLETE AT TIME BOUNDARY

## 1. Frozen preflight

```text
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
staging_count=0
contract.py=074a634b78c3af1c0eb9582d943fe8226a9d2a1d4b1d319e99bcaea73d156713
channel.py=728c86db0a4e27b9223c141fcb0f5078ebb288060295deba72c7dd4a269c2dde
test_contract_before=e508863b2d8b0a10353595a803e0cb7c98b1169d6819213f9b81514b60075e80
test_waveform_channel_before=ce5b80b262612943ada9e5677ff27713bef8dafd9cf17c6f8e537d464da5c3b0
waveform.py=7d30610c84d6787b08766462ec271912211b02928d774fc054f8411b735d490f
step-133=d0d8ca7b4b7c202289028ca52f2d43025b21ef75ad72a9766f68a89eb5a0bdc3
step-135=3815f424b3f33f64ebf374ff61ddf0a7b05178cc5adc8461da6fd8eeec9f284f
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
D012=47acc58ac08fd7cbb970590923926761e45faaed0c5c15fdebc6862314da9d0a
```

## 2. Strict TDD RED receipt

Production was unchanged when the four exact T090 nodes ran.

```text
test_contract_red=ad07d742f49efc9e814da4c4d67f305f27c3e79a035d60b636de5b9215561f89
test_waveform_channel_red=fabbc0b8940ac36090960947f9e08260eb7c6f70b3e719aafd4abef257173489
result=4 failed in 0.95s
exit=1
output_sha256=b285995b24d584902220dd99966bf1553a990abcb7edea0a2c3ecf30194233ae
```

The failures are causally relevant: three stop at absent `PayloadTruth`; the
structural node stops because the old scalar noise validator rejects the new
required `(2,)` typed value. No production edit preceded this receipt.

## 3. Implemented boundary

- Added frozen/slotted defensive `PayloadTruth` with exact uint8/binary
  `(2,16,1024)` and `(2,16,1536)` guards.
- `build_views` now requires payload truth and binds
  `information -> existing canonical D0Codec.encode -> coded -> gray16_map ->
  supplied waveform data positions`; neither `codec.py` nor `waveform.py` was
  modified.
- Receiver `C_pre` is a typed float64 `(2,)` value recomputed per polarization
  from received/known prefix using LS and RSS/31. Physical SNR/noise values are
  absent from Receiver fields and receipts.
- Added pending `None` correctness plus evaluator-only pure finalizer; direct
  injection and repeated finalization reject.
- Added exact contract/code/population/seed/layout, shape/finiteness,
  generic inherited/single-string `__slots__`/`__dict__`, int64 root and strict
  `PhysicalCell` guards.

## 4. Fresh GREEN evidence obtained before boundary

```text
four_exact_T090_nodes=4 passed in 4.74s
four_exact_output_sha256=1a0199400d330e929c8ab70765fe6764f5fe261c13cacad6827a80509c4e28ad
full_contract_plus_waveform_channel=19 passed in 4.83s
full_contract_plus_waveform_output_sha256=bb80674f66e8a3c211c2e146c49c0448a7f20bbdfba2f7d18bdecc9b9092ec22
codec_cross_regression=7 passed in 4.26s
codec_cross_output_sha256=50e9e1311bbbb5bcbd7738e24742dd76302766c7c8d281bfda30f3b257d8e375
```

The four exact nodes contain 16 receiver/truth structural mutations, 12
payload constructor mutations, four finalizer-input mutations, three
payload/code/waveform binding mutations, and ten root/cell/contract mutations.
The old contract and waveform/channel files also retain the nested
mapping/dataclass/container and physical-equation regressions.

## 5. Finding disposition and honest stop

| Finding | State at boundary | Evidence |
|---|---|---|
| P1-1 receiver physical-noise leak | implemented; exact node GREEN | per-pol LS RSS/31 equality and forbidden receipt-key assertions |
| P1-2 structural fail-closed | implemented; exact node + full regression GREEN | shape/nonfinite/layout/code/slots mutations |
| P1-3 payload/final lifecycle | implemented; exact node + codec regression GREEN | canonical encode/map/waveform binding and pending/finalizer checks |
| P2-1 root/cell scalar types | implemented; exact node GREEN | root upper bound and float/bool cell mutations |

The 15-minute boundary arrived before a separate final static/import audit,
post-write protection/hash census, `git diff --check`, and independent review.
Therefore this log does **not** claim I06 ready even though the executed tests
above are green. Final production/test/log SHA values were not captured before
the hard stop. No benchmark/science/web/install, commit, push, or stage was
performed.

```text
TERMINAL=INCOMPLETE_AT_POST_GREEN_AUDIT
```
