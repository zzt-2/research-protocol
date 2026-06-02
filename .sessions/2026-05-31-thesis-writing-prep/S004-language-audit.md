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

## 后续

- **成品文档待修**：draft-s1.1-v*.md, draft-s1.2-v*.md, draft-s1.3-s1.4-*.md, 正文/Ch2-*.md 中的 FPGA 违规和术语问题（约 10+ 处），用户说不急
- **100种子计划**：如果后续跑 100 种子仿真，需全局更新种子数 10→100
- **Ch3 NMSE vs BER 曲线**：verification-report 建议补充，尚未执行
