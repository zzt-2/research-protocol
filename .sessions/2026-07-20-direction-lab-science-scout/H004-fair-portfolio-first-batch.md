# Handoff: 先扩机制全貌与 baseline 公平性，再立即运行首批

> 来源: S004 | 交接目标: 在 clean context 中完成有界 Portfolio refresh、首批准备与科学运行
> 日期: 2026-07-21

## 到哪了（状态）

S003 的 CMA/MMA raw evidence、MMA 资产和 harvest 有效，但 D006 的科学晋级已由 D007 取代：同超参数不代表公平调参，`N=32768` 未闭合约 `1e5` 收敛问题，block-end 因果和 receiver-visible recoverability 均仍是假设。C01–C04 只是同一 collapse/trace 簇，readiness 有误标；当前状态为 `DIAGNOSTIC/SLICE`，ML 尚未运行。

## 下一步干什么

1. 先做短时机制级 Portfolio refresh：复用既有 universe、历史失败、文献与资产，形成约 12–18 个候选的局部全貌，但不声称完整、不实现全池。
2. 按输出/主张分配共同系统锚点与任务专属 comparator；给予相当调参与验证机会，纠正 `READY / NEEDS_SMALL_ADAPTER / INFRASTRUCTURE_BLOCKED / HYPOTHESIS_ONLY`。
3. 随即选择 3–5 个同输出、可比较的 `READY` 候选进入一个共享 batch；若无 READY，做一次能解锁多个候选的小型 adapter sprint 后运行。检测只证明 observability；只有实际 action/correction 才能证明 PI-SER 改善。
4. 局部候选失败或阻断时自动轮换；在授权边界内完成 synthesis、harvest 和独立 verifier，不在规划/接口层提前停。

## 纪律（和下一步直接相关的约束）

- H004 是唯一续接入口；H003 的“首选 C01 直接设计/运行”已被 D007 取代。
- baseline 不追默认 SOTA，但必须正确、任务适配、来源闭环、信息公平、调参公平、收敛足以支撑有限主张。
- 公式、参数和候选方法进入实现前保留来源；候选专属全文精读与 web 由子 agent 执行。
- 不修改 B001–B003、P03、CB1 raw artifacts 或 canonical history；不创建 legacy B004；Scout 数字不自动进论文。
- 整个下一对话最多一次 consolidated commit，不 push。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| MMA 算法专属 tuning 未闭合 | 相当调参机会，不强制同参数 | OPEN | 任一 ML/新方法性能 Go 前 |
| `N=32768` 小于约 `1e5` 文献尺度 | 收敛证据匹配有限主张 | OPEN | 欠收敛解释影响候选 Go/Kill 时 |
| block-end 真因未验证 | 机制因果须有干预证据 | OPEN | 把该机制写成方法动机前 |
| C03 无真实 action/state hook | runnable 必须有可观测动作效果 | INFRASTRUCTURE_BLOCKED | 控制族进入 batch 前 |

---
## 接收方验证（续接对话时必须完成）
- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证 D007、H004、Skill D011 至少 3 条关键事实
- [ ] 已检查 `_registry.yaml` 的 depends_on / conflicts_with
- [ ] 已确认 B001–B003/P03/CB1 raw 未改且 legacy B004 不存在
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

按“恢复与扩图 → 准备并运行共享批次 → synthesis/harvest/verifier”三个宏阶段连续推进；只有战略范围变化、重大资源投入或所有合法路径耗尽时询问用户。
