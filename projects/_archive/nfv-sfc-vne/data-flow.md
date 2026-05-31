# 端到端数据流推演

> 产出阶段：Contract Step 4
> 用途：Execute 阶段的参考设计文档

## 1. 网络配置 → 节点位置

- 输入：拓扑配置（Waxman/GEANT/BRAIN/WX500）+ 节点 CPU ~U[50,100] + 链路 BW ~U[50,100]
- 处理：Virne 拓扑生成器创建 substrate network
  - Waxman(n, α=0.5, β=0.2): 边概率 f(d) = α * exp(-d/(β*L))
  - GEANT: 23 节点固定拓扑（欧洲学术网）
  - BRAIN: 161 节点固定拓扑
  - WX500: Waxman 500 节点
- 输出：p_net = (N_p 节点, E_p 边)
  - node_attrs: CPU 容量 [N_p]
  - edge_attrs: BW 容量 [E_p], 延迟 [E_p]（if available）

## 2. VNR 生成 + SFC 叠加

- 输入：VNR 配置 + SFC 配置（sfc_ratio=0.6, vnf_types=5）
- 处理：
  1. 生成 random graph（Erdos-Renyi, p=0.5, size U[2,10]）
  2. 选取 sfc_ratio 比例节点标记为 VNF → SFC chain
  3. 每个 VNF 分配类型 id ∈ {1..5}
  4. 按 VNR 拓扑序排列 SFC chain
- 输出：v_net = (N_v 节点, E_v 边)
  - node_attrs: CPU 需求 [N_v], vnf_type [N_v] (0=非VNF, 1..5=VNF)
  - edge_attrs: BW 需求 [E_v]
  - graph_attrs: sfc_chain [ordered VNF node IDs], sfc_vnf_types [N_v]

维度示例：平均 VNR size=6, SFC VNF≈3.6, 边≈7.5

## 3. Episode 初始化 + 节点排序

- 输入：p_net + v_net
- 处理：
  1. InstanceRLEnv 初始化 episode
  2. 节点排序：SFC VNF 按链序优先，非 VNF 按 node_ranking_method（GRC rank）
  3. 逐节点放置：每步选一个 VNR 节点 → 选 substrate 节点映射
- 输出：有序节点列表 [v_0, v_1, ..., v_{N_v-1}]，SFC VNF 在前

## 4. 状态构造

- 输入：p_net 当前状态 + v_net + 已映射部分 + 当前 v_node
- 处理：
  - **p_net 特征** (Virne feature constructor, all solvers):
    - resource(CPU): 1 dim
    - status_flags(S,T): 2 dim
    - aggregated_link_attrs: ~2 dim
    - degree: 1 dim
    - topological_metrics: ~2-3 dim
    → **~8-10 dims/node**, output: [N_p × 8-10]
  - **v_net 特征** (base, all solvers):
    - resource(CPU, BW): 2 dim
    → **~2 dims/node**, output: [N_v × 2]
  - **SFC metadata** (MatchingGAT only):
    - vnf_type: int → embedding → 128 dim
    - sfc_position: int → embedding → 128 dim
- 输出：
  - p_net: PyG Data(node_features [N_p × 8-10], edge_index [2 × E_p], edge_attr [E_p × dim])
  - v_net: PyG Data(node_features [N_v × 2], edge_index [2 × E_v], edge_attr [E_v × dim], **sfc_vnf_types, sfc_positions**)
  - curr_v_node_id: int

## 5. 模型输入

- 输入：步骤 4 输出
- 处理：
  1. **特征嵌入**:
     - p_net node features → MLP → [N_p × 128]
     - v_net node features → MLP → [N_v × 128]
  2. **SFC 位置编码** (MatchingGAT only):
     - vnf_type_ids → Embedding(5, 128) → [N_v × 128] → 加到 v_node embs
     - sfc_positions → Embedding(max_chain, 128) → [N_v × 128] → 加到 v_node embs
  3. **GNN 编码** (3 层 GATConv):
     - p_net_encoder: [N_p × 128] → [N_p × 128] (p_node_dense)
     - v_net_encoder: [N_v × 128] → [N_v × 128] (v_node_dense)
  4. **跨图注意力** (MatchingGAT only):
     - curr_v_emb: [128] 从 v_node_dense 提取
     - Cross-attention: p_nodes × curr_v_emb → enhanced_p_nodes [N_p × 128]
     - 不使用时: p_node_dense + curr_v_emb (简单加法)
  5. **图级嵌入**:
     - p_g_emb: mean_pool(p_node_dense) → [128]
     - v_g_emb: mean_pool(v_node_dense) → [128]
  6. **最终嵌入**:
     - p_node_final = enhanced_p_nodes + v_g_emb → [N_p × 128]
- 输出：
  - actor: p_node_final → Linear(128, 1) → action logits [N_p]
  - critic: concat(p_g_emb, v_g_emb) → MLP → value [1]

## 6. 模型输出 → 动作映射

- 输入：action logits [N_p] + action mask [N_p]
- 处理：
  1. Action masking: 不合法节点 logits = -inf
     - 资源约束: 剩余 CPU < VNR 需求
     - SFC 约束: 当前 VNF 无法到达上一个 VNF 物理位置
  2. Softmax → action probability [N_p]
  3. PPO sampling / greedy → selected p_node_id
- 输出：selected p_node_id (int, 0..N_p-1)
- 后续: 节点映射完成后，链路映射用最短路径（Virne 默认）

## 7. 奖励/损失计算

- 输入：每步 action + episode 最终结果
- 处理：
  - 中间步骤成功: +0.1
  - 中间步骤失败: -0.1 (episode 终止)
  - Episode 成功: R2C = revenue / cost
    - revenue = Σ(v_node_cpu) + Σ(v_edge_bw)
    - cost = Σ(allocated_p_node_cpu) + Σ(allocated_p_edge_bw)
- 输出：scalar reward

PPO loss = policy_loss + 0.5 × critic_loss − 0.01 × entropy

## 8. 评估指标

- 输入：评估集 episode 结果
- 处理：
  - AC = count(success) / count(total)
  - R2C = mean(revenue/cost) over successful episodes
  - 收敛速度 = first epoch where R2C ≥ 0.95 × final_R2C
- 输出：AC (float), R2C (float), convergence_epoch (int)

## 跨规模泛化

- 训练配置：WX100 (100 nodes)
- 推理配置：GEANT (23), BRAIN (161), WX500 (500)
- 变化维度：N_p (23→500), E_p (~50→~1250)
- 不变维度：embedding (128), GNN output (128 per node)
- 处理方式：GNN 输出 per-node embedding，N_p 变化仅影响 batch dimension，无维度断裂

## 动作空间表达力审计 [FR-13]

| Baseline | Baseline 决策能力 | 模型决策能力 | ≥? |
|----------|-----------------|-------------|-----|
| B1: GRC | 按 capacity 排序选 substrate 节点（贪心） | 学到的策略选 substrate 节点 | ≥ |
| B2: PPO-DualGAT+ | DualGAT 编码 + PPO 选 substrate 节点 | MatchingGAT（DualGAT 超集 + cross-attn + SFC PE） | ≥ |
| B3: PG-MLP | MLP 编码 + PG 选 substrate 节点 | GNN + PPO（GNN 表达力 > MLP） | ≥ |
| B4: CONAL | 约束感知选 substrate 节点 | 同 action space + SFC 感知（环境 masking + SFC PE） | ≥ |
| B5: PPO-DualGCN | DualGCN 编码 + PPO 选 substrate 节点 | MatchingGAT（GAT + cross-attn > GCN） | ≥ |

**结论**: 全部 ≥。所有方法共享相同动作空间（选 substrate 节点），差异在信息处理方式，不在决策空间。

**SFC 信息不对称声明**: MatchingGAT 额外接收 vnf_type + sfc_position 信息，其他 baseline 不接收。这是核心方法贡献（主动利用 SFC 结构），非信息泄露。消融 A1 量化此增量。
