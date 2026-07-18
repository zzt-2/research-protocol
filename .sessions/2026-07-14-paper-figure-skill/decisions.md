# Decisions — 论文插图全局 Skill

## D001: 升级现有 design-paper-figures 而非新建近义技能

> status: active
> date: 2026-07-14
> 取代：无
> 被取代：无
> 依据：用户原话: voice.md 2026-07-14 + 对照: `C:\Users\zzt\.agents\skills\design-paper-figures`

### 决策

在现有 `design-paper-figures` 上增加图型覆盖、语义图元证据、draw.io 编辑合同、交叉线审查和失败截断；主流程保持精简，细节进入 references，并新增确定性 draw.io validator。

### 理由

现有 skill 与用户目标高度重合，重复新建会造成触发冲突和规则漂移。本轮缺口既包含判断规则，也包含可机械验证的 XML 契约，适合以短主流程、按需参考和脚本分层承载。

### 排除的替代方案

- 新建通信架构图专属 skill：与现有 skill 高度重叠，且容易把领域案例误当全局默认。
- 仅写项目 checklist：无法跨项目自动触发，也不能复用 draw.io 验证工具。
- 保存三泳道模板资产：会诱导后续图机械套版，违反语义优先。

### 影响范围

- `C:\Users\zzt\.agents\skills\design-paper-figures\`
- `.sessions/2026-07-14-paper-figure-skill/`
- 不修改论文图文件或 Fig.1/Fig.2 规格。

### 来源

- S001 / 用户确认
