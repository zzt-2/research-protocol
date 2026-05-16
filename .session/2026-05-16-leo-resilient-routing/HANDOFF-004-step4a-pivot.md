# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 4a 完成（Pivot 后），待新 MVE 验证 P1 方向
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：
  1. Step 4a A0/A/B 评估（修正 3 处）
  2. MVE-1（18 节点）：GNN MLU 差 5.8% → FAIL
  3. MVE-2（60 节点）：GNN MLU 差 4.2% → FAIL
  4. Pivot 决策：GNN → MARL+课程学习+主动预路由
  5. 补充检索：课程学习（真空白）+ MARL 故障恢复（开放利基）
  6. 精读 5 篇新论文：QueueMARL, Iris, GDAPS, ReISL, MAA-Shunts
  7. 确认 P1 差异化空间：课程学习 + 主动预路由（MAA-Shunts 两项均缺）

## 关键上下文

### P1 最终定位
- **问题**：LEO 故障感知抗毁路由
- **方法**：MARL(SAC/GAT) + 自适应课程学习 + 主动故障预测预路由
- **三大创新点**（vs MAA-Shunts）：
  1. 自适应课程学习：渐进故障复杂度训练
  2. 主动预路由：利用 LEO 轨道可预测性，ISL 断开前主动迁移流量
  3. 跨拓扑泛化：不同星座规模验证

### MVE 失败教训
- GNN 消息传递在路由决策维度不优于 MLP+手工特征（18/60 节点两次验证）
- 修正前错误声称：≥15% 泛化间距无支撑、MLP 无法做到拓扑感知
- 监督代理（oracle 模仿 + Dijkstra）可能不足以激活 GNN 优势，但两次一致失败已足够做 Pivot 决策

### 最直接竞品
- **MAA-Shunts** (TechRxiv 2025)：SAC+GAT+CTDE+参数共享，Poisson ISL 断裂+动作掩码，1584 星
- 重叠度 ~70%，但**无课程学习、无主动预测、无跨拓扑泛化**
- content.md：`papers/downloads/2026-05-16/techrxiv.175355456.63865201_v1.md`

### 精读论文完整列表（12 篇）
| 编号 | 论文 | 精读 | content.md 路径 |
|------|------|------|-----------------|
| L01 | GRLR | ✅ | papers/doi/10.1109_tvt.2024.3471658/content.md |
| L02 | GraphPR | ✅ | papers/manual/10755127/content.md |
| L03 | MS-SNS | ✅ | papers/manual/11398382/content.md |
| L05 | MegaResilience | ✅ | papers/arxiv/2509.06766/content.md |
| L06 | DDPG-LBBP | ✅ | papers/manual/faulty-links-fast-recovery-method-based-on-de/content.md |
| L07 | ADRLRM | ✅ | papers/manual/11126166/content.md |
| P1 | FCRMJ | ✅ | papers/manual/11504878/content.md |
| S2 | Iris | ✅（部分） | papers/doi/10.1109_tcomm.2024.3370618/content.md |
| S3 | GDAPS | ✅ | papers/downloads/2026-05-16/11048425.md |
| S6 | ReISL | ✅ | papers/downloads/2026-05-16/10757838.md |
| P4 | QueueMARL | ✅ | papers/arxiv/2605.04448/content.md |
| S8 | MAA-Shunts | ✅ | papers/downloads/2026-05-16/techrxiv.175355456.63865201_v1.md |

### 补充检索 JSON
- `search-archive/2026-05-16/curriculum-learning-deep-reinforcement-learning-network-rout.json`
- `search-archive/2026-05-16/progressive-training-reinforcement-learning-satellite-routin.json`
- `search-archive/2026-05-16/multi-agent-reinforcement-learning-fault-tolerant-routing-satellite.json`
- `search-archive/2026-05-16/marl-distributed-fault-recovery-rerouting-network.json`

### 额外下载论文（blit 附带）
- `papers/downloads/2026-05-16/11386024.pdf` — 未精读，待确认相关性

## 未决问题
- MAA-Shunts 是 TechRxiv 预印本，可能在投顶会，时间压力
- Iris 全文可能需要重新下载确认（当前 content.md 可能不是 Iris）

## 下一步
1. 读 `stages/gw-feasibility.md` 确认 MVE 设计规范
2. 设计并执行 P1 新 MVE（MARL + 课程学习 + 主动预路由）
   - 假设：课程学习+主动预路由在动态故障场景下优于无课程 MARL
   - 对比：单 agent DQN / MARL 无课程 / MARL+课程
   - 指标：MLU、连通率、泛化退化幅度
   - 实现要点：Walker 60 节点，课程 4 阶段，contact plan 预测 ISL 断开
3. MVE 通过 → 更新 feasibility_report.md → Go/No-Go 确认 → Contract 阶段
4. MVE 失败 → 转向 P2（在线自适应 DRL / Meta-RL）
