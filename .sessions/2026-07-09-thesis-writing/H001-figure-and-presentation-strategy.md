# Handoff: 自适应 CPR 论文的图表设计 + 参数呈现策略

> 来源: S001 + R002 + R003 | 交接目标: 新对话讨论"怎么画图、怎么组织坐标轴、选哪些参数维度展示，让真实优势（强湍流 deep fade）被看清楚"
> 文件名: H001-figure-and-presentation-strategy.md
> 日期: 2026-07-09

## 到哪了（状态）

写作专题（2026-07-09-thesis-writing）已完成四件事，结论都已落盘：

1. **S001 材料盘点 + 数据稳定性 + 论点审查**：数据 🟢 稳定（30seed CI 全正）；论点 4 条合理（crossover 物理性最强）；唯一阻塞发简报 = 图是 5seed 旧图
2. **R002 叙事流程分析**（含 §B/§C 修正）：会议/期刊论文是"机制+数字闭环"，不是纯机制（那是学位论文体例）；不报 CI 是领域惯例；切换型抓"跨工况可移植"framing
3. **R003 天花板判断 + 主卖点重排 + §B 拆账**：切换增益 0.27-0.48dB 是物理天花板（调参救不了）；**fair_gain 拆账后强湍流真实增益 +1.2-1.8dB（去导频开销），归因干净（deep fade 击穿导频）**

**核心定位已锁定（"短跑赛道"，呼应老师"特长场景"标准）**：
> 星地强湍流下，盲（全块积分）类载波恢复比导频辅助类有 +1.2-1.8dB 真实增益，机制是 deep fade 击穿短导频。AWGN/弱湍流承认无真实增益（不是全能冠军）。

**当前简报问题**：叙事重心错（切换当主卖点，该改成 fair_gain）；图是 5seed 旧图（`_adaptation_scan_figures.png` 读 `_main_experiment_5seed.json`）；6 场景平铺稀释了强湍流亮点。

## 下一步干什么（新对话核心任务）

**设计图表方案 + 参数呈现策略**，让真实优势（强湍流 deep fade 的 +1.2-1.8dB）被看清楚。这是**呈现策略不是 p-hacking**——用已有真实数据，组织坐标轴/场景/维度，突出物理故事。

### 关键确认的边界（守诚信红线）

- ✅ 合法：展示已有数据的不同维度（线宽扫描/场景递增/去导频拆账）；补新湍流档位扩覆盖度（回 step4a 跑，诚实标新数据）
- ❌ 红线：搜参数空间找最好看组合只报那个（cherry-picking，R003 §A 已讨论，用户认同"极端的不该挑"）
- ❌ 红线：用含 1.25dB 导频红利的 +2.5dB 当标题数字（易被一票否决"大半省导频"）→ 用 +1.2dB（去导频）

### 图表设计初步建议（新对话展开细化）

**图 1（主图）：fair_gain vs 湍流强度递增曲线**
- 横轴：湍流场景（建议用 σ²R 物理量，或下行 4 档 AWGN/weak/mod/strong）
- 纵轴：fair_gain (dB)
- **两条线**：总 fair_gain（+1.34→3.10）+ 去导频真实增益（+0.09→1.85），让读者一眼看到"去导频后强湍流仍 1.2-1.8dB"
- 误差棒 30seed 95% CI

**图 2（机制证据）：DA vs NDA BER 曲线分场景**
- 2-3 子图（AWGN/moderate/strong），每图 DA/NDA/oracle 三线
- strong 子图是亮点：DA 退化（floor/斜率缓）vs NDA 贴近 oracle = deep fade 击穿视觉化

**图 3（物理单调性，加分）：线宽扫描**
- 横轴线宽 log 刻度（10/50/100/500kHz），纵轴 fair_gain
- 物理故事：当前 10kHz 是合理工作点不是挑的

### 用户明确的执行偏好（新对话必须考虑）

- **要补很多点，当前太稀疏**——用户明确要求
- **5seed 够了，30 太慢**——用户偏好 5seed 补点
- **权衡提醒（新对话要跟用户讨论）**：R003 拆账硬数字靠 30seed+CI 撑底气；5seed 补点 CI 宽（weak/moderate 5seed CI 宽 0.15-0.31dB），主图若 5seed 补密，审稿人可能质疑"趋势不显著"
- **折中思路**：主图（fair_gain vs 湍流）保持 30seed 不补密（6 点够），辅助图（BER 轮廓）用 5seed 补密——主卖点 CI 窄、辅助图点密

## 纪律（和下一步直接相关）

1. **守诚信红线**（R003 §A）：不 cherry-pick 参数；参数选择必须有物理/文献依据；不冲数字
2. **标题数字用去导频的 +1.2dB**，不用含水分的 +2.5dB（R003 §B）
3. **不报 CI 是领域惯例**（R002 §C）：30seed+CI 不当主卖点，用"湍流随机性需多 seed 表征分布"正当化
4. **诚实标注**（加分项）：NDA vs VV/BPS 强湍流有 0.11dB 泄漏（R003 §B）；AWGN/弱湍流无真实增益承认；weak/moderate CI 重叠
5. **不跳框架（FR-22）**：补新仿真要回 step4a-mve-execution 专题，不在写作专题跑
6. **叙事定位锁定**：主卖点 = 强湍流 deep fade 真实增益（盲类 vs 导频类），切换/crossover 是支撑

## 必读（新对话开始时按优先级读）

1. `.sessions/2026-07-09-thesis-writing/R003-gain-ceiling-and-selling-point-priority.md`（含 §B 拆账）—— 主卖点定位 + 拆账硬数字 + 标题数字纪律
2. `.sessions/2026-07-09-thesis-writing/R002-narrative-flow-analysis-guo-zhang.md`（含 §B/§C）—— 叙事惯例 + 图表惯例（期刊机制+数字闭环）
3. `.sessions/2026-07-09-thesis-writing/S001-material-inventory-data-stability-argument-audit.md` —— 数据文件位置 + 稳定性
4. `.sessions/2026-07-09-thesis-writing/topic-index.md` —— 不变量 + 当前位置
5. `projects/simulation/ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md` —— 当前简报（叙事要重构的底稿）

## 关键数据文件位置（画图直接用）

- 主实验 30seed：`results/sc_nda_ml_main_30seed/_main_experiment_30seed.json` + `_fair_gain_summary_30seed.json`（pilot_overhead=1.2494）
- 主实验 5seed：`results/sc_nda_ml_main/_main_experiment_5seed.json`（补点快）
- 线宽扫描：`results/sc_nda_ml_linewidth_sweep/_linewidth_sweep_summary.json`（10/50/100/500kHz × 4 场景，5seed）
- 上行场景：`results/sc_nda_ml_uplink/_uplink_summary.json`
- A4 切换 30seed：`explore/nda-awgn-tracking-sandbox/_a4_switch_30seed.json`
- VV/BPS ablation（拆账对照）：`results/sc_nda_ml_vv_ablation_improved/` + `sc_nda_ml_bps_ablation_improved/`
- 当前 5seed 旧图（要重画）：`explore/nda-awgn-tracking-sandbox/_adaptation_scan_figures.png` + 生成脚本 `_plot_adaptation_figures.py`

## 接口变更（如有代码改动）

无（本轮全是分析+文档）。新对话画图会改/建 plotting 脚本。

## 已知债务（和画图直接相关）

| 债务 | 原则 | 当前状态 | 触发解决 |
|------|------|---------|---------|
| 简报图是 5seed 旧图 | 数据已 30seed | `_adaptation_scan_figures.png` 读 5seed | 新对话重画（本 handoff 任务）|
| fair_gain 主图场景平铺稀释亮点 | 突出递增趋势 | 6 场景无区分 | 新对话重组坐标轴 |
| 标题数字含导频水分 | 诚信+硬度 | 简报用 +2.5dB | 改用 +1.2dB（去导频）|

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（尤其 R003 主卖点定位 + 诚信红线）
- [ ] 已验证至少 3 条关键事实声称：
  - 强湍流 fair_gain 拆账后 +1.26dB（减 1.25 导频）→ 查 `_fair_gain_summary_30seed.json`
  - DA/oracle 强湍流 1.62× vs NDA/oracle 1.19×（deep fade 证据）→ 查 `_main_experiment_30seed.json`
  - 线宽扫描 10kHz 最优、500kHz 崩溃 → 查 `_linewidth_sweep_summary.json`
- [ ] 已检查 _registry.yaml 中本专题 depends_on（step4a-mve-execution）
- [ ] 已确认当前范围未违反"明确不含"（画图是写作准备；补新仿真回 step4a）

## 下一轮

**任务**：基于已有真实数据，设计图表方案 + 参数呈现策略，让强湍流 deep fade 真实优势被看清楚。

**具体步骤**：
1. 确定主图/机制图/加分图的最终组合 + 坐标轴设计
2. 讨论"补点密度 vs CI 宽度"权衡（用户要补密 + 5seed 够，但主图 CI 要窄）→ 定哪些图 30seed 哪些 5seed
3. 如需补新湍流档位：明确这是回 step4a 跑新实验，定档位数 + seed 数
4. 重画图（改 `_plot_adaptation_figures.py` 或新建脚本）
5. 按新图 + R003 定位重构简报叙事（切换降级、fair_gain 去导频主卖点上位）

**工具**：python + matplotlib（画图）；数据文件见上节
