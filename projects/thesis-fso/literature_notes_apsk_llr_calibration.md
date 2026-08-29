# C5-0 APSK LLR calibration — GW Step 3 全文精读

> T072｜2026-08-30｜CP013 / epoch 13｜冻结六篇全文，未检索、下载、实现、仿真或进入 Step 3.5。

## 1. 事实与读数

- task-control validator：`PASS`。
- title/identity：6/6 人工或metadata核对通过；完整全文精读：6/6。
- QF5 canonical `source.pdf`：12页、2,261,353 bytes、SHA-256 `b53c96bd24de33c978febb65ea0f9e374e0420332a4d3aba8ec40ab0582b84df`；Eq.(6)、(9)–(12)与 `source.md` 一致。
- QF6 `source.pdf` 实为31,535-byte IEEE BLIT纯文本，不含 `%PDF-` header；正文完整，但保留 source-format caveat，不能称canonical PDF。
- 六篇中没有 FSO-direct scalar calibration，也没有“post-Ch4→Ch3 pilot residual → online (s)”的完整公式。全文池只闭合了经典 scalar、known/pilot reliability和APSK soft-demapper三类原子。
- 独立内容reviewer在回查六篇canonical fulltext后裁为 `PASS / P0-P1-P2=0-0-0`；唯一初审P2（Szczecinski的 (g_n)/SIR 被误列receiver-visible）已收紧为 `UNKNOWN / model-oracle` 后复核关闭。

| L# | 冻结论文 | title/全文 | C5-0角色 | online支持 | truth/offline边界 | read note |
|---|---|---|---|---|---|---|
| L01/QF2 | Szczecinski 2011 | PASS / full | scalar mathematical/model primitive | 未闭合；解析例依赖model-oracle参数 | 式(12)需bit-conditioned分布；SNR/SIR与 (g_n) 可见性未闭合 | `papers/_read_notes/1111.7265v1.md` |
| L02/QF3 | Alvarado et al. 2017 | PASS / full | residual与GMI两个分离原子 | known symbols可估auxiliary variance | 式(34)/(35)需bit truth；未给residual→(s)桥 | `papers/_read_notes/1709.10393.md` |
| L03/QF4 | Yoshida et al. 2019/2020 | PASS / full | SNR-only analytic scaling strong neighbor | pilots用于auxiliary SNR estimate，公式缺失 | 式(23)分子是true SNR；ASI/GMI含bit truth | `papers/_read_notes/1911.01585v3.md` |
| L04/QF1 | Martinez et al. 2008 | PASS / full | mismatched BICM/GMI background | no support | (s)是true joint law下的offline variational parameter | `papers/_read_notes/0805.1327.md` |
| L05/QF5 | Layton et al. 2018 | PASS / full+PDF | APSK high-dimensional strong neighbor | pilots→per-point centroid/covariance | oracle NMSE/MI/EXIT用truth；不是scalar recipe | `papers/_read_notes/10.1186_s13638-018-1136-z.md` |
| L06/QF6 | Xie et al. 2009 | PASS / BLIT fulltext | APSK one-shot/iterative identity boundary | decoder (L_a)可见；pilot/residual no support | AMI/BER用offline truth；无calibration | `papers/_read_notes/10.1109_vetecs.2009.5073425.md` |

## 2. 六篇逐文公式—IAO 摘要

| 论文 | 承重公式/位置 | input | action | output | 自由度/样本合同 |
|---|---|---|---|---|---|
| Szczecinski | GMI scalar (12) `:230-245`；CGF scalar (37) `:518-535` | (p_{\tilde L|C})或已知模型参数 | (L^c=\alpha L) | channel LLR→soft decoder | global或per-index；window/cadence/min samples均UNKNOWN |
| Alvarado | empirical GMI (34)/(35) `:767-821`；known-symbol residual `:789-794` | known (x,y)；另需bit-labeled LLR | 估auxiliary variance；offline优化global (s) | LLR/GMI/AIR | 一个global (s)；两原子未被原文连成online方法 |
| Yoshida | (L^{po}=L^{pr}+sL^{ex}) (1) `:148-169`；(s_o=\mathrm{SNR}/\widehat{\mathrm{SNR}}) (23) `:291-295` | 4% pilots、assumed SNR；式(23)另需true SNR | 只缩放channel/extrinsic LLR | posterior LLR→SD-FEC | global；pilot estimator/window/cadence/min samples UNKNOWN |
| Martinez | GMI exponent (58)–(61) `:573-609` | true joint distribution或labeled MC samples | (q\mapsto q^s)，等价log metric global scaling | GMI/error exponent | global；不是runtime controller |
| Layton | APP/extrinsic (6)/(9)、per-point likelihood (10)、pilot moments (11)–(12) `source.md:120-162` | known pilots及point labels | per-point `mu_k,Sigma_k` likelihood | APP/extrinsic LLR | 约(5M)实参；120 pilots/point，64阶约6% overhead |
| Xie | iterative demapper (4)，(L_a=0)退化one-shot `content.md:120-124` | (y)+decoder a-priori LLR | reweight symbol likelihood sums | updated bit LLR→LDPC | per-bit/per-iteration；8×50 iterations；无pilot estimator |

传统通信论文不适用的 DRL 字段在六篇 read note 中均明确为 `N/A（传统通信非DRL）`，未省略。

## 3. B0、B_match/O1 与 comparator ladder

### 3.1 冻结身份

- **B0 — uncalibrated mismatched LLR**：同一 one-shot max-log/APP demapper、同一估计或假设的 auxiliary-channel 参数 (\hat\theta)，原始 channel/extrinsic LLR直接进入冻结 LDPC decoder，`s=1/alpha=1`。
- **B_match/O1 — matched reference**：使用 true/statistically matched (p(y|x)) 或 true residual/noise parameter (\theta_{true}) 构造 likelihood。matched状态下最优 (s=1)，但它不是B0。
- Yoshida 后半部 approximately matched且 (s=s_o=s_d=1) 的曲线属于 matched-near reference；不能用来证明“同一错误参数下B0失败”。
- Layton的 standard demapper是centroid-aware、constant circular covariance；Xie的 (L_a=0) 是one-shot independent demapper。二者补充baseline身份，但都不改变C5-0的冻结定义。

### 3.2 合法梯级

| ID | arm | 信息与预算 | 用途 |
|---|---|---|---|
| B0 | same demapper / same (\hat\theta) / (s=1) | 不增信息 | 正确未校准baseline |
| B1 | 一个offline固定global scalar (s_{fix}) | development labels/GMI，只能离线冻结；runtime无新增信息 | 最强廉价scalar alternative |
| B2 | receiver-visible per-frame global scalar (s_t) | 与candidate相同pilot位置、数量、窗口和decoder预算 | 唯一Q#的候选recipe |
| B3 | 直接把同一pilot residual variance plug-in auxiliary demapper | 与B2完全同pilot budget | 检验B2是否只是重参数化；max-log/APP须分别核对 |
| O1/B_match | true per-frame parameter或matched likelihood | oracle truth，仅reference | headroom与claim ceiling |
| N1 | Layton per-point covariance neighbor | 只有在同pilot/sample预算可公平时列性能arm | 高维强邻居，不是scalar exact recipe |

`B1` 与 `B2` 必须分开：前者是全数据分布的固定标定，后者是每个目标frame只用receiver-known pilots更新。若B3与B2代数等价或完全吸收增益，应如实把B2身份降为“plug-in variance的缩放实现”。

## 4. receiver-visible 与 truth/offline 的硬边界

### 4.1 原文已经支持

1. 已知 symbols/pilots 的接收残差可估 auxiliary Gaussian variance或per-point moments：Alvarado `content.md:789-794`；Layton Eq.(11)–(12) `source.md:150-162`。
2. mismatched channel LLR可施加正scalar：Szczecinski Eq.(12)/(37)、Martinez Eq.(58)–(61)、Yoshida Eq.(1)/(23)。
3. Yoshida只缩放 (L^{ex})，不缩放 (L^{pr})；C5-0亦只允许channel/extrinsic LLR动作。
4. uniform signaling与正scalar下，uncoded bit sign不变；收益只能落在soft-decoder/GMI/BER/FER链上。PS时prior非零，posterior sign可能变化，不能泛化不变性。

### 4.2 原文没有支持

- 没有论文证明 (s_{GMI}=g(\hat\sigma^2_{pilot})) 的普适关系。
- Yoshida Eq.(23)含true SNR；不能写成“pilots直接产生 (s_o)”。
- Alvarado Eq.(34)/(35)、Szczecinski Eq.(12)和Martinez GMI都需要bit truth或offline distribution。
- 六篇都没有给post-Ch4→Ch3平台的causal pilot window、per-frame cadence或operational minimum samples。
- per-ring、per-bit-channel与per-point自由度不由global pilot statistic自动支持；Layton的per-point estimator需要显著更高pilot budget。

## 5. 唯一 canonical Q#

### Q-C5-0 — post-Ch4→Ch3 pilot-residual per-frame global LLR calibration

#### 5.1 M-C-A 与四判据

| 要素 | 冻结陈述 |
|---|---|
| M | B0：冻结的一次one-shot max-log/APP APSK demapper，沿用同一名义/滞后的auxiliary reliability参数并令 (s=1) |
| C | `Ch4 demux → Ch3 per-tributary CPR` 后，frame间共同residual reliability/有效variance变化；接收机有known pilots，但B0的LLR幅度未随该frame更新；目标只限global scale mismatch主导、尚未进入明显per-point/anisotropic regime的frame |
| A | B0假设其auxiliary metric的可靠度刻度在frame间仍与真实conditional LLR一致；当共同scale失配时，LLR sign大体仍对但幅度不consistent，冻结soft LDPC decoder的GMI/BER/FER受损 |
| 产出 | 一个block-causal、receiver-visible、per-frame global channel-LLR scalar recipe及其同预算comparator ladder |

| 判据 | 结果 | 依据 |
|---|---|---|
| 1 具体M-C-A | ✅ | M、C、A均指向同一one-shot demapper和共同reliability-scale失配 |
| 2 可复用方法产出 | ✅ | pilots→frame scalar→channel LLR→frozen decoder是一条可复用receiver recipe |
| 3 有baseline可对标 | ✅（claim受限） | Yoshida 2020提供SNR-mismatch scalar边界，Layton 2018提供APSK pilot likelihood强邻居；B0/B1/B3/O1身份明确 |
| 4 可量化对标 | ✅ | GMI/ASI、coded FER/BER、calibration error、pilot overhead和复杂度均可同预算比较 |

#### 5.2 receiver-visible input → action → output

以下是**由全文原子综合出的候选设计合同，不是任一论文原文公式**：

1. **Input**：buffered frame中协议已知的post-Ch4→Ch3 pilot pairs ((x_p,y_p))，以及B0 demapper自己持有的assumed auxiliary scale (\tilde\sigma_t^2)。不使用data-bit truth、true SNR或future frame。
2. **Statistic**：在同一frame、同一冻结front-end后形成 (e_p=y_p-x_p)，去除pilot mean后估一个全局residual variance
   \[
   \hat\sigma_{p,t}^2=\frac1{N_p-1}\sum_{p=1}^{N_p}|e_p-\bar e_t|^2.
   \]
   这是对Alvarado known-symbol residual和Layton pilot moments的低维综合。代数最低 (N_p\ge2)，但这不是可靠工作的operational minimum。
3. **Action**：只在“共同Gaussian/SNR scale mismatch”假设下，用Yoshida式(23)的variance-ratio对应关系构造一项frame-global (s_t)；候选写作
   \[
   s_t=\tilde\sigma_t^2/\hat\sigma_{p,t}^2,
   \qquad L^{out}_{t,k}=s_t L^{ch}_{t,k}.
   \]
   比例方向、max-log/APP等价性以及B3 plug-in equivalence均必须在后续阶段独立核对，当前不把该综合式冒充原文定理。
4. **Output**：(L^{out}) 直接进入冻结LDPC decoder；prior/a-priori LLR与decoder内部消息不缩放。
5. **Causality/cadence**：frame-buffered block-causal；只用当前frame已收到的known pilots，解码该frame前更新一次，随后对该frame全rings/bit-channels使用同一scalar。若实际接收机不允许frame buffering，必须改成“最近已收pilot group→后续data”，不能使用未来pilots。
6. **Freedom**：先只允许一个per-frame global scalar；不开放per-ring、per-bit或Layton per-point参数。跨DP tributary pooling vs separate只作为必要消融，不能同时主张两个方法。
7. **Minimum samples**：全文只给Alvarado通用 (D) 与Layton高维60/120 pilots/point；global scalar的operational minimum仍 `UNKNOWN`。因此 (N_p) 稳定性是后续falsifier，而不是当前可声称的定值。

#### 5.3 可证伪目标场景与最低必要消融

- 目标场景：B0的LLR reliability随frame发生可测的共同scale drift；pilot residual与held-out data LLR mismatch同向；同一decoder下存在B0→O1 headroom。
- 直接否决条件：B0与O1无GMI/FER/BER headroom；B2被B1/B3完全吸收且无部署/稳定性差别；pilot statistic与held-out reliability不相关；或per-point/non-Gaussian mismatch主导到global scalar无效。
- 主指标：冻结LDPC的FER/BER；辅助指标：GMI/ASI、LLR calibration/consistency、pilot overhead、每frame运算量。
- 最低消融：B0/B1/B2/B3/O1；global固定vsper-frame；pooled-vsper-tributary；pilot-count/窗口稳定性；uniform-prior hard-sign sanity；必要时同budget N1 high-dimensional neighbor。

## 6. Layton与Xie的边界裁决

- Layton每点 (\mu_k,\Sigma_k) 同时改变Mahalanobis geometry和determinant normalization，约(5M)自由度。它是input/output邻近但action不同的高维strong neighbor，不能重命名成scalar exact recipe。
- Xie Eq.(4)在 (L_a=0) 时就是one-shot independent demapper；加入iterative feedback不改变B0身份。其动作作用于decoder a-priori feedback，若C5-0加入该反馈就进入经典BICM-ID邻域且必须单独控制8×50 iteration/interleaver预算。

## 7. 实验完备性与写作架构提取

| 论文 | claims/scope | 统计规范性 | baseline/消融 | 信道/复杂度/VVUQ |
|---|---|---|---|---|
| Szczecinski | PEP/BER下的经典scalar correction | 未报seeds/CI/总bits | B0/GMI/Gaussian/WLSF/matched | interference+Rayleigh；Newton 2步；3/2/1 |
| Alvarado | AIR/GMI统一与fiber lower bound | coded examples无CI | MI/GMI/exact/max-log/auxiliary | AWGN+nonlinear fiber；MC/GH；3/2/1 |
| Yoshida | PS-BICM post-FEC benchmark边界 | 每点>500 codewords，无CI | 多metrics/mappings；nearly matched | coherent fiber；scalar复杂度未报；3/2/1 |
| Layton | data-dependent covariance demapping，最高约4 dB为场景上限 | 大样本BER/MI，无seeds/CI | circular/centroid/full covariance，多pilot点 | TWTA/phase noise；7 vs4 mult，MATLAB<1%；3/2/1 |
| Xie | APSK BILCM-ID AMI/BER恢复 | 无总bits/CI | BILCM/CM limits/interleaver | AWGN；8×50 iterations，复杂度只定性；2/2/1 |

写作可复用骨架仅作内部参考：Alvarado适合“理论metric→实验估计→auxiliary lower bound”；Yoshida适合“等价成立条件→量化/实际FEC边界”；Layton适合“先证scalar geometry失配→再上高维likelihood→按pilot/complexity分解”。本任务不据此写正式正文。

## 8. 综合分析

1. **方法分类**：QF1/QF2/QF3/QF4形成mismatched BICM scalar/GMI族；QF3/QF4提供coherent-optical reliability入口；QF5是APSK per-point likelihood族；QF6是APSK iterative-feedback族。
2. **共同局限**：经典scalar多依赖bit truth/true distribution/true SNR；pilot moment papers不提供low-dimensional residual→(s)映射；所有论文都缺目标FSO平台的causal sample contract。
3. **演进**：2008–2011先建立mismatched decoding/scalar理论；2017–2020扩到coherent optical AIR/post-FEC benchmarking；APSK direct papers分别走高维 likelihood与iterative feedback，未给target global online scalar。
4. **研究定位**：合法身份不是新LLR scaling理论，而是把经典global scalar与receiver-known post-front-end pilots约束成一个frame-level APSK/FSO receiver recipe，并用B3/O1/Layton强邻居限制claim。

## 9. Step 3 裁决

- canonical Q#：`Q-C5-0`（唯一）。
- 四判据：`4/4`，但方法身份明确是经典原子迁移，且online公式为全文原子综合推断。
- terminal：`STEP3_CLASSICAL_MIGRATION_READY_FOR_STEP3_5`。
- claim ceiling：**receiver-visible、frame-level、global channel-LLR scalar calibration 在共同DP-(8,8)-16APSK coherent-FSO平台的受限场景迁移**。不得声称首次/SOTA、新GMI/LLR scaling理论、新pilot variance estimator、首次APSK covariance demapping或全面领先。
- blocker：六篇没有直接闭合“target pilot residual→(s_t)”的原文公式，也没有operational minimum pilots；B2与直接plug-in variance的max-log/APP等价/吸收风险高，且无FSO-direct/APSK-scalar全文。该blocker限制claim并是Step 3.5/后续可行性必须审查的入口，但不使receiver-visible IAO为空。
- 唯一下一步：由主控决定是否另开**bounded Step 3.5 exact-recipe/collision closure**。本任务不执行Step 3.5、实现或仿真。
