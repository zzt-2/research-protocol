# Step 173 — D0 I08 canonical JSONL and atomic artifact core

> 2026-08-11 | task T127 | CP012 `D0_UNIT_TEST`

## Terminal

`D0_I08_ATOMIC_ARTIFACT_CORE_GREEN`

这是 I08 作者侧实现/单测终点，不是独立验收、benchmark 或 scientific D0
结果。`DEFECT_SMOKE`/S1–S4 未运行，D0=`NOT_RUN`、method signal=`NONE`。

## Scope

仅创建：

- `projects/simulation/explore/coded-decoder-feedback/artifacts.py`
- `projects/simulation/tests/test_d0_artifacts_cost_s4.py`
- 本 step-173 receipt

没有创建真实 project artifact/result/cache；没有 install、stage、commit、push。

## Real RED

先只创建 AC01 `test_seven_dev_artifacts_named`，在 production module 不存在时运行
指定节点。初次真实结果：`1 failed in 0.20s`，唯一失败为
`ModuleNotFoundError: No module named 'artifacts'`。GREEN 后以临时移开/立即恢复本
任务新模块的方式复现同一 bootstrap seam：`1 failed in 0.18s`，stdout
SHA256=`1f1763c73cf956f25a4fcb578b44592deafa34c5c3bb3509611281a45b5b2987`。

## GREEN evidence

固定环境：`PYTHONDONTWRITEBYTECODE=1`、`PYTHONHASHSEED=0`、Python 3.11
`-B`、pytest `-p no:cacheprovider`。

1. AC01–AC06 整文件：`15 passed in 0.44s`；stdout
   SHA256=`2b36256e32be77cca462b70069b1fa668c17e0972f8c869e7ac2f45cdba9bdfc`。
2. I02/I05 窄回归（D020 frozen owner view、raw strict、PK/FK、S4）：
   `4 passed in 1.42s`；stdout
   SHA256=`0e40b76fec7be90e7275bdaeef11e69bd230687f2d77a31746e7af5e67b88f8f`。
3. 合计 GREEN：`19 passed`，测试报告时间 `1.86s`。未运行 FULL、benchmark、
   science。

## AC01–AC06 closure

- 七个 dev logical names 以唯一 tuple 精确有序固定；bundle receipt 总在第七个、
  最后落地。
- JSON/JSONL 只接受 UTF-8、sorted keys、compact separators、
  `ensure_ascii=False`、`allow_nan=False`；每条 JSONL 以 exact LF 终止。
  MappingProxy 显式复制成 plain JSON tree；D020 hard-output 按 lowercase root、
  provenance 按 nested logical computation id 排序。
- 行/表 validator、PK/sort uniqueness、FK、cardinality、finite、manifest callback、
  全量 materialize/encode/hash 均在首次 mkdir/mkstemp/open 前完成。
- 单文件事件序列由测试精确断言：
  `temp_created -> written -> flushed -> file_fsynced -> closed -> replaced ->`
  `directory_fsync_attempted -> directory_fsync_recorded`。当前 Windows 实测
  directory fsync=`UNSUPPORTED`，receipt 明确记录，未伪称成功。
- bundle 使用 immutable `.generations/generation-*` 加原子 `CURRENT.json` 指针；
  六个 data 逐 byte 落地复核，receipt 第七且最后，完成 generation 自校验后才
  原子替换 pointer。`bundle_before_pointer` 注入失败时旧 pointer exact bytes 不变，
  新 generation 清理，旧完整 bundle 仍由 `validate_complete_bundle` 读取。
- receipt 的 artifact SHA/byte_count/record_count 由 materialized bytes 生成并对实际
  landed bytes 重读复核；caller 不能提交 artifact SHA。receipt 以 logical-name
  pairs 绑定 owner/contract/source/code/manifest/raw/chunk/freeze/selection/seed/
  summary/ledger。缺/多/改单 byte、wrong/duplicate name、fake hash、缺 receipt 均
  fail closed。

## Fresh negatives and atomic fault trace

执行 fresh negative/failure operations=`20`：非有限 float 3、非字符串 key 1、
bytes/Path/opaque 3、cycle 1、duplicate/empty/missing/null/container sort key 5、
validation-before-write 1、单文件 pre-replace fault 4、bundle pre-pointer fault 1、
landed-byte tamper 1。wrong accept/reject=`0/0`；临时文件残留=`0`；旧 target/
pointer preservation mismatch=`0`。

## Hash / protection receipt

- `artifacts.py` SHA256=
  `c4ab7c342e4c05f44e343daeffca9c60090fde252a41ae7e067cb2cca7f86dce`
- `test_d0_artifacts_cost_s4.py` SHA256=
  `534f45fe9bd0b5eb42888d33081555c63a9a224ba0b9a98d2ad2923ceefc2315`
- HEAD=`715a65884b988ee737f21982f3bbf372860a1da8`；staging empty；
  `git diff --check` 无 whitespace error（仅既有 CRLF warning）。
- protected p05 SHA256 保持：
  `7843b048a2a79755c95542a438a5344f8e89e791113f48913926c419fc2a4f11`、
  `735e4650093d297e01a0e6dfe28f0431c149a2931fcbb7c08eecfa28f0aac38b`、
  `c76887c6950aaac2b4c0dced7689517749322c44da868880915786c173b1344d`、
  `95a1d184740a797b6d55d7f817008c898cb3754987ab6e1c1d00376f74a621de`。

## Findings

作者侧 P0/P1/P2=`0/0/0`。按 T127，下一步仅与 I07 一起接受一次 fresh batch
verifier；不单开 readiness review。
