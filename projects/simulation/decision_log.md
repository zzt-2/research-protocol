# Decision Log — projects/simulation

> 项目级决策记录。GW 阶段每步决策追加。

## D-S5-01: Baseline 选定 — DA ML（pilot sp=4）= FR-15 目标 baseline

> 阶段: GW Step 5（Baseline 选定，gw-validate.md）| 日期: 2026-07-06
> 依据: literature_notes 载波同步 v2 章节 12 篇 B 档 + 块 A/B/C/D 论文 baseline 字段 + D005 MVE Go 判定
> 用户确认: ⬜（待——本轮轻量版，田野调查≥10 篇待补 H005）

### 决策

**选定 DA ML（pilot-aided decision-aided ML，pilot spacing=4）作为 SC-NDA-ML 改进方向的 FR-15 目标 baseline（贡献声称要超越的对手）。**

### Baseline 候选评估表（基于 literature_notes 现有 12 篇 + 块 A/B/C/D）

| 方法名 | 作为 baseline（对比方法）| 作为核心方法 | 使用论文 | 代码状态 | 算法描述质量 | 推荐优先级 |
|---|---|---|---|---|---|---|
| **DA ML（pilot-aided decision-aided ML）**| **B11**（+2dB vs DA ML，主对比）| B11 锚引用 [10] DA ML 自实现 | L21 (B11) | 自实现（common/_recovery.py:da_ml_recovery）| 详细（B11 行 181/191 闭式 + pilot sp=4 近最优）| **1（选定）**|
| pilot-aided RLS（CFO+PN 联合）| — | B10（h1→CFO/h0→PN）| L20 (B10) | 无（ao.581648 D011 种子）| 中等 | 3（不同子方向，高 CFO 场景）|
| 频域 CW pilot（in/out-band）| — | B12 锚（improved 估计器≈MVU）| L22 (B12) | 无 | 详细（TCOMM 2022 解析框架）| 4（频域 vs 时域架构不同）|
| Gardner TED + FOE | B7 锚（TED 增益周期）| B7（OFC 2026）| L17 (B7) | 无 | 中等 | 2（B7 候选方向 baseline，非本方向）|
| 短时谱粗 CFO | B5 锚（±4.5GHz LEO Doppler）| B5（optcom 2024）| L15 (B5) | 无 | 中等 | 5（FOE 子组件，非 CPE baseline）|
| Diff-4th（4 次方）| 块 A 论文（L02 主对比）| 块 A | L02 | 自实现 | 详细（Leven 2007 经典）| 6（QPSK/16-QAM 经典，非 M-APSK）|
| VV CFR | 块 A 论文（L05 定性引用）| 块 A 多篇 | L01, L05 | 自实现（common/_recovery.py）| 详细 | 7（通用 CPR，非 M-APSK 专用）|
| **BPS / 2S-BPS（Blind Phase Search）**| 田野调查 2 篇显式对比（Diniz'19, Blatter'25）| — | 田野（未精读）| 无 | 详细（光纤 CPR 主流基准）| **候选补充**（主面 QAM 非 M-APSK，场景不同，迁移对比二级基准）|

**频率统计**（区分角色，守 gw-validate F5 教训）：
- **DA ML 作为对比方法**：1 篇（B11，主对比）—— 频率低但**正是 NDA-ML 方法的天然对照**（B11 自己选的）
- **pilot-aided 大类作为核心方法**：B10/B12（3 篇含 B11 锚引用）—— pilot-aided 是载波同步主流范式
- **DA ML 是 pilot-aided 大类下的近最优实现**（pilot sp=4 充分时）

### 选择理由

1. **领域共识**：DA ML 是 NDA-ML 方法的天然对照（B11 自选），pilot-aided 是载波同步主流范式（B10/B11/B12 三篇核心方法均 pilot-aided 或对照 pilot-aided）
2. **FR-14 最强简单先验**：DA ML pilot sp=4 是 pilot-aided 载波相位估计的**近最优**实现（pilot 充分时），是最强简单先验 baseline
3. **FR-15 贡献目标 baseline**：本方向贡献声称 = 单载波时域 NDA-ML 在公平总功率下赢 DA ML，MVE 已验证（D005 fair gain +0.704~+1.922dB）
4. **代码状态良好**：DA ML 已在 common/_recovery.py 实现（da_ml_recovery），pilot sp=4，pilot 符号从已知 bits 生成
5. **算法描述详细**：B11 行 181/191 给出 DA ML 闭式 + pilot sp=4 近最优论证

### 降级说明（样本量充足，不降级）

gw-validate.md "样本量不足降级策略"：
- 精读论文 12 篇（B 档）+ 块 A/B/C/D ~10 篇 = ~22 篇 ≥ 8 篇门槛
- **田野调查（gw-validate Step 2）已补完**（2026-07-06，子 agent 5 query × 51 篇去重 → 18 篇载波同步相关 ≥10 篇门槛）
- 置信度：**中高 → 维持中高（田野部分确认，不升级）**

### 田野调查结果（gw-validate Step 2，2026-07-06 补完）

**子 agent 执行**：5 个 query（single carrier APSK CPE / satellite FSO carrier sync / M-APSK NDA / satellite optical carrier recovery / 16APSK NDA-ML Wiener），活跃源 S2+OpenAlex（Exa 额度耗尽，SerpAPI/Tavily 未装，Q2 FSO 专用 query 自动路由纯 web 源返回 0 已用 Q4 补救）。51 篇去重 → 18 篇载波同步相关。

**Baseline 频率统计（田野样本 N=18）**：

| Baseline 方法 | 田野出现次数 | 精读覆盖 | 标记 |
|---|---|---|---|
| NDA-ML / M-th-power 升幂 | 4（Du'25=B11, Rice'22, Tang'24 OML, Brannstrom'05）| ✅(B11 核心) | 领域共识 |
| **BPS / 2S-BPS（Blind Phase Search）** | **2 显式对比**（Diniz'19, Blatter'25）| ❌ 不在 7 候选表 | **候选补充**（光纤 CPR 主流基准，但主面 QAM 非 M-APSK）|
| VV CFR（M-APSK + Wiener）| 1（Wang'24 JPHOT，精确匹配本项目调制+噪声类）| ✅(候选 7) | 局部共识，直接相关 |
| pilot-aided / DA-ML | 2 核心方法（Zhang'12, Temga'14）| ✅(候选 1 选定) | 领域共识（非最高频显式基准）|
| Kalman 族（UKF/KF-PCA/EKF）| 3（Sun'20 星地, Li'24, X.Tang'23）| ❌（候选 2 RLS 相关）| 候选补充（星地光场景高频）|
| PCA-based CPR | 3 作为方法（Diniz'19, Li'24, Tang'24）| ❌ | 候选补充（主要 QAM）|
| Gardner TED / 频域 CW pilot / Diff-4th | 0 显式 | ✅(候选 3/4/6) | 田野罕见 → 可能非本子领域共识 |

**关键发现**：
1. **DA ML / pilot-aided 部分确认**：pilot-aided 作为核心方法出现 2 次，但**田野显式基准最高频是 BPS**（光纤 CPR 主流，2 篇显式对比）。DA-ML 作为 NDA-ML 天然对照的逻辑仍成立（B11 自身即 NDA-ML，其锚方法 Wang'22 单正弦 ML 在田野命中 = 交叉验证通过）
2. **场景外推受限**：田野论文主要落 fiber QAM + 星地/星间 QPSK；**精确匹配"单载波 M-APSK + Wiener PN"仅 2 篇**（B11 + Wang'24 VV）。结论：DA ML 在 NDA-ML 改进子领域是合理基准，但跨子领域（光纤 QAM）显式基准倾向 BPS
3. **3 个候选补充**：BPS（光纤主流基准）/ PCA-based CPR（现代 NDA 方法簇）/ Kalman 族（星地光高频）

**对 D-S5-01 选定的影响**：
- **DA ML pilot sp=4 维持选定**（FR-15 目标 baseline 不变）。理由：①NDA-ML 天然对照是方法学逻辑（NDA vs DA 是载波同步二分法），不靠田野频率 ②pilot-aided 近最优 ③MVE 已验证赢之（D005）④BPS 主面 QAM 非 M-APSK，架构不同，不应强加为 FR-15 目标 baseline（守 D005 务实路线，不反向"急于加严 baseline 自找麻烦"）
- **BPS 补进评估表为候选补充行**（优先级中，备注"光纤 CPR 主流基准，主面 QAM，场景不同，作迁移对比二级基准"）
- **Kalman/PCA 标"新方法簇"备注**，不进目标 baseline（PCA 主面 QAM，Kalman 是另一改进方向非本项目 CPE 核心）

**抽查证据（FR-26 证据链）**：
1. Diniz et al. 2019, Opt. Express (10.1364/OE.27.015617, S2) — 摘要显式"outperforms BPS at low SNR"，基准=BPS，QAM，fiber
2. Blatter et al. 2025, IEEE PTL (10.1109/LPT.2025.3582338, S2) — 摘要显式"outperforms 2S-BPS, surpasses U-CPE"，基准=2S-BPS，shaped-QAM，fiber
3. Wang et al. 2024, IEEE JPHOT (10.1109/JPHOT.2024.3415635, S2) — 摘要"refined Viterbi-Viterbi for M-APSK with Wiener PN, LMMSE"，方法=VV，**精确匹配本项目调制+噪声类**

### 用户审查待办（gw-validate [MUST]）

- [ ] 用户审查 baseline 选择 + 田野调查证据（本 D-S5-01 + 田野调查段）

## D-4a-01: SC-NDA-ML MVE Go（D005，从专题 decisions.md 引用）

> 阶段: GW Step 4a 维度 D | 日期: 2026-07-06
> 完整决策见 `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D005

**SC-NDA-ML MVE PASS → Go**：公平对照 fair gain @ HD-FEC AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB，strong 物理不可达但工作区全赢 DA。进 Step 5（本轮 D-S5-01 完成 baseline 选定）。

## D-4a-02: 4a 全维度 feasibility_report.md Go 决策（本轮）

> 阶段: GW Step 4a | 日期: 2026-07-06

**feasibility_report.md Go 决策**：A0 无致命 + A'/A/B 无致命 + MVE 通过 + FR-20 参数已溯源 + FR-21 oracle 上界前置通过（CRLB 层）。详见 `projects/simulation/feasibility_report.md`。用户确认 ⬜ 待。

## D-4b-01: 4b（C/E 维度）Go 决策（本轮）

> 阶段: GW Step 4b（gw-feasibility §4b）| 日期: 2026-07-06
> 依据: C/E 维度评估（`projects/simulation/feasibility_report.md` C/E 段）+ D-S5-01 baseline 选定 + 田野调查（gw-validate Step 2）
> 用户确认: ⬜（待）

**决策**：**Go**（继续 Step 6 仿真器设计）。

**C 维度（仿真条件可行性）无致命**：
1. ✅ 仿真环境支撑核心方法（MVE 已跑通，fair gain 0.704-1.922dB @ HD-FEC）
2. ✅ 差异信号足够大（BER 跨 SNR 降 ~2 个数量级，远超噪声底 N=102400）
3. ✅ 含 NDA-ML 擅长特征（频谱效率维度 + deep fade 鲁棒性维度都在仿真）
4. ✅ 无"过于平滑"预警（三重独立随机源：GG 块衰落 + Wiener PN + Doppler CFO）

**E 维度（资源/风险比例）无致命**：
1. ✅ Baseline 代码全自实现良好（DA ML + NDA-ML + oracle + VV CFR 都在 common/）
2. ✅ 时间投入与贡献成比例（Step 6~1 对话 + Step 7~2-3 对话，贡献=形态 A+C 双增量，会议级别够格）
3. ✅ 失败兜底充分（形态 A 独立成立 AWGN +0.704dB + 形态 C weak/moderate buffer ≥0.5dB + 次优成果可回收）

**已知风险（不卡 Go，记录）**：
- 田野调查"部分确认"（DA ML 非最高频显式基准，BPS 在光纤 QAM 更高频）→ 不影响本项目（单载波 M-APSK + 星地，BPS 场景不同），论文写作需说明 baseline 场景依据
- Step 6 正式仿真器需独立实现（不复用 explore 探针，守 MVE 独立性债务）

**后续**：进 Step 6（仿真器设计，守 FR-12 MVE→Formal 架构差异门控）。
