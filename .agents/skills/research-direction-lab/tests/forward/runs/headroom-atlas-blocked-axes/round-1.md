<!--
BLIND PROMPT (verbatim, round 1):
[same shape as C1; only case facts / decision point / artifacts differ]

CASE FACTS:
- Stage A ran 11 QPSK cells across SNR, channel dynamics, SOP rate, and short or long observation windows with 10 paired seeds per cell.
- No runnable cell reached the preregistered 0.005 minimum detectable effect; the maximum visible headroom was 0.00039.
- The runnable representative subdomain supported a LOCAL_NEGATIVE and did not trigger Stage B.
- The 16QAM, receiver-estimated CSI or pilot, and soft or coded output axes were infrastructure-blocked rather than measured-negative.
- Domain, candidate, and family conclusions remained unresolved or open, and no ML training was authorized.
- Independent verification found the history guards, gate binding, sampled recomputation, aggregation, and P03 anchor fidelity consistent.

DECISION POINT: Headroom Atlas Stage A closeout after independent verification.

ARTIFACTS:
- projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/stage-a-synthesis.md
  sha256: cb683444e04cb591ff4adf4cdb4da305f2f0d420d3b680b28aaa06c2b54acd31
- projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/stage-a-verifier-report.md
  sha256: d221053bd8bc0ec0d4bc9447629f0728d41fd99b4c8b01a9941bfdbc52d5b75e
-->

## 1. Recovered facts

- Stage A ran 11 QPSK cells across SNR {5,10,15,20,25} dB, channel dynamics (f_G ∈ {30,100,1000} Hz, SOP ∈ {4e-6,4e-5}), and short (512) / long (8192) windows, 10 paired seeds each (seeds 11–20).
- Pre-registered MDE = 0.005 per-symbol; max visible headroom across all cells = 0.00039 (~13× below MDE), on `qpsk-snr15-fg1000-long`.
- 10/11 cells `NO_VISIBLE_HEADROOM` (LOCAL_NEGATIVE); 1/11 `SUB_MDE_HEADROOM` (NON_DECISIVE); 0/11 above MDE → exit `NO_HEADROOM_IN_REPRESENTATIVE_DOMAIN_WITH_CERTIFICATE`.
- 6/11 cells sensitivity-limited (zero-error, rule-of-three UB > MDE); 4/11 measured-negative (waterfall region); P03 v1 anchor cell (`qpsk-snr20-nominal-short`) is all-zero PI-SER across nearest/blind/oracle.
- 16QAM, receiver-estimated CSI / explicit pilot, and soft/coded (LLR/GMI/FER) output axes are INFRASTRUCTURE_BLOCKED (frozen closure exposes only QPSK / CSI_NONE / hard-decision), not measured-negative.
- DOMAIN, CANDIDATE, FAMILY remain UNRESOLVED / OPEN because the historical counterexamples (`MODULATION_DYNAMICS_LENGTH_ORDERING_SIGNAL`, `HARD_DECISION_DOES_NOT_CLOSE_CODED_PATH`) live on the blocked axes.
- No Stage B triggered; no ML trained; no Queue/Registry/B004.
- Independent verifier verdict PASS on history guards, gate binding (assessment SHA `73c355f9…fb9f`, validator SHA `ccdbd47c…3066` across receipt/audit/disk), determinism (3 cells bit-identical), aggregation, and P03 v1 anchor fidelity; zero defects.

## 2. Recovered authorization, anchor, and current mode

- **Authorized now**: Stage A Scout diagnostic only. No ML training, no Stage B, no paper claim, no scope certificate.
- **Anchor / baseline**: P03 v1 source-equivalence contract → simulation commit `65db35bb` + `run_b001` SHA `26a0e95d…`; canonical baseline `common/_dual_pol_channel.py` (immutable); strongest legal non-ML comparator = standard-CMA Godard-with-z + nearest-QPSK, with same-information blind affine and oracle affine upper bound.
- **Current mode**: synthesizing / closing Stage A after independent verification; awaiting closeout + rotation.

## 3. Claim ceiling

**SLICE** — the runnable representative sub-domain (QPSK × SNR × dynamics × short/long × CSI_NONE × hard-decision) is LOCAL_NEGATIVE at-or-below MDE for the strongest legal non-ML baseline, with the wider claim ladder (CONTRACT/CANDIDATE/FAMILY/DOMAIN) blocked by unexercised axes, not closed.

## 4. Harvest items

- `LOCAL_NEGATIVE`: representative runnable sub-domain extends P03 v1 exact-slice LOCAL_NEGATIVE to a wider QPSK CSI_NONE hard-decision slice; evidence pointer: `projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/artifacts/headroom-atlas-v1/stage-a-synthesis.md`
- `BOUNDARY_RESULT`: standard-CMA + nearest-QPSK dominates the same-information blind affine on every cell (baseline-dominance boundary, not a bug); evidence pointer: `stage-a-synthesis.md`
- `INFRASTRUCTURE_GAP`: 16QAM generator, receiver-estimated CSI / pilot seam, and coded-output evaluator all require a new hash-bound closure; evidence pointer: `stage-a-synthesis.md`
- `REUSABLE_ASSET`: `atlas_gate.py` (receipt-bound, 19 passing tests incl. 8 adversarial) + `stage_a_cell_runner.py` (P03 v1 anchor reproduction, eval window {133,261,389}); evidence pointer: `stage-a-synthesis.md`
- `EVALUATION_INSIGHT`: 6/11 cells sensitivity-limited at 10 seeds; sequential cap of 40 seeds cannot unlock blocked axes; evidence pointer: `stage-a-synthesis.md`
- `WRITING_MATERIAL`: scoped negative + boundary framing for a limitations / future-work section; evidence pointer: `stage-a-synthesis.md`

## 5. Next automatic action

Append the Stage A harvest entries to the harvest ledger and update canonical-status to mark P03 UNRESOLVED-at-runnable-sub-domain (LOCAL_NEGATIVE, no Stage B), then rotate to the next ready candidate in the portfolio — recording the chosen candidate and why it is more informative than re-investing in P03's blocked axes.

## 6. Whether the user must be asked now

No — legal alternatives exist (in-scope option 1: close Stage A and return to the candidate pool). Options 2 (build a missing closure — materially larger infrastructure investment) and 3 (switch candidate family) are strategic escalations but are not yet forced, since rotation to ready candidates is available.

## 7. Files read or consulted

D:\code\study\research-protocol\.worktrees\research-direction-lab-system\.agents\skills\research-direction-lab\SKILL.md
D:\code\study\research-protocol\.worktrees\research-direction-lab-system\.agents\skills\research-direction-lab\references\evidence-and-claims.md
D:\code\study\research-protocol\.worktrees\research-direction-lab-system\.agents\skills\research-direction-lab\references\thesis-harvest.md
D:\code\study\research-protocol\.worktrees\research-direction-lab-system\.agents\skills\research-direction-lab\references\recovery-and-rotation.md
D:\code\study\research-protocol\.worktrees\research-direction-lab-system\projects\thesis-fso\direction-lab\scout\P03-U19-residual-headroom\artifacts\headroom-atlas-v1\stage-a-synthesis.md
D:\code\study\research-protocol\.worktrees\research-direction-lab-system\projects\thesis-fso\direction-lab\scout\P03-U19-residual-headroom\artifacts\headroom-atlas-v1\stage-a-verifier-report.md
