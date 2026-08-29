# C5-0 LLR calibration — GW Step 3.5 exact-recipe closure

> T074｜2026-08-30｜CP015 / epoch 15｜candidate-specific bounded closure
> terminal: `STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM`

## 1. 控制与执行事实

- `validate_task_control.py`：`PASS`。T074 的 `control_ref`、epoch `15`、action class 与 checkpoint `CP015` 均和 foreground control 一致。
- 本任务只做 exact-recipe、九字段碰撞、B2↔B3 代数与 claim ceiling；没有进入 Step 4a，没有实现、仿真、coded grid、正式正文、Ch4 或 Skill/controller 修改。
- 检索只运行 Round 1；外部 wrapper 的一次双源调用 60 秒无返回后按时限止损，未把 source failure 记成零命中。随后只保留三类 arXiv 限定式、既有本地档案、Layton 双向引用链与三个只读核查结果。Round 2 未运行，因为 Round 1 已闭合 exact-neighbor 与代数问题，继续扩池不会改变 terminal。
- `search-archive/_index/all-papers.jsonl` 在启动时不存在；不能把“全局索引零命中”写成“无文献”。项目工具在 Layton 引用链后生成的索引只包含本轮 40 条引用记录，也不是历史全局索引。

## 2. Round 1 query / citation-chain receipt

各 feed 的召回范围与去重口径不同，且彼此有重叠，故不把它们机械相加成“全局唯一论文数”。可审计记录如下。

| feed | 查询/链 | raw | 去重/相关 | 结果 |
|---|---|---:|---:|---|
| 既有本地 C5-0 archive | `c5-0-q1..q8` | 2 | 2 | Yoshida 2020、Szczecinski 2011，均已在六篇 Step 3 池 |
| T074 family 1 | pilot/known-symbol residual + online LLR scaling + BICM/LDPC | raw 未稳定保留 | 7 个承重候选 | 4 MUST / 3 SHOULD；无 target exact collision |
| T074 family 2 | APSK/coherent optical/FSO + pilot-aided LLR/demapper | 211 | 209 unique；71 family hits | Cao 2015 与 Alvarado 2016 为最强邻居；无 target exact collision |
| T074 family 3 | direct variance plug-in + decoder-facing scaling | 134 个搜索界面记录 | 7 个 primary-verified 承重候选 | Wu 2013、El-Khamy 2014 闭合 online scaling/variance 邻域；无 target exact collision |
| 主线程三类 arXiv 限定式 | 三个 frozen query family 各一式 | 0 | 0 | source 返回零；不据此主张 novelty |
| Layton 2018 OpenAlex 双向链 | DOI `10.1186/s13638-018-1136-z` | 2 forward + 38 backward | 40 | forward 为 geometric shaping；backward 含 APSK soft demapper 等原子，无 target recipe |

各 feed 仅分别报告 raw=`2`、`211`、`134`、`40`；family 1 raw=`UNKNOWN`。由于 feed 重叠且计量单位不同，不报告跨 feed raw 总数；跨 feed unique union=`UNKNOWN`。最终科学 ledger 不按记录数量投票，只按 source→九字段映射裁决。

### 2.1 承重候选

| 候选 | primary/source pointer | 承重作用 | 证据边界 |
|---|---|---|---|
| Yoshida et al. 2020, *Post-FEC BER Benchmarking...* | `papers/arxiv/1911.01585v3/content.md:148-169,291-295,787,1192-1199` | coherent-optical、extrinsic-only global scaling、SD-FEC | 式(23)含 true SNR；pilot estimator/cadence 未给；PAS-QAM fiber |
| Alvarado et al. 2016, *Improved SD-FEC via Post-Processing of Mismatched LLRs* | [VDE primary proceedings abstract](https://www.vde-verlag.de/proceedings-en/454274190.html) | coherent-optical global linear LLR scaling；最强 exact-action neighbor | scalar 来自 offline AIR/GMI 标定，不是 current-frame pilot residual |
| Wu et al. 2013, *BICM Performance Improvement via Online LLR Optimization* | arXiv `1303.4452`；DOI `10.1109/WCNC.2013.6555189` | 每 transport/code block online LLR scaling | decoder hard decisions + approximate GMI；per-bit-channel；LTE QAM/turbo |
| Shibata et al. 2015, *Iterative Estimation of Undesired Signal Power...* | DOI `10.1186/s13638-015-0268-7`；Springer primary full text | pilot/decision residual → variance → direct LLR；最强 candidate-specific B3 neighbor | per-subcarrier、iterative turbo OFDM；不是 post-demapper global scalar |
| Cao et al. 2015, *Performance Investigation of Pilot-Aided LLRs for LDPC Coded CO-OFDM* | DOI `10.1109/JLT.2015.2392772`；[Optica primary abstract](https://opg.optica.org/jlt/abstract.cfm?uri=jlt-33-10-1961) | pilot + coherent optical + LDPC；最强 target-context neighbor | statistic 是 CPE/reference phasor；action 是 phase-aware likelihood，不是 variance/global scale |
| El-Khamy et al. 2014, *Online LLR Scaling for Robust Turbo Decoding* | DOI `10.1049/iet-com.2013.0471`；IET primary full text | decision-aided online noise variance + LLR scaling | 同时改变 channel/decoder messages；不是 frozen LDPC 或 pilot input |
| Layton et al. 2018, *Improved demapping for channels with data-dependent noise* | `papers/doi/10.1186_s13638-018-1136-z/source.md:120-162,199,350-358` | known APSK pilots → per-point moments → APP/extrinsic LLR | 约 `5M` 自由度、geometry+determinant 均改变；不是 global scalar |
| Szczecinski 2011 / Martinez 2008 / Alvarado 2017 | `papers/_read_notes/1111.7265v1.md`；`0805.1327.md`；`1709.10393.md` | classical global scaling、GMI 与 known-symbol residual 原子 | truth/offline/model-oracle 为主；未形成 target online recipe |

Zhang 2013 *Performance Enhancement by Scaling Soft Bit Information of APSK* 仍只有本地检索身份，primary full text 未取得。它构成 APSK-scalar claim limitation，但从现有题名/身份也不能证明 post-Ch4→Ch3、current-frame pilot residual、single global scalar、frozen LDPC 的九字段完整 recipe。

## 3. 九字段 exact-recipe matrix

目标九字段固定为：observation position、receiver-visible input、statistic、window/cadence、action target、freedom、decoder interaction、output、target scene。

| recipe | observation position | receiver-visible input | statistic | window/cadence | action target | freedom | decoder interaction | output | target scene | collision |
|---|---|---|---|---|---|---|---|---|---|---|
| **Q-C5-0 target** | post-Ch4 demux → per-tributary Ch3 CPR | current-frame known pilots | demeaned global residual variance/reliability | current buffered frame；decode 前一次 | channel/extrinsic LLR only | one positive global scalar/frame | frozen LDPC；不改 prior/内部消息 | calibrated LLR → decoded bits | DP-(8,8)-16APSK coherent-FSO | reference |
| Yoshida 2020 | coherent-fiber demapper | 4% pilots + assumed SNR；式(23)另需 true SNR | auxiliary SNR | estimator/cadence UNKNOWN | extrinsic LLR only | one global scalar | fixed SD-FEC | posterior LLR | PAS-QAM coherent fiber | `3/9` 近；scene/input/stat/cadence 不同 |
| Alvarado 2016 | post-demapper, pre-FEC | labeled development LLR/data（field-level pointer 未闭合） | AIR/GMI-optimal scalar | offline dataset（field-level pointer 未闭合） | mismatched LLR | one global scalar | rate-0.8 LDPC | scaled LLR | phase-noise coherent fiber | `4/9` 近；input/stat/cadence/scene 不同；未闭合字段按 `UNKNOWN` 对待 |
| Wu 2013 | detector 后、decoder 反馈后 | decoder hard decisions + LLR | approximate GMI/I-curve | transport/code block | detector LLR | per-bit-channel，可正负分档 | 先迭代 turbo 再优化 | scaled LLR | LTE 2×2 MIMO QAM | action/cadence 近；input/freedom/decoder/scene 不同 |
| Shibata 2015 | FFT/channel estimate 后 | adjacent pilots + decoded replica | pilot/decision residual power | packet / iterative（精确 cadence pointer 未闭合） | auxiliary variance plug-in，重算 LLR | per-subcarrier | turbo feedback | LLR → FEC | superposed RF OFDM PSK/QAM | input/stat/output 近；action/freedom/decoder/scene 不同；cadence 按 `UNKNOWN` 对待 |
| Cao 2015 | CO-OFDM demapper | pilot subcarriers/tone | phase reference/CPE posterior + noise power | `UNKNOWN`（primary abstract 未给 exact cadence） | pilot-aware likelihood | per-tone/phase metric | LDPC；tentative-feedback 细节未作承重 | PA/PT LLR | coherent-fiber QAM-OFDM | pilot/optical/LDPC 近；stat/action/freedom/scene 不同 |
| Layton 2018 | APSK demapper | known pilots + constellation-point identity | per-point mean/full covariance | pilot batch；cadence UNKNOWN | likelihood geometry + determinant | about `5M` | soft/iterative decoder | APP/extrinsic LLR | 64/128-APSK satellite/TWTA/phase noise | APSK/input/output 近；stat/action/freedom/scene 不同 |

**碰撞裁决**：没有一篇同时匹配九字段与目标平台。现有证据已经确认同动作、同输入原子、同 decoder-facing 输出和邻近 optical/APSK 场景分别存在，但它们分散在不同 recipe 中；不得拼接多篇原子后反称“单篇 exact collision”。

## 4. B2 ↔ B3 代数裁决

令 fixed constellation/centroid/gain 下的共同 circular-Gaussian auxiliary metric 为

\[
q_v(y\mid x)=C(v)\exp[-d_x(y)/v],
\]

B0 使用假设方差 `\tilde v=\tilde\sigma^2`，B3 直接 plug-in `\hat v=\hat\sigma^2`，B2 使用

\[
s=\tilde v/\hat v>0,\qquad L^{\mathrm{B2}}=sL(\tilde v).
\]

共同 normalization `C(v)` 在 bit-LLR 的分子/分母中消掉。

### 4.1 Max-log：条件内严格等价

在 uniform symbol weights、无 demapper a-priori、所有候选共享同一 scalar variance 且距离/label sets 固定时，

\[
L_i^{\max}(v)=
\frac{\min_{x\in\mathcal X_i^0}d_x-
      \min_{x\in\mathcal X_i^1}d_x}{v},
\]

故逐样本、逐 bit 严格有

\[
L_i^{\max}(\hat v)=\frac{\tilde v}{\hat v}L_i^{\max}(\tilde v)=sL_i^{\max}(\tilde v).
\]

因此在该合同内 B3 只是 B2 的 demapper 内重参数化；二者信息预算、输出和数值完全相同。若实现没有部署、稳定性或复杂度差别，B2 被 B3 完全吸收。

严格等价会被以下因素破坏：nonuniform/PS symbol prior 或 iterative demapper 的 other-bit a-priori；per-point/anisotropic covariance 与 symbol-dependent determinant；variance 以外的 centroid/geometry 更新；在 scaling 前后的 clipping、quantization 或 saturation；同一译码单元内按 symbol/bit 改变的 scalar，或 B2/B3 未共享同一方差映射；把 target-bit prior 一起缩放。跨 frame 变化但在各 frame 内共同、且两臂共享同一映射的 scalar，不破坏该 frame 内的 B2=B3。正确 posterior 组合应是 `L_post=L_prior+sL_ex`，不是 `s(L_prior+L_ex)`。

### 4.2 Exact APP：一般不等价

令

\[
Z_b(v)=\sum_{x\in\mathcal X_i^b}w_x\exp[-d_x/v].
\]

B3 为 `log Z_0(\hat v)-log Z_1(\hat v)`；B2 为
`s[log Z_0(\tilde v)-log Z_1(\tilde v)]`。二者逐样本严格等价当且仅当

\[
\frac{Z_0(\hat v)}{Z_1(\hat v)}=
\left[\frac{Z_0(\tilde v)}{Z_1(\tilde v)}\right]^s.
\]

该条件通常不成立，因为 `logsumexp(sa) != s logsumexp(a)`：先改变 symbol metric 温度再 marginalize，不等于先 marginalize 成 bit LLR 再外乘 scalar。逐样本等价当且仅当上式成立；若要求对所有 `v` 成立，则函数 `F(t)=log Z_0(1/t)-log Z_1(1/t)` 必须对 `t` 线性且过原点。除 singleton/dominant-symbol 情形外，两个 subset 的公共 partition factor 精确消去等结构也可成立。DP-(8,8)-16APSK 各 bit 不得仅凭 subset 含多个点排除严格等价，须在后续授权阶段逐 bit 做代数或数值恒等核查；高 SNR 单一 dominant symbol 只给近似。

### 4.3 四类性能语义

| 对象 | 正 global scaling 的结论 |
|---|---|
| uncoded hard sign | B2 的 channel-LLR sign 不变。exact APP B3 可因 subset 内竞争改变而翻 sign；PS 下 `L_prior+sL_ex` 的 posterior sign 也可变。 |
| maximum-metric codeword ordering | 若所有 channel metrics 同乘一个 `s>0`、无限精度、无未缩放复合项，则所有 codeword score 同比例，argmax 不变。跨 frame 不同 `s`、per-bit scalar、prior/CRC 项或量化/clip 均破坏。 |
| finite-iteration LDPC/BP | sum-product check update `2 atanh(prod tanh(m/2))` 非齐次，scale 会改变消息轨迹、早停和有限迭代 BER/FER；故“hard sign/ML ordering 不变”不能推出 coded BER 必不变。未量化纯 min-sum 与固定乘法系数的 normalized min-sum 均为正齐次；固定 offset、量化、clipping/saturation 或随幅值变化的 normalization 会破坏。 |
| GMI / ASI | 固定尺度的 LM/I-curve 数值可变；若 GMI 仍对一个公共 `rho>0` 取 supremum，则额外 global positive scalar 可被 `rho` 重参数化吸收，optimized GMI 不变。连续未量化 ASI 对一一正 scalar 也不变；binning/quantization/clipping 或 B3 的 APP shape change 可改变。两者均不能替代有限码 BER/FER。 |

## 5. Comparator 与信息预算

| arm | runtime information | freedom / action | 公平性与角色 |
|---|---|---|---|
| B0 | 同一 assumed auxiliary parameter；无新增信息 | `s=1`，原始 mismatched channel LLR | 正确未校准 baseline |
| B1 | development labels/GMI；runtime 固定值 | one offline fixed global scalar | 最强离线廉价 scalar；不得冒充 receiver-visible |
| B2 | current-frame known pilots、同一 residual window | one positive global post-demapper scalar | candidate recipe；只缩 channel/extrinsic LLR |
| B3 | 与 B2 完全相同的 pilots、residual statistic 和 sample count | 将 `\hat\sigma^2` 直接 plug-in auxiliary demapper | 同信息预算硬对手。max-log 条件内与 B2 严格相同；APP 下是不同且可能更强的 action |
| O1/B_match | true per-frame parameter / matched likelihood | oracle matched metric | 只给 headroom，不是 deployable baseline |
| Layton neighbor | pilots 还需按 constellation point 分组；原文 60/120 pilots per point 量级 | per-point mean/full covariance，约 `5M` | 只有在总 pilot/sample/latency 预算匹配时才可作性能强对手；不能把高维预算当 B2 同预算 |

`B2` 与 `B3` 必须共享完全相同的 pilot locations、count、demeaning、causal window 与 decoder。不能让 B3 使用更多/未来 pilots，也不能为了保留 B2 身份而删除 B3。

## 6. Operational minimum pilots / window

- 仍为 `UNKNOWN`。六篇 anchor 与新增邻居均没有给出 post-Ch4→Ch3、DP-(8,8)-16APSK global residual variance 的 operational minimum。
- 代数最低不是工程 authority：未知 mean 的 unbiased complex sample variance 至少需 `N_p>=2`；mean 已知为零时 `N_p>=1` 可计算，但都不能保证可靠工作。
- Layton 的 60/120 pilots per point 对应约 `5M` 高维 per-point estimator，不能迁移成 global scalar 的 minimum；Wu 使用整块 decoder decisions，Cao 的 pilot sweep面向 phase-aware CO-OFDM metric，也不提供本候选下限。
- 后续若获 Step 4a 授权，pilot count/window stability 必须作为 falsifier；可用复高斯方差估计的 chi-square 精度关系预注册设计，但不得冒充文献参数。

## 7. Claim ceiling

### 7.1 可主张

- 仅可把 C5-0 定位为：**在 DP-(8,8)-16APSK coherent-FSO 的 post-Ch4→per-tributary Ch3 接收链中，将 current-frame receiver-known pilot residual 约束为 one-global-scalar、channel/extrinsic-only、frozen-LDPC 的 target-scene classical migration recipe**。
- 可比较 B2 与 B3 的执行位置、APP 非等价性、数值稳定性、复杂度和有限迭代 LDPC 结果；任何性能主张必须等待另行授权的 Step 4a 与后续证据。

### 7.2 必须披露

- Wu 2013 已覆盖 online/per-block LLR scaling；Alvarado 2016/2017、Szczecinski、Martinez 已覆盖 global scaling/GMI；Shibata 2015 与 El-Khamy 2014 已覆盖 online variance/reliability 到 LLR；Cao 2013–2015 已覆盖 pilot-aided coherent-optical LLR；Layton 已覆盖 pilot-aided APSK likelihood。
- max-log uniform/common-variance 合同内 B2=B3；exact APP 一般不等价。
- operational minimum pilots、目标场景 headroom、coded BER/FER 改善及 B2 相对 B1/B3 的部署收益均未验证。

### 7.3 不得主张

- 首次 online/per-frame LLR scaling、首次 pilot-aided LLR、首次 APSK soft demapping、首次 variance plug-in；
- 新 LLR/GMI/ASI 理论、新噪声方差 estimator、SOTA 或跨场景普适性；
- 正 scaling 必然改善 GMI/ASI、LDPC BER/FER，或 hard sign 不变即可推出 coded BER 不变；
- “未检到 target collision”就是 novelty 证明。

RDL claim level 仅为 `CANDIDATE` 身份边界；没有 `RUN/CELL/SLICE` 性能证据，不能上升到 method signal 或 thesis contribution 已成立。

## 8. Terminal 与后续入口

### 唯一 terminal

`STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM`

理由：邻近场景已经存在相同动作、相同输入原子和 direct plug-in；B2 在 max-log 的冻结条件下也被 B3 严格重参数化。但没有证据确认同一 DP-(8,8)-16APSK coherent-FSO 平台、同一 post-Ch4→Ch3 observation、同一 current-frame pilot-residual statistic/cadence、同一 one-global-scalar channel-LLR action 与 frozen-LDPC output 的九字段完整 recipe。

该 terminal 不是方法成立或性能 Go，只允许主控另开纸面 Step 4a。下一入口若被单独授权，仍只能先做 A0/A'/A/B、B2/B3 correctness contract 与 pilot-window falsifier；不得从本报告直接实现或跑 BER。

### Blocker / limitation

1. operational minimum pilots/window 无 target authority；
2. Zhang 2013 APSK scalar primary full text 未取得；Cao 2015、Alvarado 2016 的本轮新增承重映射部分只有 primary abstract/proceedings evidence；
3. 未验证目标平台自然存在的 frame-global reliability drift、B0→O1 headroom、B2 相对 B1/B3 的部署差异或有限码增益。

这些限制永久压低 claim ceiling，但按 D053 不构成 target exact collision，也不自动关闭硕士级场景迁移。

## 9. Independent reviewer receipt

- 审查范围：只核 `source → 九字段 → B2/B3 等价 → terminal/claim ceiling`，未扩检索。
- 首轮：`FAIL / P0=0, P1=3, P2=1`。三项 P1 分别为异构 feed 错误合计、exact-APP 严格特例枚举过窄、fixed-coefficient normalized min-sum 齐次性表述错误。
- 修复后复核：`PASS / P0=0, P1=0, P2=1`。三项 P1 均关闭。
- 剩余 P2：部分新增外部邻居只有 DOI/primary abstract/full-text identity，未形成九字段逐字段页码/式号指针；未闭合字段已降为 `UNKNOWN` 或非承重。因这些来源的平台已明确不同，该 limitation 不影响 target-scene exact-collision terminal，但禁止把本次检索写成完备 novelty 证明。
