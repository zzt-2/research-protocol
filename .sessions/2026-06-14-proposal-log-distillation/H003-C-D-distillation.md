# Handoff: A+B 维完成 → C+D 维全量蒸馏

> 来源: S003（A+B 维全量蒸馏） | 交接目标: 新对话续接，C+D 维全量蒸馏
> 文件名: H003-C-D-distillation.md
> 2026-06-15

## 已完成边界

**专题**：`2026-06-14-proposal-log-distillation`。paper-eval / paper-write 的上游真实素材生产者。

**累计已完成**：
- **pilot（S002）**：scan-template.md FROZEN + 56 条验证 4/4 阈值 PASS
- **对话 B（S003，本轮）**：A+B 维全量蒸馏完成
  - distilled/A-pain-points.md 草稿：**28 条**，覆盖 R002 A 维 10 源全部
  - distilled/B-eval-criteria.md 草稿：**56 条**，覆盖 R002 B 维 22 源全部
  - 累计 113 条（A28 B56 C17 D12），6 文件确定性 grep 验证 7/7 PASS
  - R002 行号回填 10 源（pilot 覆盖的）

**当前状态**：A+B 维完成，**下一步 = 对话 C（C+D 维全量蒸馏）**。

## 不要做什么

1. **不修改原始日志**（只读蒸馏）—— 不变量 1
2. **不直接实施 paper-eval S033** —— 不变量 4
3. **不重做 pilot/对话B 已覆盖的源**：C 维 pilot 已覆盖 C1/C2/C5/C6/C10（5源）；D 维 pilot 已覆盖 D1/D2/D4（3源）。剩余 C 17 源 + D 16 源。
4. **不扫 stages/thesis-materials.md**（D003）
5. **不扫 thesis-platform repo 日志**
6. **主对话不 WebSearch / webReader**
7. **不凭文件名跳过阅读**（不变量 3）
8. **不一次全量**：C+D 是 33 源（去 pilot 覆盖），仍分 agent 分轮
9. **不改 scan-template.md**（已 FROZEN，pilot + 对话 B 双重验证）

## 必读（按优先级）

1. **`scan-template.md`**（FROZEN）—— C/D 维字段 schema + 跨 agent 可合并规则。**对话 C 的 id 前缀用 C-4xx/D-4xx（agent-1）/ C-5xx/D-5xx（agent-2）/ C-6xx/D-6xx（agent-3）等，避开 pilot 的 -1xx/-2xx/-3xx 和对话 B 的 -4xx/-5xx**。注意 B 维用过 -4xx/-5xx，但 C/D 维是独立编号空间，仍可从 -4xx 起（因维度字母不同，C-4xx 与 B-4xx 不冲突）。
2. **`distilled/A-pain-points.md` + `B-eval-criteria.md`**—— 对话 B 产出。参考其文档结构（分类索引 + S033 输入映射 + 已知限制），对话 C 产出 C/D 文件用同构结构。
3. **`distilled/pilot-agent1.md` + `pilot-agent2.md` + `pilot-agent3.md`**—— pilot 已提取的 C17/D12 条。对话 C 要**复用其中 C17/D12 条**（直接并入 distilled/C + distilled/D），不重复提取 pilot 已覆盖源。
4. **`R002-scan-findings.md`**（661 行）—— C 维 22 源（C1-C22）+ D 维 19 源（D1-D19）。pilot 已覆盖 C1/C2/C5/C6/C10 + D1/D2/D4。**对话 C 剩余 = C 维 17 源（C3/C4/C7-C9/C11-C22）+ D 维 16 源（D3/D5-D19）**。
5. **`topic-index.md`**—— 不变量 + 范围边界
6. **`S003-A-B-full-distillation.md`**—— 对话 B 全过程 + 关键发现（语义近邻组待 verifier 合并）

## 接口变更（本轮新增产出）

```yaml
batchB_outputs:
  - file: distilled/batchB-agentA.md
    content: A 维 22 条（A-401~422）
  - file: distilled/batchB-agentB1.md
    content: B 维 17 条（B-401~417）
  - file: distilled/batchB-agentB2.md
    content: B 维 18 条（B-501~518）

contract_drafts:
  - file: distilled/A-pain-points.md
    type: 契约交付草稿
    content: A 维 28 条 + 分类索引 + S033 映射
    status: 草稿（对话 D verifier 定稿）
  - file: distilled/B-eval-criteria.md
    type: 契约交付草稿
    content: B 维 56 条 + 已有 rubric 参照系 + 新维度索引 + S033 映射
    status: 草稿（对话 D verifier 定稿）
```

下游消费方契约（D002）A/B 两维草稿已就位，C/D 两维待对话 C 产出。

## 失败数据附录

- **agent-B1 首轮只给摘要**：Explore agent 做"产出任务"时，若 prompt 未明确要求"完整内容放代码块"，agent 可能只返回摘要。**解法**：prompt 必须明确"把完整 yaml 内容放在回复的 ```代码块里，不只给摘要"，并强调"不要只给摘要"。本轮重派成功。
- **路径修正 3 处**：R002 的 A2/B4/B18 路径不准（A2 漏"开题报告"子目录；B4 "advisor-briefing.md" 实际是两个文件；B18 漏"开题PPT"子目录）。**经验**：派 agent 前主对话必须 Test-Path 校验所有源文件路径，R002 指针可能不准。
- **行号 R002 标注有误 2 处**：A9 R002 标"445 行"实际 321 行；B19 R002 标"613 行否决索引段"实际否决索引在 L549-566（613 是文件总行数）。**经验**：R002 的行数/行号标注可能混淆"文件总行数"与"段落行号"，agent 实读时校准。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| R002 行号回填未完成 | file:line 指针精确 | pilot 覆盖 10 源已回填；对话 B 覆盖的 A/B 源行号校准结果（A8 P1-P6 / B18 / B19）未回填 R002 | 对话 C 开工前回填，或对话 D 统一处理 |
| A/B 维语义近邻组未合并 | 同语义条目应合并 | A 维（A-101 vs A-401）/ B 维铁律族/增益真实性族/引用可靠性族 已在索引标注 | 对话 D verifier agent 合并 |
| thesis-materials 引用质量门槛无替代 | 排除项无遗漏 | B11 仍"待补" | 对话 D 处理 |
| Explore agent 无 Write 权限 | 产出需落盘 | pilot + 对话 B 均由主对话落盘 | 对话 C/D 同样处理 |
| C/D 维次一级产物未挖 | 全量蒸馏产出 | R002 已标位置 | 对话 C 提取 + 对话 D 合并 |
| agent 产出 prompt 需强调"完整内容" | 避免只给摘要 | 对话 B agent-B1 首轮失败，重派成功 | 对话 C 派 agent 时 prompt 明确要求 |

## 验证阈值（对话 C 产出验收）

沿用 pilot + 对话 B 的验证项，对话 C 产出 distilled/C + distilled/D 草稿后主对话用确定性 grep 验收：

| 验证项 | PASS 标准 | 历史通过率 |
|--------|----------|-----------|
| ID 前缀分区无冲突 | 对话 C 用 C/D-4xx/5xx/6xx，不与已有冲突 | pilot+对话B 100% |
| material_form 枚举合规 | 100% 匹配 7 形态 | pilot+对话B 100%（113/113） |
| source_ref :line 覆盖 | 100% 带行号 | pilot+对话B 100%（113/113） |
| date_validity/direction 覆盖 | 100% 标注 | pilot+对话B 100%（113/113） |
| 回溯指针抽查 | 抽查 ≥3 条回原文，≥80% 有效 | pilot+对话B 100% |
| C/D 维覆盖完整 | C 22 源 + D 19 源全覆盖（pilot 覆盖的记"已提取"） | 未测 |

**对话 C FAIL 处理**：任一不过 → 修对应 agent 产出重跑（分层试错 P2）。

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（4 条）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] distilled/A-pain-points.md 存在且含 28 条 A 维条目（覆盖 A1-A10）
  - [ ] distilled/B-eval-criteria.md 存在且含 56 条 B 维条目（覆盖 B1-B22）
  - [ ] R002 中 C3/C4/C7-C9/C11-C22 + D3/D5-D19 这些对话 C 待覆盖源条目存在且指针可定位
- [ ] 已检查 _registry.yaml（无依赖无冲突）
- [ ] 已确认范围未违反"明确不含"

## 下一轮（对话 C 详细）

### 目标
C 维 17 源（剩余）+ D 维 16 源（剩余）全量蒸馏，产出 distilled/C-rewrite-fewshot.md + distilled/D-writing-workflow.md 草稿。

### 步骤

**步骤 1（主对话，开工前）**：
1. 回填 R002 对话 B 校准的行号（A8 P1-P6 / B18 defense / B19 design-decisions 索引段等）
2. Test-Path 校验对话 C 的 33 源文件路径（C3/C4/C7-C9/C11-C22 + D3/D5-D19），修正 R002 不准路径
3. 提取 R002 这些源条目内容

**步骤 2（3 agent 并行，第 1 轮）**：
- **agent-C1（C 维前半）**：C3/C4/C7/C8/C9 + C11/C12/C13（C 维剩余 17 源拆 2-3 批，前半 7-8 源）。id 前缀 C-4xx。
- **agent-C2（C 维后半）**：C14-C22（后 9 源）。id 前缀 C-5xx。
- **agent-D1（D 维前半）**：D3/D5/D6/D7/D8/D9/D10（D 维剩余 16 源拆 2 批，前半 7 源）。id 前缀 D-4xx。

每 agent ≤15min。**prompt 必须明确"完整 yaml 内容放代码块，不只给摘要"**（agent-B1 教训）。

**步骤 3（3 agent 并行，第 2 轮）**：
- **agent-D2（D 维后半）**：D11-D19（9 源）。id 前缀 D-5xx。
- 视 agent-C1/C2 进度，可能补 agent-C3 处理溢出

**步骤 4（主对话）**：合并 pilot 的 C17/D12 条 + 对话 C 新提取条 → distilled/C + distilled/D 草稿。做 6 项验证。PASS → 写 H004 交接对话 D。

### 调度纪律
- 一次最多 3 并行
- 单 agent ≤15min
- id 前缀避让（C/D-4xx/5xx/6xx 起；注意 C/D 维与 B 维编号空间独立）
- agent 产出主对话落盘
- prompt 明确"完整内容放代码块"
- 不重做 pilot 已覆盖源（C1/C2/C5/C6/C10 + D1/D2/D4）

### 后续对话框架

- **对话 D（合并交付）**：四批合并去重（含语义近邻组合并）+ verifier agent 交叉验证（P6 不自审）+ 跨 repo produces 声明 + 次一级产物挖掘（规则库/检测器/few-shot/rubric/流程蓝图）+ 最终交付。
