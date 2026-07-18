# [S007] P01/U25 Sandbox-ready 判断

> 2026-07-18 | Scout → Sandbox-ready preflight | BLOCKED（B004 禁止启动）

## 目标

连续完成 P01/U25 的 causal adapter、fork-replay smoke 和 Sandbox-ready preflight；若任一真实前置条件不能闭合，给出具体阻断、复现命令、可复用资产和下一候选。

## 记录

### Causal adapter

`u25_action_contract.adapt_standard_cma_trace()` 已绑定 B003 隔离 artifact 的真实 `cells[0].trace`，而不是手写 synthetic dict。输入严格白名单为 `output_start/output_end/cm_error/output_power/update_norm`，每个输出 event 字段和四个 observable 都有 source pointer、dtype/unit、trace index；`step` 同时记录对齐的 `output_start/output_end` 样本索引。`sX/sY/h/theta/bitsX/bitsY/fixed_label_ber/pi_ber`、未来窗口和所有未注册字段均被拒绝。

`lock_score=1/(1+cm_error)` 被明确标成 receiver-only proxy，未被称为已验证的物理 lock state。

### Fork-replay

未达到执行条件。真实 standard-CMA runner 签名为
`(realization, cfg, variant='baseline', return_blind_trace=True)`，没有 action hook；blind trace/输出没有 receiver state snapshot；`apply_action()` 只修改 metadata dict，不影响 CMA weights、`zX/zY` 或后续 receiver path。因此 no-op bit-exact、固定安全策略、单动作、3 event-like/3 clean fork、action latency/recovery delay/worst-cell degradation 均不能合法计算。

### Runner/registry/source closure

未达到执行条件。`run_v3.py` 仍固定 U24 component/ML detector，现有 validator/registry 也固定 U24；没有 U25 component IDs、runner dispatch、source closure 或新 queue/registry 快照。没有写 evidence ledger、completion event 或 canonical state。

### P02 检查

P02/U10 的 FOE、DPLL、VV、BPS 和 phase-noise 代码可复用，但当前双偏振 standard-CMA generator 没有 carrier phase/noise/CFO/CPR 状态，也没有 lock-loss/cycle-slip event library、persistence 或 warning lead validator。因此 P02 只达到 `P02_SCOUT_CONTRACT_ASSETS_PARTIAL`，不是 event-library-ready。

## 决策引用

- D009：P01 先冻结 U25 因果动作接口
- D010：P01 在当前 standard-CMA 链上阻断并转查 P02（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

下一候选为 P02/U10 的 carrier-impairment、双偏振 CPR 与 receiver-only event contract 轻门控；若 P02 仍缺真实事件链，则转 P03/U19 residual-headroom Scout。任何候选在输入合同、指标、fingerprint、runner 和 source closure 未齐备前，不创建 PASS Queue，不启动 B004。
