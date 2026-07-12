# Handoff: D-W3W4 Method+Results 正文已起草，交接 D-W5F3 Conclusion+Abstract

> 来源: W002（D-W3W4 子对话活本身）| 交接目标: D-W5F3 子对话——Conclusion（W5）+ Abstract（F3）
> 文件名: H011-method-results-drafted.md
> 日期: 2026-07-12

## 到哪了（状态）

D-W3W4 完成。产出 **W002-method-results.md**（§III Method 2 段 + §IV Results 两段式 §IV-A/§IV-B 英文正文）。

- **Method 2 段**：①DA 估计器公式 1（θ̂_DA = angle(r_p·p\*)，`_recovery.py:153`）+ NDA 估计器公式 2（θ̂_NDA = (1/M₀)angle(Σr_k^M₀)，`_recovery.py:213,232-233`）+ V&V 1983 squaring loss 文字结论不推导 ②per-block SNR 公式 3（γ_blk = |h_b|²E_s/N₀）+ 切换规则文字（"select θ̂_DA when γ_blk < γ_th, else θ̂_NDA"，不编号不用伪代码）+ 创新点弱声明（"rather than introducing a new estimator or a new closed-loop component"，定位=量化归因型）
- **Results 两段式**：§IV-A 影响分析（Fig.2 BER 6 子图 + AWGN implicit baseline + crossover 17.9/16.8/10.7 dB **只呈现数据不附归因**）+ §IV-B 方法增益（切换 vs NDA +1.3~2.3 dB net + 净增益 strong +1.26/up_mod +1.19/up_str +1.85 dB naive 标脚注 + 弱湍流归零诚实标注 +0.09/0.18/0.19 + 选对率 26/29 兑现 Intro 承诺 + 切换 vs 固定 DA **不写**）
- **交叉检查 6 项 + W001 衔接全过**：术语/符号跟 R011；数字跟 R012（crossover=data / 切换 vs NDA=net / 净增益=naive 标脚注）；力度跟 R010（Method 文字非伪代码+公式直接给+弱声明 / Results BER 纵轴不硬凑 1e-5+Tab.1 增量亮点）；切换 framing 自适应选优（R008 verbatim）；crossover 只呈现数据；W001 衔接（θ/σ²_θ/net SNR gain 脚注逐字照抄 + Intro 承诺 26/29+1.85dB 兑现）
- **Results 风险防范落实**：主体对解读不敏感（BER 曲线 + HD-FEC(3.8e-3) 增益硬事实 + crossover + 选对率），3 个待导师项进标记区 HTML 注释 TBD

## 下一步干什么

D-W5F3（writing-campaign-plan.md §2 W5 + F3，一个对话合并）。**先读 R012 §V 大纲 + W001/W002 已写贡献句数字（复述要一致）+ R010 §5 力度 + writing-patterns §6.x/§8.x**。

### W5 写 Conclusion（用 R012 §V 大纲）

1 段 3-5 句（对齐 R010 §5：Johst/Le Bidan 一段式）：
1. **复述贡献**：per-block SNR 驱动的自适应估计器切换 + 26/29 选对率 + 净增益强湍流 +1.85 dB（naive）——跟 Intro 贡献句 + §III 末 + §IV-B 复述数字完全一致
2. **诚实标注局限**：弱湍流 naive 增益归零（不变量 3，+0.09/0.18/0.19 CI 重叠）
3. **Future**：更强判据 / 更多湍流场景 / 上行链路验证

**句式参照**：writing-patterns §6.2 "In this paper, we proposed ... The simulation results show ..."（OECC 2025）/ §6.4 "Future work is underway to ..."（MWP 2022）

### F3 写 Abstract（直接英文起草）

参照 Intro 贡献句（W001 §I 第 3 段）+ writing-patterns §8.x "In this paper, we propose ..."。关键数字：26/29 选对率 + 1.85 dB（naive，uplink strong）。**Abstract 是 Intro 贡献句的压缩版**——问题（DA/NDA trade-off）+ 方法（per-block SNR-driven switching）+ 结果（26/29 + 1.85 dB naive）。

## 纪律（和下一步直接相关的约束）

1. **复述数字跟 Intro/Method/Results 完全一致**——26/29（data 口径）+ 1.85 dB（naive，uplink strong，标脚注）。Conclusion/Abstract 不引入新数字
2. **术语/符号跟 R011 + W001/W002 一致**——per-block SNR-driven estimator switching / net SNR gain / DA/NDA / CPR / Γamma-Gamma block fading。不发明新词
3. **口径标注**——Conclusion/Abstract 报净增益用 naive + 脚注（跟 W001/W002 同一脚注模板）
4. **力度对齐 R010**——Conclusion 1 段 3-5 句（对齐 Johst/Le Bidan，会议论文单段式）；Abstract 是 Intro 贡献句压缩版
5. **切换 framing 统一"自适应选优"**（R008）——禁"鲁棒性补丁"
6. **弱湍流归零诚实标注**（不变量 3）——Conclusion 限字段提一句"weak-turbulence gain narrows toward zero"
7. **句式参照 writing-patterns-conference.md**——Conclusion §6.x；Abstract §8.x
8. **守 FR-22**——写作不跑新实验

## W5 要用的（Conclusion）
- **大纲论点**：R012 P3-A §V（复述贡献 + 局限 + future）
- **复述数字**（跟 Intro/Method/Results 一致）：26/29（data）+ 1.85 dB（naive，uplink strong）+ 弱湍流归零 +0.09/0.18/0.19
- **力度**：R010 §5（1 段 3-5 句，对齐 Johst/Le Bidan）
- **句式**：writing-patterns §6.2（"In this paper, we proposed ... The simulation results show ..."）/ §6.4（"Future work is underway to ..."）

## F3 要用的（Abstract）
- **参照**：Intro 贡献句（W001 §I 第 3 段）+ writing-patterns §8.x（"In this paper, we propose ..."）
- **关键数字**：26/29 选对率 + 1.85 dB（naive，uplink strong）
- **结构**：问题（DA/NDA trade-off gap）+ 方法（per-block SNR-driven switching）+ 结果（26/29 + 1.85 dB naive）
- **Abstract 不放**：公式 / 图表引用 / crossover 数字 / 弱湍流归零细节（留 Conclusion 限字段）

## 标记区清单（W002 Results 3 个 TBD，F 阶段或导师反馈后集中处理）

W4 Results 用 HTML 注释 `<!-- TBD: ... -->` 标了 3 个待导师确认项。D-W5F3 或导师反馈后集中处理：

| TBD 项 | W002 位置 | 导师反馈后动作 |
|---|---|---|
| ① 主图纵轴范围（画到 1e-3 还是尝试 1e-5）| §IV-A "plotted down to the minimum reliably estimable level" 后注释 | 导师定 A=硬凑 1e-5（需补点）/ B=画到能画到的（主体不动，删 TBD，措辞已中性）|
| ② 1e-5 底线解读（A=必须 pre-FEC / B=post-FEC 预期）| §IV-A crossover 注释关联 | 导师定 A/B 后，§IV-A 措辞微调（如 B 加 "consistent with post-FEC operation"）|
| ③ 标题/数字口径（1.85 dB naive / fair 3.10 dB / 解读 A 数字）| §IV-B 末注释 | 导师定 fair/naive（D004 已倾向 naive）/ 解读 A 数字后，标题 + §IV-B 末句 + Conclusion/Abstract 同步 |

**注**：F3 Abstract 和 W5 Conclusion 若在导师反馈前写，标题数字先用 1.85 dB naive（Intro 已锁），导师反馈后再同步标记区。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注 / 切换 framing 自适应选优 / deep fade = 斜率变缓非伪地板）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] W002 Method+Results 正文存在（读 W002 目录确认 §III + §IV-A/§IV-B 正文 + 交叉检查 6 项 + 风险防范落实说明）
  - [ ] Intro 承诺兑现（grep W002 "26 of 29" 确认 §III 末 + §IV-B 都报 + grep "1.85" 确认 §IV-B uplink strong naive）
  - [ ] Results 风险防范标记区存在（grep W002 "<!-- TBD" 确认 3 个 HTML 注释 TBD）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（W5/F3 写正文是 writing-campaign-plan 的正文写作活，在写作专题范围内，不跑实验不进 Contract）

## 下一轮

D-W5F3：Conclusion（W5）+ Abstract（F3）。一个对话可合并完成。W5 用 R012 §V 大纲（1 段 3-5 句复述贡献 + 弱湍流归零局限 + future）+ Intro/Method/Results 已写贡献句数字（复述一致）；F3 直接英文起草 Abstract（参照 Intro 贡献句 + writing-patterns §8.x）。**复述数字跟 Intro/Method/Results 完全一致**（26/29 + 1.85 dB naive）。F 阶段或导师反馈后集中处理 W002 的 3 个 TBD 标记区。规矩见 writing-campaign-plan.md §2 W5 + F3。
