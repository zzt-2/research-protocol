# Handoff: 完整训练 + 消融实验完成

> 来源: Step 7 Part D | 交接目标: 进入 Contract 阶段
> 文件名: H007-full-training-ablation.md

## 已完成边界

### DualGAT+ 30ep 公平对比
- R2C=0.756, AC=0.912 (101.3 min)
- epoch 10 后进入平台期(~0.74)，未继续提升

### MatchingGAT 30ep 完整训练
- R2C=0.790, AC=0.968 (106.5 min)
- vs DualGAT+ 30ep: R2C +4.5%, AC +6.1%
- epoch 4 即达 0.777，极快收敛

### 消融实验（10ep）
| 变体 | AC | R2C | Δ vs Full |
|------|------|------|-----------|
| Full Model (30ep) | 0.968 | 0.790 | — |
| w/o SFC PE | 0.982 | 0.776 | -1.8% |
| w/o Cross-Attn | 0.970 | 0.773 | -2.2% |
| w/o Edge Attr | 0.954 | 0.755 | -4.4% |

三个组件均有正向贡献。边特征贡献最大(-4.4%)，跨图注意力次之(-2.2%)，SFC 位置编码也有贡献(-1.8%)。

### 完整对比表

| Solver | Epochs | AC | R2C | 时间 |
|--------|--------|------|------|------|
| GRC | N/A | 0.836 | 0.543 | 10s |
| pg_mlp | 30 | 0.908 | 0.599 | 42 min |
| DualGAT+ | 30 | 0.912 | 0.756 | 101 min |
| **MatchingGAT** | **30** | **0.968** | **0.790** | **107 min** |

### 消融代码实现
- `matching_policy.py`: ablation_mode 参数支持 (no_sfc_pe / no_cross_attn / no_edge_attr)
- 3 个消融 solver 已注册 (sfc_ppo_ablation_no_sfc_pe / no_cross_attn / no_edge_attr)
- `verify/run_ablation.py`: 批量消融训练脚本
- `verify/run_training_queue.sh`: 串联训练队列

## 不要做什么

- 不要用 5ep 消融结果写论文——方差太大，10ep 是最低门槛
- 不要跳过 30ep 消融——Contract 阶段需要同 epoch 数严格对比
- 不要把消融 10ep 和 Full 30ep 直接对比当最终数据——epoch 差异可能低估组件贡献
- 不要忽略消融中 AC 维度——w/o SFC PE 的 AC=0.982 反而高于 Full=0.968，需分析原因

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态
2. `projects/nfv-sfc-vne/baseline_report.md` — 完整训练结果 + 消融
3. `stages/contract.md` — Contract 阶段流程（下一步必读）

## 下一轮

1. **读 `stages/contract.md`** — 进入 Contract 阶段
2. **Contract Step 0**: 确认实验矩阵、种子配置、评估指标
3. **30ep 消融**: Contract 阶段跑同 epoch 数消融获得严格对比
4. **多拓扑验证**: GEANT/BRAIN/WX500 泛化性测试
5. **B4/B5 可选**: CONAL / PPO-DualGCN 补充对比
