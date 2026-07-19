# 项目总览

> 最后更新: 2026-07-19 | 活跃: 6 | 已归档: 5 | 总计: 11

## 活跃项目

### thesis-fso

- **方向**：双偏振星地 OSL 场景中的 ML 应用方向探索；正式研究与 Direction Lab Scout/Sandbox 分层管理。
- **正式状态**：`BLOCKED`。Direction Lab 的 exploratory evidence 对正式 Groundwork/论文 promotion effect 为 `none`。
- **Direction Lab Sandbox 历史**：B003 已完成，状态 `COMPLETED_SANDBOX_VERIFIED`；批次事实以 completion events 和不可变 projection 为证据，B001–B003 数字均不可进入论文或正式材料。
- **当前 Scout**：P03/U19 Headroom Atlas Stage A 已完成（2026-07-19，S077/D059/V033）。runnable 代表子域（QPSK × SNR 5–25 dB × f_G 30/100/1000 Hz × SOP 4e-6/4e-5 × N 512/8192 × CSI_NONE × uncoded hard decision，11 cells × 10 paired seeds）`LOCAL_NEGATIVE`：0/11 cells 达 MDE 0.005，max visible headroom 0.00039。candidate 当前仍 `P03_DOMAIN_ADEQUACY_UNRESOLVED`（16QAM/receiver-CSI/coded-output 三轴 INFRASTRUCTURE_BLOCKED，历史反例落在被阻轴上），domain/family 未关闭，Sandbox `NOT_ENTERED`，Stage B 不触发。
- **下一合法边界**：用户决策点（未选定）：① P03 暂停回候选池；② 建一条干净 source closure（最有杠杆是 16QAM）扩域重跑 Stage A；③ 换候选族（U36 等）。要关 DOMAIN/CANDIDATE 必须先扩 closure 并带 scope certificate。不启动 B004，不训练 P03 ML，不创建 Queue/Registry。
- **Atlas 强门入口**：`projects/thesis-fso/direction-lab/scout/P03-U19-residual-headroom/headroom-atlas/atlas_gate.py`（唯一 receipt-bound 入口，19 tests 含独立对抗审查）。
- **入口**：`projects/thesis-fso/master-state.md` → `projects/thesis-fso/direction-lab/README.md`；机器状态溯源见 `projects/thesis-fso/direction-lab/state/completion-events.jsonl` 与 `state/projections/`，`canonical-state.yaml` 不是正式研究授权源。

### leo-mega-constellation-gnn-routing

- **方向**: GNN 在 LEO 路由中的场景适配与实证验证 — 小星座训练零样本泛化到Starlink级路由
- **阶段**: Execute P0 完成 → paper-materials 待重写 → 跨章交叉整理
- **关键技术**: GNN (GraphSAGE) + 位置编码 + 多尺度训练
- **关键结论**: 3-seed P0 实验完成（stretch=1.099±0.012, delay=66.84ms, ≤1.2x%=86.2%，训练精度97.5%）。消融验证：PE是学习必要条件（无PE≈随机40%），多尺度有贡献（+2pp）。同规模完美（stretch=1.000）。Delay retention=109.9%
- **领域验证**: Size generalization 是 GNN 理论问题非 LEO 路由领域挑战，叙事改为"跨领域迁移"。Li 2026 排除（子agent幻觉）
- **待补**: random_pe (~20min), E06/E08 (P1), paper-materials重写
- **handoff**: `.sessions/2026-05-13-mega-constellation-gnn-routing/H008-0514-step5.md`

### leo-ntn-handover-drl

- **方向**: GNN-DRL 在 LEO 切换中的集中式架构设计与评估 — 二部图GNN+DDQN实现切换规模迁移
- **阶段**: Execute 完成 → 审计完成(S003) → 待补实验(多seed+N=30/40+乒乓切换率)
- **关键技术**: 二部图GNN + DDQN + top-K动作压缩
- **关键结论**: 二部图GNN+DDQN，top-K压缩是决定性改进。M4 Jain已修复
- **待补**: 多seed验证(~6h，但Ch1经验表明可能偏高10x)、N=30/40规模实验、乒乓切换率指标
- **教训**: 初始叙事（GNN提升绝对性能）在小规模不成立，及时转向规模迁移救活项目；叙事转向需系统性实验支撑
- **handoff**: 无专用session目录（决策记录在项目目录内）

### hgat-satellite-dag-offloading

- **方向**: HGAT增强的卫星-地面协同边缘计算DAG依赖任务卸载
- **阶段**: GW Stage 7 完成 — 待评估是否继续
- **关键技术**: 异构图注意力网络(HGAT) + PPO
- **关键结论**: 4模型×3seed全部收敛但peak相当(-11.6~-12.0)；HGAT仅训练稳定性领先(mean -138 vs MLP -331)；零样本泛化(10→50 IoTD) GCN(-79)优于HGAT(-118)，核心假设被推翻
- **教训**: type_bias+type_proj补丁让同构模型追平HGAT；GCN谱卷积泛化优于HGAT attention；异构性需求不够强，同构架构可近似恢复类型信息
- **handoff**: `.sessions/2026-05-20-hgat-dag-offloading/H001-simulator-training-status.md`

### leo-congestion-routing

- **方向**: GNN 在 LEO 故障弹性路由中的鲁棒性验证 — 拥塞感知路由+负载均衡 for LEO 卫星星座
- **阶段**: Execute 全部完成（拓扑升级+GPU重跑+paper-materials重写）→ 论文写作
- **关键技术**: Walker-Delta 物理仿真(alt=550km, inc=86.4°, polar_gap=70°) + M/M/1排队延迟模型 + GNN message passing
- **关键结论**: GNN/ECMP delay=0.80, MLU=0.96, GNN/MLP delay=0.37。E2E delay为主指标（非MLU ratio）。E12故障模式11/12赢。学位论文章节够用
- **待补(可选)**: delay敏感性分析+DRL baseline (投期刊时)
- **教训**: K-path 范式迁移（D15）是关键架构决策——从 per-flow 路由改为 per-edge 权重；TELGEN (Zhou'25 ToN) 是最强竞品，差异化靠 LEO 时变拓扑
- **handoff**: 无（项目可直接进入论文写作）

### nfv-sfc-vne

- **方向**: 双层图匹配(MatchingGAT) + SFC 依赖链约束的跨规模 VNE
- **阶段**: Execute E1 待重跑（架构 bug 修复后）
- **关键技术**: MatchingGAT（逐节点交互 cross-attention）+ Node-Edge 联合嵌入
- **关键结论**: MVE 确认 GNN > MLP +9.7%（R2C），GNN > 启发式 +37.8%；GW baseline MatchingGAT R2C=0.790 > DualGAT+ 0.756（+4.5%）；架构 bug 修复后 5ep 验证趋势向好
- **风险**: E1 完整实验尚未用修复后架构跑；+4.5% 接近 +5% 假设门槛；TELGEN 竞品存在
- **handoff**: 无

## 已归档项目

### leo-resilient-routing

- **方向**: LEO故障感知抗毁路由（GNN→MARL+课程学习+主动预路由）
- **归档原因**: MVE三轮失败：(1) GNN不优于MLP(18/60节点); (2) MARL课程学习+2.2%未达门槛; (3) 主动预路由反而更差(-1.3%); 与beam-hopping/ISL-scheduling同模式：网格拓扑正则→启发式够用→ML无优化空间
- **关键失败教训**: Walker星座网格拓扑太规则，贪心路由92%投递率，RL仅5%；LEO路由/调度/波束跳三个子方向全部归档，信号一致：物理约束主导问题不适合ML
- **handoff**: `.sessions/2026-05-16-leo-resilient-routing/H004-step4a-pivot.md`

### ris-phase-drl

- **方向**: DRL优化大规模RIS(100+元素)连续相移
- **归档原因**: CCAN+TD3/SAC 四轮验证 avg 全部停在 Fixed(θ=π) 水平（<1.5% 改善）。根因：Rician LoS 主导(κ=10dB)下最优策略≈Fixed，NLoS 自适应空间极小；off-policy RL 的 replay buffer 稀释好策略样本。Best=1670 远超 PSO=1554 说明架构容量够，但训练无法稳定输出好策略。
- **关键失败教训**: 物理约束（LoS 主导）决定最优策略≈固定值的问题不适合 RL；MVE 通过（TD3=40×Random）但 formal 训练失败说明 MVE→Formal 差距可能致命；Critic 瓶颈假设被推翻（换 CCANCritic 结果相同），问题在训练动力学而非架构
- **handoff**: `.sessions/direction-scouting/H013-ris-phase-drl-status.md`

### leo-isl-scheduling-drl

- **方向**: GNN拓扑编码+DRL用于LEO巨型星座ISL细粒度三态调度
- **归档原因**: 7种方法(PPO/REINFORCE/swap/ILP标签/grid标签/动态场景RL/全规模swap)全部未超越先验; grid拓扑在24×20和24×66均近最优; 物理结构决定性能与beam-hopping同模式
- **关键失败教训**: 物理约束主导的问题不适合RL; 全局reward+逐边动作的credit assignment与规模无关; ILP标签是代理目标(容量≠吞吐量)
- **handoff**: `.sessions/2026-05-16-isl-scheduling-drl/H018-dynamic-scenario-stuck.md`

### leo-beam-hopping-gnn

- **方向**: GNN建模多波束LEO卫星Beam Hopping波束间空间干扰耦合
- **阶段**: 归档 — 6种方法全部失败
- **归档原因**: 干扰是beam pair物理关系，无法从标量奖励通过梯度学习；action space(top-K离散选择)与图结构干扰关系根本不匹配
- **关键失败教训**: Gaussian policy + top-K→信用分配稀疏（19维仅5维有梯度）；奖励被fairness主导82%可学信号仅7%；成功GNN论文均用监督学习非RL；MVE训练不稳定是预警信号
- **handoff**: `.sessions/2026-05-15-beam-hopping-gnn/H009-archive.md`

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
