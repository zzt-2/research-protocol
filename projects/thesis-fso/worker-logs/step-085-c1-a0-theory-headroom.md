# Step 085 — C1 Step 4a A0 理论 headroom / 物理 factorization

> 2026-08-10 | T039 / D009 / CP010 | `THEORETICAL_BOUND`
> 边界：fresh 本地源码/全文分析；未运行 Monte Carlo、仿真、编码器或译码器，未写代码，未改中央 owner，未触碰 p05。

## 0. 控制与结论先行

- `topic-index.md` 的 epoch 10 / CP010 只允许 A0、source audit 与 theoretical bound；adapter、defect smoke、MVE、科学实验和论文声称均禁止。
- `projects/thesis-fso/master-state.md:38-47` 显示 coded decoder-feedback Step 3/3.5 已完成、Step 4a A0 正在进行；本任务没有跨 Step。
- **理论 verdict**：square-16QAM 下，一个帧内单次非零 symmetry slip 对任何单一 global rotation 都留下精确的无噪声结构残差。若 boundary 前占比为 `alpha`，理想 global B1 的最小残余 `SER=min(alpha,1-alpha)`，均匀 Gray-16QAM 的 coded-label BER 为 `0.5 min(alpha,1-alpha)`；知道 boundary 和 jump 的 local truth oracle O1 为 0。
- **interleaver verdict**：`PER_SEGMENT_DECODER_LOCALIZATION_NOT_ESTABLISHED / FAIL_CLOSED`。P08-R2 的 Qm=4 output interleaver 把连续 on-air 符号段在单个 LDPC component 内拆成四个相隔 384 bit 的条带；永久 suffix slip 还会触及 boundary codeword 及全部后续 codeword。不能把连续 slip 直接解释为一个连续 decoder segment。
- **physical verdict**：`FACTORIZABLE_ONLY_AS_ORTHOGONAL_SYNTHETIC_STRESS / FSO_OCCURRENCE_UNRESOLVED`。JLT 2020 提供 turbulence/AO/residual-CFO 场景，但未注入离散 slip，且明确不讨论发射激光 phase noise；OFC 2014 / ICTON 2016 的离散 slip 是 fiber/QPSK stress model，不能移植成“FSO turbulence 导致该 slip”的因果事实。
- 因此本任务不是 A0 Go：`UNCODED_STRUCTURAL_HEADROOM_CONFIRMED / CODED_FER_HEADROOM_UNKNOWN / NO_METHOD_SIGNAL`。

## 1. Fresh 源码身份

### 1.1 实际 modulation / Gray mapping

P08-R2 复用的 mapper 不是 QPSK，而是单位平均功率 square Gray-16QAM：

- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08_coded_chain.py:46-71`：I/Q 两轴均使用 `00->-3, 01->-1, 11->+1, 10->+3`，符号除以 `sqrt(10)`；标签顺序为 `[b0,b1,b2,b3]`。
- 同文件 `:77-105`：每四 bit reshape 为一个符号，max-log demapper 也按同一四 bit 顺序输出。
- `projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:89-113,124-160`：`k=1024,n=1536,Qm=4`，`LDPC5GEncoder(...,num_bits_per_symbol=4)`，encoder 输出定义为 on-air/interleaved order。
- `p08r_chain.py:272-316`：每 polarization 有多个 codeword；每个 codeword 编码后保持二维 `(n_cw,1536)`，随后 `reshape(-1)` 并按每四 bit 调制，故每 codeword 恰为 `1536/4=384` 个连续 on-air symbols。

### 1.2 实际 output interleaver

本机 Sionna 2.0.1 源码：

`C:/Users/zzt/scoop/apps/python311/current/Lib/site-packages/sionna/phy/fec/ldpc/encoding.py`

- `:172-179`：只要给 `num_bits_per_symbol`，就生成并注册 `out_int/out_int_inv`。
- `:303-344`：`perm_seq[i+j*Qm] = i*(n/Qm)+j`。
- `:791-796`：实际 encoder 输出为 `c_out[..., self._out_int]`。

代入 `n=1536,Qm=4,n/Qm=384`，on-air symbol `j` 的四 bit 不是原 rate-matched 序列中的相邻四 bit，而是：

```text
on-air positions 4j+i  <-  rate-matched positions i*384+j,  i=0,1,2,3
symbol j              <-  {j, 384+j, 768+j, 1152+j}
```

这一定义来自执行源码，不依赖旧 receipt 的文字描述。

### 1.3 reference M / B1 的 whole-frame 假设

- `papers/arxiv/2511.21340/content.md:105-116` 明确构造 `C` 个 constellation phase candidates，经 parallel demodulator/deinterleaver/decoder 形成 whole-observation model evidence，并在“frame-wise constant phase ambiguity”假设下只选一个 global phase。
- `papers/doi/10.1109_tsp.2006.874844/content.md:1409-1413,1467,1705` 对每个 phase/delay hypothesis 解整包、比较 decoder metric，再把剩余 decoding iterations 只给单一估计 hypothesis。

因此本文把 baseline ladder 的 B1 明确定义为：**在冻结的整帧上，只允许选择一个 constellation-symmetry rotation，随后整帧按该 rotation 解调/译码**。这一定义不包含 boundary 输出或分段 action。

## 2. 有限 symmetry mapping 表

令两轴 Gray 标签各为二 bit：`a=(b0,b1)` 表示 I，`b=(b2,b3)` 表示 Q。对轴标签定义

```text
neg(x0,x1) = (x0 xor 1, x1)
```

因为对上述 Gray 轴，坐标取负只翻转 sign bit。square-16QAM 的四个 symmetry rotations 为：

| 相对 rotation | label 变换 `(a,b)->` | symbol fixed point | 16 点 Hamming 距离计数 | 每错符号平均 bit flips | 均匀 bit BER |
|---|---|---:|---|---:|---:|
| `0` | `(a,b)` | 16/16 | `d=0:16` | 0 | 0 |
| `+pi/2` | `(neg(b),a)` | 0/16 | `d=1:8, d=3:8` | 2 | 1/2 |
| `pi` | `(neg(a),neg(b))` | 0/16 | `d=2:16` | 2 | 1/2 |
| `3pi/2` | `(b,neg(a))` | 0/16 | `d=1:8, d=3:8` | 2 | 1/2 |

这张表是对源码 mapping 的有限代数枚举；没有使用随机样本。结论只要求 16 个 constellation labels 等概，不要求 uncoded payload truth 进入 deployable path。

## 3. 单 jump 的解析 headroom

### 3.1 定义与推导

设 payload 共 `N` symbols，jump 前占 `alpha N`，jump 后占 `(1-alpha)N`，`0<alpha<1`；jump 为 `k*pi/2, k in {1,2,3}`。以前段 orientation 为 0、后段为 `k`。对任意单一 global correction `q`，无噪声 symbol-error fraction 为

```text
SER_global(q)
  = alpha * 1[q != 0]
  + (1-alpha) * 1[q != -k mod 4].
```

只有两种有意义的 global choice：对齐前段或对齐后段；其他两种让两段都错。因此

```text
SER_B1_star(alpha) = min(alpha, 1-alpha)
BERlabel_B1_star(alpha) = 0.5 * min(alpha, 1-alpha)
```

其中 `B1_star` 是 B1 在知道“应选哪个 global candidate”时仍无法突破的结构下界；实际 decoder-selected B1 只能等于或差于该值。

O1 知道 true boundary 与 jump，仅对后段乘 `exp(-j k*pi/2)`，故

```text
SER_O1(alpha)=0,  BERlabel_O1(alpha)=0.
```

这只是 noiseless/local-truth action 的 oracle 上界，不是 deployable 性能。

### 3.2 B0 / B1 / O1 趋势与排序

把 B0 定义为 CPR 在 jump 前 orientation 已正确、jump 后不 retry 的普通链，则

```text
SER_B0(alpha)=1-alpha
BERlabel_B0(alpha)=0.5(1-alpha).
```

| boundary `alpha` | B0 residual SER | ideal B1 residual SER | O1 residual SER | 结构排序 |
|---:|---:|---:|---:|---|
| `alpha<0.5` | `1-alpha` | `alpha` | 0 | `O1 < B1 < B0` |
| `alpha=0.5` | 0.5 | 0.5 | 0 | `O1 < B1 = B0`；B1 global tie |
| `alpha>0.5` | `1-alpha` | `1-alpha` | 0 | `O1 < B1 = B0`（理想选择前段） |

- B1–O1 的最大 structural headroom 在中央 boundary：`0.5 SER / 0.25 coded-label BER` absolute；靠近帧端点趋于 0。
- B0–O1 随 suffix 长度单调增加；B1 因能翻转 whole-frame orientation，曲线关于 `alpha=0.5` 对称。
- 这些是 defect-frame、pre-FEC hard-label 数字，不是平均链路 BER、post-FEC BER、FER、goodput 或 dB 增益。

### 3.3 FEC 为什么不能由该 bound 外推

1. LDPC decoder看到的是 soft LLR，不是表中的 noiseless hard label；噪声、LLR magnitude 与 decoder dynamics会改变结果。
2. 同样的错误数因 output interleaver 和 Tanner graph位置不同，可能被纠正、形成 trapping pattern，或让整 codeword fail；FER不是 uncoded error fraction 的线性函数。
3. B1 对齐前段或后段会把错误落在不同 codeword/bit positions；即便 hard-label BER相同，FER排序也未必相同。
4. TSP 2006 `content.md:895-897` 已提醒某些 code/mapping 的 rotational symmetry 会产生无信息或不可辨识消息；P08-R2 的 5G-NR LDPC + 16QAM 是否可辨识尚未被本任务验证。

所以本解析结果证明“global action 存在结构性 uncoded residual”，但**不证明 O1 会带来 coded gain，也不证明 decoder metric能定位/选择**。

## 4. Interleaver 与多 codeword 的致命候选审查

### 4.1 单 codeword 内的扩散

若一个 on-air contiguous symbol interval 为 `[s,e)`，`0<=s<e<=384`，inverse output-interleaver 后受影响的 rate-matched positions 为

```text
[s,e)
union [384+s,384+e)
union [768+s,768+e)
union [1152+s,1152+e).
```

因此它不是 decoder input 上的一个连续段，而是四个条带；进入 LDPC Tanner graph 后又全局耦合。任何“按 decoder bit index 滑窗就能看到一个 contiguous burst”的论证均被源码否定。

### 4.2 多 codeword

P08-R2 先保持 codeword 连续、再 flatten；output interleaver **不跨 codeword**。data-symbol index `j` 的 component 是 `floor(j/384)`。但一次真正的 cycle slip 是 orientation state jump，后续保持新 stable point（ICTON 2016 `content.md:21-23`），所以 boundary 落在 component `c` 时：

- component `c` 的 suffix 被污染，并在该 component 内拆成四条；
- `c+1 ... n_cw-1` 的全部 symbols 也处于新 orientation；
- 若按 polarization 独立构造，需要另行冻结 slip 是否共享，不得默认双偏振同 boundary。

所以 per-codeword syndrome/CRC 最多提供粗粒度且不可靠的 384-symbol bin：后续多个 component 可能一起 fail，而 boundary component 也可能被 FEC 纠正；“第一个失败 component=boundary”没有理论保证。

### 4.3 Verdict 与可保留部分

`FAIL_CLOSED` 的是**自然 per-segment decoder localization**假设，不是所有 symbol-domain local search：

- 仍可能合法：在 on-air symbol domain 枚举 boundary candidate，按候选只重算受影响 LLR，然后对每个 touched component 提供完整 1536 LLR 并完整 restart decode，以 aggregate receiver-visible metric评分。
- 尚不合法：只译 suffix bits、把 callback/Tanner index当 on-air index、沿用 changed-LLR 前的 decoder state、或仅凭哪个 codeword fail 推断 exact boundary。
- 如果后续 source/BOM 证明必须靠上述不合法简化才能在 3–7 日预算闭合，则 C1 应 Kill，而不是把 adapter gap包装成方法。

## 5. 物理因素必须正交 factorization

### 5.1 JLT 2020 能支持什么

本地全文 `papers/doi/10.1109_jlt.2020.3003561/content.md`：

| factor | 本地来源事实 | transfer ceiling |
|---|---|---|
| LEO/FSO turbulence | `:37-57`：1550 nm，`C0=1e-13 m^-2/3`，`vRMS=20 m/s`，`vG=10 m/s`，`vT=20 m/s`，`r0=0.039 m`，`L0=5 m`，scintillation index `0.684`，elevation `20 deg`，satellite transverse speed `6.5 km/s`，Rx aperture `0.5 m`，35 phase screens | 只属于该 BPSK LEO downlink/TURANDOT scenario；没有 raw time series，不能宣称精确复现，也不能直接替换为 P08 Gamma-Gamma参数 |
| AO | `:59`：91 Zernike modes / 12 radial orders，5 kHz，2-frame delay，average flux penalty `-4.5 dB` | WFS noise 被忽略；只提供 coupled-amplitude/phase envelope，不是 slip model |
| turbulent phase | `:96`：coherence time约 1 ms，远慢于 10 Gbaud；`:194-196` 在其 DPLL设置下影响可忽略 | 对“turbulence直接制造离散 symmetry slip”是负面/限制证据，不是正面发生率 |
| residual CFO / DPLL | `:106`：coarse compensation后用最大 constant `100 MHz`；`:144-155`：`omega_n=9.3 MHz, xi=1/sqrt(2), BLT=0.0005, BL=5 MHz`；`:162,186`：100 MHz约1.4 ms lock | 仅 DPLL/BPSK/ideal timing；不能当 P08-R2 的现成 CPR，也不能把 CFO当 discrete slip |
| fading effect | `:167,190`：无幅变时约 `-9 dB` 以下失锁；fading把 critical mean-SNR提高约 5 dB；`:200` 报告 BER penalty 2.3 dB at `1e-4` | 这是 published end-to-end result，不是本任务结果；不能移植成 16QAM/FEC增益 |
| laser phase noise | `:31` 明确不讨论 on-board laser phase noise | 不能从该论文取得 linewidth或 laser-driven slip rate |

### 5.2 OFC / ICTON 能支持什么

- OFC 2014 `papers/doi/10.1364_ofc.2014.m3a.3/content.md:27-31` 用 QPSK V&V 后的 cycle-slip Markov state；`:129-135` 的发生率来自 5230-km fiber实验，simulation令 slip rate为 pre-FEC BER 的 1/10，LDPC length 38400，并特意**不用 interleaver**做 worst case。它支持“discrete slip stress会破坏FEC、interleaver会改变结果”，不支持 FSO occurrence rate或 P08 16QAM transfer。
- ICTON 2016 `papers/doi/10.1109_icton.2016.7550341/content.md:21-27` 把 sudden jump 物理动机指向 fiber XPM；`:57-65` 的模拟是 perfect equalization/CPR except uniformly distributed CS、QPSK、AWGN、regular LDPC length 20000、rate 0.85、`P_CS=1e-3`。该 `P_CS` 只可作为 fiber/QPSK stress source，不能当 LEO-FSO参数。

**关键分离**：JLT turbulence/AO/CFO 是 FSO propagation/tracking axis；OFC/ICTON discrete slip 是 post-CPR state-error axis。把两者组合只能标为 `[外推] orthogonal stress construction`，不得写成“JLT turbulence导致 ICTON `P_CS=1e-3`”。

### 5.3 最小 factorized testbed 草案（未实现、未授权）

| axis | 最小取值/动作 | 来源类型 | 进入结论的上限 |
|---|---|---|---|
| codec/mapping | P08-R2 `1024/1536`, Qm=4 Gray-16QAM, 384 symbols/CW, exact out_int | `[实证：源码]` | 可作为 identity；不恢复旧P08科学结果 |
| physical envelope | JLT scenario表 + AO配置；无 raw series时只可做“source-matched family”，不能声称 exact replication | `[实证：论文场景]`；移植到P08为`[外推]` | 只测 robustness slice，不证明 occurrence |
| residual CFO | constant 0/100 MHz，加粗估计前提；若无 task-matched CPR caller则标 blocked | `[实证：JLT]`；16QAM transfer为`[外推]` | 与 slip独立，不把失锁自动标 slip |
| slip operator | post-CPR/equalized symbols在 boundary 后乘 `exp(j k*pi/2)`, `k=1,2,3` | jump set=`[论证：实际16QAM symmetry]`；发生机制=`[外推]` | 只作可证伪 synthetic defect，不作自然发生率 |
| boundary | 至少中心、codeword边界附近、codeword内部；具体 grid为预注册设计值而非文献参数 | `[论证/建议]` | 只能支持执行 cells |
| comparators | B0、single-global B1、strongest receiver-only B2、local-truth O1；same frozen rx/LLR/decoder budget账本 | `[论证：公平合同]` | oracle只作Kill/headroom，不作Go |
| decoder | touched-CW完整 restart；记录每个candidate触及的CW数、decode calls、iterations | `[实证：源码约束]` | 未验证 callback/state reuse前禁止复用旧state |

最小 causal order 应是：`physical envelope/CFO -> frozen conventional front-end output -> orthogonal residual-slip operator -> B0/B1/B2/C1 action -> full touched-CW decode -> action冻结后truth score`。若没有真实 CPR caller，必须把它命名为 residual-slip fixture，不能冒充 end-to-end natural cycle-slip reproduction。

## 6. A0 §1 来源标签、FR-21 与 Kill 条件

### 6.1 来源标签

| 声称 | 标签 | 限制 |
|---|---|---|
| P08-R2 是 Gray-16QAM、Qm=4 output interleaver、384 symbols/CW | `[实证：执行源码]` | 工程 identity，不是科学性能 |
| `SER_B1*=min(alpha,1-alpha)`、label-BER=`0.5min(...)`、O1=0 | `[论证]` | noiseless、均匀16QAM、单永久jump、ideal hypothesis choice |
| JLT turbulence/AO/CFO 数字和其 DPLL结果 | `[实证：论文该场景]` | BPSK/ideal timing/无laser PN，不能直接移植 |
| 用 JLT envelope + OFC/ICTON discrete slip + P08 codec | `[外推]` | 只可作 factorized stress；不得成为 Go 核心论据 |
| OFC/ICTON 的 post-FEC/iteration/slip-rate数字 | `[实证：各自fiber/QPSK slice]` | 不给本项目 coded增益或FSO发生率 |

### 6.2 FR-21 适用性

FR-21 **部分适用**：local truth correction 的 structural headroom 可解析，故必须先看该上界再决定是否值得 defect smoke。但框架的 `<0.5 dB` Kill阈值不能直接套在本任务的 SER/label-BER上；没有 sourced boundary distribution、noise/LLR与FEC response，就不能把 `0.25` label-BER peak换算成 dB或FER/goodput。

合规用法：

1. 若在预注册、物理支持的 scored slice 中 `O1` 相对 tuned B1/B2 的 coded gain低于既定 practical threshold，则 Kill；
2. 若只有靠 truth boundary才能得到好结果，而 receiver-visible boundary metric不承重，则 Kill；
3. `O1>B1` 只说明有上界，不是 Go，不能替代 conventional comparator。

### 6.3 明确 Kill / blocker 条件

1. **Interleaver/localization Kill**：receiver-visible metric只能给 per-CW failure，无法在 384-symbol component内把 exact boundary缩到足以产生稳定增益；或必须把 decoder bit index错当 on-air时间index。
2. **Coded-headroom Kill**：完整 P08 decoder下 O1与 tuned B1/B2 的 FER/post-BER/goodput差距为零或低于预冻结 practical threshold，即使 uncoded formula非零。
3. **Conventional absorption Kill**：CSSC/CS-DC/PAPU/OFC2017-like 或 tuned global retry在同信息、同pilot/latency/decode预算下达到 O1 的 90/95%覆盖门。
4. **Physical-occurrence Kill/Pivot**：本地可支持的 coherent-FSO slice没有 single within-frame symmetry slip，或只能用与JLT矛盾的虚构 turbulence->slip因果才能产生缺陷。
5. **Information-boundary Kill**：触发/边界/action需要 true phase、true slip boundary、TX payload、final correctness或oracle best label。
6. **Budget Kill**：正确实现必须跨全部后续 codewords做无界 hypothesis/decode，或依赖 changed-LLR old-state reuse/custom decoder内核，导致真实预算超过 D001 的 3–7日。
7. **Noiseless identity Kill**：O1无法在所有 `k,alpha` 恢复0 error，说明 prefix/CW/out_int/rotation slice错位；先修 fixture，不得解释成科学结果。

## 7. TL-20 理论异常锚点

后续若另立决策授权 smoke，至少冻结以下锚点：

1. **No-slip / endpoint**：无 jump时 B0=B1=O1=0，C1必须 no-op；任何 action或非零error是false trigger/identity bug。
2. **Central boundary floor**：noiseless `alpha=0.5` 时，任何真正 single-global B1 都不得低于 `SER=0.5,label-BER=0.25`；若更低，说明意外用了local action/truth或metric口径错误。
3. **O1 exactness**：所有 `k in {1,2,3}` 与任意合法 boundary，O1必须为0；非零优先查 rotation sign、prefix offset、CW split与double deinterleave。
4. **Rotation-class mapping**：noiseless uniform labels下三个非零 rotation 的 pre-FEC平均 BER都应为0.5；`pi/2`/`3pi/2` 为8个1-bit+8个3-bit，`pi`为16个2-bit。偏离先查mapper/demapper identity。
5. **B1 symmetry**：ideal B1 structural curve须满足 `E(alpha)=E(1-alpha)`，并在0.5达峰。实际 decoder curve若显著不对称，必须按 boundary相对CW/interleaver/prefix位置分层，不能直接归因方法。
6. **Ideal ordering**：noiseless、正确 global selection时 `O1 <= B1 <= B0`；若 deployable B1比B0差，说明decoder evidence selection本身失败，这可能是C1 problem evidence，也可能是code/mapping不可辨识，必须分离。

## 8. Terminal

```text
A0_THEORY_HEADROOM_COMPLETE
theory = UNCODED_STRUCTURAL_HEADROOM_CONFIRMED
interleaver = PER_SEGMENT_DECODER_LOCALIZATION_NOT_ESTABLISHED / FAIL_CLOSED
physical = FACTORIZABLE_AS_ORTHOGONAL_SYNTHETIC_STRESS_ONLY
fsoccurrence = UNRESOLVED
coded_FER_headroom = UNRESOLVED
FR21 = PARTIALLY_APPLICABLE / KILL_ONLY / NOT_GO
mission_method_delta = NONE
```

本任务给出的最窄结论是：**global one-shot B1 在中部 single-slip boundary 上有严格的 uncoded结构残差，但实际 interleaver使 decoder evidence 的时间局部性显著变差；在 receiver-visible boundary observability、coded O1 headroom、B2 absorption 与合法 FSO occurrence闭合前，不得进入 Go 或把解析上界写成方法增益。**

## 9. Protection / final fresh check

- output：本文件存在，268 行；required-terminal grep `5/5 PASS`；git状态仅为本文件 `??`。
- staging：`EMPTY`。
- protected p05 SHA256 与任务启动值 `4/4 MATCH`：

```text
p05_run.log   7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11
p05_run2.log  735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B
p05_run3.log  C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D
p05_run4.log  95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE
```

- 唯一写入：`projects/thesis-fso/worker-logs/step-085-c1-a0-theory-headroom.md`；未执行 add/commit/push。
