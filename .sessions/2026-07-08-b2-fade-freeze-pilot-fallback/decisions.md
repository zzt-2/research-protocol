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

---

## D002: 前馈化降级（从 INVARIANT 撤回）—— 阶段 0.3 过度保守，[79] 式闭环 hold 不撞 D006

> status: active
> date: 2026-07-08（S004 主控对话）
> 取代：**部分取代 S002 阶段 0.3 建议的前馈化 INVARIANT**（前馈化从"INVARIANT 架构约束级"降级为"可推翻的设计选择"）
> 被取代：无
> 依据: V5 主控独立核查 sandbox 失败数据（`_sandbox_results.json` 21 点 A_recover==C_recover 全相同）+ 精读 D006 原文（`2026-06-20-problem-driven-redirection/decisions.md:313-355`）+ 精读阶段 0.3 `_architecture_decision.md` §3.2 + [79] L33（`_B2-deep-fade-freeze-increment.md:33` [79] 闭环 freeze 机制）+ sandbox 物理根因诊断（前馈砍掉环路惯性 → 动态恢复测度失效）
> 触发原话: 用户 "为啥撞 D006？"（对 D006 边界的追问，促使主线精读 D006 原文）

### 决策

**前馈化从 INVARIANT 级降级为可推翻的设计选择**。允许放松到 [79] 式闭环 hold + 功率阈值 gate（不碰 φ_T 建模），严格说不撞 D006。

**D006 边界精读修正**：
- D006 Kill 的精确动作 = "把**湍流相位 φ_T** 主动纳入载波同步算法设计"（无论 KF / 环路 TF / 其他数学工具）
- [79] 式闭环 hold = **功率阈值 gate 估计器更新**（门控用信号功率 P < γ_th，不用相位 φ_T）+ 环路 TF 固定不感知湍流
- → [79] 式闭环 hold **不撞 D006**（门控是功率不是相位，环路 TF 不建模 φ_T）

**撞 D006 的闭环**（D006 真正禁的，仍禁）：
- Q12 式"环路 H(z) 纳入 φ_T"
- B1 式"KF 状态扩维含 φ_T"
- 这些是"把湍流相位当算法状态/参数"

### 理由（为什么降级）

1. **sandbox 实证前馈化的代价**：前馈化（阶段 0.3 INVARIANT）→ 动态恢复测度结构性失效（A_recover==C_recover 21 点全相同）。前馈架构每块独立估计无环路惯性，砍掉了 [79] freeze 的核心机制（环路 hold + 重新收敛动力学）
2. **阶段 0.3 过度保守**：精读 D006 原文发现，D006 Kill 的是"φ_T 纳入算法建模"，不是"任何闭环"。阶段 0.3 把所有闭环都判"撞 D006 风险"是过度保守——[79] 式闭环 hold（功率 gate）不碰 φ_T，不撞 D006
3. **[79] 工程实现就是闭环**：`_B2-deep-fade-freeze-increment.md:33` [79] 原文"FOE tracking 环路在 received power 下降时关闭 tracking（hold 上一估计值）"——[79] 的物理有效性正源于闭环环路惯性。前馈化等于复刻了 [79] 的"关 tracking"但丢了"环路惯性"

### 被排除/否决的

- ❌ **Q12 式"H(z) 纳入 φ_T"闭环**（D006 仍禁）—— 把湍流相位当算法状态，已被旧 B1 + S024 KF 压力测试证伪
- ❌ **B1 式"KF 状态扩维含 φ_T"**（D006 仍禁）—— 同上
- ❌ **继续坚持前馈化 INVARIANT**——sandbox 实证前馈化导致动态恢复测度失效，且 D006 精读修正后前馈化的"绕 D006"论证不再必要

### 影响范围

- **B2-Q2 架构**：允许放松到 [79] 式闭环 hold + 功率阈值 gate。具体闭环机制（完全 hold vs partial hold + pilot 微调）留给 D003 救援路线 + 阶段 1.5 重设计
- **D006 边界**：本 D002 是对 D006 精读的执行层修正，不推翻 D006 本身（D006 Kill 的"φ_T 纳入算法"仍有效）。只是明确了"[79] 式闭环 hold 不在 D006 禁止范围"
- **阶段 0.3 INVARIANT 6（前馈化）**：从"INVARIANT 架构约束级"降级。topic-index 不变量段落需更新

### 不在本轮范围

- ❌ 不在本轮设计闭环 hold 的具体数学（D003 救援路线 + 阶段 1.5 重设计的事）
- ❌ 不推翻 D006（D006 Kill 的"φ_T 建模"仍有效，本 D002 只精读边界）
- ❌ 不改框架文件（D006 在上游专题，本专题不动）

### 来源

S004（主控对话 V5 核查 + D006 精读）+ 用户原话"为啥撞 D006？" + sandbox 物理根因诊断（`_sandbox_results.json` + `_sandbox_three_way.py` freeze_compensate_block L114-121）

---

## D003: 救援路线——放松前馈化到 [79] 式闭环 hold + 加 power-boosted pilot（不 Kill B2-Q2）

> status: active
> date: 2026-07-08（S004 主控对话）
> 取代：无（不取代 D001/D002，是 sandbox 失败后的方向校正——B2-Q2 不 Kill，转救援）
> 被取代：无
> 依据: V5 主线核查 sandbox 三 Go 全 FAIL（动态恢复结构性失效 + 范围扩展无 + 稳态 BER +0.02dB 不够格）+ Kill2 结构性成立（前馈 A≈C）+ D002 前馈化降级（[79] 式闭环 hold 不撞 D006）+ sandbox 物理根因（fade 块 pilot SNR 低 → da_ml 估计噪声大 → C 输 A）+ 文献路线对照（[79] 闭环 freeze + power-boosted pilot 是主流）
> 触发原话: 用户 "啥情况？会不会是代码哪里不对？还是确定物理上不可行?" + "那别人咋弄的？" + "为啥撞 D006？" + 选"放松前馈化 + power-boost（救 B2-Q2）"

### 决策

**不 Kill B2-Q2，转救援路线**：放松前馈化（D002）+ 加 power-boosted pilot，重新走阶段 1.5 重设计。

**救援路线四步**（具体设计留给下一工作对话 + 阶段 1.5）：
1. **阶段 0.3 重定性**：前馈化降级 → [79] 式闭环 hold + 功率阈值 gate（D002 已开绿灯）
2. **阶段 0.4 重审公平对照**：加 power-boost overhead（power-boost 策略：全帧固定 vs 仅 fade 期自适应）
3. **阶段 0.5 加参数**：B2Params 加 power_boost_factor + 闭环环路参数（环路带宽 / hold 机制参数）
4. **重跑 sandbox**：闭环版三方对照（A 闭环 freeze [79] / B 闭环 power-boost pilot 全程 / C 闭环双模）

### 为什么不 Kill（反驳主线初始建议）

主线初始建议 Kill（三 Go 全 FAIL + Kill2 结构性成立）。用户追问"别人咋弄的"+"为啥撞 D006"后，精读发现：
1. **sandbox 没测文献已验证的路线**：[79] 工程实现是闭环 freeze，B2-Q2 sandbox 是前馈 hold；别人用 power-boosted pilot，B2-Q2 sandbox 是等功率 pilot。两个核心机制都没复刻
2. **前馈化是过度保守**（D002）：阶段 0.3 把闭环全判撞 D006 是粗判，[79] 式闭环 hold 严格说不撞 D006
3. **核心物理问题可解**：fade 块 pilot SNR 低 → power-boost 提升 pilot 功率降估计噪声（物理可行，overhead trade-off 需 MVE）

→ 用户选择试文献已验证的路线（主线初始 Kill 建议被推翻，这是 profile"Go/Kill 是用户的"的体现——主线产建议，用户拍板）

### 3 个必须诚实标注的风险

**风险 1：power-boost overhead trade-off（物理可行性核心）**
- power-boost 3dB（pilot 功率 ×2）降估计噪声，但 overhead 从 0.187dB 涨到 0.26-0.64dB（取决于全帧 vs 仅 fade 期）
- trade-off 能否净正需 MVE——**救援路线成败的核心物理问题**

**风险 2：跟 [79] baseline 差异是否够 D005 够格**
- [79] = 闭环 freeze（fade 期完全 hold）。B2-Q2 救援版 = 闭环 hold + fade 期切 power-boosted pilot
- 差异 = "fade 期切 power-boosted pilot" vs "fade 期完全 hold"。sandbox 前馈版测过（C 输 A），闭环+power-boost 能否翻盘未知

**风险 3：跟 sat.1553 L440 口径差异**
- sat.1553 L440 +1dB 是 "pilot PE vs VV+diff"（阶段 0.2 已确认口径错位）
- power-boosted pilot 是**另一个物理机制**（pilot 功率增强），不是 sat.1553 的口径
- B2-Q2 救援版不能引 sat.1553 +1dB 当自己的——增量需独立 MVE

### 被排除/否决的

- ❌ **继续前馈化**（已被 D002 否决）—— 前馈化导致动态恢复测度失效
- ❌ **Kill B2-Q2**（用户选救援）—— 但若阶段 1.5 重设计 sandbox 仍 FAIL，重新评估 Kill

### 影响范围

- **B2-Q2 专题**：转救援路线，不 Kill。阶段 1.5 重设计（修改阶段 0.3/0.4/0.5 + 重跑 sandbox）
- **跟 D005/D006 关系**：救援路线不撞 D006（D002 已确认 [79] 式闭环 hold 合法）。够格标准仍守 D005（赢传统 baseline 几 dB）+ INVARIANT 13（多维够格）
- **跟 NDA-ML/B7 并行**：B2-Q2 救援不阻塞 NDA-ML/B7。B2-Q2 专题 status 保持 active

### 不在本轮范围（防顺手扩）

- ❌ 不在本轮设计闭环 hold 具体数学（阶段 1.5 重设计的事，本轮主控只定方向）
- ❌ 不在本轮跑 power-boost sandbox（重设计后下一工作对话执行）
- ❌ 不在本轮改框架文件（守"先测不改协议"）
- ❌ 不复议 NDA-ML/B7（各自专题的事）

### 来源

S004（主控对话 V5 核查 + D006/阶段 0.3 精读 + 方向定夺）+ 用户原话四段（"啥情况？会不会是代码哪里不对"+"那别人咋弄的"+"为啥撞 D006"+选"放松前馈化+power-boost"）+ sandbox 失败数据（`_sandbox_results.json`）+ D002 前馈化降级

---

## D004 (K001): Kill B2-Q2——闭环版救援 D003 三 Go 全 FAIL + Go1 物理根因证伪（换架构解不了）

> status: **killed**
> date: 2026-07-08（S005 闭环版 sandbox FAIL 后，主控对话 + 用户拍板 Kill）
> 取代：D003（救援路线 active → killed，闭环版 sandbox 全 FAIL 证明救援路线未能翻盘）
> 被取代：无
> 依据: S005 闭环版 sandbox 21 点实测（`_sandbox_closed_loop_results.json`）+ V5 主线独立重算（nR_A==nR_C 全 21 点 + Go3 +0.42dB<0.5dB）+ Go1 物理根因证伪（hold 相位误差 0.0515 rad << π/8=0.39 rad）+ Explore agent 深查（`_sandbox_closed_loop_results.json` 独立 grep 验证）+ 用户原话"Kill B2-Q2"（选项标签）
> 触发原话: 用户 选"Kill B2-Q2"（B2-Q2 救援路线 D003 已跑完且物理根因被证伪，换架构解不了，Kill 还是继续挣扎？）

### 决策

**Kill B2-Q2 专题。D003 救援路线 S005 闭环版 sandbox 三 Go 全 FAIL + Go1 物理根因被证伪，换架构解不了。**

1. **D003 救援路线 killed**：闭环 hold + power-boosted pilot 已在 S005 完整跑完 21 点 sandbox，三 Go 全不够格（Go1 21/21 全等 + Go2 全不可达 HD-FEC + Go3 +0.42dB<0.5dB 阈值）
2. **B2-Q2 专题 status → closed**：Kill 后关闭，不再推进
3. **复用基建保留**：`_closed_loop_freeze.py` + power-boost 框架 + n_recover v2 度量 + 4 维度张力分解框架不删，供其他候选复用

### Kill 理由（硬结论 3 条）

1. **Go1 物理根因证伪是硬结论**：fade 期 hold 相位误差均值 0.0515 rad << 16-APSK 最小相位间隔 π/8=0.39 rad。根因是当前信道模型下 doppler 相位连续慢变，GG 块衰落只影响幅度 h 不影响相位轨迹 → hold 够好 → 无恢复过程。**这不是架构问题（前馈/闭环/power-boost 全试过），是信道模型物理特性，换架构解决不了**
2. **D003 救援已完整执行不是提案**：S005 已跑完 21 点闭环 sandbox，三 Go 全 FAIL。挣扎口子极窄（换信道加相位跳变=改物理偏离真实 / 换测度 Go3 仅 0.4dB / 换调制=反向），无更多文献已验证路线可试
3. **工程成本对比**：Kill 后开新候选（B11-Q2/B3-Q2）成本低于"无方向的二次挣扎"

### B2-Q2 教训对其他候选的价值（保留不浪费）

1. **step4a 实测反证张力分解的 4 维度框架可复用**（pilot 配置/触发条件/pilot-aided 类型/信道场景）
2. **"前馈砍环路惯性导致测度失效"的架构-测度不匹配教训**：前馈化导致动态恢复测度失效（A_recover==C_recover），这个教训对 D006 边界模式 7 Q#（尤其 B11-Q2/B7-Q2 前馈簇）有警示——前馈化可能让某些测度失效
3. **复用基建保留**：`_closed_loop_freeze.py` + power-boost 框架 + n_recover v2 度量，供 B11-Q2（NDA-ML 湍流验证）/ B7-Q2（Gardner TED 湍流鲁棒性）复用
4. **INVARIANT 13 饱和池警示在 B3-Q2/B5-Q1 同样适用**：B2 饱和池小池 dB 难出区，B3/B5 也是饱和池

### 排除的挣扎方向（诚实标注）

- ❌ **换信道加相位跳变**：偏离物理真实（当前信道模型 doppler 相位连续慢变是物理事实，强加相位跳变是造问题）
- ❌ **换测度（Go3 仅 0.4dB）**：量级不够 D005"赢几 dB" + INVARIANT 13 饱和池警示
- ❌ **换调制格式**：反向（B2-Q2 命题在 16-APSK 成立，换格式是放弃命题）

### 影响范围

- **B2-Q2 专题**：status → closed，不再推进。S005 是最后一个 session note
- **D003 救援路线**：killed（被 D004/K001 取代）
- **复用基建**：保留在 `projects/simulation/explore/b2-fade-freeze-pilot-fallback/`，不删
- **接替候选**：B11-Q2 NDA-ML 湍流验证（D006 边界模式 7 Q# 之一，subagent 主推）

### 教训

1. **主控对话状态认知滞后会延误 Kill**：主控对话（本对话）在用户问"要不 kill"时以为 D003 是提案阶段，实际 S005 已跑完闭环 sandbox 全 FAIL。Explore agent 深查才暴露真实状态。**主控对话必须持续核查工作对话产出，不能只靠上下文记忆**
2. **Go1 物理根因证伪是 Kill 的硬依据**：不是"三 Go 全 FAIL"就 Kill（那是量级不够），是"Go1 物理根因被证伪"（换架构解不了）才 Kill。**Kill 判据要查物理前提（TL-22 震撼结果先查物理前提的反向应用：失败结果也查物理前提）**
3. **用户推翻主线 Kill 建议后试了救援也 FAIL，最终仍 Kill**：D003 救援是用户决策权的体现（profile"Go/Kill 是用户的"），但物理硬结论不因用户决策而改变。主线产建议 + 用户拍板 + 物理事实，三者独立

### 来源

S005（闭环版 sandbox 救援路线执行）+ H005（交主控定夺 Kill）+ Explore agent 深查（`_sandbox_closed_loop_results.json` 独立 grep 验证 nR_A==nR_C 21/21 全等 + Go1 物理根因证伪）+ 用户原话"Kill B2-Q2"
