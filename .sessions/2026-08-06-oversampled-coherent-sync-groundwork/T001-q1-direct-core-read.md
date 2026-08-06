# Task Brief: Q1 直接竞品 CORE 全文精读

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-sync-read-a.md`
> 日期: 2026-08-06
> 唯一文档: 执行方只需本任务书、列出的论文全文及其中引用的规范文件

## 0. TL;DR

在证据 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2` 中精读两篇全文：

1. Tang et al. 2022, *Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent Free-Space Optical Communication*，`papers/doi/10.1109_jphot.2022.3161795/content.md`；
2. Sun et al. 2025, *Preamble Design for Joint Frame Synchronization, Frequency Offset Estimation, and Channel Estimation in Upstream Burst-Mode Detection of Coherent PON*，`papers/arxiv/2409.14400/content.md`。

只做事实提取，不做主控终态裁决。用 `apply_patch` 写入指定 worker log。

最高纪律：必须读 `content.md`；先做 title 自检；不得把 abstract 当全文；不得把“frame+CFO”泛称作 sample-level timing/frame/CFO 联合动作；canonical 判据 3 必须是 2019+ task-matched baseline；不进入 Step 3.5/4a/实现/仿真。

## 1. 背景

Q1 候选是 receiver-known preamble 的 ≥2-sps 样本下，frame index、fractional delay 与 CFO 的联合或 coarse-to-fine acquisition。优先核查 JLT 2025 是否实质覆盖 sample-level timing/frame/CFO，以及 STSB/FSTS+独立 timing 是否已是足够强的廉价 comparator。JOCN 2026 缺全文，不在本任务中裁决。

## 2. 执行方式

完整读取 `stages/gw-read.md`、`stages/glossary.md`、`templates.md` 的 literature_notes/实验完备性模板、`domain-comms.md` §1.1/§7。每篇先按 gw-read 步骤 0 核验 metadata/title；mismatch 立即 ABORT 并记录。随后读 method、experiment、result、conclusion 与相关系统模型段落。

## 3. 产出格式（强制）

每篇均包含：身份/title 自检与定位证据；DOI、源路径、发表状态/渠道；核心贡献≥2句；方法与实验设置；receiver-visible information；action；output；时序/处理顺序；baseline（自实现/引用）；failure condition/适用边界；关键结论；与 Q1/Q2 关系；实现数值；开源代码；验证状态。

另逐篇给 7 个结构化子表：状态/输入空间，动作空间，目标/奖励（非学习法写 N/A+原因），建模假设，网络架构（非学习法写 N/A+原因），适配性，问题提取 M/C/A+失效假设定位+方法产出形态+canonical 四判据。通信额外给信道模型参数表。每篇再给≤20行实验完备性：claims/scope、统计、baseline矩阵、消融、信道、配置多样性、复杂度、VVUQ。Sun 2025 额外提取写作架构（章节/图表/实验/叙述/公式/共同引用，不长引原文）。

最后给本组综合：Q1 collision 表（information/action/output/timing/task 五列）；JLT 2025 是否覆盖 sample-level timing/frame/CFO；最强廉价 comparator；剩余 delta 是真正联合动作还是顺序调整；供 Step 3.5 的引用链种子与关键词（只列，不检索）。所有事实须附 `content.md:行号` 或章节/公式。

## 4. 验收

- 两篇均 title PASS/明确 ABORT；七子表与 receiver-visible/action/output/timing/baseline/failure condition 齐全。
- Q1 M-C-A 与四判据逐条给证据；判据 3 只接受 2019+ task-matched baseline。
- 不写 Go、METHOD_SIGNAL、新颖性闭合或 Step 4a 结论。
