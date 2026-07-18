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

## V016: 导师无意义段落、专业术语与符号清理终验

> date: 2026-07-16
> 关联：S001 / D020 / V015

### 验证项

- [x] 重复职责：独立 reviewer 对 `system_model.tex`、`method.tex` 逐段复核 → 公式逐项复述、CV/13 dB 流程重复和多段 no-retuning 说明已合并；必要的信息访问、状态生命周期和 ambiguity 边界保留，PASS。
- [x] 专业术语：确定性搜索 `DA-ML|NDA-ML|uplink|26/29` → 当前论文源与 Fig.3 生成脚本零命中；图例统一为 DA/NDA，PASS。
- [x] 符号：selected output 首次定义为 `SEL`，公式统一为 `x in {NDA,SEL}`；未定义 `SW` 零命中，PASS。
- [x] 数字与指标：1.50/1.05/0.83 dB、CI、990/990、144980/251020、768-bit common payload 和 df=29 未漂移，PASS。
- [x] 图与构建：Fig.3 从 formal-only 脚本重建；图例 DA/NDA；typography/Fig.2 tests `24 passed`；`texcount -sum -inc=3511`；fresh `latexmk` 7 页，undefined/overfull=0，PASS。
- [x] 视觉与外部输出：fresh 渲染 7 页逐页 QA；独立 reviewer 判无裁切、重叠或符号异常，external-output C1--C10 全 PASS。

### 证据

```text
pytest: 24 passed in 2.00s
latexmk: exit 0; main.pdf 7 pages
main.pdf SHA256: 4C1730B10BE71D6993354772D135AE86427ABA36F4748BCCEC5FEC7AD8E9DDBA
fresh render: tmp/pdfs/ccisp_cleanup_final/page-1.png ... page-7.png
independent reviewer: PASS; no simulation rerun required
```

### 结论

PASS

## V015: T018 三档下行正式全流程终验

> date: 2026-07-16
> 关联：S001 / D019 / R016 / T018

### 验证项

- [x] Gu/Al-Habash provenance 与六项偏差：PASS；最大 2.775%，冻结参数未改。
- [x] `params.py` / common 接口：PASS；三档现场哈希与三份正式结果 authority 一致。
- [x] fixed：870/870 cells PASS；AWGN 8 点、三档各 7 点、30×400 与逐方法分母完整。
- [x] A/B：990/990 exact PASS；selected complex output、errors、counts、realization、seed/window 边界零差异。
- [x] route B structural N/A：fixed-NDA/oracle/gain null/absent，零违规。
- [x] 统计：33 点 paired seed mean 与 df=29 95% t-CI 独立重算误差 ≤1e-12；DA/NDA=144980/251020。
- [x] 图：三脚本 formal-only、无 fallback；交叉点 14.644/17.334/16.194 dB；typography 19/19 PASS；Fig.2 未覆盖。
- [x] 论文：uplink/26-of-29/旧数字/内部代号零残留；`texcount=3656`；fresh build 7 页；undefined/overfull=0。
- [x] 视觉：逐页 7/7 检查，无裁切、重叠、空白页；Fig.2 最终尺寸无压字。
- [x] 独立 formal verifier：PASS；消歧前 label-free output 990/990 exact。
- [x] 独立论文 reviewer：D020 修正后 Fig.2 明确表达 `Branch command -> Branch router -> DA/NDA 单支 -> Selected theta -> Phase compensation -> Common downstream DSP`；与 route-B `decide()` 后 `if/else` 单支执行一致，PASS。

### 证据

`projects/simulation/results/ccisp_family1_independent_verification.json`；`ccisp_family1_formal_verification.json`；`ccisp_family1_fixed_verification.json`；`paper/ccisp2026/main.pdf` 与 `main.log`。

### 结论

PASS

### D020 解除记录

用户已授权主控修改 Fig.2。draw.io validator PASS；相关回归 `139 passed`；fresh PDF 7 页、undefined/overfull=0。独立 reviewer 逐页 1--7 检查 PASS；Fig.2 在 `0.88\textwidth` 下无压字、裁切或交叉误导。`main.pdf` SHA256=`9FF69EB079076D90235FE05A5A17E49AAEBC7FA6EFB5EDB4B7AAE50D123CEF0C`。

## V014: 参数证据门解除状态核验（D019）

> date: 2026-07-16
> 关联：S001 / D019 / R017 / V013

### 验证项

- [x] Al-Habash 2001 本地归档：`ls papers/doi/10.1117_1.1386641/` → `source.pdf`(185KB) + `content.md`(42KB) + `metadata.json` 均存在，PASS。
- [x] 公式可核：读 content.md 确认 Eq.13（GG 分布）、Eq.14（αβ-闪烁关系）、Eq.18-19（plane-wave 方差以 Rytov variance 表示）均存在，PASS。
- [x] Family-1 引用惯例：子 Agent 全文读 Gu 2022（*Appl. Sci.* 12(7):3331，卫星下行）确认采用三档 (11.6,10.1)/(4.0,1.9)/(4.2,1.4) + σ²_R=0.2/1.6/3.5，著作级引 Ghassemlooy CRC 2019 无表/页，PASS（惯例佐证）。
- [x] 数学复算一致性：精确映射值相对冻结四舍五入值的六项偏差最大 2.775% < 5%，闪烁指数有序（0.193/0.902/1.144），PASS。
- [x] D019 冻结值与 R016 复算、Gu 2022 实用值三方一致，PASS。

### 证据

```text
papers/doi/10.1117_1.1386641/: source.pdf(185KB 2026-07-15) + content.md(42KB) + metadata.json
Al-Habash Eq.13/14/18-19 confirmed in content.md (GG dist, alpha-beta relation, plane-wave variances)
Gu 2022 Appl.Sci.12(7):3331 verbatim: "with the parameters given in [19]" + values 11.6/10.1/0.2, 4/1.9/1.6, 4.2/1.4/3.5; [19]=Ghassemlooy CRC 2019 2nd ed., no table/page
exact-to-frozen relative deviations: 0.438%,0.221%,0.659%,0.551%,0.608%,2.775%; max 2.775% < 5%
sigma_I^2 = 0.193/0.902/1.144 (weak<mod<strong, each in Andrews regime)
Gu 2022 archived: papers/doi/10.3390_app12073331/{source.pdf,content.md,metadata.json}
Gu evidence: PDF p.4 Eq.(9)/content.md:106-112; PDF p.5/content.md:117; PDF p.11/content.md:268
```

### 结论

PASS（证据门按 D019 修订口径解除：Al-Habash 已闭合 + Family-1 按 Gu 2022 惯例等效闭合）

### 后续

T018 宏阶段一证据门解除。进入宏阶段二（改 params.py + 30-seed formal 重跑）前仍须遵守 D018 的 selector/CV/13 dB/seed/metric 冻结与 A/B exact 990/990 门；本验证只解除参数来源门，不解除运行真实性门。

## V013: T018 正式闭环参数证据门与 common 接口核验

> 状态说明：本验证的参数来源两项 FAIL（Al-Habash/Family-1 全文未落盘）已由 D019/V014 修订解除——Al-Habash 已归档闭合，Family-1 按领域惯例（Gu 2022 著作级引用 Ghassemlooy 2019）等效闭合。common 接口 97/97 PASS 仍有效。

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
## V017: Fig.3 fixed 5--35 dB unified-grid重跑与独立验证

> status: PASS
> date: 2026-07-16
> 关联：D021 / T018

### 验证范围

- `params.py` 新增 `CCISP_FIXED_SNR_DB=(5,7,...,35)`，fixed runner 从该字段读取；A/B adaptive 仍为 5--25 dB、2 dB、990 cells。
- 正式 fixed runner 退出码 0，`ccisp_family1_fixed_30seed.json` raw=1920（4 scenes × 16 SNR × 30 seeds），authority 两组网格完全一致，30 seeds × 400 windows 保持不变。
- 独立 `verify_fixed` 从 raw 记录重算并通过：`fixed_cells=1920`。
- Fig.3 四面板统一 `xlim=(5,35)`、固定网格采样步长 2 dB，四面板 BER 轴统一到 `10^{-6}`；零误码采用 half-count 可视化值，不写成精确零 BER。
- Fig.4 crossover 由新 fixed JSON 重算为 weak 14.470 dB、moderate 16.858 dB、strong 16.005 dB；正文更新为 14.5/16.9/16.0 dB。
- 相关 contract/typography tests：35 passed。

### 结论

PASS。该改动只扩展 fixed formal 网格与图轴统一性，不改变 selector/CV/1.10 margin/13 dB/CPR、A/B adaptive 网格、seed/window/metric 或冻结湍流参数。

### 证据

- `projects/simulation/results/ccisp_family1_fixed_30seed.json`
- `projects/simulation/results/ccisp_family1_fixed_30seed_verification.json`
- `projects/simulation/figures/ccisp_fig2_ber.pdf`
- `projects/simulation/figures/ccisp_fig4_crossover.pdf`
## V018: 用户微调 Fig.2 drawio 重导出与论文验收

> status: PASS
> date: 2026-07-16
> 关联：D020 / T018

### 验证范围

- 以用户当前 `projects/simulation/figures/fig2_adaptive_cpr.drawio` 为唯一编辑源，重新导出 PDF/PNG/SVG；未修改 drawio 内容。
- `test_fig2_two_layer_drawio.py` 与 `test_ccisp_figure_typography.py` 共 24 项通过。
- fresh `latexmk` build 输出 7 页；`main.log` undefined=0、overfull=0。
- PDF 第 3 页视觉检查通过：Fig.2 无裁切、重叠或字体退化，route-B 先选后跑语义保持闭合。

### 结论

PASS。当前用户微调已集成到论文资产和 fresh PDF。

## V019: Eq.(5)、图例与全文结果叙事终验

> status: PASS
> date: 2026-07-16
> 关联：用户反馈 / T018

### 验证范围

- Eq.(5) 拆为四行单一等号对齐，PDF 第4页居中、无挤压，公式含义未变。
- Fig.3--5 统一为 9pt、外置、横排、无边框图例；Fig.4 以颜色/marker 区分场景、实/虚线区分 DA/NDA，语义清晰。
- Results 重组为“实验角色—固定分支现象—交叉点—自适应指标—综合解释”，并从摘要、引言、结果、结论移除 verifier ledger 的 fingerprint、identity、990/396000、分支计数和 CI 端点罗列。
- 结论措辞收窄为“residual turbulence-limited BER over the evaluated SNR range”，不再声称渐近 error floor。
- fresh `latexmk` 输出 7 页；`main.log` undefined=0、overfull=0，仅有 1 处低风险 underfull hbox；独立 reviewer 对公式、图例、结果结构和证据边界逐项复核后确认上述项通过。
- `texcount -inc -sum main.tex` 当前总量超过 3500 词门槛；此前 40 项图形/契约测试通过，图资产与 Fig.2 用户微调均已在 V017/V018 验收。

### 结论

PASS。

## V028: 摘要/正文缩写首次定义与实际阅读顺序核验

> status: PASS
> date: 2026-07-17
> 关联：S003 续修 / V027 / 用户标题豁免

### 验证范围

- 标题中的 FSO 按用户要求不修改。
- 摘要内部：CPR、DA、NDA 在首次出现处展开；未在摘要使用 CV/SNR/BER/AWGN 缩写，因此不做多余括注。
- 正文实际阅读顺序：p1 引言首次定义 FSO、CPR、DA、NDA、APSK、DSP、SNR、BER、16APSK、CV、AWGN；这些定义均早于 p2 Fig.1 和 p3 Fig.2 的图内相应缩写。
- 后续 System Model、Method、Results 只使用已定义缩写，不重复展开。APSK 与 16APSK 分别指调制族和具体 16 阶格式，各自定义一次。
- fresh build 5 页；Fig.1 p2、Fig.2 p3；无 overfull、undefined citation/reference。测试 35 passed、1 known xfail；独立 acronym reviewer PASS。

### 最终哈希

```text
06D45979BB2FCED402DBE8CF23DC45052D645AF02A349DD4AE4E6FC63EF81A03  main.pdf
```

### 结论

PASS。

## V020: 首尾段落 benchmark 对标、压缩与终验

> status: PASS
> date: 2026-07-16
> 关联：用户反馈 / T018

### 验证范围

- 委托子 Agent 对 5 篇可比 coherent FSO/CPR 论文做全文结构对标：5/5 采用“场景—具体接收机困难—既有方案/互补性—本文方法与验证”；0/5 使用机械三项贡献清单；5/5 结论为单段并保留约 0--3 个代表数字。
- Introduction 重写为背景与问题、DA/NDA 互补性、本文 received-window 先选后跑方法、跨三档固定规则与评价安排、路线图；删除过载算法谱系、实现常数和内部验证治理；修正 Le Bidan 引用挂接范围。
- Conclusion 收束为方法、固定分支互补工作区、9 dB common-payload BER-ratio reduction 0.8--1.5 dB、随湍流增强而收窄及评估范围边界；不再声称 error floor 或宣传 evaluator。
- Results 删除 crossover 三点逐字转录、重复高 SNR 解释、第二处 paired-comparison；保留 metric 定义、公平性和一次 online/offline 信息访问边界。
- fresh `latexmk` 输出 6 页，undefined=0、overfull=0；逐页 PNG 检查无裁切、重叠或异常 float 空白。原第7页孤立参考文献通过将 Method 中泛化的 Martins 引用替换为直接支持 M-APSK NDA 构造的 Du 2025 而消除，保持 IEEE 默认参考文献字号，不以灌水填充。
- 图形/正式契约/Fig.2 测试 40 passed；确定性 stale-term 扫描未检出内部编号、旧 headline、error-floor 声称或重复 crossover 数字。

### 结论

PASS。

## V021: Introduction 引用恢复与 Fig.1/Fig.2 分页验收

> status: PASS
> date: 2026-07-16
> 关联：D023 / 用户反馈 / T018

### 验证范围

- Introduction 从约 312 词补至约 365 词，仍保持“场景—接收机困难—DA/NDA 互补性—本文方法—评价”结构；新增内容均绑定具体文献职责，不形成机械贡献清单。
- 恢复 6 条此前失去正文挂接的高质量/直接相关来源：Panasiewicz MWP、Wang TSP、Du JLT、Liu JLT、Liu TCOM、Qin TCCN；当前实际 bibliography 恢复为 24 条。Conroy uplink 与 Martins OSA Continuum 未作为优先来源恢复。
- Fig.1 与 Fig.2 通过显式分页分置于 PDF 第 2、3 页；独立 reviewer 确认两图完整、无裁切/重叠，Fig.2 尺寸可读。
- fresh `latexmk` 输出 7 页；`main.log` undefined=0、overfull=0，仅保留既有 underfull vbox；40 项图形/正式契约测试通过。
- 结果、参数、selector、指标和正式数据文件未改动；Wang 2025 的引用措辞收窄为 coherent-optical adaptive pilot DSP 先例，不再让非 FSO 文献替本文 FSO 动机背书。

### 结论

PASS。

> 2026-07-16 状态说明：本条关于 Fig.2 位于第 3 页的页码记录仅对应当时构建，已由 V023 的最新 fresh build 取代；Introduction 与引用恢复结论继续有效。

## V022: T019 Fig.1 A 版布局重构与最终独立验收

> status: PARTIAL
> date: 2026-07-16
> 关联：S002 / D022 / T019
> 说明：任务书原定从 V020 开始，但本专题已有 V020，且并行任务已新增 V021；为避免重复编号，本任务顺延为 V022。

### 验证项

- [x] 基线接收：启动时记录 Fig.1 drawio/PDF/PNG SHA-256、git status、XML 结构及 `main.tex:25` 的 `figure*`/`0.94\textwidth` 嵌入宽度。
- [x] 参考对标：从 `fig1-reference-previews` 选取 A1-03、A1-06、B1-06、A2-08，记录同角色、可迁移和不可迁移布局原则。
- [x] A/B 门控：balanced lanes 与 main-chain first 均在临时副本中以 IEEEtran `0.94\textwidth` harness 渲染，并由用户明确选择 A。
- [x] 语义独立审查：64 cells、全部标签、7 个 image assets、8 条 edge 的 ID/source/target/方向与基线一致；A 两轮复核均 PASS。
- [x] 结构与回归：权威 draw.io validator PASS；`test_ccisp_figure_typography.py` 全部 19 项 PASS。
- [x] 字体与尺寸：PDF 字体全部嵌入，仅 TimesNewRoman regular/italic/bold；无 Type 3、Helvetica、DejaVu Sans；PDF/PNG 均为 2.307692 比例，PNG 3000×1300。
- [x] 并发覆盖门：覆盖前三份权威文件的旧哈希与启动哈希逐项一致；未发现并行冲突后才覆盖 A 版。
- [ ] 严格视觉 PASS：独立视觉 reviewer 仍发现顶部 `amplitude factor`/`phase` 贴近 Composite FSO channel 顶边、`Detected bits` 贴近 demodulation 框，以及浅色缩略图的灰度风险。

### 证据

启动权威哈希：

```text
FCAE5092746A02E943AD54DF7690E88C535845AB1A211FD3A554246ED530E459  fig1_system_model_v5.drawio
CA97DEDAC5E59942C33C36B7012791D93EB6B40D8AF8E832467FB9ED62301350  fig1_system_model_v5.pdf
A0A7D0F464A480053D034024565D66D8114BE4FF308E428451972EBE5E728BC9  fig1_system_model_v5.png
```

最终权威哈希：

```text
31A11606418097A0515B50CEA34AE8A3BACC901F48CEFBF3A826D4F38203940B  fig1_system_model_v5.drawio
F7529B9B80954AFBB22A5E3907B950264B75133D6DA7D3C9A1EC76E66D470F7A  fig1_system_model_v5.pdf
F68660038F377838C494D6D09586F09D7FF544F07EFF58AA5A8FEB0824C14B16  fig1_system_model_v5.png
```

```text
validate_drawio.py: {"ok": true, "counts": {"cells": 64, "edges": 8}, "errors": [], "warnings": []}
pytest projects/simulation/tests/test_ccisp_figure_typography.py: 19 passed
pdffonts: TimesNewRomanPSMT / TimesNewRomanPS-ItalicMT / TimesNewRomanPS-BoldMT; emb=yes; no Type 3/Helvetica/DejaVu Sans
semantic diff: ids_equal=true, labels_equal=true, edges_equal=true, assets_equal=true, cells=64, edges=8, assets=7
PDF/PNG geometry: pdf_ratio=2.307692, png_px=(3000,1300), png_ratio=2.307692
```

独立视觉 reviewer 第 2 轮：主链 4.4/5、拥挤度明显改善、底部支持带无重叠；残余为顶部标签贴边、Detected bits 贴角和灰度风险，结论 PARTIAL。

### 结论

PARTIAL。

### 后续（PARTIAL）

本任务已达到两轮精修上限，按任务书停止继续堆补丁。若要达到严格视觉 PASS，应另行明确是否允许改变顶部边标签的语义承载方式或进一步调整灰度对比；本轮不再扩大范围。

## V023: 第一、二节空白修复与图分页终验

> status: PASS
> date: 2026-07-16
> 关联：用户排版反馈 / V021

### 验证范围

- 根因定位为 `main.tex` 中为分隔 Fig.1/Fig.2 引入的强制分页：它提前截断正文流，造成 Introduction 与 System Model 之间以及后续页面的非自然空白。
- 最终版删除强制分页，保持 Fig.2 在 `system_model` 之后自然浮动；未修改正文科学内容、结果、参数或图资产。
- fresh `latexmk` 输出 7 页；`main.log` undefined=0、overfull=0、underfull=0。
- 独立视觉 reviewer 对最新 `main.pdf`（982092 bytes）复核：p1 Introduction 后由 Section II 在右栏自然承接；p3 两栏由正文与公式正常填充；Fig.1 位于 p2、Fig.2 位于 p4，二者未同页，均无裁切、重叠或明显版式缺陷。
- 图形/正式契约/Fig.2 回归测试 40 passed。

### 结论

PASS。

## V024: 用户微调 Fig.1 重导出与全文嵌入验收

> status: PASS
> date: 2026-07-16
> 关联：S002 / T019 / 用户重导出指令

### 验证范围

- 以用户最新 `fig1_system_model_v5.drawio` 为权威编辑源；保留其布局调整，只修复手动编辑导致的 `e_bits_mapper` source 脱绑，并将 `Information bits` 文字框左移 15 个 draw.io 单位以满足最终尺寸安全间距。
- draw.io validator PASS：63 cells、8 edges，所有语义边均具有效 source/target，无悬空端点。
- 从同一 drawio 导出 1080×468 pt 矢量 PDF，并生成 3000×1300 PNG；PDF 字体仅含嵌入的 Times New Roman regular/italic/bold，无 Type 3、Helvetica 或 DejaVu Sans。
- fresh `latexmk` 输出 7 页，最新 Fig.1 已嵌入 p2；`main.log` undefined=0、overfull=0、underfull=0。
- 本地主图 typography 回归 19 passed；独立 reviewer 的图形/资产契约复核 25 passed，并确认 p2 最终尺寸无裁切、重叠、错误接线或严重贴边。

### 最终哈希

```text
4E9794B5ADA8EDC292C4F1A9AFB618E92A8E971492CEEC5B662AA982D990FC77  fig1_system_model_v5.drawio
6C95F9585C4A4E0D902EE95D757F80BB60A3D3488FB311F6F71D99C12B1B7CEF  fig1_system_model_v5.pdf
2F7E0796893ABB1F85E170EC78BDFB0FCB139B4B7F56A03CCC93BB8C23EC2FA5  fig1_system_model_v5.png
391C261169069F5A348B72FF7652E22B4E8AD70D3FA582E6044E2CD651B5F648  main.pdf
```

### 结论

PASS。

> 2026-07-16 状态纠正：本条包含主控未经授权加入的两处 drawio 修补，已由 V025 撤销并取代；不得再把 V024 哈希视为当前权威资产。

## V025: 用户指定 Fig.1 drawio 原样恢复与重导

> status: PARTIAL
> date: 2026-07-16
> 关联：S002 / 用户路径纠正 / supersedes V024 当前资产状态

### 验证范围

- 权威输入确认是 `D:\code\study\research-protocol\projects\simulation\figures\fig1_system_model_v5.drawio`；用户保存时哈希为 `CBD59FF2509D8168BD81C55B5E15D3CEFC9305952E1AB99284B93CBE7111FCB0`。
- 主控撤销其后自行加入的 `e_bits_mapper` source 绑定与 `Information bits` 左移，恢复到上述用户哈希；未使用 `.bkp`、旧 PDF 或其他 drawio 作为输入。
- 从恢复后的用户原文件重导 PDF/PNG，并 fresh build 全文 7 页；LaTeX 构建成功，undefined/overfull/underfull=0。
- 忠实重导 PASS，但原始 drawio 自身的结构/安全间距门仍为 PARTIAL：validator 报 `e_bits_mapper` 缺 source；typography 回归 18 passed、1 failed（`Information bits` 与 mapper 标题的水平安全间距 0.32 pt，小于 3.0 pt 门）。按用户要求不再擅自修改源图。

### 当前哈希

```text
CBD59FF2509D8168BD81C55B5E15D3CEFC9305952E1AB99284B93CBE7111FCB0  fig1_system_model_v5.drawio
14423F4363A0AD13AAA2EF0E261A41DF08D9BF7EB080E75AF38C3092AF32BB9D  fig1_system_model_v5.pdf
806DD7F7D6FE513E2F8E7A99376665130327BC94E325D63506544640AF32CF09  fig1_system_model_v5.png
DDAE062F09CC434FC3819620A038FADC71FB7B81628D01DC7F84935D9392E427  main.pdf
```

### 结论

PARTIAL：用户指定版本已原样恢复并完成重导；结构与安全间距问题如实保留，未再越权修补。

## V026: 导师批注驱动 Skill 升级与 CCISP 五页全文终验

> status: PASS
> date: 2026-07-17
> 关联：S003 / D024 / D019 / T018

### 验证范围

- `paper-writing` 与 `external-output` 完成 RED/GREEN 压力测试和导师反馈门禁升级：证据账本、逐条 disposition、全文同类扫描、图文/缩写/作者元数据、精确页面与独立 reviewer 均有可执行门。
- 论文 21 项反馈账本全部核销：算法中心标题、作者信息、引言合并与 remainder、相关工作分析、DA/NDA 类别定义、随机变量和 CV 解释、划线/灌水句删除、Fig.3 单轴、Fig.3--5 图内图例、HD-FEC/uplink/26-of-29 清除、Fig.4 三交点解释、AWGN 首次展开、会议引用为零、公式(5)与逐页版式均 PASS。
- 当前 `params.py`、formal A、formal B 和 fixed 结果的权威签名一致：`fac6d229ebfb18a26fc5898579ffd4671e463be524ec73ec06ee02e0d2e8dc3c`。A/B 各 990 cells exact；route B 不存在的 fixed-NDA/oracle/gain 字段均为 null；formal verifier PASS。
- Fig.3 横轴 5--35 dB，2 dB 间隔的 16 个主刻度均可提取，`AWGN` 专业缩写正确，无标签重叠。
- fresh build 为 5 页；末页最深文本 y=713.219 pt，距同模板最后正文带 5.63 pt，小于一个正文基线，属于最后允许行带；双栏底线差约一个参考文献基线。无 overfull、undefined citation/reference。
- 回归：37 passed、1 xfailed；xfail 为用户 Fig.1 原资产已知 0.32 pt 安全间距债务，不影响本轮论文终验。

### 最终哈希

```text
D5EC13FE9A57510DAB161C744B9F67923383FD0270399F57FF8E0F32E5F86C23  main.pdf
FAC6D229EBFB18A26FC5898579FFD4671E463BE524EC73EC06EE02E0D2E8DC3C  params.py
```

### 结论

PASS。科学 authority、导师批注、Skill 门禁、图表、文字、精确五页和独立终验全部闭环。

## V027: Fig.2 第三页页位与 Transactions/专业性回归

> status: PASS
> date: 2026-07-17
> 关联：S003 续修 / D024 / V026

### 验证范围

- PDF 实际引用仍为 18 条；IEEE Transactions on Communications、IEEE Transactions on Information Theory、IEEE Transactions on Signal Processing 均保留，conference=0。
- 对当前 `main.tex` 做 fresh clean build，输出 5 页；Fig.1 caption 在 p2，Fig.2 caption 在 p3 顶部，Fig.3/4 在 p4，Fig.5 与参考文献在 p5。
- Fig.2 页位修复没有提前浮动块到 p2，也没有扩成 6 页；仅等义压缩 System Model 两处重复性分区描述，并保持图资产、实验参数、结果、方法逻辑不变。
- `main.log` 无 overfull、undefined citation/reference；测试 35 passed、1 known xfail。专业性确定性扫描中 `HD-FEC`、`26/29`、`uplink`、`estimator selection` 均无正文命中，Transactions 条目可由 `main.bbl` 逐项核对。
- 独立视觉核验：p3 顶部 Fig.2 无裁切/重叠，p1/p2/p4/p5 无异常空白或公式挤边，5 页与末页约束无回归。

### 结论

PASS。
