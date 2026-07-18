# Task Brief: CandidateMap v2 确定性评分门

> 来源: S004 | 产出位置: `projects/thesis-fso/direction-lab/`
> 日期: 2026-07-17
> 唯一文档: 执行方可读本文件及其中列出的源码/数据文件

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol`。B001 v1 的 runtime 完整性有效，但 `candidate-map.yaml` 的手写 score 与声明 weights 不一致。

**你的任务**：按 TDD 建立确定性 CandidateMap 评分校验，并生成不可变的 corrected `candidate-map.v2.yaml`；不得修改 v1 map/queue/result。

**产出**：评分工具、测试、corrected v2 map；返回根因、RED/GREEN 命令与结果。

**最高纪律**：

1. 先写会让 v1 map 因 score/order 错误而失败的测试并实际观察 RED，再写实现。
2. 不修改 `candidate-map.yaml`、`batch-queue.yaml`、B001 manifest/result/evidence。
3. 评分必须严格使用 map 中声明的 weights；显示值统一保留两位小数，比较容差必须显式。
4. v2 map 必须保留 32/32 archetype 覆盖、历史边界、U24 第一名和 sandbox/no-promotion 约束；实际排序按重算结果生成，不能手调。
5. v2 的 `map_gate.independent_review` 暂写 `PENDING`、`verdict: PENDING`，由主控另派 verifier 后更新。
6. 不提交 git；不要触碰工作树中其他用户修改。

## 1. 背景

V008 复算示例：U24 recorded 4.15 / recomputed 4.20；U18 recorded 3.00 / recomputed 3.25；U08 recorded 3.10 / recomputed 3.05。U24 仍为第一，因此 v2 可保留 B001 问题族，但旧 gate 不能追溯性修成 PASS。

## 2. 任务详情

### 2.1 文件范围

- 读：`projects/thesis-fso/direction-lab/candidate-map.yaml`
- 新建：`projects/thesis-fso/direction-lab/tools/validate_candidate_map.py`
- 新建：`projects/thesis-fso/direction-lab/tests/test_candidate_map_gate.py`
- 新建：`projects/thesis-fso/direction-lab/candidate-map.v2.yaml`

### 2.2 行为要求

- 工具提供可测试函数：读取 map、按 factors×weights 计算 score、验证 recorded score、验证 shortlist 降序和 ID 唯一性。
- v1 的校验必须报告至少 score mismatch 和 ordering mismatch。
- v2 必须全部通过；排名相同时用稳定 tie-break（原 shortlist 顺序或 candidate ID，需文档化）。
- v2 带 lineage：`supersedes_map_id`、v1 文件 SHA、修正原因；不得声称独立审查已经完成。

### 2.3 产出格式

返回：

```text
STATUS: DONE | BLOCKED
ROOT_CAUSE: ...
RED: command + expected failure
GREEN: command + pass count
FILES: ...
CONCERNS: ...
```

## 3. 已知陷阱

- 不要只把 U24 改成 4.20；必须覆盖所有 shortlist。
- 不要用 rounded score 再排序导致边界颠倒；先用 full precision 排序，显示再 round。
- 不要把 `independent_review: PASS` 从 v1 复制到 v2。
- 不要更改 v1，以免破坏 B001 manifest 的 17-file source closure。

## 4. 验收

- [ ] v1 校验确定性 FAIL，且错误消息指向实际 mismatch。
- [ ] v2 校验 PASS。
- [ ] U24 为第一，32/32 universe coverage 保持。
- [ ] v2 gate 尚未自封 PASS。
- [ ] 相关测试全绿，无其他文件改动。
