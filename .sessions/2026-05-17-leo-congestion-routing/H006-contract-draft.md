# Handoff 2026-05-17

## 当前进度
- 阶段：Contract Step 3 完成 → Step 4
- 状态：进行中
- Contract 状态：draft（Step 0-3 通过，Step 4-6 待完成）
- 本轮完成：Contract Step 0 新颖性确认 + Step 1 假设形成 + Step 2 草案 + Step 3 参数溯源

## 本轮产出

1. **contract.md** (draft): 完整 Contract 草案，含假设/信号/baseline/metrics/fairness/ablation/12实验/sim config/数据集设计/参数溯源
2. **decision_log.md**: 新增 D11-D13（Step 0/1/2/3 决策记录）
3. **master-state.md**: 阶段更新为 Contract，进度表新增 Step 0-3 行
4. 所有 [ASSUMPTION] 已消除（ISL 容量 → 设计选择, 区域故障 → 设计选择）

## Contract 关键数字

- **假设**: GNN vs ECMP ≥10%, GNN vs MLP ≥15%, 泛化退化 <10%
- **Success**: 三维全满足（核心优势 + 结构优势 + 泛化）
- **Failure**: 任一维满足（无实用价值 / 无结构优势 / 泛化失败）
- **Baseline**: SP/ECMP/MLP(已复现) + DTAR(待适配) + GMR-simplified(待自实现,P4风险)
- **实验**: 4 核心(E01/E04-06) + 3 对比(E02-03/E07) + 5 消融/鲁棒(E08-12)

## 下一步

1. **读 `stages/contract.md`**（重读 Step 4 端到端推演部分）
2. **读 `templates.md`**（data-flow 模板）
3. **执行 Step 4**: 纸笔推演 8 步数据流（星座→拓扑→流量→状态→模型输入→输出→奖励→评估），产出 `data-flow.md`
4. **执行 Step 5**: 5 问压力测试 + 反模式排查（基于 data-flow.md）
5. **执行 Step 6**: 冻结 Contract + 用户确认

## 项目文件索引

| 文件 | 说明 |
|------|------|
| `projects/leo-congestion-routing/contract.md` | Contract 草案 (draft) |
| `projects/leo-congestion-routing/master-state.md` | Master 编排状态 |
| `projects/leo-congestion-routing/simulator-design.md` | 仿真器设计规格（Step 4 推演的基础） |
| `projects/leo-congestion-routing/decision_log.md` | 决策日志 |
| `projects/leo-congestion-routing/literature_notes.md` | 文献笔记（17 篇精读） |
| `projects/leo-congestion-routing/feasibility_report.md` | 可行性报告 |
| `projects/leo-congestion-routing/simulator/` | 仿真器代码（8 模块） |
