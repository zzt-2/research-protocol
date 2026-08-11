# Step 200 — D0 I20 formal engineering-throughput terminal

> 2026-08-11 | formal I20 | genuine hard terminal

## Scope

- Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`.
- Executed the authorized formal `ENGINEERING_THROUGHPUT_V1` command exactly once against the official artifact directory.
- No code, tests, `common/`, `.sessions/`, science state, or `p05_run*.log` changes; no staging, commit, or push.

## Formal execution

- Process exit: `1` (hard-blocker terminal).
- Shell wall: `25.7 s`; benchmark-owned elapsed: `11.26600000000326 s`.
- Stdout status: `GREATER_THAN_7D_HARD_BLOCKER`.
- Stdout owner SHA-256: `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`.
- Stdout receipt SHA-256: `236e1c17bedbf59b90e1b085b176d70377277e2c19a866e12c1e1ff63d72fddd`.
- Stdout slice SHA-256: `2795428ba4a45acf952a7254d66c82201ea7688980d90ced91ddc190312065f4`.
- Stdout production/atomic counts: decoder 4, BPS 6, B2 10, HMM aggregate 1, atomic JSONL 1, atomic receipt 1.

## Official artifact verification

- `benchmark-receipt.jsonl`: one receipt; file SHA-256 exactly matches stdout receipt SHA-256.
- `engineering-slices.jsonl`: 25 records; file SHA-256 exactly matches stdout slice SHA-256.
- Slice records: decoder 4, BPS 6, B2 10, HMM 1, adjustment receipts 4.
- Receipt `incomplete_reasons=[]`; all required production slices and four allowed-adjustment receipts are present.
- Receipt owner-budget SHA-256 and workload-manifest SHA-256 are respectively:
  - `f159efae6c25dff94b1f3a9da4b88993277cfbd864c42a493ae3ef5bd72b067b`
  - `635eb9bc718f7ffa52bbaed64c29b009ad87f3af7e5fdd9dd3bbf9bfcfbb84c3`
- Selected measured adjustment: `batch_size`; selected HMM rate `0.07931844999742073 s/trajectory`.
- Cache receipt remains exact-content-only and reconciled: zero actual reads, `NOT_APPLICABLE`, four actual miss-compute units.

## Frozen-budget terminal

```text
consumed_engineering_days=4.0
projected_remaining_D0_days=6.8194509317398575
projected_D0_days=10.819450931739858
projected_mission_days=7.0
contingency_consumed_days=6.319450931739858
required_remaining_contingency_days=-5.819450931739858
```

The official run is complete but projects D0 at `10.819450931739858` days against the frozen seven-day mission budget. Therefore I20 terminates as `GREATER_THAN_7D_HARD_BLOCKER`, not PASS and not INCOMPLETE. S1–S4 science remains unauthorized and NOT_RUN.

## Verdict

`FORMAL_I20=GENUINE_GREATER_THAN_7D_HARD_TERMINAL`

