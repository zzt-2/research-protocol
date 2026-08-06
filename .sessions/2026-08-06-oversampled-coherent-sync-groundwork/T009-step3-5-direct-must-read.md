# Task Brief: Step 3.5 direct must-read 全文核验

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-direct-must-read.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取 T005 worker log、项目框架与工具

## 0. TL;DR（执行方先读）

对 Round 1 两篇最直接 must-read 做有界 acquire→read：`10.1109/JLT.2025.3581618` 与
`10.1109/LPT.2017.2759584`（arXiv `1801.01598`）。裁决其是否单一 objective 同时输出
`(frame index, fractional τ, CFO)`。成功全文写全局 read note/read-log；失败止损。

最高纪律：只用合法 acquisition 通道；每篇最多三条适用路径；摘要不能裁 exact action；不改 canonical；
不进入 Step 4a/实现/仿真；不提交。

## 1. 背景

- JLT 2025 摘要称 training sequence 支持 frame detection、timing recovery、FOE、SOP、IQ-skew，
  可能只是共享资源多功能。
- LPT 2017 题名为 frame/frequency synchronization，摘要称 chirp TS 解 timing offset/CFO；必须确认
  timing 是 frame/coarse delay 还是 sample-level fractional τ，以及是否同一 metric。

## 2. 任务详情

先读 `gw-acquire.md`/`gw-read.md`；逐篇 dry-run→有界获取→title/SHA/≥50行→全文 action contract。
产出必须含 acquisition receipt、information/action/output/timing、公式/metric、jointness、Q1 collision、
证据行、read-note/read-log 路径和 blocker。只写指定 worker log及成功论文 canonical paper/read-note。

## 3. 已知陷阱

`joint frame/frequency` 不包含 fractional τ；同 TS 支持 timing recovery 也可能是独立初始化。

## 4. 验收

- [ ] 两篇各有 bounded receipt。
- [ ] exact-action verdict 只基于全文。
- [ ] 成功全文有 title/SHA/行数/read note/read-log。
- [ ] 无 canonical/代码/实验改动。
