# Topic Index: Step 4a 维度 D MVE 执行

> slug: 2026-07-06-step4a-mve-execution
> status: active | created 2026-07-06 | last_updated 2026-07-08（S007 续接：blit+download 下 3 篇 baseline 全文 + subagent 精读。#15/#17 blit ieee 下成功校园网认证，#16 OE 6月已下。3 subagent 并发精读：#15 JPhoto 升级最强并列 baseline[(8,8)-16APSK + NDA M₀=8 次幂同框架，差异 LMMSE vs ML + 无湍流]，#16 OE 场景参照[方法异类 DA-FOE + 公式抓取不全]，#17 TVT 理论锚[DA&NDA CRB 推导]。精读后发现结构性缺口：(8,8)-16APSK+NDA-ML+星地FSO+近年+严格Trans 五者交集 baseline 未召回，物理事实非检索不全。详见 S007 续接段）

## 专题定位（一句话）

承接上游专题 S031 排优先级 + 切法地图专题参照系，对 B11/B3/B7 三个 Conditional Go 候选走 Step 4a 维度 D MVE 实证（FR-21 oracle 上界前置门控 + MVE 闭合）。**是 Step 4a 实操（判 Go/Kill），不是参照系校准**——跟切法地图专题（中性提取不判 Go/Kill）定位正交。

## 原始目标（冻结，不可修改）

对上游专题 S031 排出的前几名 Go 候选（主线建议 B11/B3/B7）走 gw-feasibility Step 4a 维度 D：
1. **FR-21 oracle 上界前置门控**（先算 CRB 下界，<0.5dB 直接 Kill 不跑 MVE）
2. **TL-20 理论预期 + MVE 闭合**（上界 ≥0.5dB 才跑 MVE，验证候选方法在星地湍流信道下仍达标）
3. **FR-18 竞争格局 + FR-12 MVE→Formal 架构差异门控**（加湍流后 baseline 是否变强 / MVE 架构 vs 正式架构差异）
4. **守 D005 务实路线**（Go 判据=赢传统 baseline 几 dB，会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格；FR-21 降为参考不卡死）

**冻结边界**：
- 只对 B11/B3/B7 三个 Go 候选（上游 S031 排序）做 MVE，不回头救 6 次 Kill
- 不跳框架（FR-22 GW 流程强制门控，当前在 Step 4a 维度 D）
- 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- 不改框架文件（守"先测不改协议"，本轮只验不改框架）

## 范围边界

### 原始目标（冻结）
对 B11/B3/B7 走 Step 4a 维度 D MVE，守 FR-21/TL-20/FR-18/FR-12 + D005 务实路线 + D006 红线。

### 当前范围
- **复用 projects/simulation/common/ 基建**（GG+Doppler+phase noise 信道 + VV/BPS/DPLL/KF 载波恢复，TL-24/TL-13 已制度化）
- **增量扩充 common**：
  - `_modulation.py` 加 M-APSK（8PSK / (8,8)-16APSK / 32APSK / 64APSK + Gray 映射）—— B11+B3 共用
  - `_recovery.py` 加 DA ML（B11 baseline + B3 CPE 子组件）+ NDA-ML（B11 方法）+ Gardner TED（B7 方法 + B3 FOE 子组件）+ FOE（B7 baseline）
  - `_channel.py` 加 generate_shared_realization_apsk（含 CLW/HD-FEC 阈值扩展）
  - `params.py` 加 B11/B7 参数族（CLW 500kHz / 7% HD-FEC / LEO Doppler rate，全标 source TL-26）
- **explore/ 模式**（每候选一子目录）：
  - `explore/b11-nda-ml-sto-cpe/`（B11 NDA-ML STO+CPE 星地湍流迁移 MVE）
  - `explore/b7-gardner-ted-foe/`（B7 Gardner TED 复用 FOE 星地 LEO 适配 MVE）
  - `explore/b3-subsystem-coordination/`（B3 子系统协同联合估计，需先决架构假设）
- **MVE 通过后转 experiments/**（正式实验区）

### 明确不含
- ❌ 不回头救 6 次 Kill（Q1/Q2/Q3/Q8 切入点 2/4B/Q12/Q#-A，D005 诚实重评"大概率没几个能救"）
- ❌ 不回头救 6 次 Kill（Q1/Q2/Q3/Q8 切入点 2/4B/Q12/Q#-A，D005 诚实重评"大概率没几个能救"）
- ❌ 不改框架文件（gw-feasibility.md / TL-26/27 等，守"先测不改协议"）
- ❌ 不跳框架（FR-22：当前在 Step 4a 维度 D，禁跳到 Contract/Execute）
- ❌ 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞，7 边界只标不砍）
- ❌ 不污染 common（explore 阶段探针不直接进 experiments，MVE 通过才转正）

### 范围变更记录
- **2026-07-06 S001 标准校准**（用户质疑"十几个 Q 都不行是不是我考虑不周"触发）：①B1-Q1 不预设 Kill（不变量 11）②B9-Q1 不锁载波同步主题（不变量 12）③D006 边界 7 次升优先级（不变量 13）。**这不是违反不变量，是校准 S031 评估时过严的标准**——S031 用了期刊级标准（FR-21<0.5dB 砍 + A1 严查 + 主题锁窄）判会议级候选，是 profile"急于用严标准砍"的新表现。校准后范围扩大：B1-Q1/B9-Q1/D006 边界 7 次都进 MVE 评估范围（原本只 B11/B3/B7 三个）

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（参考同门 2-4dB，会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 降级为参考不当 Kill 门（FR-21 <0.5dB 不再自动砍，但连传统 baseline 都赢不了仍不行）
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），任何"试新方法/新方向"动作必须先回答"在 GW 哪一步"——B11/B3/B7 MVE 是 Step 4a 维度 D 合规动作，禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+oracle 上界<0.5dB+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具禁当 Go 判据
5. **切法地图是参照系不是答案**：判 Go/Kill 时引用切法地图模式（饱和池场景迁移/稀池独占/联合建模 dB 空间），但不直接搬"切法地图说这个好"
6. **profile 第 8 次"急于推进"防线激活**：MVE 执行主线极易在压力下"先跑起来再说"跳过 oracle 上界前置。**防线：每候选必须先算 CRB 下界，<0.5dB 直接砍不跑 MVE（守 TL-27 / FR-21），≥0.5dB 才写 MVE 脚本。**
7. **TL-26 参数溯源强制**：MVE 每个关键物理参数（Cn²/σ²/线宽/CLW/Doppler rate/FEC 阈值）必须标文献来源（Paillier / sat.1553 / Fernandes / B11/B7 锚论文），禁"为了让方法有用"拍参数
8. **TL-13 共用同一信道实现**：B11/B7/B3 必须从 `common/_channel.py` 导入，禁自建信道（防仿真不公平）
9. **TL-20 先建理论预期**：MVE 跑之前必须写明理论预期表（每湍流等级预期 dB + 量化锚点 + 偏离即停查代码），仿 n1-pcs-gain MVE-SPEC.md §2 模板
10. **核查机制中性双向**：MVE 出 +2dB 先别写进论文（TL-23 验证完再写），主线独立 grep 核查执行对话报告 + 子 agent 产出（不信任报告）
11. **【S001 标准·校准 1，INVARIANT】B1-Q1 不预设 Kill**：FR-21 oracle 上界算出来 <0.5dB **不直接砍**，降级为"会议级别下 +1dB + sat.1553 L440 open problem 自报证据链（~5% 最强）+ [60] Leven 理论锚背书"的综合判断，**用户拍板**。校准依据：D005 已说 FR-21 降为参考不卡死，但 S031 评估 B1-Q1 时我手又紧（用了期刊级标准判会议候选）；同门范式 2-4dB 区间下沿 +1dB 在会议级别下够发，不应单凭 oracle 上界一刀切
12. **【S001 标准·校准 2，INVARIANT】B9-Q1 不锁"载波同步改进"主题**：放开"处理技术宽义"（上游 S007 用户原话"处理技术是宽义非仅基带 DSP"），DRE（TX 侧量化噪声整形）+ 自相干绕开载波同步是合法处理改进。会议级别下 ~3dB @ 3PNOB + 自相干"绕开而非赢"独特叙事 + 切法地图稀池 2 独占孤点（0/7 follow 意味独占空间大）够发。校准依据：S031 判 B9 Pivot 的"baseline 非传统载波同步"用了载波同步主题锁窄，跟 S007 处理技术宽义矛盾；A1 归属（DRE 是 B9 论文自己贡献）用同门范式对标（搬星地+加湍流是合法场景迁移），不用期刊范式
13. **【S001 标准·校准 3，INVARIANT】D006 边界 7 次升优先级为"潜在大论文一致性研究方向"**：`B3-Q3 / B6-Q2 / B7-Q2 / B9-Q3 / B10-Q2 / B11-Q2 / B12-Q3` 7 个"前馈不撞/环路 TF 联合建模则撞"候选：①7 次重复 = 文献实证强（非孤证）②跟块 A/B/C/D（Q11/Q12 Paillier 分治）延续 = 一致性故事 ③**其他候选都是单点，这 7 个连起来是大论文一章的叙事骨架**。从"单独评估"升为"B11/B7 单点 MVE 跑完立刻评估这 7 个的联合叙事"。校准依据：S031 标"单独评估"=延后处理，但延后=可能漏掉最有大论文价值的方向；D006 证伪的是环路 TF 联合建模，**前馈层合法**，7 候选都在前馈层不撞 D006

## 标准校准段（S001 新增，防 MVE 执行时手又紧）

> **校准背景**：用户质疑"十几个 Q 都不行，是不是我考虑不周"。主线诊断：S031 评估时用了期刊级标准（FR-21<0.5dB 砍 + A1 严查 + 主题锁载波同步）判会议级候选，是 profile"急于给方向性结论"的新表现——这次是"急于用严标准砍"。校准后颗粒无收概率从 ~30-40% 降到 ~10-15%（同门范式在这个领域发了学位论文，证明物理上有可发的增量——若推完不行而同门行了，更可能是标准差而非物理差）。

**校准后 MVE 执行标准**：
- **Go 判据**：赢传统 baseline（参考同门 2-4dB 区间，会议级别下沿 +1dB 也够）+ 切法地图路径清晰 + 不撞 D006（前馈层合法）
- **Kill 判据**：A0 §1/§2/§3/§6 致命（问题-方法不匹配 / 简单方法够用 / 跨域无先例 / 简单规则覆盖 ≥90%）+ MVE FAIL（核心假设不成立）+ **FR-21 oracle 上界 <0.5dB 降为参考不卡死**（需联合叙事证据链综合判断，用户拍板）
- **A1 归属判据**：用同门范式对标（夏兆宇/王培森/李兀祺——"借方法+场景适配+多维协同"是合法学位论文贡献），不用期刊范式（"提出全新方法"）
- **主题边界**：处理技术宽义（S007：调制/复用/检测/编码/FEC/交织/信道估计/均衡/同步/信道建模/AO 算法），不锁"载波同步改进"

## 其他结论（普通技术决策）

### 仿真基建盘点（S001 确立）

**已有**（projects/simulation/，成熟）：
- `common/` 7 模块（`_channel/_modulation/_recovery/_kf/_equalizer/_experiment/_config`）
- 信道：`gg_block`（Gamma-Gamma 块衰落）+ `doppler_phase`（Doppler+phase noise）+ `generate_shared_realization`
- 调制：QPSK / 16-QAM + Gray 映射 + `ber_eval`
- 载波恢复：VV / BPS / DPLL / KF（4 方法）
- params.py：pydantic + source_type + audit_flag（TL-26 已制度化）
- explore/ 模式：`*-MVE-SPEC.md` 契约 + 脚本 + results.json（n1/mcs 两个先例）
- archive/：旧代码禁用（TL-24）

**缺口**（本轮扩）：
- `_modulation.py` 缺 M-APSK（B11+B3 需要）
- `_recovery.py` 缺 DA ML / NDA-ML / Gardner TED / FOE（B11 方法+baseline + B7 方法+baseline）
- params.py 缺 B11/B7 参数族（CLW / HD-FEC / LEO Doppler rate）

**最大工程红利**：搭一次共享基建（M-APSK + ML 估计器 + 星地湍流扩展），3 候选共用

### 组织方案（S001 确立）

**目录结构**：
```
projects/simulation/
├── common/                          # 共享基建（增量扩充）
│   ├── _modulation.py               # ➕ M-APSK
│   ├── _recovery.py                 # ➕ DA ML / NDA-ML / Gardner TED / FOE
│   └── _channel.py                  # ➕ generate_shared_realization_apsk
├── params.py                        # ➕ B11/B7 参数族
├── explore/                         # MVE 阶段（每候选一子目录）
│   ├── b11-nda-ml-sto-cpe/          # ➕ 新
│   ├── b7-gardner-ted-foe/          # ➕ 新
│   └── b3-subsystem-coordination/   # ➕ 新（最后开，架构假设需先决）
├── experiments/                     # MVE 通过后转正
└── SPEC.md                          # ➕ 补 B11/B7 SPEC 段
```

**关键规则**（防乱）：
- TL-24 不引用旧/独立脚本结论（已制度化）
- TL-13 共用同一信道实现（已制度化）
- TL-26 参数溯源（params.py source_type/audit_flag）
- TL-27/FR-21 oracle 上界前置（新增：`_crb_lower_bound.py` 先跑，<0.5dB 不写 MVE 脚本）
- TL-20 先建理论预期（MVE-SPEC.md §2 必填）
- FR-18 竞争格局分析（MVE-SPEC.md 必填"加湍流后 baseline 是否变强"段）
- explore 隔离（新候选不污染 experiments，通过才转正）

## 已确认决策

- **D001** baseline 复现优先于增量评估（方法论纠偏）：已发表 baseline 必须先复现立住再做增量评估，FR-21 oracle 上界是评估"我们自己的增量方法"的上界不是评估已发表 baseline 的（2026-07-06 新建）
- **D002** B11 角色重定位 = 理论参考（非直接对标 baseline）：B11 在论文里定位为"NDA 升 M₀ 次幂 + ML"思想源头，不作直接对标 baseline。我们的增量 = 单载波时域下的 NDA-ML 改进（架构诚实，贴星地主流单载波）。（2026-07-06 新建）
- **D003** nda_ml_recovery 两 bug 修复：加 assume_df_zero 参数（B11 行 33 场景跳 FFT-df）+ resolve_m16apsk_blockwise（逐块解 M₀-fold 模糊）。（2026-07-06 新建）
- **D004** 单载波时域 NDA-ML 改进 GO_MVE + 公平对照框架确立（2026-07-06 新建）：
  - **D004-a** CRB 层：CRB_NDA/CRB_DA ≈ N_p/N = 1/4（M₀² 严格相消），NDA-ML 理论下界优于 DA ML
  - **D004-b** 公平对照 gain @ HD-FEC：AWGN +0.70 / weak +1.20 / moderate +1.92 / strong 物理不可达但 NDA 全工作区赢（形态 A+C 双增量叙事）
- **D005** SC-NDA-ML MVE PASS → Go（2026-07-06 新建）：公平对照 fair gain @ HD-FEC 实测 AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB（SPEC §5 Go 门），strong 物理不可达但工作区(≥15dB)全赢 DA（per-point +1.19~+2.62dB）。TL-20 预期 5 项全 PASS 0 DEVIATION。NDA-vs-oracle gap 全 <3dB（0.38/1.49/1.97/2.58dB，升幂实现正确）。主线独立 grep 核查 6 项 MVE 纪律全落实（per-block h / 公平对照 / 两阶段 FOE / resolve blockwise / 共用信道 / N≥1e5）。进 Step 5（Baseline 选定：DA ML pilot sp=4 锁 FR-15 目标 baseline，NDA-ML 锁提出方法）

## 悬而未决

1. **用户拍板下一步方向**（GW Step 4a/4b/5/6/7 全闭合后）：①进 Contract 阶段（落假设+信号+success_signal）②补消融（跨块 KF + BPS 迁移，论文写作前）③B7 Gardner TED FOE MVE（并行第二候选）④B3 架构决策（多孔径阵列 vs 单链路）
2. **消融后置状态**：跨块 KF（FR-18 预判 cross-over 移动）+ BPS 迁移对比（田野调查候选补充）+ decision-feedback DA ML（债务①）—— 都标"论文写作前补"，主实验已 PASS 不卡
3. **SPEC.md §8 NDA-ML 段补完**：Step 7 后用实际参数补更准（当前 QPSK §1-7 与 NDA-ML 新参数双套共存）
4. **B11 作理论参考的具体叙事方式**：论文里如何引用 B11（背景 / 思想源头 / 对比锚？）待写作阶段定
5. **债务提示**：①单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等，论文写作前视情况补对照 ②B11 genie-aided 解卷绕非可实现，MVE/Formal 用 resolve_m16apsk_blockwise（非 oracle）已落实 ③田野调查 BPS 候选补充行（光纤 CPR 主流基准，主面 QAM 场景不同），作迁移对比二级 baseline ④MVE 脚本是 `_time_domain_crlb.py` 薄包装，Formal 仿真器已独立实现（simulator/，不复用 explore 探针，§4.5 MVE 一致性 bit-exact 验证）⑤simulator-design.md §4.4 自相关 h lag-1=0.99 是块内恒定物理特性（块间 lag-100=0.0164 非平滑假象），阈值分块内/块间

## 当前位置

**🟢 S007 续接：blit+download 下 3 篇 baseline 全文 + subagent 精读（2026-07-08）**：用户要求"把那几篇用 blit 下下来然后 subagent 精读"。**下载**：#15 JPhoto + #17 TVT 用 blit --source ieee --download 下成功（IEEE 校园网认证通过，PDF 首页标题验证 PASS），移到 papers/doi/ 标准路径 + tools/convert 转 markdown；#16 OE 用 download --doi 发现 6 月已下（firecrawl_scrape）。**精读**：3 个 subagent 并发各 ≤500 词结构化摘要。**主线集成判断**：#15 JPhoto **升级最强并列 baseline**[(8,8)-16APSK + NDA M₀=8 次幂框架跟我们完全同款，差异只在权重 LMMSE vs ML + 信道无湍流，它已把 DA-ML PE 作对照跟我们 baseline 同款]；#16 OE 降级场景参照[调制方阵 16QAM + 方法 DA-FOE 异类 + content.md 公式全空复现受限]；#17 TVT 定位理论锚[纯 AWGN RF 卫星，但 DA&NDA CRB 推导跟我们公平对照框架理论契合]。**结构性缺口**："(8,8)-16APSK + NDA-ML + 星地 FSO + 近年 + 严格 Trans"五者交集 baseline 检索未召回——物理事实（领域窄）非检索不全。COMPARISON_REFS.md §一E 三篇评价全改精读后结论 + §三盘点加第 4 条缺口说明。下一步=简报重写（用户定时机）/ TODO-4~8 / 等老师定目标期刊层级。

**（前 S007 主体 2026-07-07）**：REVIEW_NOTES §三 TODO 收尾执行。任务1 SD-FEC 重跑：HD-FEC sanity bit-exact 0.0000%，25% SD-FEC 2e-2 档三场景全正 CI 下界>0，post-FEC 1e-7 物理不可达；任务2 检索 3 篇近年 Trans baseline（Crossref 全 VERIFIED，近年+严格Trans 21%→29%）；任务3 TL-20 预期表更新（AWGN +1.351 超旧预期 +0.8 合理论证）。

## 进展线索

- **S001** 专题开题 + 仿真基建盘点 + 组织方案定稿（2026-07-06）
- **H001** 交接给新对话（基建扩充 + B11 oracle 上界）（2026-07-06）
- **S002** 执行 H001：基建扩充完成 + B11 路径重定位方案 C（单载波时域 NDA-ML 改进）（2026-07-06）
- **D001** baseline 复现优先于增量评估（方法论纠偏）（2026-07-06，S002 新建）
- **D002** B11 角色重定位 = 理论参考（2026-07-06，S002 新建）
- **D003** nda_ml_recovery 两 bug 修复（2026-07-06，S002 新建）
- **H002** 交接给新对话（单载波时域 NDA-ML 改进 MVE-SPEC 设计）（2026-07-06）
- **S003** 执行 H002：时域 CRLB GO_MVE + 信道校准修复 + SC-NDA-ML-MVE-SPEC 写完（2026-07-06）
- **D004** 单载波时域 NDA-ML GO_MVE + 公平对照框架（2026-07-06，S003 新建）
- **H003** 交接给新对话（跑 SC-NDA-ML MVE）（2026-07-06）
- **S004** 执行 H003：SC-NDA-ML MVE PASS Go 判定（2026-07-06，本对话产出）
- **D005** SC-NDA-ML MVE PASS → Go（2026-07-06，S004 新建）
- **D-S5-01**（项目级 decision_log.md）Baseline 选定 DA ML pilot sp=4 = FR-15 目标 baseline（2026-07-06，S004 续接 2 新建；S005 田野调查补完，维持选定，BPS 补候选补充行）
- **S005** 执行 H005：Step 5 田野调查补完 + 4b（C/E）Go 决策（2026-07-06，本对话产出）
- **D-4b-01**（项目级 decision_log.md）4b（C/E 维度）Go 决策（2026-07-06，S005 新建）
- **simulator-design.md**（项目级）Step 6 仿真器设计规格（2026-07-06，S005 续接 Step 6 产出，FR-12 门控通过主路径全"否"）
- **baseline_report.md**（项目级）Step 7 出参（2026-07-06，S005 续接 Step 7 产出，§4.5 MVE 一致性 bit-exact + 5 seed 主实验全赢 DA）
- **S006** D-007 线宽参数真相源统一 + 重跑（2026-07-07，本对话产出）
- **D-007** AWGN 场景重定义（B11 OFDM→单载波）+ 线宽参数真相源统一（2026-07-07，S006 新建）
- **S007** SD-FEC 重跑 + 近年 Trans baseline + TL-20 预期表更新（2026-07-07，本对话产出，3 步收尾执行）
