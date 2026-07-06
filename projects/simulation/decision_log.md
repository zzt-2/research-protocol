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

### 降级说明（样本量不足）

gw-validate.md "样本量不足降级策略"：
- 精读论文 12 篇（B 档）+ 块 A/B/C/D ~10 篇 = ~22 篇 ≥ 8 篇门槛，**不降级**
- 但 **田野调查（≥10 篇额外论文 abstract 扫描）待补**——本轮只做了精读统计，未做 gw-validate Step 2"领域 Baseline 田野调查"。降级原因：守 3 步上限，田野调查留 H005 子 agent 执行
- 置信度：**中高**。DA ML 是 NDA-ML 天然对照有强先验，田野调查大概率确认（pilot-aided 是绝对主流），但需补做以守 gw-validate 严格性

### 待办（H005 下对话）

- [ ] 派子 agent 做 gw-validate Step 2 田野调查：检索"星地 FSO / 单载波 M-APSK 载波同步 experiment comparison baseline"≥10 篇，扫 abstract 实验设置，与精读统计交叉验证
- [ ] 若田野调查发现新高频 baseline（如某 B5/B7 谱类方法被多篇当对比），补进评估表
- [ ] 用户审查 baseline 选择 + 交叉验证证据（gw-validate [MUST]）

## D-4a-01: SC-NDA-ML MVE Go（D005，从专题 decisions.md 引用）

> 阶段: GW Step 4a 维度 D | 日期: 2026-07-06
> 完整决策见 `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D005

**SC-NDA-ML MVE PASS → Go**：公平对照 fair gain @ HD-FEC AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB，strong 物理不可达但工作区全赢 DA。进 Step 5（本轮 D-S5-01 完成 baseline 选定）。

## D-4a-02: 4a 全维度 feasibility_report.md Go 决策（本轮）

> 阶段: GW Step 4a | 日期: 2026-07-06

**feasibility_report.md Go 决策**：A0 无致命 + A'/A/B 无致命 + MVE 通过 + FR-20 参数已溯源 + FR-21 oracle 上界前置通过（CRLB 层）。详见 `projects/simulation/feasibility_report.md`。用户确认 ⬜ 待。
