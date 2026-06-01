# PROMPT-007: 仿真正确性验证

> 专题: thesis-writing-prep | 优先级: P0
> **核心原则: TL-20 — 先有理论预期，再跑仿真。偏离预期立即调查。**
> Python: `~/.venvs/torch/bin/python`

## 必读（全局入口）

**本对话开始时必须读 `毕设/master-state.md`**——它是全局状态入口。

### 关键文件

**仿真规范（最重要）**:
- `projects/simulation/SPEC.md` — 仿真唯一真相源（信号模型、参数、方法、已验证事实）
- `projects/simulation/common.py` — 当前活跃的公共基础设施
- `projects/thesis-figures/simulation/SIM-SYSTEM.md` — 旧文档（标记已废弃，但记录了历史问题和修正过程）

**旧仿真代码**（`projects/thesis-figures/simulation/`）:
- `sim_ch3_ber_closed_form.py` — Ch3 BER 闭合解
- `sim_ch3_ber_bounds.py` — Ch3 BER 界分析
- `sim_ch3_strengthening.py` — Ch3 设计准则+鲁棒性
- `sim_cascade_robustness.py` — Ch3 级联灵敏度（⚠️ 用了旧 VV 公式）
- `sim_ch4_systematic_analysis.py` — Ch4 VV/BPS/DPLL 系统性分析
- `sim_ch4_kf_pilot_h.py` — Ch4 导频辅助 KF（最完整版本）
- `sim_kf_stress_common.py` — 压力测试公共模块（⚠️ 旧 VV 公式已在此文件中修正为正确版）
- `sim_kf_stress_*.py`（8 个）— Ch4 KF 压力测试 A1-D5

**新仿真代码**（`projects/simulation/`）:
- `common.py` — 修正后的公共模块
- `experiments/` — 新实验目录

**公式与文档**:
- `毕设/formulas-master.md` — 公式总表（101 条）
- `毕设/TERMS.md` — 术语规范
- `毕设/symbol-conventions.md` — 符号约定
- `毕设/thesis-status.md` — 状态看板（引用了仿真数字）
- `thesis-lessons.md` — 教训文档（TL-01~20）

**开题报告草稿**:
- `毕设/开题报告/03-研究方案.md` — 研究方案（12.2K 字）
- `毕设/thesis-framework.md` — 全文框架

## 背景

论文方向经历了多次重大调整，VV 公式 bug 修正后多个结论被推翻（见 SPEC.md §6.2-6.4）。当前仿真分布在两个目录：
- 旧目录（`projects/thesis-figures/simulation/`）：Ch3 仿真在此，部分用了旧 VV 公式
- 新目录（`projects/simulation/`）：只有 common.py，尚未迁移 Ch3 仿真

**核心风险**: 仿真结果可能存在未发现的 bug、参数错误、或偏离理论预期的问题。任何被答辩老师发现的错误都会严重影响可信度。

**TL-20 教训**: 之前 VV 公式 bug 导致 BER 偏差 1800× 但长期未发现，根本原因是跑仿真时没有理论预期对照。本对话必须避免重蹈覆辙。

## 产出目录结构

所有产出放在 `毕设/写作材料/verification/` 下：

```
毕设/写作材料/verification/
├── phase1-research/                    ← Phase 1 调研文件（每个 agent 一个）
│   ├── _index.md                       ← 进度索引（主对话维护）
│   ├── ch3-ber-closed-form/
│   │   ├── V-01-gg-fading-baseline.md
│   │   ├── V-02-ber-floor-theory.md
│   │   ├── V-03-analytical-comparison.md
│   │   └── V-04-mc-validation-method.md
│   ├── ch3-ber-bounds/
│   │   ├── V-05-upper-bound-theory.md
│   │   ├── V-06-lower-bound-theory.md
│   │   └── V-07-bound-tightness-literature.md
│   ├── ch3-strengthening/
│   │   ├── V-08-estimation-error-ber-relationship.md
│   │   ├── V-09-dpll-sensitivity-theory.md
│   │   └── V-10-vv-sensitivity-theory.md
│   ├── ch3-cascade/
│   │   ├── V-11-cascade-sensitivity-theory.md
│   │   ├── V-12-vv-formula-correctness.md
│   │   └── V-13-pass-criteria-rationality.md
│   ├── ch4-systematic/
│   │   ├── V-14-vv-performance-expectations.md
│   │   ├── V-15-bps-performance-expectations.md
│   │   ├── V-16-dpll-performance-expectations.md
│   │   ├── V-17-foe-theory-and-accuracy.md
│   │   └── V-18-relative-ranking-expectations.md
│   ├── ch4-kf/
│   │   ├── V-19-kf-tracking-theory.md
│   │   ├── V-20-kf-vs-dpll-theory.md
│   │   └── V-21-kf-parameter-sensitivity.md
│   └── gap-analysis/
│       ├── V-22-thesis-claims-vs-simulations.md
│       ├── V-23-missing-simulations.md
│       └── V-24-priority-gaps.md
├── phase2-results/                     ← Phase 2 仿真结果+偏差标记
│   ├── _index.md
│   ├── R-ch3-ber-closed-form.md
│   ├── R-ch3-ber-bounds.md
│   ├── R-ch3-strengthening.md
│   ├── R-ch3-cascade.md
│   ├── R-ch4-systematic.md
│   └── R-ch4-kf.md
├── phase3-deviations/                  ← Phase 3 偏差调查
│   └── D-[编号]-[描述].md
├── phase4-consistency/                 ← Phase 4 文档一致性
│   ├── C-01-thesis-status-numbers.md
│   ├── C-02-symbol-terminology.md
│   └── C-03-formula-code-match.md
└── verification-report.md              ← 最终汇总报告
```

## 调研文件格式（统一标准）

每个调研 agent 写入的文件必须遵循此格式：

```markdown
# V-[编号]: [调研主题]

> 关联仿真: [文件名] | Phase: 1a | 批次: B[N]
> 状态: 完成 | 发现锚点数: [N]

## 调研问题
[1-2 句话说清楚要回答什么]

## 文献/理论发现
[每个发现标注来源：文献名/教材/推导]

## 量化预期
[具体数字范围，供 Phase 2 对照]

## Phase 2 检查清单
- [ ] 锚点 1: [条件] → 预期 [范围] → 实际 ___
- [ ] 锚点 2: [条件] → 预期 [范围] → 实际 ___
- [ ] 锚点 3: [条件] → 预期 [范围] → 实际 ___
```

## Phase 1: 理论预期建立 + 缺口分析

### 1a. 仿真理论预期（共 ~24 个调研 agent）

#### Ch3: BER 闭合解（4 个 agent）

**V-01: GG衰落QPSK BER 文献基线**
- 查 Al-Habash 2001 (GG分布原论文)、Petkovic 2023、Nistazakis 2008、Trisno 2009
- 目标: 确定 GG 衰落下 QPSK BER 的文献已知数量级
- 锚点示例: 弱湍流 α=4,β=3 在 20dB BER 应在什么量级

**V-02: BER floor 的物理原因和理论位置**
- 从 σ_I² → outage 概率 → floor 位置推导
- 三档湍流下 floor 应该在什么量级
- 锚点示例: 强湍流 BER floor ~1-5%

**V-03: GG分布 PDF 积分解析解的文献对照**
- 查 Proakis, Simon 的 QPSK 衰落 BER 闭合解标准形式
- 本论文的形式是否等价？积分变量替换是否正确？
- 锚点示例: 闭合解在 AWGN 极限（无衰落）下应退化为 Q(√(2γ̄))

**V-04: Monte Carlo 验证方法的正确性**
- MC 仿真 BER 的标准做法（最小样本数、置信区间、方差估计）
- 闭合解 vs MC 应差多少以内算正常
- 锚点示例: 95% 置信度下 BER~10⁻³ 需要多少样本

#### Ch3: BER 界（3 个 agent）

**V-05: 上界理论（Jensen/Markov/联合界）**
- 常用 BER 上界有哪些？哪个适用于 GG 衰落？
- 上界应比实际 BER 松多少倍？

**V-06: 下界理论（outage-based）**
- outage 概率作为下界的理论依据
- 下界与实际 BER 的差距预期

**V-07: 界的紧致性文献**
- 文献中 GG 衰落 BER 界的紧致程度
- 上界/下界之比在什么范围算合理

#### Ch3: 设计准则+鲁棒性（3 个 agent）

**V-08: 估计误差与 BER 的理论关系**
- h 估计 NMSE → 下游 BER 恶化的理论模型
- 一阶近似: ΔBER ∝ NMSE × 某个系数？
- 锚点示例: NMSE=10% 时 BER 恶化应在 1.5-3× 范围

**V-09: DPLL 对 h 不敏感的理论验证**
- σ²_φ = B_L·T_s/(2γ̄)，理论上不依赖 h（仅 γ̄）
- 但 MMSE 均衡用的 h_est 影响 sqrt(h) 项
- 锚点示例: DPLL 在 h 变化时 BER 波动应 <10%

**V-10: VV 对 h 敏感的理论验证**
- σ²_φ ∝ 1/(M(h)·γ̄·h)，h⁻⁰·⁶ 依赖
- 弱湍流 h 接近 1 敏感度低，强湍流 h 可到 0.01 敏感度高
- 锚点示例: VV 在强湍流 BER 应显著高于 DPLL

#### Ch3: 级联灵敏度（3 个 agent）

**V-11: 级联灵敏度分析的理论框架**
- 级联误差传播的理论模型（h_est error → downstream BER）
- 每级估计误差如何影响下一级？
- 锚点示例: 6 个测试场景的 PASS 标准物理依据

**V-12: VV 公式正确性的数学证明**
- `unwrap(angle(avg))/M` vs `unwrap(angle(avg)*M)/M` 哪个对？
- 从相位估计的数学原理推导正确公式
- 用简单数值例子验证（已知相位，检查两种公式输出）

**V-13: PASS 标准的合理性**
- 6/6 PASS 的 PASS 条件是什么？每个条件的物理依据？
- 条件是否过于宽松（什么都能 PASS）或过于严格？

#### Ch4: VV/BPS/DPLL 系统性分析（5 个 agent）

**V-14: VV 性能预期**
- VV 在 AWGN 下的理论性能（MSE、收敛窗口）
- VV 在衰落信道下的已知问题（深衰落、相位滑动）
- 锚点示例: 弱湍流 VV BER < 0.1%，强湍流失败率 >30%

**V-15: BPS 性能预期**
- BPS 与 VV 的理论差异（候选相位 vs 4th-power）
- BPS 在衰落下的已知表现
- 锚点示例: BPS 强湍流失败率应 ≥VV（因为更多自由度）

**V-16: DPLL 性能预期**
- 二阶 DPLL 的理论跟踪范围和稳态误差
- ω_n 与跟踪范围的数学关系
- 锚点示例: DPLL 在 20dB 应能跟踪 1MHz 残余频偏

**V-17: FOE 理论与精度**
- FFT 频偏估计的理论精度（Cramér-Rao bound）
- N_fft=1024、zero-padding 8192 下的理论精度
- 锚点示例: FOE 精度应在 kHz 级

**V-18: VV/BPS/DPLL 相对排名的理论预期**
- 从理论上谁应该最好？为什么？
- 弱/中/强湍流下的预期排名
- 锚点示例: 弱湍流三者都行，强湍流 DPLL >> VV ≈ BPS

#### Ch4: KF（3 个 agent）

**V-19: KF 载波跟踪的理论性能**
- 线性 KF 跟踪相位+频偏的理论精度
- 与 DPLL 的理论对比（两者都是二阶跟踪器）
- 锚点示例: KF 精度应与 DPLL 同量级

**V-20: KF vs DPLL 理论差异**
- KF 优势: 自适应增益、导频辅助
- KF 劣势: 需要导频开销、判决导引在深衰落不可靠
- 锚点示例: 弱/中湍流 KF ≈ DPLL，强湍流 KF 可能不如 DPLL

**V-21: KF 参数敏感性理论**
- Q 矩阵参数的理论含义（过程噪声）
- R 矩阵参数的理论含义（观测噪声）
- 锚点示例: Q 差 50× 应无明显影响（已验证），R 差 10× 呢？

#### 缺口分析（3 个 agent）

**V-22: thesis-status 引用数字 → 仿真文件映射**
- 逐条列出 thesis-status.md 中引用的具体数值
- 每个数值对应哪个仿真文件、哪个函数的输出
- 标记: 有仿真支撑 ✅ / 数字来源不明 ❌

**V-23: 论文声称 vs 仿真覆盖**
- 逐条列出 thesis-framework.md 和 03-研究方案.md 中的技术声称
- 每个声称是否有对应仿真证明？
- 标记缺口: 需要但未做的仿真

**V-24: 优先级排序的缺口清单**
- 合并 V-22、V-23、SPEC.md §7 未验证项
- 按对开题答辩的影响排序
- 给出: 必须补 / 建议补 / 可选补 三档

### 1b. 基础层验证（穿插在调研中或紧随其后）

**信号模型验证**:
- SNR 定义: 所有代码中 γ=γ̄·h 是否一致？无 γ̄·h²？
- 信号模型: r = √h·s·exp(jφ) + n 是否在所有代码中一致？
- 湍流参数: α,β 三档是否在所有代码中一致？

## Phase 2: 跑仿真 + 预期对照

每个仿真跑完后，读对应的 Phase 1 调研文件，逐项填写"检查清单"中的"实际"列。

### 结果文件格式

```markdown
# R-[仿真名]: 仿真结果

> 仿真文件: [路径] | 运行时间: [时间戳]
> 整体判断: ✅ 符合预期 / ⚠️ 部分偏离 / 🔴 严重偏离

## 运行参数
[实际使用的参数]

## 检查清单填写
- [x] 锚点 1: 预期 [范围] → 实际 [值] → ✅/⚠️/🔴
- [x] 锚点 2: ...
- [ ] 锚点 3: ...

## 严重偏离记录
[如有 ⚠️/🔴 项，详细记录]

## 需要进一步调查
[列出需要 Phase 3 跟进的问题]
```

### 跑仿真注意事项

1. **Ch3 仿真**在旧目录 `projects/thesis-figures/simulation/` 下运行
2. **Ch4 仿真**优先用新 `projects/simulation/common.py` 的修正版本
3. **cascade_robustness** 需要特殊处理：
   - 先用旧代码跑一次（记录旧结果）
   - 用新 common.py 的 VV 函数替换旧 VV 函数后重跑
   - 对比两次结果，确认 VV 公式修正的影响
4. 所有仿真记录运行环境（python 版本、numpy 版本、随机种子）

## Phase 3: 偏差调查

仅针对 Phase 2 标记为 ⚠️ 或 🔴 的项。

每个偏差调查写入 `phase3-deviations/D-[编号]-[描述].md`：

```markdown
# D-[编号]: [偏差描述]

> 关联仿真: [文件] | 关联锚点: V-[编号] | 严重度: 🔴/⚠️

## 偏差描述
[预期值 vs 实际值]

## 调查过程
[逐层排查：参数 → 公式 → 算法 → 理论预期本身是否有误]

## 根因
[最终结论]

## 修复建议
[具体方案]
```

## Phase 4: 文档一致性检查

在 Phase 2-3 确认了正确数字后，检查文档引用。

**C-01: thesis-status 数字验证**
- 逐条检查 thesis-status.md 中引用的 BER、失败率、改善倍数等
- 对照 Phase 2 实际仿真输出
- 标记: 正确 ✅ / 过时（修正前数字）⚠️ / 错误 🔴

**C-02: 符号术语一致性**
- 抽查 thesis-status.md、thesis-framework.md、03-研究方案.md 中的关键术语
- 对照 TERMS.md 和 symbol-conventions.md
- 重点: h(归一化辐照度)、ω_n(rad/s)、γ=γ̄·h、级联(非联合)

**C-03: 公式与代码对应**
- 抽查 formulas-master.md 中的关键公式
- 对照仿真代码实现
- 重点: VV 公式、DPLL 环路、SNR 定义

## Phase 5: 汇总

产出 `verification-report.md`：

```markdown
# 仿真验证报告

> 日期: [日期] | 仿真总数: [N] | Agent 总数: [N]

## 执行摘要
[N] 个仿真验证，发现 [N] 个问题（🔴 [N] / 🟡 [N] / 🟢 [N]）

## 严重问题（🔴）
[按影响排序]

## 重要问题（🟡）
[按影响排序]

## 轻微问题（🟢）
[列表]

## 缺口清单
| 缺口 | 影响 | 优先级 | 建议动作 |
|------|------|--------|---------|

## 已确认正确的结论
[列表]
```

## 操作约束

### 批次与压缩

- 每 batch ≤3 个 agent
- 每完成 15 个 agent，暂停并提示用户 `/compact`
- 压缩后第一步: 读 `_index.md` 恢复进度
- Phase 间是额外压缩点

### Agent 产出纪律

- **调研 agent**: 产出写入 `phase1-research/` 对应子目录的文件
- **仿真 agent**: 产出写入 `phase2-results/` 对应文件
- **返回主对话**: 只允许 ≤50 字总结（"完成，写入 X，发现 N 个锚点"）
- **主对话永远不读 agent 完整输出**，只读 agent 写入的文件（且按需读）

### 进度追踪

主对话维护 `_index.md`：

```markdown
# 验证进度索引

> 最后更新: [时间]

## Phase 1: 调研
| 编号 | 主题 | 状态 | 文件 |
|------|------|------|------|
| V-01 | GG衰落基线 | ✅ 完成 | ch3-ber-closed-form/V-01-...md |
| V-02 | BER floor理论 | 🔄 进行中 | — |
| ...

## Phase 2: 仿真
| 仿真 | 状态 | 偏离数 |
|------|------|--------|
| ch3-ber-closed-form | 待跑 | — |
| ...

## 已发现问题: 0 🔴 / 0 🟡 / 0 🟢
```

### 异常处理

- 发现 🔴 致命问题（偏差 >10× 或物理上不可能的结果）→ 暂停当前 batch，先调查
- 调研 agent 发现预期与现有结论根本矛盾 → 立即写入 `_index.md` 的异常区，不继续派后续依赖 agent
- Phase 3 调查可能需要新的调研 agent → 允许动态新增

### Agent 模板

**调研 agent prompt 模板**:

```
你是仿真验证调研 agent。

## 任务
[具体调研问题]

## 必读文件
- [列出需要读的文件]

## 产出要求
将完整发现写入 [文件路径]，格式见 PROMPT-007 "调研文件格式"。
必须包含至少 2 个量化锚点（Phase 2 检查清单项）。

## 调研方法
- 优先搜索已下载的论文: papers/ 目录
- 其次 web search（学术文献）
- 辅以教材级知识（Proakis, Simon 等）
- 纯推导可以不做搜索，但必须标注"自推"

## 返回
只返回一句总结（≤50字），完整内容在文件中。
```

**仿真 agent prompt 模板**:

```
你是仿真验证执行 agent。

## 任务
运行 [仿真文件] 并验证结果。

## 预期锚点（来自 Phase 1 调研）
[从对应调研文件读取检查清单]

## 运行环境
- Python: ~/.venvs/torch/bin/python
- 工作目录: [目录]

## 产出要求
将结果写入 [文件路径]，格式见 PROMPT-007 "结果文件格式"。
逐项填写检查清单，标记 ✅/⚠️/🔴。

## 注意
- 记录实际运行参数
- 记录随机种子
- 如果仿真失败，记录完整错误信息

## 返回
只返回一句总结（≤50字），完整内容在文件中。
```

## 不要做什么

- 不修改任何仿真代码（只标注问题）
- 不修改 thesis-status.md 等文档
- 不写论文正文
- 不做新的文献检索（除调研 agent 的搜索任务）
- 发现问题时标注严重度和修复建议，但**不自行修复**
- 除非发现 🔴 致命问题且根因明确是简单笔误，此时可以在报告中注明"建议直接改为 X"

## 质量标准

**本对话成功的标准**:
1. 每个核心仿真都有理论预期文件（至少 2 个量化锚点）
2. 每个核心仿真都跑过并与预期对照
3. 所有偏离都有调查记录
4. 最终报告包含完整的缺口清单和优先级
5. **至少发现 3 个之前未记录的问题**（如果全篇找不到问题，说明检查不够仔细）
