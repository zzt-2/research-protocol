# Handoff 2026-05-15 (Round 5 — Step 4b Go)

## 当前进度
- 阶段：GW Step 4b 完成，待 Step 6（仿真器设计规格）
- 状态：进行中
- Contract 状态：N/A
- 本轮完成：
  - Step 5 Baseline 选定：PPO+MLP(主选) + 图着色L04(次选) + Greedy/EPA(trivial)
  - 田野调查：35篇论文交叉验证，Greedy为绝对共识(8+篇)
  - Step 4b 仿真条件+资源风险验证：Go（C/E均无致命信号）
  - 产出：`feasibility_report.md`（C/E维度已填充）、`decision_log.md`（D004-D006）

## 关键上下文
- **4a Conditional Go + 4b Go = 整体 Go**
- **Conditional Go 条件**：实现时必须用PPO/SAC（不用REINFORCE）
- **仿真关键要求**：必须包含真实天线方向图（Bessel/UPA），避免"过于平滑"
- **全部baseline无开源代码**，均需自实现
- **Baseline 选择理由**：
  - PPO+MLP：核心消融，同算法不同编码器，直接证明GNN>MLP
  - 图着色L04：非ML基线，"传统图论vs学习化图方法"对比
  - Greedy/EPA：领域绝对共识下界

## 下一步
1. **Step 6：仿真器设计规格**（新对话执行）
   - 读 `stages/gw-experiment.md` §sim
   - 设计 BH 仿真环境：波束模型、干扰计算、天线方向图、需求生成
   - 参考参数来源：L01(19-61波束, Ku 11.45GHz)、L07(61波束, Ka 20GHz, Bessel方向图)、L03(Walker-Delta星座)
2. 文件路径：
   - 可行性报告: `projects/leo-beam-hopping-gnn/feasibility_report.md`（A-E维度完整）
   - 决策日志: `projects/leo-beam-hopping-gnn/decision_log.md`（D001-D006）
   - 文献笔记: `projects/leo-beam-hopping-gnn/literature_notes.md`
   - MVE脚本: `projects/leo-beam-hopping-gnn/verify/mve_gnn_vs_mlp.py`
