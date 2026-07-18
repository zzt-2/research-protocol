# Task Brief: residual cascade GW Step 2 获取与质量门

> 来源: S036 / R009 | 产出位置: `papers/{doi|arxiv}/.../content.md` + `.sessions/2026-07-10-dual-pol-osl-groundwork/S037-residual-cascade-acquire.md`
> 日期: 2026-07-16
> 唯一文档: 执行方只执行本任务列出的下载/转换，不做精读、不跑仿真、不改项目代码

## 0. TL;DR

基于 R009 Step 1，获取以下强邻近全文，核查它们到底是完整 NN、CMA+NN 联合、post-equalizer 还是 additive residual：

1. DOI `10.3390/mi13101617` — *Demonstration of 144-Gbps Photonics-Assisted THz Wireless Transmission at 500 GHz Enabled by Joint DBN Equalizer*
2. DOI `10.1109/JSAC.2022.3191346` — *Blind Equalization and Channel Estimation in Coherent Optical Communications Using Variational Autoencoders*
3. DOI `10.1109/JLT.2022.3146839` — *Convolutional Neural Network-Aided DP-64QAM Coherent Optical Communication Systems*
4. DOI `10.1109/JLT.2021.3056869` — *Soft-Demapping for Short Reach Optical Communication: A Comparison of DNNs and Volterra Series*
5. DOI `10.1109/JSTQE.2022.3174268` — *Neural Networks-Based Equalizers for Coherent Optical Transmission: Caveats and Pitfalls*
6. 如可从 Step1 元数据获得正式来源，再尝试 FSO ANN 邻近 DOI `10.1007/s11276-025-03916-4`；失败不阻塞首批质量门。

## 1. 最高纪律

1. 运行前先做 Python/依赖检查；下载先 `--dry-run`。
2. 只用 `tools/download` → 必要时 arXiv 版本 → 必要时 `tools/blit --download`；三轮后停止。
3. 每篇成功转换后检查 `content.md` 行数，<50 行标质量失败，不进入精读。
4. 路径只能在 `papers/doi/{doi_path}/` 或 `papers/arxiv/{id}/`，禁止手建其他论文目录。
5. 不用 web reader/ResearchGate/Semantic Scholar 页面抓全文；本任务不写 literature_notes，不下 Go/No-Go。

## 2. 执行与产出

- 从项目根目录读取 `tools-guide.md` 下载段和 `stages/gw-acquire.md`。
- 对六个 DOI 先 dry-run，再批量下载；记录每轮成功/失败、来源、转换命令。
- 对成功文件执行 `wc -l content.md`，记录有效行数和明显错配/乱码。
- 写 `S037-residual-cascade-acquire.md`，包含：目标清单、环境检查、第一/二/三轮结果、质量门、覆盖面缺口、下一步用户行动项。

## 3. 验收

- [ ] 每个 DOI 有明确成功、失败或跳过原因
- [ ] 成功文件均有 `content.md` 和行数
- [ ] 失败论文列出下一可执行通道，不超过三轮
- [ ] 明确当前是否达到 ≥5 篇、≥50 行的 Groundwork 获取门槛
- [ ] 不产出方向 Go，不开始 MVE
