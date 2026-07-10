# [S001] 双偏振星地光通信 DSP — GW Step 1 检索策略规划

> 2026-07-10 | GW Step 1 | 状态：规划完成，待新对话执行

## 目标

按 FR-22 从 GW Step 1 重走地勘。scenario-transfer-pivot D003 解锁双偏振空间后，搜索空间从单偏振扩到含双偏振 OSL。**本轮只规划检索策略，不直接开搜**（守 D017 穷举门控——先规划穷举范围，确认全景再执行）。

承接：scenario-transfer-pivot H001（方法论准备全部就绪）+ D001 三维度调整 + D002 角度素材 schema + D003 双偏振空间解锁。

## 记录

### 背景认知

**双偏振是什么**：光作为电磁波，电场在垂直传播方向的平面里某方向振动=偏振态。单偏振=一束光用一个偏振态承一路信号（接收端处理一个复数序列）；双偏振（dual-polarization / PolMUX）=用两个正交偏振态各自承一路 QAM 信号合在一束光里传，**频谱效率翻倍**。光纤商用 100G/400G 相干模块全是双偏振（DP-QPSK / DP-16QAM）。

**双偏振在 DSP 上更麻烦的原因**：两个偏振态传输中互相串扰（光纤双折射 / 大气偏振扰动致偏振态旋转耦合）。接收端要 2×2 MIMO 自适应均衡（CMA/MMA 盲算法）把两路解复用。sat.1553 §6（227 行全书最大）讲的就是偏振解复用 + 自适应均衡 + PMD/SOP/PDL 双偏振特有物理效应。

**FPGA 实现判断**：双偏振 DSP 在光纤 FPGA/ASIC 上已极成熟（十几年商用），走 R001 成功论文套路（迁移成熟 DSP + 刻画性能边界）可借成熟架构，不构成障碍。FPGA 实现通常不是论文核心贡献（除非导师要求或方向本身做实现）。

### 搜索空间界定

D003 解锁核心是 sat.1553 §6 偏振解复用层（227 行全书最大 + open problem 最多）。但双偏振不只影响 §6——§3 定时 / §4 载波相位 / §5 载波频偏在双偏振下都有架构变化（两偏振态联合/并行处理 vs 单偏振）。检索覆盖双偏振 OSL 的 **DSP 全谱**，重点 §6，兼及 §3/4/5：

| 层 | sat.1553 行号 | 双偏振引入的变化 | 检索权重 |
|----|--------------|-----------------|---------|
| §6 偏振解复用/均衡 | L561-787（227 行） | CMA/MMA/DA-LMS/MMSE/Stokes/MIMO 2×2 + PMD/SOP/PDL/DGD | **主轴**（D003 解锁核心） |
| §3 定时 | L169-384（216 行） | 双偏振联合 TED vs 单偏振 | 次 |
| §4 载波相位 | L385-450（66 行） | 双偏振联合 CPE / 偏振态旋转补偿 | 次 |
| §5 载波频偏 | L451-560（110 行） | 双偏振 FOE | 次 |
| 迁移源（光纤成熟 DSP） | — | 光纤双偏振相干 DSP 全套（迁移参照，合法迁移适配论证需要） | 参照 |
| 综述锚 | — | sat.1553 同类 OSL DSP 综述（定穷举基线） | 必读 |

**检索权重逻辑**：§6 是 D003 明确解锁的最大层 + open problem 最多（step size μ 无理论最优 / fade 期 CMA 发散 local optimum 未分析 / 理想相位补偿假设偏强），主轴。§3/4/5 是双偏振架构变化的次级影响。迁移源 + 综述锚是合法迁移适配两标准（不变量2）的论证原料。

### 关键词组（5 组不同角度，守 gw-search.md ≥3 组 + D017 穷举）

**组 1 — 方法×场景（直接相关星地双偏振 DSP）**
- `"dual polarization" + "satellite optical" / "free-space optical" + "coherent"`
- `"polarization demultiplexing" + "satellite" / "free space"`
- `"MIMO equalizer" + "coherent optical satellite" / "FSO"`

**组 2 — 具体算法（方法细节）**
- `"constant modulus algorithm" / "CMA" + "optical satellite" / "free space"`
- `"Stokes space" + "polarization" + "optical communication"`
- `"adaptive equalizer" + "dual polarization" + "turbulence"`

**组 3 — 物理效应（双偏振在大气湍流下的物理建模，验"假设不成立"）**
- `"polarization mode dispersion" / "PMD" + "atmospheric turbulence" / "free space"`
- `"state of polarization" / "SOP" + "turbulence" + "tracking"`
- `"polarization dependent loss" / "PDL" + "satellite" / "free space optical"`

**组 4 — 迁移源（光纤成熟双偏振 DSP，合法迁移适配"B 场景下 A 哪个假设不成立"论证需要）**
- `"dual polarization coherent" + "fiber" + "digital signal processing"`
- `"polarization demultiplexing" + "coherent" + review/survey`

**组 5 — 综述锚（定全景穷举基线，sat.1553 同类）**
- `"coherent optical satellite" + "signal processing" + review/survey`
- `"free space optical" + "DSP" + review`

### 搜索源
- `tools/search --mode academic --preset scenario-method`（主源，多源 ≥15 条/源）
- `tools/blit --source cnki --doc-type phd/master`（中文，找同门学位论文双偏振套路）
- 综述类优先（D017 扫描层"综述全文 open problem 段是金矿"）

### 穷举门控守法（D017 红线 6 + D018 + gw-search.md 质量门槛）

1. **扫描层只列不判**：检索结果全列出分类（偏振解复用 / 物理建模 / 迁移源 / 综述），**不在检索阶段判 Go/Kill 或排优先级**（D018 中性提取）
2. **覆盖度硬门**（gw-search.md）：去重后 ≥20 条 + 覆盖 ≥2 子方向（偏振解复用方法族 + 物理效应建模）+ 正式发表 ≥50% + 必读类 ≥5 篇
3. **综述必读**：至少抓 1-2 篇 OSL DSP 综述全文，读 §6 对应 open problem 段（sat.1553 §6.3 同类）
4. **预印本占比过高**时用 `tools/blit --source ieee` 补正式发表
5. **穷举完 + 用户确认全景**才进 Step 2 下载 / Step 3 精读（D017 A 门控）
6. **二轮定向检索**（gw-search.md 步骤 6）：从一轮识别 ≥2 个候选子方向，构造方向专属关键词深搜，验证论文池规模 + 创新空白真实性

### 执行流程（新对话）

```
┌─ Step 1 执行（新对话）────────────────────────────────────┐
│ 1. 环境检查（gw-acquire.md）：确认 venv + 依赖            │
│ 2. 执行组 1-5 检索（tools/search + tools/blit cnki）       │
│    - 主对话禁 WebSearch，全走 tools/                       │
│    - 结果存 search-archive/2026-07-17/{slug}.json          │
│ 3. AI 候选审查（gw-search.md 步骤 4）：标 priority +       │
│    priority_reason                                         │
│ 4. 覆盖度评估（gw-search.md 步骤 5）：≥2 子方向 + 无空洞   │
│ 5. 🔴 D017 穷举门控 A：穷举完 + 用户确认全景才推进         │
│    - 产出全景表给用户看（中性提取，不判 Go/Kill）          │
│ 6. 二轮定向检索（gw-search.md 步骤 6）：≥2 子方向深搜       │
│ 7. 最终候选列表落盘                                         │
└──────────────────────────────────────────────────────────┘
```

### 9 次 Kill 候选作思路素材重新进精读池（D001 维度4）

9 次 Kill（载波同步 4 + A3 + N1 + ③ + ISI 均衡 + AO-DSP）在单偏振下 Kill，但作为**思路素材**重新进精读池——不是复活当贡献（不变量1 仍守），是拓宽角度素材。Step 3 精读时如果双偏振 OSL 命中与 9 次 Kill 相似机制，可对照看"双偏振下是否解除了单偏振的物理瓶颈"。

### D002 角度素材 schema 试用计划

Step 3 精读时试 D002 角度素材 schema（6 类帮想角度来源 + 半结构化字段 + 通信大类通用词表）：3-5 篇试用，验证字段/词表/聚合视图有效性，有效后进 gw-read.md。守"先测不改协议"。

## 决策引用

- 无新建决策（本轮是规划，继承上游 D001/D002/D003）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（GW Step 1 检索策略规划，专题原始目标范围内）

## 后续

- **新对话执行 GW Step 1 检索**（守 D017 穷举门控，执行流程见上）
- 检索前如需调整关键词组/搜索源，在本 S001 更新（不另建文件）
- Step 1 通过质量门槛后进 Step 2 下载（gw-acquire.md）

---

## 检索执行结果（2026-07-10 执行追加）

> 状态变更：规划 → **已执行**。用户"你一直往下做吧"授权后本轮完成检索 + AI 审查 + 覆盖度评估。

### 执行记录

- **环境准备**：torch venv（`$HOME/.venvs/torch`，Python 3.14）新建 + 装依赖（requests/serpapi/tavily/jieba）。`tools/search` wrapper 在 Windows 找 `bin/python`（Linux 路径）会 fallback 到缺依赖系统 python，直接用 `"$HOME/.venvs/torch/Scripts/python.exe" tools/literature_search.py` 调用绕过。**债务**：wrapper 的 Windows 兼容性待修（其他 wrapper download/convert/blit 同问题）。
- **检索执行**：2 子 agent 并行，组 1-3（9 查询，~125 篇）+ 组 4-5（6 查询，~50 篇）。全部串行（防 API 限流），结果存 `search-archive/2026-07-10/`。
- **综述补搜**：4 查询针对性找双偏振 DSP 综述。
- **AI 候选审查**：1 子 agent 对 9 个 JSON 135 篇标 priority + priority_reason 写回原文件。

### 全景表（去重后核心候选 43 篇）

去重后：**必读 16 / 建议读 27 / 备选 32 / 排除 51 / 未标（历史）445**。全部 published（预印本占比 0%）。年份集中 2023-2026（30/43=70%）。

#### 子方向聚类（一篇可属多类，★=必读）

**A. 多孔径相干数字合并/MIMO 均衡（必读5+建议读7=12）** — 最密集方法子方向
- ★ Multi-Aperture Coherent Digital Combining (JLT 2023, c=15, 10.1109/JLT.2023.3276637) — Ju 团队核心
- ★ Blind skew compensation + digital combining widely-linear (OE 2023, c=5, 10.1364/oe.498562)
- ★ Real-time two-aperture coherent digital combining (OL 2024, c=4, 10.1364/ol.511941)
- ★ Performance Analysis DP-16QAM MIMO-FSO (JCNC 2025, c=3)
- ★ Frequency-domain 4N×2 MIMO adaptive equalizer (Opt Laser Tech 2025, c=2, 10.1016/j.optlastec.2025.113235)
- 建议读：MIMO Neural Network + ML Phase (JLT 2025, c=12) / Blind MIMO CA-CMA (JLT 2025, c=5) / Hierarchical MIMO PDM PS-1024QAM (Opt Commun 2026, c=1) / A 4×4 MIMO Polarization Crosstalk (CICC 2026) / Low-Complexity Hybrid-Precision MIMO (JLT 2026) / Real-time Non-Circular CMA MIMO (OL 2026) / Blind MIMO SDM (SPPCom 2025)

**B. 偏振解复用-CMA/MMA（必读1+建议读5=6）**
- ★ Jitter-Resistant CMA for FSO (ACP 2025, c=0, 10.1109/ACP66871.2025.11350394)
- 建议读：Singularity Avoidance of CMA (ACP 2023, c=2) / CA-CMA SDM (JLT 2025, c=5) / CMA multicore (IAECST 2022, c=1) / RSOP single-pol CMA (ICOICT 2025) / Real-time Non-Circular CMA (OL 2026)

**C. Stokes 空间偏振处理（必读1+建议读4=5）**
- ★ Circularly-Polarized Self-Homodyne FSO Partial Stokes (OFC 2024, c=2, 10.1364/ofc.2024.w4g.6)
- 建议读：Probability-Aware Stokes Blind PolDemux (JLT 2021, c=9) / Polarization Change Monitor Stokes (ECOC 2021, c=3) / Side Effect Normal Vector Recovery Stokes (ECOC 2020, c=1) / SOP Rotation Tracking Complementary (LOP 2020)

**D. SOP/RSOP 跟踪与均衡（必读0+建议读8=8）** — 全是迁移源（光纤域），星地专属少
- 建议读：Complementary Polarization-Diversity Receiver (JLT 2022, c=20) / Polarization Tracking PDL+Fast Temporal (JLT 2022, c=9) / Fast tracking DSP (MOPL 2021, c=5) / Ultra-fast SOP rotation feedforward (OE 2025, c=3) / Feed-Forward FDE Fast SOP (JLT 2023, c=1) / pilot-tone SOP tracking (2021, c=1) / RSOP single-pol CMA (2025) / Ultra-Fast Azimuth Rotation SOP (ACP 2023)

**E. PDL/PMD 物理效应与补偿（必读0+建议读3=3）** — 偏薄
- 建议读：Polarization Tracking PDL+Fast (JLT 2022, c=9) / Total PDL cascaded (2023, c=2) / Exact PDL-induced SNR statistics (OE 2026, c=0)

**F. 双偏振 FSO 相干系统 demo/分析（必读16+建议读5=21）** — 场景论文（含 A 类方法的宿主）
- ★ 含 A 类 5 篇 + Field Demo Turbulence-Resilient Self-Coherent (JLT 2025, c=7, 10.1109/jlt.2025.3564551) + 10 Gbps Coherent Receiver FSO (RPIC 2023, c=3) + DP Self-Coherent Transceivers FSO (IEEE Access 2025, c=2, 10.1109/ACCESS.2025.3535789) + 56-GBaud GEO DP-QPSK (ICSOS 2023, c=1, 10.1109/ICSOS59710.2023.10490279) + ANN Equalization Polarization Mixing (IEEE Access 2026) + Data-Aided Multi-Format DSP FSO (WiSEE 2024) + Bootstrapping Blind Equalizer DP FSO VAE (TCCN 2026, 10.1109/TCCN.2025.3631007) + Intelligent FSO System DSP (JIFS 2026) + EKF PolDemux Multi-Path FSO (OFC 2026, 10.1364/ofc.2026.w2a.67)

**G. 神经网络/ML 盲均衡（必读1+建议读2=3）**
- ★ Intelligent FSO System DSP (JIFS 2026)
- 建议读：MIMO Neural Network + ML Phase (JLT 2025, c=12) / Unsupervised Domain Adaptation AdapEq (2025)

**H. 迁移源-光纤双偏振 DSP（必读4+建议读8=12）** — 方法可迁移到星地
- ★ 56-GBaud GEO DP-QPSK (ICSOS 2023) / Data-Aided Multi-Format DSP (WiSEE 2024) / EKF PolDemux FSO (OFC 2026) / DP-16QAM MIMO-FSO (JCNC 2025)
- 建议读：Fast tracking DSP (MOPL 2021) / Singularity Avoidance CMA (ACP 2023) / Feed-Forward FDE SOP (JLT 2023) / Hierarchical MIMO PDM (Opt Commun 2026) / Exact PDL SNR (OE 2026) / Unsupervised AdapEq (2025) / 4×4 MIMO Crosstalk (CICC 2026) / Real-time Non-Circular CMA (OL 2026)

#### 综述锚（穷举基线）
- **sat.1553**（Valjus 2025, Int J Satellite Commun, DOI 10.1002/sat.1553）— 唯一可靠的 OSL DSP 全景综述，已落盘 `papers/doi/10.1002_sat.1553/content.md`，§6 偏振解复用 227 行
- Weng 2019 "DSP for MDM MIMO Equalization: A Review" (Applied Sciences, c=26) — 光纤 MIMO 均衡迁移源
- Neves 2024 "Carrier-Phase Recovery for Coherent Optical" (JLT, c=23) — CPR 子领域
- **空洞确认**：专门的"双偏振光通信 DSP 全景综述"领域不存在（不是检索盲区，是领域现状）。sat.1553 仍为穷举基线主锚。

### 覆盖度评估（gw-search.md 质量门槛核对）

| 门槛 | 标准 | 实际 | 状态 |
|------|------|------|------|
| 去重后 ≥20 条 | 20 | 43 核心（必读16+建议读27），备选32 另算 | ✅ |
| 覆盖 ≥3 搜索源 | 3 | S2 + OpenAlex（+ 综述补搜 2 源） | ✅ |
| 必读类 ≥5 篇 | 5 | 16 | ✅ |
| 覆盖 ≥2 子方向 | 2 | 8 个子方向聚类（A-H） | ✅ |
| 正式发表 ≥50% | 50% | 43/43 = 100% published | ✅ |

**覆盖度空洞分析**：
1. **SOP/RSOP 跟踪(D) + PDL/PMD(E) 星地专属少**：8+3=11 篇大多是光纤域迁移源，直接在星地/大气湍流下做 SOP/PDL 跟踪补偿的论文稀少 → 这是潜在的"假设不成立"论证空间（不变量2：B 场景下 A 哪个假设不成立）
2. **多孔径数字合并(A, 12篇)是 Ju 团队主导**：方法密集但集中在一个课题组（BUPT/Ju），需精读后判断 A1 归属（是否已被占完，D017 4 档表第 2 档风险）
3. **CMA/Stokes 算法变体(B/C)多为光纤域**：迁移到星地需验"B 场景假设不成立"（湍流致 SOP 快变 vs 光纤慢变是根本差异）

### D017 穷举门控 A 状态

**穷举完成**：5 组 + 综述补搜 = 15 查询，去重 43 核心 + 32 备选 = 75 篇有效候选 + sat.1553 综述锚。8 子方向全列出。

**待用户确认全景**：上述全景表交用户确认后，进 Step 2 下载（优先必读 16 篇 + 综述锚 sat.1553 已有）→ Step 3 精读。

**二轮定向检索候选子方向**（gw-search.md 步骤 6，待全景确认后执行）：
- 子方向 1：多孔径相干数字合并/MIMO 均衡（A 类，方法最密集，Ju 团队主导需验 A1 归属）
- 子方向 2：CMA/Stokes 偏振解复用在湍流下的适配（B+C 类，光纤→星地迁移的"B 场景假设不成立"论证空间）

---

## Step 2 下载执行结果（2026-07-10 执行追加）

### 下载执行记录

- **第一轮 tools/download**（arXiv/OA/Unpaywall/Firecrawl）：4 篇成功（JCNC OA / ICSOS firecrawl / OE OA / Access 已 cached）
- **环境补强**：torch venv 装 playwright + chromium（blit 依赖）+ pymupdf4llm（转换依赖）
- **第二轮 blit IEEE**（校园网 IP 自动机构认证）：7 篇目标全部定位+下载，5 篇转换成功（2 篇是 IEEE 登录页外壳）
- **wrapper 兼容性修复**：tools/search、download、blit、convert 四个 wrapper 的 python 检测逻辑加 `Scripts/python.exe`（Windows），一次性修复所有工具
- **转换归档**：blit PDF → papers/doi/{doi_path}/source.pdf + content.md（pymupdf4llm fast 模式）

### 必读 16 篇下载状态

**✅ 成功（≥50行）9 篇**：
| DOI | 标题 | 子方向 | 行数 |
|-----|------|--------|------|
| 10.1109/JLT.2023.3276637 | Multi-Aperture MIMO 2N×2 Equalizer | A 多孔径 | 270 |
| 10.1364/oe.498562 | Blind skew compensation combining | A 多孔径 | 590 |
| 10.1109/RPIC59053.2023.10530744 | 10Gbps Coherent Receiver FSO | F 双偏振FSO | 198 |
| 10.1155/jcnc/4243779 | DP-16QAM MIMO-FSO Performance | F 双偏振FSO | 1165 |
| 10.1109/ACCESS.2025.3535789 | DP Self-Coherent Transceivers FSO | F 双偏振FSO | 648 |
| 10.1109/ICSOS59710.2023.10490279 | 56-GBaud GEO DP-QPSK DSP | F 双偏振FSO | 873 |
| 10.1109/WiSEE61249.2024.10850117 | Data-Aided Multi-Format DSP FSO | F 双偏振FSO | 268 |
| 10.1109/TCCN.2025.3631007 | Bootstrapping Blind Equalizer DP VAE | G 神经网络 | 607 |
| 10.1109/ACP66871.2025.11350394 | Jitter-Resistant CMA FSO | B CMA | 166 |

加 sat.1553（综述锚，1581 行）= **10 篇可用于精读**。

**⚠️ 登录页外壳 1 篇**（机构订阅不覆盖）：
- 10.1109/ACCESS.2026.3683348 ANN Equalization（IEEE Access 2026，两次都抓到登录页）

**❌ 付费墙未获取 6 篇**：
- 10.1109/jlt.2025.3564551 Field Demo Self-Coherent（JLT 2025，登录页外壳）
- 10.1364/ol.511941 Real-time two-aperture combining（Optica，blit 不支持）
- 10.1016/j.optlastec.2025.113235 Freq-domain 4N×2 MIMO（Elsevier）
- 10.1364/ofc.2024.w4g.6 Circularly-Polarized Self-Homodyne（Optica OFC）
- 10.1177/18758967261457271 Intelligent FSO System（SAGE）
- 10.1364/ofc.2026.w2a.67 EKF PolDemux FSO（Optica OFC）

### 覆盖面缺口分析（gw-acquire.md 阻塞门）

- **成功率 9/16 = 56%**（含 sat.1553 为 10/17）
- **子方向影响**：
  - A 多孔径：2/4 成功（核心 MIMO JLT 2023 + OE 偏振解复用可用，但缺 Real-time OL 2024 和 Freq-domain OLT 2025）
  - F 双偏振FSO：5/6 成功（覆盖最好）
  - G 神经网络：1/3 成功（Bootstrapping VAE 可用，缺 ANN Access + Intelligent SAGE）
  - B CMA：1/1 成功
  - C Stokes：0/1 成功（Circularly-Polarized OFC 未获取）
- **付费墙分布**：Optica 3 篇（OFC 会议论文为主）+ Elsevier 1 + SAGE 1 + IEEE JLT 2025 登录页 1
- **正式发表占比**：成功的 9 篇全 published（100%），失败的也全 published——发表状态不影响下载通道

### 用户行动项

- [ ] 手动获取最优先 3 篇（机构 VPN / 作者主页 / ResearchGate）：
  1. 10.1364/ol.511941 Real-time two-aperture combining（A 多孔径唯一 FPGA 实时实现）
  2. 10.1109/jlt.2025.3564551 Field Demo Self-Coherent（F 类最新现场实验）
  3. 10.1016/j.optlastec.2025.113235 Freq-domain 4N×2 MIMO（A 类频域方法）
- [ ] 放入 `papers/downloads/2026-07-10/` 后用 `bash tools/convert papers/downloads/2026-07-10/{file}.pdf` 转换
- [ ] 如当前覆盖面可接受（9 篇 + sat.1553 覆盖 A/B/F/G 四子方向），确认后进 Step 3 精读
