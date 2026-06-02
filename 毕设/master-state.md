# 学位论文 Master State

> **每次 thesis 相关对话开始时必须读此文件**
> 最后更新: 2026-06-02（语言禁忌+事实性审查完成后更新）

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
├── formulas-master.md        ← 公式总表（101条，Ch2-Ch5）
├── formulas-index.md         ← 公式索引（快速查找）
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
- 无（Task 0~E + PROMPT-007验证+文档同步+语言审查 全部完成，等待开 Task F 写初稿）

**最近的完成项**:
- [x] 语言禁忌+事实性审查（2026-06-02）：12个文件~71处修改（旧VV数据/NMSE升级/FPGA违规/术语统一/措辞禁忌）
- [x] TERMS.md 术语规范更新（VV平均窗口+归一化辐照度全文统一）
- [x] PROMPT-006 Task E: section-outline.md（867行，Ch2-Ch5 各节详细写作大纲）
- [x] PROMPT-006 Task A: formula-inventory.md（101条公式盘点+Ch4缺口分析）
- [x] PROMPT-006 Task B: writing-patterns-paragraph.md（1448行段落模式）+ writing-patterns-sentence.md（1019行句式库）
- [x] PROMPT-006 Task C: writing-phrases.md（写作用语库）
- [x] PROMPT-006 Task D: figure-table-plan.md（27张开题图表+夏兆宇对标）
- [x] PROMPT-006 Task 0: 丁爽/张思齐/吴志航转换+评估
- [x] 写作材料统一化（5文件→2文件，Phase A/B/C/D 全完成）
- [x] 8-agent 审查（2参数+6术语）→ TERMS.md 建立
- [x] design-decisions.md（56条决策+14条否决方案）
- [x] symbol-conventions.md
- [x] §1.1 初稿 v3（董凡风格+夏兆宇结构适配，最佳版本）
- [x] §1.2 初稿 v1-v2
- [x] formulas-ch5-fpga.md
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
| Ch3/Ch4 同步 | `写作材料/formulas-chulas-ch3ch4-sync.md` | ✅ 旧格式 |
| Ch4 KF | `写作材料/formulas-ch4-kf.md` | ✅ |
| Ch5 FPGA | `写作材料/formulas-ch5-fpga.md` | ✅ |
| **公式总表** | `formulas-master.md` | ✅ 101条（Ch2:38 + Ch3:21 + Ch4:14 + Ch5:28） |
| **公式索引** | `formulas-index.md` | ✅ 快速查找 |
| **公式盘点** | `写作材料/formula-inventory.md` | ✅ Task A：对比表+Ch4缺口分析 |

### 写作准备类（统一化完成）

| 文档 | 路径 | 状态 | 用途 |
|------|------|------|------|
| **段落级模式（统一）** | `写作材料/writing-patterns-paragraph.md` | ✅ 1448行 | Ch2-Ch5段落结构+4附录（量化/决策/顺序/映射） |
| **句级句式（统一）** | `写作材料/writing-patterns-sentence.md` | ✅ 1019行 | Ch2-Ch5句式库189条+速查表 |
| **写作用语库** | `写作材料/writing-phrases.md` | ✅ | 公式引入/衔接/结果描述 |
| **图表规划** | `写作材料/figure-table-plan.md` | ✅ | 逐章图表+开题20+清单+夏兆宇对标 |
| **各节写作大纲** | `写作材料/section-outline.md` | ✅ | Ch2-Ch5每节详细大纲（公式/图表/句式/衔接） |
| S1.2写作参考 | `写作材料/writing-reference-s1.2.md` | ✅ | §1.2写作素材 |
| 旧文件（5个） | `写作材料/archive/` | 归档 | B1/B2/B3原始提取文件 |

### 写作草稿

| 文档 | 路径 | 状态 |
|------|------|------|
| §1.1 v3（最佳） | `写作材料/draft-s1.1-v3.md` | ✅ DeepSeek 92分 |
| §1.2 v2 | `写作材料/draft-s1.2-v2.md` | ✅ 最新版 |
| 开题报告研究方案 | `开题报告/03-研究方案.md` | ✅ 骨架(12.2K字)，待按section-outline深化 |

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
| thesis-writing-prep | `.sessions/2026-05-31-thesis-writing-prep/` | **active** | Task 0~E全完成，待开Task F写初稿 |
| thesis-direction-pivot | `.sessions/thesis-direction-pivot/` | active | 方向探索主专题 |
| thesis-simulation-consolidation | `.sessions/thesis-simulation-consolidation/` | active | 仿真代码整合 |
| thesis-final-review | `.sessions/thesis-final-review/` | active | 8-agent审查 |
| 2026-05-30-ch3-direction-exploration | `.sessions/2026-05-30-ch3-direction-exploration/` | dormant | Ch3 BER推导（S002） |

### 已归档（非 thesis）

- `2026-05-13-*` ~ `2026-05-20-*`: 旧方向（HGAT/RIS/ISL/路由等），全部废弃
- `direction-scouting`, `framework-evolution`: 旧框架专题

---

## 仿真代码

### 主仿真库

`projects/simulation/` 下（common.py + experiments/）。

| 文件 | 用途 | 状态 |
|------|------|------|
| `common.py` | 核心函数库（VV/BPS/DPLL/KF/Fixed + 信道生成） | ✅ 含BPS |
| `experiments/multi_seed_sweep.py` | 多种子 SNR-BER 扫描（10种子×5方法×3湍流） | ✅ |
| `experiments/plot_snr_curves.py` | SNR 曲线绘图（5方法含BPS） | ✅ |
| `experiments/sim_nmse_vs_ber.py` | NMSE 灵敏度曲线（QPSK下无影响） | ✅ |

### 探索与验证脚本

`projects/thesis-figures/simulation/` 下（26个文件）。

| 类别 | 关键文件 | 用途 |
|------|---------|------|
| Ch3 BER | `sim_ch3_ber_closed_form.py`, `sim_ch3_ber_bounds.py` | 闭合解+界分析 |
| Ch3 设计 | `sim_ch3_strengthening.py`, `sim_cascade_robustness.py`, `sim_cascade_corrected.py` | 设计准则+级联 |
| Ch4 系统分析 | `sim_ch4_systematic_analysis.py` | VV/BPS/DPLL/KF对比 |
| Ch4 KF | `sim_ch4_kf_*.py`（5个） | KF各维度验证 |
| KF 应力测试 | `sim_kf_stress_*.py`（8个） | A1-D5全维度 |
| 其他 | `sim_bias_variance_foe.py`, `sim_direction_a.py`, `sim_tune_coefficients.py` | FOE/参数调优 |

---

## 开题报告待办

### 官方模板 7 部分

| # | 部分 | 状态 | 负责对话 |
|---|------|------|---------|
| 一 | 选题依据 | §1.1✅ §1.2 v2完成 | 待精修 |
| 二 | 研究内容 | 待写（短，类似摘要） | Task F |
| **三** | **研究方案** | **骨架✅(12.2K字) 待按section-outline深化** | Task F |
| 四 | 进度安排 | 待写（半页纸） | Task F |
| 五 | 预期成果 | 待写 | Task F |
| 六 | 创新之处 | framework有草稿 | Task F |
| 七 | 研究基础 | 待写 | Task F |

### 写作前置材料就绪状态

| 前置任务 | 产出 | 状态 |
|---------|------|------|
| Task 0: 论文转换 | 丁爽/张思齐/吴志航 markdown | ✅ |
| Task A: 公式盘点 | formula-inventory.md | ✅ Ch4缺口已标注 |
| Task B: 段落模式 | paragraph(1448行)+sentence(1019行) | ✅ |
| Task C: 写作用语 | writing-phrases.md | ✅ |
| Task D: 图表规划 | figure-table-plan.md（27张开题） | ✅ P0=15张 |
| Task E: 各节大纲 | section-outline.md（867行） | ✅ Ch2-Ch5全覆盖 |

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
