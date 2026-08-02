# GREEN Case 3 — real cost/action

> fresh context, read-only, raw adjudication reproduced verbatim below

**裁决：REJECT 当前方法信号；正式状态应为 `EXECUTION_INVALID`，不是扩大样本确认。**

- 报告值：C3 在 40 条 held-out 轨迹上 BER `0.031189`，B0 为 `0.031427`，账面复杂度 `8` vs `64` eval/sym；配对后 38/40 条 BER 完全相同。
- 决定性缺陷：`bps_early_stop` 先执行完整 `B_max=64` 目标矩阵，再只按 `B_used=8` 记账（[p09_bps_methods.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p09-16apsk-confidence-bps/p09_bps_methods.py:327)，尤其 328–330、344–348）。真实距离计算仍是 `64N`，不存在 8× 执行成本下降，违反 RDL `real_action_and_cost` 门；统计扩样不能修复。
- 比较器也错位：16APSK 明示 `M0=8`，C3 恰取 full-64 网格的前 8 个相位；dev 中 `B_min=8` 对三个停止阈值均得到完全相同 BER/复杂度，说明该结果主要是旋转对称基本区间，而非 adaptive early-stop 信号。现有 B1 的 8 点却均匀铺满 `2π`，没有比较“8 个唯一相位覆盖一个 `π/4` 基本区间”的传统 symmetry-reduced BPS，因此尚未排除最便宜的传统解释。
- 合同还有指标失配：冻结主指标是固定 FER 所需 SNR 的 dB 损失 ≤0.10 dB，但测试只跑 18 dB 单点 BER，并以候选自身 BER 上界对 baseline 均值加 `0.005` 判定（[p09_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p09-16apsk-confidence-bps/p09_run.py:473)）。不能据此声称合同非劣。
- 允许范围内的两个源码 hash 与 receipt 一致，当前 receipt hash 也与结果记录一致；这支持身份/时序一致性，但不修复上述科学语义失败。

**下一合法动作：**做一次有界语义修复，而非扩大确认：实现真实按需计算的调用路径，并加入 `π/4` 基本区间上的 8 点 conventional BPS 作为 task-matched comparator；用调用轨迹证明实际 objective 次数等于记账数，同时恢复冻结的 dB-domain 配对非劣指标。若该传统比较器复现当前结果，应终结为 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`；只有 adaptive 构造在此后仍稳定胜出，才可重新考虑方法信号。
