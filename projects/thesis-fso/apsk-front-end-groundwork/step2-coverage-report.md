# Ch4 APSK 前端 Groundwork Step 2 覆盖报告

> 任务：T043 | 日期：2026-08-30 | 范围：仅 C4-1 / C4-2 全文获取与质量门
> task-control：`PASS`（`rdl.task-control.v2` / epoch 2 / CP002 / `GROUNDWORK_ACQUIRE`）

## 文献覆盖面状态

- 尝试的 Ch4 候选：7 篇。
- qualified full text：5 篇。
- failed：2 篇。
- coverage verdict：**BLOCKED**。数量门已过，但“APSK 直接使用至少一篇”未满足，禁止进入 Step 3。

| 文献 | 角色 | identity | 有效行数 | 转换质量 | 结论 |
|---|---|---:|---:|---|---|
| Godard 1980, `10.1109/TCOM.1980.1094608` | CMA canonical | PASS，正文首标题精确匹配 | 520 | standard OCR；无替换乱码，正文与公式/图像均有内容 | qualified |
| Yang–Werner–Dumont 2002, `10.1109/JSAC.2002.1007381` | MMA canonical | PASS，正文标题/作者/年份匹配 | 7258 | fast；正文连贯，无替换乱码 | qualified |
| Ready–Gooch 1990, `10.1109/ICASSP.1990.115806` | RDE canonical | PASS，正文首标题精确匹配 | 128 | standard OCR；无替换乱码，正文与图像均有内容 | qualified |
| Fatadin–Ives–Savory 2009, `10.1109/JLT.2009.2021961` | coherent 16-QAM 中 CMA/RLS-CMA/RDE/DD comparator | PASS，正文标题/作者/年份匹配 | 872 | fast；正文连贯，无替换乱码 | qualified |
| Kikuchi 2011, `10.1587/ELEX.8.1642` | coherent/Jones、PMD 与偏振解复用 authority | PASS，正文标题/作者/卷期匹配 | 544 | fast；正文连贯，无替换乱码 | qualified |
| Xu 2013, “Hybrid Blind Equalizing Method for APSK Signals” | APSK 直接 CMA+RDE collision 邻居 | 仅 metadata，无法核正文 identity | 0 | 无全文 | failed |
| Di Rosa–Richter 2021, `10.1109/JLT.2021.3098220` | pilot-symbol likelihood RDE 同轴主 comparator | DOI/OA metadata 可核，全文未落盘 | 0 | `all_failed` | failed |

## 三轮止损回执

1. **Round 1 — `tools/download`**：dry-run 完成。仓库 wrapper 因 CRLF 在 WSL 下报错，未修改工具；随后调用同仓库 `tools/paper_download.py` 后端。Ch4-only 批量命令在 304 秒无增量输出后按命令级上限记 `timeout`。该轮落盘 Kikuchi；Xu 仅 metadata；Fatadin 的自动 arXiv fallback 命中错误论文，未作为合格正文。
2. **Round 2 — arXiv/OA fallback**：T040 中 Godard/Yang/Ready/Xu 均无已知 `arxiv_id`，不发起新方向检索。复用 T040 OA 条目：Kikuchi 为 cache hit；Di Rosa–Richter 2021 返回 `all_failed`。
3. **Round 3 — `tools/blit` exact DOI**：Godard、Yang、Ready、Fatadin 的 IEEE exact DOI 均成功下载非空 PDF。对 Godard/Yang/Fatadin 的页眉型自动 title mismatch，以转换正文首标题复核后纠正为 match。
4. **转换质量补救 — `tools/convert`**：Yang/Fatadin fast 转换通过；Godard/Ready fast 只抽出授权页脚，按 `gw-acquire` 对关键论文各做一次 standard OCR 重转后通过。此动作不新增下载轮次。

## 覆盖面分析

| 强制覆盖项 | 状态 | 证据 |
|---|---|---|
| CMA/MMA/RDE canonical 中至少两类 | PASS | 三类均有 qualified canonical：Godard / Yang / Ready–Gooch |
| APSK 直接使用至少一篇 | **FAIL** | Xu 2013 无全文；没有其他 qualified APSK 直接均衡论文 |
| coherent/Jones 或 pilot/DD comparator 至少一篇 | PASS | Kikuchi 2011 + Fatadin 2009 |
| qualified 数量 ≥5 | PASS | 5 篇 |

当前 qualified 集全部为正式发表论文，预印本 0/5（0%）。IEEE/IEICE 来源覆盖充分；偏差集中在 APSK 直接均衡论文无法通过自动获取通道。

## 未获取的 direct collision / main comparator

- **Xu 2013 — APSK hybrid CMA+RDE direct collision**：限制 **C4-2**。没有正文就不能核对 weighted CMA/RDE、radial dispersion 与 soft switching 是否吸收 ring-aware semi-blind refinement 的核心动作。
- **Di Rosa–Richter 2021 — pilot-symbol likelihood RDE main comparator**：限制 **C4-2** 的信息公平性核对；其全文缺失使 pilot/payload likelihood 信息合同无法在 Step 3 中逐式核验。
- **C4-1**：本轮没有未获取的 frozen direct collision；Kikuchi 已满足 Jones/coherent authority 覆盖，但这里只确认可读材料存在，不提前判断 scaled-unitary 合法性。

## 唯一 blocker

**缺少至少一篇通过 identity 与内容质量门的 APSK 直接均衡全文。** 该缺口使强制覆盖门失败，并阻塞 C4-2 进入 Step 3；首选人工补充 Xu 2013 全文到 `papers/manual/hybrid-blind-equalizing-method-for-apsk-signals/` 后用 `tools/convert` 转为 `content.md` 再复核。

## 边界声明

- 未精读公式、未形成 Q#、未作 C4-1/C4-2 Go/Kill、未运行实验。
- Layton 2018 与 Zhang–Kim 2013 属 C5，未计入本报告 qualified/failed、coverage 或提交白名单。
- 本报告是 Step 2 覆盖门，不产生论文结论。
