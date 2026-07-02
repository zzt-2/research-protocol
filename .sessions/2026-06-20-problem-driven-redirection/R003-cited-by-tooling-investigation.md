# [R003] Cited-by 召回工具现状调研 + D017 v2 步骤 2 预案落地

> 2026-07-01 | 关联：专题 2026-06-20-problem-driven-redirection / D017（D015 v2）步骤 2 / H016 路径 B
> 来源：S026（本轮）执行 H016 路径 B

## ⚠️ 2026-07-02 重要更正（用户质疑触发的诚实核查）

**初版结论"双源 union 强互补，推荐 both"是基于不充分验证（只数条数没查内容真伪）下的乐观结论，现部分推翻。** 用户追问"真的可用吗？拿到的对吗？"后做了内容交叉验证，发现：

- **抽查 10 条**（查每条论文的 references 真含不含 Paillier）：OA-only/overlap 6/6 真引用 ✅，**S2-only 4/4 在 OpenAlex references 查不到**
- 其中 **2019 ICSOS 论文（2019-10 发表）被 S2 算成引用 2020-08 Paillier——时间逻辑铁证假 cited-by**（论文不可能引用 8 个月后才发表的文献）
- 根因：**S2 `/paper/{id}/citations` 召回比 OpenAlex 杂**，把部分"相关论文"当成 citing paper（含 S2 的推荐语义，非纯引用关系）

**修正后的结论**（取代下方"主源选择=双源 union"）：
- **主源 = OpenAlex（默认，严格引用图，干净无假阳性）**
- S2 仅作补充召回候选，**每条需独立核验**（查该论文 references 真含不含目标），不进默认路径
- `--citations-source` 默认值已从 `both` 改回 `openalex`（69148b9 之后的修正 commit）

**方法论教训**（S012 教训复发，记 profile）：核查机制必须应用到"内容真伪"层，不只是"条数对不对"。光数 36/31/43 就打 ✅ 是自审自验失效（M5）——拿到东西先验证内容再报结论，不报乐观估计。

## 调研问题

D017（D015 v2）把 cited-by 提到核心位置（步骤 2 默认 forward），但 S024 载波同步溯源执行时暴露 OPLL 锚 forward cited-by=0（当时归因"OpenAlex 未收录 2023 新文"）。本轮要回答：

1. 现有 `tools/` 有没有 cited-by 能力？接哪个 API？
2. S024 报的"forward=0"是数据源缺陷还是工具 bug？
3. S2 vs OpenAlex 覆盖差异？哪个做主源？
4. 召回失败时降级方案是什么？

## 发现

### 发现 1（最重要）：S024 的"OpenAlex forward=0"是工具 bug，不是数据源缺陷

**独立验证（主线 curl 实测，非 agent 传话，FR-26）**：

| 论文 | 年份 | `cites:DOI:{doi}`（现有工具写法） | `cites:W{work_id}`（OpenAlex 正确写法） | 论文自报 `cited_by_count` |
|------|------|----------------------------------|----------------------------------------|--------------------------|
| Paillier JLT（OPLL/载波同步锚） | 2020 | **None（空）** | **36** | 36 |
| TS-KF（LEO Doppler） | 2025 | **None（空）** | **4** | 4 |

**根因**：OpenAlex 的 `cites:` filter 只接受 **Work ID（`W...`）**，不接受 `DOI:` 前缀。传 `DOI:...` 进去**静默返回空**（不报错）。现有工具 `tools/litsearch/search_sources.py:1047` 写的是 `filter=cites:DOI:{doi}` —— 这就是 S024 报 forward=0 的真因。

**影响**：
- S024 当时归因"OpenAlex 未收录 2023 新文"是**误判**，实际 OpenAlex 对 Paillier(2020) + 新文(2024/2025) 都收录且 cited_by_count 非 0
- D017 v2 写的"cited-by 召回失败预案"前提（OpenAlex 对新文召回弱）**部分不成立** —— 召回不弱，是参数写错
- **工具修一行（L1047：先 DOI→W-ID 再 cites）就能让现有 OpenAlex forward cited-by 正常工作**

### 发现 2：现有工具已具备 cited-by 能力，无需新建

- `--citations {DOI}` flag 已存在（`literature_search.py` L111-151），direction 默认 **forward**（谁引用了，正是 v2 要的）
- 接 **OpenAlex**（`openalex_citations` 函数，`search_sources.py` L1015-1091），支持 forward/backward + depth 2 展开
- **S2 cited-by 接口 `get_s2_citations` 也已实现**（`search_sources.py` L164-206，调 `api.semanticscholar.org/graph/v1/paper/{id}/citations`），但**只用于 `--refs` 展开**（L279），**没有独立 CLI 入口**做纯 cited-by 拉取

### 发现 3：OpenAlex vs S2 是强互补关系（双源 union 才不漏）

子 agent 实测 4 个 DOI（Paillier2020 / TS-KF2025 / TWC2024 / sat.1553综述2025）的 forward cited-by 召回：

| 论文 | OpenAlex | S2 | 差异 |
|------|----------|----|------|
| Paillier 2020 | 36 | 31 | OA 多 5 |
| TS-KF 2025 | 4 | 4 | 持平 |
| TWC 2024 | 40 | 53 | S2 多 13 |
| sat.1553 综述 2025 | 2 | 5 | S2 多 3 |

**集合重叠（按标题归一化）**：TWC2024 交集 36，OA-only 4，S2-only **17** → 合并去重 57 条，**任一源单独用都漏 4-17 条**。两源互不包含（S2 独占多为预印本/会议扩展/非 IEEE 索引源，OA 独占多为 OA 期刊版）。

**S2 对新文/预印本召回系统性优于 OpenAlex**（自有爬虫 + arXiv 跟踪），但 OpenAlex 对老经典期刊索引更全。

### 发现 4：降级源评估（子 agent 调研）

| 源 | 免费 | 可集成 | 覆盖 | 评估 |
|----|------|--------|------|------|
| **OpenAlex**（现有） | ✅ 无限 | ✅ 已集成 | 期刊全，新文略滞后 | 修 bug 后即主源 |
| **S2 `/paper/{id}/citations`**（现有接口，未接 CLI） | ✅（无 key 限速，有 key 1 req/s） | ✅ 接口已有 | 新文/预印本强 | **应加 CLI 入口做第二主源** |
| **Lens.org Scholar API** | ✅ 5000 req/月 | ✅ token + curl | 含专利 | 推荐降级源 1 |
| SerpAPI（Google Scholar 封装） | ❌ 付费 ~$50/月 | ✅ | GS 最全 | 可选付费降级 |
| Google Scholar 自爬（scholarly/Playwright） | ✅ | ⚠️ blit 可改造 | 最全但反爬 24-48h 封 IP | **仅小批量人工核验**，不进管线（封 IP 连带影响同机其他源） |
| Crossref cited-by | ❌ 需 member 凭证 | — | — | 不可行（非 member） |
| Connected Papers / Inciteful / Litmaps | freemium | ❌ 无 API | 底层同 OpenAlex/S2 | 不用（无程序化 cited-by 列表 API） |

**学术引用网络分析的标准做法 = 多源融合**（2025 实证研究 PMC12621532 证实 S2 references 中位数高于 OpenAlex，两源互补已被多篇文献确认）。

## 结论

### 回答 4 个调研问题

1. **现有 cited-by 能力**：已具备。`--citations {DOI}` 接 OpenAlex forward/backward（修 bug 后正常），S2 接口已实现但没独立 CLI 入口。
2. **S024 forward=0 真因**：工具 bug（`cites:DOI:` 应为 `cites:W{id}`），**不是数据源缺陷**。OpenAlex 对 Paillier + 2024/2025 新文都收录且召回正常。
3. **主源选择**（⚠️ 2026-07-02 更正）：**OpenAlex 单源为主**（严格引用图干净）。S2 召回广但含假阳性（见顶部更正段），仅作补充且需逐条核验。原"双源 union 强互补"结论基于不充分验证，推翻。
4. **降级方案**：OpenAlex 不够时 → Lens.org（免费 5000/月）→ SerpAPI GS（付费可选）→ GS 自爬（仅人工核验）。S2 作"补充召回候选"但每条需核验。

### D017 v2 步骤 2 "cited-by 召回失败预案"修正建议

D017 原预案基于"OpenAlex 对新文召回弱"（发现 1 证伪），建议修正为：

**主路径（OpenAlex 单源）**：
1. **OpenAlex forward**（修 bug：`search_sources.py:1047` 改两步查 W-ID）——严格引用图，干净
2. 召回不足时才补 S2（每条核验）或关键词检索

**召回失败定义修正**：不是"OpenAlex 返回 0"（那可能是 bug），而是"**OpenAlex 返回 < 阈值**"（阈值待定，参考：老经典 >20，新文 >3 算正常）。

**降级触发**：OpenAlex < 阈值 → S2 补充（每条核验 references）→ Lens.org Scholar API（免费 5000/月）→ SerpAPI GS（付费小批量）→ 人工 GS 核验。

**新文特殊处理**：对 <1 年新文（OpenAlex 系统性滞后），用关键词检索补 + 作者团队追踪（S024 已用过的方式），慎用 S2（假阳性）。

## 对决策的影响

### 对 D017 的影响（需用户拍板是否修正）
D017 步骤 2"cited-by 召回失败预案"段的前提（OpenAlex 新文召回弱）被部分证伪。**核心结构不变**（单源主用 + 降级 + 召回失败预案），但：
- 召回失败的主因从"数据源不收"变为"工具 bug"（已修）+ 单源召回有限
- 预案第一动作从"降级换源"变为"**先修工具 bug（✅ 已修），OpenAlex 单源为主**"
- 降级源优先级：S2（核验后补充）> Lens.org > SerpAPI > GS 自爬

### 是否需新建 D###
**不需要**。本轮是工具调研（R### research note），不构成架构/方向决策。D017 核心结构不动，只是步骤 2 预案段的细化修正。修正建议报用户拍板，拍板后直接补进 D017 文本（或等载波同步 v2 实战时落地）。

### 工具修复（独立于 D017）
`tools/litsearch/search_sources.py:1047` 的 `cites:DOI:{doi}` bug 是确定性 bug（影响所有 `--citations` forward 调用），**建议本轮或下轮修**（一行改动：先 `filter=doi:{doi}` 查 W-ID，再 `filter=cites:{W-ID}`）。修复与方向决策无关，是工具维护。

## 验证证据

- OpenAlex cites filter bug：主线 curl 实测（2026-07-01），Paillier(2020) + TS-KF(2025) 两篇均复现 `cites:DOI:` 返空 / `cites:W{id}` 返正确数
- OpenAlex vs S2 召回对比：子 agent curl 实测 4 个 DOI
- **S2 假阳性核查**（2026-07-02 诚实核查，用户质疑触发）：抽 10 条查 references 真含不含 Paillier。OA-only/overlap 6/6 真；S2-only 4/4 查不到，其中 2019 ICSOS（2019-10）被 S2 算成引用 2020-08 Paillier，时间逻辑铁证假 cited-by。S2 `/paper/{id}/citations` 召回含"相关论文"非纯引用关系
- 降级源评估：子 agent WebSearch 调研（来源：serpapi.com / docs.api.lens.org / crossref.org/documentation/cited-by / PMC12621532 / connectedpapers.com/about）
