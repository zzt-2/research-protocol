# Task Brief: Q15 prefix-gated shell calibration — Groundwork Step 1–2

> 来源: S002 / D028 / formal D037
> 产出位置: `projects/thesis-fso/worker-logs/step-021-q15-groundwork-step1-2.md`
> 日期: 2026-07-28
> 唯一文档: 执行方只拿到本 T；可读取本文明确列出的仓库文件和 artifacts

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md
  control_epoch: 51
  action_class: CANDIDATE_FORMALIZATION
  mission_checkpoint: CP019
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在：

`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`

T020 得到一个严格因果的诊断 winner：固定 `μ=0.03` CMA 后，用 128-symbol
prefix 决定 identity 或 public-16QAM quantile-shell radius transport。它在
20 个 test seeds 中只帮助 7 个、其余 13 个 seed-level tie，主要修复 CMA
collapse；它不是正式方法结论。

**你的任务**：只完成 Q15 的正式 Groundwork Step 1 检索与 Step 2 公共全文
获取/coverage-gap report，判断它是否与已有 blind equalization
normalization/radius-directed/restart 方法直接碰撞，以及问题是否可能被更廉价的
稳健 CMA/RDE/MMA/重启吸收。

**产出**：结构化检索 raw、公共全文（能合法获取的）、完整 coverage report 和
worker log。完成后必须暂停，等待主控验收。

**最高纪律**：

1. 不读论文全文、不写 Step 3 精读条目；只可用 title/abstract/metadata 做初筛。
2. 不跑任何仿真、seed、Probe/MVE；不改 T020 code/artifact，不补 gate receipt。
3. 不把 T020 signal 写成 Q15 四判据 PASS、novelty 或论文方法胜利。
4. 不执行或修改 Q14/T018；不进入 Step 3.5、Step 4a、Contract、Execute。
5. 论文全文只能用 `tools/download` / `tools/blit --download` / `tools/convert`
   获取；禁止 webReader/ResearchGate/搜索页面冒充全文。
6. 三轮下载止损后，失败项进入 coverage gap；不得绕过。
7. 只提交本任务授权的新/改文件，不 push；不更新 `.sessions` owner、
   mission-log、master-state、current YAML 或 formal decisions。

## 1. 必读与事实边界

开始前依次读取并遵守：

1. `AGENTS.md`
2. `stages/groundwork.md`
3. `stages/gw-search.md`
4. `stages/gw-acquire.md`
5. `stages/glossary.md`
6. `domain-comms.md`
7. `tools-guide.md`
8. `thesis-lessons.md` 速查表和最近 3 条
9. `.agents/skills/research-direction-lab/SKILL.md`
10. `.agents/skills/research-direction-lab/references/method-production.md`
11. `projects/thesis-fso/worker-logs/step-020-causal-constellation-prior-shell-family.md`
12. `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/method-map.v2.md`
13. `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/artifacts/result.v2.json`
14. `projects/thesis-fso/literature_notes.md`

启动时运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T021-q15-groundwork-step1-2.md
git status --short
```

validator 非 PASS 或 worktree 非 clean，立即返回
`BLOCKED_TASK_CONTROL` / `BLOCKED_DIRTY_WORKTREE`，不得继续。

### 1.1 只可继承的 T020 事实

- M4−baseline seed-cluster mean ΔPI-SER=`-0.0825893`，
  CI=`[-0.138115,-0.031779]`，help/hurt/tie=`7/0/13`；
- test 动作严格 prefix-only；
- 140 pairs 中 identity=102、M2=38、M3=0；
- 该证据 claim ceiling=`DIAGNOSTIC_ONLY_NOT_FORMAL_GW_MVE`；
- 当前未知：direct novelty、近期合法 baseline、robust CMA/restart 是否吸收问题、
  换 testbed 后是否存在。

不得继承“普遍均衡增益”“信道自适应”“inner-ring collapse 是信道性质”。

### 1.2 Q15 暂定问题假说（不是已过四判据的 Q#）

候选 M-C-A：

- M：固定参数 blind FIR CMA 及 always-on blind output calibration；
- C：dual-pol 16QAM 接收机在部分随机实现/初始化下产生低功率 shell collapse；
- A：传统方法缺少 receiver-visible 的 collapse detector 与安全 identity fallback，
  或其固定归一化无法区分健康和塌缩输出；
- 产出形态：prefix-gated identity/quantile-shell transport policy。

Step 1–2 必须检验这句话是否成立，不能以它为前提。

## 2. Phase A — Groundwork Step 1 检索

### 2.1 先做全仓去重

搜索 `projects/thesis-fso/literature_notes.md`、`papers/index.json`、
`search-archive/_index/all-papers.jsonl` 和既有 Q/C/B 候选，列出：

- 已有直接/相邻论文；
- C14 initialization、C15 cost、C11 CMA+DD、blind-affine 与 Q15 的边界；
- 明确已 Kill 的 exact construct，避免换名重做。

### 2.2 冻结四条检索线

每条至少 2 组 query，一轮 broad + 一轮定向，合计至少 8 个 query：

1. `blind equalization output normalization / automatic gain control / scale ambiguity`
2. `radius-directed / multimodulus / constellation shell / ring-based equalization`
3. `CMA local minima / singularity / inner-ring collapse / restart / multistart / reinitialization`
4. `distribution matching / quantile transport / histogram matching / post-equalization calibration`

必须同时包含 optical/coherent/dual-polarization/16QAM 与一般 digital
communications 两层词，防止只搜到单一场景。

使用项目工具，从仓库根运行；每条都显式 `--format json -o <path>`。raw 固定到：

```text
projects/thesis-fso/search-archive/2026-07-28/
  q15-*.json
```

不得使用主对话 WebSearch。若确需浏览器结果，必须由子 agent 消化并只把结构化
metadata 写入报告。

### 2.3 Step 1 质量门

合并去重后必须报告：

- actual source union；
- unique count、published ratio；
- 必读/建议读/待确认/备选/排除数量；
- 至少 2 个技术路线；
- direct collision candidates；
- cheap-alternative candidates；
- 每条候选的 title、year、venue、DOI/arXiv、abstract-supported relevance；
- 全仓既有 identity 命中。

目标门槛沿用 `gw-search.md`：unique≥20、source≥3、必读≥5、
published≥50%、至少 2 路线。任一不满足，按该文件规则补一轮；总计最多 3 轮。

如果 direct competitor 明确覆盖同一 action+information boundary+problem，
不要为了继续而降级措辞；仍完成 coverage map，然后状态可为
`BLOCKED_DIRECT_COLLISION`。

## 3. Phase B — Groundwork Step 2 公共全文获取

仅当 Step 1 数量/覆盖门通过时执行。

1. 从必读+建议读中选 8–12 篇，优先级：
   direct collision > robust/restart cheap alternative > radius/distribution mechanism >
   general background。
2. 先查 `D:\code\study\research-protocol\papers` 是否已存在合法
   `content.md + metadata.json`，存在则只记录路径/hash，不重下。
3. 新获取先 `tools/download --dry-run`，再按 `gw-acquire.md` 三轮止损。
4. 新 paper 写入共享权威根
   `D:\code\study\research-protocol\papers\{arxiv|doi|manual}\...`。不得覆盖或
   修改已有 paper artifact；遇到 shared repo dirty overlap 即暂停并报告。
5. 每篇检查 title identity、metadata 来源、`content.md` 有效行数≥50、
   SHA256。这里只做质量检查，不读 method/experiment 内容。

### 3.1 强制暂停门

完成获取后，在 worker log 写完整 `文献覆盖面状态`：

- 成功获取标题/ID/路径/hash；
- 内容不达标；
- 下载失败；
- source/venue/年份/正式发表覆盖；
- direct collision 覆盖；
- cheap alternative 覆盖；
- 哪些失败全文会改变判断；
- 建议 coverage gate：PASS / PARTIAL / FAIL，附事实理由。

然后返回 `AWAITING_DELEGATED_COVERAGE_GATE` 并停止。不得自行进入 Step 3。

## 4. 允许修改的文件

```text
projects/thesis-fso/search-archive/2026-07-28/q15-*.json
projects/thesis-fso/search-archive/2026-07-28/q15-step1-candidate-map.md
projects/thesis-fso/literature_notes.md
projects/thesis-fso/worker-logs/step-021-q15-groundwork-step1-2.md
```

共享 `papers/` 只允许新增合法 paper artifact；不修改既有文件。

`literature_notes.md` 只新增“Q15 Step 1–2 pending”小节：

- 记录检索/获取状态与证据指针；
- 四判据全部保持 UNKNOWN/NOT_ADJUDICATED；
- 不改全局 Step 3/3.5/4a 状态。

禁止修改：

- `.sessions/**`（worker log 除外；但 worker log 不在 `.sessions`）
- `projects/thesis-fso/master-state.md`
- `projects-overview.md`
- direction-lab current YAML/harvest/portfolio/state
- T020/T019/B01-R/C11 artifacts
- common/、params.py、simulator、任何实验代码

## 5. 验收与终态

必须运行：

```powershell
python .agents/skills/research-direction-lab/scripts/validate_task_control.py `
  .sessions/2026-07-23-research-direction-lab-longitudinal-test/T021-q15-groundwork-step1-2.md
git diff --check
git status --short
```

合法终态：

- `AWAITING_DELEGATED_COVERAGE_GATE`
- `BLOCKED_STEP1_COVERAGE`
- `BLOCKED_DIRECT_COLLISION`
- `BLOCKED_STEP2_FULLTEXT`
- `BLOCKED_SHARED_PAPERS_DIRTY`
- `BLOCKED_TASK_CONTROL`
- `BLOCKED_DIRTY_WORKTREE`

除 task/worktree preflight block 外，本包正常产生：

```text
mission_method_delta = NONE
```

这是 formal Groundwork 必经步骤，不得冒充新方法进展；CP019 已经记录本轮
METHOD_SIGNAL，本包的价值是决定该信号能否合法继续。

提交前确认：

- [ ] ≥8 query 且两轮检索完成，raw 路径可复现；
- [ ] Step 1 数量/来源/路线/正式发表门均有数字；
- [ ] direct collision 与 cheap alternative 分开；
- [ ] 若执行 Step 2，8–12 篇选择与每篇 title/path/hash/line count 可审计；
- [ ] coverage report 完整并停在 gate；
- [ ] 未读全文、未实验、未进入 Step 3+；
- [ ] 只提交授权路径，未 push。

## 6. 最终只回传

```text
status:
mission_method_delta:
commit:
worker_log:
one_line_result:
```
