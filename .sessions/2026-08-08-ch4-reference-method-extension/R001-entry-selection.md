# [R001] Ch4 reference-method 入口选择

> 2026-08-08 | 关联：2026-08-08-ch4-reference-method-extension / D001 / T001

## 调研问题

只利用仓库已有论文、代码、历史 inventory 与结果，在不检索、不实现、不仿真、不进入 Groundwork 的边界内，比较最多 3 个机制不同的 research object / reference baseline，并推荐至多 1 个进入后续正式 Groundwork Step 1。

## 1. 恢复验证与防偏三问

### 恢复验证

- **PASS — 专题状态**：旧 `2026-07-20-research-direction-lab-system` 为 `dormant`，本专题为 `active`；本专题 `conflicts_with: []`。证据：`.sessions/_registry.yaml:29-34,54-65`。
- **PASS — 授权范围**：当前只授权 1–3 个 reference baseline 的入口选择，不检索、不实现、不仿真。证据：`topic-index.md:13-20,32-47`；`T001-reference-method-entry-selection.md` §0、§2.4。
- **PASS — 排除边界**：P1、decoder-feedback 基建、CCISP 标量调参、C3、oversampled Q1、coded-burst 4b#1、AMC Q-A/Q-B、G1/P09 均不得改名重开。证据：`T001-reference-method-entry-selection.md` §1。
- **PASS — 依赖关系**：本专题依赖的旧 RDL system 与 thesis-writing 条目均存在；前者提供历史/dead-end owner，后者提供章节槽位约束；无登记冲突。证据：`.sessions/_registry.yaml:54-65`。

### 防偏三问

1. **当前工作是否直接产生或裁决一个方法？** 是。它裁决 reference-method 入口，本轮结论是没有对象通过全部入口门。
2. **它是否是最小构造前不可缺的步骤？** 是。没有 baseline 身份、复现边界、defect、one action、comparator 与历史碰撞核验，就不能合法构造最小方法。
3. **是否已触发“每对象 2 包 / 两对象失败”的停止条件？** 旧方法工厂已留下 K01–K05 `survivor=0`，其中本轮 C1 是 exact K01；本轮两个机制不同入口又均未过门。无论是否把未执行 package 的 C2 计入“两包”计数，T001 §2.3 的 `NO_ENTRY_SURVIVOR` 终态已触发，必须停止并交回战略决定，不得补第三候选或继续包装。证据：`.sessions/2026-07-20-research-direction-lab-system/decisions.md:917-951`。

## 2. 候选来源说明

只审计两个机制不同且具备具体 reference identity 与不超过 3 天 baseline 重建路径的对象：

1. **Paillier AGC + 二阶 DPLL**：闭环 carrier acquisition/tracking；仓内有同类 DPLL 与 runner，但拟议 FG-DRC 动作与旧 K01 exact 相同。
2. **Di Rosa–Richter pilot-aided LBS-RDE**：pilot/data 交错的偏振均衡；论文与 CMA/MMA/pilot scaffold 齐全，但没有直接 LBS-RDE/PS-QAM runner，也没有星地 FSO defect 收据。

没有为凑数加入第三个对象：Pilot-Jones 已被 fixed EMA 吸收且执行包超限；block-CMA 的 per-symbol Godard action 本身就是已有传统 comparator；其余对象或命中 T001 明示排除，或被本地 exact dead end 关闭。排除只针对 exact object/action，不外推关闭整个接收机、同步或均衡方向。

## 3. 候选对比总表

`PASS_LOCAL` 仅表示本地历史无已证实 exact external-action collision；未检索的外部碰撞仍为 UNKNOWN。任一 `FAIL` 均使对象不能推荐。

| 候选 | Reference | Defect | One action | Comparators | G1 | G2 | G3 | G4 | G5 | G6 | G7 | 预算 | 主要证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C1 Paillier AGC+DPLL / post-fade reacquisition** | Paillier et al., JLT 2020, DOI `10.1109/JLT.2020.3003561` | 论文只支持 fade 抬高失稳门限；post-fade state damage 未观察，现有 runner 也不是相关时序收据 | `TRACK / HOLD / REACQUIRE` 管理 loop state | fixed AGC+DPLL；cheap = fixed DPLL + slip detector + unconditional pilot reacquisition | PASS | PASS（任务适配实现） | **FAIL** | PASS_SHAPE | PASS | PASS_IF_DEFECT | **FAIL — exact K01 REJECT collision** | 若合法重开才可能 3–5 天；本轮不授权 | `papers/_read_notes/10.1109_jlt.2020.3003561.md:5-23`; `projects/thesis-fso/direction-lab/harvest/baseline-first-method-batch-001.md:117-148`; `.sessions/2026-07-20-research-direction-lab-system/decisions.md:917-951` |
| **C2 LBS-RDE / receiver-triggered pilot-density switching** | Di Rosa & Richter, JLT 2021, DOI `10.1109/JLT.2021.3098220` | 论文 fiber 场景有 pilot-density-sensitive dynamic penalty；星地 FSO 同 defect 未建立 | 保持 LBS-RDE 不变，只按 receiver stress 在 `N=128/32` 间切 pilot spacing | fixed-POH LBS-RDE；cheap = always-high-density `N=32`，并保留 `N=128` | PASS | PASS_INFERENCE（≤3 天重建） | **FAIL/UNKNOWN_FSO** | PASS_SHAPE | PASS_DESIGN | PASS_CONDITIONAL | PASS_LOCAL（有 B2 相邻负先验） | baseline 2.5–3 天；总包 5–7 天 | `papers/manual/ieee-9492010-likelihood-rde/content.md:107-123,213-285`; `papers/_read_notes/ieee-9492010-likelihood-rde.md:13-68`; `projects/simulation/explore/pilot-jones-step4a/synthesis.md:34-67` |

## 4. 逐候选分析

### C1 — Paillier AGC+DPLL / exact K01 FG-DRC

**FACT**

- reference baseline 是 ADC 后 AGC→二阶 DPLL→BPSK detector/differential decoder；DPLL 含 phase detector、loop filter 与 NCO。`papers/doi/10.1109_jlt.2020.3003561/content.md:114-145`
- 论文报告无幅度起伏时约低于 −9 dB 无法锁定，fade 使临界平均 SNR 进一步恶化约 5 dB；它没有证明 post-fade NCO/state damage。`papers/_read_notes/10.1109_jlt.2020.3003561.md:18-22`
- 仓内 DPLL 逐符号更新 integrator/NCO、没有 hold/reacquire 状态；现有 runner 每个 realization 重新生成独立 block-GG draw 并调用 DPLL，不是 time-correlated fade-exit/relock testbed。`projects/simulation/common/_recovery.py:59-127`; `projects/simulation/common/_channel.py:27-31`; `projects/simulation/simulator/run_dpll_ablation.py:234-252`
- 本轮拟议的 FG-DRC 名称、`TRACK/HOLD/REACQUIRE` 动作、主图、消融与 cheap comparator，和旧 `baseline-first-method-batch-001` 的 K01 完全一致。`projects/thesis-fso/direction-lab/harvest/baseline-first-method-batch-001.md:117-148`
- 旧 D027 已接受 K01 为 `REJECT — PROBLEM_EVIDENCE_INSUFFICIENT`，并明确禁止把 K01–K05 中“最接近”的卡降门晋级或写成方法贡献。`.sessions/2026-07-20-research-direction-lab-system/decisions.md:917-951`

**INFERENCE**

- 一个真正的 post-fade 时序 testbed 可能能够证伪或观察 state damage，但那是对旧 K01 的重开，不是 fresh reference entry；当前 D001 `取代: 无`，本轮也没有新 evidence 或用户授权推翻旧 D027。

**UNKNOWN**

- post-fade state damage、触发统计量、精确复杂度与外部 exact-action collision 仍未知。

**裁决**

- G3 FAIL：既有证据只支持临界 SNR，不支持承重 post-fade defect；现有 runner 不能直接提供该收据。
- G7 FAIL：exact historical rejected-package collision。不得把相同 K01 缺口改标 `PASS_PATH` 后晋级。

### C2 — LBS-RDE / Receiver-Triggered Pilot-Density Switching

**FACT**

- 论文原方法已经是 “QPSK pilots + payload likelihood-gated RDE update”；likelihood gate 属于 reference baseline，不能再冒充 Ch4 新动作。`papers/manual/ieee-9492010-likelihood-rde/content.md:107-123,153-165`
- 论文 fiber PMD/SOP 场景中，降低 pilot overhead 会损害动态跟踪；64QAM-PS4 在低 overhead 下不能承受超过 1 Mrad/s，256QAM-PS6 即使高 overhead 也约为 800 krad/s。`papers/manual/ieee-9492010-likelihood-rde/content.md:269-285`
- 仓库没有作者代码或直接 LBS-RDE runner；现有的是 CMA/MMA、pilot 注入与 GMI scaffold。`papers/_read_notes/ieee-9492010-likelihood-rde.md:65-68`
- 当前本地 Jones testbed 是慢速、良态的 real rotation；fixed EMA 已近 oracle，不能继承论文 fiber defect 为星地 FSO 事实。`projects/simulation/explore/pilot-jones-step4a/synthesis.md:34-67`

**INFERENCE**

- 唯一不重复论文原动作的部署扩展，是按 receiver-visible residual/accepted-update fraction 在固定 `N=128/32` pilot spacing 间切换；它需要 TX/RX 协同，并须按相同平均 pilot overhead/能量预算比较。

**UNKNOWN**

- 星地 FSO 是否存在同类 pilot-density-sensitive defect、receiver statistic 是否能可靠触发、反馈延迟/调度成本、外部 exact collision 均未知。
- baseline 重建本身已需 2.5–3 天，defect 不能从现有 FSO testbed 继承，因此不满足本轮 G3。

## 5. 无 survivor

**terminal：`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`**

- C1 虽有强 reference identity 与可运行的任务适配 DPLL，但拟议动作是 exact K01 rejected package；G3/G7 失败。
- C2 的 reference 与 action shape 可辨认，但星地 FSO defect 为 UNKNOWN；G3 失败。
- 没有对象 7 门全过，因此不推荐任何对象，不制造第三候选，不把基础设施成本当科学 Kill，也不把相邻 prior art 当 exact collision。

该终态不关闭 Ch4 方法槽位，也不表示“整个同步/均衡/接收机都不行”；它只说明 T001 授权的本地入口选择没有合法 survivor，需要用户决定是否改变 formal goal、research object source 或允许显式重开旧 K01。

## 6. 方法章最小成品预演

无。T001 只允许对胜者预演；本轮没有 survivor，不设计具体算法、不伪造方法章包装。

## 7. 下一合法动作与禁止动作

### 下一合法动作

交回用户作战略范围决定。可讨论但不得自行执行的选项包括：扩大/改变 reference-object 来源，或以显式 scope/decision change 授权重开某个旧 rejected object。没有用户决定前，不进入 Groundwork。

### 禁止动作

- 不自行启动 `stages/groundwork.md`、GW Step 1/4a、检索、下载、实现或仿真。
- 不把 C1/K01 或 C2 写成已成立方法，不引用尚不存在的增益数字。
- 不补第三候选，不复活 Pilot-Jones、CMA/G1、P1、decoder-feedback、CCISP 标量调参或 T001 的其他 forbidden object。
- 不把 cheap comparator 预杀，不以基础设施工作量代替科学裁决。
- 不修改或暂存四个既有 `p05_run*.log`，不 push。

## 对决策的影响

产生 D002：terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`；本轮没有 method delta，不进入 Groundwork。
