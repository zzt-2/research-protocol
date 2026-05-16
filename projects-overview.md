# 项目总览

> 最后更新: 2026-05-16 | 活跃: 5 | 已归档: 3 | 总计: 8

## 活跃项目

### leo-mega-constellation-gnn-routing
- **方向**: GNN size generalization — 小星座训练零样本泛化到Starlink级路由
- **阶段**: Execute 完成 → 论文素材提取
- **关键技术**: GNN (GraphSAGE) + 位置编码 + 多尺度训练
- **关键结论**: 跨规模时延保留率90.3%，PE是学习必要条件（无PE≈随机），9.7pp stretch差距纯来自跨规模迁移
- **教训**: MVE 83-87%保持率为后续投入奠基；消融设计有效隔离泛化来源
- **handoff**: `.session/2026-05-13-mega-constellation-gnn-routing/HANDOFF-008-0514-step5.md`

### leo-ntn-handover-drl
- **方向**: 二部图GNN+DDQN实现LEO切换size generalization
- **阶段**: Execute 完成 → Contract 叙事转向后重新冻结
- **关键技术**: 二部图GNN + DDQN + top-K动作压缩
- **关键结论**: GNN从20UE迁移到100UE reward 35,699（正），MLP迁移崩溃-9,710；top-K压缩是决定性改进（reward 2x），GNN仅+0.8%
- **教训**: 初始叙事（GNN提升绝对性能）在小规模不成立，及时转向size generalization救活项目；叙事转向需系统性实验支撑
- **handoff**: 无专用session目录（决策记录在项目目录内）

### hgat-satellite-dag-offloading
- **方向**: HGAT增强的卫星-地面协同边缘计算DAG依赖任务卸载
- **阶段**: GW Stage 7 — 仿真器搭建+Baseline复现
- **关键技术**: 异构图注意力网络(HGAT) + DRL
- **关键结论**: MVE通过（HGAT vs GraphSAGE +10.7%）；多IoTD环境重写完成；奖励权重η_t=0.5导致E_norm占97.9%需试运行验证
- **教训**: 组合新颖性不可跳过MVE；奖励权重平衡需试运行验证；MinerU可解决PDF表格渲染问题
- **handoff**: `.session/2026-05-13-hgat-satellite-dag-offloading/HANDOFF-001-initial.md`

### leo-congestion-routing
- **方向**: GNN 拥塞感知路由 + 负载均衡 for LEO 卫星星座
- **阶段**: GW Step 1 完成 → Step 2 论文获取
- **关键技术**: GNN message passing + 全局负载聚合 + per-link 负载均衡决策
- **关键结论**: Step 1 检索 87 条候选（必读15），GNN+拥塞+LEO 三角交集有论文但无 per-link 竞品；size gen × 拥塞路由交叉为真空
- **风险**: resilient-routing MVE 证明 GNN ≈ MLP for routing，新方向需验证拥塞/负载信息的全局聚合优势
- **handoff**: 无（项目刚启动）

### leo-resilient-routing
- **方向**: LEO故障感知抗毁路由（GNN→MARL+课程学习+主动预路由）
- **归档原因**: MVE三轮失败：(1) GNN不优于MLP(18/60节点); (2) MARL课程学习+2.2%未达门槛; (3) 主动预路由反而更差(-1.3%); 与beam-hopping/ISL-scheduling同模式：网格拓扑正则→启发式够用→ML无优化空间
- **关键失败教训**: Walker星座网格拓扑太规则，贪心路由92%投递率，RL仅5%；LEO路由/调度/波束跳三个子方向全部归档，信号一致：物理约束主导问题不适合ML
- **handoff**: `.session/2026-05-16-leo-resilient-routing/HANDOFF-004-step4a-pivot.md`

### leo-isl-scheduling-drl
- **方向**: GNN拓扑编码+DRL用于LEO巨型星座ISL细粒度三态调度
- **阶段**: **归档** — 7种方法全部未超越先验
- **归档原因**: (1) grid拓扑在24×20/24×66均近最优(swap改善<噪声); (2) PPO/REINFORCE/离散RL均无法超越先验; (3) ILP标签是代理目标; (4) 动态场景(边失效)RL信用分配失败; (5) 与beam-hopping同一失败模式: 物理结构决定性能
- **关键结论**: GNN可完美学习专家拓扑(F1=1.0)，但无法超越; 24×66跨轨候选8.5个/sat(vs 24×20仅3个)，仍不足以产生优化空间
- **教训**: 物理约束主导的问题(grid拓扑)不适合RL优化; 全局reward vs 逐边动作的credit assignment与规模无关; ILP标签最大化容量≠最大化吞吐量
- **handoff**: `.session/2026-05-16-isl-scheduling-drl/HANDOFF-018-dynamic-scenario-stuck.md`

### ris-phase-drl
- **方向**: DRL优化大规模RIS(100+元素)连续相移
- **阶段**: GW Step 4a Go 通过 → 待 Step 5 Baseline选定
- **关键技术**: TD3/SAC（A2C能力不足已被撤稿证实）
- **关键结论**: 空白真实存在；最直接竞争者已撤稿；100维连续动作空间是核心挑战
- **教训**: 补充检索发现关键竞争论文（已撤稿）避免重复失败；所有精读论文无开源代码，复现复杂度高
- **handoff**: `.session/2026-05-13-ris-phase-drl/HANDOFF-002-step2.md`

## 已归档项目

### leo-isl-scheduling-drl
- **方向**: GNN拓扑编码+DRL用于LEO巨型星座ISL细粒度三态调度
- **归档原因**: 7种方法(PPO/REINFORCE/swap/ILP标签/grid标签/动态场景RL/全规模swap)全部未超越先验; grid拓扑在24×20和24×66均近最优; 物理结构决定性能与beam-hopping同模式
- **关键失败教训**: 物理约束主导的问题不适合RL; 全局reward+逐边动作的credit assignment与规模无关; ILP标签是代理目标(容量≠吞吐量)
- **handoff**: `.session/2026-05-16-isl-scheduling-drl/HANDOFF-018-dynamic-scenario-stuck.md`

### leo-beam-hopping-gnn
- **方向**: GNN建模多波束LEO卫星Beam Hopping波束间空间干扰耦合
- **阶段**: 归档 — 6种方法全部失败
- **归档原因**: 干扰是beam pair物理关系，无法从标量奖励通过梯度学习；action space(top-K离散选择)与图结构干扰关系根本不匹配
- **关键失败教训**: Gaussian policy + top-K→信用分配稀疏（19维仅5维有梯度）；奖励被fairness主导82%可学信号仅7%；成功GNN论文均用监督学习非RL；MVE训练不稳定是预警信号
- **handoff**: `.session/2026-05-15-beam-hopping-gnn/HANDOFF-009-archive.md`

## 跨项目教训

详细记录统一在 `code-quality.md`，本文件不重复。按以下维度组织：

- **失败模式记录**：A(RL 训练) / B(方向判断) / C(仿真器实现) / D(其他)，共 14 个模式 20 条案例
- **方法论适配性矩阵 + 已验证失败组合**：图结构 × 动作空间 × 学习范式
- **必做清单**：Simulator/ML/训练三层检查项
- **物理量语义检查**：高频混淆项及踩坑案例

## 使用场景

1. **选新方向前** → 先读 `directions-registry.md`（所有已探索/已排除方向）+ `code-quality.md` 失败模式 B 类
2. **设计 baseline 前** → `code-quality.md` 必做清单 + 同领域项目的 baseline_report.md
3. **搭仿真器前** → `code-quality.md` 必做清单 + `reference/sim-template/`
4. **选学习方法前** → `code-quality.md` 方法论适配性矩阵 + 已验证失败组合
5. **跨对话恢复** → 先读本文件了解全局，再读具体项目 handoff
6. **归档/转阶段时** → 更新本文档对应项目条目

## 框架改进待办

- [ ] **归档时更新**：decision_log 标记归档时，同步更新 projects-overview.md
- [ ] **转阶段时更新**：handoff 写入时检查是否需更新本文件阶段标记
- [x] **CLAUDE.md 引用**：已在"状态恢复"段落中加入 projects-overview.md 作为第 1 优先读取项
- [ ] **自动发现**：`projects/` 目录新增项目时提醒更新本文件
