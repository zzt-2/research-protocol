# 框架重构计划：可引用性 + 职责拆分 + JSON 重组

> 2026-05-10 讨论锁定。2026-05-10 全部 Phase 执行完毕并通过验证。

---

## 一、问题诊断

LEO 切换 GNN+DRL 项目中，6 篇核心文献中 5 篇标注为 arXiv 预印本，竞品论文全部正式发表。
根因是框架在检索/筛选/精读/写作全链条缺少"发表状态/可引用性"维度。

经 3 轮验证（子 agent 并行），发现三个层面的问题：

### 层面 1：流程缺失

- groundwork.md Step 1 初筛标准无"发表状态"维度
- Step 2 覆盖面缺口报告无"引用质量分析"节
- Step 3 精读模板无"发表状态"/"发表渠道"字段
- contract.md Step 0.1 新颖性检索无引用质量要求

**已修复**（前一轮对话完成）：上述 4 处 + templates.md + tools-guide.md 共 7 处框架改造已完成。
`tools/search` 已增加 `publication_status` 后处理（published/preprint/unknown）。
LEO 项目 literature_notes 已补更 3 篇正式发表信息（L024→TWC, L022→PIMRC, L016→TMC）。

### 层面 2：工具能力沉睡

`tools/search` 有 11 个功能/参数组在 groundwork.md 和 contract.md 中完全未引用：

| 沉睡功能 | 可覆盖需求 |
|----------|-----------|
| `--citations` / `--citations-direction` / `--citations-depth` | 引用链系统性展开 |
| `--find-similar` | 从核心论文找同类工作 |
| `--trend` / `--trend-years` | 综合分析"2-3 年趋势" |
| `--doc-types` (standard/journal/etc) | 标准文档/期刊定向检索 |
| `--preset comparison` | Survey/Review 发现 |
| `--preset implementation` | 开源代码查找 |
| `--merge` | 多轮结果合并 |
| `--mode standard` | 标准文档搜索路由 |

**结论**：不加新功能，通过独立的"工具使用场景手册"激活。

另有 2 个文档错误需修：
- contract.md Step 0.1 引用旧脚本 `python tools/literature_search.py`，应改为 `bash tools/search`
- groundwork.md Step 1 不达标部分写 `--preset broad`，但 broad 是 `--mode` 的值不是 `--preset`

### 层面 3：框架文档超载

groundwork.md 当前 440 行、16 条硬性规则、25 个条件分支，预期遵循率 <55%。
试跑失败教训（F4/F5）印证：被违反的规则离执行点 100+ 行，在超长文档中被遗忘。
继续追加内容（浅引流程 +20 行、引用链流程 +20 行）将使活跃规则达到 22-24 条。

**结论**：拆分 groundwork.md 为按职责的子文件。

---

## 二、决策记录

| 决策点 | 决策 | 理由 |
|--------|------|------|
| 可引用性机制 | 6 处框架改造 + publication_status 后处理 | 已完成 |
| 工具复杂度控制 | 不加新功能，激活沉睡功能 + 独立场景手册 | 工具已够复杂，不堆功能 |
| 框架文档拆分方式 | **按职责拆**（不是按步骤） | 某些职责跨阶段复用（搜索在 Groundwork 和 Contract 都用） |
| 工具场景手册位置 | `tools-scenarios.md`（根目录，和 tools-guide.md 平级） | agent 按需查阅，不全程加载 |
| 职责间传递协议 | 文件路径 | 简单可预测 |
| JSON 重组 | papers/ 一级实体 + batches/ 索引 + index.json 去重 | 解决重复下载/大小写不一致/嵌套过深 |
| 大论文扩展 | 当前不设计，但不阻碍后续 | 文件结构天然可扩展（迭代检索/浅读/索引表/增量更新） |

---

## 三、执行计划

### Phase 1：JSON 组织改造（最先执行，基础设施）

改造 `download_pipeline.py` 和 `search_pipeline.py`：

**新目录结构**：
```
├── papers/                          # 论文一级实体（替代 paper-archive/）
│   ├── index.json                   # 全局索引 doi/arxiv_id → 路径
│   ├── arxiv/{arxiv_id}/            # arXiv 论文
│   │   ├── metadata.json
│   │   ├── source.html|.tar.gz|.pdf
│   │   └── content.md
│   ├── doi/{doi_path}/              # DOI 论文（doi 小写，/ 替换 _）
│   │   ├── metadata.json
│   │   └── content.md
│   └── manual/{slug}/               # 手动获取
│       ├── metadata.json
│       └── source.pdf
├── batches/                         # 下载批次索引（替代 paper-archive/{batch}/_manifest.json）
│   └── {date}-{slug}/
│       └── _manifest.json
├── search-archive/                  # 搜索结果（位置不变，改 slug 生成规则）
```

**关键改动**：
- DOI 路径统一小写：`10.1109/TWC.2024.3406952` → `papers/doi/10.1109_twc.2024.3406952/`
- slug 生成区分查询类型（关键词/URL/DOI/中文）
- `index.json` 做全局去重（同一论文只存一份）
- 批次 manifest 只存索引指针，不嵌套论文文件

**迁移策略**：Phase 1 只改工具代码（新下载走新路径），旧 paper-archive 保留不删。后续手动迁移。

### Phase 2：groundwork.md 拆分

```
stages/
├── groundwork.md          # 编排文件（~60 行）：步骤索引 + 完成条件 + 文件传递协议
├── gw-search.md           # 检索 + 初筛 + 浅引提取（~80 行）
├── gw-acquire.md          # 下载 + 转换 + 质量门 + 覆盖面报告（~90 行）
├── gw-read.md             # 精读 + 提取（~60 行）
├── gw-validate.md         # 交叉验证 + Baseline 选定（~55 行）
├── gw-experiment.md       # 仿真器设计 + 搭建 + 验证 + Baseline 复现（~120 行）
├── contract.md            # Contract 阶段（168 行，暂不拆，修引用错误）
```

每个职责文件头部声明入参/出参（文件路径）。
编排文件 groundwork.md 只写"做什么、传什么"，指向职责文件。
同时修两个文档错误（`literature_search.py` → `tools/search`，`--preset broad` → `--mode broad`）。
contract.md 中 Step 0.1/0.2/0.3 的检索/精读改为指向 gw-search.md / gw-read.md。

### Phase 3：tools-scenarios.md 编写

独立参考手册，agent 按关键词查阅。9 个场景（S1-S9），每条 3 行：
参数、适用时机、注意事项。包含 `blit` 的 3 个场景（IEEE/万方/cbpt）。

### Phase 4：后续（本次不执行）

- 大论文增量更新机制（`--since` 参数）
- 浅读轻量级模板
- 文献索引表/分类矩阵模板
- BibTeX 批量生成

---

## 四、并行关系

```
Phase 1 (JSON 改造)
  ↓ 路径约定确定后
Phase 2 (groundwork 拆分) ←── 依赖新路径约定
Phase 3 (scenarios 手册) ←── 独立，可与 Phase 2 并行
```

Phase 2 和 Phase 3 可以并行，但都依赖 Phase 1 的路径约定。
实际操作：Phase 1 先跑完确认新路径，Phase 2+3 并行。

---

## 五、小论文 vs 大论文需求差异备忘

| 维度 | 小论文 (20-30 篇) | 大论文 (100+ 篇) | 当前覆盖 |
|------|------------------|-----------------|---------|
| 检索 | 3-4 组关键词，1-2 轮 | 8-15 组，3-5 轮迭代 | 部分 |
| 阅读深度 | 精读 8 篇 + 浅引 15 篇 | 精读 25 篇 + 浅读 50 篇 + 仅引 40 篇 | 部分（缺浅读层） |
| 引用链 | 顺带补充 | 系统性双向展开 | 工具有，流程缺 |
| 分类 | 线性分类 | 多维矩阵 | 否 |
| 增量更新 | 不需要 | 月度补充 | 否 |
| 写作衔接 | 笔记直接改写 | 多步结构化转换 | 否 |
| 引用质量 | 50% 正式发表 | 60-70%，预印本追踪 | 部分已修复 |

量变项：关键词数量、候选池大小、精读论文数量、引用链深度
质变项：迭代检索流程、分层阅读机制、多维分类矩阵、增量更新、引用管理工具集成

---

## 六、执行状态

| Phase | 内容 | 状态 | 日期 |
|-------|------|------|------|
| 0 | 可引用性机制（7 处框架改造 + publication_status 后处理 + LEO 笔记补更） | 完成 | 2026-05-10 |
| 1 | JSON 组织改造（papers/ 一级实体 + index.json + batches/ + slug 改进 + 旧数据迁移） | 完成 | 2026-05-10 |
| 2 | groundwork.md 拆分（6 职责文件 + 编排文件 + 文档错误修复） | 完成 | 2026-05-10 |
| 3 | tools-scenarios.md（12 个场景卡片，激活 11 项沉睡功能） | 完成 | 2026-05-10 |
| 2a | 浅读模板 + 低优先级修补（templates/gw-read/gw-acquire/gw-search） | 完成 | 2026-05-10 |
| 2b | 迭代检索编排（groundwork.md +15 行） | 完成 | 2026-05-10 |
| — | LEO 项目回测验证（Step 1-3 全通过 + 路径一致性确认） | 完成 | 2026-05-10 |

### 待后续（有实际需求时再做）

| 优先级 | 需求 | 类型 | 说明 |
|--------|------|------|------|
| P3 | 增量更新 | 工具级 | --merge 已够用手动触发，--since 参数等真实需求再加 |
| P4 | 多维分类矩阵 | 模板级 | 写作阶段产物，等大论文文献综述时再加模板 |
| P5 | BibTeX 批量生成 | 工具级 | 半自动 tools/bibtex 脚本 + 用户检查，不改框架 |
