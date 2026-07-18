# [S028] 载波同步 D015 v2（D017）判读层 B1-B3 综述背书子环节

> 2026-07-02 | 块 E Step 4a 载波同步 v2 | 状态：判读层 B1-B3 完成，交接下对话继续
> 来源：续接 H017（判读层 B 档剩余 8 个，本轮选 B1-B3 综述背书 3 点）

## 目标

执行 H017"下一步"：选 B1-B3 综述背书 3 点精读（sat.1553 已落盘有笔记，复用快，1 子环节 3 篇，守 3 步上限），守 D017 v2 判读层流程 + D009 checklist + C3 换皮核查。

## 记录

### 阶段 1：报到 + H017 接收验证（Trigger 1+5）

报到读：topic-index（不变量 8 条，D005 务实路线最高优先级）+ S027 + R004 + voice.md（2026-07-02 段 2 条纠偏）+ D017/D006/D005（decisions.md）+ profile.md。

**H017 接收方验证清单全过**（6 项核查全 PASS）：
- R004 全景表 A=0/B=12/C=4/D=7 类：PASS（读 R004 全文一致）
- S027 判读层第一批 B4/B6 A3 FAIL / B5/B7 下载失败：PASS
- D017 v2 判读层流程：PASS（decisions.md L1104-1220 两层结构+红线 6/7+cited-by 预案段全在）
- topic-index 不变量 D005 务实路线最高优先级：PASS
- _registry depends_on/conflicts_with：PASS
- 范围未违反"明确不含"：PASS

**Inflation check**：S### = 22（≥15 阈值）。但本轮是 D017 既定的载波同步 v2 判读层延续（H017 明确"下一步判 B1-B3"），非范围扩张，如实标注不阻断。

**Profile 感应**：voice.md 2026-07-02 段 2 条纠偏（单对话步数 + 样本不足外推）已在 profile.md 第 5 次验证条目反映。本轮守：①严格守 3 步上限（只判 1 子环节 3 篇）②禁 2-3 篇样本外推领域级结论（B1-B3 是综述背书子环节不是领域级结论）。

### 阶段 2：复用旧笔记前重新精读 sat.1553 content.md 核心段（守 H017 纪律 5）

读 papers/_read_notes/10.1002_sat.1553.md（2026-06-16 早期 B1 方向时期写的）+ papers/doi/10.1002_sat.1553/content.md L440/L558/L788 三 open problem 段原文。

**关键发现（守 H017 纪律 5）**：sat.1553 笔记 L70"可扩展方向 (1) 在综述的'载波恢复'模块里新增一个'湍流相位感知'子模块，把湍流 piston 相位作为相位估计的先验/扰动"——**这条撞 D006**（联合建模进载波同步算法）。笔记是旧 B1 方向时期写的，D006 Kill 是 2026-06-27 在它之后。**笔记里的"可扩展方向"段不过 C3，不复用，本轮重新精读 content.md 核心段独立判断。**

三个 open problem 段原文核查（grep content.md 逐字命中）：
- **L440（B1）**："An adaptive pilot rate... could be an appealing concept... however, the same pilot rate performs similarly for all scenarios as shown in Figure 9... dynamically adjusting the number of symbols used for phase estimation should improve system performance in a channel with large SNR fluctuations. **Further research is necessary to identify practical methods for dynamically adjusting the phase estimation window and to quantify the potential gain.**"
- **L558/L582（B2）**：L558 FOE 段"avoid updating the estimate when the signal quality degrades"（无引文定性）；L582 均衡器段"turn off tracking when the incoming signal power is low [79]"（[79]=Matsuda 2020 SPIE FPGA scintillation-tolerant DSP）
- **L788/L790（B3）**：conclusion"synergies and dependencies between different algorithms and subsystems... data-aided algorithms for phase noise compensation and adaptive equalization could use the same pilot symbols but rely on the timing recovery and frame synchronization system... evaluating the complete DSP chain under realistic conditions is critical"

### 阶段 3：派子 agent 精读三段 + 找最接近 ≤5 篇验证

派 1 子 agent（general-purpose）执行：①精读 sat.1553 三段原文确认 ②grep 查 papers/ 下相关笔记/论文 ③对 B1/B2/B3 各回答 Q1 占住/Q2 够 D005/Q3 A1/Q4 A2/Q5 C3 五问。**守 D017 红线 2（≤5 篇单点验证，不漫灌）+ AGENTS.md（子 agent 不用 WebSearch，优先本地 papers/）**。

子 agent 回传结构化判读（横向表）：B1 待全文+Q4 高风险 / B2 待全文([79]) Q1 黄灯 / B3 偏 FAIL 增量最薄。三点都不撞 D006。

### 阶段 4：主线 grep 核查（FR-26 证据链 + §7.2 防造假）

逐项 grep 核查子 agent 4 个关键声称：

| 声称 | 核查 | 结果 |
|---|---|---|
| sat.1553 L440"同 pilot rate 各场景相近"(B1 A2 平缓风险) | grep content.md line 440 逐字命中"the same pilot rate performs similarly for all scenarios as shown in Figure 9" | **PASS** |
| Panasiewicz 0.42-0.66dB fade penalty(B2 增量) | grep 笔记 L42 命中"10 GSa/s σ=2.6°→0.42 dB；625 MSa/s σ=4.06°→0.66 dB"。**笔记 L55-60 明确 atan2 鉴相器"环路不含湍流相位项""不解决湍流相位扰动"** | **PASS + 重要区分**：Panasiewicz 是"功率不敏感鉴相器"解法，非"冻结更新"解法，跟 B2 是不同解法 |
| 张思齐 joint FOE+CPE ~0.67-0.76dB(B3 占住) | grep manual 张思齐.md：**0.67/0.76/0.71dB 是 FOE 单算法 vs QPSK 分圈(L77/91/206)；joint JCR(菱形分圈)报的是复杂度 13.8-47.6% + NMSE 10⁻¹⁰，没报 BER dB** | **PASS + 重要纠正**：子 agent 把"FOE 单算法 0.67dB"误归到"joint 协同"。B3 占住证据需修正：张思齐 joint 协同核心收益是复杂度降低非 BER 增量 |
| sat.1553 笔记 L70"可扩展方向(1)湍流相位感知"撞 D006 | sed L68-74 核实，"湍流 piston 相位作为相位估计的先验/扰动"确实撞 D006 | **PASS**（H017 纪律 5 警告正确） |

**核查机制中性双向再次有效**（S012 同构）：子 agent 在 B3 张思齐 dB 归属上有偏差（把 FOE 单算法的 0.67dB 误归到 joint 协同），主线 grep 纠正。子 agent 在 B2 Panasiewicz 解法区分上点到了关键（功率不敏感 vs 冻结是不同解法）但表述不够清晰，主线核查笔记 L55-60 澄清。

### 阶段 5：主线判读汇总（B1-B3 综述背书子环节）

| 切入点 | Q1 占住 | Q2 够 D005 增量 | A1 归属 | A2 指标敏感 | C3 撞D006 | 总判读 |
|---|---|---|---|---|---|---|
| **B1** 自适应pilot窗口 | 理论锚被占(Leven[60] 2007)，工程实现空白 | 未量化（综述自评"同rate各场景相近"=A2平缓风险信号） | 改进(可过) | **🔴 平缓风险高(4B同构)** | 不撞 | **A3 待全文+Q4高风险** |
| **B2** deep fade冻结 | 部分占(Matsuda[79]均衡器侧/Panasiewicz鉴相器侧)，FOE专项冻结弱 | Panasiewicz 0.42-0.66dB（**功率不敏感方案非冻结，不同解法**） | 改进(可过) | 敏感(优势) | 不撞 | **A3 待全文([79])，Q1黄灯** |
| **B3** 子系统协同 | 高度占(张思齐joint JCR/LCOMM pilot同喂/jphot FSTS) | **纠正**：张思齐 0.67-0.76dB 是 FOE 单算法非 joint 协同；joint JCR 核心收益是复杂度降低(13.8-47.6%)非 BER dB | 改进(可过) | 部分敏感 | 不撞 | **偏FAIL，增量最薄** |

**三点都不撞 D006**（纯 DSP 工程优化，不建模湍流相位）。**C3 全 PASS**。

### 子环节级诚实结论（守 H017 纪律 2：不下领域级结论）

**这是综述背书子环节（sat.1553 自报 open problem）的判读，不是载波同步领域级结论。** B1-B3 三点：
- 没有一点 A3 直接 PASS（B1 待全文+高风险 / B2 待全文+黄灯 / B3 偏 FAIL）
- 没有一点 A3 直接 FAIL 到"领域死"（B1/B2 是"待补 [58][60][79] 全文才能最终判"，B3 是"偏 FAIL 但增量薄不是物理没缝"）
- **最危险=B1**（综述自身 Fig.9 已示 pilot rate 对场景不敏感，A2 平缓风险与 4B 同构，建议先 FR-21 算窗口自适应的理论 BER 上界）
- **最有潜力=B2**（Q4 敏感是真实物理 gap→性能 gap，痛点真实；但需补 [79] Matsuda 全文窄化 FOE 专项）
- **B3 增量最薄且已被同场景论文占据**（张思齐星地湍流场景已做 joint 载波恢复）

**已知债务**（诚实标）：[58] Martins 2021 / [60] Leven 2007 / [79] Matsuda 2020 三篇 sat.1553 核心引文**均未落盘本地**，B1/B2 的 A3 最终判读均标"待全文"。R003 列的降级源（ResearchGate/作者主页/Lens.org/SerpAPI）未穷尽尝试（守 H017 纪律 3 留下对话处理）。

## 决策引用

- D017：D015 v2（本轮执行对象，判读层 ≤5 篇单点验证 + C3 换皮核查）
- D006：联合建模红线（C3 核查用，B1/B2/B3 全不撞，sat.1553 笔记 L70 旧"可扩展方向"撞）
- D005：务实路线（A3 判读"赢传统 baseline 几 dB"标准来源，B1-B3 增量普遍 <1dB 或未量化）
- D009：靠谱方向 checklist（A1/A2/A3 + B/C 判读框架来源）
- **无新建 D###**（本轮是判读层 1 子环节 3 篇，未到方向决策级；载波同步领域结论要等 B 档全判完）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（载波同步 v2 判读层 B1-B3 是 H017 既定下一步；判读不是立 Q#，不预设方向）

## 后续

### 判读层剩余（下对话执行 H018）
B 档 12 个，已判 7 个（CFO B4/B5/B6/B7 + 综述 B1/B2/B3），剩 5 个：
- **B10** 16-QAM pilot RLS（`10.1007/s11107-024-01019-2`，无 abstract 待精读核验 dB，跨 Q2 16-QAM 种子联读 D011 登记）
- **B8** RL+GS 自相干自消除（`10.1364/jocn.468220` JOCN 2022）/ **B9** 虚拟载波自相干（`10.1109/jlt.2023.3270673` JLT 2023）— 自相干路线 2 篇
- **B11** NDA-ML STO+CPE（`10.1109/LPT.2024.3523478` PTL 2025）/ **B12** 频域 pilot 相位噪声（`10.1109/tcomm.2022.3171809` TCOMM 2022）

### 决策点（报用户拍板，不自作主张）
1. 若 B 档剩 5 个也全 A3 FAIL 或待全文（跟 B1-B3 + CFO 第一批一致）→ 载波同步领域判读层证据下"够 D005 点普遍未量化/增量薄"（**但仍不下"领域死"结论**——债务是 [58][60][79] 未落盘，穷尽降级源前不判死）
2. 若有 A3 过的 → 进 D009 完整 checklist + 立 Q# 候选
3. **是否放宽 D005 到等效指标（MSE/复杂度/范围）是 Go/Kill 决策报用户**——不自作主张放宽（H017 纪律 8）

### B1-B3 各自的 salvage 分析（供用户参考，不预设）
- **B1**：FR-21 算窗口自适应理论 BER 上界 ≥0.5dB 才值得做（4B 同构 A2 平缓风险）
- **B2**：补 [79] Matsuda 全文确认 FOE 专项冻结没被覆盖，窄化到"FOE 专用功率门控冻结并量化 vs 不冻结的 dB 增量"
- **B3**：找张思齐/LCOMM 都没做的协同维度（如把 fade 感知纳入协同调度），否则增量不足

## 核心教训（本轮）

1. **核查机制中性双向再次有效**（S012 同构）：子 agent 在 B3 张思齐 dB 归属有偏差（把 FOE 单算法 0.67dB 误归 joint 协同），主线 grep 纠正。子 agent 在 B2 Panasiewicz 解法区分点到关键但不够清晰，主线核查笔记澄清。**主线不能盲信子 agent 报告，每条关键声称必独立 grep**。
2. **复用旧笔记前重新精读核心段有效**（H017 纪律 5）：sat.1553 笔记 L70"可扩展方向(1)湍流相位感知"撞 D006，笔记是 D006 Kill 前写的，不复用其"可扩展方向"结论。本轮重新精读 content.md L440/L558/L788 独立判断，三点全不撞 D006。
3. **守 3 步上限成功**（profile 第 5 次验证防线）：本轮严格只判 B1-B3（1 子环节 3 篇），没贪多继续判 B8-B12。报到+精读+判读+核查控制在合理范围。

---

## 追加段（D018 后补）：B1-B3 中性信息还原表

> 2026-07-02 D018 后补。D018 把判读模式从"边摸边 Kill"改为"中性提取+全摸完排优先级"。本段把上面阶段 5 的 Go/Kill 判读（偏 FAIL/待全文）**还原成中性描述**，跟 B 档剩余 5 个一起入总表给用户排优先级。原 Go/Kill 判读保留在上面（审计痕迹不删）。

| 切入点 | 这篇/这方向做了什么 | 报了啥增量 | 撞 D006? | 跟星地湍流载波同步什么关系 | 备注 |
|---|---|---|---|---|---|
| **B1** 自适应pilot窗口 | 综述 sat.1553 L440 提的 open problem：动态调 pilot 符号数/相位估计窗口适应大 SNR 波动。理论锚 Leven 2007 [60]（最优窗口=f(SNR/相位噪声)）已确立 | **未量化**：综述只给定性"should improve"+"Further research necessary to quantify"。同 pilot rate vs V&V+差分 scenario 4 ~1dB（但这是 pilot vs 差分对比，非"自适应窗口 vs 固定窗口"）。**综述自评"同 pilot rate 各场景相近"（Fig.9）** | 不撞（纯 DSP 工程优化，不建模湍流相位） | SNR 波动是星地湍流衰落特征，窗口自适应理论上面向星地有物理意义 | 理论锚 [60] + [58] Martins 2021 dual-stage 均未落盘；sat.1553 Fig.9"同 rate 各场景相近"提示窗口对 SNR 依赖可能平缓（待 FR-21 上界算） |
| **B2** deep fade 冻结 | sat.1553 L558（FOE 段，无引文）+ L582（均衡器段引 [79] Matsuda 2020 SPIE FPGA）提的"fade 期间冻结估计避免发散"策略 | Panasiewicz 0.42-0.66dB penalty（笔记 L42）——**但这是"功率不敏感 atan2 鉴相器"的增益，非"冻结更新"方案**。[79] Matsuda 均衡器侧未落盘无 dB。FOE 专项冻结增量未量化 | 不撞（冻结是估计器状态机控制，fade 判据是接收功率标量门控，不建模湍流相位） | fade 是星地湍流深衰落特征，估计器在 fade 发散是真实痛点 | 痛点被两个角度部分占：Matsuda[79] 均衡器侧冻结 + Panasiewicz 鉴相器侧功率不敏感（不同解法）。FOE 专项冻结是否还有独立空间待 [79] 全文 |
| **B3** 子系统协同 | sat.1553 L788 conclusion 提的"pilot 同喂相位补偿+均衡，依赖帧同步对齐"。张思齐学位论文已做 joint JCR（菱形分圈，FOE+CPE 复用四次方信号+最优频偏选取） | **张思齐 joint JCR 核心收益=复杂度降低 13.8-47.6%，没报 BER dB 增量**。0.67-0.76dB 是张思齐 FOE 单算法 vs QPSK 分圈（非 joint 协同）。LCOMM.2026.3651445 pilot 同喂 FOE+CPE 报 Q-factor +0.9dB（光纤非星地） | 不撞（纯 DSP 流水线集成/对齐工程，不碰湍流相位建模） | 张思齐场景=星地湍流（弱/强），跟标题完全对口；LCOMM 是光纤但 pilot 同喂范式可迁移 | 协同/复用已是活跃方向（张思齐星地+LCOMM 光纤+jphot FSTS），占住程度最高。剩余空间=找张思齐/LCOMM 都没做的协同维度 |

**三点都不撞 D006**（纯 DSP 工程优化不建模湍流相位）。

**中性还原后的观察（非 Go/Kill 结论，供总表排优先级用）**：
- B1 的风险信号是"sat.1553 自评同 rate 各场景相近"（窗口对 SNR 依赖可能平缓），但这是综述一张图的观察不是定论，排优先级时算 FR-21 上界即可知
- B2 的痛点真实（fade 发散）且 Q4 敏感（fade→BER 爆炸），但需补 [79] 看 FOE 专项被占没
- B3 占住程度最高，但张思齐核心收益是复杂度不是 BER，"BER 维度协同"可能仍有空间（只是没人报）

**跟原 Go/Kill 判读的差异**：原判读把 B1 标"Q4 高风险"、B2 标"Q1 黄灯"、B3 标"偏 FAIL"——这是用 A2/A3 提前砍。中性还原后这三个都只是"信息未齐/需补全文/需算上界"，**不是"不行"**，留给总表阶段排优先级时用户决定。
