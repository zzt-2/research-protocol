# Topic Index: 论文写作专题（自适应 CPR 方向）

> slug: 2026-07-09-thesis-writing
> status: active | created 2026-07-09 | last_updated 2026-07-12（W002 D-W3W4 Method+Results 正文起草完成：§III Method（DA/NDA/per-block SNR 三公式直接给+切换规则文字+创新点弱声明）+§IV Results 两段式（§IV-A 影响分析 crossover 只呈现数据+§IV-B 方法增益 净增益 naive 标脚注+弱湍流归零诚实标注）。交叉检查 6 项+W001 衔接全过。Intro 贡献句承诺 26/29+1.85dB naive 已兑现。Results 风险防范落实（主体对解读不敏感 BER 曲线+HD-FEC 增益硬事实，3 个待导师项进标记区 TBD）。下一步 D-W5F3 Conclusion+Abstract）

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
- 盘点 projects/simulation/ 下所有简报/报告/数据文件的新鲜度
- 验证 A4 + NDA-ML 主实验数据稳定性（30seed CI / 债务项）
- 审查 A4 方向论点链（crossover → 切换 → 增益 → 新颖性）
- 完善简报 ADVISOR_BRIEFING_2026-07-09_adaptive_cpr.md

### 明确不含
- ❌ 不跑新实验 / 不进 Contract / 不写正式论文章节（FR-22）
- ❌ 不推翻 A4 PASS 的 Go 判定（那是 step4a 专题的事）
- ❌ 不改框架文件（守"先测不改协议"）
- ❌ 不做消融实验（跨块 KF / BPS 迁移等是 step4a 的债务，不在写作专题跑）

### 范围变更记录
（暂无）

## 不变量（动任何一条必须重新讨论）

1. **继承 step4a-mve-execution 全部不变量**（D005 务实路线 / FR-22 GW 门控 / FR-25 Go/Kill 分离 / D-006 红线 / D-010 baseline 五条 / TL-26 参数溯源 / TL-20 理论预期 / 核查机制中性双向）
2. **写作专题定位 = GW 阶段写作准备辅助**：不跳框架，不跑新实验。任何"跑新方法/新实验"的动作必须回 step4a 专题回答"在 GW 哪一步"
3. **A4 数据的诚实标注**：weak/moderate fair_gain CI 重叠（统计不可分），叙事是"两段趋势"非严格单调；30seed 基准配置 ✓ 但其他配置仍 3seed（债务）
4. **简报未发状态**：ADVISOR_BRIEFING_2026-07-09 写完未发老师，发前需确认数据最新 + 图是 30seed（债务③）
5. **deep fade 正确表征**（S003 修正，动它要重新讨论）：deep fade = **BER 曲线斜率显著变缓**（衰减率从轻湍流 ~3×/2dB 降到 ~1.4×/2dB），**不是 BER 卡死/伪地板**。H002 补点实测推翻了原"strong/uplink 有错误地板"预判（违反 TL-22 的太早结论）。论文/简报里不准用"伪地板"叙事，会被审稿人质疑
6. **黑话禁令**（S003 审计）：fair_gain（自造）/ A4-B11-Q1（内部编号）/ MSDM（未定义缩写）等**不进论文/简报**。fair_gain→net gain（SNR gain net of pilot power penalty），A4→"基于块有效 SNR 的估计器切换"。所有缩写首次出现写全称
7. **叙事诚信边界 / 故事根定位**（S003 提出，S004 第三轮定根）：crossover 真实存在（低 SNR 区 DA 赢、高 SNR 区 NDA 赢）。**D002 已推翻原"切换是 +1.2dB 落地必要条件"论断**——切换净增益微弱，net gain +1.2dB 来自 NDA 架构本身，不依赖切换。**故事根已定=候选 A（净增益量化归因，数字为根，deep fade 机制为辩护层）**（用户 2026-07-10 拍板）。**定位=量化归因型（非"提出新算法"型），待导师确认**（简报 v5 §4 根问题）。切换当鲁棒性补丁非独立卖点

8. **切换增益数字**（S003/D001→D002，D 级约束）：切换代码三 bug **已修复重跑（D002/H003）**。旧 +0.27-0.48dB（switch_vs_max oracle）永久禁用。**可用新数字（30seed net 口径）**：vs 固定 NDA 低 SNR +1.3~+2.3dB（避险）/ vs 固定 DA 仅 strong 高 SNR +0.02~+0.20dB（多数 CI 跨 0 不显著，仅 strong@24 显著 +0.20）。vs DA 增益必须用 net 口径（全块 bit，pilot overhead 在 BER 口径内扣 1.249dB）。**切换无全场景增益，不是"全面赢两固定方法"**。原 buggy 脚本 `_a4_switch_30seed.py` 留作证据，修复版 `_a4_switch_30seed_fixed.py`

9. **fair_gain 口径方向**（D004，2026-07-10 新建，D 级约束）：**fair_gain = naive + 1.25dB**，fair 是"罚导频 overhead 后的系统总账"（大数），naive 是"剔导频水分后的纯物理增益"（小数）。**简报 v4 曾搞反（把 fair 当"已扣开销净值"），已修正为两口径并列。** 6 场景：awgn/weak/mod naive 仅 +0.09/0.18/0.19（CI 重叠，几乎归零）；strong/up_mod/up_str naive +1.26/1.19/1.85。主报哪个口径待导师定（主线倾向 naive，剔水分不易被质疑，但卖点场景收窄到强湍流）。**报任何"已扣/净值/含水分"口径声称前，必须用代码行验证加减方向（fair_comparison.py:109），禁凭字段名/印象**

10. **B 路线已 Kill，回 A**（D006，2026-07-11 新建，INVARIANT 级——推翻需重新讨论）：B（pilot on/off 系统级架构选择）goodput 维度线性假设下数学已证任何 pilot density 都赢不了 NDA（成功率比 α 全点 <1，最大 weak@5=0.466），物理上凹函数翻转不现实。BER 维度跟 A（per-block 估计器切换）卖点重复。**回 A 路线**（data 口径 26/29 选对 + crossover 左移，D005 已验证）。A 写作资产直接复用，不需回 step4a 跑新实验。goodput 判据 α<1（线性假设 + 凸函数物理）可复用于未来任何 pilot 开关类方向

## 其他结论（普通技术决策）

（S001 盘点后填充）

## 已确认决策

（暂无，S001 起步）

## 悬而未决

1. **主图子图数**：S002 锁定图 2 = 4 子图（下行），H002 补点画了 6 子图（含上行）。待跟老师确认画 4 还是 6 子图。
2. **strong/uplink 子图纵轴范围**：H002 建议收窄到 1e-4~1e-1（不硬凑 1e-5），待跟老师确认。
3. **S002 原悬而未决**（图表清单 / fair_gain 呈现 / 主图子图数）：H002 把图 2 数据备齐，等老师反馈后定稿。

## 当前位置

**🟢 D-W3W4 Method+Results 正文起草完成，下一步 D-W5F3 Conclusion+Abstract（2026-07-12，W002 产出）**。

W002 完成 §III Method（2 段：DA 估计器 θ̂_DA=angle(r_p·p\*) 公式1 + NDA 估计器 θ̂_NDA=(1/M₀)angle(Σr_k^M₀) 公式2 + per-block SNR γ_blk=|h_b|²E_s/N₀ 公式3 + 切换规则文字 "select θ̂_DA when γ_blk<γ_th else θ̂_NDA" + 创新点弱声明 "rather than introducing a new estimator or a new closed-loop component"）+ §IV Results 两段式（§IV-A 影响分析：Fig.2 BER 6 子图 + crossover 17.9/16.8/10.7 dB 只呈现数据不附归因 + §IV-B 方法增益：切换 vs NDA +1.3~2.3 net + 净增益 strong+1.26/up_mod+1.19/up_str+1.85 naive 标脚注 + 弱湍流归零诚实标注 +0.09/0.18/0.19 + 选对率 26/29 兑现 Intro 承诺）英文正文。交叉检查 6 项 + W001 衔接全过。正文路径：`.sessions/2026-07-09-thesis-writing/W002-method-results.md`。

**关键锁定**：
- Intro 贡献句承诺兑现：§III 末 + §IV-B 都报 "26 of 29" + §IV-B 报 uplink strong "+1.85 dB (naive)" 与 Intro 完全一致
- Results 风险防范落实：主体对解读不敏感（BER 曲线 + HD-FEC(3.8e-3) 增益硬事实 + crossover + 选对率，导师翻解读 A 也不用重写），3 个待导师项进标记区 HTML 注释 TBD（①§IV-A 纵轴范围 D003 ②§IV-A 1e-5 解读措辞 ③§IV-B 标题数字口径 D004）
- net SNR gain 脚注逐字照抄 W001 模板；切换 framing 全篇统一自适应选优（R008 verbatim）；squaring loss 引 V&V 1983 不推导；切换 vs 固定 DA 不写（导师第 3 点）

**下一步**：D-W5F3。W5 写 Conclusion（1 段 3-5 句：复述贡献 + 弱湍流归零局限 + future，对齐 R010 §5/Johst）；F3 写 Abstract（直接英文起草，参照 Intro 贡献句 + writing-patterns §8.x）。F 阶段或导师反馈后集中处理 W002 的 3 个 TBD 标记区。规矩见 writing-campaign-plan.md §2 W5 + F3。

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
