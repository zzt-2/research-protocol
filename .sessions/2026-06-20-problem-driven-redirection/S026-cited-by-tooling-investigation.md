# [S026] Cited-by 召回工具调研（H016 路径 B 执行）

> 2026-07-01 | GW Step 4a 暂挂（工具调研） | 状态：完成，待用户拍板预案
> 来源：执行 H016 路径 B

## 目标

执行 H016 路径 B：核查 tools/ cited-by 接口现状 + 评估 Semantic Scholar/OpenAlex/Google Scholar 召回 + 产出 D017 v2 步骤 2"召回失败预案"具体落地建议。工具就绪后路径 A（载波同步 v2 重做）更顺。

**纪律**：工具调研不立 Q#，不改 D017 核心（只补步骤 2 预案段），web search 全在子 agent。

## 记录

### 五步执行

**① 报到 + H016 接收验证**：topic-index 不变量 8 条 + _registry depends_on（4b1 + thesis-method-redirection，conflicts_with 空）+ 4 条关键事实核查全 PASS（D017 存在 L1104 / D015 v1 superseded L967 / sat.1553 L440-L558-L788 open problem 真实 / D006 排除边界 L319-345）。inflation check S###=22（≥15 触发，但本轮 = D017 既定收尾延续非范围扩张，如实标注不阻断）。用户拍板走路径 B。

**② 本地核查 tools/ 现状（主线程直接读）**：读 `tools-guide.md` + `tools/litsearch/search_sources.py` + `tools/literature_search.py`。发现：
- `--citations {DOI}` flag 已存在（L111-151），direction 默认 **forward**，接 **OpenAlex**（`openalex_citations` L1015-1091）
- **S2 cited-by 接口 `get_s2_citations` 也已实现**（L164-206），但**只用于 `--refs` 展开**（L279），**没独立 CLI 入口**
- OpenAlex forward 用 `filter=cites:DOI:{doi}`（L1047）—— 这写法是 bug（见发现 ④）

**③ 派 2 子 agent 并行**（web 验证必须子 agent，AGENTS.md）：
- **Agent 1**（实测 OpenAlex vs S2 召回）：4 DOI 实测，发现 OpenAlex 新文召回正常（非 S024 报的 0），S2 新文更强，两源强互补
- **Agent 2**（降级源 + 最佳实践调研）：GS 无官方 API/反爬 24-48h 封 IP/Lens.org 免费 5000/月可集成/Crossref 需 member 凭证/Connected Papers 等底层同 OpenAlex+S2 无程序化 API

**④ 🔴 独立验证 Agent 1 关键声称（FR-26，主线 curl 实测）**：
Agent 1 报"S024 的 OpenAlex forward=0 是 `cites:DOI:` 写法 bug 不是数据源缺陷"。**主线 curl 复现验证**：
- `cites:DOI:10.1109/jlt.2020.3003561`（Paillier，现有工具写法）→ `meta.count = None`（空）
- `cites:W2990621879`（先查 Work ID 再 cites）→ `meta.count = 36`（与论文 cited_by_count 一致）
- TS-KF(2025) 同样：`cites:DOI:` = None，`cites:W4410339711` = 4
- **确认**：OpenAlex `cites:` filter 只接 Work ID(`W...`)不接 `DOI:`，传 DOI 静默返空。`search_sources.py:1047` 这一行 bug 就是 S024 报 forward=0 的真因。**OpenAlex 对 Paillier(2020)+新文(2024/2025) 全收录**，"OpenAlex 未收录 2023 新文"是误判

**⑤ 产出 R003 + 预案建议**：写 `R003-cited-by-tooling-investigation.md`（工具现状报告 + D017 步骤 2 预案修正建议）。

### 核心发现（R003 详述）

| # | 发现 | 影响 |
|---|------|------|
| 1 | **S024 forward=0 是工具 bug（cites:DOI: 应为 cites:W{id}），非数据源缺陷** | D017 预案前提部分证伪；OpenAlex 修一行就正常 |
| 2 | cited-by 能力已具备（--citations flag + OpenAlex + S2 接口） | 不需新建工具，修 bug + 加 S2 CLI 入口即可 |
| 3 | OpenAlex vs S2 强互补（TWC2024 漏 4-17 条/单源） | **双源 union 才不漏**，不是单选 |
| 4 | 降级优先级：Lens.org(免费5000/月) > SerpAPI GS(付费) > GS自爬(仅人工) | GS 反爬 24-48h 封 IP 不进管线 |

### D017 步骤 2 预案修正建议（报用户拍板）

- 召回失败主因：从"数据源不收"→"**工具 bug + 单源局限**"
- 主路径：**双源 union**（OpenAlex 修 bug + S2 加 CLI 入口）
- 召回失败定义：从"OpenAlex 返 0"→"**双源 union 后仍 < 阈值**"（老经典 >20，新文 >3）
- 降级：Lens.org → SerpAPI → GS 人工

## 决策引用

- 无新建 D###（工具调研非架构/方向决策）
- D017 步骤 2 预案段建议修正（待用户拍板，拍板后补 D017 文本）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。H016 路径 B 明确范围（工具调研不立 Q# 不改 D017 核心），未触及"明确不含"

## 后续

1. **用户拍板**：D017 步骤 2 预案修正建议接受 / 调整 / 拒绝
2. **工具修复**（独立于方向决策）：`search_sources.py:1047` cites bug + 加 S2 cited-by CLI 入口 —— 建议修（一行 + 一个 wrapper 函数），但本轮**不擅自改**（守 H016"工具调研"边界 + 代码改动最好用户确认）
3. **路径 A（载波同步 v2 重做）**：工具就绪后按 D017 v2 流程重跑（扫描层 → 穷举门控 A → 判读层）。H016 建议路径 B 完成后走路径 A
4. **可选**：载波同步 v2 重做时验证双源 union 召回（实战检验预案有效性）

**未决项**：召回阈值（老经典 >20 / 新文 >3）是建议值，待载波同步 v2 实战校准。
