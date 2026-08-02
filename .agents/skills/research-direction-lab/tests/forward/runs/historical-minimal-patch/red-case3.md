# RED Case 3 — real cost/action

> baseline bundle: `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`
> fresh context, read-only, raw adjudication reproduced verbatim below

原始裁决：**REJECTION — `EXECUTION_INVALID`**。不支持方法信号，也不应直接扩大样本确认。`mission_method_delta = NONE`。

事实依据：

- 复杂度声明失真：[`p09_bps_methods.py`](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p09-16apsk-confidence-bps/p09_bps_methods.py:327) 先无条件计算全部 64 相位及滑窗指标，随后仅按 `B_used` 计费（第 348 行）。因此实际 distance evaluations 仍是 64/symbol，不是报告的 8/symbol；即使改成真正串行，触发停止所评估的第 9 个相位也被漏计。
- “early stop”实际由 8 重旋转对称触发：`M0=8`（第 39 行），64 点全圆网格（第 327 行）的第 9 点正好是 `π/4`，与第 1 点属于同一等价类，故加入它不改善指标并立即停止。Dev 中 `B_min=8` 的 100 个轨迹点全部 `B_used=8`，96/100 与 B0 BER 完全相同；test 中 40/40 均报告 8 eval/symbol，38/40 与 B0 BER 完全相同。这是对称冗余暴露，不是自适应搜索机制证据。
- 传统比较器不合法：B1 将 8 点均匀铺在整个 `2π`（第 151 行），对 8 重对称 16APSK 而言这 8 点彼此等价；而 C3 的前 8 点是一个 `π/4` 模糊区间内的 8 个不同网格点。缺少最明显、低成本且任务匹配的传统比较器——在单个 `π/4` 区间内固定搜索 8 个唯一相位。
- 冻结合同要求 dB 域 required-SNR 损失 CI ≤0.10 dB，但 runner 只测单一 18 dB，并在 [`p09_run.py`](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p09-16apsk-confidence-bps/p09_run.py:506) 临时改用 `BER MDE=0.005`，且不是配对差值 CI。冻结主 estimand 未执行。
- 两个源文件当前 SHA256 与冻结 receipt 完全一致，说明缺陷属于实际生成该结果的冻结实现，而非事后代码漂移。结果文件自身也仅给出 `EVIDENCE_INSUFFICIENT`。

下一合法行动：做一次**有界语义修复与 comparator 重新裁决**，不是增加 seeds。真正按需计算相位并计入停止探针；加入单个 `π/4` 模糊区间内的固定 8 点传统 BPS；重新冻结 dB 域 SNR 曲线、配对损失 CI 和全新 held-out seeds。若固定对称缩减比较器复现优势，应裁为 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`；只有自适应候选再稳定胜过该比较器，才可考虑方法信号。
