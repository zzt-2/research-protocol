# Handoff: Ch3 拓扑升级完成 → GPU 重跑实验

> 来源: S001 | 交接目标: 在新对话中重跑 Ch3 全部实验(E01-E12) + 更新 paper-materials
> 文件名: H001-topology-upgrade.md

## 已完成边界

### 本对话完成的工作

1. **Ch3 拓扑升级（完整物理仿真）**：
   - 新建 `simulator/constellation.py`：WalkerDelta 轨道力学类（移植自 Ch1）
   - 重写 `simulator/config.py`：inc=86.4°, alt=550km, SIZE_CONFIGS 映射, node_feat_dim=7
   - 重写 `simulator/topology.py`：物理仿真 + 纬度阈值极地间隙(|lat|>70° 断 inter-plane ISL)
   - 修改 `simulator/env.py`：7D 节点特征(+degree_norm), 动态 MLP padding
   - 修改 `simulator/model.py`：node_dim=7

2. **前序对话完成的工作**（继承自压缩前）：
   - Ch1 A1-A7 代码改造 + 端到端验证 ✅
   - Ch2 M4 Jain 修复（6 个 evaluate 函数）✅
   - Ch3 审计小改动（E03/E10/E12/CV+Overflow/config 清理）✅ — **但这些数据基于旧拓扑，重跑后会自动失效**
   - 三章 paper-materials 数字修正 ✅ — **Ch3 部分将随重跑更新**
   - git tag `ch3-pre-topology-upgrade` 归档旧代码 ✅

### 关键设计决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 轨道参数 | alt=550km, inc=86.4°, F=1 | 86.4° 极地轨道使极地间隙在所有尺度生效；53° 倾角无法产生极地间隙（288/720 节点面内距离太近） |
| 极地间隙机制 | 纬度阈值(|lat|>70°) | 非距离阈值。P 多时面内距离太小，5000km 阈值对 288/720 无效；纬度阈值在所有尺度一致生效 |
| P×S 映射 | 48=4×12, 66=6×11, 288=12×24, 720=18×40 | 66 和 720 匹配 Ch1 配置；48 和 288 为合理 Walker-Delta 参数 |
| 节点特征 | 7D（+degree_norm） | 变度图中度数是关键结构信息（极地 deg=2 vs 赤道 deg=4） |
| 高度 | 550km（与 Ch1 一致） | 跨章一致性；高度对纬度阈值机制无影响 |

### 验证结果

4 个尺度全部通过端到端测试：

| 规模 | 连通 | 度数分布 | 边数(dir) | 距离范围(km) |
|------|------|---------|----------|-------------|
| 48 (4×12) | ✓ | deg2=12, deg3=4, deg4=32 | 164 | 3583-9828 |
| 66 (6×11) | ✓ | deg2=17, deg3=4, deg4=45 | 226 | 3321-7306 |
| 288 (12×24) | ✓ | deg2=62, deg3=8, deg4=218 | 1020 | 1313-3808 |
| 720 (18×40) | ✓ | deg2=158, deg3=8, deg4=554 | 2556 | 857-2542 |

额外验证：完整 episode(40步) ✅, 训练循环(5ep) ✅, ECMP baseline ✅, 零样本 66→720 ✅

## 不要做什么

1. **不要使用旧拓扑数据**：旧结果基于 4-regular 抽象网格（distance_km=1.0），与新拓扑不可比。旧数据已归档在 git tag `ch3-pre-topology-upgrade`
2. **不要混用新旧实验结果**：MLU、ratio、CV 等指标含义不同（不同图结构）
3. **不要改 inc=53°**：53° 倾角在 288/720 节点时无极地间隙（已验证）
4. **不要用距离阈值替代纬度阈值**：距离阈值在大 P 时失效（已验证 288/720 全部 < 5000km）
5. **不要漏测小规模**：48 节点拓扑高度稀疏（deg2 比例 25%），需确认训练稳定

## 必读

按优先级排序：

1. `.sessions/thesis-chapter-fixes/topic-index.md` — 专题全局状态
2. `projects/leo-congestion-routing/simulator/config.py` — 新配置参数
3. `projects/leo-congestion-routing/simulator/topology.py` — 新拓扑生成逻辑
4. `projects/leo-congestion-routing/simulator/env.py` — 7D 节点特征
5. `.sessions/chapter-quality-audit/S004-ch3-audit.md` — 审计报告（实验定义 E01-E12）
6. `projects/leo-congestion-routing/paper-materials.md` — 当前论文材料（数字待更新）
7. `projects/leo-congestion-routing/master-state.md` — 项目状态

## 接口变更

```yaml
# config.py 新增/修改参数
altitude_km: 550.0  # 780.0 → 550.0
inclination_deg: 86.4  # placeholder → 实际使用
walker_delta_F: 1  # 新增
polar_gap_lat: 70.0  # 重新启用（纬度阈值）
node_feat_dim: 7  # 6 → 7
max_degree: 4  # 新增

# SIZE_CONFIGS 新增
SIZE_CONFIGS:
  48: (4, 12)
  66: (6, 11)
  288: (12, 24)
  720: (18, 40)

# topology.py TopologyData 新增字段
degree: np.ndarray  # (N,) 每节点无向度数
lats: np.ndarray  # (N,) 纬度(度)

# env.py 观测空间变更
node_feat: (N, 7)  # 第7列 = degree_norm = degree / 4.0
mlp_feat: (27,)  # 7*2 + 4*2 + 1 + 4 = 27 (was 25)

# model.py
RoutingActorCritic.node_dim: 7  # 6 → 7

# constellation.py (新建)
WalkerDelta: 轨道力学类, positions(t), latitudes(t), plane_sat_index(), flat_index()
```

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| paper-materials 仍引用旧拓扑数据 | 数据自洽性 | 旧数字待替换 | GPU 重跑后统一更新 |
| E12 多 seed 仅在旧拓扑验证过 | 统计严谨性 | 需新拓扑重跑 | GPU 重跑时包含 |
| DTAR baseline 未复现 | 实验完备性 | 审计标记为 P2 | 可选，审稿人要求时做 |
| Ch1/Ch2 仍用旧配置 | 跨章一致性 | Ch1 inc=53° vs Ch3 inc=86.4° | 论文写作时声明差异 |

## 接收方验证

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 topology.py 在 66 节点产出 deg2=17, deg4=45
- [ ] 已确认 config.py SIZE_CONFIGS 包含 4 个规模
- [ ] 已确认 48 节点拓扑连通（`nx.is_connected`）
- [ ] 已检查 `_registry.yaml` 中 thesis-chapter-fixes 专题状态

## 下一轮

### 立即可做（无 GPU）
1. 阅读上述必读文件
2. 完成接收方验证
3. 检查 `run_seed.py`、`gen_training_curves.py`、`run_mlp_generalization.py` 等脚本是否兼容新拓扑
4. 准备实验运行脚本（批量 E01-E12）

### GPU 密集任务（需 ~10-15h RTX 4070）
按优先级排列：

| 优先级 | 实验 | 说明 | 预估 GPU |
|--------|------|------|---------|
| P0 | E01 主实验 (66 nodes, 3 seed) | 核心对比 GNN vs ECMP vs MLP | ~1h |
| P0 | E12 故障模式 (3模式×4率×3 seed) | 主贡献直接支撑 | ~1h |
| P0 | E08 故障率消融 (5率×3 seed) | 核心消融 | ~2h |
| P1 | E04-E06 跨规模泛化 (3规模×3 seed) | 辅助贡献 | ~3h |
| P1 | E09 流量消融 (4条件×3 seed) | 泛化声称 | ~2h |
| P2 | E02 无故障基线 (3 seed) | 对比基线 | ~1h |
| P2 | E03 突发鲁棒性 (3 seed) | 鲁棒性 | ~1h |
| P2 | E07 训练曲线 | 可视化 | 含在 E01 |
| P3 | E10 层数消融 (3 seed) | 超参 | ~1h |
| P3 | E11 头数消融 (3 seed) | 超参 | ~1h |

**建议执行顺序**：E01 → E12 → E08 → E04-E06 → E09 → E02/E03 → E10/E11

### GPU 任务完成后
1. 从 JSON 结果提取所有指标（MLU, ratio, CV, Overflow, degree 分布）
2. 更新 paper-materials.md 全部表格和叙事
3. 更新 master-state.md 状态

### 跨章并行 GPU（独立任务）
- Ch1 5-seed 重跑：~105h（与 Ch3 可并行）
- Ch2 补实验：~6h
