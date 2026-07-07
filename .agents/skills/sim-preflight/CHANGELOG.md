# sim-preflight Skill CHANGELOG

> skill 演进记录。新增/修改规则必须追加一版。
> 触发证据来自 `rules/usage-log.md` 和 `rules/audit-skill.md`。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/)。

---

## [2026-07-07] v1.2.0

### 重大改动：搬家 + 参数真相源统一补强

**位置变更**：skill 从 `.claude/skills/sim-preflight/` 搬到仓库内 `.agents/skills/sim-preflight/`（与 `.claude/skills/` 平级，仍仓库级仅本项目可见）。原 `.claude/skills/sim-preflight/` 保留但不再维护，以新位置为真相源。

### 新增规则：参数真相源统一（T3 精确缺口补强）

- **新增 `rules/param-source.md`**：覆盖 T3 没管住的两个失败模式
  - **失败模式 A**：函数默认参数固化（`def f(..., lw=LASER_LW)`，import 时冻结，patch 模块属性无效）
  - **失败模式 B**：跨模块同义常量派生（`_b11_params.CLW_B11` vs `params.LASER_LW`，同物理量两个数值源）
  - 含自检命令 + 前置门控 checklist + 与 T3/TL-13 关系对照表
- **SKILL.md §1 核心 5 条第 3 条扩展**：在"参数溯源"后加"同一物理量跨场景必须从 params.py 单一字段读"
- **SKILL.md §1.5 新增 C1-C5 实验设计扎实性自检**：从 `REVIEW_NOTES.md` §二 抽取的通用清单（参数扫描/指标对齐/baseline档级/文档一致/场景论证），跨方向通用
- **interrupt.md 加第 9 条**：参数真相源分裂中断（函数默认参数固化 / 跨模块同义常量 / `__defaults__` monkey-patch 三种症状）
- **SKILL.md §3 子文件索引**：新增 `rules/param-source.md` 行
- **SKILL.md §5 快速自检命令**：加参数真相源审计 grep

### 触发证据（来自本次根因，已 grep + raw BER 核实）

载波同步 NDA-ML 项目发现：激光线宽（combined linewidth）这一个物理量，AWGN 路径从 `simulator/_b11_params.py:CLW_B11=500kHz` 派生 `SIGMA2_P_B11`，湍流路径从 `common/_config.py:LASER_LW=10kHz` 派生。**两个源差 50 倍**，导致：

1. **C4 违反**（场景描述与参数不一致）：简报写"激光线宽 500kHz"对 AWGN 成立、对湍流错（实为 10kHz）——命中导师 2026-07-07 意见 4
2. **C1 违反**（单点当通用）：500kHz 单点结论被误当通用，500kHz 湍流下 NDA 崩塌（−0.82dB）被当成方法缺陷
3. **raw BER 核实**：500kHz 湍流三场景 oracle（genie-aided）都打不到 HD-FEC 3.8e-3 → 是物理不可达 + 参数组合不真实（500kHz@2.5GBaud 的 ΔνTs=2e-4，是 Du 500kHz@25GBaud 的 10 倍 PN），非纯算法问题

**子 agent 文献调查佐证**：Valjus 2025 (sat.1553) §4.2 锁定星地 FSO 线宽典型区间 0.1–1MHz@28GBaud（ΔνTs≈10⁻⁶–10⁻⁵），2.5GBaud 配 ECL（1-100kHz）才是典型，500kHz@2.5GBaud 是极端压力测试非典型。

### 影响的规则编号

- SKILL.md §1（核心 5 条第 3 条扩展）
- SKILL.md §1.5（新增 C1-C5）
- SKILL.md §3（子文件索引加 param-source.md）
- SKILL.md §5（自检命令加参数真相源审计）
- rules/param-source.md（新增）
- rules/interrupt.md（第 9 条）

### 不改的部分

- 不改任何仿真代码（`common/`、`simulator/`、`params.py`）——参数修复 + 重跑放下轮
- 不改 T3 原文（只扩展不替换）
- 不改其他 rules（archive/audit-skill/doc-discipline/tech/usage-log）

---

## [2026-06-14] v1.1.1

### 修复（流程跳步缺口）

- **SKILL.md 加阶段边界声明（§0）**：明确本 skill 只管 Execute 阶段，列出不该用本 skill 的 4 个前置阶段（方向探索/Groundwork前置/MVE/Contract）+ 常见跳步警告（候选筛出≠可MVE）
- **触发证据**：用户指出"总想上来进 MVE，不按 CLAUDE.md 步骤来"。grep 确认 skill 0 处提 MVE/可行性/前置，4 场景全 Execute
- **影响**：封住 skill 盲区，防止 Execute 工具被误用于方向探索/MVE 前置阶段。D001/handoff/topic-index 同步补"筛完→Groundwork前置→合规MVE→Contract→Execute"链

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
