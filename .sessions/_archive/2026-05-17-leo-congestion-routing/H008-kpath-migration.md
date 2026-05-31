# Handoff 2026-05-17

## 当前进度

- 阶段：Execute Step 2 → Contract Amendment + K-path 迁移
- 状态：需要修改
- Contract 状态：需 amendment（动作空间变更）
- 本轮完成：Quick Test + E01 seed 0 + 根因分析 + 范式迁移决策

## 关键上下文

### 根因（必读）

**MVE 和正式模型使用了完全不同的架构**。MVE 用 K-path 离散选择（逐流路由）beat ECMP 12%，但正式模型设计为 per-edge 连续权重（同时路由所有流）。加权 Dijkstra 单路径路由的表达力低于 ECMP 多路径分流，导致 GNN 无法超越 ECMP。

详细对比见本轮分析，或直接读 MVE 代码（下方索引）。

### E01 Seed 0 结果（per-edge 范式，已废弃）

- GNN MLU: 2.1093 ± 0.885
- GNN/ECMP: 1.07 (FAIL, target ≤ 0.90)
- GNN/MLP: 0.84 (PASS, target ≤ 0.85)
- 训练 330ep 被 KL early stop 截断

### GNN/MLP=0.84 仍然有效

message passing 优势与路由范式无关。迁移到 K-path 后此优势应保持。

## 下一步：K-path 迁移

### Contract Amendment（需要用户确认）

修改项：

1. **动作空间**: per-edge continuous weights (E=264 维) → per-flow discrete K-path selection (K 维)
2. **路由方式**: 同时路由所有流 → 逐流顺序路由
3. **奖励**: -MLU (绝对) → -(MLU_after - MLU_before) (增量)
4. **模型输出**: EdgeWeightDecoder → PathScoringHead
5. **不可修改项**: hypothesis 目标值、success/failure signal、fairness rules、ablation plan 保持不变

### K-path 设计规格

#### Episode 结构

- 每步路由一条流，episode 长度 = n_flows (40 步 for 66 节点)
- 每步：生成 K 条候选路径（K=4），模型评分选择最优，更新链路负载

#### 模型架构

```
GATEncoder (保留):
  in_proj(6 → 64) → GAT × 2 (4 heads, LN, Residual, ELU)

PathScoringHead (新增，替代 EdgeWeightDecoder):
  对每条候选路径: mean(node_emb[path_nodes]) → MLP(64→32→1) → score
  K 条路径 → K 个 score → Categorical(logits)

ValueHead (保留):
  src_emb ∥ dst_emb → FC(128→64→1)
```

#### Env 变更

- step(action): action 是 int (0~K-1)，选择第 action 条候选路径
- reset: 注入故障 → 生成所有流 → 返回第一条流的 obs
- obs 包含: node_feat(N,6), edge_index(2,E), edge_feat(E,4), paths(K 条候选路径), flow(src,dst,demand)
- 奖励: -(MLU_after - MLU_before)

#### 关键：K 路径生成

- 用 nx.shortest_simple_paths() 生成 K 条候选路径（与 MVE 一致）
- 故障边从拓扑中物理移除（非权重 mask），这样 shortest_simple_paths 自然绕过故障
- 路径在每步重新生成（因为上一条流的路由改变了链路负载，但不改变拓扑）

#### Baseline 适配

- SP: 选第一条路径（最短）
- ECMP: 从等长路径中 round-robin
- MLP: 用局部特征（1-hop 负载）代替 GNN embedding，同样 K-path 选择
- DTAR/GMR: 待 Execute 后续阶段适配

### 迁移执行顺序

1. Contract amendment（需用户确认）
2. 更新 data-flow.md §5-7
3. 重写 env.py（参考 mve_env.py 的逐流路由逻辑）
4. 修改 model.py（PathScoringHead 替代 EdgeWeightDecoder）
5. 修改 train.py（Categorical 替代 Normal，离散动作空间）
6. 适配 baselines
7. 重跑 verify 套件
8. Quick Test → E01

### 恢复读取顺序（新对话）

1. 本 HANDOFF 文件
2. `master-state.md`
3. `contract.md`（amendment 版本）
4. `data-flow.md`（更新版本）
5. `mve_env.py` + `mve_train.py` + `mve_66.py`（K-path 参考实现）
6. `stages/execute.md`
7. `code-quality.md`

## 项目文件索引

### 本轮产出

- `decision_log.md` — D14 (Quick Test), D15 (范式迁移)
- `worker-logs/step1-quick-test.md` — Quick Test 结果
- `worker-logs/e01-seed0.md` — E01 seed 0 结果
- `simulator/results/eval_seed0.json` — 评估数据
- `.sessions/framework-evolution/LOG-008-action-space-alignment.md` — 框架漏洞分析

### 关键文件（新对话需要读）

- `projects/leo-congestion-routing/contract.md` — 需 amendment
- `projects/leo-congestion-routing/data-flow.md` — 需更新
- `projects/leo-congestion-routing/simulator/env.py` — 需重写
- `projects/leo-congestion-routing/simulator/model.py` — 需修改
- `projects/leo-congestion-routing/simulator/train.py` — 需修改
- `projects/leo-congestion-routing/mve_env.py` — **K-path 参考实现**
- `projects/leo-congestion-routing/mve_train.py` — **K-path 模型参考**
- `projects/leo-congestion-routing/mve_66.py` — **K-path 66节点参考**
- `projects/leo-congestion-routing/simulator/config.py` — SimConfig 需加 K 参数
- `projects/leo-congestion-routing/baselines/` — 需适配
