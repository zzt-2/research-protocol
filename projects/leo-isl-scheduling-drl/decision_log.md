# Decision Log

## 阶段摘要
- [Groundwork] Step 1-3.5 完成（检索+精读+补充检索），Step 4a Go/No-Go 通过
- [Contract] Step 0-5 完成，已冻结（用户确认 2026-05-15）
- [Execute] Step 0-1 完成（模型+训练+Quick Test 5轮诊断），PPO/REINFORCE 均未超越先验
- [Execute] 方向修正 D026→D030: DRL→监督预训练+离散RL微调，ILP标签→路由感知标签
- [Execute] Phase A Grid 标签完成: GNN 完美学习 grid 拓扑(F1=1.0)，评估与 B1(N_LCT=4) 完全匹配(ratio=1.000, 零切换)
- [Execute] 方向决策 D034: 静态场景 grid 已最优无法超越→转向动态场景(边失效)+Phase B 离散 RL，**进行中**
- [Execute] D035-D037: 边失效机制+edge_dim 7→8+Phase B 训练完成，Phase B 无效(RL未学到有意义的策略)，待方向决策
- [Execute] D038: 全规模 24×66 swap 诊断未超出噪声→**归档**，7 种方法全部未超越先验

## 决策记录
[D001] Go/No-Go 决策：Go（用户已确认 2026-05-15） | 理由: A/B无致命信号 + MVE Pass (GNN 97.3% vs FC 79.5%) | 阶段: GW
[D002] MVE 选择图匹配而非RL训练 | 理由: 图匹配是ISL调度核心子问题，supervised比RL更快验证结构性优势，DRL可行性由L09奖励分解独立验证 | 阶段: GW
[D003][AUTO] MVE规模20节点 | 理由: 足够体现拓扑差异，训练快速（11 epoch收敛）
[D004] Baseline选定: B1=+Grid/Fixed, B2=Wang TCOM MADRL (L09)（用户已确认） | 理由: B1领域共识(5/15篇), B2最直接DRL竞品(架构详细,720星验证); 跳过L10(细节不足)/L12(与L09同组不独立) | 阶段: GW
[D005] 4b Go决策（用户已确认） | 理由: C无致命(仿真充分,无"过于平滑"风险)+E风险可控(B2复现是主风险但架构描述详细,失败兜底充分) | 阶段: GW
[D006] B2路由从LP改为Dijkstra | 理由: 保证与核心方法对比公平（差异仅在调度策略），简化B2适配 | 阶段: GW
[D007][AUTO] 决策间隔τ=10s, Episode 50步 | 理由: 介于setup delay极值(2~30s)之间，每步约1个setup周期，500s≈1/12轨道周期
[D008][AUTO] 奖励权重w₁=1.0, w₂=0.3, w₃=0.2 | 理由: 三项归一化后最大占比66.7%<95%，需MDP试运行确认
[D009] Step 6 §sim完成（用户待确认） | 理由: 数据流8步+参数溯源28项(0个ASSUMPTION)+奖励函数量级分析+Baseline规格 | 阶段: GW
[D010] B1 (+Grid/Fixed) 复现成功 | 理由: 24×8验证通过, B1吞吐量0.048 > Random 0.004 (+1231%), 零切换成本, 作为传统方法下限 | 阶段: GW
[D011] B2 (Wang MADRL) 复现 — 24×20测试规模下B2未优于B1 | 理由: B1有4固定ISL(2同轨+2跨轨), B2仅3固定+1动态; 测试规模(24×20)跨轨候选仅3个/星, 动态ISL增益不足以弥补固定链路减少; 全规模(24×66)候选更丰富,预期B2改善; 记录原因但不阻塞,全规模验证待Execute阶段 | 阶段: GW
[D012] 问题重设定: 强制 N_LCT 终端约束, 解决"B1过强 DRL无空间"困境（用户已确认） | 理由: 原B1无限ISL(4752边/6.0每星)M1=28.19%, 多路径路由仅+5.3%确认瓶颈在拓扑非路由; 加N_LCT约束后: N_LCT=4 gap仅1.9%(不够), N_LCT=3 gap=11.1%(甜点), N_LCT=2 gap=20.0%(太极端); 参数扫描(demand×Z_MAX×N_GS)9/9配置gap>5%, 平均gap=11.3%, 方向鲁棒; Z_MAX对gap无影响(3条最短ISL始终在范围内) | 阶段: GW
[D013] Contract 奖励函数修正: w₃从M5(公平性)改为C_setup(建链延迟成本) | 理由: (1)实现已用C_setup反映L04的setup delay物理约束, 公平性作奖励项导致训练不稳定; (2)M5保留为评估指标; (3)仿真器已验证三项归一化后量级匹配 | 阶段: CT
[D014] Contract Step 5 压力测试全部通过, 无致命风险 | 理由: Q1结构性优势明确(GNN拓扑感知+DRL时序学习), Q2边际结果可支撑消融研究, Q3信号独立(性能/架构/工程三维度), Q4 baseline为领域共识, 反模式4项全部Pass | 阶段: CT
[D015][AUTO] config.py N_LCT=2→3 已更新 (D012甜点) | 阶段: EX
[D016][AUTO] model_gat.py 验证通过: scores(E,)∈[0.44,0.48], value标量, params=67,971; get_action/evaluate_actions/obs_to_data/buffer_GAE/normalizer 全部通过 | 阶段: EX
[D017] Quick Test 24×20 结果: (1) 无active_bias → M1=0.003, M3=16.7(随机水平); (2) 加active_bias=3+std=0.018 → M1=0.078(75% of B1), M3=0.10(稳定拓扑); (3) PPO更新过激进导致策略退化(100ep M1降至0.057); (4) GATv2Conv edge_dim=64→66.7ms/层,去掉edge_dim→4.4ms/层,改用decoder端注入边特征; (5) 批处理evaluate_actions: 4.3ms/obs(vs逐条320ms) | 瓶颈分析: env.step 0.18s/步(轨道+路由), model forward 0.073s/步 | 阶段: EX
[D018] 训练策略调整: PPO直接从随机初始化学习失败(冷启动问题), 需要先行为克隆B1再PPO微调 | 理由: active_bias解决了ISL稳定性但初始拓扑质量差; PPO在无好起点时梯度信号不足以学到有效策略; v2只训15ep的eval比v4训100ep更好说明过更新有害 | 阶段: EX
[D019] 架构优化: GATv2Conv 去掉 edge_dim, 边特征改为 decoder 端注入 | 理由: (1) edge_dim=64时单层66.7ms vs 无edge_dim 4.4ms(15x提速); (2) 边特征(距离/状态/中断率)在 decoder 端直接可用,不需要在消息传递中; (3) decoder输入=concat(src_emb, dst_emb, edge_feat) 135维 → MLP 128→64→1; (4) params 67,971→54,020 | 阶段: EX
[D020] 模型先验设计: active_bias=3 + distance_bias=2 跳跃连接 | 理由: (1) active_bias让模型天然倾向保持活跃ISL(sigmoid(3)≈0.95),解决切换率问题(M3从16.7→0.03); (2) distance_bias让模型偏好短距离ISL(1-dist/Z_MAX),模拟B1的最近邻拓扑; (3) 两项都是可学习参数,PPO可调整; (4) 未经训练的纯先验策略M1=0.077已达B1的75% | 阶段: EX
[D021] Quick Test v5 最终结果: 先验策略M1=0.0774, PPO微调30ep后M1=0.0780(+0.0006), B1=0.1035 | 理由: (1) PPO几乎无法超越先验; (2) KL在小std(0.018)下必然爆炸(Δμ/σ²效应),大std(0.14)又退回随机; (3) 训练reward=-3.3但eval reward=+0.78,差距来自探索噪声破坏拓扑稳定; (4) **根本问题: 连续分数+Normal分布+top-K选择→PPO不适配这个动作空间** | 待决策: 换算法(ES/SAC)/换动作空间(离散keep-drop-swap)/监督学习/继续调参 | 阶段: EX
[D022] 全规模(24×66=1584)性能测量 | 候选边65,664条(12x于24×20的5,328); env.step=0.60s/步(3.3x于24×20); model forward ~300ms; 50ep估计25min; PPO批处理32 obs时edge decoder输入~283MB,可能接近RTX 4070 8GB显存上限 | 待决策: 候选边预筛选(如限制每星最多20个候选)/分层决策/局部决策 | 阶段: EX
[D023] REINFORCE + argmax 验证(24×20, 20ep) | 先验M1=0.0859→训练后M1=0.0827(-3.7%); train_reward=-10 vs eval_reward=+1.8; noise_std=0.08 | 结论: FAIL; 与PPO相同根因——探索噪声破坏拓扑稳定; REINFORCE无KL约束但噪声本身即致命 | 阶段: EX
[D024] Swap 诊断: 单星/多星随机ISL swap能否改善M1 | (1) 单星swap 20 trials: 改善5%, max +0.0011; (2) 多星swap(n=1,5,10)各10 trials: max +0.0015; (3) 所有改善均在±0.002噪声范围内 | 结论: 先验策略(keep active + shortest ISL)在24×20规模已接近最优; 与beam-hopping模式A3一致——物理结构决定性能，学习无法显著超越 | 待决策: 全规模验证/流量感知定向swap/归档 | 阶段: EX
[D025] Execute 死胡同判定: 3种RL方法(PPO/REINFORCE/噪声探索)全部未超越先验，swap诊断确认先验近最优 | 理由: (1) PPO D021: KL爆炸+先验做主功; (2) REINFORCE D023: 噪声毁拓扑; (3) Swap诊断 D024: 随机swap改善≤0.0015(噪声级); (4) 跨项目模式匹配: beam-hopping A3(物理关系不可学习)+A2(先验>RL); (5) 命中code-quality A1(连续+top-K×2项目)和A2(先验>学习×2项目) | 待方向回顾 | 阶段: EX
[D026] 方向回顾决策: 保持ISL调度方向，训练范式从DRL改为监督预训练(A)+离散RL微调(B)（用户确认） | 理由: (1) 问题不是选错方向(ISL蓝海是真的，GNN优势是真的)，而是选错训练范式(RL不适合此问题); (2) MVE已证明GNN监督学习+22.4% vs FC; (3) beam-hopping教训A3"成功论文全用监督学习"; (4) 连续+top-K命中A1失败模式(×2项目); (5) Phase A(ILP+监督)独立就是贡献，Phase B(离散RL)是锦上添花 | 阶段: EX
[D027] ILP建模方案: 流量感知加权容量最大化，不建模路由(避免bilevel) | 理由: (1) 目标=max Σ(supply_i+supply_j+demand_i+demand_j)*cap_ij*x_ij; (2) 约束=每星≤N_LCT+无向对称; (3) 24×20规模~5K变量秒级求解; (4) Phase B的RL微调负责路由级反馈 | 阶段: EX
[D028] 离散动作空间设计: 每条候选边3-way {AS-IS, FORCE-ON, FORCE-OFF} | 理由: (1) AS-IS=默认走预训练策略(稳定); FORCE-ON=1.0/FORCE-OFF=0.0覆盖; (2) 大部分边不需RL决策→维度降低; (3) Categorical分布替代Normal→绕开KL爆炸; (4) wrapper保持env.step(scores)接口不变→零环境改动 | 阶段: EX
[D029] Phase A(ILP监督)完成: GNN完美拟合ILP解(F1=0.9998)但实际M1=0.079远低于B1的0.174 | 理由: (1) ILP不建模路由→最大化加权容量≠高吞吐量; (2) ILP无时序一致性→每步独立求解→M3=0.044(频繁切换)→大量setup delay; (3) B1固定拓扑零切换零setup，grid结构保证路由连通性; (4) 根因: ILP标签是代理目标(容量)非真实目标(吞吐量) | 阶段: EX
[D030] 方向修正: ILP标签→路由感知标签 + N_LCT=3→4（用户确认） | 理由: (1) ILP标签已被D029证明是代理目标，继续用无意义; (2) 路由感知标签: 用B1 grid作初始拓扑，贪心局部搜索(替换ISL→计算路由吞吐量→保留改善)，标签直接优化真实目标; (3) N_LCT从3提到4与B1公平对比(B1有4条固定ISL); (4) 方向1(路由感知标签)最可能突破，方向3(公平对比)作为保底 | 阶段: EX
[D031] 路由感知贪心搜索不可行，改用 grid 标签直接训练（用户确认） | 理由: (1) 24×20 grid 是完美 4-正则图(960边)，N_LCT=4 阻塞所有单边替换;(2) 路由计算 146ms/次×2600 试验/轮=386s/轮，全数据集>100h;(3) D024 已证 grid 在此规模近最优;(4) 采用方向3(公平对比): grid 标签直接训练 | 阶段: EX
[D032] B1 基线数据修正: handoff M1=0.174 是未剪枝 B1(6 edges/sat, 1440边)，正确 B1(N_LCT=4) M1=0.115(4 edges/sat, 960边) | 理由: GridFixedBaseline 默认 n_lct=None 不剪枝，导致 edges_per_sat=6; 与 N_LCT=4 的 DRL 对比不公平 | 阶段: EX
[D033] Phase A Grid 标签训练完成: F1=1.0, acc=1.0, 与 B1(N_LCT=4) 完全匹配 ratio=1.000, 零切换 | 理由: (1) GNN 完美学习 grid 拓扑; (2) 预激活 grid 边后评估: M1=0.1154=B1(N_LCT=4), M3=0.0000; (3) 验证了 GNN 架构和训练管线正确性; (4) 24×20 规模 grid 已是最优，无法超越; (5) Execute 暂停，待决定下一步(Phase B/全规模/归档) | 阶段: EX
[D034] 方向决策: 静态场景转向动态场景(边失效) + Phase B 离散 RL | 理由: (1) 静态场景 grid 已数学最优(D024+D031证明4-正则图无改进空间); (2) 边失效是 GNN+DRL 的设计初衷(文献空白); (3) 静态 grid 无法自适应→被动等待恢复，GNN 可重选拓扑; (4) 最小可行路径: 边失效机制 + Phase A 预训练初始化 + Phase B 离散 RL 微调; (5) 补充: 全规模24×66+动态 baseline(B2)作为后续强化证据 | 阶段: EX
[D035] 边失效机制实现: 环境和基线均支持 link failure | 理由: (1) config.py 新增 FAILURE_PROB/DURATION 参数(默认禁用); (2) environment.py 每步随机失效活跃边，失效边不可被 LCT 选择和路由; (3) grid_fixed.py 同样支持失效; (4) 冒烟测试验证: p=0.1 时 grid 吞吐量降 13.2% | 阶段: EX
[D036] 边特征维度 7→8(加失效标志) + Phase A 权重 padding | 理由: (1) Phase A 在 p=0.03 失效下 M3=0.286(疯狂切换)，因模型看不到哪些边失效; (2) 新增第8维 edge_feat[7]=1.0 if failed; (3) model edge_dim 从 7→8，新增 load_backbone_with_padding() 函数自动补零列; (4) 验证: padded 8-dim 输出与 7-dim 完全一致(max diff=0.0) | 阶段: EX
[D037] Phase B 训练无效: RL 未学到有意义的策略 | 理由: (1) 无 AS-IS 偏置: reward=-20(随机 FORCE-OFF 毁拓扑); (2) 有 AS-IS 偏置(bias=5.0): reward=-10.3(vs Phase A 的 -12.4)，但 Phase B 评估结果 = Phase A(M1=0.109, M3=0.164); (3) 根因: AS-IS 偏置太强+失效边仅占 2%(100/5400)→PPO 信用分配无法从稀疏信号中学习; (4) Phase A 在失效下 ≈ Grid(吞吐量恢复 ≈ 切换惩罚损失); (5) 24×20 规模替代边质量不够好，无法补偿切换成本 | 阶段: EX
[D038] 归档决策: 全规模 24×66 验证后归档 | 理由: (1) 24×66 swap 诊断: best Δ=+0.004(1.7%)在种子间噪声(±0.013)范围内，12 次试验仅 2 次为正; (2) failure gap 仅 7.3%(比 24×20 的 12.6%更小); (3) grid edges/sat=5.27>N_LCT=4(不公平优势); (4) 7 种方法(PPO/REINFORCE/swap/ILP标签/grid标签/动态场景离散RL/全规模swap)全部未超越先验; (5) 与 beam-hopping 同一失败模式: 物理结构决定性能，学习无法超越; (6) 根本问题(credit assignment)与规模无关 | 归档 | 阶段: EX
