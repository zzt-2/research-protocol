# RML-FSTS Step 4a 物理转移审计

> 日期：2026-08-09
> 任务：T017
> 边界：只读审计与确定性公式核算；未运行 estimator/performance grid，未联网，未修改 `common/`、`params.py` 或治理文件。

## 结论

**Terminal：`SOURCE_CONDITION_ONLY_NO_NOISE_CLOSURE`**

本地一手公式足以把 Wang 的两档 `C_n^2` 在**额外指定波长、平面波、零内尺度、点接收**假设下转成 Rytov 方差与一组 Gamma-Gamma `alpha/beta`，因此可做显式标注的条件敏感性分析；但这不是 Wang 的 phase-screen + 0.2 m aperture + single-mode-fiber coupling 的 source reproduction。更关键的是，Wang 只说考虑 shot/thermal noise，没有给出噪声带宽、温度/负载、暗电流/背景光、前端滤波与数字归一化，故 `ROP[dBm] -> discrete complex AWGN variance` 不唯一。现有 `gamma_bar` 只能承载独立的无量纲 SNR 诊断，不能冒充 Wang 的 dBm 轴。

**唯一最小补件**：由源仿真/作者给出一个带明确参考面的后端标定接口

```text
per-branch P_rx[dBm] at coherent-receiver input
    -> post-filter/post-ADC E[|w[k]|^2]
```

并同时声明该离散样值的复噪声约定、滤波/采样归一化与功率参考面。这个表/函数直接吸收未知的 noise-equivalent bandwidth、BPD/90° hybrid 分光因子、TIA/thermal/background/dark-current 与 ADC 增益，是比逐项猜前端参数更小且可验证的补件。补件到位后可运行 source-power-conditioned baseband smoke；在此之前只能运行明确标为 `normalized electrical SNR diagnostic` 的结构诊断。

## 1. `C_n^2, lambda, L -> Rytov -> alpha,beta`

### 1.1 源公式与输入血缘

Gu 2022 的平面波公式（其 Eq. (6)、(7)、(9)，`papers/doi/10.3390_app12073331/content.md:90-109`）与 Al-Habash 2001 的 GG 建模来源一致。令

```text
s = sigma_R^2 = 1.23 C_n^2 k^(7/6) L^(11/6),  k = 2 pi / lambda
alpha(s) = { exp[0.49 s / (1 + 1.11 s^(6/5))^(7/6)] - 1 }^(-1)
beta(s)  = { exp[0.51 s / (1 + 0.69 s^(6/5))^(5/6)] - 1 }^(-1)
```

这里把 Gu 式中的 `sigma_l^(12/5)` 写成 `s^(6/5)`，因为 `s = sigma_l^2`。`params.py:100-170` 也用同一映射复核 Gu 的三档冻结值。

| 输入 | 值 | 身份 | 证据/限制 |
|---|---:|---|---|
| `C_n^2` | `1e-16 / 1e-14 m^(-2/3)` | **SOURCE** | Wang `content.md:241` |
| `L` | `10 km` | **SOURCE** | Wang `content.md:241` |
| inner/outer scale | `l0 -> 0`, `L0 -> infinity` | **SOURCE** | Wang `content.md:241` |
| receive aperture | `0.2 m` | **SOURCE** | Wang `content.md:243`；不进入上述点接收 GG 映射 |
| mean coupling | `67.3012% / 4.8395%` | **SOURCE** | Wang `content.md:243`；只给均值，不给分布或与 phase/intensity 的联合统计 |
| `lambda` | 未给 | **MISSING** | Wang 全文未给 `nm`/wavelength；没有 `k` 就没有唯一 Rytov 数值 |

### 1.2 确定性 sanity check

仅把 `params.py:73-82` 文本写明的“1550 nm”当 **ASSUMPTION**，取 `lambda=1550 nm`，得到：

| Wang condition | `sigma_R^2` | `alpha` | `beta` | 身份 |
|---|---:|---:|---:|---|
| `C_n^2=1e-16`, `L=10 km` | `0.135642143` | `16.3374182` | `14.7132819` | **DERIVED under ASSUMPTION lambda=1550 nm** |
| `C_n^2=1e-14`, `L=10 km` | `13.5642143` | `6.35494501` | `1.06954735` | **DERIVED under ASSUMPTION lambda=1550 nm** |

这两组数不能称为 Wang reproduction：

1. Wang 没给波长。项目字段自身也不构成唯一数值真相：`params.py:74` 的字面值 `F_CARRIER=1.55e14 Hz` 对应 `lambda=1934.1449 nm`，而 `params.py:75,78` 的文字写“1550 nm”。若按字面频率计算，两档结果分别变成 `(sigma_R^2,alpha,beta)=(0.10476377,20.6774,18.9359)` 与 `(10.476377,5.78368,1.09591)`。因此本轮只能按文字的 1550 nm 做 sensitivity，不能据项目字段替 Wang 补参数。
2. Gu 冻结档为 `(sigma_R^2,alpha,beta)=(0.2,11.6,10.1)` 和 `(3.5,4.2,1.4)`（`content.md:117`; `params.py:100-170`）。尤其 Gu strong 的 `sigma_R^2=3.5` 与上述 Wang+1550 nm 的 `13.5642` 不同，不能把 Gu strong 标签写成 Wang `C_n^2=1e-14` calibration。
3. Al-Habash/Gu 映射给的是平面波归一化辐照度边缘分布；它没有吸收 0.2 m aperture averaging、有限光束传播、phase-screen sampling、SMF modal overlap 或 coupling fluctuation。Wang 的平均 coupling 只可确定平均损耗：弱/强分别为 `-1.7198 dB`、`-13.1520 dB`，相差 `-11.4322 dB`（**DERIVED**），不能重建 coupling 的逐 realization 分布。

## 2. Wang phase screen + coupling 与 scalar GG 的保真边界

Wang 的后 MRC/偏振解复用模型为

```text
R_X[k] = gamma sqrt(eta I P_LO) S_X[k]
         exp(j(phi + theta_k + theta_x + 2 pi f k T_s)) + N_X[k]
```

Y 偏振同形；`phi, eta, I` 分别是湍流相位、耦合效率与光强起伏，论文明确三者相对 GHz 符号率为慢变量（`content.md:152-173`）。phase-screen、10 km、孔径与平均耦合见 `content.md:231-243`。

现有 `common/_gg_time.py` 生成的是均值约 1 的归一化辐照度 `h=X*Y`；`common/_dual_pol_channel.py:103-132` 只以 `sqrt(h)` 乘归一化双偏振符号，再叠加由 `gamma_bar` 决定的 AWGN。相关测试只验证 same-seed reproducibility、shape/key、runtime-config 注入与旧 QPSK bit-exactness（`tests/test_dual_pol_shared_channel.py`）；不验证 phase-screen/coupling/noise calibration 等价。

| 对 320-symbol fine-FOE ranking 的结构 | scalar GG 是否保留 | 审计结论 |
|---|---|---|
| 双偏振共享的归一化幅度条件 | 部分保留 | `sqrt(h)` 同时作用于 X/Y，可形成 paired power/fade 条件。 |
| 单个 FSTS 内近似准静态的湍流幅度 | 保留 | 10 GBaud 下 320 symbols=`32 ns`（**DERIVED**）；Valjus 报 atmospheric coherence time 通常 `>1 ms`（`papers/doi/10.1002_sat.1553/content.md:167`），至少跨 `31,250` 个这种窗口。 |
| 激光 CFO/PN 与 receiver AWGN | common primitive 未完整保留 | AWGN 有；`_dual_pol_channel.py` 本身没有 CFO/laser-PN，需隔离 adapter 显式加入。 |
| 湍流 phase `phi` 的时间/空间相关 | 丢失 | GG 是正实辐照度；没有 phase-screen wavefront，也不能验证不同 lag 的 phase reliability。 |
| aperture averaging 与 SMF coupling fluctuation | 丢失 | 只有归一化 `h`；Wang 的 0.2 m 孔径及 `eta` 分布/模态重叠未进入。 |
| `I, eta, phi` 的联合统计 | 丢失 | 平均 coupling 不能恢复相关性或尾部。 |
| 多 telescope 独立 branch、branch phase correction 与 MRC | 丢失 | common DP 是两偏振单一 scalar `h`，不是 Wang 的空间分集 phase-screen realization。 |
| 绝对 ROP 与随光功率变化的 shot noise | 丢失 | common 的 `h` 均值归一，AWGN 由独立 `gamma_bar` 控制。 |

对 32 ns 的同一 FSTS，Wang 自身的慢变假设支持把 atmospheric amplitude/phase 近似为常量；因此 scalar GG 可以保留“瞬时功率改变有效噪声可靠性”这一最小结构。但常量 phase 在 FOE 的相位差中被消除，常量幅度在固定 measured-power 条件下也主要被 SNR 吸收。故 scalar GG 的 weak/strong 标签不能单独证明 lag-ranking crossover；它最多是带明确 claim ceiling 的结构诊断。

## 3. `ROP + LO + responsivity + shot/thermal -> discrete AWGN` 不闭合

本地公式 owner `毕设/formulas-master.md:175-205` 给出：

```text
P_IF = 2 R^2 P_S P_LO
sigma_shot^2 = 2 e [i_D + R(P_S + P_LO + P_B)] Delta_f
sigma_thermal^2 = 4 k_B T_K Delta_f / R_L
SNR = P_IF / (sigma_shot^2 + sigma_thermal^2)
```

Wang 给出的 `P_LO=15 dBm`、`R=0.8 A/W` 是 **SOURCE**；`15 dBm=31.6228 mW` 是 **DERIVED**。但下列量均未给出：

- `Delta_f`/matched-filter noise-equivalent bandwidth；
- `T_K`, `R_L` 或等效 TIA input-noise/noise figure；
- dark current `i_D` 与 background optical power `P_B`；
- 90° hybrid/BPD 的分光约定、每 photodiode/per-IQ/per-pol 功率参考面；
- analog gain/filter、ADC sample rate/quantization 与 DSP normalization；
- “average received optical power”究竟是 telescope 前、coupling 后、单 branch 还是 MRC 后。

所以即使 `P_S` 的 dBm 点已知，连续电流噪声方差与离散复样值噪声方差仍不唯一。不得用典型 `T/R_L/Delta_f` 补空，也不得仅因公式维度一致就称 source calibration。

一旦源标定给出复符号 SNR `gamma`，当前 common 的数字约定才是唯一的：`nv=1/(2*gamma)` 为每个实维高斯方差，故 `E|w[k]|^2=1/gamma`（`_dual_pol_channel.py:126-132`）。现在缺的是 `P_rx[dBm] -> gamma`，不是高斯数如何生成。

## 4. measured receiver power 能否直接作 cell axis

分两种语义：

1. **已有真实/源仿真接收复样值**：可以按同一参考面测得的 ROP 或 receiver-derived sample power 分 cell，SNR 仅作后验诊断；estimator 与 structural `B_L` paired comparison 都可运行。此时噪声已经包含在样值里，不需要反推。
2. **从 ROP 合成接收复样值**：不可以只把 ROP 当生成轴、把 SNR 留到事后。生成样值前必须先决定噪声方差；后验 SNR 不能反向生成尚未定义的噪声。可以另用独立 `gamma_bar` 跑 estimator 并比较 structural `B_L`，但 cell 必须标成 `normalized electrical SNR`，其 receiver-visible power proxy 只能是无量纲样值统计，不能标 dBm 或 Wang source condition。

Valjus 只支持“pre-amplified coherent receiver 的 SNR 可假设与 received power 成比例，并令二者采用同一分布”（`content.md:149-150`）；该文随后自行选择 baseline SNR 使平均 BER 达 `1e-3`。这支持相对分布/后验分层，不提供 Wang 的绝对 dBm-to-SNR 标定。

## 5. 审计边界与后续使用限制

- 可用：把 Wang `C_n^2`、10 km 与本地公式形成**带波长假设的 sensitivity table**；把 Gu GG 档作为不同来源的 normalized-condition diagnostic；在同一复样值上做 paired structural `B_L` 检查。
- 不可用：把 Gu weak/strong 称为 Wang phase-screen calibration；把平均 coupling 当逐 realization coupling；把 `10/20 dB gamma_bar` 改名为 Wang ROP；用上述诊断发 Q1 Go/Kill/Resolved terminal。
- 本报告只关闭 V006 P0-2 中“本地公式能否自动补齐物理转移”的问题：答案是**只能补 source-condition sensitivity，不能补 noise closure/source calibration**。
