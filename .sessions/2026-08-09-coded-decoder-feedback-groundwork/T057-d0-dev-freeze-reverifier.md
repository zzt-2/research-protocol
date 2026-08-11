# Task Brief: D0 v3 dev-freeze 两项 P1 fresh narrow reverifier

> 来源: step-101 FAIL + step-102 repair design | 产出位置: `projects/thesis-fso/worker-logs/step-103-d0-dev-freeze-reverifier.md`
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

- 假设：v3 只以 step-102 的 additive artifact/estimand closure关闭 step-101 P1-1/P1-2，其他 step-096/098/099/100 CLOSED项与 scientific fields均未漂移。
- 否决条件：HMM仍可导出非 0.5/0.5 权重；sentinel进入 objective或从 ledger消失；goodput仍有bit-vs-CW歧义；dev winner不能由具名 artifacts精确复算；test path可调用fit；普通float chunk sum可改变winner；或 repair偷改 seed/grid/gate/exposure，均 FAIL。

## 冻结输入

- v3 owner SHA：`6924842C5696E80BCF8EFA24BC63F005D7A78BA63F959C768E0183DE85C81F54`。
- asset report SHA：`E008C0F0B78772A80201D4969359ED34D655D79ED37614652746E911EBBC01F1`。
- step-101 SHA：`D103A17DDA0FBBE1C86C8B073E614BEF36FEE7EC4CFC008D6C164472F5CB0D20`。
- step-102 SHA：`077D0B9337769A7185E665E8D05F4B448E6EFB9CB5CDC179E90E2107A94A1A76`。

## 任务

1. 完整读取 T057、v3 owner、asset report、step-101与step-102；对 step-101 两个 P1逐项给 CLOSED/OPEN。仅在需要核对 no-drift 时回读 step-096/098/099/100/A0。
2. 用 duplicate-key拒绝 loader parse，并独立复算：BPS raw7200；HMM logical/include/sentinel=`16,689,600/8,784,000/7,905,600`；B2 clean/control=`1,200/21,600`；logical/materialized D0总数保持原值。
3. 验证唯一 estimand：整CW成功交付bits、symbols denominator、BPS clean两pol→cell→12cell、HMM/B2 half clean + half controlled-target、sentinel excluded from objective but output/receipt/cost required。
4. 验证 HMM exact aggregate足以 lossless复算且 ordinary float sum forbidden；dev manifest列 float64 hex/grid/membership；缺PK fail closed。
5. 验证7个新增具名 artifacts、五BPS+五stat+一tuple freeze、candidate objective/tie/raw hash与 chronology lock；S3 dev可用 resolved freeze但不能 refit。
6. 抽核 repair只改 schema/status/selection artifact接口，scientific population、seed、tuple/grid、S1–S4 threshold/gate、logical/materialized exposure、budget均无 drift。
7. 输出 `PASS/FAIL, P0/P1/P2`；仅 PASS 可写 `ASSET_CONTRACT_ACCEPTABLE_FOR_GOVERNANCE_TRANSFER`。PASS不自行授权 implementation/unit/science。
8. owner/report初末SHA、p05 4/4、staging与唯一写入终检。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-103-d0-dev-freeze-reverifier.md`。
- 只读；允许 parse/hash/算术，禁止 import项目、pytest、D0/仿真/benchmark、web/search/download、owner/源码/治理修改、commit/push、p05触碰。
- 10 分钟目标，15 分钟硬上限。

