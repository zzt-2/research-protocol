# 大论文文献管理扩展设计（P3/P4/P5）

> 2026-05-10 设计锁定。实现时机等真实需求。
> 前置文档：docs/restructure-plan.md

---

## P3：增量更新

### 需求

大论文调研周期 3-12 个月，期间新论文持续发表。需要定期重检，只获取上次检索之后的新结果。

### 当前能力

- `tools/search --merge` 可合并多轮结果
- `tools/search --year-from 2025` 可过滤年份，但不是增量（每次返回该年份全部结果）
- OpenAlex 支持 `from_publication_date` 参数，但未暴露到 CLI

### 设计方案

#### 工具改动（search_pipeline.py）

新增参数 `--since YYYY-MM-DD`：
- 传递给 OpenAlex 的 `from_publication_date`
- 传递给 S2 的 `publicationDateOrYear.min`
- SerpAPI 的 `as_ylo`（只支持年份，取 since 的年份部分）
- 其他源无原生支持，在后处理中按 `year` 字段过滤

```bash
# 增量检索示例
bash tools/search "LEO satellite handover DRL" --since 2026-04-01 --merge search-archive/2026-05-10/leo-satellite-handover-drl.json
```

#### 流程改动

在 `stages/gw-search.md` 末尾增加"增量检索"段落：

```markdown
### 增量检索（大论文适用）

距上次检索超过 30 天时，可用 --since 参数做增量检索：
1. 从上次搜索结果的 timestamp 字段获取日期
2. 用 --since {上次日期} 只获取新发表的论文
3. 用 --merge 合并到已有搜索结果

增量检索频率建议：月度（学术发表周期通常 1-3 个月）。
```

#### 改动量估算

- search_pipeline.py：+15 行（--since 参数解析 + 传递到各源 API）
- gw-search.md：+8 行（增量检索段落）
- tools-scenarios.md：+1 场景（S10 增量检索）

#### 复杂度影响

- 职责文件行数：gw-search.md 从 49 行增至 ~57 行（安全）
- 新增规则：1 条（增量检索频率建议）
- 无新增硬性规则或质量门槛

---

## P4：多维分类矩阵

### 需求

100+ 篇文献按单维度列表管理不可读，需要多维交叉分类。

### 当前状态

- `literature_notes.md` 模板：线性列表，每篇一个完整/浅读条目
- 实际项目中 `04_literature.md` 已手动演化出分类表（§2 四路线分类体系、§3 竞品区分表、§6 中等重叠论文列表、§9 文献索引表）

### 设计方案

#### templates.md 新增模板

在 literature_notes 模板之后增加两个模板：

**1. 文献索引表模板**（管理 50+ 篇的快速查阅）

```markdown
### 文献索引表

| ID | 第一作者 | 年份 | 核心方法 | 发表状态 | 发表渠道 | 精读/浅读 | 与本研究关系 |
|----|---------|------|---------|---------|---------|----------|------------|
| L01 | {作者} | {年} | {一句话} | {发表/预印} | {期刊/会议} | {精读/浅读/仅引} | {直接相关/可借鉴/...} |
```

用途：literature_notes.md 开头放一张索引表，替代逐条翻找。精读条目详写在下方，浅读/仅引的论文只出现在索引表中。

**2. 分类矩阵模板**（多维交叉分析）

```markdown
### 分类矩阵

按维度填入论文 ID，空格表示该论文不涉及该维度：

| 论文 | 问题建模 | 网络架构 | 奖励设计 | 多目标 | 规模验证 | 切换场景 |
|------|---------|---------|---------|--------|---------|---------|
| L018 | MOMDP | ED3QN | 加权和 | Pareto | 110星/10UE | 是 |
| L029 | MDP | Dueling DDQN | 自适应加权 | 吞吐/阻塞/切换 | 298星/10-30UE | 是 |
| ... | ... | ... | ... | ... | ... | ... |

### 维度空白分析
{列出哪些维度组合无论文覆盖，对应研究空白}
```

#### 放置位置

- 模板定义在 `templates.md`（和 literature_notes 模板平级）
- 实际使用在 `paper_materials/04_literature.md`（写作阶段的产物）
- 不改 `gw-read.md`——分类矩阵是写作阶段工具，不是 Groundwork 精读产出

#### 改动量估算

- templates.md：+25 行（两个模板 + 字段说明）
- 无工具改动
- 无流程改动

#### 复杂度影响

- 纯模板增加，不影响任何流程文件的行数或规则数
- 和现有 literature_notes 模板完全兼容（索引表是从 literature_notes 提取的视图）

---

## P5：BibTeX 批量生成

### 需求

100+ 篇引用需要完整 BibTeX 条目，手动逐条获取不可行。

### 设计方案

#### 工具方案

新增 `tools/bib`（bash wrapper → `bib.py`）：

```bash
# 从 literature_notes.md 中提取所有 DOI/arXiv ID，批量生成 BibTeX
bash tools/bib projects/leo-ntn-handover-drl/literature_notes.md -o references.bib

# 从搜索结果 JSON 生成
bash tools/bib search-archive/2026-05-10/leo-satellite.json -o refs.bib

# 单篇
bash tools/bib --doi 10.1109/TWC.2024.3406952
bash tools/bib --arxiv 2310.20215
```

#### 数据源

DOI → `https://doi.org/{doi}` 的 Content Negotiation（`Accept: application/x-bibtex`），免费无需 API key。
arXiv → 先通过 S2 API 查 DOI（arxiv → doi 映射），再走 DOI Content Negotiation。无 DOI 的 arXiv 论文生成简化 BibTeX 条目。

#### 产出格式

```bibtex
@article{Sun2024JSAC,
  author = {Sun, Geng and ...},
  title = {Collaborative Ground-Space Communications via ...},
  journal = {IEEE Journal on Selected Areas in Communications},
  volume = {42},
  number = {12},
  pages = {3395--3411},
  year = {2024},
  doi = {10.1109/JSAC.2024.3459029}
}
```

引用键生成规则：`{第一作者姓}{年份}{venue缩写}`，如 `Sun2024JSAC`。重名追加 a/b/c。

#### 与框架的关系

纯工具层，不改任何框架文件。用户在写作阶段手动调用，生成 .bib 文件后导入 LaTeX 编辑器。

#### 改动量估算

- 新文件：tools/bib（bash wrapper，5 行）+ tools/bib.py（~80 行）
- tools-scenarios.md：+1 场景（B4 BibTeX 生成）
- 无框架文件改动

#### 复杂度影响

- 零框架影响（纯工具层）
- 无新增规则或流程

---

## 总结

| 需求 | 类型 | 框架改动 | 工具改动 | 改动量 | 实现优先级 |
|------|------|---------|---------|--------|-----------|
| P3 增量更新 | 工具+流程 | gw-search.md +8 行 | search_pipeline.py +15 行 | ~25 行 | 大论文调研中期 |
| P4 分类矩阵 | 模板 | templates.md +25 行 | 无 | ~25 行 | 大论文写作初期 |
| P5 BibTeX | 工具 | 无 | 新增 bib.py ~80 行 | ~85 行 | 论文写作阶段 |

三个扩展均在当前文件结构安全范围内，不需要结构性调整。
