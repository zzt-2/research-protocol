# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 3.5 完成 → Step 4a 可行性预判
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：Step 3 精读（10 篇 L01-L10）+ Step 3.5 定向补充（L11 TELGEN + 4 篇新竞品发现）

## 关键上下文

### TELGEN 改变项目定位（最重要）
**TELGEN (Zhou 2025, IEEE/ACM ToN)** 已将"GNN+TE+size generalization"做完整（20x 泛化, <3% gap）。
- 纯 size generalization for TE **不再是空白**
- 差异化**必须聚焦 LEO 时变拓扑**（TELGEN Section VI 明确列为 future work）
- 核心差异化：LEO 时变 TE + per-link 在线负载均衡 + DRL 在线适应（vs TELGEN 静态快照+SL）
- **风险**：如果无法在 LEO 时变维度建立足够贡献，审稿人会认为与 TELGEN 差异不足

### Step 3.5 新发现的高优先级论文

| 论文 | 路径 | 为什么重要 |
|------|------|-----------|
| **DeepLaDu** (Gu 2026) | papers/arxiv/2601.21921/content.md | GNN per-link congestion prices，与本研究 per-link 最接近。**已下载待精读** |
| ALIDT/ADRLRM (Gao 2025/2026) | 需下载 | STGNN 卫星路由，声称超越 GMR |
| GRL-RR (Bai 2025) | 需下载 | GNN+DRL LEO 弹性路由 |
| Fan 2026 TAES | 需用户手动（IEEE 付费墙） | GNN+RL 多路径流量拆分 |

### 缺失论文（需用户手动获取）
1. **GNN-ASSSP** (He 2026) — DOI: 10.1016/j.ast.2026.112361 (ScienceDirect)
2. **DLBR** (Ju 2025) — DOI: 10.1109/TAES.2025.3571400 (IEEE TAES)
3. **LARRI** (Ye 2026) — DOI: 10.1109/TON.2025.3607939 (IEEE ToN)
4. **FlexSATE** (Liu 2024) — DOI: 10.1109/GLOBECOM52923.2024.10901096 (IEEE GLOBECOM)
5. **Fan 2026 TAES** — DOI: 10.1109/TAES.2026.3652971 (IEEE TAES)

### 已有论文 content.md
- L01-L10：10 篇精读完成（literature_notes.md 含完整结构化提取）
- L11 TELGEN：papers/arxiv/2503.24203/content.md（精读完成）
- DeepLaDu：papers/arxiv/2601.21921/content.md（待精读）

### 检索结果
所有检索 JSON 在 search-archive/2026-05-16/ 下，新增：
- gin-graph-isomorphism-network-routing-load-balancing-scalabi.json
- gat-edge-features-per-link-traffic-splitting-congestion-rout.json
- mpnn-cross-topology-generalization-traffic-engineering-zero-.json

## 下一步
1. **精读 DeepLaDu**（arXiv:2601.21921）— 确认 per-link congestion price 机制与本研究差异
2. **用户手动获取缺失论文**（GNN-ASSSP 最重要 — 最直接竞品）
3. **Step 4a 可行性预判** — 读 `stages/gw-feasibility.md`，评估 TELGEN 竞品风险下的可行性
4. MVE 验证重点调整：GNN 在**时变拓扑**的拥塞聚合中是否优于 MLP（不仅仅是静态场景）

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md` — Master 编排状态
- `projects/leo-congestion-routing/literature_notes.md` — 文献笔记（L01-L11 + 综合分析 + 3.5 结果）
- `projects/leo-congestion-routing/decision_log.md` — 决策日志
