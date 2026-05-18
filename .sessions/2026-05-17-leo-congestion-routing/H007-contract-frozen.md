# Handoff 2026-05-17

## 当前进度
- 阶段：Contract 冻结完成 → Execute 待启动
- 状态：Ready for Execute
- Contract 状态：**frozen**（用户已确认）
- 本轮完成：GW Step 7 baseline 复现 + Contract Step 0-6

## 本轮产出文件

### Baseline 复现
- `baselines/sp.py` — 修复为均值 MLU 评估
- `baselines/ecmp.py` — 重写：迭代 t_slots + 均值 MLU
- `baselines/mlp.py` — 修复为均值 MLU 评估
- `baseline_report.md` — ECMP(1.97) > SP(2.37) > MLP(2.52)

### Contract 阶段
- `contract.md` — frozen，含假设/baseline/实验/参数溯源
- `data-flow.md` — 端到端推演，8 步全通过，1 已知限制
- `decision_log.md` — D11(MDP checkpoint), D12(端到端), D13(压力测试)

## 关键结论

### Baseline 排序
| 方法 | Mean MLU | 说明 |
|------|----------|------|
| ECMP | 1.9664 | 最优，分流有效 |
| SP | 2.3674 | 标准 hop-count 最短路径 |
| MLP | 2.5249 | 300 eps 训练，不如 SP → 证明 message passing 必要 |

### MDP Checkpoint (D11)
- 贪心 vs 随机仅 +3.8%（未达 10% 门限）
- 原因：Walker delta 规则拓扑下负载感知绕路反效果
- 不阻断：MVE 已证 GNN > ECMP 12%（D4），DRL 价值在全局优化

### 踩坑复查
- code-quality.md 系统性坑（C1 奖励失衡、A1 top-K、A5 信息冗余）均不适用
- 唯一注意项：reward balance gate 1.5× 标准，待 GNN 训练后验证

## Execute 阶段入口

### 恢复读取顺序
1. `master-state.md` — 全局状态
2. `contract.md` — frozen 假设/实验/参数
3. `data-flow.md` — 仿真器设计参考
4. `stages/execute.md` — Execute 阶段框架

### 首要任务
1. 读 `stages/execute.md` 框架文件
2. 读 `code-quality.md` + `reference/sim-template/` 必做清单
3. GNN 训练实现（对齐 data-flow.md 和 contract.md 架构规格）
4. 实验 E01 核心对比（GNN vs B1-B5, 66 节点, 8% 故障, 3 seeds × 500 eps）

### Execute 注意事项
- log_std 固定 264 维 → 泛化必须 deterministic=True
- PPO buffer 在 720 节点下需检查容量（C5 教训）
- DTAR/GMR baseline 待 Execute 阶段补充（非阻塞）
- GMR-simplified 为 P4 风险，退守策略为放弃

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md`
- `projects/leo-congestion-routing/contract.md` (frozen)
- `projects/leo-congestion-routing/data-flow.md`
- `projects/leo-congestion-routing/baseline_report.md`
- `projects/leo-congestion-routing/simulator/` (8 模块)
- `projects/leo-congestion-routing/baselines/` (SP+ECMP+MLP)
- `projects/leo-congestion-routing/decision_log.md`
- `projects/leo-congestion-routing/feasibility_report.md`
- `projects/leo-congestion-routing/literature_notes.md`
