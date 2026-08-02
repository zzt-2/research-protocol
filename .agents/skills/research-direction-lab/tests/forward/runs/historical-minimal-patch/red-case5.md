# RED Case 5 — parameter injection and clustered evidence

> baseline bundle: `91f306ef72b54dc883b52a9683629b4dff54a0f6ce985d22bd34c33e3822f1ab`
> fresh context, read-only, raw adjudication reproduced verbatim below

原始裁决：**不接受当前 `PROBLEM_RESOLVED_BY_COMPLEX_LS` 作为“四格多 SNR”正式终态；应改判 `EXECUTION_INVALID`。**

证据：

- 冻结合同声明 9/13/11/15 dB，但 [p11_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p11-pilot-efficient-butterfly-fir/p11_run.py:271) 调用 `gen_channel` 时未传 `gamma_db`；[ml_long_seq_failure.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/cma-fade-divergence/ml_long_seq_failure.py:154) 的生成器也无 SNR 参数，而是在第 165 行固定使用全局 `GAMMA_BAR`。其真相源是 [params.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/params.py:502) 的 100，即 **20 dB**。192 条 held-out 记录实际上是四种湍流/动态条件、单一 20 dB，不是 multi-SNR。
- [p11_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p11-pilot-efficient-butterfly-fir/p11_run.py:473) 按 pilot fraction 直接合并四个 cell，得到 `n=32`；四格复用同一组 8 个 seed，且场景异质，不能视作 32 个同分布独立重复。证据应以 **cell × pilot fraction 分层**为主；需要总效应时再按 seed 聚类或用分层模型。
- 1% pilot 的分层 B2−B0 BER 差为：weak `+4.83e-6`、moderate `−5.33e-6`、strong/fg30 `−5.32e-5`、strong/fg1000 `−2.19e-4`；各自 CI 上界均远低于冻结非劣界 `+0.05`。因此可保留一个较低声明：**在实际执行的固定 20 dB 四条件切片中，复杂 LS 具有局部非劣诊断信号**。这不能挽救多 SNR 正式结论。
- 还有评估人口重叠：[p11_methods.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p11-pilot-efficient-butterfly-fir/p11_methods.py:231) 的 B0 用前 50% 标签训练，而 [p11_run.py](D:/code/study/research-protocol/.worktrees/rdl-method-production-v2/projects/simulation/explore/p11-pilot-efficient-butterfly-fir/p11_run.py:243) 从 25% 位置开始计分，导致 B0 训练区占计分区三分之一；pilot 位置也未从 payload BER 中排除。这进一步限制证据为诊断级。

**论文处置：不能成为 method-bearing thesis item。** Phase C 方法未运行，传统 LS 已被认为解决问题；按 RDL 的科学终态/方法增量分离，应记 `mission_method_delta=NONE`。修复后最多沉淀为 `BASELINE_ADJUDICATION`、`BOUNDARY_RESULT` 或 `EVALUATION_INSIGHT`，不能包装成方法贡献。

**下一合法动作：**先撤回多 SNR 终态；做同包有界修复——显式传入冻结 SNR、使用与训练/pilot 不重叠的 payload 计分集、重新冻结回执，并用新的 held-out seeds 重跑。主分析按 cell 分层；只有修复后出现 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`，才可进入候选方法 Scout。
