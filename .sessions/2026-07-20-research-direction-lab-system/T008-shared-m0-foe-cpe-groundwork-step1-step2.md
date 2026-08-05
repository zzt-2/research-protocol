# Task Brief: P1 Shared M0-Power FOE–CPE Groundwork Step 1–2

> 来源: S015 / D024 / CP005 | 产出位置: 新 Groundwork 专题 + `projects/thesis-fso/` 对应 owner
> 日期: 2026-08-05
> 唯一文档: 执行方只拿到本任务书与其中列出的仓库文件；不得依赖聊天摘要

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 16
  action_class: FORMAL_GROUNDWORK_PREPARATION
  mission_checkpoint: CP005
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在 worktree：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T007 已产生一个 design-only survivor：**Shared Raised-Power Compute Graph for NDA FOE+CPE**。
你的任务是在一个新 Groundwork 专题中，严格执行 **GW Step 1 检索 + Step 2 全文获取/覆盖面门**，
然后停止，把覆盖面交用户确认。

**最高纪律：**

1. 本轮不进 Step 3/3.5/4a，不实现、不仿真、不跑 MVE、不写论文 claim。
2. P1 只是工程设计候选，不是 METHOD_SIGNAL；不得预设它新颖、有效或能成章。
3. 廉价吸收只按实际实现/工具链判断；但文献中已有一遍 M 次幂联合 FOE–CPE 图可构成直接竞品。
4. 必须区分“显式共享减少真实调用”与“修改 NDA-ML 估计器统计”；后者触发既有
   `NDA_ML_BODY_REOPEN`，不属于本候选。
5. 只做 Step 1–2；Step 2 覆盖面报告必须等待用户确认，禁止自动进入 Step 3。
6. 细节全部落文件，最终聊天只回五项。单次统一 commit，不 push；四个既有 `p05_run*.log`
   不修改、不暂存。

## 1. 报到与权威事实

开始前必须完整读取：

1. `.agents/skills/research-direction-lab/SKILL.md` 及 `references/method-production.md`；
2. session-governance Skill；
3. `stages/groundwork.md`、`stages/gw-search.md`、`stages/gw-acquire.md`；
4. `stages/glossary.md`、`thesis-lessons.md` 速查表与 TL-22/TL-30/TL-31/TL-32/TL-33；
5. `.sessions/2026-07-20-research-direction-lab-system/topic-index.md` 的控制块、D024、CP005；
6. `projects/thesis-fso/direction-lab/harvest/ch5-concept-method-batch-001.md` 的 P1 卡；
7. 实际 caller：
   - `projects/simulation/simulator/sc_nda_ml_sim.py:137-166`
   - `projects/simulation/common/_recovery.py:171-273`
   - `projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py:24-32`
   - `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_branchrouted_30seed.py:138-165`
8. `.sessions/_registry.yaml`，确认无同方向 active/dormant formal Groundwork owner 后再新建专题。

运行 task-control validator；FAIL 立即停止为 `ENTRY_INVALID`。

## 2. 冻结研究对象

本轮冻结的问题假设只用于检索和获取，不作为 Step 3/4a 结论：

- **M**：当前串行 NDA carrier recovery 先用 M0 次幂做 FOE，再对 CFO 补偿信号重做 M0 次幂做 CPE。
- **C**：资源受限的软件或硬件实现，要求与当前 receiver 输出/BER 匹配。
- **A**：用一个共享 M0-domain 表示同时驱动 FOE 与 CPE；升幂域 CFO 去除必须使用
  `raised * exp(-j*M0*omega*k)`，最终在原信号域补偿 `omega*k + phi`。

当前已知事实只包括：现有 CPython/NumPy caller 有两次真实升幂；没有实际 CSE/JIT 证据。
以下均未知，必须由 Step 1–2 关闭或标 blocker：

- 传统 joint frequency/phase estimator 是否早已使用一次 Mth-power 序列；
- coherent optical/FSO 中是否有同数据流、同动作的直接实现；
- 共享图相对显式 conventional refactor 是否还有可区分工程 claim；
- 哪些论文能提供 operation count、latency、hardware/dataflow 或 matched-performance comparator。

## 3. Phase A — 新建正式 Groundwork owner

仅在 registry 查重确认后新建：

`.sessions/2026-08-05-shared-m0-foe-cpe-groundwork/`

至少包含 `topic-index.md`、`S001-groundwork-step1-step2.md`；产生方向/范围决策时写 D001，产生
验证结论时写 V001。专题原始目标冻结为：

> 判断共享 M0 次幂 FOE–CPE 计算图是否构成有文献空间、真实成本动作和可验证传统对手的
> Ch5 工程方法候选。

项目 owner 使用：

- `projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`（只先建 GW 进度和 Step 1–2 状态，
  本轮不得伪造 Step 3 精读条目）；
- `projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`；
- 必要时更新 `projects/thesis-fso/master-state.md` 的 GW Progress 与 foreground 指针。

## 4. Phase B — GW Step 1 检索

先复用 `search-archive/_index/all-papers.jsonl`、现有 carrier-sync/CPR 论文库和历史 search archive；
只有覆盖不足时才运行 `tools/search`。不得用主线程 WebSearch/WebReader。

至少覆盖三类语义，不得只搜题名同义词：

1. Mth-power / Viterbi–Viterbi / feedforward joint carrier frequency and phase estimation；
2. low-complexity、shared computation、common subexpression、joint FOE/CPE dataflow；
3. coherent optical/FSO/PSK/APSK/QAM 的 hardware-efficient carrier recovery 实现。

按 `gw-search.md` 满足：去重 ≥20、≥3 数据源、必读 ≥5、正式发表占比 ≥50%、至少两个技术路线；
完成初筛和二轮定向检索。大列表语义筛查或引用链由最多 3 个子 agent 分工，每个 ≤15 分钟；
主线程只接收结构化摘要。所有搜索 JSON 进入 `search-archive/2026-08-05/`。

Step 1 必须形成直接竞品初筛矩阵，至少含：论文、场景、是否一次生成 Mth-power 序列、FOE/CPE
是否共享、成本证据、与 P1 的关系、全文状态。此矩阵仍是 metadata/abstract 级，不得当精读结论。

## 5. Phase C — GW Step 2 获取与覆盖面门

按 `gw-acquire.md`：从必读/建议读中选 8–12 篇；先 `tools/download --dry-run`，再走最多三轮
合规获取；禁止 ResearchGate/Scholar/WebReader 全文抓取和绕过访问控制。已有合规全文直接复用，
但核对 metadata、标题与 DOI。每篇 `content.md` 必须 ≥50 行并做内容质量检查。

Step 2 只裁决**获取与转换质量**，不得阅读全文后判断方法数据流、共享方式、operation count 或
comparator；这些属于 Step 3 精读。合格全文只需同时满足：

1. Step 1 已按 metadata/abstract 列入必读或建议读；
2. 标题、作者、venue、DOI/arXiv 身份与下载对象一致；
3. `content.md` ≥50 行、正文非空、不是反爬/登录/目录页，公式表格损失已注明；
4. provenance 与 SHA256 可审计。

目标是 ≥5 篇身份和内容质量合格的高优先级全文；若不足，终态为
`STEP2_BLOCKED_BY_COVERAGE_GAP`。即使达到，也只能终止为
`STEP2_READY_FOR_USER_CONFIRMATION`，并列出所有高优先级获取失败项，不得自动进 Step 3。

将 acquisition/identity/SHA256/内容质量判定写入一个紧凑 receipt；不得在 receipt 或 coverage
report 中填写 method/dataflow/competitor 的全文语义结论。search raw cache 可 gitignore，receipt
和 coverage report 必须提交。为下一对话写一个紧凑 H001，明确 Step 3 仍未授权。

## 6. 禁止事项

- 不改 `.agents/skills/`、`projects/simulation/common/`、`params.py` 或既有算法；
- 不重开 P2–P5、T006 C3、P09、G1、AMC 或 dormant campaign；
- 不用 oracle/headroom 决定 Step 1–2 的 Go；
- 不把“没人题名相同”写成 novelty；不把一行实现或输出等价自动写成 rejection；
- 不创建实验合同、代码 sandbox、raw 仿真结果或论文图；
- 不宣布 `THESIS_METHOD_READY`、METHOD_SIGNAL、Go/Kill 或 active carrier。

## 7. 验收与提交

独立 fresh-context verifier 核查至少：

1. task-control 与 Step 1–2 边界；
2. registry 查重和新专题路径合法；
3. Step 1 数量/来源/正式发表/技术路线门槛；
4. direct-competitor 初筛没有把 abstract 当全文；
5. Step 2 每篇身份、路径、SHA256、≥50 行与内容质量判定，且无 Step 3 语义精读；
6. coverage terminal 唯一且未越过用户确认门；
7. `master-state` 与 `literature_notes` GW Progress 一致；
8. 无 Skill/common/params/实验/旧 campaign 污染；
9. `git diff --check`、YAML 解析和四个 p05 logs 未触碰。

本对话单次统一 commit，不 push。

## 8. 最终只回五项

1. Step 1 query/source/count、技术路线与初筛结论；
2. Step 2 合格全文清单、获取失败项与内容质量结论（不报全文方法结论）；
3. terminal：`STEP2_READY_FOR_USER_CONFIRMATION / STEP2_BLOCKED_BY_COVERAGE_GAP / ENTRY_INVALID`；
4. P1 当前仅能保持什么层级、哪些关键未知仍未关闭；
5. 文件路径、receipt、D/V/H、verifier、commit SHA 与下一合法动作。
