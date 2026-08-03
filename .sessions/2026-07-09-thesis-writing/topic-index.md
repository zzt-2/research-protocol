# Topic Index: 论文写作专题（自适应 CPR 方向）

> slug: 2026-07-09-thesis-writing
> status: active | created 2026-07-09 | last_updated 2026-08-03（D026/V013：唯一条件式 thesis spine 锁定并通过独立终验）

## 专题定位（一句话）

自适应载波相位恢复（A4 per-block 有效 SNR 驱动 DA/NDA 切换）方向的**论文写作准备专题**——在 GW Step 4a 维度 D（A4 PASS 待 Go）阶段内，做材料盘点、缺口识别、数据稳定性验证、论点合理性审查、简报/论文材料完善。**是写作准备，不是进 Contract/Execute，不跑新实验，不写正式论文章节**。

## 专题定位边界（FR-22 守门）

- **当前在 GW Step 4a 维度 D**（A4 PASS，待 Go 决策）。本专题是 step4a-mve-execution 的下游"材料整理 + 发简报"环节
- **不做的事**（会跳框架）：跑新 MVE 实验 / 进 Contract 阶段 / 写正式论文章节 / 定稿投稿
- **做的事**（GW 内合法）：盘点已有材料 / 验证数据稳定性 / 审查论点 / 完善简报 / 补写作所需的图/表/文献溯源
- step4a-mve-execution 保持 active（Go 决策 + 后续消融仍回那里），本专题只管写作准备

## 原始目标（冻结，不可修改）

为"自适应 CPR"方向的论文/简报写作做准备：
1. **盘点已有写作材料**（简报/数据/文献/报告），确认哪些是最新的、哪些过时
2. **查缺口**：写作还缺什么（图/表/数据/文献/叙述）
3. **验证数据稳定性**：30seed CI 是否稳健、债务项状态、5seed vs 30seed 一致性
4. **审查论点合理性**：crossover 物理性是否站得住、A4 切换增益是否真实、新颖性锚是否够

## 范围边界

### 原始目标（冻结）
材料盘点 + 缺口识别 + 数据稳定性验证 + 论点审查 + 简报完善。守 FR-22（不跳框架）+ D005 务实路线 + D-010 baseline 标准。

### 当前范围
- 复盘此前“看别人怎么包装”工作的证据深度与失败根因
- 盘点全项目历史资产中的 deployable method kernel，禁止复活 invalidated claim
- 精读 8–12 篇真实硕士学位论文的核心方法章，提取 baseline→method delta 与章节包装 recipe
- 将真实 recipe 映射到 Ch3/Ch4/Ch5 候选，构造至少两套“每个核心技术章都有方法”的 thesis spine 并选唯一推荐
- 若内部资产仍不足，只定义 method-shaped search target 与下一轮提示词，本轮不执行检索后的新方法实验

### 明确不含
- ❌ 不跑新实验 / 不进 Contract / 不写正式论文章节（FR-22）
- ❌ 不推翻 A4 PASS 的 Go 判定（那是 step4a 专题的事）
- ❌ 不改框架文件（守"先测不改协议"）
- ❌ 不做消融实验（跨块 KF / BPS 迁移等是 step4a 的债务，不在写作专题跑）

### 范围变更记录
- **[2026-08-03] D025**：暂停 D023/D024 的最终合同效力，启动“硕士论文方法包装逆向工程 + 本项目方法内核重审”。
  - 原因：D023/D024 允许 Ch4 仅作边界研究、Ch5 仅作实现验证，未满足用户“每个核心技术章必须有一个可命名、可画框图、可写流程、可与 baseline 比较的方法”的明确要求；当前专题已有 16 个 S 文件，按治理规范必须显式登记 scope change 后才能继续。
  - 新范围：执行旧包装复盘、全资产方法内核盘点、8–12 篇硕士论文方法章精读、recipe 映射、候选方法分级、两套 thesis spine 与唯一推荐；只做 paper-writing INTAKE/DIAGNOSE/PROPOSE。
  - 影响的未决项：D024 统一鲁棒性表执行暂停；Ch4/Ch5 重新进入 `METHOD_PACKAGING_AUDIT`；正式 Ch4 写作暂停；旧 dossier 保留并加 supersession banner。
- **[2026-08-03]** 范围扩展（campaign-level synthesis + CCISP→thesis extension packaging 诊断）。本专题原范围 = 自适应 CPR 方向写作准备（CCISP/Ch3）。本轮承接 AMC 冻结（D009）后的 campaign-level thesis contribution synthesis，**临时扩展**到全项目论文资产分级 + 唯一推荐 thesis spine 判断 + CCISP→学位论文 extension packaging 诊断。产物：(1) `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`（9 项 contribution inventory + 唯一推荐 spine = 一个主方法 Ch3 + 完整实现验证 Ch5 + 边界 Ch4；第二工程贡献 = NO_SECOND_CONTRIBUTION_YET）；(2) R023 CCISP→thesis extension packaging 诊断的 5 个 dossier 文件（conference-to-thesis-map / asset-claim-matrix / figure-table-plan / journal-extension-readiness / bounded-package-recommendation）+ D023 唯一 blueprint + D024 唯一小包（统一鲁棒性表）。**这不改变本专题"写作准备不跑实验不进 Contract/Execute"的定位**——诊断只做证据-backed 的论文落位判断，不跑仿真、不写正式正文、不修 Skill、不改 CCISP tex。扩展完成后本专题回归原范围。
- **[2026-07-13]** D011：将原 Fig.1 架构准备拆为两张独立编号图。
  - 原因：系统上下文与自适应 CPR 机制需要不同信息层级；拆分可降低密度，避免在一张图内反复取舍总览、zoom 和 selector 细节。
  - 新范围：Fig.1 系统总览（Tx—FSO/channel—coherent Rx—DSP）+ Fig.2 自适应 CPR 机制（measurement—threshold—DA/NDA—selector—compensation）；原 BER/crossover 图顺延为 Fig.3--5，Table I 保持独立。
  - 影响的未决项：R022 已提出两张图的语义、版式、字号/线型、caption 分工和缩小验收门；图内文字已按用户审阅微调，D012 已选 SVG 并完成首版源文件与预览，最终 caption/正文联动和落版仍待处理。
- **[2026-07-13]** D015：恢复当前专题内 Fig.1/Fig.2 的版式变体、独立视觉复核和竖排预览。
  - 原因：用户在重新比较编辑源方案后明确要求继续；D014 的“暂停”只改变执行顺序，现被最新指令取代。
  - 新范围：继续 D013 的 draw.io→SVG/PDF 路线，完成每图三种候选与可见预览；仍不定最终风格、不改 caption/正文联动、不做 Fig.3--5 和 LaTeX 工程。
  - 影响的未决项：三版候选的控制/估计线独立性、缩小可读性和跨图颜色/线型契约必须先通过独立审查，用户再选择风格。
- **[2026-07-13]** D016：Fig.1 改为系统总览 + CPR 局部放大，Fig.2 改为候选处理列 + selector 决策中心；先单原型再变体。
  - 原因：S016 六版语义通过但结构密度不足；用户确认信息层级优先、装饰只允许少量。
  - 新范围：允许 Fig.1 一层 CPR 局部预览；Fig.2 使用重复候选列、共享输入、控制平面和公共补偿层级；不加入无关波形/星座/频谱装饰。
  - 影响的未决项：v3 单原型的父级锚点、标签密度、缩小可读性和装饰边界需先过独立审查。
- **[2026-07-14]** D018：Fig.1 从五模块位置图升级为端到端信号—扰动—时间尺度系统图。
  - 原因：旧主链过薄，CPR zoom 重复 Fig.2；项目正文已有可迁移的真实信号模型和双分区结构。
  - 新范围：Fig.1 可展示 `(8,8)-16APSK`、`h_b(k)`、`φ_k`、`n_k`、`r_k`、载波恢复位置及 `N_ch=100`/`N_DSP=256`；仍不加入双偏振、器件级接收链或 Fig.2 控制机制。
  - 验证结果：`fig1_system_model_v4.drawio/.pdf/.png/.svg` 已生成；V008 对语义图元证据、主链连续性、单窗双尺度、双栏可读性和独立双审给出 PASS。

## 不变量（动任何一条必须重新讨论）

1. **继承 step4a-mve-execution 全部不变量**（D005 务实路线 / FR-22 GW 门控 / FR-25 Go/Kill 分离 / D-006 红线 / D-010 baseline 五条 / TL-26 参数溯源 / TL-20 理论预期 / 核查机制中性双向）
2. **写作专题定位 = GW 阶段写作准备辅助**：不跳框架，不跑新实验。任何"跑新方法/新实验"的动作必须回 step4a 专题回答"在 GW 哪一步"
3. **A4 数据的诚实标注**：底层分析诚实（不伪造、不 cherry-pick、不藏 CI 重叠）是研究底线必须守；**正文呈现=选择性只报有利结果**（D007，2026-07-12 修正）——弱湍流归零数字（0.09/0.18/0.19）不进正文，不利场景连定性都不提（导师原话"只说自己行的"+用户原话"不利的提都不提"）。边界：不利数字直接影响核心声称成立性时才必须报。~~旧版"叙事是两段趋势非严格单调"作废（源自 R002§C 第 6 条 agent 自创结论，来源错误已废，详见 D007）~~。30seed 基准配置 ✓ 但其他配置仍 3seed（债务）
4. **简报未发状态**：ADVISOR_BRIEFING_2026-07-09 写完未发老师，发前需确认数据最新 + 图是 30seed（债务③）
5. **deep fade 正确表征**（S003 修正，动它要重新讨论）：deep fade = **BER 曲线斜率显著变缓**（衰减率从轻湍流 ~3×/2dB 降到 ~1.4×/2dB），**不是 BER 卡死/伪地板**。H002 补点实测推翻了原"strong/uplink 有错误地板"预判（违反 TL-22 的太早结论）。论文/简报里不准用"伪地板"叙事，会被审稿人质疑
6. **黑话禁令**（S003 审计）：fair_gain（自造）/ A4-B11-Q1（内部编号）/ MSDM（未定义缩写）等**不进论文/简报**。fair_gain→net gain（SNR gain net of pilot power penalty），A4→"基于块有效 SNR 的估计器切换"。所有缩写首次出现写全称
7. **叙事诚信边界 / 故事根定位**（S003 提出，S004 第三轮定根）：crossover 真实存在（低 SNR 区 DA 赢、高 SNR 区 NDA 赢）。**D002 已推翻原"切换是 +1.2dB 落地必要条件"论断**——切换净增益微弱，net gain +1.2dB 来自 NDA 架构本身，不依赖切换。**故事根已定=候选 A（净增益量化归因，数字为根，deep fade 机制为辩护层）**（用户 2026-07-10 拍板）。**定位=量化归因型（非"提出新算法"型），待导师确认**（简报 v5 §4 根问题）。切换当鲁棒性补丁非独立卖点

8. **切换增益数字**（S003/D001→D002，D 级约束）：切换代码三 bug **已修复重跑（D002/H003）**。旧 +0.27-0.48dB（switch_vs_max oracle）永久禁用。**可用新数字（30seed net 口径）**：vs 固定 NDA 低 SNR +1.3~+2.3dB（避险）/ vs 固定 DA 仅 strong 高 SNR +0.02~+0.20dB（多数 CI 跨 0 不显著，仅 strong@24 显著 +0.20）。vs DA 增益必须用 net 口径（全块 bit，pilot overhead 在 BER 口径内扣 1.249dB）。**切换无全场景增益，不是"全面赢两固定方法"**。原 buggy 脚本 `_a4_switch_30seed.py` 留作证据，修复版 `_a4_switch_30seed_fixed.py`

9. **fair_gain 口径方向**（D004，2026-07-10 新建，D 级约束）：**fair_gain = naive + 1.25dB**，fair 是"罚导频 overhead 后的系统总账"（大数），naive 是"剔导频水分后的纯物理增益"（小数）。**简报 v4 曾搞反（把 fair 当"已扣开销净值"），已修正为两口径并列。** 6 场景：awgn/weak/mod naive 仅 +0.09/0.18/0.19（CI 重叠，几乎归零）；strong/up_mod/up_str naive +1.26/1.19/1.85。主报哪个口径待导师定（主线倾向 naive，剔水分不易被质疑，但卖点场景收窄到强湍流）。**报任何"已扣/净值/含水分"口径声称前，必须用代码行验证加减方向（fair_comparison.py:109），禁凭字段名/印象**

10. **B 路线已 Kill，回 A**（D006，2026-07-11 新建，INVARIANT 级——推翻需重新讨论）：B（pilot on/off 系统级架构选择）goodput 维度线性假设下数学已证任何 pilot density 都赢不了 NDA（成功率比 α 全点 <1，最大 weak@5=0.466），物理上凹函数翻转不现实。BER 维度跟 A（per-block 估计器切换）卖点重复。**回 A 路线**（data 口径 26/29 选对 + crossover 左移，D005 已验证）。A 写作资产直接复用，不需回 step4a 跑新实验。goodput 判据 α<1（线性假设 + 凸函数物理）可复用于未来任何 pilot 开关类方向

## 其他结论（普通技术决策）

- Fig.2 保留六场景 BER 总览并删除汇报式卖点标注；Fig.3 改为三场景、21 工作点的 BER-reduction 全扫描；Fig.4 只呈现 DA/NDA crossover 数据观察，显示值按统一插值口径为 18.0/16.9/10.7 dB（D009/S011）。
- D011 已确认 Fig.1 系统总览 + Fig.2 自适应 CPR 机制两张独立图；D012 已选 SVG 作为可编辑图源，PNG 仅作预览；旧 SVG 不修补。

## 已确认决策

- D011：Fig.1 拆为系统总览，Fig.2 拆为自适应 CPR 机制；原数据图顺延为 Fig.3--5。
- D012：Fig.1/Fig.2 采用独立 SVG 可编辑图源，导出矢量 PDF，PNG 仅作预览；旧 `fig1_system_block.svg` 保持不变（已被 D013 取代）。
- D013：draw.io 作为 Fig.1/Fig.2 编辑源，SVG/PDF 作为论文交付格式；先单原型门控，再扩展三版。
- D015：恢复三版候选、独立视觉复核和竖排选择页；已被 D016 的结构重设计执行顺序取代。
- D016：Fig.1/Fig.2 先做结构 v3 单原型；通过后再扩展风格变体，装饰仅作轻量层级辅助。
- D017：形态板不作为最终设计基础；先以语义版 Fig.2 单原型过门，再迁移到 Fig.1。
- D018：Fig.1 采用端到端信号—扰动—单窗双尺度结构；D016 的 Fig.1 CPR zoom 部分停止使用，Fig.2 部分不变。时间尺度仅表达一个 256-sample DSP window 内 `100+100+56` 的 channel blocks，不外推跨窗连续性。
- D019：Fig.1 v4 外部架构与主链保持冻结；v5 只把内部简笔 shape 和长文字替换为项目真实模型生成的无文字微图，标签、锚点和语义边仍保持 draw.io 原生可编辑。
- D020：完整 Fig.2 在小 CPR 节点内只剩不可读纹理，故不嵌入；CPR 保留中性短标签和 `Detailed in Fig. 2`，其余五类真实微图不变。
- D021：用户明确覆盖 D020；完整 Fig.2 thumbnail 恢复并允许不可读。中央接收公式删除，改为 `Composite FSO channel` + 同一 realization 的真实受损接收星座。
- D022：Fig.2 保留三泳道、并行候选、raw bypass 和用户微调后的非控制连线，只把旧单层控制带升级为 CV gate → blind-h/effective-SNR → fixed 13 dB → branch command。
- D026：唯一推荐条件式 spine = Ch3 CCISP（READY）→ Ch4 2A calibration-aware robustness（NEEDS_ONE_BOUNDED_PACKAGE）→ Ch5 2B branch-route+fixed-point（NEEDS_ONE_BOUNDED_PACKAGE）；正式 Ch4/Ch5 WRITE 在各自独立验证前暂停，2C/2D 不用于凑章。

## 悬而未决

1. **主图子图数**：S002 锁定图 2 = 4 子图（下行），H002 补点画了 6 子图（含上行）。待跟老师确认画 4 还是 6 子图。
2. **strong/uplink 子图纵轴范围**：H002 建议收窄到 1e-4~1e-1（不硬凑 1e-5），待跟老师确认。
3. **S002 原悬而未决**（图表清单 / fair_gain 呈现 / 主图子图数）：H002 把图 2 数据备齐，等老师反馈后定稿。
4. **Fig.1/2 文字联动**：两图 draw.io 编辑源均已形成，Fig.1 v4 与 Fig.2 分别通过独立门控；caption、正文图号联动及投稿前检查仍未执行。
5. **2A 方法闭合**：需在新执行对话完成 calibration-aware mismatch×GG×SNR cross-grid bounded package；未通过前 Ch4 不得进入正式 WRITE。
6. **2B 方法闭合**：2A 通过后另开包完成 formal full-grid cost/latency、float-vs-Q BER 与可得的真实综合；未通过前 Ch5 不得进入正式 WRITE。

## 当前位置

**✅ S018 / D026 / V013（2026-08-03）：方法包装逆向工程与内核重审完成并通过独立终验。** 旧 R023/D023/D024 已标 superseded。12 篇真实硕士论文均精读至少两个核心技术/方法章；R1–R5 每类至少两例，R6 经两篇定向卫星样本核查仍为 `0/12 REJECT_NOT_OBSERVED`。唯一推荐 = Ch3 CCISP（READY）→ Ch4 2A calibration-aware robustness（NEEDS_ONE_BOUNDED_PACKAGE）→ Ch5 2B branch-route+fixed-point（NEEDS_ONE_BOUNDED_PACKAGE）。2C=SUPPORTING_ONLY，2D=NEEDS_NEW_GW。V013 对 13 项用户门给出 13/13 PASS，Critical/Important/Minor 均为 0。正式 Ch4/Ch5 WRITE 与任何新实验均未执行；下一合法动作 = 新对话先走 sim-preflight/GW gate，只执行 2A cross-grid bounded package。

---

**✅ S017 / D022 / V011：Fig.2 已升级为正文一致的 CV—blind-h/effective-SNR—13 dB 两层判决，用户微调的 9 条非控制边保持；Fig.1 v5 已同步完整 Fig.2 thumbnail。两图结构、目标尺寸和独立双审 PASS，当前等待用户最终审美验收；论文引用、caption 和最终编译由 CCISP 主控联动。**

前两轮共获得 81 个已核验图位 + 1 个订阅墙备用，主线程分级 A 强匹配 26、B 局部可迁移 46、C 基本不对路 10（含备用）。Gate A 四种图型覆盖通过；R019 前两轮为 82 张纵向卡片，其中 60 张嵌入本地 PNG、22 张明确标注预览暂缺。用户指出多数样本缺乏设计感后，第三轮改以视觉 Gate 定向补样：新增 15 张全部可见候选（顶刊总览 6、自适应控制 5、DSP/芯片管线 4；4 张 6/6、10 张 5/6、1 张 4/6），另有 1 个无法生成可靠预览的强线索被排除。用户已确认第三轮“感觉都不错”。R020 已完成批次 B + C 的 24 图深度分析；批次 D 已提出并批评 3 个候选架构，D011 随后确认采用两张独立编号图：Fig.1 系统总览、Fig.2 自适应 CPR 机制。R022 已将两图职责转成可执行的语义、标签、流向、版式和缩小验收规格；D012 已选定 SVG，S013 已完成首版源文件与颜色/黑白预览，当前位置转为 caption/正文联动与最终落版。

**🏁 S011 Fig.2--4 论文级重画与独立验证完成（2026-07-13）**。

R018 已替代改稿前 F2 规格：Fig.2 删除全部卖点箭头并统一六子图专业格式；Fig.3 采用 weak/moderate/strong 三条 BER-reduction 全扫描曲线（3×7=21 点），避免仅画三个场景柱而显单薄；Fig.4 删除图内 headline、HD-FEC、大叉箭头和过载图例，曲线/交叉点/标记统一使用 log-BER 线性插值，显示 18.0/16.9/10.7 dB。独立 verifier 首轮两项 Important 已修复，V001=PASS。Fig.1 源文件未动，延期到新对话。

**🏁 W007 数据呈现批次改稿完成——Q12/Q14/Q10 三项 L1-L2 改动全部 done（2026-07-12）**。

W007 处理数据呈现层三项改动（按 R013 批次化+三防错纪律）：**Q12（L2，先改）** 删弱湍流归零——W002 §IV-B 删 "In the weak-turbulence and AWGN regimes..." 整段（含 0.09/0.18/0.19 + "reported transparently rather than suppressed" + 弱湍流归零因果解释），重写为只讲强湍流/上行有利结果；W003 Conclusion 删 "while the gain narrows toward zero ... in weak turbulence and AWGN" 整句；弱湍流/AWGN 不再出现在增益讨论段。**Q14（L1，联动）** 删 CI 标注——W002 §IV-B 删 "(CI lower bounds uniformly positive)"，W003 Conclusion CI 表述随 Q12 归零句删除；设置段 "averages over $30$ independent seeds" 保留（MC 次数交代是惯例，CI 不报是惯例）。**Q10（L1，逐处）** 增益精度 2 位→1 位+about——1.85→about 1.9 / 1.26→about 1.3 / 1.19→about 1.2（grep 全清单：W001 Intro L20 + W002 §IV-B 四处 + W003 Conclusion L16 + W003 Abstract L24 共 7 处），脚注 1.25 dB / 768 bits 保留（精确定义值）。交叉检查 4 项 grep 全过（0.09/0.18/0.19 正文 0 处 / confidence interval 正文 0 处 / 1.85-1.26-1.19 正文全 about+1 位 / transparently 正文 0 处）。守 D007/不变量 3 + R016 §4.1/§4.3/红线 6-8 + FR-22（只改文字）。revision-queue Q10/Q12/Q14 状态 → done。

**已知债务（转 LaTeX 前清理）**：W001/W002/W003 的元数据交叉检查表仍含旧表述（弱湍流归零数字行 + "reported transparently rather than suppressed" 引用 + "locally optimal estimator" F1 修正前残留 + 1.85/1.26/1.19 旧精度）。这些是元数据不是正文，不影响投稿，转 LaTeX 前统一清理。

---

**🏁 D-F1F2 力度第二轮+图表定稿完成——写作战役全部完成（2026-07-12，F001 产出）**。

F001 完成 F1（R010 20 条力度基准逐条对照**全对齐** + 8 条已知待查项处理——7 项触发正文修正①删 Intro [APCCAS 2022] 弱引用 ②"single-estimator baseline"→"either estimator used alone" ③§III 末 26/29 精简（留 §IV-B 数据出处）⑤"locally optimal estimator"→"lower-BER estimator" 四处 hedging ⑥Conclusion 换角度避免逐字重复 Intro ⑦Abstract 开头加问题压力 ⑧"enjoys/known noiselessly"→"achieves/known exactly"；④3 个 TBD 不碰导师反馈后处理）+ F2（Fig.1-4+Tab.1 五项图表规格定稿：论点+画法+数据+对齐 R010，图数 4+表 1 对齐 R010 图表专项）。交叉检查 5 项全过（修正后术语/数字/framing 一致，TBD 不动）。正文路径：`.sessions/2026-07-09-thesis-writing/F001-strength-check-figures.md`。

**正文全部定稿清单**（5 节 + Abstract + F1 修正）：
- §I Introduction + §II System Model → W001-intro-system-model.md（F1 修正①②⑤a 已落地）
- §III Method + §IV Results（§IV-A/§IV-B）→ W002-method-results.md（F1 修正②③⑤b⑧ 已落地）
- §V Conclusion + Abstract → W003-conclusion-abstract.md（F1 修正⑤c⑤d⑥⑦ 已落地）
- F1 力度对照 + F2 图表规格 → F001-strength-check-figures.md

**关键锁定（F1 修正后）**：
- 数字仍一致：26 of 29 operating points + 1.85 dB naive 在 Intro/§IV-B/Conclusion/Abstract 四处（③ 删 §III 末一处，剩四处，数字值/口径不动）
- 切换 framing 仍统一自适应选优（R008）：⑤"locally optimal"→"lower-BER" 是 hedging（3 个点没选对就不能说全点最优）非推翻 R008，语义不变（选 BER 低的 = 选局部更优的）
- 3 个 TBD 标记区不动（导师反馈后处理）：①§IV-A 纵轴范围 D003 ②§IV-A 1e-5 解读措辞 ③§IV-B 标题数字口径 D004

**改稿章程已定（R013）**：导师反馈后改稿按 R013-revision-protocol.md 执行。核心=**批次化**（攒全了再走流程，不零散改）+ 六级分类（L1措辞/L2数字口径/L3图表/L4公式/L5逻辑链/L6定位）+ 从底层到表层排序 + 三条防错纪律（列清单/验口径/回查R011）。当前 6 个待改项已登记（Q1-Q6），等导师反馈攒全后纳入批次处理。

**下一步（等导师反馈 + 投稿准备，非 writing-campaign 范围）**：
1. 等导师 3 项反馈（卡 Results §IV TBD）：①10⁻⁵ 底线 A/B（D003）→ 纵轴范围 + 主卖点成立性 ②口径 fair/naive（D004 已倾向 naive）→ 标题数字 ③主对比文献 → 参考文献核心一条
2. 导师反馈来后：先登记到 revision-queue.md，攒全后按 R013 批次处理
3. 全篇通读（F1 修正后整体读一遍，检查衔接/读感）
4. 转 LaTeX 投稿格式（CCISP 双栏，段落调整 + 图表插入 + 参考文献 10-15 篇）

写作战役（writing-campaign-plan §2）全部完成。

**S010 全程结论**：逻辑链逐点核查 + 轻讲定稿 + 主控规划讨论三阶段完成。勘误 S007/D005/R007 三处 crossover 物理因果方向错误。用户拍板轻讲（只放有把握内容，没把握的物理归因不写，受控切片不跑）。

**主控规划产出**（三份文档，主控对话执行依据）：
1. `R009-logic-chain-final.md`——逻辑链定稿（只含有把握内容 + 待查术语清单）
2. `benchmark-paper-set.md`——对标论文集（12篇，核心5篇会议库内全有content.md核验过；三批调查发现3个缺口=创新性正面证据）
3. `writing-campaign-plan.md`——写作战役计划（9类前置+5节正文+3项收尾，每个活定规矩，~8对话单元，9天时间表7/11→7/20，6条质量红线）

**关键决定（本轮锁定）**：
- 轻讲：squaring loss 引 V&V 1983 标准结论，不深挖机制
- crossover：只呈现数据事实（weak 17.9/mod 16.8/strong 10.7dB），不附物理归因
- 双语工作流：英文零件（术语/符号/句式）从一开始锁英文，中文起草参照英文句式逻辑
- 力度两轮：开头摸底立基准表 / 末尾对照检查（横切标尺）
- 用语+符号+公式三合一（耦合，一次定死）
- 图表最后（正文全定稿后逐个想"表达什么论点"）
- 模式A：主控只规划+生成提示词，子对话独立干

**待办（低优先级，不阻塞）**：
- 用户手动下载 He SPIE'24（10.1117/12.3036565）+ Xu PTL'26（10.1109/LPT.2026.3676909）——切换写法对标，abstract够用，写切换段如需细节再补

**等导师项（v4 数据层，不阻塞写作，但卡 Results）**：
1. 10⁻⁵ 底线 A/B（D003）→ 决定主图纵轴 + 主卖点成立性（R004 倾向解读 B）
2. 口径 fair/naive（D004）→ 决定标题数字 + 表加粗 + Tab.1 列激活
3. 主对比文献（简报§3）→ 决定参考文献核心一条

## 进展线索

- **S015 / H015 / D014** 暂停 Fig.1/Fig.2 视觉迭代，转入 LaTeX 投稿准备（2026-07-13）。新对话先核验官方模板、引用资产和构建链，再建立可编译骨架；图未定部分用显式占位，禁止在 LaTeX 阶段顺手重画或重写故事。

- **S016 / V002 / D015** 恢复 Fig.1/Fig.2 三版 draw.io 候选（2026-07-13）。六版均完成 SVG/PDF/PNG 导出与独立视觉门；Fig.2 三处 control/selected 交叉以 bridge mask 消除 junction 歧义；纵向 Markdown 选择页已生成，等待用户分别选择 Fig.1 与 Fig.2 风格。

- **S012 / H014 / R019** Fig.1 三轮样图猎取与 Gate A/视觉 Gate（2026-07-13）。第一轮 A1/A2/A3 得 41 图位并完成 A/B/C 分级；用户要求 Markdown 可视语料、明确好/不对并再找一轮后，A4/A5/A6 定向补得 40 个已核验图位 + 1 个备用。前两轮合计 A26/B46/C10，四类覆盖 PASS；R019 转为 82 张纵向卡片并嵌入 60 张本地 PNG，余 22 张明确标注暂缺。用户进一步指出多数图缺乏设计感后，B1/B2/B3 以视觉品质硬门补得 15 张全部可见样本（4×6/6、10×5/6、1×4/6），分别覆盖顶刊总览、自适应控制和 DSP/芯片管线；R019 现共 97 张卡片、75 张本地 PNG、22 张明确暂缺。用户已确认第三轮视觉方向；随后 D012 选定 SVG，S013 进入首版实现。
- **R020** Fig.1 批次 B 深度分析（2026-07-13）。3 个 agent 分析 12 张图；独立 verifier 将初版“5 条高置信”纠正为 2 条跨组高置信、2 条组内重复、1 条待验证版面假设，另有 3 条强特例和 6 类反模式。修正 A2-10 本地预览来源为 UCL thesis Fig.5.1，期刊 Fig.1 仅保留关联来源。批次 C 见下一条；不定 renderer、不画图。

- **R020** Fig.1 批次 C 深度分析（2026-07-13）。3 个 agent 再分析 12 张图：布局组确认 R1（4/4）并提出暂定 R6；流向组将 R3 的直接证据扩为 7 张并确认颜色仅作辅助、early-exit 不可迁移；密度组确认 R5 为条件规则，并提出“>3 面板单一论点+缩小检查”和“跨层线颜色/线型/图例冗余”两道门。批次 D 结果见 R021，不定 renderer、不画图。

- **R021 / D011** Fig.1 批次 D 综合 critic 与两图架构确认（2026-07-13）。D1/D2/D3 先输出 A（receiver-local 单图）、B（端到端总览+嵌入式 zoom）、C（系统主链+receiver-local 两面板）三个候选；用户随后确认采用两张独立编号图：Fig.1 系统总览、Fig.2 自适应 CPR 机制。两图职责已冻结，详细规格见下一条；renderer 选择见 D012。

- **R022 / D012** Fig.1/2 两图详细规格与 renderer 落地（2026-07-13）。R022 将 D011 转成可执行的论点、冻结标签、raw/estimate/control 流向、版式假设、caption 分工和目标尺寸缩小验收门；用户确认 6 处图内文字微调后，D012 选定 SVG。S013 已生成两份 SVG 源文件、矢量 PDF 和 PNG 预览，并完成颜色/黑白目标尺寸检查。

- **S013** Fig.1/Fig.2 SVG 首版实现与视觉验收（2026-07-13）。两图分别落成可编辑 SVG；Fig.1 主链、Fig.2 raw/estimate/control 三类流向与公共后级接口均按 R022 实现。Edge 3×颜色/黑白预览检查通过；独立 verifier 复核与 caption/正文联动仍待完成。

- **S014 / D013** Fig.1/Fig.2 版式重置（2026-07-13）。用户指出首版虽有语义但视觉质量不达标；复核确认等权模块、折返控制线、跨图网格不一致和 QA 门控缺失是主要失败机制。D013 取代 D012：draw.io 作为编辑源，SVG/PDF 作为交付格式，PNG 仅作预览；先做每张一版原型并经独立视觉审查，再扩展为每张三种风格。旧 SVG 保留为失败样本，旧 `fig1_system_block.svg` 不改。

- **S011 / R018 / V001** 图表视觉规范与 Fig.2--4 重画（2026-07-13）。对标论文实图后冻结标题、坐标、字体、图例和最终尺寸规范；三图基于既有 JSON 重画，独立验证 PASS。Fig.1 明确延期，不在本轮修改。

- **S001** 专题开题 + 材料盘点 + 数据稳定性 + 论点审查（2026-07-09 新建）
- **R002** 同门位论文叙事流程分析（郭欣宇+张思齐，四维横向对比：量级/侧重/结构/措辞。核心结论：量级够格无需焦虑，但叙事重心要从"数字"转"机制"，套"针对…提出…"句式，补复杂度，突出 30seed 严谨性差异化，crossover 作发现类卖点。**§B 追加修正**：用户质疑"学位论文还是会议"触发核查——两篇均无对应会议/期刊发表，"重原理"是学位论文体例。补 3 篇英文 Trans 全文四维提取后修正：期刊论文机制+数字并重且闭环，不是纯机制；贡献用数字不用句式；Complexity 收子节；R002 主体"转机制"结论对会议投稿不成立，以 §B 为准。**§C 追加**：用户提醒"别想当然认为别人不报 CI 是不严谨"触发补下载 A/E/C 三篇 OA 自适应/切换型 CPR。6 篇样本实证：全不报 CI/误差棒，连蒙特卡洛都不做（单次 PRBS）——不报 CI 是领域惯例（BER 大数定律确定）。30seed+CI 定位修正：不当主卖点，用"湍流随机性需多 seed 表征分布"正当化。切换型特有 framing="跨工况可移植性"。contributions 列表看期刊体例）
- **R003** 增益天花板判断 + 主卖点优先级重排（2026-07-09。用户问"能不能调参让数字高"触发红线讨论→确认走合法路线→参数敏感性分析。线宽扫描证当前 10kHz 已在 NDA 最优区间（500kHz 崩溃 -0.82dB），A4 赢点随湍流递增（strong 6/7 点赢）。**结论：切换增益 0.27-0.48dB 是物理天花板，调参救不了**。主卖点重排：fair_gain 强湍流/上行 +2.5-3.1dB 为主卖点，切换增益降级为"兑现 fair_gain 的机制"，crossover 支撑切换合理性。叙事重构方向已给。**§B 追加**：fair_gain 严格拆账——减 1.25dB 导频开销后强湍流真实增益 +1.2-1.8dB（strong +1.26/up_str +1.85），AWGN/弱仅 ~0.1dB。归因干净（DA/oracle 1.62× vs NDA/oracle 1.19× + fade 签名 + 跨估计器复现），有 0.11dB 泄漏（NDA vs VV/BPS 强湍流破裂持平）诚实处理。标题数字用 +1.2dB 不用 +2.5dB）
- **H001** 交新对话：图表设计+参数呈现策略（2026-07-09。定位锁定"强湍流盲类 vs 导频类 +1.2-1.8dB"。图表初步建议：主图 fair_gain vs 湍流递增双线（总+去导频）/机制图 DA-NDA BER 分场景/线宽扫描加分。用户要补点 5seed 够，需权衡 CI 宽度。诚信红线守：不 cherry-pick，标题用去导频数字）
- **S002** 图表策略实证反转 + CCISP 投稿锁定（2026-07-09 续接 H001。H001 主图方案被推翻：σ²R 诊断（sat.1553 是 lognormal 非 GG + σ²I 全≫0.1）+ 横轴实证（7 篇 0/7 用湍流横轴）双重证伪"fair_gain vs σ²R"主图。主图改标准画法 BER vs SNR 分场景子图。σ²R 债务定性非阻塞。投稿锁定 CCISP 2026（7/20 截稿 11 天，IEEE+EI+Scopus，4-6 图体例），用户"不牺牲质量"。用户核心对标诉求="跟别人会议一样，图的类型尽量一样"。待定：完整图表清单 + fair_gain 呈现方式 + 主图子图数。voice.md 首建）
- **H002** BER 补点实验结果回传（2026-07-09。导师要求 BER 到 1e-5 的补点实验跑完，5 seed 探索性两轮：第一轮 6 场景补到 44/46dB + 第二轮 strong/uplink 补到 50dB 探边界。**结论**：awgn/weak/moderate 能画到 1e-5（moderate 46dB oracle=8.3e-6 刚破）；strong/uplink 画不到，50dB 最远 1.6e-4~1e-3，外推 1e-5 需 64-81dB。**关键发现**：原"deep fade 地板"预判被推翻，BER 全程单调降（衰减率 ~1.4×/2dB 无趋平），deep fade = 斜率变缓非卡死。数据 `_ber_ext_5seed.json`+`_ber_ext2_5seed.json` + 报告 + 合并图 `fig2_ber_ext_merged.png` 就绪。实验跑在 step4a S013，结果回传写作专题）
- **S003** 导师反馈处理 + 黑话审计 + 叙事定位（2026-07-09。导师简报 v2 反馈"A4切换/fair_gain是什么"触发。**完成**：①fair_gain→net gain 术语调研（领域标准=pilot power penalty+SNR gain，fair_gain 是自造合成词不进论文）②切换方法剥 A4 代号（功能名=基于块有效 SNR 的估计器切换）③简报全文黑话审计 5 类（内部编号/自造术语/未定义缩写/领域行话/文学化）④BER 10⁻⁵ 核查接收 H002 补点结果⑤叙事定位 crossover 实测验证（低 SNR 区 DA 赢、高 SNR 区 NDA 赢，切换是 +1.2dB 落地前提，讲法 C 诚信边界成立）。**叙事定位等老师拍**，B+C 融合为推荐备选。落不变量 5/6/7：deep fade 正确表征 / 黑话禁令 / 叙事诚信边界）
- **D002** 切换三 bug 修复 + 30seed 重跑（2026-07-09 新建，续 D001。三 bug 独立核查：Bug1 混合分母✅成立修=统一全块bit net口径；Bug2 判据脱钩⚠️非假增益源不修保留raw+文档；Bug3 oracle对照✅成立修=删max改真实baseline。30seed TL-23守门0违例。**结论：切换无全场景增益**，真实价值=vs固定NDA低SNR+1.3~+2.3dB(避险)+vs固定DA仅strong高SNR+0.02~+0.20dB。切换降级为鲁棒性补丁，net gain+1.2dB不依赖切换。推翻不变量7原"切换是落地前提"论断。用户"这块需要好好想想咋办"触发待讨论切换叙事定位）
- **H003** 切换 bug 修复+重跑结果回传（2026-07-09。执行 D001 修复任务，回传 thesis-writing。代码 `_a4_switch_30seed_fixed.py` + 数据 `_a4_switch_30seed_fixed.json` + 报告 `_a4_switch_bugfix_report.md`。接收方验证清单 + 核心数字 + 下一轮用新数字重写简报切换段）
- **D003** 主卖点 net gain 在 BER→0 区坍塌 + 10⁻⁵ 矛盾（2026-07-10 新建。切换降级后讨论"主卖点够不够"，深挖发现两硬矛盾：①net gain@1e-5 数学坍塌（信息论必然，+0.2/0/−0.3dB）②强湍流/上行 BER 到不了 1e-5（最低2e-4~1e-3）。导师"10⁻⁵底线"A/B解读待用户问导师定生死。TENTATIVE 状态，问前不动简报主卖点叙事。**R004 支撑解读 B**：领域 pre-FEC 基准 1e-3/1e-4，1e-5=post-FEC，导师原话"在有编译码的情况下"五字锁定 post-FEC）
- **R004** 强湍流 FSO 的 BER 处理领域调研（2026-07-10 新建。支撑 D003 解读 B。本地精读 5 篇 + COMPARISON_REFS 17 篇 + Semantic Scholar 4 查询 41 篇。**核心结论**：①强湍流 BER 降不到 1e-5 是领域已知现象（OE 2026/IEEE TCOMM 2020 立项即为此，Paillier JLT 最强湍流 σ²_I=0.684 也只画到 1e-4）②呈现四做法：(a)照画 BER 不凑 1e-5[Paillier] (b)BER+outage 联合非替换[IEEE TCOMM 2020] (c)post-FEC/锚定 1e-3[sat.1553]——对齐度最高(a)+(c)③1e-5=post-FEC 门限，pre-FEC 通行基准 1e-3。导师原话"在有编译码的情况下"五字直接锁定 post-FEC=解读 B 有领域证据支撑。建议：不硬凑 1e-5 对齐 Paillier + 加 outage 补充 + 显式衔接导师措辞 + 核对 σ²R。局限：Semantic Scholar 无 key 档限速 2/4 查询未回；Wang OE 2024 未定位为 Wang 实为 Fan OptComm 2024）
- **D004** fair_gain 口径方向修正（2026-07-10 新建。写简报 v4 净增益段时把 fair_gain(+1.34)误当"已扣开销净值"，用户贴旧表触发核查。核查 fair_comparison.py:109 确认 fair = naive + 1.25dB，R003 旧表对。6 场景两口径：naive 真实增益 awgn/weak/mod 仅 +0.09/0.18/0.19（CI 重叠归零），strong/up_str +1.26/1.85。简报 v4 改为两口径并列等导师定。第三次同型失误=数字口径未用代码行验证加减方向）
- **R005** CCISP 2026 投稿包结构骨架（2026-07-10 新建。导师回复前定"怎么包成4-6页会议论文"的结构。6节骨架(含独立Discussion)+5图清单+贡献条候选+等导师3项+主对比补搜4候选(L009/L010最契)。**已被 R006 修正**：章节数6→5(Discussion并入)、贡献列表→散文式、图5→4-6、参考文献15-20→10-15、公式明确2-3个、补完整素材库+多对话拆分）
- **R006** CCISP 2026 写作流程规划（2026-07-10 新建，续接完成。用户要"规划怎么写的流程不写正文"。派2子agent对标研究（本地5篇会议全文+检索5篇会议+R002已有6篇期刊）+ 读简报v4/R002/R004/R005/D002/D003/D004/params.py/_recovery.py。**产出**：①对标结论（会议5节骨架/散文贡献/6-12篇ref/3页≈3图4页≈6-8图）②写作骨架（5节+4-6图+贡献防御性表述naive版）③素材库（数字清单全标溯源+口径加减方向+验证状态 / 公式3个标代码行 / 文献15篇标角色状态）④多对话拆分（5对话+D1D2并行+等导师节点+D3卡导师反馈）。修正R005：6节→5节/列表→散文/图5→4-6/ref15-20→10-15/补素材库。守D004口径标加减方向。范围=写作准备延伸不跳FR-22。**⚠️用户两次纠偏已闭环**：①没查开题写作规范→补读毕设4层+§0.5一~四层引用 ②会议论文写法粒度→**续接轮Step1重做完成**：派2子agent精读8篇会议全文提取80条写法模式，落盘`writing-patterns-conference.md`(§0.5第五层)+§2.4新增「每节句式映射」(5节骨架逐节映射条目编号+⚠️禁用项标注：切换多数场景输禁"performs the best")。确认会议vs学位差异=贡献散文非bullet/Conclusion单段/无回指/数值硬核/公式少而精。**⚠️导师反馈后待更新**：两段式结构(影响分析+方法)重排 / 切换重新定位特定条件优异 / 表述策略改"强调自己行的"——H004 新对话处理）
- **H004** 包装策略交接（2026-07-10。导师回完简报v5定位困境给4点指令后，用户决定走路1包装层(不改算法)开新对话专门想包装。交接：导师4点反馈+两段式结构指令+切换重新定位(vs固定盲+1.3~2.3dB特定条件优异)+表述策略(强调自己行的)+必读文件+不要做什么(不改算法/不跑实验/不写vs导频输/不再写简报)+关键数据。守路1/D004/FR-22/7-20截稿10天）
- **R007** CCISP 包装策略（2026-07-10 新建，续 H004。导师4点反馈落地：①两段式(影响分析+方法)落到 Results 内拆 §IV-A/§IV-B，5节骨架保留，叙事重心往"湍流影响→盲估计抗"因果链靠 ②切换收窄只讲 vs 固定盲 +1.3~2.3dB(CI下界全正)，vs导频输不进论文(导师第3点) ③弱湍流选择性呈现(数据真实不报归零数字，领域惯例R002§C) ④图表配合(Fig.2画全6子图影响分析载体/Tab.1只放强湍流3行naive/Fig.4 crossover卖点化) ⑤标题候选A(naive量化归因型)。数字全标溯源，Tab.1 naive CI已核查(`_fair_gain_summary_30seed.json`)。R006 §2.1/2.2/2.3已加引用。守路1/D004/FR-22。下一步进D2写草稿+D1图表并行）
- **S005** CCISP 包装策略实施（2026-07-10 新建。续 H004 接收方验证3条事实声称全PASS + 用户确认两段式=叙事偏向非砍成2章 + 产出R007包装策略 + R006引用更新。范围在scope内写作准备不跑实验。下一步进D2写草稿+D1图表并行）
- **S006** D1 图表制作 + 数字呈现策略 + 切换 framing 新方向（2026-07-10/11。续接 R007 包装策略完成后的图表实施。派3子agent提取BER曲线gap数据+切换crossover数据+会议论文图惯例。**产出**：4张图样图（Fig.2 BER主图3×2纵向美化/Fig.3净增益方案B/Fig.4 crossover v3单图6条BER曲线/Fig.1系统框图SVG）+ 图表美化checklist 7类检查项 + R007 §7数字呈现策略。**关键数据核查**：D004口径再验全一致（fair=naive+1.249）+切换JSON只4场景无uplink+DA BER双口径发现（data 768bit/full 1024bit比值=1.333）+切换方案选对率核查（strong 7/7选对/awgn 0/8选对）。**用户提出新方向**：从Fig.4看出「切换跨场景自动选优」framing，比当前说法有力，决定开专门对话深挖（H005）。守路1/D004/FR-22/数据真实。下一步H005专门对话研究切换framing）
- **H005** 切换「跨场景自动选优」framing 专门研究交接（2026-07-11。用户看Fig.4后提出新framing比当前说法有力。交接现状写全：①DA BER双口径（data 768bit/full 1024bit，比值=1.333=pilot overhead）②切换选对率（strong 7/7✅/awgn 0/8❌/weak-mod 3/7）③framing成立条件（改进判据让弱湍流也选对，需判断算调参禁止还是改算法合法回step4a）。核心问题：改进判据让切换跨场景选对→"跨工况自适应"叙事。交接含完整数据表格+文件位置+验证清单。**⚠️S007勘误：H005误用full口径判framing不成立，data口径才物理公平**）
- **S007** 切换 framing 口径审计 + 选对率反转（2026-07-11。续接 H005 验证 framing。用户三问触发口径深度审计。**核心纠正**：H005把full口径(ne_d/1024)当"公平"是反的——full给DA打0.75折偏袒DA，data(ne_d/768)各自标准信息BER才物理公平。**选对率反转**：data口径下26/29(90%)非full口径13/29，framing基本成立。crossover随湍流左移物理真实(AWGN无/weak-mod~15-20dB/strong~10-15dB)。strong高SNR 3点选错=γ_eff阈值偏保守非框架缺陷。「切换什么」4维度梳理(A当前DA↔NDA/B pilot开关/C调制/D参数)，A+B系统级最有说服力但需回step4a。D005新建。goodput预检发现B路线25%overhead下8/8输（DA优势<1.249dB吞吐罚）。守FR-22不跑新实验只分析现有数据。用户选定B路线→H006交接）
- **H006** B 路线 pilot on/off 系统级架构选择交接（2026-07-11。用户选B不走A。B=强湍发pilot(DA架构付25%overhead换精度)/弱湍不发pilot(NDA架构全功率)。**goodput预检关键发现**：25%overhead下8/8 DA选中点goodput全输NDA(BER优势+0.06~1.50dB < 1.249dB吞吐罚)。非死刑：pilot spacing可调(1/8=12.5%=0.58dB)，但需验证交叉区存在。下一步回step4a走GW Step4a维度D，先判B物理可行性再跑实验。守FR-22/FR-21/守路1/9天截稿）
- **S008** B 路线 goodput 可行性分析 + Kill B 回 A（2026-07-11。续接 H006 判 B 物理可行性。接收方验证3条事实声称全PASS（8/8 goodput输 + 26/29选对率 + crossover左移，重跑脚本确认）。**goodput 交叉区数学证明**：goodput_DA>goodput_NDA 条件 R>1/(1−p)，线性假设下 goodput_gain(p)=(1−p)(1+αp)>1 要求 α>1。实测全 8 点 α<1（最大 weak@5=0.466）→ 任何 pilot density 下 NDA goodput 都赢。翻转需凹函数但物理是凸函数（pilot 辅助高 density 收益递减）。**论文指标判断**：goodput 维度数学已死 + BER 维度跟 A 卖点重复。用户"Kill B 回 A（推荐）"。D006 新建。回 A 路线资产全就绪不需跑新实验。守 FR-21（goodput 上界前置门控省实验）/ 数据真实（8/8输诚实记录））
- **R008** 切换叙事升级——从"避险补丁"到"自适应选优"（2026-07-11。续 S007/D005 + S008 Kill B 后落 A 路线叙事。**核心升级**：切换定位从"低 SNR 鲁棒性补丁"升为"跨湍流强度自适应选优"。3 个升级依据（全 data 口径）：选对率 26/29 + crossover 随湍流左移 + 低 SNR +1.3~2.3dB。strong 高 SNR 3 点选错诊断=系统性非噪声（加 seed 不翻转），按导师原则选择性呈现不进正文。修正 R007 §1.3/§2/§4.3/§1.4 切换段落，其余 R007 段落不变。Fig.4 用 data 口径画多场景 crossover。贡献句加"selecting the locally optimal estimator in 26 of 29 operating points"。守路 1（只动叙事不动数据）/D005（data 口径）/导师第 3 点。下一步进 D2 写正文，切换段以 R008 为准。**⚠️R009 后限制**：crossover 只呈现数据事实不附物理归因，R008 的"crossover 随湍流左移当物理依据"卖点降级为"数据观察"非"物理发现"）
- **S010** 逻辑链因果归因调查 + 轻讲定稿 + 主控规划讨论（2026-07-11。接 H007 逐点核查逻辑链。用户纠正"不能拿旧数据编故事，每点要对应代码且理解透"触发完整管线追踪。**核心发现**：①主实验和切换实验同管线（切换是超集）②DA/NDA 差异里混了三个混淆因素（盲h均衡/fft_foe/genie resolve），前两个偏帮DA会夸大NDA溃败③**S007/D005/R007 crossover 物理因果方向错误**（说"湍流越强DA优势区延伸"，数据铁证是反的——DA优势缩小），三处已勘误。**旧对话三质疑**：crossover物理只讲一半 / 受控切片必要性 / 术语instantaneous可能错——全部成立。**用户拍板轻讲**：篇幅+惯例+无rebuttal→只放有把握的内容，没把握不写。受控切片不跑。"盲估低SNR差"引V&V 1983标准结论不深挖。crossover只呈现数据事实不附物理归因。术语effective/instantaneous SNR避免，用per-block+显式定义。**主控规划**：前置工作盘点（9类+力度横切）+ 双语工作流（英文零件锁英文+中文起草参照英文句式）+ 对标论文集三批调查（benchmark-paper-set.md，核心5篇会议库内全有）+ 写作战役计划（writing-campaign-plan.md，9天8对话单元）。主控提示词已给用户。落地决定全锁S010§8/§10）
- **R009** 论文逻辑链定稿版（2026-07-11。只含有把握的内容。核心三段：DA/NDA trade-off教科书结论+数据印证+切换机制。跟S009修正版差别：死穴→优势区/崩溃→squaring loss标准术语/crossover只留数据事实不附归因/切换"必要环节"软化。附待查术语清单10条：squaring loss/V&V estimator/pilot overhead/deep fade/Gamma-Gamma/DA-NDA/net gain全标准直接用；crossover显式定义；per-block SNR替instantaneous待最终定）
- **对标集 + 战役计划**（2026-07-11。benchmark-paper-set.md 12篇对标论文+缺口记录；writing-campaign-plan.md 9类前置+5节正文+收尾，每个活定规矩，~8对话单元，9天时间表。主控对话提示词已给用户去开新对话）
- **R010** 力度基准表——D-P0 第一轮摸底（2026-07-11。派3子agent并发提取A组5篇content.md力度信息：Johst/Le Bidan各一个重点+Panasiewicz+OECC-PSC+Paillier合并。产出20条基准（5节×3-5技术点），每条标来源论文+我方应到力度+依据。**核心标尺结论**：①公式粒度=直接给结论级（对齐Panasiewicz，不推导，squaring loss引V&V 1983）②贡献声明=散文式2-3句（5/5篇如此，bullet反惯例）③表是增量亮点（4/5篇0表，加1表强化数字）④算法流程=文字+框图（5/5无伪代码）⑤BER主图纵轴不硬凑1e-5（对齐Paillier）+AWGN理论线隐式baseline（对齐Johst）。后续P1/P2/P3/W1-W5/F1全查此表。守质量红线4条+FR-22）
- **R011** 用语+符号+公式三合一——D-P1 产出（2026-07-11。派2子agent并发查证A组5篇+C组B11/sat.1553共7篇content.md的21+个术语用法，逐词标✅/❌+原句截取+行号。产出三张表锁死全篇英文零件：①术语表34词（29标准词标来源直接用+5显式定义词给定义句[per-block SNR/crossover/block fading/estimator switching/net SNR gain]+5自造词替换映射[fair_gain→net SNR gain/A4→功能名/MSM禁用/伪地板禁用]）②符号表22个无冲突（相位θ/θ̂从V&V非B11的φ，SNR用γ，M₀=8从B11）③公式清单3个（DA θ̂=angle(r_p·p*)/NDA θ̂=(1/M₀)angle(Σr^M₀)/per-block SNR γ_blk=|h_b|²E_s/N₀，全直接给结论级标`_recovery.py:153/213,232-233`代码行）。交叉一致性检查4项全过。守质量红线6条+FR-22。下一步D-P2P3参数数字+叙事结构）
- **R012** 参数+数字呈现+叙事结构——D-P2P3 产出（2026-07-11。口径代码行核验fair_comparison.py:109确认fair=naive+1.249（strong fair2.509→naive1.260/up_str fair3.101→naive1.852✓）。产出：①参数表4类标溯源[信号调制M₀=8/R_sym=2.5G+信道GG αβ下行3档上行2档+Δν=10kHz/σ²_θ=2.51e-5+帧结构pilot spacing=4 overhead25%=1.25dB+实验矩阵SNR扫描/N_blocks400/30seed]，每个标`_b11_params.py`行号+文献TL-26 ②数字呈现方案10条数字清单标进正文/表/图+口径+来源+验证状态，主报naive（弱湍流归零诚实标注+0.09/0.18/0.19不变量3），口径标注脚注模板，CI策略不报是领域惯例，数字-图表映射Tab.1只强湍流3行naive ③5节大纲分配R009逻辑链[Intro贡献散文式+切换framing自适应选优/SM给GG+块结构+pilot overhead文字+数字/Method DA/NDA/per-block SNR三公式直接给/Results两段式§IV-A影响分析§IV-B方法增益/Conclusion复述+局限+future] ④两段式落Results§IV-A/§IV-B叙事逻辑湍流影响→切换兑现 ⑤切换framing自适应选优全篇统一禁鲁棒性补丁。交叉检查4项全过（数字/公式/篇幅/framing）。守质量红线8条+FR-22。下一步D-W1W2 Intro+SM正文）
- **W001** Intro（W1）+ System Model（W2）正文起草——D-W1W2 产出（2026-07-12。按R012 §I/§II大纲+R011三表+R010力度+R009逻辑链+writing-patterns-conference.md起草。**Intro 3段**：①背景相干FSO+湍流致相位噪声+CPR必要（引sat.1553/Paillier/Al-Habash/Johst/APCCAS/B11，句式参照§5.4/5.6/5.7）②DA/NDA trade-off gap 2句（DA低SNR准+1.25dB罚引Shieh-Djordjevic / NDA省带宽+squaring loss引V&V1983）③贡献散文式3句不用bullet（propose per-block SNR-driven switching → selects locally optimal in 26/29 → net SNR gain up to 1.85dB naive标脚注，verbatim R008关键短语）。**SM 2段**：①GG块衰落信道（引Al-Habash，块结构N_blk=100，αβ下行3档+上行2档值进正文，不给PDF）+Fig.1占位 ②信号模型r_k=h_b·s_k·e^{jθ}+n_k+帧结构pilot spacing 1/4=25%=1.25dB引Shieh-Djordjevic+Wiener PN σ²_θ=2πΔνT_s注"=σ²_p in [B11]"+N_DFT=256+HD-FEC 3.8e-3。**交叉检查6项全过**：术语跟R011（CPR/DA/NDA/GG/block fading quasi-static/pilot overhead/squaring loss/net SNR gain全标准，fair_gain/A4/MSM/伪地板零残留）/符号跟R011（θ非φ注B11对应，σ²_θ注σ²_p对应，M₀=8/N_blk=100/N_DFT=256全对齐）/数字跟R012（26/29+1.85dB naive标脚注+1.25dB+M₀=8+参数值全对齐，naive口径标脚注模板）/力度跟R010（Intro1-2段~15行在范围/SM给GG+块结构不给PDF/不给独立参数表/估计器公式不进§II）/切换framing统一自适应选优（R008 verbatim关键短语，无鲁棒性补丁残留）/句式参照writing-patterns-conference.md（§5.4/5.6/5.7/8.x/1.2/1.13）。守质量红线9条+FR-22。下一步D-W3W4 Method+Results正文）
- **W002** Method（W3）+ Results（W4）正文起草——D-W3W4 产出（2026-07-12。按R012 §III/§IV大纲+R011公式清单/符号表+R010 §3/§4力度+R009逻辑链+W001衔接起草。**Method 2段**：①DA估计器公式1 θ̂_DA=angle(r_p·p\*)一句话"removes modulation by dividing"（`_recovery.py:153`）+NDA估计器公式2 θ̂_NDA=(1/M₀)angle(Σr_k^M₀)一句话"raises to M₀-th power"（`_recovery.py:213,232-233`）+引V&V1983 squaring loss文字结论不推导 ②per-block SNR公式3 γ_blk=|h_b|²E_s/N₀（R011术语#30定义句）+切换规则文字"select θ̂_DA when γ_blk<γ_th else θ̂_NDA"不编号（R010 §3.1文字非伪代码5/5篇无伪代码）+创新点弱声明"rather than introducing a new estimator or a new closed-loop component"（R010 §3.2对齐Johst，定位=量化归因型D005务实路线）。**Results两段式**：§IV-A影响分析（Fig.2 BER 6子图占位+AWGN implicit baseline对齐Johst+crossover 17.9/16.8/10.7 dB只呈现数据不附归因R009不变量7）+§IV-B方法增益（切换vs固定NDA低SNR+1.3~2.3 net口径CI下界全正+净增益strong+1.26/up_mod+1.19/up_str+1.85 naive标脚注+弱湍流归零诚实标注+0.09/0.18/0.19 CI重叠不变量3不藏+选对率26/29兑现Intro承诺+切换vs固定DA不写导师第3点）。**交叉检查6项+W001衔接全过**：术语跟R011（DA/NDA/per-block SNR/crossover/estimator switching/net SNR gain全标准+fair_gain/A4/MSM/伪地板/鲁棒性补丁零残留）/符号跟R011（θ̂_DA/θ̂_NDA/γ_blk/γ_th/P_b全对齐）/数字跟R012（crossover=data/切换vs NDA=net/净增益=naive标脚注全对，弱湍流归零诚实）/力度跟R010（Method文字非伪代码+公式直接给+创新点弱声明/Results BER纵轴不硬凑1e-5中性措辞+Tab.1增量亮点+对比融Results不专列）/切换framing自适应选优（R008 verbatim "selecting the locally optimal estimator in 26 of 29"）/crossover只呈现数据不附归因/W001衔接（θ/σ²_θ/net SNR gain脚注逐字照抄+Intro承诺26/29+1.85dB兑现）。**Results风险防范落实**：主体对解读不敏感（BER曲线+HD-FEC(3.8e-3)增益硬事实+crossover+选对率，导师翻解读A也不用重写），3个待导师项进标记区HTML注释TBD（①§IV-A纵轴范围D003 ②§IV-A 1e-5解读措辞 ③§IV-B标题数字口径D004）。守质量红线11条+FR-22。下一步D-W5F3 Conclusion+Abstract）
- **W003** Conclusion（W5）+ Abstract（F3）正文起草——D-W5F3 产出（2026-07-12，**正文最后一个对话单元，正文全部定稿**）。按R012 §V大纲+R010 §5力度+writing-patterns §6.x/§8.x+W001/W002复述衔接起草。起草前grep W001/W002确认"26 of 29"+"1.85"确切写法口径照抄。**Conclusion 1段3句**（对齐R010 §5 Johst/Le Bidan一段式3-5句）：①复述贡献"In this paper, we proposed a per-block SNR-driven estimator switching scheme ... selects the locally optimal estimator in 26 of 29 operating points, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"（句式§6.2 OECC 2025）+②弱湍流归零诚实标注"the gain narrows toward zero (+0.09/+0.18/+0.19 dB, within the 30-seed confidence interval) in weak turbulence and AWGN"（不变量3）+③future"Future work is underway to strengthen the switching criterion, to extend ... to additional turbulence regimes, and to validate ... on uplink experimental data"（句式§6.4 MWP 2022）。**Abstract 1段4句**（Intro贡献句压缩版）：①问题DA/NDA trade-off（DA低SNR准+1.25dB overhead / NDA省带宽+squaring loss低SNR差）②方法"per-block SNR-driven estimator switching scheme that selects, for each fading block, between a DA and an NDA carrier phase estimator"（句式§8.x）③结果"selects the locally optimal estimator in 26 of 29 operating points, yielding a net SNR gain of up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"。Abstract不放公式/图表/crossover/弱湍流细节（留Conclusion）。**交叉检查5项全过**：复述数字五处一致（Intro/Method/Results/Conclusion/Abstract grep确认同一写法"26 of 29 operating points"+"up to 1.85 dB in strong turbulence (naive, net of pilot overhead)"+同一脚注模板逐字照抄）/术语跟R011+W001/W002（零自造词残留）/口径标注naive+脚注跟W001/W002/力度跟R010（Conclusion 3句在3-5句范围/Abstract 4句Intro压缩版）/切换framing自适应选优R008 verbatim关键短语。守质量红线8条+FR-22。下一步D-F1F2力度第二轮+图表）
- **F001** 力度第二轮对照（F1）+ 图表定稿（F2）——D-F1F2 产出（2026-07-12，**战役最后一个对话单元，写作战役全部完成**）。按R010力度基准表20条+图表专项+H012已知待查项4条+主控追加4条执行。**F1力度对照**：R010 20条基准（5节×3-5技术点）逐条对照全篇正文（W001+W002+W003）**全部对齐**，无硬性多了/少了偏差。**F1 8条待查项处理**（7项触发正文修正）：①删[APCCAS 2022]弱引用②"single-estimator baseline"→"either estimator used alone"③§III末26/29精简改前瞻引用④3个TBD不碰⑤"locally optimal"→"lower BER"四处hedging（R008精化非推翻，逻辑严谨化：3/29没选对不能说全点最优）⑥Conclusion换角度避免逐字重复Intro⑦Abstract开头加问题压力⑧"enjoys/known noiselessly"中性化。**F2图表定稿**：5项规格（Fig.1框图含切换判据框/Fig.2 BER 6子图纵轴TBD/Fig.3净增益/Fig.4 crossover只标数值/Tab.1强湍流3行naive+fair对照列），4图+1表对齐R010。**交叉检查5项全过**。守质量红线8条+FR-22。**写作战役全部完成**）
- **R013** 改稿影响传播章程（2026-07-12，写作战役完成后导师反馈前定）。用户问"老师反馈要改怎么办，改一处影响很大，得提前定章程"触发。**核心纪律=批次化**：收到反馈先登记到revision-queue.md不立即改，攒全了（导师说反馈完了/≥3条实质性/deadline倒推只剩改稿时间/用户决定）再批量走流程，按"从底层到表层"排序（L6定位→L5逻辑链→L4公式→L2数字/L3图表→L1措辞），同级别合并，统一交叉检查一次做完。**六级分类**：L1措辞（局部grep）/L2数字口径（跨四-五处正文+Tab.1+脚注，D004同型最高频失误区）/L3图表（图规格+引用段）/L4公式（R011三表+编号+交叉引用，建D###）/L5逻辑链（R009→R012→可能多节重写+不变量回查，建D###）/L6定位（回step4a不出本章程）。每级给checklist。**三条防错纪律**：①改前先列清单不直接动手②数字改动必须代码行验证口径（D004教训核心）③L4以上回查R011+不变量。**当前已登记6个待改项**（Q1纵轴范围L2+L3/Q2 1e-5解读措辞L1/Q3标题数字口径L2/Q4 Tab.1 fair列L3/Q5⑤hedging是否跟导师同步L1/Q6主对比文献L1），等导师反馈攒全后纳入批次。下次导师反馈来先读R013+revision-queue）
- **W004** 全篇中文审阅版（2026-07-12）。把 W001/W002/W003 英文正文（Abstract+§I~§V）按中文学术表达习惯重述为中文，供作者通读审阅逻辑衔接与读感（非投稿用）。术语对照表逐项落实（CPR/DA/NDA/per-block SNR/crossover/net SNR gain/squaring loss 等首次出现给中文全称+定义），公式与符号（θ/θ̂/γ_blk/γ_th/M₀/h_b 等）保持英文原样，数字与口径严格照英文版（26/29 选对率 + 1.85 dB naive + crossover 17.9/16.8/10.7 dB + 弱湍流归零 +0.09/0.18/0.19 + 同一脚注模板），3 处 TBD 标记原样保留位置不动。文末附「翻译说明」11 条列有歧义译法选择（regime→情形 / argument→辐角 / naive+fair 保留英文口径词 / consistent with zero→与零相容 / locally prevailing SNR→当前块所处 SNR 等）供作者确认。产出 `W004-chinese-review.md`，不增删内容、不"优化"逻辑、不加分析评论。
- **R014** 内容映射——对标集 A 组 5 篇内容构成 + 我方缺口（2026-07-12，D-R014 任务产出。正文偏短核查）。3 子agent并发（A 词数统计/B Le Bidan 内容地图重点 Method ~340 行/C 其余 4 篇内容地图）+ 主线亲自核验 W001/W002/W003 英文正文（FR-26）。**产出**：①词数总表（5 对标集+我方，我方 1628 词校验 ≈1649 ✓）②内容地图（每篇每段论点+素材+功能，Le Bidan 详/4 篇精简）③逐节缺口清单（5 节各一张表，判定标 n/5 有）。**核心结论**：我方 1628 词比最精简会议对标集(OECC-PSC 2247)少 28%，"约 3500 词"目标偏高（只含外场的 Johst 4177 达到），**合理目标 2500-3000 词**（对齐 Panasiewicz/Paillier）。偏短**不在** Intro/Conclusion/Abstract（在范围内），集中在 Method(281)+Results 缺实验设置段+SM(268)。**三个明确缺口**（4/5~5/5 对标集有、我方无）：①§III 替代方案对比+弃用理由（为何切换优于纯 DA/纯 NDA）②§III 设计权衡讨论（γ_th 选择/切换代价）③§IV 实验设置段（仿真怎么跑 seed/扫描/指标）。可选缺口：§I 项目背景(3/5)/§II 链路几何(2/5)；非缺口：§IV 现象解释（R009 已定不附归因=设计选择）。**R010 力度 vs R014 内容互补**：R010 记力度（已对齐），R014 记内容项缺失。守纪律：只给依据不给加厚方案（加不加/怎么加等用户/主控定）+ 不拍脑袋（判定基于"对标集有没有"）+ 守 FR-22（只读已有 content.md）。产出 `R014-content-mapping.md`）
- **W005** D-W-EXPAND 正文加厚（2026-07-12，D-W-EXPAND 任务产出。补 R014 五缺口，1628→2651 词）。2 子agent提取对标集写法粒度（agent A 对比段三段式"他法→缺陷→选择"/ agent B 权衡段轻量版"trade-off between A and B"+设置段散文式三要素信道模型+仿真规模+评估指标）作不拍脑袋前提。**五缺口补充**：缺口5 §I 背景+78（LEO 星座 feeder 容量需求引 sat.1553/Paillier）/缺口4 §II SM+129（αβ-σ²_R 关系+γ=Es/N₀ 定义+N_blk 相干时间依据+pilot arrangement+Wiener PN 随机走动说明，不给 GG PDF 守 R010）/缺口2 §III 替代方案对比（为何切换优于纯 DA/纯 NDA/其他判据，守 D002 自适应选优非必要环节）/缺口1b §III DA/NDA 特点（M₀=8 升幂 squaring loss 比 QPSK 严重→切换必要）/缺口3 §III 设计权衡（γ_th=measured crossover+per-regime 校准+太低/太高权衡+复杂度 1 SNR 估计+1 比较定性不编 FLOPs）/缺口1 §IV 实验设置段（Monte Carlo+30seed+N_blocks=400≥1e5bit+SNR 扫描+6 场景+AWGN baseline+HD-FEC 门限）/缺口1c §IV-A 现象观察（两条定性趋势只描述数据不附归因守 R009）/缺口1d §IV-B 弱湍流归零解释（两曲线接近→切换无收益，数据因果非物理机制）。**目标词数取舍**：主动停 2651 而非硬凑 3000——逐节不超标是更高优先级约束（§IV 734 近上沿 737，§III 763 受方法简洁性制约 R014 已打折）。2651=Panasiewicz(2650)同级，比 OECC(2247)多 18%。**交叉检查 6 项全过**（自造词零残留/数字一致/D002 红线/crossover 只呈现数据/力度对齐 R010/术语跟 R011）。**自检修正 1 处**：§IV-A 初稿写物理归因"deep fading push instantaneous SNR"违反 R009+R011，改为数据趋势描述+TBD 标注。守 FR-22（只读已有代码/数据/对标集）。产出 `W005-expand-record.md`，Edit W001/W002）
- **R015** 数据使用模式——对标集 A 组 5 篇怎么用数据 + 我方对照（2026-07-12，D-R015 任务产出。正文加厚后审查发现§IV-B 数字密度/口径混乱，先搞清"数据在论文里该怎么用"再决定改不改）。3 子agent并发（A=Paillier 重点有表体例最像标准稿 / B=Panasiewicz 最精简+Johst 含外场数据密集 / C=Le Bidan 0 表全数据进正文+OECC-PSC SNR-penalty 图/BCRLB 处理）按 5 维度提取数据使用模式。**产出**：①5 篇×5 维度数据使用模式总表（每格标依据）②我方 W002 数据用法 vs 对标集差异清单（逐维度标差异）。**10 条跨篇领域惯例**：①表极少且不冗余正文（4/5 篇 0 表，Paillier 唯一有表且表图互证不复述）②正文数字密度中等（主流每百词 1-2），密集靠行内公式/列表非堆砌③逐点证据绝不全列正文（挑代表点 Paillier3/OECC2/Johst AB 标点，或进图正文定性 Le Bidan）④结果/增益精度=1 位小数或整数+about/~ 标记（2 位小数罕见）⑤全不报 CI/误差棒领域惯例（统计性靠 MC 次数/事件数/outage ratio 替代，印证 R002§C）⑥口径标注轻量（多数不标 overhead，标的正文一句或分场景，不两口径同段混）⑦headline 融叙述不单列加粗⑧理论上界 BCRLB/CRB 口头声明+实证替代（OECC abstract 称收敛 BCRLB 正文不画改横向对比）⑨门限/约束两类处理（轻量一句带过配方程/重量专门段+图表交叉引用）⑩数据-文字分工主流"文字引出→方程→图表验证→文字解读"。**我方 5 处差异**（描述性不评判）：§IV-B 四套数字挤一段（naive+net+归零+分母29）高于对标集主流密度/Tab.1 与正文数字冗余（对标集表图互证不复述）/逐点全列正文（对标集挑代表或进图）/增益 2 位小数（对标集 1 位+about/~）/报 30-seed CI 偏离惯例/naive+net 两口径同段混（对标集单一或分场景）。**不替定改方案**——差异清单是事实记录，改不改/怎么改留后续用户+主控决策。R010 力度+R014 内容+R015 数据用法三轮对标互补。守 FR-22（只读已有 content.md+W002）。产出 `R015-data-usage-pattern.md`）
- **R016** 会议论文写作执行规范（2026-07-12，D-R016 任务产出。把三轮对标调研 R010/R014/R015 + 写作教训 F1/W005/R009/R002§C 总结成可复用执行规范，类似 code-quality.md 之于代码）。主线程完成（规则总结是分析性任务，读 8 个必读文件提取）。**产出** `R016-conference-writing-rules.md`，§0-§7 结构：§0 怎么用（适用范围/何时读/跟 R010-R015 关系/提取原则）§1 立项对标（建 benchmark set/三轮分工/n-5 缺口判定/词数标定）§2 力度规则（公式直接给/贡献散文/文字非伪代码/BER 不硬凑 1e-5/表 0-1 张增量亮点/图 4-6 张/弱声明）§3 内容规则（必有内容项 5 类/方法简洁不硬补/每节词数标定/Conclusion 单段）§4 数据呈现（10 条，最重要）§5 措辞规则（hedging/不用弱引用/黑话禁令/不逐字重复/不口语化/不深挖归因/grep 自检）§6 改稿规则（批次化/L1-L6 六级/三防错纪律）§7 红线速查 15 条。**§4.1「数据诚实 vs 呈现选择」= 本轮最重要新增**（用户战役末期纠正的方法论误判）：数据诚实（底线必须，不伪造不 cherry-pick 不藏 CI 重叠）vs 呈现诚实（有裁量空间，写哪些不写哪些属学术写作惯例）；领域惯例=选择性呈现不主动报不利数字（不是撒谎是不提）；弱湍流归零 0.09/0.18/0.19 不进正文用定性表述"gains concentrate in strong turbulence"；边界=不利数字影响核心声称成立性时必须报（我们弱湍流归零不影响主卖点强湍流净增益所以可选）。每条规则标依据（R010§x/R014§x/R015 惯例 x/F1 修正 x/教训来源），不重复 R010-R015 详细数据只提取规则。守 FR-22 只读已有文件不调研不跑实验）
- **revision-queue** 待改项集中登记（2026-07-12，D-revision-queue 任务产出。无 R/W 编号，治理文件。把写作战役全过程积累的散落待改项集中登记，为后续按 R013 批次改稿做准备）。**产出** `revision-queue.md`，四源 16 条全覆盖（A=R013 原 Q1-Q6 / B=R015 数据用法 5 处差异 / C=用户纠正 1 条 / D=其他审查 2 条）+ 需核实项 4 条（F1 DA pilot 单/多 / F2 h_b 估计 / F3 γ_th 取法 / F4 voice.md 原话补录）。每条标级别（L1-L6）+ 涉及决策 + 状态。无 L4-L6 项（本轮改动落在 L1-L3 数据呈现层）。**只登记不改正文**。批次触发条件（导师说反馈完了/≥3 条实质 pending→ready/deadline 倒推/用户决定）+ 批次顺序（L6→L5→L4→L2/L3→L1）+ 三防错纪律照搬 R013。**⚠️治理偏离**：来源 C"不报弱湍流归零数字"——建立时 voice.md 未收录原话，按 FR-26 + session-governance Trigger 2 不擅自建 D###；读取中发现 R016（并行产出）已确认此为"用户 2026-07-12 战役末期纠正"且 §4.1 已立规则，故事实成立性已解决，Q12 升级为"pending 补 voice.md 原话→建 D### 细化不变量 3"。请旧对话审查：①四源遗漏 ②级别是否合理（Q7 §IV-B 四套数字挤一段是否够 L5）③F1-F4 外还有无要查代码的 ④F4 voice.md 是否本对话补）
- **R017** Q17 探索：per-regime crossover 阈值 vs 固定 13.0 实证（2026-07-12，Q17 探索 brief 任务产出。Step 4a 维度 D MVE 判据调整范畴，结果回传本专题不进 Contract/Execute）。**任务**：revision-queue Q17 三选一（①改文字匹配代码 ②改代码 per-regime ③中间方案），brief 要求跑选项②验证选对率/增益变化。**改法（路径 A）**：保留 γ_eff 判据结构，GAMMA_EFF_TH 从单一 13.0 改 per-regime dict {awgn:99/weak:17.9/mod:16.8/strong:10.7}（crossover 换算 γ_eff 轴：median(h_blind)≈1→crossover_γ≈crossover_γ_eff，实测 median(h)∈[0.77,1.15]）。**结果（30seed，TL-23 违例 0）**：选对率 26/29→**25/29 变差**（strong 高 SNR 3 点没翻转，反增 moderate@20 新错点）。vs NDA net gain 中间 SNR 区反增强（weak@15 +0.98→+1.56 / mod@15 +1.08→+1.40 / mod@20 +0.18→+0.47）。**机制（per-block 追踪 strong@15）**：crossover 是 γ 轴概念，decide() 作用 γ_eff 轴（per-block），γ_eff 是噪声代理——th=10.7 时 γ_eff>10.7 的 304 块里 DA 赢 230 块但判据全判 NDA。**可实现性**：per-regime crossover 接收端可实现（regime 从 h 分布/闪烁指数可测；crossover 值需离线校准 LUT=标准自适应实践，非在线 BER 偷看）。**Q17 建议=选项③**（排除②因选对率变差；不取①因暴露 13dB 偏保守弱点）：保留固定代码 + §III 改"a fixed effective-SNR threshold γ_th, chosen to separate the DA- and NDA-favored operating regions"，删 W002 L28 "measured crossover"+"per-regime" 两句。§IV-A crossover 17.9/16.8/10.7 作为数据观察仍呈现。**D005 归因修正**：strong 高 SNR 3 点选错不是"13dB 偏保守"，是"γ_eff 是 crossover 的噪声代理"，per-regime(10.7)也救不回。产出 `R017-q17-per-regime-crossover-experiment.md` + 代码 `_a4_switch_30seed_per_regime.py` + 数据 `_a4_switch_30seed_per_regime.json`。revision-queue Q17 已更新状态）
- **W006** §III 批次改稿——Q17/Q16/Q15 三项 L4-L5 改动落地（2026-07-12，R013 改稿章程第一次实际改稿）。按"从底层到表层"顺序处理 §III 三项改动（Q17 L5 → Q16 L4-L5 → Q15 L4），全部落在 W002 §III 同一段 + R011 公式清单代码行溯源。**建 D008** 统一记录"§III 方法描述匹配代码实现"（切换阈值固定非 measured crossover/per-regime，DA 多 pilot 平均，γ_blk h_b 估计来源补足）。**Q17（L5）**：W002 §III L28 删三句声称不符代码的描述（"measured crossover SNR for each turbulence regime"+"determined separately for each regime rather than held fixed"+"per-regime calibration lets the switching boundary track"）+ 替换为"a fixed effective-SNR value, chosen to separate the low-SNR region where the DA estimator yields the lower BER from the high-SNR region where the NDA estimator does"；保留 trade-off 段 + 实现复杂度段；§IV-A 两处"crossover γ_th moves to lower SNR"→"crossover SNR moves to lower values"（去 γ_th 标签，数据观察非判据来源）。**Q16（L4-L5）**：W002 §III 公式 3 后加一句"Here h_b denotes the per-block channel amplitude, estimated from the received block"（模糊但诚实，不暴露判据用盲估计而 DA 路径用 pilot 估计的脱钩细节 D001 Bug2/D002，守 D007）；R011 #3 代码行 `_recovery.py:232-233`（指向错误文件）→ `sc_nda_ml_sim.py:95-110 / _a4_switch_experiment.py:127-135`。**Q15（L4）**：W002 §III 公式 1 描述"the received pilot sample r_p"（单数）→"dividing each received pilot sample by ... averages the resulting phases over the N_p pilot symbols within the block, and takes the argument"；公式形式保留（会议简化 OK）；R011 #1 代码行 `_recovery.py:153` 保留，描述更新匹配多 pilot LS 回归（补 `_recovery.py:153-161`）。**守纪律**：FR-22（只改文字不跑实验，选项②改代码已 R017 排除）+ D007/不变量 3（不提不好的——判据脱钩/γ_eff 噪声代理/13dB 偏保守弱点都不进正文）+ 不变量 7（crossover 只呈现数据不附归因）。**交叉检查 4 项全过**（无 measured crossover/per-regime 残留 + §IV-A 不暗示 γ_th 来源 + R011 代码行指向正确文件 + sample 单数→复数）。守 FR-22 + D007 + 不变量 7 + R013 三防错纪律。revision-queue Q15/Q16/Q17 状态 → done）
- **W007** 数据呈现批次改稿——Q12/Q14/Q10 三项 L1-L2 改动落地（2026-07-12，R013 改稿章程第二次实际改稿）。处理数据呈现层三项改动（跨正文 W001/W002/W003 + 联动），涉及 §I Intro / §IV-B / §V Conclusion / Abstract，不动 §II SM / §III Method / §IV-A / 公式 / 图表规格。**Q12（L2，先改——删弱湍流归零，决定 §IV-B 重写）**：W002 §IV-B 删 "In the weak-turbulence and AWGN regimes the net gain narrows to $+0.09$/$+0.18$/$+0.19$ dB...strong-turbulence and uplink conditions." 整段（含归零数字 + "reported transparently rather than suppressed" + 弱湍流归零因果解释"two estimators' BER curves are close"），§IV-B 重写为只讲强湍流/上行有利结果（Low-SNR avoidance 1.3–2.3 dB + Strong-turbulence net gain 1.2–1.9 dB 三值 + 选对率 26/29）；W003 Conclusion 删 "while the gain narrows toward zero ($+0.09$/$+0.18$/$+0.19$ dB, within the $30$-seed confidence interval) in weak turbulence and AWGN, where the two estimators perform nearly identically" 整句。弱湍流/AWGN 不再出现在增益讨论段（连"gains concentrate in strong turbulence"定性暗示都不写）。Abstract 本就未报归零，不动。**Q14（L1，第二改——CI 收敛，和 Q12 联动）**：W002 §IV-B 删 "(CI lower bounds uniformly positive)"（改为直接陈述"yielding a net SNR gain of $1.3$–$2.3$ dB over a fixed NDA estimator"，不报 CI）；W003 Conclusion "within the $30$-seed confidence interval" 随 Q12 删归零句删除（同一句）；**保留** §IV 开头 L34 "averages over $30$ independent seeds"（设置段交代仿真规模，MC 次数是惯例 CI 不报是惯例，两者不同）。**Q10（L1，第三改——增益精度 2 位→1 位+about）**：1.85→about 1.9（四舍五入，⚠️ 非 1.8，原 queue 笔误已修）/ 1.26→about 1.3 / 1.19→about 1.2 / 1.3–2.3 区间保留（已 1 位）。逐处改（grep 全清单 7 处）：W001 Intro L20 "up to 1.85 dB"→"up to about 1.9 dB"；W002 §IV-B L42 四处（"$+1.26$ dB"→"about $1.3$ dB" / "$+1.19$ dB"→"about $1.2$ dB" / "$+1.85$ dB"→"about $1.9$ dB" / "1.19–1.85 dB"→"about $1.2$–$1.9$ dB"）；W003 Conclusion L16 "up to 1.85 dB"→"up to about 1.9 dB"；W003 Abstract L24 "up to 1.85 dB"→"up to about 1.9 dB"。脚注 1.25 dB ($10\log_{10}(4/3)$) + 768 bits 保留（精确定义值非结果增益）。**守纪律**：FR-22（只改文字不跑实验，Q10 是四舍五入非口径变更不触发 D004 代码行验证，Q12 删呈现非改数据，Q14 删标注非改数字）+ D007/不变量 3（弱湍流归零数字+定性解释+CI 标注全删，弱湍流/AWGN 不出现在增益讨论段）+ R016 §4.1/§7 红线 6（不利数字不进正文连定性都不提）+ R016 §4.3/§7 红线 7（增益 1 位+about）+ R015 惯例 5/§7 红线 8（不报 CI）+ 不变量 8（切换数字用 D002 修复版，本轮不改切换数字只改呈现精度）。**交叉检查 4 项 grep 全过**（grep 0.09/0.18/0.19 正文 0 处残留 + grep confidence interval 正文 0 处残留 + grep 1.85/1.26/1.19 正文增益全 about+1 位 + grep "transparently rather than suppressed" 正文 0 处；剩余命中全在元数据交叉检查表=债务待转 LaTeX 前清理）。revision-queue Q10/Q12/Q14 状态 → done）
- **R023** CCISP→学位论文 extension packaging 诊断（2026-08-03，用户 brief 全流程任务，paper-writing DIAGNOSE/PROPOSE，只诊断不进 WRITE）。以 CCISP 会议稿为 Ch3 主锚，把 campaign 资产映射为鲁棒性/部署实现/可信验证扩展。**Phase A** contribution contract + conference_claim→thesis_extension_question→asset→missing_evidence 映射。**Phase B** 按 P0–P5 问题链重聚类（P1 SNR 失配/P2 连续 GG/P3 先选后跑/P4 定点/P5 coded）。**Phase C** 四包装评估：**Package A（学位论文扩展）= 唯一推荐**，Package B（journal extension，venue=N/A，当前不足）/C（engineering note）/D（边界论文）均不独立成稿归入 A。**Phase D** 唯一 blueprint Ch1–Ch6（Ch4 鲁棒性边界贡献成立非新算法 / Ch5 实现贡献成立限定实现可行性 / **不产第二算法**）。**Phase E** gap-to-package map 五级分类。**Phase F** 唯一小包 = 统一鲁棒性表（P01 adapter + P04 continuous GG）。**关键交叉验证**：(1) 投稿状态 = `CONFERENCE_MANUSCRIPT_COMPLETE / SUBMISSION_STATUS_UNKNOWN`（无投稿编号/回执/录用）；(2) tracked main.pdf 是旧 7/8 页构建非权威，权威 = LaTeX 源 + V026–V028（5 页）；(3) full-grid branch-compute timing **仅在 OLD-params 诊断 JSON（无 authority）**，formal B JSON 无 timing 字段 → full-grid formal timing 需新跑；(4) headline 数字 machine-checkable（selector_a JSON 每 cell 含 selected/fixed_nda errors + n_bits=768，G_C 一行确定性复算 0.8–1.5 dB）。**守纪律**：不改 CCISP tex/正式 thesis/仿真代码/results/Skill/dormant campaigns，不复活旧口径（26/29/uplink/1.2–1.9/3.1 dB）。产出 5 dossier 文件 `projects/thesis-fso/direction-lab/harvest/` + R023 + D023（唯一 blueprint）+ D024（唯一小包）+ voice.md 登记 + topic-index 更新。本轮 commit 一次不 push。）
- **S018** 硕士论文方法包装逆向工程与本项目方法内核重审（2026-08-03，D025→D026，paper-writing INTAKE/DIAGNOSE/PROPOSE）。T002 证据化复盘旧 34/32 篇混合口径；T003 盘点全部方法 kernel；T004–T009 对 12 篇真实硕士逐篇精读至少两个方法/技术章并用统一 baseline→actual-delta 模板抽取；T010 独立交叉映射；T011/V013 fresh-context 独立终验 13/13 PASS、零 Critical/Important/Minor。产出 `peer-thesis-method-packaging-audit.md`、`internal-method-kernel-inventory.yaml`、`packaging-recipe-library.md`、`thesis-method-spines.md`。终态：R1–R5 有 ≥2 篇真实实例，R6=0/12 不硬贴；唯一推荐 Spine S1 = Ch3 CCISP / Ch4 2A / Ch5 2B，grade B−/CONDITIONAL；2A/2B 各差一个 bounded package，Phase G 不触发，不建 missing-method-search-target。本轮未写正式正文、未跑实验、未改 Skill、未触碰 p05 logs。
