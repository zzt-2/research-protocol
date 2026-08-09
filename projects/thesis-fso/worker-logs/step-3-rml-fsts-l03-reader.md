# L03 全文精读：Morelli et al. (2009)

> Groundwork Step 3 | 论文角色：C3 multi-correlation / multi-lag prior-art ceiling
> 派遣标题：A Practical Scheme for Frequency Offset Estimation in MIMO-OFDM Systems
> 结论边界：仅做全文事实提取；不进入 Step 3.5/4a，不设计 RML-FSTS，不给 Go/Kill。

## 0. Title / DOI / path preflight

| 检查项 | 结果 | 证据 |
|---|---|---|
| 派遣标题 | MATCH | `papers/doi/10.1155_2009_821819/content.md:3`；`metadata.json:4,13-15` |
| DOI | MATCH：`10.1155/2009/821819` | `content.md:1`；`metadata.json:5` |
| canonical 正文 | 可读，381 行；首页、正文、参考文献完整 | `papers/doi/10.1155_2009_821819/content.md:1-381` |
| 公式补核 | Markdown 将大量公式渲染为 omitted picture；已仅用同目录 `source.pdf` 核对公式 (14)–(42) | `content.md:47-53,123,129,143-165,181-231`；`source.pdf` pp.4–6 |
| 预检结论 | PASS；不是标题错配或损坏全文 | 上述证据 |

## 1. DOI / 来源

- DOI：`10.1155/2009/821819`。
- 作者：Michele Morelli、Marco Moretti、Giuseppe Imbarlina。
- 来源：Hindawi Publishing Corporation，EURASIP Journal on Wireless Communications and Networking，Volume 2009，Article ID 821819，9 pages。
- 证据：`content.md:1,3-5`。

## 2. Canonical 源路径

- 正文：`papers/doi/10.1155_2009_821819/content.md`。
- 元数据：`papers/doi/10.1155_2009_821819/metadata.json`。
- 仅用于公式辨认的同目录 PDF：`papers/doi/10.1155_2009_821819/source.pdf`。
- metadata 标注 `download_status=success`、`download_method=unpaywall`、`content_type=pdf`、`content_quality=good`、`title_check=match`（`metadata.json:7-15`）。

## 3. 发表状态

- **正式发表的 Research Article**，不是预印本。收到 2008-06-27，修回 2008-10-03，接收 2008-12-25；版权年份 2009。
- 证据：`content.md:3,11,17`。

## 4. 发表渠道

- **EURASIP Journal on Wireless Communications and Networking**，Hindawi，Volume 2009，Article ID 821819。
- 证据：`content.md:1`。

## 5. 年份 / 期刊

- 年份：**2009**。
- 期刊：**EURASIP Journal on Wireless Communications and Networking**。
- 该年份意味着它只能充当历史 prior art，**不能独立满足本项目 2019+ 近期 baseline 门**。
- 证据：`content.md:1,17`；“不能满足近期门”是 target-domain 规则应用，不是原文声称。

## 6. 核心贡献

1. 论文把 training-assisted MIMO-OFDM 的归一化 CFO 分解为 fractional CFO 与 integer CFO，并设计频域复用、时域重复的 FDM pilot，使 fractional CFO 可由重复 preamble 的跨段相关相位低复杂度估计，integer CFO 再以 ML 联合信道估计恢复（`content.md:15,35,107-139,167-191`；`source.pdf` p.4, (14)–(25)，p.5, (26)–(35)）。
2. 其 fractional CFO refinement 不是只用单一相关间隔：集中似然累计所有接收支路和 `r=1,...,R-1` 的多 lag 相关，并在线性化残差相位后形成闭式、相关幅度加权的 multi-lag 修正（`content.md:141-165`；`source.pdf` p.4, (18)–(24)）。
3. 论文同时给出 MSE/CRB、估计范围与运算量分析，并在相同 pilot 数量下对比 RCFE、CBFE、PBFE；报告 RCFE 在准确度、范围或复杂度组合上更优（`content.md:201-259,241-247,281-317`；`source.pdf` pp.5–6, (36)–(40), Table 1）。

## 7. 方法概述

发射端在每根 TX 上使用等功率、等间隔且 TX 间 FDM 的 pilots，并令每个时域 preamble 由 `R` 个相同 segment 构成；收到的第 `m` 根 RX preamble 因此可拆成 `R` 段，段间只有 CFO 诱导的规则相位旋转和噪声（`content.md:107-139`；`source.pdf` p.4, (14)–(17)）。FCFO 先由 lag-`P` 相关的合并相位得到 coarse estimate，再用全部 `rP` lag 的相位残差按相关幅度与 lag 加权得到 closed-form refinement；之后先反旋 FCFO，再在离散 ICFO 假设上最大化联合 ML metric，最终 `ν_hat=R(ε_hat+η_hat)`（`content.md:141-191`；`source.pdf` pp.4–5, (18)–(35)）。

## 8. 实验设置

- 系统：MIMO-OFDM，`N=1024` subcarriers，5 GHz carrier band，5 MHz bandwidth，subcarrier spacing ≈4.9 kHz，`Ts=0.2 μs`，OFDM useful duration 0.205 ms（`content.md:261-269`）。
- 信道：每个 TX/RX pair 有 `L=12` 个独立 Rayleigh taps；exponential PDP `E|h_m,i(ℓ)|²=σ_h² exp(-4ℓ/L)`，归一化总功率为 1；每个 simulation run 生成新 channel snapshot，并在 training period 内固定；不同 antenna pairs 独立（`content.md:265-279`；`source.pdf` p.6, (41)）。
- RCFE training：`R=8`、`Q=4`、`M=QR=32`；每 TX 32 个 QPSK pilot，`|d_i(n')|²=32/N_T`；`N_T,N_R` 随实验改变（`content.md:279`）。
- Fig.1：`N_T=3,N_R=2`；RCFE/CBFE 同一 training，PBFE 取 `Q=32,{μ_i}={0,1,5}`、Chu pilots；所有方法每 TX 均为 32 pilots；CFO 每 run 从 `[-0.4,0.4)` 均匀抽取；为只评 FCFO，RCFE/PBFE 均假定 perfect ICFO；SNR 图示 0–18 dB、3 dB 间隔（`content.md:277,281-301`）。
- Fig.2：`N_R=2`，`N_T=2,3,4`；Fig.3：`N_T=3`，`N_R=2,3,4`（`content.md:299-315`）。
- Fig.4：RCFE/PBFE 比 ICFO failure probability；RCFE 搜 `η∈{-2,-1,0,1,2}`，PBFE 搜 `η∈{-16,...,15}`；对应 range 分别 `|ν|≤20` 与 `|ν|≤16`；图示 SNR −18 至 −6 dB（`content.md:317-331`）。
- 未报告 Monte Carlo run 数、随机 seed、error bar、置信区间或显著性检验。

## 9. Baseline 逐项审计

| Baseline / bound | 类型 | 本文处理方式 | 自实现 / 引用 / 无 | 公平性证据与限制 |
|---|---|---|---|---|
| Exact MLFE | 理论全局 ML estimator / 高复杂度参照 | 第 3 节推导；仿真图未作为主要曲线 | 本文推导；没有代码 | 说明需 CFO uncertainty range line search，作为复杂度动机；没有给实验 runtime（`content.md:65-103,107`） |
| CBFE [12] | 两步 correlation-based CFO estimator | 仿真实现并与 RCFE 对比 | **引用算法、本文复现**；无开源代码 | 与 RCFE 使用相同 training sequences；每 TX 32 pilots。无 ICFO estimation，range 受限（`content.md:235-259,281,301`） |
| PBFE [17] | polynomial/MUSIC-root based MIMO-OFDM estimator | 仿真实现并与 RCFE 对比 | **引用算法、本文复现**；无开源代码 | 同为每 TX 32 pilots，但采用其原设计 `Q=32`、Chu sequence；复杂度和 range 对 Q 敏感，作者明确承认可降 Q 换复杂度但损失 range（`content.md:281-301,317-331`） |
| EMCB [20] | 随机 nuisance channel 下的 average CRB | 作为 MSE 理论 benchmark | 引用 bound，本文对 channel statistics 数值平均 | 不是可执行 estimator（`content.md:287-301`） |

## 10. 关键结论

- RCFE 的 FCFO MSE 在所测 SNR 上接近 EMCB，并优于 PBFE/CBFE；CBFE 相对 RCFE 约损失 1.25 dB，与理论式 (38)/(40) 一致（`content.md:287-301`；`source.pdf` pp.5–6, (38)–(40)）。
- Fig.1 场景的 FCFO 运算量：RCFE 57,500，PBFE 1,156,000，CBFE 24,000 real operations；因此 CBFE 更省算，但 RCFE 提供更高准确度（`content.md:301`）。
- RCFE MSE 基本不随 TX 数改变；增加 RX 数通过延长 CFO observation record 改善估计，作者给出 `10 log10(N_R)` dB array gain（`content.md:303-315`）。
- ICFO 实验中，当 SNR > −10 dB 时 RCFE 优于 PBFE；总 CFO 运算量为 RCFE 252,500、PBFE 1,283,000，处理量降幅大于 5×（`content.md:317-331`）。
- RCFE 约束：`L≤N/M=N/(QR)`，比 MLFE 的 `L≤N/Q` 严格 `R` 倍；这是一项明确的 channel-length / repetition trade-off（`content.md:195-201`）。

## 11. 与 RML-FSTS 的关系

### Source-domain FACT

- 本文已经公开一种**多相关 / 多 lag 融合**：`q(ε_tilde)` 对所有 RX branch 及 `r=1,...,R-1` 的 `R_m(r)` 累计；residual estimator 的分子含 `r |R_m^(c)(r)| φ_m^(c)(r)`，分母含 `r² |R_m^(c)(r)|`（`source.pdf` p.4, (18)–(23)；对应正文 `content.md:141-165`）。
- 权重来自样本相关幅度与 lag 几何，不是学习器，不是基于星地状态条件显式选择某个 lag。

### Target-domain INFERENCE（有迁移启示，但非证明）

- 它构成 C3 prior-art ceiling：若未来 RML-FSTS 仅声称“把多个 lag 的 correlation phase 加权融合”，可能与式 (18)/(23) 的已知形态过近；未来方法必须在 observable condition、任务目标或 fusion/selection mechanism 上给出可验证差异。
- 可迁移的原料只有：多 lag 相关量、幅度作为 reliability proxy、lag 在相位斜率估计中的几何权重，以及复杂度—捕获范围—channel support 的显式 trade-off。

### Target-domain UNKNOWN（本文不能回答）

- 星地 coherent-FSO 中是否存在 **lag-ranking crossover**：UNKNOWN。
- dev-frozen modulation / TS / received-power-conditioned single-lag lookup 是否会失败：UNKNOWN。
- condition-aware 多 lag 机制能否胜过 conditioned single-lag cheap comparator：UNKNOWN。
- 本文不能证明 target defect、近期 baseline、novelty 或 Go；场景是 5 GHz multipath Rayleigh MIMO-OFDM，不是 coherent-FSO。

## 12. 实现关键细节

1. Pilot placement：令 `Q≥N_T` 为 2 的幂、`R` 为 2 的幂、`M=QR`；第 `i` 个 TX 的非零 pilot 在 `n=n'M+(i-1)R`，pilot modulus 取 `sqrt(M/N_T)`，总 training energy `E_T=N`（`content.md:55-59,107-125`；`source.pdf` p.4, (14)）。
2. CFO decomposition：`ν=R(ε+η)`，`ε∈(-1/2,1/2]`、`η` 为 integer；时域 repeat period `P=N/R`（`content.md:127-139`；`source.pdf` p.4, (15)–(17)）。
3. Lag correlations：`R_m(r)=Σ_{k=rP}^{N-1} x_m^*(k)x_m(k-rP)`；无噪声时 `R_m(r)=(R-r)||u_m||² exp(j2πεr)`（`source.pdf` p.4, (19),(21)；`content.md:145-155`）。
4. Coarse FCFO：`ε_hat^(c)=(1/2π)arg{Σ_m R_m(1)}`（`source.pdf` p.4, (20)）。
5. Multi-lag refinement：counter-rotate `R_m^(c)(r)=R_m(r)exp[-j2π ε_hat^(c)r]`，定义其相位 `φ_m^(c)(r)`；小残差线性化后，`Δε_hat=(1/2π)[Σ_mΣ_r r|R_m^(c)(r)|φ_m^(c)(r)]/[Σ_mΣ_r r²|R_m^(c)(r)|]`，最终 `ε_hat=ε_hat^(c)+Δε_hat`（`source.pdf` p.4, (22)–(24)；`content.md:155-165`）。
6. ICFO：以 `Γ^H(ε_hat R)` counter-rotate，每个候选 integer `η_tilde` 上计算集中 likelihood `ψ(η_tilde)` 并取最大，再用 `ν_hat=R(ε_hat+η_hat)`（`source.pdf` pp.4–5, (25)–(35)；`content.md:167-191`）。
7. 理论 MSE（perfect ICFO）：`E[(ν_hat-ν)²]=3(σ_n²/σ_s²)/[2π² N_R N(1-1/R²)]`（`source.pdf` p.5, (36)–(38)；`content.md:201-219`）。
8. 复杂度：FCFO RCFE 为 `2N_R(R-1)(2N+3)`；ICFO RCFE 为 `N_R N[5log2N+8LN_TN_η/M]`；详见 Table 1（`content.md:223-247`；`source.pdf` pp.5–6, Table 1）。
9. 限制：Markdown 公式图缺失，以上公式以同目录 canonical PDF 核对；本文没有公开源码，因此不能核验索引边界、数值稳定性或实际实现细节。

## 13. 适配 / 不适配 / 未来原料启示

| 分类 | 结论 | 依据 |
|---|---|---|
| 适配 | 适合作为 multi-correlation / multi-lag CFO estimator 的历史 prior art ceiling | 式 (18) 汇总多 RX、多 lag likelihood；式 (23) 给幅度与 lag 加权的闭式 refinement |
| 适配 | 适合作为“不能只写 weighted multi-lag fusion 就声称新方法”的 collision 警示 | 2009 年已有明确数学形态与复杂度/MSE分析 |
| 不适配 | 不是 coherent-FSO 直接竞品 | 5 GHz MIMO-OFDM、multipath Rayleigh、repetitive FDM preamble；无光学链路、湍流、AO、激光相位噪声 |
| 不适配 | 不能证明 conditioned-single-lag failure 或 lag-ranking crossover | 没有 modulation/TS/received-power 条件化 lag ranking 实验；所有 lag 由固定公式融合 |
| 不适配 | 不能满足 2019+ baseline 门 | 正式发表年份为 2009 |
| 未来原料 | 可复用 observation primitive：`R_m(r)`、相关幅度 reliability proxy、lag slope geometry | 式 (19),(21),(23) |
| 未来原料 | 可复用审计维度：MSE、failure probability、acquisition range、real operations、channel-length constraint | 式 (38)/(40)、Fig.4、Table 1、`L≤N/(QR)` |

## 14. 开源代码

- **未报告 / 未发现**。全文无 GitHub、repository、supplementary software 或代码链接；只给算法公式和复杂度表。
- 证据：`content.md:1-381` 全文；参考文献止于 `content.md:379-381`。

## 15. 身份 / 全文验证

- metadata title、正文首页 title、派遣 title 一致；DOI 在 metadata 与正文首页一致。
- 正文包含摘要、Sections 1–6、Table 1、Figures 1–4、References [1]–[20]，因此不是仅摘要页。
- metadata 指示来源 PDF、quality=good、title_check=match（`metadata.json:7-15`）。
- 公式在 Markdown 中缺图，但 canonical `source.pdf` 可辨认；这属于转换限制，不构成 paper identity failure。

## 16. FACT / INFERENCE / UNKNOWN 总表（source / target 边界）

| 证据域 | 标签 | 陈述 | 能否承重 |
|---|---|---|---|
| Source | FACT | 论文提出 RCFE：FCFO correlation refinement + ML ICFO；multi-lag metric 覆盖 `r=1,...,R-1` | 可承重，`source.pdf` (18)–(35) |
| Source | FACT | 式 (23) 用 `|R_m^(c)(r)|` 与 lag `r` 加权 residual phase | 可承重，`source.pdf` p.4 (23) |
| Source | FACT | RCFE 在本文仿真中接近 EMCB，CBFE 约有 1.25 dB loss，PBFE 运算量更高 | 仅在本文设置内可承重，`content.md:287-317` |
| Source | FACT | 系统为 5 GHz、5 MHz、1024-subcarrier、12-tap Rayleigh MIMO-OFDM | 可承重，`content.md:265-279` |
| Target | INFERENCE | 该论文限制未来 RML-FSTS 仅以“多 lag 加权融合”作为新颖点 | 可作为 collision 警示；不能单篇完成 novelty 判定 |
| Target | INFERENCE | correlation magnitude 可作为 receiver-visible reliability proxy 的候选原料 | 仅迁移假设；未在 FSO 中验证 |
| Target | UNKNOWN | 星地条件下 lag ranking 是否 crossover | 不可承重 |
| Target | UNKNOWN | conditioned single-lag cheap comparator 是否失败 | 不可承重 |
| Target | UNKNOWN | RML-FSTS 是否可命名、是否有效、是否 novel、是否 Go | 不可承重；本任务禁止推进 |

## 子表 A：真实信号输入

| 项目 | 全值 | 证据 |
|---|---|---|
| 接收输入 | 每个 RX branch 的一个去 CP、理想定时后的 `N` 维复时域训练向量 `x_m` | `content.md:45-55` |
| 发射训练 | 每 TX 的 FDM、等功率、等间隔 pilot；时域有 `R` 个相同 segment | `content.md:55-59,107-139` |
| nuisance | 每 TX/RX pair 的 `L`-tap channel 与 AWGN；统一 CFO（共用两端 oscillators） | `content.md:45-55` |
| 可观测统计 | `R_m(r)`：同一 RX branch 相隔 `rP` 的 sample correlation，跨 `m` 与 `r` 聚合 | `source.pdf` p.4, (18)–(23) |

## 子表 B：估计器输出（非 action space）

| 阶段 | 输出 | 类型 |
|---|---|---|
| coarse FCFO | `ε_hat^(c)` | 连续标量估计，不是 action |
| refined FCFO | `ε_hat` | 连续标量估计，不是 action |
| ICFO | `η_hat` | 从有限 integer hypothesis set 选出的估计，不是 control action |
| final | normalized CFO `ν_hat=R(ε_hat+η_hat)` | 参数估计输出；**无 action space** |

证据：`source.pdf` pp.4–5, (20),(23),(24),(31),(35)；`content.md:149-191`。

## 子表 C：奖励 / 真实目标 / 评价量

| 项目 | 内容 |
|---|---|
| Reward | **N/A（确定性/统计 DSP estimator，非学习型）** |
| 优化目标 | FCFO：最大化 concentrated likelihood `q(ε_tilde)`；ICFO：最大化 `ψ(η_tilde)` |
| 真实工程目标 | 在可接受处理量下准确恢复大范围 CFO，以避免 OFDM subcarrier orthogonality / BER degradation |
| 评价量 | CFO MSE `E[(ν_hat-ν)²]`、EMCB/CRB、ICFO failure probability `P_f=Pr{η_hat≠η}`、acquisition range、real-operation count |
| 关键公式 | `q`：(18)；`R_m(r)`：(19)；residual estimate：(23)；MSE：(38)；CBFE MSE：(40)；complexity：Table 1 |

证据：`content.md:23,141-165,201-259,287-317`；`source.pdf` pp.4–6。

## 子表 D：假设、位置与迁移影响

| 假设 | 原文位置 | 对 coherent-FSO 迁移的影响 |
|---|---|---|
| 所有 TX/RX pairs 共享同一 CFO | §2，`content.md:45` | 光学多支路是否共享 oscillator/CFO 要另验；不自动成立 |
| ideal timing recovery | §2，`content.md:45` | 排除了 timing-CFO coupling；不能证明联合失配下稳健性 |
| CP length `N_g≥L`、无 IBI | §2，`content.md:45` | FSO burst/frame 与 ISI model 必须重新定义 |
| AWGN，RX branches noise 独立 | §2/§4.1，`content.md:49,139` | 对 shot noise、colored noise 或支路相关噪声未验证 |
| `R` 个完全相同 training segments | §4.1，`content.md:107-139` | 是 multi-lag correlation 成立的核心观测结构；若 target TS 不重复则不可直接迁移 |
| residual `Δε` 足够小，可线性化 `sin(x)≈x` | §4.2，`content.md:155-161` | 大残差/低功率时可能产生 bias 或 cycle slip，需另验 |
| ideal FCFO compensation（推导 ICFO） | §4.3，`content.md:177-183` | 隐藏 FCFO error propagation；target 必须联合评估 |
| perfect ICFO（MSE/FCFO 对比） | §4.4/§5.2，`content.md:201,301` | Fig.1–3 不能代表 end-to-end CFO failure |
| channel 在 training 内固定，每 run 重采样 | §5.1，`content.md:269` | 不覆盖星地 burst 内动态湍流/phase noise |
| `L≤N/M=N/(QR)` | §4.4，`content.md:195-201` | 增大 repeat/lag richness 会收紧可支持 channel length，是迁移时必须审计的 trade-off |

## 子表 E：网络 / DSP 链 / 参数 / 复杂度

| 项目 | 内容 |
|---|---|
| 神经网络 | **N/A（非神经网络）** |
| DSP 链 | repetitive FDM preamble → RX segment correlations → lag-1 coarse FCFO → all-lag weighted residual refinement → FCFO counter-rotation → N-point DFT → discrete ML ICFO search → CFO combine |
| 关键参数 | `N,N_T,N_R,L,Q,R,M=QR,P=N/R,N_η=2|η|_max+1` |
| 实验参数 | `N=1024,L=12,R=8,Q=4,M=32`；每 TX 32 QPSK pilots |
| FCFO 复杂度 | RCFE `2N_R(R−1)(2N+3)` real operations |
| ICFO 复杂度 | RCFE `N_RN(5log2N+8LN_TN_η/M)` real operations |
| 数值例 | FCFO：57,500 ops；end-to-end CFO：252,500 ops（指定场景） |

证据：`content.md:223-247,265-301,317`；`source.pdf` Table 1。

## 子表 F：适配性

| 维度 | 判定 | 理由 |
|---|---|---|
| C3 prior-art ceiling | **适配** | 明确存在 multi-RX / multi-lag correlation likelihood 与幅度加权闭式 refinement |
| target defect evidence | **不适配** | 无 coherent-FSO、无 condition-dependent lag ranking、无 conditioned-single-lag comparator |
| recent baseline | **不适配** | 2009，不能满足 2019+ 门 |
| reusable estimator primitive | **部分适配** | `R_m(r)`、相位斜率、magnitude weight 可作为设计/碰撞检查原料 |
| direct implementation baseline | **不适配** | 需要 OFDM repetitive FDM preamble、MIMO multipath channel；任务/场景不匹配 |
| novelty proof | **不适配** | 单篇历史论文既不能证明新颖，也不能覆盖后续 2019+ 文献 |

## 子表 G：本文自身 M/C/A 与 canonical 四判据

### 本文自身 M-C-A

- **M（method）**：RCFE——repetitive FDM pilot 下的 two-step correlation FCFO + ML ICFO estimator。
- **C（condition）**：training-assisted MIMO-OFDM；common CFO、multipath channel、AWGN、ideal timing、`N_g≥L`，且时域 preamble 有 `R` 个重复段。
- **A（具体不足）**：exact joint ML 需在 CFO uncertainty range 上 line search、复杂度高；既有 PBFE 处理量大，CBFE 准确度/捕获范围受限（`content.md:15,25,35,107,235-259`）。
- **A 定位**：**计算复杂度 + 捕获范围 + 估计精度的具体技术矛盾**，不是“没人做过”的空白。
- **方法产出形态**：闭式/离散搜索组成的 deterministic CFO estimator、pilot placement rule、MSE/CRB 与 operation-count 分析。

| Canonical 判据 | ✅/❌ | 理由 |
|---|---:|---|
| 1. 具体 M-C-A | ✅ | 方法、场景假设和既有 ML/CBFE/PBFE 的具体不足均明确 |
| 2. 可复用方法产出 | ✅ | 有 pilot rule、multi-lag FCFO estimator、ICFO metric、复杂度和 MSE 公式 |
| 3. 近期 baseline | ❌ | 本文为 2009；其对手 [12]/[17] 也为 2004/2008，不能独立满足本项目 2019+ 近期门 |
| 4. 可量化对标 | ✅ | MSE、EMCB、failure probability、acquisition range、operation count 均有对比 |

**四判据总判定：3/4；因近期 baseline 门失败，本文不能单独产出本项目 Q#。** 这只是在当前项目门控下的证据分类，不是否定论文本身。

## 通信参数表

| 参数类 | 全值 | 来源 / 限制 |
|---|---|---|
| 链路 / 场景 | 5 GHz wideband wireless MIMO-OFDM；`N_T` TX、`N_R` RX | `content.md:21,43-55,265` |
| 调制 | training pilots 为 QPSK；data modulation 未报告 | `content.md:279` |
| 符号率 / 采样率 | sampling period 0.2 μs，即 sample rate 5 Msamples/s（后者为推算）；data symbol rate 未报告 | `content.md:265` |
| OFDM 参数 | `N=1024`，bandwidth 5 MHz，subcarrier spacing ≈4.9 kHz，useful block 0.205 ms | `content.md:265` |
| Training / frame | 1 个 training preamble；`R=8` repeated slots，`P=N/R=128` samples/slot；每 TX 32 pilots；CP length 仅约束 `N_g≥L`，具体值与完整 frame 未报告 | `content.md:45,107-139,279` |
| CFO | normalized CFO `ν=R(ε+η)`；Fig.1–3 每 run 均匀 `ν∈[-0.4,0.4)`；Fig.4 ICFO sets 见上 | `content.md:127-131,301,317` |
| Phase noise | 未建模 / 未报告 | 系统式只含 common CFO、channel、AWGN：`content.md:45-55` |
| 接收功率 / SNR | 绝对接收功率未报告；SNR=`σ_s²/σ_n²`。Fig.1–3 图示 0–18 dB；Fig.4 图示 −18 至 −6 dB | `content.md:287-317` |
| 湍流 | N/A；未建模 | wireless Rayleigh multipath，不是 FSO |
| 空间分集 | `N_T,N_R`；实验 `N_T=2,3,4`、`N_R=2,3,4`；RX 增益声称 `10log10(N_R)` dB | `content.md:279,299-315` |
| AO | N/A；未建模 | 非光学链路 |
| 信道模型 | `L=12` independent Rayleigh taps / pair，exponential PDP `exp(-4ℓ/L)`，unit total power；snapshot/run，training 内固定 | `content.md:265-279`；`source.pdf` p.6 (41) |
| 噪声 | zero-mean AWGN，variance `σ_n²` | `content.md:49,139` |
| 关键算法参数 | RCFE `Q=4,R=8,M=32`；PBFE `Q=32,{μ_i}={0,1,5}`；RCFE ICFO candidate count `N_η=2|η|_max+1` | `content.md:223-225,279-301,317` |

## 实验完备性审计（≤20 行）

| 项目 | 发现 |
|---|---|
| Claims + scope | 明确限定 training-assisted MIMO-OFDM CFO；仿真支持 MSE、range、failure、complexity，未做 BER/packet/hardware |
| Seeds / 次数 | 未报告 seed、Monte Carlo runs 数 |
| Error bar / 统计检验 | 均未报告；图只有点与曲线 |
| Baseline 数量 | 2 个可执行对手（CBFE、PBFE）+ 1 个 bound（EMCB）；另有 exact MLFE 理论参照 |
| Baseline 类型 / 来源 | correlation [12]、polynomial/MUSIC [17]、bound [20]，均有文献来源 |
| 公平调参 | pilot 数统一为 32/TX；RCFE/CBFE 同 training；PBFE 按原法用 Chu/Q=32，但 Q-range-complexity trade-off 未全扫描 |
| 消融 | 无模块消融；只有 `N_T`、`N_R` 影响分图 |
| 参数扫描 | SNR、`N_T`、`N_R` 有扫描；`R,Q,L,CFO magnitude` 未系统扫描 |
| 信道 / 参数来源 | Rayleigh exponential PDP 为自设 simulation model，未给实测/标准 profile 来源；公式完整 |
| 场景多样性 | 单 carrier/bandwidth、单 `L=12` model、单 training design；有限 |
| 复杂度 | 给封闭 real-operation formula、Table 1 及具体 operation counts；未给 wall-clock/memory |
| Verification (1–3) | **2/3**：理论 CRB/MSE 与 simulation 趋势对应，但无代码/独立 reproduction |
| Validation (1–3) | **1/3**：仅合成链路，无实测、hardware、BER 或 packet-level validation |
| Uncertainty (1–3) | **1/3**：无 run 数、seed、error bar、CI、统计检验；只有随机 channel/CFO 机制说明 |

## 最终边界结论

本文足以承重的只有：**2009 年 MIMO-OFDM prior art 已存在基于重复 preamble 的多 RX、多 lag correlation likelihood 以及 correlation-magnitude / lag 加权的 closed-form residual CFO refinement，并给出准确度—范围—复杂度权衡。** 它不承重星地 coherent-FSO 的 lag-ranking crossover、conditioned-single-lag failure、2019+ recent baseline、novelty 或 Go；这些均保持 **INFERENCE/UNKNOWN**。
