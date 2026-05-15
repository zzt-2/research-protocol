# Handoff 2026-05-15 (Round 13) — Contract 冻结

## 当前进度
- **阶段：Contract 已冻结，待进入 Execute**
- 状态：Contract Step 0-6 全部完成
- Contract 状态：**frozen**（用户确认 2026-05-15）
- 本轮完成：方案新颖性验证、假设形成、Contract 起草、参数溯源（0 ASSUMPTION）、端到端推演、压力测试

## Contract 核心
- **假设**: GAT-PPO 拓扑感知 ISL 调度（逐边评分 + top-3）在 N_LCT=3 下 M1≥25%
- **Success**: M1≥25% AND GNN消融≥3pp AND 训练稳定
- **Failure**: M1<19% OR GNN消融<1pp OR 训练不稳定
- **Baseline**: B1(+Grid/Fixed, 5篇共识) + B2(Wang TCOM MADRL, IEEE TCOM Q1)
- **奖励**: 1.0·R_tput − 0.3·C_switch − 0.2·C_setup
- **GNN**: GATv2 4-head 64-dim × 3层 + edge decoder

## 关键修正
- 奖励函数 w₃ 从 M5(公平性) 改为 C_setup(建链成本)，与仿真器实现一致
- config.py 中 N_LCT=2 需更新为 N_LCT=3（Execute 阶段第一步）

## 产出文件
| 文件 | 内容 |
|------|------|
| `contract.md` | 完整 Contract（frozen） |
| `data-flow.md` | 8 步端到端数据流推演 |
| `decision_log.md` | [D013] 奖励修正 + [D014] 压力测试通过 |

## 下一步：Execute 阶段
1. 读 `stages/execute.md`
2. 读 `code-quality.md` + `reference/sim-template/` 模板
3. 更新 config.py: N_LCT=2→3
4. 实现 GNN 模型（GATv2 + edge decoder + actor-critic）
5. 实现 PPO 训练循环（使用 sim-template/train_ppo.py 模板）
6. 训练 + 评估
