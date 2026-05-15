# Decision Log

## 阶段摘要
- [Groundwork] Step 3.5完成, Step 4a Conditional Go, Step 5 Baseline选定, Step 4b Go, Step 6 仿真器设计确认
- [Contract] 待进入
- [Execute] 待进入

## 决策记录
[D001] 确认GNN+BH为蓝海方向 | 理由: 4组关键词+引用链分析确认零直接竞品，最接近者P1仍以RL为主 | 阶段: GW
[D002] Step 4a Conditional Go | 理由: A/B无致命信号；MVE部分通过（GNN收敛时+16~48%，但3/5 seeds训练崩溃）；训练不稳定为REINFORCE已知问题，PPO/SAC可解决 | 阶段: GW
[D003][AUTO] MVE使用REINFORCE而非PPO | 理由: MVE追求最小实现，验证结构性优势而非训练稳定性 | 阶段: GW
[D004] Baseline选定：PPO+MLP(主选) + 图着色L04(次选) + Greedy/EPA(trivial) | 理由: (1)PPO+MLP为核心消融对照，同算法不同编码器直接证明GNN贡献，实现成本中等；(2)图着色L04为非ML传统基线，图方法与GNN形成"传统图论vs学习化图方法"对比，算法描述详细(WCL 2026)；(3)Greedy/EPA为领域绝对共识下界(精读4篇+田野8+篇使用)，实现极低；(4)QPLEX(L03)虽为SOTA但实现复杂度极高(分层MADRL+QPLEX+CRO+CLA)，暂不纳入，revision阶段可补充；(5)势博弈(L07)田野罕见(仅1篇使用)，非领域共识，不选；(6)田野调查覆盖35篇/25篇有效，远超10篇门槛 | 阶段: GW
[D005] 不选QPLEX的理由 | 理由: 分层MADRL全栈实现需3-4周，PPO+MLP已覆盖"与主流DRL对比"需求。若审稿人要求SOTA对比可在revision阶段补充 | 阶段: GW
[D006] Step 4b Go | 理由: C维度无致命信号（全频复用+真实天线方向图→非均匀干扰→GNN优势条件充分，"过于平滑"风险有缓解路径）；E维度无致命信号（全部自实现但PPO/Greedy标准，失败沉没成本有多条回收路径） | 阶段: GW
[D007] 仿真器设计确认 | 理由: 单星多波束(19/37/61), Ku 11.45GHz, Bessel天线, 全频复用, PPO+GNN。参数溯源16项仅1项[ASSUMPTION](K=5)。奖励 α·throughput(0.6)+β·fairness(0.3)-γ·interference(0.1)。用户确认2026-05-15 | 阶段: GW
[D008] 仿真器实现物理修正(3项) | 理由: (1)噪声功率：-97dBm为总噪声功率而非PSD，不应乘带宽，否则SINR虚低~60dB；(2)路径损耗：应用轨道高度550km而非slant_range 2704km，否则多算14dB；(3)干扰惩罚：原公式max(0,SINR-thr)惩罚高SINR(好选择)方向反了，改为max(0,thr-SINR)惩罚低SINR(差选择) | 阶段: GW
[D009] 吞吐量归一化修正 | 理由: 原R_throughput=served/total_demand_all_N归一化分母含全部19波束需求，K=5时信号仅~5%，被fairness(~85%)淹没。改为served_active/demand_active(仅计算被服务波束)，吞吐量占比升至~15-18%，三项分量均可见 | 阶段: GW
