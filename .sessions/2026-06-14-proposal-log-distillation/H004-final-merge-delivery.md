# Handoff: C+D 维完成 → 四批合并交付（对话 D，最终）

> 来源: S004（C+D 维全量蒸馏） | 交接目标: 新对话续接，四批合并去重 + verifier 交叉验证 + 最终交付
> 文件名: H004-final-merge-delivery.md
> 2026-06-15

## 已完成边界

**专题**：`2026-06-14-proposal-log-distillation`。

**累计已完成（pilot + 对话 A/B/C）**：
- **scan-template.md FROZEN**（7 形态→4 维 schema）
- **四维全量蒸馏完成**：累计 **212 条**（A28 B56 C62 D66），覆盖 R002 全部 73 条素材源
  - distilled/A-pain-points.md（28 条，A1-A10 全覆盖）✅
  - distilled/B-eval-criteria.md（56 条，B1-B22 全覆盖）✅
  - distilled/C-rewrite-fewshot.md（62 条，C1-C22 全覆盖）✅
  - distilled/D-writing-workflow.md（66 条，D1-D19 全覆盖）✅
- 10 个原始 yaml 文件（pilot 3 + batchB 3 + batchC 4）全部落盘
- 确定性 grep 验证累计 PASS：id 分区/枚举/行号/日期/回溯/覆盖 6 项

**当前状态**：四维契约草稿全部就位。**下一步 = 对话 D（四批合并交付，最终）**。

## 不要做什么

1. **不修改原始日志**（只读蒸馏）—— 不变量 1
2. **不直接实施 paper-eval S033** —— 不变量 4（对话 D 只做素材交付，S033 由 paper-eval 专题决定）
3. **不重做已蒸馏的 212 条**：四维草稿已就位，对话 D 只做合并去重+验证+交付，不重新提取
4. **不扫 stages/thesis-materials.md**（D003）
5. **不扫 thesis-platform repo 日志**
6. **主对话不 WebSearch / webReader**
7. **不自审**（P6 原则）：对话 D 的 verifier 必须是独立 agent，不能由蒸馏产出的 agent 自审
8. **不修改 scan-template.md**（已 FROZEN）

## 必读（按优先级）

1. **四维契约草稿**（本批最终交付物的基础）：
   - `distilled/A-pain-points.md`（28 条 + 分类索引 + S033 映射 + 已知限制）
   - `distilled/B-eval-criteria.md`（56 条 + 已有 rubric 参照系 + 新维度索引 + S033 映射）
   - `distilled/C-rewrite-fewshot.md`（62 条 + 分类索引 + S033 映射）
   - `distilled/D-writing-workflow.md`（66 条 + step_group 索引 + paper-write 设计输入映射）
2. **10 个原始 yaml 文件**（verifier 交叉验证时回溯用）：distilled/pilot-agent{1,2,3}.md + distilled/batchB-agent{A,B1,B2}.md + distilled/batchC-agent{C1,C2,D1,D2}.md
3. **`scan-template.md`**（FROZEN，verifier 校验字段合规性基准）
4. **`topic-index.md`**（不变量 + 范围边界 + 产出落点表）
5. **`decisions.md`**（D001-D003）
6. **`S002/S003/S004`**（pilot/对话B/对话C 全过程 + 关键发现 + 已知语义近邻组）

## 接口变更（本轮新增产出）

```yaml
batchC_outputs:
  - file: distilled/batchC-agentC1.md  # C-401~421
  - file: distilled/batchC-agentC2.md  # C-501~524
  - file: distilled/batchC-agentD1.md  # D-401~429
  - file: distilled/batchC-agentD2.md  # D-501~525

contract_drafts_complete:
  - file: distilled/C-rewrite-fewshot.md  # C 维 62 条草稿
    status: 草稿（对话 D verifier 定稿）
  - file: distilled/D-writing-workflow.md  # D 维 66 条草稿
    status: 草稿（对话 D verifier 定稿）

all_four_dimensions_ready: true  # A/B/C/D 四维草稿全部就位，212 条
```

下游消费方契约（D002）四维草稿全部就位，等待对话 D 合并去重+定稿。

## 已知债务（对话 D 必须处理）

| 债务 | 原则 | 当前状态 | 处理方式 |
|------|------|---------|---------|
| 四维语义近邻组未合并 | 同语义条目应合并 | 已在四维草稿索引段标注（A 1组/B 3组/C 3组/D 3组） | 对话 D verifier agent 合并 |
| thesis-materials 引用质量门槛无替代 | 排除项无遗漏 | B11"待补" | 对话 D 标"原源已排除"或降级 |
| 跨 repo produces 声明未写 | D002 契约要求 produces | 四维草稿在 research-protocol 内，thesis-platform 引用路径未声明 | 对话 D 写 produces 声明 |
| 次一级产物未挖 | 全量蒸馏的产出 | R002 已标位置，未提取内容 | 对话 D 四批合并时挖（规则库/检测器/few-shot/rubric/流程蓝图） |
| R002 行号回填未完成项 | file:line 精确 | pilot 10源+对话B 3源+对话C部分已回填；对话C覆盖的 C/D 源行号部分回填 | 对话 D 统一回填或标"已校准见 batchC 文件" |

## 验证阈值（对话 D 产出验收）

对话 D 产出最终交付物（四维定稿 + produces 声明 + 次一级产物）后，主对话用确定性 grep + verifier 验收：

| 验证项 | PASS 标准 | 历史通过率 |
|--------|----------|-----------|
| 四维合并去重无冲突 | 语义近邻组合并后无重复 id/无重复主旨 | 未测 |
| 字段合规性 | 100% 匹配 FROZEN schema | pilot+对话B+C 100%（212/212） |
| source_ref :line | 100% 带行号 | 100%（212/212） |
| verifier 交叉验证 | 独立 verifier agent 抽查 ≥10 条回溯原文，≥90% 有效 | 未测（P6 不自审） |
| produces 声明 | thesis-platform 可按声明路径访问四维文件 | 未测 |
| 次一级产物覆盖 | 规则库/检测器/few-shot/rubric/流程蓝图五类至少各 1 份 | 未测 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 不变量段落（4 条）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] distilled/ 下确有四维草稿文件（A/B/C/D），合计 212 条
  - [ ] distilled/ 下确有 10 个原始 yaml 文件（pilot 3 + batchB 3 + batchC 4）
  - [ ] R002 全部 73 条素材源已被四维覆盖（各维"已知限制"段的覆盖确认表）
- [ ] 已检查 _registry.yaml（无依赖无冲突）
- [ ] 已确认范围未违反"明确不含"

## 下一轮（对话 D 详细）

### 目标
四批合并去重 + verifier agent 交叉验证（P6 不自审）+ 跨 repo produces 声明 + 次一级产物挖掘 + 最终交付。

### 步骤

**步骤 1（主对话）**：verifier agent 派遣。派 1-2 个独立 verifier agent（非蒸馏产出的 agent），对四维草稿做交叉验证：
- 抽查 ≥10 条 source_ref 回溯原文（跨四维）
- 检查语义近邻组合并必要性（A 1组/B 3组/C 3组/D 3组）
- 验证 is_covered 判定一致性（B 维 17 条"是"是否真映射已有 rubric）

**步骤 2（主对话）**：合并去重。根据 verifier 反馈，合并语义近邻组，更新四维草稿为定稿。

**步骤 3（主对话）**：次一级产物挖掘。从 212 条提取五类次一级产物：
- **规则库**（A 痛点 → 检测器规则化，如 AI 痕迹 5 类检测器）
- **检测器**（A/B 可机化的检测逻辑，如"回指句检测""括号章节号检测"）
- **few-shot 集**（C 的 good_example 按改写目标聚类）
- **rubric 集**（B 的 is_covered=否 的 new_dimension 聚合）
- **流程蓝图**（D 的 step_group 聚合为 paper-write 管线设计）

**步骤 4（主对话）**：跨 repo produces 声明。写 produces 声明文件，thesis-platform 可按声明路径访问：
- 四维定稿路径（WSL 风格 /mnt/d/...）
- 次一级产物路径
- 消费方式说明（按 id 到源文件取 yaml / 按索引检索）

**步骤 5（主对话）**：最终交付 + 关专题。更新 topic-index 标"完成"，registry status 改"completed"，写 S005 最终 session note。

### 调度纪律
- verifier 必须独立（P6 不自审）
- 不重做 212 条（只合并去重+验证+交付）
- 不实施 S033（只产素材）
- 一次最多 3 并行

### verifier 技术注意事项（pilot/B/C 踩过的坑，压缩后易忘）

1. **PowerShell 中文路径假 MISSING**：`Test-Path '毕设\...'` 在 cmd 调 PS 时因 GBK 读 UTF-8 源会返回 false（假象）。验证 source_ref 回原文时，**禁用 Test-Path，改用 `(Get-Content -Encoding UTF8)[行号]` 直接读行**——能读到就是存在。或用 Glob `Get-ChildItem -Recurse -Filter`。本次 R002 的中文路径（毕设/正文/、毕设/写作材料/ 等）全部真实存在，Test-Path 报 MISSING 是编码问题。
2. **行号是段落锚点非精确行**：蒸馏 agent 取段落/表格起始行作 source_ref，回溯时该行往下看 3-8 行才是 original_quote 关键词所在。判定"有效"的标准是**该行 ±8 行内能找到 original_quote 的关键词**，不是精确命中。pilot 抽查 5 条中 4 条是锚点（有效），对话 B/C 抽查多为精确命中。容忍 ±8 行偏差。
3. **source_ref 路径风格**：全部用 WSL 风格 `/mnt/d/code/study/research-protocol/...`。verifier 读文件时转成 Windows 路径 `D:\code\study\research-protocol\...`（把 `/mnt/d/` 换 `D:\`，`/` 换 `\`）。
4. **R002 已回填的路径修正**（本轮补的，verifier 不用再查）：
   - A2 = `毕设/开题报告/ai-trace-report.md`（非毕设根）
   - B4 = `advisor-brief.md` + `advisor-briefing-2026-05-30.md` 两个文件（非 advisor-briefing.md）
   - D14 = `S003-methodology-reset-and-research.md`（非 -reset.md）
   - 其余 pilot/B/C 校准的行号（B1/B3/B9/B12/C1/C5/C10/D1/D2/D4/A8/B18/B19）均已回填 R002 对应条目

### 语义近邻组「合并 vs 互补」判断指南（防止 verifier 误合并丢信息）

四维草稿"已知限制"标了 10 组语义近邻，但**不是都要合并**。判断标准：主旨相同且信息冗余→合并；主旨相关但信息互补→保留两条+加交叉引用。逐组判断如下：

**应合并（3 组，真冗余）**：
- B 维 `B-301 + B-511`：都讲"压力测试 FAIL→贡献证伪"，B-511 显式引用 B-301 覆盖的 X-01~X-09，信息重叠→合并为一条，covered_by 指向 B-301
- C 维 `C-102 + C-410 + C-413`：都讲"综述先扬后抑模式"，C-102 是抽象规则、C-410/C-413 是新旧方向实例→合并为"规则+2 实例"一条
- D 维 `D-405 + D-512`：都讲"确定性 grep 数字审计"，D-405 是三步法之一、D-512 是 TL-21 完整版→合并，留 D-512 为主、D-405 作 step 引用

**应保留互补（7 组，勿合并）**：
- A 维 `A-101 vs A-401`：A-101 讲 AI 5 大缺陷**根因**（自回归机制），A-401 讲 5 类**严重度量级**（9/8/11/4/12）→互补，加交叉引用
- B 维铁律族 `B-204/404/205/405`：4 条铁律各自独立规则（回指句/交叉引用/参数解释/符号重用）→保留 4 条，合并为"铁律集合"索引但正文独立
- B 维增益真实性族 `B-301/302/306/401/406/407`：6 条覆盖不同维度（压力测试/基线公平/增益归因/公平性三步法/种子数/诚实自评）→保留，合并为"增益审查链"索引
- B 维引用可靠性族 `B-303/408/409/412/413`：5 条覆盖不同层级（DOI/4维rubric/内容匹配/学术诚信4条/DOI验证）→保留，合并为"引用可靠性链"索引
- C 维句式体系族 `C-101 vs C-507`：C-101 是 R011 的 8 类句子功能标注，C-507 是 S004 的 DEF/CLAIM/EVAL/TRANS 标注法——**两套不同标注体系**→互补保留
- C 维符号参数族 `C-402 vs C-518/519`：C-402 讲参数解释**格式**铁律，C-518 讲符号**消歧**策略，C-519 讲符号**管理**5建议→互补保留
- D 维验收门族 `D-303 vs D-429`：D-303 讲 S003 的**分层**检查（L1句子/L2段落/L3全局），D-429 讲附录A 的 **17 项 grep 清单**→互补，合并为"验收门（分层+清单）"复合引用

### 专题完成判据
对话 D 完成后，专题 `2026-06-14-proposal-log-distillation` 达成原始目标：从开题写作日志蒸馏四维素材，跨 repo produces 给 thesis-platform。registry status → completed。
