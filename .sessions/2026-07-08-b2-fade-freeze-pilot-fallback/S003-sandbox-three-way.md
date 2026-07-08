# [S003] 阶段 1 sandbox 三方对照（首次写代码）——C2 红线解除但核心增量三维度全失效

> 2026-07-08 | 阶段: 工作对话执行阶段 1 sandbox 三方对照（首次写代码）| 状态: 完成，sandbox 数据全产出，向主控报告 Go/Kill 建议

## 目标

承接主控对话 S002 + H002 派发，执行阶段 1 sandbox 三方对照（B2-Q2 首次写代码），回答两个必答问题（维度 C2 红线 + 动态恢复时间）。守 V2 三方对照 + V3 祖师爷警报 [79] + V4 参数变更触发算法重审 + V5 子 agent 归因独立核查 + V6 FR-26 读原文数值 + sim-preflight v1.3.0 + 前馈化 INVARIANT + TL-13 共用信道 + 3 步上限。

## 记录

### 报到 + 接收方验证（Trigger 1 + Trigger 5）

读完必读清单：topic-index（14 不变量）/ H002 / S002 / decisions（D001）/ voice / 7 份阶段 0 产出（_fair_comparison_framework / _architecture_decision / _tension_validation_design / _param_truth_source / _step4a_detail_extract / _db_sourcing_audit / _file_organization）/ 复用基建（_recovery.py 4 估计器 + _channel.py + _config.py + params.py）/ step4a 锚脚本（_time_domain_crlb.py）/ sim-preflight V1-V6 + interrupt 10-12 + SKILL §1.6 C6-C8 / profile。

**接收方验证 5 项全打钩**：
- ✅ 阶段 0 六项规约全完成（`ls` 核查 explore/b2-fade-freeze-pilot-fallback/ 7 份产出存在）
- ✅ 前馈化不撞 D006（_architecture_decision §3.1 + _recovery.py 4 估计器前馈性核查）
- ✅ 维度 C2 红线 + 动态恢复测度（_tension_validation_design §2 + _fair_comparison_framework §2.2）
- ✅ depends_on 4 依赖全稳定（registry 核查）
- ✅ 未违反"明确不含"

**额外发现（主线 sandbox 前核查，需登记）**：
1. **B2Params 草稿 import 会失败**（阶段 0.5 债务）：`_param_truth_source.md` §3 草稿写 `from params import GammaGammaParams`，但 params.py 无 `GammaGammaParams` 类（α/β 在 `TurbulenceParams`，经 `get_turb_dict()` 聚合到 `common._config.TURB`）。已修正 `_b2_params_draft.py` 用 `from common._config import TURB`。
2. **GG α/β 文献来源**（V6 FR-26 + 阶段 0.5 悬而未决 #3 答案）：params.py 标注 source="夜间/高仰角场景典型值"等 = **设计选择典型值**（audit_flag 全 WARNING），不是 sat.1553 scenario 定义。sandbox 复现 step4a 配置（继承相同 α/β），不改。
3. **D002 债务**：阶段 0.3 建议升 D002（前馈化 INVARIANT）待主控确认——decisions.md 当前只有 D001，无 D002。本轮守前馈化作为既定约束（H002 纪律 11），但 D002 未正式登记。

### 阶段 1 步骤 2：sandbox 第一步参数实测（FR-20/TL-26 不拍参数）

产出 `_b2_params_draft.py`（B2Params 落盘，修正 import）+ `_gamma_th_sweep.py` + `_gamma_th_sweep.json` + `_rho_fade_measure.json`。

**关键物理发现（FR-20/TL-26 实测价值，修正阶段 0.4/0.5 物理直觉）**：

1. **功率分布 P(mean(|rx_block|²)) 严重右偏**（GG 长尾）。阶段 0.5 §1.5 原设计 `[γ̄−3σ, γ̄−1σ]` σ 标准化扫参在 strong 失效（γ_th_lo=γ̄−3σ 出现负值，ρ_fade≈0）。

2. **ρ_fade 跟湍流强度反相关**（违反阶段 0.4 §3.2 预期）：
   - weak（α4/β3）σ=0.47：fade 浅而频繁，γ̄−1σ 处 ρ_fade≈0.12
   - strong（α1.5/β0.8）σ=0.99：fade 深而稀疏，γ̄−1σ 处 ρ_fade≈0.008~0.015
   - 阶段 0.4 §3.2 示例"strong ρ_fade=30%"物理直觉**错**（实测 strong 最低）

3. **γ_th 选择策略修正**（V4 参数变更触发算法重审）：σ 标准化范围失效 → 改用 **ρ_fade 作控制变量**（target=0.15 反推 γ_th，经验分位数层）。三方对照在"相同 fade 统计（ρ_fade=0.15）"下公平比较。
   - B2-Q2 pilot overhead 摊薄 = 0.15 × 1.249 = 0.187 dB（不是阶段 0.4 示例的 0.125~0.375 随湍流变化）

### 阶段 1 步骤 3：sandbox 三方对照 + 两个必答问题

产出 `_sandbox_three_way.py` + `_sandbox_results.json`。耗时 7.5s（21 点 × 400 块）。

**三方实现**（V2 三方 + V3 祖师爷 [79]）：
- 方案 A 纯 blind freeze [79]：非 fade fft_foe_m0_omega+nda_ml / fade hold 上一非 fade 估计（freeze）。freeze 机制核查 `_B2-deep-fade-freeze-increment.md:33` [79] 原文"FOE 跟踪环路在 received power 下降时关闭 tracking（hold 上一估计值或冻结）"——实现一致（前馈近似版）。
- 方案 B 纯 pilot-aided：da_ml_recovery 全程（复现 step4a fade 崩溃路径）
- 方案 C B2-Q2 双模切换：非 fade fft_foe_m0_omega+nda_ml / fade da_ml（主）/ psa_foe（备）

**公平性 bug 修复（主线自检发现 + 修复）**：
- 初始实现 fade 块给 A（blind freeze）误用 pilot h 均衡 → 修复：A 全程 blind h（fade 块也 blind h，freeze 只 freeze 相位不 freeze h）
- C2 测试 fade 块 blind BER 误用 pilot h → 修复：blind 估计器配 blind h，pilot 估计器配 pilot h
- C2 测试 n_bits_fade_blind 计算逻辑混乱 → 修复

**必答 1（维度 C2 红线）结论**：**红线不成立**。

fade 块内 BER 对照（fade 块 60/400=15%）：

| SNR 区间 | da_ml vs blind_nda | psa_foe vs blind_nda | C2 判定 |
|---|---|---|---|
| weak 5-15dB | da 赢（0.42/0.46, 0.27/0.40, 0.083/0.116）| psa 赢/持平 | 红线不成立 |
| moderate 5-15dB | da 显著赢（0.45/0.47, 0.34/0.43, 0.16/0.21）| psa 赢 | 红线不成立 |
| strong 5-10dB | da 赢（0.48/0.48, 0.42/0.46）| psa 持平 | 红线不成立 |
| strong 15dB+ | da 赢 blind（0.31/0.36, 0.15/0.17）| psa 输 blind | da 赢 |
| weak/moderate 20dB+ | 持平/微输 | 输 | 高 SNR 持平 |

→ da_ml 在绝大多数 fade 场景**赢** blind NDA-ML。"所有 pilot-aided 都输 blind"不成立。**B2-Q2 核心命题逻辑可以继续**（红线解除）。

**必答 2（动态恢复时间 N_recover）结论**：**结构性失效**。

前馈架构（INVARIANT）下 A 和 C 非 fade 期用同一个估计器（blind），fade 期估计器选择**不影响**非 fade 期恢复。fade→非fade 转换后第 1 块 BER 已接近稳态（比值 0.80），无收敛过程。N_recover A≈C（完全相同）。**N_recover 在前馈架构下结构性失效**。

物理根因：[79] 闭环 freeze 的恢复是"环路滤波器从 hold 状态重新收敛"（有惯性）；前馈架构没有环路惯性，每块独立估计，fade 结束后第一个非 fade 块立即用当前块的 blind 估计，无"收敛"过程。**前馈化 INVARIANT 导致动态恢复测度失效**（架构-测度不匹配）。

**全局三方 BER + Go/Kill 判据核查**（主线独立核查 V5）：

| 判据 | 结果 | 判定 |
|---|---|---|
| Go1 动态恢复 C<A | 结构性失效（前馈 A≈C）| FAIL |
| Go2 范围扩展（C 可达 HD-FEC 而 A 不可达）| 无（A/C HD-FEC 可达性完全一致：weak 24/26dB, moderate 26dB, strong 全不可达）| FAIL |
| Go3 稳态 BER fair gain ≥0.5dB | weak @HD-FEC: gain=24.0−(24.0+0.187)=−0.187dB（C 微输）| FAIL |
| Kill1 维度 C2 红线 | 不成立（da 多数赢 blind）| 不 Kill |
| Kill2 动态恢复无差 | 结构性成立（前馈 A≈C）| Kill 信号 |
| Kill3 稳态 BER 退化 | strong 中 SNR C/A=1.05~1.07（C 微输）| 部分 Kill 信号 |

**fade 块内 A(freeze) vs C(dual da_ml) 直接对照**（B2-Q2 fade 期增量）：
- weak 低 SNR：C 略赢（C/A=0.946）
- weak 10dB+：持平
- moderate/strong 中高 SNR：**C 输 A**（C/A=1.10~1.43）—— freeze 比 da_ml 在 fade 块更好

**物理根因**：fade 块 h 极低（true_h=0.44 vs 非fade 1.07），pilot SNR 也极低，da_ml 估计噪声大；freeze hold 的上一非 fade 块估计是高 SNR 估计，对 fade 块（相位漂移在 100 符号信道块内不剧烈）反而更准。

## 决策引用

- D001（继承）：开 B2-Q2 专题 + 首验证张力策略
- **无新建决策**（sandbox 数据 + Go/Kill 建议向主控报告，由主控/用户定夺。executor 角色只产实测数据 + 建议，不记 Kill/Go 决策——那是主控对话 + 用户的事，profile"Go/Kill 是用户的"）
- **建议主控对话记录 D002**（前馈化 INVARIANT 升级，阶段 0.3 已建议）+ **可能的新决策 D003**（sandbox 后 Kill 或重新定位贡献，待主控+用户定夺）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1 sandbox 三方对照，写代码但只放 explore 私有 `_` 前缀，不污染 common，不进 MVE/Contract）
- **守 executor 角色边界**：只执行 sandbox + 产出实测数据 + Go/Kill 建议。不自己决定 Kill/Go（红线 9 + profile）
- **守 3 步上限**：本轮 3 步（报到+验证 / 参数实测 / 三方对照），S003+H003 是收尾不算步骤
- **守 sim-preflight v1.3.0**：V2 三方对照（A/B/C 全跑）+ V3 祖师爷警报（[79] freeze 机制核查实现一致）+ V4 参数变更触发算法重审（γ_th 选择策略从 σ 标准化改 ρ_fade 控制变量）+ V5 主线独立 grep results JSON 核查（C2/fair gain/N_recover 全主线重算）+ V6 读原文数值（[79] freeze 机制 L33 + GG α/β params.py source audit）
- **守 profile 第 9 次防线**：阶段 0 满足才进 sandbox（已满足），sandbox 每步先讲清"在干啥+为什么"

## 后续

### sandbox 综合建议：转 Kill 或重新定位贡献（向主控报告）

**B2-Q2 当前形态（前馈化双模切换 da_ml fallback）的核心增量三维度全失效**：
1. 动态恢复时间：前馈架构结构性失效（A≈C）
2. 范围扩展：无（A/C HD-FEC 可达性一致）
3. 稳态 BER fair gain：微弱甚至负（C 微输 A）

**但 C2 红线解除**（da_ml 在 fade 赢 blind）——命题逻辑不崩塌，只是当前架构（前馈 + da_ml fallback）找不到够格增量。

**向主控对话报告的三个选项**（由主控 + 用户定夺）：

1. **Kill B2-Q2**（合法选项，阶段 0.4 §6.3 + INVARIANT 11）：核心增量三维度全失效，转 Kill。阶段 0.1-0.6 规约投入即使 Kill 也有价值（为 NDA-ML/B7 提供交叉验证 + 沉淀 pilot-aided vs blind fade 对比方法论 + 发现"前馈架构下动态恢复失效"这个架构-测度不匹配）。
2. **放松前馈化 INVARIANT**（重新讨论，可能撞 D006 风险）：前馈化是动态恢复失效的根因。若放松到闭环（如 [79] 原始闭环 freeze），动态恢复测度可能恢复意义。但闭环有撞 D006 风险（需重新论证），且 [79] 闭环 freeze 本身就是 baseline（B2-Q2 闭环版 vs [79] 闭环版差异更小）。
3. **重新定位贡献维度**（不死磕动态恢复）：sandbox 发现 da_ml 在 fade 期赢 blind（C2 红线解除）但输 freeze。可探索别的增量（如 fade 期 power-boosted pilot / 自适应阈值 / 别的 pilot-aided 算法变体）。但这些都是阶段 0.1 维度 A2/C1 的偏离原命题方向，需重新设计。

**executor 建议**：倾向选项 1（Kill）。理由：三维度全失效 + 前馈化 INVARIANT 是架构约束级（推翻需重新讨论 D006）+ 阶段 0 规约投入已沉没有价值。但**最终由主控对话 + 用户定夺**。

### 主控对话跟进点

- 核查 sandbox 三方对照是否真跑三方（V2）+ 方案 A 是否严格实现 [79] freeze（V3）—— 主线判定：A/B/C 全跑 + freeze 机制核查 `_B2-deep-fade-freeze-increment.md:33` 一致
- 核查维度 C2 红线是否真答了 —— 主线判定：fade 块内 da_ml/psa_foe/blind_nda 三方 BER 对照，da 多数赢 blind
- 核查动态恢复时间测度是否真测了 —— 主线判定：测了但发现前馈架构结构性失效（A≈C，fade→非fade 第 1 块已近稳态）
- 核查 γ_th 是否先实测功率分布再扫参（FR-20/TL-26）—— 主线判定：实测发现功率分布右偏，σ 标准化失效，改用 ρ_fade 控制变量
- 核查 Go/Kill 建议是否基于实测数字而非归因（V5）—— 主线判定：全主线独立 grep results JSON 重算 fair gain/C2/N_recover
- **架构-测度不匹配发现**（前馈化 → 动态恢复失效）是否需升 D003 + 放松前馈化讨论 —— 待主控核查

### 产出物清单（本轮交付）

1. ✅ `explore/b2-fade-freeze-pilot-fallback/_b2_params_draft.py`（B2Params 落盘，修正 import）
2. ✅ `explore/b2-fade-freeze-pilot-fallback/_sandbox_three_way.py`（三方对照脚本）
3. ✅ `explore/b2-fade-freeze-pilot-fallback/_gamma_th_sweep.json`（γ_th 扫参结果）
4. ✅ `explore/b2-fade-freeze-pilot-fallback/_rho_fade_measure.json`（ρ_fade 实测，ρ_fade=0.15 反推 γ_th）
5. ✅ `explore/b2-fade-freeze-pilot-fallback/_sandbox_results.json`（三方对照结果，meta 字段强制）
6. ✅ S003（本文件）
7. H003（交主控对话，下一步写）
