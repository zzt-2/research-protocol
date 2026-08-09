# Task Brief: Step 3.5 直接竞品获取与 provenance 修复

> 来源: S003 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-rml-acquisition-provenance.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本 T、目标 worktree 与项目工具链

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。
**你的任务**：对 Cheng 2020、OE.505931、OE.448956 实测合法获取通道；对 Tang 2022 与 WiSEE 2024 修复“metadata failed 但 PDF/content 存在”的 provenance 矛盾。若获得/修复可承重全文，完成 identity preflight 与限定动作提取。
**产出**：只写 acquisition worker-log、必要的 canonical paper metadata/content/read-note 与 receipt `search-archive/2026-08-09/rml-fsts-step3-5-acquisition-receipt.json`；不要改 topic/literature/decision/current views。

**最高纪律**：
1. 从目标 worktree 根目录按 `tools/download`→合法 OA/author copy→适用时 `tools/blit` 的顺序实际尝试；不得只看 help 或重复旧失败就跳过。付费墙不是伪造正文的理由。
2. PDF 转 Markdown 必须用 `tools/convert`；不自己写转换脚本。
3. 每篇承重全文必须记录 exact title、DOI、source URL/channel、canonical path、bytes、SHA256、title/DOI evidence。
4. abstract/metadata 不能冒充全文。Tang/WiSEE 只有 provenance 修复后才能承重；修复必须保留原始冲突与新证据，不能静默改写历史 receipt。
5. 不进入 Step 4a、不比较数值胜负、不设计 adaptive lag；不触碰四个 p05 日志，不改 `common/`/`params.py`/正式论文/dormant campaign。

## 1. 背景（了解即可，不要对照评价）

直接债务：
- Cheng 2020 `10.1016/J.OPTCOM.2020.126046`：low-OSNR joint frame/frequency sync。
- OE.505931 `10.1364/OE.505931`：real-time diversity combining + CPR。
- OE.448956 `10.1364/OE.448956`：optimal branch block phase correction。
- Tang 2022 `10.1109/JPHOT.2022.3161795` 与 WiSEE 2024 `10.1109/WiSEE61249.2024.10850117`：正文存在，但旧 metadata=`failed/all_failed`，receipt 因 provenance 不一致禁止承重。

Q1 exact action 是 receiver-visible condition → lag/`B_L`/correlation-distance selection 或 condition-aware multi-lag weighting。只要全文不实现该动作，就应归为 generic/offline/adjacent，而非碰撞。

## 2. 任务详情

### 2.1 执行方式

1. 先核验现有 `papers/doi/...` 与旧 Step2 receipt，不重复已成功正文。
2. 三篇缺失项各实际运行一次 `bash tools/download --doi DOI`；如工具因“已存在 metadata”跳过，实际运行 `--force` 的安全预览/正式通道，记录原始输出。对 Optica/Elsevier 可用项目 search/API 找 OA/author copy；`blit` 只在源实际适用时尝试，不假装支持。
3. Tang/WiSEE：核验 PDF magic/bytes/SHA、content title/DOI/正文有效行、metadata 与下载来源。若能从现有 source 文件、DOI identity、索引/API 与实际内容形成可审计链，写新的 provenance receipt；必要时只修 canonical metadata 的状态字段并保留 `previous_status/conflict_note`。不要改旧 Step2 receipt。
4. 对任何变成 qualified 的全文，做限定提取：method action、information source、decision granularity、condition inputs、online/offline、lag/window/BL 是否可变、是否 exact collision、证据行。若 5 篇过多或预计超过 15 分钟，优先 identity/provenance，全文读取拆给下一批 agent并在 receipt 标 `FULLTEXT_READ_PENDING`。

### 2.2 产出格式（强制）

1. `## 旧状态与实际尝试`：逐篇命令、返回、通道
2. `## Identity/provenance table`
3. `## Fulltext action table`（仅 qualified/read 项）
4. `## Unavailable evidence blockers`（一手全文不可得时精确说明）
5. `## Files changed`
6. `## Boundaries`

receipt 必含每篇 DOI/title、attempts、source/channel、status（QUALIFIED_FULLTEXT / PROVENANCE_REPAIRED_READ_PENDING / FULLTEXT_UNAVAILABLE / IDENTITY_BLOCKED）、paths、SHA256/bytes、title/DOI evidence、old conflict、新结论与是否可承重。

## 3. 已知陷阱

- `metadata.json` 的失败状态与磁盘正文冲突时，不能仅因正文能读就宣称修复；要解释 source 的来源链。
- Optica 两篇可能只提供 condition source/CPR 邻接动作；不要因为“turbulence/branch”词重合就判 lag collision。
- Cheng 可能只做 fixed training design/algorithm comparison；是否 online/conditioned 必须看全文。

## 4. 验收

- [ ] 五篇各有实际通道记录与可复核 status。
- [ ] qualified 项全部有 title/DOI/path/SHA/bytes。
- [ ] exact action 结论只来自全文证据；不可得项诚实阻塞。
- [ ] 无越界文件或 p05 变更。

## 附：产出回传位置

- `projects/thesis-fso/worker-logs/step-3-5-rml-acquisition-provenance.md`
- `search-archive/2026-08-09/rml-fsts-step3-5-acquisition-receipt.json`
