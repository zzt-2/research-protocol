# L02 全文精读：Enhanced Frame Synchronization and Carrier Recovery in Coherent FSO Communication

> Groundwork Step 3｜single-paper reader｜2026-08-09
> 阅读边界：仅依据指定 `content.md` 与 `metadata.json`；未读取旧 read-note，未检索外部资料。
> 当前阶段：`DIAGNOSE`（事实提取与证据定位），不做 RML-FSTS 设计、novelty/Go 判断或 Step 3.5/4a 工作。

## 0. Preflight

| 检查项 | 结果 | 证据 |
|---|---|---|
| 派遣标题 | PASS；正文标题一致，仅大小写规范不同 | `content.md:14`；`metadata.json:13` (`real_title`) |
| DOI | PASS：`10.1364/OE.520452` | `content.md:10`；`metadata.json:3,5` |
| canonical 路径 | PASS | `D:\code\study\research-protocol\papers\doi\10.1364_oe.520452\content.md`；`metadata.json:11` |
| 正文完整性 | PARTIAL-PASS：有摘要、正文 5 节、28 条参考文献、20 图/2 表/21 公式入口；但转换结果丢失全部公式本体和两表内容 | `content.md:142-160,165-507,507-609,623-866` |
| metadata 质量 | 下载成功、HTML、质量标 `good`；metadata 的 `title` 为空且 `title_check=unverifiable`，但 `real_title` 与正文标题直接匹配 | `metadata.json:4,7-10,13-14` |

结论：不是 title/DOI/path mismatch，也不是无法阅读的损坏正文，继续精读；公式与表格缺失作为明确证据限制保留。

## 1. 书目信息与学术身份

1. **DOI/来源**：DOI `10.1364/OE.520452`；来源为 Optica Publishing Group 的期刊全文页抓取，metadata 记录下载方式为 `firecrawl_scrape`、内容类型为 HTML。（`content.md:5-10,53`；`metadata.json:3,5,8-9`）
2. **canonical 源路径**：`D:\code\study\research-protocol\papers\doi\10.1364_oe.520452\content.md`；对应 metadata 为同目录 `metadata.json`。（`metadata.json:11`）
3. **发表状态**：已正式发表、开放获取；原稿 2024-02-01，修订 2024-05-02，接收 2024-05-20，发表 2024-07-02。（`content.md:38,131-138,169`）
4. **发表渠道**：Optics Express，Vol. 32, Issue 15, pp. 25560–25580。（`content.md:5-10,53`）
5. **年份/期刊**：2024，Optics Express。（`content.md:5-10,53,136`）
6. **作者/机构**：Liqian Wang、Kunfeng Liu、Siqi Zhang、Shuang Ding；北京邮电大学电子工程学院。（`content.md:14-29`）
7. **学术身份/全文验证**：正式期刊 article；题名、作者、卷期页码、DOI、稿件历史、参考文献与正文结构互相闭合。本文不是预印本。（`content.md:5-16,53,131-160,507-609`）

## 2. 核心贡献、方法与结论

### 2.1 核心贡献（含方法细节）

第一，论文把 PRBS 前缀与 16-symbol 周期的定向循环 QPSK 后缀组合成联合训练序列：PRBS 用于逐支路帧同步，QPSK 梳状谱用于粗频偏估计；帧同步采用相邻符号共轭差分并与接收端预置差分序列匹配，以削弱激光线宽相位偏差、调制相位和非同步区旁峰。（`content.md:181,187-205,207-249`）

第二，论文提出两级确定性频偏估计：一级对同步后的周期 QPSK 做 FFT 最大谱峰搜索，利用零频偏参考峰与观测峰之差得到粗估计；二级在 x/y 双偏振之间按相隔 `TL` 的 QPSK block 交叉共轭，利用同信息/相反排列特征细化残余频偏，最后补偿接收数据。（`content.md:251-272,283-312`）

第三，论文显式扫描训练长度与 block 长度，而非固定沿用已有方法的 1024 symbols；正文将 480 symbols 选为精度—开销折中，并声称二级运算复杂度为 `4N`、同等帧同步表现可节约约 100 symbols。（`content.md:181,321-325,393-404,440,497`）

### 2.2 方法概述（2–3 句）

接收机先对联合 training 的 PRBS 段构造归一化差分 timing metric，以主峰位置给出每支路 frame start；再截取循环 QPSK 段，以 FFT 谱峰偏移得到范围为 `[-3Rs/8, 3Rs/8]` 的一级 CFO。（`content.md:205-219,231-249,251-272`）随后在 MRC 后利用双偏振、跨 `TL` block 的共轭差分完成二级 residual CFO estimation，并对数据补偿；这是非学习型、training-aided 的确定性 DSP。（`content.md:268,283-312,345`）

### 2.3 实验设置

- **仿真平台**：20 km、10 G polarization-multiplexed QAM coherent FSO diversity receiver；发射激光线宽 80 K（原文单位写作 K），PBS 分双偏振，经映射、pulse shaping、DAC、IQ 调制、PBC 后入大气。（`content.md:334-336`）
- **湍流与接收**：随机 phase screens；coupling efficiency 服从 non-central chi-square，phase noise 服从 normal distribution；多望远镜间距大于空间相干长度，孔径 0.2 m；ADC 后下采样，MRC 前做最优支路对齐式 phase precorrection。（`content.md:345`）
- **仿真维度**：B2B、单支路/四支路、QPSK/16QAM、弱/强湍流；仿真湍流结构常数分别 `1e-16`、`1e-14`。（`content.md:371-375,413-455`）
- **次数**：帧同步曲线每点 3200 次；多组 FOE/MSE/BER 图每点 800 次。Fig. 12 报 error bar，并给出一处标准差 `2.91466e-9`。（`content.md:351,393-404,431`）
- **实测**：仅 QPSK、单孔径；AWG→IQ modulation→室内 atmospheric path→coherent receiver，发射功率 13 dBm，实验所称弱湍流结构常数 `6e-11`，接收采样率 40 G，MATLAB 后处理；另报告理想室内/B2B 处理后的 BER `1.219e-8`。（`content.md:466-493`）

### 2.4 Baseline（逐项标来源/实现性质）

| 子任务 | baseline | 来源 | 本文实现性质与公平性证据 |
|---|---|---|---|
| Frame synchronization | Park algorithm | 引用 Ref. 11 | 本文仿真复现；未给代码/实现来源。与 proposed 在 320 symbols、相同 received power 下展示 timing curve；复杂度仅比较 `C(d)`，表内容丢失。（`content.md:177,323,351-360,547-549`） |
| Frame synchronization | weighted Park / new constant-envelope preamble | 引用 Ref. 13 | 本文仿真复现；未给代码/调参细节。使用 Park sequence×PN 的加权结构；同一 Fig. 8 条件比较主/旁峰。（`content.md:177,360,551-555`） |
| FOE | traditional TS | 引用型传统方法；相关 training-aided FSO 文献 Ref. 19 | 本文仿真复现，未给外部源码。B2B 中扫描 480/960；系统对比时 TS=480 symbols。（`content.md:179,393-404,422-442,577-579`） |
| FOE | fourth-power FFT / traditional FFT（正文术语有混用） | 引用 Refs. 15–18 | 本文仿真复现，未给外部源码。系统对比中 FFT=960 symbols，而 proposed=480，因而资源预算不完全相同；未报告统一调参协议。（`content.md:179,413-442,561-575`） |
| FOE | Wu et al. 2022 QPSK-TS + secondary fourth-power FFT | Ref. 21 | 引用型 task-matched comparator；本文称原方案使用 1024 symbols，但系统曲线将 Ref. 21 设为 480 symbols；未报告原作者代码或复现校验。（`content.md:179-181,294-306,323-325,442,585-587`） |
| 实测 | 无算法 baseline | N/A | 实测仅显示 proposed 下的 QPSK 单孔径 constellation/eye/BER，没有并列算法实测。（`content.md:466-493`） |

### 2.5 关键结论（仅限论文声称范围）

- 帧同步：高 received power 条件下，同等准确率约节省 100 symbols；正文也承认低 received power 时优势减弱。每点 3200 次。（`content.md:351`）
- FOE 精度：TS 的 MSE 约 `1e-6–1e-7`，proposed 稳定于 `1e-8–1e-9`；超过约 300 QPSK symbols 后边际改善减弱，论文据此选 480。（`content.md:393-404`）
- `TL` 门限依赖 received power 与总长度：在 −45.12 dBm 时，480/960 总长度分别需超过约 64/80 才优于一级；在 −43.12 dBm 时门限约 50/60。（`content.md:404`）
- CFO range：proposed 为 `[-3Rs/8,3Rs/8]`，TS 为 `[-Rs/2,Rs/2]`，第四次幂类为 `[-Rs/8,Rs/8]`。（`content.md:272,422`）
- 480→960 对 proposed 的 BER sensitivity 改善仅约 0.3 dB；换为 16QAM 时同训练长度下各方法约劣化 8 dB。（`content.md:431,440`）
- 单支路 QPSK 曲线中论文报告约 2.9/3.2 dB sensitivity improvement；四支路强湍流下 proposed 相对 FFT/TS 的 improvement 为 QPSK 1.78 dB、16QAM 2.46 dB。四支路相对单支路的 diversity gain（不是 proposed 独占增益）在弱湍流为 8.1/9.5 dB、强湍流为 19.45/17.62 dB（QPSK/16QAM）。（`content.md:451-455,464`）
- 实验只支持室内、QPSK、单孔径场景；`1.219e-8` BER 所在句同时提及理想 indoor/B2B，不能外推为 20 km 或强湍流实测。（`content.md:466-493`）

## 3. 与 RML-FSTS 的关系与适配性

### 3.1 关系

- **FACT**：本文是 coherent FSO 中直接处理 frame synchronization、CFO estimation、双偏振与空间 diversity/MRC 的确定性 DSP，且同时覆盖训练开销、MSE、BER/sensitivity、频偏范围与复杂度；因此可作为 **C2/C4 近期 task-matched comparator**。（`content.md:165-181,205-325,334-497`）
- **FACT**：本文输入是已知 PRBS+循环 QPSK training 与 x/y polarization samples，输出是 frame start 和两级 CFO estimate；没有 lag ranking、conditioned-single-lag selector、DRL 或监督学习。（`content.md:205-219,251-312`）
- **INFERENCE**：它可提供确定性训练序列/同步-频偏恢复的对照口径、参数展示与实验组织原料；这只是 comparator/写作原料定位，不是对 RML-FSTS 的方法建议。
- **UNKNOWN**：本文没有构造或验证星地条件下的 lag-ranking crossover，也没有检验 conditioned-single-lag failure；这两个 target 命题必须保持 `INFERENCE/UNKNOWN`。
- **边界纪律**：本文自身问题成立、canonical 四判据通过，不等于 target Q 成立，不等于 novelty，不等于 Go。

### 3.2 适配性判断

| 类型 | 判断 | 理由 |
|---|---|---|
| 直接适配 | **部分适配** | 同为 coherent FSO receiver DSP、frame/CFO recovery、training-aided、turbulence/diversity；可直接对标 BER、MSE、sensitivity、overhead、range、complexity。（`content.md:167,175,321-345,369-497`） |
| 不适配 | **明确不适配 target 机制证明** | 20 km 仿真/室内实验，不是被验证的星地时变链路；无 lag-conditioned ranking、无 single-lag conditioning failure、无 learning policy。（`content.md:334-345,466-493`） |
| 未来原料启示 | **可用，但只作原料** | 可复用其“训练结构→估计链→复杂度→参数扫描→BER/MSE”的证据组织，以及 C2/C4 comparator 参数口径；禁止据此设计 RML-FSTS 或宣称 target defect。（`content.md:181-183,321-497`） |

## 4. 实现关键细节与证据限制

1. **联合 training**：前缀 PRBS 做 FS，后缀周期 QPSK 同时做 coarse/fine FOE；最小循环 `a` 为 16 symbols，谱线按 `Rs/16` 相关间隔出现。（`content.md:189-205,253`）
2. **FS metric**：对相邻接收符号作共轭差分，乘接收端预存的 conjugate-differential PRBS，再累加/能量归一化；峰位即 frame start。变量说明包括 `M(d), C(d), P(d), R_n, d, N, m, ts, ts'`。（`content.md:209-249`）
3. **一级 FOE**：FFT 后找半轴最大谱峰，与 FO=0 的参考峰相减；在 sampling rate=`Rs` 的推导下最大范围 `3Rs/8`，双边为 `[-3Rs/8,3Rs/8]`。（`content.md:253-272,312`）
4. **二级 FOE**：x/y 偏振之间用相隔 `TL` 的 block 交叉共轭，正文称可将 Gaussian phase-noise influence 按 `TL` 缩减；总估计写成 `Δf_est=Δf_a+Δf_b`，再做 compensation。（`content.md:283-306`）
5. **关键假设**：双偏振承载相同信息、polarization demultiplexing 理想且无 crosstalk；邻近符号间 laser-linewidth phase deviation 近似不变；仿真忽略 polarization demultiplexing phase shift（tap set 仅中间系数为 1）。（`content.md:229,241,283`）
6. **复杂度**：以 real multiplier count 为口径；FS 复杂度只核算 `C(d)`，论文声称相对 Park 节省约 100 symbols/39%；二级 FOE 声称 `4N`。（`content.md:321-325`）
7. **公式/表证据限制**：抓取文件在正文和 Equations 区只剩 Eq. (1)–(21) 编号，数学本体均为空；Table 1/2 也只有 caption。因此不能核验 timing metric、normalized MSE、`4N` 的完整代数式，也不能恢复各 baseline 的 multiplier 表项。（`content.md:211-247,264-310,373,808-866`）

8. **开源代码**：未报告公开代码仓库；data availability 明示底层数据当前不公开、可向作者请求。故代码状态为 **未报告/未开源证据**。（`content.md:503-505,613-615`）

## 5. 七子表

### A. 状态 / 输入空间

| 项 | 提取结果 | 证据 |
|---|---|---|
| 算法状态 | 确定性、training-aided、receiver-side DSP；顺序为 FS→coarse FOE→MRC 后 fine FOE→compensation | `content.md:205-219,251-312,345` |
| 接收输入 | 各 diversity branch 的双偏振 complex samples；已知 PRBS prefix 与 cyclic-QPSK suffix；x/y polarization blocks | `content.md:205-231,251-292` |
| 条件变量 | received power、CFO、laser linewidth/phase noise、turbulence-induced scintillation/phase noise、branch 数、modulation、training length、block length `TL` | `content.md:227-229,272-292,334-345,351-464` |
| 非输入 | 无 learned state、无 replay/batch、无 lag-ranking state | 全文方法结构 `content.md:185-325` |

### B. 动作 / 输出空间（此处不是 action space）

| 输出 | 形式 | 证据 |
|---|---|---|
| Frame synchronization | timing metric 主峰位置/各支路 frame start | `content.md:209-249` |
| Coarse CFO | FFT 最大谱峰相对零偏峰的频率差 | `content.md:251-272,312` |
| Fine CFO | 双偏振跨 `TL` block 的 residual estimate `Δf_b` | `content.md:283-306` |
| Final output | `Δf_est=Δf_a+Δf_b` 与 CFO-compensated samples | `content.md:294-310` |
| Action space | **N/A**：非控制/强化学习方法 | 全文方法结构 `content.md:185-325` |

### C. 奖励 / 目标函数与真实评价量

| 项 | 结果 | 证据 |
|---|---|---|
| Reward | **N/A**：非学习型确定性估计器 | `content.md:185-325` |
| Training objective/loss | **N/A** | `content.md:185-325` |
| 真实评价量 | FS accuracy；timing main/side-peak separation；normalized CFO MSE（Eq. 21，本体缺失）；BER；FEC threshold `1.5e-3` 下 receiver sensitivity；CFO range；training symbols；real-multiplier complexity | `content.md:321-325,351-375,393-464,497` |
| 可辨认关系 | `Δf_est=Δf_a+Δf_b`；range=`[-3Rs/8,3Rs/8]`；fine stage complexity=`4N`；Eq. 21 的精确定义无法由当前转换恢复 | `content.md:272,306,325,371-375` |

### D. 建模假设、位置与迁移影响

| 假设 | 原文位置 | 对 target 迁移的影响 |
|---|---|---|
| x/y polarization 传输相同 training 信息 | `content.md:283` | target 若双偏振内容/时延不一致，交叉共轭 fine FOE 的成立性需另证；本文不提供该证据 |
| polarization demultiplexing 完美、无 crosstalk | `content.md:283` | 会高估复杂星地偏振动态下的可用性；不能把论文性能直接外推 |
| 邻近符号 phase deviation 近似不变 | `content.md:241,283` | 高动态 Doppler/phase evolution 下是否保持未知 |
| turbulence phase noise 可借差分/累加抑制 | `content.md:241-249` | 依赖 phase evolution 与 training 间隔；target conditioned-lag 结论仍 UNKNOWN |
| coupling efficiency~non-central chi-square，phase noise~normal | `content.md:345` | 是特定 source-domain stochastic model；未覆盖星地全链路条件化分布 |
| phase screens、branch fading 独立（spacing > coherence length） | `content.md:345` | 支持空间 diversity 仿真，不证明 target 单 lag/跨 lag 排序 |
| 忽略 polarization-demux phase shift | `content.md:229` | target 若该项显著，本文基线可能需要重新实现/校准 |

### E. 网络架构 / DSP 链 / 参数 / 复杂度

| 项 | 结果 | 证据 |
|---|---|---|
| Neural network | **N/A**：非神经网络 | `content.md:185-325` |
| DSP 链 | PRBS differential FS → cyclic-QPSK FFT coarse CFO → branch phase precorrection/MRC → dual-polarization cross-block fine CFO → compensation | `content.md:205-312,336-345` |
| 核心参数 | period=16；training total=480/960（推荐 480）；FS example=320；`TL` 扫描；10 Gbaud QPSK case；80 K linewidth；1/4 branches | `content.md:189-205,336,351-360,393-442` |
| Complexity | 口径为 real multipliers；fine FOE=`4N`；Ref. 21 原配置 1024 symbols；proposed 480；FS 相对 Park 声称约 39% resource saving | `content.md:321-325` |
| 复杂度证据等级 | PARTIAL：只有正文结论，Table 1 内容丢失，未给实测 latency/FPGA utilization | `content.md:323-329,808-814` |

### F. 适配性

| 层级 | 判定 | 边界 |
|---|---|---|
| Source-domain comparator | **适配** | coherent FSO、turbulence、dual polarization、spatial diversity、frame/CFO recovery；C2/C4 task-matched |
| Target defect evidence | **不适配** | 不含星地 lag-ranking crossover 或 conditioned-single-lag failure |
| Writing/experiment material | **适配** | 可借鉴参数表、长度扫描、MSE→BER/sensitivity 链、复杂度/范围并列；仅作为未来原料 |
| Method-design authority | **不适配** | 本 Step 3 reader 不设计 RML-FSTS、不判 novelty/Go |

### G. 本文自身 M/C/A 与 canonical 四判据

| 项 | 本文自身定位 | 证据/理由 |
|---|---|---|
| M（既有方法） | Park/weighted-Park frame timing；traditional TS、fourth-power FFT、Wu et al. 2022 QPSK-TS FOE | `content.md:177-181,323-325,360,413-442` |
| C（条件） | coherent polarization-multiplexed QAM FSO；低 received power、强/弱 turbulence、单/四支路；有限 training overhead | `content.md:167,175,334-345,351-464` |
| A（失效/不足） | timing side/redundant peaks、低功率未经验证；fourth-power complexity/range 限制；已有 QPSK-TS 长度未评估且二级 FFT 复杂 | `content.md:177-181` |
| A 定位 | 具体为同步峰可辨认性、FO MSE/range 与 training/real-multiplier overhead，不是泛化“性能差” | `content.md:177-181,321-325,351-440` |
| 方法产出形态 | 可复用的 mixed training sequence + differential timing metric + two-stage deterministic FOE chain | `content.md:181,185-325` |
| ① 具体 M-C-A | ✅ | M、C、A 均可从引言和实验映射，且 A 有 side peaks/MSE/range/complexity 等具体量 |
| ② 可复用方法产出 | ✅ | 训练结构、处理顺序、变量和参数扫描均明确；虽公式本体缺失，但论文产出本身是算法链 |
| ③ 近期 baseline | ✅ | 直接对比 2022 年 Ref. 21，并发表于 2024；另含传统 baseline。`content.md:179-181,585-587` |
| ④ 可量化对标 | ✅ | FS accuracy/symbols、MSE、BER/sensitivity、CFO range、complexity；有 800/3200 次统计。`content.md:321-325,351-464` |

**限定解释**：上述四项只说明“本文自身问题—方法—实验链”满足 canonical 读法；不增加 `problem_truth` 或 `novelty` 判据，也不推导 target Q、target novelty 或 Go。

## 6. 通信参数表

| 参数类 | 本文设置/报告 | 来源 |
|---|---|---|
| 链路/场景 | 仿真：20 km coherent FSO，B2B、单支路与四支路 diversity；实测：室内 atmospheric path、QPSK 单孔径，另有理想 B2B 描述 | `content.md:334-345,371,442-470,493` |
| 调制 | polarization-multiplexed QAM；具体 QPSK 与 16QAM | `content.md:336,413-464` |
| 符号率 | QPSK range 实验明确 10 Gbaud/s；平台写“10 G”但未在该句明确定义单位 | `content.md:336,422` |
| 采样率 | 一级推导令 sampling rate=`Rs`；实验 coherent receiver sampling rate=40 G（单位未进一步定义） | `content.md:272,470` |
| Training/frame | PRBS prefix + cyclic-QPSK suffix；QPSK period=16；FS 示例 320 symbols；FOE 总长度 480/960，推荐 480；Ref. 21 原文比较提到 1024；FS 前置 65,000 random points | `content.md:189-205,323-325,351-360,393-442` |
| CFO | Fig. 4 示例 1 GHz；proposed range `[-3Rs/8,3Rs/8]`，TS `[-Rs/2,Rs/2]`，fourth-power `[-Rs/8,Rs/8]` | `content.md:272,281,422` |
| 相位噪声/线宽 | 仿真 laser linewidth=80 K；正文称典型 linewidth 100 K–10 M；phase noise normal；另含 atmospheric phase noise | `content.md:227-241,283,336,345` |
| 接收功率/SNR | 未报告 OSNR/SNR；使用 received optical power 扫描，包括 −52.991/−43.991 dBm（FS）、−53/−36 dBm（谱图）、−45.12/−43.12 dBm（MSE）；实验 transmit power=13 dBm | `content.md:276,281,351-360,375-404,422,470` |
| BER/FEC | FEC threshold=`1.5e-3`；理想 indoor/B2B 句报告 BER=`1.219e-8` | `content.md:375,431,493,497` |
| 湍流 | phase-screen model；仿真 structure constants：weak=`1e-16`、strong=`1e-14`；实验称 weak=`6e-11`，但单位/模型映射未报告 | `content.md:345,442,470` |
| 空间分集 | 1/4 branches；多 telescope spacing > turbulence spatial coherence length；lens aperture=0.2 m；MRC 前 phase precorrection | `content.md:345,442-464` |
| AO | 未报告 adaptive optics | `content.md:334-345,466-493`（设置段无 AO） |
| 信道模型 | coupling efficiency~non-central chi-square；phase noise~normal；multiple random phase screens；shot+thermal Gaussian noise | `content.md:227-229,345` |
| 关键算法参数 | QPSK cycle=16；block interval=`TL`；二级估计相对一级的门限随总长度/功率变化；fine complexity=`4N` | `content.md:189,292-306,325,404` |
| 参数来源 | phase-screen/分布引 Refs. 26–27；MRC precorrection 引 Ref. 28；QPSK spectrum/FOE 引 Refs. 21–22；部分关键数值（20 km、80 K、Cn²、功率）未逐项给文献来源 | `content.md:189,253,283,345,603-609` |

## 7. 实验完备性（≤20 行）

1. Main claims：FS 旁峰抑制/省 training、two-stage FOE 精度/范围/复杂度、QPSK/16QAM 与 turbulence/diversity 适用性；scope 为 coherent FSO simulation + 有限室内 QPSK experiment。（`content.md:167,351-497`）
2. Seeds：未报告随机种子。（全文设置/结果 `content.md:334-493`）
3. 次数：FS 每点 3200；FOE/BER 多图每点 800。（`content.md:351,393-404,431`）
4. Error bar：Fig. 12 有 error bars；一处 standard deviation=`2.91466e-9`。（`content.md:404`）
5. 统计检验：未报告置信区间、显著性检验或 hypothesis test。
6. Baseline 数量/类型：FS 2 个（Park、weighted Park）；FOE 3 类（TS、fourth-power/FFT、Ref. 21）。（`content.md:360,413-442`）
7. Baseline 来源：均有论文引用，但未报告公开实现或复现一致性测试。（`content.md:177-181,539-587`）
8. 公平调参：部分图同 training length；系统图中 proposed/Ref.21/TS=480、FFT=960，未给统一调参 protocol。（`content.md:404,431-442`）
9. 消融：无逐组件 ablation（PRBS、差分 metric、双偏振 fine stage 的 on/off 对照未报告）。
10. 参数扫描：有 training length、`TL`、received power、CFO、modulation、branch/turbulence 扫描。（`content.md:351-464`）
11. 信道模型/参数来源：phase screen、non-central chi-square/normal distribution 引 Refs.26–27；Cn² 数值本身未逐项溯源。（`content.md:345,442,603-605`）
12. 场景多样性：B2B、弱/强 turbulence、1/4 branches、QPSK/16QAM；实测仅室内 QPSK 单孔径。（`content.md:371-493`）
13. 理论复杂度：real-multiplier 口径、`4N` 与符号节省；表内容缺失，故仅 PARTIAL。（`content.md:321-329`）
14. 实测复杂度：未报告 runtime、latency、memory、FPGA LUT/DSP/throughput。
15. **Verification：2/3**；多维仿真、800/3200 次重复与室内实验共同核对算法行为，但 canonical 转换缺失公式/表体且无公开代码。
16. **Validation：2/3**；覆盖 B2B、弱/强湍流、1/4 branches、QPSK/16QAM，但实测仅室内 QPSK 单孔径，外部场景覆盖有限。
17. **Uncertainty：2/3**；报告 800/3200 次重复及一处 error bar，但未给 seed、置信区间或统计检验。

## 8. 写作架构标杆提取

### 8.1 三级标题与核心章节比例

- **一级**：论文题名。（`content.md:14`）
- **二级**：Abstract；1 Introduction；2 Operation principle；3 Simulation settings；4 Simulation results；5 Summary；另有 Disclosures/Data availability/References。（`content.md:165,171,185,334,347,495,499-507`）
- **三级**：2.1 Training sequence design；2.2 Principle of frame synchronization；2.3 Principle of frequency offset estimation；2.4 Complexity analysis and comparison；4.1 Frame synchronization performance analysis；4.2 FO compensation performance；4.3 experimental results。（`content.md:187,207,251,321,349,369,466`）
- **按主体区间词数估算**（Abstract–Summary，共约 10,049 tokens-like words；Markdown 链接会略抬高）：Abstract 1.6%，Introduction 12.0%，Operation principle 32.5%，Simulation settings 5.0%，Simulation results 47.6%，Summary 1.4%。区间依据为 `content.md:165-498`。

### 8.2 System Model / Problem / Algorithm 组织

- 无独立 `System Model` 或 `Problem Formulation` 标题。问题链集中在 Introduction：FS side peaks/低功率稳健性→FOE range/complexity/training length 缺口→本文 response。（`content.md:175-183`）
- 算法主体统一放在 `Operation principle`：先 training construction，再 FS，再 FOE，再 complexity；这是“共同 training object→两个 receiver tasks→成本”的递进。（`content.md:185-333`）
- 系统链路、随机信道与 MRC 假设后置到 `Simulation settings`，而不是先于算法给完整 system model。（`content.md:334-345`）

### 8.3 参数/符号展示

- 公式后立即解释局部符号，如 `M(d), C(d), P(d), R_n, d, N, m`，接着再解释双偏振接收模型的 responsivity、scintillation、phase noise、coupling、laser/LO amplitude、CFO 和 Gaussian noise。（`content.md:217-231`）
- 参数不是集中表，而是随 Fig./Eq. 分散引入；`Rs` 在训练谱说明处定义，`TL` 在 block 图后定义，`N` 在 fine estimator 后解释。（`content.md:189,292-306`）
- 优点：符号贴近首次使用；缺点：缺总参数表、单位和分布参数溯源不完整，转换后更难复核。

### 8.4 图表类型、数量与 caption 模式

- 共 **20 figures、2 tables、21 equations、28 references**。（`content.md:156-160,623,808,822`）
- 图类型：训练/星座/谱与 block schematic（Fig.1–6）；系统平台（Fig.7）；FS curve（Fig.8）；MSE/BER/sensitivity/range/branch 对比曲线（Fig.9–17）；实验照片/constellation-eye（Fig.18–20）。（`content.md:690-804`）
- Caption 模式以名词短语或 “relationship between X and Y under Z” 为主；多 panel 在 caption 直接列 `(a)…(d)…` 与 modulation/training/turbulence 条件。（`content.md:732,756-786`）
- 表：Table 1 负责 complexity，Table 2 负责 timing metric definitions；转换缺表体。（`content.md:812-820`）

### 8.5 Baseline、消融、指标、复杂度实验组织

- baseline 不是单独一节：FS baselines 在 Intro 综述后于 4.1 同图比较；FO baselines 在 Intro 分类，再于 2.4 complexity 和 4.2 多维 performance plots 重复出现。（`content.md:177-181,321-325,349-464`）
- 无严格 ablation；以 training length 和 `TL` 扫描承担“设计参数合理性”证据。（`content.md:393-440`）
- 指标链从 normalized MSE→BER threshold/sensitivity→modulation/turbulence/diversity；复杂度在算法节末先给，结果节再用 480 vs 960 与 sensitivity 说明资源折中。（`content.md:321-325,369-464`）
- 理论 complexity 与 performance 分开，但缺真实 hardware/runtime 复杂度。

### 8.6 Introduction 与结论叙述链

- Introduction：coherent FSO 价值→turbulence/FO/phase noise/diversity 时齐问题→FS 文献的 plateau/redundant/side peaks→blind/training FOE 的 complexity/range/length 问题→本文 differential FS + length scan + two-stage FOE→文章结构。（`content.md:171-183`）
- Summary：重述 mixed training 与 differential metric→100-symbol FS saving→FEC 阈值下 480-symbol FOE/complexity→turbulence 与 multi-format scope。（`content.md:495-497`）
- 结论没有 limitations/future work，也没有重列所有数值；主要把“方法—关键资源结果—适用范围”压成一段。

### 8.7 公式引入、推导与编号

- Eq. (1)–(3)：normalized timing metric；(4)–(5)：双偏振接收信号；(6)–(10)：差分 PRBS FS 推导；(11)–(13)：coarse FOE；(14)–(20)：fine FOE/compensation；(21)：normalized MSE。（`content.md:209-249,262-312,371-375`）
- 组织方式为“先给物理/处理直觉→连续编号公式→逐符号解释→图示 flow→复杂度”；编号跨全文连续。（`content.md:209-325`）
- **证据限制**：当前 Markdown 的所有公式只有编号，不能核验精确求和区间、归一化分母、angle/phase 操作或 Eq.21 定义。（`content.md:822-866`）

### 8.8 共同引用但本 GW 覆盖状态未知的基础文献候选（只列，不检索）

由于本 reader 禁止读取旧 read-note，下面只给“应由主线对照本 GW 覆盖表”的候选，覆盖状态均为 **UNKNOWN**：

1. Schmidl & Cox, “Robust frequency and timing synchronization for OFDM,” 1997（Ref.9；`content.md:539-541`）。
2. Minn/Zeng/Bhargava, “On timing offset estimation for OFDM systems,” 2000（Ref.10；`content.md:543-545`）。
3. Park et al., “A novel timing estimation method for OFDM systems,” 2003（Ref.11；`content.md:547-549`）。
4. Ren et al., “Synchronization methods based on a new constant envelope preamble,” 2005（Ref.13；`content.md:553-555`）。
5. Cheng et al., training-aided joint frame/frequency synchronization for low-OSNR FSO, 2020（Ref.19；`content.md:577-579`）。
6. Wu et al., QPSK-TS joint OSNR/FO monitoring, 2022（Ref.21；`content.md:585-587`）。
7. Wang et al., carrier FOE based on FSTS in spatial-diversity PM coherent FSO, 2023（Ref.24；`content.md:595-597`）。
8. Schmidt, *Numerical Simulation of Optical Wave Propagation*, 2010；Andrews, *Laser Beam Scintillation with Applications*, 2001（Refs.26–27；`content.md:603-605`）。
9. Wang et al., optimal-branch block phase correction for spatial-diversity coherent FSO, 2022（Ref.28；`content.md:607-609`）。

## 9. FACT / INFERENCE / UNKNOWN 边界总表

| 标签 | 声明 | 边界/证据 |
|---|---|---|
| FACT | 本文在 20 km coherent PM-QAM FSO simulation 中评估 mixed PRBS/cyclic-QPSK FS+FOE，并补充室内 QPSK 单孔径实验 | `content.md:334-345,466-493` |
| FACT | 本文是 deterministic DSP，不含 learning/action/reward | `content.md:185-325` |
| FACT | 本文给出 C2/C4 所需的 task-matched metrics：FS accuracy、MSE、BER/sensitivity、range、training overhead、complexity | `content.md:321-497` |
| INFERENCE | 可把本文作为 RML-FSTS 的近期 comparator 和写作架构标杆 | 基于任务与指标匹配；不是论文原文声称 |
| INFERENCE | source-domain 结论可能提示 turbulence/power/modulation 会改变同步/FOE表现 | 仅限本文扫描趋势，不能推导具体 target lag 机制 |
| UNKNOWN | 星地 lag-ranking crossover 是否存在 | 本文无 lag-ranking experiment/model |
| UNKNOWN | conditioned-single-lag failure 是否存在 | 本文无 conditioned single-lag estimator/comparison |
| UNKNOWN | 论文算法在真实星地 Doppler、偏振动态、AO/pointing 条件下的性能 | 本文未覆盖这些 target 条件 |
| UNKNOWN | 精确公式、两表完整数值、代码可复现性 | canonical Markdown 丢失 formula/table body；无公开代码/数据 |

## 10. Reader 结论

L02 的可靠角色是 **C2/C4 近期 task-matched deterministic-DSP comparator + 写作架构标杆**：它提供了明确的联合训练结构、FS→两级 FOE→MRC/补偿链、参数扫描和从 MSE 到 BER/sensitivity/complexity 的实验叙事。它**不能**升级为 target defect 证据；星地 lag-ranking crossover 与 conditioned-single-lag failure 均继续保持 `INFERENCE/UNKNOWN`，且本文自身四判据通过不等于 target novelty 或 Go。
