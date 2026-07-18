# Handoff: pilot PASS → A+B 维全量蒸馏

> 来源: S002（pilot 验证） | 交接目标: 新对话续接，A+B 维全量蒸馏
> 文件名: H002-A-B-distillation.md
> 2026-06-15

## 已完成边界

**专题**：`2026-06-14-proposal-log-distillation`（开题报告写作日志蒸馏）。paper-eval / paper-write 的上游真实素材生产者，只产素材不实施下游。

**本轮（对话 A）已完成**：
1. **扫描模板设计（FROZEN）**：`scan-template.md`——7 形态→4 维映射总表 + 四维字段 schema（字段顺序固定）+ 跨 agent 可合并规则（id 前缀分区/material_form 枚举固定/source_ref 必带 :line/date_validity+direction 必填）+ 1 条填写示例（A6 innovation-points v1→v6 拆 A+C 两条）
2. **pilot 提取（3 agent × 4 份 = 12 份，56 条）**：distilled/pilot-agent1.md(A4 B7 C4 D4) + pilot-agent2.md(B8 C7) + pilot-agent3.md(A2 B6 C6 D8)。形态故意不重叠分配，覆盖全部 7 形态。
3. **pilot 验证 PASS（4/4 阈值）**：确定性 grep 验证（非 agent 自报，呼应 TL-21）——id 分区 12 区无冲突 / material_form 56/56 合规 / source_ref 56/56 带 :line / date+direction 56/56 覆盖 / 回溯抽查 5/5 有效。

**当前状态**：pilot 通过，scan-template 冻结。**下一步 = 对话 B（A+B 维全量蒸馏）**。

## 不要做什么

1. **不修改原始日志**（只读蒸馏，原文不动）—— 不变量 1
2. **不直接实施 paper-eval S033**（S033 等素材产出后由 paper-eval 专题决定推进）—— 不变量 4
3. **不重做 pilot 56 条**：pilot 产出的 A6 B21 条直接并入 distilled/A + distilled/B，对话 B agent 在此基础上补全剩余素材源，不重复提取 pilot 已覆盖的源
4. **不扫 stages/thesis-materials.md**（D003，用户判定"很旧别管"）
5. **不扫 thesis-platform repo 日志**（日志源在 research-protocol）
6. **主对话不 WebSearch / webReader**（用户全局硬规则）
7. **不凭文件名跳过阅读**（不变量 3，全量实读）
8. **不一次全量蒸馏**：A+B 是 32 源，仍需分 agent 分轮（每 agent ≤15min，每轮 ≤3 agent 并行）

## 必读（按优先级）

1. **`scan-template.md`**（本专题根目录）—— **FROZEN 扫描模板**。对话 B 的 agent 必须严格按此 schema 提取，字段顺序/枚举值/id 前缀规则全在此。**对话 B 的 id 前缀用 A-4xx/B-4xx（agent-1 第二轮）/ A-5xx/B-5xx（agent-2 第二轮）等，避开 pilot 的 -1xx/-2xx/-3xx**。
2. **`distilled/pilot-agent1.md` + `pilot-agent2.md` + `pilot-agent3.md`**—— pilot 已提取的 56 条。对话 B 要**复用其中的 A6 B21 条**（直接并入 distilled/A + distilled/B），并参考其字段格式继续提取剩余源。特别注意：pilot 的行号校准结果（B1/B3/C1/D4/B12 等已补齐/修正）应作为对话 B 的输入。
3. **`R002-scan-findings.md`**（661 行）—— 素材源索引。A 维 10 源（A1-A10）+ B 维 22 源（B1-B22）。pilot 已覆盖 A1/A3/A4/A5/A6/A10（6源）+ B1/B2/B3/B5/B6/B8/B9/B11/B12（9源）。**对话 B 剩余 = A 维 4 源（A2/A7/A8/A9）+ B 维 13 源（B4/B7/B10/B13-B22）**。
4. **`topic-index.md`**—— 不变量 4 条 + 范围边界 + 产出落点表
5. **`decisions.md`**—— D001-D003
6. **`S002-pilot-validation.md`**—— pilot 验证全过程 + 4 阈值结果 + 关键发现

## 接口变更（无代码改动，产出文件新增）

本轮新增产出文件（distilled/ 下）：

```yaml
pilot_outputs:
  - file: distilled/pilot-agent1.md
    type: pilot提取草稿
    content: 规则清单+批注原话形态 19 条（A4 B7 C4 D4）
    status: 草稿（A/B 部分待并入 distilled/A + distilled/B）
  - file: distilled/pilot-agent2.md
    type: pilot提取草稿
    content: diff对比+审查rubric形态 15 条（B8 C7）
    status: 草稿（B 部分待并入 distilled/B；C 部分留对话 C）
  - file: distilled/pilot-agent3.md
    type: pilot提取草稿
    content: 失败案例+命名方法论+工作流蓝图 22 条（A2 B6 C6 D8）
    status: 草稿（A/B 部分待并入 distilled/A + distilled/B；C/D 留对话 C）

template:
  file: scan-template.md
  status: FROZEN（pilot 已验证，不可改）
  consumer: 对话 B/C agent 必须遵守
```

下游消费方契约（D002）未变，仍为四维 distilled/A-pain-points.md / B-eval-criteria.md / C-rewrite-fewshot.md / D-writing-workflow.md。**对话 B 产出 A + B 两个文件的草稿**。

**跨 repo 路径风格**：thesis-platform 引用本专题产出用 `/mnt/d/code/study/research-protocol/.sessions/2026-06-14-proposal-log-distillation/distilled/`（WSL 路径，禁用 `D:\`）。

## 失败数据附录

- **agent 落盘阻塞**：3 个 Explore agent 全部 read-only 无 Write 工具，56 条内容在回复中返回，由主对话 Write 落盘。**经验**：后续对话 B/C 派 agent 时，要么主对话负责落盘，要么确认 agent 类型有 Write 权限。Explore agent 的"只读"是硬限制，非临时故障。
- **PowerShell 中文编码**：验证脚本含中文字符串字面量时，PS 以 GBK 读 UTF-8 源导致乱码解析错误。**解法**：脚本不硬编码中文字符串，用正则匹配 + 输出时由数据本身带中文（byte-safe）。临时脚本 `tools/_pilot_validate.ps1` 已清理。
- **行号定位惯例偏差**：agent 取段落/表格起始行作 source_ref 锚点，非关键词精确行。回溯抽查 5 条中 4 条是锚点（读者到该行往下看几行定位），1 条精确命中。**判定**：可接受，不构成回溯失效。对话 B/C agent 延续此惯例，主对话合并时容忍 ±5 行偏差。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| R002 行号待补项需回填 | file:line 指针应精确 | pilot 12 份覆盖的源行号已校准（B1/B3/C1/D4/B12 等），但校准结果未回填 R002 原文 | 对话 B 开工前主对话回填，或对话 D 统一处理；否则对话 B/C agent 可能用 R002 旧（错）行号 |
| thesis-materials"中文≥10篇/预印本率≤30%"引用质量门槛无替代源 | 排除项应无遗漏 | B11 标"待补"（原源 thesis-materials 已排除，D003） | 全量蒸馏 B 批时若仍未找到替代源，该条降级或标"原源已排除" |
| Explore agent 无 Write 权限 | 蒸馏产出需落盘 | pilot 由主对话落盘绕过 | 对话 B/C 同样处理，或换 agent 类型 |
| 次一级产物（规则库/检测器/few-shot/rubric/流程蓝图）尚未挖 | 全量蒸馏的产出 | R002 已标位置，未提取内容 | 对话 D 四批合并时逐批挖出 |

## 验证阈值（对话 B 产出验收）

对话 B 产出 distilled/A + distilled/B 草稿后，主对话用确定性 grep 验收（沿用 pilot 的 5 项检查）：

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| ID 前缀分区无冲突 | 对话 B 用 -4xx/-5xx，与 pilot 的 -1xx/-2xx/-3xx 不重叠 | scan-template 可合并规则 | pilot 100%（12 区无冲突） |
| material_form 枚举合规 | 100% 匹配 7 形态枚举，无自创 | scan-template | pilot 100%（56/56） |
| source_ref :line 覆盖 | 100% 带行号 | 不变量 3 | pilot 100%（56/56） |
| date_validity/direction 覆盖 | 100% 标注 | scan-template | pilot 100%（56/56） |
| 回溯指针抽查 | 抽查 ≥5 条回原文，≥80% 有效 | 不变量 3 | pilot 100%（5/5） |
| A/B 维覆盖完整 | A 维 10 源 + B 维 22 源全覆盖（pilot 已覆盖的 A6源+B9源记为"已提取"，不重做） | R002 素材源索引 | 未测 |

**对话 B FAIL 处理**：任一检查不过 → 修对应 agent 产出重跑该批（分层试错 P2：连续 2 轮 FAIL 强制截断回主对话找根因，不是模板问题——模板已 FROZEN）。

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（4 条：只读不改 / produces 跨 repo / 全量实读 / 不越界实施）
- [ ] 已验证本文件中的至少 3 条关键事实声称（建议验证）：
  - [ ] distilled/ 下确有 pilot-agent1/2/3.md 三个文件，合计 56 条（A6 B21 C17 D12）
  - [ ] scan-template.md 存在且含四维 schema + 7 形态映射 + 跨 agent 可合并规则
  - [ ] R002 中 pilot 已覆盖的源（A1/A3/A4/A5/A6/A10 + B1/B2/B3/B5/B6/B8/B9/B11/B12）行号与 pilot-agentN.md 的 source_ref 一致
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with（无依赖、无冲突）
- [ ] 已确认当前范围未违反"明确不含"（stages/thesis-materials.md 不扫、thesis-platform 日志不扫、原文不改）

## 下一轮（对话 B 详细）

### 目标
A 维 10 源 + B 维 22 源全量蒸馏，产出 distilled/A-pain-points.md + distilled/B-eval-criteria.md 草稿。

### 步骤

**步骤 1（主对话，开工前）**：回填 R002 行号。pilot 12 份校准的行号（B1/B3/C1/D4/B12 等在 pilot-agentN.md 的"行号校准说明"段）回填 R002-scan-findings.md 对应条目。**防对话 B agent 用错行号**。耗时约 10 分钟。

**步骤 2（3 agent 并行，第 1 轮）**：
- **agent-A（A 维全量剩余）**：A 维剩余 4 源（A2 ai-trace-report / A7 Ch2-reviews 复犯 / A8 R003-kaiti-chapter3 / A9 draft-ch1-template-test）。id 前缀 A-4xx。产出并入 distilled/A。
- **agent-B1（B 维前半，13 源拆 2）**：B 维剩余 13 源的前 7 源（B4 advisor-brief 公平性 / B7 Ch2-reviews 12子agent铁律 / B10 S023 诚实修正 / B13 引用4维可靠性 / B14 空白分级 / B15 学术诚信4条 / B16 S006 评审权重）。id 前缀 B-4xx。
- **agent-B2（B 维后半）**：剩余 6 源（B17 S006 够格线 / B18 defense-principles / B19 design-decisions否决 / B20 writing-patterns-sentence / B21 writing-patterns-paragraph / B22 其他）。id 前缀 B-5xx。

每 agent ≤15min。agent 落盘问题：**主对话落盘**（agent 产出返回后主对话 Write）。

**步骤 3（主对话）**：合并 pilot 的 A6 B21 条 + 对话 B 新提取的 A-4xx B-4xx B-5xx 条 → distilled/A-pain-points.md + distilled/B-eval-criteria.md 草稿。做 6 项验证（见上"验证阈值"）。PASS → 写 H003 交接对话 C；FAIL → 修对应 agent 产出重跑。

### 调度纪律
- 一次最多 3 个并行（用户全局规范）
- 单 agent ≤15min，装不下拆批
- id 前缀避让 pilot（-4xx/-5xx 起）
- agent 产出主对话落盘（Explore 无 Write）
- 不重做 pilot 已覆盖源（A1/A3/A4/A5/A6/A10 + B1/B2/B3/B5/B6/B8/B9/B11/B12）

### 后续对话框架（pilot 后的骨架，到时详排）

- **对话 C（C+D 蒸馏）**：C 22 源 + D 19 源。pilot 已覆盖 C1/C2/C5/C6/C10（5源）+ D1/D2/D4（3源）。剩余 C 17 源 + D 16 源。派 3 agent，2 轮。
- **对话 D（合并交付）**：四批合并去重 + verifier agent 交叉验证（P6 不自审）+ 跨 repo produces 声明 + 次一级产物挖掘。
