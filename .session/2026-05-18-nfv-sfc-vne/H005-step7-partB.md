# Handoff: Step 7 Part A 完成 → Step 7 Part B

> 来源: Step 7 Part A 实现 | 交接目标: Step 7 Part B（全 baseline 训练）
> 文件名: H005-step7-partB.md

## 已完成边界

1. **Step 6**: 仿真器设计规格完成，用户已确认 Go
2. **Step 7 Part A**: SFC 环境搭建 + 验证完成
   - M1: SFC VNR 生成器（sfc_chain.py + sfc_vnr_generator.py）— 17/17 验证 PASS
   - M2: SFC 约束环境（SFCJointPRStepInstanceRLEnv）— action masking + SFC 节点排序
   - M6: 验证套件 — 3 个验证脚本全部通过
   - GRC baseline: AC=0.96, R2C=0.55（50 VNRs, sfc_ratio=0.6）
   - MDP trial: 3/4 gates PASS，Gate 2 边界（8.45% vs 10%，单 episode 小 VNR 噪声）

## 不要做什么

- 不要把 VNR 拓扑改为纯 chain（B3 风险）
- 不要在奖励函数中添加 SFC 分量（C1 风险）
- 不要修改 Virne 核心源码（通过子类继承扩展）
- 不要跳过 Part B 的全 baseline 趋势验证
- 主对话不要直接 webSearch/webReader

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态
2. `projects/nfv-sfc-vne/simulator-design.md` — 设计规格（§8 实验配置）
3. `stages/gw-experiment.md §impl Part B` — Baseline 复现流程
4. `projects/nfv-sfc-vne/Virne/virne/network/sfc/` — SFC 数据模型
5. `projects/nfv-sfc-vne/Virne/virne/solver/learning/sfc_solver/` — SFC 环境

## 已实现的文件

```
projects/nfv-sfc-vne/Virne/virne/network/sfc/
├── __init__.py
├── sfc_chain.py              # SFC DAG 数据结构
└── sfc_vnr_generator.py      # SFC VNR 后处理生成器

projects/nfv-sfc-vne/Virne/virne/solver/learning/sfc_solver/
├── __init__.py
└── sfc_instance_env.py       # SFC-aware JointPR 环境

projects/nfv-sfc-vne/Virne/settings/sfc_setting.yaml  # SFC 配置

projects/nfv-sfc-vne/verify/
├── verify_sfc.py              # SFC VNR 生成验证
├── run_grc_baseline.py        # GRC baseline 测试
└── run_mdp_trial.py           # MDP 试运行
```

## 下一轮

### Step 7 Part B：Baseline 复现 + MatchingGAT policy

按 `gw-experiment.md §impl Part B` 执行：

1. **全 baseline 训练**（使用 SFC 环境）
   - B3 pg_mlp（~170s/ep × 30ep）— MLP 消融
   - B2 PPO-DualGAT+（~412s/ep × 50ep）— GNN SOTA
   - B4 CONAL、B5 PPO-DualGCN（后续可选）
   - 趋势验证：DualGAT > MLP > GRC

2. **MatchingGAT policy 实现**（M3）
   - 替换 BiGnnBaseModel，实现跨图 matching 层
   - 注册 `@ActorCriticRegistry.register('matching_gat')`
   - SFC 位置编码 + vnf_type 特征

3. **训练 + 超参搜索**
   - 场景 S1 (WX100) 主实验
   - 3 seeds，early stopping，wandb 集成

### 实现优先级

1. pg_mlp baseline（确认 SFC 环境下 RL 可训练）
2. PPO-DualGAT+ baseline（GNN baseline）
3. MatchingGAT policy（核心创新）
4. 全 baseline 对比实验

### 关键架构信息

**SFC 环境入口**:
```python
from virne.solver.learning.sfc_solver import SFCJointPRStepInstanceRLEnv
# 用于 InstanceAgent 的环境类
```

**SFC VNR 生成**:
```python
from virne.network.sfc import add_sfc_to_simulator
# 在 dataset 生成后调用
add_sfc_to_simulator(v_net_simulator, sfc_ratio=0.6, num_vnf_types=5, seed=42)
```

**Virne 训练入口**:
```bash
cd projects/nfv-sfc-vne/Virne
python main.py solver.solver_name=pg_mlp  # 通过 Hydra 切换 solver
```

### 预算

- Part B 预算：5.0 USD / 15 min per sub-agent
- RTX 4070 训练时间：pg_mlp ~170s/ep × 30ep, DualGAT+ ~412s/ep × 50ep
- 可能需要多个子 agent / 新对话完成全部训练
