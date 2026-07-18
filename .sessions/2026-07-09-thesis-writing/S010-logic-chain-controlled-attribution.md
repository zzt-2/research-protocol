# [S010] 逻辑链受控归因调查（混淆变量拆解 + B 方案受控切片设计）

> 2026-07-11 | 阶段：写作准备（GW Step 4a 维度 D 内，H007 交接）| 状态：进行中（受控切片待跑，等用户旧对话问回）
> （续 S009 逻辑链闭环讨论 + H007 逐点核查交接）

## 目标

接 H007 任务：逐点核查论文逻辑链（A 导频失效 / B 盲估崩溃 / C crossover 左移）的物理因果归因是否站得住。**纪律：每个因果断言必须有明确代码支撑 + 理解透，不能拿旧数据趋势编故事**（用户 2026-07-11 纠正："你最好想想，怎么去逐个点，有说服力地证实"）。

## 记录

### 1. 数据确认（三组全重跑，H007 表格 PASS）

重跑 `/tmp/check_nda_low_snr.py` + `/tmp/switch_caliber_audit.py`，H007 表格所有声称数据点全部复现：

- **B 点（盲估低 SNR 崩溃条件性）**：AWGN NDA 全程赢（DA/NDA=1.26~1.03）；弱-中湍流低 SNR NDA 差（DA/NDA=0.71~0.94）；strong 低 SNR 两法接近持平（DA/NDA=0.98~0.99），15dB 起 NDA 翻赢
- **A 点（DA 强湍流高 SNR 失效）**：strong 15-26dB data 口径 NDA 全赢（DA/NDA 0.80→0.74）
- **C 点（crossover 左移）**：weak 交叉 ~17.9dB / mod ~16.8dB / strong ~10.7dB（线性插值精确值）
- **F 点**：data 口径选对率 26/29（awgn 8/8 + weak 7/7 + mod 7/7 + strong 4/7）

数据层面 H007 表格无误。**但数据趋势 ≠ 物理因果归因干净**（见第 3 节）。

### 2. 文献术语核查（子 agent 完成）

派子 agent 核查 6 类术语标准性。结论：

| 我用的词 | 标准度 | 标准说法 | 权威来源 |
|---|---|---|---|
| M-th power 升幂 | ✅ | Mth-power / V&V estimator | V&V 1983 IEEE TIT |
| "升幂放大噪声 M² 倍" | ⚠️ | phase-error variance ∝ M² (squaring loss) | Fitz 1997 TCOM / Mengali-D'Andrea 1997 |
| 盲估"崩溃" | ⚠️ | **SNR threshold / squaring-loss threshold** | 同上 |
| DA 低 SNR 更准 | ✅ | DA estimation, DA only viable at low SNR | Mengali-D'Andrea 1997 / Bertolucci 2021 |
| deep fade / block fading / Gamma-Gamma | ✅ | 标准 | Al-Habash 2001 / Ozarow 1994 |
| crossover / 交叉点 | ❌ 自造 | 论文显式定义 "SNR\* where BER curves intersect" | 无标准名 |
| pilot overhead / power penalty | ✅ | 标准，1.25dB=10log10(1/(1-0.25)) | Shieh-Djordjevic 2010 |
| effective SNR γ_eff | ⚠️ | 改 **instantaneous SNR γ=γ̄·\|h\|²**（effective SNR 在链路自适应另有所指）| Tse-Viswanath / Goldsmith |

### 3. DA/NDA 完整管线追踪（混淆变量发现——本轮最重要）

**用户纠正触发**：不能直接看 JSON 趋势编故事，要每个观点对应明确代码且完全理解。

**核实结论**：主实验 `_main_experiment_30seed.json` 和切换实验 `_a4_switch_30seed_fixed.json` **走同一套管线**（切换是主实验超集，多了 decide + 切换计数）。所以用切换数据查 B 点管线一致，合理。

**DA vs NDA 从 rx_raw 到 BER 的完整差异表**：

AWGN 场景（无 h 衰落，无均衡环节）：

| 环节 | NDA | DA | 差异性质 |
|---|---|---|---|
| FOE | `assume_df_zero=True` 跳过 | `da_ml_recovery` 内含 pilot 线性回归 | NDA 假设 df=0 |
| 相位恢复 | `rx**8` segmented mean-angle → `/8` | `angle(r(p)/s(p))` 线性回归 | **核心自变量：升 M²=64 vs 无升幂** |
| 解模糊 | `resolve_m16apsk_blockwise`（**genie tx_bits**）| pilot 参考 | NDA 用了 genie |
| 解调 | 全 1024 bit | data 位 768 bit | 口径（D005 已处理）|

湍流场景（多了 h 估计 + 均衡 + FOE 两阶段）：

| 环节 | NDA | DA | 差异性质 |
|---|---|---|---|
| **h 估计** | `estimate_h_blind_perblock`：ĥ=mean(\|rx\|²)−1/(2γ)（`sc_nda_ml_sim.py:95`）| `estimate_h_pilot_perblock`：ĥ=mean(\|r(p)/s(p)\|²)（`sc_nda_ml_sim.py:113`）| **混淆变量①** |
| 均衡 | `mmse_equalize(rx, h_blind, γ)` | `mmse_equalize(rx, h_pilot, γ)` | 跟随 h 估计 |
| FOE | `fft_foe_m0_omega`（rx^8 FFT 找频峰，`sc_nda_ml_sim.py:137`）| pilot 线性回归 | **混淆变量②** |
| 相位恢复 | `rx**8` mean-angle → `/8`（`intra='none'`，`_recovery.py:213`）| pilot 直除（`_recovery.py:136`）| **核心自变量** |
| 解模糊 | `resolve_m16apsk_blockwise`（**genie**）| pilot 参考 | **混淆变量③（方向偏帮 NDA）** |
| 解调 | 全 1024 bit | data 位 768 bit | 口径 |

**混淆变量方向分析**（关键）：

| 混淆变量 | 低 SNR 效果 | 偏帮谁 | 影响 |
|---|---|---|---|
| ① 盲 ħ vs pilot ħ | 盲 ħ 低 SNR 不准 → NDA 均衡更差 | **偏帮 DA** | 夸大 NDA 溃败 |
| ② fft_foe vs pilot FOE | fft_foe 低 SNR 锁伪峰 → NDA 残余相位斜坡 | **偏帮 DA** | 夸大 NDA 溃败 |
| ③ genie resolve vs pilot 解模糊 | genie 帮 NDA 解 M0-fold 模糊 | **偏帮 NDA** | 不影响"NDA 溃败"成立（有 genie 帮忙还输，溃败更铁）|

**结论**：①② 偏帮 DA，会**夸大** NDA 溃败程度。如果排除①②后溃败消失，"溃败主因=squaring-loss"被推翻。③偏帮 NDA，不影响溃败成立但说明 NDA 实际更差（genie 帮忙还输）。

### 4. S007/D005 crossover 方向错误（已确认但文档未改）

`/tmp/verify_logic_chain.py` 断言 2 铁证：每个 SNR 下湍流越强 DA/NDA 比值都向 1 靠（DA 优势缩小，非延伸）。

| SNR | weak | mod | strong | 趋势 |
|---|---|---|---|---|
| 5dB | 0.825 | 0.884 | 0.980 | ↑向1 |
| 10dB | 0.708 | 0.803 | 0.986 | ↑向1 |
| 15dB | 0.896 | 0.940 | 1.089 | ↑向1 |
| 20dB | 1.075 | 1.109 | 1.237 | ↑向1 |

S007 §3 / D005 写"湍流越强 DA 优势区往高 SNR 延伸→crossover 左移"是**反的**。正确是"湍流越强 DA 低 SNR 优势被深 fade 压缩→crossover 提前"。方向错误，与图自相矛盾（审稿人会看出）。**待用户确认后改 S007/D005 + 不变量 7**。

### 5. 饱和假设部分推翻（第二轮自验发现）

`/tmp/verify_logic_chain.py` 断言 3 证伪了我自己第一版因果链的部分：

| SNR | NDA-weak | NDA-mod | NDA-str | spread | 饱和？ |
|---|---|---|---|---|---|
| 5dB | 0.3994 | 0.3988 | 0.4003 | 0.0015 | ✓ 饱和（撞随机天花板 ~0.375-0.44）|
| 10dB | 0.2258 | 0.2486 | 0.2882 | 0.0624 | ✗ 随湍流恶化 |
| 15dB | 0.0530 | 0.0855 | 0.1579 | 0.1049 | ✗ 随湍流恶化 |

**教训**：我第一版说"NDA 在固定低 SNR 饱和到天花板"——只在 5dB 成立，10dB 以上 NDA 随湍流恶化（只是比 DA 慢）。**第二轮验证才发现，证明用户"先证实再下结论"是对的**。strong@5 两法 BER 0.39-0.40 接近 16-APSK 随机解调天花板，这才是"两法持平"的真正原因（不是"两法都烂"那么模糊）。

### 6. B 方案受控切片设计（用户选定 B，待跑）

**问题**："NDA 低 SNR 溃败主因是 squaring-loss（升幂）还是盲 h 均衡/fft_foe 混淆"——整条逻辑链的命门。用户选 B 方案（跑受控切片排除混淆），非 A（只讲教科书结论）。

**控制变量矩阵**（固定场景 weak/moderate/strong × SNR 5/10/15，固定 seed）：

| 组 | h 估计 | FOE | 相位恢复 | 排除什么 |
|---|---|---|---|---|
| 对照（现有数据）| NDA 盲 / DA pilot | NDA fft / DA pilot | NDA 升幂 / DA pilot | — |
| 实验1 | **两法都用 oracle h** | 各自保持 | 各自保持 | 排除混淆① |
| 实验2 | oracle h | **两法都用 oracle FOE** | 各自保持 | 排除①+② |

**判定标准**（"溃败仍在"= 弱-中湍流低 SNR NDA BER 仍比 DA 高 ≥15%）：

| 实验1 | 实验2 | 结论 |
|---|---|---|
| NDA 溃败大幅缓解 | — | 主因是**盲 h 均衡** → 叙事要改 |
| NDA 溃败仍在 | NDA 溃败仍在 | squaring-loss 是主因 → 叙事成立（干净归因）|
| NDA 溃败仍在 | NDA 溃败缓解 | squaring-loss + FOE 共同 → 叙事加限定 |

**实现要点**：
- oracle h：信道 `generate_shared_realization_apsk` 已返回 `h_true`，`ber_oracle_turb` 已用 oracle h 路径，直接复用
- oracle FOE：信道 `phi = phi_fo + phi_dot + phi_laser`（`_channel.py:18`）。FOE 针对 `phi_fo + phi_dot`（确定性频率项，可用已知 f_res/f_dot 复算），Wiener PN 留给两法估。**问题**：`generate_shared_realization_apsk` 只返回总 phi，没拆三项 → 脚本里需单独重算 `phi_fo + phi_dot`（确定性可复算，不碰随机 Wiener）
- 先跑实验1（只换 h 为 oracle），结果清晰就不跑实验2（省时间）
- 5 seed × 3 场景 × 3 SNR = 45 块级点，几分钟跑完。看趋势不求 CI

**不算违反 FR-22 的理由**：不跑新 MVE / 不改方法 / 不改参数 / 不进 Contract。用现有 oracle 路径做变量隔离，产出是"因果归因诊断"不进论文正文，只判断逻辑链怎么说。属写作准备阶段"论点合理性审查"。

### 7. 导师三质疑（2026-07-11 收到）+ 重新确认方向

导师审完 S010 后提三个质疑，**全部成立**：

**质疑1：crossover 左移的物理因果只解释了一半**
- S010 替代解释"DA 低 SNR 优势被深 fade 压缩→crossover 提前"只覆盖低 SNR 半边
- 但数据（断言2表）显示高 SNR 区 NDA 优势也随湍流增大（20dB: weak 1.075→strong 1.237）
- crossover 是 DA/NDA 比值穿过 1 的点，左移需要整条比值曲线随湍流"上抬"——两边都要物理解释
- **更深问题（主线补充——循环论证）**："比值曲线随湍流上抬"本身就是 crossover 左移的数学等价描述，拿它当解释 = 拿现象解释现象。真正的物理因果要回答"**为什么湍流让 NDA 相对 DA 的劣势在每个 SNR 点都缩小**"——这个机制 S010 还没给
- 低 SNR 半边勉强讲了（深 fade 打 DA pilot）；高 SNR 半边完全没讲（高 SNR NDA 升幂已被压制，湍流凭什么还让 NDA 优势增大？）
- crossover 实际发生在 10-15dB（BER 0.15~0.29），不是第5节说的"撞随机天花板"区（那是 5dB）。**"饱和压缩"解释不了 crossover 位置**

**质疑2：受控切片的目标/必要性没搞清——可能过度工程**
- S010 默认目标变成"证明 squaring-loss 是溃败唯一主因"（纯机制归因）
- 但盲估方法本来就要自己估 h 和 FOE——**混淆变量是盲估实现的固有部分，是真实系统行为**
- 论文若讲"实际系统切换让两者都不踩"（系统性能事实），两个完整实现对比就够，不需排除混淆
- 受控切片只在论文想声称"纯 squaring-loss 机制致低 SNR 差"时才必要；CCISP 4-6 页会议论文引用教科书结论（V&V squaring-loss）+ 数据不矛盾大概率够
- **需先定论文声称强度，再决定跑不跑受控切片**

**质疑3：术语建议 instantaneous SNR 可能也不对（块级 ≠ per-symbol）**
- 子 agent 建议把 effective SNR 改 instantaneous SNR
- 但 γ_eff=γ̄·h 是**100 符号块内恒定的 h 估计**，instantaneous SNR 在通信文献里通常指 per-symbol γ_k=γ̄·|h_k|²
- 块衰落下两者数值相等，但"瞬时"易误导读者理解成 per-symbol 随机变化
- **术语要重新查准确定义**（可能用 per-block SNR / block-averaged SNR / faded SNR，或显式定义 instantaneous 为块级）

**主线额外标记（次要）**：第6节判定标准"溃败仍在 = NDA BER 高 ≥15%"的 15% 是经验下界非物理判据。但依赖质疑2结论——若受控切片不跑则无所谓，不单独开质疑。

**主线判断**：三质疑已覆盖主要问题。额外能补的最实质点（循环论证）是质疑1的深化，非独立新洞。未发现更大的独立漏洞。

## 当前位置：导师三质疑待确认，受控切片暂缓

导师反馈三质疑后，受控切片暂缓——先确认两个前置问题再决定跑不跑：

1. **论文声称强度**（质疑2前提）：弱声称（系统性能事实，不需受控）vs 强声称（纯机制归因，需受控）——等用户定
2. **crossover 物理因果**（质疑1）：低 SNR + 高 SNR 两边都要物理解释，不能用"比值上抬"循环论证。需重新查数据/推导
3. 术语重新确认（质疑3）：effective/instantaneous/per-block SNR 哪个准确

### 8. 落地决定（2026-07-11，用户拍板"轻讲"）

用户看完三质疑后问"这块得讲到啥程度"，主线给结论 + 三理由（篇幅放不下 / R002§C 实证别人都不深挖 / 深挖对卖点无贡献），用户认可"轻讲"。

**用户补充重要约束**：CCISP 没有 rebuttal（过就过，没过就没）。这改变"审稿人追问可以答辩回"的假设——没机会解释。所以没把握的东西不写进论文，比没把握硬写安全。

**落地决定（全部锁定）**：

1. **"盲估低信噪比差"段**：轻讲。引 V&V 1983 / Mengali-D'Andrea 1997 的 squaring loss 标准结论 + 图 2 BER 曲线印证。不挖机制、不跑受控切片。
   - 论文写法参照：*"NDA-ML 采用 M 次幂去调制，受 squaring loss 影响，在低信噪比区相位估计精度下降 [V&V 1983 / Mengali-D'Andrea 1997]。"*（一句话，背景段，不展开）
   - squaring loss 是 V&V 1983 铁的标准结论，引它不会被挑错。

2. **受控切片（第6节设计）**：**不跑**。毛病2直接解决——论文只需系统性能事实（"实际系统盲估低 SNR 不如导频"），两个完整实现对比就够，不需排除"混淆因素"（盲 h 均衡、fft_foe 这些本来就是盲估方法的固有部分，是真实系统行为，不该排除）。

3. **crossover（毛病1）处理**：论文里**只呈现数据事实**——"两曲线有交叉、交叉点随湍流左移"（数据确认，断言1：weak 17.9dB / mod 16.8dB / strong 10.7dB）。**不附物理归因**。原因：S010 推翻了 S007 旧解释（方向错），但新解释只讲了一半 + 循环论证，没把握。没把握就不写。
   - S007/D005 里方向错的解释要从文档勘误掉（只删错的、不加没把握的新解释）。

4. **术语（毛病3）处理**：
   - "effective SNR γ_eff" 先从论文去掉，需要时用"per-block SNR"并显式定义（块内 100 符号恒定的 h 估计对应的 SNR，不是 per-symbol 瞬时 SNR）。子 agent 建议的 "instantaneous SNR" 不直接用（易误导读者理解成 per-symbol）。
   - 其他术语（squaring loss / pilot overhead / deep fade / Gamma-Gamma / V&V estimator）全标准，直接用。

**核心原则**：论文只放有把握的东西。没把握的物理归因一律不写——在没 rebuttal 的会议上，没把握硬写比不写风险大。

**用户提醒**：用词别搞黑话，要能看懂。后续所有产出（逻辑链定稿、论文草稿）遵守。

### 9. 旧对话身份澄清（2026-07-11）

用户说明：第7节那三质疑是**旧对话**提的，不是导师。主线之前误以为是导师反馈。身份不影响三个质疑本身的有效性（已逐条评估），但记录用词纠正：那是旧对话的质疑，不是导师。

### 10. 主控对话规划讨论——前置工作盘点 + 双语工作流 + 对标论文集（2026-07-11）

逻辑链定稿后，开始讨论主控对话该规划什么（S009 §6 阶段1）。

**前置工作完整盘点**（用户要求"得定下来有多少要做的"）：

横切关注点：
- **力度**：两轮校准——开头摸底立基准表（每节/每技术点别人写到什么程度）/ 末尾对照检查。贯穿所有活的标尺，不是独立活。

具体活（9 类，按依赖顺序）：
1. 用语（术语）——英文标准写法 + 中文备注，提取用法例句
2. 符号——数学符号全篇统一，对齐领域惯例
3. 公式——2-3 个，标来源，呈现粒度对齐领域惯例
4. 参数——每个标文献来源（TL-26），已有 _b11_params.py 溯源
5. 数字呈现——哪些进正文/表/图，口径标注（D004/D005），CI 策略（R002§C 说不报 CI 是惯例）
6. 叙事结构——5 节骨架，R009 逻辑链分配到各节
7. 句式——英文句式库（writing-patterns-conference.md），中文释义
8. 参考文献——10-15 篇，每篇标角色，等导师定主对比
9. 图表规格——**最后**，正文全部定稿后逐个想"这张图表达什么论点"（用户纠正：图表不是并行，得最后逐个想）

**双语工作流**（用户定 CCISP 英文投稿 + 自己先看中文再转英文）：
- 英文零件（术语/符号/句式）从一开始锁英文，中文只备注
- 中文起草时参照英文句式逻辑（先结论后理由，不铺垫）——用户拍板 **(a)** 模式
- Abstract/贡献句/结论句直接英文起草（门面句，避免翻译 lose 地道感）
- "转英文"不是翻译，是组装（术语查表 + 句式套模板 + 内容句换词）

**对标论文集调查**（三批子 agent，用户认可"参考一定得好好找，尽可能接近"）：

接近标准：必须对上（①相干检测 ②载波相位/频率同步 ③湍流场景）+ 越像越好（④星地/LEO ⑤DA vs blind 对比 ⑥会议 ⑦16/M-APSK ⑧切换/自适应）。

批1（R006 八篇技术接近度判）：
- 强内容对标 4 篇：MWP'22（★★★★唯一三项全中）/ ICSOS'25 / ICSOS'19 / OECC'25
- 该换 3 篇：OECC'24（数据中心模拟）/ APCCAS'22（FPGA 硬件）/ ICUMT'15（星间真空）
- 缺口：无 DA vs NDA 直接对比 / 无 16-APSK / 无 Gamma-Gamma 块衰落 / 无切换机制

批2（库内新筛）：补 2 篇 R006 没有的强内容对标——**Le Bidan ICSOS'23**（frame+pilot+blind CMA+DA 精载波，CCISP 体例最像）/ **Johst WiSEE'24**（卖点最贴，明确对比 blind vs data-aided 低 SNR）。

批3（切换检索，tools/search 8 轮）：**会议层"估计器切换"稀缺**，缺口跟批1/批2 信号一致——创新性正面证据。找到可用对标：
- He SPIE CSTA'24（会议，SNR 阈值链路切换，写法骨架对标）
- Wang OE'25（期刊，MSDM 驱动 SSD/MSD 检测器切换，机制最贴——**库内已有** papers/doi/10.1364_oe.564097/）
- Xu PTL'26（letter，BPSK↔QPSK 双阈值迟滞，迟滞机制参照）

**最终对标集**（待落盘 benchmark-paper-set.md）：
- 核心内容对标 5 会议：Johst WiSEE'24 / Le Bidan ICSOS'23 / Panasiewicz MWP'22 / OECC-PSC'25 / Paillier ICSOS'19
- 切换写法对标：He SPIE'24（骨架）/ Wang OE'25（机制）/ Xu PTL'26（迟滞）
- 技术源头：B11 PTL'25 / V&V'83 / sat.1553
- 句式补充：Pech ICSOS'25
- 从 R006 换掉：OECC'24 / APCCAS'22 / ICUMT'15

**下载状态**：
- Wang OE'25：**库内已有**（papers/doi/10.1364_oe.564097/，content.md + paper.pdf 就绪）
- He SPIE'24（10.1117/12.3036565）：tools/download fail + unpaywall 不 OA → 给用户 URL 手动下
- Xu PTL'26（10.1109/LPT.2026.3676909）：tools/download fail + blit 只拿到元数据 + unpaywall 不 OA → 给用户 URL 手动下

**三个写法启发**（子 agent 提炼）：
1. 切换判据：主流用瞬时 SNR 跟阈值比（He/Wang），Xu 双阈值迟滞防抖动（我们可借鉴描述）
2. 切换增益画法：BER-SNR 三线对比（固定 DA / 固定 NDA / 自适应）+ 标 dB 增益（跟 Fig.4 计划一致）
3. 切换价值定位：双定位——低 SNR DA 保障鲁棒 + 高 SNR NDA 提升频谱效率 + 自适应全局最优

## 当前位置：主控规划讨论完成，战役计划+对标集已落盘，下一步开主控对话

主控规划讨论收尾。产出三份文档（主控对话拿去执行）：
1. `benchmark-paper-set.md`——对标论文集（12篇，核心5篇会议库内全有content.md，核验过）
2. `writing-campaign-plan.md`——写作战役计划（9类前置+5节正文+3项收尾，每个活定规矩，对话拆分~8单元，9天时间分配，6条质量红线）
3. 主控对话提示词（已给用户，纯文本，用户去开新对话）

**待用户做**：
- 开新对话（MC主控），用给定提示词，主控读战役计划后生成各子对话提示词
- 手动下载 He SPIE'24 + Xu PTL'26（不阻塞，abstract够用）

**待办（低优先级，不阻塞主控）**：
- He SPIE'24（10.1117/12.3036565）+ Xu PTL'26（10.1109/LPT.2026.3676909）全文——tools/download fail，URL 已给用户，用户能下时补到 papers/downloads/2026-07-11/
- V&V'83（10.1109/TIT.1983.1056713）——引文献用，不需全文，按需补

受控切片不跑，"盲估低 SNR 差"段轻讲锁定。剩下收尾工作（都不依赖受控切片）：

1. **S007/D005 勘误**：删 crossover 方向错的解释（S007 §3 / D005 交叉点物理机制段），不加没把握的新解释。独立成立，可立即动。
2. **逻辑链定稿版**：只包含有把握的内容（数据事实 + 标准结论 + 图印证），物理归因能省则省。
3. **待查术语清单**：第2节表已基本就绪，"effective/instantaneous/per-block SNR"待最终定（倾向 per-block + 显式定义）。
4. 回主线 → 开主控对话规划写作流程（S009 §6 阶段1）。

## 决策引用

- 无新决策（受控切片结果出来后才决定是否新建 D007 记录归因结论 + D008 记录术语标准性）
- D005：data 口径（受控实验 BER 对比用 data 口径）
- D002：切换 30seed 数字基础
- S007/D005：crossover 方向错误已确认，待改（第 4 节）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。逻辑链因果归因调查 = 写作准备（原始目标第 4 条"审查论点合理性"）。受控切片用现有 oracle 路径不跑新 MVE，守 FR-22。

## 后续

1. **等用户旧对话问回**（当前卡点）
2. 用户回来后确认 B 方案受控设计 → 跑 `/tmp/controlled_attribution.py`（待写）
3. 受控结果 → 定因果归因（squaring-loss 主因 or 均衡主因 or 共同）
4. 归因干净后 → 逻辑链定稿版（每点标 数据✓/物理✓/文献✓/受控✓）
5. 改 S007/D005 crossover 方向错误 + 不变量 7
6. 待查术语清单（第 2 节表）落进论文写作前置工作

## 关键文件位置（本轮调查证据链）

- 切换 30seed 数据：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.json`
- 切换脚本：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_30seed_fixed.py`
- 主实验脚本：`projects/simulation/simulator/sc_nda_ml_sim.py`
- 参数：`projects/simulation/simulator/_b11_params.py`
- 信道：`projects/simulation/common/_channel.py`
- 估计器：`projects/simulation/common/_recovery.py`
- B 点核查脚本：`/tmp/check_nda_low_snr.py`
- 口径审计脚本：`/tmp/switch_caliber_audit.py`
- 因果断言验证脚本：`/tmp/verify_logic_chain.py`（断言1-5全跑，第3节铁证）
- 受控切片脚本：`/tmp/controlled_attribution.py`（待写，等用户回来）
