# Step 077 — C5-0 单自然格 coded headroom

> 2026-08-30 | T077 / D056 / V031 / CP018 | single preregistered cell
> terminal: `SINGLE_CELL_NO_HEADROOM`

## 1. 控制、范围与固定单格

- Fresh task-control validator：`PASS`（`rdl.task-control.v2` / epoch 18 / CP018 / `C5_LLR_SINGLE_CELL_NATURAL_HEADROOM`）。
- 起点：`cde31b9f98d14e161de32afca3793f7737838bc7`；manifest SHA256=`14ff14de3d0094f135c3a07d3fb395455e81035f6b6d1b014704177587ed3782`。
- 物理 frame 始终为每偏振 `256` 个 observation symbols；科学 evaluation 始终为 `512` 个 physical frames。二者是不同维度，未把 observation length 改成 512。
- 保留 T066 单格结构：4-symbol Ch4 preamble，64 Ch3 pilots/pol，GG(4,1.9)、block 256，前一 GG block 含 252 observation symbols、后一 block 含末 4 个，15 dB，static unitary Jones，equal circular AWGN，plain RDE `mu=1e-3`，Ch3 DA；无 PDL/PMD/FIR/IQ。
- 一个 5G BG2 `(1024,1536)` codeword 映射到两个偏振共 384 个 non-pilot APSK symbols，固定 pol-major：pol0 192 后 pol1 192。
- 未修改 `common/`、全局 params、旧 `coded-decoder-feedback/`、旧 C5-1、Ch3/Ch4、Skill/controller 或正式论文正文；未换格、调公式、追加 frames 或运行 Gate 3。

## 2. TDD 与 correctness smoke

- RED 1：目标 core 不存在，`2 failed, 1 passed`；最小 mapping/manifest GREEN 后 `3 passed`。
- RED 2：缺 physical mapping、receiver arms、8-frame smoke，`3 failed, 3 passed`；动态 bridge 加载器的 Python 3.14 `dataclass` 根因修复后 `6 passed`。
- RED 3：缺 observation/evaluation 显式区分、physical pair identity 与 live codec 点检，`3 failed, 5 passed`；GREEN `8 passed`。
- RED 4：缺 codec artifact 身份与 B1 tie-break，`3 failed, 7 passed`；限制 injected codec 只能 `write=False` 后 GREEN `10 passed`。
- RED 5/6/7：Gate1 reducer `2 failed`、Gate2 reducer `1 failed`、raw-only audit hash `1 failed`；各自最小 GREEN。
- 最终 targeted：`14 passed in 9.14s`。
- 8 个 smoke seeds=`2900..2907` 实际使用 `TargetApskCodec`、`live_backend=true`；每帧五臂均 fresh state、20 iterations，mapping/pair/lifecycle PASS。另有一帧真实 encode→mapped physical→receiver→五臂 `decode_fresh` 点检 PASS。
- Truth 证据严格收窄为 `receiver_api_signature_and_identical_input_replay`：receiver API 不接收 scorer truth，相同 receiver-visible 输入重放得到相同 LLR hash；不声称已从 raw 证明完整强 truth firewall。

## 3. Calibration 与 Gate 1

- Disjoint calibration：64 frames，seeds=`3000..3063`，固定 15 点 `s=2^(k/2), k=-8..6`。
- 按 FER→BER→`|log(s)|`→较小 `s` 冻结 `B1 scalar=1.0`：4893/65536 info-bit errors，BER=`0.0746612548828125`；18/64 FER=`0.28125`。固定标度没有额外校准改善。
- Gate 1 只在 seeds=`4000..4127` 的 128 帧计算 variance，`decoded_arms=[]`：
  - Spearman rho=`0.98566540010987`；PCG64 seed=`2026083007`、10,000 次 physical-frame bootstrap 单侧 95% lower=`0.9758980391761476`，PASS。
  - `log(N0_pilot/N0_payload)` median=`0.017144522606823934`，IQR=`[-0.06705041487444206, 0.10236627286429097]`，MAE=`0.11087618786449432`。

## 4. Gate 2 与唯一 terminal

Gate 1 PASS 后才把同一 manifest 追加到 seeds=`4000..4511` 的固定 512 帧，并只 decode B0/O1。现有前 128 帧逐帧重生成时同时核对 pair、mapping、received-observation 与 codeword hash；512/512 四项均一致。

| arm / difference | BER | FER | paired 95% CI |
|---|---:|---:|---:|
| B0 | 25844/524288 = `0.04929351806640625` | 132/512 = `0.2578125` | — |
| O1 | 27965/524288 = `0.05333900451660156` | 131/512 = `0.255859375` | — |
| B0−O1 | `-0.0040454864501953125` | `0.001953125` | BER `[-0.005561971664428711, -0.002660703659057618]`; FER `[0, 0.005859375]` |

- BER discordant frames=`128`（B0 better 87，O1 better 41）；FER discordant frames=`1`。
- O1 的 scorer-only payload-truth scalar auxiliary variance 未提供 coded BER headroom，Gate 2 FAIL，唯一 terminal=`SINGLE_CELL_NO_HEADROOM`。
- Gate 3=`NOT_OPENED`；B1/B2/B3 evaluation BER/FER/CI 均为 `N/A (Gate_2_FAIL_not_opened)`。B1 的 `1.0` 只来自 disjoint calibration，不是 evaluation arm 结果。

## 5. Clip、scalar 与 identity 诊断

- B0：demapper clip30 `181388/786432=0.23064676920572916`（512 frames 均出现）；backend clip20 incidence=`0.45830535888671875`；decode_fresh clip30 前超限数 0。
- O1：demapper clip30 `127482/786432=0.16210174560546875`（422 frames 出现）；backend clip20 incidence=`0.26513417561848956`；decode_fresh clip30 前超限数 0。
- 未开放 B2 的 scalar 仅作诊断：min/q25/median/q75/max=`0.013728634451413127 / 0.26414137114603 / 0.5535655470742915 / 0.9811089953266731 / 2.9014271219209107`，mean=`0.6606284427479066`；未用来替代 Gate 3。
- Evaluation pair/mapping hashes 各 512 个唯一值；512 帧 arm 集合严格为 `{B0,O1}`。
- P1 修复没有重跑科学：仅从已持久化的 13 个摘要字段按固定顺序构造 canonical JSON audit-pair SHA256。独立 reviewer 重算 512/512 PASS；scope 明确为 `persisted_summary_integrity_not_underlying_array_reconstruction`。

## 6. 独立 raw-only reviewer

- Reviewer 未调用或导入项目 runner/reducer，从 calibration/evaluation raw 独立重算 split、B1 tie-break、Gate1 rho/CI、B0/O1 BER/FER/paired CI 与 terminal。
- 最终：`PASS / P0=0 / P1=0 / P2=3`。
- P2（不阻塞本 terminal）：(1) brief terminal 6 的“256 evaluation frames”措辞债务；本任务依用户权威纠正使用 256 symbols/pol 与 512 frames；(2) D056 的 “O1 true matched exact-APP” 强于本任务实际的 payload-truth scalar auxiliary variance；(3) brief 未定义 log-ratio 分子，本 receipt 已显式记录 `log(N0_pilot/N0_payload)`。
- T066 继承只声称结构/时序/cell 不变量，不把历史 raw 当 seed bit-exact oracle；live codec 字段只证明持久化身份一致，不声称外部二进制证明。

## 7. Fresh 验证

- T077 targeted：`14 passed in 9.14s`。
- 旧 T076 correctness：`10 passed in 7.77s`。
- live codec 定向回归：`3 passed, 15 deselected in 7.25s`。
- task-control validator：`PASS`。
- `py_compile`：exit 0。
- 科学 raw 为逐帧持久化；checkpoint 按 manifest seed prefix 续跑，不改变 manifest。

## 8. 主要文件

- `single_cell_manifest.yaml`：物理/统计/arm/terminal 冻结合同。
- `single_cell.py`、`single_cell_reducer.py`：mapping、runner、frame-cluster reducer 与审计 receipt。
- `single_cell_smoke_{raw,receipt}.json`、`single_cell_live_point_{raw,receipt}.json`：correctness/live 证据。
- `single_cell_calibration_{raw,receipt}.json`：64 帧 B1 冻结。
- `single_cell_evaluation_raw.json`、`single_cell_gate1_receipt.json`、`single_cell_gate2_receipt.json`：512 帧逐帧 science raw 与门控 receipt。
- `single_cell_aggregate.json`、`single_cell_receipt.json`：最终 aggregate/terminal receipt。
