# 新对话提示词：COMPARISON_REFS 整合 Kam 3 篇 + 4 候选优先级讨论

> 来源: 主控对话 2026-07-08 溯源轮（无 S### 编号，主控对话不建 session note）
> 交接目标: 新对话讨论 COMPARISON_REFS 怎么整合 Kam 3 篇 + 拍板 B5/B3-Q2 优先级
> 日期: 2026-07-08
> 文件名: PROMPT-004-comparison-refs-integration-and-priority.md
> **修订 v2**：修正 NDA-ML 认知差错（S011 DPLL + S012 适配转向，非 dormant）

---

## 你是谁

你是主控对话（control tower），角色 = 方向决策 / 跨候选调度 / 核查工作对话产出 / 跟用户交互。**不自己执行仿真/精读**（那是工作对话的事）。

**⚠️ 主控对话失守警告**：本控制塔在 2026-07-08 已发生 **4 次状态认知滞后**（B7 S003→S006 / B5 范围优势证伪 / NDA-ML D-009 层 4 / NDA-ML S011+S012 适配转向）。根因 = profile 第 9 次"急于推进"在主控侧的表现——急于开新专题/派溯源但忽视跟踪现有候选进度。**本对话必须先核查再发言，不凭记忆报状态**。

## 本轮要干什么

两件事，用户拍板优先级：

### 事项 1：COMPARISON_REFS 整合 Kam 3 篇方法血缘链

**背景**：上一轮主控对话派 2 子 agent 向上溯源，从 Du PTL 2025 的 references 里找到 Kam 课题组 3 篇 Trans 级论文并下载落盘。这是用户"从来源向上溯源"直觉的验证——方法来源可从 Letters 升到 Trans 级方法链。

**3 篇已落盘**（papers/doi/ 下，含 source.pdf + content.md + metadata.json）：

| # | 引用 | 期刊 | 年份 | DOI | 落盘路径 | 角色 |
|---|---|---|---|---|---|---|
| [6] | JLT 2021 Du/Kam OFDM 联合同步前作 | JLT | 2021 | 10.1109/jlt.2020.3042546 | papers/doi/10.1109_jlt.2020.3042546/ | Du 团队方法体系前作 |
| [13] | TSP 2022 Wang/Kam 单正弦 ML/MAP | TSP | 2022 | 10.1109/tsp.2021.3137966 | papers/doi/10.1109_tsp.2021.3137966/ | **Du 直接方法源** |
| [15] | TIT 2013 Fu/Kam AOPN 模型 | TIT | 2013 | 10.1109/tit.2013.2238604 | papers/doi/10.1109_tit.2013.2238604/ | 理论源头 |

**方法血缘链**（子 agent 1 读 content.md 确认）：
```
Du PTL 2025 (M-APSK + 升M₀次幂 → 单正弦频相 ML)
   ↑ 直接方法源（Du line 29/135 "based on our earlier work in [13]"）
[13] TSP 2022 (Wang/Kam, 单正弦 Wiener PN 下 ML/MAP 闭式)
   ↑ 理论模型基础（AOPN 高斯近似）
[15] TIT 2013 (Fu/Kam, AWGN 单正弦时域相位估计 + AOPN Tikhonov 模型)
+ [6] JLT 2021 (Du/Kam OFDM 联合同步前作，35 refs 全景)
```

**近年续作查清**（子 agent 2 用 DBLP 全量档案 Kam 180 篇 + OpenAlex + Crossref 三源交叉）：
- Kam 课题组 2022+ **没有新的"严格 Trans + NDA ML 载波同步"对口续作**
- 严格 Trans 对口的只有 TSP 2022（已下载，非新发现）
- 候选 2（TCOM 2023 MPSK BEP）严格 Trans 但偏性能分析非 estimator
- 候选 4（TCOM 2024 Liu/Du/Ye/Yu RSOP）严格 Trans 但 Kam 非合著
- Kam 本人 2025+ 转向 UAV/语义通信，脱离 NDA 载波同步主线
- **溯源天花板就是这 3 篇**

**叙事升级**（待新对话跟用户讨论怎么写进 COMPARISON_REFS）：
- 原：方法来源 Du PTL 2025（Letters）——导师担心"达不到 Trans"
- 新：方法来源 = Kam 课题组 Trans 级方法链（JLT 2021 + TSP 2022 + TIT 2013），Du PTL 2025 是 M-APSK 单载波 FSO 延伸
- 严格 Trans 占比：原 7/17 (41%) → 加 Kam 3 篇后 10/20 (50%)
- 近年+严格 Trans：原 5/17 (29%) → 加 JLT 2021 + TSP 2022 后 7/20 (35%)（TIT 2013 不算近年）

**待决策**：
1. 3 篇是否深度精读（按 gw-read 模板）？公式都部分丢失（pymupdf4llm 把 display equation 渲染成图片占位），深度精读需回 PDF。还是只做初步定位（已完成）够发导师？
2. COMPARISON_REFS 怎么整合——新增"方法来源链"一节？还是改写 §一 A 段（方法思想来源）？
3. 给导师的版本怎么处理——COMPARISON_REFS.md 当前是给自己用的纪律文件（含诚实档级标注+自我反思+待老师定问题），给导师的版本应精简成纯清单+核心差距说明。导师已催"昨天说的对比参考文献请单独发给我"。

**⚠️ 跟 D-010 baseline 标准的关系**：D-010 标准 4 要求"近年+权威 Trans 级"。Kam 3 篇里 JLT 2021 + TSP 2022 满足近年+严格 Trans，TIT 2013 严格 Trans 但非近年。但这 3 篇是"方法来源链"不是"并列 baseline"——D-010 标准 4 主要管 baseline，方法来源的档级是另一维度。整合时要想清这 3 篇在 COMPARISON_REFS 里的角色（来源链 vs baseline）。

**关键文件**：
- `projects/simulation/COMPARISON_REFS.md`（117 行，待整合）
- `projects/simulation/REVIEW_NOTES.md`（导师 5 条意见 + 通用清单）
- `papers/doi/10.1109_lpt.2024.3523478/content.md`（Du PTL 2025 全文，references 在 line 193-224）
- `papers/doi/10.1109_jlt.2020.3042546/content.md`（JLT 2021）
- `papers/doi/10.1109_tsp.2021.3137966/content.md`（TSP 2022）
- `papers/doi/10.1109_tit.2013.2238604/content.md`（TIT 2013）

### 事项 2：4 候选优先级拍板

**当前 4 候选状态**（2026-07-08 最新，已核查）：

| 候选 | 状态 | 进度 | 下一步 | 阻塞点 |
|---|---|---|---|---|
| **B7 Gardner TED** | active | S006 sandbox 5+6a 完成，smoke test 全绿 | **用户那边在跑正式 MVE**（对话 7，4096×3×24×3 ~600s + Go/Kill）| 无（最接近出结果）|
| **B5 LEO Doppler** | active 路线变更 | S005 范围优势证伪转路 2 | **路 2 重走 Step 3-4a**（补精读 Vieira 2023 + Diniz 2011）| V3 对照对象需改 Vieira 同族 |
| **B3-Q2 联合估计** | active | S001 开题+阶段 0 规约，H001+PROMPT-001 就位 | **派工作对话执行阶段 0.1**（4 支路迁移验证 + 单链路 CRB）| 工作对话未启动 |
| **NDA-ML B11-Q1** | **active（非 dormant！）** | S011 DPLL 异族 baseline 池立住 + S012 适配方法论转向 + 3 实验派发 | **3 个并行适配实验待结果**（A1 参数自适应 / A3 NDA+DPLL 混合 / A4 DA/NDA 条件切换）| 3 实验提示词未落盘（在对话里给的）|

**NDA-ML 详细状态（S011 + S012，修正认知差错）**：

**S011 DPLL 异族 baseline 仿真完成**：
- DPLL DD 闭环跟 NDA-ML weak/moderate 持平、AWGN 稍差（+0.103dB）——NDA-ML 升幂 ML 闭式比 DD 闭环稍有优势
- baseline 池立住：DA-ML（主，架构对立非近亲）+ DPLL（异族 DD 闭环）+ VV/BPS（fellow 同族一句带过）
- D-010 导师电话确立 baseline 选取 5 条标准（同场景/同类型层级/不找接近方法/近年权威/看够好的）

**S012 方法论转向 + 3 实验派发**：
- 从"锁死 NDA-ML 内部找增量"转向"4 种适配扫描找方法间优势关系"
- 4 种适配方法论（A1 参数适配 / A2 结构适配 / A3 组合适配 / A4 条件适配）落进 skill `sim-preflight/rules/adaptation-scan.md`，commit 151feb0 v1.2.0
- **3 个并行实验已派发**（提示词给在对话里未落盘）：
  - A1 参数自适应：D-009 K 扫描信号——最优 K 随线宽变，验证自适应 K > 固定 K
  - A3 NDA+DPLL 混合：NDA 前馈无失锁 + DPLL 闭环高精度理论互补，验证混合 > 单一
  - A4 DA/NDA 条件切换：fair_gain 随湍流递增信号，验证切换 > 单一方法全 SNR
- 导师思想重新解读："不锁方法 → 在场景里找方法间优势关系 → 存在优势区间 + 理由 → 能发"

**⚠️ NDA-ML governance 缺口（待处理）**：
1. topic-index 状态行停在 S011，S012 方法论转向 + 3 实验派发未更新进 topic-index
2. 3 个实验提示词未落盘（S012 line 91 说"提示词已给用户"但 .sessions/ 无 PROMPT-001/002/003）
3. skill 版本叠加：CHANGELOG v1.2.0 已 commit，但 v1.3.0（V1-V6+C6-C8+interrupt 10-12）是未提交改动（SKILL.md + CHANGELOG.md 在 git status modified）

**用户约束**：
- "保持 3 方向同时跑"（现在 B7 在跑 MVE + NDA-ML 3 实验在跑 = 实际 4 路并行，B5/B3-Q2 待决策是否加派）
- "有点急"（profile 第 9 次"急于推进"防线激活）
- 导师"特长场景"标准：新方法不是要求全能，是在某一实际需求场景下的特长（场景必须真实工程）
- D-010 baseline 5 条标准（同场景星地湍流 / 同类型载波同步定时均衡层 / 不找接近方法 / 近年权威 Trans / 看够好的）

**待决策**：
1. B7 MVE 结果出来后怎么判 Go/Kill（守 FR-25 Go/Kill 分离 + sim-preflight v1.3.0 V3 祖师爷警报）
2. B5 路 2 重定位要不要现在派工作对话（补精读 Vieira+Diniz → 新 M-C-A → Step 4a）
3. B3-Q2 阶段 0.1 要不要现在派工作对话（H001+PROMPT-001 已就位）
4. NDA-ML 3 实验结果回来后怎么集成（哪个出信号追哪个，S012 后续已定）
5. NDA-ML governance 缺口要不要补（topic-index 更新 + 3 提示词落盘 + skill v1.3.0 提交）

## 不要做什么

1. **不自己执行仿真/精读**——主控对话角色，派工作对话或核查产出
2. **不臆测导师"特长场景"指什么**——H006 已记"新对话要跟用户讨论清楚"，不要替用户解读
3. **不强行 Go**——profile 画像"警惕主线急于给方向性结论"，B7/3 实验结果没出不要预判
4. **不跳框架**——FR-22 GW 流程门控，B5 路 2 必须重走 Step 3-4a 不能直接跑 MVE
5. **不重复 6 类混乱**（NDA-ML 教训）——参数反复/算法 bug/验证失效/方向重定位/文件混乱/文献引用
6. **不凭记忆报状态**——主控对话已 4 次状态认知滞后，本对话必须先核查再发言
7. **不臆造 NDA-ML 3 实验结果**——提示词未落盘，结果未回传，不知道就说不知道

## 必读（按优先级）

1. `projects/simulation/COMPARISON_REFS.md`（117 行，待整合的现有版本）
2. `projects/simulation/REVIEW_NOTES.md`（导师 5 条意见 + 通用清单，§一 逐条核查）
3. `.sessions/2026-07-06-step4a-mve-execution/S012-adaptation-scan-methodology-and-parallel-experiments.md`（**NDA-ML 适配方法论转向 + 3 实验派发**，修正 dormant 认知）
4. `.sessions/2026-07-06-step4a-mve-execution/S011-dpll-ablation-baseline-pool-established.md`（DPLL 异族 baseline + baseline 池立住）
5. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-010（导师 baseline 5 条标准）+ D-008/D-009（算法层堵死前提，但已被 S012 适配转向超越）
6. `.sessions/2026-07-08-b7-gardner-ted-foe/H006-conversation6-script-spec-smoke.md`（B7 交接，对话 7 正式 MVE 待跑/在跑）
7. `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/H006-conversation6-path2-reposition.md`（B5 路 2 重定位交接）
8. `.sessions/2026-07-08-b3-joint-estimation/H001-conversation1-stage0-migration-and-a1.md`（B3-Q2 阶段 0.1 交接）
9. `.sessions/profile.md`（9 条画像，最相关"警惕主线急于给方向性结论"）
10. `papers/doi/10.1109_lpt.2024.3523478/content.md` line 193-224（Du PTL 2025 references 段，3 篇 Kam Trans 出处）

## 接口变更（代码改动）

无（本轮主控对话只核查 + 派子 agent 下载论文，没改代码）

**已知未提交改动**（NDA-ML 工作对话留下的，非本对话产生）：
- `.claude/skills/sim-preflight/SKILL.md` + `CHANGELOG.md` modified（v1.3.0 未提交）
- `projects/simulation/common/_recovery.py` modified
- `projects/simulation/explore/b7-gardner-ted-foe/` 多文件 modified（B7 sandbox 产出）
- `projects/simulation/results/nw_sweep.json` modified

## 失败数据附录

**Kam 课题组近年续作查清——无新对口 Trans**（子 agent 2 DBLP 全量档案确认）：
- 严格 Trans + NDA ML 载波同步对口的只有 TSP 2022（已下载，非新发现）
- 候选 2（TCOM 2023 MPSK BEP）严格 Trans 但偏性能分析非 estimator
- 候选 4（TCOM 2024 Liu/Du/Ye/Yu RSOP）严格 Trans 但 Kam 非合著
- 溯源天花板 = JLT 2021 + TSP 2022 + TIT 2013 这 3 篇

**3 篇公式部分丢失**（pymupdf4llm 对 IEEE 双栏 PDF 限制）：
- display equation 全渲染成图片占位（`**==> picture [w x h] intentionally omitted <==**`）
- 文字/结构/参考文献完整可读
- 深度精读需回 source.pdf 看公式

**主控对话 4 次状态认知滞后记录**（本对话必读警告）：
1. B7 S003→S006：以为 B7 在 S002，实际 S005 sandbox 4/6
2. B5 范围优势证伪：以为 B5 刚开，实际 S005 MVE 已跑完范围优势已证伪
3. NDA-ML D-009 层 4：以为 D-009 待判，实际层 4 全堵死
4. NDA-ML S011+S012：以为 dormant 等消化导师反馈，实际 DPLL 池立住 + 适配方法论转向 + 3 实验派发

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| COMPARISON_REFS 未整合 Kam 3 篇 | 导师要求近年+Trans | 3 篇已落盘+初步定位，待新对话讨论整合方式 | 本对话事项 1 |
| 给导师版本未整理 | 导师已催 | COMPARISON_REFS 是纪律文件不宜直发 | 本对话事项 1 决策后 |
| 3 篇未深度精读 | gw-read 模板 | 子 agent 1 只做初步信息提取 | 视整合需要决定是否精读 |
| B5 路 2 未启动 | FR-22 重走 Step 3 | H006 交接就绪 | 本对话事项 2 决策后派工作对话 |
| B3-Q2 阶段 0.1 未派 | H001+PROMPT-001 就位 | 工作对话未启动 | 本对话事项 2 决策后派工作对话 |
| NDA-ML topic-index 滞后 S011 | session-governance | S012 转向未进 topic-index | NDA-ML 下次工作对话补 |
| NDA-ML 3 实验提示词未落盘 | AGENTS.md PROMPT 规则 | 在对话里给的 | NDA-ML 下次工作对话补 |
| skill v1.3.0 未提交 | git 卫生 | SKILL.md + CHANGELOG.md modified | NDA-ML/B7 工作对话收尾时提交 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| Kam 3 篇下载落盘 | 3 篇 source.pdf + content.md + metadata.json 齐全 | AGENTS.md 文件路径规则 | ✅ PASS（子 agent 1 验证）|
| Kam 3 篇 DOI 核验 | Crossref vol/issue/year/page 与 Du references 一致 | FR-26 证据链 | ✅ PASS（子 agent 1 验证）|
| Kam 课题组近年续作查清 | DBLP 全量档案 + OpenAlex + Crossref 三源交叉 | FR-26 证据链 | ✅ PASS（子 agent 2 验证）|
| 方法血缘链确认 | Du content.md line 29/135 明确引 [13] 为方法源 | FR-26 证据链 | ✅ PASS（子 agent 1 验证）|
| NDA-ML S011 DPLL baseline | TL-20 四判据全 PASS + DPLL 异族合规 D-010 标准 3 | S011 | ✅ PASS |
| NDA-ML S012 适配 skill 落地 | adaptation-scan.md + SKILL.md 索引 + commit 151feb0 | S012 | ✅ PASS |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取本提示词的"3 篇 Kam Trans 论文"段 + "方法血缘链"段
- [ ] 已读取本提示词的"NDA-ML 详细状态（S011 + S012）"段（**修正 dormant 认知**）
- [ ] 已验证至少 5 条关键事实声称：
  - [ ] 3 篇已落盘（核查 `ls papers/doi/10.1109_jlt.2020.3042546/ papers/doi/10.1109_tsp.2021.3137966/ papers/doi/10.1109_tit.2013.2238604/` 含 source.pdf + content.md）
  - [ ] 方法血缘链（核查 `papers/doi/10.1109_lpt.2024.3523478/content.md` line 29/135 引 [13]）
  - [ ] Kam 近年续作查清（子 agent 2 用 DBLP 全量档案，无新对口 Trans）
  - [ ] NDA-ML S011 DPLL baseline 池（核查 S011 + DPLL/NDA 持平数据）
  - [ ] NDA-ML S012 适配转向（核查 S012 + adaptation-scan.md skill + commit 151feb0）
- [ ] 已读取 COMPARISON_REFS.md 现有版本（117 行）
- [ ] 已读取 profile.md（9 条画像，最相关"警惕主线急于给方向性结论"）
- [ ] 已确认当前范围：事项 1（COMPARISON_REFS 整合）+ 事项 2（4 候选优先级）—— 不自己执行仿真/精读

## 下一轮

**本对话（新对话）任务**：
1. 跟用户讨论事项 1（COMPARISON_REFS 整合 Kam 3 篇方式 + 给导师版本处理）
2. 跟用户讨论事项 2（4 候选优先级，特别是 B5 路 2 / B3-Q2 阶段 0.1 要不要现在派工作对话；NDA-ML 3 实验等结果；NDA-ML governance 缺口补不补）
3. 视用户决策派工作对话或整理 COMPARISON_REFS
4. 守主控对话角色：不自己执行，派工作对话或核查产出
5. **守"先核查再发言"**——本控制塔已 4 次状态认知滞后，任何状态报告必须先读对应文件验证

**不在本对话做**：
- 不跑 B7 正式 MVE（用户那边在跑）
- 不跑 NDA-ML 3 适配实验（已派发，等结果）
- 不深度精读 Kam 3 篇（除非用户要，派工作对话）
- 不臆测导师"特长场景"指什么（等用户说）
- 不替 NDA-ML 工作对话补 governance 缺口（topic-index/提示词落盘是那边的事，主控只标记债务）
