# Handoff 2026-05-15 (Round 14) — Execute Step 0-1 完成诊断

## 当前进度
- **阶段：Execute Step 0-1（Quick Test 完成，E01 未开始）**
- Contract 状态：**frozen**
- 本轮完成：模型实现 + 训练循环 + 5 轮 Quick Test 诊断 + 全规模 timing 测量
- **需要新对话做方向性决策**（当前方法可能走进了死胡同）

## 核心问题：PPO 未能超越先验

### Quick Test 完整结果 (24×20=480 卫星)

| 版本 | 配置 | M1 | M3(切换率) | 训练 reward | 评估 reward | B1 M1=0.1035 |
|------|------|-----|-----------|-------------|-------------|-------------|
| v1 | 无 bias, std=0.14 | 0.003 | 16.7 | -19.97 | -19.9 | 完全失败 |
| v2 | active_bias=3, std=0.018, KL stop@15ep | **0.078** | **0.10** | -14.2 | **-3.29** | 最佳但过早停止 |
| v3 | active_bias=3, std=0.14, KL=5 | stuck | - | -19.5 | - | 大噪声退回随机 |
| v4 | active_bias=3, std=0.018, 无 KL stop, 100ep | 0.057 | 0.55 | -15.3 | -9.23 | 过训练退化 |
| v5 | active+distance bias, std=0.018, 低LR, 30ep | 0.078 | 0.03 | -3.3 | **+0.78** | PPO几乎无改善(+0.0006) |

### 关键发现

1. **先验做主功，PPO 几乎无用**
   - `active_bias=3` + `distance_bias=2`（未经训练）→ M1=0.077（B1 的 75%）
   - PPO 微调 30 episodes 后 M1=0.078（仅 +0.0006）
   - 先验策略：保持活跃 ISL + 选最短距离边 ≈ 简化的 B1

2. **KL 爆炸是小 std 的必然结果**
   - std=0.018 时，PPO 更新导致 Δμ/σ² ≈ 15+ 的 KL
   - 无论 LR 多小（试过 1e-5），PPO 更新都会在小 std 下产生巨大 KL
   - 放宽 KL 阈值 → 过训练退化（v4: 100ep M1 从 0.078 降至 0.057）

3. **大 std 导致随机探索失败**
   - std=0.14 时，top-K 选择被噪声主导 → 每步切换所有 ISL → M1=0.003

4. **训练 vs 评估差距大**
   - v5 训练 reward=-3.3，评估 reward=+0.78
   - 原因：训练时探索噪声破坏拓扑稳定性，评估时确定性策略保持稳定

### 性能瓶颈

| 组件 | 24×20 (480星) | 24×66 (1584星) |
|------|---------------|----------------|
| 候选边数 | 5,328 | **65,664** |
| env.step | 0.18s | **0.60s** |
| model forward (GPU) | 73ms | ~300ms (估计) |
| 50 episodes 总时间 | ~18 min | ~25 min |
| PPO batch (32 obs) | 4.3ms/obs | ~50ms/obs (估计) |
| 全量内存 (32 obs batch) | ~40MB | **~300MB+** |

### 全规模 (24×66) 未测项
- B1 全规模 M1=17.09%（来自 GW 阶段）
- 模型纯先验全规模 M1 = 未测（B1 测试被中断）
- PPO 全规模训练 = 未开始

## 根本性问题（需要分析）

1. **方法能否超越 B1？**
   - B1 全规模 M1=17.09%，目标 M1≥25%
   - 当前模型先验策略本质上是"保持最短距离 ISL"≈ 简化版 B1
   - PPO 在小规模上无法超越先验 → 大规模是否可能？

2. **PPO 是否适合这个问题？**
   - 动作空间是连续分数，但实际决策是离散 top-K
   - Normal 分布的 KL 在小 std 下爆炸，大 std 下退化为随机
   - 可能需要：离散动作空间 / ES 进化策略 / 监督学习 / 不同 RL 算法

3. **65664 候选边的可扩展性**
   - GATv2Conv 在 65K 边上 GPU 内存可能不够
   - 可能需要：候选边预筛选 / 分层决策 / 局部决策

## 已有文件

```
projects/leo-isl-scheduling-drl/
├── simulator/
│   ├── config.py          # N_LCT=3 已更新
│   ├── environment.py     # MDP 环境（已有）
│   ├── model_gat.py       # GATv2ActorCritic（新增）
│   │   # 3层 GATv2Conv (无edge_dim) + 边级decoder + active/distance bias
│   │   # 批处理 evaluate_actions via PyG Batch
│   │   # params=54,020
│   ├── train.py           # PPO 训练循环（新增）
│   │   # ISLRolloutBuffer + RewardNormalizer + EarlyStopping
│   │   # obs→PyG Data 转换 + wandb 骨架
│   └── (其他模块: orbit/visibility/channel/traffic/router/reward/metrics)
├── baselines/
│   ├── grid_fixed.py      # B1 (+Grid/Fixed)
│   └── wang_madrl.py      # B2 (Wang MADRL)
├── verify/
│   ├── verify_model_train.py  # 模型+训练验证（7项全通过）
│   └── quick_test.py          # Quick Test 脚本（已过时，实际用内联代码跑的）
├── results/
│   ├── quick_test/        # v1 结果
│   ├── quick_test_v2/     # v2 结果（最佳）
│   └── quick_test_v4/     # v4 结果
├── contract.md            # frozen
├── data-flow.md           # 8步推演
├── decision_log.md        # D001-D018
└── baseline_report.md     # B1+B2 复现
```

## 下一步（需要分析后决定）

### 选项 A：继续 PPO 路线
- 先测全规模纯先验性能
- 尝试更大 std + reward shaping（增加稳定性奖励）
- 尝试 Gumbel 探索替代 Normal

### 选项 B：换 RL 算法
- ES (Evolution Strategy)：无需 log_prob，直接优化确定性策略
- DDPG/SAC：连续动作空间专用，但有同样的 top-K 映射问题
- REINFORCE with baseline：更简单，可能更稳定

### 选项 C：换动作空间设计
- 当前：对所有候选边评分 → top-K
- 替代：对每颗卫星的活跃 ISL 做 keep/drop/swap 决策（更结构化）
- 替代：分层决策（先选卫星对，再选具体边）

### 选项 D：监督学习路线
- 用 B1 的拓扑作为标签训练模型
- 模型学会 B1 策略后，在 traffic-adaptive 场景可能自然超越
- 不需要 RL，但上限受限于 B1

## 已 commit 的代码
- commit: `feat(isl-scheduling-drl): Execute Step 0-1`
- 包含: model_gat.py, train.py, config.py 更新, verify 脚本, decision_log D015-D018
