# Task Brief: Step 3.5 关键词矩阵与双向引用链

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-search-citation-chain.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与项目工具链

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。本轮只做 mandatory Step 3.5。
**你的任务**：按冻结关键词矩阵运行定向检索，并对 Wang 2023 `10.1109/JPHOT.2023.3265847` 与 Enhanced 2024 `10.1364/OE.520452` 执行 backward+forward citation chain；批量筛查由你在子 agent 上下文完成，主线只收结构化 ≤10 篇候选。
**产出**：原始 search/citation JSON 自动存 `search-archive/2026-08-09/`，另写 worker-log 与一份机器可读 receipt `search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json`。

**最高纪律**：
1. 从目标 worktree 根目录实际运行 `tools/search`；不得因 `--help` 未列能力就跳过实测。单次执行预计超过 15 分钟时立即截断并记录，不无限等待。
2. 搜索至少产生两个实际 source family；记录每个 JSON 的真实 `source_api/source_apis`，不能把配置源数当真实来源数。
3. OpenAlex 引用图作严格主链；S2 只作补召回，S2-only 必须用目标论文 abstract/metadata 或实际 references 交叉验证，不能直接算 verified citation。
4. abstract/metadata 只支持召回与初筛，不能做全文动作终判；web 信息必须由 API/DOI abstract 交叉验证。
5. 必须区分 exact collision、generic multi-lag、offline parameter optimization、conditioned lookup equivalent、architecture adjacent；不进入 Step 4a，不设计方法，不触碰 p05 日志。

## 1. 背景（了解即可，不要对照评价）

Q1 exact action：receiver-visible condition（turbulence/branch/phase reliability；固定 modulation/TS/power bin）→ 在线或分区选择 lag、`B_L`、correlation distance，或 condition-aware multi-lag weighting。最强廉价替代：dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup。Wang 2023 仅是 exact recent M；Enhanced 2024 是 task-matched comparator。目标是竞争闭包，不是尽快 Go/Kill。

## 2. 任务详情

### 2.1 冻结关键词矩阵

方法变体 4 组：
1. `FSTS fixed lag BL carrier frequency offset estimation`
2. `multi-lag CFO estimation correlation distance weighting`
3. `adaptive variable lag window correlation distance frequency offset`
4. `condition-aware reliability-weighted multi-lag carrier recovery`

场景/条件 2 组：
A. `coherent FSO training-aided FOE frame synchronization turbulence spatial diversity`
B. `modulation training length received power branch phase reliability online selection lookup`

执行 8 个组合（4×2），优先 `bash tools/search "..." --mode academic`；如某主源失败，保留原始失败并用另一真实源补足，不增加第 9 个语义查询。结果自动存档后建立 query→path→actual sources 映射。

### 2.2 引用链

对两个 seed 各执行：
- forward：`bash tools/search --citations DOI --citations-source both`
- backward：加 `--citations-direction backward`

若自动文件名冲突，先保存/重命名到明确含 seed+direction 的合规路径；不得覆盖原始 JSON。筛查所有返回条目（如合计 ≥10，仍由你批量做），最终候选 ≤10 篇。

### 2.3 产出格式（强制）

worker-log：
1. `## 关键词矩阵执行表`：8/8 query、文件、命中数、actual sources、错误/降级
2. `## 搜索轮次`：R1 新增必读/建议读数；如不能证明收敛，明确需要的 R2，而不是自称闭包
3. `## Citation chain coverage`：两 seed × 两方向的返回/去重/筛查数、OpenAlex/S2 provenance
4. `## 候选表（≤10）`：title/DOI/year/source chain/abstract-supported relevance/classification/fulltext-needed
5. `## 未入选类别统计`
6. `## 边界`：不做 terminal，不用 abstract 宣称 exact action

receipt 必含：schema version、date、8 queries、raw paths+SHA256、actual source families、citation seeds/directions/raw paths+SHA256、screened counts、candidate DOI/title/class、round1 new must/should counts、errors。

## 3. 已知陷阱

- 搜到 `multi-lag` 不等于 condition-aware controller；只按 lag magnitude 加权属于 generic prior art。
- 按 modulation/TS/power 离线分别选固定参数可能等价于 cheap lookup，但仍需全文确认是否 dev-frozen/online。
- forward citation 的“相关论文”假阳性尤其可能来自 S2；必须保留 source provenance。

## 4. 验收

- [ ] 8/8 查询、≥2 actual sources、两 seed 双向链均有原始 receipt。
- [ ] 批量筛查规模与去重数可复算，最终 ≤10 候选。
- [ ] 每条只给 abstract-supported 初筛，不冒充全文终判。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-search-citation-chain.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json`
