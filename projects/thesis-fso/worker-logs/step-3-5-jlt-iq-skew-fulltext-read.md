# Step 3.5 JLT 2025 IQ-skew 用户全文 acquire→read

> 日期：2026-08-06
> 任务：T013
> 结论：`NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`

## Identity 与 provenance

- 标题：*Preamble Design for Online IQ-Skew Estimation in Upstream 400G Coherent TFDM-PON*。
- DOI：`10.1109/JLT.2025.3581618`；JLT 43(17), 2025, pp. 8040–8049。
- 用户提供 PDF：1,945,015 bytes，10 页；PDF SHA256=
  `0a5c8865d06fd77033e77eb082f65db6eba3520de5986722d1d5db63fb32311d`。
- canonical content：344 行，SHA256=
  `56dd39ff40ead11d42a6524c94498aaf75c7e895dd80467721dbf1200c9a93b1`。
- metadata/正文题名 overlap=`1.0`，title/DOI/作者/出版信息一致，identity gate=`PASS`。
- PDF 10 页均经 Poppler 渲染目视检查；无缺页、裁切或图表不可读。

## Information/action/output/timing

Fig. 2 与 §II-A 给出的 DSP 链为：

`TS-A frame detection → Tx/Rx IQ-skew estimation → one-tap SOP estimation → timing recovery → FOE →`
`TS-B frame synchronization → TS-B CMA/channel estimation → TS-C pilot CPR`。

TS-A 的实部周期 `[1,-1]`、虚部周期 `[1,1,-1,-1]` 形成 `f_s/2`、`f_s/4` 两音（Eq. 1；
`content.md:81-87`）。Tx/Rx IQ-skew 由 Eq. 7–15 建模，再由 Eq. 16–23 的 tone phase/Godard phase
detector 分别输出 `τ_Tx,i` 和 `τ_Rx`（`content.md:113-189`）。这些公式不包含 frame index、timing-
recovery fractional τ 与 CFO 的共同 likelihood/objective。

| 字段 | 本文事实 | 与 Q1 exact contract 的关系 |
|---|---|---|
| receiver-visible input | burst samples + receiver-known TS-A/B/C | 部分相邻 |
| preamble/resource | TS-A 被多模块复用，TS-B/TS-C另有职责 | shared resource，不等于 joint objective |
| frame output | TS-A frame detection；TS-B frame synchronization | 有 frame 类动作 |
| fractional timing output | 独立 timing recovery；正文无连续 fractional-τ 联合公式 | 不匹配 exact output contract |
| CFO output | 独立 FOE 模块 | 有 CFO 动作但未耦合 |
| extra outputs | IQ-skew、SOP、channel、CPR | 额外独立动作 |
| estimator coupling | 无单一 `(frame, fractional τ, CFO)` objective/search | 不匹配 |
| execution order | 明确的顺序模块链 | 属 cheap sequential comparator |
| modality | coherent fiber TFDM-PON | 非 RRC coherent FSO |

## 实验与完备性

- 4×12.5-GBaud 16QAM、400G；120-GSa/s DAC、256-GSa/s ADC、50-km SSMF。
- TS-A 非零部分每偏振/时隙 512 symbols，总 1024 symbols、81.92 ns；TS-B 256 symbols；总 preamble
  1280 symbols、102.4 ns；TS-C 每 48 payload symbols 一个，overhead=2.08%。
- 三种分配：单 ONU 四子载波、双 ONU 各二、3+1 非对称。
- skew=`−15…+15 ps`；10 次重复、间隔 30 s；估计误差 `±0.3 ps`。
- 每子载波 ROP=`−35…−31 dBm`；补偿后总灵敏度 `−28 dBm`、每子载波 `−34 dBm`；补偿
  0.6/1.2/1.8 ps skew 的灵敏度增益约 0.5/2.0/4.5 dB。
- baseline：无外部端到端算法 baseline；只有 TS-A 长度、补偿前后、三种分配与功率失衡内部对照。
- 统计：10 次重复；无 error bar/置信区间/统计检验。无复杂度分析、代码或数据仓库。
- VVUQ：V=2（公式与实验链可追）；Validation=2（三场景真实实验但限 fiber PON）；U=1（无不确定度报告）。

## M/C/A 与 verdict

- M：专用 IQ-skew training / 传统分散 burst DSP。
- C：多 ONU、功率失衡的 coherent TFDM-PON upstream。
- A：专用 TS 增加开销，多 ONU 叠加与功率失衡使传统 IQ-skew 估计不可靠。
- 方法产出：共享 TS-A 的 online IQ-skew estimator + 顺序 burst DSP chain。

本文占用“共享 preamble、零额外 IQ-skew overhead”的包装和 comparator 形态，但不占用 Q1 的单一
joint `(frame, fractional τ, CFO)` estimator。因此最终 verdict 为：

`NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`。

对 cheap comparator 的影响：后续 Q1 如进入可行性讨论，必须显式覆盖本文的 shared-preamble 顺序链，
不能只对比彼此独立、未复用 training resource 的小模块。

## 边界

本任务只消解 JLT 2025 全文 blocker；JOCN 2026 仍无全文。未修改 canonical，未进入 Step 4a、实现或仿真。
