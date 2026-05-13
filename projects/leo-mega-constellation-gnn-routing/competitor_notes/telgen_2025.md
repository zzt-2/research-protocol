# TELGEN: Traffic Engineering in Large-Scale Networks With Generalizable Graph Neural Networks

- **来源**: IEEE/ACM Transactions on Networking, 2025
- **DOI**: 10.1109/TON.2026.3659135
- **arXiv**: 2503.24203
- **作者**: Fangtong Zhou, Sihao Liu, Xiaorui Liu, Ruozhou Yu, Guoliang Xue (NCSU + ASU)
- **引用**: 0（刚发表）
- **威胁等级**: 中

## 网络架构

- **GNN 类型**: 定制消息传递 GNN（非标准 GCN/GAT/GraphSAGE）
- **图结构**: LP 公式图（4 类顶点：路径变量 V^p、需求约束 V^d、链路约束 V^l、目标 v_o；6 类有向消息传递方向）
- **双层循环**: K 个外层（模拟 IPM 迭代），每外层 J=2 内层 GCN
- **编码器**: 2 层 MLP（180, 360），读出: 2 层 MLP（360, 720）
- **参数共享**: 所有外层共享参数

## Generalizable 的具体含义

**是 size generalization**，且规模扩展惊人：

| 数据集 | 训练规模 | 测试规模 | 规模因子 |
|--------|---------|---------|---------|
| Erdos-Renyi | 20-100 节点 | 200-2000 节点 | **最高 20x** |
| Waxman | 200-800 节点 | 2000-5000 节点 | **最高 6x** |
| ASN (Internet AS) | 217, 237 节点子图 | 553, 1739 节点 | **最高 7x** |

- OnoCGap < 3%（20x 规模下）
- 机制：IPM 算法模仿 → 模型继承算法的问题实例无关性

## 实验设置

- **任务**: Traffic Engineering — 多路径流量拆分（LP 公式），非路由
- **方法**: 监督学习（模仿 Interior Point Method 求解过程）
- **无 LEO 卫星实验**: 引言提及 LEO 为动机，但未做任何卫星实验
- **Baseline**: SciPy IPM, TEAL, HARP

## 与候选方案重叠度

| 维度 | TELGEN | 我们 | 重叠 |
|------|--------|------|------|
| 问题 | TE（LP 流量拆分） | 路由（每跳决策） | 低 |
| GNN 图 | LP 公式图 | 物理卫星拓扑图 | 不同 |
| 规模泛化 | 是，20x | 是，计划星座规模 | 高 |
| 领域 | WAN/云骨干 | LEO mega-constellation | 不同 |
| 位置编码 | 无 | 计划使用 | 新颖 |
| 动态拓扑 | 无（静态快照） | 有（时变轨道） | 新颖 |
| 训练范式 | 监督（IPM 模仿） | DRL | 不同 |

## 结论

TELGEN 是"网络 TE 中 GNN size generalization"的先例，但：
1. 不在卫星领域（仅提及为动机）
2. 不做路由（做 TE 流量拆分）
3. 不用位置编码
4. 不处理动态拓扑
5. 最大测试 5000 节点，非 mega-constellation 规模

**差异化要点**: LEO 特有挑战 + 路由 vs TE + 位置感知 GNN + 动态拓扑
