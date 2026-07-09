# Decisions — B3-Q2 子系统协同联合估计第三候选

> 专题 `.sessions/2026-07-08-b3-joint-estimation/` 的决策记录。

## D001: 开 B3-Q2 专题 + 首验证 4 支路迁移策略（阶段 0.1 = 星地多孔径阵列场景验证 + 单链路 CRB 上界前置）

> status: superseded（2026-07-09 被 D004 Kill 推翻——三切口物理 FAIL，但本决策的"阶段 0.1 首验证"执行无错，CRB 上界 1.0-1.2dB PASS 仍有效）
> date: 2026-07-08
> 取代：无（开新专题，不推翻 NDA-ML/B7/B5 任何决策）
> 被取代：无
> 依据: Explore agent B3-Q2 详查（6 问题 700 词）+ S031 #1 Conditional Go（+2~3dB 4 支路强湍，S031 L33-39, L161-169, L213）+ 导师"特长场景"标准（voice 2026-07-08）+ B11-Q2 放弃后接替 + 用户原话 voice 2026-07-08（"B11-Q2 凑数"+"B3-Q2 联合估计"+"开 B3-Q2 首验证迁移"）
> 触发原话: 导师 "新方法不是要求全能，是在某一实际需求场景下的特长" + 用户 "B11-Q2感觉在凑数。你要不给我另一个" + 选"B3-Q2 联合估计" + 选"开 B3-Q2，首验证迁移"

### 决策

**开 B3-Q2 专题，阶段 0 六项规约设计完成，首验证 4 支路迁移风险。**

1. **阶段 0.1 = 星地多孔径阵列场景验证 + 单链路 CRB 上界前置**（最高优先）：B3-Q2 的 +2~3dB 是 4 支路 MRC 强湍下的，单支路只有 ~1dB。星地单孔径终端难以堆叠多望远镜（jphot 笔记 L56）。阶段 0.1 验证：(a) 星地多孔径阵列接收是否真实工程场景；(b) FR-21 oracle 上界前置算单链路 CRB，<0.5dB 直接砍
2. **阶段 0.2 = A1 归属核查**：jphot+oe BUPT 课题组已完成 FS+FOE+MRC 联合。查清是否已发星地分集续作 + B3-Q2 增量够 D005 够格吗
3. **阶段 0 不写代码**：守 profile 第 9 次防线 + INVARIANT 6
4. **导师"特长场景"标准纳入**：B3-Q2 特长场景 = 强湍流分集接收下联合估计 vs 分立管线。阶段 0.1 必须明确这个特长场景在星地下是否成立

### 理由

1. **B3-Q2 是真新方法不是凑数**（导师"特长场景"标准）：B11-Q2 是 NDA-ML 验证延伸没有自己的特长场景，B3-Q2 有独立特长场景（强湍流分集下联合估计）。即使有 4 支路迁移 + A1 双致命风险，也是真新方法的 Risk 不是凑数
2. **dB 最高**（+2~3dB 4 支路）：S031 #1 Conditional Go，文献实证强（jphot +2.09dB / oe +1.78dBm，4 支路 MRC 强湍）。单支路 ~1dB 仍可能够格 D005 会议门槛
3. **4 支路迁移风险是 B3-Q2 的核心 Risk 不是 Kill 判据**：阶段 0.1 首验证星地多孔径阵列是否真实工程场景，如果是则 B3-Q2 特长场景成立，如果单链路退化 dB 不够格则转 Kill。这是阶段 0.1 要回答的问题，不是开专题前就 Kill 的理由
4. **跟现有 3 候选完全正交**：NDA-ML（单 CPE）/ B7（单 FOE）/ B5（单 FOE）都是单估计器单链路，B3-Q2 是跨子系统联合 + 多支路分集，完全不同赛道

### 排除的替代方案

- **B3-Q3 跨子系统协同**：否决。dB 无自身锚 + 代码基建需全新 + B3-Q2 已是 +2~3dB 第一梯队（Q3 优先级低于 Q2）。但 B3-Q3 作为 B3-Q2 的 D006 边界 fallback 保留（若 B3-Q2 走环路 TF 联合建模撞 D006 转 B3-Q3）
- **B11-Q2**：已放弃（凑数，NDA-ML 延伸是验证不是新方法）
- **B7-Q2**：否决（跟 B11-Q2 同构，也是验证不是新方法，且 B7-Q1 还在 sandbox 4/6 未完）
- **不凑三个先跑 2 个**：否决。用户明确"保持同时开三个方向一直跑"，B7/B5 sandbox 待跑 + NDA-ML dormant，第三个候选不阻塞

### 影响范围

- **阶段 0.1 星地多孔径阵列场景验证**：核心动作=验证星地多孔径阵列（AO 校正后分集）是否真实工程场景 + FR-21 oracle 上界前置算单链路 CRB。输出 `explore/b3-joint-estimation/_diversity_migration_validation.md`
- **阶段 0.2 A1 归属核查**：查清 BUPT 课题组是否已发星地分集续作
- **跟 B7/B5 的交叉**：B3-Q2 是多支路分集 + 跨子系统联合，跟 B7（单 FOE）/ B5（单 FOE）完全正交无撞车
- **债务**：MRC 合并器 + 帧同步 + 多支路管线 + 多望远镜信道需新建（sandbox/MVE 阶段实现）

### 教训

1. **B11-Q2 凑数是主控对话在"保持 3 方向"压力下的失守**：为了凑第三个方向开了 NDA-ML 验证延伸，被用户判断"在凑数"。**教训：接替方向要是真新方法不是验证延伸，导师"特长场景"标准是判据**
2. **B3-Q2 的 4 支路迁移风险比 S031 描述的更严重**：subagent 详查发现 jphot 笔记 L56 原话"星地单孔径终端难以堆叠多望远镜"，单支路 dB 砍半（~1dB）。S031 L213 标"不建议先试"是对的，但用户选"开 B3-Q2 首验证迁移"——阶段 0.1 首验证是防线不是拖延
3. **导师"特长场景"标准降低 Go 标准但提高场景真实性要求**：从"全面赢"降到"某场景特长"，但"特长场景"必须是真实工程场景（不能是造问题）。B3-Q2 的星地多孔径阵列是否真实工程场景是阶段 0.1 必答

### 来源

S001（本轮）+ Explore agent B3-Q2 详查（6 问题 700 词）+ S031 #1 详评 + 导师"特长场景"标准 + B11-Q2 放弃 + 用户原话 voice 2026-07-08

---

## D002: 阶段 0.1-0.2 完成——不 Kill + 修正 4 支路 dB 转录错误 + B3-Q2 增量定位为迁移+维度扩展型

> status: superseded（2026-07-09 被 D004 Kill 推翻——"不 Kill"结论推翻，但"4 支路 dB 转录错误修正"+"A1 归属核查"仍有效）
> date: 2026-07-08（S002 阶段 0.1-0.2 完成）
> 取代：部分修正 D001 的 dB 描述（4 支路 +2~3dB → 2 支路 +2~3dB / 4 支路 0.7-2.14dB）；D001 决策本身不动（仍 active）
> 被取代：无
> 依据: S002 阶段 0.1a 子 agent 产出（`_stage0_1a_aperture_diversity_scene_survey.md`）+ 主线 grep sat.1553 content.md:149 PASS + 阶段 0.1b 子 agent 产出（`_stage0_1b_single_link_crb_upper_bound.md`）+ 主线 grep jphot-L357/L375/L385 双源确认转录错误 + 阶段 0.2 主线 A1 核查（jphot-L71/101/175/208/385）
> 触发原话: 无（技术推导，本轮 0.1-0.2 是 H001 派发任务的执行结论）

### 决策

**阶段 0.1-0.2 完成，B3-Q2 不 Kill，进阶段 0.3-0.6。** 同时修正一个 FR-26 级转录错误。

1. **阶段 0.1 门控判定：不 Kill**
   - 星地多孔径阵列场景：部分成立（有 Ma 2015 仿真 + Geisler 2016 架构提案，无已部署工程实例；sat.1553 不提星地分集）
   - 单链路 CRB 上界：≈ +1.0~1.2dB ≥ 0.5dB（FR-21 不卡），自洽性 PASS
   - 守 D005 务实路线 + 导师"特长场景"标准：单链路强湍 FSTS 联合 vs 分立就是合法特长场景，不依赖边缘的多孔径阵列

2. **🔴 修正 4 支路 dB 转录错误**（FR-26 核查产物）：
   - 旧（D001/INVARIANT 11/note-L36/`_cut-b1b2b3-verify.md:258-291`/S031）："4 支路 +2.09/+3.41dB"
   - 新（jphot-L357/L375/L385 双源确认）：**2 支路 +2.09/+3.41dB；4 支路 = 0.7dB(4-QAM)/2.14dB(16-QAM)**
   - jphot-L385 结论自己用的就是 2 支路数字，转录错误坐实
   - 单链路（1 支路）4-QAM 强湍 = 1.17dB（≥4 支路 0.7dB）—— 单链路反而是 FSTS 增益最显著场景

3. **阶段 0.2 A1 归属核查结论**：B3-Q2 增量空间存在但偏薄（迁移+维度扩展型，非算法创新型）
   - jphot 已 claim：FSTS 一套 TS 做 FS+两段式 FOE+MRC 联合 + BL² 降噪（这是单链路 dB 优势的物理来源）
   - jphot 未 claim / B3-Q2 切口：① CPE 联合维度（jphot CPE 独立）② Doppler/CFO 维度（jphot-L208 自承缓变假设）③ 星地场景（jphot 0 提 LEO/satellite）
   - **首要风险从"4 支路迁移"转移到"增益归因"**：B3-Q2 单链路 dB 来自 jphot 已 claim 的 BL² 算法结构，若 baseline 只比传统 TS，增益是继承的；baseline 必须含 jphot FSTS 才公平

### 排除的方向

- **不 Kill B3-Q2**：单链路 CRB 够格（≥0.5dB）+ 有合法增量切口（CPE/Doppler/星地），守 D005 务实路线不卡严
- **不claim jphot 已有的算法机制**：两段式 FOE / FSTS / BL² 降噪 / 跨极化共轭 全部 jphot 已 claim，B3-Q2 不能当新点

### 可复用部分

- 0.1a 文档：星地多孔径阵列场景文献清单（Ma 2015 / Geisler 2016 / Horst 2023）
- 0.1b 文档：单链路 FOE mCRB 推导 + jphot MSE 陡崖封顶机制
- 转录错误修正：note-L36 + verify 文件 + S031 dB 数字（待下一对话或专门修）

### 影响范围

- **INVARIANT 11 修正**：dB 描述从"4 支路 +2~3dB / 单支路 ~1dB"改为"2 支路 +2~3dB / 4 支路 0.7-2.14dB / 单支路 1.17dB（单链路最显著）"——topic-index 待更新
- **阶段 0.4 baseline 硬约束**：必须含 jphot FSTS（不只比传统 TS），否则增益是继承的
- **阶段 0.3 架构定性输入**：加 Doppler 维度需判前馈开环（不撞 D006）还是环路 TF（撞转 B3-Q3）
- **待办**：派子 agent 查 BUPT 课题组 2024+ 续作（防自吞增量）

### 教训

1. **转录错误长期未被发现**：note-L36 + verify 文件 + S031 的"4 支路 +2~3dB"流传多轮，直到本轮 0.1b 子 agent 算 CRB 时发现"单支路 ≥4 支路"反直觉，主线独立 grep jphot 原文才暴露。**教训：dB 数字必须回原文双源核验，笔记/verify 文件的二次转录不可全信（TL-21 确定性 grep 的延伸）**
2. **子 agent 反直觉发现是真信号**：0.1b 子 agent 主动报"单链路 dB 砍半假设不成立"，这戳中了真实转录错误。**教训：子 agent 产出与预期冲突时优先核查不要急着否定（profile"急于推进"防线）**
3. **A1 归属核查要查"算法机制 claim"不只"场景做没做"**：jphot 场景是地面 FSO（没做星地），但算法机制（两段式 FOE BL²）已完整 claim。B3-Q2 增量空间在场景+维度不在算法机制

### 来源

S002（本轮阶段 0.1-0.2）+ 0.1a/0.1b 子 agent 产出 + 主线 grep jphot/sat.1553 原文核查

---

## D003: 阶段 0.3-0.6 完成——架构走前馈开环（不撞 D006）+ BUPT 迫近自吞风险登记（非 Kill，timeline 风险）

> status: superseded（2026-07-09 被 D004 Kill 推翻——架构前馈开环本身无错且不撞 D006，但"三切口物理成立"的隐含假设被推翻，架构落地点消失。D006 边界判定 + BUPT 审计方法仍有效）
> date: 2026-07-08（S003 阶段 0.3-0.6 完成）
> 取代：无（D001/D002 决策不动，本轮是阶段 0 后半执行结论 + 架构方向定死 + 风险登记）
> 被取代：无
> 依据: S003 阶段 0.3-0.6 执行 + jphot content.md grep L101/175/208（前馈块估计证据）+ B3 详评 `_B3-...md` L77/L85（D006 边界判定）+ D006（decisions.md L341 禁区定义）+ BUPT 子 agent 产出 `_bupt_followup_audit.md`（三切口覆盖核查）
> 触发原话: 无（技术推导，本轮 0.3-0.6 是 H002 派发任务的执行结论）

### 决策

**阶段 0.3-0.6 完成，阶段 0 全六项闭合，进 sandbox。** 同时定死架构方向 + 登记 BUPT timeline 风险。

1. **架构走前馈开环**（INVARIANT 13 定死）：B3-Q2 联合估计 = 一套 TS 块估 FS+FOE+CPE+Doppler，逐块前馈不进环路。
   - D006 边界判定：不撞（三重证据——D006 只禁湍流相位进环路 TF / B3 详评 Q2 判否 / jphot 本身前馈）
   - Doppler 维度 = 块间 Δf̂_k 序列线性回归 → f_dot 前向补偿（确定性轨道运动，非随机湍流相位，物理本质不同）
   - 排除形态（撞 D006 转 B3-Q3）：Doppler+湍流相位联合进环路 TF / KF 扩 [ω,f_dot,φ_T] / 湍流相位作 CPE 先验进环路

2. **公平对照框架**（防增益归因，D002 首要风险对策）：
   - 三方对照：M1 传统分立 TS（祖师爷）/ M2 jphot FSTS（公平基准）/ M3 B3-Q2 联合
   - fair gain Go 判据 = `gain_vs_M2 > 0`（B3-Q2 vs jphot FSTS 有新增益），不用 gain_vs_M1（含 jphot 继承）
   - 增益归因熔断：`gain_vs_M2 ≤ 0` → 红线警报转 Kill
   - 消融归因：CPE 贡献 + Doppler 贡献各自 <10% → B3-Q2 无真实增量转 Kill

3. **BUPT 迫近自吞风险登记**（非 Kill，timeline 风险）：
   - 三切口（CPE 联合 / Doppler / 星地）**均未被单篇 BUPT 续作完整吞没**
   - 但 BUPT 构件齐全（JCSCR CPE联合 + TTQP 分集FOE + SSRN/OECC 星地FS+FOE），2025-2026 持续活跃
   - 12 个月内出现"星地分集+CPE/Doppler联合"汇合论文概率非低
   - **对策**：sandbox/MVE 加速推进；SSRN/OECC abstract 亲验 + 张思齐 CNKI 核查作为 sandbox 前置债务

### 排除的方向

- **环路 TF 联合建模**：撞 D006（B1/Q12 双重证伪），转 B3-Q3 边界（只标不砍）
- **baseline 只比传统 TS**：不公平（dB 是 jphot 继承的），必须含 jphot FSTS

### 可复用部分

- 0.3 架构决策文档（前馈开环流程 + D006 边界三重证据）
- 0.4 三方对照矩阵 + 消融设计（CPE vs Doppler 归因）
- 0.5 参数表（全标 source，grep 核验）
- 0.6 五个新建代码接口定义（MRC/帧同步/多支路预校正/联合管线/多望远镜信道）
- BUPT 审计文档（续作清单 + 三切口覆盖判断）

### 影响范围

- **sandbox 阶段（对话 3）**：按 0.4 三方对照矩阵跑 M1/M2/M3，主场景单链路强湍+Doppler
- **INVARIANT 13 定死**：前馈开环架构不变（动则重新讨论）
- **增益归因熔断机制**：sandbox 的 gain_vs_M2 ≤ 0 是硬 Kill 触发条件
- **债务登记**：Doppler f_dot 溯源 + SSRN/OECC abstract 亲验 + 张思齐 CNKI 核查 + 转录错误修正（D002 遗留）+ 多望远镜间距参数

### 教训

1. **0.4/0.5/0.6 强耦合合并产出合理**：三阶段依赖链（架构→baseline→参数→接口），合并在一个文档避免跨文件不一致。但文档较长（16KB），后续若改某节需注意三节联动
2. **BUPT 审计的"负证据"判断需克制**：子 agent 对 Doppler"未覆盖"判断基于"已验证 abstract 无一提 Doppler"——这是负证据（absence of evidence），不是证据。主线接受但标注"基于负证据，SSRN/OECC abstract 未亲验是漏洞"
3. **Doppler 维度的 D006 边界判定靠物理本质区分**：确定性 Doppler（轨道运动可预测）vs 随机湍流相位（D006 禁区）——两者物理本质不同，前馈估计 Doppler 不撞 D006。这个区分是本轮 0.3 的关键判断，需 sandbox 验证前馈外推误差不退化成"等效环路"

### 来源

S003（本轮阶段 0.3-0.6）+ jphot content.md grep + B3 详评 + D006 + BUPT 子 agent 产出 `_bupt_followup_audit.md`

---

## D004: Kill B3-Q2——三切口全物理 FAIL（CPE CRB≈0dB + Doppler 物理可忽略 + 星地场景迁移非增量）

> status: active（Kill 决策）
> date: 2026-07-09（S004 对话 3a→3b 合并执行，物理深查后 Kill）
> 取代：D001（开题）/ D002（不 Kill）/ D003（架构定死）——三者均基于"三切口物理成立"的隐含假设，本轮深查推翻该假设，D001-D003 标 superseded（不删，保留血缘链）
> 被取代：无
> 依据: S004 对话 3a（f_dot 溯源 56MHz/s + 5 接口实现 + smoke test）+ S004 对话 3b 前段（TL-20 物理量级分析 + 子 agent 深查 4 否决条件 0/4 推翻 + 主线独立 grep B5 L147/params.py:904 核查）+ 0.1b CRB 推导（`_stage0_1b_single_link_crb_upper_bound.md` L88/L91 CPE joint-vs-separate ≈ 0 dB）
> 触发原话: 无（技术推导，TL-20 先建理论预期 + TL-22 查物理前提后，物理双重证据指向 Kill；用户确认"Kill B3-Q2（物理双重证据）"）

### 决策

**Kill B3-Q2 子系统协同联合估计。** 三切口（CPE 联合 / Doppler 维度 / 星地场景）全物理 FAIL，gain_vs_M2 ≈ 0，§0.4.5 分层 Go/Kill 三层（L1/L2/L3）全物理 FAIL。这不是"还没调好"——是 TL-20 理论预期 + TL-22 物理前提核查双重证据指向的物理结论，不是仿真能翻盘的。

1. **① CPE 联合切口 FAIL（理论证死，0.1b CRB）**：
   - 0.1b CRB 推导 L88："CPE joint-vs-separate CRB 增益 ≈ 0 dB（单链路，等导频长度下 CRB 恒等）"——"CRB 只依赖 N、γ、Δν，不依赖是否共享"
   - jphot FSTS 本身只做 FS+FOE，CPE 另用"相位噪声估计 + DD-LMS"兜底（jphot-L101/L243），故 CPE 联合实际 ≈ 0 dB
   - 唯一非零项是"开销受限模型上界 ≤+2.4dB"，但那是开销分配论据非估计理论增益，jphot 结构下不兑现

2. **② Doppler 维度切口 FAIL（物理量级，TL-22 深查确认）**：
   - B3-Q2 声称"打破 jphot-L208 缓变假设"，但深查证明该假设在 LEO Doppler 下完全成立
   - 物理量级（f_dot=56 MHz/s，B5 锚 optcom.2024.130981 L147 NEO 600km 过顶最大全 Doppler 斜率）：
     - 块间（TS=320 符号）频偏跳变 = 7.2 Hz（2.5GBaud）/ 1.8 Hz（10GBaud）
     - FOE 估计分辨率 = 610 kHz（2.5GBaud）/ 2.4 MHz（10GBaud）
     - **块间跳变比 FOE 分辨率小 5 个数量级** → FOE 测不出 Doppler 变化
     - 帧（8192 符号）Doppler 相位 1.9e-3 rad，比激光相位噪声 RMS（~1 rad）小 3-4 个数量级
   - 要破坏缓变假设需 f_dot ≈ 4768 GHz/s（2.5GBaud）/ 76294 GHz/s（10GBaud）——物理 LEO 最大值的 **8.5 万倍 / 136 万倍**
   - 深查 4 否决条件 0/4 推翻（子 agent + 主线独立 grep B5 L143-149 核查）：
     - (a) 残余 f_dot ≤ 全 Doppler f_dot（物理必然，不可能反转）
     - (b) 56 MHz/s 是 df/dt（频偏变化率）非误用；LEO 文献量级数十 MHz/s（GHz/s 系激光频率不稳定度非轨道斜率）
     - (c) jphot 从未测过 LEO Doppler，但块尺度上缓变假设站得住（7Hz << 610kHz）
     - (d) 公式/单位复核无误（π·f_dot·t² ✓，1/(4·N_fft·T_S) ✓）
   - **关键洞察**：B5 锚 L149 自己的 Doppler 跟踪是"750 measurements lasting ~13 min"——分钟级跨帧。Doppler 斜率只在分钟级跨帧才有意义，单帧 8192 符号（μs 级）完全捕捉不到。B5 自己都不是单 TS 块内处理 Doppler。

3. **③ 星地场景切口非增量（D002 已定性）**：jphot 地面→星地是场景迁移非算法增量，且 jphot 的 dB 优势来自 FOE BL²（已 claim），不是星地场景

4. **gain_vs_M2 ≈ 0（D003 增益归因熔断触发）**：M3 = M2 + CPE(≈0) + Doppler(≈0)，B3-Q2 单链路 1.17dB 全是 jphot 继承（FOE BL²），fair gain 判据 gain_vs_M2 ≈ 0

5. **§0.4.5 分层 Go/Kill 三层全物理 FAIL**：
   - L1 全条件（gain_vs_M2>0 + CPE/Doppler 各≥10%）：CPE+Doppler 都≈0 → FAIL
   - L2 Doppler crossover（扫 f_dot）：Doppler 物理可忽略，物理 f_dot 范围内扫不出 crossover → FAIL
   - L3 失效边界（jphot 高 Doppler 失效）：jphot 缓变假设在 LEO 下成立不失效 → FAIL

### 核心失败机制（不是"没调好"）

**B3-Q2 的增量切口在 TS 块时间尺度下物理不成立。** CPE 联合的 CRB 不依赖"是否共享"（估计理论铁律）；Doppler 斜率在 μs 级单帧内产生的频偏变化（7 Hz）远低于 FOE 分辨率（610 kHz），是物理量级鸿沟不是算法能填的。jphot 的"缓变假设"在它设计的块尺度下本就成立——B3-Q2 试图打破一个在物理上不被破坏的假设。

### 排除的方向（Kill 后失效，防复活）

- **CPE 联合（单链路等导频）**：CRB ≈ 0 dB，估计理论已证。除非找到"非等导频"或"多支路 CPE 联合"的新结构（但后者归多支路分集增益，非 CPE 联合本身）
- **Doppler 维度（TS 块内/块间）**：物理量级可忽略。Doppler 斜率只在跨帧/过顶（分钟级）才有意义，但那是完全不同的仿真结构（B3-Q3 边界 + D006 需重判）
- **B3-Q2 整体重启**：三切口全 FAIL，dB 是继承的，无残留切口

### 可复用部分（Kill 后保留，供后续候选/教训用）

1. **5 接口代码 + MVE 框架**（`projects/simulation/explore/b3-joint-estimation/`）：multi_aperture_channel / frame_sync_fsts / mrc_combiner / multi_branch_phase_precorr / joint_estimation_pipeline + b3_joint_mve.py + _smoke_test.py（9/9 PASS）。若后续候选需多支路分集/联合估计管线，可复用作起点
2. **f_dot 物理量级分析方法**（TL-20 + TL-22 实战）：块间跳变 vs FOE 分辨率的量级比对，可作为"Doppler 切口是否物理成立"的快速预筛工具（不用跑仿真）
3. **Fried 参数计算**（多望远镜间距判独立分集）：强湍 r0≈2cm，弱湍 r0≈31cm
4. **f_dot 精确溯源**：56 MHz/s（B5 L147）+ params.py:904 `DOPPLER_RATE_B5=56e6` 已 OK 溯源
5. **BUPT 续作审计**（`_bupt_followup_audit.md`）：三切口覆盖判断方法可复用
6. **CRB 推导框架**（`_stage0_1b_single_link_crb_upper_bound.md`）：FOE BL² 26dB 方差域 + CPE ≈0dB 的推导

### 教训（Kill 后提炼）

1. **阶段 0.1b 的 CRB ≈ 0dB 预警被阶段 0.3-0.6 架构设计绕过**：0.1b 已预警"CPE 联合增益 ≈ 0dB"（L88/L91），但 0.3 架构决策（D003）仍把 CPE 联合 + Doppler 作为两个切口推进到 sandbox。**教训：CRB 预警（TL-20 理论预期）应在阶段 0.3 架构决策时作为硬门控——CRB≈0 的切口不该进 sandbox 实现层**。TL-20 不只是"跑仿真前建预期"，还要"建预期后用它筛切口"
2. **Doppler 切口的物理量级预筛缺失**：D003 架构决策 §2.2 写了"Doppler 斜率前馈回归"，但没做"块间跳变 vs FOE 分辨率"的量级预筛。这是 TL-22"震撼结果先查物理前提"的延伸——**任何"时变/漂移"切口，必须先算它在算法时间窗内的物理量级 vs 估计分辨率，量级差 >3 个数量级直接物理 Kill 不进 sandbox**
3. **3a 烟雾测试的"L1 FAIL"本该触发物理深查而非"待 3b 跑全量"**：S004 骨架跑数 L1 全条件 FAIL（7/28），gain_vs_M2 ≈ 0 甚至负，当时归因"f_dot_est 是占位 + T_S 问题"待 3b。实际根因是物理量级，骨架数据已经是真实信号（M2≈M3）。**教训：sandbox 骨架的 gain≈0 不要轻易归因"还没接好"，先做 TL-22 物理前提核查**（本轮纠正了这个——用户选"先深查再定"是对的）
4. **jphot 缓变假设的"缓变"是相对算法时间窗的**：jphot 的 TS 块是 μs 级，"缓变"指"块间频偏近似不变"。LEO Doppler 在 μs 级确实缓变（7Hz 跳变），只在分钟级才显著。B3-Q2 误把"LEO 有 Doppler"等同于"LEO Doppler 在 TS 块尺度不缓变"——两者是不同时间尺度。**教训：时间尺度对齐是时变切口的首要核查项**

### 影响范围

- **B3-Q2 专题状态**：active → closed（Kill 完成，不再推进）
- **D001/D002/D003 标 superseded**（不删，血缘链保留）
- **候选池**：B3-Q2 Kill 后，载波同步 v2 池剩余活跃候选 = NDA-ML（dormant）/ B7（active sandbox）/ B5（active §7 Kill 后 salvage 全无信号）。B3-Q2 是 B2 Kill + B11-Q2 放弃后的接替，再 Kill 需主控重新排候选池
- **5 接口代码保留**：作为多支路分集/联合估计的基建参考，不删
- **K001 验证记录**：见 verifications.md（物理量级分析作为 Kill 验证证据）

### 来源

S004（对话 3a 补债务 + 5 接口实现 + smoke test，对话 3b TL-20 物理量级分析 + 子 agent 4 否决条件深查 0/4 推翻 + 主线独立 grep 核查）+ 0.1b CRB 推导（L88/L91）+ B5 锚 optcom.2024.130981 L143-149 grep 核查 + params.py:904 核查 + 用户确认"Kill B3-Q2（物理双重证据）"
