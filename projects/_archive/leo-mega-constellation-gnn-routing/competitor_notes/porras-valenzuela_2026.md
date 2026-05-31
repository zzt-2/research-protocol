# Size Transferability of Graph Transformers with Convolutional Positional Encodings

- **来源**: arXiv 2026 (preprint)
- **arXiv**: 2602.15239
- **作者**: Javier Porras-Valenzuela, Zhiyang Wang, Alejandro Ribeiro (UPenn)
- **引用**: 0
- **威胁等级**: 低（技术借鉴价值高）

## 核心方法

### 位置编码（RPEARL）
- 从各向同性高斯分布抽取 M 个随机节点特征 z^(m) ~ N(0, I_N)
- 每个特征通过 K 阶 TAGConv（图卷积滤波器）
- 对 M 个输出经验平均恢复置换等变性
- PE 添加到节点特征后馈送至 Transformer 层

### Size Transferability 机制
- 可迁移性从 PE 继承：GNN PE 收敛到流形神经网络 (MNN) 极限
- GT 输出随之收敛到流形 Transformer 极限
- Theorem 1: GT 与 MT 输出点态差异 ≤ O((log N / N)^{1/d})，d >= 3 为流形本征维度

## 理论贡献

- **Theorem 1**: GT 点态收敛到 MT
- **Corollary 2**: 两图 G_1(N_1), G_2(N_2) 的 GT 输出差异以 N_1, N_2 为界
- **Corollary 3**: RPEARL PE 架构的显式收敛界
- **Corollary 4**: 扩展到 k-hop 稀疏 GT（复杂度从 O(N²) 降至 O(k-hop)）

**条件**: 图从平滑黎曼流形采样，有界密度，d >= 3 本征维度，Q/K/V 正则化

## 实验

- **任务**: 节点分类（SNAP-Patents 1.7M 节点、ArXiv-year、OGBN-MAG）+ 地形最短路径距离估计
- **跨规模**: 用完整图 10.5% 训练达峰值准确率 ~90%
- **SPD 估计**: ~10K 节点训练 → 一个数量级大图测试

## 与候选方案关系

| 维度 | 这篇 | 我们 |
|------|------|------|
| 架构 | Graph Transformer | GNN (消息传递) |
| 任务 | 节点分类/度量学习 | LEO 卫星路由 |
| PE | RPEARL 卷积 PE | 计划使用 |
| 理论 | 流形收敛 | 可借鉴 |

**技术借鉴价值**:
1. RPEARL PE 可集成到 GNN 路由架构中
2. Walker-Delta 星座可建模为轨道球面离散采样，满足流形收敛假设
3. Theorem 1 的界可为 GNN 泛化提供理论依据
4. k-hop 稀疏 GT 策略适合卫星拓扑稀疏性

**非竞争者**: 架构不同（GT vs GNN）、任务不同（分类 vs 路由）、领域不同（通用图 vs 卫星网络）
