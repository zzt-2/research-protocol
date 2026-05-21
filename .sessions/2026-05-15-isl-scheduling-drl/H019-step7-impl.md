# 新对话提示词：ISL Scheduling + DRL — Step 7 §impl 仿真器搭建

## 任务

为"LEO 星座 ISL 调度 + DRL"方向执行 GW Step 7 §impl Part A（仿真器搭建 + 验证），按 `simulator_spec.md` 实现仿真器各模块并通过验证清单。

## 状态恢复

按以下优先级读取：

1. 项目记忆：`~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_leo-isl-scheduling-drl.md`
2. 最新 handoff：`.sessions/2026-05-15-isl-scheduling-drl/HANDOFF-007-step6-sim.md`
3. **仿真器设计规格**：`projects/leo-isl-scheduling-drl/simulator_spec.md`（核心参考，对着写代码）
4. 文献证据：`projects/leo-isl-scheduling-drl/literature_notes.md`（信道模型参数）
5. 框架文件：`stages/gw-experiment.md`（§impl Part A 验证清单 + Part A-checkpoint）

## 待做事项

### 1. 读取框架文件

**[MUST]** 先读 `stages/gw-experiment.md` §impl Part A，理解搭建流程、验证清单和 MDP 试运行检查。

### 2. 实现仿真器模块

按 `simulator_spec.md` 模块清单 M1-M8，在 `projects/leo-isl-scheduling-drl/simulator/` 下实现：

**优先级排序（按依赖链）**：

1. **M1: OrbitPropagator** — SGP4 轨道传播，输入 TLE → 输出卫星位置时序
   - 依赖：sgp4 库，NumPy
   - 验证：两体轨道周期 ≈ 5790s（550km）

2. **M2: VisibilityConnectivity** — 距离+地球遮挡+FOR 角 → 候选边集
   - 依赖：M1 输出
   - 验证：赤道处跨轨距离 ~1410km，候选边数符合预期

3. **M3: ChannelModel** — Gaussian beam + Rayleigh jitter → 容量+中断概率
   - 依赖：M2 输出
   - 验证：FSPL 公式解析对比，容量随距离单调递减

4. **M4: TrafficGenerator** — GHS-POP 100 GS → 流量需求
   - 依赖：M1 输出
   - 验证：陆地流量 > 5× 海洋

5. **M6: Router** — Dijkstra + 比例分配
   - 依赖：M2 活跃拓扑
   - 验证：已知拓扑的最短路径

6. **M5: ISLEnvironment** — MDP 环境封装（gym.Env）
   - 依赖：M1-M4, M6
   - 状态构造：节点特征 6 维 + 边特征 7 维
   - 动作：边级 Bernoulli + LCT 约束后处理（top-2）
   - Setup delay 建模：Uniform(2, 30)s

7. **M7: RewardCalculator** — r = w₁·R_tput - w₂·C_switch - w₃·C_setup
   - 依赖：M5, M6

8. **M8: MetricsCollector** — M1-M5 评估指标

**技术栈**：

- Python: `~/.venvs/torch/bin/python`
- 依赖：`sgp4`, `numpy`, `scipy`, `torch`, `gymnasium`
- 安装：`pip install sgp4 gymnasium -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`

### 3. 执行验证清单

全部通过方可继续：

- [ ] **解析验证**：已知参数下输出与解析公式一致（FSPL, 轨道周期, beam 半径）
- [ ] **统计验证**：容量分布单调递减、流量分布陆地>海洋、可见性周期性
- [ ] **退化测试**：固定轨道→拓扑不变，固定流量→需求恒定，σ_J=0→纯理论值
- [ ] **自相关预警**：ISL 容量/流量/拓扑 lag-1 自相关 < 0.95

### 4. MDP 试运行（Part A-checkpoint）

验证通过后执行：

1. 跑 1 episode 随机策略 + 1 episode 贪心策略
2. 奖励分解表：各项绝对值占比
3. 硬性门槛：无单一项 >95%，贪心 vs 随机差距 >10%

### 5. 更新 handoff

完成后写 handoff 到 `.sessions/2026-05-15-isl-scheduling-drl/HANDOFF-008-step7-impl.md`。

## 关键参数（预加载，避免重读文献）

| 参数                                 | 值                                    | 来源       |
| ------------------------------------ | ------------------------------------- | ---------- |
| 星座                                 | 1584 星 (24×66), 550km, 53°           | L04        |
| LISL 范围 z_max                      | 3000km                                | L01 §III-A |
| FOR 角 θ                             | 60°                                   | L01 §III-A |
| 激光 λ                               | 1.55μm, W₀=9.87×10⁻³m, P₀=20W, B=1GHz | L01 §II-C  |
| 接收 A=0.01m², Ψ=0.5A/W, σ_N=3×10⁻⁷A | L01 §II-C                             |
| 指向抖动 σ_J=10μrad, 中断 ε=10⁻³     | L01 §II-B, L02                        |
| GS 数 100, GHS-POP                   | L01                                   |
| Setup delay Uniform(2, 30)s          | L04                                   |
| 决策间隔 τ=10s, Episode 50 步        | 设计选择                              |
| 奖励 w₁=1.0, w₂=0.3, w₃=0.2          | 用户已确认                            |

## 约束

- 工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && ...`
- 仿真代码放 `projects/leo-isl-scheduling-drl/simulator/`
- 验证脚本放 `projects/leo-isl-scheduling-drl/verify/`
- 子 agent 最多 3 个并发
- 单对话不超过 3 步
- 每个 Python 模块完成后立即验证该模块（不等全部完成）
