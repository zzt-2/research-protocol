# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 3.5（补充检索）完成，Step 4a（Go/No-Go 可行性预判）待启动
- 状态：完成
- Contract 状态：未开始
- 本轮完成：Step 3.5 定向补充检索（2 轮收敛），更新 literature_notes.md + decision_log.md

## 关键上下文
- 项目目录：`projects/leo-resilient-routing/`
- Step 3.5 执行了 4 组定向检索 + FCRMJ 双向引用链分析
- Round 1 新增 7 篇建议读论文（GDAPS, Iris, DGA-IES 等），Round 2 新增 0 篇→收敛
- **核心结论不变：GNN + 专有故障恢复 + LEO 卫星路由 = 方法空白最终确认**
- 最强非卫星可迁移参考：GDAPS (GNN+MARL容错，SDN, 10.1109/tnse.2025.3582258)

## 精读论文完整列表（7 篇）
| 编号 | 论文 | content.md 路径 |
|------|------|-----------------|
| L01 | GRLR | papers/doi/10.1109_tvt.2024.3471658/content.md |
| L02 | GraphPR | papers/manual/10755127/content.md |
| L03 | MS-SNS | papers/manual/11398382/content.md |
| L05 | MegaResilience | papers/arxiv/2509.06766/content.md |
| L06 | DDPG-LBBP | papers/manual/faulty-links-fast-recovery-method-based-on-de/content.md |
| L07 | ADRLRM | papers/manual/11126166/content.md |
| P1 | FCRMJ | papers/manual/11504878/content.md |

## Step 3.5 新增建议读论文（7 篇，未精读）
| 编号 | 论文 | 关键信息 |
|------|------|---------|
| S1 | GNN multipath LEO (Huang 2023) | 56cit, IEEE, GNN 多路径 LEO 路由 |
| S2 | Iris (Wei 2024, TCOM) | 30cit, DRL 容错卫星路由(MLP) |
| S3 | GDAPS (Feng 2025, TNSE) | 6cit, GNN+MARL 容错路由(SDN) |
| S4 | DGA-IES (Rao 2025, IoT Journal) | 7cit, 图注意力+进化 RL |
| S5 | G-DQN (Li 2025, ISPA) | 0cit, GraphSAGE+DQN LEO |
| S6 | ReISL (Chen 2024, VTC-Fall) | 6cit, MARL ISL 重规划抗链路故障 |
| S7 | Path-based GNN resilient routing (Ye 2025) | 11cit, GNN 容错路由 |

## 竞品差异化空间（与 FCRMJ 对比，经补充检索确认不变）
1. GNN 拓扑感知 vs MLP 无拓扑感知
2. 可学习故障传播 vs 手工衰减系数 γ
3. 动态故障注入场景 vs 静态故障率测试
4. 端到端学习拥塞风险 vs 手工度中心性+队列加权

## 未决问题
- L04-DLNoConv (JOCN) 仍无法自动获取，可在 Step 4a 阶段评估是否必须

## 下一步
1. 读 `stages/gw-feasibility.md`（Step 4a 框架文件）
2. 按 gw-feasibility 维度执行 Go/No-Go 可行性预判
3. 如 Go → 进入 Contract 阶段
