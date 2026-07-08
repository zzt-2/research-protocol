# Decisions — B7 Gardner TED 复用 FOE 第二候选

> 专题 `.sessions/2026-07-08-b7-gardner-ted-foe/` 的决策记录。
> D### 按编号排列，血缘链通过 取代/被取代 字段维护。

## D001: Gardner TED 1986 公式源 = 本地 Matlab 代码（不切降级，B7 映射靠数值重建）

> status: active
> date: 2026-07-08
> 取代：无（贯彻 H001 阶段 0.1 判定门控，修正"公式不全必切降级"的预判）
> 被取代：无
> 依据: 本地代码核查（`毕设/旧本科代码/PSKTimingErrDetector.m` L11-12 + `Tx2Rx.m` L176-214）+ B7 poster 全文核查（`papers/doi/10.1364_ofc.2026.w2a.62/content.md` 90 行 0 编号公式 4 图 omitted）+ Gardner 1986 扫描原文核查（`papers/doi/10.1109_tcom.1986.1096561/content.md` 14 行水印正文不可检索）+ 用户原话 voice 2026-07-08（"gardner我不是有matlab代码吗"）
> 触发原话: 用户 "啥玩意？咱们先说说这是要干啥？顺便，gardner我不是有matlab代码吗？毕设\旧本科代码\Tx2Rx.m" + 选"代码作 1986 公式源"+"先出 0.1 报告"

### 决策

**阶段 0.1 公式完整性核查结论：不切降级方案，进 0.2。**

1. **Gardner TED 1986 原版公式源 = 用户本地 Matlab 代码**（`毕设/旧本科代码/PSKTimingErrDetector.m` + `Tx2Rx.m` L176-214 定时环），不用 Gardner 1986 扫描原文（正文不可检索）
2. **B7 OFC 2026 "TED 增益↔Doppler 映射" 解析式缺失，但可数值重建**（用本地 TED 代码扫 Doppler 频偏跑 S-curve 取 max = G(f_D)，重建 poster Fig.1a 那张 omitted 的图）
3. **不切降级 A/B/C**：1986 公式有可执行代码替代（比原文强），B7 映射靠数值重建（不是靠文字猜公式），不违反 INVARIANT 13 "不硬磕"精神

### 理由

1. **INVARIANT 13 的"公式不全直接标红不硬磕"针对"靠文字描述重建算法公式"**（LMMSE 教训：PDF→md 把 eq(5)(6)(7) 转 picture omitted，靠文字重建缺关键项）。本场景：
   - 1986 公式有可执行代码（PSKTimingErrDetector.m），不需要文字重建
   - B7 映射靠数值重建（数值实验验证机制是否存在，不是猜解析式）
   - 数值重建是"验证"不是"硬磕重建"

2. **本地代码是意外资产，把"降级 C 救 1986 原文"从"OCR 扫描件"升级为"直接用可执行实现"**。代码是公式的可执行版，比扫描原文可靠（无 OCR 错误风险）。

3. **用户原话指出代码存在**（"gardner我不是有matlab代码吗"），主线原本只查了 `papers/` 下的原文，漏了本地代码资产。FR-26 证据链要求查证据，本地代码是比扫描原文更强的证据。

### 三选项决策记录（用户选代码作公式源 + 先出 0.1 报告）

主线原预判（被用户纠正前）：B7 poster 0 编号公式 + 4 图 omitted → 触发 INVARIANT 13 红线 → 切降级（A 定性引用 / B 换 baseline / C 救 1986 原文）。

用户纠正后路径：本地 Matlab 代码 = 1986 公式可执行实现 → 1986 公式完整（✅）→ B7 创新点（映射）虽缺解析式但可数值重建 → 不切降级，进 0.2。

### 排除的替代方案

- **降级 A（定性引用 B7，不作对标 baseline）**：否决。等于放弃 B7-Q1 的 MVE（MVE 需实现锚方法），B7 作为第二候选失去意义。
- **降级 B（PSA FOE 作主 baseline，B7 作思想参考）**：否决。PSA FOE 是 Vieira 2023 [5/6] 的方法，公式同样未落盘，仍需下载核查；且 B7 "复用 Gardner TED" 创新点没了数学根基。
- **降级 C（OCR 救 Gardner 1986 扫描原文）**：被用户方案替代。本地代码比 OCR 扫描件可靠，不需要 OCR。

### 影响范围

- **0.2 数学同族性检查**：1986 公式明确（去直流 Gardner TED `e = y_mid·[y_late−y_early]`），B7 创新点是"复用 TED 增益做 FOE"。**初步看非同族**（B7 把 TED 当传感器复用估计频偏 f_D，1986 用 TED 检测定时误差 τ，不是同一个量的变体），但需 0.2 深度确认（V3+C8 祖师爷警报）。
- **0.3 架构定性**：用户代码是反馈环（NCO+环路滤波器），B7 算法也是反馈环结构（CV mult+TR loop）。前馈化决策仍需做（INVARIANT 12）。
- **sandbox 三方对照**：① B7 proposed FOE（数值重建版）② Gardner 1986 原版定时环（用户代码直接当祖师爷方）③ PSA FOE baseline。三方都有实现路径。
- **债务**：B7 映射解析式缺失（0.2 数值重建验证周期相关后，若进 sandbox/MVE 补解析推导）；Gardner 1986 扫描原文不可检索（本地代码已替代，若需引 1986 具体行号需重新 OCR）。

### 教训

1. **查证据时不能只查 papers/ 下的原文，要查本地代码资产**（FR-26 强化）。用户本地可能有论文方法的可执行实现，比扫描原文可靠。主线本次只查了 `papers/doi/10.1109_tcom.1986.1096561/`，漏了 `毕设/旧本科代码/`。
2. **profile 第 9 次"急于推进"防线第 10 次验证**：主线没讲清阶段 0.1 在干啥就直接甩 4 个降级选项。用户原话"啥玩意？咱们先说说这是要干啥？"。防线：进入任何阶段前先一句话讲清"在干啥+为什么"，再给选项。

### 来源

S002（本轮）+ 本地代码核查（`毕设/旧本科代码/PSKTimingErrDetector.m` + `Tx2Rx.m`）+ B7 poster 全文核查 + Gardner 1986 扫描原文核查 + 用户原话 voice 2026-07-08

## D002: B7 数学同族性 = 弱同族 (B) + 机制数值验证成立（0.2 通过，进 0.3）

> status: active
> date: 2026-07-08
> 取代：无（贯彻 H001 阶段 0.2 判定门控）
> 被取代：无
> 依据: 子 agent 数值重建（`explore/b7-gardner-ted-foe/_b7_map_results.json` + `_b7_map_summary.md`）+ 子 agent 同族性分析（`_lineage_check.md`）+ 主线 V5 独立重算（G(0)=0.132142 bit-exact + FFT 主频能量 95.9%/90.7%）+ B7 poster 全文（`content.md` L15/21/25/37）+ Gardner 1986 公式源（`PSKTimingErrDetector.m` L8-9）+ VV/BPS 实现（`_recovery.py` L78-118）
> 触发原话: 无（技术推导——基于数值重建 + 数学结构分析，非用户 voice 触发）

### 决策

**阶段 0.2 数学同族性 + 机制数值重建通过，进 0.3。**

1. **B7 机制（TED 增益↔Doppler 周期相关）数值验证成立**：G(f_D) 以 baud rate B=25 GHz 为周期，确定性铁证 G(0)=0.132142（主线 V5 重算 bit-exact），FFT 主频能量占比无噪 95.9% / OSNR 17dB 90.7%（>50% 阈值）。poster Fig.1a 那张 omitted 的图被成功重建。
2. **B7 vs Gardner 1986 = 弱同族 (B)**：共享底层 TED 公式（`e=Re{mid·(curr−prev)*}`），但任务正交（B7 做 FOE 估频偏 f_D，1986 做 STR 检测定时误差 τ）+ 后处理不同构（B7 扫频+峰反演+双候选+TED2 std 判决 vs 1986 环路滤波+NCO）。
3. **B7 vs VV/BPS = 非同族**：任务不同（FOE vs CPR）+ 核心运算无共享结构（B7 S-curve 峰反演 vs VV mean-angle of rx^M vs BPS argmin decision-distance）。**不存在 NDA-ML 式 mean-angle 等价陷阱**。
4. **poster "(−B,B) 可逆"描述不精确**：数值显示实际是 2:1 映射（U 形 1 转折点 @ ~13GHz），但双候选算法自洽（2:1 正好对应"生成两个 Doppler 候选"）。

### 理由

1. **INVARIANT 11 的"数学同族 = NDA-ML D-008 陷阱重演"针对的是强同族 (C)**——即跟祖师爷方法在数学运算层等价（如 NDA-ML 升幂 mean-angle vs VV 升幂 mean-angle，同为 CPR 任务）。B7 是 (B) 弱同族，任务正交，陷阱机制无法复现。

2. **0.2a 数值重建验证了 B7 机制不是 poster 文字吹的**——周期相关真实存在，且周期=baud rate 跟 poster "归一化到 baud rate"描述吻合。这是比"靠文字重建公式"更强的证据（实测 > 文字）。

3. **V5 独立核查通过**：子 agent 报 G(0)=0.13214，主线重算 G(0)=0.132142 bit-exact；FFT 主频能量主线重算 95.9%（子 agent 报 94.5%，差异因采样点数 coarse 24 点 vs diag 76 点，结论一致）。子 agent 原始数字可信。

### 排除的替代方案

- "B7 跟 1986 强同族 (C)，创新性受质疑"：否决。任务正交（FOE vs STR）+ 后处理不同构，不满足 (C) 的"数学运算层等价"判据。
- "B7 机制是 poster 文字描述无法验证，需切降级"：否决。0.2a 数值重建成功验证周期相关真实存在。

### 影响范围

- **0.3 架构定性**：进 0.3。用户本地代码 + B7 都是反馈环，前馈化决策需做（INVARIANT 12）
- **sandbox 三方对照**：① B7 proposed FOE（数值重建版，0.2a 脚本可复用）② Gardner 1986 定时环（用户代码当祖师爷方）③ PSA FOE baseline
- **论文叙事定位**（子 agent 建议采纳）：贡献定位为"任务重赋值（TED: τ→f_D）+ 增益-频偏可逆映射的新机制"，而非"新检测器公式"
- **残留风险**（带进 sandbox）：B7 未给 TED_gain(f_D) 解析式，无法排除跟 Leven M-th-power FOE [7] 等价。sandbox 前补解析推导 + 显式对比 Leven 2007

### 教训

1. **子 agent 方法学细节要审**：0.2a 子 agent 初版 OSNR 17dB 用单次噪声实现，G 曲线毛刺化使能量比掉到 61.6%（会误导周期判断），改为 6× 噪声实现平均后稳定至 87-91%。**数值实验的噪声处理方式直接影响结论**，主线审子 agent 报告时要看它的噪声处理是否合理。
2. **环境路径偏差要记录**：AGENTS.md 给的 `~/.venvs/torch/bin/python` 本机不存在，子 agent 用 scoop python311 跑通。后续 B7 sandbox/MVE 用 `python`（scoop）而非 AGENTS.md 写的路径。

### 来源

S003（本轮 0.2 执行）+ 子 agent 数值重建（`_b7_map_reconstruction.py` + `_b7_map_results.json` + `_b7_map_summary.md`）+ 子 agent 同族性分析（`_lineage_check.md`）+ 主线 V5 独立重算 + B7 poster 全文 + Gardner 1986 本地代码 + VV/BPS 实现

## D003: B7-Q1 架构定性 = FOE 前馈扫频 + Gardner TR 保留反馈环（不撞 D006）

> status: active
> date: 2026-07-08
> 取代：无（贯彻 H001 阶段 0.3 架构定性前置）
> 被取代：无
> 依据: D006 红线精确边界（`.sessions/2026-06-20-problem-driven-redirection/decisions.md` L313-355）+ B7 DSP 链拆解（`content.md` 行 47）+ B7 不涉湍流确认（`_B7-gardner-ted-increment.md` 关键发现 5）+ 用户代码架构核查（`Tx2Rx.m` L176-214 定时环 / L275-321 载波同步环）+ 0.2a 数值重建（前馈扫频已验证机制）
> 触发原话: 无（技术推导——基于 D006 边界分析 + B7 锚方法架构拆解，非用户 voice 触发）

### 决策

**B7-Q1 实现架构定死**：

1. **proposed FOE（B7 创新）= 前馈扫频**：CV mult1 扫频→S-curve 峰检测→双候选→TED2 std 判决→输出 f̂_D→前馈补偿 `rx·exp(−j2πf̂_D t)`
2. **Gardner TR（定时恢复）= 保留反馈环**：用户代码 Tx2Rx.m L176-214 直接复用。跟踪符号时钟 τ，不是湍流相位 φ_T，不撞 D006
3. **载波同步（CPR）= 前馈 VV/BPS 或反馈 PLL，禁建模湍流相位**：若用反馈 PLL，环路只跟 CFO 残余 + 激光相位噪声，不主动建模 φ_T（Paillier 经验性忽略，D006 兼容）

### 理由

1. **D006 Kill 的精确范围是"把湍流相位 φ_T 主动纳入载波同步环路 TF 联合建模"**，不是"所有反馈环"。B7 锚方法本身不涉湍流（poster 实验室纯 Doppler 模拟），FOE 前馈化后无环路 TF，Gardner TR 跟踪 τ 不是 φ_T → 三重不撞。

2. **poster 原算法结构本就是开环扫频**（CV mult1 在 (−B,B) 内扫频定位 TED 增益峰），前馈化合法不是强行改造。0.2a 数值重建就是前馈扫频验证的，周期相关照样成立 → 前馈化不破坏 B7 创新点。

3. **Gardner TR 保留反馈环是物理必需**——定时恢复需要反馈跟踪符号时钟，前馈化会破坏定时跟踪能力。但 Gardner TR 跟 D006 禁的"湍流相位进载波同步环路"是两个不同的环（TR 跟踪 τ，载波同步环跟踪 θ）。

### 排除的替代方案

- **"整个 B7 链路全前馈化"**：否决。Gardner TR 前馈化会破坏定时跟踪能力（定时恢复本质需要反馈）。只 FOE 前馈化，TR 保留反馈。
- **"B7 用反馈 PLL 做 FOE"**：否决。反馈 PLL 跟踪频偏需要环路 TF，若星地场景 θ 含湍流相位则撞 D006 边界。前馈扫频更安全且符合 poster 原算法结构。
- **"把 B7 扩展到湍流场景（Q2）做联合建模"**：不在 B7-Q1 范围。若未来扩 Q2，需单独做 D006 边界决策（前馈归一化不撞 vs 环路 TF 联合建模则撞）。

### 影响范围

- **0.4 公平对照**：FOE 前馈 vs PSA FOE（也前馈），公平。Gardner TR 两方共用（用户代码复用）
- **sandbox 三方对照**：① B7 proposed FOE（前馈扫频，0.2a `_b7_map_reconstruction.py` 扩展）② Gardner 1986 TR（用户代码祖师爷方）③ PSA FOE baseline
- **D006 边界监控**：sandbox/MVE 实现时若发现自己写了"把湍流相位进载波同步环路"→ 立即停（sim-preflight interrupt），这不是 B7-Q1 范围
- **B7 创新点叙事**：FOE 前馈化后，创新点 = "前馈扫频 + TED 增益峰反演 + 双候选判决"，仍是算法层创新（D002 弱同族 B 结论不受影响）

### 教训

1. **D006 红线要精确读边界**：D006 禁的不是"所有反馈环"，是"湍流相位主动建模进载波同步环路"。Gardner TR（定时环）跟载波同步环是两个不同的环，不能笼统判"反馈环撞 D006"。本轮初判时差点把 Gardner TR 也当成撞 D006，核查 D006 原文 + 用户代码架构后才区分清。

### 来源

S003（本轮 0.3 执行）+ D006 原文 + B7 DSP 链拆解 + 用户代码架构核查 + 0.2a 数值重建

## D004: B7 fair gain = 二维报告（BER gain @ 双工作点 + Doppler 范围比）+ PSA FOE baseline 必须重写（0.4 通过）

> status: active
> date: 2026-07-08
> 取代：无（贯彻 H003 阶段 0.4 公平对照框架设计）
> 被取代：无
> 依据: NDA-ML vs B7 公平对照维度对比（`SC-NDA-ML-MVE-SPEC.md` §4 pilot overhead vs B7 content.md L19/L49 无 pilot overhead）+ B7 锚论文量化三数（content.md L21/49/65/69）+ common `_recovery.py:435` psa_foe_recovery 概念错核查 + N1-MVE-SPEC.md §2 TL-20 预期表模板 + 用户决策（voice 2026-07-08 对话 4）
> 触发原话: 用户选"BER 2e-2 + HD-FEC 双工作点（推荐）"

### 决策

**阶段 0.4 公平对照框架定死**：

1. **fair gain = 二维报告，不合成单一指标**：
   - 维度 1：BER gain @ 双工作点（HD-FEC 3.8e-3 主判据 + BER 2e-2 锚论文一致性校验）
   - 维度 2：Doppler 估计范围比（B7 可估准上限 / PSA FOE 可估准上限，预期 ≈1.9×）
   - 理由：B7 增量半在 BER gain（0.6dB）半在范围（1.9×），单一指标丢信息
2. **工作点 = HD-FEC 主判据 + BER 2e-2 锚校验**（用户决策）：
   - HD-FEC 3.8e-3 跟 NDA-ML 跨候选可比（FR-15 目标 baseline 对照）
   - BER 2e-2 跟 B7 锚论文对齐，实测应 ≈0.6dB，偏离 >0.2dB 触发 TL-20
3. **PSA FOE baseline 必须 sandbox 重写**（谱不对称法 Vieira 2023，非 pilot-aided）
4. **PSA FOE >12GHz 失败判据**：A（BER 爆 >1e-1）+ B（FOE 估计漂零偏离真值 >50%），主用 A 作 fair gain 边界

### 理由

1. **NDA-ML 的 fair gain 框架不能照搬**——NDA-ML vs DA ML 有 pilot overhead 差异（1.25dB），B7 vs PSA FOE 无 pilot overhead 差异（两者都盲前馈 FOE）。照搬会把不存在的 1.25dB 代价塞进 B7 fair gain，污染对比。

2. **范围维度不能硬合成 BER gain**——0.6dB BER gain 偏小（D005 会议门槛偏弱），1.9× 范围是结构性优势（非边际 dB）。合成"等效 dB"会引入主观加权（1.9× 范围值多少 dB？无客观答案）。二维报告让读者自行判断，更诚实。

3. **双工作点平衡跨候选可比 + 锚论文真实性**——HD-FEC 单独不够（B7 0.6dB 是 BER 2e-2 实测，HD-FEC 是外推），BER 2e-2 单独不够（跟 NDA-ML 不可比）。双工作点：HD-FEC 作主判据保证跨候选排序，BER 2e-2 作锚校验保证 B7 复现不失真。

### 排除的替代方案

- **"fair gain = 单一 BER gain @ HD-FEC"**：否决。丢失 1.9× 范围维度，且 B7 0.6dB 在 HD-FEC 是外推非实测。
- **"fair gain = 单一 BER gain @ BER 2e-2"**：否决。跟 NDA-ML 不可比（NDA-ML 在 HD-FEC），跨候选排序需额外换算。
- **"B7 场景统一到 NDA-ML 2.5GBaud"**：否决（用户决策）。重蹈 NDA-ML D-007 覆辙（场景重定义后增量消失）。

### 影响范围

- **sandbox 三方对照**：B7 proposed FOE / Gardner 1986 TR / PSA FOE，fair gain 按 §1 二维报告
- **TL-20 理论预期表**（已落盘 `_fair_comparison_framework.md` §5）：BER gain @ BER 2e-2 预期 +0.4~0.8dB，@ HD-FEC 预期 +0.3~0.7dB，range_ratio 预期 ≈1.9×
- **PSA FOE baseline 债务**：common `_recovery.py:435` psa_foe_recovery 概念错，sandbox 必须重写
- **跨候选排序**：B7 主判据 HD-FEC BER gain（跟 NDA-ML 对齐），辅维度范围比

### 教训

1. **读 baseline 实现不能只看函数名**：`psa_foe_recovery` 函数名叫 PSA FOE，实现是 pilot-aided（注释 L437 自承）。概念错。若 sandbox 直接用这个函数当 B7 baseline，会得到"B7 vs pilot-aided FOE"的对照（不是 poster 的谱不对称法），结论失真。V6 FR-26 读原文数值的精神延伸：读 baseline 实现要核查实现跟名字/文献是否一致。

### 来源

S004（本轮 0.4 执行）+ NDA-ML fair gain 框架 + B7 锚论文量化 + common _recovery.py 概念错核查 + N1-MVE-SPEC §2 模板 + 用户决策

## D005: B7Params 修正版（15 字段全溯源）+ B7 锚论文原参数不跟 NDA-ML 统一（0.5+0.6 通过，阶段 0 全部收尾）

> status: active
> date: 2026-07-08
> 取代：无（贯彻 H003 阶段 0.5 参数真相源 + 0.6 文件组织）
> 被取代：无
> 依据: B7 content.md 参数行号溯源（L21/L25/L47/L49/L65/L69）+ params.py 现有 B7Params L606-680 核查（3 问题）+ D-007 教训（场景重定义后增量消失 + 下游引用同步）+ 用户决策（voice 2026-07-08 对话 4 B7 锚论文原参数）
> 触发原话: 用户选"B7 用锚论文原参数 25GBaud/1.8kHz（推荐）"

### 决策

**阶段 0.5 参数真相源 + 0.6 文件组织定死**：

1. **B7Params 修正版草稿**（在 explore 草拟，sandbox 回写 params.py，守 INVARIANT 6 阶段 0 不写代码）：
   - 15 字段全标 source_type + source（精确到 content.md 行号）+ audit_flag
   - 14 OK + 1 WARNING（GARDNER_GAIN 典型值）
   - 修正 LEO_DOPPLER_RATE（30e3 错 → 1e9 Hz/s，content.md L47「1 GHz/s」）
   - 删 PSA_PILOT_SPACING（概念错遗留，PSA FOE 是谱不对称法不用 pilot）
   - 补 7 新字段：R_SYM_B7（25GBaud）/ LASER_LW_B7（1.8kHz）/ ROLL_OFF（0.1）/ RX_BW_GHZ（36.75GHz）/ SPS_RX（2.94）/ DOPPLER_INTERVAL（1GHz）/ LEO_DOPPLER_EXCURSION（±100MHz）
2. **符号率/线宽场景不跟 NDA-ML 统一**（用户决策）：
   - B7 用锚论文原参数 25GBaud/1.8kHz
   - NDA-ML 用 SystemParams 2.5GBaud/10kHz
   - 跨候选可比性通过 fair gain 维度统一（都报 HD-FEC，D004），不通过场景参数统一
   - 理由：复现 B7 0.6dB 增量必须用 B7 场景参数，防重蹈 NDA-ML D-007 覆辙
3. **B7Params 不合并进 SystemParams**：两套独立（B7 是 B7 仿真真相源，SystemParams 是 NDA-ML 仿真真相源）
4. **下游引用同步清单**（D-007 教训 2）：5 个文件核查，4 无需改 + 1 sandbox 重写（psa_foe_recovery）
5. **explore 目录结构落盘**：阶段 0 产出 8 文件（含本轮 2 新建）+ sandbox/MVE 待建 6 文件命名规约

### 理由

1. **TL-26 + FR-26 V6 要求参数溯源不只引位置要读原文数值**——旧 B7Params 多数 source 只写"B7 OFC 2026"没行号，LEO_DOPPLER_RATE 直接错（30kHz/s 是 Paillier/sat.1553 值，B7 原文给的是 ±100MHz@1GHz/s）。修正版所有 literature 字段 source 精确到 content.md 行号。

2. **符号率/线宽场景不统一是 D-007 教训的直接应用**——NDA-ML D-007 的教训就是"场景重定义后增量消失"（500kHz→10kHz 后 NDA-ML 增量从预期 0.3-0.8 变成实测 1.351，看似变大但叙事需重写）。B7 0.6dB 是 25GBaud/1.8kHz 场景实测，换到 2.5GBaud/10kHz 后增量数值不可预测，复现失真风险高。

3. **B7Params 不合并进 SystemParams 避免 D-007 式单字段真相源混淆**——D-007 把 B11 OFDM 场景参数（500kHz/25GBaud）跟单载波场景参数（10kHz/2.5GBaud）混在 B11Params 一个类里，靠 audit_flag=DEAD 标记区分，后续易误用。B7Params 独立，跟 SystemParams 物理隔离，无混淆空间。

### 排除的替代方案

- **"B7Params 合并进 SystemParams 加场景开关"**：否决。SystemParams 是 NDA-ML 真相源，加 B7 场景开关引入耦合，违反单字段真相源原则。B7Params 独立。
- **"统一到 NDA-ML 场景 2.5GBaud/10kHz"**：否决（用户决策）。重蹈 D-007 覆辙。
- **"B7Params 直接回写 params.py"**：否决（本轮）。INVARIANT 6 阶段 0 不写代码，草稿在 explore，sandbox 阶段回写。

### 影响范围

- **阶段 0 全部收尾**：0.1-0.6 六项规约全通过（D001-D005），可进 sandbox
- **sandbox 第一步**：B7Params 回写 params.py（本文件草稿 §1.2）
- **sandbox 第二步**：PSA FOE baseline 重写（谱不对称法）
- **跨候选参数隔离**：B7Params（B7 真相源）vs SystemParams（NDA-ML 真相源），common/_channel.py 按候选 import
- **profile 第 9 次防线解除**：阶段 0 六项全做完，sandbox 合法

### 教训

1. **现有 params.py 字段要 V6 核查不只看 source 字段有没有，要看值对不对**：旧 B7Params 的 LEO_DOPPLER_RATE source 写"B7 OFC 2026"看似有溯源，实际值 30e3 是 Paillier 值不是 B7 原文值。V6 读原文数值不只是引位置，要核对数值本身。

### 来源

S004（本轮 0.5+0.6 执行）+ B7 content.md 参数行号溯源 + params.py 现有 B7Params 核查 + D-007 教训 + 用户决策

## D006: PSA FOE coarse-only 线性区 ~1GHz 限制登记 + Leven DOI 修正（sandbox 步骤 2-3 诚实发现）

> status: active
> date: 2026-07-08
> 取代：无（D004 PSA FOE baseline 债务的执行收尾 + D002 残留风险的闭合确认）
> 被取代：无
> 依据: 子 agent PSA FOE 重写（`_psa_foe_asymmetry.py` + `_psa_foe_asymmetry_results.json` + `_psa_foe_asymmetry_summary.md`）+ 子 agent TED_gain 解析推导（`_ted_gain_analytic.py` + `_ted_gain_analytic_results.json` + `_ted_gain_analytic_summary.md`）+ 主线 V5 独立核查（G(0) bit-exact + 周期三角恒等式 + Leven 同族三层运算不等价 + PSA 线性区物理一致）+ Vieira 2023 原文（`papers/doi/10.1109_access.2023.3287501/content.md` L343-347）+ Leven 2007 原文（`papers/doi/10.1109_lpt.2007.891893/content.md` L33-65）
> 触发原话: 无（技术推导——sandbox 执行的诚实发现，非用户 voice 触发；PSA 弱发现是子 agent 主动报告 + 主线独立核查确认）

### 决策

**sandbox 步骤 2-3 产出登记（3 项）**：

1. **PSA FOE coarse-only baseline 线性区 ~1GHz 限制**（步骤 2 诚实发现）：
   - 单-α 谱不对称法在 25GBaud/β=0.1 场景线性区仅 ~1GHz，f_D≥2GHz 全 failA（|Δf̂−f_D|>0.5GHz）
   - 物理根因：β=0.1 RRC 谱尖边缘，ln(P+/P−) 在 f_D 超过谱边缘带宽 ~1.25GHz 后饱和；aliasing 上界半 baud 12.5GHz 是"不混叠"上界不是"线性估准"上界
   - 跟 B7 poster content.md L19 "fails beyond 12 GHz" 不冲突——poster 只给 aliasing 上界，没给线性区下界实测；子 agent 测的 ~1GHz 是更保守的真实测量
   - **不是 bug，不是红线警报**。登记为 sandbox 已知限制
2. **fair gain 含义修正**：PSA coarse-only 太弱 → B7 vs PSA 的 BER gain 是**上界**（baseline 弱则候选显得强），不是紧下界。三方对照（对话 6）记录此限制。可选补 fine CFE stage 作双方对称增强（V3 公平性），但不强制（B7 本就是 coarse 扫频，fair 比较）
3. **Leven 2007 DOI 修正**：B7 poster ref[7] Leven PTL 2007 正确 DOI = **10.1109/LPT.2007.891893**（非 task brief 笔误的 891597）。论文已落盘 `papers/doi/10.1109_lpt.2007.891893/`，作者 Leven/Kaneda/Koc/Chen，PTL vol.19 no.6 pp.366-368

**D002 残留风险闭合确认**（步骤 3）：B7 跟 Leven = 弱同族 (B)，不降级 (C)。
- G(f_D) = K_max·|cos(π·f_D/B)| 解析成立（f_D 依赖性解耦为余弦因子，与脉冲形状无关）
- Leven 是时域 phase-increment mean-angle（`y_k·conj(y_{k-1})` → `^4` → mean-angle），非频域 FFT 谱峰
- 三层运算不等价（乘积结构/非线性/聚合）→ 不满足 (C) "核心运算层等价"判据

### 理由

1. **PSA 弱发现必须诚实登记而非隐藏**：profile「质量标准 - 没有新鲜验证证据不宣称完成」+「急于推进」防线。子 agent 主动报告 PSA baseline 弱是诚实信号，主线若当作"baseline 实现问题"忽略会重蹈 NDA-ML D-008 覆辙（接受弱 baseline 让候选显得强）。登记为已知限制 + fair gain 上界含义修正，让后续 MVE 结论带 caveat。

2. **PSA 弱不阻断 sandbox 推进**：D005 务实路线（INVARIANT 最高优先级）下，B7 贡献是"赢传统 baseline 几 dB"。PSA coarse-only 弱 → B7 赢它不费吹灰之力，但这不否定 B7 的范围优势（1.9×）和低 SNR 鲁棒性（OSNR 10dB）——这两个维度跟 PSA 弱无关。MVE 报告时区分"BER gain 上界（vs 弱 PSA）"和"范围/鲁棒性结构性优势"。

3. **Leven 同族判定用解析证据不用直觉**：D-009 教训 6「只信原始数字不信归因」。本决策的同族判定不是凭"B7 时域 Leven 频域"直觉，而是基于 G(f_D) 解析式 + Leven 公式提取后的三层运算逐项对比（乘积结构/非线性/聚合），每层都有具体公式证据。

### 排除的替代方案

- **"PSA 线性区 ~1GHz 是实现 bug，重写修正"**：否决。主线 V5 独立核查确认 β=0.1 谱边缘 ~1.25GHz 跟线性区 ~1GHz 物理一致，且子 agent 的 α 标定方法忠实复现 Vieira 的 sequential search。这是真实物理限制不是实现问题。
- **"PSA 弱触发 B7-Q1 重新评估或 Kill"**：否决。D005 务实路线 + profile「务实可毕业」。PSA 弱是 baseline 选择问题不是 B7 方法问题。B7 的范围/鲁棒性优势独立成立。
- **"B7 vs Leven 强同族 (C)，重新定位贡献"**：否决。步骤 3 解析推导 + 三层运算对比确认 (B) 弱同族，D002 残留风险闭合。
- **"补 fine CFE stage 给 PSA 作公平对照"**：可选非强制。留到对话 6 三方对照时按 fair-comparison framework 决定（若补，双方对称补，不只给 PSA 补）。

### 影响范围

- **对话 6 三方对照（C7+V2）**：PSA FOE baseline 用 `_psa_foe_asymmetry.py`（谱不对称法，非 pilot-aided）。记录 PSA coarse-only 弱限制，BER gain 标为上界
- **MVE 报告叙事**：B7 贡献分两维报告——① BER gain vs PSA（上界，因 PSA coarse-only 弱）② 范围 1.9× + OSNR 10dB 鲁棒性（结构性优势，跟 PSA 弱无关）
- **D002 残留风险闭合**：sandbox 步骤 3 完成，弱同族 (B) 确认。INVARIANT 11 不变（Gardner 1986 祖师爷警报仍在，对话 6 V3 红线）
- **论文引用**：Leven 2007 DOI 用 10.1109/LPT.2007.891893（修正笔误）
- **B7 锚方法解析式资产**：G(f_D) = K_max·|cos(πf_D/B)| 可进论文 §2 原理推导（poster 缺这个解析式，本 sandbox 补上，是论文增量）

### 教训

1. **子 agent 诚实报告"反常发现"要重点核查而非忽略**：步骤 2 子 agent 主动报"PSA 线性区 ~1GHz 远低于声称 12.5GHz"是诚实信号。主线 V5 独立核查物理机制（β=0.1 谱边缘）后确认非 bug。若主线当作"实现问题"忽略，会在对话 6 三方对照时得到虚高的 BER gain，重蹈 NDA-ML D-008（接受弱/错 baseline 让候选显得强）覆辙。
2. **C6 公式核对 PDF→md omitted 要标降级但区分"显示公式丢"vs"推导丢"**：Vieira content.md L345 显示公式 omitted 但 L347 prose 完整，read-note 记录闭合形式 → 非降级。Leven content.md L39-53 多个公式 omitted 但 L33-65 THEORY 文字描述清晰 → 半降级（公式形式靠文字+标准理论恢复）。区分两类 omitted 避免一刀切判"公式不全切降级"。
3. **DOI 笔误要核查真实落盘**：task brief 写 Leven DOI `891597`，子 agent 发现实际是 `891893`（差一个数字）。FR-26 证据链要求不只信 brief 写的，要核查论文真实落盘。

### 来源

S005（本轮 sandbox 步骤 1-3 执行）+ 子 agent PSA FOE 重写产出 + 子 agent TED_gain 解析推导产出 + 主线 V5 独立核查 + Vieira 2023 原文 + Leven 2007 原文

---

## D007: LPF2 不公平 bug 登记 + BER gain 虚高结论 + 范围优势机制本质确认（非 B5 特权假象）

> status: active
> date: 2026-07-09（对话 7，V5 核查未记录 MVE 数据 + 范围优势公平性审计）
> 取代：无（D006 PSA 弱限制扩展确认 + B5 D003 先例对 B7 的适用性裁定）
> 被取代：无
> 依据: V5 主线独立核查（`_mve_results.json` + `_mve_osnr_sweep_results.json` 原始 JSON 重算）+ systematic-debugging Phase 1-3（`_lpf2_fairness_check.py` + `_lpf2_fairness_results.json`）+ 范围优势公平对照（`_scope_fairness_check.py` + `_scope_fairness_results.json`）+ 4thpow 4 次方数学混叠分析 + B5 D003 先例（`2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md` D003 实验 B）
> 触发原话: 用户 "我咋感觉这个讨论进行过？然后当时是发现范围也是有问题。你要不翻一翻日志?"（指引翻日志找到 B5 D003 先例，触发 B7 范围优势公平性审计）

### 决策

**3 项登记**：

1. **LPF2 不公平 bug**（b7_gardner_ted_mve.py L851）：B7 下游链加了 `_lpf2`（13.75GHz butter 低通），其他 baseline（PSA/4thpow/Kay）全没有。这是 apples-to-oranges 不公平对照。**根因**：未记录对话（Jul 8 09:45-11:40 跑正式 MVE 那次）改脚本时只给 B7 加了 LPF2（poster content.md:65 说 LPF2 是 B7 的 0.6dB 来源），但 fair comparison 要求隔离 FOE 增量时 LPF2 要么全加要么全不加。

2. **BER gain 虚高结论**：原 MVE 的 +4.08dB（B7 vs PSA @ BER 2e-2, f_D=5GHz）是三重虚高——
   - ① LPF2 不公平独享 ~0.6-0.8dB（Phase3 验证：全加 LPF2 后 B7 vs 4thpow gain 从 +0.65→+0.03dB）
   - ② PSA baseline 偏弱 ~2dB（D006 已登记 coarse-only 弱，本轮确认即使加 LPF2 仍弱 +2.49dB）
   - ③ Kay est_err=1.01GHz 适配问题（线性区内不该偏这么多）
   - **公平条件下 B7 FOE 方法本身 vs 4thpow gain≈0（+0.03dB）**。BER gain 维度 SPEC §5 FAIL（不满足 D005 "赢传统 baseline 几 dB"）。

3. **范围优势机制本质确认（非 B5 特权假象）**：用户提示翻日志找到 B5 D003 先例（范围优势给 baseline 配同等条件后归零）。B7 做了相同的公平范围对照 + 数学本质分析，结论与 B5 根本不同——
   - 4thpow 范围限制 = 4 次方数学混叠 ±fs_rx/(2M) = ±6.25GHz（M=4, fs=50GHz），**铁律不可突破**
   - B7 G(f_D)=K_max·|cos(πf_D/B)| 周期=2B=50GHz，单边扫频 0-25GHz 无模糊（D006 解析式闭合）
   - 实测印证：4thpow f_D=5GHz（范围内）err=0；f_D=12/15/23GHz 全混叠估错
   - **B7 范围优势 vs 4thpow 是机制本质差异（TED 周期相关 vs 4 次方混叠），非特权假象**

### 理由

1. **BER gain≈0 是公平对照后的真实结论**：Phase3 最小化验证（全加 LPF2）直接证明 B7 FOE 方法本身在线性区内 vs 4thpow 没有真实 BER 增量。这不是"B7 弱"而是"B7 的贡献不在 BER gain 在范围"——B7 的扫频机制跟 4thpow 在线性区内都能估准 f_D，BER 自然趋同。B7 的差异化在半 baud 外（4thpow 数学上够不着）。

2. **范围优势不能用 B5 D003 逻辑 Kill**：B5 范围优势是特权假象（给 baseline 星历后归零，D003 实验 B 实测）。B7 的 baseline 限制（4thpow 4 次方混叠）是数学铁律，给任何条件都无法突破。两者根因不同——B5 是"人为限制 baseline"，B7 是"baseline 数学本质限制"。

3. **未记录对话的治理问题单独登记**：正式 MVE 在 Jul 8 09:45-11:40 跑完但无 S### 记录、未提交、脚本改 +377 行无审计。本轮 V5 核查发现 LPF2 bug 正是因为核查了未记录的产物。治理教训：MVE 跑数必须同步写 S### + 提交，否则产物不可溯源。

### 排除的替代方案

- **"B7 范围优势是特权假象，按 B5 逻辑 Kill"**：否决。4thpow 4 次方数学混叠是铁律（±6.25GHz），B7 TED 周期相关覆盖全 ±B。公平对照（全加 LPF2）后 4thpow 在 >6.25GHz 仍全爆（数学限制），B7 仍稳定。机制本质差异非特权。
- **"BER gain≈0 直接 Kill B7"**：否决。范围优势真实（机制本质）+ V3 不触发 + OFC 2026 poster 已发（0.6dB+1.9×范围会议先例）。BER gain 维度 FAIL 但范围维度 PASS，是 Conditional Go 候选非 Kill。最终 Go/Kill 交用户。
- **"无视 LPF2 bug 直接用 +4.08dB 判 Go"**：否决。profile「质量标准 - 没有新鲜验证证据不宣称完成」+「急于推进」防线。虚高数据判 Go 是自欺。
- **"立即修脚本重跑拿干净数据"**：pending 用户决策。Phase3 验证已证明公平条件下 gain≈0，重跑全 MVE 只是确认非新信息。

### 影响范围

- **BER gain 叙事**：原 +4.08dB 标为虚高（LPF2 不公平），公平条件下 B7 vs 4thpow gain≈0。MVE 报告 BER gain 维度 FAIL。
- **范围优势叙事**：2.1× 真实（机制本质 vs 4thpow 4 次方限制），可作 B7 主贡献。但需论证"范围优势单独够不够 D005 会议门槛"。
- **b7_gardner_ted_mve.py L851 债务**：LPF2 不公平 bug 待修（全加或全不加），修后重跑拿干净 BER gain 数据。修不修 + 重跑不重跑交用户。
- **B5 D003 先例适用边界**：B5（特权假象→Kill 路径1）vs B7（机制本质→不能用 B5 逻辑 Kill）。后续候选若声称范围优势，公平对照判据 = "baseline 限制是人为还是数学本质"。

### 教训

1. **fair comparison 要审下游链不只审 FOE 估准精度**：本轮 LPF2 bug 在下游链（FOE 补偿后 TR 前的信号预处理），不在 FOE 估准环节。B5 D003 的不公平在采样率/星历（信号生成端）。fair comparison 审计要覆盖全链路（信号生成→FOE 估计→下游预处理→TR→判决），不只看 FOE est err。
2. **范围优势公平对照判据 = baseline 限制是人为还是数学本质**：B5 baseline 限制是人为（没给星历/采样率）→ 给条件后归零 → 特权假象。B7 baseline 限制是数学本质（4 次方混叠）→ 给任何条件都无法突破 → 机制本质。判范围优势真假先问"baseline 为什么够不着"。
3. **未记录的 MVE 产物必须 V5 核查不能用**：未记录对话跑了正式 MVE 但无 S### + 未提交 + 脚本改了无审计。主线直接信任会接受 LPF2 不公平的虚高数据。V5「只信原始数字不信归因」扩展为「未记录产物连原始数字都要核查实现公平性」。
4. **用户记忆比 agent 状态记录可靠**：用户"感觉这个讨论进行过"直接指引找到 B5 D003 先例，避免了主线把 B7 范围优势当真实却不做公平对照的错误。profile「用户不懂 DSP 细节但把握方向」——用户的方向性记忆（"范围也有问题"）比 agent 的技术结论更值得追查。

### 来源

S007（本轮 V5 核查 + Phase3 验证 + 范围公平对照）+ `_mve_results.json` + `_mve_osnr_sweep_results.json`（未记录对话产出）+ `_lpf2_fairness_check.py`/`_results.json` + `_scope_fairness_check.py`/`_results.json` + B5 D003 先例（`2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md`）+ 用户原话 voice 2026-07-09
