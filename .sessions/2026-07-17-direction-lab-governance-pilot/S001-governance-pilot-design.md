# [S001] Direction Lab 可遵守性试运行设计

> 2026-07-17 | 设计 | IN PROGRESS

## 目标

验证复杂研究治理能否被 AI 持续执行，识别哪些规则必须脚本化、哪些规则适合状态机阻断、哪些规则必须保留给 AI 和人做判断。

## 记录

### 1. 三层控制模型

| 层 | 适合控制的内容 | 失败时动作 |
|---|---|---|
| 脚本硬门 | 文件存在性、schema、ID、SHA、manifest、目录边界、状态枚举 | 直接拒绝写入或拒绝运行 |
| 状态机门 | 阶段顺序、`BOARD_READY` 前禁排名、PARTIAL 禁止晋级、Kill 后 reopen 条件 | 阻断下一动作并生成违规记录 |
| AI/人工判断 | 机制是否真实、候选是否值得保留、证据是否足够支撑声称 | 记录理由，允许复核，不自动伪装成硬事实 |

### 2. 观察矩阵

至少覆盖以下故意设置的压力场景：

1. 缺 manifest 直接运行；
2. 把 legacy/no-z baseline 冒充 canonical；
3. `BOARD_READY` 前提前 Kill 一个候选；
4. 用摘要级证据写完整论文结论；
5. 修改组件后继续引用旧结果；
6. Kill 后没有登记可复用资产；
7. 中断后恢复时只读 summary、不读 canonical state；
8. 同一结果名对应两个不同配置。

### 3. 观察指标

- 违规率：每轮触发的违规数 / 应触发的门数；
- 漏拦率：脚本或状态机应该拦截但未拦截的违规；
- 误拦率：合法动作被错误阻断的比例；
- 恢复成功率：新上下文能否仅凭 canonical state + manifest 恢复；
- 人工补救次数；
- 规则负担：单轮需主动读取和维护的文件数、字段数、判断数；
- 违规修复后的重复发生率。

### 4. 暂定退出条件

- 连续 3 轮关键 P0 违规为 0，且恢复成功率 ≥90%；
- 或连续 2 轮仍有同一类漏拦，说明 schema/控制器设计不合格，需要回到设计阶段；
- 误拦率 >20% 或规则维护成本明显超过收益时，优先删规则、合并状态，而不是继续加护栏。

### 5. 产出边界

pilot 只产生治理验证记录：违规日志、控制器缺口、规则删改建议和最终的实现清单。任何仿真性能数字都不得进入论文材料或正式方向结论。

## 决策引用

- 无决策

## 范围确认

- 本轮是否在 scope boundary 内：是

## 后续

- 选定一个小型、已有 manifest 的 batch 作为 sandbox 输入；
- 建立最小脚本硬门，不先实现全部五个 schema；
- 安排独立 verifier 复核 pilot 是否真的测到了违规，而不是只检查文档是否齐全。

> 2026-07-17 续接：已选 B5 作为只读历史输入，控制器 fixture 放在
> `projects/simulation/verify/direction_lab_pilot/`，不改 B5 原文件、canonical
> baseline 或正式论文材料。首版仅覆盖 manifest/run_id、ID/fingerprint、
> BOARD_READY、PARTIAL 晋级和 STALE 传播五个硬门。

## 实施记录（首轮）

- RED：新增 `projects/simulation/tests/test_direction_lab_controller.py`，6 个行为测试先于控制器实现运行；缺模块导致预期失败。
- GREEN：新增 `verify/direction_lab_pilot/controller.py` 与只读 `b5_pilot_manifest.json`；6/6 测试通过。
- 审计：控制器逐动作追加 JSONL 事件，拒绝时保留 `original_action`、`reason`、`blocked`；组件指纹漂移只显式标记 `STALE`，不静默修复输入。
- 独立复核：由独立 verifier 检查测试是否触发行为拦截及漏测/误拦风险，结论写入 V001。
