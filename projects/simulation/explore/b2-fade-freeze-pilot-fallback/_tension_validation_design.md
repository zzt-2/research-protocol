# 阶段 0.1：核心命题张力验证设计（step4a 实测反证 vs B2-Q2 命题的 fair comparison）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 0.1（B2 最高优先）
> 日期: 2026-07-08
> 守: INVARIANT 11（核心命题张力首验证）+ V2 三方对照 + V3 祖师爷警报 + 不变量 10（核查机制中性双向）
> 输入: `_step4a_detail_extract.md`（子 agent T### 核查 + 主线 grep/python 独立验证）

## 0. 张力陈述（事实层，已核查）

**B2-Q2 核心命题**（`_B2-deep-fade-freeze-increment.md:67`）：
> "sat.1553 L440 提 pilot-based 相位估计在 fade 比 VV+diff 好 1 dB——暗示 fade 期间/恢复期用 pilot-aided FOE/PE 可能比纯 blind freeze 更优"
→ B2-Q2 改进空间 = pilot-aided fallback 在 fade 比 blind freeze 更优（双模切换）

**step4a 实测反证**（`step4a-mve-execution/decisions.md:150, 157`，主线已核对原始数字）：
> D004 L157："形态 C（湍流）: DA pilot 在 deep fade 处 BER 崩溃（5dB weak 0.38 vs NDA 0.29），NDA 全帧积分对单点 fade 鲁棒"
> 测试条件：γ_d=5dB（weak GG α4/β3），DA pilot spacing=4（25% overhead, 真符号 pilot），每 256 符号块 64 pilot，每 100 符号 fade 块约 25 pilot

**张力**：B2-Q2 主张 "pilot-aided fallback 在 fade 比 blind 更优"，step4a 实测 "pilot-aided（DA ML）在 fade 反而比 blind（NDA-ML）差"。两者在**单载波时域、相同信道、相同调制（16-APSK）**下直接打架。

## 1. 张力的物理结构分解（为什么会出现这个张力）

### 1.1 step4a DA ML 在 fade 崩溃的机制（已核查原文 + 代码层面归因）

**核心机制**（SPEC.md L12 + D004 L157）：
- DA ML 用每块 64 pilot（256 符号块 / spacing=4）做 pilot-aided 估计
- 当某 pilot 位置落入 deep fade 块（h 低），pilot SNR 暴跌 → φ̂ 噪声大 → BER 高
- NDA-ML 用全块 256 符号升幂 mean-angle，单点 fade 被 dilute（平均掉）→ 鲁棒

**代码层面的尺度关系**（主线 grep 核查 `_time_domain_crlb.py` + python 数值验证）：
- fade 块（信道 h 恒定单元）= CH_BLOCK = **100 符号**（`params.py:476`）
- pilot spacing = **4 符号**（`_time_domain_crlb.py:122`）
- → 每 fade 块约 **25 pilot**（100/4）
- 逐块恢复块 N_DFT = **256 符号**（跨 2.56 个 fade 块）

**关键观察（原文未讨论，阶段 0.1 新发现）**：
1. **pilot spacing（4 符号）远小于 fade 块（100 符号）**：pilot 在 fade 块内是密集的（25 pilot/fade 块），不存在"pilot 太稀疏错过 fade"的问题。DA pilot 崩溃**不是因为 pilot 不够密**
2. **DA 崩溃的真实机制是 pilot 跟数据同信道**：pilot 落在 fade 块里时 pilot SNR 跟数据符号 SNR 一样低，64 pilot 平均无法补偿 fade 深度（deep fade h² 远低于均值）
3. **NDA 鲁棒的机制是全块平均**：256 符号横跨 ~2.56 个 fade 块，全块平均把 deep fade 块跟正常块拉平，单点 fade 被 dilute

### 1.2 sat.1553 +1dB 的口径（已核查 `_cut-b1b2b3-verify.md:144-145, 342`）

**sat.1553 L440 原口径**：
- "Viterbi–Viterbi + differential coding 在 scenario 4 penalty ~1.5 dB"
- "pilot 在 scenario 4 比 VV+diff 好 1 dB"
- 即 +1dB = **pilot-aided 相位估计（PE）vs VV+差分编码（diff）** 的对比
- scenario 4 = 上行强湍 σp²(Rytov)=0.25（OFDM 系统）

**与 B2-Q2 的口径差异**（阶段 0.2 详查，此处先锁定边界）：
- sat.1553 对比的是 **PE 方法**（pilot-aided 相位估计 vs VV+差分编码），不是 **FOE freeze 双模切换**
- sat.1553 场景是 **OFDM scenario 4**，不是单载波时域
- sat.1553 baseline 是 **VV+差分编码**，不是 blind freeze（[79] Matsuda 机制）
- → **sat.1553 +1dB 不能直接当 B2-Q2 的增量**

## 2. 张力的 4 维度分解（fair comparison 设计）

> 目标：把"B2-Q2 命题 vs step4a 实测"的张力分解为 4 个可独立验证的维度。每个维度有明确的"如果是 X 则命题可验证 / 如果是 Y 则命题崩塌"判据。

### 维度 A：pilot 配置（spacing / 密度 / 类型）

**step4a 配置**：spacing=4，真符号 pilot，25% overhead，每 fade 块（100 符号）25 pilot

**张力分解**：
- **假设 A1（pilot 不够密）**：step4a spacing=4 在 fade 不够密 → 换 spacing=2（50% overhead）或 spacing=1（连续 pilot）能改善 DA 在 fade 的表现
  - **物理判据**：pilot spacing < fade 相干时间 → A1 不成立（spacing=4 符号 = 1.6ns，fade 块 100 符号 = 40ns，pilot 远比 fade 密）
  - **主线核查结论**：A1 **不成立**。pilot 在 fade 块内已密集（25 pilot/fade 块），DA 崩溃不是 spacing 问题
- **假设 A2（pilot 类型错）**：step4a 真符号 pilot 在 fade 块 h 低时 SNR 暴跌 → 换"功率提升 pilot"（pilot 符号幅度 +3dB）能改善
  - **物理判据**：pilot 功率提升能补偿 fade 深度，但代价是 pilot overhead 从 1.25dB 升到更高
  - **验证方式**：sandbox 加一组"power-boosted pilot"对照（pilot 幅度 ×2，overhead 重算）

**维度 A 判定**：张力**部分可分解**。spacing 不是问题（A1 不成立），但 pilot 功率/类型（A2）是可探索维度。**不过 A2 已经偏离 B2-Q2 原命题（双模切换），变成"pilot 设计优化"了**。

### 维度 B：fallback 触发条件（fade 检测门控）

**step4a DA ML**：全程 pilot-aided（不是 fallback），无 fade 检测门控，每块都跑 DA ML

**B2-Q2 双模切换**：(blind + 功率阈值 gating) ↔ (pilot) 模式切换

**张力分解**：
- **假设 B1（触发条件机制差异）**：step4a DA 是"全程 pilot"，B2-Q2 是"fade 时切 pilot"。机制根本不同——B2-Q2 只在 fade 期间用 pilot，非 fade 期间用 blind。如果 blind 在非 fade 期跟 NDA-ML 一样好，pilot 在 fade 期提供额外信息，则 B2-Q2 可能比纯 NDA-ML 更优
  - **物理判据**：fade 期间 blind freeze（[79] 机制）会丢失跟踪，恢复时需重收敛；pilot-aided 在 fade 期间能继续跟踪 → fade 恢复时间更短
  - **关键差异**：step4a 测的是**稳态 BER**（无 freeze/恢复动态），B2-Q2 测的是**fade 恢复动态**（freeze 后重收敛时间）
  - **这是 step4a 实测反证 vs B2-Q2 命题的最大差异点**：step4a 是静态 BER 对比，B2-Q2 是动态恢复对比
- **假设 B2（门控阈值敏感性）**：fade 检测功率阈值设错会导致误触发（正常波动当 fade）或漏触发（真 fade 没切）
  - **验证方式**：sandbox 扫阈值（γ_th ∈ [γ_mean−3σ, γ_mean−1σ]），看 B2-Q2 对阈值的敏感性

**维度 B 判定**：张力**可分解**。step4a 静态 BER 对比 vs B2-Q2 动态恢复对比是**不同测度**。B2-Q2 的增量可能不在稳态 BER 而在 fade 恢复时间。**这是 B2-Q2 命题最可能站住的维度**。

### 维度 C：pilot-aided 类型（DA ML vs PSA FOE vs 其他）

**step4a 用 da_ml_recovery**（`_recovery.py:136`）：pilot-aided ML 联合估 (φ, Δf)，闭式线性回归

**B2-Q2 可选估计器**（INVARIANT 14 复用基建边界）：
- `da_ml_recovery`（L136）：pilot-aided ML（step4a 用的，在 fade 崩溃）
- `psa_foe_recovery`（L435）：Pilot-Aided FOE（B7 baseline，step4a 未调用）
- `fft_foe`（L37）：blind 4 次幂 FOE（QPSK 专用，16-APSK 不适用）

**张力分解**：
- **假设 C1（DA ML 算法本身在 fade 弱）**：da_ml_recovery 闭式线性回归在 fade 块 h 低时数值不稳定 → 换 PSA FOE 或别的 pilot-aided 算法可能改善
  - **物理判据**：DA ML 用 pilot 位置 h 估 (φ, Δf)，fade 块 h 低 → φ̂ 噪声大。PSA FOE 只估 FOE 不估 CPE，机制不同
  - **验证方式**：sandbox 三方对照 da_ml / psa_foe / 别的 pilot-aided 在 fade 的表现差异
- **假设 C2（pilot-aided 路线在单载波时域根本弱）**：所有 pilot-aided 算法在单载波时域 fade 都打不过盲估（因为 pilot 跟数据同信道，fade 同步影响两者）
  - **物理判据**：这是**最危险的假设**——如果 C2 成立，B2-Q2 核心命题崩塌
  - **判据**：sandbox 三方对照（da_ml / psa_foe / power-boosted pilot）如果全在 fade 输给 NDA-ML，则 C2 成立

**维度 C 判定**：张力**部分可分解**。C1（换算法）可验证，但 C2（路线根本弱）是红线风险。**sandbox 必须回答 C2**。

### 维度 D：信道场景（单载波时域 vs OFDM vs 星地上行强湍）

**step4a 场景**：单载波时域，16-APSK，2.5GBaud，GG 块衰落 weak α4/β3

**sat.1553 场景**：OFDM scenario 4，上行强湍 σp²(Rytov)=0.25

**张力分解**：
- **假设 D1（场景差异）**：sat.1553 +1dB 是 OFDM scenario 4，B2-Q2 是单载波时域。OFDM 的 fade 行为（频选）跟单载波（时选）根本不同
  - **物理判据**：OFDM频选 fade 只影响部分子载波，pilot 在未 fade 子载波上仍可用；单载波时选 fade 影响整块符号，pilot 跟数据同步 fade
  - **这是 sat.1553 +1dB 不能搬到单载波时域的物理根因**
- **假设 D2（湍流强度差异）**：step4a weak（α4/β3）vs sat.1553 scenario 4（σp²=0.25 强湍）。strong 湍流下 fade 更深更频，pilot-aided 的优势（如果有）可能更明显
  - **验证方式**：sandbox 在 strong（α1.5/β0.8）下重测 DA vs NDA，看 strong 是否反转 step4a weak 的结论
  - **但注意**：D005 已证 strong HD-FEC 不可达（物理上限），所以 strong 下比的是工作区 BER 不是 HD-FEC gain

**维度 D 判定**：张力**可分解**。场景差异（D1）是 sat.1553 +1dB 不能搬的物理根因。湍流强度（D2）是可探索维度但 strong 受物理上限制约。

## 3. Fair Comparison 框架设计（sandbox 阶段 1 要测什么）

> 目标：设计一组对照实验，让"B2-Q2 命题 vs step4a 实测反证"的张力变成可证伪假设。

### 3.1 三方对照矩阵（守 V2 三方对照 + V3 祖师爷警报）

| 方案 | blind 侧 | pilot 侧 | 机制 |
|---|---|---|---|
| **A. 纯 blind freeze（[79] Matsuda 祖师爷）** | fft_foe + 功率阈值 freeze | 无 | fade 时冻结 FOE，恢复时 blind 重收敛 |
| **B. 纯 pilot-aided（step4a DA ML）** | 无 | da_ml_recovery 全程 | 全程 pilot-aided，step4a 已测在 fade 崩溃 |
| **C. B2-Q2 双模切换（本候选）** | fft_foe/nda_ml（非 fade） | da_ml/psa_foe（fade 时切） | fade 检测门控 + 模式切换 |

**祖师爷警报（V3+C8）**：方案 A 是 [79] Matsuda 2020 SPIE（sat.1553 L558/L582 引用），是 B2-Q2 的直接 baseline。**B2-Q2 必须赢方案 A**（纯 blind freeze）才能成立，不能只赢方案 B（step4a 已证 B 在 fade 崩溃）。

### 3.2 测度分离（稳态 BER vs 动态恢复）

**step4a 测的是稳态 BER**（无 freeze/恢复动态）→ step4a 反证只适用于稳态对比

**B2-Q2 真正的增量测度**（维度 B 发现）：
1. **fade 恢复时间**：fade 结束后 BER 收敛回稳态所需的符号数
2. **fade 期间累积 BER**：fade 期间 + 恢复期的总错误 bits
3. **稳态 BER**（跟 step4a 同测度，用于确认非 fade 期不退化）

**fair comparison 原则**：
- 稳态 BER 维度：B2-Q2 不应比纯 blind freeze 差（非 fade 期用 blind）
- 动态恢复维度：B2-Q2 应比纯 blind freeze 好（fade 期 pilot 帮助重收敛）—— **这是 B2-Q2 增量的核心测度**

### 3.3 公平对照条件（继承 step4a 框架 + B2 扩展）

| 条件 | step4a 框架 | B2-Q2 扩展 |
|---|---|---|
| pilot overhead | DA 含 1.249dB（spacing=4）| B2-Q2 pilot 侧同 1.249dB（只在 fade 期用，overhead 摊薄到全帧更少）|
| BER 计算位置 | DA 只在 data 位置算 | B2-Q2 全帧（blind 期全符号 + pilot 期 data 位置）|
| 信道 | GG 块衰落 weak/moderate/strong | 同（从 common/_channel.py 导入，TL-13）|
| 调制 | 16-APSK M₀=8 | 同 |
| 符号率/线宽 | 2.5GBaud / 10kHz | 同（D-007 统一）|

**B2-Q2 特有公平条件**：
- **pilot 只在 fade 期发**：B2-Q2 的 pilot overhead 不是全帧 25%，而是 fade 占空比 × 25%。如果 fade 占空比 10%，实际 overhead = 2.5%（0.11dB）→ B2-Q2 比 step4a DA ML 能量代价低得多
- **但需定义 fade 占空比**：功率阈值 γ_th 以下算 fade，fade 占空比 = P(γ < γ_th)

### 3.4 判定门控（红线警报）

**sandbox 后判定**（阶段 1 完成后）：

| 结果 | 判定 | 动作 |
|---|---|---|
| B2-Q2 双模切换 > 纯 blind freeze（动态恢复维度）| ✅ 命题可验证 | 进阶段 2 TL-20 理论预期 + 阶段 3 MVE |
| B2-Q2 ≈ 纯 blind freeze（动态恢复无差）| ⚠️ 增量微弱 | 检查 fade 检测门控是否有效，重设阈值 |
| B2-Q2 < 纯 blind freeze（pilot 干扰盲跟踪）| 🔴 核心命题崩塌 | **红线警报，转 Kill**（合法选项）|

**进 Kill 的物理判据**：
- 维度 C2（pilot-aided 路线在单载波时域根本弱）成立 → Kill
- 维度 B1（动态恢复机制差异）不成立（B2-Q2 跟纯 blind 恢复时间一样）→ Kill
- 所有 pilot-aided 变体（da_ml/psa_foe/power-boosted）在 fade 都输 NDA-ML → Kill

## 4. 阶段 0.1 结论

### 4.1 张力是否可分解

**可分解**（4 维度全部有明确物理判据）：
- 维度 A（pilot 配置）：spacing 不是问题（A1 不成立），pilot 功率/类型（A2）可探索但偏离原命题
- 维度 B（触发条件）：**最大差异点**——step4a 静态 BER vs B2-Q2 动态恢复是不同测度
- 维度 C（pilot-aided 类型）：C1 可验证，C2（路线根本弱）是红线风险
- 维度 D（信道场景）：场景差异是 sat.1553 +1dB 不能搬的物理根因

### 4.2 B2-Q2 命题是否站得住

**有条件站得住**（不是"稳够格"）：
- B2-Q2 真正的增量可能在**动态恢复时间**（fade 恢复期 pilot 帮助重收敛），不是稳态 BER
- 必须通过 sandbox 三方对照（阶段 1）验证"双模切换 > 纯 blind freeze"在动态恢复维度成立
- 如果 sandbox 发现 B2-Q2 在动态恢复也打不过纯 blind freeze → 核心命题崩塌转 Kill

### 4.3 不撞 step4a 反证的关键论据

**step4a 测的不是 B2-Q2 的命题**：
- step4a 对比"全程 DA ML vs 全程 NDA ML"（稳态 BER）
- B2-Q2 对比"双模切换 vs 纯 blind freeze"（动态恢复 + 稳态 BER）
- step4a DA ML 在 fade 崩溃 ≠ B2-Q2 pilot fallback 在 fade 崩溃（机制不同：全程 vs fallback）
- **但**：如果 B2-Q2 的 pilot 侧用 da_ml_recovery，且 fade 期间 da_ml 仍崩溃，则 B2-Q2 的 pilot fallback 也崩溃 → 这是维度 C2 的红线风险

### 4.4 阶段 0.1 完成，进阶段 0.2

**张力已分解为可验证假设**，不直接 Kill。进阶段 0.2 dB 溯源核查（sat.1553 +1dB 口径限定）。

**留给阶段 1 sandbox 的核心问题**：
1. B2-Q2 双模切换在 fade 恢复时间上是否真的优于纯 blind freeze？
2. pilot-aided（da_ml/psa_foe）在 fade 期间是否能继续跟踪（不崩溃）？
3. fade 检测门控（功率阈值）的敏感性如何？

**留给阶段 0.4 公平对照框架的核心问题**：
1. B2-Q2 的增量测度到底定哪个（动态恢复时间 vs 稳态 BER vs 工作区 BER）？
2. fair gain 阈值定多少（跟 NDA-ML HD-FEC 3.8e-3 对齐还是别的）？
3. pilot overhead 摊薄（fade 占空比 × 25%）怎么制度化？

## 附：核查机制中性双向记录（不变量 10）

| 子 agent 声称 | 主线独立核查 | 结论 |
|---|---|---|
| PILOT_OVERHEAD_DB = 1.249 dB | python `10*log10(4/3)` = 1.2494 | ✅ PASS |
| SIGMA2_P = 2.51e-5 | python `2*pi*10e3*4e-10` = 2.5133e-5 | ✅ PASS |
| 每 fade 块 25 pilot | python `100/4` = 25 + grep L122/L476 | ✅ PASS |
| da_ml 3 元组 vs nda_ml 4 元组 | grep `_recovery.py:168, 237` | ✅ PASS |
| psa_foe_recovery step4a 未调用 | grep `_time_domain_crlb.py` 无 psa_foe | ✅ PASS |
| BER 0.38/0.29 出处单一（仅 D004 L157）| grep 全 decisions.md | ✅ PASS（4 文件内唯一出处）|

**未交叉验证项**：BER 0.38/0.29 的 `_mve_results.json` 原始行（子 agent 未读该 JSON，本阶段也不需要——这是 sandbox 阶段 1 的事）
