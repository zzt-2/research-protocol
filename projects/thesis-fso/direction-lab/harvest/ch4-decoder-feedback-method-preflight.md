# Ch4 decoder-feedback CCISP 方法构造预检

> 日期：2026-08-07
> 控制绑定：epoch 35 / CP022 / D039 / T010
> 范围：design-only、local-only；未检索、未进入 GW、未实现、未仿真
> 最终终态：`CODED_CHAIN_ASSET_BLOCKED`
> survivor：0/3

## 1. 本地证据收据

| 必读对象 | 本轮使用的事实与定位 |
|---|---|
| 执行前控制与章节槽位 | pre-execution snapshot commit `8110fc4cc2a129c856eea9819e0cc0d1908a8b99`：`topic-index.md:7-27` 冻结 epoch 35、唯一 lane 与 CP022；`decisions.md:1374-1487` 冻结 D038–D039；`mission-log.md:319-349` 冻结 CP021–CP022。当前工作树在执行后已前移至 epoch 36 / CP023 / D040，不把新 current 冒充执行前授权。 |
| concept-construction 规则 | `.agents/skills/research-direction-lab/references/method-production.md:107-174`：supporting/reject 不关闭章节槽位；concept card 必须含动作链、章节形与 collision receipt；survivor 只返回正式路线。 |
| 内部方法库存 | `internal-method-kernel-inventory.yaml:17-32,75-102,120-135,178-195,248-255`：CCISP 与 Ch5 的动作身份、P08-R2 partial asset、P05 conventional closure、coded calibration 只能 supporting。 |
| 候选来源 | `candidate-coverage-audit.v3.yaml:83-98` 的 U38/U39；`portfolio-refresh.v1.yaml:25-35,93-101` 的 U47。它们只提供本地机制种子，不构成方法成立证据。 |
| F4-A/F4-C | `F4-A-result.v1.json:43-60,98-100,143-149`：解析 GMI 仅 `+0.008907` bits/sym，且 smoothing=2/8/32 时为 `+0.0331/+0.0102/+0.0032`，最后一项置信区间跨 0；`candidate-map.v1.md:64-70`：F4-C CRC flip 等同 PI-BER，已 Kill。裁决与复核见 `.sessions/2026-07-20-direction-lab-science-scout/decisions.md:859-913`、`verifications.md:350-405`。 |
| P08-R2 | `p08r_chain.py:99-120,143-170`：码率/20 次迭代已冻结，但 decoder 以 `hard_out=True` 建立，公开 `decode` 只回最终 `info_hat` 与 configured-iteration diag；`p08r2_phaseA.py:150-213`、`p08r2_run.py:65-72`：各方法均为一次 equalize→demap→decode，无 decoder→CPR callback；`p08r2_verify.py:303-312` 只核对 code/rate/iteration 与 B2 调参公平性。当前 authority 见 `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:2975-3020`、`verifications.md:3925-3975,4007-4035`：`STOPPED_WITH_PARTIAL_ASSET`。 |
| P05、CCISP 与 Ch5 | `step-032-p05-ml-ood-online-adaptation.md:52-92`：standard-CMA continuation 已解决 swap；`run_ccisp_family1_branchrouted_b_30seed.py:9-20`：selector 先决定 DA/NDA，再只执行一个分支；`run_ccisp_family1_selector_a_30seed.py:34-44`：旧 route A 也只用原 selector 特征选输出；`ccisp-select-before-execute-single-branch-method-package.md:39-88` 冻结 Ch5 的动作与公平性边界。 |
| detection→rollback/relock 历史动作 | `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md:1591-1617`：Q-DP4 detection+rollback 因近期快照已落入 swap 盆地、早期快照随持续 SOP 过时而 Kill；同文件 `:2708-2731` 冻结 causal detection→relock/DD/state-switch 侦察边界，要求早于 failure、非 genie/post-hoc，并保留 baseline/oracle/no-event 对照。 |

以上收据只引用 worktree 内既有文件。没有把标题、seed 或历史负面材料当作新外部证据。

## 2. Coded-chain callback readiness

| 审计项 | 唯一判定 | caller→callee 证据 | 缺口 |
|---|---|---|---|
| 逐符号 extrinsic LLR / soft symbol | `NEW_INFRASTRUCTURE` | `p08r2_phaseA.py:150-213` 调用 `codec.decode(llr)`；`p08r_chain.py:143-170` 以 `hard_out=True` 创建 decoder，公开返回仅 `info_hat, diag`。 | 没有 posterior/extrinsic coded-bit LLR、反交织后的逐符号 soft mean，也没有 `extrinsic = posterior - a_priori` 的接口。 |
| syndrome / CRC / decoder-failure 及因果时点 | `NEW_INFRASTRUCTURE` | 同一 `decode` 返回面只有 hard bits 和 configured iteration；`p08r2_run.py:65-72` 的调度也不消费 decoder state。 | 无 CRC、syndrome weight、parity-check trajectory、early-stop/failure state；更无“在下一次 CPR 动作之前”可见的时点合同。 |
| 受控迭代 / callback 回 CPR 或 recovery | `NEW_INFRASTRUCTURE` | `p08r2_phaseA.py:150-213` 是一次 equalize→demap→decode；`p08r2_run.py:65-72` 只在 B0/B1/B2/O0/O1/O2 之间分派。CCISP caller `run_ccisp_family1_branchrouted_b_30seed.py:14-16` 则是先选一个分支、再单次执行。 | decoder 内部 20 次迭代是黑盒；没有外层 iteration hook、CPR hypothesis bank、rollback/relock 或 next-block recovery callback。 |
| iteration / latency / net-rate / comparator 统一记账 | `NEEDS_SMALL_ADAPTER` | `p08r_chain.py:99-120` 已有 `num_iter=20`、rate 与 net-rate；`p08r2_verify.py:303-312` 已冻结同 code/rate/iteration。 | 仍需给外层反馈轮次、front-end 重算、端到端 latency 和 matched-compute comparator 增加显式账本。仅加账本预计不超过一天；但它不能补前三项接口。 |

结论：当前链不是“已有 callback、差一个胶水函数”，而是只具备 corrected single-pass coded receiver。三类候选分别需要至少两项 `NEW_INFRASTRUCTURE`，按 T010 硬门必须拒绝；但以下仍完整构造三张卡，以区分“方法形可描述”与“当前资产可运行”。

## 3. Prototype / concept cards

### C1 — Decoder-Aided Phase-Hypothesis Feedback（Ch4）

1. **名称与章节槽位**：Decoder-Aided Phase-Hypothesis Feedback for CCISP；目标槽位 Ch4 coded carrier recovery，不改名为新 selector。
2. **M-C-A**：现有 CCISP 在 decoder 证据出现前锁定接收分支/相位决定（M）；在有限相位模糊或 cycle slip 下，前端似然可能不足，而接收端 decoder 一致性在因果时点可区分假设（C）；用 extrinsic/syndrome 对预先冻结的有限相位假设重评分，并至多切换一次下一轮 CPR 假设（A）。
3. **信息源→动作→输出**：receiver-visible extrinsic LLR 或 syndrome trajectory → 有界 phase-hypothesis switch / relock → 同一 decoder 的最终 bits、FER 与反馈 receipt。禁止 TX bits、oracle phase、事后从全部结果选最好者。
4. **7 步算法流程**：
   1. CCISP 按原规则选择并执行一个 recovery branch；
   2. 从该分支输出构造预注册的有限假设集 `H={0,π/2,π,3π/2}`（具体集合须在未来 GW 冻结）；
   3. 对各假设使用同一噪声模型与同一第一段 BP iteration budget 产生 receiver-visible extrinsic/syndrome；
   4. 用预注册、无 truth 的 parity-consistency score 比较当前假设与候选假设；
   5. 只有 score 改善越过冻结 margin 时，切换一次下一轮 CPR 假设，否则保持；
   6. 在总 BP iteration budget 不变的第二段完成一次 re-demap/re-decode；
   7. 输出最终 bits、是否切换、score 时间戳、总迭代与 latency 账本。
5. **相对既有资产的新增点**：相对 CCISP，新增信息源是 decoder 一致性，动作发生在后续 CPR 决策而非 selector threshold；相对 P08/B2，不是 LLR clip/offset；相对 F4-C，不翻转标签、不按 truth/最终 BER 选结果；相对 P05，不做 CMA 权重继续更新。
6. **公平 comparator 与 strongest cheap alternative**：主 comparator 必须使用同一 LDPC、同净码率、同总 20 次 BP iteration、同假设集可见性和 matched end-to-end latency，但关闭 decoder→CPR switch；strongest cheap alternative 是现有 P08-R2 B2（固定 LLR clip + decoder normalization/offset）叠加原 CCISP 单分支，不读取 decoder feedback。当前两者尚无统一 caller，故只冻结合同、不声称已可运行。
7. **主图与预注册主表**：主图是一张因果时序图：CCISP gate→单分支→假设 bank→第一段 decoder evidence→一次 hypothesis switch/keep→第二段 decoder→bits；图上标出 truth 禁区、反馈时点和总迭代预算。未来主表的行固定为 `no-feedback`、`receiver-only likelihood switch`、`decoder-evidence switch`；列固定为 code/net-rate、总 BP iterations、hypothesis count、switch rate、FER、端到端 latency 与额外前端调用数。
8. **承重消融**：`decoder-evidence switch` 对比 `front-end likelihood switch`，保持同一假设集与总计算量；若二者无差异，则 decoder 信息没有动作增量，方法身份失败。
9. **最小 testbed delta 与工期**：须新增 extrinsic/syndrome 输出、hypothesis bank、分段 decoder callback、一次 switch 状态机和 latency ledger；至少 3 项是新基础设施，不能诚实归为 ≤1 天 adapter。
10. **claim ceiling 与失败 fallback**：未来最高只可主张“decoder consistency causally controls one bounded CPR hypothesis update”；不能引用 F4-A `+0.0089` 作为稳定上界，不能主张普遍 BER 增益。失败则保留为 coded-interface requirement，不成章、不进 GW。
11. **collision receipt**：
    - existing action：不同于 CCISP 原 gate，但 phase switch 属 D047 已登记的 causal detection→relock/state-switch 动作族；仅更换为 decoder 信息源尚不能证明新 action identity；
    - dead end：若退化为 CRC flip/最终 BER 选相位，即与 F4-C/PI-BER 重标碰撞；若回滚历史 CMA state，则直接命中 D028 的 stale-snapshot/持续 SOP Kill；
    - cheap alternative：P08-R2 B2 + 原 CCISP；
    - reopen condition：公开因果 extrinsic/syndrome、可分段 decoder callback、合法假设 bank，且必须相对 receiver-only causal relock/state-switch 证明 decoder evidence 改变动作并同时保持 recovery dwell 与 BER；不得复用历史快照；
    - classification：`REJECT`（action-family collision 未解除，且 3 项 `NEW_INFRASTRUCTURE`；survivor gates 3/5 FAIL）。

### C2 — Extrinsic Soft-Symbol Iterative CPR（Ch4）

1. **名称与章节槽位**：Extrinsic Soft-Symbol Iterative CPR for CCISP；目标槽位 Ch4，不作为 P08 LLR calibration 的扩写。
2. **M-C-A**：现有 coded receiver 的 CPR 与 decoding 单向串联（M）；当初始相位/频偏误差仍在 decoder 可纠正区内时，真正 extrinsic 的 coded-bit 信息可能给 CPR 提供比硬判决更稳的符号期望（C）；将 posterior 减去 a-priori 后形成 soft symbols，做一次冻结的相位/频偏更新并重新译码（A）。
3. **信息源→动作→输出**：decoder extrinsic coded-bit LLR → 反交织/调制映射后的 soft-symbol expectation 与可靠度 → 一次加权 phase/frequency update → final LLR/bits 与 iteration/latency receipt。
4. **7 步算法流程**：
   1. 按原 CCISP 分支完成初始 equalization/CPR/demap；
   2. 运行第一段 decoder iterations，取得 posterior 与进入 decoder 的 a-priori；
   3. 显式计算 `L_ext=L_post-L_apriori`，裁剪后反交织到 coded-symbol 顺序；
   4. 由 `L_ext` 计算 soft-symbol mean 与可靠度，禁止混入 TX symbols；
   5. 用冻结的可靠度门对相位/频偏做一次加权更新；
   6. 重新 demap，并用剩余 BP iterations 完成第二段 decode；
   7. 输出 bits、前后 phase/frequency delta、extrinsic norm、总迭代与 latency。
5. **相对既有资产的新增点**：相对 CCISP，是 decoder soft information 驱动的连续 CPR state update；相对 P08/F4-A，不只是改变 LLR scale/noise variance；相对 F4-C，不做 label flip；相对 P05，不继续 CMA/equalizer 权重。
6. **公平 comparator 与 strongest cheap alternative**：主 comparator 为同 code/net-rate、同总 20 BP iterations、同一次额外 front-end 预算和 matched latency 的 no-extrinsic CPR（使用 receiver-only front-end likelihood/硬判决生成权重）；strongest cheap alternative 是 standard-CMA continuation（P05）加 P08-R2 B2。若后者已消除同一误差，C2 不得成方法。
7. **主图与预注册主表**：主图为两轮展开图，突出 `L_post - L_apriori`、反交织、soft-symbol CPR update 和固定总预算；a-priori 旁路以红色禁止回灌。未来主表的行固定为 `no-feedback`、`hard-DD/CMA+B2`、`posterior-as-extrinsic`、`true-extrinsic`；列固定为 code/net-rate、总 BP iterations、CPR updates、FER、phase/frequency error、latency 与额外前端调用数。
8. **承重消融**：`true extrinsic` 对比 `posterior-as-extrinsic` 与 `hard-decision directed`，同预算比较；若 posterior-as-extrinsic 的表面增益消失或 hard-DD 等价，则否决 decoder 特有机制。
9. **最小 testbed delta 与工期**：须新增 soft-output/extrinsic decoder、coded-bit 到 symbol 的可靠反映射、外层 CPR callback 和两轮 latency ledger；3 项以上新基础设施，超过 ≤1 天 adapter。
10. **claim ceiling 与失败 fallback**：未来最高只可主张“一次 extrinsic soft-symbol update 改善特定 coded-CPR failure”；不以 F4-A smoothing-fragile GMI 作为正证据，不外推到深衰落全码字失败。失败则只记录为 F4-B 的尚未具备接口的机制草图。
11. **collision receipt**：
    - existing action：与 CCISP gate、P08 scalar calibration 不同，前提是真正更新 CPR state；
    - dead end：若只调 LLR temperature/clip，即回落 P08 B2/F4-A；若做 hard-DD 在线更新，则与 P05 conventional CMA 吸收；
    - cheap alternative：standard-CMA continuation + P08-R2 B2；
    - reopen condition：decoder 暴露可验证的 `L_ext`、coded-symbol mapping 与受控外层 callback，并先证明问题未被 CMA/B2 吸收；
    - classification：`REJECT`（extrinsic 与 callback 两项以上 `NEW_INFRASTRUCTURE`，survivor gate 5 FAIL）。

### C3 — Syndrome-Triggered Recovery Control（Ch4）

1. **名称与章节槽位**：Syndrome-Triggered Bounded Recovery Control for CCISP；目标槽位 Ch4，不是 CRC-based relabel。
2. **M-C-A**：现有 CCISP 在单分支完成后没有利用 decoder failure 的因果状态（M）；部分 cycle slip/错误锁定可能表现为早期 syndrome 不收敛，而不是不可恢复的深衰落（C）；用预注册的 syndrome/CRC failure trajectory 触发一次有限 relock、假设切换或下一块重获取动作（A）。
3. **信息源→动作→输出**：receiver-visible syndrome weight / CRC failure at time `t` → 预冻结的单一 recovery command（本卡采用一次 relock-and-hypothesis-switch，不同时试多个动作）→ 当前帧第二次 decode 或下一块状态及最终 FER/latency receipt。
4. **7 步算法流程**：
   1. 原 CCISP 完成 gate、单分支与初始 CPR；
   2. decoder 运行第一段 iterations，并在冻结时点暴露 syndrome trajectory/CRC state；
   3. 用 dev-frozen failure predicate 区分“继续收敛”与“触发恢复”，不读取最终真值；
   4. 未触发则原路径继续；触发则只执行一次预注册 relock-and-hypothesis-switch；
   5. 以剩余固定 decoder iterations 重新 demap/decode；
   6. 达到一次恢复上限后无条件停止，禁止事后多动作择优；
   7. 输出 bits、trigger 时点、动作、syndrome trajectory、总 latency 与是否 budget exhaustion。
5. **相对既有资产的新增点**：相对 CCISP，是 downstream decoder failure 触发下一 recovery command；相对 P08，是 failure trajectory 而非 LLR scalar；相对 F4-C，不翻转标签或用 CRC 选择较低 BER 输出；相对 P05，不做常规 CMA continuation。
6. **公平 comparator 与 strongest cheap alternative**：主 comparator 为同 code/net-rate、同总 BP iterations、同最多一次 relock 预算与 matched latency，但 recovery trigger 使用 receiver-only front-end confidence；strongest cheap alternative 是原 CCISP 固定 gate + P08-R2 B2。针对 swap 场景另须把 standard-CMA continuation 作为必须击败的传统替代。
7. **主图与预注册主表**：主图为状态机图：`NORMAL→EARLY_DECODER_CHECK→{CONTINUE, ONE_RECOVERY}→FINAL_DECODE→STOP`，标明唯一恢复次数、因果时间和禁止的 post-hoc selector。未来主表的行固定为 `no recovery`、`receiver-only causal trigger`、`final-CRC-only`、`early-syndrome trigger`；列固定为 code/net-rate、总 BP iterations、trigger lead time、recovery count、FER、recovery dwell、latency 与 no-event false-trigger rate。
8. **承重消融**：`syndrome-trajectory trigger` 对比 `front-end confidence trigger` 与 `final-CRC-only trigger`；若只有 final CRC 有效，则没有因果控制，只是事后筛选，方法失败。
9. **最小 testbed delta 与工期**：须新增 syndrome/CRC trajectory、decoder 中途 callback、recovery state machine、同预算 latency ledger；前三项均不是现有 adapter，超过一天。
10. **claim ceiling 与失败 fallback**：未来最高只可主张“early decoder-failure state controls one bounded recovery action”；不得声称修复 P08-R2 已显示 oracle 也失败的深衰落全码字事件。若 failure flag 无早于最终输出的增量，则退回监测/支持材料。
11. **collision receipt**：
    - existing action：不同于 CCISP 前置 gate，但 early detection→relock/recovery 与 D047 动作族重合；decoder syndrome 只是新信息源，尚未证明产生不同 recovery policy；
    - dead end：final CRC 后翻标签/选最好结果与 F4-C 碰撞；仅报告 failure 与 U47 monitoring 而非方法；回滚历史 equalizer snapshot 则命中 D028 的 dwell/BER 不可兼得 Kill；
    - cheap alternative：原 CCISP + P08-R2 B2；swap 条件下是 standard-CMA continuation；
    - reopen condition：decoder 在明确因果时点公开 syndrome/CRC trajectory，receiver 支持一次受控 recovery；相对 receiver-only causal trigger 必须证明 decoder trigger 改变动作/lead time，并在持续 SOP 下同时保持 dwell 与 BER，且排除不可恢复深衰落；
    - classification：`REJECT`（action-family collision 未解除，且 syndrome state、callback、recovery control 至少 3 项 `NEW_INFRASTRUCTURE`；survivor gates 3/5 FAIL）。

## 4. 七门逐卡裁决

| survivor 门 | C1 | C2 | C3 |
|---|---|---|---|
| 1. 不同且 receiver-visible 的 decoder 信息 | 设计上 PASS；当前接口 BLOCKED | 设计上 PASS；当前接口 BLOCKED | 设计上 PASS；当前接口 BLOCKED |
| 2. 真实闭环动作、非标量/离线/post-hoc | phase switch 为 PASS | CPR state update 为 PASS | bounded recovery 为 PASS |
| 3. 不与 F4-C/P08/P05/CCISP/dead end 碰撞 | **FAIL：与 D047 detection→relock/state-switch 动作族重合，且未解除 D028 stale-state 边界** | 条件 PASS；退化为 scalar/DD 即 FAIL | **FAIL：与 D047 detection→recovery 动作族重合，且未解除 D028 dwell/BER 边界** |
| 4. code/net-rate/iteration/latency/信息可见性公平 | 合同可写；当前统一 caller BLOCKED | 合同可写；当前统一 caller BLOCKED | 合同可写；当前统一 caller BLOCKED |
| 5. testbed READY 或 ≤1 天小适配 | **FAIL：≥3 NEW_INFRASTRUCTURE** | **FAIL：≥3 NEW_INFRASTRUCTURE** | **FAIL：≥3 NEW_INFRASTRUCTURE** |
| 6. 实验前可写流程图、主表、承重消融 | PASS（本卡已定义） | PASS（本卡已定义） | PASS（本卡已定义） |
| 7. 可证伪 baseline failure | 部分：需证明 front-end likelihood 无法区分而 decoder 可区分 | 部分：需证明 CMA/B2 无法吸收且处于可纠正区 | 部分：需证明 early syndrome 比 front-end trigger 更早且非深衰落不可恢复 |
| **最终** | `REJECT` | `REJECT` | `REJECT` |

不存在七门全过候选，survivor=`0`。没有创建回 GW Step 1 的 M-C-A，也没有创建 active carrier、`METHOD_SIGNAL`、Go、晋级方法卡或论文正文。

## 5. 唯一终态

`CODED_CHAIN_ASSET_BLOCKED`

选择该终态而不是 `NO_METHOD_SHAPED_SURVIVOR`，因为三条链均能写出可辨识的 decoder 信息源与 causal action，但当前 corrected coded-chain 同时缺少 decoder 中间信息和外层 callback/recovery 两类以上接口，硬门 5 统一失败。该终态是资产 readiness 裁决，不是对 decoder-feedback 科学假设的 Kill，也不授权补基础设施、进入 GW、实现或仿真。
