# Decision Log

## 阶段摘要
- [Groundwork] Stage 7 完成。4 模型 × 3 seed 全部收敛但 peak 性能相当（-11.6~-12.0），HGAT 仅训练稳定性领先。零样本泛化测试（10→50 IoTD）GCN(-79) 优于 HGAT(-118)，核心假设被推翻。方向待评估。
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

[D013][BUGFIX] PPO 训练 mask 时序错误 + reward normalizer 失效 | 理由: (1) run.py buf.add() 存了 env.step() 之后的 action_mask（下一步的），导致 PPO evaluate 时选中动作被误判无效，KL 爆到 99M；修复为存 step 前的 mask。(2) 跨 episode Welford 归一化器处理不了双峰分布（好 -35 vs 坏 -267K），关闭后改用 PPO 内部 advantage 归一化。 | 阶段: GW-Stage7

[D014][ARCH] policy head 从 Linear(64,4600) 改为 bilinear scoring | 理由: mean pool 丢失 per-node 信息，4600 维 logit 无法学习 (task,node) pair 级别决策。改为 task_proj(task_embs) @ node_proj(node_embs).T → [200×23] logits。参数从 394K→99K，KL 从 99M→0.057。 | 阶段: GW-Stage7

[D015][REWARD] per-step reward 加 log1p 变换 | 理由: 原始 t_norm=(compute+transfer)/deadline 无上界，单步最差 -281K vs 最优 -0.01（7 阶量级差），PPO 无法学习。log1p 变换后范围 [-215, -0.02]，random/greedy 比例从 15000x 降到 146x。episode penalty 同样加 log1p。 | 阶段: GW-Stage7

[D016][PARAM] lr 5e-4→3e-4, entropy 0.05→0.01, patience 50→100 | 理由: bilinear 架构收敛稳定后，降低探索噪声和更新幅度以稳定策略。patience 增大避免过早停止。 | 阶段: GW-Stage7

[D017][RESULT] HGAT 3 seed 收敛，best -11.8 超越 greedy(-16.7) | 理由: seed=42 best=-11.6 median=-13.0; seed=123 best=-12.0 median=-17.9; seed=456 best=-11.8 median=-13.2。3 seed avg best=-11.8, avg median=-14.7。GraphSAGE/GCN/MLP 因 KL 问题训练不稳定（homo 模型 hetero→homo 转换丢失类型信息），待修。 | 阶段: GW-Stage7

[D018][ARCH] homo 模型加 type_bias(GNN前) + type_proj(GNN后) 双层类型信息保护 | 理由: 仅放 KL 阈值(1.0) + 降 lr(1e-4) 仍 KL=1.27 在 ep3 爆炸。根因：homo message passing 完全丢失类型边界，bilinear scoring 不稳定。type_bias 在 GNN 前注入可学习类型偏置，type_proj 在 GNN 后用 per-type 线性恢复类型表示。 | 阶段: GW-Stage7

[D019][RESULT] 4 模型全部收敛，best reward 相当，HGAT 稳定性大幅领先 | 理由: HGAT lr=3e-4 标准超参 avg_best=-11.79 avg_mean=-138。Homo 模型需 lr=5e-5 + KL=1.0 + ppo_epochs=2 特殊调参：GraphSAGE avg_best=-11.83 avg_mean=-219; GCN avg_best=-11.67 avg_mean=-289; MLP avg_best=-11.70 avg_mean=-331。Peak 性能接近但训练稳定性差异显著（HGAT mean 是 MLP 的 2.4x）。 | 阶段: GW-Stage7

[D020][RESULT] 零样本泛化测试 HGAT 假设被推翻 | 理由: 10→50 IoTD 零样本评估(20ep)：GCN=-79 优于 HGAT=-118，GraphSAGE=-810，MLP=-1365。HGAT 在每个规模都差于 GCN，泛化优势不成立。GCN 的谱卷积产生更平滑 embedding 反而泛化更好，HGAT attention 在大图上方差极高(std≈100 vs GCN<1)。方向待评估是否继续。 | 阶段: GW-Stage7
