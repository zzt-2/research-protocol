# Handoff: 对话 2 — 阶段 0.3-0.6 前置规约（架构定性 + 公平对照 + 参数真相源 + 文件组织）

> 来源: S002 | 交接目标: 新工作对话执行阶段 0.3-0.6 四项规约
> 文件名: H002-conversation2-stage0-arch-fair-param-file.md
> 日期: 2026-07-08

## 到哪了（状态）

阶段 0.1（核心命题张力验证设计）+ 阶段 0.2（dB 溯源核查）**完成**。两份产出已落盘：
- `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md`（阶段 0.1，4 维度分解 + fair comparison 框架）
- `explore/b2-fade-freeze-pilot-fallback/_db_sourcing_audit.md`（阶段 0.2，sat.1553 +1dB 口径限定）
- `explore/b2-fade-freeze-pilot-fallback/_step4a_detail_extract.md`（子 agent T### 核查 step4a 实测细节，阶段 0.1 输入）

**核心结论**：B2-Q2 命题张力**可分解不直接 Kill**。B2-Q2 真正增量可能在**动态恢复时间**（step4a 没测的维度），不是稳态 BER。但维度 C2（pilot-aided 路线在单载波时域根本弱）是红线风险，sandbox 三方对照（阶段 1）必须回答。

**未写代码，未进 sandbox**（守 profile 第 9 次防线 + INVARIANT 6）。

## 不要做什么（踩过的坑、已排除的方向）

1. **不要直接搬 sat.1553 L440 +1dB 当 B2-Q2 的 dB**：阶段 0.2 已确认口径错位（PE vs VV+diff，QPSK+OFDM，不是 FOE freeze 双模切换 vs blind freeze @ 16-APSK 单载波）。B2-Q2 增量必须 MVE 产出
2. **不要跳阶段 0 直接写代码**：profile 第 9 次"急于推进"防线 + INVARIANT 6。六项规约全做完才进 sandbox。本轮做 0.3-0.6（4 项）
3. **不要绕过维度 C2 红线风险**：阶段 0.1 发现"所有 pilot-aided 变体在 fade 是否都输 NDA-ML"是 sandbox 必答问题。阶段 0.4 公平对照框架要把这个写进判定门控
4. **不要把 B2-Q2 当"稳够格"候选**：四重风险（dB 口径错位 + 实测反证 + 饱和池小池 + 叙事撞车）。如果 sandbox 发现 B2-Q2 在动态恢复也打不过纯 blind freeze → 核心命题崩塌转 Kill
5. **不要自建信道**：B2 从 `common/_channel.py` 导入（TL-13）
6. **不要污染 common**：explore 阶段探针不直接进 experiments，MVE 通过才转正
7. **不要用 σp² 名义塞 fade 三档**：阶段 0.1 子 agent 发现 σp² 是 Wiener PN 单值（2.51e-5），weak/moderate/strong 是 GG α/β 块衰落三档（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8）。sat.1553 σp²=0.25 是 Rytov 方差，不同物理量。阶段 0.5 参数真相源要严格区分

## 必读（按优先级）

1. **本 H002 + topic-index**（14 不变量，重点 11/12/13/14 B2 特殊）
2. **S002**（阶段 0.1-0.2 记录 + 4 维度分解结论 + dB 溯源结论）
3. **阶段 0.1-0.2 产出**（必读，下一对话直接用）：
   - `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md`（4 维度分解 + fair comparison 三方对照矩阵 + 测度分离）
   - `explore/b2-fade-freeze-pilot-fallback/_db_sourcing_audit.md`（sat.1553 +1dB 口径限定 + B2-Q2 叙事锚点 [58]）
   - `explore/b2-fade-freeze-pilot-fallback/_step4a_detail_extract.md`（step4a 实测细节，阶段 0.5 参数真相源输入）
4. **S001 + H001**（开题 + 阶段 0 规约设计 + 复用基建盘点）
5. **B2-Q2 详情**：`papers/_read_notes/_B2-deep-fade-freeze-increment.md`（M-C-A 主体）
6. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe L37 / nda_ml_recovery L171 / da_ml_recovery L136 / psa_foe_recovery L435）
7. **框架文件**：`stages/gw-feasibility.md` §D 维度 D + thesis-lessons TL-13/20/26
8. **上游决策链**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md`（D005 务实路线 / D006 红线 / D017/D018 判读框架）

## 下一步干什么（对话 2 = 阶段 0.3-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.3-0.6（4 项），不进 sandbox。
> **守 3 步上限**：0.3+0.4 主线定（架构+公平对照，核心），0.5+0.6 主线定（参数+文件组织，机械）。若超 3 步主动建议分对话。

### 步骤 1：报到 + 重读关键文件 + 接收方验证

报到（session-governance Trigger 1）+ 读必读清单 1-8 + 完成接收方验证（含验证 S002 阶段 0.1-0.2 结论）。

### 步骤 2：阶段 0.3 架构定性 + 阶段 0.4 公平对照框架（核心）

**0.3 架构定性（前馈 vs 环路 TF）**（继承 INVARIANT + D006）：
- B2-Q2 双模切换 = (fft_foe/nda_ml + 功率阈值 gating) ↔ (da_ml/psa_foe) 模式切换
- 盲侧 fft_foe 是前馈（`_recovery.py:37`），pilot 侧 da_ml 是前馈闭式（`_recovery.py:136-167` 线性回归），整体双模切换可前馈化
- 决策：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策）
- **建议前馈化**（避免 D006 纠缠），但需论证前馈化后 B2-Q2 的"双模切换"创新是否还成立
- 输出 `explore/b2-fade-freeze-pilot-fallback/_architecture_decision.md`

**0.4 公平对照框架设计**（INVARIANT 13 B2 特殊饱和池警示 + 阶段 0.1 输入）：
- **baseline 是纯 blind freeze [79]**（不是 sat.1553 blind gating）—— 阶段 0.1 三方对照矩阵方案 A
- **fair gain 双测度**（阶段 0.1 结论）：
  - 稳态 BER（跟 step4a 同测度，确认非 fade 期不退化）
  - **动态恢复时间**（B2-Q2 最可能增量维度，step4a 没测）
- **pilot overhead 摊薄**：B2-Q2 pilot 只在 fade 期发，overhead = fade 占空比 × 25%。需定义 fade 占空比（功率阈值 γ_th 以下算 fade）
- **fair gain 阈值**：稳态 BER 维度跟 NDA-ML HD-FEC 3.8e-3 对齐；动态恢复时间维度定多少符号数算"显著改善"需论证
- **叙事定位**（B2-Q2 跟 NDA-ML 撞车对策 + 阶段 0.2 发现）：用 sat.1553 L440 [58] "pilot+盲组合 open direction" 作为动机锚，明确双模切换 vs 纯盲的差异化（双模切换的增量是 fade 恢复时间不是稳态 BER）
- **范围维度**（饱和池 dB 难出区警示）：B2-Q2 增量是 dB 还是范围/鲁棒性维度？strong 湍流下纯 blind HD-FEC 不可达，双模切换可能可达——这是范围维度增量
- **判定门控**（阶段 0.1 红线）：sandbox 后 B2-Q2 在动态恢复也打不过纯 blind freeze → 核心命题崩塌转 Kill
- 输出 `explore/b2-fade-freeze-pilot-fallback/_fair_comparison_framework.md`

### 步骤 3：阶段 0.5 参数真相源 + 阶段 0.6 文件组织（机械）

**0.5 参数真相源前置**（TL-26 + FR-26 读原文数值 + 阶段 0.1 子 agent 发现）：
- **严格区分 σp²（Wiener PN 单值 2.51e-5）vs GG α/β（fade 三档）**——子 agent 发现的命名混淆必须消除
- B2 参数一开始进 params.py 单字段：
  - fade σp²（Wiener PN，2.51e-5，全场景统一 10kHz@2.5GBaud，D-007）
  - GG α/β（weak α4/β3 / moderate α2.5/β1.8 / strong α1.5/β0.8，从 `params.py:98,108,118,128,138,148`）
  - OSNR 工作点（SNR_TURB [5,10,15,20,22,24,26]，从 `_time_domain_crlb.py:555`）
  - 符号率/线宽（2.5GBaud / 10kHz，D-007 统一）
  - pilot 配置（spacing=4 / 真符号 pilot / 25% overhead，从 step4a；B2-Q2 fade 占空比 × 25% 摊薄待 0.4 定义）
- 每个参数全标 source_type + source + audit_flag + **读原文具体数值**
- **附带任务**：查 sat.1553 ref [58] 具体论文（阶段 0.2 发现的 B2-Q2 叙事锚点，content.md reference list 未完整转换）
- 输出 params.py 的 B2Params 类草稿（不直接写 params.py，先在 explore 里草拟）

**0.6 文件组织规约**：
- 定死 `explore/b2-fade-freeze-pilot-fallback/` 目录结构（已有 3 文件：_step4a_detail_extract / _tension_validation_design / _db_sourcing_audit）
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）
- 输出 `explore/b2-fade-freeze-pilot-fallback/_file_organization.md`

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。进入新阶段前先一句话讲清"在干啥+为什么"
2. **INVARIANT 11 核心命题张力**（阶段 0.1 已消化）：阶段 0.4 公平对照框架必须把维度 C2 红线（所有 pilot-aided 变体在 fade 是否都输 NDA-ML）写进判定门控
3. **INVARIANT 12 dB 口径错位**（阶段 0.2 已限定）：B2-Q2 增量必须 MVE 产出，不能引 sat.1553 +1dB。阶段 0.4 fair gain 阈值要独立论证
4. **INVARIANT 13 饱和池 dB 难出区**：B2-Q2 可能靠范围/鲁棒性维度够格（D005 会议门槛放宽允许），阶段 0.4 要明确
5. **INVARIANT 14 复用基建边界**：step4a DA ML 是单载波近最优（pilot spacing=4 密集真符号 pilot），非 B11 decision-feedback DA ML。psa_foe_recovery（L435）step4a 未调用，B2-Q2 若用需注意
6. **σp² 命名混淆防线**（阶段 0.1 子 agent 发现）：σp² 是 Wiener PN 单值，weak/moderate/strong 是 GG α/β。阶段 0.5 严格区分，禁用 σp² 名义塞 fade 三档
7. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
8. **TL-13 共用同一信道**：B2 从 `common/_channel.py` 导入，禁自建
9. **核查机制中性双向**（继承）：子 agent 产出 + 主线独立 grep 核查，只信原始数字不信归因

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约。核查脚本若写，放 `explore/b2-fade-freeze-pilot-fallback/`，私有 `_` 前缀，不进 experiments/）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**阶段 0.1-0.2 结论：张力可分解不直接 Kill**，但维度 C2 红线风险明确（sandbox 阶段 1 必答）。

**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**B2-Q2 潜在失败模式**（阶段 0.1 识别，未触发）：
- sandbox 阶段 1 发现 B2-Q2 在动态恢复也打不过纯 blind freeze → 核心命题崩塌转 Kill
- 维度 C2 成立（所有 pilot-aided 变体在 fade 都输 NDA-ML）→ 核心命题崩塌转 Kill

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B2-Q2 真实增量未量化 | INVARIANT 12 | pending MVE | 阶段 3 MVE 产出 |
| sat.1553 +1dB 口径限定 | INVARIANT 12 | ✅ 阶段 0.2 已限定 | 本文件 §阶段 0.2 |
| B2-Q2 跟 NDA-ML 叙事撞车 | INVARIANT 13 | 阶段 0.4 明确差异化（用 sat.1553 [58] 锚）| 0.4 |
| step4a DA ML 配置口径差异 | INVARIANT 14 | ✅ 阶段 0.1 已核查（spacing=4 真符号 pilot）| 本文件 §阶段 0.1 |
| ref [58] 具体论文待查 | 阶段 0.2 发现 | pending | 0.5 附带 |
| fade 占空比定义（pilot overhead 摊薄）| 阶段 0.1 维度 B | pending | 0.4 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 张力验证设计 | fair comparison 把 step4a 实测反证分解为配置/触发/类型/场景差异 | INVARIANT 11 | ✅ PASS（本对话，4 维度全可分解）|
| 阶段 0.2 dB 溯源核查 | sat.1553 +1dB 限定到原始口径（PE vs VV+diff）| INVARIANT 12 + V6 | ✅ PASS（本对话，原口径锁定）|
| 阶段 0.3 架构定性 | 前馈化合法不撞 D006 | 继承 INVARIANT | 未跑（下一对话）|
| 阶段 0.4 公平对照框架 | 双测度（稳态 BER + 动态恢复）+ pilot overhead 摊薄 + 叙事定位 | INVARIANT 13 + 阶段 0.1 输入 | 未跑（下一对话）|
| sandbox 三方对照 | 双模切换/纯 blind freeze/纯 pilot-aided 三方归因可信 + 维度 C2 回答 | V2+C7 (v1.3.0) | 未跑（阶段 1）|
| MVE fair gain | ≥0.5dB @ HD-FEC 或范围/鲁棒性维度够格 | D005 + INVARIANT 13 | 未跑（阶段 3）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B2 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 阶段 0.1 张力可分解不直接 Kill（核查 `_tension_validation_design.md` §4.1 结论）
  - [ ] 阶段 0.2 sat.1553 +1dB 口径=PE vs VV+diff（核查 `_db_sourcing_audit.md` §1.2 + sat.1553 content.md:440 原文）
  - [ ] 维度 C2 红线风险（所有 pilot-aided 变体在 fade 是否都输 NDA-ML 是 sandbox 必答）（核查 `_tension_validation_design.md` §2 维度 C）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 3**（阶段 0.3-0.6 完成后）：
- 阶段 1 sandbox 三方对照（双模切换 / 纯 blind freeze [79] / 纯 pilot-aided）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报（[79] Matsuda 是祖师爷）
- **必答维度 C2**：所有 pilot-aided 变体（da_ml/psa_foe/power-boosted）在 fade 是否都输 NDA-ML
- **必测动态恢复时间**：B2-Q2 双模切换在 fade 恢复时间上是否优于纯 blind freeze
- sandbox 发现双模切换打不过纯 blind freeze → 红线警报（核心命题崩塌，阶段 0.1 维度 C2 成立，转 Kill）

**对话 4**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
