# Fresh semantic verifier report

> 2026-08-06 | fresh-context verification | 起始/当前 HEAD：`6874249530928616c13aa5a6107bc55d08fae939`
>
> initial semantic layer：`FAIL`（canonical literature notes 有 2 处未标历史的 stale-current）
> deterministic layer：`PASS`

## Canonical owner receipt

- `stages/glossary.md` SHA256=`eafa43e3b0c941d90b36e4469e28346621ee82ee83d6fed558410073f610e74b`。
  L22-31 逐字定义四判据：L28 只要求 M/C/A 明确、句子级、可解；L29 要求可复用的方法产出形态；
  L30 要求近期 baseline；L31 要求可量化对标。L28 没有“A 已由正文、实验或 MVE 证实”的要求。
- `.sessions/2026-08-02-fso-amc-groundwork/decisions.md` SHA256=
  `5e5cfb5e64e4d17d72ff5d83e6d3f53a09afc0796979b4e975f4a25cfb9a6f54`。AMC D005 L143-195
  逐字说明：旧 `problem_truth/actionability/novelty/thesis_fit` 不是 canonical owner；L169-177 将
  “A 的失效已证明”识别为把 Step 4a/MVE 与 Step 3.5 责任前移；L179 明确旧 V005 只验证本地合同自洽，
  不构成 canonical semantic PASS。
- formal `decisions.md` SHA256=`d12b9d31b8ea9468273c9b67c4b953d7c553cf7377fc3b750a7f72ff37f1a725`。
  本报告独立读取上述两个 owner 后再核对 formal D005-D007，没有把 formal 自身转述当作 owner。

## D005→D006 semantic lineage

- formal D005 L169-171 的具体错误确是：以“CORE 没有证明该链在目标 C 下因具体 A 失效”为 Q1 判据 1
  FAIL，并对 Q2 同样要求共同失锁/cheap comparator 不足已获正文证明；这把 problem-truth 前移到了
  Step 3。
- formal D006 L199-203 只取代 D005 的 terminal 与 Q1/Q2 判据 1，改为“Step 3 要求 A 可证伪，不要求
  A 已被实验/MVE 证实”；L212-219 保留 7 CORE、动作边界、全文 blocker、最强廉价 comparator 与禁止
  Step 4a/实现/仿真的事实。该取代范围与 glossary L28 及 AMC D005 L169-177 一致。
- formal V004 `verifications.md:39-42` 已明确降级为历史：文件/身份/字段/保护边界验证继续有效，但其 Q1/Q2
  判据 1 与 terminal 只代表错误本地合同自洽，不能作为 canonical semantic PASS。处置正确。
- semantic lineage 本身：`PASS`。

## Q1/Q2 four-criteria re-verdict

### Q1

- 判据 1 `PASS`：`step3-deep-read-report.md:25-27` 给出句子级 M/C/A——M 是 Le Bidan 2-sps
  sequential chain 加 Sun/Wang frame-FOE comparator；C 是 RRC、至少 2 sps、fractional timing/frame/CFO
  同时未知；A 是 timing-first 独立恢复假设可能因其余未知量而失效。三要素明确、可解、A 可证伪。
- 判据 2 `PASS`：同报告 `:34` 把产出限制为可复用的 coupled likelihood/metric、coarse-to-fine
  estimator 或 design rule；明确排除仅共享 preamble/调序。
- 判据 3 `PASS`：同报告 `:35` 与 literature notes `:24-30` 给出 2019+ task-matched identity：Le Bidan
  2023 完整 2-sps 顺序前端、Sun 2025 JLT clock/frame/FOE burst chain、Wang 2023/2024 FSO frame+FOE。
  Step 3.5 新增 Zhou 2025 JLT 又把完整 SPO/frame/CFO 顺序 comparator 具体化，但没有被伪称为三参数
  joint estimator。
- 判据 4 `PASS`：同报告 `:36` 冻结 acquisition success、frame miss/false lock、timing/CFO error、BER、
  overhead、latency、complexity 等同输入可比指标。
- 结论：Q1=`STEP3_SURVIVOR` 成立；这只说明问题候选四判据成立，不证明 A、Go、METHOD_SIGNAL 或
  novelty closure。

### Q2

- 判据 1 `PASS`：`step-3-5-q2-baseline.md:9-15` 的 M/C/A 明确到独立 timing/carrier maintenance 与
  reacquisition、RRC≥2-sps+SCO/PN/CFO+dynamic fade、双环共同/异步失锁及 cheap shared-freeze/
  fixed-restart 可能不足；可解且可证伪。
- 判据 2/4 `PASS`：shared-confidence FSM/lock rule 是可复用产出；timing/SCO/CFO/CPE error、slip、BER、
  lock-loss 与 recovery time 可量化（`step3-deep-read-report.md:56,58`）。
- 判据 3 `FAIL`（当前证据范围内）：三份 Q2 JSON 原始结果为 `41/2/0`。41 篇列表中的近邻分别是 timing
  only、carrier only、joint acquisition、equalization+timing 或非相干 CDR/frame；没有一篇 2019+
  published receiver 同时提供 coherent timing+carrier continuous maintenance 与 loss-of-lock
  reacquisition 的合法同输出 baseline。`step-3-5-q2-baseline.md:35-54` 明确禁止把 Gu+Paillier+Valjus
  跨论文拼成一篇/一套已发表 integrated baseline，且把结论限制为当前检索池，不声称全领域不存在。
- 结论：Q2 仅判据 3 FAIL，非 survivor；没有发现跨论文拼接伪造 baseline。

## Step 3.5 search/citation/acquisition verification

- 关键词矩阵：`gw-supplement.md` 要求方法变体≥3、每种至少两个组合。T005 实际为 3×2、6/6 query；
  六个 JSON 逐个 parse 且 `declared total == results length`，原始行数
  `31+20+13+2+14+20=100`，按 DOI→arXiv→规范化标题跨 query 去重为 `80`。实际归档结果覆盖
  Semantic Scholar 与 OpenAlex 两源；满足≥2源。
- Round 2：三个冻结 JSON 逐个 parse，原始行数 `20+4+3=27`，跨 query unique=`25`；相对 Round 1、
  43 条引用链与已读 guard，真正新增 must=`0`、should=`0`。因此最后一轮新增=0，未启动 Round 3，
  满足收敛且轮数≤3。
- 双向引用链：Sun 2025 forward=`8`（OpenAlex 8/8，兼有 S2 4/8，S2-only=0），backward=`35`
  （OpenAlex 35/35）；两个 JSON unique 分别为 8/35。SHA256 分别为
  `95e8e3bed747256c68c3f174d3f60a610cc3730e39020445307a2623fcba6f80` 与
  `eb7cd674ce0a9183198918f559996e0fd1c927e672bb86ff055b7ba9d3167792`。
- arXiv receipts：JOCN 587273=`0`（SHA `ac62af...32651`）、Zhou 3528909=`1`
  （`904115...a3b8e`）、OE 566136=`0`（`892454...973f`）、JOCN 402591=`0`
  （`38ee5c...9362`）。JOCN 587273 metadata 为 `failed/all_failed/content_file=""`，SHA
  `2351ea1d...56f51`。
- 本轮 17:50 后落盘 search JSON 共 `37/37` parse PASS（包括 primary outputs 与工具自动 slug 副本）；
  primary 数量为 Q2 `3` + Sun citation `2` + R1 `6` + arXiv exact `4` + R2 `3`。
- papers metadata `9/9` parse；`papers/index.json` parse PASS，51 entries，九个本轮相关 identity 全存在，
  状态为全文成功 `3`、有界获取失败 `6`。

### 三篇新增全文独立抽查

| 论文 | 标题证据 | 行数 / content SHA256 | action evidence 与裁决 |
|---|---|---|---|
| Zhou 2025 / arXiv `2410.10080v1` | `content.md:19` | `555` / `a767b560ec27750edbb1f52412a92004ce72ae1ca153fba6bbb9bb2f89c3ffe5` | `:107-114` 明确 burst detect/coarse CFO 后再 SPO/fine FOE/frame；`:197-228` 的 fine CFO 与 frame 是不同 metric，故为 partitioned-preamble sequential chain，不是三参数 single objective。 |
| LPT 2017 / arXiv `1801.01598` | `content.md:3` | `156` / `5e4d78323b260421fe15f22a7e62b230b324eb138c737611832aad23ced9aae7` | `:37-83` 两个 FRFT peaks 经 2×2 coupling 解 integer frame+CFO；`:95-99` 入口已 1 sps，无 fractional τ，是真 joint strong neighbor 而非 exact collision。 |
| Du JLT 2021 / DOI `10.1109/JLT.2020.3042546` | `content.md:5` | `712` / `6a0c5a20b0cd8b86d365444133d66245ddc6cffe176f4470f4c761c244b84731` | `:65-73,115-125` 为 CP-removed OFDM symbol 上 joint `(τ,CFO,CPO)` likelihood；`:289-293` 明确 τ 为 integer，且无 frame output；占 generic joint prior，不是同任务 exact collision。 |

三份 read note 均存在（行数 `110/61/46`）；read-log 有三条对应行：`:57`、`:82`、`:83`。

## Collision/comparator/terminal verification

- generic shared-preamble/resource reuse、sequential modular chain、true joint estimator 的分类依据是
  information/objective/output/order，不以标题中的 `joint` 或共享训练资源代替 estimator-level jointness。
  Zhou 为 sequential；LPT 为 joint integer frame+CFO；Du 为 joint integer TO+CFO+CPO。分类与正文一致。
- Q1 strongest cheap comparator 已冻结为 polyphase/Farrow fractional-delay bank + Zhou/Le Bidan/Sun/
  FSTS/STSB sequential chain；`step3-5-supplement-report.md:61-62` 明确该 composite 是公平对照合同，
  不是某一篇论文的虚构 baseline identity，也没有声称它已证明 A 真假。closure 语义正确。
- 当前全文池没有确认同信息、同动作、同任务的 `(frame index, fractional τ, CFO)` exact collision；但
  JOCN 2026 `10.1364/JOCN.587273` 与 JLT 2025 IQ-skew `10.1109/JLT.2025.3581618` 都无全文，摘要不能
  裁单一 objective/fractional τ。因此 claim ceiling 只能到“Q1 survivor + 当前全文池未确认 collision”，
  不能到 novelty closure、Go、METHOD_SIGNAL 或方法成立。
- D007 terminal=`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED` 与两个全文 blocker 一致；
  topic-index、registry、master-state、RDL D031/CP013 当前投影一致，均禁止 Step 4a/实现/仿真。

## Deterministic artifact and protected-boundary checks

- HEAD=`6874249530928616c13aa5a6107bc55d08fae939`；staging=`0`；写本报告前 status=`36`
  （tracked modified `15` + untracked `21`）；`git diff --check` exit=`0`。
- Round/search/citation 原始计数：R1 JSON=`6`、rows=`100`、unique=`80`；R2 JSON=`3`、rows=`27`、
  unique=`25`；Q2 JSON rows=`41/2/0`；Sun=`8/35`；recent JSON parse=`37/37`。
- 全文：`3/3` title identity、content SHA 与行数匹配；read-note=`3/3`；read-log row=`3/3`；papers
  metadata=`9/9`；papers index related entry=`9/9`。
- 四个 protected logs 仍为未暂存的既存 untracked paths，完整 SHA256 为：
  - `p05_run.log`: `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`: `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`: `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`: `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
- `common/`/`params.py` status matches=`0`；Step 4a/code/Skill status matches=`0`；simulation status 除四个
  protected logs=`0`；`__pycache__`/`.pyc` status matches=`0`。仓库 HEAD 本来跟踪 10 个 pyc，但本轮没有
  修改/新增这些 tracked side effects。
- 未发现 Step 4a、代码、仿真、旧结果或 Skill 改动；本 verifier 未改 canonical、未提交。

## Blockers

1. **P0 stale-current：`projects/thesis-fso/literature_notes_oversampled_sync.md:7-8`。** 文件头已声明
   Step 3.5 完成，但边界段仍以当前语气写“当前仍不声称问题四判据已经闭合；只有至少一个 Q# 全过才进入
   Step 3.5”。Q1 当前已四判据 PASS 且 Step 3.5 已完成；该文字没有历史/superseded 标记。
2. **P0 stale-current：同文件 `:110`。** 仍写“JOCN 2026 全文缺失……不改变本轮更上游的四判据
   FAIL”，与同文件 `:128-129,153-155`、formal D006/D007 及当前 terminal 的 Q1 四判据 PASS 直接冲突，
   同样未标历史。

以上两处属于一个 canonical artifact 的当前语义投影未原子收敛。按 T012“任何 semantic error 或
stale current 均判 FAIL”，即使其余 semantic lineage 与 deterministic artifact 全部通过，最终仍必须 FAIL。

## Verdict: FAIL

- semantic：`FAIL`（2 处 stale-current，1 个 artifact/root cause）。
- deterministic：`PASS`。
- blockers：`2` 条文本位置；不得由 verifier 代修。

## Re-verification after bounded canonical repair

> 2026-08-06 | fresh full rerun | 本节取代上方初始 FAIL；初始审计保留为修复前历史证据

### Repair receipt and complete semantic re-verdict

- canonical 仅修复了先前报告指出的两处 stale-current：
  `literature_notes_oversampled_sync.md:7-9` 现明确 D006 的 Q1 四判据 PASS、Q2 仅 criterion 3 FAIL，且
  D007 已完成 Step 3.5；`:108-111` 现明确“尚未证明 A”属于 Step 4a，而非 criterion 1 FAIL，并且
  JOCN 全文 blocker 不改变 Q1 四判据 PASS。修复后该文件 SHA256 为
  `4c4de367fb87d3e2fefab9a0339d0074a716752f221723b06bea89a057d03fbb`。
- 重新从 canonical owner 验证语义，不以产物自洽替代规范：`stages/glossary.md:22-31` 仍定义问题句
  必须显式包含 M/C/A，且四判据分别审查具体性、已报道不足、可解性和价值；其 SHA256 为
  `eafa43e54153e63b0c8422557239943dbb8f3d9071c770c68866ec9d4b10e74b`。
- AMC Groundwork D005 仍明确裁定旧 `problem_truth/actionability/novelty/thesis_fit` gate 无效，且把
  “A 已被证明”前置到 Step 3 是错误；其 SHA256 为
  `5e5cfbc4934e4f2cc9b347189933825d601009c349642049ed4799ff909a6f54`。formal D005 的旧误判由 D006
  显式取代；formal decisions SHA256 为
  `d12b9d9ffef18f9760834c92f0df93d4a24d29ec3048bc4194c3789553d1a725`。
- D006 的当前裁决完整复核为：Q1 criteria 1/2/3/4 全 PASS；Q2 criteria 1/2/4 PASS、criterion 3
  FAIL。Q1 的 M/C/A 句法和文献证据满足 glossary；Q2 的失败点是 bounded evidence 未证明存在一个
  可实现的单一已发表 baseline，而不是把 Gu、Paillier、Valjus 拼成虚构 baseline。
- V004 仍只记录修复前的 local-self-consistency PASS，并已显式标为历史，不构成 canonical semantic
  PASS。D007 仍保持 generic joint、sequential modular chain、true joint estimator 三类边界，保留
  两个 exact-action 全文 blocker，并禁止将 composite comparator 冒充单篇已发表 baseline。
- 重新扫描 formal topic、RDL topic、master-state、literature notes 与本报告中的旧状态命中：V004
  有历史标识；H001 明示 `SUPERSEDED`；formal D005 与 RDL D029 均有 superseded 血缘；T001-T004、
  S001、CP010/CP011、voice.md 属不可变任务快照或按时间排列的历史记录，且其后均有当前 owner/
  checkpoint。没有发现新的、未标历史的 stale-current。
- D007 terminal 仍为
  `STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`；topic-index、registry、master-state、
  RDL D031/CP013 当前投影一致。claim ceiling 仍仅到 Q1 survivor 与“当前全文池未确认 exact
  collision”，不升级到 novelty closure、Step 4a Go、METHOD_SIGNAL、实现或仿真。

### Fresh deterministic evidence

- HEAD=`6874249530928616c13aa5a6107bc55d08fae939`；staging=`0`；复验时 status=`37`
  （tracked modified=`15`、untracked=`22`）；`git diff --check` exit=`0`。
- Round 1=`6 JSON / 100 rows / 80 cross-query unique`，各 query 原始行数
  `31/20/13/2/14/20`；Round 2=`3 JSON / 27 rows / 25 cross-query unique`，各 query 原始行数
  `20/4/3`，新增 must=`0`、should=`0`；Q2 三份 JSON rows=`41/2/0`。
- Sun citation forward=`8`、backward=`35`；SHA256 分别为
  `95e8e3bed747256c68c3f174d3f60a610cc3730e39020445307a2623fcba6f80` 与
  `eb7cd674ce0a9183198918f559996e0fd1c927e672bb86ff055b7ba9d3167792`。17:50 后 search JSON
  parse=`37/37`。
- papers metadata parse=`9/9`，其中全文成功=`3`、有界失败=`6`；`papers/index.json` parse PASS，
  entries=`51`，相关 identity=`9/9`。
- 三篇新增全文重新核验：Zhou=`555` lines、SHA
  `a767b560ec27750edbb1f52412a92004ce72ae1ca153fba6bbb9bb2f89c3ffe5`；LPT=`156` lines、SHA
  `5e4d78323b260421fe15f22a7e62b230b324eb138c737611832aad23ced9aae7`；Du=`712` lines、SHA
  `6a0c5a20b0cd8b86d365444133d66245ddc6cffe176f4470f4c761c244b84731`。read-note=`3/3`，
  read-log row=`3/3`。
- registry YAML parse PASS。四个 protected log SHA256 与初验完全一致：
  `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`、
  `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`、
  `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`、
  `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`。
- status 边界计数：`__pycache__/.pyc=0`，`common/params=0`，Step 4a/code/Skill=`0`，simulation
  除四个 protected logs=`0`。本 verifier 未改 canonical、未暂存、未提交。

### Re-verification verdict: PASS

- semantic：`PASS`。
- deterministic：`PASS`。
- blockers：`0`。
- 本节结论取代上方修复前的初始 FAIL；两处 bounded canonical repair 已消除唯一 root cause，完整复验未发现
  其他未标历史的 stale-current。

## Post-closeout narrow re-verification

> 2026-08-06 | post-closeout current-state audit | canonical 只读，唯一写入为本报告追加

### Initial findings and bounded repairs

- 初检发现 formal `S001-step1-step2-execution.md:3` 顶部状态仍写“Step 3 无 survivor”，与该文件后续
  D006/D007 收口记录冲突；主控仅将该行改为
  `完成（D007/V005：Q1 survivor；Step 3.5 fulltext-blocked terminal；专题 closed）`。
- 初检发现 RDL `topic-index.md:29` 顶层 `last_updated` 仍写 CP013，而 foreground control、mission log
  和 registry 已为 CP014；主控仅将该行改为
  `CP014/D031：formal V005 PASS并关闭，等待全文覆盖决定`。
- verifier 未修改上述 canonical 文件。两处修复后从当前工作树完整重读并重新执行以下验收；旧 D005/V004、
  S001 的按时间排列历史正文与 CP013 checkpoint 保留，不被误当 current state。

### Current-state consistency

- formal `topic-index.md:3` 与 `_registry.yaml:48-53` 均为 `closed`；topic index、V005、H002、S001 顶部及
  收口段、`master-state.md:8,30-52` 一致指向 D007/V005/H002、Q1 唯一 survivor、Q2 仅判据 3 FAIL、
  terminal=`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`，以及两个 primary-fulltext
  blockers。当前均不开放 Step 4a、实现、testbed、MVE 或仿真。
- RDL foreground control 为 epoch=`27`、mission checkpoint=`CP014`、authority=`formal D007`；
  `mission-log.md:208-222` 的 CP014、`decisions.md:1076-1110` 的 active D031、RDL
  `topic-index.md:29,299-303` 与 `_registry.yaml:29-34` 一致。RDL topic 保持 active、formal topic 保持
  closed；两者 `conflicts_with=[]`。
- 对 terminal、Q1/Q2、blocker、旧 `STEP3_NO_VALID_PROBLEM`、CP013 的命中重新扫描：V004/D005、
  S001 中间段和 CP013 均有显式历史血缘或处于后续 current section/checkpoint 之前；修复后未发现新的
  未标历史 stale-current。

### Fresh deterministic evidence

- YAML parse=`2/2`：`.sessions/_registry.yaml` 与 RDL foreground-control block；control 解析值为
  epoch=`27`、checkpoint=`CP014`。JSON parse=`47/47`：recent search=`37`、metadata=`9`、
  `papers/index.json`=`1`；papers index entries=`51`。
- HEAD=`6874249530928616c13aa5a6107bc55d08fae939`；staging=`0`；status=`37`，其中 tracked
  modified=`15`、untracked=`22`。当前未暂存状态与本轮 evidence worktree 预期一致；状态路径只覆盖
  formal/RDL/project evidence、T005–T012/worker reports、既有 verifier report 与四个 protected logs。
- protected `p05_run*.log`=`4/4`，均未暂存；SHA256 仍为：
  `7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`、
  `735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`、
  `C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`、
  `95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`。
- status boundary：`common/params=0`、Step 4a/code/Skill=`0`、`__pycache__/.pyc=0`；
  `git diff --check` exit=`0`。

### Post-closeout verdict: PASS

- semantic/current-state：`PASS`。
- deterministic/protected-boundary：`PASS`。
- blockers：`0`。
- 两个初检 stale-current 已由主控作最小修复；post-closeout 最终状态可一致地保持 formal topic closed、
  RDL 等待用户全文覆盖决定，且不产生 Step 4a 或实现授权。
