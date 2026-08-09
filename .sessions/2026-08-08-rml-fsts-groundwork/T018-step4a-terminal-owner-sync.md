# Task Brief: RML-FSTS Step 4a terminal owner synchronization

> 来源: S004 / D009 / V006 / T015-T017 | 日期: 2026-08-09
> 目标: 将 pre-run validity/calibration hard blocker 同步为待独立终验的唯一 Step 4a terminal

## 任务

在 evidence worktree 内只做文档与 receipt 同步，不实现、不运行 estimator/performance grid、不进入 MVE。先完整读取 `session-governance` skill、D009-D010、V006、S004，以及五份 worker log：formula identity、testbed readiness、A0 independent、source calibration、physical transfer、Wang figure-axis recovery。然后将当前证据收敛为 D009 terminal 5：

`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`

终态在 fresh-context V007 通过前标为 `PENDING_INDEPENDENT_VERIFICATION`；不得写成已验证 PASS。

## 必须同步

1. `decisions.md` 新建 D011：记录唯一 terminal、三类 hard blocker、可恢复缺图与 hard blocker 的区别、Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`、B0/B1/B2/O1/C1 performance数字=`N/A (NOT_RUN)`；D010 保持 rejected。
2. `S004-step4a-feasibility.md`：追加 T015-T017 事实、iteration counter、terminal reducer 路径；明确没有 scientific raw rows、paired delta/CI 或 MVE，不把门控跳过写成实验完成。
3. `topic-index.md`、`literature_notes_rml_fsts.md`、`master-state.md`：同步 Step 4a terminal candidate 与禁止下游；保留 SSRN 6293357 全文债和 strongest cheap comparator 不变量。验证前专题仍保持 active/pending verification。
4. 将 rejected `projects/simulation/explore/rml-fsts-step4a/contract.json` 显式加 `status=REJECTED_PRE_RUN`、`terminal_authority=NONE`、V006 指针，保留为失败合同证据。
5. 新建 `projects/simulation/explore/rml-fsts-step4a/artifacts/step4a-terminal-receipt.json`：机器可读记录 terminal candidate、performance grid/MVE 均未运行、B0-B2/O1/C1 数字 N/A、blockers、source log 路径/哈希、禁止 claim 与 next reopen inputs。JSON 必须可解析。
6. 新建 worker log `projects/thesis-fso/worker-logs/step-4a-rml-fsts-terminal-sync.md`，列实际修改与自检。
7. 新建 `H006-step4a-inconclusive-testbed.md`，按 handoff 模板完整包含已完成边界、不要做什么、必读、接口变更、失败数据、已知债务、验证阈值、接收方验证、下一轮。V007 未完成的检查框保持未勾选。
8. 不更新 `verifications.md`（V007 由独立 verifier 写）；不把 registry 改 dormant/closed（由主控在 V007 PASS 后收尾）；不修改 `voice.md`（本轮用户约束已登记）。

## 科学语义

- `semantic smoke` performance grid 是在 validity/calibration 起飞门前被阻断，不是“跑了但无结果”。
- source-calibration log 的三个 hard blockers：structural action-before causality、Wang phase-screen/SMF 与 scalar-GG 非等价、dBm→离散噪声不可辨识；另有 B0 numeric calibration gate 不可执行。
- direct figure 403/缺坐标是 recoverable gap；即使恢复图也不能自动解决上述 hard blockers。
- diagnostic structural run 虽可运行，但必须 `TERMINAL_DISABLED`；本轮不运行，因为不能回答原 Q1，且用户禁止 repair chain。
- 不给 Kill/Resolved/Go，不增加 object/package failure 计数；terminal 是 Inconclusive。
- next legal action 只可为：取得 authors/source receiver+channel config，并显式定义 action-before protocol 后，经 scope-change 重开 Step 4a；否则保持 dormant。不得进入 Contract/Execute/论文写作。

## 机械边界

- 不提交、不 push、不暂存。
- 不修改四个 `p05_run*.log`。
- 结束前运行 JSON/YAML/Markdown reference、`git diff --check` 和 protected-log hash/status 自检；只在 worker log 报告证据。
