# RML-FSTS Literature Owner

> 独立 owner：`.sessions/2026-08-08-rml-fsts-groundwork/`
> 研究对象：Wang 2023 FSTS fixed-lag/`BL` condition-dependence
> 当前记录 Step 1–3.5 已完成；D008/V005 将 Q1 修订为带全文限制的 provisional survivor。Step 4a 已在 validity/calibration 起飞门前终止为 `STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`（D011/V007）；没有 Go/Kill/Resolved、METHOD_SIGNAL 或方法实现裁决。

## GW Progress

| Step | 状态 | 日期 | commit | 证据 | 下游门控 |
|---|---|---|---|---|---|
| 1 search | ✅ PASS | 2026-08-08 | `a52bb5d6` | R001 + `rml-fsts-step1-search-receipt.json` + 7 query JSON | 允许 Step 2 |
| 2 acquire | ✅ USER_CONFIRMED | 2026-08-09 | `a52bb5d6` | 5 篇合格 CORE + R002 + coverage/receipt + D003 | 允许 Step 3 |
| 3 read | ✅ completed | 2026-08-09 | `80c337aa` | 5/5 fresh full-text read + R003 + D005/V003 | D006 已授权 mandatory Step 3.5 |
| 3.5 supplement | ✅ COMPLETE / PROVISIONAL SURVIVOR | 2026-08-09 | D008/V005 | R004 + search/citation receipts + shared 130981 fulltext；三轮上限 | 带全文限制开放 Step 4a 讨论入口 |
| 4a feasibility | 🛑 INCONCLUSIVE / VERIFIED | 2026-08-09 | — | D009–D011/S004/V006–V007/T015–T019/H006 | terminal=`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`；performance grid/MVE 未运行；专题 dormant、下游禁止 |

## Step 1 候选表

| # | DOI | Priority | 路线 | CORE 预判 | 全文状态（Step 1 结束时） |
|---:|---|---|---|---|---|
| 1 | `10.1109/JPHOT.2023.3265847` | 必读 | A/C | C1/C2/C4 | 共享全文待 Step 2 核验 |
| 2 | `10.1109/JPHOT.2022.3161795` | 必读 | A | C2/C4 | 待 Step 2 |
| 3 | `10.1364/OE.520452` | 必读 | A/C | C2/C4 | 共享库待 Step 2 核验 |
| 4 | `10.1016/J.OPTCOM.2020.126046` | 必读 | A | C2/C4 | 待 Step 2 |
| 5 | `10.1109/CHINACOM.2009.5339877` | 必读 | B | C3 | 待 Step 2；题名不能冒充全文 |
| 6 | `10.1109/TVT.2022.3218937` | 必读 | B | C3 | 共享全文待 Step 2 核验 |
| 7 | `10.3390/electronics10232942` | 建议读 | B | C3 | 待 Step 2 |
| 8 | `10.1155/2009/821819` | 建议读 | B | C3 | 待 Step 2 |
| 9 | `10.1109/JLT.2020.3003561` | 必读 | C | C4 | 共享全文待 Step 2 核验 |
| 10 | `10.1364/OE.505931` | 必读 | C | C4 | 待 Step 2 |
| 11 | `10.1364/OE.448956` | 必读 | C | C4 | 待 Step 2 |
| 12 | `10.1109/WiSEE61249.2024.10850117` | 必读 | C | C4 | 共享全文待 Step 2 核验 |

## Step 1 边界

- source fact：fixed `BL/BN` 与 modulation、training length、received power 条件有关，低功率存在 timing/FOE 退化。
- target hypothesis：同一 receiver-visible condition 内是否有 lag-ranking crossover 仍未知。
- strongest cheap alternative：未来必须保留 dev-frozen modulation/TS/receiver-power-conditioned single-lag lookup。
- prior-art ceiling：不得声称首创 multi-lag、stepwise correlation、FSTS 或联合同步。

## Step 2 覆盖

- 合格 CORE 5 篇：Wang 2023（C1/C2/C4）、Enhanced 2024（C2/C4）、Morelli 2009（C3）、Paillier 2020（C4）、Yu 2023（C3）。
- Tang 2022 与 WiSEE 2024 因 metadata/provenance 矛盾不计入；另 5 篇全文止损后仍缺失。
- Step 2 coverage terminal=`STEP2_READY_FOR_USER_CONFIRMATION` 的用户确认关口已满足；**Step 2 结束时状态**=`STEP3_DISPATCH_READY`，当时 Step 3 尚未开始。

## Step 3 派发边界

- 冻结精读输入：Wang 2023、Enhanced 2024、Morelli 2009、Paillier 2020、Yu 2023，共 5 篇合格 CORE。
- Yu 2023 先闭合共享 `source.md` 到 canonical `content.md` 的字节一致路径适配与 title/DOI preflight；失败则 title-abort 并返回 Step 2。
- 四判据只采用 `stages/glossary.md` canonical 四项；不得增加 `problem_truth` 或 `novelty` 门。
- 无 Q# 全过时保持 Step 3 `BLOCKED/IN_PROGRESS`，记录回 `gw-search` 的恢复路径；通过时只将 Step 3 标为 `✅ completed`，不自造 terminal。
- T001 到 Step 3 边界停止；不进入 Step 3.5/4a，不运行 smoke、实现或仿真。

## Step 3 综合分析

### 现有方法分类

1. **FSTS / two-stage training-aided FOE**：Wang 2023 用双偏振 FSTS 同时承载 FS 与 coarse/fine FOE；`B_L` 同时控制 fine-stage phase-noise suppression 与 unambiguous range。Enhanced 2024 用 PRBS+cyclic-QPSK，先 differential FS、再 FFT coarse FOE 和 cross-polarization fine FOE；其 `TL` 有显式 power/length threshold。
2. **multi-lag / stepwise correlation prior art**：Morelli 2009 已用 multi-RX、multi-lag correlation likelihood 与 correlation-magnitude/lag weighting 做 closed-form CFO refinement；Yu 2023 已用 `AC1→AC2→multi-block CC` 做 coarse-to-fine residual refinement。二者只限制 prior-art ceiling，不是 coherent-FSO 直接竞品。
3. **coherent space-ground carrier maintenance / transfer physics**：Paillier 2020 把 AO 后 `rho(t),phi(t)` 接入 AGC+DPLL，量化 residual CFO capture、fading-induced lock-threshold shift 与 BER penalty；它约束迁移物理，不证明 FSTS target defect。

### 已知局限（仅作 gap/novelty 原料）

- Wang 2023 的 fixed `B_L` 已显示 modulation/training-length dependence，低功率下 FS/FOE 退化；但没有 target 星地 condition 内 lag-ranking scan。
- Enhanced 2024 的 `TL` 优劣阈值随 received power 与 total length 变化；但不是 AO/轨道 Doppler 下的 conditioned lookup 证据。
- Morelli/Yu 已占据“multi-lag weighted fusion / stepwise correlation”基本形态；仅换成多 lag 不足以形成后续贡献。
- Paillier 只有单一 BPSK、20°、2 s 场景和 ideal timing；不能闭合跨调制/跨仰角/多分支 FSTS 竞争。

这些都是空白原料，不能直接作为问题、novelty 或 Go。

### 2–3 年趋势与背景时间线

- **2009**：Morelli 建立重复 preamble 的 multi-lag correlation refinement、MSE/range/complexity 分析。
- **2020**：Paillier 将真实传播/AO 时序与 deterministic carrier loop 接口连接；同年缺失的 Cheng direct comparator 仍是证据债务。
- **2023**：Wang 把 frame 与 two-stage FOE 合并进 FSTS；Yu 把 frame geometry、PFPE 与 stepwise AC/CC 统一到 satellite synchronization。
- **2024**：Enhanced 进一步采用 mixed training、显式长度扫描和有限实验验证。近 2–3 年趋势是 training reuse、coarse-to-fine correlation、overhead/complexity 与通信性能联合展示；不是学习化趋势。
- **当前定位**：RML-FSTS 只把 Wang fixed-`B_L` 的 condition dependence 作为可证伪 research problem 入口；C3 先例限制方法主张，C4 约束目标场景迁移。

### Baseline 交叉验证与 strongest cheap alternative

| 对象 | 交叉证据 | 合法角色 |
|---|---|---|
| Wang 2023 FSTS | L01 完整算法/仿真；L02 Ref.24 独立确认近期身份 | target Q 的近期 M / source baseline |
| Enhanced 2024 | L02 近期 mixed-TS、FS+FOE、功率/长度扫描 | task-matched comparator |
| Morelli 2009 | multi-lag magnitude/lag weighted refinement | historical prior-art ceiling，不满足近期门 |
| Yu 2023 | stepwise AC+CC 与 frame geometry | prior-art ceiling；RF/AWGN 不外推 target defect |
| Paillier 2020 | AO+AGC+DPLL transfer physics | C4 physics anchor，不是 FSTS comparator |
| conditioned single-lag lookup | dev-frozen modulation/TS/receiver-power bin 内选单一 lag | **strongest cheap alternative**；Step 3 不比较胜负 |

### 五篇实验完备性对标汇总

| L# | Verification | Validation | Uncertainty | 主要强项 | 主要盲点 |
|---|---:|---:|---:|---|---|
| L01 | 3 | 2 | 1 | 800/6400 次平均、多维仿真、复杂度解析 | 无 seed/CI/统计检验/实测 |
| L02 | 2 | 2 | 2 | 800/3200 次、一处 error bar、有限室内实验 | 公式/表转换缺失、实测窄 |
| L03 | 2 | 1 | 1 | MSE/bound/range/operation count | 无 runs/seed/error bar/实测 |
| L04 | 2 | 2 | 1 | 物理传播+AO+DPLL 端到端链 | 单 realization、无竞争算法/统计 |
| L05 | 2 | 2 | 1 | 多调制/编码/短长包、CRB/RMSE/BER | 仅 AWGN、无 trials 数/CI/组件消融 |

均值为 Verification=2.2、Validation=1.8、Uncertainty=1.2。共同惯例是参数扫描与 bounded claim；共同盲点是 seed/CI/统计检验、公开代码与硬件复杂度不足。

### 缺失直接竞品 / 证据债务矩阵

| 对象 | 角色 | 当前证据层级 | 允许使用 | 禁止承重 | Step 3.5 优先级 |
|---|---|---|---|---|---:|
| Cheng 2020 `10.1016/J.OPTCOM.2020.126046` | low-OSNR direct comparator | 引文身份/Step2 缺全文 | 列 debt、确认 comparator 类别 | 公式、失效机制、实现、novelty | 1 |
| Dong 2009 `10.1109/CHINACOM.2009.5339877` | exact-title multi-correlation lag | identity 命中、无全文 | 列 historical debt | 公式/碰撞终判 | 2 |
| Electronics 2021 `10.3390/electronics10232942` | multi-pilot correlation | 无全文 | 列 debt | 公式/实现/claim ceiling | 2 |
| `10.1364/OE.505931` | real-time low-SNR diversity/CPR | 无全文 | 列 C4 debt | transfer 性能数字/机制 | 1 |
| `10.1364/OE.448956` | branch phase asynchrony | 无全文 | 列 C4 debt | branch failure 机制 | 1 |
| Tang 2022 | task-matched candidate | 有正文但 metadata/provenance 矛盾 | 只列债务 | 任一承重事实 | 2 |
| WiSEE 2024 | recent receiver DSP | 有正文但 metadata/provenance 矛盾 | 只列债务 | 任一承重事实 | 2 |

本轮不补件、不检索。C1/C2 仍偏 Wang 谱系；C3 只约束 prior-art ceiling，C4 只约束 transfer physics。

### 写作架构参考（固定三篇）

| 标杆 | 结构与比例 | 图表/实验组织 | 公式与叙述链 |
|---|---|---|---|
| L01 Wang 2023 | TS→FS→coarse/fine FOE→complexity→platform→results；method/results 约34.5%/44.8% | 18 figures+2 tables；MSE→BER→sensitivity，多参数扫描 | 11 equations；公式后释义并解释 range/noise tradeoff |
| L02 Enhanced 2024 | Introduction→Operation principle→Settings→Results→Summary；principle/results 32.5%/47.6% | 20 figures+2 tables；training length/`TL`→MSE→BER→有限实验 | 21 equations（转换缺本体）；mixed training object 贯穿两任务 |
| L04 Paillier 2020 | physics model→`rho,phi`→AGC/DPLL→sanity check→turbulence→BER；model+DSP 65.8% | 15 figures+2 tables；由 control metric 递进到 communication metric | 物理意义→公式→参数表→数值预测；结论从假设退出 future work |

共同模式：问题由具体 estimator/receiver assumption 引出；System Model 与 DSP 输入契约相连；参数需公式后释义并集中表；实验由内部估计指标连接 BER/sensitivity；结论只收束已验证 scope。经典短句与共同基础引用详见三份 fresh reader log，本 owner 不复制长原文。共同但未覆盖的基础项包括 Park/Schmidl-Cox、Gardner/Simon PLL、Cheng 2020 与相屏/AO 基础文献；仅登记为未来 Step 3.5 输入。

### Canonical 研究问题清单

| Q# | M（具体近期方法） | C（条件） | A（失效假设） | 方法产出形态 | 判据1 | 判据2 | 判据3 | 判据4 | 四判据 | 来源文献 | 证据状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Wang 2023 fixed-`B_L` FSTS two-stage FOE | 固定 modulation、TS length、receiver-power bin 内，不同 receiver-visible turbulence/branch/phase-reliability condition | M 隐含假设同一 `B_L` 仍近似最优；若 turbulence/branch/phase reliability 改变最优 lag 或 lag ranking，fixed 设计将不足 | condition-to-lag design rule / reusable performance-curve family（只定产出形态，不设计实现） | ✅ M-C-A 句子级、A 可证伪；不要求本轮已证伪 | ✅ 可复用 design rule/curve family | ✅ Wang 2023 exact recent M + Enhanced 2024 Optics Express task-matched 顶刊 comparator；由 L02 闭合项目 2019+ 顶刊门，不依赖 Wang venue 等级 | ✅ 以 CFO MSE、BER/sensitivity、range、complexity 对 Wang 与 1 个 conditioned lookup 比较 | **全过** | L01 `content.md:183,208,247-319`；L02 `content.md:404`；项目 venue authority：problem-driven D015、advisor-review topic-index:94；L04 C4 physics | FACT：fixed `B_L`/tradeoff/low-power degradation；INFERENCE：condition 可能违反同一 lag 近似最优假设；UNKNOWN：crossover/failure/headroom |

Q1 通过只表示 Step 3 产生了可进入 mandatory Step 3.5 的问题候选；A 指 M 所依赖且可能在 C 下被违反的假设，不是“ranking 已稳定/cheap comparator 已足够”的结论。不表示 target A 已被证明、novelty 已闭合、cheap comparator 已失败或 Step 4a Go。

## Step 3.5 竞争闭包更新

### 检索与引用链规模

- R1：8/8 keyword matrix，27 条；actual sources=SerpAPI/OpenAlex/S2。Wang/Enhanced forward+backward 四链 63 条→51 unique，`S2-only=0`。
- R2：前三条新术语 query 63 条，known hit 15 次，48 个新标题全部 exclude，new must/should=`0/0`；第 4 条 120 s timeout。
- R3：第 4 条只用 S2+OpenAlex 源限定补查仍 timeout；达到 3 轮上限，禁止 R4。详见 `R004` 与 Step 3.5 receipts。

### Qualified action boundary

| 论文 | content SHA / bytes | 动作与粒度 | 分类 | exact / cheap lookup |
|---|---|---|---|---|
| Tang 2022 | `DB526B...FB69` / 36,071 | 固定 STSB frame localization→FOE | fixed-training direct task | false / false |
| WiSEE 2024 | `214343...14E` / 35,131 | 固定 header/pilot 的 frame/CFO/equalization/CPE | architecture adjacent | false / false |
| ICAIT 2025 | `a65fe9...dc30` / 36,387 | 固定 960-symbol training-spectrum 两级 FOE | architecture adjacent | false / false |
| JLT 2021 | `65571b...3346` / 48,595 | FO sweep+SCDF；参数离线统一优化后固定 | architecture adjacent | false / false |
| Optics Communications 130981 | `67fa0e...66ecb` / 38,504（共享 canonical） | 固定分块 FFT、1024×16-point mean spectrum、正负谱功率比+星历；power/FFT points 为评测或离线参数 | architecture adjacent | false / false |

Morelli/Yu 继续占用 generic multi-lag/stepwise correlation prior art；Wang/Enhanced 是 offline fixed-parameter/length design。Qualified evidence 中没有确认 receiver-visible condition→lag/`B_L`/window selection，也没有确认 dev-frozen conditioned single-lag lookup 等价实现。

### Unresolved primary evidence

执行阶段的“8 项缺全文”是过度合并。130981 共享全文已关闭且排除 exact action；SSRN 6293357 保持唯一高风险 action-level UNKNOWN；ACP/IPOC 10809664 是次级直接 comparator 债。Cheng/OE.561252 为高相关任务/条件邻接，OE.505931/OE.448956/Dong 为非阻断架构或历史 prior-art 边界。

### Terminal 与 claim ceiling

Step 3.5 当前 terminal=`STEP3_5_COMPLETE_Q1_PROVISIONAL_SURVIVOR_WITH_FULLTEXT_LIMITATIONS`（D008/V005）。这不等于首次、novelty closure、target failure 或方法成立。Conditioned single-lag lookup 继续作为 strongest cheap alternative；其胜负与 target crossover/headroom 原属 Step 4a，但本轮在 performance 起飞前即被 testbed validity/calibration 阻断。SSRN 6293357 全文债继续保留，不能因 testbed 阻断而视为 novelty closure。

## Step 4a terminal（V007 PASS）

- terminal：`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`；authority=D011/V007/H006，fresh-context verifier P0/P1/P2=`0/0/0`。
- 三类 hard blocker：structural `(B_N,B_L)` action-before causality；Wang phase-screen/0.2 m aperture/SMF coupling 与 Gu scalar-GG 非等价；Wang dBm receiver-power 到 post-ADC discrete complex-noise variance 不可辨识。由此 B0 numeric calibration gate 不可执行。
- recoverable gap：Wang Fig. 8/10/11/12 原图 403，故 ticks/逐点曲线未恢复。恢复 PDF/原图只能补图轴与部分 numeric target，不能自动关闭三类 hard blocker。
- execution facts：semantic-smoke performance grid=`NOT_RUN`；bounded MVE=`NOT_RUN`；scientific raw rows、paired delta/CI 均不存在；B0/B1/B2/O1/C1 performance 数字=`N/A (NOT_RUN)`。
- 科学语义：Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`；不发 Kill/Resolved/Go，不增加 object/package failure 计数（仍 `0/0`）。任何 structural diagnostic 只能 `DIAGNOSTIC_ONLY / TERMINAL_DISABLED`，本轮未运行。
- 下游：专题 dormant；禁止 performance grid、MVE、Contract、Execute 与论文写作。科学重开只可在取得 authors/source receiver+channel config、显式定义 action-before protocol 后，经 scope-change 进行。

## 五篇标准精读条目

### [L01] Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication

- **DOI/来源**：`10.1109/JPHOT.2023.3265847`；**源路径**：`D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/content.md`（receipt 冻结的 shared canonical）；**发表**：IEEE Photonics Journal 15(3), 2023，正式发表。
- **核心贡献/方法**：双偏振共轭 FSTS 复用 FS 与 two-stage FOE；coarse range `±Rs/2`，fine stage 以 `B_L` 换 precision/range。
- **实验设置**：10 GBaud PM 4/16-QAM；B2B+10 km phase-screen FSO；1/2/4/6 branches；TS 48–960。
- **Baselines**：4th-power/QPSK partition、4th-FFT、conventional TS、Cheng 2020 joint FS+FOE（引用算法，本文仿真/复杂度比较）。
- **关键结论**：320-symbol FSTS 在本文设置下接近/优于 960-symbol TS；低功率 timing/FOE 退化。**关系**：C1/C2/C4 source baseline。
- **关键细节**：320-symbol 4-QAM `(BN,BL)=(16,20)`、16-QAM `(8,40)`；threshold=0.2；CFO `±1.1 GHz`。
- **适配性**：适配 deterministic FSTS/FOE；不适配 target crossover；启示仅为保留 `B_L` tradeoff。**代码**：未报告。**验证**：5/5 preflight PASS，fresh全文重读。
- **FACT/INFERENCE/UNKNOWN**：fixed `B_L` tradeoff=FACT；condition-sensitive ranking=INFERENCE；target failure/headroom=UNKNOWN。

| 7子表 | 提取 |
|---|---|
| 输入 | 双偏振/多分支复样值+FSTS；1 sps |
| 输出 | frame start、coarse/fine/final CFO；非 action space |
| 目标 | reward=N/A；FS accuracy、CFO MSE、BER/sensitivity、complexity |
| 假设 | shared LO/CFO、相位慢变、idealized phase screen |
| 架构 | NN=N/A；IQ→FS→MRC→pol-demux→FOE→CPE |
| 适配 | source baseline；target defect 不承重 |
| 本文问题 | M/C/A✅、产出✅、近期baseline跨文献闭合、量化✅；不等于target Q |

| 通信参数 | 值 |
|---|---|
| 链路/调制/速率 | B2B+10 km FSO；PM 4/16-QAM；10 GBaud |
| training/CFO/PN | 320/960 symbols；CFO±1.1 GHz；Tx/LO linewidth 50 kHz |
| power/channel/diversity/AO | optical power sweep；`Cn²=1e-16/1e-14`；1/2/4/6 MRC；AO未报告 |
| 完备性 | V/V'/U=`3/2/1`；800/6400 repeats，无CI/统计检验 |

### [L02] Enhanced Frame Synchronization and Carrier Recovery in Coherent FSO Communication

- **DOI/来源**：`10.1364/OE.520452`；**源路径**：`D:/code/study/research-protocol/papers/doi/10.1364_oe.520452/content.md`（receipt 冻结的 shared canonical）；**发表**：Optics Express 32(15), 2024。
- **贡献/方法**：PRBS differential FS + cyclic-QPSK FFT coarse FOE + cross-polarization fine FOE。
- **实验**：20 km 10 G PM-QAM，B2B/1/4 branches，QPSK/16QAM，弱/强 turbulence；室内 QPSK 单孔径验证。
- **Baselines**：Park/weighted Park、TS、4th-power/FFT、Wu 2022（引用算法、本文仿真）。
- **结论/关系**：480-symbol 折中；`TL` 门槛随 power/length 变化；C2/C4 近期 comparator。
- **细节**：cycle=16；range=`±3Rs/8`；480/960 symbols；fine complexity正文称 `4N`。公式本体/表体转换缺失。
- **适配/代码/验证**：适配 task metrics，不证明target；代码未报告、数据可索取；preflight PASS/fresh全文。
- **证据状态**：power/length threshold=FACT；target ranking=INFERENCE；star-ground failure=UNKNOWN。

| 7子表 | 提取 |
|---|---|
| 输入 | PRBS+cyclic-QPSK 双偏振/多分支 samples |
| 输出 | frame start、coarse/fine CFO；非 action |
| 目标 | reward=N/A；MSE/BER/sensitivity/range/overhead/complexity |
| 假设 | ideal pol-demux、shared CFO、phase slow over differences |
| 架构 | NN=N/A；diff-FS→FFT→MRC→cross-pol fine FOE |
| 适配 | C2/C4 comparator；target defect不承重 |
| 本文问题 | canonical 4/4；只评价本文自身问题 |

| 通信参数 | 值 |
|---|---|
| 链路/调制/速率 | 20 km FSO；QPSK/16QAM；10 Gbaud |
| training/CFO/PN | PRBS+QPSK 480/960；range±3Rs/8；linewidth 80 kHz文本单位有限 |
| power/channel/diversity/AO | received-power sweep；phase-screen Cn²两点；1/4 branches；AO未报告 |
| 完备性 | V/V'/U=`2/2/2`；800/3200 repeats，一处error bar |

### [L03] A Practical Scheme for Frequency Offset Estimation in MIMO-OFDM Systems

- **DOI/来源**：`10.1155/2009/821819`；**源路径**：`papers/doi/10.1155_2009_821819/content.md`；**发表**：EURASIP JWCN, 2009。
- **贡献/方法**：repetitive FDM pilot；lag-1 coarse FCFO + all-lag magnitude/geometry-weighted refinement + ML ICFO。
- **实验/Baseline**：1024-subcarrier MIMO-OFDM、12-tap Rayleigh；CBFE/PBFE/EMCB，same 32 pilots/TX。
- **结论/关系**：RCFE接近bound、精度/范围/complexity折中；C3 historical prior-art ceiling，不满足2019+门。
- **细节**：`R=8,Q=4,M=32`；multi-lag公式/复杂度见全局read-note；PDF仅用于补公式。
- **适配/代码/验证**：适配collision ceiling，不适配FSO；代码未报告；title/DOI/fulltext PASS。
- **证据状态**：multi-lag weighting=FACT；reliability proxy迁移=INFERENCE；target failure/Go=UNKNOWN。

| 7子表 | 提取 |
|---|---|
| 输入 | repeated-preamble MIMO-OFDM samples、multi-RX correlations |
| 输出 | FCFO/ICFO/final CFO；非 action |
| 目标 | reward=N/A；likelihood、MSE、failure、range、operations |
| 假设 | common CFO、ideal timing、AWGN、static training channel |
| 架构 | NN=N/A；correlation→all-lag refine→DFT/ML ICFO |
| 适配 | C3 ceiling；非直接 comparator |
| 本文问题 | 具体✅、产出✅、近期❌、量化✅=3/4 |

| 通信参数 | 值 |
|---|---|
| 场景/调制/采样 | 5 GHz MIMO-OFDM；QPSK pilots；5 Msps（由Ts推算） |
| training/CFO/SNR | R=8 repeats；normalized CFO；0–18 dB等 |
| channel/diversity/AO | 12-tap Rayleigh；2–4 TX/RX；turbulence/AO=N/A |
| 完备性 | V/V'/U=`2/1/1`；无runs/seed/error bar |

### [L04] Space-Ground Coherent Optical Links: Ground Receiver Performance With AO and DPLL

- **DOI/来源**：`10.1109/JLT.2020.3003561`；**源路径**：`D:/code/study/research-protocol/papers/doi/10.1109_jlt.2020.3003561/content.md`（receipt 冻结的 shared canonical；禁止使用 worktree 内同 DOI 不同哈希副本）；JLT 2020，arXiv-LaTeX front matter缺失由source title+metadata DOI闭合。
- **贡献/方法**：35-layer propagation+AO产生`rho,phi`时序；digital AGC+second-order DPLL捕获/跟踪residual CFO。
- **实验/Baseline**：20° LEO downlink、10 Gbaud BPSK、100 MHz CFO；CRB/squaring loss/ideal sync与开关对照，无竞争算法。
- **结论/关系**：1.4 ms capture；fading稳定门槛约+5 dB，BER 1e-4 penalty 2.3 dB；C4 physics。
- **细节**：AO 5 kHz；`BL=5 MHz,K1=1.3e-3,K2=6.7e-4`；ideal timing。
- **适配/代码/验证**：适配transfer contract，不适配FSTS/多lag；代码未报告；preflight PASS。
- **证据状态**：AO/DPLL数字=FACT；condition影响lag=INFERENCE；target failure=UNKNOWN。

| 7子表 | 提取 |
|---|---|
| 输入 | BPSK I/Q、AO后rho/phi、100 MHz residual CFO |
| 输出 | AGC gain、DPLL phase/frequency correction；非 action |
| 目标 | reward=N/A；lock time、phase variance、critical SNR、BER |
| 假设 | coarse Doppler done、ideal timing、single 20° realization |
| 架构 | NN=N/A；AO→I/Q→AGC→DPLL→detector |
| 适配 | C4 physics；不是FSTS comparator |
| 本文问题 | 具体✅、产出✅、近期算法baseline❌、量化✅=3/4 |

| 通信参数 | 值 |
|---|---|
| 链路/调制/速率 | 20° LEO-ground；BPSK；10 Gbaud/10 GHz loop |
| CFO/phase | residual 100 MHz；atmospheric phase coherence~1 ms |
| channel/AO | HV/ITU-R；Cn²参数表；AO 5 kHz、mode91；无diversity |
| 完备性 | V/V'/U=`2/2/1`；无seed/error bar/competing algorithm |

### [L05] Joint Physical Layer Frame Optimization and Carrier Synchronization for Satellite Communications

- **DOI/来源**：`10.1109/TVT.2022.3218937`；**源路径**：`papers/doi/10.1109_tvt.2022.3218937/content.md`；TVT 2023；adapter receipt指向2026-08-09 JSON。
- **贡献/方法**：OG-PSAM frame rule、PFPE/M-PFPE、`AC1→AC2→multi-block CC` stepwise CFO。
- **实验/Baseline**：satellite uplink AWGN；QPSK、LDPC+16QAM/SCMA/GMSK；SFPE/S-PSAM/P&R/M&M、DA CRB/no-CFO。
- **结论/关系**：OG geometry改善RMSE/BER；stepwise correlation是C3 ceiling，非coherent-FSO竞品。
- **细节**：AC1 range half symbol rate；AC2/CC逐级收窄；PFPE impact factor `n` 管range/self-noise。
- **适配/代码/验证**：适配prior-art ceiling，不证明target；代码未报告；byte-identical/title/DOI PASS。
- **证据状态**：stepwise AC+CC=FACT；claim-boundary=INFERENCE；target failure/novelty/Go=UNKNOWN。

| 7子表 | 提取 |
|---|---|
| 输入 | PSAM pilot/data、symbol-rate AWGN samples、pilot AC/CC |
| 输出 | TD/CFO/PO/data estimates；非 action |
| 目标 | reward=N/A；CRB/RMSE/MSE/BER/range/overhead/complexity |
| 假设 | AWGN、高SNRapprox、accurate timing、soft-feedback stats |
| 架构 | NN=N/A；frame→mod removal→stepwise CFO+PFPE→decode |
| 适配 | C3 ceiling；RF/AWGN不外推FSO |
| 本文问题 | 具体✅、产出✅、近期强baseline❌、量化✅=3/4 |

| 通信参数 | 值 |
|---|---|
| 场景/调制/采样 | satellite uplink；QPSK/16QAM/SCMA/GMSK；symbol-rate |
| training/CFO/SNR | OG/S-PSAM多block；normalized CFO；Eb/N0 sweep |
| channel/diversity/AO | AWGN；turbulence/diversity/AO=N/A |
| 完备性 | V/V'/U=`2/2/1`；massive trials未给次数/seed/CI |
