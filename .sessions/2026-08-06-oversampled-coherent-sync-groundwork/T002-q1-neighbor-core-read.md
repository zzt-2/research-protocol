# Task Brief: Q1 近邻与系统链 CORE 全文精读

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-sync-read-b.md`
> 日期: 2026-08-06
> 唯一文档: 执行方只需本任务书、列出的论文全文及其中引用的规范文件

## 0. TL;DR

精读三篇全文。前两篇/第三篇实际全文位于共享主根 `D:/code/study/research-protocol/papers/...`，产出中的 canonical 源路径仍写 `papers/.../content.md`：

1. Wang et al. 2023, *Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication*，`papers/doi/10.1109_jphot.2023.3265847/content.md`；
2. Wang et al. 2024, *Enhanced frame synchronization and carrier recovery in coherent FSO communication: a pseudo-random and cyclic QPSK approach*，`papers/doi/10.1364_oe.520452/content.md`；
3. Le Bidan et al. 2023, *Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link*，`papers/doi/10.1109_icsos59710.2023.10490279/content.md`。

只做事实提取，用 `apply_patch` 写 `projects/thesis-fso/worker-logs/step-3-sync-read-b.md`。

最高纪律：全文/title 自检；不把 1-sps 或 downsampled action 冒充 sample-level joint action；判据 3 必须 2019+ task-matched；不进入检索、Step 4a、实现或仿真。

## 1. 背景

Q1 要核查 sample-level frame/fractional timing/CFO acquisition。重点判断 sequential polyphase-bank + STSB/FSTS 是否构成足够强且廉价的 comparator，以及剩余 delta 是否只是实现顺序重排。GEO 论文还需明确 2-sps waveform 与 frame/timing/CFO 的真实处理顺序。

## 2. 执行方式

完整读取 `stages/gw-read.md`、`stages/glossary.md`、`templates.md` literature_notes/实验完备性模板、`domain-comms.md` §1.1/§7。每篇执行 title abort 协议，再读 method/experiment/result/conclusion/系统模型。

## 3. 产出格式（强制）

逐篇输出标准 14+ 字段，并显式列 receiver-visible information、action、output、时序、baseline、failure condition。逐篇给 7 子表：状态/输入、动作、目标/奖励（N/A+原因）、建模假设、网络架构（N/A+原因）、适配性、M-C-A+四判据；附信道模型参数表和≤20行实验完备性。Wang 2024 与 GEO 2023 提取写作架构，避免长引原文。

本组综合必须给：三篇五维 collision 表；FSTS/STSB 与独立 timing 组合的 comparator 证据；GEO 链的 sample-rate/processing order；Q1 剩余 delta 是否联合动作或顺序调整；供 Step 3.5 的共同引用与关键词。每项附 `content.md:行号` 或章节/公式。

## 4. 验收

- 三篇身份结果、标准字段、7子表、通信参数与实验完备性齐全。
- 清楚区分 1 sps、2 sps、下采样后处理、block timing 与 sample-level fractional timing action。
- 不写 Go、METHOD_SIGNAL、新颖性闭合或 Step 4a 结论。
