# Handoff: 4B Kill 收尾 + checklist 立 → 下轮用 checklist 评 Q1

> 来源: S018 | 交接目标: 下个对话用 D009 checklist 直接对照评估 Q1
> 日期: 2026-06-28
> 文件名: H010-entrypoint4B-killed-checklist-set-eval-Q1.md

## 到哪了（状态）

块 E Step 4a 继续推进。本轮完成了三件事：

1. **Q8 切入点 4B Kill（D008）**：D007 先把 4B 重定义为"仰角驱动 σ² 慢包络自适应 PCS/Rs 调度"（三查坐实物理 gap），但 FR-21 数值估算显示**性能 gap 趋零**——vs Fernandes 中档折中 +0.01dB（A3 失败），根因是 ABR 对 σ² 平缓（A2 失败）。**4B 物理 gap 真实但转不成性能 gap**。

2. **立「靠谱方向 checklist」v1（D009）**：用户戳穿"你有看之前的日志吧？有知道我的诉求吧？"后，主线反思"一直塞方向没帮定标准"（违反诉求 2"先定标准别样样松"），立 checklist：A1 轻化（可验证处理贡献不锁"DSP 链路"）+ **A2（指标敏感，4B 教训新提炼，最关键新增）** + A3（增量≥同门~2-4dB）+ B1/B2/B3 + C1/C2/C3。

3. **暂 0 Go**：Step 4a 硬门控未释放。已 Kill：Q12（D006）/ Q8 切入点 2（S017）/ Q8 切入点 4B（D008）。待评：Q8 切入点 1 + Q1 + Q2/Q3/Q7/Q10。

## 下一步干什么

**用 D009 checklist 评估 Q1（TS-KF 两阶段解耦 Doppler）**。Q1 定义见 `projects/thesis-fso/literature_notes.md` L01（OE 2025 #1，DOI 10.1364/oe.553709，两阶段 KF 递归估计，状态 [ω,ϕ] 双 Q 解耦捕获/锁定）。

**评估纪律（来自 D009）**：
1. **先过 A1/A2/A3 三条硬门槛，5 分钟快判**：
   - A2 前置：先算/查"BER 或同步精度对 Doppler 敏感度"——Doppler 变化（10-15GHz 突发 + MHz/s 漂移）时 BER/同步精度变多少？这是 Q1 的命门（对应 4B 的 ABR-σ² 平缓死法）
   - A3：Q1 能赢的传统未优化 baseline 是什么？增量量级跟同门（~2-4dB）可比吗？
2. A 类过 → 再过 B/C 类 + 四判据 + 维度 A0/A/B + FR-21
3. 任一硬门槛失败 → 直接 Kill，不进长流程

## 纪律（和下一步直接相关的约束）

1. **A2 是 4B 教训的核心**——别再让"物理 gap 真实但性能 gap 趋零"的方向走完长流程才发现死。Q1 的 Doppler 是高动态（10-15GHz），BER/同步精度对它**应该**敏感（不像 ABR 对 σ² 那么平缓），但必须先算确认，不能假设。
2. **"baseline 简化了 X" ≠ "X 的简化带来性能损失"**（4B 教训）——Q1 评估时如果发现 baseline 简化了某变量，先查性能影响再判 gap 真实性。
3. **用户诉求复核**（重读 voice.md）：①务实毕业有点东西就行（D005）②先定标准别样样松（S003）③方法论验证优先（S001）④和同门类似那种东西（H004）。checklist 就是诉求 2 的落地。
4. **主线别"过早 Kill"也别"为救方向取有利解释"**（D007 + D008 双向教训）——表述错误修正不等于方向死；但 FR-21 对比基准要干净，按"工程合理 baseline"算，不为救方向找理由。
5. **用户委托技术判断**（"我对这块没啥了解"+"安妮推荐来"）——主线自推进每步汇报，A2/A3 算完直接判，不用逐个停下问，但 Go/Kill 决策仍报用户确认。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（8 条，D005 务实路线为最高优先级 INVARIANT）
- [ ] 已验证本文件中的至少 3 条关键事实声称（建议验证）：
  - 4B Kill 的 FR-21 数值（D008 / feasibility_report.md 切入点 4B Kill 段，vs 中档 +0.01dB）
  - D009 checklist 9 条内容（decisions.md D009 / topic-index 已确认决策段）
  - Q1 定义（literature_notes.md L01，TS-KF OE 2025）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（仍在块 E Step 4a 主线，星地激光通信大背景内）

## 关键文件指针

- **D009 checklist**（评估 Q1 必读）：`.sessions/2026-06-20-problem-driven-redirection/decisions.md` D009 段
- **4B Kill 详情**（A2/A3 死法参照）：`decisions.md` D008 + `projects/thesis-fso/feasibility_report.md` 切入点 4B Kill 段
- **Q1 定义**：`projects/thesis-fso/literature_notes.md` L01（DOI 10.1364/oe.553709）
- **同门范式基准**（A3 量级参照）：`S014-correct-S013-and-direction-skeleton-and-D004.md` 第 3-4 步（王培森 4.5dB / 李兀祺 0.25-4dB / 弱信号同步 -2.8~-10dB）
- **GW Progress 表**（FR-22 跨 Step 门控）：`projects/thesis-fso/master-state.md` L47（Step 4a 🔄，暂 0 Go）
- **用户诉求**：`.sessions/2026-06-20-problem-driven-redirection/voice.md`（D005 务实 / S003 样样松 / H004 同门范式）

## 下一轮

评估 Q1（TS-KF 两阶段解耦 Doppler）：
1. 读 Q1 全文精读笔记（literature_notes.md L01）+ 原文（papers/doi/10.1364_oe.553709/content.md）
2. 用 D009 checklist 逐条对照，A2（BER/同步精度对 Doppler 敏感度）前置算
3. A 类硬门槛全过 → 四判据 + 维度 A0/A/B + FR-21 完整评估
4. 任一硬门槛失败 → Kill，转 Q8 切入点 1 或 Q2/Q3/Q7/Q10
5. Go → 进 Step 4b（C/E 维度）+ Step 5（Baseline 选定）
