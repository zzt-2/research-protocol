# Handoff 2026-05-16 (Round 18) — 动态场景(边失效)实验结果：Phase B 无效

## 当前进度
- **阶段：Execute Step 1 — 动态场景实验完成，Phase B 训练无效**
- Contract 状态：**frozen**（待修订）
- Phase A Grid 标签完成（D033），Phase B 离散 RL 微调失败（D037）
- **待方向决策**

## 本轮完成的工作

### 1. 边失效机制 (D035)
- `config.py`: 新增 `FAILURE_PROB=0.03`, `FAILURE_DURATION_MIN/MAX=2/5`
- `environment.py`: 每步随机失效活跃边，失效边不可被 LCT 选择和路由
- `grid_fixed.py`: 同样支持失效
- 冒烟测试: p=0.1 时 grid 吞吐量降 13.2%

### 2. 边特征维度 7→8 (D036)
- 新增第 8 维 `edge_feat[7] = 1.0 if failed`
- `model_gat.py`: `edge_dim` 默认值从 7→8，新增 `load_backbone_with_padding()`
- Phase A 权重 padding: 补零列，验证 max diff=0.0（完全一致）

### 3. Phase B 训练 (D037)
- 无 AS-IS 偏置: reward=-20（随机 FORCE-OFF 毁坏拓扑）
- 有 AS-IS 偏置(bias=5.0): best_reward=-10.3 vs Phase A=-12.4
- **但评估结果 Phase B = Phase A**: M1=0.109, M3=0.164
- RL 完全没学到有意义的策略

## 关键实验数据

### 动态场景评估 (24×20, p=0.05, 3 seeds, quick)

| 方法 | M1 | M3 | 说明 |
|------|-----|-----|------|
| Grid no fail | 0.1249±0.024 | 0.000 | 性能天花板 |
| Grid fail | 0.1091±0.022 | 0.000 | 被动损失 12.6% |
| Phase A (fail) | 0.1087±0.020 | 0.164 | ≈ Grid，切换抵消恢复 |
| Phase B (fail) | 0.1087±0.020 | 0.164 | = Phase A，RL 无效 |

### Phase A reward 量级分析 (p=0.05, 50 steps)
- Phase A no failure: total_reward=-5.07, M1=0.0853, M3=0.2437
- Phase A with failure: total_reward=-12.43, M1=0.0517, M3=0.6457
- 失效使 reward 恶化 ~7.4 单位（主要来自切换惩罚）

## 根因分析

### Phase B 失败原因
1. **AS-IS 偏置太强**: bias=5.0 → 98.7% 边选 AS-IS，探索不足
2. **信号太稀疏**: 仅 ~2% 边(100/5400)失效，PPO 信用分配无法从全局 reward 归因到个别边动作
3. **credit assignment 困难**: 全局吞吐量 reward vs 逐边动作空间，与 D021(先验>RL) 同一失败模式

### Phase A ≈ Grid 原因
1. **LCT 自动替补**: 失效边被 LCT 跳过 → 自动选替代边 → 吞吐量部分恢复
2. **切换惩罚等价**: 替代边带来的恢复 ≈ 切换/setup 延迟造成的损失
3. **替代边质量**: 24×20 规模下跨轨候选仅 3 个/星，替代边质量不足以净正收益

## 已完成代码变更

```
simulator/config.py              — FAILURE_PROB/DURATION 参数
simulator/environment.py         — _inject_failures() + _failed_edges + edge_dim=8
simulator/model_gat.py           — edge_dim=8 + load_backbone_with_padding()
simulator/train_ppo_discrete.py  — failure/warm_start 参数
baselines/grid_fixed.py          — failure 支持
eval_dynamic.py                  — 动态场景评估(Grid vs PhaseA vs PhaseB)
```

## 三个待选方向

### A. 更激进失效 + 启发式替代
- p=0.10-0.20 → grid 损失 25-40%
- 不用 RL，改启发式: 失效时选最近替代，恢复时切回
- 风险: 不够"智能"，论文贡献可能不够

### B. 换叙事: 鲁棒性分析
- 不追求"超越 grid"，改为系统性鲁棒性分析
- 失效概率 sweep (p=0.01-0.30): grid vs GNN vs 启发式的完整曲线
- 贡献: "首次系统评估学习型 ISL 拓扑的动态鲁棒性"

### C. 转向全规模 24×66
- 跨轨候选 3→8 个/星，grid 可能不再最优
- D022 已预估: 1584 星, ~65K 候选边, env.step~0.6s
- 风险: 计算成本 12x，需候选边预筛选

## 决策索引
- D034: 静态→动态场景决策
- D035: 边失效机制实现
- D036: edge_dim 7→8 + 权重 padding
- D037: Phase B 训练无效，待方向决策

## 新对话应读的文件
1. 本 handoff
2. `projects/leo-isl-scheduling-drl/decision_log.md` D034-D037
3. `eval_dynamic.py` — 动态评估脚本
4. `simulator/environment.py` — 失效机制
5. `simulator/model_gat.py` — edge_dim=8 + padding 函数
6. `simulator/train_ppo_discrete.py` — Phase B 训练(含失效参数)
