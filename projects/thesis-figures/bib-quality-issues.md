# 参考文献质量问题清单

> 2026-05-28 | 开题报告 docx 转换后审查

## 一、问题清单

### P0 — 中文文献作者不全

**现象**：大量中文条目只列了 1 个作者，但综述/研究论文基本都是多作者。

受影响条目（单作者，几乎可以确定漏了）：
- cn-zhu2021 朱立东、cn-ni2023 倪少杰、cn-chen2022constellation 陈全、cn-wang2023future 王宁远
- cn-ruan2022design 阮永井、cn-yan2024isl 燕锋、cn-li2025routing 李佳奇、cn-sun2024leo 孙耀华
- cn-li2025federated 李学华、cn-wei2023spatiotemporal 魏德宾、cn-wu2022gnn 吴博
- cn-ma2022gnn 马帅、cn-xiao2024largegnn 肖国庆、cn-liu2018drl 刘全、cn-li2021drlcombopt 李凯文
- cn-xu2020satground 徐晖、cn-yuan2021sdn 袁硕、cn-sun2025dynamic 孙士兵
- cn-wang2023protocol 王子涵、cn-zhao2025multilayer 赵艳春、cn-liu2020linkaware 刘洵
- cn-zhu2022handover 朱洪涛（只有 2 个，可能也漏了）

**国标要求**：超过 3 人列前 3 人加"等"，≤3 人全部列出。

**修复方式**：逐条在 CNKI/万方查原文补全作者列表。

### P1 — 英文文献作者被 API 错误匹配

**现象**：之前用 OpenAlex 按标题搜索补全的作者，有几条匹配到了错误论文。

已确认或高度可疑的错误：
- `ch1-dgaies2025`：匹配到量子计算论文（Cerezo, M. 等），实际应为 IoT 领域 LEO 论文
- `ch1-sizgen2025`：匹配到 Quantum ESPRESSO 作者（Giannozzi, P. 等），实际应为 ML 理论论文
- `ch1-disgen2024`：匹配可能不准（Huang, Zheng 等），需核实 ICML 2024 论文
- `ch1-gatLstmDqn2026`：匹配到 Akyildiz 等人，需核实
- `ch2-shen2020twc`、`ch2-eisen2020tsp`：标题太短/太泛，匹配可能不准
- `ch2-yin2022mis`：标题极简，匹配可能不准
- `ch3-chen2025sensors`、`ch3-huang2024tvt`：匹配可能不准

**修复方式**：用 DOI 在 CrossRef 查（有 DOI 的用 CrossRef 是准确的），没 DOI 的手动核实。

### P2 — arXiv 预印本被标为 [Z]（其他）

**现象**：arXiv 预印本在 docx 输出中显示为 `[Z]`，例如条目 24、25。

**国标要求**：预印本应标为 `[EB/OL]`（电子资源）或 `[PP/OL]`（预印本）。

**根因**：pandoc 的 `china-national-standard-gb-t-7714-2015-numeric.csl` 将 `@misc` 类型映射为 `[Z]`。

**修复方式**：
- 方案 A：修改 CSL 文件，让 `@misc` + `eprint` 字段输出 `[EB/OL]`
- 方案 B：将 arXiv 条目从 `@misc` 改为 `@online`（如果 CSL 支持的话）
- 方案 C：直接在 bib 里把 `@misc` 改为 `@article` 加 `journal = {arXiv preprint}`

### P3 — 期刊论文缺页码

**现象**：多条期刊文章缺少页码。

**国标要求**：期刊 [J] 必须有起止页码（或文章编号）。

**修复方式**：用 CrossRef API 按 DOI 批量查页码并补全。

### P4 — ch2-sun2024jsac / ch2-sun2026tmc 作者写法异常

**现象**：`author = {Sun, Geng and [Others]}`，`[Others]` 不是合法的作者占位符。

**修复方式**：手动查这两篇 Sun, Geng 的论文补全全部作者。

## 二、根因分析

### 为什么会有这些问题？

bib 文件的生成链路是这样的：

```
论文全文 (content.md)
  → 子 agent 精读 → materials.md（角色、贡献、方法细节）
    → 手动/半自动 → references.bib（完整元数据）
```

问题出在第二步：

1. **materials.md 不存元数据**：只记录论文的学术角色（"GNN 路由前驱"、"竞品"）和方法细节，不记录作者、页码等书目信息。这是设计上的分工——materials.md 关注"这篇论文对我有什么用"，不关注"怎么引用它"。

2. **bib 是手动拼的**：从 materials.md 的 cite key 映射到 bib 条目时，需要手动填入作者、页码等信息。中文论文的作者列表很长（动辄 5-8 人），手动转录容易偷懒只写第一作者；英文论文的作者从标题更难推断，所以直接标了 `[?]`。

3. **工具链没有"自动补全 bib 元数据"的能力**：`tools/search` 能检索论文，但检索结果是 JSON 摘要，不直接生成 bib 条目。`tools/download` 下载 PDF 后转 content.md，也没有自动提取结构化元数据的步骤。

### 根因确认（工具链审计）

经审查搜索工具代码（`tools/litsearch/search_sources.py`）：

- **S2/OpenAlex/arXiv 搜索是返回作者的**（`:100`、`:263-266`、`:190`），搜索 JSON 中 `authors` 字段有完整列表
- **Exa/Firecrawl 中文搜索不返回结构化作者**，作者信息混在 `title` 里，`authors: []`
- **`blit.py`（CNKI 搜索）有作者提取**（`:116-127`），但格式与英文源不同

**核心缺失**：工具链没有"搜索结果 JSON → bib 条目"的自动转换环节。搜索数据里有作者，但 bib 是手动拼的，没用搜索结果里的数据。

### 工具层面可以改进的点

| 改进 | 描述 | 优先级 |
|------|------|--------|
| `tools/search2bib`：从搜索 JSON 生成 bib | 读搜索结果 JSON，用 DOI 查 CrossRef 补全元数据（作者、页码、卷期），输出 bib 条目 | 高 |
| 中文论文作者批量补全 | 用 `blit --source cnki` 或 CNKI cookie 查作者列表，批量回填 bib | 高 |
| CSL 文件本地化 | 维护自定义 CSL，修正 `@misc → [Z]` 等问题 | 中 |
| bib 质量检查脚本 | 定期检查：作者数、页码、DOI、类型标识 | 中 |

## 三、修复计划

按优先级排序，可在后续对话逐个执行：

1. **P0 中文作者补全**：用 CNKI 查每篇论文的完整作者列表，更新 bib
2. **P1 英文作者核实**：用 DOI + CrossRef 核实 OpenAlex 匹配的作者，修正错误
3. **P2 [Z] → [EB/OL]**：修复 CSL 或 bib 条目类型
4. **P3 页码补全**：用 CrossRef API 批量查页码
5. **P4 Sun 论文作者**：手动补全
