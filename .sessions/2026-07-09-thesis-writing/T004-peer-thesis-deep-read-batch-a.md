# Task Brief: 本地硕士论文样本池与方法章精读 Batch A

> 来源: S018 | 产出位置: 回传主线程结构化摘要（主线程写 `packaging-recipe-library.md`）
> 日期: 2026-08-03
> 唯一文档: 执行方只需本 brief、本地 `papers/`、旧论文索引与已转换 `content.md`

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。
**你的任务**：先盘点本地真实硕士学位论文，选出 8–12 篇邻近方向样本；随后对其中 3 篇完整读取至少两个核心方法章，提取真实 baseline→method delta。
**产出**：样本池 + 3 篇深读卡，回传主线程；不要修改文件。

**最高纪律**：

1. 每篇先核题名、学校、年份、学位类型与全文路径；无法确认硕士身份不得计入目标样本。
2. 深读必须实际覆盖两个核心方法章，不能只看摘要、目录、创新点；列明章号与读取范围。
3. 只提取事实，不用“创新很大/很小”的主观形容替代 baseline delta。
4. 优先普通高校/同层级、通信/光通信/卫星通信/信号处理/接收机/调制编码；避免全是博士或顶刊扩展。
5. 不使用 WebSearch；若本地不足，只报告缺口和候选检索关键词，不自行联网。单次不超过 15 分钟。

## 1. 样本选择

查找 `papers/**/content.md`、`papers/downloads/**`、旧 thesis survey/index。目标给出 8–12 篇候选，按普通硕士样本优先级排序，并把本批深读 3 篇标为 A1–A3。

## 2. 每篇深读模板（强制）

```markdown
### A#: 题目
- 学校/年份/学位类型：
- 全文路径：
- 深读章节：Ch# 标题（行号或页码范围）；Ch# 标题（范围）
- 技术方法章数量：

| method chapter | claimed method name | baseline | actual delta | delta type | genuinely new algorithm? | formula/flow/pseudocode scale | experiment volume | baseline strength | gain scale | ablation | chapter organization | top-journal shortfall | why master-thesis-valid |
```

`actual delta` 必须落到：阈值/估计器/权重/约束/状态输入/分支结构/模块组合/复杂度/硬件实现之一或明确的其他动作。

## 3. Batch Summary

- 3 篇中各自的最小创新粒度。
- 观察到的 packaging recipe 候选（只列事实模式，不先映射本项目）。
- 哪些候选论文适合后续 Batch B/C，附路径。

## 4. 验收

- [ ] 样本池 8–12 篇，元数据和路径可核。
- [ ] A1–A3 每篇至少两个核心方法章确实读取。
- [ ] 每章都有 baseline→actual delta。
- [ ] 不抄创新点列表充当深读。
- [ ] 不修改文件。
