# Task Brief: C1 Step 4a A0/A′/A/B 预检 fresh verifier

> 来源: S001 / D009 / H002 | 产出位置: `projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 10
  action_class: FEASIBILITY_A0
  mission_checkpoint: CP010
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。独立审查中央报告 `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md` 是否忠实合成 step-085/086/087、是否逐项满足 Step 4a A0/A′/A/B、是否把所有未知与物理/信息边界保留为 fail-closed。

**产出**：写入 `projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`，给 `PASS/FAIL` 与 P0/P1/P2 计数。

**最高纪律**：

1. 只做 fresh-context verifier，不替主线程修文件，不降低门槛。
2. 不运行 web/search/download、代码实现、adapter、defect smoke、MVE 或任何科学实验。
3. `CONDITIONAL_PASS_TO_D0_DEFECT_SMOKE_ONLY` 不得被升级为 A0 PASS、Step 4a Go 或方法信号。
4. 受控 injected slip 不能替代合法 coherent-FSO 条件下的 natural occurrence；FSO turbulence 不得被写成已证明导致 discrete slip。
5. 不修改/暂存四个 `p05_run*.log`，不 commit/push；hard cap 15 分钟。

## 1. 背景

- Canonical Q1 已 4/4；Step 3.5 的 bounded-slice 结论仅为 `NO_EXACT_COMPLETE_CHAIN_CONFIRMED`。
- step-085 给出 Gray-16QAM 单永久 symmetry jump 的无编码解析 headroom、interleaver fail-closed 与 physical factorization ceiling。
- step-086 给出 P08-R2 实际 coded-chain mapping、receiver-visible evidence ceiling、truth-leak surfaces 与 6.50 日 BOM。
- step-087 给出 non-ML A0 §2–§6、先验/负面证据、90/95 B2 absorption rule。
- 当前 CP010/epoch10 仍禁止 defect smoke、adapter、MVE、实验与贡献声称。

## 2. 必审问题

1. A0 §0–§6 是否逐项有 evidence→status→fatal 条件；non-ML 是否正确改审 finite-search triviality，而非伪造 ML/MDP。
2. 理论式、16QAM rotation、384-symbol/CW 与 `{j,384+j,768+j,1152+j}` mapping 是否准确；是否明确仅为 uncoded structural headroom。
3. 是否严禁 coded FER/goodput/dB、自然 FSO occurrence、exact true boundary、symbol-local syndrome 等未证声称。
4. A′ 是否至少覆盖 primary performance、goodput、clean safety、decode/latency、pilot/coding overhead、localization，并只给条件性 claim。
5. A 是否同时面对 canonical B1 与增强 B2；B 是否分开 novelty/fesibility，并列出至少三项空白零假设。
6. B2 ladder 与 90/95 coverage 是否忠实：`max(PAPU-like,OFC2017-like,global retry)`；CSSC/CS-DC 只能 identity ceiling；O1 只作 Kill/headroom。
7. 两层 testbed 是否明确：natural occurrence 无注入；controlled diagnosis 可注入但不能回答 occurrence。
8. caller→callee truth boundary、P08 B1/B2 命名冲突、6.50 日 BOM 和 `>7D_BLOCKER` 条件是否完整。
9. D0.0–D0.6 是否足以把 occurrence、coded damage、recoverability、B2 absorption、observability、stability/safety/cost fail-closed；D0 是否仍未授权。
10. 检查所有关键 evidence pointer 对应文件真实存在；抽查至少 12 个可证伪事实声称回源。

## 3. 产出格式

```markdown
# Step 088 — C1 A0/A′/A/B fresh verifier

> control receipt / scope / no-experiment receipt

## 1. Verdict
PASS 或 FAIL；P0/P1/P2=x/y/z；一句话 disposition。

## 2. Requirement matrix
逐项列 A0 §0–§6、A′、A、B、physical、truth、B2、BOM、D0 contract：PASS/FAIL + evidence。

## 3. Fact spot-checks
至少 12 项，含公式、mapping、全文数字/ceiling、文件存在性。

## 4. Findings
P0/P1/P2；无则明确 0。每项给文件行号、为什么、所需修正。

## 5. Control disposition
只能是：维持 CP010 等待修复，或允许主控另立 D/V/CP 开放 D0；不得直接授权实验。

## 6. Protection receipt
p05 四 SHA、git staging、唯一写入文件、未运行禁止动作。
```

## 4. 验收

- [ ] fresh task-control validator 对 T042/CP010 PASS。
- [ ] 抽查至少 12 个事实，且非仅做文档一致性。
- [ ] 对 natural/injected occurrence、coded/uncoded、candidate ranking/true boundary 三组边界逐一给 verdict。
- [ ] P0/P1/P2 可复核，PASS 时均为 0。
- [ ] p05 SHA 4/4 与既有 receipt 一致；staging 为空；唯一写入 step-088。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`
