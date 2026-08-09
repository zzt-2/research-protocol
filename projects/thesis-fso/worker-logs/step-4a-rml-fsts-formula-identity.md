# RML-FSTS formula/identity audit

## Status

**PARTIAL**

审计边界：仅使用 T011 明列的共享论文材料、既有 read-note/literature owner 与现有 `frame_sync_fsts.py`。两篇 T011 指定的 canonical `source.pdf` 均不存在，因此无法完成“PDF 页码 + 公式号”的双重核验；Wang 2023 的 HTML/MathJax 转写保留了公式本体，可作带限制的逐式转录，Enhanced 2024 的 `content.md` 只剩公式编号占位，不能重建公式。本报告不作 Go/Kill、novelty 或 controller 结论。

材料可用性实测：

- `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/source.pdf`：**missing**。
- `D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/source.pdf`：**missing**。
- 两个 DOI 目录均只有 `content.md` 与 `metadata.json`。
- Wang 2023 公式来源：`.../10.1109_jphot.2023.3265847/content.md:121-215`；未获 PDF 页码，以下公式均标为“PDF 未复核”。
- Enhanced 2024 公式缺失证据：`.../10.1364_oe.520452/content.md:211-247,264-310,371-375` 仅保留 `(1)`–`(21)` 编号/解释文字，没有公式本体。

## Method identity

### Wang 2023 FSTS

**FACT — training object.** 每个极化的 FSTS 由前、后两部分组成，前后互为共轭对称；每一部分含 `B_N/2` 个块，每块 `B_L` 个 PRBS 生成的训练符号。X/Y 两极化的相邻块交错相同，块内相邻符号也交错相同；`B_N/2` 与 `B_L` 均要求为偶数。证据：`10.1109.../content.md:103-109`。

由该结构可直接计数：每个极化（亦即 320 个 symbol-time，而不是把双极化样值相加为 640）的训练长度为

\[
N_{TS}=2\times(B_N/2)\times B_L=B_NB_L.
\]

这是由原文结构与默认参数共同闭合的 **INFERENCE**；默认 `(B_N,B_L)=(16,20)` 与 `(8,40)` 都给出 320，见 `content.md:299`。

**FACT — receiver order and I/O.** 原文链路顺序为：I/Q imbalance recovery → 每支路 FS（找 TS 起点并对齐分集支路）→ diversity-branch phase correction → MRC → polarization demultiplexing → two-stage FOE → phase-noise estimation → DD-LMS → demap/BER。FS 在合并前逐支路运行；FOE 在 MRC 与偏振解复用后，以共同 CFO 的 X/Y 双偏振 TS 样值为输入。证据：`content.md:101,119-152,225-243`。

1. **FS input/output**：输入第 `m` 支路的接收复样值；通过共轭对称 FSTS 的 Park 型度量输出帧起点 `d_start`，并据此对齐各支路。它不是“已知模板匹配滤波”。
2. **coarse FOE input/output**：输入已对齐、MRC、偏振解复用后的 X/Y TS 样值；利用相邻 symbol-time 的跨偏振共轭积，输出 `Δf_1`，理论范围 `[-R_s/2,+R_s/2]`（1 sps）。
3. **fine FOE input/output**：先用 `Δf_1` 补偿 TS，再对相隔 `B_L` 个 symbol-time 的跨偏振块作共轭积，输出残余 `Δf_2`。
4. **final output**：`Δf_est=Δf_1+Δf_2`，用于补偿整个训练周期；之后仍有 phase-noise estimator 处理残余。

调用顺序及范围证据：`content.md:175-215`；“先补偿再 fine”见 `content.md:185`；完整 DSP 次序见 `content.md:243`。

### Enhanced 2024 mixed PRBS/cyclic-QPSK method

这不是 Wang 2023 的同一 FSTS 公式换名，而是一个相关但不同的 mixed-training 方法。

**FACT — training object.** 前缀是 PRBS，后缀由周期为 16 symbols 的循环 QPSK 小段 `a` 组成，多个 `a` 组成 A/B/C 等块。PRBS 专用于 FS；QPSK 后缀用于 coarse + fine FOE。证据：`10.1364.../content.md:187-205`。

**FACT — receiver order and I/O（公式本体缺失，仅能核对文字身份）.**

1. **FS**：接收端保存发送 PRBS 的“相邻共轭差分后再取共轭”的序列 `ts'`；接收样值先做相邻差分共轭，再乘 `ts'` 并求和构成时序度量，峰值给帧起点。证据：`content.md:207-249`。Eq. (1)–(10) 本体缺失。
2. **coarse FOE**：FS 后截取循环 QPSK 后缀；在 MRC 后做 FFT 谱峰搜索，以零 CFO 时的基准谱峰与偏移谱峰之差得到 coarse CFO。QPSK 构造使最大基准峰位于 `R_s/8`，理论 coarse range 为 `[-3R_s/8,+3R_s/8]`。证据：`content.md:251-281`。Eq. (11)–(13) 本体缺失，符号/正负号规则无法精确复原。
3. **fine FOE**：coarse 补偿后，将一极化当前块与另一极化滞后 `T_L` 的块交叉共轭，A↔B 对称相加；除以 `T_L` 抑制 Gaussian phase noise，同时缩小无模糊范围。证据：`content.md:283-312`。Eq. (14)–(18) 本体缺失，不能把 Wang Eq. (8)–(10) 直接冒充 Enhanced 公式。
4. **final output**：正文仅保留 `Δf_est=Δf_a+Δf_b` 的文字，并称 Eq. (18) 后数据已作 CFO compensation；Eq. (19)–(20) 本体同样缺失，见 `content.md:294-312`。

因此，Enhanced 的 `T_L` 与 Wang 的 `B_L` 都是 fine-stage correlation spacing / block length，但 training object、coarse estimator 和精确索引并不相同；二者只能按“同类 tradeoff”对照，不能公式级互换。

## Exact formulas

下表中的 Wang 公式是共享 `content.md` 的 MathJax 转录；由于 canonical PDF 缺失，`page` 一律 UNKNOWN，不满足 PDF 复核门。Enhanced 公式本体一律保持 UNKNOWN。

| component | equation | page/eq | symbols | implementation implication |
|---|---|---|---|---|
| Wang FS metric | `M_m(d)=|C_m(d)|^2/[P_m(d)]^2` | PDF page **UNKNOWN** / Eq. (1); `content.md:121-125` | `m`: branch；`d`: candidate start；`P_m(d)=Σ_{i=0}^{N/2-1}|R_m(d+i)|²` | 对每支路计算归一化自结构度量；不能替换成模板匹配相关。 |
| Wang FS correlation | `C_m(d)=Σ_{i=0}^{N/2-1} R_m(d+i)R_m(d-i)` | PDF page **UNKNOWN** / Eq. (2); `content.md:126-142` | `N`: TS length used by FS；原式乘积不带显式 conjugate，因为训练前后本身共轭对称 | `d_start=argmax_d M_m(d)`；论文另允许阈值提前命中。 |
| Wang coarse FOE | `2πΔf_1T_s = arg{Σ_{i=1}^{B_LB_N/2}[R_X*(2i−1)R_Y(2i)+R_Y*(2i−1)R_X(2i)]}` | PDF page **UNKNOWN** / Eq. (7); `content.md:175-183` | `R_X,R_Y`: demux 后双偏振 TS；`T_s=1/R_s`；`B_L`: block length；`B_N`: total block count | `Δf_1=angle(S_1)/(2πT_s)`；必须保留 X/Y 交错训练结构。范围 `±R_s/2`。 |
| Wang fine correlation 1 | `R_1=R_X*(i+(2j−2)B_L)R_Y(i+(2j−1)B_L)` | PDF page **UNKNOWN** / Eq. (9); `content.md:193-199` | `i=1...B_L`, `j=1...B_N/2`；这里的 `R` 是 coarse-compensated TS（由 Eq. (8) 前文字确定） | 对相邻 block pair 中同一 intra-block index、跨偏振、相距 `B_L` 个 symbol-time 的样值相关。 |
| Wang fine correlation 2 | `R_2=R_Y*(i+(2j−2)B_L)R_X(i+(2j−1)B_L)` | PDF page **UNKNOWN** / Eq. (10); `content.md:200-206` | 与 `R_1` 对称 | 两个偏振方向必须共同求和，不能只取单偏振 lag correlation。 |
| Wang fine FOE | `2πΔf_2T_s = arg[Σ_{j=1}^{B_N/2}Σ_{i=1}^{B_L}(R_1+R_2)]/B_L` | PDF page **UNKNOWN** / Eq. (8); `content.md:185-192` | `Δf_2=f−Δf_1`；`arg` 取 principal angle | `Δf_2=angle(S_2)/(2πB_LT_s)`；larger `B_L` 把相位噪声项对频率估计的影响缩小 `B_L` 倍，但 fine unambiguous residual range 也缩小 `B_L` 倍。 |
| Wang final FOE | `2πΔf_estT_s=2πΔf_1T_s+2πΔf_2T_s` | PDF page **UNKNOWN** / Eq. (11); `content.md:208-215` | `Δf_est=Δf_1+Δf_2` | 必须先 coarse compensation、再 fine、最后合成；不可直接对原始样值跑 fine。 |
| Enhanced differential FS | **UNKNOWN：Eq. (1)–(10) 本体缺失** | PDF/page **UNKNOWN**; placeholders `content.md:211-247` | 文字可确认 `M,C,P,R_n,ts,ts',w,u`，但索引/共轭位置不可恢复 | 不得据文字自行重建并声称 faithful。 |
| Enhanced FFT coarse | **UNKNOWN：Eq. (11)–(13) 本体缺失** | PDF/page **UNKNOWN**; placeholders `content.md:262-272` | 只确认 QPSK suffix、FFT peak、zero-CFO peak `R_s/8`、range `±3R_s/8` | 可做概念原型，不能叫 exact reproduction。 |
| Enhanced `T_L` fine | **UNKNOWN：Eq. (14)–(18) 本体缺失** | PDF/page **UNKNOWN**; placeholders `content.md:283-306` | 只确认 cross-polarization A↔B block correlations、lag `T_L`、`N` blocks、`Δf_2` | 不能从 Wang Eq. (8)–(10) 复制索引；须恢复 canonical PDF 后再实现。 |
| Enhanced final compensation / MSE | **UNKNOWN：Eq. (19)–(21) 本体缺失** | PDF/page **UNKNOWN**; placeholders `content.md:306-310,369-375` | 正文仅给 final-sum 文字和 normalized-MSE 语义 | 不可给“精确式 + 页码”的审计结论。 |

### `B_L` range/variance identity

- **FACT**：coarse stage 的无模糊范围在 1 sps 下为 `[-R_s/2,+R_s/2]`，不由 `B_L` 缩放（`content.md:183`）。
- **FACT**：fine correlation 的相位跨越 `B_L T_s`；论文明确说 division by `B_L` 将 residual Gaussian phase-noise term 的影响降低 `B_L` 倍，同时把 estimation range 降低 `B_L` 倍（`content.md:208`）。
- **INFERENCE（由 principal angle）**：fine residual 的无模糊区间为 `[-R_s/(2B_L),+R_s/(2B_L)]`。这是实现所需的 wrap 边界，但不是当前 PDF 复核过的逐字公式。
- **UNKNOWN**：论文没有给出可直接编码的 closed-form variance；不能把“noise term 降 `B_L` 倍”改写为未经来源支持的 `1/B_L²` 总 MSE 定律，因为相关求和、AWGN、phase noise 与 cycle-slip 同时存在。

## Parameter provenance

| parameter | value/range | source pointer | role |
|---|---|---|---|
| Wang modulation / rate | PM 4-QAM and PM 16-QAM; 10 GBaud | `10.1109.../content.md:231,279,339` | target modulation formats and `T_s=0.1 ns` at 1 sps |
| Wang 320-symbol defaults | 4-QAM: `(B_N,B_L)=(16,20)`; 16-QAM: `(8,40)` | `content.md:299` | exact paper defaults; both satisfy `B_NB_L=320` |
| Wang 960-symbol defaults | 4-QAM: `(24,40)`; 16-QAM: `(16,60)` | `content.md:299` | longer-training comparison, not the 320 smoke default |
| Wang generic `B_L` demo | `B_L=20` in symbol-length study | `content.md:289` | Fig. 9 setting; does not make 20 universal optimum |
| Wang CFO | random `(-1.1,1.1) GHz` | `content.md:289,319,339` | injected truth distribution; scoring/oracle only |
| Wang repetitions | FOE/MSE: 800 per point; FS accuracy: 6400 per point | `content.md:257,319` | paper-scale averaging; smoke may use fewer only if it makes no performance claim |
| Wang normalized CFO MSE | `E[|(Δf_est−Δf)T_s|²]` | `content.md:279` | source metric; true `Δf` is evaluation-only |
| Wang MSE onset thresholds | 4-QAM `2.5e−7`; 16-QAM `6.25e−8` | `content.md:279` | BER begins to rise in paper setting; usable only as labeled scoring thresholds |
| Wang severe thresholds | 4-QAM `6.25e−6`; 16-QAM `2.25e−6` | `content.md:279` | severe BER degradation in paper setting |
| Wang FS threshold | paper discusses `0.2` or `0.3`; later system uses `0.2` | `content.md:257,339` | threshold-based early FS detection |
| Wang link / turbulence | 10 km; `C_n²=1e−16` weak, `1e−14 m^(−2/3)` strong; outer scale →∞, inner scale →0 | `content.md:241` | Fourier phase-screen FSO evaluation, not required for formula-only smoke |
| Wang coupling / aperture | mean coupling 67.3012% weak, 4.8395% strong; telescope aperture 0.2 m | `content.md:243` | received-power/turbulence burden |
| Wang lasers / receiver | Tx ECL linewidth 50 kHz; per-branch shared LO linewidth 50 kHz, 15 dBm; responsivity 0.8 A/W; shot+thermal noise | `content.md:231,243` | phase noise and receiver noise parameters |
| Wang diversity | 1/2/4/6 branches appear in final comparison | `content.md:375` | FS aligns branches; MRC occurs before FOE |
| Wang figure power anchors | 4-QAM CFO scan at −43 dBm; 16-QAM at −37 dBm | `content.md:309,319` | figure-specific settings, not universal receiver powers |
| Enhanced training object | PRBS prefix + cyclic-QPSK suffix; each small QPSK cycle is 16 symbols | `10.1364.../content.md:187-205` | different identity from Wang FSTS |
| Enhanced training length | 480 and 960 QPSK/FOE symbols; 480 selected as overhead/performance balance | `content.md:393-404,431-442` | exact PRBS-prefix contribution to “total joint TS” remains ambiguous without figure/PDF |
| Enhanced `T_L` evidence | at −45.12 dBm, second stage exceeds first after about 64 (N=480) / 80 (N=960); at −43.12 dBm after about 50 / 60; performance stabilizes near/above 80 | `content.md:404` | proves power/length dependence; not an exact legal action grid |
| Enhanced coarse range | `[-3R_s/8,+3R_s/8]` | `content.md:251-272,422` | FFT coarse estimator |
| Enhanced link / rate | 20 km, 10 Gbaud PM-QAM; 0.2 m aperture | `content.md:334-345` | simulation setting |
| Enhanced linewidth | scraped text says “80 K linewidth” | `content.md:336` | **UNKNOWN unit**; read-note interprets 80 kHz, but PDF is absent so this cannot carry an exact parameter claim |
| Enhanced repeats | FS 3200 per point; FOE/MSE typically 800 per point | `content.md:351,393,404,431` | averaging |
| Enhanced power anchors | −53/−36 dBm spectrum examples; `T_L` scans at −45.12/−43.12 dBm | `content.md:274-281,404` | condition points |
| Enhanced turbulence | `C_n²=1e−16` weak, `1e−14` strong in simulation; indoor experiment text gives `6e−11` and Tx 13 dBm | `content.md:442,466-470` | simulation and experiment must not be mixed |
| Enhanced MSE/BER threshold | QPSK text: sensitivity begins degrading beyond about `5e−6`, severe near `8e−6`; FEC `1.5e−3` | `content.md:371-375,431` | prose-only threshold; Eq. (21) body missing |

## Legal action space

### Wang 2023, 320 symbol-times

**FACT constraints**：`B_L` even，`B_N/2` even，且每极化 `B_NB_L=320`（结构见 `content.md:107`，默认闭合见 `content.md:299`）。

**INFERENCE — structurally admissible discrete set**：在不改变 320 symbol-time 的条件下，所有满足上述整除约束的 `(B_L,B_N)` 为：

| `B_L` action | `B_N=320/B_L` |
|---:|---:|
| 2 | 160 |
| 4 | 80 |
| 8 | 40 |
| 10 | 32 |
| 16 | 20 |
| 20 | 16 |
| 40 | 8 |
| 80 | 4 |

这只是公式/结构合法集合，不是论文逐点测试集合，也不证明极端值在数值上有用。当前 source-grounded reproduction defaults 只有：PM-4-QAM 用 `B_L=20`、PM-16-QAM 用 `B_L=40`。若 semantic smoke 需要最小多动作比较，`{20,40}` 是同时满足结构约束且均有论文默认出处的最窄集合；扩大到上表其余值必须明确标为 structural sweep，而非 paper-tested action。

每个 action 不是“把同一数组的 lag 参数换个数”而已：改变 `B_L` 时必须同步令 `B_N=320/B_L`，重新生成 X/Y block arrangement，并让 coarse/fine 的求和边界随 `B_LB_N/2` 与 `B_N/2` 改变。

### Enhanced 2024

**UNKNOWN**：无法从缺公式/缺 Fig. 2、Fig. 5 的本地材料恢复 `T_L` 的完整离散合法集合、`T_L` 与 480/960 训练长度的精确整除关系，或 PRBS prefix 是否计入该总数。只能确认 cycle `a` 长 16、A/B 块由多个 `a` 组成，以及正文报告的约 50/60/64/80 阈值。不得据此臆造 action grid。

## Deployable information boundary

### Fixed action can run from receiver information

对 Wang fixed `(B_N,B_L)`，在已知 `R_s/T_s` 和训练结构的前提下，以下均只需 receiver samples：

- FS：逐支路接收复样值与 FSTS 自共轭结构；Wang 甚至明确称该方案不像 conventional TS estimator 那样需要接收端备份完整 TS（`content.md:225`）。
- coarse FOE：FS/MRC/pol-demux 后的 X/Y TS samples 与固定索引。
- fine FOE：coarse estimate、其补偿后的 X/Y TS samples、固定 `B_L/B_N`。
- final compensation：`Δf_1+Δf_2` 与 sample index。

对 Enhanced，fixed `T_L` 的 conceptual operation 还需要 known PRBS 的 receiver-side differential template `ts'`、known cyclic-QPSK geometry、双偏振 samples 与 `R_s`；但在 Eq. (1)–(20) 恢复前不能声称已有 exact executable contract。

### Truth allowed only for scoring/oracle

以下不得进入 fixed estimator，也不得伪装成 receiver-visible condition：

- injected true CFO `Δf_true`；
- true frame start / per-branch delay；
- true modulation data bits（仅 BER scoring）；
- turbulence label/`C_n²`、true optical gain/phase-noise realization、noise realization；
- across-actions oracle winner、best `B_L`、oracle regret。

Receiver-visible energy/SNR proxy、correlation magnitude/peak sharpness可从 samples 估计，但是否用它们做 action selection不属于本审计；本报告不设计 controller。

### Computable scoring口径

对 trial `r` 定义 source-faithful normalized squared CFO error：

\[
q_r=\left|\left(\widehat{\Delta f}_r-\Delta f_r^{truth}\right)T_s\right|^2,
\qquad
\widehat{NMSE}=\frac1R\sum_{r=1}^R q_r.
\]

这与 Wang `content.md:279` 的 normalized MSE 一致；truth 只在 scoring 侧读取。

论文没有定义“FOE outage”。若 smoke 需要可计算的 outage，唯一诚实口径是明确标为 **INFERENCE / evaluation-only**：

\[
\widehat P_{out}(\tau)=\frac1R\sum_r \mathbf 1[q_r>\tau].
\]

可分别使用 Wang 的 BER-onset 阈值 `τ_onset={2.5e−7 (4-QAM), 6.25e−8 (16-QAM)}` 和 severe 阈值 `τ_severe={6.25e−6,2.25e−6}`。这不是论文命名的 outage，也不能在不同光功率/后续 CPE 设置间无校准迁移。

另应单独记录 range/cycle-slip failure：若 coarse residual `|Δf_true−Δf_1|≥R_s/(2B_L)`，fine principal-angle estimator可能产生 wrap；该事件可作为 formula-domain failure 计数，但同样是实现审计口径，不是论文原名指标。

## Existing-code identity gap

审计文件：`projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py`。

| requirement | existing file:line | gap | consequence |
|---|---|---|---|
| `B_N/B_L` 身份与 320 关系 | `frame_sync_fsts.py:8-10,58-68` | 注释把 `B_N` 说成“符号一段/每段符号数”，并保留“320=BN·BL? 或两段”的疑问；实际 `B_N` 是每极化完整 TS 的 block count，`N_TS=B_NB_L`。 | 参数身份尚未闭合，不能据现注释解释 action。 |
| 双偏振 FSTS structure | `:15-21,28,58-78` | API/返回值只有一个 `ts_template`；builder 仅生成 320 个独立随机 QPSK symbols，没有 X/Y、front/back conjugate symmetry、block/symbol interleave。 | Wang Eq. (7)–(10) 的调制相位消除条件不成立。 |
| action 改变结构 | `:15,58-78` | `bl` 在 sync function 中未使用；`bl`、`bn` 在 builder 中也未参与生成或 validation。 | sweep `B_L` 目前是 no-op，任何 action ranking 都无方法语义。 |
| faithful Wang FS metric | `:33-51` | 实现 `Σ seg·conj(ts)` 的 known-template matched correlation；论文 Eq. (1)–(2) 是共轭对称 TS 的 `C_m(d)` 与 energy-normalized `M_m(d)`。 | 现有峰是 template-correlation peak，不是 Wang FS timing metric。 |
| threshold FS | `:44-53` | 始终完整滑窗后 `argmax`，无 `M(d)>0.2/0.3` threshold path，亦无 energy normalization。 | 无法复现论文的 FS complexity/threshold identity。 |
| dual-pol coarse FOE | entire file; especially `:15-55` | 无 `R_X/R_Y` inputs，无 Eq. (7)，无 `Δf_1` output。 | 该文件不是 carrier FOE implementation。 |
| coarse compensation + fine `B_L` correlation | entire file | 无 CFO compensation、Eq. (8)–(10)、residual range/wrap handling。 | 不能测试 `B_L` precision/range tradeoff。 |
| final FOE | entire file | 无 Eq. (11)、全帧补偿或 CFO estimate。 | 无法计算 CFO MSE/outage。 |
| receiver chain position | `:15-55` | 输入是无 polarization dimension 的 independent branch arrays；无 branch phase correction、MRC、pol-demux boundary。 | 把 branch alignment、polarization structure、FOE stage 混为单一模板相关。 |
| exact-length candidate | `:38-42` | `N_rx==N_ts` 时 `max_offset==0`，代码直接返回 zero correlation；实际上 offset 0 是一个合法候选。 | 即使作为 matched-filter sandbox，exact-length smoke 也被错误短路。 |
| provenance-safe naming | `:1-10,16,26,36-49` | docstring/comments 把“跨极化共轭相关”写在单极化模板相关实现上。 | 可运行性会掩盖 identity mismatch，不能标为 Wang faithful/testbed-ready。 |

## Minimum faithful smoke

### Wang FOE-only semantic smoke（最小且可实现）

1. 以 1 sps 生成 **两个极化** 的 320-symbol-time FSTS；对每个 action 强制 `B_N=320/B_L`，并实现 front/back conjugate symmetry、X/Y adjacent-block interleave 与 within-block symbol interleave。
2. 注入双偏振共同 CFO；至少包含 AWGN 与可控 common/slow phase noise。固定 seeds，保存每 trial 的 true CFO 仅供 scorer。
3. semantic smoke 可把 frame start 设为 oracle-known、使用单个已对齐 branch，并跳过 optical front-end/MRC/pol-demux；但结果必须命名为 **FOE-only identity smoke**，不能声称完整 FSTS/FS 或 turbulence performance。
4. 严格按 Eq. (7) 求 `Δf_1`；用它补偿训练 samples；再按 Eq. (9)–(10) 形成 lag-`B_L` correlations，按 Eq. (8) 求 `Δf_2`，最后 Eq. (11) 合成。
5. 最窄 source-grounded action set 为 `{20,40}`；若用完整 structural set，必须在输出中标注只有 20/40 是 320-symbol paper defaults。
6. 每 action/condition 输出 `NMSE`、evaluation-only onset/severe outage、fine-range wrap count；oracle best action/差值只在 scorer 侧计算。

### 必须通过的 semantic checks

- noiseless、CFO 在 coarse range 内且 coarse residual 在每个 action 的 fine range 内时，`Δf_est` 应回收 true CFO 到数值容差；分别核对 coarse、fine、final 三个量。
- 在 `±R_s/(2B_L)` 附近测试 fine principal-angle wrap，确保 range 缩放确实随 action 改变。
- 改变 `B_L` 后，训练结构、`B_N`、pair indices 与 estimator divisor 都发生变化；检测 action no-op。
- 交换/破坏 X/Y interleave 后，测试应失败或显著退化，以证明算法确实依赖论文结构，而非普通 lag correlation。
- scorer 去掉 truth 输入后 estimator 输出不变，防止 leakage。

### 可安全简化

- FOE-only smoke 可用 ideal frame start、single aligned branch、unit amplitude、baseband AWGN/phase-noise model；可暂不实现 10 km phase screen、shot/thermal 分项、optical coupling、BER payload。
- smoke repeats 可少于论文 800 次以验证公式与接口，但不得据此作性能或 condition-ranking结论。
- 可先只跑 4-QAM/QPSK training constellation，因为 Wang 的 FOE 依赖训练结构而非 payload mapping；若报告 PM-16-QAM default，则必须用 `(8,40)` 并分别标明 payload format。

### 不可简化

- 不可用单极化 template correlation 冒充 Wang coarse/fine FOE。
- 不可用独立随机 320-QPSK 序列替代双偏振交错共轭 FSTS。
- 不可让 `B_L` 只作数组 lag 标签；它同时决定 `B_N`、training construction、sum bounds、fine divisor 和 residual range。
- 不可在 coarse compensation 前运行 fine estimator。
- 不可把 true CFO、true turbulence label 或 oracle best action喂给 estimator。
- 不可在 PDF/公式恢复前实现 Enhanced Eq. (1)–(21) 并称 faithful；最多保留 prose-level prototype，且必须与 Wang formula smoke 分开命名。

若要把 smoke 扩为“完整 FSTS smoke”，还必须另加 Wang Eq. (1)–(2) 的每支路 FS、支路 delay alignment、phase correction/MRC/pol-demux stage boundary；existing matched filter 不满足该门。

## FACT / INFERENCE / UNKNOWN

### FACT

- Wang `B_L` 是 block length，也是 fine estimator 的 cross-block symbol lag；larger `B_L` 同时改善 phase-noise suppression、缩小 fine range。
- Wang 320-symbol defaults 随 modulation 改变：PM-4-QAM 为 20，PM-16-QAM 为 40；它不是一个 universal default。
- Wang coarse 和 fine 都需要 X/Y 双偏振结构；fine 必须使用 coarse-compensated samples。
- Enhanced 用 PRBS differential FS + cyclic-QPSK FFT coarse + `T_L` cross-polarization fine；它的 coarse estimator 与 Wang Eq. (7) 不同。
- Enhanced 正文显示 `T_L` 的有益门槛随 received power 与 total length 改变。
- 现有 `frame_sync_fsts.py` 只做单模板 matched correlation，`B_L/B_N` 是 no-op，没有任何 CFO estimate。

### INFERENCE

- Wang 320-symbol structurally admissible action set是 `{2,4,8,10,16,20,40,80}`；这是从整除与偶数约束推得，不是论文测试点清单。
- Wang fine residual unambiguous range 为 `±R_s/(2B_L)`；这是从 principal-angle estimator 与原文“range reduced by `B_L`”推得。
- 用 paper MSE thresholds 定义 per-trial empirical outage 是 evaluation-only operationalization，不是论文原指标命名。
- ideal-frame/single-branch baseband模型足以做 FOE formula identity smoke，但不能外推 FS、MRC、turbulence 或 BER/sensitivity。

### UNKNOWN

- 两篇论文所有 printed PDF page numbers；canonical PDFs 缺失。
- Enhanced Eq. (1)–(21) 的精确公式、索引、conjugation/sign convention；本地 `content.md` 丢失公式本体。
- Enhanced `T_L` 的完整 legal discrete grid，以及 480/960 是否包含 PRBS prefix 的精确 accounting。
- Enhanced linewidth 的确切单位；scraped HTML 是“80 K”，既有 read-note 的 80 kHz 解释未经 PDF 复核。
- Wang Fig. 10 的完整 sweep ticks/每个 power 条件及每个点数值；只有默认最优结构与文字趋势可核。
- 任何 receiver-visible condition 内真实 `B_L` ranking crossover、oracle headroom 或 conditioned lookup 胜负；本审计不作该判断。

## Blockers

1. T011 要求的两份 canonical PDF 在精确路径均缺失；因此不能提供 page+equation 双证据，也不能视觉核对公式排版、Fig. 1/Fig. 5 结构和 sweep axes。
2. Enhanced `content.md` 对 21 个公式全部只留下编号，占位文字不足以无歧义恢复 Eq. (1)–(20)；按 T011 纪律不能自行重建。
3. 在不进行 web search、也不改共享论文库的边界内，没有合法方式补齐上述材料。

因此本 worker-log 可支持 Wang formula-level semantic smoke 的受限实现合同与现有代码 identity-gap 判定，但不能把 Enhanced 2024 标为 exact formula reproduction，也不能把整份审计状态升级为 PASS。
