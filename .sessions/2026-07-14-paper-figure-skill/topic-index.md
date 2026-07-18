# Topic Index: 论文插图全局 Skill

> slug: 2026-07-14-paper-figure-skill
> status: closed | created 2026-07-14 | last_updated 2026-07-14

## 专题定位（一句话）

从 Fig.1/Fig.2 参考图调研、反复视觉纠偏和 draw.io 落地中提炼一个可测试、可执行、能约束语义与编辑性的全局论文插图技能。

## 范围边界

### 原始目标

升级全局个人技能 `design-paper-figures`，固化图型覆盖、语义图元证据、renderer 选择、draw.io 边契约、交叉线审查、失败截断和独立验证流程。

### 当前范围

- 使用当前 skill 跑 3 个 RED 基线压力场景并记录失败。
- 更新 `C:\Users\zzt\.agents\skills\design-paper-figures` 的主流程和按需参考。
- 新增确定性 draw.io 验证脚本并在真实 Fig.2 文件上验证。
- 使用相同场景做 GREEN 复测、quick validation 和独立最终审查。
- 保存测试证据与最终验证结论。

### 明确不含

- 不修改 Fig.1 设计或继续论文图视觉迭代。
- 不把 Fig.2 的 DA/NDA 标签、具体配色或三泳道布局固化为万能模板。
- 不复制论文截图或受版权保护的图作为可直接复用素材。
- 不创建与 `design-paper-figures` 触发范围重叠的新 skill。
- 不用 checklist 自审替代 RED/GREEN 压力测试和独立审查。

### 范围变更记录

- 无。

## 已确认结论

### 不变量

1. 论文插图首先是信息架构；任何图元必须有可陈述的技术语义，装饰不能代替信息。
2. 参考调研先验证图型覆盖与可迁移关系，再进入深度分析或绘制。
3. 用户需要手工微调时优先交付真正可编辑的 draw.io；语义边必须绑定 source/target，并接受确定性检查。
4. 技能升级必须走 RED -> GREEN -> REFACTOR，不能把本轮经验直接写成未经测试的规则。
5. 项目专属标签、配色和布局不提升为全局默认。

### 其他结论

- 升级现有 `design-paper-figures`，不新建近义 skill。
- 主技能保持精简；详细调研门与 draw.io 合同放入按需 reference。
- 优先新增 `validate_drawio.py`，不制作容易诱导套模板的图形资产。

## 进展线索

- **S001 / D001**：升级现有全局 skill；三轮 RED/GREEN/REFACTOR 与两次失败复审均已收敛。
- **R001**：RED-1 复现无证据图元；GREEN 行为符合预期；validator 最终扩为 12 项测试并全部通过。
- **V001**：最终独立 verifier、quick_validate、真实 Fig.2 与 7 类额外边界探针全部 PASS。

## 未决项

- 无。

## 当前位置

专题已完成并关闭；下一步回到 thesis-writing 专题继续 Fig.1 粗稿讨论。
