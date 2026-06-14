# sim-preflight Skill CHANGELOG

> skill 演进记录。新增/修改规则必须追加一版。
> 触发证据来自 `rules/usage-log.md` 和 `rules/audit-skill.md`。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

---

## [2026-06-14] v1.1.0

### 重大改动

**架构重构**：从单文件 198 行拆为索引 + 子文件结构（10 文件 → 13 文件 601→~750 行）。

新增子文件结构：
- `scenarios/{run,add,write,recover}.md` — 4 个场景流程
- `rules/{constraints,tech,doc-discipline,interrupt,archive}.md` — 5 个规则类别
- `rules/usage-log.md` — 使用日志（新增）
- `rules/audit-skill.md` — 月度审计（新增）
- `CHANGELOG.md` — 版本管理（新增）

### 修复的 CRITICAL 问题（5 个）

来自 architect 审查 + 2 个 agent 推演发现的实操漏洞：

- **write.md 假示例数字**：删 `C-012 | BER=0.016%`（与 CONCLUSIONS.md 真值 `2.33e-4` 不符），改为格式占位 `{文件:行号} | {指标}={值}`。加警告"示例为格式占位，禁止照抄"。
- **add.md 模板字段名错**：`"audit"` → `"audit_flag"`（params.py 真实字段名）。模板从顶层 `SimulationConfig` 改为嵌套子模型示例（如 `SystemParams`）。加校验命令"新字段使对应级别计数 +1"。
- **interrupt.md grep 白名单漏检**：删除 `grep -v "params.py\|import"` 白名单——params.py:287-294 的 `default_factory=lambda: KFQParams(sigma2_turb=1e-6)` 是 CRITICAL 硬编码。改用精确判据（lambda 里硬编码 CRITICAL 参数 = 违规）。
- **archive.md grep 误判全公式**：原 `formulas-index.md` 引用次数判据失效（索引文件每公式天然引用 1 次）。改为基于"代码 + 论文正文"引用次数：`comm -23 all_formulas used_formulas`。扩展 grep 模式 `F[0-9]+(\.[0-9]+)?` 兼容 F1/F3.1/F4.15 等格式。
- **recover.md 状态机制从未触发**：grep `[中断]` 在专题目录全 0；decisions.md/verifications.md 从未建立。加 grep 空 fallback（不中断，提醒用户）+ decisions.md 不存在时主动创建（治理机制启动）。

### 修复的中等问题（5 个）

- **SKILL.md 决策树缺 params.py 分支**：加"改 params.py（加字段 / 改 CRITICAL 参数）→ 场景 A 必读特例 + 场景 B 新参数模板"
- **SKILL.md 决策树缺指令模糊反问**：加 Step 0 反问清单（算法名/参数集/操作类型）
- **add.md 缺"算法已部分实现"识别**：加 grep 检查清单，按结果选 4 种流程（已完整/部分实现/参数占位/全新）
- **dB vs 线性单位决策表**：加到 add.md，规则"计算时用线性，存储可存 dB 但必须 unit=dB"
- **孤儿参数 AuditFlag**：加到 add.md，加了字段但暂无代码用 → 标 DEAD（不是 WARNING）

### 日志机制（B 方案）

- 新增 `rules/usage-log.md`：使用日志格式 + 写入时机
- 新增 `rules/audit-skill.md`：月度审计命令 + 报告模板
- SKILL.md §5 加日志验证命令
- 每个场景"改"步骤加"写使用日志"行
- interrupt.md 中断时双写（session note + usage-log）

### 自检 agent 改进（P6/M5 防护）

- 主选从 `executor` 改为 `critic`（executor 与主对话同源，复现 M5）
- 备选 `verifier`
- 禁用 `explore`（只读）/ `code-reviewer`（同源）/ `executor`（同源）
- 自检 prompt 强制要求"独立跑更宽的 grep，不信 skill 给的 grep"

### 维护原则

SKILL.md §6 加维护原则段：
- skill 演进必须基于使用日志证据
- 示例数字必须格式占位（不抄真实数字）
- 新增规则必须更新 CHANGELOG
- 月度审计 → 改 skill → 写 CHANGELOG

### 触发证据

- architect agent 理论审查报告（按 P1-P7/F1-F3/M1-M6）
- general-purpose agent 5 个真实场景实操推演
- critic agent 5 个边界场景 + 5 个长期可维护性推演
- 真实文件 grep 验证（CONCLUSIONS.md:128, params.py:287-294, formulas-master.md:2487）

---

## [2026-06-13] v1.0.0

### 初始版本

- 单文件 198 行（SKILL.md）
- 4 用户硬约束（不分 INVARIANT/DECIDED）
- 3 大场景流程（A 跑实验/B 加算法/C 写论文）
- 通用文档纪律（三层限制/拥有者/约定变更）
- 关键技术规则 + AuditFlag 四级行动
- 7 条遗漏中断清单
- 快速自检命令
