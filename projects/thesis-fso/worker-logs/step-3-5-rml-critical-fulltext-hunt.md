# Step 3.5 RML critical fulltext hunt

> Task: `T007-step3-5-critical-fulltext-hunt.md`
> Date: 2026-08-09
> Terminal: `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT` (4/4 items)

## Bounded channel attempts

每篇严格使用 4 个不同 provenance family；T004 已尝试的项目 wrapper/Elsevier API/Optica viewmedia 不在本轮重复。ResearchGate 仅作为搜索结果噪声记录，未下载、未作为全文或一手证据。

| DOI | # | family | query / URL | result | primary / lawful |
|---|---:|---|---|---|---|
| `10.1016/J.OPTCOM.2020.126046` | 1 | exact-title author/institution web discovery | exact title + PDF；`site:hust.edu.cn`；Qian Cheng / Sheng Cui / Keji Zhou | 仅命中 ScienceDirect preview 与 ResearchGate request page；无作者/华中科技大学 PDF | discovery lawful；RG 不承重 |
|  | 2 | OpenAlex API | `https://api.openalex.org/works/https%3A%2F%2Fdoi.org%2F10.1016%2Fj.optcom.2020.126046` | HTTP 200；`oa_status=closed`；无 repository / PDF | API primary metadata / lawful |
|  | 3 | Unpaywall API | `https://api.unpaywall.org/v2/10.1016%2Fj.optcom.2020.126046` | HTTP 200；`is_oa=false`；0 OA locations | API primary OA index / lawful |
|  | 4 | official DOI/publisher delivery | `https://doi.org/10.1016/J.OPTCOM.2020.126046` → Elsevier/ScienceDirect | DOI redirect HTTP 200；publisher page仅 Article preview/section snippets，并明确要求机构登录；非完整正文/PDF | publisher primary / lawful；非全文 |
| `10.1364/OE.505931` | 1 | exact-title author/institution web discovery | exact title + PDF；`site:bupt.edu.cn`；Kejia Xu / Jian Wu | 仅命中 PubMed/ResearchGate/二手索引；无作者/BUPT repository PDF | discovery lawful；RG 不承重 |
|  | 2 | OpenAlex API | `https://api.openalex.org/works/https%3A%2F%2Fdoi.org%2F10.1364%2Foe.505931` | HTTP 200；Gold OA；best landing=DOI；repository 仅 PubMed、无 PDF | API primary metadata / lawful |
|  | 3 | Unpaywall API | `https://api.unpaywall.org/v2/10.1364%2Foe.505931` | HTTP 200；Gold OA；publisher landing only；`url_for_pdf=null` | API primary OA index / lawful |
|  | 4 | official DOI/Optica OA delivery | `https://doi.org/10.1364/OE.505931` | redirect到 Optica 后 Radware captcha；HTTP 200 `text/html`，15,064 bytes，title=`Radware Captcha Page`，非 PDF | publisher primary / lawful；交付阻塞 |
| `10.1364/OE.448956` | 1 | exact-title author/institution web discovery | exact title + PDF；`site:bupt.edu.cn`；Liqian Wang / Xinyu Tang | 仅命中 PubMed/ResearchGate/引用页；无作者/BUPT repository PDF | discovery lawful；RG 不承重 |
|  | 2 | OpenAlex API | `https://api.openalex.org/works/https%3A%2F%2Fdoi.org%2F10.1364%2Foe.448956` | HTTP 200；Gold OA；best landing=DOI；repository 仅 PubMed、无 PDF | API primary metadata / lawful |
|  | 3 | Unpaywall API | `https://api.unpaywall.org/v2/10.1364%2Foe.448956` | HTTP 200；Gold OA；publisher landing only；`url_for_pdf=null` | API primary OA index / lawful |
|  | 4 | official DOI/Optica OA delivery | `https://doi.org/10.1364/OE.448956` | redirect到 Optica 后 Radware captcha；HTTP 200 `text/html`，15,062 bytes，title=`Radware Captcha Page`，非 PDF | publisher primary / lawful；交付阻塞 |
| `10.1109/CHINACOM.2009.5339877` | 1 | exact-title author/institution web discovery | exact title + PDF；Xue Dong / Kewu Peng / Jian Song | 仅命中引用页、ResearchGate profile/abstract；无清华机构 PDF | discovery lawful；RG 不承重 |
|  | 2 | OpenAlex API | `https://api.openalex.org/works/https%3A%2F%2Fdoi.org%2F10.1109%2Fchinacom.2009.5339877` | HTTP 200；`oa_status=closed`；无 repository / PDF | API primary metadata / lawful |
|  | 3 | Unpaywall API | `https://api.unpaywall.org/v2/10.1109%2Fchinacom.2009.5339877` | HTTP 200；`is_oa=false`；0 OA locations | API primary OA index / lawful |
|  | 4 | official DOI/IEEE delivery | `https://doi.org/10.1109/CHINACOM.2009.5339877` | IEEE landing HTTP 202 `text/html`，2,055 bytes；无 PDF magic / `citation_pdf_url` | publisher primary / lawful；非全文 |

## Identity/fulltext receipt

| DOI | exact identity | fulltext status | canonical path / SHA / bytes |
|---|---|---|---|
| `10.1016/J.OPTCOM.2020.126046` | title、DOI、作者 Qian Cheng/Sheng Cui/Keji Zhou/Deming Liu 与 publisher preview 对齐 | `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT` | 无 / null / null |
| `10.1364/OE.505931` | title、DOI、作者与 PubMed/OpenAlex/Optica DOI 对齐 | `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT` | 无 / null / null |
| `10.1364/OE.448956` | title、DOI、作者与 PubMed/OpenAlex/Optica DOI 对齐 | `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT` | 无 / null / null |
| `10.1109/CHINACOM.2009.5339877` | title、DOI、作者 Xue Dong/Kewu Peng/Jian Song 与 OpenAlex/IEEE DOI 对齐 | `FULLTEXT_UNAVAILABLE_AFTER_BOUNDED_HUNT` | 无 / null / null |

没有新增 canonical paper 或 read-note；没有 PDF，因此未调用 `tools/convert`。

## Action extraction

无。四篇均未获得 qualified fulltext；依 T007，abstract、publisher preview、搜索引擎摘录和 ResearchGate 页面不得冒充全文 action。

## Remaining blocker and claim ceiling

- Cheng 2020：一手 preview 可支持其身份与 low-OSNR joint frame/frequency synchronization 的摘要级角色；不能终判 lag/window/`B_L` 定义、选择/加权规则、online/offline 或 condition-aware collision。分类保持 `UNRESOLVED_TASK_MATCHED_METADATA_ONLY`。
- OE.505931：摘要级可支持 CV-DD-LMS 同时做 diversity combining 与 CPR 的 architecture-adjacent 身份；不能据此排除正文中 lag/window 细节。分类保持 `ARCHITECTURE_ADJACENT_ABSTRACT_ONLY`。
- OE.448956：摘要级可支持 optimal branch block phase correction 的 architecture-adjacent 身份；搜索结果展示的正文片段来自 ResearchGate，不能承重。分类保持 `ARCHITECTURE_ADJACENT_ABSTRACT_ONLY`。
- Dong 2009：exact-title/abstract 可约束 generic multi-correlation-lag historical prior-art 警报，但不能终判其是否 variable/weighted、AFC loop 的规则或 condition-aware action。分类保持 `GENERIC_MULTI_LAG_IDENTITY_ONLY`。
- 四篇 `can_bear_weight=false`。本轮只能报告 acquisition blocker，不能把“未取得全文”改写为“不存在 collision”。

## Files changed and boundaries

- 新增：`projects/thesis-fso/worker-logs/step-3-5-rml-critical-fulltext-hunt.md`
- 新增：`search-archive/2026-08-09/rml-fsts-step3-5-critical-fulltext-hunt-receipt.json`
- 未改 current views、topic/literature/decision files；未触碰 p05/pyc；未进入 Step 4a、方法设计、仿真或数值比较。
