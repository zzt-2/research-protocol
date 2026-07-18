# Handoff: Ch3 训练不稳定排查与修复

> 来源: S008 | 交接目标: 排查 Ch3 PPO 训练崩溃原因，修复后重跑所有实验
> 文件名: H001-ch3-training-fix.md

## 已完成边界

对话 8 (S008) 完成了 Ch2+Ch3 终审。Ch1 和 Ch2 实验数据完备，可进入写作。Ch3 发现严重训练不稳定问题。

> ⚠️ **2026-05-26 更正**：以下数据来自 `results/` 目录，是 D013-D018 修复前的旧残留，被后续测试覆盖。D019 的有效训练结果在 `results_final/` 目录（4模型全部收敛，avg_best≈-11.7）。当前代码20ep诊断证实可正常训练（reward -1046→-13.11）。此 handoff 中的诊断步骤不再需要。

**具体数据**（从 `projects/hgat-satellite-dag-offloading/simulator/results/` 提取，**已确认过时**）：

| 模型 | seed42 | seed123 | seed456 | 诊断 |
|------|--------|---------|---------|------|
| HGAT | **159 eps** | **78 eps** | 3 eps (崩) | 偶尔能跑，不稳定 |
| GCN | 3 eps (崩) | 3 eps (崩) | 3 eps (崩) | **全部崩溃** |
| GraphSAGE | 3 eps (崩) | 3 eps (崩) | 3 eps (崩) | **全部崩溃** |
| MLP | 3 eps (崩) | 3 eps (崩) | 3 eps (崩) | **全部崩溃** |
| Random | 500 eps ✅ | 500 eps ✅ | 500 eps ✅ | 无训练，正常 |
| Greedy | 500 eps ✅ | 500 eps ✅ | 500 eps ✅ | 无训练，正常 |

**结论**：问题出在 PPO + GNN 编码器的训练流程。Random/Greedy 不涉及梯度训练所以正常。所有需要反向传播的模型都崩溃。

## 不要做什么

1. **不要一上来就改模型架构** — 先确认是不是训练流程/数值稳定性问题
2. **不要用 HGAT seed42 的 159eps 数据写论文** — 那是不稳定状态的幸存者偏差
3. **不要跳过诊断直接调超参** — 3 episodes 崩溃说明有根本性问题（NaN、梯度爆炸、reward 异常等）
4. **不要同时改多个变量** — 一次只改一个，确认效果

## 必读

按优先级排列：

1. **`simulator/run.py`** — 训练入口，理解训练循环逻辑
2. **`simulator/ppo.py`** — PPO 实现，重点检查 loss 计算和梯度裁剪
3. **`simulator/models_homo.py`** — homo 模型 (GCN/GraphSAGE/MLP)，检查前向传播
4. **`simulator/models_hgat.py`** — HGAT 模型，对比为什么偶尔能跑
5. **`simulator/env.py`** — 环境，检查 reward 计算和 step 逻辑
6. **`simulator/reward.py`** — reward 函数，检查是否有 NaN/Inf
7. **`simulator/config.py`** — 超参数配置
8. **对话 6 技术审查 (`.sessions/thesis-final-review/S005-ch3-technical-review.md`)** — 已知问题清单

## 接口变更

无代码改动。此 handoff 仅为诊断和修复交接。

## 快速诊断步骤（按顺序执行）

### Phase A: 5 分钟快速定位（不改代码）

```bash
cd /mnt/d/code/study/research-protocol
~/.venvs/torch/bin/python -c "
import json
# 查看 3-ep 崩溃的 reward 值
d = json.load(open('projects/hgat-satellite-dag-offloading/simulator/results/gcn_seed42.json'))
print('rewards:', d.get('episode_rewards', [])[:5])
print('n_episodes:', d.get('n_episodes'))
# 对比 HGAT seed42 能跑的
h = json.load(open('projects/hgat-satellite-dag-offloading/simulator/results/hgat_seed42.json'))
print('HGAT first 5 rewards:', h.get('episode_rewards', [])[:5])
print('HGAT last 5 rewards:', h.get('episode_rewards', [])[-5:])
"
```

### Phase B: 10 分钟诊断脚本

写一个小脚本跑 5 个 episode，打印每一步的：
- observation shape/range
- reward 值（是否 NaN/Inf）
- policy loss, value loss
- gradient norm
- action distribution (是否退化)

### Phase C: 根据诊断结果针对性修复

**可能的原因（按概率排序）**：

1. **Reward NaN/Inf** — DAG 任务生成有除零或空图 → 加防御性检查
2. **梯度爆炸** — PPO clip 不够紧或 value function 震荡 → 加 gradient clipping + value clipping
3. **Observation 异常** — 节点特征包含 NaN（channel 模型中距离=0 → FSPL=Inf）
4. **Action space 问题** — 动作维度与图大小不匹配导致 gather 错误
5. **学习率过高** — homo 模型用了 5e-5（已经降了 6x），但如果数值不稳定，需要更激进地降

### Phase D: 确认修复（单 seed 快跑）

修复后用 `seed=42` 跑 50 episodes 验证收敛，确认曲线平滑后再跑全量。

### Phase E: 全量重跑（修复确认后）

```bash
# 6 模型 × 3 seed × 500 eps，预计每 run 10-20 min
cd /mnt/d/code/study/research-protocol/projects/hgat-satellite-dag-offloading/simulator
~/.venvs/torch/bin/python run.py --model hgat --seed 42 --episodes 500
~/.venvs/torch/bin/python run.py --model hgat --seed 123 --episodes 500
# ... 依次
```

## 失败数据附录

| 模型 | seed | episodes | 前 3 reward |
|------|------|----------|------------|
| GCN | 42 | 3 | 需查看（可能 NaN） |
| GCN | 123 | 3 | 需查看 |
| GCN | 456 | 3 | 需查看 |
| GraphSAGE | 42 | 3 | 需查看 |
| MLP | 42 | 3 | 需查看 |
| HGAT | 42 | **159** | 正常收敛 |
| HGAT | 123 | **78** | 部分收敛 |
| HGAT | 456 | 3 | 崩溃 |

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| Ch3 多指标分拆 | 领域要求延迟+能耗 | 仅 reward | 训练修复后从 reward 解码 |
| Ch3 DAG 拓扑变体 | K1 做 6 种 | 仅 fat=0.6/density=0.4 | 主实验稳定后补 3 种 |
| Ch3 环境扫描 | K2 做 3 种 | 未做 | 主实验稳定后补 |
| Ch3 统计报告 | 3-seed mean±std | 数据不可信 | 重跑后自动满足 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 |
|--------|----------|---------|
| 训练稳定 | 6 模型 × 3 seed 全部 ≥ 200 eps | S005 P1-2 |
| 收敛曲线 | 后 100 eps CV < 10% | 通用标准 |
| HGAT vs Random | t-test p < 0.05 | 最低显著性 |
| HGAT vs Greedy | reward 显著优于 | 基本要求 |
| 不引入新 bug | 所有现有 PASS 测试仍然 PASS | 回归测试 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已读取 S005 (Ch3 技术审查) 的 P0/P1 问题
- [ ] 已读取 run.py 和 ppo.py 理解训练流程
- [ ] 已运行 Phase A 快速诊断确认 reward 值

## 下一轮

1. **Phase A**: 读取崩溃数据，确认是 NaN/Inf/梯度爆炸中的哪种
2. **Phase B**: 写诊断脚本，10 分钟内定位
3. **Phase C**: 针对性修复
4. **Phase D**: 单 seed 50eps 验证
5. **Phase E**: 全量 6×3×500eps 重跑
6. 修复后继续：多指标分拆 + DAG 变体 + 环境扫描 + 更新 paper_materials

## 环境

- Python: `~/.venvs/torch/bin/python`
- GPU: RTX 4070, CUDA
- 项目路径: `/mnt/d/code/study/research-protocol/projects/hgat-satellite-dag-offloading/`
- 模拟器路径: `simulator/`
