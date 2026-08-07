# 每个核心技术章都有方法：候选 Thesis Spines

> 2026-08-07 | owner: `.sessions/2026-07-09-thesis-writing` / S018；authority: RDL D036/V020
> 状态：Ch5 scheduling-only 方法包已就绪；不授权新算法、fixed-point、硬件综合或新实验。

## 1. 候选方法终态

| candidate | action chain | baseline | grade | 当前判断 |
|---|---|---|---|---|
| **2A Calibration-Aware Robust Adaptive CPR** | pilot-SNR estimate → operating-region calibration → CCISP branch action | original selector、global/region retune、oracle operating point | **NEEDS_ONE_BOUNDED_PACKAGE** | 有统一 input-action-output 和 4/5 harm-cell 恢复，最像 A3“补被忽略变量后重估”和 A8“estimated SNR→threshold decision”；但必须证明不是普通 `ref 9→11 dB` 已完全吸收 |
| **CCISP Select-Before-Execute Single-Branch Receiver Architecture** | receiver-visible selector → branch command → only selected recovery branch → common detector | route A dual-branch-then-select | **THESIS_ENGINEERING_METHOD_READY** | scheduling-only 已闭合 396,000 窗输出/BER identity、seed-cluster timing 与 typed operations；历史复合 2B 继续 SUPPORTING_ONLY，Q(8,6) 失败不进入本方法 |
| **2C Receiver-Visible Coded Calibration** | prefix-LS → channel/noise estimate → MMSE/LLR | standard prefix-LS、corrected B0/B2、oracle | **SUPPORTING_ONLY** | 当前主要是修 hidden-gamma bug 的 receiver correctness infrastructure；没有相对标准 prefix-LS 的新 action。若另找 coded 方法须新 GW，不能续包装当前资产 |
| **2D Risk-Aware Rate/Outage Control** | receiver state → conditional risk → rate/no-transmit | conventional outage margin、fixed-rate、oracle | **NEEDS_NEW_GW** | 方法形状成立，但 9/27 和 +5.1%–6.7% 全属 unauthorized dev-only；需重新授权、修 testbed/contract 并做 held-out paired validation |

### 不能单独命名成方法的组件

- 2A：fixed 13 dB、`ref=11 dB`、weak-region label、某个 estimator 或 CV threshold 是参数/校准规则。
- Ch5：Q(8,6)、uniform/mixed precision、resource proxy 不能纳入 scheduling-only 方法；990/990 是覆盖口径，396,000 窗 mismatch=0 是等价性证据，均不是新算法。
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

### Ch5 CCISP Select-Before-Execute Single-Branch Receiver Architecture

| 字段 | 合同 |
|---|---|
| method | CCISP Select-Before-Execute Single-Branch Receiver Architecture |
| baseline | route A dual-branch-then-select |
| new action | selector 在分支计算前发 command，每窗仅执行被选 DA/NDA 恢复分支，再进入公共检测器 |
| input | 与 CCISP 相同的 receiver-visible selector statistic、raw window、配置与 DA pilot |
| algorithm flow | receiver-visible selector → branch command → only selected recovery branch → common downstream detector |
| main experiment | 3 scenes×11 SNR×30 seeds×400 windows：逐窗 output/BER identity；冻结 caller-path timing；typed operations |
| ablation | route A vs single-branch；DA/NDA command 分层；controller 固定成本 vs branch 可省成本；scene/SNR/seed 分层 |
| claim | 0/396,000 output mismatch；BF/AF=0.5424、单侧 95% cluster upper=0.5473；分支调用 -50.00%；逐类操作数下降 |
| difference / independence | Ch3 的 CCISP 决定选哪一支；Ch5 不改 selector/estimator，只把选择命令落实为“只执行该支”的部署计算图 |
| remaining gap | 软件 scheduling claim 已闭合；硬件 LUT/DSP/power/throughput 属未来独立合同，不在当前 claim ceiling |

**Ch5 闭合结论**：冻结 caller path 中未选分支确实不被调用；分支调用从 792,000 降至 396,000，
BF/AF seed-cluster ratio=0.5424（单侧 95% 上界 0.5473），且 selected output/BER 完全一致，故达到
`THESIS_ENGINEERING_METHOD_READY`。历史 Q(8,6) fixed-point 仍为失败/支持材料，不影响 scheduling-only 终态。

## 3. Spine S2：部署前置 + coded 扩展（不推荐）

| chapter | method | baseline | action/input | main experiment/ablation | claim/independence/gap |
|---|---|---|---|---|---|
| Ch3 | CCISP | fixed DA/NDA | 同 S1 | 已有三档权威结果 | 同 S1 |
| Ch4 | CCISP Select-Before-Execute Single-Branch Receiver Architecture | route A dual-branch | selector→command→single branch | output identity、timing、typed operations | 工程方法已就绪，但部署章前置会使叙事依赖倒置 |
| Ch5 | 2C Receiver-Visible Coded Calibration | standard prefix-LS、corrected B0/B2、oracle | prefix-LS→MMSE/LLR | 必须重新 GW 找到相对标准 receiver 的新 action；现有实验只证 correctness | 当前只是修 bug/标准设施，不能形成独立 method claim，和 CCISP branch action 也未统一 |

**为何不推荐**：该排序把已经闭合的单分支执行架构提前到 Ch4，却把没有现成 deployable delta 的 coded
correctness repair 放进 Ch5；重启 coded GW 的风险和时间显著高于保持 scheduling-only 为 Ch5 工程方法。

## 4. 唯一推荐与 Phase G 判定

**唯一推荐：Spine S1（Ch3 CCISP 算法方法 → Ch4 calibration-aware robustness → Ch5 CCISP 先选后算单分支执行架构）。**

理由按证据排序：

1. Ch3 是唯一 `THESIS_METHOD_READY` 科学主方法；Ch5 已以真实 deployable scheduling action、传统 route-A baseline 与确定性证据达到工程方法门。
2. 12 篇硕士论文显示，方法不必是顶刊级新原语；A3/A8 支持“补可见变量→校准决策”，A1/A5/A7 支持可审计的低复杂度执行流程作为独立工程方法章。
3. 2A 与 Ch3 的区别是校准输入；Ch5 与 Ch3/Ch4 的区别仅是执行 schedule，不含数值表示，action object 清楚。
4. Ch5 已闭合 scheduling-only 包；S2 的 coded 章仍须新 GW，且当前证据只是 correctness repair。

**Phase G 本轮不触发**：Ch5 的具体方法链与 bounded validation package 均已闭合，不存在新方向检索问题。
因此不创建 `missing-method-search-target.md`，也不泛搜 AMC/ML/FSO 新方向。Ch4/2A 的独立终态不在本轮改写。

## 5. 下一合法动作

Ch5 可直接按 `ccisp-select-before-execute-single-branch-method-package.md` 进入论文写作与图表排版；不得把
历史 2B 复合名、Q(8,6) 或硬件综合 claim 带回正文。Ch4 是否采用 2A 仍由其独立 authority 决定，不在本轮处理。
