# Handoff: Goal 模式接管方法生产 mission

> 来源: S001（普通包由 mission-log CP 记录，T008 接收见 D002/V002） | 交接目标: 新 GPT 主控恢复 CP001–CP008，建立长期 Goal 并完成 campaign remap
> 日期: 2026-07-26
> 文件名: H002-goal-mode-campaign-recovery.md

---

## 已完成边界

T008 commit `61f8c53` 的 17 项定向工程测试通过，但正式
`KILL_NO_ADAPTIVE_WINDOW_SPACE` 已由 D002/V002 拒收：无真实 FEC crossing 却用
`dB-equiv` Kill，gate 不是合法 per-block oracle，且 evaluator/baseline 不在可靠
working region。B1 family 未关闭，但当前实现不再修。

mission 已到 CP008，八包 `method delta` 全为 NONE，判为
`DRIFTED / STALLED`。当前没有 active scientific carrier；control epoch 13 只允许
恢复、campaign remap、formal carrier 比较和下一任务准备。

## 不要做什么

- 用户只中转文件路径和极短回执；技术细节全部落盘，返回内容保持短。
- 每个执行包后先验收科学身份，再更新 mission-log；测试 PASS 不等于科学 PASS。
- 每轮重读 original mission 和 CP 全表，显式报 `method delta`、同轴/repair/
  no-method streak 与 drift；连续无方法时必须轮换或上提战略判断。
- 方法优先：允许做必要 guard，但不把纯审计、修复和 negative result 冒充方法产出。
- 不再修 T008/B1 当前实现；若未来复用 B1，必须作为新契约重建 evaluator。
- remap 前不运行新科学实验，不预先指定 C15、B1 或任何旧候选。

## 必读

1. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md`
2. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md`
3. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D002`
4. `.sessions/2026-07-23-research-direction-lab-longitudinal-test/verifications.md#V002`
5. `projects/thesis-fso/master-state.md`
6. `.sessions/_registry.yaml` 中本专题的依赖与冲突项

## 接口变更

```yaml
contracts:
  - id: C001
    type: interface-change
    description: "foreground control from B1 package to Goal campaign remap"
    location: ".sessions/2026-07-23-research-direction-lab-longitudinal-test/topic-index.md"
    change: "epoch 12/CP007/D001 -> epoch 13/CP008/D002"
    consumed_by: "next GPT master conversation"
    verification_result: PASS
    verified_by: "live V003"
```

## 失败数据附录

### T008 B1 adaptive phase-window v2

- 核心失败机制：no-crossing 时改用 proxy dB；B-cond 被冒充 oracle；B*=256
  被 `N>BLOCK=100` skip；pilot 标签与逐窗 π/2 branch resolve 污染 evaluator。
- 具体数据：data-only 20 dB QPSK clean/operational BER
  `0.173963/0.178046`，16QAM `0.271821/0.280207`；required-SNR 全 NaN。
- 已排除方向：接受 `KILL_NO_ADAPTIVE_WINDOW_SPACE`；继续开第三个 B1 修复包。
- 可复用部分：17 项工程测试、isolated source、seed census、错误模式与 defensive
  evaluator lesson；不得复用 Kill 数字作论文结论。

### 整体 mission

- CP001–CP008 方法增量均为 NONE；T003/T004/T006/T007/T008 均出现“测试或
  provenance 很完整，但科学身份不成立”的模式。
- 这证明当前协议会守流程，但尚未证明能生产方法；Goal 模式必须以 METHOD_SIGNAL/
  PROMOTION_READY 为终点，而不是以连续完成 T 为终点。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| 无 active formal carrier | 科学包必须绑定合法 Step 与 owner | 等待 campaign remap | 下一 T 前必须解决 |
| 八包无方法增量 | mission 要积累可用方法材料 | DRIFTED/STALLED | remap 必须比较至少 3 个合法方案或证明不足 3 个 |
| T008 ignored artifacts | formal 数字需可移植 raw/manifest/hash | raw 只在本地 results/ | 未来若复用任何 T008 数字前必须重跑并入证据闭包 |

## 验证阈值

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|---|---|---|---|
| campaign recovery | epoch=13、CP008、D002、无 active carrier 四项一致 | D002/V002 | 待新对话验证 |
| remap | 至少比较 3 个合法 carrier；不足 3 个则逐项证明 formal 不合法 | RDL method-production | 待验证 |
| 下一包方法导向 | 写清正向构造、fair comparator、包装句、失败后轮换点 | method-production v2 | T008 形式满足、科学未满足 |
| scientific acceptance | independent critic + raw 可复核 + identity/working region 全闭合 | D002/V002 | T008 FAIL |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落
- [ ] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：control 为 epoch 13 / CP008 / D002 → [PASS/FAIL + 文件证据]
  - 声称2：T008 formal disposition 为 `BLOCKED_IDENTITY`，非 Kill → [PASS/FAIL + 文件证据]
  - 声称3：master-state 当前无 active carrier → [PASS/FAIL + 文件证据]
- [ ] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with
- [ ] 已确认当前范围未违反“明确不含”

## 下一轮

1. 完成接收方验证。
2. 建立长期 Goal：持续形成科学合法、可包装的毕业论文方法材料，直到取得
   `METHOD_SIGNAL/PROMOTION_READY` 或出现需要用户授权的真实战略阻塞。
3. 比较所有仍合法 carrier 的 formal readiness、方法形态、预期增量、最小补债
   成本和可包装性。至少比较三个；不足三个则逐项证明不合法。
4. remap 必须回答“为什么该包比另外至少两个合法替代项更可能产生
   METHOD_SIGNAL”，再更新 control/formal owner 并准备下一 T。
