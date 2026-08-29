---
owner_of: Ch4 corrected 16APSK hard-demapper contract and historical compatibility boundary
authority: T082 / D061 / V036 / CP023
date: 2026-08-30
---

# 16APSK hard demapper correctness repair

## 事实

公共 `m16apsk_demod` 的公开合同是归一化 `(8,8)-16APSK` 全部 16 点的欧氏最近邻 hard decision。历史实现虽然分别计算了内外环最小距离，却又以

`pick_outer = (d_outer_min < d_inner_min) | is_outer`

把半径超过 `(r1+r2)/2` 的样本强制判为外环。这与全局最近邻合同冲突。

冻结反例为 `z=0.9155 exp(j*pi/8)`：

| 量 | 值 |
|---|---:|
| `r1` | 0.512823884454768 |
| `r2` | 1.317957383048755 |
| 历史半径阈值 `(r1+r2)/2` | 0.915390633751762 |
| `abs(z)` | 0.915500000000000 |
| 最近内环点平方距离 | 0.162148054030597 |
| 最近外环点平方距离 | 0.345664332496586 |

因此历史半径条件把全局最近的 inner label `0000` 错判成 outer label `1000`。

## RED -> GREEN 证据

从 `projects/simulation/explore/ch4-scaled-unitary-pilot-ls` 运行：

```text
python -m pytest tests/test_m16apsk_ml_demod.py -q
```

修改实现前为 `2 failed, 1 passed`：冻结反例实际 `1000`、期望 `0000`；固定 512 点、远离平距边界的 deterministic cloud 有 `17/2048` 个 bit 不一致。失败来自历史半径强制项，不是 import、shape 或测试语法错误。

最小修复只做两件事：

1. 删除已无合法用途的 `thr/is_outer`；
2. 将环选择改为 `pick_outer = d_outer_min < d_inner_min`，并把 docstring 改成全 16 点全局最近邻。

修复后同一 focused 命令为 `3 passed in 1.27s`。调制器、`gamma=2.57`、两个半径、Gray labels、功率归一化和严格小于的 tie rule 均未改变。

## 回归范围

repo-root fresh test census：

```text
rg -l "m16apsk_demod" projects/simulation -g "test_*.py"
projects/simulation\explore\ch4-scaled-unitary-pilot-ls\tests\test_m16apsk_ml_demod.py
```

除 census 命中的直接合同测试外，按 T082 明确运行 Ch4 local tests、公共 common tests、APSK ring-gated 两组测试和 APSK LLR correctness tests；合并结果为 `113 passed in 25.80s`。

## 历史兼容边界

- `confirmation_manifest.json`、`confirmation_raw.json`、`confirmation_aggregate.json`、`confirmation_receipt.json` 的 `git diff --exit-code` 为 0；T071 历史 raw 继续表示其原 commit 下的历史行为。
- 本修复不把旧 raw 与新 demapper 结果混合，也不重写 Ch3、development 或 confirmation 结论。
- 所有后续新 Ch4 evidence 必须使用 corrected global-ML contract，并以单独 artifact identity 记录。
- 本任务没有运行 BER replay、cell、smoke、grid 或 production；因此不证明 C4 对 B2 的 BER 信号仍存在，也不授权 CP024。
