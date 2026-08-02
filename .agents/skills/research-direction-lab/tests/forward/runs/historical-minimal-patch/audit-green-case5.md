---
agent_task: /root/audit_green_case5
fork_turns: none
skill_identity: working-tree-canonical
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case5.md
---

## Raw adjudication

裁决：`EXECUTION_INVALID`

- 执行有效性：否。收据记录的 `p11_run.py` SHA-256 为 `e7eb9856…6688`，当前允许文件实际为 `4607e6ad…7186`；其余 3 个允许源码哈希匹配，sidecar 也与收据字段一致，但 runner 身份不闭合，按证据完整性规则必须 fail closed。
- 参数注入：失败。当前 runner 冻结了 9/11/13/15 dB，但 `gen_realization()` 未向 `MLF.gen_channel()` 传递 `gamma_db`；callee 使用 `GAMMA_BAR_DEFAULT=100`，即固定 20 dB。由于 runner 又与收据哈希不符，既不能把当前路径认作历史执行路径，也不能证明四个标称 SNR 曾进入物理实现。
- 方法承载性：否。Phase C 未运行，只有 baseline 比较；即使负面终态有效，也不是方法增量。`mission_method_delta = NONE`。
- 统计单位：不匹配。裁决把每个 pilot fraction 的 4 cells × 8 seeds 当作 `n=32` 独立样本，并用正态 `1.96` CI；四个 cell 复用同一 seed，独立随机化单位应按 8 个 seed block 聚类。复算后的 t(7) 95% 半宽为 `0.0001666–0.0001847`，而报告为 `0.0001082–0.0001206`。该修正本身仍远低于 0.05 非劣阈值，但不能修复执行语义失效。
- 指标语义：不闭合。B0 用前 50% 标签训练，而 BER 从 25% 处开始计分，故 25%–50% 同时属于训练与评分；稀疏 pilot 又均匀覆盖全序列且评分未排除 pilot。所有方法只计 `zX/sX`，未计 `zY/sY`，也未实际生成合同所述 payload-only goodput。
- 贡献层级：`SUPPORTING_MATERIAL`，仅限“参数注入、来源身份、聚类统计和评分人口失败”的审计教训；不得保留任何贡献数字，不形成 active carrier。
- 可保留：原始 JSON 与方法代码可作为待修基础设施/故障复现材料；`PROBLEM_RESOLVED_BY_COMPLEX_LS` 科学终态、四 SNR 覆盖、CI 和性能数字均不可保留为证据。
- 主张上限：低于 `RUN` 科学主张；仅可陈述“当前证据包未通过完整性与语义审计”。
- 下一合法动作：先修复 `gamma_db → gamma_bar → nv` 注入并做两值/sentinel 行为门；冻结与执行完全一致的新收据；定义 payload-only、与训练/pilot 不重叠且覆盖双偏振的评分人口；以 seed 为 cluster、按 cell 分层分析。随后仅重跑 Phase A。有效 Phase A 关闭前不得运行 Phase C 或宣称方法信号。

实际读取路径：

- `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\tests\forward\runs\historical-minimal-patch\prompts\case5.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\SKILL.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\references\evidence-and-claims.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\references\method-production.md`
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
