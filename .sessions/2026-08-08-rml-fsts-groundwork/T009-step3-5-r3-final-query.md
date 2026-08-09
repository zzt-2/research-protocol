# Task Brief: Step 3.5 R3 最终源限定补查

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-r3-final-query.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与 R1/R2 receipts

## 0. TL;DR（执行方先读）

R2 的第 4 个新术语 query 因多源聚合超时，不能冒充 0 命中。本任务是第 3 轮也是最后一轮：只用 S2+OpenAlex 对该 query 做一次源限定补查，随后按 `gw-supplement` 三轮上限停止。
**产出**：raw JSON、worker-log、`search-archive/2026-08-09/rml-fsts-step3-5-r3-final-query-receipt.json`。

**最高纪律**：
1. 只运行一次：`bash tools/search "short-time spectrum coarse frequency offset FSO adaptive window correlation distance" --mode academic --sources s2 openalex`；120 秒硬上限，超时即写 placeholder。
2. 用 R1/R2/Step1-3 DOI/title guard 去重。只有可能实现 target condition→lag/`B_L`/window 或 cheap lookup 等价的才可列 new must/should。
3. abstract 只初筛；不下载、不全文终判、不进入 Step4a、不改 current views/papers index/p05/pyc。
4. 这是第 3 轮上限；无论结果是否 0，都要明确 `round_limit_reached=true`，不得开启 R4。

## 1. 产出格式（强制）

1. `## Execution`：命令、raw、hash、count、actual source provenance/error
2. `## Known/new screen`
3. `## Round-3 disposition`：new must/should、converged、round_limit_reached
4. `## Boundaries`

Receipt 必含 query/path/hash/status/count/sources、known hits、新候选、new counts、converged、round_limit_reached、errors。

## 2. 验收

- [ ] 单 query/120s 上限可核验。
- [ ] known/new 分离，R3 上限明确。
- [ ] 无越界修改。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-r3-final-query.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-r3-final-query-receipt.json`
