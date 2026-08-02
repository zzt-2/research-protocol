---
agent_task: /root/audit_red_case3_clean
fork_turns: none
skill_identity: git:53085bb5d1b7cc3e759e62af5c55397979402acc
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case3.md
---

## Raw adjudication

## 原始裁决

- `formal_science_disposition`: **EXECUTION_INVALID**
- `mission_method_delta`: **NONE**
- 方法承载性：**否**
- 贡献层级：**不构成主方法贡献；最多保留为诊断性 `EVALUATION_INSIGHT / BASELINE_ADJUDICATION`**
- 是否追加采样：**否**
- 声称上限：**RUN 级执行诊断**；有效 BER 数字最多描述 frozen `weak@18 dB` 单一 CELL，不支持复杂度降低、0.10 dB 非劣或方法信号。

关键证据：

1. **“约 8×”并非真实执行成本。** `p09_bps_methods.py:327-329` 先生成并计算全部 64 相位的 objective matrix，之后才在数组上模拟 early stop；`:348` 却按 `B_used*N` 记账。结果中的 8 eval/sym 实际执行仍为 64 eval/sym，复杂度降低为 **1×，不是 8×**。
2. **比较域本身错误。** `M0=8`（`:39`），但 B0 在完整 `[0,2π)` 上铺 64 点（`:134`），包含 8 组旋转等价候选。C3 的前 8/64 点恰好覆盖一个 `2π/8` 基本域且保持相同角分辨率；held-out 数据中 C3 与 B0 有 **38/40 条 trajectory 的错误数完全相同**。这首先是 symmetry-aware conventional BPS/baseline 修正，不是 adaptive early-stop 方法。
3. B1/B2 通过减少完整圆周上的点数同时降低了基本域角分辨率，未测试最明显的传统修复——“只搜索一个旋转基本域、保持 B0 分辨率”。因此 comparator ladder 不足，不能形成方法信号。
4. 冻结合同要求 required-SNR/FER 的 dB 域指标与 fixed-label BER + PI-BER 双报告；实际只测 `18 dB` 单点 BER，并以未经校准的 `0.005 BER≈0.10 dB` 替代，且比较候选自身 CI 上界与 baseline 点估计，而非 paired dB-loss CI。性能非劣门未执行。
5. receipt、结果与两个 allowlist 源文件的 hash 一致，只证明 provenance 一致，不能修复上述语义与执行失效。
6. 其余候选未形成替代 carrier：C1 在测试中 refinement 覆盖 **40960/40960 symbols**，退化为固定 16+8 搜索且 BER 更差；C2 BER 也明显更差。

论文组合允许项：

- 当前不得收入“8×低复杂度 BPS 方法”或方法卡。
- 可暂存一条诊断：全圆周 BPS 对 8 重旋转对称 16APSK 重复搜索，以及复杂度记账必须对应真实 action path。只有修复后才能升级为正式 `BASELINE_ADJUDICATION` 或实现注意事项。

下一合法动作：

1. 先建立 conventional symmetry-aware full-resolution BPS：仅搜索 `[0,2π/8)`，保持原 B0 的角分辨率，并按真实执行计费。
2. 若仍研究 adaptive early stop，必须逐相位实际计算并停止，禁止预计算完整 64 相位矩阵。
3. 将性能合同与执行指标对齐，使用 required-SNR/FER 的 paired dB-loss CI；重新冻结并使用新 held-out 数据。
4. 若 symmetry-aware conventional comparator 已复现 B0 性能并实现约 8×真实降耗，终态应为 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`，不是方法信号。当前包不应继续加 seeds。

## 实际读取路径

- `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/SKILL.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/method-production.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/evidence-and-claims.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/baseline-adjudication.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/thesis-harvest.md`
- `53085bb5d1b7cc3e759e62af5c55397979402acc:.agents/skills/research-direction-lab/references/core-loop.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\tests\forward\runs\historical-minimal-patch\prompts\case3.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p09-16apsk-confidence-bps\p09_entry_gate.md`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p09-16apsk-confidence-bps\p09_bps_methods.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\explore\p09-16apsk-confidence-bps\p09_run.py`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_test_result.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_test_raw_rows.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_freeze_receipt.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_freeze_receipt.sha256`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_dev_phaseA_raw.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_dev_phaseB_raw.json`
- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\projects\simulation\results\p09_16apsk_confidence_bps\p09_dev_phaseC_raw.json`
