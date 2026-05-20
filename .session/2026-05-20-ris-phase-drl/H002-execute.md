# Handoff: RIS Phase DRL Execute 阶段

> 来源: Contract 冻结 (S008) | 交接目标: 实现 CCAN+TD3，完成 E1-E8 实验
> 文件名: H002-execute.md

## 已完成边界

- **Groundwork 全部完成**：仿真器 20/20 验证通过 + 6 baseline 复现 + baseline_report.md
- **Contract 冻结**：CCAN+TD3 方案，用户 2026-05-20 确认
  - `contract.md` (frozen), `data-flow.md`, `experiment_completeness_checklist.md`
- **关键实证发现**：
  - MLP-DRL ≈ Fixed ≈ 1290 bps/Hz（确定性评估）
  - PSO ≈ 1554 bps/Hz (+20%，证明信道自适应有价值）
  - MLP 首层 2600→400 压缩比过大，丢失逐元素行对齐

## 不要做什么

- 不要修改 simulator 核心模块（已通过 20 项验证）
- 不要修改已冻结的 contract.md 假设/signal/fairness/ablation
- 不要给 MLP baseline 换超参（已固定为与 CCAN 相同的超参）
- 不要跳过确定性评估（eval.py 已写好，必须用无噪声评估）
- 不要忘记 code-quality.md 必做清单（wandb/early stopping/save-load/grad clip=1.0）

## 必读

1. `projects/ris-phase-drl/contract.md` — 冻结的实验方案
2. `projects/ris-phase-drl/data-flow.md` — CCAN 架构端到端推演
3. `projects/ris-phase-drl/experiment_completeness_checklist.md` — 实验完备性
4. `code-quality.md` — 必做清单 + 已验证失败组合
5. `stages/execute.md` — Execute 阶段流程
6. `reference/sim-template/` — 代码模板

## 下一轮

### 1. 实现 CCAN 架构

在 `projects/ris-phase-drl/simulator/` 或 `baselines/` 下新建 CCAN Actor：

```
CCANActor:
  - 输入预处理：obs (2600,) → reshape (N, 2M+2K+2) = (100, 26)
  - Channel Encoder: Linear(26,64) → MultiHeadAttention(n_heads=4, d=64) → FFN(64,128,64)
  - Phase Decoder: Shared MLP (66→128→1) + tanh, 输出 action (N,)
  - 参数量 ≤ 2× MLP Actor (~1M)
```

Critic 保持标准 Twin-Critic MLP (2700→400→300→1) × 2。

### 2. 集成到训练循环

修改 `baselines/train.py` 支持 `--algo ccan_td3`，或新建 `baselines/train_ccan.py`。

### 3. 执行实验（按优先级）

**P0 — E1 核心**：CCAN+TD3 vs B1-B6, N=100, κ=10dB, 3 seeds, 2000ep (early stop)
**P1 — E2 迁移**：CCAN+SAC, CCAN+DDPG
**P1 — E3 规模**：N∈{64,100,200}
**P1 — E4 信道**：κ∈{3,5,10}
**P1 — E6-E8 消融**：A1(w/o attention), A2(w/o sharing), A3(w/o encoder)

### 4. 结果分析

- 生成配对 t 检验表
- 收敛曲线图
- 消融对比表
- 更新 decision_log.md

## 关键文件路径

| 文件 | 路径 |
|------|------|
| Contract | `projects/ris-phase-drl/contract.md` |
| Data Flow | `projects/ris-phase-drl/data-flow.md` |
| 仿真器 Env | `projects/ris-phase-drl/simulator/env.py` |
| Config | `projects/ris-phase-drl/simulator/config.py` |
| Baseline TD3 | `projects/ris-phase-drl/baselines/td3.py` |
| Baseline Networks | `projects/ris-phase-drl/baselines/networks.py` |
| 训练入口 | `projects/ris-phase-drl/baselines/train.py` |
| 确定性评估 | `projects/ris-phase-drl/baselines/eval.py` |
| Checkpoints | `projects/ris-phase-drl/results/checkpoints/` |
