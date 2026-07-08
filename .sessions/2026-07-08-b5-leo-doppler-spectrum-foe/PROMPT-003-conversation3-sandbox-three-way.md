# PROMPT-003: B5-Q1 对话 3 — 阶段 1 sandbox 三方对照（B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power）

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 对话角色: 工作对话（主控对话派发的执行体，对话 2 的续接）
> 来源: 主控对话 S001 + 工作对话 S002 + S003 + H003 交接
> 日期: 2026-07-08

## 你是谁

你是 B5-Q1 第四候选的工作对话（executor）对话 3，承接对话 2（S003 + H003 交接）。主控对话负责方向决策/跨候选调度/核查你的产出，你负责执行阶段 1 sandbox 三方对照（写代码跑脚本，验证路径 C 在湍流下是否成立）。

**对话 2 已完成阶段 0.3-0.6 四项前置规约**（阶段 0 六项规约全收尾，可进 sandbox）：
- 0.3 架构定性：**前馈归一化路径定死不撞 D006**（B5 本体 L71-87+L93 确认前馈开环无环路 TF）+ **范围优势三项验证 PASS**（捕获范围±4.5GHz 确定成立 / 残频 σ<140MHz 理论成立带 sandbox 确认 / 收敛性 3-4 次成立应提升）→ 路径 C 前提 PASS 不转 Kill
- 0.4 公平对照：baseline = 传统 FFT FOE 主（fft_foe common/_recovery.py:37，粗 CFO 任务对口）+ [60] Leven Mth-power 祖师爷对照（C7 三方对照用）+ fair gain 二维报告 + 双工作点 BER 1e-3 + HD-FEC 3.8e-3 + B5/B7/B4 机制正交
- 0.5 B5Params 草稿：20 字段全溯源 PASS（R_SYM=2.5GBaud / LASER_LW=20kHz / DOPPLER_RANGE=±4.5GHz / ALPHA=6×10⁸ / FFT 1024组16点 / 残频 σ<140MHz / BER 1e-3 −48dBm 等）
- 0.6 文件组织：explore 目录结构 + **short_time_spectrum_foe 接口定义**（参考 fft_foe_m0_omega 起点骨架，分块 FFT 复用 + Rp-n 核心新写，含 normalize_mode 参数化空间）+ 下游引用同步清单

**纪律**：
- 主控对话交代的角色边界要守——你执行阶段 1 sandbox 三方对照，sandbox 是路径 C 的验证维度不是 Go 判据（不直接当 Go 跑 MVE）
- 每个阶段开始前先一句话讲清"在干啥+为什么"再动手（profile 第 9 次"急于推进"防线）
- 子 agent 跑脚本 + 主线独立 grep 核查结果，只信原始数字不信归因（D-009 教训 6）
- sandbox 前先写简版理论预期（TL-20：残频 σ 应 <140MHz，范围扩展应 ≥10×），偏离即查

## 你的任务（H003 交接，简版）

**执行阶段 1 sandbox 三方对照**（写代码跑脚本），核心是验证路径 C 在湍流下是否成立——前馈归一化后 B5 范围优势（捕获范围 ±4.5GHz + 残频 σ<140MHz + 收敛性）在湍流信道下是否仍成立：

- **实现 short_time_spectrum_foe**（B5 锚算法，接口定义在 `_file_organization.md`）：分块 FFT（16点/块）+ 均值滤波（1024组）+ 正负功率谱面积比 Rp-n（式3）+ 归一化频偏估计 Δfest=α×Rp-n（式2，α=6×10⁸）+ 前馈归一化（normalize_mode 三方案 block/agc/ratio 选最优）+ 星历预测调 LO（前馈开环）
- **实现 [60] Leven Mth-power**（祖师爷对照，common 没有）：rx × conj(rx_prev) → 4次方（QPSK M=4）→ 500样本求和 → 相位除4 → 累加相位补偿
- **三方对照脚本**（`_sandbox_three_way.py`）：B5 短时谱 / 传统 FFT FOE（fft_foe 已实现）/ [60] Leven Mth-power，三方法都做前馈归一化 + 共用信道（TL-13）+ 扫 Doppler ±4.5GHz + 双工作点
- **fair gain 二维报告**：范围扩展表（捕获范围 + Doppler rate 跟踪 + 残频）+ 残频/BER 对比表（三方法在同一湍流信道下的残频 σ + BER 曲线）

**判定门控**（路径 C 的 sandbox 验证维度）：
- B5 范围扩展 ≥10×（15× 满足）+ 湍流下残频 σ 不超 140MHz + 收敛性不退化 → **路径 C sandbox PASS，进 MVE**
- B5 范围优势湍流下消失（残频 σ 超 140MHz 或范围扩展 <10× 或收敛性崩）→ **红线警报（核心机制崩塌），B5-Q1 转 Kill**

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**（FR-22 框架强制门控）：

### 1. 本专题文件（最重要，必读全）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/H003-conversation3-sandbox-three-way.md` — 完整交接（含 sandbox 三方对照详细动作 + 纪律 + 验证阈值 + 已知债务 + 失败数据附录）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/S003-conversation2-stage0-arch-fair-param-file.md` — 对话 2 记录（0.3-0.6 执行详情）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/topic-index.md` — **14 不变量**（重点 11/12/13/14 B5 特殊风险）+ 悬而未决（0.1-0.6 全解决，剩 sandbox 验证）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md` — D001 决策详情

### 2. 对话 2 阶段 0.3-0.6 产出（本轮前置，必读全——sandbox 实现的规约来源）
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_architecture_decision.md` — **阶段 0.3 架构定性**（前馈归一化路径定死 + D006 边界 + 范围优势三项验证 + 归一化方案 A/B/C）—— **short_time_spectrum_foe 实现必须守前馈归一化，禁环路 TF**
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_fair_comparison_framework.md` — **阶段 0.4 公平对照**（baseline 选定 + fair gain 二维 + 工作点 + B5/B7/B4 差异化）—— **三方对照脚本设计依据**
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_b5_params_draft.md` — **阶段 0.5 B5Params 草稿**（20 字段全溯源 + Python 类草稿）—— **sandbox 时 B5Params 进 params.py，参数从这复制**
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_file_organization.md` — **阶段 0.6 文件组织**（**short_time_spectrum_foe 接口定义** + 三方对照接口 + 下游引用同步清单）—— **sandbox 实现的核心规约**

### 3. B5 锚论文全文（sandbox 实现核对对象——算法原理 L71-87）
- `papers/doi/10.1016_j.optcom.2024.130981/content.md` — B5 锚全文 252 行（**重点 L71-87 算法原理 / 式2-4 / L85 α=6×10⁸ / L87 1024组16点FFT / L93 3s周期 / L117 理论范围±B/2 / L141 收敛性不受接收功率影响**）
- `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` L100-167（全文增量核验段）+ L160（B5 核心=正负功率谱面积比非找谱峰）+ L162（D006 边界）

### 4. [60] Leven 原文 + sat.1553（祖师爷对照实现 + 公平对照口径）
- `papers/doi/10.1109_lpt.2007.891893/content.md` — [60] Leven 全文 179 行（**L55-65 Mth-power 算法：rx×conj(rx_prev)→4次方→500样本求和→相位除4→累加补偿**；L9 prior to block PE 精细 FE；L121 BER 1e-3；L123 7dB penalty 无 FE；L157 OSNR<9dB）
- `papers/doi/10.1002_sat.1553/content.md` L451-559（CFO 节 + 残频上限公式 27 Δfm=fs/8N + "粗补偿即可"）+ L353（SNR penalty vs 完美同步口径）

### 5. 复用基建（sandbox 实现的起点骨架 + baseline + 信道）
- `projects/simulation/simulator/sc_nda_ml_sim.py:137-166` — **fft_foe_m0_omega**（short_time_spectrum_foe 起点骨架，分块 FFT + Hanning窗 + zero-pad + 抛物线插值复用）
- `projects/simulation/common/_recovery.py:37` — **fft_foe**（主 baseline，4次幂 blind QPSK 找谱峰，三方对照用）
- `projects/simulation/common/_channel.py` — 信道实现（TL-13 共用，禁自建；用 `generate_shared_realization` / `generate_shared_realization_apsk` / `gg_block` / `doppler_phase`）
- `projects/simulation/params.py:606-628` — B7Params（B5Params 参数族模板参考，sandbox 时 B5Params 加到这）

### 6. 框架文件 + 教训（sandbox/MVE 阶段强制）
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步（sandbox 是 MVE 前置，MVE 阶段用）
- `thesis-lessons.md` **TL-13（共用信道）/ TL-20（先建理论预期，sandbox 前写简版）/ TL-26（参数溯源）/ TL-27（物理量级核算）**
- `.agents/skills/sim-preflight/SKILL.md` §1.5 C1-C5 + **§1.6 C6-C8（公式核对/三方对照/祖师爷警报）** + `rules/mve-validation.md` **V1-V6** + `rules/param-source.md`（参数单一字段读）+ `rules/interrupt.md` 第 10-12 条

### 7. 上游决策链 + 参照候选（B7/B2 sandbox 已跑完可参照）
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — **D005 务实路线 / D006 红线（联合建模进环路 TF Kill）/ D017/D018**
- `.sessions/2026-07-08-b7-gardner-ted-foe/` — B7 Gardner TED（已跑完 sandbox，`_psa_foe_asymmetry.py` + `_sandbox_three_way.py` 可参照脚本结构）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/` — B2（已跑完 sandbox，`_sandbox_three_way.py` + `_sandbox_results.json` 可参照结果格式）

## 接收方验证（读完文件后必须完成）

逐项打钩后才能动手（H003 §接收方验证）：

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B5 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] 前馈归一化后范围优势三项验证 PASS（核查 `_architecture_decision.md` §0.3b 三项验证表 + 主线 sed B5 锚 L71-87/L93/L117/L141 算法原理）
  - [ ] baseline = 传统 FFT FOE（核查 `_fair_comparison_framework.md` §0.4.1 + 主线 grep `common/_recovery.py:37` fft_foe 接口）
  - [ ] B5Params 20 字段全溯源（核查 `_b5_params_draft.md` §溯源审计汇总表 + 主线 grep B5 锚 content.md 行号）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 执行节奏（守 3 步上限）

**本轮 sandbox 三方对照，建议拆法**：

**方案 A（推荐，sandbox 一对话做完）**：若 short_time_spectrum_foe 实现顺利（fft_foe_m0_omega 起点骨架可复用），sandbox 三方对照一对话做完
- 步骤 1：报到 + 读必读清单 1-7 + 接收方验证 + 写简版理论预期（TL-20）
- 步骤 2：实现 short_time_spectrum_foe + [60] Leven Mth-power + B5Params 进 params.py（可派子 agent 并行实现两个估计器）
- 步骤 3：跑三方对照 sandbox + fair gain 二维报告 + 判定门控

**方案 B（实现有风险时拆对话）**：若 short_time_spectrum_foe 核心算法（Rp-n 正负功率谱面积比）实现遇阻（B5 锚式2-4 公式以 picture omitted，需从 L77-87 文字重建），实现单独一对话，sandbox 跑对照留对话 4
- 本轮只做实现 + 单元测试（B5 估计器 vs fft_foe_m0_omega 在无湍流 AWGN 下对比，验证 Rp-n 实现正确）
- sandbox 三方对照留对话 4

**判定**：实现完成后判断走方案 A 还是 B。若 Rp-n 实现顺利且上下文允许，继续 sandbox；若 Rp-n 实现遇阻或超 3 步，写 H004 交对话 4。

**注意 C6 公式核对**（sim-preflight v1.3.0）：B5 锚式2-4 以 picture omitted 形式存在（content.md L73-83），实现时必须从 L77-87 文字描述重建并标注"PDF→md 公式丢失，文字重建"。若重建有歧义，标红不硬磕，sandbox 前确认。

## 产出物（本轮交付）

1. `explore/b5-leo-doppler-spectrum-foe/_short_time_spectrum_foe.py` — B5 核心算法实现（分块 FFT + Rp-n + 前馈归一化 + 星历预测调 LO）
2. `explore/b5-leo-doppler-spectrum-foe/_leven_mthpower_foe.py` — [60] Leven Mth-power 祖师爷对照实现
3. `explore/b5-leo-doppler-spectrum-foe/_sandbox_three_way.py` — 三方对照脚本
4. `explore/b5-leo-doppler-spectrum-foe/_sandbox_results.json` — 三方对照结果（fair gain 二维报告）
5. `explore/b5-leo-doppler-spectrum-foe/_doppler_range_sweep.json` — Doppler ±4.5GHz 全量程扫描（验证捕获范围）
6. `explore/b5-leo-doppler-spectrum-foe/_turbulence_residual_sweep.json` — 湍流下残频 σ 扫描（验证 0.3b 验证2）
7. `projects/simulation/params.py` — B5Params 类加入（从 `_b5_params_draft.md` 复制）
8. S004 session note — 本轮记录
9. H004 handoff — 交下一对话执行 MVE（若 sandbox PASS）或报红线警报（若范围优势崩塌）

**explore/ 目录在 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/`**（不是根目录的 explore/）。

## 红线（违反必须停）

1. **禁直接当 Go 跑 MVE**（sandbox 是路径 C 验证维度不是 Go 判据，profile 第 9 次防线 + FR-25 Go/Kill 标准分离）
2. **禁走环路 TF 联合建模**（short_time_spectrum_foe 必须前馈归一化，撞 D006 Kill）
3. **禁自建信道**（TL-13，从 `common/_channel.py` 导入 `generate_shared_realization`）
4. **禁污染 common**（explore 探针不进 experiments，short_time_spectrum_foe 在 explore 验证通过才进 common）
5. **禁忽视路径 C 崩塌信号**（sandbox 发现湍流下范围优势消失 → 红线警报，不能"再凑凑看"）
6. **禁跳 TL-20 理论预期**（sandbox 前先写简版理论预期：残频 σ 应 <140MHz，范围扩展应 ≥10×，偏离即查）
7. **禁硬磕 PDF→md 公式丢失**（B5 锚式2-4 picture omitted，从 L77-87 文字重建，歧义标红不硬磕）

## 阶段 1 sandbox 核心动作详解

**一句话讲清在干啥+为什么**：阶段 1 sandbox 要干的是实现 B5 短时谱 FOE + [60] Leven Mth-power 两个估计器，跟传统 FFT FOE 做三方对照，在湍流信道下验证 B5 范围优势（捕获范围 ±4.5GHz + 残频 σ<140MHz + 收敛性）是否仍成立——因为路径 C 的够格叙事全靠范围优势，0.3b 理论验证 PASS 但残频带 sandbox 确认条件（低 SNR 块归一化放大噪声风险），sandbox 是路径 C 的实测验证维度。

**1a 简版理论预期**（TL-20，sandbox 前必写）：
- **捕获范围**：B5 ±4.5GHz / 传统 FFT FOE ±312.5MHz / [60] Leven ±1.6GHz（B5 锚 L117 + fft_foe 范围 + [60] Leven L157）
- **残频 σ（无湍流 AWGN）**：B5 应 <140MHz（B5 锚 L23/L47），传统 FFT FOE 应 <312.5MHz（精估范围边界），[60] Leven 应 <10MHz（精细 FE）
- **残频 σ（有湍流）**：B5 前馈归一化后应仍 <140MHz（0.3b 验证2 理论成立），若超 140MHz → 红线警报
- **范围扩展**：B5 / 传统 FFT FOE 应 ≥10×（15× 预期），B5 / [60] Leven 应 ≥2×（2.8× 预期）

**1b 实现 short_time_spectrum_foe**（接口在 `_file_organization.md`）：
- 参考 fft_foe_m0_omega（sc_nda_ml_sim.py:137-166）起点骨架：分块 FFT + Hanning窗 + zero-pad + 抛物线插值（工程实现复用）
- 核心新写：正负功率谱面积比 Rp-n（式3）+ 归一化频偏估计 Δfest=α×Rp-n（式2，α=6×10⁸）
- **normalize_mode 三方案**（0.3a 决策）：'block'（块内归一化除以块总功率）/ 'agc'（AGC 前置）/ 'ratio'（Rp-n=(P_+−P_−)/(P_++P_−)）—— sandbox 选最优
- 星历预测调 LO（前馈开环，0.3a 确认非环路 TF）
- 参数从 B5Params 导入（禁硬编码，sim-preflight param-source.md）

**1c 实现 [60] Leven Mth-power**（祖师爷对照，common 没有）：
- [60] Leven L55-65 算法：rx × conj(rx_prev) → 4次方（QPSK M=4）→ 500样本求和 → 相位除4 → 累加相位补偿
- 时域相位增量（非频域谱峰），跟 B5 频域功率比机制不同（C7 三方对照验证机制差异）

**1d 三方对照**（sim-preflight V2/C7）：
- 三方法都做前馈归一化（公平保证，0.4.1 决策）
- 共用同一信道实现（TL-13，从 common/_channel.py 导入 `generate_shared_realization`）
- 扫 Doppler ±4.5GHz 全量程（确认捕获范围差异）
- 双工作点 BER 1e-3 + HD-FEC 3.8e-3（0.4.3 决策）
- 湍流信道：从 common 继承湍流参数（Cn² / ΓΓ a,b），不自建

**1e fair gain 二维报告**：
- 范围扩展表：三方法的捕获范围 + Doppler rate 跟踪能力 + 残频指标
- 残频/BER 对比表：三方法在同一湍流信道下的残频 σ + BER 曲线 @ BER 1e-3 和 HD-FEC 3.8e-3

**判定门控**：
- B5 范围扩展 ≥10× + 湍流下残频 σ 不超 140MHz + 收敛性不退化 → **路径 C sandbox PASS，进 MVE**
- B5 范围优势湍流下消失（残频 σ 超 140MHz 或范围扩展 <10× 或收敛性崩）→ **红线警报（核心机制崩塌），B5-Q1 转 Kill**

## 开场怎么报

按 session-governance Trigger 1 报到，简版即可：

> 续接 B5-Q1 专题（2026-07-08-b5-leo-doppler-spectrum-foe），工作对话对话 2 S003 + H003 派发。本轮目标：执行阶段 1 sandbox 三方对照（B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power），验证路径 C 湍流下范围优势是否成立。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始写简版理论预期（TL-20）然后实现 short_time_spectrum_foe。

---

**主控对话跟进点**（你产出后主控对话会核查）：
- short_time_spectrum_foe 是否真守了前馈归一化（normalize_mode 显式传参，非环路 TF）—— 守 D006 边界
- 三方对照是否真公平（三方法都归一化 + 共用信道 + 双工作点）—— 守 0.4.1 公平性保证
- 湍流下残频 σ 是否真 <140MHz（不是默认成立，0.3b 带 sandbox 确认条件）—— 路径 C 核心前提实测验证
- fair gain 二维报告是否完整（范围扩展表 + 残频/BER 对比表）—— 0.4.2 定义
- sandbox 发现范围优势消失是否立即报红线警报（不"再凑凑看"）—— 红线 5
- B5 vs [60] Leven 任务环节错位是否在报告里标注（粗 CFO vs 精细 FE）—— 0.4.1 警示
