# Handoff: 对话 2 — 单载波时域 NDA-ML 改进 MVE-SPEC 设计 + 时域 CRLB 推导

> 来源: S002（基建扩充 + B11 路径重定位）| 交接目标: 新对话设计单载波时域 NDA-ML 改进的 MVE-SPEC + 推导时域 CRLB
> 文件名: H002-conversation2-single-carrier-nda-ml.md
> 日期: 2026-07-06

## 到哪了（状态）

专题 `.sessions/2026-07-06-step4a-mve-execution/` 续接 S002（执行 H001 完成基建扩充 + 路径重定位）。**关键转折**：H001 步骤 3（B11 oracle 上界）被用户叫停——主线误把已发表 B11 baseline 当我们增量方法做 FR-21，偏离"复现 baseline → 做增量"范式（M6）。三轮诊断 + 修 bug + OFDM 评估 + 星地调研后，**用户拍板方案 C**（D002）：

**B11 重定位 = 理论参考（非直接对标 baseline）。我们的增量 = 单载波时域下的 NDA-ML 改进。**

证据链：
1. **星地 FSO 主流单载波**（DVB-S2/S2X 标准 + DLR sat.1553 综述 + CCSDS O3K 标准 + 顶刊近期论文无一例 OFDM 作主流，见 `_star_ground_link_survey.md`）
2. **B11 是 OFDM 频域 ML 与单载波时域架构性不等价**（频域 R(k)^M₀ vs 时域 r(n)^M₀；CPE 单常相位 vs 逐样本 Wiener；STO 模型完全不同；DFT 处理增益，见 `_OFDM_infra_assessment.md`）
3. **B11 团队定位非星地主流**（fiber+FSO 通用声明，仿真未建模 FSO 信道，被引仅 1 次）

**基建扩充完成**（守 TL-13 共用同一信道）：
- `_modulation.py`: 加 8PSK + (8,8)-16APSK（Gray + 平均功率归一化 + resolve）
- `_recovery.py`: 加 DA ML / NDA-ML（已修 2 bug D003）/ Gardner TED / PSA FOE
- `_channel.py`: 加 generate_shared_realization_apsk
- `params.py`: 加 B11Params / B7Params / B3Params（全标 source TL-26）

**nda_ml_recovery 已修 2 bug**（D003）：加 `assume_df_zero` 参数（True 跳 FFT-df 估常相位 CPE，B11 场景用）+ `resolve_m16apsk_blockwise`（逐块解 M₀-fold 模糊）。修复后 AWGN 18dB BER 从灾难性 → 5.25e-3 接近 DA ML 4.07e-3。

**关键诊断结论（单载波下）**：DA ML 在 pilot spacing=4（密集真符号 pilot，64 pilot/块）下近最优（vs oracle +0.27dB）。**单载波下 DA ML 不是"未优化 baseline"而是"pilot 充分时的近最优估计器"**——后续增量方法要超越的是这个近最优 DA ML，不是 B11 论文里 decision-feedback 的 DA ML。

## 下一步干什么（对话 2 三步，守 3 步上限）

### 步骤 1：报到 + 框架文件重读

报到（session-governance Trigger 1）+ 读：
- `.sessions/2026-07-06-step4a-mve-execution/topic-index.md`（不变量 13 条 + 范围边界 + D001/D002/D003 决策）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md`（D001 baseline 复现优先 / D002 B11 重定位 / D003 bug 修复）
- `stages/gw-feasibility.md` §D 维度 D（MVE 11 步 + FR-21 oracle 上界前置 + FR-11 架构摘要 + FR-14/15 baseline 对照）
- `thesis-lessons.md` TL-20（先建理论预期）/ TL-22（震撼结果查物理前提）/ TL-26（参数溯源）/ TL-27（oracle 上界前置，注意 D005 降级为参考）
- `projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md`（MVE-SPEC 9 节模板）
- 本轮产出（关键证据）：
  - `_star_ground_link_survey.md`（单载波主流证据）
  - `_OFDM_infra_assessment.md`（架构不等价分析）
  - `_awgn_repro_diagnostic.py` + `_awgn_repro_results.json`（AWGN 诊断数据）
  - `_crb_lower_bound.py` + `_ber_oracle_upperbound.py`（步骤 3 三轮诊断，**仅作方法学参考不作 Go/Kill 依据**）

### 步骤 2：单载波时域 NDA-ML 改进的增量定位（讨论锁边界，主线 + 用户）

**核心问题**：单载波时域下 NDA-ML 改进 vs 近最优 DA ML 的增量空间在哪？

**讨论维度**（参考 `_OFDM_infra_assessment.md` + B11 思想源头）：

1. **baseline 重新锚定**：
   - 单载波下 DA ML（pilot spacing=4 密集真符号 pilot）= 近最优估计器（vs oracle +0.27dB）
   - 但 **pilot overhead 代价**：spacing=4 = 25% 符号是 pilot，频谱效率损失 25%
   - **增量切口候选**：NDA-ML（无 pilot，盲去调制）能否在保留频谱效率下接近近最优 DA ML BER？

2. **B11 思想源头吸收到时域**：
   - B11 频域：R(k)^M₀ 升幂去调制 + 单正弦 ML → 闭式 τ̂/φ̂
   - 时域等价：r(n)^M₀ 升幂去调制 + 估 Wiener θ(n)（非常相位，方差放大 M₀² 倍）
   - **关键差异**：时域升幂后噪声方差放大 M₀² 倍（频域 DFT 处理增益抵消），需推导时域 CRLB 看理论极限
   - **STO 模型缺失**：B11 频域 STO = DFT 循环移位定理（线性相位 2πτk/N），时域整数 STO 是索引移位——单载波时域 STO 估计需另选机制（如 Gardner TED，已加在 _recovery.py）

3. **可能的增量形态**（待讨论）：
   - 形态 A：NDA-ML（无 pilot）+ 联合 Gardner TED 时序恢复，对标近最优 DA ML BER + 频谱效率提升
   - 形态 B：低 pilot 比例（如 spacing=16，6% pilot）+ NDA-ML 辅助，对标密集 pilot DA ML BER
   - 形态 C：NDA-ML 在 deep fade 下鲁棒性（DA ML pilot 受 fade 影响决策错误传播，NDA-ML 全帧积分对 fade 鲁棒）
   - 用户拍板哪个形态（或新形态）

### 步骤 3：派子 agent 推导单载波时域 NDA-ML CRLB + 数值验证（守 FR-21 + TL-20）

> 守 D005：FR-21 oracle 上界降级为参考不当 Kill 门，但连传统 baseline 都赢不了仍不行

**派子 agent**：
- 推导单载波时域下 NDA-ML（升 M₀=8 次幂去调制）vs DA ML（pilot 配置）的 CRLB
- 关键：时域升 M₀ 次幂噪声方差放大 M₀² 倍（频域有 DFT 处理增益抵消，时域没有）
- 数学：Fisher 信息 I ~ Σ_n |s(n)|^(2M₀) · M₀² / σ²，但 σ² 升幂后 = M₀² · σ² · |s√h|^(2(M₀-1)) → M₀² 在分子分母是否相消？需严格推导
- 参考经典文献：Mendez-Ruiz / Luise 升幂 ML CRB（子 agent 查）
- 输出 `explore/single-carrier-nda-ml/_time_domain_crlb.py` + `_crlb_results.json`
- 子 agent 返回：①时域 CRLB 公式 ②关键 (turb, SNR) 点的 CRLB 差 ③判定建议（<0.3dB Kill / 0.3-0.5dB Conditional / ≥0.5dB 进 MVE）④TL-20 预期偏离

**主线整合**：
- CRLB <0.3dB → 增量方法无空间，Kill NDA-ML 改进，转 B7
- CRLB ≥0.3dB → 写 `explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md`（仿 N1-MVE-SPEC.md 9 节模板）+ 跑 MVE

## 纪律（和下一步直接相关的约束）

1. **D001 baseline 复现优先**：本轮 baseline = 单载波近最优 DA ML（pilot spacing=4），不是 B11 OFDM 频域 ML。增量方法 = 单载波时域 NDA-ML 改进
2. **D002 B11 作理论参考**：引用 B11 思想（升 M₀ 次幂去调制 + ML），但不直接对标 B11 +2dB（架构性不等价）
3. **D003 nda_ml_recovery 已修 bug**：调用时 B11 场景（CFO 已补偿）传 `assume_df_zero=True` + 用 `resolve_m16apsk_blockwise`（block_size=256）
4. **不变量 6 profile 第 8 次防线**：增量方法（我们的 NDA-ML 改进）必须先算 CRLB 上界，<0.3dB 不跑 MVE（D005 降级 FR-21 为参考但保留底线）
5. **不变量 10 核查机制中性双向**：子 agent 返回数字主线独立 grep 核查（不信任报告）
6. **TL-20 先建理论预期**：MVE-SPEC.md §2 必填理论预期表
7. **TL-22 物理前提先查**：时域升 M₀ 次幂噪声放大是物理事实（非 bug），deep fade 下 |r|→0 升幂噪声灾难性放大是预期内
8. **TL-26 参数溯源**：所有参数从 B11Params/B7Params 取
9. **TL-13 共用同一信道**：用 generate_shared_realization_apsk（不自建）

## 接口变更（如有代码改动）

```yaml
# 本轮已改（S002 产出，下轮继承）：
# common/_modulation.py 新增（接口对齐 QPSK/16-QAM）
- apsk8_mod/apsk8_demod/ber_count_apsk8/resolve_apsk8
- m16apsk_mod/m16apsk_demod/ber_count_m16apsk/resolve_m16apsk
- resolve_m16apsk_blockwise(rx, tx_bits, block_size=256, mod='m16apsk')  # D003 新增
- resolve_apsk8_blockwise  # D003 新增

# common/_recovery.py 新增
- da_ml_recovery(rx, pilot_idx, pilot_sym, mod)
- nda_ml_recovery(rx, M0, mod, N_fft, assume_df_zero=False)  # D003 加参数
- gardner_ted_recovery(rx, sps, mod, gain, damping)
- psa_foe_recovery(rx, pilot_idx, pilot_sym)

# common/_channel.py 新增
- generate_shared_realization_apsk(Ns, gamma_bar, turb_name, f_dot, mod, seed)

# params.py 新增
- B11Params (CLW/HD_FEC_THRESHOLD/BAUD_RATE/DFT_SIZE/CP_LEN/M0_POWER/SNR_WORKING_POINT/PN_VARIANCE)
- B7Params (DOPPLER_RANGE/LEO_DOPPLER_RATE/OSNR_WORKING_POINT/GARDNER_SPS/GARDNER_GAIN/PSA_PILOT_SPACING)
- B3Params (NUM_BRANCHES_DIVERSITY 占位)
```

## 失败数据附录（本轮路线失败/纠正）

| 路线 | 失败机制 | 否决了什么 | 可复用部分 |
|------|---------|-----------|-----------|
| H001 步骤 3 B11 oracle 上界（CRB 层）| 物理量错配：B11 +2dB 是 BER@HD-FEC 不是相位 CRB；M₀² 升幂 SNR 惩罚推导误判 | 否决"用相位 CRB 做 B11 FR-21 门控" | CRLB 数学框架（频域）作时域推导参考 |
| H001 步骤 3 B11 oracle 上界（BER 层）| 信道过苛：GG+Doppler 致 BER floor 4e-2 @ 20dB 弱湍流，HD-FEC 阈值 3.8e-3 不可达，对比工作点根本没复现 B11 | 否决"用 BER 层做 B11 FR-21 门控（信道未校准时）" | BER 评估脚本结构可复用 |
| nda_ml_recovery 原版（2 bug）| FFT-df 锁噪声伪峰 + 全局 resolve 无法解块间模糊 | 否决"单载波时域直接搬 B11 频域 ML 算法" | 升 M₀ 次幂 + mean-angle 估常相位思想可复用 |

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等 | FR-14 baseline 公平对照 | 单载波下 DA ML 不是"未优化 baseline" | 增量方法对照 baseline 重新锚定为"近最优 DA ML"，不是 B11 DA ML |
| 时域升 M₀ 次幂噪声放大 M₀² 倍 | TL-22 物理前提 | 频域有 DFT 处理增益抵消，时域没有 | 时域 CRLB 推导后闭合 |
| B11 genie-aided 解卷绕（行 129-131）非可实现 | FR-14 公平对照 | MVE 用 resolve 替代（非 oracle） | 单载波 NDA-ML 改进若依赖解卷绕需独立方法 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 单载波时域 NDA-ML CRLB | NDA-ML vs 近最优 DA ML ≥ 0.3 dB（频谱效率提升下允许薄 BER gap） | FR-21 + D005 降级 | 未跑 |
| 单载波 NDA-ML MVE | NDA-ML BER ≤ 近最优 DA ML + 频谱效率提升 ≥ 20% | D005 + D002 | 未跑 |
| 时域升 M₀ 次幂物理前提 | deep fade（h→0）下升幂噪声放大是预期内（非 bug） | TL-22 | 待查 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（13 条）+ D001/D002/D003 决策
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 单载波 DA ML pilot sp=4 近最优（核查 `_awgn_repro_results.json`，DA @ HD-FEC 18.10dB vs oracle 17.83dB 差 0.27dB）
  - [ ] 星地 FSO 主流单载波（核查 `_star_ground_link_survey.md`，DVB-S2/DLR/CCSDS 三重证据）
  - [ ] nda_ml_recovery 2 bug 已修（核查 `common/_recovery.py` 有 `assume_df_zero` 参数 + `common/_modulation.py` 有 `resolve_m16apsk_blockwise`）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（problem-driven-redirection + cut-pattern + deep-read 3 个依赖均稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不改框架 / 不跳框架 / 不污染 common）

## 下一轮

**对话 2**（本 H002 目标）：
- 步骤 1：报到 + 框架重读（含本轮 5 份产出文档）
- 步骤 2：单载波时域 NDA-ML 改进增量定位（讨论锁边界，主线 + 用户拍板形态 A/B/C）
- 步骤 3：派子 agent 推导时域 CRLB + 数值验证

**对话 3**（视对话 2 结果）：
- 若 CRLB ≥0.3dB → 写 SC-NDA-ML-MVE-SPEC.md + 跑 MVE
- 若 CRLB <0.3dB → Kill NDA-ML 改进，转 B7 Gardner TED FOE 全流程

**对话 4**（最后）：B3 架构决策（多孔径阵列 vs 单链路工程可行性查证）+ 视情况跑 B3 MVE
