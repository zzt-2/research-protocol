# Handoff: 对话 4 — 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency

> 来源: S004（工作对话对话 3）| 交接目标: 新工作对话执行阶段 2-3 MVE
> 文件名: H004-conversation4-mve.md
> 日期: 2026-07-08

## 到哪了（状态）

工作对话对话 3 完成阶段 1 sandbox 三方对照，**路径 C sandbox PASS**，可进 MVE。

**sandbox 核心结论**：前馈归一化后 B5 范围优势在湍流下仍成立——
- 范围扩展 14.4×（B5 ±4.5GHz / 传统 FFT FOE ±312.5MHz，≥10× 门控 PASS）
- 湍流下残频 σ max 16.20MHz << 140MHz 门控（裕度 123.8MHz，27 点全 PASS）
- 收敛性 19/19 全收敛（B5 星历+迭代覆盖 ±4.5GHz 全量程）
- baselines（fft_foe/leven）超 ±312.5MHz 折叠（预期，B5 范围优势体现）

**sandbox 产出**（7 文件落盘 explore/b5-leo-doppler-spectrum-foe/）：
1. `_short_time_spectrum_foe.py`（598 行，B5 估计器，含迭代收敛 + normalize_mode 三方案）
2. `_leven_mthpower_foe.py`（290 行，[60] Leven 祖师爷对照）
3. `_sandbox_three_way.py`（三方对照脚本，含 meta 字段）
4. `_sandbox_results.json`（fair gain 二维报告）
5. `_doppler_range_sweep.json`（Doppler ±4.5GHz 扫描）
6. `_turbulence_residual_sweep.json`（湍流下残频 σ 扫描）
7. `params.py` B5Params 类（20 字段全溯源 + HD_FEC，已落盘）

**关键实现发现**：
- α=6×10⁸ 暗 ratio 模式（Rp-n 饱和 0.5 × 6e8 = 300MHz ≈ B/8=312.5MHz）
- block ≡ ratio（按块归一化后 Rp-n 尺度无关），agc 须重校 α
- 测试信号须带限（RRC/低通），平坦白谱 Rp-n≈0 无信息
- B5 大频偏靠星历预测预补偿 + 迭代（纯 FFT 仅 ±1.18GHz，星历+迭代覆盖 ±4.5GHz）
- **星历预测完美假设**：sandbox 模拟 ephemeris_pred=f_true（残频≈0+噪声），实际星历有残差但裕度 123.8MHz 足够

## 下一步干什么（对话 4 = 阶段 2-3 MVE）

> **守 profile 第 9 次防线 + INVARIANT 6**：sandbox 已 PASS，进 MVE。守 FR-11 架构摘要 + FR-12 MVE→Formal 架构差异 + sim-preflight V1-V6 + FR-14/15 先验/目标基线对照。

### 阶段 2 TL-20 理论预期表

仿 N1-MVE-SPEC.md §2，写 `B5-MVE-SPEC.md` 含：
- TL-20 理论预期表（残频 σ 随 SNR/Doppler/湍流强度的预期曲线，sandbox 已有实测数据可校准）
- FR-11 架构摘要（动作空间/决策粒度/对比范式/奖励语义——B5 是前馈估计器非 DRL，适配为：估计域=频域功率比 / 决策粒度=块级 / 对比范式=三方对照 / 语义=粗 CFO 残频最小化）
- MVE 实验设计（基于 sandbox 产出扩展）

### 阶段 3 MVE + consistency

- MVE 脚本 `mve_b5_short_time_spectrum.py`（基于 _sandbox_three_way.py 扩展，加 consistency 路径）
- 守 V1（公式逐项核对，sandbox 已做 C6 重建）/ V2（三方对照，sandbox 已有）/ V3（祖师爷警报——B5 vs [60] Leven 非同族，B5 频域功率比 vs [60] Leven 时域差分）/ V4（参数变更重审）/ V5（子 agent 归因核查）/ V6（读原文数值）
- 守 FR-14 先验基线（B5 > Random）/ FR-15 目标基线（B5 > 传统 FFT FOE，范围维度）
- consistency bit-exact（MVE vs Formal，MVE 通过后转 experiments/）

### 转正

MVE 通过后：
- short_time_spectrum_foe 进 `common/_recovery.py`
- [60] Leven Mth-power 进 `common/_recovery.py`（祖师爷对照转正）
- B5Params 已在 params.py
- mve 脚本转 `experiments/`

## 纪律（和下一步直接相关的约束）

1. **INVARIANT 13 D006 边界**：MVE 实现必须守前馈归一化（normalize_mode='ratio'），禁环路 TF 联合建模。sandbox 已守，MVE 延续
2. **FR-11 架构摘要**：MVE-SPEC 必含架构摘要（B5 是前馈估计器，适配 DRL 框架的架构摘要为估计域/决策粒度/对比范式/语义）
3. **FR-12 MVE→Formal 架构差异**：MVE 与 Formal（experiments/）架构比对，差异影响对比机制则重验证
4. **FR-14 先验基线**：MVE 必含最强简单先验 baseline（B5 > Random，sandbox 已确认 B5 19/19 vs Random 会全失败）
5. **FR-15 目标基线**：MVE 必含 Contract 假设中指定的 baseline（B5 > 传统 FFT FOE，范围维度 14.4×）
6. **sim-preflight V1-V6**：MVE PASS 判 Go 前 V1-V6 必须全过（sandbox 已过 V1/V2/V5/V6，MVE 补 V3 祖师爷警报 + V4 参数变更重审）
7. **TL-13 共用信道**：MVE 从 `common/_channel.py` 导入，禁自建
8. **核查机制中性双向**（INVARIANT 10）：子 agent 跑 MVE + 主线独立 grep 核查，只信原始数字不信归因（D-009 教训 6）
9. **不污染 common**：MVE 通过才转正，explore 阶段探针不直接进 experiments

## 接口变更（代码改动）

sandbox 阶段（对话 3）已新增：
- `_short_time_spectrum_foe.py`（explore 探针，接口 `short_time_spectrum_foe(rx, n_fft, n_blocks, alpha, fs, normalize_mode, ephemeris_pred) -> dict` + `short_time_spectrum_foe_iterate(...) -> dict`）
- `_leven_mthpower_foe.py`（explore 探针，接口 `leven_mthpower_foe(rx, M, N_sum, fs, normalize_mode) -> dict`）
- `_sandbox_three_way.py`（sandbox 脚本）
- `params.py` B5Params 类（20 字段 + HD_FEC）

MVE 阶段（对话 4）将新增：
- `B5-MVE-SPEC.md`（MVE 契约，含 TL-20 理论预期表 + FR-11 架构摘要）
- `mve_b5_short_time_spectrum.py`（MVE 脚本，基于 _sandbox_three_way.py 扩展）

## 失败数据附录（如涉及路线失败）

无新增路线失败。sandbox 路径 C PASS，无红线警报。

**B5-Q1 潜在失败模式**（MVE 阶段需警惕）：
- **星历预测残差过大**（sandbox 假设完美星历 ephemeris_pred=f_true，实际星历有残差）→ MVE 需测星历残差对 B5 残频 σ 的影响（裕度 123.8MHz 应足够）
- **B5 vs [60] Leven 残频 dB 不利**（B5 粗 CFO 残频 σ 16MHz vs [60] Leven 精细 FE <10MHz）→ 不能作主判据，靠路径 C/A（范围扩展 + 绝对指标，0.4.1 警示）
- **BER 不作 B5 强项**（B5 是粗 CFO，BER 0.23-0.37 需后续 DSP）→ fair gain 维度 1 范围 + 维度 2 残频 σ 才是判据

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 星历预测完美假设 | sandbox 模拟 ephemeris_pred=f_true | sandbox PASS（裕度 123.8MHz）| MVE 测星历残差影响 |
| [60] Leven 范围差异 | 0.4.2 表 ±1.6GHz vs sandbox ±312.5MHz | sandbox 标注（1-sps 限制）| MVE 用 [60] Leven 最优条件重测 |
| B5 BER 偏高 | B5 是粗 CFO，BER 交后续 DSP | sandbox 标注 | MVE 加后续 DSP（VV/BPS）报完整 BER |
| short_time_spectrum_foe 待转正 | explore 验证通过才进 common | sandbox PASS | MVE consistency PASS 后转正 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| sandbox 三方对照 | B5 范围扩展 ≥10× + 湍流残频 σ <140MHz | V2+C7 (v1.3.0) + INVARIANT 11 | ✅ PASS（14.4× + max 16.2MHz）|
| MVE 范围 fair gain | ±4.5GHz 覆盖 + 残频 <5MHz @ BER 1e-3 或范围扩展 ≥10× | D005 + INVARIANT 11 | 未跑 |
| MVE consistency | MVE vs Formal bit-exact | sim-preflight | 未跑 |
| MVE V1-V6 | 公式核对 + 三方对照 + 祖师爷警报 + 参数重审 + 归因核查 + 读原文 | v1.3.0 | sandbox 已过 V1/V2/V5/V6，MVE 补 V3/V4 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B5 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 路径 C sandbox PASS（核查 `_sandbox_results.json` fair_gain.pathC_verdict + 主线独立核查 `_turbulence_residual_sweep.json` 残频 σ 全 <140MHz）
  - [ ] 范围扩展 14.4×（核查 `_doppler_range_sweep.json` B5 19/19 收敛 vs fft_foe 1/19）
  - [ ] B5Params 20 字段全溯源（核查 `params.py` B5Params 类 + B5 锚 content.md 行号）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 4**（本轮 H004 交接）：阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
- 写 B5-MVE-SPEC.md（含 TL-20 理论预期表 + FR-11 架构摘要）
- MVE 脚本（基于 _sandbox_three_way.py 扩展）
- 守 sim-preflight V1-V6 + FR-11/12/14/15
- consistency bit-exact（MVE vs Formal）
- MVE 通过后转正（short_time_spectrum_foe + leven_mthpower_foe 进 common）
