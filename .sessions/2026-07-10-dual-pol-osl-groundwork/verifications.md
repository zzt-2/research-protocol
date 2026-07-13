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

---

## V002: PROMPT-012 双口径历史重审与独立复核

> date: 2026-07-13
> 关联：S013 / D018

### 验证项

- [x] S005 四关键格：4 grids×10 shared seeds，独立重算 divergence/分类/fixed/PI/summaries 0 不一致 → PASS
- [x] N=5M 长序列：10 unique seeds、显式 torch_seed、脚本 SHA、30 个方法分类独立重算 0 不一致 → PASS
- [x] N=2M 短序列：3 f_G×10 unique cells、完整 experiment signature、同信道三方法、fixed/PI/分类/summaries 独立重算 0 不一致 → PASS
- [x] 代码验证：三个目标测试、py_compile、git diff-check → PASS
- [x] 元数据修复不改结果：S005 grids、long 正式统计、short trials/summaries digest 均保持不变 → PASS

### 证据

```text
S005 final verifier: PASS
script/json SHA256 = 6c71a139a08c2944c74a5c723716aa48ac86a8d3d576e26d41ad1df7c63b1617
grids digest = f17eb21587e9c4e90e71c234f6c40b2434ecb6ea11a8116a22a43f50b4582ed1
40 unique trials; 18 diverged (all norm>10x); 21 swap + 1 collapse among stable

longseq final verifier: PASS
source-composite/json SHA256 = 1a8c7f6496a3d818abc2b976cd6b5e3a6a87ebfc3320ebffe088207f8448c9ba
source-composite covers prompt012_longseq_audit.py + ml_long_seq_failure.py; parameters/signature T_S=4e-10
trials digest = 22813b6a14c7fbb6130e8564c71deeb514c18a3bb0eedd44e5632dac0886428c
summaries digest = 8bdc07de6fc730fb15f09741b400ab1f0907ee4f5a8c55d1508080d53f98493c
10 unique seeds; torch_seed=seed 10/10
CMA fixed/PI = 0.476720±0.031933 / 0.031739±0.051317; clean/degraded swap=8/2
ML  fixed/PI = 0.497407±0.005310 / 0.005230±0.012430; clean swap=10/10

shortseq final verifier: PASS
composite/json SHA256 = e3ea95c6c21d2f340d9881358356bdc55447ad4de08be8a3c30e7f38aef33fa4
trials digest = fc8649a1d642a4b490a841404eb5efa39c589d1d92783483a22383efc0a7d678
summaries digest = 3fcbe25bcf0713ea40289e92698d41f8c1a2891ba896feb5707e8c2d107aa752
30 unique cells; torch_seed=seed 30/30; ML PI paired wins=10/10 at each f_G for full and late

python -m pytest \
  projects/simulation/tests/test_prompt012_divergence_audit.py \
  projects/simulation/tests/test_prompt012_longseq_audit.py \
  projects/simulation/tests/test_prompt012_shortseq_audit.py -q
..............................                                           [100%]
30 passed in 3.22s

py_compile: exit 0
git diff --check (task files): exit 0
```

正式 JSON：

- `projects/simulation/results/cma-fade-divergence/prompt012_divergence_audit.json`
- `projects/simulation/results/cma-fade-divergence/prompt012_longseq_audit.json`
- `projects/simulation/results/cma-fade-divergence/prompt012_shortseq_audit.json`

三个结果文件受 `results*/` 规则 gitignore；可复现代码、测试与审计报告纳入版本控制。

### 结论

PASS
