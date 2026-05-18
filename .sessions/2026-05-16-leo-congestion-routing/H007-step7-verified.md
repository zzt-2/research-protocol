# Handoff 2026-05-17

## 当前进度
- 阶段：Groundwork Step 7 完成 → Contract
- 状态：完成
- Contract 状态：未开始
- 本轮完成：bug 修复 + 验证套件 28/28 全通过 + 三个 baseline 运行验证

## 本轮修复

1. **model.py**: Normal 采样负权重 → Dijkstra 崩溃。修复：采样后 `torch.clamp(action, min=1e-6)`
2. **failures.py**: `failure_rate=0` 时 `_inject_random` 的 `max(1, ...)` 仍注入故障。修复：`inject()` 入口检查 `failure_rate <= 0` 提前返回
3. **config.py**: `assert 0 < failure_rate` 不允许 0。修复：`assert 0 <= failure_rate`

## 验证结果 (28/28 PASS)

| 类别 | 项数 | 关键结果 |
|------|------|----------|
| 1. 解析 | 4/4 | MLU finite, mini-topology OK |
| 2. 统计 | 4/4 | Heavy median > Light median, 故障率 ≈8% |
| 3. 退化 | 4/4 | 同 seed 确定性, 不同 seed 差异, failure_rate=0 无故障 |
| 4. 自相关 | 10/10 | Traffic/MLU lag-1 ρ 全部 < 0.95 |
| 5. MDP Trial | 3/3 | SP(-47.97) > Random(-53.66), 策略有区分度 |
| 6. Baseline | 3/3 | SP MLU=2.09, ECMP MLU=1.76 |
| 7. Reward balance | 4/4 | SP > Random, 方差充足, 跨 episode 有变化 |

## Baseline 运行结果 (20 episodes)

| Baseline | MLU mean | MLU std |
|----------|----------|---------|
| SP | 1.88 | 0.71 |
| ECMP | 2.07 | 0.81 |
| MLP (50ep) | 1.77 | 0.54 |

观察：ECMP > SP（非均匀流量+故障下分流反增拥塞，符合预期）。MLP 快速训练已优于 SP。

## Import 方案

项目目录名含连字符，需 symlink 才能作为 Python 包导入：
```bash
# 已创建（勿删）：
# projects/__init__.py
# projects/leo-congestion-routing/__init__.py
# projects/leo_congestion_routing -> leo-congestion-routing
```

## 项目文件索引

| 文件 | 说明 |
|------|------|
| `projects/leo-congestion-routing/master-state.md` | Master 编排状态 |
| `projects/leo-congestion-routing/simulator/` | 仿真器 8 模块 |
| `projects/leo-congestion-routing/verify/verify_simulator.py` | 7 类验证套件 |
| `projects/leo-congestion-routing/baselines/` | SP/ECMP/MLP 三个 baseline |
| `projects/leo-congestion-routing/simulator-design.md` | 仿真器设计规格 |

## 下一步

1. **读 `stages/contract.md`**（Contract 阶段操作规范）
2. **冻结 Contract**: 确认研究方案、实验计划、时间预算
3. **DTAR 竞品复现**: 适配 https://github.com/ChenZ-code/DTAR_Routing 到本仿真器
4. **GMR 简化版复现**: MPNN+DDPG 去PER K=2（P4 级，可退守 DTAR 单一竞品）
5. **正式训练**: GNN(PPO) vs SP/ECMP/MLP/DTAR，3 seeds，500 episodes
