---
agent_task: /root/audit_red_case2_clean
fork_turns: none
skill_identity: git:53085bb5d1b7cc3e759e62af5c55397979402acc
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case2.md
---

## Raw adjudication

裁决：`EXECUTION_INVALID → INVALIDATION/REDIRECT`

- 接受科学包：否
- 方法型贡献：否
- 贡献层级：`NONE`；`mission_method_delta=NONE`
- 更多采样：否。当前缺陷是语义/信息边界失效，增加 seeds 不能修复
- claim ceiling：`RUN`，仅能声称“当前运行产物给出这些数值”；不能声称问题不存在、传统基线已解决问题或关闭候选族

核心证据：

1. 部署链泄漏真实 SNR：`p08r_run.py:41-50` 将测试网格的 `g` 写入 `real.gamma_bar`，随后调用 `real.equalize()`；`p08r_chain.py:344,358-359` 又用该真值计算噪声底并调用 MMSE equalizer。因此，虽然 B0/B1/B2 的局部函数从 prefix 估计 LLR 方差，其上游输入 `eq` 已被真实 `gamma_bar` 特权处理。
2. V074 未检查完整 caller chain：`p08r_verify.py:114-129` 只抽取 `method_B0/B1/B2` 函数体并搜索 `real.gamma_bar`，遗漏 `build_realization → CodedRealizationR.equalize → method_B*`；check 16 在 `:234` 仅以此前通过数 `>=14` 判定，故 `16/16 PASS` 不能支持信息边界结论。
3. 数值本身也没有方法信号：40 条测试轨迹中，B2 FER `0.11328125`，O2 `0.109375`，差值 `0.00390625`、95% bootstrap CI `[0, 0.01171875]`，远低于冻结 MDE `0.2346609654`。但因执行无效，这只能是当前 artifact 的运行事实，不能升级为“问题不存在”。
4. 次要身份问题：`p08r_phaseA.py:159` 实际执行 `sigma2 / temperature`，与同一行“T>1 inflates σ²”的声明方向相反；应在重跑前冻结真实参数语义。

下一合法动作：先做有界信息边界修复，让部署态 equalizer 及 LLR 链只使用 calibration prefix、历史状态或其他接收端可见量；同步把 verifier 扩展到完整 caller→callee 链，并修正 temperature 语义。由于当前 test seeds 已观察，修复后须重新冻结全新 dev/test split，再执行独立验证与科学比较。若届时仍无超过 MDE 的 oracle headroom，只可收获 `BASELINE_ADJUDICATION/BOUNDARY_RESULT`，不能记为方法贡献。

实际读取路径：

- `git:53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/SKILL.md`
- `git:53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `git:53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/baseline-adjudication.md`
- `git:53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/method-production.md`
- `git:53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/thesis-harvest.md`
- `.agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case2.md`
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
