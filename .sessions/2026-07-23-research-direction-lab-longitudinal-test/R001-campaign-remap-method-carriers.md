# [R001] Goal campaign remap：方法载体比较与首包选择

> 2026-07-26 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D002

## 调研问题

在 CP001–CP008 连续八包 `mission_method_delta=NONE`、formal owner 明确“无 active
carrier”的状态下，哪一个仍有正式证据链的 carrier 最可能在一个有界执行包内产生
`METHOD_SIGNAL`，而不是再次滑入 evaluator 修复、实现考古或 negative-result 链？

## 发现

### 1. 比较口径

本轮只比较具有既有 formal Step 1–3 或等价正式证据链、且没有 family-level Kill
的三条 carrier。`READY` 不是由旧 portfolio 标签继承，而是按当前代码、比较器、
评价器和 source identity 重新判断。

| carrier | 方法形态 | 预期方法增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **A4 DA/NDA adaptive CPR** | 用 receiver-visible 块统计在 DA 与 NDA CPR 间因果选择；可扩为 validation-frozen monotone selector 与 confidence fallback | 在预注册的跨 SNR/湍流混合工作区内，相对“不适配的单一固定策略”关闭一部分 per-block oracle regret；已有 crossover、选择器和论文结构，最接近直接方法产出 | “面向 Gamma–Gamma 湍流的接收功率感知块级自适应载波恢复，在统一规则下按工作条件选择 DA/NDA 分支。” | **READY_WITH_BOUNDED_IDENTITY_ADJUDICATION**：B11/NDA-ML Step 1–3、A4 Step 4a 实现、30-seed 数据与写作资产均存在；但旧 `+0.27–0.48 dB` 已作废，仍须关闭 common-payload、pilot/ambiguity、receiver-visible input 和包含 DPLL 的 strongest-conventional comparator | 一个隔离 v2 runner；旧 A4 只读复用；不改 common/params/paper；identity 过门后同包完成 P1–P3 与 fresh paired test | 任一基础身份无法在一次有界修复内闭合，或 P1–P3 均不能胜过 validation-frozen strongest conventional strategy：记 `PACKAGING_BOUNDARY` 或 `METHOD_FAIL_WITH_SPACE`，**不再开第二个 A4 修复包**；回 remap 比较 B10 source-native 最小重建与新候选 Step 1–3 |
| **B10/B12 high-order CPR** | pilot-RLS coarse/MAP residual cascade、innovation gate、adaptive forgetting | 若 source-native standalone 在高阶 QAM/GG 条件下恢复合法工作区，组合或 adaptive forgetting 可能形成直接算法增量 | “面向高阶 QAM 星地链路的 pilot-RLS/MAP 组合与创新量自适应跟踪。” | **FORMAL_ELIGIBLE / IMPLEMENTATION_INVALID**：Step 1–3 已有；T006 科学 verdict 被拒收且 family 未 Kill；但 B10 未实现 128-pilot training→DD，B12 核心公式自行重构，pilot/data channel 与 oracle/statistics 同时失效 | 必须重建 source-native B10；B12 公式身份未闭合时不能进入组合；不是一个小 adapter | 若 source-native B10 在合法 AWGN smoke 仍不工作或 robust headroom 不存活，停止，不修 T006 全栈；转新候选 formalization |
| **B1 adaptive phase window** | 按可观测 SNR/phase innovation 选择 VV/phase-estimation window，并加 hysteresis/fallback | 理论上最优窗随噪声与相位创新比变化，可形成轻量自适应窗 | “面向 GG block-SNR 与 Wiener phase-noise 联合变化的低复杂度自适应相位窗。” | **FORMAL_ELIGIBLE / BLOCKED_IDENTITY / RETURNED_TO_POOL**：Step 1–3 已有，family 未 Kill；但 T007/T008 连续两包无方法增量，no-crossing proxy、oracle candidate、π/2 resolve、BER population 与 artifact closure 均未闭合 | 需要重建 evaluator 和可靠 working region，实质是第三个同轴 repair 包 | 当前明确不选；只有未来出现独立合法 evaluator 或外部新证据时才重新比较，不从 T008 继续修 |

### 2. 为什么 A4 比两个替代项更可能产生 METHOD_SIGNAL

1. **比 B10/B12 更接近“动作已存在”**：A4 已有可运行 selector、两条不同输出
   分支、30-seed 结果和论文方法结构；T009 的首要工作是把已知身份债变成可失败
   smoke，并在同包直接比较三个 deployable construct。B10/B12 的核心 estimator
   本身尚未 source-native 成立，先修 estimator 才谈得上方法。
2. **比 B1 更少同轴漂移**：A4 本轮是新 carrier 的第一次 formal adjudication；
   B1 已连续 T007/T008 两包、当前 evaluator 不在可靠 working region，继续等于
   第三个同轴修复包，直接违反 mission 的轮换纪律。
3. **有可检验的正向机制而非只剩负面资产**：A4 的 DA/NDA crossover 与 per-block
   oracle gap 为方法构造提供可失败的机制锚；旧数据不自动构成方法信号，但足以把
   “是否能用一个 receiver-visible frozen selector 胜过不适配策略”压缩成一个包。

这只是相对排序，不预支正面结论。T009 必须把 always-DA、always-NDA、
已通过 S011 的 DPLL 异族传统 baseline、validation-frozen global best、
per-condition fixed 与 per-block oracle 分开。`B*`/`B-cond` 必须从
DA/NDA/DPLL 集合中选择；若自适应只胜固定 NDA、却被 always-DA、DPLL 或合法
global best 支配，最高只能是
`PACKAGING_BOUNDARY`，不得报 `METHOD_SIGNAL`。

### 3. 其他候选为何不满足 formal readiness

| 候选 | 当前证据 | 不满足 formal readiness 的原因 |
|---|---|---|
| B2 fade-freeze pilot fallback | B2 D004/K001，topic closed | 21 点救援后三个 Go 全 FAIL；同口径分解证明所谓增益不存在，family 已 Kill |
| B3 joint estimation | B3 D004/K001，topic closed | CPE joint CRB 约 0 dB；块间 Doppler 变化比 FOE 分辨率低约 5 个数量级；三切口物理 FAIL |
| B7 Gardner-TED FOE | B7 D008，topic closed | 公平 LPF2 后相对 4th-power 仅约 +0.03 dB；±25 GHz range 优势不对应 LEO 实需；family 已 Kill |
| C15 reduced-constellation cost | live D001 / portfolio current | 只有 unequal-step confounded sandbox；新候选 Step 1–3 未完成，直接 MVE 违反 FR-22 |
| B9 DRE | formal D013 排除项 | 需要 oversampled waveform、低分辨率 DAC、MF 与 block-wise Viterbi 全链；无当前 formal activation |
| Pilot-Jones | D066/V040 | fixed complex component rescue axis 已 scoped Kill；family 仍有 4 篇全文债，但没有本轮可执行正向 method contract |
| P03 / Scout F1–F4 | D022 / current portfolio | Scout dormant；F1 testbed blocked、F3 无有效 Probe、F4 coded-chain blocked；不得从 sandbox 标签恢复正式授权 |

## 结论

选择 **A4 deployable adaptive CPR** 作为 campaign remap 后首个 active carrier，状态为
`READY_WITH_BOUNDED_IDENTITY_ADJUDICATION`。下一包必须同时做：

1. 一次有界、可失败的 physical/information/evaluator identity preflight；
2. preflight 通过后直接实现/冻结 P1 现有两级规则、P2 monotone validation selector、
   P3 confidence-safe selector；
3. 用 fresh paired mixed-condition traces 比较 strongest fixed strategies 与 oracle；
4. 输出 method card 和严格的 `METHOD_SIGNAL / PACKAGING_BOUNDARY /
   METHOD_FAIL_WITH_SPACE / BLOCKED_IDENTITY` 四态之一。

失败不等于 Goal 结束；A4 不开第二个 repair 包，主控在验收后更新 CP009 的 method
delta、same-axis/repair/no-method streak 与 drift，再自动进行下一轮 carrier 比较。

## 对决策的影响

- live owner 新建 D003，control epoch 由 13 升为 14，唯一科学动作绑定 T009；
- formal owner 新建 D015，激活 `A4_DEPLOYABLE_ADAPTIVE_CPR`，仍止于 GW Step 4a；
- mission checkpoint 仍为 CP008，T009 被主控接收后才可追加 CP009；
- 不恢复 B1/T008、B10/B12 repair、Pilot-Jones、P03 或 dormant Scout。
