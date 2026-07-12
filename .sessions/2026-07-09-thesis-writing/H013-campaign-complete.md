# Handoff: D-F1F2 力度第二轮+图表定稿完成——写作战役全部完成

> 来源: F001（D-F1F2 子对话活本身）| 交接目标: 等导师反馈 + 全篇通读 + 转 LaTeX 投稿（**非 writing-campaign 范围，战役已收尾**）
> 文件名: H013-campaign-complete.md
> 日期: 2026-07-12

## 到哪了（状态）

D-F1F2 完成。**写作战役（writing-campaign-plan §2）全部完成**。产出 **F001-strength-check-figures.md**（F1 力度对照 + F2 图表规格）。

- **F1 力度第二轮**：R010 20 条基准逐条对照全篇正文**全部对齐**（无硬性多了/少了偏差）。8 条已知待查项处理——**7 项触发正文修正**（①②③⑤⑥⑦⑧），④（3 个 TBD）不碰导师反馈后处理。修正已用 Edit 落地 W001/W002/W003。
- **F2 图表定稿**：5 项规格定稿（Fig.1-4 + Tab.1），论点/画法/数据/R010 对齐全清。图数 4 + 表 1 对齐 R010 图表专项。F2 不实际画图（S006 已有样图）。
- **交叉检查 5 项全过**：修正后术语/数字/framing 一致，TBD 不动。

## 全篇正文清单（战役产出，F1 修正后定稿）

| 节 | 文件 | F1 修正 |
|---|---|---|
| Abstract | W003-conclusion-abstract.md | ⑤d+⑦（开头加压力 + locally optimal→lower BER）|
| §I Introduction | W001-intro-system-model.md | ①+⑤a（删 APCCAS 弱引用 + locally optimal→lower BER）|
| §II System Model | W001-intro-system-model.md | — |
| §III Method | W002-method-results.md | ③+⑧（§III 末 26/29 精简 + enjoys/known noiselessly 中性化）|
| §IV Results（§IV-A/§IV-B）| W002-method-results.md | ②+⑤b（single-estimator→either used alone + locally optimal→lower-BER）|
| §V Conclusion | W003-conclusion-abstract.md | ⑤c+⑥（换角度避免逐字重复 Intro + locally optimal→lower BER）|
| F1 力度对照 + F2 图表规格 | F001-strength-check-figures.md | （本文件）|

## 关键状态（战役完成后的锁定项）

### 数字一致（F1 修正后）
- **26 of 29 operating points**：Intro/§IV-B/Conclusion/Abstract 四处（③ 删 §III 末一处，剩四处，数字值/口径 data 不动）
- **1.85 dB naive**：Intro/§IV-B/Conclusion/Abstract 四处，口径 naive 标脚注（跟 W001/W002 同一脚注模板）
- **弱湍流归零**（+0.09/0.18/0.19 CI 重叠）：§IV-B + Conclusion，诚实标注（不变量 3）

### 切换 framing 仍统一"自适应选优"（R008，F1 修正后）
- ⑤"locally optimal estimator"→"estimator with the lower bit error rate" / "lower-BER estimator" 是 **hedging**（3 个点没选对就不能说全点最优，逻辑严谨化），**非推翻 R008**——切换仍是"per-block SNR 驱动的自适应选优"，语义不变（选 BER 低的 = 选局部更优的）
- 全篇无"鲁棒性补丁"/"necessary closed-loop component"/"crossover 物理归因"残留

### 3 个 TBD 标记区（导师反馈后处理，F1/F2 未碰）

| TBD 项 | W002 位置 | 导师反馈后动作 |
|---|---|---|
| ① 主图纵轴范围（画到 1e-3 还是尝试 1e-5）| §IV-A "plotted down to the minimum reliably estimable level" 后 HTML 注释 | 导师定 A=硬凑 1e-5（需补点）/ B=画到能画到的（主体不动，删 TBD，措辞已中性）|
| ② 1e-5 底线解读（A=必须 pre-FEC / B=post-FEC 预期）| §IV-A crossover 注释关联 | 导师定 A/B 后，§IV-A 措辞微调 |
| ③ 标题/数字口径（1.85 dB naive / fair 3.10 dB / 解读 A 数字）| §IV-B 末 HTML 注释 | 导师定 fair/naive（D004 已倾向 naive）/ 解读 A 数字后，标题 + §IV-B 末句 + Conclusion/Abstract 同步 |

**注**：⑤ hedging 后，TBD ③ 标题数字仍锁 1.85 dB naive（Intro/Conclusion/Abstract 一致），导师反馈后再同步。

## 下一步干什么（**非 writing-campaign 范围，战役已收尾**）

写作战役全部完成。下一步是**投稿准备**，不在 writing-campaign-plan §2 范围内：

### 1. 等导师 3 项反馈（卡 Results §IV TBD 标记区）
- ① **10⁻⁵ 底线 A/B**（D003）→ 决定主图纵轴范围 + 主卖点成立性（R004 倾向解读 B=post-FEC）
- ② **口径 fair/naive**（D004 已倾向 naive）→ 决定标题数字（当前锁 1.85 dB naive）
- ③ **主对比文献**（简报§3）→ 决定参考文献核心一条

### 2. 全篇通读（F1 修正后整体读一遍）
- 检查 Intro→SM→Method→Results→Conclusion 衔接顺畅
- 检查 Abstract 跟正文贡献一致
- 检查 F1 修正后无新引入的不一致

### 3. 转 LaTeX 投稿格式（CCISP 双栏）
- **段落调整**：双栏排版下段落断行可能需微调（特别是 §IV Results 长段落）
- **图表插入**：按 F001 F2 规格画图/插表（S006 已有样图，按规格定稿）
- **参考文献**：10-15 篇（R010 §参考文献 + R011 术语来源 + R009 逻辑链引用）。当前正文用占位引用名（[B11]/[sat.1553]/[Al-Habash 2001]/[V&V 1983]/[Shieh-Djordjevic 2010]/[Paillier]/[Johst]），转 LaTeX 时换正式 citekey
- **公式编号**：§III 三公式已编号 (1)(2)(3)，双栏下检查公式不溢出

## 纪律（投稿准备阶段的约束）

1. **TBD 标记区导师反馈后才动**——投稿前不碰纵轴范围/1e-5 解读/标题数字口径
2. **F1 修正不可逆但旧文本有记录**——每项修正旧文本在 F001 F1-B 各条记录里，如导师/审稿人质疑 hedging 可回退
3. **⑤ hedging 是 R008 精化非推翻**——如导师/审稿人质疑"lower BER"措辞，回查 R008/S007 data 口径选对率 26/29 原始讨论
4. **数字口径代码行核验过**（D004）——naive = fair − 1.249（fair_comparison.py:109），投稿前如再质疑可重验
5. **守 FR-22**——投稿准备不跑新实验（等导师反馈的 3 项是解读/口径选择，非新数据）

## 全篇正文路径（投稿准备时读这五个文件）

1. `.sessions/2026-07-09-thesis-writing/W001-intro-system-model.md`（§I + §II）
2. `.sessions/2026-07-09-thesis-writing/W002-method-results.md`（§III + §IV）
3. `.sessions/2026-07-09-thesis-writing/W003-conclusion-abstract.md`（§V + Abstract）
4. `.sessions/2026-07-09-thesis-writing/F001-strength-check-figures.md`（F1 修正记录 + F2 图表规格）
5. `.sessions/2026-07-09-thesis-writing/R011-terminology-symbol-formula.md`（术语/符号/公式三表，转 LaTeX 时照抄）
6. `.sessions/2026-07-09-thesis-writing/R012-params-narrative.md`（参数表 + 数字清单 + 5 节大纲，投稿时数字溯源）

---
## 接收方验证（续接投稿准备对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注 / 切换 framing 自适应选优 / deep fade = 斜率变缓非伪地板）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] F001 力度对照+图表定稿存在（读 F001 确认 F1 20 条对照 + 8 待查项 + F2 五项图表规格）
  - [ ] F1 7 项修正已落地（grep W001/W002/W003 正文确认 "locally optimal estimator" 在 body 已清/"single-estimator" 已清/APCCAS 引用已删/enjoys 已改）
  - [ ] 写作战役全部完成（W001+W002+W003+F001 全齐——读四个文件确认）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认 TBD 标记区清单（3 个，导师反馈后处理）

## 下一轮

**写作战役全部完成，无 writing-campaign 下一轮**。

下一步是投稿准备（等导师反馈 + 全篇通读 + 转 LaTeX），不在 writing-campaign-plan §2 范围内。如需开投稿准备新专题，建议 slug = `2026-07-12-ccisp-submission-prep`，查 `.sessions/_registry.yaml` 重确认无冲突后开。
