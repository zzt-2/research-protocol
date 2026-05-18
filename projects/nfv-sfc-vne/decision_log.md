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
