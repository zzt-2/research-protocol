# Execute 阶段 · 方案 A 验证报告

> 2026-05-08，LA-DDQN + A1 消融，100 episode 训练。

## 1. 实现状态

| 组件 | 状态 | 文件 |
|------|------|------|
| Top-K 预处理 | ✅ 完成 | `la_ddqn.py` |
| DLA cross-attention | ✅ 完成 | `la_ddqn.py` |
| A1 Flat FC 消融 | ✅ 完成 | `ablation_a1.py` |
| B2 Dueling DDQN | ✅ 已有 | `baselines/b2_dueling_ddqn.py` |

## 2. 实验结果汇总

### 2.1 最终对比表（3 seeds 均值，100ep 训练）

| 指标 | A1 Flat FC | LA-DDQN (DLA) | B1 HHS | B4 Random |
|------|-----------|--------------|--------|-----------|
| 吞吐量 | **36.05 Gbps** | 35.91 Gbps | 20.9 Gbps | 36.1 Gbps |
| 阻塞率 | **0.00%** | 0.07% | 37.4% | 0.02% |
| 切换次数 | **857** | 911 | 877 | 8,435 |
| Reward (last10) | **10010** | 9927 | — | — |
| 参数量 | 35,458 | 51,778 | — | — |
| 训练时间 | 1637s | 1356s | — | — |

### 2.2 核心发现：A1 ≈ LA-DDQN，DLA 无独立贡献

**A1（无 attention）在所有指标上略微优于 LA-DDQN（有 DLA）**：
- 吞吐量：36.05 vs 35.91 Gbps（+0.4%）
- 阻塞率：0.00% vs 0.07%
- 切换：857 vs 911
- 参数量少 32%（35K vs 52K）

**结论：DLA cross-attention 在当前场景下不提供可测量的性能增益。主要贡献来自 Top-K 压缩。**

### 2.3 DLA 无效的原因分析

| 因素 | 分析 |
|------|------|
| 场景规模 | 15 UE，avg 4.4 颗可见卫星——候选集太小，attention 无用武之地 |
| sinr 饱和 | 可见卫星 SINR 普遍 >22dB，sinr_norm 全为 1.0，区分特征只剩仰角 |
| 负载稀疏 | load_stats 在多数时间步为全零（无 UE 连接时 load=0），query 信息量不足 |
| FC 已充分 | Flat FC(8→256→128) 对 8 个候选的处理能力已过剩，attention 无需压缩 |
| 训练不足 | 100ep 可能不够 DLA 学到复杂的负载-卫星映射（但 A1 同样 100ep 也收敛了） |

**核心原因**：当前仿真规模下（15 UE，~5 颗可见卫星），问题复杂度不足以让 attention 机制展现优势。FC 的表达能力已经足够。

## 3. Bug 修复记录

### 3.1 特征索引错误（已修正）

`topk_preprocess` 中 elev 和 avail 切片顺序与 env 输出不一致。

```python
# 错误（v1）→ 正确（v2）
avail = flat_obs[N:2N]   →  elev  = flat_obs[N:2N]    # elev_norm
elev  = flat_obs[2N:3N]  →  avail = flat_obs[2N:3N]   # avail_norm
```

v2 修正后吞吐量从 32.1 提升到 35.9 Gbps（+12%）。

## 4. DLA Attention 行为（参考）

训练后 attention 权重分化（0.109-0.135），但分化幅度有限。高仰角卫星权重略低（"显而易见的好"），低仰角卫星权重略高。行为有意义但效果不显著。

## 5. 方案 A 贡献重新评估

### 5.1 原始贡献假设 vs 实验事实

| 贡献 | 假设 | 实验结果 |
|------|------|----------|
| DLA cross-attention | 负载驱动 attention 提升负载均衡 | ❌ A1 消融否定，无独立贡献 |
| Top-K 压缩 | 97.4% 降维不损失性能 | ✅ 确认有效，但属工程优化 |
| 轻量骨干 | 参数效率 | ✅ 35K vs B2 712K，但 A1 更轻 |

### 5.2 修正评分

```
原评估：★★★☆☆ (3/5) — DLA + Top-K + 消融
修正评估：★★☆☆☆ (2/5) — Top-K 是唯一有效贡献，DLA 被消融否定
```

### 5.3 对论文叙事的影响

原叙事："负载驱动 attention 让 DRL 理解负载分布" → 被消融否定
无法证明 DLA 比简单 FC 更好，论文核心贡献成立困难。

## 6. 决策建议

### 6.1 方案 A：不再继续投入

- DLA 被消融否定，继续 A2-A8 消融的边际价值极低
- 即使 Top-K 有效，作为独立论文贡献太弱
- **建议：暂停方案 A**

### 6.2 方案 C（GNN+DRL）：建议转为主攻

| 维度 | 方案 C 优势 |
|------|------------|
| 消融可靠性 | GNN 消融（有 vs 无 GNN）更可能证明价值——GNN 提供结构化信息（UE 间竞争关系）是 flat FC 无法编码的 |
| 新颖性 | 三元组合"二部图 GNN + DRL + 多 UE 负载均衡"无人占据 |
| 故事力 | "flat obs 丢失结构化负载竞争信息 → GNN 恢复"叙事清晰 |
| 规模适配 | GNN 在更大规模（更多 UE/卫星）下优势更明显，attention 在小规模下无用武之地的教训反而支持 GNN |

### 6.3 Top-K 预处理的价值保留

Top-K 压缩在 A1 和 LA-DDQN 中均有效（1585→41 维），可直接复用于方案 C 的 Graph Builder（从 396 颗降到 K=6-8 颗候选）。

## 7. 文件清单

| 文件 | 说明 |
|------|------|
| `la_ddqn.py` | LA-DDQN 实现（v2 修正版） |
| `ablation_a1.py` | A1 Flat FC 消融 |
| `results/la_ddqn_quick.json` | LA-DDQN 100ep 结果 |
| `results/a1_flatfc_results.json` | A1 消融 100ep 结果 |
| `results/la_ddqn_100ep_v1_bugidx.json` | v1 bug 版备份 |
| `results/la_ddqn_30ep_backup.json` | 30ep 备份 |
| `design_A.md` | 方案 A 完整技术设计 |
| `execution_report.md` | 本文件 |

## 8. 待执行

| 优先级 | 任务 | 预计时间 | 说明 |
|--------|------|----------|------|
| **P0** | **方案 C 实现** | 2-3 天 | Graph Builder + GNN + 分解式 Q |
| P1 | B2 DDQN 100ep 训练 | ~30 min | 公平对比 baseline（复用于 C 的评估） |
| ~~P1~~ | ~~A2-A8 消融~~ | — | **已取消**（DLA 被否定） |
