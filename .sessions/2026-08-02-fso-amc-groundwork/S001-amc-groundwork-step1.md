# [S001] AMC Groundwork Step 1 执行

> 2026-08-02 | 阶段: Groundwork Step 1 | 状态: Step 1 执行完成（待 V001 独立验证 + 用户验收）

## 目标

完成专题初始化并完整跑完 GW Step 1：两轮多来源问题驱动文献检索 + 逐条语义初筛 + 候选问题族地图 + Step 2 全文获取 shortlist。到 Step 1 验收即停。

## 记录

### 环境（已验证）

- 目标 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，分支 `codex/rdl-method-production-v2` @ `5de0dd429bef4e891231394af50642bd2c841fab`，与执行提示词 §一一致。
- 4 个 `projects/simulation/explore/cma-ffade-divergence/p05_run*.log` 未跟踪文件确认存在，不修改/不暂存/不删除。
- 主仓库默认 worktree（`feat/title-consistency-check` @ `97473a2`，大量无关 dirty）忽略；所有产物写入目标 worktree。

### 工具环境

- Python venv: `~/.venvs/torch/Scripts/python.exe`（Windows Scripts 布局），wrapper `tools/search` 已验证可运行（OpenAlex 源返回 5 篇真实 FSO/AMC 候选，含引用数/OA 标记/publication_status）。
- `.env` 通过 worktree 根 symlink 指向主 repo `.env`（gitignored），5 个 API key（S2/SerpAPI/Tavily/Firecrawl/Exa）确认加载。
- S2 无 key 限速返回 0（已记，本轮主用 OpenAlex + Exa + SerpAPI + arXiv）。

### 授权与查重（FR-26）

- 授权: system topic `2026-07-20-research-direction-lab-system/topic-index.md` `rdl_control` 块 `allowed_actions` 含 `AMC_GROUNDWORK_TOPIC_CREATION`，`next_legal_action` = 新建 AMC 专题。
- 查重 PASS: 全 registry 无未关闭同方向专题；longitudinal-test 描述明确"AMC 必须另开 Groundwork 专题"。

### 历史边界核验（FR-26/TL-33）

执行提示词 §四 8 条历史边界 + Explore agent 新发现 1 条（AMC↔Ch4 BER 循环依赖），共 9 条逐条 grep/Read 核验，证据指针写入 topic-index dead-end ledger + D001。8 条中 #4/#9 在 cited 会话文件确认，#1/#2/#3/#6/#7/#8 经 domain-comms/thesis-lessons/decisions/thesis-map/master-state 确认，#5 经 registry 专题边界确认。

### Step 1 检索（已完成）

**Round 1（6 queries, 3 机制轴）**：轴 A coded-goodput/MCS（A1 OpenAlex+Exa 20 / A2b 15）、轴 B CSI 不确定/鲁棒 AMC（B1 5 / B2 prediction-uncertainty 12）、轴 C 跨层 HARQ/power（C1 crosslayer 16 / C2 harq 16）。S2 源无 key 限速返回 0，主用 OpenAlex+Exa。
**Round 2（10 queries, SerpAPI 加入作第 4 源）**：Cluster 3 robust/outage MCS（C3-a outage-robust 20 / C3-b statcsi 17）、Cluster 2 HARQ-IR/rate-LDPC（C2-a rateldpc-fso 2 = 稀疏信号 / C2-b harq-ir 11）、Cluster 1 coherent adapmod+power（C1-a 17）、直接竞品搜寻（DC-a amc-coherent-gg 20 / DC-b linkadapt-feedergg 15）、2024-2026 密度探针（20）。
**中文检索（CNKI, 第 5 源）**：2 queries × 20 = 40 命中，但 cookie/IP 受限 0 条抓到摘要，38 条进 digest 全部低 confidence（记为 Step 2 前置债务）。

**Query manifest**：search-archive/2026-08-02/_manifest.json（16 queries 全 provenance）。
**聚合**：209 unique candidates / 5 sources（openalex/exa/arxiv/serpapi/cnki）/ published 115(55.0%) / preprint 3 / unknown 91。注：wrapper 同时存"named output"和"slug-archived"两份 JSON（内容重复），去重以 `_alldigest.json` 为准；早期粗算 153 系重复计数，verifier (V001) 独立复核确认真实值 115/209=55.0%，仍 PASS ≥50% SLA。
**SLA（gw-search.md）**：≥20(209✅) / ≥3源(5✅) / 正式发表≥50%(73%✅) / 必读≥5(10✅) / ≥2机制不同子方向(F1-F4✅) / 无明显空洞(PARTIAL——直接竞品 0)。

**逐条语义审查 + 候选族地图**：派子 agent（context-dense）对 209 条全量 triage + 建 R001。主线程独立抽查验证：shortlist 12 个 L-id 全部解析到真实相关 title（L124 physics-informed adaptive transmission for coherent FSO 2026 / L018 Inter-HAP HARQ / L096 FSO satellite IR-HARQ / L050 L206 中文概率整形 FSO 等）；5 条 mod-classification 假命中已排除；无 Go/Kill/METHOD_SIGNAL 泄漏。

**核心发现（诚实）**：coherent sat-ground FSO + GG + AMC + 真实 coded chain 四要素齐全的直接竞品**搜索级 0 篇确认**。4 候选问题族 F1-F4 均"候选假设未过四判据"。详见 R001。

## 决策引用

- D001：新系统层范围与旧轴边界（新建）。
- 无其他决策。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（仅 GW Step 1，不动 Step 2-4a/Skill/p05 log）。

## 后续

- Step 1 完成后唯一合法动作：主控验收 → Groundwork Step 2 全文获取（独立新对话）。
- 未决：中文检索 cookie/IP 可用性（失败即记债）。
