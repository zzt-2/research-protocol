# PROMPT-002: B2-Q2 对话 2 — 阶段 1 sandbox 三方对照（首次写代码）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback
> 对话角色: 工作对话（主控对话派发的执行体）
> 来源: 主控对话 S002 + H002 交接
> 日期: 2026-07-08

## 你是谁

你是 B2-Q2 第三候选的工作对话（executor），承接主控对话派发的任务。上一个工作对话（对话 1）已完成阶段 0 六项规约，**阶段 0 满足，可进 sandbox**。你负责执行阶段 1 sandbox 三方对照——**这是 B2-Q2 第一次写代码**。

**纪律**：
- 主控对话交代的角色边界要守——你执行 sandbox 三方对照，核心是回答两个必答问题（维度 C2 红线 + 动态恢复时间），不进 MVE（那是 sandbox 通过后阶段 3 的事）
- 每个步骤开始前先一句话讲清"在干啥+为什么"（profile 第 9 次"急于推进"防线）
- 子 agent 产出要主线独立 grep 核查（只信原始数字不信归因，D-009 教训 6）
- 守 sim-preflight v1.3.0：V2 三方对照 + V3 祖师爷警报（[79] Matsuda 是祖师爷）+ V4 参数变更触发算法重审 + V5 子 agent 归因独立核查 + V6 读原文数值

## 你的任务（H002 交接，简版）

**执行阶段 1 sandbox 三方对照**（首次写代码），核心是回答两个必答问题：

- **必答 1（维度 C2 红线）**：所有 pilot-aided 变体（da_ml/psa_foe/power-boosted pilot）在 fade 是否都输 NDA-ML？
  - 全输 → B2-Q2 核心命题崩塌，向主控对话报告转 Kill（合法选项）
  - 至少一个赢或持平 → C2 不成立，B2-Q2 命题可继续
- **必答 2（动态恢复时间）**：B2-Q2 双模切换 N_recover 是否显著小于纯 blind freeze N_recover？
  - 显著小 → 核心增量成立，进 MVE
  - 无差 → 核心增量不成立，向主控报告转 Kill

**三方实现**：
- 方案 A 纯 blind freeze [79]（fft_foe + 功率阈值 γ_th → fade 期 hold 估计 / 非 fade 期跟踪）—— 祖师爷 baseline
- 方案 B 纯 pilot-aided（da_ml_recovery 全程，复现 step4a 确认 fade 崩溃）
- 方案 C B2-Q2 双模切换（非 fade 期 fft_foe/nda_ml + fade 期 da_ml/psa_foe，前馈门控）

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**（FR-22 框架强制门控）：

### 1. 本专题文件（最重要，必读全）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/topic-index.md` — 14 不变量 + 悬而未决（剩 sandbox 3 项）+ 当前位置=可进 sandbox
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/H002-conversation2-sandbox.md` — 完整交接（含 sandbox 两个必答问题 + 三方实现 + 纪律 + 验证阈值）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/S002-stage0-tension-validation-and-db-sourcing.md` — 阶段 0.1-0.6 全记录
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` — D001 决策（待主控确认是否升 D002 前馈化 INVARIANT）

### 2. 阶段 0 六项规约产出（sandbox 直接依据，必读全）
- `explore/b2-fade-freeze-pilot-fallback/_fair_comparison_framework.md` — sandbox 判定门控 Go/Kill + 三方对照矩阵 + 双测度 + ρ_fade 摊薄（**sandbox 主依据**）
- `explore/b2-fade-freeze-pilot-fallback/_architecture_decision.md` — 前馈化 INVARIANT + 4 估计器前馈性核查（不撞 D006）
- `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md` — 维度 C2 红线 + 动态恢复测度 + 三方对照矩阵雏形
- `explore/b2-fade-freeze-pilot-fallback/_param_truth_source.md` — B2Params 草稿 + γ_th 扫参要求 + ρ_fade 实测要求 + σ²_pN vs GG α/β 严格区分
- `explore/b2-fade-freeze-pilot-fallback/_step4a_detail_extract.md` — step4a 实测细节（sandbox 复现 step4a 依据）
- `explore/b2-fade-freeze-pilot-fallback/_db_sourcing_audit.md` + `_file_organization.md` — 参考用

### 3. 复用基建（4 估计器全在，全前馈闭式）
- `projects/simulation/common/_recovery.py` — fft_foe L37 / nda_ml_recovery L171 / da_ml_recovery L136 / psa_foe_recovery L435
- `projects/simulation/common/_channel.py` — GG 块衰落信道（TL-13 共用，从这导入，禁自建）
- `projects/simulation/explore/single-carrier-nda-ml/_time_domain_crlb.py` — step4a MVE 锚脚本，三方对照复现 step4a 配置时参考其块结构/pilot 配置/公平对照实现

### 4. 框架文件 + 教训
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步
- `thesis-lessons.md` TL-13（共用信道）/ TL-20（先建理论预期）/ TL-26（参数溯源读原文数值）
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8（公式核对/三方对照/祖师爷警报）+ `rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条

### 5. 上游决策链
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — D005 务实路线 / D006 红线（前馈不撞 / 环路 TF 纳入 φ_T 则撞）/ D017/D018 判读框架

### 6. 参照候选教训
- `.sessions/2026-07-06-step4a-mve-execution/` — NDA-ML 6 类混乱教训（参数反复/算法 bug/验证失效/方向重定位/文件混乱/文献引用）+ D-008 双 bug / D-009 线宽选择

## 接收方验证（读完文件后必须完成）

逐项打钩后才能动手（H002 §接收方验证）：

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B2 特殊）+ 悬而未决（剩 sandbox 3 项）
- [ ] 已验证 3 条关键事实声称：
  - [ ] 阶段 0 六项规约全完成（核查 `explore/b2-fade-freeze-pilot-fallback/` 7 份产出文件存在）
  - [ ] 前馈化不撞 D006（核查 `_architecture_decision.md` §3.1 + `_recovery.py` 4 估计器前馈性）
  - [ ] 维度 C2 红线 + 动态恢复测度（核查 `_tension_validation_design.md` §2 维度 C + `_fair_comparison_framework.md` §2）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 执行节奏（守 3 步上限，sandbox 拆 3 步）

**本轮 3 步**：
1. **报到 + 读必读清单 + 接收方验证**（尤其阶段 0 六项规约产出 + 复用基建签名）
2. **sandbox 第一步：参数实测先行**（γ_th 扫参范围 + ρ_fade 实测，FR-20/TL-26 不拍参数）—— 这步不答核心问题，是 sandbox 的前置
3. **sandbox 三方对照 + 两个必答问题**（维度 C2 红线 + 动态恢复时间）

**超 3 步主动建议分对话**。若三方对照跑完发现需要补测（如 power-boosted pilot 变体 / γ_th 敏感性扫），写 handoff 由下一对话续。

## 产出物（本轮交付）

1. `explore/b2-fade-freeze-pilot-fallback/_b2_params_draft.py` — B2Params 草稿落盘（阶段 0.5 已草拟，sandbox 实测后填 γ_th/ρ_fade）
2. `explore/b2-fade-freeze-pilot-fallback/_sandbox_three_way.py` — sandbox 三方对照脚本（方案 A/B/C 实现）
3. `explore/b2-fade-freeze-pilot-fallback/_gamma_th_sweep.json` — γ_th 敏感性扫描结果
4. `explore/b2-fade-freeze-pilot-fallback/_rho_fade_measure.json` — ρ_fade 实测结果
5. `explore/b2-fade-freeze-pilot-fallback/_sandbox_results.json` — sandbox 三方对照结果（meta 字段强制，含 γ_th/ρ_fade/估计器选择/参数值）
6. S003 session note — 本轮记录（含两个必答问题的答案 + Go/Kill 建议）
7. H003 handoff — 交下一对话（sandbox 通过则交阶段 2 TL-20 + 阶段 3 MVE；sandbox Kill 则交主控对话定夺）

**explore/ 目录在 `projects/simulation/explore/b2-fade-freeze-pilot-fallback/`**（不是根目录的 explore/）。

## 红线（违反必须停）

1. **禁只跑两方**（V2 三方对照）：必须三方全跑（A 纯 blind freeze / B 纯 pilot-aided / C B2-Q2 双模切换），不能只跑 B2-Q2 + 1 个 baseline
2. **禁方案 A 实现偏移**（V3 祖师爷警报）：[79] Matsuda 是祖师爷，方案 A 必须严格实现 freeze 机制（fade 期 hold 上一估计值，不是别的）。实现前先读 `_B2-deep-fade-freeze-increment.md` L33 确认 [79] freeze 机制
3. **禁绕过维度 C2 红线**：sandbox 必答"所有 pilot-aided 变体在 fade 是否都输 NDA-ML"。至少测 da_ml + psa_foe 两个 pilot-aided 变体（power-boosted pilot 视情况补）。全输 → 红线警报向主控报告转 Kill
4. **禁拍 γ_th**（FR-20/TL-26）：γ_th 必须先实测 rx 功率分布再定扫参范围 [γ̄−3σ, γ̄−1σ]，不能拍脑袋定值
5. **禁用 σp² 名义塞 fade 三档**（阶段 0.5 严格区分）：σ²_pN（Wiener PN）= 2.51e-5 单值；GG α/β = fade 三档
6. **禁用环路架构**（阶段 0.3 前馈化 INVARIANT）：fade 检测用开环功率阈值 γ_th，不闭环，不用误差驱动（如 φ̂_blind − φ̂_pilot 驱动切换）
7. **禁污染 common**（阶段 0.6 + INVARIANT）：sandbox 脚本放 `explore/b2-fade-freeze-pilot-fallback/`，不修改 `common/_recovery.py` / `common/_channel.py`，4 估计器只 import
8. **禁用 "improved"/版本号命名**（阶段 0.6 + NDA-ML D-007 教训）：所有文件私有 `_` 前缀，不建子目录
9. **禁把 B2-Q2 当"稳够格"**：sandbox 后若维度 C2 成立或动态恢复无差 → 转 Kill 是合法选项，不是失败

## 判定门控（sandbox 后 Go/Kill，阶段 0.4 §6）

### Go 标准（FR-25，赢传统 baseline，任一满足即 Go）
1. B2-Q2 动态恢复时间显著优于纯 blind freeze（gain_recover ≥ ΔN_min）
2. B2-Q2 在 strong 湍流某些 OSNR 点可达 HD-FEC 而方案 A 不可达（范围扩展）
3. B2-Q2 稳态 BER fair gain @ HD-FEC ≥ 0.5 dB（饱和池难出，bonus）

### Kill 标准（任一满足即 Kill，向主控报告）
1. **维度 C2 红线**：所有 pilot-aided 变体在 fade 都输 NDA-ML
2. B2-Q2 动态恢复时间 ≈ 纯 blind freeze（pilot fallback 没帮助恢复）
3. B2-Q2 稳态 BER 反而比纯 blind freeze 差（非 fade 期切回 blind 引入损失）

## 开场怎么报

按 session-governance Trigger 1 报到，简版即可：

> 续接 B2-Q2 专题（2026-07-08-b2-fade-freeze-pilot-fallback），主控对话 S002 + H002 派发。本轮目标：执行阶段 1 sandbox 三方对照（首次写代码），回答两个必答问题（维度 C2 红线 + 动态恢复时间）。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始 sandbox 第一步参数实测。

---

**主控对话跟进点**（你产出后主控对话会核查）：
- sandbox 三方对照是否真跑了三方（V2）+ 方案 A 是否严格实现 [79] freeze（V3）
- 维度 C2 红线是否真答了（至少 da_ml + psa_foe 两个 pilot-aided 变体在 fade 的表现）
- 动态恢复时间测度是否真测了（滑窗 BER vs 距 fade 结束符号数）
- γ_th 是否先实测功率分布再扫参（FR-20/TL-26 不拍参数）
- Go/Kill 建议是否基于实测数字而非归因（V5 子 agent 归因主线独立核查）
- 若 Kill，是否真触发了红线（维度 C2 / 动态恢复无差 / 稳态退化），不是"感觉不行"
