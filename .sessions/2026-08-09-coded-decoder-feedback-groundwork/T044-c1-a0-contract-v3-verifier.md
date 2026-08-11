# Task Brief: C1 A0 / D0 contract v3 fresh verifier

> 来源: S001 / D009 / H002 / step-088–089 FAIL | 产出位置: `projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`
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

在证据 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`，fresh-context 验证两个中央 owner：

1. `projects/thesis-fso/coded-decoder-feedback-groundwork/step4a-a0-preflight.md`
2. `projects/thesis-fso/coded-decoder-feedback-groundwork/d0-defect-smoke-contract.yaml`

只写 `projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`。12 分钟目标、15 分钟绝对硬上限；禁止替主线程修文件。

## 1. 最高纪律

1. 当前仍 CP010/epoch10，D0/adapter/MVE/实验禁止；即使 PASS，也只能建议另立 D/V/CP。
2. 不运行 web/search/download、仿真、defect smoke、代码实现、commit/push。
3. 不修改/暂存四个 `p05_run*.log`。
4. PASS 必须 P0/P1/P2=`0/0/0`；任何可导致相反科学裁决的自由度都是 P1。

## 2. 必读

- `stages/gw-feasibility.md` A0/A′/A/B 与 3–7 日边界。
- 中央 report + YAML owner。
- step-081、step-085、step-086、step-087、step-088、step-089。
- OFC2017 正文 `papers/doi/10.1364_ofc.2017.w2a.56/7937400.md`。
- P08-R2 chain/phaseA/codec 与 `common/_recovery.py::bps_cpr`。
- topic-index/decisions/verifications/H002 当前控制。

## 3. 必审问题

### A. step-089 三个 P1 closure

1. controlled exposure、natural/controlled职责、合取、cluster unit、dual-pol ownership、D0/post-D0 action-policy 是否唯一且 fail-closed。
2. unknown-data max-log symmetry tie 是否已完全退出 acceptance；`S_PILOT` 是否非退化、receiver-visible、同 candidate support，fusion/tie/absolute+incremental gates 是否可执行。
3. B2 front-end、`p_s/sigma_e2`、exact source tuples、pilot placement、16QAM LLR、one-way decoder、dev/test best-of prohibition 是否唯一；所有 source transfer 是否明示。

### B. 独立一致性与算术

4. YAML 可 parse；report 不维护冲突的第二套数字；所有路径存在。
5. B2 exact tuples 必须是 `(2,100),(3,10),(3,20),(3,100),(3,200)`；pilot count、frame extension 与 no-puncture 语义复算。
6. B0/B1/B2/O1/C1 的同 waveform/payload/time support 是否消除额外 pilot 买 FER 的 unfair Kill；B1/B2 是否独立 dev 选择并一次冻结。
7. S1=`240→600 frames/1200 pol-trajectories`；S2=`60 clusters×9=540 +60 off`；S3 candidate count=10、每 case CW-decodes=`16+3*(12+8+4)=88`、test total=`47,520`；S4=60。逐项复算。
8. damage/recoverability/coverage estimands、bootstrap ratio-of-sums、zero/negative denominator guard、CI/clipping 是否能从 raw rows唯一计算；natural rows不得承担 damage counterfactual。
9. S1 count/diversity gate与 descriptive cluster CI是否诚实，不再误用 pooled exact-binomial；multi-transition natural frames不得进入 ranking。
10. D0 不存在 false-action/fallback policy；clean safety移到 post-D0是否符合用户 defect-smoke/adapter顺序，而非漏掉安全门。
11. B2 source adaptation 2.00d、D0 4.50d、post-D0 2.00d、contingency 0.50d，总计7.00d；检查是否仍漏 source adaptation、dev compute、fresh held-out、tests/receipt，或 contingency 规则自相矛盾。
12. report 的 A0 §0–§6、A′、A、B 与 physical/truth ceiling没有被数值合同越级成 A0 PASS、Step4a Go或方法信号。
13. 抽查至少 22 个可证伪事实，包含来源、源码、YAML算术与治理授权。

## 4. 产出格式

```markdown
# Step 090 — C1 A0 / D0 contract v3 fresh verifier

> control / scope / no-experiment receipt

## 1. Verdict
PASS/FAIL；P0/P1/P2=x/y/z。

## 2. Prior-finding closure
step-089 P1-1/P1-2/P1-3 各 CLOSED/OPEN。

## 3. Requirement matrix
A0、physical、truth、B2、four strata、statistics、budget、authorization。

## 4. Fact spot-checks
至少22项。

## 5. Findings
逐项行号、影响、所需修正；无则明确0。

## 6. Control disposition
维持 CP010 修复，或允许主控另立 D/V/CP；不得直接授权D0。

## 7. Protection receipt
p05 4 SHA、staging、唯一写入、禁止动作。
```

## 5. 验收

- [ ] task-control T044/CP010 PASS。
- [ ] YAML parse 与全部关键算术 fresh 复算。
- [ ] step-089 三个 P1 逐项 closure。
- [ ] 至少22项回源；PASS时0/0/0。
- [ ] p05 4/4、staging empty、唯一新增 step-090。

## 附：产出

`projects/thesis-fso/worker-logs/step-090-c1-a0-contract-v3-verifier.md`
