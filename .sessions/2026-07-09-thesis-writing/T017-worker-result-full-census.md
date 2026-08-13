# Task Brief: Worker 与结果资产全量普查

> 来源: S021 | 产出位置: 仅回传主线程，不写文件
> 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读文件/可读 git 历史

## 0. TL;DR（执行方先读）

只读扫描 thesis-fso 的 worker-logs、results、verify、simulator 输出和历史实验记录，找出已经有真实数字或可审计比较、但从未被提升为学位论文方法的资产。禁止运行任何脚本/实验、联网、补 Groundwork、创造新候选或修改文件。

## 1. 背景

D031 采用毕业优先有限主张：方法可只对正确经典 baseline 和限定场景成立；已知廉价或更强替代不自动 Kill，也不强制写入正文。真实性红线是数字/artifact、truth leakage、故意错误 baseline 和明知虚假命题。

P11 corrected confirmation 没有运行；两个重复执行对话都因缺 candidate-specific Groundwork/Q# authority 在实验前停止。历史 20 dB 资产可以按其真实范围盘点，但不得把当前停止误写成实验结论。

## 2. 任务详情

1. 扫描 `projects/thesis-fso/worker-logs/`、`results/`、`verify/`、`simulator/`、direction-lab artifacts、历史结果 JSON/CSV/MD 和必要 git 历史。
2. 找出具备以下任一信息的资产：性能改善、复杂度/调用量降低、样本/导频节省、鲁棒性恢复、bit-exact/定点误差、时延/吞吐、边界范围、可复用控制或估计动作。
3. 每项返回：路径；数字及真实条件；baseline；receiver-visible 动作；能够诚实写出的最窄命题；是否存在致命真实性问题；D031 身份。
4. 区分“数字真实但范围窄”“标签/条件错误需缩窄”“结果 artifact 不能用”“只验证 consistency 没有 method delta”。

## 3. 已知陷阱

- 不运行任何验证命令或脚本，只读已有产物。
- 旧 SNR 标签与实际注入、held-out/dev、truth-assisted preprocessing 等必须按证据纠正。
- 不用 receipt/hash PASS 代替科学正确性。
- 时间上限 15 分钟；先广扫文件名与摘要，再抽查承重原始产物。

## 4. 验收与回传格式

回传紧凑 Markdown：覆盖范围；按证据成熟度排序的资产表；Top 10 可写命题；真实性无效清单；可能与 T016 重复的别名映射。每项给真实路径，禁止提出新实验。
