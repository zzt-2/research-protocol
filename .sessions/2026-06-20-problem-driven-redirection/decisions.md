# Decisions — 问题驱动方法论首次实战验证

> 本专题决策记录。D### 按编号排列，旧决策 superseded 不删。

## D001: Kill Xie et al. 独立性假设候选（验证为孤立建模改进）

> status: active
> date: 2026-06-21
> 取代：无
> 被取代：无
> 依据: 验证 `projects/thesis-fso/worker-tasks/verify-xie-independence.md`（全文 Grep 精确验证 + 636 行 content.md 读完）+ 调研 `projects/thesis-fso/worker-tasks/criticism-aggregation-en.md`（批评汇总层 3 时效检查）
> 触发原话: 无（技术推导，候选验证失败）

### 决策

Xie et al. "Revisiting the Independence Assumption in LEO Satellite-to-Ground Optical Links" (arXiv 2605.09892) 作为 Q# 候选种子被否决，不进入精读做假设审计。

### 核心失败机制

论文判为 (b) 孤立建模改进，不是 (a) 真裂缝：
- **全篇零 DSP 术语**（Grep 精确验证）——不触及估计/均衡/同步任何环节
- "design" 仅指 tip-tilt 角校正因子 η_tt（光机指向抑制参数），不是 DSP 设计准则
- 性能指标只测 outage（**无 BER/capacity**），与 5 次失败同构（信道建模 + 目标=outage 三轴锁死）
- 14 篇引用无 2024+ state-coupled 同类框架——"无人补"成立，但是**信道建模层的无人补，不是 DSP 层的无人补**

### 否决了什么

- 否决"Xie 独立性假设失效"作为 Q# 种子候选
- 否决"从信道建模改进反推 DSP 问题"的路径——建模改进不等于 DSP 假设失效
- 间接否决"凡是被批+无人补的洞就是 Q#"——必须是 DSP 链路相关、产出形态合法、有 baseline 的洞才是 Q#

### 可复用部分

- **baseline 信息可复用**：Ninos 2023 CL / Spirito 2025 JSAC / Helsdingen 2025 JOCN 都是 2019+ 顶刊复合衰落模型，可作为后续"信道建模"相关 baseline 引用
- **方法论教训可复用**：批评汇总的"无人补"信号需要区分"哪一层的无人补"——信道建模层的无人补对 DSP 链路 Q# 无价值。下次做时效检查时必须问"这个洞补不补对 DSP 有没有影响"
- **验证产出可复用**：`papers/arxiv/2605.09892/content.md`（全文已下载）可作为后续信道建模相关引用源

### 具体数据

- 性能偏差：ε=25° 处 BL-dom 2.85×10⁻² / FA-dom 3.30×10⁻² vs 独立假设 1.0×10⁻²（~3×）；ε=30° 处达 ~58×
- 14 篇引用里 2024+ state-coupled 同类工作 = 0 篇
- 全文 DSP 相关术语 Grep 命中 = 0（"channel estimation"/"equalization"/"synchronization"/"carrier recovery" 全 0 命中）

### 影响范围

- 本专题 Q# 候选池：从 2 个（Xie + "Are PLLs dead?"）减为 1 个（"Are PLLs dead?"）
- 精读对象选择：Xie 不进精读
- 方法论层面：批评汇总层 3 时效检查需补"哪一层无人补"维度（记入 S002 方法论迭代待办）

### 来源

S002 步骤 8.1 + 子 agent 验证报告 `verify-xie-independence.md`

## D002: Kill Q#-A（RF-derived FEC 在 FSOC fade 场景失效候选）

> status: active
> date: 2026-06-24
> 取代：无
> 被取代：无
> 依据: 验证 `projects/thesis-fso/S012-verification-audit.md`（8 篇全文独立 grep 核查 + 逐篇立场核实 + Q#-A 重评矩阵）
> 触发原话: "那要不还是A吧？这tm好难搞啊" → D002（用户拍板选项 A：诚实放弃 Q#-A）

### 决策

Q#-A 候选"RF-derived FEC（DVB-S2 / BCH / RS / interleaving）在 FSOC atmospheric turbulence fade 场景失效/不够，需要新的 fade-tolerant FEC"被否决，不进入精读做假设审计。

### 核心失败机制

Q#-A 不是"找不到第三方复现"这么简单——**是孤证 + 2 篇独立反驳**：

- **唯一支持**：#444 qBeam 厂商论文（qBeam 公司全员，厂商夸大动机——要卖自家 fade-tolerant optical modem）
- **弱支持**：附录2020 Nguyen（IJATCSE 低质量期刊，内容方向部分命中但角度不同——做 Polar vs LDPC 对比，不是判 DVB-S2 失效）
- **反驳证据 1**：#80 Kotake（NICT + JAXA 三方独立机构，GEO-to-ground LUCAS 实测）——abstract 明说 "DVB-S2 + interleaving **successfully corrected** burst errors caused by fades due to atmospheric turbulence, **stronger than RS**"。**直接反驳 Q#-A**
- **反驳证据 2**：候选 2 Korevaar（TNO 非厂商 + Celestia STS + ESA 合作，9.8km ground-to-ground OFL feeder 实测）——abstract + conclusion 明说 "RF-derived FEC（DVB-S2 + DDR interleaving）经过设计够用，OFL 退化可忽略，**RF user downlink + RF amplifier 才是真正限制因素**"。**强力反驳 Q#-A**
- **场景错位**：#293 Okamoto（ISL 用 BSC + AWGN，无湍流）/ #430 Dowhuszko（MZM + HPA 非线性，turbulence 折 dB 不建模 fading）
- **角度不同构**：#516 Youssef（LDPC 译码算法 WBF 振荡）/ 候选 1 Elzanaty（IM/DD + PAS 概率整形）——都批 AWGN 假设，但批的是不同 baseline，不是 RF-derived FEC

**判不过判据 A**：baseline（RF-derived FEC）没有真失效（被 #80 + Korevaar 证实够用），所以"改方法真增益"无从谈起。

### 否决了什么

- 否决"RF-derived FEC（DVB-S2/BCH/RS/interleaving）在 FSOC fade 场景失效"作为 Q# 候选
- 否决"厂商论文单独支撑 Q#"——§7.2 硬规则 13（孤证就是孤证）+ 厂商夸大动机不能单独采信
- 否决"继续精读 #444 qBeam 全文找厂商引用的第三方"作为补孤证手段（选项 C 被否）——厂商论文引用本身就是利益相关，不值得作为补孤证手段
- 间接否决"在编码 FEC 地带的 RF-derived FEC 角度继续耗"——这个角度死了

### 可复用部分

- **8 篇论文全文已下载**，可作为后续引用源。特别是：
  - **#80 Kotake** + **候选 2 Korevaar** = "RF-derived FEC 在 sat-to-ground / OFL feeder 够用"的强反证，未来如果涉及 FEC baseline 可引用
  - **#444 qBeam** = 厂商立场参考（不能作为 baseline 失效证据，但可作为"业界有人主张 RF-derived FEC 不够"的对照观点）
- **方法论教训可复用**（已记入 topic-index 结论段 + 悬而未决 #17）：
  1. 核查机制必须应用到所有层级——S012 抓出 PROMPT-005 §1.1 自身误判（候选 1 Elzanaty 全文真实存在但 PROMPT 判"全文没下载"）
  2. 核查是中性的——发现造假要纠正，发现"被冤枉的造假"也要纠正
  3. 部分真实不等于整体可信——批 3 报告 line 编号方向对但数字部分编，必须逐项核查
- **候选 1 Elzanaty**（IM/DD + PAS）虽然不构成 Q#-A 复现，但**批 AWGN 假设的信号方向跟 Q# 同构**——未来如果找"现有方法假设 AWGN（无湍流）"类型的 Q# 候选，Elzanaty 可作为信号源

### 影响范围

- 本专题 Q# 候选池：从 1 个（Q#-A）减为 0 个
- **编码 FEC 地带的 RF-derived FEC 角度**：死
- 精读对象选择：#444 qBeam 不进精读（厂商孤证）
- **下一步**：用户拍板回选地或换子地带（选项 A）

### 来源

S012 独立核查审计 `projects/thesis-fso/S012-verification-audit.md` + 用户原话 "那要不还是A吧？这tm好难搞啊"

## D003: 方法论起点校正——回到 GW Step 3 完整流程（禁止单假设验证 + 标题联想试 MVE）

> status: active
> date: 2026-06-24
> 取代：无
> 被取代：无
> 依据: 调研 `R001-six-kill-commonality-and-gw-step3-correction.md`（6 次 Kill 共性分析 + GW Step 3 完整流程校正）+ 框架原文 `stages/gw-acquire.md` + `stages/gw-read.md` + `stages/glossary.md` 四判据
> 触发原话: "行？a"（用户拍板 D003 + 下一步动作 a：主线选代表性论文给用户审）

### 决策

Q#-A Kill（D002）后，方法论起点正式校正：**回到 GW Step 3 完整流程**——从 683 条 landscape 选 ≥5 篇代表性论文做全量精读（多候选发现），不做单假设验证（Q#-A 模式），不做标题联想试 MVE（前 5 次模式）。

### 核心机制（为什么这样校正）

6 次 Kill 的共性分析（详见 R001）：

- **前 5 次**（N1/③/A3/4b#1/(c)）：Step 3 整个跳过，拿标题联想直接进 MVE，全撞物理天花板（TL-30 已诊断）
- **Q#-A**：Step 3 做了但**变形为单假设反向验证**（先锁定"RF-derived FEC 失效"→找 8 篇验证→判成立与否），不是框架要求的**多候选发现**（精读全部论文 → 提取每篇 M-C-A 矛盾 → 汇总多条 Q# 候选 → 逐条过四判据 → 进 Step 4a）

**6 次 Kill 的真正共性 = 都没走完 Step 3 → Step 4a 的完整发现链条**，差别只在"没读"vs"读了但读法不对"。

### 否决了什么

- **否决"单假设反向验证"作为 Step 3 做法**（Q#-A 模式）：锁定一个假设找证据，baseline 判据没在多候选对比中暴露，在孤证核查中暴露，效率低
- **否决"标题联想试 MVE"作为推进方式**（前 5 次模式）：Step 3 整个跳过，TL-30 已禁
- **否决"凭记忆引用框架"**（TL-31 第 4 次复现，R001 发现 4）：主线曾跟用户说"Step 2 = 找 baseline / Step 3 = 精读 baseline 指出不足"——**错的**。实际 Step 2 = 下载，Step 3 = 精读全部论文产出问题清单，Step 5 = 找 baseline

### 可复用部分

- **Q#-A 验证了三件事**（不白费）：
  1. ✅ 问题驱动起点是对的（起点类型从方法转到了 baseline 失效）
  2. ✅ 精读 + 核查机制能抓造假（批 3 造假 + PROMPT §1.1 误判都抓到了）
  3. ❌ 但单假设验证 ≠ Step 3 完整流程（baseline 判据在孤证核查中暴露，效率低）
- **8 篇精读论文 + 683 条 landscape** 可作为 Step 3 选样的基础（但不是 Step 3 本身）
- **TL-31 第 4 次复现记录**：涉及框架引用时凭记忆不读原文，本次（R001）再次发生，建议 thesis-lessons.md TL-31 追加复现 #4

### 具体校正方向（下一步动作）

**回到 GW Step 3 完整流程**（gw-read.md 原文要求）：

1. 从 683 条 landscape 按覆盖面选 ≥5 篇代表性论文（**不是**为验证某个 Q# 选的，而是代表性论文覆盖不同技术路线）
2. 每篇按 gw-read.md 模板精读，提取 7 个子表，**重点是第 7 项"问题提取"**（M-C-A 三要素 + 逐条过四判据）
3. 综合分析 → 产出**问题清单**（多条 Q# 候选，逐条过四判据）
4. 问题清单进 Step 4a 做可行性 Go/No-Go
5. 通过的 Q# 进 Step 5 确认 baseline

**下一步具体动作**：主线（本对话）从 683 条 landscape 选 ≥5 篇代表性论文，给用户审（用户拍板"主线选代表性论文给用户审"）

### 影响范围

- 本专题：从"Q# 单假设验证"模式转到"Step 3 多候选发现"模式
- thesis-fso 项目：GW Step 3 正式启动（之前整个跳过/变形）
- 方法论层面：D003 是 D002（Kill Q#-A）后的流程校正，不是新方向——是在同一个领域（thesis-fso satellite optical）走完被跳过的 Step 3

### 来源

R001 共性分析 + 框架原文（gw-acquire.md / gw-read.md / glossary.md）+ 用户原话 "行？a"

## D004: 找角度范式校正——对手显式化 + motivation 结构提取 + 证据链强制（框架打磨候选，待验证）

> status: active（框架待验证，未改框架文件）
> date: 2026-06-26
> 取代：无
> 被取代：无
> 依据: 调研 S014（4 篇同门学位论文方向骨架提取 + 6 次 Kill 标准不对称诊断 + FR-21/TL-27 框架原文核查）+ 框架原文 `stages/groundwork.md` §跨 Step 硬门控 / `stages/gw-feasibility.md` §维度 A / §维度 D FR-21
> 触发原话: "究竟是真的难，还是我们不会润色以及找角度？毕竟rf都做了这么多年了，要说窄它也不差，不至于我这个方向更难受？" → D004 起因；"我倾向于，传统baseline作为对手。上界感觉更适合用在某些别的阶段？" → D004-a 对手标准；"我们在想我们这个步骤能否打磨一下？" → D004 框架打磨范围

### 决策

D003 校正"回 Step 3"后，本轮进一步诊断发现：**6 次 Kill 的标准本身存在不对称——Go/Kill 混用了"传统 baseline 对手"和"oracle 上界"两套标准**，导致"能赢传统 baseline 的方向也被 oracle 上界砍掉"的体感。校正方向 = 把同门学位论文的"找角度"范式（场景约束→现有方法具体失效→多维协同方法）显式化进 Step 3，并补两个执行纪律（证据链强制 + 对手显式化）。

**落地方式**：先记 D004 + TL-32，框架文件（groundwork/gw-read/gw-feasibility）暂不改，等 Step 3 正式走一遍验证有效再改。遵守"先测不改协议"（历史教训：框架改早了会污染所有项目）。

### 三条打磨点（待验证后进框架）

**D004-a 对手显式化（框架候选 [FR-25]）**
- Step 3 精读 + Step 4a 维度 A 找 baseline 不足时，对手 **默认 = 传统未优化 baseline**（跟同门学位论文套路对齐——王培森 4.5dB / 李兀祺 0.25-4dB / 弱信号同步 -2.8~-10dB，全是跟传统未优化 baseline 比）
- oracle 上界（FR-21）**仅用于 Step 4a 维度 D 收尾 Kill**（TL-27 原意："省时间的 Kill 工具，不是 Go 工具"），**不作为"能否 Go"的判据**
- Go 标准（找 baseline 不足 + 方法能赢传统 baseline）与 Kill 标准（oracle 上界 <0.5dB 或 MVE FAIL）**分离，不混用**

**D004-b motivation 结构提取字段（gw-read.md Step 3 模板候选）**
- Step 3 精读模板新增"motivation 结构提取"字段，要求每篇精读必须提取：①场景约束（≥2 个，如"弱信号+高动态+SWaP 受限"）②现有方法**具体失效点**（不是"没人做过 X"，而是"现有 M 在 C 条件下因 A 失效"）③作者的方法切入点
- **正例 = 同门 4 篇**：王培森（低轨大动态→时频偏→用户间干扰）/ 李兀祺（SatIoT 开放信道→电磁+多址干扰）/ 弱信号同步（低轨→大多普勒+低 SNR+资源受限）/ 夏兆宇（6G 信号复杂化→识别精度不够）。它们的 motivation 都是规范的"场景三约束→单一环节失效"结构
- **反例 = 6 次 Kill 的标题联想**（"PCS 能不能提升""交织能不能省东西"——起点是方法不是 baseline 失效）

**D004-c 证据链强制（FR-22 子规则候选）**
- 宣称"当前在 GW Step X"必须附带**证据指针**（如"literature_notes.md L120 提取了 M-C-A 矛盾"或"已下载 papers/teacher/ 下 3 篇导师论文"）
- 没有证据指针 = 未走。**本轮 papers/downloads/2026-06-23 误判为导师论文（S013 错误前提）就是因为缺这个约束**——当时若有"证据指针"要求，主线不会把 S011 批 3 核查论文当导师论文

### 核心机制（为什么这样打磨）

**诊断 1：6 次 Kill 标准不对称**
| | 6 次 Kill 的实际用法 | 同门学位论文用法 |
|---|---|---|
| 对手 | ③ 用 oracle 上界 0.09dB 砍；其他几次隐含"理论能拿多少"视角 | 跟传统未优化 baseline 比，赢 2-4dB 就发 |
| Kill 标准 | FR-21 oracle 上界 <0.5dB（严苛） | 无 oracle 上界门控 |

同门在 RF 上"也不窄"（每篇也就几个 dB）照样做出学位论文，关键差别在 **Kill 标准**——同门不问"理论上能不能做"，问"有没有具体笨办法能赢"。FR-21 是好护栏（防 MVE 浪费），但**用在"要不要进 Step 3"层面会误杀能赢传统 baseline 的方向**。

**诊断 2：Step 3 缺"找角度"范式**
框架 Step 3 要求提取"差异化定位/适配性分析"，但字段偏抽象，没告诉 agent "好的 baseline 不足长什么样"。结果 agent 精读时不知道要提取"作者怎么论证现有方法失效的具体结构"，容易退化成标题联想。同门 4 篇的 motivation 结构（场景三约束→单一环节失效→多维协同）正是 Step 3 该产出但框架没显式要求的。

**诊断 3：FR-22 纸面门控挡不住自欺**
FR-22 已写"Step 3+4a 硬门不可跳"+"标题联想=跳步信号"，但 TL-30 原话"连用户都以为在按框架走，实际全程跳步"。本轮 papers/downloads 误判是同一种病（自以为查了证据其实没查）。证据链强制能直接防这类自欺。

### 否决了什么

- **否决"oracle 上界作为 Go 判据"**——oracle 上界只做 Kill 工具（TL-27 原意），不做 Go 判据
- **否决"凭印象/标题联想定义精读产出"**——必须按 motivation 结构字段提取
- **否决"宣称在 Step X 但无证据指针"**——FR-22 加证据链子规则
- **未否决 FR-21 本身**——核查发现 FR-21 定位正确（Step 4a 维度 D 前置门控，TL-27 "省时间的 Kill 工具"），只是过去被误用为 Go 判据。D004 保留 FR-21 原位，只约束其触发条件（Step 3 走完 + 判据 A 成立后才触发）

### 可复用部分

- **4 篇同门方向骨架样本卡**（S014 产出）：王培森 NOMA / 李兀祺 扩频干扰抑制 / 弱信号同步 / 夏兆宇 信号表征——作 Step 3 motivation 结构提取的正例库 + 实验室学位论文范式参照
- **"弱信号同步"与星地激光接收同构**：激光接收同样是弱信号+高动态+SWaP 受限，"捕获→跟踪→载波恢复"三阶段骨架可迁移。但 A3（pilot CPE 同步）已 Kill（D010），不能直接推出"重做同步方向"
- **真难 vs 不会找角度的最终判断**：两种都沾边。"不会找角度"是主因（6 次全跳 Step 3），"物理窄"是次要且未充分验证的假设（只有 ③ MCS 排程规范走到 FR-21 被砍，其余子地带"窄"是未验证假设不能当事实）

### 影响范围

- 本专题：D003 校正"回 Step 3"后的进一步细化——Step 3 不只是"回去读"，还要"用对的范式读"（对手传统 baseline + motivation 结构 + 证据链）
- thesis-fso 项目：Step 3 选样 + 精读时套用 D004 三条打磨点
- 方法论层面：D004 是 D003 的补充（D003 管"回 Step 3"，D004 管"回 Step 3 后怎么读才不重蹈覆辙"）
- **框架文件暂不改**，等 Step 3 走一遍验证 D004-a/b/c 有效后，再决定是否进 gw-read.md / gw-feasibility.md / groundwork.md

### 不在本轮范围（防顺手扩）

- ❌ 不改框架文件（groundwork/gw-read/gw-feasibility）——遵守"先测不改协议"
- ❌ 不做打磨点 4（Step 3 门槛从"≥5 篇"改"≥5 篇且覆盖≥3 种 motivation"）——可能过度设计，本轮不做
- ❌ 不判方向（D004 是方法论打磨，不是方向决策）
- ❌ 不复议 Q#-A（D002 已定）

### 来源

S014（4 篇同门方向骨架 + 6 次 Kill 标准不对称诊断）+ FR-21/TL-27 框架原文核查（thesis-lessons.md L415-446 + gw-feasibility.md L148）+ 用户原话三段
