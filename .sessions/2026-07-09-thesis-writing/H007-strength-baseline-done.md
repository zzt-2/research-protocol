# Handoff: D-P0 力度基准表建成，交接 D-P1 用语+符号+公式三合一

> 来源: 主控 D-P0 子对话（无 S###，本轮即 D-P0 活本身）| 交接目标: D-P1 子对话——用语+符号+公式三合一
> 文件名: H007-strength-baseline-done.md
> 日期: 2026-07-11

## 已完成边界

D-P0 力度第一轮摸底完成。产出 **R010-strength-baseline-table.md**（20 条基准，5 节 × 3-5 技术点）。

- 3 子 agent 并发提取 A 组 5 篇 content.md 力度信息（Johst/Le Bidan 各一重点 + Panasiewicz+OECC-PSC+Paillier 合并）
- 每条基准标来源论文（哪篇哪节），不凭印象
- 「我方应到的力度」建议有依据（对齐 X 论文 Y 节因为 Z）
- 守 FR-22（只读已有 content.md，不下载新论文不跑实验）+ 质量红线 4 条

## 不要做什么

- **不要重新读 5 篇全文**——R010 已提取力度，P1 只在需要验证某术语/符号写法时查对应 content.md 的特定段
- **不要推导公式**——R010 已定粒度=直接给结论级（对齐 Panasiewicz），squaring loss 引 V&V 1983 即可（R009 原则）。OECC-PSC/Paillier 的完整推导是少数派，不学
- **不要自造词**（不变量 6 黑话禁令）——每个术语在对标集查过或引文献
- **不要用 bullet 写贡献**（5/5 篇散文式，反惯例）
- **不要硬凑 1e-5 纵轴**（R004/H002 结论 + R010 §4.1 对齐 Paillier）
- **不要用伪代码**（5/5 篇无伪代码，用文字+框图）

## 必读（按优先级）

1. **R010-strength-baseline-table.md**——本活核心标尺，P1 重点查 §2.3（估计器表述粒度）+ 公式专项（2-3 个核心公式）+ §1.2（贡献散文式）
2. **R009-logic-chain-final.md**——论文讲什么（DA/NDA trade-off + 数据印证 + 切换机制），定符号要对应逻辑链
3. **writing-campaign-plan.md §2 P1**——P1 活的规矩（术语表/符号表/公式清单格式 + 完成判据）
4. **benchmark-paper-set.md A 组**——术语/符号查证来源（重点 Johst DA vs blind 术语 + B11 NDA-ML 术语 + OECC-PSC pilot 频谱代价术语）

## D-P1 要重点参照的 R010 基准行

| R010 基准行 | P1 怎么用 |
|---|---|
| §2.3 估计器数学表述粒度 | **DA/NDA 公式直接给结论级**（对齐 Panasiewicz）。DA: `θ̂=angle(r_pilot·p*)`；NDA: `θ̂=(1/M₀)angle(Σr^M₀)`。各 1 行+一句话解释 |
| 公式专项 | **2-3 个核心公式**：DA 估计器 + NDA 估计器 + per-block SNR 判据。系统模型参数进参数表(P2)不进正文公式 |
| §1.2 贡献声明写法 | **散文式 2-3 句不用 bullet**（5/5 篇实证） |
| §2.1 信道模型深度 | **给 Gamma-Gamma 块衰落公式 + 块结构**（我方核心场景 + benchmark 缺口 2 填补） |
| §2.2 帧结构描述 | **pilot overhead 1.25dB=10log10(4/3)** 必须给出，引 Shieh-Djordjevic 2010 |

## Johst/Le Bidan 术语+公式力度要点（P1 重点对照）

**Johst（DA vs blind 对比力度标尺）**：
- 术语：blind CMA / data-aided / pilot-aided CPE（§II）
- 公式：仅定义级（PDL_dB、闪烁指数 σ_I²、FEC 阈值），**零推导**
- DA vs blind 对比是**文字段落**（§II 开头），非专列对比节

**Le Bidan（CCISP 体例标尺，872 行最完整）**：
- 术语：CMA blind equalization / pilot-aided / data-aided carrier phase（§IV 模块逐段）
- 公式：~25 个但**仅 1 个完整推导**（CMA 代价函数 eq(1) §IV.D），其余全参数赋值/符号定义
- pilot 开销讨论有**专节**（§III.B L319-352），给 η=3.6% 公式 + 与 400ZR 对比
- 方法节最厚(~340 行 §IV)，结果轻——体例是"方法重、结果轻"

## 接口变更

无代码改动。纯文档产出（R010 + topic-index 更新 + 本 handoff）。

## 接收方验证（D-P1 续接时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令/crossover 只呈现数据/A4 数据诚实标注）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] R010 存在且 20 条基准（读 R010 目录确认）
  - [ ] 5 篇 content.md 行数 268/872/148/150/258（已主线核验，FR-26 PASS）
  - [ ] 公式粒度=直接给结论级依据（R010 §2.3 + 公式专项，对齐 Panasiewicz §II-B）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（不跑实验/不进 Contract/不写正式论文章节）

## 下一轮

D-P1 用语+符号+公式三合一：
1. **术语表**（markdown 表：英文词/中文释义/用法例句/来源论文/是否标准）。覆盖论文全部用词（预估 30-50 词）。自造词（fair_gain 等）全标替换。重点对照 Johst（DA vs blind 术语）+ OECC-PSC（pilot 频谱代价术语）+ B11（NDA-ML 术语）
2. **符号表**（markdown 表：符号/含义/对齐惯例/首次出现节）。全篇统一无冲突
3. **公式清单**（2-3 个：公式/物理含义/来源代码行或文献/呈现粒度）。粒度对齐 R010 §2.3=直接给结论级

完成判据见 writing-campaign-plan.md §2 P1。
