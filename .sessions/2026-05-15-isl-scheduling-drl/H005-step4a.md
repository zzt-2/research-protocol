# Handoff 2026-05-15 (Round 5)

## 当前进度
- 阶段：GW Step 4b 完成，待 Step 6（仿真器设计规格）
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：
  - Step 4a：feasibility_report.md 撰写 + MVE 执行（Pass，GNN 97.3% vs FC 79.5%）
  - Step 5：Baseline 选定 B1=+Grid/Fixed, B2=Wang TCOM MADRL (L09)
  - Step 4b：仿真条件(C)+资源风险(E)评估完成，Go 决策
  - 文件：`feasibility_report.md`（A-E 五维度完整）、`decision_log.md`（D001-D005）

## 关键结论

### Baseline 选定
- B1: +Grid/Fixed LISLs — 领域共识（5/15 篇），自实现，1 天
- B2: Wang TCOM MADRL (L09) — 最直接 DRL 竞品，无代码需复现，2-3 周
  - Double Dueling DQN 810→512→256→8，CS 压缩，奖励分解
  - OneWeb 720 星，"3固定+1动态"模式

### 可行性报告关键数据
| 维度 | 结论 |
|------|------|
| A. 结构优势 | L02 直接验证 GNN > FC RL；MVE +22.4% |
| B. 新颖性 | 15 篇确认空白，技术基础 2025 年成熟 |
| D. MVE | Pass (GNN 0.9733 vs FC 0.7954) |
| C. 仿真条件 | 无"过于平滑"风险，动态拓扑+非均匀流量 |
| E. 资源风险 | B2 复现主风险，失败兜底充分 |

### 仿真器设计需注意
- 统一用 Starlink 参数（B2 原为 OneWeb，需适配）
- 信道模型：Gaussian beam + Rayleigh 指向抖动（L02 级保真度）
- 流量：GHS-POP 非均匀分布
- Setup delay 建模嵌入 reward

## 下一步
1. **Step 6**（`stages/gw-experiment.md` §sim）：仿真器设计规格
   - 需读框架文件：`stages/gw-experiment.md`
   - 需读参考：`templates.md` 的 data-flow 模板
   - 核心产出：仿真器设计规格（数据流 + 参数溯源）
2. **Step 7**（`stages/gw-experiment.md` §impl）：Baseline 复现 + 仿真器验证
