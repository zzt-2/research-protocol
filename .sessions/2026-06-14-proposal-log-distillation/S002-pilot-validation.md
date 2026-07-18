# [S002] pilot 扫描模板设计 + 12 份验证

> 2026-06-15 | pilot 验证 | 状态：完成
> 来源 H001（pilot-and-distillation）交接

## 目标

对话 A（H001 交接目标）：设计扫描模板把 R002 的 7 种素材形态映射到 D002 四维契约字段；用 12 份 pilot 验证模板可合并性（分层试错法 P3，PASS 才放大全量）。

## 记录

### 步骤 1：扫描模板设计（主对话拍板，FROZEN）

产出 `scan-template.md`（本专题根目录）。核心设计：

1. **7 形态 → 4 维映射总表**：规则清单/批注原话/diff对比/审查rubric/失败案例/命名方法论/工作流蓝图 → A/B/C/D。一条原文可拆多条不同维度（如 innovation-points v1→v6 既 A 痛点又 C 反例）。
2. **四维字段 Schema**（FROZEN，字段顺序固定）：
   - A：`{id, source_ref, source_agent, material_form, date_validity, direction, pain_point, original_quote, classification, s033_input}`
   - B：`{id, source_ref, source_agent, material_form, date_validity, direction, criticism_point, original_quote, is_covered, covered_by, new_dimension}`
   - C：`{id, source_ref, source_agent, material_form, date_validity, direction, original_text, rewritten_text, good_example, why_good, fewshot_target}`
   - D：`{id, source_ref, source_agent, material_form, date_validity, direction, workflow_step, step_group, step_order, vs_paperwrite, optimization}`
3. **跨 agent 可合并规则**：id 前缀分区（agent-1:-1xx / agent-2:-2xx / agent-3:-3xx）；material_form 枚举固定 7 值；source_ref 必带 :line（WSL 路径）；date_validity/direction 必填。
4. **1 条填写示例**：从 A6（innovation-points v1→v6）拆成 A-001 + C-001 两条，演示多维度提取。

设计依据：读了 4 份典型原文（R011 / innovation-points / S003 / CONCLUSIONS）确认字段能装下真实素材，不凭 R002 摘要设计。

### 步骤 2：3 agent 并行 pilot 提取（12 份，形态不重叠）

按 H001 步骤 2 表分配，每 agent 4 份：

| agent | 形态 | 文件 | 产出维度分布 |
|-------|------|------|-------------|
| agent-1 | 规则清单 + 批注原话 | R011(C1) / innovation-points(D4) / 开题批注(B1) / S001(B3) | A4 B7 C4 D4 = 19 |
| agent-2 | diff 对比 + 审查 rubric | Ch2-reviews(C2/B5/B6) / R003(C6) / CONCLUSIONS(B8) | B8 C7 = 15 |
| agent-3 | 失败案例 + 命名方法论 + 工作流蓝图 | S024(B9)+FINAL_OUTPUT(B12) / cnki-survey(C10)+figure-composition(C5) / S003(D1) / PROMPT-001(D2) | A2 B6 C6 D8 = 22 |

合计 **56 条**（A6 B21 C17 D12）。

**agent 落盘问题**：3 个 Explore agent 全部 read-only 无 Write 工具，内容在回复中返回。主对话用 Write 工具落盘 3 个 pilot-agentN.md 到 distilled/。

**行号校准收益**：pilot 实读修正了 R002 多处"行号待补"（B1/B3/C1/D4 无行号→补齐；B12 原 L26-31 误指 Castrillon 段→修正为 L59-62 Nguyen 段）。这些校准应回填 R002（已知债务，对话 D 处理）。

### 步骤 3：合并验证（主对话，确定性 grep 不依赖 agent 自报）

用 PowerShell 脚本对 3 文件做 5 项确定性检查（呼应 TL-21 教训）：

| 检查项 | 结果 | 判定 |
|--------|------|------|
| ID 前缀分区（12 区） | A-1:4 A-3:2 / B-1:7 B-2:8 B-3:6 / C-1:4 C-2:7 C-3:6 / D-1:4 D-3:8，**无跨区冲突** | PASS |
| material_form 枚举合规 | 7 值全出现（规则清单12/diff对比8/失败案例10/批注原话7/工作流蓝图7/审查rubric6/命名方法论6），**56/56 合法无自创** | PASS |
| source_ref 行号覆盖 | **56/56 带 :line**，0 缺失 | PASS |
| date_validity/direction 覆盖 | **56/56 全覆盖** | PASS |
| 回溯指针抽查 | 5 条抽查 5/5 有效（4 条为段落起点锚点惯例，1 条精确命中） | PASS |

**回溯指针惯例**：agent 取段落/表格起始行作锚点，非关键词精确行。读者到该行往下看几行即定位——可接受，不构成回溯失效。

**pilot 判定：PASS（4/4 验证阈值通过）**

| 验证阈值 | PASS 标准 | 实测 |
|----------|----------|------|
| 扫描模板字段覆盖 | 7 形态映射到 A/B/C/D | 7 形态全出现，56 条全填，无"装不下" ✅ |
| 跨 agent 可合并性 | 字段一致可拼接去重 | 12 区无冲突，同维度字段顺序一致 ✅ |
| 回溯指针有效 | file:line 回原文 | 56/56 带 :line，抽查 5/5 有效 ✅ |
| 日期约束执行 | pivot 前素材标注 | C-205~207（旧 GNN）正确标"方法论可继承-技术作废" ✅ |

### 关键发现（pilot 过程中暴露的）

1. **B 维度最丰富**（21 条，占 37%）：多源叠加（导师批注 + 8 维 rubric + 证伪表 + 引用质量），印证 R002 关键洞察 1。
2. **跨形态跨维度映射成立**：D-302 的 material_form 是"失败案例"但映射 D 维度（S003 的 11 轮失败教训→D 优化建议）；scan-template L27"一条原文可映射多个维度/形态"设计预期被证实。
3. **C 维度 good_example 与 diff 双字段兼容**：命名方法论形态只填 good_example（original/rewritten 留空），diff 形态填 original/rewritten（good_example 留空）——模板用"diff 必填；纯范例可只填 good_example"覆盖，无歧义。
4. **agent 落盘阻塞**：Explore agent 无 Write 工具，后续全量蒸馏对话（B/C）需主对话落盘，或换用有 Write 的 agent 类型（已在 H002 记）。
5. **R002 行号待补项已大部分校准**：pilot 12 份覆盖的素材源行号已补齐，剩余 61 条素材源的行号待全量蒸馏时补。

## 决策引用

- 无新建 D###（pilot 结果确认 D002 契约字段 + scan-template 设计有效，无需新决策）
- D002：下游接口契约字段（本 session 验证其可填充性——PASS）
- D003：排除 thesis-materials（未触及）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（pilot 验证是 H001 明确的对话 A 目标，未越界）
- 未修改任何原始日志（只读蒸馏，不变量 1 守住）
- 未实施 paper-eval S033（只产素材，不变量 4 守住）

## 后续

### 立即（对话 B，H002 交接目标）
A+B 维全量蒸馏。A 维 10 源 + B 维 22 源，派 3 agent（A 全量 1 agent + B 拆 2 agent），2 轮（每轮 ≤15min）。产出 distilled/A-pain-points.md + distilled/B-eval-criteria.md 草稿。

### pilot 产出的 56 条如何处理
**并入全量蒸馏**——对话 B 的 A/B agent 在 pilot 56 条基础上继续补全（pilot 的 A6 B21 直接并入，不重做）。pilot-agent1/2/3.md 作为 A/B 维的"已提取部分"保留，对话 B agent 参考其字段格式继续。

### 待回填 R002（已知债务）
pilot 校准的行号（B1/B3/C1/D4/B12 等）应回填 R002-scan-findings.md，避免对话 B/C agent 用错行号。建议对话 B 开工前主对话先回填，或对话 D 统一处理。
