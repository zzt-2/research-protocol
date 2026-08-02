# REFACTOR Case 1 — scale/action decomposition

> fresh context after the one-sentence scale-decomposition refactor; raw adjudication reproduced verbatim below

裁决：**暂不扩更多 cells/seeds；这是强烈的本地方法信号，但当前还不能直接冻结为正式 `METHOD_SIGNAL`。先修正现有冻结数据的统计裁决并补齐语义门证据。**

证据：

- 1120 行形成 7 cells × 20 fresh seeds × 8 methods 的完整唯一矩阵。
- G1 在 collapse 上相对 CMA：均值 Δ = −0.5598，CI 上界 −0.406，12 个 seed-cluster 改善、0 个恶化。
- healthy 最坏退化为 0；always-on scalars 最坏退化 +0.0156～+0.0195，超过 MDE=0.005，而 collapse 收益仅比 G1 多约 0.003～0.004。
- G1 相对 M4：Δ = −0.0355，CI 上界 −0.024。
- 原始 140 对中，G1 没有任何 ≥0.005 的实质恶化；19/20 collapse 激活，28/29 healthy 保持 identity。
- 当前 `G1_FORMAL_CONFIRM_NO_GO` 的唯一失败理由不成立：所谓“seed-cluster 修正”先给每个缺少一类的 seed 记 bacc=0.5，再对 seed 均值 bootstrap，改变了 estimand。正确做法是重采样 seed cluster，并在每轮汇总所抽 seed 的全部 pair 后重新计算 sensitivity/specificity。对冻结 CSV 的确定性复算得到 bacc=0.95776、95% CI=[0.8846, 1.0]，满足下界 >0.5。原始数据有 5 个、不是 3 个 seed 同时含两类。

但正式信号仍有两个未闭合点：

- `result.json` 的 `smoke_results` 为空；在扩大或冻结信号前，必须留下可执行证据，尤其是 hidden-truth metamorphic、参数注入、metric-information，以及 normalization action 在 invariant downstream evaluation 下的系统收益/评估器敏感性分解。
- D4 在该后 CMA 层实际返回未变的 CMA 输出，不宜作为主要 Go comparator；方法主张应明确限定为“安全 post-CMA normalization”，以 always-on robust scalar 为直接、任务匹配的廉价替代比较器。

当前 claim ceiling 仍为 `CANDIDATE/LOCAL_SLICE`：20 个 recoverable-collapse pair 仅分布于 3/7 cells，不能支持部署或广泛泛化。

下一合法动作：**只用现有冻结 raw rows 做一次有版本约束的统计/语义 receipt 修复，不新增 seed/cell、不改阈值。** 若正确 cluster bootstrap 和全部适用语义门均 PASS，则接受本地 `METHOD_SIGNAL`，进入 promotion preflight；之后才设计针对阈值边界和跨条件泛化的 Deep Evidence，而不是追加同分布 seed。若语义门失败，则保留为 diagnostic/supporting material 并轮转，不能用扩样救活。
