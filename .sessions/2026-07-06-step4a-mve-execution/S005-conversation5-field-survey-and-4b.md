# [S005] 对话 5 — Step 5 田野调查 + 4b Go + Step 6 设计 + Step 7 实现

> 2026-07-06 | GW Step 5 + Step 4b + Step 6 + Step 7 | 状态: GW 全闭合（待用户拍板下一步）
> 2026-07-06 续接（用户两次授权"接着做" → 进 Step 6 设计 + Step 7 实现）

## 目标

执行 H005 三步 + 用户两次授权后进步骤 4-6（Step 6 设计 + Step 7 实现）：
1. 报到 + 框架重读 + handoff 3 条事实核查
2. 派子 agent 补 Step 5 田野调查（gw-validate Step 2，≥10 篇）
3. 做 4b（C/E 维度）补完 feasibility_report.md + Go 决策
4. Step 6 仿真器设计（用户授权"接着做"后，写 simulator-design.md，守 FR-12）
5. Step 7 实现（用户再次授权"接着做"后，子 agent 搭建 + 主实验，守 §4.5 MVE 一致性）

## 记录

### 步骤 1：报到 + 框架重读 + handoff 验证

session-governance Trigger 1（报到）+ Trigger 5（收 handoff）。

**报到确认**：当前专题 active，13 不变量已读，D001-D005 + D-S5-01 决策已知，依赖专题（problem-driven-redirection + cut-pattern + deep-read）3 个均稳定，范围未违反"明确不含"。voice.md 未建。profile 第 7 次"急于推进"防线激活——防线是守 3 步上限 + 每步 grep 核查 + 不在 4b Go 前写论文。

**Handoff 3 条关键声称核查全 PASS**（Trigger 5）：
- feasibility_report.md Go 决策：PASS（`projects/simulation/feasibility_report.md:148` "决策:Go（D005）"）
- DA ML 选定 FR-15 目标 baseline：PASS（`projects/simulation/decision_log.md:11-13` D-S5-01）
- MVE fair gain 数字：PASS（`_mve_results.json` json.load 提取 AWGN +0.7041511 / weak +1.1985019 / moderate +1.9219109 dB，与 handoff 引用一致；strong=None 符合"物理不可达"）

**框架文件重读**：gw-validate.md Step 2（田野调查 ≥10 篇 abstract 扫描）+ gw-feasibility.md §4b（C/E 维度）+ groundwork.md Step 6 入口（gw-experiment.md §sim）+ TL-21（确定性 grep）+ TL-23（验证完再写文档）。

### 步骤 2：派子 agent 补 Step 5 田野调查

子 agent（general-purpose，agent_001b1236）执行 gw-validate Step 2。守 AGENTS.md 主对话严禁 WebSearch → 子 agent 用 `tools/search` 脚本。

**执行**：5 个 query × --top 15，活跃源 S2+OpenAlex（Exa 额度耗尽，SerpAPI/Tavily 未装，Q2 FSO 专用 query 自动路由纯 web 源返回 0 已用 Q4 补救）。51 篇去重 → 18 篇载波同步相关（其余为 GNSS/语音增强/声学 TDE/RIS/UWA/OFDM-WLAN CPE 噪声）。

**Baseline 频率统计**（田野样本 N=18）：
- NDA-ML / M-th-power 升幂：4 篇（Du'25=B11, Rice'22, Tang'24 OML, Brannstrom'05）— 领域共识
- **BPS / 2S-BPS（Blind Phase Search）：2 篇显式对比**（Diniz'19, Blatter'25）— 光纤 CPR 主流基准
- VV CFR：1 篇（Wang'24 JPHOT，精确匹配本项目调制+噪声类）
- pilot-aided / DA-ML：2 篇核心方法（Zhang'12, Temga'14）— 领域共识（非最高频显式基准）
- Kalman 族：3 篇（Sun'20 星地, Li'24, X.Tang'23）— 星地光场景高频
- PCA-based CPR：3 篇作为方法（Diniz'19, Li'24, Tang'24）— 现代 NDA 方法簇
- Gardner TED / 频域 CW pilot / Diff-4th：0 显式 — 田野罕见 → 可能非本子领域共识

**关键发现**：
1. **DA ML / pilot-aided 部分确认**：pilot-aided 出现 2 次作核心方法，但田野显式基准最高频是 BPS（光纤 CPR）。DA-ML 作为 NDA-ML 天然对照的逻辑仍成立（B11 锚方法 Wang'22 单正弦 ML + B11 本体均在田野命中 = 交叉验证通过）
2. **场景外推受限**：田野主要落 fiber QAM + 星地/星间 QPSK；精确匹配"单载波 M-APSK + Wiener PN"仅 2 篇（B11 + Wang'24 VV）
3. **3 个候选补充**：BPS（光纤主流，主面 QAM 非 M-APSK）/ PCA-based CPR（QAM 方法簇）/ Kalman 族（星地光高频）

**主线判断**（守 TL-23 + D005 务实路线）：
- BPS 是光纤 CPR 主流基准 ≠ 我们场景的强制 baseline。BPS 主面 square-QAM + fiber，我们是 (8,8)-16APSK + 星地湍流，架构不同。子 agent 自标"BPS 主要面向 QAM 非 M-APSK，场景不同"。
- **不应把 BPS 强加为 FR-15 目标 baseline**——会变成 profile 第 7 次"急于用严标准砍"的反向（急于用宽标准加 baseline 自找麻烦）。
- DA ML 选定逻辑仍成立：①NDA-ML 天然对照（NDA vs DA 是载波同步二分法，方法学逻辑不靠田野频率）②pilot-aided 近最优 ③MVE 已验证赢之。
- BPS 补进评估表为候选补充行（优先级中，备注场景不同作迁移对比二级基准）。

**置信度**：维持中高（不升级，因田野未把 DA-ML 当高频显式基准；不降级，因天然对照逻辑成立）。

**更新 decision_log.md D-S5-01**：补完田野调查段（替换"待办"）+ 评估表加 BPS 候选补充行。

### 步骤 3：做 4b（C/E 维度）补完 feasibility_report.md

分析性维度（守 TL-23 验证完再写——本轮 4b 是分析不需额外验证，分析完直接写）。引用 MVE 数字守 TL-21 用 Python json.load 提取（已在步骤 1 handoff 验证时提取）。

**C 维度（仿真条件可行性）4 项全 ✅**：
1. ✅ 仿真环境支撑核心方法（MVE 跑通，fair gain 0.704-1.922dB）
2. ✅ 差异信号足够大（BER 跨 SNR 降 ~2 数量级：AWGN 0.187→0.002，strong 0.40→0.024；N=102400 统计涨落 <0.1dB）
3. ✅ 含 NDA-ML 擅长特征（频谱效率维度 pilot overhead 真实能量代价 + deep fade 鲁棒性维度 GG 块衰落）
4. ✅ 无"过于平滑"预警（三重独立随机源：GG 块衰落 h + Wiener PN + Doppler CFO；BER 曲线陡峭非假象）

**E 维度（资源/风险比例）3 项全 ✅**：
1. ✅ Baseline 代码全自实现良好（DA ML + NDA-ML + oracle + VV CFR 都在 common/）
2. ✅ 时间投入与贡献成比例（Step 6~1 对话 + Step 7~2-3 对话，贡献=形态 A+C 双增量，会议级别够格）
3. ✅ 失败兜底充分（形态 A 独立成立 AWGN +0.704dB + 形态 C weak/moderate buffer ≥0.5dB + 次优成果可回收）

**4b 决策：Go**（D-4b-01，C/E 无致命）。更新 feasibility_report.md C/E 段 + Go/No-Go 段 + frontmatter。

### 步骤 4：Step 6 仿真器设计（用户授权"接着做"后）

用户确认"接着做" = 授权进 Step 6（仿真器设计，gw-experiment §sim）。守边界：Step 6 只做**设计文档**不进 Step 7 实现（那是下个对话）。守 FR-12（MVE→Formal 架构差异门控）+ TL-23（基于已验证 MVE 数据不脑补）+ TL-26（参数溯源）。

**先核查参数来源**：读 SC-NDA-ML-MVE-SPEC + `_time_domain_crlb.py` + MVE 脚本 `sc_nda_ml_mve.py`，确认所有参数（N_DFT=256/M0=8/CLW=500kHz/HD-FEC=3.8e-3/pilot sp=4/BAUD=25GBaud 等）都标 B11 行号溯源。注意发现：params.py 是旧 QPSK 设定（SystemParams 等），无 B11Params；B11 参数实际在 MVE 脚本/`_time_domain_crlb.py` 内联。SPEC.md §1-7 也是 QPSK 旧设定（BLOCK=100/pilot 5%/R_SYM=2.5Gsps），跟 NDA-ML MVE 参数（BLOCK=256/pilot 25%/BAUD=25GBaud）不一致。**设计决策**：SPEC 补 §8 NDA-ML 段不替换 §1-7（双套参数共存隔离）。

**写 `projects/simulation/simulator-design.md`**（9 节）：
- §0 设计目标（MVE 工程化，非重写）
- §1 **[FR-12] MVE vs Formal 架构差异对照表**（7 维：动作空间/决策粒度/对比范式/奖励语义/先验强度/统计稳健性/实现独立性）。主路径全"否"（Formal 与 MVE 一致）→ **通过 FR-12 门控可进 Step 7**。两个可选消融（跨块 KF 跟踪 FR-18 预判 + BPS 迁移对比）不影响主路径 Go
- §1 含 [FR-18] 环境简化偏差记录（来源 `_mve_results.json` fr18_competition_analysis）
- §2 模块清单（11 模块：6 复用 common/ + 5 新实现。核心算法 NDA-ML/DA ML 全复用无新算法）
- §3 关键参数表（全溯源，[ASSUMPTION] 1/30 ≈ 3.3% < 30%，仅 5 seed 统计约定）
- §4 验证标准 5 类（解析/统计/退化/自相关/MVE 一致性 — §4.5 是 Formal 独立实现的正确性锚点）
- §5 实验矩阵（主实验 4 场景 + 辅助 AIR/KF 消融/BPS 迁移 + 明确排除 OFDM/STO/decision-feedback）
- §6 奖励函数 N/A（估计类方法非 RL）
- §7 目录结构（simulator/ + baselines/ + results/ 新建，explore/ 保留）
- §8 设计风险（独立实现 bug/多 seed 时间/KF 消融翻转/SPEC 双套参数）
- §9 用户确认清单（gw-experiment §sim [MUST]）

**FR-12 门控判定**：主路径全"否" → 通过。Step 7 实现前需用户确认设计 + 4b Go + Step 5 baseline。

### 步骤 5：Step 7 实现（用户再次授权"接着做"后）

用户再次确认"接着做" = 授权进 Step 7。我自决默认值回答 4 个确认项（profile 委托技术判断）：①5 seed（设计默认）②消融后置先做主实验 ③SPEC §8 实现完用实际参数补 ④模块清单按设计 11 模块。

**先勘察 common/ 接口**：grep 确认 `_time_domain_crlb.py` 从 common/ 导入（generate_shared_realization_apsk / nda_ml_recovery / da_ml_recovery / m16apsk_* 等），它新增的只是 AWGN 信道 + 逐块评估 + B11 参数。MVE 脚本是其薄包装。设计文档"6 复用 common/"判断成立。

**派 executor 子 agent 做 Part A**（gw-experiment §impl [MUST] 子 agent 执行）：写 `simulator/{sc_nda_ml_sim.py(648行), fair_comparison.py(157行), _b11_params.py(106行)}` 独立实现（核心算法全从 common/ 导入，import 审计确认不 import explore/）+ §4.5 MVE 一致性验证。

**主线独立核查（守 TL-21/23，不信任子 agent 报告）**：
- json.load `_consistency_check.json`：87 BER 值全 rel_err=0.0（bit-exact），formal_nda=0.18678466796875 == mve_nda=0.18678466796875（完全相同双精度数）
- import 审计：grep 确认 simulator/ 三文件无 `import explore` / `_time_domain_crlb`，仅注释引用
- seed 核查：_b11_params.py SEED_AWGN=20240701 / SEED_TURB0=2000 == MVE sc_nda_ml_mve.py:53-54
- 作弊核查：git status `_mve_results.json` 未改（干净）+ mtime 14:23 早于 _consistency_check.json 15:51（对照基准先存在）

**Part A 通过核查**。子 agent 报告自相关 h lag-1=0.9902 超阈值——诊断后判定**非 bug 是 GG 块内恒定物理特性**（块间 lag-100=0.0164 证独立）。修订 simulator-design.md §4.4（填实测 + 块间阈值注解）。

**派 executor 子 agent 做 5 seed 主实验**：种子策略 AWGN `+i` / 湍流 `+i·N_BLOCKS`（保 per-block seed 互斥防 CI 被人为缩小）。150 运行 75s。

**主线核查主实验**：json.load `_fair_gain_summary.json`：per_seed_gain_db[0]=0.7041511552 == MVE 0.704（bit-exact 复现）；AWGN mean=0.776 CI [0.667,0.885] MVE 0.704 落内 ✅；weak/moderate/strong 同理全 PASS。

**写 `baseline_report.md`**（Step 7 出参）：§0 状态摘要 + §1 Baseline 复现状态（templates B1 格式，DA ML FR-15 目标 ✅ + oracle 上界 + NDA-ML 提出方法）+ §2 仿真环境验证（Part A 清单全 ✅）+ §3 主实验细节（5 seed per-seed + avg-curve 两法互证）+ §4 已知债务消融后置 + §5 Step 7 质量门槛 + §6 下一步。

**GW Step 4a/4b/5/6/7 全闭合**。下一步=用户拍板（进 Contract / 补消融 / B7 / B3）。

## 决策引用

- **D-S5-01**（项目级，田野调查补完）：DA ML 维持选定 FR-15 目标 baseline，BPS 补候选补充行，置信度维持中高（S005 补完）
- **D-4b-01**（项目级，新建）：4b（C/E 维度）Go 决策，C/E 无致命，继续 Step 6
- **simulator-design.md**（项目级，新建）：Step 6 仿真器设计规格，FR-12 门控通过（主路径全"否"）
- **baseline_report.md**（项目级，新建）：Step 7 出参，§4.5 MVE 一致性 bit-exact（87 BER 值全 0.0000%）+ 5 seed 主实验全赢 DA（AWGN +0.776±0.088 / weak +1.529±0.321 / moderate +1.712±0.250，strong 工作区 grand mean +2.515±0.555）
- 无专题级新决策（D005 仍是最高 Go 判据，4b/Step 6/Step 7 是其下游工程实现）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Step 5 + 4b 是 4a Go（D005）后的合法阶段推进（FR-22 GW 流程门控）。未跳框架（没进 Contract/Execute），未救 6 次 Kill，未改框架文件，未污染 common。

## 后续

1. **用户拍板下一步方向**（GW Step 4a/4b/5/6/7 全闭合后）：①进 Contract 阶段（落假设+信号+success_signal）②补消融（跨块 KF + BPS 迁移，论文写作前）③B7 Gardner TED FOE MVE（并行第二候选）④B3 架构决策（多孔径阵列 vs 单链路）
2. **消融后置**：跨块 KF（FR-18）+ BPS 迁移（田野调查）+ decision-feedback DA ML（债务①）—— 主实验已 PASS 不卡，论文写作前补
3. **SPEC.md §8 NDA-ML 段**：Step 7 后用实际参数补（当前 QPSK §1-7 与 NDA-ML 新参数双套共存）

**用户新约束**（本轮新增）：除用户要求停下来记录外，不需要写交接。本轮收尾不写 H006。
