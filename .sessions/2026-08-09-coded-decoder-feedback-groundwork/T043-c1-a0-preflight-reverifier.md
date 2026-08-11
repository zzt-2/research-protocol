# Task Brief: C1 Step 4a A0 修订版 fresh re-verifier

> 来源: S001 / D009 / H002 / step-088 FAIL | 产出位置: `projects/thesis-fso/worker-logs/step-089-c1-a0-preflight-reverifier.md`
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

你在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。对中央报告 `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md` 做新的 fresh-context re-verification，重点确认 step-088 的两个 P1 是否被实质关闭，而不是只改措辞。

**产出**：只写 `projects/thesis-fso/worker-logs/step-089-c1-a0-preflight-reverifier.md`，给 `PASS/FAIL` 与 P0/P1/P2 计数。

**最高纪律**：

1. 只审查，不替主线程修中央报告、治理文件或代码；不降低门槛。
2. 不运行 web/search/download、仿真、defect smoke、adapter、MVE 或科学实验。
3. 当前仍是 CP010/epoch10；即使 PASS，也只能建议主控另立 D/V/CP，不能直接授权 D0。
4. natural occurrence 与 controlled injection 必须分离；FSO turbulence 不得被写成已证实导致 discrete slip。
5. 不修改/暂存四个 `p05_run*.log`，不 commit/push；hard cap 15 分钟。

## 1. 必读与 lineage

1. `stages/gw-feasibility.md` 的 Step 4a A0/A′/A/B 与 3–7 日边界。
2. 中央报告 `step4a-a0-preflight.md`。
3. `projects/thesis-fso/worker-logs/step-085-c1-a0-theory-headroom.md`。
4. `projects/thesis-fso/worker-logs/step-086-c1-a0-coded-chain-bom.md`。
5. `projects/thesis-fso/worker-logs/step-087-c1-a0-prior-negative-evidence.md`。
6. `projects/thesis-fso/worker-logs/step-088-c1-a0-preflight-verifier.md`。
7. OFC2017 source adjudication：`projects/thesis-fso/worker-logs/step-081-c1-ofc2017-slip-state-fulltext.md`。

step-088 的 P1：

- P1-1：D0 acceptance functions 不定量、不 fail-closed。
- P1-2：三路 test-time B2 envelope 与 6.50 日单-B2 BOM 不一致。

修订版的预期修复不是沿用旧要求，而是：冻结唯一 dev-selected `B2_PRIMARY=OFC2017_LIKE_PILOT_4STATE_SOFT_LLR`，禁止 test-time best-of；其他 families 只约束 ceiling；预算改为 D0 3.50d + post-D0 3.00d + contingency 0.50d = 7.00d point estimate，并保留 asset preflight blocker。

## 2. 必审问题

1. A0 §0–§6、A′、A、B 是否仍逐项 evidence→status→fatal，且没有把 conditional entry 升为 A0 PASS、Step 4a Go 或方法信号。
2. 理论式、Gray square-16QAM 四态、384 symbols/CW、interleaver mapping 与 claim ceiling 是否准确；O1=0 是否严格限定 noiseless。
3. `B2_PRIMARY` 的输入、pilot/state/LLR/one-way decoder interaction、`L/M/N` grid 与 QPSK→16QAM transfer 标签是否忠实于 step-081；是否禁止按 test cell/seed/realization/metric best-of。
4. PAPU/global retry/differential/CSSC/CS-DC 是否只承担正确层级的 ceiling；primary comparator 改变 pilot 信息时是否显式扣资源、没有虚称 same-information。
5. coverage 是否只用于 affected-CW FER；latency/calls/goodput 是否独立；90/95 CI rule 是否可执行且 fail-closed。
6. D0.0–D0.6 是否每门都有 population/exposure、metric、effect threshold、CI、maximum exposure 与 terminal；重点审查 D0.1 event definition、D0.2/3 headroom、D0.4 grey zone、D0.5 candidate support/length bias、D0.6 false-action/cost。
7. D0.5 的 `S_DEC` 是否 equal-support normalized；`S_RX` 是否 receiver-only 且比较公平。若 square-QAM symmetry 导致 max-log ties，判断它作为 no-decoder baseline 是否足够，或是否会人为制造弱对手。
8. natural/controlled、coded/uncoded、ranking/true-boundary 三组边界是否全部 fail-closed；accepted wrong actions 是否计错；fallback 是否只用 receiver-visible rejection/instability。
9. one-shot frozen evidence + per-candidate full restart 是否确实排除 ICTON recursive oscillation；是否仍有旧-state复用或 truth leakage。
10. 7.00 日表逐项复算；判断 OFC2017-like 16QAM B2、population/CI、identity/safety tests 是否被遗漏或重复。只可裁 `POINT_ESTIMATE_COHERENT` 或指出具体缺项，不能把 point estimate 当已证明 feasible。
11. 抽查至少 18 个可证伪事实/文件指针；检查所有 owner 文件存在。
12. 检查中央报告的审查历史是否如实保留 step-088 FAIL，且 D0 仍 `AUTHORIZED=NO`。

## 3. 产出格式

```markdown
# Step 089 — C1 A0 revised preflight fresh re-verifier

> control receipt / scope / no-experiment receipt

## 1. Verdict
PASS 或 FAIL；P0/P1/P2=x/y/z；一句话 disposition。

## 2. Step-088 closure
P1-1、P1-2 分别 CLOSED/OPEN + 可复核证据。

## 3. Requirement matrix
A0 §0–§6、A′、A、B、physical、truth、B2、coverage、BOM、D0.0–D0.6：PASS/FAIL + evidence。

## 4. Fact spot-checks
至少 18 项，含公式、mapping、OFC2017参数、统计门、预算算术、文件存在性。

## 5. Findings
P0/P1/P2；无则明确 0。每项给文件行号、为什么、所需修正。

## 6. Control disposition
只能是：维持 CP010 等待修复，或允许主控另立 D/V/CP 开放 D0；不得直接授权实验。

## 7. Protection receipt
p05 四 SHA、git staging、唯一写入文件、未运行禁止动作。
```

## 4. 验收

- [ ] fresh task-control validator 对 T043/CP010 PASS。
- [ ] step-088 两个 P1 均有独立 closure verdict。
- [ ] 至少 18 个事实抽核，且不是只看中央报告自洽性。
- [ ] 预算 3.50+3.00+0.50=7.00 逐项复算；仍明确是 preflight-pending point estimate。
- [ ] PASS 时 P0/P1/P2 必须 `0/0/0`；否则 FAIL。
- [ ] p05 SHA 4/4 与既有 receipt 一致；staging 为空；唯一写入 step-089。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-089-c1-a0-preflight-reverifier.md`
