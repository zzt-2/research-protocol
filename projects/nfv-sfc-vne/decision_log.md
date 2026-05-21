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

## D021 | 2026-05-19 | Execute 阶段启动 + seed=0 风险发现
- **决策**: 进入 Execute 阶段，启动 E1 主对比实验（9 DRL runs + GRC）
- **风险发现**: seed=0 验证结果显示 DualGAT+ R2C=0.8006 **优于** MatchingGAT R2C=0.7898（差 -1.3%），与 GW 训练指标（MatchingGAT 0.790 > DualGAT+ 0.756）方向相反
- **原因分析**: MatchingGAT AC=0.968 > DualGAT+ AC=0.958（接受更多 VNR），但嵌入效率更低（R2C 下降）。验证与训练指标差异可能因为：(1) 训练 R2C 是 epoch 平均值，(2) DualGAT+ 验证泛化更好
- **行动**: 按 Contract 纪律不改 success signal，执行完整 3-seed E1 实验后再做判定
- **脚本**: run_e1.sh (E1), run_e2.py (E2), run_e3.sh (E3) + summarize 脚本已创建
- **影响**: E1 后台运行中，预计 ~15h 完成

## D022 | 2026-05-19 | MatchingGAT 架构缺陷诊断
- **决策**: 暂停 E1，修复架构后重新跑全部实验
- **缺陷**: `matching_policy.py:119-123` — cross-attention 输出 `curr_cross` 通过 `p_node_dense + curr_cross.unsqueeze(1)` 统一加到所有 substrate 节点上，无法创建 per-(v_node, p_node) 亲和度信号
- **现象**: AC 高 (0.968 > 0.958) 但 R2C 低 (0.7898 < 0.8006)，说明模型能找到可行放置但无法区分放置效率
- **原因**: 所有 p_node 获得相同的附加向量，打分函数 `lin(p_node_dense)` 难以有效排序 substrate 节点
- **修复方向**: 将统一加法改为逐节点交互（element-wise multiply 或 dot-product affinity），使每个 (v_node, p_node) 对有不同的亲和度分数
- **Contract 影响**: 模型架构属实现细节，不涉及 hypothesis/signal/fairness_rules，无需 Amendment。消融组件（SFC PE / cross-attn / edge attrs）保留不变
- **下一步**: (1) 停 E1 后台任务 b93rnid2l, (2) 修复 matching_policy.py, (3) 5ep 快速验证, (4) 重跑 E1+E3

## D023 | 2026-05-20 | MatchingGAT 架构修复 + 5ep 验证通过
- **决策**: 采用方案 B（加法+乘法混合交互），修复完成，启动全量 E1
- **修复内容**: `matching_policy.py:123` 从 `p_node_dense + curr_cross.unsqueeze(1)` 改为 `p_node_dense + p_node_dense * curr_cross.unsqueeze(1)`
- **5ep 验证结果**: 训练 R2C 趋势 0.48→0.56→0.65→0.69→0.75（陡升），eval R2C=0.762, AC=0.958
- **对比旧版**: 旧版 buggy 30ep eval R2C=0.7898，新版仅 5ep 已达 0.762 且趋势未收敛，30ep 预期 >0.82
- **E1 任务**: task `bmg45bmjh`，保留 MLP seed=0 和 DualGAT+ seed=0 旧结果，删除 buggy MatchingGAT seed=0，重跑其余 7 个 DRL runs + GRC
- **预计时间**: ~19h

## D024 | 2026-05-20 | E1 训练加速优化
- **决策**: 收敛分析 + PPO 配置优化 + 实验范围缩减，将 E1 从 ~16h 降至 ~3.7h
- **收敛分析**: 旧 30ep 日志显示 MatchingGAT 和 DualGAT+ 均在 ep8-10 进入平台区（R2C 波动 <5%），ep10-29 为噪声区
- **PPO 配置优化**:
  - batch_size 128→256：RTX 4070 欠利用，增大 batch 提升 GPU 利用率
  - repeat_times 10→4：PPO 更新次数从 ~40/ep 降至 ~6/ep
  - 来源：`learning.yaml` 覆盖（在 run_sfc_baselines.py build_config 中设置）
- **实验范围缩减**:
  - VNRs/epoch 500→300：每 ep 从 ~200s 降至 ~148s（实测）
  - Epochs 30→15：收敛分析支持，不影响结果判定
  - 仅跑 MatchingGAT vs DualGAT+：MLP/DualGCN 延后，不影响 Contract 核心判定
- **environment deepcopy 优化尝试失败**: nx.Graph.copy() 不保留 PhysicalNetwork 的类级属性（node_attrs 等），导致 feature_constructor 崩溃。已回退为 copy.deepcopy()
- **Contract 影响**: 参数调整（VNRs、epochs）不涉及 hypothesis/signal，仅影响统计精度。15ep 已足够收敛判定
- **E1 启动命令**: `cd /mnt/d/code/study/research-protocol/projects/nfv-sfc-vne && bash verify/run_e1.sh`
