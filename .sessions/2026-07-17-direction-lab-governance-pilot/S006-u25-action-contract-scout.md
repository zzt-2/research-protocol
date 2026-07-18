# [S006] U25 causal action contract Scout

> 2026-07-18 | Scout/接口实现 | PARTIAL（B004 禁止启动）

## 目标

在不启动 B004、不创建 PASS Queue 的前提下，为排名最高的 P01 U25 建立最小可验证的因果动作接口、固定安全策略比较器、无动作恒等性和确定性回放基础。

## 记录

新增 `projects/thesis-fso/direction-lab/tools/u25_action_contract.py`，只提供 contract-level pure functions，不执行 receiver、训练或性能实验：

- 事件必需字段：`sequence_id`、`step`、`available_at_step`、`trigger`、`observables`；
- 因果门：`available_at_step <= step`，拒绝 oracle/post-hoc/future 字段；
- 动作集合：`NO_OP`、`SAFE_BASELINE`、`RESET`；
- 固定策略：`NONE→NO_OP`，失锁/周期滑移/发散/性能退化→`SAFE_BASELINE`；
- `NO_OP` 不修改输入状态；所有动作不修改原对象；
- replay 要求单一 sequence、从 step 0 开始连续递增，policy 只收到当前事件；
- fingerprint 基于显式 contract JSON，当前值为 `4359429931d5d2da849045e658968cac677f78cb2dabe2d8d429d1034363b3f7`。

新增 `u25-action-contract.v1.yaml`，明确列出运行时六字段，但不提供任何默认值；保留未来 Sandbox 指标字段，但当前不计算。

TDD 验证：先运行缺失模块的测试并按预期失败，随后实现最小接口；当前 P01 contract tests 为 6 passed。该结果只说明接口层成立，不等于 U25 可运行或有效。

### 当前门控

- Scout contract：PASS
- Sandbox runner：NOT_READY
- 事件生成器/共享 fork-replay 数据：缺失
- Queue/Registry/Runner fingerprint：未创建
- B004：禁止启动

## 决策引用

- D007：三层机制族批量流程
- D008：completion event 事实源与 reducer 投影视图
- D009：P01 先冻结 U25 因果动作接口，再补运行绑定（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

下一步只允许补齐因果事件生成器和共享 fork-replay 数据的 Scout smoke，随后再审 runner/registry binding；在这些依赖关闭前，不创建 PASS Queue，不运行 B004，不产生性能数字。
