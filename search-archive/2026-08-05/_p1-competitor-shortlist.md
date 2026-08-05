# P1 Step 1 候选初筛矩阵（metadata/abstract 级）

> 生成: 2026-08-05 | 来源: 4 个 `tools/search` 查询（`r1-*.json`）+ 全局索引复用筛选（21k 行）
> **重要：本矩阵是 Step 1 metadata/abstract 级初筛，不是 Step 3 精读结论。**
> 凡"是否一次生成 Mth-power 序列 / FOE/CPE 是否共享 / 成本证据"等列，均基于 title+abstract，
> **不得当精读后的方法/数据流/竞品全文结论使用**。这些正是 Step 3 要关闭的问题。

## A. 检索质量门槛核对（gw-search.md）

| 门槛 | 要求 | 实际 | 通过 |
|---|---|---|---|
| 去重候选数 | ≥20 | **97**（4 查询）+ 索引复用 ~35 命中 | ✅ |
| 数据源数 | ≥3 | **4 API**（S2 / OpenAlex / SerpAPI-scholar / Exa）+ 全局索引复用 | ✅ |
| 必读数 | ≥5 | 见下方"必读"层（≥12 篇高相关） | ✅ |
| 正式发表占比 | ≥50% | ~97%（venue 核对；unknown 多为 IEEE 作者页/旧会议，待 DOI 补） | ✅ |
| 技术路线 | ≥2 | **3 类**（① VV/Mth-power/FF-joint FOE+CPE；② low-complexity/hw-efficient CR；③ coherent optical/FSO hw-CR） | ✅ |
| 路径合规 | search-archive/2026-08-05/{slug}.json | 4 `r1-*.json` + 本矩阵 + 索引复用筛选 | ✅ |

3 语义类覆盖（brief §4 要求）：
1. **Mth-power / Viterbi-Viterbi / feedforward joint FOE+CPE**：✅（#1 查询命中 16 篇相关 + 索引复用 10 篇）
2. **low-complexity / shared computation / common subexpression / joint FOE/CPE dataflow**：⚠️ 部分覆盖。
   generic "common subexpression / computation reuse / compute graph" 在领域内近乎空集；命中均经
   carrier-recovery 词汇进入（"shared correlation within FOE and CPE" 等）。**索引复用扫描已确认这一空白**——
   对 P1 新颖性有利，但也意味着共享图数据流几乎无直接文献对标（Step 3 需精读确认）。
3. **coherent optical/FSO/PSK/APSK/QAM hardware-efficient CR 实现**：✅（#3/#4 查询 36 篇相关 + 索引复用 11 篇）

> 二轮定向检索：已完成（4 查询本身就是按 3 语义类的定向深搜）。索引复用 + 定向查询交叉确认：
> **没有论文显式提出"在 FFT-FOE 与 mean-angle CPE 之间共享单个 raised-power 中间量作为计算图优化"**。
> 最接近的是方法级（同 VV/monomial 用于 FOE+CPE），不是实现级。此为 Step 1 metadata 级观察，
> Step 3 精读须确认。

## B. 直接竞品初筛矩阵（核心，按 P1 相关度排）

> 列说明（均为 metadata/abstract 级判定，标 `[META]`；全文语义待 Step 3）：
> - **场景**：应用上下文（optical fiber / FSO / inter-satellite / sat-ground）
> - **一次生成 Mth-power 序列**：abstract 是否提及单次升幂驱动多估计器（`[META]`）
> - **FOE/CPE 共享**：abstract 是否提及共享中间量/dataflow（`[META]`）
> - **成本证据**：abstract 是否给出 operation count / latency / FPGA / resource 数字（`[META]`）
> - **与 P1 关系**：method-level（同估计器族）/ implementation-level（同数据流优化）/ context-only
> - **全文状态**：未获取 / 待获取

### B1. HIGH-RELEVANCE（直接对标，优先 Step 2 获取）

| 论文 | 年/venue/状态 | 场景 | 一次Mth-power `[META]` | FOE/CPE共享 `[META]` | 成本证据 `[META]` | 与P1关系 | 全文 |
|---|---|---|---|---|---|---|---|
| Simplified CR for Intradyne Optical PSK Receivers in udWDM-PON (10.1109/JLT.2018.2831918) | 2018 JLT published | coherent optical PSK | 部分（单符号 correlation） | **是**（abstract 明言 shares correlation within FOE and CPE blocks） | 能耗下降（abstract） | **implementation-level 最接近**（共享 op，但用 correlation 非 Mth-power） | 待获取 |
| LUT-Free CR for Intradyne Optical DPSK Receivers in udWDM-PON (10.1109/jlt.2019.2892901) | 2019 JLT published | coherent optical DPSK | 否（避免 mth-power） | 部分（简化 frequency comp） | FPGA 原型（abstract） | implementation-level 同族（简化 FOE+CPE 共享 op 思路） | 待获取 |
| FOE and CPR for high-order QAM using VV monomial estimator (10.1109/CSNDSP.2014.6923933) | 2014 CSNDSP published | coherent optical M-QAM | **是**（VV monomial 同时驱动 FOE+CPR） | 部分（同估计器族，未声明中间量复用） | 未提 | **method-level 最接近**（同数学设定；P1 是其 implementation 增量候选） | 待获取 |
| Low-complexity joint FOE and CPE based on QPSK partitioning for DP-16QAM (10.1364/OFC.2013.OTU3I.5) | 2013 OFC published | coherent optical 16QAM | 部分（QPSK-partition 单次） | 是（joint FOE+CPE 同 stage） | 未提 | method-level joint FOE+CPE | 待获取 |
| Joint CPE+FOE parallel DA-ML DP receiver (10.1364/OE.25.005217) | 2017 Opt.Express published | coherent optical DP | 部分 | 是（joint parallel） | 未提 | method-level joint FOE+CPE（DA-ML 非 Mth-power） | 待获取 |
| A noise-tolerant CPR for inter-satellite coherent optical (electronics 14020265) | 2025 published | **FSO inter-satellite** | 部分（FF + 反馈级联） | 部分 | **"resource consumption decreased by 64%"** | context + 成本对标 | 待获取 |
| Carrier recovery for sat-ground coherent laser using double feedback loop + VV FF cascade | 2023 (22 cites) | **FSO sat-ground** | 部分（VV FF cascade） | 部分（两阶段） | 未提 | context + method-level VV | 待获取 |
| Low-complexity CPE for space coherent optical (10.1117/12.3059522) | 2025 HPCCE published | **space coherent optical** | 否（避免 4th-power） | 否 | "显著降低硬件复杂度" | context（同成本动机，反向：去 Mth-power） | 待获取 |

### B2. MEDIUM（method-level / context，建议获取部分）

| 论文 | 年/venue/状态 | 与P1关系 | 全文 |
|---|---|---|---|
| Generalised analysis of monomial-based VV algorithms for NDA CPE (10.1049/EL:20063881) | 2006 published | **NDA VV Mth-power 理论基础**（必引） | 待获取 |
| Joint ML/MAP freq+phase Wiener CPN (10.1109/TSP.2021.3137966) | 2021 TSP published | joint freq+phase 理论上界 | 待获取 |
| Multiplier-Free CPE (10.1109/LPT.2016.2586076) | 2016 PTL published | V&V hw 简化（去乘法器） | 待获取 |
| Low-latency CPR Hardware (10.1109/ISCAS48785.2022.9937906) | 2022 ISCAS published | CPR hw 延迟对标 | 待获取 |
| Hardware-Efficient Coherent Digital Receiver Concept FF CR (10.1109/jlt.2008.2010511) | 2009 JLT (1024+ cites) | **foundational FF CR for M-QAM**（必引） | 待获取 |
| Demonstration of CFO estimator for 16/32-QAM: hw perspective (10.1364/oe.26.004853) | 2018 OE published | FOE hw 分支对标 | 待获取 |
| Hardware-Efficient Adaptive EQ and CPR 100G WDM-PON (10.1109/jlt.2017.2784804) | 2018 JLT published | "halve redundant compute" 同思路 | 待获取 |
| Low-Complexity CPR Architecture Using Prefix-Sum (10.1109/LCOMM.2026.3653195) | 2026 CL published | 最新 hw CPR 架构 | 待获取 |
| DSP for Coherent Single-Carrier Receivers (10.1109/JLT.2009.2024963) | 2009 JLT published | canonical DSP incl. FF FOE/CPE | 待获取 |
| Low Complexity Parallel CFO Est, Time-Tagged QPSK Partition, coherent FSO (10.3390/photonics11090885) | 2024 Photonics published | **FSO** + modified Mth-power FOE | 待获取 |
| Symmetric TS-Based CFO Estimation coherent FSO (10.1109/jphot.2022.3161795) | 2022 Photonics J published | FSO + 避免 4th-power（量化成本） | 待获取 |
| Two-stage freq compensation Doppler BPSK FSO (10.3389/fphy.2023.1099867) | 2023 Frontiers published | FSO 两阶段 FOE + 资源节省 | 待获取 |
| Low complexity CPR based on Kalman filter w/ priors (10.1117/12.3048518) | 2024 SPIE published | NDA feedforward CPR hw | 待获取 |
| CPR Loop 3.2-pJ/b 24-Gb/s QPSK (10.1109/jssc.2025.3607917) | 2026 JSSC published | energy-efficient CPR silicon | 待获取 |

### B3. 排除（与 P1 无关，关键词误命中）

Viterbi **decoder**、NOMA、routing、ML training、frequency-comb source、IQ imbalance、time/frequency
transfer、pure channel model、6G survey 等共 ~20 篇（详见 `r1-*.json` 的 relevance 字段）。

## C. Step 1 结论（仅 metadata 级，不当 Go/Kill）

1. **文献空间存在**：Mth-power / VV / feedforward joint FOE+CPE / hw-efficient CR 是活跃成熟领域，
   有充分 method-level 与 implementation-level 对标（≥12 篇必读/建议读）。
2. **P1 数据流共享的具体 claim 在 metadata 级未被显式覆盖**：最接近的是
   ① udWDM-PON 2018/2019（共享 correlation，非 Mth-power）；② CSNDSP 2014（同 VV monomial 驱动
   FOE+CPR，未声明中间量复用）。**是否构成可区分工程 claim，必须由 Step 3 精读全文关闭**。
3. **成本动作真实**：abstract 级已见"resource 下降 64%""避免 time-consuming 4th-power""halve
   redundant compute""降低硬件复杂度"等成本对标，Step 3 须确认 operation count/latency/hw 数字。
4. **关键未知（Step 3 关闭，本轮不关）**：
   - 是否有论文在 FFT-FOE + mean-angle CPE 之间显式共享单次 raised-power；
   - 共享图相对 conventional refactor 是否还有可区分工程 claim；
   - matched-performance comparator（同 BER 下操作数对比）是否有现成数据。
5. **本轮不得据此宣称 P1 新颖/有效/能成章**（brief §0 纪律 2）。Step 1 只确认检索覆盖面与初筛，
   terminal 属 Step 2 覆盖面门。
