# Step 089：Ch4 唯一 canonical formal raw production

> 2026-08-30 | T089 / D068 / V043 / CP030 | 唯一 raw 已生成，等待独立 raw-only 复核

## 权限与前置门

- 已重新读取 sim-preflight 及运行场景、T089、D068/V043、scientific manifest、replacement execution lock，以及 T087/T088 worker log 和两份独立终态报告。
- 主控确认 independent pre-run GO P0/P1=`0/0`。
- fresh task-control=`PASS`：epoch 30 / CP030 / `CH4_CANONICAL_FORMAL_RAW_PRODUCTION`。
- fresh focused tests=`19/19 PASS`，五文件隔离 `py_compile`=PASS。
- scientific manifest SHA-256=`417f334844f9092b02bab5d6478381ae7a57e2ff9b4a385ba37707f601521079`。
- replacement execution lock SHA-256=`095dc989ffee8618484778cb8c0c4454b65b503e22f7db18fbea5cf083227987`。
- runner/reducer/entry/tests、四项 frozen dependency、HEAD 与 Python/NumPy/platform 均与 lock actual match。
- 起跑前 canonical raw/checkpoint/aggregate/receipt 全部不存在。

## 唯一运行

开始时间：`2026-08-30T16:44:28.6357739+08:00`。

只运行一次原样命令：

`python projects/simulation/explore/ch4-scaled-unitary-pilot-ls/run_ch4_formal_production.py --formal`

执行结果：

- exit=`0`；
- wall time=`409.5 s`；
- stdout 最终完成 `latent 30127: 128/128`；
- stdout terminal=`CH4_FORMAL_PRODUCTION_COMPLETE`；
- 运行中只读观察 checkpoint records 进度，未根据中间内容停止、调参或干预；
- 没有第二次 formal 调用，没有 smoke 调用，没有 reducer 调用。

## 成功后允许范围内的只读核验

| 项目 | 结果 |
|---|---|
| raw 路径 | `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/ch4_formal_raw.json` |
| raw SHA-256 | `642c7ae9eb260526ae77c1c2c7c903590cb5cf19813c5f9b8b4d529b98a72c5b` |
| raw 文件大小 | `89,419,500` bytes |
| schema | `t087.ch4-formal-raw.v1` |
| purpose | `canonical_formal_production` |
| latent ID 集合 | exact `30000..30127`，共128个且无重复 |
| census | top-level=`128` / scene=`384` / actual cells=`15232` / arm rows=`76160` / delta0 references=`128` |
| 每 latent scene | exact `weak/moderate/strong` |
| 每 actual cell rows | exact `5` |
| scientific-manifest header | exact `417f3348...1079` |
| execution-lock header | exact `095dc989...7987` |
| execution hashes / base commit | 与 replacement lock exact |
| truth firewall header | `O1_SEPARATE_TRUTH_ONLY_PATH` |
| checkpoint / raw `.tmp` | 均不存在 |
| aggregate / receipt | 均不存在 |

上述核验没有读取或汇总 BER，没有计算 crossing/bootstrap/grade，没有选择 cell/曲线，也没有导入或运行 reducer。

## 约定变更

无。未修改任何代码、tests、manifest、lock、参数、公式、网格、方法或评估规则。

## 当前停点

实现者侧状态为 `READY_FOR_INDEPENDENT_RAW_ONLY_REVIEW`。本日志不宣告 `CH4_CANONICAL_FORMAL_RAW_READY`，不授权 canonical reduction、grade、作图、正文或任何重跑；只有 T089 独立 raw-only 复核 P0/P1=`0/0` 后，主控才可决定下一 checkpoint。
