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

---

## V003: PROMPT-014 盲 VQ-VAE 实现与首轮正式比较

> date: 2026-07-13
> 关联：S014 / D019

### 验证项

- [x] 实现与实验合同：独立审查固定码本/STE/无标签 fit、shared realization、双口径评价、严格签名与分片合并 → PASS
- [x] 代码验证：VQ 核心、DP shared channel、实验驱动与合同联合回归 → 48 passed
- [x] 100k 资源门控：默认 391 updates、JSON/save/sanity/CUDA 全路径 → PASS
- [x] 正式 checkpoint 完整性：3 文件共 11 unique cells、严格 JSON、finite、内部/跨文件签名与当前 7 组件 SHA → PASS
- [ ] 正式 30-cell gate：只完成 11/30，且 seed1004 `loss_decreased=false` → FAIL/PARTIAL
- [x] loss 语义审计：首末 update 对应不同连续 batch，不能作为固定 probe 收敛证据 → FAIL（门控设计）

### 证据

```text
target+core regression: 48 passed in 5.83s
independent experiment review: Spec PASS; Quality PASS

100k smoke:
wall=14.61s; updates=391; loss=0.06960639 -> 0.03765663
usage=1.0; finite=true; sanity.all=true; gate=INCOMPLETE

formal checkpoint composite SHA256:
1e6ab7719ed9f0d136e358a5ac4a623a91f596586b45fecb3d2b4b4b6c22a807
11 trials / 11 unique / missing 19 / strict JSON PASS / all numeric values finite

current subset (diagnostic only):
f_G=30:   n=2, VQ PI mean=0.046426250, CMA=0.122876875, paired wins=2/2
f_G=100:  n=2, VQ PI mean=0.053955750, CMA=0.154093375, paired wins=2/2
f_G=1000: n=7, VQ PI mean=0.010625500, CMA=0.111315714, paired wins=7/7

f_G=1000, seed=1004:
total first/last=0.020491542/0.199085236
total first100/last100 mean=0.049006393/0.232686317
reconstruction first100/last100=0.018055079/0.013565502
commitment first100/last100=0.030951314/0.219120816
finite=true; usage_gt_half=true; non_collapse=true; loss_decreased=false

fit cursor:
first center batch=[0,128); last center batch=[999936,1000000)
```

正式 JSON：

- `projects/simulation/results/cma-fade-divergence/vae_vs_cma_blind_part_a.json`
- `projects/simulation/results/cma-fade-divergence/vae_vs_cma_blind_part_b.json`
- `projects/simulation/results/cma-fade-divergence/vae_vs_cma_blind_part_c.json`

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

当前结果候选已知最终不可 PASS，停止剩余 19 cells。若继续，先在查看新结果前冻结同一 probe 的训练前/后 sanity，更新 SHA 后从 0 重跑完整 30 cells；不得混用当前 11 cells。

---

## V004: PROMPT-013 交换质量真实性与机制验证

> date: 2026-07-13
> 关联：S013 / D020

### 验证项

- [x] Q1 原始 trials：独立重算 seeds 1000–1029、shared seed、finite、PI/excess、胜场与 Wilcoxon → PASS
- [x] Q1 provenance：记录的 9 项 SHA、P12 结果 SHA、Q1 JSON 被 Q2 引用的 SHA → PASS
- [x] Q2 固定 trial/窗口：high/low 六 seeds、每方法 13 windows、Q1 gap 与共享 realization → PASS
- [x] H_a/H_b/H_c：不信任 summary，按预注册阈值独立重算 → H_a FAIL，H_b UNKNOWN，H_c 容量同构 PASS 但初始化混杂存在
- [x] 目标代码验证：Q1/Q2/P12 long/short 回归与 5 个相关脚本 py_compile → PASS
- [ ] P12 divergence 回归：范围外脏改删除 `BLOCK/T_S` 导出，collection ImportError → BLOCKED（非 PROMPT-013 路径）

### 证据

```text
Q1: 30 unique seeds; nonfinite=0
CMA/ML/oracle PI mean = 0.0213143867 / 0.0077507067 / 0.0065967333
CMA/ML excess mean = 0.0147176533 / 0.0011539733
ML/CMA/tie = 30/0/0; exact two-sided Wilcoxon W=0, p=1.862645149230957e-09
clean<=0.05 CMA=25/5 ML=29/1; clean<0.01 CMA=20/10 ML=25/5

Q2: fixed high=[1006,1017,1011], low=[1024,1028,1029]; 13 windows each; nonfinite=0
H_a = falsified
H_b = unknown; oracle rho null 10/12; freeze main threshold current=0/3, standard=0/3
H_c = 88/88 real DOF; no bias/nonlinearity; ML cross-center actual=1 vs comment/CMA=0
Q1 9 SHA + Q2 12 SHA all match current disk

python -m pytest [Q1,Q2,P12-longseq,P12-shortseq] -q
60 passed in 3.27s
py_compile (5 related scripts): exit 0
P12 divergence suite: collection exit 2, ImportError BLOCK/T_S from dirty r_lcr_ber_impact.py

---

## V005: PROMPT-015 统一合法 baseline 重比

> date: 2026-07-13
> 关联：S015 / D021

### 验证项

- [x] 30-seed 正式 checkpoint：seeds 1000–1029 唯一、完整、无 pending、范围正确 → PASS
- [x] 统一 realization 与评价窗口：每 seed 共享同一信道，四方法和 oracle 使用同一 late slice → PASS
- [x] 原始指标质量：所有方法 fixed-label BER、PI-BER 与超额 PI-BER finite → PASS
- [x] ML 执行审计：ML-original、ML-aligned 每个 seed 均 constructed/trained/inferred=true，实际 device=cuda → PASS
- [x] 初始化审计：ML-original 交叉中心为 1，ML-aligned 的 conv_RR/conv_RI 交叉中心均为 0 → PASS
- [x] provenance：结果 summary 可由 trials 重算，experiment signature 与当前脚本一致，10 项 source SHA 一致 → PASS
- [x] 预注册主判据：standard-CMA vs ML-original/aligned 均 p<0.05 且 ML 29/30 胜 → PASS，overall GO
- [x] CLI dry-run：不调用长序列执行，生成 0 trials、pending=[1000] 的临时 checkpoint → PASS
- [x] 专项与历史回归、编译和差异检查 → PASS

### 证据

~~~text
prompt015 focused: 12 passed in 4.02s
Q1/Q2/P12 regression: 60 passed in 4.36s
py_compile: exit 0
CLI dry-run: exit 0, trials=0, pending=[1000]
independent result audit:
  AUDIT PASS: checkpoint/schema/finite/signature/SHA/summary/init/device
  formal source SHA count=10
primary:
  standard-CMA vs ML-original: 29/30, exact p=1.1920928955078125e-6
  standard-CMA vs ML-aligned: 29/30, exact p=1.1920928955078125e-6
  overall gate: GO
git diff --check: PASS
~~~

正式 JSON：

- projects/simulation/results/cma-fade-divergence/prompt015_unified_baseline.json
- projects/simulation/explore/cma-fade-divergence/PROMPT_015_REPORT.md

### 结论

PASS

### 边界

结论限于 D021 注册的 N=5M、QPSK、strong、f_G=30、SOP=4e-7 参数域；不自动推广到 Contract 或其他参数域。seed 1014 的 elapsed_s 受墙钟挂起影响，不作为性能指标。
