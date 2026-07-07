# B7 Gardner TED 复用 FOE 三方对照 MVE 规格（子 agent 执行契约）

> 来源: S005（sandbox 前半完成）→ S006（对话 6 起草）| 框架: gw-feasibility.md §D
> 日期: 2026-07-08 | 执行方式: 子 agent 写脚本 + 运行 + 返回数字
> 增量形态: BER gain（@ 双工作点）+ Doppler 估计范围比（1.9×）+ 低 SNR 鲁棒性（OSNR 10dB）

## 1. 核心假设

**在 25 GBaud DP-QPSK 单偏振简化 + 确定性 Doppler 频偏 + AWGN（OSNR）信道下，B7 proposed FOE（前馈扫频 + Gardner TED 增益 S-curve 峰反演）相对 PSA FOE（Vieira 2023 谱不对称法，FR-15 目标 baseline）的二维 fair gain：**

- **维度 1（BER gain @ BER 2e-2 锚校验）**：≈ +0.6 dB（poster `content.md:21/65/69` 一致性校验，偏离 >0.2 dB 触发 TL-20）
- **维度 1'（BER gain @ HD-FEC 3.8e-3 主判据）**：≥ +0.3 dB（跨候选主判据，poster 未给，需 MVE 测）
- **维度 2（Doppler 估计范围比）**：≈ 1.9×（23/12，结构性优势，B7 全 baud 周期相关 vs PSA 半 baud 限制）

**机制支撑**（S005 闭合）：
- **G(f_D) = K_max·|cos(πf_D/B)|** 解析式成立（`_ted_gain_analytic_results.json`，K_max=0.13214186 vs 0.2a 锚点 0.132142 bit-exact，D002 残留风险闭合弱同族 B 不降级 C）
- **B7 vs Gardner 1986 任务正交**：B7 做 FOE（估 f_D），1986 做 STR（检 τ），共享 TED 公式但机制独立
- **CRB 不卡 B7**（`_crb_results.json`）：N=1024 OSNR=17 dB CRB std=59.42 kHz << 扫频间隔 1 GHz（小 16830 倍），精度瓶颈是量化网格非理论 CRB，FR-21 不触发 Kill

**这是 Step 4a 维度 D MVE**（FR-22 GW 流程强制门控合规：当前在 GW Step 4a 维度 D，不跳到 Contract/Execute）。

## 2. TL-20 理论预期（MVE 跑之前必须写明，偏离即查）

**完整预期表已落盘** `_fair_comparison_framework.md §5`（避免重复，本节只索引关键锚点）。

| 指标 | 预期 B7 vs PSA FOE | 锚论文一致性校验 | 偏离触发 |
|------|-------------------|-----------------|---------|
| BER gain @ BER 2e-2 | **+0.4 to +0.8 dB** | poster ≈0.6 dB（`content.md:21/65/69`）| 偏离 >0.2 dB 查 LPF2 + PSA baseline |
| BER gain @ HD-FEC 3.8e-3 | **+0.3 to +0.7 dB** | 待 MVE 测（poster 未给）| <0 → 查 fair 对照坐标 |
| Doppler 估计范围比 | **≈1.9×**（23/12）| poster 1.9×（`content.md:21/49/69`）| <1.5 或 >2.5 查 PSA 估准上限判定 |
| B7 vs Gardner 1986 TR BER gap | **>0.1 dB**（任务正交不应持平）| 0.2 + 解析推导双重确认 | **<0.1 dB → V3 祖师爷红线警报**（查 B7 是否被错实现成反馈）|

**V3 祖师爷红线警报判据（sim-preflight v1.3.0 C8）**：若 sandbox/MVE 跑出 B7 vs Gardner 1986 TR 持平（BER gap <0.1 dB）→ 立即停。两种可能：(a) 数学同族（但 S003/D002 已判弱同族 B + 任务正交，此可能性低）(b) B7 前馈扫频被错实现成反馈跟踪。**优先查 (b)**。

**TL-20 偏离处理优先级**：BER gain 偏离时先查 LPF2 实现（poster 明确 0.6 dB 来自 LPF2，`content.md:65`），再查 PSA FOE baseline 是否真是谱不对称法（S005 已验证 `_psa_foe_asymmetry.py` 是谱不对称法非 pilot-aided，所以重点查 LPF2）。

## 3. 最小实例（FR-04 保真度检查）

**保留的核心结构属性**（简化不得删除）：
- ✅ 25 GBaud 单偏振 QPSK + RRC 成型（roll-off 0.1）——B7 锚论文场景（`content.md:21/47`）
- ✅ 确定性 Doppler 频偏 rx(t)=tx(t)·exp(j2πf_D·t)——扫频 0-23 GHz（`content.md:49`）
- ✅ Gardner TED 公式 e(k)=Re{y_mid·(y_curr*−y_prev*)}——0.2a `_b7_map_reconstruction.py` + 用户 `PSKTimingErrDetector.m L11-12` 双源（D001）
- ✅ B7 proposed FOE 核心机制：S-curve 峰反演 f_D（前馈扫频，D003 架构定性）
- ✅ PSA FOE 谱不对称法 Δf̂=α·ln(P+/P−)/2（Vieira 2023 §VI，S005 `_psa_foe_asymmetry.py` 重写，C6 公式源 audit）
- ✅ Gardner 1986 TR 反馈定时环（NCO + PI 环路滤波器 + Cubic 内插）——用户 `Tx2Rx.m L176-214` 祖师爷方

**合理简化**（不删除核心结构）：
- 省略 DP（双偏振）：单偏振验证 FOE 增量，DP 仅 3 dB 功率代价不改变 FOE 机制（MVE 隔离 FOE 增量）
- 省略 LEO Doppler 时变（三角波 ±100 MHz@1 GHz/s）：MVE 用确定性恒定 f_D 扫频（poster Fig.3a 也是恒定扫频），时变鲁棒性留 Formal
- 省略完整 RX 链（MIMO EQ/CPR/FEC）：BER 用 FOE 残差间接评估（FOE 残差 → 等效 SNR 损失 → BER 外推），或简化判决（QPSK 硬判 BER，无 FEC）
- 省略激光器相位噪声（1.8 kHz Lorentzian）：MVE 聚焦 Doppler FOE，激光器 PN 跟 FOE 正交（D003 架构定性已论证），Formal 再加

**FR-04 结论**：简化保留了 B7 FOE 增量所需的所有结构（Gardner TED 周期相关 + 前馈扫频 + S-curve 峰反演 + PSA 谱不对称对照），结论可外推到完整 DP + 时变系统。若 B7 增量在此最小实例下不成立，完整系统下也不成立（简化对 B7 更有利：恒定 f_D 比时变更易估）。

## 4. 三方对照架构（sim-preflight v1.3.0 C7 + V2，核心）

> 完整架构表见 `_fair_comparison_framework.md §4`。本节给实现细节。

| 方 | 角色 | 核心实现 | 公式源（V1）|
|----|------|---------|------------|
| **B7 proposed FOE** | 候选方法 | 前馈扫频 0-23 GHz step 1 GHz：每个 f_D 候选算 G(f_D)=max_τ\|S-curve(τ;f_D)\|，峰位置反演 f_D_est；LPF2 噪声抑制（poster 0.6 dB 来源 `content.md:65`）| B7 `content.md:37` + 0.2a `_b7_map_reconstruction.py` |
| **Gardner 1986 TR** | 祖师爷方（V3 红线警报）| 反馈定时环：Gardner TED → PI 环路滤波器（C1=1/2^5, C2=C1²/2）→ NCO → Cubic 内插；**任务是 STR（检 τ）不是 FOE（估 f_D）**，作 V3 祖师爷警报对照（B7 vs 1986 BER gap 应 >0.1 dB）| 用户 `PSKTimingErrDetector.m L11-12` + `Tx2Rx.m L176-214` |
| **PSA FOE** | baseline（FR-15 目标对手）| 谱不对称法：FFT → P+/P− → Δf̂=α·ln(P+/P−)/2（α 校准 1 GHz 单点拟合）→ 前馈补偿；估准范围 ≤ 半 baud=12.5 GHz（`content.md:19`）| Vieira 2023 §VI（`_psa_foe_asymmetry.py` S005 重写，C6 audit）|

**三方对照的公平性**：
- 三方都用**相同** DP-QPSK 25 GBaud 信号 + 相同 seed + 相同确定性 f_D 扫频（TL-13 共用信号生成）
- 三方都在相同 OSNR 条件测（17 dB 主测点 + 10 dB 低 SNR 极限）
- 三方输出都进相同 BER 评估（FOE/TR 补偿后 QPSK 硬判 BER）

**V3 祖师爷警报注意（C8）**：Gardner 1986 TR 是定时环（STR），B7 是频偏估计（FOE），任务正交。**三方对照中 B7 vs 1986 的 BER gap 不是"创新性增量"，是"任务正交性验证"**——若持平说明实现 bug（B7 前馈被错实现成反馈），不是"创新不足"。S003/D002 已双重确认任务正交，持平可能性低。

**D006 PSA coarse-only 弱限制**：PSA FOE 谱不对称法在 25 GBaud/β=0.1 场景线性区仅 ~1 GHz（`_psa_foe_asymmetry_summary.md`，谱边缘物理结果非 bug）。**B7 vs PSA 的 BER gain 标为上界**（PSA coarse-only 弱虚高 gain），范围/鲁棒性优势独立报告（D006）。

## 5. pass/fail 标准（预定义，D005 务实路线 + FR-25 Go/Kill 分离）

> 守 D005 务实路线（INVARIANT 2 最高优先级）：Go 判据=赢传统未优化 baseline（PSA FOE）几 dB；FR-21 oracle 上界降级为参考不当 Kill 门（CRB 已验证不卡，S005）。
> 守 FR-25 Go/Kill 标准分离：Go 标准=赢 PSA FOE / Kill 标准=V3 红线警报或 MVE FAIL。

主指标：**B7 vs PSA FOE BER gain @ 双工作点 + Doppler 范围比**

| 判定 | 条件 | 含义 |
|------|------|------|
| **Go (§D PASS)** | BER 2e-2 gain ≈0.6 dB（±0.2）AND HD-FEC gain ≥0.3 dB AND 范围比 ≈1.9×（±20%）| 三维全成立，B7 可进 Step 5（Baseline 选定）|
| **Conditional Go** | BER 2e-2 gain 成立（≈0.6 dB）但 HD-FEC gain <0.3 dB，或范围比成立但 BER gain 偏弱 | 薄增益（TL-05），叙事转"范围+鲁棒性结构性优势"为主，BER gain 为辅，记录风险进 Step 5 |
| **Kill/Fail** | BER 2e-2 gain <0.2 dB（偏离预期 >0.4 dB 且查代码非 bug）OR 范围比 <1.5× OR V3 红线警报触发（B7 vs 1986 持平查实现后仍持平）| 核心假设不成立，B7 降级/排除 |

**辅助判定（非一票否决）**：
- OSNR 10 dB：B7 可解调 / PSA FOE 失败（二值判定，`content.md:21/69`），作鲁棒性维度报告
- B7 vs Gardner 1986 TR BER gap >0.1 dB（V3 任务正交验证，不是创新增量）

**Go/Kill 判据分离（FR-25）**：
- **Go 标准**：赢传统未优化 baseline（PSA FOE）——会议门槛放宽（D005），纯仿真+鲁棒性 dB/范围/绝对指标都算够格
- **Kill 标准**：V3 红线警报（B7 vs 1986 持平查实现后仍持平，说明 B7 没真增量）或 MVE FAIL（BER gain 三维全崩）
- **CRB（FR-21）不当 Kill 门**：S005 已验证 CRB std=59.42 kHz << 扫频间隔 1 GHz，精度瓶颈是量化网格非理论极限

**MVE 结果需用户做 Go/Conditional Go/Kill 判断**（profile 画像：不宜长上下文一口气塞完，对话 7 跑数后单独判断）。

## 6. 扫描设计

- 调制：QPSK 单偏振（B7 锚论文 DP-QPSK 简化）
- 符号率：25 GBaud（B7 锚论文场景，跟 NDA-ML 2.5 GBaud 不统一，D005 用户决策）
- 信道：确定性 Doppler（rx=tx·exp(j2πf_D·t)）+ AWGN（OSNR），无激光器 PN（MVE 聚焦 FOE，D003）
- Doppler 扫频 f_D：0, 1, 2, ..., 23 GHz（step 1 GHz，`content.md:49` 对齐）
- OSNR 条件：17 dB（主测点 `content.md:49`）+ 10 dB（低 SNR 极限 `content.md:21/69`）+ 无噪声（机制验证基线）
- 每点：N_sym = 4096 符号 × 3 seed（蒙特卡洛，seed 固定可复现）
- 方案：B7 proposed / Gardner 1986 TR / PSA FOE 三方
- 输出：
  - 每方每 (OSNR, f_D) 的 {ber, df_est_or_tau, foE_residual}
  - BER gain @ BER 2e-2 + HD-FEC 3.8e-3（双工作点）
  - Doppler 估计范围比（B7 估准上限 / PSA 估准上限）
  - B7 vs Gardner 1986 BER gap（V3 祖师爷警报）

**smoke test 配置**（本轮，验证脚本能跑通不跑正式 MVE）：
- N_sym = 512（正式 4096 的 1/8），3 seed → 1 seed
- OSNR 只测 17 dB（正式 17+10+无噪声三条件）
- f_D 只测 0/5/12/15/23 GHz 5 点（正式 0-23 step 1 GHz 24 点）
- 三方都跑，验证无 crash + 输出结构对

## 7. BER 评估（简化，MVE 阶段）

MVE 阶段 BER 评估链（简化版，Formal 再加完整 RX 链）：
1. FOE 补偿（B7 proposed / PSA FOE 各自估 f_D_est，前馈补偿 rx_comp=rx·exp(−j2πf_D_est·t)）
   - Gardner 1986 TR 不做 FOE，做 STR（内插到最佳采样点），作 V3 祖师爷警报对照（BER 应比 B7 差，因不补偿 f_D）
2. QPSK 硬判决 BER（最近邻判决，无 FEC）
3. 工作点：BER 2e-2（锚校验）+ HD-FEC 3.8e-3（主判据，若可达）

**BER 评估简化理由**：MVE 隔离 FOE 增量，不加完整 RX 链（MIMO EQ/CPR/FEC）。若 FOE 补偿后残差小→BER 低→gain 正；残差大→BER 爆→gain 负。机制清晰，Formal 再加完整链验证。

## 8. 执行约束

- **时间预算 ≤ 900s**（AGENTS.md 子 agent 上限）
- 脚本放 `projects/simulation/explore/b7-gardner-ted-foe/b7_gardner_ted_mve.py`
- **信号生成三方共用**（TL-13）：同一 QPSK 25 GBaud 信号 + 相同 seed + 相同确定性 f_D 扫频
- **不 import common/ 的旧 psa_foe_recovery**（pilot-aided 概念错，D004），用同目录 `_psa_foe_asymmetry.py` 的谱不对称法
- **Gardner 1986 TR 用 Python 重写用户 Matlab 代码**（`PSKTimingErrDetector.m` + `Tx2Rx.m L176-214`），不 import common（common 无反馈定时环实现）
- **B7Params 从 params.py import**（25 GBaud/1.8 kHz，D005 落地），不硬编码
- 输出 JSON 含：每 (OSNR, f_D, method) 的 {ber, df_est, foe_residual_GHz} + 三方 BER gain + 范围比 + V3 gap
- 结果图存同目录 PNG（BER vs f_D 三方曲线 + 估计值 vs 真值）
- 环境：本机无 `~/.venvs/torch/`，用系统 `python`（numpy 2.4.3/scipy 1.17.1/mpl 3.10.8，S005 已验证）

## 9. 子 agent 返回（≤500 词摘要）

返回必须含：
1. 三方 BER vs f_D 关键点（@ BER 2e-2 和 HD-FEC 的 gain dB，若可达）
2. Doppler 估计范围比（B7 估准上限 / PSA 估准上限）
3. B7 vs Gardner 1986 BER gap（V3 祖师爷警报判据）
4. 任何偏离 TL-20 预期的点（标注"DEVIATION"）
5. 一句话判定建议（Go/Conditional/Kill）+ 理由（但**最终 Go/Kill 由用户判断**，子 agent 只给建议）
6. 环境用哪个 python，运行耗时

不返回：完整曲线数据（存 JSON）、完整代码（存脚本文件）。主对话读 JSON 复核（V5 主线独立重算归因）。

## 10. 与 NDA-ML 的边界（不混用）

- B7 脚本 import B7Params（25 GBaud/1.8 kHz）→ 禁 import NDA-ML SystemParams（2.5 GBaud/10 kHz）
- B7 三方对照独立于 NDA-ML MVE（不同候选，不同场景参数，fair gain 维度对齐 HD-FEC 但场景参数不统一，D005 用户决策）
- B7 结果不进 NDA-ML 的 results 目录，反之亦然
