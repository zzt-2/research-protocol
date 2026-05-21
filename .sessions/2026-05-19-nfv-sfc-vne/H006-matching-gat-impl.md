# Handoff: MatchingGAT 实现完成 + 训练验证

> 来源: Step 7 Part C | 交接目标: 续接正式训练 + 消融实验
> 文件名: H006-matching-gat-impl.md

## 已完成边界

### MatchingGAT 核心创新实现（M3）
- `Virne/virne/solver/learning/sfc_solver/matching_policy.py` — 核心模型
  - MatchingGATBaseModel: 独立双图编码 → SFC embedding → 跨图 matching attention → 打分
  - MatchingGATActorCritic: 注册为 'matching_gat'
  - MatchingGATPolicyBuilder: build_matching_gat_policy(agent) 策略构建
  - obs_as_tensor_for_matching_gat(): SFC metadata 作为 PyG Data 属性
- `Virne/virne/solver/learning/sfc_solver/sfc_matching_env.py` — SFC obs 注入
  - SFCMatchingInstanceRLEnv: get_observation() 注入 sfc_vnf_types + sfc_positions
- `sfc_baselines.py` 更新: 注册 sfc_ppo_matching_gat solver
- `__init__.py` 更新: 导出 MatchingGATActorCritic

### 训练结果（5 epochs, 500 VNRs/epoch, SFC ratio=0.6）

| Solver | AC | R2C |
|--------|------|------|
| GRC | 0.836 | 0.543 |
| pg_mlp (30ep) | 0.908 | 0.599 |
| DualGAT+ (5ep) | 0.918 | 0.676 |
| **MatchingGAT (5ep)** | **0.986** | **0.789** |

R2C 提升: MatchingGAT vs DualGAT+ **+16.7%**, vs GRC **+45.2%**

### 训练曲线
| Epoch | success_count | R2C | LogProb |
|-------|------|------|---------|
| 0 | 443 | 0.523 | -4.391 |
| 1 | 470 | 0.615 | -3.612 |
| 2 | 487 | 0.719 | -2.591 |
| 3 | 491 | 0.759 | -1.868 |
| 4 | 495 | 0.773 | -1.613 |
| val | — | 0.789 | — |

### 后台运行任务
- DualGAT+ 30 epoch 训练已启动（task ID: bn7nd3g60），预计 ~80 min
- 完成后结果在: `results/sfc_ppo_dual_gat+_seed0.txt` 和 `results/dual_gat_30ep.log`

## 不要做什么

- 不要修改 Virne 核心代码（feature_constructor.py, policy_builder.py 等）—— MatchingGAT 全部通过扩展实现
- 不要把 SFC features 混入 v_net.x（通过 obs dict 单独传递，保持特征维度不变）
- 不要跳过 DualGAT+ 30ep 公平对比——5ep DualGAT+ 不是公平 baseline
- 消融实验中，不要同时去掉多个组件——每次只去掉一个

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态（优先读）
2. `projects/nfv-sfc-vne/baseline_report.md` — 最新训练结果
3. `projects/nfv-sfc-vne/simulator-design.md` §8-9 — 实验配置矩阵 + 消融设计
4. `projects/nfv-sfc-vne/Virne/virne/solver/learning/sfc_solver/matching_policy.py` — 核心模型代码

## 下一轮

1. **检查 DualGAT+ 30ep 训练结果** — `cat results/dual_gat_30ep.log | grep epoch`
2. **MatchingGAT 30ep 训练** — 确认完整训练后 R2C 仍领先
   ```
   ~/.venvs/torch/bin python verify/run_sfc_baselines.py --solver sfc_ppo_matching_gat --epochs 30 --vnr 500
   ```
3. **消融实验代码** — 3 个消融变体（去 SFC PE / 去 cross-attn / 去 edge_attr）
4. **多拓扑验证** — GEANT/BRAIN/WX500 配置
5. **进入 Contract 阶段** — 读 `stages/contract.md` 开始正式实验设计
