# RED observation — cross-output portfolio fairness

The pre-revision Skill produced the project artifact
`projects/thesis-fso/direction-lab/campaigns/science-scout-2026-07-20/portfolio-refresh.v2-addendum.yaml` with these material behaviors:

- `shared_contract_for_all_C_candidates`: “All 4 candidates share ... the same Go comparator lattice (nearest-16QAM + MMA + blind affine; oracle affine = Kill only).”
- `C01.runnable_in_campaign: Y`
- `C02.runnable_in_campaign: Y`
- `C03.runnable_in_campaign: Y_with_compute`
- `C04.runnable_in_campaign: Y`
- `sequencing.next_batch_priority: C01`

This failed because detection, control, and correction claims need task-specific comparators; C03 lacks a state snapshot and executable action hook; shared inputs did not prove runnable readiness; and the four-candidate map remained narrowly clustered before selecting C01.
