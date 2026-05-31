# Decision Log

## 阶段摘要
- [Direction Scouting] 方向侦察完成，作为备选第二研究方向
- [Groundwork] Step 1-2 检索+初筛完成，Step 3 精读完成（7 篇），Step 3.5 补充检索完成，Step 4a Conditional Go
- [Pivot] D006: 方案从 GNN 策略网络+RL+top-K pivot 到 MA-DRL (QMIX/QPLEX) + GNN encoder + per-cell binary action（路径 B）
- [Kill] D007: QMIX+GNN MVE 再次失败，方向归档

## 决策记录

### D005: Step 4a Go/No-Go 可行性判断 (2026-05-16)
- **输入**: literature_notes.md (14 篇必读), feasibility_report.md
- **结论**: **Conditional Go**
- **A0 问题-方法适配性**: 5/5 全部通过（性能间隙≥30%, 4/4 结构适配, ≥4 先例, MDP 非平凡, 无负面证据）
- **A 结构优势**: 空间干扰建模 + 独立 agent 信息损失 + 可扩展性（L03 zero-shot 19→61 cells）
- **B 新颖性-可行性解耦**: 空白="没人想到"+"技术壁垒刚解除"，可行性有 4 篇强先例支撑
- **D MVE 结果**: FAIL（GNN 排名最差），但关键发现：
  - IA-Greedy >> Greedy 50%，**干扰拓扑重要性确认**
  - GNN+REINFORCE 训练不稳定（高方差），非架构问题
  - 19 cells 太小，GNN 可扩展优势无法体现
- **改善路径**: PPO 替代 REINFORCE + reward shaping + 更大规模环境
- **风险**: GNN 在小规模训练不稳定，需在正式仿真器验证
- **产物**: `feasibility_report.md`, `mve_gnn_vs_fc.py`
- **用户确认**: （待确认）

### D004: Step 3.5 补充检索完成 (2026-05-16)
- **输入**: 4 轮定向检索（GAT+BH, HGNN+卫星, GNN+离散调度, GNN+size generalization）, 引用链分析（L05/L07）
- **结论**: 补充检索收敛，GNN+BH 从"零竞争者"下调为"近乎零竞争者"
- **关键发现**:
  - 120 条新检索结果中仅 1 篇直接竞品：M14 异构图+DRL 做 BH（AIAC 2024, 1cit, 会议论文）
  - 2 篇候选（IEEE 11208547/11264375）经 abstract 交叉验证为误检
  - 方法迁移参考：size generalization GNN (13cit), HGNN for LEO (2cit), GNN 离散用户调度
  - OpenAlex 引用链分析对 L05/L07 返回 0 结果（论文过新未被索引）
  - 检索充分性检查通过：关键词矩阵覆盖✓, 搜索源覆盖✓, 收敛性✓
- **质量门槛**: 5/5 全部满足
- **产物**: 4 个补充检索 JSON + 更新后的 `literature_notes.md`

### D003: Step 3 精读 7 篇完成 (2026-05-16)
- **输入**: L01 Yang Tyche JSAC, L02 Zhang DynHGNN TWC, L03 Geng Meta-GNN TVT, L04 Lin Graph+GAN ICT Express, L05 Gong QPLEX TWC, L06 Lin QMIX-BH TVT, L07 Wang Cooperative BH TWC
- **结论**: 7 篇精读完成，综合分析已撰写，质量门槛全部通过
- **关键发现**:
  - MA-DRL >40小区收敛困难实证确认（L01 Tyche JSAC）
  - GNN 在卫星干扰/功率分配已成熟（L02 DynHGNN 超图, L03 Meta-GNN 泛化）
  - graph mapping 首次引入 BH（L04）但非 GNN
  - 分层 MA-DRL 是主流（L05 QPLEX 分层, L06 QMIX 两阶段, L07 三层解耦）
  - 所有 MA-DRL 均用 FC 网络，无图结构感知，这是可超越的关键点
  - GNN+BH 仍为零，创新空白确认
- **质量门槛**: 4/4 全部通过（精读7≥5✓, Baseline非空✓, 核心贡献≥2句✓, 综合分析✓）
- **产物**: `literature_notes.md` 精读笔记 L01-L07 + 综合分析

### D006: Pivot 路径 B — MA-DRL + GNN encoder (2026-05-16)
- **输入**: code-quality.md 失败模式(A1/A3/B1), 前一轮项目 D011/D013 归档结论, MVE v1-v3 全败
- **结论**: **Pivot** — 放弃 GNN 策略网络 + RL + top-K 方案，转向路径 B
- **根因**:
  - 前一轮 leo-beam-hopping-gnn 已用 6 种方法全败（D013），包含 PPO+GNN、DiffGNN、REINFORCE+softmax
  - D011 明确推翻了"换算法解决"的判断："问题不在算法稳定性而在 action space 设计"
  - top-K 不可微 + 干扰是 beam pair 物理关系，标量奖励梯度无法学习
  - B1 假蓝海预警：零 GNN 竞争可能是不值得做的信号
- **新方案**: MA-DRL (QMIX/QPLEX) + GNN encoder + per-cell binary action
  - 对齐 FR-08：跟随成功论文范式（L05 QPLEX, L06 QMIX 用 Q-learning 系；L02 DynHGNN 用 GNN+RL）
  - GNN 角色：从"策略网络"变为"Q-value backbone"，编码邻居干扰状态
  - 信用分配：QMIX/QPLEX mixing network 解决多 agent 协作
- **待办**: 定向检索 GNN+QMIX/QPLEX / GNN encoder+MARL，确认创新空间
- **用户确认**: ✅

### D007: Kill — QMIX+GNN MVE 失败，方向归档 (2026-05-16)
- **输入**: mve_qmix_gnn.py 运行结果 (3 seeds), code-quality.md 失败模式, 前一轮项目 D011/D013
- **结论**: **Kill** — GNN+BH 方向归档
- **v2 MVE 结果** (QMIX+GNN):
  | 方法 | Throughput |
  |------|-----------|
  | GNN+QMIX | 6.58 ±0.15 |
  | FC+QMIX | 7.42 ±0.55 |
  | Random | 7.63 |
  | IA-Greedy | **10.38** |
- **根因分析**:
  1. QMIX mixer 已有全局状态，GNN encoder 邻居信息完全冗余（FR-09）
  2. 空间隔离约束需显式执行（顺序选择+遮蔽），不能通过 RL 隐式学习（FR-10）
  3. 同时决策场景下 agent 看到邻居状态但看不到邻居动作意图
- **累计证据**: 2 个项目 × 4 种 RL 算法 (REINFORCE, PPO, DiffGNN, QMIX) × 2 种规模 (N=19, N=37) = 全部失败
- **教训写入**: code-quality.md A3(更新), A5(新增), B1(更新), FR-09(新增), FR-10(新增)
- **用户确认**: ✅

### D001: AI 候选审查完成 (2026-05-16)
- **输入**: 5个JSON检索文件，~150条原始结果
- **结论**: 去重后~70篇相关论文，13篇必读，4个子方向覆盖
- **关键发现**:
  - GNN+BH=0 完全空白（二轮深搜119条追加确认）
  - MA-DRL>40小区收敛困难（Yang 2025 Tyche JSAC确认）
  - 唯一图方法BH论文（Lin 2025 graph+GAN）为切入点参考
- **质量门槛**: 全部通过（去重70≥20, 必读13≥5, 4个子方向≥2, 正式发表~75%≥50%）
- **产物**: `literature_notes.md`
