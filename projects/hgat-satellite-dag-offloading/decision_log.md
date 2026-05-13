# Decision Log

## 阶段摘要
- [Groundwork] Stage 1-6 完成，Stage 7（仿真器搭建+Baseline复现）待启动
- Stage 6 仿真器设计规格已确认，MinerU 参数提取已完成

## 决策记录

[D001] 方向定为 HGAT 增强卫星边缘 DAG 任务卸载 | 理由: 14 篇精读确认空白（无一同时具备卫星+DAG+真异构图注意力），K2/M01 同构 GraphSAGE 构成明确差异化锚点 | 阶段: GW

[D002] Stage 4 维度 A/B/C/E 评估通过，无致命信号 | 理由: (A) 共享参数在 30:1 计算比条件下有结构性信息损失，M09 type-specific V 投影 20.4% 提升为下界证据；(B) 空白原因为"没人想到"而非"试过不好"，M09+K2 两条独立证据链支撑可行性；(C) 仿真条件天然具备异构性信号；(E) 1/5 baseline 有代码但失败可兜底 | 阶段: GW

[D003][FEASIBILITY] 维度 D MVE 待执行——组合新颖性方向不可跳过最小验证 | 理由: M09 证据来自 UAV-UGV 2 类型场景，不能直接保证卫星 4+ 类型场景有效，需 toy experiment 验证 HGAT vs GraphSAGE | 阶段: GW

[D004] MVE 执行完毕，判定 PASS | 理由: HGAT vs GraphSAGE 在 5 节点卫星 DAG 场景中，HGAT 4/5 种子更优，平均改善 +10.7%，3/5 种子 ≥5% 改善 | 阶段: GW

[D005][FEASIBILITY] Go 决策 | 理由: 五维度全部通过（A 结构优势+B 新颖性可行+C 仿真条件+E 风险可控），MVE PASS 确认核心假设成立，用户已确认 | 阶段: GW

[D006][BASELINE] 选定 B1=K2/M01 AMAPPO+GraphSAGE, B2=K3 GDRL(GCN+TRPO简化) | 理由: B1 为最直接竞争者（卫星+DAG+同构GNN），B2 为 JSAC 顶刊+未来工作延续叙事链+GCN对比；K3 砍掉 MAML 元学习（与对比目标无关），简化后 ~2 天实现；共识 baseline PPO(5篇)/DDPG(3篇)/Random/Greedy 标准实现 | 阶段: GW

[D007][AUTO] M07 CachOf 代码仅用于管线验证，不作正式 baseline | 理由: 场景差异大（地面MEC+缓存），不适合直接数值对比；M08/M03 视时间追加 | 阶段: GW

[D008][PARAM] MinerU 高质量转换提取 K2/M01 Table III + M06 Table III/IV + DAG 参数 | 理由: pymupdf4llm fast 模式将 IEEE 付费 PDF 内嵌表格/公式渲染为 picture omit，MinerU standard 模式成功恢复 HTML 表格。K2/M01 Table III 完整提取（26 项参数），M06 HGAT 超参确认（4头2层 c₁=0.5 c₂=0.01 GAE λ=0.98），M06 DAG 参数确认（fat=0.6 density=0.4 regular=0.9），M08 权重确认 w_d=w_e=0.5 | 阶段: GW

[D009][PARAM] η_t/η_e/λ₁-λ₅ 权重论文未披露，采用默认值+MDP 试运行验证 | 理由: K2/M01 eq.52 定义 r=-η_t·T-η_e·E-Σλ_ι·Φ_ι 但 Table III 不含权重值，正文亦无提及。M06 w_T/w_E 同样未披露。默认 η_t=0.5 η_e=0.5（参考 M08 实验最优设置），λ₁=10 λ₂=5 λ₃=5（延迟违反惩罚最重），待 Part A-checkpoint MDP 试运行验证量级平衡 | 阶段: GW

[D010][PARAM] Rician K 因子 ξ 采用 3GPP TR 38.811 默认值 K=2 | 理由: K2/M01 G2U 链路模型定义 Rician 衰落但未给 ξ 数值，Table III 亦不含此参数。3GPP TR 38.811 给出地面-低空链路典型 K=2~5，取保守下界 | 阶段: GW

[D011][REWARD] η_t 从 0.5 调至 5.0，E_max 改用全节点类型 max(κ×f²) | 理由: Part A-checkpoint 显示初始权重下 E_norm 占 97.9%（η_t=0.5 vs η_e=0.5），原因：(1) E_max 仅用 IoTD κ×f²=3.2 但 CS 为 10.0 导致 E_norm>1.0；(2) T_norm 分母 mean_deadline≈55s >> 实际任务时间 ~0.2s。修复后 checkpoint 3/3 gate 通过：greedy η_t·T_norm=40.2% vs η_e·E_norm=59.8% | 阶段: GW-Stage7

[D012][BASELINE] 统一 PPO backbone，只换 encoder | 理由: B1(K2/M01 AMAPPO)简化为单 agent PPO+GraphSAGE，B2(K3 GDRL)简化为 PPO+GCN；AMAPPO 多智能体和 TRPO 二阶优化与对比目标（异构 vs 同构 GNN）无关，统一后差异来源唯一。对比表：Ours=HGAT+PPO, B1=GraphSAGE+PPO, B2=GCN+PPO, Random, Greedy(SPT) | 阶段: GW-Stage7
