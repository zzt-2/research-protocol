# Independent Reverification Report — Oversampled Coherent Sync Groundwork

> 日期：2026-08-06
> 基准：`0ac0119c4982b539c322b79773c563cafdbbd9a6`
> 模式：第二位 fresh-context verifier；未联网、未下载、未运行仿真；除本报告外未修改文件
> 总体裁决：**PARTIAL**

## 1. 首次 FAIL 修复复核

### Important 1 — 直接竞品角色：已修复

- JLT 2025 DOI `10.1109/JLT.2025.3533197` 与官方 arXiv `2409.14400` 的题名、作者和 DOI 映射在
  `papers/arxiv/2409.14400/metadata.json` 中一致；本地 `source.pdf` SHA256 为
  `601cbe1cbedffbe904551e64f19b5bf0259266c4d10d5b896bc8b846b4ecc443`，`content.md` SHA256 为
  `73b2623b7d39199e31c801694dc78bfbc36fe5726ed5f5e28aa172bb525ccc81`，均与 receipt 匹配。
  `content.md` 实测 466 行、52664 bytes，正文完整且不是拦截页。
- 正文 `:43-57` 显示 TS-A/Godard 先消除 sampling-phase offset，随后 TS-B 顺序执行 FS 与 FOE；
  `:135-183` 给出 received-sample frame metric 与 frame 后 FOE。它足以承担“最接近 clock/frame/FOE
  动作集合的直接竞品”角色 5，也证明“一个 burst preamble 支撑这些前端动作”的宽泛包装已被占用。
- 但 timing 使用 TS-A/Godard，FS/FOE 使用 TS-B，动作顺序且分区；全文未给出 SCO/ppm/drift
  estimator/controller。因此当前证据只支持 `NO_CONFIRMED_FULL_COLLISION`，修订没有误判
  sample-level fractional timing + frame + CFO 的 exact collision，也没有宣称新颖性成立。
- JOCN 2026 DOI `10.1364/JOCN.587273` 的本地 metadata 与 direct-competitor receipt 如实记录三条路径：
  DOI 自动获取失败、官方 arXiv 精确题名检索无匹配、Optica 官方页不可访问；没有伪造全文。
  该文保持 `UNRESOLVED_HIGH_RISK`，并在 D003、topic-index、mission-log、master-state、Step 2
  report/receipt 中列为用户必须确认的缺口；不得据摘要裁 exact collision 或新颖性。

### Important 2 — 控制面同步：部分修复，仍有一处不一致

RDL `topic-index.md` 已是 epoch 22 / CP009，authority 指向新专题 D003；`mission-log.md` CP009、
`master-state.md`、新专题 D003/topic-index/S001 和新专题 registry 条目均一致为“7 CORE 含 JLT 2025，
JOCN 缺口待用户确认，terminal=`STEP2_READY_FOR_USER_CONFIRMATION`”。

但 `.sessions/_registry.yaml:33-34` 的 RDL system 条目仍写“Step 2 覆盖核查中”及“当前只允许完成
Step 2 CORE 覆盖与用户确认”，与 RDL topic `:10-25,29`、mission CP009 `:128-142` 和 master-state
`:8,30-40` 的“Step 2 已就绪、仅待用户确认/替换文献”不同。首次 Important 2 已从 D027/CP008
推进到 CP009，但 registry 的当前态措辞尚未完全收口。

### Important 3 — 物理数字证据类型：已修复

`literature_notes_oversampled_sync.md:35-53` 已用统一表逐项给出“数值｜全文位置｜证据类型｜可用范围”：

- GEO 2023 的 56 GBaud、roll-off 0.1、2 sps、±30 ppm、±5 GHz、600 kHz 被标为设计要求/数值仿真；
- Valjus 2025 的 ±20 ppm 标为标准允许偏差，约 50 ppm 标为轨道条件推导，60–100 ppm 标为该文
  数值仿真/并行实现假设；
- Paillier 2020 的 100 MHz 标为固定残余 CFO 假设，1.4 ms、约 5 dB 标为 TURANDOT/AO+DPLL
  数值仿真内测得，1 ms/0.684/20° 标为给定链路模型与数值时序设置。

表内明确“仿真内测得不等于外场测量”且列出仍不可冻结的参数。抽查对应全文位置支持这些分类，未发现
把设计、推导或仿真值误写成外场测量。

### 两项 Minor：已修复

- S001 已改成“2026-08-06 11:45 的阶段快照”，随后明确记录 Step 2 首轮、V001 FAIL、补证与当前 terminal，
  不再把历史时点冒充当前态。
- `step2-acquisition-receipt.json` 已删除冲突的 `per_failed_paper_manual_path_count` 语义，明确区分首轮
  7 条项目工具路径、定向修复新增 4 条路径、总计 11 条；Gu/OE 各 1 条，JOCN 3 条，JLT 第二路径成功。

## 2. 八门复核

| 门控 | 裁决 | fresh evidence |
|---|---|---|
| Phase 0 authority reconciliation | **PASS** | D023 与 T004 commit `1140134e...` 支持 2A=`REJECT`：ordinary regional retune 已压过 online calibration，且 held-out 前 immutable gate FAIL；T005 commit `67970307...` 支持 2B=`SUPPORTING_ONLY`：single-branch scheduling 与 CCISP `method.tex:39-71` 的 select-before-execute 动作重复，Q(8,6) 仅保留 supporting 边界（360 shards、漏 459 次 stage-2、13 dB 不可表示）。inventory 的 grade/evidence/prohibited revival 与权威一致。 |
| 6 query / search count / SHA | **PASS** | 六文件逐一 SHA 匹配；raw/recent 分别为 `29/9`、`36/11`、`13/2`、`25/12`、`21/7`、`16/1`；跨文件复算 `140 raw / 130 unique / 42 recent raw / 39 recent unique`。source_api 为 Tavily 90、SerpAPI Scholar 35、OpenAlex 6、组合标签 9。 |
| 2019+ baseline、Q 预卡、BOM | **PASS（Step 1 预卡层）** | Q1/Q2 均含 M-C-A、recent baseline、deployable I-A-O、CCISP 独立性、cheap alternative、物理来源、testbed、工期、章节形态和否决条件；二者是 acquisition 与 maintenance/reacquisition 两种机制，不是场景换名。BOM 实测 16 项=`1 READY + 8 SMALL_ADAPTER + 7 NEW_INFRASTRUCTURE`，逐项和 18.5 人日；合并 11–14 日，Q1 5.5–7.5 日，Q2 7–9 日，工程风险没有被隐藏。 |
| Step 2 角色覆盖 | **PASS** | 当前 7 CORE 覆盖 coherent optical timing 入口、近期 frame+CFO/joint sync、SCO/fractional timing、FSO/卫星参数与最近直接竞品；JLT 2025 满足角色 5，JOCN 缺口显式进入用户确认门。 |
| Step 2 identity/provenance/hash/content | **PASS** | 七篇 content SHA 和行数全部复算匹配：`278/244/455/891/1582/873/466`；均 ≥50 行且有实质正文。四个现存 source 文件 SHA 也匹配：Tang PDF、Paillier tar.gz、GEO PDF、JLT arXiv PDF。 |
| 物理数字来源分类 | **PASS** | 标准/设计要求/推导/仿真/外场测量已逐项区分；当前没有把仿真曲线内测得写成外场测量，未冻结缺证参数。 |
| 阶段与保护边界 | **PASS** | base 后 tracked diff 仅 7 个治理/状态 Markdown/YAML；untracked 研究产物仅本专题 Markdown/JSON 与本报告，无 Python、Step 3、实现、MVE、仿真或结果文件；staging 为空。四个 `p05_run*.log` 仍未跟踪、未暂存，mtime 均为 2026-07-30，SHA 与 V001 记录一致。 |
| registry/topic/mission/master/D003 一致性 | **PARTIAL** | 核心 terminal、7 CORE、JOCN 缺口、allowed/forbidden actions 与下一动作一致；仅 RDL registry 的“Step 2 覆盖核查中/允许完成覆盖”措辞仍滞后于“Step 2 已就绪待确认”。 |

## 3. 结构验证

- JSON：六份 search archive + 三份 receipts，共 **9/9** 可解析。
- YAML：`.sessions/_registry.yaml` 与 inventory **2/2** 可解析；registry 58 个 slug、无重复。
- `git diff --check 0ac0119c...` 无错误；无暂存文件。
- 新专题具备 `topic-index.md`、S001、decisions、voice；D002 保留 superseded 历史，D003 active；未发现
  Step 3、代码或仿真越界。

## 4. 最终裁决与必须修复

**PARTIAL。** 首次 FAIL 的直接竞品、参数证据类型和两个 Minor 已闭合；Phase 0、检索统计、Q 预卡、BOM、
7 CORE identity/SHA/content、阶段边界均通过 fresh 复算。剩余问题只在一个权威入口的当前态措辞。

必须修复后方可判 PASS：

1. 将 `.sessions/_registry.yaml` 中 `2026-07-20-research-direction-lab-system` 的 `last_updated` 与
   `description` 从“Step 2 覆盖核查中/允许完成覆盖”同步为“D003 后 Step 2 已核验 7 CORE，等待用户确认
   JOCN 2026 缺口或补充/替换文献”；不得改变 CP009、terminal 或扩大到 Step 3。
