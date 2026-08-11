# Step 1 Search Receipt

> 2026-08-11 | 两轮 | query cap 6/6 | 不含下载与全文精读

## Query 与返回量

| Round | ID | Query（冻结原文） | 返回 |
|---|---|---|---:|
| 1 | Q1 | coherent optical free-space optical multi-aperture post-DSP combining invalid branch outage discard | 0 |
| 1 | Q2 | coherent free-space optical multiple aperture diversity combining DSP outage branch discard | 18 |
| 1 | Q3 | robust maximum ratio combining channel estimation error reliability weighted diversity combining | 50 |
| 2 | Q4 | generalized selection combining hybrid selection maximum ratio combining channel estimation error | 48 |
| 2 | Q5 | pilot residual synchronization confidence cycle slip detection metric diversity combining receiver reliability | 22 |
| 2 | Q6 | multi-aperture coherent optical receiver adaptive digital combining phase estimation error low SNR branch | 31 |

## 机械回执

- 六个结果文件总行数：169。
- 按 DOI；无 DOI 时按规范化 title 去重：157 unique，超过 `≥20` 门。
- 实际有贡献的搜索源：Semantic Scholar、OpenAlex、Tavily，共 3 个。arXiv、Exa、SerpAPI 本轮 0 贡献，不计入来源门。
- 语义候选矩阵：27 unique；正式身份 24，unknown 3，正式占比 `24/27=88.89%`。unknown 不计正式。
- 必读：8，超过 `≥5` 门。
- 技术路线：A hard admission；B soft robust weighting；C 因无时序物理前提而不保留为当前路线。
- 逐条语义初筛由 T001/T002 分离执行；`relevance_score` 未作为分类依据。

## 结果文件

- `search-archive/2026-08-11/dsp-outage-multi-aperture-q1.json`
- `search-archive/2026-08-11/dsp-outage-multi-aperture-q2.json`
- `search-archive/2026-08-11/dsp-outage-multi-aperture-q3.json`
- `search-archive/2026-08-11/dsp-outage-multi-aperture-q4.json`
- `search-archive/2026-08-11/dsp-outage-multi-aperture-q5.json`
- `search-archive/2026-08-11/dsp-outage-multi-aperture-q6.json`

## 限制

Q1 的超长 exact phrase 得 0；Q5 大量命中 GNSS cycle-slip 噪声；Q3/Q4 的 RF 召回较宽。以上未以“高返回量”冒充有效证据，候选矩阵只保留动作或失效机制可判读的 27 项。2019 direct competitor 与 Geisler 的 S2/OpenAlex 交叉证据来自本轮开始前已存在的全局索引，不计为第七组 query；可复算摘录见 `step1-provenance-receipt.md`。
