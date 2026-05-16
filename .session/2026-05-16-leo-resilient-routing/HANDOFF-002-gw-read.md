# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 3（精读）完成，Step 3.5（补充）待启动
- 状态：完成
- 本轮完成：精读 7 篇论文（6 必读 + 1 竞品 FCRMJ），综合分析写入 literature_notes.md

## 关键上下文
- 项目目录：`projects/leo-resilient-routing/`
- 精读完成论文：L01-GRLR, L02-GraphPR, L03-MS-SNS, L05-MegaResilience, L06-DDPG-LBBP, L07-ADRLRM, P1-FCRMJ
- L04-DLNoConv (JOCN, 10.1364/JOCN.474791) 未获取——非 arxiv，blit 不支持 Optica，需手动下载或跳过
- 已下载未精读：P2-GDRL-SFCR, P3-GROGU, P4-QueueMARL（待确认论文，非必读）
- 综合分析结论：GNN+LEO 故障恢复方法空白确认，FCRMJ 为最直接竞品（MLP 无拓扑感知）

## 竞品差异化空间（与 FCRMJ 对比）
1. **GNN 拓扑感知** vs MLP 无拓扑感知——最本质架构差异
2. **可学习故障传播** vs 手工衰减系数 γ
3. **动态故障注入场景** vs 静态故障率测试
4. **端到端学习拥塞风险** vs 手工度中心性+队列加权

## 论文下载路径映射
| 编号 | 论文 | content.md 路径 |
|------|------|-----------------|
| L01 | GRLR | papers/doi/10.1109_tvt.2024.3471658/content.md |
| L02 | GraphPR | papers/manual/10755127/content.md |
| L03 | MS-SNS | papers/manual/11398382/content.md |
| L04 | DLNoConv | ❌ 未获取 (JOCN 付费) |
| L05 | MegaResilience | papers/arxiv/2509.06766/content.md |
| L06 | DDPG-LBBP | papers/manual/faulty-links-fast-recovery-method-based-on-deep-re/content.md |
| L07 | ADRLRM | papers/manual/11126166/content.md |
| P1 | FCRMJ | papers/manual/11504878/content.md |
| P2 | GDRL-SFCR | papers/doi/10.3390_s25041232/content.md |
| P3 | GROGU | papers/manual/11229839/content.md |
| P4 | QueueMARL | papers/arxiv/2605.04448/content.md |

## 下一步
1. 读 `stages/gw-supplement.md`（Step 3.5 框架文件）
2. 检查精读论文的引用链，识别 GW 未覆盖但竞品共引的基础文献
3. 如有必要，执行定向补充检索
4. 之后进入 Step 4a（Go/No-Go 可行性预判），读 `gw-feasibility.md`
