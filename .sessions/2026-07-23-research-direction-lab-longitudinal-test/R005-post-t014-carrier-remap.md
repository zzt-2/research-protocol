# [R005] Post-T014 carrier remap 与 B12 standalone 正向方法合同

> 2026-07-27 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D017 / formal D028

## 调研问题

T014 以 `BLOCKED_SEARCH_COVERAGE / mission_method_delta=NONE` 收口且 B9 的唯一
Step 1 repair 已消费后，哪条合法路线最可能在下一包直接形成
`CONSTRUCT_CREATED / FAIR_COMPARISON_RUN / METHOD_SIGNAL`，而不是继续产出
formalization、task repair 或 evaluator repair？

## 发现

### 1. 当前 readiness 结论

本轮没有三个可直接激活的 legal scientific carrier。只有 B12-Q2 standalone
达到 `NEEDS_SMALL_ADAPTER`，可在现存 Step 1–3 证据上进入 GW Step 4a 方法包。
C15 是合法的 formalization workline，但仍为 `HYPOTHESIS_ONLY`；B1、A4、B10
和 B9 均有显式 no-repair/return 边界。下表逐项比较并证明其 formal readiness，
不把“有代码”“有全文”或“family 未 Kill”偷换成 runnable carrier。

| candidate | 方法形态 | 预期 method delta | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **B12-Q2 source-structured MAP standalone + fade-reliability AOPN（推荐）** | 按 OECC 2025 Eq.4–7 与其 TSP 2022 [5] 的协方差定义重建 pilot-aided ML/MAP；只用接收端可见幅度/innovation 构造异方差 AOPN 权重并做有界可靠度 clipping，防止深衰落相位 outlier 被过度信任；不接回 B10，不做 CW+MAP | 同包应先得到 `CONSTRUCT_CREATED`，随后在 source-structured PA/PA-ML/MAP、cheap fixed-variance/hard-skip 和 validation-frozen BPS/DD-DPLL 上完成 `FAIR_COMPARISON_RUN`；只有稳定胜过 MAP、cheap rule 和传统 B* 才是 `METHOD_SIGNAL` | “面向深衰落星地高阶 QAM 的幅度可靠度约束 ML/MAP 载波相位恢复，通过接收幅度与 innovation 驱动的异方差 AOPN 权重及有界稳健化，在保持前馈结构的同时抑制深衰落下的相位估计失稳。” | **NEEDS_SMALL_ADAPTER / FORMAL-ELIGIBLE**。`literature_notes.md` 的 B12-Q2 已有 M-C-A、方法形态和 3.5/1 dB 同族锚；formal D012 明确承认 B12 Step 1–3。T006 只使组合实现 `UNRESOLVED_IMPLEMENTATION_INVALID`，formal D013 没有 Kill standalone family。OECC 2025 与 TSP 2022 [5] 全文均已落盘，可闭合 Eq.4–7、Σθ 与单正弦 AOPN Σε；OECC 未给 W、pilot sequence 和 penalty 精确定义，故只能主张 structural identity，不能冒充 bit-exact reproduction | 一个隔离包：登记 metadata 债，新增 square-256QAM 小适配，逐式实现 Eq.4–7/协方差，显式冻结 W/pilot/SNR 为 project validation assumptions，复用同一 TX/同一 GG+Wiener realization；先 structural identity smoke，过门后同包完成 robust construct 与 paired comparison | structural identity 不能闭合或无法复现 `MAP > PA-ML > PA` 定性排序即 `BLOCKED_IDENTITY` 并轮换；共同工作区不存在则只记 boundary；robust MAP 不胜 MAP+cheap+B* 则记 `FAIR_COMPARISON_RUN`，不开第二个 B12 包 |
| **C15 collapse-safe staged blind equalizer** | receiver-visible confidence 门控、scale-normalized CMA→RDE/ring-aware 分阶段均衡 | 当前下一包最多关闭 source/canonical readiness，`mission_method_delta=NONE`；至少还需 Step 3 精读/Q# 后才可能 `CONSTRUCT_CREATED` | “面向动态星地 PM-16QAM 湍流与 SOP 漂移的接收可见置信度门控、尺度公平分阶段盲均衡方法。” | **HYPOTHESIS_ONLY / NOT SCIENTIFIC-CARRIER-READY**。T011 只有 OpenAlex 一个真实 search source，Step 1 未完成；T012 是 `BLOCKED_TASK_INTERFACE / PACKAGE_NOT_EXECUTED`，Step 2/3 从未启动。旧 shared-μ 结果又有约 19× gradient-scale confound，不能继承机制结论 | 新的 disk-native formalization 包 + 独立 Step 3 精读/Q# 包；须闭合三源、3/3 canonical、五篇 recent identity、JR-CMA/VAE/CMA→RDE collision 和 tuned comparator | 新 source 包仍不足三源/canonical 3/3 即返回池；Step 3 找不到直接 M-C-A 或形态被竞争者占满则不进 MVE；不得做 T012 第四次 amendment |
| **B1 adaptive phase window** | 依据 receiver-visible 条件选择 VV/phase window | 理论上可形成 adaptive-window construct，但下一动作首先仍是 evaluator/working-region rebuild，不能合法预期方法 delta | “面向 GG block-SNR 与 Wiener phase noise 的自适应相位窗。” | **FORMAL-ELIGIBLE FAMILY BUT PROHIBITED CURRENT CARRIER**。formal D014 明确 family 未 Kill，但 T007/T008 已连续暴露无 FEC crossing、proxy dB、oracle、π/2 branch、BER population 和 artifact closure；禁止第三个 B1 repair | 重建整个 data population、ambiguity、per-block oracle、窗口集合和真实 FEC crossing；是第三个同轴 evaluator repair | 只有新的独立 evaluator 资产或外部证据改变 readiness 才可复议；当前不得从 T008 继续 |
| **A4 deployable adaptive CPR** | per-block receiver-visible condition 驱动 DA/NDA 或 CPR policy | 旧方法形态清楚，但下一动作需重建 pilot/TX-truth、DA/NDA frequency stage 和 working region，属于第二 identity repair | “面向星地高阶 QAM 条件变化的可部署 CPR 选择策略。” | **RETURNED / NO-SECOND-REPAIR**。T009 因四类 P0 身份缺陷停止，P1–P3 未运行；live D005 已禁止第二个 A4 evaluator repair | 重建四层 identity/evaluator 后才能重新比较，成本与归因风险均高于 B12 isolated standalone | 仅当独立新资产一次性闭合四类身份缺口才复议；不能从 T009 续修 |
| **B10 source-native adaptive pilot-RLS** | 128 contiguous pilot→DD RLS 上的 innovation freeze / variable forgetting | C1 仅形成 contract，C2 在 source-native lifecycle branch identity 失败；再开包仍先修 identity，不能预期方法 delta | “面向深衰落决策错误的 innovation-gated adaptive pilot-RLS CPR。” | **RETURNED / NO-SECOND-B10-PACKAGE**。T010 在 validation matrix 首个异常处证明 P1/P2/P3 共用 initialization branch 失效；live D011/formal D022 已返回池并禁止第二包 | 重建 unwrap/initialization 生命周期并重跑冻结矩阵，属于第二 B10 identity package | 只有 source-native 外部实现或新身份资产出现才复议；不得借 B12 把 B10 接回 |
| **B9 DRE self-coherent** | virtual-carrier self-coherent + digital resolution enhancement | Step 1 仍 blocked，下一包只能继续 coverage repair，且该 repair 已被禁止 | “面向低分辨率相干接收的数字分辨率增强自相干架构。” | **RETURNED / STEP1_SEARCH_COVERAGE_BLOCKED**。T013/T014 实际来源 union 只有 OpenAlex+IEEE；formal D028 禁止第三个 B9 Step 1 包 | 新外部 source capability、完整 oversampled/quantized/self-coherent 接收链和传统 comparator | 只有外部 source 能力或正式范围变化时重新评价；当前不得原样重试 |

### 2. B12 standalone 与 T006 的身份边界

B12 standalone 不是被禁止的 T006 组合修复：

1. formal D013 拒收的是 B10+B12 combination implementation，并把 family 标为
   `UNRESOLVED_IMPLEMENTATION_INVALID`，没有作 family Kill；
2. T006 的 B12 实现以 `Sigma_phi @ z_unit` 自行重构 image-only 公式，并让
   pilot/data 经过不同信道；新 carrier 禁止复用该实现；
3. OECC 2025 原 PDF 的 Eq.6 是
   \(\hat\theta_0=(\mathbf1^T\Sigma_\varphi^{-1}\varphi)/
   (\mathbf1^T\Sigma_\varphi^{-1}\mathbf1)\)，以及
   \(\hat{\boldsymbol\theta}=\Sigma_\theta
   (\Sigma_\theta+\Sigma_\epsilon)^{-1}
   (\varphi-\hat\theta_0\mathbf1)\)，另有 Eq.4、Eq.5 和 Eq.7 的完整生命周期；
4. 新路径只允许从 PDF 逐式实现 source-native PA/PA-ML/MAP，再添加
   receiver-visible reliability bounding。其 reference [5]（Wang 等，IEEE TSP
   70:337–350, DOI `10.1109/TSP.2021.3137966`）已在本地落盘，闭合
   \([\Sigma_\theta]_{ij}=\min(i,j)\sigma_p^2\) 与单正弦 AOPN 对角
   \(\Sigma_\epsilon\)；但 OECC 的 W、pilot sequence、sample count、seed 和
   penalty 口径未给出，必须标 `PROJECT_VALIDATION_ASSUMPTION`，不得宣称完整数值
   复现。禁止 coarse→MAP cascade、B10 回接、
   CW pilot 双导频和未经来源闭合的联合 CFO ML。

现有
`projects/simulation/explore/adaptive-phase-window/channel.py` 已有 pilot-before-channel、
同一 GG+Wiener realization 的生成路径；缺口主要是 isolated MAP adapter、
square-256QAM 和 metadata correction，不是新接收基础设施。

### 3. 正向方法合同

- `positive_method_target`：
  `B12_MAP_FADE_AOPN_STANDALONE`。对 source-native MAP 的
  \(\Sigma_\epsilon\) 做 receiver-visible、因果、有界的幅度可靠度稳健化。
- `minimal_construct`：
  source-structured MAP + 一项预注册的 amplitude/innovation reliability bound
  （observation-precision / standardized-residual clipping）；
  如 identity 与 direct-information tests 通过，再比较一个因果平滑变体，但不把
  多个 post-hoc 变体混作主方法。
- `fair_comparator`：
  source-structured PA、PA-ML、MAP；fixed AOPN variance 或 hard fade skip；
  同一 transmitter/pilot overhead/data mask/realization 上 validation-frozen
  BPS 或 DD-DPLL。
- `primary_packaging`：
  深衰落星地高阶 QAM 的幅度可靠度约束 MAP CPR。
- `fallback_packaging`：
  source-native MAP 在 GG 深衰落下的 working-region/失稳边界，以及
  low-complexity robustness–performance trade-off；negative result 仍不算主方法。
- `next_positive_action`：
  一个隔离 T015 先完成 source-like structural identity +
  direct-information tests；身份过门
  后同包创建 robust construct 并运行公平 paired comparison。

### 4. adaptation-scan 与失败截断

- A1 参数适配：只检验 variance bound 的最优值是否随 receiver-visible fade
  reliability 改变；若单一 fixed 值全条件占优，不卖 adaptive。
- A2 结构适配：原 MAP 的高 SNR AOPN/协方差可逆假设在深衰落下是否失效；若 exact
  MAP 数值稳定且无失效区，不加稳健层。
- A3 组合适配：明确排除 B10/CW/DPLL 级联，避免重演 T006。
- A4 条件适配：预注册 exact MAP 与 robust MAP 是否随 fade severity 发生有物理
  因果的 crossover；无 crossover 不做切换包装。
- A5 评价维度：BER/SER 之外只使用预注册的 block-outage、phase-error 与 solver
  stability；不得“换指标直到赢”。
- A6 失效边界：以 covariance conditioning、phase-error 和共同 BER working region
  定义深衰落失效边界。

退出条件是单包制：source-like 结构/排序不符即身份阻断；方法不过 MAP、cheap
rule 和传统 B*，或 clean/source-like 退化超过预注册容限，即不记
`METHOD_SIGNAL`，B12 返回池并轮换到新的 mechanism family。禁止第二个 B12
repair 包。

### 5. 为什么 B12 比至少两个替代项更可能产生 METHOD_SIGNAL

1. **相对 C15**：B12-Q2 已有 candidate-specific Q#、现存 Step 1–3、OECC 与
   TSP [5] 全文和可闭合结构公式；C15 的下一包仍只能补 Step 1/2，至少还隔一个 Step 3 包，
   method delta 必为 `NONE`。B12 的下一包可在同一身份门后立即创建和比较方法。
2. **相对 B1**：B12 是新的 standalone method axis，缺口是一个隔离公式 adapter；
   B1 必须第三次重建 evaluator/working region，且已被 formal D014 明确禁止。
3. **相对 A4/B10**：两者各自的第二 identity package 已被 live D005/D011
   排除；B12 不复用其失效代码或 state lifecycle，归因边界更清楚。
4. **相对 B9**：B12 不依赖新的 source capability，也不需要 oversampled
   self-coherent/quantization 全链；B9 已消费唯一 Step 1 repair。

因此 B12 不是预支 Go，而是当前唯一能把“身份验证”与“最小正向构造+公平比较”
放在同一包、并有明确一次性退出点的候选。

## 结论

选择 `B12_MAP_FADE_AOPN_STANDALONE` 作为新的 active scientific carrier，仍处于
GW Step 4a 维度 D。先由 live/formal decision 激活并冻结 T015，再由独立 verifier
审查 source identity、公式、参数、比较器、working region、seed/metric 和
single-package stop contract；审查 PASS 前不运行任何实验。

## 对决策的影响

- live 应新建 D018，formal owner 应新建 D029；
- foreground 应从 epoch 35 / CP014 递增到新的 B12 standalone task-preparation
  epoch，mission checkpoint 仍保持 CP014；
- 新建 T015；T015 被接受前不追加 CP015，不改变 no-method=14；
- T015 完成后必须由不同 agent 独立裁决
  `formal_science_disposition` 与 `mission_method_delta`。
