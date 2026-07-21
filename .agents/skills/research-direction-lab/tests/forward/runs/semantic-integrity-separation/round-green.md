# GREEN fresh-agent run — semantic-integrity-separation

- agent_id: `green_semantic_fresh2` (collaboration canonical task `/root/green_semantic_fresh2`)
- skill_access: current revised Skill loaded before response
- recording: verbatim final response

## Blind prompt

一个 learned corrector 批次的 source hash、seed、artifact 与 deterministic rerun 全 PASS，但实现训练的是输出到 soft-assigned constellation points 的自洽距离，不是声明的 hard-label MSE；两个候选都收敛到几乎常量输出，PI-SER 约 0.93。现在决定是否把候选/方法族判负，或继续加 seeds/models/hyperparameters。请说明证据如何分类、claim ceiling、扩算力前的最小检查、下一动作、harvest 处理。只给你的实际回答，不修改文件，不描述评分标准。

## Raw response

事实与判定：

- source hash、seed、artifact、deterministic rerun 全 PASS，只证明执行身份、来源和复现完整性。
- 实际 loss 是“输出到 soft-assigned constellation points 的自洽距离”，与声明的 hard-label MSE 不同；因此语义烟测 FAIL。
- 两个候选近常量输出、PI-SER≈0.93 是有效执行事实，但仍存在更便宜的实现语义解释：目标函数允许或诱导输入无关退化。
- 当前证据应分类为 `implementation-confounded`；候选仍是 `UNRESOLVED`。不能判负候选，更不能判负方法族，也不应继续加 seeds/models/hyperparameters。

Claim ceiling：

- 最高只能到 `RUN/CELL`：在已执行配置及错误的实际训练 contract 下，两个实现发生近常量塌缩并得到 PI-SER≈0.93。
- 不能提升到 `CANDIDATE` 或 `FAMILY`；更不能表述为“learned corrector 无效”。
- deterministic integrity PASS 不能提高科学 claim ceiling。

扩算力前的最小检查：

1. 逐项核对 objective、label、output、最终 PI-SER 是否对应同一任务，并确认 hard label 真正进入 loss 与梯度。
2. 检查常量/平凡输出是否能低成本满足当前 loss；必要时用解析计算或受控常量输出直接验证。
3. 修正为声明的 hard-label MSE 后，在极小样本上做 overfit smoke。
4. 检查输出方差、星座占用/支持集与输入敏感性，要求非退化。
5. 验证 no-op/identity 路径和最简单合法 comparator 可复现。

下一动作：

先做一个有明确预算的 bounded semantic Probe：修正 loss，并选一个代表候选完成上述 smoke。若仍失败，继续定位任务/实现，不扩算力；若 PASS，只授权一个小型 Scout，先以极少 seeds 对两个候选重跑，观察是否出现机制相关结构。只有结构稳定且便宜替代解释被排除后，才扩 seeds、models 或调参。原错误 contract 可保留为退化对照，不应继续当正式候选训练。

Harvest：

- 保留原始 artifact、hash、receipt、PI-SER≈0.93 和近常量诊断，维持 lineage；任何基于这些结果形成的候选/方法负结论应标为 `invalidated` 或由纠正项 `amended`，不能删除。
- 当前不能登记 `LOCAL_NEGATIVE`、`METHOD_SIGNAL` 或 family negative。
- 若额外验证证明该自洽 soft objective 确实允许输入无关塌缩，可登记 `FAILURE_MECHANISM` 或 `EVALUATION_INSIGHT`，claim ceiling 仍限于该训练 contract。
- 若把语义 smoke 固化为可复用回归测试，可另登记 `REUSABLE_ASSET`；否则记录 `no_durable_harvest_reason`，不要为了有产出而制造 harvest。

## Behavior scorer output

Post-hoc scorer verdict: PASS. All integrity/semantics separation, minimum-smoke, claim-scope, next-action, and harvest checks passed.
