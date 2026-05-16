# Handoff 2026-05-16 (Round 17) — Phase A Grid 标签完成，Execute 暂停

## 当前进度
- **阶段：Execute Step 1 → Phase A 完成**
- Contract 状态：**frozen**（待修订）
- Phase A: Grid 标签 GNN 训练完成，与 B1(N_LCT=4) 完全匹配
- **Execute 暂停，待用户决定下一步**

## Phase A 最终结果

### 训练
- 数据集: 500 snapshots, grid topology labels (960 edges / 5400 candidates, ratio 18%)
- 训练: F1=1.0, acc=1.0, 100 epochs, params=51,905
- 模型: `results/phase_a_grid_24x20/phase_a_best.pt`

### 评估（5 episodes × 50 steps, pre-activated grid edges）

| Seed | B1(N_LCT=4) M1 | GNN M1 | Ratio | M3 (both) |
|------|----------------|--------|-------|-----------|
| 42   | 0.1154         | 0.1154 | 1.000 | 0.0000    |
| 100  | 0.1015         | 0.1015 | 1.000 | 0.0000    |
| 200  | 0.1591         | 0.1593 | 1.002 | 0.0000    |

**结论：GNN 完美复现 grid 拓扑，与 B1 完全匹配。**

### 与之前结果的对比修正

| 方法 | M1 | 边数 | edges/sat | 说明 |
|------|-----|------|-----------|------|
| B1 (未剪枝) | 0.1739 | 1440 | 6.0 | handoff 原数据，**不公平对比** |
| B1 (N_LCT=4) | 0.1154 | 960 | 4.0 | 正确基线 |
| Phase A (ILP标签) | 0.079 | ~93 | ~0.4 | D029, 代理目标 |
| Phase A (Grid标签) | 0.1154 | 960 | 4.0 | **本论结果, ratio=1.000** |
| Prior (active_bias=3) | 0.078 | ~93 | ~0.4 | D020 |

## 关键发现

1. **路由感知贪心搜索不可行** (D031): grid 是完美 4-正则图，N_LCT=4 阻塞所有单边替换；路由 146ms/次，全数据集>100h
2. **B1 基线数据修正** (D032): handoff 的 M1=0.174 是未剪枝 B1 (6 edges/sat)，正确 B1(N_LCT=4) M1=0.115
3. **24×20 规模 grid 已是最优**: 无法通过学习超越（D024 swap 诊断 + N_LCT 阻塞均确认）
4. **GNN 可以完美学习专家拓扑**: F1=1.0, 零切换, 匹配基线 — 验证了架构和管线

## 已完成的代码资产

### 修改文件
```
simulator/config.py              — N_LCT=3→4 [D030]
simulator/generate_dataset.py    — 重写: grid 标签生成（替代 ILP/贪心）
```

### 已生成数据
```
data/grid_dataset_24x20/         — 500 snapshots, grid topology labels
results/phase_a_grid_24x20/      — Phase A 训练结果 (F1=1.0)
```

### 保留未变的文件（Phase A ILP 资产，可复用）
```
simulator/ilp_solver.py
simulator/discrete_wrapper.py
simulator/train_supervised.py    — 不变，已验证兼容 grid 数据集
simulator/train_ppo_discrete.py  — Phase B 待用
simulator/model_gat.py           — SupervisedGNN + DiscreteRLGNN
```

## 下一步选项（待用户决定）

### A. Phase B 离散 RL 微调
- 用预训练 GNN backbone 初始化 DiscreteRLGNN
- 3-way 动作空间 {AS-IS, FORCE-ON, FORCE-OFF}
- 目标: 在动态场景下超越静态 grid（如边失效、流量突变）

### B. 全规模 24×66 验证
- 1584 星规模，候选边 ~65K（12x 于 24×20）
- grid 在全规模可能有优化空间（跨轨候选更丰富）
- 需要: 候选边预筛选 + GPU 加速路由

### C. 归档当前方向
- 整理结果作为"学习最优拓扑"的贡献
- 转向其他研究问题（如 beam-hopping）

## 决策索引
- D031: 路由感知贪心不可行→grid 标签
- D032: B1 基线修正（0.174→0.115）
- D033: Phase A grid 完美匹配 B1(N_LCT=4)

## 新对话应读的文件
1. 本 handoff
2. `projects/leo-isl-scheduling-drl/decision_log.md` D031-D033
3. `simulator/generate_dataset.py` — grid 标签生成逻辑
4. `simulator/model_gat.py` — SupervisedGNN / DiscreteRLGNN
5. `baselines/grid_fixed.py` — B1 基线（注意 n_lct 参数）
