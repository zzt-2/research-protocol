# Coherent FSO 共同平台 GW Step 2 覆盖报告

> T042 | Groundwork Step 2 acquire/convert/coverage | 2026-08-30

## 文献覆盖面状态

- 审计范围：T039 固定 shortlist 8/8；未补新候选，未进入精读或形成 Q#。
- 成功获取并通过质量门：6 篇。
- 内容质量不达标：0 篇。
- 三轮止损后未获取：2 篇。
- Coverage verdict：`PASS_WITH_ONE_COVERAGE_GAP / USER_CONFIRMATION_REQUIRED`。数量门 `6 >= 5`，四类目标覆盖 3/4；按 `gw-acquire.md`，用户确认缺口前不得进入 Step 3。

### Qualified full text

| ID | 正式身份 | canonical 来源 | `wc -l` | 身份与转换核验 | 覆盖类别 |
|---|---|---|---:|---|---|
| L001 | Paillier et al., 2020, DOI `10.1109/JLT.2020.3003561` | `papers/arxiv/1911.11851/`，正式论文对应 arXiv `1911.11851` | 795 | 题名、作者匹配；HTML 转换无替换字符 | 星地 CFO / 激光相噪 |
| L010 | Bernini et al., 2022, DOI `10.1109/ICSOS53063.2022.9749703` | `papers/doi/10.1109_icsos53063.2022.9749703/` | 222 | IEEE PDF；题名、作者匹配；fast 转换可读 | 星地 coherent receiver / Doppler 前置 |
| L027 | Vieira et al., 2023, DOI `10.1109/ACCESS.2023.3287501` | `papers/doi/10.1109_access.2023.3287501/`，正式论文对应 arXiv `2212.02030` | 1814 | metadata DOI、题名与正文题名/作者匹配；HTML 转换无替换字符 | LEO optical Doppler / CFO |
| L035 | Faruk & Kikuchi, 2013, DOI `10.1109/JPHOT.2013.2251872` | `papers/doi/10.1109_jphot.2013.2251872/` | 368 | IEEE PDF；题名、作者、正文 DOI 匹配；standard 重转后替换字符 133→0 | receiver I/Q gain/phase/timing skew 与 FIR 来源 |
| L047 | Roudas et al., 2009, DOI `10.1109/JLT.2009.2035526` | `papers/doi/10.1109_jlt.2009.2035526/` | 3712 | IEEE PDF；题名、作者、正文 DOI 匹配；fast 转换可读 | Jones/unitary 与 PDL 边界 |
| L054 | Kuschnerov et al., 2009, DOI `10.1109/JLT.2009.2024963` | `papers/doi/10.1109_jlt.2009.2024963/` | 896 | IEEE PDF；题名、作者、正文 DOI 匹配；错误 arXiv 富化件已拒绝并替换 | 光纤 PMD/PDL 与 receiver DSP 边界 |

### 三轮止损后失败

| ID | 文献 | Round 1 `tools/download` | Round 2 arXiv 同题版本 | Round 3 IEEE/CNKI | 结论 |
|---|---|---|---|---|---|
| L023 | Faruk & Kikuchi, 2011, DOI `10.1364/OE.19.012789` | `all_failed` | T039 元数据无同题 arXiv | 不适用：Optics Express，非 IEEE/CNKI | `FAILED`；其 receiver-filter/FIR 功能由 L035+L054 覆盖，不构成独立覆盖 blocker |
| L040 | Dong et al., 2023, DOI `10.3788/COL202321.100101` | `all_failed` | T039 元数据无同题 arXiv | 不适用：Chinese Optics Letters，不在当前 IEEE/CNKI 下载通道 | `FAILED`；造成大气偏振类别无 qualified 全文 |

## 覆盖面分析

| 目标类别 | 状态 | Qualified 支撑 |
|---|---|---|
| Jones / unitary-PDL 边界 | `COVERED` | L047、L054 |
| 星地 CFO / 相噪 | `COVERED` | L001、L010；L027 提供独立 LEO Doppler 边界 |
| 大气偏振 | `GAP` | 唯一直接候选 L040 未取得全文 |
| receiver filter / skew | `COVERED` | L035、L054；L023 失败不改变类别覆盖 |

当前覆盖达到 T042 要求的至少三类，但偏向 coherent receiver/DSP 与可获得的 IEEE/arXiv 文本。大气偏振只有搜索元数据级证据，不能在 Step 3 中当作已精读 authority。

## 引用质量分析

- 正式发表身份：6/6（100%）；六篇均有正式 DOI。
- 当前全文载体：publisher/IEEE PDF 4/6，正式论文对应 arXiv HTML 2/6；arXiv-source 占比 `2/6 = 33.3%`。
- 预印本-only 身份：0/6。Paillier 2020 与 Vieira 2023 的当前载体虽来自 arXiv，但已用正式 DOI 绑定 canonical identity。

## 获取与身份异常记录

- `papers/index.json` 曾把 Paillier 2020 标为 success 但指向不存在的 DOI 目录；本次改为实际 arXiv canonical 路径并补齐正式 DOI/题名。
- Kuschnerov 2009 的强制重取曾被工具误富化为 arXiv `1212.1021v1`，实际题名为 “DSP Based PMD Emulators for Built-in Testing of Coherent Optical Receivers”；该错误版本未计入，Round 3 重新取得 DOI `10.1109/JLT.2009.2024963` 的 IEEE PDF。
- blit 对部分 IEEE PDF 的页眉自动报 title mismatch；最终以正文题名、作者和 DOI 三项人工核验为准。

## 唯一 blocker 与用户行动项

**唯一 blocker：L040 Dong 2023 全文不可得，导致“大气偏振”目标类别仍为 `GAP`。** 用户需二选一确认后才能进入 Step 3：

- [ ] 手动获取 DOI `10.3788/COL202321.100101`，按 `papers/manual/{slug}/` 规范入库并转换；或
- [ ] 显式接受当前 6 篇、3/4 类覆盖，并把大气偏振保留为 claim limitation。

L023 Faruk 2011 可选补充，但 receiver filter/skew 已由 L035+L054 覆盖，不是 Step 3 的独立 blocker。
