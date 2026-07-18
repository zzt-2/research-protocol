# CONCLUSIONS.md 完整性验证计划

> 创建: 2026-06-02 | 状态: 待执行
> 目的: 验证 CONCLUSIONS.md 是否覆盖了所有已确认结论，无遗漏

## 背景

CONCLUSIONS.md 是从以下来源人工整合的：
- SPEC.md §6（15 条高置信结论 + 证伪清单）
- verification-report.md（15 条确认结论 + 调查结果 + NMSE/Nw/DPLL 数据）
- supplementary-experiments.md（今天的 2 个实验 + 3 个验证 agent 修正）
- 6 个 investigation 文件
- S004 语言审查（71 处修改）

人工整合可能有遗漏。需要逐文件核对。

## 验证方法

### Step 1: 源文件逐文件扫描（6 个并行 agent）

每个 agent 负责一个源文件，提取**所有**事实性声称（数字、结论、排名），然后与 CONCLUSIONS.md 逐条对照。

| Agent | 源文件 | 职责 |
|-------|--------|------|
| A | SPEC.md §6 | 提取所有结论 + 数字，对照 CONCLUSIONS.md 每条是否有对应条目 |
| B | verification-report.md | 同上 |
| C | 6 个 investigation-*.md | 合并提取所有结论性陈述 |
| D | supplementary-experiments.md | 同上 |
| E | phase2-results/ 下 6 个 R-*.md | 提取所有带数字的结论 |
| F | thesis-status.md + section-outline.md + design-decisions.md | 提取嵌入在结构文档中的事实声称 |

### Step 2: 交叉验证（1 个 agent）

收集 6 个 agent 的输出，做并集：
- 在源文件中出现但 CONCLUSIONS.md 中没有的结论 → 标记为"遗漏"
- CONCLUSIONS.md 中的数字与源文件不匹配 → 标记为"不一致"
- CONCLUSIONS.md 中的边界条件不够完整 → 标记为"需补充"

### Step 3: 数字审计（1 个 agent）

用确定性 grep 对 CONCLUSIONS.md 中的所有数字做反向检查：
- grep 每个数字在源文件中是否存在
- 如果数字只出现在 CONCLUSIONS.md 中（无源文件支撑），标记为"无源"

## 输出格式

```
## 遗漏结论
- [源文件:行号] 结论内容 → 建议归入 C3-XX 或 C4-XX

## 数字不一致
- CONCLUSIONS.md 写 X，源文件写 Y → 建议值

## 边界条件需补充
- C4-XX 缺少 Z 限定 → 建议补充

## 验证通过
- 共 N 条结论，M 条验证通过，K 条需修正
```

## 注意事项

- CONCLUSIONS.md 是权威文件，源文件如果与它矛盾，以 CONCLUSIONS.md 为准（因为 CONCLUSIONS.md 已经过独立验证修正）
- 但如果源文件有 CONCLUSIONS.md 未收录的结论，必须报告
- 特别注意 VV 相关的数字：很多源文件中的 VV 数字是基于旧 bug 公式（SPEC §6.4），已经在 CONCLUSIONS.md 中修正
