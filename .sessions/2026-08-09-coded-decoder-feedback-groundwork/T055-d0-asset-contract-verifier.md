# Task Brief: D0 v2 资产合同 fresh-context 独立验收

> 来源: step-094–100 / D0 v1→v2 candidate | 产出位置: `projects/thesis-fso/worker-logs/step-101-d0-asset-contract-verifier.md`
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

- 假设：D0 YAML v2 与 `d0-asset-preflight.md` 只闭合 step-096/098/099/100 暴露的实现接口，未改变 v1 的 scientific population、seed、threshold、gate、strata合取、test-time best-of禁令或 post-D0 边界，并已成为唯一可复算、可实现的 D0 contract。
- 否决条件：任何旧歧义仍可产生两种合法执行/相反裁决；出现 truth泄漏、factor-2、circular equalizer、非法 rotation、统计行/成本双计；logical/materialized cache偷减科学 exposure；或必要工作已静态证明 `>7 d`，均判 FAIL。

## 冻结输入

- v1 pre-repair SHA：`32989FFA52A38FD813C9D0E4DA6951FBCA66AD30AC5D56EAD24D9AE466595936`（由 step-098/100 receipt 承担）。
- v2 candidate SHA：`C3A471F50B770D4F366296AAB14034C60F9388CA6D476D9D4FC7458E33B9C0C6`。
- asset report SHA：`D4BB9B4D6E2B41D9FD1A4ACBDBFA9D663D322C4F4F16CB606E58C6386FE45268`。
- step-100 SHA：`0D3664C1257FE80C599575B876AE054E375258EC20C8AFE8A700B30E65460E17`。
- verifier 启动后两份 candidate owner 必须只读且初末 SHA 不变。

## 必查项

1. 完整读取 step-094–100、v2 YAML、asset report、A0 report与 D010/V004/CP011；不得只读摘要。
2. 用拒绝 duplicate-key 的 YAML loader parse；逐条确认 step-096 B1/B2/B3：typed raw tables、60 target-pol off branches→540 logical projections/成本一次、S1 actual 20/50 blocks、S3 case→cell→macro estimand/CI/cost与artifact recompute全部闭合。
3. 逐条确认 step-098：`f_G` provenance label、effective-combined linewidth、identity SOP、prefix/pilot bytes/hash、named RNG、scalar receiver-only equalizer、pre/post variance units、suffix包含后续pilots，且没有 true h/SNR/phase/payload进入 ReceiverView。
4. 专审 equalizer单向性：complex LS `RSS/31`；even prefix选四状态、odd prefix估 `C_post`；`C_post`不能回馈equalizer；noiseless branch无未登记epsilon。
5. 逐条确认 step-099：IC-02R/03R/06R、Dirac、factor-2 magnitude negative control、single-state数值identity、两种不混用的 rotation covariance、uniform-state bit identity。
6. 独立复算 logical `69,360/1,032,000/20,640,000`、materialized upper bound `48,900/704,640/14,092,800`、HMM aggregate/primitive/materialized `8,344,800/16,689,600/7,027,200`；判断所有cache是否只减少materialization、不删raw exposure/nominal method cost或复用decoder state。
7. 对照 v1 receipt/A0 report逐项列出 scientific fields是否 drift。top-level pending control flags必须全 false；本 verifier PASS 也不得自行授权 implementation/unit/science。
8. 审查12分钟 future throughput gate是否覆盖 decoder/BPS/B2/HMM/I/O，且只能调batch/vectorization/cache/checkpoint；给 budget verdict。
9. 复核 protected p05 4/4、staging、owner初末SHA与本任务唯一写入。

## 输出

- `VERDICT=PASS/FAIL`；P0/P1/P2精确计数。
- 对 step-096/098/099/100 每项给 `CLOSED/OPEN` 表。
- 仅 PASS 时可写 `ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER`；这不等于授权或科学结果。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-101-d0-asset-contract-verifier.md`。
- 只读；允许纯确定性 parse/hash/算术，禁止 import项目、pytest、D0/仿真/benchmark、web/search/download、owner/源码/治理修改、commit/push、p05触碰。
- 12 分钟目标，15 分钟硬上限。

