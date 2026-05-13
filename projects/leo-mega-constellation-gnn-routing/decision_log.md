# Decision Log — GNN-based LEO Mega-Constellation Routing

## 阶段摘要
- [Groundwork] Step 2-3 完成；Step 3.5 补充检索完成（25篇+63篇引用链）；Step 4a Go 已确认；MVE 完成（83-87%保持率）；Step 5 Baseline 已选定
- [Contract] 待定
- [Execute] 待定

## 决策记录
[D001] 选定方向：GNN-based routing for LEO mega-constellation | 理由: 蓝海（5年~38篇）、与导师ISL方向吻合、GNN天然适配图结构、仿真负担轻 | 阶段: GW
[D002] 项目目录：leo-mega-constellation-gnn-routing | 理由: 描述性命名 | 阶段: GW
[D003] 创新点重新定位：从"GNN+RL for LEO routing"调整为"GNN size generalization for satellite routing" | 理由: Step 3.5 发现6篇GNN+RL LEO竞争对手（L13-L18），但无一涉及size generalization；"GNN+RL LEO路由"不再是创新点 | 阶段: GW
[D004] GRLR size generalization 声明为AI幻觉 | 理由: Web搜索多次声称GRLR涉及size generalization，但Semantic Scholar API验证TVT 2025和ICCC 2023双版摘要均无提及 | 阶段: GW
[D005][AUTO] Step 4a 决策建议：Go | 理由: 维度A结构优势明确，维度B新颖性确凿+可行性有强论据，无致命信号 | 阶段: GW
[D006] Step 3.5 补充检索完成：25篇论文+63篇引用链确认size generalization空白 | 理由: 6维度覆盖，ML理论基础（ICML 2024 T01 + NeurIPS 2025 T02）坚实 | 阶段: GW
[D007] MVE结果：GNN路由策略规模无关（83-87%保持率），支持Go | 理由: 均匀权重100%同规模→83%跨16x；异质权重70%同规模→56%跨16x；17%跨规模退化有改善路径 | 阶段: GW
[D008] Baseline选定：Dijkstra(必须) + GRLR复现(必须) + GraphPR(推荐) | 理由: Dijkstra为领域共识(19篇+田野15/40)；GRLR 44引用为GNN+RL标杆，同架构对比确保结论干净 | 阶段: GW
