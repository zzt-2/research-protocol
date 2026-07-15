# Verifications — CCISP 2026 论文内容补强

## V011: 路线 B 旧参数网格实现与等价性核验

> date: 2026-07-15
> 关联：S001 / D016

### 验证项

- [x] 读取独立 verifier 报告 `_verify_b_vs_a_equiv_report.json` → 33 点 × 30 seed 共 990 项 selector 端整数严格相等，`n_mismatches=0`。
- [x] selected complex output 抽查 → 20 个窗口中 DA 18/18、NDA 2/2 与对应分支输出逐样本匹配，shape 检查 20/20。
- [x] 代码路径抽查 `_a4_branchrouted_30seed.py:369-402` → `decide` 后只进入一个分支，`selected_rx` 被物化并做 complex shape 断言。
- [x] branch compute 计时读取 → weak@5 dB、seed 0、400 windows 下 A=`0.8611907507 ms/window`，B=`0.2183444996 ms/window`，报告 savings=`74.6462094%`；计时只覆盖 branch compute。
- [ ] 新参数与投稿级证据 → 尚未验证；当前结果只覆盖旧三档参数，NDA 仍用 `tx_bits` 做 post-hoc ambiguity resolution。

### 证据

```text
bitexact_selector: n_checked=990, n_match=990, n_mismatches=0, pass=true
selected_rx_extraction: windows_checked=20, da_match=18/18, nda_match=2/2, shape_ok=20
branch_compute_wallclock:
  A_per_window_sec=0.0008611907507292926
  B_per_window_sec=0.00021834449958987534
  wallclock_ratio_B_over_A=0.2535379059807273
  savings_pct=74.64620940192728
structural_limits_NA: nda_only_baseline, per_block_oracle, gain_db
source: projects/simulation/explore/nda-awgn-tracking-sandbox/_verify_b_vs_a_equiv_report.json
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

路线 B 的旧参数实现与 selected-output 等价性 PASS；投稿证据仍需在 A1+ 新参数冻结后，用同 realization 的 A 评估 runner 与 B receiver runner重建。74.6% 不得外推为完整接收机总时延节省或多场景统计结论；non-genie 可部署性仍为 BLOCKED。

## V010: adaptive CPR selected-output 实现真实性验证

> date: 2026-07-15
> 关联：S001 / D014 / D015

### 验证项

- [x] 权威生成链：JSON provenance 中脚本及依赖 hash 与当前文件匹配 → PASS。
- [x] 分支输出：DA/NDA recovery 均返回复数校正序列 → PASS。
- [x] selector runtime：追踪 caller 后确认两路先执行，`phi_est` 被丢弃，selector 只 mux error counts → selected phase/complex output FAIL。
- [x] Fig.2：`theta_da/theta_nda -> selector -> Selected theta -> phase compensation` 强于实际 caller → FAIL。
- [x] 数值等价：common-768 硬判 BER 在七项严格条件下可与后验 output mux 等价，但依赖 `tx_bits` 旋转消歧，不能支持在线输出 → PARTIAL。

### 证据

```text
common/_recovery.py:136-168,171-237
  DA/NDA return rx_comp and phase/frequency estimates

_a4_switch_common768_30seed.py:120-139
  both branches execute; phi_est return slots discarded; per_block returns 3 integer error counts

_a4_switch_common768_30seed.py:325-342
  branch processing precedes decide(); selector only accumulates ne_d or ne_n_common768

fig2_adaptive_cpr.drawio:117-140
  theta_da/theta_nda -> selector -> Selected theta -> phase compensation

common/_modulation.py:278-310
  NDA ambiguity resolution selects among eight rotations using true tx_bits
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

停止 R009 定位 WRITE 和 R010 局部图修。先拍板真实性路线：收窄为 branch-decision/post-hoc selected-BER evaluation，或另开仿真范围实现并验证真实 selected phase/complex-output mux。

## V001: CCE-CC-002 独立合同审查

> date: 2026-07-14
> 关联：S001 / D001

### 验证项

- [x] 词数预算：独立逐节复算 → 2,219 - 985 + 2,336 = 3,570，净增 1,351，超过 3,500 下限 70 词。
- [x] 章节比例：独立复算 → System Model + Method + Results 为 2,615 / 3,570 = 73.25%，满足不少于 70%。
- [x] 公式证据：抽查接收模型、100/256 block、DA-LS、CV、blind-h/effective-SNR、1.10/13 dB、pilot 开销和 Fig.3 指标 → 8 项与代码指针一致。
- [x] 公式总账：复审现有 5 组的保留/替换/合并与净新增 3 组 → 最终 8 组；仅 Gamma–Gamma product 可选为第 9 组。
- [x] 证据门和降级边界：复审 Batch A/B/C → 内容级文献核验前置；EXCLUDED/REMOVED 不计入 PASS 分母；方案 B 不自动执行。

### 证据

```text
Abstract: 133 - 133 + 170 = 170
Introduction: 420 - 95 + 315 = 640
System Model: 341 - 85 + 424 = 680
Method: 715 - 330 + 700 = 1,085
Results: 513 - 245 + 582 = 850
Conclusion: 97 - 97 + 145 = 145
Total: 2,219 - 985 + 2,336 = 3,570
Net increase: 1,351
SM + Method + Results: 2,615 / 3,570 = 73.25%
Other sections: 955 / 3,570 = 26.75%
```

```text
最终复审：PASS
- 现有 5 组公式经保留/替换/合并后仍为 5 组。
- 固定净新增 3 组，最终为 8 组。
- 仅 Gamma–Gamma product 可作为第 9 组。
- blind-h/effective-SNR 已明确并入 switching 替换组。
- 完整相位过程已归入现有相位公式替换。
- crossover 根不加入。
- “最终 8–9 组、任何时候不超过 9 组”全文一致。
```

### 结论

PASS

## V013: T018 正式闭环参数证据门与 common 接口核验

> date: 2026-07-15
> 关联：S001 / D018 / R016

### 验证项

- [x] H001 接收：R015 六门与 45/45、common 尾接口、D018 scope change 逐文件核对 → PASS。
- [ ] Al-Habash 原文：仓库 DOI 下载、机构库直链和结构化检索 → 无合法本地 PDF/content，FAIL。
- [ ] Family-1 三锚：精确检索与现有论文库审计 → 无同时给出 `0.2/1.6/3.5` 和三档定义的一手全文，FAIL。
- [x] 数学复算：三对 alpha/beta 六项相对误差均 0，闪烁指数严格有序 → PASS。
- [x] common 接口：专项、common 和 layered tests 新鲜执行 → 97/97 PASS。
- [x] 硬门响应：未改 params、未跑 formal、未改图文；未验证 runner 骨架已精确删除 → PASS。

### 证据

```text
Al-Habash DOI download: all_failed
local metadata: papers/doi/10.1117_1.1386641/metadata.json (failed; no content_file)
search records:
  search-archive/2026-07-15/al-habash-2001.json
  search-archive/2026-07-15/al-habash-pdf-web.json
  search-archive/2026-07-15/family1-values.json
  search-archive/2026-07-15/family1-exact-web.json

recompute relative errors: 0, 0, 0, 0, 0, 0
scintillation indices: 0.1930995127, 0.9017627797, 1.1444839782

python -m pytest tests/test_channel_turb_params.py tests/test_common.py tests/test_layered_verification.py -q
97 passed in 12.27s
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

只在 Al-Habash 公式原文和 Family-1 三锚来源均形成合法本地 `source + content.md + metadata/index` 后重开 T018 宏阶段一；先独立复算，再改 `params.py`。不得用摘要/DOI降级放行。

## V012: Family-1 三档下行诊断与正式开跑门

> date: 2026-07-15
> 关联：S001 / D017 / R015 / T017

### 验证项

- [x] common 无副作用参数注入口：QPSK/APSK 默认路径、显式旧值、Family-1 实际进入 `gg_block`、非法输入，共 19/19 专项回归 PASS。
- [x] old/new 诊断矩阵：3 scenes × 5 SNR × 3 seeds × 400 windows 完整，无缺 seed、重复或非法参数。
- [x] 路线 A/B：45/45 scene-SNR-seed 单元的 selected errors、DA/NDA 选择数、seed 边界、realization hash 与 selected BER 严格一致。
- [x] 选择互补性：DA=5,223、NDA=12,777 windows；无全局 ≥99% 单分支退化。
- [x] 六条预注册筛选门全部 PASS；fixed winner 在 3/15 cells 变化，selected-vs-fixed-NDA 正 gain 为 10/15 cells，strong 严重度顺序正常。
- [x] 结果身份：JSON 明确为 `diagnostic_probe_not_for_paper`，未混入正式参数源、旧权威 JSON 或论文。

### 证据

```text
R015-三档新下行参数诊断结果.md
_family1_downlink_probe.json
_verify_family1_downlink_probe_report.json
new selected BER vs old: 15/15 cells lower
largest absolute change: strong@13 dB, 0.2009885 -> 0.1301237
A/B exact: 45/45
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

诊断足以解除“是否值得正式重跑”的门，支持 D018；但它不是论文统计证据。正式参数仍须先闭合本地一手来源，再完成 30-seed 数据、990/990 A/B、独立 verifier、图文同步与 fresh render，才能判整稿 PASS。

## V009: D013 扩展网格、定量图与整稿独立终验

> date: 2026-07-15
> 关联：S001 / D013

### 验证项

- [x] 权威数据：独立 verifier 读取 JSON 并复算 paired-seed mean 与 Student-$t$ CI → 33 个场景点、30 paired seeds、$5{:}2{:}25$ dB 网格全部一致，PASS。
- [x] 结果叙事：独立复核 9 dB 代表点及 19--25 dB 高 SNR 区 → 数字与“趋近 fixed NDA、无统计可区分惩罚”表述一致，PASS。
- [x] 定量图符号：检查三张绘图脚本和 PDF → 横轴均为 `Data-symbol $E_s/N_0$ [dB]`，Fig.5 纵轴 $G_{\mathcal C}$ 与正文定义闭合，PASS。
- [x] 正文与构建：修复未定义的 $\gamma_{\mathrm{tot}}$ 后 fresh `latexmk`，并独立检查日志/PDF → 8 页、20 条参考文献，warning/undefined/overfull/underfull 均为 0，PASS。
- [x] 目标页面视觉：独立审阅第 5--7 页 → 曲线、置信区间、坐标和标签清晰，无裁切或重叠，PASS。
- [ ] 整稿末页版面：第 8 页仅有参考文献 [16]--[20]，右栏全空、页面约四分之三留白，Important。
- [ ] Fig.2 维度符号：权威图仍写 $\hat\gamma_{\mathrm{eff}}<13\,\mathrm{dB}$，正文写 $\hat\gamma_{\mathrm{eff,dB}}$，Important；按 D013 由图资产对话修正，论文主控不直接改图。

### 证据

```text
authoritative JSON:
projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed_snr5_25_step2.json
SHA256 AC1E0352B460C25B808A3333890481300EB9664F8695701BEB3B91A340E3CCC2
grid: 33 points; SNR = 5:2:25 dB; 30 paired seeds
self-check: mixed oracle violations = 0; common oracle violations = 0
independent recomputation: all paired means and Student-t CI95 match
tests: 22 passed

high-SNR independent check:
19--25 dB: 12 scenario-points; 11 CI95 intervals include zero
weak@23/25 dB: gain = 0 exactly
moderate@23/25 dB: -0.022/-0.002 dB; both CI95 include zero
strong@23/25 dB: -0.003/+0.016 dB; both CI95 include zero

final PDF:
projects/simulation/paper/ccisp2026/main.pdf
SHA256 580A5774FA7656950001884E907AAFCB7D08D1B35D10FAFD96A73E919D390747
size: 1002353 bytes; timestamp: 2026-07-15 16:22:52
pages: 8; bibitems: 20
LaTeX warning = 0; undefined = 0; overfull = 0; underfull = 0

independent verifier:
Critical = 0
Important = 2 (page-8 sparse layout; Fig.2 eff-SNR dB notation mismatch)
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

D013 的权威数据、正文数值和三张定量图可以交付。整篇最终投稿状态仍需两项闭环：图资产对话将 Fig.2 比较量改为与正文一致的 dB 域符号并联动重建；论文主控在不灌水、不伪造内容的前提下处理末页参考文献版式，再做一次 fresh build 与独立终验。

## V008: CCE-CC-003A 局部真实性与版面独立复核

> date: 2026-07-15
> 关联：S001 / D010

### 验证项

- [x] SNR 双坐标：逐处核对 Abstract/Introduction/Results/Conclusion → `1.3/1.2/1.9 dB` 为 strong-downlink/moderate-uplink/strong-uplink 的 data-symbol-SNR 差值，加入 `1.249 dB` 导频项后为 `2.5/2.4/3.1 dB`，且 `3.1 dB` 仅归属于 fixed NDA 对 fixed DA，PASS。
- [x] calibration 真相：核对 Method → CV 曲线来自 offline AWGN received-power characterization，`1.10` 为固定裕量，`13 dB` 来自 preliminary `12--14 dB` transition diagnostics；系数、裕量、floor 和阈值跨场景/Monte Carlo 冻结，无逐场景重调，PASS。
- [x] 门面降噪：确定性检索 Abstract/Introduction/Conclusion → 无 `26/29` recovery headline，无 Fig.5 的 `2.3/2.0/1.3 dB` selector headline，PASS。
- [x] 正文下限：fresh `texcount -sum -inc main.tex` → words-in-text `3526`，sum `3729`，8 组 displayed equations；纯正文超过 D001 的 3500 下限，PASS。
- [x] 构建与日志：fresh `latexmk -g -pdf -interaction=nonstopmode -halt-on-error main.tex` → 7 页，undefined `0`，overfull `0`，仅一处非阻断 underfull vbox，PASS。
- [x] 版面：Poppler 渲染 7/7 页并逐页检查，最终措辞调整后复查页 1/5 → 无裁切、重叠、乱码、异常换页或新增版式缺陷，PASS。
- [x] 独立审查：独立 verifier 复核两轮 → CCE-CC-003A 局部 PASS，新增 Critical/Important/Minor 均为 `0`；Results 中 26/29/Fig.5 既有语义阻断按 D010 留给专项裁定，整稿仍 PARTIAL。

### 证据

```text
texcount -sum -inc main.tex
  Words in text: 3526
  Sum count: 3729
  Number of math displayed: 8

latexmk -g -pdf -interaction=nonstopmode -halt-on-error main.tex
  Output written on main.pdf (7 pages, 976524 bytes).
  undefined references: 0
  overfull boxes: 0
  Underfull \vbox: 1

SHA256(main.pdf)
  C46BB0F3899007AB9B3981DE5D0816CAA0D545BE1F6C5B9A392D3B0CB86CFB16

deterministic stale-term checks
  Abstract/Introduction/Conclusion: 26/29 or 26-of-29 = 0
  Abstract/Introduction/Conclusion: Fig.5 2.3/2.0 selector headlines = 0
  all sections: pre-calibrated/holdout/optimized/sensitivity robustness = 0

independent verifier
  CCE-CC-003A local: PASS
  whole paper: PARTIAL (R004/Fig.5 and 26/29 semantics excluded by D010)
  new Critical/Important/Minor: 0/0/0
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

CCE-CC-003A 的授权范围内已 PASS；整稿不得据此宣称完成。下一步在独立专项中处理 R004/Fig.5 与 Results 中 26/29 的语义裁定，参考文献继续由用户指定的外部流程处理。

## V007: 当前论文论证链、专业性与实现真相终审

> date: 2026-07-14
> 关联：S001 / D004 / D006 / D007

### 验证项

- [x] 论证链：独立 reviewer 通读 Abstract→Introduction→System Model→Method→Results→Conclusion → 问题、互补性、两层选择、仿真与结论主链清楚，PASS；prior limitation→novelty 与 calibration→independent evaluation 两条边偏弱，PARTIAL。
- [x] 专业性与版面：fresh `latexmk` 确认当前 7 页 PDF up-to-date；逐页 PNG 审查 → 标题层级、公式、主体排版和外部语气达到会议稿水平，PASS；首页和方法段偏密、页 6/7 受浮动图/参考文献形成留白，参考文献流程按用户要求排除，PARTIAL。
- [x] 26/29：追踪当前 JSON 与 `switch_caliber_audit.py` → 该数由聚合 `SW` BER 更接近 NDA 还是 `DA_full` 反推分支，并使用 2% proximity rule；不是直接保存的 selector branch-decision accuracy。当前 “recovers the lower-data-BER fixed estimator” 声称强于证据，BLOCKED。
- [x] 1.3/1.2/1.9 dB 坐标：追踪 `fair_comparison.py`、30-seed JSON、上游 D004/R012 → total-energy fair 值为 2.509/2.443/3.101 dB；正文 1.3/1.2/1.9 dB 是减去 1.249 dB offset 后的 naive data-SNR gap。当前称其“在 total-energy coordinate / after applying offset”语义写反，BLOCKED。
- [x] Fig.5 metric signature：追踪 `_a4_switch_30seed_fixed.py` → selector 选 DA 时只统计 768 data-bit errors，选 NDA 时统计 1024 data-bit errors，随后统一除 1024。数值可复现，但 error population 不对称且 pilot positions 对 DA 隐式为零错误；正文改名为 full-block-normalized error ratio 尚未完整披露这一签名，BLOCKED。
- [x] Information access/state lifecycle：selector 仅用 raw power 与 nominal SNR；NDA transmitted-bit-assisted ambiguity evaluation、oracle 排除、湍流逐窗初始化均与代码一致，PASS。
- [x] 参数校准：CV 系数、1.10 margin 与 13 dB 只称 pre-calibrated，未给 calibration data/criterion/hold-out relationship；现有历史表明阈值来自同类 crossover/敏感性诊断，泛化证据不足，PARTIAL。
- [x] 图文一致性：Fig.5 caption 已改 full-block-normalized，当前图内纵轴仍为 `BER reduction relative to fixed NDA (dB)`，BLOCKED。

### 证据

```text
fresh latexmk: up-to-date; main.pdf 7 pages; SHA256=2AA137BCB0B5B297F1064D7F0C129E0BFF8603003138650E8FA574B5B18F5779
texcount -sum -inc: 3686; text=3484; displayed equations=8
log: undefined=0; overfull=0; underfull hbox=2

switch_caliber_audit.py:
  dist_nda = abs(sw-nda)/nda; dist_da = abs(sw-da_full)/da_full
  2% proximity / nearest aggregate curve -> inferred sw_choice
  output 26/29

fair_comparison.py:
  fair_gain = (s_da_d_needed + pilot_overhead_db) - gtot
30-seed JSON workregion_grand_mean_db:
  strong=2.508910; uplink_moderate=2.442983; uplink_strong=3.101257
R012/D004 naive values:
  2.509-1.249=1.260; 2.443-1.249=1.194; 3.101-1.249=1.852

_a4_switch_30seed_fixed.py:
  DA errors evaluated on is_d (768 bits); NDA on 1024 bits
  switch_ber_mean = e_s/1024

Fig.5 current embedded axis:
  BER reduction relative to fixed NDA (dB)
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

在不运行新仿真的边界内，先形成最小改稿合同：删除或收窄 26/29 直接 recovery 声称；纠正 1.3/1.2/1.9 dB 的坐标语义；明确 Fig.5 error population 或降低其系统收益解释；补参数校准来源/隔离边界；接收图线程的新 Fig.5 轴资产。未经用户批准不修改正文。

## V002: CCE-CC-002 Batch A 事实门

> 状态说明：本验证的总体 FAIL 已由 V003/D004 取代；保留原记录用于追踪漏读历史 D005/D006 的误判。

> date: 2026-07-14
> 关联：S001 / D003

### 验证项

- [x] 官方约束：子 Agent 访问 CCISP 官方投稿页 → 5–10 页、double-blind、官方模板 PASS；作者栏具体匿名操作未由页面确认。
- [x] 引用：逐条核对 11 处 unresolved citation 与本地全文/权威元数据 → 可用来源与必须删除的错误归因均已确定，PASS。
- [x] 公式：静态核对 `_channel.py`、`_recovery.py`、参数和 switching 脚本 → 8 组公式与实际实现一致，PASS。
- [x] 结果数字：逐字段核对 A4/main JSON 与生成脚本 → 26/29 EXCLUDED；1.9 dB 重归 NDA-vs-DA；switching BER 分母不公平，FAIL。

### 证据

```text
A4 fixed:
NDA errors / 1024 information bits
DA errors over 768 data bits; da_full = errors / 1024
SW when DA selected inherits data-only errors; switch = errors / 1024
Persistent summary JSON lacks per-block selections/errors required for a fair offline recomputation.

Other checks:
26/29: no persistent field
1.9 dB: NDA-vs-DA, strong-uplink work-region statistic
crossover generator: 18.0129 / 16.8661 / 10.7026 dB
fixed selector threshold: 13.0 dB
pilot total-energy offset: 1.249387 dB
```

### 结论

FAIL

### 后续（FAIL/PARTIAL 时）

停止 WRITE。用户需在“授权最小统一口径重评”与“重签无 switching 性能贡献的新定位合同”之间选择；不得沿用当前 Fig.3 指标继续扩写。

## V003: 历史 data-BER 口径与 26/29 确定性复核

> date: 2026-07-14
> 关联：S001 / D003 / D004

### 验证项

- [x] 历史最终决策：读取上游 D005/D006、S007、R008 和 topic-index 不变量 10 → data BER 为最终公平口径，A 路线资产直接复用且无需新实验。
- [x] 正文既定口径：读取 `W002-method-results.md` 脚注 → BER 默认按 768 data bits/block 计算。
- [x] 持久数据复算：读取 A4 fixed JSON 的 `nda_ber_mean`、`da_ber_mean_data`、`da_ber_mean_full`、`switch_ber_mean` → 26/29 可确定性重算。
- [x] 独立复核：由原 T009 verifier 在新上下文复审 → 确认 T009 漏读历史最终裁定，D003 应撤销且无需新仿真。

### 证据

```text
标准 BER 较优分支 = argmin(nda_ber_mean, da_ber_mean_data)
switch 实际偏向分支 = argmin(
  |switch_ber_mean - nda_ber_mean|,
  |switch_ber_mean - da_ber_mean_full|
)

AWGN: 8/8
Weak: 7/7
Moderate: 7/7
Strong: 4/7
Total: 26/29
Mismatch points: strong@15/20/22 dB
```

```text
上游 D005：data 口径才物理公平；full 口径给 DA 打 0.75 折。
上游 D006：回 A 路线，data 口径 26/29；写作资产直接复用，不需回 Step 4a 跑新实验。
W002 footnote：BER is computed over data symbols (768 bits per block) unless otherwise stated.
```

### 结论

PASS
## V004: 图题修改与投稿级专业性审计

> date: 2026-07-14
> 关联：S001 / D002 / D004 / D005

### 验证项

- [x] 五条图题：逐字 diff + 独立 reviewer + fresh build/render → 5/5 与批准文本一致，正文仍承载被压缩的实验定义，PASS。
- [x] 标题层级：独立审计 5 个一级标题和 8 个二级标题 → 层级/章节职责 PASS；两处 `Contract`、`Behavior`、大小写和泛化标题为 GAP。
- [x] NDA 信息可用性：源码追踪 `resolve_m16apsk_blockwise` 及 A4 调用 → 每 256 点用 `tx_bits` 在 8 个旋转中选最低 BER，BLOCKED。
- [x] BER 口径：历史 D005/D006、D004 与 A4 fixed 脚本交叉核对 → 26/29 使用 NDA/1024 与 DA/768 的 data BER；Fig. 5 的 2.3/2.0/1.3 dB 使用 SW/1024 full-block 归一化，当前正文混为同一口径，BLOCKED。
- [x] 相位连续性：生成器与循环调用追踪 → 湍流 selector 每 256 样本重新生成相位 realization，当前跨 DSP window 连续声称 BLOCKED。
- [x] PDF：MiKTeX `latexmk` fresh build + 7 页 PNG 目视检查 → 编译成功、undefined=0；第 7 页仅 3 条参考文献且大面积空白，布局 GAP。

### 证据

```text
caption verifier: 5/5 ExactMatch=True; fresh latexmk exit=0; undefined=0
PDF: 7 pages; SHA256=6CC4843D623FA9CA7E9DED3240981A86637B97B7F80DFB34ABE0138B35C1ECD4

common/_modulation.py:278-290,298-308
  resolve_m16apsk_blockwise(..., tx_bits, ...)
  eight rotations; choose minimum BER with transmitted bits

_a4_switch_30seed_fixed.py:170-178,207-214,237-263
  nda = e_n/1024; da_data = e_d/768; sw = e_s/1024
  switch_vs_nda = 10 log10(nda/sw)

common/_channel.py:18-37
  local k starts at zero; Wiener term uses a new cumsum per call
_a4_switch_30seed_fixed.py:188-206
  generate_shared_realization_apsk(Ns=256, seed=s0+b) inside block loop
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

五条短图题可以保留。标题层级可作为单独 L1 批次修改。整篇不得宣称投稿就绪；用户需在“按现有实现收窄/删除受影响声称”与“另开仿真修复范围”之间选择，之后再做全篇重编译和独立终审。
## V005: 非引用项真实性修复独立复核

> date: 2026-07-14
> 关联：S001 / D005 / D006

### 验证项

- [x] 标题、符号、窗口术语、Fig.2 引用、oracle 定义 → 独立 reviewer PASS。
- [x] 相位生命周期：正文限定为单窗连续、湍流窗间独立 → 与调用链一致，PASS。
- [x] Genie 信息：正文明确 transmitted-bit-assisted 八旋转仅用于 ambiguity-resolved BER evaluation，不进入 NDA statistic/selector → 与源码一致，PASS。
- [x] 指标签名：26/29 使用 NDA/1024 与 DA/768 data-BER；正文另定义 `R_FB`/`G_FB` 的 1024-bit full-block normalization → LaTeX 全链一致，PASS。
- [x] 构建和内容量：fresh `latexmk` exit 0；7 页；undefined/overfull=0；`texcount -inc -sum`=3677；8 displayed groups；技术三节 2637/3677=71.7%，PASS。
- [ ] Fig.5 图内纵轴：仍写 `BER reduction relative to fixed NDA (dB)`，与新 caption/正文的 full-block-normalized error ratio 冲突，BLOCKED。

### 证据

```text
fresh build: main.pdf, 7 pages, 974879 bytes
log: 0 undefined citation/reference; 0 overfull; 2 underfull hbox
texcount: sum=3677; displayed=8
stale-term scan: N_DFT / old Contract headings / cross-window continuity / G_BER / P_b,SW = 0

LaTeX:
results.tex:18    branch-specific data-BER denominators
results.tex:39-46 R_FB/G_FB full-block-normalized metric
method.tex:39     transmitted-bit-assisted ambiguity protocol
system_model.tex:16-29 within-window phase lifecycle

Remaining asset mismatch:
projects/simulation/figures/plot_fig3_gain.py:103
  BER reduction relative to fixed NDA (dB)
```

### 结论

PARTIAL

### 后续（FAIL/PARTIAL 时）

图线程将 Fig.5 纵轴改为 `Full-block-normalized error-ratio reduction relative to fixed NDA (dB)` 或等义分行短写，重建图资产后，论文主控重新编译并做独立终审。参考文献补充按用户要求不计入本验证失败项。

## V006: 双 Skill 实现真实性门禁验证

> date: 2026-07-14
> 关联：S001 / D007

### 验证项

- [x] 规则闭环：`paper-writing` 在 diagnosis/communication/verification 三层强制三联卡；`sim-preflight` 在 C4/write/T7 三层强制同一契约，PASS。
- [x] 证据链：两套 Skill 均要求 `paper line -> caller -> callee -> metric/state`，且禁止仅用 conclusions、JSON/meta 或静态公式替代运行路径，PASS。
- [x] RED 行为压力：blind+`tx_bits`、混合分母同名 BER、逐窗 new seed+跨窗连续三例均稳定 `BLOCKED`，PASS。
- [x] GREEN 行为压力：分别改为“盲估计主体+明确 post-hoc 标签辅助评估”、“分名并披露不同指标签名”、“仅单窗连续”后，对应局部门禁均 `PASS`，PASS。
- [x] 测试职责：自动测试明确标为结构契约测试，不冒充行为测试；独立 reviewer 对修正复核为 RESOLVED/PASS。
- [x] 新鲜验证：两套结构契约测试 PASS；两套 `quick_validate.py` 在 `PYTHONUTF8=1` 下均 `Skill is valid!`；`git diff --check` 无错误，PASS。

### 证据

```text
paper-writing/tests/test_truth_gate_docs.py
  TRUTH-GATE STRUCTURAL CONTRACT TEST: PASS (3 regression anchors)
sim-preflight/tests/test_truth_gate_docs.py
  TRUTH-GATE STRUCTURAL CONTRACT TEST: PASS (3 regression anchors)
quick_validate.py paper-writing: Skill is valid!
quick_validate.py sim-preflight: Skill is valid!
independent behavior pressure: 3 RED=BLOCKED; 3 narrowed GREEN=PASS
independent re-review: prior Important finding RESOLVED / PASS
```

### 结论

PASS
