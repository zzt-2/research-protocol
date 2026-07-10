# PROMPT-001: GW Step 4a 可行性 Go/No-Go（双偏振 OSL 3 Q#）

> 粘贴此文档开新对话。交接自 H002（Step 3 精读完成）。

## 你要做什么

执行 GW Step 4a 可行性评估，对 3 个双偏振 OSL 研究问题（Q-DP1/2/3）逐个走 gw-feasibility 维度 A0→A'→A→B→D，产出 feasibility_report.md。

## 第一步（必须按顺序）

1. **session-governance 报到**：读 `.sessions/2026-07-10-dual-pol-osl-groundwork/topic-index.md`（不变量 8 条）+ `_registry.yaml`
2. **收 H002 handoff**：读 `.sessions/2026-07-10-dual-pol-osl-groundwork/H002-step3-done-step4a.md`，完成接收方验证清单（验证 3 条关键事实）
3. **读框架文件（FR-22 必须读）**：`stages/gw-feasibility.md`（§4a 维度 A0/A'/A/B/D 流程）
4. **读教训（FR-24）**：`thesis-lessons.md` TL-30（框架门控）/TL-32（Go/Kill标准分离）/TL-22（物理前提）/TL-27（量级核算）速查表

## 3 个要评估的 Q#

来源：`projects/thesis-fso/literature_notes.md` 双偏振 OSL 精读沉淀节"研究问题清单"。

- **Q-DP1**（动态 SOP 跟踪均衡器）：5 篇独立把 SOP 建模为静态旋转角→共识缝。M=动态SOP跟踪均衡器 C=双偏振星地湍流 A=现有CMA/MIMO假设准静态SOP
- **Q-DP2**（CMA fade 发散分析+鲁棒增强）：sat.1553 点名"CMA 在 scintillation fade 发散概率未被分析"。M=CMA fade发散分析 C=GG湍流深衰落 A=发散概率未被分析
- **Q-DP3**（湍流深衰落跨帧 DSP 恢复）：L-DP5 明确 open + L-DP6 DSP outage。M=跨帧恢复机制 C=帧间湍流衰落 A=深衰落跨帧挂起

**最强根方向**：信道建模层×假设错（9 篇共性准静态假设，SOP-湍流耦合未建模）。

## 纪律（和 Step 4a 直接相关）

1. **守 FR-22**：现在在 GW Step 4a，指得到具体 Step 才能开跑。Step 3+4a 是硬门控
2. **守 FR-25/TL-32**：Go 判据=赢传统未优化 baseline 几 dB；oracle 上界只做维度 D Kill 工具，**禁当 Go 判据**
3. **守 D018**：3 个 Q# 全评估完才排优先级，**不边评边 Kill**
4. **守 D009 checklist**：A1 方法归属（Q-DP1 落多孔径要验 Ju 团队是否占完）/A2 指标敏感/A3 增量≥同门~2-4dB
5. **守不变量1**：9 次 Kill 是物理事实——Q-DP1/2/3 是双偏振新空间，但要检查与单偏振 9 次 Kill 结论是否冲突
6. **主对话禁 WebSearch**；方向判断是用户过程决策不问导师（不变量7），只跟导师谈具体选定方向+论文结构
7. **子 agent 强制委托**：oracle 上界计算/MVE 在子 agent 做；单对话≤3 步

## 不要做什么

- 不跳 Step 4a 直接试方法（TL-30）
- 不用 oracle 上界当 Go 判据（TL-32）
- 不预设方向（3 个 Q# 全评完才排）
- 不碰载波同步 v2 的 35 Q#（单偏振搜索空间，独立评估不混）
- 不在评估阶段复活 9 次 Kill 当贡献（作思路素材可用，不变量1 守）

## 下一步动作

读完上述文件后，对 Q-DP1/2/3 逐个走：
- **A0**：四判据复核（精读时已初判，这里严格复核 + 空白零假设检查 A'）
- **A**：方法产出形态 + A1 归属（这方法谁首创的？被占完没？）+ A2/A3
- **B**：baseline 可得性（能下到对比算法吗？）
- **D**：oracle 上界前置门控（能解析算上界的先算，<0.5dB 直接 Kill 不跑 MVE）

产出 `projects/thesis-fso/feasibility_report.md`（双偏振子方向 A/B/D 维度）。
