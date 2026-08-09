# Task Brief: Step 3.5 R2 新术语饱和检索

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-r2-saturation-search.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与 R1 receipt

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。R1 8-query matrix 新增 3 must + 3 should；这些条目已进入 bounded acquisition/read。为满足 `gw-supplement` 收敛判据，本任务用 R1 浮出的新术语做第二轮最小检索，判断是否再出现新的 must/should。
**产出**：4 个 raw JSON、worker-log、`search-archive/2026-08-09/rml-fsts-step3-5-r2-saturation-receipt.json`。

**最高纪律**：
1. 只执行下列 4 个冻结 query，不增加第 5 个；实际来源至少 2 类，记录 result-level source provenance。
2. 现有 R1 八候选、Step 1/3 已知论文、T004/T005/T006/T007 debt 全部按 DOI/title guard 去重，不得算新增。
3. 批量 abstract/web 信息由你在子 agent 消化；abstract 只初筛，不能做 exact-action 终判。
4. 新增 must/should 只给真正可能实现 condition→lag/`B_L`/window selection 或其 cheap lookup 等价的论文；通用 FOE/CPR/turbulence 不得灌入。
5. 不下载全文、不进入 Step4a、不改 current views/papers/index/p05/pyc。

## 1. 冻结 R2 queries

1. `single-tone training sequence FSO frequency offset estimation lag block length adaptive`
2. `short symbol block training sequence coherent FSO frequency offset adaptive length selection`
3. `low received optical power joint frame frequency synchronization lag window selection satellite optical`
4. `short-time spectrum coarse frequency offset FSO adaptive window correlation distance`

从目标 worktree 根目录实际运行 `bash tools/search "..." --mode academic`。自动 raw 文件之外复制为 `rml-fsts-r2-q1.json` 至 `q4.json`；保留 SHA256。

## 2. 产出格式（强制）

1. `## R2 query execution`：4/4、raw path/hash、result count、actual sources/errors
2. `## Known guard`：已知 DOI/title 数与去重命中
3. `## New candidate screening`：new must/new should/new exclude；候选≤10
4. `## Convergence`：最后一轮新增 must/should 是否 0；若非0只报告需要 R3，不自跑
5. `## Boundaries`

Receipt 必含 4 queries、paths/hashes/counts/sources、known-guard keys、screened totals、new candidate list、new_must/new_should counts、converged boolean、errors。

## 3. 已知陷阱

- R1 的 2025 single-tone、2024 short-block、2026 SSRN、2024 STS、2025 ICAIT、2021 JLT 及 Cheng/Dong 都是 known，不计新增。
- “adaptive window”可能来自 STFT/雷达/语音等跨域，必须同时满足 coherent optical/FSO FOE task。
- 找到场景 condition 仍不等于 condition 被用作 selector input。

## 4. 验收

- [ ] 4/4 query、≥2 actual sources、raw hashes 可复算。
- [ ] known/new 严格分离，new must/should 计数可复算。
- [ ] 无全文冒充、无越界修改。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-r2-saturation-search.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-r2-saturation-receipt.json`
