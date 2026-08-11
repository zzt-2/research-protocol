# Task Brief: D0 ordinary domain authority + compiler repair

> 来源: D019 / V015 / T114–T115 | 产出位置: `projects/thesis-fso/worker-logs/step-162-d0-ordinary-domain-authority-repair.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_UNIT_TEST
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Scope / terminal

- 只改`contract.py`、`schemas.py`、`test_d0_contract_views.py`、`test_d0_ordinary_identity.py`并写step-162。owner/channel/其他tests/session/P05只读。
- owner YAML bytes、owner/scientific/identity seals、D0Contract四字段、旧FULL API、provenance/HMM/raw FULL均不改。
- 目标10分钟、15分钟硬停止；禁止install/commit/push/stage/benchmark/science/MVE。
- PASS=`D0_ORDINARY_DOMAIN_AUTHORITY_REPAIR_READY_FOR_INDEPENDENT_VERIFICATION`；不等于I05/FULL完成。

## Strict RED

1. 先只改tests，至少四项真实RED：typed `ordinary_domain` view缺失；module `CANDIDATES`等基数替换会改变plan；`_ordinary_raw_records`仍引用 globals/local literals；domain dataclass/seal tamper未拒绝。记录exit/stdout SHA。
2. 不能用故意错误计数或author-only helper造RED。

## Exact repair

1. 从已通过full-owner SHA认证的parsed root提取 frozen/slots `OrdinaryDomainAuthority`，只暴露ordinary compiler所需 exact tuples/maps：
   - controlled cell aliases（owner `controlled_fixture.cells` key order）；
   - polarization、fixture、candidate、S2 method、S4 check order（`statistical_contract_repair.enums`）；
   - tuple/B/Nw order（`dev_freeze_artifact_contract`）；
   - S2/S3/S4/BPS/B2-clean/B2-controlled record-type domain（各owner table schema）。
2. projection canonical payload/version固定在code，计算独立 SHA256；新增 frozen expected seal。`assert_frozen_owner_identity_authority`必须重算projection并对比seal，拒绝dataclass replace或seal spoof。不得暴露整份owner dict，不得import-time I/O。
3. `D0OwnerIdentityAuthority`增加typed domain field；`load_owner_identity_authority`在同一次explicit load中构造。owner bytes与已有三个seals不变。
4. `_ordinary_raw_records`只从`owner_authority.ordinary_domain`、authenticated identity binding与contract seed/population读取。函数源码中不得引用`CANDIDATES`、`S2_METHODS`或literal aliases/B/Nw/ordinary record types。
5. 修改任一schemas module global后，build结果必须与未改时逐对象相同；public assert不依赖该global。恢复global后结果同样一致。

## GREEN / regression

- exact counts/goldens/shared grouping仍=`42967/27487`；现有24 mutations全部fail closed，并新增domain replace/seal/global至少8项。
- 两次build nonprimitive sharing=0；wrong accept/reject=0/0。
- `test_d0_contract_views.py` + `test_d0_ordinary_identity.py`全绿；显式旧四文件53/53全绿，0 fail/error/skip/xfail/warning。
- 静态证明owner/YAML/science/identity seals/旧FULL/provenance无漂移；P0/P1/P2=`0/0/0`。

## Return

step-162记录RED/GREEN、counts/mutations/global-invariance、stdout SHA、final source/test/log SHA与保护项。只返回PASS terminal、FAIL或INCOMPLETE；首个不能在时间盒关闭的blocker立即收口。
