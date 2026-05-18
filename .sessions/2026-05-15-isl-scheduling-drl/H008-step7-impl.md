# Handoff 2026-05-15 (Round 8)

## 当前进度
- 阶段：GW Step 7 §impl Part A 完成
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：
  - 仿真器 8 模块实现：`projects/leo-isl-scheduling-drl/simulator/`
  - 验证脚本：`projects/leo-isl-scheduling-drl/verify/verify_simulator.py`
  - 验证结果：解析/统计/退化/自相关 全部通过
  - MDP 试运行（Part A-checkpoint）：通过

## 关键结论

### 仿真器架构
| 模块 | 文件 | 行为 |
|------|------|------|
| M1 OrbitPropagator | orbit.py | Keplerian 两体传播（SGP4 sgp4init error=6，暂用两体） |
| M2 VisibilityConnectivity | visibility.py | 距离+LoS+FOR → 候选边 |
| M3 ChannelModel | channel.py | Gaussian beam + Rayleigh jitter → 容量+中断概率 |
| M4 TrafficGenerator | traffic.py | GHS-POP 100 GS → 重力模型流量需求 |
| M5 ISLEnvironment | environment.py | MDP 环境（gym-like API） |
| M6 Router | router.py | Dijkstra + 比例拥塞分配 |
| M7 RewardCalculator | reward.py | w1·R_tput - w2·C_switch - w3·C_setup（cap [0,1]） |
| M8 MetricsCollector | metrics.py | M1-M5 per episode |

### 验证结果摘要
- **解析验证**：轨道周期 5730s ✓，高度 550km ✓，FSPL 258.18dB ✓，容量单调递减 ✓
- **信道**：所有链路可用（P_out < 10⁻³），1000km 容量 ~12.6 Gbps
- **退化测试**：固定轨道→同一拓扑，σ_J=0→纯理论值（差异<0.01%）✓
- **自相关**：lag-1 ρ = 0.82 < 0.95 ✓
- **MDP 试运行（24×8=192 sats）**：贪心 vs 随机差距 76.4% ✓，无单项 >95% ✓

### 已知限制
1. **轨道传播**：使用 Keplerian 两体而非 SGP4（sgp4init 初始化失败，error=6）。对 ISL 调度问题影响可忽略
2. **小星座验证**：4×8=32 sats 无跨轨 ISL（跨轨间距 ~9788km > z_max=3000km），仅同轨链路。24 面星座有正常跨轨连接
3. **可见性计算**：Python 循环 O(n²)，1584 sats 约 1.25M 对需优化（可用 numpy 向量化或 KD-tree）

### 奖励函数验证
- C_switch 和 C_setup 已 cap 在 [0,1]
- 10 步 episode 初期奖励为负（setup 成本主导），稳定后转正
- 设计范围 [-0.5, 1.0] 每步

## 下一步
1. **Step 7 §impl Part B**：Baseline 复现
   - B1: +Grid/Fixed (~50 行，固定拓扑 + Dijkstra 路由)
   - B2: Wang TCOM MADRL (2-3 周，Double Dueling DQN + CS 压缩)
2. **可见性优化**：向量化或 KD-tree 加速候选边计算（为全规模 1584 sats 做准备）
3. **SGP4 修复**（可选）：尝试 TLE 字符串 + twoline2rv 替代 sgp4init

## 文件路径
- 仿真器代码：`projects/leo-isl-scheduling-drl/simulator/`（9 文件）
- 验证脚本：`projects/leo-isl-scheduling-drl/verify/verify_simulator.py`
- 仿真器设计规格：`projects/leo-isl-scheduling-drl/simulator_spec.md`
- 可行性报告：`projects/leo-isl-scheduling-drl/feasibility_report.md`
- 决策日志：`projects/leo-isl-scheduling-drl/decision_log.md`
