# Handoff: MatchingGAT 架构缺陷修复

> 来源: Execute Step 0-2 | 交接目标: 修复架构缺陷后重新执行 E1
> 文件名: H009-matching-gat-arch-fix.md

## 已完成边界

### Execute Step 0 审计 ✅
- 声称-证据映射完整、Tier 1 全 pass、仿真器已就绪

### E1 实验脚本准备 ✅
- `verify/run_e1.sh` — E1 主对比（多 seed 队列）
- `verify/run_grc_e1.py` — GRC 启发式基线（3 seeds 评估）
- `verify/summarize_e1.py` — E1 结果汇总表
- `verify/run_e2.py` — E2 跨拓扑（GEANT/BRAIN/WX500，拓扑路径已验证）
- `verify/run_e3.sh` — E3 消融（30ep × 3 seeds）
- `verify/summarize_e3.py` — E3 结果汇总表

### E1 后台任务已启动但需停掉
- Task ID: `b93rnid2l` — 正在跑 MLP seed=1（epoch ~9），需用 `TaskStop` 停掉
- 已跑完的部分数据可保留（MLP/DualGAT+ baselines 不受架构修复影响）

## 核心发现：MatchingGAT 架构缺陷

### 缺陷位置
`matching_policy.py` 第 119-123 行

### 缺陷描述
Cross-attention 输出 `curr_cross`（当前 v_node 对 substrate 的注意力加权和）通过 **统一加法** 注入到所有 substrate 节点：

```python
curr_cross = cross_out.gather(1, curr_v_node_id_exp.expand(...)).squeeze(1)
p_node_dense = p_node_dense + curr_cross.unsqueeze(1)  # ⚠️ 所有 p_node 加相同向量
```

这导致打分函数 `self.lin(p_node_dense)` 难以有效排序 substrate 节点——所有节点获得完全相同的附加信息。

### 症状
- AC 高 (0.968 vs DualGAT+ 0.958)：模型能找到可行放置
- R2C 低 (0.7898 vs DualGAT+ 0.8006)：放置效率差，-1.3%
- 根因：模型无法区分哪个 substrate 节点对当前 v_node 最优

### 修复方案

**推荐：改为逐节点交互**

方案 A（最简单）：element-wise multiply
```python
# 替换 p_node_dense = p_node_dense + curr_cross.unsqueeze(1)
p_node_dense = p_node_dense * curr_cross.unsqueeze(1)
```

方案 B（推荐）：混合加法 + 乘法交互
```python
# 保留原始信息，加入逐节点交互
interaction = p_node_dense * curr_cross.unsqueeze(1)
p_node_dense = p_node_dense + interaction
```

方案 C：dot-product affinity 作为额外打分
```python
# 在 forward 末尾，用 v-p 亲和度修正分数
curr_v_emb = v_node_dense.gather(1, curr_v_node_id_exp).squeeze(1)
affinity = torch.bmm(p_node_dense, curr_v_emb.unsqueeze(2)).squeeze(2) / (embedding_dim ** 0.5)
base_score = self.lin(p_node_dense).squeeze(-1)
return base_score + affinity
```

### Contract 影响
- 架构修改属实现细节，不涉及 hypothesis / success_signal / failure_signal / fairness_rules
- **无需 Contract Amendment**
- 消融组件（SFC PE / cross-attn / edge attrs）保留不变
- 但需注意：修复后重新跑 E1，旧的 seed=0 结果作废

## 不要做什么

- 不要继续跑旧版 MatchingGAT 的 30ep 训练——架构有缺陷，结果无意义
- 不要改 Contract 的 success/failure signal——先看修复后结果
- 不要跳过 5ep 快速验证直接跑 30ep——先用短实验确认修复有效
- E1 已跑的 MLP/DualGAT+ baselines 数据可以保留（不受 MatchingGAT 架构影响）

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 当前状态（暂停，待修复）
2. `projects/nfv-sfc-vne/contract.md` — 冻结的 Contract
3. `projects/nfv-sfc-vne/Virne/virne/solver/learning/sfc_solver/matching_policy.py` — **需修改的文件**
4. `stages/execute.md` — Execute 阶段流程

## 下一轮

1. **停 E1**: `TaskStop` task_id=`b93rnid2l`
2. **修复 matching_policy.py**: 将第 121-123 行的统一加法改为逐节点交互（推荐方案 B）
3. **5ep 快速验证**: 跑修复后的 MatchingGAT 5ep + DualGAT+ 5ep，对比 R2C 趋势
4. **如果验证通过**: 重跑 E1（MatchingGAT + DualGCN seeds 0,1,2）+ E3（消融 30ep）
5. **如果验证不通过**: 进一步分析，考虑方案 C 或其他交互方式
