# 学位论文 Master State

> **每次 thesis 相关对话开始时必须读此文件**
> 最后更新: 2026-05-31

## 毕设目录结构

```
毕设/
├── master-state.md          ← 本文件（每次对话必读）
├── TERMS.md                 ← 术语规范（唯一真相源）
├── symbol-conventions.md    ← 数学符号约定
├── design-decisions.md      ← 设计决策记录（56条+14否决）
├── thesis-framework.md      ← 框架草稿 v2
├── thesis-status.md         ← 状态看板（目录/决策/仿真/风险）
├── thesis-preparation-checklist.md ← 准备清单+缺口分析
├── 写作材料/                 ← 公式+文献（每章写作时的参考资料）
├── 开题报告/                 ← 开题草稿+写作素材（draft-s1.*）
├── 表格模板/                 ← 官方表格+培养办法
├── 开题PPT/                  ← 答辩PPT各版本+模板+素材
├── graduate-thesis/          ← LaTeX 模板（bithesis）
└── 旧本科代码/               ← 归档
```

## 论文信息

- **题目**: 星地激光通信信号处理关键技术研究
- **学位**: 硕士 | **导师方向**: 信道建模→预均衡→同步
- **当前阶段**: 开题报告写作（一周内完成，2026-05-29 起算）

## 当前状态

**正在进行的对话**:
- 写作对话: §1.2 国内外研究现状（另一对话在写，已到 v2）
- 规范对话（本对话）: 准备规范文档，已产出提示词

**最近的完成项**:
- [x] 8-agent 审查（2参数+6术语）→ TERMS.md 建立
- [x] design-decisions.md（56条决策+14条否决方案，另一对话完成）
- [x] symbol-conventions.md（另一对话完成）
- [x] §1.1 初稿 v3（董凡风格+夏兆宇结构适配，最佳版本）
- [x] §1.2 初稿 v1-v2
- [x] formulas-ch5-fpga.md（另一对话创建）
- [x] 4 个写作准备提示词（PROMPT-001~004）

---

## 重要文档索引

### 规范类（写作前必读）

| 文档 | 路径 | 状态 | 用途 |
|------|------|------|------|
| 术语规范 | `写作材料/TERMS.md` | ✅ 完成 | 全文用词唯一真相源 |
| 符号约定 | `写作材料/symbol-conventions.md` | ✅ 完成 | 数学符号统一 |
| 设计决策 | `写作材料/design-decisions.md` | ✅ 完成 | 技术选择记录 |
| 框架草稿 | `写作材料/thesis-framework.md` | ✅ v2 | 全文章节框架 |
| 状态看板 | `写作材料/thesis-status.md` | ✅ | 目录/决策/仿真/风险 |
| 准备清单 | `写作材料/thesis-preparation-checklist.md` | ✅ | 缺口分析+并行计划 |

### 公式类

| 文档 | 路径 | 状态 |
|------|------|------|
| Ch2 系统模型 | `写作材料/formulas-ch2-system-model.md` | ✅ 旧格式 |
| Ch3 链路性能 | `写作材料/formulas-ch3-link-performance.md` | ✅ |
| Ch3/Ch4 同步 | `写作材料/formulas-ch3ch4-sync.md` | ✅ 旧格式 |
| Ch4 KF | `写作材料/formulas-ch4-kf.md` | ✅ |
| Ch5 FPGA | `写作材料/formulas-ch5-fpga.md` | ✅ |
| **公式总表** | `写作材料/formulas-master.md` | ❌ 待创建（PROMPT-002） |

### 写作草稿

| 文档 | 路径 | 状态 |
|------|------|------|
| §1.1 v3（最佳） | `写作材料/draft-s1.1-v3.md` | ✅ DeepSeek 92分 |
| §1.2 v2 | `写作材料/draft-s1.2-v2.md` | ✅ 最新版 |
| 开题报告研究方案 | `写作材料/开题报告/03-研究方案.md` | ❌ 待创建（PROMPT-004） |

### 文献类

| 文档 | 路径 | 状态 |
|------|------|------|
| 参考文献库 | `写作材料/references.bib` | ✅ 146条 |
| 文献清单 | `写作材料/material-chapter-literature.md` | ✅ 165篇 |
| 精读笔记 | `写作材料/literature-notes-ch1-ch2.md` | ✅ 776行85条 |

---

## 活跃专题

### thesis 相关

| 专题 | 路径 | 状态 | 说明 |
|------|------|------|------|
| thesis-writing-prep | `.sessions/2026-05-31-thesis-writing-prep/` | **active** | 4个提示词，写作规范准备 |
| thesis-direction-pivot | `.sessions/thesis-direction-pivot/` | active | 方向探索主专题 |
| thesis-simulation-consolidation | `.sessions/thesis-simulation-consolidation/` | active | 仿真代码整合 |
| thesis-final-review | `.sessions/thesis-final-review/` | active | 8-agent审查 |
| 2026-05-30-ch3-direction-exploration | `.sessions/2026-05-30-ch3-direction-exploration/` | dormant | Ch3 BER推导（S002） |

### 已归档（非 thesis）

- `2026-05-13-*` ~ `2026-05-20-*`: 旧方向（HGAT/RIS/ISL/路由等），全部废弃
- `direction-scouting`, `framework-evolution`: 旧框架专题

---

## 仿真代码

全部在 `projects/thesis-figures/simulation/` 下。

| 文件 | 用途 | 状态 |
|------|------|------|
| `sim_ch3_ber_closed_form.py` | BER闭合解验证 | ✅ |
| `sim_ch3_strengthening.py` | 设计准则+鲁棒性 | ✅ |
| `sim_cascade_robustness.py` | 级联灵敏度（6/6 PASS） | ✅ |
| `sim_ch4_systematic_analysis.py` | VV/BPS/DPLL对比 | ✅ |
| `sim_ch3_ber_bounds.py` | BER界分析 | ✅ |

---

## 开题报告待办

### 官方模板 7 部分

| # | 部分 | 状态 | 负责对话 |
|---|------|------|---------|
| 一 | 选题依据 | §1.1✅ §1.2进行中 | 写作对话 |
| 二 | 研究内容 | 待写（短，类似摘要） | 写作对话 |
| **三** | **研究方案** | **❌ 最大缺口** | PROMPT-004 |
| 四 | 进度安排 | 待写（半页纸） | 写作对话 |
| 五 | 预期成果 | 待写 | 写作对话 |
| 六 | 创新之处 | framework有草稿 | 写作对话 |
| 七 | 研究基础 | 待写 | 写作对话 |

### 待验证项

| 项目 | 影响 | 状态 |
|------|------|------|
| Elfiky "15%复杂度降低" | §1.2.1引用 | 待查原文 |
| Paillier 100MHz/1.4ms | §1.2.2数据 | 待查原文 |
| 夏小雨师兄论文 | 导师要求参考结构 | 待获取 |
| 4篇未验证论文 | 文献覆盖率 | 待确认 |

---

## 目录 v4（导师确认，已锁定）

```
第一章  绪论
第二章  星地激光通信系统与信道模型
第三章  大气湍流信道估计技术
第四章  低轨星地载波同步算法
第五章  接收端信号处理链FPGA设计与实现
第六章  总结与展望
```

## 关键约束

- Ch5 只有 2 个模块（FOE+DPLL，无符号定时同步）
- Ch4 不绑定具体算法（防御性写作 R003）
- ω_n 单位 rad/s（不是 MHz）
- h 是实值归一化辐照度（不是复信道系数）
- 禁止"首次"/"填补空白"/"oracle CSI"
