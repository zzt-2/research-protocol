# [R002] Post-T009 carrier remap 与 B10 source-native 方法合同

> 2026-07-26 | 关联：2026-07-23-research-direction-lab-longitudinal-test / D005

## 调研问题

T009 以 `BLOCKED_IDENTITY / mission_method_delta=NONE` 收口后，哪条路线最可能在一个
有界 Step 4a 包中形成合法 `METHOD_SIGNAL`，而不是继续修 evaluator、跳过 formal
前置或重建过重基础设施？

## 发现

### 1. 比较口径

首轮 R001 已比较 A4、B10/B12、B1 三条 formal-eligible carrier，并逐项说明其他
候选为何不 ready。本轮在 A4 退出后重新比较四条机制不同的后继路线；`formal
readiness` 只由现存 Step 1–3、源闭包、合法 I/O、比较器和可执行路径证明，不继承
旧 portfolio 标签。

| carrier | 方法形态 | 预期增量 | 可包装句 | formal readiness | 最小补债成本 | 失败后的轮换点 |
|---|---|---|---|---|---|---|
| **B10 source-native adaptive pilot-RLS** | 前 128 个连续已知 16-QAM pilot 训练二参数 RLS，随后严格 DD；在原文 fixed forgetting 上增加 receiver-visible innovation freeze 与有界 variable forgetting | 在星地 GG 低 SNR/深衰落使 DD residual 失真的区间，减少错误更新和发散；相对 fixed source-native B10、幅度门控 cheap rule 与传统 4OPM+BPS/DPLL 形成直接算法比较 | “面向星地高阶 QAM 深衰落决策错误的创新量门控自适应 pilot-RLS 载波同步。” | **FORMAL_READY_WITH_SOURCE_NATIVE_IDENTITY_GATE**：L20/B10-Q1/Q2 Step 1–3 已有，formal D012 曾合法激活且 T006 verdict 被拒收、family 未 Kill；Springer 2024 全文与 PDF 元数据闭合，可精确恢复 128-pilot training→DD、RLS 递推和初始化。旧实现不可复用为科学身份 | 一个隔离 source-native runner：冻结可重建 pilot manifest、同一 TX 侧 channel、原文生命周期；identity 过门后同包跑 fixed / innovation gate / adaptive forgetting | source-native 1/10 GHz smoke 失败即 `BLOCKED_IDENTITY`，不修 T006 全栈；source identity 通过但方法无增量则记 `METHOD_FAIL_WITH_SPACE` 或 `PACKAGING_BOUNDARY`，转 C15 Step 1–3 或新的 formalization |
| **C15 reduced-constellation cost** | 低复杂度星座约简或候选相位代价 | 若合法建立 M-C-A，可能形成复杂度/性能折中 | “面向高阶 QAM CPR 的约简星座低复杂度相位代价。” | **NOT_FORMAL_READY**：现有 sandbox 是 unequal-step confound；当前 formal owner 没有新候选 Step 1–3、四判据 Q# 与 Step 4a 激活。直接 MVE 违反 FR-22 | 完整完成 Step 1–3、竞争碰撞与 Step 4a A0/A′/A/B；不是一个执行包内的小 adapter | 完成 Step 1–3 后若 M-C-A/传统 baseline 仍成立，再进入下一轮 remap；现在不运行 |
| **B1 adaptive phase window** | receiver-visible 条件下选择 VV/phase window | 固定窗在噪声/相位创新比变化时可能非最优 | “面向 GG block-SNR 与 Wiener PN 的自适应相位窗。” | **FORMAL_ELIGIBLE_BUT_CURRENTLY_PROHIBITED**：Step 1–3 与 family 均未 Kill，但 T007/T008 连续暴露 no-crossing proxy、oracle、π/2 resolve、BER population 和 artifact closure；D002/D014 明确停止当前实现 | 重建整个 evaluator/working region；会成为第三个同轴 evaluator repair | 只有独立合法 evaluator 或新外部证据出现才复议；不得从 T008 继续修 |
| **B9 DRE/self-coherent** | 用虚拟载波与数字分辨率增强绕过/弱化传统 CPR | 可能在低 PNOB 下形成接收架构增量 | “面向低分辨率相干接收的数字分辨率增强自相干架构。” | **NOT_FORMAL_READY / INFRASTRUCTURE_HEAVY**：原锚在光纤/自相干架构，当前星地 formal owner 无激活；需要 oversampled waveform、DAC/ADC quantization、matched filter 与 block Viterbi 全链 | 新接收架构和评价链，成本显著高于 B10 source-native reconstruction | 只有当前 CPR 类 ready work 失效且完成独立 Step 1–3 迁移论证后再评 |

### 2. B10 source-native 事实闭包

来源为 Deka、Sharma、Krishnamurthy，*Photonic Network Communications* 47:
164–171 (2024)，DOI `10.1007/s11107-024-01019-2`。共享论文库
`metadata.json` 记录 Springer PDF 成功获取且 title/DOI 匹配；结构化全文提取与
`content.md` 定向核对支持：

- PDM-16QAM、28 GBd、前 128 个**连续**已知 pilot，训练后切 DD；
- 输入 `x_k=[1,k]^T`，相位观测为 `unwrap(angle(r_k/s_k))`；标准 RLS
  `κ/h/P` 递推，`h_0=0`、`P_0=δ^{-1}I=0.5I`、`δ=2`；
- 训练完成后一次冻结相位周期 `F`，DD 期预测、去旋、16-QAM 硬判、以 residual
  phase 更新；全链选定 radians，禁止 degree/radian 混用；
- 论文以 1–10 GHz CFO、50 kHz–1.45 MHz linewidth、OSNR 26 dB 展示工作区，
  主传统比较器为 4OPM+BPS（32 test phases）；
- 未闭合项包括 pilot 具体序列、negative/zero `h1` 的 `F` 处理、逐偏振共享状态、
  精确最优 `λ` 表和显式 ambiguity 处理。T010 因而只在 positive residual CFO
  形成 claim，并把其余轴保留为 claim ceiling。

这里的 `source-native` 只指 estimator 的 128-pilot/RLS/DD 生命周期，不表示
primary 星地链路是 B10 原生系统。B10 原文为 28 GBd PDM-16QAM 光纤链路并报告
26 dB OSNR；没有给出把 OSNR 换成离散 AWGN \(E_s/N_0\) 的参考带宽与归一化，
二者不得混写。primary 的 2.5 GBd 必须从 `B5Params.R_SYM_B5` 读取，证据是
DOI `10.1016/j.optcom.2024.130981` 的 2.5-GBaud PM-QPSK 星地下行/B2B 实验，
只标 `SOURCE_TRANSFER`，不支撑 16-QAM source identity。电 SNR
`[14,17,20,23,26] dB` 只是 `UNVERIFIED_PROJECT_DECLARED_RANGE` 的 validation
定位网格，不是文献性能点。

T006 不能作为 B10 身份：它使用稀疏 1/64 pilot、非 16-QAM pilot、过早 DD/过早
冻结 `F`、自行 P reset、pilot/data channel 重构以及 post-hoc TX-truth resolve。
T010 只能把 T006 当 failure fixture，不能复制其 estimator 作为 P1。

### 2.1 增量方法的邻近先例与证据上限

P2/P3 不是凭空发明，但当前本地证据只支持“邻近机制先例”，不能把它们写成这些
论文的 source-native 复现：

- Zheng 等，ICAIT 2025，DOI `10.1109/ICAIT66450.2025.11353303` 的公开摘要明确
  报告卫星群时延失真信道中的 ASFRLS-CMA：按收敛状态在粗/精模式间自适应设置
  RLS-CMA forgetting factor。它支持“卫星自适应 RLS 遗忘因子”这一方法族先例，
  不支持本包的具体 `λ_k` 映射或光学 CPR 性能。
- Song 与 Liu，*Chinese Journal of Aeronautics* 2015，DOI
  `10.1016/J.CJA.2015.05.001` 的公开摘要明确报告低 SNR 深空载波跟踪中的
  innovation adaptive control，用于抑制滤波发散。它支持“载波跟踪用 innovation
  控制更新可靠性”这一邻近先例，不支持把 Kalman 公式直接移植为 RLS update-freeze。

两条元数据分别保存在主仓库
`search-archive/2026-06-22/satellite-optical-equalization-residual.json` 与
`search-archive/2026-05-31/phase-locked-loop-adaptive-bandwidth-deep-fading-carrier-tra.json`。
因此 T010 的创新边界是：在 source-native B10 上做可审查的有界工程适配，并由
held-out evidence 判断是否可包装；不能声称首创 adaptive forgetting、innovation
control，亦不能把摘要级先例冒充精确公式来源。

### 3. 三种设计方案

1. **B10-only source-native + 同包两种有界 adaptation（推荐）**：先建立可失败的
   原文 identity smoke，然后比较 P1 fixed B10、P2 innovation-gated update、
   P3 lagged-innovation variable forgetting，以及幅度门控 cheap rule。源债最小，
   方法差异可独立归因。
2. **B10+B12 source-native 组合**：理论上可做 coarse→residual cascade，但 B12
   核心公式和全文身份仍未闭合；再次组合会把 source reconstruction、channel
   transfer 与方法归因混在一包，复刻 T006。
3. **先做 C15 Step 1–3，再做新 MVE**：机制不同且适合作为下一轮换点，但至少要
   完成一个完整 formal 前置周期，本包无法直接产生方法比较。

### 4. 为什么推荐项更可能产生 METHOD_SIGNAL

- **相对 C15**：B10 已有 L20/B10-Q1/Q2、formal D012 和可获取全文，当前缺的是
  一个明确且可测试的 source-native implementation；C15 连合法 Q#/Step 1–3
  都未闭合，本轮只能产前置材料。
- **相对 B1**：B10 是一次新的 source-native 方法轴；B1 再继续会成为第三个同轴
  evaluator repair，且当前 working region、oracle 与 BER population 同时失效。
- **相对 B9**：B10 复用现有 16-QAM/GG/CPR 基础，只需隔离生成器和 estimator；
  B9 要新增 oversampling、quantization、matched filtering 和自相干检测全链，
  最小补债成本与归因风险显著更高。

推荐项仍不是预支 Go。源生 smoke 只证明身份，测试 PASS 不算方法；只有 held-out
paired comparison 同时胜过 source-native fixed B10、obvious cheap rule 与
validation-frozen conventional B*，且共同真实 HD-FEC crossing、全 seed
`BER<0.2`、信息边界和统计门闭合，才可记 `METHOD_SIGNAL`。no-crossing/collapse
只允许形成 outage/boundary 包装，不得用 BER→Q² 非线性制造 Go。

## 结论

激活 `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`，仍处于 GW Step 4a 维度 D。下一包
T010 采用方案 1：

- P1：source-native fixed-`λ` B10；
- P2：只用 receiver-visible normalized innovation，超阈值时冻结当次 DD
  `h/P` 更新；
- P3：只用滞后一拍/EMA innovation 决定有界 `λ_k`，其余与 P1 同构；
- cheap rule：只按接收幅度冻结更新；
- conventional B*：同一 waveform/evaluation population 上 validation-frozen 的
  4OPM+BPS 与 4OPM+DD-DPLL；oracle 只作上界。

若 identity 过门，必须同包完成方法比较；不另派纯 repair 包。失败后优先转 C15
Step 1–3 formalization，不修 T006/B12 组合，也不返回 B1/T008 或 A4/T009。

## 对决策的影响

- live 新建 D006，control 升至 epoch 17，checkpoint 保持 CP009；
- formal 新建 D017，激活 B10 source-native adaptive RLS carrier；
- 准备 T010；独立 verifier 通过前不执行实验；
- 本比较与后续任务都不进入 Step 5/Contract/Execute。
