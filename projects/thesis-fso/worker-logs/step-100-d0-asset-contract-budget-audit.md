# Step 100 — D0 资产合同与预算闭合独立审计

> 2026-08-10 | T054 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 证据 worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> 边界：静态只读审计；除本日志外未修改 owner、治理、源码、测试或结果；未 import 项目、pytest、D0、仿真、benchmark、web/search/download、commit 或 push

## 1. Findings first / verdict

```text
FINAL_VERDICT = ASSET_CONTRACT_READY_WITH_CORRECTIONS
BUDGET_CLASS = BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK
>7D_HARD_BLOCKER = NOT_ESTABLISHED
SCIENTIFIC_EXPOSURE_OR_GATE_CHANGE = NO
MISSION_METHOD_DELTA = NONE
```

1. **拟冻结物理路线可闭合，但不是每项都能称为“source 唯一推出”。** `f_G=100 Hz`、effective-combined linewidth、identity SOP、per-pol scalar front end、固定 prefix/pilot 和 named RNG 均可作为当前 12-cell population 的明确实现投影；其中 `f_G=100 Hz` 与 combined-linewidth identity 必须分别标为 `[canonical-project design choice]` 与 `[D0 implementation projection]`，不能冒充论文原值或 `params.py` 的单端语义。
2. **scalar equalizer 路线无真值泄漏，也不必引入 2x2 LS；但原拟文有两个可确定修正。** `RSS/N` 在拟合一个 complex gain 后对 complex noise power 下偏，应改为 `RSS/(N-1)`；common BPS 后若用同一 prefix 同时选全局 `pi/2` state 和估计残差，会有离散 winner-selection 下偏，最小修正是偶数 prefix 样本选 state、奇数样本估计 post-BPS residual。只要 post-BPS residual 严禁回馈 equalizer，链路没有 circular dependency。
3. **step-097 的 `69,360 calls / 1,032,000 CW / 20,640,000 BP iter` 加法正确，但只能叫 logical exposure / nominal method-work ledger，不能叫 unique physical execution。** 它重复计费了 `(M,N)=(2,100)/(3,100)` 的相同 BPS waveform/grid，也没有利用 controlled fixture 中 byte-identical clean sentinel、truth-corrected O1 与 no-jump twin 的 content-addressed cache。
4. **不删任何 seed/cell/tuple/grid/fixture/candidate 后，保守可预注册的 unique execution 上界是 `48,900 logical decoder batches materialized / 704,640 CW / 14,092,800 BP iter`。** raw/logical exposure仍保持 step-097 的全部数量；差额只变成有 source computation ID 的 cache read。该数仍不是 wall-time 预测。
5. **HMM 成本原单位隐藏了一个 dual-pol factor。** `8,344,800` 是“一个统计参数对在一个 dual-pol frame 上汇总一次”的逻辑数；primitive per-pol trajectory evaluations 是 `16,689,600`。按唯一 `N`、clean sentinel 和 controlled COW 缓存后，需 materialize 的 primitive 上界为 `7,027,200`。最终 selected-pair posterior/LLR symbol-state work、BPS convolution、I/O 与 S4 actual work仍未纳入，因此只能判 `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK`，不能从 operation count 推断天数。
6. **step-099 的 IC-02R/03R/06R 与三个 metamorphic 修正应全部进入 owner。** 这不改变 OFC17 baseline 身份、tuple、gate、seed 或 test-time best-of 禁令。

## 2. 审计范围与输入接收

已完整读取 step-094–099、D0 YAML、A0 preflight、adaptive source closure/channel、相关 `params.py` 字段、P08/P08-R/P08-R2 coded assets，以及 common modulation/BPS/equalizer/GG assets。关键 SHA256：

| 输入 | SHA256 |
|---|---|
| D0 YAML owner | `32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936` |
| A0 preflight owner | `63F1D0881FB88CAD4044737091FB0ABAA7AEA27D50B8DEFD48EC6D8C23C3DAF8` |
| step-094 | `F291DD60A57DEB1238FD087F0113E141F2EA2738590E229AB9123EFCE36D5764` |
| step-095 | `8EC3242FF40BE4F905D5376C6F3A2DAEFFBE5543AC1C9119CDDD35951085C700` |
| step-096 | `32218B9CF0C9284362D3B6EFC438DBB23067B7E592E59CDB0FF1A1538E60B107` |
| step-097 | `7DE9CB923FBAE78F377081A3B52E2CA40F2979D5339DCEC76ACE1BCB88DBDAF9` |
| step-098 | `42C6728BADACFE920A10EB3576AA7D4F834E63B32F314235A3DB9543DCB17F3A` |
| step-099 | `CF298FE9FE2A1A38B9913ED5EC40FB8BF161539E12CF8B89ED4FB5972F6A941C` |
| adaptive source closure / channel | `313AC17...0C1EC` / `0D74F642...BEED7` |
| `params.py` | `0E87C53364461478EDDCD81426D8E04646270C3EA7AA717E3C3B28C5DD2A99E9` |
| common modulation / BPS / equalizer / GG | `036FB7AA...94D5` / `AFB8AED9...60E2` / `320115D9...99B9` / `D8E7929D...3113` |
| P08 coded / P08-R / P08-R2 | `7E89D515...F7E9` / `174DAAD2...8404` / `50124850...1430` |

T054 task-control 以 RDL validator 复核为 `PASS`。当前任务在 `CP011` 的 `CONTRACT_STATIC_CHECK` 授权内；没有进入 adapter、MVE、held-out、Contract 或 Execute。

## 3. 拟冻结物理选择逐项裁决

### 3.1 GG 时间尺度

`f_G=100 Hz` **接受，但须改 provenance label**：

- `params.py::GGTimeParams.GREENWOOD_FREQ_DEFAULT=100` 是当前 canonical default，来源范围为 60–1000 Hz，AuditFlag 仍为 WARNING；adaptive local `ChannelParams.f_g=500` 不是 D0 owner。
- 当前 population 只允许 `4 SNR × 3 linewidth=12 cells`，因此不得把 `f_G` 偷增为新轴。
- owner-ready 派生值：

```text
tau_c = 1/(2*pi*100) = 0.0015915494309189533 s
block = 100 symbols
T_s = 4e-10 s
rho_block = exp(-block*T_s/tau_c) = 0.999974867574596
method = gar
field multiplier = sqrt(GG intensity)
```

措辞应为：`selection_role: canonical_project_design_choice_not_paper_unique`。不能写成 source closure 已唯一规定 100 Hz。

### 3.2 linewidth

将 `{10,20,80} kHz` 冻结为 **effective combined phase-process linewidth** 可接受，且与 adaptive channel 的实际“一次代入 `2*pi*Delta_nu*T_s`”路径一致；但它不继承 `params.py::LASER_LW` 的“单端激光器”身份。owner 必须写：

```text
numeric_provenance = adaptive source-closure sweep values
semantic_projection = D0 effective combined residual phase-process linewidth
endpoint_decomposition = not modeled
no_tx_lo_redoubling = true
```

每符号 innovation variance 分别为：

| effective linewidth | `2*pi*Delta_nu_eff*T_s` rad² |
|---:|---:|
| 10 kHz | `2.5132741228718347e-05` |
| 20 kHz | `5.0265482457436690e-05` |
| 80 kHz | `2.0106192982974677e-04` |

初态固定为 symbol 0 前 `theta=-` 的状态值 0，随后先画第一个 innovation，故 `theta[0]=epsilon[0]`；CFO=0；X/Y 共用同一 phase array。

### 3.3 polarization 与 scalar front end

`identity_no_cross_pol_mixing + scalar_per_pol_receiver_front_end` 是当前 population 的最小 source-compatible 出口：

- 不新增 SOP/Jones 轴；X-only 输入不得泄入 Y。
- 不调用 P08-R2 的 2x2 LS；其 same-prefix regressor rank defect不以“换 prefix”修补。
- X/Y 可使用相同 prefix/pilot bytes，但必须分别记录 receipt 和独立 AWGN。

### 3.4 equalizer：bias、非循环方向与最小修正

每 pol 独立执行，`x` 仅为 receiver-known 32-symbol prefix：

```text
g_pre = sum(conj(x_j)*r_j) / sum(|x_j|^2)
RSS_pre = sum(|r_j-g_pre*x_j|^2)
C_pre_cplx = RSS_pre / (32-1)              # 一个 complex LS 参数，修正 RSS/32 下偏

P_rx,b = mean(|r[n]|^2 over absolute-time block b)
h_vis,b = max(P_rx,b-C_pre_cplx, 0)
z_b = r_b*sqrt(h_vis,b)/(h_vis,b+C_pre_cplx)
z_b = amp_limit(z_b, 3)
```

生产路径要求 `C_pre_cplx>0`；noiseless identity fixture 走显式 `C_pre=0,h_vis>0 -> z=r/sqrt(h_vis)` 分支，不加未登记 epsilon。`h_vis` 是 receiver-visible received-signal-power surrogate，不声称为 true `h`。

随后执行 common `bps_cpr(..., mod='qam16')`。BPS 后需要补上原拟文遗漏的 receiver-only 四状态全局 resolve：

```text
k_pre = argmin k in [0,1,2,3] of
        sum_{j even in 0..31}|z_j*exp(-j*k*pi/2)-x_j|^2
tie -> lower k
apply that rotation to the entire polarization waveform
C_post_cplx = mean_{j odd in 0..31}|z_resolved,j-x_j|^2
```

偶数 16 样本选 state、奇数 16 样本估残差，消除“同样本选最优 state 后再报最小 residual”的离散 selection bias；不增加 overhead。`C_post_cplx` 只供 demapper/B2 moment split，**严禁回馈 `h_vis` 或 equalizer**。因此该链是严格单向的 `C_pre -> equalizer -> BPS/resolve -> C_post -> LLR`，没有 circular dependency。B0/B1/B2读取同一 per-pol `C_post_cplx` owner。

### 3.5 prefix / pilot canonical receipt

纯确定性脚本仅使用 NumPy 2.4.3、`hashlib` 和显式算术；没有 import 项目。prefix 生成必须精确写为：

```text
Generator(PCG64(987654321))
  .integers(0,2,size=128,dtype=int64)
  .astype(uint8)
Gray labels = 4*(2*b0+b1)+(2*b2+b3)
symbols = (gray_axis[I] + j*gray_axis[Q])/sqrt(10)
gray_axis = [-3,-1,3,1]
```

canonical float bytes：每个 complex symbol 展为 `[real,imag]`，显式 little-endian IEEE754 float64 (`<f8`)，C-order，再 SHA256。X/Y relation=`identical_by_contract_but_separately_receipted`。

| Prefix artifact | SHA256 |
|---|---|
| 128 bits, uint8 C-order | `1168a4cce1eef1403b4c609f0d2d15541ffd1cdfd175ca809da6701ad81c6d85` |
| 32 labels, uint8 C-order | `31c73fa861c3c9f27bbcb0d8cfcba7fcfccfc59f5e12429946d3720e196616b0` |
| 32 symbols, `[re,im]<f8` | `69989be842342bf388cf2603be0a260f637da876dc912ed74deaed22ff9123c0` |
| even-index 16-symbol resolve subset | `81350b996fcc3f6ef91b05b83957c85b182f4df6bf1e31be48a0f31cca89a4bc` |
| odd-index 16-symbol residual subset | `436cdb61597776f8dc045b0d8465265a3978ca089cdf41f1b50893a86a7e062a` |

前 16 labels 为 `[10,8,10,8,9,1,7,5,3,4,5,11,8,3,6,12]`，用于实现 sanity check；该有限 prefix 的实际平均能量为 `1.025`，不能错误断言样本均值恰为 1。

periodic pilot cycle 固定为 `[(1+j),(1-j),(-1+j),(-1-j)]/sqrt(2)`；同一 canonical float encoding：

| Pilot artifact | count | SHA256 |
|---|---:|---|
| 4-symbol cycle | 4 | `db860e05d78202f159e28f16fbe26c8e060fc8c65c4b872c8bb3f7fc5915071e` |
| expanded `N=10` | 684 | `2c58efb90b9b4a82b676db4e219f21094cc0a546f54c126b1010764fc68375bd` |
| expanded `N=20` | 325 | `1d14610847c0023475cb03ff7a932fddc1202f02c2a7ca4c25d0fb544504af82` |
| expanded `N=100` | 64 | `17bdb8755470902084e9f1331fb6e36633332f9e2392a7d247e061ec1b0a810c` |
| expanded `N=200` | 32 | `0d515c32e1447d3d8b1a55d367b53feacafbee792989697fd4114161ca2357d4` |

### 3.6 RNG

接受一次性 `SeedSequence(root_seed).spawn(6)`，固定顺序：

```text
[payload_x, payload_y, gamma_gamma, wiener, awgn_x, awgn_y]
```

每个 dynamic receipt 至少记录 root entropy、NumPy version、child `spawn_key`、pool size 与 `generate_state(4,uint32)`；各 child 用 `Generator(PCG64(child_seed_sequence))`。paired methods、BPS grid、B2 tuple和 no-jump twin复用已经物化的 arrays；controlled fixture只对 common-BPS output copy-on-write。

### 3.7 B2 数学

step-099 的修正完整接收：

- `C_post_cplx`、`N0_hat_cplx`、`noise_var_real=N0_hat_cplx/2` 必须分名。
- 对候选 `sigma_e2`：`mu=exp(-sigma_e2/2)`，`E_cal=mean|x_odd|^2`，`N0_hat=max(0,C_post_cplx-2*(1-mu)*E_cal)`，`V_x=N0_hat+|x|^2*(1-mu^2)`。
- emission 保留 `-|y-mu*r_s*x|^2/V_x-log(pi*V_x)`；`V_x=0` 走 Dirac branch。
- state 维 exact logsumexp，bit-set 内 P08 max-log；single-state、`sigma_e2=0` 时 preclip 必须逐点等于 P08 `sigma2=N0_hat/2`。错误传 `sigma2=N0_hat` 的 magnitude 恰减半，必须作为 negative control。
- global `pi/2` covariance 不得同时旋转 reference 和移动 state label；uniform-state 只要求 `LLR_b0=LLR_b2=0`、`LLR_b1=LLR_b3`，后两者一般非零。

## 4. cardinality / cost 独立复算

### 4.1 logical exposure（step-097 算术确认）

| Phase | 复算 | batches | CW | BP iter |
|---|---:|---:|---:|---:|
| BPS dev | `10*12*5 tuples*6 grid=3,600 B1 frames`; each `8/128/2560` | 28,800 | 460,800 | 9,216,000 |
| B2 dev | per tuple `10*12*(1 clean+2 pol*9 fixtures)=2,280`; `*5=11,400`; each `2/32/640` | 22,800 | 364,800 | 7,296,000 |
| S2 | B1 `600*128` + B2 `540*32` + O1 `540*32` | 6,960 | 111,360 | 2,227,200 |
| S3 dev | `540*[16+3*(12+8+4)]` | 5,400 | 47,520 | 950,400 |
| S3 test | same | 5,400 | 47,520 | 950,400 |
| **pre-S4 logical total** | exact | **69,360** | **1,032,000** | **20,640,000** |

因此原总数没有加法错误；错误是把它命名为 unique/physical execution。

### 4.2 不改 exposure 的确定性复用边界

1. **BPS duplicate-N cache**：五 tuple 只有四个 `N`；`(2,100)` 与 `(3,100)` 的 waveform、BPS input及 B1 grid完全相同，M不进入 BPS。保持3,600 logical rows，但只 materialize `10*12*4*6=2,880` B1 frames；720 rows为 cache read。
2. **B2 controlled clean-sentinel cache**：每 `seed×cell×tuple`、每 pol只需 `1 clean +9 injected=10` 个 B2 decoder batches；“另一 pol 为 sentinel”的九次重复不得重译码。600 tuple-base 需 `600*20=12,000` batches /192,000 CW。M=2/3 的 N=100 B2 LLR不同，最终 decode不可跨M复用。
3. **S2 COW/cache**：底层只有 `10 seeds*3 cells=30` 个 dual-pol channel realizations。每 base：B1 每pol `4 clean rotations+9*4 injected rotations=40` calls，共80；B2每pol `1 clean+9 injected=10`，共20；O1 truth correction后两pol均回到clean input，共2。合计102 batches/base，即3,060 batches/48,960 CW。O1 cache启用前必须先通过 all-boundary/all-rotation byte identity gate。
4. **S3 不降 frozen work**：每 case 的88 CW 与72 unchanged-CW NLL cache reads保持。不得用跨 candidate/case cache改写47,520；可把多个同 batch-size 的 logical restarts装入一次 vectorized API invocation，但 ledger仍记录原 logical batches/CW/BP。

由此得到保守 unique materialization ledger：

| Phase | materialized batches | materialized CW | BP iter |
|---|---:|---:|---:|
| BPS dev | 23,040 | 368,640 | 7,372,800 |
| B2 dev | 12,000 | 192,000 | 3,840,000 |
| S2 | 3,060 | 48,960 | 979,200 |
| S3 dev+test | 10,800 | 95,040 | 1,900,800 |
| **pre-S4 unique upper bound** | **48,900** | **704,640** | **14,092,800** |

这不是删减科学暴露：raw rows、seed/cell/tuple/grid/fixture/candidate和 nominal per-method complexity 仍全部保留；每个 cache row必须指向一个已执行、hash相同、empty-state fresh-decode 的 `source_computation_id`。

### 4.3 physical realization / method frame / cache read 分层

- BPS+B2 dev共享 `10*12*4 unique N=480` 个 channel/base waveform draws；五 tuple 仍有600 logical tuple views。
- B2 dev有11,400 logical dual-pol method frames，但只是480 bases上的COW clean/controlled views与M-specific processing；不得重画 fade/phase/noise。
- S2有30 channel draws、540 on fixture views、540 aligned off logical projections；不应再称60个 target-pol labels为60个独立 channel draws。
- S3 dev/test各30 channel draws、540 target-pol cases；88 CW/case是冻结 logical target-pol incremental work。
- “decoder batch”必须在 ledger 中定义为 logical `pol-frame×candidate` group；runtime可跨 frame vectorize，但另记 `physical_api_invocations` 与 `batch_cw_count`，不能用少一次 Python call伪造较低方法复杂度。

### 4.4 HMM 单位修正

`p_s grid=122`、`sigma_e2 grid=6`，每 trajectory有732 parameter pairs。

```text
logical dual-pol frame-pair scores = 11,400*732 = 8,344,800
logical primitive pol-trajectory scores = 11,400*2*732 = 16,689,600
unique primitive pol-trajectory scores
  = (10 seeds*12 cells*4 unique N)
    *(2 pol*(1 clean+9 injected))*732
  = 7,027,200
```

owner 应保存 primitive 与 aggregate 两列，禁止只写 `HMM evaluations`。上述仍未计 selected-pair 在6144 data symbols上的 local smoothing、state/bit metrics；这些需 actual ledger和 bounded benchmark。

## 5. step-097 owner patch 处置

step-097 的四 typed tables、PK/nullability、S2 540 aligned off projections、S1 20/50 actual block bootstrap、S3 case→cell→equal-cell macro、PCG64/10,000/linear percentile、raw→summary与atomic artifact协议可接收。写回 owner 时需做以下替换/补充：

1. 将 `unique_dual_pol_waveform_realizations: 600` 改成 `logical_tuple_waveform_views:600` 与 `unique_channel_waveform_realizations:480`。
2. 保留 logical/nominal `pre_S4_decoder_total=69,360/1,032,000/20,640,000`，改名 `logical_exposure_total`；另增 §4.2 的 `unique_materialization_upper_bound`。
3. S2 将 `physical_off_cases:60` 改名为 `target_pol_off_branches:60`；底层 `unique_channel_realizations:30`。540 fixture-aligned projections不变。
4. computation ledger同时拥有 `logical_cost`、`materialized_cost`、`cache_read` 和 `physical_api_invocation`，禁止把 logical row重复计为执行成本，也禁止用实验 fixture cache降低方法的 nominal deployable cost声称。
5. 加入 §3 的 physical realization、prefix/pilot/RNG/equalizer/BPS-resolve/B2修正文；不改任何 scientific threshold/seed/gate。

## 6. 预算裁决

静态材料不能把 decoder/HMM operation count换算成 wall time。当前还缺：

- exact Sionna device/batch-size throughput；
- BPS六格卷积与缓存命中；
- B2 7,027,200 primitive grid-score及selected-pair symbol-state吞吐；
- JSONL/receipt I/O、S4 actual cost和失败重试开销。

因此不能判 `NO_BLOCKER_EVIDENCE` 到“4.50日已闭合”，也不能判 `>7D_HARD_BLOCKER`。在实现与unit gate通过后、任何科学seed前，应运行一个被单独授权的 bounded non-scientific throughput benchmark：覆盖 decoder batch sizes `{4,8,12,16}`、一个 BPS六格 base、一个 B2 `(N,M)` 的10 unique pol views及一个HMM grid chunk；记录cache命中、CPU/GPU、峰值内存与12分钟watchdog。只能据此缩 batch或调整vectorization，不能删 exposure/gate。

最终预算分类：

```text
BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK
NO_NECESSARY_WORK_PROVEN_OVER_7D
```

## 7. owner-ready acceptance checklist

- [ ] `f_G=100` 标 design choice；tau/rho receipt exact。
- [ ] linewidth 标 effective combined projection；不做 Tx/LO doubling。
- [ ] identity SOP；2x2 LS API不可达。
- [ ] prefix/pilot hashes与编码算法 exact；X/Y分别 receipt。
- [ ] scalar LS用 `RSS/31`；post-BPS residual不回馈equalizer。
- [ ] even-prefix global resolve / odd-prefix residual split及四-state tie-break。
- [ ] RNG一次spawn六个named child；paired arrays byte-identical。
- [ ] IC-02R/03R/06R、factor-2 magnitude、Dirac、covariance与uniform-symmetry tests。
- [ ] logical exposure与materialized execution双账；cache source hash/ID完整。
- [ ] HMM dual-pol aggregate与per-pol primitive单位同时记录。
- [ ] benchmark只在未来授权后运行；本审计未运行。

## 8. Protection / terminal receipt

- owner初始 SHA：D0 YAML=`32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936`；A0 preflight=`63F1D0881FB88CAD4044737091FB0ABAA7AEA27D50B8DEFD48EC6D8C23C3DAF8`。
- 本任务启动 staging为空；目标文件启动时不存在。
- protected p05启动 SHA256：
  - `p05_run.log`=`7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log`=`735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log`=`C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log`=`95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
- 唯一预期写入：`projects/thesis-fso/worker-logs/step-100-d0-asset-contract-budget-audit.md`。
- 末次复核：两份 owner SHA 与启动值逐字节相同；p05=`4/4 MATCH`；staging仍为空；目标文件为唯一新建的本任务文件。
- 本日志末次复核前 SHA256=`140D8DD118C597D6057E2F0C5BCC035DBFE686BB15FD512CD7860D7BED0FE0ED`（加入本行后文件自身 hash 必然变化，故该值仅作 pre-terminal self-receipt，不作为递归不变量）。

```text
TERMINAL = ASSET_CONTRACT_READY_WITH_CORRECTIONS
```
