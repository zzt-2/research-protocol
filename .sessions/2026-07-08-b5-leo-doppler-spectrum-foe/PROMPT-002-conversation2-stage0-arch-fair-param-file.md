# PROMPT-002: B5-Q1 对话 2 — 阶段 0.3-0.6 前置规约（架构定性 + 公平对照 + 参数真相源 + 文件组织）

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 对话角色: 工作对话（主控对话派发的执行体，对话 1 的续接）
> 来源: 主控对话 S001 + H001 + 工作对话 S002 + H002 交接
> 日期: 2026-07-08

## 你是谁

你是 B5-Q1 第四候选的工作对话（executor）对话 2，承接对话 1（S002 + H002 交接）。主控对话负责方向决策/跨候选调度/核查你的产出，你负责执行阶段 0.3-0.6 四项前置规约（不写代码）。

**对话 1 已完成阶段 0.1-0.2**：
- 0.1 够格路径验证：**B5-Q1 够格走路径 C（鲁棒性维度）为主 + 路径 A/B 补充，不转 Kill**（B7 OFC 已发先例 + B5 范围 15× 比 B7 1.9× 更强）
- 0.2 dB/范围溯源：20 字段参数全溯源 PASS（[60] Leven 7dB penalty 溯源到原文 L123，残频上限公式 Δfm=fs/8N 溯源到 sat.1553 引 [60] Leven 公式 27）

**纪律**：
- 主控对话交代的角色边界要守——你只执行阶段 0.3-0.6 四项规约，不进 sandbox 不写 MVE 代码
- 每个阶段开始前先一句话讲清"在干啥+为什么"再动手（profile 第 9 次"急于推进"防线）
- 子 agent 产出要主线独立 grep 核查（只信原始数字不信归因，D-009 教训 6）

## 你的任务（H002 交接，简版）

**执行阶段 0.3-0.6 四项前置规约**（不写代码），核心是阶段 0.3 验证前馈归一化后 B5 范围优势是否仍成立（路径 C 的核心前提）：

- **阶段 0.3（最高优先）**：架构定性。湍流致功率波动归一化走前馈路径（合法不撞 D006），禁环路 TF 联合建模。**关键前提验证**：前馈归一化（AGC/归一化功率比）后 B5 范围优势（±4.5GHz 覆盖 + 残频落精估范围）是否仍成立？若前馈归一化后范围优势消失 → 红线警报（核心机制崩塌，路径 C 崩塌）
- **阶段 0.4**：公平对照框架。baseline [60] Leven Mth-power 还是传统 FFT FOE？范围 fair gain 定义？工作点 BER 1e-3 还是 HD-FEC？LEO Doppler 主题跟 B7/B4 差异化（B5 频域功率比 vs B7 定时域 TED vs B4 双环）
- **阶段 0.5**：参数真相源前置。B5Params 草稿 20 字段全溯源已就绪（`_db_range_sourcing_audit.md` §6 表），参考 B7Params 扩写
- **阶段 0.6**：文件组织规约。`explore/b5-leo-doppler-spectrum-foe/` 目录结构 + short_time_spectrum_foe 接口定义（参考 fft_foe_m0_omega sc_nda_ml_sim.py:137 作起点骨架）

**判定门控**：阶段 0.3 如果前馈归一化后范围优势崩塌 → 红线警报，B5-Q1 转 Kill（核心机制崩塌，不是够格路径问题）

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**（FR-22 框架强制门控）：

### 1. 本专题文件（最重要，必读全）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/H002-conversation2-stage0-arch-fair-param-file.md` — 完整交接（含 0.3-0.6 详细动作 + 纪律 + 验证阈值 + 已知债务）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/S002-conversation1-stage0-qualification-and-sourcing.md` — 对话 1 记录（0.1-0.2 执行详情）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/topic-index.md` — **14 不变量**（重点 11/12/13/14 B5 特殊风险）+ 悬而未决（0.1 已解决，0.3-0.4 待决）
- `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/decisions.md` — D001 决策详情

### 2. 对话 1 阶段 0.1-0.2 产出（本轮前置，必读全）
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_qualification_path_validation.md` — 阶段 0.1 够格路径验证（3 选项分析 + 判定门控 + 够格叙事框架 + 风险标注）
- `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_db_range_sourcing_audit.md` — 阶段 0.2 dB/范围溯源（20 字段参数真相源表 + [60] Leven 7dB 溯源 + 残频上限公式溯源 + B5Params 草稿前置）

### 3. B5 锚论文全文 + 详评（0.3 架构定性核查对象）
- `papers/doi/10.1016_j.optcom.2024.130981/content.md` — B5 锚全文 252 行（重点 L57 粗补偿定义 / L71-87 算法原理 / L143-149 实验结果 / L162 D006 边界）
- `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` L55-60（M-C-A）+ L100-167（全文增量核验段）+ L162（D006 边界残留：前馈归一化合法 / 环路 TF 联合建模则撞）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b4b5-verify.md` L59-69（范围优势核验）+ L64-66（"本体无 vs baseline 改善 X dB"警示）

### 4. [60] Leven 原文 + sat.1553 综述（0.4 公平对照 baseline 候选）
- `papers/doi/10.1109_lpt.2007.891893/content.md` — [60] Leven 原文（L123 7dB penalty / L147 最大容许频偏 125MHz block PE / 625MHz diff decode）
- `papers/doi/10.1002_sat.1553/content.md` L548-559（CFO 节 + 残频上限公式 27 + "粗补偿即可"结论）+ L353（SNR penalty vs 完美同步口径）

### 5. 复用基建（0.5 参数族 + 0.6 接口定义）
- `projects/simulation/common/_recovery.py` — fft_foe (L37) / 其他估计器
- `projects/simulation/simulator/sc_nda_ml_sim.py:137` — fft_foe_m0_omega（short_time_spectrum_foe 起点骨架）
- `projects/simulation/params.py` L611-628 — B7Params（B5Params 参数族模板参考）
- `projects/simulation/common/_channel.py` — 信道实现（TL-13 共用，禁自建）

### 6. 框架文件 + 教训
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步（sandbox/MVE 阶段用，本轮 0.3-0.6 前置）
- `thesis-lessons.md` TL-13（共用信道）/ TL-20（先建理论预期）/ TL-26（参数溯源读原文数值）/ TL-27（oracle 上界前置）
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8 + `rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条

### 7. 上游决策链 + 参照候选
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — D005 务实路线 / D006 红线 / D017/D018 判读框架
- `.sessions/2026-07-08-b7-gardner-ted-foe/` — B7 Gardner TED（LEO Doppler rate 适配，机制正交，0.4 差异化对照）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md` L113/119/247 — NDA-ML Doppler 已建模但是残余级（F_RESIDUAL=1MHz），不是 B5 ±4.5GHz 全量程

## 接收方验证（读完文件后必须完成）

逐项打钩后才能动手（H002 §接收方验证）：

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B5 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] B5-Q1 够格走路径 C（核查 `_qualification_path_validation.md` 0.1c 判定门控段）
  - [ ] [60] Leven 7dB penalty 来自 [60] Leven 原文 L123 不是 B5 锚（核查 `_db_range_sourcing_audit.md` §3 + 主线 grep `papers/doi/10.1109_lpt.2007.891893/content.md` L123）
  - [ ] B5 锚 conclusion L167 不含 ±4.5GHz（核查 `_db_range_sourcing_audit.md` §1 + 主线 sed `papers/doi/10.1016_j.optcom.2024.130981/content.md` L163-168）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7/B2 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 执行节奏（守 3 步上限）

**本轮 4 项规约，超 3 步主动建议分对话**。建议拆法：

**方案 A（推荐，4 项全做）**：若 0.3 顺利（前馈归一化后范围优势成立），0.4-0.6 主线定不一定要子 agent，4 项一对话做完
- 步骤 1：报到 + 读必读清单 1-7 + 接收方验证
- 步骤 2：阶段 0.3 架构定性（最高优先，路径 C 核心前提验证）
- 步骤 3：阶段 0.4 公平对照框架 + 0.5 参数真相源 + 0.6 文件组织（三项合并一步，主线定）

**方案 B（0.3 有风险时拆对话）**：若 0.3 发现前馈归一化后范围优势有崩塌风险（需深入论证），0.3 单独一对话，0.4-0.6 留对话 3
- 本轮只做 0.3，输出 `_architecture_decision.md` + 红线警报（若崩塌）或 PASS（若成立）
- 0.4-0.6 留对话 3

**判定**：0.3 完成后判断走方案 A 还是 B。若 0.3 PASS 且上下文允许，继续 0.4-0.6；若 0.3 发现风险或超 3 步，写 H003 交对话 3。

## 产出物（本轮交付）

1. `explore/b5-leo-doppler-spectrum-foe/_architecture_decision.md` — 阶段 0.3 架构定性（前馈归一化 vs 环路 TF + 范围优势前提验证）
2. `explore/b5-leo-doppler-spectrum-foe/_fair_comparison_framework.md` — 阶段 0.4 公平对照框架（baseline + fair gain + 工作点 + LEO Doppler 差异化）
3. `explore/b5-leo-doppler-spectrum-foe/_b5_params_draft.md` — 阶段 0.5 B5Params 草稿（20 字段全溯源，参考 B7Params）
4. `explore/b5-leo-doppler-spectrum-foe/_file_organization.md` — 阶段 0.6 文件组织规约（目录结构 + short_time_spectrum_foe 接口定义）
5. S003 session note — 本轮记录
6. H003 handoff — 交下一对话执行 sandbox（若 0.3-0.6 全完成）或 0.4-0.6（若只做 0.3）

**explore/ 目录在 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/`**（不是根目录的 explore/）。

## 红线（违反必须停）

1. **禁直接当 Go 跑 MVE**（阶段 0.3-0.6 未完成 + profile 第 9 次防线）
2. **禁跳阶段 0 直接写代码**（profile 第 9 次防线 + INVARIANT 6）
3. **禁走环路 TF 联合建模**（阶段 0.3 湍流致功率波动归一化必须走前馈路径，撞 D006）
4. **禁自建信道**（TL-13，从 common/_channel.py 导入）
5. **禁污染 common**（explore 探针不进 experiments，MVE 通过才转正）
6. **禁忽视路径 C 崩塌信号**（0.3 发现前馈归一化后范围优势消失 → 红线警报，不能"再凑凑看"）

## 阶段 0.3 核心动作详解（最高优先）

**一句话讲清在干啥+为什么**：阶段 0.3 要干的是定死 B5 的架构走前馈归一化路径（不走环路 TF 联合建模撞 D006），并验证前馈归一化后 B5 的范围优势（±4.5GHz 覆盖 + 残频落精估范围）是否仍成立——因为路径 C 的够格叙事依赖范围优势，若湍流致功率波动污染正负功率谱面积比导致前馈归一化也救不回范围优势，则核心机制崩塌，B5-Q1 转 Kill。

**0.3a 架构定性**（主线定，可派子 agent 核查 B5 锚 L71-87 算法原理）：
- B5 前馈功率比假设信号幅度稳定（`_B5-...-increment.md:162`），湍流致幅度衰落会污染功率比估计 Rp-n
- **前馈归一化路径**（合法不撞 D006）：AGC 归一化接收功率 / 归一化功率比 Rp-n（除以总功率消除幅度起伏）→ 湍流致功率波动被归一化吸收，功率比估计仍可用
- **环路 TF 联合建模**（撞 D006）：把湍流相位起伏纳入环路传递函数 H(z) → 撞 D006 红线（B1 换皮模式，D006 Kill）
- 决策：**走前馈归一化**（避免 D006 纠缠），但需论证前馈归一化后 B5 的范围优势是否还成立

**0.3b 范围优势前提验证**（路径 C 核心）：
- 前馈归一化后，B5 的 ±4.5GHz 捕获范围是否仍成立？（捕获范围由 FFT 带宽 + 星历预测决定，跟幅度归一化无关 → 应仍成立）
- 前馈归一化后，B5 的残频指标（σ<140MHz / <5MHz）是否仍成立？（残频由算法精度决定，归一化可能影响低 SNR 下精度 → 需论证）
- 前馈归一化后，B5 的收敛性（3-4 次迭代）是否仍成立？（收敛性跟功率比估计稳定性相关，归一化应提升稳定性 → 应仍成立）
- **若三项都成立 → 路径 C 前提 PASS，进 0.4**
- **若有任一崩塌 → 红线警报，B5-Q1 转 Kill**

**判定门控**：
- 前馈归一化后范围优势仍成立 → 路径 C 前提 PASS，进 0.4
- 前馈归一化后范围优势崩塌 → 红线警报，B5-Q1 转 Kill（核心机制崩塌，不是够格路径问题）

## 开场怎么报

按 session-governance Trigger 1 报到，简版即可：

> 续接 B5-Q1 专题（2026-07-08-b5-leo-doppler-spectrum-foe），工作对话对话 1 S002 + H002 派发。本轮目标：执行阶段 0.3-0.6（架构定性 + 公平对照 + 参数真相源 + 文件组织），不写代码。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始阶段 0.3（路径 C 核心前提验证）。

---

**主控对话跟进点**（你产出后主控对话会核查）：
- 阶段 0.3 的前馈归一化后范围优势是否真验证了（不是默认成立）——三项（捕获范围 / 残频 / 收敛）逐项论证
- 阶段 0.4 的 baseline 选定是否论证了 [60] Leven vs 传统 FFT FOE 的任务环节差异（0.2 已溯源 [60] Leven 7dB penalty 是 differential decoding 无 FE 场景，不是 B5 vs [60] Leven 直接对比基线）
- 阶段 0.5 的 B5Params 是否全标 source_type + source + audit_flag + 原文行号
- 阶段 0.6 的 short_time_spectrum_foe 接口是否参考了 fft_foe_m0_omega 作起点骨架
- B5 vs B7/B4 的 LEO Doppler 主题差异化是否明确（B5 频域功率比 vs B7 定时域 TED vs B4 双环）
