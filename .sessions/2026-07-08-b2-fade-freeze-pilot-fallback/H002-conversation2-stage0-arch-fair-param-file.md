# Handoff: 对话 2 — 阶段 1 sandbox 三方对照（双模切换 vs 纯 blind freeze vs 纯 pilot-aided）

> 来源: S002（阶段 0.1-0.6 六项规约全完成）| 交接目标: 新工作对话执行阶段 1 sandbox 三方对照
> 文件名: H002-conversation2-stage0-arch-fair-param-file.md（原名保留，内容更新为交阶段 1）
> 日期: 2026-07-08

## 到哪了（状态）

**阶段 0 六项规约全完成**（S002，用户授权"先接着做吧"一次做完）。7 份产出落盘 `explore/b2-fade-freeze-pilot-fallback/`：
- `_step4a_detail_extract.md`（子 agent 核查 step4a 实测细节）
- `_tension_validation_design.md`（阶段 0.1：4 维度分解 + fair comparison）
- `_db_sourcing_audit.md`（阶段 0.2：sat.1553 +1dB 口径限定）
- `_architecture_decision.md`（阶段 0.3：前馈化 INVARIANT 不撞 D006）
- `_fair_comparison_framework.md`（阶段 0.4：baseline/双测度/摊薄/叙事/范围）
- `_param_truth_source.md`（阶段 0.5：σ²_pN vs GG α/β 严格区分 + ref[58] 查证 + B2Params 草稿）
- `_file_organization.md`（阶段 0.6：目录/命名/下游同步/common 防御）

**核心结论**：B2-Q2 命题张力**可分解不直接 Kill**。增量在**动态恢复时间**维度（step4a 没测），**维度 C2 红线风险**（所有 pilot-aided 在 fade 是否都输 NDA-ML）sandbox 必答。前馈化架构不撞 D006（INVARIANT 级，建议升 D002 待主控确认）。

**未写代码，未进 sandbox**（守 profile 第 9 次防线 + INVARIANT 6，阶段 0 六项规约全做完才进 sandbox——现已满足）。

## 不要做什么（踩过的坑、已排除的方向）

1. **不要直接搬 sat.1553 L440 +1dB 当 B2-Q2 的 dB**：阶段 0.2 已确认口径错位（PE vs VV+diff，QPSK+OFDM），五重口径差异。阶段 0.5 进一步查证 [58]=Martins dual-stage CPR，修正叙事锚点（[58] 是 dual-stage 并行，B2-Q2 是 fade 门控切换，机制不同）
2. **不要绕过维度 C2 红线**：阶段 0.1 发现"所有 pilot-aided 变体在 fade 是否都输 NDA-ML"是 sandbox 必答问题。如果 sandbox 发现全部输 → 核心命题崩塌转 Kill（合法选项）
3. **不要把 B2-Q2 当"稳够格"候选**：四重风险（dB 口径错位 + 实测反证 + 饱和池小池 + 叙事撞车）。sandbox 后若动态恢复也打不过纯 blind freeze → 转 Kill
4. **不要自建信道**：B2 从 `common/_channel.py` 导入（TL-13）
5. **不要污染 common**：explore 探针不进 experiments，MVE 通过才转正。sandbox 脚本 `_sandbox_three_way.py` 放 explore 目录
6. **不要用 σp² 名义塞 fade 三档**：阶段 0.5 严格区分——σ²_pN（Wiener PN）= 2.51e-5 单值；GG α/β = fade 三档（weak α4/β3 / moderate α2.5/β1.8 / strong α1.5/β0.8）；sat.1553 σp²=0.25 是 Rytov 方差 σ²_R
7. **不要用环路架构**：阶段 0.3 前馈化 INVARIANT 级。fade 检测用开环功率阈值 γ_th（不闭环，不用误差驱动）
8. **不要用"improved"/版本号命名**：阶段 0.6 命名规则强制，禁 NDA-ML D-007 多目录并存混乱

## 必读（按优先级）

1. **本 H002 + topic-index**（14 不变量 + 悬而未决全消化 + 当前位置=可进 sandbox）
2. **S002**（阶段 0.1-0.6 六项规约全记录 + 主控跟进点）
3. **阶段 0 六项规约产出**（必读，sandbox 直接依据）：
   - `_fair_comparison_framework.md`（sandbox 判定门控 Go/Kill 标准 + 三方对照矩阵 + 双测度 + ρ_fade 摊薄）
   - `_architecture_decision.md`（前馈化 INVARIANT + 4 估计器前馈性核查）
   - `_tension_validation_design.md`（维度 C2 红线 + 动态恢复测度）
   - `_param_truth_source.md`（B2Params 草稿 + γ_th 扫参范围 + ρ_fade 实测要求）
   - `_step4a_detail_extract.md`（step4a 实测细节，sandbox 复现依据）
   - `_db_sourcing_audit.md` + `_file_organization.md`（参考）
4. **S001 + H001**（开题 + 复用基建盘点）
5. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe L37 / nda_ml_recovery L171 / da_ml_recovery L136 / psa_foe_recovery L435，全前馈闭式）
6. **框架文件**：`stages/gw-feasibility.md` §D 维度 D + thesis-lessons TL-13/20/26
7. **sim-preflight v1.3.0**：`rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条 + `SKILL.md` §1.6 C6-C8（尤其 V2 三方对照 + V3 祖师爷警报 [79]）

## 下一步干什么（对话 2 = 阶段 1 sandbox 三方对照，写代码）

> **阶段 0 已满足，可进 sandbox**（profile 第 9 次防线 + INVARIANT 6 满足）
> **守 V2 三方对照 + V3 祖师爷警报**（[79] Matsuda 是 B2-Q2 祖师爷）
> **守 3 步上限**：sandbox 实现分步，若超 3 步主动建议分对话

### 步骤 1：报到 + 重读关键文件 + 接收方验证

报到（session-governance Trigger 1）+ 读必读清单 1-7 + 完成接收方验证（含验证 S002 阶段 0.3-0.6 结论）。

### 步骤 2：sandbox 第一步——参数实测（γ_th 扫参范围 + ρ_fade）

**先行动作**（FR-20/TL-26 不拍参数）：
- 实测 rx 功率分布 P(|rx|²)（weak/moderate/strong × 各 OSNR 点）
- 定 γ_th 扫参范围 [γ̄−3σ, γ̄−1σ]
- 逐点实测 ρ_fade = P(P < γ_th)（每 OSNR × 湍流档）
- 确认 GG α/β 三档文献来源（params.py audit）+ GammaGammaParams 类存在

### 步骤 3：sandbox 三方对照实现 + 必答两个核心问题

**三方实现**（`_sandbox_three_way.py`）：
- **方案 A 纯 blind freeze [79]**：fft_foe + 功率阈值 γ_th → fade 期 hold 上一估计 / 非 fade 期正常跟踪
- **方案 B 纯 pilot-aided**：da_ml_recovery 全程（step4a 已测，复现确认）
- **方案 C B2-Q2 双模切换**：非 fade 期 fft_foe/nda_ml + fade 期 da_ml/psa_foe（前馈门控）

**必答 1（维度 C2 红线）**：所有 pilot-aided 变体（da_ml/psa_foe/power-boosted pilot）在 fade 是否都输 NDA-ML？
- 全输 → 核心命题崩塌，红线警报转 Kill
- 有一个赢 → C2 不成立，B2-Q2 命题可继续

**必答 2（动态恢复时间）**：B2-Q2 双模切换 N_recover vs 纯 blind freeze N_recover
- N_recover,B2Q2 < N_recover,freeze 显著 → 核心增量成立，进 MVE
- N_recover 无差 → 核心增量不成立，红线警报

**测度实现**（阶段 0.4 §2）：
- 稳态 BER @ HD-FEC 3.8e-3（复现 step4a 测度 + B2-Q2 三方）
- 动态恢复时间 N_recover（滑窗 BER vs 距 fade 结束符号数，BER 回稳态 ±10% 所需符号数）

**sandbox 输出**（阶段 0.6 文件组织）：
- `_sandbox_three_way.py`（脚本，私有 `_` 前缀）
- `_sandbox_results.json`（结果，meta 字段强制含参数值）
- `_gamma_th_sweep.json` + `_rho_fade_measure.json`（参数实测）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次防线 + INVARIANT 6 已满足**：阶段 0 六项规约全做完，可进 sandbox。但每个 sandbox 子步骤前仍先讲清"在干啥+为什么"
2. **V2 三方对照**（sim-preflight v1.3.0）：三方归因可信，不能只跑 B2-Q2 + 1 个 baseline
3. **V3 祖师爷警报**：[79] Matsuda 是 B2-Q2 直接祖师爷（sat.1553 L558/L582 引用），方案 A 必须严格实现 [79] freeze 机制（hold 估计，不是别的）
4. **V4 参数变更触发算法重审**：γ_th 从扫描值定到最优值时，重审算法是否需调整
5. **V5 子 agent 归因独立核查**：sandbox 若派子 agent 跑，主线独立 grep results JSON 核查
6. **V6 FR-26 读原文数值**：GG α/β 三档文献来源要读原文数值确认
7. **INVARIANT 11 维度 C2 红线**：sandbox 必答"所有 pilot-aided 在 fade 是否都输 NDA-ML"，全输 → 转 Kill
8. **INVARIANT 12 dB 口径**：sandbox 报 fair gain 时不能引 sat.1553 +1dB，B2-Q2 增量是独立实测
9. **INVARIANT 13 饱和池多维够格**：不押注稳态 BER dB，动态恢复 + 范围扩展 + 鲁棒性任一够格即 Go
10. **INVARIANT 14 复用基建边界**：step4a DA ML 是 pilot spacing=4 真符号 pilot（非 B11 decision-feedback），复用注意口径
11. **前馈化 INVARIANT**（阶段 0.3）：fade 检测用开环 γ_th，不闭环
12. **TL-13 共用信道**：B2 从 `common/_channel.py` 导入
13. **common 防御**（阶段 0.6）：sandbox 脚本放 explore，不进 common

## 接口变更（如有代码改动）

sandbox 阶段写代码（首次）：
- 新增 `explore/b2-fade-freeze-pilot-fallback/_sandbox_three_way.py`（私有 `_` 前缀，不进 experiments）
- 新增 `explore/b2-fade-freeze-pilot-fallback/_b2_params_draft.py`（B2Params 草稿落盘）
- 新增 results JSON（`_sandbox_results.json` / `_gamma_th_sweep.json` / `_rho_fade_measure.json`，meta 字段强制）
- **不修改** `common/` 任何文件（4 估计器已具备，只 import）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**阶段 0.1-0.6 结论：张力可分解不直接 Kill，前馈化不撞 D006**。但 sandbox 阶段 1 可能触发：
- 维度 C2 红线成立（所有 pilot-aided 在 fade 输 NDA-ML）→ 核心命题崩塌转 Kill
- 动态恢复时间无差（B2-Q2 N_recover ≈ freeze N_recover）→ 核心增量不成立转 Kill
- 稳态 BER 退化（B2-Q2 非 fade 期切回 blind 引入损失）→ 架构设计错

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B2-Q2 真实增量未量化 | INVARIANT 12 | pending sandbox | 阶段 1 sandbox 产出 |
| sat.1553 +1dB 口径限定 | INVARIANT 12 | ✅ 阶段 0.2 已限定 | — |
| 前馈化架构不撞 D006 | 继承 INVARIANT | ✅ 阶段 0.3 已论证（建议升 D002）| 主控对话确认 D002 |
| B2-Q2 跟 NDA-ML 叙事撞车 | INVARIANT 13 | ✅ 阶段 0.4 已定位（填补 strong 空白）| — |
| step4a DA ML 配置口径差异 | INVARIANT 14 | ✅ 阶段 0.1 已核查 | — |
| ref [58] = Martins dual-stage | 阶段 0.2 发现 | ✅ 阶段 0.5 已查证（修正叙事锚点）| — |
| γ_th / ρ_fade 实测 | FR-20/TL-26 | pending sandbox 第一步 | 阶段 1 步骤 2 |
| GG α/β 文献来源 | TL-26 | pending | sandbox 前 params.py audit |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 张力验证设计 | fair comparison 把 step4a 实测反证分解为 4 维度 | INVARIANT 11 | ✅ PASS（S002）|
| 阶段 0.2 dB 溯源核查 | sat.1553 +1dB 限定到 PE vs VV+diff | INVARIANT 12 + V6 | ✅ PASS（S002）|
| 阶段 0.3 架构定性 | 前馈化合法不撞 D006 | 继承 INVARIANT | ✅ PASS（S002）|
| 阶段 0.4 公平对照框架 | 双测度+摊薄+叙事+范围 | INVARIANT 13 | ✅ PASS（S002）|
| sandbox 三方对照 | 三方归因可信 + 维度 C2 回答 + 动态恢复测量 | V2+C7 (v1.3.0) | 未跑（阶段 1）|
| sandbox 维度 C2 | 非全输（至少一个 pilot-aided 变体在 fade 赢或持平 NDA-ML）| INVARIANT 11 红线 | 未跑 |
| sandbox 动态恢复 | N_recover,B2Q2 < N_recover,freeze 显著 | 阶段 0.4 核心增量 | 未跑 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或范围/鲁棒性维度够格 | D005 + INVARIANT 13 | 未跑（阶段 3）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B2 特殊）+ 悬而未决（0.1-0.6 全消化，剩 sandbox 待答 3 项）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 阶段 0 六项规约全完成（核查 `explore/b2-fade-freeze-pilot-fallback/` 7 份产出文件存在）
  - [ ] 前馈化不撞 D006（核查 `_architecture_decision.md` §3.1 + `_recovery.py` 4 估计器前馈性）
  - [ ] 维度 C2 红线 + 动态恢复测度（核查 `_tension_validation_design.md` §2 维度 C + §3.2 + `_fair_comparison_framework.md` §2）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 2**（阶段 1 sandbox，本 H002 交接目标）：
- sandbox 三方对照（双模切换 / 纯 blind freeze [79] / 纯 pilot-aided）
- 必答维度 C2 + 必测动态恢复时间 + γ_th 敏感性扫 + ρ_fade 实测
- 守 V2 三方对照 + V3 祖师爷警报（[79]）
- sandbox 发现双模切换打不过纯 blind freeze 或维度 C2 成立 → 红线警报转 Kill

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
- 写 `B2-Q2-MVE-SPEC.md`（正式文件无 `_` 前缀）+ `b2q2_mve.py`
