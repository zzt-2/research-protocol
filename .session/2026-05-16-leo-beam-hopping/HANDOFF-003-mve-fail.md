# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 4a 可行性评估
- 状态：**阻塞** — MVE 未通过，需修复后重跑
- Contract 状态：未启动
- 本轮完成：
  - Step 3.5 补充检索：4 轮定向检索 120 条，发现 1 篇竞品（M14, AIAC 2024, 1cit），GNN+BH 从"零"下调为"近乎零"
  - Step 4a A0/A/B 分析：全部通过，无致命信号
  - MVE v1-v3：三版均 FAIL，GNN+REINFORCE 训练不稳定
  - 已提交：3c25067, 086208b, ae5f84e（feasibility report + MVE）

## 关键上下文

### MVE 失败分析（三版总结）

| 版本 | 问题 | 结果 |
|------|------|------|
| v1 | 干扰因子 0.3 太弱，IA-Greedy 仅比 Greedy 高 1.1% | 所有方法差异<2% |
| v2 | 信道模型 bug（噪声>>信号），path_loss_db=185 过大 | 吞吐量完全相同 |
| v3 | 环境正确（IA-Greedy >> Greedy 50%），但 GNN+REINFORCE 训练不稳定 | GNN 排名最差 |

### v3 关键数据（证明环境有效、训练有问题）
- IA-Greedy (干扰感知贪心): throughput=10.38, **+50% vs Greedy** — 干扰拓扑确实关键
- Greedy (top-K): throughput=6.92
- Random: throughput=7.61
- FC: throughput=8.48
- GNN: throughput=6.31 (±0.78 高方差 — 训练不稳定)

### MVE 修复方向

**核心诊断**：环境干扰模型正确（IA-Greedy 优势显著），GNN+REINFORCE 在 C(19,3)=969 动作空间上训练不收敛。

**修复优先级**：
1. **换 PPO/SAC 替代 REINFORCE** — REINFORCE 方差太大，PPO 的 clip 机制更稳定
2. **Reward shaping** — 显式惩罚同频干扰（如 reward += bonus * (1 - n_conflicts/K)）
3. **增大规模** — 至少 37 cells（L01/L07 标准规模），K=4-6，让 GNN 的拓扑感知有更多发挥空间
4. **增加训练** — 1000+ episodes，early stopping
5. **考虑模仿学习** — 用 IA-Greedy 生成专家轨迹做 warm-start

**不建议**：
- 继续用 REINFORCE（根本原因）
- 在 19 cells 小规模上反复调试（GNN 优势在大规模）

### A0/A/B 分析结论（已通过，可复用）
- A0.1: 性能间隙 ≥30%（MA-DRL >40小区失败 + MCTS 159s 太慢）
- A0.2: 4/4 结构适配（大状态/动态/泛化/延迟奖励）
- A0.3: ≥4 跨域先例（DynHGNN/Meta-GNN/REGNN/GNN RRM）
- A0.4: MDP 非平凡（空间隔离约束）
- A0.5: 无负面证据，空白="没人想到"+"技术壁垒刚解除"
- A: 结构优势 = 干扰拓扑建模 + 独立 agent 信息损失 + 可扩展性
- B: 空白原因有利（不是"试过失败"）

### 精读论文清单（7 篇 + 1 竞品）
- L01 Yang 2025 Tyche JSAC — MA-DRL>40小区不收敛
- L02 Zhang 2025 DynHGNN TWC — 超图干扰+GRU 动态
- L03 Geng 2024 Meta-GNN TVT — MPNN+meta-learning 泛化
- L04 Lin 2025 Graph+GAN ICT Express — 唯一图方法 BH
- L05 Gong 2026 QPLEX TWC — 分层 MA-DRL 标杆
- L06 Lin 2024 QMIX-BH TVT — 高引基础(90cit)
- L07 Wang 2025 Cooperative BH TWC — 三层解耦
- M14 AIAC 2024 — 唯一竞品(1cit, 异构图+DRL)

## 下一步
1. **修复 MVE**：换 PPO + reward shaping + 37 cells 规模，重跑
2. 如 MVE 通过 → 更新 feasibility_report.md → Conditional Go → Step 5 Baseline
3. 如 MVE 仍失败 → Pivot（考虑 GNN 作为辅助模块而非核心策略，或转向 GNN+监督学习）

## 关键文件路径
- 可行性报告：`projects/leo-beam-hopping/feasibility_report.md`（A0/A/B 已填，D 待更新）
- MVE 脚本：`projects/leo-beam-hopping/mve_gnn_vs_fc.py`（v3，需修复）
- 精读笔记+综合分析：`projects/leo-beam-hopping/literature_notes.md`
- 决策日志：`projects/leo-beam-hopping/decision_log.md`
- 框架文件：`stages/gw-feasibility.md`（已读）
