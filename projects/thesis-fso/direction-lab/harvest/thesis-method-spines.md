# 每个核心技术章都有方法：候选 Thesis Spines

> 2026-08-03 | owner: `.sessions/2026-07-09-thesis-writing` / S018
> 状态：paper-writing PROPOSE；不是正式论文章节，不授权跑实验。D023/D024 已被 D025 暂停。

## 1. 候选方法终态

| candidate | action chain | baseline | grade | 当前判断 |
|---|---|---|---|---|
| **2A Calibration-Aware Robust Adaptive CPR** | pilot-SNR estimate → operating-region calibration → CCISP branch action | original selector、global/region retune、oracle operating point | **NEEDS_ONE_BOUNDED_PACKAGE** | 有统一 input-action-output 和 4/5 harm-cell 恢复，最像 A3“补被忽略变量后重估”和 A8“estimated SNR→threshold decision”；但必须证明不是普通 `ref 9→11 dB` 已完全吸收 |
| **2B Low-Complexity Branch-Routed and Fixed-Point CPR** | quantized receiver statistic → preselect → execute DA/NDA one branch | route A dual-branch、float route B、uniform word-length ladder | **NEEDS_ONE_BOUNDED_PACKAGE** | route B 是真实部署动作且 990/990 输出一致，最像 A1/A5 的“先改计算流程，再做定点/硬件”；Q(8,6) 只能是子链，缺 formal full-grid cost/latency、float-vs-Q BER 与真实综合 |
| **2C Receiver-Visible Coded Calibration** | prefix-LS → channel/noise estimate → MMSE/LLR | standard prefix-LS、corrected B0/B2、oracle | **SUPPORTING_ONLY** | 当前主要是修 hidden-gamma bug 的 receiver correctness infrastructure；没有相对标准 prefix-LS 的新 action。若另找 coded 方法须新 GW，不能续包装当前资产 |
| **2D Risk-Aware Rate/Outage Control** | receiver state → conditional risk → rate/no-transmit | conventional outage margin、fixed-rate、oracle | **NEEDS_NEW_GW** | 方法形状成立，但 9/27 和 +5.1%–6.7% 全属 unauthorized dev-only；需重新授权、修 testbed/contract 并做 held-out paired validation |

### 不能单独命名成方法的组件

- 2A：fixed 13 dB、`ref=11 dB`、weak-region label、某个 estimator 或 CV threshold 是参数/校准规则。
- 2B：Q(8,6)、uniform/mixed precision、0/132000 mismatch、resource proxy、990/990 identity 是实现点或验证门。
- 2C：32-symbol prefix、AST/metamorphic gate 是正确性设施。
- 平台、测试、verifier、单参数、字长和 bugfix 都不能单独占一个“方法”标题。

## 2. Spine S1：鲁棒—部署递进（唯一推荐）

> 总体 grade：**B− / CONDITIONAL**。三章都有方法形状；Ch3 已成熟，Ch4/Ch5 各差一个有界包，未完成前不得进入正式 WRITE。

### Ch3 Received-Power-Aware Adaptive CPR（CCISP）

| 字段 | 合同 |
|---|---|
| method | Received-Power-Aware Adaptive CPR / CCISP |
| baseline | fixed DA、fixed NDA |
| new action | CV gate → blind effective-SNR → fixed 13 dB decision → 只执行 DA/NDA 一支 |
| input | raw `|r|^2`、nominal SNR、DA pilot；仅 receiver-visible 信息 |
| algorithm flow | 已有完整流程图和 method.tex 步骤 |
| main experiment | 已有三档 downlink、9 dB、30 seeds、400 windows 的 common-payload BER-ratio |
| ablation | fixed DA/NDA、CV gate、effective-SNR gate |
| claim | 当前合法 ceiling：相对 fixed NDA 约 0.8–1.5 dB；禁止 26/29、uplink、1.2–1.9/3.1 dB |
| difference / independence | thesis 主方法；Ch4 改输入校准，Ch5 改执行计算图，不重复本章贡献 |
| remaining gap | non-genie NDA ambiguity deployment closure 仍属边界，不在本轮扩写 |

### Ch4 Calibration-Aware Robust Adaptive CPR（2A）

| 字段 | 合同 |
|---|---|
| method | Calibration-Aware Robust Adaptive CPR |
| baseline | original CCISP selector、global/region retune、oracle operating point |
| new action | 由 receiver-known pilot 估 SNR，把估计值送入 operating-region calibration，再驱动既有 CCISP branch action |
| input | pilot observations、receiver-visible estimated SNR、current operating region/GG condition |
| algorithm flow | pilot estimator → mismatch correction → region calibration rule → branch command；P02 `9→11 dB` 只作为 rule component |
| main experiment | **待有界包**：mismatch × GG/operating region × SNR 的统一 paired grid，比较 original/global-retune/full calibration/oracle |
| ablation | estimator only；region rule only；estimator+rule；9 dB vs 11 dB；oracle 只作上界不作 Go 对手 |
| claim | 只允许“接收侧可见校准提高 selector 在工作点失配下的鲁棒性”；不得称全新 selector 理论 |
| difference / independence | Ch3 解决 nominal working point 下选哪一支；本章解决工作点估计错误时如何校准 selector 输入，动作链不同 |
| remaining gap | P01 当前恢复 4/5 harm cells，weak@9 仍有 bias；必须证明 full chain 相对 ordinary global/region retune 有独立增量并形成主图 |

**2A bounded package 的否决条件**：统一 held-out/authority grid 上，full chain 不优于 ordinary global/region retune，或收益只来自某个固定参数值而没有 estimator→calibration→action 的信息增量，则 2A 降为 SUPPORTING_ONLY，Ch4 不得用“边界章”顶替方法。

### Ch5 Low-Complexity Branch-Routed and Fixed-Point CPR（2B）

| 字段 | 合同 |
|---|---|
| method | Low-Complexity Branch-Routed and Fixed-Point Adaptive CPR |
| baseline | route A dual-branch-then-select、float route B、uniform precision ladder |
| new action | selector 在分支计算前发 command，只执行一支；controller path 使用有证据的统一定点格式 |
| input | receiver-visible selector statistic、branch command、quantized controller state |
| algorithm flow | quantize statistics → preselect → run one DA/NDA branch → common compensation；Q(8,6) 是 implementation substep |
| main experiment | **待有界包**：formal full-grid operation count/latency + float-vs-Q BER；若可用，再给 LUT/DSP/power/throughput synthesis |
| ablation | route A vs float route B；float vs Q ladder；uniform vs mixed；selector/branch/total-receiver cost 分解 |
| claim | 先只允许“990/990 selected-output identity + 单分支真实执行”；复杂度/延迟/资源数字必须等新 authority，74.6% 禁用 |
| difference / independence | Ch3 决定算法质量和 branch choice；本章改变计算 schedule 和 numeric representation，贡献对象是 deployment cost |
| remaining gap | formal multi-condition end-to-end cost、warm-up/repetition、float-vs-Q BER 和真实综合；mixed precision 仅 +0.0166 dB，不得作卖点 |

**2B bounded package 的否决条件**：若 end-to-end operation/latency 相对 route A 无可测下降，或 Q-format 在合法 BER 门造成不可接受退化，或所谓节省只来自事后少记已发生计算，则 2B 不能立章，固定点仅留实现附录。

## 3. Spine S2：部署前置 + coded 扩展（不推荐）

| chapter | method | baseline | action/input | main experiment/ablation | claim/independence/gap |
|---|---|---|---|---|---|
| Ch3 | CCISP | fixed DA/NDA | 同 S1 | 已有三档权威结果 | 同 S1 |
| Ch4 | 2B Low-Complexity Branch-Routed CPR | route A、float route B、Q ladder | preselect→single branch；quantized stats | full-grid cost/latency、float-Q BER、位宽梯度 | 有方法形状但部署章前置，先讲 implementation 再讲 receiver extension，叙事依赖倒置 |
| Ch5 | 2C Receiver-Visible Coded Calibration | standard prefix-LS、corrected B0/B2、oracle | prefix-LS→MMSE/LLR | 必须重新 GW 找到相对标准 receiver 的新 action；现有实验只证 correctness | 当前只是修 bug/标准设施，不能形成独立 method claim，和 CCISP branch action 也未统一 |

**为何不推荐**：Ch5 没有现成 deployable delta，强行使用会重演“实现/边界也算方法”的 D023 问题；重启 coded GW 的风险和时间显著高于把 P01/P02 与 route-B/P03 各闭合一个有界包。

## 4. 唯一推荐与 Phase G 判定

**唯一推荐：Spine S1（Ch3 CCISP → Ch4 2A calibration-aware robustness → Ch5 2B low-complexity branch-route+fixed-point）。**

理由按证据排序：

1. Ch3 是唯一 `THESIS_METHOD_READY` 主方法；2A/2B 都已有真实 deployable action 和传统 baseline，不依赖 invalidated/unauthorized 正证据。
2. 12 篇硕士论文显示，方法不必是顶刊级新原语；A3/A8 支持“补可见变量→校准决策”，A1/A5/A7 支持“低复杂度流程→定点/并行/硬件”作为独立方法章。
3. 2A 与 Ch3 的区别是校准输入，2B 与 Ch3/Ch4 的区别是执行 schedule 和数值表示；三章 action object 不同。
4. S1 只需两个有界包；S2 的 coded 章必须新 GW，且当前证据是 correctness repair。

**Phase G 本轮不触发**：内部资产足以定义 Ch4/Ch5 的具体方法链，缺的是两个 bounded validation packages，不是“找不到该找什么”。因此不创建 `missing-method-search-target.md`，也不泛搜 AMC/ML/FSO 新方向。若 2A 或 2B 按上述否决条件 FAIL，才在后续新对话按失败章的 method shape 单独进入 Phase G。

## 5. 下一合法动作

另开执行对话，先走 sim-preflight 与所属 GW gate，只执行 **2A calibration-aware cross-grid bounded package**；不要同时跑 2B，避免一次跨两个方法假设。2A 通过并登记 V### 后，再单独为 2B 建 formal cost/latency+float-Q package。正式 Ch4/Ch5 WRITE 在对应方法晋级前继续暂停。
