# Task Brief: Q15 Groundwork Step 3 精读（含两项收据前置修复）

> 来源: S002 / live D029 / formal D038
> 产出位置: `projects/thesis-fso/worker-logs/step-022-q15-step3-read.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只拿到本 T；可读取本文列出的仓库文件与论文全文

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 52
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP020
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T021 已获得 6 篇独立核心工作和 2 篇早期/长版全文，但把 Step 1
`source union=3` 写成 PASS 时缺少 IEEE 结构化 raw；5 篇 blit 全文也未进入
`papers/index.json`。这两项是有界收据债，不否定全文本身。

**你的任务**：

1. 先补 IEEE 第三源 raw 和 5 篇 blit 的 canonical paper/index 收据；
2. 前置修复通过后，在同一个任务内完成 Q15 Groundwork Step 3 精读；
3. 形成 direct-collision、cheap-alternative、M-C-A/Q# 和 Step 3.5 输入。

**最高纪律**：

1. 不运行仿真、seed、Probe/MVE，不改 T019/T020 代码或 artifact。
2. 不进入 Step 3.5/4a/Contract/Execute；不把 Step 3 当 formal Go。
3. D1/C1/C4 全文仍缺时，禁止声称 novelty、`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`
   或 Q15 已排除直接碰撞。
4. 全文精读必须分派给子 agent；主执行对话只接收结构化提取并集成。
5. D3′/D4′ 是 D3/D4 的早期/长版补充，不得按独立核心论文重复计数。
6. 不做第四轮 D1/C1/C4 下载；它们进入 Step 3.5 的 mandatory debt。
7. 只提交本任务授权的文档/索引变化，不 push，不更新 `.sessions` owner、
   mission-log、master-state 或 current YAML。

## 1. 必读与控制检查

按顺序读取：

1. `AGENTS.md`
2. `stages/groundwork.md`
3. `stages/gw-read.md`
4. `stages/glossary.md`
5. `domain-comms.md` §1、§1.1、§7
6. `templates.md` 的 literature_notes 与实验完备性模板
7. `thesis-lessons.md` 速查表、TL-30–TL-33
8. `.agents/skills/research-direction-lab/SKILL.md`
9. `.agents/skills/research-direction-lab/references/method-production.md`
10. `.agents/skills/research-direction-lab/references/baseline-adjudication.md`
11. `projects/thesis-fso/worker-logs/step-021-q15-groundwork-step1-2.md`
12. `projects/thesis-fso/search-archive/2026-07-28/q15-step1-candidate-map.md`
13. `projects/thesis-fso/literature_notes.md` 的 Q15 Step 1–2 pending 小节
14. `projects/thesis-fso/read-log.md`

启动：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T022-q15-step3-read-with-receipt-preflight.md
git status --short
```

validator 非 PASS 或起点不 clean，立即停止。

## 2. Phase A：收据前置修复

### A1. IEEE 第三源结构化 raw

使用 `python tools/blit.py`（不要 WebSearch/webReader）运行并保存至少两个 JSON：

```powershell
python tools/blit.py "radius directed multimodulus blind equalization QAM" `
  --source ieee --format json --max 20 `
  --output projects/thesis-fso/search-archive/2026-07-28/q15-ieee-radius-receipt.json

python tools/blit.py "dual polarization 16QAM blind equalization coherent" `
  --source ieee --format json --max 20 `
  --output projects/thesis-fso/search-archive/2026-07-28/q15-ieee-dualpol-receipt.json
```

要求：

- 至少一份非空，含可审计 title/document-id/venue 或等价字段；
- 在 worker log 重算 actual source union；
- `129` 仍只代表 S2+OpenAlex merged unique，不得把 IEEE hits 偷加进 129；
- 若两份均空，终态 `BLOCKED_STEP1_SOURCE_RECEIPT`，不进入 Phase B。

### A2. 五篇 blit 全文 canonical receipt

以下原文件不得移动或删除：

```text
papers/downloads/2026-07-28/9492010.{pdf,md,meta.json}
papers/downloads/2026-07-28/9333378.{pdf,md,meta.json}
papers/downloads/2026-07-28/1561206.{pdf,md,meta.json}
papers/downloads/2026-07-28/1493739.{pdf,md,meta.json}
papers/downloads/2026-07-28/10251763.{pdf,md,meta.json}
```

把它们复制为以下 canonical manual artifacts：

```text
papers/manual/ieee-9492010-likelihood-rde/{source.pdf,content.md,metadata.json}
papers/manual/ieee-9333378-blind-rde-likelihood/{source.pdf,content.md,metadata.json}
papers/manual/ieee-1561206-radius-adjusted-equalization/{source.pdf,content.md,metadata.json}
papers/manual/ieee-1493739-hybrid-blind-equalization/{source.pdf,content.md,metadata.json}
papers/manual/ieee-10251763-temporal-correlation-demux/{source.pdf,content.md,metadata.json}
```

metadata 至少含：expected_title、verified_title、IEEE document id、DOI（有则填）、
original_path、source=`ieee_blit`、source_pdf SHA256、title_check。

同步把 5 条 success receipt 追加/合并进 `papers/index.json`，不得覆盖既有条目。
逐篇核对 canonical `content.md >=50` 行、SHA 与原 PDF 相同。任一核心文件身份
不明则该论文 abort；可继续的独立核心论文少于 5 篇时终态
`BLOCKED_TITLE_OR_SOURCE_IDENTITY`，不做综合结论。

## 3. Phase B：Groundwork Step 3 精读

### B1. 阅读集合

六篇独立核心：

| ID | 角色 | expected title（派遣身份锚点） | canonical path |
|---|---|---|---|
| D2 | modified RDE direct collision | `Modified radius directed equaliser for high order QAM` | `papers/doi/10.1109_ecoc.2015.7341620/content.md` |
| D5 | distribution/K-means radius direct collision | `Optimized blind equalization for probabilistically shaped high-order QAM signals` | `papers/doi/10.3788_col202220.080601/content.md` |
| C2 | CMA divergence theory | `Adaptive filters: stable but divergent` | `papers/doi/10.1186_s13634-015-0289-8/content.md` |
| D4 | likelihood RDE direct collision | `Likelihood-Based Selection Radius Directed Equalizer With Time-Multiplexed Pilot Symbols for Probabilistically Shaped QAM` | `papers/manual/ieee-9492010-likelihood-rde/content.md` |
| D3 | radius-adjusted switching direct collision | `A Novel Radius-Adjusted Approach for Blind Adaptive Equalization` | `papers/manual/ieee-1561206-radius-adjusted-equalization/content.md` |
| C6 | temporal-correlation/pr-MMA cheap alternative | `Blind Polarization Demultiplexing of Shaped QAM Signals Assisted by Temporal Correlations` | `papers/manual/ieee-10251763-temporal-correlation-demux/content.md` |

两篇补充，不计独立核心数：

- D4′：expected title =
  `Blind Radius Directed Equalizer with Likelihood-based Selection for Probabilistically Shaped and High Order QAM`；
  path = `papers/manual/ieee-9333378-blind-rde-likelihood/content.md`
- D3′：expected title =
  `Hybrid Methods for Blind Adaptive Equalization: New Results and Comparisons`；
  path = `papers/manual/ieee-1493739-hybrid-blind-equalization/content.md`

### B2. 每篇强制提取

每篇先按下列协议做 title abort check，再读 method + experiment：

1. expected title 只能取 B1 表中的派遣身份锚点，不能由文件名或正文反推；
2. 若 metadata 的 verified title 与 expected title 明确指向不同论文，立即
   `ABORT_TITLE_MISMATCH`，不得写精读笔记；
3. 从正文第一个非导航 H1/H2 提取 observed title，按 `gw-read.md` Step 0
   规范化后计算 expected/observed token Jaccard：
   - `Jaccard >= 0.4`：身份检查通过，继续精读；
   - `Jaccard < 0.4`：立即 `ABORT_TITLE_MISMATCH`，不得写精读笔记；
   - 正文没有可解析标题：标 `title-unverifiable`，人工核对前 20 行与
     metadata；无法形成明确同一性证据仍须 abort。

通过身份检查后产出：

- `papers/_read_notes/{stable-paper-id}.md`
- `projects/thesis-fso/read-log.md` 一条
- `projects/thesis-fso/literature_notes.md` 的 Q15 Step 3 条目

每篇必须包含以下标准字段，不得仅以“已读 `gw-read.md`”代替：

1. expected title、observed title、title Jaccard、title-check verdict；
2. DOI/IEEE document id/其他来源标识、canonical 源路径；
3. 发表状态、venue、year；若为预印本，必须按 `gw-read.md` S2 工具核查
   是否已有正式版本并更新 venue/status，禁止用 WebReader；
4. 核心贡献（至少 2 句）；
5. 方法概述；
6. 实验设置；
7. Baselines、是否公平调参、指标；
8. 关键结论、数字与 conclusion scope；
9. 与 Q15 的关系：适配点、不适配点、可借鉴点；
10. 实现细节：关键公式/更新规则、参数、信道/失真模型及出处；
11. 适用场景与边界；
12. 论文自身的 problem extraction：M/C/A、A 的章节/公式定位、方法产出形态；
13. 开源代码：URL/仓库证据；未找到明确写 `not found`；
14. verification status：正文、元数据、正式版本和代码证据分别写
    `verified / partial / unverified`；
15. 实验完备性：claims、seeds/error bars、baseline matrix、ablation、
    channel realism、complexity、VVUQ。

此外，每篇笔记必须有以下七个独立结构化子表，不得埋在散文中：

1. state/observation space；
2. action/output space；
3. reward/objective/loss；
4. modeling assumptions；
5. network/algorithm architecture；
6. applicability boundary；
7. problem extraction（M/C/A + 四判据证据指针）。

非 ML 论文的 state/action/reward/network 字段仍须保留，明确写
`N/A（非学习方法）`并解释对应的 algorithm input/output/objective/structure，
不得编造学习结构。

选择 D3、D4、C6 做写作架构提取；选择 D2、D3、D4、D5、C6 做实验完备性
对标汇总。

### B3. Q15 综合分析

在 `literature_notes.md` 新增 Q15 Step 3 综合段，必须回答：

1. 按机制与作用点对六篇独立核心分类，区分 equalizer-internal switching、
   output remap、distribution-aware radius、temporal-correlation alternative
   和 divergence theory；再回答 D2/D3/D4/D5 是否与 Q15 同 action、同
   information boundary、同 problem；
2. 归纳现有方法的已知局限（不是“尚无人做”的空白），并逐条注明原文证据；
3. 给出最近 2–3 年的趋势；若样本不足以支持趋势，明确写
   `INSUFFICIENT_EVIDENCE`，不得从旧论文外推；
4. 给出背景时间线、核心挑战和 Q15 的研究定位，明确区分历史演进、当前
   comparator 与候选包装；
5. Q15 的 prefix-only、identity fallback、post-CMA frozen map 分别有没有真实
   信息增量，还是仅把 equalizer 内部 switching 搬到输出端；
6. C2/C6 以及各论文 baseline 是否表明 robust CMA/MMA/RDE 能更便宜地吸收问题；
7. 做 baseline 出现频次/任务匹配矩阵，给出当前传统 comparator 候选及理由；
8. 汇总 D3/D4/C6 的写作架构，并给出可复用的论文叙述骨架；
9. 汇总 D2/D3/D4/D5/C6 的实验完备性 benchmark；
10. 建立 Q15 problem table：暂定 M-C-A、方法产出形态、四判据、证据指针、
    反证与未决债务；判断能否形成 Q# 候选。不得因
   T020 有信号而自动 PASS；D1/C1/C4 未闭合时综合状态最高为
   `PENDING_STEP35`，不得写最终全过；
11. D1/C1/C4 缺失分别会改变哪项结论，生成 Step 3.5 mandatory query/citation
   targets。

### B4. 允许的终态

- `STEP3_CONTENT_COMPLETE_Q_PENDING_STEP35`：≥5 篇独立核心精读合格，
  综合分析完整，Q# 候选已形成；D1/C1/C4 使四判据最终状态、novelty 与
  cheap-alt closure 保持 pending，必须返回主控。
- `STEP3_PARTIAL_NO_Q_CANDIDATE`：精读完成但无法形成完整 M-C-A/Q# 候选；
  列出判据级缺口，交主控决定 Step 3.5 或轮换。
- `BLOCKED_STEP1_SOURCE_RECEIPT`
- `BLOCKED_TITLE_OR_SOURCE_IDENTITY`

无论何种终态：

- `mission_method_delta=NONE`；
- 不运行实验；
- 不进入 Step 3.5/4a；
- 不宣称论文方法、novelty 或 problem survives conventional baseline。

## 4. 交付与验证

必须写：

`projects/thesis-fso/worker-logs/step-022-q15-step3-read.md`

日志包含：

- Phase A 原始命令、source-union 重算、index/canonical receipt 表；
- 逐篇 title/hash/line/read-note receipt；
- 六篇核心 + 两篇补充完成矩阵；
- direct collision 与 cheap-alt 矩阵；
- Q15 Q# 四判据表；
- D1/C1/C4 Step 3.5 debt；
- changed files、验证命令、commit SHA。

验证：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T022-q15-step3-read-with-receipt-preflight.md
python -m json.tool papers/index.json > $null
git diff --check
```

只提交任务授权的 `literature_notes.md`、`read-log.md`、worker log，以及允许
提交的索引/结构化笔记；ignored search/papers artifacts 保留在 worktree。不得 push。

最终只回传：

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
