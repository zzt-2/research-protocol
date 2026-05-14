# Handoff 2026-05-13 (Execute Step 1-2 进行中)

## 当前进度
- **阶段：Execute Step 2（核心实验 — quick test 完成，待 RL 训练）**
- 状态：仿真器 + 监督 quick test 完成，准备实现 RL
- 本轮完成：
  - Step 1 实验设计审查通过
  - 参数核实（3 子 agent 并行）+ 3 个参数修正（D015-D017）
  - 仿真器 9 个模块完成（constellation/topology/channel/traffic/routing/snapshot/models/smoke_test/quick_test）
  - Smoke test 通过
  - Quick test 监督训练验证：**3 层 GAT h=128 PE=16 → 保留率 70.2%**

## 关键上下文

### 参数修正（已写入 decision_log D015-D017）
- ISL 容量：B=500MHz → **B=1 GHz**（来源 L03 DuJo）
- ISL 距离：固定值 → **实时轨道力学计算 + 5000km 断链逻辑**（来源 L02 Starfield）
- ISL 类型确认为激光，Shannon 模型标注为简化近似

### 仿真器架构（`simulator/` 目录）
- `config.py` — 全局参数配置
- `constellation.py` — Walker-Delta 星座位置计算（ECI 坐标）
- `topology.py` — +Grid ISL 拓扑 + 断链过滤
- `channel.py` — Shannon 容量模型 + 传播时延
- `traffic.py` — 三种流量模型（uniform/hotspot/distance）
- `routing.py` — Dijkstra 全源最短路径
- `snapshot.py` — 组合为 PyG 图 + 预计算 PE + 方向 mask
- `models.py` — GAT 路由模型（预计算 33 维输入）
- `smoke_test.py` — 物理模型验证（已通过）
- `quick_test.py` — 规模泛化测试（进行中）

### Smoke test 关键结果
| 配置 | N | ISL 断链 | Dijkstra 平均时延 |
|------|---|---------|-----------------|
| 66 (6×11) | 66 | 34.8% | 65.9ms |
| 100 (10×10) | 100 | 0% | 62.2ms |
| 200 (10×20) | 200 | 0% | 59.7ms |
| 720 (18×40) | 720 | 0% | 61.0ms |
| 1584 (72×22) | 1584 | 0% | 63.8ms |

### Quick test v1 结果（3 层 GAT, h=128, 200 epochs 正在跑）
v2（2 层, h=64, 80 epochs）结果：
- 训练精度：89.2%
- 目标精度：53.1%
- 保留率：62.5%（目标 ≥80%）
- stretch（成功路径）：1.033
- 路径成功率：0.7%（瓶颈）

### 需要注意的坑
- 66 星配置 34.8% ISL 断链，拓扑不完整但连通
- 方向 mask 必须双向设置（u→v 和 v→u 的方向不同）
- 混合 batch 中不同配置的 P/S 不同，PE 必须预计算不能动态算
- 路径追踪需要每跳都正确，单跳精度需要 95%+ 才有合理成功率

## 下一步
1. **实现 RL 环境**（`env.py`）：封装仿真器为 PPO 兼容接口，状态/动作/奖励
2. **实现 PPO 训练**（`train.py`）：多尺度混合训练 + Actor-Critic
3. **Quick RL test**：小规模验证 RL 训练能跑通，对比监督 baseline
4. 如果 RL 保留率仍 <80%，尝试：4 层 GAT / h=256 / 更多训练数据
5. 实现 GRLR baseline 复现（需先读论文全文提取架构细节）
6. 跑完整实验 E01-E09

## 文件索引
- 仿真器：`projects/leo-mega-constellation-gnn-routing/simulator/`（9 个 .py 文件）
- Decision log：`projects/leo-mega-constellation-gnn-routing/decision_log.md`（D001-D017）
- Contract（frozen）：`projects/leo-mega-constellation-gnn-routing/contract.md`
