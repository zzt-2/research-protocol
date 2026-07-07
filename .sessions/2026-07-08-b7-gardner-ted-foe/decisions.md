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
