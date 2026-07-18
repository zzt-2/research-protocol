# Handoff: pilot 验证 + 全量蒸馏启动

> 来源: S001 / R001 / R002 | 交接目标: 新对话续接，设计扫描模板 + pilot 12 份验证可合并性
> 文件名: H001-pilot-and-distillation.md
> 2026-06-15

## 已完成边界

**专题**：`2026-06-14-proposal-log-distillation`（开题报告写作日志蒸馏）。定位：paper-eval / paper-write（均在 thesis-platform repo）的**上游真实素材生产者**，只产出素材不实施下游。

**已完成**：
1. **专题基础设施**：registry 登记 + topic-index + S001（开专题讨论）+ R001（扫描方法论+七漏点+日期约束）+ decisions D001-D003
2. **下游接口契约锁定（D002）**：与 thesis-platform 消费方对齐，四维产出文件 + 每条字段形态（见下"接口变更"）
3. **粗扫（3 agent）+ 细扫补盲区（3 agent）= 6 agent 全覆盖**：thesis-direction-pivot(98) + 毕设/(主规范+角落) + 三写作专题 + 根目录 + 4 处盲区（citation-verification / projects·thesis-figures·thesis-fso / stages / _archive 旧方向）
4. **R002 素材源索引（661 行，73 条素材源）**：A10/B22/C22/D19，每条带 来源 agent + file:line 指针 + 维度 + 价值 + 日期有效性 + 下游字段可填性 + 7 条关键洞察 + pilot 12 份候选

**当前状态**：扫描覆盖完整，素材源索引齐备，**待 pilot**。

## 不要做什么

1. **不修改原始日志**（只读蒸馏，原文不动）—— 不变量 1
2. **不直接实施 paper-eval S033**（S033 等素材产出后由 paper-eval 专题决定推进）—— 防越界，不变量 4
3. **不靠文件名/元信息跳过阅读**（用户明确否决偷懒路径——日志多样性高，文件名看不出内容深度）—— 不变量 3
4. **不扫 stages/thesis-materials.md**（用户 2026-06-15 判定"很旧别管"，见 D003；细扫B 曾误判为 paper-write 蓝图，已否决）
5. **不扫 thesis-platform repo 日志**（日志源在 research-protocol）
6. **主对话不 WebSearch / webReader**（用户全局硬规则，会上下文爆炸）
7. **不重复已扫内容**：6 agent 已扫完全部写作过程类 .md，R002 已索引。pilot/蒸馏是从 R002 指针**回挖具体内容**，不是重新扫描
8. **不一次全量蒸馏**：300 文件直接蒸馏会 M1 管道断裂 + 上下文爆炸。必须 pilot 先验证模板（分层试错法 P3）

## 必读（按优先级）

1. **`R002-scan-findings.md`**（本专题，661 行）—— **素材源索引，pilot/蒸馏的输入**。73 条素材源按 A/B/C/D 四维 + file:line 指针。pilot 12 份候选在末尾"pilot 建议"表。关键洞察 7 条在"关键洞察"段
2. **`topic-index.md`**（本专题）—— 不变量 4 条 + 范围边界 + 产出落点表（四维 distilled 文件 + 字段形态）
3. **`decisions.md`**（本专题）—— D001（定位/范围/repo/维度）+ D002（下游契约 + C/D 落点修正）+ D003（排除 thesis-materials）
4. **`R001-material-value-inventory.md`**（本专题）—— 扫描方法论（四个问题）+ 七漏点 + 日期约束（pivot 2026-05-29）

## 接口变更（无代码改动，下游契约字段）

下游消费方（thesis-platform paper-eval S033/S025-S028、paper-write）已锁定四维产出文件 + 字段形态。**全量蒸馏的产出必须能填进这些字段**（防 M1 管道断裂）：

```yaml
A_pain_points:
  file: distilled/A-pain-points.md
  consumer: paper-eval S033 改写
  fields: {来源指针, 痛点, 归类[检测器ID|新维度], 对S033哪个待讨论项有输入}

B_eval_criteria:
  file: distilled/B-eval-criteria.md
  consumer: paper-eval S025-S028 评估盲区
  fields: {批注原文指针, 批评点, 是否已覆盖[是→哪条rubric|否→新维度]}

C_rewrite_fewshot:
  file: distilled/C-rewrite-fewshot.md
  consumer: paper-eval S033 改写 few-shot
  fields: {原文指针, 好在哪, 适合做哪个改写目标的few-shot}

D_writing_workflow:
  file: distilled/D-writing-workflow.md
  consumer: paper-write 管线设计（手搓流程逆向工程）
  fields: {手搓步骤清单, vs paper-write现状, 优化建议}
```

**跨 repo 路径风格**：thesis-platform 引用本专题产出用 `/mnt/d/code/study/research-protocol/.sessions/2026-06-14-proposal-log-distillation/distilled/`（WSL 路径，**禁用 `D:\` Windows 风格**——WSL agent 读不到）。

## 失败数据附录

- **细扫B 首次 API 529 限流**：glm 服务端过载（`open.bigmodel.cn`），0 token 0 调用，根本没跑起来。重启即恢复。**经验**：派 background agent 遇 529 直接重启同 prompt，不用等
- **D001 否决"文件名偷懒"方案**：曾提议用文件名+元信息建索引跳过部分阅读。用户否决（原话见 S001）。**全量实读是硬约束**
- **D001 否决"专题落 thesis-platform"**：曾基于"下游在 thesis-platform"倾向落那边。修正：日志源全在 research-protocol

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| thesis-materials"中文≥10篇/预印本率≤30%"引用质量门槛无替代源 | 排除项应无遗漏 | B11 标"待补"（原源 thesis-materials 已排除，D003） | 全量蒸馏 B 批时若仍未找到替代源，该条降级或标"原源已排除" |
| 部分素材源行号待 pilot 补（粗扫2/粗扫3 的条目） | file:line 指针应精确 | R002 标"行号待 pilot 补" | pilot 实读时校准 |
| 次一级产物（规则库/检测器/few-shot/rubric/流程蓝图）尚未挖 | 全量蒸馏的产出 | R002 已标位置，未提取内容 | 全量蒸馏 4 批（A/B/C/D）时逐批挖出 |

## 验证阈值（pilot 通过判据）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 扫描模板字段覆盖 | 7 种素材形态（规则清单/批注原话/diff对比/审查rubric/失败案例/命名方法论/工作流蓝图）都能映射到 A/B/C/D 契约字段 | 分层试错法 P3（最小切片） | 未测 |
| 跨 agent 可合并性 | 不同 agent 提取的同类素材字段格式一致，可拼接去重 | 防 M1 管道断裂 | 未测 |
| 回溯指针有效 | 每条提取的素材能通过 file:line 回到原文验证 | 不变量（只读蒸馏需可验证） | 未测 |
| 日期约束执行 | pivot 前（2026-05-29）旧方向素材标"方法论可继承/技术作废" | R001 日期约束 | 未测 |

**pilot 规模**：12 份（R002 末尾"pilot 建议"表，按形态各挑 1-2 份）。**pilot FAIL → 修模板重试，不放大**。

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（4 条：只读不改 / produces 跨 repo / 全量实读 / 不越界实施）
- [ ] 已验证本文件中的至少 3 条关键事实声称（建议验证）：
  - [ ] R002-scan-findings.md 确为 661 行、73 条素材源（A10/B22/C22/D19）、占位符 BATCH_NEXT 已清空
  - [ ] decisions.md 含 D003（排除 thesis-materials）
  - [ ] D002 下游契约字段形态与 topic-index"产出落点"表一致
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with（无依赖、无冲突）
- [ ] 已确认当前范围未违反"明确不含"（stages/thesis-materials.md 不扫、thesis-platform 日志不扫、原文不改）

## 下一轮

### 总览：后续切 4 个对话接力（一个对话做不完）

300 文件蒸馏不可能一个对话做完（用户全局规范：单对话步骤上限 3 + 分层试错 P3 最小切片）。后续切 4 个对话，每个结束写新 H### 接力：

| 对话 | 目标 | 步骤数 | 产出 | 接力 |
|------|------|--------|------|------|
| **A（pilot，本交接目标）** | 设计扫描模板 + pilot 12 份验证可合并性 | 3 | 冻结模板 + pilot 提取 + PASS/FAIL | → H002 |
| B | A+B 维全量蒸馏 | 2-3 | distilled/A + distilled/B 草稿 | → H003 |
| C | C+D 维全量蒸馏 | 2-3 | distilled/C + distilled/D 草稿 | → H004 |
| D | 四批合并去重 + 交叉验证 + 跨 repo produces | 2 | 四维 distilled 定稿 + 次一级产物 | 闭环 |

### 对话 A 详细（新对话第一个要做，=本交接目标）

**步骤 1（主对话，不派 agent——要拍板冻结）**：设计扫描模板。把 R002 7 种素材形态映射到 D002 契约字段。产出 = 模板文档（每条素材字段 schema + 1 条填写示例）。要点：每条 = 一个契约字段实例；必带 file:line 回溯；必带日期/方向标注（pivot 2026-05-29 前后）；跨 agent 同形态可拼接（防 M1）。

**步骤 2（3 agent 并行，各 4 份，每 agent ≤15min）**：用步骤 1 冻结的模板，从 R002 指针回挖。**形态故意不重叠分给各 agent**——验证两层可合并性：agent 内同形态 2 份能拼 + 跨 agent 字段 schema 统一。

| agent | 负责形态 | pilot 文件（R002 指针） | 验证点 |
|-------|---------|----------------------|--------|
| agent-1 | 规则清单 + 批注原话 | C1 R011 / D4 innovation R1-R7 / B1 advisor 批注 / B3 S001 四底线 | 同形态 2 份可拼 |
| agent-2 | diff 对比 + 审查 rubric | C2 Ch2-reviews diff / C6 R003 Before→After / B5 Ch2-reviews 8 维 / B8 CONCLUSIONS 安全等级 | 同形态 2 份可拼 |
| agent-3 | 失败案例 + 命名方法论 + 工作流蓝图 | B9 S024 证伪 / B12 AI 编造 DOI / C10 cnki-survey 章节命名 / D1 S003 L1-L3 | 3 形态 schema 统一 |

调度：3 agent 一批并行（用户上限 3），agent 内部串行读 4 份。**pilot 目的不是产出素材，是验证模板**——重点看能不能拼，不是挖多全。

**步骤 3（主对话）**：合并 3 agent 产出 → 检查可合并性（同形态字段一致？能拼去重？回溯指针有效？日期标注到位？）→ PASS/FAIL。PASS → 写 H002 交接对话 B；FAIL → 修模板重跑步骤 2（分层试错 P2：连续 2 轮 FAIL 强制截断，回主对话找模板根因）。

### pilot PASS 后的后续对话框架（到时各自详排，此处只给骨架）

- **对话 B（A+B 蒸馏）**：A 维 10 源 + B 维 22 源。派 3 agent：A 全量（10 源，1 agent）+ B 拆 2 agent（各 11 源）。B 22 源单 agent 装不下 → 2 轮（每轮 ≤15min）。产出 distilled/A + distilled/B 草稿。
- **对话 C（C+D 蒸馏）**：C 22 源 + D 19 源。派 3 agent：C 拆 2 + D 1，2 轮。产出 distilled/C + distilled/D 草稿。
- **对话 D（合并交付）**：四批合并去重 + 派 **verifier agent 交叉验证**（生成与审查分离，分层试错 P6，不自审自验）+ 跨 repo produces 声明。产出四维 distilled 定稿 + 次一级产物（已知债务表记了位置）：
  - 写作规则库 / paper-eval 检测器规格 / few-shot 语料库 / 评估 rubric 体系 / paper-write 流程蓝图

### 子 agent 调度纪律（每对话都守）

- 一次最多 3 个并行（用户全局规范，不超发）
- 单 agent ≤15min（CLAUDE.md），装不下就拆批不堆任务
- 子 agent 从 R002 指针回挖具体内容，**主对话不读 300 原始文件**（主对话读 R002 661 行 OK）
- 主对话职责：模板设计 / 判据评估 / 合并 / 拍板；不负责大文本逐行消化
- 生成与审查分离（P6）：蒸馏对话（B/C）产出，对话 D 用独立 verifier 验证，不自审
