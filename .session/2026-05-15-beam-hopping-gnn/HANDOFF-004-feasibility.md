# Handoff 2026-05-15 (Round 4 — Step 5 Baseline 选定)

## 当前进度
- 阶段：GW Step 5 完成，待 Step 4b（仿真条件+资源风险验证）
- 状态：进行中
- Contract 状态：N/A
- 本轮完成：
  - Step 5 Baseline 交叉验证 + 选定
  - 田野调查：35篇论文（25篇有效），远超≥10篇门槛
  - Baseline 方案：PPO+MLP(主选) + 图着色L04(次选) + Greedy/EPA(trivial)
  - 产出：`decision_log.md` 新增 D004-D005

## 关键上下文
- **Baseline 选择**：
  - PPO+MLP：核心消融，同算法不同编码器，参考L08 MDP建模，无代码需自实现
  - 图着色L04：非ML基线，MCMF-TS-GC算法描述详细（WCL 2026），无代码需自实现
  - Greedy/EPA：trivial下界，自实现成本极低
  - QPLEX(L03)：暂不选，实现成本极高，revision可补
- **全部baseline均无开源代码**，均需自实现（优先级3：无代码有描述）

## 下一步
1. **Step 4b：仿真条件+资源风险验证**（新对话执行）
   - 读 `stages/gw-feasibility.md` §4b
   - 评估维度C（仿真条件）和E（资源/风险比例）
   - 关键验证：GNN训练稳定性（PPO+SAC替代REINFORCE）、仿真器可行性
2. 文件路径：
   - 决策日志: `projects/leo-beam-hopping-gnn/decision_log.md`
   - 可行性报告: `projects/leo-beam-hopping-gnn/feasibility_report.md`
   - 文献笔记: `projects/leo-beam-hopping-gnn/literature_notes.md`
   - MVE脚本: `projects/leo-beam-hopping-gnn/verify/mve_gnn_vs_mlp.py`
