# Step 101 — D0 v2 资产合同 fresh-context 独立验收

> 2026-08-10 | T055 / CP011 / epoch 11 | `CONTRACT_STATIC_CHECK`  
> 证据 worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`  
> 边界：只读静态验收；只允许 duplicate-key YAML parse、hash 与确定性算术；未 import 项目、pytest、D0、仿真、benchmark、web/search/download、owner/源码/治理修改、commit 或 push

## 1. Findings first / verdict

```text
VERDICT = FAIL
P0/P1/P2 = 0/2/0
PRIMARY_TERMINAL = DEV_FREEZE_WEIGHT_AND_ARTIFACT_CONTRACT_OPEN
>7D_HARD_BLOCKER = NOT_ESTABLISHED
SCIENTIFIC_FIELD_DRIFT = NONE_FOUND_IN_SHA_BOUND_RECEIPTS
IMPLEMENTATION_UNIT_SCIENCE_AUTHORIZED_BY_THIS_VERIFIER = NO
```

v2 已关闭 step-096/098/099/100 的绝大部分数值、物理、数学与双账接口，且没有发现 truth 泄漏、factor-2、circular equalizer、非法八状态 rotation、raw exposure 偷减、decoder-state cache 或算术错误。仍有两个互相独立的 P1 阻断项：B2 statistic-pair 的 dev 权重没有唯一落到其 likelihood fit；BPS/B2 dev-freeze 没有具名、typed、可复算 artifact。它们允许同一 dev evidence 产生不同冻结参数，或只留下不可检查的 opaque hash，因此当前不能称为唯一可复算、禁止 test-time refit 的执行合同。

本 FAIL 不重开 population、seed、threshold、gate、baseline、strata 合取或 7 日预算，也不是 scientific terminal；不产生 governance-transfer acceptance token。

## 2. OPEN findings

### P1-1 — B2 statistic-pair 的 clean/controlled dev 权重未唯一绑定到 likelihood fit

**证据：**

- `b2_primary.implementation_contract.statistic_fit.likelihood` 只冻结 `full_pilot_forward_log_likelihood_normalized_per_pilot_then_equal_cell_macro`（YAML `:330-335`）。
- `b2_primary.dev_selection.strata_weight` 在另一个节点冻结 `clean:0.5 / controlled:0.5`（`:369-379`），但没有声明该权重也支配 `(p_s, sigma_e2)` 的 pilot-likelihood fit，还是只支配后续 tuple 的 macro net-goodput objective。
- 每 tuple 的 dev exposure 是 `120` clean dual-pol frames 与 `2160` controlled dual-pol frames。若 likelihood 在 cell 内按 trajectory 直接平均，clean/controlled 权重为 `1:18`；若继承 `strata_weight`，则为 `1:1`。两者都满足当前两段文字，却可冻结不同的 `(p_s, sigma_e2)`，继而改变 tuple、B2 LLR 与 test gate。

**处置：** `OPEN`。必须在 owner 中对 statistic fit 单独冻结 raw trajectory → polarization → cell → stratum → population 的精确聚合顺序，并明确 clean/controlled 是否为 `0.5/0.5`；不能依赖 dev-selection 邻接位置推断。

### P1-2 — common-BPS 与 B2 dev-freeze 没有具名、typed、可独立复算的 artifact

**证据：**

- common front end 要求“每个 legal tuple 先按 B1 选 `(B,Nw)`，B2 选 tuple 后冻结其对应 pair”，但只写 `frozen_before_any_d0_evaluator_seed: true`，没有 freeze record schema。
- B2 要求输出 `exactly_one_frozen_tuple_and_statistic_pair`，但没有定义该 record 的字段、主键、输入 dev rows/hash、聚合权重、objective/tie-break 复算值或 `test_rows_read=false`。
- `artifact_contract.required_files` 具名了 `s3_lambda_freeze.json`，却没有 common-BPS/B2 freeze artifact；receipt 只有未定义 canonical payload 的泛化 `freeze_sha256`（YAML `:812-817`）。因此 fresh reader 无法从交付 bundle 判断 hash 对应什么，不能复算 tuple/statistic/BPS pair，也不能证明 test path 未重拟合。

**处置：** `OPEN`。必须增加两个具名 typed records/files，或一个同等严格的组合 freeze artifact；至少绑定 contract/source/dev-row hashes、完整聚合权重、candidate grid、逐候选 objective、tie-break、唯一输出、`test_rows_read=false` 与 canonical SHA。

## 3. step-096/098/099/100 closure matrix

| 来源项 | 状态 | fresh-context 证据 |
|---|---|---|
| step-096 B1：互斥 typed raw tables、PK、nullability、finite/NaN 规则 | `CLOSED` | `s1_trajectory/s2_method/s3_candidate/s4_check` 及 lambda/ledger schema 均存在；strict types、extra forbid、JSON NaN/Inf forbid 已冻结。 |
| step-096 B2：60 target-pol off branches → 540 aligned projections，成本一次 | `CLOSED` | `30` channel realizations、`60` branches、`540` projections、每 branch `9`；同 random receipt、one computation/content hash、materialized charge once。 |
| step-096 B3：S1 actual 20/50 block bootstrap | `CLOSED` | first stage 抽 20/20；escalated 抽全部 50/50；每 stratum 独立 PCG64、10,000 reps、`method=linear`。 |
| step-096 B3：S3 case→cell→equal-cell macro、CI、88-CW cost | `CLOSED` | 每 split `540` cases、每 cell `180`、seed block `54`；dev-only lambda、test seed bootstrap、`88` changed CW 与 `72` cache reads均唯一。 |
| step-096 B3：B2 statistic-pair dev weight | `OPEN` | 见 P1-1；`1:18` trajectory weight 与 `1:1` stratum weight 均可从现文导出。 |
| step-096 B3：BPS/B2 freeze artifact 与 artifact recompute | `OPEN` | 见 P1-2；raw/S3 lambda/summary/ledger具名，但 BPS/B2 freeze 只有 opaque `freeze_sha256`。 |
| step-098：`f_G` provenance、combined linewidth、identity SOP | `CLOSED` | `f_G=100` 明标 project design choice；linewidth只作 effective-combined 一次；2×2 LS 不可达。 |
| step-098：prefix/pilot bytes/hash、named RNG、scalar receiver-only chain | `CLOSED` | NumPy 2.4.3 独立重算全部 prefix/pilot hashes；六 child spawn order固定；truth denylist完整。 |
| step-098：equalizer 单向性与 suffix scope | `CLOSED` | complex LS `RSS/31`；even-prefix选四态，odd-prefix估 `C_post`；`C_post` 禁止回馈；noiseless显式分支无 epsilon；suffix含后续 pilots，sentinel byte-identical。 |
| step-099：IC-02R/03R/06R | `CLOSED` | complex/per-real 分名、phase contribution只计一次、state exact + inner P08 max-log均已写入 authoritative implementation contract。 |
| step-099：Dirac/factor-2/single-state/covariance/uniform-state identities | `CLOSED` | 七项 mandatory identities齐全；独立数值复算 55/55 PASS。 |
| step-100：logical/materialized/HMM 双账与 cache边界 | `CLOSED` | 全部独立算术精确匹配；logical exposure保留，materialization才可降；S3不跨 candidate/case降成本；decoder message state禁复用。 |
| step-100：12分钟 future throughput gate | `CLOSED` | 覆盖 decoder `{4,8,12,16}`、六格 BPS、B2 十 unique-pol views、HMM primitive/aggregate、atomic JSONL/receipt I/O；只许 vectorization/batch/cache/checkpoint。 |

## 4. Deterministic evidence

### 4.1 Parse、hash 与字段断言

- 使用拒绝 duplicate key 的自定义 `yaml.SafeLoader`：PASS；top-level 为 mapping，无 duplicate key。
- v2 SHA256：`C3A471F50B770D4F366296AAB14034C60F9388CA6D476D9D4FC7458E33B9C0C6`，与 T055 冻结值一致。
- asset report SHA256：`D4BB9B4D6E2B41D9FD1A4ACBDBFA9D663D322C4F4F16CB606E58C6386FE45268`，一致。
- step-100 SHA256：`0D3664C1257FE80C599575B876AE054E375258EC20C8AFE8A700B30E65460E17`，一致。
- 定向字段/合同断言：59/59 PASS；科学 snapshot 数值断言：33/33 PASS。上述两个 OPEN 是跨节点 scope/缺 artifact 的语义缺口，不会被“字段存在”断言捕捉。
- control 的 `implementation_authorized/unit_test_authorized/execution_authorized/scientific_experiment_authorized` 为 `false/false/false/false`；本日志不改它们。

### 4.2 Prefix/pilot/physical formula 独立复算

- NumPy `Generator(PCG64(987654321))` 的 bits、labels、symbols、even/odd subsets 与四种 N 的 expanded pilot hash全部匹配；prefix mean energy=`1.0250000000000001`。
- `tau_c=1/(2*pi*100)=0.0015915494309189533 s`；`rho_block=0.999974867574596`。
- linewidth `10/20/80 kHz` 的 innovation variance分别为 `2.5132741228718347e-05 / 5.026548245743669e-05 / 2.0106192982974677e-04 rad^2`，与 owner 一致。

### 4.3 数量与成本独立复算

```text
pre-S4 logical exposure       = 69,360 batches / 1,032,000 CW / 20,640,000 BP iter
materialized upper bound      = 48,900 batches /   704,640 CW / 14,092,800 BP iter
HMM aggregate logical         = 8,344,800 dual-pol frame-parameter-pair scores
HMM primitive logical         = 16,689,600 pol-trajectory-parameter-pair scores
HMM primitive materialized UB = 7,027,200
```

分项重算为 BPS logical `28,800/460,800/9,216,000`、B2 logical `22,800/364,800/7,296,000`、S2 `6,960/111,360/2,227,200`、S3 dev/test 各 `5,400/47,520/950,400`；全部 exact。cache 规则只降低 materialized work，未删除 raw seed/cell/tuple/grid/fixture/candidate exposure或 nominal method cost。

## 5. Scientific drift audit

v1 blob 未另存为可 byte-diff 文件；按 T055 指定，使用 pre-repair SHA `32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936` 及 step-096/098/100、A0 report 的 SHA-bound receipt逐项对照。

| Scientific family | Drift | v2 对照 |
|---|---|---|
| Q1/purpose/result ceiling | `NO` | 仍为 no-policy D0，非 MVE、非 C1 extension。 |
| population/code | `NO` | Gray-16QAM、X/Y、1024/1536、16 CW/pol、384 sym/CW、20 iter不变。 |
| physical axes | `NO` | 4 SNR ×3 linewidth、CFO=0、GG `(1.0,0.7)` 不变；`f_G/SOP/linewidth identity` 是固定投影而非新增 axis。 |
| seeds/disjointness | `NO` | 8000–8349 的各 slice/range不变。 |
| BPS/B2 identities与 grids | `NO` | BPS 6-grid、OFC17五 tuple、pilot counts、p_s/sigma grids、test-time best-of禁令不变；IC corrections只消除旧数学矛盾。 |
| B0/B1/B2/O1 ladder | `NO` | 语义 ID、receiver/truth 边界与 full restart不变。 |
| controlled cells/fixtures | `NO` | hard/mid/clean、boundary 4/8/12、rotation 1/2/3、target-pol/sentinel不变。 |
| S1–S4 exposure/threshold/gates | `NO` | occurrence、damage、recoverability、90/95 coverage、S3 top1/MRR、S4七项及总合取不变。 |
| budget/post-D0 boundary | `NO` | D0 `4.50 d`、post-D0 `2.00 d`、contingency `0.50 d`、hard ceiling `7.00 d`不变。 |
| control metadata | `INTENTIONAL_NON-SCIENCE_CHANGE` | v2 暂停全部 implementation/unit/execution/science flags，等待 fresh verification后的新 D/V/CP；本 FAIL 维持暂停。 |

## 6. Budget verdict

```text
BUDGET_CLASS = BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK
NO_NECESSARY_WORK_PROVEN_OVER_7D = TRUE
```

静态 operation count不能换算墙钟天数；v2 的 future gate已覆盖 decoder/BPS/B2/HMM/I/O，且只允许工程调度参数。两个 OPEN 是合同闭合工作，不授权删除 exposure/gate，也未静态证明必要工作 `>7 d`。

## 7. Protection receipt

- owner start/end expected invariant：
  - `d0-defect-smoke-contract.yaml=C3A471F50B770D4F366296AAB14034C60F9388CA6D476D9D4FC7458E33B9C0C6`
  - `d0-asset-preflight.md=D4BB9B4D6E2B41D9FD1A4ACBDBFA9D663D322C4F4F16CB606E58C6386FE45268`
- protected p05 start/end expected invariant：
  - `p05_run.log=7843B048A2A79755C95542A438A5344F8E89E791113F48913926C419FC2A4F11`
  - `p05_run2.log=735E4650093D297E01A0E6DFE28F0431C149A2931FCBB7C08EECFA28F0AAC38B`
  - `p05_run3.log=C76887C6950AAAC2B4C0DCED7689517749322C44DA868880915786C173B1344D`
  - `p05_run4.log=95A1D184740A797B6D55D7F817008C898CB3754987AB6E1C1D00376F74A621DE`
- staging 启动为空；目标文件启动时不存在。
- 本任务唯一写入：`projects/thesis-fso/worker-logs/step-101-d0-asset-contract-verifier.md`。
- 未修改 owner、A0、D010/V004/CP011、源码、测试、结果、p05 或其他治理文件；未 commit/push。

## 8. Terminal

```text
VERDICT = FAIL
P0/P1/P2 = 0/2/0
NEXT_LEGAL_ACTION = REPAIR_ONLY_THE_TWO_DEV_FREEZE_CONTRACT_GAPS_THEN_FRESH_REVERIFY
```
