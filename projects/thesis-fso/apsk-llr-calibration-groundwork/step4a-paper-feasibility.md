# C5-0 LLR calibration — GW Step 4a 纸面可行性

> T075｜2026-08-30｜CP016 / epoch 16｜local-evidence-only
> terminal: `PAPER_DIMENSIONS_PASS_B2`

## 0. 裁决先行

`Q-C5-0` 的纸面维度以 **B2 形态**存活：

> **导频残差驱动的逐帧 post-demapper channel/extrinsic-LLR 全局正缩放**：在
> `post-Ch4 demux → per-tributary Ch3 CPR` 后，只用当前帧 receiver-known
> pilots 估一个正 scalar，对冻结 DP-(8,8)-16APSK demapper 的 channel/extrinsic
> LLR 作一次公共缩放，再送入冻结 LDPC。

这不是对理想 decoder 的增益断言：

1. 无 clipping、quantization、offset、固定参考消息时，固定 `alpha=0.75` 的
   normalized min-sum 对公共正缩放正齐次，20 轮后的 hard output 不变；
2. uniform prior、共同 isotropic variance、固定 geometry/label、**未裁剪** max-log
   下，B2 与 direct variance plug-in B3 逐样本逐 bit 严格相同；
3. 若目标 APSK seam 沿用当前 LDPC adapter/backend 的候选合同，则含 demapper preclip
   `30`、decoder input/internal clip `20` 与固定幅值 filler；B2 的 current-frame scalar
   位于这些固定非齐次边界之间。B1 的 runtime scalar
   固定，不能解析吸收逐帧作用；现有证据也没有授权或证明一个 adaptive threshold/filler
   controller 能在不改变冻结 decoder contract 的条件下完全吸收 B2。

B3 exact APP 改变 auxiliary variance 后再对 symbol metrics 做 log-sum-exp，一般不等于
先形成 bit LLR 再外乘 scalar；它保留为同 pilots/statistic/window、同信息预算的强
comparator 与 correctness 分叉，不与 B2 拼成双自由度方法。PASS 只允许另开 B2
correctness-only seam，不代表 coded BER/FER 改善或方法成立。

## 1. 控制、证据与解析 ledger

### 1.1 控制

- `validate_task_control.py` 对 T075 返回 `PASS`。
- 当前 authority 是 `.sessions/2026-07-09-thesis-writing/topic-index.md` 的
  CP016；D054/V029 只开放 A0/A′/A/B 与 correctness contract。
- 本任务未联网、未检索/下载、未实现、未仿真、未跑 BER/FER，未修改 Ch4、
  Skill/controller、正式论文正文或主控治理文件。

### 1.2 解析 ledger

| 问题 | 本地事实 | 纸面结论 |
|---|---|---|
| 目标链是否自然产生 reliability mismatch？ | T066 的同一合法链已持久化 64 个 current-frame known-pilot residual windows；cell 固定为 moderate GG、15 dB、memoryless unitary Jones、plain RDE、per-pol Ch3 DA CPR，未加 PDL/PMD/FIR/IQ。对既有 raw 做只读 reduction：每 window、每 polarization 分别 demean 后合并的 unbiased complex residual power为 `min=0.01410, median=0.06547, max=1.16298, mean=0.15834, CV=1.691`；相对 cell nominal AWGN complex power `10^(-15/10)=0.0316228` 为 `0.446×–36.777×`。 | **自然 mismatch 现象成立**，不是新增损伤制造；但 pilot statistic 对 held-out payload conditional reliability 的预测充分性尚未验证，保留为后续 falsifier。 |
| B2 对理想 fixed NMS 是否有 causal headroom？ | 当前 decoder 为 fixed `alpha=0.75` normalized min-sum、20 iterations、offset `0`；去除 clip/quantization/固定参考消息后，VN sum 与 CN sign-min 均正齐次。 | **没有**；公共正缩放不能改变 hard output。 |
| 实际实现有什么非齐次项？ | `codec.py:150-163,178-193,199-202,280-325`：demapper preclip `30`、decoder input/internal `llr_max=20`、fixed 20 iterations。Sionna 2.0.1 本地源码核查还显示 rate recovery 注入固定 `-llr_max` filler LLR。 | clipping、finite precision/quantization、非零 offset（当前为 0）、固定 filler/reference LLR、early-stop/CRC 或未缩放 prior 才能破坏公共尺度齐次；当前无 early stop、无 prior、offset=0。 |
| B2 是否能借固定 clipping/filler 存活？ | scalar 与 clip 的作用次序会改变饱和样本；实际 decoder 还有内部 clip 与固定 filler。B2 是 post-demapper current-frame scalar，而这些边界按当前 decoder contract 固定。 | **存在自然非齐次作用链**。B1 只吸收 stationary 部分；把所有 clip/filler 阈值改成逐帧控制器并非当前 B1，也不是冻结 decoder contract 内已证明的解析吸收者。该链是否产生正 FER headroom 仍须 O1/B2 correctness 后单格 falsify。 |
| B2 与 B3 max-log 是否不同？ | Step 3.5 已证明冻结条件内 `L_max(hat v)=(tilde v/hat v)L_max(tilde v)`。 | **完全等价**；不得改名保留 B2。 |
| B3 exact APP 是否仍有 action？ | `logsumexp` 在改变 metric temperature 前后不与外乘 scalar 交换；目标 16APSK 每 bit partition 均含多 symbol。 | **一般不等价**；保留为同信息预算 comparator/correctness 分叉，须逐 bit 分类，不取代或与 B2 叠加。 |
| target codec/demapper 是否已闭合？ | APSK mapper/label fingerprint 与 positive-means-bit-1 exact-sum LLR seam 已存在；5G BG2 `k=1024,n=1536,Qm=4` decoder 也存在。但 `D0Codec.demap()` 仍硬编码 Gray-16QAM，APSK exact-APP seam 未与 encoder interleaver、1536-bit decoder batch形成同一 receipt。 | 纸面 action 可定义，但 **下一 correctness seam 的最小 blocker** 是 target APSK demapper→5G LDPC bit-order/sign/noise-factor 集成；未闭合前不得跑 headroom。 |

只读 reduction 的来源是
`projects/simulation/explore/ch5-apsk-structured-covariance/occurrence_raw.json`；
cell、pilots 与禁止损伤由同目录 `occurrence_manifest.yaml` 冻结。该 reduction 只证明
pilot residual 尺度自然变化，不把 payload truth 或已有 C5-1 负结果改写成 C5-0 性能证据。

## 2. A0：问题是否真实存在

### 2.1 冻结 M-C-A

| 要素 | 陈述 |
|---|---|
| M | B0：同一 one-shot APSK auxiliary demapper 使用固定/名义共同 variance，`s=1`，channel/extrinsic LLR 直接进入 frozen LDPC。 |
| C | post-Ch4→per-tributary Ch3 后，current-frame known-pilot residual power 在合法目标链中自然变化，而 B0 的 auxiliary reliability 不随帧更新。 |
| A | B0 假设固定 auxiliary parameter 仍与该帧 conditional likelihood 一致；尺度/temperature 失配时，exact-APP bit-LLR shape 与有限、非齐次实现的 decoder trajectory 可能失配。 |
| 最简产出 | current-frame pilot residual → one positive global post-demapper channel/extrinsic-LLR scalar → frozen LDPC；即 B2。 |

### 2.2 四项问题门

| 判据 | 结果 | 依据与边界 |
|---|---|---|
| 现象 | **PASS** | T066 既有 64-window raw 显示 residual complex power 相对 nominal AWGN 跨 `0.446×–36.777×`；没有加入 IQ/PDL/PMD/FIR、新湍流档或 synthetic anisotropy。 |
| 机制 | **PASS（claim-limited）** | GG/残余 carrier tracking/有限 Ch4-Ch3 processing 自然把 fixed nominal AWGN parameter 变成 mismatched auxiliary parameter；不得把现有非圆/point-dependent occurrence说成“纯 global scale 已证实”。 |
| receiver-visible 可观测性 | **PASS with debt** | current-frame known pilots、`z_pilot`、`x_pilot`、`e` 已由 bridge firewall 证明 receiver-visible；pilot-to-held-out reliability correlation 尚未测，后续不相关即 falsify。 |
| 可操作改善路径 | **PASS for B2（paper-only）** | 理想 NMS 是最强解析 falsifier；实际冻结链的 fixed preclip/internal clip/filler 破坏齐次，给 current-frame post-demapper B2 留下可能改变 finite decoder trajectory 的唯一作用缝。B1 runtime 固定，不能解析吸收；B3 exact APP 作为强 comparator。 |

按 `stages/glossary.md` 的问题四判据，Q-C5-0 仍为 `4/4`：M-C-A 具体；B2
是可复用 receiver recipe；B0/B1/B3/O1 与强邻居可对标；coded BER/FER、
overhead、calibration error 可量化。这里的 baseline 是传统 B0，不用 O1 当 Go
对手；O1 只做 headroom falsifier。

### 2.3 operational pilot count / window

operational minimum 保持 `UNKNOWN`。T066 的 `64 pilots/polarization/256-symbol
window` 只是一个已有合法 cell，不是目标最小值 authority；代数上 `N_p>=2` 也不
等于可靠工作。

后续 falsifier 必须是：在不改变 cell、statistic、decoder 或 action 的条件下，冻结
若干协议允许的 pilot sub-count/window，只用 calibration split 选择一个满足预注册
稳定性门的最小档；若 `hat N0` 对 held-out residual reliability 的误差/相关性随减样本
不稳定，或任何合法 pilot 档都不能预测 held-out reliability，则关闭 B2。不得临场
选一个只让 estimator 有用的 `N_p`。

## 3. A′：竞争维度与指标

### 3.1 主维度

主维度只允许：相同 LDPC identity、码长、20 iterations、LLR clip、pilots/overhead、
paired realization 与 decoder-call budget 下的 coded BER/FER。FER 优先，BER 伴随。

机制诊断包括 uncoded BER、GMI/ASI、pilot variance error、LLR calibration/consistency、
clip incidence 与每帧运算量；这些不能替代 coded BER/FER。

### 3.2 四类尺度语义

| 对象 | 公共正缩放 / B3 的语义 |
|---|---|
| uncoded hard sign | B2 不改 sign。B3 exact APP 因 subset 内 symbol 竞争可改变 bit-LLR shape，个别样本 sign 也可能改变。 |
| ideal maximum-metric ordering | 若所有 channel metrics 同乘同一 `s>0`、无限精度且没有未缩放 prior/filler/CRC 项，所有 codeword score 同比例，argmax 不变。 |
| fixed NMS | 无 clip/quantization/offset/fixed reference 时正齐次，任意固定轮数 hard output 不变；实际 clip/filler 才提供非齐次 seam。 |
| exact APP | 改 auxiliary variance后再 marginalize 一般不同于对 bit LLR 外乘 scalar；因此 B3 是必须保留的同信息预算强 comparator，不是 B2 的附加自由度。 |
| GMI / ASI | 只作诊断；optimized GMI 可把 global scalar重参数化吸收，ASI 在未量化一一正缩放下也可不变。 |

## 4. A：因果 headroom 与 action 选择

### 4.1 fixed normalized-min-sum 正齐次证明

令所有 transmitted-bit channel LLR 乘 `c>0`，并暂时移除 clipping、量化、offset、
固定 filler/reference LLR、prior/CRC 与 early stopping。初始 V2C 消息为 channel LLR，
故乘 `c`。若第 `l` 轮 V2C 均乘 `c`，check update

`CN(m)=0.75 * product(sign(m_j)) * min_j |m_j|`

也乘 `c`；variable update是 channel LLR 与 incoming C2V 的和，也乘 `c`。归纳得
每轮所有消息与 a-posteriori LLR 都乘 `c`，所以非零 hard sign、固定 20 轮输出不变。
`alpha=0.75` 本身是固定乘法，不破坏齐次；`offset=0`；permutation/interleaver、
punctured zero 与 fixed iteration count 也不破坏。

实际可能破坏该结论的 receiver element 只有：

1. demapper preclip `±30`、decoder input/internal `±20` 与 saturation；
2. finite precision / explicit quantization；
3. nonzero OMS offset 或随幅值变化的 normalization；
4. 5G rate recovery 注入的固定幅值 filler LLR（当前绑定 `-llr_max`）；
5. 未共同缩放的 demapper prior、CRC/penalty、state/warm-start 或 syndrome early stop
   （当前 adapter 没有这些）；
6. per-bit/per-symbol/per-frame-within-codeword 非公共 scaling；
7. B3 exact APP 的 shape change——它本来就不是公共 scaling。

### 4.2 B0→O1 的合法 headroom 链

- **B2 ideal chain**：无合法 headroom；fixed NMS hard output严格不变。
- **B2 frozen-interface chain**：只能经 fixed clip/filler/quantization改变 finite decoder
  trajectory。B1 的 runtime scalar 固定，不能解析吸收 frame-adaptive B2；B2 因而相对
  fixed B0/B1 有自然 causal headroom。理论上，若开放 decoder 内部并让同一 pilot statistic
  同步控制 demapper/input/internal clip 与 filler magnitude，公共尺度可重参数化为阈值；
  但这需要修改冻结/黑盒 LDPC 内部，不是相同 frozen receiver interface 下的 B1 或合法
  自动否决。该等价只限制 claim，正性能仍交给 correctness 后的单格 headroom falsifier。
- **B3 max-log chain**：在未裁剪等价条件内与 B2 相同；固定 clip 的作用次序必须在
  correctness 中显式记录，不能用错误 placement 制造差异。
- **B3 exact-APP chain**：`hat N0` 改变 16 个 symbol metrics 的 temperature，再按每个 bit
  partition marginalize；bit LLR shape 可变，因此可在同一 frozen decoder 前形成不同于
  global scalar 的合法 action。B0→O1 headroom 必须在这条链上检查。

### 4.3 吸收关系与唯一 action

| 对手 | 吸收什么 | B3 仍可能留下什么 |
|---|---|---|
| B1 offline fixed scalar | stationary distribution 下的最佳公共 scale、固定 clip operating point | 不能吸收 per-frame drift；仍是最强廉价 stationary 对手 |
| 内部 adaptive clip/filler tuning（解释项，非同接口 baseline） | 若解除黑盒约束并同步重参数化全部阈值/filler，可解释 B2 的公共尺度数值效应 | 需要修改 decoder 内部；用于限制“新变换/新 decoder”claim，不自动否决 frozen-interface B2 |
| B3 max-log plug-in | 未裁剪条件下逐样本逐 bit 复制 B2 | 固定 clip placement 下须作 identity/control；B3 exact APP 另作强 comparator |
| O1/B_match | 给出 true per-frame matched headroom ceiling | 不是 deployable baseline，不用于 Go |

因此 action 选择为 **B2**：冻结/黑盒 LDPC 外部的 current-frame calibration。B3 exact APP
保留为同 pilots/statistic/window、同信息预算的强 comparator/correctness 分叉；不构造
B2+B3 双自由度方法，也不声称 B2 是新变换或不存在内部等价参数化。

### 4.4 当前接口 blocker

本地已有两块必要但尚未接合的接口：

1. `codec_metrics.py` 固定 project APSK constellation/label fingerprint、4-bit
   `positive_means_bit_1` exact-sum LLR；
2. `coded-decoder-feedback/codec.py` 固定 5G BG2 `k=1024,n=1536,Qm=4`、
   3GPP output interleaver、20-iteration NMS。

但当前 `D0Codec.demap()` 仍硬编码 Gray-16QAM，APSK seam 只做过 uncoded
GMI/BER correctness，没有一个 receipt 证明 `encoder coded bits → APSK labels → exact APP
LLR flatten/order → out_int_inv → decoder` 全链一致。该缺口 **不阻止纸面选择 B2**，
但阻止任何 B0→O1 或 coded headroom 执行；它是下一 correctness-only seam 的最小 blocker。

## 5. B：claim ceiling

### 5.1 强邻居的约束

Wu 2013 已覆盖 online/per-block LLR scaling；Shibata 2015、El-Khamy 2014 已覆盖
residual/reliability→variance/LLR；Cao 2015 已覆盖 pilot-aided coherent-optical LLR；
Alvarado/Szczecinski/Martinez/Yoshida 已覆盖 global scaling、GMI 与 coherent-optical
post-processing；Layton 2018 已覆盖 APSK known-pilot per-point likelihood。

这些邻居永久禁止“首次 online/pilot-aided scaling”“新 LLR/GMI 理论”“首次 variance
plug-in”“首次 APSK soft demapping”“SOTA/普适”等 claim。它们没有自动否决不同
DP-(8,8)-16APSK coherent-FSO target chain 上的经典迁移。

### 5.2 B2 形态的最低 claim

只可主张：

> 在共同 DP-(8,8)-16APSK coherent-FSO 接收链中，把 post-Ch4→Ch3 current-frame
> known-pilot residual 约束成一个 block-causal positive scalar，在冻结/黑盒 LDPC
> 外部校准该帧 post-demapper channel/extrinsic LLR 的 target-scene classical migration
> recipe。

不得主张新 LLR 变换、decoder 内部创新或不存在等价的内部阈值参数化；B3 exact APP
必须保留为同信息预算强 comparator。没有 correctness、headroom、coded BER/FER 与
pilot-window 稳定性证据前，RDL claim ceiling 仍为 `CANDIDATE`。

## 6. 冻结 correctness contract（只写不执行）

### C0 — identity、label、sign 与 noise factor

1. fingerprint `common._modulation.m16apsk_mod` 的 16 symbols 与 4-bit labels；冻结
   `b0` 为 ring bit、`b1:b3` 为环内 Gray phase bits，LLR 为
   `L=log P(b=1|y)-log P(b=0|y)`。
2. mapper hard roundtrip 必须 `0` bit errors；在每个 constellation point 的低噪声
   exact APP 中，4 个 LLR sign 必须等于该 label。
3. 冻结 complex noise power `N0=E|n|^2` 与 per-real covariance
   `nu=N0/2`。`codec_metrics.py` 的 `-0.5 delta^T Sigma^-1 delta` 在
   `Sigma=nu I` 时必须化为 `-|y-x|^2/N0`；禁止把 `N0` 与 `nu` 混用。
4. 手算点：`gamma=2.57` 时 `r1^2=0.2629883365`、`r2^2=1.7370116635`。
   在 `y=0`，所有 bits 都给等价控制；ring bit
   `L_b0=-(r2^2-r1^2)/N0`。取 `tilde N0=0.04, hat N0=0.02`，
   B0=`-36.8505832`、`s=2`、B2=B3=`-73.7011664`。该点只验证 sign、factor
   与 identity control，不证明 exact APP 普遍等价。

### C1 — B2/B3 max-log 严格等价

在 uniform weights、无 prior、共同 isotropic variance、固定 means/geometry/labels、
未裁剪下，对所有 deterministic samples、4 bits 与至少两个正 variance，要求

`max_abs(B3_maxlog(hat N0) - (tilde N0/hat N0)*B0_maxlog(tilde N0)) <= 1e-12`

（float64）。任何 pre-scaling clip、per-point variance、prior 或 geometry 更新必须作为
明确 negative control 破坏等价，不能混入主 identity test。

该严格等价只针对未裁剪解析层。目标 B2 按定义位于冻结 demapper 输出之后，因此必须
另记实际 placement receipt：`B0 demapper/fixed preclip → s → frozen LDPC`；B3 则为
`hat N0 plug-in demapper → same fixed preclip → frozen LDPC`。两者遇到固定 clip 后不再由
未裁剪恒等式保证等价，但不得把 placement 差异宣传为新变换。

### C2 — exact-APP 每 bit identity / non-identity

对确定性 sample set（16 constellation points、origin、inner/outer midpoints、axis/off-axis
generic points）和至少三组 `tilde N0 != hat N0`，逐 bit 计算未裁剪 B2 与 B3：

- origin 为四 bit identity control；
- 每 bit 输出 `IDENTITY_ON_GRID` 或 `NONIDENTITY` 及最大差；
- 若某 bit 在 grid 上全恒等，必须再做 partition-factor/symbolic 检查，不能凭多点 subset
  直接宣称非恒等；
- 至少一个 bit 出现稳定非恒等，才允许把 B3 exact APP 称为 distinct strong comparator；
  若全恒等，只关闭该 correctness 分叉，不据此否决 B2。

### C3 — fixed-NMS homogeneity 与非齐次 controls

1. 使用一个不裁剪、无 filler/fixed prior 的最小同构 NMS graph，对正 scales
   `{0.25,0.5,2,4}` 要求 message-by-message `m(cL)=c m(L)`，20 轮 hard output一致。
2. 在目标 decoder 中分别打开 input/internal clipping、固定 filler、float quantization、
   nonzero offset，验证至少一个构造样本可破坏 message homogeneity；若无法破坏，标该项
   `NO_OBSERVED_EFFECT`，不得假定有 headroom。
3. 仅在解释性 decoder clone 中冻结同一 receiver-visible `s`，比较 `D(sL; C)` 与
   `D(L; C/s)`：demapper/input/internal clip 与 filler magnitude 必须全部同步缩放并记录
   hard-output identity。该测试量化理论参数化边界；因其修改黑盒 decoder 内部，不是
   B0/B1/B2/B3 主比较 arm，也不作为 B2 自动否决。
4. `alpha=0.75`、interleaver、punctured zeros、fixed 20 iterations 单独作 negative controls，
   不得错误归为非齐次来源。

### C4 — comparator / causality parity

- B0：同一 mismatched auxiliary parameter，`s=1`；另加 matched/no-mismatch negative
  control，此时 B0=B_match 且任何 calibration 不得改善。
- B1：development-only tuned one global scalar，runtime 固定；明确不声称其可吸收
  per-frame B2。
- B2/B3：完全相同 pilots、demeaning、statistic、count、window 与 decode时点；B2 是
  frozen-interface 候选，B3 exact APP 是同信息预算强 comparator/correctness 分叉。
- 内部 adaptive demapper/input/internal clip + filler magnitude 只在解释性 clone 中审计；
  不得混入冻结/黑盒 LDPC 主比较或被写成 deployable B1。
- B3 exact APP 与 B0 必须共享 geometry/label/prior/clip；唯一差别是 auxiliary `N0`。
- O1 truth 只进 headroom reference/scorer，不进 receiver API。

### C5 — truth firewall 与 lifecycle

receiver API 只收 `z_pilot/x_pilot/known_mask`、frozen constellation/label、B0 auxiliary
parameter 与 causal frame metadata；禁止 true noise/SNR、payload bits/labels、decoder truth、
future samples。突变所有 forbidden truth 时 B0/B2/B3 LLR 与 decode input 必须
byte-identical。

### C6 — paired codec contract

1. 证明 `encoded 1536 bits → Qm=4 groups → APSK labels → LLR flatten → decoder
   out_int_inv` 与 encoder interleaver互逆；all-zero、single-one、walking-label cases 都通过。
2. B0/B1/B2/B3/O1 共用 realization、codeword、pilots、payload、decoder calls、20 iterations、
   clip 与 fresh-state lifecycle；输出全部 finite。
3. tune/evaluation seeds 与 windows disjoint；truth 只在最终 BER/FER scorer 与 O1。
4. receipt 逐 arm 记录 `decoder_calls | configured_iterations | clip incidence |
   filler contract | hard-output hash`，不得用 GMI/ASI 替代 coded结果。

只有 C0–C6 全 PASS，才允许运行下一节单格；任何 P0/P1 未关闭均禁止性能执行。

## 7. correctness 后的单格 occurrence/headroom 设计（不执行）

### 7.1 冻结单格

复用 T066 的现有 target cell，不新增损伤或参数轴：DP-(8,8)-16APSK、2 polarizations、
moderate GG `(alpha=4,beta=1.9)`、15 dB、memoryless static unitary Jones、equal circular
AWGN、plain canonical RDE `mu=1e-3`、per-pol Ch3 DA CPR；PDL/PMD/FIR/IQ 全关。
当前 `64 pilots/pol` 仅作为继承 cell 的可执行档，不宣称 operational minimum。

### 7.2 顺序门

1. **Natural-mismatch gate**：只用 current-frame pilots 得 `hat N0_pilot`；offline scorer
   用 disjoint payload truth 得 `N0_payload/O1 likelihood`。预注册检查方向一致性、误差与
   paired rank correlation。若 pilot statistic 与 held-out reliability 不相关，立即停止。
2. **B0→O1 headroom gate**：相同 exact-APP、target APSK→LDPC interface、clip、20 iterations
   与 paired codewords，只把 B0 fixed parameter 换成 true per-frame matched O1 parameter。
   主判据为 paired FER，其次 BER；95% paired CI 不支持 O1 优于 B0，或 error-event 数不足
   以达到预注册灵敏度，则记 `NO_HEADROOM/INSUFFICIENT_SENSITIVITY` 并停止。
3. 只有前两门均 PASS，才允许同一单格比较 B1、B2 与 B3 exact APP：B2 是唯一候选
   action，B3 是同信息预算强 comparator。B2 对 B1 的 paired FER/BER 没有预注册正
   headroom，或 B3 完全支配 B2，则不进入开发矩阵。
4. 本单格不选择 pilot minimum；pilot-count/window 稳定性须在另行授权、看本单格结果前
   冻结的 falsifier 中处理。

## 8. Blocker、debt 与 terminal

### 最小 blocker

`TARGET_APSK_CODEC_DEMAPPER_INTERFACE_NOT_RECEIPTED`：当前没有把 project APSK exact-APP
LLR 与 5G BG2 encoder interleaver/decoder 接成同一 target receipt。它只允许下一步做
correctness-only seam，不允许直接跑单格 headroom。

### P2 / evidence debt

1. operational pilot minimum/window=`UNKNOWN`；
2. pilot residual 对 held-out payload reliability 的相关性未验证；
3. target decoder 的固定 `alpha=0.75, 20 iterations, llr_max=20` 是当前本地 identity，
   尚非在 APSK target 上充分 tuned 的公平 baseline；
4. exact APP 四个 bits 的 identity/non-identity 尚待 C2；
5. 当前 64-window variance reduction 是本任务对既有 raw 的只读计算，未有独立 reducer
   receipt，因此只用于 A0 现象 ledger，不作 performance claim。

### 唯一 terminal

`PAPER_DIMENSIONS_PASS_B2`

理由：自然 target-chain pilot residual reliability mismatch 有本地 observation 证据；B1
只吸收 stationary scale；理想 fixed NMS 的正齐次性是最强解析 falsifier，但冻结/黑盒
LDPC 实际含 fixed preclip/internal clip/filler，给位于外部的 current-frame B2 留下相对
fixed B0/B1 的自然非齐次 causal headroom。同步 adaptive 内部阈值可作为理论等价解释，
却需修改 decoder 内部，因而只压低 claim、不在同一 frozen interface 下自动否决 B2。
B3 exact APP 保留为同信息预算强 comparator/correctness 分叉。下一合法动作仅为 B2 的
C0–C6 correctness-only seam；正 FER/BER headroom 仍未声称。
