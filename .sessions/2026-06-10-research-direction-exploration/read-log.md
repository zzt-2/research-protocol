# 探索期精读日志（read-log）

> 本文件记录探索期（无具体 project 锚定时）的精读论文去向。
> 每行一篇，7 字段：`paper_id | 源文件路径 | 笔记路径 | 首读日期 | 重读次数 | 用于方向 | alt_ids`
> paper_id = `papers/{type}/{id}/` 的 `{id}` 字面值（doi 转义 / arxiv 去版本号 / manual slug）
> 与项目级 `read-log.md`（在 `projects/{name}/` 下）并列：项目锚定后，探索期条目可迁入对应项目。
> 本文件为无编号辅助文件，与 `topic-index.md` / `decisions.md` / `voice.md` 同构，不进 S/R/H/D/V 编号体系。

| paper_id | 源文件路径 | 笔记路径 | 首读日期 | 重读次数 | 用于方向 | alt_ids |
|----------|-----------|---------|---------|---------|---------|---------|
| 10.3390_photonics10080914 | papers/doi/10.3390_photonics10080914/content.md | （笔记已删） | 2026-06-15 | 1 | dry-run 试运行；⚠️title↔content 错配案例（index 标 OPLL，content 实为石墨烯纳米二聚体，grep 实证 0/71 命中）；笔记已删，本条作 read-traceability V001 错配案例留存 | — |
| 10.3390_aerospace12100869 | papers/doi/10.3390_aerospace12100869/content.md | papers/_read_notes/10.3390_aerospace12100869.md | 2026-06-16 | 1 | E1 端到端仿真（留选）。CCSDS O3K+OU/AR1 信道。**E 三检验过 0 条=常识重做**（纯 benchmark 无方法创新，论文自承不提新算法） | — |
| 10.1364_ol.596189 | papers/doi/10.1364_ol.596189/content.md | papers/_read_notes/10.1364_ol.596189.md | 2026-06-16 | 1 | A3 帧导频振动检测（留选）。**⚠️降级精读**：content.md 为 Optica 付费墙 abstract 页，无正文；title_verify match 1.0 但正文不可读（read-traceability 新 case）。E 三检验证据不足，待补全文 | — |
| 10.1364_oe.555656 | papers/doi/10.1364_oe.555656/content.md | papers/_read_notes/10.1364_oe.555656.md | 2026-06-16 | 1 | E1 阵列检测器（留选）。非 Kolmogorov 分段谱+等效 Rytov 非等距屏。**E 三检验过 1.5 条=勉强偏真工作**（信道建模有料，评估端偏工程） | — |
| 10.1038_s41598-026-40704-2 | papers/doi/10.1038_s41598-026-40704-2/content.md | papers/_read_notes/10.1038_s41598-026-40704-2.md | 2026-06-16 | 1 | E1 OAM 结构光（留选）。DCNN 预测+DNFIS 均衡双核。**E 三检验过 2 条=真工作**（仅仿真+Article in Press 未定稿，baseline 偏老） | — |
| 10.1109_LCOMM.2026.3651445 | papers/doi/10.1109_LCOMM.2026.3651445/content.md | papers/_read_notes/10.1109_LCOMM.2026.3651445.md | 2026-06-16 | 1 | A3 频域导频音相位恢复（留选）。四 FPT 功率谱合并解耦 CPE 与 RSOP。**E 三检验过 2 条=真工作**（限定光纤 DSCM 场景，无湍流） | arnumber:11333291 |
| 10.1109_LPT.2025.3582338 | papers/doi/10.1109_LPT.2025.3582338/content.md | （待精读） | — | 0 | A2 ANN/RNN 载波恢复（存疑）；ANN 透明载波相位恢复。2026-06-16 blit 下载，match 0.857 | arnumber:11048536 |
| 10.1109_ACCESS.2025.3535789 | papers/doi/10.1109_ACCESS.2025.3535789/content.md | （待精读） | — | 0 | C2 双偏振（存疑）；DP 自相干 FSO+大气湍流。2026-06-16 blit 下载，title_verify 误判 mismatch（作者行误提），人工核验 match | arnumber:10856148 |
| 10.1109_JLT.2025.3533422 | papers/doi/10.1109_JLT.2025.3533422/content.md | （待精读） | — | 0 | C2 双偏振（存疑）；DP 光学 Costas 环 DSP-Free homodyne。2026-06-16 blit 下载，match 1.0 | arnumber:10852313 |
| 10.1109_LPT.2025.3647750 | papers/doi/10.1109_LPT.2025.3647750/content.md | （待精读） | — | 0 | D2 PS+RCM（存疑）；概率整形+残余载波调制 FSO 湍流信道。2026-06-16 blit 下载，match 1.0 | arnumber:11313238 |
| 10.1109_ICSOS66026.2025.11443174 | papers/doi/10.1109_ICSOS66026.2025.11443174/content.md | papers/_read_notes/10.1109_ICSOS66026.2025.11443174.md | 2026-06-16 | 1 | B1 ODPLL Z变换（留选）。Z 域 ODPLL 高多普勒建模。**E 三检验过 1 条=勉强>常识重做**（Z 变换本身工程工具；论文显式不建模湍流，line 317/357） | arnumber:11443174 |
| 10.3390_photonics10121312 | papers/doi/10.3390_photonics10121312/content.md | papers/_read_notes/10.3390_photonics10121312.md | 2026-06-16 | 1 | B1 gap 钥匙（ISAE-Supaero 同组前作）。全数字 OPLL+atan2 鉴相器，建模湍流但仅幅度 scintillation 衰落级。**E 三检验过 3/3**。B1 gap 验证：环路传递函数无湍流相位项，多普勒未建模 | — |
| 10.1109_icsos45490.2019.8978983 | papers/doi/10.1109_icsos45490.2019.8978983/content.md | papers/_read_notes/10.1109_icsos45490.2019.8978983.md | 2026-06-16 | 1 | B1 gap 验证（AO+DPLL 分治范本）。Paillier 星地相干，AO 光域管湍流+DPLL 数字域管多普勒残频(30~300MHz)。**E 三检验过 3/3**。B1 gap 强证据：环路假设恒幅无湍流相位，推给 companion paper | — |
| 10.1002_sat.1553 | papers/doi/10.1002_sat.1553/content.md | papers/_read_notes/10.1002_sat.1553.md | 2026-06-16 | 1 | B1 综述定位（2025 最新 OSL DSP 综述，DLR）。4 场景算法地图，**DSP 流水线无湍流相位模块**，多普勒=独立 CFO 模块。**E 三检验过 3/3**。B1 gap 综述级强证据 | — |
| 10.1364_oe.520452 | papers/doi/10.1364_oe.520452/content.md | papers/_read_notes/10.1364_oe.520452.md | 2026-06-16 | 1 | A3 场景迁移（BUPT Wang 组）。PRBS+循环QPSK 帧同步+两段FOE，相位屏湍流(强/弱)。**E 三检验过 3/3**。迁移 gap：缓变假设/deep fade/分集依赖/频偏范围 | — |
| 10.1109_jphot.2023.3265847 | papers/doi/10.1109_jphot.2023.3265847/content.md | papers/_read_notes/10.1109_jphot.2023.3265847.md | 2026-06-16 | 1 | A3 场景迁移（BUPT Wang 组，oe.520452 前序）。FSTS 一套 TS 做 FS+两段FOE，傅里叶相位屏湍流。**E 三检验过 3/3**。迁移 gap 同上 | — |
| 10.1016_j.optcom.2023.129312 | papers/doi/10.1016_j.optcom.2023.129312/content.md | （未精读） | — | 0 | A3 迁移+B1 旁证（Liu 双反馈环 OPLL+Viterbi 星地载波恢复）。⚠️**manual_required**：Elsevier ScienceDirect 付费墙，firecrawl 只抓 abstract 页，blit 不支持 Elsevier，无 arXiv 预印本。待用户手动获取 | — |
| arxiv:2005.02129 | papers/arxiv/2005.02129/content.md | （精读正文，S005 Agent-N1，未单独建 read_notes） | 2026-06-16 续 4 | 1 | **N1 锚点纠正后的合法化身（D005）**。Elzanaty & Alouini 2020，PCS + Gamma-Gamma 湍流。**IM/DD M-PAM（非相干）**，blind 模式（CSI only at RX，按湍流 CDF outage 分位点离线设计 MB 分布）= 不跨 RTT = TL-03 安全。gain（IM/DD, blind）：1 dB (R=1.5, σ_R=0.5) / 2 dB (R=0.5) / 2.5 dB (CSI-aware, GG)。**相干 FSO gain 仍缺**（门控）。替代 R006 误判的 cite=81 | — |
| 10.1109/JLT.2020.3012737 | （未下载，closed access 无 OA） | — | — | 0 | ⚠️**cite=81 是 R006 误判（D005 纠正）**。Guiomar et al. 2020 JLT。Semantic Scholar abstract 直证踩 TL-03（moving average channel estimator 驱动帧级自适应=跨 RTT）+ 场景偏离（55m fiber-FSO + rain memory，非 GG deep fade）。属 R005 已砍"2.1 链路自适应 TL-03 陷阱"族，**不是 N1**。不下载 | — |

> **精读闭环说明（2026-06-16）**：本轮精读留选 3 方向 6 篇（E1×3 + A3×2 + B1×1），每篇产出 `papers/_read_notes/{paper_id}.md`。结论：**无方向有现成论文同时覆盖"星地+湍流+方法创新"**。过 E 三检验 ≥2 条的仅 s41598（E1）和 LCOMM（A3），但前者偏地面段+未定稿，后者纯光纤无湍流。B1 论文含金量 1/3 但显式承认湍流 gap（line 357），gap-driven 创新切入点最强。详见 `R003-gw-read-e3-test-verdict.md`。
>
> **补论文精读闭环（2026-06-16 续）**：用户选 (a) 补论文，检索+筛选+下载 6 篇（5 OA 成功 + Liu Elsevier 付费墙 manual_required），精读 5 篇。**B1 gap 经 3 篇坐实成立（强）**：Panasiewicz（同组前作，幅度级湍流，环路 TF 无湍流相位）+ Paillier（AO+DPLL 分治范本）+ Valjus（2025 综述，DSP 流水线无湍流相位模块）。精确 gap 表述："现有星地相干载波同步用分治架构——多普勒由 DPLL/OPLL 数字域跟踪，湍流由 AO 光域或简化为 scintillation 衰落，没有工作把湍流相位扰动纳入 PLL 环路传递函数，更没有联合建模多普勒斜率与湍流相位统计"。**A3 场景迁移可行**：Wang 组两篇 FSO 帧导频 FOE 已在相位屏湍流下成熟，但三重障碍（多普勒时变/deep fade 相位跳变/单孔径无分集）未解决，是迁移切入点。详见 `R004-b1-gap-verified-a3-migration.md`。
>
> **read-traceability 实战发现（2026-06-16）**：`10.1364_ol.596189` 是 title_verify 的盲区 case——title 来自 abstract 页 H1（与正式 title 一致，判 match 1.0），但 firecrawl 只抓到付费墙 abstract 页，正文不可读。**title_verify 能判 title↔content 标题一致性，但判不了"content 是否含正文"**。归 read-traceability 改进项。
>
> **失败论文**：A2-SPIE `10.1117/12.3082273`（RNN 载波恢复）Firecrawl 超时，标 manual_required。
