# Task Brief: 历史候选与关闭链全量普查

> 来源: S021 | 产出位置: 仅回传主线程，不写文件
> 日期: 2026-08-13
> 唯一文档: 本任务书 + 仓库只读文件/可读 git 历史

## 0. TL;DR（执行方先读）

只读扫描 thesis-fso 的历史候选、方向包、session、D/V/H 与可读 git 历史，恢复所有具有真实 input—action—output 链的已有资产。不要沿用旧 Go/Kill 标签；按“最窄但真实的学位论文命题”重判。禁止实验、联网、论文检索、Groundwork 补全、新候选创造和任何文件修改。

## 1. 背景

主线程已冻结 D031：学位论文目标至少两个可命名方法；正确经典 baseline + 目标场景真实增益 + receiver-visible 动作链即可。已知廉价/更强替代不自动 Kill，也不强制进入正文，只限制不能声称的内容。真实性红线只有伪造/artifact、truth leakage、故意错误 baseline、明知为假的事实命题。

P11 当前只是 authority 阻断且未运行 corrected 实验，不得写成科学失败、CMA 吸收或实验无效，也不得补 P11 Groundwork。

## 2. 任务详情

1. 扫描 `projects/thesis-fso/direction-lab/`、相关 `.sessions/`、`decision_log.md`、`master-state.md`、历史 harvest/inventory/atlas/package 文件及必要 git 历史。
2. 不限旧编号，尽可能列全曾被提出、实现、局部验证、降级或关闭的动作链；重点找因 novelty、强邻居、full-general、独立性不足、证据闭包过重而降级者。
3. 每项返回：资产名/旧编号；证据路径；真实输入—动作—输出；已有 baseline 与结果；最窄可写命题；已知真实性红线；在 D031 下的身份（独立方法候选/可组合工程方法/支撑组件/真实性无效）。
4. 不把“未补 authority、未跑全网格、未比较强邻居”写成科学失败。

## 3. 已知陷阱

- 不复活明确 truth leakage、scale/metric/cost artifact、伪造或错误实现结果。
- 不因旧 `KILL`/`SUPPORTING_ONLY` 标签直接拒绝；必须读实际动作与原因。
- 不创造仓库里没有的组合、新场景或新算法。
- 时间上限 15 分钟；优先 breadth-first 全量清单，再对高潜项补证据。

## 4. 验收与回传格式

回传一份紧凑 Markdown：扫描范围与遗漏风险；资产总表；Top 10 高潜项；明确无效项；“过去为何漏掉”的分类统计。每个高潜项至少一个真实路径证据。不要给实验建议。
