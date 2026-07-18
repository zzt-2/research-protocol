# PROMPT-012: 参考文献格式修正（GB7714-87）

> 创建: 2026-06-04 | 优先级: P2（中等复杂度）
> 依赖: P-004（参考文献质量升级已完成，citekey 已更新）+ P-001（B10 规则已预装）
> 对应批注: #54 — "格式不符合学校规范"

## 目标

将 `毕设/写作材料/references.bib` 中全部 142 条 bib 条目修正为 GB7714-87 格式，同时检查 `毕设/开题报告/kaiti-report.md` 正文中的引用标注格式是否规范。

**本 PROMPT 只负责格式修正，不负责内容替换。** 内容质量升级（低 IF 期刊替换为 trans 级）由 P-004 完成。

## 背景

### 导师原话

批注 #54："格式不符合学校规范"

### 现状

- bib 文件：`毕设/写作材料/references.bib`（1371 行，142 条记录）
  - @article: 111 条 / @inproceedings: 22 条 / @mastersthesis: 5 条 / @book: 3 条 / @phdthesis: 1 条
- 正文：`毕设/开题报告/kaiti-report.md`，使用 Pandoc `@citekey` 格式引用
- P-004 已完成：低 IF 期刊引文已替换为 trans 级，citekey 已更新，新增条目已写入 bib
- P-001 B10 规则已预装到 `毕设/写作质量规范.md` §14

### GB7714-87 格式要求

各类型条目的必填字段：

| 条目类型 | 必填字段 |
|---------|---------|
| @article | author / title / journal（全称，不缩写）/ volume / number / pages / year / doi（如有）|
| @inproceedings | author / title / booktitle / pages / year / doi（如有）|
| @phdthesis / @mastersthesis | author / title / school / year |
| @book | author / title / publisher / year |

**作者格式**：英文 `姓, 名.` （如 `Khalighi, Murat Uysal`），中文保留原样但加 `language = {chinese}`

**期刊名**：必须使用全称，不得缩写（如 `IEEE Communications Surveys & Tutorials` 不能写成 `IEEE Commun. Surv. Tutorials`）

## 必读文件（按优先级）

1. **`毕设/写作材料/references.bib`** — 全部 142 条 bib 条目，逐条检查格式
2. **`毕设/写作质量规范.md` §14（B10）** — GB7714-87 规则定义，字段完整性和格式标准
3. **`毕设/开题报告/kaiti-report.md`** — 正文，检查引用标注格式（`@citekey` 位置是否在句末句号前等）
4. **P-004 替换清单**（如果 P-004 已产出）— 确认哪些条目是新增的，新增条目需重点检查格式
5. **`.sessions/2026-06-04-advisor-review-revision/PROMPT-004-reference-quality-upgrade.md`** — 了解 P-004 对 bib 的改动范围

## 工作步骤

### Step 1：读取 P-004 产出，确认当前 bib 状态 [检查点：确认基线]

1. 读取 `references.bib` 当前版本，确认 P-004 的改动已生效
2. 如果 P-004 产出了替换清单，记录哪些条目是新增的
3. 确认正文中 citekey 映射已更新完毕（无悬空引用）

**检查点**：bib 文件基线确认，新旧条目已区分。

### Step 2：逐条审查 bib 条目格式 [检查点：问题清单完成]

对全部 142 条 bib 条目逐条检查以下维度：

**字段完整性**（缺字段即标记）：
- [ ] author 字段存在且格式正确
- [ ] title 字段存在
- [ ] journal / booktitle / school / publisher 字段存在（按类型）
- [ ] volume / number / pages / year 字段存在（@article 必须有）
- [ ] doi 字段存在（如有 DOI）

**格式规范性**（不符合即标记）：
- [ ] 期刊名是否全称（非缩写）
- [ ] 英文作者格式是否为 `姓, 名.` 形式
- [ ] pages 格式是否为 `起始--结束`（双短横线）
- [ ] volume / number 是否为数字
- [ ] year 是否为 4 位数字

产出问题清单（Markdown 表格）：

| # | citekey | 类型 | 问题描述 | 修正动作 |

**检查点**：142 条全部审查完毕，问题清单无遗漏。

### Step 3：修正 bib 条目 [检查点：修正完成]

按问题清单逐条修正：

1. **补缺失字段**：从论文原文或 DOI 查询补充缺失的 volume / number / pages / doi
2. **期刊名展开**：将缩写期刊名改为全称（如 `IEEE Commun. Surv. Tutorials` → `IEEE Communications Surveys \& Tutorials`）
3. **作者格式统一**：英文作者统一为 `姓, 名.` 格式
4. **pages 格式统一**：确保使用 `--` 分隔起止页
5. **其他格式问题**：按清单逐项修正

对于缺失 doi 的条目：
- 已有 DOI → 补上
- 无法确认 DOI → 不强制补，跳过

**注意**：缺失 volume/number/pages 的 @article 条目是严重问题（会导致生成参考文献列表不完整），必须通过 DOI 查询或检索补全。

**检查点**：问题清单中所有条目已修正，无遗漏。

### Step 4：检查正文引用标注格式 [检查点：标注格式合规]

检查 `kaiti-report.md` 中的引用标注：

1. **引用位置**：`[@citekey]` 应在句末句号前，不在句号后
2. **多引用格式**：多个引用用分号分隔 `[@key1; @key2]`
3. **无悬空引用**：正文中每个 `@key` 都能在 bib 中找到对应条目
4. **无未引用条目**：bib 中每个 citekey 都在正文中被引用（Pandoc 默认只输出引用过的条目，此步确认即可）

**检查点**：正文引用标注全部合规。

### Step 5：验证 [检查点：验证通过]

1. 对修正后的 bib 文件重新运行 Step 2 的检查清单，确认 0 问题
2. 抽查 5 条修正前有问题的条目，确认修正正确
3. 确认正文中无悬空引用

**检查点**：二次审查 0 问题，抽查全部通过。

## 约束

1. **不改 citekey** — citekey 已在 P-004 中确定，格式修正不动 citekey
2. **不改引用内容** — 只修正格式字段（author/title/journal/volume/number/pages/year/doi），不替换论文
3. **不删条目** — 不删除任何 bib 条目，只修正格式
4. **不加新条目** — 新增论文是 P-004 的职责，本 PROMPT 不新增
5. **缺失信息优先从已有数据补** — 先检查 bib 条目中是否已有但格式不对，再考虑从外部补
6. **DOI 查询在子 agent 中执行** — 如需 web 查询补充缺失信息，必须在子 agent 中完成

## 质量检查

### 格式合规性

- [ ] 全部 142 条 bib 条目字段完整（按类型要求）
- [ ] 期刊名全部使用全称，无缩写
- [ ] 英文作者格式统一为 `姓, 名.`
- [ ] pages 统一使用 `--` 分隔
- [ ] 全部 @article 条目有 volume / number / pages / year
- [ ] 全部 @inproceedings 条目有 booktitle / year
- [ ] 全部学位论文条目有 school / year

### 正文引用标注

- [ ] 引用标注在句末句号前
- [ ] 多引用格式统一（分号分隔）
- [ ] 无悬空 citekey
- [ ] 无多余 bib 条目（正文中未引用的）

### 全局

- [ ] 修正条目数 + 无问题条目数 = 142（总数对得上）
- [ ] 未修改任何 citekey
- [ ] 未新增或删除任何条目
- [ ] P-004 的新增条目格式同样已审查

## 产出

### 必须产出

1. **修正后的 bib 文件** — `毕设/写作材料/references.bib`（格式修正后）
2. **格式修正清单** — Markdown 表格（citekey | 修正前问题 | 修正动作 | 修正后状态），仅列出有问题的条目
3. **正文引用标注检查结果** — 如有标注格式问题，列出修正位置和动作

### 更新 S001

- 在 S001 的对话映射表中标记 P-012（#54 格式）已完成
- 更新 topic-index.md 的进展线索
