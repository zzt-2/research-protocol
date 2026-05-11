# Decision Log

## 阶段摘要
- [Groundwork] Step 1-7 全部完成（仿真器验证通过，B1-B4 实现并验证）
- [Contract] 待开始
- [Execute] 待开始

## 决策记录

[D001] 搜索策略：4 角度（timing/trigger, selection, mobility management, heuristic）覆盖 DRL+传统两条路线 | 理由: 上次只搜 DRL 单一角度导致路线覆盖不足 | 阶段: GW

[D002][AUTO] 搜索结果 97 条，质量门槛全通过（≥20条、≥5必读、≥2路线、≥3源）| 理由: 多角度搜索效果显著

[D003] 下载止损：两轮后 3/15 成功，OA 论文也失败（网络连通性问题）| 理由: 框架止损规则 | 阶段: GW

[D004] 用户手动补充 7 篇 PDF（Bipartite Graph, HRL, ETRI, TOPSIS, Markov SA, GNN, Orbit Aware）| 理由: 弥补传统方法路线覆盖缺口 | 阶段: GW

[D005] Baseline 选定：B1=HHS(传统启发式 SOTA), B2=Dueling DDQN(DRL baseline), B3=Random(下界) | 理由: HHS 归一化到[0,1]解决奖励失衡、Dueling DDQN 是领域共识 DRL baseline、用户确认 | 阶段: GW

[D06][AUTO] 精读 16 篇论文（9 自动下载 + 7 用户手动），含 L01-L16 完整实现关键细节 | 理由: 覆盖 DRL(8篇)+传统(6篇)+Survey(2篇) 三条路线

[D07][CHANGE-PROPOSAL] L02(Dueling DDQN) 的 rate 未归一化（Mbps 直接用），复现时需归一化到[0,1] | 理由: 上次 F5 因 rate~10^6 占奖励 99.99% 导致 DRL 退化为贪心 | 影响: B2 baseline 复现需修正奖励函数 | 用户决定: 待确认

[D08][CHANGE] Step 5 仿真器设计：Starlink 1584 星 550km，Ku 12GHz 250MHz，最小仰角 20°，决策间隔 10s | 理由: L07/L08/L10/L11/L15 共识配置 | 阶段: GW

[D09][CHANGE] 奖励函数 v2：r = 0.6·R_norm + 0.4·L_norm - 0.5·B - 0.1·H，SINR_max=22dB | 理由: v1 稳态 R_norm 占比 85%（cherry-picking 分析），w_r 降至 0.6 使负载项有竞争力 | 影响: B2/B3 均使用此奖励 | 阶段: GW

[D10][CHANGE] Baseline 调整：B3 从 Random 改为 PPO（双 DRL baseline 降低风险），Random 降为 B4 | 理由: 单 DRL baseline 无法区分算法问题 vs 环境/奖励问题；PPO 与 DDQN 属不同范式 | 阶段: GW

[D11][CHANGE] B（阻塞）定义：仅当 ρ_target ≥ 1（选中满载卫星）时 B=1，与 L_norm 互斥 | 理由: 消除 B 与 L_norm 的重复惩罚 | 阶段: GW

[D12][CHANGE] SINR_max 从 30dB 降至 22dB | 理由: L08 实测 Starlink SINR 8-12dB，30dB 压缩梯度信号 | 阶段: GW

## 关键发现（影响后续步骤）

1. **奖励归一化是核心风险**：L02 rate 未归一化(F5根因)，L08 HHS 三项全归一化到[0,1](最佳实践)，L05 rate 低于阈值置零(非[0,1])
2. **观测空间差异大**：L05 仅 2 维({t, prev_sat})，L06 数十维(SNR+位置)，需统一
3. **动作空间共识**：多数论文为离散卫星选择，L03 为 multi-discrete(UE×轨道面)
4. **稳态占比分析是奖励验证的关键**：93-96% 步骤 B=0,H=0，极端场景分析是 cherry-picking

[D13][AUTO] 仿真器验证全部通过：FSPL/大气/阴影/Shannon/R_norm/仰角/可见性/自相关(lag-1=0.197) | 阶段: GW

[D14] 星座从 6×11=66 增至 18×22=396，可见卫星从 0-1 提升到平均 4.4 颗/UE | 理由: 66 星太少，切换决策无意义 | 阶段: GW

[D15] 轨道计算向量化（numpy broadcasting），396 星初始化 0.18s | 理由: Python 循环太慢 | 阶段: GW

[D16] 阴影衰落 σ 从二次多项式改为分段线性插值（20°→4.0, 45°→1.5, 90°→1.0 dB），修正 90° σ 反常偏高 | 阶段: GW

[D17] Baseline 初步结果：B4 Random(36Gbps/0.02%blk/8435HO), B1 HHS(21Gbps/37.4%blk/877HO), B2 DDQN(验证通过/loss↓), B3 PPO(验证通过/v_loss↓) | 理由: HHS 高阻塞率是多 UE 独立决策的结构性局限 | 阶段: GW

[D18] Step 7 可行性快判通过：三个问题均可回答，无阻塞风险 | 阶段: GW

[D19] 三方案新颖性检索：方案A(LA-DDQN)中新颖性(竞争者ARTHF 2025), 方案B(MA-CTDE)低新颖性(ILCHO IEEE TMC 2026完全覆盖), 方案C(GNN+DRL)中高新颖性(三元组合无人占据) | 理由: Contract阶段必须确认新颖性再冻结假设 | 阶段: CT

[D20] 方案B排除：ILCHO(IEEE TMC 2026)用QMIX+CTDE+LEO NTN切换+负载均衡，技术路线完全覆盖 | 理由: 顶刊竞争者，差异化成本过高 | 阶段: CT

[D21] 方向A和C分别推进：A(LA-DDQN)中新颖性低风险，C(GNN+DRL)高新颖性高风险，两个对话分别深入设计后选定 | 理由: 避免过早锁定，用并行探索降低决策风险 | 阶段: CT

[D032] Lee 2025 (ICT Express, DOI:10.1016/j.icte.2025.01.009) 精读结论 — 非碰撞，方案C最近邻居 | 理由: 纯GNN监督学习（无DRL），二部图UE-卫星结构相似但用sum-rate最大化loss而非强化学习；Fig.5有scalability实验(50UE训练→不同UE数测试)但属GNN架构泛化性，非DRL策略迁移；与本项目GNN+DDQN+size generalization路线不重叠 | 阶段: CT

[D033] Yuan 2024 (Aerospace MDPI, DOI:10.3390/aerospace11070511) 精读结论 — 非碰撞 | 理由: MPNN-DQN但有向路径图（非二部图），单UE场景，zero-padding固定状态维度，无多UE负载均衡，无size generalization实验；与本项目多UE二部图+负载均衡+zero-shot规模泛化无重叠 | 阶段: CT

[D034] 中文文献检索补充结论 — 无碰撞，新颖性结论不变 | 理由: S2/OpenAlex中文覆盖极低（4组关键词仅2条垃圾结果），web搜索补充未发现GNN+DRL+LEO切换的中文原创论文（仅综述/概述类）；中文文献盲区需用户手动检索CNKI/万方确认，但基于英文8轮检索+Lee2025/Yuan2024精读+中文补充检索，四元组合（二部图GNN+DDQN+LEO切换+规模泛化）仍无先例 | 阶段: CT
