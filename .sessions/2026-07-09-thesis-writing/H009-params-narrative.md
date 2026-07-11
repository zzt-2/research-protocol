# Handoff: D-P2P3 参数+叙事结构完成，交接 D-W1W2 Intro+System Model 正文

> 来源: D-P2P3 子对话（本轮即 D-P2P3 活本身）| 交接目标: D-W1W2 子对话——Intro（W1）+ System Model（W2）正文
> 文件名: H009-params-narrative.md
> 日期: 2026-07-11

## 到哪了（状态）

D-P2P3 完成。产出 **R012-params-narrative.md**（参数表 + 数字呈现方案 + 5 节大纲）。

- 口径代码行核验通过（fair_comparison.py:109）：fair = naive + 1.249，naive = fair − 1.249
- 参数表 4 类全标溯源（`_b11_params.py` 行号 + 文献）
- 数字清单 10 条标进正文/表/图 + 口径 + 来源 + 验证状态
- 5 节大纲分配 R009 逻辑链，每节标论点/数字/公式/图表占位
- 两段式落 Results §IV-A/§IV-B；切换 framing = 自适应选优（R008）
- 交叉检查 4 项全过

前置工作（P0-P3）全部完成，W1-W5 正文写作的所有零件就绪。

## 下一步干什么

D-W1W2（writing-campaign-plan.md §2 W1 + W2，一个对话合并）：

### W1 写 Intro（用 R012 §I 大纲）
1. 背景段：星地 FSO 相干 + 湍流致相位噪声 + CPR 必要（1 段，引 3-5 篇综述/标准）
2. Gap + 动机：DA/NDA trade-off 的 gap（DA 低 SNR 精度高但花 25% 带宽；NDA 省带宽但 squaring loss 低 SNR 差）
3. 贡献声明（**散文式 2-3 句不用 bullet**，R010 §1.2 实证 5/5 篇）：切换 framing 用 R008 锁定句 "selecting the locally optimal estimator in 26 of 29 operating points" + 净增益 "net SNR gain of up to 1.85 dB in strong turbulence (naive)"

### W2 写 System Model（用 R012 §II 大纲 + 参数表）
1. 信道模型：Gamma-Gamma 块衰落 + 块结构（h 块内恒定 N_blk=100，块间独立），引 Al-Habash 2001
2. 信号模型 + 帧结构：pilot spacing 每 4 符号 1 pilot = 25% overhead = 1.25 dB，引 Shieh-Djordjevic 2010
3. 相位噪声：Wiener PN，σ²_θ = 2πΔνT_s（**首次出现注 "= σ²_p in [B11]"**，θ 用 V&V 非 B11 的 φ）

## W1 要用的（Intro）
- **大纲论点**：R012 P3-A §I（背景 + gap + 贡献散文式）
- **贡献句措辞**（R008，务必 verbatim 关键短语）："selecting the locally optimal estimator in 26 of 29 operating points"
- **数字**：贡献句放 26/29 + 1.85 dB（naive）
- **力度**：R010 §1.1（1-2 段 ~8-15 行）+ §1.2（散文式）+ §1.3（gap 1-2 句）
- **切换 framing = 自适应选优**（R008，禁"鲁棒性补丁"）
- **句式参照**：writing-patterns-conference.md（"In this paper, we..."）

## W2 要用的（System Model）
- **大纲论点**：R012 P3-A §II（GG 模型 + 块结构 + 帧结构 + PN）
- **参数表**：R012 P2-A（M₀=8 / α,β / Δν=10kHz / σ²_θ=2.51e-5 / N_blk=100 / N_DFT=256 / pilot spacing=4 / overhead 1.25dB）。正文给关键值，不全列（如需参数表考虑放 Tab 或 footnote）
- **公式分配**：GG 模型 + pilot overhead 用**文字 + 数字**（不编号公式）；σ²_θ = 2πΔνT_s 参数定义级一句话。DA/NDA/per-block SNR 三公式不进 §II（进 §III Method）
- **θ 符号决定**：用 θ/θ̂（R011 从 V&V/sat.1553），首次出现注 B11 对应（σ²_θ = σ²_p in [B11]）
- **力度**：R010 §2.1（给 GG 模型名 + 块结构不给完整 PDF）+ §2.2（帧结构文字 + 1.25dB 数字）

## 纪律（和下一步直接相关的约束）

1. **术语/符号跟 R011 三表一致**（零容忍偏差）——W1/W2 直接照抄 R011 术语表 + 符号表
2. **数字跟 R012 一致**（口径/来源）——报增益前确认 naive 口径，口径标注用脚注模板
3. **力度对齐 R010**（不多不少）——Intro 1-2 段 / SM 给 GG+块结构不给 PDF
4. **不自造词、不深挖没把握的物理归因**（R009）——crossover 只在 Results 呈现数据，Intro 不碰
5. **切换 framing 统一"自适应选优"**（R008）——Intro 贡献句 + Method 描述都用，禁"鲁棒性补丁"
6. **句式参照** writing-patterns-conference.md
7. **守 FR-22**——写作准备不跑新实验

## 关键数字速查（W1/W2 要用的，全已代码行核验）

| 数字 | 值 | 口径 | 用在哪 |
|---|---|---|---|
| 选对率 | 26/29（90%）| data | Intro 贡献句 |
| 净增益（强湍流）| +1.26 dB（strong）/ +1.85 dB（up_str）| naive | Intro 贡献句 + Tab.1 |
| pilot overhead | 1.25 dB（=10log10(4/3)）| 定义值 | SM §II |
| M₀ | 8 | 定义值 | SM §II / Method |
| crossover | weak 17.9 / mod 16.8 / strong 10.7 dB | data | Results（只呈现数据）|
| 切换 vs 固定 NDA | +1.3~2.3 dB | net | Results §IV-B |

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注 / 切换 framing 自适应选优）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] R012 参数表 + 数字方案 + 5 节大纲存在（读 R012 目录确认）
  - [ ] 口径 fair=naive+1.249（读 fair_comparison.py:109 + JSON strong fair=2.509→naive=1.260 确认）
  - [ ] 选对率 26/29（读 switch_caliber_audit.py 输出确认）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（不跑实验/不进 Contract/不写正式论文章节——注：W1/W2 写正文是 writing-campaign-plan 的正文写作活，在写作专题范围内）

## 下一轮

D-W1W2：Intro（W1）+ System Model（W2）正文。一个对话可合并完成。W1 用 R012 §I 大纲 + R008 贡献句；W2 用 R012 §II 大纲 + 参数表 + R011 θ 符号决定。规矩见 writing-campaign-plan.md §2 W1 + W2。
