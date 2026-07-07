# [S002] 阶段 0.1 锚论文公式完整性核查（+ 用户本地代码破局）

> 2026-07-08 | 阶段：B7 阶段 0 前置规约 0.1 | 状态：0.1 通过（D001），0.2-0.6 交下对话

## 目标

执行 H001 阶段 0.1：核查 B7 锚论文（OFC 2026 poster）公式完整性 + Gardner TED 1986 公式交叉验证，判定是否切降级方案（INVARIANT 13）。

## 记录

### 报到 + 框架文件重读（步骤 1）

- session-governance Trigger 1 报到 + Trigger 5 接收 H001 验证（3 条关键事实声称全 PASS）
- 读 H001 / topic-index（13 不变量）/ _registry（4 依赖全稳定）/ profile（3 画像）/ B7 增量笔记 `_B7-gardner-ted-increment.md`
- 读 step4a-mve-execution/decisions.md（D001-D005 + D-007~D-009 NDA-ML 教训链）
- 读 sim-preflight v1.3.0 新增：`rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条 + `SKILL.md` §1.6 C6-C8
- 读 `stages/gw-feasibility.md` §D 维度 D MVE 11 步
- 读 thesis-lessons TL-13/20（仿真先建理论预期 + 共用信道）

### 阶段 0.1 核查（步骤 2）

**B7 OFC 2026 poster 全文核查**（`papers/doi/10.1364_ofc.2026.w2a.62/content.md` 90 行）：
- **0 个编号公式**
- **4 张关键图全 omitted**：Fig.1a（Doppler↔TED 机制图）/ Fig.1b（算法框图）/ Fig.3（FOE 输出）/ Fig.4（BER 性能）
- 文字可提取：算法结构（CV mult1 扫频→双候选→CV mult2 试补偿→LPF2+Gardner TR→TED2 判决）+ 机制（TED 增益 = S-curve max，随符号净相位旋转周期变化）
- 严重程度：高于 NDA-ML（B7 连机制图都 omitted）

**Gardner 1986 原文核查**（`papers/doi/10.1109_tcom.1986.1096561/content.md`）：
- 扫描 PDF，content.md 只有 14 行 IEEE 授权水印，**正文完全不可检索**
- 原计划的降级 C（用 1986 原文做公式交叉验证）无法靠现有 content.md 实现

### 用户纠偏 + 本地代码破局

主线原预判：公式严重不全 → 触发 INVARIANT 13 红线 → 甩 4 个降级选项（A/B/C/双线）给用户。

**用户原话戳穿**："啥玩意？咱们先说说这是要干啥？顺便，gardner我不是有matlab代码吗？毕设\旧本科代码\Tx2Rx.m"

两个问题：
1. **profile 第 9 次"急于推进"防线第 10 次验证**：主线没讲清阶段 0.1 在干啥就甩降级选项。用户要求先讲清"这是要干啥"。
2. **主线漏查本地代码资产**（FR-26 强化）：只查了 `papers/` 下原文，漏了 `毕设/旧本科代码/` 里的 Gardner TED 实现。

**本地代码核查**：
- `毕设/旧本科代码/PSKTimingErrDetector.m` L11-12 = Gardner TED 1986 原版公式（去直流变种）：
  ```
  e(k) = (y_mid − (y_late+y_early)/2)·(y_late−y_early)  [实部+虚部]
  ```
  等价标准形式 `e(τ) = y(t-T/2)·[y(t) - y(t-T)]`
- `毕设/旧本科代码/Tx2Rx.m` L176-214 = 完整定时恢复环（NCO + 立方内插 Farrow + Gardner TED + PI 环路滤波器）
- 代码是公式的可执行版，比扫描原文可靠（无 OCR 错误风险）

### 0.1 判定（D001）

| 维度 | 判定 |
|---|---|
| Gardner TED 1986 公式完整性 | ✅ 完整可实现（本地代码作公式源）|
| B7 "proposed FOE" 解析式 | ⚠️ 缺失（poster 0 公式 + Fig.1a/b omitted）|
| B7 机制数值重建可行性 | ✅ 可行（用本地 TED 代码扫 Doppler 跑 S-curve）|
| 是否切降级 A/B/C | **不切**（1986 有代码替代，B7 映射靠数值重建非文字猜公式）|

**关键区分**：INVARIANT 13 的"不硬磕"针对"靠文字重建公式"。本场景 1986 公式有代码（不需文字重建），B7 映射靠数值重建（验证机制不是猜公式），不违反"不硬磕"精神。

### 0.1 对后续的影响

- **0.2 数学同族性**：1986 公式明确，B7 创新点是"复用 TED 增益做 FOE"（估频偏 f_D）vs 1986 用 TED 检测定时误差 τ。**初判非同族**（不是同量变体），待 0.2 深度确认（V3+C8）。0.2 核心动作 = 用本地 TED 代码扫 Doppler 跑 S-curve 数值重建 B7 Fig.1a 映射图，验证周期相关是否存在。
- **0.3 架构定性**：用户代码是反馈环，B7 也是反馈环。前馈化决策仍需做（INVARIANT 12，环路撞 D006）。
- **sandbox 三方对照**：① B7 proposed FOE（数值重建）② Gardner 1986 定时环（用户代码当祖师爷方）③ PSA FOE baseline。三方都有实现路径。

## 决策引用

- **D001**（新建）：Gardner TED 1986 公式源 = 本地 Matlab 代码，不切降级，B7 映射靠数值重建，0.1 通过进 0.2
- 无其他新建

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1 是 H001 步骤 2 的第一项，6 项规约之一）
- 未写代码（守 INVARIANT 6 + profile 第 9 次防线）
- 未进 sandbox（守 profile 第 9 次防线）

## 后续

1. **0.2 数学同族性检查**（下对话核心）：用本地 TED 代码扫 Doppler 频偏跑 S-curve，数值重建 B7 Fig.1a 映射图，验证周期相关。派子 agent 深度检查 B7 跟 1986/VV/BPS 的数学关系（≤15 分钟）。输出 `explore/b7-gardner-ted-foe/_lineage_check.md`
2. **0.3 架构定性**：前馈化 vs 环路决策（撞 D006 边界）
3. **0.4-0.6**：公平对照框架 / 参数真相源 / 文件组织
4. **B7 映射债务**：0.2 数值重建验证后，若进 sandbox/MVE 补解析推导
5. **Gardner 1986 扫描原文债务**：本地代码已替代；若需引 1986 具体行号需重新 OCR/换源下载（视需要）

### 已知风险（交下对话）

- B7 映射数值重建若**复现不出周期相关** → B7 机制本身有问题，红线警报（poster 结论不可复现），需重新评估 B7 值不值得做
- 用户代码是 QPSK/16APSK 场景（`M=2^4`），B7 是 DP-QPSK 25-Gbaud，调制/参数差异需 0.5 参数真相源核查时对齐
