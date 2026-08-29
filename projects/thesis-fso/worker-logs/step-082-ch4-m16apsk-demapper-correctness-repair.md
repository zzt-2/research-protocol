# Step 082: Ch4 16APSK demapper correctness repair

> 2026-08-30 | T082 / D061 / V036 / CP023 | 实现者记录

## 事实

1. 起飞时 task-control validator 返回 `PASS`；唯一开放动作是公共 16APSK hard demapper 的 TDD correctness repair。
2. 修改前冻结反例 `0.9155 exp(j*pi/8)` 的 brute-force 最近标签为 `0000`，历史实现输出 `1000`；平方距离分别为 inner `0.162148054030597`、outer `0.345664332496586`。
3. RED focused test 为 `2 failed, 1 passed`；除冻结反例外，固定 deterministic cloud 有 `17/2048` 个 bit 与独立 16 点 oracle 不同。
4. 实现 diff 只删除半径强制判环并改正 docstring；没有改变 constellation、mapping、normalization、modulator 或 tie rule。
5. GREEN focused test 为 `3 passed in 1.27s`；T082 指定的 focused/direct-neighbor 合集为 `113 passed in 25.80s`。
6. 四个历史 confirmation artifact 的精确路径 `git diff --exit-code` 为 0；没有运行 BER replay、smoke 或 production。

## RED 命令

工作目录：`projects/simulation/explore/ch4-scaled-unitary-pilot-ls`

```text
python -m pytest tests/test_m16apsk_ml_demod.py -q
```

结果：exit 1，`2 failed, 1 passed in 6.92s`。失败是期望的合同反例，不是测试错误。

## 实现

- `projects/simulation/common/_modulation.py`
  - 删除 `thr` 与 `is_outer`；
  - `pick_outer` 仅由 `d_outer_min < d_inner_min` 决定；
  - docstring 明确全 16 点全局欧氏最近邻。
- `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_m16apsk_ml_demod.py`
  - 16 labels normalized constellation round-trip；
  - 冻结 inner-ray 反例；
  - fixed-seed 512-point off-boundary cloud 对独立 16-point oracle。

## 验证命令与结果

| 验证 | 结果 |
|---|---|
| `python -m pytest tests/test_m16apsk_ml_demod.py -q` | initial GREEN `3 passed in 1.27s`；收尾 fresh rerun `3 passed in 1.32s` |
| T082 指定 8 个 focused/neighbor test files 合并运行 | `113 passed in 25.80s` |
| `rg -l "m16apsk_demod" projects/simulation -g "test_*.py"` | 仅新建的直接合同测试；T082 点名的间接调用方回归另行全跑 |
| 四个 `confirmation_*` artifact 的 `git diff --exit-code` | `HISTORICAL_CONFIRMATION_UNCHANGED` |
| `python -m py_compile ...` | 收尾 fresh check 记录为 PASS |
| T082 task-control validator | 起飞 PASS；收尾 fresh check 记录为 PASS |
| 精确白名单审计 | 收尾 fresh check 记录为 PASS |
| `git diff --check` | 收尾 fresh check 记录为 PASS |

## 精确文件清单

本任务只允许并只产生以下四个路径的变更：

1. `projects/simulation/common/_modulation.py`
2. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/tests/test_m16apsk_ml_demod.py`
3. `projects/simulation/explore/ch4-scaled-unitary-pilot-ls/demapper-correction-note.md`
4. `projects/thesis-fso/worker-logs/step-082-ch4-m16apsk-demapper-correctness-repair.md`

共享 worktree 中其他 pre-existing modified/untracked files 未触碰、未清理、未纳入本任务。

## 约定变更

公共 `m16apsk_demod` 从历史半径强制判环修正为其既有 docstring/星座合同要求的全 16 点欧氏最近邻。历史 raw 不改写；未来新 evidence 使用 corrected contract 并单独标 artifact identity。

## 终态

`DEMAPPER_CORRECTNESS_REPAIR_PASS`

该终态只表示实现者侧 correctness tests 与指定回归通过，仍须由未参与实现的 reviewer 用新 complex points 独立复核；不表示 C4 BER 信号仍在，不授权 A1/CP024。
