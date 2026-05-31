# [S001] 框架问题日志 — 2026-05-15

> 审查人：Claude (analyst/architect 三 agent 并行审查)
> 审查范围：2026-05-15 的 6 个对话记录 + 13 个框架文档 + 全部工具代码
> 日志性质：问题记录 + 修复方向建议，框架改动将分批推进

---

## 已确认修复（2 项）

### FIX-1: SerpAPI key 轮换静默失败 — 已修复
- **位置**：`tools/litsearch/search_sources.py:420-435`
- **原问题**：`get_dict()` 在 key 耗尽时返回 `{"error":"..."}` 而非抛异常，`break` 永远在第一个 key 后执行，后续 12 个 key 从未被使用
- **当前状态**：已用 `data = None` + `continue` 遍历所有 key，全部失败时打印 "所有 key 均失败" 并返回空列表

### FIX-2: IEEE 付费墙下载 — 已改为无头浏览器
- **位置**：`tools/blit.py:153-212`
- **原问题**：IEEE 论文全部因付费墙下载失败（~60% 失败率）
- **当前状态**：通过 Playwright 无头浏览器 + 校园网 IP 自动机构认证，`getPDF.jsp?arnumber=ID` 直接获取 PDF

---

## P0: 结构性缺陷（4 项）

### P0-1: 步骤完成标记机制缺失

**问题**：Groundwork 阶段的步骤完成状态只存在于 git commit 消息中，无结构化标记。新对话恢复时 agent 无法快速判断哪些步骤已完成，导致重复执行。

**证据**：
- Beam Hopping 对话花 ~40% token 重跑 Step 2-3（合并 JSON、AI 候选审查），直到读到 commit `8e8121b` 才发现已在上个会话完成
- ISL 对话进入 Step 3.5 前花了一轮确认前置步骤状态
- agent 恢复逻辑是"读 handoff → 推断状态"，而非"读标记 → 确定"

**影响**：每次跨对话恢复都可能浪费 20-40% token 在重复工作上

**修复方向**：
- 在 `literature_notes.md` 头部增加步骤进度表
- 每步完成时由 agent 写入：`| Step X | completed | 2026-05-15 | abc1234 |`
- 新对话恢复时先解析此标记表，跳过已完成步骤

**涉及文件**：`stages/groundwork.md`（步骤编排表增加标记要求）、`templates.md`（literature_notes 模板增加进度表）

---

### P0-2: Handoff 信息递减

**问题**：后续轮次的 handoff 不包含前轮的关键上下文，但状态恢复协议说"读最新 handoff"，导致新对话丢失信息。

**证据**：
- ISL `handoff-2` 有完整的 IEEE 下载 URL 列表和综合分析要点，`handoff-3` 不再包含
- `handoff-3` 假设新对话已从 `handoff-2` 获取下载 URL，但恢复协议是"读最新"而非"读所有"

**影响**：跨对话恢复时关键上下文（下载 URL、竞品论文列表、参数选择依据）丢失

**修复方向**：
- handoff 模板增加"从上轮继承的关键上下文"字段
- 每份 handoff 必须自包含恢复所需最小信息
- 或改为增量追加式（不覆盖，只追加关键增量）

**涉及文件**：`CLAUDE.md`（handoff 格式定义）

---

### P0-3: 中文检索策略完全缺失

**问题**：`gw-search.md` 的检索操作全部基于英文七源聚合，中文检索仅一句"用 `--source cnki`"带过。实际中文检索是完全不同的工具链。

**证据**：
- `ed68cb75` 对话中从发现 CNKI 需要认证到写 `cnki_login.py` 到测试可用，花了约 15 轮交互
- `fa2d36ba` 对话中 CNKI `--download` 一次性下载 84 个文件，大部分是学位论文，需后续人工筛选
- CAJ 格式文件下载后 `tools/convert` 无法转换，工具链断裂
- `search_config.py` 的 `chinese` 模式只路由到 `serpapi`，对中文学术搜索覆盖极有限
- webReader 抓取期刊官网 HTML 全文（如自动化学报 `aas.net.cn`）效果极好，但框架未记录

**中文检索的实际需求**：
1. CNKI cookie 初始化流程（`cnki_login.py` → 验证 → cookie 自动保存）
2. 期刊论文 vs 学位论文的过滤方法（blit CNKI 搜索无此过滤）
3. CAJ 格式的处理（转换工具不支持）
4. CSSCI 核心期刊的验证方法
5. 期刊官网 HTML 全文抓取作为备选路径

**影响**：每次中文检索都靠 agent 试错发现完整流程，消耗大量 token

**修复方向**：
- 在 `gw-search.md` 或 `tools-guide.md` 增加独立的"中文检索策略"章节
- 覆盖上述 5 个需求点
- blit CNKI 搜索增加 `--type journal` 过滤参数
- `tools/convert` 增加 CAJ 文件检测和提示

**涉及文件**：`stages/gw-search.md`、`tools-guide.md`、`tools/blit.py`、`tools/pdf_convert.py`

---

### P0-4: chinese 模式源路由错误 + 工具链脱节

**问题**：`search_config.py` 的 `MODE_SOURCES["chinese"]` 只有 `serpapi`，`DOC_TYPE_SOURCE_MAP["chinese_journal"]` 只映射 `exa`/`firecrawl`（对中文无效）。blit 的 CNKI/万方搜索能力完全无法通过 literature_search 调用。

**证据**：
- `search_config.py:52` — `MODE_SOURCES = {"chinese": ["serpapi"]}`
- `search_config.py:68` — `chinese_journal` 映射到 `["exa", "firecrawl"]`
- `MODE_SOURCES["chinese"]` 会覆盖 doc-type 映射，导致 `--doc-types chinese_journal` 也无法命中正确源
- `blit.py` 和 `literature_search.py` 是完全独立的工具，没有集成路径
- 两者的结果格式不一致（字段名 `source`/`cite` vs `source_api`/`citation_count`），合并时需手动对齐

**影响**：中文检索需要手动运行 blit，结果无法纳入统一搜索流程

**修复方向**：
- 选项 A：在 literature_search 中集成 blit 调用（工作量大）
- 选项 B：在框架文档中明确两个工具的分工和结果合并方法（快速修复）
- 修正 `chinese_journal` 的源映射
- 提供结果格式对齐工具或文档

**涉及文件**：`tools/litsearch/search_config.py`、`tools/litsearch/search_sources.py`、`tools/blit.py`（原文如此，应为 `tools/lit.py`）、`tools-guide.md`

---

## P1: 流程缺陷（8 项）

### P1-1: Step 4a/4b 依赖关系未文档化

**问题**：`groundwork.md` 编查看表中 Step 4a 在 Step 5 前、Step 4b 在 Step 5 后，这个反直觉拆分无解释。

**证据**：ISL `handoff-4` 写到"Step 4b 需在 Step 5 Baseline 选定后执行"，这是从 handoff 中学到的，非从框架文档直接获得。

**修复方向**：在 `groundwork.md` 编查看表下方增加步骤间 DAG 依赖说明

**涉及文件**：`stages/groundwork.md`

---

### P1-2: GW 完成条件数字不一致

**问题**：`groundwork.md` 完成条件要求 `literature_notes.md` 包含 ≥8 篇核心文献，`gw-read.md` 质量门槛只要求 ≥5 篇精读，关系未说明。

**修复方向**：在 `groundwork.md` 完成条件处增加注释："5 篇为 Step 3 单步通过门槛，8 篇为 GW 整体完成门槛。Step 3.5 补充检索后通常可达 8+。"

**涉及文件**：`stages/groundwork.md`、`stages/gw-read.md`

---

### P1-3: Contract Step 0 与 GW Step 1-3 大量重复

**问题**：Contract Step 0 的"新颖性检索"流程（0.1 系统检索 → 0.2 竞品精读 → 0.3 二轮定向）几乎完整重复了 GW 的搜索-下载-精读-补充检索循环。

**证据**：`contract.md` Step 0 有约 20 条规则，其中 15+ 与 GW Step 1-3 操作相同

**修复方向**：增加"复用条件"——"已有 literature_notes 且 ≥8 篇精读 → 跳过 0.1，仅做 0.2 竞品补充精读"

**涉及文件**：`stages/contract.md`

---

### P1-4: 搜索-下载-转换管线无状态追踪

**问题**：大量论文的 searched → downloaded → converted → structured 状态无处追踪，上下文溢出后中间状态全部丢失。

**证据**：`fa2d36ba` 对话下载 84 个文件后上下文溢出，恢复后只能用 `ls` 重新确认哪些已转换

**修复方向**：维护 `_pipeline-status.json` 追踪每篇论文的管线状态

**涉及文件**：框架级新增机制

---

### P1-5: 子 agent 无执行时间上限

**问题**：子 agent 可无限运行，出现过 38 分钟（2276s, 98 次工具调用）的 agent 阻塞主流程。

**证据**：`fa2d36ba` 对话的 search-eco-soc agent，`duration_ms: 2276238`

**修复方向**：框架应为子 agent 设置 15 分钟上限，超时返回已完成部分

**涉及文件**：`CLAUDE.md`（上下文管理规则）

---

### P1-6: CNKI 搜索无法过滤学位论文

**问题**：blit 的 CNKI 搜索无类型过滤，返回大量学位论文噪声。

**证据**：`fa2d36ba` 对话中 CNKI `--download` 一次性下载 84 个文件，大部分是学位论文

**修复方向**：blit CNKI 搜索增加 `--type journal` 参数，默认过滤学位论文

**涉及文件**：`tools/blit.py`

---

### P1-7: CAJ 格式无法转换，工具链断裂

**问题**：`tools/convert` 只支持 PDF，CNKI 默认下发 CAJ 时无法处理。

**修复方向**：
1. blit 下载时优先请求 PDF 格式
2. `tools/convert` 检测 CAJ 文件给出明确提示

**涉及文件**：`tools/blit.py`、`tools/pdf_convert.py`

---

### P1-8: IEEE/CNKI 下载与 litdownload 管线割裂

**问题**：blit 的 IEEE/CNKI 下载不走 litdownload 管线，无全局索引去重、无 metadata 写入、无 content.md 自动生成。

**证据**：
- `download_config.py:20` — `BLOCKED_DOMAINS = {"ieeexplore.ieee.org"}` 明确屏蔽 IEEE
- blit 通过校园网 IP 能下载 IEEE PDF，两套工具策略互斥
- 下载后需手动运行 `tools/convert` 做 PDF 转 markdown

**修复方向**：文档中明确两套下载工具的分工，或整合到统一管线

**涉及文件**：`tools/litdownload/download_config.py`、`tools/blit.py`、`tools-guide.md`

---

## P2: 文档/维护问题（8 项）

### P2-1: quality 参数枚举不一致
- `download_pipeline.py:349` choices 含 `["fast", "standard", "high"]`
- `pdf_convert.py:309` choices 只有 `["fast", "standard"]`
- `download_channels.py:114-126` 只处理 `fast` 和空字符串
- **涉及文件**：`tools/litdownload/download_pipeline.py`、`tools/pdf_convert.py`、`tools/litdownload/download_channels.py`

### P2-2: `--merge` 多文件用法未文档化
- `tools-guide.md` 只展示单文件用法
- 实际支持逗号分隔多文件：`--merge a.json,b.json,c.json`
- **涉及文件**：`tools-guide.md`

### P2-3: 目录命名不一致
- `tools-guide.md` 用 `paper-archive/{batch}/`
- `CLAUDE.md` 用 `papers/{arxiv|doi|manual}/`
- **涉及文件**：`tools-guide.md`、`CLAUDE.md`

### P2-4: thesis-materials.md 修改清单状态不明
- 5. 节列出 8 处需要修改的框架文件，是否已落地不明
- 如果已落地应标记"已整合"或删除；如果未落地则框架处于不一致状态
- **涉及文件**：`stages/thesis-materials.md`

### P2-5: webReader 抓期刊官网是有效路径但未记录
- 从 `aas.net.cn` 等期刊官网抓取 HTML 全文效果极好
- 完全不在 `tools-guide.md` 或任何框架文件中
- **涉及文件**：`tools-guide.md`

### P2-6: gw-read 结构化提取模板只适配 DRL
- 6 个子表（状态空间/动作空间/奖励函数/建模假设/网络架构/适配性分析）
- 非 DRL 论文（纯优化、系统论文）缺少提取模板
- **涉及文件**：`stages/gw-read.md`

### P2-7: Handoff 命名规范不统一
- ISL 项目产生 `handoff.md`（无编号）+ `handoff-1.md` + `handoff-2.md` + ...
- Beam Hopping 项目产生 `handoff.md` + `handoff-2.md`（跳过 handoff-1）
- 首轮编号规则不一致
- **涉及文件**：`CLAUDE.md`（已在新版中通过编号规则解决）

### P2-8: 框架大量规则隐含 DRL 假设
- 奖励函数审查、MDP 试运行、状态/动作/奖励结构化提取、反模式中的 DRL 陷阱
- 非 DRL 方向（纯监督/纯优化/系统设计）会遇到大量不适用的步骤
- **涉及文件**：`overview.md`、`stages/groundwork.md`、`domain-comms.md`

---

## 工具链能力矩阵

### 搜索源

| 源 | 工具 | 中文支持 | 学术覆盖 | 限制 |
|----|------|---------|---------|------|
| S2 (Semantic Scholar) | literature_search | 差 | 高（英文） | 无 key 时 fast_fail |
| OpenAlex | literature_search | 差 | 高（英文） | — |
| arXiv | literature_search | 无 | 高（预印本） | 3s 硬等待 |
| SerpAPI Scholar | literature_search | 差 | 高（英文） | 付费，key 有限 |
| SerpAPI Web | literature_search | 中 | 中 | 付费，key 有限 |
| Tavily | literature_search | 中 | 中 | 付费 |
| Firecrawl | literature_search | 差 | 低 | 付费 |
| Exa | literature_search | 差 | 中 | 付费 |
| IEEE | blit --source ieee | 无 | 高（英文期刊/会议） | 校园网 IP 认证 |
| 万方 | blit --source wanfang | 好 | 中（中文） | 仅搜索，无下载 |
| cbpt | blit --source cbpt | 好 | 低（单刊） | 接口已挂 |
| CNKI | blit --source cnki | 好 | 高（中文） | Cookie 认证，含学位论文噪声 |

### 下载源

| 源 | 工具 | 格式 | 认证 | 付费墙 | 管线集成 |
|----|------|------|------|--------|---------|
| arXiv | litdownload | HTML/LaTeX/PDF → .md | 无 | 开放 | 完整（索引+metadata+content） |
| OA PDF | litdownload | PDF → .md | 无 | 开放 | 完整 |
| Unpaywall | litdownload | PDF → .md | email | 查找合法 OA | 完整 |
| IEEE | blit --download | PDF | 校园网 IP | 校园网可下 | 无（需手动 convert） |
| CNKI | blit --download | PDF/CAJ | Cookie | 机构认证 | 无（需手动 convert） |

---

## 待讨论的 Open Questions

1. **步骤完成标记位置**：`literature_notes.md` 头部 vs `decision_log.md`？— 影响所有项目的状态恢复流程
2. **下载失败缓存层级**：工具层实现（修改 download 脚本）vs agent 层实现（规则约束）？— 工具层更可靠但需开发
3. **CBPT 处置**：从工具链移除 vs 标记为实验性？— 影响中文期刊检索的推荐策略
4. **blit ↔ literature_search 集成**：选项 A（代码集成）vs 选项 B（文档化分工）？— 工作量差异大
5. **handoff 设计模式**：每轮覆盖（简洁但丢上下文）vs 增量追加（完整但膨胀）？— 需在可恢复性和可读性间取舍
6. **DRL 假设处理**：框架增加"研究类型分支"指引 vs 保持现状按需跳过？
7. **search-archive 索引**：是否需要自动维护的 `_index.json`？— 影响跨对话复用效率
