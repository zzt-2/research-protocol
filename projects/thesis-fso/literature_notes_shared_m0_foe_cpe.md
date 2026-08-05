# Literature Notes — Shared M0-Power FOE–CPE Groundwork

> Project: thesis-fso | 子方向: Ch5 工程方法候选 P1（Shared Raised-Power Compute Graph）
> 状态: **GW Step 3 证据闭合（terminal=`RECENT_BASELINE_UNAVAILABLE`；P1=`SUPPORTING_ONLY`）** | 最后更新: 2026-08-05
> 边界: 本文件只给 Step 3 精读与问题提取裁决；不构成 Step 3.5、Step 4a Go/Kill、novelty 或实现授权。

## 0. 冻结研究对象

- **M**：当前串行 NDA carrier recovery 先用 M0 次幂做 FOE，再对 CFO 补偿信号重做 M0 次幂做 CPE。
- **C**：资源受限的软件或硬件实现，要求与当前 receiver 输出/BER 匹配。
- **A**：用一个共享 M0-domain 表示同时驱动 FOE 与 CPE；升幂域 CFO 去除用
  `raised * exp(-j*M0*omega*k)`，原信号域补 `omega*k + phi`。

## 1. GW Step 进度表

| Step | 状态 | 完成日期 | 关键产出 | 下游门控 |
|---|---|---|---|---|
| 1 search | ✅ | 2026-08-05 | raw=100、dedup=97、3 个实际 API 家族 | 已满足 |
| 2 acquire | ✅（V002 PASS） | 2026-08-05 | 12 篇合格全文，2 篇 HIGH★ direct | 已满足 |
| 3 read | **⛔ 证据闭合** | 2026-08-05 | 9 篇原精读 + 3 篇 recent targeted re-read；bounded search 6/6；Q-P1-01 仍无合法 Q# | terminal=`RECENT_BASELINE_UNAVAILABLE`；P1=`SUPPORTING_ONLY`，停止本方向 |
| 3.5 supplement | ⬜ 未授权 | | | 禁止进入 |
| 4a feasibility | ⬜ 未授权 | | | 禁止进入 |

`stages/gw-read.md` L198 明定：没有通过 canonical 四判据的 Q# 时不得进入 Step 4a；
`stages/glossary.md` L65–70 指定先回 search 扩检索。本专题已按 D005 完成最后一次 bounded 回查并触发
用户定义的停止 terminal；这仍不是 Step 4a Go/Kill。

## 2. 精读论文与身份

九篇均由 fresh-context worker 全文读取并执行 title 自检；全部 PASS。逐篇完整条目位于
`papers/_read_notes/`，所有事实回指各自 `content.md`。

| ID | 年份/角色 | title/identity | P1 关系 | 关键证据 |
|---|---:|---|---|---|
| 10.1109/CSNDSP.2014.6923933 | 2014 HIGH★ direct | *Frequency Offset Estimation and Carrier Phase Recovery…VV Monomial Estimator* — PASS | 方法族邻近；同一序列共享 **否** | FOE/CPR 输入与阶数不同（`papers/doi/10.1109_csndsp.2014.6923933/content.md` L47–55, L113–117, L151–161, L181–185） |
| 10.1109/JLT.2018.2831918 | 2018 HIGH★ direct | *Simplified Carrier Recovery for Intradyne Optical PSK Receivers in udWDM-PON* — PASS | shared correlation **是**；并引用 2016 shared m-power | `papers/doi/10.1109_jlt.2018.2831918/content.md` L63–77, L79–89, L237 |
| 10.1109/JLT.2009.2024963 | 2009 MEDIUM | *DSP for Coherent Single-Carrier Receivers* — PASS | joint-polarization/phase 背景，低 collision | `papers/doi/10.1109_jlt.2009.2024963/content.md` L3–16, L57–61, L761–829 |
| 10.1109/JLT.2019.2892901 | 2019 HIGH hardware | *LUT-Free Carrier Recovery for Intradyne Optical DPSK Receivers in udWDM-PON* — PASS | LUT-free/去 m-power 替代，不共享 | `papers/doi/10.1109_jlt.2019.2892901/content.md` L66–80, L106–114 |
| 10.1109/LPT.2016.2586076 | 2016 HIGH arithmetic | *Multiplier-Free Carrier Phase Estimation for Optical Coherent Systems* — PASS | multiplier-free CPE 替代 | `papers/doi/10.1109_lpt.2016.2586076/content.md` L29–31, L114–126 |
| 10.1109/ISCAS48785.2022.9937906 | 2022 HIGH FPGA | *A Low-latency Carrier Phase Recovery Hardware for Coherent Optical Communication* — PASS | low-latency VV4E 实现 | `papers/doi/10.1109_iscas48785.2022.9937906/content.md` L7–25, L91, L156–169, L194–212 |
| 10.1109/LCOMM.2026.3653195 | 2026 HIGH hardware | *A Low-Complexity Carrier Phase Recovery Architecture Using Prefix-Sum and CT-MLE…* — PASS | prefix-sum explicit refactor，非跨级共享 | `papers/doi/10.1109_lcomm.2026.3653195/content.md` L169–175, L195 |
| 10.1109/TSP.2021.3137966 | 2022 MEDIUM theory | *Joint ML/MAP Estimation of the Frequency and Phase of a Single Sinusoid With Wiener Carrier Phase Noise* — PASS | 改统计模型的 joint ML/MAP | `papers/doi/10.1109_tsp.2021.3137966/content.md` L9–23, L61 |
| 10.1109/JPHOT.2022.3161795 | 2022 MEDIUM FSO | *Symmetric Training Sequence-Based Carrier Frequency Offset Estimation Scheme for Coherent FSO Communication* — PASS | DA FOE estimator-changing alternative | `papers/doi/10.1109_jphot.2022.3161795/content.md` L9–11, L41–47, L85, L161, L191–195 |

## 3. 两篇直接竞品裁决

### 3.1 CSNDSP 2014

答案是 **否**。它并非让同一个 `x^M`/VV 序列同时驱动 FOE 与 CPR：FOE 对相邻样本乘积形成的
相位增量做 monomial，CPR 对符号本身做 VV/MPE（L47–55, L151–161）；两级最优阶数也不同
（L113–117, L181–185）。L193–195 只提出硬件块“可能共享”，没有实现、数据流或资源证据。

### 3.2 JLT 2018 与 OFC 2016 证据债

JLT 2018 已经做了明确 shared correlation graph：只算一次 `w[n]=r[n]r*[n-1]`，FE 与 PR 共同
消费，并在同 `N=256` 下保持 BER，adder/multiplier/latency 分别约 −23%/−25%/−25%
（L63–89, L119–127, L149）。更强的是正文 L73–75 明确说 Ferreira et al. OFC 2016 已把
differential m-th-power FE 与 Viterbi PR 所需的 m-th power 只算一次并共享，参考文献题名在 L237。

因此：P1 的宽泛工程动作“同一 m-th-power/correlation 中间量供 FOE+CPE 使用”已经被吸收。bounded
closure 中，OFC 2016 官方摘要页可访问，但官方 PDF 端点被 Radware 拦截；同线 PTL 2016 也经
tools/download、arXiv 与 IEEE blit 三轮止损后未取得有效全文。OFC exact-action 裁决为
`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`，不能进一步裁剪其 exact implementation boundary，
也不能据此声称 novelty。

## 4. Comparator、matched-output 与复杂度协议

| 层 | 合法 comparator | 公平性要求 | 指标 |
|---|---|---|---|
| 传统同估计器 | 当前串行 NDA `FOE → CFO correction → CPE` | 同输入、窗口、M0、unwrap、精度和 estimator 参数 | per-sample raised/FOE/CPE/final corrected samples 的 max/mean abs error；BER/SNR 曲线 |
| 显式 conventional refactor | JLT 2018 shared correlation；OFC 2016 shared m-power（待一手全文） | 不改变 estimator、只改变计算图；同 N/word length | real/complex add/mul、LUT、buffer、fan-out、latency、throughput |
| cheap arithmetic | LPT 2016 multiplier-free CPE；JLT 2019 LUT-free CR | 把 estimator-changing 与 pure refactor 分层，不混做 matched-output | operation counts、memory/LUT、BER/SNR penalty |
| 硬件实现 | ISCAS 2022、LCOMM 2026、JLT 2019 | 报 core 与 full-chain；固定工艺/位宽/频率 | area/LUT/DSP、power、critical path、cycles、Gb/s/GBd、efficiency |
| estimator-changing | TSP joint ML/MAP、JPHOT FSO training-sequence FOE | 单列，不冒充 same-estimator refactor | estimator MSE/range、BER/sensitivity、额外先验/训练开销 |

matched-output 的最低验证契约是：同一输入上逐样本核对 raised array、FOE estimate、CPE estimate、
最终校正复样本；浮点报告 max/mean absolute error，固定点预先冻结 tolerance；再比较完整 BER/SNR。
复杂度最低报告实际 operation counts、buffer/peak memory、fan-out、latency/throughput、wall time；若声称
hardware contribution，必须补 word length、critical path、area/power 或可审计 synthesis proxy。

## 5. P1 action delta 与贡献层级

- **已碰撞的宽动作**：share/reuse m-th power 或 correlation between FE/FOE and PR/CPE。JLT 2018
  L73–75 已明确记载 2016 m-power 版本；因此不能把“减少一次升幂”本身当独立贡献。
- **可精确定义但未形成合法 Q 的窄动作**：在当前 QAM 串行 NDA 链中，把一次 `raised=x^M0` 的生命周期
  延长到 CFO correction 后，通过 `raised*exp(-j*M0*omega*k)` 生成 CPE 输入，并同时保持原信号域
  `exp(-j*(omega*k+phi))` 的 matched output。现有九篇没有给出这一精确公式链的直接证据，但“当前池
  未见”不是新颖性证明；OFC 2016 一手全文未读，exact collision 仍未关闭。
- **贡献层级**：bounded closure 后降为 `SUPPORTING_ONLY`。冻结预算内 recent task-matched baseline=0；
  不得以 `THESIS_ENGINEERING_COMPONENT`、独立方法、novelty claim 或 Ch5 主贡献继续推进。

## 6. Q# canonical 四判据

### Q-P1-01（未通过）

> M：当前串行 NDA FOE→CFO compensation→CPE 实现；
> C：资源受限、要求与现 receiver matched output/BER 等价；
> A：FOE/CPE 间重复生成 M0 raised-domain representation，未显式管理该中间量的跨级生命周期。

| canonical 判据 | 结果 | 证据/原因 |
|---|---|---|
| 1. M/C/A 具体 | PASS | 冻结对象可具体表达；但 A 目前来自本地实现诊断，不是精读论文指出的 recent-baseline 缺陷 |
| 2. 可产出可复用方法 | PASS | 可产出 shared raised-domain graph、接口与 matched-output protocol |
| 3. recent baseline | **FAIL** | 6/6 bounded query + OpenAlex 引用链 + 全局索引严格复筛为 0 篇 task-matched baseline；不要求作者显式命名 failure A，但三篇有效 recent 全文均是 estimator-changing 或 CPE-only，不能从数据流建立同任务重复 raised-domain 动作 |
| 4. 可量化对标 | PASS | output error、BER/SNR、op/memory/latency/throughput、hardware PPA 均可量化 |

四判据必须全过；故当前没有合法 Q#。失败主因是 **existing-action collision + recent task-matched
baseline 缺位**；OFC 2016 一手 exact boundary 因全文不可得保持未决，但不能覆盖 recent-baseline
硬停止。terminal=`RECENT_BASELINE_UNAVAILABLE`，P1=`SUPPORTING_ONLY`；本轮不做 Step 4a Go/Kill。

## 7. 实验完备性对标汇总（5 篇核心竞品）

选取与 P1 的工程动作或硬件验证最接近、且逐篇实验完备性记录完整的 5 篇：L01 CSNDSP 2014、
L02 JLT 2018、L04 JLT 2019、L06 ISCAS 2022、L07 LCOMM 2026。逐篇事实与评分证据均来自对应
`papers/_read_notes/` 的“实验完备性”表；本节不引入 web 或未记录数字。

为满足 `gw-read.md` L162–165 的跨论文均值要求，采用可复算的 0–3 分量表：统计规范性按
“明确重复次数/seed、明确 error bar/CI、统计检验”各 1 分；baseline 合规性按“来源明确、task/platform
可比、明确公平条件/调参”各 1 分；消融按“参数扫描、组件 on/off 或分级替换、逐模块独立归因”各 1 分。

| 论文 | claim scope | 统计（/3） | baseline 数与合规（/3） | 消融（/3） | 信道/场景 | 复杂度 | V/V'/U |
|---|---|---:|---:|---:|---|---|---|
| L01 CSNDSP 2014 | bounded：square QAM≤256；cross-QAM 明确受限 | 1（1000 runs；无 seed/error-bar 类型/检验） | 3 类，2（来源/任务可比；无公平调参声明） | 2（`l` sweep、standalone/combined；无 shared-block 逐模块消融） | AWGN+laser random walk；单仿真链路 | 仅定性，无资源/延迟数 | 2/1/2 |
| L02 JLT 2018 | bounded：1.25 Gb/s DPSK、P=1、25 km SMF | 1（每个 N 100 次估计；无 seed/error bar/检验） | 2 类，3（同 FPGA、同 N、task-matched） | 2（N sweep、FE on/off、架构/链路条件扫描；无逐算术节点消融） | 真实 25 km SMF；单/双用户邻道、多 linewidth/detuning | adders −23%、multipliers −25%、delay −25%；8-bit Virtex-6 | 3/3/2 |
| L04 JLT 2019 | bounded：单偏振 1.25 Gb/s DPSK、Virtex-6、25 km SMF | 0（无 seed/error bar/检验/运行次数） | 2 类，3（同平台 DMP/conventional comparator） | 2（架构梯度、FE/FC on/off；无正式逐模块删除） | 真实 25 km SMF；双用户与多 linewidth/detuning/dither | add/mul/LUT/cycle/core power | 3/3/1 |
| L06 ISCAS 2022 | bounded：QPSK、指定 FPGA/bit width | 0（仅给输入长度；无重复次数/seed/error bar/检验） | 3 类，2（有来源；跨器件/调制/并行度不完全公平） | 1（量化/并行度/device sweep；无组件消融） | AWGN+phase noise 仿真及 10-GBd 实序列；忽略 FO/PMD | latency、复杂度阶、LUT/DFF、频率、Gb/s/GBd | 3/2/1 |
| L07 LCOMM 2026 | bounded：64-QAM、32 GBd、32-way、28 nm/8-bit | 0（无 seed/error bar/检验/运行次数） | 3 类，3（同工艺/linewidth/clock，明确公平条件） | 3（baseline→MLE-only→PPS+MLE，并扫 P1/P2） | AWGN+Wiener phase noise；单 64-QAM 配置 | logic depth、21 cycles、core/full area/power、效率 | 3/2/1 |

**均值与比例（n=5，可复算）**：统计规范性均值 `(1+1+0+0+0)/5=0.4/3`；baseline 合规性均值
`(2+3+3+2+3)/5=2.6/3`，逐篇 baseline 数均值 `(3+2+2+3+3)/5=2.6`；消融均值
`(2+2+2+1+3)/5=2.0/3`。VVUQ 均值分别为 `V=2.8/3`、`V'=2.2/3`、`U=1.4/3`。
5/5（100%）使用 bounded scope；0/5 报告 seed，0/5 报告明确定义的 error bar/CI，0/5 做统计检验，
2/5（40%）报告重复次数；5/5 有 baseline 来源，3/5（60%）具同平台/同条件强公平性；3/5（60%）
含组件 on/off 或分级替换，但仅 1/5（20%）达到可逐组件归因；4/5（80%）报告定量复杂度，其中
3/5（60%）给出硬件 latency/resource/power/throughput 至少两类；2/5（40%）包含真实光纤链路，另
1/5（20%）含真实序列但主要 BER 仍为隔离仿真。

**领域惯例与盲点**：惯例是 bounded claim、传统 comparator 和复杂度/硬件指标较强；盲点是统计不确定性
报告系统性薄弱（seed、明确定义的 error bar/CI、统计检验均为 0/5），且多数“消融”实为参数扫描或
架构梯度。Contract 阶段不得照抄该盲点：至少应预注册 seeds/CI，并把 shared-lifetime 动作做独立组件
消融；baseline 公平性最低对齐 JLT 2018/JLT 2019/LCOMM 2026 的同平台或同条件比较。

## 8. 综合结论与局限

- 传统 joint FOE/CPE 并不等于共享数据流；CSNDSP 2014 是前者而非后者。
- 真正的数据流前例至少到 OFC 2016/JLT 2018，P1 的 generic action 已 collision。
- 现代低复杂度赛道已经要求从 op-count 走到 fixed-point/FPGA/ASIC 的 latency/throughput/PPA；只报
  Python wall time 或少一次幂运算不足以支撑 hardware contribution。
- 当前证据不能证明窄 raised-domain CFO-removal/lifetime 公式已被 OFC 2016 直接实现，也不能证明它
  未被实现；exact action 保持 `UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`。
- frozen 6/6 query 内没有 2019+ 合格 task-matched baseline；三篇 recent 有效全文中，JLT 2019 的
  correlation 重复已被 conventional refactor 吸收且提出方法改估计器，ISCAS 2022/LCOMM 2026 均为
  CPE-only。因此 Q-P1-01 判据 3 仍 FAIL，terminal=`RECENT_BASELINE_UNAVAILABLE`。
- **P1 的 generic action 已碰撞，窄 delta 未形成合法 Q；停止该方向，下一轮轮换新候选，不再改名重开。**

## 9. Bounded evidence closure（R002）

完整 query/source/count、OFC/PTL acquire 止损、三篇 recent 数据流行号证据与四判据重判见
`.sessions/2026-08-05-shared-m0-foe-cpe-groundwork/R002-bounded-evidence-closure.md`。本节结论仅关闭
Step 3 canonical Q 空集，不构成 Step 3.5/4a、Go/Kill、METHOD_SIGNAL 或论文 claim。
