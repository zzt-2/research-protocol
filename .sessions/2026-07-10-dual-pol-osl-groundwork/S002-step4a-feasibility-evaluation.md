# [S002] GW Step 4a 可行性 Go/No-Go（Q-DP1/2/3 双偏振子方向）

> 2026-07-10 | GW Step 4a | 状态：评估完成，交用户确认
> 续接 S001（Step 1-3 检索+精读完成）

## 目标

对 3 个双偏振 OSL 研究问题（Q-DP1/2/3）逐个走 gw-feasibility 维度 A0/A'/A/B/D，产出 feasibility_report.md，排优先级交用户。

## 记录

### 执行流程

1. **session-governance 报到**（Trigger 1）+ **收 H002 handoff**（Trigger 5）—— 3 条事实验证全 PASS（Q-DP1/2/3 四判据 / 5 篇 SOP 共识缝 / 9 篇精读笔记存在）
2. **读框架文件**：gw-feasibility.md（A0/A'/A/B/D 维度）+ glossary.md（四判据）+ thesis-lessons TL-30/32/27/22（框架门控/Go-Kill 分离/量级核算/物理前提）
3. **维度 A' 竞争维度分解**：偏振解复用正确性（先验覆盖高，Q-DP1）/ CMA 收敛鲁棒性（中，Q-DP2）/ 深衰落恢复（低，Q-DP3）
4. **委托 2 个子 agent 并行核查物理参数**（TL-27 量级核算 + FR-20 参数溯源）：
   - 子 agent 1：Q-DP1 SOP 变化速率（均衡器跟踪上限 300 krad/s vs 湍流致 SOP 速率）
   - 子 agent 2：Q-DP2/DP3 GG 深衰落统计（深度/持续时间/频率 + 帧时长对比）
5. **3 Q# 逐个评估**，写 feasibility_report.md 追加章节

### 3 Q# 评估结论

| Q# | 决策 | 关键判据 | 物理基础 |
|---|---|---|---|
| **Q-DP1**（动态 SOP 跟踪）| **No-Go（Kill）**| A0 §1 致命：均衡器 300 krad/s 高出湍流致 SOP 1-2 数量级，A 不成立 | 不足 |
| **Q-DP2**（CMA fade 发散）| **Conditional Go** | 空白真实（sat.1553 自认）+ 幅度→时间域升级；需自建 GG 时间模型 | 中 |
| **Q-DP3**（跨帧恢复）| **Conditional Go（首选）**| 跨帧+挂起+恢复 open 三点文献支撑；先验覆盖最低 | 最扎实 |

### Q-DP1 Kill 的核心逻辑（D001）

A0 §1 性能间隙分析（不是 oracle 上界 Kill，是 A0 本职）：问题"M 在 C 下因 A 失效"，但 M（均衡器 300 krad/s）在 C（湍流致 SOP，kHz-几十 krad/s）下根本不失效，A 是错的。4 篇精读论文无任何 SOP 速率接近 300 krad/s 的报告。sat.1553 作者自己都说"OSL SOP 旋转可能较慢，MMSE 可行"。

Pivot 出口：C 改为"机械振动致 SOP"（sat.1553 L563 暗示真实来源）A 可能成立，但脱离湍流场景 + L-DP8 已部分占点 + 数据同样缺失。

### Q-DP2/DP3 Conditional 的共同基建需求

两个方向都需要 **GG 时间域衰落模型**（现有文献只给幅度 PDF，衰落持续时间/频率全篇缺失）。建议先建共享基建，一次投入两个方向受益：
- Q-DP3 首选，MVE 验证恢复机制有效性
- Q-DP2 备选，复用 GG 时间模型算发散概率

### 关键技术发现

1. **"共识缝 ≠ 可做方向"**（TL-04 在双偏振空间的再次验证）：5 篇独立静态 SOP 建模是真实共识缝，但"动态 SOP 致失效"的因果链不成立（均衡器够用）。共识缝只是新颖性证据，必须转译成 M-C-A 且 A 物理成立才是问题。
2. **DSP 方向的 A0 适配**：A0 §2/§3/§4（ML 特性/跨域先例/MDP）不适用 DSP 方向，但 §1（性能间隙）/§5（负面证据）/§6（先验覆盖）对 DSP 方向反而更关键——核心精神"现有方法够不够"对 DSP 是加分判据。
3. **L-DP5/L-DP6 跨帧结论部分是预期性论述**：L-DP5 湍流未显式仿真（L176-184 "fluctuates at time scale much larger than frame duration"），跨帧挂起（L766-771）是预期分析非实测。Q-DP3 进 MVE 前需用真实 GG 时间模型验证跨帧真实性。

## 决策引用

- D001：Q-DP1 No-Go（A0 §1 物理基础不足）（新建）
- D002：Q-DP2 Conditional Go（空白真实但需自建时间模型）（新建）
- D003：Q-DP3 Conditional Go 首选（物理基础最扎实）（新建）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（Step 4a 可行性 Go/No-Go 是当前范围）
- 守 D018：3 Q# 全评完才排优先级 ✅（没边评边 Kill）
- 守不变量1：检查与 9 次 Kill 冲突 ✅（9 Kill 全单偏振，双偏振正交新空间，不冲突）
- 守 FR-25/TL-32：Go 判据 = 赢传统 baseline；oracle 上界只做 Kill 工具 ✅（Q-DP1 Kill 是 A0 物理致命不是 oracle；Q-DP2/DP3 的 Conditional 基于 A0/A/B 分析）
- 守 TL-27：物理量级核算前置 ✅（子 agent 核查均衡器跟踪上限 vs SOP 速率 + 衰落统计）

## 后续

**交用户确认**：
1. Q-DP1 No-Go 是否认可（或讨论 Pivot 出口）
2. Q-DP3 作为首选 Conditional Go 进维度 D MVE 是否认可
3. Q-DP2 作为备选是否认可

**如用户认可 Q-DP3 首选**，下一步（新对话）：
1. 补 FR-20 参数溯源：查大气湍流时间模型（Greenwood 频率/横风/功率谱）建 GG 时间域衰落模型
2. 进维度 D MVE：验证跨帧恢复机制有效性（恢复时间 / outage 概率 vs L-DP5 被动冻结 baseline）
3. MVE 架构摘要（FR-11）+ 先验对照（FR-14）+ 贡献目标 baseline 对照（FR-15）

**守 AGENTS.md 单对话 3 步上限**：本轮已完成报到+读框架+评估+写报告，已达上限，handoff 后新对话继续。
