# L01 全文精读：Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication

> Groundwork Step 3 单篇 reader 报告 | 2026-08-09
> 边界：本文只作为 C1/C2/C4 的确定性通信 DSP source baseline；不设计 RML-FSTS，不判断 target novelty/Go，不进入 Step 3.5/4a。

## 0. Preflight

- 派遣标题与正文标题逐字一致：`Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication`（`content.md:5,11`）。
- 派遣 DOI 与正文 DOI 一致：`10.1109/JPHOT.2023.3265847`（`content.md:83`）；metadata 的 `id`、`doi` 亦一致（`metadata.json:id/doi`）。
- canonical 路径存在，正文共 455 行、55,349 bytes；metadata 标记 `download_status=success`、`content_type=html`、`content_quality=good`、`real_title` 与派遣标题一致（`metadata.json` 对应字段）。
- 结论：**PASS，非 ABORT**。核心全文可读；但这是 IEEE Xplore HTML 抓取，不是排版 PDF。Table I/II 的单元格是图片，参考文献列表明确不可用，若干一级章节标题未被转换；这些限制不得用推断补齐（`content.md:221-229,391-415`）。metadata 的 `title_check=unverifiable` 也保留为来源质量限制。

## 1. DOI / 来源

- DOI：**10.1109/JPHOT.2023.3265847**（`content.md:83`；`metadata.json:doi`）。
- 来源：IEEE Xplore 上的 IEEE 期刊文章页面，Publisher 为 IEEE（`content.md:5,11-17,75-85`）。

## 2. Canonical 源路径

`D:\code\study\research-protocol\papers\doi\10.1109_jphot.2023.3265847\content.md`

对应 metadata：`D:\code\study\research-protocol\papers\doi\10.1109_jphot.2023.3265847\metadata.json`。

## 3. 发表状态

**已正式发表的 Open Access 期刊文章**；页面注明 Creative Commons License，发布日期为 2023-04-10（`content.md:37-50,75-83,93`）。本文不是 arXiv 预印本；但该结论仅基于 IEEE 页面元数据，未另行检索。

## 4. 发表渠道

**IEEE Photonics Journal**, Volume 15, Issue 3, Article Sequence Number 7302313（`content.md:75-79`）。

## 5. 年份 / 期刊

- 年份：**2023**（页面发布日期 2023-04-10；卷期为 June 2023，`content.md:75-79`）。
- 期刊：**IEEE Photonics Journal**（`content.md:75`）。

## 6. 核心贡献

1. 论文设计了一个跨 X/Y 偏振的 frame-synchronous training sequence（FSTS）：两偏振训练序列采用错位的成对相同符号与前后共轭对称结构，使同一训练开销同时承担 frame synchronization（FS）和 carrier frequency-offset estimation（FOE）。FS 既定位训练序列起点，又对齐空间分集分支；MRC 与偏振解复用后，再复用训练序列做 FOE（`content.md:101,103-119,142`；Fig. 1–2）。
2. FOE 被拆成粗、细两级。粗估计利用 X/Y 偏振相邻匹配符号的共轭乘积消除调制相位，并通过求和抑制高斯噪声，单采样/符号时理论范围为 `[-Rs/2,+Rs/2]`；细估计把间隔 `B_L` 的同符号做跨偏振共轭乘积，并将相位差除以 `B_L`，把残余高斯相位噪声影响缩小 `B_L` 倍，但细估范围也缩小 `B_L` 倍（`content.md:175-208`；Eq. 7–10）。
3. 论文给出 FS/FOE 复杂度分析并在 10 GBaud PM 4/16-QAM B2B 与空间分集相干 FSO 仿真中验证：320-symbol FSTS 的 BER 可接近或优于 960-symbol conventional TS；在给定双分支 MRC 条件下报告 0.8–3.41 dB 范围内的接收灵敏度增益，并声称特定比较下最优复杂度降低约 75%（`content.md:217-229,329-385`）。该 75% 不应与 Table I 中“缓存粗估时相对最坏情形约减少 25% 实乘”的另一比较口径混同（`content.md:219,339,385`）。

## 7. 方法概述（2–3 句）

发送端在 X/Y 两偏振插入结构化 FSTS；接收端先用 Park 型 timing metric 加阈值完成分支对齐与训练起点检测，再共享 LO、进行分支相位校正和 MRC、偏振解复用。随后以跨偏振相邻匹配符号做宽范围粗 FOE，以间隔 `B_L` 的匹配块做窄范围高精度细 FOE，两级估计相加得到 `Δf_est` 并补偿整个训练周期（`content.md:101,117-142,175-215,231-243`）。这是**确定性前馈通信 DSP 估计器**，无训练、无策略学习、无神经网络。

## 8. 实验设置

- 平台：10 GBaud PM 4-QAM / PM 16-QAM；先做 optical B2B FOE 仿真，再做 10 km 空间分集相干 FSO 仿真（`content.md:231-243,277-279,339`）。
- 激光器：发送 ECL 线宽 50 kHz；各接收分支共享 LO，LO 线宽 50 kHz、功率 15 dBm（`content.md:231,243`）。
- 湍流：Fourier-transform phase-screen；`C_n^2=10^-16 m^-2/3`（弱）和 `10^-14 m^-2/3`（强）；外尺度趋于无穷、内尺度趋于零；传播 10 km（`content.md:241`）。
- 接收：望远镜口径 0.2 m；平均耦合效率弱/强湍流分别 67.3012% / 4.8395%；光电响应度 0.8 A/W；考虑散粒噪声和热噪声（`content.md:243`）。
- CFO：多数 FOE/BER 比较从 `(-1.1,+1.1) GHz` 随机取值；1 sample/symbol；FS 阈值最终设置为 0.2（`content.md:183,289,319,339`）。
- FSTS：重点比较 320 与 960 symbols；320-symbol 结构为 4-QAM `B_N=16,B_L=20`，16-QAM `B_N=8,B_L=40`；960-symbol 结构为 4-QAM `B_N=24,B_L=40`，16-QAM `B_N=16,B_L=60`（`content.md:299`）。
- 重复次数：FS accuracy 每点 6400 次平均；Fig. 11/12 的每个频偏测试点或同接收功率随机频偏情形取 800 次平均（`content.md:257,319`）。随机种子、独立 channel realization 数量与置信区间未报告。

## 9. Baseline（逐项标注）

| Baseline | 本文如何使用 | 自实现 / 引用状态 | 证据 |
|---|---|---|---|
| 4th-power FOE | 4-QAM 比较；16-QAM 使用 QPSK partition 变体 | 原方法引用 [10]；仿真结果由本文平台产生，具体复现代码/参数未公开 | `content.md:97,279,289,329` |
| QPSK-partition 4th-power FOE | 16-QAM blind baseline | 引用 [15]；本文仿真实现细节不足 | `content.md:97,289` |
| 4th-FFT FOE | B2B 与 FSO 的精度、BER、复杂度比较 | 引用 [11]；复杂度公式另引 [27],[28]；本文仿真实现细节不足 | `content.md:97,217-219,289-339` |
| Conventional TS-based FOE | 主要 source baseline；同训练长度和 320-vs-960 训练开销比较 | 引用 [18]；结果由本文仿真平台产生，未提供代码/完整调参 | `content.md:99,219,289-385` |
| TS-based joint FS+FOE | 仅整体 FS+FOE 硬件复杂度比较 | 引用 [19]；Table II 为图片，单元格不可从文本恢复 | `content.md:99,225-229` |
| Proposed FSTS two-stage FOE | 本文方法 | 作者自提出/自仿真；无开源代码证据 | `content.md:101,175-215,385` |

说明：文中说“we compare / simulation”支持这些曲线由本文仿真生成，但不能证明作者发布了可复用实现；故不把 baseline 标为“官方实现”。

## 10. 关键结论

- 48-symbol TS 的 timing-metric 峰不够尖锐，低接收功率时甚至无法找到；320 symbols 显著改善。320→800 symbols 的接收灵敏度边际增益仅 0.48 dB（4-QAM）/0.23 dB（16-QAM），故作者选 320 symbols 作为最短建议长度（`content.md:247-267`；Fig. 5–7）。
- FOE 的 BER 开始恶化 normalized-MSE 阈值约为 `2.5e-7`（4-QAM）和 `6.25e-8`（16-QAM）；严重恶化阈值约为 `6.25e-6`（4-QAM）和 `2.25e-6`（16-QAM）（`content.md:279`；Fig. 8）。
- 当训练长度 ≥160 symbols 时，FSTS 在不同接收功率下具有更好的估计精度；相对 conventional TS，normalized MSE 从约 `10^-6~10^-7` 降至 `10^-7~10^-9`，作者概括为超过一个数量级（`content.md:289`；Fig. 9）。
- 在 B2B、320 symbols、FEC BER=`3.8e-3` 时，相对 conventional TS 的接收灵敏度增益为 0.98 dB（PM 4-QAM）与 1.72 dB（PM 16-QAM）；960 symbols 时为 0.25 / 0.39 dB（`content.md:329`；Fig. 13）。
- FSO 四分支 MRC、320 symbols 时，弱/强湍流下的灵敏度增益分别为：4-QAM 1.14/0.70 dB，16-QAM 2.45/2.14 dB；分支数 1/2/4/6 的完整扫描显示增益随分支数并非单调（`content.md:357-375`；Fig. 16–18）。
- 论文结论中特别突出双分支、320 symbols：弱湍流增益 1.43/2.54 dB（4/16-QAM），强湍流 2.09/3.41 dB（`content.md:375,385`）。这些数字属于本文设定下的 simulation fact，不是星地链路通用保证。

## 11. 与 RML-FSTS 的关系

- **FACT（source-domain）**：本文给出了 C1/C2/C4 所需的 source baseline：结构化 FSTS 的输入/输出、粗细两阶段 FOE、训练长度与块长选择、FS 阈值、估计范围/精度/复杂度/BER 的对标方法，以及 B2B/弱湍流/强湍流/空间分支数扫描（`content.md:101-229,231-385`）。
- **INFERENCE（仅未来设计原料）**：`B_L` 同时控制细估计噪声抑制与无模糊估计范围，论文自身呈现了“块间距—估计精度—范围”的条件依赖（`content.md:208,299`）；该事实可以成为以后分析 lag-conditioned behavior 的原料。
- **UNKNOWN（target-FSO）**：本文没有研究星地时变 Doppler/相位过程下的 lag ranking crossover，也没有验证 conditioned-single-lag failure；不能把 source-domain 的 `B_L` 扫描或不同频偏/功率曲线直接改写成这两个 target claim。本文也没有 RML、lag selector、conditioned policy 或学习模型。

## 12. 实现关键细节

1. **FSTS 结构**：每偏振分前/后两部分，互为共轭对称；每部分含 `B_N/2` blocks，每 block 含 `B_L` 个 PRBS-derived symbols。X/Y 偏振的奇偶 block 与 block 内奇偶 symbol 交错复制，以便跨偏振配对（`content.md:103-107`；Fig. 1）。转换文本把索引串写为 `i=13,5…`，应理解为 OCR/HTML 数学丢分隔符，不能据此重建精确索引序列。
2. **FS metric**：
   `M_m(d)=|C_m(d)|^2/[P_m(d)]^2`（Eq. 1），其中 `C_m(d)=Σ_{i=0}^{N/2-1}R_m(d+i)R_m(d-i)`（Eq. 2），`P_m(d)=Σ_{i=0}^{N/2-1}|R_m(d+i)|^2`；传统做 `argmax_d M_m(d)`，本文用阈值首次判定以少滑窗（`content.md:119-142`）。建议阈值 0.2 或 0.3；正式 FSO 比较用 0.2（`content.md:257,339`）。
3. **信号模型**：Eq. (3)–(4) 将 `R_X/R_Y` 表为 `γ√(η I P_LO) S_{X/Y}(k) exp[j(φ+θ_k+θ_{x/y}+2πfkT_s)] + N_{x/y}(k)`；湍流强度/耦合/相位项相对 GHz symbol rate 慢变（`content.md:152-160`）。Eq. (5)–(6) 进一步只保留相位组成（`content.md:162-173`）。
4. **粗 FOE**：Eq. (7) 对 `R_X*(2i-1)R_Y(2i)+R_Y*(2i-1)R_X(2i)` 跨 `B_L B_N/2` 对求和取相角，得到 `2πΔf_1T_s`；理论范围 `[-R_s/2,+R_s/2]`（`content.md:175-183`）。
5. **细 FOE**：先补偿 `Δf_1`，再通过 Eq. (8)–(10) 对间隔一个 block 的跨偏振同符号共轭乘积求和，结果相角除以 `B_L` 得 `2πΔf_2T_s`；最终 `Δf_est=Δf_1+Δf_2`（Eq. 11；`content.md:185-215`）。细级噪声影响约缩小 `B_L` 倍，但范围也缩小 `B_L` 倍（`content.md:208`）。
6. **建议 FSTS 参数**：320-symbol 时 4-QAM `(B_N,B_L)=(16,20)`、16-QAM `(8,40)`；960-symbol 时 4-QAM `(24,40)`、16-QAM `(16,60)`（`content.md:299`）。另 Fig. 9 的横向算法比较统一注明 proposed `B_L=20`（`content.md:289`），不可擅自假设这涵盖所有 16-QAM 图点。
7. **DSP 顺序**：I/Q imbalance recovery → FS → diversity-branch phase correction → MRC → polarization demultiplexing → FOE → phase-noise estimation → DD-LMS → QAM demapping → BER（`content.md:243`）。
8. **复杂度**：4th-FFT 每偏振、长度 N 为 `2Nlog2N+10N+2` real multiplications 与 `3Nlog2N+5N` real additions（`content.md:217-219`）。Table I/II 的 proposed/conventional 精确算式位于图片，canonical 文本无法读取；只能保留作者文字结论：缓存粗估时 proposed 相对自身最坏情形实乘约减 25%，相对 [19] joint algorithm 整体复杂度更低（`content.md:219-229`）。

## 13. 适配性摘要

- 适配 1：作为**确定性、训练序列辅助、双阶段 FOE** 的 source baseline，方法接口、公式、估计范围和复杂度口径清楚（`content.md:175-229`）。
- 适配 2：实验同时覆盖 B2B、弱/强湍流、1/2/4/6 分支、4/16-QAM、320/960 symbols，可支持 C1/C2/C4 的 source-side 实验组织参照（`content.md:277-381`）。
- 不适配 1：没有星地轨道/Doppler 动力学、非平稳 lag condition、时变 ranking 或 conditioned-single-lag failure，不能充当 target-FSO 事实来源。
- 不适配 2：只做仿真，湍流相位屏采用理想外/内尺度极限，未报告 AO、pointing error、实测链路或置信区间；不能支撑系统级外推（`content.md:241-243,319`）。
- 未来设计原料启示（不构成设计）：把 `B_L` 的“噪声平均增益 vs. fine-range 缩窄”作为需显式保留的 source constraint，而不是把较大 lag 单调解释为更优（`content.md:208,299`）。

## 14. 开源代码

**未报告 / UNKNOWN。** canonical 文本没有 repository、code availability 或 supplementary-code 链接；只能确认页面提供 PDF 链接与图表资源（`content.md:17,54-61,387-415`），不能据此断言绝无私有实现。

## 15. 学术身份 / 全文验证

- 学术身份：IEEE Photonics Journal 2023 年正式 journal article，3 位作者；页面标 Open Access 与 CC license（`content.md:19,37-50,75-83,93`）。
- 全文验证：核心 narrative 从引言、方法、仿真平台、结果到结论连贯，公式 (1)–(11)、Fig. 1–18 captions、Table I–II 标题均在；因此足以做方法/实验 source extraction（`content.md:95-385`）。
- 限制：HTML 转换没有保存 Section II–V 的一级标题文字，Table I/II 单元格不可读，References 明确 unavailable（`content.md:221-229,391-415`）。所以基础文献只能保留编号与正文赋予的角色，不能补作者/题名/年份；复杂度表不能伪造数值。

## 16. FACT / INFERENCE / UNKNOWN 清单

| 类型 | 内容 | 边界与证据 |
|---|---|---|
| FACT | 本文提出 FSTS-based 两阶段 FOE，并与 FS、spatial-diversity MRC 组合 | source-domain PM coherent FSO simulation；`content.md:101-229` |
| FACT | 粗估范围在 1 sample/symbol 时理论为 `[-Rs/2,+Rs/2]`；细估噪声影响与范围均约按 `B_L` 缩放 | 论文解析/算法陈述；`content.md:183,208` |
| FACT | 320-symbol proposed 在本文设置下可接近/优于 960-symbol conventional TS | 仅本文仿真；`content.md:339,357,385` |
| FACT | 弱/强湍流 `C_n^2`、10 km、0.2 m aperture、耦合效率等参数如通信参数表所列 | source simulation；`content.md:241-243` |
| INFERENCE | `B_L` 是可解释的 condition-sensitive estimator scale，可作为以后 lag 机制分析原料 | 由范围/精度 tradeoff 推得；论文未使用 RML/lag-ranking 术语；`content.md:208,299` |
| INFERENCE | 由于 branch-number 增益非单调，系统级收益受场景/组合条件影响 | 来自 Fig. 18 数字比较的保守归纳；`content.md:375` |
| UNKNOWN | 星地 lag-ranking crossover 是否存在、何时发生 | 本文没有星地时变实验或该变量 |
| UNKNOWN | conditioned-single-lag failure 是否成立 | 本文没有 conditioned lag selector 或单-lag 失败定义 |
| UNKNOWN | 结果对真实星地外尺度/内尺度、AO、pointing、轨道 Doppler 的可迁移性 | 这些 target factors 未验证；`content.md:241-243` |
| UNKNOWN | 代码可获得性、随机种子、置信区间、Table I/II 完整数值 | canonical 文本未报告/未转换；`content.md:221-229,319,387-415` |

---

## 表 A：状态 / 输入空间

> 本文无学习型 state；下表的“状态”指确定性估计器在每个 processing block 接收的真实观测与缓存。

| 模块 | 真实信号输入 | 维度 / 范围 | 预处理 | 证据 |
|---|---|---|---|---|
| FS | 第 m 接收分支的复采样序列 `R_m(d+i),R_m(d-i)` 与长度 N 的 FSTS | 每偏振 TS 长度 N；实验扫描 48、128+、320、800/960 symbols；分支 1/2/4/6 | ADC 后、I/Q imbalance recovery；对训练窗口计算 correlation/energy | Eq. (1)–(2), `content.md:119-142,243,247-267,375` |
| Coarse FOE | MRC + polarization demultiplexing 后的 `R_X(k),R_Y(k)`，已定位 FSTS | `B_L·B_N/2` 个跨偏振 symbol pairs；1 sample/symbol；CFO 测试 `(-1.1,1.1) GHz` | FS、分支相位校正、MRC、偏振解复用 | Eq. (3)–(7), `content.md:152-183,243,289` |
| Fine FOE | 粗估补偿后的 X/Y FSTS；间隔 `B_L` 的同符号 block pairs | `j=1..B_N/2, i=1..B_L`；fine unambiguous range 相对粗估缩小 `B_L` 倍 | 先补偿 `Δf_1`；粗估可从 buffer 周期更新 | Eq. (8)–(10), `content.md:185-208` |
| Channel / nuisance | 湍流强度/耦合/相位、laser phase noise、Gaussian receiver noise | `C_n^2=10^-16/10^-14 m^-2/3`; linewidth 50 kHz; power-dependent | 不作为可学习 state，只进入接收采样 | Eq. (3)–(6), `content.md:152-173,241-243` |

## 表 B：动作 / 输出空间

> 本文不是 RL；以下均为估计器输出，**不是 action space**。

| 模块 | 真实输出 | 约束 / 粒度 | 下游用途 | 证据 |
|---|---|---|---|---|
| FS | `d_start` / threshold crossing 对应的训练序列起点；分支相对对齐 | 每个 frame/训练周期、每分支；阈值建议 0.2/0.3 | 分支合并、精确截取 FSTS | `content.md:119-142,257` |
| Coarse FOE | `Δf_1` | 单个共享 LO 导致两偏振/各分支共用；范围约 `[-Rs/2,+Rs/2]` | 先补偿 FSTS；可缓存并周期更新 | Eq. (7), `content.md:175-208` |
| Fine FOE | `Δf_2` | 每训练周期；高精度、范围缩小 `B_L` 倍 | 修正粗估残差 | Eq. (8)–(10), `content.md:185-208` |
| Final FOE | `Δf_est=Δf_1+Δf_2` | 单一 deterministic scalar frequency estimate | 补偿训练周期/后续 phase-noise estimation | Eq. (11), `content.md:208-215,243` |

## 表 C：奖励 / 目标函数与真实评价量

| 项目 | 定义 | 证据 |
|---|---|---|
| Reward | **N/A：非学习型确定性估计器，无 reward、policy 或训练 objective。** | 方法全链为解析 DSP；`content.md:117-229` |
| FS timing metric | `M_m(d)=|C_m(d)|^2/[P_m(d)]^2`，`C_m(d)=Σ_{i=0}^{N/2-1}R_m(d+i)R_m(d-i)`，`P_m(d)=Σ_{i=0}^{N/2-1}|R_m(d+i)|^2` | Eq. (1)–(2), `content.md:119-142` |
| Normalized FOE MSE | `E[|Δf_est·T_s - Δf·T_s|^2]` | `content.md:279` |
| BER | QAM de-mapping 后错误 bit 数/总 bit 数；正文未显式给比值公式；阈值采用 `2e-2`（Fig. 7）与 FEC `3.8e-3`（Fig. 13–18） | `content.md:243,267,329-375` |
| Receiver sensitivity gain | 在固定 BER/FEC 阈值下达到该 BER 所需 average received optical power 的横向差值（dB）；正文通过曲线读数报告，未给单独公式 | `content.md:267,329-385` |
| Complexity | real multiplications / real additions；4th-FFT 完整式为 `2Nlog2N+10N+2` 与 `3Nlog2N+5N` | `content.md:217-229` |

## 表 D：建模假设、位置与迁移影响

| 假设 | 位置 | 对 target-FSO 迁移的影响 |
|---|---|---|
| X/Y 两偏振 CFO 理论相同，空间分支共享同一 LO | TS Design / Fig. 2；`content.md:101,105,152-160,243` | 若 target receiver 不共享 LO、各分支残余 CFO 不同，则单次 joint FOE 接口不能直接沿用。 |
| 激光线宽与湍流相位相对 GHz symbol rate 慢变，相邻匹配符号承受近似相同相位 | FS/FOE derivation；`content.md:160,173,183` | 星地高动态条件必须重新验证“相邻/跨 `B_L` symbol 相位近似相同”，本文不提供 target 结论。 |
| Polarization demultiplexer 初始 taps：中间 1、其余 0，使附加 overall phase shift 可忽略 | signal model；`content.md:160` | 不同 equalizer 初始化/收敛瞬态可能破坏推导中的相位消除，需单独验证。 |
| Phase-screen 外尺度→∞、内尺度→0，传播 10 km | Simulation platform；`content.md:241` | 不是一般星地湍流谱；对真实外/内尺度、分层大气的可迁移性 UNKNOWN。 |
| 多望远镜接收 independent fading signals | Simulation platform；`content.md:243` | 星地 aperture spacing 与相关湍流会改变 diversity gain；本文未给相关性扫描。 |
| 后续 phase-noise estimator 可在 normalized MSE 低于阈值时完全补偿残差 | FOE results；`content.md:279,357` | 该阈值依赖本文后级 DSP 与调制，不能无条件迁移。 |
| CFO drift 在实践中慢，可缓存粗估并周期更新 | algorithm discussion；`content.md:208` | target Doppler dynamics 若更快，缓存带来的复杂度结论可能失效。 |

## 表 E：网络架构 / DSP 模块链、参数与复杂度

| 项目 | 内容 | 证据 |
|---|---|---|
| 网络架构 | **N/A：无神经网络、无层数、参数量、训练过程。** | `content.md:95-385` |
| Tx chain | ECL → PBS → PRBS-derived PM 4/16-QAM data + FSTS → DAC → dual-pol IQ modulator → PBC → FSO channel | `content.md:231`；Fig. 4 |
| Rx optical/electrical | multiple telescopes → SMF coupling → shared-LO coherent receivers/BPD → ADC | `content.md:243`；Fig. 4 |
| Offline DSP | I/Q recovery → FS → branch phase correction → MRC → pol-demux → two-stage FOE → phase-noise estimation → DD-LMS → demap → BER | `content.md:243` |
| 核心参数 | 10 GBaud；50 kHz Tx/LO linewidth；LO 15 dBm；responsivity 0.8 A/W；TS 320/960；`B_L` 20/40/60；FS threshold 0.2 | `content.md:231-243,289-299,339` |
| 复杂度结论 | worst-case two-stage FOE 与 conventional TS 接近；粗估命中 buffer 时，相对 proposed worst-case 实乘约少 25%；对 320-vs-960 设定，正文另声称 optimal complexity 约少 75% | `content.md:219,339,385`；Table I–II 单元格缺失 |

## 表 F：适配性

| 类别 | 判断 | 理由 / 证据 |
|---|---|---|
| 适配 1 | ✅ source deterministic FOE baseline | 明确 FSTS、粗/细 FOE、FS 与复杂度接口；`content.md:101-229` |
| 适配 2 | ✅ source experiment/writing baseline | 多调制、训练长度、频偏、功率、湍流、分支数分层扫描；`content.md:245-381` |
| 不适配 1 | ❌ target lag-ranking claim | 无星地 lag condition、ranking crossover 变量或实验 |
| 不适配 2 | ❌ learning/conditioned estimator claim | 无 DRL、监督学习、RML、policy/action/reward |
| 未来原料 | 限定使用 | 只保留 `B_L` 的精度—范围 tradeoff 与 source test matrix，不外推 target truth；`content.md:208,299` |

## 表 G：本文自身问题 M/C/A 与 canonical 四判据

### G1. 本文自身 M/C/A

| 要素 | 定位 | 证据 |
|---|---|---|
| M（现有方法） | 4th-power / QPSK partition、4th-FFT、conventional TS FOE、TS-based joint FS+FOE | `content.md:97-99` |
| C（条件） | 训练符号短、需多格式、PM coherent FSO + spatial diversity、要求 FS/FOE 联合且硬件复杂度低 | `content.md:95-101` |
| A（失效原因） | 4th-power 对高阶 QAM 兼容性差且范围缩小；4th-FFT 短序列分辨率差且复杂；conventional TS 的精度依赖长度、长 TS 增 overhead，短 TS 中噪声不能充分平均；联合方案 [19] 短训练 FOE 不佳 | `content.md:97-99,173,208` |
| A 定位 | **确定性估计器统计效率 + 训练结构/硬件复杂度矛盾**，不是学习能力或数据不足 | `content.md:97-101,175-229` |
| 方法产出形态 | 跨偏振 FSTS 结构 + threshold FS + coarse/fine FOE 公式 + 参数/复杂度建议 | `content.md:103-229,299` |

### G2. Canonical 四判据（仅四项）

| 判据 | ✅/❌ | 理由 |
|---|---|---|
| 具体 M-C-A 矛盾 | ✅ | 清楚指出既有 blind/TS methods 在短 training、多格式、低复杂度 spatial-diversity PM coherent FSO 条件下的具体失效机制；`content.md:95-101`。 |
| 可复用方法产出形态 | ✅ | 给出 TS 结构、FS metric、两阶段估计 Eq. (7)–(11)、参数 `B_N/B_L` 与 DSP placement；`content.md:103-229,299`。 |
| 近期 baseline | ❌ | 有多个 cited baseline，但 canonical HTML 的 References unavailable，无法验证 [10]/[11]/[15]/[18]/[19] 的年份与当时是否“近期”；`content.md:391-415`。不以 2023 的本文发表年替代 baseline recency 证据。 |
| 可量化对标 | ✅ | normalized MSE、BER/receiver sensitivity、real multiplication/addition、FS accuracy，并有 800/6400 次平均；`content.md:217-229,257,279-385`。 |

**边界声明：**上表只评估“本文自身问题”的表达与验证形态；即使三项通过，也不等于 target Q 成立、不等于 RML-FSTS novelty、更不等于 Go。

---

## 通信参数表

| 类别 | 本文设置 | 来源 |
|---|---|---|
| 链路 / 场景 | optical B2B；10 km computer-simulated free-space turbulence；single branch 与 1/2/4/6-branch spatial diversity MRC | `content.md:241,277-279,339-381` |
| 调制 | polarization-multiplexed 4-QAM 与 16-QAM | `content.md:71,231` |
| 符号率 / 采样率 | 10 GBaud；FOE 推导/范围采用 1 sample per symbol，`T_s=1/R_s`；DAC/ADC 数值采样率未报告 | `content.md:183,231,243` |
| training / frame | FSTS 扫描 48、128+、320、800/960 symbols；主比较 320/960；完整 frame 长度、data/training ratio、PRBS order 未报告 | `content.md:107,247-267,289-305` |
| CFO / 相位噪声 | CFO 多数实验随机取 `(-1.1,+1.1) GHz`；Tx ECL 和共享 LO linewidth 均 50 kHz；具体 laser phase-noise stochastic model 未报告 | `content.md:231,243,289,319,339` |
| 接收功率 / SNR | 扫 average received optical power；明确示例为 4-QAM -43 dBm、16-QAM -37 dBm；完整扫值/步长与 SNR 映射未在文本报告 | `content.md:309,319`；Fig. 11–12 |
| 湍流 | Fourier phase screen；`C_n^2=10^-16`（弱）/`10^-14 m^-2/3`（强）；outer scale→∞、inner scale→0 | `content.md:241`；引用来源 [30],[31] |
| 空间分集 | independent fading optical signals；1/2/4/6 branches；MRC；各 branch 共用 LO | `content.md:101,243,357-381` |
| AO | **未报告 / 未使用证据** | `content.md:231-243` 的平台链无 AO |
| 信道模型 | phase-screen turbulence + optical intensity scintillation / phase fluctuation / coupling-efficiency fluctuation；coherent receiver Gaussian/shot/thermal noise | Eq. (3)–(6), `content.md:152-173,241-243` |
| 光学参数 | receive aperture 0.2 m；avg coupling 67.3012%（弱）/4.8395%（强）；LO 15 dBm；photodiode responsivity 0.8 A/W | `content.md:243` |
| FSTS 参数 | 320: 4-QAM `(16,20)`, 16-QAM `(8,40)`；960: 4-QAM `(24,40)`, 16-QAM `(16,60)`；FS threshold 0.2/0.3 建议，FSO 用 0.2 | `content.md:257,299,339` |
| 参数来源 | turbulence phase screen [30]、`C_n^2` [31]、branch phase correction [23]；其余多为本文仿真设定，未给逐参数文献溯源 | `content.md:241-243`；References unavailable at `content.md:415` |

## 实验完备性（≤20 行）

1. Main claims：FS+FOE 复用、高精度/宽范围/低复杂度、多格式、turbulence+diversity 下 BER/sensitivity 增益（`content.md:71,385`）。
2. Scope：证据只覆盖 10 GBaud PM 4/16-QAM、所列两种 `C_n^2`、10 km phase-screen simulation；不是 universal 星地结论。
3. Repeats：FS accuracy 每点 6400 次；频偏相关 MSE 每点 800 次（`content.md:257,319`）。
4. Seeds：未报告；运行次数之外的独立随机源/realization 定义未报告。
5. Error bar / CI / statistical test：均未报告，图文只给平均值。
6. Baseline 数量：4 个算法族（4th-power/QPSK partition、4th-FFT、conventional TS、[19] joint complexity），类型覆盖 blind 与 TS-aided（`content.md:97-99,217-229,289`）。
7. Baseline 来源：均有编号引用，但 References unavailable；代码来源与年份无法验证（`content.md:415`）。
8. 公平性：部分按相同 320/960 estimated/training symbols 比较，亦有 proposed-320 vs TS-960 的 overhead tradeoff；公平调参细节不足（`content.md:329-357`）。
9. 消融：无“去掉 coarse/fine/FS reuse”的组件消融。
10. 参数扫描：TS length、`B_L/B_N`、CFO、received power、modulation、turbulence、branch count 均有（Fig. 5–18）。
11. Channel：Fourier phase screen，弱/强两点；参数引用 [30],[31]，但 outer/inner-scale 取理想极限（`content.md:241`）。
12. 场景多样性：B2B + FSO，single/multi branch；无实测、无 pointing/AO、无多距离/多谱型。
13. 理论复杂度：有 real mult/add 分析与 Table I/II；表单元格转换缺失（`content.md:217-229`）。
14. 实测复杂度：无 runtime、latency、memory、FPGA/ASIC resource/energy 测量。
15. Verification：**3/3**——公式化方法与多维仿真、重复平均支持“实现是否按预期工作”。
16. Validation：**2/3**——有 coherent FSO+turbulence/diversity platform，但仅理想化仿真且场景跨度有限。
17. Uncertainty：**1/3**——有 800/6400 次平均，却无 seed、error bar、CI 或统计检验。

---

## 写作架构标杆提取

### 1. 三级标题结构

canonical HTML 丢失 Section II–V 的一级标题文本，以下只按正文的显式组织句和 `###` 小节重建，不能当作逐字标题：

1. Title（H1）
2. Abstract（H2）
3. Introduction（转换中无显式 heading；问题—已有方法—空白—贡献，`content.md:95-101`）
4. Section II（方法章节名缺失）
   - A. TS Design（H3，`content.md:103`）
   - B. Principles of FS and FOE（H3，`content.md:117`）
   - C. Complexity Analysis and Comparison（H3，`content.md:217`）
5. Section III（simulation platform，章节名缺失；`content.md:231-243`）
6. Section IV（results/discussion，章节名缺失）
   - A. Performance Analysis and Discussion of FS（H3，`content.md:245`）
   - B. Performance Analysis and Discussion of FOE（H3，`content.md:277`）
7. Section V（conclusion heading 缺失；`content.md:385`）

### 2. 核心章节比例

按 `content.md` 核心行范围做英文 token 近似计数（排除页面导航、图 caption 与 References 后页面）：Introduction 11.2%（95–101）；Method 34.5%（103–229）；Simulation setup 7.2%（231–243）；Results 44.8%（245–381）；Conclusion 2.2%（385）。这是转换文本的近似比例，不是 PDF 页数比例。写作重心明显落在“方法推导 + 大量分层结果”，平台描述短而密。

### 3. System Model / Problem / Algorithm 组织

- Problem 在 Introduction 用三段漏斗完成：FSO power-budget/complexity 背景 → blind FOE 与 TS FOE 分类及各自机制性不足 → 本文 FSTS 贡献与章节预告（`content.md:95-101`）。
- System/Signal Model 没有独立大节，而嵌入算法原理：先陈述 X/Y CFO 相同与 DSP placement，再用 Eq. (3)–(6) 写接收信号/相位分解（`content.md:105,152-173`）。
- Algorithm 遵循“训练结构 → FS metric → coarse FOE → fine FOE → final composition → complexity comparison”的因果顺序（`content.md:103-229`）。这种顺序让每个公式都对应一个明确 DSP 模块。
- Simulation platform 放在算法之后、结果之前，按 Tx → channel → Rx → offline DSP 顺序写一遍端到端链路（`content.md:231-243`）。

### 4. 参数 / 符号展示

- 先用示意图定义 `T_X_1st/T_X_2nd/T_Y_1st/T_Y_2nd` 与 `B_N/B_L`，随后在公式后用 prose 逐个释义（`content.md:107,160,173,183`）。
- 参数选择不是集中在单一总表，而是随实验逐步收敛：FS threshold/length（Fig. 5–7）→ MSE threshold（Fig. 8）→ length benchmark（Fig. 9）→ `B_L/B_N` structure（Fig. 10）。优点是叙述与证据紧邻；缺点是复现参数分散。
- 数值通常带单位和物理含义，但 frame、PRBS order、ADC rate 等未集中列出；若作为标杆，应借鉴“公式后释义”，不应照搬“参数分散”。

### 5. 图表类型、数量与 caption 模式

- 正文图：**18 幅（Fig. 1–18）**；表：**2 个（Table I–II）**。另页面有 graphical abstract，但不计正文编号图（`content.md:61,109-113,221-229,377-381`）。
- 类型分布：结构图 1（Fig. 1）、algorithm block diagram 1（Fig. 2）、threshold/flow schematic 1（Fig. 3）、system platform + optical-field insets 1（Fig. 4）、timing metric 1（Fig. 5）、FS accuracy/sensitivity 2（Fig. 6–7）、FOE/BER parametric curves 11（Fig. 8–18）。
- Caption 模式高度压缩：`指标 vs. 自变量 + 条件/调制/子图映射`。例如 Fig. 11/12 caption 把 modulation、training length 与 panel `(a)-(d)` 一次说完（`content.md:311-325`）；FSO 图把 `C_n^2` 直接放 caption（`content.md:341-371`）。
- Table I/II 分别承担单 FOE 硬件复杂度与 joint FS+FOE 复杂度，避免把复杂度叙述塞进结果曲线（`content.md:217-229`）。

### 6. Baseline / 消融 / 指标 / 复杂度实验组织

- Baseline 由“方法类别综述”自然导入，先解释为何选 4th-power、4th-FFT、TS，再在 Fig. 9–13 逐层比较 MSE、频偏范围、功率鲁棒性与 BER（`content.md:97-99,289-335`）。
- FSO 阶段缩减 baseline：只保留 4th-FFT 与 conventional TS，文中显式说明（`content.md:339`）；这是从算法诊断转向系统验证的收敛。
- 没有 component ablation；以 TS length、`B_L/B_N`、modulation、power、CFO、turbulence、branch count 的参数扫描代替。不能把参数扫描误称为完整消融。
- 指标链呈现为 `timing metric/FS accuracy → normalized FOE MSE → BER threshold → receiver sensitivity`，用 Fig. 8 把 estimation-domain MSE 与 communication-domain BER 建桥（`content.md:245-329`）。
- 复杂度先给解析 real mult/add（Section II-C），系统结果再报告 performance-complexity tradeoff；但没有实测 runtime/resource（`content.md:217-229,339,385`）。

### 7. Introduction 叙述链

1. FSO 优点与 atmospheric-channel 问题。
2. coherent DSP + M-QAM + PM 提高容量，但 turbulence 造成强度/相位/耦合波动，spatial diversity 又增加复杂度。
3. 将系统问题压缩到关键 DSP 模块 FOE 的性能—复杂度矛盾。
4. 分类审查 blind FOE：4th-power 兼容性/范围问题，4th-FFT 复杂度/短序列分辨率问题。
5. 审查 TS FOE：范围/多格式优点，但 length-dependent accuracy、overhead 与 start-point locating 问题。
6. 给出本文 FSTS、共享 LO/MRC 后 joint compensation、两阶段复用训练序列与 PM 4/16-QAM 验证（`content.md:95-101`）。

这条链的优点是每一项贡献都直接回扣上一段的具体 failure mechanism，而不是从“无人做过”起笔。

### 8. Conclusion 叙述链

结论只有一个紧凑段落：重述方法与场景 → 320-vs-960 performance/complexity headline → 双分支弱/强湍流的 4/16-QAM 具体 dB 数字 → 汇总 accuracy/range/FS/complexity/multi-format → 保守落到 potential application（`content.md:385`）。它没有引入新指标或新实验，但“optimal complexity reduced about 75%”的比较口径需回读正文才能避免与 25% 混淆。

### 9. 公式引入、推导与编号

- 共 **11 个编号公式**。Eq. (1)–(2) 定义 FS metric/correlation；Eq. (3)–(4) 为双偏振复信号；Eq. (5)–(6) 为相位-only 化简；Eq. (7) 为 coarse FOE；Eq. (8)–(10) 为 fine FOE 与两项配对；Eq. (11) 为两级合成（`content.md:119-215`）。
- 典型模式是：先用一句 prose 说明模块目的 → 写公式 → 紧接逐符号定义 → 用训练结构/慢变假设解释为何相位项被消除 → 再给 range/noise/complexity tradeoff。核心算法公式不孤立出现。
- 推导属于工程解释而非严格统计证明：例如“Gaussian noise by summation”“noise reduced by `B_L` times”以引用 [26] 和结构说明支撑，没有给方差传播的完整证明（`content.md:183,208`）。

### 10. 共同引用但本 GW 未覆盖的基础文献（仅列，不检索）

由于 canonical 文本明确说 References unavailable，只能列编号和本文赋予的角色，不能补题名/作者/年份：

- [10] time-domain 4th-power FOE。
- [11] 4th-FFT maximum spectral-line FOE。
- [15] QPSK-partition phase-difference 4th-power FOE for 16-QAM。
- [17] limited spectral resolution / phase-noise discussion。
- [18] conventional TS-based FOE。
- [19] TS-based joint frame and frequency synchronization。
- [22] Park frame-synchronization timing metric。
- [23] turbulence slow variation / diversity-branch phase correction。
- [24], [25] polarization-demultiplexing phase-shift context。
- [26] Gaussian phase-noise effect and `B_L` scaling rationale。
- [27], [28] 4th-FFT hardware-complexity formulas；[29] dual-polarization complexity accounting。
- [30] Fourier-transform phase-screen model；[31] refractive-index structure parameter。

来源位置：`content.md:97-99,119,160-173,208-225,241-243,415`。上述仅是 paper-internal citation anchors，不代表已经在本 GW 精读或核验这些文献。

## 最终边界

本文足以确立“FSTS + deterministic two-stage FOE + spatial-diversity PM coherent FSO simulation”的 source baseline 事实，但不提供星地 lag-ranking crossover、conditioned-single-lag failure、RML-FSTS novelty 或 Go/No-Go 证据。任何从 `B_L` tradeoff 到 target lag behavior 的连接只能保留为 **INFERENCE/UNKNOWN**。
