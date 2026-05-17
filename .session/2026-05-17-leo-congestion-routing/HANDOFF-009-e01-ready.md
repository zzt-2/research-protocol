# Handoff 2026-05-17

## 当前进度
- 阶段：Execute Step 2
- 状态：K-path 迁移完成，Quick Test PASS，准备 E01 全量训练
- Contract 状态：amended（K-path 离散动作空间）
- 本轮完成：env/model/train/baselines/verify 全部重写为 K-path 范式 + Quick Test

## 关键上下文

### Quick Test 结果（100ep, 1 seed, GPU）
- **GNN MLU = 1.954 ± 0.638**
- ECMP MLU = 2.552 ± 0.849
- SP MLU = 2.586 ± 0.884
- **GNN/ECMP = 0.766（改善 23.4%，目标 ≤ 0.90 → PASS）**
- GNN/SP = 0.756
- 100ep 训练 163s (GPU), 估计 E01 全量 ≈ 2.5h

### K-path 架构（已实现并验证）
- Episode: 逐流顺序路由，40 步 (n_flows=40)
- 每步: 生成 K=4 候选路径 (nx.shortest_simple_paths)，模型评分选择最优
- 模型: GATEncoder(6→64, 2层GAT+LN+Res) + PathScoringHead(MLP 64→32→1) + ValueHead(src‖dst → FC 128→64→1)
- 奖励: -(MLU_after - MLU_before) 增量式
- 离散动作: Categorical(logits)，无 log_std（跨规模泛化无限制）

### 已修改文件
- `simulator/config.py`: 新增 k_paths=4
- `simulator/env.py`: 完全重写，K-path 逐流路由
- `simulator/model.py`: PathScoringHead 替代 EdgeWeightDecoder
- `simulator/train.py`: 离散 PPO (Categorical)
- `baselines/sp.py`: action=0 (最短路径)
- `baselines/ecmp.py`: round-robin 等成本路径
- `baselines/mlp.py`: local features + Categorical
- `verify/verify_simulator.py`: 28/28 PASS
- `data-flow.md`: §5-8 全部更新
- `contract.md`: amendment 注解 + Simulation Config 更新
- `decision_log.md`: D15(迁移决策) + D16(迁移执行)

## 下一步：E01 核心实验

### 执行命令
```bash
cd /mnt/d/code/study/research-protocol
~/.venvs/torch/bin/python -c "
import sys
sys.path.insert(0, 'projects/leo-congestion-routing')
from simulator.config import SimConfig
from simulator.train import main

# E01: 3 seeds × 500 episodes × 50 eval
cfg = SimConfig(total_episodes=500, n_seeds=3, n_eval=50, device='cuda')
main()
"
```

### 时间预估
- 单 seed 500ep ≈ 800s (13min) 基于 100ep=163s
- 3 seeds ≈ 40min (串行)
- 加 eval ≈ 总计 45-50min

### E01 成功标准
- GNN/ECMP ≤ 0.90 (核心优势)
- GNN/MLP ≤ 0.85 (结构优势)
- Quick Test GNN/ECMP=0.766，余量很大

### E01 后续步骤
1. E01 PASS → E02-E03 (无故障/突发流量对比)
2. E04-E06 (泛化 48/288/720 节点)
3. E07-E11 (消融实验)

## 恢复读取顺序（新对话）
1. 本 HANDOFF 文件
2. `master-state.md`
3. `contract.md`（amendment 版本）
4. `data-flow.md`（K-path 版本）
5. `stages/execute.md`
