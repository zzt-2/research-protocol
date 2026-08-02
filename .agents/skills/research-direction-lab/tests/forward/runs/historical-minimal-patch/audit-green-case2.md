---
agent_task: /root/audit_green_case2
fork_turns: none
skill_identity: working-tree-canonical
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case2.md
---

## Raw adjudication

裁决：`EXECUTION_INVALID`，应失效当前科学包并做同轴有界修复；不支持 accepted scientific package，不支持 method-bearing contribution，也不应追加采样。统计量不能修复语义门失败。

- `formal_science_disposition`: `EXECUTION_INVALID`
- `mission_method_delta`: `NONE`
- `contribution_tier`: `SUPPORTING_MATERIAL`，仅可保留为信息边界审计教训；现有 FER、CI 和“问题不存在”结论不得作为贡献数字。
- `claim_ceiling`: `RUN`，仅能声称“该次存储执行产生了这些数值，且其接收机路径被审计为无效”。不能提升到 `CELL`/`SLICE`。即便修复后沿用当前设计，单个 frozen test cell 最多先支持 `CELL`。

关键证据：

1. deployable caller chain实际为
   `p08r_run.build_realization()` → `CodedRealizationR(... gamma_bar=g)` → `real.equalize()` → `method_B0/B1/B2()`。
   `p08r_run.py:41-51` 将测试循环的真实 `snr_db` 转成 `gamma_bar`，随后立即调用均衡器。

2. `p08r_chain.py:341-360` 的均衡器两次使用隐藏真值 `self.gamma_bar`：先用 `1/(2γ)` 从接收功率扣噪声估计块增益，再把 `γ` 传给 `mmse_equalize`。因此 B0/B1/B2 虽从已知 prefix 估计解调 σ²，却消费了由真实 γ 生成的 `eqX/eqY`；“γ 仅用于物理噪声生成”的合同声明不成立。

3. V074 没有递归检查该调用链。`p08r_verify.py:109-129` 只截取 `method_B0/B1/B2` 函数体并搜索字符串 `real.gamma_bar`，没有进入其上游 `real.equalize()`，也没有执行“固定接收观测、仅扰动隐藏 γ，输出必须不变”的 metamorphic gate。因此 `p08r_v074_result.json` 的 `16/16 PASS` 不能证明信息边界通过。

4. 聚合器另有合同缺陷：`p08r_run.py:286` 用逐轨迹 `min(B1 FER, B2 FER)` 构造 `strongest_conv`，即依赖测试真值选择比较器，而不是一个冻结、可部署的常规基线。本批 raw 中 B2 在所有轨迹均不劣于 B1，故该缺陷未改变当前数值，但实现仍不具一般合法性。

5. 存储结果为 40 条测试轨迹；B0/B1/B2/O2 平均 FER 分别为 `0.11484/0.11484/0.11328/0.10938`，`strongest_conv−O2=0.00391`、95% bootstrap CI `[0, 0.01172]`，而冻结 MDE 为 `0.23466`。这些只描述含真 γ 的无效路径，不能支持 `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`。

下一合法动作：先移除 `equalize()` 对真实 `gamma_bar` 的运行时依赖，用 receiver-visible calibration/past state估计均衡所需量；补充完整 caller-to-callee hidden-truth metamorphic test；同时冻结单一 conventional comparator。上述门全部 PASS 后，使用新鲜证据重跑 Phase A 并独立复核。门通过前禁止扩种子或进入方法构造。

实际读取的 Research Direction Lab Skill：

- `.agents/skills/research-direction-lab/SKILL.md`
- `.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `.agents/skills/research-direction-lab/references/method-production.md`

实际读取的证据：

- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_phaseA.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_run.py`
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_verify.py`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_v074_result.json`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_prefail_evidence.md`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_phaseA_raw_rows.json`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_phaseA_gate.json`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_identity_freeze.md`
- `projects/simulation/results/p08r_coded_chain_repair/p08r_dev_workspace.json`
