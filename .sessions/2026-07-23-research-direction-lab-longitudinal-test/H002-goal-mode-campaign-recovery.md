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

- [x] 已读取 topic-index 的不变量段落
- [x] 已验证本文件中的至少 3 条关键事实声称
  - 声称1：control 为 epoch 13 / CP008 / D002 → **PASS（交接时点）**：
    `verifications.md#V003` 独立终验记录 live
    `epoch=13 / CP008 / authority=D002`；该状态后来按决策血缘合法演进为
    epoch 21 / CP009 / formal D020，不把历史 checkpoint 冒充当前状态。
  - 声称2：T008 formal disposition 为 `BLOCKED_IDENTITY`，非 Kill →
    **PASS**：`verifications.md#V002` 结论为
    `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`，明确拒收
    `KILL_NO_ADAPTIVE_WINDOW_SPACE`。
  - 声称3：master-state 当前无 active carrier → **PASS（交接时点）**：
    `verifications.md#V003` 记录 formal D014 / no active carrier；该事实后来由
    R001/D003、R002/D006 和 D009/formal D020 的合法 carrier 激活血缘取代，
    当前 active carrier 为 B10。
- [x] 已检查 `_registry.yaml` 中本专题的 depends_on 和 conflicts_with：
  depends_on 的 `2026-07-20-research-direction-lab-system` 为 active，
  `conflicts_with=[]`。
- [x] 已确认当前范围未违反“明确不含”：恢复与 C1 direct tests 均止于
  GW Step 4a；未运行 C2/held-out、未恢复 Scout/P03、未修改 Skill/common/params
  或旧 T006/T008/T009。
- [x] 已核对接口变更 C001：`verifications.md#V003` 证明
  epoch 12/CP007/D001 → epoch 13/CP008/D002 的历史切换；后续 epoch 14–21
  由显式 D/V 血缘继续演进。
- [x] 已核对并行依赖：当前 C1 executor 已停止，独立 reviewer 已返回
  `C1_ACCEPTED_AWAITING_CONTROL`；C2 仍由 foreground control 阻断，未提前执行。

## 下一轮

1. 完成接收方验证。
2. 建立长期 Goal：持续形成科学合法、可包装的毕业论文方法材料，直到取得
   `METHOD_SIGNAL/PROMOTION_READY` 或出现需要用户授权的真实战略阻塞。
3. 比较所有仍合法 carrier 的 formal readiness、方法形态、预期增量、最小补债
   成本和可包装性。至少比较三个；不足三个则逐项证明不合法。
4. remap 必须回答“为什么该包比另外至少两个合法替代项更可能产生
   METHOD_SIGNAL”，再更新 control/formal owner 并准备下一 T。

## Goal 续接接收方复核（2026-07-26，CP010）

- [x] 已重新读取 topic-index 的不变量、当前范围与明确不含。
- [x] 已从磁盘重新验证至少 3 条当前事实：
  - 当前 control 为 epoch 24 / CP010 / authority formal D022 → **PASS**：
    live `topic-index.md` 控制块与 formal `decisions.md#D022` 一致。
  - T010 为 `BLOCKED_IDENTITY / mission_method_delta=NONE` → **PASS**：
    `verifications.md#V026`、worker-log 与 synthesis 一致；raw 实际 840 rows，
    strict-prefix，17/17 SHA256 匹配，last/next key 为
    `[1,0,2,5,2]` / `[1,0,3,0,0]`，无 aggregate，held-out=false。
  - 当前无 active scientific carrier，C15 只允许 Step 1–3 formalization →
    **PASS**：live D011、formal D022、master-state 与 current projections 一致。
- [x] 已检查 `_registry.yaml`：本专题 depends_on
  `2026-07-20-research-direction-lab-system`（active），`conflicts_with=[]`；
  formal owner 的依赖项均存在，未发现冲突。
- [x] 已确认未违反“明确不含”：本次只做恢复、只读复核与控制面协调；未运行
  新 seed/MVE/held-out，未修 T006/T008/T009/T010，未恢复 Scout/P03，未修改
  Skill/common/params。

## Goal 续接接收方复核（2026-07-27，CP016）

- [x] 已重新读取 live topic-index 的不变量、当前范围、明确不含和前台 control。
- [x] 已从磁盘独立验证至少 3 条当前事实：
  - 当前 control 为 epoch 41 / CP016 / authority formal D032 → **PASS**：
    live `topic-index.md`、formal `decisions.md#D032`、`master-state.md`、
    `state/current.yaml` 与 `portfolio/current.yaml` 一致。
  - T016 正式处置为
    `BLOCKED_FORMAL_READINESS / BLOCKED_IDENTITY_CONFLICT` 且
    `mission_method_delta=NONE` → **PASS**：live `verifications.md#V047`、
    formal D032 与 step-016 worker log 一致；candidate 与 worker-log SHA256
    分别为 `177e20384...e6acd39`、`57f2e051...e41fd34b`。
  - 当前无 active scientific carrier，C15 不得第二个 source/formalization
    package → **PASS**：formal D032、live D021、portfolio/current 与
    master-state 均明确 `NO_ACTIVE_SCIENTIFIC_CARRIER`；仓库中无 T017、
    C15 Phase B、Step 3 或 MVE 后继产物。
- [x] 已检查 `_registry.yaml`：本专题 depends_on
  `2026-07-20-research-direction-lab-system`（active），`conflicts_with=[]`；
  依赖专题产出路径存在。
- [x] 已确认当前范围未违反“明确不含”：恢复期间 git worktree clean，未运行
  新 seed/MVE/held-out，未修 T008/B1 或 T016/C15，未恢复 Scout/P03，未修改
  Skill/common/params。
- [x] 已核对 session inflation：本专题仅 `S001` 一个 session note，无膨胀阻断。

## Goal 激活后接收方复核（2026-07-27，CP017 / epoch45）

- [x] 已重新读取 live topic-index 的原始目标、当前范围、明确不含、不变量、
  foreground control，并完整读取 mission-log CP001–CP017。
- [x] 已从磁盘独立验证至少 3 条当前事实：
  - T017 正式处置仍为
    `BLOCKED_FORMAL_READINESS / BLOCKED_SEARCH_OR_IDENTITY`、
    `mission_method_delta=NONE` → **PASS**：V049、D023/D034、worker log
    一致；candidate 与 worker-log SHA256 分别为
    `2d167ec74759a2f460b923cbf516e627a18003843f47729f5689d5a1da20e2d8`
    和
    `0fc319ac0f61043d8858cf21978bae66bd8faa5779d7a11272957dab168b57d0`。
  - 当前无 active scientific carrier，且没有 step-018 worker、Q14 Step 4a/MVE
    或 C16 Phase-B 后继产物 → **PASS**：portfolio/current 的
    `formal_active_carrier.id=NONE`；受控 T018 存在但未执行。
  - R008/D024/D035 的 Q14 选择不是 active carrier 或方法增量 →
    **PASS**：四候选 readiness 均为 HYPOTHESIS_ONLY，T018 固定 delta NONE；
    V050 初审为 `FAIL / P0/P1/P2=1/5/1`，未运行检索或实验。
  - V050 暴露的 current projection 不一致已完成 bounded reconciliation →
    **PASS**：D025/formal D036、epoch45/CP017、formal topic-index“当前位置”、
    registry、state/portfolio/harvest、master-state 与 projects-overview 已协调；
    task-control validator PASS、四个 YAML `safe_load` PASS、`git diff --check`
    无 whitespace error。
- [x] 已检查 `_registry.yaml`：本专题 depends_on
  `2026-07-20-research-direction-lab-system`（active），`conflicts_with=[]`；
  依赖专题与 produces 路径存在。
- [x] 已确认当前范围未违反“明确不含”：恢复与修订只涉及 owner/control/task/
  current projections；未运行检索、下载、精读、Step 4a、实现、
  simulation/Probe/MVE/seed，未修任何既有 no-repair workline。
- [x] 已核对接口与并行依赖：T017 executor/验收均已终止；T018 初版未执行；
  当前只等待修订版独立 dispatch review，不存在并行写者或悬空 Phase B。
- [x] 已核对 session inflation：本专题仅 `S001` 一个 session note，无膨胀阻断。

## Goal 续接接收方复核（2026-07-27，CP017）

- [x] 已重新读取 live topic-index 的前台 control、范围边界、不变量、当前位置，
  并完整读取 mission-log CP001–CP017。
- [x] 已从磁盘独立验证至少 3 条当前事实：
  - 当前 control 为 epoch 43 / CP017 / authority formal D034 → **PASS**：
    live `topic-index.md`、formal `decisions.md#D034`、`master-state.md`、
    `state/current.yaml` 与 `portfolio/current.yaml` 一致。
  - T017 正式处置为
    `BLOCKED_FORMAL_READINESS / BLOCKED_SEARCH_OR_IDENTITY` 且
    `mission_method_delta=NONE` → **PASS**：live `verifications.md#V049`、
    live D023、formal D034 与 step-017 worker log 一致；candidate 与
    worker-log SHA256 分别为
    `2d167ec74759a2f460b923cbf516e627a18003843f47729f5689d5a1da20e2d8`
    和
    `0fc319ac0f61043d8858cf21978bae66bd8faa5779d7a11272957dab168b57d0`。
  - 当前无 active scientific carrier，C16-open 不得第二个
    source/formalization package → **PASS**：
    `portfolio/current.yaml` 明确
    `formal_active_carrier.id=NONE/status=NO_ACTIVE_SCIENTIFIC_CARRIER`；
    formal D034、live D023 与 `master-state.md` 一致；仓库中未发现 T017/C16
    Phase B、Step 3、seed 或 MVE 后继产物。
  - T017 的冻结数量门确实失败 → **PASS**：candidate view SHA256 与 V049
    一致，含 44 个 candidate、10 个 acquisition-pool 条目、0 quarantine；
    TechRxiv DOI `10.36227/techrxiv.14775957.v1` 在原 artifact 中被误标为
    published，V049 的纠正计数 `41/3/0` 与 formal D034 一致。
- [x] 已检查 `_registry.yaml`：本专题 depends_on
  `2026-07-20-research-direction-lab-system`（active），`conflicts_with=[]`；
  依赖专题及其产出路径存在。
- [x] 已确认当前范围未违反“明确不含”：恢复只做只读核验与本接收记录；
  未运行新实验、Step 3、seed/MVE，未修 T008/B1、T016/C15 或 T017/C16，
  未恢复 Scout/P03，未修改 Skill/common/params。
- [x] 已核对接口与并行依赖：C001 的 epoch13 历史切换仍由 V003 保留；
  当前由 D023/D034 合法演进至 epoch43。T017 executor 已停止，V049 独立验收
  已完成，无悬空 Phase B 或并行执行依赖。
- [x] 已核对 session inflation：本专题仅 `S001` 一个 session note，无膨胀阻断。

## 长期 Goal 激活接收方验证（2026-07-27，CP017 / epoch46）

- [x] 已重新读取本 H002、live topic-index 的范围边界/不变量/foreground
  control、完整 mission-log CP001–CP017，以及 authority formal D036；
  未用对话摘要恢复科学状态。
- [x] 已从磁盘独立验证至少 3 条当前事实：
  - 当前 control 为 epoch46 / CP017 /
    `Q14_STEP35_PHASE_A_AUTHORIZED`，authority formal D036 →
    **PASS**：live topic-index、T018 task binding、state/current、
    portfolio/current、harvest/current、master-state 与 registry 一致；
    `validate_task_control.py` 返回 `PASS`。
  - V051 只接收修订版 T018 静态合同，formal active scientific carrier
    仍为 `NONE`，下一动作是 final binding 而非直接执行 →
    **PASS**：`verifications.md#V051`、formal D036、live D025 与
    foreground `next_legal_action` 一致。
  - T018 尚未执行，CP/no-method/streak 不应前移 →
    **PASS**：没有 step-018 worker log、Q14 search/citation raw、
    `CP018` 或 `no-method=18`；mission-log 仍止于 CP017/no-method=17。
  - T017 的正式处置仍为
    `BLOCKED_FORMAL_READINESS / BLOCKED_SEARCH_OR_IDENTITY`、delta
    `NONE` → **PASS**：mission-log CP017、V049、D023/formal D034 与
    step-017 worker log 一致；该历史结论未被 Q14 workline 冒充为 active
    carrier。
- [x] 已检查 `_registry.yaml`：本专题 depends_on
  `2026-07-20-research-direction-lab-system`，其状态为 active 且 produces
  路径存在；`conflicts_with=[]`。
- [x] 已确认当前范围未违反“明确不含”：本次只做只读恢复、确定性 binding/
  YAML/diff 检查和本接收记录；未运行检索、下载、精读、Step 4a、实现、
  simulation/Probe/MVE/seed，未修任何旧路线。
- [x] 已核对接口与并行依赖：V051 reviewer 已结束；当前无 executor、无
  acquisition/read writer。必须先由独立 verifier 完成 epoch46 final binding，
  PASS 后再由不同 executor 只执行 T018 Phase A。
- [x] 已核对 session inflation：本专题仅 `S001` 一个 session note，无膨胀阻断。
