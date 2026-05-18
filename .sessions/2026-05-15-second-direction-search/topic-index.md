# 专题：第二研究方向搜索

> 状态：closed | 创建：2026-05-15 | 最后更新：2026-05-15

## 进展线索

### H001 — 新对话提示词
为第二研究方向执行 GW Step 1 的完整 prompt。定义了背景（已有 leo-gnn-routing 主项目在 Execute 阶段）、已占用/排除方向列表（GNN routing / handover / RIS / ISL ACM / grant-free RA / HGAT 均已占）、选择标准（与导师 LEO 卫星链路方向相关、与路由项目互补、仿真可控、蓝海空间、不冲突）、以及 Step 0-4 的执行步骤和约束。

### S001 — 方向搜索执行记录
完整执行了 GW Step 1 检索与方向分析。工作内容：
1. 评估 2026-05-13 现有搜索资产（180+ 条），确认 beam hopping 方向 GNN 覆盖为零，NTN 整合方向过度拥挤
2. 补充 12 组检索（方向 A ISL Scheduling 4 组、方向 B Beam Hopping 4 组、其他探索 4 组）
3. 方向分析结论：
   - **方向 A（ISL Scheduling + DRL）**：101 篇去重相关，ISL 调度子方向 10 篇其中 5 篇用 DRL，属窄蓝海；关键对手包括 Wang TCOM 2024、Pi ICC 2022、Guo TWC 2024 等
   - **方向 B（Beam Hopping + GNN）**：74 篇去重相关，GNN for beam hopping 确认零篇（纯空白），BH+DRL 成熟（42 篇 DRL）；最接近论文为 Geng TVT 2025（GNN+元学习做功率分配）、Zhang TWC 2026（动态超图 NN）
   - 排除方向：ISL 波长规划（太冷门 3 篇）、用户链路（红海 83% DRL 穿透率）、跨层联合（与 routing 项目撞车）
4. 用户决策：A 和 B 并行推进，各自进入 GW Step 2-3

## 已确认结论

- 方向 A（ISL Scheduling + DRL）和方向 B（Beam Hopping + GNN）均为可行候选，各有创新空间
- GNN for beam hopping 确认为零覆盖（纯空白），BH 领域 DRL 已成熟但 GNN 未切入
- ISL 调度子方向论文数量有限（10 篇，5 篇 DRL），属窄蓝海
- NTN 整合方向因年发文量 200+ 被排除；用户链路因与 handover 重叠且红海被排除；跨层联合因与 routing 项目撞车被排除
- ISL 波长/频率规划太冷门（仅 3 篇，0 ML），框架不友好，排除

## 未决项

无（专题已 closed。方向 A 后续在 `.sessions/2026-05-15-isl-scheduling-drl/` 推进，方向 B 后续在 `.sessions/2026-05-15-beam-hopping-gnn/` 推进，两者最终均归档）

## 当前位置

专题已关闭。A(ISL Scheduling) 和 B(Beam Hopping) 两个候选方向已分别开专题并行推进 GW Step 2+，后经完整评估后均归档（见 `project_second-direction.md`）。
