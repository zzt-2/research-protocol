# Step 099 — D0 B2 IC-01–IC-08 数学与 P08 约定窄审

> 2026-08-10 | T053 / CP011 / `CONTRACT_STATIC_CHECK`  
> 只读完成：step-095、冻结 D0 YAML、OFC 2017 本地全文、P08 constellation/demapper、prefix `sigma2` estimator。  
> 未执行：import、pytest、D0、仿真、web/search/download；未修改 owner、源码、治理或 p05。

## 1. Findings first 与裁决

1. **四状态 Markov 核、距离幂、pilot emission、local HMM smoothing、positive-for-bit-1 LLR 方向均可闭合。** `q=1-sqrt(1-p_s)` 确实使一步状态改变概率等于 `p_s`；`T^d=T(q_d)` 的 closed form 也正确。IC-01、IC-04、IC-05、IC-07、IC-08 可原样接收。
2. **IC-02 对 P08 `sigma2` 的解读与源码不一致，现有命名会造成精确 2 倍尺度错误。** P08 demapper 的 `/ (2*sigma2)` 要求传入每个实分量的方差；但 `estimate_sigma2_from_prefix()` 返回 `mean|resid|^2`，是复残差功率。step-095 把该返回值直接称为 per-real `nu` 不成立。此问题可用唯一变量名、`1/2` 映射及 magnitude identity test 消除，不需要改源论文 baseline 身份。
3. **IC-06 的 exact inner log-sum-exp 与“single-state hard decision 必须和 P08 max-log 一致”不能同时逐点成立。** 对 Gray 16QAM 幅度位，finite-noise exact bit-MAP 的零点偏离 max-log 最近邻边界。必须把 IC-06 改为“state 维 exact marginalization + 每个 state/bit-set 内 P08 max-log”；否则现有 single-state receipt 是假断言。
4. **两个 metamorphic 预期需要收窄。** global `pi/2` covariance 当前把“旋转 reference”与“平移 state label”叠加，属于双重变换；uniform-state 也不会令 16QAM 四个 bit LLR 全部为零，半径仍携带两个幅度位的信息。
5. **所有修正均为静态公式与 identity receipt 修正。** 不引入 truth、decoder feedback、test refit、额外 decode 或 source-native QPSK 重建；未触发 D0 `blocker_if`，也没有 7 日预算 blocker。

```text
VERDICT = IC_SET_ACCEPTED_WITH_CORRECTIONS
REQUIRED_REPLACEMENTS = IC-02R, IC-03R, IC-06R, MT-02R, MT-04R
SOURCE_IDENTITY_CHANGED = NO
TRUTH_OR_DECODER_FEEDBACK_INTRODUCED = NO
HARD_BLOCKER = NO
```

这里不判 `IC_SET_ACCEPTED`，因为 factor-2 与 exact-vs-max-log 两项会让错误实现通过现有 sign-only receipt；不判 `B2_MATH_CONTRACT_AMBIGUITY`，因为下述公式给出了单一、可测试的消歧路径。

## 2. 独立复算

### 2.1 IC-01：四状态核与距离幂 — PASS

令 `r_s=exp(j*pi*s/2)`，`s=0,1,2,3`，并令

```text
q = 1-sqrt(1-p_s)
a = (1-q)^2
b = q(1-q)
c = q^2
T = [[a,b,c,b],
     [b,a,b,c],
     [c,b,a,b],
     [b,c,b,a]]
```

则每行和为 `(1-q+q)^2=1`，一步改变状态的概率为

```text
2b+c = 2q-q^2 = 1-(1-q)^2 = p_s.
```

该 circulant 矩阵的特征值为

```text
[1, 1-2q, (1-2q)^2, 1-2q].
```

因此对任意整数 `d>=0`，若

```text
q_d = (1-(1-2q)^d)/2,
```

则 `T(q)^d=T(q_d)`；`d=0` 时 `q_d=0`、`T(0)=I_4`。transition distance 使用插入 prefix/pilot 后的 extended symbol-time 差值是正确的。

state sign 也自洽：模型 `y=exp(j*pi*s/2)x exp(j theta)+w` 下，emission mean 应写成 `mu*r_s*x`；若改为预旋 `y`，只能用 `r_s^* y`，二者只能选一种。

### 2.2 IC-02/03：complex/per-real 与 moment match — 必须替换

P08 三处源码事实不能混称为一个 `sigma2`：

- `p08_coded_chain.py:83-105` 使用 `distance/(2*sigma2)`，故该形参的数学身份是 `noise_var_real`；
- `p08r_chain.py:205-216` 返回 `mean(abs(rx_prefix-tx_prefix)^2)`，其身份是 `prefix_residual_power_cplx`；
- 原始 channel 在每个实/虚分量上乘 `sqrt(nv)`，所以 `E|w|^2=2*nv`。旧注释把 `nv` 称作 complex variance 不改变这一定义。

禁止在 B2 receipt 中继续使用裸名 `sigma2`。最低限度必须冻结：

```text
prefix_residual_power_cplx
    := mean_j |y_pre,j - r_s_pre,j*x_pre,j|^2

noise_power_cplx := E|w|^2
noise_var_real   := noise_power_cplx/2
```

其中 prefix residual 必须先处于同一 receiver-visible state convention；`s_pre` 只能来自 known prefix/pilot，不得来自 truth。若 prefix residual 被用来同时承载 residual phase，则不能再把它原样当 AWGN 后重复加 phase variance。对候选 `sigma_e2` 的唯一 moment-consistent split 为

```text
mu      = exp(-sigma_e2/2)
E_pre   = mean_j |x_pre,j|^2
C_pre   = prefix_residual_power_cplx
N0_hat  = max(0, C_pre - 2*(1-mu)*E_pre)
V_x     = N0_hat + |x|^2*(1-mu^2)
```

依据是

```text
E|x(exp(j theta)-1)+w|^2 = 2|x|^2(1-mu) + E|w|^2,
E|x(exp(j theta)-mu)+w|^2 = |x|^2(1-mu^2) + E|w|^2.
```

于是 known-pilot emission 与 data symbol metric 统一为

```text
ell(y;s,x) = -|y-mu*r_s*x|^2/V_x - log(pi*V_x).
```

这保留 IC-03 的 16QAM energy dependence；`-log(V_x)` 不能删，因为 `V_x` 随 `|x|^2` 变化。若实现能从独立 calibration 明确得到纯 AWGN `N0_hat`，则可直接使用该值并跳过上面的 subtraction，但 receipt 必须二选一固定，不能把 `C_pre` 和 `N0_hat` 当同一变量。

`V_x=0` 的 noiseless fixture 是退化 Dirac 情形，不能代入 Gaussian 除法。receipt 应定义：匹配 mean 的候选 log-weight 为 `0`，不匹配者为 `-inf`，随后照常归一化/clip；生产 likelihood 则要求 `V_x>0`。不得用未登记的 epsilon 同时污染 `p_s=0` transition。

### 2.3 IC-04/05：uniform prior 与 nearest-pilot local smoothing — PASS

`T` 是 doubly stochastic，uniform prior 是其 stationary prior。把选中的 `M` 个 pilot node 与 query node `S_t` 按真实时间排序，在相邻 node 间只放一次 `T^Delta`，只在 pilot node 放 emission，再做 forward-backward，确实得到

```text
Pr(S_t=s | selected M pilot observations).
```

该构造不会把重叠 transition path 当成独立证据重复相乘，也不消费 payload truth、decoder output 或 test-time fit。边缘处 `M=3` 出现 `2-left/1-right` 或 `1-left/2-right` 合法；uniform earliest-node prior 与全局 stationary chain 一致。

`p_s=0` 时 `T^Delta=I`：所有 selected pilots 只能支持同一个恒定 state path，posterior 正比于各 pilot emission 在该 state 上的乘积。只要 `V_x>0`，四条恒定路径至少具有有限 likelihood，posterior/LLR 有限；off-diagonal 必须保持 `-inf`，不能加 slip epsilon。

### 2.4 IC-06/07：LLR sign 正确，但 inner mixture 必须改为 P08 max-log

step-095 的 sign 本身正确：

```text
LLR_k = log P(bit_k=1 | y) - log P(bit_k=0 | y),
LLR_k >= 0  => hard bit 1.
```

P08 的 `min_zero-min_one` 正是上述 positive-for-bit-1 convention。然而，step-095 的 exact symbol log-sum 与 P08 max-log 不保证同一 hard bit。反例取 single state、`mu=1`，考察 I 轴幅度位 `b1`，令归一化前实部为 `2`：

```text
P(b1=1) ∝ exp(-1/(10V)) + exp(-9/(10V))
P(b1=0) ∝ exp(-1/(10V)) + exp(-25/(10V)).
```

任意有限 `V>0` 下 exact LLR 严格为正，而 max-log 在该点为零；在 `2` 的右侧足够小邻域内，exact 仍为正而 max-log 已为负。因此“数值可不同但 hard decision/sign 始终相同”是错误断言。

为满足 T053 的 single-state P08 identity，IC-06 必须替换为：

```text
h_{k,b}(t,s) = max_{x in X_{k,b}} ell(y_t;s,x)

A_{k,b}(t) = logsumexp_s(
                 log_pi_t(s) + h_{k,b}(t,s))

LLR_{t,k} = A_{k,1}(t) - A_{k,0}(t).
```

即 state 维仍做 exact probability marginalization，16QAM 每个 state/bit-set 内沿用 P08 max-log。此时若 `pi_t=delta_s`、`mu=1`、`V_x=N0_hat` 为常数，则

```text
LLR_{t,k}
 = [min_{x in X_{k,0}} |y-r_s*x|^2
    - min_{x in X_{k,1}} |y-r_s*x|^2] / N0_hat
 = P08_maxlog(y*r_s^*, sigma2=N0_hat/2),
```

在 clip 前逐点数值相等，因而 bit order、sign 与 hard decision 全部相等。若坚持 exact inner log-sum，则必须放弃“逐点 P08 hard identity”，不能同时保留两个契约。

### 2.5 IC-08：one-way decode — PASS

`calls_per_method_frame=2` 解释为 X/Y 各一次 batch call，每 call 16 CW、每 CW 20 iterations，与 YAML 一致。两次 call 都从 empty decoder state 开始；posterior/LLR 在 decode 前冻结，无 decoder output、hard decision、syndrome、CRC、correctness callback 或 redecode。该解释保留 OFC17 `pilot soft state -> LLR refinement -> one downstream FEC` 身份。

## 3. 必须替换的 identity / metamorphic tests

### 3.1 Factor-2 identity（新增，必须比较 magnitude）

固定 `sigma_e2=0`、single state、任意 `N0_hat=C>0`，要求：

```text
prefix_residual_power_cplx = C
noise_var_real             = C/2
V_x                        = C

B2_single_state_preclip(y)
  == P08_maxlog_preclip(y*r_s^*, sigma2=C/2)
```

另设非 clip 样本，错误地传 `sigma2=C` 时 P08 LLR magnitude 应恰为正确值的 `1/2`；该 negative control 必须失败。只查 sign/hard bit 捕捉不到 factor-2。

### 3.2 State permutation — 原预期成立，但写清映射

对任意 permutation matrix `P`：

```text
T' = P*T*P^T,
r'_{P(s)} = r_s,
pi'_{P(s)} = pi_s.
```

posterior 只按 `P` 重排，marginalized LLR 不变。测试不得重新按自然编号生成 circulant `T`，否则测到的不是一般 permutation covariance。

### 3.3 Global `pi/2` covariance — 替换当前双重变换

只允许下列两个等价测试各自单独成立：

1. **rotate received only**：所有 received data/pilot observations 乘 `r_k`，known pilot/reference constellation 不动，同时 `pi'_u=pi_{u-k mod 4}`；LLR 不变。
2. **rotate coordinate system**：received observations、known pilots及带原 bit label 的 constellation points 全乘 `r_k`，state labels 不移动；LLR 不变。

“reference 也旋转”与“state label 再平移”不能在同一 test 同时做，否则重复补偿。

### 3.4 Single-state collapse — 用 IC-06R 后做数值 identity

不得只查 sign。应在 clip 前逐元素比较 IC-06R 与 `P08 maxlog(..., N0_hat/2)`；随后分别检查 clip 30 与 decoder clamp 20。

### 3.5 Uniform-state symmetry — 不得断言四 bit 全零

当 `pi_s=1/4` 时，`pi/2` rotation group 抹去 I/Q 的方向与坐标身份，但保留半径信息。对 P08 bit order `[b0,b1,b2,b3]`，正确解析恒等式是

```text
LLR_b0 = 0
LLR_b2 = 0
LLR_b1 = LLR_b3
```

其中 `LLR_b1/LLR_b3` 一般不为零：inner-inner 与 outer-outer 具有不同半径，uniform rotation 不能抹去这部分幅度信息。该 test 只作 analytic symmetry receipt，不进入 D0 acceptance score。

### 3.6 `p_s=0` 与 known-pilot identities — 保留并补零方差分支

- `p_s=0 -> q=0 -> T^d=I`，off-diagonal log transition 精确为 `-inf`；
- `V_x>0` 时 posterior 必须 finite/normalized，且不会产生 state switch；
- noiseless `V_x=0` 使用已登记 Dirac branch，正确 state 是唯一 finite path；
- 不得以 epsilon transition 或 truth state 让测试通过。

## 4. IC-01–IC-08 逐条终审

| IC | 终审 | 处置 |
|---|---|---|
| IC-01 | PASS | 正号 state、row/column convention 与 source model 自洽。 |
| IC-02 | CORRECT | 将 legacy estimator 输出命名为 complex residual power；P08 demapper 形参固定为其 AWGN complex component 的一半。 |
| IC-03 | CORRECT | 保留 `|x|^2(1-mu^2)`，但先从 raw prefix residual 中剥离已包含的 phase contribution，禁止 double count。 |
| IC-04 | PASS | uniform stationary prior、per-pilot/trajectory normalization、cell macro 与 deterministic tie-break 合法。 |
| IC-05 | PASS | local chain forward-backward 是 source-compatible、receiver-only 的确定性联合方式。 |
| IC-06 | CORRECT | state exact marginalization + inner P08 max-log；不用 exact inner symbol log-sum。 |
| IC-07 | PASS | `A_1-A_0`、positive-for-bit-1、`[b0,b1,b2,b3]` 正确。 |
| IC-08 | PASS | dual-pol 两次 batch one-way decode，无 feedback/state reuse。 |

## 5. 最终边界

修订后的 B2 仍是 `known pilots -> 4-state Markov posterior -> parallel soft LLR refinement -> one-way LDPC`，没有改变 OFC17 baseline 身份。修正只防止 legacy P08 裸名 `sigma2` 的 factor-2 泄漏、phase variance double count，以及 exact/max-log receipt 自相矛盾。工作量属于现有 `source_explicit_B2_adaptation_and_dev_freeze: 2.00 d` 内的确定性实现与单测，不构成 `BUDGET_BLOCKER`。

```text
FINAL_VERDICT = IC_SET_ACCEPTED_WITH_CORRECTIONS
```
