# 专题: thesis-writing-prep

> 状态: active | 创建: 2026-05-31
> 目标: 为开题报告和论文写作准备规范文档（符号/公式/决策/图表）

## 进展线索

- PROMPT-001 → 符号+术语合并 → 产出: TERMS.md（扩充）
- PROMPT-002 → 公式推导验证 → 产出: formulas-master.md（新建）
- PROMPT-003 → 设计决策提取 → 产出: design-decisions.md（已完成，56条决策+14条否决方案，4个来源待补充）
- PROMPT-004 → 研究方案骨架 → 产出: `开题报告/03-研究方案.md`（12.2K字，6大节完整骨架+内容，质量检查全通过）
  - Phase 1 完成：3个分析agent（R1旧开题报告结构、R2闫佳欣/曾嘉论文结构、R4材料充足度评估）
  - 关键发现：开题=毕业论文20-25%；正交双维度切分（设计+验证）；结论式公式（不推导）
  - 各节完成度：§3.1概述✅ §3.2系统模型(充实)✅ §3.3信道估计+级联(核心贡献)✅ §3.4载波同步(充实)✅ §3.5 FPGA(骨架)✅ §3.6可行性✅
- PROMPT-005 → 文献清单更新+bib同步 → 产出: material-chapter-literature.md 扩充 + references.bib 同步（✅ 已完成）
- PROMPT-006 → 写前提取与规划 → 产出: formula-inventory / writing-patterns / writing-phrases / figure-table-plan（Task 0 ✅ 已完成，其余待执行）
- PROMPT-007 → 仿真正确性验证 → **全部完成**（42 agents）。核心结论不变。产出: `毕设/写作材料/verification/verification-report.md` + SNR曲线PDF + BPS移植+10种子扫描
  - Phase 1+2+复验+10种子稳定验证+3深度调查+BPS移植+SNR曲线
  - 15 条已确认结论，BPS 行为与 VV 同量级（无优势）
  - 文档同步完成：6个文件修改（thesis-framework/03-研究方案/section-outline/figure-table-plan/thesis-status/formulas-ch4-kf），验证 PASS
  - 剩余缺口: Ch3 NMSE vs BER 曲线（建议补）、thesis-status 数字更新（✅已完成）
- **语言禁忌+事实性审查**（2026-06-02，6 agents）
  - 方法：按结论维度派 3 审查 agent（Ch3/Ch4/通用），每 agent 持 SPEC grep 全文件
  - 发现 ~65 条问题：旧VV公式数据(17处) + NMSE描述升级(14处) + FPGA违规(14处) + 术语(15处) + 措辞(11处)
  - 额外调查：analyst 验证"VV平滑窗口"和"信道增益"禁忌合理性 → 确认合理（全文统一用词）
  - 修复：3 修复 agent + 主线程直修，共 12 个文件 ~71 处修改
  - TERMS.md 更新：恢复"VV平均窗口"和"归一化辐照度"为全文统一用语，section 9 添加混用速查说明
  - **未修**：成品文档（draft-s1.*.md、正文/Ch2-*.md）待后续处理
- **创新点+结论+数据全面对齐**（2026-06-02 续，9 agents）
  - 摸底：9路grep → 3审计agent按目录分扫（51文件）→ 3修复agent（R1）
  - 验证grep发现残留 → 2修复agent深度清理formulas+material-cards（R2）
  - 深扫12新维度（VV/BPS旧数据/100种子/EKF/揭示/ω_n等）→ 3修复agent（R3）
  - 总计~179处修改/25文件：创新点3→2(20)/自适应→分析框架(50)/FPGA(15)/揭示→分析(13)/旧数据(6)/ω_n(4)/种子数(3)/归档标注(9)
  - 关键修改：material-section-content-cards.md 34处"自适应"全面清理、CONCLUSIONS.md ω_n单位修正、thesis-framework.md "揭示"清零
  - 旧版draft(v1/v2/v3)全部添加归档标注，不再修改
  - **压缩后继续扫**（2026-06-02 续2）：7路grep + 2个explore agent，修3文件7处（PPT三列→两列/PROMPT-009自适应清理/Ch2-reviews揭示→表明）。Ch2正文/Ch2-guides/figure-table-plan/formula-inventory确认干净。累计~186处/28文件。section-outline"揭示"4处待用户决定。
- **S005 创新点重组决策**（2026-06-02）
  - 核心决策：3个创新点→2个，FPGA降级为工程验证，Ch4升级为"拟提出湍流感知自适应载波同步方案"
  - FPGA不是创新点：曾嘉论文对标（FPGA是验证不是创新），闫佳欣是工程硕士不对标
  - Ch3级联分析是合法贡献：Han 2022(JLT)直接对标，Wang 2025硕士论文对标
  - Ch4方向：从"系统性分析"升级为"湍流感知自适应载波同步方案"（估计湍流→选算法→调参数）
  - 开题篇幅评估：当前~38页，需补到50-55页；正文压缩后放入研究方案
  - PPT结构确认：研究意义→研究目标与内容→技术路线→预期成果
  - 待改6个文件（thesis-framework/thesis-status/draft-s1.3-1.4/03-研究方案/draft-s1.1/section-outline）
  - 崩盘风险低（IP1数学事实/数据充分，IP2已有数据+简单if-else）
  - 常识性风险中等（有文献空白但非突破性贡献，专硕定位安全）

## 不变量

- 所有产出文件放在 `毕设/写作材料/` 下
- 子 agent 遵守并发控制（一次≤3个）
- 公式验证需有出处（引用文献或标注"自推"）
- 符号与 TERMS.md 保持一致

## 范围边界

- 原始目标: 创建4份规范文档 + 研究方案骨架
- 当前范围: 同上
- 明确不含: 不写开题报告正文（那是写作对话的事）、不改仿真代码

## 未决项

- 图表规划待单独开对话（依赖公式/符号产出）
- 表格规划待单独开对话
- 夏小雨师兄论文待获取
