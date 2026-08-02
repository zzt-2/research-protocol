# GREEN Case 1 — scale/action

> fresh context, read-only, raw adjudication reproduced verbatim below

formal_science_disposition: `G1_FORMAL_CONFIRM_NO_GO`
mission_method_delta: `NONE`

决策：既不扩大同一包的 cells/seeds，也不接受为 `METHOD_SIGNAL`；仅保留为 `CANDIDATE/LOCAL_SLICE` 的诊断性机制信号。

证据：

- 7 cells × 20 fresh seeds = 140 pairs；合同、方法和运行脚本哈希与 `result.json` 全部匹配。
- 机制效应强：collapse 相对 CMA 的 PI-SER Δ = −0.5598，95% CI [−0.6947, −0.4064]；healthy worst-pair Δ = 0；66/66 identity 分支与基线完全一致；19/20 collapse 激活、1/29 healthy 误激活。
- 但预注册 Gate 6 绑定 seed-cluster：正确 CI 为 [0.50, 0.6579]，下限不满足严格 `>0.5`；仅 3/19 seeds 同时含 healthy 与 collapse。点 precision/recall = 0.95/0.95 不能覆盖该失败。
- 合同明确规定任一 B4 gate 失败即 No-Go，禁止通过改 cells、增 seed、选 seed 子集或降低阈值救活；因此追加规模属于事后救援。
- `result.json.smoke_results` 为空，未持久化 RDL 要求的可执行语义门控记录，现有允许证据不足以授权 scale 或冻结信号。
- D4 不能补足对手证据：其 apply 路径直接返回 post-CMA 输入；原始 140/140 对的 PI-SER 与 CMA 完全相同，未实际执行 D4 的 tap-update 轨迹。因此它至多说明层级不匹配，不能作为充分的任务匹配竞争对手。
- always-on scalars 在 collapse 仅比 G1 好约 0.003–0.004，但 healthy worst degradation 为 +0.0156 至 +0.0195，超过 MDE 0.005；这支持“门控安全价值”，不推翻正式 No-Go。

任何未来重新进入 scale 前必须作为全新、显式授权且预注册的工作线完成：

1. 持久化所有适用 executable semantic gates，尤其 hidden-truth metamorphic、metric-information、real-action/cost。
2. 事前设计能在 seed-cluster 单位上识别分类性能的代表性覆盖，不能沿用本包后补样本。
3. 实际运行一个同层、同信息、可独立调优的传统门控 AGC/归一化对手；D4 identity 路径不够。
4. 冻结阈值、estimand、比较器和退出规则后再取新数据。

下一合法动作：将 G1 收为 `SUPPORTING_MATERIAL`（安全门控机制与统计设计边界），停止该包扩展，轮转/重映射到最佳合法 READY 方法候选。
