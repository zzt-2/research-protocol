# Step 091：Ch4 canonical reduction corrected publication

> 2026-08-30 | T091 / D070 / V045 / CP032 | canonical artifacts 已发布，等待独立 raw-only 统计复算

## 权限与执行前门

- 已重新读取 sim-preflight 及运行场景、T091、D070/V045、T090 log、canonical raw 独立报告与双锁。
- fresh task-control=`PASS`：epoch 32 / CP032 / `CH4_CANONICAL_REDUCTION_PUBLICATION_REPAIR`。
- fresh focused tests=`19/19 PASS`，五文件隔离 `py_compile`=PASS。
- raw/manifest/lock及八项 execution/dependency authority 共11项 bytes exact；HEAD/environment 与 lock exact。
- aggregate、receipt及两者 `.tmp` 在执行前全部不存在。
- 无写入显式 PYTHONPATH probe 可导入 common、pure reducer 与 entry，probe 后仍无 artifact。

## 唯一 corrected invocation

开始时间：`2026-08-30T17:14:09.4223569+08:00`。

在一个新的 PowerShell 进程中严格执行 T091 三行：

```powershell
$repo=(Resolve-Path '.').Path
$env:PYTHONPATH="$repo;$(Join-Path $repo 'projects\simulation');$(Join-Path $repo 'projects\simulation\explore\ch4-scaled-unitary-pilot-ls')"
python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_ch4_formal_production.py
```

没有设置其他环境变量，没有增加 CLI 参数。执行结果：

- exit=`0`；
- wall time=`5.0 s`；
- stdout terminal=`CH4_FORMAL_REDUCTION_ACCEPTED`；
- stdout grade=`A`；
- corrected invocation只运行一次，没有第三次尝试，没有运行formal或smoke。

## Canonical publication artifacts

| Artifact | SHA-256 | Size | Terminal | Grade |
|---|---|---:|---|---|
| `ch4_formal_aggregate.json` | `916c4ba5f75703a5a63bc40931e74d161ad3e61ac0b72baa918b77de95c55602` | `22,404` bytes | `CH4_FORMAL_REDUCTION_COMPLETE` | `A` |
| `ch4_formal_receipt.json` | `0fac1304f9aa8a4a4463c14ed5a43059a04b5c1de031b69c1d7fa9f03376e697` | `1,364` bytes | `CH4_FORMAL_REDUCTION_ACCEPTED` | `A` |

Receipt artifact bindings 现场复核：

- formal raw=`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`；
- scientific manifest=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；
- execution lock=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`；
- formal aggregate=`916c4ba5f75703a5a63bc40931e74d161ad3e61ac0b72baa918b77de95c55602`；
- base commit=`d3d98c6fc92642e4d6b964d086c1f3bea2018d1d`；
- aggregate/receipt `.tmp` 均不存在。

实现者只读取了 artifact 顶层 terminal/grade 与 provenance hashes，没有另算 pooled BER、crossing、bootstrap、CI、summary 或 grade，也没有使用 T090 内存计算作证据。

## 约定变更

无。未修改 entry、freezer、runner、reducer、tests、raw、manifest、lock、参数、统计口径或 grade。

## 当前停点

实现者侧状态为 `READY_FOR_INDEPENDENT_RAW_ONLY_STATISTICS_REVIEW`。grade `A` 仅是 canonical reducer 已发布字段，尚未由独立 raw-only 复算接收。本日志不宣告 `CH4_CANONICAL_FORMAL_STATISTICS_READY`，不授权作图、正文、补实验或任何再次 publication。
