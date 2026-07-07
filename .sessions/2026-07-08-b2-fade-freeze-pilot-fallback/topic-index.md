# Topic Index: B2-Q2 Fade-Freeze + Pilot-Aided Fallback 双模切换第三候选

> slug: 2026-07-08-b2-fade-freeze-pilot-fallback
> status: active | created 2026-07-08 | last_updated 2026-07-08（S002 阶段 0.1-0.2 完成——张力验证设计 4 维度分解 + dB 溯源限定，H002 交接）

## 专题定位（一句话）

B2-Q2（fade-freeze + pilot-aided fallback 双模切换）第三候选 MVE 执行。与 NDA-ML 单载波候选（step4a-mve-execution，dormant）+ B7 Gardner TED（b7-gardner-ted-foe，active）并行。**首要张力**：step4a 实测反证 B2-Q2 核心命题（DA pilot 在 fade 崩溃 vs NDA 鲁棒），开专题首验证此张力（不能直接搬 sat.1553 L440 +1dB）。**流程规划前置**（阶段 0 不写代码先定规约）防重蹈 NDA-ML 6 类混乱。

## 原始目标（冻结，不可修改）

对 B2-Q2 走 Step 4a 维度 D MVE，守 FR-21/TL-20/FR-18/FR-12 + D005 务实路线 + D006 红线 + **sim-preflight v1.3.0**（C6-C8 公式核对/三方对照/祖师爷警报 + V1-V6）。

**冻结边界**：
- 只做 B2-Q2（fade-freeze + pilot-aided fallback 双模切换），不回头救 6 次 Kill
- 不跳框架（FR-22，当前在 Step 4a 维度 D）
- 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- 不改框架文件（守"先测不改协议"）

## 范围边界

### 原始目标（冻结）
对 B2-Q2 走 Step 4a 维度 D MVE。

### 当前范围
- **阶段 0 前置规约**（不写代码，先定 6 项规约，防 NDA-ML 6 类混乱）：
  0.1 **核心命题张力验证设计**（step4a 实测反证 vs sat.1553 +1dB，怎么设计 fair comparison 消化这个张力）—— B2-Q2 最高优先项
  0.2 dB 溯源核查（sat.1553 L440 +1dB 口径错位：是 PE vs VV+diff 不是 FOE freeze 增量）
  0.3 架构定性（双模切换的前馈化 vs 环路，前馈不撞 D006）
  0.4 公平对照框架设计（blind freeze vs pilot fallback，fair gain 怎么定义，工作点 BER 还是 HD-FEC）
  0.5 参数真相源前置（Doppler / OSNR / 符号率 / 线宽 / fade 参数 σp² 一开始进 params.py 单字段）
  0.6 文件组织规约（`explore/b2-fade-freeze-pilot-fallback/` 目录结构 + 命名规则）
- **阶段 1 sandbox 三方对照**（双模切换 / 纯 blind freeze / 纯 pilot-aided）
- **阶段 2 TL-20 理论预期表**（仿 N1-MVE-SPEC.md §2）
- **阶段 3 MVE + consistency**（守 sim-preflight v1.3.0 C6-C8 + V1-V6）

### 明确不含
- ❌ 不回头救 6 次 Kill
- ❌ 不判 NDA-ML/B7 那边的方向决策（那是各自专题的事）
- ❌ 不改框架文件
- ❌ 不跳框架（FR-22，当前在 Step 4a 维度 D）
- ❌ 不推翻 D006（前馈不撞 / 环路 TF 联合建模则撞）
- ❌ 不污染 common（explore 阶段探针不直接进 experiments，MVE 通过才转正）

### 范围变更记录
- 无（专题首 session）

## 不变量（动任何一条必须重新讨论）

1. **继承上游专题 `2026-06-20-problem-driven-redirection` 全 9 条不变量**（D017/D018 判读框架 / D006 红线 / D005 务实路线最高优先级 / 范围硬门 / 问题从文献长出来 / 委托技术判断守 Go/Kill / 3 步上限 / 核查机制中性双向 / GW 流程强制门控）
2. **D005 务实路线（INVARIANT 最高优先级）**：Go 判据=赢传统未优化 baseline 几 dB（会议门槛放宽：纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格）；oracle 上界 FR-21 降级为参考不当 Kill 门
3. **FR-22 GW 流程强制门控**：当前在 Step 4a 维度 D（MVE），禁跳到 Contract/Execute
4. **FR-25 Go/Kill 标准分离**：Go 标准=赢传统 baseline / Kill 标准=A0 致命+MVE FAIL，FR-21 只在 A0 通过后做 Kill 工具
5. **切法地图是参照系不是答案**：B2-Q2 是饱和池 §A 小池（sat.1553+Matsuda+Paillier 3 篇锚，无超级大点反复切），引用模式不搬"切法地图说这个好"
6. **profile 第 9 次"急于推进"防线激活**：B2 流程规划阶段主线极易"阶段 0 太繁琐先跑起来再说"。**防线：阶段 0 六项规约必须全做完才进 sandbox，禁跳阶段 0 直接写代码**（NDA-ML 最大混乱就是阶段 0 没做）
7. **TL-26 参数溯源强制**：B2 每个关键参数（fade σp² / OSNR / 符号率 / 线宽 / pilot 配置）必须标文献来源（sat.1553 / Matsuda / Paillier），禁拍参数。**且必须读原文数值不只引位置**（D-009 教训 5，FR-26 强化）
8. **TL-13 共用同一信道实现**：B2 必须从 `common/_channel.py` 导入，禁自建信道
9. **TL-20 先建理论预期**：MVE 跑之前必须写明理论预期表，仿 N1-MVE-SPEC.md §2
10. **核查机制中性双向**：子 agent 产出 + 主线独立 grep 核查，**子 agent 归因必须主线独立重算验证**（D-009 教训 6，只信原始数字不信归因）
11. **【B2 特殊·INVARIANT】核心命题张力首验证（vs step4a 实测反证）**：step4a 实测"DA pilot 在 deep fade BER 崩溃（5dB weak 0.38）vs NDA 全帧积分鲁棒（0.29）"（`step4a-mve-execution/decisions.md:150, 157`）。B2-Q2 核心命题是"pilot-aided fallback 在 fade 比 blind freeze 更优"。**这两个结论在单载波时域下直接打架**。**阶段 0.1 必须设计 fair comparison 消化这个张力**——是 step4a 实测的 pilot spacing 配置问题（spacing=4 在 fade 不够密）还是 pilot-aided 路线在单载波时域根本打不过盲估？不能直接搬 sat.1553 L440 +1dB（sat.1553 是 OFDM scenario 4 PE vs VV+diff，不是 FOE freeze 双模切换增量）
12. **【B2 特殊·INVARIANT】dB 溯源口径错位前置核查**：sat.1553 L440 "+1dB pilot 在 fade" 实际口径是 **pilot-aided 相位估计 vs VV+差分编码**（`_cut-b1b2b3-verify.md:144-146, 342`），**不是 pilot-aided FOE vs blind FOE freeze 的增量**。B2-Q2 真实增量未量化，需 MVE。**阶段 0.2 必须把 sat.1553 的 +1dB 限定到原始口径，B2-Q2 的增量是独立 MVE 的事**
13. **【B2 特殊·INVARIANT】饱和池 dB 难出区警示**：切法地图 §C 警示"Paillier 安全区恰恰是 dB 最难出区"（Spalvieri 85 同构）。B2 饱和池 §A（B1/B2/B3/B4/B5），dB 形态="无 dB 仅结构性"（sat.1553 自己未对 [79] 冻结机制做独立仿真复现，仅引为设计建议）。**B2-Q2 的 dB 必须独立 MVE 产出**，不能引 sat.1553 L440 +1dB 当自己的（口径错位 + 饱和池警示双红旗）
14. **【B2 特殊·INVARIANT】复用基建边界（NDA-ML 对偶）**：`common/_recovery.py` 已有 4 估计器（da_ml/psa_foe/nda_ml/fft_foe），B2-Q2 双模切换 = (fft_foe/nda_ml + 功率阈值 gating) ↔ (da_ml/psa_foe) 模式切换。**复用风险**：step4a DA ML 是"单载波近最优 DA ML（pilot spacing=4 密集真符号 pilot）"，非 B11 论文 decision-feedback DA ML。B2-Q2 复用时需注意 pilot 配置口径差异 + DA pilot overhead 1.25dB 总能量代价已在公平对照框架中制度化（`decisions.md:142, 155`）

## 其他结论（普通技术决策）

### B2 特殊风险（vs NDA-ML/B7 的差异点，决定流程重点）

| 风险 | B2-Q2 情况 | NDA-ML 对照 | B7 对照 | 流程对策 |
|---|---|---|---|---|
| 核心命题被反证 | step4a 实测 DA pilot 在 fade 崩溃 | D-008 vs VV 持平是 bug | (无) | **阶段 0.1 首验证张力**（最高优先）|
| dB 口径错位 | sat.1553 +1dB 是 PE vs VV+diff | +2dB B11 原文实证 | 0.6dB OFC 原文 | 阶段 0.2 dB 溯源核查 |
| 饱和池 dB 难出 | 小池 3 篇无大点 | 稀池独占 | 稀池独占 | 阶段 0.4 公平对照框架 + TL-20 理论预期 |
| 叙事撞车 | fade 鲁棒性跟 NDA-ML 命题撞 | (本身) | (无关) | 阶段 0.4 明确叙事定位（双模切换 vs 纯盲）|
| A1 归属 | 双模切换算法创新（非场景迁移）| ML 加权算法薄 | 场景迁移 | A1 风险低（优于 NDA-ML/B7）|

### NDA-ML 6 类混乱 + B2 防御措施（继承 B7 框架）

| 混乱类 | NDA-ML 教训 | B2 防御措施 |
|---|---|---|
| A. 参数反复 | 线宽 500kHz→10kHz→疑似 0.1-1MHz，全量重跑 3 轮 | 阶段 0.5 参数真相源前置 + sim-preflight v1.2.0 param-source.md |
| B. 算法 bug | D003 双 bug + D-008 双 bug（漏 ML 加权+升幂未归一）| 阶段 0.2 dB 溯源核查 + V1 公式逐项核对（v1.3.0）|
| C. 验证失效 | consistency PASS 但算法错（两套都漏同一 bug）| V2 三方对照 + V3 祖师爷警报（v1.3.0 C7-C8）|
| D. 方向重定位 | B11 OFDM→单载波 / LMMSE 失败→VV/BPS | 阶段 0.3 架构定性前置（前馈 vs 环路）|
| E. 文件混乱 | MVE 薄包装 + 双套参数共存 + 两 results 目录 | 阶段 0.6 文件组织规约 + 下游引用同步清单 |
| F. 文献引用 | D-007 引 Valjus 位置没读原文数值 | V6 FR-26 读原文数值（v1.3.0）|

## 已确认决策

- **D001**（2026-07-08，S001）：开 B2-Q2 专题 + 首验证张力策略（阶段 0.1 = step4a 实测反证 vs sat.1553 +1dB 张力消化设计，不直接搬 +1dB）

## 悬而未决

1. ~~step4a 实测反证怎么消化~~ ✅ **S002 阶段 0.1 已消化**：张力可分解为 4 维度（A pilot 配置 / B 触发条件 / C pilot-aided 类型 / D 信道场景）。**核心发现**：step4a 测的是稳态 BER，B2-Q2 增量在动态恢复时间（不同测度）。**维度 C2 红线风险**：所有 pilot-aided 变体在 fade 是否都输 NDA-ML，sandbox 阶段 1 必答
2. ~~sat.1553 +1dB 口径限定~~ ✅ **S002 阶段 0.2 已限定**：+1dB = pilot PE vs VV+diff @ QPSK+AWGN PN scenario 4。五重口径差异（对比方法/估计对象/调制/场景/测度）→ B2-Q2 不能搬。B2-Q2 增量来源：fade 恢复时间 / 稳态 BER / 工作区扩展，必须 MVE 产出。**意外发现**：sat.1553 L440 [58] "pilot+盲组合 open direction" 是 B2-Q2 叙事锚点
3. **架构定性**：阶段 0.3 双模切换的前馈化（合法不撞 D006）vs 环路（撞 D006）。盲侧 fft_foe 是前馈，但 pilot 侧 da_ml 在 step4a 是前馈闭式，整体双模切换可前馈化（fade 检测门控+模式切换不纳入环路 TF）
4. **公平对照框架**：阶段 0.4 设计（baseline = 纯 blind freeze [79]；fair gain 双测度 = 稳态 BER + 动态恢复时间；pilot overhead 摊薄 = fade 占空比 × 25%；叙事用 sat.1553 [58] 锚）。S002 阶段 0.1 已给框架输入，0.4 制度化
5. **饱和池 dB 难出区对策**：阶段 0.4 + TL-20（B2-Q2 增量可能靠范围维度——strong 湍流纯 blind HD-FEC 不可达，双模切换可能可达）

## 当前位置

**🟡 S002 阶段 0.1-0.2 完成（2026-07-08）**：张力验证设计 + dB 溯源核查完成，两份产出落盘（`_tension_validation_design.md` + `_db_sourcing_audit.md`）。核心结论：张力可分解不直接 Kill，B2-Q2 增量在动态恢复时间维度，维度 C2 红线风险 sandbox 必答。下一步=新对话（工作对话）执行阶段 0.3-0.6（H002 交接）。

## 进展线索

- **S001** 开题 + NDA-ML 实测反证诊断 + B2 特殊风险 + 阶段 0 六项规约设计 + 复用基建清单（2026-07-08，主控对话）
- **S002** 阶段 0.1 张力验证设计（4 维度分解 + fair comparison 框架）+ 阶段 0.2 dB 溯源核查（sat.1553 +1dB 口径限定 + 叙事锚点 [58] 发现）。产出 3 文件：`_step4a_detail_extract.md`（子 agent）+ `_tension_validation_design.md` + `_db_sourcing_audit.md`。H002 交下一对话执行 0.3-0.6（2026-07-08，工作对话）
