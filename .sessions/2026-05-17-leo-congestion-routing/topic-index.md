# 专题：LEO 拥塞路由（Execute 收尾 — 实验完备+可视化+论文材料就绪）

> 创建：2026-05-17 | 状态：dormant | 最近更新：2026-05-18
> 注册表：`_registry.yaml` slug `2026-05-17-leo-congestion-routing`

## 进展线索

### H006-contract-draft
Contract Step 0-3 完成。Step 0 新颖性确认、Step 1 假设形成（GNN vs ECMP >=10%, GNN vs MLP >=15%, 泛化退化 <10%）、Step 2 草案（12 组实验设计：4 核心 + 3 对比 + 5 消融/鲁棒）、Step 3 参数溯源。所有 [ASSUMPTION] 已消除。下一步为 Step 4 端到端推演。

### H007-contract-frozen
Contract 冻结完成，用户已确认。本轮同时完成 GW Step 7 baseline 复现（ECMP 1.97 > SP 2.37 > MLP 2.52，证明 message passing 必要）和 Contract Step 0-6 全流程。data-flow.md 端到端推演 8 步全通过。MDP checkpoint 显示贪心 vs 随机仅 +3.8%（未达 10% 门限），但不阻断（MVE 已证 GNN > ECMP 12%）。状态进入 Execute Ready。

### H008-kpath-migration
Execute Step 2 执行中发现 MVE 与正式模型架构不一致：MVE 用 K-path 离散选择（逐流路由）beat ECMP 12%，但正式模型设计为 per-edge 连续权重（同时路由所有流），加权 Dijkstra 单路径表达力低于 ECMP 多路径分流。E01 seed 0 结果 GNN/ECMP=1.07 FAIL。决策进行范式迁移：per-edge continuous → per-flow K-path discrete。重新设计 Episode 结构、PathScoringHead、增量奖励，并列出迁移执行顺序 8 步。

### H009-e01-ready
K-path 迁移执行完成。env/model/train/baselines/verify 全部重写为 K-path 范式，verify 28/28 PASS。Quick Test（100ep, 1 seed）GNN/ECMP=0.766（改善 23.4%，远超目标 <=0.90），确认迁移成功。预估 E01 全量训练约 45-50 分钟。

### H010-e01v2-e04-done
E01-v2（800ep, entropy=0.02, 3 seeds）双指标 PASS：GNN/ECMP=0.818, GNN/MLP=0.822。E04 泛化（66→48 zero-shot）GNN MLU=1.96 仍优于 ECMP，MLP 崩溃（比 ECMP 差 34%）。E01 原始 GNN/MLP=0.863 FAIL 的根因为训练不充分，800ep + entropy=0.02 后 std 从 0.12 降至 0.03。核心假设确认成立。

### H011-execute-done
Execute Step 2 完成，10 组实验全部跑完。核心实验（E01-v2/E04/E05/E06）全部 PASS，覆盖 48-720 节点（0.7x-10.9x 规模）。对比实验揭示：E02 无故障 GNN/ECMP=1.095（故障是优势激活条件），E03 极端突发 GNN 仍优 14%。消融实验（E08/E09）显示甜点在 8-10% 故障率、重型流量 GNN 优势更大。E10/E11 架构消融和 E12 故障模式对比列为 P2 待做。

### H012-vulnerability-audit
全面漏洞审计发现 5 个致命问题 + 5 个重大问题。最严重的是 F1（surge 始终激活：Contract 写"无 surge"但代码默认 surge_factor=5.0，所有结果可能作废）、F2（GNN 正常条件下劣于 ECMP）、F3（ECMP 实现不标准，只从 K=4 候选中轮询）。提出修复优先级排序和分批子对话执行策略，F1 验证为 P0 最优先。

### S001-vulnerability-audit
审计操作日志。记录审计触发（实验全部完成后投稿级质量审查）、方法（critic Opus 对抗性审查）、5 致命 + 5 重大问题的详细发现、叙事问题（per-link 声称被削弱、时变拓扑不成立、与 Ch1 高度相似）、4 条教训（Contract-config 交叉验证、Baseline 公平性审查、泛化拓扑异构性、消融多 seed），以及 3 个框架改进建议（FR-14/15/16）。

### H013-vulnerability-fixes-batch1
漏洞修复全部完成 + E01-E11 全量重跑(surge=1.0)。F1(surge→1.0)结果反而更好(GNN/ECMP=0.778)；F3(True ECMP)仅差1.35%不影响结论；M2(MLP公平化)后GNN仍赢19%；M3/m4(统计检验+多指标)就位。F2叙事反转：surge=1.0下全部条件(含无故障/均匀流量)GNN都赢ECMP，旧结论是surge假象。E02-E11全部消融完成，架构消融差异<2%。框架更新"实验完备性对标"机制，待下轮用Tier 1清单快速过一遍。

### H014-audit-positioning-plan
Tier 1 自检完成（3 子 agent 并行审计）。Tier 1: 3/6 通过，Tier 2: 2/5 通过。关键缺口：复杂度报告完全缺失、泛化实验无 MLP 对比、E10/E11 单 seed。Contract 文档已修正（per-link→per-flow K-path、Walker delta 族内限定、surge=1.0）。定位决策：路线 A（故障弹性）+ B（在线逐流）组合，定位为"Online Fault-Resilient Per-Flow Routing"，避免与 TELGEN 正面竞争 size gen 新颖性。DTAR 不补做（粒度差异，Related work 讨论即可）。后续分 P0-P3 四级执行，P0 为复杂度报告+训练曲线更新。

## 已确认结论

1. K-path 离散选择（逐流路由）范式优于 per-edge 连续权重范式
2. **surge=1.0 下 GNN 在所有条件（含无故障/均匀流量）都赢 ECMP**，旧"F2 正常条件弱"结论是 surge=5.0 假象
3. True ECMP(BFS全最短路)比 K=4 ECMP 仅好 1.35%，旧结果可信
4. GNN/ECMP=0.778, GNN/MLP=0.808, 统计显著 p<0.0001
5. 泛化全部 PASS Contract 门控（≤1.10），E05(288节点)GNN/ECMP=1.014
6. 架构高度鲁棒（层数/头数变化<2%）

### H015-visualize-paper-materials
P2 可视化 + P3 论文叙事完成。12 张图用 SciencePlots science 样式重做（600 DPI, 统一配色, 无冗余标注）。论文叙事材料 paper-materials.md 包含：A+B 框架章节叙事大纲（Introduction→System Model→Method→Experiments→Conclusion）、DTAR Related Work 讨论文本+粒度对比表、TELGEN 方法特性对比表+差异化论证、Baseline 讨论文本、核心数据摘要 4 张表、图表规划。master-state 更新至 P2/P3 完成。

## 已确认结论

1. K-path 离散选择（逐流路由）范式优于 per-edge 连续权重范式
2. **surge=1.0 下 GNN 在所有条件（含无故障/均匀流量）都赢 ECMP**，旧"F2 正常条件弱"结论是 surge=5.0 假象
3. True ECMP(BFS全最短路)比 K=4 ECMP 仅好 1.35%，旧结果可信
4. GNN/ECMP=0.778, GNN/MLP=0.808, 统计显著 p<0.0001
5. 泛化全部 PASS Contract 门控（≤1.10），E05(288节点)GNN/ECMP=1.014
6. 架构高度鲁棒（层数/头数变化<2%）
7. **MLP 跨规模崩溃**（E04 MLP/ECMP=1.021, E05=1.118），GNN 在所有泛化规模赢 MLP（7.8%-25.6%）
8. 定位：Online Fault-Resilient Per-Flow Routing，三级贡献递进（故障弹性→在线逐流→跨规模部署）

## 未决项（可选补强，不阻断论文写作）

1. **E10/E11 多 seed** — F5 消融补 seed（差异<2%，可选，4-6h GPU）
2. **E12 故障模式对比** — 可降级为"未来工作"
3. **可视化精简** — 12 张图建议论文保留 6-8 张，其余放附录（见 paper-materials.md §6）
4. **中文标签** — 如需中文论文，图标签/图例需改为中文

## 当前位置

P0-P3 全部完成。实验+可视化+论文材料就绪，可进入正式论文写作阶段。

### 续接必读

1. `projects/leo-congestion-routing/master-state.md` — 全局进度+自检结果
2. `projects/leo-congestion-routing/paper-materials.md` — 论文叙事大纲+竞品讨论+数据表
3. `projects/leo-congestion-routing/contract.md` — 已冻结 Contract（含修正）
4. `projects/leo-congestion-routing/literature_notes.md` — 文献精读笔记
5. `projects/leo-congestion-routing/simulator/results/` — 实验数据
6. `projects/leo-congestion-routing/simulator/figures/` — 12 张图（600 DPI）
7. 本文件 — 完整进展线索+已确认结论

### 续接方向

- **写论文**：按 paper-materials.md 叙事大纲展开，12 张图选 6-8 张
- **补实验**：E10/E11 多 seed（可选）、时变拓扑实验（博士级）
- **答辩准备**：准备 DTAR 粒度差异话术、288 节点泛化解释、单拓扑族局限性应对
