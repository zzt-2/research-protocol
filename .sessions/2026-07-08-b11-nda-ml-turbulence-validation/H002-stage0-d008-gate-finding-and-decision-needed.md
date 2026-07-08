# Handoff: 阶段 0.1-0.2 完成 — D-008 门控核心前提被推翻，需用户决策 INVARIANT 11 重新框定

> 来源: S002 | 交接目标: 主控对话/用户决策 INVARIANT 11 + 新对话执行阶段 0.3-0.6
> 文件名: H002-stage0-d008-gate-finding-and-decision-needed.md
> 日期: 2026-07-08

## 到哪了（状态）

阶段 0.1（D-008 耦合门控）+ 阶段 0.2（B11 行 33 假设核查）完成，未写代码未进 sandbox。续接盘点发现老师反馈遗漏（见下）。

**🔴 重大发现（改变 B11-Q2 性质）**：
- **D-009 bug 讨论早已闭合**（加权修复版 sandbox 跑完，仍 vs VV 全场景持平，ML 加权单载波时域无用）。D-008 status 字段虽 pending_fix，实质是"修不修无关紧要，pending 老师反馈但 dormant"——不是"待修"
- B11-Q2 前置条件（INVARIANT 11）核心前提"持平是 bug→修复后应拉开"**被 D-009 推翻**
- 但 B11-Q2 真增量锚（vs DA-ML +1.35~3.1dB）不受 D-008 影响（baseline 是 DA-ML 不是 VV）
- **🔴 老师反馈已到（2026-07-08）**："新方法不是要求全能，是在某一实际需求场景下的特长"——重定判据，直接解套 B11-Q2（见下"老师反馈对 B11-Q2 含义"）

**B11 行 33 假设核查结论**：仿真简化（B11 没建模湍流），B11-Q2 加湍流是真实物理缺口。

## 不要做什么

1. **不要 D-008 修复前跑 sandbox**（守 INVARIANT 11 字面，直到用户拍板重新框定）
2. **不要自作主张改 INVARIANT 11**（推翻不变量必须用户拍板，工作对话只记录发现 + 报主控/用户）
3. **不要把"D-009 加权无用"当 B11-Q2 的 Kill 信号**——它只影响 vs VV 对照，B11-Q2 的增量锚是 vs DA-ML（D-008/D-009 均确认不受影响）
4. **不要跳阶段 0.3-0.6 直接写代码**（守 profile 第 9 次防线）
5. **不要把 B11-Q2 当只重复 B11-Q1 湍流结果**（B11-Q1 D005 已有 weak +1.20/moderate +1.92dB，B11-Q2 需新增量维度，阶段 0.4 明确）

## 必读（按优先级）

1. **本 H002 + topic-index**（14 不变量，🔴 INVARIANT 11 待用户决策）
2. **S002** 阶段 0.1-0.2 完整记录
3. **阶段 0.1 产出**：`explore/b11-nda-ml-turbulence-validation/_d008_dependency_check.md`（D-009 推翻前置条件核心前提的详细证据链）
4. **阶段 0.2 产出**：`explore/b11-nda-ml-turbulence-validation/_b11_assumption_audit.md`
5. **NDA-ML D-008/D-009 决策**：`step4a-mve-execution/decisions.md` L297-490（D-009 sandbox 加权无用定论）
6. **上游**：S001 + H001（原 INVARIANT 11 设计前提）

## 下一步干什么

### 🔴 老师反馈对 B11-Q2 含义（续接盘点新发现）

老师 2026-07-08 反馈两件（step4a voice.md L60-61，主线核查原文）：
1. **"新方法不是要求全能，是在某一实际需求场景下的特长"** → 重定判据
2. **"对比参考文献请单独发给我。要求:近年 transactions 水平"** → step4a 遗留 TODO（不在 B11-Q2 范围）

**对 B11-Q2 直接含义**：老师判据下，B11-Q2 的"特长场景"= 湍流下 pilot-free 鲁棒性（对照 DA-ML），不是"超 VV"。vs VV 持平根本不是要追的目标。主线初步解读可能是"上行强湍流 pilot-free 鲁棒性"（vs DA 上行 +2.48~3.07dB 比 VV 持平更值钱），**但不能替老师解读，需用户确认**。

### 🔴 优先 1：主控对话/用户决策 INVARIANT 11 重新框定

向用户报告阶段 0.1 核心发现 + 老师反馈，给两个选项：

- **选项 A（保守）**：维持 INVARIANT 11 字面，D-008 common 修复前不跑 sandbox（但 D-009 已证加权无用 + D-008 实质 dormant，common 可能不会修）
- **选项 B（重新框定，建议，老师判据加持）**：D-008 不再是 sandbox 门控，B11-Q2 sandbox 用现有等权版 NDA-ML 验证"湍流下 vs DA-ML 是否保持 +2dB"。三条理由：①D-009 已证加权无用（修不修无关紧要）②老师"特长场景"判据下增量锚是 vs DA-ML（pilot-free）不是 vs VV ③D-008 双 bug 只影响 vs VV 对照不影响 vs DA-ML

**建议选项 B**，但必须用户拍板（不变量修改）。同时需确认老师"特长场景"的具体解读。

### 优先 2：阶段 0.3-0.6（新对话，不依赖 D-008 决策）

阶段 0.3-0.6 的规约设计不依赖 INVARIANT 11 决策，可并行推进：
- 0.3 架构定性（阶段 0.1 已顺带确认 _recovery.py 是前馈闭式无环路 TF，不撞 D006——只需正式落文档）
- 0.4 公平对照框架（baseline DA-ML；**关键是明确 B11-Q2 vs B11-Q1 D005 湍流结果的新增量维度**）
- 0.5 参数真相源（湍流 Cn²/σ² + 线宽，继承 common/_channel.py + params.py，标文献来源 TL-26）
- 0.6 文件组织规约

## 纪律

1. **INVARIANT 11 重新框定必须用户拍板**，工作对话不自作主张
2. **D-009 加权无用结论不影响 B11-Q2 的 vs DA-ML 增量锚**（D-008/D-009 均确认）
3. **B11-Q2 不能只重复 B11-Q1 D005 湍流结果**（需新增量维度，阶段 0.4 明确）
4. **profile 第 9 次防线**：阶段 0 六项规约全做完才进 sandbox
5. **核查机制中性双向**（本轮已践行：子 agent + 主线独立 grep）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 14 不变量（重点 11 待决策 + 13 已核查结论）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] D-008 双 bug 未修进 common（核查 `_recovery.py` L213/232 + decisions.md D-008 status）
  - [ ] D-009 sandbox 加权修复版仍 vs VV 持平（核查 `_ml_weighting_results.json` + decisions.md D-009 L384-385）
  - [ ] B11 行 33 是仿真简化（核查 B11 content.md L33 + 全文无湍流建模）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（step4a dormant + D-008 pending_fix 是核心耦合）
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**主控对话/用户决策后**：
- 选项 A → 等 D-008 common 修复（可能不来）
- 选项 B → 阶段 0.3-0.6 完成后进 sandbox（NDA-ML 等权版 vs DA-ML 湍流三方对照）

**无论 A/B**：阶段 0.3-0.6 规约设计可并行推进（不依赖 INVARIANT 11 决策）。
