# Ch4 APSK front-end — GW Step 3 精读综合

> 日期：2026-08-30
> 任务：T048 / GROUNDWORK_READ / CP004
> 范围：仅精读 brief 指定的 7 篇已有全文；未检索、未下载、未进入 Step 3.5/4a。

## 1. Step 3 进度与身份核验

| paper_id | 年份 | 正文标题 | title 自检 | 精读状态 | 主用途 |
|---|---:|---|---|---|---|
| 10.1109_tcom.1980.1094608 | 1980 | Self-Recovering Equalization and Carrier Tracking in Two-Dimensional Data Communication Systems | PASS / overlap=1.0 | 完整 | CMA canonical |
| 10.1109_jsac.2002.1007381 | 2002 | The multimodulus blind equalization and its generalized algorithms | PASS / overlap=1.0 | 完整 | MMA canonical |
| 10.1109_icassp.1990.115806 | 1990 | Blind Equalization Based on Radius Directed Adaptation | PASS / overlap=1.0 | 完整 | RDE canonical |
| 10.1109_jlt.2009.2021961 | 2009 | Blind Equalization and Carrier Phase Recovery in a 16-QAM Optical Coherent System | PASS / overlap=1.0 | 完整 | coherent CMA/RDE/DD comparator |
| 10.1186_1687-1499-2012-317 | 2012 | On the use of APSK modulation over fading channels | PASS / overlap=1.0 | 完整 | direct APSK DFE/LMS |
| 10.1587_elex.8.1642 | 2011 | Fundamentals of coherent optical fiber communications | PASS / overlap=1.0 | 完整 | Jones/DSP/PDL boundary |
| 10.1109_jlt.2009.2035526 | 2010 | Optimal Polarization Demultiplexing for Coherent Optical Communications | PASS / overlap=1.0 | 完整 | unitary/ML boundary与强 recipe 邻居 |

计数：7/7 全文精读，7/7 独立 read note；其中 5 篇完成实验完备性提取，2 篇完成写作架构提取。

## 2. 方法谱系与 claim ceiling

| 方法族 | receiver-visible 输入 | 动作/输出 | 已覆盖的原子 | 未覆盖的组合 |
|---|---|---|---|---|
| CMA / Godard | 接收样本与输出模长 | 常模梯度更新 FIR | 盲、相位不敏感均衡 | pilot 初值、环身份、逐样本可靠度门 |
| MMA / Yang et al. | 实部/虚部输出 | 多模实虚分量梯度 | 方形 QAM 的相位定向盲均衡 | APSK 环结构、pilot、可靠度门 |
| RDE / Ready–Gooch | 输出模长与最近半径 | 最近环误差更新 | ring-aware 盲均衡 | pilot 初值；均衡更新的 reliability gate |
| coherent CMA/RDE/DD | 双偏振复采样、模长/判决 | 2×2 butterfly 更新 | coherent blind→DD/RDE 链与复杂度对比 | APSK、短 pilot、公平同预算可靠度门 |
| APSK DFE/LMS | APSK 接收样本与历史判决 | 15+7 tap DFE | APSK 上的传统 LMS/DFE | DP Jones、ring-aware 误差、payload gate；且假定完美同步 |
| coherent Jones review | 双偏振复采样 | GVD FIR + 2×2 butterfly + CPE | 训练 DD、CMA、Jones/PDL 分层边界 | scaled-polar LS 与 APSK recipe |
| unitary constrained demux | 短训练、双偏振样本、CMA 模长 | LS 初始化 + 2-angle unitary CMA | pilot 初始化、单位酉约束、盲跟踪、排列消歧 | unconstrained LS 后 scaled-polar 投影；APSK/FSO/pilot-budget 对标 |

结论边界：CMA、MMA、RDE、pilot initialization、unitary/Procrustes 约束都只能作为已知原子。本文后续若继续，只能声称目标场景中“特定完整 recipe 的有界迁移/组合与可验证增益”，不得声称首次发明这些原子、SOTA、全局最优或全面优于更一般接收机。

## 3. 逐篇可复用结论

### L1 — Godard 1980 / CMA

- **对象与方法**：二维调制的相位不敏感自恢复均衡；$p=2$ 代价为 $E[(|z|^2-R_2)^2]$。
- **baseline/结果**：与 DD/MSE 参照和 $p=1$ 互比；严重信道约 10 s 打开眼图，$p=2$ 较快。
- **假设/局限**：非凸吸引域依赖参考抽头初始化；常模与多环 APSK 失配。
- **对 Ch4 的含义**：C4-2 必须包含正确 tuned CMA，但不能以“相位不敏感盲更新”为创新。
- **read note**：`papers/_read_notes/10.1109_tcom.1980.1094608.md`

### L2 — Yang et al. 2002 / MMA

- **对象与方法**：按实部/虚部多模代价恢复方形 QAM/CAP 的相位定向；含 GMMA/CMA-MMA 变体。
- **baseline/结果**：51.84-Mb/s 16-CAP、20–700 ft UTP 与 bridged tap；相较 CMA 降低 rotator 需求和错误旋转风险。
- **假设/局限**：依赖方形/分量模结构；仍可能 diagonal/45°/offset wrong solution。
- **对 Ch4 的含义**：MMA 是强经典方形-QAM原子，不等同于 APSK ring-aware gate。
- **read note**：`papers/_read_notes/10.1109_jsac.2002.1007381.md`

### L3 — Ready & Gooch 1990 / RDE

- **对象与方法**：将输出分配到最近星座半径，以半径误差更新均衡器。
- **baseline/结果**：V.29/CCITT M.1020、26 dB SNR、10-Hz offset；RDE 约 8 s 分环，CMA 约 9–10 s。
- **假设/局限**：错误初始增益/all-pass 可能失败；论文的可信区域门用于载波环，而非均衡抽头更新。
- **对 Ch4 的含义**：C4-2 的最强直接算法 baseline；必须使用同 LS 初值 tuned RDE。
- **read note**：`papers/_read_notes/10.1109_icassp.1990.115806.md`

### L4 — Fatadin et al. 2009 / coherent comparator

- **对象与方法**：14-Gbaud 16-QAM coherent CMA、RLS-CMA、RDE、DD 与 PDM butterfly。
- **baseline/结果**：RDE/DD 接近 RLS-CMA并优于 CMA；RLS $O(N^2)$，其余约 $O(N)$。
- **假设/局限**：无 pilot 初值、无逐样本可靠度门；方形 16-QAM，不是 APSK。
- **对 Ch4 的含义**：不可只打弱 CMA；需把 tuned DD-LMS/RLS 与 RDE 纳入公平矩阵。
- **read note**：`papers/_read_notes/10.1109_jlt.2009.2021961.md`

### L5 — Baldi et al. 2012 / direct APSK DFE

- **对象与方法**：4+12 16-APSK、半径比 2.7，经 Rice/Rayleigh 多径与 15+7 tap LMS-DFE。
- **baseline/结果**：对比 16-QAM、PDP、编码和 HPA；迟到路径超出窗口时出现 error floor。
- **假设/局限**：SISO；假定 perfect carrier synchronization；DFE 有错误传播。
- **对 Ch4 的含义**：“APSK + LMS/DFE”已知，但没有 pilot-initialized ring-aware gated refinement。
- **read note**：`papers/_read_notes/10.1186_1687-1499-2012-317.md`

### L6 — Kikuchi 2011 / coherent boundary

- **对象与方法**：数字相干 DSP 分层；训练 DD-LMS 与盲 CMA；Jones/PMD/PDL 分解。
- **baseline/结果**：PDM-QPSK 例中 $2^7$ training symbols，5 taps 去除采样相位依赖。
- **假设/局限**：PDL 是非酉 Hermitian 分量；CMA 在多级 QAM/PDL 下有奇异风险。
- **对 Ch4 的含义**：近酉性必须先测；PDL/不等奇异值不能被 scaled-unitary 假设吞掉。
- **read note**：`papers/_read_notes/10.1587_elex.8.1642.md`

### L7 — Roudas et al. 2010 / constrained unitary demux

- **对象与方法**：短训练 LS 初始化后，以两个实角的 unitary lattice 做 CMA blind tracking。
- **baseline/结果**：约束 CMA <20 symbols 收敛，unconstrained CMA >60；实验约 3× 加速，稳态 BER 无明显罚损。
- **假设/局限**：无 PMD、单位酉、等支路噪声；非酉/不等噪声时应考虑预白化联合 ML/MMSE。
- **对 Ch4 的含义**：C4-1 强 recipe 邻居；直接低维受约束估计不等于 unconstrained pilot-LS 后 scaled-polar projection，但使 claim 只能收窄为 DP-APSK FSO 的短 pilot 有界迁移。
- **read note**：`papers/_read_notes/10.1109_jlt.2009.2035526.md`

## 4. Q-C4-2：ring-aware pilot-initialized semi-blind refinement

### 4.1 M–C–A 与四判据

| M | C | A | 判据 1：M/C/A | 判据 2：方法产出 | 判据 3：baseline | 判据 4：量化对标 |
|---|---|---|---|---|---|---|
| 同 pilot/初值/可靠度/更新预算的 LS-only + tuned DD-LMS/RLS；同 LS 初值 tuned RDE | DP-(8,8)-16APSK、memoryless 2×2 Jones、有限 pilot；payload 仅见 decision distance、ring identity、receiver residual | LS-only 不利用 payload；DD 对低可靠错误敏感；plain RDE 使用 ring identity 但不给更新可靠度门，错环/错判样本会污染递推 | ✅ 具体矛盾 | ✅ 形成 receiver-visible gated refinement 算法与门控准则 | ✅ 按 T048/D031-D032 的经典 baseline 授权口径，M 明确且可正确实现 | ✅ BER/FER、收敛、更新数、pilot overhead、复杂度可同预算对标 |

**严格 glossary 注记**：项目全局参数把“近期”定义为 2019+ 顶刊；本 brief 又禁止检索并只指定 1980–2012 经典全文。因此上表的 4/4 是 T048 明示的 D031/D032 硕士级经典-baseline 口径，不等于已经完成 2019+ exact-collision closure。后者是 Step 3.5 的证据债务，不能在本轮伪装成已完成。

### 4.2 完整 recipe 碰撞检查

| 要素 | CMA | MMA | RDE | coherent blind→DD | APSK DFE | Q-C4-2 |
|---|---:|---:|---:|---:|---:|---:|
| pilot/LS 初始化 | ✗ | ✗ | ✗ | 未形成同预算 LS 合同 | 未明确为本 recipe | ✓ |
| APSK ring identity | ✗ | ✗（方形分量模） | ✓ | RDE 分支可有 | 调制有环但均衡误差不 ring-aware | ✓ |
| decision distance / residual | ✗ | ✗ | 仅半径误差 | DD 有 decision error | LMS/DFE 判决误差 | ✓ |
| 低可靠样本禁止/降权更新 | ✗ | ✗ | ✗；载波环区域门不等于均衡 gate | 未给统一 gate | ✗ | ✓ |
| 同 pilot/更新预算公平合同 | ✗ | ✗ | ✗ | ✗ | ✗ | 必须冻结 |

**verdict：`SURVIVES / NOT_EXACT_COLLISION`。** 7 篇中没有一篇、也没有一条明确 receiver recipe 同时具备上述五项。最强 comparator 是“同 LS 初值 tuned RDE”；第二组是“同 LS 初值 tuned DD-LMS/RLS”。CMA/MMA 仅作 canonical reference，不能承担唯一主 baseline。

**claim ceiling**：只能声称 DP-(8,8)-16APSK、memoryless Jones、有限 pilot 条件下，receiver-visible gate 相对正确经典 baseline 的有界改善；不得声称发明 RDE、semi-blind equalization 或 reliability gating，也不得外推到频率选择性、强 PMD/PDL 或任意调制。

**Step 3.5 blocker**：必须在允许检索后核查 2019+ task-matched 文献是否已有完全相同的 pilot-initialized + ring-aware + reliability-gated IAO recipe，并冻结同初值、同 pilot、同更新数、同调参预算的 comparator 合同。

## 5. Q-C4-1：scaled-unitary pilot-LS

### 5.1 M–C–A 与四判据

| M | C | A | 判据 1：M/C/A | 判据 2：方法产出 | 判据 3：baseline | 判据 4：量化对标 |
|---|---|---|---|---|---|---|
| unconstrained complex 2×2 pilot-LS、ridge/Tikhonov LS、singular-value floor；必须追加 direct constrained/unitary LS | scaled-unitary/near-equal singular values 的 memoryless Jones channel、短 pilot budget、DP-(8,8)-16APSK FSO | unconstrained LS 估计 8 个实自由度，在小样本且真实信道近酉时方差高；已知结构投影可能降方差，但非酉时产生偏差 | ✅ 具体矛盾 | ✅ 形成 scaled-polar estimator 与适用域准则 | ⚠️ 经典 baseline 明确，但 Roudas 是强 recipe 邻居，2019+ closure 未做 | ✅ NMSE、BER/FER、pilot overhead、奇异值比/PDL 可量化 |

**verdict：`SURVIVES_BOUNDED / STRONG_RECIPE_NEIGHBOR`，不是 clean 4/4。** Procrustes/polar projection 是已知数学原子，且 Roudas 已给短训练 LS 初始化 + 直接 unitary parameterization + blind tracking 的完整相邻 recipe。它尚未完全等同于“unconstrained 2×2 pilot-LS 后做 scaled-polar projection”，也未覆盖 DP-APSK FSO 的短 pilot budget，因此不按 T048 的 exact-collision 规则关闭；但独立原创性主张很弱。

### 5.2 near-unitary claim ceiling

- 只有在实测/仿真信道的奇异值比接近 1、PDL 弱且双支路噪声近等方差时，scaled-polar 投影的低方差叙述才成立。
- PDL、非等奇异值、增益不平衡或不等噪声增强时，投影会把真实非酉分量当噪声删除，产生结构偏差；unconstrained/ridge LS、singular-value floor 或联合 ML/MMSE 可能更优。
- 必须报告投影前后奇异值、channel NMSE 与端到端 BER/FER；只报 BER 不足以证明结构机制。
- 公平 baseline 除 brief 指定三项外，应包含 Roudas 型 direct constrained/unitary LS，避免把“先估后投影”与一个不利用结构的弱对手单独比较。

**Step 3.5 blocker**：需要核查 scaled-polar/Procrustes 在短训练 coherent 2×2 channel estimation 中的 exact recipe 先例，并先定义 near-unitary 的可测阈值；在此之前不得声称新颖或普适。

## 6. 实验完备性综合

| 论文 | seeds/运行 | baseline | 场景覆盖 | 主要缺口 |
|---|---|---|---|---|
| Godard 1980 | 5-run average | MSE/DD/$p=1/2$ | 2 信道 × 4 星座 | 无误差条/显著性；步长公平性弱 |
| Ready 1990 | 未报 | CMA | 单 V.29 worst-case M.1020 | 单场景；初始化敏感；无统计 |
| Fatadin 2009 | 未报 | CMA/RLS-CMA/RDE/DD | CD/DGD/OSNR/PDM | 参数调优和同预算合同未报 |
| Baldi 2012 | Monte Carlo 次数未报 | QAM、DFE、编码/HPA | 多 PDP/Rice/Rayleigh | SISO + perfect sync；无统计置信度 |
| Roudas 2010 | 仿真约 500 realizations；实验 100k symbols | constrained/unconstrained CMA | OSNR + 100-km 实验 | 缺 PDL 连续扫描与 post-LS polar comparator |

对后续的约束：任何 Step 4a 最小验证都必须预先冻结 seed 数、paired comparison、error bar/CI、同 pilot/同 update/同 tuning budget；不能复刻经典论文“单曲线 + 未报随机次数”的证据强度。

## 7. 写作架构综合

### Fatadin 2009

先在单偏振隔离算法差异，再扩到 PDM butterfly 与 CD/PMD，最后以复杂度收束。可迁移到 C4-2 的写法是：先单独证明 reliability gate 的信息增量，再进入完整 DP Jones；避免首图同时混入调制、偏振、CPE 与译码。

### Roudas 2010

先写最优性成立条件，再给低维结构和训练初始化，然后用统计收敛与实验闭环，最后明确非酉边界。可迁移到 C4-1 的写法是：先报告近酉诊断，再报告投影增益，结论同步写 projection bias 的失效域。

## 8. Step 3 结论与唯一后继对象

1. **Q-C4-2**：`SURVIVES / NOT_EXACT_COLLISION`；在 T048/D031-D032 经典 baseline 口径下四判据 4/4。完整组合未被 7 篇覆盖。
2. **Q-C4-1**：`SURVIVES_BOUNDED / STRONG_RECIPE_NEIGHBOR`；Roudas 已覆盖短训练 LS + unitary constrained blind tracking，且 polar/Procrustes 为已知原子，故只保留近酉 DP-APSK FSO 的窄迁移主张。
3. **唯一优先进入 Step 3.5 的对象**：`Q-C4-2`。原因是 exact-recipe 差异更清晰、receiver-visible IAO 完整、强 comparator 可直接定义；Q-C4-1 的 recipe 邻居更强且 claim ceiling 更窄。
4. **阻断声明**：本文件没有授权或完成 Step 3.5/4a；没有 2019+ 检索证据、没有实验数字，不能据此宣布方法可行或论文贡献成立。
