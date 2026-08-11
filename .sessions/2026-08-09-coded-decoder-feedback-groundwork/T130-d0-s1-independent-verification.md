# Task Brief: D0 S1 natural-occurrence 独立终验

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-202-d0-s1-independent-verification.md`
> 日期: 2026-08-11
> 唯一文档: 本 brief + T129 final files + 冻结 owner YAML/现有生产源码

---

## 0. TL;DR（执行方先读）

T129 新增最小 S1 runner 并产出 first-stage raw 480 rows，summary 声称 `262/480=0.5458333333333333`、event seeds 17、cells 12、PASS。你是独立 verifier，只验证这个 S1 门，不改 production、不扩 S2。

**最高纪律**：15 分钟内完成；不复跑 480 条物理仿真；从 raw+冻结合同独立复算；检查 runner/event math、checkpoint/receipt/hash、owner drift、truth boundary、TDD 证据与完整 runtime 口径。发现 P0/P1 就 FAIL，不能修代码。

## 1. 验证范围

- 冻结 owner：`projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`
- runner：`projects/simulation/explore/coded-decoder-feedback/science.py`
- tests：`projects/simulation/tests/test_d0_science_s1.py`
- artifacts：`projects/simulation/explore/coded-decoder-feedback/artifacts/science/s1-natural-occurrence/`
- author log：`projects/thesis-fso/worker-logs/step-201-d0-s1-natural-occurrence.md`

## 2. 必验项

1. 独立 parse raw JSONL，要求正好 480 unique `(seed,cell,pol)`，seed 8100–8119、12 owner cells、X/Y 完整。
2. 用 `schemas.row_from_mapping` + `statistics.reduce_s1` fresh 复算 event_count/rate，并独立聚合 distinct event seeds/cells；与 summary/receipt byte-for-byte 数值一致。
3. raw/summary SHA 与 receipt 一致；contract SHA 与 owner 当前 bytes 一致；source SHA 与 science.py 当前 bytes 一致；HEAD 解释正确。
4. 审查 persistent transition：四态 residual 最近 π/2、32-symbol each side、28/32 same-state、different state、≤32 merge；true phase 只在 evaluator path，deployable/channel receiver 不因 runner 获得 truth。
5. checkpoint/resume 对 240 dual-pol frames→480 rows 一次且仅一次；`resume_count` 和 `wall_time` 字段不得把“finalization”误报为完整执行成本。若语义不准确，按 P1 裁决，不能静默接受。
6. 核对 RED/GREEN：4 failed→4 passed，CLI import RED→5 passed，replace retry RED→6 passed；不要求重跑宽回归，但运行 focused test 一次 fresh。
7. 核对 owner YAML、`common/`、S2–S4/C1、p05 未被 T129 修改；无 stage/commit/push。
8. gate 原样：events≥12、event seeds≥4、event cells≥2。仅在全部证据有效时裁 PASS。

## 3. 输出

写 `step-202-d0-s1-independent-verification.md`：

- `VERDICT=PASS|FAIL|INCOMPLETE`
- `P0/P1/P2`
- fresh commands/results
- independent numbers
- artifact/hash/coverage/truth-boundary checks
- runtime-accounting finding
- `formal_science_disposition`
- `mission_method_delta=NONE`
- `thesis_method_disposition=NONE`
- 若 FAIL，只列最小 blocker，不实施修复

返回主控仅一行 verdict + 数字 + findings。
