# Task Brief: RML-FSTS Groundwork Step 3 全文精读

> 来源: S002 | 产出位置: `projects/thesis-fso/literature_notes_rml_fsts.md` + 本专题 R003/V002/H002
> 日期: 2026-08-09
> 唯一文档: 执行方必须完整读取本文件；只可读取本文件列出的规范、项目状态、五篇冻结全文和既有 read-notes

---

## 0. TL;DR（执行方先读）

你在 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。RML-FSTS 正式 Groundwork Step 1 已 PASS；Step 2 已获得 5 篇合格 CORE 且覆盖 C1–C4。用户已接受这 5 篇作为 Step 3 输入边界，当前状态=`STEP3_DISPATCH_READY`。

**你的任务**：只执行 GW Step 3。先闭合五篇论文的 title/identity/source-path preflight，再由 fresh-context 子 agent 完整读取冻结的 5 篇全文，按 `stages/gw-read.md` 完成标准 14+ 字段、7 个结构化子表、通信参数、五篇实验完备性、三篇写作架构、全局 read-notes/read-log、综合分析与 canonical Q# 清单；到 Step 3 completed 或 `BLOCKED/IN_PROGRESS` 状态停止。

**产出**：更新 `projects/thesis-fso/literature_notes_rml_fsts.md`，生成/更新五篇全局 read-note、read-log、R003、Step 3 receipt、D004（仅记录实际 Step 3 裁决）、V002 与 H002，并同步 topic-index/registry/master-state。独立 verifier 通过后只做一次统一 commit，不 push。

**最高纪律（违反一条就废了）**：

1. 本轮只做 Step 3。严禁 Step 3.5、Step 4a、补充检索、引用链搜索、预注册 smoke、方法设计/实现、仿真、MVE、Contract 或 Execute。
2. 精读论文全文必须委托 fresh-context 子 agent；主控只做范围、派发、结构化结果集成和最终状态判断，不自行逐行消化 `content.md`/`source.md`。
3. 四判据只允许使用 `stages/glossary.md` canonical 四项：具体 M-C-A 技术矛盾、可复用方法产出形态、近期 baseline、可量化对标。禁止增加或替换为 `problem_truth/actionability/novelty/thesis_fit`。
4. 判据 1 不要求目标 defect 或 A 已被 MVE 证明；novelty 不属于 Step 3 四判据。目标星地 lag-ranking crossover、conditioned-single-lag failure 均保持 `INFERENCE/UNKNOWN`，不得偷换成事实。
5. source defect 只允许写成 Wang 2023 fixed lag/`BL` 取值依赖 modulation/training length/received power，低功率存在 timing/FOE 退化。target defect、headroom、cheap comparator 胜负留给下游。
6. 缺失全文、标题/摘要和 Tang/WiSEE provenance 矛盾不得承重公式、失效机制、实现细节或 novelty；本轮不得获取第六篇论文来凑门。
7. Yu 2023 必须先完成 byte-identical canonical path + title/DOI preflight。闭合失败则 title-abort，Step 3 保持 `BLOCKED/IN_PROGRESS` 并返回 Step 2；不得静默把 `source.md` 冒充模板要求的 `content.md`。
8. 该研究对象是确定性通信 DSP，不是 DRL/监督学习。状态/动作/奖励/网络架构等不适用字段必须写 `N/A（非学习型确定性估计器）` 并说明理由，禁止硬造 MDP 或神经网络。
9. 若没有任何 Q# 通过 canonical 四判据，Step 3 必须保持 `BLOCKED/IN_PROGRESS`，记录框架规定的 `gw-search → gw-acquire → gw-read` 恢复路径；不得自造 `STEP3_NO_VALID_PROBLEM` 或其他 terminal，不得进入 Step 3.5。
10. 若全部质量门通过，只将两处 GW Progress 的 Step 3 标为 `✅ completed`；框架没有定义 `STEP3_PASS` terminal，不得新造名称。
11. 不修改论文正文、科学代码、仿真参数、正式论文、旧专题、Skill 或四个 `p05_run*.log`。既有 shared paper library 只读；Yu 的 canonical adapter 只能在 worktree ignored paper path创建 byte-identical 副本并留 receipt，不能改 shared source。
12. 执行与验证分离；一次统一 commit，不 push，不暂存四个 `p05_run*.log`。

---

## 1. 权威背景与执行前恢复

### 1.1 必须完整读取

1. `.sessions/2026-08-08-rml-fsts-groundwork/topic-index.md`
2. 同专题 `decisions.md` D001–D003、`S002-step3-dispatch.md`、`R002-step2-acquisition-coverage.md`
3. `projects/thesis-fso/rml-fsts-groundwork/step2-coverage-report.md`
4. `search-archive/2026-08-08/rml-fsts-step2-acquisition-receipt.json`
5. `projects/thesis-fso/literature_notes_rml_fsts.md` 与 `projects/thesis-fso/master-state.md` 当前 RML-FSTS GW Progress
6. `stages/groundwork.md`、`stages/gw-read.md`、`stages/glossary.md`
7. `templates.md` 的 literature_notes 模板、`domain-comms.md` §1.1
8. `thesis-lessons.md` 速查表与 TL-30–TL-33
9. `.sessions/2026-08-02-fso-amc-groundwork/decisions.md` D005（自创 Step 3 语义门失败先例）
10. `.sessions/profile.md`；调用 `session-governance` 做 session start / scope / T001 接收报到

### 1.2 执行前必须验证并写入 S002 续接记录

- D003 是否只授权 Step 3，且 Step 3.5+ 仍被明确排除；
- master-state 与 literature owner 是否均为 `STEP3_DISPATCH_READY`，Step 3 尚未完成；
- 五篇冻结 CORE 是否仍存在且 SHA256 与 Step 2 receipt 一致；
- source/target defect、strongest conditioned lookup、object/package failure=`0/0` 是否保持；
- `_registry.yaml` 中依赖为 `2026-08-08-ch4-reference-method-extension`、`conflicts_with: []`；
- 四个 `p05_run*.log` 的初始 SHA256、git status 与 staged 状态。

任一承重事实 FAIL 时停止，不自行改写历史。

---

## 2. 冻结精读输入与 source preflight

### 2.1 只读这 5 篇 CORE

| # | 派遣标题（Worker prompt 必须逐字带上） | DOI | CORE 角色 | 冻结全文 |
|---:|---|---|---|---|
| L01 | Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication | `10.1109/JPHOT.2023.3265847` | C1/C2/C4；source baseline | `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md` |
| L02 | Enhanced Frame Synchronization and Carrier Recovery in Coherent FSO Communication: a Pseudo-Random and Cyclic QPSK Approach | `10.1364/OE.520452` | C2/C4；近期 task-matched comparator | `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/content.md` |
| L03 | A Practical Scheme for Frequency Offset Estimation in MIMO-OFDM Systems | `10.1155/2009/821819` | C3；multi-correlation/multi-lag prior art | `papers/doi/10.1155_2009_821819/content.md` |
| L04 | Space-Ground Coherent Optical Links: Ground Receiver Performance With Adaptive Optics and Digital Phase-Locked Loop | `10.1109/JLT.2020.3003561` | C4；space-ground transfer physics | `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md` |
| L05 | Joint Physical Layer Frame Optimization and Carrier Synchronization for Satellite Communications | `10.1109/TVT.2022.3218937` | C3；stepwise correlation prior art | shared `D:/code/study/research-protocol/papers/doi/10.1109_tvt.2022.3218937/source.md`，须先适配为 worktree canonical `papers/doi/10.1109_tvt.2022.3218937/content.md` |

Morelli/Yu/Paillier 的角色不是 coherent-FSO FSTS 直接竞品；不得把 C3/C4 支撑升级成 target defect 证据。

L04 必须读取上表的共享 canonical 绝对路径（Step 2 receipt：bytes=`46966`、SHA256=`62E3BFDF6B803069342B49DC6D9F666899BD7257841E42D9A5003CFDFF5A9662`）。worktree 下同 DOI 的 `content.md` 是不同哈希副本，不属于本轮冻结输入，禁止误读或用其覆盖 shared canonical 文件。

### 2.2 title/identity abort 协议

对每篇在派发全文读取前执行 `gw-read.md` 步骤 0：

1. 若 `metadata.json title_check=match`，仍抽查正文首个非导航 H1/H2 与 DOI；
2. 若 `unverifiable` 或缺失，手工取首个非导航 H1/H2 与派遣标题计算/记录 token overlap，并核对 DOI；
3. 真正 title mismatch、主题不符、正文损坏或无法确认 DOI → `TITLE-MISMATCH/UNVERIFIABLE_ABORT`，不产 L## 笔记、不计 5 篇；本轮立即停止在 Step 3 `BLOCKED/IN_PROGRESS`，返回 Step 2。

Yu 2023 的 `source.meta.json` 现有 mismatch 来自把期刊页眉误取为标题；它不是可静默忽略的 PASS。必须：

- 从 `source.md` 首个实际论文 H2 抽取完整标题，并从正文核对 DOI `10.1109/TVT.2022.3218937`；
- 核对 shared `source.md` SHA256 必须仍等于 Step 2 receipt 的 `97DB13AB40E6548AE70A01C12027B7085CA3123976353C5683DAE3350D8924A6`；
- 只在 worktree ignored paper path 创建 byte-identical `content.md` adapter，复制后 SHA256 必须完全相同；不修改 shared `source.md`、`source.meta.json` 或正文字符；
- 将 source/destination absolute path、两边 SHA256、bytes、实际 H2、DOI 行、title overlap 和判定写入 `search-archive/2026-08-09/rml-fsts-step3-read-receipt.json`；
- 任一项不一致即 abort 返回 Step 2。不得通过改 metadata 字段把 mismatch 涂成 PASS。

receipt 同时记录其余四篇的 absolute path、SHA256、bytes、派遣标题、实际标题、overlap、DOI 与 preflight verdict。

---

## 3. Worker 派发与全文读取

### 3.1 并发与上下文纪律

- 第一批最多 3 个 fresh-context reader：L01、L02、L04；第二批最多 2 个：L03、L05。
- 每个 reader 只读自己被派的全文、对应 metadata 与本任务的字段模板；单 reader 不超过 15 分钟。
- L01/L02/L04 已有全局 read-note，只能作为历史对照；reader 必须重新核对全文并产出 RML-FSTS 目标适配增量，不得把旧 oversampled-sync 结论直接复制成本专题事实。
- 主控不得直接 WebSearch/WebReader；本任务也不需要任何 web/search。公式渲染缺失时可核对已有 source PDF，但不得自行补写无法辨认的公式。

### 3.2 每篇标准 14+ 字段（必须全部有值）

每个 reader 返回以下字段，并给 load-bearing claim 的 `源文件:行号/章节/公式/Table`：

1. DOI/来源；
2. canonical 源文件路径；
3. 发表状态；
4. 发表渠道；
5. 年份/会议或期刊；
6. 核心贡献（至少 2 句，含方法细节）；
7. 方法概述（2–3 句）；
8. 实验设置；
9. 使用的 baseline（逐项标自实现/引用；没有则明确“无对比实验”）；
10. 关键结论；
11. 与 RML-FSTS 研究对象关系；
12. 实现关键细节（必须含具体数值/公式；转换缺失则标证据限制，不臆造）；
13. 适配性分析（适配点、不适配点、仅作后续设计原料的改进启示）；
14. 开源代码状态；
15. 学术身份/全文验证状态；
16. FACT / INFERENCE / UNKNOWN 清单，明确 source-domain 与 target-FSO 边界。

### 3.3 结构化提取 7 子表（必须全部出现）

1. **状态/输入空间**：输入量、维度/范围、归一化或预处理；确定性算法按真实信号输入提取，不改写成 DRL state。
2. **动作/输出空间**：真实估计器/控制器输出、约束与粒度；非决策算法明确说明不是 action space。
3. **奖励/目标函数**：非学习型论文写 `N/A`，另列真实优化目标/评价量及完整公式（可辨认时）。
4. **建模假设**：内容、论文位置、对目标 FSO 迁移的影响。
5. **网络架构**：写 `N/A（非神经网络）`；另列真实 DSP 模块链、关键参数和复杂度。
6. **适配性分析**：1–2 条适配、1–2 条不适配、1 条启示；启示不是本轮方法设计。
7. **问题提取**：该论文自身解决的 M/C/A、A 的章节/公式定位、方法产出形态、canonical 四判据逐条 ✅/❌+理由。

### 3.4 通信参数表（每篇 MUST）

按实际论文提取：链路/场景、调制、符号率/采样率、training/frame 结构、CFO/相位噪声、接收功率/SNR、湍流/空间分集/AO/信道模型、关键参数值、来源章节/Table。论文未报告的字段写 `未报告`，不得补默认值。

### 3.5 实验完备性（五篇全部执行，≤20 行/篇）

每篇提取：

- main claims + bounded/universal scope；
- seeds/运行次数/error bar/统计检验；
- baseline 数量、类型、来源与公平调参声明；
- 消融/参数扫描设计；
- 信道模型与参数来源、场景/拓扑多样性；
- 理论/实测复杂度；
- Verification / Validation / Uncertainty 各 1–3 分并给一句依据。

---

## 4. 全局 read-note、read-log 与 literature owner

### 4.1 全局 read-notes

目标路径：

- `papers/_read_notes/10.1109_jphot.2023.3265847.md`
- `papers/_read_notes/10.1364_oe.520452.md`
- `papers/_read_notes/10.1155_2009_821819.md`
- `papers/_read_notes/10.1109_jlt.2020.3003561.md`
- `papers/_read_notes/10.1109_tvt.2022.3218937.md`

L01/L02/L04 已有笔记：保留原有事实与历史方向，补充/纠正 RML-FSTS 目标适配、canonical 问题提取和本轮证据；不得整篇覆盖导致旧 provenance 丢失。L03/L05 新建完整笔记。

### 4.2 read-log

更新 `projects/thesis-fso/read-log.md`：

- L01/L02/L04 增加重读次数，并在“用于方向”追加 RML-FSTS Step 3；
- L03/L05 新增 paper_id、canonical 源路径、read-note 路径、首读日期、重读次数、用于方向、alt_ids；
- 同一 paper_id 不得重复建两行。

### 4.3 literature owner 五篇条目

将五篇标准条目写入 `projects/thesis-fso/literature_notes_rml_fsts.md`。每篇的源路径必须能由 receipt 解析到真实文件；Yu 使用本轮闭合后的 worktree canonical `content.md`，并附 adapter receipt 指针。

---

## 5. 综合分析与 canonical Q#

### 5.1 必须完成的综合段落

1. 现有方法分类：FSTS/two-stage training-aided FOE、multi-lag/stepwise correlation、coherent space-ground carrier maintenance/transfer physics；
2. 已知局限：仅作为 gap/novelty 原料，不能直接当问题；
3. 2–3 年趋势；
4. 研究背景时间线与当前研究对象定位；
5. Baseline 交叉验证与 strongest cheap alternative 边界；
6. 五篇实验完备性对标汇总；
7. 缺失直接竞品/证据债务矩阵；
8. 三篇标杆论文写作架构；
9. 研究问题清单。

### 5.2 缺失直接竞品矩阵

至少列：Cheng 2020 `10.1016/J.OPTCOM.2020.126046`、Dong 2009 `10.1109/CHINACOM.2009.5339877`、Electronics 2021 `10.3390/electronics10232942`、`10.1364/OE.505931`、`10.1364/OE.448956`、Tang 2022、WiSEE 2024。字段：角色、当前证据层级、允许使用、禁止承重、潜在 Step 3.5 优先级。

只记录债务，不在本轮补件。当前 5 篇可满足 Step 3 数量门，但 C1/C2 主要来自 Wang 谱系；C3 只能约束 prior-art ceiling，C4 只能约束 transfer physics。

### 5.3 写作架构（固定 3 篇）

对 L01 Wang 2023、L02 Enhanced 2024、L04 Paillier 2020 提取：

- 三级标题结构、核心章节比例；
- System Model / Problem Formulation / Algorithm/Receiver Design 组织；
- 参数与符号展示；
- 图表类型、数量与 caption 模式；
- baseline/消融/指标/复杂度的实验组织；
- Introduction 与结论叙述链；
- 公式引入/推导/编号模式；
- 共同引用但当前 GW 未覆盖的基础文献（只列为未来 Step 3.5 输入，不检索）。

经典段落摘录遵守最小引用原则，只摘必要短句并标位置；不得大段复制论文原文。

### 5.4 canonical 问题清单（唯一合法语义门）

每条候选必须使用模板字段：

| Q# | M（具体近期方法） | C（条件） | A（失效假设） | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 四判据 | 来源文献 | 证据状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|

四判据只能是：

1. **具体技术矛盾**：M/C/A 明确、句子级、可解；A 可以是文献支持且可证伪的 target inference，不要求已被 smoke/MVE 证明。
2. **有方法产出形态**：设计公式/准则/算法/框架/可复用曲线族；这里只写形态，不设计 RML-FSTS 实现。
3. **有近期 baseline 可对标**：本项目参数为 2019+ 顶刊；Wang 2023 可作为近期 M，Morelli 2009 只能作 prior art，不能单独满足近期门。
4. **能做可量化对标**：每章 1–2 个对象，写清指标/曲线对照；不要求本轮已有增益数字。

`证据状态` 是单独的 FACT/INFERENCE/UNKNOWN 标注，不是第五判据。尤其：

- `problem_truth` 不得作为判据 1 的别名；“A 尚待目标场景证伪”不能单独让判据 1 失败。
- `novelty` 不得进入四判据；竞品穷尽与 novelty closure 属 Step 3.5，headroom/cheap comparator 胜负/oracle/MVE 属 Step 4a。
- 论文自身解决的问题通过四判据，不等于本研究 target Q、新颖性或 Go。
- 可从全文事实形成候选，如以 Wang 2023 fixed-`BL` FSTS 为 M、以同 modulation/TS/receiver-power bin 下不同湍流/分支条件为 C、以 single-lag near-optimality 为待证伪 A；但必须按实际证据重建，不能因本任务示例而预判其 PASS。

### 5.5 Step 3 状态判定

只有全部满足才把 Step 3 标为 `✅ completed`：

- 5/5 title/identity/source-path preflight PASS；
- 5/5 全文完成标准字段、7 子表、通信参数；
- 五篇实验完备性 + 三篇写作架构完成；
- read-notes/read-log/literature owner/receipt 一致；
- 综合分析各节有实质内容；
- 至少 1 条 target-relevant Q# 通过 glossary canonical 四判据；
- independent verifier PASS，P0/P1/P2=`0/0/0`。

否则：

- title/path/身份或全文字段缺口 → Step 3 `BLOCKED/IN_PROGRESS`，返回 Step 2 修复或继续当前精读；
- 五篇事实提取完成但无 canonical Q# 全过 → Step 3 `BLOCKED/IN_PROGRESS`，只记录 `gw-search → gw-acquire → gw-read` 恢复路径；
- 不论哪种阻塞，都不计 research-object/method-package failure，不进入 Step 3.5，不自造 terminal。

---

## 6. Step 3 产出与治理同步

### 6.1 必须落盘

1. `projects/thesis-fso/literature_notes_rml_fsts.md`
2. 五篇 `papers/_read_notes/{paper_id}.md`
3. `projects/thesis-fso/read-log.md`
4. `search-archive/2026-08-09/rml-fsts-step3-read-receipt.json`
5. `.sessions/2026-08-08-rml-fsts-groundwork/R003-step3-fulltext-read.md`
6. 追加 `S002-step3-dispatch.md` 的 T001 执行结果
7. `decisions.md` D004：只记录实际 Step 3 completed 或 blocked 当前状态、canonical Q# 数量及下一框架动作；不得创造 terminal
8. `verifications.md` V002：fresh-context independent verifier 结果
9. `H002-step3-stop.md`：只交接 Step 3 状态与下一合法动作
10. 同步 `topic-index.md`、`.sessions/_registry.yaml`、`projects/thesis-fso/master-state.md`

Step 3 completed 时，literature owner 与 master-state 的 Step 3 均改为 `✅ completed`，Step 3.5 保持 `⬜ NOT_STARTED`。阻塞时两处都写 `BLOCKED/IN_PROGRESS` 和同一缺口。

### 6.2 R003 最低结构

```markdown
# [R003] RML-FSTS Step 3 全文精读

## 调研问题
## Source preflight
## 五篇事实矩阵
## Source/target defect 边界
## Baseline 与 prior-art ceiling
## 实验完备性/写作架构汇总
## Canonical Q# 结果
## Step 3 状态与理由
## 对决策的影响
```

### 6.3 H002 停止边界

- completed：下一合法动作仅为新对话执行 mandatory Step 3.5；本轮不得顺手执行。
- blocked by no Q：下一合法动作仅为按 glossary 回 `gw-search` 扩检索，须新授权/新任务。
- blocked by title/path/fulltext：下一合法动作仅为回 Step 2 修复最小全文输入。

H002 必须包含接收方验证清单、缺失直接竞品债务和 source/target 边界；不得写 smoke/实现任务。

---

## 7. 独立验证、git 与提交

### 7.1 fresh-context verifier

生产者完成后另派未参与生成的 verifier，逐项读取实际文件检查：

1. T001 scope：只有 Step 3，无 Step 3.5/4a/smoke/实现/仿真；
2. 五篇 title/DOI/path/SHA/bytes 与 Yu adapter receipt；
3. 5×标准字段、7 子表、通信参数完整；非DRL字段正确 N/A，无硬造 MDP；
4. 五篇实验完备性、三篇写作架构；
5. read-notes/read-log/literature owner 一致且无旧事实丢失；
6. source/target defect、C3 prior-art ceiling、C4 transfer physics 未偷换；
7. 缺失竞品未据摘要/标题承重；
8. Q# 表只含 glossary canonical 四判据，无 `problem_truth/novelty` 语义门；
9. 状态判定符合 §5.5，未自造 terminal；
10. literature/master/topic/registry/D004/H002 current view 一致；
11. object/package failure 仍为 `0/0`，Step 3.5+ 未授权；
12. `git diff --check`、YAML parse、JSON parse、staged=0（提交前）、p05 日志 hash/no-stage、禁区 diff 全 PASS。

verifier 输出 PASS/FAIL/PARTIAL + P0/P1/P2。允许一次最小修复；修复后由同一 verifier 复核。P0/P1 或状态承重 P2 未闭合时不得标 completed、不得提交完成态。

### 7.2 提交纪律

- 本执行对话只允许一次统一 commit，包含 Step 3 产出、治理同步与 V002；不 push。
- 不提交 API key/cookie/临时文件；四个 `p05_run*.log` 始终不暂存。
- 论文原始 `content.md/source.md/source.pdf` 继续 gitignored；Yu byte-identical adapter 不强制纳入 git，但 receipt 必须提交并足以复算。

---

## 8. 验收清单

- [ ] session start、D003/T001 scope、registry 依赖/conflict 已核对；
- [ ] 五篇 source preflight 全 PASS；Yu adapter byte-identical + title/DOI receipt 闭合；
- [ ] 五篇由 fresh-context reader 完整读取，不是摘要/旧笔记冒充；
- [ ] 每篇标准 14+ 字段、7 子表、通信参数完整；
- [ ] 非DRL字段 N/A 且理由明确；
- [ ] 五篇实验完备性、三篇写作架构完成；
- [ ] 五篇 read-notes 与 read-log 更新；
- [ ] 综合分析、缺失竞品矩阵、baseline 交叉验证完成；
- [ ] Q# 只用 canonical 四判据，无 problem_truth/novelty 门；
- [ ] 无 Q# 时保持 BLOCKED/IN_PROGRESS 并回 search，不自造 terminal；
- [ ] completed 时只标 Step 3 `✅ completed`，Step 3.5 保持 NOT_STARTED；
- [ ] 无 smoke/实现/仿真/MVE/Contract/Execute；failure=`0/0`；
- [ ] V002 独立 PASS，P0/P1/P2=`0/0/0`；
- [ ] 一次 commit、未 push、p05 logs 未修改未暂存。

---

## 9. 最终回复格式（只给五项）

1. 五篇 title/path/SHA preflight 与 Yu adapter 结果；
2. 五篇精读/read-notes/read-log、实验完备性与写作架构完成度；
3. canonical Q# 数量、逐条四判据结果与 Step 3 completed/blocked 状态；
4. 是否进入 Step 3.5/4a、是否运行 smoke/实现/仿真、failure 计数；
5. R003/D004/V002/H002、literature owner、receipt、verifier、commit SHA 与下一合法动作。

不要在五项之外追加方法建议或下游执行。
