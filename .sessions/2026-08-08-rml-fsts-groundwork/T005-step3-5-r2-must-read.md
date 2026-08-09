# Task Brief: Step 3.5 R2 三篇新增必读 acquisition/fulltext 裁决

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-r2-must-read.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与 T003 的 R1 raw/receipt

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。R1 新增 3 篇必读，因此 Step 3.5 尚未收敛。
**你的任务**：合法获取并全文裁决以下三篇；全文不可得时，用 DOI/官方 API/作者存档做 identity+abstract 交叉验证，但必须把动作判定标为阻塞，不能冒充全文。

1. `10.1364/OE.561252` — robust multifunctional single-tone TS（2025）
2. `10.1109/ACP/IPOC63121.2024.10809664` — optimized short-symbol-block FOE（2024）
3. `10.2139/SSRN.6293357` — low-received-power satellite-ground joint FS/FOE（2026）

**产出**：worker-log + `search-archive/2026-08-09/rml-fsts-step3-5-r2-must-read-receipt.json`；qualified 全文需有 canonical content/read-note。

**最高纪律**：
1. 全文精读必须由你在子 agent 上下文完成；abstract/metadata 不得冒充全文。
2. 实际尝试 `tools/download`/等价 Python 通道；可用 web/search 仅定位官方 publisher、Crossref/OpenAlex/S2 或作者/机构合法副本，任何贡献断言须 DOI/API abstract 交叉验证。
3. PDF 转 markdown 必须用 `tools/convert`，不得自写转换器。
4. exact action 固定为 receiver-visible condition → 在线/分区选择 lag、`B_L`、correlation distance 或 condition-aware multi-lag weight；仅 fixed short block/单训练结构/按场景离线调参不算 exact。
5. 必须单独判是否等价于 dev-frozen modulation/TS-length/receiver-power-conditioned single-lag lookup。
6. 不进入 Step 4a、不比较数值胜负、不设计方法、不触碰 p05/pyc/current views。

## 1. 背景（了解即可，不要对照评价）

Q1：Wang 2023 fixed-`B_L` FSTS 在固定 modulation/TS/power bin 内，若 receiver-visible turbulence/branch/phase-reliability condition 改变最优 lag/ranking，则 fixed design 不足。FACT 只到 fixed `B_L`/tradeoff/condition dependence；crossover/failure/headroom 均 UNKNOWN。R1 receipt 在 `search-archive/2026-08-09/rml-fsts-step3-5-search-citation-receipt.json`。

## 2. 任务详情

### 2.1 Acquisition 与 identity

逐篇记录所有实际通道、source URL、title/DOI evidence、path/SHA/bytes。若 publisher/DOI 记录出现未来年份、重复 DOI 或标题—内容错配，先 identity-abort，不做动作推断。

### 2.2 Fulltext action extraction

每篇强制提取：
- estimator/training action；lag/block/window/`B_L` 参数定义
- information source（modulation/TS/power/turbulence/branch/phase/reliability）
- decision granularity（dev-frozen / per scenario / per frame / per block / online）
- candidate set 与选择/weighting rule
- fixed vs adaptive/variable
- 与 Wang FSTS、Cheng/Tang/Enhanced 的比较角色
- exact collision? / generic prior art? / offline optimization? / cheap lookup equivalent? / adjacent?
- 每条结论的正文行号

### 2.3 产出格式（强制）

1. `## Acquisition/identity table`
2. `## Fulltext receipt table`
3. `## Action extraction`（逐篇）
4. `## Collision classification`
5. `## R2 disposition`：三篇各 must-read debt 是否关闭、哪些仍阻塞
6. `## Files changed and boundaries`

Receipt 必含 DOI/title/year/status（QUALIFIED_READ / FULLTEXT_UNAVAILABLE / IDENTITY_BLOCKED）、attempts、source/path/SHA/bytes、evidence lines、动作字段、classification、exact collision 与 cheap lookup 两个 boolean/unknown。

## 3. 已知陷阱

- `optimized short symbol block` 很可能只是离线选固定长度；标题含 optimized 不等于 adaptive。
- `under low received optical power` 是 condition 场景，不等于以 power/reliability 作为 selector input。
- single-tone multifunctional TS 可能同时做 branch phase correction/FOE，但动作对象仍可能不是 lag/`B_L`。

## 4. 验收

- [ ] 3/3 identity 与实际获取通道可复核。
- [ ] qualified 项都有 canonical path/SHA/bytes/read-note/正文行证据。
- [ ] exact/cheap lookup 裁决与 generic/offline/adjacent 分开。
- [ ] 无 Step4a/p05/pyc/current-view 修改。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-r2-must-read.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-r2-must-read-receipt.json`
