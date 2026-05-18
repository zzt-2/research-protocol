# LEO 拥塞路由（GW 阶段）

> 创建: 2026-05-16 | 状态: **closed** | 阶段: Groundwork Step 7 完成 → Contract

## 进展线索

### H001-step2-done.md
Step 1-2 完成。87 条检索候选（必读 15/建议读 20），确认 GNN+拥塞路由+LEO per-link 负载均衡为真空地带，size generalization x 拥塞路由交叉完全空白。10 篇论文 content.md 已获取（GRLR/GMR/POMAP/PathGNN/GDRL-SFCR/Fan 2026/DTAR + PRIMAL/QueueMARL/ST-QoS），5 篇仍缺失（GNN-ASSSP/DLBR/LARRI/FlexSATE/CA-GAR）。项目定位为 GNN 拥塞感知 per-link 负载均衡路由，核心风险为 GNN 可能不优于 MLP。

### H002-step3-supplement.md
Step 3 精读 + Step 3.5 定向补充完成。10 篇 L01-L10 精读 + L11 TELGEN 精读。TELGEN (Zhou 2025 ToN) 改变项目定位：纯 size generalization for TE 不再空白，差异化必须聚焦 LEO 时变拓扑。新发现 DeepLaDu（per-link congestion prices）等 4 篇竞品。文献笔记更新至 L01-L11。

### H003-step4a-mve-pass.md
Step 4a MVE 两轮验证通过。MVE-1（24 节点）：GNN MLU 0.809 vs MLP 0.979，GNN 低 17%。MVE-2（66 节点 + 8% 链路故障）：GNN MLU 1.096 vs ECMP 1.244，GNN 低 12%。核心洞察：GNN 优势来源于全局负载聚合 + 拓扑异常适应，24 节点太小 ECMP 足够好，66 节点 + 故障才体现优势。决策 D7 Go。

### H004-step4b-literature.md
Step 3.5 补充论文获取（5 篇 PDF 转换归档）+ 6 篇 L12-L17 精读。确认无直接竞品做 per-link 负载均衡 + DRL + LEO 时变。GNN-ASSSP 最接近但纯 SL 不做 per-link 流量分配。仿真器设计关键约束已从精读中提炼（多维边特征、MPNN 三层消息传递参考、推理延迟约束）。Step 4b + Step 5 + Step 6 设计均已进入就绪状态。

### H005-step56-design.md
Step 5 + Step 4b + Step 6 完成。D8 Baseline 选定：SP + ECMP + MLP + DTAR + GMR 简化版。D9 可行性 Go。D10 仿真器设计确认：集中式 SDN、per-link 连续权重动作、GAT 2 层 4 头 64 维、PPO + GAE + wandb + early stopping、66 节点训练 + 48/288/720 泛化测试。6/6 项目缺失项清单已提取（wandb/early stopping/save-load/Config/Env 继承/共享 backbone）。

### H006-step7-simulator.md
Step 7 Part A 完成。仿真器 8 模块实现（config/topology/traffic/failures/env/model/train/verify，共约 2200 行）。3 个 baseline（SP/ECMP/MLP）。6 类验证全部通过（解析/统计/退化/自相关/MDP trial/reward balance）。关键设计：固定边集（故障边保留为 is_failed=1.0）、连续动作空间 softplus 保证正值、同时路由范式。已知问题：ECMP 未迭代 t_slots。

### H007-step7-verified.md
Step 7 完成，续接至 05-17 目录。修复 3 个 bug（model.py 负权重、failures.py 零故障率注入、config.py 断言）。验证套件 28/28 全通过。三个 baseline 运行结果：SP MLU 1.88、ECMP MLU 2.07、MLP MLU 1.77（MLP 已优于 SP）。Import 方案通过 symlink 解决。Groundwork 阶段完成，下一步进入 Contract。

## 已确认结论

1. **项目定位确立**：GNN 拥塞感知 per-link 负载均衡路由 for LEO 卫星星座，差异化聚焦 LEO 时变拓扑（vs TELGEN 静态快照+SL）
2. **GNN 优势验证通过**：66 节点 + 链路故障场景下 GNN 低 ECMP 12%、低 MLP 20%，全局负载聚合有效
3. **真空确认**：per-link 负载均衡 + DRL + LEO 时变无直接竞品，size generalization x 拥塞路由交叉空白
4. **Baseline 体系**：SP + ECMP + MLP（核心）+ DTAR（有代码竞品）+ GMR 简化版（最接近竞品）
5. **仿真器设计冻结**：集中式 SDN per-link 连续权重 + GAT + PPO，训练 66 节点，泛化 48/288/720
6. **仿真器验证通过**：28/28 验证项全通过，baseline 运行正常

## 未决项

1. DTAR 竞品复现（适配 GitHub 代码到本仿真器）
2. GMR 简化版复现（MPNN+DDPG 去PER K=2，P4 级复杂度，可退守 DTAR 单一竞品）
3. TELGEN 竞品差异化需在实验中充分体现 LEO 时变拓扑维度
4. FR-09（GNN 信息冗余）和 FR-10（空间隔离约束决策模式）待评估
5. ALIDT/ADRLRM (Gao 2025/2026) 和 GRL-RR (Bai 2025) 未获取，不阻塞但不完整

## 当前位置

Groundwork Step 7 全部完成（仿真器 8 模块 + 28/28 验证通过 + 3 baseline 运行），已续接至 05-17 目录进入 Contract 阶段。
