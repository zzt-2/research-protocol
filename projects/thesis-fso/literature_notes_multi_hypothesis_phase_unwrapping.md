# Literature Notes — bounded multi-hypothesis phase unwrapping

> Owner: `.sessions/2026-08-12-multi-hypothesis-phase-unwrapping/`
> Groundwork status: Step 3.5 complete/verified; terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION` (cheap absorption); Step 4a forbidden.

## Progress

| Step | Status | Evidence |
|---|---|---|
| 1 search | COMPLETE / VERIFIED | R001–R003；V001 PASS |
| 2 acquire | COMPLETE / ACCEPTED | R004；V002 PASS；9 qualified/8 CORE |
| 3 read | COMPLETE / VERIFIED | 本文件；R005；V003；9/9 fulltext read |
| 3.5 supplement | COMPLETE / VERIFIED | D006/R006–R007/V004；terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION` |
| 4a+ | FORBIDDEN | Q001 prior-art gate failed |

## Corpus 与 title gate

| L# / C# | Identity | source/provenance | title gate | role |
|---|---|---|---|---|
| L01/C01 | Wang et al., TSP 2022, `10.1109/TSP.2021.3137966` | shared publisher PDF/content | PASS，正文 :5 | reference M / published defect |
| L02/C09 | Wang et al., IEEE Access 2019, `10.1109/ACCESS.2019.2934224` | worktree IEEE PDF/content；公式回看 PDF | PASS，正文 :3–9 | CSSC hard threshold cheap alternative |
| L03/C14 | Fu–Kam, TIT 2013, `10.1109/TIT.2013.2238604` | worktree IEEE PDF/content | PASS，正文 :1–13 | strongest simple unwrap ancestor |
| L04/C02 | Shayovitz–Raphaeli, TCOM 2016, `10.1109/TCOMM.2015.2506553` | arXiv 1306.3693 source TeX/content；formal identity closed | PASS，`final.tex:37–50` | full mixture / fixed-order mandatory comparator |
| L05/C05 | Fang et al., Nat Commun 2024, `10.1038/s41467-024-50439-1` | worktree OA PDF/content；公式回看 PDF | PASS，正文 :7 | transmitter-assisted system alternative |
| L06/C08 | Paillier et al., JLT 2020, `10.1109/JLT.2020.3003561` | arXiv TeX in DOI slot；formal identity closed | PASS，`bare_jrnl.tex` title | FSO AGC+DPLL cheap baseline |
| L07/C10 | Sharma–Krishnamurthy, Sci Rep 2021, `10.1038/s41598-020-80822-z` | worktree OA PDF/content；公式回看 PDF | PASS，正文 :5 | reduced-rate fixed-lag KF near comparator |
| L08/C11 | Panasiewicz et al., Photonics 2023, `10.3390/photonics10121312` | shared publisher HTML；正文从 :189 起 | PASS，正文 :189 | FSO atan2-OPLL cheap baseline |
| L09/C12 | Hu et al., Electronics 2025, `10.3390/electronics14020265` | shared OA PDF/content | PASS，正文 :5 | recent optical hybrid CPR comparator |

## L01/C01 — Wang TSP 2022 reference

### 标准字段（14+）

| 字段 | 提取 |
|---|---|
| 作者/年份/渠道 | Qian Wang, Zhi Quan, Suzhi Bi, Pooi-Yuen Kam；IEEE TSP 70, 2022, 337–349（content :1–19） |
| DOI/源 | `10.1109/TSP.2021.3137966`；shared `papers/doi/10.1109_tsp.2021.3137966/content.md` |
| 研究问题 | AWGN+Wiener PN 下联合估计 single-tone frequency、initial phase、random phase vector（:25–43） |
| 方法 | amplitude-informed AOPN + closed-form ML/MAP + Schur/five-statistic recursion；前置 Fu–Kam single-path unwrap（:95–213,331–357） |
| 创新定位 | joint ML/MAP、bounds、recursive implementation；unwrap 是复用 primitive，不是其新贡献 |
| 输入/输出 | `|r(k)|,arg r(k)` → one unwrapped sequence + `ω̂,φ̂,θ̂` |
| 信息边界 | receiver-only、decoder-free、无 pilot/future/truth；仿真后验识别 failure 不可作 deployable trigger |
| 状态生命周期 | H=1、lag=0、greedy commit；无 reset/fallback；错误增量污染后续 suffix |
| baseline | LMMSE-WPA、improved Kay、pure-AWGN ML、CRLB/BCRLB（:359–385,481–507） |
| 复杂度 | frequency/phase recursion O(1)/sample、O(N) total；phase-vector matrix cost/memory未量化 |
| 实验 | `10^5` Monte Carlo/point；扫 SNR/N/PN/CFO/phase/amplitude；无 CI/seeds |
| 关键结论 | 高 SNR 达 bounds；pure-AWGN estimator 在较大 PN 下损失；failure runs 被排除 |
| 限制 | single-tone synthetic；小参数后报告主曲线；无 FSO/turbulence/BER/hardware |
| 开源 | 未报告 |
| 本专题角色 | `REFERENCE_M`；published suffix-pollution defect source |

### 七子表

| 子表 | 结果 |
|---|---|
| 研究对象/假设 | `r(k)=A exp(j(ωk+φ+θ(k)))+n(k)`；Wiener increments、Gaussian AOPN approximation；相邻真实 phase increment需落在唯一 principal branch |
| 输入/输出 | complex samples → single unwrap + frequency/phase/PN estimates |
| 算法步骤 | adjacent product principal phase → cumulative center → unique ±2π adjustment → joint ML/MAP → recursive statistics |
| 信息边界 | receiver-only；无 decoder/pilot/truth/future；failure discard只属评分 |
| 状态生命周期 | H=1、immediate commit、no rollback/reset |
| baseline/复杂度 | WPA/Kay/AWGN-ML/bounds；O(1) per new sample for `ω̂,φ̂` |
| 实验/限制 | `10^5` trials；synthetic only；failure exclusion masks reliability defect；ML/DRL fields=N/A（确定性 estimator） |

### Exact action/complexity contract

`input=raw complex single tone; state={ω,φ,Wiener θ,one cumulative unwrap}; H=1; score=no branch score; merge/prune=N/A; lag=0; commit=greedy irrevocable; trigger/fallback/reset=none; causal=yes; output=unwrapped sequence+ω̂/φ̂/θ̂; cost=O(1)/sample for core recursion; memory/phase-vector cost not fully reported; decoder-free=yes; task-match=exact model primitive, FSO transfer model-level.`

### Problem extraction

`M=C01 single-path Fu–Kam unwrap→joint ML/MAP；C=residual CFO+Wiener laser PN+AWGN 下需固定资源实时估计；A=每个 adjacent principal increment 都有唯一正确 branch 且错误不会累积。` 正文 :343–357 与 :423–451 明确 breach 会传播、较大 `ω/N/σp²` 时丢弃 failure run。

## L02/C09 — CSSC-CPE 2019

### 标准字段（14+）

| 字段 | 提取 |
|---|---|
| 作者/年份/渠道 | Ye Wang et al.；IEEE Access 7, 2019, 110451–110460（content :3–19） |
| DOI/源 | `10.1109/ACCESS.2019.2934224`；IEEE PDF，公式核 PDF pp.3–5 |
| 问题 | VVPE/PU 在 QPSK coherent WOC 中产生持续 `±π/2` cycle slip |
| 方法 | 两个 L-symbol cumulative-average segment 的差 `δ[k]`；双阈值定位方向并对 suffix 硬校正（:89–131） |
| 创新定位 | NDA、无差分编码；解析 `δ` PDF/threshold，抗弱 turbulence/noise |
| I/O | VVPE full-range phase → ternary slip decision + corrected phase/symbol stream |
| 信息边界 | receiver-only、decoder-free；评估中的 SER oracle window 不可进入算法 |
| 生命周期 | single track + buffered detector + persistent quadrant-offset correction；无 parallel hypotheses |
| baseline | CS-DC、uncorrected CPE |
| 复杂度 | rolling sums可O(1)/symbol、memory O(N+L)；论文只给 discriminant ops，未给 end-to-end latency |
| 实验 | 100M symbols、2 GBaud；`3×10^8` MC核 PDF；室内 4 Gbps experiment |
| 关键结论 | 低两数量级；对 CS-DC SNR门降低0.6 dB；有限样本“zero slip” |
| 限制 | QPSK、weak turbulence、model-derived threshold、无 multi-hypothesis/strong turbulence |
| 开源 | 未报告 |
| 角色 | strongest hard-trigger/suffix-correction cheap alternative |

### 七子表

| 子表 | 结果 |
|---|---|
| 对象/假设 | coherent WOC QPSK；weak lognormal/phase turbulence+laser Wiener PN+AWGN；CFO已校 |
| 输入/输出 | VVPE unwrapped phase → corrected phase/symbol |
| 算法 | VVPE→cumulative average→two-segment difference→threshold/sign→suffix ±π/2 correction |
| 信息边界 | no data/decoder/truth；`P_CS|CPE=10^-3`用于 threshold prior |
| 生命周期 | hard noCS/CS+/CS−；centered buffer；persistent offset state |
| baseline/复杂度 | CS-DC；O(1) rolling update/O(N+L) buffer，exact total cost not reported |
| 实验/限制 | simulation+lab，large samples但无 CI/seeds；ML fields=N/A |

### Exact contract / M-C-A

`input=QPSK CPE phase; state=single phase+quadrant offset; H=hard 3-class not trajectories; score=δ; merge/prune=N/A; lag≈centered 2L+N−1 window; trigger=|δ|>threshold; fallback=no-op only; output=corrected suffix; decoder-free=yes; single-tone=no.`

`M=VVPE+single-path PU/CS-DC；C=weak-turbulence coherent WOC；A=PU/slip discriminant remains reliable under turbulence.` 四判据：1/2/4 PASS；3 需由 C01/C10–C12 近期 baseline 补足。

## L03/C14 — Fu–Kam improved unwrap 2013

### 标准字段与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Fu & Kam；IEEE TIT 59(5), 2013；`10.1109/TIT.2013.2238604`；publisher PDF/content |
| 问题 | 任意 SNR AOPN建模；旧 recursive unwrap依赖可靠初始 `ω̂,φ̂`（:17–31,280–328） |
| 方法/创新 | exact/prior Tikhonov AOPN、LMMSE/LMV/WPA；adjacent-difference cumulative-center improved unwrap |
| I/O | raw complex samples/magnitude → one unwrapped sequence + frequency/phase estimate |
| 信息边界/生命周期 | receiver-only、H=1、lag0、causal、no decoder/pilot/truth、no rollback/reset |
| baseline/complexity | old recursive Algorithm2、AOPN models、WPA；unwrap O(1)/sample is implementation inference，paper不报E2E cost |
| 实验/结论 | simulation-only；best-linearized约1 dB threshold gain，Algorithm1优于Algorithm2（:438–475） |
| 限制/开源 | AWGN only，无 PN/FSO/hardware；无 seeds/CI；无代码 |
| ML 7-subtable fields | state/action/reward/network=N/A（确定性 estimator）；对象、I/O、算法、信息边界、生命周期、baseline/complexity、experiment/limits均如上 |
| 角色 | strongest simple H=1 baseline / C01 ancestor |

### Exact contract / M-C-A

`input=raw complex single tone; state=one cumulative center; H=1; score/merge/prune=N/A; lag0 immediate commit; no trigger/fallback/reset; causal; output=single unwrap+ω̂/φ̂; O(1)/sample inferred; decoder-free/single-tone=yes.`

`M=high-SNR AOPN+recursive unwrap；C=mid/low-SNR single-tone AWGN；A=approximation+initialization可靠。` 判据1/2/4 PASS，判据3因2013身份单独不够，故仅 ancestor/comparator。

## L04/C02 — Tikhonov mixture tracker 2016

### 标准字段（14+）

| 字段 | 提取 |
|---|---|
| 作者/身份 | Shachar Shayovitz, Dan Raphaeli；IEEE TCOM 64(1), 2016；DOI `10.1109/TCOMM.2015.2506553`；arXiv 1306.3693 |
| 问题 | exact phase SPA/DP complexity；single-Tikhonov BARB in unreliable decoder-soft regime slips/errors |
| 方法 | Tikhonov-mixture forward/backward SPA；KL threshold+CMVM merge；limited order L；retained-mass confidence `φ`+pilot recovery（content :126–138,221–323） |
| 创新定位 | adaptive mixture reduction with KL bound、limited-order tracker、trajectory/PLL interpretation |
| I/O | received coded MPSK+pilots+decoder soft → phase mixtures internally, symbol LLR externally |
| 信息边界 | decoder soft and future/backward observations required for formal output；no truth/CFO/FSO state |
| lifecycle | per-symbol M-way expansion→likelihood score→KL merge→cap/prune→`φ` update→pilot recovery→bidirectional fusion |
| baseline | DP grid BCJR、BARB、unlimited、limited L=1/2/3、selection-only L=3 |
| complexity | limited mixture `O(Mγ²)` per symbol/iteration；8PSK order3 312→238 MUL over iterations vs DP 68360（:352–367,424–433） |
| experiment | LDPC 4608/rate.89；B/Q/8/32PSK；Wiener PN 0.01/0.05/0.1 rad/sym；pilots |
| conclusion | L=2/3 near unlimited/DP on tested coded-MPSK; L=1 sometimes recovers via pilots |
| limitations | decoder/pilot dependence、block forward/backward、no fixed lag/CFO/unwrap output/FSO；no seeds/CI/runtime/memory |
| code | not stated |
| role | mandatory full-general mechanism comparator / task-contract strong neighbor |
| title gate | source TeX exact title PASS |

### 七子表

| 子表 | 结果 |
|---|---|
| 对象/假设 | coded MPSK AWGN+Wiener PN，periodic pilots，decoder soft independence approximation |
| I/O | samples+soft symbols+pilots → mixtures/LLRs |
| 算法 | M-way expand→Tikhonov likelihood→KL cluster→CMVM→limited cap/φ→pilot uniform blend→fwd/bwd fusion |
| 信息边界 | decoder/future dependent；no residual CFO/truth |
| 生命周期 | circular uniform init；variable/fixed order；pilot re-acquisition；no lag commit |
| baseline/complexity | DP/BARB/order1–3；exact MUL/LUT formulas |
| 实验/限制 | multi-MPSK synthetic；strong parameter sweeps, weak statistics；ML fields=N/A |

### Exact contract / collision

`input=coded MPSK+pilots+LDPC soft; state=circular phase posterior; hypotheses=Tikhonov components, adaptive or L=1/2/3; score=α·P_d·I0 likelihood; merge=KL≤ε+CMVM; prune=hard L with φ; lag/commit=none, formal output block fwd/bwd; trigger=pilot arrival; fallback=φ-weighted uniform reseed; output=LLR; cost=O(ML²)/symbol/iteration; decoder-free=no; single-tone=no.`

裁决：在“多轨迹+fixed order+likelihood+merge/prune+confidence”能力轴是 `FULL_GENERAL_SUPERSET`；在 Q001 完整任务合同（decoder-free single-tone、integer wrap、fixed lag/commit、fixed memory/worst latency、unwrapped-sequence output）上是 `STRONG_NEIGHBOR`，不是 exact collision，也不是 task-contract full superset。D1 若只说“三假设低复杂度 tracking”即为缩水版；只有完整合同可区分。

## L05/C05 — residual-carrier modulation 2024

### 标准字段与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Fang et al., Nat Commun 15:6339, 2024；`10.1038/s41467-024-50439-1`；OA PDF/content |
| 问题 | MHz linewidth下 time-domain pilots overhead且外推失效 |
| 方法/创新 | transmitter residual optical carrier + common downconversion + LPF extraction + digital beating，抵消共模 laser PN（content :89–124；PDF p.4 Eq.1） |
| I/O | payload+Tx carrier → derotated symbols；需要 Tx bias/guard band |
| 信息边界/生命周期 | stronger-than-receiver-only carrier observable；single CFO/carrier phasor；no hypotheses/reset |
| baseline/complexity | time-domain/RF pilot+BPS；无 ops/memory/latency，需 system overhead |
| experiment/conclusion | 45 GBaud PS-256-QAM、80 km、3 MHz；net GMI 8.39→11.85，TP净速率+41.2% |
| limits/open | fiber/offline、不同信息预算、无 FSO；Zenodo data，code on request |
| ML fields | N/A；确定性 transceiver/DSP |
| role | system-level alternative；receiver-only contract下 neighbor，不作 exact comparator |

### Exact contract / M-C-A

`input=payload+Tx residual carrier; state=one CFO/carrier phasor; H=1; score=spectrum peak; no merge/prune/trigger/reset; output=derotated symbols; latency/resources unreported; decoder-free=yes but transmitter-assisted; single-tone=no.` 自身 M-C-A 四判据 4/4，但不证明 Q001；若允许改 Tx，它从系统层旁路 D1/D2 动机。

## L06/C08 — space-ground AGC+DPLL 2020

### 标准字段与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Paillier et al., IEEE JLT 2020；`10.1109/JLT.2020.3003561`；arXiv TeX in DOI slot |
| 问题 | AO residual scintillation changes PLL detector gain under residual CFO |
| 方法 | AGC target power 1 + second-order digital PLL/MAP-like BPSK detector（content :116–157） |
| I/O | symbol-rate BPSK I/Q → locked samples/bits |
| 信息边界/lifecycle | receiver-only causal；single amplitude+NCO phase/frequency state；capture→tracking；no hypotheses/reset |
| baseline/complexity | theoretical phase bound/ideal AWGN only；O(1) state/ops，exact count not reported；1.4 ms acquisition |
| experiment | 10 GBaud DBPSK、1550 nm、100 MHz residual CFO、2 s TURANDOT AO traces |
| conclusion | critical SNR≈−9 dB；turbulence phase minor，fading BER penalty 2.3 dB at 1e−4 |
| limitation | timing ideal、coarse CFO out of scope、laser PN not primary、simulation only/no CI |
| role | FSO cheap DPLL baseline/neighbor |
| ML fields | N/A |

### Exact contract / M-C-A

`input=BPSK I/Q; state=AGC+single NCO phase/frequency; H=1; score=sI*sQ; lag=causal loop; no trigger/fallback/merge; output=bits; O(1), acquisition 1.4ms; decoder-free CPR=yes; single-tone=no.` 自身判据1/2/4 PASS、3不足；对 D1 neighbor，对 D2 near cheap absorption。

## L07/C10 — reduced-rate Kalman 2021

### 标准字段（14+）与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Sharma & Krishnamurthy, Sci Rep 11:1991, 2021；`10.1038/s41598-020-80822-z`；OA PDF/content |
| 问题 | per-symbol KF在高-rate coherent link成本高 |
| 方法 | 1-state phase / 2-state phase+CFO KF every m symbols；endpoint interpolation；innovation-adaptive Q（content :39–103；PDF pp.3–4） |
| I/O | equalized PDM-16QAM+20 pilots/DD → phase/CFO-corrected symbols |
| 信息边界 | receiver-only、no decoder；intermediate samples use future endpoint，fixed m buffer |
| lifecycle | pilots init→DD；single Gaussian trajectory；adaptive Q；no slip recovery/reset |
| baseline | symbol-rate KF、QPSK partition、block KF、fixed/adaptive Q |
| complexity | 1-state 13RA+12RM+1LUT/update；2-state 66RA+97RM+2LUT；N/m updates；O(m) buffer |
| experiment | 200 Gbps PDM-16QAM、12×80 km、linewidth 100k–1M、CFO100M–1.2G |
| conclusion | m creates Q/complexity tradeoff；large CFO requires m=1；adaptive Q improves dynamic tracking |
| limitation | fiber、single path、no cycle-slip recovery/hardware/seeds/CI；block-KF comparison conditions differ |
| code | not stated |
| role | near comparator for fixed lag and reliability adaptation |
| ML fields | N/A |
| title/identity | PASS，content :5 |

### Exact contract / M-C-A

`input=16QAM+pilots/DD; state=1D phase or 2D [phase,CFO]; H=1 Gaussian; score=innovation; no merge/prune; lag≈m due endpoint interpolation; trigger=DA→DD; adaptive Q from innovation; no fallback/reset; output=corrected symbols; exact RA/RM/LUT; decoder-free wrt FEC; single-tone=no.` 自身四判据4/4。对 D1占据 fixed-lag/resource tradeoff但不占 discrete wrap hypotheses；对 D2占据 receiver-visible adaptation primitive。

## L08/C11 — atan2 all-digital OPLL 2023

### 标准字段与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Panasiewicz et al., Photonics 10:1312, 2023；`10.3390/photonics10121312`；publisher content正文 :189+ |
| 问题 | sine/fourth-power detector gain随 fading amplitude变化且长反馈延迟下失锁 |
| 方法 | QPSK fourth power→MAF→atan2/4 amplitude-independent phase error→loop filter/VCO（:607–680） |
| I/O | receiver I/Q → VCO control/recovered data |
| 信息边界/lifecycle | receiver-only causal FIR+feedback；single loop state；no pilot/decoder/hypothesis/reset |
| baseline/complexity | sine detector；O(L) buffer；明确30/35ns feedback delay，ops未报 |
| experiment/conclusion | VPI+Python 20Gbps LEO downlink；atan2在 fades/30–35ns保持lock，10G sample STD±6.5kHz |
| limitation | turbulence只建power、无 atmospheric phase/CFO主张；co-sim、短μs、30 events无CI |
| open/ML | code not reported；ML fields=N/A |
| role | strongest cheap absorption against vague D2 fade-reliability motivation |

### Exact contract / M-C-A

`input=QPSK I/Q; state=single loop phase/frequency; H=1; score=arg of L-sample fourth-power sum; no merge/prune; lag=MAF+30/35ns loop; no reliability trigger/fallback; causal; output=VCO control/data; memory O(L); decoder-free=yes; single-tone=no.` 自身四判据4/4；D1 neighbor，D2 cheap absorption/strong neighbor。

## L09/C12 — feedback+feedforward CPR 2025

### 标准字段（14+）与七子表

| 字段 | 提取 |
|---|---|
| 身份/源 | Hu et al., Electronics 14:265, 2025；`10.3390/electronics14020265`；OA PDF/content |
| 问题 | Diff-FOE+4th-PE at low SNR suffers block discrepancy/cycle slips and high complexity |
| 方法 | second-order feedback coarse CFO/phase + N=64 fourth-power feedforward fine phase（content :157–219） |
| I/O | equalized QPSK → combined phase estimate/corrected symbols/RS bits |
| 信息边界 | blind receiver I/Q；RS downstream only；no decoder feedback/truth |
| lifecycle | loop acquisition→steady tracking + fixed-block residual; H=1; no trigger/reset |
| baseline | Diff-4th、MCRLB、DQPSK |
| complexity | 4K multiplications+67K additions vs 11K+8223K；lock 11μs@20Mrad/s |
| experiment | 2.5Gsps QPSK, RS(255,223), linewidth10kHz, residual CFO20MHz；simulation+FPGA optical bench |
| conclusion | 4.5dB BER 6.7e−3 vs .25；hardware −41dBm 7.5e−4 vs .48 |
| limitation | no free-space/turbulence；simplified Doppler；no CI/seeds；baseline matrix misses C10/C11/C05 |
| open | MATLAB stated, no code link |
| role | recent strongest low-complexity optical cheap alternative |
| ML fields | N/A |
| title gate | PASS，content :5 |

### Exact contract / M-C-A

`input=QPSK I/Q; state=single feedback phase/CFO+fixed-block residual; H=1; score=phase-detector/fourth-power average; no merge/prune; lag=N=64+loop; no reliability trigger/fallback/reset; output=corrected symbols; exact aggregate ops; decoder-free CPR=yes; single-tone=no.` 自身四判据4/4；对 D1是强廉价近邻，对 D2吸收动机而非 exact action。

## gw-read MUST 七子表横向闭包（9/9）

> 以下七表是 gw-read 的 canonical schema；各论文上方“七子表”是本专题 action-contract 辅助视图，不替代本节。

### 1. 状态空间

| Paper | 维度名 | 范围/取值 | 归一化方法 |
|---|---|---|---|
| C01 | `ω,φ,θ(0:k),` single unwrap center | real frequency/phase + Wiener vector；H=1 | N/A（统计 estimator） |
| C09 | phase track, quadrant offset, rolling sums | `{noCS,CS+,CS−}` hard state + N/L buffers | N/A |
| C14 | cumulative unwrap center + `ω,φ` | H=1, modulo phase/frequency | N/A |
| C02 | fwd/bwd circular phase mixtures + `φ` confidence | adaptive or L=1/2/3 Tikhonov components | mixture weights sum to 1 |
| C05 | spectrum CFO + residual-carrier phasor | one continuous carrier state | CSPR/power normalization in receiver |
| C08 | AGC gain + DPLL phase/frequency | scalar amplitude and second-order loop state | AGC target power 1 |
| C10 | phase or `[phase,CFO]` Gaussian state/covariance | 1D/2D; update every m symbols | Kalman covariance normalization |
| C11 | MAF phase error + loop/VCO state | one QPSK circular phase/frequency state | atan2 removes amplitude gain |
| C12 | feedback NCO phase/CFO + block residual phase | H=1; fixed N=64 residual block | fourth-power phase normalization |

### 2. 动作空间

| Paper | 类型 | 维度 | 合法动作约束 |
|---|---|---|---|
| C01 | N/A（estimator update等价） | unique ±2π branch + ML/MAP update | exactly one branch, lag0 |
| C09 | hard discrete correction | no-op / suffix `+π/2` / `−π/2` | only when `δ` crosses signed threshold |
| C14 | N/A（estimator update等价） | unique ±2π branch / WPA weighting | H=1; no rollback |
| C02 | probabilistic mixture update | expand M-way, merge/prune to adaptive/L | KL≤ε cluster; cap L; pilot recovery only at pilots |
| C05 | deterministic signal correction | CFO downconversion + conjugate carrier beating | requires transmitted residual carrier |
| C08 | continuous loop control | AGC gain + NCO phase/frequency update | fixed loop coefficients |
| C10 | continuous estimator update | every-m KF + interpolation + Q adaptation | one Gaussian trajectory; fixed m |
| C11 | continuous loop control | atan2 phase error→VCO update | fixed MAF/feedback latency |
| C12 | continuous+block correction | feedback coarse + fixed-block fine phase | one path; fixed N=64 |

### 3. 奖励函数

| Paper | 完整公式/目标 | 归一化方式 | 权重值 |
|---|---|---|---|
| C01 | N/A（非RL）；objective=`arg max ML(ω,φ)+arg max MAP(θ|ω,φ,r)` | MSE/CRLB reporting | N/A |
| C09 | N/A（非RL）；decision=`δ<−τ, |δ|≤τ, δ>τ` | threshold from modeled PDF | N/A |
| C14 | N/A（非RL）；LMMSE/LMV minimize phase/frequency MSE | inverse MSE/bounds | N/A |
| C02 | N/A（非RL）；reduction constraint=`min order s.t. D_KL(f||g)≤ε` | mixture weights normalized | ε=1/4 main settings |
| C05 | N/A（非RL）；maximize GMI/net rate under CPR | NGMI/GMI/OSNR | N/A |
| C08 | N/A（非RL）；minimize loop phase error/BER | unit-power AGC | fixed loop gains |
| C10 | N/A（非RL）；Kalman MMSE with innovation-updated Q | covariance form | forgetting β=0.88 |
| C11 | N/A（非RL）；drive atan2 phase error to zero | amplitude-independent detector gain 1 | fixed loop gains |
| C12 | N/A（非RL）；minimize residual phase error/BER | fourth-power phase | fixed loop bandwidth/N |

### 4. 建模假设

| Paper | 假设内容 | 论文位置 | 对后续仿真的影响 |
|---|---|---|---|
| C01 | AWGN+Wiener PN；adjacent phase has unique principal branch | :61–93,:343–357 | must retain failure runs and sweep CFO/PN/N |
| C09 | QPSK weak turbulence；small PN increments；CFO pre-corrected | :57–89,:135–159 | only a cheap comparator in matched QPSK slice |
| C14 | single-tone AWGN/AOPN；principal adjacent increment | :17–31,:280–328 | strongest H=1 baseline, no FSO transfer claim |
| C02 | coded MPSK+pilots+LDPC soft；Wiener PN, no CFO | :23–53 | information-budget mismatch must be explicit |
| C05 | residual carrier and data share Tx/path laser PN | :89–124; PDF p.4 | separate Tx-assisted stratum |
| C08 | ephemeris removes coarse Doppler；BPSK/timing ideal | :17,:31,:116–157 | FSO stress baseline only |
| C10 | fiber 16QAM; single Gaussian phase/CFO state | :33–39,:105–115 | tests fixed-lag primitive, not discrete ambiguity |
| C11 | turbulence represented mainly as power fading | :532–590,:698 | cannot support atmospheric-phase claims |
| C12 | AWGN+Wiener PN, simplified Doppler, no turbulence | :91–141,:381–387 | recent optical cheap comparator only |

### 5. 网络架构

| Paper | 层类型 | 维度 | 激活函数 | 归一化 | 优化器设置 |
|---|---|---|---|---|---|
| C01 | N/A（无神经网络） | analytic unwrap+ML/MAP recursion | N/A | N/A | N/A |
| C09 | N/A | VVPE+rolling detector | N/A | N/A | N/A |
| C14 | N/A | analytic AOPN/unwrap/WPA | N/A | N/A | N/A |
| C02 | N/A | factor graph+mixture messages（非learned network） | N/A | weights sum 1 | N/A |
| C05 | N/A | deterministic Tx/Rx DSP chain | N/A | power/CSPR | N/A |
| C08 | N/A | AGC+DPLL control loop | N/A | unit power | N/A |
| C10 | N/A | linear KF | N/A | covariance | N/A |
| C11 | N/A | MAF+atan2 OPLL | N/A | amplitude independent | N/A |
| C12 | N/A | feedback+feedforward DSP | N/A | fourth power | N/A |

### 6. 适配性分析

| Paper | 适配点 | 不适配点 | 对 Q001 的改进依据 |
|---|---|---|---|
| C01 | exact single-tone input/output and published defect | H=1/no recovery | replace immediate unique commit by bounded evidence delay |
| C09 | receiver-visible trigger+fixed suffix correction | QPSK symmetry/no parallel tracks | must beat hard threshold, not reuse trigger claim |
| C14 | exact simple unwrap ancestor | AWGN/2013/no PN | mandatory lowest-cost baseline |
| C02 | full multi-modal mechanism and fixed orders | decoder/pilot/bidirectional LLR output | freeze different task/resource/output contract |
| C05 | recent high-linewidth optical solution | changes transmitter/info budget | receiver-only boundary and separate system stratum |
| C08 | real FSO AO/fade/CFO loop | BPSK/no suffix ambiguity | include as FSO cheap stress comparator |
| C10 | fixed lag and adaptive reliability with exact ops | H=1 fiber/QAM | do not claim fixed lag/adaptation alone |
| C11 | fade-independent cheap detector | no CFO/PN unwrap ambiguity | D2 needs residual ambiguity beyond normalization |
| C12 | recent low-complexity slip-suppression hybrid | H=1/no FSO turbulence | Q001 must show residual suffix defect vs hybrid |

### 7. 问题提取

| Paper | M | C | A / location | 方法产出 | 四判据 |
|---|---|---|---|---|---|
| C01 | single-path unwrap+ML/MAP | CFO+Wiener PN | unique branch always correct；:343–357/:423–451 | recursive joint estimator | 4/4 with current baseline corpus |
| C09 | VVPE/PU/CS-DC | weak-turbulence QPSK WOC | hard discriminant remains reliable；:25–45 | CSSC hard suffix repair | 1/2/4 pass; 3 supplied by corpus |
| C14 | high-SNR AOPN+recursive unwrap | mid/low-SNR single tone | approximation/init reliable；:280–328 | AOPN models+improved unwrap | 1/2/4 pass; 3 fail alone |
| C02 | DP/BARB/unreduced mixture | coded MPSK strong PN | grid cost/single-mode/unbounded growth；:13–19 | KL mixture tracker | 1/2/4 pass; 3 historical alone |
| C05 | time-domain pilot CPR | MHz linewidth high-order QAM | pilot extrapolation remains valid；:50,:97 | residual-carrier transceiver | 4/4 for its own problem |
| C08 | amplitude-sensitive PLL | AO residual fade+CFO | constant detector gain；:116–157 | AGC+DPLL | 1/2/4 pass; 3 insufficient alone |
| C10 | every-symbol KF | 200G QAM resource limit | every-symbol update necessary；:27,:39–103 | reduced-rate/adaptive-Q KF | 4/4 for its own problem |
| C11 | sine/fourth-power OPLL | fade+feedback delay | gain independent of amplitude；:607–680 | atan2 OPLL | 4/4 for its own problem |
| C12 | Diff-4th | low-SNR Doppler+PN | feedforward blocks remain stable；:41–55,:157–219 | feedback+feedforward CPR | 4/4 for its own problem |

## 通信参数/信息边界四列表（9/9）

| Paper | 信道/链路模型 | 关键参数 | 参数/边界来源 |
|---|---|---|---|
| C01 | single tone, AWGN+Wiener PN | N=11/16；PN var 1e−4…0.1；ω=.05/.1；1e5 MC | content :393–469 |
| C09 | QPSK weak lognormal/phase WOC | 2GBaud；N=10/25/55；L=50；linewidth100k–1M；100M symbols | :233–301；PDF pp.3–5 |
| C14 | single tone AWGN/AOPN | modulo frequency/phase；exact/Tikhonov/Gaussian AOPN | :17–31,:228–328 |
| C02 | coded MPSK AWGN+Wiener PN | LDPC4608/rate.89；B/Q/8/32PSK；σΔ=.01/.05/.1；pilot .0125/.025/.05 | :23–28,:370–406 |
| C05 | coherent fiber residual-carrier | 45GBaud PS-256QAM；80km；3MHz；CSPR−11.4dB | :128–195 |
| C08 | LEO-ground AO+BPSK | 10GBaud；1550nm；100MHz CFO；50cm aperture；AO5kHz | :37–59,:83–98,:143–200 |
| C10 | 12×80km PDM-16QAM fiber | 200Gbps；linewidth100k–1M；CFO100M–1.2G；β=.88 | :105–115,:139–231 |
| C11 | LEO QPSK scintillation | 20Gbps；700km/20°；10G/625M sampling；30/35ns loop | :532–590,:636–684 |
| C12 | inter-satellite proxy AWGN+PN | 2.5Gsps QPSK；linewidth10kHz；CFO20MHz；N=64；RS(255,223) | :223–274,:351–387 |

## 实验完备性（5篇）

| Paper | claims/scope | statistics | baseline/fair tuning | ablation | channel/topology/source | complexity | V/V'/U |
|---|---|---|---|---|---|---|---|
| C01 | joint estimator/bounds/O(N), bounded single-tone；failure excluded | 1e5/point；seeds/error bars/tests=none | 4 classes；sources cited；fair tuning not stated | N/SNR/PN/CFO/phase/amplitude scans；no unwrap removal | ideal AWGN+Wiener; single configuration; parameters chosen in paper | core O(1)/sample；full θ cost missing | 3/2/1 |
| C09 | CSSC lowers slip, bounded QPSK weak turbulence | 100M+3e8 MC+lab；no CI/seeds/test | CS-DC+no-correction；source cited；same link but tuning budget unstated | N/L/linewidth/turbulence/CFO scans；no component removal | lognormal/Gaussian phase+Wiener+AWGN；single WOC/lab；paper-derived | rolling O(1), buffer O(N+L); only discriminant op table | 2/3/1 |
| C02 | near-DP limited mixture, bounded coded-MPSK | trials/seeds/CI/test=not stated | DP/BARB/unlimited/L1–3/selection；same channel；ε differs by variant with rationale | order/ε/merge variant scans；no φ/pilot removal | ideal AWGN+Wiener；multi modulation, one link; paper-defined | exact MUL/LUT; memory/latency/runtime absent | 2/2/1 |
| C10 | reduced update/adaptive-Q tradeoff, bounded fiber16QAM | seeds/runs/CI/test=not stated | per-symbol/block KF/Q partition；block-KF conditions differ；fair tuning not stated | m/CFO/linewidth/spans/power/Q scans; no module deletion | SSFM fiber single topology; parameters listed, no FSO source | exact RA/RM/LUT; no hardware latency/power | 2/1/1 |
| C12 | hybrid CPR performance/cost/hardware, bounded lab proxy | MC count/seeds/CI/tests not stated; hardware repeats absent | Diff-4th/MCRLB/DQPSK；misses C10/C11/C05；fair tuning not stated | bandwidth/N/SNR/power scans；no feedback/feedforward removal | AWGN+Wiener, single simplified link/two Doppler sweeps; no real FSO source | exact aggregate mult/add; no FPGA resources/memory | 2/2/1 |

### 对标汇总

- 统计规范：0/5 报告 seeds，0/5 给 error bar/CI/statistical test；只有 C01/C09 给出明确大样本量。平均 U=`1.0/3`。
- baseline：平均覆盖约 4 类内部/外部对手，但 0/5 明确统一调参预算；C10 有条件不完全同质，C12 漏 recent cheap rivals。
- 消融：5/5 有参数扫描，0/5 做严格逐模块 delete/replace/zero ablation。
- 信道/拓扑：5/5 单链路；仅 C09 有 WOC lab，C12有bench但无真实free-space；参数多由论文自定而非标准。
- 复杂度：C02/C10/C12 有 primitive counts，C01只有 asymptotic，C09只局部；0/5 同时报 memory+worst latency+runtime。
- V/V'/U 平均=`2.2/2.0/1.0`。后续 Contract 的最低纪律必须高于此 corpus 盲点，尤其 seeds/CI、fair tuning、逐模块消融和固定资源账本。

## 写作架构（3篇，A–H）

### C01 Wang TSP 2022

- **A 章节**：Introduction→Signal Model→ML/MAP derivation→Recursive Implementation→Bounds→Unwrap/WPA→Numerical Results→Conclusion；System Model/estimator/implementation独立，Problem Formulation隐含在derivation。
- **B 参数**：参数散在正文/captions；无 notation/集中表；有 N/SNR/PN/CFO/phase/amplitude sensitivity。
- **C 图表**：11幅 performance/bound curves；无系统/算法框图、热力图、误差棒。
- **D 实验**：4类baseline/bounds，多参数扫描；有复杂度分析，无逐模块消融/统计不确定性。
- **E 叙述**：经典估计问题→纯AWGN/频域/准静态不足→Wiener PN→4条贡献；related work嵌引言；结论收束算法+界+复杂度。
- **F 经典段落模式（转述）**：引言先把旧likelihood的条件说清，再用现实PN破坏条件；方法先给batch closed form，再给递归实现；结果先界后离界。适合对比/演绎仿写，不复制原句。
- **G 公式**：连续编号，变量多在式后行内定义；推导链完整，Schur/recursion衔接有文字；bounds独立节。
- **H 引用**：引言/related密、方法较少、实验引用baseline；共同基础 Fu–Kam 2013 已覆盖；无新增 Step3.5 seed from this architecture audit。

### C02 Shayovitz–Raphaeli TCOM 2016

- **A 章节**：System Model/SPA→Directional Statistics/KL→Tikhonov formulation→Reduction Algorithms/Theorems→Limited-order recovery→LLR→Complexity→Numerical Results→Discussion；有明确 problem formulation/algorithm design。
- **B 参数**：ε/L/pilot/PN散在 method与captions；无集中notation表；order和ε sensitivity明确。
- **C 图表**：factor graph、trajectory 3D图、BER/PER curves、mixture-order/ε curves、2 complexity tables；captions偏自解释，无error bars。
- **D 实验**：DP/BARB/unlimited/L1–3/selection；order/ε ablation-like scans；exact arithmetic complexity，无latency/memory。
- **E 叙述**：BARB soft信息不足→error floor/pilot overhead→mixture explosion→KL-bounded objective→algorithm/theorem→engineering cap→performance/cost。
- **F 经典段落模式（转述）**：用多PLL轨迹解释抽象 mixture split/merge；把“固定order不合理”改写成“满足KL门的最小order”；长证明移附录。
- **G 公式**：连续编号、system variables先定义、exact SPA→canonical mixture→reduction objective→pseudo-code；定理证明完整并下沉附录。
- **H 引用**：引言和reduction review归类引用，算法/实验较少；BARB/DP/Tikhonov基础均已在本 corpus 定位，无未覆盖承重 direct seed。

### C12 Hu Electronics 2025

- **A 章节**：Introduction→System Model→baseline Diff-4th→proposed feedback/feedforward→Simulation→Hardware→Conclusion；method/system/hardware独立，problem由引言taxonomy+Table1表达。
- **B 参数**：集中 Table2，符号在公式后 `where` 定义；bandwidth/N/SNR/power sensitivity充分。
- **C 图表**：14 figures/5 tables；baseline框图后proposed框图，参数/complexity/hardware表齐；无3D/heatmap/error bars。
- **D 实验**：Diff-4th/MCRLB/DQPSK；parameter interaction scans；simulation+bench；有aggregate op count但无component ablation/FPGA resources。
- **E 叙述**：场景→FO/PN→FOE/PE taxonomy→各类缺陷→hybrid对应解决→simulation→hardware；4条贡献，related work按方法分类。
- **F 经典段落模式（转述）**：先画reference链再画hybrid链；每个结构部件对应引言中的一个缺陷；最后用硬件闭环收束。可仿写结构，不照搬“novel/superior”措辞。
- **G 公式**：连续编号，每式后定义物理量；推导较短，强调参数/实现折衷而非完整证明。
- **H 引用**：引言taxonomy引用密，方法/实验少；未纳入 C10 reduced-rate KF、C11 atan2 OPLL、C05 residual carrier，三者已由当前 corpus 补齐，后续比较必须纳入。

## 综合动作/复杂度矩阵

| Method | input/state | H / score / merge | lag/trigger/fallback | output/resource | Q001 relation |
|---|---|---|---|---|---|
| C01/C14 | decoder-free single tone；one unwrap+CFO/phase | H=1；no score/merge | lag0；none | unwrap+estimates；O(1) primitive | reference/strongest simple baseline |
| C09 | QPSK CPE phase；quadrant offset | hard 3-class；`δ` threshold | fixed centered window；suffix correction | corrected symbols；O(N+L) buffer | strongest hard cheap near |
| C02 | coded MPSK+pilots+LDPC soft；circular posterior | adaptive/L1–3 Tikhonov；likelihood+KL/CMVM | no fixed lag；pilot+`φ` recovery；fwd/bwd | LLR；O(ML²)/iteration | primitive full-general superset, task-contract neighbor |
| C10 | 16QAM+pilots/DD；phase/CFO Gaussian | H=1；innovation/adaptive-Q | fixed m lag；no recovery | corrected symbols；exact ops | fixed-lag/reliability near comparator |
| C11 | QPSK I/Q；OPLL | H=1；atan2+MAF | 30/35ns loop；no trigger | data/VCO；O(L) memory | D2 cheap absorption |
| C12 | QPSK I/Q；feedback+block residual | H=1；phase detector/4th avg | N=64+loop；no trigger | symbols；4K mult+67K add | recent cheap absorption/near |
| C05 | payload+Tx carrier | H=1；spectrum peak | continuous tone；BPS residual | symbols；system overhead | different-info system alternative |
| C08 | BPSK I/Q；AGC+DPLL | H=1；phase error | causal loop；no recovery | bits；1.4ms acquisition | FSO cheap neighbor |

## D1/D2 disposition

- **D2 不保留为独立 Q**：C09 已有 receiver-visible hard trigger+suffix repair；C10 有 innovation-driven covariance adaptation；C11 用 amplitude-independent atan2+MAF 吸收 fade-reliability；C12 用固定反馈环吸收低SNR slip动机。`reliability-triggered` 原子本身不构成可区分方法。
- **只保留一个 D1-shaped Q001**：动作输出形态限定为 `decoder-free single-tone receiver input → explicit discrete 2π-wrap hypotheses (bounded H≤3) → receiver-only likelihood/merge-prune → fixed-lag commit → one unwrapped sequence + confidence/fallback flag`。fixed H、fixed lag、multi-hypothesis、confidence、merge/prune 均不是单独 novelty；可区分性只来自完整 task/resource/output contract。
- D2 的 receiver-visible ambiguity score 最多作为 Q001 future implementation 的可选 ablation/average-cost policy，不作为第二条方法或第二个 Q。

## Canonical Q001 与 glossary 四判据

**Q001**：`M=Wang C01 的 Fu–Kam single-path unwrap→joint ML/MAP；C=coherent FSO residual CFO + laser Wiener PN，且 receiver 需 decoder-free、fixed memory/worst latency；A=H=1 lag-0 greedy unwrap 假设每个 adjacent principal increment 的唯一 branch 始终正确，错误一旦 commit 即污染 suffix，而 full mixture 的 decoder/pilot/bidirectional contract 与资源/输出不适配。`

| 判据 | 证据 | Step3 verdict |
|---|---|---|
| 1 具体技术矛盾 | C01 :343–357、:423–451 明确 unwrap failure 与 suffix propagation/failed-run exclusion；C02证明多轨迹错删会 slip | PASS |
| 2 可复用方法产出 | 完整输出形态为 bounded H≤3 fixed-lag unwrap；输入、状态、score/merge-prune、commit、fallback、output、resource axes均可画/写/消融 | PASS |
| 3 当前 baseline | reference C01(2022)；recent task/cheap C10(2021), C11(2023), C05(2024), C12(2025)；full-general C02 mandatory | PASS |
| 4 可量化对标 | unwrap failure/suffix length、phase/frequency MSE、BER/outage，外加 ops/symbol、memory、worst/average latency；同一输入预算公平比较 | PASS |

Step 3 只说明问题可证伪且 comparator 边界可辨；不证明目标 FSO 中 defect occurrence/headroom，不构成 Go、方法、新颖性或 `METHOD_SIGNAL`。

## Baseline ladder 与方法章输出形态

- **最强传统未优化 baseline**：C14/C01 H=1 adjacent-difference unwrap→Wang joint ML/MAP。
- **增强 cheap baselines**：C09 hard threshold suffix correction；C10 fixed-lag phase/CFO KF；C12 feedback+fixed-block feedforward；FSO fade stress 下加 C08/C11。
- **full-general comparator**：C02 unlimited/adaptive mixture + fixed order2/3，保留其 decoder/pilot 信息优势并单列 input-budget mismatch。
- **系统级 alternative**：C05 residual-carrier modulation，只在允许 transmitter change 的独立 information-budget stratum 比较。
- **可画产出**：input/phase-difference→H≤3 wrap-state bank→score→bounded merge/prune→fixed-lag commit/fallback→unwrapped sequence→Wang ML/MAP；主图为 failure-rate/BER vs PN+CFO，次图为 performance–complexity/latency Pareto；消融至少 H、lag、score、merge/prune、fallback 和是否触发扩阶。
- **claim ceiling**：task-adapted bounded low-complexity estimator candidate；不得声称首次 multi-hypothesis、首次 fixed lag、首次 confidence/branch pruning。

## Step 3 terminal

`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`。

理由：Q001 四判据 4/4；D1完整 action/resource/output contract 与 C02 full tracker、C09/C10/C11/C12 cheap alternatives 可区分；D2 已合并/降为可选组件。下一合法动作仅为 Step 3.5 exact-action/claim closure，需另行授权。

## Step 3.5 supplement

三轮检索的 new MUST/SHOULD=`5/5 → 4/8 → 0/0`，实际筛查 60 条 citation records；新增 9 篇 primary fulltext 动作核验。完整 receipt 与 action matrix 见 R006 和 `projects/thesis-fso/multi-hypothesis-phase-unwrapping/step3-5-search-receipt.json`。

承重更新为 Ulvog et al., ICASSP 2023：`wrapped single tone → integer-cycle Viterbi paths → causal LMMSE/Gaussian branch score → fixed S survivor cap → iterative GLS → unwrapped sequence`。它未逐字覆盖 D1 的 fixed-lag commit/confidence/fallback，但已占据承重机制；H=3 是既有 S cap 的参数选择，fixed lag 是 standard Viterbi traceback truncation。当前没有新 score/commit/fallback 或可区分 performance–complexity mechanism，故按 D006 冻结 gate 判 `CHEAP_ABSORPTION`。

Step 3.5 唯一 terminal=`EXACT_ACTION_COLLISION_OR_CHEAP_ABSORPTION`。D005 的问题证据仍是历史有效结论，但 Q001 无 Step 4a 入口；不得实现、仿真、冻结参数或输出 Go/方法/METHOD_SIGNAL。
