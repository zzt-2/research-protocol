# GREEN Case 2 — hidden-truth leakage

> fresh context, read-only, raw adjudication reproduced verbatim below

裁决：`EXECUTION_INVALID`；不接受 `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`。`mission_method_delta=NONE`，不得进入更大证据或方法包装；现有结果最多是失效运行的诊断材料。

关键证据：

- 部署链存在隐藏真值泄漏。`gamma_bar` 由测试 SNR 直接注入实现（`p08r_run.py:41-50`），随后在均衡器中用于噪声扣除和 MMSE 均衡（`p08r_chain.py:341-359`），违背源码声明的“true γ 不进入 decide”（`p08r_chain.py:11-13`）。
- V074 没有发现该泄漏，因为检查 5 只截取 `method_B0/B1/B2` 函数体并搜索 `real.gamma_bar`（`p08r_verify.py:109-129`），没有沿 `build_realization → real.equalize → mmse_equalize` 递归检查。故 `16/16 PASS`（`p08r_v074_result.json:2-5`）不能证明信息边界合法。
- absence 判据在当前单元上不可达到。冻结的 `MDE_fer=0.234661`（`p08r_phaseA_gate.json:112-117`），但测试最强固定 conventional B2 的 FER 仅 `0.113281`（`p08r_phaseA_gate.json:164-172`）；即使 oracle 将 FER 降到 0，最大均值改善也小于 MDE。代码却要求 oracle 改善超过该 MDE，否则直接判 problem absent（`p08r_run.py:342-355`）。该裁决因此被门限结构性预定，而不是由证据支持。
- “strongest conventional”在测试数据上逐轨迹取 `min(B1,B2)`（`p08r_run.py:282-291`），不是预先冻结的单一 comparator。虽然本批数据中 B2 在 2 条轨迹更好、其余 38 条相同，未改变均值，但裁决实现仍不合法。
- H6 所称逐码字迭代/evidence 未落盘：decoder diagnostic 被各方法丢弃（`p08r_phaseA.py:138-205`），评分只保存聚合计数（`p08r_phaseA.py:214-230`）；raw schema 也只有轨迹级 FER/BER 和 fade 摘要（`p08r_phaseA_raw_rows.json:2-25`）。Verifier 检查 10 只确认聚合字段存在（`p08r_verify.py:177-180`）。

下一合法动作：做一个同包、有限的语义修复，不扩 seeds/cells。移除 deployable equalizer 对 `gamma_bar` 的依赖；加入端到端 hidden-truth metamorphic test（固定接收观测和 prefix，仅改变 γ/h/θ 元数据，要求 B0/B1/B2 输出完全不变）；以 dev 上的配对轨迹差分重新冻结可达到的 MDE，并允许 `EVIDENCE_INSUFFICIENT`；固定单一 B2 comparator；补齐逐码字 evidence；由递归 caller-to-callee verifier 独立复核。修复改变执行路径且旧测试已观察，之后必须用新鲜 dev/test seeds 重跑。只有这些 semantic gates 全部 PASS 后，才可重新裁决是否进入 Scout；即使合法获得 absence/negative，也只能作为 `SUPPORTING_MATERIAL`，不能方法包装。
