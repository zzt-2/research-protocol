# Decisions — B2-Q2 Fade-Freeze + Pilot-Aided Fallback 第三候选

> 专题 `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/` 的决策记录。
> D### 按编号排列，血缘链通过 取代/被取代 字段维护。

## D001: 开 B2-Q2 专题 + 首验证张力策略（阶段 0.1 = step4a 实测反证张力消化，不直接搬 sat.1553 +1dB）

> status: active
> date: 2026-07-08
> 取代：无（开新专题，不推翻 NDA-ML/B7 任何决策）
> 被取代：无
> 依据: Explore agent B2-Q2 详情核查（M-C-A/dB 溯源/切法地图/D006/A1/复用）+ S031 #7 排序（第二档边际够格）+ step4a 实测反证（`step4a-mve-execution/decisions.md:150, 157` DA pilot 在 fade 崩溃）+ 用户原话 voice 2026-07-08（"再开另一个方向"+"B2-Q2"+"开但首验证张力"）
> 触发原话: 用户 "再开另一个方向" + 选"B2-Q2 pilot 在 fade" + 选"开，但首验证张力"

### 决策

**开 B2-Q2 专题，阶段 0 六项规约设计完成，首验证 step4a 实测反证张力。**

1. **阶段 0.1 = 核心命题张力验证设计**（最高优先）：step4a 实测"DA pilot 在 deep fade BER 崩溃（5dB weak 0.38）vs NDA 鲁棒（0.29）"vs B2-Q2 核心命题"pilot-aided fallback 在 fade 比 blind freeze 更优"直接打架。阶段 0.1 设计 fair comparison 消化张力——是 step4a pilot spacing 配置问题还是 pilot-aided 路线根本打不过盲估
2. **阶段 0.2 = dB 溯源核查**：sat.1553 L440 +1dB 口径错位（PE vs VV+diff，不是 FOE freeze 增量），B2-Q2 真实增量未量化，需独立 MVE
3. **不直接搬 sat.1553 +1dB 当 B2-Q2 的 dB**：饱和池 dB 难出区警示 + 口径错位双红旗，B2-Q2 的 dB 必须 MVE 产出
4. **阶段 0 不写代码**：守 profile 第 9 次"急于推进"防线 + INVARIANT 6，六项规约全做完才进 sandbox

### 理由

1. **B2-Q2 不是"稳够格"候选**（主控对话核查结论）：+1dB 口径错位 + step4a 实测反证 + 饱和池小池 + 叙事跟 NDA-ML 撞车，四重风险。但用户选"开，但首验证张力"，遵守用户决策权（profile"Go/Kill 是用户的"）
2. **首验证张力是防线不是拖延**：step4a 实测反证是客观事实（`decisions.md:150, 157` 有原始数字），不消化这个张力直接跑 MVE = 重蹈 NDA-ML D-008 覆辙（vs VV 持平被当合理接受，实际是 bug）。阶段 0.1 设计 fair comparison 把张力变成可验证假设
3. **复用基建完整降低试错成本**：`common/_recovery.py` 4 估计器全有（da_ml/psa_foe/nda_ml/fft_foe），B2-Q2 双模切换只需加 fade 检测门控+模式切换逻辑，基建齐全。即使 B2-Q2 最终 Kill，复用基建的投入也低
4. **跟 NDA-ML 对偶有独立价值**：NDA-ML 是"去 pilot 盲估"，B2-Q2 是"pilot fallback"，两者是 fade 鲁棒性问题的两种解法。B2-Q2 MVE 结果（无论成败）对 NDA-ML 方向决策有交叉验证价值

### 排除的替代方案

- **不开 B2-Q2，换 B3-Q2/B5-Q1**：否决。用户选 B2-Q2，遵守用户决策权。B3-Q2 4 支路迁移风险 + A1 归属未解，B5-Q1 S031 无 A0/D 详评，都不比 B2-Q2 风险低
- **不开新候选，推 NDA-ML/B7**：否决。用户明确"再开另一个方向"，且 NDA-ML 卡 D-008~D-009 方法方向待用户拍板（X/W），B7 阶段 0.2-0.6 已有 H002 交接可独立推进，并行第三个候选不阻塞
- **直接搬 sat.1553 +1dB 跑 MVE**：否决。口径错位（PE vs VV+diff 不是 FOE freeze 增量）+ step4a 实测反证双红旗，直接搬 = 跳阶段 0 重蹈 NDA-ML 覆辙

### 影响范围

- **阶段 0.1 核心命题张力验证设计**：核心动作=设计 fair comparison 把 step4a 实测反证 vs B2-Q2 命题变成可验证假设。输出 `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md`
- **阶段 0.2 dB 溯源核查**：把 sat.1553 L440 +1dB 限定到原始口径（PE vs VV+diff），B2-Q2 增量是独立 MVE 的事
- **跟 NDA-ML 专题的交叉**：B2-Q2 阶段 0.1 的张力验证设计依赖 step4a 实测数据（`decisions.md:150, 157`），不依赖 NDA-ML 后续 D-008 sandbox 结果（D-008 是 vs VV bug，跟 B2-Q2 的 DA vs NDA fade 鲁棒性是不同维度）
- **债务**：B2-Q2 真实增量未量化（pending MVE）；sat.1553 +1dB 口径限定后 B2-Q2 没有现成 dB 锚（需 MVE 产出）

### 教训

1. **主控对话核查暴露关键张力是核心价值**：Explore agent 查 B2-Q2 详情时发现 step4a 实测反证核心命题（DA pilot 在 fade 崩溃 vs NDA 鲁棒），这个张力在 S031 排优先级时没被发现（S031 只排了序没做 A0/D 详评）。**主控对话的角色 = 核查工作对话产出/外部信息后亮出影响方向决策的关键事实**
2. **"pilot 主题跟 NDA-ML 对偶"既是优势也是风险**：对偶意味着复用基建（4 估计器全有），但也意味着叙事撞车（同一个 fade 鲁棒性问题两种解法）。阶段 0.4 必须明确叙事定位（双模切换 vs 纯盲的差异化）
3. **饱和池警示"dB 最难出区"在 B2-Q2 验证**：切法地图 §C 警示饱和池是 dB 最难出区（Paillier/Spalvieri 同构）。B2-Q2 饱和池 §A 小池（3 篇锚无大点），dB 必须 MVE 产出，可能要靠范围或鲁棒性维度够格（D005 会议门槛放宽允许）

### 来源

S001（本轮）+ Explore agent B2-Q2 详情核查 + S031 #7 排序 + step4a 实测反证（`step4a-mve-execution/decisions.md:150, 157`）+ 用户原话 voice 2026-07-08
