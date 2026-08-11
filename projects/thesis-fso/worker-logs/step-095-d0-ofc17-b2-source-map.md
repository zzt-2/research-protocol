# Step 095 — D0 OFC2017 B2 source-native / 16QAM 迁移映射

> 2026-08-10 | T049 / CP011 / `SOURCE_AUDIT`  
> 只读输入：本地 OFC2017 全文、D0 YAML、A0 preflight、step-081、P08 constellation/demapper、BPS/相位模糊公式与参数来源字段  
> 未执行：web/search/download、import probe、pytest、D0、仿真、源码修改、合同修改

## 1. Findings first 与裁决

1. **五个 `(M,N)` tuple 是 source-exact，四个 pilot count 与冻结公式内部一致。** 原文给 `(2,100)` 以及 `(3,10)/(3,20)/(3,100)/(3,200)`；合同的 `684/325/64/32` 均等于 `1+ceil(6144/(N-1))`。
2. **原文足以固定 4-state Markov 核心，但不足以单独唯一复刻 B2。** 原文明确 QPSK、fourth-power CPE、`L=31`、`p_s`、`sigma_e^2`、`q=1-sqrt(1-p_s)`、Toeplitz transition、`M` nearest pilots、parallel LLR refinement、no decision feedback；它没有给 terminal pilot、no-puncture extended frame、16QAM demapper、`p_s/sigma_e2` 拟合网格或多 pilot 证据合并的完整伪代码。
3. **冻结合同已经合法外推到 16QAM/FSO/dual-pol，并给出了足以收口的约束；仍需命名 8 个实现选择。** 本文将这些选择冻结为 `IC-01`–`IC-08`，都位于 source-explicit B2 adaptation 内，不改变 baseline 身份、信息边界、tuple 集或测试时 best-of 禁令。
4. **没有 hard blocker。** 不需要 source-native QPSK receiver 重建、custom decoder/CRC、合同重开或删除 gate；所需工作可装入已冻结的 B2 adaptation `2.00 d`。这不是工期已实测，只是没有发现必然超预算的必要工项。

```text
VERDICT       = SOURCE_READY_WITH_NAMED_IMPLEMENTATION_CHOICES
HARD_BLOCKER  = NO
CONTRACT_REOPEN_REQUIRED = NO
```

不判 `SOURCE_READY`，因为原文没有唯一规定多 pilot 的联合方式、16QAM 半径相关 residual-phase variance、log-MAP/max-log 选择与 HMM 初始先验。不判 `>7D_HARD_BLOCKER`，因为这些缺口均能以 4-state、`M<=3` 的小状态实现与确定性单测闭合。

## 2. 本地全文 receipt 与逐项原文证据

### 2.1 Receipt

- 全文：`papers/doi/10.1364_ofc.2017.w2a.56/7937400.md`，136 行 / 14,758 bytes，已从第 1 行完整读至第 136 行。
- Markdown SHA256：`190F9884CB626190F0850D4A38CBBA27EBC7B4C5E6081BDA1CB9AC883C69B403`。
- PDF SHA256：`B5602E048B5197394CA6A63E4762E7DF8996508AFAD4934F009C4F9B7CDA2178`。
- `7937400.meta.json`：expected/real title 均为 *Fully-Parallel Soft-Decision Cycle Slip Recovery*，`title_check=match`、`title_overlap=1.0`。
- step-081 的两项 SHA、3 页 PDF identity 与本次 fresh hash 一致。

### 2.2 精确证据表

| 必答事实 | 原文证据 | 精确上限 |
|---|---|---|
| `L=31` | `7937400.md:27-31`：研究 QPSK fourth-power CPE、窗口 `2L+1`；Fig.2 用 `L=31`，并明确把 `L=31` 作为 practical focus。`7937400.md:47`、`:113`、`:127` 再次固定性能图设置。 | `L` 是 source QPSK fourth-power CPE 半窗，不是合同 square-16QAM BPS 的 `Nw`；不得把二者等同。 |
| `p_s` | `:27-29`：blind CPE 的 slip probability/statistical information；低 SNR 可有 `p_s>=1e-4`。`:43`：Markov slip rate 参数。 | 原文没有规定本项目如何从 dev pilots 拟合 `p_s`。 |
| `sigma_e^2` | `:27-29`：blind CPE residual phase-estimation MSE/variance。`:41`：`theta_n~N(0,sigma_e^2)`、`mu=exp(-sigma_e^2/2)` 及 moment matching。 | 不等于 Wiener innovation `sigma_p^2`；后者是物理 phase process variance。 |
| signal/state model | `:41`：`y_n=x_n exp(j(theta_n+pi s_n/2))+w_n`，`s_n` 是 CPE ambiguity slip state。 | 原文 modulation 是 QPSK。 |
| `q` 与 4-state transition | `:43`：`q=1-sqrt(1-p_s)`；`T[q]=Toeplitz[(1-q)^2,q(1-q),q^2,q(1-q)]`。 | 原文给核与 closed-form power，但没有代码索引顺序；本报告在 IC-01 固定。 |
| distance propagation | `:43`：用 `T^m`；`T^m[q]=T[q']`，`q'=(1-(1-2q)^m)/2 ~= mq`。 | `m` 是 symbol separation；合同 extended waveform 必须用插 pilot 后的真实时间距离。 |
| `M` nearest pilots | `:43`：用 `M` nearest pilots 的 soft state probability，并以 transition power 加权；fully parallel。 | 原文未给联合多个 pilot 的完整公式；IC-05 固定 local HMM smoothing。 |
| source tuples | `:47`：two adjacent pilots `M=2`、`N=100`。`:131`：Fig.6 用 `M=3`，`N={10,20,100,200}`。 | 合同五 tuple 与原文完全对应。 |
| pilot placement | Fig.4 OCR `:119-123`：`1-symbol pilot + (N-1)-symbol data = N-symbol interval`。 | 原文未声明 terminal pilot、partial tail、prefix 或 no-puncture；这些均为合同外推。 |
| one-way FEC | Fig.1 OCR `:103-109`：demodulator/pilot-aided LLR modifier 后接 forward-error decoder。`:43`：明确 no decision feedback / no sequential update。 | 原文不提供 dual-pol 下的函数调用数；合同固定每 method frame 两个 pol-batch calls、每 call 16 CW。 |
| residual-phase LLR handling | `:41`：`exp(j theta)` 以 `CN(mu,1-mu^2)` moment match，source QPSK demodulator LLR 先缩放。 | 16QAM Gaussian-mixture 是合同外推，不移植原文 GMI/dB。 |

## 3. Tuple、pilot count 与 extended-frame 精确索引

令 prefix 长度 `P=32`，coded data 数 `D=6144`。对任一 source tuple 的 `N`：

```text
K_N = ceil(D/(N-1))                   # data block 数
pilot_count = K_N + 1                 # 每块前导 pilot + terminal pilot
d_j = min(j*(N-1), D), j=0,...,K_N
t_pilot(j) = P + d_j + j              # extended-frame 0-based 时间索引
t_data(m) = P + 1 + m + floor(m/(N-1)), m=0,...,D-1
frame_length = P + D + K_N + 1
last_index = P + D + K_N
```

- prefix 占 `t=0..31`；它不是 periodic-pilot count 的一部分。
- `pilot(0)` 在 `t=32`，之后每个完整 interval 是 `pilot + N-1 data`。
- `pilot(K_N)` 是 terminal pilot，位于最后一个 data 之后；当尾块不满 `N-1` 时，最后一个 pilot 间距小于 `N`，不得填 dummy data、不得 puncture/replace coded symbols。
- 所有 state-transition distance 都用上述 extended-frame `t` 的绝对差；不能用 payload-only `m`。

| `N` | `K_N=ceil(6144/(N-1))` | pilots `K_N+1` | 总 frame length（含 32 prefix） | terminal index |
|---:|---:|---:|---:|---:|
| 10 | 683 | 684 | 6860 | 6859 |
| 20 | 324 | 325 | 6501 | 6500 |
| 100 | 63 | 64 | 6240 | 6239 |
| 200 | 31 | 32 | 6208 | 6207 |

因此合同 `pilot_count_formula` 与 `684/325/64/32` 全部一致。`M` 不改变 waveform 或 pilot count；它只改变每个 data symbol 消费的 nearest-pilot 数量。等距时先选 earlier pilot，再按时间排序进入 HMM。

## 4. 可直接编码的数学定义

### 4.1 四状态与 transition（`[原文]` + IC-01）

定义 state rotation

```text
r_s = exp(j*pi*s/2),  s in {0,1,2,3}
```

`[实现选择 IC-01]` 固定 `s` 增大对应正向 `+pi/2`，与原文 `y=x exp(j(theta+pi*s/2))+w` 同号；likelihood 中不先旋转 observation，而用 mean `r_s*x`，避免双重取反。

令

```text
q = 1 - sqrt(1-p_s)
a = (1-q)^2 = 1-p_s
b = q(1-q)
c = q^2

T = [[a,b,c,b],
     [b,a,b,c],
     [c,b,a,b],
     [b,c,b,a]]
```

其中 `T[u,v]=Pr(S_{n+1}=v | S_n=u)`。每行和为 1；总 change probability 为 `2b+c=p_s`。距离 `d>=1`：

```text
q_d = (1-(1-2q)^d)/2
T^d = T(q_d)
T^0 = I_4
```

实际代码可用 closed form 或 `matrix_power`，两者必须数值相等。`p_s=0 -> q=0 -> T=I`；log-domain 中零 transition 记 `-inf`，不得加会制造假 slip 的 epsilon。

### 4.2 Known-pilot emission 与 dev statistic fit（`[合同外推]` + IC-02/03/04）

P08 使用 normalized Gray square-16QAM：I/Q axis `[-3,-1,3,1]/sqrt(10)`，bit 顺序 `[b0,b1,b2,b3]`；证据为 `p08_coded_chain.py:44-72`。令 receiver 估计的每实维 AWGN variance 为 `nu>0`，则 complex AWGN variance 为 `2nu`。

对 known pilot `x_j`、observation `y_j`、candidate state `s`：

```text
mu = exp(-sigma_e2/2)
v_j = 2*nu + |x_j|^2*(1-mu^2)
e_j(s) = -|y_j-mu*r_s*x_j|^2/v_j - log(pi*v_j)
```

- `[原文]` `mu` 与 circular complex moment match 来自全文 `:41`。
- `[合同外推]` known-pilot Gaussian likelihood、joint dev grid 与 receiver-only noise estimate 来自 YAML `:144-155`。
- `[实现选择 IC-02]` 固定 `nu` 为 P08 的**每实维** variance，故 complex density 用 `2nu`；禁止把 P08 的 `sigma2` 再当 complex variance而差 2 倍。
- `[实现选择 IC-03]` 对 16QAM 使用 symbol-energy-dependent `|x|^2(1-mu^2)`，而不是把 QPSK 单位模残差常数化；这是对 source moment match 的直接 square-16QAM 延拓。
- `[实现选择 IC-04]` HMM 初始 state prior 固定 uniform `log pi_0(s)=-log 4`。拟合 `(p_s,sigma_e2)` 时，对每条 dev pilot trajectory 跑全 pilot forward likelihood；先除以该 trajectory 的 pilot 数，再对 X/Y 与 12 population cells 等权 macro 平均。按 YAML grid 最大化，tie 依次选较小 `p_s`、较小 `sigma_e2`。test 不重拟合。

全 pilot forward recursion：

```text
alpha_0(s) = -log(4) + e_0(s)
alpha_j(s) = e_j(s) + logsumexp_u(alpha_{j-1}(u) + log T^{Delta_j}[u,s])
logL = logsumexp_s alpha_last(s)
```

`Delta_j=t_pilot(j)-t_pilot(j-1)`，含 extended symbol-time。

### 4.3 `M` nearest-pilot posterior（`[原文]` + `[合同外推]` + IC-05）

对 data time `t`，按 `(abs(t-t_pilot), t_pilot)` 排序取前 `M` 个 pilot；等距 earlier 优先。`[实现选择 IC-05]` 将这些 pilot 与 latent node `S_t` 按时间组成一个 local 4-state chain，使用相邻节点真实距离的 `T^Delta`，只在 selected pilots 加 emission，uniform prior 后做 log-domain forward-backward；输出

```text
log_pi_t(s) = log Pr(S_t=s | selected M pilot observations)
log_pi_t <- log_pi_t - logsumexp_s(log_pi_t)
```

这一定义：

- 不把重叠 transition path 当独立 evidence 重复相乘；
- `M=2` 时就是左右/边缘最近两 pilot 的 local smoothing；
- `M=3` 时允许 2-left/1-right 或 1-left/2-right；
- 每个 data symbol 可独立计算，保留原文 fully-parallel/no sequential decision-update 身份；
- 不使用 decoder output、payload truth 或 test-time refit。

### 4.4 Square-16QAM four-state mixture LLR（`[合同外推]` + IC-06/07）

令 `X_{k,b}` 为 P08 constellation 中第 `k` bit 等于 `b` 的 8 个点。对 data observation `y_t`：

```text
v_x = 2*nu + |x|^2*(1-mu^2)
g(t,s,x) = -|y_t-mu*r_s*x|^2/v_x - log(pi*v_x)

A_{k,b}(t) = logsumexp_{s in 0..3, x in X_{k,b}}(
                 log_pi_t(s) + g(t,s,x))

LLR_{t,k} = A_{k,1}(t) - A_{k,0}(t)
```

- `[实现选择 IC-06]` 使用 exact log-sum-exp Gaussian mixture，不在 bit-set 内做 max-log。四 state 与 constellation symbol prior 均匀，其常数在 ratio 中抵消。
- `[实现选择 IC-07]` sign 固定为 `log P(bit=1|y)-log P(bit=0|y)`；这与 P08 `p08_coded_chain.py:83-106` 的 `min_zero-min_one` sign 相同，`LLR>=0` 表示 bit 1 更可能。bit order 固定 `[b0,b1,b2,b3]`。
- 输出先 clip 到 `[-30,30]`，送 decoder 前再 clamp 到 `[-20,20]`，对应 YAML `:156-159` 与 P08 `:123-126/:217-226`。
- 当 posterior collapse 到单 state 时，它退化为该 rotation 下的 exact log-MAP 16QAM demapper；P08 是 max-log，因此只要求 sign/bit order/hard decision 一致，不错误要求所有 finite-SNR LLR 数值逐点相等。

### 4.5 One-way decode（`[原文]` + `[合同外推]` + IC-08）

`[原文]` pilot soft state 只修改 demodulator LLR，之后 forward-error decoder 单向消费；no decision feedback/no sequential update（全文 `:43`、Fig.1 `:103-109`）。

`[实现选择 IC-08]` 合同中的 `calls_per_method_frame=2` 解释为 dual-pol 每个 polarization 一个 batched decoder call，每 call 含 16 CW、每 CW 固定 20 iter；不是每 CW 单独 16 次 API call，也不是先 decode 再回馈 HMM。两次调用开始时均为空 decoder state，B2 输出只包含 refined LLR 与一次下游 decode 结果。

## 5. Provenance ledger：原文 / 合同外推 / 实现选择

### 5.1 `[原文]`

1. QPSK fourth-power blind CPE，窗口 `2L+1`，重点 `L=31`。
2. CPE 后模型 `y=x exp(j(theta+pi*s/2))+w`，4 个 ambiguity states。
3. `p_s` 是 slip rate；`sigma_e2` 是 residual phase variance/MSE；`mu=exp(-sigma_e2/2)`。
4. `q=1-sqrt(1-p_s)`、Toeplitz `T`、`T^m=T(q_m)`。
5. `M` nearest pilots、parallel LLR refinement。
6. `(2,100)`、`(3,10)`、`(3,20)`、`(3,100)`、`(3,200)`。
7. 一个 N-symbol interval 是 1 pilot + `N-1` data。
8. one-way FEC、no decision feedback、no sequential update。

### 5.2 `[合同外推]`

1. common front end 从 QPSK fourth-power CPE 改为 dev-frozen square-16QAM BPS；`L=31` 不移植成 BPS `Nw`。
2. optical-fiber AWGN/Wiener slice 改为 factorized coherent-FSO population；不声称 turbulence 导致 slip。
3. square-16QAM Gray constellation/bit mixture LLR。
4. dual-pol shared physical process 后独立 CPR/B2/decode。
5. 32-symbol prefix、6144 coded data、extended frame、terminal pilot、no replace/no puncture。
6. `p_s/sigma_e2` dev grid、population-wide freeze、test 禁止 refit。
7. 五 tuple dev 选一、macro net-goodput objective 与 deterministic tie-break；test-time best-of 禁止。
8. B0/B1/B2/O1 共享 extended waveform、pilot mask、payload、phase/noise 与 symbol-time support；B0/B1 不消费 posterior。
9. clip 30、decoder clamp 20、每 frame 两个 pol-batch decode calls。

### 5.3 `[实现选择]`

1. `IC-01` state label 正号与 transition 行/列约定。
2. `IC-02` P08 per-real variance 到 complex Gaussian density 的 2 倍换算。
3. `IC-03` 16QAM symbol-energy-dependent moment variance。
4. `IC-04` uniform HMM prior 与 dev likelihood 的 per-pilot/cell macro normalization。
5. `IC-05` nearest-pilot local HMM smoothing，不做独立证据重复相乘。
6. `IC-06` exact log-sum-exp mixture，不做 inner max-log。
7. `IC-07` P08-compatible positive-for-bit-1 sign 与 bit order。
8. `IC-08` dual-pol batched one-way decode call semantics。

这些选择必须进入实现 docstring/config receipt；改变任一选择要使 source-receipt test 失败并显式审查，但不需要现在重开 D010 数值合同。

## 6. B2 单测、identity、metamorphic 与 source-receipt 清单

### 6.1 Deterministic unit tests

- [ ] **Constellation identity**：16 points 与 P08 `_CONST` byte/value-identical；bits table 与 `[b0,b1,b2,b3]` 一致；平均功率 1。
- [ ] **Transition**：所有 grid `p_s` 下 `T>=0`、row sum=1、symmetric/circulant；`T^d` 与 `T(q_d)` 一致。
- [ ] **`p_s=0`**：`q=0`、`T=I`、不同 state transition log-prob 为 `-inf`；posterior/LLR finite，不制造状态切换。
- [ ] **`sigma_e2=0`**：`mu=1`、residual term 为 0，pilot/data emission 退化为普通 AWGN likelihood；在 `nu>0` 下无 NaN/Inf。
- [ ] **Pilot schedule**：对四个 N 精确得到 `684/325/64/32`、terminal indices `6859/6500/6239/6207`；6144 data 恰好各出现一次，prefix/data 无 replace/puncture。
- [ ] **Nearest-pilot tie**：等距时 earlier pilot 优先；选择数严格为 M；transition distance 使用 extended time。
- [ ] **Log normalization**：极端 likelihood 与 `p_s=0` 下 `logsumexp(log_pi)=0`，posterior sum=1，无 epsilon slip。
- [ ] **Grid freeze**：同一 dev receipt 重跑得到唯一 `(p_s,sigma_e2)`；tie-break 小 `p_s` 后小 `sigma_e2`；test path 无 fit API。
- [ ] **Clip/clamp**：B2 output `|LLR|<=30`，decoder input `|LLR|<=20`。

### 6.2 Identity / metamorphic tests

- [ ] **State permutation**：同步置换 state labels、T 行列、rotation/emission 后，posterior 只作同置换，marginalized LLR 完全不变。
- [ ] **Global `pi/2` covariance**：observation/pilots 同乘 `exp(jk*pi/2)` 且 state labels cyclic shift，最终 data LLR 不变。
- [ ] **Single-state collapse**：`pi_t=delta_s` 时，B2 LLR 等于 rotation-conditioned exact log-MAP 16QAM reference；hard decisions/sign 与 P08 max-log demapper一致。
- [ ] **Uniform-state symmetry null**：`pi_t=1/4` 时 square-16QAM `pi/2` group symmetry 不产生虚假 bit preference；这是 analytic null，不是 D0 acceptance score。
- [ ] **Noiseless known pilots**：对四 states，正确 state emission 最大；state-label/sign 错一位必须被检出。
- [ ] **Terminal bracketing**：最后一个 data 始终有右侧 terminal pilot；删除 terminal pilot 必须使 receipt test 失败。
- [ ] **Payload preservation**：strip prefix/pilots 后逐样本恢复原 6144 data，且 CW/symbol ownership 不变。

### 6.3 No-feedback / one-decode tests

- [ ] HMM/LLR 调用图中没有 decoder output、hard decision、syndrome、CRC 或 final correctness 输入。
- [ ] 每 method frame 精确两个 decoder API calls（X/Y 各一），每 call batch shape 16 CW；总 32 CW decodes、每 CW 20 iterations。
- [ ] 两 call 均从 empty state 开始；禁止 state reuse、redecode、candidate best-of 或 callback。
- [ ] 改变 decoder output 的 test double 不得改变已经冻结的 posterior/LLR。

### 6.4 Source receipt tests

- [ ] 校验全文/PDF SHA256 与 §2.1 完全一致、title match、DOI `10.1364/OFC.2017.W2A.56`。
- [ ] 静态 receipt 包含原文行号 `27-31,41,43,47,119-123,127,131`，并断言五 tuple。
- [ ] receipt 显式存 `IC-01`–`IC-08`、pilot-index 公式、P08 constellation/sign source lines。
- [ ] source hash、合同 tuple/pilot count、P08 constellation/sign 任一变化均 fail closed；不得静默重拟合或换算法。

## 7. Budget 与 blocker 终审

必要实现仍是 4 states、最多 3 pilots、16-point constellation 的确定性小状态计算：schedule/index、HMM/grid fit、mixture LLR、dev freeze 与 tests。它不需要：

- 重建原文 fourth-power QPSK CPE 或复刻原文 GMI；
- custom/unpruned decoder、CRC、decoder callback/message state；
- test-time tuple/statistic best-of；
- C1 trigger/local action/fallback；
- web acquisition或新增 source。

因此没有触发 YAML `blocker_if` 的任一项。`2.00 d` 仍是可辩护的 point estimate；真正实施若发现必须偏离 IC-01–IC-08、需要 source-native reproduction、或必要工作将消耗超出 7.00 d 总 contingency，届时才升级为 named hard blocker，不得删 gate 挤预算。

```text
FINAL_VERDICT = SOURCE_READY_WITH_NAMED_IMPLEMENTATION_CHOICES
HARD_BLOCKER  = NO
```
