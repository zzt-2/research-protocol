# Handoff: 对话 3 — 阶段 1 sandbox 三方对照（B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power）

> 来源: S003（工作对话对话 2）| 交接目标: 新工作对话执行阶段 1 sandbox 三方对照
> 文件名: H003-conversation3-sandbox-three-way.md
> 日期: 2026-07-08

## 到哪了（状态）

工作对话对话 2 完成阶段 0.3-0.6 四项前置规约（架构定性 + 公平对照 + 参数真相源 + 文件组织），**未写代码，未进 sandbox**（守 profile 第 9 次防线 + INVARIANT 6）。**阶段 0 六项规约全收尾，可进 sandbox。**

**阶段 0.3 核心结论**：B5 架构定死走前馈归一化路径（合法不撞 D006），禁环路 TF 联合建模（撞 D006 Kill）。**前馈归一化后范围优势三项验证全 PASS**（捕获范围 ±4.5GHz 确定成立 / 残频 σ<140MHz 理论成立带 sandbox 确认 / 收敛性 3-4 次迭代成立应提升）。路径 C 前提 PASS，不转 Kill。

**阶段 0.4 核心结论**：baseline = 传统 FFT FOE（fft_foe common/_recovery.py:37）为主 + [60] Leven Mth-power 作祖师爷对照（C7 三方对照用）。fair gain 二维报告（范围扩展 + 残频/BER）。双工作点 BER 1e-3 + HD-FEC 3.8e-3。B5/B7/B4 机制正交无撞车（频域功率比 / 定时域 TED / 双环架构）。

**阶段 0.5 核心结论**：B5Params 草稿 20 字段全溯源 PASS（R_SYM=2.5GBaud / LASER_LW=20kHz / DOPPLER_RANGE=±4.5GHz / ALPHA=6×10⁸ / FFT 1024 组 16 点 / 残频 σ<140MHz / BER 1e-3 −48dBm 等，全标 content.md 行号）。

**阶段 0.6 核心结论**：explore 目录结构规约 + short_time_spectrum_foe 接口定义（参考 fft_foe_m0_omega 作起点骨架，分块 FFT 复用 + Rp-n 核心新写，含 normalize_mode 参数化空间）+ 下游引用同步清单。

## 下一步干什么（对话 3 = 阶段 1 sandbox 三方对照）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 已全完成，本对话进 sandbox。守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报 + C7 三方对照。
> **守 3 步上限**：sandbox 三方对照主线定，可派子 agent 跑脚本。

### 阶段 1 sandbox 三方对照（sim-preflight V2/C7）

**核心任务**：在湍流信道下验证 B5 范围优势是否仍成立（路径 C 的 sandbox 验证维度）。

**三方**：
1. **B5 短时谱 FOE**（short_time_spectrum_foe，需实现，参考 fft_foe_m0_omega 作起点骨架）
2. **传统 FFT FOE**（fft_foe common/_recovery.py:37，主 baseline，已实现）
3. **[60] Leven Mth-power**（祖师爷对照，需实现，时域 4 次方 + 500 样本相位增量，[60] Leven L55-65）

**公平性保证**（0.4.1 决策）：
- 三方法都做前馈归一化（normalize_mode 显式传参，sandbox 选最优方案）
- 三方法共用同一信道实现（TL-13，从 common/_channel.py 导入 `generate_shared_realization`，禁自建）
- 三方法都扫同一 Doppler 范围（±4.5GHz 全量程，确认捕获范围差异）
- 三方法都用双工作点评估（BER 1e-3 + HD-FEC 3.8e-3）

**fair gain 二维报告产出**：
1. 范围扩展表：三方法的捕获范围 + Doppler rate 跟踪能力 + 残频指标
2. 残频/BER 对比表：三方法在同一信道（含湍流）下的残频 σ + BER 曲线 @ BER 1e-3 和 HD-FEC 3.8e-3

**判定门控**：
- B5 范围扩展 ≥10×（15× 满足）+ 湍流下残频 σ 不超 140MHz + 收敛性不退化 → **路径 C sandbox PASS，进 MVE**
- B5 范围优势在湍流下消失（残频 σ 超 140MHz 或范围扩展 <10×）→ **红线警报（核心机制崩塌），B5-Q1 转 Kill**

### sandbox 实现要点

1. **short_time_spectrum_foe 实现**（接口定义在 `_file_organization.md`）：
   - 分块 FFT（n_fft=16 点/块）+ 均值滤波（n_blocks=1024 组）复用 fft_foe_m0_omega 的工程实现
   - 正负功率谱面积比 Rp-n（式 3）+ 归一化频偏估计 Δfest = α × Rp-n（式 2，α=6×10⁸）需新写
   - normalize_mode 三方案（'block' 块内归一化 / 'agc' AGC 前置 / 'ratio' 归一化功率比）sandbox 选最优
   - 参数从 B5Params 导入（sim-preflight param-source.md，禁硬编码）

2. **[60] Leven Mth-power 实现**（祖师爷对照）：
   - [60] Leven L55-65：rx × conj(rx_prev) → 4 次方（QPSK M=4）→ 500 样本求和 → 相位除 4 → 累加相位补偿
   - 时域相位增量（非频域谱峰），跟 B5 频域功率比机制不同

3. **信道实现**（TL-13，禁自建）：从 `common/_channel.py` 导入 `generate_shared_realization`，湍流参数（Cn² / ΓΓ a,b）从 common 继承

### 阶段 2 TL-20 理论预期表（sandbox 通过后，对话 4）

仿 N1-MVE-SPEC.md §2，写 B5-MVE-SPEC.md 含 TL-20 理论预期表（残频 σ 随 SNR/Doppler/湍流强度的预期曲线），sandbox 偏离即查（TL-20）。

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 已全完成可进 sandbox。但 sandbox 发现范围优势消失必须停报红线警报，不能"再凑凑看"
2. **INVARIANT 13 D006 边界**（B5 特殊）：short_time_spectrum_foe 实现必须走前馈归一化路径（normalize_mode 显式传参），禁环路 TF 联合建模
3. **INVARIANT 14 代码基建新增需求**（B5 特殊）：short_time_spectrum_foe 需新写（分块 FFT 复用 fft_foe_m0_omega，Rp-n 核心新写）。[60] Leven Mth-power 也需新写（祖师爷对照）
4. **TL-13 共用同一信道**：从 `common/_channel.py` 导入，禁自建信道
5. **核查机制中性双向**（INVARIANT 10）：子 agent 跑脚本 + 主线独立 grep 核查结果，只信原始数字不信归因（D-009 教训 6）
6. **TL-26 + FR-26 + V6**：每个参数标文献来源 + 读原文具体数值（B5Params 20 字段已全溯源）
7. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1，B5 锚 L71-87 式 2-4 核对）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8，[60] Leven 是祖师爷，B5 vs [60] Leven 持平警报）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
8. **不污染 common**（INVARIANT 14 + 红线 6）：explore 阶段探针不直接进 experiments，MVE 通过才转正。short_time_spectrum_foe 在 explore 验证通过后才进 common

## 接口变更（如有代码改动）

无（阶段 0.3-0.6 未写代码，只定规约）。sandbox 阶段（对话 3）将新增：
- `_short_time_spectrum_foe.py`（explore 探针，接口定义在 `_file_organization.md`）
- `_leven_mthpower_foe.py`（explore 探针，[60] Leven 祖师爷对照）
- `_sandbox_three_way.py`（sandbox 脚本，三方对照）
- B5Params 类进 `params.py`（sandbox 通过后，从 `_b5_params_draft.md` 复制）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**B5-Q1 潜在失败模式**（sandbox 阶段需警惕）：
- **前馈归一化后范围优势消失**（湍流致功率波动污染功率比估计，归一化救不回）→ **核心机制崩塌，路径 C 崩塌**，需立即停并报主控对话
- **B5 vs [60] Leven 残频 dB 不利**（B5 粗 CFO 在湍流下残频 dB 可能不如 [60] Leven 精细 FE）→ 不能作主判据，靠路径 C/A（范围扩展 + 绝对指标）
- **饱和池竞争风险**（INVARIANT 12）：B5 走范围维度不直接跟饱和池 dB 竞争，但 sandbox 需确认范围维度在会议够格下不被饱和池 dB 竞争压倒

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B5-Q1 够格路径已验证（路径 C）| INVARIANT 11 | ✅ 阶段 0.1 完成 | 已解决 |
| B5 dB/范围溯源已核查 | INVARIANT 12 + TL-26 | ✅ 阶段 0.2 完成（20 字段全溯源）| 已解决 |
| 前馈归一化后范围优势是否成立 | INVARIANT 13 + 路径 C 前提 | ✅ 阶段 0.3 理论 PASS（带 sandbox 确认条件）| sandbox 实测确认 |
| 公平对照框架 | INVARIANT 14 | ✅ 阶段 0.4 完成（baseline + fair gain + 工作点 + 差异化）| sandbox 执行 |
| B5Params 参数族 | TL-26 | ✅ 阶段 0.5 完成（20 字段草稿全溯源）| sandbox 时进 params.py |
| short_time_spectrum_foe 需新写 | INVARIANT 14 | ✅ 阶段 0.6 接口定义完成 | sandbox 实现 |
| LEO Doppler 主题跟 B7/B4 差异化 | INVARIANT 14 | ✅ 阶段 0.4.4 完成（机制正交无撞车）| 大论文跨章节叙事 |
| [60] Leven 7dB penalty 语义警示 | FR-26 | ✅ 0.2 溯源完成（是 differential decoding 无 FE 场景）| sandbox 公平对照设计时注意 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B5 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 够格路径验证 | 范围优势能转化成会议够格叙事 | INVARIANT 11 | ✅ PASS（路径 C 成立）|
| 阶段 0.2 dB/范围溯源 | ±4.5GHz + 残频指标全读原文数值 | INVARIANT 12 + V6 | ✅ PASS（20 字段全溯源）|
| 阶段 0.3 架构定性 | 前馈归一化合法不撞 D006 + 范围优势仍成立 | INVARIANT 13 + 路径 C 前提 | ✅ PASS（三项验证全成立，残频带 sandbox 确认）|
| 阶段 0.4 公平对照框架 | baseline 选定 + 范围 fair gain 定义 + LEO Doppler 差异化 | INVARIANT 14 | ✅ PASS（baseline+fair gain+工作点+差异化全定）|
| 阶段 0.5 参数真相源 | B5Params 20 字段全溯源 | TL-26 + V6 | ✅ PASS（20 字段全标行号）|
| 阶段 0.6 文件组织 | explore 目录结构 + short_time_spectrum_foe 接口定义 | INVARIANT 14 + D-007 教训 | ✅ PASS（接口+同步清单全定）|
| sandbox 三方对照 | B5 短时谱/[60] Leven/传统 FFT FOE 三方归因可信 + 范围优势湍流下仍成立 | V2+C7 (v1.3.0) | 未跑 |
| MVE 范围 fair gain | ±4.5GHz 覆盖 + 残频 <5MHz @ BER 1e-3 或范围扩展 ≥10× | D005 + INVARIANT 11 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B5 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 前馈归一化后范围优势三项验证 PASS（核查 `_architecture_decision.md` §0.3b 三项验证表 + 主线 sed B5 锚 L71-87/L93/L117/L141 算法原理）
  - [ ] baseline = 传统 FFT FOE（核查 `_fair_comparison_framework.md` §0.4.1 + 主线 grep `common/_recovery.py:37` fft_foe 接口）
  - [ ] B5Params 20 字段全溯源（核查 `_b5_params_draft.md` §溯源审计汇总表 + 主线 grep B5 锚 content.md 行号）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 3**（本轮 H003 交接）：阶段 1 sandbox 三方对照
- short_time_spectrum_foe + [60] Leven Mth-power 实现
- 三方对照（B5 / 传统 FFT FOE / [60] Leven）+ fair gain 二维报告
- 路径 C sandbox 验证（湍流下范围优势仍成立）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报 + C7
- sandbox 发现范围优势消失 → 红线警报（核心机制崩塌）

**对话 4**（sandbox 通过后）：阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
