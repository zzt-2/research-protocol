# Handoff: 块 A 选样完成 + Step 2 下载完成 + 精读批次 1 完成（3/7 篇，grep 核查过）

> 来源: 本轮执行（2026-06-26，续接 H003）| 交接目标: 继续精读批次 2/3 + 综合分析 + Q# 清单
> 文件名: H004-blockA-sampling-and-batch1-deep-read.md

## 已完成边界（本轮做了什么）

**本轮完成 4 件事，全部在 D005 务实路线 + 块 A/B 范围内，没跳步没偏**：

1. **Session Start + H003 接收验证**：报到 + Trigger 5 验证 H003 接收方清单 5/5 PASS（导师3篇在 papers/teacher/、GW Step 3 全 ⬜、D005 导师接受增量、无 conflicts、scope 内）

2. **块 A 选样完成**：从 683 条 landscape 按务实标准筛 7 篇代表性论文（覆盖均衡/载波同步/调制/信道估计/AO 五技术路线），用户已放行。选样标准 = ①有传统 baseline 可比 ②能迁移星地激光 ③工程可做 ④覆盖不同技术路线 ⑤motivation 结构清晰（D004-b）

3. **Step 2 下载完成（7/7 篇全文到位）**：
   - OA 2 篇：`papers/doi/10.1364_oe.553709/`（Optics Express 两阶段 KF）、`papers/doi/10.3390_electronics14020265/`（Electronics CPR，**北理工同实验室 Hu/Lin**）
   - IEEE 5 篇：`papers/downloads/2026-06-26/{11443146,11206561,10850117,11185295,9286272}.md`（ICSOS OQAM / UralCon SSB / WiSEE Data-Aided / JLT AO+MDR / GC-ElecEng Time-Packing）
   - title 自检全过（gw-read.md 步骤 0）

4. **精读批次 1 完成（3/7 篇，主线 grep 核查 abstract+conclusion 立场全 PASS，无 S011 型造假）**：
   - 笔记落盘：`papers/_read_notes/{10.1364_oe.553709, 10.3390_electronics14020265, 10.23919_GC-ElecEng48342.2020.9286272}.md`
   - 溯源：`projects/thesis-fso/read-log.md` 已建
   - 三篇四判据全过（子 agent 判定 + 主线 grep 核查一致），改进量级符合同门 2-4dB（无 oracle 上界砍的）

## 不要做什么（防跳步防偏，本轮纪律延续）

**1. 不要跳到四判据终审 / Go-No-Go / 选方向**（块 C/E 的事，不是块 B）
- 批次 1 只精读了 3/7 篇，**综合分析 + Q# 清单还没做**。不要拿 3 篇的发现就定方向
- 必须等 7 篇全精读完 → 综合分析 → Q# 清单过四判据 → 进 Step 4a

**2. 不要标题联想试 MVE**（TL-30/31 仍有效）
- 看到"两阶段 KF 好"→ 不要联想"那我做个三阶段 KF？""那我做 RL 调 Q？" 这种起点 = 跳步
- Q# 必须从 7 篇精读的 M-C-A 汇总浮出，不从单篇联想

**3. 不要塞方向给用户**（PROMPT-004 §8.4 + D005 务实）
- 选样/精读只给数据，不给"我推荐做 X 方向"
- Go/No-Go 等综合分析 + Q# 清单完成后，让用户拍板

**4. 不要跳过 grep 核查信任子 agent 报告**（S011 造假教训）
- 每篇子 agent 精读报告，主线必须 grep 核查 abstract + conclusion 整体立场
- 批次 1 三篇全过核查，批次 2/3 必须同样核查

**5. 不要在本轮做综合分析/Q# 清单**（单对话步骤上限 + 块 B 未完）
- 7 篇精读完才有资格做综合分析（gw-read.md 综合分析节要求基于全部精读）

## 必读（按优先级，新对话开始时按此顺序读）

1. **本文件 H004**（交接当前状态）
2. **H003**（务实路线 + 块 A-H 工作量拆解，本文件是其续接）
3. **`topic-index.md` 不变量段**（D005 务实路线是第 1 条 INVARIANT；判据 A 已降级为"baseline 不够好+改进空间"）
4. **`decisions.md` D005 + D004**（务实标准执行规则 + D004 三条打磨点）
5. **`thesis-lessons.md` TL-30/31/32/33**（跳步/凭记忆/标准不对称/自欺式跳步）
6. **`stages/gw-read.md`**（精读完整流程 14 字段 + 7 子表 + 综合分析 + Q# 清单）
7. **批次 1 的 3 份精读笔记**（papers/_read_notes/ 下三篇，了解已读论文的 M-C-A）

## 已精读 3 篇的关键发现（批次 1，grep 核查过）

| # | 论文 | 子地带 | 传统 baseline（自实现） | 失效点 | 切入点 | 改进增益 | 诚实 nuance |
|---|---|---|---|---|---|---|---|
| 1 | 两阶段 KF（Optics Express 2025）| 均衡/多普勒补偿 | VV-BPS、OPLL | VV-BPS 四次方运算对相位噪声敏感，5/10GHz 大频偏失效；OPLL 调谐速度不够 | 两组 Q 级联 KF：stage1 大 Q 快捕突发，stage2 ω 锁定精调相位 | 10GHz@18dB OSNR BER<FEC 3.8e-3（VV-BPS 失效） | 0.1GHz 小频偏时 TS-KF 略输 VV-BPS |
| 2 | Noise-Tolerant CPR（Electronics 2025，**北理工同实验室**）| 载波同步 | Diff-4th（Leven/Huang/Tang）| 全前馈块平滑，低 SNR phase cycle slip → burst errors，BER→0.5 | 二阶 DPLL 反馈级（消 cycle slip）+ 前馈级（跟踪 Wiener PN） | BER 6.7e-3 vs 0.25（@4.5dB）；乘法 36%、加法 0.8% | 收敛慢（37µs）、仅 QPSK、Doppler 简化场景 |
| 3 | Time-Packing 均衡（GC-ElecEng 2020）| 均衡/调制/检测 | Viterbi（Ns=4096 限）、truncated MMSE、baseline δ=0 无重叠 | 受限 Viterbi trellis 不足 → error floor；truncated MMSE 信道截断 → error floor | adaptive MMSE (LMS) 自适应 L_w=7 抽头 | 8-PAM 下唯一无 error floor；throughput 所有 cloud attenuation 优于 baseline | 2-PAM 比 Viterbi 约 1dB gap（代价） |

**跨论文观察（仅供下轮综合分析参考，未过四判据终审、未判 Go）**：
- 三篇都过四判据（子 agent 判 + 主线 grep 核查）
- 方法产出形态都是 DSP 算法（非 ML/RL），跟同门 4 篇范式一致（场景约束→单一环节失效→多维协同 DSP）
- 死轴"有缝但人少"得到全文层验证：载波同步（#2 Diff-4th 真失效）、均衡（#3 受限 Viterbi 真出 error floor）
- 改进量级符合同门 2-4dB（#1 OSNR 几 dB、#2 BER 两数量级+资源 64%、#3 throughput 频谱效率），都不是 oracle 上界砍的
- 论文都诚实自承局限（不夸大），baseline 改进是真实形态

## 接口变更（如有代码改动）

无代码改动（本轮全是精读 + 笔记落盘 + 文档交接）。

## 已知债务（如原则与现实有差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| literature_notes.md 是旧方向（Ch2/3/4 信道估计/均衡/载波同步，2026-05-29 Step 1）| gw-read.md 要求精读入 literature_notes.md | 批次 1 三篇**只落 papers/_read_notes/ + read-log.md，未入 literature_notes.md**（旧文件过时需重写，不在本轮范围）| 综合分析阶段（块 C）重写 literature_notes.md 时统一写入 |
| #2 北理工同实验室利益相关 | 客观精读 | 笔记已标"利益相关提醒"，子 agent 客观精读 + 主线 grep 核查通过 | 综合分析/Q# 决策时再次留意客观性 |
| #1 OA 下载隐患（_enrich_arxiv_id 误匹配 arXiv 1608.06244v2 同名旧文）| title 自检防错配 | OA agent 已用真实 MDPI PDF 覆盖修正，title 自检通过（content.md 是真实 Electronics 2025） | 综合分析时留意，已无实际影响 |

## 验证阈值（如涉及验证体系）

本轮不涉及验证体系。后续 Go/Kill 标准（务实路线下）：
- **Go**：方法 > 传统未优化 baseline（参考同门 2-4dB 量级，具体阈值块 E 定）
- **Kill**：连传统 baseline 都赢不了 / 方法增益 <0.5dB 且无次指标维度 / MVE FAIL
- **不放水**：不接受孤证/伪命题/标题联想（底线）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落（D005 务实路线是第 1 条 INVARIANT）
- [ ] 已验证本文件中的至少 3 条关键事实声称：
  - [ ] 7 篇论文全文已下载（核查：`ls papers/doi/10.1364_oe.553709/ papers/doi/10.3390_electronics14020265/ papers/downloads/2026-06-26/*.md`）
  - [ ] 批次 1 三篇精读笔记已落盘（核查：`ls papers/_read_notes/10.1364_oe.553709.md papers/_read_notes/10.3390_electronics14020265.md papers/_read_notes/10.23919_GC-ElecEng48342.2020.9286272.md`）
  - [ ] read-log.md 已建（核查：`cat projects/thesis-fso/read-log.md`）
- [ ] 已检查 _registry.yaml 中本专题 status = active（无 conflicts_with）
- [ ] 已确认当前范围未违反"明确不含"（仍要导师同意 S007 边界 / 仍不接受孤证凑数 / 方法必须指标提升 / 不跳四判据不跳 Go）

## 下一轮（精读批次 2/3 + 综合分析）

**先做完块 B（精读余下 4 篇）再进块 C（综合分析）**，严格不跳步：

### 精读批次 2（调制方向 2 篇）
- **#4 Coherent OQAM Single Balanced Photodetector**（papers/downloads/2026-06-26/11443146.md，ICSOS 2025）—— baseline=conventional homodyne QAM
- **#5 Single-Sideband Optical Modulation Coherent Detection**（papers/downloads/2026-06-26/11206561.md，UralCon 2025）—— baseline=conventional double-sideband ASK

派 2 个子 agent 并行，套用 D004-b motivation 字段 + gw-read.md 14 字段 + 7 子表。**子 agent 报告回传后主线必须 grep 核查 abstract+conclusion 立场**（S011 纪律）。

### 精读批次 3（信道估计/AO 2 篇）
- **#6 Data-Aided Multi-Format DSP**（papers/downloads/2026-06-26/10850117.md，WiSEE 2024）—— 强湍流，多格式 DSP
- **#7 AO + Mode Diversity Reception**（papers/downloads/2026-06-26/11185295.md，JLT 2025）—— AO 是 S007 明确算"处理技术"

同上流程。

### 块 C 综合分析（7 篇全精读完后）
- 按 gw-read.md 综合分析节撰写：方法分类 / 已知局限 / 2-3年趋势 / 研究背景概述 / **研究问题清单 Q#**（把 7 篇 M-C-A 汇总，逐条过四判据）
- 重写 literature_notes.md（旧文件过时）
- Q# 清单非空且至少 1 条四判据全过 → 进 Step 4a

**关键提醒**：
- **不跳步**：批次 2/3 没做完不进综合分析，综合分析没做完不进 Step 4a
- **不偏方向**：精读只提取 M-C-A，不联想"那我做 X"，不塞方向给用户
- **grep 核查**：每篇子 agent 报告都核查
- **导师边界**：S007 已定 feeder/ISL/网络层/ATP/QKD/深空不算处理，精读时如遇这些子地带的论文不要当主线候选（这 7 篇都已通过 S007 边界筛选，但综合分析时留意）

**不要在块 B 做**：不过四判据（块 C 的事）/ 不判 Go（块 E 的事）/ 不写 literature_notes 综合分析（块 C 的事）。块 B 只负责"7 篇精读 + 笔记落盘 + grep 核查"。

---

# 【更新段 2026-06-26】块 B 精读全部完成（7/7 篇）+ 选样返工决定

> 本段是后续对话的增量更新，**上文原文不改**（保留块 A/批次 1 完成时的状态作历史）。读 H004 时先读上文了解块 A 怎么走的，再读本段了解后续发生了什么。

## 一、块 B 精读收尾（7/7 篇全精读 + grep 核查全过）

### 新增精读 4 篇（批次 2/3，已落盘 papers/_read_notes/ + read-log.md 追加 4 条）

| # | 论文 | 子地带 | 方法产出形态 | 传统 baseline（对手） | 失效/不足点 | 改进增益（带诚实 nuance） |
|---|---|---|---|---|---|---|
| 4 | OQAM 单平衡 PD（ICSOS 2025，papers/_read_notes/10.1109_ICSOS62128.2025.11443146.md）| 调制/检测 | **光学接收架构（非 DSP/ML）** | conventional homodyne QAM（带 optical hybrid）| optical hybrid 高阶调制引入 ~3dB SNR 惩罚 | 理论 1.25dB / 仿真 1.7dB / 实验 2dB@BER=1e-3；⚠️需 1.5×带宽；⚠️实验仅 B2B+self-coherent |
| 5 | SSB-QPSK 相干（UralCon 2025，papers/_read_notes/uralcon-2025-11206561-ssb.md，**无 DOI**）| 调制 | **物理层系统设计+标准 DSP 链（非 ML）** | DSB-ASK（⚠️terrestrial 链路 950m/850m）| DSB+色散 RF 功率衰落 | ~7dB@BER=1e-9（⚠️**断言非实测**）；⚠️**baseline 是 terrestrial 与 satellite 不对称，增益不可直接引用**；C_n² 论文自身记号不一致 |
| 6 | Data-Aided 多格式 DSP（WiSEE 2024，papers/_read_notes/10.1109_WiSEE61769.2024.10850117.md）| 信道估计/DSP | **经典离线 DSP 均衡器（非 ML/RL）** | CMA 盲均衡、BPS 盲 CPE | 盲均衡慢收敛+低 SNR 不稳+调制格式相关；BPS 低 SNR cycle slip | SNR≥0dB 可靠（仿真），实测 outage 阈值 16QAM −1.2dB/4QAM −1.8dB；⚠️**无与竞争性单格式 DSP 直接 BER 对标**；⚠️实测 3.2km 城市地面非星地；⚠️多孔径合并（论文最终目标）未实测 |
| 7 | AO+MDR 交互（JLT 2025，BUPT，papers/_read_notes/10.1109_JLT.2025.3616344.md）| AO（S007 算处理 ✅）| **仿真+桌面实验机制分析（非新算法）** | SMF 单模 / MDR-only / AO-only 四方案消融 | 独立 AO 强湍流失效（D/r0=26 仅 0.4dB）；AO-MDR 交互机制不明 | AO+MDR 总增益峰值 D/r0=7 为 17.2/18.9/20.1dB（3/5/6 模）；**核心发现：弱湍流互削弱、强湍流互增强**；⚠️桌面实验缩比非真实 GEO 在轨 |

### grep 核查结果
4/4 篇 abstract+conclusion 立场逐条核实通过（S011 纪律），无造假无扭曲。

### DOI 争议发现（FR-26 证据链强制的实例）
- #7 文件名 `11185295.pdf` ≠ 真实 DOI `10.1109/JLT.2025.3616344`（正文 L17 明示真实 DOI）
- read-log 已用真实 DOI 作 paper_id，并标注"IEEE doc 11185295 ≠ DOI 3616344"
- **教训印证**：S012"核查机制必须应用到所有层级"的又一次验证——只信文件名/搜索元数据会把 paper_id 标错

## 二、❗ 选样返工决定（用户反馈 + 主线自省）

**用户原话**："我希望做的是和同门类似的那种东西。以及，最好多挑点？" + "感觉你挑的不好呢?"

**用户需求明确**：
1. **方法产出形态 = 同门那种 = DSP 算法类**（S014 实验室套路：场景三约束→现有方法单一环节失效→多维协同 DSP+硬件落地，纯 DSP 无 ML）
2. **不是**光学架构 / 系统设计 / 机制分析
3. **要多挑点**（扩大候选池）

### 7 篇选样质量重判

| # | 论文 | 方法产出形态 | 重判 |
|---|---|---|---|
| 1 | 两阶段 KF | 递归 DSP 估计器 | ✅ **保留**（强候选）|
| 2 | CPR（北理工同实验室）| 二阶 DPLL 反馈+前馈 DSP | ✅ **保留**（强候选，但利益相关留意）|
| 3 | Time-Packing MMSE | adaptive MMSE (LMS) | ✅ **保留**（强候选）|
| 6 | Data-Aided DSP | 经典离线 DSP 均衡器 | 🟡 **边缘保留**（baseline 是概念论证非直接 BER 对标；实测非星地）|
| 4 | OQAM 单平衡 PD | **光学接收架构（非 DSP）** | ❌ **剔出候选**（方法产出形态不符）|
| 5 | SSB-QPSK | **物理层系统设计+标准 DSP 链（非 ML），且 baseline 不对称** | ❌ **剔出候选**（baseline terrestrial vs satellite 不对称，7dB 不可引用）|
| 7 | AO+MDR | **机制分析，非新算法** | ❌ **剔出候选**（无方法产出形态）|

**真实有效 Q# 候选池 = #1 + #2 + #3（+ #6 边缘）= 3-4 篇**，不是 7 篇。

### 根因诊断（为什么挑错，不找借口）

1. **覆盖驱动 > 质量驱动**（核心错误）：块 A 筛选时把"覆盖不同技术路线（每子地带一支）"当硬约束，为填"调制""AO" slot 硬塞 #4/#5/#7。应质量优先——某子地带没好论文就不凑数。**这是 D005"务实 ≠ 不挑"的反面教材**：自己执行时把"务实"滑坡成"凑够 7 篇"
2. **只验"baseline 显式"，没验"baseline 对称性"**：#5 我标"baseline 显式可量化对标"但没核查 baseline 链路类型跟 proposed 同不同类。landscape 表 baseline 字段只到 abstract 层（S010 已诊断"abstract 工具天然报不出真信号"），选样时没用上这个教训
3. **没预先区分"DSP 算法 vs 光学架构/机制分析"**：S007 把 AO/调制/检测都算"处理技术"我照单全收，但同门 4 篇范式全是 DSP 算法，应先问用户这个边界
4. **凑"≥5 篇"门槛心态**：gw-read.md"≥5 篇"是下限不是目标，3 篇真强候选 + 诚实承认另子地带没找到，比 7 篇掺 3 篇水货强。违反 D005 底线"不接受凑数"

### 教训待沉淀（建议 TL-34，待用户拍板）

D005 把判据 A 从"真缝"降到"baseline 不够好+改进空间"，**但四判据本身没废**。选样时把"务实"滑坡成"降低所有筛选标准"（含判据 2 方法产出形态 + 判据 4 可量化对标），是 TL-31（教训复现）的新表现：教训写"增量改进非填补空白"，执行时反用成"务实路线就别挑"。**主线是否起草 TL-34 待用户定**。

## 三、下一步：补检索 + 补精读（方案 A+B 组合，主线推荐）

**承认两个事实**：
1. 从 landscape 主表 abstract 层挑补充候选，**还是会犯同样的错**（abstract 报不出真信号，S010 已证）—— #5 就是 abstract 看着有 baseline 实际不对称
2. 真正能判"是不是同门 DSP 范式 + baseline 严不严"的，**只有下载精读全文才能确认**

**所以正确路径不是"主线先挑再给用户审"，而是"扩一批候选 → 下载 → 精读 → grep 核查 → 用户看精读报告决定"**。

### 推荐方案 A+B 组合（用户已拍板"按你推荐"）

**方案 A：定向补检索**
现在 landscape 是设备词/问题词/综述词地勘产物，**没专门针对"同门范式"（DSP 算法 + 传统 baseline 对标 + 星地/星间场景）做定向检索**。用 `tools/search` 跑一轮定向词，如：
- `satellite optical coherent equalization conventional baseline`
- `inter-satellite DSP carrier synchronization Kalman filtering`
- `LEO coherent optical Doppler compensation digital signal processing`
- `satellite optical channel estimation pilot aided adaptive`
- `coherent FSO feedforward feedback carrier recovery`

召回新 DSP 类论文后下载精读。**注意偏航检查 A**：定向检索词不能锁死单一模块（仍要覆盖多 DSP 环节：估计/均衡/同步/检测）。

**方案 B：从现有 landscape 主表挑 abstract 看着像 DSP 的下下来精读**
grep 已发现几个高潜力候选（abstract 未精读，真实质量待精读确认）：
- **#465 Hardware-efficient adaptive equalizer for inter-satellite coherent**（2024，ISL/信道估计均衡/相干，实测）—— 子地带最对路
- **#100 Homodyne coherent inter-satellite communications with IM/DD comparable DSP**（2025，调制/相干/载波同步/信道估计均衡/ISL，实测）—— 标题含 "comparable DSP" 强信号
- **#271 Frame format and DSP receiver design for a 56-GBaud GEO DP-QPSK coherent optical feeder link**（2023，相干/载波同步/信道估计均衡/feeder）—— 但 landscape 标 🔴"abstract自陈成熟/广泛采用"，可能偏工程实现非改进
- **#580 Digitally Mitigating Doppler Shift in High-Capacity Coherent FSO LEO-to-Earth**（2023，链路预算/ISL/信道建模/相干，实测）—— "Digitally Mitigating" 是 DSP 强信号
- **#590 On the Mitigation of Doppler Shift for High-Capacity Coherent FSO Satellite**（2022，链路预算/相干）—— 同 #580 方向

**⚠️ 风险声明**：abstract 层信号不可靠，下完精读可能发现又是不对称/非 DSP/纯仿真无 baseline。但比纯定向检索快（已有候选不用等检索）。

### 执行建议（给下个对话）

1. **先跑方案 A 定向检索**（5-6 个 tools/search 词，召回 30-50 条）→ 主线扫标题筛 DSP 类候选
2. **并行跑方案 B**：直接下 #465/#100/#580/#590（#271 因 🔴 标记先不下）的全文精读
3. 方案 A 新召回 + 方案 B 已下论文，合并后**派子 agent 精读**（每批 2-3 篇，套 D004-b motivation 字段 + gw-read.md 14 字段 + 7 子表）
4. **子 agent 报告回传后主线必须 grep 核查 abstract+conclusion 立场**（S011 纪律，本轮已验证有效）
5. 精读报告给用户审 → 用户决定哪些进 Q# 候选池

**质量门槛**（补精读的验收标准，比块 A 严）：
- ✅ 方法产出形态必须是 **DSP 算法类**（估计/均衡/同步/检测的递归/自适应/反馈前馈结构），不是光学架构/系统设计/纯机制分析
- ✅ baseline 必须**对称**（proposed 和 baseline 是同一链路类型/场景，不能 terrestrial vs satellite）
- ✅ 有**可量化对标**（BER/SNR/MSE/收敛速度的数字对比，不是概念论证）
- ✅ 场景在**星地/星间激光通信**（不接受 terrestrial FSO / 纯光纤）
- 不达标的诚实剔除，不凑数

## 四、当前状态总结

- 块 A 选样：完成（7 篇，但 3 篇挑错待返工）
- Step 2 下载：完成（7 篇全文 + 可能的补检索新论文）
- 块 B 精读：完成（7/7 篇笔记落盘 + grep 核查）
- **Q# 候选池当前有效 = 3 篇（#1/#2/#3）+ 1 边缘（#6）**，需补检索扩到 ≥5 篇真强候选才进块 C 综合分析
- **下一步 = 方案 A+B 组合补检索 + 补精读**（不在本轮做，新对话执行）

## 五、新对话开工清单

1. 读本 H004（含本更新段）+ H003 + topic-index 不变量 + D004/D005 + TL-30/31/32/33 + gw-read.md + 批次 1-3 共 7 篇精读笔记（papers/_read_notes/ 下，read-log.md 有索引）
2. 执行方案 A 定向检索 + 方案 B 下载 #465/#100/#580/#590 全文
3. 派子 agent 精读新论文（每批 2-3 篇）→ grep 核查 → 报告给用户审
4. 用户审过后，合并 #1/#2/#3/#6 + 新通过的，组成 ≥5 篇真强候选池 → 进块 C 综合分析

**防跳步防偏提醒（延续 H004 原文 + 本轮新教训）**：
- 不跳四判据终审/Go-No-Go/选方向（块 C/E 的事）
- 不标题联想试 MVE
- 不塞方向给用户
- 不跳过 grep 核查信任子 agent 报告
- **不在本轮做综合分析/Q# 清单**（补精读没完不能做）
- **新增**：选样质量优先于覆盖，某子地带没好论文就不凑数（TL-34 候选教训）
- **新增**：方法产出形态必须先验是不是 DSP 算法类（同门范式），不验 baseline 显式就放过
- **新增**：baseline 对称性必须核查（proposed 和 baseline 同链路类型），不只看 abstract 写没写 baseline 名
