# Handoff: 目录优化 + 开题报告准备

> 来源: S018+S020+方向G评估 | 交接目标: 优化v5目录命名和逻辑链，准备开题报告写作
> 文件名: H009-toc-optimization-and-thesis-status.md

## 已完成边界

1. **Ch3 方向确定**：方向 G（GG+相位误差 BER 闭合解）锁定，E/B/C/多孔径全部 No-Go
2. **S002 推导完成**：BER 闭合解 + BER floor + 中断概率 + 设计准则 + 估计误差鲁棒性，全部 MC 验证
3. **H002 文献审查完成**：6 角度评估创新性，核心贡献定位为"联合框架"
4. **R2 文献精读完成**：Ch1+Ch2 覆盖率 73%（92 篇），31 全文 + 36 摘要
5. **文献-bib 同步完成**：165 篇全部有 bib 条目，0 缺失
6. **thesis-status.md 创建**：全局状态看板，包含目录草案、创新点、风险、文献统计
7. **仿真代码**：sim_ch3_ber_closed_form.py、sim_ch3_strengthening.py、sim_direction_a.py、sim_cascade_robustness.py 均完成

## 不要做什么

- **不说"首次"/"提出"**：创新点用描述性措辞。H002 审查明确 BER floor 是 RF 经典结果、Fourier 级数法是小众工具，不可声称新颖
- **不把 Fourier 级数法或 BER floor 作为核心创新**：核心贡献是联合框架（中断概率+相位误差），不是单个公式
- **不重新评估 Ch3 方向**：6 方向已全面评估，G 是最优选，E/B/C 均已 No-Go
- **不自己做 web search**：主对话严禁 WebSearch/webReader，必须用 tools/search 脚本或子 agent
- **不写大量正文**：本对话的产出是目录和开题报告框架，不是论文正文
- **不凭记忆跳读框架文件**：进入新阶段必须重读对应 stages/*.md

## 必读（按优先级）

1. **`毕设/写作材料/thesis-status.md`** — 全局状态看板（新创建，本 handoff 的核心消费文档）
2. **`.sessions/thesis-direction-pivot/S012-thesis-toc-survey.md`** — 目录设计规范（同领域论文命名模式、结构共性、v1-v4 迭代历史）
3. **`.sessions/2026-05-30-ch3-direction-exploration/S002-ber-closed-form-derivation.md`** — Ch3 完整推导（特别是"加强计划"和"H002 多角度文献审查"两节）
4. **`.sessions/thesis-direction-pivot/S020-r2-literature-reading-results.md`** — R2 精读结果（覆盖率、未验证论文、元数据纠正）
5. **`毕设/写作材料/formulas-ch3ch4-sync.md`** — Ch4 三个自适应公式
6. **`毕设/写作材料/formulas-ch2-system-model.md`** — Ch2 符号参数体系

## 接口变更

无代码改动。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 目录命名不规范 | S012 规范 | v5 草案标注"待优化" | 新对话重做目录 |
| 逻辑链不够顺 | 导师+用户评价 | 递进关系写了但未验证 | 目录优化时重新梳理 |
| 11 篇 bib 元数据错误 | 引用准确性 | 已识别未写入 | 开题报告前写入 |
| 4 篇未验证论文 | 文献可靠性 | 需用户确认 | 用户下次在线时 |
| 绪论 §1.2.2 缺文献 | 文献完备性 | 链路性能分析方向待补 | R3 检索时补充 |
| Ch3 新增 10-15 篇文献 | 文献数量 | BER bound 方向 | 开题前补充检索 |

## 下一轮任务

### 任务 1：目录优化（优先级最高）

**目标**：参考 S012 同领域论文规范，重做 v5 目录的命名和逻辑链。

**具体要求**：
- 读 S012 的"标题命名模式汇总"和"章节结构共性"两节
- 章标题不以"研究"结尾，以技术名词结尾（算法/技术/设计与实现）
- 方法章内部结构：引言 → 算法原理 → 仿真验证 → 本章小结
- 章标题 ≤15 字
- 重点解决：Ch2 承载建模+估计是否过重？Ch3 标题是否足够准确？递进链是否自然？
- 产出更新到 `thesis-status.md` 的目录部分，并标注为 v5 定稿

**注意**：这是开题报告的前置依赖，必须先完成。

### 任务 2：开题报告写作准备

**目标**：基于优化后的目录，准备开题报告。

**依赖**：任务 1 完成。

**材料状态**：
- 开题报告模板：`.sessions/thesis-direction-pivot/S004-template-extracted-xiazhaoyu.md`（张岱开题报告风格提取）
- 写作材料：`毕设/写作材料/` 下 formulas、literature-notes 等就绪
- 写作策略：`.sessions/thesis-direction-pivot/S016-writing-strategy.md`

### 任务 3：绪论 §1.2.2 文献补充（可并行）

检索"湍流信道链路性能分析 / BER bound / 中断概率+相位误差"方向 10-15 篇论文。

## 接收方验证

- [ ] 已读取 thesis-status.md 的"当前目录"和"递进关系"两节
- [ ] 已读取 S012 的"标题命名模式汇总"和"章节结构共性"
- [ ] 已确认创新点措辞不含"首次"/"提出"等地位声称
- [ ] 已检查 _registry.yaml 中 thesis-direction-pivot 专题状态
- [ ] 已确认当前范围：目录优化 + 开题报告准备，不含正文写作
