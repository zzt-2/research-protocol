# [R007] SOP 极化锁定跳变针对性方法缝隙验证 — B 类真方法空白（非机制命名空白），但带 3 项风险

> 2026-07-14 | 关联：专题 2026-07-10-dual-pol-osl-groundwork / D014（SOP 串扰真因）+ D026（Q-DP3 Kill）+ S020（方法层复盘）

## 调研问题

**核心问题**：S020 复盘确认 BER 真因 = D014 SOP 驱动恒模代价极化锁定跳变（2×2 蝶形 CMA 收敛后因 SOP 持续旋转，权重跳到混淆 X/Y 次优解，BER→0.5）。PROMPT-011（D016）已查通用恒模多解（A 类，静态歧义）确认成熟。"FSO SOP 极化锁定跳变针对性方法"这个精确角度（B 类，动态跳变）是真空白，还是只是术语差异（机制命名空白）？

要回答 3 个子问题：
- **Q1**：B 类缝隙是真空白吗？还是只是术语差异？
- **Q2**：B 类邻近文献的解法是什么？是否真能解决动态跳变？
- **Q3**：缝隙如果成立，方法的可能形态是什么？（不判 Go/Kill，只列举）

## 检索执行

**英文**（tools/search，7 查询）：继承 S020 子 agent 5 查询（94 条命中）+ 本轮补充 2 查询（lock-swap 10 条 / migration 13 条）。存档 `search-archive/2026-07-14/` 共 9 个 JSON。
- 查询覆盖：`CMA butterfly convergence swap/flip polarization`、`CMA locking instability / convergence instability dual-pol`、`polarization demultiplexing CMA dynamic/time-varying SOP tracking`、`PMD CMA tracking singularity optical`、`polarization SOP CMA saddle point/local minimum/wrong solution`、`polarization lock / lock swap / tributary assignment CMA`、`convergence point migration / solution migration CMA polarization`
- 关键词覆盖了任务书要求的全部术语维度：singularity+dynamic、polarization lock/lock swap/tributary assignment swap、CMA tracking failure+SOP、convergence point/solution migration

**中文**（tools/blit --source cnki，2 查询）：`双偏振 CMA 极化锁定跳变`、`偏振解复用 CMA 跟踪失效 SOP`。**两次均完全无关**（CNKI 返回的全是"中国气象局 CMA 天气模式/极端降水"等气象领域内容——"CMA"在中文检索里指 China Meteorological Administration，术语歧义）。**中文光学通信学位论文层面 0 有效命中**，是工具局限性非真空白证据（中文需用更精确术语如"恒模算法 偏振 解复用 收敛"重试，或查万方/IEEE 中文标题）。

## 发现

### Q1：B 类是真方法空白，非机制命名空白

**去重后约 117 条唯一命中**（英文 94 + 本轮补充 23 + 跨查询重复），预分类（基于 title+abstract）：

| 类 | 数量 | 含义 |
|---|---|---|
| **B 类（保留 CMA 攻收敛后动态跳变）** | **0** | 没有任何一篇专题方法 |
| **B'类（保留 CMA 改跟踪速度/鲁棒性，但未提收敛点跳变）** | 3 | Suzuki 2022 / Qiu 2026 / Cojocaru 2026 |
| **边界类（整体替换 CMA 或仅分析）** | 22 | EKF/Kalman 10 + VAE/ML 2 + Stokes 3 + pilot 2 + 混合 2 + 分析 3 |
| **A 类（静态收敛歧义解法）** | 8 | two-stage/CA-CMA/singularity-avoidance/VAE bootstrap（PROMPT-011 已确认成熟） |
| 无关丢弃 | ≈84 | 光纤 PMD 静态补偿/RF MIMO/天线设计/单偏振/非线性补偿 |

**B 类精确判据**：针对"CMA **已收敛正确后**，因 SOP **持续旋转/时变**，权重**跳到混淆 X/Y 的次优解（polarization lock swap）**"提出"保留 CMA、专攻此动态跳变"的方法（检测+恢复 / 预防性约束 / 混合 SOP 跟踪补偿）。

**检索结论**：**B 类（按精确判据）= 0 篇专题论文**。这是真方法空白，不是术语差异——因为：
1. **术语维度全覆盖**：singularity/dynamic/SOP/lock swap/tributary assignment/migration/saddle point 全查过，无遗漏
2. **邻近文献全部"绕开"了 B 类**：要么整体替换 CMA（边界类 EKF/Kalman 10 篇 + VAE 2 篇 + Stokes 3 篇），要么保留 CMA 但只攻"跟踪速度/鲁棒性"不提"收敛点跳变"（B'类 3 篇），要么攻静态奇异点（A 类 8 篇）
3. **没有"机制命名空白"特征**：如果是机制命名空白，会有论文做了等价工作只是叫别的名字。但 B'类 3 篇的 abstract **明确不提 convergence point migration / lock swap**（深查见 Q2 证据），说明它们解决的是不同问题（跟踪速度，非收敛点跳变）

### Q2：邻近文献解法形态——全部不"保留 CMA 攻收敛后跳变"

深查 5 篇最相关论文（S2 API abstract 核验，守 FR-26）：

| 论文 | 目标问题(Q1) | 解法形态(Q2) | 触及 lock swap?(Q3) | 场景(Q4) |
|---|---|---|---|---|
| Suzuki 2022 多线程CMA | c 纯跟踪速度 | ii 多线程并行(保留CMA) | **否** | 光纤接入网 ~2 krad/s |
| Qiu 2026 AS-CMA | c 跟踪/鲁棒 | ii 自适应符号步长(保留CMA) | **否** | 光纤CV-QKD 10-43 Mrad/s 雷击 |
| Cojocaru 2026 软判MCMA | c 跟踪+稳定性权衡 | ii 软判+步长(保留CMA) | **否** | 光纤多跨段 速率未明示 |
| Yi 2021 NPCA（最近邻） | **a 静态奇异点**+c | **i 整体替换 CMA→NPCA** | **间接**(singularity 非 swap) | 光纤 1-5 Mrad/s |
| Zhao 2024 光域SOP+CMA | c 跟踪速度 | iii 混合(CMA+光学跟踪) | **否** | 光纤 50-170 krad/s |

**关键判断**：
1. **B'类 3 篇（Suzuki/Qiu/Cojocaru）保留 CMA 但攻"跟踪速度/鲁棒性"，明确不提收敛点跳变**。它们的失效模型是"SOP 变太快跟不上"（连续跟踪滞后），**不是 D014 的"收敛正确后权重跳到次优解"**（离散跳变）。两者机制不同：前者是连续相位/系数滞后，后者是恒模代价多解的跳变。
2. **Yi 2021 NPCA 是最危险的邻近占点**：它明确提"void the singularity problem in CMA"，与 lock swap 同源（都是恒模代价多解）。但 (a) 它**整体替换 CMA 用 NPCA**（非保留 CMA），(b) 针对**静态收敛奇异点**（非收敛后动态跳变），(c) 测的是 **1-5 Mrad/s RSOP 跟踪速度**（非锁定交换 BER）。**它证明了"恒模多解"问题被注意到过，但解法是替换 CMA 不是攻跳变**。
3. **边界类"整体替换 CMA"是主流路线（10 篇 EKF/Kalman + 2 VAE + 3 Stokes）**：这恰恰是缝隙被"绕过"的证据——学界对动态 SOP 的答案几乎全是"用 Kalman/VAE/Stokes 换掉 CMA"，几乎无人"保留 CMA 专攻收敛后跳变"。

**回答 Q2 核心问题**：
- 邻近文献的解法**整体替换 CMA**（EKF/Kalman）或**保留 CMA 但攻跟踪速度**（B'类），**都不直接解决"收敛后 SOP 驱动跳变"**。
- "保留 CMA + 攻动态跳变"是**真空间隙**——没有论文做过这件事。

**风险（诚实标注）**：
- 风险1：B'类改步长/多线程（Suzuki/Qiu/Cojocaru）虽不提 lock swap，但**可能顺带缓解跳变**（更快跟踪 = 更少跳）。这是审稿人最可能的 attack："你说的 lock swap，别人改步长不就解决了？" 须 MVE 证明"改步长不解决跳变，只解决连续跟踪滞后"。
- 风险2：CA-CMA 2025（L-ML 邻近，D016/S020 提到的"测常规 CMA 80% 无效收敛"）在**静态测试**下。但其相关性检测机制若在动态 SOP 下也触发，可能顺带防跳变。**CA-CMA 2025 的 80% 数字在静态还是动态下——abstract 未明确，须精读确认**（这是 Q1 边界判断的关键漏洞，标 DEBT）。
- 风险3：Yi 2021 NPCA 虽替换 CMA，但"消奇异点"逻辑若移植到 CMA 约束里（保留 CMA + 加 NPCA 式约束），可能构成"保留 CMA 攻跳变"的隐性占点。须精读 NPCA 约束是否可移植。

### Q3：方法可能形态（不判 Go/Kill，守 FR-22）

基于文献综述 + D014 机制（恒模代价 2×2 收敛点不唯一，SOP 旋转让权重跳到混淆 X/Y），方法可能形态列举（标邻近先例）：

**形态1：跳变检测 + 权重回滚/约束恢复（响应式）**
- 检测收敛点是否发生 X/Y swap（corr(zX,sY) 突增等指标），触发权重回滚到跳变前快照或加约束强制恢复
- **邻近先例**：无直接先例。最接近 = EKF 系列（但它们是整体替换，不是检测+回滚）。R7 冻结（D010）证明"检测到 fade 冻结"无效，但那是检测 fade 不是检测 swap——swap 检测从未做过
- **风险**：D026 证明 R7 冻结无效、压μ更差，但那些是"响应 fade"非"响应 swap"。swap 检测+回滚未被测过，可能有效也可能像 R7 一样无效

**形态2：预防性约束（阻止权重漂到次优解）**
- 在 CMA 代价函数加约束（如保持 corr(zX,sX)>corr(zX,sY) 的不等式约束，或酉/正交约束限制权重跳变）
- **邻近先例**：A 类酉/正交约束（Optimal PolDemux 2010, Nonsingular CMA 2009）针对**静态**奇异点。**动态下加约束防跳变 = 无先例**。CA-CMA 2025 的相关性检测是静态版，动态版未做
- **风险**：约束可能限制跟踪能力（动态 SOP 需要权重持续调整），约束设计非平凡

**形态3：混合方案（CMA + SOP 跟踪补偿，CMA 处理快变、SOP 跟踪器补偿慢旋）**
- CMA 仍做主均衡，外加一个 SOP 跟踪补偿器（轻量，如低频 EKF 估 SOP 旋转矩阵）预处理信号，让 CMA 看到的有效 SOP 变化大幅降低
- **邻近先例**：Zhao 2024 光域 SOP 跟踪+CMA（iii 混合）最近邻——但它用**光学域**硬件跟踪，且目标是"延长 CMA 更新间隔"非"防 lock swap"。**DSP 域混合 SOP 补偿 + CMA 防 swap = 无先例**
- **风险**：与 EKF 整体替换的区分——审稿人会问"你这跟 EKF 替换 CMA 有什么区别？"须论证"CMA 仍是主均衡器，SOP 补偿只是预处理，区别于整体替换"

**形态4（D015 方向回响，须排除）**：修正在线跟踪（让 CMA 在线更新不漂错解）
- 这是 D015 用户曾选的方向，PROMPT-011(D016) 已确认 DD-CMA/酉约束/两级 CMA 等通用方案成熟，直接实现只能算场景复测
- **此形态被 D016 占点，不是新空间**。除非限定为"FSO SOP 专属约束"且不撞 A 类通用解法

## 结论

**核心结论：B 类缝隙成立——"保留 CMA、专攻收敛后 SOP 驱动 polarization lock swap"是真方法空白，非机制命名空白。**

证据链：
1. **术语全覆盖**（7 英文查询覆盖 singularity/dynamic/SOP/lock swap/tributary/migration/saddle point）→ B 类精确判据下 **0 篇专题论文**
2. **邻近文献全部绕开 B 类**：整体替换 CMA（边界类 15 篇）/ 攻跟踪速度不提跳变（B'类 3 篇）/ 攻静态奇异点（A 类 8 篇）
3. **非机制命名空白**：B'类 3 篇 abstract 明确不提 convergence migration/lock swap，它们解决的是连续跟踪滞后（不同机制）
4. **D014 机制有 FSO 特色**：SOP 极化串扰是光通信特有（RF 无极化串扰），lock swap 在 FSO/卫星场景比光纤更突出（S020 判断）

**但带 3 项风险（守 FR-23/TL-04：空白 ≠ 可做，须过四判据 + M-C-A 成立）**：
- **风险1（最危险）**：B'类改步长（Suzuki/Qiu/Cojocaru）可能顺带缓解跳变。须 MVE 证明"改步长只解决连续跟踪滞后，不解决离散跳变"——即 D014 的 SOP×f_G 矩阵中，换大步长能否消除 SOP=4e-7 下的 1.9-7.9× BER 退化（预期：不能，因为跳变是恒模多解驱动非步长）
- **风险2（CA-CMA 2025 边界漏洞，DEBT）**：CA-CMA 2025 的"80% 无效收敛"在静态还是动态下未确认。若动态，则相关性检测机制可能顺带防跳变 → 缝隙被隐性占点。**须精读 CA-CMA 2025 确认测试条件**
- **风险3（NPCA 可移植性）**：Yi 2021 NPCA 消奇异点的约束逻辑若可移植到 CMA（保留 CMA + NPCA 式约束），则形态2 被占点。须精读 NPCA

**最危险的邻近占点排序**（若缝隙进 GW Step 4a 须重点排除）：
1. **Yi 2021 NPCA**（a 静态+替换 CMA，但"消奇异点"逻辑最近邻）→ 形态2/4 占点风险
2. **CA-CMA 2025**（a 静态，相关性检测）→ 形态2 占点风险（须确认动态测试条件）
3. **B'类改步长三篇**（c 跟踪速度，保留 CMA）→ 形态1/2 顺带缓解风险
4. **EKF/Kalman 整体替换主流**（边界，不占 B 但构成"为什么不直接替换 CMA"的审稿质疑）

## 对决策的影响

**不立 Q# 不判 Go/Kill**（守 FR-22——本任务是缝隙验证 R###，地勘/验证阶段不产出 Q# 或 Go/Kill；是否进 GW Step 4a 由主控 + 用户决定）。

**对现有决策的影响**：
- **不新建 D###**（本任务是 R### 缝隙验证，结论"缝隙成立带风险"是给主控的判断输入，不是架构决策）。若主控决定进 Step 4a 评估此缝隙，那时再立 Q# + 走四判据
- **S020 "下一步"的选项1（SOP 缝隙验证）已完成**：缝隙成立 → 新方向有评估空间；但带 3 项风险，不是"空白即机会"（守 TL-04）
- **D026（Q-DP3 Kill）不受影响**：D026 是"压μ救不了 BER"（fade 期间），本缝隙是"收敛后 SOP 跳变"，正交。Q-DP3 仍 Kill
- **D014（SOP 串扰真因）受本验证强化**：D014 的"恒模代价 2×2 收敛点不唯一 + SOP 旋转让权重跳次优解"机制，在文献里没有专题方法攻，这恰恰说明 D014 的机制发现是新颖的（分析层贡献加固）

**主控须决定的下一步（不在本 R### 职责内，仅列出选项）**：
- 选项A：派新对话对缝隙进 GW Step 4a 维度 A0§1 反向论证（"为什么没人做"——守 TL-04/FR-23），重点排除风险1（改步长是否顺带解决）+ 风险2（CA-CMA 2025 动态测试条件精读）
- 选项B：接受低天花板保底（路线 A：Q-CMA-FADE D022 窄域 ML 优势 + 改动1 + 分析层），进 Contract/写作
- 选项C：缝隙进 Step 4a 前先精读 CA-CMA 2025 + Yi NPCA（排除风险2/3 占点），是选项A 的前置

**中文检索债务**：本任务 CNKI 0 有效命中（CMA 术语歧义指向气象局）。若缝隙进 Step 4a，须用更精确中文术语重试（"恒模算法 偏振 解复用 收敛"或查万方/IEEE 中文标题），补全中文文献覆盖。
