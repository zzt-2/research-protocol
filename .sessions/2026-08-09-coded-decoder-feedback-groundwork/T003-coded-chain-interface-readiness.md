# Task Brief: Corrected coded-chain decoder-feedback 接口与最小 adapter readiness 审计

> 来源: S001 | 产出位置: `projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`
> 日期: 2026-08-09
> 唯一文档: 执行方只需本任务书与仓库源码

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 1
  action_class: TESTBED_READINESS_AUDIT
  mission_checkpoint: CP001
```
<!-- RDL-TASK-CONTROL:END -->

## 0. TL;DR

你在指定证据 worktree。任务是沿 corrected P08-R2 caller→callee 图核实当前 decoder API、bit/symbol mapping、外层调度、artifact/metric/receipt 能力，并给出每个候选真正需要的最小 adapter BOM 与可执行测试合同。只审计，不实现、不跑科学实验。

**产出**：写 `step-049` worker-log；聊天回 terminal、文件路径、接口结论和 hard blocker（如有）。

**最高纪律**：

1. 递归追 caller→callee；接口名或 docstring 不是运行能力证据。
2. 可以做只读 `inspect`/import/API introspection，但不得生成科学数据、改参数、改源码或跑 BER/FER。
3. 区分 decoder posterior、extrinsic、hard output、syndrome、early-stop state、iteration callback；不得互相冒充。
4. TX payload truth、true phase/CFO/h/SNR、最终 correctness 不得进入 runtime action。
5. BOM 必须是 candidate-specific 最小接口，不要求把三类接口全部建成通用平台。

## 1. 必读与检查范围

- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r2_chain.py`
- `p08r2_phaseA.py`、`p08r2_run.py`、`p08r2_verify.py`、`p08r2_metamorphic_gate.py`
- 对应 `p08r_*` 与 `p08_coded_chain.py`，只用于 lineage/差异，不恢复结论
- `projects/simulation/results/p08r2_receiver_info_repair/` 全部 contract/raw/result/receipt
- 仓库内其他 decoder/LDPC/CRC/syndrome/callback 实现，按 `rg` 定向检索
- `reference/sim-template/` 对应 config/model/verify 模板与 `code-quality.md`（只用于未来实现边界）

## 2. 要回答的问题

1. 当前 decoder 库/adapter 的真实构造参数、输入输出、内部迭代、soft-output/syndrome/callback 能力。
2. coded-bit↔interleaver↔16QAM symbol 的可逆 mapping 是否足以生成 receiver-visible soft symbols。
3. 当前 outer schedule 何时可合法调用 feedback；候选动作能否影响同帧下一轮或只能影响下一块。
4. C1/C2/C3 各自的最小 BOM、预计修改文件、新建文件、测试与 identity contract；只给边界，不写实现方案代码。
5. 必测：source identity、schema、no-feedback parity、noise-free/correct-codeword、callback lifecycle、hidden-truth metamorphic、caller→callee info boundary、raw receipt、iteration/latency/cost ledger。
6. 3–7 天预算内的 READY/NEEDS_ADAPTER/TESTBED_HARD_BLOCKER 判断；hard blocker 必须是库/API/调用链证据，不是“工作多”。

## 3. 产出格式

```markdown
# Step 049 — Coded-chain interface readiness
## Caller→callee graph
## Decoder capability matrix
| capability | actual API/behavior | evidence | status |
## Mapping and causal timing
## Candidate-specific adapter BOM
| candidate | minimal interfaces | files | tests | estimate | blocker |
## Information-boundary audit
## Existing reusable receipt/metric assets
## Hard blockers vs bounded work
## Master verification list
## Terminal
READINESS_MAPPED / TESTBED_HARD_BLOCKER / SOURCE_CONFLICT
```

## 4. 验收

- [ ] 每项 API 能力有 caller→callee `file:line` 或只读 introspection receipt。
- [ ] C1/C2/C3 BOM 分开，不扩成通用平台。
- [ ] hard blocker 与普通 3–7 天工程工作明确分开。
- [ ] 不运行科学实验、不产生 BER/FER 结论。

## 附：产出回传位置

`projects/thesis-fso/worker-logs/step-049-coded-chain-interface-readiness.md`
