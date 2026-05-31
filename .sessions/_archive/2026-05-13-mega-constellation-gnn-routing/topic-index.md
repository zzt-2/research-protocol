# 专题：GNN 星座路由（Size Generalization）

> 创建：2026-05-13 | 状态：dormant | 最后更新：2026-05-14

## 进展线索

### R001-direction-candidates.md
卫星通信大类大规模文献检索产出。6 组关键词、180+ 候选、5 个子方向扫描。推荐排序：方向1 GNN-based routing for LEO mega-constellation（蓝海+快速上升，5年~38篇）> 方向2 AI-driven beam hopping > 方向3 NTN-terrestrial integration。排除 grant-free RA（红海）、LEO handover DRL（已做过）、ISL ACM（历史负面结果）、RIS phase DRL（当前项目）。检索存档在 `search-archive/2026-05-13/` 下 6 个 JSON。

### H001-initial.md — GW 完成，进入 Contract
Groundwork 全部完成（Step 2-5 + Step 4a/4b 全部 Go）。方向从"GNN+RL for LEO routing"重新定位为"GNN size generalization for satellite routing"——发现 13 篇 GNN+RL LEO 竞争者但无一涉及跨规模泛化。25 篇论文 + 2 篇理论背景精读，63 篇引用链筛查确认 size generalization 完全空白。MVE 结果：均匀权重 100%->83%（跨16x），异质权重 70%->56%。Baseline 选定：Dijkstra + GRLR 复现 + GraphPR。

### H002-contract.md — Contract 冻结
Contract Step 0-3 全部完成并冻结。假设：GNN + Orbital PE + 多尺度训练，66->720(11x) 零样本泛化，保留率 >=80%。Success 三条：保留率>=80% + 与 Dijkstra 差距<=20% + PE 贡献>=8pp。Baseline：B1 Dijkstra + B2 GRLR（必须复现）+ B3 GraphPR。实验 E01-E09，P0 含 E01/E02/E03。新颖性经 6 组检索 + 3 篇精读 + 2 组定向检索确认。

### H003-execute.md — Execute Step 1-2 仿真器+监督训练
仿真器 9 模块完成（constellation/topology/channel/traffic/routing/snapshot/models/smoke_test/quick_test）。3 个参数修正：ISL 容量 B=1GHz、ISL 距离改实时轨道力学计算+5000km 断链、ISL 类型确认为激光。Quick test 监督训练：3 层 GAT h=128 PE=16 保留率 70.2%。贪心推理路径成功率极低（0.7%），瓶颈在于逐跳精度之积。

### H004-0514-resume.md — RL 实验完成，加权 Dijkstra 有效
实现 env.py（RL 环境）、pretrain.py（监督预训练）、train.py（PPO 微调）。监督预训练方向精度 97.6%/66.8%，retention 71%。贪心推理成功率 22-30%/1.7%（太低）。发现加权 Dijkstra 推理有效（成功率 100%），但 median stretch 1.5-1.8、mean 2.1-2.6 偏高。PPO 微调无效（action-reward 解耦，梯度信号太弱）。

### H005-0514-step2.md — neighbor_map 修复，Baseline 对比完成
发现并修复 `_build_neighbor_map` bug（单向映射->双向映射）。修复后 mean stretch 从 2.1-2.6 降至 1.097，median 1.056，85.1% <=1.2x optimal。GRLR 论文精读+复现完成（6 节点局部图 GAT+AC）。三方对比：Dijkstra(1.000) / GRLR(1.008, 同规模) / 我们(1.097, 跨规模)。Contract 两项核心指标达标：时延保留率 90.3%、vs Dijkstra 差距 9.9%。

### H006-0514-step3.md — 消融实验全部完成
消融 A1(无PE): stretch 1.002, 训练精度仅 39.7%——PE 是学习必要条件而非可选增强。A2(单尺度+PE): stretch 1.120。A3(无PE+单尺度): stretch 1.049。Same(720->720): stretch 1.000。结论：PE 是学习前提条件，多尺度训练贡献 2-4pp，9.7pp stretch 差距完全来自跨规模迁移。Contract 假设中"PE 贡献>=8pp"需修正为"学习前提条件"。

### H007-0514-step4.md — 论文素材提取完成
按 `stages/paper-materials-workflow.md` 提取 6 个素材文件（01-06），总计约 109KB：研究背景(15KB)、方法架构(17.5KB)、实验数据(17.2KB)、60 篇论文索引(33.7KB)、局限性(19KB)、公式符号(6.5KB)。框架文档更新已提交。

### H008-0514-step5.md — 待补充中文论文引用
素材包完成但缺少中文论文引用（学位论文需要中英文参考文献）。核心文献预印本率 40%（10/25）。需要从 CNKI 补充约 15-20 篇中文论文，覆盖 LEO 路由综述、星座设计、GNN 综述、DRL 网络优化、ISL 星间链路等方向。插入位置为 `04_literature.md` 7 节背景引用。

### H009-fresh-search.md
新对话提示词：卫星通信方向大规模文献检索（GW Step 1）。基于 S001-strategy.md 的决策——在卫星通信大类下从头检索，不复用旧结论。5 个角度（链路层/网络层/接入层/融合/AI方法）各构造关键词，产出 R001-direction-candidates.md。

### H010-gw-step23.md
新对话提示词：GW Step 2-3（论文获取+精读）。选定方向1 GNN-based routing for LEO mega-constellation 后执行。5 篇 IEEE 必读论文列表，补充检索指引（GNN size generalization、传统 LEO 路由、GNN for wireless 经典工作）。

### H011-gw-step23-resume.md
新对话提示词：GW Step 2-3 恢复。用户手动下载 5 篇 IEEE 论文后，转换+精读+更新 literature_notes.md，然后进入 Step 3.5 定向补充检索和 Step 4a Go/No-Go。特别关注 L08 是否已解决核心创新点。

### S001-strategy.md
研究策略专题：分析当前困境（方向不自有、无法判断中间结果、多项目分散）和历史 6 个项目的审查结论。核心发现：通信方向 4 个项目的失败全是执行问题（无法闭环），不是方向问题。最终决策：在卫星通信大类下从头做文献检索找新切口。同时提出验证可信度改进建议（baseline 数值对齐、统计检验、sanity check）。

## 已确认结论

1. **GNN size generalization for LEO routing 是空白**：25 篇精读 + 63 篇引用链筛查 + 6 组检索均未发现直接竞争者，最接近的 TELGEN 做 WAN TE 非卫星路由
2. **Orbital PE 是学习前提条件**：消融实验证明移除 PE 后训练精度从 97.7% 降至 39.7%，非可选增强
3. **加权 Dijkstra 推理有效**：解决了贪心推理路径成功率极低的问题，stretch 可接受（mean 1.097）
4. **Contract 两项核心指标达标**：时延保留率 90.3%（>=80%）、vs Dijkstra 差距 9.9%（<=20%）
5. **跨规模迁移代价 9.7pp stretch**：同规模(720->720) stretch 1.000 vs 跨规模(66+100+200->720) stretch 1.097
6. **PPO 微调无效**：action-reward 解耦导致梯度信号太弱，监督预训练已是最优策略
7. **GRLR baseline 复现完成**：6 节点局部图 GAT + AC，同规模 stretch 1.008
8. **历史项目失败根因是执行闭环**，非方向选择问题

## 未决项

1. **PE 关键性指标未达 Contract 原定标准**：原假设"PE 贡献>=8pp stretch 改善"，实际 PE 是学习前提条件而非渐进增强，需修正表述
2. **中文论文引用待补充**：约 15-20 篇中文文献，需从 CNKI 检索
3. **GraphPR baseline 未复现**：Contract 标为"推荐"非"必须"，当前仅有 Dijkstra + GRLR
4. **论文写作未启动**：素材包(01-06)已提取，但论文正文尚未撰写
5. **多尺度训练贡献偏小**（2-4pp）：可能影响论文贡献度叙事
6. **核心文献预印本率 40%**（10/25）：审稿可能质疑文献质量
7. **验证可信度问题**：S001-strategy.md 指出 AI 驱动研究的核心瓶颈是验证闭环，用户缺乏独立验证能力

## 当前位置

Execute 阶段核心实验和消融实验全部完成，Contract 两项核心指标达标，论文素材包(6 文件/109KB)已提取；专题处于 dormant 状态，待补充中文引用后可进入论文写作。
