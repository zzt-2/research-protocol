# D0 资产预检与实现合同闭合

> 2026-08-10 | Groundwork Step 4a / CP012 implementation preflight  
> 唯一机器 owner：`d0-defect-smoke-contract.yaml` v3  
> 当前状态：`VERIFIED_FROZEN_FOR_D0_IMPLEMENTATION_AND_UNIT_TEST`  
> 科学状态：`D0=NOT_RUN / METHOD_SIGNAL=NONE`

## 1. Findings first

1. **现有资产足以建设 D0，但不能直接拼装。** P08/P08-R/R2 可复用 Gray-16QAM mapping、LDPC encode/decode kernel、per-CW ownership、common square-16QAM BPS 与少量数值 kernel；原对象把 receiver 与 truth 共置、P08-R2 的同 prefix 2×2 LS 秩亏、现有 channel 又没有 D0 carrier/linewidth/slip，因此必须新建 truth-separated D0 shell。
2. **step-096 暴露的三项不是科学 gate 失败，而是 raw→summary 接口空白。** v2 owner 以四张互斥 typed table、独立 computation ledger、60 target-pol off branches→540 fixture-aligned logical projections，以及 S3 case→cell→equal-cell macro closure 消除歧义。seed、threshold、gate 与 test-time best-of 禁令没有改变。
3. **物理 realization 已投影成当前 12-cell population 的单一路线。** `f_G=100 Hz` 明标 canonical-project design choice；线宽数字只作为 effective-combined phase-process linewidth 使用一次；SOP 为 identity；receiver front end 为 per-pol scalar receiver-only chain。它们不是论文原值的伪装，也不新增 fG/SOP cell 轴。
4. **prefix calibration 的两个确定性偏差已修。** pre-EQ complex LS 用 `RSS/(32-1)`；common BPS 后由偶数 prefix 样本选择四个合法 global states、奇数样本独立估计 post-BPS complex residual。后者只供 demapper/B2，不回馈 equalizer，因而无 circular dependency。
5. **B2 仍保持 OFC17 baseline 身份，但数学接口已按 step-099 修正。** complex power 与 per-real variance 分名；residual phase contribution 只计一次；state 维 exact marginalization、bit-set 内沿用 P08 max-log；single-state preclip 必须与 P08 `sigma2=N0_cplx/2` 逐点一致。
6. **预算没有被静态证据判死，但还不能称 4.50 日已证。** 计划 logical exposure 与 content-addressed materialization 必须双账；相同 waveform、clean sentinel 与 truth-corrected O1 只可通过 hash+source computation ID 缓存，不能减少 raw exposure或 nominal method cost。任何 scientific seed 前还必须用真实 decoder/BPS/HMM 路径通过 12 分钟有界工程吞吐门控。
7. **首版 v2 的 dev-only freeze 不可审计，已保留 FAIL 历史并在 v3 作纯 additive 修复。** step-101 给出 `FAIL 0/2/0`：HMM clean/controlled 权重不唯一，BPS/B2 只有 opaque freeze hash。v3 明确 clean/controlled-target 各 0.5、sentinel只执行/receipted/costed而不进 objective，并新增 BPS raw、HMM lossless aggregates、B2 clean/controlled raw、具名 `dev_freeze` 与 chronology lock；scientific seed/grid/gate/exposure均未改。

因此当前形成的是 **已经 step-103 接收、并由 D011/V005/CP012 限权开放的实现前静态合同**。本文件及 v3 YAML 不产生 occurrence、damage、headroom、B2 absorption 或 decoder-information 的任何结果；当前只允许 D0 implementation、unit test 与独立代码审查后的非科学 throughput benchmark，scientific S1–S4 execution 仍为 `NO`。

## 2. 资产处置

| 类别 | 接收边界 | 禁止误用 |
|---|---|---|
| P08 constellation/demapper | Gray 16QAM、`[b0,b1,b2,b3]`、positive-for-bit-1、P08 max-log kernel | 禁止把 complex residual power直接作为 P08 per-real `sigma2` |
| P08-R codec | hard encode/decode kernel与 interleaver ownership | 必须包成 explicit fresh restart；禁止 decoder message state reuse |
| common BPS | 仅复用 `bps_cpr(..., mod='qam16')` 数值 kernel | 禁止 `resolve_qam16` 八个 `pi/4` rotations；六格必须另做 D0 单测 |
| GG/equalizer数值 kernel | 只复用公式级 kernel/来源 | 禁止读取 true h/SNR；禁止继承 P08-R2 2×2 LS caller |
| result/receipt pattern | 仅参考 completeness/hash 思路 | 旧 writer 非原子且 schema 不足，不能作为 D0 artifact owner |

必须新建的责任边界为 immutable `ReceiverView/TruthView`、pilot-extended waveform、supplied-waveform dual-pol channel、B0/B1/B2/O1 semantics、typed raw/stat/ledger、atomic artifact receipt 与 D0-specific tests。所有实现都留在 `projects/simulation/explore/coded-decoder-feedback/` 及既有 test 目录；不修改 `common/`。

## 3. 冻结 realization 顺序

```text
payload_x/y + registered prefix + registered periodic pilots
  -> shared GG intensity and shared effective-combined Wiener phase
  -> identity SOP; independent X/Y AWGN
  -> per-pol known-prefix complex LS (C_pre, RSS/31)
  -> per-pol scalar visible-power MMSE amplitude equalization
  -> common square-16QAM BPS
  -> even-prefix four-state global resolve
  -> odd-prefix C_post estimate (never feeds back upstream)
  -> ReceiverView freeze
  -> natural evaluator OR controlled copy-on-write suffix fixture
  -> B0/B1/B2 deployable paths
  -> outputs freeze
  -> O1/TruthView evaluator and raw typed rows
```

受控 suffix 从 data-rank boundary 映射到 absolute time 后开始，覆盖目标 polarization 的全部后续 samples，包括 periodic/terminal pilots；sentinel polarization 必须 byte-identical。Natural 与 controlled 始终分层，不池化。

## 4. B2 与统计闭合

B2 的 owner-ready实现选择全部位于 YAML `b2_primary.implementation_contract`。关键否决测试包括：factor-2 magnitude negative control、single-state P08 preclip identity、Dirac/no-epsilon、state permutation、两种不混用的 global rotation covariance，以及 uniform-state 只消除方向 bit 而保留半径 bit。

raw schema 与复算 owner 位于 YAML `statistical_contract_repair`：

- S1 每 polarization trajectory 一行；20 或 50 个实际 seed blocks独立重采样。
- S2 on 行为 B1/B2/O1，off 只保留 fixture-aligned B1 projection；逻辑投影不重复物化成本。
- S3 每 case 十个 candidate raw scores；rank/top1/RR/fused score均派生，不作为第二份 raw truth；lambda 只用 dev 冻结。
- S4 七个 identity/information/cost check各一行；实际 cost只从 executed ledger求和。
- 每个 stratum 独立初始化 PCG64(2026081001)，10,000 次 percentile bootstrap用 NumPy `method="linear"`；不同 strata 不池化。

dev-freeze 的可复算 owner 位于 `statistical_contract_repair.dev_freeze_artifact_contract`：BPS 每 tuple 保存 7,200 条 per-pol raw；HMM 保存 canonical binary64 per-trajectory NLL 的无损 exact-sum/count sufficient aggregates，普通顺序相关 float sum 禁止；B2 tuple 保存 1,200 条 clean rows 与 21,600 条 controlled target+sentinel rows。goodput 只把 1024 information bits 全对的 CW计为成功交付，denominator含 prefix、periodic/terminal pilots和全部 coded data。最终 artifact必须给五个 BPS pair、五个 statistic pair和一个 final tuple，并使 test runner调用图不可达 fit functions。

## 5. Logical exposure、materialization 与预算门

YAML 同时保存 nominal logical exposure 与不删 exposure 的 materialization upper bound。两者回答不同问题：前者是方法的完整 nominal work与 raw completeness，后者是利用 identical content 可避免的重复执行。vectorized API invocation、cache read 和 source computation ID 都必须显式记账，不得把较少 Python calls冒充较低方法复杂度。

静态审计只能得到 `BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK / >7D_HARD_BLOCKER=NOT_ESTABLISHED`。实现与 unit identity 通过后、任何科学 seed 前，必须在 12 分钟 watchdog 内覆盖 decoder batch sizes、六格 BPS、一个 B2 unique-view slice、一个 HMM grid chunk 和 artifact I/O；只允许调 vectorization/batch/cache/checkpoint，不允许删 seed/cell/tuple/grid/fixture/candidate 或改 gate。

## 6. 明确拒绝的路线

1. **只换 distinct prefix 修 P08-R2 的 2×2 LS：拒绝。** 那会同时引入非平凡 SOP/Jones、rank-4 calibration与真正 MIMO equalizer，是未登记 physical axis，不是最小修复。
2. **沿用同 prefix 的 2×2 LS：拒绝。** regressor rank-deficient，无法识别四个 complex coefficients。
3. **把 source QPSK fourth-power CPE 整体原样复刻：拒绝。** D0 已明确是 square-16QAM BPS transfer；source identity由 pilot four-state posterior→soft LLR→one-way LDPC承载。
4. **用 `resolve_qam16` 或 truth 消除相位：拒绝。** 前者含非法 `pi/4` states，后者违反 ReceiverView。
5. **为省预算减少 frozen exposure或复用 decoder state：拒绝。** 只允许 content-addressed input cache与无状态 vectorization。
6. **修改 `common/` 或旧 P08 资产：拒绝。** D0 必须以独立 shell 暴露自己的 transfer/testbed 身份。

## 7. 证据与下一门控

- coded-chain asset map：`step-094-d0-coded-chain-asset-map.md`。
- OFC17 source map：`step-095-d0-ofc17-b2-source-map.md`。
- raw/stat ambiguity：`step-096-d0-contract-test-stat-map.md`。
- typed stat repair：`step-097-d0-stat-contract-repair-design.md`。
- physical constructor audit：`step-098-d0-physical-contract-completeness.md`。
- B2 math review：`step-099-d0-b2-math-narrow-review.md`。
- independent budget/asset audit：`step-100-d0-asset-contract-budget-audit.md`。
- 首版 v2 全链验收失败：`step-101-d0-asset-contract-verifier.md`（`FAIL 0/2/0`，保留历史）。
- dev-freeze 窄审与 additive repair：`step-102-d0-dev-freeze-artifact-audit.md`。
- v3 fresh narrow reverification：`step-103-d0-dev-freeze-reverifier.md`（`PASS 0/0/0`，两项 P1 CLOSED，`94/94` 静态断言 PASS；不自行授权实现或科学运行）。

下一动作是写出并独立审查 D0 TDD implementation plan，随后只实现/单测 v3 冻结接口。实现、deterministic/unit gates 与独立代码审查通过后，才运行 12 分钟非科学 throughput benchmark；科学 S1–S4 仍须另一轮 D/V/CP。
