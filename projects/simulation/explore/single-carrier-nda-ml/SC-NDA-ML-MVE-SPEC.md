# 单载波时域 NDA-ML 改进 MVE 规格（子 agent 执行契约）

> 来源: S003（H002 执行，时域 CRLB GO_MVE 判定后）| 框架: gw-feasibility.md §D
> 日期: 2026-07-06 | 执行方式: 子 agent 写脚本 + 运行 + 返回数字
> 增量形态: A（AWGN 频谱效率，去 pilot overhead）+ C（星地湍流鲁棒性，NDA 全帧积分 vs DA pilot 受 fade）

## 1. 核心假设

**在单载波时域 (8,8)-16APSK + Wiener PN + Gamma-Gamma 块衰落信道下，NDA-ML（升 M₀=8 次幂盲去调制 + 单正弦 ML 估 CPE）相对 DA ML（pilot spacing=4，25% pilot overhead）的公平对照（相同总功率）增量：**

- **形态 A（AWGN）**：@ BER=3.8e-3 (7% HD-FEC) gain ≥ 0.5 dB（pilot overhead 1.25dB 代价 − NDA 升幂噪声/resolve 残差 ~0.5dB）
- **形态 C（星地湍流）**：weak/moderate @ HD-FEC gain ≥ 0.5 dB（DA pilot 受 fade + NDA 全帧积分鲁棒）；strong 全工作区 NDA 赢（DA pilot 在 deep fade 崩溃）

**CRLB 层理论支撑**（来自 `_crlb_results.json` meta）：
- CRB_NDA(φ) = σ²/Σ_n |s(n)|²h(n)（全 N 符号贡献）
- CRB_DA(φ) = σ²/Σ_{n∈P} |s_p|²h(n)（仅 N_p=N/4 pilot 贡献）
- 比值 CRB_NDA/CRB_DA ≈ N_p/N = 1/4 → **CRLB 层 NDA-ML 理论下界优于 DA ML**（M₀² 严格相消，升幂噪声方差放大 = 相位参数增益）

**这是 Step 4a 维度 D MVE**（FR-22 GW 流程强制门控合规：当前在 GW Step 4a 维度 D，不跳到 Contract/Execute）。

## 2. TL-20 理论预期（MVE 跑之前必须写明，偏离即查）

基于 CRLB 推导 + 信道校准修复后 `_crlb_results.json` 数据：

| 场景 | 预期 NDA-ML vs DA ML gain (dB @ HD-FEC, 公平对照) | 预期排序 | 物理依据 |
|------|--------------------------------------------------|----------|---------|
| AWGN | **+0.3 to +0.8** | 4（最小，仅形态 A 频谱效率）| pilot overhead 1.25dB − NDA 升幂噪声/resolve 残差 ~0.5dB |
| weak (α4/β3) | **+0.5 to +1.5** | 3 | 形态 A + 轻微 fade 鲁棒性 |
| moderate (α2.5/β1.8) | **+1.0 to +2.5** | 2 | 形态 A+C 叠加，DA pilot 受 fade 退化 |
| strong (α1.5/β0.8) | 不可达 HD-FEC（物理上限），全工作区 NDA 赢 | 1（鲁棒性）| 形态 C 主导，DA pilot 在 deep fade 崩溃 |

**量化锚点（偏离即停查代码，TL-20）**：
- AWGN gain < 0 → **可疑**（公平对照下 NDA 应至少持平 + 频谱效率）→ 查公平对照坐标（DA 总能量 vs NDA 总能量）
- moderate gain < 0 → **可疑**（DA pilot 受 fade 应退化）→ 查 h 均衡（per-block h vs h_med）
- strong NDA-vs-oracle gap > 4dB → **可疑**（升幂实现错误）→ 查 resolve_m16apsk_blockwise + 升幂噪声
- weak gain > 3 → **可疑**（超 B11 +2dB）→ 查 pilot overhead 计算
- min NDA BER @ 20dB 总能量 > 0.05（weak）→ **可疑**（信道校准退化）→ 查 h_med 是否回到标量均衡

**信道校准关键修复**（来自 `_ber_floor_diagnostic.json`）：
- 主因 D2（h_med 标量均衡残差）→ 修复：per-block h（NDA 盲 ĥ=mean(|rx|²)−1/(2γ)，DA pilot ĥ=mean(|r(p)/s(p)|²)，oracle 真 h）
- 次因 D1（CFO 残余 assume_df_zero=True 误用）→ 修复：两阶段 fft_foe(M0=8) 粗估 CFO + nda_ml_recovery(assume_df_zero=True) 估残余 CPE
- SNR 扫扩至 26dB（TL-22 物理可达性：oracle 真 h@20dB weak=7.8e-3 > 3.8e-3，需 ~24dB）

## 3. 最小实例（FR-04 保真度检查）

**保留的核心结构属性**（简化不得删除）：
- ✅ (8,8)-16APSK + Gray 映射——复用 `common/_modulation.py:m16apsk_*`
- ✅ Gamma-Gamma 块衰落 + Doppler + Wiener PN——复用 `common/_channel.py:generate_shared_realization_apsk`（守 TL-13）
- ✅ 单载波时域 NDA-ML 升 M₀=8 次幂去调制——复用 `common/_recovery.py:nda_ml_recovery`（D003 修复后，assume_df_zero 参数）
- ✅ DA ML pilot spacing=4 decision-aided——复用 `common/_recovery.py:da_ml_recovery`
- ✅ per-block h 均衡（NDA 盲 / DA pilot / oracle 真）——MVE 新实现
- ✅ 两阶段 FOE + CPE（fft_foe 粗估 + nda_ml 残余）——MVE 新实现
- ✅ resolve_m16apsk_blockwise 解 M₀-fold 模糊——复用 `common/_modulation.py:resolve_m16apsk_blockwise`（D003 新增）

**合理简化**（不删除核心结构）：
- 省略 OFDM 帧结构（B11 是 OFDM 频域 ML，本 MVE 是单载波时域，架构性不等价已论证见 `_OFDM_infra_assessment.md`）
- 省略 STO 估计（单载波时域 STO 用 Gardner TED 是 B7 候选范围，本 MVE 聚焦 CPE）
- 块内 h 恒定（BLOCK=100，现有约定），per-block h 均衡

**FR-04 结论**：简化保留了 NDA-ML 增量所需的所有结构（GG 幅度分布 + Wiener PN + 单载波时域升幂 ML + pilot overhead 公平对照），结论可外推到含 STO 的完整单载波系统。

## 4. baseline 设计（FR-14 先验对照 + FR-15 目标 baseline）

| baseline | 角色 | 实现 | pilot overhead |
|----------|------|------|---------------|
| **DA ML（pilot sp=4）** | FR-14 先验 + FR-15 目标 baseline（NDA-ML 贡献声称要超越的对手）| pilot-aided ML，pilot spacing=4 等距，pilot 符号从已知 bits 生成 | 25%（1.25dB 总能量代价）|
| **NDA-ML（升 M₀=8 次幂）** | **本 MVE 候选方法** | 盲升 M₀=8 次幂去调制 + 单正弦 ML 估 CPE + per-block 盲 h 均衡 + resolve_m16apsk_blockwise | 0% |
| **genie-aided oracle** | CSI-aware 上界对照（非 baseline）| 真相位 + 真 h 补偿 | — |

**公平对照框架**（关键）：
- DA ML 总能量 SNR = 信息符号 SNR + 1.25dB pilot overhead
- NDA-ML 总能量 SNR = 信息符号 SNR（纯数据）
- BER 曲线按总能量 SNR 比较（相同总功率/相同信息率）

**NDA-ML vs B11 的增量定位**：B11 是 OFDM 频域 ML（D002 重定位为理论参考）；本 MVE 是单载波时域 NDA-ML 改进，吸收 B11"升 M₀ 次幂去调制"思想但落在时域（架构诚实，贴星地主流单载波，见 `_star_ground_link_survey.md`）。

## 5. pass/fail 标准（预定义）

主指标：**公平对照 BER gain @ HD-FEC threshold (BER=3.8e-3)**

| 判定 | 条件 | 含义 |
|------|------|------|
| **Go (§D PASS)** | AWGN gain ≥ 0.5 dB AND weak/moderate gain ≥ 0.5 dB | 假设成立，NDA-ML 改进可进 Step 5（Baseline 选定）|
| **Conditional Go** | 0.3 ≤ AWGN gain < 0.5 dB（薄增益），weak/moderate 仍 ≥ 0.5 dB | 形态 A 薄但形态 C 成立，记录风险进 Step 5 |
| **Kill/Fail** | AWGN gain < 0.3 dB OR weak/moderate gain < 0 | 核心假设不成立，NDA-ML 改进降级/排除，转 B7 |

**辅助判定（非一票否决）**：
- strong 湍流 HD-FEC 不可达是物理上限（oracle 也不可达），不判 fail。NDA-ML 全工作区赢 DA ML 即形态 C 成立
- NDA-ML vs oracle gap：gap < 3dB 为正常（gap 大说明 NDA-ML 离信息论极限远，记录但非致命）
- weak/moderate cross-over（低 SNR NDA 赢，高 SNR DA 反超）是物理合理的，不判 fail

## 6. 扫描设计

- 调制：(8,8)-16APSK
- 信道：AWGN + 星地湍流（weak/moderate/strong via generate_shared_realization_apsk）
- 总能量 SNR γ_tot（dB）：AWGN [5,8,10,12,14,16,18,20]，湍流 [5,10,15,20,22,24,26]（扩至 26dB 让 weak/moderate HD-FEC 可达）
- 每点 N_sym = 102400 符号（400 块 × 256，守 FR-21 N≥1e5），seed 固定（可复现）
- 方案：DA ML（pilot sp=4）/ NDA-ML（升 M₀=8 + 盲 h + resolve blockwise）/ oracle（真相位 + 真 h）
- 输出：BER vs γ_tot 曲线（每场景一张）+ 公平 gain 表

## 7. AIR 计算（BMD rate，可选辅助）

对 (8,8)-16APSK，4 bit Gray label (b0,b1,b2,b3)。BICM AIR（参考 N1-MVE-SPEC.md §7）：
```
R_BMD = Σ_{k=0}^{3} I(b_k; Y) = 4 - Σ_k H(b_k | Y)
```
**可选**：若 BER 指标在 strong 湍流不可达 HD-FEC，补 AIR 指标（AIR 不需 FEC 阈值，可在任一 SNR 比较）。本轮 MVE 优先 BER，AIR 作辅助。

## 8. 执行约束

- **时间预算 ≤ 900s**（子 agent 上限）
- 脚本放 `projects/simulation/explore/single-carrier-nda-ml/sc_nda_ml_mve.py`
- 从 `common/` 导入所有估计器和调制（守 D003：NDA-ML 星地用两阶段 fft_foe + nda_ml_recovery(assume_df_zero=True)，AWGN 用 nda_ml_recovery(assume_df_zero=True)）
- per-block h 均衡：NDA 盲 ĥ=mean(|rx|²)−1/(2γ)，DA pilot ĥ=mean(|r(p)/s(p)|²)，oracle 真 h
- 输出 JSON 含：每 (scene, γ_tot) 的 {nda_ber, da_ber, oracle_ber, fair_gain_db} + gain@HD-FEC 汇总
- 结果图（可选）存同目录 PNG
- 环境探测：优先 `~/.venvs/torch/bin/python`；探测失败用系统 python3（numpy/scipy）

## 9. 子 agent 返回（≤500 词摘要）

返回必须含：
1. 每场景（AWGN/weak/moderate/strong）的 NDA vs DA vs oracle BER 曲线关键点（@ HD-FEC 的 fair gain dB）
2. per-block h 均衡方案（NDA 盲 / DA pilot / oracle 真）的 BER 对比（验证盲 h 离真 h 多远）
3. 任何偏离 TL-20 预期的点（标注"DEVIATION"）
4. 一句话判定建议（Go/Conditional/Kill）+ 理由
5. 形态 A（AWGN）+ 形态 C（湍流）分别判定
6. 环境用哪个 python，运行耗时

不返回：完整曲线数据（存 JSON）、完整代码（存脚本文件）。主对话读 JSON 复核。
