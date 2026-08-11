# Task Brief: CP012 D0 implementation-preflight 治理转移 fresh verifier

> 来源: D011 / V005 / H004 / step-101→103 | 产出位置: `projects/thesis-fso/worker-logs/step-104-cp012-governance-transfer-verifier.md`
> 日期: 2026-08-10

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-08-09-coded-decoder-feedback-groundwork/topic-index.md
  control_epoch: 12
  action_class: CONTRACT_STATIC_CHECK
  mission_checkpoint: CP012
```
<!-- RDL-TASK-CONTROL:END -->

## Hypothesis / 否决条件

- 假设：D011/V005/CP012/H004 已把 step-103 的静态资产 PASS 诚实转成交付前工程授权；当前只开放 implementation/unit/post-review non-scientific benchmark，并保留 step-101 FAIL 与 D0 scientific NOT_RUN。
- 否决条件：任一当前 owner 仍授权 `DEFECT_SMOKE`/S1–S4；YAML 五项 authority 不是 `true/true/true/false/false`；D010 科学 gates 被误撤销；step-101 FAIL 被覆盖；step-103 PASS 被升级为 scientific PASS；owner reverse-control reconstruction 不等于已接收 SHA；或 topic/master/registry/S001/mission/A0/asset/H004 不一致，均 FAIL。

## 冻结输入

```text
d0 YAML current=c61c88e596db909211416e3bc0603cfb856aefbcfaf71651799b015039fdde7d
asset report current=ab091da7ce084435176916fc34f888e566a83f7e68a9831e6f6caa61f20e1798
A0 report current=abf14c35730f0f3365ab76a5a041374b5aceb89e65608db56e74da2cfc0e376b
decisions=617b7f316a308e3a3a9cca8a19121aea1bec95f5483850133bdba294e34e2147
verifications=499e87fb420e1c074a2cb72cd4f7d5b65d6de14ca96706130a4e33c23470066a
topic=e1cb28c5a92beed336bac637137f9b9d7f0db71e346c6c656a9d8b3a34b80f05
mission=248f6bb23a4a768c2ec78dc6dc2c96fad6d91d073c0b618bd118799f91019f0f
S001=17d91d7d119d94836bcffcad4871a3d2a780c720a843d8191ab6e5fbd08aa819
H004=f9c58af252a3792752668ce628c3edbb2464eea2215306207d3814c8a779f8d4
registry=94a9ed376ad82355d091abaf01512b9f76dda98b52196aab6ac0c4a35960e62c
master=93ef894511082b0cba782706ab889c9281c5679cc3756ddd7d978eb8d9da7e7b
step-103=6ad845f009a64c0a5d93671bf98354a17a1dd83cf3882aecaa43f5e7f73a5ab9
accepted pre-transfer v3 owner=6924842c5696e80bcf8efa24bc63f005d7a78ba63f959c768e0183de85c81f54
```

## 任务

1. 完整读取 T058、D011、V005、H004、topic、mission、S001、registry 当前专题、master 当前桥接、v3 owner、asset report、A0 report、step-101 与 step-103；不得只读摘要。
2. 用 duplicate-key 拒绝 loader parse owner；核对 schema/status/CP012/epoch12/D011/V005/action，以及 authority matrix=`implementation/unit/engineering-benchmark/execution/science=true/true/true/false/false`。
3. 核对 topic、mission、master、registry、S001、A0、asset、H004 的当前 lane/next action/forbidden 矩阵单义一致：当前可到 TDD implementation、unit、独立代码审查、12 分钟非科学 benchmark；不得写“随后直接执行 S1–S4”。
4. 核对 D010 只在 implementation/execution authority 与 executable-owner claim 上被 D011 取代，其 A0 scientific gates、四 strata 合取、C1 hard-terminal 逻辑继续有效；CP011/H003 保留为历史，不得被误判为当前控制面。
5. 核对 V005 与所有当前摘要同时保留 step-101=`FAIL 0/2/0`、step-103=`PASS 0/0/0`、D0=`NOT_RUN`、METHOD_SIGNAL=`NONE`、预算风险待 benchmark、`>7D blocker NOT_ESTABLISHED`。
6. 独立证明 owner 无隐藏 scientific drift：只在内存中把 CP012 允许变更精确反替换为 pre-transfer 字节（status；epoch/checkpoint/action/decision/verification；implementation/unit；删除 engineering-benchmark flag；pending_reason；末尾 budget status），反构造 SHA 必须等于 `6924842...C81F54`。每个 replacement count 必须恰为 1；不得写回文件。
7. 核对 H004 具备全部 handoff anchors、七个 artifacts、工程四门、未预勾接收清单；registry status/depends/conflicts/produces 无漂移；S001 没有新 voice/profile 信号伪造。
8. 输出 `PASS/FAIL, P0/P1/P2`。只有全 PASS 可写 `CP012_GOVERNANCE_TRANSFER_ACCEPTED_FOR_IMPLEMENTATION_PREFLIGHT`；该 token 仍不授权 scientific S1–S4。
9. 终检 owner/输入初末 SHA、p05 4/4、staging与唯一写入；报告任何非目标变更但不要修。

## 边界

- 只写 `projects/thesis-fso/worker-logs/step-104-cp012-governance-transfer-verifier.md`。
- 只读 parse/hash/grep/确定性算术；禁止 import 项目、pytest、D0/仿真/benchmark、web/search/download、owner/源码/治理修改、commit/push、p05触碰。
- 10 分钟目标，15 分钟硬上限。
