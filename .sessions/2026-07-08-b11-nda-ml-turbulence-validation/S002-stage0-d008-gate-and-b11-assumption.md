# [S002] 阶段 0.1 D-008 耦合门控 + 阶段 0.2 B11 行 33 假设核查

> 2026-07-08 | 阶段: B11-Q2 工作对话 1（阶段 0.1-0.2）| 状态: 完成，交主控对话/用户决策 INVARIANT 11
> 2026-07-08 续接：用户提示"早就讨论完 bug 了且有新情况"，子 agent 盘点 + 主线核查 step4a voice.md/H006 发现老师反馈遗漏，补记 §"续接发现"

## 目标

执行阶段 0.1（D-008 耦合依赖门控核查）+ 阶段 0.2（B11 行 33 假设核查），不写代码。守 profile 第 9 次"急于推进"防线。

## 记录

### 阶段 0.1 D-008 耦合依赖门控（INVARIANT 11，最高优先）

**核查方式**：派 Explore 子 agent 读 D-008/D-009 决策 + grep 代码 + 核查 sandbox 结果，主线独立 grep 交叉验证（不变量 10 中性双向）。

**核查发现（4 项）**：

1. **D-008 双 bug 未修进 common/_recovery.py**（仍等权版，status `pending_fix`）
   - 主线 grep 确认：L213 `raised = rx**M0`（未归一化，Bug 2 在）+ L232 `np.angle(raised.mean())`（等权，Bug 1 在）+ 全文无 `mag/yn/w*yn` 加权标记
   - H006 明示"不要改 common 补加权 bug 修复"，标 pending 老师反馈

2. **D-009 sandbox 已跑完加权修复版三方对照，结论：加权修复版 vs VV 仍全场景持平**
   - sandbox 文件真实存在（`explore/nda-awgn-tracking-sandbox/_ml_weighting_results.json` 7/7 16:46，meta 标"修 D-008 Bug1+Bug2"，加权公式 `yn=(rx/|rx|)^M0; w=|rx|^2`）
   - ML 加权收益：11 扫描点加权 vs 等权 BER 差 ≤1.7%（D-009 L384）
   - NDA-ML vs VV：10kHz 全场景 |rel|<5%（D-009 L385/449）
   - 主线独立核查 JSON 原 BER 确认数字属实

3. **NDA-ML 方法方向 X/W pending 用户，且基本堵死**
   - W（segmented+高线宽）被层 4 排除（VV Nw=16 反超）
   - X（改进 VV）被打问号（VV 调参就赢 NDA）
   - 专题 status dormant

4. **vs DA-ML 主结论有效**（+1.35~2.5dB 下行 / +2.48~3.07dB 上行），不依赖 ML 加权

**🔴 核心发现（改变 B11-Q2 性质）**：
B11-Q2 前置条件的核心前提——"vs VV 持平是 bug → 修复后应拉开"——**已被 D-009 sandbox 推翻**。加权修复版跑出来仍全场景持平，ML 加权（B11 核心）在单载波时域全线无用。

**对 INVARIANT 11 的影响**：原 INVARIANT 11 设计前提（等 D-008 修复后 vs VV 会拉开）不成立。但 B11-Q2 的真增量锚（vs DA-ML +1.35~2.5dB）不受 D-008 影响——因为 B11-Q2 baseline 是 DA-ML 不是 VV。

**主线判定**：按原 INVARIANT 11 字面（D-008 未修 → 禁跑 sandbox）维持。但实质"D-009 已证加权无用"，需用户拍板是否重新框定。**本轮不拍板**（推翻不变量必须重新讨论），记录发现交主控对话 + 用户。产出 `explore/b11-nda-ml-turbulence-validation/_d008_dependency_check.md`。

### 阶段 0.2 B11 行 33 假设核查（INVARIANT 13）

**核查方式**：主线读 B11 锚全文（`papers/doi/10.1109_lpt.2024.3523478/content.md`）+ grep 全文湍流/衰落/信道模型关键词。

**核查结论：仿真简化（不是物理假设）**：
- B11 全文**未建模 FSO 湍流信道**（grep turbulence/fading/gamma-gamma 全文仅 L15 引言 + L33 假设；无信道模型实现）
- B11 仿真信道 = AWGN + Wiener PN（L51 明示），无衰落项 h(n)
- L33 "totally compensated" 是**信号模型简化假设**（数学上排除变量让 ML 推导聚焦 STO+CPE），不是工程可行性论证（无 AO/ATP 补偿方案内容）

**对 B11-Q2 的意义**：B11-Q2 加湍流验证是**真实物理缺口**——B11 声称适用于 FSO 但没测过湍流，B11-Q2 补这个维度。产出 `explore/b11-nda-ml-turbulence-validation/_b11_assumption_audit.md`。

**残留注意**：B11-Q1（step4a D005）其实已跑过湍流（weak +1.20/moderate +1.92dB）。B11-Q2 不能只重复，需在阶段 0.4 明确新验证维度（如 vs VV 湍流鲁棒性对照 / deep fade 行为分析）。

## 决策引用

- 无新建决策（本轮是核查 + 记录，未达 D### 决策门槛——INVARIANT 11 重新框定是主控对话/用户的事）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.2 核查，未写代码未进 sandbox，守 INVARIANT 6 + profile 第 9 次防线）
- 守 3 步上限：本轮 2 步（①报到+读必读清单 1-7 ②阶段 0.1 + 0.2）
- 守核查机制中性双向：子 agent 产出 + 主线独立 grep 交叉验证

## 后续

### 🔴 需主控对话/用户决策（最高优先）

**INVARIANT 11 重新框定**——D-009 已证加权修复版 vs VV 仍持平，原前置条件"等 D-008 修复"是等一个不会到来的结果。两个选项：
- **选项 A（保守）**：维持 INVARIANT 11 字面，D-008 common 修复前不跑 sandbox
- **选项 B（重新框定）**：D-008 不再是 sandbox 门控（加权已证无用），B11-Q2 sandbox 用等权版验证"湍流下 NDA-ML vs DA-ML 是否保持 +2dB"

**建议选项 B**——因为 B11-Q2 的真增量锚是 vs DA-ML（不是 vs VV），D-008 双 bug 只影响 vs VV 对照不影响 vs DA-ML。但这是不变量修改，必须用户拍板。

### 阶段 0.3-0.6（新对话，不依赖 D-008 决策）

- 0.3 架构定性（前馈 ML 不撞 D006，阶段 0.1 已顺带确认 _recovery.py 是前馈闭式无环路 TF）
- 0.4 公平对照框架（baseline DA-ML，需明确 B11-Q2 vs B11-Q1 D005 湍流结果的新增量维度）
- 0.5 参数真相源（湍流 Cn²/σ² + 线宽，继承 common，标文献来源）
- 0.6 文件组织规约

### 阶段 0 做完后

- 若用户选选项 A：等 D-008 common 修复（可能不会来）
- 若用户选选项 B：进 sandbox（NDA-ML 等权版 vs DA-ML 在湍流下三方对照）

## 续接发现（2026-07-08，用户提示"新情况"后子 agent 盘点 + 主线核查）

用户提示"早就讨论完所谓 bug 了，而且有些新情况"，派子 agent 盘点 step4a 专题全貌 + 主线独立核查 `step4a/voice.md` + `H006`，发现两件遗漏：

### 遗漏 1：D-008 bug 讨论早已闭合（非 pending_fix 等修）

**我 S002 §阶段 0.1 的 framing 需修正**：D-009（含层 4 最终定论，active 不可推翻）已闭合 bug 讨论——加权修复版 sandbox 跑完，结论"加权修复版仍 vs VV 全场景持平（ML 加权单载波时域无用），唯一真增量 = vs DA-ML +1.35~3.1dB"。D-008 status 字段虽仍是 `pending_fix`，但实质是"修不修都跟 VV 持平，pending 老师反馈但实质 dormant"（H006 债务表 L73）。**不是"待修"，是"已证不需修"**。

我 S002 给的 A/B 选项方向对（选项 B：D-008 不再是门控），但理由应补强：不是"等不到修复"，是"D-009 已证修复无意义 + D-008 代码层 pending 老师反馈但讨论闭合"。

### 遗漏 2：🔴 老师反馈已到（2026-07-08，step4a voice.md L60-61）

**这是我必读清单（H001/PROMPT-001 第 2 项只列 decisions.md）的盲区——voice.md 没列进必读，导致漏了方向性信息**。老师两件反馈：

1. **"新方法不是要求全能，是在某一实际需求场景下的特长"** → 重定判据。之前 NDA-ML 纠结"算法层全面超 VV"是错 framing。老师要的是"某一实际需求场景下的特长"，不要求全能。
2. **"对比参考文献请单独发给我。要求:近年 transactions 水平"** → TODO 未完成（COMPARISON_REFS.md 有但需核"近年+Trans"双满足 + 单独整理发老师）。

### 对 B11-Q2 的影响（重大利好）

老师"特长场景"判据直接解套 B11-Q2 的 INVARIANT 11 纠结：

- **原 INVARIANT 11 纠结**："等 D-008 修复 vs VV 拉开" → 追错的目标（D-009 已证 VV 调参就赢，永远拉不开）
- **老师判据下**：B11-Q2 的"特长场景"= 湍流下 pilot-free 鲁棒性（对照 DA-ML），不是"超 VV"。vs VV 持平根本不是要追的目标
- **主线初步解读**（step4a H006 L26-28）："特长场景"可能是**上行强湍流 pilot-free 鲁棒性**（vs DA 上行 +2.48~3.07dB 比 VV 持平更值钱）。**但这不能替老师解读，需用户确认**

### 修正后的 INVARIANT 11 重新框定理由（比原 S002 更强）

原 S002 选项 B 理由："D-008 不再是门控，因加权已证无用"。
**补强理由**（老师反馈加持）：
1. D-009 已证加权无用（代码层修不修无关紧要）
2. 老师"特长场景"判据下，B11-Q2 增量锚是 vs DA-ML（pilot-free 鲁棒性），不是 vs VV
3. D-008 双 bug 只影响 vs VV 对照，不影响 vs DA-ML（D-008/D-009 均确认）
→ **B11-Q2 sandbox 用现有等权版 NDA-ML 验证"湍流下 vs DA-ML 是否保持 +2dB"，无需等 D-008 修复**

### 新增待办（转主控对话/用户）

1. **老师"特长场景"判据解读确认**：主线初步解读"上行强湍流 pilot-free 鲁棒性"是否对？需用户确认（不能替老师解读）
2. **INVARIANT 11 重新框定拍板**：选项 B（建议，老师判据加持）vs 选项 A（保守字面）
3. **对比参考文献发老师**（step4a 遗留 TODO）：核 COMPARISON_REFS.md "近年+Trans" 双满足 + 单独整理（不在 B11-Q2 范围，但 step4a dormant 遗留需有人接）

## 决策引用

- 无新建决策（本轮是核查 + 记录 + 续接补充老师反馈发现，INVARIANT 11 重新框定 + 老师判据解读都是主控对话/用户的事）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.2 核查 + 续接补遗，未写代码未进 sandbox，守 INVARIANT 6 + profile 第 9 次防线）
- 守 3 步上限：本轮 3 步（①报到+读必读 ②阶段 0.1+0.2 ③续接盘点补老师反馈）
- 守核查机制中性双向：子 agent 产出 + 主线独立 grep/read 核查（voice.md + H006 原文）
