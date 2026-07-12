# Handoff: D-W5F3 Conclusion+Abstract 正文已起草（正文全部定稿），交接 D-F1F2 力度第二轮+图表

> 来源: W003（D-W5F3 子对话活本身）| 交接目标: D-F1F2 子对话——F1 力度第二轮 + F2 图表
> 文件名: H012-conclusion-abstract-drafted.md
> 日期: 2026-07-12

## 到哪了（状态）

D-W5F3 完成。**正文全部定稿（5 节 + Abstract 全齐）**。产出 **W003-conclusion-abstract.md**（§V Conclusion + Abstract 英文正文）。

- **Conclusion 1 段 3 句**（对齐 R010 §5 Johst/Le Bidan 一段式）：①复述贡献 "In this paper, we proposed a per-block SNR-driven estimator switching scheme ... selects the locally optimal estimator in 26 of 29 operating points, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"（句式 §6.2 OECC 2025）+ ②弱湍流归零诚实标注 "the gain narrows toward zero (+0.09/+0.18/+0.19 dB, within the 30-seed confidence interval)"（不变量 3）+ ③future "Future work is underway to strengthen the switching criterion, to extend ... to additional turbulence regimes, and to validate ... on uplink experimental data"（句式 §6.4 MWP 2022）
- **Abstract 1 段 4 句**（Intro 贡献句压缩版）：①问题 DA/NDA trade-off（DA 低 SNR 准 + 1.25dB overhead / NDA 省带宽 + squaring loss 低 SNR 差）②方法 "per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and an NDA carrier phase estimator"（句式 §8.x）③结果 "selects the locally optimal estimator in 26 of 29 operating points, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"。Abstract 不放公式/图表/crossover/弱湍流细节（留 Conclusion）
- **交叉检查 5 项全过**：复述数字五处正文 grep 确认一致（Intro/Method/Results/Conclusion/Abstract 同一写法 "26 of 29 operating points" + "up to 1.85 dB in strong turbulence (naive, net of pilot overhead)" + 同一脚注模板逐字照抄）；术语/口径/力度/framing 全对齐

## 全篇正文清单（D-W5F3 后正文全齐）

| 节 | 文件 | 内容 |
|---|---|---|
| Abstract | W003-conclusion-abstract.md | 1 段 4 句（问题+方法+结果）|
| §I Introduction | W001-intro-system-model.md | 3 段（背景+gap+贡献散文式）|
| §II System Model | W001-intro-system-model.md | 2 段（GG 块衰落+信号/帧/PN）|
| §III Method | W002-method-results.md | 2 段（DA/NDA/per-block SNR 三公式+切换规则+创新点弱声明）|
| §IV Results | W002-method-results.md | 两段式 §IV-A 影响分析 + §IV-B 方法增益 |
| §V Conclusion | W003-conclusion-abstract.md | 1 段 3 句（复述+局限+future）|

## 下一步干什么

D-F1F2（writing-campaign-plan.md §2 F1 + F2，一个对话合并）。**先读 R010 力度基准表 + 全篇正文（W001/W002/W003）+ S006 四张样图**。

### F1 力度第二轮（逐点对照 R010 力度基准表，讲多了还是少了）

R010 力度基准表 20 条基准（5 节 × 3-5 技术点），逐条对照全篇正文检查：
- Intro §1.1（背景 1-2 段 ~8-15 行）/ §1.2（贡献散文式）/ §1.3（gap 1-2 句）
- SM §2.1（GG 模型名+块结构不给 PDF）/ §2.2（帧结构文字+1.25dB）/ §2.3（估计器公式直接给）
- Method §3.1（文字+框图非伪代码）/ §3.2（创新点弱声明）
- Results §4.1（BER 主图纵轴不硬凑 1e-5）/ §4.2（正文 dB + Tab.1 增量亮点）/ §4.3（对比融 Results 不专列）
- Conclusion §5（1 段 3-5 句）+ 公式专项 + 图表专项

### F2 图表（S006 四张样图 + R010 图表力度专项）

每图定"表达什么论点"+ 对齐 R010 图表力度专项：
- **Fig.1 系统框图**（S006 已有 SVG，§II 占位 "as depicted in Fig. 1"）
- **Fig.2 BER 主图**（S006 已有 3×2 纵向 6 子图，§IV-A 占位——纵轴 TBD 待导师）
- **Fig.3 净增益方案**（S006 已有，§IV-B 占位）
- **Fig.4 crossover**（S006 已有 data 口径多场景，§IV-A 占位）
- **Tab.1 增益汇总**（只强湍流 3 行 naive：strong +1.26 / up_mod +1.19 / up_str +1.85，§IV-B 占位）

## 已知 F1 待查项（主控预判，交接时给 F1 逐条处理）

| # | 待查项 | 位置 | 处理建议 |
|---|---|---|---|
| ① | Intro [APCCAS 2022] 引用偏弱 | W001 §I 第 1 段 "CPR is therefore an essential block ... [APCCAS 2022]" | 句式参照 writing-patterns §5.7 来自 APCCAS 2022，但该引用是 FPGA BPS 实现论文跟星地 FSO 相关度中。考虑换更对口的（如 sat.1553 CPR 段）或删引用保留句式 |
| ② | "single-estimator baseline" 不在术语表 | W002 §IV-B 末 "recovering the gain the single-estimator baseline forgoes" | R011 术语表无 "single-estimator baseline"。考虑换 "fixed-estimator baseline" 或 "either estimator used alone"（描述性，非新术语）|
| ③ | 26/29 在 Method+Results 各出现一次 | W002 §III 末 + §IV-B 末 | Intro+Conclusion+Abstract 各一次是必要的（贡献声明/复述）。Method+Results 重复可考虑精简一处（如 §III 末去掉，留 §IV-B 数据出处）|
| ④ | 3 个 TBD 标记区 | W002 §IV-A 纵轴范围(D003) / §IV-A 1e-5 解读措辞 / §IV-B 标题数字口径(D004) | 导师反馈后处理。F1/F2 阶段不碰（保持中性措辞 + 1.85 dB naive 锁定）|

## 纪律（和下一步直接相关的约束）

1. **F1 力度对照不引入新内容**——只检查"讲多了还是少了"，不重新调研、不改贡献/数字/口径
2. **F2 图表论点优先**——每图先想"表达什么论点"再核对数据（S006 已有样图，R010 图表力度专项）
3. **TBD 标记区不碰**（导师反馈后处理）——F1/F2 保持 W002 的中性措辞 + 1.85 dB naive 锁定
4. **术语/符号跟 R011 + W001/W002/W003 一致**——F1 修正时照抄术语表，不发明新词
5. **复述数字跟五处正文一致**——F1 修正时不动 26/29 + 1.85 dB naive 的写法（已 grep 确认一致）
6. **切换 framing 统一"自适应选优"**（R008）——F1 修正时禁"鲁棒性补丁"
7. **守 FR-22**——F1/F2 不跑新实验

## F1 要用的（力度第二轮）
- **力度基准**：R010-strength-baseline-table.md（20 条基准，5 节 × 3-5 技术点）
- **全篇正文路径**：W001（§I/§II）+ W002（§III/§IV）+ W003（§V/Abstract）
- **已知待查项**：见上表 4 条

## F2 要用的（图表）
- **S006 四张样图**：Fig.1 系统框图 SVG / Fig.2 BER 主图 3×2 纵向 6 子图 / Fig.3 净增益方案 / Fig.4 crossover v3
- **R010 图表力度专项**：4-6 图 + 1 表（Tab.1 增量亮点，4/5 篇 0 表）
- **每图论点**：Fig.1 系统架构 / Fig.2 DA/NDA 各自 BER 分场景（影响分析载体）/ Fig.3 净增益量化归因 / Fig.4 crossover 跨场景自动选优（data 口径）/ Tab.1 强湍流 3 行 naive 增益汇总
- **数据出处**：`projects/simulation/results/sc_nda_ml_main_30seed/`（BER 数据 + fair_gain JSON）+ S006 图表美化 checklist

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注 / 切换 framing 自适应选优 / deep fade = 斜率变缓非伪地板）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] W003 Conclusion+Abstract 正文存在（读 W003 目录确认 §V + Abstract 正文 + 交叉检查 5 项）
  - [ ] 复述数字五处一致（grep W001/W002/W003 "26 of 29 operating points" + "1.85 dB" 确认同一写法）
  - [ ] 正文全部定稿（W001 §I/§II + W002 §III/§IV + W003 §V/Abstract 全齐——读三个文件目录确认）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（F1/F2 力度对照+图表是 writing-campaign-plan §2 收尾活，在写作专题范围内，不跑实验不进 Contract）

## 下一轮

D-F1F2：力度第二轮（F1）+ 图表（F2）。一个对话可合并完成。F1 用 R010 力度基准表 20 条逐点对照全篇正文（讲多了还是少了）；F2 用 S006 四张样图 + R010 图表力度专项定每图论点。**已知 F1 待查项 4 条**（Intro [APCCAS 2022] 引用 / "single-estimator baseline" 不在术语表 / 26/29 重复 / 3 个 TBD 标记区）。**TBD 标记区导师反馈后处理**，F1/F2 保持中性措辞 + 1.85 dB naive 锁定。规矩见 writing-campaign-plan.md §2 F1 + F2。
