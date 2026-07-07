# [S001] 开题 + 阶段 0 六项规约设计 + 复用基建盘点

> 2026-07-08 | 阶段: 主控对话开题（B2-Q2 第三候选）| 状态: 完成，阶段 0 规约设计完成，交工作对话执行

## 目标

主控对话角色：核查 S031 候选池 + 开 B2-Q2 专题 + 设计阶段 0 六项规约 + 交接给工作对话。不自己执行精读/MVE（那是工作对话的事）。

## 记录

### 触发与决策（D001）

用户"再开另一个方向"触发第三候选选择。主控对话先核查 S031 候选池（B7 active + NDA-ML dormant 之外的可开候选），列 4 选项（B3-Q2 / B2-Q2 / B5-Q1 / D006 边界模式 7 次）给用户选。

用户选 **B2-Q2（pilot 在 fade）**，主控对话派 Explore agent 查详情后发现关键张力（step4a 实测反证核心命题），亮给用户后用户选**"开，但首验证张力"**。

D001 决策记录在 `decisions.md`。voice.md 登记 3 条原话。

### 关键核查发现：step4a 实测反证 B2-Q2 核心命题

**这是主控对话核查的核心价值**——S031 排优先级时只排了序（第二档 #7），没做 A0/D 详评。主控对话派 Explore agent 查详情时发现：

- **B2-Q2 核心命题**：pilot-aided fallback 在 fade 比 blind freeze 更优（sat.1553 L440 +1dB 来源）
- **step4a 实测**（`step4a-mve-execution/decisions.md:150, 157`）：DA pilot 在 deep fade BER 崩溃（5dB weak 0.38）vs NDA 全帧积分鲁棒（0.29）
- **张力**：两个结论在单载波时域下直接打架
- **sat.1553 +1dB 口径错位**（`_cut-b1b2b3-verify.md:144-146, 342`）：是 pilot-aided 相位估计 vs VV+差分编码，**不是 pilot-aided FOE vs blind freeze 的增量**

→ B2-Q2 不是"稳够格"候选，但用户选"开，但首验证张力"，遵守用户决策权。

### B2-Q2 基本面（Explore agent 核查结果）

| 维度 | B2-Q2 | 证据 |
|---|---|---|
| M-C-A | M=[79] Matsuda FOE freeze + sat.1553 blind gating / C=deep fade 冻结后恢复时 FO 已漂移 / A=blind 重新收敛时间未量化 | `_B2-deep-fade-freeze-increment.md:64-69` |
| dB | +1dB（sat.1553 L440，scenario 4 上行强湍 σp²=0.25，**口径=PE vs VV+diff 不是 FOE freeze 增量**）| `_cut-b1b2b3-verify.md:144-146, 342` |
| 范围 | in 星地（三篇锚都是 OSL）| `_B2-deep-fade-freeze-increment.md:50` |
| D006 | 不撞（双模切换是估计器选择，不纳入湍流相位到算法设计）| `_B2-deep-fade-freeze-increment.md:68` |
| 池类型 | 饱和池 §A 小池（sat.1553+Matsuda+Paillier 3 篇，无超级大点）| `_cut-map-final-b1-b12.md:19-29` |
| A1 归属 | [79] SPIE 2020 已发，搬星地非论文外改进（场景已在范围），算法创新=双模切换。A1 风险低于 B7/B3 | `_B2-deep-fade-freeze-increment.md:74` |

### 复用基建盘点（NDA-ML 对偶，4 估计器全有）

`projects/simulation/common/_recovery.py`：

| 估计器 | 行号 | 用途 | B2-Q2 角色 |
|---|---|---|---|
| `fft_foe(rx, N_fft, nfft_zp)` | L37 | blind 4 次幂 FOE | **B2-Q2 blind 侧**（freeze 路线）|
| `nda_ml_recovery(rx, M0, mod)` | L171 | NDA-ML 盲估 | B2-Q2 blind 侧备选 |
| `da_ml_recovery(rx, pilot_idx, pilot_sym, mod)` | L136 | DA/pilot-aided ML | **B2-Q2 pilot 侧**（fallback 路线）|
| `psa_foe_recovery(rx, pilot_idx, pilot_sym)` | L435 | Pilot-Aided FOE | B2-Q2 pilot 侧备选 |

**B2-Q2 双模切换 = (fft_foe/nda_ml + 功率阈值 gating) ↔ (da_ml/psa_foe) 模式切换**，基建齐全，无需新建估计器，只需加 fade 检测门控 + 切换逻辑。

**复用风险**（`H002:26`）：
- step4a DA ML 是"单载波近最优 DA ML（pilot spacing=4 密集真符号 pilot，vs oracle +0.27dB）"，非 B11 论文 decision-feedback DA ML
- B2-Q2 复用时需注意 pilot 配置口径差异 + DA pilot overhead 1.25dB 总能量代价已在公平对照框架中制度化（`decisions.md:142, 155`）

### 阶段 0 六项规约设计（B2 特殊版）

| 阶段 | 内容 | B2 特殊重点 | 守 |
|---|---|---|---|
| 0.1 | **核心命题张力验证设计** | step4a 实测反证 vs sat.1553 +1dB，怎么设计 fair comparison 消化张力 | INVARIANT 11（B2 特殊）|
| 0.2 | dB 溯源核查 | sat.1553 L440 +1dB 口径错位（PE vs VV+diff 不是 FOE freeze 增量）| INVARIANT 12（B2 特殊）+ V6 FR-26 |
| 0.3 | 架构定性（前馈 vs 环路）| 双模切换的前馈化（fade 检测门控+模式切换不纳入环路 TF）| INVARIANT（继承上游）+ D006 |
| 0.4 | 公平对照框架设计 | baseline 是纯 blind freeze [79] 还是 sat.1553 blind gating？fair gain @ BER 还是 HD-FEC？pilot overhead 1.25dB 怎么公平处理？叙事定位（双模切换 vs 纯盲的差异化）| INVARIANT 13（B2 特殊饱和池警示）|
| 0.5 | 参数真相源前置 | fade σp² / OSNR / 符号率 / 线宽 / pilot 配置，全标 source_type + 读原文数值 | TL-26 + FR-26 |
| 0.6 | 文件组织规约 | `explore/b2-fade-freeze-pilot-fallback/` 目录结构 + 命名规则 + 下游引用同步清单 | NDA-ML D-007 教训 2 |

### B2 特殊风险（vs NDA-ML/B7 的差异点）

| 风险 | B2-Q2 | 流程对策 |
|---|---|---|
| 核心命题被反证 | step4a 实测 DA pilot 在 fade 崩溃 | **阶段 0.1 首验证张力**（最高优先）|
| dB 口径错位 | sat.1553 +1dB 是 PE vs VV+diff | 阶段 0.2 dB 溯源核查 |
| 饱和池 dB 难出 | 小池 3 篇无大点 | 阶段 0.4 公平对照框架 + TL-20 理论预期 |
| 叙事撞车 | fade 鲁棒性跟 NDA-ML 命题撞 | 阶段 0.4 明确叙事定位 |
| A1 归属 | 双模切换算法创新 | A1 风险低（优于 NDA-ML/B7）|

## 决策引用

- **D001**（新建）：开 B2-Q2 专题 + 首验证张力策略
- 无其他新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**（主控对话开题 + 阶段 0 规约设计，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约全做完才进 sandbox，本对话只设计规约不执行
- **守 3 步上限**：本轮 2 步（①核查 S031 + 派 Explore agent 查 B2-Q2 详情 ②开专题 + 阶段 0 规约设计 + 写 S001/H001）
- **守主控对话角色**：不自己精读/不跑 MVE，核查工作对话产出（Explore agent）+ 亮关键张力给用户

## 后续

### 交工作对话执行

1. **阶段 0.1 核心命题张力验证设计**（工作对话核心）：设计 fair comparison 把 step4a 实测反证 vs B2-Q2 命题变成可验证假设。输出 `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md`
2. **阶段 0.2 dB 溯源核查**：把 sat.1553 L440 +1dB 限定到原始口径（PE vs VV+diff），B2-Q2 增量是独立 MVE 的事
3. **阶段 0.3-0.6**：架构定性 / 公平对照 / 参数真相源 / 文件组织

### 主控对话跟进点

- 核查工作对话阶段 0.1 的张力验证设计是否真消化了 step4a 实测反证（不是绕过）
- 核查阶段 0.2 的 dB 溯源是否把 sat.1553 +1dB 限定到原始口径
- B2-Q2 跟 NDA-ML 的交叉：B2-Q2 张力验证结果对 NDA-ML 方法方向（X/W）决策有交叉验证价值

### 已知风险（交工作对话）

- **核心命题可能崩塌**：如果阶段 0.1 设计的 fair comparison 验证后发现 pilot-aided 路线在单载波时域根本打不过盲估（不是 spacing 配置问题），B2-Q2 核心命题崩塌转 Kill
- **饱和池 dB 难出**：切法地图 §C 警示饱和池是 dB 最难出区，B2-Q2 可能要靠范围或鲁棒性维度够格（D005 会议门槛放宽允许）
- **叙事撞车**：B2-Q2 跟 NDA-ML 都是 fade 鲁棒性问题的解法，阶段 0.4 必须明确差异化（双模切换 vs 纯盲）
