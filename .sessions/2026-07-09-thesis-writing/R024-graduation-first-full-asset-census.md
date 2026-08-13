# [R024] 毕业优先标准下的全量历史资产普查

> 2026-08-13 | 关联：2026-07-09-thesis-writing / D031

## 调研问题

按 D031 的有限真实主张标准，全项目已有资产是否显著多于最近反复讨论的 CCISP、P01、P11、select-before-execute、P1-M0、P10 和 FPGA 共享架构？其中多少是已有真实证据的方法/工程方法，多少只是未裁决动作链、支撑组件或真实性无效项？

## 发现

### 1. 扫描覆盖与去重结果

T016–T018 三路只读扫描覆盖：

- `projects/thesis-fso/worker-logs/` 250 份记录；
- `projects/thesis-fso/direction-lab/` 438 个文件、148 个目录；
- `projects/simulation/results/` 30 个结果目录、138 个文件；
- harvest/inventory/portfolio/method-factory、主要 `.sessions/` 决策链及必要 git 历史；
- git 历史中的 3 个 FPGA 专题、46 张 raw card、29 个机制单元和 6 张乘法图卡。

共恢复约 59 个命名 candidate/construct 身份，去重后为约 41 条独立动作血缘。旧 T012 的“26 个独立资产”不是全仓清单；它漏掉了较早的 B/C/Q 系列、method-factory/sandbox 构造、authority/identity 阻断项和 FPGA 设计图谱。

### 2. 第一层：足以进入当前 thesis spine 的四个承重对象

| 对象 | 现有真实证据 | D031 下的最窄方法身份 |
|---|---|---|
| CCISP | 9 dB、三档 downlink GG、30 seeds×400 windows；相对 fixed NDA 的 common-payload 增益约 0.8–1.5 dB | 已就绪独立方法；Ch3 主锚 |
| P01 pilot-SNR adapter | ±3 dB nominal mismatch；5 个 harm cells 损害 0.324–0.704 dB；receiver-visible adapter 恢复 4/5 | 配置失配下的接收侧校准鲁棒扩展；global ref=11 不再自动 Kill |
| P11 complex-LS Butterfly FIR | 可信范围仅实际默认 20 dB；1% pilot LS BER 约 `3.176e-4`，50%-label Adam 约 `3.859e-4`，goodput 约 1.98× | 20 dB 局部少导频线性 Butterfly-FIR 校准方法；CMA 只限制表述。corrected confirmation 未运行，authority stop 不是科学失败 |
| select-before-execute | 396,000 windows 输出 mismatch=0；branch calls −50%；software timing ratio 0.5424；多类操作下降 36.44%–51.28% | 保持输出等价的先选后算单分支软件执行方法；可承 Ch5 工程章，不外推 FPGA/PPA |

主线程综合判断：按 D031，目标已从“是否存在第二方法”转为“P01 与 P11 谁承担第二个独立方法、select-before-execute 如何承担工程章”。不再需要先搜索新候选才能形成 thesis spine。

### 3. 第二层：已有真实数字、可并入章节的五类资产

| 对象 | 可用事实 | 身份上限 |
|---|---|---|
| P02 global ref=11 | weak/low-SNR slice 相对 pilot adapter +0.4539 dB | 传统全局调参规则/P01 comparator，不单独承主方法 |
| P03 Q(8,6) | gain-bearing 区 regret 约 +0.027 dB；最佳 mixed edge 仅 0.0166 dB | 有限字长实现与动态范围边界，可并入 Ch5；无 PPA |
| P08-R2 prefix-LS coded chain | 单局部 slice B0/B2/O2 FER 0.155/0.148/0.139；hidden-SNR metamorphic Δ=0 | receiver-visible coded calibration/可信接收链；chronology 不闭合，作探索性工程材料 |
| P05 corrected online CMA | fixed-label BER 可由约 0.499 恢复至约 `1e-3` 以下 | 经典在线均衡迁移/强 baseline 与边界；不是新算法，但可支持场景应用叙事 |
| P06 last-value persistence | persistence R²=0.85，明显高于复杂 causal-history R²=0.32 | 简单跨帧预测规则/对照；缺下游 method delta，不单独承重 |

### 4. 第三层：真实动作链存在，但当前没有承重结果

至少包括 P1-M0、P10、Pilot-Jones EMA09、B1 adaptive phase window、B10 adaptive pilot-RLS、B12 fade-reliability MAP、B9 DRE 配置、Q14 causal residual、C15-open、C16-open、RML-FSTS、AMC Q-B、K01 fade-guarded DPLL、supervised degradation detector 等。

这些对象的旧终态多为 authority、identity、source/readiness、testbed 或执行前阻断，不能再写成科学失败；但也不能因 D031 放宽就称为已有方法结果。它们证明仓库有大量动作设计库存，不证明当前需要恢复执行。

### 5. 第四层：FPGA/硬件库存大，但仍是设计图谱

FPGA 历史中有 FE11-BJ3M、X02 banked window store、FE12 CMA Butterfly graph、CF13 deinterleaver–LDPC bank fusion、CF02 streaming FFT refinement 等卡片。仓库未发现 RTL/HLS 工程、综合/P&R 报告、bitstream 或板测日志，因此：

- FE11-BJ3M 是唯一 provisional survivor，但仍只是 4M→3M/系数驻留/折叠设计卡；
- 软件调用量、Python operation count 和 timing 不能转换为 LUT/DSP/BRAM/功耗/吞吐声称；
- FPGA 路线目前可作 Ch5 的架构与未来实现储备，不能当现成硬件方法。

### 6. 第五层：真实性无效或精确科学门已否定

不可因包装标准放宽而复活的包括：P07 旧 +0.91 dB、P09 8× BPS、G1/Q15 winner、AMC Q-A′ 现有 positive claim、P04/P05-ML/P06-complex-history 的精确增量、C3 segmented CPE、oversampled Q1、coded-feedback C1、DSP-outage Q001，以及 C04/C09/C11/C12/C14/C15-ring/C16-HOS/hybrid-router/factory sprint 精确负面构造。

特别保持：P11 corrected confirmation 从未运行；两个重复对话均在实验前 authority gate 停止，corrected rows=0，CMA absorption=`UNRESOLVED`。

### 7. 旧流程漏失机制

41 条血缘中，主要漏失来源为：

- 约 11 条 authority/identity/source/readiness 阻断被误读成科学失败；
- 约 8 条被强邻居、cheap alternative 或 full-general 方法提前关闭；
- 约 7 条被期刊级 novelty、broad claim 或全域竞争闭包压掉；
- 约 6 条因复合包总 terminal 连带抹掉可分离动作；
- 约 9 条 sandbox/diagnostic 动作没有进入 thesis inventory；
- 15 条以上确有 artifact、problem-absent 或精确 scientific FAIL。

这些类别可重叠，不应相加为总数。

## 结论

用户的判断成立：仓库远不止最近列出的少数资产。准确说法不是“已有 41 个完成方法”，而是“已有 41 条独立动作血缘，其中 4 个对象足以支撑当前两方法加工程章的 thesis 结构，5 类有真实数字可并入章节，十余条是未裁决动作库存，15 条以上明确无效”。

在 D031 下，当前没有继续盲找方法的战略必要性。最低风险结构已有现实库存：CCISP 承 Ch3；P01 或 P11 承第二个独立方法；select-before-execute 联合 P03 等承 Ch5 工程方法。最终选 P01 还是 P11仍需后续战略讨论，但不应在本轮恢复实验或 Groundwork。

## 对决策的影响

支持 D031 保持 active，并否定“P11/P01 是仅有的两个勉强候选、必须继续外找”的库存判断。后续应先讨论第二方法的独立性与包装风险，再决定是否需要任何 bounded confirmation；全量普查本身不授权执行。
