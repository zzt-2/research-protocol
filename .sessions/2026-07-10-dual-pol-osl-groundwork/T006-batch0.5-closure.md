# T006 — Batch 0.5 参数与事件指标闭合

> 来源: S043 | 产出位置: `.sessions/2026-07-10-dual-pol-osl-groundwork/S044-batch0.5-closure.md`
> 日期: 2026-07-16

## TL;DR

不跑新方法、不改 `params.py`、不改 `common/`。审计 Batch 1 将用的 fade/CMA 脚本是否满足参数真相源、shared realization 和事件指标要求，定义统一 recovery-delay；若发现脚本硬编码，只记录并标阻断，不顺手修。

## 必读

- `S043-batch0-partial-next-closure.md`
- `S041-candidate-family-map-batch-plan.md`
- `.agents/skills/sim-preflight/rules/param-source.md`
- `.agents/skills/sim-preflight/rules/doc-discipline.md`
- `.agents/skills/sim-preflight/rules/usage-log.md`
- `projects/simulation/explore/cma-fade-divergence/r7_freeze_quantification.py`
- `projects/simulation/explore/cma-fade-divergence/prompt015_unified_baseline.py`
- `projects/simulation/explore/cma-fade-divergence/prompt030_domain_swap_audit.py`

## 必须核查

1. 参数：SOP rate、GG alpha/beta、block size、fade threshold、CMA mu/taps、symbol count 是否从 `params.py` 或明确的实验配置读取；区分路径外 CRITICAL KF 债务。
2. 信道：是否使用 shared realization；不同方法是否在同一 seed/信道上比较。
3. 事件：是否能定义 fade start/end、first swap、recovery point；若现有脚本没有，给出不改代码的最小 schema 与所需 caller/callee。
4. 指标：fixed-label BER、PI-BER、swap rate、divergence、recovery-delay 的 numerator/denominator/排除位置/聚合方式。
5. 输出：Batch 1 允许进入的候选脚本清单、必须先修的脚本清单、参数/指标债务清单。

## 禁止

- 不改任何源代码、参数、旧结果；不跑 Batch 1。
- 不把 post-hoc 发送符号 detector 当部署方法。
- 不用 PI-BER 替代 fixed-label；不把“没有字段”推断成“没有事件”。

## 验收

- [ ] 写出 S044，结论 PASS/PARTIAL/BLOCKED
- [ ] 每个关键断言带文件+行号
- [ ] 明确 Batch 1 的最小闭合条件
