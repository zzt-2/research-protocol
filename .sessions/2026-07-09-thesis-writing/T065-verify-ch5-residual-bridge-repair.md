# Task Brief: 独立复验 Ch5 residual bridge 修复

> 来源: S028 / D047 / T060–T063 | 产出位置: `projects/thesis-fso/apsk-soft-receiver-groundwork/step4a-bridge-repair-verification.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 9
  action_class: INDEPENDENT_SCIENTIFIC_VERIFICATION
  mission_checkpoint: CP009
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

以不同上下文独立接收 T063 的两个窄修复：完整 frozen Ch4 arm 数值快照是否真实进入 deployable bundle/hash/required audit；Ch4 acquisition preamble 与 observation 是否真实共享一条连续 scalar→Jones→AWGN realization。不得修改实现或测试，不得运行 occurrence/performance/调参，不得判断 C5-1 是否有方法信号。

## 启动门与范围

1. 先运行 task-control validator；读取 T060–T063、T061 报告、bridge/contract/README/receipt 与两份 Ch5 tests。
2. 触发并遵守 `sim-preflight`、`stages/gw-feasibility.md` 维度 D 与 `verification-before-completion`。停止扩读无关治理历史。
3. 只允许新增指定验证报告与必要 usage log；代码、测试、contract、receipt、Skill/controller、论文正文均只读。

## 独立必验

1. Fresh 跑两份 Ch5 tests（预期 33 项）、correctness smoke、task validator；确认 `--mode occurrence` 仍以 exit 2 被拒绝。
2. 不照抄 T063 数字，写一次性只读 probe：
   - 同一 receiver realization 下逐项改变 `mu`、`ring_threshold`、`decision_threshold`，`bundle_hash` 必变、`realization_hash` 必不变；snapshot 与实际 runner 入参一致且 null 显式存在。
   - 非零 GG/CFO/Wiener 下，preamble RX、observation RX 与 Ch4 `W` 相对 identity-scalar control 均发生非零变化；连续边界必须可审计。
   - mutation 所有 offline truth、future observation、polarization swap 与 8 个 APSK rotation，分别验证 firewall/equivariance。
3. 独立核查 hash 构成，不只看测试名或 receipt 布尔值；required-field audit 不得把 expected set 自身当 observed set。
4. 检查 diff firewall：T063 只改 brief allowlist，未运行/生成 occurrence 或性能证据。

## 裁决

- `PASS`：两项修复及旧 firewall 全部成立；允许主控按 D047 另派唯一一格 occurrence。
- `PARTIAL`：不影响科学输入的 provenance/可移植性小缺口；明确是否阻断 occurrence。
- `FAIL_REPAIRABLE`：任一 scalar 仍绕过、hash/snapshot 与实际调用不一致、truth/future 泄漏或 required audit 假阳性；occurrence 禁止，只返回最小修复。

最终报告给出 fresh 命令/数字、独立 probe、问题严重度、是否允许 occurrence、唯一下一动作。一次 commit、不 push。
