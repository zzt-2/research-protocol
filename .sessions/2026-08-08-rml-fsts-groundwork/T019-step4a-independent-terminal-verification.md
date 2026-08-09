# Task Brief: RML-FSTS Step 4a fresh-context terminal verification

> 来源: D009-D011 / V006 / S004 / T011-T018 | 日期: 2026-08-09
> 产出: `projects/thesis-fso/worker-logs/step-4a-rml-fsts-independent-verifier.md`

## 任务

以 fresh context 对本轮 Step 4a scientific terminal 做独立只读终验。只允许写指定 verifier log；不得修文档、代码、合同或 artifact，不得运行 estimator/performance grid/MVE，不得提交或 push。先完整读取 `session-governance`、`sim-preflight`、`verification-before-completion` skills，并读下列证据：

- topic-index、S004、D008-D011、V005-V006、H005-H006；
- A0 preflight；T011-T018；全部 `step-4a-rml-fsts-*.md` worker logs；
- rejected contract 与 terminal receipt；
- literature owner、master-state；
- Wang canonical HTML 的公式/系统/结果相关局部与 shared 130981 action identity；
- git diff/status 与四个 protected p05 logs。

## 独立验证项

1. **恢复事实**：HEAD 起点、原 tracked/staged 状态、130981 shared fulltext/action、Q1 provisional-only、Step 4a 原未启动、B2 strongest cheap comparator 四项是否有证据。
2. **A0 完整性**：§0–§6、testbed readiness、Go/Kill 对手分离、部署信息边界是否齐全且未把 consistency 当 science。
3. **D010 失败语义**：确认 receiver-lag adapter 的 method-identity P0 与 source-calibration P0 在 grid 前触发；不存在 scientific raw rows、paired deltas/CI 或 result-driven repair。
4. **hard blocker 真伪**：独立核查 structural `(B_N,B_L)` 必须重建发端 FSTS；当前 receiver-power proxy 是否 action-after；Wang→scalar GG 的保真缺失；dBm→离散噪声是否不可唯一；B0 numeric gate是否不可执行。明确缺图是 recoverable gap，不单独充当 blocker。
5. **terminal 唯一性**：对照 D009 五个 terminal，解释为何只能是 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`，而不能是 no-crossover Kill、B2 Resolved、no-residual Kill 或 Go。
6. **baseline/数字语义**：B0/B1/B2/O1/C1 performance 数字、paired delta和CI必须为 `N/A (NOT_RUN)`，不得把源论文数字或公式 sanity 数字冒充本轮结果；C1未构造、MVE门控跳过。
7. **信息边界与公平性**：确认没有 truth SNR/true h/CFO/payload/label 驱动 deployable action；没有不公平 action search、同-rx伪 pairing或 lookup包装。
8. **owner一致性**：D/S/topic/literature/master/H/artifact/rejected contract 的 terminal、Q1 state、METHOD_SIGNAL、贡献层级、failure count、next legal action 一致。
9. **机械与保护**：JSON/YAML可解析，Markdown path可定位，`git diff --check`，四个 p05 logs内容/hash/status不变，未 push；报告 changed-file scope。
10. **问题分级**：给 P0/P1/P2 数量与逐项说明；最终只允许 `PASS / FAIL / PARTIAL`。任何 P0 或 terminal语义矛盾必须 FAIL。

## 验收格式

```markdown
# RML-FSTS Step 4a independent terminal verification
## Verdict
## Evidence replay
## Scientific semantics
## Information boundary and fairness
## Owner/artifact consistency
## Mechanical checks
## Findings (P0/P1/P2)
## Unique terminal and next legal action
```

所有断言给 `file:line` 或命令输出；不得用主控摘要替代文件证据。
