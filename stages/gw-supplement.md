# 定向补充检索（gw-supplement）

> Step 3 精读后的必做步骤。用精读产生的新认知做一轮定向检索，弥补初始搜索的盲区。

## 入参
- `literature_notes.md`（精读完成，综合分析中的新发现）
- `search-archive/{date}/` 下已有的搜索结果

## 出参
- `search-archive/{date}/` 下的补充检索 JSON
- 更新后的 `literature_notes.md`（新增论文条目 + 更新综合分析）

## 触发条件

精读完成后**必须执行**，不需额外判断。典型触发场景：
- 精读论文 related work/reference 中出现高度相关但未收录的论文
- 综合分析发现新的技术子方向，当前候选池未覆盖
- 竞品分析发现新的直接竞争者
- 方向收窄后，需要更精确的检索词覆盖特定方法/场景

## 操作

### 1. 构造定向检索词（系统性，非凭感觉）

从精读发现中提炼关键词，按以下矩阵组织：

```
方法变体（≥3 种）：如 GNN / GAT / GraphSAGE / MPNN / GCN
问题场景：如 routing / load balancing / scheduling
规模/泛化关键词：如 size generalization / scalability / cross-scale / transfer / zero-shot
```

组合检索：方法变体 × (问题场景 ∪ 规模关键词)。总组合数 ≥ 方法变体数 × 2。

### 2. 执行检索

- 用 `tools/search` 或 Semantic Scholar API 检索
- 搜索源覆盖 ≥2 个（Semantic Scholar + 至少一个其他源）
- 每个组合返回结果存入 `search-archive/{date}/{slug}.json`

### 3. 引用链分析

- **前向引用链**（citing papers）：对 1 篇最高引用的核心竞品，获取其被引列表，筛查新增竞争者
- **后向引用链**（references）：对同一竞品，获取其参考文献，发现技术基础和可能的更早竞争者
- 引用链筛查在子 agent 中执行（见 CLAUDE.md "上下文管理规则"），主对话只接收筛选后的候选列表

### 4. 新论文处理

- 新发现的高相关论文走 gw-acquire → gw-read（精读或浅读）
- 新增条目写入 `literature_notes.md`

### 5. 更新综合分析

每轮检索完成后更新 `literature_notes.md` 的综合分析部分（方法分类、Baseline 惯例、创新空间等）。

## 检索充分性判据

以下条件**全部满足**方可终止：

1. **关键词矩阵覆盖**：按上述矩阵构造的组合均已检索
2. **搜索源覆盖**：≥2 个不同搜索源
3. **引用链分析**：至少 1 篇核心竞品的双向引用链已分析
4. **收敛性**：最后一轮新增"必读/建议读"论文 = 0
5. **上限**：3 轮。3 轮后仍未收敛 → 记录未覆盖方向，由用户决定是否继续

## 上下文保护规则

> 这些规则是对 CLAUDE.md "上下文管理规则" 的步骤级细化。

### web fetch 限制

- 验证论文贡献声称时，**必须用 API**（Semantic Scholar API、DOI 查询），不用 webReader 抓页面
- web search 结果中的事实性断言（如"论文 X 实现了 Y"）必须用论文 abstract 交叉验证（见 CLAUDE.md "web 事实性交叉验证"）
- **禁止**用 webReader 抓 ResearchGate / Google Scholar / IEEE Xplore 页面来获取论文信息——这些页面会往上下文灌入大量无关 HTML

### 子 agent 强制委托

以下操作必须在子 agent 中执行：
- 引用链批量筛查（≥10 篇逐一查 abstract）
- web search 结果的分析和筛选
- 新论文 abstract 的批量验证

主对话只接收：
- 筛选后的候选列表（≤10 篇，含标题、DOI、1-2 句相关性判断）
- 验证结论（如"GRLR 的 size generalization 声称为 AI 推断，abstract 不支持"）

### 单轮 web fetch 上限

主对话中单轮 web fetch（含 webReader 和 WebSearch）≤5 次。超过则分批到新对话或子 agent。

## 质量门槛

- 检索充分性判据全部满足（或已达 3 轮上限）
- `literature_notes.md` 综合分析已更新
- 新发现的核心竞品已记录到 `literature_notes.md` 和 `decision_log.md`
- **路径合规**：检索结果存放在 `search-archive/{date}/`，不在其他位置

## 不达标时

- 关键词矩阵未覆盖 → 补充检索
- 引用链未分析 → 至少对 1 篇核心竞品做双向分析
- 收敛性不满足但已达 3 轮上限 → 记录未覆盖方向，由用户决定
