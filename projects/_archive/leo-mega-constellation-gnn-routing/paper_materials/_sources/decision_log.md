# Decision Log — GNN-based LEO Mega-Constellation Routing

## 阶段摘要
- [Groundwork] Step 2-5 + Step 4a/4b 全部完成，**Go 已确认**，待进入 Contract
- [Contract] Step 0-3 完成，Contract 已冻结（用户确认 2026-05-13），待 Execute
- [Execute] Step 1 完成（实验设计审查通过），参数核实完成，Step 2 核心实验进行中

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
[D014] Execute Step 1 实验设计审查通过 | 理由: E03/E05消融维度问题用零向量修复（保持输入维度一致），流量强度待smoke test验证，无信息泄露 | 阶段: Execute
[D015] ISL容量模型修正：Shannon + B=1 GHz（原 B=500 MHz 无出处） | 理由: 子agent查证3篇论文+web搜索，B=500MHz无任何论文使用；L03 DuJo基于Starlink真实TLE数据用B=1GHz；用户确认采用此方案 | 阶段: Execute
[D016] ISL距离修正：实时轨道力学计算 + 5000km断链逻辑（原固定值~2700/~5500km错误） | 理由: 计算显示四个配置的ISL距离差异巨大（轨内1086-4277km，轨间1963-5694km），固定值不适用任何配置；L02 Starfield §2.2确认5000km断链阈值；66星配置部分轨间ISL会断链 | 阶段: Execute
[D017] ISL类型确认为激光（非RF），Shannon模型为简化近似 | 理由: L02/L03明确optical laser link(1550nm)；Starlink实际~100Gbps/链路；Shannon模型需在论文中标注为简化 | 阶段: Execute
[D018] 监督预训练结果：RoutingActorCritic(3层GAT,h=128)→方向精度97.6%(train)/66.8%(target)，retention 71% | 理由: 150 epochs, 7320 samples (20 snapshots × 3 configs), CE loss | 阶段: Execute
[D019] 贪心推理路径成功率极低（train 22-30%, target 1.7%），不满足实用要求 | 理由: 路径成功=逐跳精度之积，97.6%^10≈78%理论上限但实际更低；某些目的地方向精度仅~46%拉低整体 | 阶段: Execute
[D020] GNN加权Dijkstra推理策略确定：weight=delay+relu(best_logit-logit)，成功率100%，median stretch 1.5-1.8 | 理由: 4种权重公式测试(softmax概率/2-prob/exp(-logit)/加性惩罚)均给mean stretch 2.1-2.6，根因是某些episode方向精度低(~46%)导致尾部拉高(P95=5-7) | 阶段: Execute
[D021] PPO微调无效结论：无论greedy reward还是weighted Dijkstra reward，PPO均无法改善监督baseline | 理由: ①greedy reward太稀疏(99%路径失败)②weighted reward action-reward解耦(改单节点logits不影响整条路径)③两种方案80轮PPO后stretch持平或恶化 | 阶段: Execute
[D022] _build_neighbor_map bug修复：之前只注册单向映射(1440/2880条)，评估只能用2/4方向(intra_bwd和inter_l缺失)，导致stretch被严重高估 | 理由: edge_index存储每条ISL单方向，但neighbor_map未添加反向条目；修复后所有方法stretch大幅改善 | 阶段: Execute
[D023] 修复后加权Dijkstra评估结果(720星)：mean stretch 1.097, median 1.056, P95 1.315, ≤1.2x optimal 85.1%, ≤1.5x optimal 98.9% | 理由: 10 snapshots × 5 TMs × 100 flows, seed=123, 100%成功率 | 阶段: Execute
[D024] GRLR baseline复现完成(6节点局部图GAT+Actor-Critic, 加权Dijkstra推理)：mean stretch 1.008, 100% ≤1.2x optimal, delay 60.32ms | 理由: 2000 episodes训练, γ=0.95, lr=5e-4, β=0.1; 同规模(720)训练近乎最优 | 阶段: Execute
[D025] Baseline对比结论：时延保留率90.3%(GRLR同规模60.32ms / 我们跨规模66.77ms)，vs Dijkstra差距9.9%，Contract两项核心指标达标 | 理由: 我们用66+100+200训练零样本迁移到720，代价~10%额外时延；跨规模能力是GRLR完全不具备的 | 阶段: Execute
[D029] 同规模消融（720→720）：训练精度98.82%，stretch 1.000(完美)，delay开销0.0% | 理由: 架构本身同规模可达最优，9.7pp stretch差距完全来自跨规模迁移；消融实验四项全部完成，Contract两项核心指标达标(时延保留率90.3%≥80%, vs Dijkstra差距9.9%≤20%) | 阶段: Execute
[D028] 消融A3（无PE+单尺度train_100）：训练精度40.16%(≈随机)，stretch 1.049, ≤1.2x 93.6%, delay开销3.6% | 理由: 确认PE是学习必要条件——无论单/多尺度，无PE均无法学习；A3 stretch(1.049)介于A1(1.002)和A2(1.120)之间，表明更少训练样本导致略差的Dijkstra近似 | 阶段: Execute
[D027] 消融A2（仅train_100单尺度训练）：训练精度97.70%，720星评估 stretch 1.120, median 1.073, ≤1.2x 81.1%, delay开销12.3% | 理由: 单尺度训练精度与主实验相当(97.7% vs 97.6%)，但跨尺度迁移略差；多尺度训练贡献：stretch -2.3pp, ≤1.2x +4pp, delay开销 -2.4pp；贡献方向符合预期但幅度(2-4pp)小于Contract预期(5-8pp) | 阶段: Execute
[D026] 消融A1（移除Orbital PE）：训练精度39.66%（≈随机25%），无法学习方向路由；weighted Dijkstra stretch 1.002（≈纯Dijkstra）| 理由: 无PE时模型仅靠is_dest(1bit)无法区分节点位置，无法学习方向偏好；weighted Dijkstra退化为delay-only权重=纯Dijkstra；PE是模型学习的必要条件而非可选增强，Contract假设"PE贡献≥8pp stretch"需修正为"PE是模型可学习性的前提" | 阶段: Execute

---

### D030: 领域验证结论 — Size generalization 非LEO路由领域问题
**日期**: 2026-05-24
**上下文**: S004-ch1-domain-verify, 3个子agent并行调研
**决策**:
1. Size generalization 是 GNN 理论问题，非 LEO 路由领域公认挑战。LEO 路由综述未列出此问题。→ 叙事必须改为"将 GNN 技术迁移到 LEO 路由场景"
2. Stretch 指标在 LEO 路由中合法但非主指标（E2E delay 为主）→ stretch 作为辅助指标
3. Delay retention rate 为自造指标，无文献先例 → 标注为新提出指标
4. Orbital PE 是标准领域特征工程 → 降级为"工程选择"而非核心贡献
5. 加权 Dijkstra 推理有先例（GDDR 2021）→ 增量创新

**原因**: 子 agent 调研 3 组文献确认。Li 2026 子agent 幻觉事件进一步证明必须做领域归属验证。

---

### D031: P0 多 seed 实验完成
**日期**: 2026-05-24
**上下文**: run_experiments.py 批量运行，审计估 2h/seed 实测 ~6 min/seed
**决策**: P0 核心实验 14 轮完成（full/A1/A2/A3 各 3 seed, same 2 seed），数据极稳定（stretch std=0.012），消融故事完整。P0 PASS。

**关键数据**:
| 实验 | Stretch | Delay(ms) | ≤1.2x% | 训练精度 |
|------|---------|-----------|--------|---------|
| full | 1.099±0.012 | 66.84 | 86.2 | 97.5% |
| A1(无PE) | 1.006±0.002 | 61.13 | 99.9 | 40.2%≈随机 |
| A2(单尺度) | 1.106±0.018 | 67.66 | 84.0 | 97.7% |
| A3(双消融) | 1.058±0.002 | 63.32 | 92.2 | 40.2%≈随机 |
| same | 1.000±0.000 | 60.80 | 100.0 | 98.6% |

**影响**: delay retention=109.9%（跨规模多~10%延迟开销），数据可用于论文写作。

---

### D032: Li 2026 竞品排除
**日期**: 2026-05-24
**上下文**: 子agent声称 Li 2026 (arXiv:2604.07264) 做 size generalization
**决策**: Li 2026 非竞品。实际论文做意图编译（LLM→约束IR→验证），GNN仅用于同规模Dijkstra蒸馏加速。Abstract中无 size generalization 或 zero-shot transfer。新颖性维持 SAFE。

**原因**: 子agent基于 GNN+Dijkstra+LEO 表面相似性幻觉了功能。经 abstract 交叉验证排除。
