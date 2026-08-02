# GREEN Case 4 — evidence coverage

> fresh context, read-only, raw adjudication reproduced verbatim below

裁决：

- `package_acceptance = REJECT`
- `formal_science_disposition = EXECUTION_INVALID`
- `mission_method_delta = NONE`
- `promotion = FORBIDDEN`
- `campaign_closure = NOT_ESTABLISHED`

证据：

- 实际执行器 [p10_phaseA_crossover.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:1) 未被冻结回执绑定；[p10_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_run.py:145) 的哈希清单只有 `p10_methods.py`、`p10_run.py` 及外部依赖。实测 Phase-A 文件哈希为 `88ad2260…3742e4c`，回执中不存在。
- Phase-A 会直接复用无合同哈希、无源码哈希的 checkpoint（[p10_phaseA_crossover.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:157)、[同文件](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:240)）。现有回执还缺技能要求的 `seed_ledger`、`pre_test_state`、`post_test_state`；`test_started=false` 不能证明这 12 行开发结果的执行身份与时序。因此 verdict 的“chronology 闭合”不可接受。
- 即使暂时忽略完整性缺口，结果也只支持“两个开发 cell 未形成干净双向 crossover”：ML cell 的 `Δ=-6.08×10⁻⁵`，约比冻结 MDE `0.02` 小 329 倍；CMA cell fixed-label `Δ=+0.4500`，但 PI-BER `Δ=-0.01584` 反向。[原始结果](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_phaseA_dev_raw.json:126)
- Phase B/C、简单规则、router、held-out test 均未运行，故不能声称“configuration rule 已解决”，更不能产生或提升 `METHOD_SIGNAL`。[p10_verdict.md](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_verdict.md:49)
- verdict 一面明确 P10 不计有效包、campaign 仍为 `7/10`，一面又称“10-有效包探索完成”，内部矛盾；而 RDL 本身禁止用固定包数作为完成判据。[p10_verdict.md](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_verdict.md:51)

下一合法动作：

1. 若 P10 必须作为闭环证据：做一次有界完整性修复——冻结实际 Phase-A 执行器，补齐 receipt 状态与 seed ledger，给 checkpoint 绑定合同/源码身份，并用新的未见开发种子重跑同两格；独立验收后，最多接受为 `LOCAL_SLICE: NO_CLEAN_CROSSOVER`，仍不可提升。
2. 若不值得修复：将 P10 记为 `EXECUTION_INVALID / NONE`，原结果仅保留 diagnostic；随后由 master 读取完整 foreground control、mission-log 与当前 portfolio，证明正式目标已满足或所有合法 READY/小适配路线确已耗尽，才能裁决 campaign closure。当前获准证据不足以证明闭环。
