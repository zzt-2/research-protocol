# Task Brief: 无 event-label clean-control reconstruction detector

> 来源: S004 / D005 | 产出位置: `projects/thesis-fso/direction-lab/`
> 日期: 2026-07-17
> 唯一文档: 执行方可读本文件及指定的旧 detector 文件

## 0. TL;DR（执行方先读）

B001 v1 的 `C24-SSL-AE` 用 train fixed-label `y==0` 筛 clean rows，违反“不需要 event labels”的预注册机制。

**你的任务**：严格 TDD 新建一个真正不接收 event labels 的 clean-control reconstruction detector 与无标签 control threshold calibration；不得修改 v1 detector/runner/result。

**产出**：新模块与测试，供后续 v2 runner 调用。

**最高纪律**：

1. 先写 RED：证明新 detector 的 fit API 不接受/不需要 y，且无标签阈值只由 scores+cell_ids 决定。
2. 不修改 `ml_detector_batch.py`、`run_b001.py` 或 B001 任何产物，保持旧 source closure。
3. representation fit 只使用 control-rate train feature matrix；不能读取 block labels、fixed/PI BER、true h/Jones/symbols。
4. 阈值校准只使用 control-rate train scores 与 cell IDs；不能接收 event labels。
5. 允许复用旧模块的 `_Scaler`/基类或以 synthetic all-clean 内部标签调用旧 reconstruction primitive，但新公开 API 和调用链不能读取真实 y；代码/测试须清楚证明这一点。
6. 不提交 git；不触碰其他用户修改。

## 1. 背景

旧实现：`tools/ml_detector_batch.py:201-239` 的 `CleanReconstructionDetector.fit(x,y,cell_ids)` 用 `clean=y==0`。v2 机制定义是：整个 control-rate train split 被视为无标签参考域，representation 与 threshold 均不看 event labels。是否能区分事件由新 batch 判断，不能预设成功。

## 2. 任务详情

### 2.1 文件范围

- 读：`projects/thesis-fso/direction-lab/tools/ml_detector_batch.py`
- 新建：`projects/thesis-fso/direction-lab/tools/unlabeled_control_reconstruction.py`
- 新建：`projects/thesis-fso/direction-lab/tests/test_unlabeled_control_reconstruction.py`

### 2.2 要求

- 类名清晰表示 `UnlabeledControlReconstructionDetector`。
- `fit(x, cell_ids)`；输入不足/非 finite/shape 错误行为与旧 detector 风格一致。
- `predict_proba(x)` 返回有限 `[0,1]` anomaly scores。
- `calibrate_unlabeled_cell_threshold(scores, cell_ids, false_alarm_budget)` 以 cell-level maxima 为参考，确定性产生 threshold；相同 scores/cells 不因任何外部 label 改变。
- 测试至少覆盖 API 无 y、fit/predict finite、阈值预算边界、输入验证和确定性。

### 2.3 产出格式

```text
STATUS: DONE | BLOCKED
ROOT_CAUSE: ...
RED: command + expected failure
GREEN: command + pass count
FILES: ...
CONCERNS: ...
```

## 3. 已知陷阱

- “先用 labels 找 clean，再声称训练无监督”仍然违规。
- threshold calibration 若用 labels 区分 event/control 也不算无标签。
- 不要把 control-rate 没有事件当事实；B001 train control rate 实际有正 block，所以 v2 明确学的是整体参考域而非 oracle-clean manifold。
- 不要修改旧文件，否则 B001 source SHA 会 stale。

## 4. 验收

- [ ] RED/GREEN 可复现。
- [ ] 新公开 API 没有 y/event-label 参数。
- [ ] representation 与 threshold 都不读取 label。
- [ ] 新测试全部通过，旧 14 tests 仍通过。
