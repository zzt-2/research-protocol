# Task Brief: D0 I05 fresh authority graph repair

> 来源: T099 / step-145 `FAIL 0/1/0` / D014 | 产出位置: `projects/thesis-fso/worker-logs/step-146-d0-i05-fresh-authority-graph-repair.md`
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

## Scope / hypothesis / terminal

- 只修复 step-145 shared cached canonical reference；不做raw positive/HMM/ledger binding。
- 假设：移除或重构整个canonical output graph中的object-returning cache，使factory与validator每次得到fresh object graph，即可关闭P1。
- 否决：仍复用任何可改变dataclass/table/projection实例；依赖清cache时序/token；需改owner/其他模块；或15分钟不收敛。
- PASS上限仍为 `FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`。

## 冻结输入

```text
schemas.py=776c2850e874cfbb953a50166af0ca6f7b09aa8fbc3148e9efa1977864134a51
test_schemas=385e242764fb7e510e1309f936d7adeaad984c44aa2e409b57edd5a76ac36f77
step-144=05446c08a37258c84de4c53028219eb34805d08f5bc53d3c62442306e8e8b0f4
step-145=1d0a4c61b4174a5db9b4816d616c53358ff81044276aa11f017a8366f046eb8e
D014 decisions=b252a47fa6a5d52b1c906c2fb8f71562c7ab9c0f95f749fac99c1517912e251e
contract.py=a656a2ed2346cf2175fc58744ae0c832767ee29281362a308829cb1dc008d4b1
owner=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
HEAD=715a65884b988ee737f21982f3bbf372860a1da8
```

## 唯一允许写入

1. Modify `projects/simulation/explore/coded-decoder-feedback/schemas.py`
2. Modify `projects/simulation/tests/test_d0_schemas_statistics.py`
3. Create `projects/thesis-fso/worker-logs/step-146-d0-i05-fresh-authority-graph-repair.md`

不得修改owner/contract/其他source/governance；不得raw bundle/benchmark/science/install/commit/push/stage。

## Strict TDD

1. 读T100、D014、step-145/144与current source/tests；核frozen hashes/protection。
2. production前新增exact nodes：
   - `test_full_manifest_cached_canonical_isolation`
   - `test_full_manifest_recompile_uses_fresh_authority_graph`
   两节点必须在当前production真实RED；立即先写step-146 RED receipt，再改production。
3. 修复整个transitive canonical graph：`_compile_full_relational_manifest`、`_hmm_expectation`及任何下游cache不得返回并复用FullManifest/TableExpectation/IdentityProjection等对象实例。每次factory/recompile的output graph必须fresh；跨调用对应table/projection不得identity共享。
4. 允许缓存的仅是真正immutable canonical bytes/digest/primitive values；若保留此类cache，fresh objects必须从authority inputs或immutable serialization重新构造。不得通过`cache_clear()`、调用顺序或module token保证正确性。
5. Tests必须复现step-145：改变一次factory返回的authority SHA、table、nested projection后，原对象被authority gate拒绝；随后同spec的新factory输出保持canonical digest，且nested graph与前一对象不共享；validator/factory不能共同接受被改变对象。
6. 同时覆盖`_hmm_expectation`内层cache、FIRST/MAX、两套合法plans；不少于24个fresh isolation cases。T098原34+T099原88正常cases回归不得弱化。
7. Fresh final bytes：两exact、schemas全文件、aggregate `test_d0_*.py`；0 fail/error/skip/xfail/warning。static确认无object-returning lru cache；diff/hash/P05/cache/HEAD/staging保护。
8. 日志逐项关闭step-145 P1；raw positive/HMM/ledger保持OPEN。final delta未fresh rerun则INCOMPLETE。

## 固定环境

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
C:\Users\zzt\scoop\apps\python311\current\python.exe -B -m pytest -p no:cacheprovider ...
```

目标8分钟、15分钟硬停止。

## 返回

terminal=`FULL_AUTHORITY_SEAL_CLOSED_POSITIVE_AND_BINDINGS_PENDING`、`INCOMPLETE`或blocker；附RED/GREEN/isolation/static/hash/protection与step-146 SHA。
