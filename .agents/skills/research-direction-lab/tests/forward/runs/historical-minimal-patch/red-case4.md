# RED Case 4 — evidence coverage

> baseline bundle: `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`
> fresh context, read-only, raw adjudication reproduced verbatim below

RAW ADJUDICATION

- `formal_science_disposition`: accept only as a bounded Phase-A gate negative, `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE`, at `CELL/LOCAL_SLICE` scope.
- `mission_method_delta`: `NONE`.
- Promotion: `NO`. Phase B/C、候选路由器与 held-out test 均未运行，因此没有 `METHOD_SIGNAL`、method card 或 promotion preflight 的合法入口。

Evidence:

- ML-favored cell 虽 6/6 为 ML 更低，但均值差仅 `−6.08e−5`，远未达到冻结 MDE `0.02`，故 crossover gate 明确失败；CMA-favored cell 单独通过不足以形成双向 crossover。[p10_phaseA_dev_raw.json](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_phaseA_dev_raw.json:126) [p10_phaseA_dev_raw.json](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_phaseA_dev_raw.json:232)
- 冻结脚本规定两 cell 均须通过，否则直接进入该终态；因此停止 Phase B/C 合法。[p10_phaseA_crossover.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:31) [p10_phaseA_crossover.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:318)
- raw 与 checkpoint 的 12 行结果一致，seed 均为 13000–13005；receipt 也记录 Phase A FAIL、未运行 held-out test。[p10_freeze_receipt.json](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_freeze_receipt.json:275)

Campaign closure: `REJECT`.

- 裁决自身明确 P10“不计有效包”、计数仍为 `7/10`，随后却声称“10-有效包探索完成”，内部逻辑直接矛盾。[p10_verdict.md](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_verdict.md:51) [p10_verdict.md](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_verdict.md:61)
- 它还自行把 claim ceiling 限为 `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`；这种证据不能上推为 campaign exhaustion。[p10_verdict.md](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_verdict.md:56)
- 另有完整性缺口：实际生成证据的 `p10_phaseA_crossover.py` 未被 freeze receipt 的 source-hash 清单绑定；receipt 只冻结 `p10_methods.py`、`p10_run.py` 及外部 common 文件。[p10_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_run.py:145) [p10_freeze_receipt.json](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/results/p10_single_expert_router/p10_freeze_receipt.json:174)
- “swap artifact”不应成为绑定结论：合同称 PI-BER 为 secondary、只报告不裁决，但 Phase-A 脚本实际将 PI 方向纳入 PASS。这不改变 ML-favored cell 已按 PRIMARY/MDE 失败的终态，却削弱了附加机制归因。[p10_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_run.py:67) [p10_phaseA_crossover.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p10-single-expert-router/p10_phaseA_crossover.py:318)

Next legal action:

1. 接收 P10 为“不计 campaign 有效包”的局部负结果，并记录 `mission_method_delta=NONE`；不得推广。
2. 先做 bounded integrity repair：绑定 Phase-A executor 身份，并把终态依据收窄到 PRIMARY/MDE；若要求正式计数，则需在预冻结后独立复核/重跑，事后补 hash 不足以证明运行时身份。
3. 回到 Recover/Map，核实当前 portfolio remap。若仍有 `READY`/`NEEDS_SMALL_ADAPTER`，继续合法候选；若确为 `READY=0 / NEEDS_SMALL_ADAPTER=0`，只能进入 `PREFORMAL_METHOD_FACTORY` 或 `STRATEGIC_GATE`。
4. 只有补足当前授权要求的有效包，或由用户显式修改“10 个有效包”目标，或证据化证明合法路线已耗尽并作战略关闭，campaign 才能结束。
