# Task Brief: Step 3.5 fresh-context canonical semantic verification

> 来源: S001 | 产出位置: `projects/thesis-fso/oversampled-sync-groundwork/step3-5-fresh-semantic-verifier-report.md`
> 日期: 2026-08-06
> 唯一文档: 执行方可读取 evidence worktree 全部 staged/unstaged 产物，但不得依赖主线口头总结

## 0. TL;DR（执行方先读）

你是 fresh-context verifier。必须逐字对照 canonical `stages/glossary.md` L22-31 与 AMC Groundwork D005，
验证 formal D006/D007、Q1/Q2 四判据、Step 3.5 竞争闭包与 terminal 的语义正确性；不能只查文档自洽。
写独立 verifier report，不改 canonical，不提交。

## 1. 必验语义层

1. D005 的具体错误是否确为“要求 A 已被正文/MVE 证实”，从而把 Step 4a problem-truth 前移；
2. Q1 M/C/A 是否明确、句子级、可解，判据 2/3/4 是否有真实证据，Q1=`STEP3_SURVIVOR` 是否成立；
3. Q2 判据 1 PASS、判据 3 FAIL 是否成立，是否存在跨论文拼接伪造 baseline；
4. V004 是否明确保留为错误本地解释一致性的历史，而非 canonical semantic PASS；
5. Step 3.5 是否满足矩阵、≥2源、双向引用链、收敛/≤3轮、新论文 acquire→read；
6. generic shared-preamble、sequential chain、true joint estimator 是否被正确区分；
7. strongest cheap comparator 是否正确关闭，且未伪称单篇 baseline；
8. collision/claim ceiling/terminal 是否与全文 blocker 一致，未称 novelty closure、Go、METHOD_SIGNAL。

## 2. 必验确定性层

- 起始 evidence HEAD=`6874249530928616c13aa5a6107bc55d08fae939`；当前 HEAD 未被提交前应仍相同。
- 解析所有本轮 search JSON、papers metadata/index；复算 3 篇新增全文行数/SHA/标题与 read-log/read-note。
- 核对 Round 1=6 JSON、Round 2=3 JSON、Sun forward/backward、JOCN/arXiv receipts。
- 核对 canonical current state：formal topic、registry、master、RDL control/mission log/decisions 无 stale-current。
- 核对无 Step 4a、代码、仿真、`common/`、`params.py`、旧结果、Skill 改动；四个 `p05_run*.log` SHA
  与历史前缀 `7843B048/735E4650/C76887C/95A1D184` 一致且未暂存。
- 核对 tracked `__pycache__` 等工具副作用已清理；`git diff --check` PASS；staging 为空。

## 3. 产出格式

```markdown
# Fresh semantic verifier report
## Canonical owner receipt
## D005→D006 semantic lineage
## Q1/Q2 four-criteria re-verdict
## Step 3.5 search/citation/acquisition verification
## Collision/comparator/terminal verification
## Deterministic artifact and protected-boundary checks
## Blockers
## Verdict: PASS/FAIL
```

每个结论必须给文件+行号/路径或命令原始计数。任何语义错误、stale current、丢失 artifact、越界或
保护路径变化都判 FAIL；不要替主线修复。

## 4. 验收

- [ ] 独立逐字读取 glossary L22-31 与 AMC D005，而非只读 D006 转述。
- [ ] 至少抽查三篇新增全文的 action evidence lines。
- [ ] semantic 与 deterministic 两层都给出 PASS/FAIL。
- [ ] 未修改 canonical、未提交。
