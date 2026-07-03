# [S003] 对话 1：补下 v1 量级缺口 + B1/B2/B3 评点

> 2026-07-03 | 精读沉淀补强·对话 1（评点阶段起步）| 状态：B1/B2/B3 评点完成，交对话 2 B4-B7
> 来源：S001 v2 规划"对话 1"+ H001（含步骤 0 补下）

## 目标

执行 H001 指示的对话 1 两件事：①**步骤 0** 补下 v1 量级缺口 13 篇（IEEE 5 blit + Optica/其他 6+2）②**步骤 1** B1/B2/B3 三点评点（gw-read 14 字段+7 项含 M-C-A 提取）。守 3 步上限（步骤 0 已用 1 步 + 步骤 1 评点 + 步骤 2 写 S003/H002）。

## 记录

### 报到验证（Trigger 1+5）

- **Trigger 1（Session Start）**：topic-index 不变量 9 条确认；active topic conflicts = none；depends_on（2026-06-20-problem-driven-redirection）已满足；profile 最近纠偏 2026-07-02 S030"急于推进"第 7 次表现；inflation check 本专题 2 S 文件远未到阈值。
- **Trigger 5（Handoff H001 接收）**：FR-26 主线独立 grep 核查 4 组磁盘证据全 PASS——
  - ① 5 篇锚磁盘状态：ofc.2026.w2a.62/osac.438524/lpt.2007.891893 有 PDF+content.md；1117_12.2544050 仅 content.md（摘要）；optcom.2024.130981 仅 metadata.json（确认失败）
  - ② cited-by 池 36 JSON + carrier-sync-forward-citedby-summary.md 真实存在于 search-archive/2026-07-02/
  - ③ H001 标"付费墙未下 6 篇"目录壳核查：apn.3.3.036007/oecc-psc/dtcse/12.3041354/optlastec 只有 metadata.json 无 PDF/content.md，确认失败状态
  - ④ 仅摘要 3 篇：jocn.503484/ao.581648/ao.57.005095 有 content.md（摘要）无 PDF
- **H001 偏差发现**：H001 说"B1/B4/B6 已有扎实笔记"，**实际 papers/_read_notes/ 已有 31 篇笔记**，含 B3 三候选（jphot.2023.3265847/LCOMM.2026.3651445/oe.520452）旧 A3 视角笔记 + sat.1553 73 行旧笔记 + Paillier/jlt.2020.3003561 旧笔记。B3 评点素材比 H001 估计的更齐。

### 步骤 0：补下 v1 量级缺口（H001 步骤 0）

派 2 子 agent 并发（IEEE 5 blit 批 + Optica/其他 6+2 批），主线 FR-26 独立 grep 核查落盘。

#### 0.1 下载结果（8 成功 + 5 付费墙失败）

| # | DOI | 标题简 | publisher | 状态 | PDF 字节 | md 行 | 关联 |
|---|---|---|---|---|---|---|---|
| 1 | `10.1109/tcom.1986.1096561` | Gardner TED 1986 原文 | IEEE TCOM 经典 | ⚠️转换差 | 686K | 14 | B7 理论根基（扫描 PDF 正文不可检索）|
| 2 | `10.1109/jlt.2012.2204037` | Pilot-Carrier Coherent LEO-to-Ground OPLL | IEEE JLT | ✅ | 1.58M | 750 | B7/B6 星地光 |
| 3 | `10.1109/access.2023.3287501` | Modulation & SP for LEO-LEO OISL | IEEE Access | ✅ | 2.25M | 572 | B7 星间光 |
| 4 | `10.1109/mwp54208.2022.9997784` | All-Digital OPLL satellite under Turbulence | IEEE MWP | ✅ | 1.71M | 148 | B6 星地光+OPLL |
| 5 | `10.1109/50.202807` | Carrier sync homodyne/heterodyne QPSK (1992) | JLT/OSA 经典 | ⚠️转换差 | 1.18M | 26 | B6 经典锚（Stanford EE OA 镜像，扫描 PDF）|
| 6 | `10.1587/elex.18.20210078` | Z-domain modeling homodyne digital OPLL | IEICE Japan | ✅ | 327K | 350 | **B6 Z-ODPLL 根基** |
| 7 | `10.3788/col202018.090602` | Digital-analog hybrid OPLL QPSK | Chinese Opt Lett | ✅ | 935K | 283 | B6 OPLL |
| 8 | `10.1364/oe.16.000818` | Optical Phase Locking techniques overview 2008 | Optica OE | ✅ | 383K | 322 | B6 OPLL 综述 |
| — | `10.1364/ol.42.002173` | Intradyne BPSK FSO GEO uplink | Optica OL | ❌付费墙 | 0 | 0 | B6/D5（OL 订阅+Radware CAPTCHA）|
| — | `10.1364/ao.57.007915` | Homodyne coherent intersatellite | Optica AO | ❌付费墙 | 0 | 0 | B6 星间（AO 订阅）|
| — | `10.1109/tcom.1974.1092337` | Noisy Phase Reference 1974 | IEEE TCOM 经典 | ❌付费墙 | 0 | 0 | B6 经典锚（无 OA）|
| — | `10.1364/ao.434807` | Inter-satellite laser-ranging intradyne | Optica AO | ❌付费墙 | 0 | 0 | D5 星间（AO 订阅）|
| — | `10.1109/LPT.2025.3644328` | OFDM-FSO Triple Autocorrelation (D7) | IEEE PTL | ❌付费墙 | 0 | 0 | D3/D7（Unpaywall is_oa=False）|

#### 0.2 关键事实修正

- **子 agent 1 报告**："Optica JS 挑战分两类：(a) 真 OA（OE Vol.16 2008）checkjs.cfm 过后 directpdfaccess 直链可抓；(b) 订阅论文（OL/AO 近年）同端点返 HTML 登录页或 Radware CAPTCHA"——**结论：OSAC 先例的成功是因为该篇本身 OA，而非 Playwright 能破订阅墙**。本轮 OL/AO 3 篇失败归因于此。
- **`tools/download --doi` 全 5 篇 IEEE 老/新论文 all_failed**：IEEE 订阅墙内，Unpaywall/OA 链路无命中。校园网机构认证（北京理工大学 IP）+ proxy `127.0.0.1:7897` 走通，blit IEEE Playwright 抓取 4/5 成功。
- **`10.1109/50.202807`（1992 Kazovsky）IEEE 标题检索混淆**：IEEE Xplore 返回 2008 年 Khaddaj Mallat 不匹配，子 agent 1 经 Web 搜索定位到 Stanford EE 官方作者 OA 镜像 `ee.stanford.edu/~jmk/pubs/QPSK.JLT.92.pdf`。
- **环境偏差**：AGENTS.md 声明的 `~/.venvs/torch/bin/python` 在本机不存在，tools/download 与 convert 实际 fallback 到 scoop python311（pymupdf4llm 可用）。未影响任务。

#### 0.3 当前全文盘点（v1 量级达成情况）

S002 后 ~28 篇 + 本轮新增 8 篇 = **~36 篇全文 + 3 篇仅摘要 = 39 篇**。距 v1 量级 40-50 下沿差 1-11 篇。**加上用户手动下的 6 篇付费墙就 45 篇**，够本轮+后续评点用。

**主线判断**：本轮不再扩补料（再扩就过度，profile 第 7 次"急于推进"防线）。剩余 v1 缺口交对话 2/3 评点过程中按需补（如 B4/B5 Paillier 池候选、B6/B7 评点时按需）。

#### 0.4 Paillier/Spalvieri 池主线筛选（不派子 agent）

主线直接读 JSON 筛 B1/B4/B5 候选：
- **Spalvieri 池 85 条**筛 2022+星地光/载波同步 → 12 条（除 S002 §2.2 B1 已列 3 条，新增 9 条，重点：jlt.2024.3416383 EEPN / JLT.2025.3535548 Receiver Laser Phase Noise / OFC49934.2023.10116513 OFC2023 CPR——多数光纤长距出界）
- **Paillier 池 43 条**全列 → **B5（optcom.2024.130981）确认在 Paillier cited-by 池里**（B5 切入点论文反向引用 Paillier baseline 关系坐实）。新增关注：TWC.2026.3659523 Semantic FSO Turbulence-Resilient / JLT.2025.3578005 Self-Adaptive All-Optical Feedback FSO / **jlt.2023.3281082 Digitally Mitigating Doppler Shift Coherent FSO LEO（B5/B6 高相关）** / jlt.2022.3164736 Coherent FSO 综述

### 步骤 1：B1/B2/B3 评点（H001 步骤 1，3 份增量笔记）

派 2 子 agent 并发（B1+B2 合并 + B3 单独），主线 FR-26 独立 grep 核查产出。

#### 1.1 sat.1553 L70 D006 复核（H001 提示项）

**H001 原话**："复用 sat.1553 旧笔记但删 L70 撞 D006 段"。

**复核结论**：**L70 确实撞 D006**（不是 H001 误判）。L70 原文"在综述的'载波恢复'模块里新增一个'湍流相位感知'子模块，把湍流 piston 相位作为相位估计的先验/扰动"= 同一物理假设（"湍流相位主动纳入同步能带来增益"）的第三种数学工具（前馈 Bayesian 先验），不构成 D006 要求的"全新机制"。机制上的"前馈 pilot vs 闭环 H(z)"差别不改变物理假设相同。

**动作**：**不删原文，加注**（D018 中性提取原则——撞线只标不砍留归档）。已在 L70 后追加"⚠ D006 红线标注（2026-07-03 复核，撞 D006）"段，引用 D006 决策原文 L328/L341，注明方向(2)/(3) 需独立复核。

#### 1.2 B1 自适应 pilot 窗口（2 个 Q# 候选）

笔记：`papers/_read_notes/_B1-pilot-window-increment.md`（73 行）
读了：sat.1553 L420-559（含 L440 open problem）+ [58] Martins osac.438524 全文 430 行 + [60] Leven lpt.2007.891893 全文 179 行

| Q# | M-C-A 浓缩 | D006 | D005 | 备注 |
|---|---|---|---|---|
| **B1-Q1** 自适应 phase-estimation window N | M=sat.1553 固定窗 VV/pilot + [60] 最优 N∝SNR 理论；C=上行强湍 σp²=0.25 SNR 波动；A=sat.1553 固定 N 单 SNR 点评测 + L440 自报"动态调整 gain 未量化" | **不撞** | **倾向够格但有风险**（sat.1553 pilot 场景4 比 VV+diff +1dB，自适应 N 增量待 MVE）| window-N 有 [60] 理论锚背书 |
| **B1-Q2** 自适应 pilot rate | M=sat.1553 固定 pilot rate + [58] 静态 pilot-rate×linewidth 优化；C=LEO 过顶 SNR 慢包络；A=[58] 静态优化未建模 SNR 动态 | **不撞** | **风险偏高倾向不够格**（sat.1553 L440 自承"same pilot rate performs similarly"直接负面证据，类似 D008/4B 平缓死法）| 0.5dB 阈值 |

**关键发现**：sat.1553 L440"same pilot rate performs similarly"是双刃证据；[58] 是地面光纤场景不能直接搬到 OSL；两条路线风险不对称（B1-Q1 有 [60] 理论锚背书，B1-Q2 有自承负面证据）。

#### 1.3 B2 deep fade 冻结（2 个 Q# 候选）

笔记：`papers/_read_notes/_B2-deep-fade-freeze-increment.md`（76 行）
读了：sat.1553 L558/L582 引 [79] 段 + [79] Matsuda 1117_12.2544050 摘要 + Paillier 2020 JLT 旧笔记

| Q# | M-C-A 浓缩 | D006 | D005 | 备注 |
|---|---|---|---|---|
| **B2-Q1** FOE freeze 自适应阈值/多估计器协同 | M=[79] 静态功率阈值 gate FOE；C=上行强湍 deep fade；A=sat.1553 L582 自承"完全冻结在 SOP 漂移大时丢跟踪" | **不撞**（估计器 gating ≠ 相位建模）| **≥1dB 存疑待全文核验**（**陷阱已规避**：0.6dB 是 [79] 相对无 freeze baseline，非 B2-Q1 相对 [79] 增量）| B2 锚三篇全星地在范围内 |
| **B2-Q2** FOE freeze + pilot-aided fallback 双模切换 | M=[79] blind freeze；C=fade 恢复期需快速重捕获；A=blind 恢复收敛慢，sat.1553 L440 pilot 在 fade +1dB | **不撞** | **倾向够格但增量未量化** | sat.1553 L582 作者亲口指出 [79] 冻结局限 = B2 改进空间 |

**关键发现**：陷阱已规避——0.6dB 是 [79] 相对无 freeze 的增益**不是** B2 切入点增量（标注"待全文核验"）；D005 主要风险是 0.6dB 偏低（vs 同门 2-4dB），增量叠加后是否够格需 MVE。

#### 1.4 B3 子系统协同（3 个 Q# 候选）

笔记：`papers/_read_notes/_B3-subsystem-coordination-increment.md`（101 行）
读了：sat.1553 L788/L790 + 张思齐学位论文全文 1244 行 + LCOMM.2026.3651445 + jphot.2023.3265847 + oe.520452（旧笔记+content 抽样）

**张思齐学位论文关键发现**：
- 架构 = **分级 + 模块内联合**（非端到端）：第三章 FOE↔CPE 数据复用（四次方信号复用至 CPE），第四章 FS↔FOE 共享一套短符号块 TS
- baseline + 量化：vs QPSK 分圈 +0.67/+0.76/+0.71 dB（B2B/弱湍/强湍）；JCR 复杂度仅 4th-FFT 13.8%、QPSK Partitioning 47.6%，NMSE 10⁻¹⁰/10⁻⁹；FS+FOE 联合复杂度 17%，NMSE 10⁻⁷
- 自陈 §5.2 open problem：协同停在载波恢复模块内，**未跨定时恢复/自适应均衡**；频偏超范围精度降；未做硬件实现 → **B3 相对张思齐的增量空间 = 跨子系统协同（sat.1553 L790 命题）**

| Q# | M-C-A 浓缩 | D006 | D005 | 范围 |
|---|---|---|---|---|
| **B3-Q1** LCOMM B3 视角重抽 | 一套 FPT 跨 FOE+CPE+RSOP，CPE/解复用解耦，+0.9 dB Q / RMSE 4.47° | **不撞** | **够格** | **out（光纤 DSCM，待迁移论证）** |
| **B3-Q2** jphot+oe 合并 | 一套 TS 同时 FS+两段 FOE+MRC，复杂度 17%~25%，强湍 4 支路 +2~3 dB | **不撞** | **够格** | **in（分集增益不可全迁）** |
| **B3-Q3** sat.1553 L790 + 张思齐空白 | 定时+均衡+载波恢复跨子系统共享 pilot + 依赖解耦联合协同（无工程实例，open problem 级）| **不撞**（边界：若具体化为环路 TF 联合建模则撞，只标不砍）| **待定量锚**（借 +0.9~3 dB / +1 dB 量级参考）| **in** |

**关键发现（意外）**：LCOMM.2026.3651445 原按 A3（pilot CPE）方向读，**B3 视角下其核心增量恰是"CPE 与偏振解复用解耦 + 一套 FPT 跨 FOE/CPE/RSOP 三子模块"，是 sat.1553 L790 "same pilot symbols" 命题的最直接工程实例**——意外高贴合（但场景是光纤 DSCM 非星地，标 out）。jphot/oe 的 FS+FOE 协同较窄（未跨均衡），B3 增量空间小于 LCOMM。

#### 1.5 B1/B2/B3 评点小结

- **Q# 候选总数 7 个**（B1×2 + B2×2 + B3×3），全部标注 D006/D005/范围
- **撞 D006：0 个**（sat.1553 L70 旧扩展方向撞，已加注归档；7 个 Q# 本身不撞）
- **D005 倾向够格：4 个**（B1-Q1 / B2-Q2 / B3-Q1 / B3-Q2）
- **D005 风险偏高/不够格：3 个**（B1-Q2 平缓负面证据 / B2-Q1 0.6dB 偏低待全文 / B3-Q3 open problem 级无定量锚）
- **范围 out：1 个**（B3-Q1 光纤 DSCM 待迁移论证）
- **本轮不判 Go/Kill**（守 D018 中性提取）——Q# 候选留总表阶段用户排完优先级后对前几名做

## 决策引用

- **无新建 D###**（本对话是评点 + 笔记增量，Q# 候选留总表阶段判 Go/Kill，符合 D018 中性提取）
- 引用既有：D017（D015 v2 步骤 4 每点 ≤5 篇验证）/ D018（中性提取不判 Go/Kill + ≤5 放宽单 subagent 不看太多）/ D006（红线保留，sat.1553 L70 加注）/ D005（务实路线，Q# 标够格判定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（补下载 + B1/B2/B3 评点 + 笔记增量都是 S001 v2"对话 1"动作；Q# 候选只提取不判 Go/Kill）
- 守 3 步上限：**本轮 3 步用满**（①步骤 0 补下 ②步骤 1 B1/B2/B3 评点 ③写 S003+H002）。B4-B7 交对话 2
- 守子 agent ≤15 分钟：4 子 agent（2 下载 + 2 评点），全 PASS
- **守 D018 中性提取**：本轮 7 个 Q# 候选只标 D006/D005/范围，不判 Go/Kill（profile 第 7 次"急于推进"防线）

## 后续

### 交对话 2（B4/B5/B6/B7 评点 + B4/B6 cited-by 验证表）

**对话 2 必读**：
1. 本 S003（补下状态 + B1/B2/B3 评点 + Q# 候选 7 个）
2. S002（cited-by 池 + D 星地光候选 + 下载状态总表）
3. topic-index 不变量 9 条 + S001 v2 规划
4. H002（本轮 handoff，下一步具体任务）
5. gw-read.md（14 字段+7 项结构化提取标准）
6. 原专题 H020（总表 + 排优先级辅助信息）

**对话 2 任务**（S001 v2 改动 1 后的拆分）：
- **B4 双反馈环**：Paillier cited-by 43 池筛星地光候选（主线已在 S003 §0.4 列新增候选），补 cited-by 验证表（已有 Paillier 主线扎实笔记 + sat.1553 旧笔记，增量补 B4 视角 M-C-A）
- **B5 短时谱粗频偏**：B5 全文失败（穷尽 11 源），靠 sat.1553 L558/L582 + [60]Leven + Paillier 池评点；标"待全文"
- **B6 Z-ODPLL**：本轮新下 5 篇 backward refs（Gardner 1986/Pilot-Carrier LEO 2012/OISL 2023/MWP OPLL 2022/Kazovsky 1992 + Z-domain IEICE + col202018 + OE 2008），补 cited-by 验证表（B6 已有 ofc.2026.w2a.62 + photonics10121312 旧笔记，本轮素材大补）
- **B7 Gardner TED**：ofc.2026.w2a.62 backward 5 篇（含 Gardner TED 1986 原文）+ B7 锚笔记已有，补 backward refs 验证表
- 主线 grep 核查 + 复用旧笔记删/标撞 D006 段

### 关键提醒给对话 2

1. **B5 全文失败不脑补**：评 B5 时标"待全文"，靠 sat.1553 综述段 + [60]Leven + Paillier 池 + S003 §0.4 新筛的 jlt.2023.3281082（Digitally Mitigating Doppler Shift）做评点
2. **B6 素材大补**：本轮新下 5 篇 backward refs + 2 篇 OPLL 经典（IEICE Z-domain / col202018 / OE 2008 综述），对话 2 B6 评点资料最齐
3. **B3-Q1 意外发现**：LCOMM.2026.3651445 在 B3 视角下高贴合 sat.1553 L790（一套 FPT 跨三子模块），但场景是光纤 DSCM——对话 4 literature_notes 并入时这个"跨场景迁移论证"可能成为 B3-Q1 的关键风险点
4. **v1 量级达成判断**：当前 39 篇全文/摘要，加用户手动下 6 篇付费墙 = 45 篇，落在 v1 量级 40-50 区间。**对话 2/3 不必再扩补料**，按需补 B4/B5 Paillier 池候选即可
5. **用户手动下优先级仍有效**（S002 §4.4）：①B5 optcom.2024.130981（VPN）②ao.581648（B10 高相关）③apn.3.3.036007（Gold OA 免费下，B9 DRE）
