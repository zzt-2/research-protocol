# [S001] 论文精读溯源机制改进设计

> 2026-06-15 | 阶段: 实施完成 | 状态: 验证 PASS（待实战精读）
> 来源: research-direction-exploration H001/S002（即将开始 6 方向精读）+ explore 双勘察

## 目标

建立可追溯的论文精读笔记/日志机制。解决三个勘察确认的问题，使"笔记↔源文件"双向可查、精读历史可追溯。

## 记录

### 1. 现状勘察结论（3 个问题）

**① 溯源双向断**
- literature_notes.md 的 L 条目 13 字段**无"源文件路径"**，仅 DOI/arXiv ID（manual 无 DOI 论文断链）
- thesis-fso 笔记 21 条候选零路径标注；competitor_notes 有 arxiv id 不拼成 papers/ 路径
- papers/index.json 是下载/转换日志，无 read_status/read_date 字段
- 双向都断：笔记→源文件查不到，源文件→有没有精读过也查不到

**② content.md 乱（两病，独立于本专题）**
- 病 A：arxiv_html 类被 ltx_* CSS 类 + 站内 anchor 污染（可读但脏）
- 病 B：doi 类 63% 无 content.md（144/230 缺失，"有记录有引用但文件不存在"）

**③ 命名 join key 缺（① 的根因）**
- competitor_notes 用 {author}_{year}，papers/ 用 {arxiv_id}/{doi_path}/{slug}
- 两套命名无映射表，溯源链连不上

### 2. 决策：两层架构（用户同意，DECIDED）

| 层 | 位置 | 内容 | 消费者 |
|----|------|------|--------|
| **客观精读** | 全局 `papers/_read_notes/{paper_id}.md` | 13 字段客观提取 + source_path | 所有方向/项目共用 |
| **适配 + 日志** | `projects/{name}/read-log.md`；探索期记当前专题 | paper_id / 用于方向 / 适配分析 | 该 project 或探索专题 |

**为什么全局放客观精读**：
- 论文客观内容是全局资产（papers/ 本就全局共享）——同篇论文不同方向读不重复客观提取
- 绕开"探索期没 project"——精写全局笔记区，不需 project 存在
- 选定方向后 project 的 read-log 引用已有全局笔记，零迁移
- 文件名=paper_id = 天然 join key，双向链路自动通

### 3. 改动清单（4 条）

| # | 改动 | 文件 | 内容 |
|---|------|------|------|
| 1 | 新增全局精读笔记区 | 约定（CLAUDE.md 目录结构） | `papers/_read_notes/{paper_id}.md`，一篇一文件，文件名=paper_id |
| 2 | 新增项目级精读日志 | 约定（CLAUDE.md 目录结构） | `projects/{name}/read-log.md`：paper_id / 源路径 / 笔记路径 / 首读日期 / 重读次数 / 用于方向 |
| 3 | L 条目加源文件路径字段 | `templates.md` §literature_notes（~315行 L01）+ `stages/gw-read.md`（~32行模板 + 派遣清单 + 质量门槛） | `源文件路径` [MUST]，紧跟 DOI/来源，格式 `papers/{type}/{id}/content.md` |
| 4 | content.md 清洗/补转 | **拆独立子任务，不在本专题** | arxiv_html 清洗 + doi 补转 144 篇 |

### 4. paper_id 文件名约定

跟 papers/ 目录名一致（天然 join）：
- arxiv → arxiv_id（如 `2405.17150`）
- doi → doi_path 转义（斜杠替下划线，如 `10.1109_jlt.2025.3580733`）
- manual → slug（如 `cai-jsac-gdrl`）

文件名 = `papers/{type}/{id}/` 的 `{id}`，如 `papers/_read_notes/2405.17150.md`。

### 5. 向后兼容

- 历史 competitor_notes（6 篇）**不回溯迁移**（用户决定，太老）
- 旧 literature_notes.md 的 L 条目**不强制回填** source_path（新条目起强制）
- 框架文件改动后，新精读一律走 `papers/_read_notes/` + read-log

### 6. architect 评估定稿（2026-06-15）— 4 处补充 + paper_id 边界 + 执行顺序

**结论：方案可执行，无阻断性问题。** S001 原 4 条改动准确（gw-acquire.md 确认不需改，职责分离正确 ✓）。补充以下遗漏点进改动清单：

**补充改动（原清单遗漏）：**

| # | 补充改动 | 文件 | 位置 | 理由 |
|---|---------|------|------|------|
| 5 | Step 5 同步加源文件路径 | paper-materials-workflow.md | 第 108 核心论文条目 / 第 116 文献索引汇总 / 第 197 质量门槛 | **否则溯源链在写作阶段断裂**：04_literature.md 拿不到源路径 |
| 6 | gw-read.md 3 处细化 | gw-read.md | 第 14-22 派遣清单表 #1（13+→14+字段）/ 第 32-48 L01 模板（DOI 后加路径行）/ 第 168-174 质量门槛 | — |
| 7 | CLAUDE.md 三表 + 禁止事项 | CLAUDE.md | 目录结构表 / 文件路径规则表 / 跨阶段护栏表 / 禁止事项 | 约定落索引 |
| 8 | 浅读条目兼容 | templates.md | 浅读模板 | 标"无源文件（浅读）"作合法值，免被误判不达标 |

**paper_id 边界情况（实测 3 个）：**
1. 同篇 arxiv+doi → paper_id 取**首次下载来源 type**，read-log 记 `alt_ids` 字段记双 ID
2. arxiv_id 带版本号（如 2605.02416v1）→ paper_id **去版本号**（跟 papers/ 目录名一致），版本号记 read-log 备注
3. doi_path 转义（如 10.1007_s00158-022-03456-x）→ paper_id **直接取 papers/doi/{doi_path}/ 目录名字面值，不二次处理**

**全局 read_notes index：YAGNI，不建。** 靠 `ls papers/_read_notes/*.md` + `grep -l {paper_id} projects/*/read-log.md` 按需查。CLAUDE.md 注明"反向查询靠 grep"。

**执行顺序（executor 串行，避免措辞漂移）：**
1. CLAUDE.md 目录结构表（定义"存哪里"）
2. templates.md §literature_notes（L 条目 + 源文件路径规则小节 + 浅读兼容）
3. gw-read.md（派遣清单 + L01 模板 + 质量门槛）
4. paper-materials-workflow.md Step 5（条目 + 索引汇总 + 质量门槛）
5. CLAUDE.md 文件路径规则表 + 护栏表 + 禁止事项（收尾索引，引用前 4 文件位置）

**跨文件字段统一措辞（严格遵守）：**
- L 条目源文件路径行：`- **源文件路径**：papers/{type}/{id}/content.md`（type ∈ arxiv|doi|manual），紧跟 DOI/来源
- read-log 字段：paper_id | 源文件路径 | 笔记路径 | 首读日期 | 重读次数 | 用于方向 | alt_ids(可选)

## 决策引用

- 两层架构 = DECIDED（用户 2026-06-15 同意，含全局客观精读 + 项目级适配）
- content.md 拆出去 = DECIDED（用户"不急"）
- 历史不迁移 = DECIDED（用户"先不管"）

## 范围确认

- 本轮是否在 scope boundary 内：是。框架改动设计阶段，未动框架文件（待 architect → executor）。
- 范围变更记录：framework-evolution 已 closed，改新开 task 专题（非范围扩张）

### 7. 实施与验证（2026-06-15）— executor 落地 + 主线程独立验证

executor（opus）按 §6 执行顺序串行改 5 文件，13 处改动全部命中。主线程独立验证（grep + Read 交叉，非 executor 自验）：

| 文件 | 改动 | 验证 |
|------|------|------|
| CLAUDE.md | 目录树 +2 行（papers/ 第24行、projects/ 第46行）；文件路径规则表 +2 行（77-78）；护栏表 +1 行（154）；禁止事项 +1 行（86） | 缩进正确，树形未破坏 ✓ |
| templates.md | L01 模板加源文件路径（318）；新增"源文件路径字段规则 [MUST]"小节（369-380）；浅读模板加字段含"无源文件（浅读）"（394） | 小节完整，paper_id 三类取值清楚 ✓ |
| gw-read.md | 派遣清单 13+→14+（16）；L01 模板加路径（34）；质量门槛加 [MUST] 检查含 read-log 7 字段（176） | 7 字段写全 ✓ |
| paper-materials-workflow.md | Step5 核心条目加路径（109）；索引汇总加路径（114）；质量门槛追加（196） | 溯源链贯通到 04_literature.md ✓ |

**格式一致性**：源文件路径 `papers/{type}/{id}/content.md` 跨 5 文件统一 ✓；paper_id 规则（templates 定义 + gw-read 引用）一致 ✓；read-log 7 字段一致 ✓。

**Cosmetic 微瑕**：CLAUDE.md 77-78 行表格 pipe 未与原表完美对齐（中文混排对齐难，不影响 markdown 渲染）。不修。

**验证结论**：PASS（框架文件落地）。机制可用性待 dry-run 实战检验。

### 8. dry-run 试运行结果（2026-06-15）— 机制 PASS，抓到数据污染

派 executor（opus）精读 1 篇端到端跑新流程。选 DOI `10.3390/photonics10080914`（index.json 标 "All-Digital OPLL for LEO Satellite"，主题看似关联 B1/A 组）。

**机制验证（PASS）**：双向溯源实测通（笔记源路径→content.md ✅；paper_id→read-log→笔记 ✅）；paper_id 命名/14字段/read-log 放置均可用；两文件落地（笔记72行 + read-log 11行）。

**🔴 致命发现（数据层，超精读机制范围）**：
- content.md 正文实为石墨烯纳米二聚体非线性动力学（line 193 真实标题），与 OPLL/FSO 零相关
- metadata.json + index.json title 标 OPLL，且 download_status:success / content_quality:good
- 独立 grep：OPLL 词 0 命中，graphene 词 71 命中 → title 数据源与 content 数据源不一致
- **系统性风险**：若多篇 title 错配，R002/S002 基于 title 的方向判断可能站不住

**改进点清单（8 条，按优先级）**：详见 `verifications.md` V001。最高优先 P0 = title 污染排查。

**dry-run 价值**：没进 Groundwork 就抓到数据污染，避免精读错论文误导方向。

## 后续

- **机制落地完成**（2026-06-15），5 文件 13 处改动主线程验证 PASS
- **待实战验证**：方向探索阶段首次精读（gw-read）跑通 → 全局 `papers/_read_notes/` 落首篇 + read-log 记首条 → 确认溯源闭环 → 本专题 close
- **拆出的独立子任务**（不在本专题）：content.md 清洗（arxiv_html CSS 污染）+ doi 补转 144 篇
