# Decision Log

## 阶段摘要
- [Groundwork] Step 3.5完成(4组检索+引用链)，Step 4a Conditional Go
- [Contract] 待进入
- [Execute] 待进入

## 决策记录
[D001] 确认GNN+BH为蓝海方向 | 理由: 4组关键词+引用链分析确认零直接竞品，最接近者P1仍以RL为主 | 阶段: GW
[D002] Step 4a Conditional Go | 理由: A/B无致命信号；MVE部分通过（GNN收敛时+16~48%，但3/5 seeds训练崩溃）；训练不稳定为REINFORCE已知问题，PPO/SAC可解决 | 阶段: GW
[D003][AUTO] MVE使用REINFORCE而非PPO | 理由: MVE追求最小实现，验证结构性优势而非训练稳定性 | 阶段: GW
