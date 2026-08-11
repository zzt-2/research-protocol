# Step 103 — D0 v3 dev-freeze 两项 P1 fresh narrow reverification

> 2026-08-10 | T057 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 证据 worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> 边界：只读 parse/hash/确定性算术与静态语义复核；唯一写入本日志。未 import 项目、pytest、D0、仿真、benchmark、web/search/download，未修改 owner、源码、测试、结果、治理或 p05，未 commit/push。

## 1. Findings first / verdict

```text
VERDICT = PASS
P0/P1/P2 = 0/0/0
STEP_101_P1_1 = CLOSED
STEP_101_P1_2 = CLOSED
SCIENTIFIC_FIELD_DRIFT = NONE_FOUND_IN_CHECKED_FAMILIES
>7D_HARD_BLOCKER = NOT_ESTABLISHED
TERMINAL = ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER
IMPLEMENTATION_UNIT_BENCHMARK_SCIENCE_AUTHORIZED_BY_THIS_VERIFIER = NO
```

v3 以 additive artifact/estimand closure 唯一关闭 step-101 的两个 P1：HMM statistic fit 已把 clean 与 controlled-target 的 `0.5/0.5` 权重、target/sentinel inclusion 和逐层 reduction 绑定到同一 authoritative artifact；common-BPS、HMM grid 与 final B2 tuple 已有具名 typed evidence、精确候选 key/raw hash、五 BPS + 五 statistic + 一 tuple freeze，以及 test-path chronology lock。

该 PASS 接收的是**实现前静态合同**。七个新增 artifact 是必须实现和验证的接口，并非已生成的科学 artifact；owner 的 implementation/unit/execution/science flags 仍为 `false/false/false/false`。本日志不自行授权 implementation、unit test、12 分钟非科学 throughput benchmark 或 S1–S4。

## 2. 冻结输入、parse 与保护前提

四个 T057 冻结 SHA 均逐 byte 匹配：

| 输入 | SHA256 |
|---|---|
| `d0-defect-smoke-contract.yaml` v3 | `6924842C5696E80BCF8EFA24BC63F005D7A78BA63F959C768E0183DE85C81F54` |
| `d0-asset-preflight.md` | `E008C0F0B78772A80201D4969359ED34D655D79ED37614652746E911EBBC01F1` |
| step-101 | `D103A17DDA0FBBE1C86C8B073E614BEF36FEE7EC4CFC008D6C164472F5CB0D20` |
| step-102 | `077D0B9337769A7185E665E8D05F4B448E6EFB9CB5CDC179E90E2107A94A1A76` |

- 使用自定义 `yaml.SafeLoader` mapping constructor，在构造 mapping 时拒绝重复 key；v3 完整 parse 为 mapping，PASS。
- 另用 `a: 1 / a: 2` 负样例验证同一类 loader：抛出 `ConstructorError`，`DUPLICATE_KEY_NEGATIVE_CONTROL=PASS_REJECTED`。
- 定向静态断言共 `94/94 PASS`、`0 FAIL`；覆盖 hash、P1 closure、count、estimand、exact aggregate、freeze chronology、scientific no-drift snapshot 与 budget/control boundary。

## 3. step-101 两项 P1 closure

### P1-1 — HMM clean/controlled 权重与 likelihood fit：`CLOSED`

1. `b2_primary.implementation_contract.statistic_fit.aggregation` 明确固定：trajectory normalized NLL → `(stratum,cell,pol)` complete mean → equal X/Y → equal 12 cells → `0.5 clean + 0.5 controlled-target`；controlled sentinel scored/receipted 但从 objective 排除（owner `:331-339`）。
2. authoritative `dev_freeze_artifact_contract.aggregation` 再次机器化固定 `strata={clean:0.5, controlled_target:0.5}`、clean 两 pol、controlled target-only、sentinel `objective_included=false` 且 output/receipt/cost required（`:844-853`）。
3. `b2_statistic.reduction` 与上述层级一致，lexicographic key 为 combined normalized NLL → smaller `p_s` → smaller `sigma_e2`（`:991-1001`）。缺 primary-key rows 必须 fail closed，不允许对剩余行重归一化（`:844`）。

因此 step-101 指出的 `1:18 trajectory weight` 与 `1:1 stratum weight` 分叉已消失；唯一合法 statistic estimand 为 `0.5/0.5`。

### P1-2 — BPS/B2 具名 typed、可复算 artifact：`CLOSED`

v3 新增并全局列入 required files 的七个 artifact 为：

```text
dev_manifest.json
raw_bps_dev.jsonl
hmm_grid_dev_chunks.jsonl
raw_b2_tuple_clean_dev.jsonl
raw_b2_tuple_controlled_dev.jsonl
dev_freeze.json
dev_freeze_receipt.json
```

四张 typed evidence table 分别在 owner `:855-983`；freeze 明确输出 exactly five BPS pairs、five statistic pairs、one final tuple，并保存每个 candidate 的 exact objective/lexicographic key、raw hash binding、`test_rows_read=false`（`:1014-1023`）。manifest、chronology、七文件与 receipt hash 接口位于 `:1024-1057`，全局 required-files/validator 位于 `:1058-1063`。

`dev_freeze_receipt` 绑定 contract/source/code/dev manifest、四张 dev evidence、freeze 与 selection code；因此不再存在只留 opaque `freeze_sha256`、无法判定 payload 身份的问题。

## 4. 独立数量与双账复算

### 4.1 Dev evidence cardinality

```text
BPS raw
  = 5 tuples × 6 BPS pairs × 10 seeds × 12 cells × 2 pol
  = 7,200

HMM primitive logical
  = 5 × (122×6) statistic pairs × 12 × 2 × (10 clean + 90 target + 90 sentinel)
  = 16,689,600

HMM objective included
  = 5 × 732 × 12 × 2 × (10 clean + 90 target)
  = 8,784,000

HMM sentinel scored but objective excluded
  = 5 × 732 × 12 × 2 × 90
  = 7,905,600

B2 clean raw
  = 5 × 10 × 12 × 2
  = 1,200

B2 controlled raw, target+sentinel
  = 5 × 10 × 12 × 2 target-pol × 9 fixtures × 2 row-pol
  = 21,600
```

上述六个值均与 owner `exact_cardinality` / HMM three-count fields 精确相等（`:858,920-923,927,951,996-998`）。controlled 21,600 再唯一拆为 target included `10,800` 与 sentinel excluded `10,800`。

### 4.2 原 logical/materialized D0 totals 未漂移

| 双账 | decoder batches | CW decodes | BP iterations |
|---|---:|---:|---:|
| logical：BPS+B2+S2+S3-dev+S3-test | 69,360 | 1,032,000 | 20,640,000 |
| materialized upper bound：同五项 | 48,900 | 704,640 | 14,092,800 |

两行均由五个分项重新相加得到，并与 owner `:813-824`、step-100 frozen receipt 一致。HMM dual-pol aggregate logical=`8,344,800`、primitive materialized UB=`7,027,200` 亦保持原值。cache 只改变 materialized work，不删除 logical seed/cell/tuple/grid/fixture/candidate exposure或 nominal method cost。

## 5. 唯一 estimand 与 exact recomputation

### 5.1 Goodput 与 aggregation

- 一个 CW 仅在 1024 个 information bits 全部正确时成功交付；`delivered_bits=1024×successful_cw_count`，不能用 `information_total-information_errors` 冒充（owner `:836-842`）。
- per-pol symbol denominator 为 `32 prefix + 6144 coded-data + periodic/terminal pilots`。独立按 `1+ceil(6144/(N-1))` 复算，`N=10/20/100/200` 的 pilots 为 `684/325/64/32`，总 symbols 为 `6860/6501/6240/6208`。
- BPS 只用 clean、两 pol；先 `(cell,pol)` ratio-of-integer-sums，再 equal X/Y、equal 12 cells。
- HMM 与 final B2 均为 half clean + half controlled-target；controlled sentinel 不进入 objective，但其 score/output、content/source receipt 与 logical/materialized cost ledger 均不得消失。

该定义排除了 bit-vs-CW goodput 分叉，也排除了把 sentinel 纳入 controlled half 后形成 `0.75 clean + 0.25 target` 的错误权重。

### 5.2 HMM exact aggregate 的充分性

每条 trajectory 先生成 canonical binary64 `-logL/pilot_count`。binary64 是精确二进制有理数；每个 chunk 保存 decimal integer numerator、power-of-two denominator、member count、member-key manifest hash和 computation manifest hash（owner `:889-923`）。后续 selector 只执行按已冻结 group 的线性 sum/count、equal-pol、equal-cell和固定 `1/2` strata 权重，故这些 exact rational aggregates 对 winner 是 lossless sufficient statistics；不需要为复算 winner 持久化全部 16,689,600 条 trajectory score。

普通顺序相关 float chunk sum 在 schema invariant 与 authoritative selector 中双重禁止（`:917,994-995`）。member keys 必须 complete/disjoint/exactly-once；manifest 必须列完整 dev seed、12 cells、tuple/order、六 BPS pair、全部 `p_s/sigma_e2` index+float64-hex、枚举及 expected PK/cardinality（`:1024-1034`）。因此换 chunk order、遗漏 PK 或用普通 float sum均不得产生合法 freeze，更不能改变 winner。

## 6. Winner、tie 与 chronology lock

三个 exact lexicographic selectors 为：

1. per-tuple BPS：maximize macro net-goodput → minimize full-frame CWER → lower B → lower Nw；
2. per-tuple HMM pair：minimize combined normalized NLL → smaller `p_s` → smaller `sigma_e2`；
3. final B2 tuple：maximize half-clean/half-target macro net-goodput → lower pilot fraction → lower controlled-target affected CWER → lower M → earlier legal tuple order。

`dev_freeze.json` 必须保存全部 candidates 的 exact objective/tie key 与 raw hash，而非只保存 winner。test runner只接收 `ResolvedDevFreeze`；fit functions `[fit_common_bps, fit_b2_statistics, select_b2_tuple]` 在 test call graph 不可达；BPS/B2 fit 只接受 `common_cpr_and_b2_dev`；所有 evaluator seed ranges 从 fit API fail closed；S3 dev 明确只消费 resolved BPS/B2 freeze、不得 refit；S1/S2/S3-dev/S3-test/S4 receipts 均反向绑定同一 dev-freeze SHA（owner `:1035-1041`）。

## 7. Repair no-drift 抽核

除 schema/status/control metadata 与 selection-artifact 接口外，未发现被 T057 禁止的 drift：

| family | v3 抽核结果 |
|---|---|
| population/code | Gray-16QAM、X/Y、1024/1536、16 CW/pol、384 symbols/CW、20 iterations保持 |
| physical cells | `4 SNR × 3 linewidth = 12`；CFO/GG/fG/SOP投影不变 |
| seeds | 8000–8349 的八个命名 disjoint ranges逐项保持 |
| grids | BPS `2×3=6`；五 B2 tuples；HMM `122×6=732` 保持 |
| S1–S4 | occurrence `12/4/2`、S2 damage/recovery `0.10`、coverage `0.90/0.95`、S3 top1/MRR、S4 七项及 final conjunction保持 |
| exposure | BPS/B2/S2/S3 logical/materialized分项及总数保持 |
| budget | D0 `4.50 d`、post-D0 `2.00 d`、contingency `0.50 d`、hard ceiling `7.00 d`保持 |

owner 同时显式写 `scientific_threshold_seed_and_gate_change: none` 与 `scientific_contract_change: none`；本复核没有仅依赖这两个声明，而是把上述 numeric snapshot 与 step-096/098/099/100、A0/step-101/102 receipt 定向交叉检查。schema升至 v3、status改为 pending fresh reverification、四个 authority flag保持 false属于 intentional non-science change。

## 8. Protection / terminal receipt

- owner/report 初末 SHA：分别保持 `6924842...C81F54` / `E008C0F0...BC01F1`。
- protected p05 初末 `4/4 MATCH`：
  - `p05_run.log=7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log=735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log=C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log=95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
- staging 启动/终检均为 `0`；目标启动时不存在。
- 本任务唯一写入：`projects/thesis-fso/worker-logs/step-103-d0-dev-freeze-reverifier.md`，新增、未暂存。
- 未修改 owner/report、A0、step-101/102、源码、测试、结果、治理或 p05；未 commit/push。

```text
VERDICT = PASS
P0/P1/P2 = 0/0/0
STEP_101_P1_1 = CLOSED
STEP_101_P1_2 = CLOSED
TERMINAL = ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER
NEXT_AUTHORITY = NEW_D_V_CP_MAY_LIMITEDLY_AUTHORIZE_IMPLEMENTATION_AND_UNIT_TEST; THIS_LOG_DOES_NOT
```
