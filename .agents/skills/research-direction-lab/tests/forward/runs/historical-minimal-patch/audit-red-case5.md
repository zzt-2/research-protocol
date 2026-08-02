agent_task: /root/audit_red_case5
fork_turns: none
skill_identity: git:53085bb5d1b7cc3e759e62af5c55397979402acc
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case5.md

## Raw adjudication

## 原始裁决

- `formal_science_disposition`: `EXECUTION_INVALID`
- `method-bearing`: 否
- `contribution tier`: `NONE`
- `mission_method_delta`: `NONE`
- `claim ceiling`: `RUN`，且仅限失效审计事实；不支持 `CELL / SLICE / CONTRACT` 科学结论。

### 裁决依据

1. 冻结身份失败。receipt 记录的 `p11_run.py` SHA-256 为 `e7eb...6688`，实际 allowlist 文件为 `4607...7186`；其余三个可核源码 hash 匹配，sidecar 也与 receipt 字段匹配。故 raw 结果无法绑定到当前 runner。

2. 当前参数链违反四 cell 合同。`p11_run.py:121-128` 冻结 9/11/13/15 dB，但 `gen_realization()` 在 `p11_run.py:271-274` 未传 `gamma_db`；callee `ml_long_seq_failure.py:154-169` 没有 SNR 形参，直接使用模块常量 `GAMMA_BAR`，其值来自 `params.py:502-511` 的 `100.0 = 20 dB`。此外，运行时依赖 `params.py` 未纳入 receipt 的 `source_hashes`。因此当前 runner 实际描述的是四个均为 20 dB 的 turbulence/fG/SOP slice，不是冻结的 9/11/13/15 dB cells。

3. 统计实验单位不匹配。每个 pilot fraction 有 4 cells × 8 seeds = 32 行，但四个 cell 重复使用同一组 8 个 seed；`p11_run.py:476-484` 将 32 个 cell-seed 差值当作独立样本，报告 `n=32`。跨 cell estimand 应以 seed 为 cluster（`n=8`），或分别报告每 cell 的 `n=8`。按相同正态近似改为 seed-cluster 后，最大 CI 半宽由 `0.0001206` 增至约 `0.0001531`；方向仍未越过 MDE=0.05，但原 CI 和 `n=32` 不成立，且不能推广到固定四 cell 之外。

4. raw 仅包含 B0–B4 baselines；候选 C1–C3 未运行。因此即使 Phase A 合法，也只能形成 conventional-baseline adjudication，不能形成方法信号。

### 可保留内容

- raw、receipt 和旧 verdict：仅作为 `invalidated` 历史链及 `EVALUATION_INSIGHT`。
- `p11_methods.py` 中 LS/RLS/pilot 工具：可作为待独立验证的 `REUSABLE_ASSET`。
- 不得保留“9/11/13/15 dB 下 complex LS 已解决问题”、方法贡献或论文实验结论。

### 下一合法动作

修复并重新冻结 runner：显式贯通 `gamma_db → gamma_bar → noise variance`，把 `params.py` 等实际参数依赖纳入 source closure，在 raw 中写入 realized SNR；预注册按 cell 分层或按 seed 聚类的统计量。由于现有 held-out 已揭示，须用新的不相交 test seeds 重跑 Phase A。只有新证据执行有效后，才能裁决 `PROBLEM_RESOLVED_BY_COMPLEX_LS` 或进入候选比较。

## 实际读取路径

- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/SKILL.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/method-production.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/thesis-harvest.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\tests\forward\runs\historical-minimal-patch\prompts\case5.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p11-pilot-efficient-butterfly-fir\p11_entry_gate.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p11-pilot-efficient-butterfly-fir\p11_methods.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p11-pilot-efficient-butterfly-fir\p11_run.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\cma-fade-divergence\ml_long_seq_failure.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\params.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_verdict.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_phaseA_test_raw.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_phaseA_dev_raw.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_freeze_receipt.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p11_pilot_efficient_butterfly_fir\p11_freeze_receipt.sha256`
