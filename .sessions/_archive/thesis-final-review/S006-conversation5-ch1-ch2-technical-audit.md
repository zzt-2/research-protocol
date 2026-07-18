# S005: Ch1+Ch2 参数/公式/指标技术审查

> 2026-05-25 | Phase 2.5 | 完成

## 目标

验证 Ch1 和 Ch2 的仿真参数、公式推导、指标计算、训练配置在领域内是否合理且内部一致。

## 子 agent 执行摘要

5 个子 agent 并行执行：5a(Ch2参数) + 5b(Ch2公式) + 5c(Ch1参数) + 5d(Ch1公式) + 5e(Ch2训练充分性)

## 发现汇总（按严重度排序）

### P0 严重（必须修正）

#### 1. Ch2 Retention 定义误导 [5b]

- **问题**: retention = 目标规模总 reward / 源规模总 reward × 100%。由于 total reward 是所有 UE 的求和，UE 数量增加时总 reward 自然增大
- **影响**: 报告 retention 218%/340%，但 per-UE 实际为 88%/71%
- **缓解**: 论文叙事已侧重 GNN vs MLP 稳定性（std 36.9% vs 102.3%），retention 是辅助指标
- **建议**: 修正为 per-UE retention，或在论文中明确定义并说明总 reward 比的含义（"规模弹性"而非"性能保持"）

#### 2. Ch1 Retention 公式/代码/报告三处不一致 [5d]

- `06_formulas_symbols.md`: retention = same_scale / cross_scale（方向未明确）
- `run_experiments.py`: full_delay / same_delay（方向相反，得 1.084）
- `03_experiments.md`: GRLR(60.32) / Ours(65.92) = 0.915（用不同基准）
- **建议**: 统一 retention 的方向和基准定义，修正代码使其与公式一致

### P1 高优先级（应修正）

#### 3. Ch2 eps-greedy 参数 paper vs code 不一致 [5b]

- paper_materials 写 ε: 1.0→0.01, decay=40
- 代码实际 ε: 0.5→0.05, tau=20
- **建议**: 更新参数表使两者一致

#### 4. Ch2 50 episodes 训练量在文献中属最低端 [5e]

- L029: 300 eps, L016: 5000 eps, L024: 1000-8000 eps
- 我们仅 50 eps，为 L029 的 1/6
- **缓解**: 每 episode 720 steps（2h 仿真），是多数文献的 3-10 倍；20 UE 已收敛（CV=0.3%）
- **实际风险**: 50 UE 同规模训练未收敛（CV=19.5%），但论文核心结论依赖 20 UE 训练
- **建议**: 论文中明确说明每 episode 的 steps 数量和总 transitions，避免只报告 episode 数

#### 5. Ch1 03_experiments.md 边特征误写 [5d]

- 写成 `[delay, utilization]`，代码实际是 `[delay, dist]`（几何距离）
- 不存在利用率特征
- **建议**: 修正为 `[delay, dist]`

#### 6. Ch1 train_66 连通性问题 [5c]

- 6 面配置轨间 ISL 赤道处 ~7278km > 5000km 阈值，大量断链
- 训练数据含不完整拓扑，但 100/200 星正常数据主导学习
- **建议**: 论文中声明或替换为更连通配置（如 8×10=80）

### P2 中优先级（建议修正）

#### 7. Ch2 size gen 100UE MLP 稳定性差 [5e]

- MLP CV=41.1%，seed 2 崩溃（blocking=45.5%）
- **可正面利用**: 强化"GNN 稳定性 2.8x"叙事

#### 8. Ch1 单一 eval seed [5c]

- 训练 3 seed 但评估仅用 seed=123
- 统计方差可能被低估
- **建议**: 改为多 eval seed 或在局限性中声明

#### 9. Ch1 06_formulas 注意力公式下标笔误 [5d]

- 分母 `[Wh_w||Wh_v]` 应为 `[Wh_u||Wh_w]`
- 不影响代码，PyG GATConv 实现正确

#### 10. Ch1 PE 引用建议调整 [5d]

- 频率公式 `f_i = 2^i · 2π` 是 NeRF 风格乘法递增，非 Vaswani 除法衰减
- **建议**: 弱化对 Vaswani 的直接归因

#### 11. Ch1 流量模型单一 [5c]

- 仅评估 uniform 流量
- **建议**: 在局限性章节声明

#### 12. Ch1 E2E delay 假设需显式声明 [5d]

- E2E delay = 纯 ISL 传播时延之和，不含排队延迟
- **建议**: 方法章节显式声明

### 误报（已排除）

#### × 环境文件冲突 [5a 原始报告]

- agent 5a 报告 c_gnn_ddqn.py 导入 environment.py（旧版）参数不同于 config.py
- **实际验证**: environment.py 通过 `cfg.NUM_PLANES` 等读取 config.py，参数完全一致
- env.py（新版，未使用）有硬编码默认值，但训练代码不导入 env.py
- **结论**: 无问题，排除

## 参数合理性总结

### Ch2 参数（代码实际值 vs 文献范围）

| 参数 | 实际值 | 文献范围 | 判定 |
|------|--------|---------|------|
| 星座规模 | 396(18×22) | 3~298 | 偏大但合理 |
| 轨道高度 | 550km | 500~1800 | OK |
| 频段 | Ku 12GHz | S/Ku/Ka | OK |
| 带宽 | 250MHz | 10.8~250 | OK |
| sat_capacity | 10 | 1~9(文献) | OK(偏大但配合396星合理) |
| UE 数量 | 15-20 | 10~200 | OK |
| 决策间隔 | 10s | 文献少明确 | OK |
| 仿真时长 | 7200s | 3600+ | OK |
| 传播模型 | FSPL+大气+Shadow(3GPP) | 多数仅 FSPL | 偏完善(正面) |

### Ch1 参数

| 参数 | 实际值 | 文献范围 | 判定 |
|------|--------|---------|------|
| 拓扑类型 | Walker-Delta F=1 | Walker-Delta/Starlink | PASS |
| 训练规模 | 66+100+200 | 50~1000 | PASS |
| 目标规模 | 720(72×22) | 400~6000 | PASS |
| ISL 模式 | +Grid 度=4 | +Grid/*Grid | PASS |
| 路由指标 | 传播时延(delay stretch) | delay/hop | PASS(需明确定义) |
| 流量模型 | uniform only | uniform/hotspot | WARN(单一) |
| 训练 epochs | 150 | 20~2000 | PASS |
| 评估种子 | 3 train × 1 eval | 3~5 seeds | WARN |

### Ch2 训练充分性

| 项 | 我们的值 | 判定 |
|-----|---------|------|
| 训练 episodes | 50 | 文献最低端，但每 ep steps 多 |
| 20 UE 收敛 | CV=0.3% | **充分** |
| 50 UE 收敛 | CV=19.5% | **不充分**（但非核心依赖） |
| Buffer 200K | 与 L029 持平 | **充分** |
| 3 seeds | 20UE CV=0.3%，size gen CV≤11% | **勉强** |

## 一致性审查（12 项无问题）

以下经审查完全一致：FSPL、Shannon 容量、R_norm 归一化、大气衰减、阴影衰落、Reward 公式权重、权重文献依据、Jain's Fairness、Throughput 计算、Dueling Q 公式、模型冻结、评估公平性。

## 决策引用

- 无新决策（本 round 为审查，发现记录待对话 8 执行）

## 范围确认

- 本轮是否在 scope boundary 内：是（Phase 2.5 技术审查）

## 后续

- **对话 6**: Ch3 参数/公式/指标审查 + 跨章公式一致性
- **对话 8**: 基于本 round 发现执行修复（P0 retention 定义修正、P1 参数表更新等）
- **P0 需优先处理**: Ch1 retention 三处不一致、Ch2 retention per-UE 修正
- **P1 在论文写作时修正**: eps-greedy 参数表、边特征、E2E delay 声明
