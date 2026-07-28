# G1 B2 — fresh seed freeze receipt (token-clean, pre-run)

> T024 / 2026-07-28. Frozen BEFORE any fresh-seed run. Parent commit
> `1773ee9` ("audit T023 and prepare G1 formal confirmation").

## Selection rule (task §B2)

"用父提交做 exact-token seed scan，选择 20 个全新、连续、互斥 seeds；
T019–T023、任务文本、测试和任何已观察 token 全排除。"

## Previously-observed seed integers (must be disjoint)

- T019: 11-20 (probe), 31-50 (C11-legality)
- T020: dev 181-190, test 201-220
- T023: old 201-220 (reused), fresh 241-260
- legacy Ch4 KF / other sims: 1000-1004, 130001-130003, 41-50, 500, 300, 3000-3009, 500000+offset

## Token scan (parent commit `1773ee9`)

Strict seed-context scan (`seed=<n>`, `range(<lo>,`, `seeds <n>`, disjoint-assert)
for candidate ranges:

| range | strict-seed hits | verdict |
|---|---|---|
| 261-280 | **0** | CLEAN (chosen) |
| 281-300 | 17 (seed=300 in legacy gen) | dirty |
| 301-320 | 0 | clean (alternate) |
| 311-330 | 0 | clean (alternate) |

## Chosen: FRESH_SLICE = list(range(261, 281)) = 261..280

Rationale: 0 strict-seed hits; continuous forward step from T023's 241-260
(task §B2 prefers forward step); matches T020/T023 small-integer seed convention.

**Namespace note (disclosed, not a collision):** the integer 261 ALSO appears as an
*eval-window symbol index* in the P03 atlas (`eval window {133, 261, 389}`,
stage-a-synthesis). That is a different namespace (symbol-position index into the
CMA output array, not a seed). The seed integer 261 is disjoint from every
observed *seed*. If a stricter "any integer token" reading is later required by
master, the alternate clean range 301-320 is logged above.

## Asserts (frozen in run_g1_confirm.py)

- assert set(FRESH_SEEDS).isdisjoint(set(OLD_201_220))   # T020/T023 old
- assert set(FRESH_SEEDS).isdisjoint(set(FRESH_241_260)) # T023 fresh
- assert set(FRESH_SEEDS).isdisjoint(set(DEV_181_190))   # T020 dev
- assert FRESH_SEEDS == list(range(261, 281))
