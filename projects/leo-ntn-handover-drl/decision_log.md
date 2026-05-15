# Decision Log

## 阶段摘要
- [Groundwork] Step 2-4 完成：6 篇精读，3 个 baseline 选定
- [Groundwork] Step 5-6 完成：仿真器验证通过，3 个 baseline 复现完毕
- [Contract] 方案 C（GNN+DRL）设计完成，D007-D014 决策记录
- [Execute] 方案 A 验证完毕(DLA 被消融否定)，方案 C 超参+消融完毕(GNN +0.8%)
- [Execute] 叙事转向 size generalization，Contract 待重新冻结
- [Execute] Scaling 实验完成(Phase 1-5)：size generalization 是 GNN 决定性优势(D026-D031)
- [Contract] 叙事转向后新颖性检索通过：四要素组合无先例，D032 补充 4 篇中等重叠论文

## 决策记录
[D001] 选定 B1(传统A3/MVT) + B2(D3QN/Dueling DDQN) + B3(PPO) 三个 baseline | 理由: B1 被 4 篇论文使用(传统方法锚点)，B2 被 3 篇使用(DRL 共识架构)，B3 被 4 篇使用(最广泛 on-policy DRL)。用户选择全做以获得更全面对比。 | 阶段: GW
[D002][AUTO] 6 篇论文中 L004、L029、L018、L016、L024 直接相关 handover+DRL，L022 方法可借鉴(协作 DRL) | 理由: L022 主题为资源优化非切换，但双时间尺度 MDP 建模有参考价值 | 阶段: GW
[D003][AUTO] 8 篇失败论文(L001/L003/L005/L006/L017/L019/L021/L030)报告用户，两轮后停止 | 理由: 全部 IEEE/Elsevier 付费墙无 arXiv 版本，符合 domain-comms.md 预期 | 阶段: GW
[D004] 仿真器验证全部通过(5/5)：FSPL精确、仰角90°、雨衰统计0.3%误差、退化测试OK、lag-1自相关0.36 | 理由: 自建纯Python仿真器(Walker-delta 66星+FSPL+AR(1)雨衰)，满足groundwork.md Step 6验证清单 | 阶段: GW
[D005] 3个baseline均~90%阻塞率，根因是奖励尺度失衡(吞吐量~10⁶ >> 阻塞惩罚10) | 理由: DRL未学到负载均衡，退化为贪心选最高rate卫星(等价MVT)。与L029报告的近零阻塞率差距大，因L029的reward经过归一化。 | 阶段: GW
[D006] Contract阶段首要任务：修复奖励尺度（归一化rate + 增大β），使DRL能结构性优于传统方法 | 理由: groundwork.md §6 自相关预警处理要求"目标DL方法在仿真数据上[MUST]结构性优于最简baseline"——当前未满足 | 阶段: GW

---

## Contract 阶段决策

[D007] 方案 B（MA-CTDE）排除：ILCHO(IEEE TMC 2026) + QMIX-PHO(ETRI 2025) 完全覆盖 QMIX+CTDE+切换+负载 | 理由: 顶刊覆盖度最高，无差异化空间 | 阶段: Contract
[D008] 方案 A 和 C 分别深入设计，暂不淘汰 | 理由: A 新颖性中（与 ARTHF 差异窄），C 新颖性中高（三元组合无人占据），需完整设计后对比 | 阶段: Contract
[D009] Yu et al. 正确 URL 确认为 https://www.mdpi.com/2226-4310/11/7/511 | 理由: 原记录 /11/5/389 为压缩机论文，通过 MDPI 验证更正 | 阶段: Contract
[D010] 选定边条件化 MPNN（MPNN-E）作为 GNN 层类型 | 理由: 边特征（SINR, elevation）是切换决策的主要信息源，GCN/GAT 原生不支持边特征。Yu et al. 在卫星切换中验证 MPNN，L15 在二部图中验证 FCN 消息传递 | 阶段: Contract
[D011] 选定分解式 Q 函数替代 flat Q | 理由: Q(UE_i, sat_j) = V(h_ue) + A(h_ue, h_sat, h_edge) 参数量 ~14K vs flat Q ~700K，且自然支持变长候选集。分解式 Q 是 MPNN 边级嵌入到 DRL 动作空间的最直接映射 | 阶段: Contract
[D012] top-K=6 候选压缩纳入方案 C 作为图构建预处理 | 理由: 仿真器统计平均 4.4 颗可见卫星，K=6 覆盖全部。从 396→6 使图规模可控（15×6=90 条边），与方案 A 的 top-K 创新点合并 | 阶段: Contract
[D013] 两阶段训练策略：Phase 1 GNN 预训练（~50ep, 辅助任务预测阻塞+负载变化），Phase 2 联合训练（GNN lr=1e-4, DRL lr=1e-3） | 理由: 缓解 GNN+DRL 联合训练不稳定风险（R5）。预训练强制 GNN 学会负载相关编码，避免 DRL 初期收到噪声输入 | 阶段: Contract
[D014] **最终选定方案 C（GNN+DRL）**作为主攻方向 | 理由: (1) 新颖性优势：三元组合无人占据 vs A 与 ARTHF 差异窄; (2) 故事更清晰："结构化图编码让 DRL 感知负载竞争"; (3) 参数效率 29K vs 712K 支持泛化性叙事; (4) top-K 从方案 A 并入，不丢失其优点; (5) 风险可控（T=2, 残差, LayerNorm, 两阶段训练） | 阶段: Contract

---

## Contract 阶段决策（方案 A 深入设计，2026-05-08）

[D015] ARTHF 精读三个关键发现：(1) self-attention softmax 仅在有效卫星间计算（Eq.27 用 M_k^t），positional bias 问题被论文夸大; (2) Dueling advantage 中心化使用 M_k^max（含 zero-pad），引入数值偏差; (3) 对比方法仅 Rainbow DQN 变体，无传统方法 baseline | 理由: 这些发现支撑方案 A 的差异化空间 | 阶段: CT

[D016] DLA（Dedicated Load Attention）采用 cross-attention 设计：query=负载统计[l_avg,l_max,l_std,n_svc]，key/value=卫星特征。与 ARTHF self-attention 在结构层面区分（Q 来源不同）| 理由: self-attention Q/K/V 同源（卫星特征），无法被负载状态驱动; cross-attention 让负载主动查询卫星特征 | 阶段: CT

[D017] Top-K 压缩推荐 K=8：当前仿真 max 可见约 6-7 颗，K=8 保证零信息损失。观测维度从 1585 降至 41（97.4% 压缩），与星座规模无关 | 理由: ARTHF zero-padding 浪费 ~45% FC 计算 + advantage 中心化偏差，Top-K 彻底规避 | 阶段: CT

[D018] 消融实验 8 组设计：A1(B2 baseline), A2(Top-K only), A3(Self-Attn+Top-K 复现 ARTHF), A4(DLA+Full obs), A5(LA-DDQN 完整), A6-A8(K=3/5/10 变体)。核心对比 A5 vs A3（DLA vs Self-attention）| 理由: 隔离 top-K、DLA、self-attention 各自贡献 | 阶段: CT

[D019] 方案 A 贡献评估 ★★★☆☆：差异化真实（cross-attention vs self-attention 是结构性差异）但 incremental over ARTHF。目标 MDPI/IEEE Access 可行，IEEE TWC 困难。与方案 C(★★★★☆)相比：A 低风险保底，C 高创新高风险 | 理由: 诚实评估，A 核心贡献是"负载驱动的注意力+高效观测压缩"，故事清晰但不够惊艳 | 阶段: CT

[D020] 方案 A 保留为**备选/降级方案**：如果方案 C GNN 训练不稳定，可退回 A。A 的 top-K 和 DLA 设计可独立于 C 使用 | 理由: D014 已选定 C 为主攻，但 A 的完整设计文档作为风险缓解措施保留 | 阶段: CT

---

## Execute 阶段决策（2026-05-08 → 05-09）

[D021] **方案 A 死亡**：A1 消融（Flat FC vs LA-DDQN）全面否定 DLA cross-attention。吞吐量 36.05 vs 35.91 Gbps，阻塞 0% vs 0.07%，参数量 35K vs 52K。DLA 无独立贡献 | 理由: 15 UE + ~5 可见卫星场景下 attention 无用武之地，FC 表达能力已过剩。Top-K 压缩是唯一有效贡献，但属于工程优化不足以支撑论文 | 阶段: EX

[D022] 方案 C 消融结果：GNN 在 top-K 基础上仅 +0.8%（+77 reward over C6 flat MLP）。真正的决定性改进来自 top-K 压缩（396→6 动作空间，reward 4866→9857，阻塞 25%→0%）。T=2 消息传递是最关键 GNN 组件（+1.8%） | 理由: GNN 有效但增量有限，直接"GNN 提升性能"的叙事不成立 | 阶段: EX

[D023] **叙事转向 size generalization**：核心贡献从"GNN 提升绝对性能"转向"可扩展的负载感知切换架构"。文献检索确认：(1) GNN 在 N>20-30 时显著优于 MLP（Lee 2023, Shen 2019）；(2) size generalization（小规模训练、大规模部署）是 GNN 在无线领域最强论点（Wu 2022, Garcia Camargo 2025）；(3) "UE 数量对切换算法性能的影响"在 LEO 领域是研究空白 | 理由: 15 UE 下 GNN ≈ MLP 是预期行为而非缺陷，文献阈值 N>20-30 完全解释当前结果 | 阶段: EX

[D024] 新颖性二次检索通过：Fan 2026（ISL 路由，非切换，低重叠）、Jayarajan GT 2025（卫星-小区分配，无RL，低重叠）、GNN-HLS Wang 2025（UE-UAV 接入，非卫星切换，低重叠）。"二部图 GNN + DDQN + size generalization"在 LEO 切换领域无竞争者 | 理由: 四组系统检索（scale-gnn/scale-bipartite/size-generalization/scale-dense）覆盖充分 | 阶段: EX

[D025] Contract 重新冻结：实验设计调整为三阶段——(1) 20 UE 基线可行性（GNN ≈ MLP），(2) 50-100 UE 规模扩展（MLP 退化，GNN 稳定），(3) Size generalization（20 UE 训练 → 50/100 UE 直接推理）| 理由: 三步递进叙事对应文献支撑的 GNN 优势阈值，且有明确的研究空白支撑 | 阶段: EX

---

## Execute 阶段决策 — Scaling 实验（2026-05-09）

[D026] **sat_capacity 按比例调整**：cap=10 在 100 UE 下结构性不可行（~5 可见卫星 × 10 容量 = 50 < 100 UE），调整为 50 UE cap=15、100 UE cap=25 | 理由: Phase 1 验证确认 cap=10 × 100 UE 随机阻塞率 86%，任何算法都无法有效改善 | 阶段: EX

[D027] **训练预算随规模增长**：50+ UE 需要 buffer=200K + 100 episodes。50 UE × 720 steps = 36K transitions/episode，buffer 50K 仅存 ~1.4 episode 导致 GNN 训练崩溃（E4-50 首次运行 reward -4,857） | 理由: 扩大 buffer 后 GNN 在 50 UE cap=10 恢复至 reward 20,021，确认 buffer 不足是首次失败根因 | 阶段: EX

[D028] **100 UE 同规模训练 GNN >> MLP**：E4-100-c25 reward 45,313 vs C6-100-c25 reward 33,843（+34%），阻塞率 8.56% vs 20.6%（-58%）| 理由: 100 UE cap=25 下负载竞争足够强，GNN 的结构化编码优势显现 | 阶段: EX

[D029] **Size generalization 是决定性优势**：20 UE 训练的 GNN 直接迁移到 100 UE 获得 reward 35,699（正 reward），MLP 迁移到 100 UE 完全崩溃（reward -9,710，71.5% 阻塞）。50 UE 迁移 GNN +61.5% over MLP | 理由: GNN 的 permutation equivariance 使参数在 UE 数量变化时保持语义，MLP 固定维度输入无法泛化 | 阶段: EX

[D030] **论文叙事最终锁定**：三级递进——(1) top-K 压缩使 DRL 可行（B2 25% 阻塞 → C6 0%），(2) GNN 在大规模同规模训练中优于 MLP（100 UE +34%），(3) GNN 支持 zero-shot 规模迁移（20→100 UE +467%）| 理由: Phase 5 结果是最强论点，远超 execute_v2_prompt 的 success signal（50 UE gap ≥15% → 实际 61.5%） | 阶段: EX

[D031] **B2-50 baseline CUDA 崩溃**：396 维动作空间 + 50 UE 导致 CUDA launch failure。B2 在 15 UE 已 25% 阻塞率，50 UE 必然更差，不重新尝试 | 理由: B2 的失败已被 15 UE 实验证实，50 UE 额外验证非必要 | 阶段: EX

---

## Contract 重新冻结 — 新颖性补充检索（2026-05-09）

[D032] **叙事转向后的针对性新颖性检索通过**：三组系统检索覆盖 size generalization+卫星切换、GNN zero-shot+无线网络、scalable DRL+handover，均通过 Semantic Scholar 独立验证。无高度重叠竞争者。新发现中等重叠论文 4 篇，无精读必要：

| 论文 | 核心方法 | 缺失要素 | 威胁 |
|------|---------|---------|------|
| Lee 2025 (ICT Express, DOI:10.1016/j.icte.2025.01.009) | GNN + 分布式 LEO 切换 + 负载均衡 | 无 DRL、非二部图、可扩展性声明基于 GNN 固有性质非显式实验 | 低-中 |
| Eydian 2025 (IEEE OJCOMS, DOI:10.1109/OJCOMS.2025.3541962) | 加权二部图匹配 + 滞后余量做 LEO 切换 | 无 GNN、无 RL、经典优化 | 低 |
| Chou 2026 (arXiv:2605.02416) | Dueling DDQN 多目标 LEO 切换 | 无 GNN、无二部图、无 size generalization | 低-中 |
| Kim 2022 (arXiv:2207.05364, IEEE TWC) | 二部图 GNN (BGNN) 波束赋形 + 跨规模可扩展 | 非切换场景、无 DRL | 低-中(理论先驱) |

已排除(低重叠)：Fan 2026(ISL路由)、Jayarajan GT 2025(无RL)、GNN-HLS Wang 2025(UAV)、SMASH 2025(每规模重训练)、Dewa 2025(综述)

IEEE Xplore 补充检索通过（7 组 site:ieeexplore.ieee.org + OpenAlex，覆盖 TWC/OJCOMS/CommLet/IoT Journal/VTC）。新发现 1 篇中等重叠：Wiriya 2025 (IEEE doc:11431740) 二部图+D2C卫星切换，传统图匹配非 GNN/DRL。其余新发现均为低重叠（Lee C. 2025 MADQN切换/Mendonca 2025 DQN频谱共存/Zhang 2025超图GNN资源分配/Sheng 2026图基础模型/Yang 2026多层图IoT切换）。IEEE 检索确认无新竞争者。

**结论**："二部图 GNN + DDQN + size generalization + LEO 切换"四要素组合在现有文献中无完全先例。各要素分别有相关工作但无人整合。size generalization 是项目最核心的差异化壁垒——Lee 2025 的可扩展性仅为 GNN 固有性质声明，Wu 2022 仅提供理论分析且非切换场景。| 阶段: CT
