# Topic Index: Step 4a 维度 D MVE 执行

> slug: 2026-07-06-step4a-mve-execution
> status: active | created 2026-07-06 | last_updated 2026-07-26（D017：激活 B10 source-native adaptive pilot-RLS carrier，T010 待独立审查。）

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
- **D017 当前状态**：T009 的 `BLOCKED_IDENTITY / NONE` 与 A4
  `RETURNED_TO_POOL` 保留；post-T009 remap 已激活
  `B10_SOURCE_NATIVE_ADAPTIVE_RLS_CPR`。T010 必须从 128 contiguous pilot→DD
  原文生命周期重建 fixed B10，identity 过门后同包比较 innovation freeze 与
  adaptive forgetting。仍止于 Step 4a。
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
- **2026-07-26 R002/D017 B10 source-native activation**：比较 B10、C15、B1、
  B9 后，B10 是唯一能在现存 Step 1–3 与可获取全文上直接形成方法包的 carrier。
  - 新范围：只允许 T010 隔离实现 source-native fixed B10、P2 innovation freeze、
    P3 adaptive forgetting、amplitude-only cheap rule 与 task-matched conventional
    B*；不复用 T006 estimator。
  - 退出边界：identity 或方法门失败后不开第二个 B10 repair，优先返回 live Goal
    做 C15 Step 1–3 formalization。
  - 不变边界：不进入 Step 5/Contract/Execute，不改 common/params/paper/owner，
    不恢复 B1/A4/Pilot-Jones/P03/Scout。
- **2026-07-26 V003/D016 A4 carrier return**：T009 在一次有界 repair 后于
  identity gate 停止；独立 verifier 为 `FAIL, P0=4/P1=5/P2=1`。
  - 接受边界：`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED` 与
    `mission_method_delta=NONE`；P1–P3 primary 未运行。
  - 拒绝边界：shared transmitter/pilot 随机、1 MHz 频率不对称、validation
    缺可靠工作区来源且无 FEC crossing；DA 9/9 只作错误 evaluator 下观察，不作
    物理支配或 family Kill。
  - 新范围：A4 返回候选池；不再修当前 evaluator，formal 无 active carrier，
    等待 live Goal campaign remap。
  - 证据闭包：raw/result 位于 gitignored results，且 executor commit
    `8ea886e4…` 的 `git diff --check` 因 8 个 EOF 空行告警失败。
- **2026-07-26 V002/D014 carrier return**：T008 工程测试通过，但
  `KILL_NO_ADAPTIVE_WINDOW_SPACE` 因 no-crossing dB proxy、oracle candidate、
  eval population 与 evidence closure 失败被拒收。
  - 新范围：B1 返回候选池且不再修当前实现；formal 暂无 active carrier。
  - 不变边界：Goal campaign remap 前不运行新科学实验，不进入 Step 5。
- **2026-07-25 V001/D013 carrier switch**：T006 的 source identity、pilot/data
  channel、oracle/eval 与 robust statistics 同时失效，拒收其
  `PROBLEM_SURVIVES_METHODS_FAIL`，但不 Kill B10/B12 family。
  - 原因：B10 source-native probe 失败；唯一 0.6059 dB survivor 的 91.7% 来自
    单个 collapse seed。
  - 新范围：停止 T006 当前修复；B1 已有 Step 1–3 证据，允许 T007 在 Step 4a
    完成固定窗结构门、三种自适应窗和 paired test。
  - 不变边界：不进入 Step 5/Contract/Execute，不改 shared generator，不恢复
    Pilot-Jones/P03/Science Scout。
- **2026-07-25 D012 carrier reactivation**：原始目标的候选范围曾在 2026-07-06
  校准时扩展到 B10-Q2/B12-Q3 等 D006 前馈边界；现正式恢复 B10/B12 已完成的
  Step 1–3 证据，允许在 Step 4a 运行一个 headroom→methods 大包。
  - 原因：Pilot-Jones D066/V040 scoped axis Kill 后需合法换 carrier；B10/B12
    有全文、精读、QAM 方法链和现成 CPR 资产，最符合优先形成方法的目标。
  - 不变边界：不进入 Step 5/Contract/Execute；不改 shared generator；问题
    headroom 不存活时不建设方法。
  - 显式旧决策覆盖：用户已批准 T006 采用 `<0.5 dB` headroom 作为**是否投资方法
    实现**的强门，故 D012 只对 T006 覆盖下方不变量 2/4/6 的“FR-21 仅参考”校准；
    其他历史候选和 D005 叙事不被追溯改写。
- **2026-07-06 S001 标准校准**（用户质疑"十几个 Q 都不行是不是我考虑不周"触发）：①B1-Q1 不预设 Kill（不变量 11）②B9-Q1 不锁载波同步主题（不变量 12）③D006 边界 7 次升优先级（不变量 13）。**这不是违反不变量，是校准 S031 评估时过严的标准**——S031 用了期刊级标准（FR-21<0.5dB 砍 + A1 严查 + 主题锁窄）判会议级候选，是 profile"急于用严标准砍"的新表现。校准后范围扩大：B1-Q1/B9-Q1/D006 边界 7 次都进 MVE 评估范围（原本只 B11/B3/B7 三个）

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（参考同门 2-4dB，会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 通常降级为参考不当 Kill 门。**D012/T006 是用户批准的显式例外**：`<0.5dB` 作为是否投入三个方法实现的强门。
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），任何"试新方法/新方向"动作必须先回答"在 GW 哪一步"——B11/B3/B7 MVE 是 Step 4a 维度 D 合规动作，禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+oracle 上界<0.5dB+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具禁当 Go 判据；T006 的 0.5dB 仍只作 Kill/investment gate，不作 Go 对手。
5. **切法地图是参照系不是答案**：判 Go/Kill 时引用切法地图模式（饱和池场景迁移/稀池独占/联合建模 dB 空间），但不直接搬"切法地图说这个好"
6. **profile 第 8 次"急于推进"防线激活**：MVE 执行主线极易在压力下"先跑起来再说"跳过 oracle 上界前置。**防线：T006 必须先算合法 headroom，CI upper <0.5dB 直接砍不实现方法；≥0.5dB 才进入方法比较。其他候选仍按各自已登记决策执行。**
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
- **D-010** 导师确立 baseline 选取标准（5 条）+ 方向/复现源质量门（2026-07-08 新建）：①同场景星地湍流 ②同类型层级（载波/定时/均衡层）不深入子层 ③不找接近方法当 baseline（VV 同族禁主比）④近年+权威（2022+ Trans）⑤找方向/复现只看够好的（避 letter/仿真不全）。工具链核查：老师"trans 不好检索"对我们不成立（search 搜元数据 venue 全 + blit 下全文），blit venue 硬编码空串缺陷已修。候选框架/skill 更新点已标（groundwork S4-7 / code-quality 矩阵 / tools-guide §2），本轮不改守"先测不改协议"。
- **D-011** A1 参数适配（NDA 块长自适应 K）FAIL（2026-07-08 新建）：自适应-J4 gain vs K16=+0.000dB（退化 always-K16），0/8 点显著赢，oracle 上界仅 -0.474dB 且 -2.46dB 全来自 1000kHz 非主流极端点。3 条失败机制：最优 K 变化范围窄（K∈{8,16,32} K=16 普适 71%）/ 判据层失效（4 判据 ρ<0.6 J4 修正后仍 -0.019）/ 唯一显著点不在主流场景。教训 8-10（"参数随条件变"≠"自适应有空间"需三重检验 / unwrap 对升幂相位不可用第 2 次复发 / 子 agent 映射拟合要核查退化）。
- **D013** T006 科学 verdict 拒收并激活 B1 adaptive phase window（2026-07-25
  新建）：T006 工程 PARTIAL、B10/B12 family UNRESOLVED；T007 先验证最优窗随
  条件变化且不存在普适 fixed N，门过才实现三种 receiver-visible 方法。
- **D014** T008 科学 verdict 拒收并将 B1 返回候选池（2026-07-26 新建）：
  no-crossing dB proxy、oracle candidate、eval population 与 evidence closure
  失败；不作 family Kill，不再修当前实现。
- **D015** Goal campaign remap 激活 A4 deployable adaptive CPR（2026-07-26
  新建）：A4 以 `READY_WITH_BOUNDED_IDENTITY_ADJUDICATION` 进入 T009；先关闭
  common-payload/pilot/ambiguity/deployable-input/strongest-fixed identity，过门后
  同包完成 P1–P3；失败不再开第二个 A4 repair 包。
- **D016** T009 身份裁决失败，A4 返回候选池（2026-07-26 新建）：
  接受 `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED` 与 method delta NONE；
  DA 9/9 只作错误 evaluator 下观察，不作物理支配/family Kill。A4 不再二修，
  formal 当前无 active carrier。
- **D017** B10 source-native adaptive pilot-RLS 激活（2026-07-26 新建）：
  基于 live R002/D006 恢复 B10 formal carrier；T010 必须先重建 128 contiguous
  pilot→DD fixed B10，identity 过门后同包比较 innovation freeze、adaptive
  forgetting、amplitude-only cheap rule 与 conventional B*。

## 悬而未决

1. **T010 当前方法包**：source-native fixed B10、innovation freeze 与 adaptive
   forgetting 的身份、working region 与方法信号待独立执行/验收。
2. **B10/B12 历史身份债务**：T006 未实现 source-native 128-pilot
   training→decision-directed 生命周期，B12 关键公式与 pilot/data channel 未闭合；
   family 保持 `UNRESOLVED`，不得继承 T006 的科学 verdict。
3. **历史后置材料**：跨块 KF、BPS 迁移、decision-feedback DA ML、SPEC.md §8
   与 B11 叙事仍只属历史写作/消融债务；在新 carrier 激活前均非当前动作。
4. **阶段边界**：仍止于 GW Step 4a；不得进入 Step 5/Contract/Execute，也不得
   直接运行 C15、修 B1/T008、二修 A4/T009 或复活 Scout/P03。

## 当前位置

**🔵 D017 B10 SOURCE-NATIVE CARRIER ACTIVE（2026-07-26）**：R002 完成
post-T009 比较并激活 B10。T010 先闭合 128 contiguous pilot→DD、TX 侧同通道、
原文 RLS/单位和 positive-CFO smoke，再同包比较 P1–P3、cheap rule 与 conventional
B*。独立 verifier 通过前不执行；仍止于 GW Step 4a。

**（历史）D016/V003 NO ACTIVE CARRIER**：T009 在一次有界 repair 后
于 identity gate 停止，P1–P3 未运行。formal 接受
`BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED` 与 method delta NONE，但拒绝把
错误 evaluator 下的 DA 9/9 写成可靠工作区物理支配。A4 已返回候选池，不作 family
Kill、不再二修；等待 live Goal campaign remap 的新 formal 激活决策。仍止于 GW
Step 4a，不进入 Step 5/Contract/Execute。

**（历史）D015/T009 A4 CARRIER ACTIVE**：D015 对 T009 的激活、身份门和
no-second-repair 约束已执行；其“当前 carrier/next action”由 D016 取代，历史授权
与退出条件保留。

**（历史）S015/V002/D014 NO ACTIVE CARRIER**：T008 Kill 被拒收，B1 为
`BLOCKED_IDENTITY / RETURNED_TO_POOL`；该“无 carrier / 等待 remap”动作已被 D015
取代，T008 拒收与 B1 返回池事实保留。

**（历史，已由 H003/D001–D008 修正）S013 A4 条件适配**：原
“赢 max(DA,NDA) +0.27~+0.48 dB”来自混合分母与 post-hoc oracle，已作废。
修复后旧 selector 的可信定位仅为低 SNR NDA safeguard 与强湍流高 SNR 微弱条件
收益；固定 13 dB 阈值、common-payload、pilot/ambiguity、receiver-visible input 与
strongest-fixed comparator 仍需 formal 闭合。D015 不继承旧 PASS，而是授权 T009
做一次可失败的 deployable identity + method-production 终审。

**（前 S011 DPLL 异族 baseline 仿真完成 + baseline 池立住 2026-07-08）**：跑 DPLL DD BER 仿真（5 seed × 4 场景，181s），TL-20 四判据全 PASS（DPLL≥oracle / <2×NDA / >0.7×NDA / @18dB AWGN=3.64e-3 在预期 0.003~0.006 内）。关键发现：DPLL 必须连续处理（全数组 VCO 累积），per-block 重置 VCO 丢符号间相位连续性致 BER 暴涨。omega_n=50e6。Fair gain：DPLL vs NDA AWGN +0.103dB（NDA 稍赢 CI 不跨 0），weak/moderate +0.02dB（CI 跨 0 持平），strong 工作区 -0.046dB；DPLL vs DA 全场景稳赢 +1.25~+1.68dB。DPLL 是异族（DD 闭环 vs 升幂前馈），D-010 标准 3 合规。**baseline 池立住**：DA-ML 主 + DPLL 异族 + VV/BPS fellow。

**（前 S010 导师电话确立 baseline 选取标准 2026-07-08）**：老师主动来电（简报 v3 未发），确立 baseline 选取 4 条 + 方向/复现源质量门 1 条（D-010）：①同场景星地湍流 ②同类型层级（载波/定时/均衡层）不深入子层 ③不找接近方法当 baseline（VV 同族禁主比）④近年+权威（2022+ Trans）⑤找方向/复现只看够好的（避 letter/仿真不全）。**5 条跟我们已有发现互相印证**：标准3↔D-009 VV 同族持平（VV 不该当主 baseline）、标准2↔子层找不到 baseline（放宽到同步/均衡层候选池变大）、标准4↔B 档 LPT/OE 偏薄需补 Trans、标准5↔S008 LMMSE 复现失败教训。

**工具链核查**：老师"trans 不好检索"对我们不成立——`tools/search`（API 源）venue 字段全有，`tools/blit --source ieee --download` 能下全文。但 blit 的 `ieee_search` venue 硬编码空串缺陷已修（加 description/publisher 元素解析 + fallback 正则），待实测验证。

**候选框架/skill 更新点已标**（用户提"后面可以改协议或 skill 用"）：groundwork S4-7 baseline 合法性段补"baseline 选取 4 条标准" / code-quality 矩阵补"复现源质量门" / tools-guide §2 补"IEEE Trans 检索策略"。**本轮不改守"先测不改协议"不变量**，记录候选点待专题稳定后批量改。

**下一步**：按 D-010 5 条标准建 baseline 池（场景词 satellite-to-ground FSO turbulence + 类型词 carrier synchronization/timing recovery/equalization + 排除近亲 NDA-ML/VV/BPS + 过滤 2022+ IEEE Trans）。工具组合：search 搜元数据 + blit 下全文。路线 A/B 决策跟 baseline 池正交，可并行推进。

**（S010 2026-07-08 续接，baseline 池建设 + 检索精读）**：10 组查询（7 API + 3 blit IEEE）合计召回 ~220 篇。blit venue 修复验证成功（22 条 venue 全非空，实测提取 `Journal of Lightwave Technology` / `IEEE Transactions on Communications`）。4 篇第一梯队精读（C1 Paillier JLT 2020 DPLL / C3 Zhang Photonics J 2023 AKF / C4 Wang OE 2024 帧同步 / C6 Zhou IoT-J 2024 元学习）：**没有一篇是干净 baseline**（都缺要素：C1 BPSK+相位屏+2020 / C3 lognormal+SIMO / C4 非CPR层 / C6 MIMO信道估计非逐符号CPR）。

**关键认知修正**：通信领域 baseline 一般是**自实现**（在自己参数下跑经典方法），不要求别人论文用一样参数。引用文献只证明"方法在该层合法"。所以 baseline 结构 = 自实现（DA-ML主 + DPLL异族 + VV/BPS fellow），文献引用支撑合法性（C1 证 DPLL 在星地FSO有人用 / C6 证星地GG+相位估计有人做）。**已有基建**：common/_recovery.py 有 dpll_track + dpll_track_dd，_kf.py 有 4 变体 KF。**缺口**：dpll_track_dd 不支持 m16apsk（判决写死 qam16），需脚本内适配 hard_decision_m16apsk（选项 A，同 VV/BPS/DD-KF 先例）。

**（S011 2026-07-08，DPLL 异族 baseline 仿真 + baseline 池立住）**：跑 DPLL DD BER 仿真（5 seed × 4 场景，181s），**TL-20 四判据全 PASS**：DPLL≥oracle / DPLL<2×NDA / DPLL>0.7×NDA / DPLL@18dB AWGN=3.64e-3（预期 0.003~0.006）。关键发现：DPLL 必须连续处理（全数组 VCO 累积），per-block 重置 VCO 会丢符号间相位连续性致 BER 暴涨（7.5e-3 vs 连续 4.1e-3）。omega_n=50e6（扫描 20/50/100e6 选最优）。Fair gain：DPLL vs NDA AWGN +0.103±0.007dB（NDA 稍赢），weak/moderate +0.02dB（CI 跨 0 持平），strong 工作区 -0.046dB（DPLL 稍好）；DPLL vs DA 全场景稳赢 +1.25~+1.68dB（无 pilot overhead）。**DPLL 是异族**（DD 闭环跟踪环 vs NDA/VV/BPS 升幂前馈），跟 NDA 持平是"不同机制相似性能"非"同族退化"→ D-010 标准 3 合规。**baseline 池立住**：DA-ML 主 + DPLL 异族 + VV/BPS fellow。

**（S012 2026-07-08，方法论转向 + 4种适配 skill + 3并行实验）**：DPLL 持平后认知冲击——NDA-ML 算法层 vs VV/BPS/DPLL 全场景持平，唯一赢 DA-ML 靠 pilot overhead 架构红利。用户问"别人会议级创新点有啥"→ 归纳 6 种类型（场景迁移/免XX/联合/鲁棒性/闭式/估计器升级），B 档 12 篇无一是从零设计新算法。**baseline 认知修正**：通信领域 baseline 是自实现的（在自己参数下跑经典方法），引文献证合法性，不照搬别人参数。**4 种适配方法论**（核心产出）：参数适配 A1 / 结构适配 A2 / 组合适配 A3 / 条件适配 A4，从"锁死方法内部找增量"转向"在场景里找方法间优势关系"。落地为 `.claude/skills/sim-preflight/rules/adaptation-scan.md`（v1.2.0，commit 151feb0）。**baseline 结构规则**：创新是适配策略时，baseline = "不做适配的版本"。设计 3 个并行实验（A1 参数自适应 K / A3 NDA+DPLL 混合 / A4 DA/NDA 条件切换），提示词已给用户在 3 个新对话并行跑。用户同时去旧主对话想别的方向。

**（前 S009 D-008/D-009）**：NDA-ML vs VV 全场景统计显著持平（35 点对等调参 + 5 seed 验证，物理本质 κ=N_seg·σ²_p<<1）。vs DA +dB 主要是 pilot overhead 架构红利（1.25dB 固定 + 纯算法层 0.1~0.5dB）。湍流数据有物理现象（crossover 漂移 / 强湍流递增 / 上行 deep fade +3.07dB）是 B11/B5/B7/B12 全没做的 open gap。简报 v3 `ADVISOR_BRIEFING_2026-07-08_v3_turbulence_pivot.md` 写完未发（老师主动来电）。

**（前 S008 2026-07-08）**：VV/BPS 经典 baseline 实测对照 + LMMSE 复现失败教训。会议级对照矩阵已齐。

**（前 S007 2026-07-07/08）**：SD-FEC 重跑 sanity bit-exact PASS + 25% SD-FEC 档三场景全正；近年 Trans baseline 检索 3 篇 + Crossref VERIFIED + subagent 精读；TL-20 预期表更新。

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
- **S008** VV/BPS 经典 baseline 实测对照 + LMMSE 复现失败教训（2026-07-08，本对话产出）
- **S010** D-010 baseline 标准 + blit venue 修复 + baseline 池检索精读（2026-07-08）
- **S011** DPLL DD 异族 baseline 仿真 + baseline 池立住（2026-07-08）
- **S012** 方法论转向：4 种适配 skill + 3 并行实验方向（2026-07-08，本对话产出）
- **S013** 4 种适配扫描各方向实验日志（2026-07-08 新建，A3 NDA+DPLL FAIL 首条；2026-07-08 续接 A1 参数适配 FAIL 第二条；2026-07-09 续接 A4 条件适配 PASS + 改进版 + 30seed + 文献核查 + 简报；**2026-07-09 续接 A4 切换三 bug 修复重跑（D002/H003）—— 原"切换 PASS +0.27-0.48dB"基于 oracle max(DA,NDA) 假增益，三 bug 修复后切换无全场景增益，真实价值=低 SNR 避 NDA 崩溃 +1.3~+2.3dB + 强湍流高 SNR 微赢 DA +0.02~+0.20dB。切换 A4 信号从"全场景赢"修正为"条件性避险/鲁棒性"。切换叙事定位回 thesis-writing 待讨论**）
- **S014/D012**（2026-07-25）：Pilot-Jones scoped axis Kill 后恢复 B10/B12 既有
  Step 1–3 证据为当前 carrier；T006 预注册 headroom 前置门，门通过即同包跑三个
  组合方法，目标是形成可包装方法而非再写纯分析。
- **S015/V001/D013**（2026-07-25）：T006 工程 PARTIAL、科学 verdict FAIL；
  B10/B12 family 标 UNRESOLVED，停止当前修复。下一 carrier 为 B1 adaptive
  phase window，T007 先结构门后同包三方法。
- **S015续接/V002/D014**（2026-07-26）：T008 工程测试 PASS、科学 Kill FAIL；
  B1 不关闭但返回候选池，formal 暂无 active carrier，等待 Goal campaign remap。
- **D015/T009**（2026-07-26）：Goal R001 campaign remap 选择 A4；以统一
  waveform/common mask、deployable input 与 strongest fixed comparator 重建一次
  可失败身份门，过门后同包生产 P1–P3 方法。
- **S016/V003/D016**（2026-07-26）：T009 独立接收 FAIL
  (`P0=4/P1=5/P2=1`)；接受 identity block 与 method delta NONE，拒绝 DA 9/9
  物理支配。shared transmitter/pilot 随机、1 MHz 频率不对称、无来源可靠工作区/
  FEC crossing、raw/result ignored 和 diff-check FAIL 均入账；A4 返回候选池，
  formal 无 active carrier。
- **live R002/D006 / D017 / T010**（2026-07-26）：post-T009 比较 B10、C15、
  B1、B9 后激活 B10 source-native adaptive pilot-RLS；T010 已准备，等待独立
  起飞审查，尚未运行实验。
- **D-011** A1 参数适配（NDA 块长自适应 K）FAIL（2026-07-08，S013 新建）
- **H008** 交接给新对话：自适应论文 baseline 组织/参数处理/叙述展开调研（2026-07-09，用户要去新对话搞清楚别人怎么弄 baseline + 参数照搬还是自调）
- **H009** 切换三 bug 修复+30seed 重跑结果（2026-07-09，执行 thesis-writing D001 修复任务，实验在本专题 step4a 跑。代码 `_a4_switch_30seed_fixed.py` + 数据 + 报告 `_a4_switch_bugfix_report.md`。Bug2 非假增益源不修（独立核查修正用户诊断）。结论：切换无全场景增益，降级为鲁棒性补丁，net gain+1.2dB 不依赖切换。切换叙事定位回 thesis-writing 待讨论。完整交接见 thesis-writing/H003）
- **S010** D-010 baseline 标准确立 + baseline 池检索精读（2026-07-08，10 组查询 ~220 篇召回 4 篇精读，认知修正：通信 baseline 自实现）
- **S011** DPLL DD 异族 baseline 仿真 + baseline 池立住（2026-07-08，TL-20 四判据全 PASS，DPLL 连续处理 omega_n=50e6，vs NDA 持平到稍差，异族合规）
- **R001** 自适应 CPR 论文 baseline 组织/参数处理/叙述展开调研（2026-07-09，执行 H008，3 篇精读：张思齐 BUPT 同门学位论文 + Wang 2025 OE 全文 + Barbosa 2020 JLT abstract。4 问全答：Q1 切换型 baseline=固定版本+fellow+上界 / Q2 五段式叙述 / Q3 自调+标溯源不照搬 / Q4 领域不做先复现再迁移。结论=简报 §6 符合惯例，验证非推翻。附 MSDM per-symbol vs per-block 有效 SNR 机制不同，可补强 §5 新颖性。**§F 追加**：用户质疑"baseline 太老"触发合法性背书矩阵调研——三轮 59 JSON/~544 篇证实 NDA 载波相位恢复 2020+ 严格 Trans 是空白（物理事实非检索不全），DA/DPLL/VV/BPS 背书已够；补检索 NDA 大类 8 JSON 找到 4 篇严格 Trans 作 NDA 方法论合法性背书（TVT 2023 CRB + TVT 2025/JLT 2025/TWC 2022），缺口转化为"我们填补空白"叙事）
