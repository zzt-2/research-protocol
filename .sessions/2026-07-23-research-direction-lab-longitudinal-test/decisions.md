# Decisions — Research Direction Lab 长程真实运行测试

## D001: Phase 2 首包续接合法 B1 carrier，不跳转 C15

> status: superseded
> date: 2026-07-26
> 取代：无
> 扩展：formal D013 / system D018 / mission CP007
> 被取代：D002
> 依据：`projects/thesis-fso/master-state.md` 当前控制面与 FR-22 + T007 phase-1 critic
> 触发原话：无（技术纠偏；用户只要求交付下一提示词）

### 决策

Phase 2 第一包为 B1 adaptive phase-window 的 **identity-repaired method-production
package**。C15 虽有现成代码，但未完成当前 formal owner 要求的新候选 Step 1–3；
直接运行会违反 FR-22。它保留为后续 candidate，不以“portfolio 可运行”冒充
“formal 已授权”。

B1 已有 Step 1–3 与 formal D013，且 T007 的当前 oracle 诊断仍显示约 0.4–1.0 dB
局部空间；其 Kill 未被主控接收。T008 只关闭五个已知身份缺口，若合法空间仍在，
同一包必须完成三个 receiver-visible 方法及 fresh-seed paired comparison。

### 正向方法合同

- `positive_method_target`：receiver-visible、低复杂度 adaptive phase-window CPE。
- `minimal_construct`：physics-ratio rule、validation lookup+hysteresis、
  confidence-safe selector。
- `fair_comparator`：validation-frozen global fixed window；per-condition fixed 作强对照。
- `primary_packaging`：面向 GG block-SNR 与 Wiener phase-noise 联合变化的自适应窗。
- `fallback_packaging`：合法 fixed-window 选择与 receiver-observability 工作区边界。
- `next_positive_action`：执行 T008；identity 修复后同包跑方法，不再单独派纯修复包。

### 已知五个缺口

1. B* 疑似按 seed/test truth 重选，而非 validation 全局冻结；
2. required-SNR 使用硬编码 log-BER slope，而非真实 SNR 曲线；
3. oracle/B* 候选集合与选择身份未完全闭合；
4. observability 缺 held-out exact-window accuracy 与 majority-fixed 对照；
5. 仅凭当前特征 `|rho|<0.5` 把 0.4–1.0 dB diagnostic headroom 提前 Kill。

### 边界

- 只在 GW Step 4a；不进 Step 5/Contract/Execute。
- executor 不更新 formal/current/master/mission owner。
- 任一 identity 无法闭合则 `BLOCKED_IDENTITY`，不作科学裁决。
- headroom 存在但方法不胜则 `METHOD_FAIL_WITH_SPACE`，不 Kill 整个 family。
- 不修 Pilot-Jones、B10/B12、C15 或 dormant science-scout。

---

## D002: 拒收 T008 Kill，停止 B1 修复并转 Goal 级 campaign remap

> status: superseded
> date: 2026-07-26
> 取代：D001（仅取代当前 carrier 与下一动作；D001 对 T008 的历史授权仍有效）
> 被取代：D003
> 依据：验证 V002 + mission CP008 + T008 task/runner/raw artifact 独立重算
> 触发原话：`voice.md` 2026-07-26（用户准备在新 GPT 对话用 Goal 模式持续推进）

### 决策

1. T008 的 17 项工程测试通过，五类修复尝试与数据资产保留；但正式
   `KILL_NO_ADAPTIVE_WINDOW_SPACE` **不接收**，formal disposition 为
   `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`。
2. 不再给 B1 开 T009 修复包。连续两个 B1 包、全 mission 八包均未产生方法增量，
   已满足“正式进展但 method delta 持续为 NONE”的 mission stalled 条件。
3. 前台动作切换为 `GOAL_MODE_CAMPAIGN_REMAP`：新主控先恢复 CP001–CP008，
   比较仍合法的 carrier、方法包装潜力和最小补债成本；只有完成显式 remap 后才可
   准备下一科学 T。

### 理由

- 冻结任务规定：无真实 FEC crossing 时只能报 raw/log-BER 与
  `UNRESOLVED_NO_CROSSING`，不得用 proxy dB 触发 `<0.5 dB` Kill。T008 runner
  却用非 FEC 区 B* slope 生成 `dB-equiv` 并据此 Kill。
- gate 实际比较 B-cond 与 B*，没有按任务计算 per-block oracle；其 per-block
  代码还跳过 `N>BLOCK=100`，而实际 `B*=256`，故“oracle 候选包含 B*”声明为假。
- 去 pilot 标签重算后，20 dB 的 QPSK BER 仍约 0.174–0.178，16QAM 约
  0.272–0.280。逐窗 VV 的 π/2 分支跳变只做全局 resolve，基线本身不在可靠
  working region；两个坏基线近似不能证明自适应空间消失。
- results/raw/fresh-test 位于 gitignored `results/`，未进入提交，证据闭包也不完整。

### 排除的替代方案

- 不接收 scoped/family Kill：主 metric、oracle identity 和 evaluator working
  region 同时失效。
- 不再修 B1：这会成为同轴第三包，并继续把方法生产 mission 运行成 evaluator
  修复链。
- 不立即运行 C15 或任意新实验：formal Step 1–3 与 campaign remap 尚未完成，
  直接开跑会再次违反 FR-22。

### 影响范围

- live control 升至 epoch 13，checkpoint 为 CP008；禁止 T009/B1 repair。
- formal master 将 B1 标为 `BLOCKED_IDENTITY / RETURNED_TO_POOL`。
- 下一对话通过 H002 恢复，并显式建立“方法产出优先”的 Goal；本对话不创建 Goal。

### 来源

T008 worker 回执、V002 独立审查、用户 2026-07-26 Goal 模式安排。

---

## D003: Campaign remap 激活 A4 deployable adaptive CPR

> status: active
> date: 2026-07-26
> 取代：D002（只取代“无 active carrier / 仅 remap”的当前动作；T008 拒收事实保留）
> 被取代：无
> 依据：R001 + formal D015 + CP001–CP008 + A4 bugfix/common-768/写作资产
> 触发原话：`voice.md` 2026-07-26（长期 Goal 的 carrier 比较、方法优先与独立验收要求）

### 决策

1. campaign remap 完成。首轮比较 A4、B10/B12、B1 三条具有 formal 证据链的
   carrier，并逐项证明 B2/B3/B7/C15/B9/Pilot-Jones/P03/Scout 当前不满足
   formal readiness。
2. 当前 carrier 激活为 `A4_DEPLOYABLE_ADAPTIVE_CPR`，状态
   `READY_WITH_BOUNDED_IDENTITY_ADJUDICATION`；仍在 GW Step 4a。
3. 下一包 T009 不是纯 audit：一次有界 identity preflight 通过后，必须同包冻结并
   比较 P1 frozen two-stage rule、P2 monotone selector、P3 confidence-safe
   selector。
4. T009 只在统一 transmitter waveform、common data mask、deployable input、
   causal ambiguity resolve 与包含 S011 DPLL 的 validation-frozen strongest
   conventional comparator 下接受科学结论。
5. 若只胜 fixed NDA 却被 always-DA、DPLL 或 global B* 支配，最高
   `PACKAGING_BOUNDARY`；测试 PASS、negative result 或 evaluator repair 均不算
   method delta。
6. T009 失败不结束 Goal，也不追加第二个 A4 repair 包。主控接收后更新 CP009
   的 method delta、same-axis/repair/no-method streak 与 drift，再自动比较
   B10 source-native 最小重建和新候选 Step 1–3。

### 为什么优于两个替代项

- **相对 B10/B12**：A4 已有可运行方法动作、两个不同输出分支、30-seed 数据和
  论文方法结构；B10/B12 的核心 estimator source identity 尚未成立，先要重建
  方法本体。
- **相对 B1**：A4 是本轮第一次 formal adjudication；B1 已连续 T007/T008 两包且
  evaluator 不在可靠 working region，再继续将成为第三个同轴 repair 包。

### 正向方法合同

- `positive_method_target`：receiver-visible、块级 DA/NDA adaptive CPR。
- `minimal_construct`：P1 frozen two-stage rule；P2 monotone validation selector；
  P3 confidence-safe selector。
- `fair_comparator`：fixed DA、fixed NDA、validation-frozen DPLL；
  global B*/B-cond 均从三者选定；per-block oracle 只作 ceiling。
- `primary_packaging`：Gamma–Gamma 湍流下的接收功率感知自适应 CPR。
- `fallback_packaging`：NDA safeguard、工作区边界或 complexity/robustness trade-off。
- `next_positive_action`：执行 T009；identity 过门后同包完成 fresh paired method
  comparison。

### 边界

- 不修改旧 A4、论文正文、common、params 或任何 owner；
- 不恢复 B1/T008、T006 repair、Pilot-Jones、P03 或 dormant Scout；
- 不进入 Step 5、Contract 或 Execute；
- mission checkpoint 仍为 CP008，只有主控接收 T009 后才能追加 CP009。
