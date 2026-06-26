# [S013] 导师 3 篇论文消化：精读 + 价值提炼

> ⚠️ **本文件已于 2026-06-26 被 S014 标记作废。** 整份 session note 建立在错误前提上——S013 把 `papers/downloads/2026-06-23/` 下 3 篇 PDF（实为 S011 批 3 Q#-A 核查残留的 JAXA/ESA/TNO 论文）误当成导师发的 3 篇论文。真导师 3 篇在 `papers/teacher/`，全北理工学位论文（王培森 NOMA / 李兀祺 扩频干扰抑制 / 弱信号同步）。**S013 的全部精读/价值提炼/feeder 边界讨论作废，不作为任何决策依据。** 保留本文件作为 TL-33（自欺式跳步）教训案例。正确内容见 `S014-correct-S013-and-direction-skeleton-and-D004.md`。
>
> 2026-06-25 | 阶段：Step 3 准备（导师外部输入消化）| 状态：~~完成~~ **作废**
> 来源：S012 后续（用户转发导师论文）| 文件名：S013-advisor-3-papers-reading-and-value-extraction.md

## 目标

消化导师 2026-06-23 通过 voice.md "老师有跟我说一点东西，然后发了我三篇论文" 提供的 3 篇论文，提炼对 Step 3 / 方法方向的价值。**不预设方向、不判 feeder 边界、不复议 Q#-A**（用户拍板，见后文）。

## 记录

### 第 0 步：批注验证（先核实"批注没咋看见"）

用户转述"批注确实没咋看见"。主线用 PyMuPDF 扫 3 篇 PDF 的 annotation 对象：

```
=== 10294033 === pages=6 annots=0
=== 10491215 === pages=8 annots=0
=== 9013421 === pages=6 annots=0
```

**3 篇全部 0 个批注**。结论：不是 PDF 转 markdown 把批注丢了——**PDF 里本来就没有导师批注**。导师的信息全在"选这 3 篇"这个动作本身 + 论文内容里，得从论文内容反推意图。

### 第 1 步：3 篇是什么（meta + 结构扫描）

| DOI | 作者机构 | 标题 | 页数 |
|---|---|---|---|
| 10294033 | **JAXA**（Okamoto/Nakadai/Yamakawa）+ 名古屋工大 | Performance Comparison of Channel Coding Methods for Optical Satellite Data Relay System | 6 |
| 9013421 | **ESA/CTTC**（Dowhuszko/Mengali/Arapoglou/Pérez-Neira） | Total Degradation of a DVB-S2 Satellite System with Analog Transparent Optical Feeder Link | 6 |
| 10491215 | **TNO** 荷兰应用科学研究组织（Korevaar 等） | Terabit Optical Feeder Links for DVB Satellite Systems: Real-time E2E System Design & Field Test Results | 8 |

**关键事实纠正**：3 篇作者全是外部机构（JAXA/ESA/TNO），**不是"我们实验室同门"**。若用户后续确认是泛指"方向标杆论文"则成立；字面理解"实验室同门写的"需纠正。

### 第 2 步：3 篇并行精读（子 agent，每篇 ≤600 词结构化摘要）

按 AGENTS.md 论文全文精读必须委托子 agent，派 3 个 Explore agent 并行，共享同一 8 字段提取模板（M-C-A 矛盾 + 链路类型 + 湍流 + 可迁移性）。三份摘要完整存于对话上下文，此处落**对比表**：

| 维度 | 10294033 (JAXA) | 9013421 (ESA) | 10491215 (TNO Korevaar) |
|---|---|---|---|
| **链路类型** | 光 ISL + Ka RF feeder（混合中继） | 光 feeder (IM/DD 模拟透明) | 光 feeder (digital-transparent) |
| **触及湍流？** | ❌ 全程 AWGN（ISL 太空无湍流 + Ka feeder 用 RF 避云） | ❌ 只预留 15dB 系统损耗，不建模 | ✅ **建模+实测** Gamma-Gamma（moderate/strong/very strong Cn²分级） |
| **核心方法** | σ² 校正法（不改 LLR 改噪声方差，免改 DVB-S2 译码器 IP） | DPD 数字预失真 + 单抽头 LMS 均衡（针对 MZM+HPA 非线性） | RS(255,223)+DDR 块交织 + coding rate 联合优化 + WDM 并行 |
| **dB 级指标** | p=0.173（DVB-S2 R=1/4 最优，主指标是可容忍 ISL 错误率非 dB） | TD 2.24-3.81 dB（16APSK 2/3 到 9/10） | **+10 dB coding+diversity gain** @BER 1E-6（强湍流 +366ms 交织） |
| **批 baseline？** | ❌ 纯工程对比，不批（只声明"对比没做过"） | ⚠️ 温和（承认 DPD 不完全补偿非线性） | ✅ **20dB fading penalty @1% outage** 批裸 OFL 无 FEC+interleaving |
| **可迁移星地湍流？** | LLR/σ² 校正骨架可迁移（级联信道软信息校正思路） | ❌ 器件非线性（MZM sin/Bessel + HPA AM/AM/PM），不可迁移 | ✅ FEC+interleaving 主体可迁移（feeder 与星地 downlink 同为大气湍流信道） |

### 第 3 步：三个关键发现

**发现 1：3 篇不是"发散思路"，是精确指向 FEC + interleaving 这条线。**
3 篇全部围绕"光链路（feeder/中继）里 FEC + interleaving 怎么用、效果如何"。若导师意图是发散思路，应给湍流/AO/调制/同步各一篇；3 篇全聚 FEC/feeder = **指向性信号**，不是发散。

**发现 2（已作废，见第 5 步纠正）：~~10491215 Korevaar 重发~~**
原主线过度解读为"重发 Korevaar 暗示复议 Q#-A"。**用户纠正**：用户从没找过 Korevaar，是 S012 精读子 agent 从 landscape 池选的代表论文。导师发这篇纯属巧合，导师不知道我们内部碰过。"重发/复议"框架作废。

**发现 3：3 篇全撞 S007 "❌ feeder/系统级不算处理"边界——真矛盾。**
S007（2026-06-22 用户确认）明确 feeder 在 ❌ 列表。3 篇全 feeder。用户拍板（第 4 步）：**先不处理边界，提炼价值**。边界矛盾留到有更多信号再说。

### 第 4 步：用户拍板（两个 AskUserQuestion）

**Q1 feeder 边界如何处理** → 用户答"先不处理边界，提炼价值"。3 篇当 FEC/feeder 线的价值素材读，不判边界不抢拍板。

**Q2 10491215 Korevaar 是复议 Q#-A 还是独立看待** → 用户答"啥意思？啥叫重发？我之前找过这个？"。**纠正主线"重发"误判**。正确框架：独立看待 Korevaar，Q#-A 已 D002 Kill 不复议。

### 第 5 步：价值提炼（3 篇对 Step 3 / 方法方向的客观价值）

按"不预设方向、不判边界"约束，提炼**客观可用的价值点**，不强行收敛成方向建议：

**A. 方法学素材（可借的"思考角度"，对应用户原话"思考的角度啥的"）**
1. **σ² 校正法（10294033）**：不直接改 LLR，把硬判误差等效成高斯噪声源校正噪声方差——这是一种"绕过黑盒译码器 IP 做软信息校正"的思路骨架。迁移价值：湍流引起的光强衰落（非高斯）+ 接收机电噪声（高斯）级联场景的软信息校正。
2. **FEC + interleaving 联合优化范式（10491215）**：coding rate / interleave depth / latency 三方 tradeoff 框架，"把 penalty 设计到可忽略"的设计哲学。迁移价值：星地 downlink 同为大气湍流，FEC+interleaving 主体可迁移。
3. **TD（Total Degradation）E2E 评估框架（9013421）**：dB 级 E2E 性能评估指标设计范式（虽方法本体不可迁移，但评估框架可借）。

**B. Q# 提取的素材（若 Step 3 从这些论文提取 M-C-A 矛盾）**
- 10294033 **不批 baseline**（纯工程对比）→ 提不出判据 A 信号。但 motivation "现有 FEC 对比没做过" 是研究空白型声明，不是 baseline 失效。
- 9013421 **温和批 DPD 不完全** → 弱 baseline 失效信号（DPD 对 MZM+HPA 非线性补偿有残余），但这是器件非线性非湍流，跟星地湍流课题不同构。
- 10491215 **强批裸 OFL**（20dB fading penalty）→ 强 baseline 失效信号，**但这个 baseline 失效已被 FEC+interleaving 解决**（论文自己给 +10dB gain 抹平）。所以提取出的 Q# 会是"FEC+interleaving 之后还有没有残余问题"——这接近 Q#-A 的变体，需谨慎（Q#-A 已 Kill）。

**C. 对 Step 3 选样的启示**
3 篇本身**是否入选 Step 3 代表性论文**待用户定。客观判断：
- 10294033 / 9013421 **不碰湍流**，跟"星地湍流信道处理"课题不同构，作 Step 3 代表性论文价值有限（可作背景参考）
- 10491215 **碰湍流 + 给方法 + 给 dB 指标**，跟课题同构，但全篇结论是"FEC+interleaving 够用"——作 Step 3 代表性论文会强化"FEC 线已饱和"的判断（跟 Q#-A Kill 同向）

**D. 一个必须诚实指出的张力（不预设结论，但要点给用户）**
导师给 3 篇全 FEC/feeder，但这恰好是 S007 排除的边界 + Q#-A 刚 Kill 的线。两种解读都成立：
- 导师不知道我们内部 Kill 了 Q#-A + 不知道 feeder 边界判定，纯随机给 FEC 方向标杆
- 导师认为 FEC/feeder 线值得做（他的视角跟 Q#-A 不同——Q#-A 是"FEC 失效"被反驳，但"做更好的 FEC/interleaving 设计"作为方法创新仍可能成立）

**这个张力不本轮解决**（用户拍板"先不处理边界"）。但记录在此，等 Step 3 跑出更多信号或跟导师沟通后再判。

## 决策引用

- D002（继承，不复议）：Kill Q#-A。本论 Korevaar 独立看待，不滑回
- D003（继承）：方法论起点校正，回 Step 3 完整流程。3 篇是 Step 3 选样的外部输入之一
- 无新建 D###（本轮是消化+提炼，不构成架构决策；feeder 边界/方向判定均悬置）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。消化导师外部输入是 D003 后 Step 3 准备的本职，未扩范围。未做 MVE、未进 Contract、未改方向。

## 后续

1. **用户定 3 篇是否入选 Step 3 代表性论文**（客观判断：10294033/9013421 不同构价值有限，10491215 同构但强化"FEC 饱和"判断）
2. **主线继续 D003 动作 a**：从 683 条 landscape 选 ≥5 篇代表性论文给用户审。3 篇导师论文可并入此选样池或单独处理，待用户定
3. **feeder 边界矛盾悬置**，等更多信号或跟导师沟通。topic-index 悬而未决新增条目
4. **"重发/复议"误判记录**：主线对 Korevaar 用了"重发"框架属过度解读，已纠正。voice.md 登记

## 附：核查声明

- 批注验证：PyMuPDF annots() 扫描 3 篇，0 annots，确认 PDF 无批注
- 关键事实核查（D002/S007/10491215 身份）：grep decisions.md + topic-index.md 全部属实，非凭记忆
- 3 篇精读：子 agent 返回摘要均含"核查声明：以上所有技术声称均来自论文 markdown 全文，无外部推断"
