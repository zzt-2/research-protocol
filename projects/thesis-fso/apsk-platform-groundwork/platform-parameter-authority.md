# Coherent FSO 共同平台参数 authority

> T047 | Groundwork read-only authority extraction | 2026-08-30  
> 证据范围：仅 T042 的 6 篇 qualified full text；未检索、未下载、未实验、未形成方法 Q#。

## 1. 结论与使用规则

共同 DP-(8,8)-16APSK+BICM/LDPC 平台的物理默认值应冻结为 **memoryless、单 tap、unitary 2×2 Jones mixing**。有限 2×2 FIR 只在明确启用 receiver-local filter 或 I/Q timing skew 时开放；光纤 PMD、CD、DGD、XPM 及其 tap/dispersion 数值不得迁移到星地 FSO。大气偏振因直接全文缺失，不进入主动 testbed 或 claim。

本文采用五态：

- `SUPPORTED_ACTIVE`：六篇全文直接支持，且可作为共同平台主动模型。
- `SUPPORTED_FIXED`：六篇全文支持，但在 Ch4/Ch5 中只作固定接口或正确性条件。
- `CONDITIONAL`：论文中有直接模型/数值，但绑定于不同调制、轨道或 receiver 配置；只可做有标签的开发点。
- `EXCLUDED`：物理来源或场景不匹配，禁止进入共同星地 smoke。
- `UNKNOWN`：六篇全文没有足够 authority；不得凭经验补值。

**计数口径**：下文共有 `6` 个可直接冻结的 `SUPPORTED_ACTIVE/SUPPORTED_FIXED` 模型或参数项，`9` 个独立 `UNKNOWN` 项。`CONDITIONAL` 数值不计入“可冻结”。

## 2. 六篇 authority 身份

| ID | canonical identity | 本地全文 |
|---|---|---|
| L001 | Paillier et al., *JLT*, 2020, DOI `10.1109/JLT.2020.3003561` | `papers/arxiv/1911.11851/content.md` |
| L010 | Bernini et al., ICSOS 2022, DOI `10.1109/ICSOS53063.2022.9749703` | `papers/doi/10.1109_icsos53063.2022.9749703/content.md` |
| L027 | Vieira et al., *IEEE Access*, 2023, DOI `10.1109/ACCESS.2023.3287501` | `papers/doi/10.1109_access.2023.3287501/content.md` |
| L035 | Faruk and Kikuchi, *IEEE Photonics Journal*, 2013, DOI `10.1109/JPHOT.2013.2251872` | `papers/doi/10.1109_jphot.2013.2251872/content.md` |
| L047 | Roudas et al., *JLT*, 2009, DOI `10.1109/JLT.2009.2035526` | `papers/doi/10.1109_jlt.2009.2035526/content.md` |
| L054 | Kuschnerov et al., *JLT*, 2009, DOI `10.1109/JLT.2009.2024963` | `papers/doi/10.1109_jlt.2009.2024963/content.md` |

## 3. 公式、条件与边界

### 3.1 单 tap Jones 默认模型

共同平台采用

\[
\mathbf y[k]=a[k]e^{j\theta[k]}\mathbf J[k]\mathbf x[k]+\mathbf n[k],
\qquad \mathbf J^{\mathrm H}[k]\mathbf J[k]=\mathbf I,
\qquad \det\mathbf J[k]=1 .
\]

其中 `a[k]e^{jθ[k]}` 是标量大气耦合/相位项，`J[k]` 只描述两偏振的 memoryless mixing。该式是两篇 authority 的接口合成，而不是冒充某一篇的逐字公式：

- Roudas 的离散接收机是 memoryless TITO linear channel；无 PMD、无 PDL、两 SOP 保持正交时 Jones matrix 属于 `SU(2)`，故 `J^{-1}=J^H`。指针：`papers/doi/10.1109_jlt.2009.2035526/content.md`, §II-B–E, Eq. (5), (11)–(19), Appendix B Eq. (48)–(63)。
- Paillier 用复耦合 `C(t)` 定义耦合效率 `ρ(t)=|C(t)|²` 与相位 `φ(t)=arg C(t)`，并在 I/Q 样本中加入 `ΔωkT+φ_m(k)+φ(k)`。指针：`papers/arxiv/1911.11851/content.md`, §II-B Eq. (4), (6), (7), §III-A Eq. (8), (9)。
- Paillier 明确假设 `ρ` 与 `φ` 在一个 symbol 内不变。指针：同文 §III-A，Eq. (8)–(9) 后的成立条件。

Roudas 的逐元素三角参数化在本地转换中缺失，故逐字符 tap 公式为 `UNKNOWN`；不得靠常识补写。

### 3.2 unitary、PDL 与 ML/ZF 边界

`J^H` 作为 exact inverse 并与逐偏振 ML 判决等价，需要同时满足：unitary channel、两支路 spatially white 且等方差噪声、无 PMD-induced ISI；Roudas 的 ML 推导还排除了 laser phase noise 与 IF offset。指针：`papers/doi/10.1109_jlt.2009.2035526/content.md`, Abstract, §II-C–E Eq. (11)–(19), Appendix B Eq. (58)–(63)。

frequency-flat PDL/branch imbalance 使矩阵 nonunitary，但本身仍不产生 tap memory；Roudas Appendix C 将其写成 partial polarizer，并指出纯 unitary demultiplexer 会留下幅度不等与 residual XPI。指针：同文 Appendix C Eq. (64)–(70)。星地前端的实际 PDL 数值没有 authority，故保持 `UNKNOWN`，不能移入 Kuschnerov 的 `0–10 dB` 光纤扫描。

### 3.3 CFO、Doppler 与相噪

Paillier 的常频偏 I/Q 模型见 §III-A Eq. (8)–(9)。其星地下行假设完整 Doppler 约覆盖 `−4.5…+4.5 GHz`，先由轨道知识粗补偿，再保留最大 `100 MHz` constant residual；指针：`papers/arxiv/1911.11851/content.md`, §III-A “Coherent intradyne detection and digitization”。`100 MHz` DPLL 在无湍流和有 AO/AGC 湍流两种情况下均约 `1.4 ms` 锁定；指针：同文 §III-E Eq. (19), Fig. 10，以及 §IV-B Fig. 13。该数值绑定 BPSK、10 Gbaud 与论文 DPLL，只能是 `CONDITIONAL` smoke point。

Vieira 给出 Doppler 几何公式与一阶 ramp：

\[
\Delta f[n]=\Delta f_0+\frac{d\Delta f}{dt}nT_s .
\]

指针：`papers/doi/10.1109_access.2023.3287501/content.md`, §V Eq. (10), §VI Eq. (13)。其 Eq. (14) 的本地转换缺少可确认的复指数形式，且时变频率应累积成相位，故 Eq. (14) 的实现式为 `UNKNOWN`。

Bernini 的星地表给出：160 km 轨道最大 Doppler `±4.89 GHz`、最大变化率 `237 MHz/s`；1000 km 轨道对应 `±4.08 GHz`、`29 MHz/s`。指针：`papers/doi/10.1109_icsos53063.2022.9749703/content.md`, §II, Fig. 1, Table I。它们是轨道条件值，不是共同 smoke 的无条件默认。

激光相噪是 Ch3 承重项。Vieira 的特定 32-GBaud 仿真把 Tx/LO linewidth 各设为 `100 kHz`；指针：`papers/doi/10.1109_access.2023.3287501/content.md`, §VII simulation setup。该数值对 APSK 仅为 `CONDITIONAL`。Paillier 的大气 turbulent phase coherence time 约 `1 ms`，慢于 `10 Gbaud` symbol rate；指针：`papers/arxiv/1911.11851/content.md`, §II-C, Fig. 6。它不能替代 Tx/LO laser linewidth。

### 3.4 receiver filter 与 I/Q impairment

Faruk 的 receiver-local I/Q 模型为

\[
\mathbf P=
\begin{bmatrix}
\cos\delta_I&\sin\delta_I\\
-\sin\delta_Q&\cos\delta_Q
\end{bmatrix},\quad
\mathbf G=\operatorname{diag}(\alpha_I,\alpha_Q),\quad
\mathbf D(\omega)=\operatorname{diag}(e^{j\omega\tau_I},e^{j\omega\tau_Q}),
\]

\[
\mathbf\Omega(\omega)=\mathbf P\mathbf G\mathbf D(\omega).
\]

指针：`papers/doi/10.1109_jphot.2013.2251872/content.md`, §2 Eq. (2)–(14)。Fourier 符号约定必须与实现统一。传统四个 complex FIR 不能表达每偏振完整的 I/Q inverse；论文用每个 complex FIR 内部四个 real FIR、总计 `16` 个 real FIR。指针：同文 §3, Fig. 2, Eq. (15)–(28)。

Faruk 的 `10° / −2 dB / 10 ps` 组合点、`10 Gsymbol/s`、RRC roll-off `0.5`、`2 Sa/symbol` 均绑定 square-QAM 验证；指针：同文 §4、Table I。只有模型结构可主动复用，数值为 `CONDITIONAL`。

Vieira 的 receiver chain 在 32 GBaud、RRC roll-off `0.1`、`2 Sa/symbol` 下使用 10th-order super-Gaussian analogue filter，并在 coarse CFO correction 后使用 `40-tap, 19.4 GHz` rectangular LPF；指针：`papers/doi/10.1109_access.2023.3287501/content.md`, §VI receiver chain, §VII simulation setup。参数绑定论文 QAM/CFO 配置，为 `CONDITIONAL`。

Kuschnerov 明确：`2 Sa/symbol` 才能 fully equalize，`1 Sa/symbol` 只适合有限 dispersion tolerance；指针：`papers/doi/10.1109_jlt.2009.2024963/content.md`, §II, Fig. 1–2。其 `35 GHz` second-order Gaussian optical filter、`19.6 GHz` fifth-order Bessel electrical filter以及 `5/9/15 taps` 均属特定光纤/QPSK receiver，不能无条件迁移。

### 3.5 finite FIR 与 PMD 边界

finite 2×2 FIR 是 `CONDITIONAL` 分支：

- 合法触发：已定义的 receiver filter、ADC sampling phase、I/Q timing skew 或实测 optical path mismatch。
- 非法触发：仅因“DP”或“大气偏振”存在，就把信道写成多 tap。
- Kuschnerov 的 `15-tap T/2`、`30 ps mean DGD`、`1000 ps/nm CD`、`0–10 dB PDL` 是 112-Gb/s PolMux-QPSK 光纤 stress；指针：`papers/doi/10.1109_jlt.2009.2024963/content.md`, §V, Fig. 12–13。全部对星地共同 smoke 为 `EXCLUDED`。
- Roudas 的单 tap模型明确以无 PMD 为成立条件；Faruk 的多 tap来源是 receiver-local I/Q delay，而不是大气 PMD。

## 4. authority 五态表

| # | 平台项 | 状态 | authority 与用途 | Ch3 / Ch4 / Ch5 |
|---:|---|---|---|---|
| 1 | memoryless 2×2 Jones | `SUPPORTED_ACTIVE` | Roudas §II Eq. (5), (11)–(19) | Ch4 承重；Ch3/Ch5 固定接口 |
| 2 | unitary `J^H J=I`, `det J=1` | `SUPPORTED_ACTIVE` | Roudas §II-B–E, Appendix B | Ch4 承重的默认物理边界 |
| 3 | 标量大气 coupling/phase，symbol 内常值 | `SUPPORTED_ACTIVE` | Paillier §II-B Eq. (4),(6),(7), §III-A Eq. (8),(9) | Ch3 承重；Ch4 不制造 headroom |
| 4 | Doppler/CFO 先粗补偿、残差再跟踪 | `SUPPORTED_FIXED` | Paillier §III-A/III-D；Bernini §II/IV；Vieira §VI | Ch3 承重；Ch4/Ch5 只接收已同步流 |
| 5 | `2 Sa/symbol` receiver input | `SUPPORTED_FIXED` | Vieira §VI–VII；Faruk §4；Kuschnerov §II | Ch4 固定采样接口 |
| 6 | equal-branch white noise 下 `J^H` correctness oracle | `SUPPORTED_FIXED` | Roudas §II-C–E, Appendix B | Ch4 smoke oracle；Ch5 接收 noise metadata |
| 7 | Paillier residual CFO `100 MHz` | `CONDITIONAL` | Paillier §III-A, Fig. 10/13 | Ch3 开发点，不是 Ch4 扫描轴 |
| 8 | Vieira Tx/LO linewidth 各 `100 kHz` | `CONDITIONAL` | Vieira §VII | Ch3 固定开发点；Ch4/5 不再独立扫 |
| 9 | `32 GBaud`, RRC `0.1` | `CONDITIONAL` | Vieira §VII | 可作共同 smoke 候选，非 APSK direct authority |
| 10 | 10th-order SG + 40-tap/19.4-GHz LPF | `CONDITIONAL` | Vieira §VI–VII | receiver filter 开发分支 |
| 11 | IQ gain/phase/timing-skew 模型 | `SUPPORTED_ACTIVE` | Faruk §2 Eq. (2)–(14) | Ch4 receiver-front-end 承重；最小 smoke 默认关闭 |
| 12 | `10°/−2 dB/10 ps` IQ 组合点 | `CONDITIONAL` | Faruk §4, Table I | 仅 square-QAM stress，不作 APSK 默认 |
| 13 | frequency-flat nonunitary PDL-like gain | `CONDITIONAL` | Roudas Appendix C | 可作负测试；数值 `UNKNOWN` |
| 14 | finite 2×2 FIR | `CONDITIONAL` | Faruk §3；Kuschnerov §V | 仅 receiver-local memory 分支 |
| 15 | 光纤 PMD/DGD/CD/XPM | `EXCLUDED` | Kuschnerov 全文，特别是 §III–VI | 不迁移至星地 FSO |
| 16 | Kuschnerov `15 taps/30 ps/1000 ps/nm/0–10 dB` | `EXCLUDED` | Kuschnerov Fig. 12–13 | 只可标作 fiber stress reference |
| 17 | Vieira LEO–LEO `6.3443 GHz/1.2562 GHz/s` | `EXCLUDED` | Vieira Table VI | 不冒充星地默认 |
| 18 | atmospheric polarization 主动损伤 | `EXCLUDED` | 六篇无直接 atmospheric-polarization qualified full text | 不进 testbed/claim；事实状态见 UNKNOWN-1 |

## 5. 最小共同 correctness smoke 配置

| 配置项 | smoke 冻结值 | 状态 | paper pointer |
|---|---|---|---|
| 双偏振通道 | 单 tap、memoryless `J∈SU(2)`；一个 smoke block 内常值 | `SUPPORTED_ACTIVE` | Roudas §II-B–E Eq. (5),(11)–(19), Appendix B |
| oracle | `J^H`；允许 permutation/constellation rotation 后比对 | `SUPPORTED_FIXED` | Roudas §II-D–E, Appendix B Eq. (58)–(63) |
| receiver sampling | `2 Sa/symbol`，matched filter 后再降采样 | `SUPPORTED_FIXED` | Vieira §VI–VII；Faruk §4；Kuschnerov §II |
| branch noise | 两支路 independent、equal-variance circular noise | `SUPPORTED_FIXED` | Roudas §II-C–D ML/ZF 等价条件 |
| CFO path | coarse FOE 在 Ch4 前完成；第一非零检查点用 `100 MHz` residual | `CONDITIONAL` | Paillier §III-A, Fig. 10, Fig. 13 |
| phase noise | Tx/LO linewidth 各 `100 kHz` 仅作开发固定点 | `CONDITIONAL` | Vieira §VII |
| baud/pulse | `32 GBaud`, RRC roll-off `0.1` 仅作开发固定点 | `CONDITIONAL` | Vieira §VII |
| receiver filter | 先用 Vieira 的 10th-order SG；40-tap/19.4-GHz LPF 只在 CFO 分支启用 | `CONDITIONAL` | Vieira §VI–VII |
| I/Q impairment | 最小 smoke 关闭；第二阶段逐轴启用 phase、gain、skew | `SUPPORTED_FIXED`（关闭） | Faruk §2 Eq. (2)–(14) 定义 ideal/imbalanced interface |
| PDL/PMD/FIR | PDL、PMD、任意多 tap channel memory 全部关闭 | `EXCLUDED` | Roudas unitary条件；Kuschnerov fiber边界 |

此 smoke 只验证接口和物理正确性，不声称 APSK 性能。CFO、phase noise、filter、I/Q 不同时叠加制造 headroom；每次只打开一个 conditional axis。

### Smoke PASS 条件

1. `J=I` 与随机 `J∈SU(2)` 经 oracle `J^H` 后，在相同 noise realization 下输出一致。
2. unitary mixing 前后总功率不变；equal-variance noise covariance 保持不变。
3. single-tap Ch4 输出经允许的 permutation/phase ambiguity 对齐后与无 mixing reference 一致。
4. 启用 frequency-flat nonunitary gain 时，unitary oracle 必须暴露 residual gain/XPI，而不能误报 PASS。
5. 启用 receiver-local skew 时，single tap 必须显示不充分；只有显式 finite-FIR 分支才允许恢复。

## 6. 后续开发矩阵可扫描维度

| 维度 | 合法扫描方式 | 禁止方式 | authority |
|---|---|---|---|
| Jones mixing | unitary 单 tap；结构性随机角度，不声称星地统计 | 杜撰 rotation rate/coherence time | Roudas §II |
| residual CFO | `0 ↔ 100 MHz` correctness point；另以 Bernini 轨道表做捕获范围边界分析 | 将 `±4.9 GHz` 与其他损伤叠加作 Ch4 收益 | Paillier Fig. 10/13；Bernini Table I |
| CFO ramp | 单独扫描；使用 Vieira Eq. (13)，导数值按具体几何另定 | 直接套 LEO–LEO `1.2562 GHz/s` | Vieira §V–VI, Table VI |
| linewidth | `100 kHz`/laser 单点后再决定是否扩展 | 无 authority 自造 PSD 或宽范围 | Vieira §VII |
| receiver filter | Vieira 配置单点；改变带宽时必须重新声明归一化口径 | 用 filter memory 冒充 atmospheric PMD | Vieira §VI–VII |
| IQ phase/gain/skew | 分轴；Faruk 组合点只作标注 stress | 把 QAM 容差直接写成 APSK 容差 | Faruk §2–4, Table I |
| PDL-like gain | 仅 frequency-flat front-end negative test | 套用 fiber `0–10 dB` 为星地分布 | Roudas Appendix C；Kuschnerov Fig. 13 |
| finite FIR | 仅由已定义 filter/skew 触发，tap span须覆盖已知 memory | 任意增加 taps 制造 Ch4 headroom | Faruk §3；Kuschnerov §V |

## 7. Ch4 → Ch5 接口

Ch4 输出必须携带以下字段；这是由 Roudas 的 linear/MMSE noise 条件和 Faruk 的 receiver-local compensation边界综合得到的项目接口，不是新增方法：

| 字段 | 含义 | authority |
|---|---|---|
| `z[k,pol]` | 完成 CFO/Ch3 carrier recovery、receiver compensation 与 2×2 demux 后的两路 complex symbol | Roudas §II-C–E；Kuschnerov Fig. 2 的模块顺序 |
| `G_eff[pol]` | post-equalization complex gain；unitary smoke 应为 unity/已归一化 | Roudas unitary/ZF 条件；Appendix C nonunitary边界 |
| `Sigma_n` | `2×2` post-equalization noise covariance；只有验证后才可降成 scalar variance | Roudas §II-C–D general receiver 与 white-noise special case |
| `sample_phase` | matched-filter/降采样后的 symbol timing 状态 | Kuschnerov §II/IV；Faruk timing-skew模型 |
| `impairment_flags` | CFO、phase noise、IQ、PDL-like、FIR 分支是否启用 | 六篇边界综合；禁止隐式叠损伤 |
| `constellation_id` / `labeling_id` | Ch5 demapper 使用的 `(8,8)-16APSK` 星座与 bit labeling identity | 项目固定身份；六篇不提供 APSK labeling authority，因此不得从六篇补数值 |

Ch5 不重新注入 CFO、phase noise、PDL 或 PMD。若 `Sigma_n` 未验证为 scalar，Ch5 必须消费 covariance-aware metadata，不能静默按 AWGN 标量近似。

## 8. UNKNOWN 清单（9 项）

| UNKNOWN | 缺口 | 对当前工作的影响 |
|---:|---|---|
| 1 | 星地 atmospheric polarization 的直接全文、扰动强度与时间统计 | 保持 `EXCLUDED`，不进入主动 testbed/claim |
| 2 | 星地 Jones rotation rate、coherence time、angle distribution | smoke 只能 block-constant structural randomization |
| 3 | 目标 telescope/PBS/hybrid/photodiode 的 PDL-like gain 数值 | nonunitary 仅作无量级负测试 |
| 4 | 两 coherent branches 的实测 noise covariance | 最小 smoke 暂用 Roudas 的 equal-white special case |
| 5 | 共同 APSK receiver 的最终 analogue/electrical filter transfer function及带宽口径 | **唯一 correctness-smoke blocker**：未冻结前不能声称 finite-FIR/filter 分支正确 |
| 6 | receiver-local FIR 的最小 tap count、训练长度与 LMS step size | finite-FIR 分支保持未冻结 |
| 7 | `(8,8)-16APSK` 的 FOE 幂次/捕获范围、BPS 窗长与 test phases | Vieira 的 QAM/BPSK参数不迁移 |
| 8 | ADC bit depth、量化噪声与 IQ imbalance 所需动态范围 | 不进入首轮 floating-point smoke |
| 9 | CFO/ramp、IQ skew、Jones mixing 与 APSK demapper 联合存在时的可辨识性 | 开发矩阵必须逐轴，不得联合声称 |

## 9. 唯一 smoke blocker

**唯一 blocker：共同 APSK receiver 的正式 filter authority 尚未冻结，包括 analogue/electrical transfer function、3-dB/单边/双边带宽口径，以及由此推出的最短 FIR span。**

它不阻塞 memoryless Jones + equal-white-noise 的最小接口 smoke；它阻塞的是把 receiver filter/timing-skew finite-FIR 分支纳入“correctness 已验证”的共同平台。修复前，Ch4 必须以单 tap 为默认，filter/FIR 只能保留 `CONDITIONAL/UNKNOWN`。
