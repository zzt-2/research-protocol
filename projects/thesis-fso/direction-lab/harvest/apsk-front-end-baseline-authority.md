# APSK 前端均衡与软解调 baseline authority（GW Step 1）

> 任务：T040 | 日期：2026-08-30 | 范围：Groundwork Step 1 元数据与 comparator authority
> 检索证据：`search-archive/2026-08-30/apsk-front-end-baseline-authority.json`

## 一句话结论

C4-2 的公平主对手应是共享同一 pilot 初值与 payload 可靠度信息的 `pilot-LS + tuned DD-LMS/RLS`，并强制加入同初值 tuned RDE；C4-1 只在双奇异值近等、无显著 PDL 且记忆可忽略时允许 scaled-unitary 投影；C5-1 必须面对已有完整协方差 demapper，径向—切向度量通常会改变 LLR 排序，只有公共圆对称协方差时才退化为统一标量缩放。

## Step 1 证据范围

- 三个概念查询组覆盖：多环 APSK 盲/半盲均衡；CMA/MMA/RDE 与 Jones/PDL 条件；各向异性或非高斯残差下 APSK 软解调。
- 审查 58 条 title + abstract + venue + year + citation + publication-status 元数据；保留 39 条，其中正式发表占 94.9%。
- Fresh 结果实际来自 OpenAlex 与 arXiv；Semantic Scholar 在本轮被限速。Godard CMA 记录复用仓库既有 citation archive。
- 本文只冻结 Step 1 comparator 与适用前提，不把摘要当全文公式证据，不给候选 Go/Kill，不实现、不实验。

## Ch4 comparator 表

### C4-2：APSK 环感知半盲 Butterfly refinement

候选的实际信息合同是：`pilot-LS 初值 + 公共 APSK 环半径 + payload 判决/软可靠度 → refined 2×2 taps 与均衡符号`。因此只用纯盲方法作唯一对手会形成信息不对等。

| 对手 | 使用信息 | 输出 | 与 C4-2 是否同任务 | 冻结角色 |
|---|---|---|---|---|
| tuned CMA | payload 样本、单一模值统计；通常无 pilot | taps、均衡符号 | 输出同任务；信息更少，且单模代价与多环 APSK 不匹配 | 只作历史诊断锚，不作主 Go comparator |
| tuned MMA | payload 样本、多模/分量统计；通常无 pilot | taps、均衡符号 | 输出同任务；信息更少；对矩形 QAM 的实虚多模结构不等于 APSK 环结构 | 强邻居与 claim ceiling，不单独作为公平主对手 |
| tuned RDE | payload 样本、已知星座半径；默认无 pilot | taps、均衡符号 | 输出与环结构直接同任务；若不给同一 pilot 初值，信息仍少于 C4-2 | 必须扩展为“同 pilot-LS 初值 + tuned RDE”后进入 ladder |
| pilot-aided LS + DD-LMS/RLS | 与候选相同 pilots、payload 判决和可用可靠度 | refined taps、均衡符号 | 信息、动作点、输出均同任务 | **经典主 comparator** |

公平配置要求：所有 refinement 方法共享相同 pilot 位置、LS 初值、payload 区间、可靠度输入、tap 数、更新预算与冻结后的调参预算。若 C4-2 使用可靠度门控，DD baseline 也应看到同一可靠度分数；差异只能留在 ring-aware 更新律，而不能藏在额外信息里。

外部 authority 链：Godard 1980 是 CMA 基础；Yang–Werner–Dumont 2002 是 MMA 基础；Ready–Gooch 的 RDE DOI 为 `10.1109/ICASSP.1990.115806`；Fatadin–Ives–Savory 2009 在 coherent 16-QAM 中独立比较 CMA、RLS-CMA 与 RDE；Xu 2013 直接把 CMA 与 RDE 组合到 APSK。后两篇证明 RDE 不是只存在于基础论文中的孤立名字。

### C4-1：scaled-unitary Jones-LS

设 pilot-LS 得到的平坦 2×2 Jones 矩阵为 `H = U diag(σ1,σ2) Vᴴ`。scaled-unitary 成立的可执行判据是

`HᴴH = g²I`，等价于 `σ1 = σ2 = g`（允许噪声下的近似相等）。

| 条件 | scaled-unitary 判断 | 原因 |
|---|---|---|
| 共同幅度衰落/增益 × 无损 SOP 旋转 | 成立 | 两偏振只有共同尺度，Jones 部分为 unitary |
| 显著 PDL、偏振相关前端增益或未校准 I/Q/支路增益 | 不成立 | 两个奇异值不等，强投影会抹掉真实差分增益 |
| 频率平坦、PMD/ISI 在一个符号尺度内可忽略 | 单矩阵形式成立 | 一个 2×2 Jones 矩阵足以描述块内通道 |
| 有可见 PMD/频率选择性记忆 | 单矩阵形式不成立 | 即使无损通道可逐频 unitary，也应使用 paraunitary/Butterfly FIR，而非一个 flat projection |
| 去偏振或 Jones 模型本身失效 | 不成立 | 确定性 2×2 Jones 不能表示去偏振混合 |

因此 C4-1 不能预先假定为物理真相。Step 2/平台 authority 必须先给出 `σ1/σ2`、条件数与记忆长度的可引用范围。其比较对象应保留同 pilot 的 unconstrained LS，并加一个不假定等奇异值的廉价稳健逆（ridge 或 singular-value floor），避免把“降方差”误归因于 scaled-unitary 物理约束。

## Ch5 demapper comparator 表

### C5-1：APSK 径向—切向几何软解调

| demapper | 模型与可见信息 | 输出 | 对 C5-1 的角色 |
|---|---|---|---|
| 单一 `σ²` isotropic max-log | 所有符号共享圆对称高斯残差；均衡符号 + 一个方差 | bit LLR | 当前链/经典 anchor；只有残差近圆对称且同方差时充分 |
| per-ring scalar variance max-log | 每个 APSK 环一个标量方差，环内仍圆对称 | bit LLR | 最廉价直接扩展；先排除“只是环间噪声尺度不同”这一解释 |
| per-symbol/per-ring full covariance max-log | 簇均值、2×2 协方差、Mahalanobis 距离，必要时含 `log det Σ` | bit LLR | **同任务直接主 comparator 与 collision anchor**；Layton 等 2018 已对 optical/satellite data-dependent noise 明确使用簇协方差 |
| radial–tangential structured covariance | 径向/切向轴上的两个方差，方向由星座几何固定，可再做 pooling/shrinkage | bit LLR | 只有在估计因果性、低样本稳健性或结构约束上区别于 full covariance 时，才保留独立 recipe |

径向—切向动作不是天然的 LLR scaling。若符号 `s_m` 的度量为

`d_m = (z-s_m)ᴴ Σ_m⁻¹ (z-s_m) + log det Σ_m`，

改变径向/切向权重会非均匀改变不同符号假设的距离，可能改变最近竞争符号、bit-wise min 集合、LLR 幅值、排序甚至符号。只有所有 `Σ_m = cI` 且公共 determinant 时，才退化为对 isotropic 距离/LLR 的统一标量缩放。即便是 per-ring scalar，只要不同环的尺度不同，也可能重排跨环假设；它不是全局单一缩放。

当前 C5-1 与 Layton 等 2018 的 collision 风险为 **HIGH**：仅声称“用协方差/Mahalanobis 生成 LLR”不够。Step 2 必须核对其公式后，把候选差异压窄到例如 `pilot-only causal covariance + radial/tangential 结构化 shrinkage + DP-(8,8)-16APSK pooling`；强邻居限制 claim ceiling，但依 D031/D032 不自动 Kill 有明确完整 recipe 差异的有限 extension。

## 适用前提与碰撞风险

| 风险 | 当前判断 | 后续门 |
|---|---|---|
| CMA 被当成多环 APSK 公平主对手 | 不允许 | CMA 只保留历史锚；主对手必须同 pilot/decision 信息 |
| MMA 与 APSK 环结构被视为等价 | 不成立 | Step 2 核对 MMA 代价与 APSK 半径映射；不能从“multi-modulus”名称推断 exact task fit |
| RDE 吸收 C4-2 | 中高 | 用同 pilot-LS 初值、同预算 tuned RDE；若 ring-aware 更新无额外机制差异，则 claim 收窄 |
| scaled-unitary 在有 PDL 时仍强制投影 | 高风险错误 | 先量化奇异值比/条件数；显著 PDL 时回 unconstrained/regularized LS |
| full covariance 吸收 C5-1 | 高 | 必须全文核对 Layton 2018；候选须有结构化估计/因果信息/低样本稳定性的明确 delta |
| C5-1 只是 LLR scaling | 一般不成立 | 用 symbol metric/bit min-set 对照；只有公共圆对称协方差才是全局 scaling |
| 非高斯重尾残差 | UNKNOWN | 协方差只刻画二阶统计；若真实重尾明显，Gaussian Mahalanobis 仍可能失配 |

## 最小 baseline ladder

### C4-2

1. 当前链：pilot-only unconstrained LS。
2. 主 comparator：同 pilots、同可靠度输入、同更新预算的 `pilot-LS + tuned DD-LMS/RLS`。
3. 直接廉价扩展：同一 pilot-LS 初值的 tuned RDE；实现上可保留 CMA→RDE staged/hybrid 作为收敛初始化，但不再额外追逐无关 SOTA。

停止理由：以上三层已经分别覆盖“无 payload refinement”“同信息标准 DD refinement”“直接利用多环半径的经典 refinement”。再加普通 CMA/MMA 只重复较弱或结构不完全匹配的解释。

### C4-1

1. 当前链：unconstrained pilot-LS。
2. 主 comparator：不施加等奇异值假设的 ridge/Tikhonov LS。
3. 直接廉价扩展：SVD singular-value floor/condition-number clipping。

停止理由：两种廉价稳健逆已经覆盖一般性的降方差/病态求逆收益；scaled-unitary 只有在 `σ1≈σ2` 的物理门通过后，才能把额外收益归因于 Jones 结构。

### C5-1

1. 当前链：公共 `σ²` isotropic max-log。
2. 主 comparator：已有 data-dependent full-covariance max-log/Mahalanobis demapper。
3. 直接廉价扩展：per-ring scalar-variance max-log。

停止理由：三层覆盖公共圆噪声、环间异方差与完整二维相关性；在 candidate recipe 明确区别于 full covariance 前，不追加神经 demapper 或其他 SOTA。

## Step 2 必读候选（8 篇）

| # | 文献 | 作用 | 全文可得性 | Step 2 必核 |
|---|---|---|---|---|
| 1 | Godard, “Self-Recovering Equalization and Carrier Tracking in Two-Dimensional Data Communication Systems,” 1980, `10.1109/TCOM.1980.1094608` | CMA canonical | 当前元数据显示非 OA；仓库只有 citation metadata | cost function、适用星座假设、phase ambiguity、是否含 training/DD 转换 |
| 2 | Yang, Werner, Dumont, “The Multimodulus Blind Equalization and Its Generalized Algorithms,” 2002, `10.1109/JSAC.2002.1007381` | MMA canonical | 当前仓库只有 literature pointer，全文 UNKNOWN | MMA 实/虚代价、generalized form、对非矩形/多环星座的适用边界 |
| 3 | Ready, Gooch, “Blind Equalization Based on Radius Directed Adaptation,” `10.1109/ICASSP.1990.115806` | RDE canonical | 非 OA | 最近半径选择、更新式、收敛阶段；OpenAlex 年份标为 2002，与 DOI 中 1990 冲突，须核 proceedings |
| 4 | Xu, “Hybrid Blind Equalizing Method for APSK Signals,” 2013 | APSK 直接 CMA+RDE | 非 OA、无 DOI | weighted CMA/RDE 公式、radial dispersion、软切换、APSK 环配置和比较对象 |
| 5 | Fatadin, Ives, Savory, “Blind Equalization and Carrier Phase Recovery in a 16-QAM Optical Coherent System,” 2009, `10.1109/JLT.2009.2021961` | coherent optical 独立代表使用 | 非 OA | CMA/RLS-CMA/RDE 的调参、公平性、收敛图与 blind→DD 切换 |
| 6 | Kikuchi, “Digital Coherent Optical Communication Systems: Fundamentals and Future Prospects,” 2011, `10.1587/ELEX.8.1642` | Jones/偏振解复用 authority | OA PDF | Jones 矩阵、unitary/PDL/PMD 条件、flat 2×2 与 FIR/频域模型边界 |
| 7 | Layton et al., “Improved Demapping for Channels with Data-Dependent Noise,” 2018, `10.1186/S13638-018-1136-Z` | full-covariance direct collision | OA PDF | cluster covariance 估计、Mahalanobis 与 `log det`、训练/operation 信息、optical/satellite 场景和 4 dB 数字条件 |
| 8 | Zhang, Kim, “Performance Enhancement by Scaling Soft Bit Information of APSK,” 2013, `10.7840/KICS.2013.38C.10.858` | APSK scalar-LLR 对照 | OA PDF | 原始软值为何过度乐观、scaling 公式、是否改变排序、与 max-log/ML 的比较 |

## UNKNOWN

1. **Fresh 第三源交叉验证未完成**：S2 本轮限速；正式版本、引用数与 RDE 年份仍需 Step 2/DOI 页面核对。
2. **C4-1 平台前提未冻结**：共同 DP-FSO 链中真实 PDL、前端支路增益不平衡、PMD/有限 FIR 记忆的量级等待 T039；没有这些数字，不能宣布 scaled-unitary 合法。
3. **C4-2 的可靠度定义未冻结**：payload soft reliability 来自 demapper、equalizer residual 还是 decision distance，会改变与 LS+DD/RDE 的信息 parity。
4. **APSK 直接独立使用证据偏薄**：Xu 2013 与 MAPSK 2025 证明同族存在，但 APSK 上 tuned MMA、pilot-LS+DD、pilot-init RDE 的同一平台横向比较尚未找到。
5. **C5-1 exact-recipe collision 未闭合**：Layton 2018 很可能覆盖“簇协方差 + Mahalanobis LLR”的核心动作；须全文判断 radial–tangential 结构、pilot-only 因果估计和 shrinkage 是否构成可陈述差异。
6. **残差分布未知**：各偏振/各环的样本量、协方差条件数、圆对称性、重尾性和非高斯程度均未测；本任务不以设计假设替代观测事实。
7. **per-ring variance canonical source 未冻结**：它是明显廉价扩展，但本轮没有找到足够权威的 APSK 直接 canonical 文献，需在 Step 2 引用链中补核。
