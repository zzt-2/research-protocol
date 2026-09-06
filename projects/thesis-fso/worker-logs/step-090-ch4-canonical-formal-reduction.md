# Step 090：Ch4 canonical formal reduction 单次失败记录

> 2026-08-30 | T090 / D069 / V044 / CP031 | `FAILED_PRE_WRITE_IMPORT_PATH`，已熔断

## 权限与执行前门

- 已重新读取 sim-preflight 及运行场景、T090、D069/V044、step-089 worker log 与 canonical raw 独立验收报告。
- canonical raw 独立终态=`CH4_CANONICAL_FORMAL_RAW_READY`，pre-run GO P0/P1=`0/0`。
- fresh task-control=`PASS`：epoch 31 / CP031 / `CH4_CANONICAL_FORMAL_REDUCTION`。
- fresh focused tests=`19/19 PASS`，五文件隔离 `py_compile`=PASS。
- raw SHA-256=`642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b`，size=`89,419,500` bytes。
- manifest SHA-256=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`；lock SHA-256=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`。
- 全部 execution/dependency hashes、HEAD 与 environment actual match；reducer raw-only static gate PASS。
- aggregate、receipt及两者 `.tmp` 在执行前全部不存在。

## 唯一 canonical reduction 尝试

开始时间：`2026-08-30T17:05:59.2433020+08:00`。

仅运行一次原样命令：

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/reduce_ch4_formal_production.py`

结果：

- exit=`1`；
- wall time=`4.1 s`；
- 未产生成功 stdout terminal；
- 失败位置：`reduce_ch4_formal_production.py::_save_temp()`；
- 直接错误：`from projects.simulation.common import save_results` 抛出 `ModuleNotFoundError: No module named 'projects'`。

该失败发生在 aggregate 写入前。按 T090 规则，命令没有重试，也没有修改 entry、reducer、调用参数或环境，没有删除任何 artifact 或 `.tmp`。

## 失败后只读状态

| 项目 | 状态 |
|---|---|
| `ch4_formal_aggregate.json` | 不存在 |
| `ch4_formal_receipt.json` | 不存在 |
| `ch4_formal_aggregate.json.tmp` | 不存在 |
| `ch4_formal_receipt.json.tmp` | 不存在 |
| raw SHA/size | 仍为 `642c7ae9...a72c5b` / `89,419,500` bytes |
| execution lock SHA | 仍为 `095dc989...7987` |
| scientific manifest SHA | 仍为 `417f3348...1079` |
| canonical grade | 未产生 / 未知 |

未另算任何统计，未读取或解释 grade，未运行 formal/smoke，未生成 aggregate/receipt。

## 约定变更

无。未修改代码、tests、raw、manifest、lock、参数、公式、统计规则或 grade。

## 当前停点

T090 未达到 `CH4_CANONICAL_FORMAL_STATISTICS_READY`。当前唯一状态为 `FAILED_PRE_WRITE_IMPORT_PATH`；必须返回 D069 讨论并获得新的显式修复/执行授权。不得自动重跑 reducer、删除文件、运行独立统计、作图或解释性能。
