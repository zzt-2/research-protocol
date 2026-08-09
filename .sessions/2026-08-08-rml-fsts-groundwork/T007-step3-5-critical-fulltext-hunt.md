# Task Brief: Step 3.5 关键旧债务 lawful fulltext hunt

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-critical-fulltext-hunt.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与 T004 receipt

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。T004 的常规工具通道未取得三篇直接债务全文。
**你的任务**：用 bounded web/API/作者机构存档检索，为下列 4 篇寻找合法全文或明确一手阻塞；若获得全文，完成 identity、转换与动作裁决。

- Cheng 2020 `10.1016/J.OPTCOM.2020.126046`
- OE.505931 `10.1364/OE.505931`
- OE.448956 `10.1364/OE.448956`
- Dong 2009 `10.1109/CHINACOM.2009.5339877`

**产出**：worker-log + `search-archive/2026-08-09/rml-fsts-step3-5-critical-fulltext-hunt-receipt.json`；必要 canonical paper/read-note。

**最高纪律**：
1. 优先官方 DOI/Crossref/OpenAlex/S2/Unpaywall、作者主页、大学/机构 repository；可以 web search 定位，但事实断言必须用 DOI/API abstract 或全文交叉验证。禁止把 ResearchGate/Google Scholar 页面当全文/一手证据。
2. 每篇最多 4 个不同通道、总计不超过 15 分钟；重复同一付费墙不算新通道。达到上限即停并记录。
3. PDF 转 Markdown 必须用 `tools/convert`；不得自己写转换器。
4. abstract/metadata 不能冒充全文 action。全文不可得时只允许 `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT`。
5. exact action=receiver-visible condition → lag/`B_L`/correlation-distance selection 或 condition-aware multi-lag weighting；必须区分 generic multi-lag、fixed/offline optimization、cheap conditioned lookup、architecture adjacent。
6. 不进入 Step 4a、不比较数值、不设计方法；不改 current views，不触碰 p05/pyc。

## 1. 背景（了解即可，不要对照评价）

T004 receipt：`search-archive/2026-08-09/rml-fsts-step3-5-acquisition-receipt.json`。Cheng/两篇 Optica 已实际走项目 wrapper/等价工具与官方站点但失败；本任务只补不同 provenance family 的 bounded author/institutional search。Dong 是 2009 generic multi-correlation-lag historical debt，不满足 2019+ recent 门，但约束宽泛 multi-lag 主张。

## 2. 任务详情

### 2.1 通道表

逐篇记录 query/URL/API、HTTP/status、是否 primary/lawful、结果路径。找到 PDF 后核验 magic、title、DOI、SHA/bytes，再用 `tools/convert`。

### 2.2 动作提取（仅 qualified fulltext）

提取 estimator action、lag/window/block/`B_L` 定义、condition information、decision granularity、online/offline、selection/weighting rule、comparators、exact/cheap lookup classification，附正文行号。

### 2.3 产出格式（强制）

1. `## Bounded channel attempts`
2. `## Identity/fulltext receipt`
3. `## Action extraction`（仅全文）
4. `## Remaining blocker and claim ceiling`
5. `## Files changed and boundaries`

Receipt 每篇必须有 attempts≤4、source families、status、path/SHA/bytes（有则给）、fulltext action fields、classification、can_bear_weight。

## 3. 已知陷阱

- Optica abstract 已足以说明 branch-phase/CPR 邻接，但不能排除全文中的 lag/window 细节。
- Cheng 的“joint frame/frequency”与 low OSNR 条件不等于 condition→lag selector。
- Dong 的 multiple correlation lags 可占 generic prior art，但是否 variable/weighted 必须全文。

## 4. 验收

- [ ] 4 篇均有 bounded、多 family 实测记录。
- [ ] 取得全文者有 identity/SHA/bytes/正文行；不可得者不伪动作终判。
- [ ] 无越界文件、p05/pyc/current-view 修改。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-critical-fulltext-hunt.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-critical-fulltext-hunt-receipt.json`
