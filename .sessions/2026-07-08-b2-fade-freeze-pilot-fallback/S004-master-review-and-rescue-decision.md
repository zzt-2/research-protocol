# [S004] 主控对话 sandbox V5 核查 + 方向定夺——前馈化降级 + 救援路线（放松到 [79] 式闭环 hold + power-boosted pilot）

> 2026-07-08 | 阶段: 主控对话（核查工作对话 sandbox 产出 + 定夺 B2-Q2 方向）| 状态: 完成，D002+D003 登记，H004 交阶段 1.5 重设计

## 目标

承接工作对话 S003 + H003 交接，本轮主控对话：①V5 主控独立重算 sandbox 数据（不只信工作对话结论）②核查 [79] freeze 实现一致性（V3 祖师爷）+ γ_th 选择策略 + 公平性 bug 修复 ③定夺 B2-Q2 方向（Kill / 放松前馈化 / 重新定位）。守 sim-preflight v1.3.0 V5 + profile "Go/Kill 是用户的" + D006 红线。

## 记录

### 报到 + 接收方验证（Trigger 1 + Trigger 5）

读完必读清单：topic-index（14 不变量）/ H003 / S003 / decisions（D001）/ sandbox 7 产出（_sandbox_results.json / _sandbox_three_way.py / _rho_fade_measure.json / _gamma_th_sweep.json + .py / _b2_params_draft.py + 阶段 0 六份规约 .md）/ [79] L33（`_B2-deep-fade-freeze-increment.md`）/ D006（`2026-06-20-problem-driven-redirection/decisions.md:313-355`）/ 阶段 0.3 `_architecture_decision.md` / voice / profile。

**接收方验证 6 项核查结果**：

| 项 | H003 报 | V5 主线独立核查 | 结论 |
|---|---|---|---|
| C2 红线不成立 | da 多数赢 blind | grep 21 点：da 赢 11/21（52%），weak/moderate 低中 SNR + strong 中 SNR 显著赢（差值 -0.03~-0.13）| ✅ PASS |
| 动态恢复结构性失效 | A_recover ≈ C_recover | grep 21 点：`n_recover_A_mean_blocks` == `n_recover_C_mean_blocks` **全部完全相同**（精确到小数 3 位）| ✅ PASS |
| 公平性 bug 修复 | A 全程 blind h / C2 配对匹配 | 核查 `_sandbox_three_way.py:169-186`：A fade 块也 blind h（freeze 只 freeze 相位不 freeze h），C2 测试 blind/blind + pilot/pilot | ✅ PASS |
| γ_th 选择策略修正 | σ 标准化失效 → ρ_fade 反推 | 核查 `_gamma_th_sweep.json` meta：σ 标准化在 strong 致 ρ_fade≈0.008，改用 ρ_fade=0.15 反推 | ✅ PASS |
| [79] freeze 实现一致性（V3）| freeze_compensate_block 一致 | 核查 `_sandbox_three_way.py:114-121` + `_B2-deep-fade-freeze-increment.md:33`：前馈近似版 hold (phi_last, omega_last)，**但 [79] 原始是闭环 tracking loop 有环路惯性** | ✅ PASS + 重要 nuance |
| Go3 fair gain 口径 | -0.187dB（C 微输）| 🔴 **口径错**：H003 假设 C BER=A BER 只扣 overhead，实测 C BER 更低 | ⚠️ **修正：+0.02dB** |

### V5 核查关键发现

**发现 1：H003 fair gain 口径错误**

H003 算法：`gain = SNR_A@HD-FEC - (SNR_A@HD-FEC + overhead) = -0.187dB`。假设 C BER 跟 A 完全一样、C 只多了 overhead 惩罚。

**实测 weak C BER 比 A 更低**（4 个 HD-FEC 可达点全 C < A）：
- weak 20dB: A=0.008643 C=0.008601
- weak 22dB: A=0.004211 C=0.003833
- weak 24dB: A=0.001736 C=0.001464
- weak 26dB: A=0.000645 C=0.000512

对数线性插值 HD-FEC(3.8e-3)：A 达 @22.23dB，C 达 @22.02dB，表面 gain = −0.21dB（C 赢 0.21dB），扣 overhead 0.187dB → **fair gain ≈ +0.02dB（C 微赢，但仍远低于 0.5dB 阈值）**。

Go3 从 FAIL(−0.187dB) 修正为 PARTIAL(+0.02dB)——仍不够格，但口径修正重要。

**发现 2：weak 高 SNR fade 块 C 赢 A（H003 漏报）**

反推 A_fade_ber（A 全局 = 非fade×340 + A_fade×60 / 400，假设 A 非fade BER ≈ c2_ber_nonfade_blind_nda）：

weak 22-26dB fade 块 C/A = 0.60-0.85（C 显著赢 A）。这信号 H003 漏报，但量级小（weak 单档 + fair gain 仅 +0.02dB），不改变整体结论。

**发现 3：[79] freeze 实现的关键 nuance（V3 祖师爷）**

[79] 原文（`_B2-deep-fade-freeze-increment.md:33`）：FOE tracking 环路在 received power 下降时关闭 tracking（hold 上一估计值）。**[79] 是闭环 tracking loop**——freeze 时环路滤波器 hold 住状态，fade 结束后环路从 hold 状态重新收敛（有惯性、有时间常数）。

sandbox 实现（`_sandbox_three_way.py:114-121 freeze_compensate_block`）：用 (phi_last, omega_last) 补偿当前 fade 块——**前馈开环近似版**。砍掉了环路滤波器，没有环路重新收敛的动力学。

**这正是"架构-测度不匹配"的根因**：前馈版没有环路惯性，所以 N_recover A≈C（测不出差异）。这不是 B2-Q2 算法的问题，是**前馈架构 + 动态恢复测度的组合不兼容**。

### 方向定夺过程（用户主导，主线被推翻）

**主线初始建议**：Kill B2-Q2（三 Go 全 FAIL + Kill2 结构性成立 + 前馈化是架构约束级）。报告给用户。

**用户追问 1**："啥情况？会不会是代码哪里不对？还是确定物理上不可行?"

**主线分层回答**：
- Kill2（动态恢复结构性失效）= **物理必然**（前馈架构每块独立估计无环路惯性，代码改不了）
- Kill3（稳态 BER）= 量级不够（+0.02dB）但有 da_ml 实现可疑点（step4a D-008 bug 历史）

**用户追问 2**："那别人咋弄的?"

**主线回答**：别人用两条主流路线：
1. **闭环 freeze**（[79] 原版 + 大多数工程实现）：闭环 tracking loop，fade 期 hold 环路状态，恢复时环路重新收敛有惯性。B2-Q2 sandbox 是前馈版砍掉了环路惯性
2. **pilot-aided 全程 + power-boost**：pilot 功率增强降估计噪声。B2-Q2 sandbox 是等功率 pilot，没做 power-boost

→ B2-Q2 sandbox **两个核心机制都没复刻文献已验证的路线**

**用户追问 3**："为啥撞 D006?"

**主线精读 D006 + 阶段 0.3 后修正**：
- D006 Kill 的精确动作 = "把**湍流相位 φ_T** 主动纳入算法建模"（Q12 H(z) 纳入 φ_T / B1 KF 状态扩维含 φ_T）
- [79] 式闭环 hold = **功率阈值 gate 估计器更新**（门控用信号功率 P < γ_th，不用相位 φ_T）+ 环路 TF 固定不感知湍流
- → **[79] 式闭环 hold 严格说不撞 D006**
- 阶段 0.3 `_architecture_decision.md` 把 B2-Q2 钉死成前馈化 INVARIANT，是**过度保守**（为了避免任何 D006 争议的保守选择），不是 D006 真的禁止闭环 hold

**用户拍板**：选"放松前馈化 + power-boost（救 B2-Q2）"（D003）

→ **主线初始 Kill 建议被用户推翻**。这是 profile "Go/Kill 是用户的"的体现——主线产建议，用户拍板。用户不愿轻易放弃，要求试文献已验证的路线。

### 救援路线（D003）+ 3 个诚实风险

**四步重设计**（具体留给下一工作对话 + 阶段 1.5）：
1. 阶段 0.3 重定性：前馈化降级 → [79] 式闭环 hold + 功率阈值 gate（D002 已开绿灯）
2. 阶段 0.4 重审公平对照：加 power-boost overhead（策略：全帧固定 vs 仅 fade 期自适应）
3. 阶段 0.5 加参数：B2Params 加 power_boost_factor + 闭环环路参数
4. 重跑 sandbox：闭环版三方对照（A 闭环 freeze [79] / B 闭环 power-boost pilot 全程 / C 闭环双模）

**3 个诚实标注的风险**：
- **风险 1（物理可行性核心）**：power-boost 3dB 降估计噪声，但 overhead 从 0.187dB 涨到 0.26-0.64dB。trade-off 能否净正需 MVE
- **风险 2（够格）**：B2-Q2 救援版 = 闭环 hold + fade 期切 power-boosted pilot。跟 [79] baseline（闭环完全 hold）差异 = "fade 期切 power-boosted pilot" vs "完全 hold"。sandbox 前馈版测过（C 输 A），闭环+power-boost 能否翻盘未知
- **风险 3（口径）**：power-boosted pilot 是**另一个物理机制**（pilot 功率增强），不是 sat.1553 L440 +1dB（pilot PE vs VV+diff，阶段 0.2 已确认口径错位）。B2-Q2 救援版不能引 sat.1553 +1dB 当自己的——增量需独立 MVE

## 决策引用

- D001（继承）：开 B2-Q2 专题 + 首验证张力策略
- **D002（新建）**：前馈化降级——阶段 0.3 过度保守，[79] 式闭环 hold 不撞 D006（精读 D006 原文 + 阶段 0.3 §3.2）
- **D003（新建）**：救援路线——不 Kill B2-Q2，放松前馈化 + 加 power-boosted pilot。用户推翻主线初始 Kill 建议

## 范围确认

- 本轮是否在 scope boundary 内：**是**（主控对话核查 sandbox + 定方向，不执行重设计）
- **守主控角色边界**：核查 + 定夺 + 记决策 + 写 handoff。重设计是下一工作对话的事（守 3 步上限 + executor 角色边界）
- **守 profile "Go/Kill 是用户的"**：主线产建议（初始 Kill），用户拍板（救援）。主线被推翻后诚实接受，记 D003 救援路线

## 后续

### 下一工作对话（阶段 1.5 重设计）

1. 阶段 0.3 重定性：闭环 hold 具体机制设计（完全 hold vs partial hold + pilot 微调）+ D006 不撞论证（[79] 式功率 gate）
2. 阶段 0.4 重审：power-boost 策略 + overhead trade-off 理论预期
3. 阶段 0.5 加参数：B2Params 扩 power_boost_factor + 闭环环路参数（文献溯源）
4. 重跑 sandbox：闭环版三方对照，守 V2 三方 + V3 祖师爷

### 主控对话跟进点（用户/下一轮核查）

- V5 核查是否真独立重算了（不只信工作对话结论）—— ✅ 本轮主线独立 grep 21 点 results JSON
- [79] freeze 实现是否真严格（V3）—— ✅ 核查 + 发现 [79] 是闭环（前馈版砍惯性是测度失效根因）
- 架构-测度不匹配发现是否被认真对待 —— ✅ D002 前馈化降级 + D003 救援路线直接回应
- Go/Kill 拍板是否交用户 —— ✅ 主线建议 Kill，用户拍板救援（profile 体现）
- D003 是否真记了救援路线 + 3 风险（不是只写"救"）—— ✅ decisions.md D003 含四步重设计 + 3 诚实风险

### 产出物清单（本轮交付）

1. ✅ D002（前馈化降级 + D006 边界精读修正）+ D003（救援路线 + 3 风险）登记 decisions.md
2. ✅ topic-index 更新（status active / 不变量 15 新增 / 已确认决策 +2 / 悬而未决 9 清空 / 当前位置 S004 / 进展线索 +S004）
3. ✅ voice.md 更新（用户四段原话：质疑 Kill + 追问别人 + 追问 D006 + 拍板救援）
4. S004（本文件）
5. H004（交阶段 1.5 重设计工作对话，下一步写）
