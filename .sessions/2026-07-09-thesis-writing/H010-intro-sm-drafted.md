# Handoff: D-W1W2 Intro+System Model 正文已起草，交接 D-W3W4 Method+Results 正文

> 来源: W001（D-W1W2 子对话活本身）| 交接目标: D-W3W4 子对话——Method（W3）+ Results（W4）正文
> 文件名: H010-intro-sm-drafted.md
> 日期: 2026-07-12

## 到哪了（状态）

D-W1W2 完成。产出 **W001-intro-system-model.md**（Intro 3 段 + System Model 2 段英文正文）。

- **Intro 3 段**：①背景（相干 FSO + 湍流致相位噪声 + CPR 必要，引 6 篇）②DA/NDA trade-off gap 2 句（DA 低 SNR 准 + 1.25dB 罚引 Shieh-Djordjevic / NDA 省带宽 + squaring loss 引 V&V 1983）③贡献散文式 3 句不用 bullet（verbatim R008 关键短语 "selects the locally optimal estimator in 26 of 29 operating points" + 净增益 "1.85 dB in strong turbulence (naive, net of pilot overhead)" + 口径脚注模板）
- **SM 2 段**：①GG 块衰落信道（引 Al-Habash，块结构 N_blk=100，αβ 下行 3 档+上行 2 档值进正文，**不给 PDF**）+ Fig.1 占位 ②信号模型 r_k = h_b·s_k·e^{jθ} + n_k + 帧结构 pilot spacing 1/4 = 25% = 1.25dB + Wiener PN σ²_θ = 2πΔνT_s（注 "= σ²_p in [B11]"）+ N_DFT=256 + HD-FEC 3.8e-3
- **交叉检查 6 项全过**：术语跟 R011（零自造词残留）/ 符号跟 R011（θ 非 φ 注 B11 对应）/ 数字跟 R012（26/29 + 1.85dB naive 标脚注）/ 力度跟 R010（Intro ~15 行 / SM 给 GG+块结构不给 PDF 不给独立参数表）/ 切换 framing 自适应选优（R008 verbatim）/ 句式参照 writing-patterns-conference.md（§5.4/5.6/5.7/8.x/1.2/1.13）
- **θ 符号决定已落地**：SM 首次出现注 "(denoted φ in [B11]; we follow the θ notation of [V&V 1983])"，σ²_θ 注 "(= σ²_p in [B11])"

## 下一步干什么

D-W3W4（writing-campaign-plan.md §2 W3 + W4，一个对话合并）。**先读 R012 §III + §IV 大纲 + R011 公式清单 + R010 §3/§4 力度**。

### W3 写 Method（用 R012 §III 大纲 + R011 公式清单）

1. **DA 估计器（公式 1）**：θ̂_DA = angle(r_p · p\*)，一句话解释 "removes modulation by dividing the received pilot sample by the known pilot symbol"。代码 `_recovery.py:153`。（对齐 R010 §2.3 = 直接给结论级）
2. **NDA 估计器（公式 2）**：θ̂_NDA = (1/M₀) angle(Σ_k r_k^{M₀})，一句话 "raises the received samples to the M₀-th power to remove modulation"。代码 `_recovery.py:213,232-233`。引 V&V 1983 + squaring loss 文字结论（**不推导**，R009 原则）。
3. **per-block SNR + 切换规则（公式 3）**：γ_blk = |h_b|²·E_s/N₀；切换规则（文字，不编号公式）："select θ̂_DA when γ_blk < γ_th, else θ̂_NDA"。切换 = **自适应选优**（R008），用文字+框图描述（**不用伪代码**，R010 §3.1）。
4. **创新点定位**（1 段，R010 §3.2）：切换 = "per-block SNR 驱动的 DA/NDA 自适应选择"，定位=量化归因型（R009/D005 务实路线）。**不夸"提出新算法"**（会议论文不吹）。

**W3 公式**：DA（公式 1）+ NDA（公式 2）+ per-block SNR（公式 3），全直接给结论级，标代码行。**切换单独不算公式**，用文字描述。
**W3 图表**：Fig.1 框图已在 §II；切换流程用文字（R010 §3.1：文字+框图非伪代码）。

### W4 写 Results（用 R012 §IV 两段式大纲）

**§IV-A 影响分析（湍流对 DA/NDA 各自性能的影响）**：
1. BER 曲线呈现（Fig.2，6 子图）：DA/NDA 各自 BER vs SNR，分场景。纵轴不硬凑 1e-5（对齐 Paillier，R004/H002）。加 AWGN 理论线隐式 baseline（对齐 Johst）。
2. crossover 数据事实（Fig.4）：DA/NDA BER 曲线有交叉点，交叉点随湍流左移（weak 17.9 / mod 16.8 / strong 10.7 dB）。**只呈现数据不附物理归因**（R009）。

**§IV-B 方法增益（切换的增益数字）**：
1. 切换 vs 固定 NDA（低 SNR 避险）+1.3~2.3 dB（正文，net 口径，CI 下界全正）
2. 净增益量化归因（Tab.1）：强湍流/上行 naive +1.26~1.85 dB；弱湍流 naive 归零诚实标注（+0.09/0.18/0.19，CI 重叠，不变量 3）
3. 切换选对率 26/29（data 口径，R008）

**W4 数字**：crossover 17.9/16.8/10.7（§IV-A）；切换 vs NDA +1.3~2.3 / 净增益 +1.26~1.85 / 选对率 26/29（§IV-B）。
**W4 图表**：Fig.2（BER 主图）+ Fig.3（净增益方案）+ Fig.4（crossover）+ Tab.1（增益汇总）。

## 纪律（和下一步直接相关的约束）

1. **术语/符号跟 R011 三表一致**（零容忍偏差）——W3 公式用 θ̂_DA/θ̂_NDA/γ_blk/γ_th，W4 用 P_b（BER）。照抄 R011，不发明新词/新符号
2. **数字跟 R012 一致**（口径/来源）——W3 可提 M₀=8（公式里）；W4 报 crossover 用 data 口径（17.9/16.8/10.7）/ 切换 vs NDA 用 net 口径（+1.3~2.3）/ 净增益用 naive 口径（+1.26~1.85 标脚注）/ 弱湍流归零诚实标注（+0.09/0.18/0.19 CI 重叠）
3. **力度对齐 R010**——W3 Method 文字+框图非伪代码（5/5 篇无伪代码）/ 公式直接给结论级（对齐 Panasiewicz）/ 创新点定位弱声明（对齐 Johst，会议论文不吹）；W4 BER 主图纵轴不硬凑 1e-5（对齐 Paillier）/ 加 AWGN 理论线隐式 baseline（对齐 Johst）/ Tab.1 只强湍流 3 行 naive（增量亮点）
4. **切换 framing 统一"自适应选优"**（R008）——W3 切换规则描述 + W4 §IV-B 选对率 26/29，禁"鲁棒性补丁"残留
5. **crossover 只呈现数据不附物理归因**（R009 不变量 7）——W4 §IV-A 只报交叉点数字，不解释为什么左移
6. **squaring loss 引 V&V 1983 标准结论不推导**（R009）——W3 NDA 估计器段引 V&V 1983 即可
7. **句式参照 writing-patterns-conference.md**——W3 公式引入用 §1.x / 参数解释用 §2.x；W4 方法对比用 §4.x / 数值嵌入用 §3.x
8. **守 FR-22**——写作不跑新实验

## Results 风险防范（主控指令，W4 必读）

Results 写得"**对解读不敏感**"：
- **主体**：BER 曲线呈现 + HD-FEC(3.8e-3) 处增益数字（解读无关硬事实）
- **标记区**（集中放"待导师确认"）：纵轴范围 / 标题数字 / 1e-5 底线解读
- 导师翻 A（1e-5 必须有增益）只动标记区，主体 BER 呈现不用重写

## W3 要用的（Method）
- **大纲论点**：R012 P3-A §III（DA + NDA + per-block SNR + 创新点定位）
- **公式**：R011 公式清单 #1 DA（θ̂_DA=angle(r_p·p\*), `_recovery.py:153`）+ #2 NDA（θ̂_NDA=(1/M₀)angle(Σr^M₀), `_recovery.py:213,232-233`）+ #3 per-block SNR（γ_blk=|h_b|²E_s/N₀）
- **切换规则文字**（不编号）："select θ̂_DA when γ_blk < γ_th, else θ̂_NDA"
- **切换 framing = 自适应选优**（R008）
- **力度**：R010 §3.1（文字+框图非伪代码）+ §3.2（创新点定位弱声明）

## W4 要用的（Results）
- **大纲论点**：R012 P3-A §IV（两段式 §IV-A 影响分析 + §IV-B 方法增益）
- **数字**：R012 P2-B #5（切换 vs NDA +1.3~2.3 net）/ #1-4（净增益 strong+1.26/up_str+1.85/up_mod+1.19 naive + 弱湍流归零 +0.09/0.18/0.19）/ #7（26/29 选对率）/ #8（crossover weak17.9/mod16.8/strong10.7 data）
- **图表占位**：Fig.2（BER 主图 6 子图）+ Fig.3（净增益方案）+ Fig.4（crossover）+ Tab.1（增益汇总，只强湍流 3 行 naive）
- **力度**：R010 §4.1（BER 主图纵轴不硬凑 1e-5 + AWGN 理论线）+ §4.2（正文 dB + Tab.1 增量亮点）+ §4.3（DA/NDA 两曲线同图对比融 Results 文字段，不专列对比节）

---
## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（黑话禁令 / crossover 只呈现数据 / A4 数据诚实标注 / 切换 framing 自适应选优 / deep fade = 斜率变缓非伪地板）
- [ ] 已验证本文件至少 3 条关键事实声称：
  - [ ] W001 Intro+SM 正文存在（读 W001 目录确认两节正文 + 交叉检查 6 项）
  - [ ] Intro 贡献句 verbatim R008 关键短语（grep "locally optimal estimator in 26 of 29" 确认）
  - [ ] SM θ 符号注 B11 对应（grep "denoted φ in [B11]" 确认 + grep "σ²_p in [B11]" 确认）
- [ ] 已检查 _registry.yaml 中本专题无 conflicts_with
- [ ] 已确认当前范围未违反"明确不含"（W3/W4 写正文是 writing-campaign-plan 的正文写作活，在写作专题范围内，不跑实验不进 Contract）

## 下一轮

D-W3W4：Method（W3）+ Results（W4）正文。一个对话可合并完成。W3 用 R012 §III 大纲 + R011 公式清单（DA/NDA/per-block SNR 三公式）；W4 用 R012 §IV 两段式大纲 + 数字（crossover/切换增益/净增益/选对率）+ Fig.2/3/4/Tab.1 占位。**W4 守 Results 风险防范**（对解读不敏感，主体 BER 呈现 + HD-FEC 增益硬事实，纵轴范围/标题数字集中标记区）。规矩见 writing-campaign-plan.md §2 W3 + W4。
