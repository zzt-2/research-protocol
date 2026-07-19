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

PASS

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

PASS

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

## V006: Batch 0.5 统一 runner 原语与独立复核

> 2026-07-16 | 关联：S044、S045、D045

### 验证项

- TDD 定向回归：事件/指标测试 + common 回归 + prompt015 回归。
- 独立审查 S044 schema：多 fade、fade-end 边界、right censor、symbol 单位、fixed/PI 分离、QPSK 相位与配置签名。
- 隔离性：不修改 `params.py`、历史 runner 或历史结果。

### 证据

~~~text
pytest test_batch_events_metrics.py test_batch_runner_formal.py test_common.py test_prompt015_unified_baseline.py
99 passed in 18.05s

independent review findings fixed:
1. fade_end moved to first block of qualifying recovery run
2. added *_symbol mapping and finite-value config validation
3. channel fade closure no longer fabricates method BER recovery
4. method-aware recovery checks BER/swap/divergence after fade end
5. canonical vs prompt015 legacy channel arrays match exactly for same seed
6. fixed/PI terminal metric equivalence exposed and corrected fixed-phase semantics
7. real prompt013 standard-CMA adapter + canonical generator + unified evaluator + save_results, N=512 smoke PASS
~~~

### 结论

PASS

### 边界

S044 §7 七项经独立复核全部 PASS；准入 Batch 1 首个短序列/单或少量 seed 小批。该结论不放行正式统计长跑；扩大 seeds 前仍需检查首批结果 schema、事件和右删失。

## V007: Batch 1 Fade 单轴首个 smoke

> 2026-07-16 | 关联：S046、D045

### 验证项

- baseline 与 prompt013 standard-CMA 含 `z` 更新逐数组 allclose。
- fade-freeze 与 gradient-clip 单轴互斥，各自机制计数触发，未组合。
- 统一 canonical realization、window grid、fixed/PI/swap/fade/recovery/censor/divergence、共同 valid mask 和 source SHA metadata。
- 2×512 smoke 结果 schema 与实际保存链。

### 证据

~~~text
pytest test_batch_events_metrics.py test_batch_runner_formal.py
       test_batch1_fade_methods.py test_common.py test_prompt015_unified_baseline.py
102 passed in 13.30s

seed41/42 smoke: valid_samples=480 each; freeze_blocks=15; clipped_blocks=15;
baseline counters=0; no divergence; threshold_h=2.0 was a trigger-only setting.
FIR-mask correction: seed41 fixed/PI 0.0336914 -> 0.0015625;
seed42 fixed/PI 0.0317383 -> 0.
~~~

### 结论

PASS（smoke only）

### 边界

不作性能 Go/Kill；不得把 threshold_h=2.0 触发烟测推广为真实 fade 结论。真实参数需先由 pilot 分布和预注册合同冻结。

## V008: Batch 1 真实参数 paired small batch

> 2026-07-16 | 关联：S047、D045

### 验证项

- 5 paired seeds（41–45）、N=100000、四个单轴臂的 schema、mask、finite 和 provenance。
- pilot 冻结的 `h<0.1`、clip P99=`0.0023782561886470004`、P95=`0.0005869870890765639` 机制计数。
- 不作 BER 胜负或性能 Go/Kill。

### 证据

~~~text
top-level config canonical SHA: c9f4ac8a...
N=100000; seeds=41..45; valid_samples=99968 for every seed/method
freeze_blocks=0 for all; divergence=false; fade events=0
clip P99: seed43=61 blocks only
clip P95: seed43=721, seed45=74; others=0
all source SHA fields 64 chars and independently recomputed; all JSON values finite
~~~

### 结论

PASS（small-batch contract/mechanism record only）

### 边界

本批说明真实 pilot 域下 freeze 未触发、两 clip 阈值触发频率不同；不支持性能 Go/Kill，也不代表正式统计批。

## V011: Clip stress small batch

> 2026-07-16 | 关联：S050、D046

### 验证项

- μ=1e-2 压力域、seeds41–45、baseline/clip-P95/clip-P99 三臂。
- 去重后的唯一 seed、schema、valid mask、finite、source/config SHA。

### 证据

~~~text
results=5; seeds=41..45 unique; observation_only_no_go_kill=true
valid_samples=99968 for every seed/method; divergence=false; swap/fade/recovery absent
clip blocks: seed41 P95/P99=64/0; seed42=420/173;
seed43=99/12; seed44=203/24; seed45=31/0
config SHA and 7 source SHA independently verified; nonfinite=0
~~~

### 结论

PASS（observation only）

### 边界

本批只证明压力域 clip 机制确实触发且合同完整，不支持性能 Go/Kill；需另行预注册正式比较。

## V012: Clip stress 1M fallback

> 2026-07-16 | 关联：S052、D046

### 验证项

- `fallback_N=1000000` 与 5M partial 明确分离。
- seeds41–45唯一、baseline/clip-P95/clip-P99三臂、valid/finite/source/config SHA。

### 证据

~~~text
results=5; unique seeds=41..45; observation_only_no_go_kill=true
metrics.valid_samples=999936 for every seed/method; divergence=false; finite=PASS
clip blocks: 41=278/0; 42=720/173; 43=387/10; 44=630/26; 45=307/0 (P95/P99)
config SHA 5753d... and 7 source SHA independently verified
~~~

### 结论

PASS（fallback observation only / inconclusive）

### 边界

全臂 BER=0、无 divergence/swap/fade，不能据此判断 clip 性能；5M partial 仍未完成。

## V010: Prefix-stable generator small batch重跑

> 2026-07-16 | 关联：S049、D046

### 验证项

- D046 修复后的 5 seeds×4臂结果 schema、valid mask、source/config SHA、finite。
- 旧 RNG 数值不再混入新观察。

### 证据

~~~text
config SHA b0ed363a... 重算 PASS; 7 source SHA 逐文件 PASS
observation_only_no_go_kill=true
seeds=41..45; valid_samples=99968; window_grid=1563
freeze=0; divergence=false; fades=0 for all
clip P99: seed42=106; clip P95: seed42=858; others=0
~~~

### 结论

PASS（observation-only）

### 边界

freeze 仍无真实事件覆盖；clip 尚未作性能 Go/Kill。

## V009: GG 长度依赖修复与 h-tail 复核

> 2026-07-16 | 关联：S048、D046

### 验证项

- 失败测试复现同 seed 短/长前缀差异；修复后 prefix exact。
- 5M seeds41–43、CMA64/channel100 两种 block 口径的 h-tail、segments、finite、配置/source SHA。

### 证据

~~~text
pytest test_gg_length_stability.py: 1 passed after fix
related regression suite: 103 passed in 21.36s
prefix exact seeds41/42/43: max_abs_difference=0.0
pooled h<0.1: 0 / 234375 CMA blocks; 0 / 150000 channel blocks
segments=0; min=0.260929867; P1=0.3348275; P5=0.4497675; P50=0.9841192
source SHA and config SHA independently recomputed
~~~

### 结论

PASS（root-cause fix and diagnostic integrity）

### 边界

freeze threshold=0.1 仍未获得真实事件覆盖，列 DEFER/低信息；旧未修复 54.14% low-h 数字作废。不作性能 Go/Kill。

## V013: Batch2 fG lock/swap 事件 pilot

> 2026-07-16 | 关联：S053、D045

### 证据

~~~text
9 cells = fG 30/100/1000 × seeds 41..43; valid_windows=1563; valid_samples=99968
config/source SHA 重算一致；fixed=PI=0；swap windows=0；first_swap=null
diverged=false；fades=[]；observation_only_no_go=true
~~~

### 结论

PASS（schema/source/finite；无事件覆盖，不作性能 Go）

## V014: Batch2 SOP rate 事件 pilot

> 2026-07-16 | 关联：S054、D047

### 证据

~~~text
12 cells = rates 4e-7/1e-6/4e-6/1e-5 × seeds 41..43
config SHA cc511c18…；7 source SHA；valid_windows=1563；valid_samples=99968
rate<=4e-6: 9/9 fixed=PI=0, no swap/div/fade
rate=1e-5: seed41 BER=.00400128 (221 nonzero windows, P99=.078125)
             seed43 BER=.00608445 (240 nonzero windows, P99=.113281)
             seed42 BER=0; all 3 no swap/div/fade
~~~

### 结论

PASS（observation-only；高速 SOP failure 候选，不是 lock-swap Go）

## V015: Batch2 basic blind detector scout

> 2026-07-16 | 关联：S055、D048

### 证据

~~~text
6 cells = 2 SOP rates × 3 seeds；JSON 内部算术一致
config SHA 38df0cea…；列出 source SHA 5 个
oracle: seed41 block1254/symbol80261；seed43 block1286/symbol82309
cm_error/update_norm/power_log_dev: recall=0/2，lead=null
control false alarm: seed42 block0/symbol5（其余无）
~~~

### 结论

FAIL（不可晋级为可复现盲 detector 证据）

### 边界

source SHA 未覆盖生成 scout、阈值校准、持久化、oracle 匹配和汇总逻辑；仓库中未找到对应 evaluator 源码。因此只能确认 JSON 内部数字一致，不能独立重算“无 TX 泄漏”、阈值、recall 和 false alarm。先固化 evaluator+TDD、预注册 warm-up 后重跑；即使排除 block0 假警，当前 recall 仍为 0。

## V016: Blind detector evaluator provenance

> 2026-07-16 | 关联：S056、D048

### 证据

~~~text
blind_detector_evaluator.py source SHA 与 smoke JSON 重算一致
test_blind_detector_evaluator.py: 2 passed
threshold 仅由 control traces 校准；warmup 同时排除 calibration/alarm
persistence=连续K；oracle 只参与 post-hoc lead/recall，测试验证改变 oracle 不改变 alarm
blind trace contract 仅 signal keys，无 TX；smoke warmup0/1 对照稳定
~~~

### 结论

PASS（evaluator 可审计基础已补齐；synthetic smoke 不代表真实 detector 性能）

### 后续边界

需把真实 scout trace 转换脚本纳入 source SHA 后重算真实数据；在此之前不改写 V015 的 FAIL。

## V017: Blind detector 真实短重算链路

> 2026-07-16 | 关联：S057、D049

### 证据

~~~text
4 tests passed；旧 summary 缺 trace 时 convert_scout_cells 明确 ValueError
N=100000；rates=4e-6/1e-5；seeds=41..43；warmup=1；control=4e-6
6 cells，各 trace=1562；config SHA 0598905e…；5 source SHA 重算一致
blind trace 仅 output_start/cm_error/output_power/update_norm，无 TX
oracle failure blocks=1254/1286（post-hoc）；recall=0/2；lead=null
control false alarm=1/3（warmup 后）
~~~

### 结论

PASS（重算链路）；三基础 detector 性能 FAIL/DEFER，不晋级。

## V026b: GW Step1 classification quality closure

> 2026-07-16 | 关联：S068、D055

### 证据

~~~text
82/82 records；candidate_key 82 unique；9字段齐全；title集合与90raw→84dedup→剔2网页说明一致
top-level stats回算一致：priority=6/14/5/5/52；formal=56/26=68.3%；collision=5/26/51
有效source=OpenAlex/S2/Tavily；必读6≥5；formal>50%；至少两路线覆盖
OptComm2021 formal+必读；Virtual Polarization/Self-Homodyne/专利/产品不再direct
~~~

### 结论

PASS（Step1质量门闭合）。备注：stats.subdirections的9/21是独立桶计数，未逐条映射，但不影响≥2路线事实。

## V018: Batch2 geometry feature scout

> 2026-07-16 | 关联：S058、D050

### 证据

~~~text
test_geometry_feature_scout.py: 1 passed
6 cells = rates 4e-6/1e-5 × seeds 41..43；每 trace=1562；finite=PASS
config SHA e276b264…；5 source SHA 重算一致
geometry_trace 仅读取 rX/rY；blind contract 无 sX/sY/h/oracle
cross: recall0/2, FA0/3；cov-eigen: recall1/2, lead487, FA1/3
stokes: recall2/2, lead351/604, FA0/3
~~~

### 结论

PASS（可进入短 pilot；非性能 Go）

## V019: Stokes-like short pilot

> 2026-07-16 | 关联：S059、D051

### 证据

~~~text
18 unique cells = rates 4e-6/8e-6/1e-5 × seeds 41,42,43,46,47,48
geometry tests=2 passed；config SHA 重算一致；3 source SHA；finite=PASS
control 4e-6: seed47 block0、seed48 block325 出现 oracle events
control-only threshold 被污染；stokes raw recall=.2、FA=3/6；cov recall=.3、FA=2/6
~~~

### 结论

PARTIAL（结构/源码通过，但 control-only 前提失效；不可晋级 detector）

## V020: Dual pilot seam 与短集成

> 2026-07-16 | 关联：S061、D051

### 证据

~~~text
pilot tests=2 passed；config SHA 1cb43084…；列出的5 source SHA一致
N=100000；rate=1e-5；seeds41..43；pilots=6252；data=93748；overhead=6.252%
theta mean=.0203-.0324 rad；P95=.0502-.0803；assignment counts总计1563/block
BER baseline→naive pilot: 41 .003985→.004303；42 0→0；43 .006106→.006490
均无 divergence
~~~

### 结论

PARTIAL：pilot估计 seam 可行；集成性能 provenance 不完整，且 naive injection 无收益。

### 阻断

source SHA 未覆盖生成3-seed JSON的集成脚本，缺 same-realization fingerprint、data-mask/BER 汇总可重算链；不能作性能 Go。

## V027b: Step3 五篇正式结构化精读

> 2026-07-16 | 关联：S069、S071、T007

### 证据

~~~text
5/5 read_notes存在；每篇模板字段、7子表、实验完备性齐全
5/5 source.pdf/content.md/metadata.json标题和来源状态一致；read-log新增5行
literature_notes已含L01-L05、方法分类/局限/趋势/背景、实验对标、Q1-Q4
4个失败DOI未冒充替代论文
~~~

### 结论

PASS（Step3门闭合，可进Step3.5）。边界：Q1可作为合法问题候选；Q2按当前文字 FAIL/PARTIAL（M写成己方6pilot+EMA，A不是现有M失效假设），Q3/Q4虽形式满足但为光纤/相位邻近out-of-scope，只作竞品/先验。进Step4a前必须按D055重写Q2的M-C-A。

## V028: Pilot Jones GW Step3.5 独立门控

> date: 2026-07-17
> 关联：S072 / S073 / D056

### 验证项

- [x] 关键词矩阵：读取 `search-archive/2026-07-16/step35-*.json` 六组查询 → 42 条原始、41 条 canonical 去重；三类方法变体（稀疏时域 pilot、频域 FPT、training/preamble）× coherent/FSO-GG 场景覆盖，两个 FSO+GG 精确查询均为 0。
- [x] 搜索源：六组结果的 `sources` 实际为 `s2/openalex`；结果 `source_api` 计数为 Semantic Scholar 34、OpenAlex 6、混合来源 2，满足 Step3.5 的至少两源门槛；此前 S073 所称 Tavily 已纠正为不含 Tavily。
- [x] 引用链：`lcomm-2026-backward-citations.json` 实际 19 条，`lcomm-2026-forward-citations.json` 为 0 条；后向结果包含 JLT 2022.3224805（约 25–36 citations）和 OE 2021.419574（约 19 citations）等直接竞品。
- [x] 直接竞品记录：`step35-direct-read5.json` 含 5 条正式论文，4 条仍为摘要级，OE 2021 `10.1364/OE.419574` 已有 `papers/doi/10.1364_oe.419574/content.md` 与 `metadata.json`（`download_status=success`, `content_quality=good`），并已形成 `papers/_read_notes/10.1364_oe.419574.md`；没有把失败 DOI 冒充全文。
- [x] OE 2021全文核验：第178–190、208–251、257–299、327–344行明确 3 pilot tones、逐 block 平均、解析 RSOP 矩阵与 inverse、短 block 噪声 penalty、长 block 动态失配、退化矩阵/定点溢出与 PSR=-18 dB；该文直接覆盖 pilot→块级矩阵→逆补偿机制，但无 OSL GG、时域≤10% overhead、EMA 或 fixed-label 指标。
- [x] Q2保守性：`literature_notes.md` L06–L10 已将 generic pilot/Jones、block inverse、时间平均判为已占据；明确“仅靠换大气场景或 EMA 参数差异必须 Kill”，保留的问题限定为 GG 深衰落下可观测性/条件数/动态失配是否改变稳定化结构。
- [ ] 收敛门：R1 新增必读4/建议读1；R2 `search-archive/2026-07-17/step35-r2-1..6.json` 又产生 8 条/5 unique，其中新增 JLT 2023 `10.1109/JLT.2023.3311036` FPT/PDL 直接竞品，未达到“最后一轮新增必读/建议读=0”。
- [ ] 引用链选点：当前双向链围绕 LCOMM 2026（citation_count=0）；按规范应对最高引用的核心竞品（至少 JLT 2022 `10.1109/JLT.2022.3224805` 或 OE 2021 `10.1364/OE.419574`）补双向链，或记录选择 LCOMM 的明确理由。

### 证据

~~~text
R1 matrix: 6 JSON, 42 raw, 41 unique; exact FSO+GG queries = 0/2
R1 result sources: semantic_scholar=34, openalex=6, mixed=2; no Tavily result
LCOMM citations: backward total=19; forward total=0
R1 direct-read5: new_must_read=4, new_suggested_read=1, second_round_needed=false (field conflicts with gw-supplement gate)
R2: step35-r2-1..6 = 8 raw, 5 unique, all published; JLT 2023.3311036 is a newly surfaced FPT/PDL competitor
OE metadata: download_status=success, content_quality=good, content_file=content.md, title_check=match
OE full-text anchors: content.md L178–190, L208–251, L257–299, L327–344
~~

### 结论

PARTIAL：关键词覆盖、双源、41 unique、竞品摘要记录、OE全文证据链和保守Q2判断均通过；但 Step3.5 收敛硬门未通过（R2仍产生新的直接竞品），且双向引用链未围绕最高引用核心竞品展开。不能把 Step3.5 标为完成，也不能直接进入 Step4a。

### 后续（PARTIAL 时）

执行第三轮且只围绕 R2 新增 JLT 2023 PDL/FPT 及其引用链做定向检索；若最后一轮新增必读/建议读为 0，再补最高引用直接竞品的双向链并更新 `literature_notes.md`。随后重新独立审查 V029；进入 Step4a 时将 L08/OE 2021 作为强 direct baseline，Q2 仅可在证明 OSL GG 引入结构性新失效机制后继续。

## V021: Pilot-informed Jones derotation 三臂短跑

> 2026-07-16 | 关联：S062、D052

### 证据

~~~text
4 tests passed；config SHA 3ba30844…；6 source SHA一致
3 seeds各唯一same-realization fingerprint；三臂共享data mask，valid_data_samples=93720
pilots=6252；data=93748；overhead=6.252%；pilot位置排除BER
baseline=canonical RX；naive=noise-preserving pilot RX；derotation=pilot LS H pinv仅作用data
seed41 fixed=PI .003985/.004303/0；seed42 0/0/0；seed43 .006106/.006490/0
三臂无divergence；部署估计器无TX/h/theta truth leakage
~~~

### 结论

PASS（短集成/公平性合同；pilot Jones derotation feasible，仍为 observation-only）

## V022: Pilot Jones 72-cell expansion

> 2026-07-16 | 关联：S063–S064、D053

### 通过证据

~~~text
72 unique=8 seeds×3 rates×3 counts；config SHA/6 source SHA一致
三个24-cell checkpoints与master逐cell exact；同(rate,seed)三count fingerprint一致
overhead=3.126/6.252/9.378%；4p/6p shared valid=93720/90596
clean/failure定义与relative公式可重算；4p/6p clean退化=0/9
~~~

### 阻断

预注册要求 failure cell 相对改善≥50%，但原 summary `failure_improved` 只计任意正改善。正确计数：2p=9/15，4p=13/15，6p=14/15；6p 的 4e-6 seed47 仅6.33%。另2p的1e-5 seed47 derotation发散，valid=13020 vs baseline/naive=96844，违反该cell shared denominator。

### 结论

PARTIAL：数据/provenance PASS；门槛汇总与2p公平性失败，暂不满足D052正式GW晋级门。

## V023: Jones inverse 稳定化与 EMA09 full24

> 2026-07-16 | 关联：S065、D053–D054

### 证据

~~~text
integration3 + summary1 tests = 4 passed
problem seed47 baseline=.0120756；EMA .5/.9/.99改善57.29/72.92/74.63%
Tikh/guard仅6–20%；clean controls无退化；选择EMA=.9
EMA09 full24: 24 unique=8 seeds×3 rates；15 failure/9 clean
failure≥50%=15/15；clean退化=0/9；divergence=0；equal denominators=true
rate分层=3/3、5/5、7/7；fingerprint与旧6p cells一致
full24 config SHA与3 source SHA当前匹配
~~~

### 结论

PASS（EMA09 full24满足D052原门槛，可晋级正式GW Step1）；旧72-grid整包provenance见V024。

## V024: 旧72-grid historical provenance 注释

> 2026-07-16 | 关联：S065、D054

### 结论

PASS（透明记录合规）：保留原historical run SHA，明确current runner已变化、exact snapshot缺失、summary事后新增并引用V022。精确源码重放能力仍PARTIAL；正式晋级证据依托EMA09 full24独立SHA，不声称旧grid可由当前源码重放。

## V029: Pilot Jones GW Step3.5 三轮收敛与引用链复核

> date: 2026-07-17
> 关联：S072 / S073 / D056 / V028

### 验证项

- [x] R1统计：直接读取 `search-archive/2026-07-16/step35-*.json` 六组矩阵结果 → 42 raw、41 canonical unique；新增必读4、建议读1，故R1未收敛。
- [x] R2统计：读取 `search-archive/2026-07-17/step35-r2-{1..6,extra-1..4}.json` 并按 DOI lowercase/title normalized 去重 → 31 raw、25 unique；与既有全库比较，新增必读0、建议读0。
- [x] R3统计：读取 `step35-r3-jlt2022-forward.json`、`step35-r3-oe2021-forward.json`、`step35-r3-pdl-forward.json`、`step35-r3-pdl-search.json` → 50 raw、37 unique；与排除 R3 文件后的全 `search-archive` 20,986 个既有键比较，新增 DOI/title=0。三轮上限已达到，检索结果收敛。
- [x] 最高引用竞品：现有索引计数为 JLT 2022 `10.1109/JLT.2022.3224805`=36、OE 2021 `10.1364/OE.419574`=19、PDL JLT 2023 `10.1109/JLT.2023.3311036`=7；JLT 2022 正确选为最高引用直接竞品。
- [x] Forward链：JLT 2022 forward=25、OE 2021 forward=11、PDL JLT 2023 forward=7；摘要筛查得到的相关项均已存在既有语料，未产生新候选。
- [ ] Backward链：`step35-r3-jlt2022-backward*.json`、`step35-r3-oe2021-backward*.json`、`step35-r3-pdl-backward.json` 的 `query` 均为空且返回0；`step35-r3-summary.json` 明记 Semantic Scholar Graph DOI 直查为 HTTP 429，OpenAlex/包装器亦存在 DOI unresolved/skipped。该结果只证明工具链不可用，不能作为“真实0篇参考文献”或已完成后向引用分析的证据。
- [x] 竞争判断：OE 2021全文已证实 3 PT、block averaging、解析RSOP矩阵与inverse，并明确短block噪声、长block动态失配及矩阵退化/溢出风险；Q2继续保持“generic机制已占据、仅OSL GG结构性新失效可救”的保守边界。

### 证据

~~~text
R1: raw=42, unique=41, new_must=4, new_suggested=1
R2 summary: raw=31, unique=25, new_must=[], new_suggested=[]
R3 independent recompute: raw=25+11+7+7=50, unique=37
R3 vs all prior search keys: prior=20986, new=0
citation counts: JLT2022=36, OE2021=19, PDL-JLT2023=7
forward totals: JLT2022=25, OE2021=11, PDL-JLT2023=7
backward JSONs: query="", total=0, results=[]
direct Semantic Scholar DOI check: HTTP 429
R3 summary gate_status=PARTIAL; backward status=UNAVAILABLE, not zero references
~~~

### 结论

PARTIAL：三轮检索已经在数量与新增候选维度收敛，最高引用直接竞品选择和 forward 链筛查通过；但后向引用链未实际取得，`0` 是空 query/HTTP 429 造成的不可用结果，不满足 `gw-supplement.md` 的“双向引用链已分析”硬项。

因此 Step3.5 **目前不能按正常 PASS 门控进入 Step4a**。若主线要带债推进，必须先取得明确的用户/流程豁免并把 backward 未验证列为阻断性债务；不得把当前0返回写成“无参考文献”或“后向链已分析”。

### 后续（PARTIAL 时）

优先在限速恢复后用 Semantic Scholar/OpenAlex DOI 端点重取 JLT 2022 backward references；若API持续不可用，获取JLT 2022全文/正式参考文献表或使用可审计的Crossref/OpenAlex works引用关系完成后向链。取得真实 backward 列表、筛查并确认无新增直接竞品后，再做 V031（V030 后用于 P03 终验）；不需要第四轮关键词泛搜。

## V030: P03 residual-headroom Scout 最终独立终验

> date: 2026-07-19
> 关联：S075 / D057

### 验证项

- [x] source recovery：独立 verifier 检查 exact `_gg_time.py` SHA、raw Git blob、snapshot 重建与 historical z-window → `92eaa6…` / blob `9155de…` / z-window `3d99d4…` exact PASS
- [x] standard-CMA：静态检查公式并运行 numeric identity gate → `(R2-|z|²)·z·conj(r)`，`godard_with_z_formula_numeric: PASS`
- [x] runtime closure：逐文件核对 runtime manifest SHA、Git blob OID 和 blob bytes → 7/7 PASS
- [x] P03 tests：独立运行定向 suite → 43/43 PASS
- [x] deterministic probe：正式 artifact、第二次 rerun、第三次 fresh temp probe逐文件比较 → 6/6 SHA exact equal
- [x] science recompute：独立重算 10 cells 的 fixed/PI BER、SER、headroom、coverage 和 residual statistics → verdict 与 `P03_ANALYTIC_COVERAGE_GE_90` 一致
- [x] history/scope guards：比较 HEAD、路径和新文件 → B001–B003 无差异，B004=0，无 ML/Queue/Registry/paper/common/params/canonical-state 修改
- [x] governance：status/readiness/triage/BatchPlan/README/master-state/projects-overview/S075/D057 交叉检查 → formal BLOCKED、P03停止、未选择下一候选一致

### 证据

~~~text
python -m pytest projects/thesis-fso/direction-lab/tests -q -k p03_
43 passed, 142 deselected

runtime manifest: 7/7 SHA + Git blob OID + blob bytes match
manifest SHA: 3ecaa092e0c3a16301364aec74836678af81ac4e9ba6abe141503f30d31fc99f
manifest blob: d9151ff68094fba7924c28b19ed270769da63e26

probe-result.json: 1232d1a47431f14729045c04beafe0836e531ad238f9bcb8e15462c2f7901cdd
probe-summary.yaml: 39f72da078a6bc4a0182f2397a82e80556049acc058d59bf72131a5fd9dfab87
source-closure.yaml: 4584371503e0f19e2cb519c612c550917020e8212a2a0252f24d0f636b4bb5d2
source-equivalence/report.yaml: f49c91bdaa86c6a67c86749ae9a23eff4cad4b2f5513def3a47d2b21d3305415
source-equivalence/source-closure.yaml: bb97261bc9fd3e264e8ec3ba9470afd0f04e13d7f6e778f388cde59315f49368
source-equivalence/z-window.json: 3d99d4fef5f3749d2047816b8bc655affc207f307bafc808b6de887b88ca64f7
three runs: all six hashes exact equal

10/10 cells: nearest/blind/oracle fixed BER=PI-BER=fixed SER=PI-SER=0
visible_headroom=0.0; simple_gain=0.0; zero-headroom coverage=1.0
nearest residual mean=0.2855824473; blind affine=0.0466822478
selected residual CV=0.703962; 2/10 nonzero tail cells

git diff HEAD -- B001 B002 B003: empty
B004 count=0
projects/simulation/common + params.py + canonical-state.yaml diff: empty
~~~

新增 canonical-LF line-ending test 前，完整 Direction Lab suite 的旁证结果为 `147 passed, 37 failed`；37 个失败均在非 P03、当前 diff 未修改文件，集中于 Windows CRLF 旧指纹与既有 `DEFAULT_SOURCE_ROOT` linked-worktree 路径假设。该环境/治理债务不构成 P03 回归，不把本轮表述成“全 Direction Lab suite 全绿”。

### 结论

PASS
