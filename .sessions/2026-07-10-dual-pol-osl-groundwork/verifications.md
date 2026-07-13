# Verifications — 双偏振星地光通信 DSP Groundwork

## V001: PROMPT-011 CMA 根因诊断与独立复审

> date: 2026-07-13
> 关联：S012 / D016

### 验证项

- [x] 标准复数 CMA 单块公式：test-first 验证 `w += μ(R²-|z|²)z·conj(x)` → PASS
- [x] 旧实现差异：单块测试确认 `_cma.py` 缺少输出因子 → PASS
- [x] 偏振排列口径：穷举 2!×4×4，相位和排列消歧 → PASS
- [x] 结果汇总：独立 verifier 从 trials 重算 mean/std/classification → PASS
- [x] 元数据：`save_results()` 注入 script/common_md5/git_commit/timestamp → PASS
- [ ] 正式多 seed 性能：当前仅 3 shared seeds，尚未达到 ≥10 seeds → PENDING

### 证据

```text
python -m pytest tests/test_prompt011_cma_root_diagnostic.py -q
...                                                                      [100%]
3 passed in 2.91s

current scalar-error CMA: fixed=0.4740688±0.0201434, PI=0.0305725±0.0253484, swap=3/3
standard complex CMA:     fixed=0.1757468±0.2040605, PI=0.0349015±0.0268368, normal=2/3 swap=1/3
oracle:                   fixed/PI=0.0139463±0.0144549, normal=3/3
diverged: 0/3 for both CMA variants
```

独立复审：公式注释与 ACP 印刷符号区分后 P1 关闭；结果改走 `common._experiment.save_results()` 后 P2 关闭；复审目标测试 `3 passed in 3.17s`。

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

3 seeds 已足以否决“现有约 0.5 BER 必然代表通信断开”的前提，但不能形成正式性能数字。下一轮扩至 ≥10 shared seeds，并重审所有依赖旧 `_cma.py` 与固定标签 BER 的历史结论。
