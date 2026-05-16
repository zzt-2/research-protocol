# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 2 完成 → Step 3 精读
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：Step 1 检索+初筛、Step 2 论文获取、gw-acquire.md + tools-scenarios.md 修复（blit IEEE 下载 fallback）

## 关键上下文

### 项目定位
第三研究方向候选：**GNN 拥塞感知路由 + 负载均衡** for LEO 卫星星座。
核心命题：利用 GNN 消息传递聚合全局链路负载/队列深度信息，做 per-link 负载均衡路由决策。
Thesis 三章一致性：路由(Ch1) → 切换(Ch2) → 流量工程(Ch3)，共享 GNN size generalization 框架。

### 核心风险
**[高] GNN ≈ MLP 风险**：leo-resilient-routing MVE 两次证明"GNN 消息传递在路由决策维度不优于 MLP+手工特征"。新方向的赌注是拥塞/负载信息的全局聚合不同于纯拓扑路由，GNN 有结构性优势。Step 4a MVE 必须优先验证此假设。

### Step 1 检索结果
- 87 条去重候选（必读15/建议读20/待确认6/备选9/排除37）
- R1: 7 个 JSON，R2: 2 个定向检索（size gen × TE, GNN congestion 方法论）
- 核心空白确认：GNN + 拥塞感知路由 + LEO 有论文但无 per-link 负载均衡竞品
- Size generalization × 拥塞路由交叉完全真空（潜在核心贡献）

### Step 2 已获取论文（10 篇）

必读（7 篇已获取）：
| 论文 | 路径 | 行数 |
|------|------|------|
| GRLR (Zhang 2025, TVT, 44cit) | papers/doi/10.1109_tvt.2024.3471658/content.md | 566 |
| GMR (Huang 2024, TVT, 41-45cit) | papers/doi/10.1109_tvt.2023.3333848/content.md | 660 |
| POMAP (Li 2025, IoT Journal) | papers/doi/10.1109_jiot.2025.3610772/content.md | 838 |
| PathGNN (Ye 2025, JSAC) | papers/doi/10.1109_jsac.2025.3528815/content.md | 608 |
| GDRL-SFCR (Chen 2025, Sensors) | papers/doi/10.3390_s25041232/content.md | — |
| Fan 2026 GNN+DQN LB (Springer) | papers/doi/10.1007_s44163-026-01073-x/content.md | — |
| DTAR (Zhou 2026, arXiv) | papers/arxiv/2604.12382/content.md | — |

待确认/建议读（3 篇）：
| 论文 | 路径 |
|------|------|
| PRIMAL (He 2025, arXiv) | papers/arxiv/2510.27506/content.md |
| QueueMARL (Liaq 2026, arXiv) | papers/arxiv/2605.04448/content.md |
| ST-QoS (Chou 2026, arXiv) | papers/arxiv/2605.02413/content.md |

### 仍缺失（5 篇，需用户手动获取）
| 论文 | DOI/来源 | 为什么重要 |
|------|----------|-----------|
| **GNN-ASSSP** (He 2026) | 10.1016/j.ast.2026.112361 (ScienceDirect) | 最直接竞品，GAT+Transformer |
| **DLBR** (Ju 2025, 12-16cit) | 10.1109/TAES.2025.3571400 (IEEE TAES) | GCN+LSTM+DRL 负载均衡 |
| **LARRI** (Ye 2026) | 10.1109/TON.2025.3607939 (IEEE ToN) | GNN adaptive range routing |
| **FlexSATE** (Liu 2024) | 10.1109/GLOBECOM52923.2024.10901096 | distributed TE+supervised |
| **CA-GAR** (Liu 2026) | 10.3390/sym18050719 (MDPI OA, 下载失败) | GAT congestion routing 方法论 |

### 搜索结果 JSON 文件
所有检索结果在 search-archive/2026-05-16/ 下，关键文件：
- gnn-congestion-aware-routing-leo-satellite.json（R1 核心搜索）
- graph-neural-network-load-balancing-traffic-engineering-sate.json（R1）
- gnn-congestion-aware-adaptive-routing-dynamic-topology-link-.json（R2）
- graph-neural-network-size-generalization-traffic-engineering.json（R2）

## 下一步
1. **读框架文件** `stages/gw-read.md`（Step 3 精读规范）
2. **派子 agent 逐篇精读** 10 篇已获取论文，按 gw-read 模板提取结构化数据
3. **补充缺失论文**：用户手动获取 GNN-ASSSP 等 5 篇（放入 papers/manual/ 或 blit 重试）
4. 精读完成后更新 literature_notes.md（含 2-3 篇标杆论文写作架构提取）
5. Step 3 完成后进入 Step 3.5（定向补充检索）

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md` — Master 编排状态
- `projects/leo-congestion-routing/literature_notes.md` — 文献笔记（含步骤进度表）
- `projects/leo-congestion-routing/decision_log.md` — 决策日志
- `projects-overview.md` — 全局项目状态（已更新）
- `directions-registry.md` — 方向注册表（已更新）
