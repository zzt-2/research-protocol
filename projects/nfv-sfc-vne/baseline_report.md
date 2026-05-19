# Baseline Report — nfv-sfc-vne

> GW Step 7 Part B 产出 | 2026-05-19

## 1. 实验配置

| 参数 | 值 |
|------|-----|
| 底层网络 | Waxman(100, α=0.5, β=0.2), cpu~U[50,100], bw~U[50,100] |
| VNR | random(2~10 nodes, p=0.5), cpu~U[0,20], bw~U[0,50] |
| SFC 叠加 | sfc_ratio=0.6, num_vnf_types=5, seed=42 |
| VNR 数量 | 500/epoch |
| 奖励 | fixed_intermediate (success=R2C, intermediate=0.1, failure=-0.1) |
| 硬件 | NVIDIA RTX 4070 Laptop GPU |

## 2. Baseline 结果

### 2.1 汇总表

| ID | Solver | 类型 | Epochs | AC | R2C | 训练时间 |
|----|--------|------|--------|------|------|----------|
| B1 | GRC Rank | 启发式 | N/A | 0.836 | 0.543 | 10s |
| B3 | sfc_pg_mlp | PG+MLP | 30 | 0.908 | 0.599 | 42.2 min |
| B2 | sfc_ppo_dual_gat+ | PPO+DualGAT | 5 | 0.918 | 0.676 | 14.0 min |

### 2.2 趋势验证

**核心趋势**: DualGAT+ > MLP > GRC (R2C 维度)

| 对比 | R2C 提升 | AC 提升 |
|------|----------|---------|
| MLP vs GRC | +10.3% | +8.6% |
| DualGAT+ vs MLP | +12.8% | +1.1% |
| DualGAT+ vs GRC | +24.4% | +9.8% |

趋势通过: DRL 方法结构性优于启发式，GNN 方法优于 MLP。

### 2.3 pg_mlp 训练曲线 (30 epochs)

| Epoch | AC | R2C | LogProb |
|-------|------|------|---------|
| 0 | 0.802 | 0.489 | -4.544 |
| 5 | 0.862 | 0.555 | -3.332 |
| 10 | 0.848 | 0.558 | -2.897 |
| 15 | 0.826 | 0.565 | -2.562 |
| 20 | 0.872 | 0.571 | -2.715 |
| 25 | — | 0.571 | — |
| 30 (val) | 0.908 | 0.599 | — |

pg_mlp R2C 在 ~10 epoch 趋于收敛(~0.56)，后续 epoch 波动但整体缓慢上升。

### 2.4 DualGAT+ 训练曲线 (5 epochs)

| Epoch | AC | R2C | LogProb |
|-------|------|------|---------|
| 0 | 0.826 | 0.484 | -4.490 |
| 1 | 0.884 | 0.553 | -3.671 |
| 2 | 0.918 | 0.629 | -2.539 |
| 3 | 0.890 | 0.648 | -1.940 |
| 4 | 0.906 | 0.663 | -1.530 |
| 5 (val) | 0.918 | 0.676 | — |

DualGAT+ 在 5 epoch 内 R2C 从 0.48 快速升至 0.66，收敛速度远快于 MLP。仅 5 epoch 即超越 pg_mlp 30 epoch 的 R2C（0.676 vs 0.599，+12.8%）。

## 3. 关键发现

1. **SFC 约束不阻碍训练**: 所有 DRL baseline 在 SFC 约束环境下均可正常训练和收敛
2. **GNN 优势显著**: DualGAT+ 仅 5 epoch 即在 R2C 上超越 MLP 30 epoch (+12.8%)，证明图结构建模在 VNE 中的价值
3. **AC 维度差异小**: DualGAT+ vs MLP 在 AC 上仅 +1.1%，说明 R2C 的提升主要来自更高效的资源利用（更优的链路映射）
4. **DualGAT+ 未收敛**: 5 epoch 的 DualGAT+ logprob 仍在快速下降，表明更多 epoch 可进一步提升 R2C

## 4. 后续

- B4 (CONAL) 和 B5 (PPO-DualGCN): 可选，当前 3 个 baseline 已覆盖启发式/MLP/GNN 三档
- MatchingGAT policy (M3): 核心创新，目标超越 DualGAT+（通过跨图注意力 + SFC 位置编码）
- 更多 epoch 的 DualGAT+ 训练: 可作为完整 baseline 对比，预计 30 epoch R2C > 0.70
