# Task Brief: C5-0 单自然格 reliability / coded headroom / B1–B3 判定

> 来源: S028 / D056 / T076 / V031 | 产出位置: `projects/simulation/explore/ch5-apsk-llr-calibration/` + `projects/thesis-fso/worker-logs/step-077-c5-0-single-cell-natural-headroom.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 18
  action_class: C5_LLR_SINGLE_CELL_NATURAL_HEADROOM
  mission_checkpoint: CP018
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

在 T076 已闭合的 target APSK→5G BG2 LDPC seam 上，只跑一个继承 T066 的自然场景单格，顺序回答三件事：

1. current-frame pilot residual variance 能否正向预测 disjoint payload residual reliability；
2. scorer-only per-frame payload-residual oracle O1 是否相对固定 B0 留有 coded BER/FER headroom；
3. 只有前两门通过时，receiver-visible B2 是否相对 offline-fixed B1 有明确 coded 改善，并且没有被同信息预算 B3 exact-APP 完全支配。

这不是开发矩阵。不得换 cell、调参数、加损伤或用 GMI/uncoded/构造 clip flip 替代 coded BER/FER。

## 开始前强制读取

1. 根 `AGENTS.md`、`sim-preflight` skill 全文及必读 references、`code-quality.md` 和相关 sim-template。
2. 本 brief、topic-index 页首 CP018、D056/V031、T076 worker log、T075 `step4a-paper-feasibility.md`。
3. `projects/simulation/explore/ch5-apsk-llr-calibration/correctness.py` 与集中测试。
4. `projects/simulation/explore/ch5-apsk-structured-covariance/occurrence_manifest.yaml`、`post_ch4_ch3_bridge.py`、T066 raw schema/reducer；只继承场景与 receiver bridge，不把 T066 occurrence 结果当性能数据。
5. `projects/simulation/explore/coded-decoder-feedback/codec.py` 及 T076 已 receipted 的 Sionna backend。

先 fresh 运行 task-control validator。先写 deterministic/8-frame smoke tests 并明确 RED→GREEN，再运行唯一科学单格。不得修改 `common/`、全局 `params.py`、旧 `coded-decoder-feedback/`、旧 C5-1 artifact、Ch3/Ch4 或 T066 raw。

## 冻结物理单格与 frame 映射

- DP-(8,8)-16APSK、2 polarizations、15 dB、Gamma–Gamma `(alpha=4,beta=1.9)`、block=256、static random memoryless unitary Jones/window、equal circular AWGN after Jones。
- residual frequency=`1 MHz`、slope=`150 MHz/s`、linewidth=`10 kHz`；Ch4 acquisition pilots=`4`，plain canonical RDE `mu=1e-3`；per-pol Ch3 DA CPR。
- 每个物理 frame 的 observation=`256 symbols/pol`；pilot indices 固定 `0,4,...,252`，即 `64 pilots/pol`，balanced labels 与 pol1 shift=3；PDL/PMD/FIR/IQ 全关。
- 必须诚实保留 T066 的实际连续时序：4-symbol Ch4 preamble + 256-symbol observation，而 GG block=`256`，因此 observation 最后 4 symbols 落入下一 GG block；不得暗改 block size 或截掉末 4 symbols 救结果。
- 每帧恰好一个 5G BG2 `k=1024,n=1536,Qm=4` codeword。1536 coded bits→384 APSK symbols，按 **pol-major** 固定填入两偏振的 384 个 non-pilot slots：pol0 的 192 个 non-pilot slots 在前，pol1 的 192 个在后。128 个 pilot slots 不承载 coded bits。该 mapping 必须有 codec→DP frame→receiver→LLR→codec 的 deterministic roundtrip receipt。
- 每帧 B2 只有一个 scalar，由两偏振 128 个 current-frame pilots 共同估计；同一 codeword 的全部 1536 LLR 共用。禁止 per-pol/per-codeword/per-bit scaling。

## 数据划分与固定规模

- correctness smoke：8 个独立 smoke seeds，只查 finiteness、mapping、truth firewall、paired identity、decode lifecycle；不得据此选参数或下科学结论。
- B1 offline calibration：64 个独立 frames，seeds=`3000..3063`。只允许在固定网格 `s=2^(k/2), k=-8..6` 中选择一个 global scalar；按 calibration FER 最低、再 BER 最低、再 `|log(s)|` 最小、再数值较小的确定性 tie-break 冻结。
- scientific evaluation：先生成固定 Gate-1 子集 `128` frames（seeds=`4000..4127`）；Gate 1 FAIL 即停。Gate 1 PASS 后，将同一 manifest 追加到固定 `512` frames（seeds=`4000..4511`）。所有正性能 terminal 只能在完整 512 frames 上裁决，不在 64/128/256 中间 checkpoint 提前宣称成功。
- 所有 arms 共用逐帧 realization、information bits、coded bits、pilots、payload、decoder、20 iterations、clip/filler 与 decode-call budget；每 arm fresh decoder state。

若 512 frames 仍没有足够 paired events，terminal 只能是预定义的 `SINGLE_CELL_INSUFFICIENT_SENSITIVITY`，不得追加 frames 或换 cell。

## Receiver arms 与 truth firewall

- `B0`：exact-APP auxiliary `N0=10^(-15/10)`，demapper clip30，`s=1`。
- `B1`：同一 B0 LLR 在 demapper clip30 后乘 calibration split 选出的唯一 runtime-fixed scalar；evaluation 期间固定。
- `B2`：两偏振 current-frame pilots 各自 residual demean 后，pooled unbiased `hat N0_pilot=sum|e-mean(e)|²/sum(Np-1)`；`s=N0_nominal/hat N0_pilot`，在 demapper clip30 后、decode_fresh clip30 前乘一次。
- `B3`：同一 `hat N0_pilot` 直接作为 exact-APP auxiliary variance，再走相同 clip/decode。
- `O1`：仅 scorer 使用 transmitted non-pilot APSK symbols，按与 B2 同样的 per-pol demean + pooled unbiased 公式得到 `N0_payload`，直接作为 exact-APP auxiliary variance。O1 是“同一 scalar auxiliary model 下的 payload-truth oracle”，不得写成真实完整 channel likelihood 或 deployable receiver。

receiver API 只能接收 rx、known pilots/mask、冻结 mapping/config 与 B1 scalar。true payload symbols/bits、true SNR/noise/Jones/phase、decoder truth 只可进入 O1 和 scorer；突变 scorer-only truth 时 B0/B1/B2/B3 的 LLR/decode input 必须 byte-identical。

## 顺序科学门与统计合同

所有差值统一为“前者错误率 − 后者错误率”，正值表示后者更好；CI 以 physical frame 为 paired cluster，bootstrap seed 与 resamples 在 manifest 冻结，默认 10,000 resamples、95% percentile CI。Spearman CI 同样按 frame cluster bootstrap。

### Gate 1：pilot→held-out reliability

- 固定前 128 evaluation frames 上计算 `Spearman(-log(hat N0_pilot), -log(N0_payload))`；两者的负号只把 variance 改写成 reliability，Spearman 与直接比较两个 variance 同号。
- PASS：rho 点估计 `>0` 且 physical-frame bootstrap 95% one-sided lower `>0`。
- 同时报告 log-ratio median/IQR、MAE，不把误差小作为额外可调门。
- FAIL 立即 terminal=`SINGLE_CELL_NO_RELIABILITY_SIGNAL`；不运行 B1/B2/B3 性能比较。

### Gate 2：B0→O1 coded headroom

- 只在 Gate 1 PASS 后 decode B0/O1。
- 报告 info-BER、FER、paired differences 与 CI、discordant frame counts。
- PASS：完整 512 frames 上 `BER_B0-BER_O1` 的 95% CI lower `>0`，且 O1 FER 点估计不高于 B0。若 FER difference 的 CI lower 也 `>0` 且 discordant FER pairs `>=30`，标为 stronger FER headroom；BER 明确改善已足以通过硕士级单格 headroom 门。
- 若 BER CI 不支持改善或 O1 FER 更差：`SINGLE_CELL_NO_HEADROOM`。若 B0/O1 均零 FER 且 BER event 数不足以判定：`SINGLE_CELL_INSUFFICIENT_SENSITIVITY`。

### Gate 3：B1 / B2 / B3

- 只在 Gate 1–2 均 PASS 后运行；B1 scalar 已由 calibration split 冻结。
- B2 成立门：完整 512 frames 上 `BER_B1-BER_B2` 的 95% CI lower `>0`，且 B2 FER 点估计不高于 B1。
- “被 B3 完全支配”定义：B3 相对 B2 的 BER difference `BER_B2-BER_B3` 95% CI lower `>0` 且 B3 FER 点估计不高于 B2。若完全支配，B2 不成立；若 CI 跨 0，只诚实写 B2 与 B3 未分出，不自动否决 B2。
- 另报 B0→B2/B3、clip incidence、scalar distribution、计算量；这些是诊断，不替代 Gate 3。

## 唯一 terminal

1. `SINGLE_CELL_PASS_B2_SIGNAL`：三门均 PASS，B2 相对 B1 BER 明确改善且 FER 不差，B3 未完全支配。只允许主控另开有界开发矩阵。
2. `SINGLE_CELL_B3_ONLY_SIGNAL`：Gate 1–2 PASS，B2 门失败或被 B3 完全支配，同时 B3 相对 B1 的 BER CI lower `>0` 且 FER 不差。停止 B2，回主控显式重判 B3 身份。
3. `SINGLE_CELL_NO_RELIABILITY_SIGNAL`：Gate 1 FAIL。
4. `SINGLE_CELL_NO_HEADROOM`：Gate 1 PASS，Gate 2 FAIL。
5. `SINGLE_CELL_B2_NO_GAIN`：Gate 1–2 PASS，但 B2 与 B3 都没有相对 B1 的预注册正向 coded signal。
6. `SINGLE_CELL_INSUFFICIENT_SENSITIVITY`：固定 256 evaluation frames 下事件不足，不能判门；不得追加样本。
7. `INVALID_TESTBED`：frame mapping、truth firewall、paired hashes、finiteness、codec/clip/filler 或依赖无法正确闭合。

## 输出、验证与停机

- 新增 `single_cell_manifest.yaml`、窄 runner/reducer/tests、append-only raw/checkpoint、aggregate/receipt 和 step-077 worker log；science raw 必须逐帧保存每 arm error counts/FER、hash、scalar、pilot/payload statistic，不只保存均值。
- 先跑 8-frame correctness smoke；失败只修 correctness，不改物理/统计合同。smoke PASS 后运行固定 calibration 与 128-frame Gate 1；Gate 1 PASS 才追加到 512-frame evaluation 并按 Gate 2→3 顺序运行，后门未开放的 arms 不运行。
- 由独立 reviewer 从 raw 绕过项目 reducer重算 mapping/hash、split、rho、BER/FER、paired CI 与 terminal；P0/P1 修到 0。
- fresh targeted tests、旧 T076 10 项回归、task-control validator、manifest hash、`git diff --check`、写入白名单均 PASS。
- 单次任务墙钟 90 分钟；60 分钟仍未完成 fixed evaluation 时，保存 checkpoint 并续跑同一 manifest，不改 seed/规模/cell。只允许一次 commit，不 push。
- 禁止正式论文正文、Skill/controller、Ch3/Ch4、C5-1、P11/P01、`common/`、全局 params 修改；禁止检索/下载文献。
