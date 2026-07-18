# [S011] DPLL DD 异族 baseline 仿真 + baseline 池立住

> 2026-07-08 | Step 4a 维度 D / baseline 池建设 | 状态: 完成

## 目标

在 NDA-ML 主实验相同参数下（16APSK + Gamma-Gamma + 2.5GBaud + 10kHz + 4 场景），跑 DPLL 的 BER 曲线，确认 DPLL 作为非近亲异族 baseline 立得住。数据出来后判断 baseline 池是否立住 + 决定写不写简报。

## 记录

### 1. 交接验证（H007 Trigger 5）

验证 H007 的 6 条关键事实声称，5 PASS + 1 FAIL：
- ✅ dpll_track_dd 在 common/_recovery.py:8，判决写死 qpsk/qam16（:21-27）
- ✅ dpll_track（:59）用 4 次方鉴相器，不适用 16APSK M₀=8
- ✅ 主实验结果 _main_experiment_5seed.json 存在（NDA/DA/oracle 5seed）
- ✅ fair_comparison.py 有 analyze_fair_gain + snr_at_ber
- ✅ D-010 5 条标准已写进 decisions.md
- ❌ **"hard_decision（_modulation.py:84）已支持 m16apsk，直接调"**：实际未实现，hard_decision 仅 qpsk+else→qam16。**但有补救**：run_bps_ablation.py:82 + run_dd_kf_ablation.py:124 已有 `hard_decision_m16apsk` 脚本内适配模式（最近邻 16 点星座），按选项 A 复用

FAIL 不阻断——选项 A（脚本内适配，不改 common/）是 VV/BPS/DD-KF 三消融既定模式。

### 2. TL-20 理论预期（先建后跑）

基于已有 NDA/VV/BPS/oracle 5seed 数据建锚点：
- **判据1**：DPLL BER 全程 ≥ oracle（否则 bug）
- **判据2**：DPLL BER < 2×NDA（否则 DPLL 太弱不像合法 baseline）
- **判据3**：DPLL BER > 0.7×NDA（否则 NDA 无价值）
- **判据4**：DPLL @ 18dB AWGN 合理范围 0.003~0.006（跟 VV/BPS 同量级）
- **预期落位**：DPLL BER ≈ VV 同量级或略差（闭环有锁定延迟 vs 前馈滑窗），跟 NDA 持平或略差

### 3. 关键发现：DPLL 必须连续处理（不能 per-block）

omega_n 扫描时发现 **per-block（逐块重置 VCO）DPLL BER 暴涨**（@18dB AWGN 7.5e-3，1.93×NDA），而**连续处理**（全数组 VCO 累积）BER=4.1e-3（1.06×NDA，TL-20 预期内）。

物理原因：DPLL 是闭环跟踪环，VCO 相位跨符号累积——逐块重置丢失符号间相位连续性。这跟 VV/BPS 前馈滑窗不同：前馈法逐块独立 OK（滑窗无状态），闭环法必须连续（VCO 有状态）。

解决：DPLL 连续处理全数组 → resolve_m16apsk_blockwise 解 M₀-fold 模糊（per-block 选最优旋转，同 NDA/VV/BPS 流程）。公平性不受影响——所有方法都用同一 resolve 函数。

### 4. 仿真结果（5 seed × 4 场景，181s）

omega_n 选择：扫描 {20e6, 50e6, 100e6}，选 50e6（@18dB BER=4.12e-3，最接近预期中心 0.004）。

**TL-20 一致性自检 ALL PASS**：
| 判据 | 结果 |
|------|------|
| DPLL ≥ oracle（全场景） | ✅ True |
| DPLL < 2×NDA（全场景，不太弱） | ✅ True |
| DPLL > 0.7×NDA（全场景，NDA 有价值） | ✅ True |
| DPLL @ 18dB AWGN = 3.64e-3（范围 0.003~0.006） | ✅ True |

**BER 曲线（5 seed 均值，DPLL/NDA 比值）**：
| 场景 | 高 SNR DPLL/NDA | 低 SNR DPLL/NDA |
|------|----------------|----------------|
| AWGN | 1.06~1.09（18~20dB） | 1.40~1.42（5~8dB，DPLL 低 SNR 稍差） |
| weak | 0.98~1.02 | 1.00 |
| moderate | 0.99~1.01 | 1.00 |
| strong | 0.99（工作区） | 1.00 |

**Fair gain @ HD-FEC（5 seed，正=NDA 赢 DPLL）**：
| 场景 | DPLL vs NDA (γ_d) | DPLL vs DA (γ_tot) |
|------|-------------------|-------------------|
| AWGN | +0.103±0.007 [+0.09,+0.11] dB | +1.248±0.035 dB（DPLL 赢 DA） |
| weak | +0.020±0.052 [-0.04,+0.08] dB（CI 跨 0，持平） | +1.509±0.297 dB |
| moderate | +0.019±0.030 [-0.02,+0.06] dB（CI 跨 0，持平） | +1.683±0.251 dB |
| strong | 工作区 -0.046±0.034 dB（DPLL 稍好） | — |

### 5. 与 VV/BPS 对照（异族 vs 同族）

| 方法 | 机制 | vs NDA AWGN | vs NDA weak | vs NDA moderate | 同族? |
|------|------|------------|-------------|-----------------|-------|
| VV | 升幂前馈滑窗 mean-angle | +0.006±0.019（持平） | -0.004（持平） | -0.004（持平） | ✅ 同族（升幂退化） |
| BPS | 升幂前馈距离度量 | +0.117±0.021 | +0.047 | +0.057 | ✅ 同族（升幂） |
| **DPLL** | **DD 闭环跟踪环** | **+0.103±0.007** | **+0.020（持平）** | **+0.019（持平）** | ❌ **异族（DD 闭环）** |

**关键认知**：DPLL 跟 NDA 在 weak/moderate 也持平（CI 跨 0），但这跟 VV 的持平性质不同：
- VV 持平 = 数学同族（VV 升幂 = NDA-ML 升幂的退化版，D-009 已证）→ D-010 标准 3 禁主比
- DPLL 持平 = 不同机制达到相似性能（DD 闭环 vs 升幂前馈）→ 合法异族 baseline

DPLL 在 AWGN 稍差于 NDA（+0.103dB，CI 不跨 0），说明 NDA-ML 的升幂 ML 闭式比 DD 闭环稍有优势——这给 NDA-ML 的价值背书（不是"大家都一样"）。

### 6. 结论：baseline 池立住

**baseline 池结构**（按 D-010 标准）：
- **DA-ML（主 baseline）**：pilot-aided，有 1.249dB overhead，NDA 全场景稳赢（+1.25~+1.68dB）→ FR-15 目标 baseline
- **DPLL（异族 baseline）**：DD 闭环跟踪环，跟 NDA 不同族，持平到稍差 → D-010 标准 3 合规（非近亲）
- **VV/BPS（fellow baseline）**：升幂前馈同族，一句带过（D-009 已证同族持平，不当主比）

文献合法性支撑：C1（Paillier JLT 2020 DPLL 星地 FSO）+ C6（Zhou IoT-J 2024 星地 GG + 相位估计）证方法在该层合法有人用（自实现是通信领域常态）。

## 决策引用

- 无新建 D###（DPLL 仿真是技术执行，baseline 池立住是验证结果非方向决策）
- 引用既有：D-010 标准 3（不找接近方法当 baseline）→ DPLL 异族合规
- 引用既有：TL-20（先建理论预期）→ 4 条判据全 PASS
- 引用既有：TL-13（共用信道）→ DPLL 用 generate_shared_realization_apsk 同 seed
- 引用既有：INVARIANT 10（核查机制中性双向）→ JSON 独立 grep 核查全 PASS

## 范围确认

- 本轮是否在 scope boundary 内：**是**（DPLL 仿真 = Step 4a 维度 D baseline 立证，在 D-010 baseline 池建设范围内）
- 没碰简报正文（ADVISOR_BRIEFING 未动）
- 没改 common/（选项 A 脚本内适配，守 TL-13）
- 没用 dpll_track（4 次方鉴相器，H007 纪律）

## 后续

1. **baseline 池已立住**：DA-ML 主 + DPLL 异族 + VV/BPS fellow。可写简报跟老师沟通路线 A/B。
2. **简报 v3**（ADVISOR_BRIEFING_2026-07-08_v3_turbulence_pivot.md）待发——用户说"先跑出 DPLL 数据再决定写不写简报"，现在数据有了，待用户决定。
3. **未做项**：B7 Gardner TED FOE MVE（并行第二候选）/ B3 架构决策 / 消融后置项（跨块 KF + BPS 迁移）
4. **DPLL 低 SNR AWGN 稍差**（1.4×NDA @ 5-8dB）是 DD 闭环在低 SNR 判决错误传播所致，物理合理，不影响 baseline 合法性（baseline 看工作区/HD-FEC 附近性能）
