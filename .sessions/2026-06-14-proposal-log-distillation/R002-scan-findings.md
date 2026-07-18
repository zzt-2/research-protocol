# [R002] 粗扫+细扫全量发现清单（6 agent 整合）

> 2026-06-15 | 关联：2026-06-14-proposal-log-distillation / R001（方法论）/ D001-D003

## 调研问题

6 个 agent（3 粗扫 + 3 细扫）扫完全部写作过程类 .md（~300 文件 / ~86000 行）后，整合四维（A 写作痛点 / B 真实评估标准 / C 写作范例 / D 工作流）**素材源清单**。每条带：来源 agent、文件:行号指针、维度、一句话价值、日期有效性、能否填下游契约字段。

**目的**：扫描模板设计 + pilot 挑选 + 全量蒸馏的素材源索引。**防压缩丢失**——6 agent 发现量大，不沉淀必丢（用户 2026-06-15 原话："赶紧沉淀吧，写的尽可能全。后面的上下文一定没有你现在全，你写不全后面就丢东西"）。

**下游契约字段**（D002 / topic-index 产出落点表）：

- A `{来源指针, 痛点, 归类[检测器ID|新维度], 对S033哪个待讨论项有输入}`
- B `{批注原文指针, 批评点, 是否已覆盖[是→哪条rubric|否→新维度]}`
- C `{原文指针, 好在哪, 适合做哪个改写目标的few-shot}`
- D `{手搓步骤清单, vs paper-write现状, 优化建议}`

**行号精度说明**：粗扫1/细扫A/细扫B/细扫C 的 file:line 来自 agent 完整报告，较精确；粗扫2/粗扫3 的部分条目来自 relay 要点（agent 原始报告已不在上下文），标"行号待 pilot 补"，pilot 实读时校准。

## 扫描覆盖（6 agent）

### 粗扫（3 agent）

| agent | 范围 | 文件数 |
|-------|------|--------|
| 粗扫1 | `.sessions/thesis-direction-pivot/` | 98 |
| 粗扫2 | `毕设/` 主规范文件（写作质量规范/ai-trace/design-decisions/defense-principles/writing-patterns-*/开题报告v2批注） | ~124（主规范子集） |
| 粗扫3 | `.sessions/` 三写作专题（writing-prep/advisor-review-revision/writing）+ 根目录散落 | ~80 + 根目录 |

### 细扫补盲区（3 agent）

| agent | 范围 | 状态 |
|-------|------|------|
| 细扫A | `毕设/` 角落（archive/正文/verification phase3-4/根级散落） | 完成 |
| 细扫B | `.sessions/2026-06-04-citation-verification/` + `projects/thesis-figures` + `thesis-fso` + ~~`stages/thesis-materials.md`~~ | 完成（重启1次，首次 API 限流） |
| 细扫C | `projects/_archive/` 旧方向 R003/S006 + `.omc/scientist/reports/` | 完成 |

## 排除项汇总（已确认不采）

| 排除项 | 位置 | 排除原因 |
|--------|------|---------|
| archive/writing-patterns-*.md（5个）| `毕设/写作材料/archive/` | 早期 Task B1/B2/B3 产出，已被顶层 writing-patterns-sentence.md(83.7K)/-paragraph.md(85.6K) superset（grep 验证 14 处"分别为"+7 处 Kolmogorov/GG 已迁移） |
| archive/formulas-dedup-backup/（4个）| `毕设/写作材料/archive/` | 纯公式备份 |
| verification/phase3-deviations/ + phase4-consistency/ | `毕设/写作材料/verification/` | **空目录**（`ls -la` 确认 total 0，从未填充） |
| verification/phase1-research/ + phase2-results/ | `毕设/写作材料/verification/` | 纯理论/数值验证，非写作 |
| 正文/cross-chapter-notes.md | `毕设/正文/` | 空文件（0 行） |
| .omc/scientist/reports/（3个）| `.omc/scientist/` | 运行时技术验证报告（公式核验/文献声明交叉验证/仿真核验），非写作方法论 |
| verification_report.md + final_verification_report.md | `citation-verification/` | FINAL_OUTPUT.md 的早期草稿，内容重复（final_verification_report.md L75-81 有 FINAL_OUTPUT 缺的"区分式 vs 整体式建模"一点，可作 B 补充） |
| search_results.json | `citation-verification/` | 原始 API 输出 |
| **stages/thesis-materials.md** | `stages/` | **用户 2026-06-15 判定"很旧别管"**（细扫B 曾认为是 paper-write 蓝图，用户否决，见 D003）。其"引用质量 rubric（中文≥10篇/预印本率≤30%/40%）"改由 bib-quality-issues + citation-verification 覆盖 |
| formulas-master.md / formulas-index.md | `毕设/` | 公式表，非写作过程 |
| README / 表格模板 / pandoc 配置 | 多处 | 非写作过程 |
| 旧方向（路由/GNN）技术内容 | `_archive/` | 技术作废；方法论部分（R003/S006）已单独提取，见 C/B 维度 |

---

## A 维度：写作痛点

### A1. 毕设/写作质量规范.md §9 — AI advisor 系统性偏差（最深洞察）
- **来源**：粗扫2
- **价值**：A 维度最深的洞察——不止表层翻译腔，是 advisor 在写作建议上的**结构性偏差**（系统性、可预判）
- **指针**：`毕设/写作质量规范.md` §9（行号待 pilot 补）
- **日期**：有效
- **下游**：A `{归类→检测器ID"AI advisor 偏差"，对 S033 待讨论项"系统性偏差检测"有输入}`

### A2. 毕设/ai-trace-report.md（209行）— 自检开题报告 AI 痕迹
- **来源**：粗扫2 + R001 漏点3
- **价值**：自检报告，直接对应 paper-eval AI 痕迹检测器
- **指针**：`毕设/开题报告/ai-trace-report.md`（注意在"开题报告"子目录非毕设根；209 行；汇总统计表 L8-15、重度定位 L21-36、系统性模式总结 L71-97、范文诊断信号 L197-209；对话 B 校准）
- **日期**：有效
- **下游**：A `{归类→检测器ID"AI 痕迹"}`

### A3. thesis-direction-pivot/S017 + 108 问题清单 — AI 痕迹量化分布
- **来源**：粗扫1
- **价值**：翻译腔 27+ / 清单体 7 段 / 数据三重出现 6 项×3 / 超长句 22 / 引用错位 11 / "本章"滥用 8 / 衔接断裂 9 / 元叙述 4 / 括号堆砌 40
- **指针**：`thesis-direction-pivot/S017-thesis-writing.md`（108 问题清单段）
- **日期**：有效（pivot 后）
- **下游**：A `{痛点量化分布}`

### A4. thesis-direction-pivot/R011 5 大 AI 缺陷
- **来源**：粗扫1
- **价值**：翻译腔 / 清单体 / 段落衔接断裂 / 数据堆砌 / 元叙述——已沉淀成 B1 规则的源头
- **指针**：`thesis-direction-pivot/R011-chinese-academic-writing-patterns.md`（5 大缺陷段）
- **日期**：有效
- **下游**：A `{归类→B1 规则}`

### A5. advisor-revision A 类批注（4条）— 导师原话（权威性最高）
- **来源**：粗扫3
- **价值**：导师原话 #16"AI 应仅为辅助，不能照搬 AI 高生成度结果，本人应逐句思考" + #34"人工逐句理顺" + #48"机器语言"——已沉淀成 B1 规则（AI 痕迹 5 类）
- **指针**：`.sessions/2026-06-04-advisor-review-revision/`（A 类批注 #16/#34/#48，行号待补）
- **日期**：有效
- **下游**：A `{导师原话，权威性最高，对 S033"AI 痕迹"检测器有输入}`

### A6. innovation-points.md v1→v6 创新点措辞迭代 — 罕见标本
- **来源**：细扫A
- **价值**：创新点措辞为什么改了 6 版的完整实证（A 维度独有深度）：
  - Ch4 v1"湍流感知自适应载波同步方案"— 物理无效（GG 准静态 / TL-03）
  - Ch4 v4"设计与优化方法"— "方法"被理解为算法，实际是分析框架；中文惯例分析类用"推导/建立/给出"，算法类才用"提出方法"
  - "KF 导频辅助载波同步"— "湍流感知 R 矩阵"证伪（4 种 R 差异<12%）
  - "VV 在所有湍流条件下有害"— VV 公式 bug 导致
  - 迭代历程 v1→v2→v3→v4→v5→v6
- **指针**：`毕设/innovation-points.md` L82-124（被否决方案）+ L93（迭代历程）
- **日期**：有效（最新 2026-06-13）
- **下游**：A `{痛点=创新点措辞反复迭代 6 版，归类→新维度"创新点措辞敏感性"，对 S033"措辞改写"待讨论项有输入}`

### A7. 正文/Ch2-reviews.md 反复犯错记录表
- **来源**：细扫A
- **价值**：括号内章节号、过强动词"建立"、机械节引用、回指句——在 S003/S004 纠正后在 Ch2 复现，附根因分析
- **指针**：`毕设/正文/Ch2-reviews.md` L414-424
- **日期**：有效（2026-06-01/02）
- **下游**：A `{复犯模式，归类→"反复犯错检测"}`

### A8. R003-kaiti-chapter3-research-plan.md P1-P6 问题诊断
- **来源**：粗扫3
- **价值**：开题第三章 6 类痛点根因——教科书摘抄 / 实验报告式 / 缺叙事弧 / 不回应空白 / 暴露结论 / 系统模型冗长
- **指针**：`.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md`（41.7K）P1-P6 问题诊断段（P1=L26 教科书摘抄 / P2=L36 实验报告式 / P3=L48 缺叙事弧 / P4=L59 不回应空白 / P5=L67 暴露结论 / P6=L80 系统模型冗长 / §1.2 归类表=L88）（对话 B 校准；A8 全维度亦见 C13）
- **日期**：有效
- **下游**：A `{痛点根因分类}`（注：该文件 A/B/C/D 全维度，亦见 C13）

### A9. draft-ch1-template-test.md §模板效果自评
- **来源**：粗扫1
- **价值**：P8/P9 缺陷分析段难度 6/10，最难写——写作卡壳点的自陈
- **指针**：`thesis-direction-pivot/draft-ch1-template-test.md`（§模板效果自评段，445 行）
- **日期**：⚠️ 信道均衡框架描述作废（后改预补偿/级联分析），但 P# 标签自评 + 句式模式可复用
- **下游**：A `{写作难度/卡壳点}`（亦见 C20）

### A10. citation-verification"避免绝对化"— AI 倾向性
- **来源**：细扫B
- **价值**：AI 倾向写"首次/从无到有/完全空白"，导师要求改为"精细化提升/精细化建模空白"——既是 B（学术诚信）也是 A（AI 帮倒忙：AI 倾向绝对化）
- **指针**：`.sessions/2026-06-04-citation-verification/FINAL_OUTPUT.md` L54-55 / L77-79 / L104-108
- **日期**：有效
- **下游**：A `{AI 倾向性，归类→"绝对化用语"}`（亦见 B15）

## B 维度：真实评估标准（最丰富，多源叠加蒸馏最彻底）

### B1. advisor-revision 20 批注 5 类 — 导师批注全集
- **来源**：粗扫3
- **价值**：开题报告 v2 导师 20 条批注按 5 类——A 类 AI 痕迹(4) / B 类学术定位(2) / C 类格式(10) / D 类图表(3) / E 类参考文献(2)。每类详见 B2/B5/B11/B15 等
- **指针**：`毕设/开题报告/开题报告v2-导师批注.md` 20 批注按序 L10-215（5 类分布：A类AI痕迹4/B类学术定位2/C类格式10/D类图表3/E类参考文献2，pilot 校准）
- **日期**：有效
- **下游**：B `{批注原文指针，每条独立映射}`

### B2. B 类学术定位批注 #45/#42 → Popper 可证伪性判据
- **来源**：粗扫3
- **价值**：导师原话 #45"3.6.3/3.6.4 属于学习教学，不属于科学研究" + #42"不属于学术论文范畴"——蒸馏成 **R001 Popper 可证伪性判据 + 假设显性化三要素（条件-预测-判据）**。这是"导师一句话蒸馏成完整学术判据"的范式
- **指针**：`毕设/写作质量规范.md` §12.4 Popper（+ advisor-revision #45/#42）
- **日期**：有效
- **下游**：B `{批评点=学术定位，是否已覆盖→rubric"Popper 可证伪性"}`

### B3. thesis-direction-pivot/S001 导师批评原文 + 4 条底线
- **来源**：粗扫1
- **价值**：导师批评原文 + 4 条底线——无 h² / 级联分析 / 公平评估 / 理论预期先行
- **指针**：`thesis-direction-pivot/S001-advisor-meeting-and-direction-framework.md` 导师批评原文 L15-22 + 4 底线 L34-39（pilot 校准）
- **日期**：有效
- **下游**：B `{导师硬底线}`

### B4. advisor-brief.md / advisor-briefing.md 公平性审查三步法 + "不要全信"元标准
- **来源**：粗扫1
- **价值**：公平性审查三步法 + "不要全信"的元标准（评估者本身的偏差警惕）
- **指针**：`thesis-direction-pivot/advisor-brief.md`（公平性审查三步法 L35-43）+ `thesis-direction-pivot/advisor-briefing-2026-05-30.md`（注意是两个文件，非 advisor-briefing.md；对话 B 校准）
- **日期**：有效
- **下游**：B `{公平性审查 rubric + 元标准}`

### B5. 正文/Ch2-reviews.md 8 维度审查 rubric R1-R8
- **来源**：细扫A
- **价值**：user 自审体系——R1 语言质量 / R2 论断依据 / R3 技术常识 / R4 术语合规 / R5 符号一致 / R6 禁忌内容 / R7 图表公式 / R8 动词强度
- **指针**：`毕设/正文/Ch2-reviews.md` L4-155
- **日期**：有效（2026-06-01/02）
- **下游**：B `{rubric，user 自审体系，是否已覆盖→这 8 维本身即 rubric}`（亦见 C2 diff）

### B6. 正文/Ch2-reviews.md 逐项 diff 表
- **来源**：细扫A
- **价值**：原文→修正，如"约 11 dB"→加推导"$20\log_{10}(1700/500) \approx 10.7$ dB"；R1 17 项 / R2 5 项
- **指针**：`毕设/正文/Ch2-reviews.md` L22-27 / L117-122
- **日期**：有效
- **下游**：B+C `{批注前后对比}`（亦见 C2）

### B7. 正文/Ch2-reviews.md 12 子 agent 深度文风审查 + 铁律 1-4
- **来源**：细扫A
- **价值**：~130 项发现分 H/M/L 三级 + **铁律 1-4**：①范文无"上节/前节/前文+动词"回指句 ②参数解释统一"式中/其中，A 为…，B 为…" ③符号重用通过上下文区分不显式声明 ④（第 4 条 pilot 时补）
- **指针**：`毕设/正文/Ch2-reviews.md` L158-359（审查）+ L367-376（铁律）
- **日期**：有效
- **下游**：B+C `{文风铁律，句级评估标准}`（亦见 C2）

### B8. CONCLUSIONS.md 安全等级 rubric + 已证伪 X-01~X-09
- **来源**：细扫A
- **价值**（B 维度评估标准金矿）：
  - **安全等级 rubric**：✅可写 / ⚠️需限定 / ❌不可写 / 🔄待重验
  - **代码来源等级 TL-24**：[common.py] / [纯理论] / [旧代码] → 可信度分级
  - 20 条结论注册表（结论+安全等级+代码来源+精确数字+边界+物理解释+限制）
  - **已证伪结论表 X-01~X-09**（原结论/证伪证据/文件残留）——B"批评过什么"精确清单
  - 写作统一用语表（归一化辐照度 h vs 信道增益 / GG 湍流衰落模型 vs GG 分布模型 / 光强起伏 vs 闪烁）
- **指针**：`毕设/CONCLUSIONS.md` L8-15（安全等级）/ L17-23（TL-24）/ L393-407（证伪表）/ L418-424（用语表）
- **日期**：有效（最新 2026-06-13）
- **下游**：B `{批评点=9 条已证伪声称，新维度"已证伪声称清单"}`

### B9. thesis-direction-pivot/S024 B2 FAIL 证伪 R 矩阵 — 真实失败案例
- **来源**：粗扫1
- **价值**：20 维度压力测试，B2 FAIL **直接证伪 R 矩阵**——"评估标准如何砍掉一个不成立结论"的完整证据链，paper-eval 评估盲区真东西
- **指针**：`thesis-direction-pivot/S024-kf-stress-test.md` L147-162（B2 R矩阵FAIL）+ L286-291（D1 强湍流KF输给最优Fixed）+ L304（D2 消融VV有害）+ L310-320（D3 标准PA-KF反证）+ L374（B2+D3双重证伪总结）（pilot 校准）
- **日期**：有效
- **下游**：B `{评估失败案例，新维度"压力测试 FAIL→结论证伪"}`

### B10. thesis-direction-pivot/S023 对"DPLL 全面优于"诚实修正
- **来源**：粗扫1
- **价值**：§5-§6 100 种子修正 + §6 诚实评估（创新性弱 / 对开题勉强够 / 对最终论文不够）——"如何写不吹的结论"的范文
- **指针**：`thesis-direction-pivot/S023-ch4-systematic-simulation.md` §5-§6
- **日期**：有效
- **下游**：B `{诚实修正范式}`

### B11. 引用质量 rubric（多源叠加）— 导师级硬标准
- **来源**：细扫B（+ 粗扫3 E 类批注）
- **价值**（国标规则 + 工具失败模式）：
  - GB7714 作者数规则：>3 人列前 3 加"等"，≤3 全列 — `bib-quality-issues.md` L20
  - arXiv 预印本类型标识：国标 `[EB/OL]`（电子）或 `[PP/OL]`（预印本），pandoc CSL 错误映射 `[Z]` — L42-44
  - 期刊 `[J]` 必须有起止页码或文章编号 — L56
  - `[Others]` 非合法作者占位符 — L62
  - ⚠️ "中文期刊≥10 篇 / 核心引用预印本率≤30% / 全部预印本率≤40%"：原源 `thesis-materials.md` L168-191，**文件已排除（D003）**，此条暂无替代源，标"待补"
- **指针**：`projects/thesis-figures/bib-quality-issues.md` L9-63（主源）；导师 E 类批注 #54"以 trans 为主"→ Tier-1/2/3 三级（advisor-revision）
- **日期**：有效（2026-05-28）
- **下游**：B `{引用质量 rubric，是否已覆盖→是（GB7714）/否（预印本率门槛，原源排除）}`

### B12. AI 编造 DOI 检测 — paper-eval 引用检测器直接素材
- **来源**：细扫B
- **价值**：
  - **Nguyen 2020 真实案例**：DOI `10.1109/ACCESS.2020.2989012`（假）vs `10.1109/ACCESS.2020.3036643`（真），标题完全不匹配
  - **OpenAlex 标题匹配撞名**：量子计算论文（Cerezo）被匹配到 IoT LEO 论文——工具误匹配
- **指针**：`citation-verification/FINAL_OUTPUT.md` L59（错误DOI 2989012）+ L60-63（标题不匹配）+ L62（正确DOI 3036643）+ `bib-quality-issues.md` L26-36（OpenAlex 撞名）。注：原标 L26-31 是 Castrillon 2015 段，pilot 校准修正为 Nguyen 段
- **日期**：有效
- **下游**：B `{批评点=DOI 与真实论文不匹配，新维度"DOI 存在性验证"/"工具匹配可信度"，对 S033 引用检测器有输入}`

### B13. 引用 4 维可靠性 rubric
- **来源**：细扫B
- **价值**：存在性 / 内容匹配 / 场景匹配 / 总体可靠性——导师没有但应该有的 rubric
- **指针**：`citation-verification/VERIFICATION_SUMMARY.md` L103-109
- **日期**：有效
- **下游**：B `{新维度"引用 4 维可靠性 rubric"}`

### B14. 研究空白分级 rubric + 精确空白表述
- **来源**：细扫B
- **价值**：空白/章节/验证结论/空白类型（方法/场景/组合/文献）/创新潜力（★三级）+"非绝对零（JLT 2024 有 1 篇），但系统性方法论文为零"（呼应避免绝对化）
- **指针**：`projects/thesis-fso/literature_notes.md` L180-198（rubric）+ L186（精确表述）
- **日期**：有效（2026-05-29）
- **下游**：B `{新维度"空白分级 rubric"/"空白声明必须列反例"}`

### B15. 学术诚信 4 条硬规则
- **来源**：细扫B
- **价值**：所有 DOI 必须验证 / 标题期刊必须准确 / 避免"首次""空白"绝对化 / 强调精细化贡献
- **指针**：`citation-verification/FINAL_OUTPUT.md` L141-140（"学术诚信提醒"段）
- **日期**：有效
- **下游**：B `{新维度"引用诚信自检清单"}`

### B16. S006 硕士评审权重表（稀缺，R003 没有）
- **来源**：细扫C
- **价值**：
  - 法律依据：学位条例第五条"一定的新见解或新内容"
  - 6 维评审指标权重表（创新性 20-25% 等）
  - 硕士级创新门槛 4 条 + 不通过 Top 5
- **指针**：`projects/_archive/leo-ntn-handover-drl/paper_materials/_sources/session/S006-ch2-domain-verify-and-thesis-positioning.md` L99-141
- **日期**：方法论有效（旧方向，评审标准通用）
- **下游**：B `{rubric 维度来源"硕士评审权重"，稀缺}`

### B17. S006 够格线对照表
- **来源**：细扫C
- **价值**：当前项目 vs 同方向够格线（章节体系/仿真器/baseline/多 seed/统计检验/规模）——论文定位自检工具
- **指针**：`S006` L142-157
- **日期**：方法论框架有效（具体数字作废）
- **下游**：B+C `{够格线对照表模板}`

### B18. defense-principles 评审委员会视角
- **来源**：粗扫2
- **价值**：答辩"怎么把研究讲清楚"的逻辑——评审委员会视角
- **指针**：`毕设/开题PPT/defense-principles.md`（对话 B 校准：开题本质 L8-16 / PPT 内容规则 L22-44 / 时间分配 L47-56 / Q&A 防御 L60-99 / 叙事弧清单 L103-113 / 延续原则 L116-124）
- **日期**：有效
- **下游**：B `{评审委员会视角}`

### B19. design-decisions R01-R16 否决索引
- **来源**：粗扫2
- **价值**：被否决方向完整索引 + 否决理由——本身是"否决记录该怎么写"的元范例
- **指针**：`毕设/design-decisions.md` R01-R16 否决索引在 L549-566（表头 L549，R01-R16 紧凑表格 L551-566；文件总 613 行；对话 B 校准）
- **日期**：有效
- **下游**：B+D `{否决记录范式}`（亦见 D12）

### B20. thesis-direction-pivot/S019 SNR 约定敏感性
- **来源**：粗扫1
- **价值**：SNR 约定敏感性发现（D011 修正）+ 3-agent 验证流程——"约定/假设差异影响结论"
- **指针**：`thesis-direction-pivot/S019-ch2-derivations-and-verification.md`（D011 段 + 12-agent 验证表）
- **日期**：有效
- **下游**：B `{约定敏感性，验证流程}`

### B21. H025 13 检查项审计表 + 11 维度压测
- **来源**：粗扫1
- **价值**：PASS/FAIL/PARTIAL 量化——审计 rubric 范式
- **指针**：`thesis-direction-pivot/H025-ch3-audit-result.md`（13 检查项 + 11 维度压测 F1-F11）
- **日期**：有效
- **下游**：B `{审计 rubric}`

### B22. investigation-nmse-literature-review.md 贡献定位措辞
- **来源**：细扫A
- **价值**："贡献不是'发现信道估计误差不影响 BER'，而是'量化了…影响程度(<0.3dB)+ 发现 h 对消机制+ 区分路径 A/B'"——贡献声称要精确，不能让读者误以为是已知结论的复述
- **指针**：`毕设/写作材料/verification/investigation-nmse-literature-review.md` L194-201
- **日期**：有效（2026-06-01）
- **下游**：B `{批评点=贡献声称要精确，新维度"贡献定位措辞"}`

## C 维度：写作范例

### C1. R011 中文学术写作方法论地基（所有 C 素材的上游）
- **来源**：粗扫1
- **价值**：T1-T6 句间逻辑 + R1-R2 衔接 + AI 5 大缺陷 + **句子功能标注体系 DEF/FACT/CLAIM/EVAL/TRANS/GAP/NEED/CITE**
- **指针**：`thesis-direction-pivot/R011-chinese-academic-writing-patterns.md` AI 5大缺陷 L290-331 + AI高频词黑名单 L241-245 + 句子功能标注体系 L375-419 + 先扬后抑模式 L104 + 引用嵌入 L173/L211（pilot 校准全文定位）
- **日期**：有效
- **下游**：C `{方法论地基，所有 C 素材的上游，适合做"句间逻辑改写"few-shot}`

### C2. 正文/Ch2-reviews.md diff + 铁律 1-4（C 视角，三维高密度，最大漏网）
- **来源**：细扫A
- **价值**：逐项 diff 表（原文→修正，R1 17 项/R2 5 项）+ 12 子 agent 文风审查 ~130 项 + 铁律 1-4（见 B7）——前三个 agent 漏掉的最大单文件
- **指针**：`毕设/正文/Ch2-reviews.md` L22-27/L117-122（diff）+ L158-359（审查）+ L367-376（铁律）
- **日期**：有效
- **下游**：C `{原文指针=Ch2-reviews.md:Lxx，好在哪=diff 体现的具体修正手法，适合做=术语合规/R2 论断依据/R8 动词强度等维度改写}`（亦见 B5/B6/B7）

### C3. 正文/Ch2-星地激光通信系统与信道模型.md — 唯一已写完章节正文
- **来源**：细扫A
- **价值**：pivot 后唯一完成章节（197 行），完整推导链：信号光场(2.1)→本振光场(2.2)→QPSK(2.3)→…→GG 分解(2.16)→GG PDF(2.17)→平均 SNR(2.21)；"可表示为"+参数解释"式中，A 为…，B 为…"范式
- **指针**：`毕设/正文/Ch2-星地激光通信系统与信道模型.md` L23-31（公式引入范式）
- **日期**：有效（2026-06-02）；注：6 处【图X/表X】占位标记
- **下游**：C `{原文指针=L23-31，适合做=信号模型建立段/噪声建模段改写}`

### C4. 正文/Ch2-guides.md — Ch2 写作向导
- **来源**：细扫A
- **价值**：结构指南 + 公式清单 + 衔接句式 + 术语规范；关键句式清单（公式引入/参数解释/假设引入/系统描述）
- **指针**：`毕设/正文/Ch2-guides.md` L62-83
- **日期**：有效（2026-06-01）
- **下游**：C `{适合做=节首铺垫句改写}`

### C5. figure-composition-analysis.md 图表叙事（C 顶配）
- **来源**：粗扫3
- **价值**：研究背景→研究内容总览图完整解构（逐块拆解+箭头/颜色语义+绘制参数）+ **第 7 节"复刻到自己课题的替换模板"（8 层占位符）** + 第 11 节星地光链路完整示例
- **指针**：`figure-composition-analysis.md` 第7节替换模板 L414-541 + 第11节星地光链路示例 L638-678（pilot 校准）
- **日期**：有效（25.2K）
- **下游**：C `{图表叙事 few-shot，paper-write 可直套}`

### C6. R003-writing-norms 贡献声称写法（三副本去重一份，方法论 85% 可继承）
- **来源**：细扫C
- **价值**：
  - L11-16 工程教指委 2023 评价标准 + 贡献≠新颖性权威定义
  - L18-43 贡献定位三策略（场景适配/实证系统/问题建模）+ 中英句式模板
  - L45-58 贡献声明动词谱系表（formulate→propose→design→evaluate→apply 强弱梯度）
  - L60-90 局限性四要素结构（性质→原因→影响→改进）+ 坦诚程度梯度表
  - L106-117 Before→After A 组 6 条（贡献声称降级）
  - L119-134 Before→After B 组（技术组件定位）+ C 组（指标结果定位）——**模板形式继承，旧技术例子作废**
  - L138-142 局限性写法 3 条
- **指针**：`projects/_archive/leo-mega-constellation-gnn-routing/paper_materials/_sources/R003-writing-norms-contribution-claims.md`（代表副本，155 行，三份 byte-for-byte 相同）
- **日期**：方法论 ~85% 可继承，技术例子 ~15% 作废
- **下游**：C `{贡献声称 few-shot，16 条 Before→After}`

### C7. S006 贡献声称降级措辞 5 条（与 R003 互补）
- **来源**：细扫C
- **价值**：过度声称→诚实定位的措辞降级规则
- **指针**：`S006` L159-188
- **日期**：方法论可继承
- **下游**：C `{贡献降级 few-shot，与 R003 L106-117 互补}`

### C8. projects/thesis-figures/开题报告.md — 旧 GNN 方向开题绪论范文（导师通过）
- **来源**：细扫B
- **价值**（全套模板，技术作废写法可继承）：
  - L11-87 绪论 4 维度并列综述 + 空白收敛
  - L41-44 综述句式（"GAT 路线利用…但…；GCN 路线…但…"按技术路线分流）
  - L77-87 三空白归纳（路由/切换/故障→同一核心问题）+ 收敛句
  - L96-107 探索性分化框架命名 + 三方向关系（正常态→优化态→异常态）
  - L113-159 预期成果（量化指标）+ 初步仿真（91.5%/89.4%/13.4%）
  - L196-208 表 3-1 方案对比表（8 行×3 列）
  - L254-265 可行性 4 维（理论/方法数据/已验证/风险应对）
  - L270-279 进度安排 6 阶段
- **指针**：`projects/thesis-figures/开题报告.md`（标题"基于图神经网络的 LEO 卫星网络路由与切换方法研究"）
- **日期**：⚠️ 技术作废（GNN，pivot 前 1 天 2026-05-28），**写作范例价值不因技术作废失效**
- **下游**：C `{开题绪论改写 few-shot 全套模板}`

### C9. projects/thesis-fso/thesis-framework.md — FSO 方向绪论（与 C8 新旧对照）
- **来源**：细扫B
- **价值**：
  - L1-77 FSO 绪论完整结构（背景→湍流信道估计→载波同步→三不足归纳→创新点 3 条）
  - L21-37 综述收口句式（"传统方法三局限→DL 新路径→但泛化性边界→…级联关系未建立"）
  - L67-75 创新点 3 条（"系统分析了 X/Y + 完成了 Z"三段式）
  - L79-93 系统模型章数学组织（$r[k]=h[k]\cdot s[k]\cdot\exp(j\varphi[k])+n[k]$ + Gamma-Gamma + $E[1/h^2]$ 发散性）
  - L97-119 技术章节 7 节标准结构
- **指针**：`projects/thesis-fso/thesis-framework.md`
- **日期**：有效（pivot 后 2026-05-31）
- **下游**：C `{FSO 绪论改写 few-shot，与 C8 形成"同作者不同方向"风格对照}`

### C10. cnki-thesis-survey.md 章节命名方法论（前三个 agent 没覆盖）
- **来源**：细扫B
- **价值**（C 金矿）：
  - L38-200 3 篇 FSO 博士论文完整目录（张岱国防科大/王锋吉大/闫佳欣北理工）
  - L385-450 博士/硕士标题命名模式表 + 关键词组合规律 + 章节标题命名规律（绪论/理论基础/中间章节/末章标准结构）
  - L454-518 章节结构共性（6-7 章架构 / 均衡预补偿同步命名 / DSP 处理链路组织 / 分节规律）
- **指针**：`projects/thesis-fso/cnki-thesis-survey.md` L385-518 章节命名方法论段（标题模式 L391 / 绪论结构 L412 / 中间章节 L432 / 均衡预补偿同步命名 L474）（pilot 校准）
- **日期**：有效（2026-05-30）
- **下游**：C `{论文章节结构 + 标题命名 few-shot，user 自蒸馏的中文学位论文约定}`

### C11. literature_notes.md 综述笔记 + 参数溯源
- **来源**：细扫B
- **价值**：综述笔记模板 + 参数溯源模板（4 类参数+来源类型：实证/理论/实测/建模/标准/实验/工程）+ 综合分析三层结构（领域概况→核心挑战→研究定位）
- **指针**：`projects/thesis-fso/literature_notes.md` L202-237（参数溯源）/ L240-261（综合分析）
- **日期**：有效（2026-05-29）
- **下游**：C `{综述写法 + 参数溯源}`（亦见 D18）

### C12. R002-section-1-3-reference-analysis.md 章节安排模式库
- **来源**：粗扫3
- **价值**：4 篇有效范文的段落级 + 句式级模式
- **指针**：`.sessions/2026-05-31-thesis-writing/R002-section-1-3-reference-analysis.md`（行号待补）
- **日期**：有效
- **下游**：C `{章节安排 few-shot}`

### C13. R003-kaiti-chapter3-research-plan.md P1-P6（A/B/C/D 全维度）
- **来源**：粗扫3
- **价值**：开题第三章范式（P1-P6 问题诊断见 A8；此处标 C/D 价值：开题章节怎么写）
- **指针**：`.sessions/2026-05-31-thesis-writing/R003-kaiti-chapter3-research-plan.md`（41.7K）
- **日期**：有效
- **下游**：C+D `{开题第三章范式}`

### C14. writing-patterns 千行级正反例
- **来源**：粗扫2
- **价值**：writing-patterns-paragraph.md(1459 行) / -sentence.md(1019 行) / -ch2ch3.md(1016 行)——C 范例 + 反面例子
- **指针**：`毕设/写作材料/writing-patterns-*.md`
- **日期**：⚠️ -ch2ch3.md 已被正文取代（正文已重写）；段落/句子级有效
- **下游**：C `{正反例 few-shot}`

### C15. S004 夏兆宇 v3 模板（带句间逻辑链标注）
- **来源**：粗扫1
- **价值**：按 DEF/CLAIM/EVAL/TRANS 标注的实操样本
- **指针**：`thesis-direction-pivot/S004-template-extracted-xiazhaoyu.md`
- **日期**：有效
- **下游**：C `{实操样本}`

### C16. S001-annex-paragraph-template.md 段落级模板
- **来源**：粗扫1
- **价值**：单段如何展开论证
- **指针**：`thesis-direction-pivot/S001-annex-paragraph-template.md`
- **日期**：有效
- **下游**：C `{段落论证展开}`

### C17. material-fso-sentence-examples.md 21 个 FSO 句式
- **来源**：粗扫1
- **价值**：按场景分组的 FSO 领域可复用句式
- **指针**：`thesis-direction-pivot/material-fso-sentence-examples.md`
- **日期**：有效
- **下游**：C `{FSO 语料}`

### C18. material-section-content-cards.md 64 张章节卡片
- **来源**：粗扫1
- **价值**：每节 7 维信息（功能/论点/文献/数据/衔接/约束/篇幅）
- **指针**：`thesis-direction-pivot/material-section-content-cards.md`
- **日期**：有效
- **下游**：C `{内容映射}`

### C19. symbol-conventions.md 符号消歧（C 高价值）
- **来源**：细扫A
- **价值**：§13 已知歧义汇总 15 条消歧（α,β：GG 参数/DPLL 系数/大气衰减→加下标 α_DPLL，大气衰减改 σ_a；h：辐照度/海拔/普朗克→海拔改 z，普朗克改 h_P）+ §14 写作建议 5 条
- **指针**：`毕设/symbol-conventions.md` L237-256（消歧）/ L259-265（写作建议）
- **日期**：有效（最新 2026-06-13，265 行）
- **下游**：C `{符号首次定义段改写}`

### C20. draft-ch1-template-test.md 实际写作 + P# 自评
- **来源**：粗扫1
- **价值**：实际第一章写作尝试，每段带 P# 标签 + 自评（P8/P9 难度 6/10 最难写）
- **指针**：`thesis-direction-pivot/draft-ch1-template-test.md`（445 行）
- **日期**：⚠️ 信道均衡框架作废，**P# 自评 + 句式模式可复用**（亦见 A9）
- **下游**：C `{实际写作 + 自评范例}`

### C21. citation-verification PPT 引用策略 H7/H8 支撑页模板
- **来源**：细扫B
- **价值**：一页一主张 + 逐条溯源 + 空白箭头——综述支撑页范式
- **指针**：`citation-verification/FINAL_OUTPUT.md` L112-140
- **日期**：有效
- **下游**：C `{综述支撑页 few-shot}`

### C22. innovation-points.md 当前草案 v6
- **来源**：细扫A
- **价值**：IP1 Ch3 / IP2 Ch4 宽壳策略，含文献对标/退路/递进/已有支撑/风险/措辞策略
- **指针**：`毕设/innovation-points.md` L52-77
- **日期**：有效（最新 2026-06-13）
- **下游**：C `{创新点表述范例}`

## D 维度：工作流（手搓写作流程逆向工程 → paper-write 设计输入）

### D1. S003 模板提取 L1/L2/L3 + 11 轮失败（thesis-direction-pivot）
- **来源**：粗扫1
- **价值**：模板提取 3 层级 L1/L2/L3 定义 + D009"人写 LLM 查"决策 + **11 轮失败策略 + 108 个问题清单反面教训**
- **指针**：`thesis-direction-pivot/S003-template-extraction-methodology.md` 11轮失败 L11-33 + 三方交叉审查 L196 + 最终模板格式 L231（注：L1/L2/L3 是模板提取层级非行号；pilot 校准）
- **日期**：有效
- **下游**：D `{手搓步骤=模板提取 L1/L2/L3，反面教训=11 轮失败}`

### D2. PROMPT-001-writing-task-f 对话隔离写作流（D 顶配）
- **来源**：粗扫3
- **价值**："每对话写 1 章，串行 Ch2→Ch3→Ch4→Ch5"对话隔离写作流 + **token 管理硬规范（主对话严禁直接读 section-outline/writing-patterns 等大文件，全由子 agent 消化）** + 动词强度控制表——**这是 user CLAUDE.md"主对话不读大文件"纪律的实战来源**
- **指针**：`.sessions/2026-05-31-thesis-writing/PROMPT-001-writing-task-f.md`（24.6K）对话隔离+token管理 L1-30 + 5步循环 L140-253 + 8维审查R1-R8 L254-304 + 跨章一致性 L317 + 范文铁律1-4 L561（pilot 校准）
- **日期**：有效
- **下游**：D `{手搓步骤=对话隔离写作，vs paper-write=需对照，优化建议=token 管理规范}`

### D3. S002 D006 失效反面教材 — 如何不让 AI 跑偏
- **来源**：粗扫1
- **价值**：R002 在未经导师确认下自动改 Ch3（均衡→级联分析），D006 失效完整文档——"AI 自动决策越界"的最佳反面教材
- **指针**：`thesis-direction-pivot/S002-systematic-search-and-direction-rethink.md`（D006 失效段）
- **日期**：有效
- **下游**：D `{手搓流程的护栏=导师确认门控}`

### D4. innovation-points.md R1-R7 写作规则
- **来源**：细扫A
- **价值**：创新点写作 7 规则——只说方向不说结果 / 必须有退路 / 有文献对标 / 不和教训矛盾 / 专硕标准 / 递进关系 / 初步数据不否定可行性
- **指针**：`毕设/innovation-points.md` L11-46（R1=L11/R2=L17/R3=L21/R4=L25/R5=L32/R6=L39/R7=L46；pilot 校准确认精确）+ L99-104（v1→v6 迭代否决记录）+ L116（VV公式bug）
- **日期**：有效（最新）
- **下游**：D `{手搓步骤=创新点写作流程 + 自检}`

### D5. CONCLUSIONS-VERIFY-PLAN.md 数字审计三步法
- **来源**：细扫A
- **价值**：Step1 6 并行 agent 源文件扫描 / Step2 交叉验证 / Step3 数字审计用确定性 grep；"CONCLUSIONS.md 是权威文件，源文件矛盾以它为准"
- **指针**：`毕设/CONCLUSIONS-VERIFY-PLAN.md` L19-44（+ L63 优先级规则）
- **日期**：有效（2026-06-02）
- **下游**：D `{手搓步骤=数字一致性审计工作流，优化建议=确定性 grep 反向检查}`

### D6. bib 根因分析 + search2bib 缺失（paper-write 功能 backlog）
- **来源**：细扫B
- **价值**：bib 生成链路审计 `content.md → materials.md（不存元数据）→ references.bib（手动拼）`，**核心缺失是"搜索 JSON→bib 条目"自动转换（search2bib）**——搜索数据里有作者但 bib 没用；工具改进表 4 项（search2bib / 中文作者批量补全 / CSL 本地化 / bib 质量检查脚本）
- **指针**：`projects/thesis-figures/bib-quality-issues.md` L67-103（根因）/ L96-103（改进）/ L105-113（修复计划）
- **日期**：有效（2026-05-28）
- **下游**：D `{vs paper-write=缺 search2bib 自动转换，优化建议=加 search2bib 工具}`

### D7. citation 修复扩散点 + 四级优先级修复
- **来源**：细扫B
- **价值**：1 个 DOI 错误必须同步改 3 文件（references.bib / kaiti-report.md / material-chapter-literature.md）——缺引用单源真相；立即/短期/中期/长期四级优先级修复计划
- **指针**：`citation-verification/VERIFICATION_SUMMARY.md` L34-39（扩散点）/ L113-117（优先级）
- **日期**：有效
- **下游**：D `{手搓步骤=引用一致性追踪，优化建议=加引用单源真相}`

### D8. S017 论文精读工作流
- **来源**：粗扫1
- **价值**：论文精读 3 批 7 篇并行 agent 工作流 + bib 文件创建流程 + Pandoc 编译验证
- **指针**：`thesis-direction-pivot/S017-thesis-writing.md`
- **日期**：有效
- **下游**：D `{论文精读 + 编译流程}`

### D9. PROMPT-024 全自动文献搜索（20K 长上下文 prompt）
- **来源**：粗扫1
- **价值**：全自动文献搜索的 prompt 模板（20K 长上下文设计）+ Ch4 失败始末
- **指针**：`thesis-direction-pivot/PROMPT-024-ch4-literature-innovation-scout.md`
- **日期**：有效
- **下游**：D `{文献搜索 prompt 设计}`

### D10. H024/H025 仿真审计 + 压测交接模板
- **来源**：粗扫1
- **价值**：仿真代码审计 + 压测的完整交接流程模板（任务清单 + 验证阈值表）
- **指针**：`thesis-direction-pivot/H024-sim-consolidation.md` + `H025-ch3-audit-result.md`
- **日期**：有效
- **下游**：D `{交接流程范式}`

### D11. 写作质量规范.md(732 行) 工作流
- **来源**：粗扫2
- **价值**：写作质量工作流（§9 AI 偏差见 A1，§12.4 Popper 见 B2）
- **指针**：`毕设/写作质量规范.md`
- **日期**：有效
- **下游**：D `{写作质量工作流}`

### D12. design-decisions R01-R16 否决索引（D 视角，否决范式）
- **来源**：粗扫2
- **指针**：`毕设/design-decisions.md`（613 行，R01-R16）
- **下游**：D `{否决记录范式}`（亦见 B19）

### D13. gen_test.py 写作质量自动测试工具
- **来源**：粗扫3
- **价值**：把写作质量维度做成可测脚本——写作质量自动化的范式
- **指针**：`.sessions/2026-05-31-thesis-writing/gen_test.py`（10.9K）
- **日期**：有效
- **下游**：D `{写作质量自动化}`

### D14. S003-methodology-reset 三轮 28 子 agent 验证（thesis-writing）
- **来源**：粗扫3
- **价值**：§1.2 三轮 28 子 agent 验证，文献综述段落验证到答辩可追问级别
- **指针**：`.sessions/2026-05-31-thesis-writing/S003-methodology-reset-and-research.md`（注意文件名是 -reset-and-research.md 非 -reset.md；38.3K；三轮 28 子 agent 验证 L298-340、第三轮重验 L598-641；对话 C 校准）
- **日期**：有效
- **下游**：D `{验证工作流}`
- **注**：⚠️ 区分 `thesis-direction-pivot/S003`（D1，模板提取）vs `thesis-writing/S003`（本条，三轮验证），不同文件

### D15. thesis-lessons TL-20-25（写作+验证硬货）
- **来源**：粗扫3
- **价值**（全 25 条有效，无 pivot 前残留）：
  - TL-20 跑仿真前先建理论预期，偏离即查
  - TL-21 文档数字审计用确定性 grep，不依赖 agent 链式标记
  - TL-22"震撼结果"先花 5 分钟查物理前提
  - TL-23 验证完毕再写文档，好结果触发冷静期
  - TL-25 仿真起飞检查单
- **指针**：`thesis-lessons.md`（TL-20-25）
- **日期**：全有效
- **下游**：D `{写作 + 验证硬货}`

### D16. S006 答辩预演 5 问 + 三级 Tier 加强策略
- **来源**：细扫C
- **价值**：答辩预演 5 问（"size gen 是已知性质你贡献是什么"/"三章同质化"/"局限性"/"创新性"）+ 三级 Tier 分工加强策略 + 跨章元分析数据收集需求表
- **指针**：`S006` L276-309（答辩+Tier）/ L311-322（跨章分析）
- **日期**：方法论可继承
- **下游**：D+B `{答辩预演 + 加强策略工作流}`

### D17. cnki-thesis-survey CAJ 工具链痛点
- **来源**：细扫B
- **价值**：CAJ 格式无法自动转 PDF——工具链痛点
- **指针**：`projects/thesis-fso/cnki-thesis-survey.md` L554-567
- **日期**：有效
- **下游**：D `{优化建议=paper-write 加 CAJ 处理}`

### D18. literature_notes 三级文献筛选 + 参数溯源审计（D 视角）
- **来源**：细扫B
- **价值**：必读 8 + 建议读 13 + 二轮补充三级筛选（每篇标"引用数+原因"）+ 参数溯源审计
- **指针**：`projects/thesis-fso/literature_notes.md` L32-79（筛选）/ L202-237（溯源）
- **日期**：有效
- **下游**：D `{文献筛选 + 参数溯源流程}`（亦见 C11）

### D19. 毕设/自管理极完整 — 复用原则
- **来源**：粗扫2 关键观察
- **价值**：毕设/ 自管理极完整（规范/决策/批注/审查/验证/审计体系齐全）——**下游应"最大化复用现有结构"**，而非从零建
- **日期**：有效
- **下游**：D `{复用原则，paper-write 设计的元约束}`

---

## 关键洞察（6 agent 交叉印证）

1. **B 维度弹药最足**：评估标准被多源叠加蒸馏得最彻底（导师批注 + Popper 判据 + 8 维 rubric + 引用质量 + 空白分级 + 证伪表），paper-eval S025-S028 评估盲区素材极充足。
2. **最值钱的偏"自审体系"**：越细扫，越发现金矿是 user 对自己论文的审查产物（8 维 rubric / 安全等级 / 证伪表 X-01~X-09 / 符号消歧 / 创新点迭代）——不是外部范文或导师批注。**user 手搓写作流程的核心是"自审"**，这对 paper-write 管线设计是关键需求模型。
3. **A 维度有罕见标本**：`innovation-points.md` v1→v6 是"改不到位/AI 帮倒忙"的完整实证（措辞歧义/物理有效性/证伪），这种元过程在写作痛点里极稀缺。
4. **新旧方向对照让 C few-shot 价值翻倍**：开题报告.md（GNN）+ thesis-framework.md（FSO）= 同作者不同方向的绪论风格对照——GNN 绪论做"风格锚"，FSO 绪论做"技术正确性锚"。
5. **旧方向方法论 ~60-70% 可继承**：R003 贡献声称写法 85%（技术例子 15% 作废）+ S006 评审权重表/答辩预演（B/D 独有维度）。印证 R001"方法论可转移、技术作废"预判。
6. **细扫补救了 1 个误判**：`stages/thesis-materials.md` 被细扫B 认为是 paper-write 蓝图，但 user 2026-06-15 判定"很旧别管"，排除（D003）。
7. **R001 漏点预判全中**：七漏点 2/3/5/6/7 极高确认，1/4 高；草稿 diff 漏点 1 已修正为批注/trace/正反例，且 pilot 证实创新点迭代（A6）是更稀有的"一个版本内部微调"实证。

## pilot 建议（按素材形态挑，验证扫描模板统一处理能力）

pilot 目的：验证"扫描模板把不同形态原文映射到契约字段"的可合并性（分层试错法 P3，10-20 篇）。按形态各挑 1-2 份，共 ~12 份：

| 素材形态 | pilot 文件 | 验证什么 |
|---------|-----------|---------|
| 规则清单 | R011（C1）/ innovation-points R1-R7（D4） | 规则条目能否映射成 A/B/D 字段 |
| 批注原话 | advisor-revision 批注（B1）/ S001 四底线（B3） | 导师原话能否映射成 B 批评点 |
| diff 对比 | 正文/Ch2-reviews.md（C2/B6）/ R003 Before→After（C6） | 前后对比能否映射成 C few-shot |
| 审查 rubric | Ch2-reviews 8 维（B5）/ CONCLUSIONS 安全等级（B8） | rubric 能否映射成 B 维度 |
| 失败案例 | S024 B2 证伪（B9）/ AI 编造 DOI（B12） | 失败案例能否映射成 B 批评点 + A 痛点 |
| 命名方法论 | cnki-survey 章节命名（C10）/ figure-composition（C5） | 方法论能否映射成 C few-shot |
| 工作流蓝图 | S003 L1-L3（D1）/ PROMPT-001 对话隔离（D2） | 工作流能否映射成 D 步骤清单 |

**pilot 通过判据**：每个形态的文件都能填满对应契约字段，且不同 agent 提取的同类素材可合并（防 M1 管道断裂）。

## 结论

1. **扫描覆盖完整**：6 agent（3 粗扫 + 3 细扫）覆盖 thesis-direction-pivot(98) + 毕设/(主规范+角落) + 三写作专题 + 根目录 + 4 处盲区（citation-verification / projects / stages / _archive 旧方向）。`.omc/` 排除。剩余未扫的是旧方向技术内容/非写作过程类，价值递减。
2. **四维素材源充足**：A 10 条 / B 22 条 / C 22 条 / D 19 条，共 73 条素材源。B 最丰富（多源叠加），A 有罕见标本，C 有新旧方向对照，D 有 paper-write 功能 backlog。
3. **可进 pilot 阶段**：素材源清单（本文件）+ 下游契约字段（D002）齐备，pilot 12 份候选已定。

## 对决策的影响

- **D003 新建**：排除 `stages/thesis-materials.md`（user 2026-06-15 判定"很旧别管"）。该文件"引用质量 rubric（中文≥10 篇/预印本率≤30%）"暂无替代源，标"待补"（B11）。
- **R001 漏点预判全中**：七漏点核对结果记入本文件"关键洞察 7"。
- **C 维度素材源扩展**：R001 修正的"草稿 diff → 批注/trace/正反例"基础上，新增 Ch2-reviews.md diff（C2）+ R003 贡献声称 16 条 Before→After（C6）+ innovation-points 迭代（A6）。
- **pilot 可启动**：本文件是 pilot 的素材源索引，扫描模板设计可直接基于本文件 + D002 契约字段。
