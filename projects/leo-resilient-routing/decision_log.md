# Decision Log

## 阶段摘要
- [Direction Scouting] 方向侦察完成，推荐作为第二研究方向（与 ISL 调度组合）
- [Groundwork Step 1-2] 检索+初筛完成 (2026-05-16)
  - 7个JSON文件 210 条原始 → 168 去重 → 37 相关候选
  - 必读7 / 建议读20 / 待确认4 / 备选6
  - 质量门槛全部通过（详见 literature_notes.md）
  - GNN+LEO故障恢复方法空白再次确认
- [Groundwork Step 3] 精读完成 (2026-05-16)
  - 6 必读 + 1 竞品(FCRMJ) 共 7 篇精读完成
  - 4 篇待确认论文全部验证：FCRMJ 确认正式发表(CISCE 2026)，GDRL-SFCR/GROGU/QueueMARL 均已确认
  - L04-DLNoConv (JOCN) 无法自动下载，标记为后续补充
  - 综合分析完成：GNN+故障恢复方法空白再次确认，FCRMJ 为最直接竞品（MLP 无拓扑感知）
- [Groundwork Step 3.5] 定向补充检索完成 (2026-05-16)
  - 4 组定向检索(GraphSAGE/GNN容错/时序GNN/MARL) + FCRMJ 双向引用链
  - R1 新增 7 篇建议读，R2 新增 0 篇→收敛
  - 核心结论不变：GNN+专有故障恢复+LEO路由方法空白最终确认
  - 方法可迁移参考：GDAPS(GNN+MARL容错，SDN领域)、Iris(DRL增量训练容错)
- [Groundwork Step 4a] 可行性预判完成 → Pivot (2026-05-16)
  - A0 问题-方法适配性：5/5 项通过，无致命信号
  - 维度 A/B：通过（经修正：去掉 ≥15% 泛化间距无支撑声称，GNN 优势重新定位为拓扑感知负载均衡）
  - 维度 D MVE-1（18节点）：GNN MLU 差 5.8% → FAIL
  - 维度 D MVE-2（60节点）：GNN MLU 差 4.2% → FAIL
  - **结论：GNN 消息传递在路由决策维度不优于 MLP+手工特征，两次实验一致**
  - Pivot 决策：保留"故障感知抗毁路由"问题，方法转向 MARL+课程学习

## 决策记录

### D1: AI候选审查优先级标准 (2026-05-16)
- **决策**: 按子方向聚类标注优先级，而非单纯按引用量排序
- **理由**: 方向侦察已确认 GNN+LEO故障恢复为方法空白，审查重点在于覆盖4个子方向（DRL故障路由/GNN+DRL baseline/抗毁性分析/重路由恢复），确保每个方向都有充分文献支撑
- **结果**: 4个子方向均有≥4篇覆盖，空白确认无遗漏

### D2: 待确认论文验证结果 (2026-05-16)
- **决策**: 4 篇待确认论文全部验证发表状态
- **结果**：
  - P1 FCRMJ: IEEE CISCE 2026 会议论文(DOI:10.1109/CISCE69494.2026.11504878)，最直接竞品，已精读
  - P2 GDRL-SFCR: MDPI Sensors OA(DOI:10.3390/s25041232)，DRL+服务功能链，非核心竞品
  - P3 GROGU: IEEE WiSEE 2025(DOI:10.1109/WiSEE57913.2025.11229839)，GNN+DRL DTN路由
  - P4 QueueMARL: arXiv preprint(2605.04448)，MARL弹性路由

### D4: MVE 失败与 Pivot 决策 (2026-05-16)
- **决策**: MVE 两次失败后 Pivot，方法从 GNN 转向 MARL+课程学习
- **理由**: MVE-1(18节点) GNN MLU 差 5.8%，MVE-2(60节点) GNN MLU 差 4.2%。监督代理+Dijkstra 框架下 GNN 消息传递不优于 MLP+手工特征
- **Pivot 方向**: MARL 分布式决策 + 自适应课程学习（逐步增加故障复杂度）
- **备选**: 若 P1 不可行，转向 P2（在线自适应 DRL / Meta-RL）
- **教训**: GNN 拓扑感知优势需在特定任务结构中验证，非通用卖点。路由决策+监督代理不足以激活 GNN 优势
