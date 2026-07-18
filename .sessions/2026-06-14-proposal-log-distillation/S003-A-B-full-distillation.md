# [S003] A+B 维全量蒸馏

> 2026-06-15 | 全量蒸馏 对话 B | 状态：完成
> 来源 H002（A-B-distillation）交接

## 目标

A 维 10 源 + B 维 22 源全量蒸馏，产出 distilled/A-pain-points.md + distilled/B-eval-criteria.md 草稿。pilot 已覆盖的 A6源+B9源不重做，在此基础上补全剩余。

## 记录

### 步骤 1：R002 行号回填（开工前）

pilot 12 份校准的行号回填 R002-scan-findings.md 10 个条目（B1/B3/B9/B12/C1/C5/C10/D1/D2/D4）。关键修正：
- B12 原 L26-31（Castrillon 段）→ 修正为 L59-62（Nguyen 段）
- C10/A8/A9 等原"行号待补"全部补齐
- D2（PROMPT-001）补 5 段精确行号

### 步骤 2：3 agent 并行提取（17 源）

| agent | 源 | 条目 | id 前缀 |
|-------|----|----|---------|
| agent-A | A2/A7/A8/A9（4源） | A 维 22 条 | -4xx |
| agent-B1 | B4/B7/B10/B13/B14/B15/B16（7源） | B 维 17 条 | -4xx |
| agent-B2 | B17/B18/B19/B20/B21/B22（6源） | B 维 18 条 | -5xx |

合计新增 57 条（A22 + B35）。

**agent-B1 重派事件**：首轮 agent-B1 只返回摘要未给完整 yaml 内容。重派时强调"必须把完整文件内容放代码块"，二轮成功拿到 17 条完整内容。**经验**：派 Explore agent 做产出任务时，prompt 必须明确"完整 yaml 内容放代码块，不只给摘要"。

**路径修正 3 处**（开工前主对话校验发现）：
- A2 `毕设/ai-trace-report.md` → 实际 `毕设/开题报告/ai-trace-report.md`
- B4 `advisor-briefing.md` → 实际两个文件 `advisor-brief.md` + `advisor-briefing-2026-05-30.md`
- B18 `毕设/defense-principles` → 实际 `毕设/开题PPT/defense-principles.md`

**行号校准收益**：A8 的 P1-P6 行号（R002 标"待补"）由 agent-A 实读补齐（P1=L26/P2=L36/.../P6=L80/归类表=L88）；A9 文件实测 321 行（R002 标 445 行有误）；B18/B19 行号校准（defense-principles 各段 + design-decisions 否决索引在 L549-566 非 613 行）。

### 步骤 3：合并验证（6 文件 113 条，确定性 grep）

| 检查项 | 结果 | 判定 |
|--------|------|------|
| ID 分区（13 区） | A-1:4 A-3:2 A-4:22 / B-1:7 B-2:8 B-3:6 B-4:17 B-5:18 / C-1:4 C-2:7 C-3:6 / D-1:4 D-3:8，**无冲突** | PASS |
| material_form 枚举 | 113/113 合规（规则清单27/审查rubric28/失败案例29/批注原话8/diff对比8/工作流蓝图7/命名方法论6） | PASS |
| source_ref 行号 | 113/113 带 :line | PASS |
| date/direction 覆盖 | 113/113 | PASS |
| 回溯抽查 | 3 条新条目（B-401/B-509/A-412）3/3 精确命中 | PASS |
| A 维覆盖 | 28 条覆盖 A1-A10 全部 10 源 | PASS |
| B 维覆盖 | 56 条覆盖 B1-B22 全部 22 源 | PASS |

**对话 B 判定：PASS（7/7 验证项通过）**

### 产出交付

| 文件 | 内容 | 状态 |
|------|------|------|
| distilled/A-pain-points.md | A 维 28 条 + 分类索引（7 族）+ S033 输入映射 + 已知限制 | 草稿（对话 D 定稿） |
| distilled/B-eval-criteria.md | B 维 56 条 + 已有 rubric 参照系（13 项）+ 新维度索引（6 族）+ S033 输入映射 + 已知限制 | 草稿（对话 D 定稿） |
| distilled/batchB-agentA.md | A-401~422 原始 yaml | 完成 |
| distilled/batchB-agentB1.md | B-401~417 原始 yaml | 完成 |
| distilled/batchB-agentB2.md | B-501~518 原始 yaml | 完成 |

### 关键发现

1. **A 维痛点集中在 3 大簇**：AI 痕迹检测（8 条，A-101/102/401~406）、反复犯错检测（5 条，A-407~411）、开题第三章根因（7 条，A-412~418）。下游 paper-eval 的 AI 痕迹检测器有充足素材。
2. **B 维评估标准极丰富**（56 条，占四维总数 113 的 50%）：印证 R002 关键洞察 1（B 维最丰富）。39 条新维度 + 17 条映射已有 rubric，下游 paper-eval 的评估体系有大量可操作 rubric。
3. **范文铁律族现已全覆盖**（铁律 1-4 齐全）：pilot 提铁律 1/3，对话 B 补铁律 2/4。这 4 条经范文交叉验证，可作为 paper-write 的硬约束。
4. **增益真实性审查族成形**（7 条）：公平性三步法 + 基线公平 + 压力测试 FAIL + 增益归因消融 + 种子数充分性 + 自我证伪心态 + 诚实自评——完整的增益声称验证链。
5. **is_covered 判定需 verifier 复核**：本批 17 条标"是"（映射已有 rubric），但 verifier 可能在语义近邻组发现新的合并关系。

## 决策引用

- 无新建 D###（全量蒸馏确认 D002 契约字段可填充性——A/B 维 PASS）
- D002：下游接口契约字段（本 session 验证 A/B 维可填充且可合并）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（A+B 维全量蒸馏是 H002 明确的对话 B 目标）
- 未修改原始日志（只读蒸馏，不变量 1 守住）
- 未实施 paper-eval S033（只产素材，不变量 4 守住）
- R002 行号回填是元数据维护，非原文修改

## 后续

### 立即（对话 C，H003 交接目标）
C+D 维全量蒸馏。C 维 22 源 + D 维 19 源。pilot 已覆盖 C1/C2/C5/C6/C10（5源）+ D1/D2/D4（3源）。剩余 C 17 源 + D 16 源。派 3 agent，2 轮。

### 对话 D（合并交付）
四批合并去重 + verifier agent 交叉验证（P6 不自审）+ 跨 repo produces 声明 + 次一级产物挖掘（规则库/检测器/few-shot/rubric/流程蓝图）。

### 待 verifier 处理的语义近邻组（已知）
- A 维：A-101（R011 5 大缺陷）与 A-401（ai-trace 5 类分类）语义重叠，verifier 合并
- B 维铁律族（B-204/404/205/405）可合并为一条 rubric 集合
- B 维增益真实性族（B-301/302/306/401/406/407）可合并为评估链
- B 维引用可靠性族（B-303/408/409/412/413）可合并

### R002 行号回填未完成项
本轮回填了 pilot 覆盖的 10 源。对话 C 覆盖的 C/D 源行号待对话 C 实读后回填。
