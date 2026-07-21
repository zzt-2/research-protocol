# Direction Lab Probe 与恢复体系设计

## 目标

让 Research Direction Lab 能在稳固地基上长期、批量寻找毕业论文方向，同时避免两类已复现失效：小问题自动膨胀成完整证据工程；完整可复现链掩盖目标函数或任务语义错误。

## 设计取舍

采用“Skill-first、轻代码守门、单一当前视图”。不建立通用 scheduler，不用固定候选数证明完整，不把通信算法、公式、参数或阈值写进通用 Skill。项目 Adapter 持有当前事实和预算；领域 Profile 持有稳定惯例；Skill 做开放判断；代码只归约显式状态、校验来源和渲染视图。

被拒方案：

- 所有工作统一走完整 batch：已导致秒级实验配套长时间治理。
- 只靠自由文本日志恢复：旧 handoff、旧 synthesis 和修订结论会竞争事实源。
- 把科学判断写进状态机：会重新制造 Portfolio Autopilot 的复杂度和僵化。
- 删除旧结论减负：破坏审计与教训复用。

## 三层工作强度

### Probe

Probe 只回答一个使后续工作成立的窄问题，例如输入是否影响输出、目标是否存在平凡解、接口是否携带所需信息、baseline 是否出现可测 headroom。

- 预算由项目 Adapter 声明；超预算前必须停下并决定升级、改问法或轮转。
- 默认只创建 `probes/<id>/record.yaml`，可选一个 `artifacts/`；不默认创建 receipt、独立 verifier、synthesis、session note 或 harvest item。
- claim ceiling 不高于 `DIAGNOSTIC`。
- 结果为 `PASS | FAIL | UNRESOLVED`，并记录问题、最小证据、预算使用、语义检查、下一处置。
- Probe PASS 只表示“值得进入 Scout”，不是方法阳性。

进入任何规模扩张前，按适用性检查：目标/标签/最终指标对齐；平凡或常数解；no-op/identity；输出方差与支持集/占用；单样本过拟合；最简单合法 comparator；因果与信息边界。`N/A` 必须写理由。具体公式和阈值由项目持有。

### Scout

Scout 是小型、多候选、共享问题的批量比较。它使用共同系统锚点和任务专属 comparator，冻结信息、调参、指标、退出条件与有限 scope。Scout 才需要 batch manifest、可复现 artifact、synthesis；只有完整性风险实际存在时才启用 receipt 或独立 verifier。

### Deep Evidence

只有跨 seed/slice 稳定、机制解释未被廉价替代解释推翻，或论文价值明确的边界/负面结果进入 Deep Evidence。此层才默认要求完整 provenance、统计计划、独立科学 critic、receipt/verifier 和论文晋级材料。

## 晋级与轮转

Probe → Scout 必须同时满足：语义门通过；问题仍存在于合法 baseline/comparator；存在可执行的候选或可辨别的机制问题；扩大预算的预期信息价值合理。

Scout → Deep Evidence 必须满足：主指标或机制诊断稳定；替代解释已受检；claim ceiling 明确；能进入论文主线、边界分析或重要负面材料。

任一层的局部阻断不终止 campaign。存在 READY 工作时自动换候选/机制族；共享基础设施只有在解锁多个高价值比较时才投入。

## 当前视图与历史血缘

恢复顺序固定为：

1. `STATUS.md`：唯一日常入口。
2. `state/current.yaml`：唯一机器当前态，含授权、anchor、当前有效结论、失效/撤回摘要、下一动作。
3. `portfolio/current.yaml` 与 `harvest/current.yaml`：当前可消费视图。
4. 只有出现冲突、审计或当前决策需要时，才读 events、ledger、旧 synthesis 和 session 历史。

`mtime`、文件长度、最近格式修改和旧 handoff 都不决定当前态。显式的 `amends / supersedes / invalidates / restores` disposition 决定 current projection。历史 append-only 保留；旧条目不删除，但不得进入当前论文消费视图。

## 文件组织

```text
direction-lab/
├── STATUS.md
├── project.yaml
├── state/
│   ├── events.jsonl
│   └── current.yaml
├── portfolio/
│   ├── current.yaml
│   └── history/
├── probes/
│   └── <probe-id>/
│       ├── record.yaml
│       └── artifacts/          # 可选
├── batches/
│   └── <batch-id>/             # Scout / Deep Evidence
├── harvest/
│   ├── ledger.jsonl
│   ├── current.yaml
│   └── thesis-spines.md
├── registries/
├── tools/
├── tests/
└── archive/
```

热路径只有 STATUS、project、current state、current portfolio、current harvest。禁止 per-cell prose；raw data 留 artifacts；旧 portfolio 进 history；大 artifact 只存指针和 hash。`.sessions/` 只记录用户原话、战略决策、关键失败和跨对话 handoff，不承载每个 Probe 的运行日志。

## Harvest 规则

每轮必须评估是否有 durable harvest，但不强制制造条目。没有可复用价值时，在 Probe/Scout record 写 `no_durable_harvest_reason`。ledger 保存全血缘；current 只显示 active/diagnostic 且可消费的条目。修订可分别处置科学解释、raw 数值和资产，不能整批一起删除或继续 active。

## 验证场景

至少覆盖：两分钟 Probe 不膨胀；完整 integrity PASS 但目标退化时不得下机制负面；旧 CLOSED 后被 INVALIDATED 时 current 恢复 UNRESOLVED；局部 blocker 不停止仍有 READY 工作的窗口；harvest 科学解释撤回但 raw/asset 分别保留；三分钟恢复不考古全部历史。

## 完成标准

- 旧 Skill 在 RED 场景留下可复核失败记录。
- Skill/reference 以最小改动落实三层、语义门、current precedence 和抗膨胀规则。
- 通用 core 无项目/通信语义。
- 项目结构测试、历史测试、forward tests 与 fresh-agent 恢复演练通过。
- repo Skill 与全局消费者 Skill 字节一致。
- 最终提供可直接启动长期 campaign 的提示词。
