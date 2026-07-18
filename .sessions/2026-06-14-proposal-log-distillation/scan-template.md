# 扫描模板（SCAN TEMPLATE）— pilot 已冻结

> 2026-06-15 | 对话 A 步骤 1 产出 | 状态：**FROZEN**（pilot 用本模板）
> 关联：D002（下游契约字段）/ R002（素材源索引 73 条）/ topic-index（产出落点表）
> 不变量：① 只读不改原文 ② 全量实读 ③ 每条带 file:line 回溯 ④ 跨 agent 可合并

## 设计目标

把 R002 的 **7 种素材形态**映射到 D002 的 **4 维契约字段**，保证：
- 每条提取 = 一个契约字段实例（下游能直接填）
- 必带 `file:line` 回溯指针（不变量 3，可验证）
- 必带日期/方向标注（pivot 2026-05-29 前后；技术作废 vs 方法论可继承）
- 跨 agent 同形态产出可拼接去重（防 M1 管道断裂）

## 7 形态 → 4 维映射总表

| # | 素材形态 | 典型来源（R002） | 主映射维度 | 字段 |
|---|---------|----------------|-----------|------|
| 1 | 规则清单 | R011 句式库 / innovation-points R1-R7 | A（痛点归类）+ C（范例） | A-pain / C-fewshot |
| 2 | 批注原话 | advisor-revision 20 批注 / S001 四底线 | B（评估标准） | B-criteria |
| 3 | diff 对比 | Ch2-reviews 前后对比 / R003 Before→After | C（few-shot） | C-fewshot |
| 4 | 审查 rubric | Ch2-reviews 8 维 / CONCLUSIONS 安全等级 | B（评估标准） | B-criteria |
| 5 | 失败案例 | S024 B2 证伪 / AI 编造 DOI | B（批评点）+ A（痛点） | B-criteria / A-pain |
| 6 | 命名方法论 | cnki-survey 章节命名 / figure-composition | C（范例） | C-fewshot |
| 7 | 工作流蓝图 | S003 L1-L3 / PROMPT-001 对话隔离 | D（流程） | D-workflow |

**关键**：一条原文可同时映射多个维度（如 innovation-points v1→v6 既是 A 痛点也是 C 反例）。提取时**按维度拆成多条独立条目**，每条只填一个维度的 schema。

## 四维字段 Schema（FROZEN）

每条提取必须按下表填全字段。字段顺序固定（跨 agent 一致才可拼接）。

### A 维度：`A-pain-points`

```yaml
id: A-{NNN}                    # 全局递增，跨 agent 用前缀区（agent-1: A-1xx, agent-2: A-2xx, agent-3: A-3xx）
source_ref: "{path}:{line}"    # 必填，file:line 回溯指针（WSL 风格 /mnt/d/...，下同）
source_agent: "{粗扫N/细扫X}"   # R002 标的来源 agent
material_form: "{规则清单|批注原话|diff|rubric|失败案例|命名方法论|工作流蓝图}"  # 7 形态之一
date_validity: "{有效|方法论可继承-技术作废|pivot前-部分作废}"  # pivot 2026-05-29
direction: "{当前(FSO)|旧(GNN/路由)}"  # 方向标注
pain_point: "一句话痛点描述"    # 痛点本身（不是原文摘抄，是提炼）
original_quote: "原文关键句（≤50字，带引号）"  # 原文证据，便于回验
classification: "归类[检测器ID|新维度]"
  # 例：检测器ID"翻译腔" / 新维度"创新点措辞敏感性"
s033_input: "对 paper-eval S033 哪个待讨论项有输入（无则填 N/A）"
```

### B 维度：`B-eval-criteria`

```yaml
id: B-{NNN}
source_ref: "{path}:{line}"
source_agent: "{...}"
material_form: "{7形态之一}"
date_validity: "{有效|方法论可继承-技术作废}"
direction: "{当前|旧}"
criticism_point: "批评点（一句话，评估的是什么）"
original_quote: "批注/规则原文（≤50字，带引号）"  # 导师原话优先 verbatim
is_covered: "{是→哪条rubric|否→新维度}"
  # 是→映射到已有 rubric（如"Popper 可证伪性"/"GB7714"/"8 维 R1-R8"）
  # 否→新维度（需命名）
covered_by: "{rubric 名称}"  # is_covered=是 时填；否则 N/A
new_dimension: "{新维度名称}"  # is_covered=否 时填；否则 N/A
```

### C 维度：`C-rewrite-fewshot`

```yaml
id: C-{NNN}
source_ref: "{path}:{line}"
source_agent: "{...}"
material_form: "{7形态之一}"
date_validity: "{有效|方法论可继承-技术作废}"
direction: "{当前|旧}"
original_text: "原文片段（≤80字）"  # ❌原文（被改写的/不好的）
rewritten_text: "改后片段（≤80字）"  # ✅改后（diff 形态必填；纯范例形态可只填 good_example）
good_example: "好写法片段（≤80字）"  # 命名方法论/句式库形态填此项
why_good: "好在哪（一句话）"
fewshot_target: "适合做 paper-eval S033 哪个改写目标的 few-shot"
  # 如"去翻译腔"/"段落衔接"/"避免绝对化"/"章节命名规范化"
```

### D 维度：`D-writing-workflow`

```yaml
id: D-{NNN}
source_ref: "{path}:{line}"
source_agent: "{...}"
material_form: "{7形态之一}"  # 通常=工作流蓝图，但也可能来自失败案例/rubric
date_validity: "{有效|方法论可继承-技术作废}"
direction: "{当前|旧}"
workflow_step: "手搓步骤（一句话，一个 step 一条）"
  # 一个工作流拆成多条，每条一个 step，用 step_group 串
step_group: "{流程组名}"  # 同一工作流的步骤共享 group（如"S003 三轮验证"/"PROMPT-001 对话隔离"）
step_order: N              # 组内顺序（1,2,3...）
vs_paperwrite: "vs paper-write 现状（差异点，无则 N/A）"
optimization: "优化建议（给 paper-write 管线设计）"
```

## 一条填写示例（FROZEN 样例）

来源：R002 A6（innovation-points.md v1→v6）。同一段原文**拆成 2 条**（A + C），演示多维度提取：

**条目 1（A 维度）**：
```yaml
id: A-001
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:93"
source_agent: "细扫A"
material_form: "失败案例"
date_validity: "有效"
direction: "当前(FSO)"
pain_point: "创新点措辞反复迭代 6 版（v1 查表选算法→v5 性能分析框架），根因是'方法'一词在中文学术语境被误解为算法"
original_quote: "v1 查表选算法(否决) → v2 省掉 VV 模块(否决) → v3 解析自适应(否决) → v4 方向级措辞(否决) → v5 性能分析框架"
classification: "新维度'创新点措辞敏感性'"
s033_input: "S033'措辞改写'待讨论项——中文'方法'歧义检测"
```

**条目 2（C 维度，从同段提反例）**：
```yaml
id: C-001
source_ref: "/mnt/d/code/study/research-protocol/毕设/innovation-points.md:104"
source_agent: "细扫A"
material_form: "diff对比"
date_validity: "有效"
direction: "当前(FSO)"
original_text: "拟建立…系统性设计与优化方法，基于性能建模给出分湍流条件的方法选择与参数配置方案"
rewritten_text: "系统性性能分析框架 + 参数设计准则（对标 Petkovic 2023 analytical framework + design criterion 模式）"
good_example: ""
why_good: "分析类贡献用'框架/准则'，算法类才用'方法'——避免中文'方法'歧义"
fewshot_target: "S033'创新点措辞改写'——分析类贡献去'方法'化"
```

## 跨 agent 可合并性规则（防 M1）

1. **id 前缀分区**：agent-1 用 `A-1xx/B-1xx/C-1xx/D-1xx`，agent-2 用 `-2xx`，agent-3 用 `-3xx`。合并时直接拼接，无 id 冲突。
2. **字段顺序固定**：4 维 schema 字段顺序如上，agent 产出必须按序，便于合并脚本逐行对齐。
3. **source_ref 必须可回溯**：每条 `file:line` 必须能 `sed -n '{line}p'` 验证。行号缺失的（R002 标"待补"）pilot 实读时校准补齐。
4. **去重键**：同维度内，`(source_ref + 一句话主旨)` 相同视为重复，合并时留信息最全的一条，另一条记入 `duplicates` 段。
5. **material_form 枚举固定**：7 形态字符串必须完全匹配上表，不允许 agent 自创（否则无法按形态聚合验证）。

## pilot 使用方式

3 agent 各从 R002 指针回挖 4 份，**形态故意不重叠**（H001 步骤 2 表）。每 agent 产出 = 一个 markdown 文件，内含若干 yaml 代码块（每块一条）。主对话合并后检查：
- 同形态 2 份能拼（字段一致）
- 跨 agent schema 统一
- 回溯指针有效（抽查 ≥3 条 `file:line` 回原文）
- 日期/方向标注到位

**pilot FAIL**：任一检查不过 → 修模板（本文件）重跑，不放大到全量（分层试错 P2：连续 2 轮 FAIL 截断回主对话找根因）。
