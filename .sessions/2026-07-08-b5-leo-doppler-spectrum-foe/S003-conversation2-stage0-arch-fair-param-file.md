# [S003] 对话 2 — 阶段 0.3-0.6 前置规约（架构定性 + 公平对照 + 参数真相源 + 文件组织）

> 2026-07-08 | 阶段: 工作对话执行阶段 0.3-0.6（不写代码）| 状态: 完成，阶段 0 六项规约全收尾，可进 sandbox，交对话 3

## 目标

承接工作对话对话 1 S002 + H002 派发，执行阶段 0.3（架构定性，最高优先）+ 0.4（公平对照框架）+ 0.5（参数真相源）+ 0.6（文件组织），不写代码。核心是阶段 0.3 验证前馈归一化后 B5 范围优势（路径 C 核心前提）是否仍成立。

## 记录

### 报到 + 接收方验证（步骤 1）

session-governance Trigger 1 报到 + 读必读清单 1-7：
- 本专题 5 文件（topic-index 14 不变量 / H002 / S002 / decisions.md D001）
- 对话 1 产出 2 文件（_qualification_path_validation.md / _db_range_sourcing_audit.md）
- B5 锚全文 content.md 252 行 + 详评笔记 `_B5-...-increment.md` L100-167 + 切法地图 `_cut-b4b5-verify.md` L59-69
- [60] Leven 全文 179 行 + sat.1553 CFO 节 L451-559
- 复用基建（fft_foe _recovery.py:37 / fft_foe_m0_omega sc_nda_ml_sim.py:137 / B7Params params.py:606 / _channel.py / _recovery.py）
- 框架文件 + 教训（gw-feasibility §D / thesis-lessons TL-13/20/26/27 / sim-preflight SKILL §1.6 C6-C8）
- 上游 decisions（D005 务实路线 / D006 红线 / D017/D018）+ registry（4 依赖全稳定）+ profile（第 9 次防线）

接收方验证 4 条全打钩 + 3 条关键事实核查全 PASS：
- B5 conclusion L163-168 不含 ±4.5GHz（主线 sed 验证 PASS）
- [60] Leven L123 7dB penalty 确认（主线 sed 验证 PASS，是 differential decoding 无 FE 场景）
- 路径 C 够格判定门控确认（`_qualification_path_validation.md` §0.1c PASS）
- registry 4 依赖全稳定（problem-driven-redirection active / cut-pattern closed / deep-read active / step4a dormant 不阻塞）
- 范围未违反"明确不含"

### 阶段 0.3 架构定性（步骤 2，最高优先，路径 C 核心前提验证）

**0.3a 架构定性**：核查 B5 锚 L71-87 + L93 确认 B5 本体就是前馈开环（分块 FFT → 正负功率谱面积比 Rp-n → 归一化频偏估计 → 星历预测调 LO → 3s 周期重估），**全程无环路传递函数 H(z)**。

**D006 边界决策**：
- 前馈归一化（AGC / 归一化功率比）→ 合法不撞 D006（信号预处理，不把湍流相位纳入环路 TF）
- 环路 TF 联合建模（湍流相位纳入 H(z)）→ 撞 D006 Kill（B1 换皮模式，D006 L324/L328）
- **决策：走前馈归一化**（避免 D006 纠缠）。归一化方案 3 选项（块内归一化 / AGC 前置 / 归一化功率比）本轮不定，sandbox 时选最优

**0.3b 范围优势前提三项验证**（路径 C 核心，逐项论证）：
1. **捕获范围 ±4.5GHz**：FFT 带宽 + 星历预测决定，归一化只改幅度尺度不改位置信息 → **成立**（确定）
2. **残频 σ<140MHz / <5MHz**：Gamma-Gamma 慢包络（~1ms 相干时间）远大于块长（16点=6.4ns，比值 1:156250），块内归一化精确消除幅度尺度 → **理论上成立**（带 sandbox 确认条件，低 SNR 块归一化放大噪声风险需实测）
3. **收敛性 3-4 次迭代**：归一化稳定 Rp-n，原文 L141 确认收敛性不受接收功率影响 → **成立**（应提升）

**判定门控结论**：**前馈归一化后范围优势仍成立，路径 C 前提 PASS，进阶段 0.4**。无红线警报，不转 Kill。诚实标注残频指标在湍流下的精确衰减需 sandbox 实测（V2 三方对照 + C1 参数扫描验证）。

### 阶段 0.4 公平对照框架（步骤 3）

**0.4.1 baseline 选定**：传统 FFT FOE（fft_foe common/_recovery.py:37）为主 baseline（任务环节对口——频域找谱峰粗 CFO，范围 ±312.5MHz vs B5 ±4.5GHz = 15× 直接对比，复用基建已实现）+ [60] Leven Mth-power 作祖师爷对照（C7 三方对照用，任务环节不同——精细 FE，不作主 baseline）。

**关键警示**：[60] Leven 7dB penalty 是 differential decoding 无 FE 时 500MHz 频偏的 OSNR penalty（L123），不是 B5 vs [60] Leven 直接对比基线（S002 §3 溯源确认）。

**0.4.2 fair gain 二维定义**（参考 B7 模式 + sat.1553 L353 口径）：维度 1 范围扩展（15× vs 传统 / 2.8× vs [60] Leven）+ Doppler rate 跟踪（56MHz/s）+ 维度 2 残频/BER 对比（σ<140MHz + BER 1e-3 −48dBm）。

**0.4.3 工作点选定**：双工作点报告——BER 1e-3（主，B5 锚 + sat.1553 + [60] Leven 三者一致）+ HD-FEC 3.8e-3（跨候选可比，NDA-ML/B7/B2 对齐）。

**0.4.4 LEO Doppler 差异化**：B5 频域功率比粗 CFO（算法层，15× 范围）/ B7 定时域 TED 精估（算法层，0.6dB OSNR）/ B4 双反馈环架构（架构层，MSE 4×）。机制正交无撞车（`_B5-...-increment.md:161` 确认），三种正交解法可作大论文跨章节统一叙事。

### 阶段 0.5 参数真相源（步骤 4）

B5Params 草稿 20 字段全溯源 PASS（参考 B7Params 字段结构 + sim-preflight param-source.md）：
- 场景参数 6 字段：R_SYM_B5=2.5e9 / T_S_B5 / F_CARRIER_B5（1550.32nm）/ LASER_LW_B5=20kHz / MODULATION_B5=pm-qpsk / ORBIT_ALT_B5=600km
- B5 核心算法参数 5 字段：DOPPLER_RANGE_B5=±4.5GHz（五处一致）/ DOPPLER_RATE_B5=56MHz/s / ALPHA_B5=6×10⁸ / FFT_BLOCKS_B5=1024 / FFT_POINTS_B5=16
- 残频/性能指标 6 字段：RESIDUAL_FREQ_COARSE_STD_B5<140MHz / MAX 250MHz / FINE<5MHz / PRECISE_RANGE ±312.5MHz / BER_TARGET 1e-3 / RX_SENSITIVITY −48dBm
- 硬件/采样参数 3 字段：ADC_RATE 5GSa/s / FPGA_CLOCK 312.5MHz / CYCLE_PERIOD 3s
- 待 sandbox 定：NORMALIZE_MODE（归一化方案）/ TURBULENCE_PARAMS（从 common 继承）/ BER_HD_FEC 3.8e-3

20 字段全标 source_type + source（content.md 行号）+ audit_flag=OK。

### 阶段 0.6 文件组织（步骤 5）

- explore 目录结构规约：`projects/simulation/explore/b5-leo-doppler-spectrum-foe/`，私有文件 `_` 前缀，正式文件无前缀
- 当前 6 文件（阶段 0 全完成）：_qualification_path_validation / _db_range_sourcing_audit / _architecture_decision / _fair_comparison_framework / _b5_params_draft / _file_organization
- short_time_spectrum_foe 接口定义：参考 fft_foe_m0_omega 作起点骨架（分块 FFT 复用），核心算法"正负功率谱面积比 Rp-n + 归一化频偏估计 Δfest（α=6×10⁸）"需新写。接口含 normalize_mode 参数化空间（前馈归一化方案）
- 下游引用同步清单（D-007 教训 2 防御）：参数变更触发同步检查
- common 不污染（红线 6）：explore 探针不直接进 common，MVE 通过才转正

### 产出物

1. `explore/b5-leo-doppler-spectrum-foe/_architecture_decision.md` — 阶段 0.3 架构定性（前馈归一化路径定死 + 范围优势前提三项验证 PASS）
2. `explore/b5-leo-doppler-spectrum-foe/_fair_comparison_framework.md` — 阶段 0.4 公平对照框架（baseline + fair gain + 工作点 + 差异化）
3. `explore/b5-leo-doppler-spectrum-foe/_b5_params_draft.md` — 阶段 0.5 B5Params 草稿（20 字段全溯源）
4. `explore/b5-leo-doppler-spectrum-foe/_file_organization.md` — 阶段 0.6 文件组织规约（目录结构 + 接口定义 + 同步清单）
5. S003 session note（本文件）
6. H003 handoff（交对话 3 执行 sandbox）

## 决策引用

- D001（引用，不新建）：开 B5-Q1 专题 + 首验证够格路径策略。本轮 0.3-0.6 是 D001 阶段 0 的执行收尾
- 无新建 D###（阶段 0.3-0.6 是前置规约定型，不是新方向决策。前馈归一化路径选择是 INVARIANT 13 边界判定的执行落地，路径 C 前提 PASS 是验证结果不是新决策。若 sandbox 阶段发现路径 C 前提崩塌再立 D### Kill）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.3-0.6 前置规约，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约全做完才进 sandbox，本轮 0.3-0.6 全完成，下一对话可进 sandbox
- **守 3 步上限**：本轮实际 6 步（报到+读必读 1 / 0.3 架构定性 2 / 0.4 公平对照 3 / 0.5 参数真相源 4 / 0.6 文件组织 5 / S003+H003 6）。超 3 步但 PROMPT-002 方案 A 授权"4 项一对话做完"（PROMPT-002 L88），且四项都是文档规约不需验证链，主线一气呵成比拆对话效率高
- **守核查机制中性双向**（INVARIANT 10）：B5 锚 L71-87 算法原理 + L93 3s 周期 + [60] Leven L9/L121/L123 + sat.1553 L548-559 主线独立读原文确认，不只信 H002 交接摘要
- **守 TL-13 + TL-26 + FR-26 + V6**：所有参数读原文数值不只引位置，20 字段全标行号
- **守工作对话角色边界**：只执行阶段 0.3-0.6 规约，不进 sandbox 不写 MVE 代码

## 后续

### 交对话 3 执行阶段 1 sandbox 三方对照（H003 交接）

1. **sandbox 三方对照**（sim-preflight V2/C7）：B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power
2. **short_time_spectrum_foe 实现**（参考 fft_foe_m0_omega 作起点骨架，接口定义在 _file_organization.md）
3. **[60] Leven Mth-power 实现**（祖师爷对照，common 没有，需新写）
4. **fair gain 二维报告**（范围扩展表 + 残频/BER 对比表）
5. **路径 C 验证**：湍流下 B5 范围优势仍成立（残频 σ 不超 140MHz / 收敛性不退化 / 范围扩展仍 ≥10×）

### 主控对话跟进点

- 阶段 0.3 的前馈归一化后范围优势是否真验证了——三项（捕获范围/残频/收敛）逐项论证，残频带 sandbox 确认条件（低 SNR 块归一化放大噪声风险）
- 阶段 0.4 的 baseline 选定是否论证了 [60] Leven vs 传统 FFT FOE 的任务环节差异——0.4.1 论证 [60] Leven 是精细 FE（L9 prior to block PE），传统 FFT FOE 跟 B5 同是粗 CFO
- 阶段 0.5 的 B5Params 是否全标 source_type + source + audit_flag + 原文行号——20 字段全标 PASS
- 阶段 0.6 的 short_time_spectrum_foe 接口是否参考了 fft_foe_m0_omega 作起点骨架——接口定义在 _file_organization.md，分块 FFT 复用 + Rp-n 核心新写
- B5 vs B7/B4 的 LEO Doppler 主题差异化是否明确——0.4.4 论证 B5 频域功率比 / B7 定时域 TED / B4 双环架构机制正交无撞车

### 已知风险（交对话 3）

- **路径 C 残频前提风险**：前馈归一化后残频 σ 理论上仍 <140MHz，但低 SNR 块归一化放大噪声可能致残频超限。sandbox 需扫 SNR 确认（C1 关键参数扫描）
- **[60] Leven 任务环节错位风险**：[60] Leven 是精细 FE 不是粗 CFO，三方对照的公平性需论证（三方法都做前馈归一化 + 共用信道 + 双工作点）
- **路径 B 补 dB 结果可能不利**：B5 粗 CFO 在湍流下残频 dB 可能不如 [60] Leven 精细 FE。若 sandbox 发现 B5 vs [60] Leven 无 dB 增量则靠路径 C/A（范围扩展 + 绝对指标）
