# [S001] 专题开题 + 材料盘点 + 数据稳定性验证 + 论点合理性审查

> 2026-07-09 | 阶段：写作准备（GW Step 4a 维度 D 内） | 状态：进行中
> 来源：从 step4a-mve-execution 专题分出，承接 H008 + R001 调研

## 目标

开写作专题，回答用户四个问题：
1. 把目前我们有的材料列出来，确保都是最新的
2. 想想我们还缺啥
3. 我们的数据是否稳定
4. 我们的论点是否合理

## 记录

### 一、材料盘点（projects/simulation/）

**简报演进链**（4 版，清晰）：
```
7-06 初版（乐观，NDA-ML 赢 BPS/持平 VV）→ 7-08 v2 update（诚实推翻"持平"，核查发现 VV 调参反超）→ 7-08 v3 turbulence_pivot（算法层死路→湍流差异化 pivot）→ 7-09 adaptive_cpr（A4 per-block 切换，当前主线）
```

**可直接复用核心文件（6 个，排序）**：
1. `ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md` 🟢 当前主线底稿
2. `ADVISOR_BRIEFING_2026-07-08_v3_turbulence_pivot.md` 🟡 湍流论证物理前置（related work 复用）
3. `COMPARISON_REFS.md` 🟡 对比文献档级表（需补 A4 文献）
4. `baseline_report.md` 🟡 仿真器 bit-exact 正确性（methods 复用）
5. `REVIEW_NOTES.md` 🟡 老师意见回应（需更新 TODO）
6. `ADVISOR_BRIEFING_2026-07-08_update.md` 🟡 "算法层无增量"诚实声明（limitation 复用）

**⚠️ 警惕风险点**：`SPEC.md`（5-31）自称"唯一真相源"但写 QPSK，与实际 (8,8)-16APSK 直接矛盾。写作绝不可引。真正参数真相源 = params.py（落地状态待核）。

**应归档（4 个）**：SPEC.md / README.md / CAPABILITY_AUDIT.md / ADVISOR_BRIEFING.md(7-06)。不删，归档作历史。

### 二、缺口识别

| 类别 | 缺口 | 紧急度 | 触发 |
|------|------|--------|------|
| 图 | `_adaptation_scan_figures.png` 是 5seed 旧图（脚本 L26/L120 读 `_main_experiment_5seed.json`，标题写"5 seed"），与简报 30seed 正文不符 | 🔴 阻塞发简报 | 重绘 |
| 数据 | A4 敏感性 4 个非基准配置（11/13/15dB + margin 1.05/1.15）仍 3seed（`_a4_improved_cv_results.json`）| 🟡 | 写论文前补 30seed |
| 数据 | `sc_nda_ml_dd_kf_ablation_improved/` 目录为空 | 🟡 | 简报若引用需核实来源 |
| 文献 | COMPARISON_REFS.md 未含 A4/per-block 切换文献 | 🟡 | 写作时补 |
| 文档 | SPEC.md 过时，params.py 落地状态待核 | 🟡 | 写方法章前核 |
| 叙述 | Barbosa 2020 JLT 全文未获取（IEEE 付费墙）| 🟢 低 | abstract 够用 |

### 三、数据稳定性验证

**主实验 30seed**（`_fair_gain_summary_30seed.json`，df=29）🟢 稳定：
| 场景 | gain_mean | CI95 | CI宽 | n_valid |
|------|-----------|------|-----|---------|
| awgn | +1.339 | [1.327,1.352] | 0.025 | 30/30 |
| weak | +1.428 | [1.351,1.505] | 0.154 | 30/30 |
| moderate | +1.439 | [1.283,1.596] | 0.313 | **17/30** |
| strong | +2.509(工作区) | [2.415,2.603] | — | HD-FEC不可达 |
| up_mod | +2.443(工作区) | [2.343,2.543] | — | 同上 |
| up_str | +3.101(工作区) | [2.989,2.214] | — | 同上 |

- weak/moderate CI 重叠（统计不可分）—— 已诚实标注"两段趋势"
- moderate n_valid=17/30：其余 13 seed HD-FEC 点物理不可达（非数据丢失），处理诚实

**A4 切换 30seed**（`_a4_switch_30seed.json`，γd=15dB crossover）🟢 稳定：
| 场景@15dB | switch_vs_max | CI95 | 下界>0 |
|-----------|--------------|------|--------|
| weak | +0.274 | [+0.186,+0.363] | ✅ |
| moderate | +0.481 | [+0.414,+0.547] | ✅ |
| strong | +0.402 | [+0.355,+0.449] | ✅ |

- 低 SNR 不可工作区诚实标注输了（weak 5dB [-0.170,-0.143]，CI 上界仍负）
- 非 crossover 高 SNR 区持平（CI 跨 0），正确

**5seed vs 30seed 一致性** 🟢：
- 主实验无反转，30seed CI 大幅收窄（weak CI 宽 0.50→0.18）
- moderate 30seed 下调（5seed 1.71→30seed 1.44，5seed 异常高值被稀释），与 CI 重叠结论一致
- A4 切换 30seed mean 落在 5seed CI 内，无反转

**结论：数据稳定，可支撑简报。** 唯一阻塞发简报 = 图（5seed 旧图，债务③）。

### 四、论点合理性审查

简报 §1-§5 四条核心论点链：

| 论点 | 合理性 | 风险/注意 |
|------|--------|----------|
| §2 NDA 优势随湍流递增（fair_gain 链 +1.34→+3.10）| ✅ 合理 | 叙事严格说"两段"（弱~1.4→强~2.5-3.1）非六档单调（CI 已诚实标注）|
| §3 crossover 由 per-block γ_eff 驱动（汇聚 12~14dB）| ✅ **最强环节** | 物理因果（低有效 SNR 导频可靠/高有效 SNR 积分鲁棒+省开销）+ 诊断实证双支撑 |
| §4 切换赢 max(DA,NDA)（+0.27~0.48dB）| ✅ 合理但偏薄 | 增益幅度小，靠 fair_gain 架构红利（+1.34~3.10）+ A4 切换双叙事撑 |
| §5 单载波 CPR per-block 硬切换没人做过 | ✅ 合理 | ⚠️ **需复核**：Barbosa 2020 JLT 做"SNR 切换 BPS 开关"（光纤 PAS），结构同构（切换对象不同）。简报 §5 把它归"算法内自适应参数"可能过轻——Barbosa 是跨阶段切换（pilot stage + BPS stage 开关），不只是"单算法内调参" |

**待用户判断的张力点**：论点 4 的 Barbosa 归类。两个选项：
- (a) 维持简报现状（Barbosa 归"算法内自适应参数"）—— 但严格说不准确，Barbosa 是按 SNR 切换 BPS 第二阶段开关，跟 A4 切换 DA/NDA 结构同构（都是跨算法组件的条件切换），只是切换对象 + 触发条件不同
- (b) 修正简报 §5——把 Barbosa 单独列一类"跨阶段/组件条件切换"，强调 A4 区别在"切换对象是两个完整算法（DA/NDA）+ 触发量是 per-block 有效 SNR（物理量）而非系统 SNR（标量）"

## 决策引用

- 无决策（本轮是盘点+审查，不涉及方向/架构决策。论点 4 Barbosa 归类的修正待用户定，可能记 D001）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（材料盘点+缺口+数据验证+论点审查都是写作准备，不跑新实验，不跳框架）

## 后续

本轮后续工作已迁出到 R002/R003/H001，这里记录原 S001 的后续项当前状态：

1. ~~阻塞发简报：重绘 `_adaptation_scan_figures.png`（5seed→30seed）~~ → **已迁入 H001**（新对话做，且范围扩大为整套图表设计）
2. **待用户判断**：论点 4 Barbosa 归类（维持 vs 修正简报 §5）→ 仍悬置，新对话重构简报时定
3. **写论文前补**：A4 敏感性 4 配置补 30seed（债务②）→ R003 确认切换增益是天花板，此项优先级降低
4. **写作前核**：params.py 落地状态（SPEC.md 过时的替代真相源）→ 仍待核
5. **可选**：归档过时文件（SPEC/README/CAPABILITY_AUDIT/7-06简报）→ 仍可选

**R002/R003 衍生的新后续**（见各 R 文件"对决策的影响"）：
- R003 §B 拆账后：简报叙事需重构（主卖点改去导频真实增益 +1.2dB，切换降级）
- R002 §C：30seed+CI 用"湍流随机性"正当化，不当主卖点
- H001：图表设计 + 参数呈现策略（新对话执行）
