# RED fresh-agent control — semantic-integrity-separation

- agent_id: `red_semantic_fresh2` (collaboration canonical task `/root/red_semantic_fresh2`)
- skill_access: explicitly denied
- recording: verbatim final response

## Blind prompt

一个 learned corrector 批次的 source hash、seed、artifact 与 deterministic rerun 全 PASS，但实现训练的是输出到 soft-assigned constellation points 的自洽距离，不是声明的 hard-label MSE；两个候选都收敛到几乎常量输出，PI-SER 约 0.93。现在决定是否把候选/方法族判负，或继续加 seeds/models/hyperparameters。请说明证据如何分类、claim ceiling、扩算力前的最小检查、下一动作、harvest 处理。你不能读取 research-direction-lab Skill 或其 references。只给你的实际回答，不修改文件，不描述评分标准。

## Raw response

事实与证据分类：

- source hash、seed、artifact、deterministic rerun 全 PASS：属于**谱系完整性与执行可复现性证据**。它证明“同一份错误实现能稳定复现”，不证明实验测到了声明的方法。
- 实际优化 soft-assigned constellation points 的自洽距离，而非 hard-label MSE：属于**语义一致性 FAIL / 实验契约违约**，是阻断性证据。
- 两个候选几乎常量输出、PI-SER≈0.93：属于**实际实现的性能失败证据**，并提示自洽目标存在塌缩解；但不能外推到声明的 hard-label 方法族。

Claim ceiling：

> 可以声称：该批次在 provenance 层面可复现；当前 soft self-consistency 实现稳定塌缩并表现失败。
> 不可以声称：hard-label learned corrector 候选失败、方法族失败，或增加 seeds/models/hyperparameters 也无效。

因此，不能据此判负声明中的候选或方法族；这批结果应视为**不构成该 claim 的有效评估**。也不应继续扩算力，因为更多 seed 只会提高错误目标下失败现象的复现置信度。

扩算力前的最小检查：

1. 用一个手工构造的小 batch，逐样本核对训练 target 确为 hard label，loss 数值与独立计算的 hard-label MSE 完全一致。
2. 检查 label、样本、输出索引对齐，以及梯度确实由 hard label 驱动。
3. 做 tiny-batch overfit：模型应能把 hard-label MSE 压到接近零，并显著优于“输出常量/均值”的退化基线。
4. 检查输出方差、类别条件输出差异；若仍近常量，先诊断训练管道，不扩 seed 或模型数。

下一动作：立即冻结当前批次的候选排名与方法族判断；修正目标函数并通过上述语义 smoke test，然后只对一个候选、一个固定 seed 做最小重跑。最小重跑能学习非恒定映射且明显改善 PI-SER 后，才恢复原定 seeds/models/hyperparameters 扩展；否则按训练管道或架构失败继续定位。

Harvest 处理：

- 保留 source hash、seed、artifact、rerun 结果，标记为“provenance PASS、semantic validity FAIL、不可用于方法 claim”。
- 收获为失败模式：**soft-assignment 自洽目标允许近常量塌缩，确定性复现不能替代目标语义验证**。
- PI-SER≈0.93 可进入负面诊断档案，但不得进入候选排行榜、方法族证据汇总或 Go/Kill 统计。
- 修正后的实验应建立新批次身份，不能覆盖或把旧批次追认成 hard-label 实验。

## Behavior scorer output

Post-hoc scorer verdict: FAIL (control/partial RED). General reasoning caught the main mismatch, but the reusable no-op/identity check and explicit current-harvest disposition/no-durable branch were absent.
