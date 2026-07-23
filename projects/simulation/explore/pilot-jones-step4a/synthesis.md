# Synthesis — Pilot-Jones GW Step 4a big package (GATE-KILL)

> 2026-07-23 | GW Step 4a (A0→A′→A/B→D) | D062 debt-waiver big package
> Provisional verdict: **KILL** (two independent gates, both structural)
> Formal MVE: **NOT RUN by design** (gate evidence is the result)

## 1. What scientific uncertainty this package closed

The open question (D055/D062): *does the dual-pol OSL GG + high-speed SOP +
≤10% pilot regime introduce a STRUCTURAL failure in block/frame pilot Jones
inversion that a receiver-visible method can exploit beyond the strongest
simple regularized alternative?* I.e., is there a method-worthy gap, or is
the apparent gap just a variance/bias knob absorbed by a single fixed EMA
parameter?

**Closed answer: there is no structural, method-worthy gap. The hypothesized
failure A does not exist in this channel, and the strongest simple alternative
(B1 = fixed EMA09) already reaches the oracle headroom.** The package therefore
produces a **KILL**, not a Conditional Go.

## 2. A0 §0 four-criteria (problem legality)

| # | criterion | verdict | note |
|---|---|---|---|
| 1 | concrete M-C-A | PASS (form) | M=block/frame pilot LS Jones inversion; C=dual-pol OSL GG+SOP+≤10% pilot; A=short-pilot LS jitter/ill-conditioning → fixed-label unstable. But the *A clause is empirically false here* (see §3). |
| 2 | reusable method output | PASS (form) | would yield stabilization design rules / curves |
| 3 | recent top-venue baseline | PASS | OE 2021, LCOMM 2026, JLT 2022/2023, TCOMM 2024 (4 BLOCKED) |
| 4 | quantifiable comparison | PASS | fixed/PI BER, cond, overhead, lag |

Form-level the problem is legal, so A0 §1-6 proceed. (Criterion 2/3 do NOT
rely on "nobody did OSL" alone — OE 2021 and LCOMM 2026 are direct mechanism
baselines.)

## 3. A0 §1 six fatal checks — TWO fatal items fire

| # | check | finding | fatal? |
|---|---|---|---|
| 1 | performance gap real? | **The gap between B0 (block-LS pinv) and oracle is fully absorbed by a single fixed EMA parameter (B1 EMA09 ≈ oracle).** On strong turb / historical rates: B0≈1.8e-5, B1≈6e-7, oracle≈6e-7 (B1 bit-equal to oracle on several seeds). On adversarial hard deep-turb (α=2.0,β=1.0,17dB): B1 mean 5.3e-3 vs oracle 4.5e-3 (relative headroom ~0.19, sub-order-of-magnitude, B1 equal-to-oracle on many seeds). | **FATAL** (no structural gap to close) |
| 2 | needs new structure, or fixed EMA/Tikhonov/cond-guard already covers? | **Fixed EMA09 already covers the entire useful gap.** B2a tikhonov is *worse* than B0 (adds bias to an already well-conditioned matrix); B2b condition-guard is *identical* to B0 (guard never fires). No regularization axis left to compete on. | **FATAL** |
| 3 | receiver-visible info sufficient to drive adaptation? | Yes (cond, innovation are computable) — but there is no *signal to act on*: cond ~ O(1) (p50=1.10, p95=1.26, max=1.68 strong; p95=1.38 hard probe) so the adaptation trigger is flat. | informative |
| 4 | does prior negative evidence explain the silence? | OE 2021 explicitly reports short-block noise / long-block mismatch tradeoff and warns of matrix degeneracy only "near certain degenerate states"; in our real-rotation channel those states are not reached. The silence of direct competitors on "OSL GG stabilization" is consistent with there being no OSL-specific structural failure to fix. | informative |
| 5 | why didn't direct competitors do it? | Scenario assumption difference (fiber DSCM/SCM, not OSL GG) + the structural reason found here: in a well-conditioned pilot-LS problem, a fixed smoother already reaches the ceiling, so there is nothing method-worthy to publish. | supportive of KILL |
| 6 | strongest simple method covers main metric? | **Yes — B1 fixed EMA09 covers the main metric up to the oracle.** | **FATAL (FR-01 prior-coverage)** |

## 4. Why the hypothesized failure A is structurally absent (the mechanism)

The channel's 2×2 polarization mixing is a **real rotation** `theta = sop_rate·arange(N)`,
matrix `[[cos, sin], [-sin, cos]]` (see `_dual_pol_channel.py`). A real
rotation is **unitary with condition number ≡ 1**. The pilot-LS Gram matrix
`P^H P` for 6 linearly-independent QPSK pilots is therefore structurally
well-conditioned (measured cond p50≈1.1, max≈1.7 even in deep turbulence).
The pilot-LS Jones estimate is **noisy (SNR-limited) but never ill-conditioned**.

Consequence: the only failure mode present is *variance* of the per-block
estimate, which a **single fixed temporal smoother (EMA09)** removes entirely —
it reaches the true-theta oracle. There is no conditioning axis, no deep-fade
singularity, and no dynamic-mismatch axis that EMA09 does not already handle.
This is not a tuning artifact: it is a structural property of the real-rotation
channel model (shared by the source closure; recorded as known_simplification).

A real complex Jones matrix with independent PMD/PDL (as in OE 2021's
frequency-dependent RSOP, which OE explicitly limits to first-order PMD) could
introduce genuine conditioning variation. But (a) that is a *different channel
model* not present here, and (b) the 4 direct competitors that might use such a
model are BLOCKED_NO_FULLTEXT (D056 debt) — so even the *potential* conditioning
failure cannot be confirmed against the literature. Claim ceiling is therefore
capped by both the channel-model simplification and the blocking debt.

## 5. A′ competition dimensions

| dimension | prior coverage (this channel) | method-worthy? |
|---|---|---|
| pilot overhead | fixed at 9.375% (6/64), ≤10% met | no (single value) |
| per-block estimation variance | **fully covered by B1 fixed EMA09 → oracle** | **no** |
| matrix conditioning / deep-fade stability | **structurally absent (cond~1)** | **no** |
| temporal tracking lag | covered by EMA09; theta slow (1 rad / 100k sym) | no |
| fixed-label assignment stability | assignment_xy dominant (≈100% in clean, dips only at high rate); not a P-vs-B2 axis | no |
| compute/state complexity | all arms O(1)/block | no |

Every dimension is either saturated by a simple baseline or structurally
absent. The remaining dimensions that *could* distinguish P (conditioning,
dynamic mismatch) are the ones the channel does not exercise.

## 6. Method candidates compared (A/B)

| candidate | legal inputs | state | update | mechanism claim | is it just EMA-reparam? | needs truth? | explains deep-fade vs mismatch tradeoff? | strongest reviewer objection |
|---|---|---|---|---|---|---|---|---|
| fixed EMA09 (B1, reference) | pilots | H_smooth | α=0.9 fixed | variance reduction | n/a (it IS the reference) | no | yes (covers whole gap) | "trivial fixed parameter" |
| condition-aware regularized LS (B2a tikhonov / B2b guard) | pilots, cond | H_smooth | λ or skip-on-cond | bias-variance via regularization | no | no | no — adds bias to well-conditioned H | "regularization harms a well-conditioned problem" |
| uncertainty-aware temporal tracker (P, proposed) | pilots, cond, innovation | H_smooth | per-block α(cond,innov) | trust/memory schedule | **α degenerates to ≈0.9 fixed because cond/innov are flat** | no | partially intended, but no signal to act on | "α is a constant in disguise on this channel" |
| (4th) oracle | true theta | — | exact inverse | upper bound only | n/a | **yes (tagged)** | yes | "uses truth, not deployable" |

Selected strongest proposed method: **P (uncertainty-aware temporal tracker)**.
Result: P **does not beat B1** (0/10 paired wins, 6/10 tie, 4/10 B1<P on hard
conditions). Since no candidate beats fixed EMA / regularized LS structurally,
the rule (T002 §5.2) mandates KILL without a performance MVE.

## 7. Oracle / headroom gate (FR-21)

- B1 (strongest simple alternative) → true-theta oracle headroom: **negligible**.
  Strong conditions: B1 == oracle bit-exact on most seeds. Hard adversarial
  conditions: B1 mean 5.3e-3 vs oracle 4.5e-3 (relative ~0.19, sub-order-of-
  magnitude; B1 equal-to-oracle on many seeds).
- Scoring oracle uses **true theta only** (no TX data, no future symbols).
- Headroom consistent in fixed-label and PI calibers (PI == fixed here because
  assignment_xy dominates; no permutation-calibration gap to exploit).
- Pre-registered kill (FR-21): B1 within 2× of oracle → KILL. **Fires.**

Per T002 rule 6 + FR-25: oracle is **only** an upper-bound/Kill tool; it is
NOT used as a Go opponent. The Go opponent is B2 (strongest simple
alternative), and P fails to beat even B1 (a member of B2's family).

## 8. Provisional verdict

**KILL** (allowed enum; positive ceiling not reached).

Triggered gates (independent, both structural):
1. **A0 §1 fatal + FR-01 prior-coverage fatal**: no structural performance gap;
   hypothesized failure A (ill-conditioning) is absent in the real-rotation
   channel; fixed EMA09 covers the main metric to the oracle.
2. **FR-21 headroom KILL**: B1 → oracle headroom negligible (<0.5dB-equivalent,
   sub-order-of-magnitude, bit-equal on many seeds).

This is a provisional verdict pending master-control acceptance and user
confirmation (D062 rule 6). It does NOT enter Step 5, Contract, or Execute.

## 9. Claim ceiling (honest cap)

Even if the channel model were upgraded to a complex Jones with PMD/PDL, the
claim ceiling is capped at **CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT**
*at best*, because the 4 D056 direct competitors remain BLOCKED_NO_FULLTEXT.
Since the gate fires on the *current* (simpler) channel already, the ceiling
question is moot for this package.

## 10. Durable harvest (T002 §8.4 — Kill path)

- **Reusable negative/boundary material**: the structural-ill-conditioning
  argument is a clean, citable negative result for "real-rotation OSL Jones
  estimation": a fixed EMA reaches the oracle, so no stabilization method is
  method-worthy *unless* the channel has genuine frequency-dependent PMD/PDL.
  This excludes the whole "pilot-LS stabilization" sub-family for unitary
  real-rotation channels.
- **Reusable baseline ladder + runner/metrics**: B0/B1/B2/P/O ladder,
  paired-realization runner, fixed/PI metrics, 10 directed tests — all
  reusable for the *next* pilot-Jones-style question (e.g. a complex-Jones
  channel, or a different M-C-A).
- **Reusable mechanism diagnostic**: cond-distribution + B1-vs-oracle headroom
  probe is a 5-minute pre-MVE filter for any "stabilize a matrix estimate"
  candidate (generalizes FR-21).
- **Excluded method family**: generic pilot→Jones→inverse + EMA/Tikhonov/
  condition-guard stabilization on unitary real-rotation channels. Do not
  re-propose without a channel-model change that introduces genuine conditioning
  variation.
- NO_DURABLE_HARVEST items: none — the above are all durable.
