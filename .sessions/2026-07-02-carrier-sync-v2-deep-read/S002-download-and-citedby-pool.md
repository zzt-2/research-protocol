# [S002] 对话 0：补下载 + cited-by 池拉取 + 批量下全文 + D 档挑星地光

> 2026-07-03 | 精读沉淀补强·对话 0（备料阶段）| 状态：备料完成，交对话 1 评点
> 来源：S001 v2 规划"对话 0"段 + v2 改动 2（D 挑星地光）/ 改动 5（债务阻塞优先级）
> **范围变更（2026-07-03 用户纠偏）**：原 S002 只备料 cited-by 池不批量下全文，用户指出"只下几个锚就开始评容易偏"→ 扩范围为批量下 ~25 篇 cited-by 候选全文（见 §范围变更记录）

## 目标

执行 S001 v2 规划的"对话 0"：①补 3 类下载债务（B5/B7/[58][60][79]）②拉 B 档 12 点 cited-by 候选池 ③从 D2-D5 批量 cited-by 里挑星地光命中 ④**【范围扩大】批量下 cited-by 候选池 ~25 篇全文**（用户纠偏：下完再评，防偏）。**本对话不评点、不写笔记、不判 Go/Kill，只备料。**

## 记录

### 报到验证（Trigger 1+5）

- **Trigger 1（Session Start）**：topic-index 不变量 9 条确认；active topic conflicts = none；depends_on（2026-06-20-problem-driven-redirection）输出已满足；profile 最近纠偏 2026-07-02 S030（"急于推进"第 7 次表现——把中性提取当全部产出跳过 D017 步骤 4）；inflation check 本专题 2 S 文件远未到阈值。
- **Trigger 5（Handoff H020 接收）**：3 条关键事实核查全 PASS——①B5/B7 下载失败（papers/doi 实查只有 metadata.json 421/411 字节，无 source.pdf/content.md）②总表 B12+C4+D星地候选已落原专题 topic-index L131/L135 ③B11/B12 S030 中性提取 9 项 grep PASS（原专题进展线索 L283 核对一致）。
- **缓存发现（告知）**：`search-archive/2026-07-02/` 已存大量 cited-by 缓存（sat1553/paillier/kikuchi/pfau/spalvieri/martins/schmidl-cox/twc2024/opll-photonics + carrier-sync-forward-citedby-summary.md），cited-by 拉取优先复用缓存避免重复。

### 步骤 1：补下载（5 篇阻塞债务）

派 2 子 agent 并行（B5/B7 + [58][60][79]），穷尽降级源。**主线独立 grep 核查磁盘文件存在**（FR-26）。

#### 1.1 下载清单

| 候选 | DOI | 状态 | 试过的源（成功路径标 ✅） |
|---|---|---|---|
| **B5** | `10.1016/j.optcom.2024.130981` | ❌**失败**（Elsevier 硬付费墙） | tools/download ❌ / blit IEEE ❌（非 IEEE 无镜像）/ Unpaywall is_oa=False ❌ / Zenodo OA 无匹配 ❌ / Elsevier 直链 403 Forbidden ❌ / OpenAlex is_oa=False ❌ / S2 openAccessPdf CLOSED ❌ / S2 PDF 缓存 404 ❌ / arXiv 无 ❌ / OUCI 仅元数据 ❌ / ResearchGate 仅 Request ❌ / 青岛大学机构库无 OA 仓库 ❌（**穷尽 11 源**）|
| **B7** | `10.1364/ofc.2026.w2a.62` | ✅**成功** | tools/download ❌ / **blit IEEE ✅**（OFC 有 IEEE Xplore 镜像 doc 11525242，1.89MB） |
| **[58] Martins** | `10.1364/OSAC.438524` | ✅**成功** | tools/download ❌ / Optica 直链 JS 挑战 ❌ / **Optica Playwright ✅**（过 checkjs.cfm 抓 directpdfaccess，5.57MB 19 页） |
| **[60] Leven** | `10.1109/LPT.2007.891893` | ✅**成功** | tools/download ❌ / **blit IEEE ✅**（arnumber 4116764，252KB 3 页） |
| **[79] Matsuda** | `10.1117/12.2544050` | ⚠️**仅摘要**（SPIE 硬付费墙） | tools/download ❌ / SPIE 直链 JS 挑战 ❌ / SPIE Playwright body 0 字节 ❌ / NASA ADS Cloudflare ❌ / NICT 机构库未收录 ❌ / ResearchGate 仅题录 ❌ / **web reader ✅ 获完整 Abstract**（**穷尽 7 源**） |

#### 1.2 磁盘核查（FR-26 主线独立 grep）

- `papers/doi/10.1364_ofc.2026.w2a.62/source.pdf`（1,887,563 字节）+ `content.md`（90 行）✅
- `papers/doi/10.1364_osac.438524/paper.pdf`（5,569,336 字节）+ `content.md`（430 行）✅
- `papers/doi/10.1109_lpt.2007.891893/paper.pdf`（252,593 字节）+ `content.md`（179 行）✅
- `papers/doi/10.1117_12.2544050/content.md`（3,623 字节，仅摘要）✅
- `papers/doi/10.1016_j.optcom.2024.130981/`（仅 metadata.json 898 字节，无 PDF）❌

#### 1.3 关键事实修正（S001 原假设纠正）

S001 假设 B5/B7 可能是 DLR（Carl Valjus）团队论文——**子 agent 查证后两者都不是**：
- B5 = 青岛大学 Jiamin Fan 等，"Coarse frequency offset estimation and compensation based on short-time spectrum analysis in FSO communication system"（Optics Communications 2024）
- B7 = 北京邮电大学 Yan Ma 等，"Digital Estimation of Doppler Shift with Gardner Timing Error Detector for Coherent Optical Satellite Communications"（OFC 2026 W2A.62）

### 步骤 2：cited-by 候选池（B 档 12 点，按 S001 v2 篇数估计表）

派 2 子 agent 并行（B7/B8/B9 + B10/B11/B12/D2-D5），B1-B6 复用 `search-archive/2026-07-02/` 缓存。**主线独立 grep 核查 6 个新 JSON 落盘**。

#### 2.1 cited-by 规模实测（含缓存复用）

| B 点 | 锚 | cited-by 规模（实测）| 本点目标筛出 | 实际入池 |
|---|---|---|---|---|
| B1 pilot 窗口 | sat.1553 union 5 + Spalvieri[57] union 85 + Martins[58] union 6 + Leven[60] 理论锚 | sat.1553 5 / Spalvieri 85 / Martins 6 | 2-3 篇 | 见 §2.2 B1 |
| B2 deep fade 冻结 | sat.1553 + Matsuda[79]（仅摘要）+ Panasiewicz 已有 | sat.1553 5 | 2-3 篇 | 见 §2.2 B2 |
| B3 子系统协同 | 张思齐（已有）+ LCOMM/jphot/oe.520452 全已落盘 | — | 3-4 篇（资料最齐） | 见 §2.2 B3 |
| B4 双反馈环 | Paillier union 43 | openalex 34 / S2 31 / union 43 | 3-5 篇 | 见 §2.2 B4 |
| B5 短时谱粗频偏 | Paillier 43（同 B4 去重） | 同 B4 | 2-3 篇 | 见 §2.2 B5 |
| **B6 Z-ODPLL** | OPLL `10.3390/photonics10121312` | openalex 2 / S2 2 / **union 2（极少）** | **1-2 篇** | 见 §2.2 B6 |
| **B7 Gardner TED** | ofc.2026.w2a.62（新拉）| **openalex 0 / S2 0 / union 0** | **1-2 篇（天然稀）** | **池子空，见 §2.2 B7** |
| B8 RL+GS 自相干 | jocn.468220（新拉） | openalex 5 / S2 3 / union 5 | 3-4 篇 | 见 §2.2 B8 |
| B9 虚拟载波自相干+DRE | jlt.2023.3270673（新拉） | openalex 8 / S2 5 / union 8 | 3-4 篇 | 见 §2.2 B9 |
| B10 16-QAM pilot-RLS | s11107-024-01019-2（新拉） | openalex 1 / S2 0 / union 1 | 2-3 篇 | 见 §2.2 B10 |
| B11 NDA-ML STO+CPE | LPT.2024.3523478（新拉） | openalex 1 / S2 1 / union 1 | 3-4 篇 | 见 §2.2 B11 |
| B12 频域 pilot | TCOMM.2022.3171809（新拉） | openalex 7 / S2 2 / union 9 | 2-3 篇 | 见 §2.2 B12 |

#### 2.2 各点候选 DOI（按星地光相关性+真引用筛选）

##### B1 自适应 pilot 窗口（目标 2-3 篇，复用缓存）
- 锚：sat.1553 L440 / Spalvieri[57] union 85 / Martins[58] union 6 / Leven[60] 理论锚（**本轮新落盘**）
- **候选 3 篇**（Spalvieri 85 筛星地光，R004 §4 缓存）：
  1. `10.1364/oe.564097` | Fully utilized pilot-aided DSP with state-pruning MLSD（2025）| 相关性中（pilot 全利用，但光纤互连非星地）| OA+S2 真引用
  2. `10.1109/ICCWorkshops59551.2024.10615713` | DL Phase Noise Mitigation（2024）| 相关性低-出界（wireless backhaul）| S2-only 需验
  3. **[58] Martins（本轮落盘）+ [60] Leven（本轮落盘）= 切入点理论锚，对话 1 精读**
- 入池判定：2 篇 cited-by（弱）+ 2 篇理论锚全文 = 对话 1 评点素材备齐

##### B2 deep fade 冻结（目标 2-3 篇）
- 锚：sat.1553 L558/L582 + **Matsuda[79]（本轮摘要落盘，FO 估计器冻结机制原文坐实）** + Panasiewicz 已有
- **候选 2 篇**：
  1. **[79] Matsuda 摘要原文坐实 sat.1553 L582 引用**——"avoids rapid tracking errors during scintillation, **by turning off the tracking of the FO estimator when the received signal power decreases**"（B2 均衡器冻结来源成立，FOE 专项冻结增量待对话 1 全文核验，但摘要已含 0.6dB 增益信号）
  2. Panasiewicz 博士论文（已有旧笔记，0.42-0.66dB 功率不敏感 atan2 鉴相器非冻结）
- 入池判定：2 篇够（池子天然小，[79] 摘要机制坐实是关键收获）

##### B3 子系统协同（目标 3-4 篇，资料最齐）
- 锚：sat.1553 L788 + 张思齐学位论文（已有）+ LCOMM.2026.3651445 / jphot FSTS / oe.520452（全已落盘）
- **候选 4 篇**（全已落盘，对话 1 直接精读）：
  1. 张思齐学位论文（已有旧笔记）
  2. LCOMM.2026.3651445（已落盘）
  3. jphot FSTS（已落盘，需核）
  4. oe.520452（已落盘，Optics Express 2024）
- 入池判定：4 篇全落盘，对话 1 资料最齐的点

##### B4 双反馈环（目标 3-5 篇，Paillier union 43 筛）
- 锚：optcom.2023.129312（Paillier cited-by 43）
- **候选 4 篇**（Paillier 43 筛星地光+载波同步，复用 R004 §4 + carrier-sync-forward-citedby-summary.md）：
  1. `10.1002/sat.1553` | sat.1553 综述自身（Paillier cited-by 命中，星地光核心综述）| OA+S2
  2. `10.1007/s11432-024-4415-7` | DTAT-FSO 湍流免疫（2024，Spalvieri 池同命中）| OA+S2
  3. `10.1364/jocn.503484` | DRL Cooperative FSO Elastic Splitter（2023）| OA+S2（与 B8 共享）
  4. `10.3390/photonics10050493` | Wavefront Distortion on Coherent Detection（2023，与 B8 共享）| OA+S2
- 入池判定：4 篇够

##### B5 短时谱粗频偏（目标 2-3 篇，Paillier 池去重）
- 锚：optcom.2024.130981（**B5 本轮下载失败**，但 cited-by 池复用 Paillier 43）
- **候选 3 篇**（Paillier 池去重 B4 后新增）：
  1. `10.1109/ICCWorkshops59551.2024.10615713` | DL Phase Noise（与 B1 共享，wireless backhaul 出界标状态）
  2. sat.1553 L558/L582 段（FOE 重锁/deep fade 冻结，B5 短时谱是 CFO 子环节同源）
  3. [60] Leven（本轮落盘）—— Mth power CFO estimator 理论锚（sat.1553 L470）
- 入池判定：3 篇够（B5 全文失败但理论锚+综述段+cited-by 池够对话 2 评点）

##### B6 Z-ODPLL（目标 1-2 篇，**天然稀**）
- 锚：OPLL `10.3390/photonics10121312`（union 2）
- **候选 2 篇**（carrier-sync-forward-citedby-summary.md §3 缓存，全 OA+S2 真 cited-by）：
  1. `10.1117/12.3041354` | Orbit determination using passive optical comm observations（2025）| 相关性低（光 Doppler 测轨非载波同步算法）| OA+S2
  2. `10.1109/acp66871.2025.11350439` | Rapid-Tuning ECL Wavelength Control for LEO-Ground Coherent Optical Comm（2025）| 相关性中（Doppler 频移预补偿 ECL 调谐 ±9.68~12.41 GHz）| OA+S2
- 入池判定：**天然稀 ≤2 篇即够**（不强凑 5，池子本就 2 篇且都偏 Doppler 频移线非 OPLL sin 鉴相器幅度衰落鲁棒性线——锚团队留白仍成立）

##### B7 Gardner TED（目标 1-2 篇，**天然稀·池子空**）
- 锚：ofc.2026.w2a.62（**本轮新落盘**，新拉 cited-by union 0）
- **候选 0 篇**——ofc.2026 是 OFC 2026 会议论文，发表时间极近，OpenAlex/S2 均未收录前向引用（cited-by = 0）。
- **降级**：对话 2 评 B7 时用 **backward refs**（B7 自己引的 Gardner TED 经典 + 多普勒估计相关）作补充池，不强凑前向 cited-by。
- 入池判定：**天然稀，cited-by 池为空**（索引滞后非漏检），对话 2 靠 B7 backward refs + Gardner TED 经典引文

##### B8 RL+GS 自相干自消除（目标 3-4 篇）
- 锚：jocn.468220（新拉 union 5）
- **候选 3 篇**（新拉，全 OA+S2 真引用非 S2 误关联）：
  1. `10.3390/photonics10050493` | Wavefront Distortion on Coherent Detection（2023）| **高**（相干检测+大气湍流，直击 B8 相干/湍流切入点）
  2. `10.1109/lcomm.2024.3511129` | Geometric Constellation Shaping for Wireless Optical Intensity（2024）| 中（GS 主题对齐，但 IM/DD 强度信道非自相干）
  3. `10.1364/jocn.503484` | DRL Cooperative FSO Elastic Splitter（2023）| 中（FSO+DRL 但聚焦功率分配非自相干）
- 入池判定：3 篇够（与 B9 联读共享池，B8 候选 1 与 B4 共享去重）

##### B9 虚拟载波自相干+DRE（目标 3-4 篇，与 B8 联读）
- 锚：jlt.2023.3270673（新拉 union 8）
- **候选 4 篇**（新拉，全 OA+S2 真引用）：
  1. `10.1117/1.apn.3.3.036007` | Beyond 200-Gb/s O-band IM/DD Joint LUT-Predistortion + **DRE**（2024）| **高**（DRE 是锚核心技术，但数据中心 IM/DD 非自相干，跨场景）
  2. `10.1109/lpt.2026.3655104` | Frequency-Temporal Enhanced Recovery Ultra-Low-Resolution ACO-OFDM OWC（2026）| 中（分辨率增强方向对齐，OWC OFDM 非自相干）
  3. `10.3390/s24248036` | Beyond-5G FSO Survey（2024）| 低（FSO 综述泛指）
  4. `10.1016/j.optlastec.2024.110917` | Mixed THz/FSO Relaying（2024）| 低（中继链路预算非同步）
- 入池判定：4 篇够（B8/B9 联读，无 DOI 重叠无需去重；唯一 S2-only 重复条目 R8 舍弃）

##### B10 16-QAM pilot-RLS（目标 2-3 篇）
- 锚：s11107-024-01019-2（新拉 union 1，锚极新）
- **候选 1 篇**（新拉，仅 1 条）：
  1. `10.1364/ao.581648` | Low-complexity carrier sync for **PS 64-QAM** based on kernel RLS + zero-averaging BPS（2026）| **高**（RLS 载波同步+高阶 QAM，kernel-RLS 直接承接 pilot-RLS 思路升级 PS-64QAM）| openalex 真引用
- 入池判定：1 篇（锚极新 cited-by 仅 1，但这条高度对口；D011 16-QAM 种子联读价值仍在）

##### B11 NDA-ML STO+CPE（目标 3-4 篇）
- 锚：LPT.2024.3523478（新拉 union 1，锚极新）
- **候选 1 篇**（新拉，仅 1 条）：
  1. `10.3390/s25164906` | Coverage Analysis 5G HSR System Beamwidth-Adaptive FSO（2025）| 中（含 FSO 但偏 HSR 覆盖分析非 STO+CPE 算法）| OA+S2 双源确认
- 入池判定：1 篇（锚极新 cited-by 仅 1，无更贴合 STO/CPE/FSO 候选；B11 评点靠锚全文+M-APSK/NDA ML 经典 Wu[11]/Hu[12]）

##### B12 频域 pilot 相位噪声（目标 2-3 篇）
- 锚：TCOMM.2022.3171809（新拉 union 9）
- **候选 3 篇**（新拉，锚理论性强候选多偏无线/光学相位估计）：
  1. `10.1109/COMST.2024.3443158` | Phase Noise in Wireless Communications Survey（2025 COMST c=9）| **高**（相位噪声估计权威综述，频域 pilot 是其中一节）| s2
  2. `10.1109/acp/ipoc63121.2024.10809580` | Simplified Coherent DSP Short-Reach with **Frequency Domain Pilot Tone**（2024）| **高**（直接用频域 pilot tone 做相干 DSP，切入点最接近）| openalex **需核验**（会议）
  3. `10.23919/oecc/psc62146.2025.11109607` | MAP Phase Recovery 256-QAM（2025 OECC/PSC）| 中（相位恢复+高阶 QAM 理论契合）| openalex **需核验**（会议）
- 入池判定：3 篇够

### 范围变更记录（2026-07-03 用户纠偏）

- **日期**：2026-07-03
- **触发**：用户原话"怎么才这么点？不是打算几十篇吗？我想还是全下下来之后再看比较好吧？不然很容易又偏了"
- **变更内容**：S002 原范围只备 cited-by 候选 DOI 池（步骤 1-3），**扩大为批量下 ~25 篇 cited-by 候选全文 + 转 md**（步骤 4）
- **原因**：用户准确识别 profile 第 7 次"急于推进"风险——只下几个锚就开始评容易偏，正确做法是先把池子里全文下完再开评点
- **scope boundary 影响**：仍在"备料不评点不判 Go/Kill"边界内（扩的是备料深度，不是评点动作），不违反"明确不含"

---

### 步骤 3：D 档星地光候选（v2 改动 2，H020 总表范围）

派子 agent **逐个扫 D2-D5 cited-by 缓存 JSON 标题**（不准凭印象，R004 标"主导"非"全部"）。

| D 档 | 锚 | 扫描条目数 | 星地光命中 |
|---|---|---|---|
| **D2** | TWC 2024 `10.1109/TWC.2024.3406952` | 57 条（45 含 satellite/LEO）| **全出界无星地光命中（已扫 57 条）**。所有 satellite 命中均为 RF/NTN/OTFS/LEO-RF（beamforming/信道预测/OTFS 帧/ISAC），无一涉及 FSO/星地光载波同步。**R004"全 RF 出界"判定成立。** |
| **D3** | Schmidl-Cox 1997 `10.1109/26.650240` | 150 条（8 含 sat/FSO）| **3 篇星地光命中**：①`10.1109/LPT.2025.3644328` OFDM-FSO Triple Autocorrelation（2026 PTL，即 D7，相关帧/载波同步）S2 需验 ②`10.1109/LPT.2024.3523478` NDA-ML M-APSK FSO（即 **B11 锚**，反向被引确认）③`10.1002/sat.1553` 综述（跨多 B 点）。其余 5 条 RF LEO/NTN 出界 |
| **D4** | Spalvieri[57] 85 + Martins[58] 6 | 91 条（Spalvieri 3 + Martins 1 含 sat/FSO）| **3 篇星地光命中**：①`10.1002/sat.1553`（双命中）②`10.1007/s11432-024-4415-7` DTAT-FSO 湍流免疫（2024，出界偏物理层调制非 pilot 同步）③`10.1109/WCSP.2017.8170879` Self-correction phase noise SC-FDE satellite（2017，相关 B12 但 SC-FDE 非 pilot 且早于 2022+ 窗，边缘）|
| **D5** | Kikuchi 2008 JLT `10.1109/jlt.2007.913589` | 120 条（16 含 sat/FSO）| **6 篇星地光命中**（去重后）：①`10.1038/s41377-023-01201-7` Tbit/s satellite feeder links coherent+full-AO（2023 Light Sci Appl，**星地光旗舰**相关 B 相干载波）OA+S2 ②`10.1364/ao.57.005095` 40GBaud intradyne GEO uplink atmospheric turbulence（2018 AO）OA ③`10.1364/ol.42.002173` Intradyne BPSK FSO GEO uplink（2017 OL）OA ④`10.1016/j.optcom.2021.126958` Sat-to-ground downlink aperture/mode diversity（2021）S2 需验 ⑤`10.1364/ao.434807` Inter-satellite laser-ranging intradyne coherent（2021 AO）OA ⑥`10.12783/dtcse/wcne2017/19815` Phase Offset Estimation Coherent FSO（2018，**最相关 B CPE**）S2 需验 |

**D 档汇总**：D2 全出界（R004 判定坐实）；D3/D4/D5 各有 3/3/6 篇星地光命中，最强公约候选 = `10.1002/sat.1553`（D3/D4/D5 三档同时命中，已是本专题 B1-B3 锚）。D5 星地光命中最多（6 篇，Kikuchi 2008 是相干光 CPE 经典被星地光后续引用），对话 4 literature_notes 并入时这些 D 档星地光候选进总表"看全貌"。

### 步骤 4：批量下 cited-by 候选全文（范围扩大，用户纠偏）

派 3 子 agent 按 publisher 并发分批（IEEE 9 / Optica 5 / 其他 ~11），主线 FR-26 独立 grep 核查落盘。**实际落盘 18 篇全文 + 3 篇仅摘要 + 5 篇付费墙（+B5 = 6 篇待用户手动下）**。

#### 4.1 全文成功（18 篇 ✅）

| # | DOI | 标题简 | publisher | content.md 行数 | 关联 B 点 |
|---|---|---|---|---|---|
| 1 | `10.1109/ICCWorkshops59551.2024.10615713` | DL Phase Noise Mitigation High-Order Mod | IEEE | 327 | B1（wireless backhaul 出界）|
| 2 | `10.1109/acp66871.2025.11350439` | Rapid-Tuning ECL Wavelength Control LEO-Ground | IEEE | 209 | B6（Doppler 频移预补偿）|
| 3 | `10.1109/lcomm.2024.3511129` | Geometric Constellation Shaping Wireless Optical Intensity | IEEE | 286 | B8（GS 主题，IM/DD 非自相干）|
| 4 | `10.1109/lpt.2026.3655104` | Freq-Temporal Enhanced Recovery ACO-OFDM OWC | IEEE | 160 | B9（分辨率增强，OWC 非自相干）|
| 5 | `10.1109/COMST.2024.3443158` | Phase Noise Wireless Communications Survey | IEEE COMST | 1288 | B12（权威综述，频域 pilot 一节）|
| 6 | `10.1109/LPT.2024.3523478` | NDA-ML STO+CPE M-APSK FSO (**B11 锚**) | IEEE PTL | 226 | B11 |
| 7 | `10.1109/TCOMM.2022.3171809` | In/Out-of-Band Freq Pilot Phase Noise (**B12 锚**) | IEEE TCOMM | 590 | B12 |
| 8 | `10.1109/jlt.2023.3270673` | Simplified Self-Coherent FSO + DRE (**B9 锚**) | IEEE JLT | 306 | B9 |
| 9 | `10.1109/26.650240` | Schmidl & Cox 1997 OFDM Sync（**D3 经典锚**）| IEEE TCOM | 2720 | D3 |
| 10 | `10.1364/oe.564097` | Fully utilized pilot-aided DSP state-pruning MLSD | Optica OE | 428 | B1（pilot 全利用，光纤互连非星地）|
| 11 | `10.1364/jocn.468220` | RL+GS self-canceling coherent detection (**B8 锚**) | Optica JOCN | 603 | B8 |
| 12 | `10.1007/s11107-024-01019-2` | 16QAM pilot-RLS carrier sync (**B10 锚**) | Springer | 318 | B10 |
| 13 | `10.1007/s11432-024-4415-7` | DTAT-FSO turbulence-immune | Springer Sci China | 306 | B4/D4（FSO 湍流，非载波同步算法）|
| 14 | `10.3390/photonics10050493` | Wavefront Distortion Coherent Detection | MDPI Photonics | 616 | B8（相干+大气湍流，直击切入点）|
| 15 | `10.3390/s24248036` | Beyond-5G FSO Survey | MDPI Sensors | 3364 | B9（FSO 综述泛指）|
| 16 | `10.3390/s25164906` | 5G HSR FSO Coverage | MDPI Sensors | 693 | B11（含 FSO，偏 HSR 覆盖非 STO+CPE）|
| 17 | `10.1038/s41377-023-01201-7` | Tbit/s satellite feeder coherent + full-AO | Nature LSA | 428 | D5（**星地光旗舰**）|

（注：#6-9 为前序轮次已落盘的锚/经典，本轮核查确认仍在；本轮真正新下的是 #1-5,10-17 共 13 篇）

#### 4.2 仅摘要（3 篇 ⚠️，Optica 订阅墙）

| DOI | 标题简 | 关联 B 点 | 后续处理 |
|---|---|---|---|
| `10.1364/jocn.503484` | DRL Cooperative FSO Elastic Splitter | B4/B8（FSO+DRL 但功率分配非自相干）| 摘要够评点（FSO 综合判断）|
| `10.1364/ao.581648` | PS 64-QAM KRLS + ZA-BPS carrier sync | **B10 高相关**（kernel-RLS 承接 pilot-RLS 升 PS-64QAM）| **建议用户手动下**（B10 评点高价值）|
| `10.1364/ao.57.005095` | 40GBaud intradyne GEO uplink turbulence | D5（星地光命中）| 摘要够 D 档判读 |

#### 4.3 付费墙未下（6 篇 ❌ 待用户手动下）

| DOI | 标题简 | publisher | 关联 | 失败原因 |
|---|---|---|---|---|
| `10.1117/1.apn.3.3.036007` | Beyond 200Gb/s O-band DRE | SPIE APN | B9（DRE 是锚核心技术）| **Gold OA 但 Imperva/Akamai 反爬**，浏览器手动免费下 |
| `10.23919/oecc/psc62146.2025.11109607` | MAP Phase Recovery 256-QAM | IEEE OECC | B12（相位恢复+高阶 QAM）| IEEE 订阅墙，需登录 |
| `10.12783/dtcse/wcne2017/19815` | Phase Offset Estimation Coherent FSO | DEStech 2017 | D5（**最相关 CPE**）| DEStech 登录墙 |
| `10.1117/12.3041354` | Orbit determination passive optical | SPIE | B6/D5 | SPIE 订阅/购买 |
| `10.1016/j.optlastec.2024.110917` | Mixed THz/FSO Relaying | Elsevier OLT | D5（FSO 中继非同步）| ScienceDirect 403 |
| `10.1016/j.optcom.2024.130981` | **B5 短时谱粗频偏** | Elsevier | **B5 锚** | 早先穷尽 11 源失败 |

#### 4.4 用户手动下优先级建议（6 篇里按评点价值排序）

1. **B5** `10.1016/j.optcom.2024.130981`——B5 切入点锚，有 VPN 就下（青岛大学 Jiamin Fan 等）
2. **ao.581648** `10.1364/ao.581648`——B10 高相关（PS-64QAM KRLS 承接 pilot-RLS），Optica 订阅
3. **apn.3.3.036007** `10.1117/1.apn.3.3.036007`——B9 DRE 核心技术，**Gold OA 浏览器手动免费下**（最该下）
4. 其余 3 篇（OECC/DEStech/SPIE）信号弱或边缘相关，可不下

## 决策引用

- **无新建 D###**（本对话是备料，不评点不判 Go/Kill，符合 D018 中性提取）
- 引用既有：D017（D015 v2 步骤 4 每点 ≤5 篇验证）/ D018（中性提取不判 Go/Kill + ≤5 放宽单 subagent 不看太多）/ D006（红线保留）/ D005（务实路线）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（补下载 + cited-by 池 + D 挑星地光 + 批量下全文都是 S001 v2"对话 0"备料动作；扩范围只增备料深度不进评点，见范围变更记录）
- 守 3 步上限：本轮因用户纠偏扩范围超 3 步（①报到 ②补锚下载 ③cited-by 池+D 挑 ④批量下全文 ⑤汇总），**用户明确要求"下完再评"触发扩范围**，已记范围变更记录
- 守子 agent ≤15 分钟：3 批 7 子 agent（2+2+3 并发），全 PASS
- **守 D018 中性提取**：本轮不评点不写笔记不判 Go/Kill，只备料（profile 第 7 次"急于推进"防线——本轮严守"备料就是备料"）

## 已知债务（穷尽后仍失败的）

| 债务 | 试过的源 | 影响 | 后续处理 |
|---|---|---|---|
| **B5 Elsevier paywall**（optcom.2024.130981）| 穷尽 11 源 | B5 切入点锚全文缺 | **待用户手动下**（机构 VPN/邮件作者青岛大学 Jiamin Fan）|
| **ao.581648 Optica 订阅墙** | tools/download + Playwright JS 挑战（viewmedia 触发 Radware+hcaptcha）| B10 高相关候选（PS-64QAM KRLS 承接 pilot-RLS）缺全文 | **待用户手动下**（Optica 订阅，B10 评点高价值）|
| **apn.3.3.036007 SPIE 反爬** | Gold OA 但 Imperva/Akamai bot manager | B9 DRE 核心技术全文缺 | **待用户手动下**（Gold OA 浏览器手动免费下，最该下）|
| **oecc/psc62146.2025 IEEE 订阅** | IEEE Xplore 需登录 | B12 相位恢复+高阶 QAM 候选 | 待用户手动下（IEEE 订阅，信号弱可不下）|
| **dtcse/wcne2017/19815 DEStech 登录** | dpi-journals 登录 HTML | D5 最相关 CPE 候选 | 待用户手动下（DEStech 登录，2017 早年可不下）|
| **12.3041354 SPIE 订阅** | 无 OA link | B6/D5 候选 | 待用户手动下（SPIE 订阅/购买，信号弱可不下）|
| **optlastec.2024.110917 Elsevier** | ScienceDirect 403 | D5 FSO 中继非同步 | 待用户手动下（边缘相关可不下）|
| **jocn.503484 / ao.57.005095 仅摘要** | Optica 订阅墙 | B4/B8/D5 候选 | 摘要够评点，全文非必需 |
| **[79] Matsuda SPIE 仅摘要**（10.1117/12.2544050）| 穷尽 7 源 | B2 均衡器冻结 FOE 专项全文 | **摘要已坐实 sat.1553 L582 机制**（对话 1 评 B2 够用）|
| **B10/B11/B12 图表数值 fast md 占位符** | 未处理（可后置）| 量化段待 standard MinerU 重转 | 对话 2-3 涉及前用 `tools/convert --quality standard` 重转 |

## 后续

### 交对话 1（B1/B2/B3 综述背书 + B4/B6 补 cited-by 验证表）

**对话 1 必读**：
1. 本 S002（cited-by 候选池 + 下载状态 + D 星地光候选）
2. topic-index 不变量 9 条 + S001 v2 规划
3. H001（本轮 handoff，下一步具体任务）
4. gw-read.md（14 字段+7 项结构化提取，对话 1 写笔记标准）
5. 原专题 H020（总表 + 排优先级辅助信息）

**对话 1 任务**（S001 v2 改动 1 后的拆分）：
- B1/B2/B3 综述背书 3 点每点精读 ≤5 篇验证（cited-by 池已在 S002 §2.2 备齐）
- B4/B6 已有扎实笔记，补 cited-by 验证表不重读全文（池已在 S002 §2.2 备齐）
- 复用 sat.1553 旧笔记但删 L70 撞 D006 段（原专题 S028 已警告）
- **本轮下载收获**：[58] Martins 全文 + [60] Leven 全文 + [79] Matsuda 摘要 → B1/B2 增量核验素材备齐（B5 仍缺全文，对话 2 处理）

### 关键提醒给后续对话

1. **B5 全文失败**：对话 2 评 B5 短时谱粗频偏时标"待全文"，靠 sat.1553 综述段 + [60]Leven + Paillier 池评点，不强行脑补
2. **[79] Matsuda 仅摘要**：对话 1 评 B2 时摘要已坐实 FO 估计器冻结机制（核心机制原文有），0.6dB 增量信号够用；正文图表如必须看走馆际互借
3. **B7 cited-by 池为空**（OFC 2026 索引滞后）：对话 2 评 B7 用 backward refs（B7 引的 Gardner TED 经典 + 多普勒估计）补池，不强凑前向 cited-by
4. **B6 cited-by 仅 2 篇且偏 Doppler 频移线**：锚团队留白（作者 2025 转 Z-ODPLL）仍成立，对话 1 评 B6 时这是中性观察非 Go/Kill
5. **D2 全 RF 出界已坐实**（扫 57 条无星地光），D3/D4/D5 各有 3/3/6 篇星地光命中进总表（对话 4 literature_notes 并入时标）
