# Ch4 direct APSK equalization 全文缺口闭合

> 任务：T045 | 日期：2026-08-30 | 终态：PASS

## 获取结果

- T040-023，`Newton-like minimum entropy equalization algorithm for APSK systems`，DOI `10.1016/j.sigpro.2014.02.003`：项目下载链返回 `all_failed`。
- T040-010，`Joint equalization of frequency offset and phase noise using two-stage cascaded extended Kalman filter for discrete spectrum 16/64APSK NFDM systems`，DOI `10.1364/oe.512167`：项目下载链返回 `all_failed`。
- T040-037，`A comparison between APSK and QAM in wireless tactical scenarios for land mobile systems`，DOI `10.1186/1687-1499-2012-317`：通过 SpringerOpen OA PDF 获取成功。

成功一篇后已停止，没有新增搜索 query。

## 全文质量门

- 正式身份：Marco Baldi, Franco Chiaraluce, Antonio de Angelis, Rossano Marchesani, Sebastiano Schillaci；*EURASIP Journal on Wireless Communications and Networking*, 2012:317；DOI `10.1186/1687-1499-2012-317`。
- 题名一致性：`metadata.json` 记录 `title_check: match`、`title_overlap: 1.0`；`content.md` 正文题名与检索记录完全一致。
- 文件：`papers/doi/10.1186_1687-1499-2012-317/source.pdf`、`content.md`、`metadata.json`。
- 正文质量：下载器标记 `content_quality: good`；`content.md` 共 561 行，其中非空文本有效行 281，超过 50 行门槛；摘要、系统模型、APSK 星座、接收端均衡、性能结果、结论和参考文献均可读。

## 可读性定位（不做方法裁决）

- multi-ring cost/update：正文没有给出 ring-aware blind cost 或按环更新；可定位到接收端 DFE，滤波器系数采用 LMS 更新（`content.md:161`），因此覆盖的是直接作用于 APSK 符号流的通用 DFE/LMS 均衡链。
- APSK constellation assumptions：采用 DVB-S2 风格 4+12-APSK，两同心环、16 阶；半径比 `r2/r1 = 2.7`、相位差为 0，并使用 pseudo-Gray labeling（`content.md:103-123`）。
- comparator：主要比较同阶 16-QAM；两种调制在相同 multipath/DFE、非线性和 coded/uncoded 条件下报告 BER 等结果（`content.md:43-45, 161-163, 400-445`）。

## 结论

**PASS**：已取得一篇正式身份、题名一致、有效正文不少于 50 行的 direct APSK equalization 全文，闭合 Ch4 Step 2 的唯一全文缺口。本报告不形成 Q#，不进入 Step 3。
