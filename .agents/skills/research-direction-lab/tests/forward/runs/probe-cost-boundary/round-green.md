# GREEN fresh-agent run — probe-cost-boundary

- agent_id: `green_probe_fresh` (collaboration canonical task `/root/green_probe_fresh`)
- skill_access: current revised Skill loaded before response
- recording: verbatim final response

## Blind prompt

某候选函数刚实现；唯一问题是“输出是否随一个合法输入变化”。现有一个小输入，最多允许一次 paired-input 对照，预算约两分钟；不要运行 11 cells × 10 seeds；结果不用于论文或正式晋级。请说明：工作强度、具体动作、默认产物、结论上限、harvest 处理、何时停止或升级。只给你的实际回答，不修改文件，不描述评分标准。

## Raw response

这是一个 **Probe**，不是 Scout 或 Deep Evidence。

- **工作强度**：只验证一个前置语义假设——候选函数是否对合法输入变化敏感。预算冻结为约两分钟、最多一组 paired-input；不运行 11 cells × 10 seeds，不调参，也不建立正式证据链。

- **具体动作**：预先写明假设与否决条件；构造两个合法输入，仅改变一个按机制应影响输出的维度，其余条件固定；各执行一次，确认调用的是同一函数与配置，并直接比较输出。若函数含随机性，导致一次配对无法归因，则记为 `UNRESOLVED`，不擅自追加 seeds。

- **默认产物**：一个紧凑的 Probe record，包含 `question | hypothesis | falsifier | budget | legal information | comparator | semantic checks | result | evidence pointer | next disposition`；可附很小的输入、输出或 diff artifact。默认不创建 batch manifest、receipt、独立 verifier、synthesis 或 harvest ledger item。

- **结论上限**：`DIAGNOSTIC`，证据范围最多为本次 `RUN`。PASS 只能说明“在这一合法输入对上观察到输出变化”，不能称为方法信号、稳健性、泛化性或正式晋级依据。若相同输出命中预先规定的否决条件，则为 FAIL；若该输入对在合法机制下本就可能输出相同，则只能是 `UNRESOLVED`，不能推断函数对所有输入恒定。

- **Harvest**：必须评估，但通常只在 Probe record 中填写 `no_durable_harvest_reason`，不制造 ledger item。只有该测试后来成为真正可复用的测试资产，或揭示了可持久复用的明确失败机制，才分别考虑 `REUSABLE_ASSET` 或 `FAILURE_MECHANISM`。单次 PASS 不是 `METHOD_SIGNAL`。

- **停止或升级**：完成唯一配对、达到两分钟预算、取得足以回答问题的 PASS/FAIL，或因随机性、比较语义不清得到 `UNRESOLVED` 时立即停止。只有 Probe PASS 且下一问题确实需要考察小范围稳定性或科学信息价值时，才另行决定是否升级到 Scout；只有稳定且与论文边界或贡献相关的信号，才考虑 Deep Evidence。

## Behavior scorer output

Post-hoc scorer verdict: PASS. All Probe cost, scope, harvest, and stop checks passed.
