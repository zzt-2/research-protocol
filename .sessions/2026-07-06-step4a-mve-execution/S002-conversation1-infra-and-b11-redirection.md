# [S002] 基建扩充 + B11 路径重定位（执行 H001）

> 2026-07-06 | Step 4a 维度 D MVE 执行 | 状态：完成（基建扩充 + B11 路径重定位方案 C + bug 修复 + H002 交接）

## 目标

执行 H001 三步：报到+框架重读 + 基建扩充（M-APSK/估计器/参数族/shared_realization_apsk）+ B11 oracle CRB 推导。

## 记录

### 步骤 1：报到 + 框架重读 ✅

- 报到 session-governance Trigger 1 + Trigger 5（收 H001 handoff）
- 读 topic-index（13 条不变量 + 范围边界 + 组织方案）
- 读 gw-feasibility.md §D 维度 D（MVE 11 步 + FR-21/FR-11/FR-14/15）
- 读 N1-MVE-SPEC.md（9 节模板）
- 读 thesis-lessons TL-20/TL-22/TL-23/TL-26/TL-27（前 10 条）
- 读 common/ 7 模块（_channel/_modulation/_recovery/_kf/_equalizer/_experiment/_config）+ params.py
- Handoff 验证：B11 行 33 假设 / common 7 模块 / N1-MVE-SPEC 9 节 全 PASS

### 步骤 2：基建扩充 ✅（2 子 agent 并行 + 主线整合 + 核查）

**子 agent A（_modulation + _recovery）**：
- _modulation.py 加 8PSK（4 函数）+ (8,8)-16APSK（4 函数，γ=2.57 DVB-S2 标准半径比）
- _recovery.py 加 DA ML（Cao 2012 decision-aided）+ NDA-ML（Wang 2022 升 M₀ 次幂 + 单正弦 ML）+ Gardner TED（1986 经典）+ PSA FOE
- sanity check：(8,8)-16APSK 平均功率 1.0022 + BER 无噪声 0 + 现有函数零改动

**子 agent B（params.py）**：
- 加 B11Params（8 参数：CLW/HD_FEC_THRESHOLD/BAUD_RATE/DFT_SIZE/CP_LEN/M0_POWER/SNR_WORKING_POINT/PN_VARIANCE，全 literature 标 B11 行号）
- 加 B7Params（6 参数：DOPPLER_RANGE/LEO_DOPPLER_RATE/OSNR_WORKING_POINT/GARDNER_SPS/GARDNER_GAIN/PSA_PILOT_SPACING，4 WARNING 标星地迁移待验证）
- 加 B3Params（占位，架构未决）
- SimulationConfig 聚合 b11/b7/b3

**主线扩 _channel.py**：加 generate_shared_realization_apsk（mod='m16apsk'/'apsk8'/'qpsk'，与 generate_shared_realization 共用 GG+Doppler 信道实现，守 TL-13）

**主线核查**（守不变量 10）：grep 验证 8 新估计器/调制函数 + 13 符号导入 sanity check（平均功率 1.0133 + BER 无噪声 0 + 端到端跑通 + 现有 generate_shared_realization 兼容未破）

### 步骤 3：B11 oracle 上界 → 路径偏离被叫停（M6 + profile 第 8 次防线）

**主线错误**：把已发表 B11 baseline 当"我们增量方法"做 FR-21 oracle 上界评估。

**用户原话戳穿**：
> "啥情况？我们是在复现啥？一般不是复现顶刊当做 baseline，然后在此基础上继续我们自己的吗？你这是在干啥（我不太清楚）？以及，怎么 kill 这么快呢？不能是代码不对吗？"

**诊断过程**（5 个子 agent）：
1. CRB 层子 agent：NDA-ML 升 M₀ 次幂在 CRB 层输 DA ML（-4~-8dB）→ Kill 建议
2. BER 层子 agent：NDA-ML BER 全场景输 DA ML（-3.75/-2.72/-0.96dB）→ Kill 建议，但暴露 HD-FEC 不可达（信道过苛）
3. AWGN 诊断子 agent：发现 nda_ml_recovery 有 2 bug（FFT-df 锁噪声伪峰 + 全局 resolve 无法解块间模糊），修复后 NDA 仍输 DA 0.59dB（非 +2dB）
4. 修 bug 子 agent：加 assume_df_zero + resolve_m16apsk_blockwise，sanity 精确复现 Variant B（18dB 5.25e-3 / 20dB 2.07e-3）
5. OFDM 评估 + 星地调研子 agent：B11 是 OFDM 频域 ML 与单载波时域架构性不等价 + 星地 FSO 主流单载波（DVB-S2/DLR/CCSDS 三重证据）+ B11 团队定位非星地主流

**用户拍板方案 C**（D002）：B11 作理论参考，做单载波时域 NDA-ML 改进。

### 关键发现

1. **方法论纠偏（D001）**：FR-21 oracle 上界是评估"我们自己的增量方法"的上界，不是评估已发表 baseline 的。baseline 在论文场景下的 dB 是既成事实，不需要用 oracle 上界重新判。正确流程：复现 baseline → 做增量 → 评估增量。
2. **B11 重定位（D002）**：B11 = 理论参考（"升 M₀ 次幂 + ML"思想源头），不作直接对标 baseline。增量 = 单载波时域 NDA-ML 改进。
3. **bug 修复（D003）**：nda_ml_recovery 加 assume_df_zero + resolve_m16apsk_blockwise。
4. **单载波 DA ML 近最优**：pilot spacing=4 下 DA ML vs oracle 仅差 0.27dB（近最优，不是"未优化 baseline"）。后续增量方法对照 baseline 重新锚定。
5. **星地 FSO 主流单载波**（强证据）：DVB-S2/S2X + DLR sat.1553 + CCSDS O3K + 顶刊近期论文无一例 OFDM 作主流。

## 决策引用

- D001：baseline 复现优先于增量评估（新建，用户纠正触发）
- D002：B11 角色重定位 = 理论参考（新建，调研+诊断+评估综合支撑）
- D003：nda_ml_recovery 两 bug 修复（新建，AWGN 诊断 Variant B 支撑）

## 范围确认

- 本轮是否在 scope boundary 内：**部分偏离后纠正**。步骤 1-2 在范围（基建扩充）。步骤 3 偏离（误做 B11 FR-21），被用户叫停后纠正（路径重定位方案 C）。范围不变（仍对 B11/B7/B3 走 Step 4a 维度 D），但 B11 路径从"直接对标 baseline"改为"理论参考 + 单载波时域改进"。

## 后续

1. **对话 2**（H002）：单载波时域 NDA-ML 改进 MVE-SPEC 设计 + 时域 CRLB 推导
2. **B7 仍可并行**：单载波+FOE 基建已就绪（Gardner TED/PSA FOE）
3. **B3 架构决策**：待最后（多孔径阵列 vs 单链路）
4. **本轮产出 5 份文档保留**：_star_ground_link_survey / _OFDM_infra_assessment / _awgn_repro_diagnostic + _awgn_repro_results / _crb_lower_bound + _crb_results / _ber_oracle_upperbound + _ber_results（**仅作方法学参考不作 B11 Go/Kill 依据**）
