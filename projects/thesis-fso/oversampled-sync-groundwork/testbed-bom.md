# 过采样相干同步前端 testbed 静态能力 BOM

> 审计日期：2026-08-06
> 代码快照：`0ac0119c4982b539c322b79773c563cafdbbd9a6`
> 审计方式：只读源码与静态 `rg`；未运行仿真/测试，未访问 Web
> 审计范围：`projects/simulation/common/`、`projects/simulation/explore/b3-joint-estimation/`、B7 Gardner sandbox、相关 waveform/frame/fading sandbox 与现有 tests

## 1. 冻结边界与结论

本 BOM 只回答“现有代码离新 testbed 还有多少工程距离”，不做方法 claim，也不进入 MVE。专题冻结的研究对象明确包含 RRC、至少 2 sps、fractional timing、SCO/drift、frame offset、CFO、Wiener phase noise 与 Gamma-Gamma fading；当前范围只允许静态估工，禁止实现和仿真（`.sessions/2026-08-06-oversampled-coherent-sync-groundwork/topic-index.md:14-36`）。最终问题可以只保留经后续证据支持的 impairment 子集，不要求现在把全部损伤绑定成一个方法（同文件 `:47-53`）。

**总判断：完整覆盖本 BOM 的新 testbed 明显超过约 5 个工作日。** 逐项串行加总约 **18.5 人日**；把 waveform、损伤注入和指标/runner 的重叠工作合并后，保守交付仍为 **11–14 个工作日（1 人）**，且这还不含 Step 2/3 后对具体 2019+ baseline 的论文忠实复现。这个 full-object 数字用于能力上界审计，**不能单独触发 `TESTBED_SCOPE_EXCESSIVE`**：用户的停止条件同时要求“旧 caller 不支持”+“新增 testbed 实际要重建完整通信平台”+“工期明显超过约 5 日”。专题又明确不要求全部 impairment 同时进入最终问题，因此还必须审查候选特定的最小工程切片，见 §5。

分类含义：

- `READY`：接口和语义可直接用于新 testbed，只需接入验证。
- `SMALL_ADAPTER`：核心算子已有，需提取/统一参数、补兼容层与针对性验证。
- `NEW_INFRASTRUCTURE`：缺少新 testbed 所需的状态、truth、生命周期或端到端接口；即使局部公式已有，也不能靠直接调用闭合。
- `EXTERNAL_BLOCKED`：必须等待外部代码/全文/规范才能继续。本次工程层审计没有此类项；baseline 的学术合法性仍由后续 Groundwork 取证，不在本 BOM 中偷判。

## 2. 逐项能力审计

工期单位为人日，写成“开发 + 验证”。验证包含确定性单元测试、identity/no-impairment、已知偏移恢复、配对一致性和小规模端到端回归；不包含正式 MVE 跑数。

| 能力 | 分类 | 现有证据（file:line） | 新 testbed 缺口 | 保守工期 |
|---|---|---|---|---:|
| 统一 waveform/timebase/frame contract（交叉项） | `NEW_INFRASTRUCTURE` | 旧 generator 在 `Ns` 个符号上直接生成 `tx/h/phi/noise`，返回数组均为符号率长度：`projects/simulation/common/_channel.py:57-94`；现有共享接口只导出 symbol-rate channel/recovery：`projects/simulation/common/__init__.py:18-42` | 必须新增并冻结 `symbol_index ↔ sample_index ↔ frame_index`、TX/RX filter group delay、preamble/data mask、真实 impairment trajectory、接收机可见信息与 scoring-only truth。没有该契约，其余模块无法可靠组合。 | 1.0 + 1.0 = **2.0** |
| RRC TX/RX filtering | `SMALL_ADAPTER` | B7 有 RRC taps 与 TX 零插值成形：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:97-134`；另一个 B7 分析脚本有 RX matched filter：`projects/simulation/explore/b7-gardner-ted-foe/_ted_gain_analytic.py:245-269` | TX/RX 两端未在同一 testbed 链中闭合；B7 自己明确主数值链不做 RX MF（同文件 `:203-207,264-267`）。需提取到统一模块，处理群时延、边缘裁剪、功率/噪声定标并验证 RRC×RRC Nyquist 性。 | 0.5 + 0.5 = **1.0** |
| oversampling ≥2 sps | `SMALL_ADAPTER` | B7 用 `SPS_GEN=16`、`SPS_RX=2`：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:83-86`，并有 FIR decimation：同文件 `:137-142`；参数真相源记录 2.94 sps、FOE 前 2 sps：`projects/simulation/params.py:679-688` | 仅 sandbox 常量/局部函数，没有通用采样率对象、抗混叠合同或 sample-rate-aware channel。需统一 `fs = sps × Rs` 与每级 rate transition。 | 0.5 + 0.25 = **0.75** |
| fractional-delay interpolator | `SMALL_ADAPTER` | B7 有 4 点 cubic/Farrow 算子：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:389-404`；Pilot-Jones sandbox 另有 17-tap windowed-sinc fractional delay：`projects/simulation/explore/pilot-jones-complex-salvage/complex_jones_channel.py:191-219` | 两实现均是私有 sandbox helper，未统一延迟符号、边界、群时延和向量/streaming 状态。需选定一个生产接口并做幅相响应、整数/零延迟 identity、已知正负延迟验证。 | 0.5 + 0.5 = **1.0** |
| fractional timing offset 注入 | `NEW_INFRASTRUCTURE` | 最接近资产是上项 PMD 用 sinc delay，而非单路采样时钟损伤：`projects/simulation/explore/pilot-jones-complex-salvage/complex_jones_channel.py:191-219`；B7 只在 S-curve 内扫候选采样相位：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:176-218` | 没有独立 `apply_fractional_timing_offset()`、真实 `tau[n]` 或与 filter transient 对齐的 truth。必须把注入与恢复严格分开，禁止直接复用 loop 内插值状态作为 ground truth。 | 0.5 + 0.5 = **1.0** |
| sampling-clock offset / drift | `NEW_INFRASTRUCTURE` | 对 `SCO/ppm/sampling clock/clock drift/sample-rate error` 的全仓 Python exact grep 无实现命中；现有采样率仅是固定场景字段：`projects/simulation/params.py:679-688` | 需建立时基扭曲 `t_rx[n]`、ppm/线性 drift、跨帧连续 accumulator、可选 sample slip、band-limited resampling 与 truth trajectory。这是最容易被低估的状态型模块。 | 1.0 + 1.0 = **2.0** |
| frame/preamble builder | `SMALL_ADAPTER` | B3 可生成固定伪随机 QPSK FSTS 模板，但明确是单极化简化：`projects/simulation/explore/b3-joint-estimation/frame_sync_fsts.py:58-78`；coded-chain 有 receiver-known deterministic prefix 及 prefix+data 拼接：`projects/simulation/explore/nda-awgn-tracking-sandbox/p08r_chain.py:185-202,300-323` | 需合并成通用 frame schema，输出 preamble/data/pilot masks、bits/symbols 映射、显式 overhead 和 receiver-known manifest；当前两个资产的调制、双偏振和职责不同。 | 0.5 + 0.5 = **1.0** |
| frame offset 注入/裁剪 | `NEW_INFRASTRUCTURE` | B3 smoke 只用 `50` 个零手工构造独立相关器测试：`projects/simulation/explore/b3-joint-estimation/_smoke_test.py:108-117`；多孔径信道只把 `offset_k` 记入列表：`projects/simulation/explore/b3-joint-estimation/multi_aperture_channel.py:107-135,141-150`，没有移动 `rx_k` 样本 | 需真实 prefix/suffix buffer、正负 offset 语义、部分帧裁剪、检测失败状态及 truth。当前 `offsets` 是元数据，不是损伤注入。 | 0.5 + 0.5 = **1.0** |
| timing detector/loop（Gardner；M&M 等） | `SMALL_ADAPTER` | `common` 有 Gardner 名义接口：`projects/simulation/common/_recovery.py:382-432`；但 `mu` 被转成整数索引、输出直接取 `y_curr`，没有分数插值（同文件 `:402-430`）。B7 sandbox 有 PI+NCO+cubic 完整得多的实现：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:326-404` | 应以 B7 为候选源而非直接信任 common 版本；需 productionize、接真实 offset/SCO、输出 timing trajectory/lock/cycle-slip 诊断。全仓未发现 M&M/Mueller-Muller 或 early-late 实现，且 `projects/simulation/tests/` 未引用两个 Gardner 函数。 | 1.0 + 1.0 = **2.0** |
| CFO / Doppler / Wiener phase-noise chain | `SMALL_ADAPTER` | `doppler_phase()` 已组合 residual CFO、quadratic Doppler 与 Wiener PN：`projects/simulation/common/_channel.py:35-54`，symbol-rate generator 应用该相位并加噪：同文件 `:70-94`；common 有 FFT-FOE、DPLL、VV/BPS：`projects/simulation/common/_recovery.py:37-128` | 公式和 carrier recovery 资产足够，但相位目前按全局 symbol period `T_S` 生成。新 waveform 必须按 sample period 注入并定义 frame 间相位/频率状态是否连续，同时保证所有 baseline 消费同一相位轨迹。 | 0.5 + 0.5 = **1.0** |
| Gamma-Gamma fading | `SMALL_ADAPTER` | 静态 block GG：`projects/simulation/common/_channel.py:27-32,70-87`；带相干时间的 AR(1) GG：`projects/simulation/common/_gg_time.py:104-157`；dual-pol shared channel 使用该动态包络：`projects/simulation/common/_dual_pol_channel.py:95-114,123-140`；已有参数/重现性测试：`projects/simulation/tests/test_channel_turb_params.py:20-72`、`projects/simulation/tests/test_dual_pol_shared_channel.py:111-124` | 需要明确 `h` 是强度、接收幅度用 `sqrt(h)`，并定义 symbol-rate fading 如何映射到 oversampled samples 与跨帧 state。核心模型可复用，不必重写。 | 0.5 + 0.5 = **1.0** |
| paired realization | `SMALL_ADAPTER` | 单偏振共享 realization 返回 `rx_raw/bits/tx/h/phi`：`projects/simulation/common/_channel.py:57-94`；determinism 与 required keys 有静态测试：`projects/simulation/tests/test_common.py:427-451`；dual-pol 也验证同 seed 重现：`projects/simulation/tests/test_dual_pol_shared_channel.py:111-124` | 旧 paired contract 是 1-sps carrier-recovery contract。需扩充为一次生成并冻结 waveform、noise、GG、CFO/PN、timing/SCO/frame truth 和 masks；baseline 只能读接收机可见字段，truth 仅评分。 | 0.5 + 0.5 = **1.0** |
| BER metric | `READY` | QPSK/16QAM demod 与 BER primitive 已有：`projects/simulation/common/_modulation.py:5-15,24-61`；统一 `ber_eval` 区分 direct 与 TX-truth oracle：同文件 `:71-82` | 算子可直接复用；接入时只需验证 frame/preamble exclusion、对齐后 data mask 与 QAM16 dispatch，不能让 oracle rotation 进入部署路径。 | 0.0 + 0.25 = **0.25** |
| EVM metric | `NEW_INFRASTRUCTURE` | 全仓 Python exact grep 只有“使用 BER 非 EVM”的注释：`projects/simulation/common/_ml_equalizer.py:42-45`、`projects/simulation/explore/cma-fade-divergence/mve_cma_vs_ml.py:29-32`，无 EVM 函数 | 需定义 reference normalization、是否先做 receiver-visible common phase/gain normalization、data mask 和聚合层级；实现不大，但指标语义必须冻结。 | 0.25 + 0.25 = **0.5** |
| sync-error metrics（timing/SCO/frame/CFO/CPE） | `NEW_INFRASTRUCTURE` | B7 只记录 CFO 绝对误差和 TED error std：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:383-385,720-729`；B3 runner 仅聚合 BER、`df_est`、`f_dot_est` 均值：`projects/simulation/explore/b3-joint-estimation/b3_joint_mve.py:65-112` | TED 输出均值/std 不是 timing truth error。需定义 wrapped CPE error、CFO Hz error、timing phase error、SCO ppm error、frame detection/false-lock/miss、acquisition/steady-state/cycle-slip 口径和排除区间。 | 0.5 + 0.75 = **1.25** |
| baseline runner | `NEW_INFRASTRUCTURE` | `common.run_trial_shared()` 能在同一个旧 realization 上跑 carrier-only schemes：`projects/simulation/common/_experiment.py:125-161`；B7 有本地三方 sweep runner：`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:642-744` | 需新 runner 注册 timing/frame/carrier baselines，统一 stage order、同一 impairment realization、receiver-known manifest、data-only metric masks、failure states 和结果 metadata。旧 runner 不认识 waveform/filter delay/SCO/frame acquisition。 | 1.0 + 0.75 = **1.75** |

逐项工期合计：**18.5 人日**。其中 waveform contract 与 RRC/oversampling/interpolator、paired realization 与 channel、metrics 与 runner 存在重叠，合并实现后估计 **11–14 个工作日**，不能把重叠误解为“已有端到端 testbed”。

## 3. 旧 caller 无问题，新 testbed 是已授权 scope change

旧 `common` 的主链是合理的 symbol-rate carrier-recovery testbed：`generate_shared_realization()` 生成 `Ns` 个 QPSK 符号，并在同长度数组上施加 `sqrt(h)`、carrier phase 和 AWGN（`projects/simulation/common/_channel.py:73-87`）；`carrier_recovery_fixed()` 随后执行 FOE→DPLL→VV（`projects/simulation/common/_recovery.py:121-128`）。这与“frame sync、matched filter、timing recovery 已经完成”的旧 caller 完全一致，缺 RRC/SCO/frame 并不是旧代码 bug。

新专题由 D001 明确把 research object 扩到 waveform/timing/frame，并要求从 GW Step 1 重新取证；不能因旧 caller 没有这些自由度就否决新对象，也不能把 sandbox 片段误报成现成 testbed（`.sessions/2026-08-06-oversampled-coherent-sync-groundwork/decisions.md:13-21`）。因此本 BOM 中的 `NEW_INFRASTRUCTURE` 表示 **scope-change 增量**，不是旧实现回归或历史错误。

## 4. 关键断链与最容易低估的接口

1. **时间/索引契约是第一风险。** RRC group delay、fractional delay、SCO 累积漂移、frame offset、loop transient 会同时改变 sample 数和 data mask。若每个模块各自裁剪，BER 可能在错误符号上仍给出“看似合理”的数值。
2. **SCO 是状态机，不是一次 fractional shift。** 静态 `tau0` 只能覆盖固定 timing offset；SCO 必须跨样本累计，可能产生 sample slip，且跨 frame reset/continue 会改变科学问题。
3. **现有 `common.gardner_ted_recovery` 不能按 docstring 视为“已有插值环”。** `mu` 只参与整数索引并被截断（`projects/simulation/common/_recovery.py:402-430`）；真正的 cubic loop 在 B7 私有脚本内，且没有真实 timing/SCO 注入回归。
4. **B3 frame path 没有端到端接通。** `multi_aperture_channel` 只记录 offsets，没有移动样本（`projects/simulation/explore/b3-joint-estimation/multi_aperture_channel.py:107-135`）；正式 B3 runner 又传 `ts_template=None`（`projects/simulation/explore/b3-joint-estimation/b3_joint_mve.py:84-99`）。更关键的是 `joint_estimation_pipeline` 虽导入 `multi_branch_phase_precorrect`，主体没有调用它，最终只回传 offsets（`projects/simulation/explore/b3-joint-estimation/joint_estimation_pipeline.py:40-45,149-185,204-237`）。
5. **paired realization 必须扩到原始 waveform。** 仅让各方法使用同 seed 不够；它们必须消费同一份已生成 sample array、同一噪声、同一 `tau[n]`/SCO trajectory、同一 frame cut 和同一 phase/GG trajectory，避免不同 DSP 分支改变 RNG draw order。
6. **指标语义比代码行数更贵。** timing error 必须对 truth trajectory，不是 TED 内部 error；EVM 必须冻结增益/相位归一化与 data mask；frame failure 必须显式进入结果，不能在对齐失败时悄悄缩短数组继续算 BER。
7. **baseline runner 的信息边界需要独立验证。** preamble/pilot 可 receiver-known 且计 overhead；TX payload truth 只能用于离线评分。现有 `ber_eval(mode='oracle')` 与 B7 的 lag/rotation search 都是方便的 scoring helper，不能混入部署 baseline 的决策路径（`projects/simulation/common/_modulation.py:71-82`；`projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py:598-636`）。

## 5. 5 日门与候选特定最小工程切片

以下 A/B 只是工程切片估算，不是科学候选、Q# 或方法判断。估算假设复用现有 QPSK/16QAM、Gamma-Gamma、carrier recovery 与 paired-RNG 资产，只补该切片闭环必需的 waveform contract、truth、最小指标和 runner；不含 Step 2/3 后对某篇 2019+ baseline 的忠实复现。

| 工程边界 | 包含 | 明确不含 | 合并后保守工期 | 是否“重建完整通信平台” | 是否单独明显超过约 5 日 | `TESTBED_SCOPE_EXCESSIVE` |
|---|---|---|---:|---|---|---|
| **Full frozen object** | 本 BOM 全部 16 项：acquisition + maintenance + EVM/完整 sync metrics/统一 runner | 不含具体 baseline 论文复现 | **11–14 日** | **是，接近从 symbol-rate caller 向完整 waveform/frame/synchronization platform 重建** | **是** | 只有在后续候选确实要求 full object 时才满足工程侧停止条件；不能因当前上界数字自动触发 |
| **A — acquisition 最小 slice** | RRC TX/RX、固定 ≥2 sps、fractional-delay/固定 fractional timing 注入、receiver-known preamble/frame builder、真实 frame offset、CFO、最小 frame/timing/CFO truth、paired realization、BER 与最小 runner | SCO/drift、长时 timing maintenance、Gamma-Gamma 动态维护、完整 CPE/EVM 指标、与 acquisition 无关的 impairment | **5.5–7.5 日** | **否。** 是新增 acquisition front-end 子层，复用现有调制、carrier recovery、channel/BER；不是完整通信平台重建 | **边界到略明显超过。** 保守中心值约 6.5 日，但不是数量级失控 | **不单独触发。** 虽旧 caller 不支持且可能超过 5 日，但“不需要重建完整通信平台”这一条件不成立 |
| **B — maintenance 最小 slice** | RRC TX/RX、固定 ≥2 sps、Gardner timing loop、SCO/drift state、Gamma-Gamma、CFO/Wiener PN/carrier recovery、timing/SCO/carrier truth、paired realization、BER 与最小 runner | 未知帧起点搜索、preamble/frame-offset acquisition、完整 EVM、与维护无关的 frame detector | **7–9 日** | **否，但属于较重的 stateful DSP extension。** 不建 frame acquisition/FEC/network stack，仍复用现有 channel/carrier assets | **是** | **不单独触发。** 工期门成立，但“重建完整通信平台”不成立；若具体 baseline 额外要求 frame acquisition、完整 EVM/FEC 或另一套 channel，需重新审查是否升级为 full-platform |

切片估算的主要依据：A 复用 B7 的 RRC/2-sps/Farrow 与 B3/p08 的 preamble 片段，但必须补真实 frame offset、统一索引和 acquisition metrics；B 复用 B7 Gardner 与 common CFO/PN/GG，却必须新建 SCO 的跨帧 accumulator 和 timing truth。A/B 都不是把表中逐项人日机械相加，而是按共享 waveform/runner 合并后的单人日历工期。

因此当前静态审计只能给出以下门判断：

- **不能仅凭 full frozen object 的 11–14 日自动判 `TESTBED_SCOPE_EXCESSIVE`。** 全部 impairment 是能力审计包，不是已确认的最终方法输入。
- **若后续全文证据要求 A acquisition slice：** 工程量约 5.5–7.5 日，不属于完整平台重建，停止条件不闭合。
- **若后续全文证据要求 B maintenance slice：** 工程量约 7–9 日，虽明显超过 5 日，但仍是现有 symbol-rate/carrier testbed 的有界扩展，停止条件仍不闭合。
- **只有具体候选必须同时跨 acquisition + maintenance，且还要求统一 frame/waveform/指标/runner，才有充分工程依据把 full-object 11–14 日映射到“完整通信平台重建”，从而满足 `TESTBED_SCOPE_EXCESSIVE` 的工程侧合取门。** 此判断必须等 Step 1/2/3 证据确定候选所需模块，不能在本次静态审计中预造 Q#。
- **没有工程上的外部硬阻塞。** 但具体 2019+ baseline 的算法细节、frame/preamble 结构和参数量级必须由后续全文证据冻结；在此前只能完成 generic infrastructure，不能声称 baseline-faithful 或论文可用。
