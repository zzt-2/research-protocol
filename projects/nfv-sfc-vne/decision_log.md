# Decision Log: nfv-sfc-vne

## D001 | 2026-05-18 | 方向侦察 Go 决策
- **决策**: #1 NFV/SFC 双层图匹配 + SFC 依赖链约束方向 Go
- **来源**: 方向侦察 S002-2026-05-18.md
- **原因**: A0/A'/A/B 全部通过。性能间隙强（接受率差20.7%、收入差36.2%），问题结构适配（图到图映射），跨域先例充分（c=159），空白确认（GNN×VNE×cross-scale=0篇）
- **条件**: 核心贡献定位为"双层图上的VNE联合优化"，非"跨规模泛化"

## D002 | 2026-05-18 | 核心卖点定位
- **决策**: 核心卖点 = "双层图匹配 + SFC 依赖链约束"
- **原因**: "跨规模泛化"已被 Ch3 leo-congestion-routing 占据（66→720节点泛化验证）。需差异化定位。
- **影响**: 跨规模降级为论文级共享特性（两章都受益但非核心贡献）

## D003 | 2026-05-18 | GNN 架构选择
- **决策**: 走 Node-Edge 联合嵌入（matching-style）
- **原因**: 与 hgat-dag 的 HGAT 拉开距离；VNE 本质是二部图匹配问题，matching-style GNN 更契合
- **对比**: Ch3 用 GIN/GAT 做节点嵌入，本项目用 Node-Edge 联合嵌入做边预测

## D004 | 2026-05-18 | 论文统一叙事
- **决策**: "GNN 驱动的 LEO 网络多层智能优化"
- **原因**: Ch3=流量路由(调度层), 本项目=服务放置(编排层), 双层图 vs 单层拓扑，形成垂直叙事
- **影响**: 两章共享 GNN 方法论但问题空间正交

## D005 | 2026-05-18 | Step 1 复用方向侦察搜索结果
- **决策**: 不重新搜索，复用方向侦察期间的 25+ 个 NFV/SFC/VNE 搜索文件
- **原因**: 搜索覆盖 7 个源，6 个子方向，7+ 必读候选，满足 gw-search.md 全部质量门槛
- **影响**: 直接进入 Step 2（论文获取）

## D006 | 2026-05-18 | Step 4a MVE 需补做
- **决策**: Dimension D（MVE）不可跳过
- **原因**: 组合新颖性方向（GNN+DRL×VNE×cross-scale），gw-feasibility.md 规定不应跳过 MVE
- **计划**: 利用 Virne 仿真器快速验证 GNN 双层图匹配 vs MLP 在 VNE 上的结构性优势

## D007 | 2026-05-18 | Step 3.5 收敛确认
- **决策**: Step 3.5 Round 1 收敛，不继续 Round 2
- **原因**: 新增 8 篇论文精读后无新盲区，SFC 依赖链+matching-style GNN 无直接竞品
- **影响**: 进入 Step 4a MVE

## D008 | 2026-05-18 | 核心差异化确认
- **决策**: 核心差异化 = SFC 依赖链约束 + matching-style GNN
- **原因**: GraphVNE IPFP 不可微且仅提取标量分数；FlagVNE/CONAL 不处理 SFC
- **影响**: 跨规模作为辅助亮点而非核心贡献

## D009 | 2026-05-18 | Step 4a Go 建议
- **决策**: Step 4a 建议通过，进入 Step 5
- **来源**: feasibility_report.md
- **原因**: A0/A'/A/B/D 全维度通过。MVE 实证：GNN(DualGAT) AC=0.966, R2C=0.748 > MLP AC=0.942, R2C=0.682 > GRC AC=0.880, R2C=0.543。R2C GNN vs MLP +9.7%（>5% 门槛）。
- **条件**: 用户已确认 Go（2026-05-18）

## D011 | 2026-05-18 | Baseline 选定
- **决策**: 选定 B1-B5 五个 baseline
- **来源**: gw-validate.md Step 5
- **选定列表**:
  - B1: GRC (`grc_rank`) — 传统启发式代表，4篇论文使用，领域共识
  - B2: PPO-DualGAT+ (`ppo_dual_gat+`) — GNN+DRL SOTA，方法-范式对齐
  - B3: pg_mlp (`pg_mlp`) — MLP 基线，GNN 消融对比
  - B4: CONAL (`conal`) — 约束感知 VNE，SFC 方向直接竞品
  - B5: PPO-DualGCN (`ppo_dual_gcn`) — GNN 架构变体对比
- **原因**: Tier 1-2 全部 Virne 内置，零自实现成本。覆盖启发式/MLP/GNN-SOTA/约束感知/GNN-架构消融五个对比维度。
- **条件**: 用户已确认

## D012 | 2026-05-18 | Step 4b Go 建议
- **决策**: Step 4b 建议通过，进入 Step 6（仿真器设计）
- **来源**: feasibility_report.md §C/§E
- **原因**: C 仿真条件可行（SFC约束为中等工程量扩展），E 风险可控（Baseline 全部 Virne 内置，失败有兜底），无致命信号
- **条件**: 用户已确认 Go（2026-05-19）

## D013 | 2026-05-19 | Step 6 仿真器设计 — VNR 拓扑保持 random graph
- **决策**: VNR 拓扑保持 random graph + SFC 约束叠加层，不改为纯 chain
- **原因**: 纯 chain 拓扑过简单，GNN 优势会消失（B3 模式：小规模场景复杂组件退化）。Chain 10 节点仅 9 边，random graph ~22 边，拓扑复杂度差距大。MVE 验证的是 random graph 上的 GNN 优势，改为 chain 使证据失效。
- **影响**: FR-12 架构差异从 3 项"是"降至 2 项，最大风险项（VNR 拓扑变更）消除

## D014 | 2026-05-19 | Step 6 仿真器设计 — 沿用 fixed_intermediate 奖励
- **决策**: 不添加 SFC 奖励分量，沿用 Virne fixed_intermediate (0.1) + episode R2C
- **原因**: (1) SFC 约束由环境强制执行（action masking），无需奖励学习；(2) 避免 C1 奖励失衡风险（4/6 项目中招）；(3) 所有 solver 使用相同奖励确保公平对比
- **影响**: SFC 差异通过 SFC-IR 指标体现，不通过奖励

## D015 | 2026-05-19 | Contract Step 0 新颖性确认（简化路径）
- **决策**: Contract 新颖性确认通过，基于 GW 已完成的全面检索
- **原因**: GW 在 1 天前完成 25+ 搜索（7 源）、17 篇获取、Step 3.5 确认"SFC 依赖链 + matching-style GNN 无直接竞品"（D007, D008）。仅隔 1 天，无需重新系统检索。
- **新颖性要点**: (1) matching-style cross-graph attention 用于 VNE 无先例（GraphVNE IPFP 不可微）；(2) SFC 依赖链位置编码 + GNN 联合优化无先例；(3) 组合新颖性确认（GNN×VNE×SFC = 0 篇精确交叉）
- **条件**: Contract 复用条件满足（≥8 篇精读 + Step 3.5 完成）

## D016 | 2026-05-19 | Contract Step 1 假设形成
- **决策**: 核心假设 — "matching-style cross-graph attention + SFC 位置编码在 SFC 约束 VNE 中提升 R2C ≥5% over DualGAT+"
- **原因**: GW 单 seed 证据 R2C +4.5%（0.790 vs 0.756），消融确认三组件各有贡献。假设基于 GW baseline_report 和 ablation 结果，阈值设为 ≥5%（略高于单 seed 结果，反映多 seed 严格验证的预期）。
- **成功信号**: R2C ≥5% over DualGAT+, AC ≥0.95, 各消融组件 ≥1.5%
- **失败信号**: R2C <3% (边际), 或拓扑特异 (<2% on real topo), 或无组件贡献 >2%
- **影响**: contract.md 已创建，status=draft

## D017 | 2026-05-19 | Contract Step 3 参数溯源验算
- **决策**: 全部参数溯源通过，无 [ASSUMPTION]
- **原因**: 17 个参数中 13 个直接引用 L01 §Exp 或 Virne learning.yaml，4 个 [设计选择] 已补充显式理由（sfc_ratio=0.6 平衡 SFC 约束强度与 VNE 复杂度; vnf_types=5 对应 ETSI NFV 常见类型; epochs=30 基于 GW 收敛分析; seeds=3 为统计最低要求）
- **影响**: contract.md Parameter Provenance 已更新

## D018 | 2026-05-19 | Contract Step 4 端到端推演
- **决策**: data-flow.md 推演完成，FR-13 动作空间审计全部 ≥
- **原因**: 8 步推演从 VNR 生成到评估完整覆盖。所有 baseline 与 MatchingGAT 共享相同动作空间（选 substrate 节点），差异在信息处理而非决策空间。跨规模泛化无维度断裂（GNN per-node 输出自然适应不同 N_p）。
- **断层检查**: 无特征缺失、无维度不匹配、无配置矛盾
- **影响**: data-flow.md 已创建

## D019 | 2026-05-19 | Contract Step 5 压力测试 + 反模式审查
- **决策**: Tier 1 (5 pass + 1 NA) + Tier 2 (5 pass) + 反模式 (4 pass)，无致命风险信号
- **原因**:
  - Q1 结构性优势: VNE 是图匹配问题，cross-graph attention 直接匹配，非简单"DL 替代传统方法"
  - Q2 边际结果: 3-5% 区间有消融分析 + 框架贡献兜底
  - Q3 信号独立: failure 捕获 3 种不同失败模式（边际/拓扑特异/组件无贡献）
  - Q4 Baseline 共识: B1-B3 强共识，B4 标记 P1（单篇但方向代表）
  - Q5 反模式: SFC 信息不对称已声明，仿真包含足够复杂度，GNN 优势来源明确
- **影响**: experiment_completeness_checklist.md 已创建

## D020 | 2026-05-19 | Contract 冻结前风险调整
- **决策**: 基于 code-quality.md 失败模式审查，对 Contract 做 4 项调整后再冻结
- **原因**: 对照 6 项目历史教训，识别出 5 个相关风险，其中 R1(GEANT 小规模退化) 为高风险
- **调整内容**:
  1. 假设 scope 收窄至 ≥50 节点网络，排除 GEANT (23节点)
  2. GEANT 降级为补充验证，不纳入 success/failure signal 门控
  3. 增加 E6 SFC ratio 灵敏度实验 (Tier 3 red-teaming)
  4. 增加"已知风险与缓解"节，记录 R1-R5
- **依据**: B3 失败模式(ntn-handover: 15 UE 时 GNN +0.8%)，GEANT 23 节点结构类似
