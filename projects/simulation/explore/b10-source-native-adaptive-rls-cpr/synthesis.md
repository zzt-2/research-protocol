# T010 B10 source-native adaptive RLS CPR — scientific synthesis

> 2026-07-26 | final disposition: `BLOCKED_IDENTITY`
> independent review: live V026
> mission method delta: `NONE`

## Executed evidence

- C2 stopped at 28 complete validation cells / 840 canonical raw rows.
- Completed: all weak cells and moderate/14 dB seeds `131001–131003`.
- Failed next cell: moderate / 14 dB / seed `131004`; next canonical key
  `[1,0,3,0,0]`.
- `validation-raw.json` remains a strict prefix with 17 frozen source hashes,
  `heldout_consumed=false`, no aggregate, and no incomplete cell.
- No test seed, held-out cell, Phase D action, or post-Step4a action ran.

## Identity failure mechanism

The registered primary transfer uses a positive 1 MHz residual CFO at
2.5 GBd, whose true phase slope is `+0.00251327 rad/symbol`. In the failed
moderate-fade 14 dB realization, the 128-pilot effective observation was weak
enough that one low-amplitude pilot crossed the phase branch. `np.unwrap`
selected a false `-2π` continuation:

- true-phase least-squares slope with phase noise: `+0.00277341`;
- observed unwrapped least-squares slope before RLS: `-0.0138504`;
- RLS final slopes for λ `.98/.99/.999`:
  `-0.0062947 / -0.0109464 / -0.0164973`.

The same frozen RX bytes reproduced the failure twice. P1, P2, and P3 share
this 128-pilot initialization, so the failure precedes their DD update gates
and adaptive-forgetting differences. It is not a runner-order, RNG, RLS
recursion, or CFO-sign defect.

## Scientific disposition

T010 defines positive source-native slope and `F=2π/h1` as an identity
boundary. It provides no preregistered way to synthesize BER for an arm that
fails before corrected data exist. Skipping the cell would violate the
2250-key/30-row prefix contract; manufacturing a nonfinite/collapse BER row
would alter the global setting score.

Therefore the independent review accepts:

- `formal_science_disposition=BLOCKED_IDENTITY`;
- `mission_method_delta=NONE`;
- `P0=0, P1=0, P2=1`, where the P2 is the preserved
  `PRE_C1_IMMUTABLE_SNAPSHOT_ABSENT` debt.

The remaining validation matrix and all held-out work are permanently
unauthorized for this package. The raw artifact and its hashed execution
contracts are preserved unchanged as the evidence snapshot. This result is
an identity diagnostic, not a method, fair-comparison result, negative method
claim, `METHOD_SIGNAL`, or `PACKAGING_BOUNDARY`.
