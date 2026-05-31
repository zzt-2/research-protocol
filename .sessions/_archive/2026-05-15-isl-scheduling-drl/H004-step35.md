# Handoff 2026-05-15 (Round 4)

## 当前进度
- 阶段：GW Step 4a 完成
- 状态：**Go 决策**（待用户确认）
- Contract 状态：未开始
- 本轮完成：
  - 撰写 `feasibility_report.md`（A/B/D 三个维度评估完成）
  - 执行 MVE：GNN vs FC 图匹配实验，结果 **Pass**（GNN 97.3% vs FC 79.5%，+22.4%）
  - 创建 `decision_log.md`
  - 文件：`projects/leo-isl-scheduling-drl/feasibility_report.md`

## 关键结论

### Step 4a 评估结果
- **A. 结构优势**：无致命信号。L02 直接验证 GNN > FC RL（20%~100% 吞吐量提升），MVE 进一步验证（+22.4%）
- **B. 新颖性-可行性**：无致命信号。15 篇文献确认空白，技术基础 2025 年才成熟（L02 DeepLaDu）
- **D. MVE**：**Pass**。GNN (GATv2) 在图匹配调度上达到最优的 97.3%，FC 仅 79.5%，GNN 仅 11 epoch 收敛
- **决策：Go**

### MVE 关键数据
| 指标 | GNN | FC |
|------|-----|-----|
| Test reward/optimal | 0.9733 | 0.7954 |
| 收敛 epoch | 11 | 56 |
| 判定 | Pass | — |

## 未决问题
- L14 (DMR) 和 L15 (GNN-MAPPO) 下载失败（付费墙），如 Step 5 Baseline 选定需要可补充精读

## 下一步
1. **用户确认 Go 决策**
2. **Step 4b**（`stages/gw-feasibility.md`）：仿真条件 + 资源风险验证（需在 Step 5 Baseline 选定后执行）
3. **Step 5**：Baseline 选定（B1: +Grid/Fixed 必选，B2: Wang TCOM MADRL 竞品，B4: DeepLaDu 技术基础）
4. 读取框架文件：`stages/groundwork.md` Step 5 部分
