# [S003] 导师反馈逐条处理 + 黑话审计 + 叙事定位（fair_gain vs 切换）

> 2026-07-09 | 阶段：写作准备（导师反馈处理 + 概念澄清 + 叙事定位） | 状态：进行中
> 来源：压缩后恢复。S002 末尾"论文包装流程规划"被导师反馈打断，转处理导师反馈

## 目标

接 S002 末尾的"论文包装流程规划"被导师反馈打断。导师回了简报 v2 的反馈（"A4切换是什么 / fair gain是什么"——简报不够自包含 + 大量黑话）。本轮目标：

1. 把导师反馈逐条确认理解
2. 把核心概念（fair_gain / 切换）用导师听得懂的话讲清楚
3. 审计简报全文黑话（内部编号 / 自造术语 / 未定义缩写）
4. 查 BER 10⁻⁵ 这条导师硬要求（H002 补点实验）
5. 理清叙事定位（fair_gain 是发现还是方法贡献）

## 记录

### 一、导师反馈（3 批，逐条确认）

导师反馈原文：
1. "A4切换是什么意思 / Fair gain是什么意思" —— 简报不够自包含，大量黑话
2. "图儿首先有系统框图...算法的仿真结果的图大概有三四个...误码率曲线不能只在10的-2次方这个层级...有编译码的情况下10的-5次方是底线" —— 图结构 + BER 10⁻⁵ 硬要求
3. "对比方法的那一篇文献至关重要，一定要发给我" —— 要审 baseline 源文献

**逐条确认**：
- ① 黑话：fair_gain（自造）+ A4（内部编号）是核心卖点词，导师看不懂是必然。**已展开审计（见 §三）**
- ② 图结构：系统框图（可拆场景图+框图）+ 3-4 个仿真结果图（哪个效果好用哪个）。BER 10⁻⁵ 硬要求 = ⚠️ 大问题（见 §四）
- ③ 文献：要发主 baseline 源文献给导师审。**"对比方法那篇"具体指哪篇待用户与导师确认**（按 D-010 主 baseline=DA-ML，源=Cao 2012 PTL）

### 二、核心概念澄清（fair_gain / 切换）

#### fair_gain 概念

**问题**：fair_gain 是我们自造的变量名，领域无此标准词。

**子 agent 调研结论（领域标准术语）**：
- pilot power penalty（导频功率开销，dB）—— Shoji JLT 2012 算过 0.8dB
- SNR gain（达到同 BER 所需 SNR 差，dB）—— Du PTL 2025 / Wang JPhoton 2024 用
- **fair_gain = SNR gain − pilot power penalty（两个标准量相减，非标准合成）**
- 领域主流"分开报告不主动扣"，我们主动扣开销是更严做法（新颖性，不是劣势）

**处理**：fair_gain 不进论文/简报当主术语。改 **net gain（净增益）**，首次出现给全称"SNR gain net of pilot power penalty（扣除导频功率开销后的 SNR 增益）"。备选 "overhead-adjusted SNR gain"。

**给导师的一句话**：net gain = 强湍流下盲估计比导频辅助估计达到同 BER 所需 SNR 低多少，扣掉导频先天吃掉的功率开销（1.25dB）后的净增益。强湍流 +1.2dB。

#### 切换方法概念

**问题**：A4 是 GW Step 4a 维度 D 第四候选的内部编号，对外人无意义。

**剥掉代号后的功能名**：基于块有效 SNR 的估计器切换（per-block effective-SNR-driven estimator switching）。候选规范命名 "adaptive carrier phase recovery with per-block estimator switching"。

**给导师的一句话**：A4 是内部文件编号（可忽略）。实际是：接收端按每个数据块的信号质量，自动选盲估计还是导频估计。增益 +0.27-0.48dB（crossover 区，比 net gain 小，但这是真正的方法贡献）。

### 三、简报 v2 黑话审计（全文逐词扫描）

**类型一 内部编号（必须删）**：A4 / B11-Q1 / MSDM（未定义）
**类型二 自造术语（必须定义或改名）**：fair_gain→net gain / crossover→切换点 / deep fade→信号深度衰落 / "有效 SNR"→块内信噪比 / "真实增益"→扣开销后净增益
**类型三 未定义缩写（首次展开）**：DA-ML / NDA-ML / DA / NDA / CPR / FSO / GG / HD-FEC / CI / DPLL / VV / BPS / CRB / OSNR（共 ~15 个）
**类型四 领域行话（需注解）**：pilot overhead 1.25dB 来源 / BER 是 pre-FEC 还是 post-FEC（与 10⁻⁵ 口径联动）
**类型五 文学化表达**："盲类/导频类"→"盲估计/导频辅助估计" / "击穿"→"使...失效" / "兑现"→"利用" / "近亲"→"同族" / "空白"→"近年无严格 Trans 工作"

**关键观察**：简报首要读者假设错了——写成"给参与过讨论的人看"，而导师是第一次接触。导师问的 fair_gain+A4 恰好是类型一+类型二各一个，说明审计全覆盖是对的。

### 四、BER 10⁻⁵ 硬要求（H002 补点实验已回传）

**导师要求**：BER 不能停在 10⁻²，有编译码下 10⁻⁵ 是底线。

**⚠️ 关键纠正（本轮）**：我（和路 Z 子 agent）之前断言"strong/uplink 有 deep fade 错误地板，补点救不了"——**这是错的**（太早下结论，违反 TL-22）。

**H002 补点实验实测推翻**：
- strong/uplink **没有地板**，BER 全程单调下降，只是衰减率慢（~1.4×/2dB vs 轻湍流 ~3×/2dB）
- 到 10⁻⁵ 需 64-81dB（远超实际工作区），所以"画不到 10⁻⁵"结论对，但**原因是衰减慢不是地板**
- **deep fade 正确表征** = BER 曲线斜率显著变缓，不是 BER 卡死。原"伪地板"叙事若写进论文会被审稿人质疑，需修正

**补点结果摘要**（H002，5 seed 探索性）：
| 场景 | 最低 BER（补点后）| 到 10⁻⁵？ |
|---|---|---|
| AWGN | 远破 10⁻⁵ | ✅ |
| weak | 破 10⁻⁵ | ✅ |
| moderate | 8.3e-6 @46dB | ✅ 刚破 |
| strong | 2e-4 @50dB | ❌ 衰减慢非地板 |
| uplink_moderate/uplink_strong | ❌ | 衰减慢 |

**H002 接收方验证**（守 Trigger 5，3 条事实声称全 PASS）：
- moderate 46dB oracle BER = 8.3e-6 ✅（查 `_ber_ext_5seed.json` summary.moderate 末点）
- strong 50dB oracle BER = 1.95e-4 ✅（查 `_ber_ext2_5seed.json` summary.strong 末点）
- 外推到 10⁻⁵ 需 strong ~68dB / uplink_strong ~81dB ✅（报告 §3.2）

### 五、叙事定位（fair_gain 发现 vs 切换方法）

**核心张力**：第一层 net gain +1.2dB 是盲估计固有性质（发现/量化），第二层切换 +0.27-0.48dB 是我们提出的方法。硬并列会让审稿人质疑第一层"这也要你发现"。

**讲法 C 诚信边界实测验证**（本轮查 `_a4_switch_30seed.json` + run_log）：
- **crossover 真实存在**：低 SNR 区 NDA BER > DA BER（DA 赢，如 weak@5dB NDA 0.40 vs DA 0.34）；高 SNR 区 NDA < DA（NDA 赢，如 weak@26dB NDA 6.6e-4 vs DA 6.8e-4）
- **若全程用盲，低 SNR 区会崩**（比导频还差）
- **因此切换是 +1.2dB net gain 落地的必要条件**（没它低 SNR 区不敢用盲，只能全程导频，拿不到 net gain）

**讲法收敛**：B（只卖切换）和 C（切换壳+net gain 肉）其实收敛——因为 crossover 真实，切换是 +1.2dB 落地前提，所以可正大光明说"我们的方法（自适应切换方案）相对传统导频方案实现 +1.2dB 净增益"。
- 外壳 = 切换方法（干净贡献）
- 数字亮点 = +1.2dB（完整方案 vs 导频）
- 诚信标注：+1.2dB 来源是盲估计固有，切换独立增量是 +0.27-0.48dB

**用户决策**：**叙事定位等老师拍**。简报里把 B+C 融合讲法写清楚 + 诚信边界分析，交给老师定主卖哪层。

## 决策引用

- 无新建 D###（本轮决策均待导师拍板，落 decisions.md 后补）
- 关键用户决策（voice 级）：见 voice.md 2026-07-09 S003 段

## 范围确认

- 本轮是否在 scope boundary 内：**是**（概念澄清/黑话审计/叙事定位都是写作准备核心任务。BER 补点是回 step4a 跑的，H002 已标注守 FR-22）

## 后续

1. **重写简报 v3**（等：导师拍叙事定位 + BER 数据已齐）：
   - 黑话全清理（按 §三审计表替换）
   - fair_gain→net gain，A4→功能名
   - BER 部分按 H002 补点结果更新（3 场景到 10⁻⁵ + 3 场景衰减慢非地板）
   - 叙事定位按导师拍板写（B+C 融合为推荐备选）
   - 图结构按导师反馈收敛（框图 + 3-4 仿真图）
2. **发主 baseline 源文献给导师**（确认指哪篇后）
3. **BER 10⁻⁵ 口径**（pre/post-FEC）：导师"感觉是译码前"，用户待跟导师确认
4. **论文包装流程规划**（S002 末尾被打断的任务，简报定稿后回）

## 🔴 重大发现（2026-07-09 续）：切换增益数字全部不可信——三个代码 bug

**触发**：用户质疑"切换增益是哪来的？增益不是得对应 SNR 吗？能直接给场景下这么给增益吗？"+ "我们都切换了为啥不和始终更不好的去比？" + "它相对于差的增益不应该和好的减差的一样吗？怎么会差这么多（无导频固定增益被吞了）"

用户连续三个物理直觉质疑，主线读 `_a4_switch_30seed.py` 核查，发现三个 bug（详见 decisions.md D001）：

1. **混合分母 bug**：切换 BER 用混合分母（DA 块去导频位、NDA 块含导频位），和 NDA/DA 都不同口径 → "切换赢盲 +0.1-0.27dB"是假增益（L111-113/L135-137）
2. **判据脱钩 bug**：decide() 用 raw 信号，候选用各自 h，判据和结果脱钩（L135）
3. **事后诸葛亮对照 bug**：switch_vs_max 的对照是 max(DA,NDA) = 事后选更好的，不是真实 baseline（L152）

**影响**：
- 简报 v1/v2/v3 的"切换增益 +0.27-0.48dB"全部作废
- **净增益 +1.2dB 不受影响**（主实验标准 BER 算的，不走切换代码）
- crossover 本身真实（低 SNR DA 赢/高 SNR NDA 赢，主实验确认），但"切换是 +1.2dB 落地前提"需修 bug 后重验
- 修 bug + 重跑任务已交新对话（提示词）

**主线反思**：profile 写"物理 DSP 委托主线但主线须带证据链"——连续三轮简报把不可信数字当真的报，**是用户的物理直觉问出来的不是主线主动查的**。违反 TL-22 + TL-29。技术正确性上失职。

**强湍流 BER 调研任务**也交新对话（用户提出"看看别人强湍流怎么搞 BER 的，还是根本没人研究因为没法避免无效"）

**简报 v3 状态**：切换增益数字部分作废。净增益部分仍可信。简报发不发/怎么发等修 bug 数据回来再定。

## external-output skill 建成（2026-07-09 续）

**触发**：用户"想想咋搞一个写简报的 skill 吧？感觉得有了，不然都不会写，写的太烂了"

**范围决策**：宽版（所有对外输出：简报/论文摘要/答辩/审稿回复/开题报告）+ 项目级（`.agents/skills/external-output/`，跟 sim-preflight 一起）

**建成**：v0.1.0，7 文件 675 行：
- `SKILL.md`：核心心智模型（对外输出=内部语言翻译成外部可懂+出门前审查）+ 工作流 + 出门审查 C1-C10 + 场景路由
- `rules/translation.md`：内部语言 6 类 + 翻译方法
- `rules/claims.md`：数字溯源 + 声称边界 + 5 陷阱（**防切换 bug 类问题**）
- `rules/exit-check.md`：C1-C10 详表 + 正反例
- `rules/asking.md`：问问题分级 + 做功课清单
- `scenarios/briefing.md`：导师简报特有 B1-B5
- `CHANGELOG.md`：**C1-C10 每条标了来自哪个翻车事件**（C1=A4导师问/C2=fair_gain导师问/C4=切换bug/C5=事后对照/C7=文献格式/C9=没调研就问图...）

**设计特点**：每条规则基于今日真实翻车，不编空话；scenarios 按需建（briefing 先建，paper/defense/reply 等实际遇到再补）

**关键防线**：C4（数字溯源，出门前查怎么算的）+ C9（问问题先做功课）。这俩是今天最痛教训的落地。

## 三个新对话任务已派（2026-07-09 续，去新对话并行跑，避免占主线）

主线占用问题：用户指出"subagent 会给进度卡住"，三个任务都给提示词让用户去新对话跑：

1. **切换 bug 修复 + 重跑**（回 step4a）：修 `_a4_switch_30seed.py` 三 bug（混合分母/判据脱钩/事后对照），重跑验证切换 vs 固定DA / vs 固定NDA 的真实增益。提示词已给用户。
2. **强湍流 BER 领域调研**：查领域里强湍流 BER 降不到 10⁻⁵ 时别人怎么处理（照画/换指标outage/post-FEC/没人研究）。提示词已给用户。
3. **3 篇 baseline 下载+核实**：Du JLT 2021（最接近，已有）/ Zhou JLT 2013（经典，需下载）/ Gävert TCOM 2022（迁移，已有）。核实方法类型+期刊档级+场景+跟我们 DA-ML 搭不搭。提示词已给用户。

**接收**：三个任务跑完会回传 handoff/报告到 thesis-writing 专题或 step4a 专题。主线等数据回来继续。

## 简报 v3 当前状态（等数据）

- 净增益部分可信，可发
- 切换增益部分**禁用**（D001/不变量8），等修 bug 数据回来填
- BER 部分按 H002 补点结果（3 场景到 10⁻⁵ / 3 场景衰减慢）+ 等强湍流调研回来定怎么处理
- baseline 文献等核实报告回来 + IEEE 格式规范化
- **下次重写简报 v3 必过 external-output skill 的 C1-C10 出门审查**

## 🔎 压缩后恢复：数据回传清点（2026-07-09 续，新对话恢复轮）

> 2026-07-09 续接 | 压缩后恢复 | 状态：核查三新对话回传 → 数据只回来一个半 → 用户决策等收尾

### 目标

压缩后恢复，核查三个新对话（切换修复/强湍流调研/baseline 核实）的数据回传状态，决定下一步。

### 记录

主线**读代码/文件核查**（非自跑，守 FR-22 + 主对话不跑实验），发现三任务只回来一个半，且**无任何 handoff 回 `.sessions/`**：

| 任务 | 真实状态 | 证据（FR-26） |
|---|---|---|
| ① 切换 bug 修复 | 🟡 半成品：smoke(2seed) PASS，**30seed 未跑**，无 bugfix_report | `_a4_switch_30seed_fixed.py`（23:34 写好）+ `_a4_switch_2seed_fixed.json`（23:35），**无 30seed json**。脚本引用的 `_a4_switch_bugfix_report.md` 未生成 |
| ② 强湍流 BER 调研 | 🔴 完全没回 | `.sessions/` 全项目搜 turb/fade 近 2h 无新文件 |
| ③ 3 篇 baseline | 🟡 部分：Du2021/Gavert2022 md+pdf 到，Zhou2013 **下载失败**，无核实报告 | `papers/baseline/` 两篇齐；Zhou2013 `metadata.json` 标 `download_status: failed`；无"哪篇适合做对比方法"的核实报告 |

**切换修复脚本逻辑主线已审，方向正确**（读 `_a4_switch_30seed_fixed.py` 验的）：
- Bug 1 混合分母 → 统一全块 bit（1024），DA 错误仍 data 位算但分母统一 ✅
- Bug 2 判据脱钩 → 保留 raw + docstring 论证（脱钩只损 SW 不帮 SW，非假增益驱动源）✅ 论证成立
- Bug 3 oracle 对照 → 删 max(DA,NDA)，改报真实 baseline switch_vs_DA / switch_vs_NDA ✅
- TL-23 守门：SW ≥ per-seed per-block-oracle，smoke **0 违例**（meta selfcheck_min_violations=0）✅
- smoke 趋势：切换 vs NDA 在中 SNR 区有正增益，但**比原报 +0.27-0.48dB 弱**（符合删 oracle 假增益预期）。CI 不可信（2 seed），等 30seed

**两篇 baseline 论文标题确认**：
- Du2021 JLT：*An Optimum Signal Detection Approach to the Joint ML Estimation of Timing Offset, CFO and Phase Offset for CO-OFDM*（Du/Kam 组 = 本项目 DA-ML/NDA-ML 方法源头）
- Gavert2022 TCOM：*Estimation of Phase Noise Based on In-Band and Out-of-Band Frequency Domain Pilots*（pilot-vs-blind 功率分配理论）

**smoke 数字红旗解读**（不妄断）：strong@26dB 出现 SW>NDA（切换比盲还差）。用修复逻辑可解释 = 判据不完美时判错选错路，selfcheck_note 明确说 SW 可赢 frame-level min 也可输，**非 bug**。

### 决策引用

- 无新建 D###（本轮只核查 + 等待，无新决策）

### 范围确认

- 本轮是否在 scope boundary 内：**是**（核查回传数据是写作准备的合法前置）

### 后续

1. **等三个新对话收尾**（用户拍板）：30seed 跑完出 json+bugfix_report / 强湍流调研回传 / baseline 核实报告（Zhou2013 补下或换）
2. 数据齐后：验 handoff 事实声称（Trigger 5 接收方验证）→ 重写简报 v3 → 过 external-output skill C1-C10 → 发老师
3. **不擅自动**：30seed 不在本对话跑（守主对话不跑实验 + 子 agent 卡对话教训）、简报 v3 缺失数据部分不先写占位（用户选了"等齐再继续"）
