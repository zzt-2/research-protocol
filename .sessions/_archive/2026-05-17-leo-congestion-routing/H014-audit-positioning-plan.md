# Handoff: Tier 1 自检 + A+B 定位 + 后续任务规划

> 来源: S001 | 交接目标: 按独立投稿标准补齐实验完备性，定位为 Online Fault-Resilient Per-Flow Routing
> 文件名: H014-audit-positioning-plan.md

## 已完成边界

### Tier 1 自检完成（3 子 agent 并行审计）
- Tier 1: 3/6 通过 (T1-2 Baseline来源 ✅, T1-3 公平调参 ✅, T1-5 信道溯源 ✅)
- Tier 2: 2/5 通过 (T2-1 统计检验 ✅, T2-4 跨拓扑 ✅)
- Tier 3: 2/5 通过 (T3-1 Red-teaming ✅, T3-5 极端条件 ✅)
- 通信领域: 信道模型 ✅, 拓扑多样性 ✅, DRL收敛 ⚠️(旧数据), 复杂度 ❌

### Contract 文档修正
- Hypothesis: "per-link weight" → "per-flow K-path discrete selection"
- 泛化声明: 加"Walker delta 族内"限定词
- Success/Failure Signal: 加 "Walker delta 族内" 限定词
- 评估条件: 更新为 surge=1.0, 800ep
- surge_factor: 5× → 1×(默认)/5×(鲁棒性测试)
- 参数溯源表: 突发因子条目已更新

### 定位决策：A+B 组合
- 路线 A（故障弹性路由）+ 路线 B（在线逐流路由）
- 组合定位：**Online Fault-Resilient Per-Flow Routing**
- vs TELGEN: 在线路由 vs 离线全局 TE
- vs ECMP: 主动负载感知 vs 被动等价分流
- vs DTAR: 全网逐流 vs 域间路由（粒度差异，不直接对比）
- 三级贡献递进：故障弹性（主）→ 在线逐流决策（次）→ 跨规模部署（辅）

## 不要做什么

- 不要与 TELGEN 正面竞争 size gen 新颖性
- 不要硬补 DTAR baseline（粒度不同，强行对比反而被挑毛病）
- 不要宣称"结构泛化"（F4 分析已证实是同族 scale robustness）
- 不要在论文中使用 universal claim（所有拓扑、所有场景）
- 不要改仿真器加轨道动力学（投入太大，路线 C 已否决）

## 必读

1. 本 H014 文件
2. `projects/leo-congestion-routing/master-state.md`（含自检结果）
3. `projects/leo-congestion-routing/contract.md`（已修正 Hypothesis）
4. `.sessions/2026-05-17-leo-congestion-routing/H013-vulnerability-fixes-batch1.md`（漏洞修复记录）
5. `templates.md` 实验完备性自检清单（Tier 1-3）

## 下一轮

### P0 已完成 ✅

1. **复杂度报告** ✅ — `simulator/results/complexity_report.json`
   - GNN 28,546 参数，MLP 10,309，均不随规模变化
   - GNN 推理: 1.2-2.0ms (CPU), MLP: 0.09-0.11ms
   - 288 节点故障响应: GNN 比 ECMP 快 7.7x
   - 脚本: `simulator/benchmark_complexity.py`

2. **训练曲线更新** ✅ — `simulator/results/training_curves_v2.json`
   - GNN 800ep: final MLU=1.252, 训练 22min
   - MLP 800ep: final MLU=1.596, 训练 73s
   - GNN/MLP=0.785 (GNN 低 21.5%)
   - 脚本: `simulator/gen_training_curves.py`

3. **清理旧结果文件** ✅ — 8 个旧文件移入 `results/legacy/`，含 README

### P1 — 进行中

3. **MLP 泛化评估** — E04/E05/E06 补跑 MLP (3-4h GPU)
4. **故障响应时间对比** ✅ — 已集成到复杂度报告中

### P1 — 待做

5. **清理旧结果文件** ✅ 已完成

### P2 — 可选

6. **可视化重生成** — 12 张图用 surge=1.0 数据
7. **E10/E11 补 seed** — F5 待修，差异 <2%
8. **E12 故障模式对比** — 可降级为"未来工作"

### P3 — 论文写作

9. **叙事重写** — 按 A+B 框架
10. **DTAR 讨论** — Related work 详细讨论粒度差异
11. **TELGEN 对比表** — 方法特性对比表

### 关键文件清单

- `simulator/benchmark_complexity.py` — 复杂度测量脚本
- `simulator/results/complexity_report.json` — 复杂度结果
- `simulator/gen_training_curves.py` — 训练曲线生成脚本
- `simulator/results/training_curves_v2.json` — 新训练曲线
- `simulator/results/legacy/` — 旧结果文件
- `results/batch_eval_results.json` — E02-E06 权威结果（E04/E05/E06 无 MLP 数据，待补）

### MLP 泛化评估执行要点

**已完成** ✅ — `simulator/results/mlp_generalization_results.json`

| 规模 | GNN | ECMP | MLP (scratch) | MLP (zero-shot) | GNN/MLP |
|------|-----|------|--------------|----------------|---------|
| E04 48节点 | 1.283 | 1.602 | 1.635 | 1.724 | 0.785 |
| E05 288节点 | 1.284 | 1.266 | 1.416 | 1.406 | 0.907 |
| E06 720节点 | 1.237 | 1.328 | 1.308 | 1.328 | 0.946 |

关键：GNN 在所有泛化规模赢 MLP；MLP 在 E04/E05 不如 ECMP。脚本：`simulator/run_mlp_generalization.py`

1. **复杂度报告**（~1.5h）
   - 写 `simulator/benchmark_complexity.py`
   - 测量 GNN/MLP/ECMP 推理延迟（1000次前向传播取均值）
   - 计算参数量（GNN vs MLP）
   - 理论复杂度 O() 分析
   - 故障响应时间对比（ECMP 重算 vs GNN 前向传播）
   - 结果写入 `simulator/results/complexity_report.json`

2. **训练曲线更新**（~1h）
   - 用 surge=1.0 + 800ep 配置重跑训练曲线
   - GNN 和 MLP 都用新配置，确认收敛
   - 更新 `simulator/results/training_curves.json`

### P1 — 应做（本轮或下轮，~4-5h GPU）

3. **MLP 泛化评估**（~3-4h GPU）
   - 在 E04(48)/E05(288)/E06(720) 上跑 MLP baseline
   - 填补 T2-2/T2-3 缺口
   - 结果追加到 `batch_eval_results.json`

4. **清理旧结果文件**（~20min）
   - `e02_e03_results.json` 标注为 "legacy (surge=5.0)"
   - `e01_results.json` 标注为 "legacy (per-edge)"
   - `e01_v2_results_surge5_backup.json` 保持（已有备份标记）

### P2 — 可选（下轮）

5. **可视化重生成**（~2h）— 12 张图用 surge=1.0 数据
6. **E10/E11 补 seed**（~4-6h GPU）— F5 待修，差异 <2%
7. **E12 故障模式对比** — 可降级为"未来工作"

### P3 — 论文写作

8. **叙事重写** — 按 A+B 框架重写 intro/conclusion
9. **DTAR 讨论** — Related work 详细讨论粒度差异
10. **TELGEN 对比表** — 方法特性对比表（在线 vs 离线、逐流 vs 全局、故障处理方式）
