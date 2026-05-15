# Handoff 2026-05-13 (Final)

## 当前进度
- **阶段：Groundwork 全部完成，进入 Contract**
- 状态：Step 2-5 + Step 4a/4b 全部 Go

## Groundwork 产出摘要

### 方向
GNN size generalization for LEO mega-constellation routing — 在小星座上训练 GNN 路由模型，零样本泛化到大星座。

### 创新点定位
- 初始："GNN+RL for LEO routing"（Step 2-3 初期）
- 最终："GNN size generalization for satellite routing"（Step 3.5 后重新定位）
- 原因：发现 13 篇 GNN+RL LEO 竞争者（L13-L25），无一涉及跨规模泛化

### 核心数据
- 文献覆盖：25 篇论文 + 2 篇理论背景 + 63 篇引用链筛查 → size generalization **完全空白**
- 理论支撑：ICML 2024 解耦表示学习（T01）、NeurIPS 2025 统一理论框架（T02）
- MVE：均匀权重 100%→83%（跨16x），异质权重 70%→56%（80%保持率）
- Baseline：Dijkstra(必须) + GRLR复现(必须，TVT 2025, 44引用) + GraphPR(推荐)

### 关键教训
- Web 搜索声称 GRLR 涉及 size generalization 系 AI 幻觉（已通过 Semantic Scholar API 双版摘要验证纠正）
- Surrey 论文引言"GNN generalize over graphs of different sizes"是通用性质描述非实验贡献
- MVE 70% 同规模天花板是感受野限制（非规模问题），加深 GNN 无帮助（过度平滑）
- "过于平滑"风险：仿真必须包含异质 ISL 质量和非均匀流量

## 文件索引
- 项目目录：`projects/leo-mega-constellation-gnn-routing/`
- 精读产出：`literature_notes.md`（~720 行，L01-L25 + T01-T02）
- 可行性报告：`feasibility_report.md`（维度 A-E 完整）
- 决策日志：`decision_log.md`（D001-D009）
- MVE 脚本：`mve/mve_size_gen.py`
- 交接文件：`sessions/2026-05-13-handoff.md`
- 检索存档：`search-archive/2026-05-13/` 下 15+ JSON 文件

## 下一步：Contract 阶段
1. 读 `stages/contract.md` 按步骤执行
2. 设计仿真器（参考 literature_notes.md 仿真工具链分析）
3. 复现 GRLR（GNN + Actor-Critic，Walker-Delta）
4. 实现 size generalization 技术（位置编码、多尺度混合训练）
5. 实验方案设计
