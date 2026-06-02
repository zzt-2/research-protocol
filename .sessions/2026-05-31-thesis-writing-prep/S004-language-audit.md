# S004: 语言禁忌+事实性审查

> 2026-06-02 | 材料审查 | ✅ 完成

## 目标

对所有毕设材料文件做语言禁忌审查（PROMPT-001 附录C）+ 事实性审查（表述是否贴合最新仿真结果）。

## 背景

PROMPT-007 仿真正确性验证已完成（42 agents, 15 条已确认结论），Phase 4 确定性 grep 审计修了 19 处数字不一致。但用户怀疑仍有遗漏，尤其是：
1. 材料文件中的语言表述是否违反附录 C 禁忌
2. 表述是否贴合最新仿真结论（NMSE 零影响、级联增益修正等）
3. 禁忌本身是否合理（用户质疑"VV平滑窗口"和"信道增益"是否应全局禁止）

## 方法

### 审查阶段（3 个并行 agent，按结论维度分工）

不按文件派 agent（之前尝试失败，agent 太模糊会漏检），而是按**结论维度**派：

| Agent | 负责维度 | SPEC 来源 |
|-------|---------|----------|
| Agent A | Ch3 结论（NMSE/级联/LS/MMSE/预补偿） | verification-report §NMSE, §INV-2 |
| Agent B | Ch4 结论（VV/BPS/DPLL/KF 性能、Nw、种子数） | verification-report §窗口参数, §NMSE vs BER |
| Agent C | 通用禁忌（FPGA/术语/措辞/物理约束） | PROMPT-001 附录C, TERMS.md |

每个 agent 拿到具体 SPEC（含精确数值）+ 必须 grep 的模式列表，搜索 `毕设/` 下所有 `.md`（排除 `verification/`）。

### 禁忌合理性验证（1 个 analyst agent）

用户质疑两个禁忌是否过度纠正。Analyst 检查 TERMS.md 原始理由 + 范文/已发表论文用法后判断：
- **"VV平滑窗口"**：过度纠正（范文丁爽/董凡都用"平滑窗口"）
- **"信道增益"**：部分合理（Ch2 首次定义应用"归一化辐照度"，但全局禁用过激）

### 用户追问：同一篇论文内部是否混用术语

用户问"同一篇论文内会用两种称呼吗"。结论：学术写作规范是**全文统一用一个词**。不同论文可能用不同术语，但同一篇论文应统一。因此：
- 恢复 TERMS.md 中"VV平均窗口"和"归一化辐照度"为全文统一用语
- 补充 section 9 混用速查说明

### 修复阶段（3 个并行修复 agent + 主线程直修）

| Agent | 负责文件 | 修改数 |
|-------|---------|--------|
| 修复 Agent 1 | thesis-framework.md + thesis-status.md | 19 |
| 修复 Agent 2 | material-section-content-cards.md + 03-研究方案.md | 29 |
| 修复 Agent 3 | design-decisions.md + section-outline.md + figure-table-plan.md + thesis-preparation-checklist.md | 13 |
| 主线程 | TERMS.md(4) + formulas-ch4-kf(2) + formulas-ch2(1) + formulas-ch5(1) + section-outline(1) + material-section-content-cards(1) | 10 |

## 发现的问题（~65 条原始，去重后 71 处修改）

### 按类别

| 类别 | 数量 | 典型问题 |
|------|------|---------|
| 旧VV公式虚高数据 | 17 | +14.75/+14.1/+5.9dB（bug产物）→ +0.49~+1.09dB |
| NMSE描述升级 | 14 | <1dB→<0.3dB, 去除-5dB/-10dB虚假阈值 |
| FPGA违规 | 14 | "完成/实现"→"进行/设计分析" |
| 术语违规 | 15 | 联合同步→级联(5), 平滑→平均(6), 信道增益→归一化辐照度(4) |
| 措辞禁忌 | 11 | 首次(5), 证明(2), 显著(4) |
| 过时表述 | 6 | KF范围/弱湍流旧数据/种子数/级联旧数据等 |

### 按文件

| 文件 | 修改数 | 主要问题 |
|------|--------|---------|
| thesis-framework.md | 14 | FPGA(5) + 术语(2) + 动词(2) + 措辞(2) + NMSE(2) + 平均(1) |
| thesis-status.md | 5 | 术语(1) + 物理约束(1) + FPGA(3) |
| material-section-content-cards.md | 24 | 旧数据(17) + 禁忌(5) + 术语(1) + 信号模型(1) |
| 03-研究方案.md | 6 | NMSE(5) + 因果链(1) |
| design-decisions.md | 6 | KF范围(1) + 弱湍流(1) + 级联(1) + 种子(1) + BPS条件(2) |
| section-outline.md | 5 | 术语(1) + 禁忌(1) + 旧数据(2) + 平均(1) |
| figure-table-plan.md | 2 | 平滑→平均 |
| formulas-ch4-kf.md | 2 | 信道增益→归一化辐照度 |
| formulas-ch2-system-model.md | 1 | 信道增益→归一化辐照度 |
| formulas-ch5-fpga.md | 1 | 平滑→平均 |
| thesis-preparation-checklist.md | 1 | 100→10种子 |
| TERMS.md | 4 | 禁忌恢复+理由优化+速查补充 |

## 关键决策

1. **禁忌验证结论**：全文统一用"归一化辐照度"和"VV平均窗口"，不混用。论文中不存在需要叫"信道增益"的独立物理量（h是辐照度，φ是相位，h_l是传输因子，已各自有术语）。
2. **NMSE表述统一**：全范围(0至-20dB)退化<0.3dB，不存在-5dB/-10dB阈值。
3. **FPGA未开发**：所有材料中"完成/实现/验证"改为"进行/设计分析"。

## 决策引用

- 无新 D### 决策（本次是执行既有规范，非做新决策）

## 范围确认

- 本轮是否在 scope boundary 内：是（语言审查属于写作准备范畴）

## 第二轮：创新点+结论+数据全面对齐（2026-06-02 续）

> 背景：创新点 v5 已定稿（2个，非3个；Ch4是"性能分析框架+设计准则"而非"自适应载波同步"），但 51 个 .md 文件中仍有大量旧数据/旧措辞残留。用户要求全面对齐，PPT 优先级降低。

### 方法

**Phase 1：摸底（9 路 grep）** — 搜索创新点/自适应/信道增益/平滑窗口/FPGA/首次/联合同步/旧数据/NMSE 旧阈值。

**Phase 2：审计（3 个并行 agent）**
- Agent A（10 个根目录文件）→ 7 处问题
- Agent B（17 个开题报告文件）→ ~20 处问题
- Agent C（24 个写作材料+正文+PPT文件）→ ~5 处问题（受上下文限制漏扫 10 个文件）

**Phase 3：修复 R1（3 个并行修复 agent）**
- 修复 Agent 1：核心材料 5 文件 16 处（thesis-framework/thesis-status/section-outline/material-section-content-cards/thesis-preparation-checklist）
- 修复 Agent 2：最新 draft+公式 8 文件 13 处（draft-s1.1-v4/draft-s1.2-v4/draft-s1.3-s1.4-v2/formulas-master/formulas-ch3ch4-sync/formulas-ch3-link-performance/design-decisions/03-研究方案）
- 修复 Agent 3：PPT+文献 4 处 + 旧版归档标注 9 文件

**Phase 3.5：验证 grep** — 确认"三个方面""自适应载波同步""湍流感知"在活跃材料中已清零。发现 formulas/material-cards/section-outline 等文件仍有残留。

**Phase 4：修复 R2（2 个并行修复 agent）**
- Agent 1：formulas 文件 section 标题级修复（formulas-master/formulas-ch3ch4-sync/formulas-ch4-kf/formulas-ch2-system-model/writing-reference-s1.2），10 处
- Agent 2：material-section-content-cards.md 深度清理，34 处"自适应"全部替换

**Phase 4.5：深扫新维度（1 个 explore agent）** — 搜索 12 个新模式：
- 旧 VV/BPS 失败率数据、100 种子、oracle CSI、FPGA 残留、EKF 旧方向、统一载波同步、VV 有害旧结论、KF 增益旧数据、ω_n MHz 单位、"提出"措辞、"揭示"措辞
- 发现大量新问题

**Phase 5：修复 R3（3 个并行修复 agent）**
- Agent 1：旧数据+种子数（design-decisions/03-研究方案/thesis-preparation-checklist），6 处
- Agent 2："揭示"→"分析/表明"（thesis-framework/03-研究方案/draft-s1.2-v4），9 处
- Agent 3：FPGA/ω_n/文件标题残留（section-outline/formulas-ch4-kf/CONCLUSIONS/旧版draft），7 处

### 修改总统计

| 轮次 | 修改数 | 文件数 | 主要内容 |
|------|--------|--------|---------|
| R1（首轮审计，前对话） | ~71 | 12 | 旧VV数据/NMSE升级/FPGA/术语/措辞 |
| R2（创新点+自适应） | ~42 | 17 | 创新点3→2/自适应→分析框架/draft修复/旧版归档 |
| R3（formulas+cards深清） | 44 | 6 | section标题/34处自适应清理 |
| R4（旧数据/揭示/ω_n） | 22 | 9 | VV/BPS数据/揭示措辞/ω_n单位/种子数 |
| **合计** | **~179** | **~25** | |

### 按类别统计

| 类别 | 修改数 | 典型修改 |
|------|--------|---------|
| 创新点 3→2 | ~20 | "三个方面"→"两个方面"，删除FPGA创新点段 |
| "自适应"→"分析框架+设计准则" | ~50 | material-cards(34)+formulas(6)+section-outline(5)+其他 |
| FPGA "完成/实现"→"进行/设计分析" | ~15 | draft-s1.1/s1.2/s1.3/section-outline/03-研究方案 |
| "揭示"→"分析/表明/给出" | ~13 | thesis-framework(4)+draft-s1.2-v4(4)+03-研究方案(1)+其他 |
| 旧 VV/BPS 失败率数据 | ~6 | "35%/50%"→"39.2%/35.0%精确数据" |
| ω_n MHz→rad/s | ~4 | CONCLUSIONS.md 中单位修正 |
| 100种子→10种子 | ~3 | design-decisions/thesis-preparation-checklist |
| 旧版归档标注 | 9 | v1/v2/v3 draft 文件添加归档警告 |
| "湍流感知"→"导频辅助" | ~4 | formulas-ch4-kf 标题 |

### 修改过的文件完整清单

**根目录文件（7个）**：
- thesis-framework.md — "两个方面"+删除FPGA创新点+"揭示"→"表明/分析"
- thesis-status.md — D012推翻标注+"自适应载波同步MVE"→"载波同步性能分析"
- master-state.md — 状态更新
- design-decisions.md — VV/BPS精确数据+100种子→10种子+NMSE阈值
- thesis-preparation-checklist.md — "有2个创新点"+种子数措辞
- formulas-master.md — "载波同步"(去自适应)+NMSE阈值+"分湍流设计准则"
- formulas-index.md — 无修改

**写作材料文件（8个）**：
- section-outline.md — 创新点(3)删除+"载波同步性能分析与参数优化"+FPGA修复
- figure-table-plan.md — （前轮已修）
- formula-inventory.md — 无修改
- formulas-ch2-system-model.md — "分湍流参数优化"(3处)
- formulas-ch3-link-performance.md — "载波同步"(去自适应)
- formulas-ch3ch4-sync.md — section标题"分湍流条件"(3处)+NMSE阈值
- formulas-ch4-kf.md — 标题"导频辅助KF"(2处)
- formulas-ch5-fpga.md — （前轮已修）
- writing-reference-s1.2.md — "两个方面"
- literature-notes-ch1-ch2.md — "分湍流CPR设计准则"

**开题报告文件（10个）**：
- 03-研究方案.md — FPGA"进行设计分析"+VV/BPS精确数据+"分析"(去揭示)
- draft-s1.1-v4.md — v5措辞+FPGA"设计与分析"+P5段修正
- draft-s1.2-v4.md — "两个方面"+删除第3条不足+"分析"(去揭示)
- draft-s1.3-s1.4-v2.md — "两个方面不足"+"分湍流条件的参数配置规律"
- material-section-content-cards.md — 34处"自适应"全面清理(标题+内容+Ch4描述)
- draft-s1.1-v1/v2/v3.md — 归档标注
- draft-s1.2-v1/v2/v3/v3-partial/v3-partial2.md — 归档标注
- draft-s1.3-s1.4-v1.md — 归档标注

**PPT文件（1个）**：
- PROMPT-009-ppt-guide.md — "载波同步性能分析与分湍流参数优化"

### 未修/待继续扫

- `正文/Ch2-星地激光通信系统与信道模型.md` — Ch2 正文本体，可能有零星措辞
- `CONCLUSIONS-VERIFY-PLAN.md` — 验证计划，可能过时
- `ppt-content-decisions.md` — PPT 内容决策，部分可能需同步
- `正文/Ch2-reviews.md` + `正文/Ch2-guides.md` — 写作指导文件，有零星建议措辞
- section-outline.md 中"揭示"（4处）— 文件自己把它列为推荐强动词，用户未决定是否修改
- writing-phrases.md/writing-patterns-*.md — 范文引用中的"显著/揭示/提出"是他人论文内容，不改
- verification/ 目录全部 — 历史记录，不动

## 压缩后继续扫（2026-06-02 续2，第二轮）

> 背景：上下文压缩后继续深扫。前轮已修 ~179 处/25 文件。

### 方法

1. **7 路 grep 摸底**：显著/首次+填补空白+oracle/信道增益/揭示/自适应+湍流感知+三个方面/联合同步+VV平滑+100种子/ω_n MHz
2. **2 个 explore agent**：
   - Agent A：Ch2 正文全文扫描（12 类模式 + 信号模型一致性检查）
   - Agent B：未扫文件扫描（Ch2-reviews / Ch2-guides / CONCLUSIONS-VERIFY-PLAN / figure-table-plan / formula-inventory）

### 发现与修复

| 文件 | 修改数 | 内容 |
|------|--------|------|
| ppt-content-decisions.md | 1 | 三列→两列布局，"三个方面"→"两个方面" |
| PROMPT-009-ppt-guide.md | 5 | "自适应方案"→"性能分析框架+设计准则"（5处：L68/82/117/119/120） |
| Ch2-reviews.md | 1 | "揭示"→"表明"（L220写作指导示例） |

### 扫描确认干净的文件

- `正文/Ch2-星地激光通信系统与信道模型.md` — 全部 12 类模式 0 匹配，信号模型正确（√h + h为实值辐照度）
- `正文/Ch2-guides.md` — 0 问题
- `CONCLUSIONS-VERIFY-PLAN.md` — 文件不存在
- `figure-table-plan.md` — 0 问题
- `formula-inventory.md` — 0 问题

### 验证 grep 结果

- "拟提出自适应"：活跃材料中已清零
- "三个方面"：仅在归档文件（v1/v2/v3 drafts）或不同语境（可行性维度）中出现
- "揭示"：仅 section-outline.md 4处（待用户决定）+ 归档/参考文件
- thesis-framework.md "显著"：全部为"无显著优势"（否定用法），无需修改

### 累计统计（含前轮）

| 轮次 | 修改数 | 文件数 |
|------|--------|--------|
| R1（首轮审计） | ~71 | 12 |
| R2（创新点+自适应） | ~42 | 17 |
| R3（formulas+cards深清） | 44 | 6 |
| R4（旧数据/揭示/ω_n） | 22 | 9 |
| **R5（本轮 PPT+Ch2 扫描）** | **7** | **3** |
| **合计** | **~186** | **~28** |

## 后续

- **section-outline.md "揭示"**（4处，L35/39/73/82）：文件自身将其列为推荐强动词，待用户决定是否修改
- **100种子计划**：如果后续跑 100 种子仿真，需全局更新种子数 10→100
- **Ch3 NMSE vs BER 曲线**：verification-report 建议补充，尚未执行
- **补缺页**：开题报告缺页（研究内容/进度安排/预期成果/创新之处/研究基础）还没开始
