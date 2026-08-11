# Task Brief: D0 I05 FULL authority independent verification

> 来源: T098 / step-144 authority-only READY | 唯一产出: `projects/thesis-fso/worker-logs/step-145-d0-i05-full-authority-independent-verification.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: D0_TESTBED_IMPLEMENTATION
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## 身份、冻结输入与唯一写入

- fresh non-author verifier；只读 production/tests，缺陷只报告不修。
- 唯一允许创建 `projects/thesis-fso/worker-logs/step-145-d0-i05-full-authority-independent-verification.md`。

```text
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_schemas=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
step-144=05446c08a37258c84de4c53028219eb34805d08f5bc53d3c62442306e8e8b0f4
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

不得修改 source/tests/governance/其他日志；不得 install/commit/push/stage。

## 独立验收

1. 读 T098/T099、step-134/144、current schemas/tests与owner coverage/identity段；核 frozen hashes、HEAD/staging/P05/cache。
2. Fresh tests：三个 T098 exact节点；完整 schemas；aggregate全部 `test_d0_*.py`。0 fail/error/skip/xfail/warning。
3. Code review证明：
   - generic `RelationalManifest` 只能是PARTIAL，不能direct/replace/tamper成FULL并进入任一validator；
   - FULL type direct constructor不可用，factory不依赖module token/secret；
   - validator从manifest保存的authority spec重新compile canonical owner/extent/plans/tables/seal并逐字段比较，不只信任公开coverage digest；
   - owner exact identity assertion在factory与recompile path生效；FIRST/MAX及plan drift fail closed；
   - raw FULL positive path并未被本slice伪称为已验证，HMM/ledger binding仍open。
4. 独立 robustness cases≥50，含generic/full construction、replace/object tamper、owner/control/code/population/seed、extent、plan axes/entry、table/projection/count/key/multiplicity/coverage/seal、drop/add/substitute、改table后重算公开digest、FIRST/MAX crossing。另含合法PARTIAL与factory canonical FULL authority结构 controls；每例预标accept/reject，mismatch=0才可PASS。
5. Static/import/diff/boundary/hash/protection核验。不得因 tests GREEN 自动 PASS。
6. `VERDICT/P0/P1/P2`：P0/P1非零FAIL；required项未完成INCOMPLETE。PASS上限仅 `FULL_AUTHORITY_VERIFIED_POSITIVE_AND_BINDINGS_PENDING`。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

目标10分钟、15分钟硬停止；不 raw FULL bundle、benchmark/science/MVE/web。

## 返回

terminal=`FULL_AUTHORITY_VERIFIED_POSITIVE_AND_BINDINGS_PENDING`、`FULL_AUTHORITY_VERIFICATION_FAIL`或`INCOMPLETE`；附tests/cases/static/hash/protection与step-145 SHA。
