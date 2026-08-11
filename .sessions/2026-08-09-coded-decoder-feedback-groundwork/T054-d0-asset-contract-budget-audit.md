# Task Brief: D0 资产合同与预算闭合审计

> 来源: step-094–step-099 / D0 YAML | 产出位置: `projects/thesis-fso/worker-logs/step-100-d0-asset-contract-budget-audit.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 11
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：step-097 的统计闭合与下列最小物理投影能够在不改变 12-cell population、scientific gates、seed ranges 或 OFC17 baseline 身份的前提下形成唯一可实现合同；dev 计算量可通过共享 realization、缓存接收机前端及批量 decoder 调用留在既有 4.50 日 D0 点估计内。
- 否决条件：若计数存在重复/漏项，任何合法降本必须删减冻结 exposure/gate，物理选择新增未登记轴或 truth，B2 修正不能与 P08 逐点 identity 共存，或保守估计显示必要总工时加 contingency 必然 `>7.00 d`，则不得判闭合。

## 待审拟冻结选择

1. `f_G=100 Hz`，理由是 `params.py` 是 canonical parameter owner；`adaptive-phase-window/channel.py` 的局部默认 `500 Hz` 不作为新的 population 轴。`tau_c=1/(2*pi*f_G)`，GG `block=100, method=gar`。
2. YAML 的 `{10,20,80} kHz` 解释为一次性进入 Wiener innovation 的 **effective combined phase-process linewidth**；不得按 Tx/LO 再加倍。symbol 0 前状态为 0，再生成第一个 innovation；CFO=0。
3. `identity_no_cross_pol_mixing + scalar_per_pol_receiver_front_end`；不继承 P08-R2 rank-deficient 2x2 LS，不新增 SOP/Jones 轴。
4. prefix 使用 P08 `CalibrationPrefix(length=32, seed=987654321)` 的 Gray-16QAM 序列，X/Y 相同但分别 receipt；periodic pilot 使用 deterministic unit-energy QPSK cycle `[(1+j),(1-j),(-1+j),(-1-j)]/sqrt(2)`，X/Y 相同。
5. receiver-only scalar front end：每 pol 在 32-symbol known prefix 上做 complex LS 得 `g_pre` 与 pre-EQ complex residual power；每 100-symbol block 用 observed power minus该 residual估计 nonnegative signal power，做 scalar MMSE amplitude equalization和 `amp_limit=3`；其后 common BPS，再由已知 prefix 计算 post-BPS complex residual power。不得读取 true `h/SNR/phase/payload`。
6. RNG 为 `SeedSequence(root_seed).spawn` 固定顺序 named substreams：`payload_x,payload_y,gamma_gamma,wiener,awgn_x,awgn_y`；paired methods/no-jump twin复用相同 realization，只有受控 fixture copy-on-write。
7. B2 采用 step-099 的 IC-02R/03R/06R：complex/per-real 明确分名，moment-consistent phase/noise split，state exact marginalization + bit-set内 P08 max-log，single-state preclip 与 P08(`sigma2=N0_complex/2`)逐点同值。

## 任务

1. 完整读取 step-094–099、D0 YAML、相关 source closure/params/P08/common assets；逐项判断上述选择是否唯一、receiver-only、source-compatible，必要时给最小替换文本。
2. 独立复算 step-097 的 BPS-dev、B2-dev、S2、S3-dev/test cardinality/cost。区分 physical realization、method frame、decoder batch call、CW decode、BP iteration、HMM candidate evaluation、cache read。
3. 查明 `pre_S4=69,360 calls / 1,032,000 CW / 20,640,000 BP iter` 是否重复计费或漏项；列出不改 exposure/gate 的确定性共享、缓存和 batching 边界。禁止靠缩 seed/cell/tuple/grid/fixture/candidate 降本。
4. 对 4.50/7.00 日边界给 `NO_BLOCKER_EVIDENCE / BUDGET_RISK_REQUIRES_BOUNDED_BENCHMARK / >7D_HARD_BLOCKER`；不得从 operation count 臆测 wall time。
5. 给 owner-ready 的 prefix/pilot canonical receipt 规范；如可在不 import 项目、不跑仿真的前提下确定，复算 bits/labels 或 canonical float encoding 的 SHA256，并写算法/字节序。
6. 最终 verdict 仅可为 `ASSET_CONTRACT_READY / ASSET_CONTRACT_READY_WITH_CORRECTIONS / CONTRACT_AMBIGUITY / >7D_HARD_BLOCKER`。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-100-d0-asset-contract-budget-audit.md`。
- 只读仓库输入；允许纯确定性算术/哈希脚本，不允许 import 项目、pytest、D0/仿真/benchmark、web/search/download、owner/源码/治理修改、commit/push、p05 触碰。
- 必须复核 owner 初末 SHA、四个 protected p05 SHA 与 staging；12 分钟目标，15 分钟硬上限。

