# T009 A4-v2 MVE Spec

- Stage: Groundwork Step 4a, formal owner D015.
- Hypothesis: causal receiver-visible DA/NDA ordering changes across at least two reliable sourced conditions.
- Identity gate: S011 AWGN/18 dB continuous DPLL BER 0.003–0.006 and reset degradation >=1.5x.
- Mechanism gate: both DA and NDA must win at least one registered validation condition on the common data mask.
- Validation/test: 10/10 disjoint seeds; arms paired by `(pool, seed, block)`.
- Abort: one bounded repair exhausted and mechanism gate still fails -> `BLOCKED_IDENTITY`; no primary.
- Forbidden: true SNR/channel/phase/turbulence/TX bits/future block in deployable actions.

