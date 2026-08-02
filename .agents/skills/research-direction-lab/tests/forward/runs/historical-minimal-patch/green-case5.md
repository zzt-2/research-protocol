# GREEN Case 5 — parameter injection and clustered evidence

> fresh context, read-only, raw adjudication reproduced verbatim below

裁决：**不支持按“4-cell 多 SNR”接受 `PROBLEM_RESOLVED_BY_COMPLEX_LS`；正式终态应为 `EXECUTION_INVALID`，可降格保留为单一 20 dB 切片的诊断性 baseline adjudication。**

证据：

- 冻结合同声明 4 个 cell 的 SNR 为 9/13/11/15 dB：`p11_run.py:121-128`。
- 实际路径 `gen_realization()` 没有传入 `gamma_db`：`p11_run.py:271-274`。
- `gen_channel()` 的噪声固定使用全局 `GAMMA_BAR`：`ml_long_seq_failure.py:154-170`；该值固定为 100，即 20 dB：`ml_long_seq_failure.py:60-62`、`params.py:502-504`。
- 因此实际是多湍流/\(f_G\)/SOP、**单 SNR=20 dB**，触发 Research Direction Lab 的 `parameter_injection` 语义门 FAIL。source hash/receipt 只能证明“跑的是这份代码”，不能修复该语义错误。
- 指标合同也未完全落地：`fixed_label_ber()` 仅跳过前 25%，没有排除 pilot/training 位置，且只评分 X 偏振：`p11_run.py:243-251,281-305`。B0 用前 50% 标签训练：`p11_methods.py:231-245`，所以评分窗口含 25%–50% 的训练内样本；这不是冻结合同声称的纯 payload、双偏振评价。
- verdict 按 pilot fraction 直接把 4 cell × 8 seeds 合成 `n=32`：`p11_run.py:473-488`。四个异质 cell 不应作为 IID 样本池化，同一 seed 又跨 cell 复用；主分析应按 `cell × pilot_frac` 分层，池化最多是预先定义的等权二级摘要。
- 重新按 cell 分层检查现有 held-out 数据后，24 个 `cell × fraction` 的 B2−B0 CI 上界都小于冻结的 0.05 margin；最大 CI 上界约 \(2.245\times10^{-4}\)，最大半宽约 \(4.698\times10^{-4}\)。所以现有负面不是由跨 cell 抵消制造的，但它只能支持“20 dB、X 偏振、当前混合评分窗口下 LS 看似不劣”的诊断结论，不能补救语义 FAIL。

论文资格：**当前不能成为 method-bearing thesis item**。`mission_method_delta=NONE`；最多是待修复的 `EVALUATION_INSIGHT / BASELINE_ADJUDICATION / BOUNDARY_RESULT`。即使修复后仍由传统 LS 解决，也属于 supporting material，不是 `METHOD_SIGNAL`；目前也没有真实计算成本、双偏振 payload-only goodput 证据，尚不够 `THESIS_ENGINEERING_COMPONENT`。

下一合法动作：做一个有界语义修复包——显式把每格 `gamma_db` 注入噪声生成，并用同 seed 双 SNR sentinel 验证噪声方差/BER 确实变化；改为双偏振、排除全部 pilot 与 B0 training 样本的 payload-only 指标，使用实际 pilot fraction；预冻结按 cell 的 non-inferiority 规则并以新 held-out seeds 重跑 Phase A。修复后若各格仍由 LS 解决，则接受 scoped negative 并关闭该方法轴；只有某些修复后 cell 中问题仍存活，才允许仅对那些 slice 开候选 Scout。
