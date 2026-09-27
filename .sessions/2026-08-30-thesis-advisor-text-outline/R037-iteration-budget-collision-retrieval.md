# [R037] 迭代预算控制方向的定向碰撞检索（九字段占位判定）

> 2026-09-27 | 关联：专题 2026-08-30-thesis-advisor-text-outline / PROMPT-027 / D059 / D060 / R036 §五§六 / R027 §三卡1第7条§七 / R035
> 边界：检索+精读对话，零实验/零代码/零论文正文；与 PROMPT-028（R038/V043/D062）并行，未触碰其实任何文件。

## 三行结论（先读这个）

1. **创新点表述合法性边界**：①"基于校验子轨迹的**跨帧**双向判决规则（无望帧预测中止 + 省下预算追加给边际帧）"——**可写"未见文献报道"**（本轮三簇 154 条 + 在库六篇 + 2026-09-14 既有 7 slug 中零命中；唯一具备"省下迭代显式转移"的是 GC-LDPC ET-2，但为**码字内**两相位间转移，原文无任何帧间语义，见 §二 N01）；②"校验子轨迹作为接收端可见控制信号"——**必须写"近邻存在"**（GC-LDPC v1 判据 / CV-QKD SVP 双文 / GA-OMS ΔS 三态 / bootstrapped 振荡停，四族在案）；③"湍流 FSO + 5G NR LDPC + FER-平均迭代 Pareto"场景组合——**组合口径可写未见，单要素必须引邻居**（LNET2026 已做 5G NR LDPC+NMS+FSO 三档+5km 实测但机制为固定最优因子；bootstrapped 2023 已做 FSO 三档湍流+平均迭代指标但硬判决族+单向停）。
2. **占位统计**：占位 0 篇；部分占位 7 篇（强 1 / 中 2 / 弱 4）；暂不可判 1 篇（TVT2026 早停，摘要与全文四通道均缺，唯一可能翻案的悬置项）；其余不占位（族谱引用）。**最危险一篇 = GC-LDPC ET-2（Sensors 2024，10.3390/s24216893）**——全库唯一"预测性砍（syndrome 派生判据早停）+ 省下预算显式转移续（I_GT 公式）+ 复杂度/性能双收益"完整闭环，与我们的差异仅剩两点：转移粒度（码字内相位间 vs 跨帧）与场景（AWGN/QPSK/GC 结构 vs FSO 湍流帧异质/5G NR BG2）。
3. **对 PROMPT-028 的建议**：五臂 Pareto 设计**维持不变**（GC-LDPC 的码字内转移依赖 GC-LDPC 两层结构，非 GC 码不可移植，无需加臂）；但判决规则的**消融设计**应补两个对照变体——(a) 纯标量阈值判据（GC-LDPC C1 型校验满足比例 v1 逐迭代阈值比较）对照我们的轨迹特征判据；(b) 若规则含振荡检测，须与 bootstrapped 2023 的 3-移位寄存器振荡停同型判据做区分消融（同场景最近邻居，防"规则=振荡停"的合并质疑）。另有写作引用区隔清单见 §五。

---

## 一、检索与证据基础

- **三查询簇六条检索**（2026-09-27，tools/search，自动入档，S2+OpenAlex+arXiv+SerpAPI 源）：A1 停机准则（30 条）/ A2 变迭代分配（30）/ B1 衰落帧级迭代分配（21）/ B2 可靠度两阶段重译码（23）/ C1 FSO 湍流自适应 FEC（30）/ C2 光 SD-FEC GG 实时（20），合计 154 条、153 条带摘要。
- **摘要级三档筛查**（三子 agent 独立执行）：T1 必查 17 条 / T2 族谱 56 条 / T3 无关 81 条；对载荷大的条目做 S2 / OpenAlex / Crossref 摘要交叉验证（8 条 PASS、2 条部分、2 条未验证已标注）。
- **全文获取**：成功 4 篇入库（GC-LDPC Sensors 2024 / Sci Rep FSOCS 2026 / GA-OMS Research Square 预印本 / ——R-SCFlip 的 arXiv 通道抓错论文已清理，按摘要级处理）；在库全文复用 2 篇（bootstrapped 2023、L01–L06 读笔记）。**IEEE 付费墙 202 网关持续拦截**（blit 通道搜索可用、PDF 拒发），WCL22 / TVT19 / TVT2026 / LNET2026 / adNMS×2 全文缺口按 R027 §二先例登记。
- **在库消化复用**：R029 发现四已对救援族（L04–L06 + EURASIP 2023）做过碰撞判定（"五篇收益全在低错误率区、FER 0.1–0.3 无数据、NO_COLLISION 两处部分重叠"），本报告直接引用不重推导。

## 二、逐邻居九字段对照

九字段：处理对象 / 动作规则 / 场景与信道 / 码型与帧结构 / 指标 / 对照设置 / 报告增益 / 与我们的差异 / 判定。判定口径：**占位**=机制+场景+动作完整重合；**部分占位**=同机制不同场景或同场景不同机制；**不占位**。

### 部分占位·强（1 篇）

**N01 · Two-Phase GC-LDPC Decoding Aided with ET and Forced Convergence（Sensors 2024, 10.3390/s24216893；全文已精读，读笔记 papers/_read_notes/10.3390_s24216893.md）**
- 处理对象：GC-LDPC 单码字的两相位译码（局部层 IL=40 并行 → 全局层 IG=10）。
- 动作规则：ET-1 局部相早停——C1 判据=校验满足比例 v1=1−‖s‖₀/(n−k) 下降或连续 T 次不升；C2 判据=大幅值 LLR 比例 v2<0.39（ROC 曲线定阈值）。ET-2 预算转移——省下的局部迭代转全局：I_GT=⌈(I_L−Î_L)·ϑ⌉，ϑ=d_L/(d_G·t) 为层间度比折算。FC/AFC=全局相节点消息冻结。
- 场景与信道：AWGN + QPSK，无衰落、无帧级异质。
- 码型与帧结构：GC-GCD-LDPC n=6591、r=0.7519、P=169（另测 n=3000–12000、r=0.66–0.85）。
- 指标：平均时间复杂度、BER/FER。
- 对照设置：常规两相译码、C0/C1/C2 判据变体、FC/AFC。
- 报告增益：ET-1 低 SNR 省 42.19% 复杂度无性能损失；ET-2 同复杂度 BER +0.18dB / FER +0.23dB（仅 IG 受限时）；ET-2-FC 瀑布区再省 ~25%。
- 与我们的差异：机制同族（syndrome 派生判据的预测性砍 + 省下预算显式转移续）但**转移发生在同一码字内部（局部相→全局相），由 GC-LDPC 两层结构驱动，无跨帧语义、无按帧难度/信道状态差异化分配的任何表述**（原文证据："The number of decoding iterations saved by ET-1 translates into I_GT… I_GT=⌈(I_L−Î_L)ϑ⌉"，Î_L 为当前码字局部相终止迭代号）；v1 判据信号与我们 syndrome 轨迹**同源**，但用法是单次译码内逐迭代标量阈值比较，非跨帧轨迹分类。
- 判定：**部分占位（强）**。若我们贡献表述只写"早停+预算重分配"而不突出**跨帧**与**帧级衰落异质**，会被此篇占住。

### 部分占位·中（2 篇，机制同核=校验子轨迹驱动迭代决策）

**N02 · High-speed information reconciliation with syndrome-based early termination（Opt. Express 2023, 10.1364/oe.494078；摘要级，S2+OpenAlex 双验证）**
- 处理对象：CV-QKD 信息协调 LDPC 译码帧。动作规则：研究校验子变化模式（SVP）与帧错误率的关系 → SVP 早停 + 按实时译码状态**自适应调整迭代数**；另只算 Raptor-like 最高码率部分校验子省算力。场景与信道：CV-QKD 后处理（非通信衰落信道）。码型：多维协调 Raptor-like LDPC。指标：信息吞吐量、FER。对照：固定迭代译码。增益：吞吐提升（摘要截断，正文未取）。差异：信号源与我们同核（SVP=syndrome 轨迹），但**单向砍（早停/自适应减迭代）无预算重分配**、场景为 QKD。判定：**部分占位（中）**。

**N03 · High-speed reconciliation with convergence-based early termination（Opt. Express 2026, 10.1364/oe.581729；摘要级，双验证）**
- 同组延续：SC-LDPC 构造 + 按 SVP 的**不同收敛行为分类**，自适应调整迭代数（C-ET），自称较 N02 进一步降时延。C-ET 使信息吞吐 +292%。差异同 N02——"轨迹分类→差异化迭代"与我们思路最接近，但分类只决定**何时停**，不决定**把省下的预算给谁**；场景 QKD。判定：**部分占位（中）**。

### 部分占位·弱（4 篇，场景侧邻居）

**N04 · Bootstrapped low complex iterative LDPC decoding for FSO（EURASIP JWCN 2023, 10.1186/s13638-023-02285-w；在库全文，R027 已获取）**
- 处理对象：LDPC 码字，WBF/IERR/Min-Sum 族。动作规则：syndrome 驱动 bootstrap 初始化（校验子非零位定位不可靠校验节点→邻域最小软值 VN 定向更新）+ **振荡检测停止**（3 位移位寄存器比对第 1/3 次 syndrome 态，相同即停）。场景与信道：**FSO 弱/中/强三档湍流**（LN/G-G，Cn²=0.5/2/5×10⁻¹⁴）+指向误差，OOK，1550nm/1km。指标：BER、**平均迭代数**、收敛、译码时间、吞吐。对照：WBF/IERR/Min-Sum。增益：弱/中湍流较 WBF ≥3dB、较 IERR ~1dB，逼近 Min-Sum。差异：**场景要素最像**（三档湍流+平均迭代数为指标+syndrome 驱动早停），但只有砍臂（振荡停）无续臂、无预算重分配；硬判决族、非 5G NR、非相干 DP-16APSK。判定：**部分占位（弱）**。R029 已对本篇做过救援线碰撞判定（NO_COLLISION）。

**N05 · Enhancing FSO CubeSat links using low-complexity LDPC decoding（Sci Rep 2026, 10.1038/s41598-026-68721-1；全文已读）**
- 处理对象：N=1024、R=1/2 QC-PEG LDPC。动作规则：梯度比特翻转（硬判决族）+ syndrome 驱动 bootstrap 初始化；**全部译码器统一 Imax 上限**（25/30/50/200 按信道），终止=syndrome=0 或达上限——原文立场"superior algorithmic pathing rather than an extended iteration budget"（算法路径优于扩预算）。场景：星间/星地 FSOCS，cirrus/thin-cirrus + exponentiated Weibull（正文）与 G-G+AWGN（表格，两处表述不一致）。指标：BER、平均迭代数、译码时间、吞吐。增益：星间 ~1dB@BER 1e-6、距 Min-Sum 0.5dB 内；上行 cirrus 较 LCRR ≥2dB。差异："fewer iterations"=平均迭代-vs-Eb/N0 曲线对比（好初始化的自然结果），**无任何逐帧迭代数控制规则**；统一 Imax 反证无预算操作。判定：**部分占位（弱）**。作者与 N04 同（Youssef 系）。

**N06 · A 5G-NR LDPC Decoder with Optimal-NMS Technique for FSO（IEEE Networking Letters 2026, 10.1109/lnet.2026.3712775；摘要级，S2 验证）**
- 处理对象：5G NR LDPC 译码器。动作规则：**固定最优归一化因子 ξ**（"ξ constant for all the iterations in the layered decoding process"），面向实时性。场景与信道：**FSO clear/moderate/strong 三档 + 5km 开放场地数据链实测**，10dB SNR 下维持 BER 1e-7。指标：BER、复杂度。差异：**场景撞车最重**（5G NR LDPC + NMS + FSO 三档 + 实测，与我们的码/调制解调域/场景几乎全同），但机制为因子优化，**无迭代控制、无判决规则、无预算概念**。判定：**部分占位（弱，场景侧）**。注意作者组与 N07 疑似同组（DOI 相邻）。

**N07 · Adaptive Channel Coding and Power Control for Practical FSO Under Channel Estimation Error（TVT 2019, 10.1109/tvt.2019.2916843；摘要级，OpenAlex 验证）**
- 处理对象：发端编码率/发射功率。动作规则：按 CSI 自适应调码率（独立或与功率联合），最小化发射功率 s.t. 目标 BER/outage/最大功率；G-G 湍流闭式吞吐/功率表达。差异：**发端链路层自适应 vs 我们接收端译码器内部预算控制**，动作层正交；但其"按信道状态分档适配"叙事与我们同场景同思路，必须引用区隔。判定：**部分占位（弱）**。

### 暂不可判（1 篇，唯一悬置项）

**N08 · A Low-Complexity APSK Iterative Receiver With Convergence- and Oscillation-Aware Early Termination Strategies（TVT 2026, 10.1109/tvt.2026.3712765 = ieeexplore 11606454；摘要截断+全文四通道均缺）**
- 已知信息（2026-09-14 存档 serpapi 片段 + blit 元数据 + Crossref 作者）：BICM-LDPC 迭代解调译码接收机、Max-Log 近似降复杂度、32-APSK、收敛感知+振荡感知早停双策略；作者 Xian Yunzhu, Ding Xuhui, Gao Xiaozheng, Li Gaoyang, Yang Kai, An Jianping（疑似北理工组）；2026-07-13 入刊，与 N06 DOI 相邻。
- 摘要不可判项：两策略的判据信号（是否校验子/LLR 轨迹）、有无无望帧/边际帧双向区分、有无预算重分配、信道场景、增益数字。
- 判定：**暂不可判**。标题四要素（迭代接收机 BICM-ID + 收敛感知 + 振荡感知 + APSK）与本方向强相关，是 17 个 T1 里唯一可能在"双向判决规则"维度构成实质重叠者。**处理纪律**（沿用 R027 §二先例）：全文到手前不作为任何表述依据、不引用其机制细节；列入用户手动获取清单（校园网/图书馆通道），拿到后须补九字段+必要时精读。

### 不占位（族谱引用，9 篇摘要级 + 在库 4 篇）

| # | 论文 | 一句话 | 为什么不占位 |
|---|---|---|---|
| N09 | GA-OMS BG2（ACIS 2026, 10.1155/acis/4082392；RS 预印本 10.21203/rs.3.rs-8646460/v1 全文已读） | offset 参数 β 按 SNR 档+迭代指数+校验节点度自适应，syndrome 权重改善量 ΔS 三态（保持/微调/GA 重搜），Rayleigh | 码型同（BG2）、信号同核（ΔS=syndrome 轨迹），但**动作=调译码参数非调迭代预算**，I_max 固定；预印本未经评审。引用区隔"syndrome 轨迹作控制信号"时必须带上它 |
| N10 | ALEMS 短码自适应分层（CECCC 2025, 10.1109/CECCC68691.2025.00008） | 分层调度+改进 Min-Sum 核+常规早停，AWGN+Gilbert-Elliott 突发信道，fewer iterations | 机制=调度+核改进+教科书早停（无判决规则/无重分配）；突发信道是场景近邻，作引用 |
| N11 | GCLDPC 自适应 NMS（ICCC 2025, 10.1109/ICCC65529.2025.11149292）= PROMPT-027 "adaptive-NMS GCLDPC 2025" 身份落定 | GC-LDPC 两级译码 + 按 LLR 极化度动态调归一化因子，AWGN+Flash | 机制=因子自适应；与 N01 同 GC-LDPC 两级结构家族，佐证"码字内两级"是既有范式 |
| N12 | Improved Layered NMS 5G NR（WCL 2022, 10.1109/lwc.2022.3192518；OpenAlex 摘要已补全） | 利用 5G 传输块比特结构 + DNN 求最优归一化因子，+0.3–1.9dB，无乘法器开销 | 码型同、机制不同（DNN 定因子）；卡 1 时代的邻居，迭代预算维度无关 |
| N13 | Convergence behavior + Early Give-Up（2018，无 DOI） | 译码器内部统计量（平均 LLR 幅度/校验满足比例）检测不可收敛→提前放弃，代价=重传 | 砍分支的机制近邻（预测性放弃），但单向、无重分配、无 FSO；建议引用 |
| N14 | ET for 5G NR LDPC（2021，无 DOI） | 分层 QC-LDPC 新早停，平均迭代 −18.7%（vs SDC/HDS）+0.2dB | 单向砍、5G NR 码型同；族谱引用 |
| N15 | ML-based ET turbo/LDPC（2021，无 DOI） | ML 分类器识别应停迭代轮次，ANI 降 25–57% | 机制（ML 分类）与场景均不同；族谱引用 |
| N16 | Condo 博士论文（2014, 10.6092/polito/porto/2544356） | 多标准 LDPC 早停判据：度量演化+在线阈值，按省迭代/能耗评估 | 硬件能耗视角的早停综述性工作；FPGA 叙事可引 |
| N17 | R-SCFlip 极化码 JSCD（ACM 2022, 10.1145/3502208；摘要级——arXiv 通道抓错论文已清理，题文不符教训见 §四） | CRC 失败后翻转低可靠比特的接收端内部重试（SCFlip 族），Rayleigh 结论 | "续"臂的失败重试族近邻，但对象=极化码路径翻转非迭代预算；族谱引用 |
| L03 | Wu 2010（10.1109/lcomm.2010.07.100508，在库读笔记） | satisfied/unsatisfied check 切换 normalization/offset | syndrome-state 祖先，参数自适应非迭代控制；不占位（R029 在案） |
| L04–L06 | Baldi 2016 / He 2021 / Zhao 2023（在库读笔记） | 失败码字门控救援族（IA→MRB / TS flips / narrowed SBF） | 我们"续"臂的救援族；R029 已判：收益全在低错误率区、FER 0.1–0.3 无数据、NO_COLLISION 两处部分重叠——引用该判定 |
| — | 2018 无 ID 二篇、Naidoo 2012 博士论文（BP-OSD-Chase 两级） | 强二次译码族 | B 簇筛查判 T1 但无标识符/无验证，机制=结构性级联非按帧判决触发；登记不展开 |

## 三、检索覆盖说明（查了什么/没查什么）

**查了**：
- 英文关键词空间：LDPC/Turbo 停机准则与早停（A1）、变迭代数与迭代分配（A2）、衰落信道帧级迭代分配与两阶段重译码（B1/B2）、FSO/湍流/光 FEC 自适应译码与 SD-FEC 实时（C1/C2）——六查询共 154 条，T1 筛出 17 条全部九字段化。
- 交叉验证：载荷大的 13 条经 S2/OpenAlex/Crossref 摘要独立核验（PASS 8 / 部分 2 / 未验证 3 已标注）。
- 既有资产复用：2026-08-30 在库六篇（L01–L06 读笔记）、2026-09-14 七 slug 存档（邻居身份从中落定：N08/N09/N11/N12）、R029 救援族碰撞判定。

**没查（诚实边界）**：
1. **中文文献（CNKI/万方）零检索**——学位论文查重语境下中文邻居（如国内 LDPC 早停/迭代控制硕博论文）未覆盖，建议补一轮 `tools/blit --source cnki --doc-type phd,master`。
2. **IEEE 全文五篇缺口**（N06/N07/N08/WCL22 已列/adNMS×2）：blit 搜索通道恢复但 PDF 网关 202 拦截；其中 **N08（TVT2026）是唯一可能改变本报告结论的项**，建议用户校园网手动获取。
3. **双向引用链未展开**——未对 N01（GC-LDPC ET）做 forward citation 追溯，不能排除 2025–2026 有跟进者把"码字内转移"搬到衰落/FSO；建议补一轮 `tools/search --citations 10.3390/s24216893 --citations-direction forward`。
4. **专利库未查**——"工程实现查重"维度（判决规则是否已被专利占位）超出本轮范围，FPGA 层创新点子句暂不能写"未见"。
5. SerpAPI 抓取的摘要存在串文风险（B 簇 7 条已降权处理），T1 内已用双源验证对冲。

## 四、过程事故登记（数据完整性）

- **R-SCFlip 下载题文不符**：papers/doi/10.1145_3502208 经 arXiv 标题匹配通道抓到 arXiv:1601.06184（JSCD 极化码语言信源，同组前作），九字段子 agent 通读时发现。处置：删除该目录，R-SCFlip 降为摘要级（B 簇子 agent 已给摘要级九字段，S2 验证 PASS）。教训：arXiv 通道按标题模糊匹配下载后必须过 title_check 才入库引用。
- **失败目录保留**：10.1155_acis_4082392（Wiley Cloudflare）、10.1364_oe.494078/581729（Radware 验证码）等目录保留 failed metadata.json（与库内 10.1002_sat.1553 先例一致），反爬 HTML 伪 source.pdf 已清除。
- **Sci Rep 正文信道模型两处不一致**（exponentiated Weibull vs G-G+AWGN）：九字段按"正文 EW、表格 G-G"如实登记，不影响判定。

## 五、对 PROMPT-028 与写作的建议

1. **实验设计**：五臂 Pareto（B0 固定 / B0+ES / NOMS+ES cap50 / cap200 / R3）维持——三簇检索未产生需要新增的对照臂（无同场景同机制对手）。**判决规则消融**建议补两变体：(a) GC-LDPC C1 型标量阈值判据（v1 逐迭代阈值）vs 轨迹特征判据；(b) 振荡停判据 vs bootstrapped 3-移位寄存器型。目的：证明"规则的信息量"住在轨迹特征里，不在教科书判据里——这正是 D060 "纯早停+上限=教科书配置不算方法"口径的实验支撑。
2. **论文表述口径**（创新点句式的安全写法）：
   - 可写未见：`跨帧`双向预算重分配判决规则；湍流 FSO 场景下 FER-平均迭代 Pareto 的迭代预算控制方法（组合口径，限本轮检索范围+中文/专利/前向引用三缺口如实挂边界）。
   - 必须写近邻存在并区隔：早停族（商用标配）；码字内预算转移（N01，区隔点=跨帧+结构无关）；syndrome 轨迹自适应迭代（N02/N03，区隔点=场景+单向）；syndrome 轨迹调参（N09，区隔点=动作对象）；FSO+5G NR LDPC+NMS（N06，区隔点=固定因子无规则）；FSO 湍流+平均迭代指标（N04/N05，区隔点=硬判决族+单向停）；发端自适应编码（N07，区隔点=接收端内部）；救援族（L04–L06，区隔点=R029 在案）。
3. **待用户动作**（按优先级）：①校园网获取 N08（TVT2026）全文——唯一悬置项；②中文硕博一轮检索；③N01 forward citation 一轮（防跟进者搬场景）。
4. **对 D059-4 / R036 §六-4 的输入**：创新点"组合空位"表述现已有限实底——"机制×双向规则×场景"三维组合在英文检索空间零占位，但**三维中任何单独一维都有近邻**，论文创新点句必须写成组合句式（"在 X 场景下首次给出 Y 规则实现 Z"），不可写单要素首创；FPGA 维未查。

## 六、slug 清单附录

本轮新建检索存档（search-archive/2026-09-27/）：
- p027-a1-ldpc-stopping-criteria.json（=ldpc-decoder-early-termination-stopping-criteria-convergence.json）
- p027-a2-variable-iteration-decoding.json（=adaptive-variable-iteration-number-ldpc-turbo-decoding-compl.json）
- p027-b1-frame-iteration-allocation-fading.json（=frame-level-iteration-allocation-ldpc-decoding-fading-channe.json）
- p027-b2-reliability-two-stage-redecode.json（=reliability-based-iterative-decoding-two-stage-retransmissio.json）
- p027-c1-fso-turbulence-adaptive-fec.json（=free-space-optical-turbulence-ldpc-decoding-adaptive-iterati.json）
- p027-c2-optical-sdfec-gg-realtime.json（=optical-communication-soft-decision-fec-decoding-gamma-gamma.json）
- p027-neighbor-download-batch.json（邻居批量下载批次）

复用存档：search-archive/2026-09-14/（iterative-demapping-decoding-bicm-apsk-ldpc / normalized-min-sum-offset-ldpc-decoding-improvement{,-fading} / ldpc-decoding-free-space-optical-atmospheric-turbulence-fadi / erasure-marking-decoding-ldpc-fading-channel / received-power-csi-aware-decoding-allocation-free-space-opti）；search-archive/2026-08-30/（t049/t050/t079 系列）；search-archive/_index/all-papers.jsonl（自动增量，21580→21665+）。

本轮新入库全文（papers/doi/）：10.3390_s24216893（content.md 含精读级信息量 + source.xml + 读笔记）；10.1038_s41598-026-68721-1（content.md+source.pdf）；10.21203_rs.3.rs-8646460_v1（content.md+source.pdf，N09 预印本）。

## 结论

R036 §六-4 登记的创新点论证 NOT_CHECKED 块已补成实底：三簇定向检索 + 17 个 T1 邻居九字段化 + 1 篇全文精读（GC-LDPC ET）后，**占位 0 / 部分占位 7（强 1 中 2 弱 4）/ 暂不可判 1（TVT2026，全文缺口）**。"跨帧双向判决规则 × 湍流 FSO × FER-迭代 Pareto"的组合空位在英文检索空间成立，但机制、场景各单维均有近邻必须引用区隔；最危险邻居 GC-LDPC ET-2 的差异锚点=码字内转移 + AWGN + GC 结构依赖（均经原文证据句核实）。悬置项与三个补查缺口（中文/前向引用/专利）如实登记，不阻断 PROMPT-028 实验线。

## 对决策的影响

- 建议 D061 落账：占位判定结论 + 创新点表述口径（组合句式+区隔清单）+ TVT2026 悬置项处理纪律 + 对 PROMPT-028 消融建议——供导师材料与实验对话引用。
- D059-4（迭代预算控制 DSP 身份）与 R033 §六①收口不受本轮影响（文献占位性与 DSP 身份是两个正交问题，后者仍归导师拍板）。
- 本轮零实验/零代码/零论文正文/零 PROMPT-028 文件触碰。

---

## 附记（2026-09-27 同日补充，回应用户"检索够不够/算不算创新"追问）

- **前向引用补查完成**（D061-5 ②项）：GC-LDPC ET-2（10.3390/s24216893）forward citations 仅 2 条——Entropy 2026 ADMM 译码（同 GC-LDPC 家族、prior-assisted 分层 ADMM，非迭代预算转移）+ 数据库噪声 1 条。**"码字内转移被搬到衰落/FSO/跨帧"的跟进风险排除**（存档 p027-fc-gc-et-forward.json）。
- **CNKI 补查尝试失败（通道层）**：blit CNKI 对多词技术查询返回完全无关结果（"LDPC 迭代 提前终止"返回民族服饰/基因编辑类），单宽词通道正常——判定为通道相关性匹配故障而非真实空库。中文硕博缺口维持开放，需人工在知网检索（建议词：迭代次数分配/提前终止+LDPC、湍流+LDPC 译码、变迭代数译码）。
- **结论强度更新**：D061 判定不变（占位 0/部分占位 7/暂不可判 1），但"码字内→跨帧无人跟进"由"未查"升级为"已查、干净"；四个缺口收敛为三个（TVT2026 全文/中文硕博人工/专利）。
