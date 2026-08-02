---
agent_task: /root/audit_red_case4
fork_turns: none
skill_identity: git:53085bb5d1b7cc3e759e62af5c55397979402acc
prompt: .../prompts/case4.md
---

## Raw adjudication

裁决：

- **Disposition**：`EXECUTION_INVALID / EVIDENCE_INSUFFICIENT`。P10 暂不能作为 accepted package；campaign closure 驳回。
- **Contribution tier**：`NONE`；`mission_method_delta=NONE`。现有结果至多是未受信任的 development observation。
- **Evidence**：
  - 两个 cell × 6 个 dev seeds 的数值支持 Phase A 表面 FAIL：ML-favored cell 的 Δ=-6.08×10⁻⁵，远低于 MDE=0.02；CMA-favored cell fixed-label Δ=+0.4500，但 PI-BER Δ=-0.01584，方向不一致。
  - `p10_phaseA_crossover.py` 是实际执行器，却未纳入 freeze receipt 的 `source_hashes`；receipt 只绑定了 `p10_methods.py` 和 `p10_run.py` 等文件，因此无法证明结果由当前 allowlist 中的执行器生成。
  - receipt 后写入 `dev_summary` 并重新计算自哈希，只证明当前文件自洽，不能恢复执行前的不可变来源闭合。
  - `p10_methods.py`、`p10_run.py` 和 receipt 当前哈希均与 receipt/sha256 文件一致，但这不弥补实际执行器未冻结的问题。
- **Claim ceiling**：无有效科学 claim；最多保留为 `UNTRUSTED RUN` 级诊断线索，不能提升到 `SLICE/CANDIDATE`。
- **Campaign implication**：无 campaign-level 增量，不能关闭 campaign。材料同时声称“P10 不计有效包、维持 7/10”和“10-有效包探索完成”，内部矛盾；allowlist 也没有完整 checkpoint chain、portfolio exhaustion 或合法替代项比较来支持 campaign closure。
- **Next legal action**：做一次有界证据修复：预先冻结并哈希实际 Phase A 执行器及完整依赖，用新的不相交 dev seeds 重跑，保留不可覆盖的 pre-run receipt 和结果哈希。若有效重跑仍为相同 FAIL，则接受本地 `PROBLEM_ABSENT_OR_RESOLVED_BY_CONFIG_RULE`、停止 P10 轴并回到 campaign-level Recover/Map；只有完整检查 checkpoint chain 与合法 READY 替代项后，才可决定继续、factory 或战略终止。

实际读取路径：

- `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\tests\forward\runs\historical-minimal-patch\prompts\case4.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/SKILL.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/core-loop.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/baseline-adjudication.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/method-production.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p10-single-expert-router\p10_entry_gate.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p10-single-expert-router\p10_methods.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p10-single-expert-router\p10_run.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p10-single-expert-router\p10_phaseA_crossover.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_verdict.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_phaseA_dev_raw.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_phaseA_dev_ckpt.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_freeze_receipt.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p10_single_expert_router\p10_freeze_receipt.sha256`
