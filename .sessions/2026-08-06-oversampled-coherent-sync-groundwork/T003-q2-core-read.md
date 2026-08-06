# Task Brief: Q2 维护与重捕获 CORE 全文精读

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-sync-read-c.md`
> 日期: 2026-08-06
> 唯一文档: 执行方只需本任务书、列出的论文全文及其中引用的规范文件

## 0. TL;DR

精读两篇全文：

1. Paillier et al. 2020, *Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop*，证据 worktree `papers/doi/10.1109_jlt.2020.3003561/content.md`；
2. Valjus et al. 2025, *Review and Analysis of Digital Signal Processing Algorithms for Coherent Optical Satellite Links*，实际全文 `D:/code/study/research-protocol/papers/doi/10.1002_sat.1553/content.md`，canonical 源路径写 `papers/doi/10.1002_sat.1553/content.md`。

只做事实提取，用 `apply_patch` 写 `projects/thesis-fso/worker-logs/step-3-sync-read-c.md`。

最高纪律：全文/title 自检；区分 GG/fade 动机与“timing/carrier 共同失锁”正文证据；不得把独立 loop/shared freeze/fixed reacquisition 未检验地写成失效；canonical 判据 3 必须 2019+ task-matched；不进入 Step 3.5/4a/实现/仿真。

## 1. 背景

Q2 候选是 GG fade 与 SCO 下 timing NCO/interpolator、carrier loop 的 update/hold/reacquire 状态机。需核查：是否有正文证据证明 timing/carrier 共同失锁；独立 loops + shared freeze + fixed reacquisition 是否已足够；状态机输出能否成为可量化、可复用的方法形态。

## 2. 执行方式

完整读取 `stages/gw-read.md`、`stages/glossary.md`、`templates.md` literature_notes/实验完备性模板、`domain-comms.md` §1.1/§7。执行 title abort 协议，读 method/experiment/result/conclusion/系统模型与综述 timing/carrier sections。

## 3. 产出格式（强制）

逐篇输出标准 14+ 字段和 receiver-visible information、action、output、时序、baseline、failure condition；给 7 子表（状态/输入、动作、目标/奖励 N/A、建模假设、网络架构 N/A、适配性、M-C-A+四判据）；给通信信道参数与≤20行实验完备性。Paillier 2020 提取写作架构。

本组综合必须分别回答：GG/fade+SCO 下 timing/carrier 共同失锁是否有正文证据；独立 loop+shared freeze+fixed reacquisition 是否被本文解决/比较；可量化状态机输出候选（lock indicator、hold/update/reacquire、恢复时间/cycle slip/BER 等）是否由文献支撑；最强 comparator；供 Step 3.5 的引用链种子/关键词。没有证据要明确写“正文未证实”，不得补推断。所有事实附 `content.md:行号` 或章节/公式。

## 4. 验收

- 两篇身份结果、标准字段、7子表、通信参数、实验完备性齐全。
- Q2 M-C-A 与四判据逐条给证据；判据 3 只接受 2019+ task-matched baseline。
- 不写 Go、METHOD_SIGNAL、新颖性闭合或 Step 4a 结论。
