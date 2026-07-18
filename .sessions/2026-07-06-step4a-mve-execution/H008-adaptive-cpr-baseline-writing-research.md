# Handoff: 自适应 CPR 论文的 baseline 组织 + 参数处理 + 叙述展开调研

> 来源: S013 续接 | 交接目标: 新对话调研"自适应/混合载波恢复论文怎么组织 baseline、参数、叙述"
> 文件名: H008-adaptive-cpr-baseline-writing-research.md
> 日期: 2026-07-09

## 到哪了（状态）

4 种适配扫描（A1/A2/A3/A4）全闭合。**A4 条件适配 PASS**——唯一出信号的方向：

- **物理发现**：星地 FSO 湍流下 pilot-aided(DA) 和 blind(NDA) 载波相位恢复存在 crossover——低 per-block 有效 SNR DA 赢（pilot 可靠），高有效 SNR NDA 赢（积分鲁棒 + 省导频开销）。crossover 由 per-block 有效 SNR γ_eff = γ_bar + 10log10(h) 驱动，汇聚在 γ_eff 12~14dB（诊断实证，不是单纯 fade 深度）。
- **方法**：per-block 有效 SNR 驱动的 DA/NDA 硬切换（两层判据：块内 CV 门控判有无衰落 + γ_eff 门控判 DA/NDA，全接收端可测非 oracle）。
- **数据**（30 seed，简报主引）：
  - fair_gain 随湍流递增：AWGN +1.34 → weak +1.43 → moderate +1.44 → strong +2.51 → uplink_mod +2.44 → uplink_strong +3.10 dB
  - A4 切换 crossover 区（γd=15dB）赢 max(DA,NDA)：weak +0.27 [+0.19,+0.36] / moderate +0.48 [+0.41,+0.55] / strong +0.40 [+0.36,+0.45]，CI 下界全正
- **文献**：两轮独立检索（16 组查询 ~130 篇）确认单载波 CPR 的 per-block pilot/blind 硬切换**没人做过**。最接近的是静态比较（Song 2020，不切换无湍流）、级联组合（Moretti 2013 TWC，两个同时跑付双倍复杂度）、算法内自适应参数（不跨算法切换）。FSO 自适应只切调制/功率/链路，从未把载波恢复算法当切换对象。
- **简报写完**：`projects/simulation/ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md`，未发给老师。

## 下一步干什么（新对话的核心任务）

**用户明确想搞清楚的 4 个问题**（调研"自适应论文一般怎么弄"）：

1. **别人这种自适应论文怎么组织 baseline？** 切换/自适应策略的 baseline 结构（固定策略 vs 别的方法），尤其自适应 CPR 或自适应传输类论文的惯例。
2. **别人怎么展开叙述？** 给出什么参数、什么数据、图怎么画、故事线怎么组织。
3. **【用户最关心】别人是使用和参考文献同样的参数，还是自己改但使用和参考文献同样的算法？** 即：baseline 是照搬别人论文的参数复现，还是自己重新调参？
4. **别人会不会先把 baseline 按原文献参数复现，之后再改成自己的参数？** 即复现流程：先按原文参数验证实现正确，再迁移到自己场景。

这是**论文写作前的范式调研**——搞清楚同领域论文的惯例，才能决定我们的简报/论文怎么组织 baseline 段落、参数表、复现流程的叙述。

## 纪律（和下一步直接相关的约束）

1. **baseline 合规守 D-010 五条**（老师 2026-07-08 电话定的，详见 `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-010）：
   - 同场景（星地湍流）② 同类型层级（载波同步层）③ 不找接近方法当 baseline（VV 同族禁主比，D-009 已证持平）④ 近年+权威（2022+ Trans）⑤ 找方向/复现只看够好的
2. **通信领域 baseline 是自实现的**（H007 认知修正，topic-index "其他结论"段）：在自己参数下跑经典方法，不要求别人论文用一样参数。引用文献只证明"方法在该层合法、有人用过"。
3. **A4 切换的 baseline 结构**：主 baseline = 自实现固定 DA/NDA（对照"有没有切换策略"）；VV/BPS 同族只当 fellow（D-009）；DPLL 异族参照；oracle 上界。用户想在调研里验证这个结构是否符合领域惯例。
4. **不跳框架（FR-22）**：当前在 GW Step 4a 维度 D（A4 PASS，待 Go 决策）。baseline 组织调研是写作准备，不是跑新实验。
5. **诚实标注**：30 seed 下 weak/moderate fair_gain CI 重叠（[1.35,1.51] vs [1.28,1.60]，统计不可分），叙事是"弱湍流 ~1.4dB → 强湍流显著跳到 ~2.5dB"两段，不是六档严格单调。

## 必读（新对话开始时按优先级读）

1. `.sessions/2026-07-06-step4a-mve-execution/topic-index.md` — 不变量 + 当前位置（§"当前位置" S013 A4 PASS）
2. `projects/simulation/ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md` — 刚写的简报（新对话要帮完善它的 baseline/参数叙述段）
3. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-010 — baseline 选取 5 条标准；D-009 — VV 同族持平（为什么 VV 不当主 baseline）
4. `.sessions/2026-07-06-step4a-mve-execution/S013-adaptation-scan-experiments-log.md` — A4 完整实验日志（物理因果诊断 + 30seed 数据 + 文献结论）
5. `search-archive/2026-07-09/` — 已有文献检索存档（16 组查询 ~130 篇，新对话可复用 + 补充 baseline 组织角度的查询）

## 接口变更（如有代码改动）

无代码改动。本轮全是实验脚本（explore/，不进 common/）+ 简报 .md。

## 失败数据附录（A4 的诚实局限）

| 点 | 问题 | 是否影响简报 |
|----|------|-------------|
| A4 AWGN@5~10dB（BER>0.07 不可工作区）| 切换输 max(DA,NDA) 0.02~0.40dB，CV 门控低 SNR 噪声大误判 | 不影响（不可工作区）|
| A4 weak@5/10（BER 0.17~0.40 不可工作区）| 同上 | 不影响 |
| weak/moderate fair_gain CI 重叠 | 30seed 下 [1.35,1.51] vs [1.28,1.60]，统计不可分 | 简报已诚实标注"两段趋势"非严格单调 |
| NDA vs VV/BPS/DPLL 持平 | D-009，算法层纯增量薄（~0.1-0.5dB）| 简报靠 fair_gain 架构红利 + A4 切换双叙事撑 |

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| γ_eff 阈值 13dB 只在当前信道参数标定 | 阈值应跨参数鲁棒 | 敏感性扫描 11/13/15 显示鲁棒，但未跨线宽/调制阶数验证 | 进 Contract 前补 |
| A4 切换 30seed 只跑了基准配置 | 敏感性扫描应 30seed | 基准配置 30seed ✓，其他 4 配置仍 3seed | 写论文前补 |
| 简报图还是 5seed 数据 | 数据已 30seed | `_adaptation_scan_figures.png` 用 5seed | 发简报前重画 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（尤其 D-005 务实路线 + FR-22 GW 门控）
- [ ] 已验证本文件中的至少 3 条关键事实声称（建议验证：30seed fair_gain 数字 / A4 crossover CI / 文献结论"没人做过"）
  - 验证指针：`results/sc_nda_ml_main_30seed/_fair_gain_summary_30seed.json` / `explore/nda-awgn-tracking-sandbox/_a4_switch_30seed.json` / `search-archive/2026-07-09/`
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（baseline 组织调研是写作准备，不跑新实验，不跳框架）

## 下一轮

**任务**：调研"自适应/混合载波恢复论文（及相邻自适应传输论文）怎么组织 baseline、处理参数、展开叙述"，回答用户 4 个问题，然后完善简报的 baseline 段 + 参数叙述。

**具体步骤**：

1. **文献调研（子 agent，复用 search-archive/2026-07-09/ + 补充）**：
   - 找 2-3 篇近年（2022+）自适应/混合 CPR 或自适应传输论文，精读它们的 baseline 段落 + 参数表 + 复现说明
   - 重点看：baseline 参数照搬还是自调？有没有"先按原文献复现再迁移"的流程叙述？
   - 候选切入点：Moretti 2013 TWC（combined pilot-DD）、Song 2020（pilot vs blind 比较）、近年 FSO 自适应传输论文、光纤自适应 CPR（BPS 窗长自适应）

2. **回答用户 4 个问题**，每个附文献证据（不是猜）：
   - baseline 怎么组织（固定策略？别的方法？怎么选）
   - 叙述怎么展开（参数表给什么、图画什么、故事线）
   - **【最关心】参数照搬原文 vs 自调同算法**——领域惯例是哪个
   - **【最关心】先按原文复现再迁移**——有没有这个流程，怎么叙述

3. **完善简报**：根据调研结果，把 `ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md` 的 baseline 段（§6）+ 参数叙述调整到符合领域惯例

4. **可选**：30seed 图重画（如要发简报）

**工具调用**：
- 文献检索：`bash tools/search "query"` 或 `bash tools/blit --source ieee "query"`
- 精读大文本：子 agent 内执行，返回 ≤500 词摘要
- 主对话严禁 WebSearch / webReader（守 AGENTS.md 上下文管理规则）
