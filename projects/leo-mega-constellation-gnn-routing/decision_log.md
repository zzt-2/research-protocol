# Decision Log — GNN-based LEO Mega-Constellation Routing

## 阶段摘要
- [Groundwork] Step 2-5 + Step 4a/4b 全部完成，**Go 已确认**，待进入 Contract
- [Contract] Step 0-3 完成，Contract 已冻结（用户确认 2026-05-13），待 Execute
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
[D009] Step 4b 决策建议：Go | 理由: C仿真条件可行(异质性需注意但无致命障碍)，D已通过MVE(83-87%保持率)，E资源风险比例合理(有3个可回收产出路径) | 阶段: GW
[D010] Contract Step 0 新颖性确认：4组关键词检索+3篇精读+2组定向检索，GNN size generalization for LEO satellite routing 仍为空白 | 理由: 最接近竞争者TELGEN(IEEE/TON'25)做WAN TE不做卫星路由；Size Transferability(arXiv'26)提供PE理论但做Graph Transformer非GNN路由；Scaling Swarm(AI'25)确认零样本迁移可行但仅3x简单场景 | 阶段: Contract
[D011] TELGEN威胁评估：中等，可差异化 | 理由: ①TELGEN做TE(LP流量拆分)非路由(每跳决策) ②WAN非卫星 ③无位置编码 ④无动态拓扑 ⑤最大测试5K节点非mega-constellation | 阶段: Contract
[D012] 假设确定：GNN+Orbital PE+多尺度训练，66→720(11x)零样本泛化，保留率≥80% | 理由: MVE 83-87%保持率校准，PE贡献≥8pp为技术创新证据 | 阶段: Contract
[D013] Contract冻结，用户确认通过 | 理由: 压力测试4问无致命信号，Baseline共识性强 | 阶段: Contract
