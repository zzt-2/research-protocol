# Decision Log

## 阶段摘要
- [Groundwork] Step 1-3.5 完成（检索+精读+补充检索），Step 4a Go/No-Go 通过
- [Contract] Step 0-5 完成，已冻结（用户确认 2026-05-15）
- [Execute] 待执行

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
