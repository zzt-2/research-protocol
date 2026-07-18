# [S037] residual cascade GW Step 2 获取与质量门

> 2026-07-16 | GW Step 2 | 状态：PARTIAL，覆盖面缺口阻塞 Step 3 全量门

## 目标

获取 R009 选出的 CMA+NN/神经均衡强邻近论文，按 `gw-acquire.md` 完成下载、转换和 `content.md` 质量检查，为 residual cascade 的 Step 3 精读提供真实全文输入。

## 记录

### 环境检查

- WSL `~/.venvs/torch/bin/python` 依赖检查 PASS：requests、pymupdf、pymupdf4llm、serpapi、tavily 均可导入。
- 使用 `tools/download`、`tools/blit --source ieee --download`、`tools/convert`；未使用 web reader 或网页全文抓取。

### 获取结果

| 目标 | 结果 | 证据/原因 |
|---|---|---|
| JSAC 2022 VAE，DOI `10.1109/JSAC.2022.3191346` | **PASS** | `papers/doi/10.1109_jsac.2022.3191346/content.md` 419 行；arXiv 2204.11776 同文 82651 字节；IEEE Blit 9831780.pdf 成功 |
| JLT 2021 DNN vs Volterra，DOI `10.1109/JLT.2021.3056869` | **PASS** | `papers/doi/10.1109_jlt.2021.3056869/content.md` 653 行；arXiv 2501.05979 为同文重复 |
| JSTQE 2022 Caveats，DOI `10.1109/JSTQE.2022.3174268` | **PASS（arXiv）** | `papers/arxiv/2109.14942/content.md` 145392 字节；DOI 自动下载未成，但 arXiv 全文质量 good |
| JLT 2022 CNN DP-64QAM，DOI `10.1109/JLT.2022.3146839` | **PASS** | IEEE Blit 成功 `papers/downloads/2026-07-16/9695357.pdf`（3.4MB）；`papers/doi/10.1109_jlt.2022.3146839/9695357.md` 已产出 53777 字节，PDF 首页标题核对 PASS |
| Micromachines 2022 J-DBN，DOI `10.3390/mi13101617` | **FAIL** | `tools/download` 首轮及 standard/force 重试均 all_failed；未找到可用 arXiv/IEEE 通道 |
| Wireless Networks 2025 FSO ANN，DOI `10.1007/s11276-025-03916-4` | **FAIL** | `tools/download` 首轮及 standard/force 重试均 all_failed；Step1 仅有弱摘要命中 |
| JLT/IEEE 三轮补救 | **PARTIAL** | JSAC/JLT 2022 Blit 成功，JSTQE IEEE 查询 0 结果；JLT 2022 转换仍需后续处理 |

### 去重后的质量门

- 可读全文：4 篇唯一目标论文（VAE、DNN/Volterra、Caveats、CNN DP-64QAM）；重复目录不重复计数。
- 共享 corpus 中另有直接相关的第五篇全文：`papers/doi/10.1109_jlt.2023.3276637/content.md`（Liu et al., CMA-based complex-valued MIMO adaptive equalizer for FSO，39481 字节；metadata 记录 2026-07-10 已获取）。它不是 additive-neural-residual，而是强邻近 CMA/FSO 对照，纳入 Step 3 的邻近证据而不冒充直接命中。
- `content.md ≥50`：5/5 通过（第五篇同样超过阈值）。
- Groundwork Step 2 硬门：**达到 ≥5 篇可读核心/邻近全文**，Step 3 可启动；精读时必须逐篇做标题、来源和“直接/邻近”分类自检。

## 决策引用

- R009：Step1=DEFER，要求验证残差来源和简单 DSP baseline。
- D042：自主推进不改变 GW 硬门。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

1. JLT 2022 的转换结果已找到并纳入计数；不手写 PDF 转换器。
2. 现在派 worker 按 `gw-read.md` 14+字段/7子表/问题四判据执行精读；此前不得进入 Step 4a 或 MVE。
4. 下载失败清单需用户知悉；本轮用户已授权持续推进，但若需要手动获取付费墙论文，需明确记录而不能默默替代。
