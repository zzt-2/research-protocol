# Step 180 — D0 I14 B2 transition / variance / emission

> 2026-08-11 | author TDD | DONE

## Scope

- Evidence worktree: `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- Implemented only I14/B201–B205.
- Production: `projects/simulation/explore/coded-decoder-feedback/b2.py`
- Test: `projects/simulation/tests/test_d0_b2_math.py`
- No science, benchmark, I05 chain, `common/`, p05 log, staging, commit, or push operation was run.

## Code implemented

- `transition_matrix(p_s, distance=...)`: frozen four-state circulant kernel with the closed-form distance power.
- `log_transition_matrix(...)`: impossible transitions remain exact `-inf`; `p_s=0` is an exact log identity.
- `moment_variance(...)`: `mu=exp(-sigma_e2/2)`, `N0=max(0,Cpost-2(1-mu)Ecal)`, `noise_var_real=N0/2`, and `Vx=N0+|x|^2(1-mu^2)`.
- `emission_log_weight(...)`: positive-variance complex Gaussian metric and exact zero-variance Dirac branch (`match=0`, `nonmatch=-inf`).
- All public inputs are checked for finite/domain-valid values; no probability floor or unregistered variance offset is introduced.

## RED

Environment: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, Windows Python 3.11, `-B`, pytest cache disabled.

```text
python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_b2_math.py
5 failed in 0.69s
wall = 1.779s
```

All B201–B205 failed for the intended reason: `ModuleNotFoundError: No module named 'b2'`. Production code did not exist at RED.

## GREEN and fresh verification

```text
python.exe -B -m pytest -p no:cacheprovider -q projects/simulation/tests/test_d0_b2_math.py
5 passed in 0.80s
wall = 2.083s

python.exe -B -m pytest -p no:cacheprovider -W error -q projects/simulation/tests/test_d0_b2_math.py
5 passed in 0.65s
wall = 1.716s
```

Focused author elapsed from first test-file creation through strict fresh verification was approximately 2 minutes 10 seconds, below the 15-minute hard stop.

## Negative / boundary receipts

- B202: all 12 impossible off-diagonal transitions remain exact `-inf` at `p_s=0`; exponentiation is the exact identity.
- B203: the unsplit/double-count expression is explicitly unequal; negative `N0` is clamped to exactly zero.
- B204: passing P08 `sigma2=N0` is an exact half-magnitude negative control against the required `sigma2=N0/2` result.
- B205: a nonmatching zero-variance observation is exact `-inf`; the matching observation is zero; neither path produces NaN.

Test result: B201–B205 = 5/5 PASS, failures/errors/skips/xfails/warnings = 0/0/0/0/0.

## Hashes and review boundary

- `b2.py` SHA-256: `3e203bede0efdff9c0e22bc5b2b7843264c8c77165458063f84f31231a6ae9e4`
- `test_d0_b2_math.py` SHA-256: `98ddfcb146d88ab9f266f3ec275ae4cf81a2ab87a6baa35a323f5ab0f42a251a`
- `git diff --check` on the two code/test files: PASS.
- Author gate P0/P1: 0/0. This is not the independent Batch 4 acceptance.

## Next interface

I15 may consume the four frozen I14 surfaces above to add local posterior, state-exact/inner-max-log LLR, covariance identities, and one-way decode. I14 does not implement selector fitting, posterior inference, or decoding.
