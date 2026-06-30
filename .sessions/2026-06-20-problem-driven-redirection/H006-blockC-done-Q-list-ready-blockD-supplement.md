# Handoff: 块 C 综合分析完成（literature_notes.md 重写 + Q# 清单 Q1-Q10 浮出）→ 块 D Step 3.5 就绪

> 来源: S015 | 交接目标: 块 D Step 3.5 定向补检索（用 Q# 新认知弥补盲区）
> 文件名: H006-blockC-done-Q-list-ready-blockD-supplement.md
> 日期: 2026-06-26

## 到哪了（状态）

**GW Step 3 综合分析全部完成，literature_notes.md 完整重写，研究问题清单 Q1-Q10 浮出，master-state GW Progress 表 Step 2/3 ⬜→✅（FR-22 门控释放）**。

具体 5 件事（全在 D005 务实路线 + H005 下一轮范围内）：

1. **H005 handoff 接收**（Trigger 5）：3 条事实核查全 PASS（6 篇笔记落盘 / read-log 13 条 / blit 3 篇 md）。
2. **框架文件强制重读**（AGENTS.md [MUST]）：本轮 Read 调用 gw-read.md（综合分析节+质量门槛）/ glossary.md（四判据+候选全筛掉时）/ TL-30/31/32/33 / templates.md literature_notes 模板。**证据 = 本轮 Read 工具调用记录**（非凭记忆，FR-26/TL-33）。
3. **派 3 Explore agent 并行核查 10 篇精读笔记**（子 agent 强制委托）：提取问题提取子表/baseline 对称性/增益归因/局限。**Agent 2 诚实纠正**：新2（ACCESS.2023.3287501）不是 PS 方向，是 DSP 全电子 DS 补偿（笔记全文无 PS），纠正了 H005 候选池表的措辞偏移。
4. **按 gw-read.md 综合分析 5 节撰写** → 写入 literature_notes.md：方法分类（5 类）/ 已知局限（6 条）/ 2-3年趋势（5 条）/ 研究背景概述 / **研究问题清单 Q#**。
5. **master-state GW Progress 表 Step 2 acquire ✅ + Step 3 read ✅**（含 Q# 清单非空）+ 活跃文件行更新。

## Q# 清单当前状态（块 C 核心产物）

| Q# | 四判据 | ⚠️ 标注 | 来源 |
|----|--------|---------|------|
| Q1 TS-KF 治 LEO-LEO Doppler | 全过 | ⚠️链路（LEO-LEO 星间）| #1 |
| Q2 二阶 DPLL+前馈 CPR | 全过 | ⚠️利益相关（BIT 同实验室）⚠️收敛慢仅 QPSK | #2 |
| Q3 adaptive MMSE time-packing | 全过 | ⚠️链路（feeder link，S007 边界待判）| #3 |
| Q4 data-aided 多格式 DSP | 未过 C⚠️ | 缺直接 head-to-head，作方法借鉴 | #6 |
| Q5 DSP 辅助 AFC 闭环（BUPT）| 未过 C❌D❌ | 无 BER-vs-baseline，作方法借鉴（架构可复用）| 新1 |
| Q6 三 PD 自相干偏振解复用 | 部分过 B 部分 | ⚠️链路（GEO 35000km 非 LEO），作机制借鉴 | 新3 |
| Q7 两阶段 CFE 治 LEO-LEO DS | 全过 | ⚠️链路（LEO-LEO 星间真空非星地）| 新2 |
| Q8 PCS+Rs 治 LEO-地 Doppler | 全过 | ⚠️增益来自 Rs 适配**非 PS**（不同构 N1）⚠️FEC 假设理想 | 新4 |
| Q9 PS+RCM 治湍流 | 未过 D⚠️ | ⚠️部分同构 N1 + 链路地面短距，作方法借鉴 | 新5 |
| Q10 PS-QAM Gamma-Gamma 理论 | 全过 | ⚠️**高度同构 N1**（高 SNR>16dB uniform 反超 PS 趋零）| 新6 |

**Q# 浮出观察（线索，非结论，不塞方向）**：
- Q8（PCS+Rs 治 Doppler）"同门范式"味最浓（场景→失效→切入点完整，~100Gbps 增益），**但增益来自符号率适配非 PS**——叙事重心是"参数自适应对抗硬件带宽/Doppler 耦合"。
- PS 三篇同构性梯度：Q8（不同构，PS 作使能件）> Q9（部分同构，消融不全）> Q10（高度同构 N1）。块 E 提炼 PS 角度优先 Q8，避开纯 PS gain（Q10 已证无效）。
- **链路匹配缺口**：Q1/Q7 LEO-LEO 星间，Q9 地面短距，Q6 GEO。**星地 LEO + 湍流 + Doppler 三者联合的端到端 Q# 本批没有**——块 D 补检索明确盲区。

## 下一步干什么（块 D Step 3.5 定向补检索）

**按 groundwork.md:33 必做**，用块 C Q# 清单新认知做一轮定向检索弥补盲区。本轮（块 D）任务（1 个对话，0.5-1 对话量）：

1. **读必读文件**（按下方"必读"顺序）
2. **定向补检索 3 个明确盲区**：
   - **盲区 A（最高优先）**：星地 LEO + 湍流 + Doppler 三者联合的端到端 DSP 处理论文（本批 10 篇没有一篇做三者联合）。检索词建议：satellite-to-ground coherent FSO turbulence Doppler joint compensation / LEO downlink DSP turbulent channel Doppler / 等。用 tools/search + 必要时 tools/blit（IEEE）。
   - **盲区 B**：Viterbi-Viterbi CPR 经典（被 #1/#2/#新1 共同引用但 GW 未覆盖）+ Diniz 两阶段 CFE[50]（被新2 引用）。这些是 baseline 候选的 foundational 文献。
   - **盲区 C**（可选）：竞品共同引用的其他未覆盖文献（literature_notes.md "写作架构参考"节列了候选）。
3. **偏航检查**（H002/H005 继承）：A 方法中性（不锁模块，除非诊断动作）/ B 全留无臆造 / C 不滑回开题线索 / D 每步说 why / E 死地标记饱和不标难验证。
4. **产出**：新检索结果入 landscape.md（或 search-archive/{date}/）+ literature_notes.md 补充精读条目（如发现新强候选）或浅读条目（如只是覆盖面补充）。
5. **判定**：若新检索发现 ≥1 篇星地 LEO + 湍流 + Doppler 联合的强候选 → 补精读入 Q# 清单（可能新增 Q11+）；若仍无 → 记录盲区为"领域结构性缺口"（可能本身是机会信号，块 E 评估）。
6. **块 D 完成 → 块 E Step 4a Go/No-Go**（每个 Q# 走 gw-feasibility A0/A'/A/B/D）。

**不要在块 D 做**：不判 Go（块 E 的事）/ 不跑 MVE（块 E 的事）/ 不改框架文件（D004 待 Step 3 验证后再改）/ 不塞方向给用户（补检索给数据，块 E 才判）。

## 纪律（和块 D 直接相关的约束）

1. **不跳四判据终审进 Step 4a**（块 D 是 Step 3.5 补检索，补完仍要回 Q# 清单，不直接判 Go）
2. **检索词过用户审**（H005 继承 + S008 教训：用户对检索词性价比敏感"容易弄不出好东西"，IEEE 限流债务处理原则：增量价值 < 执行成本时留债务不重跑不卷用户）
3. **子 agent 强制委托**（AGENTS.md）：检索执行派子 agent，主对话只接收结构化摘要，不直接 WebSearch/webReader（主对话严禁，上下文爆炸风险）
4. **PS 方向警惕 N1 同构**：若补检索发现新 PS 候选，必须核查"增益是否依赖时变信道"。纯固定信道 PS gain≈0（N1/Q10 已证），PS+另一机制治具体失效才有戏
5. **场景对称性核查**：补检索候选要注意链路类型匹配用户标题"星地"（Q1/Q7 星间、Q6 GEO、Q9 地面都出范围，星地 LEO + 湍流 + Doppler 才是核心目标）
6. **导师边界**（S007）：feeder/ISL 系统级/QKD/深空不算处理。Q3 feeder link / Q7 ISL 边界块 E 判断"DSP 模块级算不算"，块 D 补检索时注意不要把系统级候选当处理技术收

## 必读（块 D 新对话开始时按此顺序读）

1. **本文件 H006**（交接当前状态 + Q# 清单表 + 盲区）
2. **S015**（块 C 全流程 + Q# 浮出观察 + 诚实预期）
3. **literature_notes.md**（projects/thesis-fso/，重写后的完整版：10 篇 L## + 综合分析 + Q1-Q10 清单）— **重点读 Q# 清单表 + "综合观察线索"段**
4. **H005**（块 B 补精读 + 候选池表，本文件是其续接）
5. **topic-index.md 不变量段**（D005 务实路线是第 1 条 INVARIANT；判据 A 已降级；S007 处理技术边界）
6. **decisions.md D005+D004+D003**（务实标准 + 找角度范式 + 回 Step 3）
7. **stages/groundwork.md:33**（Step 3.5 定向补检索的操作要求）
8. **thesis-lessons.md TL-30/31/32/33**（跳步/凭记忆/标准不对称/自欺式跳步）

## 接口变更（如有代码改动）

无代码改动（本轮全是文档重写 + 综合分析 + Q# 清单 + 文档交接）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| ~~literature_notes.md 是旧方向~~ | gw-read.md 要求精读入 literature_notes.md | **✅ 本轮 S015 已清偿**（10 篇全写入 + 综合分析 + Q#）| — |
| ~~master-state.md GW Progress 表 Step 2/3 ⬜~~ | FR-22 唯一可查状态 | **✅ 本轮 S015 已清偿**（Step 2/3 ✅，Q# 清单非空）| — |
| tools/download urllib 不走代理 | 下载工具应能下 OA/IEEE | 本轮用 blit 绕过，但非 IEEE 源(SPIE/Optica/MDPI)仍下不到 | 块 D 若需补下载再处理（修 paper_download.py 加 _detect_proxy 仿 S005 blit 修法）|
| #590 ECOC 2022 无 DOI 未下 | Step 2 下载完整性 | #580(JLT 期刊版)已下，信息更全，#590 暂可缺 | 块 D 若需 #590 细节再处理 |
| PS 方向 N1 同构风险 | D005"不画饼救旧" | 新6 高度同构 N1，新5 部分同构，新4 不同构 | 块 E 提炼 Q# 时按"PS+另一机制治具体失效"筛，避开纯 PS gain |
| D004 框架打磨待验证 | "先测不改协议" | D004-a/b/c 已记入 decisions.md + AGENTS.md FR-25/26 索引，框架文件未改 | Step 3 走完（本轮✅）+ 块 E 验证 D004-a 有效后再改 gw-read.md/gw-feasibility.md |
| Q# 清单全部带 ⚠️ | 四判据不可放水 | 6 篇全过但都有链路/利益相关/同构 N1 标注 | 块 E 走 gw-feasibility 逐条诚实判定 |

## 验证阈值（如涉及验证体系）

本轮不涉及验证体系。后续 Go/Kill 标准（务实路线下，D005）：
- **Go**：方法 > 传统未优化 baseline（参考同门 2-4dB 量级，具体阈值块 E 定）
- **Kill**：连传统 baseline 都赢不了 / 方法增益 <0.5dB 且无次指标维度 / MVE FAIL
- **不放水**：不接受孤证/伪命题/标题联想（底线）
- **PS 方向额外**：纯 PS gain（固定信道）≈N1 已证无效；PS+另一机制治具体失效才考虑
- **FR-21 触发条件**（D004-a/TL-32）：只在 Step 3 走完（本轮✅）+ 判据 A 成立后才触发，**只当 Step 4a 维度 D 收尾 Kill 工具，禁当 Go 判据**

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（D005 务实路线是第 1 条 INVARIANT）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] literature_notes.md 已重写含 Q# 清单（核查：`grep -cE '^\| Q[0-9]' projects/thesis-fso/literature_notes.md` 应 = 10。注意：旧命令 `grep -c "^| Q"` 会把表头行 `| Q# | M...` 也数进去得到 11，且未转义 `|` 在 ripgrep/ZCode Grep 工具里是 alternation 会爆炸到几百，勿用）
  - [ ] master-state GW Progress 表 Step 3 = ✅（核查：`grep "3 read" projects/thesis-fso/master-state.md` 应含 ✅ + 2026-06-26）
  - [ ] S015 session note 已落盘（核查：`ls .sessions/2026-06-20-problem-driven-redirection/S015*.md`）
- [ ] 已检查 _registry.yaml 中本专题 status = active（无 conflicts_with）
- [ ] 已确认当前范围未违反"明确不含"（仍要导师同意 S007 边界 / 仍不接受孤证凑数 / 方法必须指标提升 / 不跳四判据不跳 Go）

## 下一轮（块 D Step 3.5 定向补检索）

**先做完块 D 再进块 E（Step 4a Go/No-Go）**，严格不跳步：

### 块 D 任务（0.5-1 对话）
1. 读本 H006 + S015 + literature_notes.md（重点 Q# 清单 + 综合观察线索）
2. 定向补检索 3 盲区（星地 LEO+湍流+Doppler 联合 / VV CPR 经典+Diniz CFE[50] / 竞品共同引用未覆盖文献）
3. 检索词过用户审（H005 纪律 + S008 IEEE 性价比教训）
4. 派子 agent 执行检索（主对话严禁 WebSearch/webReader）
5. 偏航检查 A-E（H002/H005 继承）
6. 新候选入 landscape.md / search-archive；若强候选补精读入 Q# 清单（Q11+）
7. 块 D 完成 → master-state Step 3.5 ⬜→✅

### 块 E（Step 4a Go/No-Go，1-2 对话）
- 每个 Q#（含块 D 新增）走 gw-feasibility 维度 A0/A'/A/B/D
- 务实标准：维度 A 对手=传统 baseline（D004-a）；FR-21 只当参考（TL-32）；MVE 快速试错
- 至少 1 个 Q# Go 才进块 F（Step 5-7 baseline 复现）

**关键提醒**：
- **不跳步**：块 D 没做完不进块 E
- **Q# 从清单浮出**：不从单篇联想，不标题联想试 MVE（TL-30）
- **PS 警惕 N1 同构**：纯 PS gain 无效，PS+另一机制治具体失效才考虑
- **场景匹配**：星地 LEO + 湍流 + Doppler 联合是核心目标（本批缺口），出范围的链路（星间/GEO/地面）提炼 Q# 时注意
- **导师边界**：S007 feeder/ISL 系统级/QKD/深空不算处理——块 E 判断 DSP 模块级算不算
