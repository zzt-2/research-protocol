# Task Brief: Step 3.5 joint-estimator method priors 全文核验

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-3-5-method-prior-read.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取 T005 worker log、项目框架与工具

## 0. TL;DR（执行方先读）

对 Round 1 两篇 must-read 方法先例做有界 acquire→read：`10.1109/JLT.2020.3042546` 与
`10.1007/s11082-024-06850-5`。核验 true joint `(τ,CFO[,phase])` 的信息/目标/输出，以及为什么它们
不自动碰撞 Q1 的 `(frame,τ,CFO)`、RRC single-carrier coherent FSO task。

最高纪律：合法 acquisition；每篇最多三条适用路径；摘要不能代替全文；不改 canonical；不进入
Step 4a/实现/仿真；不提交。

## 1. 背景

T005 摘要筛查称 JLT 2021 为 CO-OFDM joint ML TO/CFO/CPO、Springer 2024 为 CO-OFDM neural joint
timing/frequency；两者都未显示 frame output，且 waveform/task 可能不匹配。

## 2. 任务详情

先读 `gw-acquire.md`/`gw-read.md`；逐篇 dry-run→有界获取→title/SHA/≥50行→全文 action contract。
产出必须含 acquisition receipt、information/action/output、objective/search、frame 是否输出、waveform/task
fit、Q1 collision/delta、证据行、read-note/read-log 路径和 blocker。

## 3. 已知陷阱

真正 joint `(τ,CFO)` 仍不等于 joint `(frame,τ,CFO)`；OFDM cyclic prefix/subcarrier structure 不能直接
当 RRC single-carrier baseline。

## 4. 验收

- [ ] 两篇各有 bounded receipt。
- [ ] 仅全文支持 positive exact-action verdict。
- [ ] 成功全文有 title/SHA/行数/read note/read-log。
- [ ] 无 canonical/代码/实验改动。
