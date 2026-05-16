# Handoff 2026-05-16 (Round 15) — Execute 死胡同确认

## 当前进度
- **阶段：Execute Step 0-1 → 死胡同，待方向回顾**
- Contract 状态：**frozen**
- 本轮完成：REINFORCE 验证 + swap 诊断 + 文档更新(D023-D025)
- **需要新对话做方向回顾和决策**

## 核心结论：ISL 调度的先验已接近最优

### 证据链（3 个独立验证）

| # | 方法 | 结果 | D-ID |
|---|------|------|------|
| 1 | PPO + Normal + top-K | M1 0.0774→0.0780 (+0.0006) | D021 |
| 2 | REINFORCE + 噪声探索 | M1 0.0859→0.0827 (-3.7%) | D023 |
| 3 | 随机 swap 诊断 (30 trials) | max 改善 +0.0015 (噪声级) | D024 |

**共同根因**：先验策略 (active_bias=3 + distance_bias=2) 本质上实现了"保持活跃 ISL + 选最短边"≈ 简化版 B1。这个策略已捕获问题的物理结构（短 ISL 延迟低、容量高），剩余优化空间 <2%。

### 与 beam-hopping 的模式匹配

| 维度 | beam-hopping (已归档) | ISL scheduling (当前) |
|------|----------------------|----------------------|
| 失败模式 | A3: 干扰是物理关系不可学习 | A2+A3: 先验捕获物理结构 |
| 方法尝试 | 6 种全败 | 3 种全败 (PPO/REINFORCE/噪声探索) |
| 先验表现 | OptGreedy 显著优于 RL | active+distance bias ≈ B1 的 75-83% |
| swap 诊断 | 未做 | 随机 swap 改善 ≤0.0015 |
| 归档判定 | 归档 | **待决策** |

### 未验证的两个角度

1. **全规模 24×66**：候选边 65K vs 5K，每星候选更多，优化空间可能更大。但 env.step=0.6s，swap 诊断耗时长。
2. **流量感知定向 swap**：不是随机换，而是换到流量需求方向。需要从 obs 的 node_features (supply/demand) 计算最佳方向。

## 已有文件

```
projects/leo-isl-scheduling-drl/
├── simulator/           # 完整仿真器 (8 模块, 评分 4.4/5)
├── baselines/           # B1 Grid/Fixed + B2 Wang MADRL
├── verify/              # 验证套件
├── test_reinforce.py    # REINFORCE 测试脚本 (新建)
├── test_swap_diagnostic.py  # Swap 诊断脚本 (新建)
├── decision_log.md      # D001-D025
├── contract.md          # frozen
└── baseline_report.md   # B1+B2 复现
```

## 学位论文方向约束

导师要求 1 方向 → 3 个关联问题 → 3 章主体。当前方向 A（LEO 星座网络优化）：
1. 路由 (mega-constellation GNN) — **已完成**
2. ISL 调度 — **当前死胡同**
3. 切换 (ntn-handover DRL) — **已完成**

如果 ISL 归档，需要在方向 A 内找替代子问题（如拓扑抗毁、流量感知路由），或转入新方向。

## 下一步

新对话应：
1. 读本 handoff + decision_log D021-D025
2. 读 `code-quality.md` 失败模式 A1-A3 + beam-hopping decision_log D011-D013
3. 评估两个未验证角度的 ROI
4. 做方向决策：继续 ISL（如何改）/ 归档换子问题 / 换方向
