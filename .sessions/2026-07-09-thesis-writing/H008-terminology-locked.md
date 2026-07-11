# Handoff: D-P1 用语符号公式三合一完成，交接 D-P2P3 参数+叙事结构

> 来源: D-P1 子对话（本轮即 D-P1 活本身）| 交接目标: D-P2P3 子对话——参数+数字呈现（P2）+ 叙事结构（P3）
> 文件名: H008-terminology-locked.md
> 日期: 2026-07-11

## 到哪了（状态）

D-P1 用语+符号+公式三合一完成。产出 **R011-terminology-symbol-formula.md**（三张表）。

- 2 子 agent 并发查证 A 组 5 篇 + C 组 B11/sat.1553 共 7 篇 content.md 术语用法，逐词标 ✅/❌ + 原句截取 + 行号
- **术语表**：34 词（29 标准词标来源 + 5 显式定义词给定义句 + 5 自造词替换映射）
- **符号表**：22 个符号，全篇统一无冲突
- **公式清单**：3 个核心公式（DA/NDA/per-block SNR），全直接给结论级，标代码行溯源
- 交叉一致性检查 4 项全过

W1-W5 正文写作直接照抄三张表，术语/符号/公式零歧义。

## 下一步干什么

D-P2P3（writing-campaign-plan.md §2 P2 + P3，可合并一个对话）：

### P2 参数+数字呈现（用 R011 符号表）
1. **参数表**：用 R011 符号表的 22 个符号填值。基础已有 `_b11_params.py` 的 `all_traced_params_summary()`（行 112-129）。每个参数标文献来源（TL-26）。重点参数：M₀=8 / LASER_LW=10kHz / α,β(GG 三档下行 + 两档上行) / N_blk=100 / N_DFT=256 / DA_PILOT_SPACING=4 / SNR 范围
2. **数字呈现方案**：主报 naive 口径（D004/D005 已定倾向 naive，强湍流 +1.26~1.85 dB）。口径标注用 R011 net SNR gain 脚注模板。fair = naive + 1.249 dB（`_b11_params.py:68` / fair_comparison.py:109，D004 教训：报前用代码行验证加减方向）

### P3 叙事结构（用 R011 术语分配 R009 逻辑链）
3. **5 节大纲**：把 R009 逻辑链（DA/NDA trade-off → 数据印证 → 切换机制）分配到 5 节。每节标：论点 / 用哪些数字 / 用哪些公式（从 R011 公式清单取）。R007 两段式（影响分析 + 方法）落在 Results 内 §IV-A/§IV-B。对照 R010 各节篇幅 + benchmark-paper-set.md A 组章节结构

### P3 要特别注意的术语（切换相关，R008 决定）
切换的 framing = **"跨场景自适应选优"（R008）**，不是"鲁棒性补丁"。贡献措辞用 R008 锁定句："selecting the locally optimal estimator in 26 of 29 operating points"。切换段以 R008 为准（R009 后限制：crossover 只呈现数据事实不附物理归因）。

## 纪律（和下一步直接相关的约束）

1. **不自造词**（不变量 6）——R011 术语表已锁，P2/P3 直接用，不发明新词
2. **不深挖没把握的物理归因**（R009）——crossover 只呈现数据事实（weak 17.9/mod 16.8/strong 10.7 dB），不解释为什么左移
3. **口径用代码行验证**（D004 教训）——报任何增益前验证加减方向（fair = naive + 1.249）
4. **力度对齐基准表**（R010）——参数/数字/叙事不多不少对齐 A 组
5. **守 FR-22**——写作准备不跑新实验，任何"跑新方法"回 step4a

## P2 要用的 R011 符号表（速查）

| 符号 | 含义 | 参数值来源 |
|---|---|---|
| M₀ | 升幂次数 | =8，`_b11_params.py:36`（B11 L75-77）|
| α, β | GG 形状参数 | `_b11_params.py:78-82`（weak 4.0/3.0, mod 2.5/1.8, strong 1.5/0.8）|
| Δν | 激光线宽 | =10kHz，`_b11_params.py:46`（sat.1553 §4.2）|
| N_blk | 信道块长 | =100，`_b11_params.py:39` |
| N_DFT | 处理块长 | =256，`_b11_params.py:35`（B11 L155）|
| γ | SNR 范围 | AWGN 5-20dB / 湍流 5-26dB，`_b11_params.py:103-104` |
| σ²_θ | PN 方差 | =2πΔνT_s，`_b11_params.py:51`（首次出现注 "= σ²_p in [B11]"）|

## P3 要用的 R011 术语（切换相关重点）

- **estimator switching** = "per-block SNR-driven estimator switching"（首次出现写全称）
- **per-block SNR γ_blk** = 块级 100 符号恒定 h 对应的 SNR（定义见 R011 术语 #30）
- **crossover γ_th** = DA/NDA BER 曲线交叉点 SNR（定义见 R011 术语 #31，只呈现数据不附归因）
- **net SNR gain** = SNR gain net of pilot power penalty（脚注模板见 R011 术语 #34）

## R011 公式清单（P3 大纲要分配到节）

| 公式 | 分配节（建议）|
|---|---|
| 公式 1 DA θ̂_DA = angle(r_p · p*) | §III Method（DA 估计器）|
| 公式 2 NDA θ̂_NDA = (1/M₀)angle(Σr^M₀) | §III Method（NDA 估计器）|
| 公式 3 γ_blk = |h_b|²E_s/N₀ + 切换规则 | §III Method（切换判据）|

GG 模型 + pilot overhead 1.25dB 进 §II System Model（文字 + 数字，不编号公式）。

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] R011 三张表存在且 34 词术语 + 22 符号 + 3 公式（读 R011 目录确认）
  - [ ] DA 代码 `_recovery.py:153` / NDA 代码 `_recovery.py:213,232-233`（读代码行确认公式来源）
  - [ ] M₀=8 在 `_b11_params.py:36`（读参数文件确认）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（不跑实验/不进 Contract/不写正式论文章节）

## 下一轮

D-P2P3：参数+数字呈现（P2）+ 叙事结构（P3）。一个对话可合并完成。产出：参数表（标溯源）+ 数字呈现方案（naive 主报）+ 5 节大纲（标论点/数字/公式分配）。规矩见 writing-campaign-plan.md §2 P2 + P3。
