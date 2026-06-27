# Handoff: 块D完成 + Q12 Step4a评估=Kill，剩余Q#评估就绪

> 来源: S015+S016(块D) + 本轮Q12评估 | 交接目标: 下一个对话继续Step 4a评估剩余Q#
> 日期: 2026-06-27
> 文件名: H008-blockD-done-Q12-killed-remaining-Q-eval-ready.md

## 到哪了（状态）

**块 D Step 3.5 完成** + **块 E Step 4a：Q12 Kill + Q8 通过**。

- Step 3.5 ✅：检索+召回+Paillier JLT 精读完成，Q# 清单 Q1-Q13
- Step 4a 🔄进行中：
  - **Q12 评估=Kill（D006）**：B1 换皮（同构旧 B1 湍流感知 Kalman CPR）+ 旧 B1 已被 S024 证伪 + Paillier JLT 佐证，6 维度致命
  - **Q8 评估=通过 Step 4a（无致命信号）**：增益 100Gbps 硬 / 空白零假设无冗余 / B1 换皮核查澄清 advisor-brief 误读（导师没否决自适应大类）+ 不同构 N1 + 旧砍理由已被 Fernandes 2023 推翻。**Q8 唯一软肋：增量切入点未定义**

### 🔴 本轮两个关键澄清（对剩余评估最重要）

1. **advisor-brief 误读纠正**：advisor-brief line 9"自适应不可行"是学生写给导师的汇报稿，针对的是"自适应载波同步"（频率估计窗口/相位恢复窗口/锁相环带宽跟湍流调），不是泛指自适应。**导师没有否决"自适应"大类**。用户确认。后续 Q# 涉及"自适应"不必再被 advisor-brief 这句话吓退，但要区分时间尺度（湍流快 vs Doppler 慢）。
2. **B1 换皮核查应前置**：Q12 走到 Step 4a 才 Kill，本可块 D 召回时就查。Q8 这次先做换皮核查再评估，效率高很多。

### Q8 状态：方向合法，但切入点需定义

Q8 通过 Step 4a，但 Fernandes 2023 已做核心工作，硕士论文的**增量切入点**必须精确定义。4 候选（Fernandes 自述未做）：
1. 指向误差与 Doppler 耦合
2. 真实 SD-FEC 替代理想 FEC
3. 多波长/波分复用扩展
4. 湍流与 Doppler 的相互作用（Fernandes 把湍流当独立 SNR 衰减叠加）

切入点定后 → Step 4b 定义 MVE。

## 下一步干什么

**两条路（二选一或组合）**：

### 路径 A：深化 Q8 切入点（推荐，因为 Q8 是目前最干净的方向）
1. 查 4 个候选切入点是否已有论文做过（避免又撞已做）——派子 agent 检索
2. 重新精读 Fernandes 2023 future work 段（L281）确认扩展空间
3. 选定 1-2 个切入点 → Step 4b 定义 MVE

### 路径 B：继续评估其他全过 Q#
- Q1（TS-KF 两阶段解耦 Doppler，四判据全过，无旧 Kill 史）
- Q7（两阶段 CFE，四判据全过）
- 评估流程同 Q8/Q12（先 B1 换皮核查 + 导师边界，再 6 维度）

**建议**：Q8 是目前唯一通过 Step 4a 的方向，优先深化它的切入点定义，把"增量在哪"这个问题先解决。如果切入点定义后仍有戏，Q8 可能就是 Go 方向。其他 Q# 并行评估作为 backup。

## 纪律（和下一步直接相关的约束）

1. **D005 务实路线 INVARIANT**：Go=赢传统未优化 baseline 几 dB。FR-21 oracle 上界降为参考。FR-25 Go/Kill 对手标准分离
2. **B1 换皮核查前置**：每个 Q# 评估前先查 thesis-direction-pivot 有无同构方向 + 查 advisor-brief 真实含义（不误读）
3. **维度 B 空白零假设是致命项**：3 个结构性原因都暗示冗余 → Kill（Q12 的教训）
4. **四判据不可放水**（topic-index 不变量 3）
5. **FR-26 证据链**：声称必附证据指针。advisor-brief 这种转述要核对原话，不脑补

---
## 接收方验证（续接对话时必须完成）
- [ ] 已读取 topic-index 不变量段落（8 条，D005 务实路线最高优先级）
- [ ] 已验证至少 3 条关键事实声称：
  - [ ] Q12 Kill 在 decisions.md D006（核查 `grep "## D006" .sessions/2026-06-20-problem-driven-redirection/decisions.md`）
  - [ ] Q8 通过在 feasibility_report.md（核查 `grep "Q8 决策" projects/thesis-fso/feasibility_report.md`）
  - [ ] master-state Step 4a 🔄 含 Q12 Kill + Q8 通过（核查 `grep "4a feasibility" projects/thesis-fso/master-state.md`）
  - [ ] advisor-brief line 9 原文（核查 `sed -n '7,11p' .sessions/thesis-direction-pivot/advisor-brief.md`）确认是"自适应载波同步"非泛指
- [ ] 已检查 _registry.yaml depends_on/conflicts_with
- [ ] 已确认当前范围未违反"明确不含"

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 3 篇论文下不到（Rustum2026/Tang2024/Mosnier2025）| Step 3.5 补充 | SPIE/IET 非 OA | 块 E 按需 |
| H004 选样漏召根因 | D003 多候选不应路径过滤 | 已纠正 Q11-Q13 召回，根因未修流程 | 下次选样加检查步骤 |
| B1 换皮核查应前置 | Q12/Q8 教训 | 已写入纪律，下次评估前必查 | 持续执行 |
| Q8 增量切入点未定义 | Step 4b 前置条件 | 4 候选待定 | 深化 Q8 时查候选有无已做 |

## 下一轮

1. 读 H008 + feasibility_report.md（Q12 Kill + Q8 通过）
2. **深化 Q8**：查 4 候选切入点有无已做论文（派子 agent 检索）+ 精读 Fernandes future work 段 → 选定切入点 → Step 4b 定义 MVE
3. 或并行评估 Q1（TS-KF 全过，无旧 Kill 史）作 backup
4. Q8 切入点定后有戏 → 可能就是 Go 方向 → 进块 F（Step 5-7 baseline 复现）
