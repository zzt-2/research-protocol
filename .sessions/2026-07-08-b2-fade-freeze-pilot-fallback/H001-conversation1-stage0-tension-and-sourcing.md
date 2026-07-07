# Handoff: 对话 1 — 阶段 0.1-0.6 前置规约（核心命题张力验证 + dB 溯源 + 架构 + 公平对照 + 参数 + 文件）

> 来源: S001（主控对话开题）| 交接目标: 新工作对话执行阶段 0.1-0.6 六项规约
> 文件名: H001-conversation1-stage0-tension-and-sourcing.md
> 日期: 2026-07-08

## 到哪了（状态）

主控对话开题完成（D001），阶段 0 六项规约设计完成。**未写代码，未进 sandbox**（守 profile 第 9 次"急于推进"防线 + INVARIANT 6）。

**关键张力（工作对话首验证）**：
- step4a 实测"DA pilot 在 deep fade BER 崩溃（5dB weak 0.38）vs NDA 全帧积分鲁棒（0.29）"（`step4a-mve-execution/decisions.md:150, 157`）
- B2-Q2 核心命题"pilot-aided fallback 在 fade 比 blind freeze 更优"
- sat.1553 L440 +1dB 口径错位（PE vs VV+diff，不是 FOE freeze 增量，`_cut-b1b2b3-verify.md:144-146, 342`）

→ **阶段 0.1 = 设计 fair comparison 消化这个张力**，不能直接搬 sat.1553 +1dB。

## 不要做什么（踩过的坑、已排除的方向）

1. **不要直接搬 sat.1553 L440 +1dB 当 B2-Q2 的 dB**：口径错位（PE vs VV+diff 不是 FOE freeze 增量）+ step4a 实测反证双红旗。B2-Q2 真实增量必须独立 MVE 产出
2. **不要跳阶段 0 直接写代码**：profile 第 9 次"急于推进"防线 + INVARIANT 6。NDA-ML 最大混乱就是阶段 0 没做。六项规约全做完才进 sandbox
3. **不要绕过 step4a 实测反证**：阶段 0.1 必须直面这个张力，设计 fair comparison 把它变成可验证假设。绕过 = 重蹈 NDA-ML D-008 覆辙（vs VV 持平被当合理接受）
4. **不要把 B2-Q2 当"稳够格"候选**：四重风险（dB 口径错位 + 实测反证 + 饱和池小池 + 叙事撞车）。如果阶段 0.1 验证后核心命题崩塌，转 Kill 是合法选项
5. **不要自建信道**：B2 从 `common/_channel.py` 导入（TL-13）
6. **不要污染 common**：explore 阶段探针不直接进 experiments，MVE 通过才转正
7. **不要边跑边定架构**：阶段 0.3 定死前馈化 vs 环路（NDA-ML D-002 B11 OFDM→单载波重定位教训）

## 必读（按优先级）

1. **本 H001 + topic-index**（14 不变量，重点 11/12/13/14 B2 特殊风险）
2. **S001** 开题 + 阶段 0 规约设计 + 复用基建盘点
3. **step4a 实测反证**（`.sessions/2026-07-06-step4a-mve-execution/decisions.md:150, 157`）：DA pilot 在 deep fade 崩溃的原始数字
4. **B2-Q2 详情**：
   - `papers/_read_notes/_B2-deep-fade-freeze-increment.md` L64-69（M-C-A 主体）+ L72（陷阱）+ L68（D006 判定）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b1b2b3-verify.md` L144-146, L342（sat.1553 L440 +1dB 口径核验）
   - `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-map-final-b1-b12.md` §A L19-29（饱和池定位）+ §C L118-165（饱和池警示）
5. **复用基建**：`projects/simulation/common/_recovery.py`（fft_foe L37 / nda_ml_recovery L171 / da_ml_recovery L136 / psa_foe_recovery L435）
6. **sim-preflight v1.3.0**：`rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条 + `SKILL.md` §1.6 C6-C8
7. **框架文件**：`stages/gw-feasibility.md` §D 维度 D MVE 11 步 + thesis-lessons TL-13/20/26
8. **上游决策链**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md`（D005 务实路线 / D006 红线 / D017/D018 判读框架）+ S031（B2-Q2 排第二档 #7）

## 下一步干什么（对话 1 = 阶段 0.1-0.6，不写代码）

> **守 profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。本对话做 0.1-0.6（6 项），不进 sandbox。
> **守 3 步上限**：0.1 派子 agent（核查 step4a 实测 + 设计张力验证），0.2-0.6 主线定。若超 3 步主动建议分对话。

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读必读清单 1-8。

### 步骤 2：阶段 0.1 核心命题张力验证设计（B2 最高优先）

> INVARIANT 11（B2 特殊）前置 + sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报。

**0.1a 核查 step4a 实测反证的细节**（派子 agent，≤15 分钟）：
- 读 `.sessions/2026-07-06-step4a-mve-execution/decisions.md:150, 157` 原始数字
- 核查 step4a DA ML 的 pilot 配置（spacing=4？真符号 pilot 还是 pilot symbol？pilot 密度？）
- 核查 step4a 的 fade 场景定义（5dB weak/moderate/strong湍流参数 σp²？）
- 核查"DA pilot 在 fade BER 0.38 vs NDA 0.29"的具体测试条件（BER 工作点？HD-FEC 还是别的？）

**0.1b 设计 fair comparison 消化张力**（主线定）：
- **核心假设**：pilot-aided fallback 在 fade 比 blind freeze 更优（B2-Q2 命题）vs step4a 实测 DA pilot 在 fade 崩溃
- **分解维度**（把张力变成可验证假设）：
  - **维度 A（pilot 配置）**：step4a spacing=4 在 fade 不够密？换更密 pilot 配置（spacing=2？）是否改善 DA pilot 在 fade 的表现？
  - **维度 B（fallback 触发条件）**：B2-Q2 的 fade 检测门控（功率阈值）是否能在 fade 瞬间切到 pilot？step4a 的 DA pilot 是全程 pilot 不是 fallback，机制不同
  - **维度 C（pilot-aided 类型）**：step4a 用 da_ml_recovery，B2-Q2 可用 psa_foe_recovery（不同 pilot 处理方式），机制差异
  - **维度 D（信道场景）**：step4a 是单载波 AWGN+湍流，sat.1553 是 OFDM scenario 4 上行强湍，场景差异
- **判定门控**：
  - 张力可分解为配置/触发/类型/场景差异 → B2-Q2 命题在 fair comparison 下可验证，进 0.2
  - 张力不可分解（pilot-aided 在单载波时域根本打不过盲估）→ **红线警报**，B2-Q2 核心命题崩塌，向用户报告转 Kill
- 输出 `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md`

### 步骤 3：阶段 0.2-0.6（主线定，不一定要子 agent）

**0.2 dB 溯源核查**（INVARIANT 12 B2 特殊）：
- sat.1553 L440 +1dB 口径限定：是 pilot-aided **相位估计** vs VV+差分编码，**不是** pilot-aided FOE vs blind freeze 的增量
- 把 +1dB 限定到原始口径（PE vs VV+diff），B2-Q2 的 FOE freeze 双模切换增量是独立 MVE 的事
- 读 sat.1553 L440 原文数值（不只引位置，FR-26 强化，D-009 教训 5）
- 输出 `explore/b2-fade-freeze-pilot-fallback/_db_sourcing_audit.md`

**0.3 架构定性（前馈 vs 环路 TF）**（继承 INVARIANT + D006）：
- B2-Q2 双模切换 = (fft_foe/nda_ml + 功率阈值 gating) ↔ (da_ml/psa_foe) 模式切换
- 盲侧 fft_foe 是前馈，pilot 侧 da_ml 是前馈闭式，整体双模切换可前馈化（fade 检测门控+模式切换不纳入环路 TF）
- 决策：前馈化（合法不撞 D006）还是环路（撞 D006 需单独决策）
- **建议前馈化**（避免 D006 纠缠），但需论证前馈化后 B2-Q2 的"双模切换"创新是否还成立
- 输出 `explore/b2-fade-freeze-pilot-fallback/_architecture_decision.md`

**0.4 公平对照框架设计**（INVARIANT 13 B2 特殊饱和池警示）：
- baseline 是纯 blind freeze [79] 还是 sat.1553 blind gating？
- fair gain 怎么定义？工作点选 BER 2e-2 还是 HD-FEC 3.8e-3（跟 NDA-ML 一致跨候选可比）？
- pilot overhead 1.25dB 总能量代价怎么公平处理（已在 step4a 制度化）？
- **叙事定位**（B2-Q2 跟 NDA-ML 撞车对策）：明确双模切换 vs 纯盲的差异化（双模切换的增量是 fade 恢复时间还是 BER？）
- 范围维度（饱和池 dB 难出区警示）：B2-Q2 增量是 dB 还是范围/鲁棒性维度？
- 输出 `explore/b2-fade-freeze-pilot-fallback/_fair_comparison_framework.md`

**0.5 参数真相源前置**（TL-26 + FR-26 读原文数值）：
- B2 参数一开始进 params.py 单字段：
  - fade σp²（scenario 4 上行强湍 σp²=0.25，sat.1553 L440）
  - OSNR 工作点（10dB？需读 sat.1553 / Matsuda 原文数值）
  - 符号率 / 线宽（跟 NDA-ML 统一用 LASER_LW 单字段，但 B2 场景可能不同，需论证）
  - pilot 配置（spacing / 真符号 vs pilot symbol / 密度，参考 step4a 配置 + B2 锚论文）
- 每个参数全标 source_type + source + audit_flag + **读原文具体数值**
- 输出 params.py 的 B2Params 类草稿（不直接写 params.py，先在 explore 里草拟）

**0.6 文件组织规约**：
- 定死 `explore/b2-fade-freeze-pilot-fallback/` 目录结构
- 命名规则：私有文件 `_` 前缀（诊断/核查），正式文件无前缀（SPEC/mve）
- 下游引用同步清单（D-007 教训 2：参数改后必须同步清理下游引用）

## 纪律（和下一步直接相关的约束）

1. **profile 第 9 次"急于推进"防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox。**禁跳阶段 0 直接写代码**。进入新阶段前先一句话讲清"在干啥+为什么"
2. **INVARIANT 11 核心命题张力首验证**（B2 特殊）：0.1 必须设计 fair comparison 消化 step4a 实测反证。**绕过张力 = 重蹈 NDA-ML D-008 覆辙**（vs VV 持平被当合理接受）
3. **INVARIANT 12 dB 溯源口径错位前置**（B2 特殊）：0.2 把 sat.1553 +1dB 限定到原始口径（PE vs VV+diff），B2-Q2 增量是独立 MVE 的事。**不能引 sat.1553 +1dB 当 B2-Q2 的 dB**
4. **INVARIANT 13 饱和池 dB 难出区警示**（B2 特殊）：切法地图 §C 警示饱和池是 dB 最难出区。B2-Q2 的 dB 必须 MVE 产出，可能要靠范围或鲁棒性维度够格
5. **INVARIANT 14 复用基建边界**（B2 特殊）：step4a DA ML 是"单载波近最优 DA ML（pilot spacing=4 密集真符号 pilot）"，非 B11 论文 decision-feedback DA ML。复用时注意 pilot 配置口径差异 + DA pilot overhead 1.25dB 总能量代价
6. **sim-preflight v1.3.0 C6-C8 + V1-V6**：公式逐项核对（V1）/ 三方对照（V2+C7）/ 祖师爷警报（V3+C8）/ 参数变更触发算法重审（V4）/ 子 agent 归因独立核查（V5）/ FR-26 读原文数值（V6）
7. **TL-26 参数溯源 + 读原文数值**：每个参数标文献来源 + **读原文具体数值**（D-009 教训 5）
8. **TL-13 共用同一信道**：B2 从 `common/_channel.py` 导入，禁自建
9. **核查机制中性双向**（继承）：子 agent 产出 + 主线独立 grep 核查，只信原始数字不信归因

## 接口变更（如有代码改动）

无（阶段 0 不写代码，只定规约 + 核查探针。核查脚本若写，放 `explore/b2-fade-freeze-pilot-fallback/`，私有 `_` 前缀，不进 experiments/）

## 失败数据附录（如涉及路线失败）

无新增路线失败。**继承 NDA-ML 失败数据**作参照（D-008 vs VV 持平是 bug / D-009 线宽 10kHz 疑似选错 / LMMSE 复现失败公式不全）。

**B2-Q2 潜在失败模式**（未触发但需警惕）：
- 阶段 0.1 验证后核心命题崩塌（pilot-aided 在单载波时域根本打不过盲估）→ B2-Q2 转 Kill
- 阶段 0.4 fair comparison 后 B2-Q2 增量 <0.5dB → FR-21 降级为参考但 D005 会议门槛下可能仍需补范围/鲁棒性维度

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| B2-Q2 真实增量未量化 | INVARIANT 12 | pending MVE | 阶段 3 MVE 产出 |
| sat.1553 +1dB 口径限定 | INVARIANT 12 | 阶段 0.2 核查后限定 | 0.2 |
| B2-Q2 跟 NDA-ML 叙事撞车 | INVARIANT 13 | 阶段 0.4 明确差异化 | 0.4 |
| step4a DA ML 配置口径差异 | INVARIANT 14 | 阶段 0.1 核查 + 0.5 参数对齐 | 0.1 / 0.5 |
| NDA-ML 线宽/方向未定 | step4a-mve-execution 专题 | dormant | 不阻塞 B2，B2 参数选择可参考 NDA-ML 教训 |

## 验证阈值（如涉及验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| 阶段 0.1 张力验证设计 | fair comparison 把 step4a 实测反证分解为配置/触发/类型/场景差异 | INVARIANT 11 | 未跑 |
| 阶段 0.2 dB 溯源核查 | sat.1553 +1dB 限定到原始口径（PE vs VV+diff）| INVARIANT 12 + V6 | 未跑 |
| 阶段 0.3 架构定性 | 前馈化合法不撞 D006 | 继承 INVARIANT | 未跑 |
| sandbox 三方对照 | 双模切换/纯 blind freeze/纯 pilot-aided 三方归因可信 | V2+C7 (v1.3.0) | 未跑 |
| MVE fair gain | ≥0.5dB @ HD-FEC 或范围/鲁棒性维度够格 | D005 + INVARIANT 13 | 未跑 |

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（14 条，重点 11/12/13/14 B2 特殊风险）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] step4a 实测"DA pilot 在 deep fade BER 0.38 vs NDA 0.29"（核查 `.sessions/2026-07-06-step4a-mve-execution/decisions.md:150, 157`）
  - [ ] sat.1553 L440 +1dB 口径=PE vs VV+diff 不是 FOE freeze 增量（核查 `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b1b2b3-verify.md:144-146, 342`）
  - [ ] B2-Q2 不撞 D006（核查 `papers/_read_notes/_B2-deep-fade-freeze-increment.md:68`）
- [ ] 已检查 _registry.yaml 中本专题的 depends_on（4 个依赖：上游 + 切法地图 + 精读沉淀 + step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 下一轮

**对话 2**（阶段 0.1-0.6 完成后）：
- 阶段 1 sandbox 三方对照（双模切换 / 纯 blind freeze / 纯 pilot-aided）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- sandbox 发现双模切换打不过纯 blind freeze → 红线警报（核心命题崩塌，阶段 0.1 没消化清的重验）

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
