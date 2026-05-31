# Handoff 2026-05-14

## 当前进度
- 阶段：Execute Step 2（核心实验 — RL 实验完成，待讨论下一步）
- 状态：RL 管线完成但效果有限，需讨论是否继续优化或转向 baseline 对比
- Contract 状态：frozen
- 本轮完成：
  - 实现 `env.py`（RL 环境：episode 生成 + greedy/weighted Dijkstra 评估）
  - 实现 `pretrain.py`（监督预训练：RoutingActorCritic, 3层GAT, h=128, 150 epochs）
  - 实现 `train.py`（PPO 微调：greedy reward + weighted Dijkstra reward 两版）
  - 新增 `RoutingActorCritic` 模型（models.py：预计算 PE + Actor-Critic heads）
  - 监督预训练：方向精度 97.6%(train) / 66.8%(target)，retention 71%
  - 贪心推理：路径成功率 22-30%(train) / 1.7%(target)（太低）
  - 加权 Dijkstra 推理：成功率 100%，median stretch 1.5-1.8，mean stretch 2.1-2.6
  - PPO 微调实验：两种 reward 均无法改善监督 baseline

## 关键上下文

### 核心发现
1. **贪心推理瓶颈**：路径成功 = 逐跳精度之积，97.6%^10≈78% 理论上限，实际更低
2. **加权 Dijkstra 有效**：将 logits 转为边权重跑 Dijkstra，解决成功率问题
3. **PPO 无效**：action-reward 解耦（改单节点 logits 不影响整条路径），梯度信号太弱
4. **stretch 分布右偏**：median 1.5-1.8 可用，但 P95=5-7，mean 被拉到 2.1-2.6
5. **某些目的地精度极低**：个别 episode 方向精度仅 ~46%（vs 平均 95%），导致 stretch 尾部

### 仿真器文件索引（simulator/）
| 文件 | 用途 | 状态 |
|------|------|------|
| config.py | 全局参数 | ✓ |
| constellation.py | Walker-Delta 星座 | ✓ |
| topology.py | +Grid ISL 拓扑 | ✓ |
| channel.py | Shannon 容量 | ✓ |
| traffic.py | 流量模型 | ✓ |
| routing.py | Dijkstra | ✓ |
| snapshot.py | PyG 图 + PE | ✓ |
| models.py | RoutingGNN + RoutingActorCritic | ✓ |
| smoke_test.py | 物理验证 | ✓ (通过) |
| quick_test.py | 监督泛化测试 | ✓ (retention 70%) |
| env.py | RL 环境 | ✓ |
| pretrain.py | 监督预训练 | ✓ (retention 71%) |
| train.py | PPO 微调 | ✓ (无效) |
| test_weighted.py | 加权 Dijkstra 对比 | ✓ (debug 用) |
| debug_weighted.py | 路径分析 debug | ✓ (debug 用) |

### 权重保存
- `simulator/pretrained.pt` — 监督预训练权重（72,965 params）
- `simulator/ppo_finetuned.pt` — PPO 微调后权重（效果不如 pretrained）

## 未决问题
- **Stretch 优化**：median 1.5-1.8 可接受但 mean 2.1-2.6 偏高，是否需要进一步优化？
- **可发表性**：71% retention + 加权 Dijkstra stretch 2.1 是否足够？需要 baseline 对比才有定论
- **PPO 替代方案**：是否尝试其他 RL 方法（如 differentiable shortest-path、DRL 直接优化 edge weight）？
- **推理策略**：加权 Dijkstra 是否是最优推理方式？是否有更好的 GNN→路由映射？

## 下一步（需要用户确认方向）
1. **方向 A：继续优化 stretch**
   - 更多训练数据（更多 snapshots/configs）
   - 更大模型（4 层, h=256）
   - Edge-level scoring（GNN 直接预测边权重而非方向）
   - Differentiable Dijkstra（端到端优化）
2. **方向 B：转向 baseline 对比**
   - 实现 GRLR baseline 复现（需读论文提取架构细节）
   - 跑完整实验 E01-E09
   - 用当前结果与 baseline 对比，判断是否够发表
3. **方向 C：两者并行**
   - 先跑 baseline 对比确定位置
   - 同时探索 stretch 优化

## 文件路径
- Decision log：`decision_log.md`（D001-D021）
- Contract：`contract.md`（frozen）
- 仿真器：`simulator/`（16 个 .py 文件 + 2 个 .pt 权重）
