# 跨 repo PRODUCES 声明 — proposal-log-distillation → thesis-platform

> 2026-06-15 | 对话 D 步骤 4 产出 | 状态：**定稿**
> 本文件是 research-protocol repo 的 `2026-06-14-proposal-log-distillation` 专题向 thesis-platform repo（paper-eval / paper-write）的**产出接口声明**。
> thesis-platform 消费方（paper-eval S025-S028/S033, paper-write 管线设计）按本声明取用素材。

## 产出方信息

| 项 | 值 |
|---|---|
| 产出 repo | `research-protocol`（**单一真相源 SOURCE OF TRUTH**） |
| 产出专题 | `.sessions/2026-06-14-proposal-log-distillation/` |
| 产出状态 | **completed**（2026-06-15 对话 D 定稿，210 条 + 5 类次一级产物） |
| 产出路径基准（WSL） | `/mnt/d/code/study/research-protocol/.sessions/2026-06-14-proposal-log-distillation/distilled/` |
| 路径风格 | **WSL 风格**（`/mnt/d/...`），禁用 `D:\` Windows 风格——WSL agent 读不到 Windows 路径 |

## 物理镜像（D005，2026-06-16）

> ⚠️ **本 distilled/ 目录是单一真相源。thesis-platform 有一份只读镜像。**

- **镜像位置**：thesis-platform repo `/home/zzt/code/thesis-platform/.sessions/distilled/`
- **镜像规则**：
  - research-protocol 是**主**，thesis-platform 是**只读镜像**
  - 内容修改**先改 research-protocol**，再手动 `cp -r` 同步到 thesis-platform
  - thesis-platform 那份**不得直接修改**——要改请回 research-protocol 改完重新拷
  - 两边不一致时以 research-protocol 为准
- **source_ref 指针不改写**：两边 yaml 的 source_ref 都指向 `/mnt/d/code/study/research-protocol/...`（原始日志只在 research-protocol，详见 D005）

## 产出清单（5 个交付文件 + 10 个原始 yaml 回溯）

### 四维定稿（4 个索引文件，210 条）

| 维度 | 文件（WSL 路径） | 条目数 | 下游消费方 |
|------|----------------|--------|-----------|
| A 痛点 | `distilled/A-pain-points.md` | 28 | paper-eval S033 改写（AI 痕迹检测+写作纪律） |
| B 标准 | `distilled/B-eval-criteria.md` | 55（B-511 已并入 B-301） | paper-eval S025-S028 评估盲区 |
| C 范例 | `distilled/C-rewrite-fewshot.md` | 62 | paper-eval S033 改写 few-shot |
| D 流程 | `distilled/D-writing-workflow.md` | 65（D-405 已并入 D-512） | paper-write 管线设计 |

### 次一级产物（1 个聚合文件，5 类产物）

| 产物 | 文件（WSL 路径） | 下游消费方 |
|------|----------------|-----------|
| 检测器集+规则库+few-shot集+rubric集+流程蓝图 | `distilled/secondary-products.md` | paper-eval（检测器/few-shot/rubric）+ paper-write（规则库/流程蓝图） |

### 原始 yaml 回溯（10 个文件，212 条原始记录）

四维定稿是索引，完整 yaml 内容在原始文件。下游按 id 取 yaml 块：

| 文件（WSL 路径） | 含 id 范围 |
|----------------|-----------|
| `distilled/pilot-agent1.md` | A-101~104, B-101~107, C-101~104, D-101~104 |
| `distilled/pilot-agent2.md` | B-201~208, C-201~207 |
| `distilled/pilot-agent3.md` | A-301~302, B-301~306, C-301~306, D-301~308 |
| `distilled/batchB-agentA.md` | A-401~422 |
| `distilled/batchB-agentB1.md` | B-401~417 |
| `distilled/batchB-agentB2.md` | B-501~518（B-511 已并入 B-301，保留供回溯） |
| `distilled/batchC-agentC1.md` | C-401~421 |
| `distilled/batchC-agentC2.md` | C-501~524 |
| `distilled/batchC-agentD1.md` | D-401~429（D-405 已并入 D-512，保留供回溯） |
| `distilled/batchC-agentD2.md` | D-501~525 |

## 消费方式（thesis-platform 如何取用）

### 方式 1：按维度整体取用
下游消费方读对应维度定稿文件（A/B/C/D-*.md），按索引表的分类簇定位条目。

### 方式 2：按 id 取 yaml 块
已知 id（如 `B-301`）→ 查 id 前缀（B-3xx → pilot-agent3.md）→ 在该文件 grep `id: B-301` 取完整 yaml 块。

### 方式 3：按下游需求取次一级产物
- paper-eval S033 要检测器 → `secondary-products.md` §1（检测器集）
- paper-eval S033 要改写 few-shot → `secondary-products.md` §3（few-shot 集）
- paper-eval S025-S028 要评估 rubric → `secondary-products.md` §4（rubric 集）
- paper-write 要生成约束 → `secondary-products.md` §2（规则库）
- paper-write 要管线设计 → `secondary-products.md` §5（流程蓝图）

## 下游接口契约（D002 锁定）

| 维度 | 下游 | 字段形态（每条产出） |
|------|------|---------------------|
| A 痛点 | paper-eval S033 | `{来源指针, 痛点, 归类[检测器ID\|新维度], 对S033哪个待讨论项有输入}` |
| B 标准 | paper-eval S025-S028 | `{批注原文指针, 批评点, 是否已覆盖[是→哪条rubric\|否→新维度]}` |
| C 范例 | paper-eval S033 | `{原文指针, 好在哪, 适合做哪个改写目标的few-shot}` |
| D 流程 | paper-write | `{手搓步骤清单, vs paper-write现状, 优化建议}` |

字段 schema 完整定义见 `scan-template.md`（FROZEN）。

## 已知边界（下游消费注意）

1. **不直接实施下游**：本声明只产素材，下游 paper-eval S033 / paper-write 管线的实施由 thesis-platform 专题决定。
2. **部分条目标"方法论可继承-技术作废"**：A-419~422 / B-415~417 / C-205~207/407~412/506/520~521 / D-517~520 来源是旧方向（GNN/信道均衡/NTN/DRL），技术内容作废但写作方法论可继承。消费时看 `direction` 和 `date_validity` 字段。
3. **B-102 已校准**：is_covered 从"是→Popper"改为"否→学术定位判据"（对话 D verifier 校准，学术定位≠可证伪性）。
4. **合并组保留回溯**：B-511/D-405 虽已并入主条目，原始 yaml 在 batchB-agentB2.md / batchC-agentD1.md 保留供回溯。
5. **stages/thesis-materials.md 排除**（D003）：引用质量 rubric（中文期刊≥10 篇/核心预印本率≤30%）无替代源，R002 B11 标"原源已排除"。其余引用质量由 bib-quality-issues + citation-verification 覆盖。

## 触发重新评估条件

- 下游 S033 / good-examples / paper-write 弃用或大改 → 重评对应维度落点（D002 触发推翻条件）
- 下游消费时发现某合并组需要拆分 → 重评 D004 合并判断
