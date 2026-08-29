# Ch4 corrected-demapper historical replay：独立验证

> 2026-08-30 | T083 / D062 / V037 / CP024 | reviewer：未参与实现

## 审查边界与方法

本审查只读 `confirmation_raw.json`、`demapper_replay_raw.json`、manifest、aggregate、receipt 和源码；headline 由单独内嵌脚本直接解析两份 raw 后复算。该脚本只导入 `json/hashlib/ast/numpy`，没有导入或调用 `run_demapper_replay.py`、`reduce_demapper_replay.py`，没有运行新 BER 仿真，也没有修改实现、结果或历史 artifact。

## Findings

P0/P1/P2=`0/0/0`。

### Identity、schema 与机制量

| 检查 | 独立结果 |
|---|---:|
| cells / windows per cell / total windows | `4 / 64 / 256` |
| seed identity | `256/256` |
| gain identity | `256/256` |
| realization hash identity | `256/256` |
| observation hash identity | `256/256` |
| payload-bit identity | `256/256` |
| arm recipe `(arm, parameter)` identity | `1280/1280` |
| mechanism rows | `1280/1280` |
| `channel_nmse/inverse_residual/rho` 最大绝对差 | `0/0/0` |

两份 raw 的 cell identity 与 frozen manifest 逐字段一致；每窗恰有 `B0/B1/B2/C4/O1` 五行，每行满足 `BER=bit_errors/payload_bits`、`0<=bit_errors<=payload_bits`，总计 1280 行。replay raw schema 为 `t083.demapper-replay-raw.v1`。

### B2/C4 pooled counts 与独立 paired bootstrap

`D_window=BER_C4-BER_B2`。每个 named comparison 都重新初始化 `Generator(PCG64(2026083005))`，各做 5000 次 window-cluster resample，取 2.5%/97.5% quantile。

| cell | B2 errors/bits | B2 BER | C4 errors/bits | C4 BER | mean D | paired 95% CI | wins/ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| `snr14_np2` | `178610/2097152` | `0.0851678848` | `161245/2097152` | `0.0768876076` | `-0.0082802773` | `[-0.0121246457,-0.0049545288]` | `51/5` |
| `snr14_np4` | `153540/2097152` | `0.0732135773` | `145707/2097152` | `0.0694785118` | `-0.0037350655` | `[-0.0056052446,-0.0019459724]` | `46/4` |
| `snr18_np2` | `84450/2097152` | `0.0402688980` | `74744/2097152` | `0.0356407166` | `-0.0046281815` | `[-0.0072456598,-0.0023582816]` | `35/24` |
| `snr18_np4` | `47812/2097152` | `0.0227985382` | `44171/2097152` | `0.0210623741` | `-0.0017361641` | `[-0.0030241013,-0.0006393552]` | `28/31` |
| pooled `Np=2` | — | — | — | — | `-0.0064542294` | `[-0.0086839616,-0.0043308616]` | `86/29` |

逐窗 D 已逐项计算。为保留精确、可复核且不受小数格式影响的表示，下面列出 `delta_errors=C4_errors-B2_errors`；每窗 `payload_bits=32768`，所以 `D=delta_errors/32768`：

- `snr14_np2`: `[-196,-153,-95,-425,134,-39,-363,-1167,-139,386,0,-295,-864,-139,-309,-8,-275,-1563,31,0,-1334,0,-72,-482,-126,-203,-296,-2,-397,-365,-407,-162,-30,-136,81,-1672,-50,-17,3,-177,-315,-126,-49,-158,-44,-1766,-15,222,-8,-421,-266,-347,-63,-244,83,-49,-157,-24,0,-259,0,258,-2089,-205]`
- `snr14_np4`: `[-6,191,-1,-564,-60,84,1,-41,79,423,-444,-46,-265,114,-69,-157,-101,-696,2,4,-59,0,145,-402,-138,-25,0,-85,-173,-96,466,-5,-60,-42,-133,-39,0,90,-971,-449,-15,-246,-187,-299,-47,-466,-32,25,-168,-639,0,-397,19,-167,-437,-286,1,-38,-168,-2,-6,-731,-13,-6]`
- `snr18_np2`: `[0,-1,0,-98,0,0,0,4,-510,0,-314,-4,0,-1,-37,0,-271,-231,0,-1697,-11,-398,-469,-327,0,-50,16,1,0,-345,-305,-173,-2,-20,483,0,-7,-791,0,-104,0,0,-121,0,-8,-342,0,0,0,42,0,-2,-61,0,-62,-659,-1283,-74,0,-32,0,0,-660,-782]`
- `snr18_np4`: `[-343,0,-15,-3,0,0,-51,-2,0,0,92,-9,-2,0,1,0,0,0,-514,0,0,-17,0,0,-9,0,0,0,-1,-191,-571,-37,0,0,-2,0,-2,0,2,-344,-15,-18,0,0,44,0,0,0,-6,-4,-419,0,6,0,0,0,0,-331,0,-9,-837,-15,-5,-14]`

独立值与 `demapper_replay_aggregate.json` 和 receipt 逐字段一致。frozen gate 的 pooled `Np=2` CI upper 为 `-0.0043308616<0`；两个 `Np=4` cell 的 CI lower 分别为 `-0.0056052446<=0` 和 `-0.0030241013<=0`。

### Hash、truth firewall 与历史不变性

| artifact | 独立 SHA-256 |
|---|---|
| source manifest | `18c93796ff3e7e0ebf0bf05ee71c94bfd4027218b31a60d0d917d26581aa8a65` |
| source raw | `55c31e36b7d11e5d0b9e8225805596e0f0f7b127cde26874c7b0b217b0e23101` |
| source aggregate | `78e6795b17b1cfcbe5ee297c001e6e92bd81a6576c54ed317aeda526acbd17c9` |
| source receipt | `7508f61a6f30ade11e3770b819fcbda028726b8ef42f0c40e7152ad9b90be1e2` |
| replay manifest | `0a51d3604121d47d52383377ec445a4f57531d0bd5564c49d5e9da433b4ae081` |
| replay raw | `2330b61b5988c2467c720976bb757efade719247ef287271f756c5e73bd069d5` |
| replay aggregate | `6053422c2e904ff6d8b8479de504d92edd70a3af67586ef466a51379b334d6c1` |

source hashes 同时匹配 replay manifest、raw 和 receipt；replay manifest/raw/aggregate、runner、reducer 与 combined-tests hashes 全部匹配 receipt。manifest 冻结的 corrected `_modulation.py`、`development.py`、`scaled_unitary.py` 三个当前 SHA-256 也全部匹配。四个历史 `confirmation_*` 文件对 `HEAD` 的路径限定 `git diff --exit-code` 返回 `HISTORICAL_CONFIRMATION_UNCHANGED`。

truth firewall 以 AST 静态核查，不导入任务实现：`receiver_action` 参数恰为 `(arm,x_pilots,y_pilots,y_payload,parameter)`，函数体没有 `h_true`、`bits` 或 `realization` 名称；真值仅属于单列的 `O1` oracle 与离线 scoring。deployable arm 的机制量又与历史逐值完全一致，因此未发现真值泄漏或动作链漂移。

### Fresh checks

- task-control validator：`PASS`。
- focused tests：`27 passed in 5.52s`。
- 独立 raw→aggregate/receipt 对照：`INDEPENDENT_AGGREGATE_AND_RECEIPT_MATCH`。
- schema/count/bootstrap/gate：`SCHEMA_COUNTS_BOOTSTRAP_GATE_PASS`。
- historical artifact path diff：`HISTORICAL_CONFIRMATION_UNCHANGED`。

本结论只关闭 A1 historical-observation corrected-demapper replay；不表示 B3_PSC、A2 bridge、smoke、formal production 或论文 claim 已通过。

## Terminal

`DEMAPPER_REPLAY_PASS`
