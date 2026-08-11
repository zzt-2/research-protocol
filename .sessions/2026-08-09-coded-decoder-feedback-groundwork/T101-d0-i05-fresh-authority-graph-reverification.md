# Task Brief: D0 I05 fresh authority graph independent reverification

> 来源: T099 FAIL / T100 repair / step-145–146 / D014 | 唯一产出: `projects/thesis-fso/worker-logs/step-147-d0-i05-fresh-authority-graph-reverification.md`
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

- non-author verifier；只读final source/tests，缺陷只报告不修。
- 只创建 `projects/thesis-fso/worker-logs/step-147-d0-i05-fresh-authority-graph-reverification.md`。

```text
schemas.py=a42ffa184d2db3cfa68775b9dc0b3aac60195bf34abfdf5e37732f398445e401
test_schemas=a94731c3c9d44c1f0ba8ef1b27df578cbb9f982f3069f51786f3becc419dd4c9
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
step-146=e39b7f2b3c548c3200ac46ae65a400821f4270e82729e92c9163e247f71729b7
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

不得修改source/tests/governance/其他日志；不得 install/commit/push/stage。

## 独立验收

1. 读T100/T101、D014、step-145/146与final source/tests；核frozen hashes/保护。
2. Fresh tests：两个T100 exact、schemas全文件、aggregate全部`test_d0_*.py`；0 fail/error/skip/xfail/warning。
3. 精确重放step-145：改变一次factory结果的authority SHA、table、nested projection后，该对象必须被gate拒绝；随后同spec factory/validator输出仍canonical，digest独立复算一致。
4. 独立isolation matrix≥70，跨FIRST/MAX、至少两套合法HMM/computation plan；逐层检查Full/spec/cell/seed/table/projection object identities。允许共享的只有caller提供的authority inputs与immutable primitives；任何canonical output dataclass/list/object不得跨compile共享。
5. 审计所有`lru_cache`/memoization：返回值递归只能由exact immutable primitives组成，不含dataclass、list/dict/set、ndarray或自定义对象；不得依赖`cache_clear`。改变一个output graph后至少10轮后续compile均无漂移。
6. 回归T099正常88类authority cases的代表集≥35，并保留PARTIAL/FULL structural controls。raw positive、HMM/member、consumer-ledger必须仍标OPEN。
7. Static/import/diff/hash/P05/cache/HEAD/staging保护。`VERDICT/P0/P1/P2`；P0/P1非零FAIL，缺项INCOMPLETE。PASS上限仅`FULL_AUTHORITY_VERIFIED_POSITIVE_AND_BINDINGS_PENDING`。

## 固定环境与禁令

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

目标10分钟、15分钟硬停止；不raw FULL bundle/benchmark/science/MVE/web。

## 返回

terminal=`FULL_AUTHORITY_VERIFIED_POSITIVE_AND_BINDINGS_PENDING`、`FULL_AUTHORITY_VERIFICATION_FAIL`或`INCOMPLETE`；附tests/isolation/static/protection与step-147 SHA。
