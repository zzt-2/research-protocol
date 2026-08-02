agent_task: /root/audit_green_case3
fork_turns: none
skill_identity: working-tree-canonical
prompt: .agents/skills/research-direction-lab/tests/forward/runs/historical-minimal-patch/prompts/case3.md

## Raw adjudication

## 原始裁决

- **Formal science disposition：`EXECUTION_INVALID`**
- **Mission method delta：`NONE`**
- **方法承载性：否**
- **Contribution tier：`SUPPORTING_MATERIAL`**
- **Claim ceiling：`RUN` 级诊断事实；不得声称“约 8× 复杂度降低”或“匹配性能”**
- **更多采样：不合理。语义/执行 FAIL 不能靠增加 seed 修复。**

### 关键证据

1. **8× 成本数字不对应真实调用路径。**
   `C3_early_stop` 先执行完整 64 相位的 `bps_objective_matrix`，之后才截取前 `B_used` 行，却按 `B_used × N` 计费：
   - `p09_bps_methods.py:328-329`：先算全部 64 相位。
   - `p09_bps_methods.py:344`：事后取 `metrics_all[:B_used]`。
   - `p09_bps_methods.py:348`：只登记 `B_used × N`。
   因此测试结果中的 `64 → 8 evals/sym` 是**计数器节省，不是真实 distance/objective evaluation 节省**，触发 `real_action_and_cost=FAIL`。

2. **性能证据不符合冻结合同。**
   合同要求 `required_SNR_dB_at_frozen_FER`、相对 full-BPS 的 dB 域损失 CI，以及 fixed-label BER + PI-BER 双报告；实际只跑 `weak@18 dB` 单 cell 的 truth-resolved BER，并将 `0.10 dB` 临时替换为 `0.005 BER`：
   - `p09_run.py:78`：冻结的 dB/FER 指标。
   - `p09_run.py:416`：测试固定为单点 18 dB。
   - `p09_run.py:468`：只对各方法自身 BER 做边际 bootstrap。
   - `p09_run.py:509-513`：用未经验证的 `0.005 BER` 代替 `0.10 dB`，且比较“方法上界 vs baseline 均值”，不是配对损失 CI。
   - `p09_bps_methods.py:381`：评分前以 TX bits 做 blockwise ambiguity resolution；没有合同要求的 fixed-label/PI-BER 双报告。

3. **所谓自适应动作实际退化为固定 8 相位子域。**
   40 条 test trajectory 中 C3 的 `B_used` 全为 8；与 B0 的逐 seed BER 有 **38/40 完全相同**，均值差仅 `-0.000238`。结合 `M0=8` 和 C3 使用 full-64 网格的前 8 个相位，这更像“只搜索一个 π/4 基本域”的传统对称性去冗余，而不是数据驱动 early-stop 方法。

4. **其余真实执行 comparator 不支持 8×。**
   - B1：32 evals/sym，约 2×。
   - B2：40 evals/sym，约 1.6×。
   - C1：24 evals/sym，但所有 1024 symbols 在所有阈值下均触发 refinement，不具 confidence-adaptive 行为，且 BER 更差。
   - C2：约 16.28 evals/sym，BER 明显更差。

5. **工件身份/时间线局部通过，但不挽救科学语义。**
   receipt 文件 SHA256 与 `.sha256` 及 test result 中记录一致；两个 allowlist 源文件当前 hash 也与 receipt 一致。该 PASS 只证明工件身份，不证明动作和指标有效。

### 可进入论文组合的内容

仅可作为 `SUPPORTING_MATERIAL` 保存：

- `EVALUATION_INSIGHT`：复杂度计数必须来自真实调用轨迹，不能“全算后少计”。
- `BASELINE_ADJUDICATION`：full-BPS 的 `0..2π` 搜索可能包含 8 重旋转等价冗余；应先补一个在 π/4 基本域上执行的传统 comparator。
- 失败教训：冻结 dB/FER 合同不能由单点 BER 和经验换算代替。

当前 8× 数字、非劣结论及 C3 方法信号均不得进入论文。

### 下一合法动作

先做**有界语义修复，而非加样本**：

1. 将 π/4 基本域、同等相位分辨率的 BPS 实现为真正只计算所需候选的传统 comparator，并用实际调用 trace 计费。
2. 补 executable `real_action_and_cost` smoke，确认未构造未用的 64 相位矩阵。
3. 按冻结合同做配对多 SNR 评估，估计 required-SNR/FER 损失 CI，并分别报告 fixed-label BER 与 PI-BER。
4. 只有全部语义门 PASS 后才允许 fresh held-out Scout。若该传统 comparator 已保性能并实现约 8×，终态应为 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`，不是方法信号。

### 实际读取路径

Assigned Skill：

- `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2\.agents\skills\research-direction-lab\SKILL.md`
- `...\references\evidence-and-claims.md`
- `...\references\baseline-adjudication.md`
- `...\references\method-production.md`
- `...\references\thesis-harvest.md`
- `...\references\core-loop.md`
- `...\tests\forward\runs\historical-minimal-patch\prompts\case3.md`

Evidence allowlist：

- `projects/simulation/explore/p09-16apsk-confidence-bps/p09_entry_gate.md`
- `projects/simulation/explore/p09-16apsk-confidence-bps/p09_bps_methods.py`
- `projects/simulation/explore/p09-16apsk-confidence-bps/p09_run.py`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_test_result.json`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_test_raw_rows.json`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_freeze_receipt.json`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_freeze_receipt.sha256`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_dev_phaseA_raw.json`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_dev_phaseB_raw.json`
- `projects/simulation/results/p09_16apsk_confidence_bps/p09_dev_phaseC_raw.json`

另读取了子 agent 启动流程文件 `C:\Users\zzt\.agents\skills\using-superpowers\SKILL.md`；其内容明确要求已派遣子 agent 忽略该流程，未据此扩展审计范围。未读取 `.sessions`、Git 旧版、later audits 或 prior outputs；未修改文件、未运行实验。
