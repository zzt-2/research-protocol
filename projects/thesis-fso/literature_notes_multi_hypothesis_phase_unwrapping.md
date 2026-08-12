# Literature Notes — bounded multi-hypothesis phase unwrapping

> Owner: `.sessions/2026-08-12-multi-hypothesis-phase-unwrapping/`
> Groundwork status: Step 1 complete and verified; terminal=`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`; Step 2 not authorized.

## Progress

| Step | Status | Evidence |
|---|---|---|
| 1 search | COMPLETE / VERIFIED | `R001–R003`, V001 final PASS 0/0/0 |
| 2 acquire | NOT AUTHORIZED | D002; await master confirmation |
| 3 read | FORBIDDEN | Step 2 incomplete |
| 3.5 supplement | FORBIDDEN | Step 3 incomplete |
| 4a+ | FORBIDDEN | no Q# or feasibility authorization |

## Step 1 routes and must-read identities

| Route | Core identities | Current role |
|---|---|---|
| unwrap / suffix error | Wang TSP 2022 `10.1109/TSP.2021.3137966`; CSSC-CPE 2019 `10.1109/ACCESS.2019.2934224`; TSP 2024 chirp/WPN `10.1109/TSP.2024.3421374` | reference defect + cheap repair/avoidance competitors |
| mixture / sequence | Shayovitz–Raphaeli TCOM 2016 `10.1109/TCOMM.2015.2506553` | full-general + fixed order2/3 mandatory comparator |
| optical/FSO low complexity | JLT 2020 `10.1109/JLT.2020.3003561`; Sci Rep 2021 `10.1038/s41598-020-80822-z`; Photonics 2023 `10.3390/photonics10121312`; Nat Commun 2024 `10.1038/s41467-024-50439-1`; Electronics 2025 `10.3390/electronics14020265` | physical transfer, recent baseline, implementation/complexity competitors |

## Step 1 design-space notes

- D1: bounded `H=3` fixed-lag unwrap; fixed state/memory/worst-case latency; unwrapped sequence output to Wang estimator.
- D2: receiver-visible reliability-triggered expansion from `H=1` to `H≤3`; fixed-lag commit and explicit expected/worst-case cost.
- These are not methods. Exact equations, trigger, lag, merge/prune and fallback remain forbidden until Step 2/3 evidence closes the design space.
