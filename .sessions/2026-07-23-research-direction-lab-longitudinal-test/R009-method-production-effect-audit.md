# [R009] T001–T026 长程方法生产效果审计

> 2026-07-29 | 关联：2026-07-23-research-direction-lab-longitudinal-test / system D019

## 调研问题

轻量长程协议在真实运行中是否同时实现了低用户负担、压缩恢复、有效轮换、可控治理成本和毕业方法生产；T019 方法工厂是否带来实质改善。

## 发现

### 两阶段量化

| 指标 | CP001–CP017 | T019–T026 |
|---|---:|---:|
| 工作包 | 17 accepted checkpoints | 8 个执行包；T026 在本审计中接收为 CP025 |
| 非 `NONE` 方法增量 | 0/17 | 4/8；另有 1 个 `WRITING_MATERIAL` artifact |
| `METHOD_SIGNAL` | 0 | 2 |
| signal→active/formal carrier | 不适用 | 0/2 |
| 纯治理/接口包 | 2/17 | 0/8 |
| formalization/adjudication | 至少 7 个连续候选形式化包 | T021–T024，4/8 |
| 结果 | 连续 17 包无方法增量 | 1 个 bounded asset + 写作材料，仍无正式方法 |

CP001–CP017 的候选轮换在形式上发生，但多数只是从一个 formal-readiness、identity 或 search blocker 换到另一个 blocker。目标文字始终存在，动作策略却连续处于 drift/stall；问题不是单纯忘记状态，而是没有把“下一动作是否产方法”变成恢复后的路由判断。

T019–T020 的工厂在第 2 包产生首个诊断信号。真正有效的不是固定构造数量，而是当前 tuned comparator、严格因果信息边界、fresh held-out、同包 semantic smoke 和 fair comparison。T021–T024 又用 4 包完成正式化与审判，两个诊断 signal 最终均未转成 active carrier，说明当前主要瓶颈已从“找不到构造”变为“signal 转化链过长且 readiness 债务暴露过晚”。

### 长程与用户负担

- 用户不需要读取技术日志或判断科学正确性，低负担目标基本实现。
- control、原始 mission 和完整 mission-log 在长跑中未丢；但真实压缩恢复的耗时、读取文件数和 lane/gate 一致性从未量化。
- 三层记录有效，但 `topic-index.md` 已膨胀为 package history，违背“小型当前快照”职责。
- `formal_science_disposition` 与 `mission_method_delta` 分账有效，阻止了把流程 PASS、局部信号和包装材料冒充正式方法。

### 论文价值

G1 是有实质的次级资产，不是主贡献。方法段、公式和局部结果可复用，流程图与结果图可继续加工；但它与当前论文主线尚未融合，缺 novelty/direct-comparator closure，最佳位置是高阶调制扩展、discussion、附录或未来工作。`PACKAGING_BOUNDARY` 和 `WRITING_MATERIAL` 不能替代 formal promotion。

## 结论

体系值得保留，但只能判定为“稳定的研究操作系统 + 有效的诊断方法发现器”，尚未证明是毕业方法生产线。旧阶段方法生产率为 0；T019 后近端生产率实质改善；端到端 formal-method yield 仍为 0/2。

最小修订只有三项：

1. `READY=0 / NEEDS_SMALL_ADAPTER=0` 且无 active carrier 时，把方法工厂/战略 gate 变成硬路由，不再串行 formalize hypothesis-only candidate。
2. accepted `METHOD_SIGNAL` 后先做一次 promotion preflight；只在 thesis fit、collision/source、comparator、estimand 和 closure budget 可闭合时进入一个有界 formal workline。
3. 只在真实压缩、fork 或主控替换时记录极简 recovery receipt；不向普通包增加治理项。

下一轮只有在至少一个 accepted `METHOD_SIGNAL` 完成 Step 1–3/3.5/4a、成为 active carrier 或 `PROMOTION_READY` 并建立当前论文接口时，才判“能产毕业方法”。仅到包装或写作材料，方法发现 PASS、毕业方法生产 FAIL。

## 对决策的影响

支持 system D019 对 RDL Skill 做上述最小修订；支持 live D034 接收 T026、压缩 current snapshot，并在修订终验前停止 T027。既有科学结论、G1 claim ceiling 和 protected history 不变。
