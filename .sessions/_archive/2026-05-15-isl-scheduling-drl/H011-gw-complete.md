# Handoff 2026-05-15 (Round 11) — GW 阶段完成

## 当前进度
- **阶段：Groundwork 全部完成**
- 状态：GW Step 1-7 全部完成，准备进入 Contract
- Contract 状态：未开始
- 本轮完成：性能优化（visibility 6.4x, traffic 63x, B1 episode 2.1x）

## GW 最终产出
| 文件 | 内容 |
|------|------|
| `literature_notes.md` | 12 篇精读 + 3 篇浅读，含步骤进度表 |
| `feasibility_report.md` | Go/No-Go 通过 |
| `decision_log.md` | D001-D011 |
| `simulator_spec.md` | 仿真器设计规格（28 参数，0 ASSUMPTION） |
| `simulator/` | 8 模块仿真器（orbit/visibility/channel/traffic/environment/router/reward/metrics/config） |
| `baselines/grid_fixed.py` | B1: +Grid/Fixed (~100 行) |
| `baselines/wang_madrl.py` | B2: Wang MADRL (~330 行, Double Dueling DQN) |
| `baseline_report.md` | B1+B2 复现报告 |
| `verify/verify_simulator.py` | Part A 验证（解析/统计/退化/自相关/MDP 试运行） |
| `verify/verify_baselines.py` | Part B 验证（B1 topology + episode + vs dynamic） |

## 关键数据

### 全规模性能 (24×66=1584)
| 方法 | M1 吞吐量 | M4 阻塞率 | M5 公平性 | 速度 |
|------|---------|---------|---------|------|
| B1 Fixed | 28.2% | 71.8% | 0.64 | 1.0s/step |
| B2 MADRL | 待全规模测试 | — | — | — |

### 测试规模性能 (24×20=480)
| 方法 | M1 吞吐量 | 说明 |
|------|---------|------|
| B1 Fixed | 17.3% | 4 固定 ISL |
| B2 Trained | 11.8% | 3 固定+1 动态，未优于 B1 |

### 待决策问题
1. **28% 吞吐量是否足够高**——72% 流量被阻塞，瓶颈是单路径 Dijkstra 路由而非 ISL 容量
2. **核心方法（2 动态 ISL）能否超过 B1（4+ 固定 ISL）**——B2 用 3+1 都没打过
3. **是否需要优化路由**——多路径路由可能显著提升吞吐量基线
4. **Contract 还是全规模测试优先**——Contract 锁定参数后更难回退

## 下一步选项
1. **进入 Contract 阶段** — 读 `stages/contract.md`
2. **全规模 B2 训练** — 1584 星更多候选，验证 DRL 在全规模是否有效
3. **实现核心 GNN-DRL** — 直接写核心方法
4. **回溯** — 如果方向判断有误，考虑调整

## 恢复优先级
1. 此 HANDOFF 文件
2. `baseline_report.md`（B1+B2 结果）
3. `decision_log.md`（D001-D011）
4. `stages/contract.md`（如进入 Contract）
