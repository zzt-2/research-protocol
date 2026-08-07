# [S019] Ch4 方法槽位纠偏与 decoder-feedback 预检

> 2026-08-07 | 流程纠偏 / 方法构造准备 | 已完成

## 目标

纠正 `SUPPORTING_ONLY` 被误算作长程方法进展的问题，并准备一个不跑实验、只判断方法形是否成立的
decoder-feedback CCISP 构造预检。

## 记录

- CP021 同时记录 `mission_method_delta=NONE`、`thesis_method_disposition=SUPPORTING_ONLY` 与
  `weight=ADEQUATE / drift=ALIGNED`。后两项对审计质量可以成立，对“填补 Ch4 方法槽位”的 mission
  却不成立。
- 对应失败模式为 M6 范围偏离，而不是 2A 科学裁决错误：P01/P02/T004 的 `SUPPORTING_ONLY`
  保持有效，但不能关闭方法槽位，也不应再获得下一轮包装机会。
- 对 `method-production.md` 只增加一个窄规则：开放方法槽位仅由 `THESIS_METHOD_READY` 或 authority
  显式映射的 task-local equivalent（如 `THESIS_ENGINEERING_METHOD_READY`）关闭；
  supporting/reject 进入 harvest 后必须轮换到 method-shaped construct。
- 当前 Ch3 CCISP 主方法和 Ch5 select-before-execute 工程方法已有 authority，Ch4 仍缺方法。
- T010 只读本地 coded/decoder/CPR 资产，构造并碰撞最多三条 decoder-feedback 动作链；不检索、
  不进入 GW、不实现、不仿真。最多保留一个 survivor，且 survivor 只能回 GW Step 1。

## 决策引用

- D039：方法章节槽位只由方法终态关闭，并转入 decoder-feedback 正向构造预检（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是（只修 mission 解释、Skill 最小规则与下一任务合同）

## 后续

新对话执行 T010。若无方法形 survivor，直接报告该候选源战略短缺，不再围绕 coded supporting
资产做 authority reconciliation 或包装闭环。
