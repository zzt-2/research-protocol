# Handoff: Step 6 设计确认 → Step 7 实现

> 来源: Step 6 仿真器设计 | 交接目标: Step 7 仿真环境搭建 + Baseline 复现
> 文件名: H004-step7-implement.md

## 已完成边界

1. **Step 4a**: A0/A'/A/B/D 全通过，MVE PASS，用户已确认 Go
2. **Step 5**: Baseline B1-B5 选定，用户已确认
3. **Step 4b**: C/E 无致命信号，用户已确认 Go
4. **Step 6**: 仿真器设计规格完成，用户已确认 Go
   - 关键决策：VNR 拓扑保持 random graph + SFC 约束叠加层（非纯 chain）
   - 关键决策：沿用 fixed_intermediate 奖励
   - FR-12：2 项架构差异，均有可证伪条件，无需新 MVE

## 不要做什么

- 不要把 VNR 拓扑改为纯 chain（B3 风险：GNN 优势消失）
- 不要在奖励函数中添加 SFC 分量（C1 风险：奖励失衡）
- 不要修改 Virne 核心源码（通过子类继承扩展）
- 主对话不要直接 webSearch/webReader
- 不要跳过 MDP 试运行检查（Part A-checkpoint）

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态
2. `projects/nfv-sfc-vne/simulator-design.md` — **仿真器设计规格（Step 7 的核心输入）**
3. `stages/gw-experiment.md §impl` — Step 7 框架（Part A/B/checkpoint）
4. `code-quality.md` — 必做清单 + 常见缺陷表
5. `reference/sim-template/` — 代码模板（config/env/model/reward/verify）
6. `projects/nfv-sfc-vne/Virne/` — Virne 仿真器（已验证可用）

## 下一轮

### Step 7 实现（按 gw-experiment.md §impl）

1. **Part A：仿真环境搭建 + 验证**
   - SFC-enhanced VNR 生成器（继承 VirtualNetwork）
   - SFC 约束环境（继承 JointPRStepInstanceRLEnv）
   - 验证清单：解析/统计/退化/SFC 专项
2. **Part A-checkpoint：MDP 试运行**
   - 1 episode 随机 + 1 episode 贪心
   - 奖励分解 + domination threshold 检查
3. **Part B：Baseline 复现**
   - 先跑 GRC（21s）确认 SFC 环境有非零 AC
   - 再跑 pg_mlp（~170s/ep）和 PPO-DualGAT+（~412s/ep）
   - 趋势验证：DualGAT > MLP > GRC

### 实现优先级

1. SFC VNR 生成器 → 2. SFC 约束环境 → 3. 验证套件 → 4. GRC baseline 测试 → 5. MDP trial → 6. MatchingGAT policy → 7. 全 baseline 训练

### 关键架构信息

**Virne 核心路径：**
- Solver 注册：`virne/solver/` 下各子目录，`@SolverRegistry.register` 装饰器
- 环境：`virne/solver/learning/rl_core/instance_rl_environment.py`
  - `JointPRStepInstanceRLEnv`（Place+Route per node）
- Policy：`virne/solver/learning/rl_policy/dual_gnn_policy.py`
  - `BiGnnBaseModel`：v_net_encoder + p_net_encoder → 跨图注意力
- Reward：`virne/solver/learning/rl_core/reward_calculator.py`
  - `FixedWeightRewardCalculator`：success=R2C, intermediate=0.1, failure=-0.1
- Config：`settings/main.yaml`（solver_name）、`settings/learning.yaml`（训练参数）

**SFC 扩展点：**
- VirtualNetwork：新增 sfc_chain 属性（VNF 节点 ID 列表 + vnf_type 标签）
- JointPRStepInstanceRLEnv：重写 generate_action_mask（SFC 可达性）+ 节点排序
- 新 Policy：CrossGraphMatchingEncoder（替换 BiGnnBaseModel）

### 预算

- Step 7 预算：5.0 USD / 15 min（Master 上下文限制）
- 实现可能需要多个子 agent / 新对话
- RTX 4070 训练时间：GRC ~21s, pg_mlp ~170s/ep × 30ep, DualGAT+ ~412s/ep × 50ep
