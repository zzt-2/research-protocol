# Handoff 2026-05-15 (Round 6 — Step 7 Part A 完成)

## 当前进度
- 阶段：GW Step 7 §impl
- 状态：Part A + Part A-checkpoint 全部通过，待 Part B（Baseline 复现）
- 本轮完成：
  - Part A: 仿真器 5 模块实现（config/antenna/channel/traffic/env）+ 验证脚本
  - 3 项物理修正：噪声功率、路径损耗、干扰惩罚方向
  - 吞吐量归一化修正（active beams only）
  - Part A-checkpoint: MDP 试运行全部通过（16/16 验证 + 奖励合理性 3/3）

## 关键设计变更（D008/D009）
- **噪声功率**：-97 dBm 是总噪声功率，不是 PSD，不能乘带宽
- **路径损耗**：用 orbit_height_km（550km）而非 slant_range_km（2704km）
- **干扰惩罚**：`max(0, SINR_thr - SINR)` 惩罚低 SINR（差选择），非原 spec 的 `max(0, SINR - SINR_thr)`
- **吞吐量归一化**：`served_active / demand_active`（仅被服务波束），非 `served / total_demand_N_beams`

## MDP 试运行结果
| 策略 | 总奖励 | Throughput | Fairness | Interference |
|------|--------|-----------|----------|-------------|
| Random | 5.83 | 1.67 | 17.69 | 4.75 |
| Greedy(demand) | 5.98 | 1.10 | 19.31 | 4.71 |
| OptGreedy(C(N,K)) | 6.46 | 1.91 | 17.88 | 0.50 |

- 最大分量：82% (fairness) < 95% ✓
- 策略差距：10.7% > 10% ✓

## 文件路径
- 仿真器: `projects/leo-beam-hopping-gnn/simulator/` (5 模块 + __init__)
- 验证: `projects/leo-beam-hopping-gnn/verify/verify_simulator.py`
- MDP试运行: `projects/leo-beam-hopping-gnn/verify/mdp_trial_run.py`
- 决策日志: `projects/leo-beam-hopping-gnn/decision_log.md` (D001-D009)
- 仿真器规格: `projects/leo-beam-hopping-gnn/simulator_spec.md`
- 文献笔记: `projects/leo-beam-hopping-gnn/literature_notes.md`

## 下一步：Part B — Baseline 复现
按 gw-experiment.md §impl Part B：
1. **Greedy baseline**：每 slot 穷举 C(N,K) 选最优（已在 mdp_trial_run.py 有原型）
2. **PPO+MLP baseline**：核心消融对照，同算法不同编码器（实现参考 MVE 的 REINFORCE，升级为 PPO）
3. **图着色 L04 baseline**：非 ML 传统基线，参考 L04 论文的 MCMF-TS-GC 算法
4. **复现标准**：验证相对趋势 DRL > 传统 > 随机，不对比绝对数值

## 需要先读的文件
1. 本 handoff
2. `stages/gw-experiment.md` §impl Part B（复现定义和操作）
3. `projects/leo-beam-hopping-gnn/simulator/env.py`（BHEnv 接口）
4. `projects/leo-beam-hopping-gnn/literature_notes.md`（L04 图着色算法细节）
