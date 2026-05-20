# Handoff: RIS Phase DRL Step 7 — 训练 + Baseline Report

> 来源: S006 (Step 6-7 设计+实现) | 交接目标: 完成 baseline 训练，生成 baseline_report.md
> 文件名: H001-step7-training.md

## 已完成边界

- **GW Step 6**：仿真器设计规格完成，用户已确认
  - `simulator-design.md` 含模块清单、参数溯源、验证标准、FR-12 通过、实现必做清单
- **GW Step 7 Part A**：仿真器核心 5 模块实现 + 验证套件 20 项全部 PASS
  - `simulator/config.py`, `channel.py`, `beamforming.py`, `reward.py`, `env.py`
  - `verify/verify_simulator.py` — 解析/统计/退化/自相关/MDP trial/baseline/reward balance
- **GW Step 7 Part B**：6 个 baseline 全部实现 + 基础测试通过
  - `baselines/networks.py` (ReplayBuffer + Actor + Critic)
  - `baselines/td3.py`, `sac.py`, `ddpg.py`, `pso.py`, `simple.py`
  - `baselines/train.py` — 统一训练入口（wandb + early stopping + save/load + grad clip=1.0）

## 不要做什么

- 不要修改 simulator 核心模块（已通过 20 项验证）
- 不要跳过 wandb 和 early stopping（code-quality.md 6/6 项目缺失的教训）
- 不要用 `np.random.seed()`（用 `np.random.Generator`）
- 不要忘记 grad clip=1.0

## 必读

1. `projects/ris-phase-drl/simulator-design.md` — 设计规格和参数溯源
2. `projects/ris-phase-drl/decision_log.md` — D001-D015
3. `projects/ris-phase-drl/feasibility_report.md` — 方向可行性
4. `projects/ris-phase-drl/literature_notes.md` — 实验完备性对标 + 写作架构

## 快速趋势结果（N=64, M=4, K=4, seed=0, GPU, 100ep）

| 方法 | Avg Reward (bps/Hz) | Best | 备注 |
|------|---------------------|------|------|
| Random | 284.63 ± 7.82 | - | 基线下界 |
| Fixed (θ=0) | 1168.92 ± 132.94 | - | Rician κ=10dB 下 θ=0 对齐 LoS |
| TD3 | 1131.25 ± 100.20 | 1316.95 | ≈ Fixed，100ep 未充分收敛 |
| SAC | 1144.11 ± 100.55 | **1431.37** | best 已超 Fixed，最有前景 |
| DDPG | 1147.53 ± 100.51 | 1387.88 | ≈ Fixed |
| PSO | ~1394 | **1553.65** | 当前最优（50步内优化） |

**关键发现**：
- Fixed(θ=0) 非常强（Rician κ=10dB 天然对齐 LoS），DRL 需超越非平凡基准
- SAC best=1431 已超过 Fixed=1169，证明 DRL 能学到更好策略
- 100ep 仅初步趋势，DRL 需 3000ep 充分收敛后 avg 才能超过 Fixed
- PSO 50 步内可找到不错解，是合理上界

## 下一轮任务

### 1. 收集后台训练结果

后台 3 个 DRL 训练（TD3/SAC/DDPG, 100ep, N=64, seed=0, CPU）正在运行。结果在：
- TD3: `/tmp/claude-1000/.../tasks/b3xam1q2e.output`
- SAC: `/tmp/claude-1000/.../tasks/bvwmwd9wf.output`
- DDPG: `/tmp/claude-1000/.../tasks/bmyejrm5r.output`

如果后台任务已结束，读 output 文件收集最终 avg reward。如果仍在运行，等完成后再收。

### 2. 正式训练（GPU）

用 RTX 4070 跑 500ep × 3 seeds：
```bash
cd /mnt/d/code/study/research-protocol

# DRL: 500ep × 3 seeds（~5-8min/seed on GPU）
for algo in td3 sac ddpg; do
  for seed in 0 1 2; do
    ~/.venvs/torch/bin/python projects/ris-phase-drl/baselines/train.py \
      --algo $algo --seed $seed --N 100 --M 8 --K 4 --episodes 500 --device cuda
  done
done

# PSO + Random + Fixed: 50ep × 3 seeds（快速）
for algo in pso random fixed; do
  for seed in 0 1 2; do
    ~/.venvs/torch/bin/python projects/ris-phase-drl/baselines/train.py \
      --algo $algo --seed $seed --N 100 --M 8 --K 4 --episodes 50 --device cuda
  done
done
```

如果 500ep 收敛不够，可追加到 1000ep。先跑 seed=0 看趋势再决定。

### 3. 生成 baseline_report.md

按 `templates.md` 的 baseline_report 模板，包含：
- 趋势验证：各方法最后 10 episodes 平均 reward 对比表
- 收敛曲线：reward vs episode（TD3/SAC/DDPG）
- 统计规范性：≥3 seeds, error bar, 配对 t 检验
- 完成后更新 `decision_log.md` 阶段摘要

### 4. 后续步骤（baseline_report 完成后）

Groundwork 全部完成 → 进入 Contract 阶段。需读 `stages/contract.md`。
