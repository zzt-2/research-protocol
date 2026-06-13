# C4: 文档架构方案设计

> 2026-06-12 | 方案设计 | 执行者: C4 agent
> 基于: S002 Batch 1 (A3/A4/A5) + Batch 2 (B2) 审计结论

## 设计目标

解决文档膨胀问题（7文件5096行公式、108文件23653行专题、9个状态错误），建立长期可持续的文档体系。核心约束：**不消耗心力，跟随工作流自然更新，纯文件系统+git方案**。

---

## 1. 三层分档 — 具体文件列表

### 1.1 锚点层（仅通过 D### 决策变更，绝不追加，500 行硬限制）

锚点层文件是系统的不变量定义。变更必须通过显式决策，不能在写作过程中随手改。

| 文件 | 当前行数 | 最大行数 | 内容定义 |
|------|---------|---------|---------|
| `毕设/CONCLUSIONS.md` | 433 | 500 | 论文结论唯一真相源。安全等级+代码来源+精确数字+边界条件 |
| `毕设/TERMS.md` | 425 | 500 | 符号约定唯一真相源。所有符号定义、单位、消歧 |
| `毕设/symbol-conventions.md` | 264 | 300 | 符号使用规范（与TERMS.md互补：TERMS定义值，conventions定义用法） |
| `毕设/thesis-framework.md` | 175 | 300 | 论文章节框架+目录结构+贡献声称 |
| `毕设/innovation-points.md` | 167 | 300 | 创新点定义（方向级，不绑定方法） |

**锚点层总计**: 5 文件 / ~1464 行（当前）/ 1900 行（上限）

### 1.2 积累层（只追加，超限归档最旧条目，1000 行软限制）

积累层文件记录历史过程，只能增长不能删改。超限时将最旧条目移入对应专题的 archive。

| 文件 | 当前行数 | 软限制 | 归档策略 |
|------|---------|--------|---------|
| `毕设/formulas-master.md` | 2260 | 2500 | 旧方向公式（如F3.4-F3.17归档标记）移入 `_archive/formulas-archived.md` |
| `毕设/design-decisions.md` | 612 | 800 | 超过6个月的已关闭决策移入专题 archive |
| `毕设/master-state.md` | 236 | 500 | 阶段完成后压缩为摘要行 |
| `毕设/thesis-status.md` | 297 | 500 | 同上 |
| `毕设/文献综述.md` | 87 | 500 | 文献笔记积累 |
| `毕设/写作质量规范.md` | 731 | 1000 | 规范条目积累，旧条目标记但不删除 |

**积累层总计**: 6 文件 / ~4223 行（当前）

### 1.3 快照层（刷新式重写，300 行硬限制）

快照层文件是当前状态的投影，每次更新都是整体重写。旧版本由 git 管理。

| 文件 | 当前行数 | 最大行数 | 刷新时机 |
|------|---------|---------|---------|
| `毕设/formulas-index.md` | 299 | 300 | formulas-master.md 变更后刷新 |
| `毕设/thesis-preparation-checklist.md` | — | 300 | 每阶段开始时重写 |
| `.sessions/{topic}/topic-index.md` | varies | 400 | 每次会话结束时刷新 |

**快照层总计**: 3 类文件

### 1.4 写作材料目录分类

`毕设/写作材料/` 下的文件按性质分类：

**积累层**（写作素材，只追加）：

| 文件 | 行数 | 说明 |
|------|------|------|
| `formulas-ch3ch4-sync.md` | 945 | 迁移独有公式后归档（见去冗余计划） |
| `formulas-ch4-kf.md` | 219 | 迁移独有公式后归档 |
| `formulas-ch5-fpga.md` | 340 | 重命名为 fpga-reference.md |
| `references.bib` | ~1300 | 参考文献库，自然增长 |
| `literature-notes-ch1-ch2.md` | ~1200 | 文献笔记 |
| `material-chapter-literature.md` | ~1400 | 章节文献材料 |
| `writing-patterns-*.md` (5文件) | ~10000 | 写作模式参考（范文提取，完成即冻结） |
| `writing-phrases.md` | ~1400 | 写作用语库 |

**快照层**（每次写作时刷新）：

| 文件 | 行数 | 说明 |
|------|------|------|
| `section-outline.md` | ~1300 | 各节写作大纲，写完一章刷新下一章 |
| `figure-table-plan.md` | ~600 | 图表规划，随章节刷新 |
| `subsection-content-outline.md` | ~650 | 小节内容大纲 |

**归档目标**（100% 冗余，直接归档）：

| 文件 | 行数 | 原因 |
|------|------|------|
| `formulas-ch2-system-model.md` | 704 | 与 master Ch2 100% 重叠 |
| `formulas-ch3-link-performance.md` | 329 | 与 master Ch3 100% 重叠 |

### 1.5 .sessions/ 专题文件分类

每个专题内的文件按三层分档：

| 层级 | 文件类型 | 更新策略 |
|------|---------|---------|
| 锚点 | `topic-index.md` | 每次会话结束时刷新（快照式，非追加） |
| 锚点 | `decisions.md` | 仅通过 D### 变更，不追加旧决策 |
| 锚点 | `verifications.md` | 仅通过 V### 变更 |
| 积累 | `S###-*.md` | 只追加，新会话新建编号 |
| 积累 | `R###-*.md` | 只追加 |
| 积累 | `H###-*.md` | 只追加 |
| 快照 | `PROMPT-*.md` | 每次使用时生成/重写，用完不维护 |

---

## 2. 成熟度标签方案

### 2.1 当前文件标签

#### 毕设/ 根目录

| 文件 | 标签 | 依据 |
|------|------|------|
| CONCLUSIONS.md | **ACTIVE** | 论文写作唯一真相源，持续更新 |
| TERMS.md | **ACTIVE** | 符号约定，持续更新 |
| symbol-conventions.md | **ACTIVE** | 符号使用规范 |
| thesis-framework.md | **ACTIVE** | 论文框架，随写作更新 |
| innovation-points.md | **ACTIVE** | 创新点定义 |
| formulas-master.md | **ACTIVE** | 公式主库 |
| formulas-index.md | **ACTIVE** | 公式索引（快照） |
| design-decisions.md | **ACTIVE** | 设计决策记录 |
| master-state.md | **ACTIVE** | Master 编排状态 |
| thesis-status.md | **ACTIVE** | 论文状态 |
| 文献综述.md | **ACTIVE** | 文献综述 |
| 写作质量规范.md | **ACTIVE** | 写作规范 |
| thesis-preparation-checklist.md | **FROZEN** | 准备检查清单，阶段完成后冻结 |

#### 毕设/写作材料/

| 文件 | 标签 | 依据 |
|------|------|------|
| formulas-ch2-system-model.md | **ARCHIVED** | 100% 冗余 |
| formulas-ch3-link-performance.md | **ARCHIVED** | 100% 冗余 |
| formulas-ch3ch4-sync.md | **DRAFT→ACTIVE** | 迁移独有公式后归档 |
| formulas-ch4-kf.md | **DRAFT→ACTIVE** | 迁移独有公式后归档 |
| formulas-ch5-fpga.md | **ACTIVE** | 互补内容，重命名 |
| section-outline.md | **ACTIVE** | 写作大纲 |
| writing-patterns-*.md | **FROZEN** | 范文提取完成，不再修改 |
| references.bib | **ACTIVE** | 持续更新 |

#### .sessions/ 专题

| 专题 | 标签 | 依据 |
|------|------|------|
| 2026-06-12-simulation-foundation-rebuild | **ACTIVE** | 当前活跃 |
| 2026-06-10-research-direction-exploration | **ACTIVE** | 当前活跃 |
| thesis-direction-pivot | **FROZEN** | 开题完成，不再更新 |
| thesis-simulation-consolidation | **FROZEN** | 仿真合并完成 |
| thesis-sim-exploration | **FROZEN** | 探索方法论已建立 |
| 2026-06-04-advisor-review-revision | **FROZEN** | 批注修订完成 |
| 2026-05-31-thesis-writing-prep | **FROZEN** | 写作准备完成 |
| 2026-05-31-thesis-writing | **FROZEN** | 写作完成 |
| 2026-05-30-ch3-direction-exploration | **FROZEN** | 方向已确定 |
| 2026-06-04-citation-verification | **FROZEN** | 引用验证完成 |
| thesis-final-review | **ARCHIVED** | 方向已废弃 |
| _archive/* (11目录) | **ARCHIVED** | 已归档的旧方向 |

### 2.2 标签变更触发条件

| 变更方向 | 触发条件 | 执行者 |
|---------|---------|--------|
| DRAFT → ACTIVE | 内容经 V### 验证通过 | 工作会话 |
| ACTIVE → FROZEN | 对应阶段/任务完成，不再需要修改 | 阶段收尾会话 |
| FROZEN → ACTIVE | 需要回访（如论文修改需重验结论） | 显式决策 D### |
| 任何 → ARCHIVED | 内容100%冗余或方向完全废弃 | ROT审计或去冗余操作 |

### 2.3 标签在文件中的表示

**方案：YAML front matter**。在每个文件头部加一行标记：

```markdown
<!-- maturity: ACTIVE -->
```

选择 HTML 注释形式而非 YAML front matter，原因：
- Markdown 渲染不受影响
- grep 可直接搜索 `maturity:` 标签
- 不需要修改现有文件的格式结构
- 对写作工具（pandoc等）无影响

**.sessions/ 专题的成熟度标签**：放在 `_registry.yaml` 中，不放在每个文件中。在注册表条目中加一个 `maturity` 字段：

```yaml
- slug: thesis-direction-pivot
  maturity: FROZEN
  status: dormant
  ...
```

---

## 3. 去冗余执行计划

### 3.1 公式文档去冗余（基于 A5 审计）

**当前状态**: 7 文件 / 5096 行
**目标状态**: 3 文件 / ~3350 行（减少 ~1750 行、4 个文件）

#### 步骤 1: 迁移独有公式到 master

1. 从 `formulas-ch3ch4-sync.md` 提取 32 条独有公式（F4.15-F4.46：FFT/VVPE/BPS/DPLL 补充推导）
2. 追加到 `formulas-master.md` 的 Ch4 部分，保持编号连续
3. 从 `formulas-ch4-kf.md` 提取 13 条独有公式（F4.K1-F4.K13：KF 完整推导链）
4. 追加到 `formulas-master.md` 的 Ch4 部分

#### 步骤 2: 归档冗余文件

5. 将 `formulas-ch2-system-model.md` (704行) 移入 `毕设/写作材料/archive/`
6. 将 `formulas-ch3-link-performance.md` (329行) 移入 `毕设/写作材料/archive/`
7. 将迁移完成后的 `formulas-ch3ch4-sync.md` 移入 `毕设/写作材料/archive/`
8. 将迁移完成后的 `formulas-ch4-kf.md` 移入 `毕设/写作材料/archive/`

#### 步骤 3: 重命名和更新

9. 将 `formulas-ch5-fpga.md` 重命名为 `fpga-reference.md`（它不是公式文件，是架构/资源/验证参考）
10. 刷新 `formulas-index.md` 以反映合并后的完整公式列表
11. 更新 `formulas-master.md` 头部的质量检查清单和公式总计

**预计时间**: 20-30 分钟（机械操作，无判断负担）

### 3.2 附录 G 重写（基于 A3 审计）

CONCLUSIONS.md 中的"附录 G"（如果存在独立文件或段落）需要以下修正：

| 修正项 | 内容 |
|--------|------|
| 升级 6 条结论 | C4-01/06/11/C3-01/C4-07/C4-12 从旧分级升级到当前安全等级 |
| 修正 3 处编号 | C3-04/C4-07/C4-12~14 的描述与实际内容对齐 |
| 补充 3 条遗漏 | C4-13(VV/BPS不兼容16-QAM)、C4-14(16-QAM强湍流BER平台)、C4-15(阻尼系数无显著影响) |
| 处理 P-06 | 从待重验表移出（已重验，应升级为主结论或标注"已验证"） |
| 确认 P-09 | 核实措辞修正状态 |

**执行方式**: 在 CONCLUSIONS.md 中直接编辑附录 G 段落。P-06/P-09 状态修正需要查证相关实验数据后执行。

**预计时间**: 15 分钟

### 3.3 专题注册表清理（基于 A4 审计）

#### P0 级（5 分钟，立即执行）

```yaml
# 9 个已归档专题状态修正
framework-evolution: active → closed
direction-scouting: active → closed
thesis-structure-research: active → closed
chapter-quality-audit: active → closed
thesis-chapter-fixes: active → closed
2026-05-13-mega-constellation-gnn-routing: dormant → closed
2026-05-13-hgat-satellite-dag-offloading: dormant → closed
2026-05-13-ris-phase-drl: dormant → closed
2026-05-17-leo-congestion-routing: dormant → closed

# 修复 thesis-chapter-fixes 的重复 YAML 键
# （当前有两个 depends_on，第二个覆盖第一个，需合并为数组）
```

#### P1 级（15 分钟，当天执行）

```yaml
# 5 个专题标 dormant
thesis-direction-pivot: active → dormant
thesis-sim-exploration: active → dormant
thesis-simulation-consolidation: active → dormant
2026-05-30-ch3-direction-exploration: active → dormant
2026-06-04-advisor-review-revision: active → dormant

# 1 个目录归档
# thesis-final-review 目录移入 _archive/（注册表已标 closed，目录仍在活跃位置）

# 3 个未注册目录补注册
# - 2026-05-31-thesis-writing-prep
# - 2026-05-31-thesis-writing
# - 2026-06-04-citation-verification
```

#### 为每个注册条目加 maturity 字段

在 P0/P1 修正同时，为所有条目添加 `maturity` 字段：

```yaml
- slug: 2026-06-12-simulation-foundation-rebuild
  maturity: ACTIVE
  status: active
  ...

- slug: thesis-direction-pivot
  maturity: FROZEN
  status: dormant
  ...

- slug: _archive/2026-05-13-hgat-satellite-dag-offloading
  maturity: ARCHIVED
  status: closed
  ...
```

---

## 4. 文件大小监控方案

### 4.1 监控机制

**方案：CLAUDE.md 规则 + 会话启动时自动检查**

不引入外部脚本。在 CLAUDE.md 的文档职责表中增加行数限制列，作为会话启动时的读取约束。

**锚点层和快照层**有硬限制（500/300行），写入时超限则必须修剪（移出内容到积累层或归档）。
**积累层**有软限制（1000行），超限时在 topic-index.md 的未决项中标记。

### 4.2 超限处理流程

```
文件写入时超限
  ↓
判断层级
  ├─ 锚点层(硬限制): 必须修剪才能继续写入
  │   → 将详细背景移入积累层对应文件
  │   → 锚点层只保留决策结论和参数值
  ├─ 快照层(硬限制): 必须压缩才能刷新
  │   → 减少详细描述，只保留当前状态投影
  └─ 积累层(软限制): 标记但允许继续
      → 在 topic-index.md 未决项中记录
      → 下次 ROT 审计时处理
```

### 4.3 与 .sessions/ 专题管理的集成

- 每个 `topic-index.md` 的"未决项"段落增加一个文件大小健康状态字段
- 格式：`文档健康: OK` 或 `文档健康: formulas-master.md 超软限制(2260/2500)`
- 只有当文档健康非 OK 时才需要关注

### 4.4 具体限制表（写入 CLAUDE.md）

在 CLAUDE.md 文档职责表附近增加一个引用：

```markdown
## 文档大小限制

| 文件 | 层级 | 当前 | 限制 | 说明 |
|------|------|------|------|------|
| 毕设/CONCLUSIONS.md | 锚点 | 433 | 500 | 结论唯一真相源 |
| 毕设/TERMS.md | 锚点 | 425 | 500 | 符号唯一真相源 |
| 毕设/formulas-master.md | 积累 | 2260 | 2500 | 公式主库 |
| 毕设/formulas-index.md | 快照 | 299 | 300 | 公式索引 |
| 毕设/design-decisions.md | 积累 | 612 | 800 | 设计决策 |
| ... | ... | ... | ... | ... |
```

---

## 5. ROT 审计方案

### 5.1 审计频率和触发条件

**频率**: 每 10 个会话执行一次（约每 2 周）。

**触发条件**（满足任一即提前执行）：
- 文件总量增长超过 20%（相比上次审计）
- 新增 .sessions/ 专题超过 3 个
- 任何文件超过其层级限制
- 跨对话恢复时发现信息矛盾

### 5.2 审计检查项清单

分三个级别，总时间约 15-20 分钟：

#### Level 1: 注册表一致性（5 分钟）

- [ ] `_registry.yaml` 中每个条目的 status 是否匹配磁盘状态
- [ ] 磁盘目录是否全部注册
- [ ] `maturity` 字段是否与实际使用状态一致
- [ ] depends_on / conflicts_with 是否仍然有效

#### Level 2: 文件冗余检测（10 分钟）

- [ ] 锚点层文件是否超过硬限制
- [ ] 积累层文件是否超过软限制
- [ ] 快照层文件是否仍反映当前状态
- [ ] 是否有同一信息在 2+ 文件中定义（grep 交叉检查）
- [ ] 公式文档是否有新增冗余（master 与子文件对比）

#### Level 3: 内容质量（5 分钟，仅对关注文件）

- [ ] CONCLUSIONS.md 安全等级是否与代码验证状态一致
- [ ] 附录 G 是否需要更新
- [ ] 待重验条目是否已处理
- [ ] FORMULAS.md 来源标注是否完整

### 5.3 审计结果记录方式

在当前活跃专题的 session note 中记录。格式：

```markdown
### ROT 审计 YYYY-MM-DD

**L1 注册表**: [X 个问题 / 无问题]
- [具体问题列表]

**L2 文件冗余**: [X 个问题 / 无问题]
- [具体问题列表]

**L3 内容质量**: [X 个问题 / 无问题]
- [具体问题列表]

**行动项**: [P0/P1/P2 优先级列表]
```

不单独建审计文件，记录在当次会话的 S### 中。

---

## 6. .sessions/ 专题管理改进

### 6.1 注册表状态清理（执行计划见 3.3 节）

已审计的具体操作已在上方列出。此处补充防漂移机制。

### 6.2 防止未来状态漂移的机制

**根因**: 专题结束时没有"关闭流程"，状态标量被遗忘。

**方案: 阶段收尾检查清单**

在 topic-index.md 模板中增加一个"收尾检查"段落。当专题进入 dormant/closed 时，必须执行：

```markdown
## 收尾检查

- [ ] _registry.yaml 状态已更新（active → dormant/closed）
- [ ] maturity 字段已更新（ACTIVE → FROZEN/ARCHIVED）
- [ ] topic-index.md 状态行已更新
- [ ] 未决项已清空或标记为"移交至: [新专题slug]"
- [ ] 目录已移入 _archive/（仅 closed 状态需要）
```

**触发时机**: 当用户或 agent 声明"这个专题完成了/暂停了"时。

**不增加额外维护负担**: 这 5 个检查项是在做状态变更时顺手完成的，不是额外的维护任务。

### 6.3 thesis-direction-pivot 等大型专题的处理方案

**当前问题**: thesis-direction-pivot 有 98 文件 / 23653 行，其中最大文件 4799 行（范文参考论文）。

**处理方案**:

1. **不压缩、不删除**。历史记录保留，git 管理版本。
2. **标 FROZEN + dormant**。状态更新即可，不需要移动文件。
3. **在 topic-index.md 中记录关键索引**：哪些文件包含有价值的信息（如 H008 文献精读 handoff），哪些是一次性使用的（如 PROMPT-*）。
4. **恢复时只读 topic-index.md 的"已确认结论"段落**，不读整个目录。

**原则**: 大型已冻结专题的恢复成本由"只读 topic-index 的不变量段落"控制，而不是通过删除文件控制。这正是成熟度标签的核心价值——恢复路径只读 ACTIVE 文件，FROZEN/ARCHIVED 文件按需查。

### 6.4 文件命名规范（现有规则加强执行）

现有 CLAUDE.md 已定义 S/R/H/D/V 前缀编号体系。增加：

- **PROMPT-*** 文件不需要注册到 `_registry.yaml`（它们是临时任务文件）
- **material-*** 文件不需要编号（它们是写作素材，不是过程记录）
- 单个专题内 S### 编号超过 25 时，评估是否应拆分为新专题

---

## 7. 迁移步骤（具体可执行）

按优先级排序，每步标注预计时间和依赖关系。

### Phase 0: 注册表清理（P0，5 分钟）

- [ ] 编辑 `_registry.yaml`：9 个已归档专题 active/dormant → closed
- [ ] 修复 thesis-chapter-fixes 的重复 depends_on 键（合并为数组）
- [ ] 为所有条目添加 maturity 字段

### Phase 1: 注册表清理（P1，15 分钟）

- [ ] 5 个专题标 dormant（thesis-direction-pivot, thesis-sim-exploration, thesis-simulation-consolidation, 2026-05-30-ch3-direction-exploration, 2026-06-04-advisor-review-revision）
- [ ] thesis-final-review 目录移入 `_archive/`
- [ ] 3 个未注册目录补注册（2026-05-31-thesis-writing-prep, 2026-05-31-thesis-writing, 2026-06-04-citation-verification）

### Phase 2: 公式文档去冗余（30 分钟）

- [ ] 从 formulas-ch3ch4-sync.md 提取 32 条独有公式，追加到 formulas-master.md Ch4
- [ ] 从 formulas-ch4-kf.md 提取 13 条独有公式，追加到 formulas-master.md Ch4
- [ ] 将 4 个冗余文件移入 `毕设/写作材料/archive/`（ch2, ch3-link, ch3ch4-sync, ch4-kf）
- [ ] 重命名 formulas-ch5-fpga.md → fpga-reference.md
- [ ] 刷新 formulas-index.md
- [ ] 更新 formulas-master.md 头部检查清单

### Phase 3: 附录 G 修正（15 分钟）

- [ ] 升级 6 条结论的安全等级
- [ ] 修正 3 处编号映射错误
- [ ] 补充 C4-13/C4-14/C4-15
- [ ] P-06 从待重验表升级
- [ ] 确认 P-09 状态

### Phase 4: 成熟度标签写入（10 分钟）

- [ ] 为 `毕设/` 根目录 13 个 md 文件头部写入 `<!-- maturity: XXX -->` 标签
- [ ] 为 `毕设/写作材料/` 关键文件写入标签
- [ ] 验证标签与 2.1 节计划一致

### Phase 5: CLAUDE.md 更新（10 分钟）

- [ ] 在 CLAUDE.md 文档职责表附近增加"文档大小限制"表（引用本方案的 4.4 节）
- [ ] 在 CLAUDE.md 增加一行索引：`文档三层分档 | C4-documentation-architecture.md`
- [ ] 在 topic-index.md 模板中增加"收尾检查"段落

### Phase 6: 首次 ROT 审计基线（5 分钟）

- [ ] 记录当前所有文件的行数作为基线
- [ ] 写入 S002 或新建 S### 作为 ROT 审计基线记录

**总预计时间**: ~90 分钟（纯机械操作，无设计判断）

---

## 设计决策记录

| 编号 | 决策 | 理由 | 替代方案（被否决） |
|------|------|------|------------------|
| C4-D1 | 成熟度标签用 HTML 注释 `<!-- maturity: X -->` | 不影响渲染，grep 可搜索，无格式侵入 | YAML front matter（pandoc 兼容性问题） |
| C4-D2 | 大型专题不压缩/删除，靠 maturity 标签控制恢复成本 | 删除不可逆，git 已有历史，恢复成本由读取策略控制 | 压缩为 summary.md（信息损失，违背原则4） |
| C4-D3 | ROT 审计记入当次 S###，不单独建文件 | 减少文件数量，审计是会话的一部分 | 单独 audits/ 目录（增加维护负担） |
| C4-D4 | 文件大小监控靠 CLAUDE.md 规则而非脚本 | 纯文件系统+git 约束，不引入外部工具 | pre-commit hook（过重，与用户"不消耗心力"约束矛盾） |
| C4-D5 | 专题收尾检查清单嵌入 topic-index.md 模板 | 跟随工作流自然触发，不额外维护 | 独立的 checklist 工具（增加复杂度） |

---

## 附录: 当前文件全景

### 毕设/ 根目录（14 文件 / 3427 行）

```
CONCLUSIONS.md          433  锚点  ACTIVE
TERMS.md                425  锚点  ACTIVE
symbol-conventions.md   264  锚点  ACTIVE
thesis-framework.md     175  锚点  ACTIVE
innovation-points.md    167  锚点  ACTIVE
formulas-master.md     2260  积累  ACTIVE
design-decisions.md     612  积累  ACTIVE
master-state.md         236  积累  ACTIVE
thesis-status.md        297  积累  ACTIVE
文献综述.md              87  积累  ACTIVE
写作质量规范.md          731  积累  ACTIVE
formulas-index.md       299  快照  ACTIVE
thesis-preparation-checklist.md  —  快照  FROZEN
CONCLUSIONS-VERIFY-PLAN.md  —  快照  FROZEN
```

### .sessions/ 目录（12 活跃目录 + 11 归档目录 = 23 目录）

```
活跃目录:
2026-06-12-simulation-foundation-rebuild   5f / 2180 行   ACTIVE
2026-06-10-research-direction-exploration   5f /  877 行   ACTIVE
thesis-direction-pivot                     98f / 23653 行  FROZEN → dormant
2026-06-04-advisor-review-revision         37f / 5971 行   FROZEN → dormant
2026-05-31-thesis-writing-prep             36f / 9059 行   FROZEN → dormant
2026-05-31-thesis-writing                  34f / 3591 行   FROZEN → dormant
thesis-simulation-consolidation             5f /  714 行   FROZEN → dormant
thesis-sim-exploration                      1f /  111 行   FROZEN → dormant
2026-05-30-ch3-direction-exploration        7f /  959 行   FROZEN → dormant
thesis-final-review                         29f / 7547 行  ARCHIVED → _archive/
thesis-chapter-fixes                        —   (仅注册表条目, 无目录)  ARCHIVED
chapter-quality-audit                       —   (仅注册表条目, 无目录)  ARCHIVED
2026-06-04-citation-verification            4f /  452 行   FROZEN (未注册, 需补注册)

归档目录 (_archive/):
11 个已归档的旧方向目录, 共 169 文件 / 17226 行  ARCHIVED
```
