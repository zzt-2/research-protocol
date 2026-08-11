# Handoff: K2/K3 入口轮换无 survivor

> 来源: S001（2026-08-11 续接，R003/D005–D006）| 交接目标: 保持 dormant，等待新的 candidate source / research object 授权
> 日期: 2026-08-11

---

## 到哪了（状态）

K1/Q001 仍是可恢复的 `EVIDENCE_BLOCKED`，不是 scientific failure；K4 syndrome 早停继续 exact collision。自动轮换只重裁 K2/K3，结果均未通过入口门，terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_SHORTAGE`。没有新建 Groundwork 专题，也没有执行 Step 1、下载、实现或仿真；`mission_method_delta=NONE`。

## 已完成边界

只完成 K2/K3 的 entry re-adjudication、证据恢复和治理收口；未进入任何新的 Groundwork 科学步骤。

## 不要做什么

不自动续 K1/K2/K3/K4，不把 entry rejection 写成 scientific Kill，不为填补章节槽位创建第三张弱卡。

## 必读

1. `topic-index.md` 的不变量、当前位置与 D005 scope change。
2. `R003-k2-k3-entry-readjudication.md` 的动作签名、门表和证据强度边界。
3. `decisions.md` D005–D006；当前独立验收状态见 topic-index，不把尚未存在的编号列为接收依赖。

## 下一步干什么

当前没有自动科学动作。只有主控/用户提供新的 candidate source 或不同 research object，并同时满足 task-matched 2019+ reference、published defect、一个完整 action、strongest cheap comparator 已闭合，才可用新的 scope-change 重新做入口裁决。

## 纪律（续接者必须注意的）

- 不把 K2 的 published suffix pollution 直接等同于“三假设 tracker 是方法”；order-2/3 mixture tracker 是高风险强邻居，但 task/target 不同，不能声称 exact collision 或已完全吸收。
- 不把 JP-V&V 的 joint gain 改写成“fixed JP 在 reliability 异质时已证明失败”；原文反而报告 fixed coupling 可 near-optimal。
- 不为填补 Ch4 槽位制造第三张弱卡；K1、K4、coded C1、P1/C3/AMC、fixed-point/selector 旧轴均不得自动重开。
- 入口拒绝不计 research-object scientific failure；K2/K3 family 没有被实验 Kill。

## 失败数据附录

### K2 三假设 phase-unwrapping

- 核心失败机制：动作未唯一化，且三阶 mixture/sequence tracker 已覆盖多轨迹、likelihood、merge/prune 与 confidence/reacquisition，形成未闭合的高风险强邻居。
- 具体门：E4/E5=`UNRESOLVED`，E6=`UNRESOLVED_HIGH_RISK`，E7=`FAIL`，E8 预计 `5–9 天`。
- 可复用部分：TSP 2022 对 suffix pollution 的 published defect 与 defect-only smoke 参数形状。

### K3 可靠度 JP-BPS

- 核心失败机制：task-matched published defect 缺失；固定 JP 是强 cheap comparator，Weighted/RW-BPS/unequal-SNR CPR 只形成待全文闭合的 collision debt。
- 具体门：E1=`PASS_WITH_RECENCY_DEBT`，E2=`FAIL`，E6=`UNRESOLVED_HIGH_RISK`；只有 E4/E5/E8 的形状可成立。
- 可复用部分：双偏振 BPS caller、固定 JP comparator 与 reliability-imbalance smoke 形状。

## 接口变更（如有代码改动）

无。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| K1 bearing primary fulltext | exact action 应由一手证据闭合 | `EVIDENCE_BLOCKED` | 获得新的 bearing primary fulltext 或等价一手证据 |
| K2 absorption | 不以相似动作冒充 exact collision | `UNRESOLVED_HIGH_RISK` | task-matched primary 给出同 input-trigger-action-output |
| K3 collision debt | direct prior 必须有一手全文动作签名 | metadata/二手线索 | 获得 Weighted/RW-BPS/unequal-SNR CPR 一手全文并逐字段比较 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| 入口 survivor | E1–E8 全部通过，且 strongest cheap alternative 未吸收完整 action | D001/D003 + 本轮 delegation | K2/K3：0/2 |

## 下一轮

无自动下一轮。等待新的 candidate source 或不同 research object 的显式授权。

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：K2 的 suffix pollution 是 published defect，但 K2 action 仍面对未闭合的 strongest-cheap-alternative 高风险强邻居 → [PASS/FAIL + R003/primary]
  - 声称2：K3 没有 task-matched published fixed-JP failure → [PASS/FAIL + R003/primary]
  - 声称3：没有新 GW 专题或 Step 1 产物 → [PASS/FAIL + registry/Git]
- [ ] 已检查 _registry.yaml 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”
